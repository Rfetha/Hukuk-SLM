# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

**HakHukuk / Hukuk-TR** — a Turkish-language legal AI assistant built on a Small Language Model (SLM). The mission: democratize access to justice by simplifying legal language, drafting documents, and helping citizens understand their own cases.

**Project framing (decided 2026-05-29): private repo + proprietary license for now.** Repo is private, commercial rights belong to the owner. Model weights + model card may be published on HF later (optional). Academic paper door is not closed — if it makes sense later, the rigor/reproducibility (fixed seeds, logged runs, clean ablations) is already in place. Do NOT assume OSS or Apache-2.0 for the project itself; base model (Gemma 4 12B, `gemma-4-12B-it-qat-q4_0-unquantized`) is Apache-2.0 and must be attributed.

**Current state: Phase 1 in execution (research-grade).** Git repo is live; data pipeline + eval harness + v1 SFT (Modal A100) are built and run. As of 2026-06-13 we are designing a literature-grounded eval benchmark (CORE-HARD + TRAP/abstention) and have reframed v1 as the wrong SFT target → planning a fresh v2. **The authoritative running narrative is `docs/record/research_log/README.md` (chronological) + `docs/adr/` (decisions).** Read those first for current state — the strategy docs below give the original *plan*, the record gives *what actually happened*.

## Documents (read these before doing anything)

- `docs/VISION.md` — mission, design principles, and the 5-phase evolution roadmap (SLM → RAG/Graph → niche → agentic → citizen platform). The authoritative source for *what* we're building and in what order.
- `docs/FINE_TUNING.md` — the technical playbook for Phase 1: hardware constraints, QLoRA/Unsloth stack, data pipeline, training recipe, ablation matrix, evaluation plan. The authoritative source for *how* to build Phase 1.
- `docs/_archive/Hukuk-TR_ ... Stratejik Araştırma Raporu.md` — a broader strategic research report, **marked superseded/historical (banner at top); moved to `docs/_archive/` 2026-07-05.** It proposes a much larger base model (Gemma 4 26B A4B MoE) that conflicts with the core accessibility constraint. The operative base is **Gemma 4 12B** (`gemma-4-12B-it-qat-q4_0-unquantized`, QLoRA → Q4_0 GGUF) per `VISION.md`/`FINE_TUNING.md`/`TEKNIK_PLAN.md`. Keep the report only as an idea source for market/evolution/RAG.
- `TODO.md` — the active task list, organized by phase.
- **`docs/record/research_log/README.md` — the chronological research record (NEW, authoritative for "what happened").** Every significant experiment/result/decision lands here as a dated entry, with numbers + lesson + paper-mapping.
- `docs/adr/` — Architecture Decision Records. Every big decision = an immediate ADR (context/options/consequence).

## Documentation discipline (HARD RULE — this is a research project headed for a paper)

We must be able to **retroactively reconstruct and write the paper X days/weeks later** from the repo alone. Therefore:

- **Every significant experiment, result, or decision → write it down immediately**, while context is fresh. Two homes: `docs/record/research_log/README.md` (chronological narrative + numbers + lesson + which paper section it serves) and `docs/adr/` (a discrete ADR per big decision). A finding that lives only in chat is a finding lost.
- **Numbers are sourced, not remembered.** Record the exact metric, n, judge, seed, and the file the result lives in (`outputs/eval/...`). Reproducibility (fixed seeds, logged runs, clean ablations) is the point — it keeps the paper door open.
- **Negative/surprising results are first-class** (they are the K3 paper findings): log v0's collapse, the blind-vs-RAG ceiling, "SFT degrades abstention," etc. with the same rigor as wins.
- When a decision contradicts an older doc, **flag the contradiction in both places** rather than silently overwriting — the audit trail is the asset.

## Core constraints that shape every decision

These are non-negotiable framing from the docs — honor them in any code or recommendation:

- **Accessibility over raw performance.** Product target = run on consumer GPUs incl. ~8 GB. Chosen base: **Gemma 4 12B** (`gemma-4-12B-it-qat-q4_0-unquantized`, QLoRA fine-tune → Q4_0 GGUF ~6.5GB deploy). The 8GB end-user target is achieved via QAT → Q4_0 quantization after fine-tuning, not by limiting training to a 4B model.
- **Actual dev machine (corrected 2026-05-29): RTX 5070 Laptop, ~12 GB VRAM, Blackwell (sm_120), CUDA 13.1** — NOT the RTX 4070 / 8 GB the older docs assume. 12B QLoRA on 12 GB is tight (batch=1, gradient_checkpointing required) but feasible. ⚠️ Blackwell/sm_120 + CUDA 13.1 is bleeding-edge: PyTorch, `bitsandbytes`, `flash-attn`, `Unsloth` all need recent Blackwell-compatible builds. The 8 GB figure in older docs is the *end-user accessibility target*, not our training rig.
- **Local machine is for prototyping; real training runs go to the cloud** (Colab Pro A100 40GB, Kaggle, or RunPod). Validate the pipeline locally on tiny models (Gemma 3 270M smoke test) before spending cloud quota.
- **Currency lives in the library, not the model's brain.** Laws change; weights don't. Keep legal-currency concerns for the Phase 2 RAG/Graph layer — do not try to bake current statutes into fine-tuning.
- **Citizen-facing language, not lawyer jargon.** Default output behavior is legal-term → plain-Turkish translation. ⚠️ **UNDER REVISION (2026-06-13):** the primary audience has been reframed to the **expert (lawyer)**; plain-language citizen output becomes an **app-layer prompt mode**, not the model's training target. Correctness/grounding comes from RAG. See `docs/record/research_log/README.md` (2026-06-13 entry) + pending ADR-0010; until that ADR lands, treat this bullet as historical.
- **License-clean data.** Use only public/open sources (Mevzuat.gov.tr, Resmi Gazete, Yargıtay open portal, Kaggle/HF open datasets). **Never** use commercial sources (Lexpera, Kazancı) — copyright poison whether the repo stays private/commercial or weights are published later. Mask PII in training data. (Repo itself is private + proprietary; see project framing above.)

## Intended technical stack (from FINE_TUNING.md — not yet set up)

When scaffolding the project, build toward this stack:

- **Environment:** `uv` + Python 3.11. WSL2 (Ubuntu 22.04) + **Blackwell-compatible CUDA (13.x — exact version verified at install; NOT 12.1)** recommended over native Windows to reduce `bitsandbytes`/`flash-attn` pain. ⚠️ sm_120 needs recent Blackwell-built wheels.
- **Training:** PyTorch 2.4+, Unsloth (primary; fall back to TRL+PEFT+transformers for unsupported models), bitsandbytes 0.43+ (NF4 4-bit), FlashAttention-2.
- **Method:** QLoRA — `r=16`, `lora_alpha=32`, `target_modules="all-linear"`, `lora_dropout=0.05`, `batch=1`, `gradient_checkpointing=True`. Gemma 4 12B encoder-free unified mimarisi — ayrı vision/audio encoder yok, tüm modality aynı decoder'dan geçer; text-only SFT multimodal yeteneği bozmaz. Model kartı teyitli: native OCR (Türkçe dahil), el yazısı tanıma, document/PDF parsing, ses girişi. Faz 3'te belge fotoğrafı + sesli soru use case'leri devreye girer; `visual_tokens=560-1120` belge görselleri için gerekli. See `FINE_TUNING.md §2` for the full config and `§5` for the training recipe.
- **Deploy pipeline:** Fine-tune (NF4 QLoRA) → merge (bf16) → Q4_0 quantize via llama.cpp → GGUF ~6.5GB → 8GB VRAM end-user.
- **Data format:** chat-template JSON (`messages` with `user`/`assistant` roles), Gemma-compatible. Four task variants: Q&A, term simplification, statute summarization, scenario→citation.
- **Eval:** custom Turkish legal benchmark — **HakHukuk Eval Suite** (`scripts/build_eval_sets.py` → CORE-HARD + TRAP; axes A1 groundedness / A3 abstention-RejectionRate / A4 citation-format; `bench_scorecard.py`). LLM-as-judge (gpt-4o-mini, cross-judge gpt-4o via `judge_agreement.py`). **Human-κ DESCOPED** (no annotators) → judge-agreement + ~30 author spot-check instead. See `knowledge/summary_eval_benchmark_literature.md`.
- **Tracking / reproducibility:** Weights & Biases; DVC or HF Hub for model+dataset versioning; fixed seeds, locked requirements.

## Working notes

- Project docs and the working language are **Turkish.** Match that language in docs, comments, and commit messages unless asked otherwise. Code identifiers stay in English.
- This **is a git repository** (branch `master`). Scripts live in `scripts/`, eval outputs in `outputs/eval/`, data in `data/`. There is still no formal build/test/lint setup — add when it earns its keep.
- Phase ordering is strict and deliberate (`VISION.md §2`). Don't jump ahead to RAG/Graph (Phase 2) or agents (Phase 3) while Phase 1 (a fine-tuned, benchmarked base model) is incomplete — each phase is a self-contained OSS deliverable.
- **`docs/TEKNIK_PLAN.md` is the active execute plan** (full roadmap + detailed Phase 1 steps + locked decisions). **`knowledge/summary_mecellem_turkish_legal.md`** captures the key prior-art findings. Read both before doing Phase 1 work.
- **Phase 1 base model: Gemma 4 12B** (`google/gemma-4-12B-it-qat-q4_0-unquantized`, updated 2026-06-07; was Qwen3.5-4B). We do our OWN fine-tune. We reuse Mecellem's open recipe (cleaning chain, curriculum), eval model (`newmindai/Muhakim`), and Apache-2.0 code — but adapt to Gemma 4 architecture. TurboQuant (arXiv:2504.19874) noted for Phase 3 KV-cache serving; see `knowledge/summary_turboquant.md`.
- **Data: `docs/VERI_PLANI.md` is the authoritative data plan.** Hard rule, learned the hard way: **EDA-verify every dataset before trusting it** — `newmindai/EuroHPC-Legal` looked great (43K, Apache 2.0) but sampling revealed garbage (mismatched Q&A, hallucinated laws, Ottoman-era content) and was rejected. Scope is **current Republic-of-Turkey legislation only.** Ground truth = Mevzuat.gov.tr. Verified-usable so far: `OrionCAF/turkish_law_qa_dataset`, `Renicames/turkish-law-chatbot` (both Apache 2.0). Data we lack (plain-language, citizen-niche, scenario→statute) is produced via **grounded synthetic generation** (real statute text → LLM generates pairs → verify). `scripts/scan_hf_datasets.py` scans + EDA-peeks HF candidates; `scripts/eda_datasets.py` + `scripts/build_sft_dataset.py` built `data/processed/sft_v0/` (~32K Q&A).
- **Live legislation source: the `bedesten.adalet.gov.tr/mevzuat` JSON API** — reverse-engineered from `saidsurucu/mevzuat-mcp` (MIT) and tested working. Auth-free, no Playwright. Search + full text + article tree; same backend also serves case law (içtihat) for Phase 2. Contract reference: `docs/BEDESTEN_API.md`, probe client: `scripts/bedesten_probe.py`. **Requires a Turkish IP** (gov firewall blocks foreign/VPN IPs — both mevzuat.gov.tr and bedesten). We use the live API over the frozen `muhammetakkurt/mevzuat-gov-dataset` (907 laws, Sept 2024) when freshness/coverage matters.
