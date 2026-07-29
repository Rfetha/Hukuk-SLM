# Yürütme tuzakları — yeni hat (Qwen3.5-4B)

> **Bu belge ne:** *"hata vermeden yanlış sonuç üreten"* kalıpların tek listesi. Her satır bu hatta
> **fiilen ısırdı**; hiçbiri teorik değil. Bir koşuya başlamadan önce ilgili bölümü oku.
>
> **12B hattının karşılığı:** [`../adr/gemma4-12b-dersler.md`](../adr/gemma4-12b-dersler.md) Bölüm A.
> Orada **base-agnostik dersler**, burada **bu hattın yürütme tuzakları** var. Bazıları aynı dersin
> yeni base'deki tekrarıdır — o zaman ikisi de işaretlidir.
>
> **Kaynak:** `sprint1.md` (Sprint 1 yürütme belgesi, **kapandı**) uyarı blokları + `research_log`
> [#39](research_log/2026-07-24-cp0-base-dogrulama-kapisi.md) ·
> [#40](research_log/2026-07-25-cp4-fla-core-ve-hiz-kaldiraclari.md) ·
> [#41](research_log/2026-07-29-cp6-tau-grounding-olcumu.md).
>
> **Ekleme kuralı:** yeni bir sessiz-bozulma çıkarsa **aynı gün** buraya bir satır + `research_log`
> girdisi. Kalıcı bir karar doğuruyorsa ayrıca ADR.

---

## Neden bu belge var

Bu hattın hata sınıfı **çökme değil, sessiz yanlışlık**. Sunucu açılır, istek **200** döner, JSON
gelir, skorlama scripti sayı üretir, tablo dolar — ve sayı yanlış bir şeye aittir. Regex omurgası
**boş çıktı üzerinde de** çalışır, `--data` varsayılanı **doğru boyutta** yanlış set verir,
kuantizasyon yarıda kesilse de dosya **diskte durur**.

> **Tek kural:** bir sayı üretildiğinde *"bu sayı neyin sayısı"* sorusunun cevabı **künyeden**
> okunabilmeli. Okunamıyorsa sayı yoktur.

---

## 1. Üretim / eval

| # | tuzak | ne olur | korunma | kaynak |
| :-- | :--- | :--- | :--- | :-- |
| 1.1 | **`--data` düşürülür** | Varsayılan `data/train/grounded_qa/test.jsonl` — CANON değil, **eğitim setinin komşusu**. `--n` havuz boyutuyla aynı olduğu için çıktı *doğru görünür* | `--data` her modda **açıkça** yaz | sprint1 CP2 |
| 1.2 | **`--thinking off` düşürülür** | Qwen3.5 düşünen model: `</think>` kapanmaz → `content=''`, HTTP **200**, sıfır hata. Script'e **erken patlama kapısı** eklendi ama bayrak yine zorunlu (ADR-0030) | künyede `thinking=off` gör | #39 Bulgu 1 |
| 1.3 | **Şablon dalı yanlış render** | minja bir dalı yanlış değerlendirdi (12B'de); model **hiç durmadı**, girdiyi tekrarladı. Hiçbir aşamada hata yok | `/apply-template` çıktısını **gözle** oku; `enable_thinking` true/false **farklı** render vermeli | #38 · #39 kapı 2 |
| 1.4 | **`--max-chunk-chars 900` düşürülür** | Eval-mirror kırılır — model eğitildiğinden **uzun bağlamla** ölçülür (ADR-0011 değişmezi) | CP2/CP6 bayrakları birebir | sprint1 CP6 |
| 1.5 | **`--n` / seed kayması** | Kıyasın iki tarafı farklı örneklem → delta anlamsız | n = 80/80/70/80/80/80, seed **3407** | sprint1 CP2 |
| 1.6 | **Güç durumu** | Pilde **7.9** t/s, şarjda **134** t/s — **17×**. Performans sayısı prize bağlı | ölçüm öncesi şarj durumunu künyeye yaz | #39 Bulgu 2 |
| 1.7 | **Yanlış runtime ile kıyas** | Çıpalar Q4_K_M GGUF + llama-server ile üretildiyse, `--adapter` (transformers, 4-bit) yolu **kıyaslanamaz** sayı verir — tablo yine dolar | özne hep aynı taşıyıcıdan; adaptör **merge edilip GGUF'a** gider | #41 §2 |

## 2. Hakem / skorlama

| # | tuzak | ne olur | korunma | kaynak |
| :-- | :--- | :--- | :--- | :-- |
| 2.1 | **Red-regex kalibre edilmemiş** | Base'in baskın red kalıbı `bulunmuyor`u görmüyordu → kalibrasyonsuz **M3 0.000** (gerçek 1.000), **M2b 0.662** (gerçek 0.987) | her **aile** için ayrı kalibrasyon; 15/15 ileri + 2/2 geri elle | #39 Bulgu 3 |
| 2.2 | **Rakip ailesi kalibre edilmemiş** | Rakibin reddi **eksik sayılır** → sapma **bizim lehimize**. TASARIM §3.4: kalibrasyonsuz hiçbir abstention sayısı raporlanmaz | `compare_runs.py` kalibre edilmemiş etiketi **⚠️ ile işaretler** | sprint1 CP7 |
| 2.3 | **A1 yerine ham ortalama** | Çekinme faith=0 alıp ortalamayı çeker: 12B'de ham 0.737 vs gerçek **0.904**; bu hatta base ALL 0.8385 vs **A1 0.973** | A1 **cevaplanan-only** (`rescore_answered.py`) + **coverage yanında** | ADR-0011 · #39 |
| 2.4 | **Coverage değişince A1 kıyası** | Model daha çok cevaplamaya başlayınca A1 kıyası elmayla-armut olur (base kendi seçtiği kolay dilimde ölçülür) | **eşleştirilmiş alt küme**: ikisinin de cevapladığı sorularda A1 | #41 §4.2 |
| 2.5 | **`rejection_exact` ↔ `rejection_rate` karıştırılır** | regex-red ile LLM-red farklı şey ölçer; hakem "reddedip sonra açıklayan" cevabı ABSTAIN sayar, regex saymaz | ikisi **birlikte** raporlanır | #39 CP2 |
| 2.6 | **Payda kayar** | `valid_traps` modele göre değişir (M2b: 75 / 67 / 80) — oran aynı paydada değil | oran **payda ile** yazılır | #41 §3 |
| 2.7 | **Sağlayıcı pinlenmemiş** | Aynı model kimliği farklı servis yığınında (farklı kuantizasyon) koşar → sayılar kıyaslanamaz, **hata vermez** | özet JSON'da `judge_providers` **tek eleman**; `compare_runs.py` yığın uyuşmazlığında **tabloyu basmaz** | ADR-0029 |
| 2.8 | **Hakem gürültüsü sinyal sanılır** | Aynı girdi + aynı hakem, iki koşu: `faith_macro` ±0.005 ama **`cit_precision` ±0.044** | tavan dışı `cit_precision`'da 0.04'lük fark **sinyal değildir**; `runs=1` künyeye yazılır | #41 §6 |
| 2.9 | **Regex kopyası çoğalır** | `rescore_answered.py` kalibre edilmemiş bir regex **kopyası** taşıyordu → tüm A1/coverage sayıları yanlıştı | tek kaynaktan import (`score_abstention.REJECT_RE`) | CP7 kaydı |
| 2.10 | **Eğitim biçimi hakemde cezalanır** | RAFT şablonunun 1. adımı (*"ilgili kaynak KAYNAK 3'tür, diğerleri farklı konuda"*) kaynak **hakkında** cümle → hakem `NOT_IN_SOURCE` der. `τ_g`'nin desteksiz iddialarının **%58'i** bu | 🔴 **AÇIK** — `open_questions.md` §13.8, `τ_a`'dan önce karara bağlanmalı | #41 §4.3 |
| 2.11 | **`.env` yüklenmez** | Hakem anahtarı görünmez, script ilk adımda durur (bu sefer **gürültülü** — para harcanmadı) | skorlama kabuğunda `set -a; source .env; set +a` | #41 (oturum) |

## 3. Eğitim

| # | tuzak | ne olur | korunma | kaynak |
| :-- | :--- | :--- | :--- | :-- |
| 3.1 | **`--target-modules` verilmez** | Eski varsayılan `in_proj_*`'ı kaçırıyordu → **24 linear-attention katmanı LoRA'sız** kalır, hata vermeden. Bedeli ölçüldü: `‖τ_g‖`'nin **%26.8'i** | bayrak **zorunlu ve varsayılansız** (`train_sft.py` · `train_orpo.py`) | #40 Bulgu 4 · #41 |
| 3.2 | **`all-linear` VLM'de** | Qwen3.5 bir **VLM** — `all-linear` görüntü kulesine de LoRA takar | metin kulesi modül listesi açıkça verilir (11 modül) | #39 CP0.7 |
| 3.3 | **Turn işareti yanlış** | `train_on_responses_only` **hiçbir şeyi maskelemez**, loss tüm diziden akar, eğitim **sessizce** bozulur | `train_sft.py` render'a karşı assert eder — assert'in **tetiklendiğini smoke'ta gör** | 12B #38 |
| 3.4 | **`fla-core` eksik** | `import fla` çalışır (→ transformers fast-path'i **açık sanır**) ama `fla.modules` yok → **model hiç yüklenmez**. Eksik `fla-core`, fla'nın hiç olmamasından **kötü** | `--no-deps` ile kurulumda `fla-core` ayrıca | #40 Bulgu 1 |
| 3.5 | **`causal-conv1d` yok** | *"fast path is not available"* uyarısı basılır — **uyarı ölçüt değil**, `s/it` ölçüt. Çıktı geçerli, fallback matematiksel olarak aynı | hızı ölç, uyarıyı okuma | #40 · #41 |
| 3.6 | **Modal yol tuzağı** | `--data` **konteyner** yoludur (volume `/data`'ya bağlı) — yerel yol verilirse koşu yanar | `/data/<dizin>`; script artık model yüklenmeden **saniyede** patlar | #40 Bulgu 4 |
| 3.7 | **`remote()` / `--detach`siz `spawn`** | Ephemeral app entrypoint bitince kapanır, job **iptal olur**; `remote()` client'a bağlı bekler, WSL kapanınca SIGTERM → job ölür. **4 koşu yakarak** öğrenildi | `spawn()` + `--detach` | 12B dersler |
| 3.8 | **ORPO `--adapter` (continuation)** | `--adapter tg` yazmak **ardışık SFT** üretir — yani kolu değil **Taban B'yi** kaydeder, ve fark edilmez | `--fresh-adapter` **zorunlu** | TASARIM §4.1.1 |
| 3.9 | **Rejim sapması** | precision / `r`/`alpha` / dropout / seed / `target_modules` kollar arasında ayrışırsa `τ = θ_ft − θ_base` tanımı bozulur → **merge geçersiz** | TASARIM §4.1.1 zorunlu-eşleşen tablosu | ADR-0036 |
| 3.10 | **Epoch sayısı 1 sanılır** | 1.741 çift ÷ etkin batch 64 = epoch başına **27 adım**; `τ_g` 1.083 adım koşuyor. 1 epoch ORPO ham base'den yeni davranış öğretmez | ORPO **`epochs = 3`** (82 adım) | TASARIM §4.1.1 |

## 4. Veri

| # | tuzak | ne olur | korunma | kaynak |
| :-- | :--- | :--- | :--- | :-- |
| 4.1 | **`--exclude`suz DEV üretmek** | CORE-HARD seçimi **seed'den bağımsız ve sıralı** — farklı seed aynı maddeleri verir. `--exclude`suz "DEV" TEST'in ikinci bir kopyasıdır, **hata vermez** | `--exclude` + **kesişim = 0** kabul ölçütü | sprint1 CP1 |
| 4.2 | **Teacher jargonu sızar** | Eğitim hedeflerinin **%7.51'i** teacher'ın iç etiketini (`GOLD`/`DISTRACTOR`) taşıyordu; öğrenci o etiketi girdide **hiç görmediği hâlde** ezberler. #16'nın birebir tekrarı | `scrub_teacher_jargon.py` → `raft_scrubbed/`; teacher **öğrencinin gördüğü etiket uzayında** promptlanır | #39 Bulgu 4 |
| 4.3 | **Truncation** | `max_seq_len` yetmezse örnek "tüm label −100" diye düşer ya da cevap **ortadan kesilir** — *yarım cevap öğretimi*, uyarısız. Suçlu cevap değil **kaynak bloğu** | `measure_token_budget.py`; **etkilenen >%1 ise koşma** | 12B #15 |
| 4.4 | **Başka modelin hataları** | `orpo_abstain/`'in `rejected` tarafı **12B'nin fabrikasyonları**. Olduğu gibi kullanmak yeni modele **başka bir modelin hatalarını** öğretir | yeni base ile **yeniden hasat** (`gen_v3_rejected.py`) | TASARIM §4.1 |
| 4.5 | **Topik-skew** | Seed dosyası kanuna göre **sıralı**ydı; yarıda kesilen üretim "rastgele örnek" değil **sistematik kapsama deliği** verdi | üretim öncesi shuffle + kapsama kontrolü | 12B #14 |
| 4.6 | **Veri şeması sessizce yanlış** | Pack `source` alanını gold metni sanıyordu — o alan **provenance etiketiydi**. Hata vermedi; 16 çağrılık smoke yakaladı | her veri üretiminden sonra **küçük smoke** | 12B #14 |

## 5. Artefakt / araç

| # | tuzak | ne olur | korunma | kaynak |
| :-- | :--- | :--- | :--- | :-- |
| 5.1 | **Kuantizasyon yarıda kesilir** | Dosya "var" görünür — bir GGUF 666 tensörün 4'ünde kesilmişti, **70 MB** diskte duruyordu | `setup_llamacpp.sh` <100 MB'da durur; boyutu **base ile karşılaştır** | sprint1 CP0 |
| 5.2 | **Merge sessizce eksik** | Adaptörün bir kısmı base'de karşılık bulamazsa dosya yine yazılır ve *"merge oldu"* görünür | `merge_lora.py` **uygulanan/toplam** eşitliğini assert eder (224/224) | #41 §2 |
| 5.3 | **Merge doğrulanmaz** | Yanlış merge normal boyutta, normal görünümlü bir model üretir | iki kapı: `‖merged − base‖_F ≈ ‖τ‖` **ve** GGUF **base ile aynı boyutta** | #41 §2 |
| 5.4 | **`set -e` mesajı yutar** | `snap=$(ls …)` gibi bir atama başarısız olunca `set -e` **mesaj basmadan** öldürür; script "sessizce" durur | başarısızlığı beklenen atamalarda `\|\| true` + açık kontrol | #41 (oturum) |
| 5.5 | **Göreli yol `cd`'den sonra** | Script içinde `cd` varsa argümandaki göreli yol **başka yere** çözülür | argümanları **başta mutlaklaştır** | #41 (oturum) |
| 5.6 | **`.env` emekli base'i gösterir** | `BASE_MODEL` eski hattı işaret ediyordu — ADR-0026'nın tam uyardığı tuzak. Koşular script'ler `--model` zorunlu kıldığı için kurtuldu (**şans, tasarım değil**) | base **parametre**, varsayılan **yok**, tanımsızsa erken patla | #39 Bulgu 5 |
| 5.7 | **Ara f16 GGUF diski doldurur** | 8-22 GiB; `KEEP_F16=1` unutulursa birikir | varsayılan sil; scratchpad **oturum-kapsamlı**, kalıcı iş `~/code/` altına | sprint1 CP0 |
| 5.8 | **WSL2 belleği host'un yarısı** | Host 32 GB olsa da VM **15.9 GB** görür (`.wslconfig`'de `memory=` yoksa) | bellek hesabını **`free`'den** yap, host'tan değil | #41 §2 |

---

## Kullanım — koşu öncesi kısa liste

**Eval koşusu:** `--data` açık mı · `--thinking off` var mı · `--max-chunk-chars 900` · n/seed CP2 ile
aynı mı · taşıyıcı CP2 ile aynı mı (GGUF/llama-server) · künyede hepsi görünüyor mu.

**Eğitim koşusu:** `--target-modules` verildi mi · turn işareti assert'i tetiklendi mi · `fla-core`
kurulu mu · `--data` konteyner yolu mu · `spawn()` + `--detach` · rejim TASARIM §4.1.1 ile eşleşiyor mu.

**Skorlama:** `.env` yüklü mü · gateway pinli mi · red-regex bu **aile** için kalibre mi · A1
cevaplanan-only mu · coverage yanında mı · payda yazıldı mı.

**Artefakt:** merge 224/224 mü · `‖merged − base‖ ≈ ‖τ‖` mi · GGUF boyutu base ile aynı mı ·
kuantizasyon bitti mi.
