# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

**HakHukuk** — an open-source Turkish legal assistant built on a small language
model. Mission: make legal language legible to the citizen.

**⚠️⚠️ FRAMING CHANGED 2026-08-03 — read this before anything else.**

This was a **master's thesis** project (private repo, proprietary licence, claim-driven).
It is now a **fully public open-source product**: Apache-2.0, weights + code + data +
the entire research record. An arxiv paper may follow, but it is **no longer the goal**.

```
WAS   thesis  → prove a claim  → gates, pre-registration, ablations serve the claim
IS    product → build the best model → same discipline, now a "don't fool yourself" tool
```

**The goal is the model.** Beat Gemini 3.1 Flash-Lite, then reach Flash and Pro.
Priorities live in [`ROADMAP.md`](ROADMAP.md), tied to measured gaps.

### What the change removes

| constraint | why it existed | now |
| :--- | :--- | :--- |
| **ONE size point** (ADR-0028, ~4B) | the thesis ran at a single point | ❌ **lifted** — 8B/12B are open, multiple sizes may ship |
| **graph-RAG out of scope** (ADR-0019) | thesis boundary | ❌ **lifted** — the harness is the product's core |
| **Kapı 5 / CP4-CP5 baselines** | proving the methodological claim | 🔽 **optional** — deferred, see [`sprint2b.md`](sprint2b.md) |
| **frozen TEST seen once** | selection bias vs. the paper | 🔁 repurposed as a **release acceptance test** |
| *"never say frontier"* | paper terminology rule | ❌ moot |

### What the change keeps — all of it

Fixed seeds · logged runs · run manifests (`KUNYE.json`) · pre-registered gates ·
same-day research log · an ADR per decision · the trap list.

**This is not ceremony.** In one sprint the discipline caught four things that would
otherwise have become wrong published numbers: a metric that rewarded refusing
(`A1` is answered-only), the same blind spot on the merge side, a validity gate that
voided a degenerate model's results, and a normalization prescription that
**measurement reversed** ([ADR-0052](docs/adr/0052-merge-norm-dengeleme-hukmu-tersine.md)).

### Current artifact

**`HakHukuk-4B-v0.1`** (internal id `tgta_v1`) — two LoRA branches trained
independently from the raw base, merged as task vectors with raw TIES.
Card: [`MODEL_CARD.md`](MODEL_CARD.md) · registry: [`docs/record/kollar.md`](docs/record/kollar.md).

```
                  ours 4B   Gemini 3.1 FL
M1 faithful mass    71.6%      72.9%
M2 Rej              0.893      0.930
A1                  0.909      0.956
M2b Rej             0.877      1.000   ← widest gap; the harness closes it in code
```

⚠️ **All of it measured with the harness OFF** — the real product number has never
been run. `v0.1` because the config was selected on DEV and is not validated against
baselines.

### Target audience: the CITIZEN — but read the trap

Plain language is the **presentation layer of a correct answer, not a training
target.** Training toward plain/short answers was tried and **lowered accuracy**;
the citizen-register round matched base while abstention collapsed
([ADR-0010](docs/adr/gemma4-12b-dersler.md#adr-0010)). So: train for correctness and
abstention, simplify at the **prompt layer**.

**Three record documents, three different jobs** — don't confuse them:
- `TASARIM.md` — *what we will do.* Decisions, rejected alternatives, gates, open questions.
- `docs/record/gemma4-12b-kronoloji.md` — *what happened and what the numbers were.* The 12B line's full chronology with every measurement preserved verbatim. Source material for the paper's **Results**.
- `docs/adr/gemma4-12b-dersler.md` — *what we learned.* Base-agnostic lessons + the 26 ADRs' decisions. Source material for **Methodology** and **Limitations**.

New findings go to `docs/record/research_log/` (numbering continues at **#39**); new decisions get a new ADR (**0027** onward). Note `docs/V2_PLAN.md` and the v4 recipe are SUPERSEDED (12B-era, historical). The 2026-07-17 spec is **partially superseded** by ADR-0027 — its parity framing, cost accounting and judge design live on; its base decision, graph scope and corpus answer were updated.

## Documents (read these before doing anything)

- **`TASARIM.md` (repo root) — ⭐ THE authoritative design doc for the current line.** What we will build and what we will measure: the two-layer claim, the task-vector lattice, the two matrices, DEV/TEST, harness, gates, scope limits, and — critically for the paper — **the rejected alternatives with their reasons** (§11). Start here.
- **`referans-design-doc.md` (repo root) — the user's original draft.** Input to `TASARIM.md`. **Kept clean; never edit.** Its numbers were illustrative placeholders and were deliberately NOT carried over.
- **`docs/adr/gemma4-12b-dersler.md` — ⭐ everything the retired line learned, in one file.** The 26 ADRs of the Gemma 4 12B line (0001-0026) were consolidated here on 2026-07-24 and the individual files deleted (recoverable from git). Three parts: **(A) lessons** — base-agnostic, this is what you read; **(B) decision record** — each ADR's decision, rejected alternatives, outcome, and *status in the new line*; **(C) entry points** into the raw log. Every `ADR-00NN` mention elsewhere in the repo still resolves — the file carries an anchor per ADR (`#adr-0011`). **Read part A before designing any experiment**: it is where "plain SFT destroys abstention", "the eval mirror is mandatory", and "`spawn()` not `remote()`" live. The new decision ledger starts at ADR-0027.
- `docs/VISION.md` — mission, design principles, and the 5-phase evolution roadmap (SLM → RAG/Graph → niche → agentic → citizen platform). The authoritative source for *what* we're building and in what order.
- `docs/FINE_TUNING.md` — the technical playbook for Phase 1: hardware constraints, QLoRA/Unsloth stack, data pipeline, training recipe, ablation matrix, evaluation plan. The authoritative source for *how* to build Phase 1.
- `docs/_archive/Hukuk-TR_ ... Stratejik Araştırma Raporu.md` — a broader strategic research report, **marked superseded/historical (banner at top); moved to `docs/_archive/` 2026-07-05.** It proposes a much larger base model (Gemma 4 26B A4B MoE) that conflicts with the core accessibility constraint. The operative base is **Gemma 4 12B** (`gemma-4-12B-it-qat-q4_0-unquantized`, QLoRA → Q4_0 GGUF) per `VISION.md`/`FINE_TUNING.md`/`TEKNIK_PLAN.md`. Keep the report only as an idea source for market/evolution/RAG.
- `TODO.md` — the active task list, organized by phase.
- **⭐ `docs/record/kollar.md` — the artifact registry.** Every trained branch AND merge has its identity here; *an artifact with no row is nameless and must not be used*. Current: `tg_v1` (‖τ‖ 10,4722) · `ta_v1` (‖τ‖ 1,1806) · **`tgta_v1` = `HakHukuk-4B-v0.1`** — the first working merge (raw TIES, ADR-0052), which produced ARA KAPI's green result. **Both names stay and do different jobs:** `tgta_v1` is internal traceability (the registry's whole point — *which branch, which version* answerable from the filename), `HakHukuk-4B-v0.1` is outward-facing (model card · paper). ⚠️ `v0.1` not `v1.0` **on purpose**: the config was selected on DEV over 3 variants and has **not been tested against the baselines** — `v1.0` opens only if Kapı 5 passes. It also carries the base/ours/Gemini table with an explicit **"NOT a parity claim"** banner (harness off, cost not normalized, DEV pool, merge config selected on DEV).
- **`docs/record/research_log/README.md` — the chronological research record (NEW, authoritative for "what happened").** Every significant experiment/result/decision lands here as a dated entry, with numbers + lesson + paper-mapping.
- **`docs/record/yurutme-tuzaklari.md` — ⭐ read BEFORE any run.** The single list of *"produces a wrong number without erroring"* patterns on this line, each one having actually bitten: dropped `--data`/`--thinking off`, uncalibrated refusal regex, missing `--target-modules`, `set -e` swallowing the error message, half-finished quantization that still leaves a file on disk. This line's failure class is **silent wrongness, not crashes**. The 12B line's equivalent is `docs/adr/gemma4-12b-dersler.md` part A.
- **`sprint3.md` (repo root) — ⭐ THE ACTIVE execution doc (`/goal sprint3.md`).** **HARNESS** — retriever + citation verifier + rejection gate, then the first **harness-ON** measurement (never run). Chosen over more model training because two of our three measured gaps (A1, M2b) close **in deterministic code**, because retrieval changes the input distribution the model sees, and because **without a retriever there is no product** — today the user must paste the statute text themselves. Opens with **five design decisions** (embedder · chunk unit · static vs live corpus · ⭐ the harness-ON eval protocol · gate threshold) that block coding.
- **`sprint2b.md` (repo root) — ⏸️ DEFERRED (`/goal sprint2b.md` when arxiv is decided).** The baselines Sprint 2 deferred: **CP4** (single-stage mixed) · **CP5** (sequential + on-policy control) → **Kapı 5**, the inner claim's real test. ⛔ It opens with an **unresolved decision** that blocks CP4: the pre-registered text says *mixed SFT*, but `τ_a` was trained with **ORPO** — running the baseline as plain SFT would confound *method* (merge vs mixed) with *objective* (ORPO vs SFT) and hand a reviewer the grounds to void Kapı 5. Recommendation on file: mixed **ORPO** via `is_pref` row masking, which `MaskedORPOTrainer` already supports.
- **`sprint2.md` (repo root) — ✅ CLOSED 2026-08-03 (ARA KAPI 🟢 güçlü yeşil; CP4-CP5 deferred by the human, needs a new `/goal`). Kept as the record.** Sprint 2 = *"produce everything Sprint 3's merge experiment needs, and make sure that experiment will be fair."* CP0 thinking-mode measurement ([ADR-0040](docs/adr/0040-dusunce-modu-olculecek-on-kayitli-kural.md), pre-registered 🟢🟡🔴 rule — this is the **trigger for RS-FT**; a GREEN result reopens ADR-0035 and reverses ADR-0030 clause 2) · CP0.5 `causal-conv1d` speed gate · CP1 judge-prompt fix ([ADR-0041](docs/adr/0041-raft-meta-iddia-hakem-kurali.md)) · CP2 `rejected` re-harvest ([ADR-0042](docs/adr/0042-rejected-havuzu-tek-kaynak-ve-on-policy-kontrol.md)) · CP3 `τ_a` + 🔴 **ARA KAPI** · CP4-CP5 baselines. Order is gate-bound; **no money goes to the baselines until the mid-gate passes.**
- **⚠️ Kapı 5 lost clause (d) on 2026-07-29 — [ADR-0039](docs/adr/0039-kapi-6-parametrik-sizinti.md).** M5 (parametric leakage) is now its own **Kapı 6**, anchored at **base** (not the competitor) on two metrics — coverage ≤ 37.5% and memorized-mass (`coverage × A1`) ≤ 10.7%. Not a loosening: `τ_g` fails it today and that is reported, and every cell is also reported against the original (d). The split exists because a hard M5 veto made Kapı 5 unpassable by any `τ_g`-containing cell — the gate closed before it could measure what it was built to measure.
- `docs/record/sprint1/sprint1-sonuc-tablosu.md` — Sprint 1's permanent result record: base ↔ Gemini 3.1 Flash-Lite ↔ `τ_grounding` on one protocol, with derived readings (faithful-answer mass, matched-subset A1) and validity caveats. **Not a parity claim** — harness off, cost not normalized. `sprint1.md` itself is **CLOSED (2026-07-29)**, kept in place as an audit trail.
- `docs/adr/` — Architecture Decision Records. Every big decision = an immediate ADR (context/options/consequence).

## Documentation discipline (HARD RULE — this is a research project headed for a paper)

We must be able to **retroactively reconstruct and write the paper X days/weeks later** from the repo alone. Therefore:

- **Every significant experiment, result, or decision → write it down immediately**, while context is fresh. Two homes: `docs/record/research_log/README.md` (chronological narrative + numbers + lesson + which paper section it serves) and `docs/adr/` (a discrete ADR per big decision). A finding that lives only in chat is a finding lost.
- **Numbers are sourced, not remembered.** Record the exact metric, n, judge, seed, and the file the result lives in (`outputs/eval/...`). Reproducibility (fixed seeds, logged runs, clean ablations) is the point — it keeps the paper door open.
- **Negative/surprising results are first-class** (they are the K3 paper findings): log v0's collapse, the blind-vs-RAG ceiling, "SFT degrades abstention," etc. with the same rigor as wins.
- When a decision contradicts an older doc, **flag the contradiction in both places** rather than silently overwriting — the audit trail is the asset.

## Core constraints that shape every decision

These are non-negotiable framing from the docs — honor them in any code or recommendation:

- **Accessibility over raw performance.** Product target = run on consumer GPUs. **The base is a PARAMETER, not a decision (ADR-0026): no script carries a default; an undefined base must fail EARLY** — silently falling back to the wrong model turns a multi-hour run into invisible garbage. Current **working assumption** = a ~4B-class instruct model (ADR-0027, supersedes ADR-0003's Gemma 4 12B), and **no run starts before it clears the 6-item verification gate** in `TASARIM.md` §8: llama.cpp architecture support (ADR-0025 is now a *base selection criterion*) · chat-template render verified **by eye** (`research_log` #38: minja mis-rendered a branch, the model never stopped, and a CANON run was silently wasted) · turn-marker assert · Unsloth/sm_120 · quantization (**Q4_K_M** absent an official QAT checkpoint — ADR-0023's pure-Q4_0 was QAT-specific and does **not** transfer) · license.
  **≤8 GB = SOFT GATE (not a hard limit):** preferred band ≤8 GB, but configurations above it (12/16/24 GB) are still reported, *at a cost on the accessibility axis* — a cost-performance **curve**, not a single point (ADR-0018). **⚠️ ADR-0028 narrows this: the thesis runs at ONE size point.** The whole grid — 2 branches + 2 baselines (5 training runs) + the lattice + harness + parity matrix — sits on a single ~4B-class base, which trains on the local RTX 5070 at **$0** (the 12B line had to send every run to Modal). A second size is **future work**: the same recipe applied to a bigger model after the thesis ships, not a chapter in it.
  **Three costs are accepted and must appear in Limitations, not be glossed as "future work":** (a) the **external-validity gap does not close** — "are these findings specific to this base?" stays unanswered, inheriting the 12B line's permanent limitation; (b) the **capacity question is unmeasurable** — "does the skill conflict shrink as capacity grows?" was the merge claim's most interesting second question and cannot be asked at one point; (c) **ADR-0018's curve requirement is not met** — the soft-gate framing survives in principle, but what gets reported is a single marked point, not a measured curve. The same-family rule from ADR-0027 is **deferred, not cancelled**: whenever that second pass happens, family and size must not change together or the difference is attributable to neither (ADR-0017's reason for rejecting the multi-base arm).
  Harness never enters the GPU (embedder on CPU, graph + index in CPU RAM/disk) — that is the fits/doesn't-fit difference. ⚠️ Historical note: the "bottleneck is KV-cache, not weights" claim was **measured false for the 12B base** (KV was 18% of weights); it must be re-measured per base, never assumed.
- **Actual dev machine (corrected 2026-05-29): RTX 5070 Laptop, ~12 GB VRAM, Blackwell (sm_120), CUDA 13.1** — NOT the RTX 4070 / 8 GB the older docs assume. 12B QLoRA on 12 GB is tight (batch=1, gradient_checkpointing required) but feasible. ⚠️ Blackwell/sm_120 + CUDA 13.1 is bleeding-edge: PyTorch, `bitsandbytes`, `flash-attn`, `Unsloth` all need recent Blackwell-compatible builds. The 8 GB figure in older docs is the *end-user accessibility target*, not our training rig.
- **Local machine is for prototyping; real training runs go to the cloud** (Colab Pro A100 40GB, Kaggle, or RunPod). Validate the pipeline locally on tiny models (Gemma 3 270M smoke test) before spending cloud quota.
- **Currency lives in the library, not the model's brain.** Laws change; weights don't. Keep legal-currency concerns for the Phase 2 RAG/Graph layer — do not try to bake current statutes into fine-tuning.
- **Citizen-facing language, not lawyer jargon.** Default output behavior is legal-term → plain-Turkish translation. ⚠️ **UNDER REVISION (2026-06-13):** the primary audience has been reframed to the **expert (lawyer)**; plain-language citizen output becomes an **app-layer prompt mode**, not the model's training target. Correctness/grounding comes from RAG. **Resolved by ADR-0010 (`docs/adr/gemma4-12b-dersler.md#adr-0010`, in force):** primary training target = expert register; citizen plain-language = app-layer prompt mode. Evidence: training toward plain/short answers *lowered* accuracy, and the citizen-register round matched base while abstention collapsed — plainness is the presentation layer of a correct answer, not a training target. Register held at ~1.0 across the 12B line.
- **License-clean data.** Use only public/open sources (Mevzuat.gov.tr, Resmi Gazete, Yargıtay open portal, Kaggle/HF open datasets). **Never** use commercial sources (Lexpera, Kazancı) — copyright poison whether the repo stays private/commercial or weights are published later. Mask PII in training data. (Repo itself is private + proprietary; see project framing above.)

## Intended technical stack (from FINE_TUNING.md — not yet set up)

When scaffolding the project, build toward this stack:

- **Environment:** `uv` + Python 3.11. WSL2 (Ubuntu 22.04) + **Blackwell-compatible CUDA (13.x — exact version verified at install; NOT 12.1)** recommended over native Windows to reduce `bitsandbytes`/`flash-attn` pain. ⚠️ sm_120 needs recent Blackwell-built wheels.
- **Training:** PyTorch 2.4+, Unsloth (primary; fall back to TRL+PEFT+transformers for unsupported models), bitsandbytes 0.43+ (NF4 4-bit), FlashAttention-2.
- **Method: QLoRA per branch, then task-vector merge (ADR-0027).** Per-branch QLoRA — `r=16`, `lora_alpha=32`, `target_modules="all-linear"`, `lora_dropout=0.05`, `batch=1`, `gradient_checkpointing=True`. **Every branch trains from the RAW BASE, independently.** This is a validity requirement, not a style choice: a task vector is defined as `τ = θ_ft − θ_base`, so all branches must share one `θ_base`. Training one branch on top of another produces sequential SFT, not a task vector — i.e. it destroys the very thing we set out to measure.
  Merging is **simultaneous k-way** TIES/DARE, not iterative — `TIES(TIES(τg,τa),τr) ≠ TIES(τg,τa,τr)`, because TIES trims, elects signs and averages across *all* vectors at once. Each LoRA is materialized as `ΔW = (α/r)·BA` in **bf16**, merged in **full weight space** (TIES operates element-wise on the delta, so LoRA-space combination is only valid for a plain linear sum), and quantized **last**. Merging runs on **host RAM, streaming tensor-by-tensor** — never on the GPU; full materialization of base + all branches in bf16 runs to tens of GB and would strain host RAM at the contrast point. **⚠️ ADR-0036's normalization prescription was REVERSED on 2026-08-03 — [ADR-0052](docs/adr/0052-merge-norm-dengeleme-hukmu-tersine.md): the main result is now RAW TIES, norm-balanced is the ablation.** The original text follows because its *premise* was confirmed; only its *inference* was refuted. **Each `τ` is normalized (`τ/‖τ‖`) before merging — ADR-0036.** Branches train at very different scales (`τ_g` 1,083 steps @1e-4 · `τ_a` 82 steps @1e-5), and TIES' sign-election + disjoint-mean are **mass-weighted**, so without normalization the small-norm branch is erased at exactly the parameters where the skills genuinely conflict — and "abstention wasn't preserved" would be read off a scale artifact. Raw TIES is still run as an ablation. **DARE does not fix this** (it preserves expectation, hence the ratio). `‖τ‖` is measured and reported **unconditionally** for every branch.
  **Merging itself costs no training compute** — that is what makes sweeping merge techniques realistic. But sweep on **DEV**, never on the frozen CANON test set.
- **Deploy pipeline:** per-branch QLoRA (NF4) → materialize ΔW (bf16) → k-way merge (full weight space, host RAM) → quantize via llama.cpp (**Q4_K_M** absent an official QAT checkpoint) → GGUF → consumer GPU.
- **⚠️ Multimodal / OCR is NOT a base-selection argument and never was measured.** Whatever base is chosen, treat native OCR claims as unproven until tested in-repo. For Turkish specifically the right Phase-3 architecture is a **separate OCR preprocessor, not native VLM OCR**: dedicated engines beat general VLMs on Turkish, and `ğ→˘g` / `ş→¸s` / `İ→Ì` breakages corrupt RAG matching in legal text (OCRTurk, arXiv:2602.03693).
- **Data format:** chat-template JSON (`messages` with `user`/`assistant` roles), Gemma-compatible. Four task variants: Q&A, term simplification, statute summarization, scenario→citation.
- **Eval: 6-mode CANON (ADR-0011), extended by ADR-0027 with a DEV/TEST split.** Modes: M1 distractor-faithfulness · M4 oracle ceiling · M2 near-miss refusal · M2b multi-source-miss refusal · M3 empty-context refusal · **M5 blind/parametric = ANTI-TARGET** (must NOT rise; currency belongs in the library, not the weights). Invariants: seed **3407**, eval-mirror **900-char** chunk clip (the clip applied in training must be applied identically at eval, or the model is measured on longer context than it was trained on), A1 = answered-only macro, and — new, **ADR-0043** — **thinking ON with a budgeted forced close: 1024 thinking + 512 answer tokens** (`gen_eval_grounded.py --think-budget`). The budget is a **regime invariant with the same standing as the seed and the clip**: every subject, branch, lattice cell and competitor runs at the same budget; a mismatch does not error, it just voids the comparison.
  ⚠️ **Why forced closure exists at all** (`research_log` #42): under `--thinking on` the bare base **never closes `</think>`** in M1/M2/M5 — it oscillates between answering and abstaining (same reasoning line **219×**) and returns an empty `content` with HTTP 200. This is **non-termination, not truncation**: raising the budget 8× (4096→32768) changed nothing, `temp 0.6` rescued half, Q8_0 changed nothing. Notably `τ_g` **does** terminate on its own (35/36, median 452 tokens) — fine-tuning stabilized the reasoning rather than killing it. Cost of the mode: **249 → ~1198 tokens/answer (~4.8×)**, which goes straight into ADR-0017's parity accounting. **Sprint 1's three anchors were measured thinking-off and must be re-run before they can anchor anything in the new protocol.**
  **TEST = `data/eval/canon/` (40+35), frozen, seen ONCE in the final report. DEV = newly generated CANON-protocol items**, and all merge/hyperparameter selection happens there — sweeping against the frozen set would burn it for selection and make every number optimistic.
  **Judge = four-layer defense:** judge-free backbone (regex abstention + deterministic citation verification — most of the claim surface never meets a judge) · a 3-family panel only on judgment axes (M1/M4), with κ reported via `judge_agreement.py` · **family exclusion** (no subject graded by its own family's judge) · self-preference measured and reported. **Human-κ DESCOPED** (no annotators).
  **Mandatory pre-step:** calibrate the refusal-detection regex on *every* competitor family. Left uncalibrated it undercounts their refusals and shifts scores **in our favor** — no number is reported before this is done.
- **Tracking / reproducibility:** Weights & Biases; DVC or HF Hub for model+dataset versioning; fixed seeds, locked requirements.

## Working notes

- Project docs and the working language are **Turkish.** Match that language in docs, comments, and commit messages unless asked otherwise. Code identifiers stay in English.
- This **is a git repository** (branch `master`). Scripts live in `scripts/`, eval outputs in `outputs/eval/`, data in `data/`. There is still no formal build/test/lint setup — add when it earns its keep.
- Phase ordering is strict and deliberate (`VISION.md §2`) — **with one deliberate exception (2026-07-17, ADR-0019):** the thesis parite iddiası harness olmadan kurulamaz, bu yüzden **Faz 2'nin retriever + atıf-doğrulayıcı + red-kapısı dilimi teze dahildir.** Bu istisna **graph-RAG'i KAPSAMAZ** (o kesin future-work). Agents (Faz 3) hâlâ kapsam dışı. Yani: harness dilimi ✅ teze girer, graph-RAG ❌ girmez.
- **`docs/TEKNIK_PLAN.md` is the active execute plan** (full roadmap + detailed Phase 1 steps + locked decisions). **`knowledge/summary_mecellem_turkish_legal.md`** captures the key prior-art findings. Read both before doing Phase 1 work.
- **Base model = a parameter with a working assumption, not a fixture.** See the accessibility constraint above and `TASARIM.md` §8 for the 6-item gate. We do our OWN fine-tune. Mecellem stays **cite-only** (ADR-0016/0020) — it is a CPT foundation base, not an assistant, so "we beat it" is a category error and is never claimed. TurboQuant (arXiv:2504.19874) is future-work for Phase 3 serving and **is not in llama.cpp**; today's lever is `--cache-type-k/-v q8_0` (`knowledge/summary_turboquant.md`).
- **Data: `docs/VERI_PLANI.md` is the authoritative data plan.** Hard rule, learned the hard way: **EDA-verify every dataset before trusting it** — `newmindai/EuroHPC-Legal` looked great (43K, Apache 2.0) but sampling revealed garbage (mismatched Q&A, hallucinated laws, Ottoman-era content) and was rejected. Scope is **current Republic-of-Turkey legislation only.** Ground truth = Mevzuat.gov.tr. Verified-usable so far: `OrionCAF/turkish_law_qa_dataset`, `Renicames/turkish-law-chatbot` (both Apache 2.0). Data we lack (plain-language, citizen-niche, scenario→statute) is produced via **grounded synthetic generation** (real statute text → LLM generates pairs → verify). `scripts/scan_hf_datasets.py` scans + EDA-peeks HF candidates; `scripts/eda_datasets.py` + `scripts/build_sft_dataset.py` built `data/processed/sft_v0/` (~32K Q&A).
- **Live legislation source: the `bedesten.adalet.gov.tr/mevzuat` JSON API** — reverse-engineered from `saidsurucu/mevzuat-mcp` (MIT) and tested working. Auth-free, no Playwright. Search + full text + article tree; same backend also serves case law (içtihat) for Phase 2. Contract reference: `docs/BEDESTEN_API.md`, probe client: `scripts/bedesten_probe.py`. **Requires a Turkish IP** (gov firewall blocks foreign/VPN IPs — both mevzuat.gov.tr and bedesten). We use the live API over the frozen `muhammetakkurt/mevzuat-gov-dataset` (907 laws, Sept 2024) when freshness/coverage matters.
