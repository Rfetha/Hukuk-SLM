#!/usr/bin/env bash
# HakHukuk — Faz 1 otonom driver (Adım 1→3).
#
# Zincir: smoke → v0 SFT → base eval → v0 eval → Muhakim hakem → birleşik skorkart.
#   Doğruluk=Muhakim (kapı) · Sadelik=GPT-4o-mini+göz (fark) · Ayrışma bayrağı.
#   SIRALI: SLM eval'leri (Gemma VRAM'de) bitince Muhakim 8-bit yüklenir → çakışma yok.
# Herhangi bir adım hata verirse `set -e` ile DURUR (boşa saatlerce eğitim yok).
# Arka planda koşmak için tasarlandı; tüm çıktı outputs/phase1_run.log'a da gider.
#
# Kullanım:
#   bash scripts/run_phase1.sh            # tüm zincir
#   bash scripts/run_phase1.sh smoke      # sadece smoke
#   bash scripts/run_phase1.sh from-base  # smoke atla, base eval'den başla
#   bash scripts/run_phase1.sh from-train # base eval atla, v0 train'den başla
set -euo pipefail

# --- Repo köküne geç ---
cd "$(dirname "$0")/.."
REPO="$(pwd)"

PY="${PY:-$HOME/code/global_venv/bin/python}"
STAGE="${1:-all}"

# Python stdout'u unbuffered yap → loss/log satırları ANINDA log'a düşer
# (yoksa ~4KB buffer dolana dek loss görünmez). Karar 2026-06-07.
export PYTHONUNBUFFERED=1

mkdir -p outputs/eval
LOG="$REPO/outputs/phase1_run.log"

# Tüm çıktıyı hem ekrana hem log'a (arka planda log'dan izlenir).
exec > >(tee -a "$LOG") 2>&1

banner() { echo ""; echo "======== $* ========  [$(date '+%H:%M:%S')]"; echo ""; }

# --- .env yükle ---
if [[ -f .env ]]; then
  set -a; source .env; set +a
  echo "[driver] .env yüklendi (OPENAI key $([[ -n "${OPENAI_API_KEY:-}" ]] && echo set || echo YOK), budget=${OPENAI_BUDGET_USD:-?})"
else
  echo "[driver] UYARI: .env yok — hakem skoru atlanacak."
fi

echo "[driver] başlangıç: $(date) | stage=$STAGE | py=$PY"
$PY -c "import torch; print('[driver] GPU:', torch.cuda.get_device_name(0), '| torch', torch.__version__)"

run_smoke() {
  banner "ADIM 0 — SMOKE (5-step eğitim, pipeline testi)"
  $PY scripts/train_sft.py \
    --run-name smoke --data data/processed/sft_v0 \
    --max-steps 5 --grad-accum 2 --output-dir outputs/smoke
  echo "[driver] ✅ smoke yeşil — pipeline çalışıyor."
}

run_base_eval() {
  banner "ADIM 2 — BASE EVAL (referans skor)"
  $PY scripts/eval.py --label base
}

run_v0_train() {
  EPOCHS="${V0_EPOCHS:-1}"   # karar 2026-06-07: hızlı geri bildirim için 1 epoch (~12h)
  banner "ADIM 3 — v0 SFT (32K jargon, ${EPOCHS} epoch)"
  $PY scripts/train_sft.py \
    --run-name v0 --data data/processed/sft_v0 --epochs "$EPOCHS"
  echo "[driver] ✅ v0 adapter → outputs/v0"
}

run_v0_eval() {
  banner "ADIM 3b — v0 EVAL"
  $PY scripts/eval.py --label v0 --adapter outputs/v0
}

run_muhakim() {
  # SIRALI: SLM eval'leri bitti (model VRAM'den indi) → Muhakim 8-bit yüklenir.
  # Kayıtlı {base,v0}_detail.jsonl cevaplarını doğruluk eksenlerinde puanlar.
  banner "ADIM 3c — MUHAKIM HAKEM (doğruluk kapısı)"
  $PY scripts/muhakim_judge.py --load 8bit --details \
    outputs/eval/base_detail.jsonl outputs/eval/v0_detail.jsonl
}

build_report() {
  # Birleşik skorkart: Doğruluk(Muhakim) | Sadelik(GPT+göz) | Ayrışma bayrağı.
  banner "SKORKART — Doğruluk(Muhakim) · Sadelik(GPT+göz) · Ayrışma"
  $PY scripts/build_scorecard.py --labels base v0
}

case "$STAGE" in
  smoke)       run_smoke ;;
  from-base)   run_base_eval; run_v0_train; run_v0_eval; run_muhakim; build_report ;;
  from-train)  run_v0_train; run_v0_eval; run_muhakim; build_report ;;
  # train-first: asıl FT'yi HEMEN başlat; referans base eval'i sonra koş (sıra bilimsel olarak fark etmez).
  train-first) run_v0_train; run_base_eval; run_v0_eval; run_muhakim; build_report ;;
  all)         run_smoke; run_base_eval; run_v0_train; run_v0_eval; run_muhakim; build_report ;;
  # sadece skorkartı yeniden üret (kayıtlı eval + Muhakim çıktısından, GPU'suz)
  scorecard)   build_report ;;
  # sadece Muhakim + skorkart (SLM eval'leri zaten varsa)
  muhakim)     run_muhakim; build_report ;;
  *) echo "[driver] bilinmeyen stage: $STAGE"; exit 2 ;;
esac

banner "✅ FAZ 1 DRIVER BİTTİ (stage=$STAGE)"
echo "[driver] bitiş: $(date)"
