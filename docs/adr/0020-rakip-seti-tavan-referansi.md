# ADR-0020 — Rakip seti: dağıtım-sınıfı kapalı modeller + tavan referansı

**Statü:** Yürürlükte · **Tarih:** 2026-07-17
**İlgili:** ADR-0016 (dış-benchmark/rakip konumlama — REVİZE), ADR-0017 · spec §4 · OpenRouter erişimi

## Bağlam
ADR-0016 frontier kıyasını "kendi canon setimizde" konumlamış ve aday listesi olarak *"GPT-4o / Claude / Gemini + Llama-3.1-8B baseline + Mecellem-4B"* demişti. Yeni tez (ADR-0017) bu kıyası ana iddia yapınca rakip setinin **netleştirilmesi + daraltılması** gerekti: kimin "rakip", kimin "referans", kimin "ilgili çalışma" olduğu tezin savunulabilirliğini belirliyor.

## Karar
1. **Rakipler = kapalı ticari, DAĞITIM SINIFI:** **Gemini 3 Flash · Claude Sonnet · GPT-5-mini.** Modern frontier'ın ölçekte gerçekten koşulan katmanı (kimse her sorguya en üst-uç ödemiyor) + bizim maliyet köşemize en yakın. **Parite hedefi bunlar.**
2. **Tavan referansı (rakip DEĞİL):** **Gemini 3.5 Pro · Claude Opus.** Grafikte **tek referans çizgisi** — "neden en güçlüsüyle kıyaslamadınız?" açığını kapatır; parite iddia edilmez, sadece tavanı gösterir. Maliyeti ~$3, ölçülmemesi savunmada açık bırakır.
3. **Terminoloji:** paper'da rakiplere "frontier" **denmez**, **maliyet bandı** denir → "hangisi frontier" tartışması açılmaz.
4. **Rakip inference = OpenRouter** (tek anahtar, `base_url` değişikliği, mevcut `OpenAI()` uyumlu). **Yeni para-kapısı.**
5. **Tarihli snapshot pin zorunlu** (`gpt-4o-2024-11-20` gibi) + ölçüm tarihi kaydı — tez rampası ≥2 yıl, sürüm kayması (spec §9).

## ADR-0016'dan farklar (revize)
- **Llama-3.1-8B ve Nemotron ÇIKTI.** Rakip tanımı = kapalı ticari lablar; açık modeli yerelde koşma sorusunu **Gemma base (C/E hücreleri) + Mecellem** zaten cevaplıyor. (Nemotron ayrıca OCRTurk'te TR belge işlemede en zayıf, arXiv:2602.03693 — off-thesis.)
- **Mecellem** = "açık referans / ilgili çalışma", ızgara dışı, **yeni koşu YOK** (cite-only, ADR-0016 korunur). "Geçtim" iddiası kurulmaz (CPT foundation base ≠ asistan; kategori farkı).
- ADR-0016'nın "dış İngilizce benchmark koşulmaz" kararı (BigLaw/LegalBench/law-MMLU) **aynen geçerli.**

## Sonuç
Deney ızgarası: özne × {harness yok / var} × 6-mod CANON. Adil kıyas = D (bizim+harness) vs B (rakip+harness). Hakem self-preference'ı: hakemsiz omurga (`rejection_exact` + atıf-doğrulama) + cross-family panel + aile-dışlama (spec §6).
