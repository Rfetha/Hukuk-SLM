#!/usr/bin/env python
"""
HakHukuk — QLoRA SFT eğitim script'i (Faz 1, Adım 3/5).

Gemma 4 12B + Unsloth QLoRA (NF4 4-bit) → vatandaş-dilli hukuk SLM.
v0 (32K jargon) ve v1 (sade + grounded) için aynı script, --data ile değişir.

Plan: docs/FAZ1_PLAN.md Adım 3. Hiperparametreler TEKNIK_PLAN.md Adım 7.
Ortam: ~/code/global_venv (Blackwell sm_120, torch 2.10+cu128, unsloth 2026.6.1).

Kullanım:
  python scripts/train_sft.py --run-name v0 \
      --data data/processed/sft_v0 --epochs 2

Not: 12GB VRAM → batch=1 + gradient_checkpointing ZORUNLU.
"""
import argparse
import os

# Unsloth, torch'tan ÖNCE import edilmeli (patch'leri uygular).
from unsloth import FastModel
from unsloth.chat_templates import train_on_responses_only

import torch
from datasets import load_dataset
from trl import SFTTrainer, SFTConfig

# TEKNIK_PLAN Adım 6 — her örneğe eklenen kimlik+davranış system prompt'u.
SYSTEM_PROMPT = (
    "Sen HakHukuk'sun. Türk hukuku hakkında sade, anlaşılır Türkçe bilgi verirsin.\n"
    "Emin olmadığın konularda \"Bu konuda güncel mevzuata veya bir avukata "
    "danışmanızı öneririm\" dersin.\n"
    "Asla kanun maddesi veya bilgi uydurmaz, tahmin etmezsin.\n"
    "Bu yanıt hukuki tavsiye değil, bilgilendirme amaçlıdır."
)

# Gemma 4 turn işaretleri — responses-only maskeleme için (sadece model cevabından loss).
# DİKKAT: Gemma 4 template'i `<|turn>user\n` / `<|turn>model\n` kullanır
# (eski Gemma'nın `<start_of_turn>...` değil). Tokenizer render'ı ile doğrulandı 2026-06-07.
GEMMA_USER_PART = "<|turn>user\n"
GEMMA_ASSISTANT_PART = "<|turn>model\n"


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="google/gemma-4-12B-it-qat-q4_0-unquantized")
    p.add_argument("--data", default="data/processed/sft_v0",
                   help="train.jsonl + validation.jsonl içeren dizin")
    p.add_argument("--run-name", default="v0")
    p.add_argument("--output-dir", default=None, help="varsayılan: outputs/<run-name>")
    p.add_argument("--max-seq-len", type=int, default=2048)
    p.add_argument("--epochs", type=float, default=2.0)
    p.add_argument("--batch", type=int, default=1)
    p.add_argument("--grad-accum", type=int, default=16)
    p.add_argument("--lr", type=float, default=2e-4)
    p.add_argument("--lora-r", type=int, default=16)
    p.add_argument("--lora-alpha", type=int, default=32)
    p.add_argument("--lora-dropout", type=float, default=0.05)
    p.add_argument("--seed", type=int, default=3407)
    p.add_argument("--no-system", action="store_true",
                   help="system prompt ekleme (ablation için)")
    p.add_argument("--wandb", action="store_true", help="W&B'ye logla")
    p.add_argument("--max-steps", type=int, default=-1, help="smoke test için sınırla")
    return p.parse_args()


def main():
    args = parse_args()
    out = args.output_dir or f"outputs/{args.run_name}"
    os.environ["WANDB_PROJECT"] = "hakhukuk-sft"
    report_to = "wandb" if args.wandb else "none"

    # --- Model + tokenizer (NF4 4-bit) ---
    model, tokenizer = FastModel.from_pretrained(
        model_name=args.model,
        max_seq_length=args.max_seq_len,
        load_in_4bit=True,           # QLoRA → NF4
        full_finetuning=False,
    )

    # --- LoRA adapter ---
    model = FastModel.get_peft_model(
        model,
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        # all-linear: Gemma'nın tüm lineer projeksiyonları
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        bias="none",
        use_gradient_checkpointing="unsloth",  # 12GB için zorunlu
        random_state=args.seed,
    )

    # --- Veri: messages → Gemma chat-template metni ---
    def to_text(example):
        msgs = example["messages"]
        if not args.no_system:
            msgs = [{"role": "system", "content": SYSTEM_PROMPT}] + msgs
        text = tokenizer.apply_chat_template(
            msgs, tokenize=False, add_generation_prompt=False,
        )
        return {"text": text}

    data_files = {"train": os.path.join(args.data, "train.jsonl"),
                  "validation": os.path.join(args.data, "validation.jsonl")}
    ds = load_dataset("json", data_files=data_files)
    ds = ds.map(to_text, remove_columns=[c for c in ds["train"].column_names])

    # --- Trainer ---
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=ds["train"],
        eval_dataset=ds["validation"],
        args=SFTConfig(
            dataset_text_field="text",
            max_seq_length=args.max_seq_len,
            per_device_train_batch_size=args.batch,
            gradient_accumulation_steps=args.grad_accum,
            warmup_ratio=0.03,
            num_train_epochs=args.epochs,
            max_steps=args.max_steps,
            learning_rate=args.lr,
            lr_scheduler_type="cosine",
            optim="adamw_8bit",
            bf16=True,
            logging_steps=10,
            save_strategy="epoch",
            eval_strategy="epoch",
            output_dir=out,
            seed=args.seed,
            report_to=report_to,
            run_name=f"hakhukuk-{args.run_name}",
        ),
    )

    # Sadece model cevabından loss (user/system tokenları maskelenir).
    trainer = train_on_responses_only(
        trainer,
        instruction_part=GEMMA_USER_PART,
        response_part=GEMMA_ASSISTANT_PART,
    )

    print(f"[train] GPU: {torch.cuda.get_device_name(0)} | "
          f"adapter r={args.lora_r} | data={args.data} | out={out}")
    trainer.train()

    # --- Adapter kaydet ---
    model.save_pretrained(out)
    tokenizer.save_pretrained(out)
    print(f"[train] bitti → adapter: {out}")


if __name__ == "__main__":
    main()
