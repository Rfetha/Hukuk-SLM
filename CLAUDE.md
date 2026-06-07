# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

**HakHukuk / Hukuk-TR** — a Turkish-language legal AI assistant built on a Small Language Model (SLM). The mission: democratize access to justice by simplifying legal language, drafting documents, and helping citizens understand their own cases.

**Project framing (decided 2026-05-29): private repo + proprietary license for now.** Repo is private, commercial rights belong to the owner. Model weights + model card may be published on HF later (optional). Academic paper door is not closed — if it makes sense later, the rigor/reproducibility (fixed seeds, logged runs, clean ablations) is already in place. Do NOT assume OSS or Apache-2.0 for the project itself; base model (Gemma 4 12B, `gemma-4-12B-it-qat-q4_0-unquantized`) is Apache-2.0 and must be attributed.

**Current state: planning/research only.** There is no code yet. The repo holds strategy documents that define the architecture, fine-tuning approach, and 5-phase roadmap. The first job is to turn `docs/FINE_TUNING.md` and `docs/VISION.md` into an actual data pipeline and training run.

## Documents (read these before doing anything)

- `docs/VISION.md` — mission, design principles, and the 5-phase evolution roadmap (SLM → RAG/Graph → niche → agentic → citizen platform). The authoritative source for *what* we're building and in what order.
- `docs/FINE_TUNING.md` — the technical playbook for Phase 1: hardware constraints, QLoRA/Unsloth stack, data pipeline, training recipe, ablation matrix, evaluation plan. The authoritative source for *how* to build Phase 1.
- `docs/Hukuk-TR_ ... Stratejik Araştırma Raporu.md` — a broader strategic research report, **marked superseded/historical (banner at top).** It proposes a much larger base model (Gemma 4 26B A4B MoE) that conflicts with the core accessibility constraint. The operative base is **Gemma 4 12B** (`gemma-4-12B-it-qat-q4_0-unquantized`, QLoRA → Q4_0 GGUF) per `VISION.md`/`FINE_TUNING.md`/`TEKNIK_PLAN.md`. Keep the report only as an idea source for market/evolution/RAG.
- `TODO.md` — the active task list, organized by phase.

## Core constraints that shape every decision

These are non-negotiable framing from the docs — honor them in any code or recommendation:

- **Accessibility over raw performance.** Product target = run on consumer GPUs incl. ~8 GB. Chosen base: **Gemma 4 12B** (`gemma-4-12B-it-qat-q4_0-unquantized`, QLoRA fine-tune → Q4_0 GGUF ~6.5GB deploy). The 8GB end-user target is achieved via QAT → Q4_0 quantization after fine-tuning, not by limiting training to a 4B model.
- **Actual dev machine (corrected 2026-05-29): RTX 5070 Laptop, ~12 GB VRAM, Blackwell (sm_120), CUDA 13.1** — NOT the RTX 4070 / 8 GB the older docs assume. 12B QLoRA on 12 GB is tight (batch=1, gradient_checkpointing required) but feasible. ⚠️ Blackwell/sm_120 + CUDA 13.1 is bleeding-edge: PyTorch, `bitsandbytes`, `flash-attn`, `Unsloth` all need recent Blackwell-compatible builds. The 8 GB figure in older docs is the *end-user accessibility target*, not our training rig.
- **Local machine is for prototyping; real training runs go to the cloud** (Colab Pro A100 40GB, Kaggle, or RunPod). Validate the pipeline locally on tiny models (Gemma 3 270M smoke test) before spending cloud quota.
- **Currency lives in the library, not the model's brain.** Laws change; weights don't. Keep legal-currency concerns for the Phase 2 RAG/Graph layer — do not try to bake current statutes into fine-tuning.
- **Citizen-facing language, not lawyer jargon.** Default output behavior is legal-term → plain-Turkish translation.
- **License-clean data.** Use only public/open sources (Mevzuat.gov.tr, Resmi Gazete, Yargıtay open portal, Kaggle/HF open datasets). **Never** use commercial sources (Lexpera, Kazancı) — copyright poison whether the repo stays private/commercial or weights are published later. Mask PII in training data. (Repo itself is private + proprietary; see project framing above.)

## Intended technical stack (from FINE_TUNING.md — not yet set up)

When scaffolding the project, build toward this stack:

- **Environment:** `uv` + Python 3.11. WSL2 (Ubuntu 22.04) + **Blackwell-compatible CUDA (13.x — exact version verified at install; NOT 12.1)** recommended over native Windows to reduce `bitsandbytes`/`flash-attn` pain. ⚠️ sm_120 needs recent Blackwell-built wheels.
- **Training:** PyTorch 2.4+, Unsloth (primary; fall back to TRL+PEFT+transformers for unsupported models), bitsandbytes 0.43+ (NF4 4-bit), FlashAttention-2.
- **Method:** QLoRA — `r=16`, `lora_alpha=32`, `target_modules="all-linear"`, `lora_dropout=0.05`, `batch=1`, `gradient_checkpointing=True`. Gemma 4 12B encoder-free unified mimarisi — ayrı vision/audio encoder yok, tüm modality aynı decoder'dan geçer; text-only SFT multimodal yeteneği bozmaz. Model kartı teyitli: native OCR (Türkçe dahil), el yazısı tanıma, document/PDF parsing, ses girişi. Faz 3'te belge fotoğrafı + sesli soru use case'leri devreye girer; `visual_tokens=560-1120` belge görselleri için gerekli. See `FINE_TUNING.md §2` for the full config and `§5` for the training recipe.
- **Deploy pipeline:** Fine-tune (NF4 QLoRA) → merge (bf16) → Q4_0 quantize via llama.cpp → GGUF ~6.5GB → 8GB VRAM end-user.
- **Data format:** chat-template JSON (`messages` with `user`/`assistant` roles), Gemma-compatible. Four task variants: Q&A, term simplification, statute summarization, scenario→citation.
- **Eval:** lm-eval-harness + a custom Turkish legal benchmark (bar exam questions, term-simplification accuracy, LLM-as-judge with GPT-4o, ≥2 human lawyer annotators with Cohen's κ).
- **Tracking / reproducibility:** Weights & Biases; DVC or HF Hub for model+dataset versioning; fixed seeds, locked requirements.

## Working notes

- Project docs and the working language are **Turkish.** Match that language in docs, comments, and commit messages unless asked otherwise. Code identifiers stay in English.
- This is **not a git repository yet** and there is no build/test/lint setup. When the first code lands, `git init` and establish these. Until then, "the build" is conceptual.
- Phase ordering is strict and deliberate (`VISION.md §2`). Don't jump ahead to RAG/Graph (Phase 2) or agents (Phase 3) while Phase 1 (a fine-tuned, benchmarked base model) is incomplete — each phase is a self-contained OSS deliverable.
- **`docs/TEKNIK_PLAN.md` is the active execute plan** (full roadmap + detailed Phase 1 steps + locked decisions). **`knowledge/summary_mecellem_turkish_legal.md`** captures the key prior-art findings. Read both before doing Phase 1 work.
- **Phase 1 base model: Gemma 4 12B** (`google/gemma-4-12B-it-qat-q4_0-unquantized`, updated 2026-06-07; was Qwen3.5-4B). We do our OWN fine-tune. We reuse Mecellem's open recipe (cleaning chain, curriculum), eval model (`newmindai/Muhakim`), and Apache-2.0 code — but adapt to Gemma 4 architecture. TurboQuant (arXiv:2504.19874) noted for Phase 3 KV-cache serving; see `knowledge/summary_turboquant.md`.
- **Data: `docs/VERI_PLANI.md` is the authoritative data plan.** Hard rule, learned the hard way: **EDA-verify every dataset before trusting it** — `newmindai/EuroHPC-Legal` looked great (43K, Apache 2.0) but sampling revealed garbage (mismatched Q&A, hallucinated laws, Ottoman-era content) and was rejected. Scope is **current Republic-of-Turkey legislation only.** Ground truth = Mevzuat.gov.tr. Verified-usable so far: `OrionCAF/turkish_law_qa_dataset`, `Renicames/turkish-law-chatbot` (both Apache 2.0). Data we lack (plain-language, citizen-niche, scenario→statute) is produced via **grounded synthetic generation** (real statute text → LLM generates pairs → verify). `scripts/scan_hf_datasets.py` scans + EDA-peeks HF candidates; `scripts/eda_datasets.py` + `scripts/build_sft_dataset.py` built `data/processed/sft_v0/` (~32K Q&A).
- **Live legislation source: the `bedesten.adalet.gov.tr/mevzuat` JSON API** — reverse-engineered from `saidsurucu/mevzuat-mcp` (MIT) and tested working. Auth-free, no Playwright. Search + full text + article tree; same backend also serves case law (içtihat) for Phase 2. Contract reference: `docs/BEDESTEN_API.md`, probe client: `scripts/bedesten_probe.py`. **Requires a Turkish IP** (gov firewall blocks foreign/VPN IPs — both mevzuat.gov.tr and bedesten). We use the live API over the frozen `muhammetakkurt/mevzuat-gov-dataset` (907 laws, Sept 2024) when freshness/coverage matters.
