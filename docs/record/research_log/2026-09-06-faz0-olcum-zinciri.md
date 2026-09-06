# #62 — Faz 0: ölçüm zinciri · aletin dört kusuru bulundu, kütle %68,4 → %80,1

**Tarih:** 2026-09-06 / 07 · **Harcanan: ~$1,38** · **Eğitim koşusu: SIFIR**
**Artefakt:** `tgta_v1` — **ağırlıklar hiç değişmedi**

> **Turun tek cümlesi:** Modeli iyileştirmedik; **ölçtüğümüz şeyin ne olduğunu düzelttik** —
> ve dört ayrı kusur bulundukça sayı %68,4'ten %80,1'e çıktı.

## Neden bu tur açıldı

Kullanıcı ön-kabulü: *"3.5 Flash-Lite'e ancak yetişiyoruz, net farkla geçip 3.5 Flash'e
yetişmeliydik."* Doğrulamak için rakip ölçümünün künyesi açıldı ve **ilk kusur oradan çıktı.**

---

## Bulgu 1 — Kaybın yarısı erişim değil, SORU (ADR-0067)

`recall@10 = 0,8750`'nin kaçırdığı 10 kalem gözle okundu. Ölçüt: *"soruyu tek başına okuyan
bir hukukçu altın maddeyi adlandırabilir mi?"*

| sınıf | sayı |
| :--- | ---: |
| **(e) soru altın maddeyi BELİRLEMİYOR** | **5/10** |
| (d) gerçek erişim hatası | 5/10 |
| (b) tablo/chunk · (c) yürürlük | 0 |

En ağırı: İİK 31/a **gemi sicili** hakkındaydı, sorusu *"Mahkeme benim lehime bir karar verirse
ne olur?"* — belirsiz değil, neredeyse **ilgisiz**.

⭐ **Eşleşmeler tam metinle denetlendi ve DOĞRU çıktı** ⇒ kusur yer-gerçeğinde değil, sorunun
**bağlamının sökülmüş** olmasında. Sorular altın maddenin **içinden** üretilmiş; üç kusur sınıfı:
**A** askıda gönderim (öncülsüz *"bu"*) · **B** kanun ailesi belirsiz · **C** kurum belirsiz.

**Sonuç:** DEV 13 + TEST 2 soru yeniden yazıldı (insan onaylı, 15/15). `recall@10` **0,8750 → 0,9375**.
⚠️ **Bir kayıp geri ALINMADI:** id 79 bulunuyorken kaçtı — eski soru öncülsüzdü ama içindeki
*"eğitim"* sözcüğü maddeyle eşleşiyordu; yeni soru o çıpayı kaybetti. Geri almak, eval sorusunu
ölçülen sistemin lehine ayarlamak olurdu.

## Bulgu 2 — Kusur BM25'te değil, FÜZYONDA (ADR-0068)

Kalan 5 hatada kol bazında ölçüm: **dört kalemde bir kol altını 0. sırada bulmuştu**, RRF ikisini
toplayınca ilk 10'un dışına itiyordu. Aritmetiği: `k=60`'ta `1/60 + 1/157 = 0,0231` < iki kolda
5. sıra `2/65 = 0,0308` ⇒ *"iki kolda vasat olmak, bir kolda mükemmel olmayı yeniyor."*

`RRF_K` **60 → 10**. Seçim gerekçesi **plato** (`r@5 = 0,8250`, k∈[5,20]), sivrilik değil.
⭐ **Genelleme donmuş TEST'te, seçimden SONRA doğrulandı:** dört koşulun dördünde de `r@10`
yükseliyor ve kazanç TEST'te (+2,5 p) DEV'dekinin (+1,25 p) **iki katı**.
`recall@10` **0,9375 → 0,9500** · kütle tavanı **%87,5 → %93,75**.

## Bulgu 3 — DEV ↔ TEST farkının %81'i BİLEŞİMDEN (ADR-0069)

TEST'in `recall@10`'u DEV'den ~15 p düşük. Sebep setin zorluğu değil: ayrım **kanuna göre
kusursuz katmanlı (2:1)** ama **madde uzunluğuna göre katmanlanmamış**. Erişim uzunlukta
**U biçimli**: Q1 0,8000 · Q2 0,9333 · Q3 0,9333 · **Q4 0,6667**. En zor dilimde DEV'in payı
**%12**, TEST'in **%50**. Standardize edilince fark 0,1375 → bileşimin açıkladığı **0,1118 (%81)**.

⇒ **v1 kabul testinin kütle tavanı ≈%75'tir, DEV'in %93,75'i değil.** İki sayı aynı metrik
değildir. Raporlama biçimi kabul testi **koşmadan önce** ön-kayıtlandı (S15 → ADR-0069).
🆕 Yeni borç: **uzun madde chunk'lama** — B9'dan ayrı; orada bozuk chunk, burada **doğru ama
çok uzun** chunk (chunk = tam madde, ADR-0054/K2'nin ilk ölçülen bedeli).

## Bulgu 4 — 🚨 Üretim bütçesi rakiple EŞİT DEĞİLDİ, ve aleyhimizeydi (ADR-0070)

`gen_eval_grounded` iki yol izliyordu: rakip `reasoning_budget + max_new_tokens = 1536`,
**biz `think_budget = 1024`**. Ayrı 512 cevap payı **yalnız `content` boş kalan** kalemlere
veriliyordu. Kod ADR-0043 §2'ye **sadıktı**; kusur protokolün kendisindeydi.

| kol | zorla kapatılmayan | tavan | 1024'ü fiilen aşan |
| :--- | ---: | ---: | ---: |
| BİZ (üç koşuda da) | 75-76 / 59 | **1024** | — |
| 3.1 FL | — | **1532** | **36/80** |
| 3.5 FL | — | **1532** | **18/80** |

ADR-0043 §3 *"bütün rakipler aynı bütçeyle koşar; sapma kıyası geçersiz kılar"* diyordu —
**şart tutmuyordu.** 🚨 Ve bu, **yayımlanmış bir hükmü çürüttü**: `g2-fl-harness/OZET.md` §K2
*"bizde ADR-0043 gereği ayrık bütçe var"* diyordu. O dosyada **üstü çizilerek** damgalandı.

Tek formüle geçildi: `max_tokens = (reasoning_budget or think_budget or 0) + max_new_tokens`.
⚠️ **Neden bugün patladı:** önsöz kalkınca model `</think>`'i daha sık kendi kapatıyor (zorla
kapatma **21/80 → 5/80**), ayrı 512 payını alan kalem azaldı, paylaşımlı bütçenin bedeli görünür
oldu. **S14 kararı kusuru yaratmadı, açığa çıkardı.**

Tetikleyen olay: F0.2 koşusu kesiklik kapısında düştü (5/80 = %6,2 > %5). **Kapı doğru çalıştı** —
hakem parası harcanmadan durdurdu. Kesiklik **belirtiydi**, sebep bütçe eşitsizliğiydi.

## Bulgu 5 — Dedektör İKİ kez yanıldı, iki farklı şablonda (`suskunluk_terazisi`)

**Bizim kolda:** 80 kalem gözle okundu → alet 5 çekinme dedi, **beşi de gerçek**;
aletin *"cevapladı"* dediği ama red ibaresi taşıyan 7 kalem de okundu → **yedisi de tam cevap**.
**Alet ↔ göz farkı SIFIR** (önceki turda 14 ↔ 8 idi; ADR-0061'in onarımı tuttu).

**Rakip kollarda — zorunlu kalibrasyon adımı:** 28 rakip çekinme kalemi okundu.

| kol | alet | temiz çekinme | çekinceli cevap | **açık yanlış pozitif** |
| :--- | ---: | ---: | ---: | ---: |
| BİZ | 4 | **4** | 0 | **0** |
| 3.1 FL | 8 | 5 | 0 | **3** |
| 3.5 FL | 9 | 5 | 2 | **2** |
| 3.5 Flash | 11 | 7 | 3 | **1** |

Örnek (3.1 FL id 38): *"**TCK 235'e göre** … cezalandırılır."* — altın maddeden **doğru cevap**,
alet çekinme saymış. ⇒ **Üstünlüğümüzün bir kısmı aletin eseriydi**; düzeltilmiş sayılar raporlandı.

Alet + protokol birlikte **`suskunluk_terazisi`** adını aldı (kullanıcı kararı): dedektör tek
başına hüküm vermez, **iki kefe** gerekir.

## Sonuç — dört özne, eşit sınav, aynı birim (ilk kez)

| eksen | **BİZ** | 3.1 FL | 3.5 FL | **3.5 Flash** |
| :--- | ---: | ---: | ---: | ---: |
| **kütle** (bağlayıcı: GÖZ-katı) | **0,8011** | 0,7058 | 0,7622 | **0,7425** |
| A1 · altın getirilen | **0,8902** | 0,7900 | 0,8449 | 0,8523 |
| aşırı-red | **4** | 8 | 9 | 11 |
| **uydurulmuş madde** | **0** | 1 | 4 | 4 |
| `recall@10` | 0,9500 | 0,9500 | 0,9500 | 0,9500 |

**`v1.0` kapısı madde (1): üç okumada da GEÇTİ** — en muhafazakârında **+5,86 p** (ADR-0064).
Ağustos'ta aşırı-red rakibin **iki katıydı**; bugün en güçlü eksenimiz.

## Diğer kapanan borçlar
- **F0.5 · `SOURCE_CLIP` 3500 → 12000** ($0,78): `k=10`'un paydasının **65'i k=4'ün önbelleğinden
  devralınmıştı** (önek çakışması). Şimdi 0 devralınıyor. ⚠️ Tahmin $0,30'du; sapmanın sebebi
  **borcun kendisi** — eski koşuda hakem zaten çağrılmıyordu.
- **F0.6 · `tgta_v1` VRAM**: 3,09 / 3,70 / 5,76 GiB (base ile birebir), ≤8 GB kapısı 128K'da bile geçiliyor.

## ⚠️ Kendi aleyhimize iki kayıt
1. **8 isabetsizliğin 2'si benim yazdığım sorularda** (id 27 · 42): durumu tarif ederken **komşu
   maddenin dilini** kullanmışım (KMK 25'in açılışı · TBK 214'ün ifadesi). Yanlılık koruması
   **ters yönde** işledi. Sorular düzeltilmedi.
2. **B1 için otomatik vekil metrik YOK** ve ölçüldü: `faith<0,6` süzgeci 4, *"altın atıflarda
   yok"* süzgeci 3, **gözle tam tarama 8** buluyor. ADR-0055'in kodunun açılmamış olmasının
   mekanik açıklaması budur.

## Ders
**Dört kusurun dördü de "hata vermeden yanlış sayı üreten" sınıftandı** ve dördü de ancak
**gözle okuma** ya da **künyeyi açıp okuma** ile bulundu. Sayısal kapılar dördünü de geçirmişti.
Yol boyunca 8 alet tuzağı daha yakalandı ve plana yazıldı (`--out` dizin bekliyor · `--cihaz cuda`
şart · `--model` varsayılanı üretimden farklı · `tail` borusu ilerlemeyi gizliyor ·
`cp0_thinking_gen.sh` emekli değil canlı koşucu · harness `free`'ye bakıp arka plan görevini
öldürüyor · rakip tarafı `--reasoning-budget` ister · `measure_vram_stack` bayrakları).
