# Kusur 21 — atıf-çözüm onarımı ürün yüzeyine taşındı

**Tarih:** 2026-09-11 · **İnsan kararı:** *"Onarımı ürün yüzeyine de taşı."*
**DURUM: ONARILDI.** Ayrışma ölçüldü, **gerçekti**, kapatıldı; ölçüm hattının davranışı
**değişmedi** ve bu 94 dosya · 11.634 hüküm üzerinde sha256 ile kanıtlandı.

---

## 1. Ayrışma NEREDE ve NASIL

| | ürün yüzeyi `hakhukuk/araclar.py` (önce) | ölçüm hattı `scripts/erisim_korpus/atif_dogrula.py` |
| :--- | :--- | :--- |
| indeks | `self._adlar`: `_ad_normal(ad)` → `{(no, ad)}` | `KanunDizini`: `sonek` · `tam` · `adi` |
| sondaki parantez | **atılmaz** | `_ad_varyantlari` ile atılır (`… (G.V.K.)`) |
| sonek eşleşmesi | **yok** — yalnız birebir ad | `≥2` sözcüklü sonek (`_ad_adaylari` 1. gevşeme) |
| baştan sözcük atma | **yok** | var, ama kalan **BİREBİR** ad olmalı (2. gevşeme) |
| çözülemeyen ad | `()` | `AYRISTIRILAMADI` (sessizce kanun SEÇMEZ) |

Yani ürün yüzeyi kusur 18'in **onarımını değil, onarımdan da katı bir eski hâli** taşıyordu:
yanlış kanuna basmıyordu ama parantezli ve kısaltılmış adları **hiç çözemiyordu**.

## 2. Ayrışma ÖLÇÜMÜ (onarım öncesi)

Aynı girdi kümesinde iki çözümün döndürdüğü `kanun_no` kümeleri karşılaştırıldı.
Alet: `scratchpad/ayrisma_olc.py` (gerçek korpus, 40.496 satır / 892 kanun).

| girdi kümesi | n | **FARKLI** | oran |
| :--- | ---: | ---: | ---: |
| korpusun **892 kanun adı** (tam hâliyle) | 892 | **19** | %2,1 |
| **parantezli adlı 16 kanun**, parantezsiz yazımla | 16 | **7** | **%43,8** |
| çıpa koşusunun gerçek atıfları (`f02-biz-onsozsuz`) | 114 | **24** | **%21,1** |

Örnekler (ürün ↔ ölçüm):

```
'Gelir Vergisi Kanunu'   ürün []            ↔ ölçüm ['193']
'İflas Kanunu'           ürün []            ↔ ölçüm ['2004']
'Sanat Eserleri Kanunu'  ürün []            ↔ ölçüm ['5846']
'İş Kanunu'              ürün ['1475','4857'] ↔ ölçüm ['1475','4857','854']
```

⚠️ Bu bir **BULGU**dur: ayrışma çıpanın gerçek atıflarının **beşte birinde** vardı.
Vatandaşa giden `kanun_bul` kaldıracı, *"Gelir Vergisi Kanunu"* için modele **"böyle bir
kanun yok"** diyordu — yayımlanan sayıyı üreten alet ise **193**'ü buluyordu.

**Onarım sonrası aynı ölçüm: 0/892 · 0/16 · 0/114.**

## 3. Seçilen seçenek: **(a)** — `araclar.py` onarılmış mantığı `scripts/`'ten import eder

```python
from atif_dogrula import _ad_adaylari, _dizin_kur  # noqa: E402
```

**Gerekçe (üçü de ölçülebilir, tercih değil):**

1. **(b) bir DÖNGÜ kurardı.** `hakhukuk/araclar.py` **zaten** `scripts/erisim_korpus`'tan
   `madde_anahtari` alıyor. Ad çözümü `hakhukuk/`'a taşınsaydı `atif_dogrula` da
   `hakhukuk`'u import edecekti ⇒ paket düzeyinde **iki yönlü** bağımlılık. Kusur 11'i
   kapatmaz, **düğümler**.
2. **(a) ölçüm hattına HİÇ dokunmaz.** Görevin ⛔ şartı *"ölçüm hattının davranışı
   değişmeyecek"*; dosya **byte-identical** kalınca bu şart ihlal edilemez hâle gelir.
   (b) ise ölçüm hattının bir dosyasını değiştirip kanıt yükünü üstlenirdi.
3. **Marjinal borç ≈ 0.** `araclar.py`'de yol köprüsü ve `scripts/erisim_korpus` importu
   **zaten vardı**; eklenen tek şey aynı klasörden **ikinci bir import satırı**. Yeni bir
   bağımlılık YÖNÜ doğmadı.

### Kusur 11'e etkisi
**Büyümedi, kapanmadı — sayısı arttı, yönü aynı.** `hakhukuk/` → `scripts/` bağımlılığı
`araclar.py`'de bir importtan ikiye çıktı (`madde_anahtar` + `atif_dogrula`); `servis.py`
zaten aynı şeyi yapıyor (ADR-0078 karar 5 onu **onarmamayı** seçti). Borcun **gerçek**
kapanışı `madde_anahtar` · `atif_dogrula` · `score_abstention` üçlüsünün `hakhukuk/`'a
taşınmasıdır ve o **ayrı bir iştir** — bu görevde yapılmadı, çünkü ölçüm hattının üç
dosyasını birden değiştirirdi.

## 4. TDD — kırmızı görülen testler

`tests/test_araclar.py` (fixture korpusa 193 `GELİR VERGİSİ KANUNU (G.V.K.)` · 1319
`EMLAK VERGİSİ KANUNU` · 2004 `İCRA VE İFLAS KANUNU` eklendi):

```
FAILED tests/test_araclar.py::test_kanun_bul_atif_dogrula_ile_AYNI_sonucu_verir[Gelir Vergisi Kanunu]
FAILED tests/test_araclar.py::test_kanun_bul_atif_dogrula_ile_AYNI_sonucu_verir[GELİR VERGİSİ KANUNU]
FAILED tests/test_araclar.py::test_kanun_bul_atif_dogrula_ile_AYNI_sonucu_verir[İflas Kanunu]
FAILED tests/test_araclar.py::test_kanun_bul_parantezli_adi_DOGRU_kanuna_cozer
FAILED tests/test_araclar.py::test_kanun_bul_resmi_adin_SONEGINI_de_cozer
5 failed, 14 passed in 0.10s
```

`test_kanun_bul_parantezli_adi_DOGRU_kanuna_cozer` kırmızı mesajı:
`AssertionError: 1319'a kayma ya da çözememe: set()` — ürün yüzeyi **çözemiyordu**.
Onarımdan sonra: `19 passed`.

## 5. Eşdeğerlik kanıtı — ölçüm hattının davranışı DEĞİŞMEDİ

Alet: `scratchpad/esdegerlik.py`. İki kol, **aynı** 94 `*detail*.jsonl`:

- **A kolu** — onarım ÖNCESİ alet, `git show HEAD:` ile geçici dizine alınmış izole kopya,
  `hakhukuk` **hiç import edilmeden** (tuzak 5.9: denetim için `git stash` kullanılmaz).
- **B kolu** — çalışma ağacı, **önce `hakhukuk.araclar` import edilerek** (onarımın ölçüm
  hattına sızabileceği **tek kanal**: `sys.path` mutasyonu).

```
dosya: 94   hüküm satırı: 11.634
A sha256: fcf78e9154fcf971af8ad4edf99b2a1e8e3efa84f90745809d883ed6a57f4172
B sha256: fcf78e9154fcf971af8ad4edf99b2a1e8e3efa84f90745809d883ed6a57f4172
✅ EŞDEĞER — birebir aynı
```

Ek olarak `git diff -- scripts/` **boş** ve çıpalar aynen yeniden üretiliyor:

```
f02-biz-onsozsuz   80 cevap · 114 atıf · DOGRULANDI 114 · diğer 0
g16-kabul-testi    40 cevap ·  52 atıf · DOGRULANDI  52 · diğer 0
```

**MANŞET DEĞİŞMEDİ: 0/114 ve 0/52 duruyor.**

## 6. Gerçek paket importuyla çalıştırma (llama-server YOK, `servis.answer` çağrılmadı)

```
paket: /home/ersoy/code/Hukuk-SLM/hakhukuk/__init__.py
  kanun_bul('Gelir Vergisi Kanunu'          ) -> (('193', 'GELİR VERGİSİ KANUNU (G.V.K.)'),)
  kanun_bul('Emlak Vergisi Kanunu'          ) -> (('1319', 'EMLAK VERGİSİ KANUNU'),)
  kanun_bul('İflas Kanunu'                  ) -> (('2004', 'İCRA VE İFLAS KANUNU'),)
  kanun_bul('İş Kanunu'                     ) -> (('1475','İŞ KANUNU'), ('4857','İŞ KANUNU'), ('854','DENİZ İŞ KANUNU'))
  kanun_bul('Türk Ceza Kanunu'              ) -> (('5237', 'TÜRK CEZA KANUNU'),)
  kanun_bul('Fikir ve Sanat Eserleri Kanunu') -> (('5846', 'FİKİR VE SANAT ESERLERİ KANUNU'),)
  kanun_bul('Sanat Eserleri Kanunu'         ) -> (('5846', 'FİKİR VE SANAT ESERLERİ KANUNU'),)
  kanun_bul('Bulunmayan Kanun'              ) -> ()
```

## 7. Endişeler — kayda geçirildi, onarılmadı

1. **`kanun_bul` boş demeti hâlâ İKİ hâli birden anlatıyor:** *"kanun yok"* ile *"ad
   çözülemedi"*. `atif_dogrula` bunları `KANUN_YOK` ↔ `AYRISTIRILAMADI` diye **ayırıyor**;
   araç imzası ayırmıyor. Üçüncü bir dönüş hâli ADR-0076'nın belgelediği imzayı
   değiştirirdi ⇒ yapılmadı, `kanun_bul` docstring'ine yazıldı. **Sessizce yanlış kanun
   SEÇİLMİYOR** — kusur 18'in kalıbı bu tarafta yok.
2. **`'İş Kanunu'` artık `854 DENİZ İŞ KANUNU`'nu da döndürüyor** (sonek gevşemesi).
   Bu, ölçüm hattının **kasıtlı** davranışıdır (`_ad_adaylari` 1. gevşeme, ADR-0038
   kalibrasyon borcu) ve tek kaynak kuralının bedelidir; ayrı bir alet olsaydı yine
   ayrışırdık. Aday çokluğu `kanun_bul`'da zaten **hepsini döndür** ilkesiyle görünür.
3. **Kusur 11 açık.** §3'teki gerçek kapanış işi hâlâ borç kuyruğunda.
