#!/usr/bin/env python3
"""Eşleştirilmiş alt kümede A1 — tuzak 2.4'ün aleti.

Coverage iki kolda farklıysa ham A1 kıyası elmayla armuttur: az cevaplayan kol, kendi seçtiği
KOLAY dilimde ölçülür. base soruların %57,5'ini, `tgta_v1` %78,75'ini cevaplıyor — yani
"base'in A1'i daha yüksek" cümlesi bu kontrol yapılmadan kurulamaz.

⚠️ İKİ dosya gerekir: `cevap` yalnız `*_detail.jsonl`'de, `faithfulness` yalnız `gnd_*.jsonl`'de.
`id` üzerinden birleştirilir; `gnd`'de karşılığı olmayan bir `detail` kaydı SESSİZCE ATLANMAZ,
KeyError verir (payda kaymasın).

Kullanım:
  python scripts/eslesmis_a1.py \\
    --detail-a outputs/eval/cp09-butceli-1024-512/m1_base_th_detail.jsonl \\
    --gnd-a    outputs/eval/cp09-butceli-1024-512/gnd_m1_base_th.jsonl \\
    --detail-b outputs/eval/cp3-supurme-ham/m1_tg_ta_ham_th_detail.jsonl \\
    --gnd-b    outputs/eval/cp3-supurme-ham/gnd_m1_tg_ta_ham_th.jsonl \\
    --etiket-a base --etiket-b tgta_v1
"""
import argparse
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_abstention import exact_reject  # noqa: E402  — TEK kaynak (tuzak 2.9)


def _yukle(yol):
    kayitlar = {}
    with open(yol, encoding="utf-8") as f:
        for satir in f:
            if satir.strip():
                k = json.loads(satir)
                kayitlar[str(k["id"])] = k
    return kayitlar


def _cevaplayanlar(detail, mode):
    return {i for i, k in detail.items() if not exact_reject(k.get("cevap", ""), mode)}


def eslesmis_a1(detail_a, gnd_a, detail_b, gnd_b, mode):
    """İki koşunun ikisinin de CEVAPLADIĞI kalemlerde A1 makrosu.

    Çekinme tespiti tek kaynaktan (`score_abstention.exact_reject`) gelir; regex kopyası
    çoğaltmak tuzak 2.9'dur. `mode` zorunlu (ADR-0044).
    """
    da, ga = _yukle(detail_a), _yukle(gnd_a)
    db, gb = _yukle(detail_b), _yukle(gnd_b)
    ortak = sorted(set(da) & set(db), key=lambda x: (len(x), x))
    kesisim = [i for i in ortak
               if i in _cevaplayanlar(da, mode) and i in _cevaplayanlar(db, mode)]
    if not kesisim:
        raise ValueError("eşleştirilmiş kesişim BOŞ — kıyas kurulamaz")
    eksik = [i for i in kesisim if i not in ga or i not in gb]
    if eksik:
        raise KeyError(f"gnd kaydı olmayan id'ler: {eksik[:5]} (toplam {len(eksik)})")
    fa = statistics.fmean(ga[i]["faithfulness"] for i in kesisim)
    fb = statistics.fmean(gb[i]["faithfulness"] for i in kesisim)
    return {
        "n_kesisim": len(kesisim), "n_ortak_id": len(ortak),
        "n_cevaplayan_a": len(_cevaplayanlar(da, mode)),
        "n_cevaplayan_b": len(_cevaplayanlar(db, mode)),
        "a1_a": fa, "a1_b": fb, "fark": fa - fb,
        "id_listesi": kesisim,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--detail-a", required=True)
    p.add_argument("--gnd-a", required=True)
    p.add_argument("--detail-b", required=True)
    p.add_argument("--gnd-b", required=True)
    p.add_argument("--etiket-a", required=True)
    p.add_argument("--etiket-b", required=True)
    p.add_argument("--mode", default="data", help="ADR-0044 — 'blind' dışında feragat cümlesi red sayılır")
    p.add_argument("--out", default="")
    a = p.parse_args()
    r = eslesmis_a1(a.detail_a, a.gnd_a, a.detail_b, a.gnd_b, a.mode)
    print(f"eşleştirilmiş n = {r['n_kesisim']}  (ortak id {r['n_ortak_id']} · "
          f"cevaplayan {r['n_cevaplayan_a']} ↔ {r['n_cevaplayan_b']})")
    print(f"  A1 {a.etiket_a:<12} = {r['a1_a']:.4f}")
    print(f"  A1 {a.etiket_b:<12} = {r['a1_b']:.4f}")
    print(f"  fark ({a.etiket_a} − {a.etiket_b}) = {r['fark']:+.4f}")
    if a.out:
        r["etiket_a"], r["etiket_b"] = a.etiket_a, a.etiket_b
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(r, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
