### 2026-06-08 — Grounded pivot → v1 verisi + kalite kapısı
- **Hamle:** doğruluğu **gerçek kanun maddesinden imal et** (madde → GPT-4o-mini Q&A üretir → doğrula).
- **Veri:** `data/processed/sft_v1/` — **21.458 grounded Q&A** (train 19.305 / val 1.131 / test 1.022), ~$1.16. Kaynak = 2.759 madde, **10 çekirdek kanun** (TMK,TBK,İİK,İş,TKHK,Aile,HMK,KatMülk,TCK,CMK). Üslup: **kısa, sade, vatandaş** (üretim promptu öyle diyor). 32K forum KATILMADI.
- **Filtre:** `gen_grounded.py::usable()` ham 40K'dan değişiklik/stub/mülga maddelerini eler (40K→21K→çekirdek 2.759).
- **Eğitim-öncesi kalite kapısı (ADR-0002):** `score_grounded_corpus.py`, n=40 → **faithfulness 0.984**, hall 0.016, cit_precision 1.0, wrong_ref 0.0. → veri temiz.

