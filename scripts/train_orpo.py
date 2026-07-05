#!/usr/bin/env python
"""v3 ADIM 6b — ORPO eğitim (MaskedORPOTrainer): near-miss abstention fix (v3_recipe).

Unsloth FastModel + TRL 0.24 ORPOTrainer subclass. base = v2b ADAPTER'dan DEVAM (grounding taşınır).
MaskedORPOTrainer: her satır `is_pref` taşır → grounding-replay satırında (is_pref=0) OR-terimi
NaN-safe SIFIRLANIR (torch.where), yalnız NLL(chosen) akar = SFT-replay. abstain-çiftinde (is_pref=1)
tam ORPO. Kaynak-doğrulandı: trl/trainer/orpo_trainer.py 0.24.0 (loss=policy_nll_loss−losses.mean()
satır 830; odds_ratio_loss per-örnek `losses` satır 675; is_pref collator else-dalında list, satır 79).

⚠️ ADIM 7 Modal smoke DOĞRULAYACAK: (a) v2b-continuation (PeftModel is_trainable) Unsloth'la çalışıyor mu,
(b) is_pref batch'te list olarak geliyor mu, (c) OOM/loss. Offline sadece syntax + tasarım doğru.

Kullanım (Modal):
  modal run modal_train.py::spawn_v3 --smoke      # önce ~50 step (para-kapısı)
  modal run modal_train.py::spawn_v3 --run-name v3 --epochs 1
"""
import argparse
import os

# Unsloth ÖNCE (patch'ler). PatchDPOTrainer → TRL DPO/ORPO trainer'larını Unsloth'a uyarlar.
from unsloth import FastModel, PatchDPOTrainer
PatchDPOTrainer()

import torch
from datasets import load_dataset
from transformers.trainer_utils import get_last_checkpoint
from trl import ORPOTrainer, ORPOConfig


class MaskedORPOTrainer(ORPOTrainer):
    """Per-satır is_pref maskesi: is_pref=0 (grounding-replay) → OR-terimi sıfırlanır (NaN-safe),
    yalnız NLL(chosen) = SFT-replay. TRL 0.24 get_batch_loss_metrics'in OR-agregasyonu değiştirilmiş
    kopyası (loss = policy_nll_loss − maskeli_mean(losses))."""

    def get_batch_loss_metrics(self, model, batch, train_eval="train"):
        metrics = {}
        # is_pref collator else-dalında list olarak gelir; concatenated_forward'a girmeden ÇIKAR.
        is_pref_raw = batch.pop("is_pref", None)

        forward_output = self.concatenated_forward(model, batch)
        (policy_chosen_logps, policy_rejected_logps, policy_chosen_logits,
         policy_rejected_logits, policy_nll_loss) = forward_output[:5]
        if self.aux_loss_enabled:
            aux_loss = forward_output[5]

        losses, chosen_rewards, rejected_rewards, log_odds_ratio, log_odds_chosen = self.odds_ratio_loss(
            policy_chosen_logps, policy_rejected_logps
        )

        # --- MASKELİ OR-AGREGASYON (NaN-safe) ---
        if is_pref_raw is not None:
            is_pref = torch.as_tensor([bool(x) for x in is_pref_raw],
                                      device=losses.device, dtype=torch.bool)
            # ⚠️ losses*mask DEĞİL: OR-loss log1p(-exp(...)) NaN üretebilir, nan*0=nan zehirler.
            # torch.where seçilmeyen daldan NaN taşımaz.
            losses = torch.where(is_pref, losses, torch.zeros_like(losses))
            or_term = losses.sum() / is_pref.sum().clamp(min=1)
        else:
            or_term = losses.mean()

        loss = policy_nll_loss - or_term        # tam ORPO loss (maskeli OR)

        reward_accuracies = (chosen_rewards > rejected_rewards).float()
        prefix = "eval_" if train_eval == "eval" else ""
        g = self.accelerator.gather_for_metrics
        metrics[f"{prefix}rewards/chosen"] = g(chosen_rewards).mean()
        metrics[f"{prefix}rewards/rejected"] = g(rejected_rewards).mean()
        metrics[f"{prefix}rewards/accuracies"] = g(reward_accuracies).mean()
        metrics[f"{prefix}rewards/margins"] = g(chosen_rewards - rejected_rewards).mean()
        metrics[f"{prefix}logps/rejected"] = g(policy_rejected_logps).detach().mean()
        metrics[f"{prefix}logps/chosen"] = g(policy_chosen_logps).detach().mean()
        metrics[f"{prefix}logits/rejected"] = g(policy_rejected_logits.detach().mean()).mean()
        metrics[f"{prefix}logits/chosen"] = g(policy_chosen_logits.detach().mean()).mean()
        # forget-vekili: grounding NLL trendi M1-risk göstergesi (v3_recipe ADIM 8).
        metrics[f"{prefix}nll_loss"] = g(policy_nll_loss).detach().mean()
        metrics[f"{prefix}log_odds_ratio"] = g(log_odds_ratio).detach().mean()
        metrics[f"{prefix}log_odds_chosen"] = g(log_odds_chosen).detach().mean()
        for k, v in metrics.items():
            metrics[k] = v.item()
        if self.aux_loss_enabled:
            loss += self.aux_loss_coef * aux_loss
        return loss, metrics


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="google/gemma-4-12B-it-qat-q4_0-unquantized")
    p.add_argument("--adapter", default="outputs/v2b", help="DEVAM edilecek v2b adapter (grounding taşır)")
    p.add_argument("--data", default="data/processed/sft_v3", help="train.jsonl + validation.jsonl")
    p.add_argument("--run-name", default="v3")
    p.add_argument("--output-dir", default=None)
    p.add_argument("--beta", type=float, default=0.1, help="ORPO OR ceza ağırlığı (recipe λ; {0.05,0.1,0.25})")
    p.add_argument("--lr", type=float, default=1e-5, help="v2b'den devam → düşük (5e-6–1e-5)")
    p.add_argument("--epochs", type=float, default=1.0)
    p.add_argument("--batch", type=int, default=1)
    p.add_argument("--grad-accum", type=int, default=64, help="per_device×grad_accum≥64 (OR-sinyali stabil)")
    p.add_argument("--max-length", type=int, default=1536)
    p.add_argument("--max-prompt-length", type=int, default=1152)
    p.add_argument("--warmup-ratio", type=float, default=0.05)
    p.add_argument("--lora-r", type=int, default=16)
    p.add_argument("--lora-alpha", type=int, default=32)
    p.add_argument("--seed", type=int, default=3407)
    p.add_argument("--max-steps", type=int, default=-1, help="smoke için sınırla")
    p.add_argument("--save-steps", type=int, default=100,
                   help="checkpoint aralığı; 2-epoch koşuda ~1-epoch ara-checkpoint için düşür (ör. 28)")
    p.add_argument("--fresh-adapter", action="store_true",
                   help="FALLBACK: v2b-continuation çalışmazsa base'e YENİ adapter (grounding'i kaybeder)")
    return p.parse_args()


def main():
    args = parse_args()
    out = args.output_dir or f"outputs/{args.run_name}"

    model, tokenizer = FastModel.from_pretrained(
        model_name=args.model, max_seq_length=args.max_length,
        load_in_4bit=True, full_finetuning=False,
    )

    if args.fresh_adapter:
        # Fallback: base'e yeni adapter (grounding taşınmaz — sadece continuation başarısızsa).
        model = FastModel.get_peft_model(
            model, r=args.lora_r, lora_alpha=args.lora_alpha, lora_dropout=0.0,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                            "gate_proj", "up_proj", "down_proj"],
            bias="none", use_gradient_checkpointing="unsloth", random_state=args.seed,
        )
        print("[orpo] ⚠️ FRESH adapter (base'den) — grounding taşınmadı", flush=True)
    else:
        # v2b-CONTINUATION: v2b LoRA'sını trainable yükle (grounding taşınır, recipe Q2).
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, args.adapter, is_trainable=True)
        print(f"[orpo] v2b-continuation: {args.adapter} (is_trainable) — grounding taşındı", flush=True)

    data_files = {"train": os.path.join(args.data, "train.jsonl"),
                  "validation": os.path.join(args.data, "validation.jsonl")}
    ds = load_dataset("json", data_files=data_files)

    cfg = ORPOConfig(
        beta=args.beta,
        max_length=args.max_length,
        max_prompt_length=args.max_prompt_length,
        per_device_train_batch_size=args.batch,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        num_train_epochs=args.epochs,
        max_steps=args.max_steps,
        warmup_ratio=args.warmup_ratio,
        lr_scheduler_type="cosine",
        optim="adamw_8bit",
        bf16=True,
        logging_steps=5,
        save_strategy="steps",
        save_steps=args.save_steps,
        save_total_limit=3,
        eval_strategy="steps" if args.max_steps < 0 else "no",
        eval_steps=100,
        output_dir=out,
        seed=args.seed,
        report_to="none",
        remove_unused_columns=False,      # is_pref sütunu KORUNSUN (ORPO zaten False set eder)
    )

    trainer = MaskedORPOTrainer(
        model=model,
        args=cfg,
        train_dataset=ds["train"],
        eval_dataset=ds["validation"],
        processing_class=tokenizer,
    )

    ckpt = get_last_checkpoint(out) if os.path.isdir(out) else None
    if ckpt:
        print(f"[orpo] RESUME → {ckpt}", flush=True)
    print(f"[orpo] GPU={torch.cuda.get_device_name(0)} | beta={args.beta} lr={args.lr} "
          f"grad_accum={args.grad_accum} | data={args.data} | out={out}", flush=True)
    trainer.train(resume_from_checkpoint=ckpt)

    model.save_pretrained(out)
    tokenizer.save_pretrained(out)
    print(f"[orpo] bitti → adapter: {out}", flush=True)


if __name__ == "__main__":
    main()
