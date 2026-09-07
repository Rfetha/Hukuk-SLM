# #63 — Skor kartının boşlukları kapatıldı: üç ölçüm, üçü de **kendi aleyhimize**

**Tarih:** 2026-09-07 · **harcanan:** **$0,21** · **GPU:** $0 (yerel)
**Neden bu tur açıldı:** `MODEL_CARD.md` klasik skor kartı düzenine çevrildi (sütunlarda modeller,
satırlarda eksenler) ve tabloda **11 "ölçülmedi" hücresi** çıktı. İnsan kararı: *"tamamını
kapamalıyız."* ⇒ Boşluklar tek tek fiyatlandırıldı ve kapatıldı.

## Bulgu 0 — Dört boşluk, **dört farklı sınıf**; kartta hepsi aynı görünüyordu

Asıl kusur buydu: `ölçülmedi` etiketi **boşluk · kayıt eksiği · insan-zamanı · karar** ayrımını
siliyordu.

| dipnot | hücre | gerçekte ne |
| :--- | ---: | :--- |
| ᵈ isabetsizlik | 3 | **insan-zamanı** — gözle okuma yalnız bizde yapılmıştı |
| ᵍ $/cevap | 4 | **kayıt eksiği** — girdi token'ı hiç kaydedilmemiş |
| ᶠ M5 | 3 | **karar** — ADR-0039 rakip çıpasını reddetmişti |
| ᵇ base sütunu | 8 | **boşluk** — base hiç harness AÇIK koşulmamış |

## Bulgu 1 — İsabetsizlik: *"biz iyiyiz"* cümlesi **KURULMUYOR**

Üç rakip kolu **80/80 gözle** okundu, `f02/GOZLE_OKUMA_80.md` §2 ile **birebir aynı tanım**:

| özne | isabetsizlik | cevaplanan tabanda |
| :--- | ---: | ---: |
| **biz** | **8/80** | 8/75 = %10,7 |
| 3.1 Flash-Lite | **8/80** | — |
| 3.5 Flash-Lite | **7/80** | — |
| 3.5 Flash | **8/80** | 8/71 = **%11,3** |

⛔ **Kurulmayacak cümle:** *"İsabetsizlikte berabereyiz, o hâlde eşitiz."* İki 8 **aynı tabanda
değil** — Flash 9 kalemde sustuğu için 71'de sınandı, biz 75'te.

⭐ **Asıl sarsıcı bulgu:** f02'de bizim isabetsiz olduğumuz **id 27 ve 42**, kendi öz-denetimimizde
*"benim soru yazımım komşu maddeye kaydırdı"* diye işaretlediğimiz kalemlerdi. **Rakip o tuzağa
düşmedi** ⇒ kaynağı soru **değil, model** olabilir. Bu, **B1 turunun hedefini doğrudan değiştirir**:
soruyu onarmak yerine modeli düzeltmek gerekiyor olabilir.
⭐ Üç kolda da isabetsiz olan **id 32 · 36 · 61** ise **ortak zorluk** adayı — model kusuru değil.

## Bulgu 2 — `$/cevap`: kayıt eksiği **yeniden koşmadan** kapatıldı

Girdi token'ı `detail.jsonl`'e hiç yazılmamıştı. Yeniden üretim ~$1,22 tutacaktı.
⭐ **Ucuz yol ölçümle bulundu:** istem 80/80 **bayt-bayt aynı**, ve üç Gemini **aynı tokenizer'ı**
kullanıyor — 3 kalemde sınandı, `prompt_tokens` birebir (**2842 / 2681 / 2343**). ⇒ Sayım yalnız
**en ucuz** modelde yapıldı, fiyatlar ayrı uygulandı: **$0,48 yerine $0,0487'ye AYNI exact sayı.**

| özne | $/cevap | girdi tok | çıktı tok |
| :--- | ---: | ---: | ---: |
| 3.1 Flash-Lite | $0,001895 | 193.042 | 68.916 |
| 3.5 Flash-Lite | $0,001152 | 193.042 | 13.685 |
| **3.5 Flash** | **$0,009914** | 193.042 | 55.950 |
| biz · base | **$0** | — | yerel GPU |

⭐ Girdi token'ı üçünde **birebir aynı (193.042)** — **eşit sınavın maliyet tarafındaki kanıtı**.
⭐ Kapı çıpası 3.5 Flash, 3.5 FL'nin **8,6 katı**.
🆕 **Kayıt kuralı doğdu:** bundan sonraki her koşu `prompt_tokens`'ı da yazacak.

## Bulgu 3 — M5: düşük olmamız **iki şey birden** söylüyor

| özne | M5 A1 | **ezber kütlesi** |
| :--- | ---: | ---: |
| **biz** | 0,4105 | **0,3900** |
| base | 0,4818 | 0,4698 |
| 3.1 Flash-Lite | 0,6795 | 0,6710 |
| 3.5 Flash-Lite | 0,7013 | 0,7013 |
| **3.5 Flash** | **0,8241** | **0,8241** |

⛔ ***"M5'te rakipleri yendik"* KURULMAZ.** M5 bir **anti-hedef** ve kapı çıpası **base**'dir —
ADR-0039 §2 rakip çıpasını değerlendirip **reddetti**. Düşük M5 bizim için *"kaynağa dayanıyoruz"*
demek; **aynı sayı** aynı zamanda *"Gemini Türk hukukunu kaynaksızken bizden **iki kat** iyi
biliyor"* demektir (0,8241 ↔ 0,4105).
⭐ DRY rakiplere **uygulanamadı** (llama.cpp örnekleyicisi) — **ve ölçüldü ki gerekmiyor**:
üç kolda da döngü **yok**, kesiklik %0 · %0 · %2,5.

## Bulgu 4 — Base aynı bütçede **ÖLÇÜLEMİYOR**, ve sebebi bir bulgu

Base harness AÇIK koşuldu ve **geçerlilik kapısından kaldı**: kesik **16/80 = %20** (eşik %5).
Hakem çağrılmadı — kapı parayı korudu.

🔬 16 kesiğin **15'i GERÇEK kesilme**, yalnız 1'i döngü ⇒ **DRY işe yaramaz** (M5'in tam tersi).
Sebep: base **uzun, kaynak alıntılayan** cevaplar yazıyor ve **1536'ya sığmıyor**.

⭐ **Karşılaştırma bulgunun kendisi:** base **kör modda** (kaynaksız) yalnız **2/80** kesik veriyor.
⇒ Base'i şişiren şey **kaynakların kendisi**. Bu, [#42](2026-07-29-cp0-dusunce-modu-sonlanmama.md)'nin
*"`τ_g` kendi kendine sonlanıyor — ince ayar muhakemeyi stabilize etti"* bulgusunun **harness
açıkken** ölçülmüş hâli: aynı bütçede **biz 4/80, base 16/80**.

⚠️ 🚨 **Modal bunu ÇÖZMEZ** — kesiklik donanımdan değil **bütçeden**. Modal'ın verdiği hız.
⇒ Tek anlamlı yol **daha büyük bütçe + "EŞİT SINAV DEĞİL" damgası**; koşu bütçe **2048** ile
yeniden başlatıldı (`f11-base-harness-butce2048`, yerel, $0).
⛔ O sayılardan ***"ince ayar şu kadar kazandırdı"* cümlesi KURULAMAZ** — fark ince ayardan mı
bütçeden mi **ayırt edilemez**.

## 🆕 Borç — eval setinde **altın etiket şüphesi** (id 46)

**İki bağımsız gözle okuma, birbirinden habersiz, AYNI kalemi işaretledi.**
Altın **KMK 53** (1965 öncesi irtifak haklarına dair **geçiş hükmü**) ↔ modelin dayandığı
**KMK 14**, ki lafzen *"Kat mülkiyetine geçişte ayrıca yönetim plânı istenmez"* diyor ⇒ **soruyu
doğrudan karşılıyor**. Üç kolda da **sınır durum** sayıldı, hiçbirinde sayıya katılmadı
⇒ **üç öznenin de sayısı bugün alt sınırda**.
🚨 Doğruysa bu bir **model kusuru değil ÖLÇÜM kusurudur** ve Faz 0'ın beş kusuruyla **aynı sınıf**.
⛔ Bugün düzeltilmedi: altın etiket değişikliği ADR-0067'nin **insan onayı** usulünü ister ve
**donmuş TEST'i** de ilgilendirir.

## Ders

**Bir skor kartında `ölçülmedi` yazmak, ölçmemekten daha tehlikeli olabilir** — çünkü dört farklı
şeyi (boşluk · kayıt eksiği · insan-zamanı · karar) tek etiket altında saklıyor ve okur hepsini
*"ölçemedik"* diye okuyor. Dördü ayrıştırılınca **üçü $0,21'e kapandı**, dördüncüsü ise
*"ölçülemedi"*ye dönüştü — ve o dönüşüm **kendi başına bir bulgu** oldu.

⚠️ Ve bu turun üç sayısı da **kendi aleyhimize** çıktı. Üçü de olduğu gibi yazıldı.
