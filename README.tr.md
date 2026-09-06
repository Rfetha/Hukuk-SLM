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
indeks, `k=10`, tamamı CPU'da) ve sistem isteminde **kaynak-yeterliliği önsözü** varken
(2026-08-06'dan beri ana protokol — [ADR-0058](docs/adr/0058-b-i-kaynak-yeterliligi-onsozu-benimsendi.md)):

| | harness KAPALI | **harness AÇIK — RESMÎ** | AÇIK, önsözsüz *ablasyon* |
| :--- | ---: | ---: | ---: |
| altın madde bağlamda | **kurgu gereği** garanti | **70/80 — `recall@10` 0,875** | 70/80 — birebir aynı |
| coverage | 0,788 | **0,7625** | 0,7625 *(birebir aynı)* |
| sadık-cevap kütlesi | %71,6 | **%62,8** | %61,3 |
| A1 · cevaplanan | 0,909 | **0,8229** | 0,8042 |
| A1 · altın getirilen alt küme | 0,909 | **0,8705** | 0,8616 |
| **uydurulmuş madde numarası** | 0 | **0 / 83** | 0 / 118 |
| altın bağlamdayken çekindi ↓ | 17/80 | **14/80** | 16/80 |
| *başka bir gerçek* maddeden cevapladı ↓ | — | **5/80** | 7/80 |

> 🚨 **DÜZELTİLDİ 2026-09-06.** Bu bölüm bugüne kadar **ADR-0058 ÖNCESİ** çıpaları
> (%61,3 · 0,862 · 0/118 · 16/80 · 7/80) resmî sayı gibi yayımlıyordu. Onlar **önsözsüz
> ablasyon** sayılarıdır ve **silinmedi**, sağdaki sütunda duruyor. Resmî koşu:
> `outputs/eval/olcum-bi/harness_tablo.json` ·
> [#56](docs/record/research_log/2026-08-05-olcum-bosluklari.md) §5 (D1). Ablasyon koşusu:
> `outputs/eval/s2-harness-k10-etiketli/`.

**Arkasında durduğumuz sayı %62,8.** Bu bir gerileme değil — iki ölçüm aynı şeyi
ölçmüyor ve KAPALI sütunu bir rakip değil **tavan**.

> ⚠️ Aşağıdaki ayrıştırma **önsözsüz** çıpaya (%61,3) karşı, yani 10,2 puanlık açık için
> yapıldı. ADR-0058 sonrası açık **8,8 puandır** ve **yeniden ayrıştırılmamıştır.**

10,2 puanlık açığı ayrıştırdık:
**≈5,1 puan erişim ıskası** (harness'ın — 10/80 soruda altın madde hiç gelmiyor) +
**≈4,5 puan dikkat dağılması** (modelin — altın getirildiğinde bile yanına dokuz madde
konunca A1 0,909 → 0,862 düşüyor).

⚠️ **İndirmeden önce bilinmesi gereken bir sonuç.** %62,8 sayısı *model + retriever + önsöz*
üçlüsünün sayısıdır. Önsöz bugün tek bir ölçüm script'inin içinde duruyor ve dağıtılmıyor,
retriever da aşağıdaki servis yoluna bağlı değil — dolayısıyla modeli düz indiren kişi manşeti
değil **ablasyon** sütununu (%61,3) yeniden üretir. İkisini de paketlemek `v1`'in ilan edilmiş
şartıdır ([yol haritası](ROADMAP.md)).

🚨 **Ve ölçüm kendi planımızı çürüttü.** Atıf doğrulayıcıyı A1 açığını kapatmak için
kurduk. **Sıfır** uydurulmuş madde numarası buldu — yakalamak için kurulduğu sınıf
**boş**. Model numara uydurmuyor; erişim ıskaladığında *başka bir gerçek* maddeden
cevaplıyor (**5/80**; önsözsüz ablasyon: 7/80). Asıl büyük hata bunun tersi: **14/80**
(ablasyon: 16/80) soruda model, altın madde **bağlamındayken** çekiniyor — ve bu sayı harness
kapalıyken de neredeyse aynı (17/80), yani bir **model** özelliği, erişim özelliği değil.
Deterministik kod bunu kapatamaz.
Ayrıntı ve tam kayıt: [yol haritası](ROADMAP.md) · [`sprint3-part1.md`](docs/_arsiv/sprint3-part1.md).

⚠️ **Bu 14/80 ve 16/80 sayıları incelemede.** 2026-09-06'da çekinme dedektörünün bir istem
rejiminde **doğru, atıflı bir cevabı** çekinme sayabildiği ölçüldü; resmî çıpada **en az bir
doğrulanmış yanlış pozitif** var ve bulaşmanın büyüklüğü **ölçülmedi**
([#60](docs/record/research_log/2026-09-06-hasat-kabul-olcutu-coktu.md)).

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
| [`docs/adr/`](docs/adr/) | 60 karar kaydı — bağlam, seçenekler, **elenenler** *(0059 rezerve, henüz yazılmadı)* |
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
