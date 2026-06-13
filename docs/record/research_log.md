# HakHukuk — Araştırma Kaydı (kronolojik)

> **Bu dosya ne:** Projenin **deney günlüğü** — ne yaptık, ne çıktı, ne karar verdik, paper'ın hangi
> bölümüne yarar. Tek dosya, kronolojik, **paper/rapor hammaddesi.** ADR'ler *kararı* tutar; bu dosya
> *anlatıyı + sayıları + öğrenilen dersi* tutar. Yeni anlamlı deney/bulgu → buraya bir girdi.
>
> **Paper haritası:** K1=ablasyon (base→+SFT→+RAG), K3=ayrışma bulguları (beklenmedik negatif sonuçlar).
> Detaylı hedef: `docs/PAPER_TARGET.md`. Kararlar: `docs/adr/`.

---

## Künye
- **Model:** Gemma 4 12B (`gemma-4-12B-it-qat-q4_0-unquantized`) + QLoRA → (Faz 3) Q4_0 GGUF.
- **Ana metrik:** groundedness — FactScore (claim böl→doğrula) + ALCE (atıf prec/recall, wrong_ref), `scripts/groundedness.py`. Hakem: gpt-4o-mini (paper'da cross-judge gpt-4o).
- **Eğitim yeri:** Modal A100. **Eval:** lokal ($0, OpenAI hakem).
- **Birincil kitle (2026-06-13 reframe):** UZMAN (avukat/hukukçu). Vatandaş = app-layer ikinci register.

---

## Zaman çizelgesi

### ~2026-05/06 — Çerçeve + planlama
- Private repo + proprietary lisans (ADR-0007). Base = Gemma 4 12B (ADR-0003). Eğitim = Modal A100 (ADR-0004).
- Veri kuralı: yalnız güncel TC mevzuatı; Lexpera/Kazancı ASLA. EDA-doğrula (newmindai/EuroHPC reddedildi — çöp). (ADR-0005)
- Akademik hedef: niş + sistem paper'ı (ADR-0006), `docs/PAPER_TARGET.md`.

### 2026-06-07/08 — v0 (forum verisi) → BAŞARISIZ
- **Veri:** `data/processed/sft_v0/` — 29K, `turkish_law_qa_dataset` + `turkish-law-chatbot` (forum).
- **Sonuç:** modeli batırdı (base-altı doğruluk).
- **Post-mortem (2026-06-13 kanıtlandı):** "7 Kasım 1982'de yürürlüğe girmiştir." cevabı **154 farklı soruya birebir** yapıştırılmış; atıf oranı düşük (~%13.6 sıkı ölçüt). → forum verisi sistemik kirli.
- **Ders (paper K3 adayı):** kaynaksız QA verisi doğruluğu öğretmez, halüsinasyon hattı ezberletir.

### 2026-06-08 — Grounded pivot → v1 verisi + kalite kapısı
- **Hamle:** doğruluğu **gerçek kanun maddesinden imal et** (madde → GPT-4o-mini Q&A üretir → doğrula).
- **Veri:** `data/processed/sft_v1/` — **21.458 grounded Q&A** (train 19.305 / val 1.131 / test 1.022), ~$1.16. Kaynak = 2.759 madde, **10 çekirdek kanun** (TMK,TBK,İİK,İş,TKHK,Aile,HMK,KatMülk,TCK,CMK). Üslup: **kısa, sade, vatandaş** (üretim promptu öyle diyor). 32K forum KATILMADI.
- **Filtre:** `gen_grounded.py::usable()` ham 40K'dan değişiklik/stub/mülga maddelerini eler (40K→21K→çekirdek 2.759).
- **Eğitim-öncesi kalite kapısı (ADR-0002):** `score_grounded_corpus.py`, n=40 → **faithfulness 0.984**, hall 0.016, cit_precision 1.0, wrong_ref 0.0. → veri temiz.

### 2026-06-09 — v1 SFT eğitimi (Modal A100)
- 1 epoch, 1207 step, ~3.5h ≈ ~$10. **Başlatma dersi (ADR-0008):** `modal run --detach ...::spawn_train` (fire-and-forget); `train.remote` client'a bağlı bekler → WSL kapanınca cancel → job ölür (4 kez yandı). Çözüm: `spawn()`.
- Adapter → `outputs/v1/` (checkpoint-1207).

### 2026-06-12 — Dış v2-analiz raporu değerlendirildi → ADR-0009
- Rapor "filtre gevşek, %3 değişiklik dili kaçıyor, fix=STUB'ı gövdeye yay" dedi.
- **Gerçek `usable()` import edilip 40K'da koşuldu → iddia FABRİKASYON** (AMEND/STUB zaten tüm gövdede; kaçak %0). Fix no-op. Filtreye DOKUNULMADI.
- Yan ürün: `outputs/eval/v1_suspect_sources.json` (404 şüpheli kaynak: 341 kısa + 65 mülga-gövde) → hedefli v1-audit için.
- **Ders (paper Methodology):** bir agent "çalıştırıp ölçtüm" dese bile gerçek modülü import edip doğrula.

### 2026-06-13 — ⭐ base vs v1 eval: KÖR vs RAG (asıl bulgu)
**Kurulum:** `gen_eval_grounded.py` — model soruyu cevaplar, gerçek madde **referans** (yer-gerçeği) olarak skorlanır. İki mod: KÖR (madde prompt'ta yok, parametrik) / RAG (`--with-source`, etiketli madde prompt'ta). n=20, gpt-4o-mini hakem.

| metrik | KÖR base | KÖR v1 | RAG base | RAG v1 |
|---|---|---|---|---|
| faithfulness | 0.571 | 0.520 | **0.980** | **0.971** |
| hallucination | 0.429 | 0.480 | 0.020 | 0.029 |
| cit_precision | 0.833 | 0.200 | 0.950 | 0.850 |
| wrong_ref | 0.125 | 0.800 | 0.050 | 0.150 |
| cit_recall | 0.900 | 0.450 | 1.000 | 0.900 |

**Bulgular:**
1. **KÖR test yanıltıcıydı.** Madde verilince faithfulness 0.52→0.97, halüsinasyon 0.48→0.03. v1'in "felaketi" (KÖR wrong_ref 0.80) **test artefaktı** — model ezberden madde no uyduruyordu.
2. **Etiket hatası:** RAG'da madde *metni* verilip *etiketi* (Kanun+no) verilmeyince model numarayı yine uydurdu. Etiket eklenince (`ragL`) atıflar düzeldi. → **Faz 2 RAG dersi: getirilen chunk atıf metadatasını taşımalı.**
3. **RAG modda v1 ≈ base** (faith 0.971 vs 0.980; v1 cit_precision 0.85 < base 0.95). **SFT ana metrikte base'i GEÇMEDİ, atıfta hafif geriletti.**

**Reframe (bugün netleşti):** birincil kitle = uzman; doğruluk RAG'dan; sadelik app-layer. → "v1 kısa/sade" satış noktası değil.

**Strateji kararı (subagent analizi):** v1'i **eğitim hedefi olarak reddet**, grounding altyapısını koru → **dar v2** kur:
- RAG-**modunda** eğit (deploy mimarisiyle eşleş; KÖR eğitim wrong_ref 0.80'in sebebi).
- **Uzman-register** (v1 vatandaş-register'ı yanlış kitle).
- **%15-25 hedge/red** örneği (v1'de %1.1 → SFT'nin tek base+prompt'la zor taklit edilen meşru rolü: kaynak-yokken uydurma yerine "maddede yok/danış").
- **Başarı kapısı:** faithfulness DEĞİL (tavan) → **wrong_ref ≤0.05 + hedge-isabeti + atıf-format tutarlılığı.**
- **Versiyonlama:** v2 = **base'den taze QLoRA** (v1 üstüne DEĞİL). v0/v1/v2 = deney nesli, ağırlık atası değil. v1 arşivlenir (ablasyon referansı).

**Açık doc çelişkisi:** VISION.md §1 "default output = vatandaş dili / terim→sade çeviri" reframe ile çelişiyor → ADR-0010 + VISION düzeltmesi bekliyor.

---

## Açık kararlar / sıradaki
- [ ] ADR-0010: reframe (uzman birincil register) + VISION.md §1 düzeltmesi.
- [ ] n=40 + zor (uzun/çok-koşullu madde) sette base vs v1 teyit (tavan-gürültü ayrımı).
- [ ] v2 tasarımı: RAG-modu veri üretimi + hedge dilimi + uzman register prompt.
- [ ] Kaynak-eksik eval seti (hedge-isabeti ölçmek için) — yeni.
- [ ] Rakip baseline (Mecellem-Qwen3-4B, Llama-3.1-8B) bizim terazide, RAG-modu.
- [ ] MCQ ekseni (hakem-bağımsız), cross-judge gpt-4o, ~30 yazar spot-check.

## Paper'a ne yarar (eşleme)
- **K1 ablasyon:** base → +SFT → +RAG tablosu. **Uyarı:** faithfulness'la ölçülürse "+SFT" satırı boş çıkar (tavan); SFT katkısını wrong_ref/hedge/format eksenlerinde göster.
- **K3 ayrışma/negatif bulgular:** (a) v0 forum verisi çöküşü (154x ezber), (b) **KÖR-vs-RAG: parametrik madde-no ezberi imkansız, RAG tavanı SFT'yi faithfulness'ta gereksizleştirir** — güçlü, yayınlanabilir negatif bulgu, (c) etiketsiz-chunk → uydurma atıf.
- **Methodology:** grounded veri imali, kalite kapısı köprüsü, dış-iddia doğrulama disiplini.
