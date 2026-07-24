#!/usr/bin/env bash
# CUDA toolkit'i sudo'suz kur (NVIDIA resmî redistributable tarball'ları).
# Gerekçe: pip'teki nvidia-cuda-nvcc-cu12 yalnız ptxas içeriyor, nvcc YOK;
# sistemde CUDA toolkit kurulu değil; Linux için hazır llama.cpp CUDA binary'si yok.
# GPU (RTX 5070 Ti, sm_120) ve sürücü zaten çalışıyor — eksik olan sadece DERLEYİCİ.
set -euo pipefail
CUDA_ROOT="$HOME/code/cuda-12.9"
BASE="https://developer.download.nvidia.com/compute/cuda/redist"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

declare -A PKGS=(
  [cuda_nvcc]="cuda_nvcc/linux-x86_64/cuda_nvcc-linux-x86_64-12.9.86-archive.tar.xz"
  [cuda_cudart]="cuda_cudart/linux-x86_64/cuda_cudart-linux-x86_64-12.9.79-archive.tar.xz"
  [libcublas]="libcublas/linux-x86_64/libcublas-linux-x86_64-12.9.1.4-archive.tar.xz"
  [cuda_cccl]="cuda_cccl/linux-x86_64/cuda_cccl-linux-x86_64-12.9.27-archive.tar.xz"
  [cuda_nvrtc]="cuda_nvrtc/linux-x86_64/cuda_nvrtc-linux-x86_64-12.9.86-archive.tar.xz"
)

mkdir -p "$CUDA_ROOT"
for name in "${!PKGS[@]}"; do
  echo "### $name"
  curl -sL "$BASE/${PKGS[$name]}" -o "$TMP/$name.tar.xz"
  tar -xf "$TMP/$name.tar.xz" -C "$TMP"
  d=$(find "$TMP" -maxdepth 1 -type d -name "${name}-linux*" | head -1)
  cp -rn "$d"/* "$CUDA_ROOT/" 2>/dev/null || true
done

# Redistributable tarball'lar kütüphaneleri lib/ altına koyar, nvcc ise lib64/ arar.
ln -sfn "$CUDA_ROOT/lib" "$CUDA_ROOT/lib64"

echo "### doğrulama — gerçek derleme+link testi (sm_120)"
"$CUDA_ROOT/bin/nvcc" --version | tail -2
T=$(mktemp -d)
echo '__global__ void k(){} int main(){return 0;}' > "$T/t.cu"
"$CUDA_ROOT/bin/nvcc" -arch=sm_120 "$T/t.cu" -o "$T/t.out"
[ -x "$T/t.out" ] && echo "✅ nvcc derleme+link OK" || { echo "❌ link başarısız"; exit 1; }
rm -rf "$T"
echo "CUDA_ROOT=$CUDA_ROOT"
