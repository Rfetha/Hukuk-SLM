#!/usr/bin/env python3
"""Harness AÇIK ölçüm tablosu (sprint3 Adım 4) — deterministik eksenler.

Harness AÇIK bir koşunun `*_detail.jsonl`'ini okur ve şunları çıkarır:

  1. **Erişim** — altın madde getirildi mi, kaçıncı sırada (`recall@k`, modelden bağımsız)
  2. **Kütle** — coverage × A1. ⚠️ Tek eksenle okuma yasağı (Sprint 2'nin en pahalı dersi):
     A1 cevaplanan-only, çekinerek kazanmayı ödüllendirir. A1 hakem ister; bu betik
     coverage'ı **regexle** verir, A1 varsa `--gnd` ile birleştirilir.
  3. **Kapı** — ADR-0038 katı + `cogunluk`/`cerrahi` ablasyonları, aynı küme üzerinde post-hoc
  4. **Atıf** — doğrulandı / madde yok / kanun yok / ayrıştırılamadı
  5. **K2'nin bedeli** — altın getirildi AMA cevap 900 char kırpmasının ötesinde kalmış olabilir

⚠️ **Kıyas şerhi.** `groundedness --mode data` yer-gerçeği olarak **tek** altın maddeyi
alır. Harness KAPALI'da altın bağlamda garanti; harness AÇIK'ta olmayabilir ve model
soruyu **başka** bir maddeden doğru cevaplasa bile bu ölçü onu sadakatsiz sayar. Bu yüzden
A1 hem tüm kümede hem **altın getirilen alt kümede** raporlanır — ikincisi ON/OFF için
kıyaslanabilir olandır.

Kullanım:
  python scripts/harness_tablo.py --details outputs/eval/s3-harness-acik/h1_<etiket>_detail.jsonl \\
      [--gnd outputs/eval/s3-harness-acik/gnd_h1_<etiket>.jsonl]
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from atif_dogrula import Dogrulayici, DOGRULANDI, MADDE_YOK, KANUN_YOK, AYRISTIRILAMADI  # noqa: E402
from red_kapisi import kapi, POLITIKALAR  # noqa: E402
from score_abstention import exact_reject  # noqa: E402


def _oran(pay, payda):
    return round(pay / payda, 4) if payda else None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--details", required=True)
    p.add_argument("--gnd", default="", help="groundedness çıktısı (A1 için); yoksa A1 boş kalır")
    p.add_argument("--korpus", default="data/corpus/mevzuat_maddeler.jsonl")
    p.add_argument("--out", default="")
    a = p.parse_args()

    kayitlar = [json.loads(l) for l in open(a.details, encoding="utf-8") if l.strip()]
    if not kayitlar or "harness" not in kayitlar[0]:
        raise SystemExit("[tablo] 🚫 bu dosyada harness izi yok — harness AÇIK koşusu mu?")
    n = len(kayitlar)
    k = kayitlar[0]["harness"]["k"]

    # 1) Erişim
    siralar = [r["harness"]["altin_sirasi"] for r in kayitlar]
    getirildi = [s is not None for s in siralar]
    erisim = {f"recall@{j}": _oran(sum(1 for s in siralar if s is not None and s < j), n)
              for j in (1, 3, 5) if j <= k}

    # 2) Kütle (coverage regexle; A1 hakemden)
    cevaplandi = [not exact_reject(r.get("cevap", ""), "data") for r in kayitlar]
    coverage = _oran(sum(cevaplandi), n)

    a1 = a1_getirilen = None
    if a.gnd:
        gnd = {g.get("id"): g for g in
               (json.loads(l) for l in open(a.gnd, encoding="utf-8") if l.strip())}
        puanli = [(i, g) for i, g in gnd.items() if g.get("faithfulness") is not None]
        if puanli:
            a1 = _oran(sum(g["faithfulness"] for _, g in puanli), len(puanli))
            alt = [(i, g) for i, g in puanli if getirildi[i]]
            a1_getirilen = _oran(sum(g["faithfulness"] for _, g in alt), len(alt)) if alt else None

    # 3) Kapı (üç politika, post-hoc aynı küme — ADR-0038)
    d = Dogrulayici(a.korpus)
    hukumler = [d.cevabi_dogrula(r.get("cevap", "")) for r in kayitlar]
    kapilar = {}
    for pol in POLITIKALAR:
        kararlar = [kapi(r.get("cevap", ""), h, pol) for r, h in zip(kayitlar, hukumler)]
        gecen = sum(1 for x in kararlar if x.gecti)
        kapilar[pol] = {
            "gecen": gecen, "reddedilen": n - gecen,
            "atifsiz_gecen": sum(1 for x in kararlar if x.gecti and x.n_atif == 0),
            "kapi_sonrasi_coverage": _oran(
                sum(1 for x, c in zip(kararlar, cevaplandi) if x.gecti and c), n),
        }

    # 4) Atıf dağılımı
    dagilim = {x: 0 for x in (DOGRULANDI, MADDE_YOK, KANUN_YOK, AYRISTIRILAMADI)}
    for hs in hukumler:
        for h in hs:
            dagilim[h.hukum] += 1

    # 5) Erişim ↔ davranış çapraz tablosu — harness'ın asıl sınavı
    capraz = {
        "altin_geldi_cevapladi": sum(1 for g, c in zip(getirildi, cevaplandi) if g and c),
        "altin_geldi_cekindi": sum(1 for g, c in zip(getirildi, cevaplandi) if g and not c),
        "altin_gelmedi_cevapladi": sum(1 for g, c in zip(getirildi, cevaplandi) if not g and c),
        "altin_gelmedi_cekindi": sum(1 for g, c in zip(getirildi, cevaplandi) if not g and not c),
    }

    sonuc = {
        "kaynak": a.details, "n": n, "harness_k": k,
        "erisim": erisim,
        "kutle_ekseni": {"coverage": coverage, "A1_tum": a1,
                         "A1_altin_getirilen_alt_kume": a1_getirilen,
                         "kutle_tum": round(coverage * a1, 4) if a1 else None},
        "kapi": kapilar,
        "atif_dagilimi": dagilim,
        "erisim_davranis_caprazi": capraz,
        "not": ("A1 tek-altın yer-gerçeğine göre; harness AÇIK'ta model BAŞKA bir maddeden "
                "doğru cevaplasa da sadakatsiz sayılır → ON/OFF kıyası için "
                "A1_altin_getirilen_alt_kume kullanılır."),
    }
    print(json.dumps(sonuc, ensure_ascii=False, indent=2))
    if a.out:
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        json.dump(sonuc, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"[tablo] → {a.out}")


if __name__ == "__main__":
    main()
