#!/usr/bin/env python
"""
HakHukuk — eval terazisi (Faz 1, Adım 1-2).

Akış: model (base VEYA base+adapter, 4-bit) → sabit eval örnekleminde cevap üret
      → GPT-4o-mini hakem (doğruluk + sade dil rubriği) → ortalama skor
      → göz testi markdown dökümü (insan okuması için).

Karar gerekçesi: memory [[eval-harness-decision]]. Sabit örneklem:
`data/eval/eval_sample_v1.jsonl` (make_eval_sample.py ile donduruldu) — base ve
v0 (ve sonraki tüm iterasyonlar) TAM AYNI sorularla ölçülür.

Bütçe: OPENAI_BUDGET_USD (.env) aşılırsa hakem çağrıları durur, ama generation
sürer ve göz testi yine dökülür (hakemsiz skor = None).

Kullanım:
  # Ham base (referans):
  python scripts/eval.py --label base
  # v0 adapter:
  python scripts/eval.py --label v0 --adapter outputs/v0
  # Smoke (1 soru, hakemsiz — pipeline testi):
  python scripts/eval.py --label smoke --n 1 --no-judge
"""
import argparse
import json
import os
import sys
import time

# Unsloth, torch'tan ÖNCE (train_sft.py ile aynı kural).
from unsloth import FastModel

import torch

# train_sft.py ile AYNI system prompt — eğitim/eval tutarlı olsun.
SYSTEM_PROMPT = (
    "Sen HakHukuk'sun. Türk hukuku hakkında sade, anlaşılır Türkçe bilgi verirsin.\n"
    "Emin olmadığın konularda \"Bu konuda güncel mevzuata veya bir avukata "
    "danışmanızı öneririm\" dersin.\n"
    "Asla kanun maddesi veya bilgi uydurmaz, tahmin etmezsin.\n"
    "Bu yanıt hukuki tavsiye değil, bilgilendirme amaçlıdır."
)

# gpt-4o-mini fiyat (USD / 1M token) — bütçe tahmini için.
PRICE_IN = 0.15 / 1_000_000
PRICE_OUT = 0.60 / 1_000_000

JUDGE_SYSTEM = (
    "Sen Türk hukukunda uzman, titiz bir değerlendirmecisin. Bir vatandaşın hukuk "
    "sorusu, gerçek bir avukatın referans cevabı ve bir yapay zekâ modelinin cevabı "
    "verilecek. Modeli İKİ eksende 1-10 puanla:\n"
    "1) dogruluk: Hukuki içerik referansla tutarlı mı, uydurma kanun/yanlış bilgi "
    "var mı? (10=tam doğru, 1=ciddi yanlış/halüsinasyon)\n"
    "2) sadelik: Sıradan bir vatandaşın anlayacağı sade Türkçe mi, jargon az mı? "
    "(10=çok sade ve anlaşılır, 1=ağır hukuk jargonu)\n"
    "SADECE şu JSON formatında yanıt ver, başka hiçbir şey yazma:\n"
    '{"dogruluk": <1-10>, "sadelik": <1-10>, "gerekce": "<tek cümle>"}'
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default=os.environ.get(
        "BASE_MODEL", "google/gemma-4-12B-it-qat-q4_0-unquantized"))
    p.add_argument("--adapter", default=None,
                   help="LoRA adapter dizini (ör. outputs/v0); yoksa ham base")
    p.add_argument("--eval-set", default="data/eval/eval_sample_v1.jsonl")
    p.add_argument("--label", default="base", help="rapor/çıktı etiketi")
    p.add_argument("--n", type=int, default=-1, help="ilk N soru (-1=hepsi)")
    p.add_argument("--max-seq-len", type=int, default=2048)
    p.add_argument("--max-new-tokens", type=int, default=512)
    p.add_argument("--out-dir", default="outputs/eval")
    p.add_argument("--judge-model", default=os.environ.get("JUDGE_MODEL", "gpt-4o-mini"))
    p.add_argument("--no-judge", action="store_true", help="hakem atla (smoke/offline)")
    return p.parse_args()


def load_eval_set(path, n):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    if n is not None and n >= 0:
        rows = rows[:n]
    return rows


def build_model(args):
    model, tokenizer = FastModel.from_pretrained(
        model_name=args.model,
        max_seq_length=args.max_seq_len,
        load_in_4bit=True,
        full_finetuning=False,
    )
    if args.adapter:
        # Eğitilmiş LoRA adapter'ı base'in üstüne yükle.
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, args.adapter)
        print(f"[eval] adapter yüklendi: {args.adapter}")
    FastModel.for_inference(model)
    return model, tokenizer


def generate(model, tokenizer, soru, max_new_tokens):
    msgs = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": soru},
    ]
    inputs = tokenizer.apply_chat_template(
        msgs, tokenize=True, add_generation_prompt=True,
        return_tensors="pt",
    ).to(model.device)
    with torch.no_grad():
        out = model.generate(
            input_ids=inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,            # deterministik — tekrar-üretilebilir eval
            temperature=None,
            top_p=None,
            top_k=None,
            pad_token_id=tokenizer.eos_token_id,
        )
    gen = out[0][inputs.shape[1]:]
    return tokenizer.decode(gen, skip_special_tokens=True).strip()


def judge(client, model_name, soru, referans, cevap):
    """GPT-4o-mini hakem → (dogruluk, sadelik, gerekce, in_tok, out_tok)."""
    user = (
        f"SORU:\n{soru}\n\n"
        f"REFERANS AVUKAT CEVABI:\n{referans}\n\n"
        f"MODEL CEVABI:\n{cevap}\n\n"
        "Yukarıdaki rubrikle JSON ver."
    )
    resp = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "system", "content": JUDGE_SYSTEM},
                  {"role": "user", "content": user}],
        temperature=0,
        response_format={"type": "json_object"},
    )
    content = resp.choices[0].message.content
    usage = resp.usage
    data = json.loads(content)
    return (
        float(data.get("dogruluk", 0)),
        float(data.get("sadelik", 0)),
        str(data.get("gerekce", "")),
        usage.prompt_tokens,
        usage.completion_tokens,
    )


def main():
    args = parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    rows = load_eval_set(args.eval_set, args.n)
    print(f"[eval] {args.label}: {len(rows)} soru | model={args.model} "
          f"| adapter={args.adapter or '—'}")

    # --- Hakem istemcisi (varsa) ---
    use_judge = not args.no_judge
    client = None
    budget = float(os.environ.get("OPENAI_BUDGET_USD", "0") or "0")
    if use_judge:
        key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not key:
            print("[eval] UYARI: OPENAI_API_KEY yok → hakem atlanıyor.")
            use_judge = False
        else:
            from openai import OpenAI
            client = OpenAI(api_key=key)

    model, tokenizer = build_model(args)

    results = []
    spent = 0.0
    judge_stopped = False
    t0 = time.time()
    for i, r in enumerate(rows):
        soru = r["soru"]
        referans = r.get("referans_cevap", "")
        cevap = generate(model, tokenizer, soru, args.max_new_tokens)

        rec = {"id": r.get("id", i), "soru": soru, "referans": referans,
               "cevap": cevap, "dogruluk": None, "sadelik": None, "gerekce": None}

        if use_judge and not judge_stopped:
            try:
                d, s, g, it, ot = judge(client, args.judge_model, soru, referans, cevap)
                spent += it * PRICE_IN + ot * PRICE_OUT
                rec.update(dogruluk=d, sadelik=s, gerekce=g)
                if budget and spent >= budget:
                    print(f"[eval] BÜTÇE doldu (${spent:.4f} ≥ ${budget}) "
                          f"→ kalan sorularda hakem atlanır.")
                    judge_stopped = True
            except Exception as e:
                print(f"[eval] hakem hatası (soru {i}): {e} → bu soru hakemsiz.")
        results.append(rec)
        sc = (f"dog={rec['dogruluk']} sad={rec['sadelik']}"
              if rec["dogruluk"] is not None else "hakemsiz")
        print(f"  [{i+1}/{len(rows)}] {sc} | {time.time()-t0:.0f}s")

    # --- Skor özeti ---
    judged = [r for r in results if r["dogruluk"] is not None]
    summary = {"label": args.label, "n": len(results), "n_judged": len(judged),
               "judge_cost_usd": round(spent, 4)}
    if judged:
        summary["dogruluk_ort"] = round(sum(r["dogruluk"] for r in judged) / len(judged), 2)
        summary["sadelik_ort"] = round(sum(r["sadelik"] for r in judged) / len(judged), 2)
    else:
        summary["dogruluk_ort"] = None
        summary["sadelik_ort"] = None

    # --- Çıktılar ---
    detail_path = os.path.join(args.out_dir, f"{args.label}_detail.jsonl")
    with open(detail_path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    summary_path = os.path.join(args.out_dir, f"{args.label}_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    # Göz testi markdown — insan okuması (ilk 10 + skorlar).
    goz_path = os.path.join(args.out_dir, f"{args.label}_goz_testi.md")
    with open(goz_path, "w", encoding="utf-8") as f:
        f.write(f"# Göz Testi — {args.label}\n\n")
        f.write(f"Skor: doğruluk={summary['dogruluk_ort']} "
                f"sadelik={summary['sadelik_ort']} "
                f"(n={summary['n']}, hakem={summary['n_judged']}, "
                f"maliyet=${summary['judge_cost_usd']})\n\n---\n\n")
        for r in results:
            f.write(f"## Soru {r['id']}\n\n")
            f.write(f"**Soru:** {r['soru']}\n\n")
            f.write(f"**Model cevabı:** {r['cevap']}\n\n")
            f.write(f"**Referans (avukat):** {r['referans']}\n\n")
            if r["dogruluk"] is not None:
                f.write(f"**Hakem:** doğruluk={r['dogruluk']} sadelik={r['sadelik']} "
                        f"— {r['gerekce']}\n\n")
            f.write("---\n\n")

    print(f"\n[eval] ÖZET {args.label}: {json.dumps(summary, ensure_ascii=False)}")
    print(f"[eval] detay → {detail_path}")
    print(f"[eval] göz testi → {goz_path}")
    return summary


if __name__ == "__main__":
    main()
