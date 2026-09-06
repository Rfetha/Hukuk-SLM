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

## Madde (3) — ⏳ ÖLÇÜLÜYOR

M5 (kör/parametrik) **v2 biriminde hiç ölçülmedi**; 2026-09-07'de yerel `m5` koşusu başlatıldı
(`outputs/eval/f07-m5-anti-hedef/`). Kapı bu madde sayıyla kapanmadan **`v1.0` hükmü eksiktir**.
⚠️ M5 yükselmişse bugünkü kazancın bir kısmı **ezberden** gelmiş demektir — ADR-0039/0040 bu
ekseni tam olarak bunun için anti-hedef ilan etmişti.

## Ne KURULMAZ

1. **"TEST'te de geçeriz."** Ölçüm **DEV**'de; TEST'in erişim tavanı ≈%75 (ADR-0069) ve kabul
   testi koşulmadı.
2. **Hakem panelinden geçmiş bir hüküm.** Hâlâ **tek aile** (`gpt-4o-mini`), κ yok,
   self-preference ölçülmedi — kapanmamış borç.
3. **"Model bu kadar iyileşti."** Kazancın büyük kısmı **eğitimden değil ölçümden** geldi:
   soru onarımı (ADR-0067, `recall@10` +6,25 p), füzyon onarımı (ADR-0068), bütçe eşitlenmesi
   (ADR-0070). **Model ağırlıkları hiç değişmedi** — `tgta_v1` sabahki artefaktın aynısı.
