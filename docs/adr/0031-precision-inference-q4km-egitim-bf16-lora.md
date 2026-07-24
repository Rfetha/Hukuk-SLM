# ADR-0031 — Precision: dağıtım Q4_K_M · eğitim bf16 taban + LoRA (QLoRA değil)

**Statü:** Yürürlükte (eğitim kolu **ölçüme bağlı**, aşağıda) · **Tarih:** 2026-07-24
**Otorite belge:** `TASARIM.md` §8 (kapı 5) · §4.2 (merge = tam ağırlık uzayı, kuantizasyon en son)
**İlgili:** ADR-0023 (saf-Q4_0 QAT'e özgü) · ADR-0026 (base bir parametre) · ADR-0028 (tek boyut
noktası, "yerelde $0" gerekçesi) · ADR-0030 (base seçimi) · `gemma4-12b-dersler.md#adr-0003` (12B hattı QLoRA'ydı)
**Kanıt:** `research_log` [#39](../record/research_log/2026-07-24-cp0-base-dogrulama-kapisi.md) ·
`outputs/eval/vram_stack.json`

---

## Bağlam

İki ayrı precision sorusu var ve karıştırılmamalı:

1. **Dağıtım precision'ı** — son kullanıcıya hangi kuantizasyon gider? Erişilebilirlik ekseni
   (ADR-0018 yumuşak kapı ≤8 GB) buna bakıyor.
2. **Eğitim precision'ı** — LoRA hangi taban üzerinde eğitilir? İç iddianın (task-vector merge)
   ölçüm temizliği buna bakıyor.

TASARIM §12 iki açık borç işaretlemişti: *"VRAM tahminleri ölçülmedi"* ve *"CANON bf16/NF4'te
koşuyor, dağıtım artefaktı kuantize → ölçtüğümüz ≠ dağıttığımız."* Bu ADR birincisini kapatıyor.

---

## Karar 1 — dağıtım: **Q4_K_M**, sabit

Kuantizasyon merdiveni üretildi ve VRAM × bağlam matrisi **ölçüldü** (RTX 5070 Ti, `-ngl 99 -fa on`,
KV `q8_0`; sunucu payı = yüklüyken − taban):

| kuantizasyon | dosya | ctx 4096 | ctx 32768 | ctx 131072 | tg256 |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **Q4_K_M** | 2.58 GiB | **3.09 GiB** | 3.70 GiB | 5.76 GiB | **122.9 t/s** |
| Q5_K_M | 2.93 GiB | 3.45 | 4.05 | 6.11 | 106.9 |
| Q6_K | 3.31 GiB | 3.82 | 4.42 | 6.48 | 103.1 |
| Q8_0 | 4.28 GiB | 4.79 | 5.40 | 7.46 | 88.1 |
| f16 | 8.07 GiB | 8.57 ❌ | 9.17 ❌ | 10.16 ❌ | — |

**Kullanıcı kuralı:** *"Q4'ten yüksek bir precision <8 GB'a sığıyorsa ona geçeriz."* Ölçüm Q8_0'ın
**sığdığını** gösteriyor (ctx 131072'de bile 7.46 GiB). **Karar yine de Q4_K_M** — kullanıcı kararı,
gerekçe: 7.46 GiB gerçek bir 8 GB kartta masaüstü/compositor payından sonra **başlık bırakmıyor**;
ölçtüğümüz sayı sunucunun payı, kartın tamamı değil. Ek olarak Q4_K_M decode'da **%28 hızlı**
(122.9 vs 88.1 t/s) ve `$`/sorgu metriği doğrudan throughput'a bağlı (ADR-0017).

TASARIM §8 kapı 5 zaten Q4_K_M diyordu → **supersede yok, teyit var.**

### Yan bulgu — hibrit mimarinin erişilebilirlik kazancı

Bağlamı **32×** büyütmek (4096 → 131072) VRAM'e yalnız **+3.17 GiB** ekliyor. Sebep yapısal:
32 katmanın **24'ü linear attention** (sabit boyutlu özyineli durum), KV yalnız **8 full-attention**
katmanında bağlamla büyüyor. Dense bir modelde aynı ctx artışı çok daha pahalıdır.
⚠️ Bu, CLAUDE.md'nin *"KV-cache darboğazı her base için yeniden ölçülür, varsayılmaz"* kuralının
bu base'deki cevabıdır — 12B'de KV ağırlıkların %18'iydi, burada tablo tamamen farklı.

---

## Karar 2 — eğitim: **bf16 taban (donuk) + bf16 LoRA**, QLoRA değil

Kullanıcı kararı: *"bizim FT'ler de full precision olacak."*

### Okuma belirsizliği — kayda geçer

"Full precision" iki şey olabilir:

| | taban | eğitilen | değerlendirme |
| :--- | :--- | :--- | :--- |
| **(a)** full fine-tuning | bf16 | **tüm ağırlıklar** | ~60-70 GB (ağırlık + gradyan + AdamW fp32 momentleri + fp32 master) → yalnız A100-80/H100 |
| **(b)** LoRA, QLoRA değil | **bf16, donuk** | LoRA r=16 | 12B hattının bir adım üstü |

**(b) seçildi.** Gerekçe:

1. **Kullanıcının iki mesajı da precision ekseninde kurulmuştu** (Q4 ↔ FP8 ↔ full precision),
   *"hangi parametreler eğitilir"* ekseninde değil. (b) o ekseni tam karşılıyor: NF4 yuvarlaması
   eğitimden tamamen çıkar.
2. **İç iddianın aletini keskinleştirir.** TIES/DARE `ΔW = θ_ft − θ_base` üzerinde eleman bazında
   budama ve işaret-seçimi yapar. QLoRA'da o ΔW kuantizasyon gürültüsü taşır; merge'ün "hangi eleman
   önemli, hangi işaret kazanır" kararı kısmen gürültüye bakar. bf16 tabanda bu confound kalkar.
   *12B hattında bu gerekçe yoktu — orada merge iddiası yoktu.*
3. **(a) araştırma sorusunu değiştirir.** TASARIM §1.2 iddiayı *"beceri başına bağımsız eğitilmiş
   **LoRA kolları** + task-vector merge"* diye yazıyor. Task arithmetic full FT'de de tanımlıdır
   (Ilharco et al. öyle yapmıştı) ama bu, tüketici donanımı + sıfır marjinal maliyet ipini koparır.
4. **(a) ölçmek istediğimiz çatışmayı büyütür.** Hattın merkezi negatif bulgusu SFT'nin abstention'ı
   sıfırlaması (#07, #32). LoRA'nın düşük rank'i regülarizatörün kendisi — repo'nun kendi dersi
   "LoRA + düşük rank + replay" üçlüsünü unutmayı engelleyen şey diye adlandırıyor. (a) o freni kaldırır.
5. **(a) merge süpürmesini pahalılaştırır.** TASARIM §6.3: *"merge işlemlerinin eğitim maliyeti sıfır
   — merge tekniği taramasını gerçekçi kılan tek şey."* λ / TIES density / DARE drop-rate taraması
   LoRA'da birkaç matris çarpımı; full task-vector'de her nokta 3 × 8 GiB delta okuma-yazma.
   Süpürme olmadan *"merge çalışmıyor"* ile *"bu λ yanlış"* ayrılamaz (§11'in elenen alternatifi).

### Uygulama

`train_sft.py` / `modal_train.py`: `load_in_4bit=False`, `dtype=bfloat16`. Diğer her şey sabit —
`r=16` · `lora_alpha=32` · `lora_dropout=0.05` · replay karışımda · `lr ≥ 3e-4` yasak
(`--allow-high-lr` olmadan script durur) · `save_steps=200` + oto-resume.

**`target_modules` artık `"all-linear"` DEĞİL** (ADR-0030 açık kalemi): Qwen3.5 bir VLM ve
`all-linear` LoRA'yı görüntü kulesine de takıyor. Metin kulesi listesi:

```
q_proj, k_proj, v_proj, o_proj                          # full_attention katmanları
in_proj_qkv, in_proj_z, in_proj_a, in_proj_b            # linear_attention katmanları
gate_proj, up_proj, down_proj                           # MLP
```
Doğrulandı: **29.908.992** eğitilebilir param, görüntü kulesi temiz.

### ⚠️ Bu karar ÖLÇÜME BAĞLI — açık uç

**Ölçülemedi:** bf16 tabanın yerel 12 GB karta sığıp sığmadığı. Sebep `causal-conv1d` engeli —
kurulu olmadan `transformers` linear-attention fast path'ini açmıyor ve torch fallback'i
özyineli durumu her zaman adımı için materyalize ediyor (seq 512'de bile OOM, tepe 10.76 GiB).
Bu bir *hız* değil *bellek* engeli; fast path açılmadan hiçbir bellek sayısı temsili değil.

> ⚠️ **Geri alınan bir ara sonuç:** bir noktada *"bf16 taban yerele sığmıyor"* denmişti. O ölçüm
> **geçersizdi** — test aracı `SFTTrainer`'ın füzyonlu CE'sini atlayıp 248.320'lik sözlükte tam
> logit tensörünü materyalize ediyordu. Sayı, konfigürasyonu değil aracı ölçüyordu.

**Karar kuralı, şimdi yazılır (sonradan rasyonalize edilmesin):**

| ölçüm sonucu | karar |
| :--- | :--- |
| bf16 + LoRA yerele **sığıyor** | (b) kalır, eğitim **yerelde $0** — ADR-0028'in gerekçesi ayakta |
| **sığmıyor**, Modal maliyeti kabul edilebilir | (b) kalır, eğitim **Modal**'a taşınır — ADR-0028'in *"yerelde $0"* gerekçesi **düşer**, limitations'a yazılır (12B hattı zaten Modal'daydı, `#adr-0004`) |
| **sığmıyor** ve Modal maliyeti istenmiyor | **QLoRA'ya dön** (12B'nin yaptığı). Tezden ölçülebilir hiçbir şey gitmez; limitations'a *"task vector'ler NF4 tabandan türetildi"* cümlesi eklenir |

---

## Elenen alternatifler

| eleme | neden |
| :--- | :--- |
| **Q8_0 dağıtım** | Ölçümde <8 GB'a sığıyor (7.46 GiB @ 131k) ama gerçek kartta masaüstü payından sonra başlık kalmıyor; ayrıca decode %28 yavaş → `$`/sorgu artar |
| **f16 dağıtım** | ctx 4096'da bile **8.57 GiB** — 8 GB bandına sığmıyor. Ölçüldü, tartışma kapandı |
| **(a) full fine-tuning** | Yukarıdaki 5 madde. Maliyet en zayıf gerekçe (~$40-90); asıl sebep araştırma sorusunu değiştirmesi ve merge süpürmesini öldürmesi |
| **Q4_0 (12B'nin kullandığı)** | ADR-0023'ün saf-Q4_0 kararı **QAT'e özgüydü**; Qwen3.5-4B'nin QAT checkpoint'i yok → Q4_K_M doğru varsayılan (TASARIM §8 kapı 5) |

---

## Sonuçlar

- `models/gguf/q35-4b-q4_k_m.gguf` = **dağıtım ve eval artefaktı** (CANON bu dosyada koşar).
- `q35-4b-f16.gguf` **saklandı** — TASARIM §12'nin *"ölçtüğümüz ≠ dağıttığımız"* hizalama koşusu
  (kuantize vs bf16, aynı CANON) artık bu makinede yapılabilir: f16 çıkarımı ctx 4096'da 8.57 GiB
  ve 12 GB karta sığıyor. **Borç kapatılabilir hale geldi.**
- Eğitim precision'ı `causal-conv1d` ölçümüne kadar **koşullu**; karar kuralı yukarıda önceden yazılı.
