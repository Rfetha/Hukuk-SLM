#!/usr/bin/env python
"""G1 — Hakem-geçerliliği: cross-judge uyumu (κ) + yazar spot-check. Literatür: RAGBench/RAGTruth
(LLM-judge'i insana/ikinci hakeme karşı doğrula, %93-95 / %91.8 uyum bildiriliyor).

Bizim tüm skorlar gpt-4o-mini'den → tek hakem akademik olarak eksik. Bu araç üç iş yapar:

  (1) CROSS-JUDGE uyumu: aynı kayıtların iki hakemce (gpt-4o-mini vs gpt-4o) skorlarını karşılaştır.
        python scripts/judge_agreement.py cross --a outputs/eval/abst_X.jsonl \
               --b outputs/eval/abst_X_gpt4o.jsonl --field verdict --kind cat
      (Önce ikinci hakemi koş: score_abstention/groundedness --judge-model gpt-4o --label X_gpt4o)

  (2) SPOT-CHECK export: N kaydı elle etiketlemen için CSV'ye çıkar (yazar-doğrulama).
        python scripts/judge_agreement.py export --a outputs/eval/abst_X.jsonl --n 30 \
               --out outputs/eval/spotcheck_X.csv

  (3) AUTHOR uyumu: doldurduğun CSV'yi oku, yazar↔hakem uyumu + κ.
        python scripts/judge_agreement.py author --csv outputs/eval/spotcheck_X.csv --field verdict

Çıktı: uyum % + Cohen's κ (kategorik) veya Pearson r (sayısal). κ≥0.6 makul, ≥0.8 güçlü.
"""
import argparse
import csv
import json
import os


def load_jsonl(p):
    rows = json.load(open(p, encoding="utf-8")) if p.endswith(".json") else \
        [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
    return rows if isinstance(rows, list) else [rows]


def cohen_kappa(a, b):
    """İki etiketçi (a,b) listesi → Cohen's κ (kategorik)."""
    cats = sorted(set(a) | set(b))
    n = len(a)
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    return round(po, 3), round((po - pe) / (1 - pe), 3) if pe < 1 else 1.0


def pearson(a, b):
    n = len(a); ma = sum(a) / n; mb = sum(b) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    va = sum((x - ma) ** 2 for x in a) ** 0.5
    vb = sum((y - mb) ** 2 for y in b) ** 0.5
    return round(cov / (va * vb), 3) if va and vb else 0.0


def cross(a):
    A = {r["id"]: r for r in load_jsonl(a.a)}
    B = {r["id"]: r for r in load_jsonl(a.b)}
    ids = sorted(set(A) & set(B))
    va = [A[i].get(a.field) for i in ids]
    vb = [B[i].get(a.field) for i in ids]
    print(f"[cross-judge] {a.field} | n={len(ids)} | A={os.path.basename(a.a)} B={os.path.basename(a.b)}")
    if a.kind == "cat":
        po, k = cohen_kappa([str(x) for x in va], [str(x) for x in vb])
        print(f"  uyum={po:.1%}  Cohen's κ={k}  ({'güçlü' if k>=0.8 else 'makul' if k>=0.6 else 'ZAYIF'})")
    else:
        r = pearson([float(x or 0) for x in va], [float(x or 0) for x in vb])
        print(f"  Pearson r={r}  ({'güçlü' if abs(r)>=0.8 else 'makul' if abs(r)>=0.6 else 'ZAYIF'})")


def export(a):
    rows = load_jsonl(a.a)[: a.n]
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "soru", "cevap", "judge_verdict", "AUTHOR_verdict(elle doldur)"])
        for r in rows:
            w.writerow([r.get("id"), (r.get("soru") or "")[:120], (r.get("cevap") or "")[:300],
                        r.get("verdict") or r.get("label") or "", ""])
    print(f"[export] {len(rows)} kayıt → {a.out}  (son sütunu elle doldur, sonra: author modu)")


def author(a):
    rows = list(csv.DictReader(open(a.csv, encoding="utf-8")))
    pairs = [(r["judge_verdict"].strip(), r[[k for k in r if k.startswith("AUTHOR")][0]].strip())
             for r in rows if r.get("judge_verdict", "").strip() and
             r[[k for k in r if k.startswith("AUTHOR")][0]].strip()]
    if not pairs:
        print("[author] elle doldurulmuş satır yok"); return
    j, au = zip(*pairs)
    po, k = cohen_kappa(list(j), list(au))
    print(f"[author↔judge] n={len(pairs)} | uyum={po:.1%}  Cohen's κ={k}  "
          f"({'güçlü' if k>=0.8 else 'makul' if k>=0.6 else 'ZAYIF'})")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("cross"); c.add_argument("--a", required=True); c.add_argument("--b", required=True)
    c.add_argument("--field", default="verdict"); c.add_argument("--kind", choices=["cat", "num"], default="cat")
    e = sub.add_parser("export"); e.add_argument("--a", required=True); e.add_argument("--n", type=int, default=30)
    e.add_argument("--out", required=True)
    au = sub.add_parser("author"); au.add_argument("--csv", required=True); au.add_argument("--field", default="verdict")
    a = p.parse_args()
    {"cross": cross, "export": export, "author": author}[a.cmd](a)


if __name__ == "__main__":
    main()
