#!/usr/bin/env python3
"""Muhakim'i (newmindai/Muhakim, ArmoRM 8B doğruluk reward-model'i) yerele indir.

HF repo'su tek-shard'ı standart-dışı isimlendirmiş (`model-00001-of-00001.safetensors`,
index json YOK) → transformers 5.x onu `model.safetensors` diye arayıp bulamıyor.
Bu script indirir + dosyayı `model.safetensors`'a çevirir → `muhakim_judge.py` yerelden yükler.

Kullanım: python scripts/dl_muhakim.py   (~15GB, bir kez)
"""
import os
from huggingface_hub import snapshot_download

DST = "models/Muhakim"


def main():
    p = snapshot_download("newmindai/Muhakim", local_dir=DST,
                          ignore_patterns=["*.png", "images/*", "*.jpg"])
    print("[dl] indi:", p, flush=True)
    src = os.path.join(DST, "model-00001-of-00001.safetensors")
    tgt = os.path.join(DST, "model.safetensors")
    if os.path.exists(src) and not os.path.exists(tgt):
        os.rename(src, tgt)
        print("[dl] rename → model.safetensors", flush=True)
    print("[dl] dosyalar:", sorted(os.listdir(DST)), flush=True)


if __name__ == "__main__":
    main()
