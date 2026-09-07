# HakHukuk

> **A Turkish legal assistant: a 4B model small enough to run on a laptop, trained to say "that is not in these sources."**
> An open-source **product** — weights + code + data + **the entire research record**. Not a thesis.

[Model card](MODEL_CARD.md) · [Türkçe](README.tr.md) · [Roadmap / plan](docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md) · [License](LICENSE)

Most of the work in a legal assistant is not answering. It is **refusing to answer when the
sources do not support one.** A confident, wrong article number is worse than silence — it is
the failure mode that makes a legal tool dangerous. `HakHukuk-4B-v0.1` (internal id `tgta_v1`)
is trained for both halves of that job: **ground** the answer in the supplied statute, and
**abstain** when the statute does not cover the question.

**Who it is for:** a Turkish citizen who is not a lawyer (the product goal) · a researcher
working on Turkish legal NLP (the record goal).

---

## ⛔ Can I install and run it today? — **NO**

That is the honest answer to the first question. **The model is measured; the product is not packaged.**

| piece | status | evidence (measured, 2026-09-07) |
| :--- | :--- | :--- |
| Model weights (Q4_K_M GGUF, **2.59 GiB**) | ✅ exist and are measured — ⛔ **not published anywhere yet** | size: [ADR-0071](docs/adr/0071-v1-release-artefakti-tek-gguf.md) · `git ls-files models/` → **0 files**; adapters are deliberately not kept in the repo |
| Retrieval index (**40,496** articles) | ✅ exists locally — ⛔ **not in git**, distribution format undecided | `du -sh data/index/mevzuat_bge_m3_s2` → **80 MB**; `git ls-files data/index` → only 2 `KUNYE.json` files; **open decision S8** (plan §S8) |
| Serving layer (API / CLI / TUI) | ❌ **does not exist as code** | `grep -rlE "fastapi\|uvicorn\|flask\|gradio" scripts/` → **0**; there is no `hakhukuk/` directory |
| Prompt | ❌ not a shippable artifact — it lives inside the evaluation scripts | plan **Task 5** · **open decision S18** |

⚠️ **The headline number is produced by `model + retriever + prompt`.** It cannot be reproduced
until all three are packaged together. That packaging is the plan's **Hat A** phase, and its
output is `v0.2` ([ADR-0065](docs/adr/0065-bolunmus-surumleme.md)).

---

## Headline numbers

**Regime:** DEV split, `n=80` · harness **ON** (hybrid BM25 + `bge-m3`, `k=10`, `RRF_K=10`,
CPU-only) · **no sufficiency preamble** · seed 3407 · 900-char chunk clip · generation
budget **1536** · judge `openai/gpt-4o-mini`.

| axis | value | source file |
| :--- | ---: | :--- |
| **faithful-answer mass** | **0.8011** | [`outputs/eval/f02-biz-onsozsuz/KUNYE.json`](outputs/eval/f02-biz-onsozsuz/KUNYE.json) |
| `coverage` | 0.9375 | same manifest |
| A1 · answered-only | 0.8545 | same manifest |
| A1 · gold-retrieved subset | 0.8902 | same manifest |
| `recall@10` | 0.9500 | same manifest |
| **fabricated article numbers** | **0 / 114** | same manifest |
| over-refusal (abstained with gold in context) | **4 / 80** | same manifest |
| misattribution (answered from a *different real* article) | **8 / 80** — **full read by eye** | [`outputs/eval/f02-biz-onsozsuz/GOZLE_OKUMA_80.md`](outputs/eval/f02-biz-onsozsuz/GOZLE_OKUMA_80.md) |
| truncated items | 4 / 80 (5.0% — exactly at the validity threshold) | same manifest |
| mean completion tokens | 782.5 | [`outputs/eval/f04-rakip-onsozsuz/KALIBRASYON_ve_OZET.md`](outputs/eval/f04-rakip-onsozsuz/KALIBRASYON_ve_OZET.md) |
| VRAM (ctx 4,096 / 32,768 / 131,072) | 3.09 / 3.70 / 5.76 GiB | `outputs/eval/_artefakt/vram_stack_tgta_v1.json` ([ADR-0071](docs/adr/0071-v1-release-artefakti-tek-gguf.md)) |

⛔ **The harness-OFF ("ceiling") regime was NOT re-measured in this unit.** The old `v1`-unit
ceiling figure is not comparable to today's numbers and is not repeated in this document.

---

## Competitor comparison — an **equal exam**, three readings

Same 80 questions, same context, same budget, same judge. **Equality was not assumed, it was
measured:** `recall@10` = **0.9500** for all four subjects and `context_shown` is
**byte-identical in 80/80**
([`f04-rakip-onsozsuz/KALIBRASYON_ve_OZET.md`](outputs/eval/f04-rakip-onsozsuz/KALIBRASYON_ve_OZET.md)).

The mandatory calibration step (28 competitor abstention items read by eye) found that the
abstention detector **over-counts refusals on the Gemini template** — meaning part of our lead
was an artifact of the instrument. The three readings below correct for that; **the binding one
is the most conservative: GÖZ-katı (strict-by-eye)**
([ADR-0064](docs/adr/0064-v1-kapisi-uc-maddeli-on-kayit.md)).

| faithful-answer mass | tool (raw) | by-eye, medium | **by-eye, strict (binding)** |
| :--- | ---: | ---: | ---: |
| **HakHukuk-4B-v0.1** | **0.8011** | **0.8011** | **0.8011** |
| Gemini 3.1 Flash-Lite | 0.6746 | 0.7058 | 0.7058 |
| Gemini 3.5 Flash-Lite | 0.7174 | 0.7403 | 0.7622 |
| Gemini 3.5 Flash | 0.6925 | 0.7050 | 0.7425 |

*(Our arm is identical across all three readings: all 80 items were read by eye and the
**tool ↔ eye difference is zero**.)*

Other axes (raw tool numbers, same file):

| axis | ours | 3.1 FL | 3.5 FL | 3.5 Flash |
| :--- | ---: | ---: | ---: | ---: |
| A1 · gold-retrieved | **0.8902** | 0.7900 | 0.8449 | 0.8523 |
| **fabricated articles** | **0** | 1 | 4 | 4 |
| truncated items | 4 (5.0%) | 5 (6.2%) | 0 | 4 (5.0%) |
| mean completion tokens | 782.5 | 861.5 | **171.1** | 699.4 |

### ⚠️ Sentences this table does **not** support

1. **"We would pass on TEST too."** The measurement is on **DEV**. The frozen TEST set's
   retrieval ceiling is ≈75%
   ([ADR-0069](docs/adr/0069-kabul-testi-tavan-kullanimi-raporlamasi.md)) and the acceptance
   test **has not been run**.
2. **"A verdict that survived a judge panel."** It is still a **single judge family**
   (`gpt-4o-mini`), there is **no** κ, and self-preference was **not measured**. This is an open
   debt — the plan's **`HP`** phase closes it.
3. **"The model got this much better."** Most of the gain came not from training but from
   **measurement** (see below).

---

## 🚨 Where the gain came from: **the weights never changed**

Phase 0 ran **zero training runs** and the number moved from 68.4% to **80.1%**. What was found
was not a better model but **defects in the measuring instrument** — five of them, every one in
the *"produces a wrong number without erroring"* class, every one of which **passed the numeric
gate**, and every one caught only by **reading by eye** or by opening and reading the run manifest.

| # | defect | effect | source |
| :-- | :--- | :--- | :--- |
| 1 | The questions had been **stripped of their context** — 5/10 retrieval misses were really "a lawyer reading this question alone cannot name the gold article" | `recall@10` 0.8750 → **0.9375** | [ADR-0067](docs/adr/0067-soru-onarimi-dev-test-v2.md) |
| 2 | The defect was not in BM25 but in **fusion**: at `RRF_K=60`, "mediocre in both arms" beat "perfect in one arm" | `RRF_K` 60 → 10; `recall@10` 0.9375 → **0.9500** | [ADR-0068](docs/adr/0068-rrf-k-60-to-10.md) |
| 3 | **81% of the DEV ↔ TEST gap came from set composition** (not stratified by article length) | the acceptance test's ceiling was pre-registered at ≈**75%** | [ADR-0069](docs/adr/0069-kabul-testi-tavan-kullanimi-raporlamasi.md) |
| 4 | 🚨 **The generation budget was not equal to the competitor's, and it was against us** — ours 1024, theirs effectively 1532 | one formula for everyone: budget **1536**, identical across all four subjects | [ADR-0070](docs/adr/0070-uretim-butcesi-esitlendi.md) |
| 5 | 🆕 **The gate clause had NO ANCHOR** — `v1.0` clause (3) said *"M5 must not rise above today's"*, but `tgta_v1`'s M5 had **never been measured in any unit**; the clause referred to itself | anchor read from ADR-0039 (**base**, not the competitor); M5 re-run on both arms | [ADR-0073](docs/adr/0073-m5-rejimine-dry-eklendi.md) · trap **2.17** |

*(These five are **Faz 0's** findings. ⚠️ A sixth instrument defect was found **the day
before**, in the B10 round: the abstention detector turned out to be prompt-regime dependent
([ADR-0061](docs/adr/0061-cekinme-dedektoru-istem-rejimi-bagimliligi.md),
[#61](docs/record/research_log/2026-09-06-dedektor-onarimi-b10-yeniden.md)). Its **competitor-side**
manifestation was measured inside Faz 0 — the F0.4 calibration found **6 clear false positives**
on competitor arms and **0** on ours, which is why the binding reading is the **most conservative**
one ([`f04 calibration`](outputs/eval/f04-rakip-onsozsuz/KALIBRASYON_ve_OZET.md)). The same
detector was wrong a **third** time on 2026-09-07, in blind mode: **6 of 6** flags were false
positives.)*

Full narrative: [`research_log #62`](docs/record/research_log/2026-09-06-faz0-olcum-zinciri.md)

---

## The `v1.0` gate — three clauses, pre-registered formula

The formula was written **before any competitor number was seen**; the numbers were then derived
mechanically ([ADR-0064](docs/adr/0064-v1-kapisi-uc-maddeli-on-kayit.md)).

| clause | verdict | number | source |
| :--- | :--- | :--- | :--- |
| **(1)** mass ≥ 3.5 Flash − 2.0 points | ✅ **PASSED** | strict-by-eye: **0.8011 ↔ threshold 0.7225** → **+5.86 p** | [`f04 summary`](outputs/eval/f04-rakip-onsozsuz/KALIBRASYON_ve_OZET.md) |
| **(2)** misattribution does not regress | ✅ (true by definition today) | anchor re-pinned at **8/80** in the new unit; it binds at the **next training round** | [`GOZLE_OKUMA_80.md`](outputs/eval/f02-biz-onsozsuz/GOZLE_OKUMA_80.md) |
| **(3)** M5 (blind/parametric) does **not** rise — anti-target | ✅ **PASSED** | memorized mass **0.3899 ↔ base 0.4697** (tool) · **0.4057 ↔ 0.4739** (by eye) | [`outputs/eval/f07-m5-anti-hedef/KUNYE.json`](outputs/eval/f07-m5-anti-hedef/KUNYE.json) · [`GOZLE_OKUMA_CEKINME.md`](outputs/eval/f07-m5-anti-hedef/GOZLE_OKUMA_CEKINME.md) |

⚠️ **The version is still `v0.1`, on purpose.** Versioning was deliberately split
([ADR-0065](docs/adr/0065-bolunmus-surumleme.md)): the **product version** (`v0.2 → v1.0`) passes
through the product's own gate, while the **claim version** stays tied to the mid-gate that
**failed** on 2026-08-06
([ADR-0045](docs/adr/0045-ara-kapi-merge-onarim-kontrolu.md)). ⛔ A failed gate stays failed —
it was neither loosened nor redefined.

---

## What it does **not** promise

- ⛔ **It is not legal advice.** It is not a lawyer and its output does not substitute for legal
  advice. Verify every article number against [mevzuat.gov.tr](https://www.mevzuat.gov.tr).
- ⛔ **It is not 100% accurate.** On the 80-question DEV set, **8 misattributions** and
  **4 over-refusals** were measured (tables above). The measurement is the verdict of a
  **single judge family**.
- ⛔ **Currency lives in the library, not in the weights.** Legislation changes; weights do not.
  Keeping statutes current is the retrieval layer's job. This is a design decision, not a gap.
- ⛔ **Scope: current Republic-of-Türkiye legislation only.** Ottoman-era material, case-law
  interpretation and foreign law are out of scope.
- ⛔ **No parity claim.** The comparison above is on **DEV**, with a single judge family, and
  cost is not normalized.

---

## How it was built

```
raw base ──┬── LoRA SFT   (grounding)   → τ_g
           └── LoRA ORPO  (abstention)  → τ_a
                                          │
              simultaneous 2-way raw TIES ┘  → HakHukuk-4B-v0.1 (tgta_v1)
```

Two skills that **actively fight each other**: training for grounding collapses abstention, and
training for abstention collapses grounding. **Neither branch is usable alone**; the merge
restores both. Every branch is trained **independently from the raw base** — the task-vector
definition (`τ = θ_ft − θ_base`) requires it.

⚠️ The ratios behind this section were measured in the **old (`v1`) unit** and are not comparable
to the headline numbers above; per-branch figures and manifests live in
[`docs/record/kollar.md`](docs/record/kollar.md).

---

## Roadmap

The order is **binding** (human decision, 2026-09-07) —
[full plan](docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md):

| phase | what | output |
| :--- | :--- | :--- |
| **`HP`** — judge panel | a second and third judge family, κ, self-preference measurement | no number stays the verdict of one family |
| **Hat A** — packaging (runs parallel to `HP`) | the `hakhukuk/` package: prompt artifact · types · service · CLI · TUI · index distribution | **an installable product** |
| **Phase C** — documentation layer | `PRODUCT.md` · `ROADMAP.md` · `TODO.md` · `docs/MIMARI.md` (none of the four exists today) | **`v0.2` RELEASE** |
| **Hat B** — model | B1 (misattribution) · `τ_a` amplitude · gate run + frozen-TEST acceptance test | **the `v1.0` gate** |

`v2` = the application/API layer on top of this same model. arxiv is a **by-product**, not the goal.

---

## Repository map

| location | what |
| :--- | :--- |
| `hakhukuk/` | ⛔ **does not exist yet** — the product package; Hat A will write it |
| [`scripts/`](scripts/) | the **measuring instrument** (deliberately separate from the product). Five subfolders: [`egitim/`](scripts/egitim/) · [`olcum_uretim/`](scripts/olcum_uretim/) · [`puanlama/`](scripts/puanlama/) · [`erisim_korpus/`](scripts/erisim_korpus/) · [`veri_hazirlik/`](scripts/veri_hazirlik/) |
| [`docs/record/research_log/`](docs/record/research_log/) | the **research record** — what happened, chronologically, with every number; latest entry **#62** |
| [`docs/adr/`](docs/adr/) | the **decision ledger** — 46 numbered files, numbering runs to **0073** (`0001-0026` live in one file: [`gemma4-12b-dersler.md`](docs/adr/gemma4-12b-dersler.md); **0059 is reserved**) |
| [`docs/record/kollar.md`](docs/record/kollar.md) | the **artifact registry** — every branch and merge with its manifest. *An artifact with no row is nameless and must not be used.* |
| [`docs/record/yurutme-tuzaklari.md`](docs/record/yurutme-tuzaklari.md) | the list of patterns that **produce a wrong number without erroring** — every one of them actually bit us |
| [`outputs/eval/`](outputs/eval/) | raw evaluation outputs and run manifests (`KUNYE.json`) |
| [`data/corpus/mevzuat_maddeler.jsonl`](data/corpus/) | the 40,496-article legislation corpus |
| [`tests/`](tests/) | `pytest` unit tests |
| [`CLAUDE.md`](CLAUDE.md) | repository map + binding rules |

---

## The research record is itself the asset

In this repository **negative results are first-class**, and the places where our own published
claims were refuted are **stamped** in the record: runs invalidated by their own pre-registered
gates · a normalization decision **reversed** because measurement contradicted it
([ADR-0052](docs/adr/0052-merge-norm-dengeleme-hukmu-tersine.md)) · a mid-gate that **failed**
([ADR-0045](docs/adr/0045-ara-kapi-merge-onarim-kontrolu.md)) · and the admission that *"the gain
came from measurement, not training"*
([#62](docs/record/research_log/2026-09-06-faz0-olcum-zinciri.md)).

Numbers are **sourced, not remembered**: every result's metric, `n`, judge, seed and output file
are pinned in the run manifest (`KUNYE.json`).

---

## Data and license

- **Sources:** [mevzuat.gov.tr](https://www.mevzuat.gov.tr) · Resmî Gazete · the Yargıtay open
  portal · the `bedesten.adalet.gov.tr` JSON API ([contract](docs/BEDESTEN_API.md)) · two
  Apache-2.0 Hugging Face datasets · synthetic pairs generated **from** real statute text and
  verified. Data plan: [`docs/VERI_PLANI.md`](docs/VERI_PLANI.md) · training recipe:
  [`docs/FINE_TUNING.md`](docs/FINE_TUNING.md).
- ⛔ **No commercial legal database was used at any point** (Lexpera, Kazancı, etc.) — copyright
  poison. This was a rule from day one, not a later cleanup.
- PII is masked in training data.
- **License: Apache-2.0** ([`LICENSE`](LICENSE)). The base model `Qwen/Qwen3.5-4B` is
  Apache-2.0; the full attribution chain is in [`NOTICE`](NOTICE).

## Contributing

Contributions, criticism, and **reproduction attempts** — especially reproduction attempts — are
all welcome. If you cannot reproduce a number, that is a bug report.
