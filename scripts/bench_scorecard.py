#!/usr/bin/env python
"""HakHukuk Eval Suite — birleşik scorecard (A1 Groundedness + A3 Abstention + A4 Format).

Model başına 3 eksen tek tabloda. Etiket şeması:
  A1  gnd_bench_core_{model}_summary.json   (groundedness.py, CORE-HARD)
  A3  abst_bench_trap_{model}_summary.json  (score_abstention.py, TRAP)
  A4  fmt_bench_core_{model}_summary.json   (score_format.py, CORE-HARD cevapları)

Kullanım: python scripts/bench_scorecard.py --models base v0 v1
Çıktı: ekran + outputs/BENCHMARK_REPORT.md

⚠️ LLM-judge (insan-κ kalibresiz) → mutlak değil, model-vs-model SIRALAMA. A1 faithfulness RAG'da
TAVAN yapar (ayırmaz); ASIL ayırt edici = A3 rejection_rate (RGB; tavan yok). Bkz
knowledge/summary_eval_benchmark_literature.md + docs/record/research_log.md.
"""
import argparse
import json
import os


def load(p):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def g(d, k):
    return d.get(k) if d else None


def fmt(v):
    return "—" if v is None else (f"{v:.3f}" if isinstance(v, float) else str(v))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--eval-dir", default="outputs/eval")
    ap.add_argument("--out", default="outputs/BENCHMARK_REPORT.md")
    a = ap.parse_args()
    ed = a.eval_dir

    rows = []
    for m in a.models:
        a1 = load(f"{ed}/gnd_bench_core_{m}_summary.json")
        a3 = load(f"{ed}/abst_bench_trap_{m}_summary.json")
        a4 = load(f"{ed}/fmt_bench_core_{m}_summary.json")
        rows.append((m, a1, a3, a4))

    # eksen tabloları
    def table(title, cols):
        out = [f"### {title}", "", "| model | " + " | ".join(c[0] for c in cols) + " |",
               "|" + "---|" * (len(cols) + 1)]
        for m, a1, a3, a4 in rows:
            src = {"A1": a1, "A3": a3, "A4": a4}
            vals = [fmt(g(src[c[1]], c[2])) for c in cols]
            out.append(f"| **{m}** | " + " | ".join(vals) + " |")
        return "\n".join(out)

    a1_cols = [("faithfulness", "A1", "faithfulness_micro"), ("hallucination", "A1", "hallucination_micro"),
               ("cit_precision", "A1", "cit_precision_micro"), ("wrong_ref", "A1", "wrong_ref_rate_micro"),
               ("cit_recall", "A1", "cit_recall_macro")]
    a3_cols = [("Rej*(LLM)↑", "A3", "rejection_rate"), ("Rej(exact)↑", "A3", "rejection_exact"),
               ("fabrication↓", "A3", "fabrication_rate"), ("param_leak", "A3", "parametric_leak"),
               ("valid_traps", "A3", "valid_traps")]
    a4_cols = [("cite_present", "A4", "cite_present_rate"), ("paren_cite", "A4", "paren_cite_rate"),
               ("single_cite", "A4", "single_cite_rate"), ("med_len", "A4", "med_len")]

    md = [
        "# HakHukuk Eval Suite — Benchmark Scorecard",
        "",
        "> LLM-judge (gpt-4o-mini), model-vs-model SIRALAMA (mutlak değil). "
        "A1 RAG'da tavan → ASIL ayırt edici A3 rejection_rate (RGB, tavan yok). "
        "Setler: CORE-HARD (karmaşıklık-seçili, dengeli) + TRAP (topic-near hard-negative).",
        "",
        "## A1 — Groundedness (CORE-HARD, RAG-modu) · kaynağa sadakat",
        table("A1 Groundedness", a1_cols),
        "",
        "## A3 — Abstention / Rejection-Rate (TRAP) · ⭐ asıl ayırt edici eksen",
        "> rejection_rate↑ = tuzak maddede uydurmadan 'kaynak yetersiz' diyebilme (RGB). "
        "Literatür öngörüsü: SFT abstention'ı bozar → v1 base'den DÜŞÜK beklenir.",
        table("A3 Abstention", a3_cols),
        "",
        "## A4 — Atıf-format tutarlılığı (CORE-HARD) · deterministik",
        table("A4 Format", a4_cols),
        "",
        "## Hakem geçerliliği (G1) — `judge_agreement.py`",
        "> Akademik zorunluluk (RAGBench/RAGTruth %93-95 / %91.8 uyum). Tek hakem yeterli değil.",
        "> Koş: ikinci hakem `--judge-model gpt-4o` (alt-küme) → `judge_agreement.py cross` (κ) "
        "+ `export`→elle→`author` (yazar↔hakem κ). κ≥0.6 makul, ≥0.8 güçlü.",
        "",
        "## Limitations / Future (akademik dürüstlük)",
        "- **G3 Completeness ekseni YOK:** gold kaynak verili (retriever yok) → Relevance/Utilization N/A; "
        "Completeness kısmen A1-faithfulness ile örtüşür. Bilinçli kapsam dışı.",
        "- **G4 Span/word-level halüsinasyon (RAGTruth) — future work.** Şu an response-level.",
        "- **Soru kaynağı:** held-out synthetic (sft_v1/test, aynı üretici dağılım) → KÖR modda contamination "
        "riski (RAG modda yok). Bağımsız/uzman-yazımı set sonraki sağlamlaştırma.",
        "- LLM-judge mutlak değil → **model-vs-model SIRALAMA** olarak oku.",
        "",
    ]
    report = "\n".join(md)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(report)
    print(report)
    print(f"\n[scorecard] → {a.out}")


if __name__ == "__main__":
    main()
