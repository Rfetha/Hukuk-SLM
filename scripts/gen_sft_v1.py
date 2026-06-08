#!/usr/bin/env python3
"""4d — grounded SFT v1 üretici: 2759 vatandaş maddesi → ~20K (soru, doğru+atıflı cevap).

Tek-örnek `gen_grounded.py`'nin (4a, doğrulanmış: faith 1.0) çoklu-örnek + ölçek sürümü.
Madde başına, MADDENİN GERÇEKTEN DESTEKLEDİĞİ kadar (3–MAX) ayrık vatandaş Q&A üretir —
model uyduramaz (kaynak = gerçek madde). Eski 32K KATILMAZ (v0'ı batıran oydu; ayrıca
kaynaksız → groundedness ile puanlanamaz). v1 = saf grounded.

Akış: usable+ALLOWED_LAWS havuzu → her maddeye 1 gpt-4o-mini çağrısı (çoklu pair, JSON) →
chat-template + kaynak_madde → hash-split → data/processed/sft_v1/{train,validation,test}.jsonl

Kullanım:
  python scripts/gen_sft_v1.py --limit 5        # küçük test
  python scripts/gen_sft_v1.py --max-pairs 8    # tam koşu (arka planda)
"""
import argparse
import hashlib
import json
import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from gen_grounded import (ALLOWED_LAWS, MADDE_PATH, MAX_MADDE_CHARS,
                          PRICE_IN, PRICE_OUT, clean_text, usable)

OUT_DIR = "data/processed/sft_v1"
RAW_POOL = os.path.join(OUT_DIR, "raw_pool.jsonl")

GEN_SYSTEM = (
    "Sen Türk hukuku için yüksek kaliteli eğitim verisi üreten bir uzmansın. "
    "Sana GERÇEK bir kanun maddesi verilir; görevin SADECE o maddeye dayalı, birbirinden "
    "FARKLI (örtüşmeyen) vatandaş soru-cevap çiftleri üretmek. Madde dışına çıkma, "
    "bilgi/kanun uydurma; madde az şey söylüyorsa AZ çift üret."
)

GEN_TEMPLATE = (
    "Aşağıda gerçek bir Türk kanun maddesi var. Bu maddenin GERÇEKTEN cevapladığı, "
    "birbirinden farklı en fazla {k} adet vatandaş soru-cevap çifti üret (madde azsa daha az):\n"
    "- SORU: sıradan bir vatandaşın günlük dilde soracağı doğal soru (jargon kullanma).\n"
    "- CEVAP: SADECE bu maddeye dayanarak; hukuken DOĞRU, sade vatandaş Türkçesiyle, "
    "kısa ama TAM. Cevabın sonunda atıfı aynen şu biçimde yaz: ({kanun}, {madde_no}). "
    "Köşeli parantez/yer-tutucu KULLANMA.\n"
    "Çiftler birbirini TEKRARLAMASIN; her biri maddenin farklı bir yönünü sorsun. "
    "Madde dışına çıkma, uydurma.\n\n"
    "KANUN: {kanun} — {madde_no}\n"
    "MADDE METNİ:\n{text}\n\n"
    'SADECE şu JSON: {{"ornekler": [{{"soru": "...", "cevap": "..."}}, ...]}}'
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default=os.environ.get("GEN_MODEL", "gpt-4o-mini"))
    p.add_argument("--max-pairs", type=int, default=8)
    p.add_argument("--limit", type=int, default=0, help="sadece ilk N madde (test)")
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--split-only", action="store_true",
                   help="üretme; sadece raw_pool'dan dedup+split kur")
    return p.parse_args()


def art_key(r):
    return f"{r.get('kanun_no')}|{r.get('madde_no')}"


def load_done_keys():
    """Resume: raw_pool'da zaten üretilmiş maddelerin anahtarları."""
    keys = set()
    if os.path.exists(RAW_POOL):
        for line in open(RAW_POOL, encoding="utf-8"):
            try:
                keys.add(art_key(json.loads(line)))
            except Exception:
                pass
    return keys


def finalize(seed):
    """raw_pool.jsonl → soru-dedup → hash-split → train/validation/test.jsonl"""
    recs = [json.loads(l) for l in open(RAW_POOL, encoding="utf-8")]
    seen, dedup = set(), []
    for rec in recs:
        q = rec["messages"][0]["content"]
        if q not in seen:
            seen.add(q)
            dedup.append(rec)
    counts = {"train": 0, "validation": 0, "test": 0}
    files = {sp: open(os.path.join(OUT_DIR, f"{sp}.jsonl"), "w", encoding="utf-8")
             for sp in counts}
    for rec in dedup:
        sp = bucket(rec["messages"][0]["content"], seed)
        files[sp].write(json.dumps(rec, ensure_ascii=False) + "\n")
        counts[sp] += 1
    for fh in files.values():
        fh.close()
    print(f"[v1] FINALIZE: {len(recs)} ham → {len(dedup)} dedup | split {counts} "
          f"(toplam {sum(counts.values())})")


def load_pool(limit):
    rows = [json.loads(l) for l in open(MADDE_PATH, encoding="utf-8")]
    pool = [r for r in rows if usable(r)
            and (r.get("kanun_adi") or "").strip().upper() in ALLOWED_LAWS]
    if limit:
        pool = pool[:limit]
    return pool


def gen_one(client, model, r):
    kanun = r.get("kanun_adi", "")
    prompt = GEN_TEMPLATE.format(k=8, kanun=kanun, madde_no=r.get("madde_no", ""),
                                 text=(r.get("text") or "")[:MAX_MADDE_CHARS])
    resp = client.chat.completions.create(
        model=model, temperature=0.7, response_format={"type": "json_object"},
        messages=[{"role": "system", "content": GEN_SYSTEM},
                  {"role": "user", "content": prompt}])
    u = resp.usage
    cost = u.prompt_tokens * PRICE_IN + u.completion_tokens * PRICE_OUT
    data = json.loads(resp.choices[0].message.content)
    out = []
    for ex in (data.get("ornekler") or [])[:8]:
        soru, cevap = clean_text(ex.get("soru", "")), clean_text(ex.get("cevap", ""))
        if soru and cevap and len(cevap.split()) >= 5:
            out.append({
                "messages": [{"role": "user", "content": soru},
                             {"role": "assistant", "content": cevap}],
                "source": f"grounded_{model}",
                "kanun_adi": kanun, "madde_no": r.get("madde_no"),
                "kanun_no": r.get("kanun_no"),
            })
    return out, cost


def bucket(q, seed):
    h = int(hashlib.md5(f"{seed}:{q}".encode("utf-8")).hexdigest(), 16) % 100
    return "test" if h < 5 else ("validation" if h < 10 else "train")


def main():
    a = parse_args()
    os.makedirs(OUT_DIR, exist_ok=True)

    if a.split_only:
        finalize(a.seed)
        return

    from openai import OpenAI
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise SystemExit("[v1] OPENAI_API_KEY yok (.env yükle)")
    # timeout: takılan çağrı worker'ı süresiz kilitlemesin; max_retries: 429'da kontrollü backoff
    client = OpenAI(api_key=key, timeout=60.0, max_retries=4)
    budget = float(os.environ.get("OPENAI_BUDGET_USD", "5"))

    pool = load_pool(a.limit)
    done = load_done_keys()                       # RESUME
    todo = [r for r in pool if art_key(r) not in done]
    print(f"[v1] havuz={len(pool)} | zaten bitmiş={len(done)} | yapılacak={len(todo)} | "
          f"model={a.model} workers={a.workers} bütçe=${budget}")

    lock = threading.Lock()
    raw_fh = open(RAW_POOL, "a", encoding="utf-8")  # APPEND = resume-safe
    state = {"spent": 0.0, "pairs": 0, "done": 0, "stop": False}

    def work(r):
        if state["stop"]:
            return
        try:
            out, cost = gen_one(client, a.model, r)
        except Exception as e:
            with lock:
                print(f"[v1] HATA {r.get('kanun_adi','')[:20]} m.{r.get('madde_no')}: {e}")
            return
        with lock:
            # her madde biter bitmez ANINDA diske yaz + flush (WSL kapansa bile kalır)
            for rec in out:
                raw_fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            raw_fh.flush()
            os.fsync(raw_fh.fileno())
            state["spent"] += cost
            state["pairs"] += len(out)
            state["done"] += 1
            if state["done"] % 50 == 0:
                print(f"[v1] {state['done']}/{len(todo)} madde | {state['pairs']} çift "
                      f"| ${state['spent']:.2f}", flush=True)
            if state["spent"] >= budget:
                state["stop"] = True
                print(f"[v1] ⚠️ bütçe ${budget} doldu, durduruluyor")

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(work, r) for r in todo]
        for _ in as_completed(futs):
            pass
    raw_fh.close()
    print(f"[v1] üretim bitti | {state['done']} yeni madde | {state['pairs']} yeni çift "
          f"| maliyet ${state['spent']:.2f}")
    finalize(a.seed)
    print(f"[v1] → {OUT_DIR}/")


if __name__ == "__main__":
    main()
