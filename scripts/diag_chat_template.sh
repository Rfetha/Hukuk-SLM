#!/usr/bin/env bash
# Tanı: llama-server sohbet şablonunu nasıl işliyor + EOG kümesinde ne var?
# Gerekçe (2026-07-24): 12B duman testinde model durmadı, '<|turn>user' üretip
# kendi kendine konuşmaya devam etti — bir CANON koşusunu sessizce çöpe çevirecek hata.
set -euo pipefail
MODEL="${1:?gguf yolu gerekli}"
PORT=8091
BIN="$HOME/code/llama.cpp/build-cuda/bin/llama-server"

"$BIN" -m "$MODEL" -ngl 99 -fa on -c 4096 --host 127.0.0.1 --port "$PORT" \
  > /tmp/diag_server.log 2>&1 &
SRV=$!
trap 'kill $SRV 2>/dev/null || true' EXIT
for i in $(seq 1 90); do curl -sf "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 && break; sleep 2; done

echo "### /apply-template çıktısı (modele giden ham metin):"
curl -s "http://127.0.0.1:$PORT/apply-template" -H 'Content-Type: application/json' -d @- <<'JSON' | python3 -c "import sys,json;print(repr(json.load(sys.stdin)['prompt']))"
{"messages":[{"role":"system","content":"SISTEM METNI"},{"role":"user","content":"KULLANICI SORUSU"}]}
JSON

echo
echo "### /props → chat_template + EOG:"
curl -s "http://127.0.0.1:$PORT/props" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print('chat_template (ilk 200):', repr(d.get('chat_template','')[:200]))
print('bos:',d.get('bos_token'),' eos:',d.get('eos_token'))
"
echo
echo "### server log — token/EOG uyarıları:"
grep -iE "control-looking|eog|eos|template" /tmp/diag_server.log | head -10
