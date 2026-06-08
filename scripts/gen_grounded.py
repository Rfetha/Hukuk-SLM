#!/usr/bin/env python3
"""Grounded SFT örnek üretici — gerçek kanun maddesi → (soru, doğru+sade+atıflı cevap).

Sorun (ölçüldü): 32K forum verisi base'den düşük doğrulukta (legal_acc 0.274 < base 0.362)
→ modele doğruluk öğretemez. Çözüm: doğruluğu GERÇEK MADDEDEN imal et — cevap maddeye
bağlı olduğunda doğruluk imal edilir. Çıta: Muhakim legal_acc > 0.362 (base'i geç).

İki üretici (bake-off): `--backend gpt` (gpt-4o-mini) vs `--backend local` (Gemma base).
Kazananla ~20K'ya ölçeklenecek. "Güvenmeden önce doğrula."

Çıktı: `outputs/eval/{label}_detail.jsonl` (id/soru/referans=madde/cevap/kanun/madde_no)
→ `muhakim_judge.py` ile doğruluk, `--judge` ile GPT sadelik puanlanır.

Kullanım:
  python scripts/gen_grounded.py --backend gpt   --n 25 --label gnd_gpt   --judge
  python scripts/gen_grounded.py --backend local --n 25 --label gnd_local --judge
"""
import argparse
import json
import os
import random
import re

MADDE_PATH = "data/raw/mevzuat_maddeler.jsonl"
MAX_MADDE_CHARS = 3000

# Vatandaş-merkezli çekirdek kanunlar (eval seti bunlarla örtüşüyor: icra/kira/miras/iş/ceza).
CITIZEN_LAWS = [
    "MEDENİ", "BORÇLAR", "İCRA VE İFLAS", "İŞ KANUNU", "CEZA", "TÜKETİCİNİN",
    "KİRA", "AİLE", "CEZA MUHAKEMESI", "HUKUK MUHAKEMELERİ", "KAT MÜLKİYETİ",
]

GEN_SYSTEM = (
    "Sen Türk hukuku için yüksek kaliteli eğitim verisi üreten bir uzmansın. "
    "Sana GERÇEK bir kanun maddesi verilir; görevin o maddeye DAYALI tek bir "
    "(soru, cevap) örneği üretmek. Madde dışına çıkma, bilgi/kanun uydurma."
)

GEN_TEMPLATE = (
    "Aşağıda gerçek bir Türk kanun maddesi var. Buna dayanarak BİR eğitim örneği üret:\n"
    "- SORU: sıradan bir vatandaşın bu konuda gerçek hayatta soracağı, günlük dilde, "
    "doğal bir soru (hukuk jargonu kullanma).\n"
    "- CEVAP: SADECE bu maddeye dayanarak; hukuken DOĞRU, sade vatandaş Türkçesiyle, "
    "kısa ama TAM; cevabın sonunda \"(<kanun adı>, <madde no>)\" şeklinde atıf ver. "
    "Madde dışına çıkma, uydurma.\n\n"
    "KANUN: {kanun} — {madde_no}\n"
    "MADDE METNİ:\n{text}\n\n"
    "ÇIKTI formatı (başka hiçbir şey yazma):\n"
    "SORU: <soru>\n"
    "CEVAP: <cevap>"
)

# --- inline GPT hakem (referans = GERÇEK madde → doğruluk = maddeye sadakat) ---
JUDGE_SYSTEM = (
    "Bir vatandaş hukuk sorusu, kaynak kanun maddesi ve bir cevap verilecek. İKİ eksende "
    "1-10 puanla:\n"
    "1) dogruluk: Cevap KAYNAK MADDEYE sadık mı, uydurma/çelişki var mı? "
    "(10=tam sadık, 1=çelişkili/uydurma)\n"
    "2) sadelik: Sıradan vatandaşın anlayacağı sade Türkçe mi? (10=çok sade, 1=ağır jargon)\n"
    'SADECE JSON: {"dogruluk": <1-10>, "sadelik": <1-10>, "gerekce": "<tek cümle>"}'
)
PRICE_IN, PRICE_OUT = 0.15 / 1e6, 0.60 / 1e6


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--backend", choices=["gpt", "local"], required=True)
    p.add_argument("--label", required=True)
    p.add_argument("--n", type=int, default=25)
    p.add_argument("--seed", type=int, default=3407)
    p.add_argument("--out-dir", default="outputs/eval")
    p.add_argument("--gpt-model", default=os.environ.get("GEN_MODEL", "gpt-4o-mini"))
    p.add_argument("--base-model", default=os.environ.get(
        "BASE_MODEL", "google/gemma-4-12B-it-qat-q4_0-unquantized"))
    p.add_argument("--max-new-tokens", type=int, default=400)
    p.add_argument("--judge", action="store_true", help="inline GPT sadelik+sadakat hakemi")
    p.add_argument("--citizen-only", action="store_true", default=True)
    return p.parse_args()


def usable(r):
    t = (r.get("text") or "").strip()
    if len(t) < 250:
        return False
    low = t.lower()
    if t.startswith("(") and ("işlenmiştir" in low or "değiştir" in low[:120]):
        return False
    if "yürürlükten kaldırıl" in low[:80]:
        return False
    return True


def parse_gen(txt):
    s = re.search(r"SORU:\s*(.+?)\s*CEVAP:\s*(.+)", txt, re.S | re.I)
    if not s:
        return None, None
    return s.group(1).strip(), s.group(2).strip()


def gen_gpt(client, model, prompt):
    r = client.chat.completions.create(
        model=model, temperature=0.7,
        messages=[{"role": "system", "content": GEN_SYSTEM},
                  {"role": "user", "content": prompt}])
    u = r.usage
    return r.choices[0].message.content, u.prompt_tokens, u.completion_tokens


def judge_gpt(client, model, soru, madde, cevap):
    user = f"SORU:\n{soru}\n\nKAYNAK MADDE:\n{madde[:MAX_MADDE_CHARS]}\n\nCEVAP:\n{cevap}"
    r = client.chat.completions.create(
        model=model, temperature=0, response_format={"type": "json_object"},
        messages=[{"role": "system", "content": JUDGE_SYSTEM},
                  {"role": "user", "content": user}])
    d = json.loads(r.choices[0].message.content)
    u = r.usage
    return (float(d.get("dogruluk", 0)), float(d.get("sadelik", 0)),
            d.get("gerekce", ""), u.prompt_tokens, u.completion_tokens)


def main():
    a = parse_args()
    rows = [json.loads(l) for l in open(MADDE_PATH, encoding="utf-8")]
    pool = [r for r in rows if usable(r)]
    if a.citizen_only:
        cz = [r for r in pool if any(k in (r.get("kanun_adi") or "").upper()
                                     for k in CITIZEN_LAWS)]
        if len(cz) >= a.n:
            pool = cz
    random.seed(a.seed)
    sample = random.sample(pool, min(a.n, len(pool)))
    print(f"[gen] backend={a.backend} havuz={len(pool)} örnek={len(sample)} seed={a.seed}")

    # --- backend kur ---
    client = None
    if a.backend == "gpt" or a.judge:
        from openai import OpenAI
        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            raise SystemExit("[gen] OPENAI_API_KEY yok (.env yükle)")
        client = OpenAI(api_key=key)
    model = tokenizer = None
    if a.backend == "local":
        import torch
        from unsloth import FastModel
        model, tokenizer = FastModel.from_pretrained(
            model_name=a.base_model, max_seq_length=4096,
            load_in_4bit=True, full_finetuning=False)
        FastModel.for_inference(model)

    def local_gen(prompt):
        import torch
        msgs = [{"role": "system", "content": GEN_SYSTEM},
                {"role": "user", "content": prompt}]
        inp = tokenizer.apply_chat_template(
            msgs, tokenize=True, add_generation_prompt=True,
            return_tensors="pt").to(model.device)
        with torch.no_grad():
            out = model.generate(input_ids=inp, max_new_tokens=a.max_new_tokens,
                                 do_sample=True, temperature=0.7, top_p=0.9,
                                 pad_token_id=tokenizer.eos_token_id)
        return tokenizer.decode(out[0][inp.shape[1]:], skip_special_tokens=True).strip()

    budget = float(os.environ.get("OPENAI_BUDGET_USD", "5"))
    spent = 0.0
    op = os.path.join(a.out_dir, f"{a.label}_detail.jsonl")
    os.makedirs(a.out_dir, exist_ok=True)
    kept = 0
    with open(op, "w", encoding="utf-8") as f:
        for i, r in enumerate(sample):
            kanun = r.get("kanun_adi", "")
            prompt = GEN_TEMPLATE.format(kanun=kanun, madde_no=r.get("madde_no", ""),
                                         text=(r.get("text") or "")[:MAX_MADDE_CHARS])
            try:
                if a.backend == "gpt":
                    raw, it, ot = gen_gpt(client, a.gpt_model, prompt)
                    spent += it * PRICE_IN + ot * PRICE_OUT
                else:
                    raw = local_gen(prompt)
            except Exception as e:
                print(f"[gen] id={i} ÜRETİM HATA: {e}")
                continue
            soru, cevap = parse_gen(raw)
            if not soru or not cevap:
                print(f"[gen] id={i} parse başarısız, atla")
                continue
            rec = {"id": i, "soru": soru, "referans": r.get("text", ""),
                   "cevap": cevap, "dogruluk": None, "sadelik": None, "gerekce": None,
                   "kanun_adi": kanun, "madde_no": r.get("madde_no"),
                   "kanun_no": r.get("kanun_no"), "source": f"grounded_{a.backend}"}
            if a.judge and spent < budget:
                try:
                    d, s, g, it, ot = judge_gpt(client, a.gpt_model,
                                                soru, r.get("text", ""), cevap)
                    spent += it * PRICE_IN + ot * PRICE_OUT
                    rec.update(dogruluk=d, sadelik=s, gerekce=g)
                except Exception as e:
                    print(f"[gen] id={i} hakem hata: {e}")
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            kept += 1
            sc = (f"dog={rec['dogruluk']} sad={rec['sadelik']}"
                  if rec["dogruluk"] is not None else "")
            print(f"[{a.label}] id={i:>2} {kanun[:28]:28s} kept ✓ {sc}")
    print(f"\n[gen] {kept}/{len(sample)} örnek → {op}  | GPT maliyet ${spent:.3f}")


if __name__ == "__main__":
    main()
