# ADR-0018 — 8 GB = soft gate, sert kısıt değil; erişilebilirlik = maliyet-performans eğrisi

**Statü:** Yürürlükte (**karar 3'ün gerekçesi düzeltildi 2026-07-23**) · **Tarih:** 2026-07-17
**İlgili:** ADR-0003, ADR-0017, **ADR-0021**, **ADR-0023** · spec §3.3-3.4 · `knowledge/summary_turboquant.md`

> ⚠️ **DÜZELTME (2026-07-23, ADR-0021/0023).** Aşağıdaki **karar 3 bu base için yanlıştı:**
> "bellek darboğazı çoğunlukla ağırlık değil KV-cache" — ölçüm tersini söylüyor. Gemma 4 12B'de
> 128K bağlamda KV = **1.16 GB**, Q4_0 ağırlık = **~6.5 GB** → KV, ağırlığın yalnız **%18'i.**
> Darboğaz **ağırlık.** (Sebep: 48 katmanın 40'ı `sliding_attention`, win=1024 → bağlamla
> büyümüyor; büyüyen 8 `full_attention` katmanı 1 KV head × 512 dim; `attention_k_eq_v=True`
> cache'i bir daha yarıya indiriyor. Kaynak: `scripts/kv_cache_compare.py`.)
>
> **Kararın kendisi (soft-gate + eğri) ayakta ve ölçümle güçlendi** — ama TurboQuant'ın rolü
> değişti: **bellek-darboğazı çözücü değil, bağlam tavanı kaldıracı.** 8 GB'da bf16 KV ile
> 64.755 token; q8_0 ile 149.990; q4_0 ile 320.461; ~3 bit ile 434.108. Ve dağıtım hattımız
> llama.cpp olduğu için **bugün kullanılabilir kaldıraç `--cache-type-k/-v`**; TurboQuant
> llama.cpp'de yok, sonraya bırakıldı (ADR-0023).
>
> Ayrıca karar 3'ün son cümlesi ("base değiştirmenin ~1.5GB verdiğinden fazlasını bedavaya
> verir") artık gereksiz: base kıyası KV üzerinden değil, **8 GB'da bağlam tavanı** üzerinden
> kazanıldı (176.128 vs 90.982 token — ADR-0021).

## Bağlam
Eski dokümanlar (`CLAUDE.md`, `VISION.md`) "~8 GB VRAM"ı sert kısıt gibi yazıyordu. Yeni tez erişilebilirliği tek nokta değil **eksen** (maliyet × kalite Pareto) olarak kuruyor; sert 8 GB kilidi bu ekseni tek noktaya çökertir.

## Karar
1. **≤8 GB = SOFT GATE (tercih bandı), yasak değil.** Bir yapılandırma ≤8 GB tutuyorsa "tercih bölgesinde"; aşan yapılandırmalar (12/16/24 GB) da **erişilebilirlik ekseninde kayıpla raporlanır.** 8 GB, maliyet-performans eğrisi üzerinde işaretli bir bant — eğrinin sonu değil.
2. **Boyut/bellek = ölçüm, karar değil.** Aile içi boyut eğrisi (E4B / 12B / 26B) — aile, tokenizer, QAT hattı, eğitim kodu sabit (Katman 2, HPC gelirse).
3. **Bellek darboğazı çoğunlukla ağırlık değil, uzun-RAG KV-cache'i.** Çözüm: **TurboQuant** — KV-cache 2.5–3.5 bit, eğitim gerektirmez, online, Llama-3.1-8B'de 4.5× sıkıştırmada full-precision performans, **ağırlığa dokunmaz.** Base değiştirmenin (~1.5GB) verdiğinden fazlasını bedavaya verir.

## Sonuç
`CLAUDE.md` + `VISION.md` "8 GB" ifadeleri soft-gate olarak güncellendi. Base sabit kalır (ADR-0017); düşük-spec ihtiyacı base değişikliğiyle değil, quantization + KV-cache sıkıştırma + boyut-eğrisi ölçümüyle karşılanır.
