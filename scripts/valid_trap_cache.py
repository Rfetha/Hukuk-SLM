#!/usr/bin/env python3
"""CP2-r — cevaba KÖR `valid_trap` önbelleği (ADR-0048 · ADR-0049 m.2).

Ölçüldü (`research_log` #45): `valid_trap` her özne için, hakem o öznenin **cevabını görerek**
yeniden yargılanıyordu. Aynı 80 M3 kaleminde 54/56/**39** — 19 kalemde etiket özneye göre
değişiyor. Bir tuzağın geçerliliği kalemin **değişmez** özelliğidir; öznenin cevabına bağlı olamaz.

Sonuç: çekinme metriklerinin **paydası özneye bağlanmış** ve sapma **yön değiştiriyor**
(M2b aleyhimize ~7p, M3 lehimize ~12p) — ön-kayıtlı bir kapı için gürültünün en kötü türü.

Bu betik geçerliliği **bir kez**, **cevaba kör**, **kalem düzeyinde** hesaplar ve önbelleğe yazar.
Özne skorlaması onu **okur**, yeniden sormaz.

🚨 M3 HAKEME GİTMEZ (ADR-0048 m.2). `--empty-context` altında bağlam
`"(İlgili kaynak bulunamadı.)"` — kaynak metni **yok**, yani "kaynak soruyu cevaplıyor mu"nun
cevabı tanım gereği 80/80 **hayır**. Hakeme sorulduğu için 39-56 çıkmıştı: gereksiz gürültü **ve**
para.

🚨 Bağlamın özneler arası **bit-birebir aynı** olduğu doğrulandı (m2 70/70 · m2b 80/80 · m3 80/80,
sıfır fark) — önbelleğin `id` anahtarlı olmasını meşru kılan olgu budur. Betik bunu **her koşuda
yeniden doğrular**; ayrışma varsa önbellek yazılmaz.

Hakem **gpt-4o** (ADR-0049 m.2): önbellek bir kez hesaplanıp commit edildiği için maliyet argümanı
düşer, ve `gpt-4o-mini` tam bu eksende zayıf. Skorlama hakemi **mini olarak kalır** — `valid_trap`
bir *kürasyon etiketi*, puanlama yargısı değil; aile dışlaması (ADR-0032) tetiklenmiyor.

Kullanım:
  python scripts/valid_trap_cache.py --run-dir outputs/eval/cp09-butceli-1024-512 \
      --out outputs/eval/cp2-r-kor-payda/valid_trap_cache.json
"""
import argparse
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm_client import (make_client, resolve, price, request_kwargs,  # noqa: E402
                        note_provider, seen_providers, loads_tolerant)
from score_abstention import GECERLILIK_SYSTEM as SYSTEM  # noqa: E402  — semantik kilit, TEK kaynak

# Hangi modun geçerliliği nereden okunur. `alan=None` → hakeme GİTMEZ, sabit.
MOD_KAYNAK = {
    "m2":  {"alan": "referans",       "sabit": None},
    "m2b": {"alan": "context_shown",  "sabit": None},
    "m3":  {"alan": None,             "sabit": True},   # ADR-0048 m.2 — bağlam boş
}
CLIP = 900          # eval-ayna klipi (ADR-0011 değişmezi)

# ⚠️ 2026-08-06: kör yargı ARTIK `score_abstention.py`'nin kendisinde (kusur K3). Bu betik
# `{mod}:{id}` anahtarlı tarihsel önbelleği (cp2-r) üretmiş olduğu için kayıt uğruna duruyor;
# YENİ koşularda gerek yok — `score_abstention.py` paydayı kendi önbelleğinden okur/yazar.


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", required=True,
                   help="detay dosyalarının bulunduğu koşu klasörü (m{mod}_{etiket}_detail.jsonl)")
    p.add_argument("--out", required=True)
    p.add_argument("--tags", nargs="+", default=["base_th", "tg_v1_th", "gem_th"],
                   help="bağlam-aynılığı doğrulaması için özne etiketleri")
    p.add_argument("--modes", nargs="+", default=["m2", "m2b", "m3"])
    p.add_argument("--onceki-onbellek", nargs="+", default=[],
                   help="daha önce yazılmış valid_trap_cache.json dosyaları — içlerindeki "
                        "{mod}:{id} kalemleri YENİDEN HAKEME GİTMEZ. Geçerlilik kalemin "
                        "özelliği olduğu için (ADR-0048) bu meşru; ek turlarda 1. turun "
                        "bedeli tekrar ödenmez.")
    p.add_argument("--sadece-teyit", default=None,
                   help="koşu dizini — yalnız `abst_{mod}_{tag}_teyit.jsonl` içinde verdict="
                        "FABRICATE olan id'ler damgalanır. Gerekçe: kabul ölçütü `teyit ∧ kör`, "
                        "yani teyitten düşen kalemin damgası HİÇBİR yerde kullanılmıyor. "
                        "⚠️ Bedeli: havuz geneli geçerlilik oranı ölçülmez (yalnız kabul "
                        "adaylarınınki). O oran gerekiyorsa bu bayrak VERİLMEZ.")
    p.add_argument("--judge-model", default="gpt-4o")
    p.add_argument("--budget-usd", type=float,
                   default=float(os.environ.get("OPENAI_BUDGET_USD", "5") or "5"))
    return p.parse_args()


def load_detail(run_dir, mode, tag):
    p = f"{run_dir}/{mode}_{tag}_detail.jsonl"
    if not os.path.exists(p):
        return None
    return {json.loads(l)["id"]: json.loads(l) for l in open(p, encoding="utf-8") if l.strip()}


def collect_items(run_dir, mode, tags, alan):
    """Kalemleri topla VE bağlamın özneler arası aynı olduğunu doğrula.

    Doğrulama zorunlu: önbellek `id` anahtarlı, yani 'bağlam kalemin özelliğidir' varsayımına
    dayanıyor. Varsayım bozulursa önbellek sessizce yanlış olur — bu hattın hata sınıfı.
    """
    per_tag = {t: load_detail(run_dir, mode, t) for t in tags}
    per_tag = {t: d for t, d in per_tag.items() if d}
    if not per_tag:
        return None, None
    ids = sorted(set.intersection(*[set(d) for d in per_tag.values()]))
    if alan is None:
        return {i: None for i in ids}, []
    items, sapan = {}, []
    for i in ids:
        vals = {(per_tag[t][i].get(alan) or "")[:CLIP] for t in per_tag}
        if len(vals) > 1:
            sapan.append(i)
        items[i] = next(iter(vals))
    return items, sapan


def kaynak_izi(source):
    """Kaynak metnin parmak izi — önbellek yeniden kullanımını doğrulamak için.

    Why: önbellek `{mod}:{id}` anahtarlı ve bu 'bağlam kalemin özelliğidir' varsayımına
    dayanıyor. Varsayım iki koşu ARASINDA bozulursa (havuz değişti, kırpma değişti) yeniden
    kullanım sessizce yanlış etiket taşır. İz eşleşmiyorsa çökeriz.
    """
    return hashlib.sha256((source or "").encode("utf-8")).hexdigest()[:16]


def onbellek_yukle(yollar):
    """Önceki önbellekleri tek sözlükte birleştir. Aynı anahtar çakışırsa ilk dosya kazanır."""
    birlesik = {}
    for y in yollar:
        d = json.load(open(y, encoding="utf-8"))["cache"]
        yeni = {k: v for k, v in d.items() if k not in birlesik}
        birlesik.update(yeni)
        print(f"[kör-payda] önceki önbellek {y}: {len(d)} kalem, {len(yeni)} yeni")
    return birlesik


def judge(client, model, soru, source):
    r = client.chat.completions.create(
        model=model, temperature=0, **request_kwargs(model),
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": f"SORU:\n{soru}\n\nKAYNAK:\n{source}"}])
    note_provider(r)
    d = loads_tolerant(r.choices[0].message.content)
    u, p = r.usage, price(model)
    return d, u.prompt_tokens * p[0] + u.completion_tokens * p[1]


def main():
    a = parse_args()
    client, gateway = make_client()
    a.judge_model = resolve(a.judge_model, gateway)
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)

    cache, meta, spent = {}, {}, 0.0
    onceki = onbellek_yukle(a.onceki_onbellek)
    for mode in a.modes:
        cfg = MOD_KAYNAK[mode]
        items, sapan = collect_items(a.run_dir, mode, a.tags, cfg["alan"])
        if items is None:
            print(f"[kör-payda] {mode}: detay dosyası yok, atlandı"); continue
        if sapan:
            raise SystemExit(
                f"🚨 {mode}: bağlam {len(sapan)} kalemde özneler arası FARKLI (ör. {sapan[:5]}).\n"
                "   Önbellek `id` anahtarlı olamaz — geçerlilik kalem özelliği değil. DURDURULDU.")

        # Soruyu ilk öznenin detayından al (soru da kalem özelliği)
        first = load_detail(a.run_dir, mode, a.tags[0]) or \
            load_detail(a.run_dir, mode, next(t for t in a.tags if load_detail(a.run_dir, mode, t)))

        if a.sadece_teyit:
            tp = f"{a.sadece_teyit}/abst_{mode}_{a.tags[0]}_teyit.jsonl"
            if not os.path.exists(tp):
                raise SystemExit(f"🚨 --sadece-teyit verildi ama {tp} yok. Teyit adımı koştu mu?")
            tut = {r["id"] for r in json.load(open(tp, encoding="utf-8"))
                   if r.get("verdict") == "FABRICATE"}
            n0 = len(items)
            items = {i: v for i, v in items.items() if i in tut}
            print(f"[kör-payda] {mode}: --sadece-teyit → {n0} kalemden {len(items)}'i "
                  f"damgalanacak ({n0 - len(items)} kalem teyitten düştü, damgası kullanılmayacak)")

        if cfg["sabit"] is not None:
            for i in items:
                cache[f"{mode}:{i}"] = {"gecerli": cfg["sabit"], "kaynak": "TANIM",
                                        "reason": "bağlam boş — kaynak metni yok (ADR-0048 m.2)"}
            meta[mode] = {"n": len(items), "gecerli": len(items), "hakem": "YOK (tanım gereği)",
                          "maliyet_usd": 0.0}
            print(f"[kör-payda] {mode}: {len(items)}/{len(items)} GEÇERLİ — hakeme gitmedi (tanım)")
            continue

        n_valid, cost0, devralinan = 0, spent, 0
        for k, i in enumerate(items, 1):
            anahtar, iz = f"{mode}:{i}", kaynak_izi(items[i])
            eski = onceki.get(anahtar)
            if eski is not None:
                if eski.get("kaynak_izi") not in (None, iz):
                    raise SystemExit(
                        f"🚨 {anahtar}: önceki önbellekteki kaynak izi TUTMUYOR "
                        f"({eski['kaynak_izi']} ≠ {iz}). Aynı id farklı bağlam taşıyor — "
                        "önbellek yeniden kullanılamaz. DURDURULDU.")
                cache[anahtar] = eski
                n_valid += 1 if eski["gecerli"] else 0
                devralinan += 1
                continue
            if spent >= a.budget_usd:
                raise SystemExit(f"BÜTÇE doldu (${spent:.3f}) — önbellek YARIM, yazılmadı")
            d, c = judge(client, a.judge_model, first[i]["soru"], items[i])
            spent += c
            g = not d.get("source_answers")
            n_valid += 1 if g else 0
            cache[anahtar] = {"gecerli": g, "kaynak": a.judge_model,
                              "reason": d.get("reason"), "kaynak_izi": iz}
            if k % 20 == 0:
                print(f"  {mode} {k}/{len(items)} geçerli={n_valid} ${spent:.4f}", flush=True)
        meta[mode] = {"n": len(items), "gecerli": n_valid,
                      "gecerli_orani": round(n_valid / len(items), 4),
                      "devralinan": devralinan, "yeni_hakem": len(items) - devralinan,
                      "hakem": a.judge_model, "maliyet_usd": round(spent - cost0, 4)}
        print(f"[kör-payda] {mode}: {n_valid}/{len(items)} GEÇERLİ "
              f"({n_valid/len(items):.3f}) ${spent-cost0:.4f}"
              + (f" · {devralinan} devralındı, {len(items)-devralinan} yeni hakem"
                 if devralinan else ""))

    out = {
        "olcum": "cevaba KÖR valid_trap — kalem düzeyinde, bir kez (ADR-0048 · ADR-0049 m.2)",
        "run_dir": a.run_dir, "judge_model": a.judge_model, "judge_gateway": gateway,
        "judge_providers": seen_providers(), "temperature": 0, "clip": CLIP,
        "baglam_ayniligi_dogrulandi": True,
        "devralinan_onbellekler": a.onceki_onbellek or None,
        "sadece_teyitten_gecenler": a.sadece_teyit or None,
        "mod_ozet": meta, "toplam_maliyet_usd": round(spent, 4),
        "not": "Skorlama hakemi gpt-4o-mini OLARAK KALIR; bu bir kürasyon etiketi. "
               "verdict yeniden hesaplanmaz — cevaba bağlılığı meşrudur.",
        "cache": cache,
    }
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n[kör-payda] {len(cache)} kalem → {a.out}  (toplam ${spent:.4f})")


if __name__ == "__main__":
    main()
