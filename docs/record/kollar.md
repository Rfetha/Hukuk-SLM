# Kol kaydı — her `τ_X` versiyonunun künyesi

> **Bu belge ne:** eğitilmiş her kolun (task-vector dalının) **tek kayıt yeri**. Bir artefakt
> diskte duruyorsa burada bir satırı vardır; satırı yoksa o artefakt **kimliksizdir ve kullanılmaz.**
>
> **Neden var:** bu hattın hata sınıfı sessiz yanlışlık. *"Bu sayı hangi kolun, hangi versiyonun
> sayısı"* sorusu **dosya adından** cevaplanabilmeli — o yüzden versiyon zincirin her halkasında
> taşınır: adaptör → merge → GGUF → eval etiketi.
>
> **Kural (2026-07-29):** repo dışı artefakt **yok**. Her şey `/home/ersoy/code/Hukuk-SLM` altında.
> Adaptörler git'te **değil** (`.gitignore: outputs/**/*.safetensors`, ayrıca 114 MB > GitHub'ın
> 100 MB dosya sınırı) ve **yedeklenmiyor** — bilinçli karar: adaptör veri + reçete + seed sabitken
> yeniden üretilebilir, yeri doldurulamaz varlıklar (veri · belgeler · eval çıktıları) zaten metin
> ve git'te. *(12B hattının adaptörleri bu kararın bedelini gösterdi: repo dışı devir paketi
> silindi, adaptörler kalıcı kayıp — kasıtlı, çünkü o hat emekli.)*

---

## Adlandırma

```
outputs/<kol>_v<N>/                      LoRA adaptörü        (asıl artefakt)
models/merged/<kol>_v<N>/                merge edilmiş bf16   (yeniden üretilebilir)
models/gguf/<kol>_v<N>-<QUANT>.gguf      taşıyıcıya giden     (yeniden üretilebilir)
eval etiketi: <mod>_<kol>_v<N>           ör. m1_tg_v1
```

**Kol kısaltmaları:** `tg` = `τ_grounding` · `ta` = `τ_abstention` · `base_a` = Taban A (karışık SFT) ·
`base_b1`/`base_b2` = Taban B'nin iki aşaması (ardışık SFT).

**Yeni versiyon ne zaman açılır:** eğitim rejiminde (veri · adım · lr · `r`/`alpha` · dropout ·
`target_modules` · precision · seed) **herhangi bir** değişiklik. Rejim aynıysa yeni versiyon
açılmaz — aynı artefakttır.

> ⚠️ **Versiyon karıştırma = merge geçersizliği.** `τ = θ_ft − θ_base` tanımı bütün kolların
> **aynı θ_base**'den ve **eşleşen rejimden** gelmesini şart koşar (`TASARIM.md` §4.1.1, ADR-0036).
> Farklı versiyonları birleştirmek hata vermez, sadece ölçtüğün şeyi yok eder.

---

## Kollar

| kol | ver | tarih | durum | rejim | `‖τ‖_F` | eval etiketi | kayıt |
| :--- | :-- | :--- | :--- | :--- | ---: | :--- | :--- |
| `τ_grounding` | **v1** | 2026-07-28 | 🟢 aktif | 1.083 adım · lr 1e-4 · r=16/α=32 · dropout 0.05 · 224 LoRA çifti · seed 3407 · veri `train/raft/` | **10.4589** | `*_tg` *(Sprint 1; v1 demektir)* | [#41](research_log/2026-07-29-cp6-tau-grounding-olcumu.md) |
| `τ_abstention` | — | — | ⏳ CP3'te eğitilecek | 82 adım (3 epoch) · lr 1e-5 · etkin batch 64 · `--fresh-adapter` | — | — | `sprint2.md` CP3 |

### `τ_grounding` v1 — açık kalemler *(2026-07-29 gecesi, bütçeli kipte YENİDEN YAZILDI)*

⚠️ Aşağıdaki tablo **CP0.9'dan sonra baştan yazıldı**. Eski hâli thinking-off ölçümünden geliyordu
ve o protokol artık canlı değil (ADR-0043 m.4). Kaynak:
[`research_log` #43](research_log/2026-07-29-cp09-butceli-dusunce-cipalari.md).

| # | sebep | thinking-off | **bütçeli** | durum |
| :-- | :--- | :--- | :--- | :--- |
| 1 | **M5 anti-hedef ihlali** | 36.9 → **44.2** ❌ | 42.5 → **39.2** | ✅ **KAPANDI** — Kapı 6'yı bugün `τ_g` geçiyor, base geçemiyor |
| 2 | **A1 düşüşü** (cevapladığında hata) | 0.973 → 0.847 | 0.986 → **0.866** | 🟡 **duruyor** — ne kadarı meta-iddia artefaktı, CP1 söyleyecek |
| 3 | **RAFT şablonunun meta-iddiaları** (desteksiz iddiaların %58'i) | — | — | 🟡 hakem tarafında (ADR-0041, CP1) |
| 4 | **Akıl yürütme izi İngilizce** | 8/8 | 8/8 | 🟡 ürün vaadi *"okunabilir muhakeme"* karşılanmıyor; izli eğitim verisi gerektirir |
| 5 | 🆕 **M2b çöküşü** — gold yokken distractor'lardan cevap uyduruyor | 1.000 ✅ | **0.607** (fabrikasyon 0.393) | 🔴 **EN GÜÇLÜ sebep** — üstelik tam kendi eğitim ailesinde (RAG_MULTI) |

**Ne değişti:** eski tablonun *"en güçlü sebep"*i (M5 ihlali) bütçeli kipte **ortadan kalktı**;
yerine M2b geldi. Yani `τ_g` v2'nin gerekçesi artık *"ezberi azalt"* değil **"kaynak yokken sus"**.
Bu aynı zamanda `τ_a`'nın hedefiyle çakışıyor — v2 mi `τ_a` mı sorusu Sprint 2'nin açık kararı
([`sprint2.md`](../../sprint2.md) ARA KAPI bölümü).

> **Kural (değişmedi):** v2 açılırsa **bütün açık kalemler aynı anda** kapatılır. Ayrı ayrı
> eğitmek iki kat para (~$5.5) ve iki kat kafes yeniden ölçümü demektir. ADR-0040 m.4 gereği
> yeniden eğitilen her kol **düşünme yeteneğini koruyacak** biçimde eğitilir.

### `τ_grounding` v1 — düşünce modu davranışı *(n=470'te DÜZELTİLDİ, 2026-07-29)*

⚠️ CP0'ın n=36'lık ölçümü *"`τ_g` düşünüyor ve duruyor, 35/36"* diyordu ve bu **genel bir kazanç**
sanılmıştı. n=470'te kazanç **eğitim istemi ailesine özgü** çıktı:

| istem ailesi | modlar | base zorunlu kapatma | `τ_g` | ort token base→`τ_g` |
| :--- | :--- | --: | --: | :--- |
| **RAG_MULTI** ← `τ_g`'nin eğitim biçimi | m1 · m2b · m3 | %91.7 | **%5.8** | 1098 → **476** |
| RAG_tek | m4 · m2 | %96.7 | %79.3 | 1116 → 1046 |
| BLIND | m5 | %100.0 | %95.0 | 1284 → 1146 |

Kendi ailesinde etki muazzam (token **yarıya**, kendi kendine kapanma %94); dışında marjinal.
CP0'ın örneklemi o aileden geldiği için genel görünmüştü. Ayrıntı: `research_log` #43 Bulgu 2.

**Maliyet ekseni:** `τ_g` toplamda **772 tok/cevap** (base 1135, Gemini 543) — kendi istem
ailesinde **476**, yani orada rakipten ucuz.
