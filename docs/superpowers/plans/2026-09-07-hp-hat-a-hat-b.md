# `HP` → Hat A → Hat B — uygulama planı (`v0.2` → `v0.3`)

> Başlık 2026-09-09'da düzeltildi: hedef `v1.0` idi, **verilmedi**. Gerekçe [ADR-0077](../../adr/0077-v1-0-verilmedi-v0-3.md): engel modelin başarımı değil, ölçüm aygıtının güvenilirliği (tek hakem ailesi, κ 0,534 < 0,6).

## İCRA DURUMU — 2026-09-09 · **82/90 kutucuk** · `v0.3` etiketlendi

> **Bu blok planın tek doğru durum kaynağıdır.** Aşağıdaki görev başlıkları değişmedi;
> ne bittiği kutucuklardan, **neyin sırada olduğu buradan** okunur.
> `/goal` promptu: [`goal-hp-hat-a-hat-b.md`](goal-hp-hat-a-hat-b.md) *(2026-09-09'da yenilendi)*
> Plan kapsamı dışında kalan açık kusurlar: [`post-hp-hat-b-tickets.md`](post-hp-hat-b-tickets.md)

| | durum |
| :--- | :--- |
| **FAZ 1** · hakem paneli | **G1 · G3 bitti** — ikinci hakem ailesi koştu, κ **ilk kez ölçüldü** (`tam_sadık` **0,534** · `atıf_temiz` **0,409**, aracın eşiği 0,6 ⇒ **ALTINDA**), [ADR-0074](../../adr/0074-hakem-paneli-kuruldu-baglayici-hukum.md) + [#64](../../record/research_log/2026-09-07-hakem-paneli-iki-aile.md) yazıldı |
| **G2** | **ATLANDI** — insan kararı (bütçe). *(G4 bu satırdan çıkarıldı: 2026-09-09'da koştu, bkz. SIRA 3.)* Bakiye **$3,45** ↔ rakip kolunun ikinci hakemle puanlanması **$2,81**; panel **iki aileli** kaldı ve bu ADR-0074'te **eksiklik olarak** yazılı |
| **FAZ 2** · Hat A | **G5·G6·G7·G8b·G9·G10·G12 bitti**, G11 2/3 — `hakhukuk/` paketi doğdu (istem tek kaynak · tipler · terazi · servis · CLI · TUI), mülga süzgeci girdi, yeniden üretim zinciri yazıldı |
| **G8** · indeks dağıtımı | **BEKLETİLİYOR** — korpus **8,4×** büyüyecek (40.496 → ~340.303 madde) |
| **FAZ 3** · belge katmanı | **G13 bitti** — `PRODUCT.md` · `ROADMAP.md` · `TODO.md` · `docs/MIMARI.md` yazıldı, kırık işaretçiler onarıldı, `MODEL_CARD` §7.2/§8/§10 güncellendi |
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

**Bitmiş görevlerde talimat silindi, bulgu tutuldu** (aynı gün, 16 blok / 18 KB): *"şu dosyayı
yaz"* diyen kod kopyaları ve `git commit` reçeteleri çıkarıldı — karşılıkları repoda ve git
geçmişinde, üstelik kopyalar **bayatlamıştı** (`tui.py`'ye `__main__` bloğu, `servis.py`'ye
`answer_arac`, `tipler.py`'ye beşinci durum eklendi). ⛔ Koşu komutları **silinmedi**: onlar
talimat değil **rejim künyesidir**, ve bu hattın disiplini künyede görünmeyen bayrağın sessizce
düştüğü üzerine kuruludur.

### İŞ SIRASI

| sıra | iş | durum | kapı |
| :--- | :--- | :--- | :--- |
| ~~1~~ | **G8 Adım 1b** — `KUNYE` taşınabilirlik | BİTTİ | kopyalanmış ağaçtan yüklendi, `recall@10` **0,9500** |
| **2** | **G12 Adım 6-7** — TUI gözle doğrula | **AÇIK** | üç soruda rozet + atıf + kaynak + ibare **ekranda görüldü**, insan teyit etti |
| ~~3~~ | **G4** — Sonnet-5 rakip havuzunda | BİTTİ | eşit sınav kanıtlı; **Sonnet-5 ÖNDE** (0,8348 ↔ 0,8011) · $1,1932 |
| ~~4~~ | **G16** — `v1.0` kabul testi | BİTTİ | donmuş TEST tek kez açıldı; kütle **0,5804** · `v1.0` VERİLMEDİ → `v0.3` (ADR-0077) |
| ~~5~~ | **G18** — araç katmanı | BİTTİ | 5 kaldıraç · sınırlı döngü · regresyon **80/80 birebir** |
| ~~6~~ | **G17** — modeli YAYINLA | BİTTİ | HF'te, `sha256` doğrulandı; **şu an ÖZEL** (insan kararı) |
| **7** | **G19** — HTTP API (FastAPI) | **AÇIK** | dokuz karar kilitlendi 2026-09-09; kapıları görevin içinde |

⛔ **SIRA 2 bir insan gözü kapısıdır** ve kendi başına işaretlenmez. Bu kapı 2026-09-09'da bir
ürün kusuru yakaladı: `python -m hakhukuk.tui` hiç açılmıyordu (`__main__` bloğu yoktu) ve 163
test bunu görmemişti — kaynak denetimi mantığın sızmadığına bakar, programın çalıştığına değil.

**Plan kapsamı dışındaki açık kusurlar:** [`post-hp-hat-b-tickets.md`](post-hp-hat-b-tickets.md)
— on ticket. En ağırı: ürün yolunda cevapların **~%5'i boş** dönüyor ve bu, ADR-0040'ın kendi
geçerlilik kapısını geçmez.


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

### Görev 1: İkinci hakem ailesi (Anthropic) — aynı kayıtlar yeniden puanlanır

**Dosyalar:**
- Create: `outputs/eval/hp-hakem-paneli/` (+ `KUNYE.json`)
- Read: `scripts/puanlama/judge_agreement.py` · `scripts/puanlama/groundedness.py` · `scripts/puanlama/llm_client.py`
- Girdi (**değişmez, yeniden üretilmez**): `outputs/eval/f02-biz-onsozsuz/h1_tgta_v1_f02_nb_detail.jsonl`

**Arayüzler:**
- Tüketir: F0.2'nin `h1_*_detail.jsonl` dosyası (80 kalem, önsözsüz, bütçe 1536)
- Üretir: `outputs/eval/hp-hakem-paneli/gnd_h1_tgta_v1_anthropic.jsonl` +
  `..._summary.json` — `judge_agreement.py cross --b` bunu bekler

**Üretim YENİDEN KOŞULMAZ.** Panel **hakem** değişkenini ölçüyor; üretimi de değiştirmek
iki değişkeni birlikte oynatır (ADR-0017). Aynı 80 cevap, farklı hakem.

- [x] **Adım 1: Hakem kimliğini ve fiyatını koşmadan ÖNCE doğrula**

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
set -a && . ./.env && set +a && \
curl -s -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  https://openrouter.ai/api/v1/models | \
python -c "
import json,sys
d=json.load(sys.stdin)['data']
for m in d:
    if 'claude' in m['id'] and 'sonnet' in m['id']:
        p=m['pricing']
        print(f\"{m['id']:<45} girdi \${float(p['prompt'])*1e6:.2f}/M  çıktı \${float(p['completion'])*1e6:.2f}/M\")
"
```
`verify:` en az bir `anthropic/claude-*-sonnet*` kimliği ve **fiyatı** basıldı.
Kimliği **tahmin etme** — buradan al. Fiyat `gpt-4o-mini`'den **belirgin yüksekse**
maliyeti yeniden hesapla ve **$1'ı aşacaksa DUR ve sor**.

- [x] **Adım 2: Bedeli ölç — 5 kalemlik duman koşusu**

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
set -a && . ./.env && set +a && export OPENAI_API_KEY="$OPENROUTER_API_KEY" && \
mkdir -p outputs/eval/hp-hakem-paneli && \
LLM_GATEWAY=openrouter LLM_PROVIDER_ORDER=Anthropic \
python scripts/puanlama/groundedness.py \
  --details outputs/eval/f02-biz-onsozsuz/h1_tgta_v1_f02_nb_detail.jsonl \
  --label h1_tgta_v1_anthropic_duman --mode data \
  --judge-model <ADIM-1'DEN GELEN KİMLİK> --n 5 \
  --out-dir outputs/eval/hp-hakem-paneli
```
`verify:` `gnd_h1_tgta_v1_anthropic_duman_summary.json` yazıldı, `n=5`, `judge_cost_usd` **basıldı**.
Tam koşu tahmini = `judge_cost_usd × 16`. **> $1 ise DUR ve sor.**

> **ÖLÇÜLDÜ 2026-09-07 — bu adım $1 kapısını GERÇEKTEN tetikledi.**
> Kimlik `anthropic/claude-sonnet-5` ($2,00/M girdi · $10,00/M çıktı). Duman koşusu
> `judge_cost_usd` **$0,117** ⇒ tam koşu **$1,87**. Liste fiyatı `gpt-4o-mini`'nin
> ~14 katı ama **gerçek bedel 45 katı** ($0,0417 ↔ $1,87) — hakem çok daha uzun gerekçe
> üretiyor. *Fiyat oranından maliyet tahmin etme; duman koşusu şart.*
> **`anthropic/claude-sonnet-5:batch` (yarı fiyat) bu yoldan KULLANILAMAZ** — insan
> kararıyla denendi, `404: "This model is only available through the Batch API. Use the
> /api/beta/batches endpoint"`. `llm_client` senkron; batch ayrı taşıyıcı demek. Bedeli $0
> oldu (hiç çağrı geçmedi) ve olgu `llm_client.py`'ye yorum olarak damgalandı.
> `llm_client.PRICE` **fiyat kaydı olmayan modeli SystemExit ile reddediyor** — koşudan
> önce satır eklenmeli. Bu bir kapı, engel değil: yanlış fiyatla maliyet raporlanmasın.

- [x] **Adım 3: Tam koşu (80 kalem), AYRIK**

```bash
cd /home/ersoy/code/Hukuk-SLM && \
setsid nohup bash -c 'source ~/code/global_venv/bin/activate && \
  set -a && . ./.env && set +a && export OPENAI_API_KEY="$OPENROUTER_API_KEY" && \
  export PYTHONUNBUFFERED=1 && \
  LLM_GATEWAY=openrouter LLM_PROVIDER_ORDER=Anthropic \
  python scripts/puanlama/groundedness.py \
    --details outputs/eval/f02-biz-onsozsuz/h1_tgta_v1_f02_nb_detail.jsonl \
    --label h1_tgta_v1_anthropic --mode data \
    --judge-model <ADIM-1 KİMLİĞİ> \
    --out-dir outputs/eval/hp-hakem-paneli; \
  echo "EXIT=$?"' > /tmp/hp_anthropic.log 2>&1 < /dev/null &
```
`verify:` `/tmp/hp_anthropic.log` sonunda `EXIT=0` · `gnd_h1_tgta_v1_anthropic_summary.json`
`n=80` · `judge_cost_usd` künyeye yazılacak.

- [x] **Adım 4: Commit**

*(commit komutu 2026-09-09'da silindi — karşılığı repoda ve git geçmişinde; plandaki kopya artık güncel değildi.)*

---

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

### Görev 3: κ hesabı + öz-tercih ölçümü + hangi sayının bağlayıcı olduğu

**Dosyalar:**
- Create: `outputs/eval/hp-hakem-paneli/KAPPA.md` · `KUNYE.json`
- Create: `docs/adr/0074-hakem-paneli-kuruldu-baglayici-hukum.md`
- Read: `scripts/puanlama/judge_agreement.py` (üç modu var: `cross` · `export` · `author`)

**Arayüzler:**
- Tüketir: üç ailenin `gnd_*.jsonl` dosyaları
- Üretir: her eksen için **κ** ve **bağlayıcı okuma kuralı** — Görev 16'nın kapı koşusu bunu kullanır

- [x] **Adım 1: İkili κ'ları hesapla — üç çift**

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
D=outputs/eval/hp-hakem-paneli && \
for CIFT in "f02-biz-onsozsuz/gnd_h1_tgta_v1_f02_nb:$D/gnd_h1_tgta_v1_anthropic:openai_anthropic" \
            "f02-biz-onsozsuz/gnd_h1_tgta_v1_f02_nb:$D/gnd_h1_tgta_v1_google:openai_google" \
            "$D/gnd_h1_tgta_v1_anthropic:$D/gnd_h1_tgta_v1_google:anthropic_google"; do
  A="outputs/eval/${CIFT%%:*}.jsonl"; R="${CIFT#*:}"; B="${R%%:*}.jsonl"; AD="${R#*:}"
  echo "=== $AD ==="
  python scripts/puanlama/judge_agreement.py cross --a "$A" --b "$B" --field verdict --kind cat
done
```
**`--field` adını TAHMİN ETME.** Önce oku:
`head -1 outputs/eval/f02-biz-onsozsuz/gnd_h1_tgta_v1_f02_nb.jsonl | python -m json.tool`
— bu turda **üç kez** yanlış bayrak/alan adı çıktı, üçü de yalnız koşarken görüldü.
`verify:` üç çift için uyum % **ve** κ basıldı.

- [x] **Adım 2: Öz-tercih ölçümü — "hakem kendi ailesinin cevabını kayırıyor mu"**

Elimizde **dört özne** var (biz + üç Gemini) ve artık **iki-üç hakem**. Öz-tercih testi:
*Google hakem, Google öznelerine OpenAI hakemden **sistematik olarak yüksek** not veriyor mu?*

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
python - <<'PY'
import json, glob, os
def oku(p):
    return {r["id"]: r for r in (json.loads(l) for l in open(p, encoding="utf-8"))}
# Rakip kollarını Google hakemle notlamak AİLE DIŞLAMASI ihlalidir (ADR-0032) ⇒ ölçülmez.
# Öz-tercih burada YALNIZ şu soruyla sınanır: hakemler BİZİM kolumuzda birbirinden
# sistematik sapıyor mu, yoksa gürültü mü?
print("   Öz-tercih tam ölçümü aile dışlaması nedeniyle KURULAMIYOR (Google özne ↔ Google hakem yasak).")
print("   Raporlanan: hakemler arası SİSTEMATİK KAYMA (bias), bizim kolumuzda.")
PY
```
`verify:` her hakem çifti için **ortalama fark** (bias) ve **mutlak fark ortalaması** (gürültü)
ayrı ayrı basıldı. İkisi **ayrı** raporlanır: sistematik kayma ≠ rastgele gürültü.
Ölçülemeyen şey (**Google özne ↔ Google hakem**) `KAPPA.md`'ye **açık borç** olarak yazılır.

- [x] **Adım 3: `KAPPA.md` — üç okuma, ve BAĞLAYICI olanın seçimi**

Zorunlu içerik:
1. Üç κ değeri + `judge_agreement.py`'nin kendi eşiği (**κ ≥ 0,6 makul · ≥ 0,8 güçlü**)
2. **Aile dışlaması matrisi** — hangi özne × hakem hücresi **yasak** ve neden
3. Hakemler arası **bias ↔ gürültü** ayrımı, sayıyla
4. **Yeniden-koşum gürültü tabanı 0,3 A1 puanıdır ve YALNIZ A1 için ölçüldü.** Hakemler
   arası fark bu tabanın **altındaysa** *"hakemler ayrışıyor"* cümlesi **kurulmaz**
5. Kütle için **ayrı taban yok** (`kütle = coverage × A1`, coverage varyansı o tabanda yok)

`verify:` `KAPPA.md` üç κ, aile matrisi ve *"bağlayıcı okuma"* cümlesini içeriyor.

- [x] **Adım 4: ADR-0074 — bağlayıcı hüküm kuralı, KAPI KOŞUSUNDAN ÖNCE ön-kayıt**

Bu ADR **Görev 16'dan önce** yazılır. ADR-0050: raporlama biçimi koşudan **önce**
ön-kayıtlanır; sayı görüldükten sonra *"şu hakeme göre..."* demek kuralın engellediği şeydir.

Karara bağlanacaklar: (a) `v1.0` kapısının bağlayıcı hakemi **hangisi** (ya da **panel
ortalaması** / **en muhafazakârı**), (b) κ eşiğin altında çıkarsa ne olur, (c) rakip kolları
iki aileyle notlandığı için hükmün **hangi kısmı** üç aileye dayanıyor.
`verify:` ADR'de *"bu kural kapı koşusundan ÖNCE yazıldı"* şerhi ve **tarih** var.

- [x] **Adım 5: `research_log` #63 + README satırı + commit**

`verify:` `docs/record/research_log/README.md`'de **#63** satırı var; her sayının yanında
**kaynak dosya adı** duruyor.

---

### Görev 4: `v1.0` rakip havuzunun genişletilmesi — **SIRAYA ALINDI (SIRA 3)**

> **Karar iki kez değişti, ikisi de insan kararı ve ikisi de burada duruyor:**
> **(a) 2026-09-07 sabah — ATLANDI:** bakiye $3,45 iken önce donmuş TEST kabul koşusuna ayrıldı.
> **(b) 2026-09-07 akşam — GERİ ALINDI, sıraya girdi.** Sebebi ölçüldü: kalan planın tamamı
> OpenRouter'dan yalnız **~$0,30** istiyor (bağlayıcı hakem `gpt-4o-mini` ve 80 kalem puanlama
> **$0,0417** raporlanan / ~$0,067 gerçek) ⇒ bakiyenin **on katı marjı** var. *"Panel pahalı"*
> sanısı Sonnet'in **hakem** bedelinden geliyordu ($1,86); **özne** bedeli ayrı bir sayıdır.
>
> **Neden değerli:** havuzda bugün yalnız **Gemini ailesi** var. Frontier sınıfı bir öznenin
> aynı sınavdaki kütlesi **hiç ölçülmedi** — *"2,59 GiB'lık yerel model, frontier'ın ne kadar
> gerisinde, kaynak verildiğinde?"* sorusunun cevabı bugün **yok**.
>
> **Kapıyı ETKİLEMEZ** (ADR-0072 m.2): eşik oynamaz, çıpa `3.5 Flash` **kalır**; yeni özne
> **raporlanır**, eşiği **kurmaz**. ⇒ `v1.0` hükmü bu koşudan bağımsızdır.
> **GPT sınıfı yine dışarıda** (hakemi değiştirir + bugünkü dört sayıyı yeniden koşturur) ve
> bu `v1.0` yayınında **eksiklik olarak** yazılır — bütçe bahanesi olarak değil.
>
> **Bedel ÖLÇÜLMEDİ — Adım 1b bu yüzden eklendi.** Planın *"~$0,35"*'i **Gemini fiyatıyla**
> hesaplanmıştı; Sonnet **$2,00/M girdi · $10,00/M çıktı** (3.5 FL: $0,30/$2,50) ve gerçek
> fatura ayrıca **1,6×**. Kaba tahmin $1,0-1,6 ⇒ **duman koşusu şart**.

**Dosyalar:** Create: `outputs/eval/hp-rakip-havuzu/`
**Bağımlılık:** Görev 3 **bitmiş** olmalı.

**S16 KAPANDI 2026-09-07: TEK `anthropic/claude-*-sonnet*` sınıfı özne.**
Aile dışlamasına takılmıyor ⇒ bugünkü dört sayı **yeniden koşulmaz**; bedel ~**$0,35**.
GPT sınıfı **usulen** dışarıda (hakemi değiştirirdi) ve bu `v1.0` yayınında **eksiklik
olarak yazılır** — bütçe bahanesi olarak değil.
Girdiler [ADR-0072](../../adr/0072-v1-rakip-havuzu-genisler.md)'de: özne başı **~$0,35**
(F0.4'te ölçüldü: üç çıpa **$1,35**) · Anthropic öznesi sorunsuz · **GPT öznesi** hakem
değişikliği + bugünkü dört sayının **yeniden koşulması** demek.

- [x] **Adım 1: İnsan kararını al ve künyeye yaz** *(kod yok — karar adımı)*
**Karar 2026-09-07 (insan): TEK özne, `anthropic/claude-sonnet-5`.** Kimlik ve fiyat
OpenRouter `/api/v1/models`'ten ölçüldü: **$2,00/M girdi · $10,00/M çıktı**.
`verify:` `KUNYE.json` seçilen özneyi **tam model kimliğiyle** listeliyor.

- [x] **Adım 1b : Bedeli ÖLÇ — 5 kalemlik duman koşusu, tam koşudan ÖNCE** **BİTTİ 2026-09-07**

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
set -a && . ./.env && set +a && mkdir -p outputs/eval/hp-rakip-havuzu && \
OPENAI_API_KEY="$OPENROUTER_API_KEY" \
python scripts/olcum_uretim/gen_eval_grounded.py \
  --server-url https://openrouter.ai/api/v1 \
  --server-model anthropic/claude-sonnet-5 \
  --data data/eval/dev/core_hard.jsonl \
  --label h1_sonnet5_duman --n 5 --seed 3407 \
  --harness-indeks data/index/mevzuat_bge_m3_s2 --harness-k 10 \
  --max-chunk-chars 900 --thinking on --reasoning-budget 1024 \
  --max-new-tokens 512 --out-dir outputs/eval/hp-rakip-havuzu
```
`verify:` 5 kalem üretildi; **bakiye koşu ÖNCESİ ve SONRASI ölçülür** (`/api/v1/credits`) ve
gerçek fark yazılır. Tam koşu tahmini = fark × 16. **> $1 ise DUR ve sor.**
`--think-budget` **KULLANILMAZ** — rakip tarafı `--reasoning-budget` alır (ikisi karşılıklı
dışlayıcı; künye kanıtı `g2-fl-harness/KUNYE.json` → `"reasoning_budget": 1024`).

**ÖLÇÜLDÜ 2026-09-07 akşam — ama ölçüm biçimi kayda geçer:** duman koşusu başlatıldı,
**iptal edildi ve çıktısı yanlışlıkla silindi**; bedel yine de **bakiye farkından** okundu —
`total_usage 16,5520 → 16,6032` = **$0,0512 / 5 kalem** ⇒ ×16 = **~$0,82**. `$1` kapısının
**altında** ⇒ tam koşu doğrudan koşulur.
Bu, tahmin değil **gerçek fatura** farkıdır: OpenRouter'ın 1,6× marjı **zaten içinde**.
Dolayısıyla `judge_cost_usd`'ye uygulanan 1,6× çarpanı bu sayıya **UYGULANMAZ** — iki kez
sayılırdı.
**Artefakt yok:** duman koşusunun `_detail.jsonl`'i silindi, yalnız bakiye kaydı var.
Tam koşunun künyesi bunu böyle yazar.

- [x] **Adım 2: Her özne için üretim — F0.4'ün BİREBİR aynı komutu** **BİTTİ 2026-09-09**

Rakip tarafı **`--reasoning-budget 1024`** kullanır, `--think-budget` **DEĞİL** (ikisi
karşılıklı dışlayıcı; `--think-budget` istemci-taraflı zorunlu kapatmadır ve **yalnız bizim
kolda**). Künye kanıtı: `g2-fl-harness/KUNYE.json` → `"reasoning_budget": 1024`.
`verify:` her özne için `h1_*_detail.jsonl` **80 satır** · komutta `--sufficiency-preamble` **yok**.

**ALINDI 2026-09-09** — `outputs/eval/hp-rakip-havuzu/h1_sonnet_5_nb_detail.jsonl`, **80 satır**,
`anthropic/claude-sonnet-5`, seed 3407 · k=10 · 900 klip · `--reasoning-budget 1024` ·
önsözsüz (koşu çıktısı: *"kaynak-yeterliliği önsözü KAPALI"*) · süre ~17 dk.
Künyeye giren üretim sayıları: `completion_tokens` ort **706,6/cevap** (toplam 56.530) ·
`reasoning_tokens` ort **70,7/cevap** (80/80 bildirildi) · **4/80 kalem `finish_reason='length'`**
⇒ kesiklik damgası Adım 4'te taşınır.

**BEDEL KAPIYI AŞTI — $1,1932, tahmin $0,82 idi (+%45).** Bakiye ölçüldü:
`total_usage 16,60321828 → 17,79643028`; kalan **$2,2036**.
Sebep ölçülebilir: duman koşusunun 5 kalemi ($0,0512 ⇒ ×16 = $0,82) **temsili değilmiş** —
tam koşuda cevap başına 706,6 completion token çıktı ve Sonnet'in çıktı fiyatı $10,00/M.
**Ders, kural olarak yazılır:** `n=5`'lik duman koşusundan **×16 ile** doğrusal ekstrapolasyon,
uzunluğu soruya göre değişen bir özne için **kapı kurmaya yetmez**; duman koşusu ya
**tabakalanmış** (kısa/orta/uzun) seçilir ya da kapıya **%50 emniyet payı** konur.
Hüküm üzerindeki etkisi **YOK**: bu koşu ADR-0072 m.2 gereği yalnız **raporlanır**, `v1.0`
eşiğini kurmaz. Ama bütçe artık **$2,20** ve kalan planın ihtiyacı ~$0,10.

- **BORÇ** · **Adım 2b (bu koşudan doğdu): duman-koşusu ekstrapolasyonu bir KAPI değil, TAHMİNDİR**
Bir sonraki yeni özne/aile için ya tabakalanmış duman koşusu ya da %50 emniyet payı.
Bu satır **borç** olarak açık kalır; bugün koşulacak yeni özne yok.

- [x] **Adım 3: Eşit sınav kapısı — `recall@10` birebir aynı mı** **GEÇTİ 2026-09-09**

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
for f in outputs/eval/hp-rakip-havuzu/h1_*_detail.jsonl; do
  python - "$f" <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
hit = sum(1 for r in rows if r.get("gold_retrieved") or r.get("altin_getirildi"))
print(f"{sys.argv[1].split('/')[-1]:<52} n={len(rows)} recall@10={hit/len(rows):.4f}")
PY
done
```
`verify:` **hepsinde 0,9500** ve bizim kolla birebir. Farklıysa **DUR** — harness eşleşmemiş,
hüküm kurulmaz (ADR-0057).

**YUKARIDAKİ KOMUT BOZUK — sessizce 0,0000 yazdırıyor. Düzeltilmiş hâli aşağıda.**
`_detail.jsonl` şemasında `gold_retrieved` da `altin_getirildi` de **YOKTUR**; alan
`harness.altin_sirasi`'dır (`harness_tablo.py`:115 bunu kullanır). Komut hata vermeden
`recall@10=0,0000` bastı ⇒ *"eşit sınav kapısı ÇÖKTÜ"* diye okunabilirdi. Bu, bu hattın
**sessiz yanlışlık** sınıfının bir örneğidir ve komut burada onarıldı:

```python
s = [json.loads(l)["harness"]["altin_sirasi"] for l in open(yol, encoding="utf-8") if l.strip()]
print(f"recall@10 = {sum(1 for x in s if x is not None and x < 10)/len(s):.4f}")
```

**KAPI GEÇTİ 2026-09-09 — ölçüldü:**

| | recall@1 | recall@3 | recall@5 | **recall@10** |
| :--- | ---: | ---: | ---: | ---: |
| **Sonnet-5 (yeni)** | 0,5250 | 0,7625 | 0,8250 | **0,9500** |
| 3.5 Flash-Lite (F0.4 çıpası) | 0,5250 | 0,7625 | 0,8250 | **0,9500** |

Dört basamağın **dördü de** birebir aynı — beklenen, çünkü erişim modelden bağımsız (aynı
indeks · aynı k · aynı sorular). `altin_dusuruldu` = **0** ⇒ mülga süzgeci altını düşürmedi.
⇒ Sınav eşit, **hüküm kurulabilir** (ADR-0057).

- [x] **Adım 4: Puanlama + kesiklik damgası + gözle kalibrasyon** **BİTTİ 2026-09-09**

**Red-regex her yeni özne ailesinde kalibre EDİLMELİ.** Kalibresiz bırakmak onların
reddini **eksik** sayar ve puanı **bizim lehimize** kaydırır. F0.4'te ölçüldü: Gemini
kollarında **6 açık yanlış pozitif**, bizde **0**.
`verify:` özne başına **ALET / GÖZ-orta / GÖZ-katı** üç okuma da raporlandı.

**ALINDI 2026-09-09.** Hakem `openai/gpt-4o-mini` (aile dışlaması sağlandı: Anthropic özne
↔ OpenAI hakem) · `judge_cost_usd` **$0,0588**. Kesiklik damgası: **4/80 `length`** — BİZ ve
3.5 Flash kollarıyla **birebir aynı** (4/80), yani kesiklik kıyası bozmuyor.

**Kalibrasyon (8/8 kalem gözle okundu →** `outputs/eval/hp-rakip-havuzu/GOZLE_KALIBRASYON_sonnet_5.json`**):**

| kol | alet | temiz çekinme | çekinceli cevap | **açık yanlış pozitif** |
| :--- | ---: | ---: | ---: | ---: |
| **BİZ** | 4 | 4 | 0 | **0** |
| 3.5 Flash | 11 | 7 | 3 | **1** |
| **Sonnet-5** | **8** | **4** | **1** | **3** — id 17 · 35 · 41 |

Kusur **ADR-0061'in birebir aynı sınıfı**, aile değişti: dedektör **son esaslı ibareyi** tarıyor,
bu ailenin şablonu cevabı **şerh cümlesiyle** kapatıyor. id 35: *"nafaka davaları basit
yargılama usulüne tabidir"* açılışı, *"…açıkça başka bir usul **belirtilmediği** sürece…"*
kapanışı ⇒ **olumlu hükmün içindeki olumsuzlama** red sayılmış. `REJECT_RE`'ye dokunulmadı.

**HÜKÜM — üç okuma altında kütle:**

| okuma | BİZ `tgta_v1` | **Sonnet-5** | fark |
| :--- | ---: | ---: | ---: |
| ALET (ham) | **0,8011** | 0,7911 | +1,00 p bize |
| GÖZ-orta | 0,8011 | **0,8223** | **−2,12 p** |
| **GÖZ-katı** | 0,8011 | **0,8348** | **−3,37 p** |

**Sonnet-5 ÖNDE.** Öne geçtiğimiz tek okuma, önde olmadığımızı bildiğimiz okumadır:
alette Sonnet aleyhine **3 yanlış pozitif** var, bizde **0**. Aynı düzeltmeyi F0.4'te Gemini
ailesinin **lehine** yapmıştık; burada kendi **aleyhimize** uygulandı. Hakem gürültü tabanı
~0,3 A1 puanı ⇒ −2,12 ve −3,37 puan **anlamlı**.

**Önde olduğumuz tek eksen:** uydurma madde numarası **0/114 ↔ 2/163**.
`coverage` (ALET) 0,9375 ↔ 0,9000 da bizde, ama GÖZ-katı'da Sonnet 0,9500'e çıkıyor.

- **BORÇ** · **Adım 4b — B1 HAKKINDAKİ CÜMLEMİZ ÇÜRÜDÜ, borç açık kalır**
`wrong_ref_rate_micro`: **BİZ 0,0769 ↔ Sonnet-5 0,0083** — **9,3× geride**. Deterministik
doğrulayıcı ise *"var olmayan madde"* ekseninde bizi **0/114** ile önde gösteriyor (Sonnet
2/163). İkisi çelişmiyor, **farklı şey sayıyorlar**: madde **uydurmuyoruz**, var olan
**YANLIŞ** maddeye atıf yapıyoruz. ⇒ Planın *"B1'de rakiplerden geride değiliz"* hükmü
**yalnız Gemini havuzunda** doğruydu; frontier havuzunda **geçmiyor**. `v2`'nin gerekçesi
güçlendi. Bugün kapatılmaz (G14 atlandı, ADR-0075) — **borç**.

- [x] **Adım 5: `OZET.md` + commit** **BİTTİ 2026-09-09** →
`outputs/eval/hp-rakip-havuzu/OZET.md`. Eşik **oynamadı**, çıpa `3.5 Flash` **kaldı**.

`v1.0` kapısının eşiği **oynamaz**; çıpa `3.5 Flash` kalır (ADR-0072 madde 2).
Yeni özneler **raporlanır**, eşiği **kurmaz**.

---

# FAZ 2 · Hat A — paketleme ($0, GPU yok) → `v0.2`

**`HP`'ye PARALEL koşabilir.** Hakeme ve GPU'ya dokunmaz.

**Ölçülmüş boşluk (2026-09-07):**
- Servis katmanı **kod olarak yok**: `grep -rlE "fastapi|uvicorn|flask|gradio" scripts/` → **0**
- Modeli indiren kişi yayımlanan sayıyı **üretemiyor** (YB6)
- ~~`textual` **kurulu değil**~~ → **8.2.8 kurulu** *(2026-09-09)*
- İndeks **80 MB** ve `.gitignore:166` gereği git'te **yok** ⇒ S8 gerçek bir soru

---

### Görev 5: İstem artefaktı — spec'in dediğinden KÖTÜ **AÇIK KARAR S18**

**Dosyalar:**
- Create: `hakhukuk/__init__.py` · `hakhukuk/istem.py` · `tests/test_istem.py`
- Modify: `scripts/olcum_uretim/gen_eval_grounded.py:39-58` · `scripts/veri_hazirlik/raft_pack.py:20` ·
  `scripts/egitim/train_sft.py:31` · `scripts/veri_hazirlik/gen_v3_rejected.py:37` · `scripts/veri_hazirlik/build_orpo_v3.py:36`

**Arayüzler:**
- Üretir: `hakhukuk.istem.SISTEM_KOR` · `SISTEM_TEK_KAYNAK` · `SISTEM_COK_KAYNAK` ·
  `ISTEM_SURUMU: str` · `damga() -> str`
- Tüketir: yok (yaprak modül — bilerek bağımsız)

**Neden:** Spec *"istem yalnız `gen_eval_grounded.py` içinde"* diyordu. **Sayıldı:**
`"Sen HakHukuk'sun"` literali **5 dosyada**. Ve içerikler karşılaştırıldı:

| sabit | tanım | durum |
| :--- | ---: | :--- |
| `SYSTEM_PROMPT_RAG` | 3 | üçü de **bayt-bayt aynı** (`bbfdd6613f`) |
| `SYSTEM_PROMPT_RAG_MULTI` | 1 | `gen_eval_grounded` **import ediyor** |
| **`SYSTEM_PROMPT`** | 2 | **SÜRÜKLENMİŞ** |

Sürüklenmenin tam yeri — **son satır**:
- ölçüm (`gen_eval_grounded.py:39`): `…ilgili kanun ve madde numarasını belirt.`
- eğitim (`train_sft.py:31`): `Bu yanıt hukuki tavsiye değil, bilgilendirme amaçlıdır.`

Bu, **M5'in (kör mod) istemidir**. ⇒ İş mekanik refactor değil; **hangi metnin kanon olduğuna
karar vermek** gerekiyor (**S18**).

- [x] **Adım 1: Karar ALINDI 2026-09-07 → ölçülen sürüm kanon**

**`SISTEM_KOR` = `gen_eval_grounded.py`:39'un metni** — son satırı *"Cevabını kısa ve anlaşılır
tut; ilgili kanun ve madde numarasını belirt."* Yayımlanan **%80,1 dâhil bütün sayılar** bununla
üretildi; başka metin kanon olsaydı yayımlanan sayı **yeniden üretilemez** olurdu.
⇒ `train_sft.py`:31'deki sürüm **ÖLÜ KOD** (olguyla doğrulandı) → **bu görevde SİLİNİR**.
⇒ Feragat cümlesi isteme **girmez**; S10 gereği **çıktı yüzünde** ayrı satır (Görev 10).

- [x] **Adım 2: Failing test yaz**

*(kod 2026-09-09'da silindi — karşılığı repoda ve git geçmişinde; plandaki kopya artık güncel değildi.)*

- [x] **Adım 3: Testi koş, BAŞARISIZ olduğunu gör**

Run: `cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && python -m pytest tests/test_istem.py -v`
Beklenen: `FAIL` — `ModuleNotFoundError: No module named 'hakhukuk'`

- [x] **Adım 4: Asgari uygulama**

*(kod 2026-09-09'da silindi — karşılığı repoda ve git geçmişinde; plandaki kopya artık güncel değildi.)*

*(kod 2026-09-09'da silindi — karşılığı repoda ve git geçmişinde; plandaki kopya artık güncel değildi.)*

- [x] **Adım 5: Damgayı hesapla ve dosyaya yaz**

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
python -c "from hakhukuk import istem; print(istem.damga())"
```
Çıkan değeri `DAMGA_v1`'e yaz. `verify:` `python -m pytest tests/test_istem.py -v` → **3 passed**.

- [x] **Adım 6: `scripts/` beş dosyayı TEK KAYNAĞA bağla — SERT ENGEL**

Beş dosyadaki literaller **silinir** ve yerine import gelir:

```python
# scripts/olcum_uretim/gen_eval_grounded.py — satır 39-57 yerine
from hakhukuk.istem import (
    SISTEM_KOR as SYSTEM_PROMPT,
    SISTEM_TEK_KAYNAK as SYSTEM_PROMPT_RAG,
    SISTEM_COK_KAYNAK as SYSTEM_PROMPT_RAG_MULTI,
)
```
`scripts/` modülleri `sys.path`'e **kendi dizinini** ekliyor; `hakhukuk` **repo kökünde**
olduğu için kök de eklenmeli. Faz 0 planı **Görev 9 · T5 Adım 2** bu düzeltmeyi zaten
tanımlıyor — **önce o adım koşulur**, sonra bu adım.
`verify:` `grep -rc "Sen HakHukuk'sun" scripts/` → **0** · `python -m pytest` **yeşil**.

- [x] **Adım 7: KANIT KAPISI — istem dosyadan okunuyorken sayı BİREBİR aynı mı**

Bu adım atlanamaz. İstemi taşımak sayıyı **değiştirmemeli**; değiştiyse bir şey kaydı.

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
set -a && . ./.env && set +a && \
OUT_DIR=outputs/eval/a1-istem-kaniti \
MODES="h1" HARNESS_INDEKS=data/index/mevzuat_bge_m3_s2 HARNESS_K=10 \
THINK_BUDGET=1024 MAXTOK=512 CTX=8192 N_OVERRIDE=10 \
bash scripts/olcum_uretim/cp0_thinking_gen.sh models/gguf/tgta_v1-q4_k_m.gguf istem_kaniti
```
Sonra 10 kalemi F0.2'nin aynı 10 kalemiyle karşılaştır:
```bash
python - <<'PY'
import json
a = {r["soru"].strip(): r for r in (json.loads(l) for l in open(
    "outputs/eval/f02-biz-onsozsuz/h1_tgta_v1_f02_nb_detail.jsonl", encoding="utf-8"))}
b = [json.loads(l) for l in open(
    "outputs/eval/a1-istem-kaniti/h1_istem_kaniti_detail.jsonl", encoding="utf-8")]
ayni = sum(1 for r in b if a.get(r["soru"].strip(), {}).get("cevap") == r["cevap"])
print(f"birebir aynı: {ayni}/{len(b)}")
assert ayni == len(b), "   İSTEM TAŞINMASI ÇIKTIYI DEĞİŞTİRDİ — sebep bulunmadan devam edilmez"
PY
```
`verify:` `birebir aynı: 10/10`. Değilse **DUR** — metin bayt düzeyinde farklı demektir.

> **KOŞULDU 2026-09-07 — sonuç 8/10, ve planın "değilse metin farklıdır" ÇIKARIMI YANLIŞMIŞ.**
> İki sapmanın ikisi de sebebe bağlandı, ikisi de istem taşımasına ait **değil**:
> 1. **Yürürlük süzgeci** (`63b691e`, Görev 8b) getirilen kaynak listesini bir kalemde
>    değiştirdi: `İŞ KANUNU|Madde 111` **mülga** çıktı ve elendi ⇒ `context_shown` farklı
>    (7289 → 6538 kar.). Kasıtlı davranış değişikliği. **Sıralama dersi:** kanıt kapısı,
>    retriever'ı değiştiren bir görevden **ÖNCE** koşulmalıydı — çıpa kirlendi.
> 2. **Üretim tam deterministik değil.** **Gürültü tabanı ÖLÇÜLDÜ:** aynı komut ikinci kez
>    koşuldu (`outputs/eval/a1-determinizm-tabani/`), aynı kod · aynı istem · aynı retriever,
>    tek değişken sampling ⇒ **9/10** ve `context_shown` **10/10 birebir**. Farklı olan tek
>    kalem (`CMK 153`) iki noktalama formu arasında salınıyor ve determinizm koşusu F0.2'nin
>    **eski formunu birebir yeniden üretti**.
>
> ⇒ **8/10 = 1 gürültü + 1 yürürlük süzgeci. İstem taşımasına atfedilebilen sapma: 0/10.**
> Kapının sorduğu soru (*"istemi taşımak çıktıyı değiştirdi mi"*) **HAYIR** diye cevaplandı.
> Sınır: n=10, tek tekrar; kararsız kalemin salınım sıklığı ölçülmedi.
>
> **Ve kapının kendisi bir ürün kusuru buldu** (uçtan uca koşuda): `terazi._atiflari_cikar`
> atfı daima `f"Madde {n}"` kuruyordu, korpus kimliği ise kendi yazımını taşıyor —
> **23.766 `Madde` · 8.922 `MADDE` · 7.808 diğer** ⇒ korpusun beşte birine yapılan DOĞRU
> atıflar *"doğrulanamadı"* çıkıyordu (yanlış NEGATİF). `madde_anahtari` ile normalleştirildi;
> 80 kalemde **CEVAP 33 → 54 · ÇEKİNCELİ 38 → 17**, suskunluk çıpası **5** değişmedi.

- [x] **Adım 8: Commit** *(yapısal değişiklik — davranış değişmez, AYRI commit)*

*(commit komutu 2026-09-09'da silindi — karşılığı repoda ve git geçmişinde; plandaki kopya artık güncel değildi.)*

---

### Görev 6: Tipler — üç durumun kod seviyesinde ayrılması

**Dosyalar:** Create: `hakhukuk/tipler.py` · `tests/test_tipler.py`

**Arayüzler:**
- Üretir: `Durum` (enum) · `Kaynak` · `Atif` · `Cevap` — Görev 7·9·10·12 hepsini kullanır
- Tüketir: yok

**Neden enum, neden `bool` değil:** `suskunluk_terazisi`'nin bulgusu **üç durum** olduğuydu
(cevap · **çekinceli cevap** · suskunluk) ve bir dördüncüsü Faz 0'da ölçüldü (**kesik**).
`bool cevap_verdi` bu ayrımı **kaybeder** — vatandaş için en tehlikelisi tam da ortadaki:
*"doğrudan madde yok, bununla birlikte…"* cevap gibi görünür ama değildir.
*(CLAUDE.md §4: public API'de bool flag yok · §9: kapalı küme → sum type.)*

- [x] **Adım 1: Failing test yaz**

*(kod 2026-09-09'da silindi — karşılığı repoda ve git geçmişinde; plandaki kopya artık güncel değildi.)*

- [x] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör**

Run: `python -m pytest tests/test_tipler.py -v` → `FAIL` (`No module named 'hakhukuk.tipler'`)

- [x] **Adım 3: Asgari uygulama**

*(kod 2026-09-09'da silindi — karşılığı repoda ve git geçmişinde; plandaki kopya artık güncel değildi.)*

- [x] **Adım 4: Testi koş, GEÇTİĞİNİ gör**

Run: `python -m pytest tests/test_tipler.py -v` → **4 passed**

- [x] **Adım 5: Commit**

*(commit komutu 2026-09-09'da silindi — karşılığı repoda ve git geçmişinde; plandaki kopya artık güncel değildi.)*

---

### Görev 7: `suskunluk_terazisi` ürün yüzeyi — uydurulmuş atıf kullanıcıya GİTMEZ

**Dosyalar:**
- Create: `hakhukuk/terazi.py` · `tests/test_terazi.py`
- Read: `scripts/puanlama/score_abstention.py` (`exact_reject`, `REJECT_RE`) · `scripts/erisim_korpus/atif_dogrula.py`

**Arayüzler:**
- Tüketir: `hakhukuk.tipler` (Görev 6)
- Üretir: `siniflandir(metin, kaynaklar, finish_reason) -> tuple[Durum, tuple[Atif, ...]]`
  — Görev 9 (`servis.answer`) bunu çağırır

**Neden ürün yüzeyi:** Bugün ölçüm aleti olan üç şey üründe **güven mekanizması** olur.
Ölçüldü: bizim kolda uydurulmuş madde **0/114**, rakiplerde **1 · 4 · 4**. Bu bir **satış
noktasıdır** ve kullanıcıya gösterilmelidir.

**Faz 0'ın taze dersi buraya doğrudan giriyor:** `exact_reject`'in *"bulunmamaktadır"*
ailesi hukuk metninde **iki iş görür** — *"kaynakta yok, cevaplayamam"* (çekinme) ↔
*"kanunda böyle bir hüküm yok"* (**esasa ilişkin cevap**). 2026-09-07'de kör modda
**6/6 yanlış pozitif** verdi. ⇒ Ürün sınıflandırıcısı **kaynak var mı** bilgisini
kullanmak zorundadır; metne tek başına bakarsa **aynı hatayı yapar**.

- [x] **Adım 1: Failing test yaz — Faz 0'ın GERÇEK vakalarıyla**

*(kod 2026-09-09'da silindi — karşılığı repoda ve git geçmişinde; plandaki kopya artık güncel değildi.)*

- [x] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör**

Run: `python -m pytest tests/test_terazi.py -v` → `FAIL` (`No module named 'hakhukuk.terazi'`)

- [x] **Adım 3: Uygulama**

*(kod 2026-09-09'da silindi — karşılığı repoda ve git geçmişinde; plandaki kopya artık güncel değildi.)*

- [x] **Adım 4: Testi koş, GEÇTİĞİNİ gör**

Run: `python -m pytest tests/test_terazi.py -v` → **5 passed**
Geçmiyorsa **eşiği değil sınıflandırıcıyı** düzelt; testler Faz 0'ın **gerçek** vakaları.

> **UYGULANDI 2026-09-07 — planın yukarıdaki kodunun İKİ kusuru ölçüldü, ikisi de
> "hata vermeden yanlış sonuç" sınıfından:**
> 1. `from score_abstention import REJECT_RE` — plan `sys.path`'e yalnız `scripts` ekliyor,
>    ama dosya **`scripts/puanlama/`** alt klasöründe (T5 bölünmesi). Doğrusu:
>    `os.path.join(_KOK, "scripts", "puanlama")`.
> 2. `_ATIF` regex yalnız **anahtar-önce** yazımı tutuyordu (`madde 503`). Gerçek cevaplarda
>    **sayı-önce** yazım da var (`503. madde` · `33. maddesi`) ve planın kendi ilk testi tam
>    bu yüzden düşüyordu — atıf çıkmayınca dolu cevap SUSKUNLUK sayılıyordu. İkinci kol eklendi.
>
> **Adım 5 sonucu:** suskunluk **5/80**, id'ler `[15, 37, 45, 66, 79]` — `GOZLE_OKUMA_80.md`'nin
> gözle okuduğu kümeyle **BİREBİR**. Beşincisi (id 79) gözün *"DOĞRU davranış, altın bağlamda
> yok"* dediği kalem ⇒ **aşırı-red 4/80**, çıpayla tam uyum. CEVAP 33 · ÇEKİNCELİ 38 · KESİK 4.

- [x] **Adım 5: REGRESYON KAPISI — 80 gerçek kalemde alet ↔ göz**

```bash
source ~/code/global_venv/bin/activate && \
python - <<'PY'
import json
from hakhukuk.terazi import siniflandir
from hakhukuk.tipler import Durum, Kaynak
rows = [json.loads(l) for l in open(
    "outputs/eval/f02-biz-onsozsuz/h1_tgta_v1_f02_nb_detail.jsonl", encoding="utf-8")]
sayim = {d: 0 for d in Durum}
for r in rows:
    kaynak_var = bool((r.get("context_shown") or "").strip())
    #    Sahte kaynak GERÇEK bir Kaynak olmalı: _atiflari_cikar `.kimlik` okuyor.
    #    `object()` verirsek AttributeError — testte değil, kapıda patlar.
    sahte = (Kaynak(kanun_adi=r.get("kanun_adi", ""), kanun_no=str(r.get("kanun_no", "")),
                    madde_no=r.get("madde_no", ""), metin="", sira=1),) if kaynak_var else ()
    d, _ = siniflandir(r["cevap"] or "", kaynaklar=sahte,
                       finish_reason=r.get("finish_reason") or "stop")
    sayim[d] += 1
for d, n in sayim.items():
    print(f"{d.name:<11} {n}")
print("\n   GÖZ çıpası (F0.3, 80/80 okundu): aşırı-red 4/80")
PY
```
`verify:` `SUSKUNLUK` sayısı **4/80 göz çıpasına yakın**. Sapma **> 2 kalemse** her fark eden
kalem **id'siyle listelenir ve gözle okunur** — sayı düzeltilmeden devam edilmez.

- [x] **Adım 6: Commit**

*(commit komutu 2026-09-09'da silindi — karşılığı repoda ve git geçmişinde; plandaki kopya artık güncel değildi.)*

---

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

### Görev 8b : Yürürlük — mülga madde vatandaşa GİTMEZ + korpusa tarih damgası

**Dosyalar:** Modify: `scripts/erisim_korpus/retriever.py` · `data/index/mevzuat_bge_m3_s2/KUNYE.json` ·
Create: `tests/test_yururluk.py` · `data/corpus/KUNYE.json`

**Neden — ölçüldü 2026-09-07, tahmin değil:**

| olgu | sayı |
| :--- | :--- |
| korpus kapsamı | **892 kanun** · 40.496 madde — **kanun katmanı**; yönetmelik/tüzük **yok** |
| `mulga` (yürürlükten kalkmış) bayrağı | korpusta **VAR** — 2.547 madde `True` |
| `retriever.py` bunu kullanıyor mu | **HAYIR** — `grep mulga scripts/erisim_korpus/retriever.py` → **0 sonuç** |
| gerçek koşuda sızıntı | **800 getirilen kaynağın 2'si mülga** (%0,2) · **2/80 kalem** (id 7 · 63) |
| korpusun güncellik tarihi | **YOK** — korpusta **tek bir tarih alanı bile yok** |

⇒ Bugün vatandaşa **yürürlükten kalkmış madde** gösterilebiliyor ve modelin bunu anlamasını
sağlayan **hiçbir sinyal yok**. `CLAUDE.md` *"S2 — carries the validity field"* diyor —
**taşıyor ama kullanılmıyor**; bu çelişki iki yerde damgalanmalı.

**Bu bir "eksik özellik" değil, YANLIŞ CEVAPtır** — bu yüzden `v2`'de değil **burada**.
`CLAUDE.md`'nin çekirdek kısıtı *"güncellik kütüphanede, ağırlıkta değil"* diyor; ama kütüphanenin
**tarihi yok** ve **mülgayı ayırt etmiyor**. İnsan kararı 2026-09-07: **ucuz olan v1'e, inşa v2'ye.**

- [x] **Adım 1: Failing test yaz** — `tests/test_yururluk.py`

İki test: (a) `retriever.getir()` sonuçlarının hiçbirinde `mulga=True` olmayacak — bugün 800
kaynağın 2'sinde var; (b) `data/corpus/KUNYE.json` **anlık görüntü tarihi** taşıyacak ve
`kapsam == "kanun"` diyecek — *"bu korpus ne zamana göre günceldir"* sorusu bugün **cevaplanamıyor**.
Beklenen alanlar: `anlik_goruntu_tarihi` · `kaynak` · `kapsam` · `n_kanun=892` · `n_madde=40496`.

- [x] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör**

Run: `python -m pytest tests/test_yururluk.py -v` → `FAIL` (mülga süzgeci yok · `KUNYE.json` yok)

- [x] **Adım 3: `retriever.py`'de yürürlük süzgeci — ve kararı GÖRÜNÜR kıl**

**Süzmek mi damgalamak mı?** İkisi farklı: süzmek mülga maddeyi **kaybeder** (bazen soru tam da
mülga maddeyle ilgilidir), damgalamak **gösterir ama işaretler**.
**Karar: varsayılan SÜZ**, açıkça istenirse getir; ve getirilen her kaynak `mulga` alanını
**taşısın** ki `hakhukuk/terazi.py` (Görev 7) kullanıcıya rozet gösterebilsin.
**Public API'de bool bayrak yok** (CLAUDE.md §4) → `Yururluk` enum: `YALNIZ_YURURLUKTE`
(varsayılan) · `MULGA_DAHIL`.

`verify:` `pytest tests/test_yururluk.py` yeşil **ve** `recall@10` **0,9500'de KALIR** — o 2 mülga
kaynak hiçbir kalemin **altını değildi**, dolayısıyla süzgeç manşet sayıyı **oynatmamalı**.
Oynarsa **DUR**: sebebi bulunmadan devam edilmez (bu, kaçırdığımız bir bağımlılık demektir).

- [x] **Adım 4: `data/corpus/KUNYE.json` — anlık görüntü künyesi**

Zorunlu: `anlik_goruntu_tarihi` · `kaynak: "mevzuat.gov.tr"` · `kapsam: "kanun"` · `n_kanun: 892` ·
`n_madde: 40496` · `n_mulga: 2547` · `sha256` ·
`kapsam_disi: ["yönetmelik","tüzük","KHK","tebliğ"]` — **ne KAPSAMADIĞI açıkça yazılır**.
`verify:` `pytest` yeşil; `MODEL_CARD.md` ve `README*.md` bu tarihi **alıntılıyor**.

- [x] **Adım 5: Çelişkiyi iki yerde damgala**

`CLAUDE.md`'nin *"S2 — carries the validity field"* cümlesi bugün **yanıltıyor**: alan var,
**kullanılmıyordu**. Düzeltmeden sonra cümle doğru olur; **düzeltme tarihi** yazılır.
`verify:` `CLAUDE.md` ile `data/index/.../KUNYE.json` aynı şeyi söylüyor.

- [x] **Adım 6: Commit**

**v2'ye kalanlar — burada YAPILMIYOR:** canlı `bedesten` API (**B6**, **TR IP şart** — gov
firewall yurtdışı/VPN'i bloke ediyor) · **892 → tam kapsam** (yönetmelik/tüzük; **yeniden
indeksleme** turu ister, B9 ile paketlenir) · otomatik tazelik boru hattı.

---

### Görev 9: Servis katmanı — `answer(soru) → Cevap` (**tek derin modül**)

**Dosyalar:** Create: `hakhukuk/servis.py` · `tests/test_servis.py`
**Bağımlılık:** Görev 5 · 6 · 7 · 8

**Arayüzler:**
- Tüketir: `hakhukuk.istem` · `hakhukuk.tipler` · `hakhukuk.terazi` · `scripts/erisim_korpus/retriever.py`
- Üretir: `answer(soru: str, *, k: int = 10) -> Cevap` — Görev 10 (CLI) ve 12 (TUI) **yalnız
  bunu** çağırır

**Tasarım (POSD derin modül):** Arayüz **tek fonksiyon**; arkasında retriever + llama-server +
istem + terazi **gizli**. Harness **GPU'ya girmez** — embedder CPU'da, indeks CPU RAM'de;
*"sığar/sığmaz"* farkı budur.

- [x] **Adım 1: Failing test yaz — sunucusuz, sahte taşıyıcıyla**

*(kod 2026-09-09'da silindi — karşılığı repoda ve git geçmişinde; plandaki kopya artık güncel değildi.)*

- [x] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör**

Run: `python -m pytest tests/test_servis.py -v` → `FAIL`

- [x] **Adım 3: Uygulama**

*(kod 2026-09-09'da silindi — karşılığı repoda ve git geçmişinde; plandaki kopya artık güncel değildi.)*

`retriever.getir` **imzasını TAHMİN ETME** — `scripts/erisim_korpus/retriever.py`'yi aç, gerçek fonksiyon
adını ve dönüş şeklini oku, koda **onu** yaz. Bu turda üç kez yanlış imza/bayrak çıktı.
`--max-chunk-chars 900` ölçüm rejiminin değişmezidir; `[:900]` kırpması onunla **aynı** olmalı.

- [x] **Adım 4: `_uret`'i doldur** — `llama-server`'a `/v1/chat/completions`,
`temperature=0`, `seed=3407`, `max_tokens=DUSUNCE_BUTCESI + CEVAP_BUTCESI`.
`verify:` `python -m pytest tests/test_servis.py -v` → **3 passed**.

- [x] **Adım 5: UÇTAN UCA KAPI — gerçek sunucuyla 3 soru**

`verify:` üç soruda da `durum` ∈ {`CEVAP`, `CEKINCELI`} · `kaynaklar` boş değil ·
her `dogrulandi=True` atıf gerçekten getirilen kaynaklarda **var** (gözle doğrulanır).

- [x] **Adım 6: Commit**

---

### Görev 10: CLI + sorumluluk ibaresi **AÇIK KARAR S10**

**Dosyalar:** Create: `hakhukuk/cli.py` · `tests/test_cli.py` · Modify: `pyproject.toml`

**Arayüzler:** Tüketir `servis.answer` · Üretir `hakhukuk` konsol komutu

**S10 KISMEN KAPANDI 2026-09-07 (insan kararı): geçici muhafazakâr metin ŞİMDİ girer.**
`hakhukuk/cli.py` içinde **tek sabit** `SORUMLULUK_IBARESI`; `hakhukuk/tui.py` onu **import
eder**, kopyalamaz (S18'in dersi: aynı metin iki yerde durursa sessizce ayrışır).
`Durum` ne olursa olsun **koşulsuz** basılır.
Hâlâ açık: **nihai hukuki metin** — hukukçu görüşü gelince **tek yerden** güncellenir.
Kodda ve model kartında *"GEÇİCİ — S10 açık"* şerhi durur.

- [x] **Adım 1: Failing test yaz**

*(kod 2026-09-09'da silindi — karşılığı repoda ve git geçmişinde; plandaki kopya artık güncel değildi.)*

- [x] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör** → `FAIL`

- [x] **Adım 3: Uygulama** — `argparse`; çıktıda **durum rozeti** · cevap · **atıflar
(doğrulanmamış olanlar ile)** · kaynak listesi · **sorumluluk ibaresi**.
İbare koşullu **değildir**: `Durum` ne olursa olsun basılır.

- [x] **Adım 4: Testi koş, GEÇTİĞİNİ gör** → **2 passed**

- [x] **Adım 5: Commit**

---

### Görev 11: Yeniden üretim yolu — tek komut

**Dosyalar:** Create: `scripts/yeniden_uret.sh` · `docs/YENIDEN_URETIM.md`

**Neden:** Yayımlanan kütle (**%80,1**) bugün **hiç kimse tarafından yeniden üretilemez** —
istem `gen_eval_grounded.py` içindeydi (Görev 5 çözdü), indeks git'te yok (Görev 8 çözecek),
ve komut zinciri hiçbir yerde **tek parça** yazılı değil.

- [x] **Adım 1: Zinciri yaz** — indeks hazırla → llama-server aç → `h1` üret →
geçerlilik kapısı → puanla → `harness_tablo.py`.
`verify:` script `bash -n` temiz; her adım künyeye **ne yazdığını** basıyor.

- **ERTELENDİ** · **Adım 2: TEMİZ MAKİNE KAPISI** — `git clone` + `uv sync` + tek komut.

> **ERTELENDİ 2026-09-07 — bugün koşulsa TANIM GEREĞİ düşer.** `git clone` çalışan bir ürün
> vermiyor çünkü indeks **git'te yok** (`.gitignore:166`, `data/index/**/*.npy` — 79 MB ikili) ve
> dağıtımı **Görev 8**'e bağlı; o da korpus kararını bekliyor. Bu bir eksiklik değil, **bilinen
> bir bağımlılık**: [`docs/YENIDEN_URETIM.md`](../../YENIDEN_URETIM.md) engeli açıkça yazıyor.
> ⇒ Görev 8 açıldığı gün bu adım **onun kapısı** olarak koşulur.
`verify:` üretilen kütle **%80,1 ± 0,3 p** (hakem gürültü tabanı). Dışındaysa **DUR**;
fark **kaynaklanmadan** yayımlanmaz.

- [x] **Adım 3: Commit**

---

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

- [ ] **Adım 6: Gözle doğrula** — `python -m hakhukuk.tui`, üç soru sor.
`verify:` dört durumdan en az ikisi ekranda **ayırt edilebiliyor**; sorumluluk ibaresi
**her** cevapta görünüyor.

- [ ] **Adım 7: Commit**

```bash
git add hakhukuk/tui.py tests/test_tui.py pyproject.toml && \
git commit -m "A7: basit TUI (textual) — answer() üstünde ince kabuk, kapı testiyle korunuyor"
```

---

# FAZ 3 · Belge katmanı ($0) → `v0.2` YAYIN

**Dördü de bugün YOK** (ölçüldü 2026-09-07).

---

### Görev 13: `PRODUCT.md` · `ROADMAP.md` · `TODO.md` · `docs/MIMARI.md`

**Dosyalar:** Create (4) · Delete: `referans-design-doc.md` *(spec §9: insan kararı)*

- [x] **Adım 1: `PRODUCT.md`** — vatandaş kim · hangi soruyu soruyor · cevap neye benziyor ·
**VAAT ETMEDİĞİ** (hukuki tavsiye değil · güncellik indeksin işi · %100 doğruluk değil) ·
`v1`↔`v2` sınırı · üç maddeli kapı · iki sürüm şeması.
`verify:` her nicelik yanında **kaynak dosya adı** taşıyor · *"vaat etmiyor"* bölümü var.

- [x] **Adım 2: `ROADMAP.md`** — bu planın fazları: `HP` → Hat A ∥ → Faz 3 → Hat B → `v1.0` → `v2`.
Her adım: *ne · neden (**hangi ölçülmüş boşluk**) · `verify:` · bedel · bağımlılık*.
`verify:` kritik yol işaretli · **AÇIK KARAR** damgaları **S5·S7·S8·S9·S10·S12·S16·S17·S18**.

- [x] **Adım 3: `TODO.md`** — yalnız **bugün koşulabilir** kalemler; her satır bir `ROADMAP`
adımına bağlı. `verify:` her satırda bağlantı var.

- [x] **Adım 4: `docs/MIMARI.md`** — `v1` zinciri: base → kollar → merge → GGUF → retriever →
istem → `answer()` → CLI/TUI · `v2` sınırı. `referans-design-doc.md` 'nin işlevini devralır.
`verify:` her kutu **var olan bir dosyaya** ya da bir `ROADMAP` adımına işaret ediyor
(döngüyle sınanır, gözle değil).

- [x] **Adım 5: Kırık link onarımı — TARİHSEL KAYITLARA DOKUNMA**

Güncellenir: `CLAUDE.md` · `MODEL_CARD.md` · `README.md` · `README.tr.md` · `DEVIR-PROMPT.md` *(silindi)*.
**Güncellenmez:** `docs/record/**` · `docs/adr/**` — *"o gün şu belge şunu diyordu"* kaydı;
spec §11'in ilk kuralı **KAYIT TEMİZLENMEZ**.
`verify:` `grep -rE '(ROADMAP|TODO|TASARIM|VISION|PAPER_TARGET)\.md' CLAUDE.md README*.md MODEL_CARD.md`
çıktısındaki her yol **var olan** bir dosyayı gösteriyor · `git diff --stat docs/record docs/adr`
→ **0 değişiklik**.

- [x] **Adım 6: `MODEL_CARD.md` tam yazımı** — bugün yalnız *"ESKİ BİRİM"* bandı çakılı.
Yeni manşet · üç maddeli kapının **sayıları** · `HakHukuk-4B-v1.0-Q4_K_M.gguf` ad kuralı
(ADR-0071) · VRAM tablosu (3,09 / 3,70 / 5,76 GiB) · **Limitations**: üç kabul edilen bedel
(dış geçerlilik · kapasite sorusu · ADR-0018'in eğrisi) + **tek aile hakem** borcu.
`verify:` kartta *"ESKİ BİRİM"* bandı **kalmadı**; her sayının yanında kaynak dosya var.

- [x] **Adım 7: `v0.2` etiketi + commit**

---

# FAZ 4 · Hat B — model (~$7-15, Modal) → `v1.0`

**`HP` (Görev 3) bitmeden başlamaz.** Sebebi ADR-0064'ün kendi *"Ne KURULMAZ"* maddesi:
bugünkü her sayı tek ailenin hükmü; kapıyı **panelsiz** koşmak aynı borcu `v1.0`'a taşır.

---

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

### Görev 16: `v1.0` kapı koşusu (~$1) + kabul testi

**DONMUŞ TEST BURADA, TEK KEZ AÇILIR** (`data/eval/canon/`).

**S5 gereği (2026-09-07): Wilson %95 aralıkları her oranın YANINDA raporlanır; kapı hükmü
nokta tahminle kurulur (ADR-0050).** İki şerh **zorunlu**: (a) madde (2)'nin çıpası 8/80'in
aralığı **[4/80 – 15/80]** ⇒ *"gerileme yok"* kuralı **tek kalemlik** oynamayı ihlal sayamaz;
(b) madde (3)'ün ikili ayağında aralıklar **örtüşüyor** ⇒ hüküm nokta tahmine dayanıyor.
Madde (1)'e Wilson **uygulanmaz** (`kütle = coverage × A1` — binom modeli yanlış olur).

- [x] **Adım 1: DEV'de üç maddeyi yeniden koş** — ADR-0064 + **ADR-0074**'ün (panel) bağlayıcı
okumasıyla. `verify:` üç madde de sayıyla; **her sayım adımında gözle okuma**.

> **TÜRETİLDİ 2026-09-07 ($0, veri diskte).** ADR-0074 bağlayıcı hakemi **değiştirmedi**
> (`gpt-4o-mini` kaldı) ⇒ üç maddenin sayıları da değişmedi. Kaynak:
> `outputs/eval/f02-biz-onsozsuz/` (`KUNYE.json` · `harness_tablo.json`).
>
> | madde | sayı | Wilson %95 (S5) |
> | :--- | ---: | :--- |
> | **(1)** kütle ≥ 3.5 Flash − 2,0 p | **0,8011** ↔ eşik 0,7225 · **+5,86 p** çıpa üstü | **UYGULANMAZ** — kütle = coverage × A1, binom modeli yanlış olur |
> | **(2)** isabetsizlik kötüleşmesin | **8/80** = 0,1000 | **[0,052 – 0,185]** = [4,1/80 – 14,8/80] |
> | **(3)** M5 yükselmesin | BİZ 76/80 = 0,9500 ↔ BASE 78/80 = 0,9750 | [0,878–0,980] ↔ [0,913–0,993] |
>
> **İki şerh ZORUNLU oldu ve kapı hükmünün yanında durur:**
> 1. Madde (2)'nin aralığı **[4/80 – 15/80]** ⇒ *"gerileme yok"* kuralı **tek kalemlik**
>    oynamayı ihlal sayamaz.
> 2. Madde (3)'ün aralıkları **ÖRTÜŞÜYOR** ⇒ hüküm **nokta tahmine** dayanıyor. Geçersiz
>    kılmaz, **damgalanır**.
>
> **Ve artık üçünün yanında ölçülmüş bir kırılganlık var:** ikinci hakem ailesiyle kütle
> **0,8011 → 0,6940** (κ 0,534). Bu sayı kapıya **girmiyor** (eşit sınav yok — rakip kolu o
> hakemle puanlanmadı) ama `MODEL_CARD` §7.2'de ve [ADR-0074](../../adr/0074-hakem-paneli-kuruldu-baglayici-hukum.md)'te yazılı.
- [x] **Adım 2: Kabul testi — donmuş TEST** **KOŞULDU 2026-09-09 · insan onaylı, TEK KEZ**
**ADR-0069 raporlaması zorunlu:** ham kütle **manşet ve bağlayıcı**; yanına **tek** tanısal
oran `tavan kullanımı = kütle ÷ recall@10`; **her iki setin `recall@10`'u yanında zorunlu**.
Rakip kıyas cümlesi bu orandan **KURULMAZ**. TEST'in tavanı **≈%75**, DEV'inki **%95**.
`verify:` `OZET.md` ham kütleyi manşet yapıyor; tavan görünmeden oran yayımlanmamış.

**ALINDI** → [`outputs/eval/g16-kabul-testi/OZET.md`](../../../outputs/eval/g16-kabul-testi/OZET.md) ·
[`KUNYE.json`](../../../outputs/eval/g16-kabul-testi/KUNYE.json)
Rejim `f02-biz-onsozsuz/KUNYE.json` ile **her eksende birebir**; kanonik koşucu kullanıldı.
Geçerlilik kapısı: kesiklik **1/40 = %2,5** (eşik %5; DEV tam eşikteydi).

| | **TEST** (40, donmuş) | **DEV** (80) |
| :--- | ---: | ---: |
| **ham kütle — MANŞET** | **0,5804** | 0,8011 |
| `recall@10` = tavan | **0,7500** | 0,9500 |
| tavan kullanımı | **0,7739** | 0,8433 |
| coverage | 0,7750 [0,625–0,877] | 0,9375 [0,862–0,973] |
| aşırı-red | **5/40** [0,055–0,261] | 4/80 [0,020–0,122] **aralıklar ÖRTÜŞÜYOR** |
| **uydurulmuş madde no** | **0/52** | 0/114 |
| `wrong_ref_rate` | **0,2424** | 0,0769 3,2× kötü |

**Düşüşün ayrıştırılması:** toplam **−22,07 p**; tavan-eşdeğer beklenti 0,6324 ⇒ tavanın
açıkladığı **−16,87 p (%76)**, **açıklamadığı −5,20 p (%24)**. ADR-0069'un öngörüsü
doğrulandı **ama tam değil** — model görülmemiş veride tavanını **daha kötü** kullanıyor.
*"Hepsi bileşim"* denmedi.

**Gözle okuma kapısı (ADR-0064 m.\*):** 9/40 çekinmenin dokuzu da okundu, **yanlış pozitif 0**
⇒ ALET = GÖZ, kütle üç okumada da 0,5804.

**ADR-0069 kendi içinde çelişiyor, damgalanır:** oranı `kütle ÷ recall@10` diye tanımlıyor,
örneğinde `0,730 ÷ 0,9375` (coverage) kullanıyor. Tanım esas alındı; coverage paydasıyla
TEST 0,7489 ↔ DEV 0,8545. ADR'ye dokunulmadı.

**DONMUŞ TEST BİR KUSUR YAKALADI ve düzeltildi (TDD):** `atif_dogrula.py` çok anlamlı kanun
adında adayları `sorted()` ile geziyordu; `İŞ KANUNU` için bu **1475 (mülga)** demekti ve
**doğru cevap MÜLGA damgası yiyordu** (id 32, altın 4857/111, 1. sırada). Kodun kendi ilkesi
tek `kanun_no` içinde vardı, adaylar arasında yoktu. TEST atıf **DOGRULANDI 50→52 · MULGA 2→0**.
Manşet **değişmedi** (kütle bu doğrulayıcıdan gelmiyor) · geçmiş sayılar **oynamadı**
(DEV 114, Sonnet 161+2 aynı).

- [x] **Adım 3: Hüküm** **VERİLDİ 2026-09-09 → [ADR-0077](../../adr/0077-v1-0-verilmedi-v0-3.md)**

**`v1.0` VERİLMEDİ; ürün sürümü `v0.3`.** İnsana soruldu, *"tercih yok"* denerek **devredildi**
⇒ karar **model tarafından** verildi ve ADR'de böyle damgalandı (insan **tersine çevirebilir**).
Gerekçe **yeni bir eşik değil**, ADR-0064'ün kendi metni: `v1.0` için eksik iki şeyden
**(a) kabul testi koşmadı → KAPANDI**, **(b) tek hakem ailesi → AÇIK** (κ 0,534 < 0,6, G2
atlandı) ⇒ **`v1.0`'ı bloke eden model değil, ölçüm aygıtı.**
`verify:` hüküm **aynı sayıyla** üç yerde: [ADR-0077](../../adr/0077-v1-0-verilmedi-v0-3.md) ·
[log #65](../../record/research_log/2026-09-09-kabul-testi-ve-frontier-kiyasi.md) ·
`MODEL_CARD.md` §5.

**Ön-kayıtlı sayısal kabul eşiği YOK — bu bir bulgudur, mazeret değil:**
ADR-0064 m.(1) eşiği `3.5 Flash − 2,0 p`; o çıpa **DEV**'de ölçüldü, rakipler donmuş TEST'te
**hiç koşmadı** ⇒ eşik TEST'te **türetilemiyor**. ADR-0069 m.3 tavan kullanımını **kapı
olmaktan men ediyor**. Planın kendi cümlesi yalnız *"geçerse `v1.0`"* diyor ve **"geçmek"
tanımsız**. Sayıyı gördükten sonra eşik yazmak ADR-0050'nin yasakladığı şeydir.
⇒ `v1.0` mü, `v0.3` mü — **insan verir** (ADR-0065 ikisini de mümkün kılıyor).
Geçerse **`v1.0`** + `HakHukuk-4B-v1.0-Q4_K_M.gguf` (ADR-0071).
Geçmezse sayı **damgalanarak yayımlanır** ve `v0.x` devam eder (ADR-0065).
`verify:` hüküm ADR'de, `research_log`'da ve `MODEL_CARD.md`'de **aynı sayıyla** duruyor.
- [x] **Adım 4: Commit + etiket** BİTTİ **2026-09-09** — etiket `v0.3` (kapı geçilmedi, ADR-0077)

---

### Görev 18 : Araç katmanı — KALDIRAÇ *(ADR-0076 · 2026-09-08)*

**Dosyalar:** Create: `hakhukuk/araclar.py` · `tests/test_araclar.py` ·
Modify: `hakhukuk/servis.py` · `hakhukuk/tipler.py` · `tests/test_tipler.py`

**Neden:** bugünkü akış **tek atış ve sabit** — model arayıp aramayacağına, tekrar
arayacağına, bir maddenin metnini okuyup okumayacağına **karar vermiyor**.

**ÖNCE BUNU OKU — bu görevin ilk gerekçesi ÖLÇÜLDÜ ve ÇÜRÜDÜ (2026-09-08):**
Taslak *"model TBK 214 ile TBK 217'yi yan yana okuyabilseydi görürdü"* diyordu.
`harness.altin_sirasi` alanı okundu:

| eksen | büyüklük | altın bağlamda mıydı | araç çözer mi |
| :--- | ---: | :--- | :--- |
| isabetsizlik | 8/80 | **8/8 EVET** (biri 1. sırada) | sorun **seçim**, erişim değil |
| aşırı-red | 4/80 | **4/4 EVET** (üçü 1. sırada) | model bakıyor, kullanmıyor |
| uydurulmuş madde | **0**/114 | — | çözülecek sorun yok |
| **recall kaybı** | **4/80** | gelmedi | `ara` **deneyebilir** — TEK hedef |

⇒ **Eval hedefi 4 kalem, garanti değil.** İnsan kararı (2026-09-08): beş araç da konur,
ama gerekçe **eval kazancı değil ÜRÜN YETENEĞİ** — ve bu gerekçe **ölçülmemiştir**,
öyle damgalanır ([ADR-0076](../../adr/0076-kapi-kaldirac-ayrimi-arac-katmani.md)).
Araç katmanının kazancı **yayımlanan hiçbir sayıya eklenmez**.

**KAPI ↔ KALDIRAÇ ayrımı bağlayıcı** (ADR-0076): atıf doğrulama · mülga süzgeci · durum
sınıflandırma **TOOL DEĞİLDİR**, döngünün **dışında** koşulsuz çalışır. Uydurulmuş madde
**0/114** garantisi buradan geliyor; tool yapılırsa model çağırmayı unuttuğu an buharlaşır.

- [x] **Adım 1: Failing test — beş araç + KAPI'nın atlanamazlığı** **2026-09-09** — `tests/test_araclar.py` (8 test) + `tests/test_servis.py`'ye 5 araç testi

En kritik test: *"model hiç araç çağırmasa bile atıf doğrulama ÇALIŞIR"* ve
*"model `terazi`'yi atlayamaz"*. Araç testleri deterministik (sahte korpusla, indekssiz).

- [x] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör** `ModuleNotFoundError: hakhukuk.araclar` — kırmızı görüldü

- [x] **Adım 3: `Durum.ARAMA_TUKENDI` + `tipler.py`** dört hâl **beşe** çıktı; `test_durum_dort_hali_var` → `test_durum_bes_hali_var`, gerekçesi testin docstring'inde

`tests/test_tipler.py::test_durum_dort_hali_var` **kırılacak** — beklenen, davranış
değişiyor: dört hâl **beşe** çıkıyor. Test güncellenir, gerekçesi yazılır.
`KESIK` ile **birleştirilmez**: `KESIK` = *"cümle yarım"*, `ARAMA_TUKENDI` = *"cümle tam,
dayanağı eksik olabilir"* — kullanıcıya **farklı şey** söylerler.

- [x] **Adım 4: `hakhukuk/araclar.py` — beş deterministik araç** `Araclar` sınıfı

| araç | imza | ölçülmüş hedef |
| :--- | :--- | :--- |
| `ara` | `(sorgu: str, k: int = 10) -> tuple[Kaynak, ...]` | **4/80** recall kaybı |
| `madde_getir` | `(kanun_no: str, madde_no: str) -> Kaynak \| None` | yok — ürün yeteneği |
| `madde_var_mi` | `(kanun_no: str, madde_no: str) -> bool` | yok — uydurma zaten **0/114** |
| `kanun_bul` | `(ad: str) -> tuple[tuple[str, str], ...]` | yok |
| `yururlukte_mi` | `(kanun_no: str, madde_no: str) -> Yururluk \| None` | yok |

**Hiçbiri LLM çağırmaz** — araç katmanı deterministik kalır, yoksa yeni bir hata kaynağı olur.
Kimlik karşılaştırmaları **`madde_anahtari` ile** yapılır (büyük/küçük duyarsız, `Geçici
Madde` ayrı) — düz metin karşılaştırması korpusun **%22'sinde** yanlış negatif veriyordu.
`verify:` her araç için birim testi yeşil; hiçbiri ağ ya da model istemiyor; testler sahte
korpusla koşuyor (indeks gerekmiyor).

**ALINDI 2026-09-09 — 8 test yeşil, ağ/model/indeks YOK.**
**Plandan sapma, damgalanır:** planın imzaları modül fonksiyonu (`ara(sorgu, k=10)`);
uygulama bir **sınıf** (`Araclar`) — metot imzaları **birebir aynı**, ama korpus enjekte
edilebilir olduğu için testler sahte korpusla, monkeypatch'siz koşuyor. Modül fonksiyonu
gizli bir tekil (singleton) isterdi ve testte onu yamamak gerekirdi.
**Donmuş TEST'in dersi araç katmanına taşındı:** `kanun_bul` ada uyan **BÜTÜN** kanunları
döndürür — tek numara döndürmek, `atif_dogrula.py`'de bugün onardığımız kusurun (alfabetik
ilk aday = mülga 1475) araç katmanında yeniden üretilmesi olurdu.
`ara`, retriever verilmemişse **açıkça patlar**: sessiz boş liste *"sonuç yok"* ile
*"arama hiç çalışmadı"*yı vatandaş için aynı şeye çevirirdi.

- [x] **Adım 5: çok adımlı mod, SINIRLI döngü** `servis.answer_arac()` — AYRI fonksiyon

```python
AZAMI_ADIM = 4     #    sınır. Dayanınca Durum.ARAMA_TUKENDI — sessizce teslim EDİLMEZ.
```
`verify:` döngü sınırına dayanan senaryo testte `ARAMA_TUKENDI` veriyor · KAPI'lar döngü
sonrası **her hâlde** çalışıyor (araç çağrılmasa da).

**ALINDI 2026-09-09.** **Plandan sapma:** `answer()`'a bayrak eklenmedi, **AYRI
fonksiyon** yazıldı — `servis.answer_arac()`. Sebebi iki katlı: (1) CLAUDE.md §4 public
API'de bool bayrağı yasaklıyor; (2) ayrılık **regresyon kapısını yapısal olarak** kazanıyor —
`git diff` `servis.py` için **120 ekleme, 0 silme**, yani araçsız yolun kodu **hiç
dokunulmadı**.
**Bugün taşıyıcı araç çağrısı AYRIŞTIRMIYOR** ve bu `_uret_arac`'ta açıkça yazılı:
llama-server tarafında tool-calling açılana kadar araçlı yol tek atış davranır. Sessiz boş
demet döndürmek *"model araç istemedi"* ile *"taşıyıcı aracı taşımıyor"*u aynı şeye çevirirdi
⇒ **borç, gizlenmedi.**

- [x] **Adım 6: REGRESYON KAPISI — araçsız davranış DEĞİŞMEDİ mi** **GEÇTİ 2026-09-09**

Araç katmanı **varsayılanı bozmamalı**: araç kullanılmayan yolda 80 kalemlik sınıflandırma
çıktısı **birebir aynı** kalmalı (suskunluk `[15, 37, 45, 66, 79]`).
`verify:` 80 kalem yeniden koşuldu, suskunluk kümesi **değişmedi**.

**ALINDI 2026-09-09 — ölçülerek, iddiayla değil.** Aynı betik, aynı sunucuya karşı, iki
kez koşuldu: bir kez bu görevin kodunda, bir kez `4d69388`'de (görev öncesi, ayrı `git
worktree`). Sonuç:

> **80/80 kalem BİREBİR AYNI** — `durum` · `atif` · `kaynak` · `metin`, dördü de özdeş.

Artefaktlar: [`aracsiz_yol_80.json`](../../../outputs/eval/g18-arac-katmani/aracsiz_yol_80.json)
(sonrası) · [`aracsiz_yol_80_ONCESI.json`](../../../outputs/eval/g18-arac-katmani/aracsiz_yol_80_ONCESI.json)
(öncesi) · betik `scripts/olcum_uretim/regresyon_aracsiz_yol.py`.

**Kapı önce KIRMIZI yandı ve sebebi kayda geçer: karşılaştırma yanlıştı, kod değil.**
Betiğin ilk sürümü suskunluk kümesini planın ön-kayıtlı `[15, 37, 45, 66, 79]` kümesiyle
karşılaştırıyordu. O küme **ölçüm hattının** kümesidir (`gen_eval_grounded.py` +
`exact_reject`) ve öncesi/sonrası koşusu bunu kesinleştirdi: **öncesi de aynı kümeyi
veriyor** ([10, 34, 63]). Betik onarıldı; artık tek koşudan hüküm kurmuyor.

---

**BU KOŞUNUN YAN ÜRÜNÜ: ÜRÜN YOLU İLE ÖLÇÜM HATTI AYNI ŞEYİ ÇALIŞTIRMIYOR**
*(yeni borç — bu görevin kırdığı bir şey değil, öncesi koşusuyla kanıtlandı)*

| | ürün yolu (`servis.answer`) | ölçüm hattı (**yayımlanan 0,8011 buradan**) |
| :--- | ---: | ---: |
| kesik/boş cevap | **7/80 = %8,75** | 4/80 = %5,0 |
| **tamamen BOŞ metin** | **4/80 = %5,0** (id 7 · 64 · 65 · 66) | **0** |
| suskunluk kümesi | [10, 34, 63] | [15, 37, 45, 66, 79] |

Yedi kesik kalemin **yedisi de** ölçüm hattında `finish=stop` ile tamamlanıyor (485-892
token) ⇒ sorun soruların zorluğu değil, **bütçe mimarisi**. Ölçüm hattı düşünceyi 1024'te
**zorla kapatıp** cevaba ayrı 512 veriyor; ürün yolu ikisini tek havuzda (1536) yarıştırıyor.
Sonuç `research_log` #42'nin ölçtüğü **sonlanmama**: model `</think>`'i hiç kapatmıyor,
bütçeyi düşünce kanalında bitiriyor, **HTTP 200 ile boş içerik** dönüyor.

Boş cevap **gizlenmiyor** (durum `KESIK`, rozet *"cevap YARIM"*) ama vatandaş için sonuç
boş ekran. **ADR-0040'ın geçerlilik kapısı %5'tir; ölçüm hattı tam eşikte geçiyor, ürün
yolu %8,75 ile GEÇEMEZDİ.**
**Bugün düzeltilmedi:** ürün yoluna zorunlu kapatma koymak **rejim değişikliğidir** ⇒
insan kararı + yeniden ölçüm ister (goal kuralı: *"yeni rejim → DUR ve SOR"*).
Model kartında ve HF kartında **açıkça** yazılıdır.

- [x] **Adım 7: CLI/TUI'de görünürlük** `ARAMA TÜKENDİ` (CLI) · `🔵 ARAMA TÜKENDİ` (TUI); `test_cli_bes_durumu…` yeşil

`verify:` `ARAMA_TUKENDI` rozeti CLI ve TUI'de **görünüyor**; `python -m pytest` yeşil.

---

### Görev 17 : Modeli YAYINLA — `v1` release *(ADR-0075 · 2026-09-08)*

**Dosyalar:** Create: `hakhukuk/kurulum.py` *(kısmi)* · Modify: `README.md` · `README.tr.md` · `MODEL_CARD.md`

**Ölçülmüş boşluk — plan bunu HİÇ içermiyordu, insan sorusu ortaya çıkardı (2026-09-08):**

| | durum |
| :--- | :--- |
| repo | `github.com/Rfetha/Hukuk-SLM` — kod · veri · araştırma kaydı **public** |
| ağırlıklar | `models/gguf/tgta_v1-q4_k_m.gguf` · **2,6 GB** · yalnızca **yerel diskte** |
| git'te mi | hayır — `.gitignore:41` `*.gguf` |
| HF'de mi | **hayır** — `README*.md` ve `MODEL_CARD.md`'de **tek bir HF linki yok** |

⇒ *"açık kaynak model"* iddiası bugün **yarım**: kod + veri + kayıt açık, **ağırlıklar değil**.
[ADR-0071](../../adr/0071-v1-release-artefakti-tek-gguf.md) **ne** yayımlanacağını karara
bağlamış (tek GGUF + ad kuralı) ama **nasıl ve ne zaman** hiçbir yerde yazılı değildi.

- [x] **Adım 1: Artefaktı ADR-0071'in adıyla hazırla** **BİTTİ 2026-09-09**

Kapı sonucuna göre ad: geçerse `HakHukuk-4B-v1.0-Q4_K_M.gguf`, geçmezse
`HakHukuk-4B-v0.2-Q4_K_M.gguf` (ADR-0065 bölünmüş sürümleme buna izin veriyor).
İç ad `tgta_v1-q4_k_m.gguf` **korunur** — iki ad ayrı iş görür (`kollar.md`).
`verify:` `sha256` hesaplandı ve `kollar.md`'ye yazıldı; boyut **2,59 GiB**.

**ALINDI 2026-09-09** → [`kollar.md`](../../record/kollar.md) *(2026-09-09 bloğu)*
`sha256` **`755e15e92e9f7021934f2d5eada6c1f02fcc92be23f0536b0c2a0a9586e7bffc`** ·
**2.783.446.720 bayt = 2,592 GiB** (ADR-0071'in 2,59 GiB'iyle tutuyor).
**Ad, plandan SAPIYOR ve sebebi yazılı:** plan bu dalda *"`v0.2`"* diyordu; `v1.0` kapısı
geçilmedi (ADR-0077) ve ürün sürümü **`v0.3`** oldu — `v0.2` git'te **zaten etiketli**, bugün
yapılan yayına verilemez ⇒ **`HakHukuk-4B-v0.3-Q4_K_M.gguf`**.
Dosya kopyalanmadı: 2,6 GB'lık ikinci kopyanın karşılığı yok, ad yükleme anında verilir.
`docs/record/kollar.md`'ye **yeni tarihli blok eklendi**, geçmiş satır **yeniden
yazılmadı** — kaydın *"o gün bu belge bunu diyordu"* niteliği korundu.

- [x] **Adım 2: HF model reposu — kart + lisans + İNDEKS ŞERHİ** BİTTİ **2026-09-09**

**En kritik satır:** model **tek başına indirildiğinde yayımlanan sayıyı ÜRETEMEZ** —
`%80,1` bir *harness AÇIK* sayısıdır, bağlamı **retriever** seçmiştir. Kartta bu **ilk
ekranda** durmalı, dipnotta değil.
`verify:` HF kartı `MODEL_CARD.md`'nin manşetini **aynı sayıyla** taşıyor · indeks engeli
(`Görev 8`) **açıkça** yazılı · Apache-2.0 + `NOTICE` yerinde.

**ALINDI 2026-09-09** → **https://huggingface.co/Rfetha/HakHukuk-4B-v0.3-Q4_K_M**
**Durum: ÖZEL** — insan kararı 2026-09-09: açık kusurlar giderilene kadar depo özele alındı.
Yükleme ve bütünlük doğrulaması tamamlanmıştır; geri alınan yalnız görünürlüktür.
Yüklenenler: `HakHukuk-4B-v0.3-Q4_K_M.gguf` · `README.md` (model kartı) ·
`ORNEK_CEVAPLAR.md` · `LICENSE` · `NOTICE`.

**Bütünlük kanıtı — iddia değil, ölçüm:** HF'teki dosyanın boyutu **2.783.446.720 bayt** ve
`sha256` değeri **`755e15e92e9f7021…`**, yereldeki artefaktla **birebir** (`kollar.md`,
2026-09-09 bloğu). Yükleme bozulmadı.

Kartın **ilk üç bölümü** şu kısıtları taşıyor: (1) model tek başına bildirilen başarımı
**üretemez**, indeks dağıtılmadı (Görev 8); (2) ürün yolunda cevapların **~%5'i boş** döner
(Görev 18 Adım 6'nın yan ürünü); (3) hukuki tavsiye değildir.
Karşılaştırma bölümü tek sütunluk kütle tablosundan **tam skor kartına** genişletildi:
11 eksen × 5 özne + temel model sütunu, kütlenin üç okuması ve eşit sınav kanıtı ayrı
tablolarda. Sonnet-5'te ölçülmeyen iki eksen *"ölçülmedi"* yazıldı, tahmin yazılmadı.

- [x] **Adım 3: `README.md` · `README.tr.md` · `MODEL_CARD.md` — indirme yolu** BİTTİ **2026-09-09**

`verify:` üç belgede de **çalışan** HF linki var; `tests/test_belgeler.py` yeşil.

- [x] **Adım 4: Commit + etiket** BİTTİ **2026-09-09** — `v0.3` etiketi atıldı, 16 commit yerelde (push insan kararı bekliyor)

**Sürüm etiketi kapı sonucuna bağlıdır** — `v1.0` ancak Görev 16 geçerse verilir.

---

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
| **B1** | **İsabetsizlik** — gerçek ama soruya uymayan maddeden cevaplama (`ADR-0055`) | ~~5/80~~ → **8/80** *(v2 birimi, ilk kez gözle)* | **Görev 14** — birinci sıra eksen |
| **B4** | `τ_a` merge'de seyreliyor (0,987 → 0,766, **−22,1 p**); çare eğitim **genliğinde** | `‖τ_a‖` **1,1806** ↔ `‖τ_g‖` 10,4722 (8,87×) | **Görev 15** |
| **YB2** | M2b bir **eğitim** borcu — kapı yolu ölçülerek öldü | `h2b@k=4` **0,735 < 0,766** | **Görev 15 Adım 3** |
| **YB6** | 🔴 **Dağıtım istemi artefaktı YOK** | istem 5 dosyada, biri **sürüklenmiş** (S18) | **Görev 5** — sert engel |
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

🚨 **KAPSAM İNSAN KARARIYLA GENİŞLETİLDİ ve çelişki iki yerde damgalandı.** Bu planın başlığı
`v0.2 → v0.3`'tür ve [`00-IS-SIRASI.md`](../00-IS-SIRASI.md) bugüne kadar *"CLI + TUI yeterli
(insan kararı) — HTTP API ve web arayüzü **v2**"* diyordu. O cümle **artık geçerli değil**:
API `v1` tarafına alındı. Gerekçe teknik değil, insan tercihidir; öyle yazılır.
⛔ **S9 AÇILMADI:** API **yerel ve tek kullanıcı**dır (`127.0.0.1`). Barındırma, kimlik, hız
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
| 5 | Boş/boşluk sorgu → **422** | Ölçüldü: `_getir("")` sabit gürültü döndürüyor. ⛔ Uydurulmuş uzunluk eşiği **YOK** |
| 6 | **Serileştirilmiş** tek istek · opsiyonel ekstra `hakhukuk[api]` | Tekilin evre güvenliği **ölçülmedi**; ölçüm rejimi sıralı istekti. Çekirdek kurulum şişmez (`pyproject.toml` ilk satırındaki karar) |

- [ ] **Adım 1: Failing test** — `tests/test_api.py`, `TestClient` ile, **sunucu ve model YOK**
(`servis.answer` monkeypatch'lenir). Sınanacaklar: `sunum` dizesi dört parçayı da taşıyor ·
boş sorgu 422 · boş metin 503 · dolu KESİK 200 · API'nin kendi mantığı yok (kaynak denetimi).

- [ ] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör**

- [ ] **Adım 3: Bağımlılığı opsiyonel ekstra olarak ekle**
`verify:` `pip install -e .` çekirdek bağımlılıkları **değiştirmiyor**; `[api]` ekstrası
`fastapi` ve `uvicorn`'u getiriyor, sürümler **kurulu ortamdan okunarak** pinlenir.

- [ ] **Adım 4: `hakhukuk/api.py` — uygulama**
`verify:` her altı karar testle çivili; `api.py` içinde `REJECT_RE`, `siniflandir(`, `_getir(`
geçmiyor (ince kabuk kapısı, `test_tui.py`'nin aynısı).

- [ ] **Adım 5: Testi koş, GEÇTİĞİNİ gör + commit**

- [ ] **Adım 6: Gözle doğrula** — `hakhukuk-api` ile aç, bir soru sor, cevabı **gör**.
`verify:` `sunum` alanı ekranda rozet + atıf + kaynak + ibare taşıyor; boş sorgu 422 dönüyor.
⛔ Bu da bir **insan gözü kapısıdır** (SIRA 2 ile aynı sınıf).

⚠️ **Bu görev ticket 1 ve 3'ü ÇÖZMEZ.** Boş cevap kusuru (~%5) API'de 503 olarak **görünür**
hâle gelir ama **giderilmez**; donma sorunu API'de yoktur çünkü istek serileştirilir ve istemci
bekler. İkisi de [`post-hp-hat-b-tickets.md`](post-hp-hat-b-tickets.md)'de açık kalır.
