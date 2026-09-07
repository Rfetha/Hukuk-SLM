# `HP` → Hat A → Hat B — uygulama planı (`v0.2` → `v1.0`)

> **Ajan işçiler için:** GEREKLİ ALT-BECERİ: `superpowers:subagent-driven-development` (önerilen)
> ya da `superpowers:executing-plans`. Adımlar `- [ ]` kutucuklu.
> ⛔ **Kutucuk yalnız `verify:` çıktısı GERÇEKTEN alındıktan sonra işaretlenir.**

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
TUI için `textual` (**henüz kurulu değil** — ölçüldü 2026-09-07).

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
  (ADR-0073). ⛔ **Yalnız M5.** Rakip içeren hiçbir moda eklenmez — DRY bir `llama.cpp`
  örnekleyicisidir, Gemini'ye uygulanamaz, dolayısıyla orada **eşitlenemez** (ADR-0057).
- **Donmuş TEST'e dokunulmaz:** her şey `data/eval/dev/`. `data/eval/canon/` **yalnız**
  Görev 16'nın kabul testinde, **tek kez** açılır.
- **⚡ ŞARJ:** her GPU koşusundan önce künyede `güç : ŞARJDA` doğrulanır. Pilde GPU
  **180 MHz**'e kısılıyor → 80 kalem **4,8 saat** ↔ şarjda **~25 dk** (ölçüldü 2026-09-07).
- **Uzun koşular `setsid nohup … &` ile AYRIK başlatılır**, `Monitor` ile beklenir.
  ⛔ Harness'ın arka plan görevi olarak başlatma: bellek gözcüsü `free`'ye bakıp öldürüyor.
  ⛔ Çıktıyı `| tail`'a sokma — süreç bitene kadar hiçbir şey görünmez.
- **Her koşudan önce** [`docs/record/yurutme-tuzaklari.md`](../../record/yurutme-tuzaklari.md)
  okunur. **17 tuzağın hepsi** *"hata vermeden yanlış sayı üretir"* sınıfından.
- ⭐ **Gözle okuma bir kapıdır.** Faz 0'da sayısal kapı **beş kusuru** geçirdi; beşini de göz
  ya da *"bu sayıyı neyle, hangi birimde kıyaslayacağım?"* sorusu yakaladı.
- **Bütçe — ÖLÇÜLDÜ 2026-09-07:** OpenRouter **$6,60** (`total_credits` 20 −
  `total_usage` 13,397) · Modal **$29,19**. ⚠️ Devir notundaki *"~$8,88"* **yanlıştı**.
  Bu plan **~$10-20** harcar ⇒ **OpenRouter bakiyesi `HP` + kapı koşusuna yetmeyebilir.**
  ⛔ **DUR ve sor:** tek adımda **>$1** harcamadan önce.
- **Lisans:** yalnız kamuya açık kaynak (Mevzuat.gov.tr · Resmî Gazete · Yargıtay açık portal).
  ⛔ **Lexpera / Kazancı ASLA** — telif zehri. Eğitim verisinde PII maskelenir.
- **Kod dili İngilizce, belge/yorum/commit dili TÜRKÇE.**
- ⛔ **DUR ve sor:** yeni rejim kararı · **>$1** harcama · donmuş TEST'in açılması ·
  bir `AÇIK KARAR` damgasının kendi başına kapatılması.

### 🔓 AÇIK KARARLAR — insan cevabı olmadan ilgili görev BAŞLAMAZ

| # | soru | bloke ettiği görev |
| :-- | :--- | :--- |
| **S5** | İkili oran çözünürlük sınırı (Wilson aralığı kapı kuralını değiştirir) | Görev 16 (yorum) |
| **S7** | LoRA adaptörleri HF'ye yüklensin mi? | Faz 0 planı **T1** |
| **S8** | İndeks nasıl dağıtılır? (80 MB — ölçüldü) | **Görev 8** |
| **S9** | `v2` nasıl barındırılır? | bu planın **dışında** |
| **S10** | Avukatlık Kanunu / hukuki sorumluluk sınırı — **hukukçu görüşü** | **Görev 11** |
| **S12** | KARAR-6 paralel slot (`-np`) — bozuk ölçütle toplandı | Görev 13 (taşıyıcı) |
| **S16** 🆕 | `v1.0` rakip havuzunda hangi sağlayıcı, kaç özne? | **Görev 4** |
| **S17** 🆕 | Kuantizasyon eğrisi ölçülsün mü? | bu planın **dışında** |
| **S18** 🆕 | Sürüklenmiş `SYSTEM_PROMPT`'un hangi hâli kanon? | **Görev 5** |

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

# FAZ 1 · `HP` — hakem paneli (~$3-5) 🔒 ÖNCE

**Neden:** Bugün yayımlanan **her** sayı `openai/gpt-4o-mini`'nin **tek başına** hükmü.
κ **yok**, öz-tercih **ölçülmedi** — ADR-0064 bunu *"Ne KURULMAZ"* madde 2 olarak zaten borç
yazmış. Ve [ADR-0072](../../adr/0072-v1-rakip-havuzu-genisler.md)'nin GPT öznesi **bu panel
kurulmadan eklenemez** (aile dışlaması, ADR-0032).

**Ölçülmüş boşluk:** `scripts/judge_agreement.py` **hazır** — üç modu var (`cross` · `export` ·
`author`), eşik dosyada yazılı: **κ ≥ 0,6 makul · ≥ 0,8 güçlü**. Yeni araç **gerekmiyor**.

---

### Görev 1: İkinci hakem ailesi (Anthropic) — aynı kayıtlar yeniden puanlanır

**Dosyalar:**
- Create: `outputs/eval/hp-hakem-paneli/` (+ `KUNYE.json`)
- Read: `scripts/judge_agreement.py` · `scripts/groundedness.py` · `scripts/llm_client.py`
- Girdi (**değişmez, yeniden üretilmez**): `outputs/eval/f02-biz-onsozsuz/h1_tgta_v1_f02_nb_detail.jsonl`

**Arayüzler:**
- Tüketir: F0.2'nin `h1_*_detail.jsonl` dosyası (80 kalem, önsözsüz, bütçe 1536)
- Üretir: `outputs/eval/hp-hakem-paneli/gnd_h1_tgta_v1_anthropic.jsonl` +
  `..._summary.json` — `judge_agreement.py cross --b` bunu bekler

⛔ **Üretim YENİDEN KOŞULMAZ.** Panel **hakem** değişkenini ölçüyor; üretimi de değiştirmek
iki değişkeni birlikte oynatır (ADR-0017). Aynı 80 cevap, farklı hakem.

- [ ] **Adım 1: Hakem kimliğini ve fiyatını koşmadan ÖNCE doğrula**

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
⛔ Kimliği **tahmin etme** — buradan al. ⚠️ Fiyat `gpt-4o-mini`'den **belirgin yüksekse**
maliyeti yeniden hesapla ve **$1'ı aşacaksa DUR ve sor**.

- [ ] **Adım 2: Bedeli ölç — 5 kalemlik duman koşusu**

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
set -a && . ./.env && set +a && export OPENAI_API_KEY="$OPENROUTER_API_KEY" && \
mkdir -p outputs/eval/hp-hakem-paneli && \
LLM_GATEWAY=openrouter LLM_PROVIDER_ORDER=Anthropic \
python scripts/groundedness.py \
  --details outputs/eval/f02-biz-onsozsuz/h1_tgta_v1_f02_nb_detail.jsonl \
  --label h1_tgta_v1_anthropic_duman --mode data \
  --judge-model <ADIM-1'DEN GELEN KİMLİK> --n 5 \
  --out-dir outputs/eval/hp-hakem-paneli
```
`verify:` `gnd_h1_tgta_v1_anthropic_duman_summary.json` yazıldı, `n=5`, `judge_cost_usd` **basıldı**.
Tam koşu tahmini = `judge_cost_usd × 16`. ⛔ **> $1 ise DUR ve sor.**

- [ ] **Adım 3: Tam koşu (80 kalem), AYRIK**

```bash
cd /home/ersoy/code/Hukuk-SLM && \
setsid nohup bash -c 'source ~/code/global_venv/bin/activate && \
  set -a && . ./.env && set +a && export OPENAI_API_KEY="$OPENROUTER_API_KEY" && \
  export PYTHONUNBUFFERED=1 && \
  LLM_GATEWAY=openrouter LLM_PROVIDER_ORDER=Anthropic \
  python scripts/groundedness.py \
    --details outputs/eval/f02-biz-onsozsuz/h1_tgta_v1_f02_nb_detail.jsonl \
    --label h1_tgta_v1_anthropic --mode data \
    --judge-model <ADIM-1 KİMLİĞİ> \
    --out-dir outputs/eval/hp-hakem-paneli; \
  echo "EXIT=$?"' > /tmp/hp_anthropic.log 2>&1 < /dev/null &
```
`verify:` `/tmp/hp_anthropic.log` sonunda `EXIT=0` · `gnd_h1_tgta_v1_anthropic_summary.json`
`n=80` · `judge_cost_usd` künyeye yazılacak.

- [ ] **Adım 4: Commit**

```bash
git add outputs/eval/hp-hakem-paneli/ && \
git commit -m "HP: ikinci hakem ailesi (Anthropic) — aynı 80 cevap, farklı hakem"
```

---

### Görev 2: Üçüncü hakem ailesi (Google) — ⚠️ AİLE DIŞLAMASI burada ısırır

**Dosyalar:**
- Create: `outputs/eval/hp-hakem-paneli/gnd_h1_tgta_v1_google*.json*`
- Read: [ADR-0032](../../adr/0032-hakem-paneli-uc-aile-ve-aile-dislama.md)

**Arayüzler:**
- Tüketir: Görev 1 ile **aynı** girdi dosyası
- Üretir: üçüncü ailenin `gnd_*.jsonl`'i — Görev 3'ün κ üçlüsü bunu bekler

🚨 **Kritik ayrım — bu görevin varlık sebebi:**

| özne | ailesi | Google hakem kullanılabilir mi |
| :--- | :--- | :--- |
| **`tgta_v1` (biz)** | Qwen/Alibaba | ✅ **evet** — üç ailenin hiçbiri bizim ailemiz değil |
| `gemini-3.1-FL` · `3.5-FL` · `3.5-Flash` | **Google** | ❌ **HAYIR** — kendi ailesi kendini notlayamaz |

⇒ **Üçlü κ yalnız BİZİM kolumuzda kurulur.** Rakip kolları **iki aileyle** (OpenAI + Anthropic)
notlanır. Bu bir eksiklik değil, **ADR-0032'nin kuralının doğrudan sonucudur** ve raporda
**açıkça** yazılır.

- [ ] **Adım 1: Kimlik + fiyat doğrula** — Görev 1 Adım 1'in aynısı, `gemini` filtresiyle.
`verify:` kimlik ve fiyat basıldı.

- [ ] **Adım 2: Tam koşu (80 kalem), AYRIK** — Görev 1 Adım 3'ün aynısı;
`LLM_PROVIDER_ORDER=Google`, `--label h1_tgta_v1_google`.
`verify:` `EXIT=0` · `n=80` · `judge_cost_usd` basıldı.

- [ ] **Adım 3: Aile dışlaması denetimi — otomatik, gözle değil**

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
        print(f"🚨 İHLAL  {os.path.basename(f)}  özne={ozne_aile} hakem={hakem_aile} ({jm})")
        ihlal += 1
print(f"\naile dışlaması ihlali: {ihlal}")
sys.exit(1 if ihlal else 0)
PY
```
`verify:` çıktı `aile dışlaması ihlali: 0` ve **çıkış kodu 0**. ⛔ İhlal varsa **DUR** —
o sayı yayımlanamaz.

- [ ] **Adım 4: Commit**

---

### Görev 3: κ hesabı + öz-tercih ölçümü + hangi sayının bağlayıcı olduğu

**Dosyalar:**
- Create: `outputs/eval/hp-hakem-paneli/KAPPA.md` · `KUNYE.json`
- Create: `docs/adr/0074-hakem-paneli-kuruldu-baglayici-hukum.md`
- Read: `scripts/judge_agreement.py` (üç modu var: `cross` · `export` · `author`)

**Arayüzler:**
- Tüketir: üç ailenin `gnd_*.jsonl` dosyaları
- Üretir: her eksen için **κ** ve **bağlayıcı okuma kuralı** — Görev 16'nın kapı koşusu bunu kullanır

- [ ] **Adım 1: İkili κ'ları hesapla — üç çift**

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
D=outputs/eval/hp-hakem-paneli && \
for CIFT in "f02-biz-onsozsuz/gnd_h1_tgta_v1_f02_nb:$D/gnd_h1_tgta_v1_anthropic:openai_anthropic" \
            "f02-biz-onsozsuz/gnd_h1_tgta_v1_f02_nb:$D/gnd_h1_tgta_v1_google:openai_google" \
            "$D/gnd_h1_tgta_v1_anthropic:$D/gnd_h1_tgta_v1_google:anthropic_google"; do
  A="outputs/eval/${CIFT%%:*}.jsonl"; R="${CIFT#*:}"; B="${R%%:*}.jsonl"; AD="${R#*:}"
  echo "=== $AD ==="
  python scripts/judge_agreement.py cross --a "$A" --b "$B" --field verdict --kind cat
done
```
⚠️ **`--field` adını TAHMİN ETME.** Önce oku:
`head -1 outputs/eval/f02-biz-onsozsuz/gnd_h1_tgta_v1_f02_nb.jsonl | python -m json.tool`
— bu turda **üç kez** yanlış bayrak/alan adı çıktı, üçü de yalnız koşarken görüldü.
`verify:` üç çift için uyum % **ve** κ basıldı.

- [ ] **Adım 2: Öz-tercih ölçümü — "hakem kendi ailesinin cevabını kayırıyor mu"**

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
print("⚠️ Öz-tercih tam ölçümü aile dışlaması nedeniyle KURULAMIYOR (Google özne ↔ Google hakem yasak).")
print("   Raporlanan: hakemler arası SİSTEMATİK KAYMA (bias), bizim kolumuzda.")
PY
```
`verify:` her hakem çifti için **ortalama fark** (bias) ve **mutlak fark ortalaması** (gürültü)
ayrı ayrı basıldı. ⚠️ İkisi **ayrı** raporlanır: sistematik kayma ≠ rastgele gürültü.
🆕 Ölçülemeyen şey (**Google özne ↔ Google hakem**) `KAPPA.md`'ye **açık borç** olarak yazılır.

- [ ] **Adım 3: `KAPPA.md` — üç okuma, ve BAĞLAYICI olanın seçimi**

Zorunlu içerik:
1. Üç κ değeri + `judge_agreement.py`'nin kendi eşiği (**κ ≥ 0,6 makul · ≥ 0,8 güçlü**)
2. **Aile dışlaması matrisi** — hangi özne × hakem hücresi **yasak** ve neden
3. Hakemler arası **bias ↔ gürültü** ayrımı, sayıyla
4. ⚠️ **Yeniden-koşum gürültü tabanı 0,3 A1 puanıdır ve YALNIZ A1 için ölçüldü.** Hakemler
   arası fark bu tabanın **altındaysa** *"hakemler ayrışıyor"* cümlesi **kurulmaz**
5. Kütle için **ayrı taban yok** (`kütle = coverage × A1`, coverage varyansı o tabanda yok)

`verify:` `KAPPA.md` üç κ, aile matrisi ve *"bağlayıcı okuma"* cümlesini içeriyor.

- [ ] **Adım 4: ADR-0074 — bağlayıcı hüküm kuralı, KAPI KOŞUSUNDAN ÖNCE ön-kayıt**

⛔ Bu ADR **Görev 16'dan önce** yazılır. ADR-0050: raporlama biçimi koşudan **önce**
ön-kayıtlanır; sayı görüldükten sonra *"şu hakeme göre..."* demek kuralın engellediği şeydir.

Karara bağlanacaklar: (a) `v1.0` kapısının bağlayıcı hakemi **hangisi** (ya da **panel
ortalaması** / **en muhafazakârı**), (b) κ eşiğin altında çıkarsa ne olur, (c) rakip kolları
iki aileyle notlandığı için hükmün **hangi kısmı** üç aileye dayanıyor.
`verify:` ADR'de *"bu kural kapı koşusundan ÖNCE yazıldı"* şerhi ve **tarih** var.

- [ ] **Adım 5: `research_log` #63 + README satırı + commit**

`verify:` `docs/record/research_log/README.md`'de **#63** satırı var; her sayının yanında
**kaynak dosya adı** duruyor.

---

### Görev 4: `v1.0` rakip havuzunun genişletilmesi 🔓 **AÇIK KARAR S16**

**Dosyalar:** Create: `outputs/eval/hp-rakip-havuzu/`
**Bağımlılık:** Görev 3 **bitmiş** olmalı.

⛔ **Bu görev insan cevabı olmadan BAŞLAMAZ.** Cevaplanacak: *hangi sağlayıcı(lar), kaç özne?*
Girdiler [ADR-0072](../../adr/0072-v1-rakip-havuzu-genisler.md)'de: özne başı **~$0,35**
(F0.4'te ölçüldü: üç çıpa **$1,35**) · Anthropic öznesi sorunsuz · **GPT öznesi** hakem
değişikliği + bugünkü dört sayının **yeniden koşulması** demek.

- [ ] **Adım 1: İnsan kararını al ve künyeye yaz** *(kod yok — karar adımı)*
`verify:` `KUNYE.json` seçilen özneleri **tam model kimliğiyle** listeliyor.

- [ ] **Adım 2: Her özne için üretim — F0.4'ün BİREBİR aynı komutu**

⚠️ Rakip tarafı **`--reasoning-budget 1024`** kullanır, `--think-budget` **DEĞİL** (ikisi
karşılıklı dışlayıcı; `--think-budget` istemci-taraflı zorunlu kapatmadır ve **yalnız bizim
kolda**). Künye kanıtı: `g2-fl-harness/KUNYE.json` → `"reasoning_budget": 1024`.
`verify:` her özne için `h1_*_detail.jsonl` **80 satır** · komutta `--sufficiency-preamble` **yok**.

- [ ] **Adım 3: Eşit sınav kapısı — `recall@10` birebir aynı mı**

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
`verify:` **hepsinde 0,9500** ve bizim kolla birebir. Farklıysa 🚨 **DUR** — harness eşleşmemiş,
hüküm kurulmaz (ADR-0057).

- [ ] **Adım 4: Puanlama (panel hakemleriyle) + kesiklik damgası + gözle kalibrasyon**

⚠️ **Red-regex her yeni özne ailesinde kalibre EDİLMELİ.** Kalibresiz bırakmak onların
reddini **eksik** sayar ve puanı **bizim lehimize** kaydırır. F0.4'te ölçüldü: Gemini
kollarında **6 açık yanlış pozitif**, bizde **0**.
`verify:` özne başına **ALET / GÖZ-orta / GÖZ-katı** üç okuma da raporlandı.

- [ ] **Adım 5: `OZET.md` + commit** — ⛔ `v1.0` kapısının eşiği **oynamaz**; çıpa
`3.5 Flash` kalır (ADR-0072 madde 2). Yeni özneler **raporlanır**, eşiği **kurmaz**.

---

# FAZ 2 · Hat A — paketleme ($0, GPU yok) → `v0.2`

**`HP`'ye PARALEL koşabilir.** Hakeme ve GPU'ya dokunmaz.

**Ölçülmüş boşluk (2026-09-07):**
- Servis katmanı **kod olarak yok**: `grep -rlE "fastapi|uvicorn|flask|gradio" scripts/` → **0**
- Modeli indiren kişi yayımlanan sayıyı **üretemiyor** (YB6)
- `textual` **kurulu değil**
- İndeks **80 MB** ve `.gitignore:166` gereği git'te **yok** ⇒ S8 gerçek bir soru

---

### Görev 5: İstem artefaktı — 🚨 spec'in dediğinden KÖTÜ 🔓 **AÇIK KARAR S18**

**Dosyalar:**
- Create: `hakhukuk/__init__.py` · `hakhukuk/istem.py` · `tests/test_istem.py`
- Modify: `scripts/gen_eval_grounded.py:39-58` · `scripts/raft_pack.py:20` ·
  `scripts/train_sft.py:31` · `scripts/gen_v3_rejected.py:37` · `scripts/build_orpo_v3.py:36`

**Arayüzler:**
- Üretir: `hakhukuk.istem.SISTEM_KOR` · `SISTEM_TEK_KAYNAK` · `SISTEM_COK_KAYNAK` ·
  `ISTEM_SURUMU: str` · `damga() -> str`
- Tüketir: yok (yaprak modül — bilerek bağımsız)

**Neden:** Spec *"istem yalnız `gen_eval_grounded.py` içinde"* diyordu. **Sayıldı:**
`"Sen HakHukuk'sun"` literali **5 dosyada**. Ve içerikler karşılaştırıldı:

| sabit | tanım | durum |
| :--- | ---: | :--- |
| `SYSTEM_PROMPT_RAG` | 3 | ✅ üçü de **bayt-bayt aynı** (`bbfdd6613f`) |
| `SYSTEM_PROMPT_RAG_MULTI` | 1 | ✅ `gen_eval_grounded` **import ediyor** |
| **`SYSTEM_PROMPT`** | 2 | 🚨 **SÜRÜKLENMİŞ** |

Sürüklenmenin tam yeri — **son satır**:
- ölçüm (`gen_eval_grounded.py:39`): `…ilgili kanun ve madde numarasını belirt.`
- eğitim (`train_sft.py:31`): `Bu yanıt hukuki tavsiye değil, bilgilendirme amaçlıdır.`

Bu, **M5'in (kör mod) istemidir**. ⇒ İş mekanik refactor değil; **hangi metnin kanon olduğuna
karar vermek** gerekiyor (**S18**).

- [ ] **Adım 1: Kararı al — hangi `SYSTEM_PROMPT` kanon** *(kod yok)*

⛔ **İnsan kararı.** Girdiler: ölçüm sürümüyle **bütün M5 sayıları** üretildi (Faz 0 dahil);
eğitim sürümündeki feragat cümlesi **ürün için değerli** (A6/S10 ile örtüşüyor).
`verify:` karar `docs/open_questions.md` **S18** satırına ve ADR'ye işlendi.

- [ ] **Adım 2: Failing test yaz**

```python
# tests/test_istem.py
import hashlib
from hakhukuk import istem


def test_istem_surumu_ve_damgasi_sabittir():
    """İstem değişirse damga değişir → yayımlanan sayı yeniden üretilemez hâle gelir.

    Bu test bir KAPIDIR: damgayı bilerek güncellemeden istemi değiştiremezsin.
    """
    assert istem.ISTEM_SURUMU == "v1"
    assert istem.damga() == istem.DAMGA_v1


def test_uc_istem_de_bos_degil_ve_farklidir():
    metinler = [istem.SISTEM_KOR, istem.SISTEM_TEK_KAYNAK, istem.SISTEM_COK_KAYNAK]
    assert all(m.strip() for m in metinler)
    assert len(set(metinler)) == 3


def test_damga_metinlerin_sha256si():
    beklenen = hashlib.sha256(
        "\n---\n".join(
            [istem.SISTEM_KOR, istem.SISTEM_TEK_KAYNAK, istem.SISTEM_COK_KAYNAK]
        ).encode("utf-8")
    ).hexdigest()[:16]
    assert istem.damga() == beklenen
```

- [ ] **Adım 3: Testi koş, BAŞARISIZ olduğunu gör**

Run: `cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && python -m pytest tests/test_istem.py -v`
Beklenen: `FAIL` — `ModuleNotFoundError: No module named 'hakhukuk'`

- [ ] **Adım 4: Asgari uygulama**

```python
# hakhukuk/istem.py
"""Ürünün istem metinlerinin TEK kaynağı.

⚠️ Neden bu dosya var (ölçüldü 2026-09-07): `"Sen HakHukuk'sun"` literali repoda BEŞ
dosyada bulundu ve `SYSTEM_PROMPT` ölçüm ile eğitim arasında SÜRÜKLENMİŞTİ (son satırları
farklıydı). Sürüklenme hata vermez — yalnız modelin eğitildiği istem ile ölçüldüğü istem
sessizce ayrışır. Bkz. açık soru S18.

⛔ Metni değiştirirsen DAMGA_v1 de değişmeli ve ISTEM_SURUMU yükselmeli; aksi hâlde
tests/test_istem.py kırılır. Bu bir kapıdır, engel değil: yayımlanmış bir sayı,
üretildiği istem olmadan yeniden üretilemez.
"""
import hashlib

ISTEM_SURUMU = "v1"

# M5 / kör mod — modele KAYNAK VERİLMEZ. (S18 kararının uygulandığı yer.)
SISTEM_KOR = (
    "Sen HakHukuk'sun. Türk hukuku hakkında sade, anlaşılır Türkçe bilgi verirsin.\n"
    "Emin olmadığın konularda \"Bu konuda güncel mevzuata veya bir avukata "
    "danışmanızı öneririm\" dersin.\n"
    "Asla kanun maddesi veya bilgi uydurmaz, tahmin etmezsin.\n"
    "Cevabını kısa ve anlaşılır tut; ilgili kanun ve madde numarasını belirt."
)

# M4 — tek altın kaynak verilir.
SISTEM_TEK_KAYNAK = (
    "Sen HakHukuk'sun. Türk hukuku hakkında sade, anlaşılır Türkçe bilgi verirsin.\n"
    "Sana bir KAYNAK madde metni verilecek. Cevabını YALNIZCA bu kaynağa dayandır; "
    "kaynakta olmayan bilgi veya madde numarası UYDURMA.\n"
    "Cevabını kısa ve anlaşılır tut; dayandığın kanun ve madde numarasını belirt."
)

# M1/M3/h1 — çok kaynak (harness). ⚠️ Bu metin bugün scripts/raft_pack.py:20'de duruyor
# ve EĞİTİM VERİSİ onunla paketlendi; buraya BİREBİR kopyalanır, yeniden yazılmaz.
SISTEM_COK_KAYNAK = "<<< raft_pack.py:20'den BİREBİR kopyalanacak — yeniden yazma >>>"

DAMGA_v1 = "<<< Adım 5'te hesaplanıp buraya yazılacak >>>"


def damga() -> str:
    """Üç istemin birleşik sha256'sının ilk 16 hanesi. Künyeye bu yazılır."""
    return hashlib.sha256(
        "\n---\n".join([SISTEM_KOR, SISTEM_TEK_KAYNAK, SISTEM_COK_KAYNAK]).encode("utf-8")
    ).hexdigest()[:16]
```

```python
# hakhukuk/__init__.py
"""HakHukuk — açık kaynak Türk hukuku asistanı (ürün katmanı).

⚠️ Bu paket ÜRÜNDÜR; `scripts/` ÖLÇÜM ALETİDİR. Ayrı olmalarının ölçülmüş sebebi:
`scripts/` 72 dosya ve 18 modül uzantısız import'la birbirine bağlı (envanter 2026-09-07).
Ürünü oraya koymak, kullanıcının kurulumunu ölçüm hattının tamamına bağımlı yapardı.
"""
__version__ = "0.2.0"
```

- [ ] **Adım 5: Damgayı hesapla ve dosyaya yaz**

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
python -c "from hakhukuk import istem; print(istem.damga())"
```
Çıkan değeri `DAMGA_v1`'e yaz. `verify:` `python -m pytest tests/test_istem.py -v` → **3 passed**.

- [ ] **Adım 6: `scripts/` beş dosyayı TEK KAYNAĞA bağla — SERT ENGEL**

Beş dosyadaki literaller **silinir** ve yerine import gelir:

```python
# scripts/gen_eval_grounded.py — satır 39-57 yerine
from hakhukuk.istem import (
    SISTEM_KOR as SYSTEM_PROMPT,
    SISTEM_TEK_KAYNAK as SYSTEM_PROMPT_RAG,
    SISTEM_COK_KAYNAK as SYSTEM_PROMPT_RAG_MULTI,
)
```
⚠️ `scripts/` modülleri `sys.path`'e **kendi dizinini** ekliyor; `hakhukuk` **repo kökünde**
olduğu için kök de eklenmeli. Faz 0 planı **Görev 9 · T5 Adım 2** bu düzeltmeyi zaten
tanımlıyor — **önce o adım koşulur**, sonra bu adım.
`verify:` `grep -rc "Sen HakHukuk'sun" scripts/` → **0** · `python -m pytest` **yeşil**.

- [ ] **Adım 7: 🚨 KANIT KAPISI — istem dosyadan okunuyorken sayı BİREBİR aynı mı**

⛔ Bu adım atlanamaz. İstemi taşımak sayıyı **değiştirmemeli**; değiştiyse bir şey kaydı.

```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
set -a && . ./.env && set +a && \
OUT_DIR=outputs/eval/a1-istem-kaniti \
MODES="h1" HARNESS_INDEKS=data/index/mevzuat_bge_m3_s2 HARNESS_K=10 \
THINK_BUDGET=1024 MAXTOK=512 CTX=8192 N_OVERRIDE=10 \
bash scripts/cp0_thinking_gen.sh models/gguf/tgta_v1-q4_k_m.gguf istem_kaniti
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
assert ayni == len(b), "🚨 İSTEM TAŞINMASI ÇIKTIYI DEĞİŞTİRDİ — sebep bulunmadan devam edilmez"
PY
```
`verify:` `birebir aynı: 10/10`. ⛔ Değilse **DUR** — metin bayt düzeyinde farklı demektir.

- [ ] **Adım 8: Commit** *(yapısal değişiklik — davranış değişmez, AYRI commit)*

```bash
git add hakhukuk/ tests/test_istem.py scripts/ outputs/eval/a1-istem-kaniti/ && \
git commit -m "A1: istem artefaktı — beş kopya tek kaynağa indi, 10/10 birebir kanıtlandı"
```

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

- [ ] **Adım 1: Failing test yaz**

```python
# tests/test_tipler.py
import pytest
from hakhukuk.tipler import Atif, Cevap, Durum, Kaynak


def test_durum_dort_hali_var():
    assert {d.name for d in Durum} == {"CEVAP", "CEKINCELI", "SUSKUNLUK", "KESIK"}


def test_cevap_donmus_ve_degistirilemez():
    c = Cevap(metin="x", durum=Durum.CEVAP, atiflar=(), kaynaklar=())
    with pytest.raises(Exception):
        c.metin = "y"


def test_kaynak_kimligi_kanun_madde_ciftidir():
    k = Kaynak(kanun_adi="İŞ KANUNU", kanun_no="4857", madde_no="Madde 31",
               metin="…", sira=1)
    assert k.kimlik == "4857/Madde 31"


def test_atif_dogrulanmamis_olarak_baslar():
    a = Atif(kanun_no="4857", madde_no="Madde 31")
    assert a.dogrulandi is False
```

- [ ] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör**

Run: `python -m pytest tests/test_tipler.py -v` → `FAIL` (`No module named 'hakhukuk.tipler'`)

- [ ] **Adım 3: Asgari uygulama**

```python
# hakhukuk/tipler.py
"""Ürün yüzeyinin veri tipleri. Donmuş — cevap üretildikten sonra değiştirilemez.

⚠️ Neden `Durum` bir enum, `bool` değil (ölçüldü 2026-09-06/07): çekinme dedektörü ÜÇ kez
yanıldı çünkü dünya ikili değil. `suskunluk_terazisi` üç hâl buldu (cevap · çekinceli cevap ·
suskunluk); Faz 0 dördüncüyü ölçtü (kesik). Vatandaş için en tehlikelisi ORTADAKİdir:
"doğrudan madde yok, bununla birlikte…" — cevap gibi görünür, değildir.
"""
from dataclasses import dataclass
from enum import Enum


class Durum(Enum):
    """Bir cevabın vatandaşa ne söylediği. Kapalı küme."""

    CEVAP = "cevap"            # dayanağı var, atıflı
    CEKINCELI = "cekinceli"    # kısmen dayanaklı — rozetle gösterilir
    SUSKUNLUK = "suskunluk"    # dürüst "bilmiyorum"
    KESIK = "kesik"            # üretim bütçesi bitti — YARIM cevap, gizlenmez


@dataclass(frozen=True)
class Kaynak:
    """Retriever'ın getirdiği tek madde."""

    kanun_adi: str
    kanun_no: str
    madde_no: str
    metin: str
    sira: int

    @property
    def kimlik(self) -> str:
        """`kanun_no/madde_no` — korpustaki anahtar (bkz. tuzak 7.6: %22,7 yineleniyor)."""
        return f"{self.kanun_no}/{self.madde_no}"


@dataclass(frozen=True)
class Atif:
    """Modelin cevapta andığı madde. `dogrulandi` deterministik olarak doldurulur."""

    kanun_no: str
    madde_no: str
    dogrulandi: bool = False


@dataclass(frozen=True)
class Cevap:
    metin: str
    durum: Durum
    atiflar: tuple[Atif, ...]
    kaynaklar: tuple[Kaynak, ...]
```

- [ ] **Adım 4: Testi koş, GEÇTİĞİNİ gör**

Run: `python -m pytest tests/test_tipler.py -v` → **4 passed**

- [ ] **Adım 5: Commit**

```bash
git add hakhukuk/tipler.py tests/test_tipler.py && \
git commit -m "A2: ürün tipleri — dört durum enum'la ayrıldı (bool ayrımı kaybediyordu)"
```

---

### Görev 7: `suskunluk_terazisi` ürün yüzeyi — uydurulmuş atıf kullanıcıya GİTMEZ

**Dosyalar:**
- Create: `hakhukuk/terazi.py` · `tests/test_terazi.py`
- Read: `scripts/score_abstention.py` (`exact_reject`, `REJECT_RE`) · `scripts/atif_dogrula.py`

**Arayüzler:**
- Tüketir: `hakhukuk.tipler` (Görev 6)
- Üretir: `siniflandir(metin, kaynaklar, finish_reason) -> tuple[Durum, tuple[Atif, ...]]`
  — Görev 9 (`servis.answer`) bunu çağırır

**Neden ürün yüzeyi:** Bugün ölçüm aleti olan üç şey üründe **güven mekanizması** olur.
Ölçüldü: bizim kolda uydurulmuş madde **0/114**, rakiplerde **1 · 4 · 4**. Bu bir **satış
noktasıdır** ve kullanıcıya gösterilmelidir.

🚨 **Faz 0'ın taze dersi buraya doğrudan giriyor:** `exact_reject`'in *"bulunmamaktadır"*
ailesi hukuk metninde **iki iş görür** — *"kaynakta yok, cevaplayamam"* (çekinme) ↔
*"kanunda böyle bir hüküm yok"* (**esasa ilişkin cevap**). 2026-09-07'de kör modda
**6/6 yanlış pozitif** verdi. ⇒ Ürün sınıflandırıcısı **kaynak var mı** bilgisini
kullanmak zorundadır; metne tek başına bakarsa **aynı hatayı yapar**.

- [ ] **Adım 1: Failing test yaz — Faz 0'ın GERÇEK vakalarıyla**

```python
# tests/test_terazi.py
from hakhukuk.terazi import siniflandir
from hakhukuk.tipler import Durum, Kaynak

IS_K_31 = Kaynak(kanun_adi="İŞ KANUNU", kanun_no="4857", madde_no="Madde 31",
                 metin="Muvazzaf askerlik ödevi dışında manevra veya herhangi bir "
                       "sebeple silâh altına alınan …", sira=1)


def test_olumsuz_hukum_kaynak_VARKEN_cevaptir_cekinme_degildir():
    """2026-09-07 · GERÇEK vaka (BİZ id=37): alet bunu çekinme saydı, göz CEVAP dedi.

    "…zorunlu bir şart bulunmamaktadır" bir HUKUKİ HÜKÜMDÜR, red değil.
    """
    metin = ("Vesayet altındaki bir kişi için aile meclisinin kurulmasının zorunlu bir "
             "şartı bulunmamaktadır. Vesayet, mahkeme kararıyla atanır. "
             "**İlgili Kanun:** Türk Medeni Kanunu, 503. madde.")
    durum, atiflar = siniflandir(metin, kaynaklar=(IS_K_31,), finish_reason="stop")
    assert durum is not Durum.SUSKUNLUK


def test_kaynak_YOKKEN_ayni_metin_suskunluk_sayilabilir():
    """Aynı metin, kaynak yokken: "kaynakta yok" okuması artık MÜMKÜN."""
    metin = "Bu konuda elimdeki kaynaklarda bir hüküm bulunmamaktadır."
    durum, _ = siniflandir(metin, kaynaklar=(), finish_reason="stop")
    assert durum is Durum.SUSKUNLUK


def test_kesik_cevap_gizlenmez():
    """Faz 0 · id 43: yarım cümle sessizce teslim edilmez."""
    durum, _ = siniflandir("İddianame, Cumhuriyet Başsavcılığı tarafından mahkemeye "
                           "sunulur ve mahkeme tarafından kabul edilirse",
                           kaynaklar=(IS_K_31,), finish_reason="length")
    assert durum is Durum.KESIK


def test_uydurulmus_atif_dogrulanmadi_isaretlenir():
    """Faz 0 · base id=16: "4711 Sayılı Türk Hakemlik Kanunu" — var olmayan kanun."""
    metin = "Karşı oy yer almaz. 4711 Sayılı Türk Hakemlik Kanunu'nun 33. maddesi."
    _, atiflar = siniflandir(metin, kaynaklar=(IS_K_31,), finish_reason="stop")
    assert atiflar, "atıf çıkarılamadı"
    assert all(not a.dogrulandi for a in atiflar), "getirilen kaynakta olmayan atıf doğrulanmış"


def test_kaynaktaki_atif_dogrulanir():
    metin = "İş Kanunu Madde 31 uyarınca sözleşme askıya alınır."
    _, atiflar = siniflandir(metin, kaynaklar=(IS_K_31,), finish_reason="stop")
    assert any(a.dogrulandi for a in atiflar)
```

- [ ] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör**

Run: `python -m pytest tests/test_terazi.py -v` → `FAIL` (`No module named 'hakhukuk.terazi'`)

- [ ] **Adım 3: Uygulama**

```python
# hakhukuk/terazi.py
"""suskunluk_terazisi — ürün yüzeyi.

⚠️ NEDEN VAR (üç kez ölçüldü, üçünde de alet FAZLA RED saydı):
   2026-09-06  bizim şablon, önsözsüz    alet 14 → göz  8   (ADR-0061)
   2026-09-06  Gemini şablonu, F0.4      alet 11 → göz  7
   2026-09-07  kör mod, iki kol          alet  6 → göz  0   (6/6 yanlış pozitif)

Kök sebep: "…bulunmamaktadır" ailesi hukuk metninde İKİ iş görür —
  (a) "kaynakta yok, cevaplayamam"  = çekinme
  (b) "kanunda böyle bir hüküm yok" = ESASA İLİŞKİN CEVAP
Metne tek başına bakan bir sınıflandırıcı bunları ayıramaz. Bu modül `kaynaklar`ı da
görür: kaynak YOKSA (a) mümkündür, kaynak VARSA (b) çok daha olasıdır.
"""
import os
import re
import sys

from hakhukuk.tipler import Atif, Durum, Kaynak

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from score_abstention import REJECT_RE  # noqa: E402  — TEK KAYNAK, kopyalanmaz

# "Kanunda hüküm yok" kalıbı: olumsuzlama + hemen ardından bir madde/kanun atfı.
# Bu birleşim bir CEVAPTIR; tek başına olumsuzlama değildir.
_ESASA_ILISKIN = re.compile(
    r"(bulunmamakta|belirtilmemiş|yer almaz|düzenlenmemiş)", re.IGNORECASE)
_ATIF = re.compile(
    r"(?:(\d{3,5})\s*[Ss]ayılı[^.]{0,60}?)?"
    r"(?:madde|md\.?)\s*[:\s]*([0-9]+(?:/[a-zA-Z])?)", re.IGNORECASE)


def _atiflari_cikar(metin: str, kaynaklar: tuple[Kaynak, ...]) -> tuple[Atif, ...]:
    """Metindeki madde atıflarını çıkar ve GETİRİLEN kaynaklara karşı doğrula.

    Doğrulama deterministik: atıf, getirilen kaynakların kimlik kümesinde varsa doğrudur.
    Yoksa `dogrulandi=False` — bu, kullanıcıya UYARIYLA gösterilir, sessizce geçilmez.
    """
    kimlikler = {k.kimlik for k in kaynaklar}
    kanunlar = {k.kanun_no for k in kaynaklar}
    out: list[Atif] = []
    for kanun_no, madde in _ATIF.findall(metin):
        kn = kanun_no or (next(iter(kanunlar)) if len(kanunlar) == 1 else "")
        mn = f"Madde {madde}"
        out.append(Atif(kanun_no=kn, madde_no=mn, dogrulandi=f"{kn}/{mn}" in kimlikler))
    return tuple(out)


def siniflandir(
    metin: str, kaynaklar: tuple[Kaynak, ...], finish_reason: str
) -> tuple[Durum, tuple[Atif, ...]]:
    """Cevabı dört durumdan birine ayır ve atıflarını doğrula.

    Yan etkisi yok, idempotent. `finish_reason` üretimden GELDİĞİ GİBİ verilir —
    "length" sessizce yutulmaz (Faz 0: yarım cümle teslim edilmişti).
    """
    atiflar = _atiflari_cikar(metin, kaynaklar)

    if finish_reason == "length":
        return Durum.KESIK, atiflar

    red = bool(REJECT_RE.search(metin))
    esasa = bool(_ESASA_ILISKIN.search(metin))

    if red and not kaynaklar:
        # Kaynak yok ⇒ "kaynakta yok, cevaplayamam" okuması MÜMKÜN.
        return Durum.SUSKUNLUK, atiflar
    if red and kaynaklar and not atiflar:
        # Kaynak var ama model hiçbirine dayanmadı ⇒ gerçek çekinme.
        return Durum.SUSKUNLUK, atiflar
    if esasa or any(not a.dogrulandi for a in atiflar):
        # Olumsuz hüküm ya da doğrulanamayan atıf ⇒ çekinceli: cevap gibi görünür, tam değildir.
        return Durum.CEKINCELI, atiflar
    return Durum.CEVAP, atiflar
```

- [ ] **Adım 4: Testi koş, GEÇTİĞİNİ gör**

Run: `python -m pytest tests/test_terazi.py -v` → **5 passed**
⚠️ Geçmiyorsa **eşiği değil sınıflandırıcıyı** düzelt; testler Faz 0'ın **gerçek** vakaları.

- [ ] **Adım 5: 🚨 REGRESYON KAPISI — 80 gerçek kalemde alet ↔ göz**

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
    # ⚠️ Sahte kaynak GERÇEK bir Kaynak olmalı: _atiflari_cikar `.kimlik` okuyor.
    #    `object()` verirsek AttributeError — testte değil, kapıda patlar.
    sahte = (Kaynak(kanun_adi=r.get("kanun_adi", ""), kanun_no=str(r.get("kanun_no", "")),
                    madde_no=r.get("madde_no", ""), metin="", sira=1),) if kaynak_var else ()
    d, _ = siniflandir(r["cevap"] or "", kaynaklar=sahte,
                       finish_reason=r.get("finish_reason") or "stop")
    sayim[d] += 1
for d, n in sayim.items():
    print(f"{d.name:<11} {n}")
print("\n⚠️ GÖZ çıpası (F0.3, 80/80 okundu): aşırı-red 4/80")
PY
```
`verify:` `SUSKUNLUK` sayısı **4/80 göz çıpasına yakın**. Sapma **> 2 kalemse** her fark eden
kalem **id'siyle listelenir ve gözle okunur** — sayı düzeltilmeden devam edilmez.

- [ ] **Adım 6: Commit**

```bash
git add hakhukuk/terazi.py tests/test_terazi.py && \
git commit -m "A8: suskunluk_terazisi ürün yüzeyine taşındı — sınıflandırıcı artık kaynağı da görüyor"
```

---

### Görev 8: İndeks dağıtımı 🔓 **AÇIK KARAR S8**

**Dosyalar:** Create: `hakhukuk/kurulum.py` · `tests/test_kurulum.py`

**Ölçülmüş girdiler (2026-09-07):**
- `data/index/mevzuat_bge_m3_s2/` = **80 MB** (tek dosya `gomme.npy` 82,9 MB + `KUNYE.json`)
- `.gitignore:166` → `data/index/**/*.npy` ⇒ ikili **git'te YOK**, yalnız künye takipli
- Korpus `data/corpus/mevzuat_maddeler.jsonl` = **37 MB**, git'te **VAR**
- Yeniden üretim: `bge-m3` ile **40.496 madde** gömülür — CPU'da **~2 sa 45 dk**, GPU'da ~10 dk

⇒ Kullanıcı indeksi repodan **alamıyor**. İki seçenek: **(a)** HF dataset'ten indir ·
**(b)** kurulumda üret. ⛔ **İnsan kararı olmadan bu görev başlamaz.**

- [ ] **Adım 1: Kararı al ve `docs/open_questions.md` S8'e işle** *(kod yok)*
`verify:` S8 satırı `✅ KAPANDI → (a)` ya da `(b)` diyor, gerekçesiyle.

- [ ] **Adım 2: Failing test yaz** — karar (a) ise indirme + `sha256` doğrulama, (b) ise
üretim + `KUNYE.json` eşleşmesi sınanır. ⚠️ İki durumda da test **künye eşleşmesini** sınar:
indeksin `KUNYE.json`'u korpusun sürümüyle uyuşmuyorsa `recall@10` sessizce düşer.

- [ ] **Adım 3-5: Uygulama · test yeşil · commit**

🔒 **BU ADIMLAR BİLEREK BOŞ — S8 kapanmadan yazılamazlar.** İki seçenek **farklı kod** ister:
- **(a) HF dataset:** `huggingface_hub.hf_hub_download` + `sha256` doğrulama + yeni bağımlılık
- **(b) kurulumda üret:** `bge-m3` yükle + 40.496 madde göm + `KUNYE.json` yaz (**~2 sa 45 dk
  CPU** / ~10 dk GPU) — yeni bağımlılık yok, ama kurulum saatlerce sürer

⛔ Şimdi ikisinden birini yazmak, insana ait bir kararı **sessizce** vermek olur.
Karar gelince adımlar bu görevin içine, tam koduyla yazılır.

---

### Görev 9: Servis katmanı — `answer(soru) → Cevap` (**tek derin modül**)

**Dosyalar:** Create: `hakhukuk/servis.py` · `tests/test_servis.py`
**Bağımlılık:** Görev 5 · 6 · 7 · 8

**Arayüzler:**
- Tüketir: `hakhukuk.istem` · `hakhukuk.tipler` · `hakhukuk.terazi` · `scripts/retriever.py`
- Üretir: `answer(soru: str, *, k: int = 10) -> Cevap` — Görev 10 (CLI) ve 12 (TUI) **yalnız
  bunu** çağırır

**Tasarım (POSD derin modül):** Arayüz **tek fonksiyon**; arkasında retriever + llama-server +
istem + terazi **gizli**. ⛔ Harness **GPU'ya girmez** — embedder CPU'da, indeks CPU RAM'de;
*"sığar/sığmaz"* farkı budur.

- [ ] **Adım 1: Failing test yaz — sunucusuz, sahte taşıyıcıyla**

```python
# tests/test_servis.py
from hakhukuk import servis
from hakhukuk.tipler import Durum, Kaynak

IS_K_31 = Kaynak(kanun_adi="İŞ KANUNU", kanun_no="4857", madde_no="Madde 31",
                 metin="Muvazzaf askerlik ödevi dışında …", sira=1)


def test_answer_kaynaklari_ve_atiflari_dondurur(monkeypatch):
    monkeypatch.setattr(servis, "_getir", lambda soru, k: (IS_K_31,))
    monkeypatch.setattr(servis, "_uret",
                        lambda mesajlar: ("İş Kanunu Madde 31 uyarınca askıya alınır.", "stop"))
    c = servis.answer("Askerlik nedeniyle iş sözleşmesi ne olur?")
    assert c.durum is Durum.CEVAP
    assert c.kaynaklar == (IS_K_31,)
    assert any(a.dogrulandi for a in c.atiflar)


def test_answer_bos_getirmede_susar(monkeypatch):
    """Retriever boş dönerse model konuşturulmaz — üründe M5 koşulu OLUŞMAMALI."""
    monkeypatch.setattr(servis, "_getir", lambda soru, k: ())
    c = servis.answer("İlgisiz soru")
    assert c.durum is Durum.SUSKUNLUK
    assert c.kaynaklar == ()


def test_answer_kesigi_gizlemez(monkeypatch):
    monkeypatch.setattr(servis, "_getir", lambda soru, k: (IS_K_31,))
    monkeypatch.setattr(servis, "_uret", lambda mesajlar: ("Yarım cüm", "length"))
    assert servis.answer("x").durum is Durum.KESIK
```

- [ ] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör**

Run: `python -m pytest tests/test_servis.py -v` → `FAIL`

- [ ] **Adım 3: Uygulama**

```python
# hakhukuk/servis.py
"""Ürünün tek derin modülü: answer(soru) → Cevap.

Arayüz tek fonksiyon; retriever, llama-server, istem ve terazi ARKASINDA gizli.
⛔ Harness GPU'ya GİRMEZ (embedder CPU, indeks CPU RAM/disk) — "sığar/sığmaz" farkı budur.

⚠️ Retriever boş dönerse model ÇAĞRILMAZ. Sebebi ölçülmüştür: kaynaksız (M5) koşullarda
model kendinden emin ve YANLIŞ hukuk üretiyor (2026-09-07: İş K. 31 → "35. ve 36. madde",
İİK 79/a → "110. madde", TBK 230 → "6502 Sayılı Tüketici Kanunu"). Üründe bu koşul
OLUŞMAMALIDIR.
"""
from hakhukuk.istem import SISTEM_COK_KAYNAK
from hakhukuk.terazi import siniflandir
from hakhukuk.tipler import Cevap, Durum, Kaynak

VARSAYILAN_K = 10          # ADR-0068 · RRF_K=10 ile ölçülen recall@10 = 0,9500
DUSUNCE_BUTCESI = 1024     # ⚠️ Üründe cevap bütçesinden AYRI (Faz 0: paylaşımlı havuz
CEVAP_BUTCESI = 1024       #    düşünceye yanıp cevaba 3 karakter bırakmıştı)


def _getir(soru: str, k: int) -> tuple[Kaynak, ...]:
    """Hibrit BM25 + bge-m3, RRF ile füzyon. CPU'da çalışır."""
    import os
    import sys
    sys.path.insert(0, os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
    import retriever  # noqa: PLC0415 — ağır bağımlılık, ithalat gecikmeli
    ham = retriever.getir(soru, k=k)
    return tuple(
        Kaynak(kanun_adi=h["kanun_adi"], kanun_no=str(h["kanun_no"]),
               madde_no=h["madde_no"], metin=h["metin"], sira=i + 1)
        for i, h in enumerate(ham)
    )


def _uret(mesajlar: list[dict]) -> tuple[str, str]:
    """llama-server'a tek istek. Döner: (metin, finish_reason)."""
    raise NotImplementedError("Adım 4'te doldurulacak")


def answer(soru: str, *, k: int = VARSAYILAN_K) -> Cevap:
    """Bir soruya kaynaklı, atıfları doğrulanmış cevap üret.

    Boş getirmede model çağrılmaz; dürüst suskunluk döner.
    """
    kaynaklar = _getir(soru, k)
    if not kaynaklar:
        return Cevap(
            metin="Elimdeki mevzuat kaynaklarında bu soruyu karşılayan bir hüküm bulamadım. "
                  "Güncel mevzuata veya bir avukata danışmanızı öneririm.",
            durum=Durum.SUSKUNLUK, atiflar=(), kaynaklar=())

    blok = "\n\n".join(
        f"[KAYNAK {s.sira}] {s.kanun_adi} {s.madde_no}\n{s.metin[:900]}" for s in kaynaklar)
    mesajlar = [{"role": "system", "content": SISTEM_COK_KAYNAK},
                {"role": "user", "content": f"KAYNAKLAR:\n{blok}\n\nSORU: {soru}"}]
    metin, finish = _uret(mesajlar)
    durum, atiflar = siniflandir(metin, kaynaklar, finish)
    return Cevap(metin=metin, durum=durum, atiflar=atiflar, kaynaklar=kaynaklar)
```

⚠️ `retriever.getir` **imzasını TAHMİN ETME** — `scripts/retriever.py`'yi aç, gerçek fonksiyon
adını ve dönüş şeklini oku, koda **onu** yaz. Bu turda üç kez yanlış imza/bayrak çıktı.
⚠️ `--max-chunk-chars 900` ölçüm rejiminin değişmezidir; `[:900]` kırpması onunla **aynı** olmalı.

- [ ] **Adım 4: `_uret`'i doldur** — `llama-server`'a `/v1/chat/completions`,
`temperature=0`, `seed=3407`, `max_tokens=DUSUNCE_BUTCESI + CEVAP_BUTCESI`.
`verify:` `python -m pytest tests/test_servis.py -v` → **3 passed**.

- [ ] **Adım 5: 🚨 UÇTAN UCA KAPI — gerçek sunucuyla 3 soru**

`verify:` üç soruda da `durum` ∈ {`CEVAP`, `CEKINCELI`} · `kaynaklar` boş değil ·
her `dogrulandi=True` atıf gerçekten getirilen kaynaklarda **var** (gözle doğrulanır).

- [ ] **Adım 6: Commit**

---

### Görev 10: CLI + sorumluluk ibaresi 🔓 **AÇIK KARAR S10**

**Dosyalar:** Create: `hakhukuk/cli.py` · `tests/test_cli.py` · Modify: `pyproject.toml`

**Arayüzler:** Tüketir `servis.answer` · Üretir `hakhukuk` konsol komutu

⛔ **S10 (Avukatlık Kanunu / sorumluluk sınırı) hukukçu görüşü gerektiriyor ve repoda hiç
değerlendirilmemiş.** ⚠️ Ama S10'un açık olması **ibarenin girmesini engellemez** — açık olan
*"metnin tam olarak ne diyeceği"*dir. Bir ilk metinle başlanır, hukukçu görüşü gelince
**tek yerden** güncellenir.

- [ ] **Adım 1: Failing test yaz**

```python
# tests/test_cli.py
import subprocess
import sys


def test_cli_sorumluluk_ibaresini_HER_cevapta_basar():
    r = subprocess.run([sys.executable, "-m", "hakhukuk.cli", "--kuru-calisma", "test"],
                       capture_output=True, text=True)
    assert r.returncode == 0
    assert "hukuki tavsiye değil" in r.stdout.lower()


def test_cli_dort_durumu_ayirt_edilebilir_basar():
    r = subprocess.run([sys.executable, "-m", "hakhukuk.cli", "--durumlari-listele"],
                       capture_output=True, text=True)
    for ad in ("CEVAP", "CEKINCELI", "SUSKUNLUK", "KESIK"):
        assert ad in r.stdout
```

- [ ] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör** → `FAIL`

- [ ] **Adım 3: Uygulama** — `argparse`; çıktıda **durum rozeti** · cevap · **atıflar
(doğrulanmamış olanlar ⚠️ ile)** · kaynak listesi · **sorumluluk ibaresi**.
⛔ İbare koşullu **değildir**: `Durum` ne olursa olsun basılır.

- [ ] **Adım 4: Testi koş, GEÇTİĞİNİ gör** → **2 passed**

- [ ] **Adım 5: Commit**

---

### Görev 11: Yeniden üretim yolu — tek komut

**Dosyalar:** Create: `scripts/yeniden_uret.sh` · `docs/YENIDEN_URETIM.md`

**Neden:** Yayımlanan kütle (**%80,1**) bugün **hiç kimse tarafından yeniden üretilemez** —
istem `gen_eval_grounded.py` içindeydi (Görev 5 çözdü), indeks git'te yok (Görev 8 çözecek),
ve komut zinciri hiçbir yerde **tek parça** yazılı değil.

- [ ] **Adım 1: Zinciri yaz** — indeks hazırla → llama-server aç → `h1` üret →
geçerlilik kapısı → puanla → `harness_tablo.py`.
`verify:` script `bash -n` temiz; her adım künyeye **ne yazdığını** basıyor.

- [ ] **Adım 2: 🚨 TEMİZ MAKİNE KAPISI** — `git clone` + `uv sync` + tek komut.
`verify:` üretilen kütle **%80,1 ± 0,3 p** (hakem gürültü tabanı). ⛔ Dışındaysa **DUR**;
fark **kaynaklanmadan** yayımlanmaz.

- [ ] **Adım 3: Commit**

---

### Görev 12: Basit TUI (`textual`)

**Dosyalar:** Create: `hakhukuk/tui.py` · `tests/test_tui.py` · Modify: `pyproject.toml`
**Bağımlılık:** Görev 9 · 10

⚠️ **`textual` kurulu DEĞİL** (ölçüldü 2026-09-07: `ModuleNotFoundError`). Yeni bağımlılık ⇒
gerekçe: tek ekranlı arayüzü elle yazmak `prompt_toolkit`/`curses` seviyesinde **kendi
mantığını** doğurur; `textual` bunu hazır veriyor ve `answer()`'ın üstünde **ince kabuk**
kalmasını sağlıyor.
⛔ **Web arayüzü, API sunucusu, hesap/oturum DEĞİL** — onlar `v2` (S9).

- [ ] **Adım 1: Bağımlılığı ekle ve sürümü PİNLE**
`verify:` `python -c "import textual; print(textual.__version__)"` çalışıyor · `pyproject.toml`'da
**tam sürüm** yazılı.

- [ ] **Adım 2: Failing test** — TUI'nin **kendi mantığı olmadığını** sınar:

```python
# tests/test_tui.py
import inspect

from hakhukuk import tui


def test_tui_kendi_mantigi_yok_yalnizca_answer_cagirir():
    """TUI ince kabuktur. Sınıflandırma/atıf mantığı BURAYA sızarsa iki yerde bakım olur."""
    kaynak = inspect.getsource(tui)
    for yasak in ("REJECT_RE", "re.compile", "siniflandir(", "_getir(", "_uret("):
        assert yasak not in kaynak, f"TUI'ye mantık sızmış: {yasak}"
    assert "answer(" in kaynak
```

- [ ] **Adım 3: Testi koş, BAŞARISIZ olduğunu gör**

Run: `python -m pytest tests/test_tui.py -v` → `FAIL` (`No module named 'hakhukuk.tui'`)

- [ ] **Adım 4: Uygulama — ince kabuk**

```python
# hakhukuk/tui.py
"""Tek ekranlı terminal arayüzü. answer() üstünde İNCE KABUK — kendi mantığı YOKTUR.

⚠️ Sınıflandırma/atıf mantığı buraya sızarsa iki yerde bakım olur ve ikisi sessizce
ayrışır (bkz. istem sürüklenmesi, S18: aynı metin beş dosyada, ikisi farklıydı).
tests/test_tui.py bunu bir KAPI olarak sınar.
"""
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header, Input, Static

from hakhukuk.cli import SORUMLULUK_IBARESI
from hakhukuk.servis import answer
from hakhukuk.tipler import Durum

ROZET = {
    Durum.CEVAP: "🟢 CEVAP",
    Durum.CEKINCELI: "🟡 ÇEKİNCELİ CEVAP — doğrudan hüküm bulunamadı",
    Durum.SUSKUNLUK: "⚪ SUSKUNLUK — dayanak bulunamadı",
    Durum.KESIK: "🟠 KESİK — üretim bütçesi bitti, cevap YARIM",
}


class HakHukukTUI(App):
    TITLE = "HakHukuk"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Hukuki sorunuzu yazın…", id="soru")
        yield VerticalScroll(Static("", id="cikti"))
        yield Footer()

    def on_input_submitted(self, olay: Input.Submitted) -> None:
        c = answer(olay.value)
        atif = "\n".join(
            f"  {'✅' if a.dogrulandi else '⚠️ DOĞRULANAMADI'} {a.kanun_no} {a.madde_no}"
            for a in c.atiflar) or "  (atıf yok)"
        kaynak = "\n".join(f"  {k.sira}. {k.kanun_adi} {k.madde_no}" for k in c.kaynaklar)
        self.query_one("#cikti", Static).update(
            f"{ROZET[c.durum]}\n\n{c.metin}\n\nATIFLAR:\n{atif}\n\n"
            f"KAYNAKLAR:\n{kaynak}\n\n{SORUMLULUK_IBARESI}")


def main() -> None:
    HakHukukTUI().run()
```

⚠️ `SORUMLULUK_IBARESI` **Görev 10'da** `hakhukuk/cli.py`'de tanımlanır ve buradan **import
edilir** — iki yere yazılmaz (S18'in dersi).

- [ ] **Adım 5: Testi koş, GEÇTİĞİNİ gör**

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

- [ ] **Adım 1: `PRODUCT.md`** — vatandaş kim · hangi soruyu soruyor · cevap neye benziyor ·
**VAAT ETMEDİĞİ** (hukuki tavsiye değil · güncellik indeksin işi · %100 doğruluk değil) ·
`v1`↔`v2` sınırı · üç maddeli kapı · iki sürüm şeması.
`verify:` her nicelik yanında **kaynak dosya adı** taşıyor · *"vaat etmiyor"* bölümü var.

- [ ] **Adım 2: `ROADMAP.md`** — bu planın fazları: `HP` → Hat A ∥ → Faz 3 → Hat B → `v1.0` → `v2`.
Her adım: *ne · neden (**hangi ölçülmüş boşluk**) · `verify:` · bedel · bağımlılık*.
`verify:` kritik yol işaretli · **AÇIK KARAR** damgaları **S5·S7·S8·S9·S10·S12·S16·S17·S18**.

- [ ] **Adım 3: `TODO.md`** — yalnız **bugün koşulabilir** kalemler; her satır bir `ROADMAP`
adımına bağlı. `verify:` her satırda bağlantı var.

- [ ] **Adım 4: `docs/MIMARI.md`** — `v1` zinciri: base → kollar → merge → GGUF → retriever →
istem → `answer()` → CLI/TUI · `v2` sınırı. `referans-design-doc.md`'nin işlevini devralır.
`verify:` her kutu **var olan bir dosyaya** ya da bir `ROADMAP` adımına işaret ediyor
(döngüyle sınanır, gözle değil).

- [ ] **Adım 5: Kırık link onarımı — ⛔ TARİHSEL KAYITLARA DOKUNMA**

Güncellenir: `CLAUDE.md` · `MODEL_CARD.md` · `README.md` · `README.tr.md` · `DEVIR-PROMPT.md`.
⛔ **Güncellenmez:** `docs/record/**` · `docs/adr/**` — *"o gün şu belge şunu diyordu"* kaydı;
spec §11'in ilk kuralı **KAYIT TEMİZLENMEZ**.
`verify:` `grep -rE '(ROADMAP|TODO|TASARIM|VISION|PAPER_TARGET)\.md' CLAUDE.md README*.md MODEL_CARD.md`
çıktısındaki her yol **var olan** bir dosyayı gösteriyor · `git diff --stat docs/record docs/adr`
→ **0 değişiklik**.

- [ ] **Adım 6: `MODEL_CARD.md` tam yazımı** — bugün yalnız *"ESKİ BİRİM"* bandı çakılı.
Yeni manşet · üç maddeli kapının **sayıları** · `HakHukuk-4B-v1.0-Q4_K_M.gguf` ad kuralı
(ADR-0071) · VRAM tablosu (3,09 / 3,70 / 5,76 GiB) · **Limitations**: üç kabul edilen bedel
(dış geçerlilik · kapasite sorusu · ADR-0018'in eğrisi) + **tek aile hakem** borcu.
`verify:` kartta *"ESKİ BİRİM"* bandı **kalmadı**; her sayının yanında kaynak dosya var.

- [ ] **Adım 7: `v0.2` etiketi + commit**

---

# FAZ 4 · Hat B — model (~$7-15, Modal) → `v1.0`

⛔ **`HP` (Görev 3) bitmeden başlamaz.** Sebebi ADR-0064'ün kendi *"Ne KURULMAZ"* maddesi:
bugünkü her sayı tek ailenin hükmü; kapıyı **panelsiz** koşmak aynı borcu `v1.0`'a taşır.

---

### Görev 14: `B1` — isabetsizlik, reddetme-örneklemesi (~$5)

**Neden:** Faz 0'da **ilk kez gözle** sayıldı: **8/80**. B10 (aşırı-red) 4/80'e indi ⇒ **B1
artık birinci sıradaki eksen**. ⚠️ Ve **otomatik vekil metrik YOK**: `faithfulness < 0,6`
süzgeci 4 buluyor, *"altın madde atıflarda yok"* süzgeci 3 — **göz 8** buluyor (ADR-0066).

**Alet HAZIR:** `scripts/b10_hasat.py` · Modal `harvest_b10` (ADR-0047 m.2, L4'te doğrulanmış) ·
sızıntı süzgeci (13.350 → 12.914, konteynerde bayt-özdeş). ⛔ **Yeniden kurulmaz.**

- [ ] **Adım 1: Ön-kayıt — hedef bandı ve durma kuralı, KOŞUDAN ÖNCE**
`verify:` ADR'de hedef bant, durma kuralı ve *"kaç kalem kazanç $X'e değer"* eşiği yazılı.
⚠️ B10 turunun dersi: hedef **iki kalemlik** bir boşluğa daralmıştı ve tur **kapatıldı**.

- [ ] **Adım 2: Hasat** (Modal, AYRIK) — `verify:` kabul oranı + sızıntı süzgeci sayıları künyede.
- [ ] **Adım 3: Eğitim** — `--fresh-adapter` **ZORUNLU** (`τ = θ_ft − θ_base`; adaptörden devam
etmek **ardışık SFT** üretir, task-vector değil). `verify:` künyede `fresh_adapter: true`.
- [ ] **Adım 4: Merge (ham TIES) + GGUF** — `verify:` `‖τ‖` ölçüldü ve `kollar.md`'ye satır eklendi.
- [ ] **Adım 5: Ölç + GÖZLE OKU** — `verify:` isabetsizlik **gözle** sayıldı; alet↔göz deltası yazıldı.
- [ ] **Adım 6: Commit + `kollar.md` + `research_log`**

---

### Görev 15: `B4` — `τ_a` genliği (~$1,3) + `YB2` M2b

**Neden (ölçüldü):** merge'de `τ_a` **0,987 → 0,766** seyreliyor (−22,1 p). Teşhis **genlik**:
70 adım @1e-5 → `‖τ_a‖` **1,1806** ↔ `‖τ_g‖` **10,4722**, oran **8,87×**.
Kaldıraç: **aynı ORPO ile daha çok adım / daha yüksek lr**.
⛔ Yöntemi de değiştirmek **iki değişkeni birlikte** oynatır (ADR-0017).

- [ ] **Adım 1: Ön-kayıt** — hangi `‖τ_a‖` değeri hedefleniyor, hangi M2b eşiği bekleniyor.
- [ ] **Adım 2: Eğitim** (`--fresh-adapter`) — `verify:` `‖τ_a‖` **ölçüldü ve raporlandı**.
- [ ] **Adım 3: Merge + M2b ölçümü** — `verify:` merge sonrası M2b **yeni çıpanın üstünde**.
- [ ] **Adım 4: Commit**

---

### Görev 16: `v1.0` kapı koşusu (~$1) + kabul testi

⛔ **DONMUŞ TEST BURADA, TEK KEZ AÇILIR** (`data/eval/canon/`).

- [ ] **Adım 1: DEV'de üç maddeyi yeniden koş** — ADR-0064 + **ADR-0074**'ün (panel) bağlayıcı
okumasıyla. `verify:` üç madde de sayıyla; **her sayım adımında gözle okuma**.
- [ ] **Adım 2: Kabul testi — donmuş TEST**
⚠️ **ADR-0069 raporlaması zorunlu:** ham kütle **manşet ve bağlayıcı**; yanına **tek** tanısal
oran `tavan kullanımı = kütle ÷ recall@10`; **her iki setin `recall@10`'u yanında zorunlu**.
⛔ Rakip kıyas cümlesi bu orandan **KURULMAZ**. TEST'in tavanı **≈%75**, DEV'inki **%95**.
`verify:` `OZET.md` ham kütleyi manşet yapıyor; tavan görünmeden oran yayımlanmamış.
- [ ] **Adım 3: Hüküm** — geçerse **`v1.0`** + `HakHukuk-4B-v1.0-Q4_K_M.gguf` (ADR-0071).
Geçmezse sayı **damgalanarak yayımlanır** ve `v0.x` devam eder (ADR-0065).
`verify:` hüküm ADR'de, `research_log`'da ve `MODEL_CARD.md`'de **aynı sayıyla** duruyor.
- [ ] **Adım 4: Commit + etiket**

---

## ⏭️ Bu planın DIŞINDA

- **T5** `scripts/` alt-klasör düzeni — **Faz 0 planı Görev 9**'da yazılı, 8 adım.
  ⚠️ Görev 5 Adım 6'nın **ön koşulu** T5 Adım 2'dir (`sys.path` deseni).
- **T1** `models/` ~20 GB — ön koşulu **AÇIK KARAR S7**.
- **S17** kuantizasyon eğrisi · **S9** `v2` barındırma · **Hat C** metodoloji paper'ı.
- 🆕 **`exact_reject`'in kör mod dalı** — *"…bulunmamaktadır"* ailesi kör modda red sayılmamalı.
  ⛔ Faz 0'da **bilerek düzeltilmedi** (kapının sayısı üretildikten sonra aleti değiştirmek
  ADR-0050'nin sınırında). Sıradaki turda **koşudan ÖNCE** düzeltilir.
- 🆕 **`recall_taban.json`** — Faz 0'ın tek *"kaynaklanmadı"* ihlali; ölçüm mevcut rejimde
  ($0, ~15 dk) yeniden koşulup dosya **gerçekten** üretilir.
