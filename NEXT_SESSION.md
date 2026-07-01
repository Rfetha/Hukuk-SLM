# DEVİR NOTU — 2026-07-01 (v2b tam eğitim KOŞUYOR, dönünce = bitti mi? → eval)

## TEK CÜMLE
v2b tam eğitim Modal A100'de `--detach` ile **başlatıldı ve sağlıklı koşuyor** →
sıradaki tek iş: **bitti mi teyit → adapter çek → 🔴 eval-mirror → D1 canon eval**.

## ▶ KOŞAN İŞ (2026-07-01 23:40'ta başladı)
- **App:** `ap-mjvVVy5ZycRX5q69zcM9Tu` · FunctionCall `fc-01KWFPKKQZK44G3CWWV45FH36V`
- **State (başlangıç):** `ephemeral (detached)` · Tasks=1 · A100-40GB
- **Config kilidi doğrulandı:** lr=1e-4, r=16/α=32, all-linear, warmup=0.05, --no-system, 3e-4 YASAK
- **İlerleme (son görülen):** model yüklendi → tokenize bitti (17.323 train + 962 val) → Map/Filter → step'ler
- **Beklenen:** ~994 step × ~15.75s ≈ 4-4.5h · ~$15-18 (Modal $30 kredi; kart kapı olarak eklendi 2026-07-01)
- **⚠️ Modal kart dersi:** A100/H100 için hesaba ödeme yöntemi ŞART (kredi olsa bile). Kart eklendi.

## ▶ DÖNÜNCE — HIZLI PLAN (kopyala-yapıştır)

**Adım 0 — ortam:**
```bash
cd ~/code/Hukuk-SLM && source ~/code/global_venv/bin/activate
```

**Adım 1 — bitti mi? (adapter = tek gerçek kanıt):**
```bash
modal volume ls hukuk-outputs /v2b | grep adapter_model    # adapter_model.safetensors VARSA → bitti ✅
modal app list | grep ap-mjvVVy5ZycRX5q69zcM9Tu            # stopped + adapter var = başarı; task hâlâ varsa sürüyor
modal app logs ap-mjvVVy5ZycRX5q69zcM9Tu 2>&1 | tr '\r' '\n' | grep -iE "train_loss|train_runtime|Removed|Error|Trace"  # final loss + hata + "Removed N" (N küçük olmalı, truncation fix)
```
- **Bittiyse →** Adım 2.
- **App stopped ama adapter YOKSA (hata/yarıda öldü) →** logda Traceback oku; `train_sft.py` ara-checkpoint + oto-resume var → aynı komutu tekrar koş (kaldığı yerden devam):
  ```bash
  modal run --detach modal_train.py::spawn_v2b --run-name v2b --epochs 1
  ```

**Adım 2 — adapter'ı çek:**
```bash
modal volume get hukuk-outputs /v2b ./outputs/v2b
```

**Adım 3 — 🔴 D1 ÖNCESİ eval-mirror (ADR-0013) — ATLANIRSA EVAL HAKSIZ:**
900-char chunk kırpmayı eval tarafına AYNALA (`gen_eval_grounded.py` / `raft_pack.py`),
yoksa v2b'yi eğitildiğinden uzun context'le ölçeriz. `clip_sources_block` mantığı
`build_sft_v2b.py`'de hazır — `raft_pack.labeled_chunk`'a `max_chars` paramı ekleyip
`gen_eval_grounded` distractor modunda kullan.

**Adım 4 — D1 canon eval (base / v1 / v2b — aynı M1/M3):**
```bash
# M1 (gold+4 distractor, A1): faith ≥0.879 KORU
python scripts/gen_eval_grounded.py --label bench_m1_v2b --adapter outputs/v2b \
  --data data/eval/core_hard.jsonl --distractors 4 --n 40
python scripts/groundedness.py --details outputs/eval/bench_m1_v2b_detail.jsonl --label bench_m1_v2b --mode data
# M3 (empty-context, A3): abstention =1.000 KORU
python scripts/gen_eval_grounded.py --label bench_m3_v2b --adapter outputs/v2b \
  --data data/eval/core_hard.jsonl --empty-context --n 40
# KAPI (§6): A3≥0.741 · A1∧A2≥0.875 · A4≥0.9 · CORE-KÖR gerilemesin · +uzman-register/format
```

**Adım 5 — bulgu→research_log, karar→ADR (D3).**

## ŞU AN NEREDEYİZ
- **A-track ✅** — base baseline: M1 faithfulness **0.879**, M3 abstention **1.000**.
- **B-track ✅** — `answers.jsonl` 19.305/19.305 (grounded 15.458 / abstain 3.847). assemble (kept 18.670):
  train 17.323 / val 962 / test 962, slice = grounded 13.350 / abstain 3.455 / replay 518.
- **Truncation FIX ✅** — `--max-chunk-chars 900`: >2048 %11.6→%0.03, quote context'te %100. max_seq_len=2048.
- **Replay ✅** — `build_replay_tr.py` (AlicanKiraz0 MIT) → 600 örnek, assemble %3.
- **C-track 🟢 KOŞUYOR** — tam v2b eğitim A100'de detach'te başlatıldı (yukarı bkz).

## AÇIK İŞLER (bloklamaz)
- 🔴 **eval-mirror (Adım 3)** — D1'i bloklar.
- ⚪ **C2 ablasyon** — P [60/80/100] · replay [%1/5] · rank [8/16] (tam-run iyiyse).
- ⚪ **Doc temizliği (2026-07-01)** — 26 bulgu denetlendi, düzeltmeler uygulanıyor (ADR-0010 yazılıyor,
  bayat Qwen/vatandaş-dili/v0-sıradaki izleri SÜPERSED notuyla). Bitmişse research_log'a düş.

## DOSYALAR
- Plan: `docs/V2_PLAN.md` (§5.1 reçete · §5.2 pipeline · §9 execution)
- Kayıt: `docs/record/research_log.md`
- ADR: 0008 (spawn) · 0010 (uzman-register reframe) · 0011 (canon eval) · 0012 (scope) · 0013 (5-mod matris)
- Veri: `build_sft_v2b.py` · `gen_v2b_answers.py` · `build_replay_tr.py` · `raft_pack.py`
- Eğitim: `modal_train.py::spawn_v2b` · `train_sft.py` (3e-4 kilidi)
