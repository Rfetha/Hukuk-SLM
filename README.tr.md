# HakHukuk

**Dizüstü bilgisayarda koşacak kadar küçük, "bilmiyorum" demeyi öğrenmiş bir Türkçe hukuk asistanı.**

[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[Model kartı](MODEL_CARD.md) · [Yol haritası](ROADMAP.md) · [English](README.md)

---

Bir hukuk asistanının işinin büyük kısmı cevap vermek değil, **kaynak
desteklemiyorken cevap vermemektir.** Kendinden emin ve yanlış bir madde numarası,
sessizlikten kötüdür — bir hukuk aracını tehlikeli yapan hata biçimi budur.

HakHukuk, bu işin iki yarısı için de eğitilmiş 4B'lik bir model (2,59 GiB,
Q4_K_M): cevabı verilen mevzuata dayandır, mevzuat soruyu kapsamıyorsa çekin.

> ### ⚠️ Hukuki tavsiye değildir
> Bu bir araştırma çıktısıdır. Avukat değildir, ürettiği metin hukuki tavsiye
> değildir. Mevzuat değişir, ağırlıklar değişmez. **Erişim (retrieval) katmanı var
> ve ölçüldü, ama aşağıdaki servis yoluna henüz paketlenmedi** — mevzuat metnini
> hâlâ siz veriyorsunuz. Ürettiği her madde numarasını
> [mevzuat.gov.tr](https://www.mevzuat.gov.tr) üzerinden doğrulayın.

## Nerede duruyor

DEV kümesi, harness kapalı, hakem `gpt-4o-mini`. Tam protokol [model kartında](MODEL_CARD.md).

| | sadık-cevap kütlesi ↑ | aşırı-red ↓ | kaynak yokken red ↑ | tok/cevap ↓ |
| :--- | ---: | ---: | ---: | ---: |
| çıplak base | 56,7% | 0,425 | 0,961 ᴷ³ | 1192 |
| **HakHukuk-4B-v0.1** | **71,6%** | **0,212** | **0,766** ᴷ³ | **714** |
| Gemini 3.1 Flash-Lite | 72,9% | 0,237 | 0,883 ᴷ³ | — |

ᴷ³ **M2b 2026-08-06'da yeniden puanlandı.** Eski sayılar, hakemin **modelin cevabına bakarak**
verdiği bir paydayla üretilmişti — yani aynı sınav her modelde farklı payda veriyordu. Payda artık
cevaba kör ve kollarda birebir aynı (`valid_traps` bu sınavda 61…80 → **77**). Eski değerler
[`#57`](docs/record/research_log/2026-08-06-cekinme-aleti-onarimi.md)'de duruyor; çeviri tablosu orada:
base `0,986 → 0,961` · biz `0,877 → 0,766` · Gemini FL `1,000 → 0,883`.
⚠ **M2/A1 sütunları yeniden puanlanmadı**, hâlâ modele bağımlı paydayı taşıyor.

Flash-Lite'ın sadık-cevap kütlesinin **%98'ine ulaşıyoruz ve ondan daha az
reddediyoruz** — 2,59 GiB'lık bir modelle ve ~sıfır marjinal maliyetle. Yalnız
çeldirici kaynaklar verildiğinde reddetme ekseninde hâlâ geride kalıyoruz (0,766 ↔ 0,883 —
payda onarılınca açıklık 12,3 → 11,7 puana daraldı, ama işaret değişmedi).

**Bu bir parite iddiası değildir:** harness kapalı, maliyet normalize edilmedi ve
merge yapılandırması DEV'de seçildi.

### Harness açıkken — ürünün dürüst sayısı

Yukarıdaki tablo doğru maddeyi modelin eline veriyor. Gerçek kullanıcının böyle bir
lüksü yok. Bağlamı bir retriever seçtiğinde (hibrit BM25 + `bge-m3`, 40.496 maddelik
indeks, `k=10`, tamamı CPU'da):

| | harness KAPALI | **harness AÇIK** |
| :--- | ---: | ---: |
| altın madde bağlamda | **kurgu gereği** garanti | **70/80 — `recall@10` 0,875** |
| sadık-cevap kütlesi | %71,6 | **%61,3** |
| A1 · altın getirilen alt küme | 0,909 | **0,862** |
| **uydurulmuş madde numarası** | 0 | **0 / 118** |

**Arkasında durduğumuz sayı %61,3.** Bu bir gerileme değil — iki ölçüm aynı şeyi
ölçmüyor ve KAPALI sütunu bir rakip değil **tavan**. 10,2 puanlık açığı ayrıştırdık:
**≈5,1 puan erişim ıskası** (harness'ın — 10/80 soruda altın madde hiç gelmiyor) +
**≈4,5 puan dikkat dağılması** (modelin — altın getirildiğinde bile yanına dokuz madde
konunca A1 0,909 → 0,862 düşüyor).

🚨 **Ve ölçüm kendi planımızı çürüttü.** Atıf doğrulayıcıyı A1 açığını kapatmak için
kurduk. **Sıfır** uydurulmuş madde numarası buldu — yakalamak için kurulduğu sınıf
**boş**. Model numara uydurmuyor; erişim ıskaladığında *başka bir gerçek* maddeden
cevaplıyor (7/80). Asıl büyük hata bunun tersi: **16/80** soruda model, altın madde
**bağlamındayken** çekiniyor — ve bu sayı harness kapalıyken de aynı (17/80), yani bir
**model** özelliği, erişim özelliği değil. Deterministik kod bunu kapatamaz.
Ayrıntı ve tam kayıt: [yol haritası](ROADMAP.md) · [`sprint3-part1.md`](docs/_arsiv/sprint3-part1.md).

## Nasıl kuruldu

```
ham base ──┬── LoRA SFT   (dayanaklandırma) → τ_g
           └── LoRA ORPO  (çekinme)         → τ_a
                                              │
              eşzamanlı 2-yollu TIES ─────────┘  → HakHukuk-4B-v0.1
```

Birbiriyle **fiilen çatışan** iki beceri: dayanaklandırma için eğitmek çekinmeyi
çökertiyor (ölçüldü: 0,961 → 0,506 ᴷ³), çekinme için eğitmek dayanaklandırmayı
çökertiyor (%56,7 → %41,2). Hiçbir kol tek başına kullanılabilir değil. Merge
ikisini de geri getiriyor — dayanaklandırma tamamen korunuyor, çekinme çöküşünün
**%57'si** ~~%71'i~~ onarılıyor *(oran 2026-08-06'da ᴷ³ paydalarından yeniden türetildi:
`(0,766−0,506)/(0,961−0,506)`; not [`MODEL_CARD.md`](MODEL_CARD.md)'de).*

## Hızlı başlangıç

```bash
# 1. llama.cpp kur
bash scripts/setup_llamacpp.sh

# 2. modeli ayağa kaldır
llama-server -m models/gguf/tgta_v1-q4_k_m.gguf \
    -c 8192 -ngl 99 -fa on --cache-type-k q8_0 --cache-type-v q8_0

# 3. mevzuat metnini bağlam olarak vererek sor
curl localhost:8080/v1/chat/completions -d '{
  "messages": [{"role":"user","content":"KAYNAKLAR:\n<mevzuat metni>\n\nSORU: <soru>"}],
  "temperature": 0
}'
```

## Çalışmayı yeniden üretmek

Araştırma kaydının tamamı bu depoda — negatif bulgular, kendi ön-kayıtlı kapısına
takılıp **geçersiz sayılan iki koşu** ve ölçüm çeliştiği için **sonradan tersine
çevrilen bir karar** dahil.

| | |
| :--- | :--- |
| [`docs/record/research_log/`](docs/record/research_log/) | ne olduğu, kronolojik, her sayıyla |
| [`docs/adr/`](docs/adr/) | 55 karar kaydı — bağlam, seçenekler, **elenenler** |
| [`docs/record/kollar.md`](docs/record/kollar.md) | artefakt kaydı: her kol ve merge, künyesiyle |
| [`docs/record/yurutme-tuzaklari.md`](docs/record/yurutme-tuzaklari.md) | **hata vermeden yanlış sayı üreten** kalıplar — her biri fiilen ısırdı |
| [`outputs/eval/`](outputs/eval/) | ham eval çıktıları ve koşu künyeleri |

Seed'ler, base commit hash'i, GGUF sağlama toplamları ve hakem ayarları koşu
künyelerinde (`KUNYE.json`) sabitlenmiştir.

## Veri

[mevzuat.gov.tr](https://www.mevzuat.gov.tr) ve `bedesten.adalet.gov.tr` API'sinden
mevzuat; iki Apache-2.0 Hugging Face veri seti; gerçek mevzuat metninden üretilip
doğrulanmış sentetik çiftler.

**Hiçbir aşamada ticari hukuk veritabanı kullanılmadı** — bu, sonradan yapılan bir
temizlik değil, ilk günden konmuş bir kuraldı. Bkz. [`NOTICE`](NOTICE) ve
[`docs/VERI_PLANI.md`](docs/VERI_PLANI.md).

## Durum

`v0.1`. Yapılandırma DEV'de seçildi ve tek-aşamalı/ardışık ince ayar tabanlarına
karşı henüz doğrulanmadı. Doğrulanana kadar sürüm 1.0'ın altında kalır.

Katkı, eleştiri ve yeniden üretme denemeleri — özellikle yeniden üretme denemeleri —
memnuniyetle karşılanır.

## Lisans

Apache-2.0. Base model `Qwen/Qwen3.5-4B` Apache-2.0'dır; tam atıf zinciri için
[`NOTICE`](NOTICE).
