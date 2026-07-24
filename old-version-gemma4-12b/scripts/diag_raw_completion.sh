#!/usr/bin/env bash
# Ham /completion ile modelin GERÇEKTE ne ürettiğini gör (sohbet ayrıştırıcısı devrede değil).
# llama.cpp Gemma 4'ten '<|channel>thought ... <channel|>' bekliyor; üretmezse 500 veriyor.
# Soru: model bu diziyi hiç üretmiyor mu, yoksa istem mi yanlış?
set -euo pipefail
MODEL="${1:?gguf yolu gerekli}"
PORT=8095
BIN="$HOME/code/llama.cpp/build-cuda/bin/llama-server"
"$BIN" -m "$MODEL" -ngl 99 -fa on -c 4096 --host 127.0.0.1 --port "$PORT" > /tmp/raw_server.log 2>&1 &
SRV=$!; trap 'kill $SRV 2>/dev/null || true' EXIT
for i in $(seq 1 90); do curl -sf "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 && break; sleep 2; done

ask() {
  local label="$1" prompt="$2"
  echo "── $label"
  echo "   istem: $(printf '%q' "$prompt")"
  python3 -c "
import json,sys,urllib.request
body=json.dumps({'prompt':sys.argv[1],'n_predict':160,'temperature':0,'cache_prompt':False}).encode()
r=urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:$PORT/completion',body,{'Content-Type':'application/json'}))
d=json.load(r)
print('   ham çıktı:',repr(d['content']))
print('   durdu mu :',d.get('stop_type'),'| stopping_word:',repr(d.get('stopping_word','')))
" "$prompt"
}

Q='KAYNAK MADDE:\nTürk Borçlar Kanunu Madde 146 — Kanunda aksine bir hüküm bulunmadıkça, her alacak on yıllık zamanaşımına tabidir.\n\nSORU: Genel zamanaşımı süresi nedir?'

ask "1) sistemsiz, düz model turu" "$(printf "<|turn>user\n${Q}<turn|>\n<|turn>model\n")"
ask "2) boş düşünce kanalı ön-doldurulmuş" "$(printf "<|turn>user\n${Q}<turn|>\n<|turn>model\n<|channel>thought\n<channel|>")"
ask "3) sistem turu + <|think|> (llama.cpp'nin ürettiği)" "$(printf "<|turn>system\n<|think|>\nSen Türk hukuku uzmanısın.<turn|>\n<|turn>user\n${Q}<turn|>\n<|turn>model\n")"
