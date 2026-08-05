# HakHukuk-4B-v0.1

A 4B-parameter Turkish legal assistant built by training two LoRA branches
independently from the raw base and merging them as task vectors.

| | |
| :--- | :--- |
| **Base** | [`Qwen/Qwen3.5-4B`](https://huggingface.co/Qwen/Qwen3.5-4B) · Apache-2.0 · commit `851bf6e8` |
| **Method** | 2 × LoRA (r=16, α=32) from raw base → simultaneous 2-way TIES merge |
| **Internal id** | `tgta_v1` = `tg_v1` + `ta_v1` (see [`docs/record/kollar.md`](docs/record/kollar.md)) |
| **Format** | GGUF Q4_K_M · **2.59 GiB** · runs on a consumer laptop GPU |
| **Language** | Turkish |
| **License** | Apache-2.0 |

> ## ⚠️ THIS IS NOT LEGAL ADVICE
>
> HakHukuk is a research artifact for **understanding** legal text. It is **not**
> a lawyer, and its output is **not** legal advice. Do not use it to make
> decisions about a real legal matter. Consult a qualified attorney.
>
> **Legislation changes; model weights do not.** This model's knowledge is frozen
> at its training data. It has **no retrieval layer yet** (see [Roadmap](ROADMAP.md))
> — it cannot tell you what the law says *today*. Treat every article number it
> produces as a claim to verify against [mevzuat.gov.tr](https://www.mevzuat.gov.tr).

---

## What it is for

Given **a question** and **source legal text**, the model should either

1. answer, citing the article it used, **or**
2. say *"the provided sources do not cover this"* when they don't.

The second half is the hard part and the reason this project exists. A model that
answers everything is worse than useless in a legal setting — a confident wrong
article number is more dangerous than "I don't know".

## Evaluation

All numbers on the **DEV** split, **harness OFF** (no retriever, no citation
verifier, no rejection gate), judge `gpt-4o-mini`, thinking on with a 1024+512
budget, seed 3407, temperature 0.

| | M1 faithful-answer mass ↑ | over-refusal ↓ | A1 ↑ | M2 Rej ↑ | M2b Rej ↑ | tok/answer ↓ |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| bare base (Qwen3.5-4B) | 56.7% | 0.425 | 0.9864 | 0.814 | 0.986 | 1192 |
| **HakHukuk-4B-v0.1** | **71.6%** | **0.212** | 0.9087 | 0.893 | 0.877 | **714** |
| Gemini 3.1 Flash-Lite | 72.9% | 0.237 | 0.9561 | 0.930 | 1.000 | — |

**Modes.** M1 = answer from a given article · M2 = a *wrong* article is supplied,
the model must refuse · M2b = only distractors are supplied, gold absent, must
refuse · A1 = faithfulness of claims, **computed over answered items only** ·
**faithful-answer mass = coverage × A1**.

### How to read this honestly

- **vs. the base:** +26% faithful-answer mass, over-refusal halved, 40% cheaper
  per answer. The fine-tune did real work.
- **vs. Gemini 3.1 Flash-Lite:** we reach **98.2%** of its faithful-answer mass
  and **refuse less often than it does** — but we are behind on A1 (0.909 vs
  0.956), M2 (0.893 vs 0.930) and clearly behind on **M2b (0.877 vs 1.000)**.
- **This is not a parity claim.** The harness is off, cost is not normalized, and
  the merge configuration was **selected on DEV over 3 variants**. The competitor
  comparison has still never been run with the harness on.

### With the harness ON (first measured 2026-08-04)

Same artifact, same regime, DEV; the only change is that a retriever — not a
hand-built context — decides what the model sees. Retriever: hybrid BM25 +
`BAAI/bge-m3` (RRF), 40,496-article index, **k=10** (swept 2026-08-05).
Full record: [#51](docs/record/research_log/2026-08-04-harness-acik-ilk-olcum.md) ·
**correction + k sweep: [#54](docs/record/research_log/2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md)**.

> 🚨 **Corrected 2026-08-05.** The first published ON numbers used the wrong metric —
> `harness_tablo.py` reported a macro over *all* scored items as `A1`, while `A1` is
> **answered-only** (ADR-0011). The OFF anchor used the correct metric, so the ON/OFF
> comparison was apples-to-oranges. Both arms re-derived; old values struck through.

| | harness OFF | harness ON (k=5) | **harness ON (k=10)** |
| :--- | ---: | ---: | ---: |
| gold article in context | guaranteed (by construction) | 60/80 — recall@5 0.750 | **70/80 — recall@10 0.875** |
| coverage | 0.788 | 0.750 | **0.775** |
| A1 (answered-only) | 0.909 | ~~0.782~~ **0.759** | **0.768** |
| **faithful-answer mass** | **71.6%** | ~~58.7%~~ **56.9%** | **59.5%** |
| ⭐ A1, **gold-retrieved subset** | 0.909 | ~~0.934~~ **0.923** | **0.843** |
| verified citations | 87/89 | **89/89** | **118/120** |
| **fabricated article numbers** | 0 | **0** | **0** |
| strict-gate rejections | 2/80 | 1/80 | 1/80 |

**59.5% is the honest product number** (k=10). Most of the drop from 71.6% is retrieval:
at k=5 the gold article missed the top 5 in 25% of questions; raising k to 10 recovers
10 of those and lifts mass by 2.6 points.

⚠️ **But more context costs faithfulness.** On the *same* questions where the gold article
was retrieved, A1 falls **0.923 → 0.843** going from k=5 to k=10 — measured distraction.
The net gain comes from retrieval outweighing that cost. At k=5 the model was *more*
faithful on retrieved-gold questions than in the OFF setting (0.923 vs 0.909); **at k=10
that reverses** (0.843).

⭐ **k=10 also improves abstention calibration.** On questions that do not identify their
own legal domain, coverage drops 0.944 → 0.722, while on self-identifying questions it
rises 0.694 → 0.790 — the ordering flips from **wrong** to **right**
([#53](docs/record/research_log/2026-08-05-ayirt-edicilik-etiketi.md)).

⚠️ **Known limit of the citation verifier.** The model does not fabricate article
numbers — it copies the label from its context. In 14/80 questions the gold was not
retrieved and it answered from a *different real* article: the citation verifies,
the gate passes it, and the answer still does not fit the question. Deterministic
citation checking solves fabrication, **not** off-target grounding.

⚠️ A1 is scored against a **single** gold article, so an answer correctly sourced
from another article counts as unfaithful — the comparable figure across ON/OFF is
the **gold-retrieved subset** row. And the DEV questions were written with the gold
article in hand: ~25% do not identify their subject on their own, so recall@5 = 0.750
is a ceiling of *this question set*, not of the retriever.

### Why `v0.1` and not `v1.0`

The configuration was selected on DEV and has **not** been validated against
single-stage or sequential fine-tuning baselines. Until it is, the version stays
below 1.0.

## Hardware

```
GPU     ~6 GB VRAM   weights 2.59 GiB + KV cache (1 slot, 8192 ctx, q8_0) + buffers ≈ 3.5 GB
                     4 GB may work with -c 4096 — untested
RAM     ~8 GB        the harness (embedder, index) runs on CPU by design
disk    ~5 GB        model + corpus + index
```

⚠️ These are **calculated, not measured**. A measured peak will replace them when the harness
lands. The design rule behind them: **the harness never enters the GPU** — that is what makes
the difference between fitting on a laptop and not.

## Method

```
raw base ──┬── LoRA SFT   (grounding)   → τ_g   ‖τ‖ = 10.4722
           └── LoRA ORPO  (abstention)  → τ_a   ‖τ‖ =  1.1806
                                                       ────────
                        simultaneous 2-way TIES ────────┘
                        raw (no norm balancing) · trim_k 0.2 · λ 1.0
```

Both branches are trained **independently from the same raw base** — a
requirement, not a style choice: a task vector is `τ = θ_ft − θ_base`, so all
branches must share one `θ_base`.

**Why raw TIES and not norm-balanced.** The branches differ in norm by **8.87×**.
We expected the small branch to be erased without normalization and pre-registered
norm balancing as the main setting. **The measurement said the opposite:**
normalizing pushed `τ_a` to ~4.9× its trained amplitude, crushed grounding
(71.4% → 53.4%) and at higher scale made the model degenerate into repetition
loops. Raw TIES preserved grounding fully **and** repaired 71% of the branch's
abstention collapse (0.607 → 0.877). The prescription was reversed after
measurement — see [ADR-0052](docs/adr/0052-merge-norm-dengeleme-hukmu-tersine.md).

## Known limitations

1. **No currency.** Legislation is frozen in the weights. No retrieval layer yet.
2. **M2b is our weakest axis (0.877).** When given only distractor articles, the
   model still fabricates ~12% of the time. A rejection gate in the harness is the
   planned fix — deterministic code, not more training.
3. **Reasoning traces are in English.** Measured 8/8. For a citizen-facing product
   that promises readable reasoning, this is a real gap.
4. **`τ_a` learned a template.** Its typical abstention is a fixed sentence
   (median answer length 58 characters). Measured and pre-registered as a risk;
   the fix is queued.
5. **The model thinks before answering** (~714 tokens/answer including reasoning).
   Cheaper than the base's 1192 but not free.
6. **Judge-based metrics.** A1/Rej come from an LLM judge with no human-κ
   calibration. Treat them as **model-vs-model rankings**, not absolute truth.
7. **Single size, single base.** No evidence that these findings transfer.

## Reproducibility

Everything is in this repository: the full chronological research log (including
the negative results and the two invalidated runs), 52 ADRs, run manifests with
seeds and hashes, and the evaluation harness.

```
docs/record/research_log/   what happened, with numbers
docs/adr/                   why each decision was made, and what was rejected
docs/record/kollar.md       artifact registry — every branch and merge
outputs/eval/               raw evaluation outputs
```

## Citation

```bibtex
@software{hakhukuk2026,
  title  = {HakHukuk: a task-vector merged Turkish legal assistant},
  year   = {2026},
  url    = {https://github.com/Rfetha/Hukuk-SLM},
  license = {Apache-2.0}
}
```
