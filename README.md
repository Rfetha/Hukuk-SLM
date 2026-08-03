# HakHukuk

**A Turkish legal assistant small enough to run on a laptop — built to say "I don't know".**

[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[Model card](MODEL_CARD.md) · [Roadmap](ROADMAP.md) · [Türkçe](README.tr.md)

---

Most of the work in a legal assistant is not answering. It is **refusing to answer
when the sources don't support one.** A confident, wrong article number is worse
than silence — it is the failure mode that makes a legal tool dangerous.

HakHukuk is a 4B model (2.59 GiB, Q4_K_M) trained for both halves of that job:
ground the answer in the supplied statute, and abstain when the statute doesn't
cover the question.

> ### ⚠️ Not legal advice
> This is a research artifact. It is not a lawyer and its output is not legal
> advice. Legislation changes; weights do not. **There is no retrieval layer yet** —
> the model cannot tell you what the law says today. Verify every article number
> against [mevzuat.gov.tr](https://www.mevzuat.gov.tr).

## Where it stands

DEV split, harness off, judge `gpt-4o-mini`. Full protocol in the [model card](MODEL_CARD.md).

| | faithful-answer mass ↑ | over-refusal ↓ | refusal on missing sources ↑ | tok/answer ↓ |
| :--- | ---: | ---: | ---: | ---: |
| bare base | 56.7% | 0.425 | 0.986 | 1192 |
| **HakHukuk-4B-v0.1** | **71.6%** | **0.212** | 0.877 | **714** |
| Gemini 3.1 Flash-Lite | 72.9% | 0.237 | 1.000 | — |

We reach **98% of Flash-Lite's faithful-answer mass and refuse less often than it
does**, at 2.59 GiB and ~zero marginal cost. We are still behind it on refusing
when only distractor sources are present — that gap is the top item on the
[roadmap](ROADMAP.md), and the planned fix is deterministic code, not more training.

**This is not a parity claim:** the harness is off, cost is not normalized, and
the merge configuration was selected on DEV.

## How it was built

```
raw base ──┬── LoRA SFT   (grounding)   → τ_g
           └── LoRA ORPO  (abstention)  → τ_a
                                          │
              simultaneous 2-way TIES ────┘   → HakHukuk-4B-v0.1
```

Two skills that **actively fight each other**: training for grounding collapses
abstention (measured: 0.986 → 0.607), and training for abstention collapses
grounding (56.7% → 41.2%). Neither branch is usable alone. The merge restores
both — grounding fully preserved, 71% of the abstention collapse repaired.

## Quick start

```bash
# 1. get llama.cpp
bash scripts/setup_llamacpp.sh

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
| [`docs/adr/`](docs/adr/) | 52 decision records — context, options, what was rejected |
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
