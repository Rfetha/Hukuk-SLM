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


## Bulgu 6 — Kapı maddesinin **çıpası yoktu**, ve düzeltme reçetesi kusurun yarısına uymadı (ADR-0073)

**2026-09-07.** Faz 0'ın son kutucuğu — `v1.0` kapısı madde (3), *"M5 (kör/parametrik)
YÜKSELMEZ"* — üç ayrı katmanda kırıldı ve üçü de **sessiz** kırılmalardı.

### (a) Ön-kayıtlı madde, ölçülemez hâlde ön-kayıtlıydı

Madde *"M5 ≤ **bugünkü**"* diyordu. Koşmadan önce sorulan tek soru — ***"bu sayıyı neyle
kıyaslayacağım?"*** — maddeyi düşürdü: **`tgta_v1`'in M5'i hiçbir birimde hiç ölçülmemişti.**
Defterde `m5_base_th` · `m5_gem_th` · `m5_tg_v1_th` vardı; **merge öznesi yoktu.**
*"Bugünkü"* diye bir sayı olmadığı için madde **kendi kendine referans veriyordu**.

Çıpa [ADR-0039](../../adr/0039-kapi-6-parametrik-sizinti.md) §2'den okundu: **çıpa BASE'dir,
rakip değil** — rakip çıpası orada zaten **değerlendirilip reddedilmişti**
(*"modeli aldığımız noktadan kötüye götürmemeliyiz"*). Ve üç sayı birden raporlanır:
`coverage` · `A1` · `ezber kütlesi = coverage × A1`.
⇒ Eski `base_th` **kıyaslanamaz birimde** (v1 soru seti + 1024 bütçe) ⇒ base **yeniden koşuldu**.

**Yeni tuzak sınıfı (2.17):** *ön-kayıt kuralına uyan ama çıpası olmayan kapı maddesi.*
Kurala uyduğu için denetimden geçiyor; ölçülemez olduğunu **kendisi söylemiyor**.

### (b) Geçerlilik kapısı kaldı — ve ADR-0040'ın reçetesi 3/5 kalemde ETKİSİZ

Koşu 80/80 üretildi (şarjda **21 dk**; pilde 4,8 saat sürecekti — tuzak 1.6 sayıyla ödendi)
ve kapıdan **kaldı**: kesik **5/80 = %6,2 > %5**, `EXIT=2`. ⭐ **Hakem çağrılmadı** — kapı,
bozuk bir koşuya para harcanmasını **fiilen** engelledi.

Beş kalem **gözle okundu**, sonra **deterministik** bir kuyruk-tekrarı dedektörüyle bağımsız
sınandı; **ikisi aynı hükmü verdi** (bu turda alet ↔ göz ilk kez **anlaştı**):

| sınıf | kalem | kanıt |
| :--- | :--- | :--- |
| bütçe kesilmesi | 27 · 43 | 27: düşünce 1536'nın **tamamını** yaktı, cevaba **3 karakter** kaldı (`"Kat"`) |
| 🚨 yozlaşmış tekrar | 28 · 74 · 54 | ibare **×21** · **×19** · **×82** |

ADR-0040 *"kesik > %5 → MAXTOK büyütülüp tekrar koşulur"* diyor. **Üç kalemde bu ölçülmüş
biçimde etkisiz:** `temperature=0` açgözlü kod çözmede döngüye girmiş model **matematiksel
olarak** çıkamaz — büyük bütçe **daha uzun bir döngü** üretir.
[#42](2026-07-29-cp0-dusunce-modu-sonlanmama.md) aynı sınıfta bütçeyi **8× artırmış
(4096 → 32768) ve hiçbir şey değişmemişti.** Yani ön-kayıtlı kural, **kapsamadığı** bir
kusur sınıfına çarptı ⇒ karar insana taşındı.

### (c) Ucuz kaldıraç ölçüldü: $0, hakem yok, deterministik hüküm

İnsan itirazı doğruydu ve benim çerçevem darcı: *"rejimi değiştirmek"* pahalıdır, ama
*"kaldıracın işe yarayıp yaramadığını ölçmek"* **$0**. Döngü tespiti deterministik olduğu
için **hakem bile gerekmedi**.

5 suçlu kalem · aynı GGUF, seed, bütçe, istem · değişen yalnız sunucu bayrağı.
✅ **Kontrol kapısı 5/5 BAYT-BAYT** — alt küme resmî koşuyu birebir üretti.

| kol | kesik | döngü |
| :--- | ---: | ---: |
| kontrol *(bugünkü rejim)* | **5/5** | **3** |
| **`dry` 0.8/1.75/2** | **0/5** | **0** |
| `repeat_penalty 1.1` | 1/5 | 0 |

**DRY seçildi** — ve gerekçesi alan-özgü: ceza `0,8 × 1,75^(n−2)` ile tekrarlanan **dizinin**
uzunluğuyla üstel büyür ⇒ **2 token'a kadar tekrar serbest**. Hukuk metninde *"madde"*,
*"kanun"* ve kanun numaraları **meşru olarak** tekrarlar ve ceza almaz; `repeat_penalty`
ise penceredeki **her** token'ı bağlamsız cezalandırır (ve ölçümde 1 kesik bıraktı).
⭐ İki ceza da logit'i **seçimden önce** değiştirir ⇒ **`temperature=0` ve determinizm korunur**;
#42'nin yarısını kurtaran `temp 0.6` bunu **bozardı**. Ucuz kaldıraç, aynı zamanda
**metodolojik olarak temiz** olan çıktı.

**Kapsam yalnız M5 — tercih değil, teknik zorunluluk.** DRY bir `llama.cpp` örnekleyicisidir,
**Gemini'ye uygulanamaz** ⇒ rakip içeren hiçbir modda eşitlenemez. M5 rakip içermez
(ADR-0039: çıpa base) ve base de yerel `llama.cpp` ⇒ **iki kola da eşit** uygulanabilir.

### 🚨 Kabul edilen bedel — sayıdan ayrılamaz

**DRY modeli DOĞRU yapmadı, AKICI yaptı.** Kör modda cevaplar artık tam ve akıcı — ve yanlış:
İş K. **31** → *"35. ve 36. Maddeler"* · İİK **79/a** → *"110. Madde"* · KMK **33** →
*"Kanun No 633, 10. Madde"* · TBK **230** → *"6502 Sayılı Tüketici Kanunu"*.
M5'in ölçmek için var olduğu şey **tam olarak budur**.

⇒ Döngü kalemi ile akıcı-yanlış kalem hakemden **aynı notu almaz** ⇒ **DRY'li M5, DRY'siz M5
ile aynı birimde DEĞİLDİR**; cp09'un M5 sayılarıyla kıyas **kurulmaz**. Bugünkü iki kol
kendi aralarında aynı birimdedir ve hüküm **orada** kurulur.

⚠️ Ayrıca ölçüldü ve damgalandı: yozlaşmış cevap **çekinme sayılmaz** ⇒ `coverage`'ı yükseltir,
hakem A1'i düşürür. `ezber kütlesi = coverage × A1` olduğu için döngü, anti-hedefi
**olduğumuzdan iyi** gösterebilirdi — ADR-0044'ün *"sapma bizim lehimize"* sınıfı.
İki kolun **aynı** rejimde koşması bunu dengeliyor: **fark** okunabilir, **mutlak** değer
damgasız yayımlanmaz.

### Sonuç — madde (3), İKİ okumada da

| kol | okuma | `coverage` | `A1` | **ezber kütlesi** |
| :--- | :--- | ---: | ---: | ---: |
| **BİZ** | ALET | 0,9500 | 0,4105 | **0,3899** |
| **BİZ** | **GÖZ** | 1,0000 | 0,4057 | **0,4057** |
| base | ALET | 0,9750 | 0,4818 | **0,4697** |
| base | **GÖZ** | 1,0000 | 0,4739 | **0,4739** |

```
ALET  coverage ✅ (−2,50 p)   ezber kütlesi ✅ (−7,98 p)
GÖZ   coverage ✅ (±0,00 p)   ezber kütlesi ✅ (−6,82 p)
```
🟢 **GEÇTİ** — ve **hüküm dedektöre bağımlı değil**: kusur iki kolu da aynı yönde etkiliyor,
ADR-0057'nin eşit sınavı burada **koruyucu** görev görüyor.

### Ve alet ÜÇÜNCÜ kez yanıldı — ilk kez kör modda

Kapının `(*)` şartı gereği çekinme işaretli 6 kalem okundu: **6/6 yanlış pozitif.** Altısı da
hukuki bir **olumsuz hüküm** kuruyor **ve atıf yapıyor** — cevap veriyorlar, üstelik çoğu
**yanlış** (base id 16: *"4711 Sayılı Türk Hakemlik Kanunu"* — **var olmayan bir kanun**).
Mekanizma: `REJECT_RE`'nin *"bulunmamaktadır"* ailesi hukuk metninde **iki iş görür** —
*"kaynakta yok"* (çekinme) ↔ *"kanunda böyle bir hüküm yok"* (**esasa ilişkin cevap**).
**Kör modda kaynak yoktur** ⇒ birinci okuma **tanımı gereği imkânsız**.

| # | nerede | alet → göz |
| :-- | :--- | :--- |
| 1 | bizim şablon, önsözsüz (ADR-0061) | 14 → **8** |
| 2 | Gemini şablonu, F0.4 | 11 → **7** |
| 3 | **kör mod, iki kol** | 6 → **0** |

Üçünde de yön aynı: **alet fazla red sayıyor.** Üçü de yalnız **gözle** görüldü.
⛔ Alet bugün **düzeltilmedi** — kapının sayısı üretildikten sonra aleti değiştirmek ADR-0050'nin
yasakladığı hareketin sınırındadır. Doğru sıra: ölç → iki okumayı da raporla → **sonraki turda,
koşudan ÖNCE** düzelt.

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
