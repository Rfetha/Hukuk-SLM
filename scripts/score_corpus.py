#!/usr/bin/env python3
"""Bir SFT korpusundan (messages jsonl) sabit-seed örnek çek → detail.jsonl yaz.

Amaç: eğitim verisinin KENDİSİNİ skorkarttan geçirmek (modeli değil).
  - Sebep teyidi: eski 32K'nın cevapları zaten düşük legal_acc mı? → "çöp veri→çöp model".
  - İleride: grounded üretilen veriyi eğitmeden önce skorla (çıtayı geçiyor mu?).

Çıktı `{out-dir}/{label}_detail.jsonl` (id/soru/cevap/referans) → `muhakim_judge.py`
ve istenirse GPT sadelik hakemi aynı dosyayı okur.

Kullanım:
  python scripts/score_corpus.py --data data/processed/sft_v0/train.jsonl \
      --label corpus32k --n 40 --seed 3407
  python scripts/muhakim_judge.py --details outputs/eval/corpus32k_detail.jsonl
"""
import argparse
import json
import os
import random


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--data", required=True, help="messages formatında jsonl")
    p.add_argument("--label", required=True)
    p.add_argument("--n", type=int, default=40)
    p.add_argument("--seed", type=int, default=3407)
    p.add_argument("--out-dir", default="outputs/eval")
    return p.parse_args()


def extract(rec):
    msgs = rec.get("messages", [])
    soru = next((m["content"] for m in msgs if m["role"] == "user"), None)
    cevap = next((m["content"] for m in msgs if m["role"] == "assistant"), None)
    return soru, cevap


def main():
    a = parse_args()
    rows = [json.loads(l) for l in open(a.data, encoding="utf-8")]
    random.seed(a.seed)
    sample = random.sample(rows, min(a.n, len(rows)))
    os.makedirs(a.out_dir, exist_ok=True)
    op = os.path.join(a.out_dir, f"{a.label}_detail.jsonl")
    n = 0
    with open(op, "w", encoding="utf-8") as f:
        for i, rec in enumerate(sample):
            soru, cevap = extract(rec)
            if not soru or not cevap:
                continue
            # referans=cevap: korpusun kendi cevabı zaten "altın" → doğruluk için yeterli kıyas.
            out = {"id": i, "soru": soru, "referans": cevap, "cevap": cevap,
                   "dogruluk": None, "sadelik": None, "gerekce": None,
                   "source": rec.get("source")}
            f.write(json.dumps(out, ensure_ascii=False) + "\n")
            n += 1
    print(f"[corpus] {a.label}: {n}/{len(sample)} örnek → {op}  (seed={a.seed})")


if __name__ == "__main__":
    main()
