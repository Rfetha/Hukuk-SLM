#!/usr/bin/env python
"""v2b SFT veri inşası — RAFT paketleme + kalite kapısı + replay + split (V2_PLAN §5.2).

İki alt-komut (Adım 2 = teacher-LLM cevap üretimi ARADA, ayrı/compute):

  pack      Adım 1 → soru↔gold tohumundan RAFT context paketle, P-dilimine ata.
            Çıktı = teacher-LLM GİRDİSİ (cevaplar henüz YOK).
            data/processed/sft_v2b/packed.jsonl

  (— ARADA: B2 teacher-LLM packed.jsonl'a cevap üretir → answers.jsonl —)

  assemble  Adım 3/4/5 → cevapları al, DETERMİNİSTİK kapılardan geçir (verbatim⊂gold,
            atıf eşleşme, abstention-ifadesi), replay karıştır, split + chat-template yaz.
            data/processed/sft_v2b/{train,validation,test}.jsonl

Hedge mekanizması = context-yeterliliği (V2_PLAN §5.2): P dilimi gold'u context'e koyar
(grounded), (1-P) dilimi gold'u ÇIKARIR (abstention). Base-prob YOK; tek knob = P.

NOT: Adım 3'teki faithfulness≥0.95 (LLM-judge) kapısı = B3, ayrı script (mevcut groundedness
hattı). Buradaki kapılar DETERMİNİSTİK (string/regex) — ucuz ön-eleme.

Kullanım:
  python scripts/build_sft_v2b.py pack --p 0.8 --distractors 4 --seed 3407
  # (B2 cevap üretir → data/processed/sft_v2b/answers.jsonl)
  python scripts/build_sft_v2b.py assemble --answers data/processed/sft_v2b/answers.jsonl \
         --replay data/processed/replay_tr.jsonl --replay-frac 0.03
"""
import argparse
import json
import os
import random
import re

import raft_pack

SEED_PATH = "data/processed/sft_v1/train.jsonl"   # soru↔gold tohumu (v1 CEVAPLARI kullanılmaz)
MADDE_PATH = "data/raw/mevzuat_maddeler.jsonl"
OUT_DIR = "data/processed/sft_v2b"

ABSTAIN_RE = re.compile(
    r"düzenle(?:m[ie]yor|nmemiş|nmemekte)|yer al(?:m[ıi]yor|mamakta)|bulunma(?:maktadır|z|yor)|"
    r"kapsama(?:maktadır|z)|içerme(?:mektedir|z|miyor)|kaynak(?:lar)?da (?:bu|yok)",
    re.IGNORECASE)
QUOTE_RE = re.compile(r"##begin_quote##(.+?)##end_quote##", re.DOTALL)


def _norm(v):
    return "" if v is None else str(v).strip()


def load_madde_index(path):
    """(kanun_no|madde_no) → en dolu GERÇEK madde metni (gen_eval_grounded ile AYNI mantık).

    DİKKAT: sft_v1 kayıtlarındaki `source` alanı madde metni DEĞİL, provenance etiketi
    ('grounded_gpt-4o-mini'). Gerçek gold metni bu index'ten join edilir — yoksa gate
    her grounded örneği 'alıntı gold'da değil' ile reddeder (B1 bug, 2026-06-14).
    """
    idx = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            k = f"{_norm(r.get('kanun_no'))}|{_norm(r.get('madde_no'))}"
            t = (r.get("text") or "").strip()
            if t and len(t) > len(idx.get(k, "")):
                idx[k] = t
    return idx


def extract_seed(rec, madde_idx):
    """sft_v1 kaydından (soru, gold_text, meta) çıkar. gold_text madde index'ten JOIN."""
    msgs = rec.get("messages", [])
    soru = next((m["content"] for m in msgs if m.get("role") == "user"), None)
    meta = {"kanun_no": rec.get("kanun_no"), "kanun_adi": rec.get("kanun_adi"),
            "madde_no": rec.get("madde_no")}
    k = f"{_norm(meta['kanun_no'])}|{_norm(meta['madde_no'])}"
    gold_text = madde_idx.get(k, "")
    return soru, gold_text, meta


# ---------------------------------------------------------------- pack (Adım 1)
def cmd_pack(a):
    os.makedirs(OUT_DIR, exist_ok=True)
    seeds = [json.loads(l) for l in open(a.seeds, encoding="utf-8") if l.strip()]
    pool_recs, pool_by_kanun = raft_pack.load_madde_pool(a.madde_path)
    madde_idx = load_madde_index(a.madde_path)   # GERÇEK gold metni için JOIN tablosu
    rng = random.Random(a.seed)

    out_path = os.path.join(OUT_DIR, "packed.jsonl")
    n_grounded = n_abstain = n_skip = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for i, rec in enumerate(seeds):
            soru, gold_text, meta = extract_seed(rec, madde_idx)
            if not soru or not gold_text:
                n_skip += 1
                continue
            gold_rec = {"kanun_no": meta["kanun_no"], "kanun_adi": meta["kanun_adi"],
                        "madde_no": meta["madde_no"]}
            include_gold = rng.random() < a.p          # P → grounded, (1-P) → abstain
            prng = random.Random(a.seed + i)           # örnek-başına deterministik distractor
            chunks, gold_in = raft_pack.pack_context(
                gold_rec, gold_text, pool_recs, pool_by_kanun, a.distractors, prng,
                include_gold=include_gold)
            slice_kind = "grounded" if gold_in else "abstain"
            n_grounded += gold_in
            n_abstain += (not gold_in)
            f.write(json.dumps({
                "id": i,
                "soru": soru,
                "sources_block": raft_pack.format_sources_block(chunks),
                "slice": slice_kind,
                "gold_kanun_adi": meta["kanun_adi"],
                "gold_madde_no": meta["madde_no"],
                "gold_kanun_no": meta["kanun_no"],
                "gold_text": gold_text,
                # teacher-LLM (B2) bu alanları doldurur: "answer"
            }, ensure_ascii=False) + "\n")
    print(f"[pack] {out_path}: grounded={n_grounded} abstain={n_abstain} skip={n_skip} "
          f"(P={a.p}, k={a.distractors})")
    print(f"[pack] sıradaki (B2): teacher-LLM her satıra 'answer' üret → answers.jsonl")
    print(f"[pack]   grounded → CoT + ##begin_quote## [gold'dan birebir] + (KANUN, Madde X), uzman register")
    print(f"[pack]   abstain  → 'Verilen kaynaklarda ... bulunmuyor' (uydurma YOK)")


# ------------------------------------------------------------ assemble (Adım 3/4/5)
def _gate(row):
    """DETERMİNİSTİK kapı (Adım 3) — geçen örnek + ret sebebi döndür."""
    ans = (row.get("answer") or "").strip()
    if not ans:
        return False, "boş cevap"
    if row["slice"] == "grounded":
        m = QUOTE_RE.search(ans)
        if not m:
            return False, "verbatim-quote yok"
        quote = re.sub(r"\s+", " ", m.group(1)).strip()
        quote = quote.strip("\"“”„«»'‘’").strip()    # teacher metni tırnağa sarabilir → soyut
        gold_norm = re.sub(r"\s+", " ", row.get("gold_text", ""))
        if quote and quote[:60] not in gold_norm:   # alıntı gerçekten gold'da mı (⊂)
            return False, "alıntı gold'da değil (uydurma quote)"
        gold_ord = raft_pack.madde_ord(row.get("gold_madde_no"))
        if gold_ord is not None and str(gold_ord) not in ans:
            return False, "atıf madde no eşleşmiyor"
        return True, "ok"
    else:  # abstain dilimi
        if not ABSTAIN_RE.search(ans):
            return False, "abstention ifadesi yok (uydurmuş olabilir)"
        return True, "ok"


def cmd_assemble(a):
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = [json.loads(l) for l in open(a.answers, encoding="utf-8") if l.strip()]
    kept, rejected = [], []
    for r in rows:
        ok, reason = _gate(r)
        (kept if ok else rejected).append((r, reason))

    # chat-template (Adım 5 format)
    def to_chat(r):
        return {
            "messages": [
                {"role": "system", "content": raft_pack.SYSTEM_PROMPT_RAG_MULTI},
                {"role": "user", "content": f"KAYNAKLAR:\n{r['sources_block']}\n\nSORU: {r['soru']}"},
                {"role": "assistant", "content": r["answer"]},
            ],
            "slice": r["slice"],
            "gold_madde_no": r.get("gold_madde_no"),
            "gold_kanun_no": r.get("gold_kanun_no"),
        }

    examples = [to_chat(r) for r, _ in kept]

    # Adım 4 — replay karıştır (forgetting'e karşı, §5.1-D: %1-5)
    n_replay = 0
    if a.replay and os.path.exists(a.replay):
        rep = [json.loads(l) for l in open(a.replay, encoding="utf-8") if l.strip()]
        n_replay = int(len(examples) * a.replay_frac / max(1e-9, (1 - a.replay_frac)))
        random.Random(a.seed).shuffle(rep)
        for r in rep[:n_replay]:
            r["slice"] = "replay"
            examples.append(r)
    elif a.replay:
        print(f"[assemble] ⚠️ replay yolu yok ({a.replay}) → replay ATLANDI (forgetting riski, §5.1-D)")

    # Adım 5 — split (deterministik)
    random.Random(a.seed).shuffle(examples)
    n = len(examples)
    n_test = max(1, int(n * a.test_frac))
    n_val = max(1, int(n * a.val_frac))
    test, val, train = examples[:n_test], examples[n_test:n_test + n_val], examples[n_test + n_val:]

    for name, part in [("train", train), ("validation", val), ("test", test)]:
        p = os.path.join(OUT_DIR, f"{name}.jsonl")
        with open(p, "w", encoding="utf-8") as f:
            for ex in part:
                f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    # kapı raporu (B3 deterministik kısmı)
    from collections import Counter
    rej_reasons = Counter(reason for _, reason in rejected)
    report = {
        "in": len(rows), "kept": len(kept), "rejected": len(rejected),
        "reject_reasons": dict(rej_reasons), "replay_added": n_replay,
        "split": {"train": len(train), "validation": len(val), "test": len(test)},
    }
    json.dump(report, open(os.path.join(OUT_DIR, "assemble_report.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"[assemble] → {OUT_DIR}/{{train,validation,test}}.jsonl  (+ assemble_report.json)")
    print("[assemble] NOT: faithfulness≥0.95 LLM-judge kapısı (B3) AYRI: groundedness hattı.")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    pp = sub.add_parser("pack", help="Adım 1 — RAFT context paketle (teacher-LLM girdisi)")
    pp.add_argument("--seeds", default=SEED_PATH)
    pp.add_argument("--madde-path", default=MADDE_PATH)
    pp.add_argument("--p", type=float, default=0.8, help="grounded oranı (gold context'te); (1-P)=abstention")
    pp.add_argument("--distractors", type=int, default=4, help="örnek başına distractor (k)")
    pp.add_argument("--seed", type=int, default=3407)
    pp.set_defaults(func=cmd_pack)

    ap2 = sub.add_parser("assemble", help="Adım 3/4/5 — kapı + replay + split")
    ap2.add_argument("--answers", required=True, help="B2 çıktısı (packed + 'answer' alanı)")
    ap2.add_argument("--replay", default=None, help="genel TR instruction jsonl (chat-template)")
    ap2.add_argument("--replay-frac", type=float, default=0.03, help="replay oranı (§5.1-D: %1-5)")
    ap2.add_argument("--val-frac", type=float, default=0.05)
    ap2.add_argument("--test-frac", type=float, default=0.05)
    ap2.add_argument("--seed", type=int, default=3407)
    ap2.set_defaults(func=cmd_assemble)

    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
