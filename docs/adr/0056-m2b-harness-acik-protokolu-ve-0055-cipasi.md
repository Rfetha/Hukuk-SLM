# ADR-0056 — `m2b`'nin harness-AÇIK protokolü + ADR-0055'in çıpası düzeltildi

- **Tarih:** 2026-08-05
- **Durum:** kabul edildi
- **Karar veren:** insan (`/grill-with-docs` oturumu)
- **Kaynak ölçüm:** [research_log #55](../record/research_log/2026-08-05-s2-yururluk-alani.md) · [#54](../record/research_log/2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md)
- **Tadil eder:** [ADR-0055](0055-isabet-denetimi-ekseni.md) (ön-kayıtlı kabulün çıpası) · [ADR-0054](0054-harness-tasarim-kararlari-k2-k5.md) K4'ü **tamamlar** (m2b'yi kapsamıyordu)
- **Açar:** Sprint 3 Part 2'nin ölçüm planı — bu ADR'siz `m2b` harness-AÇIK **tanımsız**

## Bağlam

Sprint 3 Part 1 iki gerekçeyle açılmıştı: *"atıf doğrulayıcı A1'i kapatır"* ve *"red kapısı
M2b'yi kapatır"*. Ölçüm sonunda **birincisi çürüdü** (uydurulmuş madde numarası **0/118** —
yakalanacak sınıf boştu), **ikincisi hiç sınanmadı**: `m2b` harness AÇIK **bir kez bile
koşulmadı** ([`sprint3-part1.md`](../../sprint3-part1.md) borç listesi).

Sınamak için önce **tanımlamak** gerekti, çünkü `m2b` harness KAPALI'da bir **kurgu**dur:
aynı 80 `core_hard` sorusu, altın madde **zorla çıkarılmış**, yerine 4 elle-paketlenmiş
hard-negative (`--data core_hard.jsonl --distractors 4 --no-gold`). Harness AÇIK'ta bağlamı
**retriever** seçiyor — *"altın yok"* koşulu artık kurgunun değil, erişimin sonucu.

---

## Karar 1 — `m2b` harness-AÇIK = **altın ablasyonu**, korpus-dışı küme değil

**Aynı 80 soru. Retriever `k+1` getirir; altın madde sonuçtaysa DÜŞÜRÜLÜR; ilk `k` kalır.**

Böylece tek bir değişken oynar: **çeldiricileri kim seçti** — elle paketleyen insan mı,
retriever mı. Bağlam uzunluğu `k=10` ile aynı kalır (Part 1 bağlam uzunluğunun **kendi
başına** sadakate mal olduğunu ölçtü: A1 0,9230 → 0,8426), soru kümesi ADR-0054 K4'ün
**"küme değişmez"** değişmezini korur ve sayı **0,877** çıpasıyla doğrudan kıyaslanabilir.

### ❌ Reddedilen A — korpus-dışı yeni soru kümesi

Cevabı 40.496 maddelik indekste **gerçekten** olmayan sorular üretmek. Ürün gerçeğine en
yakın koşul bu ve değeri yüksek — ama **çıpası yok**: 0,877 ile kıyaslanamaz, dolayısıyla
*"kapı M2b'yi kapattı mı"* sorusunu **cevaplayamaz**. O soru bir **iddia denetimi**dir ve
iddia denetimi aynı çıpa olmadan yapılamaz.

⚠️ Bu ret **kalıcı değil, sıralamadır.** Korpus-dışı prob ayrı bir soruyu (*"kullanıcı
korpusta olmayan bir şey sorunca ne oluyor"*) cevaplıyor ve kendi turunu hak ediyor.
Bu ADR onu **kapsam dışı değil, sonraki** ilan eder.

### ❌ Reddedilen B — mevcut `genelleme/` kümelerini kullanmak

`ood_qa.jsonl` · `trap_ood.jsonl` · `trap_xkanun.jsonl` üçü de **yakın-ıska** tipi:
altın madde korpusta **var**, yalnız yanlış olan veriliyor. Bu **M2**'nin malzemesi.
Retriever koşulduğunda altını **bulabilir** — o anda koşul kendini yok eder.

---

## Karar 2 — İki ayrı sayı raporlanır, **kapının katkısı** ayrı ölçülür

`Rej_model` (kapısız, salt modelin çekinmesi) ve **kapının katkısı**
(`Rej_kapı_sonrası − Rej_model`) **ayrı** yazılır.

**Gerekçe mekanik:** kapı yalnız **doğrulanamayan atıf** varken ateşler. Harness AÇIK'ta
model atıf etiketini bağlamdan **kopyalıyor** → atıf doğrulanıyor → kapı geçiriyor. Yani
tek bir birleşik `Rej` sayısı düşerse *"kapı mı yetersiz, model mi"* **ayrılamaz** — ve bu,
Part 1'in aynen düştüğü hatadır (AÇIK↔KAPALI ayrıştırmasını sonradan yapmak zorunda kaldık).

### ⛔ Ön-kayıtlı tahmin — sayı görülmeden yazıldı

```
A. KAPININ KATKISI ≈ 0        (0-2 / 80)
   gerekçe: uydurulmuş madde no 0/118 → ateşleyecek mekanizma ölçülmüş biçimde yok
   TUTARSA  : Part 1'in M2b iddiası YAPISAL olarak çürük (sınanmamış değil,
              bu rejimde ateşlenemez) → M2b eğitim tarafına geçer
   TUTMAZSA : kapı hakkını veriyor, yürürlükte kalır

B. Rej_model   0,30 - 0,60    (çıpa: harness KAPALI m2b = 0,877)
   gerekçe: Part 1 çapraz tablosunda altın GELMEYEN 10 soruda model yalnız 3'ünde
            çekindi (Rej 0,30). ⚠️ Bu alt küme YANLI — #53'e göre altın gelmeyen
            sorular ağırlıkla "belirsiz" sınıfı ve model orada DAHA AZ çekiniyor.
            Bu yüzden aralık geniş bırakıldı.
   < 0,877  : 🚨 harness M2b eksenini KAPATMIYOR, KÖTÜLEŞTİRİYOR — manşet bulgu,
              olduğu gibi kayda geçer
```

⚠️ **A1 cevaplanan-only raporlanır ve `rescore_answered` ile çapraz doğrulanır** (tuzak
**2.16** — bu hattın bir kapı hükmü zaten bir kez metrik hatasıyla tersine döndü).

---

## Karar 3 — ADR-0055'in ön-kayıtlı çıpası **%59,5 → %61,3**

ADR-0055 B-i deneyinin kabulünü *"kütle ARTAR (bugünkü resmî: k=10 · %59,5)"* diye yazdı.
O sayı **S2-öncesi korpustan**. B-i **S2 korpusunda** koşacak.

**Değişen:** yalnız çıpa sayısı. **Değişmeyen:** eşiğin kendisi (*"kütle ARTAR"*), yön
ölçütü (belirsiz alt kümede çekinme ≥ ayırt edici alt kümede), ve red şıkkı (düşerse B-i
düşer, B-ii'ye geçilir).

**Gerekçe:** %59,5 ile kıyaslamak, önsözün etkisiyle **korpus onarımının** etkisini
toplardı — ve hiçbir yerde hata çıkmazdı. Part 1 tam bu yüzden S1→S2 sırasını **bağlayıcı**
ilan etmişti; aynı tuzağın ikinci yüzü budur.

⚠️ **Bu bir eşik gevşetmesi DEĞİLDİR** ve öyle okunmaması için ayrıca kaydediliyor.
[ADR-0050](0050-verim-kapisi-tahmin-edici-duzeltmesi.md)'nin kuralı *"sonucu gördükten
sonra **eşik değil alet** düzeltilir"*. Burada düzeltilen **ölçü birimi** — hangi korpusta
üretilmiş bir sayıyla kıyaslandığı. Eşik daha **zor** hâle geldi (%59,5 yerine %61,3'ü
geçmek gerekiyor), gevşek değil.

**Ek:** yön ölçütünün S2 korpusundaki güncel değeri **bilinmiyor** (#53 S2-öncesinde
ölçtü). B-i koşmadan önce `outputs/eval/s2-harness-k10-etiketli/` üzerinden **post-hoc**
hesaplanır — bedeli **$0**, yeni üretim yok.

---

## Karar 4 — Doğrulayıcı, ölçüm turu boyunca **dondurulur**

Borç **B8** (katı kapının tek karakterlik yazım hatasına takılması) bir **tolerans
süpürmesi** olarak ölçülür — *"tolerans şu olsaydı kaç doğru atıf kurtulur ↔ kaç yanlış
içeri girer"* — ama **`atif_dogrula.py` değiştirilmez.** Süpürme eldeki `detail.jsonl`
dosyaları üzerinde post-hoc koşar.

**Gerekçe:** doğrulayıcı değişirse kapı kararları değişir, kapı kararları değişirse hem
`m2b` turunun hem B-i turunun sayıları **farklı aletlerle** üretilmiş olur — ve %61,3
çıpası da eski aletle üretildiği için B-i'nin kıyası ayrıca bozulur. Toleransın
**benimsenmesi** ayrı bir karardır ve eğri elde olduktan sonra kendi ADR'sini alır.

## Sonuçlar

- `m2b` harness-AÇIK artık **tanımlı**; Part 1'in sınanmamış yarısı ölçülebilir hâle geldi.
- Ölçüm turunun **hiçbir adımı GPU istemiyor**; tahmini hakem bedeli ~$0,15 *(bütçe ≤ $2)*.
- ⚠️ Karar 1'in kabul ettiği bedel: bu protokol *"kullanıcı korpusta olmayan bir şey
  sorunca ne oluyor"* sorusunu **ölçmez**. Ürün-güvenliği açısından gerçek olan o soru;
  bu tur **iddia denetimi** yapıyor, ürün denetimi değil. Ayrım gizlenmiyor.
- ⚠️ Karar 2'nin B tahmini **yanlı bir alt kümeden** türetildi ve bu, tahminin kendisinde
  yazılı. Tutmazsa *"tahmin kötüydü"* değil **"payda yanlıydı"** diye okunur.
- Bu ADR bir **plan değildir** — Part 2'nin uygulama planı `docs/superpowers/plans/` altına yazılır ve
  sonuçları `docs/record/research_log/`'a düşer.
