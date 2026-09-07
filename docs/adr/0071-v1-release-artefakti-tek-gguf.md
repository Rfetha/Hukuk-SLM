# ADR-0071 — `v1.0` release artefaktı: **tek** GGUF, adında kuantizasyon

**Tarih:** 2026-09-07 · **Statü:** ✅ yürürlükte · **Karar:** insan
**Bağlı:** [ADR-0065](0065-bolunmus-surumleme.md) (ürün ↔ iddia sürümü) ·
[ADR-0031](0031-precision-inference-q4km-egitim-bf16-lora.md) (çıkarım Q4_K_M) ·
[ADR-0027](0027-tasarim-kilitleri-paralel-kol-merge.md) (kol tanımı, `τ = θ_ft − θ_base`) ·
[`kollar.md`](../record/kollar.md) §*"iki ad ayrı iş görür"*

## Bağlam

`HakHukuk-4B-v0.1` bugün **iki bağımsız LoRA kolunun** (`tg_v1` · `ta_v1`) ham TIES ile
birleştirilmiş hâli. Repoda **adaptörler tutulmuyor** (bilinçli — `artefakt-tek-klasör`
kuralı) ve yayımlanan her sayı **merge edilmiş Q4_K_M GGUF** üzerinde üretildi.

Soru: `v1.0`'da vatandaş **neyi indirir**?

## Karar

**1. Tek bir artefakt yayımlanır: adaptörleri merge edilmiş TEK GGUF.**
Adaptör + merge script'i dağıtımı yapılmaz.

**2. Dosya adı dört şeyi taşır — model · boyut · sürüm · KUANTİZASYON:**

```
HakHukuk-4B-v1.0-Q4_K_M.gguf
```

**3. İç ad korunur.** `tgta_v1-q4_k_m.gguf` izlenebilirlik için kalır; iki ad
[`kollar.md`](../record/kollar.md)'nin zaten yürürlükteki kuralıyla **ayrı iş görür**
(iç = *"hangi kol, hangi sürüm"*; dış = model kartı · yayın · anlatım).

### Neden kuantizasyon **adın içinde**

Kuantizasyon bir ayrıntı değil, **artefaktın kimliğidir** — hem sayıyı hem donanım
gereksinimini değiştirir. Ölçüldü (`outputs/eval/_artefakt/vram_stack_tgta_v1.json`):

| | dosya | VRAM ctx 4.096 | ctx 32.768 | ctx 131.072 |
| :--- | ---: | ---: | ---: | ---: |
| `Q4_K_M` | **2,59 GiB** | **3,09 GiB** | 3,70 GiB | 5,76 GiB |

Adında kuantizasyon olmayan bir dosya, *"benim kartıma sığar mı"* sorusunu **indirmeden**
cevaplatmaz; ve ileride ikinci bir kuantizasyon yayımlandığında iki dosya **aynı adı** ister.

## Reddedilenler

- **Adaptör + merge script'i yayımla** — REDDEDİLDİ. Üç bedeli var: (a) kullanıcı **8,66 GiB
  base**'i ayrıca indirip merge koşmak zorunda kalır; (b) merge host RAM'de bf16 akışıyla
  çalışır — vatandaşın makinesinde **yeniden üretilebilirliği ölçülmedi**; (c) yayımlanan sayı
  merge+kuantize edilmiş dosyada üretildi, adaptörlerde **değil** — dağıtılan şey ölçülen şey
  olmalı.
- **`v1.0`'da birden çok kuantizasyon yayımla (Q4_K_M + Q5_K_M + Q8_0)** — REDDEDİLDİ **şimdilik**.
  Her kuantizasyon **ayrı bir artefakttır** ve ADR-0057'nin eşit sınavı gereği kendi kapı koşusunu
  ister; üçü **üç kat ölçüm** demek. `v1.0` tek noktayı yayımlar, kuantizasyon eğrisi
  **açık borç** olarak kalır (ADR-0018'in "tek nokta, eğri değil" bedeliyle aynı sınıf).
- **Adda sürüm yok, yalnız `HakHukuk-4B-Q4_K_M.gguf`** — REDDEDİLDİ: `v0.1` ile `v1.0` aynı
  boyutta ve aynı kuantizasyonda; sürüm düşerse **iki farklı model ayırt edilemez**.

## Açık kalan

- ⚠️ **Kuantizasyon eğrisi ölçülmedi.** `Q4_K_M`'in `Q5_K_M`/`Q8_0`'a göre kütle kaybı
  **bilinmiyor**; ADR-0031 çıkarım hassasiyetini seçti ama **kaybı ölçmedi**.
- ⚠️ `HakHukuk-4B-v1.0` adı **ADR-0064'ün üç maddesi geçilmeden** kullanılmaz (ADR-0065).
