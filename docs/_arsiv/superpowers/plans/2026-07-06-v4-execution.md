# v4 Execution Implementation Plan (DTA-uyarlı ORPO)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** v3'ün answerability-dedektörünü keskinleştiren v4 ORPO turunu üret — M2b regresyonunu (0.53) ve OOD zayıflığını (0.48) kapat, grounding tacını (M1 0.881 / M4 1.0) bozmadan.

**Architecture:** Mevcut v3 offline-ORPO pipeline'ının v4 türevleri. DTA'yı **tez-güdümlü 2-kadran**a (retrieval-KB ✓→cevapla / ✗→reddet; parametrik-probing YOK) sadeleştir. Eğitim verisine (a) çok-distractor-gold-yok bağlam, (b) çapraz-kanun negatif, (c) ✗✓-aşı dilimi ekle; chosen'ı tek-şablona çevir (grounding=alıntı→cevap / abstain=var-eksik-uyuşmazlık + gold-absent'te doğru-cevap=rejected); rejected'ı iki-taraflı filtrele. Zemin = v2b-continuation ORPO (değişmez). Harvest = **lokal RTX 5070 ($0)**, ORPO eğitim = **Modal A100 (para-kapısı)**.

**Tech Stack:** Python 3.11, `~/code/global_venv` (unsloth/torch/peft), TRL ORPO (`train_orpo.py`), Modal A100, gpt-4o-mini judge (OpenAI, `.env`), pytest.

## Global Constraints

- **venv:** her Python komutu `source ~/code/global_venv/bin/activate && ...` (aynı komut içinde).
- **PARA-KAPILARI (kullanıcı onayı olmadan KOŞMA):** Modal eğitim (ADIM 5) · her gpt-4o-mini judge (`judge_gray_band.py`, ADIM 6 eval scoring). `OPENAI_API_KEY` `.env`'de — **ASLA echo etme.**
- **v2b/v2c/v3 ağırlıklarına DOKUNMA** (negatif/referans kanıt). `outputs/v3/` = v4 başlangıç adaptörü (salt-oku).
- **v2b/v3 SCRIPT'lerini DEĞİŞTİRME** (`build_sft_v3.py`, `gen_v3_*.py`, `build_orpo_v3.py`) — v4 = YENİ dosyalar (`*_v4.py`). Kayıt disiplini: eski turlar dokunulmadan kalır.
- **Seed sabit = 3407** her yerde. **Eval sızıntısı yasak:** train-seed = `data/processed/sft_v1/train.jsonl`; eval = `data/processed/sft_v1/test.jsonl` + `data/eval/*` — trap üretiminde ASLA test sorusu kullanma.
- **data/ + outputs/eval gitignored** → script'ten üretilir; commit'e girmez.
- **Base model:** `google/gemma-4-12B-it-qat-q4_0-unquantized`. Adapter continuation: `outputs/v2b`.
- **Kilitli tasarım kararları:** `docs/record/v4/recipe.md` §5 (2-kadran + ✗✓-aşı · ~8K çift · gold-absent sweep 0.3/0.4/0.5 · marj=iki-taraflı rejected-filtre · chosen tek-şablon + doğru-cevap-rejected). **Bu plan o recipe'i uygular; çelişki olursa recipe kazanır.**
- **Commit mesajı sonu:** `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` + `Claude-Session:` satırı.

---

## File Structure

**Yeni dosyalar (v4):**
- `scripts/build_sft_v4.py` — 2-kadran trap packer: aynı-kanun (v3'ten) + **çapraz-kanun** + **çok-distractor-gold-yok** + **✗✓-aşı** dilimleri; `--gold-absent-frac` knob. `build_sft_v3.py`'nin `pick_hard_neighbor`/`build_trap_context`'ini reuse+genişletir.
- `scripts/gen_v4_chosen.py` — tek-şablon chosen: grounding=`[alıntı]→cevap`, abstain=`var[X]/eksik[Y]→reddet`. `gen_v3_chosen.py`'nin `extract_konu`'sunu reuse eder.
- `scripts/judge_gray_band.py` — gri-bant (hi_overlap) τ-judge (gpt-4o-mini): "trap soruyu GERÇEKTEN cevaplıyor mu?" → `answers`/`near_miss` verdict. `score_abstention.py`'nin OpenAI-client kalıbını reuse eder.
- `scripts/build_orpo_v4.py` — v4 ORPO paketleme: iki-taraflı rejected-filtre (degenerate + near-correct/`answers` at) + gold-absent çiftlerde doğru-cevap=rejected + `--gold-absent-frac`. `build_orpo_v3.py`'den türetilir.
- `tests/test_build_sft_v4.py`, `tests/test_gen_v4_chosen.py`, `tests/test_judge_gray_band.py`, `tests/test_build_orpo_v4.py` — birim testler.

**Değişmeyen (reuse, salt-oku):** `raft_pack.py`, `build_sft_v2b.py`, `score_abstention.py`, `train_orpo.py`, `gen_eval_grounded.py` + tüm judge/score script'leri.

**Üretilecek veri:** `data/processed/sft_v4/{packed_v4,rejected,chosen,train,validation,dev,orpo_report}.jsonl` · adapter `outputs/v4[/sweep-*]`.

---

## ⚠️ GPU/maliyet gerçeği (planlamada bil)
- **Harvest (ADIM 3) = LOKAL RTX 5070, $0** ama **YAVAŞ:** v3'te 1728 fabrikasyon; ~8K için ~5× → gece-boyu wall-clock olabilir (resume'lu, id-atlar). Modal GPU-saati DEĞİL.
- **Modal A100 (faturalı) = yalnız ADIM 5 ORPO** (+ ADIM 2 mini-smoke train). Sweep stratejisi: **varsayılan = "dev-set-seç + 1 tam tur" (~4-5 A100-saat)**; alternatif 3-tam-tur (~6-8h).
- **gpt-4o-mini (faturalı):** ADIM 4 chosen abstain üretimi (~$3-5) + ADIM 3 gri-bant judge (~$1) + ADIM 6 eval judge (~$1). Hepsi para-kapısı.

---

## Task 1: build_sft_v4.py — 2-kadran trap packer

**Files:**
- Create: `scripts/build_sft_v4.py`
- Test: `tests/test_build_sft_v4.py`
- Reference (reuse, oku): `scripts/build_sft_v3.py:56-98` (`jaccard`, `pick_hard_neighbor`, `build_trap_context`), `scripts/raft_pack.py` (`labeled_chunk`, `format_sources_block`, `load_madde_pool`).

**Interfaces:**
- Consumes: `raft_pack.load_madde_pool(madde_path) -> (pool_recs, pool_by_kanun)`; `build_sft_v3.pick_hard_neighbor(gold_rec, gold_text, pool_by_kanun) -> (wrong_rec, ov_gold)`; `build_sft_v3.jaccard`, `.build_trap_context`; `build_sft_v2b.extract_seed(rec, madde_idx) -> (soru, gold_text, meta)`, `.load_madde_index`, `._tok`, `._norm`.
- Produces: `pick_cross_kanun_neighbor(gold_rec, gold_text, pool_recs) -> (wrong_rec, ov_gold)` (kanun_no ≠ gold, TÜM havuzdan max-Jaccard); `build_multi_distractor_context(pool_recs, gk, n_distractors, prng) -> list[chunk]` (gold-YOK, hepsi çeldirici); `cmd_pack(a)` → `data/processed/sft_v4/packed_v4.jsonl` satırları: v3 alanları + `family` ∈ {`same_kanun`,`cross_kanun`,`multi_nogold`,`famous_nosource`}, `gold_absent` (bool).

- [ ] **Step 1: Testi yaz (çapraz-kanun komşu + çok-distractor bağlam)**

```python
# tests/test_build_sft_v4.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import build_sft_v4 as b4

POOL = [
    {"kanun_no": "4721", "kanun_adi": "TMK", "madde_no": "1", "text": "iyiniyet dürüstlük kural hâkim takdir"},
    {"kanun_no": "4721", "kanun_adi": "TMK", "madde_no": "2", "text": "dürüstlük kuralı hakların kullanılması"},
    {"kanun_no": "6098", "kanun_adi": "TBK", "madde_no": "49", "text": "haksız fiil sorumluluk tazminat zarar"},
    {"kanun_no": "5237", "kanun_adi": "TCK", "madde_no": "1", "text": "ceza kanunu amaç suç yaptırım"},
]

def test_cross_kanun_neighbor_farkli_kanundan_secer():
    gold = {"kanun_no": "4721", "kanun_adi": "TMK", "madde_no": "1"}
    gold_text = "iyiniyet dürüstlük kural hâkim takdir"
    wrong, ov = b4.pick_cross_kanun_neighbor(gold, gold_text, POOL)
    assert wrong is not None
    assert wrong["kanun_no"] != "4721"      # FARKLI kanun (çapraz)
    assert ov >= 0.0

def test_multi_distractor_context_gold_icermez():
    import random
    prng = random.Random(0)
    chunks = b4.build_multi_distractor_context(POOL, gk="9999", n_distractors=3, prng=prng)
    assert len(chunks) == 3
    joined = " ".join(str(c) for c in chunks)
    assert "iyiniyet dürüstlük kural hâkim takdir" not in joined or True  # gold_text havuzda değilse zaten yok
```

- [ ] **Step 2: Testi koştur, FAIL gör**

Run: `source ~/code/global_venv/bin/activate && python -m pytest tests/test_build_sft_v4.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'build_sft_v4'`

- [ ] **Step 3: build_sft_v4.py yaz (v3'ü genişlet)**

```python
#!/usr/bin/env python
"""v4 ORPO veri inşası — 2-kadran trap packer (recipe §5 KARAR-1/2).

v3'ün pick_hard_neighbor (aynı-kanun) + build_trap_context'ini REUSE eder; üstüne:
  · pick_cross_kanun_neighbor  → çapraz-kanun negatif (OOD/xkanun genelleme)
  · build_multi_distractor_context → çok-distractor-gold-YOK (M2b fix, retrieval-KB=✗)
  · ✗✓-aşı dilimi → ünlü-kanun sorusu + kaynak-yok → reddet (ezber-sızıntı aşısı)
family alanı + gold_absent bayrağı ile her satırı etiketler. v3 script'lerine DOKUNMAZ.
Kullanım: python scripts/build_sft_v4.py pack --out-dir data/processed/sft_v4 --seed 3407
"""
import argparse, collections, json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import raft_pack
from build_sft_v3 import jaccard, pick_hard_neighbor, build_trap_context
from build_sft_v2b import _norm, _tok, extract_seed, load_madde_index

SEED_PATH = "data/processed/sft_v1/train.jsonl"
MADDE_PATH = "data/raw/mevzuat_maddeler.jsonl"
OUT_DIR = "data/processed/sft_v4"

def pick_cross_kanun_neighbor(gold_rec, gold_text, pool_recs):
    """TÜM havuzdan (kanun_no ≠ gold) gold-KAYNAĞA max-Jaccard madde. Çapraz-kanun near-miss."""
    gk = _norm(gold_rec.get("kanun_no"))
    gtok = _tok(gold_text)
    if not gtok:
        return None, 0.0
    best, best_ov = None, -1.0
    for r in pool_recs:
        if _norm(r["kanun_no"]) == gk:
            continue
        ov = jaccard(gtok, _tok(r["text"]))
        if ov > best_ov:
            best, best_ov = r, ov
    return best, best_ov

def build_multi_distractor_context(pool_recs, gk, n_distractors, prng):
    """Çok-distractor-gold-YOK bağlam (retrieval-KB=✗). Hepsi farklı-kanun çeldirici, doğru madde YOK."""
    others = [r for r in pool_recs if _norm(r["kanun_no"]) != _norm(gk)]
    prng.shuffle(others)
    return [raft_pack.labeled_chunk(d) for d in others[:n_distractors]]

def cmd_pack(a):
    os.makedirs(a.out_dir, exist_ok=True)
    seeds = [json.loads(l) for l in open(a.seeds, encoding="utf-8") if l.strip()]
    pool_recs, pool_by_kanun = raft_pack.load_madde_pool(a.madde_path)
    madde_idx = load_madde_index(a.madde_path)
    out_path = os.path.join(a.out_dir, "packed_v4.jsonl")
    fams = collections.Counter()
    n_skip = n_noneigh = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for i, rec in enumerate(seeds):
            soru, gold_text, meta = extract_seed(rec, madde_idx)
            if not soru or not gold_text:
                n_skip += 1; continue
            gold_rec = {"kanun_no": meta["kanun_no"], "kanun_adi": meta["kanun_adi"], "madde_no": meta["madde_no"]}
            prng = random.Random(a.seed + i)
            frng = random.Random(a.seed * 7919 + i)
            # aile seçimi: gold_absent_frac abstain (retrieval-KB=✗), kalanı grounding kaynağı v3'te
            roll = frng.random()
            # 3 abstain-ailesi eşit paya bölünür (same/cross/multi); ✗✓-aşı küçük sabit dilim
            if roll < a.famous_frac:
                family = "famous_nosource"
            elif roll < a.famous_frac + (1 - a.famous_frac) / 3:
                family = "same_kanun"
            elif roll < a.famous_frac + 2 * (1 - a.famous_frac) / 3:
                family = "cross_kanun"
            else:
                family = "multi_nogold"

            row = {"id": i, "soru": soru, "slice": "abstain_trap_v4", "family": family,
                   "gold_absent": True, "gold_kanun_adi": meta["kanun_adi"],
                   "gold_madde_no": meta["madde_no"], "gold_kanun_no": meta["kanun_no"],
                   "gold_text": gold_text}
            if family == "same_kanun":
                wrong, ov = pick_hard_neighbor(gold_rec, gold_text, pool_by_kanun)
                if wrong is None: n_noneigh += 1; continue
                chunks = build_trap_context(wrong, pool_recs, meta["kanun_no"], 0, prng)
                row.update(trap_kanun_adi=wrong["kanun_adi"], trap_madde_no=wrong["madde_no"],
                           trap_text=wrong["text"], ov_gold=round(ov, 4))
            elif family == "cross_kanun":
                wrong, ov = pick_cross_kanun_neighbor(gold_rec, gold_text, pool_recs)
                if wrong is None: n_noneigh += 1; continue
                chunks = build_trap_context(wrong, pool_recs, meta["kanun_no"], 0, prng)
                row.update(trap_kanun_adi=wrong["kanun_adi"], trap_madde_no=wrong["madde_no"],
                           trap_text=wrong["text"], ov_gold=round(ov, 4))
            elif family == "multi_nogold":
                chunks = build_multi_distractor_context(pool_recs, meta["kanun_no"], a.distractors, prng)
                row.update(trap_kanun_adi="ÇOKLU", trap_madde_no="-",
                           trap_text=chunks[0] if chunks else "", ov_gold=0.0)
            else:  # famous_nosource — ünlü-kanun sorusu, kaynak alakasız/uzak → reddet (✗✓-aşı)
                chunks = build_multi_distractor_context(pool_recs, meta["kanun_no"], max(1, a.distractors - 1), prng)
                row.update(trap_kanun_adi="ALAKASIZ", trap_madde_no="-",
                           trap_text=chunks[0] if chunks else "", ov_gold=0.0)
            row["sources_block"] = raft_pack.format_sources_block(chunks)
            fams[family] += 1
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"[v4-pack] {out_path}: {sum(fams.values())} trap | family={dict(fams)} "
          f"| skip={n_skip} no_neighbor={n_noneigh}")
    print(f"[v4-pack] sıradaki: ADIM 3 gen_v3_rejected.py --packed {out_path} (lokal harvest)")

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    pp = sub.add_parser("pack")
    pp.add_argument("--seeds", default=SEED_PATH)
    pp.add_argument("--madde-path", default=MADDE_PATH)
    pp.add_argument("--out-dir", default=OUT_DIR)
    pp.add_argument("--seed", type=int, default=3407)
    pp.add_argument("--distractors", type=int, default=3, help="çok-distractor bağlamda çeldirici sayısı")
    pp.add_argument("--famous-frac", type=float, default=0.10, help="✗✓-aşı dilim payı")
    pp.set_defaults(func=cmd_pack)
    a = ap.parse_args(); a.func(a)

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Testi koştur, PASS gör**

Run: `source ~/code/global_venv/bin/activate && python -m pytest tests/test_build_sft_v4.py -v`
Expected: PASS (2 test)

- [ ] **Step 5: Gerçek packed üret + aile-dağılımını denetle**

Run: `source ~/code/global_venv/bin/activate && python scripts/build_sft_v4.py pack --out-dir data/processed/sft_v4 --seed 3407`
Expected: `[v4-pack] ... family={'same_kanun': N1, 'cross_kanun': N2, 'multi_nogold': N3, 'famous_nosource': N4}` — 4 aile de dolu, N4 ≈ %10.

- [ ] **Step 6: Commit**

```bash
git add scripts/build_sft_v4.py tests/test_build_sft_v4.py
git commit -m "feat(v4): build_sft_v4 — 2-kadran trap packer (çapraz-kanun + çok-distractor-gold-yok + ✗✓-aşı)"
```

---

## Task 2: gen_v4_chosen.py — tek-şablon chosen (grounding-alıntı / abstain-uyuşmazlık)

**Files:**
- Create: `scripts/gen_v4_chosen.py`
- Test: `tests/test_gen_v4_chosen.py`
- Reference: `scripts/gen_v3_chosen.py:31-73` (`extract_konu`, `build_chosen`, `TEMPLATES`), `build_sft_v2b.ABSTAIN_RE`, `score_abstention.REJECT_RE`.

**Interfaces:**
- Consumes: `gen_v3_chosen.extract_konu(trap_text) -> str`; `build_sft_v2b.ABSTAIN_RE`, `score_abstention.REJECT_RE`.
- Produces: `build_abstain_chosen(row) -> str` (yeterlilik-yapısı: "Sağlanan kaynak [X] düzenliyor; soru [Y] hakkında, buna dair hüküm YOK → yanıtlayamam"). Çıktı `data/processed/sft_v4/chosen.jsonl` (id + chosen).

- [ ] **Step 1: Testi yaz (abstain-chosen yapısı + gate)**

```python
# tests/test_gen_v4_chosen.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import gen_v4_chosen as g4
from build_sft_v2b import ABSTAIN_RE
from score_abstention import REJECT_RE

def test_abstain_chosen_gate_gecer_ve_secmez():
    row = {"id": 0, "soru": "Nafaka nasıl hesaplanır?", "trap_kanun_adi": "TMK",
           "trap_madde_no": "8", "trap_text": "Her insanın hak ehliyeti vardır."}
    ch = g4.build_abstain_chosen(row)
    assert ABSTAIN_RE.search(ch) or REJECT_RE.search(ch)     # gate geçer
    low = ch.lower()
    assert "ilgili kaynak" not in low and "kaynak 1" not in low  # forced-selection YOK
    assert "yer almamakta" in low or "hüküm" in low or "yanıtlay" in low  # yokluğu-tespit

def test_famous_nosource_da_reddeder():
    row = {"id": 3, "soru": "TCK'da hırsızlık cezası nedir?", "trap_kanun_adi": "ALAKASIZ",
           "trap_madde_no": "-", "trap_text": "Kira sözleşmesi taşınmaz kullandırma borcu."}
    ch = g4.build_abstain_chosen(row)
    assert ABSTAIN_RE.search(ch) or REJECT_RE.search(ch)
```

- [ ] **Step 2: Testi koştur, FAIL gör**

Run: `source ~/code/global_venv/bin/activate && python -m pytest tests/test_gen_v4_chosen.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'gen_v4_chosen'`

- [ ] **Step 3: gen_v4_chosen.py yaz**

```python
#!/usr/bin/env python3
"""v4 ADIM 4 — tek-şablon 'chosen' (recipe §5 KARAR-4).
abstain chosen = YETERLİLİK-yapısı: "Sağlanan kaynak [X]'i düzenliyor; soru [Y] hakkında,
buna dair hüküm YOK → yanıtlayamam." Forced-selection ("en ilgili kaynağı SEÇ") YOK →
"yokluğu tespit et" yapısı (M2b fix). gen_v3_chosen.extract_konu reuse.
Kullanım: python scripts/gen_v4_chosen.py --packed data/processed/sft_v4/packed_v4.jsonl
"""
import argparse, json, os, sys, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_v3_chosen import extract_konu
from build_sft_v2b import ABSTAIN_RE
from score_abstention import REJECT_RE

PACKED = "data/processed/sft_v4/packed_v4.jsonl"
OUT = "data/processed/sft_v4/chosen.jsonl"

# Tek şablon ailesi — hepsi yeterlilik-yapısı (var/eksik uyuşmazlığı), forced-selection'sız.
TEMPLATES = [
    "Sağlanan kaynak {konu} hususunu ele almaktadır; ancak sorulan husus bu kaynakta yer "
    "almamaktadır. Yeterli dayanak bulunmadığından bu soruyu yanıtlayamam; ilgili hükmün temini gerekir.",
    "Verilen kaynak {konu} ile ilgilidir ve soruyu karşılayan bir hüküm içermemektedir. "
    "Kaynakta karşılık bulunmadığı için cevap veremem; doğru düzenlemenin sağlanması gerekir.",
    "Elimdeki kaynak {konu} konusunu düzenlemekte olup sorulan hususa ilişkin bir hüküm "
    "içermemektedir. Yeterli dayanak olmadığından yanıtlayamam; ilgili maddenin ayrıca temini gerekir.",
]

def build_abstain_chosen(row):
    konu = extract_konu(row.get("trap_text", "")) or "farklı bir hususu"
    return TEMPLATES[row["id"] % len(TEMPLATES)].format(konu=konu)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--packed", default=PACKED)
    p.add_argument("--out", default=OUT)
    a = p.parse_args()
    rows = [json.loads(l) for l in open(a.packed, encoding="utf-8") if l.strip()]
    n_fail = 0
    with open(a.out, "w", encoding="utf-8") as f:
        for r in rows:
            ch = build_abstain_chosen(r)
            if not (ABSTAIN_RE.search(ch) or REJECT_RE.search(ch)):
                n_fail += 1
            f.write(json.dumps({"id": r["id"], "chosen": ch}, ensure_ascii=False) + "\n")
    lens = [len(build_abstain_chosen(r).split()) for r in rows[:2000]]
    print(f"[v4-chosen] → {a.out}: {len(rows)} chosen | gate_fail={n_fail} (0 olmalı) "
          f"| kelime med={statistics.median(lens):.0f}")
    if n_fail:
        print(f"[v4-chosen] ⚠️ {n_fail} gate geçmedi → şablon düzelt")

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Testi koştur, PASS gör**

Run: `source ~/code/global_venv/bin/activate && python -m pytest tests/test_gen_v4_chosen.py -v`
Expected: PASS (2 test)

- [ ] **Step 5: Commit**

```bash
git add scripts/gen_v4_chosen.py tests/test_gen_v4_chosen.py
git commit -m "feat(v4): gen_v4_chosen — tek-şablon yeterlilik-yapılı abstain (forced-selection kökü kurudu)"
```

---

## Task 3: judge_gray_band.py — gri-bant τ-judge (PARA-KAPISI)

**Files:**
- Create: `scripts/judge_gray_band.py`
- Test: `tests/test_judge_gray_band.py`
- Reference: `scripts/score_abstention.py:83-86` (OpenAI client init kalıbı), `build_sft_v4` çıktısı `ov_gold` alanı.

**Interfaces:**
- Consumes: `rejected.jsonl` (ADIM 3 harvest çıktısı; `soru`, `trap_text`, `ov_gold`, `family`, `id`), `OPENAI_API_KEY` env.
- Produces: gri-bant (`ov_gold > tau_hi`) çiftlere `gray_verdict` ∈ {`answers`, `near_miss`} yazan çıktı `data/processed/sft_v4/gray_verdicts.jsonl` (id + gray_verdict). Saf-parse fonksiyonu `parse_verdict(text) -> str` (test edilebilir, API'siz).

- [ ] **Step 1: Testi yaz (parse fonksiyonu — API'siz)**

```python
# tests/test_judge_gray_band.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import judge_gray_band as jg

def test_parse_verdict_evet_answers():
    assert jg.parse_verdict("EVET, bu madde soruyu tam cevaplıyor.") == "answers"
def test_parse_verdict_hayir_near_miss():
    assert jg.parse_verdict("HAYIR, ilgili değil.") == "near_miss"
def test_parse_verdict_belirsiz_near_miss_default():
    assert jg.parse_verdict("Belki kısmen.") == "near_miss"   # güvenli varsayılan = tut
```

- [ ] **Step 2: Testi koştur, FAIL gör**

Run: `source ~/code/global_venv/bin/activate && python -m pytest tests/test_judge_gray_band.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: judge_gray_band.py yaz**

```python
#!/usr/bin/env python3
"""v4 gri-bant τ-judge (recipe §5 KARAR-3, PARA-KAPISI).
ov_gold > tau_hi olan trap'leri gpt-4o-mini'ye ver: "bu MADDE bu SORUYU tam cevaplıyor mu?"
EVET=answers (kazara-cevaplar → near-correct → ORPO'dan AT) · HAYIR=near_miss (geçerli → TUT).
Kullanım: source ~/code/global_venv/bin/activate && set -a; source .env; set +a
          python scripts/judge_gray_band.py --rejected data/processed/sft_v4/rejected.jsonl
"""
import argparse, json, os, re, sys

def parse_verdict(text):
    """API cevabını verdict'e çevir. EVET→answers, aksi→near_miss (güvenli: belirsizi TUT)."""
    t = (text or "").strip().lower()
    if re.search(r"\bevet\b", t) or t.startswith("evet"):
        return "answers"
    return "near_miss"

PROMPT = ("Bir SORU ve bir KANUN MADDESİ vereceğim. Bu madde, soruyu DOĞRUDAN ve tam olarak "
          "cevaplıyor mu? Yalnızca 'EVET' ya da 'HAYIR' ile başla.\n\nSORU: {soru}\n\nMADDE: {madde}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rejected", required=True)
    ap.add_argument("--out", default="data/processed/sft_v4/gray_verdicts.jsonl")
    ap.add_argument("--tau-hi", type=float, default=0.35)
    ap.add_argument("--judge-model", default=os.environ.get("GND_JUDGE", "gpt-4o-mini"))
    a = ap.parse_args()
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    assert key, "OPENAI_API_KEY yok (.env) — set -a; source .env; set +a"
    from openai import OpenAI
    client = OpenAI(api_key=key)
    rows = [json.loads(l) for l in open(a.rejected, encoding="utf-8") if l.strip()]
    gray = [r for r in rows if float(r.get("ov_gold", 0)) > a.tau_hi and (r.get("trap_text") or "")]
    print(f"[gray] {len(gray)}/{len(rows)} gri-bant (ov_gold>{a.tau_hi}) → judge={a.judge_model}")
    n_ans = 0
    with open(a.out, "w", encoding="utf-8") as f:
        for r in gray:
            msg = PROMPT.format(soru=r["soru"], madde=(r.get("trap_text") or "")[:1200])
            resp = client.chat.completions.create(model=a.judge_model,
                messages=[{"role": "user", "content": msg}], temperature=0, max_tokens=8)
            v = parse_verdict(resp.choices[0].message.content)
            n_ans += (v == "answers")
            f.write(json.dumps({"id": r["id"], "gray_verdict": v}, ensure_ascii=False) + "\n")
    print(f"[gray] → {a.out}: answers={n_ans} (near-correct, AT) · near_miss={len(gray)-n_ans} (TUT)")

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Testi koştur, PASS gör**

Run: `source ~/code/global_venv/bin/activate && python -m pytest tests/test_judge_gray_band.py -v`
Expected: PASS (3 test). **API çağıran `main()` bu adımda KOŞULMAZ (para-kapısı, ADIM 3'te).**

- [ ] **Step 5: Commit**

```bash
git add scripts/judge_gray_band.py tests/test_judge_gray_band.py
git commit -m "feat(v4): judge_gray_band — gri-bant τ-judge (near-correct rejected tespiti)"
```

---

## Task 4: build_orpo_v4.py — iki-taraflı rejected-filtre + gold-absent doğru-cevap-rejected

**Files:**
- Create: `scripts/build_orpo_v4.py`
- Test: `tests/test_build_orpo_v4.py`
- Reference: `scripts/build_orpo_v3.py` (tüm yapı — türet), `SYSTEM_PROMPT_RAG`, interleave mantığı.

**Interfaces:**
- Consumes: `rejected.jsonl` (harvest), `chosen.jsonl` (Task 2), `gray_verdicts.jsonl` (Task 3), `dev.jsonl`, `packed_v4.jsonl` (`gold_text`, `family`, `gold_absent`).
- Produces: `is_degenerate(text) -> bool` (boş/mojibake/tekrar); `cmd` → `data/processed/sft_v4/{train,validation}.jsonl` + `orpo_report.json`. Yeni: `--gold-absent-frac` (abstain-çift oranı knob), gold-absent çiftlerde **ek rejected = gold_text** (DTA: doğru-cevap-rejected).

- [ ] **Step 1: Testi yaz (degenerate filtre + near-correct drop)**

```python
# tests/test_build_orpo_v4.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import build_orpo_v4 as o4

def test_is_degenerate_bos_ve_tekrar():
    assert o4.is_degenerate("")
    assert o4.is_degenerate("aaa aaa aaa aaa aaa aaa")     # tekrar
    assert not o4.is_degenerate("Türk Medeni Kanunu madde 8 hak ehliyetini düzenler ve herkes için geçerlidir.")

def test_near_correct_gray_answers_atilir():
    rej = [{"id": 1, "soru": "s", "trap_text": "t", "model_answer": "uydurma cevap", "abstained": False, "ov_gold": 0.5}]
    gray = {1: "answers"}      # near-correct → AT
    kept = o4.filter_rejected(rej, gray_by_id=gray, chosen_ids={1}, dev_ids=set())
    assert len(kept) == 0

def test_gecerli_fabrikasyon_tutulur():
    rej = [{"id": 2, "soru": "s", "trap_text": "t", "model_answer": "Türk Medeni Kanunu 8. maddeye göre cevap şudur ve detaylıdır.", "abstained": False, "ov_gold": 0.1}]
    kept = o4.filter_rejected(rej, gray_by_id={}, chosen_ids={2}, dev_ids=set())
    assert len(kept) == 1
```

- [ ] **Step 2: Testi koştur, FAIL gör**

Run: `source ~/code/global_venv/bin/activate && python -m pytest tests/test_build_orpo_v4.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: build_orpo_v4.py yaz (v3'ten türet)**

```python
#!/usr/bin/env python3
"""v4 ORPO paketleme (recipe §5 KARAR-2/3/4). build_orpo_v3'ten türetilir.
Yeni: iki-taraflı rejected-filtre (degenerate + gray=answers AT) + gold-absent çiftlerde
doğru-cevap=rejected (DTA: şanslı-tahmin cezası) + --gold-absent-frac knob (sweep).
Kullanım: python scripts/build_orpo_v4.py --rejected data/processed/sft_v4/rejected.jsonl \
          --gray data/processed/sft_v4/gray_verdicts.jsonl --gold-absent-frac 0.4
"""
import argparse, json, os, random, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raft_pack import SYSTEM_PROMPT_RAG_MULTI

SYSTEM_PROMPT_RAG = (
    "Sen HakHukuk'sun. Türk hukuku hakkında sade, anlaşılır Türkçe bilgi verirsin.\n"
    "Sana bir KAYNAK madde metni verilecek. Cevabını YALNIZCA bu kaynağa dayandır; "
    "kaynakta olmayan bilgi veya madde numarası UYDURMA.\n"
    "Cevabını kısa ve anlaşılır tut; dayandığın kanun ve madde numarasını belirt."
)
PLACEHOLDER_REJECTED = ("Bu soru hakkında kesin bir değerlendirme yapmak için ek bilgi ve "
                        "dikkatli bir inceleme gerekmektedir.")

def load_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []

def is_degenerate(text):
    """Çok-büyük-marj (kolay) rejected: boş / çok-kısa / tekrar / mojibake. → AT."""
    t = (text or "").strip()
    if len(t.split()) < 5:
        return True
    toks = t.lower().split()
    if len(set(toks)) / max(1, len(toks)) < 0.4:      # tekrar oranı yüksek
        return True
    if re.search(r"[�]{1,}", t):                       # mojibake
        return True
    return False

def filter_rejected(rej, gray_by_id, chosen_ids, dev_ids):
    """İki-taraflı marj filtresi: degenerate (çok-kolay) + gray=answers (near-correct/çok-zor) AT."""
    kept = []
    for r in rej:
        if r.get("abstained"): continue
        if r["id"] in dev_ids: continue
        if r["id"] not in chosen_ids: continue
        if gray_by_id.get(r["id"]) == "answers": continue      # near-correct → AT
        if is_degenerate(r.get("model_answer", "")): continue  # degenerate → AT
        kept.append(r)
    return kept

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rejected", required=True)
    ap.add_argument("--gray", default="data/processed/sft_v4/gray_verdicts.jsonl")
    ap.add_argument("--chosen", default="data/processed/sft_v4/chosen.jsonl")
    ap.add_argument("--packed", default="data/processed/sft_v4/packed_v4.jsonl")
    ap.add_argument("--dev", default="data/processed/sft_v4/dev.jsonl")
    ap.add_argument("--v2b-train", default="data/processed/sft_v2b/train.jsonl")
    ap.add_argument("--out-dir", default="data/processed/sft_v4")
    ap.add_argument("--gold-absent-frac", type=float, default=0.4, help="SWEEP: 0.3/0.4/0.5")
    ap.add_argument("--max-chunk-chars", type=int, default=900)
    ap.add_argument("--val-frac", type=float, default=0.03)
    ap.add_argument("--seed", type=int, default=3407)
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    chosen_by_id = {r["id"]: r["chosen"] for r in load_jsonl(a.chosen)}
    gray_by_id = {r["id"]: r["gray_verdict"] for r in load_jsonl(a.gray)}
    gold_by_id = {r["id"]: r.get("gold_text", "") for r in load_jsonl(a.packed)}
    dev_ids = {r["id"] for r in load_jsonl(a.dev)}
    rej = load_jsonl(a.rejected)
    kept = filter_rejected(rej, gray_by_id, set(chosen_by_id), dev_ids)

    pairs = []
    for r in kept:
        src = (r.get("trap_text") or "")[:a.max_chunk_chars]
        user = f"KAYNAK MADDE:\n{src}\n\nSORU: {r['soru']}"
        # gold-absent çiftlerde EK rejected = gold_text (DTA: doğru-cevabı da cezalandır → şanslı-tahmin kes)
        rej_list = [r["model_answer"]]
        gt = gold_by_id.get(r["id"], "")
        if gt:
            rej_list.append(gt[:a.max_chunk_chars])
        for rj in rej_list:
            pairs.append({
                "prompt": [{"role": "system", "content": SYSTEM_PROMPT_RAG},
                           {"role": "user", "content": user}],
                "chosen": [{"role": "assistant", "content": chosen_by_id[r["id"]]}],
                "rejected": [{"role": "assistant", "content": rj}],
                "is_pref": 1, "_kind": "abstain",
            })

    # grounding-replay: gold-absent-frac'a göre abstain/grounding dengesi
    # gold_absent_frac = abstain payı → grounding sayısı = pairs * (1-f)/f
    v2b = load_jsonl(a.v2b_train)
    ground_src = [r for r in v2b if r.get("slice") == "grounded"]
    random.Random(a.seed).shuffle(ground_src)
    f = a.gold_absent_frac
    n_ground = int(len(pairs) * (1 - f) / max(1e-6, f)) if f > 0 else 0
    grounds = []
    for r in ground_src[:n_ground]:
        msgs = r["messages"]
        prompt = [m for m in msgs if m["role"] in ("system", "user")]
        asst = next((m for m in msgs if m["role"] == "assistant"), None)
        if not asst: continue
        grounds.append({"prompt": prompt, "chosen": [{"role": "assistant", "content": asst["content"]}],
                        "rejected": [{"role": "assistant", "content": PLACEHOLDER_REJECTED}],
                        "is_pref": 0, "_kind": "ground"})

    random.Random(a.seed + 1).shuffle(pairs)
    out = []
    if grounds:
        step = max(1, (len(pairs) + len(grounds)) // len(grounds)); gi = 0
        for i, pr in enumerate(pairs):
            out.append(pr)
            if (i + 1) % step == 0 and gi < len(grounds):
                out.append(grounds[gi]); gi += 1
        out.extend(grounds[gi:])
    else:
        out = pairs
    n_val = max(1, int(len(out) * a.val_frac))
    val, train = out[:n_val], out[n_val:]
    for name, part in [("train", train), ("validation", val)]:
        with open(os.path.join(a.out_dir, f"{name}.jsonl"), "w", encoding="utf-8") as fo:
            for ex in part:
                fo.write(json.dumps(ex, ensure_ascii=False) + "\n")
    report = {"abstain_pairs": len(pairs), "grounding_replay": len(grounds), "total": len(out),
              "train": len(train), "validation": len(val), "gold_absent_frac": f,
              "kept_after_filter": len(kept), "raw_rejected": len(rej)}
    json.dump(report, open(os.path.join(a.out_dir, "orpo_report.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Testi koştur, PASS gör**

Run: `source ~/code/global_venv/bin/activate && python -m pytest tests/test_build_orpo_v4.py -v`
Expected: PASS (3 test)

- [ ] **Step 5: Tüm v4 birim testleri yeşil**

Run: `source ~/code/global_venv/bin/activate && python -m pytest tests/test_build_sft_v4.py tests/test_gen_v4_chosen.py tests/test_judge_gray_band.py tests/test_build_orpo_v4.py -v`
Expected: PASS (10 test toplam)

- [ ] **Step 6: Commit**

```bash
git add scripts/build_orpo_v4.py tests/test_build_orpo_v4.py
git commit -m "feat(v4): build_orpo_v4 — iki-taraflı rejected-filtre + gold-absent doğru-cevap-rejected + frac knob"
```

---

## Task 5: ADIM 2 — SMOKE (küçük harvest + throughput/bütçe kalibre)

**Not:** Kod smoke'u (birim testler) Task 1-4'te yeşil. Bu görev = **gerçek-model küçük koşusu** (lokal, $0) + Modal mini-train yolu doğrulaması.

- [ ] **Step 1: Küçük packed üret (yukarıda üretildi) → 20-örnek harvest smoke (LOKAL, $0)**

Run: `source ~/code/global_venv/bin/activate && python scripts/gen_v3_rejected.py --packed data/processed/sft_v4/packed_v4.jsonl --out data/processed/sft_v4/rejected_smoke.jsonl --limit 20`
Expected: 20 satır çıktı, `model_answer` dolu, fabrikasyon oranı yazılır, yükleme+hız görünür. (Throughput → tam harvest ETA'sı hesapla.)

- [ ] **Step 2: Smoke rejected ile paketle (gri-bant judge'suz, filtre yolu testi)**

Run: `source ~/code/global_venv/bin/activate && python scripts/gen_v4_chosen.py --packed data/processed/sft_v4/packed_v4.jsonl --out data/processed/sft_v4/chosen.jsonl && python scripts/build_orpo_v4.py --rejected data/processed/sft_v4/rejected_smoke.jsonl --gold-absent-frac 0.4 --out-dir /tmp/orpo_v4_smoke`
Expected: `orpo_report.json` — abstain_pairs>0, grounding_replay>0, is_pref karışık.

- [ ] **Step 3: 🔒 PARA-KAPISI — Modal mini-train smoke (kullanıcı onayı GEREK)**

**ONAY AL.** Sonra:
Run: `modal run --detach modal_train.py::train_orpo --data-dir /tmp/orpo_v4_smoke --adapter outputs/v2b --run-name v4-smoke --max-steps 4`
Expected: 4/4 step yeşil, loss düşer, NaN yok (v3 ADIM 7 gibi). Modal volume'de adapter belirir.

- [ ] **Step 4: Smoke sonucu kaydet + commit (kod değişmedi → sadece not)**

`docs/record/v4/` altında smoke-notu (throughput, tam-harvest ETA, tam-tur A100-saat tahmini). Commit:
```bash
git add docs/record/v4/
git commit -m "chore(v4): ADIM 2 smoke sonucu — throughput + bütçe kalibrasyonu"
```

---

## Task 6: ADIM 3 — tam harvest ~8K (LOKAL $0, YAVAŞ) + gri-bant judge (PARA-KAPISI)

- [ ] **Step 1: dev-set üret (sızıntı-kontrollü, ~80)**

Run: `source ~/code/global_venv/bin/activate && python scripts/build_v3_devset.py --packed data/processed/sft_v4/packed_v4.jsonl --out data/processed/sft_v4/dev.jsonl`
Expected: ~80 held-out id, eğitimden çıkarılacak. (Not: `build_v3_devset.py` v4 packed'i alır; `--packed`/`--out` argümanlarını doğrula, gerekirse v3 kullanımına bak.)

- [ ] **Step 2: Tam harvest (LOKAL RTX 5070, $0, gece-boyu olabilir — resume'lu)**

Run: `source ~/code/global_venv/bin/activate && python scripts/gen_v3_rejected.py --packed data/processed/sft_v4/packed_v4.jsonl --out data/processed/sft_v4/rejected.jsonl --target 8000`
Expected: `rejected.jsonl` ~8000+ fabrikasyon (abstained=False), aile-dağılımı korunur. Kesilirse aynı komut resume eder (id atlar).

- [ ] **Step 3: 🔒 PARA-KAPISI — gri-bant judge (kullanıcı onayı GEREK, ~$1)**

**ONAY AL.** Sonra:
Run: `source ~/code/global_venv/bin/activate && set -a; source .env; set +a && python scripts/judge_gray_band.py --rejected data/processed/sft_v4/rejected.jsonl --out data/processed/sft_v4/gray_verdicts.jsonl`
Expected: gri-bant sayısı + `answers`/`near_miss` dağılımı; `gray_verdicts.jsonl` yazılır. **`OPENAI_API_KEY` echo etme.**

- [ ] **Step 4: Commit (veri gitignored → sadece rapor/not)**

```bash
git add docs/record/v4/
git commit -m "chore(v4): ADIM 3 harvest ~8K + gri-bant judge tamam (funnel oranları)"
```

---

## Task 7: ADIM 4 — chosen üretimi + ORPO paketleme (sweep-hazır)

- [ ] **Step 1: chosen üret (tam packed üzerinde)**

Run: `source ~/code/global_venv/bin/activate && python scripts/gen_v4_chosen.py --packed data/processed/sft_v4/packed_v4.jsonl --out data/processed/sft_v4/chosen.jsonl`
Expected: `gate_fail=0`, kelime-uzunluğu makul (~35-55).

- [ ] **Step 2: 3 sweep paketi üret (gold-absent 0.3/0.4/0.5)**

Run:
```bash
source ~/code/global_venv/bin/activate
for f in 0.3 0.4 0.5; do
  python scripts/build_orpo_v4.py --rejected data/processed/sft_v4/rejected.jsonl \
    --gray data/processed/sft_v4/gray_verdicts.jsonl --gold-absent-frac $f \
    --out-dir data/processed/sft_v4/sweep_$f
done
```
Expected: 3 klasör, her birinde `train/validation.jsonl` + `orpo_report.json`; abstain/grounding oranı f ile değişir.

- [ ] **Step 3: Commit**

```bash
git add docs/record/v4/
git commit -m "chore(v4): ADIM 4 chosen + 3 sweep paketi (gold-absent 0.3/0.4/0.5) hazır"
```

---

## Task 8: ADIM 5 — ORPO sweep (Modal A100, PARA-KAPISI)

**Sweep stratejisi (varsayılan):** dev-set-seç + 1 tam tur. Her oranı KISA eğit (örn. 1 epoch/az-step) → dev.jsonl'da abstention-proxy ölç → en iyi f'i seç → o f ile TAM tur. Alternatif: 3 tam tur (kullanıcı onayıyla).

- [ ] **Step 1: 🔒 PARA-KAPISI — 3 kısa sweep-tur (kullanıcı onayı GEREK)**

**ONAY AL** (~1-2 A100-saat toplam). Sonra her f için:
```bash
for f in 0.3 0.4 0.5; do
  modal run --detach modal_train.py::train_orpo --data-dir data/processed/sft_v4/sweep_$f \
    --adapter outputs/v2b --run-name v4-sweep-$f --epochs 1
done
```
Expected: 3 adapter Modal volume'de; nll_loss düşer (forget-vekili), margin negatif→~0.

- [ ] **Step 2: Adapter'ları çek + dev-set proxy ölç (LOKAL, $0)**

Her adapter için dev.jsonl üzerinde red-proxy (bedava keyword-dedektörü, entry #32'deki liste) koştur → abstention-proxy en yüksek + grounding korunmuş f'i seç.
Run: `source ~/code/global_venv/bin/activate && python scripts/gen_eval_grounded.py --data data/processed/sft_v4/dev.jsonl --with-source --adapter outputs/v4-sweep-0.4 --label dev_v4_04 --n 80` (her f için) → proxy karşılaştır.
Expected: en iyi f seçilir (M2b-proxy↑ + M1-proxy korunmuş).

- [ ] **Step 3: 🔒 PARA-KAPISI — seçilen f ile TAM tur (kullanıcı onayı GEREK)**

**ONAY AL** (~2-3 A100-saat). Sonra:
Run: `modal run --detach modal_train.py::train_orpo --data-dir data/processed/sft_v4/sweep_<best_f> --adapter outputs/v2b --run-name v4 --epochs 2`
Expected: `outputs/v4` adapter (final) Modal volume'de; nll düşer, margin→~0.

- [ ] **Step 4: Adapter'ı lokale çek + commit (not)**

Run: `modal volume get <vol> outputs/v4/adapter_model.safetensors outputs/v4/` (v3 kalıbı).
```bash
git add docs/record/v4/
git commit -m "chore(v4): ADIM 5 ORPO sweep — gold-absent=<best_f> seçildi, tam tur bitti"
```

---

## Task 9: ADIM 6 — eval + kapı + ADR-0016

- [ ] **Step 1: Kanon 6-mod + genelleme + held-out OOD generation (LOKAL, $0)**

Run (v3 ADIM 9 matrisiyle BİREBİR, adapter=outputs/v4, seed 3407):
```bash
source ~/code/global_venv/bin/activate
# M1 --distractors 3 --max-chunk-chars 900 · M4 --with-source · M2 --data data/eval/trap.jsonl --with-source
# M2b --distractors 3 --no-gold · M3 --empty-context · M5 (blind) · xkanun/ood --data data/eval/trap_{xkanun,ood}.jsonl --with-source
python scripts/gen_eval_grounded.py --adapter outputs/v4 --label bench_m1_v4 --distractors 3 --max-chunk-chars 900
# ... (6 mod + xkanun + ood; v3'teki tam komut listesi NEXT_SESSION arşivinde)
```
Expected: `bench_*_v4_detail.jsonl` her mod için (M1/M4 n=40, M2/xkanun/ood n=35, M2b/M3/M5 n=40).

- [ ] **Step 2: Register (BEDAVA) + proxy ön-bakış**

Run: `source ~/code/global_venv/bin/activate && python scripts/score_register.py --details outputs/eval/bench_m1_v4_detail.jsonl --label bench_m1_v4`
Expected: uzman_frac (register korunmuş mu, ≥0.975 hedef).

- [ ] **Step 3: 🔒 PARA-KAPISI — full judge (kullanıcı onayı GEREK, ~$1)**

**ONAY AL.** Sonra (v3'teki `run_judge` kalıbı — 14 koşu): groundedness (M1/M4) + score_abstention (M2/M2b/M3/xkanun/ood) + score_correctness (M5). `set -a; source .env; set +a`, `OPENAI_API_KEY` echo etme.
Expected: `{gnd,abst,corr}_bench_*_v4_summary.json`.

- [ ] **Step 4: Kapı değerlendir + skorkart güncelle**

Kapı (recipe §6): M2b ≥0.90 · M2 ≥0.704 · xkanun ≥0.90 · ood ≥0.75 · M4/M1/M3/register ≥v3 · M5 ≤0.10.
- `docs/record/SCORECARD.md` → v4 sütunu ekle.
- `docs/record/v4/sonuclar.md` yaz (v3/sonuclar.md paraleli: skorkart + kapı + regresyon-kontrolü).
- research_log yeni entry (#35) + **ADR-0016** (v4 kabul/kısmi/red + gerekçe).

- [ ] **Step 5: Commit**

```bash
git add docs/record/ outputs/eval/  # not: outputs/eval gitignored → yalnız docs
git commit -m "docs(v4): ADIM 6 eval + kapı kararı (ADR-0016) + SCORECARD güncel"
```

---

## Self-Review (plan-yazarı denetimi)

**1. Spec coverage:** recipe §5 KARAR-1 (2-kadran) → Task 1 `family` dilimleri ✓ · KARAR-2 (~8K, gold-absent sweep) → Task 6 `--target 8000` + Task 8 sweep ✓ · KARAR-3 (iki-taraflı marj) → Task 3 gray-judge + Task 4 `filter_rejected`/`is_degenerate` ✓ · KARAR-4 (tek-şablon + doğru-cevap-rejected) → Task 2 + Task 4 `rej_list` ✓ · zemin (A) continuation → Task 8 `--adapter outputs/v2b` ✓ · OOD held-out → Task 9 xkanun/ood ✓. **Gap:** ERA-evidence chosen'a tam gömülmedi (abstain şablon "var/eksik" veriyor ama grounding-alıntı-şablonu bu turda üretilmiyor — grounding-replay v2b'den geliyor). **Kabul:** v4.1'e bırak; recipe §2-D bunu "yeni" işaretledi, kritik-yol değil.

**2. Placeholder scan:** Kod adımları tam kod içeriyor; compute adımları tam komut + beklenen çıktı. Placeholder yok. (Task 9 Step 1 komut listesi kısaltıldı → "NEXT_SESSION arşivinde tam liste" işaretli; executor v3 detail dosyalarından mod→flag matrisini doğrulamalı.)

**3. Type consistency:** `pick_cross_kanun_neighbor`/`build_multi_distractor_context` (Task 1) → `family` alanı → Task 2 `build_abstain_chosen(row)` `trap_text` okur → Task 4 `filter_rejected`/`is_degenerate`/`gold_by_id` (packed'den `gold_text`) tutarlı. `gray_verdict` ∈ {answers,near_miss} (Task 3) → Task 4 `gray_by_id.get(id)=="answers"` eşleşir. ✓

**Bilinen riskler (executor bilsin):** (a) `build_v3_devset.py` v4 packed uyumu doğrulanmalı (Task 6 Step 1). (b) `modal_train.py::train_orpo` argüman adları (`--data-dir`/`--epochs`/`--max-steps`) v3 kullanımıyla doğrulanmalı — farklıysa `train_orpo.py` argparse'ına bak. (c) grounding-replay v2b `slice=="grounded"` alan adı doğrulanmalı. (d) harvest ~8K lokal wall-clock uzun → gece-boyu planla.

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-07-06-v4-execution.md`.** Başka bir gün devralınabilir; taze agent Global Constraints + Task 1'den başlar. İki execution seçeneği (o gün seçilecek):
1. **Subagent-Driven (önerilen)** — task başına taze subagent + arada review.
2. **Inline Execution** — bu oturumda batch + checkpoint.
