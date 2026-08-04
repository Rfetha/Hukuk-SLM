#!/usr/bin/env python3
"""S3a ön-prob — retriever altın maddeyi bulabiliyor mu? `recall@k`.

Model çağrısı YOK, hakem YOK, GPU YOK. Altın etiket zaten elimizde: DEV soruları
maddelerden üretildi.

⛔ ÖN-KAYITLI EŞİKLER (sayı görülmeden yazıldı, değiştirilemez):
   recall@10 ≥ %90   → S3 planı aynen koşar
   recall@10 %70-90  → hibrit (BM25 + yoğun) eklenir, S3 büyür
   recall@10 < %70   → DUR, insana sor — sorun korpus yapısında

Kullanım:
  python scripts/recall_olc.py --yontem bm25 --out outputs/eval/s3a-on-prob
  python scripts/recall_olc.py --yontem yogun --model intfloat/multilingual-e5-base --out ...
"""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from madde_anahtar import madde_anahtari, korpus_indeksi  # noqa: E402,F401

KORPUS = "data/corpus/mevzuat_maddeler.jsonl"
DEV = "data/eval/dev/core_hard.jsonl"
KLER = (1, 5, 10, 20)


def recall_at_k(siralar: list, k: int) -> float:
    """Altının ilk k içinde geldiği oran. `sira=None` → hiç gelmedi."""
    if not siralar:
        return 0.0
    return sum(1 for s in siralar if s is not None and s < k) / len(siralar)


def korpus_yukle():
    kayitlar = [json.loads(l) for l in open(KORPUS, encoding="utf-8") if l.strip()]
    anahtarlar = [madde_anahtari(r["kanun_no"], r["madde_no"]) for r in kayitlar]
    # Gömülecek metin: kanun adı + madde no + gövde. Kanun adı ayırt edici bir sinyal.
    metinler = [f"{r['kanun_adi']} {r['madde_no']} {r['text']}" for r in kayitlar]
    return kayitlar, anahtarlar, metinler


def dev_yukle():
    dev = [json.loads(l) for l in open(DEV, encoding="utf-8") if l.strip()]
    sorular = [d["messages"][0]["content"] for d in dev]
    altinlar = [madde_anahtari(d["kanun_no"], d["madde_no"]) for d in dev]
    return sorular, altinlar


def sirala_bm25(metinler, sorular, en_fazla):
    from rank_bm25 import BM25Okapi
    bm25 = BM25Okapi([m.lower().split() for m in metinler])
    return [bm25.get_scores(s.lower().split()).argsort()[::-1][:en_fazla] for s in sorular]


def sirala_yogun(metinler, sorular, en_fazla, model_adi):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_adi, device="cpu")
    K = model.encode(metinler, batch_size=64, normalize_embeddings=True,
                     show_progress_bar=True, convert_to_numpy=True)
    S = model.encode(sorular, normalize_embeddings=True, convert_to_numpy=True)
    return [(S[i] @ K.T).argsort()[::-1][:en_fazla] for i in range(len(sorular))]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--yontem", choices=["bm25", "yogun"], required=True)
    p.add_argument("--model", default="intfloat/multilingual-e5-base",
                   help="yalnız --yontem yogun için")
    p.add_argument("--out", required=True)
    a = p.parse_args()

    os.makedirs(a.out, exist_ok=True)
    kayitlar, anahtarlar, metinler = korpus_yukle()
    sorular, altinlar = dev_yukle()
    print(f"[s3a] korpus {len(kayitlar):,} madde · DEV {len(sorular)} soru · yöntem={a.yontem}",
          flush=True)

    en_fazla = max(KLER)
    t0 = time.time()
    if a.yontem == "bm25":
        sirali = sirala_bm25(metinler, sorular, en_fazla)
        etiket = "bm25"
    else:
        sirali = sirala_yogun(metinler, sorular, en_fazla, a.model)
        etiket = a.model.replace("/", "_")
    gecen = time.time() - t0

    # Altının kaçıncı sırada geldiği. Aynı anahtarda birden çok kayıt olabilir
    # (mükerrer/tadil) — HERHANGİ birine isabet sayılır.
    siralar = []
    for i, altin in enumerate(altinlar):
        sira = None
        for yer, ix in enumerate(sirali[i]):
            if anahtarlar[ix] == altin:
                sira = yer
                break
        siralar.append(sira)

    sonuc = {
        "yontem": etiket, "n": len(sorular), "korpus": len(kayitlar),
        "recall": {f"recall@{k}": round(recall_at_k(siralar, k), 4) for k in KLER},
        "hic_bulunmayan": sum(1 for s in siralar if s is None),
        "gecen_sure_s": round(gecen, 1),
        "esik_karari": None,  # aşağıda dolduruluyor
    }
    r10 = sonuc["recall"]["recall@10"]
    sonuc["esik_karari"] = (
        "PLAN AYNEN" if r10 >= 0.90 else
        "HIBRIT GEREKIR" if r10 >= 0.70 else
        "DUR — INSANA SOR"
    )
    yol = os.path.join(a.out, f"recall_{etiket}.json")
    json.dump(sonuc, open(yol, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(sonuc, ensure_ascii=False, indent=2))
    print(f"[s3a] → {yol}", flush=True)


if __name__ == "__main__":
    main()
