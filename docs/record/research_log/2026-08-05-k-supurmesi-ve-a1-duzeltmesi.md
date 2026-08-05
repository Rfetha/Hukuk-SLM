# #54 — S1: `k` süpürmesi (k=10) · 🚨 ve yayınlanmış kütle sayısı YANLIŞ metrikle üretilmiş

**Tarih:** 2026-08-05 · **Sprint:** [`sprint3.md`](../../../sprint3.md) **S1** (borç B3)
**Özne:** `tgta_v1` = `HakHukuk-4B-v0.1` — k=5 koşusuyla **aynı artefakt, aynı 80 soru**
**Bedel:** GPU **$0** (yerel, şarjda) · hakem **$0,0403** · **Çıktı:** `outputs/eval/s3-harness-k10/`

> İki bulgu var ve ikincisi birinciden büyük. **(1)** k=10 kütleyi yükseltiyor, kabul ölçütü
> geçildi. **(2)** Bunu ölçerken `harness_tablo.py`'nin **A1'i yanlış hesapladığı** görüldü —
> ve o hatalı sayı `MODEL_CARD.md` dâhil **sekiz belgeye** yayılmış durumda.

---

## 🚨 BÖLÜM 1 — Metrik hatası: `A1` yerine ham makro (tuzak 2.3'ün birebir tekrarı)

### Ne oldu

`scripts/harness_tablo.py` `A1_tum` diye raporladığı sayıyı **puanlanan tüm kalemlerin**
makrosu olarak hesaplıyordu. Oysa ADR-0011 ve tuzak 2.3 gereği **A1 = cevaplanan-only**.
Fark, çekinmelerin de hakemden puan almasından geliyor: model çekinirken de cümle kuruyor,
hakem o cümlelere iddia diyor ve puanlıyor.

```
k=5 : puanlanan 71 → TÜMÜ 0,7823 · cevaplanan(A1) 0,7591 · ÇEKİNENLER 0,9091 (n=11)
k=10: puanlanan 74 → TÜMÜ 0,7541 · cevaplanan(A1) 0,7681 · ÇEKİNENLER 0,6819 (n=12)
```

### ⚠️ Sapma **yön değiştiriyor** — bu, gürültünün en kötü türü

k=5'te çekinmeler **0,9091** alıp makroyu **yukarı**, k=10'da **0,6819** alıp **aşağı** çekti.
Yani hata sabit bir kayma değil; iki koşuyu **birbirine göre** bozuyor. Sonuç:

| | bozuk aletle | düzeltilmiş aletle |
| :--- | ---: | ---: |
| k=5 kütle | %58,7 | **%56,9** |
| k=10 kütle | %58,4 | **%59,5** |
| **hüküm** | k=10 **DÜŞÜK** → 🔴 RET | k=10 **YÜKSEK** → ✅ KABUL |

**Ön-kayıtlı kapının hükmü, aletin düzeltilmesiyle tersine döndü.** Bu tam olarak
[ADR-0050](../../adr/0050-verim-kapisi-tahmin-edici-duzeltmesi.md)'nin durumu ve kuralı
aynen uygulandı: **sonucu gördükten sonra EŞİK değil ALET düzeltilir.** Ön-kayıtlı olan
*büyüklük* (*"k=10'un kütlesi k=5'inkini geçmeli"*), onu kestiren tahmin edici değil.
Düzeltme **iki kola da simetrik** uygulandı ve eşik aynı koşudan yeniden türetildi
(%58,7 → %56,9); eşik gevşetilmedi, **yeniden ölçüldü**.

### ⚠️ Daha kötüsü: ON/OFF kıyası elmayla armuttu

Harness **KAPALI** çıpası (`outputs/eval/cp3-supurme-ham/a1_m1_tg_ta_ham_th.txt`) **doğru**
metrikle üretilmiş: `A1_faithfulness_macro_answered` = **0,9087**, kütle 63/80 × 0,9087 =
**%71,6** ✅. Yani `%71,6 ↔ %58,7` karşılaştırmasının **bir tarafı cevaplanan-only, diğer
tarafı ham makroydu.**

### Düzeltilmiş resmî sayılar

| eksen | harness KAPALI (m1) | harness AÇIK k=5 | harness AÇIK k=10 |
| :--- | ---: | ---: | ---: |
| coverage | 63/80 = 0,7875 | 60/80 = 0,7500 | 62/80 = **0,7750** |
| **A1 (cevaplanan-only)** | **0,9087** | ~~0,7823~~ → **0,7591** | **0,7681** |
| **kütle = coverage × A1** | **%71,6** | ~~%58,7~~ → **%56,9** | **%59,5** |
| A1 · altın getirilen | 0,9087 | ~~0,9344~~ → **0,9230** | **0,8426** |

**#51'in ⭐ manşet bulgusu AYAKTA ama sayısı değişti:** *"retriever altını bulduğunda model
daha sadık"* — **0,9230 > 0,9087**, marj +2,6 puandan **+1,4 puana** indi. ⚠️ Ve bu bulgu
**k'ya bağlı:** k=10'da **0,8426 < 0,9087**, yani **tersine dönüyor** (bkz. Bölüm 2).

### Düzeltilen belgeler

`sprint3.md` · `MODEL_CARD.md` · `CLAUDE.md` · `ROADMAP.md` · `TODO.md` ·
[`kollar.md`](../kollar.md) · [research_log #51](2026-08-04-harness-acik-ilk-olcum.md) ·
[#53](2026-08-05-ayirt-edicilik-etiketi.md). Eski sayı **silinmedi**, üstü çizilip yanına
doğrusu yazıldı (çelişki iki yerde birden işaretlenir kuralı).

### Alet düzeltmesi

`harness_tablo.py` artık `A1_cevaplanan` (gerçek A1) **ve** `faith_macro_tum_cekinme_dahil`
(eski sayı, doğru adıyla) alanlarını ayrı yazıyor; `kutle_tum` **A1'den** türetiliyor.
Alt küme kırılımları da aynı tanımı kullanıyor. → **tuzak 2.16**.

---

## BÖLÜM 2 — S1'in asıl sonucu: k=10 kabul edildi, ama tahmin ıskaladı

### Ön-kayıtlı tahmin ↔ ölçüm

`sprint3.md`'de sayı görülmeden yazılan tahmin ve gerçekleşen:

| büyüklük | tahmin (k=10) | **ölçüldü** | hüküm |
| :--- | ---: | ---: | :--- |
| altın getirilen | ~70/80 | **70/80** | ✅ **birebir tuttu** |
| coverage | ~0,76 | **0,775** | ✅ tuttu |
| A1 | ~0,86 | **0,7681** | ❌ **9 puan ıskaladı** |
| **kütle** | ~%65 | **%59,5** | ❌ **5,5 puan ıskaladı** |

**Erişim tahmini kusursuz, davranış tahmini yanlıştı.** Tahmin, *"altın getirilenlerde A1
0,934 kalır"* varsayımına dayanıyordu. Ölçüldü: **kalmadı, 0,8426'ya düştü.**

### ⭐ k'nın bedeli ölçüldü: dikkat dağılması gerçek

```
                              k=5      k=10
altın getirilen             60/80    70/80   (+10)
altın getirilende A1        0,9230   0,8426  (−8,0 puan)   ← k'nın BEDELİ
coverage                    0,750    0,775   (+2,5 puan)
A1 (cevaplanan-only)        0,7591   0,7681  (+0,9 puan)
KÜTLE                       %56,9    %59,5   (+2,6 puan)   ← net kazanç
```

`sprint3.md`'nin ret şıkkı *"kütle düşerse sebebi (bağlam uzunluğu mu, dikkat dağılması mı)
gözle okunur"* diyordu. Kütle **düşmedi**, ama dikkat dağılması **yine de ölçüldü**: aynı
soruda altın madde bağlamda dururken, yanına 5 madde daha konunca sadakat **8 puan**
düşüyor. Net kazanç, erişimin kazandırdığı 10 sorunun bu kaybı **aşmasından** geliyor.

### Erişim ↔ davranış çaprazı — B1'in sınıfı yarıya indi

```
                              k=5    k=10
altın geldi   → cevapladı      46      55
altın geldi   → çekindi        14      15    ← aşırı-red DEĞİŞMEDİ
altın GELMEDİ → cevapladı      14       7    ← B1'in sınıfı YARIYA indi
altın GELMEDİ → çekindi         6       3
```

**B1 (*"gerçek ama soruya uymayan madde"*) k ile küçülüyor: 14 → 7.** Ama **aşırı-red
küçülmüyor** (14 → 15): altın madde bağlamda olmasına rağmen çekinilen soru sayısı k'dan
**bağımsız**. Yani coverage kaybının bu yarısı erişimle çözülmüyor — model tarafında.

### Ayırt-edicilik kırılımı ([#53](2026-08-05-ayirt-edicilik-etiketi.md)'ün etiketiyle)

| alt küme | n | `recall@5` | `recall@10` | A1 k=5 → k=10 | kütle k=5 → k=10 |
| :--- | ---: | ---: | ---: | ---: | ---: |
| ayırt edici | 62 | 0,8226 | **0,9355** | 0,8651 → 0,7997 | %60,0 → **%62,1** |
| belirsiz | 18 | 0,5000 | **0,6667** | 0,4909 → 0,6493 | %46,4 → **%46,9** |

k'nın kazancı **ayırt edici** tarafta toplanıyor (+2,1 puan kütle); belirsiz tarafta
neredeyse **yok** (+0,5). Erişim orada da yükseliyor (0,50 → 0,67) ama kütleye dönüşmüyor.
→ *k büyütmek, belirsiz soru sorununu çözmüyor.*

### ⭐⭐ Ama k=10 **çekinme kalibrasyonunun yönünü düzeltiyor**

[#53](2026-08-05-ayirt-edicilik-etiketi.md) k=5'te *"model, erişimin en çok battığı yerde en
az çekiniyor"* diye ters bir kalibrasyon ölçmüştü. k=10'da:

| coverage | k=5 | k=10 |
| :--- | ---: | ---: |
| ayırt edici (n=62) | 0,6935 | **0,7903** |
| belirsiz (n=18) | **0,9444** | **0,7222** |
| sıralama | ❌ ters (belirsizde **+25,1** puan fazla cevaplıyor) | ✅ doğru (ayırt edicide **+6,8** puan) |

Belirsiz alt kümede çekinme **1/18 → 5/18**. On parça bağlamda hiçbiri soruyu karşılamayınca
model bunu **fark edebiliyor**; beş parçada fark edemiyordu. Bu, k=10'un kütle dışındaki en
değerli kazancı ve **ürün güvenliği** ekseninde doğrudan bir iyileşme.

### Geçerlilik ve kıyaslanabilirlik kapıları

```
✅ kesik 2/80 (%2,5 < %5)           · düşünen 80/80 · zorla kapatılan 4/80 (k=5'te 15/80)
✅ örneklem BİREBİR aynı 80 soru    (tuzak 1.5 — soru/kanun_no/madde_no üçlüsü tek tek eşleşti)
✅ CTX sığıyor: en uzun istem 3.582 tok + 1024 düşünce + 512 cevap = 5.118 < 8.192
   bağlam ort. 3.664 → 7.100 karakter
✅ hakem k=5 ile birebir: gpt-4o-mini · OpenRouter · LLM_PROVIDER_ORDER=OpenAI (tek eleman)
```

⭐ **Yan gözlem:** bağlam iki katına çıkarken **zorla kapatma 15/80 → 4/80'e düştü** ve
ortalama token 731'e indi. Daha çok bağlam, modeli daha az **düşündürüyor** — #42'nin
*"belirsizlik döngü üretiyor"* mekanizmasıyla tutarlı.

---

## BÖLÜM 3 — Atıf doğrulayıcısı ilk kez bir şey yakaladı: ve o bir **yazım hatası**

k=10'da atıf dağılımı `DOGRULANDI 118 · KANUN_YOK 2 · MADDE_YOK 0 · AYRIŞTIRILAMADI 0`.
İki `KANUN_YOK` **gözle okundu** (ADR-0038'in şartı — katı kapıda her yanlış negatif
doğrudan coverage kaybı):

```
soru id=29 "Cayma hakkı nedir?"
bağlamda  : FİKİR VE SANAT ESERLERİ KANUNU Madde 57 ve 58   (sıra 5 ve 9)
model yazdı: "Fikir ve Sanat ESELERİ Kanunu Madde 57 / 58"   ← bir harf düştü ('r')
hüküm     : KANUN_YOK → katı kapı REDDETTİ
```

**Uydurma değil, kopyalama hatası.** Madde numaraları (57, 58) **doğru**, kanun bağlamda
**var**. Yani:

1. **#51'in *"uydurulmuş madde numarası 0"* bulgusu k=10'da da AYAKTA** — 0/120 atıfta
   uydurulmuş numara yok. Model hâlâ etiketi kopyalıyor.
2. **Yeni bir yanlış-negatif sınıfı:** *tek karakterlik transkripsiyon hatası.* ADR-0038'in
   kalibrasyonu resmî adın **kısa hâlini** (sonek eşleşmesi) çözmüştü; **yazım hatasını**
   çözmüyor. Katı kapıda bunun bedeli **tüm cevabın reddi**.
3. Ayrıştırıcı ayrıca adın **başını da düşürüyor** (`Fikir ve` atılıp `Sanat Eseleri Kanunu`
   olarak ayrıştırıldı) — #51'de bulunan *"ada kaçan önceki sözcük"* hatasının **ters yönü**.

⚠️ **Karar verilmedi, borç olarak açılıyor (B8).** Yazım hatasına tolerans (ör. normalleştirilmiş
düzenleme uzaklığı) katı kapıyı **gevşetir**; gevşetme kararı ölçülmeden verilmez — yanlış
pozitif üretirse ürün vaadini (*"denetlenebilir"*) doğrudan zedeler.

---

## Hüküm

- ✅ **S1 KABUL: `k=10` yürürlüğe giriyor.** Kütle **%56,9 → %59,5** (+2,6 puan), kabul
  ölçütü (k=5'i geçmek) **düzeltilmiş aletle** karşılandı.
- ⚠️ Kazanç, ön-kayıtlı tahminin (**~%65**) **altında**; sebep ölçüldü: **dikkat dağılması**
  altın getirilende A1'i 8 puan düşürüyor. `k=20` denemek için gerekçe **zayıf** —
  `recall@20` yalnız +5 puan (0,925) getirirken bağlam iki katına daha çıkar ve bu bedel
  ölçülmüş biçimde büyür.
- 🚨 **Yayınlanmış kütle sayısı düzeltildi**: `%58,7` → **`%56,9`** (k=5). Ürünün bugünkü
  resmî sayısı artık **k=10 · %59,5**.

## Paper eşlemesi

**Results:** `k` süpürmesi ve erişim ↔ dikkat dağılması takası (aynı soruda altın bağlamdayken
k 5→10 sadakati 8 puan düşürüyor). **Methodology / Limitations:** ⭐ ön-kayıtlı bir kapının
hükmünün **tahmin edicinin hatasıyla** tersine dönebilmesi ve düzeltmenin ADR-0050 kuralıyla
(eşik değil alet) yapılması. **Negatif bulgu:** deterministik atıf doğrulayıcısının ilk
yakaladığı şey bir fabrikasyon değil **transkripsiyon hatası**; katı kapı doğru bir cevabı
tek karakter yüzünden reddediyor.
