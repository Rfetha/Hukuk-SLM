# ADR-0064 — `v1.0` kapısı: üç maddeli, δ = 2,0 puan · ön-kayıtlı formül, mekanik sayı

**Tarih:** 2026-09-06 (formül) · 2026-09-07 (sayılar) · **Statü:** ✅ yürürlükte · **Karar:** insan
**Bağlı:** [ADR-0050](0050-verim-kapisi-tahmin-edici-duzeltmesi.md) (eşiği insan koyar, koşudan
ÖNCE) · [ADR-0057](0057-harness-rekabet-kapisi-esit-sinav.md) (eşit sınav) ·
[ADR-0065](0065-bolunmus-surumleme.md) (ürün ↔ iddia sürümü)

## Ön-kayıt sırası — kural gereği

**Formül 2026-09-06 öğleden önce**, hiçbir rakip sayısı görülmeden yazıldı. Çıpa
(`3.5 Flash`) o an **hiç ölçülmemişti**. Sayılar 2026-09-07'de mekanik olarak türedi.
⇒ Eşik sonuçtan sonra oynatılamaz; ARA KAPI'nın kalıbı budur.

## Kapı

```
(1) kütle ≥ (3.5 Flash'ın kütlesi) − 2,0 puan     ← ASIL KAPI, eşleşmiş rejim, aynı 80 soru
(2) isabetsizlik GERİLEMEZ                         ← vatandaş için en tehlikeli kusur sınıfı
(3) M5 (kör/parametrik) YÜKSELMEZ                  ← ANTİ-HEDEF, ezber kazancı kapıdan geçmez
(*) her sayım adımında GÖZLE OKUMA zorunlu         ← sayısal kapı bozuk ölçümü bir kez geçirdi
```

### δ = 2,0 puan — neden bu sayı

⚠️ **Gürültü tabanına dayalı bir δ KURULAMAZ:** hakem yeniden-koşum tabanı (0,3 p) yalnız **A1**
için ölçüldü; kütle = coverage × A1 ve **coverage'ın varyansı o tabanda yok**. δ bu yüzden
ölçümden değil **insan kararından** gelir: *"yetişti"* demeyi hak edecek kadar dar, ölçüm
gürültüsünün altına düşmeyecek kadar geniş.

### Bağlayıcı okuma: **GÖZ-katı** (insan kararı, 2026-09-07)

Çekinme dedektörü rakip şablonlarında **fazla red sayıyor** (F0.4 kalibrasyonu: 28 rakip
kalemi gözle okundu; 3.1 FL'de 3, 3.5 FL'de 2, Flash'ta 1 **açık yanlış pozitif** + 5 çekinceli
cevap; bizim kolda **0**). Üç okuma da raporlanır, **bağlayıcı olan en muhafazakârı**:
rakiplerin çekinceli cevapları da **cevap** sayılır → onların kütlesi en yüksek, farkımız en dar.
⇒ *"Kendi lehine okudun"* denemez.

## Madde (1) — ✅ GEÇTİ

*(kaynak: `outputs/eval/f04-rakip-onsozsuz/KALIBRASYON_ve_OZET.md` · `f02-biz-onsozsuz/harness_tablo.json`)*

| okuma | 3.5 Flash | eşik = Flash − 0,020 | BİZ | hüküm | fark |
| :--- | ---: | ---: | ---: | :--- | ---: |
| ALET (ham) | 0,6925 | 0,6725 | 0,8011 | ✅ | +10,86 p |
| GÖZ-orta | 0,7050 | 0,6850 | 0,8011 | ✅ | +9,61 p |
| **GÖZ-katı — BAĞLAYICI** | **0,7425** | **0,7225** | **0,8011** | ✅ **GEÇTİ** | **+5,86 p** |

**Eşit sınav kanıtlandı, varsayılmadı:** `recall@10` dört öznede de **0,9500**;
`context_shown` **80/80 bayt-bayt aynı**; istem, bütçe (1536, ADR-0070) ve hakem yığını aynı.

## Madde (2) — çıpa YENİ BİRİMDE yeniden türetildi

Spec'te *"≤ 7/80"* yazıyordu. O sayı **v1 soru setinden** geliyordu ve **hiç gözle sayılmamıştı**.
2026-09-06'da v2 biriminde **ilk kez tam gözle** sayıldı: **8/80** (75 cevaplanan kalemin
tamamı tarandı; iki otomatik süzgeç de tek başına yetmiyor — ADR-0066).

**Karar (insan): çıpa 8/80'e yeniden çivilenir, kural "gerileme yok".**
Dayanağı ADR-0050'nin kendi hükmü: *"alet düzeltilir, eşik oynatılmaz — ama alet değişirse
eşik aynı formülle **yeni birimde yeniden türetilir**."* Eşik **gevşetilmiyor**, birimi
düzeltiliyor. `7/80` ile `8/80` **aynı birimde değildir** ve kıyaslanamaz.

**Bugünkü değer = çıpa = 8/80** ⇒ madde (2) bugün **tanım gereği sağlanıyor**; bağlayıcı
olduğu yer **bir sonraki eğitim turudur** (B1).

## Madde (3) — ✅ GEÇTİ *(2026-09-07)*

*(kaynak: `outputs/eval/f07-m5-anti-hedef/KUNYE.json` · `GOZLE_OKUMA_CEKINME.md`)*

### 🚨 Önce: bu maddenin ÇIPASI YOKTU

Madde *"M5 ≤ **bugünkü**"* diye yazılmıştı, ama `tgta_v1`'in M5'i **hiçbir birimde hiç
ölçülmemişti** (defterde yalnız `base_th` · `gem_th` · `tg_v1_th`; **merge öznesi yok**).
*"Bugünkü"* diye bir sayı olmadığı için madde **kendi kendine referans veriyordu** ve hiçbir
hüküm üretemezdi. Ön-kayıt kuralına uyduğu için de denetimden geçmişti.

Çıpa [ADR-0039](0039-kapi-6-parametrik-sizinti.md) §2'den okundu: **çıpa BASE'dir, rakip
değil** — rakip çıpası orada zaten **değerlendirilip reddedilmişti** (*"modeli aldığımız
noktadan kötüye götürmemeliyiz"*). Ve **üç sayı birden** raporlanır.
⇒ Base **aynı birimde yeniden koşuldu.** Tuzak listesine **2.17** olarak yazıldı.

### Rejim: DRY — ve bu da bir insan kararıydı

İlk koşu **geçerlilik kapısından kaldı** (kesik 5/80 = %6,2 > %5, `EXIT=2`, hakem çağrılmadı).
Gözle okundu: **3 yozlaşmış tekrar** (×21 · ×19 · ×82) + 2 bütçe kesilmesi. ADR-0040'ın
*"MAXTOK büyüt"* reçetesi üçünde **ölçülmüş biçimde etkisiz**. $0'lık ablasyon DRY'nin
döngüyü de kesikliği de sıfırladığını gösterdi ⇒ [ADR-0073](0073-m5-rejimine-dry-eklendi.md).
⛔ **Eşik oynatılmadı; değişen ALET.**

### Sayılar — İKİ okuma birden

| kol | okuma | `coverage` | `A1` | **ezber kütlesi** |
| :--- | :--- | ---: | ---: | ---: |
| **BİZ** | ALET | 0,9500 | 0,4105 | **0,3899** |
| **BİZ** | **GÖZ** | 1,0000 | 0,4057 | **0,4057** |
| base | ALET | 0,9750 | 0,4818 | **0,4697** |
| base | **GÖZ** | 1,0000 | 0,4739 | **0,4739** |

```
ALET  coverage 0,9500 ≤ 0,9750 ✅   ezber kütlesi 0,3899 ≤ 0,4697 ✅  (−7,98 p)
GÖZ   coverage 1,0000 ≤ 1,0000 ✅   ezber kütlesi 0,4057 ≤ 0,4739 ✅  (−6,82 p)
```

⭐ **Hüküm dedektöre bağımlı DEĞİL** — dedektörün kusuru iki kolu da aynı yönde etkiliyor;
ADR-0057'nin eşit sınavı burada **koruyucu** görev görüyor.

### Gözle okuma (madde * gereği) — alet ÜÇÜNCÜ kez yanıldı

Alet 6 kalemi çekinme saydı; göz **6/6'sını yanlış pozitif** buldu. Altısı da hukuki bir
**olumsuz hüküm** kuruyor **ve atıf yapıyor** — yani cevap veriyor, üstelik çoğu **yanlış**
(base id 16: *"4711 Sayılı Türk Hakemlik Kanunu"* — **var olmayan bir kanun**).
Mekanizma: `REJECT_RE`'nin *"bulunmamaktadır"* ailesi hukuk metninde iki iş görür — *"kaynakta
yok"* (çekinme) ↔ *"kanunda böyle bir hüküm yok"* (**esasa ilişkin cevap**). **Kör modda kaynak
yoktur** ⇒ birinci okuma tanımı gereği imkânsız.
⇒ `suskunluk_terazisi`'nin üçüncü yanılması (14→8 · 11→7 · **6→0**), üçünde de **fazla red**.
🆕 Açık borç: `exact_reject`'in kör mod dalı. ⛔ **Bugün düzeltilmedi** — kapının sayısı
üretildikten sonra aleti değiştirmek ADR-0050'nin yasakladığı hareketin sınırındadır.

### Okuma

Model **kaynaksızken base'den daha az isabetli** (A1 0,4057 ↔ 0,4739) ve gözle bakıldığında
**iki kol da hiç susmuyor** (80/80 konuşuyor). ⇒ **Kazanç ezberden gelmiyor.** İnce ayar
modeli kaynaksızken daha çok konuşturmuş ya da daha çok tutturmuş olsaydı **burada görülürdü**;
tersi çıktı. İstenen yön budur: *"güncellik kütüphanede, ağırlıkta değil."*

---

## 🟢 KAPI KAPANDI — üç madde de sayıyla

| madde | hüküm | sayı |
| :--- | :--- | :--- |
| (1) kütle ≥ Flash − 2,0 p | ✅ **GEÇTİ** | GÖZ-katı **0,8011 ↔ eşik 0,7225** → **+5,86 p** |
| (2) isabetsizlik gerilemez | ✅ | çıpa **8/80**'e yeni birimde çivilendi; bağlayıcı olduğu yer **sonraki tur** |
| (3) M5 yükselmez | ✅ **GEÇTİ** | ezber kütlesi **−6,82 p** (GÖZ) / **−7,98 p** (ALET) |
| (*) her sayımda gözle okuma | ✅ | üç sayım adımında da yapıldı; **ikisinde alet yanıldı** |

## Ne KURULMAZ

1. **"TEST'te de geçeriz."** Ölçüm **DEV**'de; TEST'in erişim tavanı ≈%75 (ADR-0069) ve kabul
   testi koşulmadı.
2. **Hakem panelinden geçmiş bir hüküm.** Hâlâ **tek aile** (`gpt-4o-mini`), κ yok,
   self-preference ölçülmedi — kapanmamış borç.
3. **"Model bu kadar iyileşti."** Kazancın büyük kısmı **eğitimden değil ölçümden** geldi:
   soru onarımı (ADR-0067, `recall@10` +6,25 p), füzyon onarımı (ADR-0068), bütçe eşitlenmesi
   (ADR-0070). **Model ağırlıkları hiç değişmedi** — `tgta_v1` sabahki artefaktın aynısı.
