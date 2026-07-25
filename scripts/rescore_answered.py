#!/usr/bin/env python
"""Cevaplanan-only A1 rescore (ADR-0011) — çekinmeleri AYIRARAK macro faithfulness.

A1 = "cevaplananlarda groundedness" (çekinme faith=0 alıp macro'yu HAKSIZ çeker). Bu script
bir gnd detail + bench detail çiftini alır, çekinmeleri (cevap ABSTAIN_RE'yi geçen) DETERMİNİSTİK
ayırır, kalan (cevaplanan) satırlarda macro faithfulness + cit_precision hesaplar.

Aynı kural base/v1/v2b'ye UYGULANIR → elmayla-elma (§6 üstünlük kapısı güç şartı).

Kullanım:
  python scripts/rescore_answered.py --gnd outputs/eval/gnd_bench_m1_base.jsonl \
      --bench outputs/eval/bench_m1_base_detail.jsonl --label m1_base
"""
import argparse
import json

# ⚠️ TEK KAYNAK (2026-07-25): red tespiti score_abstention.REJECT_RE'den İTHAL edilir.
#
# Buraya kadar bu dosya kendi KOPYA regex'ini taşıyordu ve docstring "score_abstention ile
# AYNI" diyordu — ama #39'un kalibrasyonu (2026-07-24) yalnız score_abstention.py'ye işlendi,
# kopya eski hâlinde kaldı. İki tanım sessizce ayrıştı. Ölçülen fark (n=480 cevap, 6 küme):
# üç ayrışma, ÜÇÜ DE eski kopyanın YANLIŞ-POZİTİFİ —
#   · `kaynak(?:lar)?da (?:bu|yok)` bir CEVABI red saydı
#     ("Verilen kaynaklarda bu konuyu düzenleyen madde TCK 227'dir")
#   · `bulunmaz` kanunun kendi KOŞUL dilini red saydı ("hüküm bulunmazsa",
#     "başvuruda bulunmazsanız") — #39'un `(?!sa)` bakışı tam bunu eliyor.
# Yön tek taraflı: yanlış-pozitif red → doğru cevaplanmış satır "cevaplanan" kümesinden
# DÜŞÜYOR → coverage OLDUĞUNDAN DÜŞÜK, A1 havuzu daralıyor. Coverage, τ_grounding'in
# hedef metriği olduğu için bu yön zararsız değil.
# Kopya yerine ithal → kalibrasyon bir yerde yapılır, her yerde geçerlidir (TASARIM §3.4).
from score_abstention import REJECT_RE as ABSTAIN_RE


def load(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gnd", required=True, help="groundedness per-row detail (faithfulness taşır)")
    ap.add_argument("--bench", required=True, help="gen_eval detail (cevap taşır — çekinme tespiti)")
    ap.add_argument("--label", required=True)
    a = ap.parse_args()

    gnd = {r["id"]: r for r in load(a.gnd)}
    bench = {r["id"]: r for r in load(a.bench)}
    ids = sorted(set(gnd) & set(bench))

    answered, abstained = [], []
    for i in ids:
        cevap = bench[i].get("cevap", "")
        (abstained if ABSTAIN_RE.search(cevap) else answered).append(i)

    def macro(field, subset):
        vals = [gnd[i].get(field) for i in subset if gnd[i].get(field) is not None]
        return round(sum(vals) / len(vals), 4) if vals else None

    # cit_precision micro (cevaplananda): Σok / Σcit
    cit_ok = sum(gnd[i].get("n_citations_ok", 0) or 0 for i in answered)
    cit_tot = sum(gnd[i].get("n_citations", 0) or 0 for i in answered)

    out = {
        "label": a.label,
        "n_total": len(ids), "n_answered": len(answered), "n_abstain": len(abstained),
        "over_refusal_rate": round(len(abstained) / len(ids), 4) if ids else None,
        "A1_faithfulness_macro_answered": macro("faithfulness", answered),
        "faithfulness_macro_ALL(çekinme dahil)": macro("faithfulness", ids),
        "cit_precision_micro_answered": round(cit_ok / cit_tot, 4) if cit_tot else None,
        "wrong_ref_rate_macro_answered": macro("wrong_ref_rate", answered),
        "note": "A1=cevaplanan (ABSTAIN_RE ile çekinme ayrıldı, ADR-0011). Aynı kural tüm modellere.",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return out


if __name__ == "__main__":
    main()
