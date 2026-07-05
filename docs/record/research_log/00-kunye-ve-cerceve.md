# HakHukuk — Araştırma Kaydı (kronolojik)

> **Bu dosya ne:** Projenin **deney günlüğü** — ne yaptık, ne çıktı, ne karar verdik, paper'ın hangi
> bölümüne yarar. Tek dosya, kronolojik, **paper/rapor hammaddesi.** ADR'ler *kararı* tutar; bu dosya
> *anlatıyı + sayıları + öğrenilen dersi* tutar. Yeni anlamlı deney/bulgu → buraya bir girdi.
>
> **Paper haritası:** K1=ablasyon (base→+SFT→+madde-verili/oracle), K3=ayrışma bulguları (beklenmedik negatif sonuçlar).
> Detaylı hedef: `docs/PAPER_TARGET.md`. Kararlar: `docs/adr/`.

---

## Künye
- **Model:** Gemma 4 12B (`gemma-4-12B-it-qat-q4_0-unquantized`) + QLoRA → (Faz 3) Q4_0 GGUF.
- **Ana metrik:** groundedness — FactScore (claim böl→doğrula) + ALCE (atıf prec/recall, wrong_ref), `scripts/groundedness.py`. Hakem: gpt-4o-mini (paper'da cross-judge gpt-4o).
- **Eğitim yeri:** Modal A100. **Eval:** lokal ($0, OpenAI hakem).
- **Birincil kitle (2026-06-13 reframe):** UZMAN (avukat/hukukçu). Vatandaş = app-layer ikinci register.
- **Eval modları (terim — 2026-06-13 düzeltildi):** **KÖR** = madde prompt'ta yok, model ezberden cevaplar (parametrik bilgi testi). **MADDE-VERİLİ (oracle-context)** = doğru maddenin metni `--with-source` ile ELLE prompt'a konur. ⚠️ Bu **gerçek RAG DEĞİL** — retriever/DB yok (henüz). "Mükemmel getirme" simülasyonu, yani gerçek RAG'ın **iyimser tavanı** (gerçek retriever yanlış/eksik getirir → skorlar bundan düşük olur). Eskiden "RAG modu" deniyordu; yanıltıcı olduğu için "madde-verili" olarak yeniden adlandırıldı. Yalnız "Faz 2 RAG" ibareleri gelecekteki gerçek retriever sistemini kasteder.

---

## Zaman çizelgesi

