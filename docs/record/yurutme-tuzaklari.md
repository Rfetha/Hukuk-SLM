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
| 1.8 | **`--thinking on` + bütçe = "artırırsan düzelir" sanısı** | Base M1/M2/M5'te `</think>`'i **hiç** kapatmıyor: kesilme değil **sonlanmama**. Aynı muhakeme satırı 219 kez tekrarlanıyor; 4096 → 32768 (**8×**) hiçbir şey değiştirmedi, Q8_0'da da aynı, `temp 0.6` yarısını kurtardı. Bütçe artırmak **saatleri yakar ve yine "geçersiz koşu" yazar** | düşünen model + belirsizlik içeren istem = **`--think-budget N` zorunlu** (zorunlu kapatma). Bütçe **ön-kayıtlı** seçilir, künyeye ve maliyet muhasebesine yazılır | #42 |
| 1.10 | **n=3 smoke, n=470'i temsil eder sanılır** | CP0 n=36'da *"base M4/M3'te kendi kapatıyor, `τ_g` 35/36 duruyor"* dedi; n=470'te M4 **76/80 zorla**, M3 **60/80** ve `τ_g`'nin kazancı **yalnız kendi istem ailesinde**. Smoke hata vermez, sadece **yanlış genelleme** kurdurur | smoke = *"boru hattı çalışıyor mu"*, **asla** *"davranış şu"*. Davranış iddiası tam n bekler | #43 Bulgu 2·4 |
| 1.9 | **900-kar klip numaralı listeyi ortadan keser** | Kaynak bloğu `"…Suçlar (madde 309, 310, 311,"` diye biterse model *"birebir alıntıla"* talimatıyla **sayıyı saymayı sürdürüyor**: `…1682, 1683, 1684` — 8 örnekte 1'i. Hata yok, cevap dolu, **çöp**. Yalnız düşünce açıkken gözlendi (thinking-off Sprint 1'de 0/80) | `finish_reason='length'` sayacı bunu yakalar — **kesik oranı okunmadan sonuç okunmaz**; satır-bazlı döngü metriği bunu KAÇIRIR (2 satır, 8625 kar) | #42 |

## 2. Hakem / skorlama

| # | tuzak | ne olur | korunma | kaynak |
| :-- | :--- | :--- | :--- | :-- |
| 2.1 | **Red-regex kalibre edilmemiş** | Base'in baskın red kalıbı `bulunmuyor`u görmüyordu → kalibrasyonsuz **M3 0.000** (gerçek 1.000), **M2b 0.662** (gerçek 0.987) | her **aile** için ayrı kalibrasyon; 15/15 ileri + 2/2 geri elle | #39 Bulgu 3 |
| 2.2 | **Rakip ailesi kalibre edilmemiş** | Rakibin reddi **eksik sayılır** → sapma **bizim lehimize**. TASARIM §3.4: kalibrasyonsuz hiçbir abstention sayısı raporlanmaz | `compare_runs.py` kalibre edilmemiş etiketi **⚠️ ile işaretler** | sprint1 CP7 |
| 2.3 | **A1 yerine ham ortalama** | Çekinme faith=0 alıp ortalamayı çeker: 12B'de ham 0.737 vs gerçek **0.904**; bu hatta base ALL 0.8385 vs **A1 0.973** | A1 **cevaplanan-only** (`rescore_answered.py`) + **coverage yanında** | ADR-0011 · #39 |
| 2.4 | **Coverage değişince A1 kıyası** | Model daha çok cevaplamaya başlayınca A1 kıyası elmayla-armut olur (base kendi seçtiği kolay dilimde ölçülür) | **eşleştirilmiş alt küme**: ikisinin de cevapladığı sorularda A1 | #41 §4.2 |
| 2.5 | **`rejection_exact` ↔ `rejection_rate` karıştırılır** | regex-red ile LLM-red farklı şey ölçer; hakem "reddedip sonra açıklayan" cevabı ABSTAIN sayar, regex saymaz | ikisi **birlikte** raporlanır | #39 CP2 |
| 2.6 | **Payda kayar** | `valid_traps` modele göre değişir (M2b: 75 / 67 / 80) — oran aynı paydada değil | ~~oran **payda ile** yazılır~~ → **YETERSİZ, bkz. 2.14**: paydayı yazmak kirliliği görünür kılar, **gidermez** | #41 §3 · **#45** |
| 2.14 | **Filtre etiketi özne başına yeniden yargılanır** | 2.6'nın kökü. `valid_trap` (tuzak geçerli mi) hakemden **öznenin cevabıyla aynı çağrıda** isteniyor → hakem cevaba **çapalanıyor** ve etiket kalemin değil öznenin özelliği oluyor. Ölçüldü: aynı 80 M3 kaleminde 54/56/**39**, **19 kalemde** etiket özneye göre değişiyor; cevabı görmek `gpt-4o-mini`'yi **22,3p** kaydırıyor (`gpt-4o` 8,4p). Sapma **yön değiştirir** (M2b aleyhimize ~7p, M3 lehimize ~12p) → ön-kayıtlı kapı için gürültünün en kötü türü. Hiçbir yerde hata vermez | tuzak geçerliliği **kalem düzeyinde, bir kez, cevaba KÖR** hesaplanıp önbelleğe alınır; özne skorlaması onu **okur**, yeniden sormaz. Kontrol: aynı id kümesinde özneler arası `len({valid_trap})==1` | **#45** |
| 2.15 | **Tanım gereği bilinen etiketi hakeme sormak** | M3'te bağlam **boş** (`sources_block="(İlgili kaynak bulunamadı.)"`) → "kaynak cevaplıyor mu" sorusunun cevabı 80/80 **hayır**. Hakeme sorulduğu için 39-56 çıktı: gereksiz gürültü **ve** para | mod tanımından çıkan etiket **sabitlenir**, hakeme gitmez | **#45** |
| 2.7 | **Sağlayıcı pinlenmemiş** | Aynı model kimliği farklı servis yığınında (farklı kuantizasyon) koşar → sayılar kıyaslanamaz, **hata vermez** | özet JSON'da `judge_providers` **tek eleman**; `compare_runs.py` yığın uyuşmazlığında **tabloyu basmaz** | ADR-0029 |
| 2.8 | **Hakem gürültüsü sinyal sanılır** | Aynı girdi + aynı hakem, iki koşu: `faith_macro` ±0.005 ama **`cit_precision` ±0.044** | tavan dışı `cit_precision`'da 0.04'lük fark **sinyal değildir**; `runs=1` künyeye yazılır | #41 §6 |
| 2.9 | **Regex kopyası çoğalır** | `rescore_answered.py` kalibre edilmemiş bir regex **kopyası** taşıyordu → tüm A1/coverage sayıları yanlıştı | tek kaynaktan import (`score_abstention.REJECT_RE`) | CP7 kaydı |
| 2.10 | **Eğitim biçimi hakemde cezalanır** | RAFT şablonunun 1. adımı (*"ilgili kaynak KAYNAK 3'tür, diğerleri farklı konuda"*) kaynak **hakkında** cümle → hakem `NOT_IN_SOURCE` der. `τ_g`'nin desteksiz iddialarının **%58'i** bu | 🔴 **AÇIK** — `open_questions.md` §13.8, `τ_a`'dan önce karara bağlanmalı | #41 §4.3 |
| 2.12 | **Red-regex MOD'a göre yanlış** | Kör modun sistem istemi feragat cümlesini (*"bir avukata danışın"*) **emrediyor**; regex onu red sayınca **dolu cevaplar çekinme oldu** → M5 coverage düşük, ezber kütlesi **3.4× küçük** ölçüldü. M5 anti-hedef olduğu için sapma **bizim lehimize**. base 54/56 · Gemini 58/62 · `τ_g` 50/51 "red" yalnızca o cümleydi | kalibrasyon **aile × MOD** — `exact_reject(cevap, mode)`, `mode` zorunlu (ADR-0044) | #43 Bulgu 1 |
| 2.13 | **Tek eksende ölçüp "iyileşti" demek** | M2'de doğru davranış reddetmek → *"her şeye reddet"* diyen model **1.0** alır. Kaynak-yeterliliği önsözü M2'yi 0.968'e çıkardı, M1 kütlesini **28.2**'ye düşürdü (aşırı-red 0.6875) | çekinme ekseninde her kazanç **karşı eksende** (M1 coverage/kütle) doğrulanır | #43 Bulgu 5-b |
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
| 4.7 | **Kabul ölçütü ≠ raporlanan metrik** | ORPO `rejected` hasadının kabul ölçütü **regex** (`exact_reject` red saymıyor), ama M2/M2b tablolarının ve ARA KAPI'nın okuduğu sayı **LLM hakemi**. *"Reddedip sonra açıklayan"* cevabı regex fabrikasyon sanıyor → havuza **doğru çekinme örnekleri** `rejected` olarak giriyor → ORPO modele **çekinmeyi cezalandırmayı** öğretir. Ölçüldü: regex %30 kabul dedi, hakem geçerli tuzaklarda **%71'ine ABSTAIN** dedi; gerçek verim **%5**. Eğitim koşar, loss düşer, hiçbir yerde hata yok | veri hasadının kabul ölçütü, o veriyle eğitilen kolun **raporlanacağı metrikle aynı** olmalı; regex ile LLM arasındaki fark (CP0.9: 0.61 ↔ 0.814) **ölçülüp** ölçüte bağlanır. Kabul edilen adaylar `cp2_audit.py` + `score_abstention.py` ile **denetlenir** | **#44** |
| 4.8 | **Tuzak havuzunun kendisi geçersiz** | ⚠️ **BÜYÜKLÜĞÜ ÇÜRÜDÜ (#45)** — "%42" zayıf hakemin **çapalanma artefaktıydı** (bkz. 2.14); güçlü hakem (`gpt-4o`) aynı 36 kalemde **%8,3–16,7** diyor. Olgu duruyor (havuz tamamen temiz değil), **oran** durmuyor. Bu ölçüte dayanan ön-eleme filtresi de **net zararlı** çıktı (kestiği 7 kalemin 6'sı geçerli tuzak) → koşulmadı | tuzak geçerliliği (`valid_traps`) hasat huninin **ayrı bir satırı** olarak raporlanır; havuz kalitesi eğitim öncesi ölçülür — **ama ölçen hakem cevaba kör olmalı ve gücü rapor edilmeli** | #44 · **#45** |

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
| 5.9 | **`pgrep`/`pkill -f` kendini yakalar** | `pkill -f "llama-server -m models/..."` kendi komut satırıyla eşleşip **kabuğu öldürdü** (exit 144); `until ! pgrep -f "groundedness\|..."` döngüsü kendini görüp **asla çıkmadı** (13 dk boşa döndü) | desende köşeli parantez: `pkill -f "[l]lama-server"` | #43 (oturum) |
| 5.8 | **WSL2 belleği host'un yarısı** | Host 32 GB olsa da VM **15.9 GB** görür (`.wslconfig`'de `memory=` yoksa) | bellek hesabını **`free`'den** yap, host'tan değil | #41 §2 |

## 6. Bulut / orkestrasyon

| # | tuzak | ne olur | korunma | kaynak |
| :-- | :--- | :--- | :--- | :-- |
| 6.1 | **`modal run` efemer app + `spawn()` = iş HİÇ koşmaz** | Terminal *"✓ App completed"* yazar, log yalnızca *"Stopping app — local entrypoint completed"* içerir. **Hiçbir iş başlamamıştır, hata da yoktur.** Yerel giriş noktası dönünce efemer app kapanır ve kuyruktaki `spawn()` işi onunla ölür. Ders A4.1 zaten `spawn() + --detach` diyordu, bayrak düşürülmüştü | **`modal run --detach`** zorunlu. Ve *"SPAWNED ✓"* mesajı işin koştuğunu **KANITLAMAZ** — `modal volume ls <out>` ile çıktının gerçekten yazıldığını doğrula | **#47** |
| 6.2 | **Veri kapısı model yüklemeden SONRA** | Yol/format hatası, model A100'e yüklendikten sonra patlar → boşa GPU dakikası. `train_orpo.py --data` bir **dizin** bekliyordu (`train.jsonl` + `validation.jsonl`); dosya yolu verilince `load_dataset` `<dosya>/train.jsonl` aradı. `train_sft.py` aynı denetimi **yükleme öncesi** yapıyordu, `train_orpo.py` yapmıyordu | Her eğitim betiği girdi dosyalarını `os.path.isfile` ile **model yüklenmeden önce** doğrular. `train_orpo.py` düzeltildi | **#47** |
| 6.3 | **Bütçe defteri iki cüzdanı toplar** | `sprint2.md` *"Modal cap $42.50 · harcanan $6.57 · kalan $35.93"* diyordu; gerçek Modal kalanı **$7.27**'ydi. Defterdeki harcamaların neredeyse tamamı **OpenAI hakem** ücretiydi (GPU yereldeydi), ~$28'lik Modal harcaması ise **emekli 12B hattına** aitti ve bu defterde hiç görünmüyordu → CP4-CP5 sığmaz hâle gelmişti ve fark edilmemişti | GPU ve hakem maliyetleri **ayrı tabloda**. Modal sayısı **panelden okunur**, defterden türetilmez | **#47** (oturum) |
| 6.4 | **Hazır imajın `ENTRYPOINT`'i** | llama.cpp `ghcr.io/ggml-org/llama.cpp:server-cuda` imajının entrypoint'i `/app/llama-server`. Temizlenmezse çalıştırıcının `python …` komutu **ona argüman olur** → `error: invalid argument: python`. Belirti: konteyner **saniyeler içinde** ölür, GPU logu hiç açılmaz — ve sebebi kodda değil imajda | üçüncü-taraf imaj kullanırken `.entrypoint([])` ile **açıkça temizle**; ilk koşuda konteyner logunun ilk 5 satırını gözle oku | **#48** |
| 6.5 | **Lock dosyası iş türüne göredir** | `requirements.lock.txt` **eğitim** için üretildi; hasat/eval betiklerinin bağımlılığı (`openai`) içinde **yok**. Aynı imajı yeni bir iş türü için kullanınca `ModuleNotFoundError` konteynerde, **GPU ayrıldıktan sonra** patlar — para yanmış olur | yeni **iş türü** = bağımlılıkları imaj katmanında **açıkça** ekle (`pip_install("openai==2.41.0")`, sürüm yerelle eşitlenir). Lock'un adı hangi işe ait olduğunu söylemiyorsa, söyletecek bir yorum satırı koy | **#48** |
| 6.6 | **Öbekli eş zamanlı istemci slotları boş bekletir** | `pool.map` / chunked desende **her öbek en yavaş kalemini bekler**. Hata vermez, çıktı doğrudur — sadece **%30 daha pahalıdır**. Ölçüldü: slot doluluğu **%70** (10.220 slot-s iş / 14.496 slot-s kapasite); sürekli beslemeye (`FIRST_COMPLETED` + yeniden doldur) geçince **1,84×** hızlanma (3,65 → 1,98 s/üretim) | kalemler **bağımsızsa bariyer kullanma**. Gönderilen istek/sıra/seed değişmediği sürece bu **yalnız zamanlama** değişikliğidir, veriyi etkilemez | **#48** |
| 6.7 | **`gpu="A100"` takma adı iki farklı kart verir** | Modal'ın `gpu="A100"` etiketi hem **40GB** hem **80GB** kart verebiliyor; bant genişliği oranı **1,55 ↔ 2,03 TB/s = 1,31×**. Künyeye gerçek kart yazılmazsa iki koşu arasındaki hız farkı **yanlış sebebe** yazılır. Fiilen ısırdı: `-np 32` ↔ `-np 64` karşılaştırmasında gözlenen fark **1,32×** çıktı ve *"slot artışı işe yaramadı"* ile *"np64 yavaş karta düştü"* **ayrılamadı** | künyeye `nvidia-smi`'den okunan **gerçek kart adı** (`gpu_gercek`) yazılır — etiket değil. Karşılaştırma iki koşunun `gpu_gercek`'i **eşit değilse** kurulmaz | **#48** |
| 6.8 | **Kümülatif ortalamayı erken okuyup karar verme** | Yüksek eş zamanlılıkta **ilk dalga inmeden** `geçen_süre ÷ tamamlanan` şişik görünür: `-np 64` koşusu **75. üretimde 4,96 s/üretim** gösterdi, **2,93**'te kapandı. Ara çıktıya bakıp koşu iptal etmek, sağlıklı bir koşuyu öldürür ve parayı **iki kez** yakar | ön-kayıtlı verim kapıları `gate_after_s` ile **gecikmeli** bakar (ADR-0047 m.3); kapı `limit` kontrolünden **önce** değerlendirilir, hiç değerlendirilmediyse künyeye `değerlendirilmedi` yazılır — *"geçildi"* damgası **hak edilmeden basılmaz** | **#48** |
| 6.9 | **Ön-kayıtlı bir kapıyı kümülatif ortalamayla beslemek** | **6.8'in kod tarafındaki kardeşi** — orada *insan* ara çıktıya bakıp koşuyu iptal ediyordu, burada *kapı* aynı yanlı sayıyla **otomatik** karar veriyor. Yüksek eş zamanlılıkta `geçen_süre ÷ tamamlanan`, `concurrency` kadar isteğin birlikte indiği **açılış geçicisini her kaleme paylaştırır** → erken okumada hız **sistematik olarak kötü** görünür ve kapı, eşiği **geçecek** bir koşuyu durdurur. Fiilen ısırdı: gerçek kararlı hızı ~**2,4 s/üretim** olan m2 koşusu **600. saniyede 2,97** okunup durduruldu (eşik **2,88**) — **aynı koşu 73 sn sonra, 673. saniyede zaten 2,89'daydı**. İki tip de durduruldu, ~$1,2 GPU yandı; hiçbir yerde hata yok, künyeye düzgün bir 🔴 damga bile düştü | kapı **kararlı hızı** ölçsün: boru hattı `concurrency` kalemle **dolduktan sonraki** süre ÷ o andan sonraki üretim (`cp2_harvest.py::kararli_hiz`). Kümülatif alan **silinmez**, yanına yazılır (eski koşularla karşılaştırılabilirlik). **Kural: sonucu gördükten sonra EŞİK değil ALET düzeltilir** — ön-kayıtlı olan *büyüklük*tür, onu kestiren tahmin edici değil; ayrım raporda korunmazsa dışarıdan **gevşetme** görünür (ADR-0050) | **#48** · [ADR-0050](../adr/0050-verim-kapisi-tahmin-edici-duzeltmesi.md) |
| 6.10 | **İki detached iş aynı çıktı dizinine yazar** | `--detach` işi terminalden **kopar**; ikinci kez başlatmak birinciyi durdurmaz, **yanına** koşar. İkisi de aynı `--out`'a yazınca: (a) GPU maliyeti **iki katı**, (b) havuz sırası seed'e bağlı ve deterministik olduğu için ikisi büyük ölçüde **aynı kalemleri** üretir → çıktıda **yinelenen id**, (c) `KUNYE.json`'u **son biten iş yeniden yazar** → künyedeki sayaçlar dosyanın içeriğini tarif etmez, (d) yanlış olanı durdurunca yazma ortasında kesilir → **yarım son satır**. Devam mekanizması (`load_done`) korumaz: her iş **kendi başlangıcındaki** id kümesini okur, sonra birbirini görmez. Fiilen ısırdı (16:47 ↔ 16:52, ikisi de `/cp2c-64`) | başlatmadan **önce** `modal app list \| grep <fn>` — canlı iş varsa yeni koşu **başlatılmaz**. Çakışma olduysa **ilerlemesi fazla olanı** tut (başlangıç saatini değil), diğerini `modal app stop -y`. Çıktı kabul/eğitime girmeden **id bazlı tekilleştirme + yarım son satır onarımı** zorunlu (`scripts/cp2c_birlestir.py`); **ortadaki** bozuk satır onarılmaz, çökertir — o bilinen kesilme kalıbı değildir | **#48** §5 |
| 6.11 | **Devam mekanizması yalnız KABUL edilenleri hatırlar** | Hasat/üretim betiği çıktı dosyasına **kabul edilen** kalemi yazar, elenenler yalnız sayaçta kalır. Sonuç: bir **ek tur** iki yoldan da sessizce boşa gider — *taze dizinde* devam kaydı boş olduğu için deterministik havuz sırası **0'dan** başlar ve **aynı kalemler** yeniden üretilir; *aynı dizinde* ise devam kaydı elenenleri bilmediği için üretimlerin ~%69'u **zaten denenip elenmiş** kalemlere gider. İkisinde de hata yok, GPU yanar, sonra tekilleştirme havuzu küçültür ve azlık **yanlış sebebe** yazılır. Fiilen yakalandı: `/cp2c`'nin 68 kabulü havuz pozisyonu **1-229** arasında — sıra baştan yürüyor | devam kaydı *"denendi"*yi ifade edemiyorsa ek tur **sıra atlamayla** koşulur: `cp2_harvest.py --skip-first N`, N = önceki turun künyesindeki `denenen`. Taze dizin (provenans) + künyeye `skip_first`. Havuz biterse **üretim başlamadan** çöker. Genel kural: *"kaldığın yeri"* saklamayan bir devam mekanizması, devam ettiğini **sanmana** izin verir | **#48** §9 |

---

## Kullanım — koşu öncesi kısa liste

**Eval koşusu:** `--data` açık mı · **`--thinking on` + `--think-budget 1024` + `--max-new-tokens 512`**
(ADR-0043; thinking-off artık canlı rejim DEĞİL) · `--max-chunk-chars 900` · n/seed CP2 ile aynı mı ·
taşıyıcı CP2 ile aynı mı (GGUF/llama-server) · **koşu klasörü + `KUNYE.json`** yazıldı mı ·
kesik oranı %5'in altında mı.

**Eğitim koşusu:** `--target-modules` verildi mi · turn işareti assert'i tetiklendi mi · `fla-core`
kurulu mu · `--data` konteyner yolu mu · `spawn()` + `--detach` · rejim TASARIM §4.1.1 ile eşleşiyor mu.

**Skorlama:** `.env` yüklü mü · gateway pinli mi · red-regex bu **aile VE bu mod** için kalibre mi
(ADR-0044) · A1 cevaplanan-only mu · coverage yanında mı · payda yazıldı mı · çekinme kazancı
**karşı eksende** doğrulandı mı.

**Artefakt:** merge 224/224 mü · `‖merged − base‖ ≈ ‖τ‖` mi · GGUF boyutu base ile aynı mı ·
kuantizasyon bitti mi.
