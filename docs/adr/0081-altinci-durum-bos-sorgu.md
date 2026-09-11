# ADR-0081 — Altıncı `Durum` eklendi: **`BOS_SORGU`** — boş sorgu, "kaynakta karşılık yok" DEĞİLDİR

**Tarih:** 2026-09-11
**Statü:** yürürlükte
**Karar:** **insan** (2026-09-11) — tip düzeyi bir değişikliktir ve bu yüzden kod yazılmadan
önce karara bağlanmıştır. Kararın metni (plan, `AÇIK KUSURLAR` kusur 16):
*"ALTINCI `Durum` EKLENSİN — tip düzeyi değişiklik, **ADR-0081** yazılacak."*
**Bağlı:** [ADR-0076](0076-kapi-kaldirac-ayrimi-arac-katmani.md) (beşinci değer `ARAMA_TUKENDI`:
*sınır GÖRÜNÜR olmalı* — bu ADR'nin emsali ve aynı gerekçe kalıbı) ·
[ADR-0061](0061-cekinme-dedektoru-istem-rejimi-bagimliligi.md) (çekinme dedektörünün rejim
bağımlılığı: aleti ikili sanmanın bedeli) ·
[ADR-0040](0040-dusunce-modu-olculecek-on-kayitli-kural.md) (geçerlilik kapısı — bu değerin
ölçüm hattında **üretilmediği** için o kapıya dokunmadığı yer) ·
[ADR-0080](0080-urun-yolu-zorunlu-dusunce-kapatmasi.md) (aynı turun rejim kararı)
**Kaynak:** kod incelemesi bulgusu **B5** (2026-09-11), `hakhukuk/servis.py`
`_bos_sorgu_cevabi()` docstring'inde **şerh olarak yazılıydı** · kusur kaydı: plan
[`AÇIK KUSURLAR`](../superpowers/plans/2026-09-07-hp-hat-a-hat-b.md#açık-kusurlar--kayıt-ve-devir) kusur **16**
**Kayıt:** [#66](../record/research_log/2026-09-11-urun-yuzeyi-ve-aygit-kusurlari.md)

---

## Bağlam — rozet ile gövde AYNI ŞEYİ SÖYLEMİYORDU

Boş sorgu kapısı (kusur 4, Görev 21) `servis.answer()`'a kondu ve `_getir`'e hiç girmeden
dürüst bir mesajla dönüyordu. Ama döndürdüğü durum `Durum.SUSKUNLUK`'tu ve ürün yüzeyinde
iki cümle **birbirini yalanlıyordu**:

| nerede | ne diyor |
| :--- | :--- |
| **rozet** (`cli.ROZET[Durum.SUSKUNLUK]`) | *"🤐 SUSKUNLUK — **kaynaklarda karşılık bulunamadı**"* |
| **gövde** (`_bos_sorgu_cevabi()`) | *"**Soru boş görünüyor.** Cevap üretebilmem için … soru yazmanız gerekir."* |

Rozet *"aradım ve bulamadım"* der. O dalda **hiç arama yapılmaz** — kapı `_getir`'den
öncedir ve bu, kapının varlık sebebidir (`_getir("")` sabit bir gürültü kümesi döndürüyordu).
Yani rozet, gerçekleşmemiş bir işlemi rapor ediyordu.

İkinci ve daha sessiz sonuç: **boş sorgular suskunluk sayımının içine bir yol açmıştı.**
Bugün bu yoldan hiçbir şey geçmiyor (DEV'de 0 boş kalem) ama yolun kendisi açıktı.

## Niçin `Durum` **kapalı bir küme** — ve niçin bu, değer eklemeyi yasaklamaz

`tipler.py`'nin başındaki ölçülmüş gerekçe: `Durum` bir `bool` değil, çünkü **dünya ikili
değil** ve bunu iddia eden alet **üç kez** yanıldı (üçünde de FAZLA red saydı):

```
2026-09-06  bizim şablon, önsözsüz    alet 14 → göz  8   (ADR-0061)
2026-09-06  Gemini şablonu, F0.4      alet 11 → göz  7
2026-09-07  kör mod, iki kol          alet  6 → göz  0   (6/6 yanlış pozitif)
```

Kapalı küme olmasının işlevi, **her hâlin adının olması ve adsız bir hâlin başka bir adın
altına saklanamamasıdır**. Bu yüzden küme kapalıdır; ama kapalılık, **yeni bir hâl ölçülünce
ona yeni bir ad verilmesini yasaklamaz** — tam tersine onu şart koşar. ADR-0076 bunu bir kez
yapmıştı (`ARAMA_TUKENDI`, `KESIK`'e katlanmadı) ve bu ADR aynı kalıbın ikinci uygulamasıdır.

## Niçin altıncı değer **gerçekten ayrı bir şey söylüyor**

| durum | vatandaşa söylediği | vatandaşın yapması gereken |
| :--- | :--- | :--- |
| `SUSKUNLUK` | *"Aradım; **kaynaklarda karşılık yok.**"* | soru geçerli — başka kaynağa / avukata git |
| `BOS_SORGU` | *"**Soru yazılmadı**; arama YAPILMADI."* | **soruyu yaz** |

İkisi farklı **eylem** gerektirir, dolayısıyla farklı hâldir. `KESIK` ↔ `ARAMA_TUKENDI`
ayrımının kurulma gerekçesi birebir budur: *"cümle yarım"* ile *"cümle tam, dayanağı eksik"*
vatandaşa farklı şey söyler.

## Elenen seçenek — `SUSKUNLUK`'u yeniden kullanıp ROZETİ değiştirmek

Reddedildi. Rozet metnini *"soru yazılmadı veya kaynaklarda karşılık yok"* gibi bir hâle
getirmek çelişkiyi görünürde kapatırdı, ama **bütün suskunluk kalemlerini yanlış
etiketlerdi**: gerçek çekinme kalemleri (bugün ölçülen 8/80, gözle) *"soru yazılmadı"*
ihtimalini taşımaz. Tek bir kusurlu kalem için doğru sınıflandırılmış onlarca kalemin
etiketini bulanıklaştırmak, bu hattın **ölçüm aletini bozma** sınıfındaki hatasıdır
(ADR-0050'nin kalıbı: **alet düzeltilir, eşik/etiket oynatılmaz**).

Ayrıca rozeti bulanıklaştırmak, `Durum`'un kendi varlık sebebini çürütürdü: ayrımı **tip
seviyesinde** kurup sunum katmanının bunu okumasını sağlamak, ayrımı **metinde** anlatmaya
çalışmaktan üstündür (POSD, *"errors out of existence"*).

## Karar

1. `Durum`'a altıncı değer: **`BOS_SORGU = "bos_sorgu"`**.
2. `servis._bos_sorgu_cevabi()` bu değeri döndürür — gövde metni **değişmedi**.
3. Beş yüzey güncellendi: `cli.ROZET` (`⌨️ BOŞ SORU — soru yazılmadı; arama YAPILMADI`) ·
   `tui.ROZET` (`⚫ BOŞ SORU — soru yazılmadı, arama yapılmadı`) ·
   `cli.main --durumlari-listele` (kümeyi gezer, kendiliğinden altı basar) ·
   `api.py` şeması (`durum: str` — **büyümedi**, gerekçe aşağıda) ·
   `terazi.siniflandir` (bu değeri **üretmediği** teste bağlandı).
4. **Kapı `answer()`/`answer_arac()`'ta, teraziden ÖNCEDİR.** `terazi` bir MODEL ÇIKTISINI
   sınıflandırır; *"boş sorgu"* diye bir model çıktısı yoktur — boş sorguda model hiç
   çağrılmaz. `terazi` kaynağında `BOS_SORGU` geçmediği ayrıca **test edilir**.

## Ne KURULMAZ

- **Bu değer ÖLÇÜM HATTINDA ÜRETİLMEZ.** Ölçüm hattı (`scripts/olcum_uretim/**`)
  `hakhukuk.tipler`'i kullanmaz; `terazi.siniflandir` bu değeri üretemez ve DEV kümesinde
  (`data/eval/dev/core_hard.jsonl`, n=80) **0 boş kalem** vardır.
  ⇒ **Yayımlanmış hiçbir sayı etkilenmez** — ne `0,8011`, ne kabul testinin `0,5804`'ü,
  ne çekinme/aşırı-red sayaçları. Bu bir **ürün yüzeyi** düzeltmesidir.
- **`api.py` şeması BÜYÜMEDİ ve büyümemeli.** HTTP yüzeyinde boş sorgu `answer()`'a hiç
  ulaşmaz: `422` kapısı önce durur (Görev 19 karar 5). Dolayısıyla `durum == "bos_sorgu"`
  diye dal yazan bir tüketicinin dalı **ölü** olurdu. Bu, şemaya bir `enum` eklememenin de
  gerekçesidir; testle çivilendi.
- Bu karar *"boş sorgu kusuru artık yok"* **demez** — kusur (kusur 4) Görev 21'de zaten
  kapanmıştı. Bu ADR yalnız o kapının **ne söylediğini** düzeltir.
