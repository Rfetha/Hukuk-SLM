# HakHukuk

> # 🚨 SAYILAR 2026-09-07'DE DEĞİŞTİ — AŞAĞIDAKİLER ESKİ BİRİMDEDİR
>
> Bu belgedeki **her** kütle/aşırı-red/A1 sayısı **v1 soru seti · `RRF_K=60` · 1024 üretim
> bütçesi** birimindedir ve bugünkü sayılarla **KIYASLANAMAZ**. Faz 0 ölçüm zinciri aletin
> dört kusurunu buldu (soru seti · füzyon · DEV↔TEST bileşimi · **rakiple eşit olmayan üretim
> bütçesi**) ve **model ağırlıklarına hiç dokunmadan** sayılar değişti:
>
> | eksen | bu belgede (eski) | **ölçülen (v2 birimi)** |
> | :--- | ---: | ---: |
> | sadık-cevap kütlesi | %68,4 | **%80,1** |
> | `recall@10` | 0,875 | **0,9500** |
> | aşırı-red | 9/80 | **4/80** |
> | uydurulmuş madde | 0/83 | **0/114** |
>
> ⛔ **Bu belgedeki rakip kıyas cümleleri geçersizdir.** Eşit sınavda ölçülen yeni tablo:
> BİZ **0,8011** ↔ 3.1 FL 0,7058 ↔ 3.5 FL 0,7622 ↔ **3.5 Flash 0,7425** (bağlayıcı GÖZ-katı
> okuması). `v1.0` kapısı madde (1) **geçildi**.
>
> Kaynaklar: [`research_log #62`](docs/record/research_log/2026-09-06-faz0-olcum-zinciri.md) ·
> [ADR-0064](docs/adr/0064-v1-kapisi-uc-maddeli-on-kayit.md) ·
> [ADR-0067](docs/adr/0067-soru-onarimi-dev-test-v2.md) ·
> [ADR-0068](docs/adr/0068-rrf-k-60-to-10.md) ·
> [ADR-0070](docs/adr/0070-uretim-butcesi-esitlendi.md) ·
> [`f04-rakip-onsozsuz/KALIBRASYON_ve_OZET.md`](outputs/eval/f04-rakip-onsozsuz/KALIBRASYON_ve_OZET.md)
>
> **Bu belge belge-katmanı turunda yeniden yazılacak; bant o zaman kalkar.**


**Dizüstü bilgisayarda koşacak kadar küçük, "bilmiyorum" demeyi öğrenmiş bir Türkçe hukuk asistanı.**

[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[Model kartı](MODEL_CARD.md) · `ROADMAP.md` ⚰️ *(2026-09-06'da silindi → [güncel plan](docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md); yeniden yazımı **Görev 13**)* · [English](README.md)

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
| coverage | 0,788 | **0,8250** ~~0,7625~~ | **0,9000** ~~0,7625~~ |
| sadık-cevap kütlesi | %71,6 | **%68,4** ~~%62,8~~ | **%73,0** ~~%61,3~~ |
| A1 · cevaplanan | 0,909 | **0,8288** | 0,8110 |
| A1 · altın getirilen alt küme | 0,909 | **0,8729** | 0,8593 |
| **uydurulmuş madde numarası** | 0 | **0 / 83** | 0 / 118 |
| altın bağlamdayken çekindi ↓ | 17/80 | **9/80** ~~14/80~~ | **5/80** ~~16/80~~ |
| *başka bir gerçek* maddeden cevapladı ↓ | — | **5/80** | 7/80 |

> 🚨 **YENİDEN PUANLANDI 2026-09-06 — çekinme dedektörü bozuktu ve yalnız BİZİ cezalandırıyordu.**
> Açılış hükmü olmayan dalda `exact_reject` **cevabın tamamını** tarıyordu; bizim cevap
> şablonumuzun eleme gerekçesi (*"diğer kaynaklar … **içermemektedir**"*) red regex'ini
> tetikliyordu. Gemini'nin cevaplarında o kalıp yalnız **3/80** kalemde var, yani hata
> **bizim kendi eğitim şablonumuza özgüydü**. Onarım **bizim** sayılarımızı oynattı, rakibinkine
> **hiç dokunmadı** (varsayılmadı, ölçüldü).
> **80 kalem gözle okunduğunda** aşırı-red **8/80** ve kütle **%69,6**; alet 9/80 ve %68,4
> veriyor — **yayımlanan aletin sayısıdır**, çünkü senin yeniden üretebileceğin odur.
> Eski değerler **silinmedi**, üstü çizildi.
> [ADR-0061](docs/adr/0061-cekinme-dedektoru-istem-rejimi-bagimliligi.md) ·
> [#61](docs/record/research_log/2026-09-06-dedektor-onarimi-b10-yeniden.md) ·
> kalem kalem kayıt: `outputs/eval/olcum-bi/B10_GOZLE_OKUMA_80.md`

> 🚨 **Ve yeniden puanlama ADR-0058'in kendi gerekçesini TERSİNE ÇEVİRDİ — iki sütundan birini
> alıntılamadan önce bunu oku.** Önsöz **kütleyi yükselttiği için** benimsenmişti (%61,3 → %62,8).
> Onarılmış aletle **düşürüyor**: **önsözlü %68,4, önsözsüz %73,0** (−4,6 puan). Çift gerçekten
> eşleşmiş bir sınav — aynı 80 id, **80/80 birebir aynı `context_shown`**, aynı `recall@10`;
> değişen tek şey istem. Ama önsözün **diğer ayakları hâlâ ayakta**: A1 **0,8288 ↔ 0,8110** ve
> isabetsizlik **5/80 ↔ 7/80**, ikisi de önsözün lehine. Takas iki yönlü: önsöz modeli
> **daha seçici ama daha suskun** yapıyor.
> **Protokol DEĞİŞTİRİLMEDİ** — bu kendi ADR'sini ve insan kararını ister (açık soru **S14**).
> Resmî = önsözlü.

**Arkasında durduğumuz sayı %68,4.** KAPALI sütunuyla arasındaki fark bir gerileme değil —
iki ölçüm aynı şeyi ölçmüyor ve KAPALI bir rakip değil **tavan**.

> ⚠️ Aşağıdaki ayrıştırma **önsözsüz** çıpaya (%61,3) karşı, yani 10,2 puanlık açık için
> yapıldı. ADR-0058 sonrası açık **8,8 puandır** ve **yeniden ayrıştırılmamıştır.**

10,2 puanlık açığı ayrıştırdık:
**≈5,1 puan erişim ıskası** (harness'ın — 10/80 soruda altın madde hiç gelmiyor) +
**≈4,5 puan dikkat dağılması** (modelin — altın getirildiğinde bile yanına dokuz madde
konunca A1 0,909 → 0,862 düşüyor).

⚠️ **İndirmeden önce bilinmesi gereken bir sonuç.** %68,4 sayısı *model + retriever + önsöz*
üçlüsünün sayısıdır. Önsöz bugün tek bir ölçüm script'inin içinde duruyor ve dağıtılmıyor,
retriever da aşağıdaki servis yoluna bağlı değil — dolayısıyla modeli düz indiren kişi manşeti
değil **ablasyon** sütununu (%73,0) yeniden üretir. İkisini de paketlemek `v1`'in ilan edilmiş
şartıdır (`ROADMAP.md` ⚰️ *(2026-09-06'da silindi → [güncel plan](docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md); yeniden yazımı **Görev 13**)*).
*(Evet — ablasyon sütunu şu an **daha yüksek**. Yukarıdaki ADR-0058 şerhine bak: bu tersine
dönüş **açık bir soru**, ablasyonu ürün diye dağıtmanın gerekçesi değil.)*

🚨 **Ve ölçüm kendi planımızı çürüttü.** Atıf doğrulayıcıyı A1 açığını kapatmak için
kurduk. **Sıfır** uydurulmuş madde numarası buldu — yakalamak için kurulduğu sınıf
**boş**. Model numara uydurmuyor; erişim ıskaladığında *başka bir gerçek* maddeden
cevaplıyor (**5/80**; önsözsüz ablasyon: 7/80). Asıl büyük hata hâlâ bunun tersi: **9/80**
(ablasyon: 5/80) soruda model, altın madde **bağlamındayken** çekiniyor — harness kapalıyken
17/80, yani bir **model** özelliği, erişim özelliği değil. Deterministik kod bunu kapatamaz.
Ayrıntı ve tam kayıt: `ROADMAP.md` ⚰️ *(2026-09-06'da silindi → [güncel plan](docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md); yeniden yazımı **Görev 13**)* · `sprint3-part1.md` ⚰️ *(arşiv silindi; borç kuyruğu **`DEVIR-PROMPT.md` *(silindi)* §5**'e kurtarıldı)*.

✅ **Bu sayılar 2026-09-06'ya kadar 14/80 ve 16/80'di — yanlıştılar, ve bu düzeltme turun
ürettiği en değerli şey oldu.** Dedektör onarıldı, **80 kalemin tamamı gözle okundu**, gerçek
sayı **8/80** çıktı (alet 9/80 diyor). Eski on dördün **altısı** doğru, atıflı cevaptı ve
yanlışlıkla red sayılmıştı; ters yönde **hiçbir çekinme kaçırılmamıştı**. Bu açığı kapatmak için
bir eğitim turu planlanmıştı — **iptal edildi**, çünkü ön-kayıtlı hedef (8-11/80) **hiç eğitim
yapılmadan** zaten karşılanmıştı: *"sorunun"* **%43'ü ölçüm aletinin kendisiymiş**.
⛔ **Küçüldü, yok olmadı** — 8/80 hâlâ Gemini 3.5 Flash-Lite'ın 6/80'inin üstünde.
[ADR-0062](docs/adr/0062-b10-turu-kapatildi-hedef-egitimsiz-karsilandi.md) ·
[#60](docs/record/research_log/2026-09-06-hasat-kabul-olcutu-coktu.md) ·
[#61](docs/record/research_log/2026-09-06-dedektor-onarimi-b10-yeniden.md)

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
bash scripts/egitim/setup_llamacpp.sh

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
