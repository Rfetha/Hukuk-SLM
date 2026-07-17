# ADR-0018 — 8 GB = soft gate, sert kısıt değil; erişilebilirlik = maliyet-performans eğrisi

**Statü:** Yürürlükte · **Tarih:** 2026-07-17
**İlgili:** ADR-0003, ADR-0017 · spec §3.3-3.4 · `knowledge/summary_turboquant.md`

## Bağlam
Eski dokümanlar (`CLAUDE.md`, `VISION.md`) "~8 GB VRAM"ı sert kısıt gibi yazıyordu. Yeni tez erişilebilirliği tek nokta değil **eksen** (maliyet × kalite Pareto) olarak kuruyor; sert 8 GB kilidi bu ekseni tek noktaya çökertir.

## Karar
1. **≤8 GB = SOFT GATE (tercih bandı), yasak değil.** Bir yapılandırma ≤8 GB tutuyorsa "tercih bölgesinde"; aşan yapılandırmalar (12/16/24 GB) da **erişilebilirlik ekseninde kayıpla raporlanır.** 8 GB, maliyet-performans eğrisi üzerinde işaretli bir bant — eğrinin sonu değil.
2. **Boyut/bellek = ölçüm, karar değil.** Aile içi boyut eğrisi (E4B / 12B / 26B) — aile, tokenizer, QAT hattı, eğitim kodu sabit (Katman 2, HPC gelirse).
3. **Bellek darboğazı çoğunlukla ağırlık değil, uzun-RAG KV-cache'i.** Çözüm: **TurboQuant** — KV-cache 2.5–3.5 bit, eğitim gerektirmez, online, Llama-3.1-8B'de 4.5× sıkıştırmada full-precision performans, **ağırlığa dokunmaz.** Base değiştirmenin (~1.5GB) verdiğinden fazlasını bedavaya verir.

## Sonuç
`CLAUDE.md` + `VISION.md` "8 GB" ifadeleri soft-gate olarak güncellendi. Base sabit kalır (ADR-0017); düşük-spec ihtiyacı base değişikliğiyle değil, quantization + KV-cache sıkıştırma + boyut-eğrisi ölçümüyle karşılanır.
