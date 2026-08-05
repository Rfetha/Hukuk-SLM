#!/usr/bin/env bash
# CP0 — düşünce modu ölçümü: 6-mod CANON üretimi, `--thinking on` (ADR-0040, sprint2.md CP0).
#
# Ne yapar: llama-server'ı açar, DEV havuzunda 6 modu üretir, KESİK-CEVAP KAPISINI uygular,
# sunucuyu kapatır. Puanlama AYRI betik: scripts/cp0_thinking_score.sh
#
# Kullanım:
#   bash scripts/cp0_thinking_gen.sh models/gguf/q35-4b-q4_k_m.gguf base_th          # CP0-a (6 mod)
#   THINK_BUDGET=1024 MAXTOK=512 bash scripts/cp0_thinking_gen.sh models/gguf/tg_v1-q4_k_m.gguf tg_v1_th
#
# Ortam: PORT=8080 · CTX=8192 · MAXTOK=4096 · NGL=99 · DEV=data/eval/dev · MODES="m1 m4 m2 m2b m3 m5"
#
# 🚨 Neden bu betik var (docs/record/yurutme-tuzaklari.md):
#   1.1 `--data` düşerse varsayılan EĞİTİM setinin komşusu gelir, hata vermez → burada AÇIK
#   1.2 `--thinking` düşerse ölçülen şey başka moddur                        → burada AÇIK
#   1.4 `--max-chunk-chars 900` eval-mirror değişmezi (ADR-0011)             → burada AÇIK
#   1.5 n/seed CP2 ile birebir aynı, yoksa delta anlamsız                    → tablo aşağıda
#   5.4 `set -e` mesajı yutar                                                → -e YOK, açık `die`
#   5.5 göreli yol `cd`'den sonra kayar                                      → GGUF başta mutlaklaştırılır
#
# ⚠️ CTX: Sprint 1 çıpaları `-c 4096` ile üretildi. Düşünce açıkken 4096 token'lık üretim bütçesi
# istemin YANINA sığmıyor → varsayılan 8192. İstem birebir aynı; değişen yalnız sunucu kapasitesi.
# Bu sapma künyeye yazılır (research_log #42).

set -uo pipefail        # -e BİLEREK yok: tuzak 5.4

die() { echo "❌ $*" >&2; exit 1; }

GGUF_IN="${1:?kullanım: cp0_thinking_gen.sh <gguf> <etiket-son-eki> }"
TAG="${2:?kullanım: cp0_thinking_gen.sh <gguf> <etiket-son-eki> }"

GGUF="$(readlink -f "$GGUF_IN")" || die "GGUF yolu çözülemedi: $GGUF_IN"
[ -f "$GGUF" ] || die "GGUF yok: $GGUF"

PORT="${PORT:-8080}"
CTX="${CTX:-8192}"
MAXTOK="${MAXTOK:-4096}"          # CEVAP bütçesi (bütçeli düşüncede Sprint 1 ile aynı: 512)
THINK_BUDGET="${THINK_BUDGET:-0}" # >0 → zorunlu kapatma (research_log #42); ÖN-KAYITLI seçilir
SERVER_URL="${SERVER_URL:-}"      # verilirse sunucu AÇILMAZ, var olan kullanılır
NGL="${NGL:-99}"
DEV="${DEV:-data/eval/dev}"
MODES="${MODES:-m1 m4 m2 m2b m3 m5}"
# Çıktılar KOŞU KLASÖRÜNE yazılır (2026-07-29): her ölçüm turu kendi dizininde + KUNYE.json.
# Düz `outputs/eval` artık yalnız koşu klasörlerini barındırır; oraya yazmak turları karıştırır.
OUT_DIR="${OUT_DIR:-outputs/eval/cp09-butceli-1024-512}"
BIN="${BIN:-$HOME/code/llama.cpp/build-cuda/bin/llama-server}"
LOG="$OUT_DIR/cp0_server_${TAG}.log"

[ -x "$BIN" ] || die "llama-server yok: $BIN"
[ -f "$DEV/core_hard.jsonl" ] || die "DEV havuzu yok: $DEV/core_hard.jsonl"
[ -f "$DEV/trap.jsonl" ]      || die "DEV havuzu yok: $DEV/trap.jsonl"
mkdir -p "$OUT_DIR"

# n = CP2/CP6 ile BİREBİR (tuzak 1.5). N_OVERRIDE yalnız CP0-b'nin gözle-bakma koşusu için.
mode_args() {
  case "$1" in
    m1)  echo "--data $DEV/core_hard.jsonl --distractors 4 --n ${N_OVERRIDE:-80}" ;;
    m4)  echo "--data $DEV/core_hard.jsonl --with-source   --n ${N_OVERRIDE:-80}" ;;
    m2)  echo "--data $DEV/trap.jsonl      --with-source   --n ${N_OVERRIDE:-70}" ;;
    m2b) echo "--data $DEV/core_hard.jsonl --distractors 4 --no-gold --n ${N_OVERRIDE:-80}" ;;
    m3)  echo "--data $DEV/core_hard.jsonl --empty-context --n ${N_OVERRIDE:-80}" ;;
    m5)  echo "--data $DEV/core_hard.jsonl                 --n ${N_OVERRIDE:-80}" ;;   # kör
    # HARNESS AÇIK (sprint3 Adım 4): bağlamı distractor kurgusu değil RETRIEVER seçer.
    # m1 ile tek farkı bu; kırpma, sistem promptu ve üretim rejimi AYNI kalır.
    h1)  echo "--data $DEV/core_hard.jsonl --harness-indeks $HARNESS_INDEKS --harness-k ${HARNESS_K:-5} --n ${N_OVERRIDE:-80}" ;;
    # HARNESS AÇIK + ALTIN ABLASYONU (ADR-0056 Karar 1) = m2b'nin harness-AÇIK karşılığı.
    # h1 ile tek farkı budur; k, kırpma, istem ve rejim AYNI kalır.
    h2b) echo "--data $DEV/core_hard.jsonl --harness-indeks $HARNESS_INDEKS --harness-k ${HARNESS_K:-10} --harness-no-gold --n ${N_OVERRIDE:-80}" ;;
    *)   return 1 ;;
  esac
}

# 🚨 Veri kapısı: h1 istendi ama indeks verilmediyse, model yüklenmeden dur (tuzak 6.2).
case " $MODES " in
  *" h1 "*|*" h2b "*) [ -n "${HARNESS_INDEKS:-}" ] || die "h1/h2b modu HARNESS_INDEKS ister (ör. data/index/mevzuat_bge_m3_s2)";;
esac

echo "### künye"
echo "  gguf      : $GGUF"
echo "  etiket    : *_${TAG}"
echo "  modlar    : $MODES"
echo "  thinking  : on   | cevap bütçesi: $MAXTOK | düşünce bütçesi: ${THINK_BUDGET:-—} | max_chunk_chars: 900 | seed: 3407"
echo "  sunucu    : ctx=$CTX  -ngl $NGL -fa on  KV q8_0/q8_0  port=$PORT
  harness   : ${HARNESS_INDEKS:-KAPALI}${HARNESS_INDEKS:+ · k=${HARNESS_K:-5}}"
echo "  güç       : $(cat /sys/class/power_supply/AC*/online 2>/dev/null | head -1 | sed 's/1/ŞARJDA/;s/0/PİLDE ⚠️/')"  # tuzak 1.6
echo

# ---- sunucu ----------------------------------------------------------------
stop_server() { :; }
if [ -n "$SERVER_URL" ]; then
  echo "ℹ️  var olan sunucu kullanılıyor: $SERVER_URL (yeni süreç açılmadı)"
else
  SERVER_URL="http://127.0.0.1:$PORT/v1"
  "$BIN" -m "$GGUF" -ngl "$NGL" -fa on --no-context-shift \
    --cache-type-k q8_0 --cache-type-v q8_0 -c "$CTX" \
    --host 127.0.0.1 --port "$PORT" > "$LOG" 2>&1 &
  SRV=$!
  stop_server() { kill "$SRV" 2>/dev/null || true; wait "$SRV" 2>/dev/null || true; }
  trap stop_server EXIT

  for _ in $(seq 1 120); do
    curl -sf "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 && break
    kill -0 "$SRV" 2>/dev/null || { tail -25 "$LOG"; die "llama-server öldü (log: $LOG)"; }
    sleep 2
  done
  curl -sf "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 || { tail -25 "$LOG"; die "sunucu 240s'te açılmadı"; }
  echo "✅ llama-server hazır (pid $SRV, log $LOG)"
fi
echo

# ---- üretim ----------------------------------------------------------------
for M in $MODES; do
  ARGS="$(mode_args "$M")" || die "bilinmeyen mod: $M"
  echo "==================== $M → ${M}_${TAG} ===================="
  # shellcheck disable=SC2086
  python scripts/gen_eval_grounded.py \
    --server-url "$SERVER_URL" --server-model local \
    --thinking on --max-new-tokens "$MAXTOK" --think-budget "$THINK_BUDGET" \
    --max-chunk-chars 900 --seed 3407 \
    --label "${M}_${TAG}" --out-dir "$OUT_DIR" $ARGS \
    || die "$M üretimi başarısız — sonraki modlar KOŞULMADI"
  echo
done

stop_server
trap - EXIT

# ---- 🚨 GEÇERLİLİK KAPISI (ADR-0040): kesik-cevap > %5 → koşu GEÇERSİZ --------
echo "==================== GEÇERLİLİK KAPISI ===================="
python - "$OUT_DIR" "$TAG" $MODES <<'PY'
import json, sys
out_dir, tag, modes = sys.argv[1], sys.argv[2], sys.argv[3:]
tot = trunc = 0; tok_sum = tok_n = 0; think_n = forced_n = 0
print(f"{'mod':<5} {'n':>4} {'kesik':>6} {'%':>6} {'ort tok':>8} {'düşünen':>8} {'zorla':>6}")
for m in modes:
    rows = [json.loads(l) for l in open(f"{out_dir}/{m}_{tag}_detail.jsonl", encoding="utf-8") if l.strip()]
    t = sum(1 for r in rows if r.get("finish_reason") == "length")
    tk = [r["completion_tokens"] for r in rows if r.get("completion_tokens")]
    th = sum(1 for r in rows if (r.get("reasoning_len") or 0) > 0)
    fc = sum(1 for r in rows if r.get("forced_close"))
    tot += len(rows); trunc += t; tok_sum += sum(tk); tok_n += len(tk); think_n += th; forced_n += fc
    print(f"{m:<5} {len(rows):>4} {t:>6} {100*t/max(1,len(rows)):>5.1f}% "
          f"{(sum(tk)/len(tk) if tk else 0):>8.1f} {th:>7} {fc:>6}")
pct = 100 * trunc / max(1, tot)
print(f"\nTOPLAM  n={tot}  kesik={trunc} (%{pct:.1f})  "
      f"ort completion_tokens={tok_sum/max(1,tok_n):.1f}  düşünce kanalı kullanan={think_n}/{tot}  "
      f"zorla kapatılan={forced_n}/{tot}")
if think_n == 0:
    print("\n🚨 HİÇBİR cevapta reasoning_content YOK → `enable_thinking` bayrağı işlemedi olabilir "
          "(#38 mekanizması). diag_chat_template.sh ile render'ı GÖZLE doğrula. SONUÇ OKUNMAZ.")
    sys.exit(2)
if pct > 5.0:
    print(f"\n🚨 KOŞU GEÇERSİZ — kesik-cevap %{pct:.1f} > %5 eşiği (ADR-0040 geçerlilik ön şartı).\n"
          "   Sonuç OKUNMAZ. MAXTOK büyütülüp tekrar koşulur; puanlamaya para harcanmaz.")
    sys.exit(2)
print("\n✅ Geçerlilik kapısı geçildi — sonuç okunabilir. Sıradaki: scripts/cp0_thinking_score.sh")
PY
