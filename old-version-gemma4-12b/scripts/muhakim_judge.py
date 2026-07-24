#!/usr/bin/env python3
"""Muhakim (newmindai/Muhakim, ArmoRM 8B) ile kayıtlı eval cevaplarını puanla.

Amaç: BİZİM in-house eval'i (GPT-4o-mini hakem, doğruluk+sadelik) BAŞKA bir
ekibin kalibrasyonuyla (Muhakim çok-amaçlı ödül modeli) karşılaştırmak.

Muhakim referans-BAĞIMSIZ bir reward model'dir:
  girdi  = (soru, cevap)  →  çıktı = gated skalar `score` + 5 eksen `rewards`
  eksenler = [statute_reference, legal_accuracy, case_law_reference,
              linguistic_coherence, depth_coverage]
  ⚠️ "sadelik/vatandaş dili" ekseni YOK → avukatça derinlik/atıf ödüllendirir.

SIRALI çalışır: bu script çalışırken SLM yüklü DEĞİL (VRAM yarışı yok).
8B bf16 ~16GB > 12GB → 8-bit (varsa 4-bit) yükle. trust_remote_code şart.

Kullanım:
  python scripts/muhakim_judge.py                    # base + v0 detail'leri
  python scripts/muhakim_judge.py --details outputs/eval/v0_detail.jsonl
  python scripts/muhakim_judge.py --format plain      # "User:/Assistant:" düz
"""
import argparse
import json
import os
import sys

import torch

OBJ = ["statute_reference", "legal_accuracy", "case_law_reference",
       "linguistic_coherence", "depth_coverage"]
# Yerel kopya tercih edilir: HF repo'su tek-shard'ı standart-dışı isimlendirmiş
# (model-00001-of-00001.safetensors, index json yok) → transformers bulamıyor.
# scripts/dl_muhakim.py ile models/Muhakim'e indirilip model.safetensors'a çevrildi.
_LOCAL = "models/Muhakim"
MODEL_ID = os.environ.get("MUHAKIM_MODEL") or (
    _LOCAL if os.path.isdir(_LOCAL) else "newmindai/Muhakim")


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--details", nargs="+",
                   default=["outputs/eval/base_detail.jsonl",
                            "outputs/eval/v0_detail.jsonl"])
    p.add_argument("--out-dir", default="outputs/eval")
    p.add_argument("--max-seq-len", type=int, default=2048)
    p.add_argument("--format", choices=["chat", "plain"], default="chat",
                   help="chat=tokenizer.apply_chat_template (ArmoRM doğru kullanım); "
                        "plain=model kartındaki 'User:/Assistant:' düz metin")
    p.add_argument("--load", choices=["8bit", "4bit", "bf16"], default="8bit")
    return p.parse_args()


def load_model(load_mode):
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    kw = dict(trust_remote_code=True, torch_dtype=torch.bfloat16,
              device_map="auto")
    if load_mode in ("8bit", "4bit"):
        from transformers import BitsAndBytesConfig
        if load_mode == "8bit":
            qc = BitsAndBytesConfig(load_in_8bit=True)
        else:
            qc = BitsAndBytesConfig(load_in_4bit=True,
                                    bnb_4bit_quant_type="nf4",
                                    bnb_4bit_compute_dtype=torch.bfloat16)
        kw["quantization_config"] = qc
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID, **kw)
    model.eval()
    return tok, model


def build_text(tok, soru, cevap, fmt):
    if fmt == "plain":
        return f"User: {soru}\nAssistant: {cevap}"
    msgs = [{"role": "user", "content": soru},
            {"role": "assistant", "content": cevap}]
    try:
        return tok.apply_chat_template(msgs, tokenize=False)
    except Exception:
        return f"User: {soru}\nAssistant: {cevap}"


@torch.no_grad()
def score_one(tok, model, text, max_len):
    enc = tok(text, return_tensors="pt", truncation=True, max_length=max_len)
    enc = {k: v.to(model.device) for k, v in enc.items()}
    out = model(**enc)
    score = float(out.score.squeeze().item())
    rewards = [float(x) for x in out.rewards.squeeze().tolist()]
    return score, rewards


def main():
    args = parse_args()
    print(f"[muhakim] yükleniyor: {MODEL_ID} ({args.load}) …", flush=True)
    tok, model = load_model(args.load)
    dev = next(model.parameters()).device
    if torch.cuda.is_available():
        print(f"[muhakim] VRAM: {torch.cuda.memory_allocated()/1e9:.1f}GB | dev={dev}",
              flush=True)

    printed_sample = False
    all_summ = {}
    for path in args.details:
        if not os.path.exists(path):
            print(f"[muhakim] ATLA (yok): {path}", flush=True)
            continue
        label = os.path.basename(path).replace("_detail.jsonl", "")
        rows = [json.loads(l) for l in open(path, encoding="utf-8")]
        out_rows = []
        for i, r in enumerate(rows):
            text = build_text(tok, r["soru"], r["cevap"], args.format)
            if not printed_sample:
                print("\n[muhakim] ÖRNEK girdi (ilk):\n" + "-" * 40
                      + f"\n{text[:600]}\n" + "-" * 40 + "\n", flush=True)
                printed_sample = True
            score, rewards = score_one(tok, model, text, args.max_seq_len)
            rec = {"id": r.get("id", i), "soru_n": len(r["soru"].split()),
                   "cevap_n": len(r["cevap"].split()),
                   "muhakim_score": round(score, 4),
                   "dogruluk": r.get("dogruluk"), "sadelik": r.get("sadelik")}
            rec.update({f"m_{o}": round(v, 4) for o, v in zip(OBJ, rewards)})
            out_rows.append(rec)
            print(f"[{label}] id={rec['id']:>2} score={score:+.3f} "
                  f"legal_acc={rec['m_legal_accuracy']:+.3f} "
                  f"(GPT dog={rec['dogruluk']} sad={rec['sadelik']})", flush=True)

        op = os.path.join(args.out_dir, f"muhakim_{label}.jsonl")
        with open(op, "w", encoding="utf-8") as f:
            for rec in out_rows:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        n = len(out_rows)
        summ = {"label": label, "n": n,
                "muhakim_score_ort": round(sum(x["muhakim_score"] for x in out_rows) / n, 4)}
        for o in OBJ:
            summ[f"{o}_ort"] = round(sum(x[f"m_{o}"] for x in out_rows) / n, 4)
        all_summ[label] = summ
        print(f"\n[muhakim] {label} ÖZET: {json.dumps(summ, ensure_ascii=False)}\n",
              flush=True)

    sp = os.path.join(args.out_dir, "muhakim_summary.json")
    json.dump(all_summ, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"[muhakim] özet → {sp}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
