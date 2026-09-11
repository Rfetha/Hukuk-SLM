# #66 — Ürün yüzeyi temizlendi; temizliğin kendisi aygıtta üç yeni kusur buldu

**Tarih:** 2026-09-11 · **Bedel:** **$0** — hakem hiç çağrılmadı, kütle hesaplanmadı;
tek donanım gideri yerel GPU (bir üretim koşusu, 42 dk 13 sn).
**Çıktılar:** [`outputs/eval/g21-zayif-eslesme/`](../../../outputs/eval/g21-zayif-eslesme/) ·
[`outputs/eval/g22-kv-fp16/`](../../../outputs/eval/g22-kv-fp16/)
**Kararlar:** [ADR-0079](../../adr/0079-zayif-eslesme-rozeti-eklenmedi.md)
**Commit aralığı:** `b0c5acd..5030886` (11 commit)
**Plan:** [`plans/2026-09-07-hp-hat-a-hat-b.md`](../../superpowers/plans/2026-09-07-hp-hat-a-hat-b.md)
Görev 20 (Adım 1-5) · Görev 21 (Adım 1-10) · Görev 22 (Adım 1)

> **Turun tek cümlesi:** *ürün yüzeyi temizlendi; temizliğin kendisi, ölçüm aygıtında üç yeni
> kusur buldu.* Ağırlıklara dokunulmadı, yayımlanmış hiçbir sayı değişmedi.

---

## 1. Görev 21 — ürün yüzeyi kusur temizliği (TDD, 10 kırmızı → yeşil)

Plan'ın `AÇIK KUSURLAR` bölümündeki on üç kusurun dokuzu *$0 ve küçük* diye ayrılmıştı. Bu tur
onları kapattı: **boş sorgu kapısı** (kusur 4, `servis.answer()` içinde — arayüzlerde değil,
uydurulmuş uzunluk eşiği **yok**) · **iskele işareti süzgeci** (kusur 12a, yalnız sunum
katmanında; `Cevap.metin` **ham** kalır) · **`madde_sayisi` türetilmiş alanı** (kusur 13, ham
`madde_no` korunur) · **TUI donması** (kusur 3, çalışan iş parçacığı) · **açılış yönergesi +
statik kapsam satırı** (kusur 8 ve 5b; sınıflandırıcı **kurulmadı** — yanılan bir kapsam
sınıflandırıcısı vatandaşa *"bu konu kapsamda yok"* diyerek cevabı olan soruyu öldürür).

Kırmızı-yeşil zinciri kayıtlı: `tests/test_kusurlar.py` 15 testle açıldı, **10'u kırmızı
görüldü** (`.superpowers/sdd/g21/adim-1-2-report.md`); tur sonunda takım
**178 → 216 yeşil, 2 xfail** (taban: `adim-6-7-report.md`; kapanış:
`.superpowers/sdd/g21/duzeltme-report.md` ve `python -m pytest -q --co` → 218 toplanan).

## 2. Asıl ders: testler yeşilken duran **dört** "hata vermeden yanlış"

Adım 10 yeşildi, şartname uyumu dört kilitli kararda da tamdı — ve bağımsız kod incelemesi
(`.superpowers/sdd/g21/inceleme-report.md`) yine **dört ayrı sessiz yanlış** buldu. Hiçbirini
test yakalamamıştı, çünkü hiçbiri **hata vermiyordu**:

| # | bulgu | kanıt | sonuç |
| :-- | :--- | :--- | :--- |
| 1 | `tui.py` `bicimle()`'yi hiç çağırmıyordu ⇒ `##begin_quote##` **vatandaşa gidiyordu** | `tui.py` kendi sunum dizesini ayrı bir `ROZET` sözlüğüyle kuruyordu | süzgeç `cli.py`'den **import** edildi (kopyalanmadı), `is` testiyle çivilendi |
| 2 | Kapsam satırı *"40.496 madde"* diyordu; retriever **mülgayı eliyor** | `data/corpus/KUNYE.json`: `n_madde 40496` − `n_mulga 2547` ⇒ **37.949** | doğru sayı künyeden **türetiliyor**, koda gömülmüyor |
| 3 | `madde_sayisi` *"Geçici Madde 1"* ile *"Madde 1"*i **aynı sayıya** indiriyordu | `madde_anahtar.py`'nin başlığı bunu açıkça yasaklıyor: karışırsa `recall@k` şişer ve **hiçbir yerde hata çıkmaz** | önekli biçimler artık `None` döner |
| 4 | TUI'de iki ardışık Enter **iki çalışan** başlatıyordu; son biten kazanıyordu ⇒ ikinci sorunun altında **birinci sorunun cevabı** | `@work(thread=True)` `exclusive` **olmadan**, `servis`'in modül düzeyi tekilleri **kilitsiz** | `exclusive=True` + koşu sürerken girdi kapalı |

Aynı incelemede alıntı sınırı da düzeltildi: `##begin_quote## … ##end_quote##` **silinmek**
yerine tipografik tırnağa çevrildi — işaretler gürültü değil, *"burası kanunun kendi
cümlesidir"* sınırıdır; silmek kanunun lafzı ile modelin yorumunu tipografik olarak
ayırt edilemez hâle getiriyordu. `scripts/` ölçüm hattına **dokunulmadı**
(`score_register.py:41` aynı işareti register göstergesi olarak sayar).

**Kök neden kayda geçti (açık kusur 17):** `tui.py` ve `cli.py` **iki paralel sunum
katmanıdır**. Bu turun iki sızıntısı (iskele işareti · kapsam satırı) tek tek kapatıldı,
kök neden **duruyor** — bir sonraki sunum kuralı yine yalnız bir yüzeye uygulanacaktır.
Aynı incelemeden üç yeni kusur daha doğdu: **14** (`madde_sayisi` ölü alan) · **15**
(kapsam satırı yalnız TUI'de) · **16** (boş sorgu rozeti gövdesini yalanlıyor).

## 3. Görev 21 Adım 8 — ön-kayıtlı **ÖLÇÜM**: rozet EKLENMEDİ

Kusur 5a (*"erişim başarısız olduğunda kullanıcıya sinyal yok"*) için eşik **ölçüme
bağlanmıştı**: `recall@10`'un kaçırdığı kalemlerle tutturduklarının skor dağılımı ayrışmazsa
**rozet yoktur**. Ölçüldü — `scripts/erisim_korpus/zayif_eslesme_olc.py`, n=80 DEV, CPU,
65,7 s, **$0**, hakemsiz (`outputs/eval/g21-zayif-eslesme/KUNYE.json`).

**Rejim çıpası tuttu:** aynı koşuda `recall@10` **0,9500 (76/80)** ölçüldü ve çıpayla
(`outputs/eval/f02-biz-onsozsuz/KUNYE.json`, `recall_at_10`) **birebir** aynı çıktı
(`cipa_tutuyor_mu: true`) ⇒ ayrışmanın yokluğu **ölçümün kusuru değil**.

Altı aday göstergenin hiçbiri ayırmıyor (`outputs/eval/g21-zayif-eslesme/BULGU.md`, ham veri
`skorlar_80.json`). En iyi aday `ortalama_skor`'da dört kaçağın **dördünü birden** yakalayan
eşik (`≤ 0,09721`) aynı anda doğru getirilmiş **23/76** kalemi *"zayıf eşleşme"* diye
damgalardı; diğer beş göstergede bedel 53 · 56 · 57 · 59 · 60 yanlış pozitiftir.
`marj_1_2` ve `entropi`'de kaçırılanların **medyanı daha iyi** — retriever yanılırken de
kendinden emin görünüyor.

**Kaçırılan dört kalem:** `5237/Madde 89` · `5237/Madde 103` · `6284/MADDE 10` · `6098/MADDE 99`.

**n=4 damgası zorunlu.** Dört kalemden türetilecek her eşiğin güven aralığı berbattır; tek
kalemin konumu değişse görüntü değişirdi. Söylenen şey dar ve kesindir: **eldeki dört örnekte
ayrışma yok.** Eşik **uydurulmadı**, **kusur 5a AÇIK KALIR** — ve bu bir **bulgudur**,
başarısızlık değil. Karar: [ADR-0079](../../adr/0079-zayif-eslesme-rozeti-eklenmedi.md).

Aynı belgenin kendi iki **yorum** cümlesi tablolarıyla çelişiyordu (inceleme bulgusu B7) —
`entropi` yüzdeliği ve HÜKÜM parantezi. Sayı tabloları ve hüküm **değişmedi**; iki gerekçe
cümlesi verinin desteklediğiyle değiştirildi ve her sayı `skorlar_80.json`'dan yeniden
hesaplandı. Bu hattın kuralı: **çelişki damgalanır, sessizce düzeltilmez.**

## 4. Görev 20 — konteyner rejim kilidi (Adım 1-5)

Paketleme burada kolaylık değil, **rejim kilididir**: bağlayıcı llama.cpp bayrakları bugüne
kadar yalnız düz metin olarak üç belgede yazılıydı. `compose.yaml` onları zorlayan ilk
artefakttır ([ADR-0078](../../adr/0078-konteyner-dagitimi-rejim-kilidi.md)).

- Testler compose'u **`yaml.safe_load` ile ayrıştırarak** sınıyor, metin araması yapmıyor;
  indirme kapısı ağsız (monkeypatch). Kırmızı koşu **12 hata** görüldü, kapanışta
  **207 yeşil, 2 xfail** (commit `c234313`).
- Bağlayıcı bayraklar birebir taşınıyor, tek izinli sapma `--host 0.0.0.0`, yayın yalnız
  `127.0.0.1`. İki temel imaj da **pinli**.
- **İkinci bir `--host` sapması doğdu** (`app`/uvicorn) ve kilitli beş kararda **yoktu** —
  gerekçesi `llama` sapmasıyla aynı sınıftan, ama karar metni onu kapsamıyor; **insan damgası
  bekliyor**. Ürün kodu (`api.py`) değiştirilmedi, erişim yüzeyi genişlemedi.
- **Adım 4'ün iki boyut tahmini ölçümle düzeldi** (`du -sb`, tahmin değil): `models/**`
  **79.639.851.820 B = 74,2 GiB** (plan metni *"2,6 GB"* diyordu — o tek GGUF'un boyutuydu) ·
  indeks `.npy` iki dosya **165.871.872 B = 158,2 MiB** (*"79 MB"* tek dosyaydı).

## 5. Görev 22 Adım 1 — KV kuantizasyonu 80 kalemde, hakemsiz, **$0**

Kusur 2 (*"sunucu yapılandırması cevabı değiştiriyor, etkisi ölçülmedi"*) bugüne kadar **tek
soruda** gözlenmişti. 80 kalemde ölçüldü: aynı GGUF, aynı seed 3407, aynı bütçe, aynı indeks;
düşen **tek bayrak çifti** `--cache-type-k/-v q8_0` ⇒ llama.cpp varsayılanı `f16/f16`
(`outputs/eval/g22-kv-fp16/KUNYE.json`, `KARSILASTIRMA.md`).

| eksen | çıpa `q8_0` | yeni `f16` |
| :--- | ---: | ---: |
| **bayt olarak değişen cevap** | — | **65 / 80** (%81,2) |
| karakter medyanı | 715,0 | 706,5 (**−%1,2**) |
| `completion_tokens` medyanı | 731,0 | 718,5 (−%1,7) |
| kalem başına mutlak fark medyanı | — | 47,5 karakter / 18,5 token |
| çekinme (`exact_reject`, `mode="data"`) | 5 / 80 | 5 / 80 |
| tamamen boş cevap | 0 / 80 | 0 / 80 |
| `forced_close` | 3 / 80 | 3 / 80 |
| `finish_reason == "length"` | 4 / 80 | 3 / 80 |
| durum sınıfı `CEVAP / CEKINCELI / SUSKUNLUK / KESIK` | 70 / 1 / 5 / 4 | 71 / 1 / 5 / 3 |
| katı atıf kapısından reddedilen | **0** | **3** |
| **uydurulmuş madde numarası** | **0 / 114** | **0 / 152** |

**Manşet: cevapların %81,2'si bayt olarak değişti, buna karşılık hiçbir sayaç birden fazla
kalem oynamadı.** Toplulaştırılmış eksenler kıpırdamadı, kalem düzeyi büyük oynadı: **6/80**
kalem ürün durum sınıfı değiştirdi ve toplam uzunluk farkını **dört kalem** taşıyor
(`id 25` · `41` uzadı, `75` · `69` kısaldı; `25` ve `41` yinelemeli döngüye girip bütçeyi
tüketiyor — **döngü sınıfı iki rejimde de var, değişen hangi kalemin döngüye girdiğidir**).

**Kütle üzerine cümle KURULMADI** — kütleyi hakem üretir, hakem para ister, para kapısı
Adım 2'nin **insan kararıdır**. Bedel girdisi ölçüldü ve uydurulmadı: çıpanın gerçek hakem
bedeli **$0,0417** (`outputs/eval/f02-biz-onsozsuz/hakem.log`), fp16 kolunun düz tahmini
**$0,042**, **%50 emniyet paylı üst sınır $0,063** — bakiye $2,20'nin %2,9'u.

**Kusur 2 kaydının tek-soruluk gözlemi ÇÜRÜDÜ.** Kayıt `SUSKUNLUK → CEKINCELI` geçişi
gözlemişti; 80 kalemin **hiçbirinde tekrarlanmadı**. `CEKINCELI` sayısı iki koşuda da **1** ve
**aynı** kalemdir; gözlenen altı geçişin hepsi `KESIK` ekseninde toplanıyor. Tek soruluk
gözlem genel kural değilmiş.

Çekinme sayısı iki koşuda da 5, ama **bileşimi farklı**: altın bağlamdayken susma (aşırı-red)
**4 → 3**, altın gelmediği için susma **1 → 2** (`harness_tablo.json` erişim-davranış çaprazı
bunu bağımsız doğruluyor). Taraf değiştiren iki kalem gözle okundu.

**fp16'nın ürettiği, çıpada hiç görülmeyen bozulma sınıfı** (açık kusur 19): model istem **yer
tutucusunu harfiyen bastı** — *"(KANUN ADI, Madde 13)"* — **0/80 ↔ 2/80** (`id 23` · `36`,
gözle doğrulandı). Yani *"KV kuantizasyonu manşet dağılımı bozmuyor"* denebilir;
*"cevaplar aynı kalıyor"* **denemez**.

**Kontrol değişkeni sızıntısı — şerh.** Çıpa ile yeni koşu **2 kalemde** (`id 7` · `63`) farklı
kaynak gördü. Sebep KV değil, çıpadan **sonra** gelen yürürlük süzgecidir (`63b691e`,
2026-09-07): düşen iki kaynak `İŞ KANUNU Madde 111` (1475) ve `Madde 87` (4857), ikisi de
korpusta `mulga: True` — CLAUDE.md'nin kaydettiği *"800 kaynağın 2'si mülgaydı"* ölçümüyle
**aynı iki kalem**. Altın madde iki koşuda da ilk 10'da kaldı, sayaçların hiçbirini
etkilemiyorlar; ama *"tek değişken KV"* cümlesi **tam doğru değildir** ve temiz alt küme
n=78'dir.

## 6. Turun en pahalı bulgusu: ölçüm aygıtında **üç yeni kusur**

Üçü de bu hattın kendi failure class'ı — *"hata vermeden yanlış"* — ve üçü de
[`yurutme-tuzaklari.md`](../yurutme-tuzaklari.md)'ye yazıldı.

**Tuzak 1.11 — duman koşusundan doğrusal maliyet tahmini kapı kurmuyor.** Rakip havuzuna yeni
özne eklenirken (#65) 5 kalemlik duman koşusundan ×16 doğrusal ekstrapolasyonla **$0,82**
tahmin edilmişti; tam koşu **$1,1932** tuttu, ön-kayıtlı **$1** kapısı **%45** aşıldı. Kural
yazıldı (kod değil): duman koşusu ya **tabakalanmış** seçilir ya kapıya **%50 emniyet payı**
konur.

**Tuzak 1.12 — künyenin KV satırı SABİT DİZE.** `cp0_thinking_gen.sh:89` künyeye
`KV q8_0/q8_0` diye **sabit metin** basıyor; aynı satırdaki `$CTX` · `$NGL` · `$PORT` ·
`$EXTRA_ARGS` değişkenken KV değil. Betik `SERVER_URL` ile dış bir sunucuya bağlandığında o
sunucunun KV ayarını **hiç okumuyor**. Bu koşunun `kosu.log`'u **`q8_0` dedi, gerçek `f16`
idi** — yani kıyasın ölçmek için var olduğu **tek değişken** künyede yanlış görünüyordu.
Yakalayan şey künye değil, `/proc/<pid>/cmdline` okumasıydı; bağımsız ikinci kanıt sunucu
günlüklerinden geldi (atılan istem önbelleği girdisi medyanı **257,2 → 306,8 MiB, ×1,19**).
**İroni aynı betiğin iki satır üstünde yazılı:** *"künyede görünmeyen bayrak sessizce düşer,
koşu geçerli görünür."* Genel kural: künyedeki her alan ya bir **değişkenden** ya bir
**ölçümden** gelir; elle yazılmış bir alan künyeyi **kanıt olmaktan çıkarır**.

**Tuzak 1.13 — atıf doğrulayıcı kanun adını GEVŞEK eşleştirip YANLIŞ kanuna çözüyor.**
*"Gelir Vergisi Kanunu Madde 73"* atfı `kanun_no 1319` = **EMLAK VERGİSİ KANUNU** diye
çözüldü, 73 orada bulunamadı ve `MADDE_YOK` = **uydurma** damgası yedi. Oysa madde korpusta
**VAR**: `193 / Madde 73`, adı *"GELİR VERGİSİ KANUNU (G.V.K.)"* — parantezli sonek eşleşmeyi
bozuyor ve korpusta **16 kanun** parantezli ad taşıyor (`data/corpus/mevzuat_maddeler.jsonl`
üzerinde sayıldı). Doğrudan koşularak kanıtlandı.

**Bu alet, yayımlanan `0/114` manşetini üretendir.** Çıpa koşusunda `MADDE_YOK` **hiç yok**
(114/114 `DOGRULANDI`) ⇒ manşet **yanlış-pozitif yönünden temizdir**. Fakat aynı gevşeklik
**ters yönde** de çalışabilir — yanlış çözülen bir kanunda aynı numaralı bir madde varsa atıf
**yanlış `DOGRULANDI`** alır ve uydurma sayısı **iyimser** okunur — ve **o yön
ÖLÇÜLMEMİŞTİR**. Çürütülen bir şey yoktur; **ölçülmemiş bir yön** vardır. Çıpanın 114 atfının
**2'si** adı birebir tutmayan bir kanuna çözülüyor (*"Mülkiyet Kanunu"* → `6769`,
*"Yayın Hizmetleri Hakkında Kanun"* → `6112`); ikisi de makul, ama eşleştirme birebir değil.
Açık kusur **18**.

## 7. Ders

**Bu turda ürün yüzeyinde kapatılan her kusur, aygıtta bir kusur açığa çıkardı — ve hiçbirini
sayısal bir kapı yakalamadı.** Dördünü **kod incelemesi** yakaladı (testler yeşilken), üçünü
**künyeyi ya da aletin kendisini doğrudan koşturmak**. Kapılar geçilmişti: Adım 10 yeşildi,
şartname uyumu tamdı, geçerlilik kapısı geçiyordu, künye dolmuştu.

Kayıt eşlemesi: methodology (ölçüm aygıtının kendi kusurları) · negatif bulgu (rozet eklenmedi,
tek-soruluk KV gözlemi çürüdü) · limitations (kusur 17 · 18 · 19 açık).
