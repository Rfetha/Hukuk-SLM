#!/usr/bin/env python
"""
Sabit-seed eval örneklemi dondurucu (Faz 1, Adım 1).

`data/eval/citizen_qa_eval.jsonl` (2080 gerçek vatandaş sorusu + avukat cevabı)
içinden deterministik N soru seçer → `data/eval/eval_sample_v1.jsonl`.

Amaç: base ve v0 (ve sonraki tüm iterasyonlar) TAM AYNI sorularla ölçülsün.
Seed sabit → tekrar çalıştırınca aynı örneklem çıkar. Dosya bir kez donar,
commit edilir; eval.py her zaman bu donmuş dosyayı okur.

Kullanım:
  python scripts/make_eval_sample.py --n 30 --seed 3407
"""
import argparse
import json
import random

SRC = "data/eval/citizen_qa_eval.jsonl"
OUT = "data/eval/eval_sample_v1.jsonl"

# Çok kısa/çok uzun soru-cevapları ele (judge için dengeli, anlamlı örnekler).
MIN_Q = 40      # soru en az ~40 karakter (anlamlı bir vaka)
MAX_Q = 1800    # çok uzun duvar metinleri at (generation/judge token şişmesin)
MIN_A = 80      # referans avukat cevabı en az ~80 karakter (boş/placeholder değil)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=30)
    p.add_argument("--seed", type=int, default=3407)
    p.add_argument("--src", default=SRC)
    p.add_argument("--out", default=OUT)
    args = p.parse_args()

    rows = []
    with open(args.src, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            q = (r.get("soru") or "").strip()
            a = (r.get("referans_cevap") or "").strip()
            if MIN_Q <= len(q) <= MAX_Q and len(a) >= MIN_A:
                rows.append({"soru": q, "referans_cevap": a,
                             "nis": r.get("nis") or r.get("etiket") or ""})

    rng = random.Random(args.seed)
    rng.shuffle(rows)
    sample = rows[: args.n]

    with open(args.out, "w", encoding="utf-8") as f:
        for i, r in enumerate(sample):
            r["id"] = i
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"[make_eval_sample] uygun {len(rows)} sorudan {len(sample)} seçildi "
          f"(seed={args.seed}) → {args.out}")


if __name__ == "__main__":
    main()
