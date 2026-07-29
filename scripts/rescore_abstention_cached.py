#!/usr/bin/env python3
"""CP2-r — çekinme koşularını cevaba KÖR paydayla yeniden puanla (ADR-0048 · ADR-0049 m.2).

**Hakem çağrısı YOK, maliyet $0.** Neden yeterli: `score_abstention.py` her kalem için `verdict`i
(`ABSTAIN`/`FABRICATE`) `valid_trap`ten **bağımsız olarak** kaydediyor — geçersiz sayılan
kalemlerde de dolu (doğrulandı: 11/11). Ve `verdict` yeniden hesaplanmaz: o **cevap hakkındadır**,
cevaba bağlı olması **meşrudur**, kirlenme yok (ADR-0049 m.2).

Yani düzeltme = paydayı önbellekten oku + oranları yeniden böl.

🚨 **Eski sayılar SİLİNMEZ.** Çıktı `abst_*_summary_KOR.json` olarak **yanına** yazılır; hangi
sayının hangi paydayla üretildiği görünür kalır (ADR-0048 m.6).

Kullanım:
  python scripts/rescore_abstention_cached.py \
      --run-dir outputs/eval/cp09-butceli-1024-512 \
      --cache outputs/eval/cp2-r-kor-payda/valid_trap_cache.json \
      --out-dir outputs/eval/cp2-r-kor-payda
"""
import argparse
import glob
import json
import os
import re


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", required=True)
    p.add_argument("--cache", required=True)
    p.add_argument("--out-dir", required=True)
    return p.parse_args()


def oran(pay, payda):
    return round(pay / payda, 3) if payda else None


def main():
    a = parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    cache = json.load(open(a.cache, encoding="utf-8"))["cache"]

    satirlar = []
    for path in sorted(glob.glob(f"{a.run_dir}/abst_*.jsonl")):
        m = re.match(r"abst_(m\d+b?)_(.+)\.jsonl$", os.path.basename(path))
        if not m:
            continue
        mode, tag = m.group(1), m.group(2)
        rows = json.load(open(path, encoding="utf-8"))

        eksik = [r["id"] for r in rows if f"{mode}:{r['id']}" not in cache]
        if eksik:
            print(f"  ⚠️ {mode}/{tag}: {len(eksik)} kalem önbellekte YOK → atlandı ({eksik[:3]})")
            continue

        gecerli = [r for r in rows if cache[f"{mode}:{r['id']}"]["gecerli"]]
        n_v = len(gecerli)
        yeni = {
            "rejection_rate":  oran(sum(1 for r in gecerli if r["verdict"] == "ABSTAIN"), n_v),
            "fabrication_rate": oran(sum(1 for r in gecerli if r["verdict"] == "FABRICATE"), n_v),
            "rejection_exact": oran(sum(1 for r in gecerli if r["reject_exact"]), n_v),
            "parametric_leak": oran(sum(1 for r in gecerli if r["used_parametric"]), n_v),
            "valid_traps": n_v, "invalid_traps": len(rows) - n_v, "n": len(rows),
        }

        eski_p = f"{a.run_dir}/abst_{mode}_{tag}_summary.json"
        eski = json.load(open(eski_p, encoding="utf-8")) if os.path.exists(eski_p) else {}

        out = {
            "label": f"{mode}_{tag}", "mode": mode, "tag": tag,
            "payda": "cevaba KÖR valid_trap, kalem düzeyinde önbellek (ADR-0048)",
            "payda_hakemi": json.load(open(a.cache, encoding="utf-8"))["judge_model"],
            "verdict_hakemi": eski.get("judge_model", "gpt-4o-mini"),
            "verdict_yeniden_hesaplanmadi": True,
            "YENI": yeni,
            "ESKI_ozneye_bagli_payda": {k: eski.get(k) for k in
                                        ("rejection_rate", "fabrication_rate", "rejection_exact",
                                         "parametric_leak", "valid_traps", "invalid_traps", "n")},
            "hakem_maliyeti_usd": 0.0,
        }
        json.dump(out, open(f"{a.out_dir}/abst_{mode}_{tag}_summary_KOR.json", "w",
                            encoding="utf-8"), ensure_ascii=False, indent=2)

        satirlar.append((mode, tag, eski.get("valid_traps"), n_v,
                         eski.get("rejection_rate"), yeni["rejection_rate"]))

    print(f"\n{'mod':5} {'özne':10} {'geçerli ESKİ→YENİ':>18}   {'RED ESKİ→YENİ':>18}   fark")
    print("-" * 70)
    for mode, tag, ve, vy, re_, ry in satirlar:
        d = (ry - re_) if (ry is not None and re_ is not None) else None
        print(f"{mode:5} {tag:10} {str(ve):>7} → {str(vy):<7}   "
              f"{str(re_):>7} → {str(ry):<7}   {('%+.3f' % d) if d is not None else '—'}")
    print(f"\n[kör-payda] {len(satirlar)} koşu yeniden puanlandı · hakem maliyeti $0 → {a.out_dir}")


if __name__ == "__main__":
    main()
