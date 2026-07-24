#!/usr/bin/env bash
# llama.cpp'yi KALICI olarak kur + CUDA ile derle + GGUF üret.
#
# Neden kalıcı: scratchpad oturum-kapsamlı, temizleniyor (2026-07-24'te 22 GiB
# build+GGUF kaybedildi). Kurulum ~/code/llama.cpp, çıktılar models/gguf/ (gitignored).
#
# Kullanım:  bash scripts/setup_llamacpp.sh [12b|e4b|all]
set -euo pipefail

LC="$HOME/code/llama.cpp"
VENV="$HOME/code/llamacpp_venv"          # global_venv'den AYRI — onu asla kirletme
OUT="$(cd "$(dirname "$0")/.." && pwd)/models/gguf"
HUB="$HOME/.cache/huggingface/hub"
WHAT="${1:-all}"

mkdir -p "$OUT"

# ── 1. izole venv ────────────────────────────────────────────────────────────
if [ ! -d "$VENV" ]; then
  echo "### izole venv kuruluyor (global_venv'e DOKUNULMAZ)"
  python3 -m venv "$VENV"
fi
"$VENV/bin/pip" install -q --upgrade pip cmake ninja 2>&1 | tail -1

# ── 2. llama.cpp ─────────────────────────────────────────────────────────────
if [ ! -d "$LC/.git" ]; then
  echo "### llama.cpp klonlanıyor → $LC"
  git clone --depth 1 https://github.com/ggml-org/llama.cpp.git "$LC" 2>&1 | tail -1
fi
cd "$LC" && echo "llama.cpp @ $(git log --oneline -1)"

# ── 3. CUDA derleme (sm_120 / Blackwell) ─────────────────────────────────────
CUDA_HOME="$HOME/code/cuda-12.9"
if [ ! -x "$LC/build-cuda/bin/llama-server" ]; then
  # nvcc: pip'teki nvidia-cuda-nvcc-cu12 YALNIZ ptxas içeriyor (nvcc yok), sistemde
  # CUDA toolkit kurulu değil, Linux için hazır llama.cpp CUDA binary'si de yok.
  # → NVIDIA resmî redistributable tarball'ları, sudo'suz (scripts/setup_cuda_toolkit.sh).
  [ -x "$CUDA_HOME/bin/nvcc" ] || bash "$(dirname "$0")/setup_cuda_toolkit.sh"
  NVCC="$CUDA_HOME/bin/nvcc"
  echo "nvcc: $("$NVCC" --version | tail -1)"
  echo "### CUDA build — sm_120 / Blackwell (uzun sürer)"
  "$VENV/bin/cmake" -B build-cuda -DGGML_CUDA=ON -DCMAKE_BUILD_TYPE=Release \
      -DLLAMA_CURL=OFF -DCMAKE_CUDA_COMPILER="$NVCC" \
      -DCMAKE_CUDA_ARCHITECTURES=120 -DCUDAToolkit_ROOT="$CUDA_HOME" 2>&1 | tail -5
  "$VENV/bin/cmake" --build build-cuda --config Release -j "$(nproc)" \
      --target llama-server llama-cli llama-quantize 2>&1 | tail -5
fi
ls -la "$LC/build-cuda/bin/llama-server"

# ── 4. dönüştürme bağımlılıkları ─────────────────────────────────────────────
"$VENV/bin/pip" install -q -r "$LC/requirements/requirements-convert_hf_to_gguf.txt" 2>&1 | tail -1

# ── 5. tokenizer yaması + dönüştürme ─────────────────────────────────────────
# Gemma 4'ün tokenizer_config'inde extra_special_tokens LİSTE; transformers 4.x
# DICT bekliyor → AttributeError. Snapshot'ı symlink'le kopyalayıp alanı düzelt.
prep() {
  local repo="$1" dst="$2"
  local snap; snap=$(ls -d "$HUB/$repo"/snapshots/*/ | head -1)
  rm -rf "$dst"; mkdir -p "$dst"
  for f in "$snap"*; do ln -sf "$(readlink -f "$f")" "$dst/$(basename "$f")"; done
  rm -f "$dst/tokenizer_config.json"
  "$VENV/bin/python" - "$snap" "$dst" <<'PY'
import json, sys
snap, dst = sys.argv[1], sys.argv[2]
d = json.load(open(f"{snap}/tokenizer_config.json"))
est = d.get("extra_special_tokens")
if isinstance(est, list):
    d["extra_special_tokens"] = {t.strip("<|>").replace("|", "_") + "_token": t for t in est}
json.dump(d, open(f"{dst}/tokenizer_config.json", "w"), ensure_ascii=False, indent=1)
PY
}

convert() {
  local repo="$1" tag="$2"
  [ -f "$OUT/$tag-q4_0-pure.gguf" ] && { echo "### $tag zaten var, atlanıyor"; return; }
  echo "### $tag: hazırlık + dönüştürme"
  prep "$repo" "/tmp/gguf-prep-$tag"
  cd "$LC"
  "$VENV/bin/python" convert_hf_to_gguf.py "/tmp/gguf-prep-$tag" \
      --outfile "$OUT/$tag-f16.gguf" --outtype f16 2>&1 | tail -6
  # --pure: token_embd Q6_K'ya YÜKSELTİLMEZ (ADR-0023 — QAT tam Q4_0 için kalibre)
  "$LC/build-cuda/bin/llama-quantize" --pure "$OUT/$tag-f16.gguf" \
      "$OUT/$tag-q4_0-pure.gguf" Q4_0 2>&1 | tail -4
  rm -f "$OUT/$tag-f16.gguf"    # 22 GiB ara dosya — Q4_0 üretildikten sonra gereksiz
  rm -rf "/tmp/gguf-prep-$tag"
}

[ "$WHAT" = "12b" ] || [ "$WHAT" = "all" ] && \
  convert "models--google--gemma-4-12B-it-qat-q4_0-unquantized" "g4-12b"
[ "$WHAT" = "e4b" ] || [ "$WHAT" = "all" ] && \
  convert "models--google--gemma-4-E4B-it-qat-q4_0-unquantized" "g4-e4b"

echo
echo "### SONUÇ — $OUT"
ls -la "$OUT"/*.gguf 2>/dev/null | awk '{printf "%-40s %7.2f GiB\n", $9, $5/1073741824}'
echo "Referans (2026-07-24 ölçümü): g4-12b-q4_0-pure = 6.26 GiB"
