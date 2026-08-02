# ADR-0050 — Verim kapısının **tahmin edicisi** düzeltildi: kümülatif ortalama → **kararlı hız** (eşik **2,88** aynı)

**Statü:** Yürürlükte · **Tarih:** 2026-08-02
**Otorite belge:** `sprint2.md` CP2-c · **TADİL EDER:** [ADR-0047](0047-cp2-hedef-750-modal-hasat.md) **m.3**
(m.3'ün metni **değiştirilmedi**; bu ADR onun *tahmin edicisini* düzeltir — eşiğine dokunmaz)
**İlgili:** ADR-0042 (on-policy `rejected`) · ADR-0043 (bütçeli düşünce, rejim değişmezi) ·
ADR-0039 (*"kapı ölçemez hâle gelince kapı bölünür, eşik gevşetilmez"* emsali)
**Kanıt:** `hukuk-data:/cp2c/KUNYE.json` + `cp2c_m2_funnel.json` / `cp2c_m2b_funnel.json`
(app `ap-5f6rLHHFohhupMGvhkla9I`, 2026-08-02 16:19-16:46, kart `NVIDIA A100-SXM4-40GB`) ·
`research_log` [#48](../record/research_log/2026-08-02-cp2c-modal-koprusu.md) *"16:19-16:47 · üretim
denemesi ve verim kapısı olayı"* · **düzeltilen kod:** `scripts/cp2_harvest.py::kararli_hiz`
**Yeni yürütme tuzağı:** [6.9](../record/yurutme-tuzaklari.md)

---

## Bağlam — kapı, geçecek bir koşuyu durdurdu

ADR-0047 m.3 ön-kayıtlı bir yürütme kapısı kurmuştu: *"koşunun ilk dakikalarında gerçek verim
okunur, tahmini aşıyorsa koşu durdurulur."* Ölçtüğü büyüklük **ölçekte s/üretim**, eşik
**2,88 s/üretim** (`--gate-max-s-per-uretim`), bakma anı **600. saniye** (`--gate-after-s`).

CP2-c'nin ilk üretim koşusunda kapı **iki tipte de** tetiklendi:

| tip | denenen | kabul (regex) | oran | kümülatif s/üretim | geçen s | kapı damgası |
| :--- | --: | --: | --: | --: | --: | :--- |
| **m2** | 233 | 68 | %29,2 | 2,89 | 672,9 | 🔴 `DURDU: 2,97 > 2,88 (202. üretimde)` |
| **m2b** | 235 | 45 | %19,1 | 2,96 | 694,9 | 🔴 `DURDU: 2,95 > 2,88 (204. üretimde)` |

Kapı **doğru çalıştı**: eşiği aştığını gördü, koşuyu durdurdu, damgayı künyeye yazdı. Sorun
kapının varlığında ya da eşiğinde değil — **ölçme aletindeydi.**

### Teşhis: kapı doğru **büyüklüğe**, **yanlı bir tahmin ediciyle** bakıyordu

Kapı `geçen_süre ÷ tamamlanan` okuyordu, yani **t0'dan kümülatif ortalama**. Yüksek eş
zamanlılıkta `concurrency` kadar istek **aynı anda başlar ve aynı anda iner**; bu **açılış
geçicisinin** maliyeti kümülatif ortalamada **her kaleme paylaştırılır**. Sonuç: erken okumada hız
**sistematik olarak kötü** görünür.

Aynı m2 koşusunun logundan pencere pencere **marjinal** hız:

| pencere | üretim | süre | marjinal s/üretim |
| :--- | --: | --: | --: |
| 0 → 25 | 25 | 142 s | **5,70** ← açılış dalgası |
| 100 → 175 | 75 | 167 s | **2,22** |
| 100 → 200 | 100 | 238 s | **2,38** ← gerçek kararlı hız |
| 200 → 225 | 25 | 73 s | **2,90** ← kapı sonrası **boşalma** fazı (iş verilmiyor) |

→ m2'nin gerçek (kararlı) hızı ~**2,4 s/üretim**, yani eşiğin **ALTINDA**.

> ### 🔍 Yanlılığın sonuçtan bağımsız kanıtı — koşunun kendi logu
> Kapı **600. saniyede** `2,97` okuyup durdurdu. **Aynı koşu 673. saniyede zaten `2,89`'daydı.**
> Ölçülen büyüklük kararlı hâline doğru **hâlâ inerken** karar verilmişti. Kanıt bir yorum ya da
> yeniden koşu değil, durdurulan koşunun **kendi künyesi**.

7.500 üretimlik gerçek bir koşuda açılış dalgası toplam sürenin ~**%0,6'sıdır** — yani ölçekte
**amortize olur** ve kümülatif ortalama ile kararlı hız birbirine yakınsar. Yanlılık tamamen bir
**erken okuma** problemidir; kapı ise tanımı gereği erken okur.

### Yan bulgu — **tip asimetrisi** (yeni)

m2b, m2'den ~**%25 yavaş**: kararlı hız m2 ~**2,4** ↔ m2b ~**3,0** s/üretim (m2b penceresi
125→175). Sebep m2b isteminin **çeldirici blokları taşıması** → prefill daha uzun. Bu, m2b'nin
`-np 64`'te de eşiğe **yakın** koşacağı anlamına gelir ve koşu öncesinde yazılmıştır.

---

## Karar

### 1. Eşik **DEĞİŞMEDİ** — 2,88 s/üretim. Değişen, o büyüklüğü ölçen **alet**

Ön-kayıtlı olan **büyüklüktür** (ölçekte s/üretim) ve **eşiktir** (2,88); ikisi de yerinde duruyor.
Ön-kayıtlı olan, o büyüklüğün **hangi tahmin ediciyle** kestirileceği **değildi** — ADR-0047 m.3
yalnız *"gerçek verim okunur"* diyor, tahmin ediciyi belirtmiyor. Kapı artık **kararlı hızı** okur:

```
kararlı hız = (şimdi − boru hattının dolduğu an) ÷ (o andan sonraki üretim sayısı)
              boru hattı dolar  ⇔  tamamlanan üretim = concurrency
```

Uygulama: `scripts/cp2_harvest.py::kararli_hiz` — `t_warm`/`n_warm`, `tried == concurrency` anında
işaretlenir; boru hattı henüz dolmadıysa kümülatife düşer (koşunun çok kısa bittiği hâl).

### 2. Kümülatif sayı **huniden çıkmadı** — eski koşularla karşılaştırılabilirlik

`saniye_per_uretim` (kümülatif) yerinde duruyor, **yanına** `saniye_per_uretim_kararli` eklendi;
istatistik satırı **ikisini birden** basıyor. Sebep: bu hattın önceki bütün hız sayıları kümülatif
tahmin ediciyle ölçüldü (#48'in smoke tablosu dâhil); alanı silmek o sayıları okunamaz yapardı.
**Raporda ikisi birlikte verilir.**

### 3. Kapı `--limit` kontrolünden **ÖNCE** değerlendirilir

Aynı dosyada aynı gün bulunan ikinci kusur: bütçe (`--limit`) dolduğu için erken dönüldüğünde kapı
**hiç değerlendirilmeden atlanabiliyordu** ve huniye **hak edilmemiş** bir *"geçildi"* damgası
düşüyordu. Sabahki `-np 64` smoke'u (2,93 s/üretim, eşik 2,88) tam bunu yapmıştı. Artık kapı önce
değerlendirilir; hiç değerlendirilmediyse damga `değerlendirilmedi (koşu <gate_after_s>s'den kısa
bitti)` der. **Ön-kayıtlı bir kapının sessizce geçilmiş görünmesi, kapının hiç olmamasından kötüdür.**

### 4. ADR-0047 m.3'ün metni **değiştirilmez** — bu ADR onu **tadil eder**

m.3 olduğu gibi durur; yanına bu ADR'ye işaret eden bir satır düşülür. Karar değiştiğinde eskisi
silinmez (ADR-0047 üstüne yazmak, kapının o an nasıl kurulduğunu kayıttan siler ve paper'ın
Methodology'sini yalanlar).

---

## ⚖️ "Bu bir gevşetme mi?" — soru sorulur ve cevaplanır

**Sorulması gereken hâli:** karar **sonucu gördükten sonra** verildi. Kapı tetiklendi, koşu durdu,
para yandı — ve ardından ölçüm aracı değişti. Bu, dışarıdan bakan biri için *"kapıya takıldılar,
kapıyı değiştirdiler"* ile **aynı görünür**. Bu ADR'nin varlık sebebi o iki hareketi ayırmaktır.

**Cevap — üç dayanak:**

1. **Eşiğe dokunulmadı.** Ön-kayıtlı sayı (2,88) ve ölçtüğü büyüklük (ölçekte s/üretim) aynen
   duruyor. Gevşetme şıkkı (**B**) açıkça masaya kondu ve **açıkça reddedildi** (aşağıda).
2. **Yanlılık, sonuçtan bağımsız kanıtlandı.** Kanıt koşunun kendi logudur: kapı 600. saniyede 2,97
   okudu, **aynı koşu 73 saniye sonra 2,89'daydı** ve düşmeye devam ediyordu. Yani düzeltme
   *sonucu kurtarmak için* değil, *aletin yanlılığı ölçüldüğü için* yapıldı. Yanlılığın yönü de
   önceden bilinebilirdi: açılış geçicisi kümülatif ortalamayı **her zaman** yukarı iter, hangi
   koşuda olursa olsun.
3. **Karar insana götürüldü.** Ajan tek başına eşiğe de tahmin ediciye de dokunmadı; A/B/C
   şıkları sunuldu, insan **A**'yı seçti (2026-08-02).

**⚠️ Buna rağmen bir bedel kalır ve gizlenmez:** düzeltme **kapı tetiklendikten sonra** yapıldı.
Aynı yanlılık kapının *lehimize* çalıştığı bir koşuda ortaya çıksaydı fark edilir miydi — bu
soruya *"evet"* diyemeyiz. Bu yüzden madde **Limitations'a girer**: *ön-kayıtlı yürütme kuralları
ölçüm yanlılığına karşı bağışık değildir; bu hatta bir verim kapısı, eşiğini geçecek bir koşuyu
yanlı bir tahmin edici yüzünden durdurdu (bedel ~$1,2 GPU — panelden okunacak tahmin).*

---

## Reddedilen seçenekler

| # | seçenek | neden reddedildi |
| :-- | :--- | :--- |
| **B** | **Eşiği 2,88 → 3,2 gevşetmek** | ❌ **Sonucu gördükten sonra ön-kayıtlı bir eşiği oynatmak = çıpalama** ve ön-kayıt kurumunun kendisini geçersiz kılar. Bu hattın emsali tam ters yönde: ADR-0039'da kapı ölçemez hâle gelince **kapı bölündü**, eşik gevşetilmedi. Ayrıca gereksiz — gerçek hız (~2,4) eşiğin **altında**, yani gevşetmenin çözdüğü bir problem yok |
| **C** | **Kapıyı kabul edip CP2-c'yi negatif bulgu olarak kapatmak** | ❌ Dürüst ama **teşhisi yanlış**. Yanlış olan taşıyıcı (ADR-0047 m.2) ya da hasat tasarımı değil, **ölçen aletti**. Ölçüm aracının yanlılığını *"sonuç"* diye kaydetmek, kayda geçen sayıyı **kalıcı olarak yanlış** yapar ve gelecekteki her hasat kararını o yanlış sayıya dayandırır |
| — | **Kümülatif alanı huniden çıkarmak / üstüne yazmak** | ❌ Önceki bütün hız sayıları (smoke koşuları, #48'in tablosu) kümülatifti; alanı silmek onları okunamaz yapardı. Yan yana yazılır |
| — | **Kapıyı tamamen kaldırmak** | ❌ *Para akarken tahmine güvenilmez* (ADR-0047 m.3'ün gerekçesi, `fla-core` dersi #40 ve CP0.5 aynı şeyi söylüyor). Kapı bir kez yanlış tetiklendi diye kaldırılırsa, bir dahaki sefere **doğru** tetikleneceği koşuda kimse durdurmaz |

---

## Sonuçlar

- ✅ Kapı artık ölçmek üzere kurulduğu büyüklüğü ölçüyor: **kararlı hız**, açılış geçicisi hariç.
- ✅ **Eşik 2,88 s/üretim değişmedi**; ölçtüğü büyüklük değişmedi; ADR-0047 m.3 yürürlükte.
- ✅ Huni artık **iki tahmin ediciyi birden** yazıyor (`saniye_per_uretim` + `saniye_per_uretim_kararli`).
- ✅ Hak edilmemiş *"geçildi"* damgası kapandı → damga üç değerli: `DURDU… / geçildi / değerlendirilmedi`.
- ⚠️ **Limitations:** kapı bir koşuyu **hatalı** durdurdu (~$1,2 GPU, ⚠️ tahmin — panelden okunacak,
  tuzak 6.3); düzeltme **sonucu gördükten sonra** yapıldı ve öyle raporlanır.
- ⚠️ **Tip asimetrisi ön-kayda geçti:** m2b ~%25 yavaş (kararlı ~3,0 ↔ m2 ~2,4) → `-np 64` koşusunda
  da kapıya **yakın** koşar; takılırsa **m2 tam, m2b kısmi** kalır ve hedef 750 için ADR-0047'nin
  *koşullu geri alma* maddesi işler.
- ⏳ **Açık:** düzeltilmiş kapının ilk gerçek sınavı `-np 64` üretim koşusudur; sonucu #48'e yazılır.

## Paper eşlemesi

- **Methodology:** ön-kayıtlı yürütme kapılarında **büyüklük ↔ tahmin edici** ayrımı; kararlı-durum
  tahmin edicisinin tanımı ve kümülatif tahmin edicinin geriye dönük karşılaştırılabilirlik için
  **birlikte** raporlanması.
- **Limitations:** yukarıdaki iki ⚠️ maddesi birebir.
