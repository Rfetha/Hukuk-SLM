#!/usr/bin/env python3
"""B2 — v2b teacher-LLM cevap üretimi (V2_PLAN §5.2 Adım 2).

`build_sft_v2b.py pack` çıktısını (packed.jsonl) alır, her satıra HEDEF cevap üretir:
  · grounded dilim → teacher-LLM (gpt-4o-mini): CoT + ##begin_quote## [gold'dan BİREBİR] +
    sonuç + (KANUN, Madde X), UZMAN register. (maliyetli)
  · abstain dilim  → ŞABLON (API yok, bedava): uzman-register çekinme ifadesi, çeşitli.

Çıktı: data/processed/sft_v2b/answers.jsonl (packed satırları + "answer" alanı).
Sonra: python scripts/build_sft_v2b.py assemble --answers data/processed/sft_v2b/answers.jsonl

Dirençli: çıktı varsa tamamlanan id'leri atlar (resume). --limit ile smoke.
Maliyet: yalnız grounded dilim API çağırır; ~15K çağrı (gpt-4o-mini). --limit ile önce dene.

Kullanım:
  export OPENAI_API_KEY=...   (veya .env)
  python scripts/gen_v2b_answers.py --limit 20            # smoke
  python scripts/gen_v2b_answers.py                       # tamamı
"""
import argparse
import json
import os
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

PACKED = "data/processed/sft_v2b/packed.jsonl"
OUT = "data/processed/sft_v2b/answers.jsonl"

TEACHER_SYSTEM = (
    "Sen uzman bir Türk hukuku eğitmenisin. Sana bir SORU, NUMARALI kaynaklar (biri doğru = "
    "GOLD, diğerleri ilgisiz distractor) ve ayrıca GOLD madde metni verilecek.\n"
    "Bir EĞİTİM hedef-cevabı üret, ŞU yapıda ve UZMAN dille (vatandaş-basit DEĞİL):\n"
    "1) Kısa gerekçe: hangi kaynak ilgili, neden; distractor'ları neden eledin (1-2 cümle).\n"
    "2) ##begin_quote## ile GOLD metinden ilgili cümleyi KELİMESİ KELİMESİNE alıntıla "
    "(kısaltabilirsin ama SÖZCÜKLERİ DEĞİŞTİRME) ##end_quote##\n"
    "3) Sonuç cümlesi + atıf: (KANUN ADI, Madde X) — madde no'yu kaynak etiketinden al, UYDURMA.\n"
    "Yalnız GOLD'a dayan. Düz metin döndür.\n"
    "ÖNEMLİ: 'GOLD' iç etikettir; CEVAP METNİNDE 'GOLD' kelimesini ASLA kullanma (hiçbir ekle/"
    "çekimle: GOLD metni/madde/kaynak vb. YASAK). İlgili kaynağa 'ilgili kaynak', 'ilgili madde' "
    "veya '[KAYNAK N]' diye atıf yap."
)

# abstain dilimi — uzman-register şablonlar (API yok). id ile çeşitlendirilir.
ABSTAIN_TEMPLATES = [
    "Verilen kaynaklarda bu hususu düzenleyen bir hüküm bulunmamaktadır; sunulan maddeler "
    "soruyla doğrudan ilgili değildir. Güvenilir bir atıf için ilgili mevzuat hükmünün "
    "sağlanması gerekir.",
    "Sunulan kaynaklar arasında bu konuyu düzenleyen madde yer almamaktadır. İlgili düzenleme "
    "elimdeki metinlerde bulunmadığından madde atfı yapmam doğru olmaz.",
    "Mevcut kaynaklar bu soruyu karşılayan bir hüküm içermemektedir. Kaynakta bulunmayan bir "
    "maddeye dayanarak cevap vermem yanıltıcı olur; ilgili hükmün ayrıca temin edilmesi gerekir.",
    "Bu konuyu düzenleyen bir madde verilen kaynaklarda yer almıyor. Doğru bir atıf "
    "yapabilmem için ilgili mevzuat metninin sağlanması gerekmektedir.",
]


def gen_grounded(client, model, row, max_retries=8):
    """Teacher çağrısı + exponential backoff. 429/geçici hatada geri çekilir (ban yememe).
    Tier 1 TPM 200K → ~6 worker ara sıra 429 alır; backoff self-throttle eder."""
    gold_id = f"{row.get('gold_kanun_adi','')} {row.get('gold_madde_no','')}"
    user = (f"KAYNAKLAR:\n{row['sources_block']}\n\n"
            f"SORU: {row['soru']}\n\n"
            f"GOLD madde ({gold_id}):\n{row['gold_text'][:3000]}")
    last = None
    for attempt in range(max_retries):
        try:
            r = client.chat.completions.create(
                model=model, temperature=0.4,
                messages=[{"role": "system", "content": TEACHER_SYSTEM},
                          {"role": "user", "content": user}],
            )
            return r.choices[0].message.content.strip()
        except Exception as e:
            last = e
            name = type(e).__name__
            # 429/RateLimit/geçici → backoff; kalıcı (ör. auth/bad request) → hemen fırlat
            if "RateLimit" in name or "429" in str(e) or "Timeout" in name or "Connection" in name:
                wait = min(60, (2 ** attempt) + random.uniform(0, 1))  # exp + jitter
                time.sleep(wait)
                continue
            raise
    raise last


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--packed", default=PACKED)
    p.add_argument("--out", default=OUT)
    p.add_argument("--model", default=os.environ.get("GEN_MODEL", "gpt-4o-mini"))
    p.add_argument("--limit", type=int, default=0, help="ilk N satır (smoke); 0=tamamı")
    p.add_argument("--workers", type=int, default=4,
                   help="eşzamanlı API isteği (Tier 1 TPM 200K → 4 güvenli ~160K; 6 tavana binip 429 yer; 1=sıralı)")
    a = p.parse_args()

    rows = [json.loads(l) for l in open(a.packed, encoding="utf-8") if l.strip()]
    if a.limit:
        rows = rows[:a.limit]

    done = set()
    if os.path.exists(a.out):                       # resume
        for l in open(a.out, encoding="utf-8"):
            if l.strip():
                done.add(json.loads(l)["id"])
    todo = [r for r in rows if r["id"] not in done]
    n_grounded = sum(1 for r in todo if r["slice"] == "grounded")
    print(f"[B2] toplam={len(rows)} tamamlanan={len(done)} kalan={len(todo)} "
          f"(API çağrısı={n_grounded} grounded; abstain={len(todo)-n_grounded} şablon)")

    client = None
    if n_grounded:
        from openai import OpenAI
        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            raise SystemExit("OPENAI_API_KEY yok (.env yükle: set -a && . ./.env && set +a)")
        # timeout ZORUNLU: timeout'suz client (default 600s) paralel koşuda asılı sokette
        # tüm worker'ları kilitler (gözlemlendi 2026-06-14). 30s → asılı çağrı düşer, backoff retry.
        # max_retries=0: kendi exp-backoff'umuz var (gen_grounded), SDK'nın retry'ı çift olmasın.
        client = OpenAI(api_key=key, timeout=30.0, max_retries=0)

    # abstain'ler API'siz (bedava, anında) → önce onları yaz; grounded'ı paralel havuza ver.
    write_lock = threading.Lock()
    counter = {"ok": 0, "err": 0}

    def worker(row):
        """Bir satırın cevabını üret (grounded=API+backoff, abstain=şablon). out dict veya None."""
        if row["slice"] == "grounded":
            try:
                ans = gen_grounded(client, a.model, row)
            except Exception as e:
                with write_lock:
                    counter["err"] += 1
                    print(f"  id={row['id']} HATA: {type(e).__name__}: {str(e)[:120]} → atla "
                          f"(resume tekrar dener)", flush=True)
                return None
        else:
            ans = ABSTAIN_TEMPLATES[row["id"] % len(ABSTAIN_TEMPLATES)]
        return dict(row, answer=ans)

    f = open(a.out, "a", encoding="utf-8")
    try:
        if a.workers <= 1:                              # sıralı (eski davranış, smoke/debug)
            for row in todo:
                out = worker(row)
                if out is None:
                    continue
                with write_lock:
                    f.write(json.dumps(out, ensure_ascii=False) + "\n"); f.flush()
                    counter["ok"] += 1
                    if counter["ok"] % 25 == 0 or row["slice"] == "grounded":
                        print(f"  [{counter['ok']}/{len(todo)}] ({row['slice']}) id={row['id']}", flush=True)
        else:                                           # PARALEL (ThreadPool + yazım lock)
            print(f"[B2] {a.workers} worker + backoff (Tier 1 TPM 200K self-throttle)", flush=True)
            with ThreadPoolExecutor(max_workers=a.workers) as ex:
                futs = {ex.submit(worker, row): row for row in todo}
                for fut in as_completed(futs):
                    out = fut.result()
                    if out is None:
                        continue
                    with write_lock:                    # tek yazar → satır karışmaz
                        f.write(json.dumps(out, ensure_ascii=False) + "\n"); f.flush()
                        counter["ok"] += 1
                        done_n = counter["ok"] + counter["err"]
                        if counter["ok"] % 50 == 0:
                            print(f"  [{done_n}/{len(todo)}] yazılan={counter['ok']} hata={counter['err']}",
                                  flush=True)
    finally:
        f.close()

    print(f"[B2] → {a.out}  (yeni yazılan={counter['ok']}, hata/atlanan={counter['err']})")
    if counter["err"]:
        print(f"[B2] ⚠️ {counter['err']} satır atlandı → scripti TEKRAR koş (resume onları dener)")
    print(f"[B2] sıradaki: python scripts/build_sft_v2b.py assemble --answers {a.out}")


if __name__ == "__main__":
    main()
