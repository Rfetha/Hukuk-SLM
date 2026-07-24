#!/usr/bin/env bash
# Gemma 4 şablonu × llama.cpp minja uyumsuzluğunu kapatan bayrağı bul.
# Sorun: minja tanımsız `enable_thinking`'i "tanımlı+doğru" sayıyor →
#   sistem turuna <|think|> giriyor AMA üretim isteminin sonundaki
#   '<|channel>thought\n<channel|>' (reasoning bastırıcı) yazılmıyor.
# Beklenen DOĞRU istem sonu: '<|turn>model\n<|channel>thought\n<channel|>'
set -euo pipefail
MODEL="${1:?gguf yolu gerekli}"
PORT=8093
BIN="$HOME/code/llama.cpp/build-cuda/bin/llama-server"

try() {
  local label="$1"; shift
  "$BIN" -m "$MODEL" -ngl 99 -fa on -c 4096 --host 127.0.0.1 --port "$PORT" "$@" \
    > /tmp/fix_server.log 2>&1 &
  local srv=$!
  for i in $(seq 1 90); do curl -sf "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 && break
    kill -0 $srv 2>/dev/null || { echo "[$label] server öldü: $(tail -2 /tmp/fix_server.log)"; return; }
    sleep 2; done

  echo "── $label"
  curl -s "http://127.0.0.1:$PORT/apply-template" -H 'Content-Type: application/json' -d \
    '{"messages":[{"role":"system","content":"S"},{"role":"user","content":"U"}]}' \
    | python3 -c "import sys,json;print('   istem:',repr(json.load(sys.stdin)['prompt']))"

  curl -s "http://127.0.0.1:$PORT/v1/chat/completions" -H 'Content-Type: application/json' -d @- <<'JSON' \
    | python3 -c "
import sys,json
d=json.load(sys.stdin)
if 'choices' not in d: print('   HATA:',str(d)[:300])
else:
    c=d['choices'][0]
    print('   cevap:',repr(c['message']['content'][:160]))
    print('   bitiş:',c.get('finish_reason'))
" || echo "   (yanıt ayrıştırılamadı)"
{"model":"local","temperature":0,"max_tokens":150,"messages":[
{"role":"system","content":"Sen Türk hukuku alanında uzman bir asistansın. Yalnızca verilen KAYNAK MADDE'ye dayanarak cevap ver."},
{"role":"user","content":"KAYNAK MADDE:\nTürk Borçlar Kanunu Madde 146 — Kanunda aksine bir hüküm bulunmadıkça, her alacak on yıllık zamanaşımına tabidir.\n\nSORU: Genel zamanaşımı süresi nedir?"}]}
JSON
  kill $srv 2>/dev/null || true; wait $srv 2>/dev/null || true
}

try "A: varsayılan (bozuk referans)"
try "D: yamalı şablon (enable_thinking=false)" --chat-template-file configs/gemma4_nothink.jinja
