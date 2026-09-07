# Faz 0 — ölçüm zinciri (uygulama planı)

> **Ajan işçiler için:** GEREKLİ ALT-BECERİ: `superpowers:executing-plans` ya da
> `superpowers:subagent-driven-development`. Adımlar `- [ ]` kutucuklu.
> ⛔ **Kutucuk yalnız `verify:` çıktısı GERÇEKTEN alındıktan sonra işaretlenir.**

**Amaç:** `PRODUCT.md`'nin manşet sayısını çivilemek — yeni varsayılan (önsözsüz) rejimin
sayısını gözle doğrulanmış hâle getirmek, rakip çıpalarını aynı rejimde ölçmek ve `v1.0`
kapısının eşiğini eğitimden **önce** ön-kayıtlamak.

**Mimari:** Zincir, sırası bağlayıcı. Erişim (F0.1) en başta, çünkü eşit sınavın kanıtı
*"`recall@10` bütün öznelerde birebir aynı"* — indeksi sonradan oynatmak rakip koşularını
çöpe atar (~$1,35). Her koşu kendi klasörüne + `KUNYE.json`'una yazar.

**Yığın:** llama.cpp (`llama-server`, Q4_K_M, KV q8_0) · `scripts/cp0_thinking_gen.sh` (canlı
koşucu; llama-server'ı açar, künyeyi basar, kesiklik kapısını uygular) ·
`scripts/gen_eval_grounded.py` (tek üretim gövdesi) · `groundedness.py` · `harness_tablo.py` ·
`recall_olc.py` · `measure_vram_stack.py` · hakem `openai/gpt-4o-mini` @ openrouter.

## Global kısıtlar — her görev bunları örtük olarak taşır

- **Python:** `source ~/code/global_venv/bin/activate` **aynı komut içinde**.
- **Sırlar:** `set -a && . ./.env && set +a` · üretim OpenRouter'a giderken `OPENAI_API_KEY="$OPENROUTER_API_KEY"`.
- **Rejim değişmezleri (uyuşmazlık hata VERMEZ, kıyası GEÇERSİZ kılar):**
  `--seed 3407` · `--max-chunk-chars 900` · `--thinking on` · `--think-budget 1024` ·
  `--max-new-tokens 512` · `--n 80` · veri `data/eval/dev/core_hard.jsonl` ·
  indeks `data/index/mevzuat_bge_m3_s2` · `--harness-k 10`.
- **Yeni varsayılan rejim ÖNSÖZSÜZ:** `EXTRA_ARGS` **boş** bırakılır. Künyedeki
  `ekstra : <yok>` satırı bunun kanıtıdır — bayrağın düştüğü tuzak sınıfı budur.
- **Hakem yığını:** `--judge-model openai/gpt-4o-mini`, `LLM_PROVIDER_ORDER=OpenAI`,
  aile dışlaması (Google özneyi OpenAI hakem notlar).
- **Donmuş TEST'e dokunulmaz:** her şey `data/eval/dev/`. `data/eval/canon/` **açılmaz**.
- **Her koşudan önce** `docs/record/yurutme-tuzaklari.md` okunur.
- **Bütçe:** Modal $29,19 · OpenRouter $10,26. Bu plan **~$1,65** harcar.
  🚨 **DÜZELTME 2026-09-07 — bütçe hatırlanmıştı, ölçülmemişti.** Devir notu *"OpenRouter
  ~$8,88"* diyordu ($10,26 − bugünkü $1,38). **Ölçülen gerçek bakiye: $6,60**
  (`/api/v1/credits`: `total_credits` 20 − `total_usage` 13,397) — **$2,28 fark**, kaynağı
  bu planın dışındaki harcamalar. ⇒ Aşama 2'nin T1 tahmini (~$3-5) bakiyenin **yarısından
  fazlası**; sıralama kararı bu sayıyla yeniden okunmalı. **Ders:** para da bir sayıdır ve
  bu repoda sayı hatırlanmaz, **kaynaklanır**.
- ⭐ **Gözle okuma bir kapıdır** — sayısal kapı bozuk ölçümü bir kez geçirdi.
- 🔌 **PİLDE ÖLÇÜM KOŞMA — sayısı ölçüldü (2026-09-07).** `cp0_thinking_gen.sh` künyeye
  `güç : PİLDE ⚠️` basıyor ve bu **boş bir uyarı değil**: pilde GPU **P5 · SM clock 180 MHz**'e
  kısılıyor (şarjda ~2.000 MHz), üretim **8,4 t/s** (şarjda ~42 t/s) ⇒ **~5-11× yavaş**.
  Ölçülmüş etki: M5'in 80 kalemi **şarjda ~57 dk, pilde ~4,8 saat**.
  ⚠️ Sayı DEĞİŞMEZ (`temperature=0`, seed 3407) — değişen yalnız süre; ama saatlerce süren bir
  koşu, teşhisi de imkânsızlaştırıyor (*"takıldı mı yavaş mı"* ayrımı yapılamıyor).
  ⭐ Ayrıca ölçüldü: **M5'te kalem başına İKİ üretim** gerekiyor — model kör modda `</think>`'i
  bütçe içinde kapatmıyor, zorla-kapatma yolu devreye giriyor (research_log #42'nin kalıntısı).
  M5 kalem başına ~1800 token, diğer modların **iki katı**.
- 🚨 **Uzun koşuyu harness'ın arka plan görevi olarak başlatma.** Ölçüldü 2026-09-06: koşunun
  tepe kullanımı **7,2 GB / 15,9 GB** (llama-server 1,65 + python 3,65) ve `available` **9 GB**
  iken, Linux kalanı sayfa önbelleğine aldığı için **`free` 0'a düşüyor**; harness'ın bellek
  gözcüsü `free`'ye bakıp görevi **öldürdü** (0/80'de). Gerçek bellek sıkıntısı YOKTU.
  ⇒ Uzun koşular `setsid nohup … &` ile **ayrık** başlatılır, `Monitor` ile beklenir.
  ⚠️ WSL2'ye 15,9 GB verilmiş (makinede 32 GB var, `.wslconfig`'de bellek ayarı yok).
- 🚨 **ANTİ-HEDEF ÇIPASI BOŞTU — 2026-09-07'de yakalandı.** Kapı maddesi *"M5 ≤ **bugünkü**"*
  yazıyordu, ama `tgta_v1`'in M5'i **hiçbir birimde hiç ölçülmemişti** (mevcut M5 sayıları
  `base_th` · `gem_th` · `tg_v1_th`; merge öznesi yok). *"Bugünkü"* diye bir sayı yoktu —
  madde kendi kendine referans veriyordu ve **hiçbir hüküm üretemezdi**.
  ⇒ Çıpa [ADR-0039](../../adr/0039-kapi-6-parametrik-sizinti.md) §2'den okundu: **çıpa BASE'dir,
  rakip değil** (*"modeli aldığımız noktadan kötüye götürmemeliyiz"*; rakip çıpası **reddedilmişti**),
  ve **üç sayı birden** raporlanır: `coverage` · `A1` · `ezber kütlesi = coverage × A1`.
  ⇒ Eski `base_th` (v1 soru seti + 1024 bütçe) **kıyaslanamaz birimdedir**; base M5 **v2 biriminde
  yeniden koşuldu** (ADR-0050: *alet değişirse eşik aynı formülle yeni birimde türetilir*).
  **Tuzak sınıfı:** kapı maddesi ön-kayıtlıydı ama **çıpası yoktu** — sayısal kapı, ölçülemez
  olduğunu kendisi söylemez; ancak koşmadan önce *"bu sayıyı neyle kıyaslayacağım"* diye
  sorulunca ortaya çıkar.

---

### Görev 1 · F0.1 — erişim teşhisi (`recall@10` neyi kaçırıyor)

**Dosyalar:** Create: `outputs/eval/f01-erisim/recall_taban.json` ·
`outputs/eval/f01-erisim/KACIRILAN_10.md` · Read: `scripts/recall_olc.py` · `scripts/retriever.py`

> 🚨 **KAPANIŞ DENETİMİ 2026-09-07: `recall_taban.json` HİÇ OLUŞMADI.** Adım 1-2 `[x]`
> işaretliydi ve **ölçüm gerçekten koştu** (sayılar `KACIRILAN_10.md` ve
> `f01b/SONUC_recall_v1_v2.md`'de, manşet `0,9500` ise `f02-biz-onsozsuz/KUNYE.json`'da) —
> ama **ham JSON hiçbir yere yazılmadı**: `find outputs -newermt 2026-09-06 -name "recall_*.json"`
> **boş** döndü. Klasördeki tek dosya `KACIRILAN_10.md`.
> **Sebebi tuzağın kendisi:** `--out` bir dizindir; yanlış yol verilen koşunun çıktısı
> temizlik sırasında kayboldu ve kimse fark etmedi, çünkü **sayı `.md`'ye elle geçirilmişti**.
> ⇒ Bu, *"sayı hatırlanmaz, **kaynaklanır**"* kuralının bu turdaki tek ihlali.
> **Kapatma:** ölçüm mevcut rejimde ($0, GPU ~15 dk) bir kez daha koşulup dosya **gerçekten**
> üretilir. **Ders:** `verify:` satırı *"dosya oluştu"* diyorsa, kutucuk işaretlenmeden önce
> **dosyanın varlığı sınanmalı** — bu turda 39 kutucuğun 38'inde sınandı, birinde sınanmadı.

**Arayüz:** Üretir → `KACIRILAN_10.md` (kaçırılan kalemlerin sınıflaması) ve bir **karar önerisi**.
⛔ Bu görev indeksi **değiştirmez**; değişiklik ADR gerektirir (Görev 1b).

- [x] **Adım 1: Taban ölçümü — üç yöntem ayrı ayrı**

```bash
source ~/code/global_venv/bin/activate && \
mkdir -p outputs/eval/f01-erisim && \
python scripts/recall_olc.py --help
```
`verify:` `--yontem` / `--kapsam` / `--model` / `--out` / `--cihaz` bayraklarının gerçek
değer kümesi görülür. **Bayrak adlarını buradan al, tahmin etme.**

- [x] **Adım 2: `recall@10`'u yöntem başına bas**

⚠️ **`--out` bir DİZİNDİR, dosya değil** (`recall_olc.py`:134 `os.makedirs(a.out)` · :204
`os.path.join(a.out, f"recall_{etiket}.json")`). Dosya yolu verilirse o adda bir **klasör**
açılır ve çıktı içine gömülür — hata vermez, sessizce yanlış yere yazar (2026-09-06'da olan
budur).

⚠️ **`--cihaz cuda` ŞART** — `recall_olc.py` hazır indeksi kullanmaz, **korpusun tamamını her
koşuda yeniden gömer** (40.496 madde). Script kendi yorumunda ölçüsünü veriyor (:63):
**CPU ~4,1 madde/sn → koşu başına ≈2 saat 45 dk**; `hibrit` + `yogun` = **≈5,5 saat**.
Aynı yorum çareyi de veriyor: *"recall@k CİHAZDAN BAĞIMSIZ bir sayıdır; `--cihaz` yalnız
indeksleme süresini değiştirir"* — yani GPU sayıyı **değiştirmez**, yalnız hızlandırır.
⛔ GPU'nun boş olduğunu doğrula (`nvidia-smi`): llama-server açıkken bu koşu VRAM'i böler.

```bash
rm -rf outputs/eval/f01-erisim && mkdir -p outputs/eval/f01-erisim && \
source ~/code/global_venv/bin/activate && set -a && . ./.env && set +a && \
export PYTHONUNBUFFERED=1 && \
for Y in bm25 hibrit yogun; do
  python scripts/recall_olc.py --yontem "$Y" --kapsam korpus --cihaz cuda \
    --out outputs/eval/f01-erisim || echo "❌ $Y DURDU"
done
```
⚠️ Çıktıyı `| tail -N` ile boruya sokma — süreç bitene kadar **hiçbir şey görünmez**,
koşunun ilerliyor mu takıldı mı olduğu anlaşılmaz (2026-09-06'da olan budur).
`verify:` hibrit değer **0,875** çıkar (bugünkü çıpa; `g2-fl-harness/KUNYE.json`
`recall_at_10` ile birebir). Çıkmazsa **DUR** — çıpa kaymış, sebebi bulunmadan devam edilmez.

- [x] **Adım 3: Kaçırılan 10 kalemi GÖZLE oku ve sınıfla**

80 kalemin altın maddesi ilk 10'a girmeyenleri çıkar; her biri için: soru · altın madde ·
retriever'ın getirdiği ilk 3 · **kaçırma sebebi**. Sınıflar: (a) sorgu-madde kelime örtüşmesi
yok · (b) altın madde chunk'ı bölünmüş/tablo (borç **B9**) · (c) yürürlük/alt-madde kimliği
(S2 alanı) · (d) BM25 ↔ dense çekişmesi RRF'te yanlış tarafa düştü · (e) yer-gerçeği hatalı.
`outputs/eval/f01-erisim/KACIRILAN_10.md`'ye yaz.
`verify:` 10 kalemin **10'u** sınıflanmış; her satırda kalem id'si + sebep sınıfı var.

- [x] **Adım 4: Karar önerisi yaz, UYGULAMA**

`KACIRILAN_10.md` sonuna: sınıf dağılımı · en ucuz müdahale · **beklenen kazanç** ·
⚠️ *"indeks değişirse rakip kolları yeniden koşulmalı"* şerhi.
`verify:` öneri tek cümlelik bir eylem + tahmini `recall@10` içeriyor.

- [x] **Adım 5: Commit**

```bash
git add outputs/eval/f01-erisim/ && \
git commit -m "F0.1 erişim teşhisi — kaçırılan 10 kalem gözle sınıflandı, indeks DEĞİŞMEDİ"
```

**🚦 İNSAN KAPISI:** Adım 4'ün önerisi uygulanacak mı? Uygulanırsa ADR + Görev 1b, ve
**Görev 2 zorunlu** olur. Uygulanmazsa Görev 2 **atlanır** ve mevcut önsözsüz koşu geçerlidir.

---

### Görev 1b · soru onarımı — ✅ TAMAM *(planda yoktu, Görev 1'in bulgusundan doğdu)*

- [x] 155 sorunun tamamı belirlenebilirlik ölçütüyle tarandı → DEV 13 · TEST 2 kusurlu
- [x] 15 öneri yalnız altın madde metninden yazıldı, **insan onayına** sunuldu, onaylandı
- [x] Uygulandı: DEV+TEST `core_hard` **v2**, yedekler `.v1-2026-09-06`, `KUNYE_soru_onarimi_2026-09-06.json`
- [x] Etki ölçüldü: `recall@10` **0,8750 → 0,9375** (kaçan 10→5) · kontrol grubu çıpayı birebir üretti
- [x] ⛔ id 79 bulunuyorken kaçtı — **geri alınmadı** (eval sorusunu retriever lehine ayarlamak olurdu)

### Görev 2 · F0.2 — bizim kolun yeniden üretimi 🚨 **ZORUNLU** *(sorular değişti; eski koşullu hüküm geçersiz)*

**Dosyalar:** Create: `outputs/eval/f02-biz-onsozsuz/` (+ `KUNYE.json`)

- [x] **Adım 1: Üretim — önsözsüz, harness AÇIK**

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
set -a && . ./.env && set +a && \
OUT_DIR=outputs/eval/f02-biz-onsozsuz \
MODES="h1" HARNESS_INDEKS=data/index/mevzuat_bge_m3_s2 HARNESS_K=10 \
THINK_BUDGET=1024 MAXTOK=512 CTX=8192 \
bash scripts/cp0_thinking_gen.sh models/gguf/tgta_v1-q4_k_m.gguf tgta_v1_f02_nb
```
`verify:` künyede **`ekstra : <yok>`** (önsöz YOK — kanıt) · `harness : data/index/... · k=10` ·
`thinking : on | cevap bütçesi: 512 | düşünce bütçesi: 1024` · geçerlilik kapısı: kesik **≤%5**.

- [x] **Adım 2: Puanlama**

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
set -a && . ./.env && set +a && LLM_PROVIDER_ORDER=OpenAI \
python scripts/groundedness.py \
  --details outputs/eval/f02-biz-onsozsuz/h1_tgta_v1_f02_nb_detail.jsonl \
  --label h1_tgta_v1_f02_nb --mode data --judge-model openai/gpt-4o-mini \
  --out-dir outputs/eval/f02-biz-onsozsuz
```
`verify:` `gnd_h1_tgta_v1_f02_nb_summary.json` yazıldı, `n=80`.

- [x] **Adım 3: Harness tablosu**

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
python scripts/harness_tablo.py \
  --details outputs/eval/f02-biz-onsozsuz/h1_tgta_v1_f02_nb_detail.jsonl \
  --gnd outputs/eval/f02-biz-onsozsuz/gnd_h1_tgta_v1_f02_nb.jsonl \
  --korpus data/corpus/mevzuat_maddeler.jsonl \
  --out outputs/eval/f02-biz-onsozsuz/harness_tablo.json
```
`verify:` `recall@10` **Görev 1'in yeni değeriyle birebir** · kütle · coverage · A1 basıldı.

- [x] **Adım 4: KUNYE.json + commit** — künyede rejim değişmezleri, `sufficiency_preamble: false`,
`git_sha`, indeks sürümü. `verify:` `python -c "import json;json.load(open('outputs/eval/f02-biz-onsozsuz/KUNYE.json'))"` hata vermez.

---

### Görev 3 · F0.3 — ⭐ önsözsüz rejimin 80 kalemi GÖZLE OKUNUR

**Dosyalar:** Create: `<koşu-klasörü>/GOZLE_OKUMA_80.md` ·
Read: `outputs/eval/olcum-bi/B10_GOZLE_OKUMA_80.md` (kalıp) · `scripts/score_abstention.py`

**Neden:** Bu adım 2026-09-06'da bozuk ölçümü yakalayan tek şeydi. Önsözlü çıpada aletin
14 dediği yerde göz **8** dedi — **6 yanlış pozitif**. Önsözsüz rejim hiç okunmadı.

- [x] **Adım 1: Kalıbı oku** — `B10_GOZLE_OKUMA_80.md`'nin sütun düzenini birebir devral.
`verify:` sütunlar listelendi.

- [x] **Adım 2: 80 kalemin tamamını oku ve sınıfla**

Kaynak: geçerli koşunun `h1_*_detail.jsonl` (Görev 2 koştuysa `f02`, koşmadıysa
`outputs/eval/s2-harness-k10-etiketli/h1_tgta_v1_h1_k10_et_detail.jsonl`).
Her kalem: id · altın geldi mi · model sustu mu **(göz)** · alet ne dedi · atıf doğru mu ·
**isabetsizlik mi** (gerçek ama yanlış madde). ⛔ Örneklem değil, **80/80**.
`verify:` dosyada 80 satır var; `aşırı-red (göz)` ve `isabetsizlik (göz)` sayıları basıldı.

- [x] **Adım 3: Alet ↔ göz deltasını raporla**

Tablo: alet 5/80 ↔ göz ?/80 · yanlış pozitif · yanlış negatif. ⚠️ Delta **sıfır bile olsa**
yazılır — negatif sonuç birinci sınıftır.
`verify:` delta tablosu var; delta ≠ 0 ise **her fark eden kalem** id'siyle listelenmiş.

- [x] **Adım 4: Kütle düzeltmesi**

Göz sayıları kütleyi oynatıyorsa düzeltilmiş kütle hesaplanır ve **ikisi yan yana** yazılır
(alet kütlesi damgalanarak durur, silinmez).
`verify:` `kütle (alet)` ve `kütle (göz)` iki ayrı satır olarak var.

- [x] **Adım 5: Commit**

```bash
git add outputs/eval/*/GOZLE_OKUMA_80.md && \
git commit -m "F0.3 önsözsüz rejimin 80 kalemi GÖZLE OKUNDU — alet↔göz deltası raporlandı"
```

---

### Görev 4 · F0.4 — rakip çıpaları, ÖNSÖZSÜZ, tek kez (~$1,35)

**Dosyalar:** Create: `outputs/eval/f04-rakip-onsozsuz/` (+ `KUNYE.json` + `OZET.md`)
**Özneler:** `google/gemini-3.1-flash-lite` · `google/gemini-3.5-flash-lite` ·
**`google/gemini-3.5-flash`** *(ilk kez ölçülüyor — `v1.0` kapısının çıpası)*

- [x] **Adım 1: Üç özneyi üret — önsöz bayrağı YOK**

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
set -a && . ./.env && set +a && export OPENAI_API_KEY="$OPENROUTER_API_KEY" && \
mkdir -p outputs/eval/f04-rakip-onsozsuz && \
for M in google/gemini-3.1-flash-lite google/gemini-3.5-flash-lite google/gemini-3.5-flash; do
  TAG="$(echo "$M" | tr '/.' '__' )_nb"
  python scripts/gen_eval_grounded.py \
    --server-url https://openrouter.ai/api/v1 --server-model "$M" \
    --thinking on --max-new-tokens 512 --reasoning-budget 1024 \
    `# ⚠️ rakip tarafı --reasoning-budget kullanır, --think-budget DEĞİL: ikisi karşılıklı` \
    `# dışlayıcı; --think-budget istemci-taraflı zorunlu kapatmadır ve yalnız bizim kolda.` \
    `# Künye kanıtı: g2-fl-harness/KUNYE.json → "reasoning_budget": 1024` \
    --max-chunk-chars 900 --seed 3407 --n 80 \
    --data data/eval/dev/core_hard.jsonl \
    --harness-indeks data/index/mevzuat_bge_m3_s2 --harness-k 10 \
    --label "h1_${TAG}" --out-dir outputs/eval/f04-rakip-onsozsuz || { echo "❌ $M DURDU"; break; }
done
```
`verify:` üç `h1_*_detail.jsonl` dosyası, her biri **80 satır**. ⛔ `--sufficiency-preamble`
komutta **yok** — bizim rejimle eşleşmenin şartı bu.

- [x] **Adım 2: Eşit sınav kapısı — `recall@10` birebir aynı mı**

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
for f in outputs/eval/f04-rakip-onsozsuz/h1_*_detail.jsonl; do
  python - "$f" <<'PY'
import json,sys
rows=[json.loads(l) for l in open(sys.argv[1],encoding="utf-8") if l.strip()]
hit=sum(1 for r in rows if r.get("gold_retrieved") or r.get("altin_getirildi"))
print(f"{sys.argv[1].split('/')[-1]:<52} n={len(rows)} recall@10={hit/len(rows):.4f}")
PY
done
```
`verify:` üç öznede de **aynı** değer, ve bizim kolun değeriyle birebir. Farklıysa 🚨 **DUR** —
harness eşleşmemiş, hüküm kurulmaz (ADR-0057). ⚠️ Alan adı çıkmazsa `detail.jsonl`'in
anahtarlarını `head -1 | python -m json.tool` ile oku, tahmin etme.

- [x] **Adım 3: Puanlama — üçü de aynı hakem yığınında**

Her özne için `groundedness.py --mode data --judge-model openai/gpt-4o-mini` +
`harness_tablo.py` (Görev 2 Adım 2-3'ün birebir aynı komutları, yalnız `--label`/`--details` değişir).
`verify:` üç `harness_tablo*.json`; hakem yığını üçünde de aynı.

- [x] **Adım 4: Kesiklik damgası (tuzak 1.9 · K2)**

`finish_reason == "length"` oranı özne başına basılır. ⚠️ Rakipte muhakeme bütçesi
sağlayıcı tarafından **yok sayılıyor** (K2) — kesik >%5 ise sayı raporlanır ama
kesime duyarlı eksenler **TAVAN/TANIMSIZ** damgası taşır. Ortak kesiksiz alt kümede de hesapla.
`verify:` özne başına kesik oranı + ortak kesiksiz `n` yazıldı.

- [x] **Adım 5: `OZET.md` + `KUNYE.json` + commit**

`OZET.md`: eşit sınav kanıt tablosu · kademe tablosu (her satırda hüküm) ·
`$/cevap` **girdi+çıktı** (yalnız çıktıya bakmak sıralamayı ters gösterir — Ö7) ·
⛔ *"ölçülmedi"* olan hiçbir şeye hüküm yazılmaz.
`verify:` `git commit` sonrası `OZET.md` üç öznenin kütlesini ve **bizim kütlemizi** yan yana gösterir.

---

### Görev 5 · F0.5 — `SOURCE_CLIP` ödenir (YB3, ~$0,30)

**Dosyalar:** Modify: `scripts/score_abstention.py` çağrısındaki `SOURCE_CLIP` ·
Create: `outputs/eval/f05-source-clip/`

**Neden:** `k`'nın **çekinme** ekseni bugün **TANIMSIZ** — kör payda hakemi `k=10`'da
kaynakların **%57'sini** görüyor (`SOURCE_CLIP=3500`), `k=4`'te %100'ünü.

- [x] **Adım 1: Bugünkü `SOURCE_CLIP` değerini ve nerede uygulandığını bul**

```bash
cd /home/ersoy/code/Hukuk-SLM && grep -rn "SOURCE_CLIP" scripts/ | head
```
`verify:` değer ve uygulandığı satır görülür.

- [x] **Adım 2: Kırpmasız kör payda ile yeniden puanla**

`score_abstention.py`'nin gerçek bayrakları: `--details` · `--label` · `--out-dir` ·
`--judge-model` · `--source-field` · `--pay-kaynagi` · `--payda-kaynagi` ·
`--gecerlilik-hakemi` · `--gecerlilik-onbellek`. Adım 1'de bulunan `SOURCE_CLIP` kırpması
kaldırılır (kod sabitiyse **ortam değişkenine** çıkarılır, varsayılan bugünkü değer kalır —
davranış değişmeden ölçüm mümkün olsun). Koşu `k=10` kolunda, **aynı hakem yığını**
(`openai/gpt-4o-mini`, `LLM_PROVIDER_ORDER=OpenAI`) ve **aynı önbellek anahtarı** (ADR-0060:
anahtar hakem istemine eşitlendi — istem değişirse önbellek ıskalar, sessizce eski sayı gelmez).
⛔ Çıktı **yeni klasöre** (`outputs/eval/f05-source-clip/`), eski özet dosyasının üzerine yazılmaz.
`verify:` yeni `valid_traps` paydası basıldı ve **eski değerin yanında** durur; önbellek
isabet/ıska sayısı log'da görülür (ıska ≈ %100 beklenir — istem değişti).

- [x] **Adım 3: Şerh yaz** — ⚠️ tarihsel `verdict`'ler artık kıyaslanamaz; eski sayılar
`~üstü çizili~` olarak korunur, **silinmez**.
`verify:` şerh dosyada; eski/yeni iki sütun yan yana.

- [x] **Adım 4: Commit**

---

### Görev 6 · F0.6 — `tgta_v1` VRAM ölçümü ($0, ~15 dk)

**Dosyalar:** Create: `outputs/eval/_artefakt/vram_stack_tgta_v1.json`

**Neden:** Bugünkü **3,09 GiB** (ctx 4.096) **base GGUF** üzerinde ölçüldü; yayımlanacak
artefaktın kendisi ölçülmedi.

- [x] **Adım 1: Ölç**

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
# ⚠️ Script'in bayrakları: --ggufs --ctxs --kv-type --out. `--cache-type-k/-v`,
# `--host`, `--port`, `--no-context-shift` llama-server'ın bayraklarıdır, bu script'in DEĞİL
# (2026-09-06'da koşmadan önce yakalandı).
python scripts/measure_vram_stack.py \
  --ggufs models/gguf/tgta_v1-q4_k_m.gguf \
  --ctxs 4096 32768 131072 --kv-type q8_0 \
  --out outputs/eval/_artefakt/vram_stack_tgta_v1.json
```
`verify:` üç ctx için sunucu GiB + tepe MiB basıldı. Base ile kıyas: ctx 4.096 → base **3,09 GiB**.
⚠️ Fark **%1'den büyükse** sebebi yazılır (aynı boyut Q4_K_M olmalı: base 2.783.446.752 B ↔
`tgta_v1` 2.783.446.720 B).

- [x] **Adım 2: `≤8 GB` yumuşak kapısına göre hüküm** — hangi ctx'e kadar bandın içinde.
`verify:` tek satırlık hüküm dosyada.

- [x] **Adım 3: Commit**

---

### Görev 7 · F0.7 — eşik ön-kaydı + karar defteri

**Dosyalar:** Create: `docs/adr/0063-yeterlilik-onsozu-kaldirildi.md` ·
`docs/adr/0064-v1-kapisi-uc-maddeli-on-kayit.md` ·
`docs/adr/0065-bolunmus-surumleme.md` ·
`docs/adr/0066-b1-yontemi-reddetme-orneklemesi.md` ·
`docs/record/research_log/2026-09-06-faz0-olcum-zinciri.md` ·
Modify: `docs/record/research_log/README.md` (**#62** satırı) · `docs/open_questions.md`
⚠️ **0059 REZERVE — atlanır.**

- [x] **Adım 1: ADR-0063** — önsöz kaldırıldı. ADR-0058'in gerekçesinin **tersine döndüğünü**
iki yerde işaretle (0058'in kendi dosyasına da şerh). Ölçüm: önsözlü %68,4 ↔ önsözsüz %73,0
(−4,6 p kütle) · A1 0,8288 ↔ 0,8110 · isabetsizlik 5/80 ↔ 7/80 · aynı 80 soru, **80/80 birebir
aynı bağlam**, değişen yalnız istem.
`verify:` ADR-0058 dosyasında *"gerekçesi ADR-0063 ile tersine döndü"* şerhi var.

- [~] **Adım 2: ADR-0064 — kapı, sayıyla kapanır**  ⏳ **madde (3) M5 ölçümünü bekliyor**

```
(1) kütle ≥ (3.5 Flash kütlesi, F0.4) − 2,0 p
(2) isabetsizlik ≤ (F0.3'ün göz sayısı)
(3) M5 ≤ bugünkü
(*) her sayım adımında gözle okuma
```
`verify:` δ=2 p'nin **neden gürültü tabanından türetilemediği** yazılı (taban 0,3 p yalnız A1
için; kütle = coverage × A1 ve coverage varyansı o tabanda yok) · sayılar F0.3/F0.4'ten
**alıntı ve dosya adıyla**.

- [x] **Adım 3: ADR-0065** (bölünmüş sürümleme) + **ADR-0066** (B1 = reddetme-örneklemesi,
GRPO **gerekçeli** ertelendi: $10-30 tahmin ↔ Modal $29,19, tahmin ölçülmedi).
`verify:` ADR-0066'da GRPO'nun **hangi ölçümle** açılacağı yazılı.

- [x] **Adım 4: research_log #62** — Faz 0'ın tam anlatısı: ne koştu, ne çıktı, **ne şaşırttı**.
`verify:` README tablosuna #62 satırı eklendi; her sayının yanında kaynak dosya var.

- [x] **Adım 5: `open_questions.md` bakımı** — kapanan **S1 · S2 · S11 · S14** ADR'lere işlenip
**kapanış dizinine** taşınır (gövdeden çıkar, iz kalır); otorite `TASARIM.md` → `PRODUCT.md`.
`verify:` `grep -c "TASARIM.md" docs/open_questions.md` → **0**.

- [x] **Adım 6: Commit**

---

### Görev 8 · T3 + T4 — ucuz temizlik (Faz 0'a paralel, bağımsız)

- [x] **Adım 1: `.gitignore`'a `.pytest_cache/`**
`verify:` `git check-ignore -q .pytest_cache && echo ignored`

- [x] **Adım 2: `scripts/train_orpo.py` docstring'i gerçeğe çekilir**
Bugünkü hâli *"base = v2b ADAPTER'dan DEVAM (grounding taşınır)"* diyor; bu **ardışık SFT**
kalıbıdır ve `τ = θ_ft − θ_base` tanımına aykırıdır. Gerçek: `τ_a v1` **`--fresh-adapter`** ile
ham base'den koştu (`docs/record/kollar.md`:64). Docstring bunu söyleyecek, `--adapter`
yolunun **task-vector üretmediği** şerhiyle.
`verify:` `grep -n "fresh-adapter" scripts/train_orpo.py` docstring'de eşleşme verir · `pytest` **112 passed, 2 xfailed**.

- [x] **Adım 3: Commit** (yapısal değişiklik — davranış değişmez, ayrı commit)

---

### Görev 9 · T5 — `scripts/` çöp denetimi + alt-klasör düzeni *(insan talebi 2026-09-07)*

**Talep:** *"`scripts` içinde gereksiz çöp script var mı kontrol et, var ise sil; yok ise klasörü
düzenle — hepsi tek yığında çok kötü, `scripts/abc/abc.py` gibi alt-klasörlere bölünmeli."*

⚠️ **Bu görev Faz 0'ın ÖLÇÜM zincirinin dışındadır** (Görev 8 gibi: paralel, bağımsız temizlik).
Faz 0'ın manşet sayısı **40/40 ile kapanır**; T5 onun **üstüne** eklenen iştir.

**Envanter — ölçüldü 2026-09-07 (salt okunur, hiçbir dosyaya dokunulmadı):**

| | sayı |
| :--- | ---: |
| toplam script (`.py` 51 + `.sh` 21) | **72** · 11.817 satır · ~712 KB |
| **CANLI-KOD** (script/`modal_train.py`/test çağırıyor ya da import ediyor) | **44** |
| BELGE-BAĞLI (yalnız `docs/**` ya da `*.md`'de adı geçiyor) | 22 |
| YETİM (hiçbir yerde adı geçmiyor) | **6** |

### 🚨 Bulgu 1: **silinecek çöp YOK**

Altı yetimin **hiçbiri** çöp değil — docstring'leri okundu, hepsi ya belgelenmiş bir üretim
hattının halkası ya da bağımsız bir tanı aracı:

| dosya | neden kalır |
| :--- | :--- |
| `gen_v2b_answers.py` | `build_sft_v2b pack` → **bu** → `assemble` zincirinin **ortanca halkası** |
| `build_v3_devset.py` | ORPO hiperparametre dev-set'i (v3 reçetesi Adım 5), sızıntı kontrollü — **yeniden üretim için gerekli** |
| `score_format.py` | A4 atıf-format metriği, deterministik (LLM'siz) — **CANON'un dört ekseninden biri** |
| `diag_modal_gpu.py` | Modal imajında GPU görünürlüğü tanısı; CP2-c'de **gerçek bir hatayı yakaladı** |
| `build_eval_ood_qa.py` | OOD eval seti üreticisi (v3 held-out kanun) |
| `watch_run.sh` | Modal koşusu yoklayıcı |

⇒ *"Adı başka kodda geçmiyor"* bu repoda **çöp demek değil**: `scripts/`'in çoğu dosyası
**elle çağrılan giriş noktasıdır**. Silme ölçütü *"referanssız"* olamaz.

### 🚨 Bulgu 2: taşımanın gerçek maliyeti — **sessizce kırılan 65 import**

**18 modül**, ~**65** satır **uzantısız** Python import'uyla çağrılıyor
(`import runlock` · `from build_sft_v2b import clip_sources_block` · `import raft_pack` …).
Hepsi `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))` desenine dayanıyor —
yani **"kardeş dosya"** varsayıyor (18 dosyada bu satır var, **16'sı birebir aynı**).

⇒ Alt-klasöre bölününce bu import'lar **`ImportError` ile çalışma zamanında** patlar; bir GPU
koşusunun ortasında da patlayabilir. **Bu reponun tam olarak "sessiz yanlışlık" sınıfı.**

**En çok referans taşıyanlar:** `gen_eval_grounded.py` (19 kod ref) · `score_abstention.py` (18) ·
`groundedness.py` (15) · `build_sft_v2b.py` (9) · `raft_pack.py` · `llm_client.py` ·
`rescore_answered.py` (7'şer).

**Gruplar arası köprü gerektiren 7 modül:** `atif_dogrula` · `madde_anahtar` · `raft_pack` ·
`build_sft_v2b` · `score_abstention` · `llm_client`/`runlock` · `retriever`.

**Maliyet:** **~353 kod referans satırı** (kritik — taşıma anında kırılır) ·
~622 belge satırı, ama bunun **~590'ı tarihsel `research_log`/ADR** (*"o gün şu yoldan koşuldu"*
diyen kayıtlar — ⛔ **güncellenmez**, kayıt temizlenmez) ve yalnız **~30'u** güncel referans
belgesi (`CLAUDE.md` · `DEVIR-PROMPT.md` · aktif spec) ⇒ **güncellenir**.

### Önerilen taksonomi (5 grup, işlevden türetildi)

| klasör | ne | kaç dosya |
| :--- | :--- | ---: |
| `scripts/egitim/` | LoRA eğitim · merge · GGUF · kurulum | 6 |
| `scripts/olcum_uretim/` | harness koşucuları · üretim gövdesi · tanı · VRAM/token ölçümü | 14 |
| `scripts/puanlama/` | hakemlik · skorlama · tablo · karşılaştırma · `llm_client` · `runlock` | 22 |
| `scripts/erisim_korpus/` | retriever · recall · korpus bütünlüğü · atıf doğrulama | 10 |
| `scripts/veri_hazirlik/` | SFT/ORPO/RAFT veri inşası · B8/B10/CP2 hasat hattı | 20 |

### Adımlar

- [ ] **Adım 1: Taşımadan ÖNCE taban ölç** — `pytest` (beklenen **112 passed, 2 xfailed**) ·
her `.sh` için `bash -n` · `git status` temiz.
`verify:` üç çıktı da kaydedildi; **taşıma sonrası kıyas çıpası budur**.

- [ ] **Adım 2: `sys.path` desenini ÖNCE düzelt, taşımayı SONRA yap** *(sıra bağlayıcı)*

18 dosyadaki satır, kendi klasörü yerine **`scripts/` kökünü + tüm alt klasörleri** ekleyecek
hâle getirilir. Böylece dosya **hangi alt klasöre giderse gitsin** kardeşlerini bulur:

```python
_R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # scripts/
sys.path[:0] = [_R] + [os.path.join(_R, d) for d in sorted(os.listdir(_R))
                       if os.path.isdir(os.path.join(_R, d)) and not d.startswith(("_", "."))]
```

⚠️ **Bu adım taşımadan ÖNCE ve TEK BAŞINA commit edilir.** Henüz alt klasör yokken de doğru
çalışır (liste boş döner, `_R` = `scripts/`) ⇒ `pytest` bu adımdan sonra **hâlâ yeşil olmalı**.
Yeşil değilse taşımaya **geçilmez**. *(Beck, Tidy First: yapısal değişiklik davranışı değiştirmez
ve ayrı commit'lenir.)*
`verify:` `pytest` **112 passed, 2 xfailed** — Adım 1'in çıpasıyla **birebir aynı**.

- [ ] **Adım 3: `tests/`'in yol kurulumu** — testler de `scripts/`'i `sys.path`'e ekliyor.
`tests/conftest.py` (yoksa oluştur) `scripts/` kökünü **ve alt klasörlerini** ekler; tekil
test dosyalarındaki elle `sys.path` satırları oraya devredilir.
`verify:` `pytest` yeşil, ve `grep -c "sys.path" tests/*.py` **azalmış**.

- [ ] **Adım 4: `git mv` ile taşı** — taksonomiye göre, **grup grup**, her grup **ayrı commit**.
⛔ Tek seferde hepsini taşıma: kırılma olursa hangi grubun kırdığı anlaşılmaz.
`verify:` her gruptan sonra `pytest` yeşil **ve** `bash -n` her `.sh` için temiz.

- [ ] **Adım 5: Kod referanslarını güncelle** — `bash scripts/X.sh` · `python scripts/X.py` ·
`modal_train.py`'nin `cmd` listeleri · Modal imajındaki `/root/scripts/...` yolları.
🚨 **`modal_train.py` en riskli**: yol string'i orada **çalışma zamanına kadar sessiz kalır**
(tuzak 6.12: *"bayrak script'e eklenir, çağrı zincirine eklenmez"*).
`verify:` `grep -rn "scripts/[a-z0-9_]*\.\(py\|sh\)" --include="*.py" --include="*.sh" .`
çıktısındaki **her** yol var olan bir dosyayı gösterir (döngüyle sınanır, gözle değil).

- [ ] **Adım 6: Güncel belgeleri güncelle, TARİHSEL OLANLARA DOKUNMA**
Güncellenir: `CLAUDE.md` · `DEVIR-PROMPT.md` · aktif spec (~30 satır).
⛔ **Güncellenmez:** `docs/record/**` · `docs/adr/**` (~590 satır) — bunlar *"o gün şu yoldan
koşuldu"* diyen **tarihsel kayıtlar**; spec §11'in ilk kuralı: **KAYIT TEMİZLENMEZ.**
`verify:` `git diff --stat` `docs/record/` ve `docs/adr/` altında **0 değişiklik** gösterir.

- [ ] **Adım 7: Uçtan uca duman testi** — bir gerçek koşu zinciri kısa `--n` ile çalıştırılır
(ör. `cp0_thinking_gen.sh` + `cp0_thinking_score.sh`, `N_OVERRIDE=2`).
**Neden:** `pytest` import'ları yakalar, **`bash` çağrılarını yakalamaz**; bu turda üç kez
yanlış bayrak/yol çıktı ve üçü de yalnız koşarken görüldü.
`verify:` zincir uçtan uca hatasız tamamlanır ve künye basılır.

- [ ] **Adım 8: Commit + `docs/record/yurutme-tuzaklari.md`'ye tuzak yaz**
*"Paylaşılan modülleri alt klasöre taşımak uzantısız import'ları sessizce kırar"*.

**Bedel:** $0 · ~30-45 dk · **GPU gerekmez** ⛔ ama Faz 0'ın koşuları bitmeden **başlamaz**
(`cp0_thinking_gen.sh` canlı kullanımda).
**Bağımlılık:** Faz 0 Görev 7 kapanmış olmalı.

---

## ⏭️ Bu planın DIŞINDA — sonraki plana

- **T1** `models/` ~20 GB temizliği — ⚠️ ön koşulu **AÇIK KARAR S7** (adaptörler HF'ye yüklensin mi);
  adaptörler yedeksizken türevleri silmek yıkım yarıçapını büyütür.
- **T2** 16 script'in arşivi — 🚨 **ölçüldü ve toplu taşıma YAPILAMAZ**: 7'si canlı kodla bağlı
  (`cp0_thinking_gen.sh` ← `modal_train.py` + `cp3_merge_dene.sh` · `cp2_harvest.py` ←
  `modal_train.py` · `cp2c_kabul.sh` ← `score_abstention.py`). Liste **izole 9'a** indi ve
  **Faz 0'dan sonraya** alındı — ölçümün aletini ölçümden önce oynatmıyoruz.
- 🆕 **Borç: uzun madde chunk'lama.** Ölçüldü 2026-09-06: `_src_len` en uzun çeyreğinde
  `recall@10` = **0,6667** (Q2/Q3'te 0,9333). İlişki **U biçimli** — en kısa çeyrek de 0,8000.
  Sebep: chunk = **tam madde** (ADR-0054/K2); uzun madde çok konuyu kapsar, tek gömme seyrelir,
  BM25 uzunluk normalizasyonu cezalandırır. ⚠️ **B9'dan AYRI**: orada *bozuk* chunk var
  (tablo/cetvel parçaları), burada **doğru ama çok uzun** chunk.
- 🆕 **Borç: DEV/TEST ayrımı katmanlanmamış.** Kanuna göre kusursuz 2:1, ama madde uzunluğuna
  göre değil: en zor uzunluk diliminde DEV'in payı %12, TEST'in **%50**. Düzeltmek **donmuş
  TEST'i açmak** demek → bugün yapılmıyor. Raporlama tarafı ADR-0069 ile kapatıldı (S15).
- **Dört belge** (`PRODUCT.md` · `ROADMAP.md` · `TODO.md` · `docs/MIMARI.md`) + kırık link
  onarımı + `referans-design-doc.md`'nin silinmesi — Faz 0'ın sayıları geldikten sonra.
