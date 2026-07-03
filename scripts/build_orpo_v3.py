#!/usr/bin/env python3
"""v3 ADIM 6a — ORPO train.jsonl paketleme (abstain-çifti + grounding-replay, is_pref interleave).

v3_recipe Q4/Q6/Q8 + framing kararı. Her satır TRL conversational-preference şeması:
  {"prompt":[msgs], "chosen":[{assistant}], "rejected":[{assistant}], "is_pref":0/1}

İKİ SATIR TİPİ (framing kendi sınav-moduna eşlenir):
  · abstain-çifti (is_pref=1): ORACLE framing (eval M2). prompt=SYSTEM_PROMPT_RAG + "KAYNAK MADDE:
    {trap_text[:900]}". chosen=muhakemeli-red (gen_v3_chosen). rejected=v2b GERÇEK fabrikasyonu
    (gen_v3_rejected, yalnız abstained=False). MaskedORPOTrainer'da OR-terimi AKTİF.
  · grounding-replay (is_pref=0): RAG_MULTI framing (M1 koruması). prompt/chosen = v2b'nin grounded
    örneği (reuse, sft_v2b). rejected = KISA placeholder (~13 sıradan token; NaN-hijyeni, tek-token DEĞİL).
    MaskedORPOTrainer'da OR-terimi SIFIRLANIR → yalnız NLL(chosen) = SFT-replay.

is_pref DETERMİNİSTİK INTERLEAVE (random DEĞİL): grounding her `step` konumda bir → micro-batch'ler
karışık, OR-sinyali seyrelmez (per_device × grad_accum ≥ 64 çift emniyet).

dev.jsonl id'leri eğitimden ÇIKARILIR (sızıntı yok). ADIM 4 judge τ'sü RAFİNE edene kadar
hi_overlap fabrikasyonlar da DAHİL (provizyonel geçerlilik; işaretli).

Kullanım (rejected.jsonl geldikten sonra):
  python scripts/build_orpo_v3.py --rejected data/processed/sft_v3/rejected.jsonl
  # SMOKE (fixture ile):
  python scripts/build_orpo_v3.py --rejected data/processed/sft_v3/rejected_batchtest.jsonl --out-dir /tmp/orpo_smoke
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raft_pack import SYSTEM_PROMPT_RAG_MULTI

# ORACLE framing (gen_v3_rejected ile AYNI — abstain-çifti prompt'u eval M2'yi hedefler).
SYSTEM_PROMPT_RAG = (
    "Sen HakHukuk'sun. Türk hukuku hakkında sade, anlaşılır Türkçe bilgi verirsin.\n"
    "Sana bir KAYNAK madde metni verilecek. Cevabını YALNIZCA bu kaynağa dayandır; "
    "kaynakta olmayan bilgi veya madde numarası UYDURMA.\n"
    "Cevabını kısa ve anlaşılır tut; dayandığın kanun ve madde numarasını belirt."
)

# Grounding-replay rejected placeholder: kısa, ~13 sıradan token, tek-token DEĞİL (NaN-hijyeni).
# İçeriği loss'a girmez (is_pref=0 → OR maskeli), yalnız concat şeklini sağlar.
PLACEHOLDER_REJECTED = ("Bu soru hakkında kesin bir değerlendirme yapmak için ek bilgi ve "
                        "dikkatli bir inceleme gerekmektedir.")

DEFAULTS = dict(
    packed="data/processed/sft_v3/packed_v3.jsonl",
    chosen="data/processed/sft_v3/chosen.jsonl",
    dev="data/processed/sft_v3/dev.jsonl",
    v2b_train="data/processed/sft_v2b/train.jsonl",
    out_dir="data/processed/sft_v3",
)


def load_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rejected", required=True, help="gen_v3_rejected çıktısı (fabrikasyonlar)")
    ap.add_argument("--chosen", default=DEFAULTS["chosen"])
    ap.add_argument("--dev", default=DEFAULTS["dev"])
    ap.add_argument("--v2b-train", default=DEFAULTS["v2b_train"])
    ap.add_argument("--out-dir", default=DEFAULTS["out_dir"])
    ap.add_argument("--replay-frac", type=float, default=0.20,
                    help="grounding-replay / abstain-çifti oranı (Q6 hafif replay; M1-koruma knob)")
    ap.add_argument("--max-chunk-chars", type=int, default=900, help="oracle kaynak clip (v2b eğitim uzunluğu)")
    ap.add_argument("--val-frac", type=float, default=0.03)
    ap.add_argument("--seed", type=int, default=3407)
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)

    chosen_by_id = {r["id"]: r["chosen"] for r in load_jsonl(a.chosen)}
    dev_ids = {r["id"] for r in load_jsonl(a.dev)} if os.path.exists(a.dev) else set()
    rej = load_jsonl(a.rejected)

    # --- abstain-çiftleri: yalnız GERÇEK fabrikasyon (abstained=False), dev HARİÇ, chosen mevcut ---
    pairs = []
    n_abst = n_nodev = n_nochosen = 0
    for r in rej:
        if r.get("abstained"):
            n_abst += 1
            continue
        if r["id"] in dev_ids:
            n_nodev += 1
            continue
        ch = chosen_by_id.get(r["id"])
        if not ch:
            n_nochosen += 1
            continue
        src = (r.get("trap_text") or "")[:a.max_chunk_chars]
        user = f"KAYNAK MADDE:\n{src}\n\nSORU: {r['soru']}"
        pairs.append({
            "prompt": [{"role": "system", "content": SYSTEM_PROMPT_RAG},
                       {"role": "user", "content": user}],
            "chosen": [{"role": "assistant", "content": ch}],
            "rejected": [{"role": "assistant", "content": r["model_answer"]}],
            "is_pref": 1,
            "_kind": "abstain", "_hi_overlap": r.get("judge_flag") == "hi_overlap",
        })

    # --- grounding-replay: v2b grounded örnekleri (RAG_MULTI), rejected=placeholder ---
    v2b = load_jsonl(a.v2b_train) if os.path.exists(a.v2b_train) else []
    ground_src = [r for r in v2b if r.get("slice") == "grounded"]
    import random
    random.Random(a.seed).shuffle(ground_src)
    n_ground = int(len(pairs) * a.replay_frac)
    grounds = []
    for r in ground_src[:n_ground]:
        msgs = r["messages"]
        # messages = [system(RAG_MULTI), user, assistant]
        prompt = [m for m in msgs if m["role"] in ("system", "user")]
        asst = next((m for m in msgs if m["role"] == "assistant"), None)
        if not asst:
            continue
        grounds.append({
            "prompt": prompt,
            "chosen": [{"role": "assistant", "content": asst["content"]}],
            "rejected": [{"role": "assistant", "content": PLACEHOLDER_REJECTED}],
            "is_pref": 0,
            "_kind": "ground", "_hi_overlap": False,
        })

    # --- DETERMİNİSTİK INTERLEAVE: grounding'i eşit aralıklarla serp (random shuffle DEĞİL) ---
    random.Random(a.seed + 1).shuffle(pairs)     # abstain sırası deterministik-karışık
    out = []
    if grounds:
        step = max(1, (len(pairs) + len(grounds)) // len(grounds))
        gi = 0
        for i, pr in enumerate(pairs):
            out.append(pr)
            if (i + 1) % step == 0 and gi < len(grounds):
                out.append(grounds[gi]); gi += 1
        out.extend(grounds[gi:])                 # kalan grounding sona
    else:
        out = pairs

    # --- split (deterministik) ---
    n_val = max(1, int(len(out) * a.val_frac))
    val, train = out[:n_val], out[n_val:]
    for name, part in [("train", train), ("validation", val)]:
        with open(os.path.join(a.out_dir, f"{name}.jsonl"), "w", encoding="utf-8") as f:
            for ex in part:
                f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    n_hi = sum(1 for p in pairs if p["_hi_overlap"])
    report = {
        "abstain_pairs": len(pairs), "grounding_replay": len(grounds),
        "total": len(out), "train": len(train), "validation": len(val),
        "replay_frac_eff": round(len(grounds) / max(1, len(pairs)), 3),
        "interleave_step": (max(1, (len(pairs) + len(grounds)) // len(grounds)) if grounds else None),
        "skipped": {"abstained_no_contrast": n_abst, "dev_excluded": n_nodev, "no_chosen": n_nochosen},
        "hi_overlap_provisional": n_hi,
        "note": "hi_overlap fabrikasyonlar DAHİL (ADIM 4 judge τ'sü RAFİNE edecek). is_pref=1 abstain, 0 grounding.",
    }
    json.dump(report, open(os.path.join(a.out_dir, "orpo_report.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"[v3-orpo] → {a.out_dir}/{{train,validation}}.jsonl (+ orpo_report.json)")


if __name__ == "__main__":
    main()
