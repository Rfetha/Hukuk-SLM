# #67 — Aleti onardık, çıpaları yeniden puanladık, konteyneri ayağa kaldırdık; kusurların dördü **aynı gün bizim yazdığımız koddan** çıktı

**Tarih:** 2026-09-11/12 (turun ikinci yarısı) · **Bedel:** **$0,045067** — turun tek hakem
çağrısı Görev 22 Adım 2'ye aitti ve [#66](2026-09-11-urun-yuzeyi-ve-aygit-kusurlari.md)'nın
ekinde kayıtlıdır; **bu kaydın kapsadığı işlerin tamamı hakemsiz, GPU'suz ve ağsızdır** (yalnız
`docker compose up` HF'ten pinli revizyonu çekti). Kaynak: plan, Görev 22 Adım 2 —
OpenRouter `total_usage` 17,91293753 → 17,95800443.
**Çıktılar:** [`outputs/eval/g22-atif-onarim/`](../../../outputs/eval/g22-atif-onarim/) ·
[`outputs/eval/g22-rakip-yeniden-puanlama/`](../../../outputs/eval/g22-rakip-yeniden-puanlama/) ·
[`outputs/eval/g20-imaj-olcumu/`](../../../outputs/eval/g20-imaj-olcumu/)
**Kararlar:** [ADR-0081](../../adr/0081-altinci-durum-bos-sorgu.md) ·
[ADR-0082](../../adr/0082-app-kutusu-host-sapmasi.md)
**Commit aralığı:** `2d83c5d..4a56f78` — **31 commit** (`git rev-list --count f1edb73..HEAD`);
turun tamamı 2026-09-11 00:00'dan beri **50 commit**, hepsi **yerel** (`origin/master`'a göre
60 gönderilmemiş commit var, push EDİLMEDİ)
**Plan:** [`plans/2026-09-07-hp-hat-a-hat-b.md`](../../superpowers/plans/2026-09-07-hp-hat-a-hat-b.md)
Görev 12 (Adım 6-7) · Görev 19 (Adım 6) · Görev 20 (Adım 6-8) · Görev 21 (Adım 11) ·
`AÇIK KUSURLAR` kusur **14-32**

> **#66 nerede bitiyordu:** *"ürün yüzeyini temizlemek ölçüm aygıtında üç kusur buldu"* —
> tuzak **1.11 · 1.12 · 1.13**, §13'e kadar.
> **#67 ondan sonrasıdır ve dersi bir adım öteye gidiyor:** bu turda bulunan kusurların
> **dördü bizim aynı gün yazdığımız koddandı** ve **hiçbirini test yakalamadı**.
> Ağırlıklara dokunulmadı; yayımlanan **tek** sayı değişti ve o da **aleyhimize** (§3).

---

## 1. Yedi insan kararı uygulandı — kusur 14-20

#66'nın kod incelemesi dört yeni kusur doğurmuş, ikisi daha G22 Adım 1'den gelmişti. Yedisi de
insana soruldu, yedisi de karara bağlandı ve uygulandı (plan, `AÇIK KUSURLAR`):

| kusur | karar ve sonuç | commit |
| :-- | :--- | :--- |
| **14** | `madde_sayisi` **ölü alandı** — SİL (YAGNI). Alan + yardımcı + 4 test silindi; üretimde sıfır çağrı `grep` ile doğrulandı | `7d1af54` (yapısal) |
| **15** | kapsam satırı yalnız TUI'deydi — CLI ve HTTP'ye de EKLE. `bicimle()`'ye kondu ⇒ **üç yüzey birden** aldı; sayılar `data/corpus/KUNYE.json`'dan okunuyor | `61162d0` |
| **16** | rozet ile gövde birbirini yalanlıyordu — **ALTINCI `Durum`: `BOS_SORGU`**. Tip düzeyi değişiklik olduğu için kod yazılmadan önce karara bağlandı: [ADR-0081](../../adr/0081-altinci-durum-bos-sorgu.md). Beş yüzey güncellendi; kapı teraziden **önce**dir, `terazi` bu değeri üretemez ve bu **testle çivilendi** | `d79c01b` |
| **17** | `tui.py` ile `cli.py` **iki paralel sunum katmanıydı** ve bu, turun iki sızıntısının (iskele işareti · kapsam satırı) **kök nedeniydi** — BİRLEŞTİR. TUI kendi sunum dizesini kurmayı **bıraktı**; tek katman `cli.bicimle(cevap, rozet=…)`, rozet **parametre** (bool bayrak yok) | `613e3ba` (yapısal) |
| **19** | fp16 rejiminde model istem yer tutucusunu harfiyen basıyordu (`0/80 ↔ 2/80`) — sunumda **silinmedi, dürüstçe işaretlendi**: `(KANUN ADI, Madde 13)` → `(kanun adı belirtilmemiş, Madde 13)` | `5398c66` |
| **20** | ürün yolunun ikinci geçişi `reasoning_content` alanına bağımlıydı ve sunucu varsayılanı değişirse **sessizce tek geçişe düşerdi** — İKİSİ DE: **çalışma anı kapısı** (sessiz düşüş yerine ERKEN ve gürültülü patlama, ADR-0026'nın sınıfı) **ve** `compose.yaml`'da `--reasoning-format deepseek` **açıkça pinlendi** | `3a8109e` · `1d0c616` |

Kusur **21** ve **22** aynı gün karara bağlandı ve §3-§4'te kendi başlıklarını aldı.

---

## 2. Atıf doğrulayıcı ONARILDI ve ÇIPALAR yeniden puanlandı

Kaynak: [`outputs/eval/g22-atif-onarim/BULGU.md`](../../../outputs/eval/g22-atif-onarim/BULGU.md)
· tuzak **1.13** · insan kararı: *"aleti onar **ve** çıpaları yeniden puanla"*.
Model çağrılmadı, `llama-server` açılmadı, donmuş TEST'e yeni soru sorulmadı — diskte **zaten
duran** cevaplara **düzeltilmiş alet** yeniden uygulandı. ADR-0050'nin kalıbı: *alet düzelir,
eşik oynamaz.*

**TDD.** 8 test eklendi, onarımdan önce koşuldu: **4 kırmızı · 25 yeşil**. Kalan 4 test ilk
koşuda da yeşildi — bunlar bilerek konmuş **regresyon çıpalarıdır** ve *eski doğruların
bozulmadığını* çiviler (`0/114` manşetinin kaynağı · *"İcra **ve** İflas"* · *"Sina**î**
Mülkiyet"* · aynı adlı iki kanunda **yürürlüktekini** seçme).

**Çözüm kuralı — tek cümle.** Ad çözümünde **en çok TEK gevşemeye** izin verilir: ya atıftaki
adın tamamı bir kanun adının (sondaki parantezi atılmış hâli dahil) ≥2 sözcüklü **soneki** olur,
ya da ayrıştırıcının ada kattığı **baştaki sözcükler** atılır ve kalan **birebir** bir kanun adı
olur — **ikisi birden asla**. İkisi birden gerekiyorsa hüküm **`AYRISTIRILAMADI`**'dır ve
sessizce bir kanun **SEÇİLMEZ**. Ayrıca `Hukum` artık **çözülen kanunun ADINI** taşır, ki
yanlış çözüm gözle görülebilsin.

**Kusur sınıfının kapandığının kanıtı — sentetik prob, $0.** Adı modelin fiilen yazdığı biçimde
(parantezsiz) verilen 16 kanunda:

| sonuç | ÖNCE | SONRA |
| :--- | ---: | ---: |
| doğru kanuna çözdü (`DOGRULANDI`) | 0 / 16 | **7 / 16** |
| **YANLIŞ** kanuna çözüp yine `DOGRULANDI` aldı | **7 / 16** | **0 / 16** |
| `AYRISTIRILAMADI` | 9 / 16 | 9 / 16 |

Kalan 9, adında parantez **ortada** olan kanunlardır (`… GAZLARI (LPG) PİYASASI …`);
bu **ayrıştırıcının** (regex) kusurudur, çözümün değil, ve **kapsam dışı bırakıldı**.

**Çıpalar OYNAMADI — ve bu bir bulgudur, boş bir sonuç değil:**

| küme | n cevap | n atıf | `DOGRULANDI` ÖNCE → SONRA |
| :--- | ---: | ---: | :--- |
| DEV çıpa `f02-biz-onsozsuz` | 80 | 114 | 114 → **114** (`MADDE_YOK` 0 → 0) |
| donmuş TEST `g16-kabul-testi` | 40 | 52 | 52 → **52** (`MADDE_YOK` 0 → 0) |
| fp16 koşusu `g22-kv-fp16` | 80 | 152 | 149 → **150**, `MADDE_YOK` **1 → 0** |

Yayımlanan **`0/114`** (DEV) ve **`0/52`** (donmuş TEST) manşetleri **aynen durmaktadır**.
`g22-atif-cozum` *"manşet temiz ama TESADÜFEN — korunma aletten değil ÖRNEKLEMDEN geliyor"*
demişti (114 atfın hiçbiri parantezli adlı bir kanuna denk gelmemişti); **artık korunma
aletten geliyor** ve manşet aynı yerde duruyor.

**Onarım başka bir yeri bozdu mu — geniş süpürme.** Aynı alet 94 koşu dosyasında kullanılıyor:
**11.634 atıf** tarandı, **41'inin** (%0,35) hükmü/çözümü değişti — 22'si `DOGRULANDI →
AYRISTIRILAMADI` (çoğu **yanlış kanuna basılmış** `DOGRULANDI`'nın kalkması), 16'sı
`MADDE_YOK → AYRISTIRILAMADI`, 2'si `MADDE_YOK → DOGRULANDI`, 1'i `DOGRULANDI → MULGA`.
Tekilleştirilmiş 15 kalıp gözle okundu. **Tek gerçek kayıp:** korpus adı `SİLÂHLI` (şapkalı
`â`) yazıyor, ayrıştırıcının sözcük sınıfı `â` taşımıyor, ad kesiliyor; eski gevşek çözüm bu
**yazım farkını** tesadüfen kurtarıyordu, yeni kural kurtarmıyor. Bedeli **tek vakada**
ölçüldü ve o vaka **geçersiz ilan edilmiş** bir koşudadır (canlı çıpada ve donmuş TEST'te
yok). Yazım-hatası toleransı borcu (**B8**) bu turda **kapatılmadı**.

---

## 3. RAKİPLER de yeniden puanlandı — ve sonuç **ALEYHİMİZE**, öyle yazıldı

Kaynak:
[`outputs/eval/g22-rakip-yeniden-puanlama/BULGU.md`](../../../outputs/eval/g22-rakip-yeniden-puanlama/BULGU.md)
· kusur **22** · insan kararı: *"Sonuç aleyhimize çıksa bile yazılır: bugün tabloda iki farklı
aletin sayısı yan yana duruyor ve bu ADR-0057'nin **eşit sınav** kuralını ihlal ediyor."*

**Kalibrasyon kapısı önce koşuldu ve GEÇTİ.** Yayımlanan boru hattı (`scripts/puanlama/harness_tablo.py`)
önce **bizim** kolumuzda koşuldu; üretilen JSON yayımlanan `f02-biz-onsozsuz/harness_tablo.json`
ile **alan alan birebir** çıktı: kütle **0,8011** · `coverage` **0,9375** · `A1` **0,8545** ·
`recall@10` **0,9500** · `atif_dagilimi` `{DOGRULANDI 114, MADDE_YOK 0, KANUN_YOK 0,
AYRISTIRILAMADI 0, MULGA 0}`. **Kapı geçti ⇒ rakiplere geçilebildi.**

**702 atfın yalnız 1'i değişti** ve o da **rakip aleyhine yanlış** basılmış bir damgaydı:

| kol | `MODEL_CARD` gösterimi ÖNCE → SONRA |
| :--- | :---: |
| BİZ `tgta_v1` | 0/114 → **0/114** (değişmedi) |
| `gemini-3.1-flash-lite` | **1/152 → 0/153** — tek değişen |
| `gemini-3.5-flash-lite` | 4/130 → **4/130** (değişmedi) |
| `gemini-3.5-flash` | 4/133 → **4/133** (değişmedi) |
| `claude-sonnet-5` | 2/163 → **2/163** (değişmedi) |

Değişen tek atıf gözle okundu: 3.1 Flash-Lite, soru **id 25** (*"Kira bedelini nasıl
belirliyoruz?"*), atıf *"GELİR VERGİSİ KANUNU, Madde 73"* — eski alet adı çift gevşemeyle
`VERGİSİ KANUNU` sonekine düşürüp **1319 EMLAK VERGİSİ KANUNU**'na çözüyor, orada 73. madde
bulunmayınca `MADDE_YOK` (= uydurma) damgası basıyordu. Korpus tanığı **vardır ve mülga
değildir** (`193 / Madde 73`, `mulga = False`) ve modelin yazdığı içerikle birebir örtüşüyor.
**Yeni hüküm doğrudur.**

**Kaybettiğimiz şey ve karşılığında aldığımız şey — ikisi de yazılır.** *"Uydurulmuş madde
numarası"*, bugüne kadar rakiplerin **tamamının** üstünde olduğumuz **tek deterministik**
eksendi; `gemini-3.1-flash-lite` artık bu eksende bizimle **eşittir** (`0` ↔ `0`) ve üstelik
paydası lehine büyümüştür (`152 → 153`). Karşılığında **eşit sınav** sağlanmıştır
([ADR-0057](../../adr/0057-harness-rekabet-kapisi-esit-sinav.md)): tablodaki beş sütunun beşi
de artık **aynı, onarılmış aletin** sayısıdır ve *"bizimki onarılmış aletle, rakipler
onarılmamış aletle"* şerhi kaldırılabilir. Her kol **iki kez** koşuldu, çıktılar **bayt bayt**
aynı (kusur 23'ün *"bir kez eski sayıyı verdi ve tekrarlanamadı"* olayı **görülmedi**).

**Yan etki, yayımlanmamış bir alanda, yine de kayda geçirilir:** 3.1 FL'de katı red kapısı
`gecen` **78 → 79** · `reddedilen` **2 → 1** · `kapi_sonrasi_coverage` **0,8625 → 0,8750**.
Bu alanlar `MODEL_CARD`/`HF_KARTI`'nda yayımlanmamıştır, dolayısıyla düzeltilecek bir manşet
yoktur.

### Satırın BİRİMİ hiçbir yerde yazılı değildi — ve bu bir ön sondayı zaten yanıltmıştı

Yayımlanan `x/y` gösterimi `atif_dagilimi`'nden **iki ayrı alanla** kuruluyor:

```
pay   ("uydurulmuş madde")  = MADDE_YOK + KANUN_YOK
payda ("doğrulanan atıf")   = DOGRULANDI            <- TOPLAM ATIF DEĞİL
```

Ön sonda *"3.5 Flash-Lite 4 → 3"* okumuştu; **yeniden üretilemedi ve çürütüldü** — o kolda
**hiçbir atfın hükmü değişmedi**. Düşüş, **eski payın** `MADDE_YOK + KANUN_YOK = 3 + 1 = 4`
iken **yeni payın** yalnız `MADDE_YOK = 3` okunmasından doğan bir **birim kaymasıdır**.
Aynı sebeple sondanın paydası da (`154 ↔ 152` · `134 ↔ 130`) yanlış değil, **başka bir
büyüklüktü**: `atif_dogrula.py`'nin CLI'ı `n_atif` alanında **toplam atfı** basıyor.
Çelişki `MODEL_CARD` ve `CLAUDE.md`'ye **iki yerde** damgalandı.

**Yan kusur (25), kapatılmadı:** Sonnet-5 hücresi **farklı birim** kullanıyor — paydası
**toplam atıf** (163), Gemini sütunlarınınki **`DOGRULANDI`** (152/130/133). Bu iki hücre
**aynı kesir değildir**. Sayı oynamadığı için hüküm etkilenmedi; birim farkı açık kusur
olarak kayıtlıdır.

---

## 4. Kusur 21 — ürün yüzeyi ile ölçüm hattı AYRIŞMIŞTI, ve ayrışma büyüktü

`hakhukuk/araclar.py` **kendi ikinci ad indeksini** taşıyordu; §2'nin onarımı oraya geçmemişti.
Tuzak **2.18**'in kalıbı: *aynı ölçümün ikinci bir aleti*. Sonuç, vatandaşa giden atıf
doğrulaması ile yayımlanan sayıyı üreten doğrulamanın **AYRI** olmasıydı. İnsan kararı:
*"onarımı ürün yüzeyine de taşı — tek kaynak."*

**Ayrışma önce ÖLÇÜLDÜ, sonra onarıldı** (rapor: `.superpowers/sdd/g21/kusur-21-report.md`,
commit `f6908e3`):

| küme | farklı çözülen |
| :--- | ---: |
| 892 kanun adı | **19** |
| parantezli adlı 16 kanun | **7** |
| çıpanın gerçek atıfları (n=114) | **24** |

Ve ayrışmanın **yönü beklenenin tersiydi**: ürün yüzeyi onarımdan **daha da katı** bir eski hâl
taşıyordu — yanlış kanuna basmıyordu, ama parantezli/kısaltılmış adları **hiç çözemiyor**,
modele *"böyle bir kanun yok"* diyordu. Onarım sonrası **0/892 · 0/16 · 0/114**.

Seçenek (a) seçildi: `araclar.py` `atif_dogrula`'dan **import eder**, kopya indeks **silindi**.
**Eşdeğerlik kanıtlandı:** 94 dosya · 11.634 hüküm, iki kolun çıktısı `sha256` **birebir**.

---

## 5. Görev 20 — konteyner uçtan uca ÇALIŞTI, ama ÖNCE KIRILDI

Sıra olduğu gibi anlatılır, çünkü **kırılmanın kendisi turun en öğretici bulgusudur**.

### 5.1 İmaj build edildi ve ÖLÇÜLDÜ (tahmin yazılmadı)

Kaynak: [`outputs/eval/g20-imaj-olcumu/BULGU.md`](../../../outputs/eval/g20-imaj-olcumu/BULGU.md)
— hakem YOK, model çağrısı YOK, HF'ten indirme YOK.

| ölçü | değer |
| :--- | ---: |
| build çıkış kodu · süre | **0** · **234 saniye** |
| build bağlamı (BuildKit'in gerçekten aktardığı) | **77,42 MB** |
| `hakhukuk:0.3.0` — açılmış | **2,13 GB** (sıkıştırılmış içerik 452,7 MB) |
| `llama.cpp:server-cuda-b10902` — açılmış | **6,99 GB** (sıkıştırılmış 2,59 GB) |
| iki imajın toplamı | **9,12 GB** |

`.dockerignore` **74 GB'lık `models/**`'ı kesti**; imajda tek bir `.gguf`, `gomme.npy` ya da
`safetensors` **yok** (`find / -xdev` → **0 eşleşme**) ⇒ **ağırlık ve indeks imaja gömülmedi**.

**G20 ajanının torch endişesi ÇÜRÜTÜLDÜ.** Endişe: *"`sentence-transformers` torch'u kurulu
bulmazsa PyPI'nin CUDA tekerleğine düşer ve imaj ~5 GB şişer."* İmajın içinden ölçüldü:
`torch.__version__` = **`2.14.0+cpu`**, `torch.version.cuda` = **`None`** ⇒ **CPU tekerleği**,
katman **943 MB**'da kaldı. **Duman denetimi 3/3 geçti** (import · `hakhukuk --kuru-calisma`
çıkış 0 · `indir` modülü, hepsi `--network none` ile).

İki kusur ölçüldü ve **onarılmadı**: **29** — `COPY data/corpus/` ürünün hiç okumadığı bir
**36,1 MiB**'lık yedeği imaja sokuyor (76,7 MB'lık korpus katmanının %49'u); **30** — §6'da.

### 5.2 `docker compose up` koştu: indirme kapısı GEÇTİ, ama her soru HTTP 500 verdi

`export HF_TOKEN=…` ile üç kutu da ayağa kalktı: `indir` **çıkış 0** · `llama` **healthy** ·
`app` **Up**. **`sha256` + bayt kapısı GERÇEKTEN ateşlendi ve TUTTU**; model HF'ten pinli
revizyondan indi, indeks **volume'de** bulundu ve HF yedeğine **hiç gidilmedi** (karar 4'ün
*"volume öncelikli"* hükmü çalıştı). Boş sorgu **422** döndü.
**Ama gerçek soru HTTP 500 verdi — açık kusur 32.**

**Kök sebep, ve bu turun en öğretici bulgusu.** İndeksin `KUNYE.json`'u korpus yolunu
**indeks dizinine göreli** tutuyordu (`../../corpus/mevzuat_maddeler.jsonl`). Repoda bu
`data/corpus/…`'a doğru çözülüyor; konteynerde indeks **volume'de** olduğu için `/corpus/`'a
çözülüyor ve korpus orada değil. Yani bu, **`G8 Adım 1b`'nin TAŞINABİLİRLİK onarımının TERS
YÜZÜDÜR**: mutlak yol → göreli yol değişikliği `git clone`'u **onardı**, ama indeksin repo
ağacının **DIŞINA** taşındığı tek düzeni (konteyner) **kırdı**.
**Sessiz değildi:** `SystemExit` ile gürültülü patlıyordu.

### 5.3 Çözümün inceliği ve S18 kapısı

İnsan kararı: *"korpusu da volume'e koy."* Korpusu öylece `/artefakt/corpus/`'a koymak
**yetmezdi** — `../../` indeks dizininden **iki** seviye çıkar. O yüzden **repo düzeni birebir
aynalandı** (commit `0e2a470`):

```
/artefakt/HakHukuk-4B-v0.3-Q4_K_M.gguf
/artefakt/index/mevzuat_bge_m3_s2/{KUNYE.json,gomme.npy}
/artefakt/corpus/mevzuat_maddeler.jsonl
```

**S18 kapısı kuruldu:** korpus artık imajda **ve** volume'de; `indir.py::yerlestir_korpus`
kopyayı imajdaki kaynaktan alır ve **her koşuda `sha256` eşitliğini sınar**, tutmazsa
`KimlikHatasi` → çıkış ≠ 0 ⇒ iki daemon da **hiç başlamaz**. Ölçüldü: imaj = volume = künye
`a35e6efc1612…`.

**Sonuç: uçtan uca HTTP 200**, bağımsız olarak **ikinci, farklı** bir soruyla da doğrulandı
(*"İşveren iş sözleşmesini haklı nedenle nasıl feshedebilir?"* → `İŞ KANUNU Madde 25`, 4 atıf,
10 kaynak, doğrulanmış); boş sorgu **422**; model **yeniden inmedi**
(`sha256 755e15e9…86e7bffc` · **2.783.446.720** bayt, birebir). Görev 20 Adım 6 ve Adım 8
kapandı; Adım 8'in *"HENÜZ UÇTAN UCA DOĞRULANMADI"* damgası **ölçülen gerçekle** değiştirildi.

**Üç şerh gizlenmedi:** (a) `git clone` sonrası indeks dizinini **insan doldurmak zorunda** —
G8 bekletiliyor, indeks ne HF'te ne imajda; hata mesajı artık tam yolu ve derinlik şartını
yazıyor, kusur **kapanmadı, görünür oldu**. (b) Korpus artık **üç yerde** (repo · imaj ·
volume); kapı imaj ↔ volume'ü sınıyor, **repo ↔ imaj ayrışması SINANMIYOR** — kalıcı çare
kusur **11**. (c) Uçtan uca doğrulama **iki soru** ile yapıldı; ürün yolunun boş cevap kusuru
(`MODEL_CARD` §7.9) bu koşuyla **ölçülmedi**.

İcra sırasında doğan ikinci `--host` sapması (`app` kutusu, `uvicorn … --host 0.0.0.0`)
insan tarafından **onaylandı** ve ADR-0078'e yazılmak yerine **kendi ADR'sini** aldı:
[ADR-0082](../../adr/0082-app-kutusu-host-sapmasi.md). `api.py` **değiştirilmedi**, erişim
yüzeyi `ports: "127.0.0.1:8000:8000"` ile aynı kaldı, **S9 yine açılmadı**.

---

## 6. GÖZ KAPISININ BİLANÇOSU — bu kaydın asıl dersi

Üç insan gözü kapısı geçti — **G12** (Adım 6-7) · **G21** (Adım 11) · **G19** (Adım 6) — ve
**süit YEŞİLKEN duran dört kusuru** yakaladılar — ⚠️ **DÜZELTME 2026-09-12:** burada önce *"273 test yeşilken"* yazılmıştı ve **yanlıştı**; dördü aynı ana ait değil. Doğrusu commit sırasından okundu: **26** ve **27** süit **267** yeşilken duruyordu (`faad932` ↔ `063330c`); **28** süit **273** yeşilken (`6a58d72` sonrası); **30** süit **274** yeşilken (`8e8e385` sonrası). Tek bir yuvarlak sayıya bağlamak üçünü de yanlış anlatır

| kusur | ne | niçin test görmedi |
| :-- | :--- | :--- |
| **26** | sunumda **çift tırnak**: model işaretlerin içine kendi düz tırnağını da yazınca `“ "…" ”` çıkıyor | **Bu kusuru AYNI GÜN BİZ EKLEDİK** (kusur 12a/19 süzgeci) ve testlerimiz **tırnaksız** alıntıyla yazıldığı için bu hâli görmemişti. TDD ile kapatıldı, commit `6a58d72`, +6 test |
| **27** | Kaynaklar listesinde madde biçimi tutmuyor — `MADDE 349` · `Madde 8` · `MADDE 16` yan yana | Korpusun **ham** tutarsızlığının vatandaş ekranına yansıması; ham alan bilerek korunuyor. Kayda geçti, **AÇIK** |
| **28** | `hakhukuk-api` / `hakhukuk-tui` / `hakhukuk` komutları **çalışmıyordu** | İki ayrı sebep: (1) paket venv'e **hiç kurulmamıştı**; (2) **latent kusur** — `license = "Apache-2.0"` PEP 639 **dize** biçimidir, `build-system.requires` yalnız `setuptools>=68` diyordu ve kurulu **70.2.0** o biçimi **reddediyor** ⇒ yalıtımlı kurulum çalışıyor (pip en yeni setuptools'u çeker), **`--no-build-isolation` kurulumu PATLIYORDU**. `setuptools>=77` yazıldı ve `tests/test_belgeler.py::test_build_system_license_bicimiyle_TUTARLI` bunu **kapı** olarak çiviledi |
| **30** | `cli.py` künye yolunu **repo köküne göreli** çözüyordu ⇒ `site-packages`'e kurulunca bulunamıyor, kapsam satırı **sessizce** *"künye okunamadı — sayı belirsiz"*e düşüyor | **Bu kusuru da AYNI GÜN BİZ EKLEDİK** (G21 Adım 7). **Konteynerin İÇİNDE** yakalandı; host'ta **görünmüyordu**, çünkü paket **editable** kurulu. Onarıldı: künye yolu paketin **içine** göre çözülüyor, commit `91cd0af` |

Dördünden **ikisi** (26 ve 30) **bizim aynı gün yazdığımız koddandı**.

---

## 7. Turun sayıları

| eksen | değer | kaynak |
| :--- | :--- | :--- |
| test | **178 → 281 yeşil, 2 xfail** | `python -m pytest -q` (2026-09-12); 283 toplanan |
| commit | bu kaydın kapsadığı **31** (`2d83c5d..4a56f78`); turun tamamı **50** | `git rev-list` |
| push | **YAPILMADI** — `origin/master`'a göre 60 gönderilmemiş commit | `git rev-list --count origin/master..HEAD` |
| harcanan | **$0,045067** (G22 Adım 2'nin hakem koşusu; bu kaydın işleri **$0**) | OpenRouter `total_usage` önce/sonra |
| plan paydası | **88 → 114/115 kutucuk** | plan `İCRA DURUMU` satırı, git geçmişi |
| ADR | **0079 · 0080 · 0081 · 0082** | `docs/adr/` |
| tuzak | **1.11 · 1.12 · 1.13** | `docs/record/yurutme-tuzaklari.md` |
| açık kusur kaydı | **13 → 32 kalem**; açık kalanlar **5a · 23 · 24 · 25 · 27 · 29**, devredilenler **6 · 11 · 12b** | plan, `AÇIK KUSURLAR` |
| ağırlıklar | **değişmedi** | — |

---

## 8. Ders

#66'nın dersi *"ürün yüzeyini temizlemek aygıtta kusur buldu"* idi. **#67'nin dersi bir adım
öteye gidiyor:** bu turda bulunan kusurların **dördü bizim aynı gün yazdığımız koddandı**
(26 · 30 ve bunlara eklenen 21 · 32'nin tetiklediği düzen) ve **hiçbirini test yakalamadı** —
çünkü testler, kusurun **görülmediği** varsayımla yazılmıştı: alıntı testi **tırnaksızdı**,
kurulum testi **editable** kurulumun altında koşuyordu, yol testi **repo ağacının** içinden
bakıyordu. Kapıların yakaladığı şey **kodun yanlışlığı değil, TESTİN KÖRLÜĞÜ**ydü; test bir
varsayımı paylaştığı sürece o varsayımı sınayamaz. Ve bir onarımın (`G8 Adım 1b`) başka bir
düzeni kırması, *"onarım da bir değişikliktir ve kendi regresyonunu ister"* kuralının bu
hattaki **üçüncü** kanıtıdır.
