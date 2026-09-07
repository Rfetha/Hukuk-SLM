# HakHukuk

> # 🚨 SAYILAR 2026-09-07'DE DEĞİŞTİ — AŞAĞIDAKİLER ESKİ BİRİMDEDİR
>
> Bu belgedeki **her** kütle/aşırı-red/A1 sayısı **v1 soru seti · `RRF_K=60` · 1024 üretim
> bütçesi** birimindedir ve bugünkü sayılarla **KIYASLANAMAZ**. Faz 0 ölçüm zinciri aletin
> dört kusurunu buldu (soru seti · füzyon · DEV↔TEST bileşimi · **rakiple eşit olmayan üretim
> bütçesi**) ve **model ağırlıklarına hiç dokunmadan** sayılar değişti:
>
> | eksen | bu belgede (eski) | **ölçülen (v2 birimi)** |
> | :--- | ---: | ---: |
> | sadık-cevap kütlesi | %68,4 | **%80,1** |
> | `recall@10` | 0,875 | **0,9500** |
> | aşırı-red | 9/80 | **4/80** |
> | uydurulmuş madde | 0/83 | **0/114** |
>
> ⛔ **Bu belgedeki rakip kıyas cümleleri geçersizdir.** Eşit sınavda ölçülen yeni tablo:
> BİZ **0,8011** ↔ 3.1 FL 0,7058 ↔ 3.5 FL 0,7622 ↔ **3.5 Flash 0,7425** (bağlayıcı GÖZ-katı
> okuması). `v1.0` kapısı madde (1) **geçildi**.
>
> Kaynaklar: [`research_log #62`](docs/record/research_log/2026-09-06-faz0-olcum-zinciri.md) ·
> [ADR-0064](docs/adr/0064-v1-kapisi-uc-maddeli-on-kayit.md) ·
> [ADR-0067](docs/adr/0067-soru-onarimi-dev-test-v2.md) ·
> [ADR-0068](docs/adr/0068-rrf-k-60-to-10.md) ·
> [ADR-0070](docs/adr/0070-uretim-butcesi-esitlendi.md) ·
> [`f04-rakip-onsozsuz/KALIBRASYON_ve_OZET.md`](outputs/eval/f04-rakip-onsozsuz/KALIBRASYON_ve_OZET.md)
>
> **Bu belge belge-katmanı turunda yeniden yazılacak; bant o zaman kalkar.**


**A Turkish legal assistant small enough to run on a laptop — built to say "I don't know".**

[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[Model card](MODEL_CARD.md) · `ROADMAP.md` ⚰️ *(2026-09-06'da silindi → [güncel plan](docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md); yeniden yazımı **Görev 13**)* · [Türkçe](README.tr.md)

---

Most of the work in a legal assistant is not answering. It is **refusing to answer
when the sources don't support one.** A confident, wrong article number is worse
than silence — it is the failure mode that makes a legal tool dangerous.

HakHukuk is a 4B model (2.59 GiB, Q4_K_M) trained for both halves of that job:
ground the answer in the supplied statute, and abstain when the statute doesn't
cover the question.

> ### ⚠️ Not legal advice
> This is a research artifact. It is not a lawyer and its output is not legal
> advice. Legislation changes; weights do not. **The retrieval layer exists and is
> measured, but it is not yet packaged into the serving path below** — you still
> supply the statute text yourself. Verify every article number against
> [mevzuat.gov.tr](https://www.mevzuat.gov.tr).

## Where it stands

DEV split, harness off, judge `gpt-4o-mini`. Full protocol in the [model card](MODEL_CARD.md).

| | faithful-answer mass ↑ | over-refusal ↓ | refusal on missing sources ↑ | tok/answer ↓ |
| :--- | ---: | ---: | ---: | ---: |
| bare base | 56.7% | 0.425 | 0.961 ᴷ³ | 1192 |
| **HakHukuk-4B-v0.1** | **71.6%** | **0.212** | **0.766** ᴷ³ | **714** |
| Gemini 3.1 Flash-Lite | 72.9% | 0.237 | 0.883 ᴷ³ | — |

ᴷ³ **M2b re-scored 2026-08-06.** The old numbers were produced with a denominator the
judge decided **while looking at the model's answer** — so the same exam yielded a different
denominator per model. The denominator is now answer-blind and identical across arms
(`valid_traps` 61…80 → **77** on this exam). Old values are kept in
[`#57`](docs/record/research_log/2026-08-06-cekinme-aleti-onarimi.md), which carries the full
conversion table: base `0.986 → 0.961` · ours `0.877 → 0.766` · Gemini FL `1.000 → 0.883`.
⚠ **The M2/A1 columns have NOT been re-scored** and still carry the model-dependent denominator.

We reach **98% of Flash-Lite's faithful-answer mass and refuse less often than it
does**, at 2.59 GiB and ~zero marginal cost. We are still behind it on refusing
when only distractor sources are present (0.766 vs 0.883 — the gap narrowed
from 12.3 to 11.7 points once the denominator was fixed, but the sign did not change).

**This is not a parity claim:** the harness is off, cost is not normalized, and
the merge configuration was selected on DEV.

### With the harness on — the honest product number

The table above hands the model the right article. A real user has no such luxury.
With a retriever choosing the context instead (hybrid BM25 + `bge-m3`, 40,496-article
index, k=10, CPU-only) and the **source-sufficiency preamble** in the system prompt
(main protocol since [ADR-0058](docs/adr/0058-b-i-kaynak-yeterliligi-onsozu-benimsendi.md)):

| | harness OFF | **harness ON — official** | ON, no-preamble *ablation* |
| :--- | ---: | ---: | ---: |
| gold article in context | guaranteed *by construction* | **70/80 — recall@10 0.875** | 70/80 — identical |
| coverage | 0.788 | **0.8250** ~~0.7625~~ | **0.9000** ~~0.7625~~ |
| faithful-answer mass | 71.6% | **68.4%** ~~62.8%~~ | **73.0%** ~~61.3%~~ |
| A1 (answered-only) | 0.909 | **0.8288** | 0.8110 |
| A1, gold-retrieved subset | 0.909 | **0.8729** | 0.8593 |
| **fabricated article numbers** | 0 | **0 / 83** | 0 / 118 |
| abstains with gold in context ↓ | 17/80 | **9/80** ~~14/80~~ | **5/80** ~~16/80~~ |
| answers from a *different real* article ↓ | — | **5/80** | 7/80 |

> 🚨 **Rescored 2026-09-06 — the abstention detector was broken, and it penalised only us.**
> In the no-opening-verdict branch `exact_reject` scanned the *whole* answer, so our answer
> template's discarded-sources rationale (*"the other sources do **not contain** …"*) tripped
> the refusal regex. Gemini's answers carry that phrase in only 3/80 cases, so the bug was
> **specific to our own training template**. Repairing it moved **our** numbers and left the
> competitor's untouched (measured, not assumed).
> Reading 80 items **by eye** gives **8/80** abstentions-with-gold and 69.6% mass; the tool
> gives 9/80 and 68.4%, and the tool's number is the one published because it is what you
> reproduce. Old values are struck through, not deleted.
> [ADR-0061](docs/adr/0061-cekinme-dedektoru-istem-rejimi-bagimliligi.md) ·
> [#61](docs/record/research_log/2026-09-06-dedektor-onarimi-b10-yeniden.md) ·
> per-item log: `outputs/eval/olcum-bi/B10_GOZLE_OKUMA_80.md`

> 🚨 **And the rescoring inverted ADR-0058's own rationale — read this before quoting either
> column.** The preamble was adopted *because it raised mass* (61.3% → 62.8%). With the
> repaired detector it **lowers** it: **68.4% with, 73.0% without** (−4.6 points). The pair is
> a genuinely matched exam — same 80 ids, **byte-identical `context_shown` in 80/80**, same
> `recall@10`; the only difference is the prompt. But the preamble's *other* legs still hold:
> A1 **0.8288 ↔ 0.8110** and misattribution **5/80 ↔ 7/80**, both in its favour. The trade is
> two-sided: the preamble makes the model **more selective but more silent**.
> **The protocol has NOT been changed** — that needs its own ADR and a human decision (open
> question **S14**). Official = with preamble.

**68.4% is the number we stand behind.** The gap to the OFF column is not a regression — the
two settings do not measure the same thing, and OFF is a **ceiling, not a rival**.

> ⚠️ The decomposition below was made against the **no-preamble** anchor (61.3%), i.e. a
> 10.2-point gap. After ADR-0058 the gap is **8.8 points** and it has **not** been
> re-decomposed.

We decomposed the 10.2-point gap: **≈5.1 points retrieval miss** (the
harness's — the gold article never arrives in 10/80 questions) and **≈4.5 points
distraction** (the model's — even when the gold *is* retrieved, A1 falls 0.909 →
0.862 because nine other articles sit beside it).

⚠️ **One consequence you should know before downloading.** The 68.4% figure is produced by
*model + retriever + preamble*. The preamble currently lives in one evaluation script and is
not shipped, and the retriever is not wired into the serving path below — so a plain download
reproduces the **ablation** column (73.0%), not the headline. Packaging both is the stated
condition for `v1` (`ROADMAP.md` ⚰️ *(2026-09-06'da silindi → [güncel plan](docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md); yeniden yazımı **Görev 13**)*).
*(Yes — the ablation column is currently the **higher** one. See the ADR-0058 note above: that
inversion is a live open question, not a reason to ship the ablation as the product.)*

🚨 **And the measurement refuted our own plan.** We built the citation verifier to
close the A1 gap. It found **zero fabricated article numbers** — the class it was
built to catch is empty. The model doesn't invent article numbers; it answers from a
*different real* article when retrieval misses (**5/80**; no-preamble ablation: 7/80). The
larger failure is still the opposite one: in **9/80** (ablation: 5/80) questions the model
abstains *while the gold article is in its context* — and with the harness off it is 17/80, so
it is a model property, not a retrieval one. Deterministic code cannot close it.
Details and the full record: `ROADMAP.md` ⚰️ *(2026-09-06'da silindi → [güncel plan](docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md); yeniden yazımı **Görev 13**)* · `sprint3-part1.md` ⚰️ *(arşiv silindi; borç kuyruğu **`DEVIR-PROMPT.md` *(silindi)* §5**'e kurtarıldı)*.

✅ **Those counts were 14/80 and 16/80 until 2026-09-06 — they were wrong, and the correction
is the single most useful thing this round produced.** The detector was repaired, all 80 items
were read **by eye**, and the true count is **8/80** (the tool says 9/80). Six of the old
fourteen were correct, cited answers misfiled as refusals; **no abstention was ever missed** in
the other direction. A training round had been planned to close this gap — it was **cancelled**,
because the pre-registered target (8-11/80) turned out to be already met with **no training at
all**: 43% of the "problem" was the measuring instrument.
⛔ It is **smaller, not gone** — 8/80 is still above Gemini 3.5 Flash-Lite's 6/80.
[ADR-0062](docs/adr/0062-b10-turu-kapatildi-hedef-egitimsiz-karsilandi.md) ·
[#60](docs/record/research_log/2026-09-06-hasat-kabul-olcutu-coktu.md) ·
[#61](docs/record/research_log/2026-09-06-dedektor-onarimi-b10-yeniden.md)

## How it was built

```
raw base ──┬── LoRA SFT   (grounding)   → τ_g
           └── LoRA ORPO  (abstention)  → τ_a
                                          │
              simultaneous 2-way TIES ────┘   → HakHukuk-4B-v0.1
```

Two skills that **actively fight each other**: training for grounding collapses
abstention (measured: 0.961 → 0.506 ᴷ³), and training for abstention collapses
grounding (56.7% → 41.2%). Neither branch is usable alone. The merge restores
both — grounding fully preserved, **57%** ~~71%~~ of the abstention collapse repaired
*(ratio re-derived 2026-08-06 from the ᴷ³ denominators: `(0.766−0.506)/(0.961−0.506)`;
[`MODEL_CARD.md`](MODEL_CARD.md) carries the note).*

## Quick start

```bash
# 1. get llama.cpp
bash scripts/egitim/setup_llamacpp.sh

# 2. serve the model
llama-server -m models/gguf/tgta_v1-q4_k_m.gguf \
    -c 8192 -ngl 99 -fa on --cache-type-k q8_0 --cache-type-v q8_0

# 3. ask, supplying the statute text as context
curl localhost:8080/v1/chat/completions -d '{
  "messages": [{"role":"user","content":"KAYNAKLAR:\n<statute text>\n\nSORU: <question>"}],
  "temperature": 0
}'
```

## Reproducing the work

The whole research record is in this repository — including the negative results,
the two runs that were invalidated by their own pre-registered gates, and a
decision that was **reversed after measurement contradicted it**.

| | |
| :--- | :--- |
| [`docs/record/research_log/`](docs/record/research_log/) | what happened, chronologically, with every number |
| [`docs/adr/`](docs/adr/) | 60 decision records — context, options, what was rejected *(0059 is reserved, not yet written)* |
| [`docs/record/kollar.md`](docs/record/kollar.md) | artifact registry: every branch and merge, with its manifest |
| [`docs/record/yurutme-tuzaklari.md`](docs/record/yurutme-tuzaklari.md) | the traps that produce a **wrong number without erroring** — each one actually bit us |
| [`outputs/eval/`](outputs/eval/) | raw evaluation outputs and run manifests |

Seeds, base commit hash, GGUF checksums and judge settings are pinned in the run
manifests (`KUNYE.json`).

## Data

Legislation from [mevzuat.gov.tr](https://www.mevzuat.gov.tr) and the
`bedesten.adalet.gov.tr` API; two Apache-2.0 Hugging Face datasets; synthetic
pairs generated **from** real statute text and verified.

**No commercial legal databases were used at any point** — a standing rule from
day one, not a later cleanup. See [`NOTICE`](NOTICE) and [`docs/VERI_PLANI.md`](docs/VERI_PLANI.md).

## Status

`v0.1`. The configuration was selected on DEV and has not been validated against
single-stage or sequential fine-tuning baselines. Until it is, the version stays
below 1.0.

Contributions, criticism, and reproduction attempts are all welcome — especially
reproduction attempts.

## License

Apache-2.0. Base model `Qwen/Qwen3.5-4B` is Apache-2.0; see [`NOTICE`](NOTICE)
for the full attribution chain.
