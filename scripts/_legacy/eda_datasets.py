#!/usr/bin/env python
"""İndirilen hukuk veri setleri için EDA (keşifsel veri analizi).

Her set için: satır sayısı, sütunlar, boş/mükerrer oranı, soru/cevap uzunluk
dağılımı, en sık tekrar eden sorular ve örnek satırlar.

Kullanım: python scripts/eda_datasets.py
"""
import sys
import pandas as pd
from datasets import load_dataset

pd.set_option("display.width", 120)

# (hf_id, soru_sütunu, cevap_sütunu)
TARGETS = [
    ("OrionCAF/turkish_law_qa_dataset", "question", "answer"),
    ("Renicames/turkish-law-chatbot", "Soru", "Cevap"),
]


def eda(hf_id, qcol, acol):
    print("\n" + "=" * 80)
    print(f"EDA: {hf_id}")
    print("=" * 80)
    ds = load_dataset(hf_id)
    print(f"split'ler: { {k: len(v) for k, v in ds.items()} }")
    # tüm split'leri birleştir
    df = pd.concat([ds[s].to_pandas() for s in ds.keys()], ignore_index=True)
    print(f"toplam satır: {len(df):,} | sütunlar: {list(df.columns)}")

    q, a = df[qcol].astype(str), df[acol].astype(str)

    # boşluk / mükerrer
    empty_q = (q.str.strip() == "").sum()
    empty_a = (a.str.strip() == "").sum()
    dup_pair = df.duplicated(subset=[qcol, acol]).sum()
    dup_q = df.duplicated(subset=[qcol]).sum()
    print(f"\nboş soru: {empty_q} | boş cevap: {empty_a}")
    print(f"birebir mükerrer (soru+cevap): {dup_pair:,} (%{100*dup_pair/len(df):.1f})")
    print(f"mükerrer soru: {dup_q:,} (%{100*dup_q/len(df):.1f})")

    # uzunluk dağılımı (kelime)
    qw, aw = q.str.split().map(len), a.str.split().map(len)
    print("\nsoru uzunluğu (kelime):")
    print(qw.describe(percentiles=[.5, .9, .99]).round(1).to_string())
    print("\ncevap uzunluğu (kelime):")
    print(aw.describe(percentiles=[.5, .9, .99]).round(1).to_string())

    # çok kısa cevaplar (kalite şüphesi)
    short_a = (aw < 5).sum()
    print(f"\n5 kelimeden kısa cevap: {short_a} (%{100*short_a/len(df):.1f})")

    # en sık tekrar eden sorular
    print("\nen sık 3 soru:")
    for txt, c in q.value_counts().head(3).items():
        print(f"  ({c}x) {txt[:90]}")

    # örnekler
    print("\n--- 2 rastgele örnek ---")
    for _, row in df.sample(2, random_state=42).iterrows():
        print(f"  Q: {str(row[qcol])[:140]}")
        print(f"  A: {str(row[acol])[:220]}")
        print("  " + "-" * 40)


if __name__ == "__main__":
    for t in TARGETS:
        try:
            eda(*t)
        except Exception as e:
            print(f"\n! {t[0]} EDA hatası: {e}", file=sys.stderr)
