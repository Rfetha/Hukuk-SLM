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
                   help="RAG-modu: madde metnini prompt'a koy (ezber değil, verilen kaynaktan cevap)")
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


def generate(model, tokenizer, soru, max_new_tokens, source=None):
    if source:  # RAG-modu: kaynağı prompt'a koy
        sys = SYSTEM_PROMPT_RAG
        user = f"KAYNAK MADDE:\n{source[:3500]}\n\nSORU: {soru}"
    else:       # kör mod: sadece soru (parametrik bilgi testi)
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

    detail = os.path.join(a.out_dir, f"{a.label}_detail.jsonl")
    with open(detail, "w", encoding="utf-8") as f:
        for i, (rec, soru, src) in enumerate(sample):
            # RAG-modu: kaynağı ETİKETLE (Kanun adı + Madde no) → model atıf no'sunu
            # uydurmasın, verilen etiketten kopyalasın (Faz 2 RAG: chunk atıf taşır).
            labeled_src = f"{rec.get('kanun_adi','')} {rec.get('madde_no','')}\n{src}"
            cevap = generate(model, tokenizer, soru, a.max_new_tokens,
                             source=labeled_src if a.with_source else None)
            out = {
                "id": i,
                "soru": soru,
                "referans": src,                       # GERÇEK madde metni = yer-gerçeği
                "cevap": cevap,
                "kanun_adi": rec.get("kanun_adi"),
                "madde_no": rec.get("madde_no"),
                "kanun_no": rec.get("kanun_no"),
            }
            f.write(json.dumps(out, ensure_ascii=False) + "\n")
            print(f"  [{i+1}/{len(sample)}] {rec.get('kanun_adi')} {rec.get('madde_no')} "
                  f"→ {len(cevap)} kar")

    print(f"[gen-eval] detay → {detail}")
    print(f"[gen-eval] sıradaki: python scripts/groundedness.py "
          f"--details {detail} --label {a.label} --mode data")


if __name__ == "__main__":
    main()
