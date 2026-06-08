#!/usr/bin/env python3
"""Birleşik skorkart — ANA = Groundedness · İKİNCİL = Muhakim · BİLGİ = Sadelik(app).

Karar (2026-06-08, [[eval-accuracy-gate]]): ürün riski = halüsinasyon → ANA kapı groundedness.
  - ANA (kapı)     = Groundedness (`groundedness.py`): Faithfulness↑, Hallucination↓,
                     wrong_ref↓ (yanlış maddeye yönlendirme), cit_recall↑. FactScore+ALCE.
  - İKİNCİL (bilgi)= Muhakim legal_accuracy/statute (ArmoRM 8B) — derinlik/atıf sinyali,
                     KAPI DEĞİL (kısa-sade'ye yanlı; paper K3 kanıtı).
  - BİLGİ (app)    = Sadelik (GPT-4o-mini) — MODEL gate değil, vatandaş-modu/app sinyali.
  - AYRIŞMA bayrağı= groundedness-faithfulness ↔ Muhakim-legal sert zıtsa → Muhakim yanlılığı
                     kanıtı + insan denetimi.

⚠️ Groundedness LLM-judge (insan-κ kalibresiz, Aşama C) → mutlak değil, model-vs-model SIRALAMA.
⚠️ Muhakim skorları reward-model logit'i (mutlak % değil) → sıralama için oku.

Girdi (groundedness.py + muhakim_judge.py + eval.py çıktıları):
  outputs/eval/gnd_{label}_summary.json   (ANA: faithfulness/hallucination/wrong_ref/recall)
  outputs/eval/gnd_{label}.jsonl          (per-soru faithfulness — ayrışma için)
  outputs/eval/muhakim_{label}.jsonl      (İKİNCİL: Muhakim per-soru)
  outputs/eval/{label}_summary.json       (BİLGİ: GPT sadelik ort)
Çıktı: outputs/PHASE1_REPORT.md
"""
import argparse
import json
import os
import statistics


def load_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8")] if os.path.exists(p) else []


def load_json(p):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--labels", nargs="+", default=["base", "v0"])
    p.add_argument("--eval-dir", default="outputs/eval")
    p.add_argument("--out", default="outputs/PHASE1_REPORT.md")
    p.add_argument("--flag-z", type=float, default=1.5,
                   help="groundedness↔Muhakim z-skor farkı bu eşiği aşarsa ayrışma bayrağı")
    return p.parse_args()


def zscores(xs):
    if len(xs) < 2:
        return [0.0] * len(xs)
    m = statistics.mean(xs)
    s = statistics.pstdev(xs) or 1.0
    return [(x - m) / s for x in xs]


def fmt(v, sign=False, nd=3):
    if v is None:
        return "—"
    return (f"{v:+.{nd}f}" if sign else f"{v:.{nd}f}")


def main():
    a = parse_args()
    ed = a.eval_dir

    per_label = {}
    pooled = []  # (label, id, faithfulness, muh_legal)
    for lbl in a.labels:
        gnd = load_json(f"{ed}/gnd_{lbl}_summary.json")
        gnd_rows = {r["id"]: r for r in load_jsonl(f"{ed}/gnd_{lbl}.jsonl")}
        muh = {r["id"]: r for r in load_jsonl(f"{ed}/muhakim_{lbl}.jsonl")}
        gpt = load_json(f"{ed}/{lbl}_summary.json")

        muh_legal = muh_statute = None
        if muh:
            mv = [m.get("m_legal_accuracy") for m in muh.values() if m.get("m_legal_accuracy") is not None]
            sv = [m.get("m_statute_reference") for m in muh.values() if m.get("m_statute_reference") is not None]
            muh_legal = round(statistics.mean(mv), 3) if mv else None
            muh_statute = round(statistics.mean(sv), 3) if sv else None

        per_label[lbl] = {
            "gnd": gnd,
            "muh_legal": muh_legal, "muh_statute": muh_statute,
            "gpt_sad": (gpt or {}).get("sadelik_ort"),
        }
        # ayrışma havuzu (faithfulness ↔ Muhakim legal, id eşli)
        for i, gr in gnd_rows.items():
            m = muh.get(i)
            if m is not None and gr.get("faithfulness") is not None:
                pooled.append((lbl, i, gr["faithfulness"], m.get("m_legal_accuracy")))

    # --- ayrışma bayrağı (pooled z) ---
    valid = [p for p in pooled if p[3] is not None]
    flags = []
    if len(valid) >= 2:
        zf = zscores([p[2] for p in valid])
        zm = zscores([p[3] for p in valid])
        for (lbl, i, fa, ml), a_zf, a_zm in zip(valid, zf, zm):
            d = a_zf - a_zm
            if abs(d) >= a.flag_z:
                flags.append((abs(d), lbl, i, fa, ml,
                              "Grounded↑ Muhakim↓" if d > 0 else "Grounded↓ Muhakim↑"))
        flags.sort(reverse=True)

    # --- yaz ---
    L = ["# Faz 1 — Birleşik Skorkart\n",
         "> **ANA = Groundedness** (kapı) · **İkincil = Muhakim** (bilgi) · "
         "**Sadelik = app sinyali** (model gate değil) · Ayrışma = Grounded↔Muhakim zıt.  \n"
         "> ⚠️ Groundedness LLM-judge (insan-κ **kalibresiz**, Aşama C) → mutlak değil, "
         "model-vs-model **sıralama**. Muhakim = reward-model logit'i (mutlak % değil).\n",
         "## ANA — Groundedness (FactScore claim-level + ALCE atıf)\n",
         "| Model | Faithfulness ↑ | Hallucination ↓ | wrong_ref ↓ | cit_recall ↑ | n_claims | hakem/runs |",
         "|---|---|---|---|---|---|---|"]
    for lbl in a.labels:
        g = (per_label.get(lbl) or {}).get("gnd")
        if not g:
            L.append(f"| {lbl} | (gnd yok) | — | — | — | — | — |")
            continue
        L.append(f"| {lbl} | {fmt(g.get('faithfulness_micro'))} | "
                 f"{fmt(g.get('hallucination_micro'))} | {fmt(g.get('wrong_ref_rate_micro'))} | "
                 f"{fmt(g.get('cit_recall_macro'))} | {g.get('total_claims', '—')} | "
                 f"{g.get('judge_model', '?')}/{g.get('runs', '?')} |")
    L.append("")

    # Δ groundedness (ilk iki etiket)
    g0 = (per_label.get(a.labels[0]) or {}).get("gnd") if len(a.labels) >= 2 else None
    g1 = (per_label.get(a.labels[1]) or {}).get("gnd") if len(a.labels) >= 2 else None
    if g0 and g1:
        df = (g1.get("faithfulness_micro") or 0) - (g0.get("faithfulness_micro") or 0)
        dh = (g1.get("hallucination_micro") or 0) - (g0.get("hallucination_micro") or 0)
        L += [f"**Δ ({a.labels[1]} − {a.labels[0]}):** faithfulness **{df:+.3f}**, "
              f"hallucination **{dh:+.3f}** _(faithfulness↑ + hallucination↓ = iyi)_\n"]

    # İKİNCİL + BİLGİ
    L += ["## İkincil (bilgi) — Muhakim + Sadelik(app)\n",
          "| Model | Muhakim·legal | Muhakim·statute | Sadelik (GPT 1-10, app) | Göz testi |",
          "|---|---|---|---|---|"]
    for lbl in a.labels:
        s = per_label.get(lbl) or {}
        gz = f"`{ed}/{lbl}_goz_testi.md`"
        L.append(f"| {lbl} | {fmt(s.get('muh_legal'), sign=True)} | "
                 f"{fmt(s.get('muh_statute'), sign=True)} | "
                 f"{s.get('gpt_sad') if s.get('gpt_sad') is not None else '—'} | {gz} |")
    L += ["",
          "- Muhakim = **ikincil** (derinlik/atıf; kısa-sade'ye yanlı → kapı değil).",
          "- Sadelik = **app/vatandaş-modu** sinyali; model gate **değil** ([[eval-accuracy-gate]]).\n"]

    # ayrışma
    L.append(f"## Ayrışma bayrağı (|Δz| ≥ {a.flag_z}) — Muhakim yanlılığı + insan denetimi\n")
    if flags:
        L.append("| Model | id | Faithfulness | Muhakim legal | Yön |")
        L.append("|---|---|---|---|---|")
        for _, lbl, i, fa, ml, yon in flags[:12]:
            L.append(f"| {lbl} | {i} | {fa:.2f} | {fmt(ml, sign=True, nd=2)} | {yon} |")
        L.append(f"\n**{len(flags)} soruda** Grounded↔Muhakim sert ayrışıyor. "
                 "'Grounded↑ Muhakim↓' = doğru ama kısa-sade cevap (Muhakim yanlılığı, K3 kanıtı).")
    else:
        L.append("_(ayrışma yok ya da yetersiz gnd/muhakim eşli veri)_")
    L.append("")

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, "w", encoding="utf-8").write("\n".join(L))
    print("\n".join(L))
    print(f"\n[scorecard] → {a.out}")


if __name__ == "__main__":
    main()
