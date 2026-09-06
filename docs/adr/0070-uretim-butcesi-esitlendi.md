# ADR-0070 — Üretim bütçesi rakiple EŞİTLENDİ (tek formül, 1536) · ADR-0043 §2 m.1 değişir

**Tarih:** 2026-09-06 · **Statü:** ✅ yürürlükte · **Karar:** insan
**Değiştirdiği:** [ADR-0043](0043-dusunce-modu-acik-butceli-kapatma.md) §2 adım 1
**Düzelttiği yayımlanmış hüküm:** `outputs/eval/g2-fl-harness/OZET.md` §K2

## Bulgu — ölçüldü, varsayılmadı

ADR-0043 §3: *"bütün özneler, bütün kollar ve bütün **rakipler aynı bütçeyle** koşar.
Sapma hata vermez, sadece **kıyası geçersiz kılar**."* **Bu şart tutmuyordu.**

`gen_eval_grounded.py` iki farklı yol izliyordu:

```
rakip  (reasoning_budget dolu):  max_tokens = reasoning_budget + max_new_tokens = 1536
BİZ    (think_budget dolu):      max_tokens = think_budget                      = 1024
```

ADR-0043 §2'nin protokolü (`1) 1024 izin ver · 2) content BOŞSA zorla kapat · 3) 512 ile devam`)
birebir uygulanmıştı — yani **kod ADR'ye sadıktı**. Ama ayrı 512 payı **yalnız `content` boş
kalan** kalemlere veriliyordu; model `</think>`'i kendi kapatıp cevaba başladığında cevap
**1024'ün kalanına** sığmak zorundaydı.

**Ölçüm (`completion_tokens` tavanı, zorla kapatılmayan kalemler):**

| kol | zorla kapatılmayan | tavan | zorla kapatılan | tavan |
| :--- | ---: | ---: | ---: | ---: |
| BİZ · v2/RRF10/önsözsüz | 75/80 | **1024** | 5 | 1536 |
| BİZ · v1/RRF60/önsözsüz | 76/80 | **1024** | 4 | 1306 |
| BİZ · v1/RRF60/önsözlü (çıpa) | 59/80 | **1024** | 21 | 1291 |
| 3.1 FL | — | **1532** | 1024'ü aşan: **36/80** | — |
| 3.5 FL | — | **1532** | 1024'ü aşan: **18/80** | — |

⇒ **Rakip 1536 toplam bütçeyle koştu, biz yaygın durumda 1024 ile.** Sapma **bizim aleyhimize**.

🚨 **Yayımlanmış bir hüküm çürüdü.** `g2-fl-harness/OZET.md` §K2 şöyle diyordu:
*"rakipte muhakeme cevabın 512'lik payını yiyor; **bizde ADR-0043 gereği ayrık bütçe** +
zorunlu kapanış var."* İkinci yarısı yanlıştı — bizde de düşünce cevabın payını yiyordu,
üstelik daha küçük bir toplamdan. Şerh o dosyada **üstü çizilerek** damgalandı, silinmedi.

## Karar

**Tek formül, iki tarafta da:**

```python
max_tokens = (reasoning_budget or think_budget or 0) + max_new_tokens
```

Bizim kol da artık **1536** alıyor. Zorunlu kapatma mekanizması (`content` boşsa iz + `</think>`
+ `/completions`) **aynen duruyor** — research_log #42'nin sonlanmama bulgusu bu ADR'den
etkilenmiyor, yalnız tetiklendiği nokta 1024'ten 1536'ya kayıyor.

**ADR-0043 §2 adım 1 değişir:** *"Düşünceye 1024 token izin ver"* → *"Toplam üretime
`düşünce + cevap` = 1536 token izin ver."* §2'nin gerekçesi (1024'ün ölçülmüş bir bant olması,
cevap bütçesinin Sprint 1 ile aynı 512 olması) **ayakta**; değişen yalnız ikisinin **ayrı mı
paylaşımlı mı** verildiği. **ADR-0043 §3 (rejim değişmezliği) aynen yürürlükte** — bu ADR onu
ihlal etmiyor, **ihlali onarıyor**.

## Tetikleyen olay

F0.2 koşusu kesiklik kapısında düştü: **5/80 = %6,2 > %5** (ADR-0040). 5 kesikten **4'ü tam
1024'te** ve `forced_close=False` — yani cevap payını hiç almadan. Kesiklik bir **belirtiydi**,
sebep bütçe eşitsizliğiydi. ⭐ Kapı doğru çalıştı: hakem parası harcanmadan durdurdu.

⚠️ Ve neden **şimdi** patladı: önsöz kaldırılınca model `</think>`'i daha sık kendi kapatıyor
(zorla kapatma **21/80 → 5/80**), dolayısıyla ayrı 512 payını alan kalem sayısı düştü ve
paylaşımlı bütçenin bedeli görünür oldu. Yani S14 kararı bu kusuru **yaratmadı, açığa çıkardı**.

## Bedeli

- Bizim üç kolumuzun sayıları **eski rejimde** kalır ve damgalanır.
- ✅ **Rakip kolları yeniden koşulmaz** — onlar zaten 1536'daydı; formül artık onlarınkiyle aynı.
- Bizim kol yeniden koşulur: **~35 dk, $0** (yerel).
- Base gibi sonlanmayan bir model artık 1536 yakıp sonra 512 alır (önce 1024+512) → o kolun
  token maliyeti yükselir; ADR-0017 muhasebesine yazılır.

## Reddedilenler

- **Kabul et ve damgala** (1024'te kal, kesikliği şerh et) — REDDEDİLDİ: ön-kayıtlı %5 kapısı
  çiğnenir **ve** bütçe eşitsizliği ayakta kalır; ADR-0043 §3'e göre kıyas geçersiz olmaya devam eder.
- **Rakipleri 1024'e indir** — REDDEDİLDİ: 3.1 FL'de 36/80, 3.5 FL'de 18/80 kalem 1024'ü aşıyor;
  sınav eşitlenmez, rakip tarafında devasa kesiklik üretilir.

## Doğrulama
`pytest` **112 passed, 2 xfailed** · sözdizimi denetimi geçti · yeniden koşuda kesiklik kapısı
(`≤%5`) ve `completion_tokens` tavanı künyeye yazılacak.
