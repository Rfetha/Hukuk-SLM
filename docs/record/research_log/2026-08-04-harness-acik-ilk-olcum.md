# #51 — ⭐ HARNESS AÇIK ilk ölçüm: ürün sayısı ilk kez görüldü

**Tarih:** 2026-08-04 · **Sprint:** [`sprint3.md`](../../../sprint3.md) Adım 1-4
**Özne:** `tgta_v1` = `HakHukuk-4B-v0.1` (ham TIES) — harness KAPALI çıpasıyla **aynı artefakt**
([`kollar.md`](../kollar.md): `tgta_v1 == cp3-supurme-ham/*_tg_ta_ham_th_*`)
**Bedel:** GPU yerel $0 · **hakem $0,038** · **Çıktılar:** `outputs/eval/s3-harness-acik/`

> Bu sayı **hiç görülmemişti.** Bugüne kadarki her ölçüm harness KAPALI'ydı: modele altın
> madde (m1'de çeldiricilerle birlikte) **elle** veriliyordu. Harness AÇIK'ta bağlamı
> **retriever** seçiyor — yani ürünün gerçekte yapacağı şey.

## Kurulum

```
retriever   hibrit BM25 + BAAI/bge-m3, RRF · indeks 40.496 madde · k=5
chunk       TAM MADDE indekslenir, 900 karakter kırpması bağlam modele verilirken (ADR-0054/K2)
rejim       thinking on · 1024 düşünce + 512 cevap · seed 3407 · CTX 8192 · Q4_K_M + llama-server
tek fark    m1 ile h1 arasında SADECE bağlamın nereden geldiği. Kaynak bloğu biçimi,
            kırpma, sistem promptu ve üretim rejimi AYNI — yoksa kıyas kurulamaz.
geçerlilik  ✅ kesik 2/80 (%2,5 < %5) · düşünen 80/80 · zorla kapatılan 15/80
```

## ⭐ Tablo — harness AÇIK ↔ KAPALI, aynı model

| eksen | harness **KAPALI** (m1) | harness **AÇIK** (h1, k=5) |
| :--- | ---: | ---: |
| altın madde bağlamda | **garanti** (kurgu) | **60/80** — `recall@5` 0,750 |
| coverage (cevaplanan) | 63/80 = **0,7875** | 60/80 = **0,7500** |
| A1 (cevaplanan-only, tüm küme) | **0,9087** | **0,7823** |
| **kütle = coverage × A1** | **%71,6** | **%58,7** |
| ⭐ A1 · **altın getirilen** alt küme | 0,9087 *(hep getirilir)* | **0,9344** |
| atıf: doğrulanan / toplam | 87 / 89 | **89 / 89** |
| **uydurulmuş madde numarası** | **0** | **0** |
| katı kapı reddi | 2/80 | **1/80** |
| kapı sonrası coverage | — | **0,7375** |

## Üç okuma

### 1. Ürün sayısı oracle sayısından **düşük** — ve olması gereken bu

Kütle **%71,6 → %58,7**. Düşüşün tamamı erişimden geliyor: soruların %25'inde altın madde
ilk 5'e girmiyor ve model ya çekiniyor ya başka bir maddeden cevaplıyor. Bu, harness'ın
kusuru değil **ölçümün dürüstleşmesi**: bugüne kadarki sayılar modele doğru maddeyi elle
veren bir kurguda alınmıştı.

### 2. ⭐ Retriever doğru maddeyi bulduğunda model **daha** sadık: A1 0,9344 > 0,9087

Bu beklenmedik ve iyi bir sonuç. Altın getirilen 60 soruda A1 **0,9344** — m1'in
0,9087'sinin **üstünde**. Olası açıklama: m1 bağlamı 4 **hard-negative çeldirici** +
altından oluşuyor; retriever bağlamı ise konusal olarak yakın 5 gerçek maddeden oluşuyor
ve çeldiriciler kadar tuzaklı değil. Yani *"gerçek retriever daha gürültülü bağlam verir"*
varsayımı — S3'e girerken yazdığımız gerekçelerden biri — **bu ölçümde doğrulanmadı**.

### 3. ⚠️ Kapı fabrikasyona karşı çalışıyor ama asıl hatayı **yakalayamıyor**

Katı kapı 80 cevaptan **1**'ini reddetti ve doğrulanan atıf oranı **89/89**. Çünkü model
madde numarası **uydurmuyor** — bağlamdaki etiketi kopyalıyor. Asıl hata şurada:

```
altın geldi   → cevapladı   46
altın geldi   → çekindi     14
altın GELMEDİ → cevapladı   14   ← A1'i düşüren sınıf
altın GELMEDİ → çekindi      6
```

**14 soruda model altın gelmeden cevapladı** ve muhtemelen getirilen *başka* bir maddeden.
O atıf **gerçek** — korpusta var, doğrulanır, kapıdan geçer. Yani atıf doğrulayıcısı
*"uydurulmuş atıf"*ı çözüyor ama *"gerçek ama soruya uymayan madde"*yi çözmüyor. Bu
**tasarımın sınırı**, hatası değil — ve S3'ün asıl açığı olarak kayda geçiyor.

⛔ **Bu, Sprint 3'ün varlık gerekçesinin yarısını çürütüyor.** `sprint3.md` §"Neden harness"
madde 2 şunu diyordu:

```
A1  0,909 → atıf doğrulayıcı  uydurulan madde numarası yakalanır  deterministik
```

Uydurulan madde numarası **yok**. Doğrulayıcının yakalayacağı bir şey olmadığı için A1'e
katkısı **ölçülebilir biçimde sıfır**. A1'in açığı fabrikasyondan değil **isabetsizlikten**
geliyor ve o deterministik kodla çözülmüyor. Aynı maddenin `M2b` ayağı **çürümedi,
sınanmadı** — harness açık m2b hiç koşulmadı. Hüküm `sprint3.md`'ye de işlendi (çelişki
iki yerde birden işaretlenir kuralı).

Aynı bölümün 3. maddesi (*"gerçek retriever ~5 gürültülü parça verecek"*) de **zayıfladı**
— yukarıdaki 2. okuma ölçtü: retriever bağlamı m1'in çeldiricili bağlamından daha az tuzaklı.

## Doğrulayıcı kalibrasyonu — ADR-0038'in adını koyduğu borç ödendi

Katı kapıda **her yanlış negatif doğrudan coverage kaybıdır**. İlk koşuda 5 `KANUN_YOK`
çıktı; **gözle** okununca beşinin de yanlış negatif olduğu görüldü — model resmî adın
yaygın **kısa hâlini** yazıyor ve bu hâl resmî adın **soneki**:

| model yazdı | korpustaki resmî ad |
| :--- | :--- |
| `İflas Kanunu` | `İCRA VE İFLAS KANUNU` (2004) |
| `Teknik Düzenlemeler Kanunu` | `ÜRÜN GÜVENLİĞİ VE TEKNİK DÜZENLEMELER KANUNU` (7223) |
| `RÜŞVET VE YOLSUZLUKLARLA MÜCADELE KANUNU` | `MAL BİLDİRİMİNDE BULUNULMASI, RÜŞVET VE YOLSUZLUKLARLA MÜCADELE KANUNU` (3628) |

Ad indeksi ≥2 sözcüklü sonekleri de taşıyacak şekilde düzeltildi (1 sözcüklü sonek
*"Kanunu"* her kanuna uyar, dışlandı — testi var). **Etkisi:** `KANUN_YOK` 5 → 0, katı
kapı reddi 6 → 1. ⚠️ Bu **alet** düzeltmesi, eşik değil (tuzak 6.9 kuralı): ölçülen
büyüklük değişmedi, onu kestiren araç yanlış negatif veriyordu.

Aynı disiplin Adım 2'de dört hata daha yakalamıştı — hepsi **yanlış alarm** yönünde,
yani hakemsiz güvenilemezdi: ad çakışması (`İŞ KANUNU` = 4857 **ve** 1475) · yalnız BÜYÜK
harfli adı tanıma · Python `upper()`'ın Türkçe olmaması (`Medeni` → `MEDENI` ≠ `MEDENİ`) ·
ada kaçan önceki sözcük (`Ayrıca TÜRK BORÇLAR KANUNU`).

## Şerhler

- ⚠️ **A1 tek-altın yer-gerçeğine göre.** `groundedness --mode data` yalnız altın maddeyi
  doğru kabul ediyor; harness AÇIK'ta model **başka** bir maddeden doğru cevaplasa bile
  sadakatsiz sayılıyor. ON/OFF kıyası için kıyaslanabilir olan **A1 · altın getirilen alt
  küme** (0,9344). Tüm-küme A1'i (0,7823) bu yanlılığı taşıyor.
- ⚠️ **Soru kümesi erişim için yetersiz belirlenmiş** (#49, tuzak 7.4). `recall@5` 0,750
  bu kümenin tavanı. K4 kararı gereği ayırt-edicilik etiketi eklenip sayılar iki alt kümede
  ayrı raporlanacak — **bu tur henüz yapılmadı**, S3'ün açık borcu.
- ⚠️ **k=5 seçildi, süpürülmedi.** S3a eğrisi `recall@10` 0,875 / `@20` 0,925 diyor; k
  büyütmek erişimi yükseltir ama bağlamı uzatır ve 900 karakter kırpmasıyla etkileşir.
  k süpürmesi yapılmadı.
- ⚠️ Hakem `gpt-4o-mini`, insan-κ kalibresiz — mutlak değil, model-vs-model sıralama.

## Paper eşlemesi

**Results:** ilk harness-AÇIK ölçümü, KAPALI ile yan yana. **Ana bulgu:** erişim bulduğunda
model daha sadık (0,9344 > 0,9087), yani darboğaz model değil **erişim**. **Negatif/sınır
bulgusu:** atıf doğrulayıcısı fabrikasyonu çözüyor, *"gerçek ama soruya uymayan madde"*yi
çözmüyor. **Methodology:** deterministik doğrulayıcının kalibrasyonu ve yanlış-negatifin
katı kapıda doğrudan coverage kaybına dönüşmesi.
