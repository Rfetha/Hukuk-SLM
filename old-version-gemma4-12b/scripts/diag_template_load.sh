#!/usr/bin/env bash
# --chat-template-file GERÇEKTEN okunuyor mu? Benzersiz bir işaretle kanıtla.
# Ardından doğru düzeltmeyi (üretim istemine boş düşünce kanalı) dene.
set -euo pipefail
MODEL="${1:?gguf yolu gerekli}"
PORT=8097
BIN="$HOME/code/llama.cpp/build-cuda/bin/llama-server"
CFG="$(cd "$(dirname "$0")/.." && pwd)/configs"

render() {
  local label="$1"; shift
  "$BIN" -m "$MODEL" -ngl 99 -fa on -c 4096 --host 127.0.0.1 --port "$PORT" "$@" \
    > /tmp/tl_server.log 2>&1 &
  local srv=$!
  for i in $(seq 1 90); do curl -sf "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 && break
    kill -0 $srv 2>/dev/null || { echo "── $label → SERVER ÖLDÜ: $(tail -3 /tmp/tl_server.log)"; return; }
    sleep 2; done
  echo "── $label"
  curl -s "http://127.0.0.1:$PORT/apply-template" -H 'Content-Type: application/json' -d \
    '{"messages":[{"role":"system","content":"S"},{"role":"user","content":"U"}]}' \
    | python3 -c "import sys,json;print('   ',repr(json.load(sys.stdin)['prompt']))" || echo "   (render başarısız)"
  kill $srv 2>/dev/null || true; wait $srv 2>/dev/null || true
}

# 1) Dosya okunuyor mu? Tamamen sahte bir şablon ver.
printf 'ISARET_SABLON_OKUNDU' > /tmp/marker.jinja
render "1) işaret şablonu (dosya okunuyorsa 'ISARET_SABLON_OKUNDU' görülmeli)" --chat-template-file /tmp/marker.jinja

# 2) Gerçek düzeltme: resmî şablon + üretim isteminin sonuna KOŞULSUZ boş düşünce kanalı.
render "2) düzeltilmiş şablon" --chat-template-file "$CFG/gemma4_nothink.jinja"
