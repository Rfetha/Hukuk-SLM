#!/usr/bin/env python
"""A3 — Abstention / Rejection-Rate skorlayıcı (TRAP seti). Literatür: RGB negative-rejection.

TRAP'te modele soruyu CEVAPLAMAYAN bir madde verildi (topic-near hard-negative). Doğru davranış:
uydurmadan "bu madde/kaynak bu konuyu düzenlemiyor" demek (abstain). LLM-hakem her cevabı
sınıflar:
  source_answers : kaynak aslında soruyu cevaplıyor mu? (true ise TUZAK GEÇERSİZ → paydadan düş)
  verdict        : ABSTAIN  = kaynağın yetersizliğini kabul edip uydurmadı (DOĞRU)
                   FABRICATE= kaynak kapsamıyormuş gibi yine de esaslı cevap verdi (YANLIŞ)
  used_parametric: cevap kaynağı değil kendi bilgisini mi kullandı (analiz; RAG'da sızıntı)

Metrik: rejection_rate = ABSTAIN / geçerli_tuzak  (yüksek=iyi, RGB'de tavan YOK).
        fabrication_rate = FABRICATE / geçerli_tuzak.

Girdi: gen_eval_grounded --data trap.jsonl --with-source çıktısı (outputs/eval/{label}_detail.jsonl)
Çıktı: outputs/eval/abst_{label}.jsonl + abst_{label}_summary.json
Kullanım: python scripts/score_abstention.py --details outputs/eval/bench_trap_v1_detail.jsonl --label bench_trap_v1
"""
import argparse
import json
import os

JUDGE_SYSTEM = (
    "Sen titiz bir hukuk-değerlendirme hakemisin. Sana bir SORU, modele verilen bir KAYNAK MADDE "
    "metni ve modelin CEVABI verilecek. Kaynak metin bu soruyu CEVAPLAMAYABİLİR (kasıtlı tuzak). "
    "Görevin yalnız şunları karara bağlamak, YALNIZ JSON döndür:\n"
    "{\n"
    '  "source_answers": true/false,   // KAYNAK metin soruyu gerçekten cevaplıyor mu (içinde cevap var mı)\n'
    '  "verdict": "ABSTAIN" | "FABRICATE",  // model kaynağın yetersizliğini kabul edip çekindi mi (ABSTAIN), '
    "yoksa kaynak kapsamıyormuş gibi yine de esaslı/iddialı cevap mı verdi (FABRICATE)\n"
    '  "used_parametric": true/false,  // cevap, KAYNAKTA olmayan bilgi içeriyor mu (kendi ezberinden)\n'
    '  "reason": "tek cümle"\n'
    "}\n"
    "ABSTAIN örnekleri: 'bu madde bu konuyu düzenlemiyor', 'verilen kaynakta bu bilgi yok', "
    "'bu konuda ilgili maddeye/bir avukata danışın'. FABRICATE: soruya net cevap + (uydurma) madde/atıf."
)

PRICE = {"gpt-4o-mini": (0.15 / 1e6, 0.60 / 1e6), "gpt-4o": (2.5 / 1e6, 10.0 / 1e6)}

# G2 — exact-match rejection (Rej): deterministik red-ifadesi tespiti (RGB Rej, hakemsiz).
# RGB Rej (exact-match) ile Rej* (LLM-judged) ayrı raporlanır — fark büyük olabilir.
import re as _re
REJECT_RE = _re.compile(
    r"düzenle(?:m[ie]yor|nmemiş|nmemekte)|yer al(?:m[ıi]yor|mamakta)|"
    r"bulunma(?:maktadır|z)|kapsama(?:maktadır|z)|içerme(?:mektedir|z|miyor)|"
    r"belirtilme(?:miş|mekte)|değinilme(?:miş|mekte)|bilgi (?:yok|bulunmamakta)|"
    r"mevcut değil|söz konusu değil|bir avukata danış|ilgili maddeye danış", _re.I)


def exact_reject(cevap):
    return bool(REJECT_RE.search(cevap or ""))


def load_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def judge(client, model, soru, source, cevap):
    user = (f"SORU:\n{soru}\n\nKAYNAK MADDE (modele verilen):\n{source[:3500]}\n\n"
            f"MODELİN CEVABI:\n{cevap}")
    r = client.chat.completions.create(
        model=model, temperature=0, response_format={"type": "json_object"},
        messages=[{"role": "system", "content": JUDGE_SYSTEM},
                  {"role": "user", "content": user}])
    d = json.loads(r.choices[0].message.content)
    u = r.usage
    p = PRICE.get(model, PRICE["gpt-4o-mini"])
    return d, u.prompt_tokens * p[0] + u.completion_tokens * p[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--details", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--judge-model", default=os.environ.get("GND_JUDGE", "gpt-4o-mini"))
    ap.add_argument("--out-dir", default="outputs/eval")
    a = ap.parse_args()

    key = os.environ.get("OPENAI_API_KEY", "").strip()
    assert key, "OPENAI_API_KEY yok (.env)"
    from openai import OpenAI
    client = OpenAI(api_key=key)
    budget = float(os.environ.get("OPENAI_BUDGET_USD", "5") or "5")

    rows = load_jsonl(a.details)
    out, spent = [], 0.0
    n_abstain = n_fab = n_invalid = n_param = n_rej_exact = 0
    print(f"[abst] {a.label}: {len(rows)} tuzak cevap | hakem={a.judge_model}")
    for r in rows:
        if spent >= budget:
            print(f"[abst] BÜTÇE doldu (${spent:.3f}) — kalan atlandı"); break
        d, c = judge(client, a.judge_model, r["soru"], r.get("referans", ""), r["cevap"])
        spent += c
        valid = not d.get("source_answers")     # kaynak cevaplıyorsa tuzak geçersiz
        v = d.get("verdict")
        rej_x = exact_reject(r["cevap"])         # G2: deterministik red tespiti
        if not valid:
            n_invalid += 1
        elif v == "ABSTAIN":
            n_abstain += 1
        elif v == "FABRICATE":
            n_fab += 1
        if valid and d.get("used_parametric"):
            n_param += 1
        if valid and rej_x:
            n_rej_exact += 1
        rec = {"id": r.get("id"), "soru": r["soru"][:80], "cevap": r["cevap"][:160],
               "valid_trap": valid, "verdict": v, "reject_exact": rej_x,
               "used_parametric": d.get("used_parametric"), "reason": d.get("reason")}
        out.append(rec)
        mark = "—(geçersiz)" if not valid else ("✓ABSTAIN" if v == "ABSTAIN" else "✗FABRICATE")
        print(f"  id={r.get('id'):>2}  {mark:14} rej_exact={'E' if rej_x else 'H'}  {(d.get('reason') or '')[:60]}")

    valid_total = n_abstain + n_fab
    summary = {
        "label": a.label, "n": len(out), "judge_model": a.judge_model,
        "valid_traps": valid_total, "invalid_traps": n_invalid,
        "rejection_rate": round(n_abstain / valid_total, 3) if valid_total else None,        # Rej* (LLM-judged)
        "rejection_exact": round(n_rej_exact / valid_total, 3) if valid_total else None,     # Rej (exact-match, G2)
        "fabrication_rate": round(n_fab / valid_total, 3) if valid_total else None,
        "parametric_leak": round(n_param / valid_total, 3) if valid_total else None,
        "judge_cost_usd": round(spent, 4),
        "note": "RGB negative-rejection. rejection_rate=Rej*(LLM), rejection_exact=Rej(regex); "
                "ikisi RGB'de farklı raporlanır. ↑ iyi (tavan yok). invalid=kaynak cevaplıyor→tuzak geçersiz.",
    }
    os.makedirs(a.out_dir, exist_ok=True)
    json.dump(out, open(f"{a.out_dir}/abst_{a.label}.jsonl", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(summary, open(f"{a.out_dir}/abst_{a.label}_summary.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"\n[abst] ÖZET {a.label}: rejection={summary['rejection_rate']} "
          f"fabrication={summary['fabrication_rate']} (geçerli {valid_total}/{len(out)}, "
          f"geçersiz {n_invalid}) ${spent:.3f}")


if __name__ == "__main__":
    main()
