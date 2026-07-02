#!/usr/bin/env python
"""Grounded eval üretici — base vs v1 karşılaştırması için MODEL cevabı + GERÇEK madde referansı.

Boşluk: `eval.py` referans=avukat-cevabı koyar; `groundedness.py --mode data` ise referans=
GERÇEK madde metni ister. `score_grounded_corpus.py` o madde-join köprüsünü yapar ama KORPUSU
(gold cevap) skorlar, model çıktısını değil. Bu script ikisini birleştirir:

  test.jsonl sorusu → model (base VEYA base+adapter, 4-bit) cevap üret
    → (kanun_no|madde_no) ile data/raw/mevzuat_maddeler.jsonl'den GERÇEK madde metnini join et
    → detail.jsonl {soru, referans=madde metni, cevap=model çıktısı} → groundedness.py --mode data

Böylece base ve v1 TAM AYNI grounded sorularla, gerçek maddeye karşı ölçülür (dürüst kapı).
Örneklem deterministik (sabit seed) → base ve v1 aynı soruları görür.

Kullanım:
  # Base (referans):
  python scripts/gen_eval_grounded.py --label eval_base --n 40
  # v1 adapter:
  python scripts/gen_eval_grounded.py --label eval_v1 --adapter outputs/v1 --n 40
  # Smoke (üretim+join testi, hızlı):
  python scripts/gen_eval_grounded.py --label smoke --n 2 --adapter outputs/v1

Sonra:
  python scripts/groundedness.py --details outputs/eval/eval_v1_detail.jsonl --label eval_v1 --mode data
"""
import argparse
import json
import os
import random

# Unsloth, torch'tan ÖNCE (train_sft.py/eval.py ile aynı kural).
from unsloth import FastModel
import torch

# eval.py ile AYNI system prompt — eğitim/eval/üretim tutarlı olsun.
SYSTEM_PROMPT = (
    "Sen HakHukuk'sun. Türk hukuku hakkında sade, anlaşılır Türkçe bilgi verirsin.\n"
    "Emin olmadığın konularda \"Bu konuda güncel mevzuata veya bir avukata "
    "danışmanızı öneririm\" dersin.\n"
    "Asla kanun maddesi veya bilgi uydurmaz, tahmin etmezsin.\n"
    "Cevabını kısa ve anlaşılır tut; ilgili kanun ve madde numarasını belirt."
)

# RAG-modu (--with-source): madde metni prompt'a verilir → model EZBERDEN değil VERİLEN
# kaynaktan cevaplar+atıf yapar. Deploy ortamı (Faz 2 RAG) ile eşleşen ADİL test.
SYSTEM_PROMPT_RAG = (
    "Sen HakHukuk'sun. Türk hukuku hakkında sade, anlaşılır Türkçe bilgi verirsin.\n"
    "Sana bir KAYNAK madde metni verilecek. Cevabını YALNIZCA bu kaynağa dayandır; "
    "kaynakta olmayan bilgi veya madde numarası UYDURMA.\n"
    "Cevabını kısa ve anlaşılır tut; dayandığın kanun ve madde numarasını belirt."
)

# M1/M3 — çok-kaynak (RAFT/distractor) sistem promptu: ortak modülden (eğitim ile AYNI, ADR-0013).
import raft_pack
SYSTEM_PROMPT_RAG_MULTI = raft_pack.SYSTEM_PROMPT_RAG_MULTI

# EVAL-MIRROR (2026-07-02, ADR-0013): eğitimin 900-char chunk clip'ini eval tarafında AYNEN
# kullan. Yoksa v2b, eğitildiğinden UZUN context'le ölçülür (haksız). clip_sources_block eğitimle
# birebir aynı fonksiyon → dağılım garantili eşleşir. (build_sft_v2b saf stdlib, torch/unsloth yok.)
from build_sft_v2b import clip_sources_block

MADDE_PATH = "data/raw/mevzuat_maddeler.jsonl"


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default=os.environ.get(
        "BASE_MODEL", "google/gemma-4-12B-it-qat-q4_0-unquantized"))
    p.add_argument("--adapter", default=None,
                   help="LoRA adapter dizini (ör. outputs/v1); yoksa ham base")
    p.add_argument("--data", default="data/processed/sft_v1/test.jsonl")
    p.add_argument("--madde-path", default=MADDE_PATH)
    p.add_argument("--label", required=True, help="çıktı etiketi (eval_base / eval_v1)")
    p.add_argument("--n", type=int, default=40)
    p.add_argument("--seed", type=int, default=3407)
    p.add_argument("--max-seq-len", type=int, default=2048)
    p.add_argument("--max-new-tokens", type=int, default=512)
    p.add_argument("--out-dir", default="outputs/eval")
    p.add_argument("--with-source", action="store_true",
                   help="M4 RAG-modu: TEK gold madde metnini prompt'a koy (temiz Oracle, iyimser tavan)")
    p.add_argument("--distractors", type=int, default=0, metavar="N",
                   help="M1: gold + N hard-negative distractor (RAFT çok-kaynak). v2b grounding manşeti.")
    p.add_argument("--max-chunk-chars", type=int, default=900, metavar="N",
                   help="eval-mirror: her [KAYNAK] chunk'ını N char'a kırp — eğitim §5.1 truncation "
                        "fix ile AYNI (900≈243 tok; 5 chunk 2048'e sığar). 0=kapalı. v2b'yi eğitildiği "
                        "context uzunluğuyla ölçmek için ŞART (ADR-0013). Sadece --distractors modunda etkin.")
    p.add_argument("--empty-context", action="store_true",
                   help="M3 (E-set): hiç kaynak verme (boş bağlam) → doğru davranış=abstention")
    p.add_argument("--no-gold", action="store_true",
                   help="M2 training-matched: --distractors ile gold'u ÇIKAR (sadece distractor, "
                        "RAG_MULTI prompt) → RAG-ıska abstention. v2b eğitim abstain dilimiyle AYNI mod.")
    return p.parse_args()


def norm(v):
    return "" if v is None else str(v).strip()


def load_madde_index(path):
    """(kanun_no|madde_no) → en dolu madde metni (score_grounded_corpus ile aynı mantık)."""
    idx = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            k = f"{norm(r.get('kanun_no'))}|{norm(r.get('madde_no'))}"
            t = (r.get("text") or "").strip()
            if t and len(t) > len(idx.get(k, "")):
                idx[k] = t
    return idx


def extract(rec):
    msgs = rec.get("messages", [])
    soru = next((m["content"] for m in msgs if m["role"] == "user"), None)
    return soru


def build_model(args):
    model, tokenizer = FastModel.from_pretrained(
        model_name=args.model,
        max_seq_length=args.max_seq_len,
        load_in_4bit=True,
        full_finetuning=False,
    )
    if args.adapter:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, args.adapter)
        print(f"[gen-eval] adapter yüklendi: {args.adapter}")
    FastModel.for_inference(model)
    return model, tokenizer


def generate(model, tokenizer, soru, max_new_tokens, source=None, sources_block=None):
    if sources_block is not None:  # M1/M3: çok-kaynak (distractor) veya boş bağlam
        sys = SYSTEM_PROMPT_RAG_MULTI
        user = f"KAYNAKLAR:\n{sources_block}\n\nSORU: {soru}"
    elif source:  # M4: tek gold kaynak
        sys = SYSTEM_PROMPT_RAG
        user = f"KAYNAK MADDE:\n{source[:3500]}\n\nSORU: {soru}"
    else:       # M5 kör mod: sadece soru (parametrik bilgi testi)
        sys = SYSTEM_PROMPT
        user = soru
    msgs = [
        {"role": "system", "content": sys},
        {"role": "user", "content": user},
    ]
    inputs = tokenizer.apply_chat_template(
        msgs, tokenize=True, add_generation_prompt=True,
        return_tensors="pt",
    ).to(model.device)
    with torch.no_grad():
        out = model.generate(
            input_ids=inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,            # deterministik — tekrar-üretilebilir eval
            temperature=None, top_p=None, top_k=None,
            pad_token_id=tokenizer.eos_token_id,
        )
    gen = out[0][inputs.shape[1]:]
    return tokenizer.decode(gen, skip_special_tokens=True).strip()


def main():
    a = parse_args()
    os.makedirs(a.out_dir, exist_ok=True)

    rows = [json.loads(l) for l in open(a.data, encoding="utf-8") if l.strip()]
    idx = load_madde_index(a.madde_path)

    # M1 distractor modu → ortak RAFT paketleyici (build_sft_v2b ile AYNI; ADR-0013).
    pool_recs = pool_by_kanun = None
    if a.distractors > 0:
        pool_recs, pool_by_kanun = raft_pack.load_madde_pool(a.madde_path)
        print(f"[gen-eval] distractor havuzu: {len(pool_recs)} madde "
              f"({len(pool_by_kanun)} kanun) | k={a.distractors} hard-negative")

    # Madde metni JOIN olanlardan deterministik örneklem (kapsam=%100 garanti).
    pool = []
    for r in rows:
        k = f"{norm(r.get('kanun_no'))}|{norm(r.get('madde_no'))}"
        src = idx.get(k, "")
        soru = extract(r)
        if src and soru:
            pool.append((r, soru, src))
    random.seed(a.seed)
    random.shuffle(pool)
    sample = pool[:a.n]
    print(f"[gen-eval] {a.label}: havuz={len(pool)} (madde eşleşen) → örneklem={len(sample)} "
          f"| adapter={a.adapter or '—'}")

    model, tokenizer = build_model(a)

    import random as _rnd
    detail = os.path.join(a.out_dir, f"{a.label}_detail.jsonl")
    with open(detail, "w", encoding="utf-8") as f:
        for i, (rec, soru, src) in enumerate(sample):
            # RAG-modu: kaynağı ETİKETLE (Kanun adı + Madde no) → model atıf no'sunu
            # uydurmasın, verilen etiketten kopyalasın (Faz 2 RAG: chunk atıf taşır).
            labeled_src = f"{rec.get('kanun_adi','')} {rec.get('madde_no','')}\n{src}"
            sources_block = None
            context_shown = ""
            mode = "blind"
            if a.empty_context:                         # M3 (E-set): hiç kaynak
                sources_block = "(İlgili kaynak bulunamadı.)"
                context_shown = ""
                mode = "empty"
            elif a.distractors > 0:                     # M1: gold+distractor · M2(no-gold): distractor-only
                rng = _rnd.Random(a.seed + i)           # örnek-başına deterministik
                chunks, _ = raft_pack.pack_context(
                    rec, src, pool_recs, pool_by_kanun, a.distractors, rng,
                    include_gold=not a.no_gold)         # --no-gold → gold ÇIKAR (M2 abstain, training-matched)
                sources_block = raft_pack.format_sources_block(chunks)
                if a.max_chunk_chars > 0:               # EVAL-MIRROR: eğitim clip'i (§5.1, ADR-0013)
                    # gold baş satırı = "{kanun_adi} {madde_no}" (labeled_chunk ile aynı _norm).
                    # ref cevap ##begin_quote## taşımaz (core_hard sade) → gold da baştan kırpılır;
                    # kritik olan context UZUNLUĞUNUN eğitimle eşleşmesi (v2b haksız uzun görmesin).
                    gold_label = f"{rec.get('kanun_adi','')} {rec.get('madde_no','')}"
                    ref_msgs = rec.get("messages") or []
                    ref_answer = next(
                        (m.get("content", "") for m in ref_msgs
                         if m.get("role") in ("assistant", "model")), "")
                    sources_block = clip_sources_block(
                        sources_block, ref_answer, gold_label, a.max_chunk_chars)
                context_shown = sources_block
                mode = "distractor_nogold" if a.no_gold else "distractor"
            elif a.with_source:                         # M4: tek gold
                context_shown = labeled_src
                mode = "oracle"

            cevap = generate(
                model, tokenizer, soru, a.max_new_tokens,
                source=labeled_src if (a.with_source and not a.distractors and not a.empty_context) else None,
                sources_block=sources_block)
            out = {
                "id": i,
                "soru": soru,
                "referans": src,                       # GERÇEK gold madde = yer-gerçeği (groundedness/correctness)
                "context_shown": context_shown,        # modele GERÇEKTEN gösterilen bağlam (abstention için)
                "mode": mode,
                "cevap": cevap,
                "kanun_adi": rec.get("kanun_adi"),
                "madde_no": rec.get("madde_no"),
                "kanun_no": rec.get("kanun_no"),
            }
            f.write(json.dumps(out, ensure_ascii=False) + "\n")
            print(f"  [{i+1}/{len(sample)}] ({mode}) {rec.get('kanun_adi')} {rec.get('madde_no')} "
                  f"→ {len(cevap)} kar")

    print(f"[gen-eval] detay → {detail}")
    print(f"[gen-eval] sıradaki: python scripts/groundedness.py "
          f"--details {detail} --label {a.label} --mode data")


if __name__ == "__main__":
    main()
