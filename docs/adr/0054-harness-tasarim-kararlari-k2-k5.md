# ADR-0054 — Harness tasarım kararları kilitlendi: K2 · K3 · K4 · K5

- **Tarih:** 2026-08-04
- **Durum:** kabul edildi
- **Karar veren:** insan (K2, K4) · S3a ölçümü (K3) · ADR-0038 yürürlükte (K5)
- **Kaynak ölçüm:** [research_log #49](../record/research_log/2026-08-04-s3a-on-prob.md)
- **Açar:** `sprint3.md` Adım 1-4 (bu ADR'siz kod yazılamıyordu — sprint'in ⛔ kuralı)

## Bağlam

`sprint3.md` beş tasarım kararını kod yazımının **önüne** koydu. K1 (gömme modeli) S3a
ön-probunda ölçümle kapandı (`BAAI/bge-m3` + BM25, RRF hibriti). Kalan dördü bu ADR'de.

---

## K2 — Chunk birimi: **tam madde indekslenir, kırpma modele verirken**

**Karar:** retriever eşleşmeyi maddenin **tamamı** üzerinde yapar. ADR-0011'in 900 karakter
kırpması **yalnız bağlam modele verilirken** uygulanır — yani bugünkü eval'de uygulandığı
yerde, aynı noktada.

**Gerekçe:** eval-ayna kuralının koruduğu şey *"modelin eğitimde gördüğü uzunlukla eval'de
gördüğü uzunluk aynı olsun"*dur; kuralın öznesi **modelin girdisi**, indeks değil. İndeksi
de kırpmak, uzun maddelerin 900 karakterden sonraki hükümlerini **aranamaz** hale getirirdi
— eval-ayna kuralının hedeflemediği bir kayıp.

**Kabul edilen bedel:** retriever'ın eşleştiği metin ile modelin gördüğü metin **aynı
değil**. Bir madde, yalnız 900 karakterden sonraki kısmı yüzünden getirilip modele o kısım
olmadan verilebilir. Bu **ölçülebilir** ve harness-AÇIK ölçümünde *"getirildi ama cevap
kırpılan kısımdaydı"* vakası olarak raporlanır.

**Yan sonuç:** S3a'nın recall sayıları tam madde üzerinde ölçüldü → **aynen geçerli**,
yeniden ölçüm gerekmiyor.

---

## K3 — Statik korpus mu, canlı API mi: **statikle başla, canlı katman sonra**

**Karar:** harness `data/corpus/mevzuat_maddeler.jsonl` (29 Temmuz anlık görüntüsü, 40.496
madde) üzerine kurulur. Canlı `bedesten` katmanı S3'ten **sonra** eklenir.

**Gerekçe:** ölçüm tekrarlanabilirliği. Canlı API'nin içeriği koşular arasında değişirse
harness-AÇIK sayıları kıyaslanamaz hale gelir. S3a bedesten sözleşmesinin **geçerli**
olduğunu doğruladı (4/4 çağrı `SUCCESS`), yani canlı katman bir **risk** değil bir
**sıralama** meselesi — güncellik iddiası ayakta, uygulaması ertelendi.

---

## K4 — Harness AÇIK ölçüm protokolü: **küme değişmez, ayırt-edicilik etiketi eklenir**

**Karar:** `data/eval/dev/core_hard.jsonl` **değiştirilmez**. Her soruya *"kendi başına
ayırt edici mi"* etiketi eklenir ve harness sayıları **iki alt kümede ayrı** raporlanır.

**Bağlam (S3a bulgusu):** DEV soruları altın madde elde tutularak üretildi; ~%25'i tek
başına hangi kanuna ait olduğunu söylemiyor (*"Başvurum kabul edilirse ne olur?"*).
Ölçüldü: aday havuzu altının kendi kanunuyla sınırlanınca aynı BM25 `recall@10`
**0,625 → 0,875**. Yani `recall@k` retriever kabiliyetinin değil **kümenin** tavanı.

**Neden küme değiştirilmiyor:** sayı görüldükten **sonra** küme değiştirmek, dışarıdan
*"kümeyi cilaladılar"* diye okunur — tuzak 6.9'un kuralının veri tarafındaki karşılığı:
*sonucu gördükten sonra ölçüt değil ALET düzeltilir.* Etiket, kümeyi değiştirmeden aleti
keskinleştiriyor: tek sayı yerine iki eksen.

**⚠️ Etiketleme yöntemi — dürüstlük şartı.** Etiket, **erişim sonucundan habersiz** bir
hakemle atanır: hakem yalnız soruyu görür, hangi maddeden üretildiğini ve retriever'ın onu
bulup bulmadığını **görmez**. Hakem istemi ADR'ye ve `research_log`'a **etiketleme
koşulmadan önce** yazılır. Ölçüt:

> *Soru tek başına okunduğunda, hangi kanun/konu alanına ait olduğu anlaşılıyor mu?
> (Bir hukukçu soruyu görüp 1-2 kanuna daraltabiliyorsa **evet**.)*

**Kaydedilen çekince:** bu sorunu fark eden analiz, kaçırılan soruları **görerek** yapıldı.
Etiketleme hakemi kör olsa da, *"bu ekseni ölçme fikri"* sonuçtan doğdu. Bu, raporda
gizlenmez — ayrım şu: ölçülen **büyüklük** ön-kayıtlı değil, ama **ölçüm aleti** sonuca
göre ayarlanmadı (hakem kör, istem önceden yazılı, küme değişmedi).

---

## K5 — Red kapısı eşiği: **ADR-0038 katı, değişmedi**

**Karar:** [ADR-0038](0038-red-kapisi-esigi-kati.md) yürürlükte — **tek** doğrulanamayan
atıf tüm cevabı reddettirir.

**Ölçülecek:** harness açıkken **aşırı-red** yaratıp yaratmadığı. S3a bunun neden zorunlu
olduğunu sayıyla gösterdi: `recall@10` = 0,875 ise soruların ~%12'sinde model doğru maddeyi
**hiç görmeden** cevap üretmeye çalışacak. Katı kapı bu vakalarda tanımı gereği reddedecek.

⚠️ Bu yüzden harness-AÇIK tablosunda **kütle = coverage × A1** ekseni zorunlu. Adım 0 aynı
gün bunun neden şart olduğunu bir kez daha gösterdi: modül-başına merge iki eksende
kazanıyor görünüp kütlede düştü ve karar $0'a verildi ([ADR-0053](0053-modul-basina-norm-kapsami-reddedildi.md)).

---

## Sonuçlar

- ✅ `sprint3.md`'nin ⛔ kilidi açıldı: Adım 1-4 kodlanabilir.
- ✅ S3a'nın recall sayıları K2 kararıyla **geçerli kalıyor** (tam madde üzerinde ölçüldü).
- ⚠️ K2'nin bedeli (*retriever'ın gördüğü ≠ modelin gördüğü*) harness-AÇIK ölçümünde
  **ayrı bir vaka sınıfı** olarak sayılır, sessizce yutulmaz.
- ⚠️ K4'ün etiketleme turu, harness-AÇIK ölçümünden **önce** koşulur; istemi ve kör'lüğü
  kayda geçer.
