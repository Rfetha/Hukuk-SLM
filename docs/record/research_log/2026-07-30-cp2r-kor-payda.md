# #46 — CP2-r: cevaba kör payda · üç eşik türetildi · **düzeltme 6 karşılaştırmanın 4'ünde aleyhimize**

**Tarih:** 2026-07-30 · **Checkpoint:** `sprint2.md` CP2-r · **GPU:** yok · **Maliyet:** $0,2298
**Karar belgeleri:** [ADR-0048](../../adr/0048-cevaba-kor-tuzak-gecerliligi.md) ·
[ADR-0049](../../adr/0049-sprint2-kalan-kararlarin-kilitlenmesi.md) m.1/m.2/m.3 ·
[ADR-0045](../../adr/0045-ara-kapi-merge-onarim-kontrolu.md) (eşik formülleri)
**Çıktı:** `outputs/eval/cp2-r-kor-payda/` (+ `KUNYE.json`)
**Betikler:** `valid_trap_cache.py` · `rescore_abstention_cached.py` · `cp2r_esikler.py`
**Girdi:** CP0.9'un mevcut dosyaları — **hiçbir hedef model çağrılmadı**

---

> 🚨 **DAMGA 2026-08-06 (kusur K-3) — bu girişin kör payda sayıları EMEKLİ BİR ALETİN
> sayılarıdır. SİLİNMEDİ, ama artık yürürlükte değil.**
>
> Bu tur `valid_trap_cache.py` + `rescore_abstention_cached.py` ile ölçüldü; ikisi de
> `score_abstention.py`'den **ayrı** bir kör payda üretiyordu ve klipleri farklıydı. Aynı
> cp09 koşularında iki alet **çelişen** sayı veriyor (hepsi hakem gürültü tabanının 4-7 katı):
>
> | cp09 m2b Rej | cevaba bağlı | **bu giriş** (klip 900) | yürürlükteki alet (klip 3500) | fark |
> | :--- | ---: | ---: | ---: | ---: |
> | base | 0,986 | **0,949** | **0,961** | 1,2 p |
> | Gemini | 1,000 | **0,861** | **0,883** | 2,2 p |
> | `τ_g` | 0,607 | **0,519** | **0,506** | 1,3 p |
>
> **Sebep ölçüldü — 900 bir KATEGORİ HATASIYDI.** ADR-0011'in 900'ü `gen_eval_grounded`'ın
> **her `[KAYNAK]` parçasına AYRI** uyguladığı üretim-zamanı eval-ayna klipi;
> `context_shown` zaten kırpılmış parçaların BİRLEŞİMİ. Bu tur o parça sabitini birleşime
> uyguladı. cp09 m2b'de (n=80, `[KAYNAK` sayımı): tam metinde **320** kaynak · klip 900 ile
> hakem **147**'sini görüyor (**%46**) · klip 3500 ile **320**'sini (**%100**). Yani bu
> girişin kör paydası bağlamın **yarısından** karar vermiş.
>
> **Ayakta kalanlar:** (a) paydanın cevaba KÖR olması gerektiği hükmü — ADR-0048 yürürlükte;
> (b) M3'ün **80/80** tanımı — 2026-08-06'da alete alındı (KARAR-2) ve altı koşuya uygulandı;
> (c) m2b kurgu tabanının geçildiği (79/80 ↔ yürürlükteki alet 77/80, ikisi de ≫ 40).
> **Yürürlükteki sayılar:** `outputs/eval/cp09-butceli-1024-512/abst_*_summary.json` ·
> [#57](2026-08-06-cekinme-aleti-onarimi.md) · [#58](2026-08-06-payda-tekillesmesi.md).
>
> ⛔ Bu girişteki **eşikler de emekli**: ARA KAPI 2. gözlemi 2026-08-06'da yeniden türetildi
> ve **hükmü değişti** — bkz. #58 ve [ADR-0045](../../adr/0045-ara-kapi-merge-onarim-kontrolu.md).

---

## Yapılan

#45 `valid_trap`'in özne başına yeniden yargılandığını göstermişti. ADR-0048 düzeltmeyi karara
bağladı: geçerlilik **cevaba kör**, **kalem düzeyinde**, **bir kez**. Bu tur onu uyguladı.

**Ön koşul doğrulandı:** eval bağlamı üç modda da özneler arası **bit-birebir aynı**
(m2 70/70 · m2b 80/80 · m3 80/80, sıfır fark) → önbelleğin `id` anahtarlı olması meşru.
Betik bunu her koşuda yeniden doğrular ve ayrışmada **durur**.

**Maliyet neden bu kadar düşük:** `verdict` (ABSTAIN/FABRICATE) yeniden hesaplanmadı — o **cevap
hakkındadır**, cevaba bağlılığı meşrudur. Ve `score_abstention.py` onu `valid_trap`ten bağımsız
kaydediyor, geçersiz sayılan kalemlerde de dolu (doğrulandı 11/11). Yani düzeltme = önbellek
($0,23) + **saf aritmetik ($0)**. M3 hakeme hiç gitmedi (ADR-0048 m.2).

## 1) Payda her modda yukarı çıktı

| mod | eski (özne başına) | **yeni (cevaba kör)** | oran |
| :--- | :--- | --: | --: |
| m2 | 55 / 57 / 59 | **66/70** | 0,943 |
| m2b | 61 / 65 / 72 | **79/80** | 0,988 |
| m3 | 39 / 54 / 56 | **80/80** | 1,000 *(tanım, hakem yok)* |

Kirli hakem geçerli tuzakları **sistematik olarak** geçersiz sayıyordu. M3'te 39-56 → 80 tanımsal
hatanın düzelmesi.

## 2) ⭐ M2b kurgu tabanı **fena hâlde geçildi** — ve bir bulgu çürüdü

Ön-kayıtlı taban **40/80** (ADR-0049 m.3), ölçülen **79/80** → merge onarım kontrolü ARA KAPI'nın
2. gözlemi olarak **kalır**.

Bu, CP2 pilotundaki *"m2b'de 25 adayın 24'ü geçersiz tuzak"* bulgusunu **çürütüyor**: o da kirli
hakem artefaktıydı. M2b kurgusu (distractor'lar aynı kanundan → komşu madde soruyu cevaplıyor
olabilir) endişesi **ölçümle desteklenmedi**.

⚠️ **Şerh:** pilot **havuz** kalemlerinde (`abstain_trap_v3`), bu ölçüm **DEV** kalemlerinde —
aynı kurgu, farklı küme. Kurgu sağlam çıktı; havuz tarafı CP2-c'de aynı kör damgayla ayrıca ölçülecek.

## 3) Üç eşik türetildi — hareket tahminden **çok küçük**

Ön-kayıtlı olan **formül**, sayı değil (ADR-0049 m.1):

| eşik | eski | **yeni** | formül |
| :--- | --: | --: | :--- |
| 1) `τ_a` tekil M2 Rej ≥ | 0.934 | **0.923** | base 0.803 + 0.12 |
| 2) merge M2b ≥ | 0.887 | **0.8541** | base 0.949 × 0.90 |
| muhafız M1 A1 ≥ | 0.888 | **0.8799** | base A1 0.9777 × 0.90 |

Tahmin ~0.91'di; gerçek **0.923** — yalnız **1,1 puan** kolaylaşma.

**Ve daha önce açık bırakılan bir soru kapandı:** *"muhafız 0.888 mi 0.880 mi?"* (#44, CP1'in yeni
hakemi base A1'i 0.986 → 0.9777'ye taşımıştı). Cevap **0.880**. Bu kayma `valid_trap`'ten
**bağımsız** — groundedness ekseni, CP1'in istem değişikliğinden geliyor.

## 4) ⭐⭐ Düzeltme **tek yönlü değil** — 6 karşılaştırmanın 4'ü aleyhimize

ADR-0049 m.1, eşik hareketinin lehimize olduğunu kabul edip üç maddeli savunma yazmıştı. Ölçüm o
savunmanın **en güçlü kanıtını** getirdi: düzeltme bizi kayırmıyor, **ölçümü düzeltiyor.**

| karşılaştırma | eski açık | yeni açık | kayma | kim lehine |
| :--- | --: | --: | --: | :--- |
| m3 base − `τ_g` | 0,077 | **0,200** | **+0,123** | 🔴 aleyhimize |
| m3 Gemini − `τ_g` | 0,077 | **0,200** | **+0,123** | 🔴 aleyhimize |
| m2b base − `τ_g` | 0,379 | **0,430** | **+0,051** | 🔴 aleyhimize |
| m2 base − `τ_g` | −0,059 | −0,030 | **+0,029** | 🔴 aleyhimize |
| m2b Gemini − `τ_g` | 0,393 | 0,342 | −0,051 | 🟢 lehimize |
| m2 Gemini − `τ_g` | 0,057 | 0,015 | −0,042 | 🟢 lehimize |

**En çok kayan özne RAKİP:** Gemini M2 **−0,082**, M2b **−0,139**. Kirli paydadan en çok o
yararlanıyordu (M2b'de 1.000 raporlanmıştı, gerçek **0,861**).

### Özne bazında kaymalar (RED)

| mod | base | Gemini | `τ_g` v1 |
| :--- | :--- | :--- | :--- |
| m2 | 0,814 → **0,803** (−0,011) | 0,930 → **0,848** (−0,082) | 0,873 → **0,833** (−0,040) |
| m2b | 0,986 → **0,949** (−0,037) | 1,000 → **0,861** (−0,139) | 0,607 → **0,519** (−0,088) |
| m3 | 1,000 → 1,000 | 1,000 → 1,000 | 0,923 → **0,800** (−0,123) |

> 🚨 **DAMGA 2026-08-06 (Ö3) — bu tablonun SAĞ tarafı da artık EMEKLİ.** Buradaki *"yeni"*
> değerler **klip 900** aletinden geliyordu ve o alet K-3'te bir **kategori hatası** olarak
> çürüdü (parça sabiti birleşik bağlama uygulanmıştı). Yürürlükteki üçüncü sütun
> ([#57](2026-08-06-cekinme-aleti-onarimi.md) · [#59](2026-08-06-m2-paydasi-ve-karar-4.md)):
> ```
>      base            Gemini          τ_g v1        payda
> m2   0,803 (aynı)    0,848 (aynı)    0,833 (aynı)   66   ᴷ⁴ — iki alet aynı hükümde birleşti
> m2b  0,949 → 0,961   0,861 → 0,883   0,519 → 0,506  77   ᴷ³
> ```
> ⭐ `m2`'de iki alet **aynı paydayı** verdi (66/70) — 900 klipinin zararı yalnız
> **birleştirilmiş çok-kaynaklı** bağlamda (`m2b`, `h2b`) doğuyor. Eski sayılar silinmedi.

## 5) `τ_g` hakkında yeni gerçek: açık **raporlanandan büyük**

- **M2b 0,607 → 0,519** · base'e açık **0,379 → 0,430**. `τ_a`'nın hedefi daha da acil.
- **M3 0,923 → 0,800** — #43'teki 0,923 fazla iyimserdi (çelişki #43 ve #45'te işaretli).
- M2'de base'i geçme durumu **korundu** ama daralttı (0,873 → 0,833 vs base 0,803).

## Ders

**Bir ölçüm hatası düzeltildiğinde yönünü önceden bilmek mümkün değil — ve tam bu yüzden düzeltme
sonucu görmeden yapılmalı.** Burada eşik lehimize 1,1 puan kaydı ama `τ_g`'nin karşılaştırmalı
açıkları dört yerde büyüdü; net etki **aleyhimize.** Aynı düzeltme sonuç görüldükten sonra
yapılsaydı hangi yöne çekildiği asla ayrıştırılamazdı.

İkinci ders: **kirli bir payda en çok, o paydada en iyi görünen özneyi kayırır.** Gemini M2b'de
1.000 raporlamıştı; kör paydada 0,861. Rakip lehine sapma, kendi lehimize sapmadan **daha
tehlikeliydi** çünkü parite iddiasını sessizce zorlaştırıyordu.

## Paper eşlemesi

- **Methodology / judge design:** cevaba-kör, kalem düzeyinde, önbelleklenmiş filtre etiketi;
  mod tanımından çıkan etiket hakeme sorulmaz.
- **Limitations:** paydanın hakemi (`gpt-4o`) skorlama hakeminden (`gpt-4o-mini`) farklı —
  bilinçli, kayda geçti, önbellek commit edildi.
- **Negatif bulgu:** M2b kurgu endişesi **desteklenmedi** (79/80); pilotun "24/25 geçersiz"
  bulgusu kirli hakem artefaktı.
- **Sonuçlar (dürüstlük kanıtı):** ön-kayıtlı eşiği düzeltilmiş çıpadan yeniden türetmek, net
  etkisi **aleyhimize** olan bir işlemdi — ve sonuç görülmeden yapıldı.

## Etkilenmeyen / bilinçli dokunulmayan

`sprint1-thinking-off/` ve `cp09-ab-ayrimi/` **düzeltilmedi** — thinking-off canlı rejim değil
(ADR-0043 m.4), tarihsel kayıt olarak kalıyor. `outputs/eval/cp09-butceli-1024-512/`'nin eski
özetleri **yerinde duruyor**; düzeltilmiş sayılar `cp2-r-kor-payda/`'da **yanına** yazıldı.
