# ADR 0003 — Base model: Gemma 4 12B (Qwen3.5-4B'i süpersed eder)

- **Durum:** Yürürlükte (2026-06-07) · **TEYİT + SABİTLENDİ (2026-07-17, ADR-0017).**
- **Geriye dönük kayıt.**

> ⚠️ **GEREKÇE NETLEŞTİRMESİ (2026-07-17):** Aşağıdaki gerekçe listesinde **multimodal/OCR YOKTUR** ve olmamalıdır — o yalnız "Değerlendirilen alternatifler"de *reddedilen* encoder-ekli yığını gerekçelendirirken geçer, bir **seçim nedeni değildir.** `TEKNIK_PLAN.md` S13 ve eski `VISION.md` bunu gerekçeye kaydırmıştı (gerekçe-kayması) → düzeltildi. ADR-0017 base'i tez için sabitlerken asıl gerekçeyi **QAT→Q4_0 zinciri** olarak teyit etti.

## Bağlam
Çekirdek ürün kısıtı: **erişilebilirlik** — son kullanıcı ~8GB VRAM tüketici GPU'sunda çalıştırabilmeli
(`VISION.md`). İlk seçim Qwen3.5-4B idi (küçük = kolay sığar). Ayrıca eski strateji raporu Gemma 4 26B
A4B MoE öneriyordu (çok büyük, erişilebilirlikle çelişir). Gemma 4 ailesinin **QAT → Q4_0** hattı,
büyük bir modeli fine-tune edip dağıtımda küçültmeyi (kaliteyi eğitimde tutup boyutu sonradan
düşürmeyi) mümkün kıldı.

## Karar
Base model = **Gemma 4 12B** (`google/gemma-4-12B-it-qat-q4_0-unquantized`).
Hat: QLoRA fine-tune (NF4) → bf16 merge → **Q4_0 GGUF ~6.5GB** → 8GB VRAM son kullanıcı.
8GB hedefi *quantization*'la sağlanır, **eğitimi 4B'ye kısarak değil**.

## Değerlendirilen alternatifler
- **Qwen3.5-4B** → SÜPERSED. 12B'nin akıl yürütme/Türkçe kapasitesi belirgin üstün; Q4_0 ile zaten
  8GB'a sığıyor → küçük modelin tek avantajı (boyut) ortadan kalktı. Ayrıca rakip Mecellem de
  Qwen3-4B tabanlı → farklı base ile **niş** ayrışması güçlenir (`[[paper-target]]`).
- **Gemma 4 26B A4B MoE** (eski rapor) → REDDEDİLDİ; erişilebilirlik kısıtını ihlal eder.
- **Encoder-ekli multimodal yığın** → gereksiz; Gemma 4 encoder-free unified mimari, text-only SFT
  multimodal yeteneği (OCR/PDF/ses, Faz 3) bozmaz.

## Sonuç
- Apache-2.0 base → lisans-temiz, model kartında atıf şartı (ADR 0007).
- 12B QLoRA yerel 12GB RTX 5070'te sıkışık (batch=1 + gradient_checkpointing) → gerçek eğitim
  Modal A100'e taşındı (ADR 0004).
- Mecellem'in açık reçetesi (temizlik zinciri, curriculum) yeniden kullanılır ama Gemma 4 mimarisine
  uyarlanır. Gemma 4 turn işaretleri (`<|turn>user`/`<|turn>model`) tokenizer'da doğrulandı.

## İlgili
`VISION.md`, `FINE_TUNING.md`, `TEKNIK_PLAN.md`, ADR 0004, ADR 0007, `[[paper-target]]`
