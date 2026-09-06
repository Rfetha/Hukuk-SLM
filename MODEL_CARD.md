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
> at its training data. A retrieval layer **exists and is measured** (see the
> harness-ON section below), but it is **not packaged into the serving path** — the
> quick-start below still expects you to supply the statute text. Treat every article
> number it produces as a claim to verify against [mevzuat.gov.tr](https://www.mevzuat.gov.tr).

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
| bare base (Qwen3.5-4B) | 56.7% | 0.425 | 0.9864 | 0.803 ᴷ⁴ | 0.961 ᴷ³ | 1192 |
| **HakHukuk-4B-v0.1** | **71.6%** | **0.212** | 0.9087 | 0.833 ᴷ⁴ | **0.766** ᴷ³ | **714** |
| Gemini 3.1 Flash-Lite | 72.9% | 0.237 | 0.9561 | 0.848 ᴷ⁴ | 0.883 ᴷ³ | — |

ᴷ³ **M2b re-scored 2026-08-06.** The old numbers were produced with a denominator the
judge decided **while looking at the model's answer** — so the same exam yielded a different
denominator per model. The denominator is now answer-blind and identical across arms
(`valid_traps` 61…80 → **77** on this exam). Old values are kept in
[`#57`](docs/record/research_log/2026-08-06-cekinme-aleti-onarimi.md), which carries the full
conversion table: base `0.986 → 0.961` · ours `0.877 → 0.766` · Gemini FL `1.000 → 0.883`.

ᴷ⁴ **M2 re-scored 2026-08-06** (same defect, same fix, paid separately — 10 runs share one
70-item exam, so a single payment of **$0.1054** closed all of them). The denominator was
**55–63 per arm** on an identical exam; it is now **66/70 in every arm** — a self-verifying
check that is reported because it can fail. Conversion: base `0.814 → 0.803` · ours
`0.893 → 0.833` · Gemini FL `0.930 → 0.848`.
🚨 **This correction runs IN OUR FAVOUR and is reported as such.** The arm that moved most is
the **competitor** (−8.2 pts vs our −6.0); the gap on M2 narrows from **3.7 to 1.5 points**.
The dirty denominator was flattering Gemini more than us. *(The [#46](docs/record/research_log/2026-07-30-cp2r-kor-payda.md)
correction of the same class went the other way — against us. Neither direction was chosen.)*
Source: [`outputs/eval/karar3-m2-payda/`](outputs/eval/karar3-m2-payda/m2_payda_2026-08-06.json).
⚠ **The A1 column has NOT been re-scored** — it is not a function of `valid_trap` (separate axis);
its own stack caveat is in the box below.

> 🚨 **The A1 column is not judge-stack matched (measured 2026-08-06).** The base and Gemini rows
> were judged on the **openai-direct** gateway with a **pre-ADR-0041** judge prompt; our row was
> judged on **openrouter (provider-pinned)** with the current one. Re-judged under the current
> protocol on the identical answers, **base A1 = 0.9587** (−2.77 pts) and **Gemini FL = 0.9592**
> (+0.31) — the shift is asymmetric, so it cannot be dismissed as gateway noise. The two causes
> (gateway vs judge-prompt version) **cannot be separated**: the old stack is permanently
> unreachable (no OpenAI credit). Source: `outputs/eval/g1-eslesmis-a1/`.
> ⚠️ On a **coverage-matched** subset (n=40, one denominator, all stacks matched) the A1 axis
> does **not** separate base from ours: base **0.9525** · ours **0.9563** · FL **0.9813**, with
> 33/40 items tied. The raw A1 column above rewards **answering less**.

**Modes.** M1 = answer from a given article · M2 = a *wrong* article is supplied,
the model must refuse · M2b = only distractors are supplied, gold absent, must
refuse · A1 = faithfulness of claims, **computed over answered items only** ·
**faithful-answer mass = coverage × A1**.

### How to read this honestly

- **vs. the base:** +26% faithful-answer mass, over-refusal halved, 40% cheaper
  per answer. The fine-tune did real work.
- **vs. Gemini 3.1 Flash-Lite:** we reach **98.2%** of its faithful-answer mass
  and **refuse less often than it does** — but we are behind on A1 (0.909 vs
  0.956), M2 (0.833 vs 0.848) ᴷ⁴ and clearly behind on **M2b (0.766 vs 0.883)** ᴷ³.
  - ⚠️ **The M2 gap is ONE item wide — read it as the instrument's resolution
    limit, not as a result.** After the denominator was equalized (ᴷ⁴) both arms
    share denominator **66**, so the quantum is `1/66 = 1.52 points`:
    `tgta_v1` abstains on **55/66**, Gemini on **56/66**. The 0.015 difference is
    *exactly one judge verdict*. Before the repair the gap was ~2.4 items wide;
    it is now the smallest non-zero difference this instrument can express.
    A single item flipping would report "we equalized with Gemini on M2" —
    that sentence should not be constructed from a one-item move.
    ⚠️ The **0.3 A1-point** judge noise floor does **not** cover this axis (it was
    derived for the answered-only A1 macro). No substitute floor is asserted here:
    setting one is a human decision, filed as debt in
    [`docs/open_questions.md`](docs/open_questions.md).
- **This is not a parity claim.** The harness is off, cost is not normalized, and
  the merge configuration was **selected on DEV over 3 variants**. The competitor
  comparison has still never been run with the harness on.

### With the harness ON (first measured 2026-08-04)

Same artifact, same regime, DEV; the only change is that a retriever — not a
hand-built context — decides what the model sees. Retriever: hybrid BM25 +
`BAAI/bge-m3` (RRF), 40,496-article index, **k=10** (swept 2026-08-05).
Full record: [#51](docs/record/research_log/2026-08-04-harness-acik-ilk-olcum.md) ·
**correction + k sweep: [#54](docs/record/research_log/2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md)** ·
**corpus repair: [#55](docs/record/research_log/2026-08-05-s2-yururluk-alani.md)** ·
**sufficiency preamble adopted as main protocol:
[#56](docs/record/research_log/2026-08-05-olcum-bosluklari.md) §5 (D1) /
[ADR-0058](docs/adr/0058-b-i-kaynak-yeterliligi-onsozu-benimsendi.md)**.

**Source directories.** Main-protocol (with preamble, official) run:
`outputs/eval/olcum-bi/`. No-preamble ablation run:
`outputs/eval/s2-harness-k10-etiketli/`.

> 🚨 **Corrected 2026-08-05.** The first published ON numbers used the wrong metric —
> `harness_tablo.py` reported a macro over *all* scored items as `A1`, while `A1` is
> **answered-only** (ADR-0011). The OFF anchor used the correct metric, so the ON/OFF
> comparison was apples-to-oranges. Both arms re-derived; old values struck through.

| | harness OFF | ON (k=5) | ON (k=10) | ⭐ **ON k=10, repaired corpus + sufficiency preamble** |
| :--- | ---: | ---: | ---: | ---: |
| gold article in context | guaranteed (by construction) | 60/80 — recall@5 0.750 | 70/80 — recall@10 0.875 | **70/80 — recall@10 0.875** |
| coverage | 0.788 | 0.750 | 0.775 | **0.8250** ~~0.763~~ |
| A1 (answered-only) | 0.909 | ~~0.782~~ 0.759 | 0.768 | **0.8288** ~~0.8229~~ (ablation, no preamble: **0.8110**) |
| **faithful-answer mass** | **71.6%** | ~~58.7%~~ 56.9% | 59.5% | **68.4%** ~~62.8%~~ (no-preamble ablation: **73.0%** ~~61.3%~~ ⚠️ now *higher* — see note) |
| ⭐ A1, **gold-retrieved subset** | 0.909 | ~~0.934~~ 0.923 | 0.843 | **0.8729** ~~0.8705~~ (ablation, no preamble: **0.8593**) |
| verified citations | 87/89 | 89/89 | 118/120 | **80/83** (ablation, no preamble: 116/118) |
| **fabricated article numbers** | 0 | **0** | **0** | **0/83** (ablation, no preamble: 0/118) |
| strict-gate rejections | 2/80 | 1/80 | 1/80 | **3/80** (ablation, no preamble: 1/80) |

**68.4% is the honest product number** ~~62.8%~~ (k=10, repaired corpus, `--sufficiency-preamble`
main protocol — ADR-0058; no-preamble ablation: **73.0%**).

> 🚨 **Rescored 2026-09-06 ([ADR-0061](docs/adr/0061-cekinme-dedektoru-istem-rejimi-bagimliligi.md) ·
> [#61](docs/record/research_log/2026-09-06-dedektor-onarimi-b10-yeniden.md)).** The abstention
> detector scanned the *whole* answer in one branch, so our template's discarded-sources
> rationale was read as a refusal. The bug was **specific to our own answer template** — the
> competitor's numbers did not move at all when it was fixed (measured). All 80 items were then
> read **by eye**. ⚠️ The fix also **inverted ADR-0058's rationale**: the preamble now *lowers*
> mass (68.4% with, 73.0% without) though it still improves A1 and misattribution. The protocol
> was **not** changed — open question **S14**.

> ⚠️ The decomposition below was made against the **no-preamble** anchor (61.3%); after
> ADR-0058 the gap is **8.8 points** and it has **not** been re-decomposed.

Most of the drop from 71.6%
is retrieval: at k=5 the gold article missed the top 5 in 25% of questions; raising k to 10
recovers 10 of those (+2.6 points), and repairing sub-article identity in the corpus adds
another **+1.8**.

⚠️ **Two caveats travel with the last column, permanently.** (a) Three of the 80 DEV gold
labels were corrected **after** the numbers were seen — the procedure was tightened (rule-based
selection, blind judge, pre-registered prompt, position-bias control, human approval) and the
correction **did not raise** the headline, but the ordering stands on the record. (b) The
judge's **re-run noise floor was measured at ~0.3 A1 points** on bit-identical inputs; no
difference smaller than that is interpreted here.

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
numbers — it copies the label from its context. In **5/80** questions (ablation, no preamble:
7/80; 14/80 at k=5) the gold was not retrieved and it answered from a *different real*
article: the citation verifies, the gate passes it, and the answer still does not fit the
question. Deterministic citation checking solves fabrication, **not** off-target grounding.

🚨 **The larger gap is the opposite failure: over-refusal.** In **9/80** ~~14/80~~ (ablation, no preamble: **5/80** ~~16/80~~) questions the
model abstains *while the gold article is in its context* — **≈2.8× the size** of the
off-target class above (14 ↔ 5), and **independent of `k`** (14 → 15 → 16 across every setting
measured). No amount of retrieval improvement closes it; it is a model-side gap and it is
the stated reason for the next training round.

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

> 🚨 **Corrected 2026-09-06.** This section previously said the figures were
> ~~**calculated, not measured**~~ and that *"a measured peak is still owed"*. That was
> **wrong**: a measurement exists — `outputs/eval/_artefakt/vram_stack.json`, produced by
> [`scripts/measure_vram_stack.py`](scripts/measure_vram_stack.py). The old prose is struck,
> not deleted.

**Measured**, `llama-server`, Q4_K_M, KV cache `q8_0`, one slot (⚠️ the GPU model is **not**
recorded in the output file — only pstate, clocks, power and temperature are):

| context | server VRAM | peak |
| ---: | ---: | ---: |
| 4,096 | **3.09 GiB** | 4,530 MiB |
| 32,768 | 3.70 GiB | 5,146 MiB |
| 131,072 | 5.76 GiB | 7,259 MiB |

```
RAM     ~8 GB        the harness (embedder, index) runs on CPU by design
disk    ~5 GB        model + corpus + index
```

> ⚠️ **The measurement was taken on the BASE GGUF (`q35-4b-q4_k_m.gguf`), not on this model.**
> `tgta_v1` is the same architecture, quantization and file-size class (2.59 GiB), so the
> figures are expected to carry over — but **`tgta_v1` itself has not been measured** and no
> number here is claimed for it. Closing that costs $0 and ~15 minutes; it is a listed `v1`
> item ([roadmap](ROADMAP.md), Phase 0.2).

The harness landed and the design rule held in practice: it runs entirely on CPU
(embedder + 40,496-article index, 759 ms per query) and **never enters the GPU**. That is what
makes the difference between fitting on a laptop and not.

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
loops. Raw TIES preserved grounding fully **and** repaired **57%** ~~71%~~ of the branch's
abstention collapse (0.506 → 0.766 ᴷ³; the jump is unchanged at +0.26). The prescription was reversed after
measurement — see [ADR-0052](docs/adr/0052-merge-norm-dengeleme-hukmu-tersine.md).

> ⚠️ **Why the repair ratio moved but the jump did not** (corrected 2026-08-06, defect K2).
> The ratio is `(merge − τ_g) / (base − τ_g)`, so it moves when *any* of the three inputs is
> re-scored. The blind-denominator fix (ᴷ³) re-scored all three: old `(0.877−0.607)/(0.986−0.607)
> = 71.2%` → current `(0.766−0.506)/(0.961−0.506) = **57.1%**`. The inputs above had been
> updated in place; this **derived** figure had not — it stood 14 points **in our favour**
> underneath a ᴷ³ stamp that certified it as reviewed. Harmful precisely because it was stamped.

## Known limitations

1. **No currency in the shipped path.** Legislation is frozen in the weights. The
   retrieval layer is built and measured but not wired into serving.
2. **M2b is our weakest axis (0.766 ᴷ³) and the planned fix is now MEASURED DEAD.** When
   given only distractor articles, the model still answers ~12% of the time. The
   rejection gate was built as the fix. It was run on 2026-08-05 in a **matched exam**
   (harness-ON with the gold article ablated, 4 sources ↔ 4 sources, same regime) and
   🚨 **it made the axis worse, not better: 0.735 vs 0.766 ᴷ³** (sign unchanged). The gate rejected 2/80,
   and the mechanism it depends on is measurably empty — `KANUN_YOK 0`, `MADDE_YOK 0`,
   and **36/80 answers carry no citation at all**, so there is nothing for the gate to
   fire on. The model copies labels from its context, so its citations verify and the
   gate passes them. Deterministic code **cannot** close M2b in this regime; the fix
   moves to training. Note the exam favoured the harness and it still lost: the
   closed-harness distractors are all drawn from the gold article's own law
   (same-law rate **1.00** vs **0.475**), which makes abstaining harder, not easier.
3. **Reasoning traces are in English.** Measured 8/8. For a citizen-facing product
   that promises readable reasoning, this is a real gap.
4. **`τ_a` learned a template.** Its typical abstention is a fixed sentence
   (median answer length 58 characters). Measured and pre-registered as a risk;
   the fix is queued.
5. **The model thinks before answering** (~714 tokens/answer including reasoning).
   Cheaper than the base's 1192 but not free.
6. **Judge-based metrics, and only ONE judge family.** A1/Rej come from a single LLM judge
   family (`gpt-4o-mini`) with **no κ and no three-family panel** — the panel specified in
   ADR-0032 was never built, and human-κ is DESCOPED. Every judgment-axis number on this card
   carries a **single-family** stamp. Treat them as **model-vs-model rankings**, not absolute
   truth.
7. **Single size, single base — and this gap does NOT close.** No evidence that these findings
   transfer to another size or family. This is an accepted, permanent cost of the one-size-point
   design, not future work.
8. 🚨 **The ARA KAPI (mid-gate) FAILED on 2026-08-06 — the merge has not been validated against
   the baselines.** What was pre-registered was the *formula*
   (`merge M2b ≥ 0.90 × base's answer-blind M2b`), not a number: threshold **0.8649** ↔ merge
   **0.766** → **short by 9.9 points** (it also fails the older 0.887 threshold; denominators
   are equal, 77 ↔ 77). Per ADR-0050 the *tool* was repaired and the threshold was **not**
   touched. That gate is what authorized the CP4-CP5 baseline spend — **that authorization is
   gone**, so *"merge preserves conflicting skills better than sequential/mixed SFT"* remains
   **unproven**. [ADR-0045](docs/adr/0045-ara-kapi-merge-onarim-kontrolu.md) ·
   [#58](docs/record/research_log/2026-08-06-payda-tekillesmesi.md).
9. 🚨 **Gemini 3.5 Flash-Lite is ahead of us in the product regime.** First measured
   2026-08-06 on a matched exam (ADR-0057; `recall@10` identical at 0.875 across all three
   subjects): faithful-answer mass **68.4% (us) ~~62.8%~~ · 61.7% (3.1 FL) · 69.5% (3.5 FL)** — we pass
   3.1 FL by **+1.0 point (narrow)** and 3.5 FL passes us by **6.7 points**. Over-refusal is
   where we lose: **23.75%** vs **12.5%** for both competitors — roughly **twice** theirs.
   We do lead both on A1 (answered and gold-retrieved). Source:
   `outputs/eval/g2-fl-harness/OZET.md`.
10. **ADR-0018's cost-performance CURVE requirement is not met.** One marked point is reported,
    not a measured curve across sizes.
11. **The sufficiency preamble buys accuracy partly by saying less.** Adopting it (ADR-0058)
    raised mass and A1, but claims fell 268 → **206** (−23%), total citations 118 → **83**
    (−30%), answers with no citation at all 8 → **13**. Whether that trade is acceptable for a
    legislation assistant — where *auditability* is the promise — is **an open question, not a
    settled one** ([`docs/open_questions.md`](docs/open_questions.md), OQ-3 / decision S6).
12. ✅ **The over-refusal counts were wrong and have been corrected — 14/80 → 9/80 (8/80 by
    eye).** On 2026-09-06 the abstention detector was found to score a correct, cited answer as
    an abstention: in the no-opening-verdict branch it scanned the whole answer, and our
    template's discarded-sources rationale tripped the refusal regex. Six of the fourteen were
    false positives; **none were missed in the other direction**. All 80 items were read by eye
    (`outputs/eval/olcum-bi/B10_GOZLE_OKUMA_80.md`). ⚠️ The bug was **specific to our own answer
    template** and therefore **penalised only us** — the competitor's numbers did not move when
    it was fixed. A training round planned to close this gap was **cancelled**: the
    pre-registered target (8-11/80) was already met with no training at all
    ([ADR-0062](docs/adr/0062-b10-turu-kapatildi-hedef-egitimsiz-karsilandi.md) ·
    [#60](docs/record/research_log/2026-09-06-hasat-kabul-olcutu-coktu.md) ·
    [#61](docs/record/research_log/2026-09-06-dedektor-onarimi-b10-yeniden.md)).
13. ⛔ **Over-refusal is smaller, not solved.** 8/80 is still above Gemini 3.5 Flash-Lite's
    **6/80**, and *"how far would training push it down"* was **never measured** — the round
    that would have answered it was cancelled. This stays an open limitation.
14. 🚨 **ADR-0058's rationale is inverted and the protocol has not yet been revisited.** The
    sufficiency preamble was adopted because it raised mass; after the detector repair it
    **lowers** mass (68.4% with, **73.0%** without) while still improving A1 (0.8288 ↔ 0.8110)
    and misattribution (5/80 ↔ 7/80). The pair is a matched exam — same 80 ids,
    byte-identical context in 80/80. Changing the main protocol needs its own ADR and a human
    decision; until then the official number is the **with-preamble** one
    ([`docs/open_questions.md`](docs/open_questions.md), **S14**).

## Reproducibility

Everything is in this repository: the full chronological research log (including
the negative results and the two invalidated runs), 60 ADRs, run manifests with
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
