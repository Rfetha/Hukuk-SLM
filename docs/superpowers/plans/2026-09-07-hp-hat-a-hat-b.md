# `HP` → Hat A → Hat B — uygulama planı (`v0.2` → `v0.3`)

> Başlık 2026-09-09'da düzeltildi: hedef `v1.0` idi, **verilmedi**. Gerekçe [ADR-0077](../../adr/0077-v1-0-verilmedi-v0-3.md): engel modelin başarımı değil, ölçüm aygıtının güvenilirliği (tek hakem ailesi, κ 0,534 < 0,6).

## İCRA DURUMU — 2026-09-11 · **111/115 kutucuk** · `v0.3` etiketlendi

> **2026-09-11 turu:** **G22 KAPANDI 5/5** (Adım 2 ve 3 insana soruldu, ikisi de onaylandı) · G21 **10/11** (kalan: Adım 11 insan gözü) · G20 **5/9** (kalan: Adım 6 `HF_TOKEN` ister · Adım 7 göz · Adım 8). **Kalan 7 kutucuğun 3'ü insan gözü kapısı**, biri insandan sır bekliyor. **178 → 216 test yeşil**, 2 xfail · 12 commit (yerelde, push EDİLMEDİ). Kayıt **#66**, kararlar **ADR-0079** ve **ADR-0080**. Harcanan: **$0,045067** (OpenRouter ölçümü). Yeni tuzaklar **1.11 · 1.12 · 1.13** — üçü de **ölçüm aygıtının içinde**. Yeni açık kusurlar **14-20**.

> ⚠️ **Kutucukları SAYARAK doğrulamaya çalışma — bu dosyada 40 tane var, 115 değil.**
> 2026-09-10'da bitmiş on dört görev **kapanış bloğuna indirildi** ve tam metinleri
> [`docs/record/2026-09-10-hp-hat-a-hat-b-kapanan-gorevler.md`](../../record/2026-09-10-hp-hat-a-hat-b-kapanan-gorevler.md)'ye
> **taşındı** (kopyalanmadı). Onların 75 kutucuğu kayıt dosyasında; sayıları kapanış
> bloklarının başlığında duruyor (`4/4`, `6/6`, …). Planda kalan 40 kutucuk **açık beş işin**
> ve bekletilen `G8`'in kutucuklarıdır. **Payda burada yazar ve tek doğru kaynak burasıdır**;
> aynı gün G21 (11 kutucuk) + G22 (5 kutucuk) eklenerek **99 → 115** oldu.

> **Bu blok planın tek doğru durum kaynağıdır.** Aşağıdaki görev başlıkları değişmedi;
> ne bittiği kutucuklardan, **neyin sırada olduğu buradan** okunur.
> `/goal` promptu: [`goal-hp-hat-a-hat-b.md`](goal-hp-hat-a-hat-b.md) *(2026-09-09'da yenilendi)*
> Açık kusurların kaydı ve devri: **bu dosyanın sonundaki** [AÇIK KUSURLAR](#açık-kusurlar--kayıt-ve-devir) bölümü

| | durum |
| :--- | :--- |
| **FAZ 1** · hakem paneli | **G1 · G3 bitti** — ikinci hakem ailesi koştu, κ **ilk kez ölçüldü** (`tam_sadık` **0,534** · `atıf_temiz` **0,409**, aracın eşiği 0,6 ⇒ **ALTINDA**), [ADR-0074](../../adr/0074-hakem-paneli-kuruldu-baglayici-hukum.md) + [#64](../../record/research_log/2026-09-07-hakem-paneli-iki-aile.md) yazıldı |
| **G2** | **ATLANDI** — insan kararı (bütçe). *(G4 bu satırdan çıkarıldı: 2026-09-09'da koştu, bkz. SIRA 3.)* Bakiye **$3,45** ↔ rakip kolunun ikinci hakemle puanlanması **$2,81**; panel **iki aileli** kaldı ve bu ADR-0074'te **eksiklik olarak** yazılı |
| **FAZ 2** · Hat A | **G5·G6·G7·G8b·G9·G10·G12 bitti**, G11 2/3 — `hakhukuk/` paketi doğdu (istem tek kaynak · tipler · terazi · servis · CLI · TUI), mülga süzgeci girdi, yeniden üretim zinciri yazıldı |
| **G8** · indeks dağıtımı | **BEKLETİLİYOR** — korpus **8,4×** büyüyecek (40.496 → ~340.303 madde) |
| **FAZ 3** · belge katmanı | **G13 bitti** — `PRODUCT.md` · `ROADMAP.md` · `TODO.md` · `docs/MIMARI.md` yazıldı, kırık işaretçiler onarıldı, `MODEL_CARD` §7.2/§8/§10 güncellendi |
| **FAZ 5** · dağıtım | **AÇIK 2026-09-10** — insan kararıyla iki iş `v1` tarafına alındı: **G19** (HTTP API, 6 kutucuk) ve **G20** (konteyner dağıtımı, 9 kutucuk, [ADR-0078](../../adr/0078-konteyner-dagitimi-rejim-kilidi.md)). İkisi de **yerel ve tek kullanıcı**; `S9` açılmadı |
| **FAZ 6** · kusur temizliği | **AÇIK 2026-09-10** — açık kusurların **on biri işe döndü**: **G21** (ürün yüzeyi, 11 kutucuk, **$0**) · **G22** (rejim + KV ölçümü, 5 kutucuk, GPU + insan kapısı). Üçü **devredildi**: kusur 6 ve 12b → `v2` (borç **B1** · **B11**), kusur 11 → sıranın dışı |
| **FAZ 4** · Hat B | **KAPANDI 2026-09-09** — G16 (kabul testi, `v0.3`) · G4 (Sonnet-5) · G18 (araç katmanı) · G17 (yayın) bitti. G14 · G15 **atlandı** (ADR-0075). Açık kalan tek kapı: **G12 Adım 6**, insan gözü |

**Ölçülen 2026-09-09:** **164 test yeşil**, 2 xfail · **16 commit** (yerelde, push edilmedi) ·
`v0.3` etiketli · toplam harcanan **$4,37** (bugün $1,21) · OpenRouter bakiye **$2,20**.
*(Not: raporlanan `judge_cost` gerçekte düşenin 1/1,6'sı — kapı marjı ADR-0072 m.2'de yazılı.)*

### Payda 2026-09-09'da düzeltildi — 89'dan 84'e, sonra Görev 19 ile 90'a

Plan 89 kutucukla açılmıştı ve 79'u işaretliydi; okuyan on iş kaldığını sanıyordu. Gerçek iki
işti. Aradaki 19 kutucuk, kapatılmış kararların kalıntısıydı: G2 (üçüncü hakem, bütçe kararı) ·
G14 ve G15 (eğitim turları, ADR-0075) · G8'in iki adımı (korpus planına bağlı) · G11 Adım 2
(G8'e bağlı) · Görev 4'e sonradan yazılan iki **borç** satırı.

Bunlar **silinmedi** — metin ve gerekçe aynen duruyor, çünkü *"ne koşulmadı ve niçin"* bu planın
en değerli kaydı. Yalnız `- [ ]` olmaktan çıkıp durum etiketli düz maddeye indiler; bir daha
işaretlenmeyecek bir kutucuk, paydayı kirletmekten başka iş görmüyordu.
Ayrıca Görev 17 Adım 4 açık görünüyordu ama iş bitmişti (`v0.3` etiketi atıldı); düzeltildi.
Aynı gün **Görev 19** (HTTP API) insan kararıyla eklendi ve payda 84'ten **90**'a çıktı; açık
sekiz kutucuğun ikisi SIRA 2, altısı Görev 19.

**2026-09-10 · ikinci temizlik — bu sefer taşındı, silinmedi.** Plan **2.337 satıra** çıkmıştı
ve ölçüldü: **%65'i kapanmış işti**, açık üç iş %9'luk bir dilimde kalıyordu. Dahası bu
bulguların sayıları `docs/record/` ve `docs/adr/` içinde **zaten vardı** — plan kaydın **ikinci
kopyasını** taşıyordu, ki `AÇIK KARAR S18` tam bu sınıfı ölçmüştü: *aynı metin iki yerde
durursa sessizce ayrışır*. On dört bitmiş görev kayıt dosyasına taşındı; planda kapanış bloğu
ve işaretçi kaldı. **2.337 → 1.343 satır, 128,6 → 79,5 KB.**
**Taşınmayanlar, insan kararı:** **atlanan** görevler (G2 · G14 · G15) ve **bekletilen** G8
olduğu gibi kaldı — *"ne koşulmadı ve niçin"* bu planın en değerli kaydıdır.

**2026-09-10'da payda 90'dan 99'a çıktı:** **Görev 20** (konteyner dağıtımı) insan kararıyla
eklendi, 9 kutucuk. Payda büyüdü çünkü **iş** eklendi — kapatılmış karar kalıntısı değil.
Gerekçe [ADR-0078](../../adr/0078-konteyner-dagitimi-rejim-kilidi.md)'de: paketlemenin sebebi
kolaylık değil, ticket 2'nin **ölçtüğü** kusurdur (sunucu bayrağı cevabı değiştiriyor ve
bağlayıcı yapılandırmayı bugün hiçbir şey zorlamıyor).

**Bitmiş görevlerde talimat silindi, bulgu tutuldu** (aynı gün, 16 blok / 18 KB): *"şu dosyayı
yaz"* diyen kod kopyaları ve `git commit` reçeteleri çıkarıldı — karşılıkları repoda ve git
geçmişinde, üstelik kopyalar **bayatlamıştı** (`tui.py`'ye `__main__` bloğu, `servis.py`'ye
`answer_arac`, `tipler.py`'ye beşinci durum eklendi). Koşu komutları **silinmedi**: onlar
talimat değil **rejim künyesidir**, ve bu hattın disiplini künyede görünmeyen bayrağın sessizce
düştüğü üzerine kuruludur.

### İŞ SIRASI

| sıra | iş | durum | kapı |
| :--- | :--- | :--- | :--- |
| ~~1~~ | **G8 Adım 1b** — `KUNYE` taşınabilirlik | BİTTİ | kopyalanmış ağaçtan yüklendi, `recall@10` **0,9500** |
| ~~2~~ | **G12 Adım 6-7** — TUI gözle doğrula | **BİTTİ** | üç soruda rozet + atıf + kaynak + ibare **ekranda görüldü**, insan teyit etti |
| ~~3~~ | **G4** — Sonnet-5 rakip havuzunda | BİTTİ | eşit sınav kanıtlı; **Sonnet-5 ÖNDE** (0,8348 ↔ 0,8011) · $1,1932 |
| ~~4~~ | **G16** — `v1.0` kabul testi | BİTTİ | donmuş TEST tek kez açıldı; kütle **0,5804** · `v1.0` VERİLMEDİ → `v0.3` (ADR-0077) |
| ~~5~~ | **G18** — araç katmanı | BİTTİ | 5 kaldıraç · sınırlı döngü · regresyon **80/80 birebir** |
| ~~6~~ | **G17** — modeli YAYINLA | BİTTİ | HF'te, `sha256` doğrulandı; **şu an ÖZEL** (insan kararı) |
| **7** | **G19** — HTTP API (FastAPI) | **5/6** | kod BİTTİ 2026-09-10, **178 test yeşil**; açık tek kutucuk **Adım 6 = insan gözü kapısı** |
| ~~8~~ | **açık kusurlar** — kayıt | — | [AÇIK KUSURLAR](#açık-kusurlar--kayıt-ve-devir) bölümü. **On üçün on biri 2026-09-10'da G21+G22'ye alındı**, üçü devredildi. Kalan kayıt **kutucuk değildir, paydaya girmez** |
| **9** | **G20** — konteyner dağıtımı | **5/9** | beş karar kilitlendi 2026-09-10 ([ADR-0078](../../adr/0078-konteyner-dagitimi-rejim-kilidi.md)); **Adım 0 GPU kapısı GEÇTİ** — konteyner RTX 5070 Ti'yi host ile birebir görüyor. **Adım 1-8 KODLANMADI:** insan kararı 2026-09-10 — bu tur yalnız *tasarım* turuydu, icra ayrı onayla başlar |
| ~~10~~ | **G21** — ürün yüzeyi kusur temizliği | **BİTTİ 11/11** | kusur 3·4·5·7·8·12a·13 · **$0** · dört karar kilitli 2026-09-10. **Adım 8 bir ÖLÇÜMDÜR** — ayrışma yoksa rozet **EKLENMEZ** ve kusur 5a açık kalır. **Adım 11 insan gözü kapısı** |
| ~~11~~ | **G22** — rejim kusuru + KV ölçümü | **BİTTİ 5/5** | kusur 1·2 · GPU · **Adım 2 ve Adım 3 DUR-ve-SOR**. Kusur 2'nin *"bedeli sıfır dolar"* kaydı grill'de **çürütüldü**: kütle **hakem** ister ⇒ para. Önce $0'lık deterministik karşılaştırma |

**SIRA 2 bir insan gözü kapısıdır** ve kendi başına işaretlenmez. Bu kapı 2026-09-09'da bir
ürün kusuru yakaladı: `python -m hakhukuk.tui` hiç açılmıyordu (`__main__` bloğu yoktu) ve 163
test bunu görmemişti — kaynak denetimi mantığın sızmadığına bakar, programın çalıştığına değil.

**Plan kapsamı dışındaki açık kusurlar:** [AÇIK KUSURLAR](#açık-kusurlar--kayıt-ve-devir)
bölümü, **on üç** kusur, **kutucuk taşımaz**. En ağırı: ürün yolunda cevapların **~%5'i boş**
dönüyor ve bu, ADR-0040'ın kendi geçerlilik kapısını geçmez.


**Sıra 4 → 5 → 6 BAĞLAYICI** ([ADR-0076](../../adr/0076-kapi-kaldirac-ayrimi-arac-katmani.md) m.4):
kabul testi **araçsız** koşulur, çünkü yayımlanan %80,1 ve kapı eşiği araçsız rejimde ölçüldü
ve **rakipler araç kullanamaz** — araçlı koşmak ADR-0057'nin *eşit sınav* kuralını ihlal eder.
Araç katmanı kapıdan **sonra**, ürün özelliği olarak girer.

**`v1` = ham base + SFT hattı. KAPANDI — [ADR-0075](../../adr/0075-v1-sft-kapanir-v2-sequential-rl.md) (insan kararı 2026-09-08).**
Eğitim turları (**G14 · G15**) koşulmaz; `v1` bugünkü `tgta_v1` artefaktıyla kapanır ve
yayımlanır. **`v2` = `tgta_v1` üstüne sequential RL** (GRPO + düşünce ayarı) — ayrı plan.

| neden | ölçülmüş gerekçe |
| :--- | :--- |
| **G14 atlandı** | ~~Hedef eksende **geride değiliz** (biz 8/80 ↔ rakipler 8·8·7·8)~~ **BU CÜMLE 2026-09-09'da ÇÜRÜDÜ** — o kıyas yalnız **Gemini havuzunaydı**; Sonnet-5 karşısında `wrong_ref` **0,0769 ↔ 0,0083 = 9,3× GERİDEYİZ** ([OZET](../../../outputs/eval/hp-rakip-havuzu/OZET.md)). Karar **değişmiyor** (G14 yine koşulmuyor, ADR-0075) ama **gerekçesi düştü**: bugün tek gerekçe otomatik vekil metriğin **yok** oluşu ⇒ her tur **80 kalem gözle okuma** = insan saati. B10 aynı sınıftan bir turdu ve **eğitimsiz** kapandı (ADR-0062) |
| **G15 atlandı** | Onaracağı şey (`B4`, −22,1 p) bir **merge** kaybıdır; `τ_a` **tek başına 0,987**. Sequential mimaride merge **yok** ⇒ aynı puan ödenmeden geri gelir. Terk edilecek mimariyi onarmak olurdu |
| **`v1` şimdi yayımlanıyor** | Çalışan ürünü, sonucu belirsiz bir tur için aylarca bekletmek — ADR-0065 bölünmüş sürümlemeyi tam bunu önlemek için kurdu |

**Bedeli açıkça yazılıdır:** ADR-0027'nin **task-vector hattı `v1`'de DONDURULUR**
(`τ = θ_ft − θ_base` tüm kolların aynı `θ_base`'i paylaşmasını şart koşar; `tgta_v1`'i yeni
başlangıç almak bunu bozar ⇒ `v2` **sequential post-training**'dir, task vector değil).
Ve **G14/G15 değersiz sayılmadı** — koşulmadılar, ne verecekleri **bilinmiyor**; ikisi de
borç olarak **açık kalır**.

**Sıra 3 neden burada (karar kilitlendi 2026-09-07, insan):** `anthropic/claude-sonnet-5`
**özne olarak** rakip havuzuna girer — bugün havuzda yalnız Gemini ailesi var ve **frontier
sınıfı hiç ölçülmedi**. Kapıyı **etkilemez** (ADR-0072 m.2: eşik oynamaz, çıpa `3.5 Flash`
kalır; yeni özne yalnız **raporlanır**), eğitim turlarına ve donmuş TEST'e **dokunmaz** ⇒
bağımsız, ve ucuz olduğu ölçülürse erken koşulabilir.
**Bedeli ÖLÇÜLDÜ 2026-09-07 akşam: tam koşu ~$0,82** — `$1` kapısının **altında**.
Ölçüm biçimi kayda değer: duman koşusu (5 kalem) başlatıldı, **iptal edildi ve çıktısı
yanlışlıkla silindi**, ama bedel **bakiye farkından** okundu — `usage 16,5520 → 16,6032`
= **$0,0512 / 5 kalem** ⇒ ×16 = **$0,82**. Planın *"~$0,35"* rakamı **Gemini
fiyatlarıyla** hesaplanmıştı ve **yanlıştı**; Sonnet'in çıkarım fiyatı 4-5 katı
($2,00/M girdi · $10,00/M çıktı ↔ 3.5 FL $0,30/$2,50).
**Ders: harcanan tutar, çıktı kaybolsa bile `/api/v1/credits` farkından ölçülebilir.**
`judge_cost_usd` liste fiyatının türevidir; **bakiye farkı gerçeğin kendisidir** ve
aralarında bugün **1,6×** kapı marjı ölçüldü.

---

> **Ajan işçiler için:** GEREKLİ ALT-BECERİ: `superpowers:subagent-driven-development` (önerilen)
> ya da `superpowers:executing-plans`. Adımlar `- [ ]` kutucuklu.
> **Kutucuk yalnız `verify:` çıktısı GERÇEKTEN alındıktan sonra işaretlenir.**

**Amaç:** Faz 0'ın ölçtüğü modeli **vatandaşın gerçekten kullanabileceği bir ürüne** çevirmek —
ve yayımlanan her sayıyı **tek ailenin hükmü** olmaktan çıkarmak.

**Mimari:** Dört faz, **sırası bağlayıcı** (insan kararı 2026-09-07).
`HP` **önce** gelir çünkü bugünkü **her** sayı `gpt-4o-mini`'nin tek başına hükmü; panel
kurulmadan yeni rakip eklemek *"aynı şüpheli hakemle daha çok sayı üretmek"* olur ve
[ADR-0072](../../adr/0072-v1-rakip-havuzu-genisler.md)'nin GPT öznesi zaten imkânsız kalır.
**Hat A** `HP`'ye **paralel** koşabilir (GPU'ya ve hakeme dokunmaz, **$0**) ve `v0.2`'yi üretir.
**Hat B** `HP`'nin κ sonucuna **bağımlıdır** ve `v1.0` kapısını koşar.

```
HP (hakem paneli, ~$3-5)  ──┐
                            ├──►  Faz C (belge katmanı, $0)  ──►  v0.2 YAYIN
Hat A (paketleme, $0)  ─────┘                                        │
                                                                     ▼
                                              Hat B (model, ~$7-15) ──► v1.0 KAPISI
```

**Yığın:** Python 3.11 + `uv` · `source ~/code/global_venv/bin/activate` ·
llama.cpp (`llama-server`, Q4_K_M, KV q8_0) · `sentence-transformers` (`bge-m3`, CPU) ·
BM25 + dense hibrit, RRF (`RRF_K=10`) · `pytest` · hakem geçidi OpenRouter ·
TUI için `textual` (~~henüz kurulu değil~~ → **8.2.8 KURULU**, ölçüldü 2026-09-09).

---

## Global kısıtlar — her görev bunları örtük olarak taşır

- **Python:** `source ~/code/global_venv/bin/activate` **aynı komut içinde**.
- **Sırlar:** `set -a && . ./.env && set +a`. Anahtarlar hiçbir dosyaya, log'a, künyeye yazılmaz.
- **Rejim değişmezleri (uyuşmazlık hata VERMEZ, kıyası GEÇERSİZ kılar):**
  `--seed 3407` · `--max-chunk-chars 900` · `--thinking on` · `--think-budget 1024` ·
  `--max-new-tokens 512` (toplam bütçe **1536**, ADR-0070) · `--n 80` ·
  veri `data/eval/dev/core_hard.jsonl` (**v2**, ADR-0067) ·
  indeks `data/index/mevzuat_bge_m3_s2` · `--harness-k 10` · `RRF_K=10` (ADR-0068) ·
  **önsözsüz** (`EXTRA_ARGS` boş — künyedeki `ekstra : <yok>` satırı kanıttır, ADR-0063).
- **M5 rejimi ayrıdır:** `SERVER_EXTRA="--dry-multiplier 0.8 --dry-base 1.75 --dry-allowed-length 2"`
  (ADR-0073). **Yalnız M5.** Rakip içeren hiçbir moda eklenmez — DRY bir `llama.cpp`
  örnekleyicisidir, Gemini'ye uygulanamaz, dolayısıyla orada **eşitlenemez** (ADR-0057).
- **Donmuş TEST'e dokunulmaz:** her şey `data/eval/dev/`. `data/eval/canon/` **yalnız**
  Görev 16'nın kabul testinde, **tek kez** açılır.
- **ŞARJ:** her GPU koşusundan önce künyede `güç : ŞARJDA` doğrulanır. Pilde GPU
  **180 MHz**'e kısılıyor → 80 kalem **4,8 saat** ↔ şarjda **~25 dk** (ölçüldü 2026-09-07).
- **Uzun koşular `setsid nohup … &` ile AYRIK başlatılır**, `Monitor` ile beklenir.
  Harness'ın arka plan görevi olarak başlatma: bellek gözcüsü `free`'ye bakıp öldürüyor.
  Çıktıyı `| tail`'a sokma — süreç bitene kadar hiçbir şey görünmez.
- **Her koşudan önce** [`docs/record/yurutme-tuzaklari.md`](../../record/yurutme-tuzaklari.md)
  okunur. **17 tuzağın hepsi** *"hata vermeden yanlış sayı üretir"* sınıfından.
- **Gözle okuma bir kapıdır.** Faz 0'da sayısal kapı **beş kusuru** geçirdi; beşini de göz
  ya da *"bu sayıyı neyle, hangi birimde kıyaslayacağım?"* sorusu yakaladı.
- **Parasal kapı tahmini TABAKALANMIŞ duman koşusundan yapılır** (tuzak **1.11**, ölçüldü
  2026-09-09): yeni bir özne eklenirken duman koşusu kısa · orta · uzun soru içerecek biçimde
  seçilir, ya da kapıya **%50 emniyet payı** konur. n=5'ten doğrusal çarpım $0,82 dedi, gerçek
  **$1,1932** tuttu — $1 kapısı **hata vermeden** %45 aşıldı.
- **Bütçe — ÖLÇÜLDÜ 2026-09-07:** OpenRouter **$6,60** (`total_credits` 20 −
  `total_usage` 13,397) · Modal **$29,19**. Devir notundaki *"~$8,88"* **yanlıştı**.
  Bu plan **~$10-20** harcar ⇒ **OpenRouter bakiyesi `HP` + kapı koşusuna yetmeyebilir.**
  **DUR ve sor:** tek adımda **>$1** harcamadan önce.
- **Lisans:** yalnız kamuya açık kaynak (Mevzuat.gov.tr · Resmî Gazete · Yargıtay açık portal).
  **Lexpera / Kazancı ASLA** — telif zehri. Eğitim verisinde PII maskelenir.
- **Kod dili İngilizce, belge/yorum/commit dili TÜRKÇE.**
- **DUR ve sor:** yeni rejim kararı · **>$1** harcama · donmuş TEST'in açılması ·
  bir `AÇIK KARAR` damgasının kendi başına kapatılması.

### AÇIK KARARLAR — insan cevabı olmadan ilgili görev BAŞLAMAZ

| # | durum | bloke ettiği görev |
| :-- | :--- | :--- |
| ~~S5~~ | **KAPANDI** → Wilson **raporlanır**, kapı kuralı **değişmez** (ADR-0050) | ~~Görev 16~~ · iki şerh zorunlu |
| ~~S7~~ | **KAPANDI** → adaptör yüklenmez; yalnız **merge edilmiş GGUF** yayımlanır | ~~T1~~ · T1 zaten bağlı değilmiş |
| ~~S8~~ | **KAPANDI** → **(a) HF dataset** (79,1 MiB; `huggingface_hub` zaten var) | ~~Görev 8~~ **açıldı** + kod borcu |
| **S9** | **AÇIK** — `v2` nasıl barındırılır? | bu planın **dışında** (`v2`) |
| ~~S10~~ | **KAPANDI** → geçici muhafazakâr metin, **tek kaynakta** | ~~Görev 10 · 12~~ **açıldı** |
| ~~S12~~ | **ERTELENDİ** → `τ_a` v2 turuna; `v1.0` yolunda **değil** | ~~Görev 13~~ *(eşleme yanlıştı)* |
| ~~S16~~ | **KAPANDI** → **tek Claude Sonnet öznesi** (~$0,35) | ~~Görev 4~~ **açıldı** |
| **S17** | **AÇIK** — kuantizasyon eğrisi ölçülsün mü? | bu planın **dışında** |
| ~~S18~~ | **KAPANDI** *(iki katman)* → **ölçülen sürüm kanon**; `τ_g` çift-system **değil** | ~~Görev 5~~ **açıldı** |

**Grilleme turu 2026-09-07: dokuz sorunun YEDİSİ kapandı, ikisi gerekçeli ertelendi.**
Bloke edilen görev sayısı **dört → sıfır**. Kapanışların üçü **olguyla** geldi (insan kararı
gerekmedi): S18'in çift-system katmanı · S8'in gerçek bedeli · S12'nin yanlış eşlemesi.
Ve grilleme **planın kendi üç iddiasını çürüttü** — hepsi bu planda yazılıydı:
*"diskten cevaplanamıyor"* (S18) · *"kurulumda üret ~10 dk"* (S8) · *"Görev 13'ü bloke ediyor"* (S12).

--- | :--- |
| **S5** | İkili oran çözünürlük sınırı (Wilson aralığı kapı kuralını değiştirir) | Görev 16 (yorum) |
| **S7** | LoRA adaptörleri HF'ye yüklensin mi? | Faz 0 planı **T1** |
| **S8** | İndeks nasıl dağıtılır? (80 MB — ölçüldü) | **Görev 8** |
| **S9** | `v2` nasıl barındırılır? | bu planın **dışında** |
| ~~S10~~ | **KAPANDI** → geçici metin şimdi girer, tek kaynakta; nihai metin hukukçu görüşüne bağlı | ~~Görev 10~~ **açıldı** |
| **S12** | KARAR-6 paralel slot (`-np`) — bozuk ölçütle toplandı | Görev 13 (taşıyıcı) |
| ~~S16~~ | **KAPANDI** → **tek Claude Sonnet öznesi** (~$0,35); GPT sınıfı usulen dışarıda | ~~Görev 4~~ **açıldı** |
| **S17** | Kuantizasyon eğrisi ölçülsün mü? | bu planın **dışında** |
| **S18** | Sürüklenmiş `SYSTEM_PROMPT`'un hangi hâli kanon? | **Görev 5** |

---

## Dosya yapısı — hangi dosya neyden sorumlu

**Yeni paket: `hakhukuk/`** *(repo kökünde, `scripts/`'ten AYRI)*

`scripts/` **ölçüm aletidir**; `hakhukuk/` **üründür**. Ayrı olmalarının ölçülmüş sebebi:
`scripts/` 72 dosya, 11.817 satır ve **18 modül uzantısız import'la** birbirine bağlı
(envanter 2026-09-07). Ürünü oraya koymak, vatandaşın kurulumunu **ölçüm hattının tamamına**
bağımlı yapar.

| dosya | tek sorumluluğu |
| :--- | :--- |
| `hakhukuk/istem.py` | **İstem metinlerinin TEK kaynağı.** Sürümlü sabitler + `sha256` damgası |
| `hakhukuk/tipler.py` | `Durum` (enum) · `Kaynak` · `Atif` · `Cevap` — donmuş `dataclass`'lar |
| `hakhukuk/servis.py` | **Derin modül:** `answer(soru) → Cevap`. Retriever + llama.cpp + istem **içeride gizli** |
| `hakhukuk/terazi.py` | `suskunluk_terazisi` ürün yüzeyi: cevabı üç duruma ayırır, uydurulmuş atıfı **kullanıcıya gitmeden** yakalar |
| `hakhukuk/cli.py` | `hakhukuk "soru"` — `answer()` üstünde ince kabuk, **kendi mantığı yok** |
| `hakhukuk/tui.py` | `textual` tek ekran — `answer()` üstünde ince kabuk, **kendi mantığı yok** |
| `hakhukuk/kurulum.py` | İndeks indir/üret · GGUF indir · doğrula (S8'e göre doldurulur) |
| `tests/test_istem.py` … | Her modül için deterministik birim testi (`pytest`) |

**Neden ayrı `terazi.py`:** *(POSD silme testi)* silinirse üç sorumluluk **üç çağırana** yayılır
(CLI · TUI · gelecekteki API). Karmaşıklığı tek yerde tutuyor ⇒ **derin modül**, shallow değil.

**Belge katmanı (spec §8):** `PRODUCT.md` · `ROADMAP.md` · `TODO.md` · `docs/MIMARI.md`
— dördü de **bugün yok** (ölçüldü 2026-09-07).

---

# FAZ 1 · `HP` — hakem paneli (~$3-5) ÖNCE

**Neden:** Bugün yayımlanan **her** sayı `openai/gpt-4o-mini`'nin **tek başına** hükmü.
κ **yok**, öz-tercih **ölçülmedi** — ADR-0064 bunu *"Ne KURULMAZ"* madde 2 olarak zaten borç
yazmış. Ve [ADR-0072](../../adr/0072-v1-rakip-havuzu-genisler.md)'nin GPT öznesi **bu panel
kurulmadan eklenemez** (aile dışlaması, ADR-0032).

**Ölçülmüş boşluk:** `scripts/puanlama/judge_agreement.py` **hazır** — üç modu var (`cross` · `export` ·
`author`), eşik dosyada yazılı: **κ ≥ 0,6 makul · ≥ 0,8 güçlü**. Yeni araç **gerekmiyor**.

---

### Görev 1: İkinci hakem ailesi (Anthropic) — **KAPANDI 2026-09-07** · 4/4

Aynı 80 kayıt ikinci hakem ailesiyle yeniden puanlandı. **Üretim yeniden KOŞULMADI** — panel
yalnız *hakem* değişkenini ölçer; üretimi de değiştirmek iki değişkeni birbirine karıştırırdı.

→ tam metin: [kapanan görevler](../../record/2026-09-10-hp-hat-a-hat-b-kapanan-gorevler.md) §G1 · [ADR-0074](../../adr/0074-hakem-paneli-kuruldu-baglayici-hukum.md) · [#64](../../record/research_log/2026-09-07-hakem-paneli-iki-aile.md)
### Görev 2: Üçüncü hakem ailesi (Google) — **ATLANDI 2026-09-07 (insan kararı)**

> **BU GÖREV KOŞULMADI.** Sebep sayıyla: OpenRouter bakiyesi **$3,45**, rakip kolunu ikinci
> hakemle puanlamanın tahmini gerçek faturası **$2,81** (bakiyenin %81'i) ve donmuş TEST kabul
> koşusunun puanlaması da aynı bakiyeden ödenecekti. İnsan kararı: *"tek puanlayıcı ile de devam
> edilebilir; amaç çalışan uçtan uca ürün."*
> ⇒ Panel **iki aileli** kaldı, ADR-0032'den **sapıldı** ve bu yayında **eksiklik** olarak yazılır
> ([ADR-0074](../../adr/0074-hakem-paneli-kuruldu-baglayici-hukum.md) · [#64](../../record/research_log/2026-09-07-hakem-paneli-iki-aile.md)).
> Aşağıdaki adımlar, borç kapanacağı gün koşulmak üzere **olduğu gibi duruyor**.

**Dosyalar:**
- Create: `outputs/eval/hp-hakem-paneli/gnd_h1_tgta_v1_google*.json*`
- Read: [ADR-0032](../../adr/0032-hakem-paneli-uc-aile-ve-aile-dislama.md)

**Arayüzler:**
- Tüketir: Görev 1 ile **aynı** girdi dosyası
- Üretir: üçüncü ailenin `gnd_*.jsonl`'i — Görev 3'ün κ üçlüsü bunu bekler

**Kritik ayrım — bu görevin varlık sebebi:**

| özne | ailesi | Google hakem kullanılabilir mi |
| :--- | :--- | :--- |
| **`tgta_v1` (biz)** | Qwen/Alibaba | **evet** — üç ailenin hiçbiri bizim ailemiz değil |
| `gemini-3.1-FL` · `3.5-FL` · `3.5-Flash` | **Google** | **HAYIR** — kendi ailesi kendini notlayamaz |

⇒ **Üçlü κ yalnız BİZİM kolumuzda kurulur.** Rakip kolları **iki aileyle** (OpenAI + Anthropic)
notlanır. Bu bir eksiklik değil, **ADR-0032'nin kuralının doğrudan sonucudur** ve raporda
**açıkça** yazılır.

- **ATLANDI** · **Adım 1: Kimlik + fiyat doğrula** — Görev 1 Adım 1'in aynısı, `gemini` filtresiyle.
`verify:` kimlik ve fiyat basıldı.

- **ATLANDI** · **Adım 2: Tam koşu (80 kalem), AYRIK** — Görev 1 Adım 3'ün aynısı;
`LLM_PROVIDER_ORDER=Google`, `--label h1_tgta_v1_google`.
`verify:` `EXIT=0` · `n=80` · `judge_cost_usd` basıldı.

- **ATLANDI** · **Adım 3: Aile dışlaması denetimi — otomatik, gözle değil**

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
python - <<'PY'
import json, glob, os, sys
AILE = {"openai": "OpenAI", "anthropic": "Anthropic", "google": "Google", "gemini": "Google"}
def aile(x):
    x = (x or "").lower()
    for k, v in AILE.items():
        if k in x:
            return v
    return "?"
ihlal = 0
for f in sorted(glob.glob("outputs/eval/**/gnd_*_summary.json", recursive=True)):
    d = json.load(open(f, encoding="utf-8"))
    lab, jm = d.get("label", ""), d.get("judge_model", "")
    ozne_aile = aile(lab.replace("tgta_v1", "").replace("base", ""))
    hakem_aile = aile(jm)
    if ozne_aile != "?" and ozne_aile == hakem_aile:
        print(f"   İHLAL  {os.path.basename(f)}  özne={ozne_aile} hakem={hakem_aile} ({jm})")
        ihlal += 1
print(f"\naile dışlaması ihlali: {ihlal}")
sys.exit(1 if ihlal else 0)
PY
```
`verify:` çıktı `aile dışlaması ihlali: 0` ve **çıkış kodu 0**. İhlal varsa **DUR** —
o sayı yayımlanamaz.

- **ATLANDI** · **Adım 4: Commit**

---

### Görev 3: κ + öz-tercih + bağlayıcı hüküm — **KAPANDI 2026-09-07** · 5/5

κ **ilk kez ölçüldü**: `tam_sadık` **0,534** · `atıf_temiz` **0,409** — aracın **0,6** eşiğinin
ALTINDA. Öz-tercih ölçüldü, `KAPPA.md` yazıldı; bağlayıcı hüküm kuralı **kapı koşusundan ÖNCE**
ön-kayda geçti. Bu sayı bugün `v1.0`'ın verilmemesinin **tek gerekçesidir**.

→ tam metin: [kapanan görevler](../../record/2026-09-10-hp-hat-a-hat-b-kapanan-gorevler.md) §G3 · [ADR-0074](../../adr/0074-hakem-paneli-kuruldu-baglayici-hukum.md) · [#64](../../record/research_log/2026-09-07-hakem-paneli-iki-aile.md)
### Görev 4: Rakip havuzu — Sonnet-5 — **KAPANDI 2026-09-09** · 6/6 *(SIRA 3)*

`anthropic/claude-sonnet-5` özne olarak girdi. **Eşit sınav kapısı GEÇTİ**: `recall@10`
**0,9500 ↔ 0,9500**, birebir. **Sonnet-5 ÖNDE** — GÖZ-katı okumada kütle **0,8348 ↔ 0,8011**
(−3,37 p); öne geçtiğimiz tek okuma, önde olmadığımızı bildiğimiz okumadır.
Önde olduğumuz tek eksen **uydurulmuş madde: 0/114 ↔ 2/163**.
`wrong_ref_rate_micro` **0,0769 ↔ 0,0083 = 9,3× GERİDE** ⇒ planın *"B1'de rakiplerden geride
değiliz"* hükmü **yalnız Gemini havuzunda** doğruydu.
Bedel **$1,1932**; tahmin $0,82 idi ⇒ **$1 kapısı %45 aşıldı**.

**İki alet dersi:** (a) `n=5`'lik duman koşusundan ×16 doğrusal ekstrapolasyon **kapı kurmuyor**;
(b) `recall` komutu var olmayan bir alan adı yüzünden **hata vermeden `0,0000`** bastı — eşit
sınav kapısı çökmüş gibi okunabilirdi.

→ tam metin: [kapanan görevler](../../record/2026-09-10-hp-hat-a-hat-b-kapanan-gorevler.md) §G4 · [ADR-0072](../../adr/0072-v1-rakip-havuzu-genisler.md) · [#65](../../record/research_log/2026-09-09-kabul-testi-ve-frontier-kiyasi.md)
### Görev 5: İstem artefaktı — **KAPANDI 2026-09-07** · 8/8 *(S18)*

Spec *"istem yalnız tek dosyada"* diyordu; **sayıldı: `"Sen HakHukuk'sun"` literali 5 dosyada**
ve `SYSTEM_PROMPT` **sürüklenmişti** — eğitilen istem ile ölçülen istem sessizce ayrışmıştı.
Karar: **ölçülen sürüm kanon**, çünkü yayımlanan %80,1 dâhil bütün sayılar onunla üretildi.
`hakhukuk/istem.py` tek kaynak oldu (`grep -rc "Sen HakHukuk'sun" scripts/` → **0**) ve damga
dosyaya çakıldı. **Kanıt kapısı:** istem dosyadan okunurken çıktı **10/10 birebir** aynı.

→ tam metin: [kapanan görevler](../../record/2026-09-10-hp-hat-a-hat-b-kapanan-gorevler.md) §G5
### Görev 6: Tipler — üç durumun ayrılması — **KAPANDI** · 5/5

`Durum` bir **enum**, `bool` değil. `bool cevap_verdi` vatandaş için en tehlikeli hâli —
ortadaki *"doğrudan madde yok, bununla birlikte…"* — **kaybeder**. TDD ile kuruldu; sonradan
`KESIK` ve `ARAMA_TUKENDI` eklenerek beşe çıktı.

→ tam metin: [kapanan görevler](../../record/2026-09-10-hp-hat-a-hat-b-kapanan-gorevler.md) §G6
### Görev 7: `suskunluk_terazisi` ürün yüzeyi — **KAPANDI** · 6/6

Ölçüm aleti olan üç şey (atıf doğrulama · red tespiti · durum sınıflandırma) üründe **güven
mekanizmasına** dönüştü: uydurulmuş atıf kullanıcıya **GİTMEZ**. Faz 0'ın taze dersi doğrudan
girdi — `exact_reject`'in *"bulunmamaktadır"* dalı **6/6 yanlış pozitif** vermişti, bu yüzden
ürün sınıflandırıcısı **kaynak var mı** bilgisini de kullanır. Regresyon kapısı 80 gerçek
kalemde alet ↔ göz karşılaştırmasıyla geçti.

→ tam metin: [kapanan görevler](../../record/2026-09-10-hp-hat-a-hat-b-kapanan-gorevler.md) §G7
### Görev 8: İndeks dağıtımı **BEKLETİLİYOR** *(insan kararı 2026-09-07)*

> **BU GÖREV ŞİMDİ KOŞULMAZ.** S8 kapandı (**(a) HF dataset**) ama kararın **girdisi değişti**:
> kapsam `CB_KARAR` + `KKY` dahil genişleyecek ⇒ indeks **79 MB → ~697 MB** (ölçüldü:
> 9.722 belge ≈ **340.303 madde**, bugün 40.496 — **8,4×**).
> ⇒ Bugünkü 79 MB'lık indeksi paketlemek, **birkaç hafta sonra atacağımız** bir iştir.
>
> **Bağımlılık:** [`specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md`](../specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md)
> planı bitmeden bu görev başlamaz. `v0.2` **genişletilmiş korpusla** çıkar.
>
> **Ama Görev 8b (mülga süzgeci) BEKLEMEZ** — o bir doğruluk meselesi ve bugünkü korpusta da
> geçerli (800 getirilen kaynağın 2'si mülga).
> Ve **Adım 1b'nin kod borcu da beklemez**: `KUNYE.json`'un mutlak yol + `mtime` kilidi
> hangi boyutta olursa olsun **başka makinede çöker**.
>
> **Yeniden okunacak girdiler:** *"dakikalar içinde kurulur"* cümlesi **düşer** ·
> **(b) kurulumda üret seçeneği FİİLEN ÖLDÜ** (gömme GPU'da ~1,5 sa, **CPU'da ~23 sa**).


**Dosyalar:** Create: `hakhukuk/kurulum.py` · `tests/test_kurulum.py`

**Ölçülmüş girdiler (2026-09-07):**
- `data/index/mevzuat_bge_m3_s2/` = **80 MB** (tek dosya `gomme.npy` 82,9 MB + `KUNYE.json`)
- `.gitignore:166` → `data/index/**/*.npy` ⇒ ikili **git'te YOK**, yalnız künye takipli
- Korpus `data/corpus/mevzuat_maddeler.jsonl` = **37 MB**, git'te **VAR**
- Yeniden üretim: `bge-m3` ile **40.496 madde** gömülür — CPU'da **~2 sa 45 dk**, GPU'da ~10 dk

⇒ Kullanıcı indeksi repodan **alamıyor**. İki seçenek: **(a)** HF dataset'ten indir ·
**(b)** kurulumda üret. **İnsan kararı olmadan bu görev başlamaz.**

- [x] **Adım 1: Karar ALINDI 2026-09-07 → (a) HF dataset**

79,1 MiB indirme; `huggingface_hub==1.18.0` **zaten bağımlılık**. Reddedilen (b)'nin gerçek
bedeli ölçüldü: `BAAI/bge-m3` **4,3 GB** + CPU'da **~2 sa 45 dk** (planın *"~10 dk"* etiketi
**GPU** ölçümüydü — yanlıştı).

- [x] **Adım 1b : ÖNCE `KUNYE.json`'un taşınabilirlik kilidini kır** **BİTTİ 2026-09-09**

Bu adım olmadan **her iki seçenek de** başka makinede çöker. `KUNYE.json`'un `korpus` bloğu
**mutlak yol + `(bayt, mtime)`** taşıyor; `retriever.py`:143-152 yüklemede doğruluyor, uymazsa
`SystemExit`. `git clone` sonrası `mtime` checkout zamanı olur ⇒ patlar.
Yapılacak: mutlak yol → **repo-göreli** · `mtime` vekili → **içerik hash'i** · künyeye
**önek sözleşmesi** (bge-m3 önek almaz; kural bugün `retriever.py`:80-90'da) ve `bge-m3`
**revision/hash'i** eklenir.
`verify:` repo başka bir dizine kopyalanır, `retriever` **hatasız yükler**, `recall@10` **0,9500**.

**`verify:` ALINDI — ölçüldü, hatırlanmadı:**

| ne | sonuç |
| :--- | :--- |
| kopyalanmış ağaç *(scratchpad, repo dışı)* + korpus `mtime`'ı `git checkout` gibi tazelendi | `retriever` **hatasız yükledi** |
| `recall@10`, **kurulu indeksten**, DEV n=80, `Yururluk.YALNIZ_YURURLUKTE` | **0,9500** (76/80) — çıpayla birebir |
| kontrol: HEAD'deki kod, ikinci makine koşullarında | `🚫 korpus bulunamadı: /home/baskabir/...` ⇒ **hata gerçekti** |
| test | **148 geçti**, 2 xfail *(öncesi 143)* — 5 yeni test |

**Plandan iki sapma, ikisi de burada damgalanıyor:**
1. **Yol `repo`-göreli değil, `indeks dizini`-göreli** (`../../corpus/mevzuat_maddeler.jsonl`).
   Sebep: repo kökünü keşfetmek yeni bir kavram ister ve HF'ten inen indeks repo ağacının
   içinde olmayabilir; indeks↔korpus bağıntısı ise sabittir. Taşınabilirlik ölçütü aynen
   karşılanıyor, üstelik testlerde `tmp_path` altında da çalışıyor.
2. **`model_revision` = `null`.** İndeks 2026-08-05 17:30'da kuruldu, yerel HF önbelleği
   2026-09-06 18:07'de doldu (**iki** snapshot var) ⇒ önbellekteki commit o günkü kolun
   **kanıtı değildir** ve uydurulmadı. Bundan sonra kurulan her indeks bu alanı `retriever.kur`
   içinde **ölçerek** yazar (`_model_revizyonu`).

**`data/index/mevzuat_bge_m3/` (pre-S2) bilerek ESKİ BİÇİMDE bırakıldı** — işaret ettiği
korpus sürümü diskte yok (37.903.062 ≠ 38.751.499 bayt), içerik hash'i **bilinemez**. Bugün de
dünkü gibi yüklenmiyor; tek fark hükmün okunur olması: *"eski biçim … yeniden kur"*.

**`scripts/erisim_korpus/recall_indeksten.py`** eklendi: `recall_olc.py` korpusu **sıfırdan
gömer** ve diskteki indekse hiç bakmaz ⇒ *"dağıtılan indeks doğru mu"* sorusu bugüne kadar
**ölçülemiyordu**. Bu betik onu ölçer ve verify'ı yeniden koşulabilir kılar.

- **BEKLETİLİYOR** · **Adım 2: Failing test yaz** — karar (a) ise indirme + `sha256` doğrulama, (b) ise
üretim + `KUNYE.json` eşleşmesi sınanır. İki durumda da test **künye eşleşmesini** sınar:
indeksin `KUNYE.json`'u korpusun sürümüyle uyuşmuyorsa `recall@10` sessizce düşer.

- **BEKLETİLİYOR** · **Adım 3-5: Uygulama · test yeşil · commit**

**S8 KAPANDI 2026-09-07 → (a).** Aşağıdaki iki seçenek kaydı, *neyin reddedildiğini* göstermek için duruyor. İki seçenek **farklı kod** ister:
- **(a) HF dataset:** `huggingface_hub.hf_hub_download` + `sha256` doğrulama + yeni bağımlılık
- **(b) kurulumda üret:** `bge-m3` yükle + 40.496 madde göm + `KUNYE.json` yaz (**~2 sa 45 dk
  CPU** / ~10 dk GPU) — yeni bağımlılık yok, ama kurulum saatlerce sürer

Şimdi ikisinden birini yazmak, insana ait bir kararı **sessizce** vermek olur.
Karar gelince adımlar bu görevin içine, tam koduyla yazılır.

---

### Görev 8b: Yürürlük süzgeci — **KAPANDI 2026-09-07** · 6/6

Korpus `mulga` alanını **2026-08'den beri taşıyordu ama `retriever.py` OKUMUYORDU**. Gerçek bir
koşuda **800 getirilen kaynağın 2'si yürürlükten kalkmış madde** ve vatandaşa gidiyordu — bu
eksik özellik değil **YANLIŞ CEVAPtır**, o yüzden `v2`'ye değil buraya alındı.
`Yururluk` enum'u ile varsayılan **YALNIZ_YURURLUKTE** oldu (public API'de bool bayrak yok):
sızıntı **2 → 0**, `recall@10` **0,9500'de KALDI**. Korpusa anlık görüntü künyesi eklendi —
892 kanun · 40.496 madde · **2.547 mülga** · kapsam **yalnız kanun** (yönetmelik/tüzük/KHK yok).

→ tam metin: [kapanan görevler](../../record/2026-09-10-hp-hat-a-hat-b-kapanan-gorevler.md) §G8b
### Görev 9: Servis katmanı `answer(soru) → Cevap` — **KAPANDI** · 6/6

POSD derin modül: arayüz **tek fonksiyon**, arkasında retriever · `llama-server` · istem ·
terazi gizli. Uçtan uca kapı gerçek sunucuya karşı üç soruyla koşuldu.

→ tam metin: [kapanan görevler](../../record/2026-09-10-hp-hat-a-hat-b-kapanan-gorevler.md) §G9
### Görev 10: CLI + sorumluluk ibaresi — **KAPANDI 2026-09-07** · 5/5 *(S10)*

S10 **kısmen** kapandı: nihai hukuki ibare hukukçu görüşüne bağlı, bu yüzden **geçici
muhafazakâr metin** girdi ve `cli.py` onun **tek kaynağı** oldu — `tui.py` ve `api.py` import
eder, **kopyalamaz** (S18'in dersi: aynı metin iki yerde durursa sessizce ayrışır).

→ tam metin: [kapanan görevler](../../record/2026-09-10-hp-hat-a-hat-b-kapanan-gorevler.md) §G10
### Görev 11: Yeniden üretim yolu — **2/3** *(kalan adım Görev 8'e bağlı)*

Yayımlanan **%80,1** o güne kadar **hiç kimse tarafından yeniden üretilemiyordu**.
`scripts/yeniden_uret.sh` + [`docs/YENIDEN_URETIM.md`](../../YENIDEN_URETIM.md) zinciri yazdı.
Üçüncü adım (indeks dağıtımı) **Görev 8'e bağlı** olduğu için kutucuktan çıkarıldı.

→ tam metin: [kapanan görevler](../../record/2026-09-10-hp-hat-a-hat-b-kapanan-gorevler.md) §G11
### Görev 12: Basit TUI (`textual`)

**Dosyalar:** Create: `hakhukuk/tui.py` · `tests/test_tui.py` · Modify: `pyproject.toml`
**Bağımlılık:** Görev 9 · 10

~~**`textual` kurulu DEĞİL** (ölçüldü 2026-09-07: `ModuleNotFoundError`)~~ → **kuruldu, 8.2.8**
(ölçüldü 2026-09-09; Adım 1'in kapısı bu ölçümle geçti). Yeni bağımlılık ⇒
gerekçe: tek ekranlı arayüzü elle yazmak `prompt_toolkit`/`curses` seviyesinde **kendi
mantığını** doğurur; `textual` bunu hazır veriyor ve `answer()`'ın üstünde **ince kabuk**
kalmasını sağlıyor.
**Web arayüzü, API sunucusu, hesap/oturum DEĞİL** — onlar `v2` (S9).

- [x] **Adım 1: Bağımlılığı ekle ve sürümü PİNLE**
`verify:` `python -c "import textual; print(textual.__version__)"` çalışıyor · `pyproject.toml`'da
**tam sürüm** yazılı.

- [x] **Adım 2: Failing test** — TUI'nin **kendi mantığı olmadığını** sınar:

*(kod 2026-09-09'da silindi — karşılığı repoda ve git geçmişinde; plandaki kopya artık güncel değildi.)*

- [x] **Adım 3: Testi koş, BAŞARISIZ olduğunu gör**

Run: `python -m pytest tests/test_tui.py -v` → `FAIL` (`No module named 'hakhukuk.tui'`)

- [x] **Adım 4: Uygulama — ince kabuk**

*(kod 2026-09-09'da silindi — karşılığı repoda ve git geçmişinde; plandaki kopya artık güncel değildi.)*

`SORUMLULUK_IBARESI` **Görev 10'da** `hakhukuk/cli.py`'de tanımlanır ve buradan **import
edilir** — iki yere yazılmaz (S18'in dersi).

- [x] **Adım 5: Testi koş, GEÇTİĞİNİ gör**

Run: `python -m pytest tests/test_tui.py -v` → **1 passed**

- [x] **Adım 6: Gözle doğrula** — **İNSAN TEYİT ETTİ 2026-09-11.** `python -m hakhukuk.tui` açıldı, üç soru soruldu. `verify:` **dört durumdan İKİSİ ekranda ayırt edildi** — `🟢 CEVAP` (kira feshi, TBK 330, atıf `✓` doğrulanmış) ↔ `⚪ SUSKUNLUK` (kapsam dışı soru, atıf bölümü hiç çıkmadı, **doğru davranış**); sorumluluk ibaresi **her iki cevapta da** görüldü.
`verify:` dört durumdan en az ikisi ekranda **ayırt edilebiliyor**; sorumluluk ibaresi
**her** cevapta görünüyor.

- [x] **Adım 7: Commit** — TUI kodu 2026-09-09'da commit edilmişti; bu turda üç kez daha değişti (kusur 3 · 8 · 17 · 26) ve her biri kendi commit'ini aldı.

```bash
git add hakhukuk/tui.py tests/test_tui.py pyproject.toml && \
git commit -m "A7: basit TUI (textual) — answer() üstünde ince kabuk, kapı testiyle korunuyor"
```

---

# FAZ 3 · Belge katmanı ($0) → `v0.2` YAYIN

**Dördü de bugün YOK** (ölçüldü 2026-09-07).

---

### Görev 13: Belge katmanı — **KAPANDI 2026-09-07** · 7/7

`PRODUCT.md` · `ROADMAP.md` · `TODO.md` · `docs/MIMARI.md` yazıldı, kırık işaretçiler onarıldı,
`MODEL_CARD` genişletildi, **`v0.2` etiketlendi**. `docs/record/**` ve `docs/adr/**` bilerek
**GÜNCELLENMEDİ** — onlar *"o gün şu belge şunu diyordu"* kaydıdır.
`tests/test_belgeler.py` artık canlı belgelerdeki her işaretçiyi yürüyor: **ölü işaretçi bir
testi düşürüyor**, gözle taramaya bırakılmıyor.

→ tam metin: [kapanan görevler](../../record/2026-09-10-hp-hat-a-hat-b-kapanan-gorevler.md) §G13
### Görev 14: `B1` — isabetsizlik **ATLANDI 2026-09-08 (ADR-0075)**

> **KOŞULMADI.** `v1` SFT ile kapanıyor. Gerekçe ölçülmüş: hedef eksende **geride değiliz**
> (biz **8/80** ↔ rakipler **8 · 8 · 7 · 8**, [#63](../../record/research_log/2026-09-07-skor-karti-bosluklari.md))
> ve `B1` için **otomatik vekil metrik yok** (süzgeçler 4 ve 3 buluyor, **göz 8** — ADR-0066)
> ⇒ her tur **80 kalem gözle okuma** ister; bedeli para değil **insan saati**.
> **`B1` borç olarak AÇIK kalır** — bu bir öncelik kararıdır, ölçüm sonucu değil.
> Aşağıdaki adımlar, tur açılacağı gün koşulmak üzere **olduğu gibi duruyor**.

**Neden:** Faz 0'da **ilk kez gözle** sayıldı: **8/80**. B10 (aşırı-red) 4/80'e indi ⇒ **B1
artık birinci sıradaki eksen**. Ve **otomatik vekil metrik YOK**: `faithfulness < 0,6`
süzgeci 4 buluyor, *"altın madde atıflarda yok"* süzgeci 3 — **göz 8** buluyor (ADR-0066).

**Alet HAZIR:** `scripts/veri_hazirlik/b10_hasat.py` · Modal `harvest_b10` (ADR-0047 m.2, L4'te doğrulanmış) ·
sızıntı süzgeci (13.350 → 12.914, konteynerde bayt-özdeş). **Yeniden kurulmaz.**

- **ATLANDI** · **Adım 1: Ön-kayıt — hedef bandı ve durma kuralı, KOŞUDAN ÖNCE**
`verify:` ADR'de hedef bant, durma kuralı ve *"kaç kalem kazanç $X'e değer"* eşiği yazılı.
B10 turunun dersi: hedef **iki kalemlik** bir boşluğa daralmıştı ve tur **kapatıldı**.

- **ATLANDI** · **Adım 2: Hasat** (Modal, AYRIK) — `verify:` kabul oranı + sızıntı süzgeci sayıları künyede.
- **ATLANDI** · **Adım 3: Eğitim** — `--fresh-adapter` **ZORUNLU** (`τ = θ_ft − θ_base`; adaptörden devam
etmek **ardışık SFT** üretir, task-vector değil). `verify:` künyede `fresh_adapter: true`.
- **ATLANDI** · **Adım 4: Merge (ham TIES) + GGUF** — `verify:` `‖τ‖` ölçüldü ve `kollar.md`'ye satır eklendi.
- **ATLANDI** · **Adım 5: Ölç + GÖZLE OKU** — `verify:` isabetsizlik **gözle** sayıldı; alet↔göz deltası yazıldı.
- **ATLANDI** · **Adım 6: Commit + `kollar.md` + `research_log`**

---

### Görev 15: `B4` — `τ_a` genliği **ATLANDI 2026-09-08 (ADR-0075)**

> **KOŞULMADI — ve sebebi G14'ünkinden farklı.** `B4` bir **merge** kaybıdır, eğitim
> kalitesi sorunu değil: `τ_a` **tek başına M2b 0,987**, merge sonrası **0,766**.
> `v2` **sequential** mimariye geçiyor (ADR-0075) ⇒ **merge yok** ⇒ aynı **22,1 puan**
> ödenmeden geri gelir. Bu turu koşmak, birkaç hafta sonra **terk edilecek bir mimariyi
> onarmak** olurdu.
> Teşhis (**genlik**, `‖τ‖` oranı **8,87×**) kayıtta kalır: merge mimarisine dönülürse
> ilk okunacak yer burasıdır.

**Neden (ölçüldü):** merge'de `τ_a` **0,987 → 0,766** seyreliyor (−22,1 p). Teşhis **genlik**:
70 adım @1e-5 → `‖τ_a‖` **1,1806** ↔ `‖τ_g‖` **10,4722**, oran **8,87×**.
Kaldıraç: **aynı ORPO ile daha çok adım / daha yüksek lr**.
Yöntemi de değiştirmek **iki değişkeni birlikte** oynatır (ADR-0017).

- **ATLANDI** · **Adım 1: Ön-kayıt** — hangi `‖τ_a‖` değeri hedefleniyor, hangi M2b eşiği bekleniyor.
- **ATLANDI** · **Adım 2: Eğitim** (`--fresh-adapter`) — `verify:` `‖τ_a‖` **ölçüldü ve raporlandı**.
- **ATLANDI** · **Adım 3: Merge + M2b ölçümü** — `verify:` merge sonrası M2b **yeni çıpanın üstünde**.
- **ATLANDI** · **Adım 4: Commit**

---

### Görev 16: `v1.0` kapı koşusu + kabul testi — **KAPANDI 2026-09-09** · 4/4

Donmuş TEST (`data/eval/canon/`, n=40) **insan onayıyla, TEK KEZ açıldı**; rejim DEV koşusunun
her ekseninde birebir, araçsız (ADR-0076 m.4).

| | **TEST** (40, donmuş) | DEV (80) |
| :--- | ---: | ---: |
| **ham kütle — MANŞET** | **0,5804** | 0,8011 |
| `recall@10` = tavan | **0,7500** | 0,9500 |
| tavan kullanımı | **0,7739** | 0,8433 |
| **uydurulmuş madde no** | **0/52** | 0/114 |
| `wrong_ref_rate` | **0,2424** | 0,0769 |

Düşüşün **%76'sı setin erişim tavanından**, %24'ü değil. Gözle okuma kapısı: 9/40 çekinmenin
dokuzu da okundu, **yanlış pozitif 0**.

**Hüküm: `v1.0` VERİLMEDİ, ürün sürümü `v0.3`.** Engel modelin başarımı değil **ölçüm aygıtı**
(tek hakem ailesi, κ 0,534). Donmuş TEST için **ön-kayıtlı sayısal eşik YOKTU** — bu bir
bulgudur, mazeret değil; sayı görüldükten sonra eşik yazmak ADR-0050'nin yasakladığı şeydir.

**Donmuş TEST bir kusur yakaladı ve TDD ile onarıldı:** `atif_dogrula.py` çok anlamlı kanun
adlarında **doğru cevaba MÜLGA damgası** vuruyordu (id 32, altın 1. sırada).

→ tam metin: [kapanan görevler](../../record/2026-09-10-hp-hat-a-hat-b-kapanan-gorevler.md) §G16 · [ADR-0077](../../adr/0077-v1-0-verilmedi-v0-3.md) · [ADR-0069](../../adr/0069-kabul-testi-tavan-kullanimi-raporlamasi.md) · [#65](../../record/research_log/2026-09-09-kabul-testi-ve-frontier-kiyasi.md)
### Görev 18: Araç katmanı — KALDIRAÇ — **KAPANDI 2026-09-09** · 7/7

**Bu görevin ilk gerekçesi ölçüldü ve ÇÜRÜDÜ:** isabetsizlik (8/80) ve aşırı-red (4/80)
kalemlerinin **hepsinde altın madde zaten bağlamdaydı** ⇒ sorun erişim değil **seçim**.
Aracın ölçülmüş tek hedefi kaldı: **4/80 recall kaybı**.

**KAPI ↔ KALDIRAÇ ayrımı bağlayıcı** (ADR-0076): atıf doğrulama · mülga süzgeci · durum
sınıflandırma **tool DEĞİLDİR**, döngü dışında koşulsuz çalışır — **0/114** garantisi oradan
gelir ve tool yapılsaydı model çağırmayı unuttuğu an buharlaşırdı.
Beş deterministik kaldıraç · **sınırlı** döngü · sınıra dayanmak **görünür** (`ARAMA_TUKENDI`).
**Regresyon kapısı GEÇTİ: araçsız davranış 80/80 birebir.**

**Yan ürünü bir ürün kusuru ortaya çıkardı:** ürün yolu ile ölçüm hattı aynı şeyi
çalıştırmıyor — ürün yolunda **4/80 cevap tamamen BOŞ**. Düzeltmesi bir rejim değişikliğidir
⇒ bugün düzeltilmedi, **açık kusur 1** olarak duruyor.

→ tam metin: [kapanan görevler](../../record/2026-09-10-hp-hat-a-hat-b-kapanan-gorevler.md) §G18 · [ADR-0076](../../adr/0076-kapi-kaldirac-ayrimi-arac-katmani.md)
### Görev 17: Modeli YAYINLA — **KAPANDI 2026-09-09** · 4/4

**Plan bunu HİÇ içermiyordu; insan sorusu ortaya çıkardı:** kod, veri ve araştırma kaydı
public'ti ama **ağırlıklar yalnız yerel diskteydi** ⇒ *"açık kaynak model"* iddiası yarımdı.
`HakHukuk-4B-v0.3-Q4_K_M.gguf` HF'e yüklendi ve **bütünlük ölçüldü, iddia edilmedi**:
`sha256 755e15e9…` · **2.783.446.720 bayt**, yereldeki artefaktla birebir.
Kartın ilk üç bölümü kısıtları taşıyor: model **tek başına yayımlanan sayıyı ÜRETEMEZ**
(indeks dağıtılmadı, Görev 8) · ürün yolunda **~%5 boş cevap** · hukuki tavsiye değildir.
**Depo bugün ÖZEL** — insan kararı 2026-09-09; geri alınan yalnız **görünürlüktür**.

→ tam metin: [kapanan görevler](../../record/2026-09-10-hp-hat-a-hat-b-kapanan-gorevler.md) §G17 · [ADR-0071](../../adr/0071-v1-release-artefakti-tek-gguf.md)
## `v2` — bundan SONRAKİ tur (bu planın DIŞINDA)

> Karar: [ADR-0075](../../adr/0075-v1-sft-kapanir-v2-sequential-rl.md) · plan **henüz yazılmadı**.

```
v1  ham base ──► SFT (τ_g) + ORPO (τ_a) ──► ham TIES ──► tgta_v1 ──► YAYIN  ← bu plan
v2  tgta_v1 (bf16, models/merged/tgta_v1/, 8,8 GB) ──► GRPO + düşünce ayarı ──► v2.0
```

**Neden RL bu hatta mümkün:** **doğrulanabilir ödül hazır** — `hakhukuk/terazi.py` atıf
doğrulamasını **deterministik** yapıyor (atıf getirilen kaynakta var mı: evet/hayır).
Reward model **gerekmiyor**, LLM-hakem bedeli **yok**.

**Ön koşul (ADR-0075 m.4):** ödül fonksiyonu **çekinmeyi korumak zorunda**. ADR-0010 ölçtü —
düz SFT abstention'ı **yok etti**; RL'de risk daha keskindir. Korunacak taban:
uydurulmuş madde **0/114** · aşırı-red **4/80** · kütle **0,8011**.
Tur başlamadan ödül fonksiyonu + hedef bant + **durma kuralı** ön-kayıtlanır (ADR-0050).

---

## AÇIK KARARLAR — tam bağlam *(`docs/open_questions.md` 'den devralındı 2026-09-07)*

> Dosya silindi: 18 sorunun 9'u kapanmıştı ve kapanışları zaten ADR'lerde yazılı.
> Canlı 9'u **buraya**, karar için gereken tam bağlamıyla taşındı. **Tek kaynak burasıdır.**
> Bir damga **kendi başına kapatılamaz** — kapanış insan kararıdır ve bir ADR'ye yazılır.

### S5 — **KAPANDI 2026-09-07** *(insan kararı)*

> **Karar: Wilson %95 aralığı RAPORLANIR, kapı kuralı DEĞİŞMEZ.** Hüküm nokta tahminle kurulmaya
> devam eder; aralık **yanında** yayımlanır.
> **Gerekçe ADR-0050:** kapı sayıları **üretildikten sonra** kural değiştirmek, eşiği sonuçtan
> sonra oynatmaktır — yönü lehimize bile olsa. Aletin düzeltilmesiyle **eşiğin** değiştirilmesi
> ayrı şeylerdir; bu ikincisidir.
>
> **Hesap $0 ve YAPILDI** (`z=1,96`, `n=80`):
>
> | oran | pay/payda | nokta | Wilson %95 | genişlik |
> | :--- | ---: | ---: | :--- | ---: |
> | coverage BİZ | 75/80 | 0,9375 | [0,862 – 0,973] | 11,1 p |
> | coverage 3.5 Flash | 67/80 | 0,8375 | [0,742 – 0,903] | 16,1 p |
> | **isabetsizlik çıpası** (madde 2) | 8/80 | 0,1000 | **[0,052 – 0,185]** | **13,4 p** |
> | M5 coverage BİZ | 76/80 | 0,9500 | [0,878 – 0,980] | 10,2 p |
> | M5 coverage base | 78/80 | 0,9750 | [0,913 – 0,993] | 8,0 p |
>
> **İki şerh ZORUNLU oldu ve kapı hükmünün yanında durur:**
> 1. **Madde (2)** *"gerileme yok"* diyor, ama 8/80'in aralığı **[4/80 – 15/80]** ⇒ **tek kalemlik**
>    oynama anlamlı fark değildir; sonraki turda bu kuralın çözünürlüğü yeniden konuşulmalı.
> 2. **Madde (3)**'ün ikili ayağında aralıklar **ÖRTÜŞÜYOR** (BİZ [0,878–0,980] ↔ base [0,913–0,993])
>    ⇒ *"M5 yükselmedi"* hükmü **nokta tahmine** dayanıyor. Bu, hükmü geçersiz kılmaz ama
>    **damgalanır**.
> **Madde (1)'e Wilson doğrudan UYGULANAMAZ:** `kütle = coverage × A1`, yani ikili bir oranla
> sürekli-skorlu bir makronun çarpımı — binom modeli yanlış olur.


**Soru:** **İkili oran çözünürlük sınırı**

**Seçenekler / girdiler:** (a) `k` kalem kuralı · (b) ölçülmüş taban (hakem maliyeti var) · (c) Wilson aralığı ($0, kapı kuralını değiştirir)

**Bağlı olduğu:** ⬇️ **OQ-2**

### S7 — **KAPANDI 2026-09-07** *(insan kararı)*

> **Karar: adaptörler YÜKLENMEZ. Yayımlanan tek şey merge edilmiş GGUF'tur** — kullanıcı onu
> indirir ve doğrudan kullanır (ADR-0071 ile aynı yönde).
>
> **Olgu düzeltmesi:** T1'in *"adaptör yedeği ön koşuldur"* gerekçesi **ölçümle çürüdü**. T1 yalnız
> **reddedilmiş varyantları** siliyor (`merged/tg_ta_modulmin` + `merged/tg_ta_globalmin` +
> `gguf/cp2s-ties-smoke` = **20,2 GB**); `tgta_v1` · `tg_v1` · base **korunuyor**. Disk baskısı da
> yok (839 GB boş). ⇒ **T1, S7'ye kilitli değil.**
>
> **KABUL EDİLEN BEDEL — yazılmadan geçilmez:** GGUF yayımlanınca **merge edilmiş model**
> yedeklenmiş olur, ama `outputs/tg_v1` ve `outputs/ta_v1` **tek kopya** kalır. Ve `τ_g`'nin
> komut künyesi **yok** (`kollar.md`:76-78 kabul ediyor: `--data` argümanını gösteren künye
> yok, `raft_scrubbed` seçimi **davranışsal çıkarım**). ⇒ Adaptörler kaybolursa `τ_g`
> **yeniden üretilemez** ve *"merge ağırlığını değiştirip yeniden birleştirelim"* denemez.
> `kollar.md`'nin *"yeniden üretilebilir"* gerekçesi bu kol için **kanıtlanmış değildir**.
> 12B hattında bu tam olarak yaşandı: adaptörler **kalıcı kayıp**.


**Soru:** **LoRA adaptörleri HF'ye yüklensin mi?**

**Seçenekler / girdiler:** `kollar.md`'nin *"adaptörler yedeklenmiyor — bilinçli"* kararını **değiştirir** → **ADR gerekir**. 12B hattında adaptörler **kalıcı kaybedildi**; HF yayını ilk gerçek yedek olur

**Bağlı olduğu:** [`record/kollar.md`](../../record/kollar.md) · [ADR-0034](../../adr/0034-emekli-hat-artefaktlarinin-repodan-cikarilmasi.md)

### S8 — **KAPANDI 2026-09-07** *(insan kararı)* ⇒ **Görev 8 açıldı**

> **Karar: (a) HF dataset'ten indirilir.** `huggingface_hub==1.18.0` **zaten bağımlılık**
> (`requirements.lock.txt`:31) ⇒ yeni bağımlılık yok.
>
> **Planın etiketi YANLIŞTI ve düzeltildi.** *"(b) kurulumda üret (~10 dk)"* diyordu; o **10 dk
> GPU'da** ölçülmüş (`outputs/eval/s3a-on-prob/recall_BAAI_bge-m3.json`: `cihaz: cuda`,
> `gecen_sure_s: 625.3`). **Ürün yığını CPU** ⇒ gerçek bedel **~2 saat 45 dk**
> (`recall_olc.py`:74 ölçülmüş yorum: ~4,1 madde/sn × 40.496) **artı** `BAAI/bge-m3` **4,3 GB**
> indirme. Karşısında (a): **79,1 MiB**.
>
> **YENİ KOD BORCU — hiç sorulmamıştı, olgu taramasında çıktı.** İndeksin `KUNYE.json`'u
> **mutlak yol + `(bayt, mtime)`** kilidi taşıyor ve `retriever.py`:143-152 yüklemede bunu
> doğrulayıp uymazsa `SystemExit` veriyor. ⇒ **Her iki seçenek de bugün başka makinede ÇÖKER**:
> yol yok, ve `git clone` sonrası `mtime` checkout zamanı olur. Künyenin kendi
> `mtime_duzeltme_notu` alanı bu vekilin *"içerik-korumalı dokunuşlarda yanlış alarm verdiğini"*
> zaten yazmış. ⇒ **Görev 8'in ilk adımı bu kilidi taşınabilir hâle getirmektir**
> (mutlak yol → göreli/içerik hash'i). Bu kod borcudur, insan kararı değil.
> Ayrıca künyede **önek sözleşmesi** yazılı değil (kural `retriever.py`:80-90'da) ve
> `bge-m3`'ün **revision/hash'i** yok — dağıtılan indeksin yeniden üretilebilirliği için ikisi de eklenmeli.


**Soru:** **İndeks nasıl dağıtılır?** (80 MB)

**Seçenekler / girdiler:** (a) HF dataset · (b) kurulumda üret (~10 dk)

**Bağlı olduğu:** v1 §C5

### S9 — bloke ettiği: bu planın **dışında** (`v2`)

**Soru:** **v2 nasıl barındırılır?**

**Seçenekler / girdiler:** (a) yalnız self-host · (b) + hız-sınırlı vitrin (~$100-300/ay) · (c) hosted-first **mahremiyet vaadini zayıflatır** **TR IP** kısıtı bulut barındırmayı da kısıtlayabilir

**Bağlı olduğu:** taslak §4.1 · [`BEDESTEN_API.md`](../../BEDESTEN_API.md)

### S10 — **KISMEN KAPANDI 2026-09-07** *(insan kararı)*

> **Karar: muhafazakâr GEÇİCİ metin şimdi girer, TEK kaynakta.**
> `hakhukuk/cli.py` içinde tek sabit (`SORUMLULUK_IBARESI`); `hakhukuk/tui.py` onu **import
> eder**, kopyalamaz (S18'in dersi: aynı metin iki yerde durursa sessizce ayrışır).
> Metin bilerek **fazla temkinli**: *"hukuki tavsiye değildir · bilgilendirme amaçlıdır ·
> avukata danışın"*. `Durum` ne olursa olsun **koşulsuz** basılır.
> **Hâlâ açık olan:** nihai hukuki metin — **hukukçu görüşü** gerekiyor. Geldiğinde
> **tek yerden** güncellenir. Kodda ve model kartında *"GEÇİCİ — S10 açık"* şerhi durur.
> ⇒ **Görev 10 ve Görev 12 açıldı.**


**Soru:** **Avukatlık Kanunu / hukuki sorumluluk sınırı**

**Seçenekler / girdiler:** **hukukçu görüşü gerekir** — repo'da hiç değerlendirilmemiş

**Bağlı olduğu:** taslak §4.6

### S12 — **ERTELENDİ 2026-09-07** *(insan kararı, gerekçeli)*

> **Karar: `τ_a` v2 turuna ertelendi.** Şimdi $1 ve 50 dk harcanmaz.
>
> **Planın eşlemesi YANLIŞTI:** *"bloke ettiği: Görev 13"* yazıyordu, ama **Görev 13 belge
> yazımıdır**, taşıyıcı değil. KARAR-6'nın gerçek tüketicisi `τ_a` v2 hasadıdır — **bu planda yok**.
> ⇒ `v1.0` kapısının üç maddesinden **hiçbiri** buna bağlı değil.
>
> **Olgu:** bozuk ölçüt **onarıldı** (commit `463e8da`, 2026-09-06); `b10_hasat.py`:63 onarılmış
> `exact_reject`'i **import ediyor** ⇒ düzeltme hasada otomatik yansıyor. Yeniden koşma bedeli
> **ölçülmüş**: ~50 dk Modal L4 / **~$1**, hakem **$0**, Modal bakiyesi **$29,19** ⇒ bütçe engeli yok.
> Soru **hazır**, yalnız sırası gelmedi.


**Soru:** **KARAR-6 — paralel slot (`-np`)**

**Seçenekler / girdiler:** sayılar geldi (Jaccard **0,5278** · birebir **3/19**) **bozuk ölçütle toplandı** → ölçüt onarılınca **yeniden koşulur**, hükmü **insan** kurar

**Bağlı olduğu:** [#60](../../record/research_log/2026-09-06-hasat-kabul-olcutu-coktu.md)

### S16 — **KAPANDI 2026-09-07** *(insan kararı)*

> **Karar: TEK `anthropic/claude-*-sonnet*` sınıfı özne.** Gerekçe bütçeden ve aile
> dışlamasından birlikte çıktı: ölçülen bakiye **$6,60**, `HP` tek başına ~$3-5 yiyor.
> Anthropic öznesi **aile dışlamasına takılmıyor** ⇒ bugünkü dört sayı **yeniden koşulmaz**;
> bedeli ~**$0,35**. Bir özne *"başka sağlayıcıyla da kıyaslandı"* cümlesini **kurar**;
> üç özne bunu daha güçlü yapmaz ama bakiyeyi yer.
> **GPT sınıfı DIŞARIDA kalıyor** ve bu `v1.0` yayınında **eksiklik olarak yazılır** —
> sebebi bütçe değil **usul**: GPT öznesi hakemi değiştirir (ADR-0032).
> ⇒ **Görev 4 açıldı.**


**Soru:** **`v1.0` rakip havuzunda hangi sağlayıcı(lar), kaç özne?** Havuzun genişlemesi **karara bağlandı** (insan, 2026-09-07) ama **kimin ekleneceği** açık. Şekli **aile dışlaması** belirliyor: hakem `openai/gpt-4o-mini` olduğu için bir **GPT öznesi** hakemi değiştirmeyi **ve bugünkü dört sayıyı yeniden koşmayı** gerektirir; Anthropic öznesi sorunsuz. Bedel öznebaşı ~$0,35 (F0.4'te ölçüldü: üç çıpa $1,35). Eşik **oynamaz** — çıpa `3.5 Flash` kalır, yeni özneler yalnız **raporlanır**.

**Seçenekler / girdiler:** ⇒ **T1 (hakem paneli) ön koşul** · [ADR-0072](../../adr/0072-v1-rakip-havuzu-genisler.md) · [ADR-0032](../../adr/0032-hakem-paneli-uc-aile-ve-aile-dislama.md)

### S17 — bloke ettiği: bu planın **dışında**

**Soru:** **Kuantizasyon eğrisi ölçülsün mü?** `v1.0` **tek** artefakt yayımlıyor: `Q4_K_M` (ADR-0071). `Q5_K_M`/`Q8_0`'ın kütle kaybı **bilinmiyor** — ADR-0031 çıkarım hassasiyetini *seçti* ama **kaybı ölçmedi**. Her kuantizasyon **ayrı artefakttır** ve ADR-0057'nin eşit sınavı gereği **kendi kapı koşusunu** ister ⇒ üç nokta = üç kat ölçüm. ADR-0018'in *"tek nokta, eğri değil"* bedeliyle **aynı sınıf**.

**Seçenekler / girdiler:** [ADR-0071](../../adr/0071-v1-release-artefakti-tek-gguf.md) · [ADR-0031](../../adr/0031-precision-inference-q4km-egitim-bf16-lora.md) · [ADR-0018](../../adr/gemma4-12b-dersler.md#adr-0018)

### S18 — **KAPANDI 2026-09-07** *(iki katmanı da)* ⇒ **Görev 5 açıldı**

> **Katman 2 — *"`τ_g` çift-system ile mi eğitildi"* — OLGUYLA kapandı, insan kararı gerekmedi.**
> Planda *"diskten cevaplanamıyor"* yazıyordu; **yanlıştı**. Qwen3.5 sohbet şablonu
> (`outputs/ta_v1/chat_template.jinja`:83-86) iki `system` mesajına
> **`TemplateError: System message must be at the beginning`** veriyor — birleştirmiyor, ikisini
> de basmıyor, **hata veriyor**. Ve `raft_scrubbed/train.jsonl`'in **17.323/17.323** satırının ilk
> mesajı `system`. ⇒ `--no-system` verilmeseydi koşu **ilk örnekte çökerdi** ve
> `outputs/tg_v1/adapter_model.safetensors` (1.083 adım, `‖τ_g‖=10,4589`) **hiç oluşmazdı.**
> **Hüküm: `τ_g` çift-system ile eğitilmedi.** Kanıt künye değil, **yapısal imkânsızlık**.
> Tek artık belirsizlik: `tg_v1` kendi tokenizer'ını kaydetmemiş; render 6 gün sonraki
> `ta_v1` kopyasıyla yapıldı (aynı base). Şablon o 6 günde değiştiyse çıkarım zayıflar — **düşük
> olasılık, diskten kapatılamıyor.**
>
> **Katman 1 — hangi metin kanon: ÖLÇÜLEN SÜRÜM.**
> `hakhukuk/istem.py::SISTEM_KOR` = `gen_eval_grounded.py`:39'un metni, son satırı
> *"Cevabını kısa ve anlaşılır tut; ilgili kanun ve madde numarasını belirt."*
> **Gerekçe:** yayımlanan **%80,1 dâhil bütün sayılar** bu metinle üretildi; başka bir metni kanon
> yapmak yayımlanan sayıyı **yeniden üretilemez** kılardı.
> ⇒ `train_sft.py`:31'deki sürüm **ÖLÜ KOD** — olgu taramasıyla doğrulandı: hiçbir artefakta
> girmemiş (v2b reçetesi `--no-system`'i zorunlu kılıyor **ve** RAFT verisinde çalışması fiziksel
> olarak imkânsız). **Görev 5'te silinir.**
> ⇒ Feragat cümlesi isteme **girmez**; S10 gereği **çıktı yüzünde** ayrı satır olarak durur —
> ikisine birden koymak mükerrer olurdu.


**Soru:** **Sürüklenmiş `SYSTEM_PROMPT`'un hangi hâli doğru — ve `τ_g` çift-system ile mi eğitildi?** Ölçüldü 2026-09-07: `SYSTEM_PROMPT` **iki yerde tanımlı ve aynı değil** — ölçüm (`gen_eval_grounded.py`) *"…ilgili kanun ve madde numarasını belirt."* ile bitiyor, eğitim (`train_sft.py`) *"Bu yanıt hukuki tavsiye değil, bilgilendirme amaçlıdır."* ile. Bu **M5'in kör-mod istemidir**. İkinci katman: eğitim verisi (`raft_scrubbed/train.jsonl`) **zaten `system` rolü taşıyor**, `train_sft.py` ise `--no-system` verilmedikçe başa **bir tane daha** ekliyor (`modal_train.py` varsayılanı `no_system=False`; bayrağın yardım metni *"v2b ZORUNLU — veri system'i zaten taşır"* diyor). `τ_g v1` koşusunda verilip verilmediği **diskten cevaplanamıyor**: `outputs/tg_v1/` yalnız `adapter_config.json` + ağırlık taşıyor, **koşu künyesi yok**.

**Seçenekler / girdiler:** **Hat A / A1'in ön koşulu** — beş kopya tek kaynağa inerken hangi metnin kanon olduğu insan kararı. `τ_g`'yi yeniden eğitme gerekçesi **değildir**; bulgu **kayda geçer**, düzeltme sıradaki tura yazılır.

**Bağlı olduğu:** [spec §5 damgası](../specs/2026-09-06-yeni-belge-katmani-design.md) · `scripts/egitim/train_sft.py`:31,202 · `scripts/olcum_uretim/gen_eval_grounded.py`:39 · [`kollar.md`](../../record/kollar.md)

---

## 📋 AÇIK BORÇ KUYRUĞU — `DEVIR-PROMPT.md` *(silindi)* §5'ten devralındı (2026-09-07)

> §5'in kendi cümlesi *"yeni roadmap bunları taşımalı"* diyordu. `DEVIR-PROMPT.md` *(silindi)* silindi;
> kuyruk **buraya** taşındı. Durum sütunu **bugün** yeniden değerlendirildi.

| # | borç | ölçülen büyüklük | bugünkü durum |
| :-- | :--- | :--- | :--- |
| **B1** | **İsabetsizlik** — gerçek ama soruya uymayan maddeden cevaplama (`ADR-0055`) | ~~5/80~~ → **8/80** *(v2 birimi, ilk kez gözle)* · **frontier kıyası 2026-09-09:** `wrong_ref_rate_micro` **0,0769 ↔ 0,0083 = 9,3×** | **`v2`'ye DEVREDİLDİ** (ADR-0075) — Görev 14 **atlandı**; **kusur 6** bu borcun ürün yüzündeki adıdır. Canlı örnek 2026-09-10: TBK **330** (taşınır kirası) seçildi, doğru cevap aynı kaynak listesindeki **347**'deydi |
| **B4** | `τ_a` merge'de seyreliyor (0,987 → 0,766, **−22,1 p**); çare eğitim **genliğinde** | `‖τ_a‖` **1,1806** ↔ `‖τ_g‖` 10,4722 (8,87×) | **Görev 15** |
| **YB2** | M2b bir **eğitim** borcu — kapı yolu ölçülerek öldü | `h2b@k=4` **0,735 < 0,766** | **Görev 15 Adım 3** |
| **YB6** | 🔴 **Dağıtım istemi artefaktı YOK** | istem 5 dosyada, biri **sürüklenmiş** (S18) | **Görev 5** — sert engel |
| **B11** | 🆕 **Eğitim verisinin iskele işaretleri modele ÖĞRETİLDİ** — `##begin_quote##` cevabın gövdesinde vatandaşa gidiyor | kaynak **istem değil**: `gen_v2b_answers.py`:36-37 öğretmene böyle söylüyor, `build_sft_v2b.py`:57 bloğu koruyor | **`v2`** — düzeltmesi yeniden eğitimdir. `v1`'de yalnız **sunum katmanında süzülür** (Görev 21 Adım 4); ⛔ ölçüm hattı dokunulmaz, `score_register.py`:41 işareti **register göstergesi sayıyor** |
| **B8** | Katı kapı **tek karakterlik yazım hatasına** takılıyor (`…ESELERİ…`) | **1/80** · eğri ölçüldü, tolerans **BENİMSENMEDİ** (risk tarafında **0 gözlem**) | **açık, planda YOK** — düşük öncelik, ama kaydı burada |
| **B9** | Tablo/cetvel parçaları madde diye indeksli (~**7.966** satır) | modele **0/800** blok ulaşıyor | **v2** — indeksi değiştirir, yeniden indeksleme turuyla paketlenir |
| **B6** | **Canlı `bedesten` katmanı yok** — sözleşme **4/4 geçerli**, ürün çağırmıyor | **TR IP şart** (gov firewall yurtdışı/VPN'i bloke ediyor) | **v2** |
| ~~B10~~ | Aşırı-red | 9/80 → **4/80** | **kapandı** — [ADR-0062](../../adr/0062-b10-turu-kapatildi-hedef-egitimsiz-karsilandi.md) |
| ~~YB3~~ | `k`'nın çekinme ekseni **TANIMSIZ** (`SOURCE_CLIP=3500`) | ödendi **$0,78** | **kapandı** — `SOURCE_CLIP=12000`, `gecerlilik_devralinan` 65→0 |
| ~~B2·B3·B5·B7~~ | — | — | kapandı |
| **ARA KAPI** | **DÜŞTÜ** 2026-08-06: merge M2b **0,766** ↔ eşik **0,8649** → **9,9 p** altında | paydalar eşit (77↔77) | **CP4-CP5 yetkisi YOK.** Ürün sürümü ayrıldı ([ADR-0065](../../adr/0065-bolunmus-surumleme.md)); **iddia sürümü** buna bağlı kalır |

---

## BORÇ: eval setinde ALTIN ETİKET şüphesi — id 46 *(2026-09-07)*

**İki bağımsız gözle okuma, birbirinden habersiz, AYNI kalemi işaretledi ve AYNI şüpheyi kurdu.**

| kalem | altın etiket | modelin dayandığı | şüphe |
| :--- | :--- | :--- | :--- |
| **id 46** | KMK **53** *(1965 öncesi irtifak haklarına dair **geçiş hükmü**)* | KMK **14** | KMK 14 **lafzen** *"Kat mülkiyetine geçişte ayrıca yönetim plânı istenmez"* diyor ⇒ **soruyu doğrudan karşılıyor** |

⇒ Üç kolda da bu kalem *"isabetsizlik mi, altın etiket hatası mı"* diye **sınır durum** sayıldı ve
**hiçbirinde sayıya katılmadı**. Yani bugün **üç öznenin de sayısı bu kalem yüzünden alt sınırda**.

**Neden ciddi:** eğer altın etiket yanlışsa, bu bir **model kusuru değil ölçüm kusurudur** ve
Faz 0'ın bulduğu beş kusurla **aynı sınıftandır** (*"hata vermeden yanlış sayı üretir"*).
**Bugün düzeltilmedi** — ADR-0067'nin soru onarımı **insan onayıyla** yapılmıştı; altın etiket
değiştirmek de aynı usulü ister ve **donmuş TEST'i de ilgilendirir**.
**Yapılacak:** hukuk metnine bakılarak KMK 53 ↔ KMK 14 kararı verilir; değişirse ADR + üç öznenin
sayısı yeniden okunur (yeniden **koşulmaz** — yalnız gözle sayım güncellenir, $0).

---

## Bu planın DIŞINDA

- **T5** `scripts/` alt-klasör düzeni — **Faz 0 planı Görev 9**'da yazılı, 8 adım.
  Görev 5 Adım 6'nın **ön koşulu** T5 Adım 2'dir (`sys.path` deseni).
- **T1** `models/` ~20 GB — ön koşulu **AÇIK KARAR S7**.
- **S17** kuantizasyon eğrisi · **S9** `v2` barındırma · **Hat C** metodoloji paper'ı.
- **`exact_reject`'in kör mod dalı** — *"…bulunmamaktadır"* ailesi kör modda red sayılmamalı.
  Faz 0'da **bilerek düzeltilmedi** (kapının sayısı üretildikten sonra aleti değiştirmek
  ADR-0050'nin sınırında). Sıradaki turda **koşudan ÖNCE** düzeltilir.
- **`recall_taban.json`** — Faz 0'ın tek *"kaynaklanmadı"* ihlali; ölçüm mevcut rejimde
  ($0, ~15 dk) yeniden koşulup dosya **gerçekten** üretilir.

---

### Görev 19 : HTTP API — `answer()` üstünde ince kabuk *(insan kararı 2026-09-09)*

**Dosyalar:** Create: `hakhukuk/api.py` · `tests/test_api.py` · Modify: `pyproject.toml`

**KAPSAM İNSAN KARARIYLA GENİŞLETİLDİ ve çelişki iki yerde damgalandı.** Bu planın başlığı
`v0.2 → v0.3`'tür ve [`00-IS-SIRASI.md`](../00-IS-SIRASI.md) bugüne kadar *"CLI + TUI yeterli
(insan kararı) — HTTP API ve web arayüzü **v2**"* diyordu. O cümle **artık geçerli değil**:
API `v1` tarafına alındı. Gerekçe teknik değil, insan tercihidir; öyle yazılır.
**S9 AÇILMADI:** API **yerel ve tek kullanıcı**dır (`127.0.0.1`). Barındırma, kimlik, hız
sınırı ve mahremiyet vaadi soruları **açılmıyor** — S9 `v2`'de açık soru olarak duruyor.

**Neden ince kabuk.** `cli.py` ve `tui.py` ile aynı ilke: API'nin **kendi mantığı olmaz**.
Sınıflandırma, atıf doğrulama ve kaynak seçimi `answer()`'ın içindedir; API yalnız taşır.
`SORUMLULUK_IBARESI` `cli.py`'den **import edilir, kopyalanmaz** (S18'in dersi: aynı metin iki
yerde durursa sessizce ayrışır).

**Kilitlenen altı karar — grill oturumu, 2026-09-09:**

| # | karar | gerekçe |
| :--- | :--- | :--- |
| 1 | **Yerel, tek kullanıcı** (`127.0.0.1`, kimlik yok) | S9'u açmaz, mahremiyet vaadine dokunmaz |
| 2 | Yapısal alanlar **+ hazır `sunum` dizesi** | Tembel tüketici tek alanı bassa bile rozet + atıf + kaynak + ibare gider; dürüstlük sözleşmesi HTTP'de düşmez |
| 3 | Yalnız **`answer()`** | `answer_arac()` taşıyıcıda araç çağrısı ayrıştırmıyor ⇒ açılırsa tüketici araç kullanıldığını **sanır** |
| 4 | Boş metin → **503**, dolu KESİK → **200** | *"HTTP 200 ile boş içerik"* bu hattın #42'de ölçtüğü kusurun adıdır; sınırı geçmesine izin verilmez |
| 5 | Boş/boşluk sorgu → **422** | Ölçüldü: `_getir("")` sabit gürültü döndürüyor. Uydurulmuş uzunluk eşiği **YOK** |
| 6 | **Serileştirilmiş** tek istek · opsiyonel ekstra `hakhukuk[api]` | Tekilin evre güvenliği **ölçülmedi**; ölçüm rejimi sıralı istekti. Çekirdek kurulum şişmez (`pyproject.toml` ilk satırındaki karar) |

- [x] **Adım 1: Failing test** BİTTİ **2026-09-10** — `tests/test_api.py`, 14 test, `TestClient` ile, **sunucu ve model YOK**
(`servis.answer` monkeypatch'lenir). Sınanacaklar: `sunum` dizesi dört parçayı da taşıyor ·
boş sorgu 422 · boş metin 503 · dolu KESİK 200 · API'nin kendi mantığı yok (kaynak denetimi).

- [x] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör** BİTTİ **2026-09-10** — **8 failed + 6 error**, `api.py` yoktu

- [x] **Adım 3: Bağımlılığı opsiyonel ekstra olarak ekle** BİTTİ **2026-09-10** — `fastapi 0.141.1` · `uvicorn 0.52.4`, sürümler **kurulu ortamdan okundu**
`verify:` `pip install -e .` çekirdek bağımlılıkları **değiştirmiyor**; `[api]` ekstrası
`fastapi` ve `uvicorn`'u getiriyor, sürümler **kurulu ortamdan okunarak** pinlenir.

- [x] **Adım 4: `hakhukuk/api.py` — uygulama** BİTTİ **2026-09-10**
`verify:` her altı karar testle çivili; `api.py` içinde `REJECT_RE`, `siniflandir(`, `_getir(`
geçmiyor (ince kabuk kapısı, `test_tui.py`'nin aynısı).

- [x] **Adım 5: Testi koş, GEÇTİĞİNİ gör + commit** BİTTİ **2026-09-10** — **178 test yeşil** (164 → +14), 2 xfail · commit `0f02896`

**Alet dersi, kayda geçti:** `pyproject` testinin ilk sürümü **metin araması** yapıyordu ve
`[project.optional-dependencies]` başlığından önceki bir **yorum satırındaki** *"fastapi"*
geçişine takıldı — kodu değil **aleti** yanılttı. `tomllib` ile yapı okunacak biçimde
düzeltildi. Bu hattın bilinen sınıfı: *"hata vermeden yanlış"*.

- [ ] **Adım 6: Gözle doğrula** — `hakhukuk-api` ile aç, bir soru sor, cevabı **gör**.
`verify:` `sunum` alanı ekranda rozet + atıf + kaynak + ibare taşıyor; boş sorgu 422 dönüyor.
Bu da bir **insan gözü kapısıdır** (SIRA 2 ile aynı sınıf).

**Bu görev ticket 1 ve 3'ü ÇÖZMEZ.** Boş cevap kusuru (~%5) API'de 503 olarak **görünür**
hâle gelir ama **giderilmez**; donma sorunu API'de yoktur çünkü istek serileştirilir ve istemci
bekler. İkisi de aşağıdaki [AÇIK KUSURLAR](#açık-kusurlar--kayıt-ve-devir) bölümünde açık kalır.

---

### Görev 20 : Konteyner dağıtımı — paketleme bir REJİM KİLİDİ *(insan kararı 2026-09-10 · [ADR-0078](../../adr/0078-konteyner-dagitimi-rejim-kilidi.md))*

**Dosyalar:** Create: `Dockerfile` · `compose.yaml` · `.dockerignore` · `hakhukuk/indir.py` ·
`tests/test_konteyner.py` · Modify: `pyproject.toml` · `README.md` · `README.tr.md` · `MODEL_CARD.md`

**KAPSAM İNSAN KARARIYLA GENİŞLETİLDİ, çelişki iki yerde damgalandı.**
[`00-IS-SIRASI.md`](../00-IS-SIRASI.md) *"web arayüzü hâlâ `v2`"* diyor; **konteyner dağıtımı
web arayüzü değildir** ve `v1` tarafına alınmıştır. Gerekçe teknik değil, insan tercihidir.
**S9 yine AÇILMADI:** konteyner **yerel ve tek kullanıcı** — `llama` yalnız iç ağda,
`app` yalnız `127.0.0.1`'e yayımlanır. Barındırma ve mahremiyet vaadi `v2`'de açık durur.

**Gerekçe kolaylık DEĞİL, ölçülmüş bir kusurdur.** Ticket 2: aynı soru, aynı kod,
`--seed 3407`, sıcaklık 0 — KV önbelleği `q8_0` ↔ fp16 değişince **cevap değişti**
(`sha256` `79b6915a…` ↔ `e97a2b85…`, uzunluk 201 ↔ 622). Bağlayıcı yapılandırma bugün yalnız
**düz metin** olarak üç belgede yazılı ve hiçbir şey onu zorlamıyor. `compose.yaml` onu
zorlayan ilk artefakttır.

**Grill'de kod okumasıyla çıkan üç bulgu (iddia değil, dosya satırı):**

| # | bulgu | kanıt |
| :--- | :--- | :--- |
| F1 | `hakhukuk` paketi **tek başına kurulamıyor** — `servis.py` çalışma anında `sys.path`'e `scripts/` ekleyip `retriever.py`'yi oradan alıyor, indeks yolu repo köküne göreli | `hakhukuk/servis.py:27,46-48` ↔ `pyproject.toml` `packages = ["hakhukuk"]` ve ilk satırı *"`scripts/` bilerek DIŞARIDA"* |
| F4 | *"en güncel modeli çek"* bu hattın hata sınıfı — yayımlanan sayı **belirli bir dosyanındır** | `sha256 755e15e9…` · **2.783.446.720 bayt** ([`kollar.md`](../../record/kollar.md) 2026-09-09) |
| F5 | `pyproject.toml` `version = "0.2.0"`, git etiketi **`v0.3`** — imaj etiketi buradan türerse yanlış etiketlenir | `pyproject.toml:6` ↔ `git tag` |

**Ortam ölçüldü 2026-09-10:** Docker **28.4.0** · compose **v2.39.4-desktop.1** ·
RTX 5070 Ti Laptop **12227 MiB**, sürücü **591.97**. **`nvidia-ctk` WSL yolunda YOK** ⇒
konteynerin GPU'yu görüp görmediği **ölçülmedi**; Adım 0 tam olarak bunu ölçer.

**Topoloji — 3 kutu, 2 daemon, 2 imaj:**

```
hakhukuk-indir   TEK SEFERLİK   app imajının aynısı, farklı komut
                 HF'ten pinlenmiş revizyon → sha256 KAPISI → paylaşılan volume
                 tutmazsa çıkış ≠ 0 ⇒ iki servis de HİÇ başlamaz
llama            daemon · GPU   llama.cpp sunucu imajı · volume'den GGUF
                 bağlayıcı bayraklar compose'da YAZILI
app              daemon · CPU   hakhukuk + bge-m3 · volume'den indeks
                 HAKHUKUK_SUNUCU=http://llama:8080/v1 · ports "127.0.0.1:8000:8000"
```

`indir` ve `app` **aynı imajı** paylaşır (`huggingface-hub` zaten bağımlılık) — üçüncü
Dockerfile yok. Üçüncü kutunun silme testi: silinirse `sha256` kapısı iki entrypoint'e
dağılır ve **aynı mantık iki yerde** durur — S18'in ölçülmüş dersi.

**Kilitlenen beş karar** *(tam gerekçe ve elenen seçenekler: [ADR-0078](../../adr/0078-konteyner-dagitimi-rejim-kilidi.md))*:

| # | karar | gerekçe |
| :--- | :--- | :--- |
| 1 | Bağlayıcı bayraklar `compose.yaml`'a **birebir** | Ticket 2 ölçtü: bunlar tercih değil, **cevabı belirleyen** ayarlar |
| 2 | **Tek sapma:** `--host 127.0.0.1` → `--host 0.0.0.0` | Konteyner içinde `127.0.0.1` komşudan erişilemez. Erişim yüzeyi `ports: "127.0.0.1:8080:8080"` ile **aynı** kalır; üretimi etkilemez |
| 3 | HF revizyonu **pinlenir** + `sha256` + bayt sayısı kapısı, tutmazsa **erken çıkış** | ADR-0026'nın *"tanımsız base ERKEN patlar"* kuralının aynı sınıfı |
| 4 | İndeks **iki yollu**: volume öncelikli, HF yedek | G8'in bekleme gerekçesi bozulmaz — boyut kararı HF'te yaşar, **imaj değişmez** |
| 5 | İmaj **repo ağacını kopyalar**, F1 onarılmaz | Retriever'ı pakete taşımak yapısal değişiklik; 26 dosyanın yol köprüsü ve tüm ölçüm hattı aynı dosyayı kullanıyor ⇒ kendi turunu ve regresyonunu hak eder. Borç **ticket 11** olarak yazılır |

- [x] **Adım 0: GPU KAPISI** BİTTİ **2026-09-10** — **GEÇTİ**, ölçüldü.

`docker run --rm --gpus all nvidia/cuda:12.9.1-base-ubuntu24.04 nvidia-smi` konteynerin içinden
**`NVIDIA GeForce RTX 5070 Ti Laptop GPU, 12227 MiB, 591.97`** döndü — host'ta okunan üç değerle
**birebir aynı**, çıkış kodu 0. `nvidia-ctk`'nin WSL yolunda bulunamaması bir engel değilmiş:
GPU'yu Docker Desktop'ın WSL2 arkayüzü geçiriyor. **Topoloji değişmiyor**, CPU'ya düşülmedi
(düşmek `-ngl 99`'u düşürürdü ve bu **yeni rejim** olurdu).

- [x] **Adım 1: Failing test** — `tests/test_konteyner.py`. **Docker GEREKMEZ.**
Sınanacaklar: `compose.yaml`'daki `llama` komutu kanonik bayrak kümesini **birebir** taşıyor ·
`--host 0.0.0.0` sapması var ve `ports` yalnız `127.0.0.1`'e yayımlıyor · `indir.py` yanlış
`sha256` karşısında **erken çıkıyor** (indirme monkeypatch'lenir, ağ YOK) · pinlenmiş revizyon
dizesi `latest` **değil**.

- [x] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör** — 2026-09-11: **12 hata** (compose ve `indir.py` yoktu)

- [x] **Adım 3: `hakhukuk/indir.py`** — pinlenmiş revizyon · `sha256` + bayt kapısı · erken çıkış
`verify:` bozuk baytla çağrıldığında çıkış kodu ≠ 0 ve **hiçbir dosya volume'de bırakılmıyor**
(yarım-yazılmış artefakt, bu hattın *"hata vermeden yanlış"* sınıfının kendisidir).

- [x] **Adım 4: `Dockerfile` · `compose.yaml` · `.dockerignore`**
`verify:` `.dockerignore` `data/index/**/*.npy` ve `models/**`'i **dışarıda** tutuyor
(2,6 GB + 79 MB build bağlamına girmez); `compose.yaml` üç kutuyu ve
`depends_on: service_completed_successfully` bağını taşıyor.

- [x] **Adım 5: Testi koş, GEÇTİĞİNİ gör + commit** — **207 yeşil, 2 xfail** · commit `c234313`

**Adım 1-5'te ÖLÇÜLEN, plan metnini DÜZELTEN iki sayı** (2026-09-11, `du -sb` — tahmin değil):
`models/**` **79.639.851.820 B = 74,2 GiB** *(Adım 4 metni "2,6 GB" diyordu — o tek GGUF'un boyutu,
klasörün değil)* · `data/index/**/*.npy` iki dosya, toplam **165.871.872 B = 158,2 MiB**
*("79 MB" tek dosyaydı)*. Repo kökündeki `.env` de build bağlamının dışına alındı.

✅ **İKİNCİ `--host` SAPMASI — İNSAN KARARI 2026-09-11: ONAYLANDI** →
[ADR-0082](../../adr/0082-app-kutusu-host-sapmasi.md).
⚠️ **Başta *"ADR-0078'e altıncı karar olarak yazılır"* denmişti; öyle YAPILMADI ve sebebi
kayda geçti:** `docs/adr/**` **yeniden yazılmaz** ve bu deponun kendi emsali genişletmeyi
**yeni ADR** ile yapmaktır (ADR-0052 → 0036, ADR-0039 → Kapı 5). 0078'in metni **değişmedi**
— o gün **beş** karar kilitlenmişti ve kayıt öyle durur; 0078'e yalnız **tek satırlık işaretçi**
düşüldü. Çelişki **iki yerde** damgalı. *(Aşağıdaki gerekçe kararın dayanağıdır.)*
Karar 2 yalnız `llama` için sapma tanımlıyordu. `app` kutusu da aynı sorunu yaşıyor:
`api.py` `HOST="127.0.0.1"` diyor ve konteyner içinde bu arayüz host'tan erişilemez
(`ports` konteynerin eth0'ına proxy'ler, loopback'ine değil). Ajan `hakhukuk-api` yerine
`uvicorn … --host 0.0.0.0` çağırdı ve **`api.py`'ye DOKUNMADI**; erişim yüzeyi
`ports: "127.0.0.1:8000:8000"` ile aynı kaldı ⇒ S9 hâlâ açılmadı, ürün kodu değişmedi.
Elenen seçenek: `api.py`'ye ortam değişkeni eklemek — ürün kodunu değiştirirdi.
Gerekçe `llama` sapmasıyla **aynı sınıftan**, ama karar metni onu kapsamıyor.

- [ ] **Adım 6: `docker compose up` — indirme kapısı GERÇEKTEN koştu**
⚠️ **İNSANDAN İSTENENLER (Adım 6 bunlarsız koşamaz):** (1) **`HF_TOKEN`** — depo ÖZEL, tokensız
401; (2) **indeks kaynağı** — `HAKHUKUK_INDEKS_DEPO` bilerek BOŞ bırakıldı çünkü `G8`
bekletiliyor ve yayımlanmış indeks deposu yok ⇒ indeks ya volume'e elle konur ya depo adı
verilir, aksi hâlde `indir` kutusu **kasten** patlar ve iki daemon da hiç başlamaz.
⚠️ Boyut ölçülürken **özellikle bakılacak:** `sentence-transformers` torch'u kurulu bulmazsa
PyPI'nin CUDA tekerleğine düşer ve imaj ~5 GB şişer.
`verify:` `indir` kutusu `sha256`'yı doğruladı ve çıkış kodu 0; `llama` ve `app` ayağa kalktı.
**İmaj boyutu ÖLÇÜLÜR ve buraya yazılır** — tahmin yazılmaz.

- [ ] **Adım 7: Gözle doğrula** — API'ye bir soru, cevabı **gör**. **İNSAN GÖZÜ KAPISI**
(SIRA 2 ve Görev 19 Adım 6 ile aynı sınıf; kendi başına işaretlenmez).
`verify:` `sunum` alanı rozet + atıf + kaynak + ibare taşıyor; boş sorgu **422**.

- [ ] **Adım 8: Belgeler + sürüm** — ⚠️ **YAZILDI 2026-09-11, kutucuk BİLEREK AÇIK.** İnsan cevabı iki dışlayıcı seçeneği birden işaretledi (*"şimdi yaz"* + *"Adım 6'dan sonra"*); ikisini karşılayan okuma uygulandı: belgeler **yazıldı**, ama konteyner yolu *"**HENÜZ UÇTAN UCA DOĞRULANMADI**"* damgasıyla girdi ve kutucuk **Adım 6 koşana kadar açık** kalır. Commit `b7c3638`. Üç belgede de: `docker compose up` yolu · *"konteyner yayımlanan `0,8011`'i ÜRETMEZ"* şerhi · *"`docker compose up` hiç koşulmadı, imaj hiç build edilmedi, boyut ölçülmedi"* damgası (⛔ **tahmini boyut YAZILMADI**). `pyproject` `0.2.0` → **`0.3.0`** (F5). Belgeye yazılan her olgu `compose.yaml` **ayrıştırılarak** doğrulandı — **22/22 TUTTU**, hiçbiri hatırlanarak yazılmadı. — `README.md` · `README.tr.md` · `MODEL_CARD.md`'ye
`docker compose up` yolu; `pyproject.toml` `0.2.0` → `0.3.0` (F5).
`verify:` `tests/test_belgeler.py` yeşil; üç belgede de konteyner yolu **ve** *"konteyner
yayımlanan `0,8011`'i ÜRETMEZ"* şerhi var.

**Bu görev ticket 1 · 3 · 4 · 6'yı ÇÖZMEZ.** Boş cevap konteynerde de boş döner, Görev 19
sayesinde **503 olarak görünür**. Paketleme bir model kusurunu onarmaz.

---

### Görev 21 : Ürün yüzeyi kusur temizliği — kusur 3·4·5·7·8·12a·13 *(insan kararı 2026-09-10)*

**Dosyalar:** Modify: `hakhukuk/servis.py` · `hakhukuk/cli.py` · `hakhukuk/tui.py` ·
`hakhukuk/tipler.py` · `tests/test_servis.py` · `tests/test_cli.py` · `tests/test_tui.py` ·
`docs/record/yurutme-tuzaklari.md` *(yalnız EKLEME)* · Create: `tests/test_kusurlar.py`

**Niçin bu görev var.** `AÇIK KUSURLAR` bölümünün başlığı *"plan kapsamında ÇÖZÜLMEYENLER"*
diyordu ve okuyan *"çözülemez"* diye anlıyordu. 2026-09-10'da tek tek bakıldı: **on üç kusurun
on biri bu planda çözülebilir, dokuzu $0 ve küçük.** Bu görev o dokuzu topluyor; ağır ikisi
(kusur 1 ve 2) rejim ve GPU istediği için **Görev 22**'ye ayrıldı.

**Grill'de kusur KAYITLARININ KENDİSİ üç yerde düzeltildi — bunlar yeni bulgudur:**

| # | kayıt ne diyordu | grill ne buldu |
| :--- | :--- | :--- |
| 5a | *"skor dağılımına bakıp zayıf eşleşme durumunu göster"* | Eşik **ölçülmeden** konursa bu **uydurulmuş eşiktir** — bu hattın kendi yasakladığı şey (G19 karar 5, tuzak 2.17). Önce **ayrışma ölçülür**; `recall`'ın kaçırdığı **4/80** ile tutturduğu 76/80'in skor dağılımı **ayrışmıyorsa ROZET YOKTUR** ve bu bir **bulgudur**, başarısızlık değil |
| 5b | *"kapsam dışı soruları ayırt edip kullanıcıya bildir"* | Ayırt etmek bir **sınıflandırıcıdır** ve yanılır; yanıldığında vatandaşa *"bu konu kapsamda yok"* der ve **cevabı olan soruyu öldürür**. Ucuz ve dürüst alternatif: kapsamı **her zaman statik olarak göstermek** — *"yürürlükteki kanunlar; yönetmelik · tüzük · KHK · tebliğ YOK"*. Sınıflandırıcı yok, yanlış negatif yok |
| 13 | *"normalizasyon"* | Ham alanları **yeniden yazmak** kaynağın ne dediğini kaybettirir. Korpusun kendisi de tutarsız (`MADDE 349` ↔ `Madde 6`) ⇒ çare normalizasyon değil, **türetilmiş alan**: ham `madde_no` **korunur**, kıyas için `madde_sayisi` eklenir |

**Kilitlenen dört karar:**

| # | karar | gerekçe |
| :--- | :--- | :--- |
| 1 | Boş sorgu kapısı **`servis.answer()`'a** konur, arayüzlere değil | KAPI döngü dışındadır ve **üç yüzeyi birden** korur; G19'un 422'si yalnız HTTP yüzeyini koruyordu, `_getir` hâlâ savunmasızdı. **Uydurulmuş uzunluk eşiği YOK** — yalnız boş/boşluk |
| 2 | `##begin_quote##` süzgeci **yalnız `bicimle()`'de**; `Cevap.metin` **HAM kalır** | `metin` modelin ham çıktısıdır, değiştirmek kaydı bozar. G19 karar 2'nin sözleşmesi zaten *"`sunum` dizesi"*tir. ⛔ Ölçüm hattına **DOKUNULMAZ**: `scripts/puanlama/score_register.py:41` aynı işareti **register göstergesi olarak SAYIYOR** |
| 3 | Kapsam satırı **statik**, sınıflandırıcı YOK | Yanılan bir kapsam sınıflandırıcısı, cevabı olan soruyu öldürür |
| 4 | Zayıf-eşleşme rozeti **ölçüme bağlı**; ayrışma yoksa **rozet YOK** | Uydurulmuş eşik, bu hattın en pahalı hata sınıfını (*"hata vermeden yanlış"*) doğrudan besler |

- [x] **Adım 1: Failing test** — `tests/test_kusurlar.py` + mevcut dosyalara ekler.
Sınanacaklar: boş/boşluk sorgu `_getir`'e **hiç ulaşmıyor** · `"kira?"` **reddedilmiyor** ·
`bicimle()` çıktısında `##begin_quote##` **yok** ama alıntı metni **duruyor** · `Cevap.metin`
işaretleri **hâlâ taşıyor** (ham) · `Atif("6098","Madde 330").madde_sayisi ==
Kaynak(...,"MADDE 330").madde_sayisi` · `tui.py` `answer()`'ı olay döngüsünde **çağırmıyor** ·
açılış ekranında yönerge **ve** kapsam satırı var · `scripts/` altında süzgeç **yok**
(ölçüm hattı dokunulmazlık kapısı).

- [x] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör** — 2026-09-11: `tests/test_kusurlar.py` 15 test, **10 KIRMIZI görüldü** (183 geçti · 2 xfail). Beklenmedik geçen YOK.

- [x] **Adım 3: kusur 4 — boş sorgu KAPISI** (`servis.answer`)
`verify:` `_getir` boş sorguyla **çağrılmıyor**; CLI ve TUI okunur bir mesaj veriyor;
`"kira?"` **geçiyor**. API'nin kendi 422'si **değişmiyor** (iki yerde iki kapı değil, API
kendi sınırında erken reddeder — bu tekrar değil, sınır savunmasıdır).

- [x] **Adım 4: kusur 12a — `bicimle()`'de iskele işareti süzgeci**
`verify:` `sunum` temiz · `Cevap.metin` **HAM** · `grep -rn "begin_quote" scripts/` çıktısı
**değişmedi** (ölçüm hattı dokunulmadı).

- [x] **Adım 5: kusur 13 — `madde_sayisi` türetilmiş alanı**
`verify:` ham `madde_no` alanları **aynen duruyor**; `madde_sayisi` üç yazım biçimini de
(`MADDE 349` · `Madde 6` · `330`) aynı değere indiriyor.

- [x] **Adım 6: kusur 3 — TUI'yi çalışan iş parçacığına al**
`verify:` kaynak denetimi `answer()`'ın olay döngüsünde çağrılmadığını gösteriyor;
ilerleme satırı **gerçekten çiziliyor** (Adım 11'de gözle doğrulanır).

- [x] **Adım 7: kusur 8 + 5b — açılış yönergesi + STATİK kapsam satırı**
`verify:` uygulama açıldığında ekran **boş değil**; kapsam satırı korpus künyesinin
söylediğini diyor (**892 kanun · 40.496 madde · yönetmelik/tüzük/KHK/tebliğ YOK**) ve sayılar
`data/corpus/KUNYE.json`'dan **okunuyor**, koda gömülmüyor.

- [x] **Adım 8: kusur 5a — ÖLÇÜM: zayıf eşleşme ayrışıyor mu** — **KOŞTU 2026-09-11 · HÜKÜM: ROZET EKLENMEZ**
80 DEV kaleminde RRF skor dağılımı: `recall`'ın **kaçırdığı 4** kalem ile tutturduğu 76'yı
ayıran bir eşik **var mı**. `verify:` ayrışma **sayıyla** raporlandı. **Ayrışmıyorsa rozet
EKLENMEZ** ve bu sonuç kusur kaydına yazılır — *"ölçtük, ayrışmıyor"* bir **bulgudur**.
⛔ Ayrışma zayıfsa eşik **uydurulmaz**; kusur 5a **açık kalır**.

- [x] **Adım 9: kusur 7 — kuralı YAZ (kod değil)** — tuzak **1.11** eklendi (Bölüm 1; `1.10` ile aynı hata sınıfı, numara çakışmıyor; önceden var olan `2.17`/`5.8`/`5.9` çakışmalarına DOKUNULMADI) + Global kısıtlara bir cümle girdi
`docs/record/yurutme-tuzaklari.md`'ye **yeni satır eklenir** *(dosya yeniden yazılmaz)* ve
Global kısıtlara bir cümle girer: *yeni özne eklenirken duman koşusu **tabakalanmış**
(kısa/orta/uzun) seçilir ya da kapıya **%50 emniyet payı** konur.*
`verify:` tuzak listesinde satır var ve **numarası çakışmıyor**.
⚠️ **Grill bulgusu:** listede **iki ayrı `2.17` satırı** var (biri #58, biri #62) — numara
çakışması **zaten mevcut**; yeni satır bunu büyütmemeli.

- [x] **Adım 10: Testler yeşil + commit** *(davranışsal ve yapısal değişiklikler AYRI commit)* — **195 yeşil, 2 xfail** (2026-09-11). Üç commit: `6d81340` ölçüm · `d75b5c5` davranış · `4f0b795` kayıt. Yapısal ↔ davranışsal ayrımı: bu turda saf yapısal değişiklik YOK — tek ad değişikliği (`_iskele_isaretlerini_sil` → kamusal) aynı turda DOĞAN kodun adıdır, mevcut kodun yeniden adlandırılması değil; ayrı commit onu gerekçesiz bırakırdı.

- [x] **Adım 11: GÖZ KAPISI** — **İNSAN TEYİT ETTİ 2026-09-11.** Beş şartın beşi de ekranda görüldü:
ekran **donmuyor** (`⏳ kaynaklar taranıyor…` Enter'dan **hemen sonra** çizildi) · açılışta yönerge
**ve** kapsam satırı (`892 kanun · yürürlükteki 37.949 madde …`) · cevapta `##begin_quote##`
**YOK** · boş sorgu okunur mesaj alıyor · **iki ardışık Enter'da girdi KİLİTLENDİ**, ikinci
sorgu birincinin cevabını ezmedi.

🔴 **VE KAPI İŞİNİ YAPTI — 273 test yeşilken duran İKİ kusuru ekran yakaladı:**
**kusur 26** (sunumda **çift tırnak**: model işaretlerin içine kendi düz tırnağını da yazınca
`“ "…" ”` çıkıyordu) — ⚠️ bu kusuru **aynı gün BEN eklemiştim** (kusur 12a/19 süzgeci) ve
**testlerim tırnaksız alıntıyla yazıldığı için görmemişti**; TDD ile kapatıldı (commit
`6a58d72`, +6 test). **kusur 27** (Kaynaklar listesinde `MADDE 349` ↔ `Madde 8` yan yana —
korpusun ham tutarsızlığının vatandaş ekranına yansıması) — kayda geçti, **açık**.

**Ders, bu turun üçüncüsü:** sayısal kapı (273 yeşil test) bu iki kusuru **geçirdi**; ikisini de
**bakan göz** buldu. ADR-0051'in gözle-okuma şartı bu turda da karşılığını verdi.
`verify:` ekran **donmuyor** ve ilerleme satırı çiziliyor · açılışta yönerge + kapsam satırı
**görüldü** · cevapta `##begin_quote##` **YOK** · boş sorgu okunur bir mesaj alıyor.

**Bu görev kusur 6 · 11 · 12b'yi ÇÖZMEZ** — üçü de devredildi, bkz. `AÇIK KUSURLAR` başlığı.

---

### Görev 22 : Rejim kusuru + KV ölçümü — kusur 1·2 *(insan kararı 2026-09-10)*

**Dosyalar:** Modify: `hakhukuk/servis.py` *(onay gelirse)* · Create: `outputs/eval/g22-*/` ·
yeni ADR + `research_log` girişi

**Niçin ayrı görev.** İkisi de GPU ister, ikisi de **insan kapısı** taşır ve biri **rejim
değişikliğidir**. Görev 21'in $0'lık akışına karıştırılırsa, onaya bağlı bir iş yüzünden
ucuz iş de bekler.

**Grill'de kusur 2'nin kaydı DÜZELTİLDİ — bu yeni bir bulgudur:**
kayıt *"bedeli sıfır dolar, yaklaşık bir saat GPU"* diyordu. **Yanlış:** karşılaştırma
**kütle** üzerinden yapılacaksa kütleyi **hakem** üretir ⇒ **para harcanır** ve bakiye
**$2,20**. Bu yüzden iş ikiye bölündü: önce **$0'lık deterministik** karşılaştırma, kütle
ancak **ayrı bir bedel kapısından** sonra.

- [x] **Adım 1: kusur 2 — DETERMİNİSTİK karşılaştırma ($0)** — **KOŞTU 2026-09-11**
Varsayılan (fp16) KV ile ikinci sunucu açılır, 80 kalem üretilir; `q8_0` koşusuyla
**hakem çağırmadan** karşılaştırılır. `verify:` kaç cevap **bayt olarak değişti** (`sha256`) ·
çekinme sayısı · **uydurulmuş madde** sayısı · kesik/boş sayısı. **Kütle HESAPLANMAZ.**

- [x] **Adım 2: kusur 2 — bedel kapısı: kütle ölçülsün mü** — **SORULDU, İNSAN KARARI 2026-09-11: ÖLÇÜLSÜN.**
Gerekçe (insan): Adım 1 sayaçların oynamadığını gösterdi ama cevapların **%81'i bayt olarak
değişti** ve **6 kalem durum sınıfı değiştirdi**; sayaçlar sabitken kütlenin de sabit kaldığı
**çıkmaz**. Bedel **$0,0418** doğrusal, **%50 emniyet payıyla $0,0626** — `$1` kapısının
**altında**, bakiyenin %2,8'i. ⚠️ Tahminin dayanağı duman koşusu **değil**, çıpanın
**ÖLÇÜLMÜŞ** `$0,0417`'si (tuzak **1.11**'in istediği şey budur).

**KOŞTU 2026-09-11.** Duman koşusu **tabakalanmış** (5 kalem, cevap uzunluğuna göre 5 eşit
tabakanın medyanı) → ölçekleme kalem sayısı değil **hakem-istemi karakter yükü** üzerinden
(×18,04; naif ×16,0'dan muhafazakâr) → doğrusal `$0,0487`, %50 payla `$0,0731`.
**GERÇEK HARCAMA `$0,045067`** (OpenRouter `total_usage` 17,91293753 → 17,95800443, koşudan
önce/sonra) — sert kapının (`$0,15`) **%30'u**. Bakiye `$2,0420`.
⇒ **Tuzak 1.11'in reçetesi çalıştı:** tabakalanmış duman koşusu bu sefer **üstten** tahmin etti
(tahmin 0,0487 ↔ gerçek 0,0451), 2026-09-09'daki gibi %45 alttan değil.

| eksen | çıpa q8_0 | fp16 | fark | kaynak |
| :--- | ---: | ---: | ---: | :--- |
| **kütle** | **0,8011** | **0,7932** | **−0,79 p** | `harness_tablo.json` ↔ `harness_tablo_gnd.json` |
| `coverage` | 0,9375 | 0,9375 | aynı | ″ |
| `A1_cevaplanan` | 0,8545 | 0,8461 | −0,84 p | ″ (`rescore_answered.py` ile **çapraz doğrulandı**) |
| `cit_precision_micro` | 0,9231 | 0,8252 | **−9,79 p** | `gnd_*_summary.json` |
| **`wrong_ref_rate_micro`** | **0,0769** | **0,1553** | **2,0× KÖTÜLEŞME** | ″ |

**HÜKÜM — iki ayrı okuma, ikisi de yazılıyor:**
1. **Kütle farkı tek yönlü hükme YETMİYOR.** −0,79 p, devralınan ~0,3 puanlık gürültü tabanının
   2,8 katı; ama o taban **aynı cevaplara** hakemi yeniden koşmanın gürültüsüdür ve burada
   cevaplar da değişti (65/80 bayt farklı). **Bu koşu çiftine ait aynı-cevap tabanı ÖLÇÜLMEDİ**
   (ikinci hakem koşusu ≈`$0,044`). Kalem düzeyinde **18/80** kalem **iki yönlü** oynadı; toplam
   fark bu salınımların **artakalanıdır**. Ayrıca `groundedness.py` hakeme **seed göndermiyor**
   (belirlenim yalnız `temperature=0`) — iki kolda da aynı olduğu için birimi bozmuyor, ama
   küçük farkların yorumunu zayıflatıyor.
2. **Tabanın AÇIKÇA üstündeki tek eksen atıf isabetidir ve o eksen KÖTÜLEŞTİ.**
   `wrong_ref_rate` **iki katına** çıktı. Bu, Adım 1'in **hakemsiz** bulgusuyla aynı yönde
   (atıf sayısı 114 → 152, katı kapı reddi 0 → 3) ⇒ iki bağımsız alet aynı şeyi söylüyor.
   ⚠️ Bu **B1 eksenidir** ve zaten frontier'ın 9,3× gerisindeyiz (`0,0769 ↔ 0,0083`);
   fp16 o açığı **2 katına** çıkarıyor. ⇒ **Ürünün taşıyıcı rejimi `q8_0` kalmalıdır** —
   ~~bu bir öneridir, kapı değil~~ → **İNSAN KARARI 2026-09-11: `q8_0` KALSIN.** Öneri
   **karara döndü**; bağlayıcı yapılandırma (`--cache-type-k q8_0 --cache-type-v q8_0`)
   `compose.yaml`'da, `MODEL_CARD` §7.10'da ve HF kartında **zaten yazılı** — bu karar onları
   **teyit eder**, değiştirmez. Gerekçe ölçülmüştür: fp16'da `wrong_ref_rate` **2,0×**
   kötüleşiyor (`outputs/eval/g22-kv-fp16/KUTLE.md`) ve bu, frontier'ın zaten 9,3× gerisinde
   olduğumuz **B1 eksenidir**.

**Yan bulgu:** çekinme **5/80 ↔ 5/80** ama **küme farklı**: `{15,37,45,66,79}` ↔ `{15,45,51,66,79}`.
Aynı sayı, farklı kalemler — toplulaştırılmış sayacın neyi gizlediğinin örneği.
Adım 1 küçük bir sapma gösterirse kütle ölçmenin karşılığı yoktur. Büyük sapma gösterirse
hakem bedeli **tahmin edilir** ve `$1` kapısına vurulur. ⚠️ Tahmin **tabakalanmış** duman
koşusundan yapılır (kusur 7'nin dersi) ya da **%50 emniyet payı** eklenir.

- [x] **Adım 3: kusur 1 — REJİM KARARI** — **SORULDU, İNSAN KARARI 2026-09-11: EKLENSİN.**
Ürün yolu, ölçüm hattının **iki geçişli zorunlu düşünce kapatmasına** gelir. ⛔ Yayımlanan
**0,8011 ölçüm hattının sayısıdır ve DEĞİŞMEZ** — değişen **ürün yoludur**. Elenen seçenekler:
*"şimdi karar verme"* (kusur 1'in çıpası elde, beklemenin karşılığı yok) ve *"ekleme"*
(ADR-0040'ın %5 geçerlilik kapısını ürün yolu **%8,75** ile geçemiyor; kesikliği damgalamak
onu **gidermiyor**). ⇒ Adım 4 AÇILDI.
Ürün yoluna ölçüm hattının **iki geçişli zorunlu düşünce kapatması** eklensin mi.
Karar verilmeden **kod yazılmaz**. Kararın anlamı: ürün yolu ile ölçüm hattı **aynı rejime**
gelir; yayımlanan **0,8011 ölçüm hattının sayısıdır ve DEĞİŞMEZ** — değişen ürün yoludur.

- [x] **Adım 4: kusur 1 — uygulama + 80 kalem yeniden ölçüm** — **KOŞTU 2026-09-11, ÜÇ ŞARTIN ÜÇÜ DE GEÇTİ**

Kaynak: `outputs/eval/g22-rejim/KARSILASTIRMA.md` · ham `aracsiz_yol_80_zorunlu_kapatma.json`
· künye `KUNYE.json`. Çıpa `outputs/eval/g18-arac-katmani/aracsiz_yol_80.json`. $0, q8_0 rejimi,
1.061 s. Üç şart bağımsız olarak **yeniden hesaplanarak** doğrulandı.

| `verify:` şartı | öncesi | sonrası | hüküm |
| :--- | ---: | ---: | :--- |
| **tamamen boş 0/80** | 4/80 (id 7·64·65·66) | **0/80** | **GEÇTİ** |
| kesik, ADR-0040 **%5** kapısı (≤4/80) | 7/80 (**%8,75**) | **3/80 (%3,75)** | **GEÇTİ** |
| suskunluk farkı **raporlanıyor** | `[10,34,63]` | `[7,10,34,63,64]` | **GEÇTİ** — aşağıda |

**Suskunluk kümesi — ⛔ fark GİZLENMEDİ.** Giren **2** (id **7** · **64**), çıkan **0**.
İkisi de daha önce **tamamen boş** dönen kalemlerdi; şimdi açıkça *"verilen kaynaklarda bu
konuyu düzenleyen madde bulunmuyor"* diyorlar. Diğer iki bozuk kalem (id **65** · **66**) tam
**CEVAP**'a döndü (TMK 406 / TMK 425). ⇒ Dört kusurlu kalemin **ikisi cevaba, ikisi açık
çekinmeye** gitti.

**Değişiklik CERRAHİ:** `sha256` olarak değişen **yalnız 4/80** kalem — tam da bozuk olan
dördü; kalan **76 kalem birebir aynı**. Kaynak kümesi **80/80'de değişmedi** (retriever'a
dokunulmadı), doğrulanamayan atıf **10 → 10**.

⛔ **Kütle HESAPLANMADI** ve **0,8011'e DOKUNULMADI** — bu koşu ürün yolunun sayısıdır.

⚠️ **İki şerh, ikisi de kayda geçti:**
1. **B10'a +2 kalemlik yük.** Kesik sayacının düşmesi karşılığında **aşırı-red** ekseni iki
   kalem ağırlaştı. Bu tur bunu **ölçmedi**, yalnız kaydetti — B10 eşiği ayrı bir turun işi.
2. **2. geçiş `reasoning_content` alanına bağımlı.** `llama-server`'ın `--reasoning-format`
   varsayılanı değişirse mekanizma **sessizce tek geçişe düşer**. Koşuda doğrulandı ama
   **testle çivilenemiyor** (sunucu davranışı, kodun değil) ⇒ *"hata vermeden yanlış"*
   sınıfından bir bağımlılık, açık kusur **20**.
Çıpa **elimizde**: `outputs/eval/g18-arac-katmani/aracsiz_yol_80.json` (öncesi: kesik 7/80,
**tamamen boş 4/80**). `verify:` **tamamen boş 0/80** · kesik oranı ADR-0040'ın **%5**
geçerlilik kapısını **GEÇİYOR** · suskunluk kümesi öncesiyle karşılaştırılıp **fark
raporlanıyor** (gizlenmiyor).

- [x] **Adım 5: Bulguları yaz + commit** — **YAZILDI 2026-09-11.** [ADR-0080](../../adr/0080-urun-yolu-zorunlu-dusunce-kapatmasi.md) (rejim kararı, karar sahibi **insan**) + kayıt **#66**'ya *"EK — bu kayıt yazıldıktan SONRA eklendi"* bölümü (§8-§13). Ayrı bir #67 açılmadı: aynı gün, aynı tur. `verify:` her sayının yanında kaynak dosya adı **var**; kusur **1** ve **2**'nin kayıtları sonuçlarıyla **güncellendi**; `test_belgeler.py` **yeşil** (kırık işaretçi yok); andığı altı ADR'nin (0040 · 0043 · 0065 · 0070 · 0077 · 0078) **altısı da mevcut**.
`verify:` her sayının yanında **kaynak dosya adı** var; kusur 1 ve 2'nin kayıtları
**sonuçlarıyla** güncellendi.

---

## AÇIK KUSURLAR — kayıt ve devir

> **Bu bölüm KUTUCUK TAŞIMAZ ve paydaya GİRMEZ.** Kusurun *kaydı* ile işin *kapsamı* ayrı tutulur.
>
> **2026-09-10 (insan kararı):** bu kayıt `plans/post-hp-hat-b-tickets.md`'de ayrı bir dosyaydı;
> plana **taşındı ve dosya silindi**. Bu, [`00-IS-SIRASI.md`](../00-IS-SIRASI.md)'nin eski bakım
> kuralıyla **çelişir**; çelişki iki yerde damgalandı ve kuralın koruduğu şey *"kutucuk taşımaz"*
> şartıyla ayakta tutuldu. Gerekçe teknik değil, tercihtir.
>
> **Aynı gün ikinci karar:** başlık *"plan kapsamında ÇÖZÜLMEYENLER"* idi ve okuyan **"çözülemez"**
> diye anlıyordu. Tek tek bakıldı — **on üçün on biri bu planda çözülebilir, dokuzu $0 ve küçük.**

### Kusur → nerede kapanıyor

| # | kusur | nerede |
| :-- | :--- | :--- |
| 1 | ürün yolunda 4/80 cevap **tamamen boş** | **KAPANDI 2026-09-11** · insan rejim onayı + Görev 22 Adım 4: **0/80**, kesik %8,75 → %3,75, ADR-0040 kapısı GEÇTİ. Şerh: B10'a +2 kalem, ve kusur **20** doğdu |
| 2 | KV ayarının 80 kalemdeki etkisi ölçülmedi | **ÖLÇÜLDÜ 2026-09-11** ($0, hakemsiz): **%81 bayt değişimi**, sayaçlar ±1 kalem. **Kütle ölçülmedi** — Adım 2 insan bedel kapısı, tahmin **$0,0626** (%50 emniyet payı dahil) |
| 3 | TUI donuyor | **Görev 21** Adım 6 |
| 4 | boş sorgu reddedilmiyor | **Görev 21** Adım 3 |
| 5a | zayıf eşleşme sinyali | **ÖLÇÜLDÜ 2026-09-11 · ROZET EKLENMEDİ · kusur AÇIK KALIR** — altı göstergenin hiçbiri ayırmıyor; en iyi adayda 4 kaçık için **23 yanlış alarm**. Ölçüm: `outputs/eval/g21-zayif-eslesme/BULGU.md`. Devri planın kapanış bloğunda yazılacak |
| 5b | kapsam bildirimi | **KAPANDI 2026-09-11** · Görev 21 Adım 7 · statik satır, sınıflandırıcı YOK; sayılar `KUNYE.json`'dan okunuyor |
| **6** | `wrong_ref` 9,3× geride | **DEVREDİLDİ → `v2`** · borç **B1**, ADR-0075 |
| 7 | duman koşusu tahmini kapı kurmuyor | **Görev 21** Adım 9 · kural yazılır, kod değil |
| 8 | açılışta yönlendirme yok | **Görev 21** Adım 7 |
| 9 | SIRA 2 kapısı açık | **Görev 12** Adım 6-7 · yeni iş değil, aynı kapının aynası |
| 10 | dağıtım kararları | push **KAPANDI** · **HF görünürlüğü insan kararı**, iş değil |
| **11** | paket tek başına kurulamıyor | **DEVREDİLDİ → kendi turu** · [`00-IS-SIRASI`](../00-IS-SIRASI.md) *"sıranın dışında"*, ADR-0078 m.5 |
| 12a | `##begin_quote##` vatandaşa gidiyor | **Görev 21** Adım 4 · sunum katmanı |
| **12b** | işaretlerin **kaynağı** eğitim verisi | **DEVREDİLDİ → `v2`** · borç **B11** |
| 13 | `madde_no` biçimi tutmuyor | **Görev 21** Adım 5 · türetilmiş alan, ham veri korunur. ⚠️ Alan eklendi ama **hiçbir yerde KULLANILMIYOR** — bkz. kusur **14** |
| **14** | `madde_sayisi` **ölü alan**; asıl kıyas yeri zaten `madde_anahtari` kullanıyor | **YENİ 2026-09-11**, G21 incelemesinden. Silinmesi ya da bağlanması **ayrı karar**  **İNSAN KARARI 2026-09-11: SİL** — ölü kod, YAGNI; bağlanacağı yer yok  **→ **KAPANDI 2026-09-11** — alan + yardımcı + 4 test silindi; üretimde sıfır çağrı `grep` ile doğrulandı. Commit `7d1af54` (yapısal) |
| **15** | kapsam satırı **yalnız TUI'de**; CLI ve HTTP yüzeyi göstermiyor | **YENİ 2026-09-11.** Tek kaynak sağlandı (`cli.kapsam_satiri`), **gösterim** ürün kararıdır — insan  **İNSAN KARARI 2026-09-11: CLI ve HTTP'ye de EKLE** — tek kaynak `cli.kapsam_satiri` zaten var  **→ **KAPANDI 2026-09-11** — `bicimle()`'ye kondu ⇒ **CLI · TUI · HTTP üçü birden** aldı; sayılar `KUNYE.json`'dan okunuyor. Üç yüzeyde de **çalıştırılarak** görüldü. Commit `61162d0` |
| **16** | boş sorgu: rozet *"kaynaklarda karşılık bulunamadı"* ↔ gövde *"soru boş"* | **YENİ 2026-09-11.** Altıncı bir `Durum` **tip düzeyi** değişikliktir, **ADR ister**; ölçüm etkisi bugün 0 (DEV'de 0 boş kalem)  **İNSAN KARARI 2026-09-11: ALTINCI `Durum` EKLENSİN** — tip düzeyi değişiklik, **ADR-0081** yazılacak  **→ **KAPANDI 2026-09-11** — altıncı `Durum` = **`BOS_SORGU`**, beş yüzey güncellendi, [ADR-0081](../../adr/0081-altinci-durum-bos-sorgu.md) yazıldı. Commit `d79c01b` |
| **18** | ⭐ **atıf doğrulayıcı kanun adını YANLIŞ kanuna çözüyor** — *"Gelir Vergisi Kanunu"* → **1319 Emlak Vergisi** | **YENİ 2026-09-11**, G22 Adım 1; **ters yön aynı gün ÖLÇÜLDÜ** (insan kararı), `outputs/eval/g22-atif-cozum/BULGU.md`. Alet **manşet `0/114`'ü üretenin ta kendisi**. **Manşet TEMİZ — ama TESADÜFEN:** 114 atfın **0'ı** yanlış kanuna çözülüp `DOGRULANDI` almış; sebebi hiçbirinin **parantezli adlı** kanuna denk gelmemesi. Alet, parantezli adlı **16 kanunun 7'sinde** yanlış kanuna `DOGRULANDI` basıyor (kanıtlandı: *"Gelir Vergisi Kanunu Madde 1"* → `1319` → `DOGRULANDI`). ⚠️ Donmuş TEST'in **`0/52`**'si aynı aletle üretildi ve **ölçülmedi**. **Onarım AÇIK KARAR** — insan *"önce ölç"* dedi, ölçüldü  **İNSAN KARARI 2026-09-11: ALETİ ONAR + ÇIPALARI YENİDEN PUANLA** — donmuş TEST'in ham çıktısı diskte; yeniden **puanlamak** yeni sınav açmak DEĞİLDİR, aynı cevaplara düzeltilmiş aleti uygulamaktır (ADR-0050 kalıbı)  **→ **KAPANDI 2026-09-11** — alet onarıldı, çıpalar yeniden puanlandı: **`0/114` ve `0/52` OYNAMADI**, parantezli 16 kanunda yanlış-kanun+`DOGRULANDI` **7/16 → 0/16**. Commit `0031976`. ⚠️ Yan etkisi **kusur 22** |
| **19** | fp16 rejiminde model **istem yer tutucusunu harfiyen basıyor** (*"(KANUN ADI, Madde 13)"*) | **YENİ 2026-09-11**, G22 Adım 1. `0/80 ↔ 2/80`. Çıpa rejiminde **yok**; rejime bağlı bir bozulma sınıfı  **İNSAN KARARI 2026-09-11: KAPATILSIN** — sunum katmanında süzülür  **→ **KAPANDI 2026-09-11** — sunumda `(KANUN ADI, Madde 13)` → `(kanun adı belirtilmemiş, Madde 13)`. **Silinmedi, dürüstçe işaretlendi**: madde numarası vatandaşın doğrulayabileceği tek adrestir; silmek onu yok ederdi. Commit `5398c66` |
| **20** | ürün yolunun 2. geçişi `reasoning_content` alanına bağımlı — sunucunun `--reasoning-format` varsayılanı değişirse **sessizce tek geçişe düşer** | **YENİ 2026-09-11**, G22 Adım 4. Koşuda doğrulandı ama **testle çivilenemiyor** (sunucu davranışı). Boş cevap kusuru **sessizce geri gelebilir**  **İNSAN KARARI 2026-09-11: İKİSİ DE** — çalışma anı kapısı (sessiz düşüş yerine ERKEN patlama, ADR-0026 kalıbı) **ve** `compose.yaml`'da açık `--reasoning-format` bayrağı  **→ **KAPANDI 2026-09-11, iki yarısı da** — kod: `servis._reasoning_kapisi()`, sessiz düşüş yerine **erken ve gürültülü** `RuntimeError` (commit `3a8109e`); compose: `--reasoning-format deepseek` açıkça pinlendi ve **mutasyon denetimiyle** çivilendi (commit `1d0c616`). ⛔ Kapı **gözlem** kapısıdır, açılış yoklaması değil — yalnız **zaten kusurlu** hâlde ateşler, düşünce üretmeyen **meşru** sunucuyu öldürmez |
| **21** | `hakhukuk/araclar.py` **kendi ikinci ad indeksini** taşıyor — kusur 18 onarımı oraya GEÇMEDİ | **YENİ 2026-09-11.** Tuzak **2.18** kalıbı: *aynı ölçümün ikinci bir aleti*. Ölçüm hattı onarıldı, **ürün yüzeyi hâlâ eski çözümde** ⇒ vatandaşa giden atıf doğrulaması ile yayımlanan sayıyı üreten doğrulama **AYRI**  **→ İNSAN KARARI 2026-09-11: ONARIMI ÜRÜN YÜZEYİNE DE TAŞI** — tek kaynak. ⚠️ `hakhukuk/` → `scripts/` import'u **kusur 11**'in borcudur; çözüm onu **kısmen açabilir**  **→ KAPANDI 2026-09-11.** Ayrışma **gerçekti ve büyüktü**: 892 kanun adında **19**, parantezli 16'da **7**, çıpanın gerçek atıflarında **24/114** farklı. Ürün yüzeyi onarımdan **daha da katı** bir eski hâl taşıyordu — yanlış kanuna basmıyordu ama parantezli/kısaltılmış adları **hiç çözemiyordu** (modele *"böyle bir kanun yok"* diyordu). Sonrası **0/892 · 0/16 · 0/114**. Seçenek **(a)**: `araclar.py` `atif_dogrula`'dan import eder, kopya indeks **silindi**. **Eşdeğerlik kanıtlandı:** 94 dosya · 11.634 hüküm, iki kolun çıktısı `sha256` **birebir**. Commit `f6908e3` |
| **22** | rakip kollarının uydurma sayıları **onarılmamış aletle** üretildi | **YENİ 2026-09-11.** `MODEL_CARD` §karşılaştırma ve `CLAUDE.md` manşet bloğu *"1 · 4 · 4"* diyor; sonda **aleyhimize** oynadığını gösteriyor (3.1 FL **1→0**, 3.5 FL **4→3**). Sayılar **yazılmadı**: sondanın paydası yayımlanan boru hattınınkiyle tutmuyor (154↔152 · 134↔130) ⇒ **birim eşit değil**. Yeniden puanlama **$0, deterministik, hakemsiz**. Çelişki **iki yerde** damgalandı  **→ İNSAN KARARI 2026-09-11: YENİDEN PUANLA** — yayımlanan boru hattıyla, payda **birebir** olsun diye. Sonuç aleyhimize çıksa bile **yazılır**: bugün tabloda **iki farklı aletin** sayısı yan yana duruyor ve bu ADR-0057'nin *eşit sınav* kuralını ihlal ediyor  **→ KAPANDI 2026-09-11.** Yayımlanan boru hattıyla (`harness_tablo.py`) beş kol yeniden puanlandı; **kalibrasyon geçti** (bizim `harness_tablo.json` **alan alan** yeniden üretildi). **702 atfın 1'i** değişti: `3.1 FL` `1/152` → **`0/153`**, ve o damga **rakip aleyhine yanlış** basılmıştı. ⇒ **ALEYHİMİZE**: tek deterministik üstünlüğümüzde artık **eşitiz**; karşılığında **eşit sınav** sağlandı. Her kol **iki kez**, bayt bayt aynı |
| **23** | ilk yeniden-puanlama koşusu **eski sayıyı verdi ve tekrarlanamadı** | **YENİ 2026-09-11.** Modül gölgeleme arandı, bulunamadı. Yayımlanan sayılar 4 ardışık koşuda bayt-bayt aynı + bağımsız probla teyitli, ama **bu sınıftan bir sayı tek koşuya dayandırılmamalı** |
| **24** | iki README'nin *"Bugün kurup çalıştırabilir miyim? — HAYIR"* tablosu **BAYAT** | **YENİ 2026-09-11**, G20 Adım 8'de yakalandı. *"`hakhukuk/` dizini yok"* ve *"ağırlıklar hiçbir yerde yayımlandı değil"* diyor — **ikisi de artık YANLIŞ**. Kapsam dışı olduğu için dokunulmadı, yanına işaretçi konuldu. Vatandaşa **yanlış** bilgi veren bir tablo; kendi turunu hak ediyor |
| **25** | `MODEL_CARD` *uydurulmuş madde* satırında **İKİ FARKLI KESİR BİRİMİ** | **YENİ 2026-09-11.** Gemini sütunlarının paydası **`DOGRULANDI`**, Sonnet-5 hücresininki **toplam atıf** (163). Sayı oynamadığı için hüküm etkilenmedi, ama aynı satırda iki birim var. ⚠️ Birimin hiçbir yerde yazılı olmaması **bir ön sondayı zaten yanılttı** (*"3.5 FL 4 → 3"* diye okunan şey birim kaymasıydı; o kolda hiçbir atıf değişmedi) |
| **26** | sunumda **çift tırnak**: model işaretlerin içine kendi düz tırnağını da yazınca `“ "…" ”` çıkıyor | **YENİ 2026-09-11, İNSAN GÖZÜ KAPISINDA yakalandı.** Kusuru **bugün ben ekledim** (kusur 12a/19 süzgeci); testlerim **tırnaksız** alıntıyla yazılmıştı ve bu hâli görmemişti. ⇒ **Kapının kendisi işe yaradı:** 267 test yeşilken duran bir kusuru ekran yakaladı |
| **27** | Kaynaklar listesinde **madde biçimi tutmuyor** — `MADDE 349` · `Madde 8` · `MADDE 16` yan yana | **YENİ 2026-09-11**, aynı göz kapısında görüldü. Korpusun **ham** tutarsızlığı (kusur 13); veri bozulmasın diye ham alan **korunuyor**, ama **vatandaş ekranında** tekdüze gösterim ayrı bir iştir. ⚠️ Kusur 13 için eklenen `madde_sayisi` **kıyas** içindi ve kullanılmadığı için silindi (kusur 14) — **gösterim** sorunu onunla çözülmezdi, ayrı kalır |
| **28** | ⭐ **`hakhukuk-api` / `hakhukuk-tui` / `hakhukuk` komutları ÇALIŞMIYOR** — paket kurulu değil | **YENİ 2026-09-11, göz kapısı hazırlanırken yakalandı.** `pyproject.toml:30-33` üç giriş noktası tanımlıyor ama `pip show hakhukuk` → **not found** ⇒ `hakhukuk-api` çağrısı `No such file or directory` veriyor. Çalışan yol: `python -m hakhukuk.cli` · `python -m hakhukuk.tui` · `python -m uvicorn hakhukuk.api:uygulama`. ⚠️ **Bugün yazdığım belgeler ve göz kapısı defteri `hakhukuk-api` komutunu ÖNERİYOR** — yani **çalışmayan bir komut belgelenmiş** durumda. Kusur **11**'in (paket tek başına kurulamıyor) doğrudan görünen yüzü. `plan Görev 19 Adım 6`'nın `verify:` metni de aynı komutu yazıyor |
| **17** | `tui.py` `bicimle()`'yi çağırmıyor — **iki paralel sunum katmanı** | **YENİ 2026-09-11.** Bu turda iki sızıntının (iskele işareti · kapsam satırı) **kök nedeni**; ikisi de tek tek kapatıldı, **kök neden duruyor**  **İNSAN KARARI 2026-09-11: BİRLEŞTİR** — tek sunum katmanı; S18'in dersi bu turda **iki kez** ısırdı  **→ **KAPANDI 2026-09-11** — `tui.py` kendi sunum dizesini kurmayı **bıraktı**; tek katman `cli.bicimle(cevap, rozet=…)`, rozet **parametre** (bool bayrak yok), TUI ince kabuk kaldı. Commit `613e3ba` (yapısal) |

### Kapanış ve devir kuralı *(insan kararı 2026-09-10)*

Bu bölüm planın kapanmasını **engellemez**, ama plan kapandığında **boş olmak zorunda değildir**.
Şart şudur: **kapanış anında açık kalan her kusur, adıyla bir sonraki plana devredilir; hiçbir
yere devredilmemiş açık kusur varsa kapanış GEÇERSİZDİR.** Devir, planın kapanış bloğunda tek
tek yazılır.

Sebep: plan kapandığı gün **kayda dönüşür** (`faz0` planı gibi — *"artık kayıttır, açılmaz"*).
Devir kuralı olmazsa açık kusurlar **kapalı bir kaydın içinde donar**, ve bu tam olarak
silinen bakım kuralının önlemek için var olduğu şeydir.

---

### 1. Ürün yolunda cevapların yaklaşık yüzde beşi tamamen boş dönüyor

**Gözlem.** 80 soruluk geliştirme kümesinde `hakhukuk.servis.answer()` ile ölçüldü:

| | ürün yolu | ölçüm hattı |
| :--- | ---: | ---: |
| kesik veya boş cevap | 7/80 (%8,75) | 4/80 (%5,0) |
| tamamen boş metin | 4/80 (id 7, 64, 65, 66) | 0 |

**Kanıt.** `outputs/eval/g18-arac-katmani/aracsiz_yol_80.json`. Yedi kesik kalemin yedisi de
ölçüm hattında `finish=stop` ile tamamlanmıştır (485-892 belirteç), yani sorunun kaynağı
soruların zorluğu değildir.

**Neden.** Ölçüm hattı düşünce kanalını iki geçişte **zorla kapatır** (`--think-budget 1024`),
ürün yolu kapatmaz ve düşünce ile cevap tek bütçeyi (1536) paylaşır. Model bazı örneklerde
`</think>` etiketini hiç kapatmaz, bütçeyi düşüncede bitirir ve HTTP 200 ile boş içerik döner.
Bu bir sonlanmama sorunudur; araştırma kaydı #42'de aynı sınıf ölçülmüştür.

**Sonucu.** ADR-0040'ın geçerlilik kapısı yüzde beştir. Ölçüm hattı tam eşikte geçmekte, ürün
yolu yüzde 8,75 ile **geçememektedir**. Yayımlanan 0,8011 ölçüm hattının sayısıdır.

**Yapılacak.** Ürün yoluna iki geçişli zorunlu kapatma eklenecek mi, karar verilmeli. Bu bir
rejim değişikliğidir ve uygulanırsa 80 kalem yeniden ölçülmelidir.

---

### 2. Sunucu yapılandırması cevabı değiştiriyor, etkisi ölçülmedi

**Gözlem.** Aynı soru, aynı kod, seed 3407, sıcaklık 0; değişen tek etken KV önbelleğinin
kuantizasyonu:

| KV önbelleği | durum | `sha256` | uzunluk |
| :--- | :--- | :--- | ---: |
| `q8_0` (bütün ölçümlerin yapıldığı) | SUSKUNLUK | `79b6915a…` | 201 |
| varsayılan (fp16) | ÇEKİNCELİ | `e97a2b85…` | 622 |

**Kanıt.** Kontrollü deney: 8081 numaralı bağlantı noktasında varsayılan KV ile ikinci sunucu
açıldı, 8080 değiştirilmedi. Aynı yapılandırmada iki koşu birebir aynı çıktı verdi, yani bu
belirsizlik değil yapılandırmanın sonucudur.

**Sonucu.** Modeli indiren kişi kendi sunucu bayraklarını seçer. Bağlayıcı yapılandırma HF
kartının üçüncü bölümüne yazıldı, `MODEL_CARD` §7.10'a ve `servis.py` docstring'ine şerh düşüldü.

**Yapılacak.** Varsayılan KV ile 80 kalem yeniden ölçülmeli; bugün 0,8011'in o rejimde
korunacağı **iddia edilmiyor**. ~~Bedeli sıfır dolar, yaklaşık bir saat GPU.~~

**ÖLÇÜLDÜ 2026-09-11 — Görev 22 Adım 1.** Kaynak: `outputs/eval/g22-kv-fp16/KARSILASTIRMA.md`
· ham `h1_tgta_v1_g22_fp16_detail.jsonl` · künye `KUNYE.json`. Çıpa
`outputs/eval/f02-biz-onsozsuz/h1_tgta_v1_f02_nb_detail.jsonl`. Hakem ÇAĞRILMADI, **$0**,
42 dk GPU (şarjda). Rejim eşitliği doğrulandı: iki koşuda da `n_slots 4` · `kv_unified true`
· seed 3407 · bütçe 1024+512 · k=10 · önsözsüz; fark **yalnız** `--cache-type-k/-v`'nin
düşürülmesi (llama.cpp varsayılanı f16).

| eksen | q8_0 (çıpa) | fp16 |
| :--- | ---: | ---: |
| **bayt olarak değişen cevap** | — | **65/80 (%81,2)** |
| karakter medyanı *(n=80)* | 720 | 707 |
| kesik (`finish_reason=length`) | 4/80 | 3/80 |
| **tamamen boş** | 0/80 | 0/80 |
| çekinme (`exact_reject`, `mode=data`) | 5/80 | 5/80 |
| — bunun altın bağlamda olanı (aşırı-red) | 4 | 3 |
| **uydurulmuş madde** | **0/114** | **0/152** |
| katı atıf kapısı reddi | 0 | 3 |
| ürün durum sınıfı değişen kalem | — | 6/80 |
| **istem yer tutucusu sızıntısı** (*"(KANUN ADI, Madde 13)"*) | **0/80** | **2/80** |

⚠️ **İki medyan, iki payda — çelişki değil, damgalanması gereken bir ayrım:** yukarıdaki
**720 → 707** medyanı **n=80** üzerinde; `KARSILASTIRMA.md` §2.1'deki **715,0 → 706,5** ise
kontrol değişkeni düşen iki kalem (id 7 · 63) hariç **n=78** üzerinde. İkisi de doğru; hangi
paydada olduğu yazılmazsa *"aynı ölçüm iki sayı veriyor"* diye okunur (tuzak **2.6**'nın sınıfı).

**HÜKÜM: sapma toplulaştırılmış eksenlerde KÜÇÜK, kalem düzeyinde BÜYÜK.** Hiçbir sayaç
birden fazla kalem oynamadı; buna karşılık cevapların **%81'i bayt olarak değişti**.
⛔ **Kütle üzerine cümle KURULMADI — ölçülmedi** (hakem ister, Adım 2'nin bedel kapısı).
**Kusur kaydının tek-soruluk gözlemi (`SUSKUNLUK → CEKINCELI`) 80 kalemin hiçbirinde
tekrarlanmadı** — genel kural değilmiş; gözlenen geçişler `KESIK` ekseninde toplanıyor.

**Turun iki YAN BULGUSU (ikisi de aletin içinde, ikisi de onarılmadı):**
- **Kontrol değişkeni sızıntısı:** çıpa ile yeni koşu **2 kalemde** (id 7 · 63) farklı kaynak
  gördü. Sebep KV değil **kod**: yürürlük süzgeci (`63b691e`, 2026-09-07) çıpadan **sonra**
  geldi. Bağımsız doğrulandı (`context_shown` farkı tam olarak bu iki id). Sayaçları
  etkilemiyor (ikisi de her iki koşuda cevaplanmış, `finish=stop`), ama *"tek değişken KV"*
  cümlesi **tam doğru değildir** ve bu damgalanmadan bırakılamaz.
- Künyenin KV satırı **sabit dize** — tuzak **1.12**; bu koşunun `kosu.log`'u `q8_0` diyor,
  gerçek `f16`. Gerçek rejim `/proc/<pid>/cmdline`'dan okundu.

---

### 3. Arayüz soru sorulduğunda donuyor

**Gözlem.** `hakhukuk/tui.py` içinde `on_input_submitted` doğrudan `answer()` çağırıyor ve
Textual'ın olay döngüsünü otuz ile altmış saniye bloke ediyor. "Kaynaklar taranıyor" satırı bile
çizilemiyor, çünkü çizim aynı döngüde sıraya giriyor.

**Sonucu.** Donmuş ekran ile boş ekran kullanıcı açısından ayırt edilemiyor.

**Yapılacak.** `answer()` bir çalışan (worker) iş parçacığına alınmalı ve ilerleme göstergesi
gerçekten çizilmeli.

---

### 4. Boş sorgu reddedilmiyor, sabit bir gürültü kümesi dönüyor

**Gözlem.** Ölçüldü 2026-09-09:

```
_getir("", 10)   → RUMELİ DEMİRYOLLARI Madde 22 · ASAYİŞE MÜESSİR … Madde 1 ·
                    ÖZEL TÜKETİM VERGİSİ Madde 7 · OLAĞANÜSTÜ HAL … MADDE 12 …
_getir(" ", 10)  → aynı küme
```

Boş sorgu ile tek boşluk aynı sonucu veriyor; BM25 sıfır skor üretince sıralama korpus sırasına
düşüyor ve ilk on kayıt sabit bir gürültü olarak dönüyor. Model bu kaynaklarla çağrılıyor.

**Sonucu.** Anlamsız bir girdi, anlamlı görünen bir kaynak listesiyle karşılanıyor.

**Yapılacak.** Boş veya anlamsız kısalıktaki sorgu, retriever'a gitmeden reddedilmeli. Bu, bir
KAPI'dır ve döngü dışında uygulanmalıdır.

---

### 5. Erişim başarısız olduğunda kullanıcıya sinyal verilmiyor

**Gözlem.** Kullanıcı 2026-09-09'da iki soruda birbiriyle tamamen ilgisiz kaynak listeleri gördü
(örnek: Amme Alacaklarının Tahsili 51, Hususi Hastaneler 13, Damga Vergisi 30, Basın Mesleği 3).
Model doğru davranarak sustu, ancak arayüz *"getirilen kaynaklar sorunuzla ilgisiz"* bilgisini
vermiyor; kullanıcı bunu ürün hatası olarak okuyor.

**Ölçülmüş bağlam.** `recall@10` 0,9500'dür, yani her yirmi sorudan birinde doğru madde ilk ona
hiç girmez. Kapsam yalnızca yürürlükteki kanunlardır; yönetmelik, tüzük, KHK ve tebliğ korpusta
yoktur.

**Yapılacak.** İki ayrı iş: (a) getirilen kaynakların skor dağılımına bakıp *"zayıf eşleşme"*
durumunu arayüzde göstermek; (b) kapsam dışı soruları ayırt edip kullanıcıya kapsamı bildirmek.
İkisi de ürün yeteneğidir, ölçülen sayıya eklenmez.

**(b) KAPANDI 2026-09-11** — Görev 21 Adım 7. Kapsam satırı **statik** yazıldı, sınıflandırıcı
kurulmadı: yanılan bir kapsam sınıflandırıcısı vatandaşa *"bu konu kapsamda yok"* diyerek cevabı
olan soruyu öldürür. Sayılar `data/corpus/KUNYE.json`'dan okunuyor, koda gömülmedi.

**(a) ÖLÇÜLDÜ 2026-09-11 ve ROZET EKLENMEDİ — kusur 5a AÇIK KALIR.** Kaynak:
`outputs/eval/g21-zayif-eslesme/BULGU.md` · ham veri `skorlar_80.json` · künye `KUNYE.json`
(betik `scripts/erisim_korpus/zayif_eslesme_olc.py`, $0, hakemsiz, CPU). Aynı koşuda
`recall@10` **0,9500 (76/80)** ölçüldü ve çıpayla (`outputs/eval/f02-biz-onsozsuz/KUNYE.json`)
**birebir** tuttu ⇒ rejim farkı yok, ayrışmanın yokluğu ölçümün kusuru değil.

Kaçırılan dört kalem: `5237/Madde 89` · `5237/Madde 103` · `6284/MADDE 10` · `6098/MADDE 99`.
Altı aday göstergenin hiçbiri iki grubu ayırmıyor:

| gösterge | kaçırılan (n=4) medyan | tutturulan (n=76) medyan | kaçırılanın EN İYİsinin altında kalan tutturulan |
| :--- | ---: | ---: | ---: |
| **`ortalama_skor`** *(en iyi aday)* | 0,09276 | 0,10163 | **23/76** |
| `top1_skor` | 0,13691 | 0,16783 | 53/76 |
| `marj_1_2` | 0,02084 | 0,02051 | 56/76 |
| `std_skor` | 0,01934 | 0,02861 | 59/76 |
| `yayilim` | 0,06546 | 0,09129 | 60/76 |
| `entropi` | 2,28165 | 2,26997 | 57/76 |

En iyi adayda bile dört kaçığı yakalayan bir eşik, **doğru getirilmiş 23 kalemi** *"zayıf
eşleşme"* diye damgalardı — dört kalem için yirmi üç yanlış alarm. `marj_1_2` ve `entropi`'de
kaçırılanların medyanı tutturulanlarınkinden **daha iyi**: retriever yanlış getirirken de
kendinden emin görünüyor. ⚠️ **n=4 damgası:** dört kalemden türetilecek her eşiğin güven
aralığı berbattır; ayrışma *tam* görünse bile tek kalem hükmü çevirirdi — burada zaten tam
değil. Eşik **uydurulmadı**; *"ölçtük, ayrışmıyor"* bir **bulgudur**, başarısızlık değil.

---

### 6. Yanlış kaynağa atıf: frontier karşısında geride

**Gözlem.** `wrong_ref_rate_micro`: HakHukuk 0,0769, Claude Sonnet-5 0,0083. Yaklaşık 9,3 kat
geride.

**Ayrım.** Bu, uydurulmuş madde numarası değildir; o eksende önde olan taraf HakHukuk'tur
(0/114'e karşı 2/163). Model madde uydurmuyor, mevcut ve yanlış maddeye atıf yapıyor.

**Sonucu.** Planın *"B1'de rakiplerden geride değiliz"* hükmü yalnızca Gemini havuzunda
doğruydu. Frontier havuzunda geçmiyor.

**Yapılacak.** B1 borcu `v2` turuna taşındı. Bugün kapatılmıyor (ADR-0075).

**Canlı örnek, 2026-09-10 (Görev 19 göz kapısı) — TEK gözlem, ölçüm DEĞİL.** Soru:
*"Kiracı kira sözleşmesini feshetmek isterse ne kadar önce bildirmeli?"* Model
**TBK Madde 330**'u seçti ve *"üç gün önceden"* dedi. Madde gerçektir, alıntı birebirdir ve
atıf doğrulayıcısı **geçmiştir** — ama 330 **taşınır** kirasını düzenler. Vatandaşın
*"kira sözleşmesi"* dediği şey konut/çatılı işyeri kirasıdır ve onun bildirim süresi **aynı
kaynak listesindeki Madde 347**'dedir (sıra 2, modele verilmişti).

Bu, kusurun cinsini gösteriyor: **uydurma değil, UYGULANABİLİRLİK hatası**. Deterministik
atıf doğrulayıcısı bu sınıfı yakalayamaz — maddenin var olup olmadığına bakar, soruya
uyup uymadığına değil. `wrong_ref_rate` tam olarak bunu sayıyor.

---

### 7. Duman koşusundan doğrusal maliyet tahmini kapı kurmuyor

**Gözlem.** Beş kalemlik duman koşusundan çarpım yoluyla 0,82 dolar tahmin edildi; gerçekleşen
1,1932 dolar oldu, yani bir dolarlık kapı yüzde 45 aşıldı.

**Neden.** Cevap uzunluğu soruya göre değişen bir özne için beş kalemlik örneklem temsili
değildir. Gerçekleşen: cevap başına 706,6 belirteç, çıktı fiyatı milyon başına on dolar.

**Yapılacak.** Yeni bir özne eklenirken duman koşusu ya tabakalanmış seçilmeli (kısa, orta, uzun)
ya da kapıya yüzde elli emniyet payı konmalı.

---

### 8. Arayüz açılışında yönlendirme yok

**Gözlem.** Uygulama açıldığında çıktı alanı tamamen boştur; ne yapılacağını söyleyen bir satır
yoktur. Kullanıcı bunu "boş ekran" olarak okumuştur.

**Yapılacak.** Açılışta kısa bir yönerge gösterilmeli.

---

### 9. SIRA 2 kapısı açık

`hp-hat-a-hat-b` planının Görev 12 Adım 6-7 kapısı, insan gözüyle doğrulama gerektirir ve
kapanmamıştır. Üç soruda durum rozeti, atıflar, kaynaklar ve sorumluluk ibaresinin ekranda
görüldüğünün insan tarafından teyidi beklenmektedir.

Not: bu kapı çalışırken bir ürün kusuru yakalandı — `python -m hakhukuk.tui` komutu hiçbir şey
yapmıyordu, çünkü modülde `if __name__ == "__main__":` bloğu yoktu. Onarıldı ve testle çivilendi.
Kapının varlık sebebi tam olarak budur.

---

### 10. Dağıtım kararları

- ~~**Push.** On üç commit `hp-hat-a-hat-b` dalında bekliyor, `origin`'e gönderilmedi.~~
  **KAPANDI:** dal `master`'a alındı ve `origin`'e gönderildi; `v0.3` etiketi de push edildi.
  Ağaç temiz, yerel ile `origin` eşit (2026-09-09).
- **Hugging Face.** Depo 2026-09-09'da insan kararıyla **özele** alındı; açık kusurlar giderilene
  kadar böyle kalacak. Yükleme ve `sha256` doğrulaması tamamlanmıştır, geri alınan yalnız
  görünürlüktür.

---

### 11. `hakhukuk` paketi tek başına kurulamıyor — `pyproject`'in kendi cümlesi çalışma anında geçersiz

**Gözlem.** `pyproject.toml` `packages = ["hakhukuk"]` der ve ilk satırı *"`scripts/` (ölçüm
aleti) bilerek DIŞARIDA"* der. Oysa ürün paketi çalışma anında `scripts/`'e bağlıdır:

```
hakhukuk/servis.py:46-48   sys.path[:0] = [.../scripts, .../scripts/erisim_korpus]
hakhukuk/servis.py:48      from retriever import Retriever
hakhukuk/servis.py:27      _INDEKS = "data/index/mevzuat_bge_m3_s2"   # repo köküne GÖRELİ
```

Kök, `hakhukuk/servis.py`'nin kendi konumundan iki üst dizin olarak hesaplanır. Bu, **git
ağacından** koşarken çalışır; bir wheel'den kurulduğunda `scripts/` ve `data/` orada yoktur.

**Sonucu.** *"`pip install hakhukuk`"* diyen bir kurulum yolu **retriever'ı bulamaz**. Bugün
kimse bu yolu belgelemiyor, dolayısıyla kullanıcıya yansımış bir kusur **değildir**; ama
`pyproject.toml`'un kendi gerekçe cümlesi ile kodun davranışı **çelişmektedir**.

**Kararla dokunulmadı.** [ADR-0078](../../adr/0078-konteyner-dagitimi-rejim-kilidi.md) madde 5:
Görev 20'nin imajı repo ağacını kopyalar ve köprü bugünkü gibi çalışır. Onarım (retriever'ı
`hakhukuk/` içine taşımak) **yapısal bir değişikliktir**; aynı dosyayı 26 dosyanın yol köprüsü
ve tüm ölçüm hattı kullanıyor ⇒ kendi turunu ve kendi regresyon koşusunu hak eder.

**Yapılacak.** İki seçenek ölçülerek karşılaştırılmalı: (a) `retriever.py`'yi `hakhukuk/`
içine taşımak ve `scripts/` tarafını ondan import ettirmek; (b) `pyproject.toml`'daki cümleyi
gerçeğe uydurup bağımlılığı açıkça yazmak. Bugün hiçbiri seçilmedi.

---

### 12. Eğitim verisinin `##begin_quote##` işaretleri vatandaşa GİDİYOR

**Gözlem, 2026-09-10 (Görev 19 göz kapısı).** Ürün yolundan dönen cevabın gövdesinde:

```
2) ##begin_quote## "Taraflardan her biri, bir taşınıra ilişkin kira sözleşmesini üç gün
   önceden yapılacak fesih bildirim süresine uyarak her zaman feshedebilir." ##end_quote##
```

**Kaynağı ölçüldü, tahmin edilmedi.** İşaretler **istem katmanından gelmiyor**:
`hakhukuk/istem.py`'nin üç istem metninin hiçbirinde geçmiyorlar. Eğitim verisinin
üretim biçimindeler — `scripts/veri_hazirlik/gen_v2b_answers.py:36-37` öğretmen modele
*"`##begin_quote##` ile GOLD metinden kelimesi kelimesine alıntıla … `##end_quote##`"*
diyor, ve `build_sft_v2b.py:57` bu bloğu pencere kırpmasında **koruyor**. Model işareti
**öğrenmiş** ve üretiyor.

**Sonucu.** Vatandaş, kendisine ait olmayan bir iskele işaretini okuyor. CLI, TUI ve HTTP
API'nin üçü de aynı metni gösteriyor, çünkü üçü de `answer()`'ın metnini olduğu gibi taşıyor.

**Ne YAPILMADI ve niçin.** İşaretleri kaldırmak iki yoldan yapılabilir ve ikisi aynı şey
değildir: (a) **sunum katmanında süzmek** — bir KAPIdır, döngü dışındadır, modeli ve
yayımlanan sayıyı değiştirmez; (b) **eğitim verisini düzeltmek** — `v2` turunun işidir ve
yeniden eğitim ister. Bugün hiçbiri seçilmedi.

**Uyarı.** (a) seçilirse, süzme **yalnız ürün yüzeyinde** yapılmalı; ölçüm hattına
girmemeli. `scripts/puanlama/score_register.py:41` `##begin_quote##` işaretini bir
**register göstergesi** olarak sayıyor ⇒ ölçüm hattında süzmek o metriği sessizce değiştirir.

---

### 13. `Atif.madde_no` ile `Kaynak.madde_no` biçimi tutmuyor

**Gözlem, 2026-09-10.** Aynı yanıtta: `atiflar[0].madde_no == "Madde 330"`,
`kaynaklar[2].madde_no == "MADDE 330"`. Biri istem çıktısından ayrıştırılıyor, öteki
korpustan geliyor.

**Sonucu.** Bugün bir kusura yol açmıyor — atıf doğrulaması sayı üzerinden yapılıyor ve
**geçti**. Ama iki alan aynı şeyi adlandırıyor ve **farklı biçimde**; bir tüketici bu ikisini
eşitlemeye kalkarsa sessizce yanlış sonuç alır. HTTP API bu iki alanı **dışarıya** açtı,
dolayısıyla biçim artık bir sözleşme yüzeyidir.

**Yapılacak.** Normalizasyonun nerede yapılacağına karar verilmeli. Karar verilmeden
dokunulmadı: `terazi.py` ve korpus anahtarı (`kanun_no/madde_no`, tuzak 7.6) aynı biçime
bağlı olabilir.
