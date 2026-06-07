#!/usr/bin/env python
"""HF Hub'da Türkçe hukuk veri setlerini tarar + adayların içine bakar (EDA-lite).

Kullanım:
    python scripts/scan_hf_datasets.py            # tarama + örnek satırlar
    python scripts/scan_hf_datasets.py --peek X   # tek dataset'in içine bak

Token gerekmez (public API). Çıktı: aday tablo + lisans + örnek satırlar.
"""
import json
import sys
import urllib.parse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (HakHukuk data scan)"}
QUERIES = ["turkish law", "hukuk", "turkish legal", "yargitay", "danistay",
           "mevzuat", "kanun", "turkish constitution", "avukat"]


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def license_of(tags):
    for t in tags or []:
        if t.startswith("license:"):
            return t.split(":", 1)[1]
    return "?"


def size_of(tags):
    for t in tags or []:
        if t.startswith("size_categories:"):
            return t.split(":", 1)[1]
    return "?"


def scan():
    seen = {}
    for q in QUERIES:
        url = f"https://huggingface.co/api/datasets?search={urllib.parse.quote(q)}&limit=25"
        try:
            for d in get(url):
                did = d["id"]
                if did not in seen:
                    seen[did] = {
                        "id": did,
                        "dl": d.get("downloads", 0),
                        "likes": d.get("likes", 0),
                        "license": license_of(d.get("tags")),
                        "size": size_of(d.get("tags")),
                        "modified": (d.get("lastModified") or "")[:10],
                    }
        except Exception as e:
            print(f"  ! arama hatası ({q}): {e}", file=sys.stderr)

    rows = sorted(seen.values(), key=lambda x: x["dl"], reverse=True)
    print(f"\n{'='*100}\n{len(rows)} aday Türkçe-hukuk veri seti (indirme sayısına göre)\n{'='*100}")
    print(f"{'dataset':52s} {'indirme':>8s} {'beğeni':>6s} {'lisans':>14s} {'boyut':>12s} {'güncel':>11s}")
    print("-" * 100)
    for r in rows[:30]:
        print(f"{r['id']:52s} {r['dl']:>8} {r['likes']:>6} {r['license']:>14s} {r['size']:>12s} {r['modified']:>11s}")
    return rows


def peek(dataset, n=3):
    print(f"\n{'='*100}\nİÇERİK: {dataset}\n{'='*100}")
    try:
        info = get(f"https://datasets-server.huggingface.co/info?dataset={urllib.parse.quote(dataset)}")
        for cfg, v in info["dataset_info"].items():
            feats = list(v["features"].keys())
            splits = {s: sv.get("num_examples") for s, sv in v["splits"].items()}
            total = sum(x for x in splits.values() if x)
            print(f"  config='{cfg}'  alanlar={feats}")
            print(f"  split'ler ({total} toplam örnek): {splits}")
    except Exception as e:
        print(f"  ! info alınamadı: {e}")
    # örnek satırlar
    try:
        splitsmeta = get(f"https://datasets-server.huggingface.co/splits?dataset={urllib.parse.quote(dataset)}")
        first = splitsmeta["splits"][0]
        cfg, split = first["config"], first["split"]
        rows = get(f"https://datasets-server.huggingface.co/rows?dataset={urllib.parse.quote(dataset)}"
                   f"&config={urllib.parse.quote(cfg)}&split={urllib.parse.quote(split)}&offset=0&length={n}")
        print(f"\n  --- '{split}' split'inden {n} örnek ---")
        for x in rows.get("rows", []):
            row = x["row"]
            for k, val in row.items():
                s = str(val).replace("\n", " ")
                print(f"  [{k}] {s[:220]}")
            print("  " + "-" * 50)
    except Exception as e:
        print(f"  ! örnek satır alınamadı: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--peek":
        peek(sys.argv[2])
    else:
        scan()
        for ds in ["newmindai/EuroHPC-Legal", "Renicames/turkish-law-chatbot"]:
            peek(ds)
