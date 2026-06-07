#!/usr/bin/env python
"""Doğrulanmış hazır Q&A setlerini tek, temiz, chat-template SFT v0 setine birleştirir.

- Kaynaklar: OrionCAF/turkish_law_qa_dataset, Renicames/turkish-law-chatbot
- Temizlik: strip, boş/kısa cevap süz, birebir + çapraz mükerrer at
- Format: {"messages":[{"role":"user",...},{"role":"assistant",...}], "source":...}
- Çıktı: data/processed/sft_v0/{train,validation,test}.jsonl

Not: bu v0 SFT verisi UZMAN dilinde. Sadeleştirme katmanı sonraki adımda (grounded üretim) eklenecek.
Kullanım: python scripts/build_sft_dataset.py
"""
import json
import hashlib
from pathlib import Path
import pandas as pd
from datasets import load_dataset

OUT = Path("data/processed/sft_v0")
SOURCES = [
    ("OrionCAF/turkish_law_qa_dataset", "question", "answer"),
    ("Renicames/turkish-law-chatbot", "Soru", "Cevap"),
]
MIN_ANSWER_WORDS = 5


def load_all():
    frames = []
    for hf_id, qcol, acol in SOURCES:
        ds = load_dataset(hf_id)
        df = pd.concat([ds[s].to_pandas() for s in ds.keys()], ignore_index=True)
        df = df[[qcol, acol]].rename(columns={qcol: "question", acol: "answer"})
        df["source"] = hf_id.split("/")[-1]
        frames.append(df)
        print(f"  yüklendi {hf_id}: {len(df):,}")
    return pd.concat(frames, ignore_index=True)


def clean(df):
    n0 = len(df)
    df["question"] = df["question"].astype(str).str.strip()
    df["answer"] = df["answer"].astype(str).str.strip()
    # boş
    df = df[(df["question"] != "") & (df["answer"] != "")]
    # kısa cevap süz
    df = df[df["answer"].str.split().map(len) >= MIN_ANSWER_WORDS]
    # birebir mükerrer (soru+cevap)
    df = df.drop_duplicates(subset=["question", "answer"])
    # çapraz mükerrer soru (ilkini tut)
    df = df.drop_duplicates(subset=["question"])
    print(f"  temizlik: {n0:,} -> {len(df):,} (-{n0-len(df):,})")
    return df.reset_index(drop=True)


def to_messages(row):
    return {
        "messages": [
            {"role": "user", "content": row["question"]},
            {"role": "assistant", "content": row["answer"]},
        ],
        "source": row["source"],
    }


def split(df, seed=42):
    # deterministik hash tabanlı split (yeni veri eklenince stabil kalır)
    def bucket(q):
        h = int(hashlib.md5(q.encode("utf-8")).hexdigest(), 16) % 100
        return "test" if h < 5 else ("validation" if h < 10 else "train")
    df["_split"] = df["question"].map(bucket)
    return df


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    df = load_all()
    df = clean(df)
    df = split(df)
    counts = {}
    for sp in ["train", "validation", "test"]:
        part = df[df["_split"] == sp]
        counts[sp] = len(part)
        with open(OUT / f"{sp}.jsonl", "w", encoding="utf-8") as f:
            for _, row in part.iterrows():
                f.write(json.dumps(to_messages(row), ensure_ascii=False) + "\n")
    print(f"\nyazıldı -> {OUT}")
    print(f"  {counts} (toplam {sum(counts.values()):,})")
    print(f"  kaynak dağılımı:\n{df['source'].value_counts().to_string()}")


if __name__ == "__main__":
    main()
