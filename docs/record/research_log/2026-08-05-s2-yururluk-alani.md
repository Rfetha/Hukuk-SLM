# #55 — S2: yürürlük alanı + madde kimliği (borç B7) · kapsam **menüden değil ölçümden**

**Tarih:** 2026-08-05 · **Sprint:** [`sprint3.md`](../../../sprint3.md) **S2**
**Betikler:** `scripts/korpus_yururluk.py` (yeni) · `scripts/atif_dogrula.py` (MULGA hükmü)
**Veri:** `data/corpus/mevzuat_maddeler.jsonl` (yazıldı, yedek alındı) ·
**İndeks:** `data/index/mevzuat_bge_m3_s2` (yeni dizin; eskisi korundu)

## 1. Kapsam kararı — yanlış soruyu sormaktan dönüldü

[#52](2026-08-05-korpus-butunlugu.md) korpusun bozuk olduğunu bulmuş ve S2'yi üç işe
büyütmüştü: `mulga` · alt-madde soneki · tablo-parçası eleme. Üçüncüsü indeksi değiştirip
o günkü `recall@k` sayılarını geçersiz kılacaktı, yani ucuz değildi.

Kapsam kararı **doğru soruya çevrilerek** verildi. Yanlış soru: *"korpus ne kadar bozuk?"*
Doğru soru: **"modelin GÖRDÜĞÜ bağlamda çöp var mı?"** — çünkü korpusta duran ama hiç
getirilmeyen bir satırın ürüne maliyeti yoktur. Ölçüm, k=10 koşusunun `context_shown`
alanı ayrıştırılarak **modele giden metnin kendisi** üzerinde yapıldı.

| bozulma sınıfı | korpusta | **modele ulaşan blok** | altın etiketi | karar |
| :--- | ---: | :--- | ---: | :--- |
| **A — tablo/cetvel parçası** | ~7.966 satır | **0 / 800** | — | **ertelendi (B9)** |
| **B — alt-madde soneki** | **485 satır** | **14 / 800 · 12 soru** | 3/80 | ✅ **yapıldı** |

**Sınıf A neden ulaşmıyor:** parçalar çok kısa — `", Ek"` (4 karakter),
`"7/8/2003 5162 4, Ek"` (19). Ne BM25 ne yoğun vektör onları üste çıkarıyor, RRF de
çıkaramıyor. Korpusu şişiriyorlar, **ölçülmüş erişim etkileri sıfır**.

Elemek **ölçülemez bir kazanç için ölçülmüş bir sayıyı harcamak** olurdu — bu repoda
[ROADMAP §5.2](../../../ROADMAP.md)'nin graph-RAG'i ertelerken kullandığı ölçütün aynısı.

### ⚠️ Yinelenme ≠ kirlenme

İlk sayım `(kanun_adi|madde_no)` anahtarı üzerinden yapılınca k=10'da *"26/80 soru bozuk
parça görüyor"* çıktı; `context_shown` üzerinden **6/80** (sonek kuralı düzeltilince 12/80).
Fark şu: **anahtar yinelenmiş olsa bile retriever o anahtarın doğru satırını getiriyordu.**
Biri korpusun özelliği, diğeri bağlamın. **Sayının hangi nesne üzerinde ölçüldüğü, sayının
kendisinden önemli** — aynı korpus için %29,4 ile %1,8 arasında gezinen iki doğru sayı var.

## 2. Yapılan iş

`scripts/korpus_yururluk.py` — **atomik yazma**: geçici dosyaya yaz → doğrula → `os.replace`.
Doğrulama düşerse korpus **değişmez** (POSD rollback gate).

| dönüşüm | satır | not |
| :--- | ---: | :--- |
| `mulga` + `ilga_eden_kanun/madde` + `ilga_tarihi` | **2.547** | ilga kaynağı çıkarılan **%99,6** |
| alt-madde soneki `madde_no`'ya taşındı | **485** | `Madde 31` → `Madde 31/a` |

`scripts/atif_dogrula.py` — **`MULGA`** hükmü. `_hukum` artık anahtar **seti** değil
**indeks sözlüğü** alıyor; maddenin *varlığı* ile *yürürlüğü* tek aramada görülüyor, yeni
parametre açılmadı. `all(mulga)` kullanıldı: bir anahtar birden çok satıra düşebiliyor,
yürürlükte **tek** satır varsa atıf mülga sayılmaz — geçerli atıfları yanlış reddetmemek için.
`red_kapisi.py`'ye **dokunulmadı**: `DOGRULANDI` dışındaki her hükmü zaten kötü sayıyor.

### Kabul ölçütü — geçti

```
1475/15 mulga=True · 1475/14 mulga=False (kıdem tazminatı yürürlükte)   ✅
"İş Kanunu Madde 15" → MULGA · katı/çoğunluk/cerrahi üçünde de REDDEDİLDİ ✅
yanlış-pozitif sıfır — 3 örneklem turu, gözle                            ✅
```

## 3. 🐞 İki kural doğrulama hedefine çarpıp düzeldi

İkisi de **hata vermeden yanlış veri üretecekti** — bu hattın imza failure class'ı.

**(a) Sonek kuralı %80 eksikti.** Yalnız küçük harf aranıyordu (`[a-zçğıöşü]`). Korpusta en
sık sonek **büyük `/A`** — 249 satır. 98 satırlık bir sınıf sanılan şey gerçekte **485**.
Kaçan 387 satır, düzeltme yapılmış gibi görünen bir korpus bırakacaktı.

**(b) İlga kaynağı, tarihin son parçasını kanun sanıyordu.** `"22/5/2003/4857/120 md."`
içinden `2003/4857` okunuyordu, çünkü tarih ile kanun arasındaki ayraç yalnız **tire**
sanılmıştı — oysa **bölü** de olabiliyor. `1475/15`'in ilga kaynağı `4857 md.120` yerine
**`2003 md.4857`** çıkmıştı.

⭐ **Sprint'in kendi verify kalemi ele verdi.** `1475/15`'i hedef olarak yazmak bir tören
değildi; iki kuralı da o hedef düşürdü. Ön-kayıtlı doğrulama hedefinin değeri tam olarak bu.

## 4. ⚠️ Dürüst negatif sonuç — B7 bir skor özelliği değil

Mevcut k=5 ve k=10 koşuları yeni korpusa karşı **yeniden puanlandı**:

```
              k=5              k=10
MULGA          0                0
hükmü DEĞİŞEN cevap  0/80       0/80
```

Yani açık **mekanik olarak** kapandı ama bu DEV kümesinde **ölçülen görülme sıklığı sıfır**.
B7 bir **ürün-güvenliği** özelliğidir, bir metrik iyileştirmesi değil — öyle raporlanıyor.
Bunun kaydedilmesi şart: aksi hâlde ileride *"S2 hiçbir şeye yaramadı"* diye okunur, oysa
ölçülen şey *"bu kümede tetiklenmedi"*dir. Mülga atıf riski soru dağılımına bağlıdır ve
`core_hard` yürürlükteki maddeler üzerinden üretilmiştir — sıfır çıkması **beklenebilirdi**.

## 5. Eval etiketleri düzeltilmedi — çünkü gerek kalmadı

Onarım öncesi altın anahtar `2004/Madde 31`'i **`31/a` satırı da** karşılayabiliyordu; artık
ikisi ayrı kayıt. Havuz iki eval kümesinde de korunuyor: `dev` **80/80**, `canon` **40/40**.
Yani soru kümesi değişmedi, **yer doğruluğu sıkılaştı** — bir kalem artık yanlış satırla
"bulundu" sayılamıyor. ADR-0054/K4'ün *"küme değişmez"* kuralı ihlal edilmedi.

## 6. İndeks — yeni dizine kuruldu

`madde_no`, gömülen metnin parçası (`kanun_adi + madde_no + text`), o yüzden 485 satırın
gömmesi değişti ve bayat-indeks kapısı **tasarlandığı gibi patladı**
(`37903062 → 38751499 bayt`). İndeks **`data/index/mevzuat_bge_m3_s2`**'ye kuruldu;
eskisi **silinmedi** — S2 öncesi sayıların yeniden üretilebilmesi için. Harness AÇIK k=10
yeni indeksle **yeniden koşuluyor**.

## Paper eşlemesi

**Methodology:** kapsam kararının *"veri ne kadar bozuk"* değil *"bozukluk modele ulaşıyor
mu"* diye ölçülmesi; aynı korpus için %29,4 (anahtar yinelenmesi) ve %1,8 (bağlam kirlenmesi)
sayılarının ikisinin de doğru ama farklı nesneleri ölçmesi. **Limitations / Data:** yürürlük
bilgisi korpusta yoktu; atıf doğrulayıcı *var mı* sorusunu yanıtlıyor, *geçerli mi* sorusunu
yanıtlamıyordu. **Negatif bulgu:** ürün-güvenliği düzeltmesinin mevcut değerlendirme
kümesinde ölçülen etkisi **sıfır** — güvenlik özellikleri skor üzerinden savunulamaz.
