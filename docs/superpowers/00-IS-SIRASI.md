# `docs/superpowers/` — iş sırası

> Bu klasörün **giriş dosyası**. Neyin ne zaman koşacağını söyleyen TEK yer.
> *(`00-` öneki kasten: dosya adı sıralamasında `plans/` ve `specs/`'in **üstüne**, listenin
> en başına çıksın diye. 2026-09-08'de kısa bir süre `README.md` idi — GitHub klasör görünümü
> için doğruydu ama IDE ağacında en dibe düşüp adını kaybediyordu; günlük bakılan yer IDE.)*

> **Bu dosya bir HARİTA, bir plan değil.** Kutucuk taşımaz. Söylediği tek şey: *elimdeki altı
> belgeden hangisi şimdi, hangisi sonra, ve hangisi neyi bekliyor.*
> Sıra **insan tarafından kilitlendi** (2026-09-07). Bir planın *içindeki* adım sırası o planın
> kendi meselesi; burası **planlar arası** sırayı bağlar.
>
> Bir belgeyi sıradan çıkarmak ya da araya sokmak **insan kararıdır** — kendi başına yapma.

---

## Bir bakışta

| plan | durum |
| :--- | :--- |
| [`2026-09-06-faz0-olcum-zinciri.md`](plans/2026-09-06-faz0-olcum-zinciri.md) | **KAPANDI** 48/48 · $1,47 |
| [`2026-09-07-hp-hat-a-hat-b.md`](plans/2026-09-07-hp-hat-a-hat-b.md) | **KAPANDI 2026-09-12** · **115/115** · $0,045067 |
| [`2026-09-08-mevzuat-kapsam-ve-tazelik.md`](plans/2026-09-08-mevzuat-kapsam-ve-tazelik.md) | ⏭️ **SIRADAKİ** — **62 kutucuk AÇIK**, hiç başlanmadı |

**Kapanan planın devir tablosu onun kendi KAPANIŞ bloğundadır** — sıradaki plan açılmadan
önce oradan okunur. Kapanan plan **yeniden işletilmez**; devamı yeni planda yaşar.

### `hp` → Hat A → Hat B — kapanış künyesi *(2026-09-12)*

```
kutucuk      115/115          test        164 → 281 yeşil, 2 xfail
commit       62 · PUSH EDİLDİ (origin/master, 2026-09-12)
harcanan     $0,045067        sürüm       v0.3 · artefakt HakHukuk-4B-v0.1
yazılanlar   ADR 0074-0082 · kayıt #64-#67 · tuzak 1.11 · 1.12 · 1.13
```

| ne yapıldı | sonuç |
| :--- | :--- |
| **hakem paneli** (G1·G3) | κ **ilk kez ölçüldü** — `tam_sadık` **0,534** < 0,6 ⇒ **`v1.0` VERİLMEDİ**, `v0.3` (ADR-0077) |
| **rakip havuzu** (G4) | Sonnet-5 girdi ve **ÖNDE**: kütle **0,8348** ↔ bizim **0,8011** |
| **kabul testi** (G16) | donmuş TEST **tek kez** açıldı — kütle **0,5804**, tavan `recall@10` **0,7500** |
| **ürün katmanı** (G5-G12·G19) | `hakhukuk/` paketi: istem · tipler · terazi · servis · CLI · TUI · HTTP API |
| **araç katmanı** (G18) | 5 kaldıraç · sınırlı döngü · regresyon **80/80 birebir** |
| **ürün yüzeyi** (G21) | 7 kusur kapandı · üç göz kapısı da **GEÇTİ** |
| **rejim + KV** (G22) | ürün yolu ölçüm hattının rejimine geldi ⇒ **boş cevap 4/80 → 0/80** (ADR-0080) |
| **konteyner** (G20) | `docker compose up` **uçtan uca çalışıyor** · imaj **2,13 GB** · torch **CPU** |

### Bu turun üç dersi

**① Ürün yüzeyini temizlemek ÖLÇÜM AYGITINDA kusur bulur.** En ağırı: atıf doğrulayıcı kanun
adını gevşek eşleştirip **yanlış kanuna `DOGRULANDI`** basıyordu (tuzak **1.13**). Onarıldı
(**7/16 → 0/16**) ve çıpalar yeniden puanlandı: `0/114` ve donmuş TEST `0/52` **oynamadı** —
ama korunmanın **aletten değil ÖRNEKLEMDEN** geldiği ortaya çıktı.

**② Aleyhe çıkan sonuç da yazılır.** İnsan kararıyla rakipler de yeniden puanlandı:
`3.1 Flash-Lite` **1/152 → 0/153**. Tek deterministik üstünlüğümüzde artık **eşitiz**;
karşılığında **eşit sınav** alındı (ADR-0057). Sayı `MODEL_CARD` ve `CLAUDE.md`'de değişti.

**③ Sayısal kapı TESTİN KÖRLÜĞÜNÜ görmez.** Üç insan gözü kapısı, **süit yeşilken duran dört
kusuru** yakaladı — çift tırnak (**26**) · madde biçimi (**27**) · `hakhukuk-api` çalışmıyor
(**28**) · künye yolu (**30**). **İkisi aynı gün bizim yazdığımız koddandı** ve testler onları
görmedi çünkü kusurun *görülmediği* varsayımla yazılmışlardı (tırnaksız alıntı · editable
kurulum · repo ağacı). *(Süit o anlarda sırasıyla **267 · 267 · 273 · 274** yeşildi;
bir ara burada tek sayı olarak "273" yazılmıştı, **yanlıştı**, 2026-09-12'de düzeltildi.)*

### Açık kusurlar — **32 kayıt**, kutucuk taşımaz

| durum | sayı | hangileri |
| :--- | ---: | :--- |
| **kapandı** | **23** | 1 · 3 · 4 · 5b · 7 · 8 · 9 · 10ᵖ · 12a · 13 · 14 · 15 · 16 · 17 · 18 · 19 · 20 · 21 · 22 · 26 · 28 · 30 · 32 |
| **devredildi** | **3** | **6** → `v2`/`B1` · **11** → kendi turu · **12b** → `v2`/`B11` |
| **açık** | **8** | **2ᵏ** · **5a** · 23 · 24 · 25 · 27 · 29 · 31 |

ᵖ kusur **10**'un `push` yarısı kapandı (62 commit gitti); **HF görünürlüğü** yarısı **insan
kararı** olarak açık. ᵏ kusur **2** ölçüldü ve `q8_0` kararına bağlandı; satırı kayıt olarak durur.

**Tam metin ve devir gerekçeleri:** kapanan planın
[AÇIK KUSURLAR](plans/2026-09-07-hp-hat-a-hat-b.md#açık-kusurlar--kayıt-ve-devir) bölümü ve
[KAPANIŞ](plans/2026-09-07-hp-hat-a-hat-b.md) bloğu. **Devredilmemiş açık kusur YOKTUR** ⇒
kapanış geçerlidir.

### Kapanış *"ürün bitti"* DEMEZ

`v1.0` verilmedi ve sebebi değişmedi: **engel model değil ÖLÇÜM AYGITIDIR** — her sayı hâlâ
**tek hakem ailesinin** hükmü, κ **0,534** ([ADR-0077](../adr/0077-v1-0-verilmedi-v0-3.md)).
Bu turda aygıtta **üç yeni kusur** bulunması o teşhisi **güçlendirdi**.

## `v1` ↔ `v2` çizgisi — insan kararı 2026-09-08 ([ADR-0075](../adr/0075-v1-sft-kapanir-v2-sequential-rl.md))

```
v1   ham base ──► SFT (τ_g) + ORPO (τ_a) ──► ham TIES ──► tgta_v1 ──► YAYIN
v2   tgta_v1 (bf16) ──► GRPO + düşünce (thinking) ayarı ──► v2.0
```

**`v1` SFT ile KAPANIR** — `B1`/`B4` eğitim turları koşulmaz. İkisinin de gerekçesi ölçülmüş
ve **birbirinden farklı**: `B1`'de rakiplerden **geride değiliz** (8/80 ↔ 8·8·7·8) ve otomatik
metrik yok; `B4` ise bir **merge** kaybı (`τ_a` tek başına 0,987) ve `v2`'de merge olmadığı
için **konusuz** kalıyor.

### Araç katmanı `v1`'e dahil — [ADR-0076](../adr/0076-kapi-kaldirac-ayrimi-arac-katmani.md)

**KAPI ↔ KALDIRAÇ ayrımı:** atıf doğrulama · mülga süzgeci · durum sınıflandırma **TOOL
DEĞİLDİR** — döngünün dışında **koşulsuz** çalışır (uydurulmuş madde **0/114** garantisi
oradan gelir). Model yalnız **deterministik kaldıraçları** çağırır: `ara` · `madde_getir` ·
`madde_var_mi` · `kanun_bul` · `yururlukte_mi`.
Döngü **sınırlı** (`AZAMI_ADIM`) ve sınıra dayanmak **görünür**: `Durum.ARAMA_TUKENDI`.
Sebep: bu hattın en pahalı hata sınıfı *"hata vermeden yanlış"* — 17 tuzağın **hepsi** o
sınıftan, ve agentic akış tam o riski büyütür.
**Kapı koşusuna GİRMEZ** (ADR-0076 m.4): %80,1 ve eşik **araçsız** ölçüldü, rakipler araç
kullanamaz ⇒ araçlı koşmak ADR-0057'nin eşit sınavını ihlal eder. Sıra: **kabul testi →
araç katmanı → yayın.**
`v1`'de araç kullanımı **istem katmanındadır** (eğitilmedi, güvenilirliği düşük olacak);
**öğrenilmesi `v2`'nin işi** — GRPO ödülüne *"doğru aracı doğru anda çağırdı mı"* girer.
~~**CLI + TUI yeterli** (insan kararı) — HTTP API ve web arayüzü `v2`.~~
**BU CÜMLE 2026-09-09'da DEĞİŞTİ (insan kararı):** HTTP API `v1` tarafına alındı ve ana plana
**Görev 19** olarak girdi. Gerekçe teknik değil, tercihtir; öyle yazılıyor.
**S9 açılmadı:** API **yerel ve tek kullanıcı** (`127.0.0.1`, kimlik yok, hız sınırı yok).
Barındırma, mahremiyet vaadi ve TR IP kısıtı soruları `v2`'de açık duruyor. Web arayüzü hâlâ `v2`.

**2026-09-10'da ikinci kez genişledi (insan kararı):** **konteyner dağıtımı** da `v1` tarafına
alındı ve ana plana **Görev 20** olarak girdi ([ADR-0078](../adr/0078-konteyner-dagitimi-rejim-kilidi.md)).
**Konteyner web arayüzü değildir**; *"web arayüzü hâlâ `v2`"* cümlesi **yürürlükte kalır** ve
**S9 yine açılmadı** — `llama` yalnız iç ağda, `app` yalnız `127.0.0.1`'e yayımlanır.
Gerekçe bu kez teknik ve **ölçülmüş**: ticket 2, sunucu bayrağının **cevabı değiştirdiğini**
gösterdi (`q8_0` ↔ fp16, aynı seed, farklı `sha256`), ve bağlayıcı yapılandırmayı bugün hiçbir
şey zorlamıyor. `compose.yaml` onu zorlayan **ilk artefakttır** — paketleme burada kolaylık
değil, **rejim kilidi**.

**Bedeli:** `τ = θ_ft − θ_base` tanımı tüm kolların aynı base'i paylaşmasını şart koşar ⇒
`tgta_v1`'i yeni başlangıç almak bunu bozar ⇒ **ADR-0027'nin task-vector hattı `v1`'de
DONDURULUR**, `v2`'ye taşınmaz. `v2`'nin iddiası merge değil **RL kazancıdır**.
`B1` ve `B4` **borç olarak açık kalır** — koşulmadılar, ne verecekleri **bilinmiyor**.

---

## Görev 8 nedir — *"kullanıcı indeksi nereden alacak"*

Retriever olmadan ürün yok, ve retriever **indeks** olmadan çalışmaz. Ama indeks ikili bir
dosya ve **git'te değil**:

| | |
| :--- | :--- |
| indeks | `data/index/mevzuat_bge_m3_s2/gomme.npy` = **79 MB** |
| git'te mi | **hayır** — `.gitignore:166` `data/index/**/*.npy` |
| korpus | `data/corpus/mevzuat_maddeler.jsonl` = 37 MB, git'te **var** |
| sıfırdan üretmek | 40.496 maddeyi `bge-m3` ile gömmek: GPU ~10 dk, **CPU ~2 sa 45 dk** |

⇒ `git clone` yapan biri **çalışan bir ürün elde etmiyor**. Görev 8 bu boşluğu kapatıyor:
`hakhukuk/kurulum.py` indeksi **HF dataset'ten indirir** (karar S8 → **(a)**, 2026-09-07).

## Neden Görev 8 bekliyor — tek sebep, ölçülmüş

Görev 8 *"indeksi kullanıcıya nasıl dağıtırız"* sorusunu kapatıyor. Bugün cevabı yazsak
**yanlış boyutu** paketlemiş oluruz:

| | bugünkü korpus | insan kararıyla genişleyen korpus |
| :--- | ---: | ---: |
| belge | 892 | **9.722** |
| madde | 40.496 | **340.303** (8,4×) |
| indeks | 83 MB | **~697 MB** |

83 MB'ı HF dataset'e koymakla 697 MB'ı koymak **aynı iş değil** (S8'in *"(b) kurulumda üret"*
seçeneği bu yüzden öldü: gömme CPU'da ~23 saat). ⇒ Görev 8, korpus kararı koda dökülmeden
koşmaz. Kaynak: [spec §7b](specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md).

### Ama iki iş BEKLEMEZ — ikisi de doğruluk meselesi, boyut meselesi değil

| iş | neden beklemez |
| :--- | :--- |
| **Görev 8b** · mülga madde süzgeci | Bugün 800 getirilen kaynağın 2'si **yürürlükten kalkmış** madde ve vatandaşa gidiyor. Bu eksik özellik değil, **YANLIŞ CEVAP**. Korpus büyüyünce sayı da büyür — erken düzelt. |
| **Görev 8 Adım 1b** · `KUNYE` taşınabilirlik kilidi | **BİTTİ 2026-09-09.** `KUNYE.json` mutlak yol + `mtime` damgalıyordu ve `retriever.py` bunu yüklemede doğruluyordu ⇒ `git clone` sonrası her makinede `SystemExit`. Yol indeks dizinine **göreli**, `mtime` vekili **sha256** oldu. Doğrulandı: kopyalanmış ağaçtan yüklendi, `recall@10` **0,9500**. |

---

## Belge belge — ne olduğu ve durumu

| belge | tür | durum | ne der |
| :--- | :--- | :--- | :--- |
| [`plans/2026-09-06-faz0-olcum-zinciri.md`](plans/2026-09-06-faz0-olcum-zinciri.md) | plan | **48/48 KAPANDI** | Ölçüm zinciri onarıldı; v1.0 kapısının üç maddesi de DEV'de sayıyla geçti. Aletin **beş** kusuru bulundu. Artık **kayıt**tır — açılmaz, kutucuğu işaretlenmez. |
| [`plans/2026-09-07-hp-hat-a-hat-b.md`](plans/2026-09-07-hp-hat-a-hat-b.md) | plan | **AÇIK, 88/115** | Yürüyen ana plan. **En üstünde İCRA DURUMU bloğu var — durum oradan okunur.** `v0.2` ve `v0.3` bu planla etiketlendi. İş sırasının yedisinden beşi kapandı. Açık üçü: **SIRA 2** (insan gözüyle TUI doğrulaması), **SIRA 7** (Görev 19 Adım 6 — kod bitti, göz kapısı açık) ve **SIRA 9** (Görev 20, konteyner — Adım 0 GEÇTİ). Plan kapsamı dışındaki on üç kusur da bu dosyanın **sonunda**, kutucuksuz. |
| [`plans/goal-hp-hat-a-hat-b.md`](plans/goal-hp-hat-a-hat-b.md) | başlatıcı | **İCRA MODU 2026-09-10** | Planın `/goal` promptu (3.997 karakter, sınır 4.000). **Tasarım fazı kapandıktan sonra icraya hizalandı**: alt-ajan sürümlü, kapı yoksa otonom akar. Açık beş sıra: **2 · 7 · 9 · 10 · 11**; ikisi (2 ve 7) insan gözü kapısıdır. |
| [`specs/2026-09-06-yeni-belge-katmani-design.md`](specs/2026-09-06-yeni-belge-katmani-design.md) | spec | **plana döküldü** | Ana planın *niye bu sırada* olduğunun gerekçesi. Yeni iş üretmez; sıra tartışılırsa buraya bakılır. |
| [`specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md`](specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md) | spec | **plana döküldü** | Üç kilitli karar (K1 kapsam · K2 anlık görüntü + fark taraması · K3 kapsam kapısı). Plan yazılırken **iki sayısı ölçülerek çürütüldü** ve §7b'ye damgalandı. |
| [`record/2026-09-10-…-kapanan-gorevler.md`](../record/2026-09-10-hp-hat-a-hat-b-kapanan-gorevler.md) | kayıt | **taşındı 2026-09-10** | Ana planın **bitmiş on dört görevinin** tam metni. Plan 2.337 → 1.343 satıra indi; yerlerinde kapanış blokları var. **Plan değildir** — kutucukları tarihseldir, açılmaz. Atlanan (G2·G14·G15) ve bekletilen (G8) görevler **planda kaldı**. |
| [`plans/2026-09-08-mevzuat-kapsam-ve-tazelik.md`](plans/2026-09-08-mevzuat-kapsam-ve-tazelik.md) | plan | **yazıldı, 0/62** | Yukarıdaki spec'in uygulaması. Ana plandan **sonra** koşar. |

---

## Bu sıranın dışında kalanlar

| iş | nerede | neden dışarıda |
| :--- | :--- | :--- |
| **T1** `models/` ~20 GB temizliği | Faz 0 planı §| Ön koşulu S7'ydi; S7 kapandı (**yalnız merge GGUF**) ⇒ artık koşabilir, ama kimseyi bloke etmiyor |
| **kusur 11** · `hakhukuk` paketi tek başına kurulamıyor | ana planın `AÇIK KUSURLAR` bölümü | **Ana plandan DEVREDİLDİ 2026-09-10.** `servis.py`:46 çalışma anında `scripts/`'e köprü kuruyor, `pyproject.toml`'un *"`scripts/` DIŞARIDA"* cümlesi geçersiz. Onarımı **yapısaldır**: aynı dosyayı 26 dosyanın yol köprüsü ve tüm ölçüm hattı kullanıyor ⇒ **kendi turu ve kendi regresyon koşusu**. [ADR-0078](../adr/0078-konteyner-dagitimi-rejim-kilidi.md) m.5 bugün onarmamaya karar verdi |
| **Hat C** metodoloji yazısı | yeni-belge-katmani spec §7 | `v1.0` sonrası |
| **S9** `v2` barındırma · **S17** kuantizasyon eğrisi | — | Hiçbir planın kapsamında değil; açık soru olarak duruyor |
| `recall_taban.json` | ana plan §| Faz 0'ın tek *"kaynaklanmadı"* ihlali. $0, ~15 dk — bir sonraki durakta ödenir |

---

## Bakım kuralı

Bir plan kapandığında **iki yer** güncellenir: planın kendi kapanış bloğu ve **bu dosyanın
"Bir bakışta" kutusu**. Sıra değişirse gerekçe buraya yazılır — sıra değişikliğinin *niye*si
başka hiçbir yerde durmuyor.

~~Bir planın yürütülmesi sırasında çıkan ve o planın kapsamında **çözülmeyen** kusur, plana
sıkıştırılmaz: ayrı bir ticket dosyasına yazılır ve buradaki tabloya bir satır olarak girer.~~

**BU KURAL 2026-09-10'da DEĞİŞTİ (insan kararı).** Ayrı ticket dosyası **kaldırıldı**;
`plans/post-hp-hat-b-tickets.md` silindi ve on üç kusur ana planın sonundaki
[AÇIK KUSURLAR](plans/2026-09-07-hp-hat-a-hat-b.md#açık-kusurlar--kayıt-ve-devir)
bölümüne taşındı. Gerekçe teknik değil, tercihtir; öyle yazılıyor.
**Kuralın koruduğu şey ayakta:** *"planın kapsamı ile borcun kaydı ayrı tutulur, yoksa plan hiç
kapanmaz"*. Ayrım artık dosyayla değil **kutucukla** sağlanıyor — kusur bölümü `- [ ]` taşımaz
ve paydaya girmez. Bu şart düşerse kural da düşer ve plan kapanamaz hâle gelir.
