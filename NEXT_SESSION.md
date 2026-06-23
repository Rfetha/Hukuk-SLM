# DEVİR NOTU — 2026-06-24 (v2b veri HAZIR, tam eğitim başlatılacak)

## TEK CÜMLE
v2b verisi tamamlandı + truncation fix + replay Modal'a yüklendi, smoke config'i doğruladı →
sıradaki tek iş: **tam v2b eğitimini `--detach` ile başlat → adapter çek → D1 canon eval**.

## ▶ DÖNÜNCE — HIZLI PLAN (kopyala-yapıştır)

**Adım 0 — ortam:**
```bash
cd ~/code/Hukuk-SLM && source ~/code/global_venv/bin/activate
```

**Adım 1 — tam eğitimi başlat (`--detach` ŞART; ~4-4.5h, ~$15-18):**
```bash
modal run --detach modal_train.py::spawn_v2b --run-name v2b --epochs 1
```
Çıktıdaki **app-id**'yi not et (`ap-...`). Spawn = fire-and-forget → **PC'yi kapatabilirsin.**

**Adım 2 — koşuyor mu teyit (PC kapatmadan önce 1 kez):**
```bash
modal app list | grep <app-id>     # State=ephemeral, Tasks=1 olmalı (stopped/0 = ÖLDÜ, tekrar başlat)
modal app logs <app-id>            # ilk 5 dk: model yükle→tokenize→step başlar; "Removed N samples" → N küçük olmalı
```

**Adım 3 — ertesi gün / birkaç saat sonra dönünce: bitti mi?**
```bash
modal volume ls hukuk-outputs /v2b | grep adapter_model    # adapter_model.safetensors VARSA → bitti ✅
modal app list | grep <app-id>                              # State=stopped + adapter var = başarı; task hâlâ varsa sürüyor
modal app logs <app-id> 2>&1 | tr '\r' '\n' | grep -iE "train_loss|train_runtime|Error|Trace"  # final loss + hata var mı
```
- **Bittiyse →** Adım 4'e (adapter çek + eval).
- **App stopped ama adapter YOKSA (hata/yarıda öldü) →** logda Traceback'i oku; `train_sft.py` ara-checkpoint + oto-resume var → aynı komutu tekrar koş (kaldığı checkpoint'ten devam eder).

**Adım 4 — adapter çek + D1 eval:** aşağıdaki "YAPILACAKLAR" #3-#6. **🔴 D1'den ÖNCE eval-mirror (#4) yapılmazsa eval haksız olur.**

---

## ŞU AN NEREDEYİZ
- **A-track ✅** — base baseline ölçülü: M1 faithfulness **0.879**, M3 abstention **1.000**.
- **B-track ✅ BİTTİ** — `answers.jsonl` **19.305/19.305** (grounded 15.458 / abstain 3.847).
  İcra ve İflas (2.727) + Kat Mülkiyeti (552) topik-skew onarıldı. assemble (kept 18.670):
  `train 17.323 / val 962 / test 962`, slice = grounded 13.350 / abstain 3.455 / **replay 518**.
- **Truncation FIX ✅** — `--max-chunk-chars 900` (gold quote korunur): >2048 **%11.6→%0.03**,
  quote context'te %100. max_seq_len=2048 kalır.
- **Replay ✅** — `build_replay_tr.py` (AlicanKiraz0 MIT, genel TR) → 600 örnek, assemble %3.
- **C-track ✅ HAZIR + DOĞRULANDI** — smoke (eski veri) bitti: loss 1.411, ~15.75s/step, OOM yok.
  Düzeltilmiş veri Modal'da (`hukuk-data:/sft_v2b`, `--force` yüklendi).

## ⚠️ MODAL DERSİ (PC kapatınca patlamasın)
**`modal run --detach ...`** ŞART. Detach'siz koşu local entrypoint bitince app'i `stopped` yapıp
task'ı öldürüyor (gözlemlendi: 0 task). `--detach` = app bulutta `ephemeral`, PC/WSL kopsa da sürer.

## YAPILACAKLAR (sırayla)

### 1) (opsiyonel ama önerilir) Temiz-veri smoke — fix'i pratikte teyit (~$0.15)
```bash
cd ~/code/Hukuk-SLM && source ~/code/global_venv/bin/activate
modal run --detach modal_train.py::spawn_v2b --smoke
# logda "Removed 0 ... samples" görmeli (ilkinde 1.421'di). İzle:
modal app logs <app-id>
```

### 2) TAM eğitim (fire-and-forget, ~4-4.5 saat, ~$15-18)
```bash
modal run --detach modal_train.py::spawn_v2b --run-name v2b --epochs 1
# reçete §5.1 gömülü: lr=1e-4, r=16/α=32, all-linear, warmup=0.05, --no-system, replay veride.
# 3e-4 YASAK (train_sft kilidi aktif). ~994 step × ~15.75s/step.
# İzle: modal app logs <app-id>   |   PC'yi kapatabilirsin (detach).
```

### 3) Adapter'ı çek
```bash
modal volume get hukuk-outputs /v2b ./outputs/v2b
```

### 4) 🔴 D1 ÖNCESİ — eval=train dağılımı (ADR-0013)
**900-char chunk kırpmayı eval tarafına AYNALA** (`gen_eval_grounded.py` / `raft_pack.py`),
yoksa v2b'yi eğitildiğinden uzun context'le ölçeriz (haksız). `clip_sources_block` mantığı
`build_sft_v2b.py`'de hazır — `raft_pack.labeled_chunk`'a `max_chars` paramı ekleyip
`gen_eval_grounded` distractor modunda kullan.

### 5) D1 canon eval (base / v1 / v2b — aynı M1/M3)
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

### 6) Bulgu→research_log, karar→ADR (D3)

## AÇIK İŞLER (bloklamaz, sırası gelince)
- 🔴 **eval-mirror (madde #4)** — D1'i bloklar, tam-run'u bloklamaz.
- ⚪ **C2 ablasyon** — P [60/80/100] · replay [%1/5] · rank [8/16] (tam-run iyiyse).
- ⚪ pack seed'leri shuffle (partial-tolerant) — bu sefer %100 bitti, kritik değil.

## DOSYALAR
- Plan: `docs/V2_PLAN.md` (§5.1 reçete · §5.2 pipeline · §9 execution)
- Kayıt: `docs/record/research_log.md` (2026-06-24: B2 tam set · replay · truncation fix · detach)
- ADR: 0008 (spawn) · 0011 (canon eval) · 0012 (scope) · 0013 (5-mod matris)
- Veri scriptleri: `build_sft_v2b.py` (pack/assemble+clip) · `gen_v2b_answers.py` · `build_replay_tr.py` · `raft_pack.py`
- Eğitim: `modal_train.py::spawn_v2b` · `train_sft.py` (3e-4 kilidi)
