#!/usr/bin/env python
"""
HakHukuk — Modal sarmalayıcı (Faz 1 SFT, bulut eğitim).

`scripts/train_sft.py`'a DOKUNMADAN onu Modal A100'de subprocess ile koşar.
Yerel RTX 5070 sadece prototip/eval; gerçek 12B QLoRA eğitimi burada (bkz CLAUDE.md).

Kullanım (yerelden):
  # 1) Önce KREDİ-DOSTU deneme koşusu (~50 step, ~3-4 dk, ~$0.15):
  modal run modal_train.py --smoke

  # 2) Loss düşüyor / config sağlamsa TAM koşu:
  modal run modal_train.py --epochs 1
  modal run modal_train.py --epochs 2 --run-name v0

  # 3) Bitince adapter'ı yerele çek (eval LOKALDE koşulur):
  modal volume get hukuk-outputs /v0 ./outputs/v0

GPU = A100 40GB (TEKNIK karar: 12B QLoRA tatlı nokta; H100 boşa, L4 yavaş).
"""
import modal

app = modal.App("hukuk-sft")

# --- Ortam: requirements.lock.txt'teki pinli sürümler (CUDA 12.x, A100 uyumlu) ---
# Modal'da Ampere/Ada GPU → yerel Blackwell sm_120 wheel derdi YOK.
image = (
    modal.Image.debian_slim(python_version="3.11")
    # --no-deps: lock zaten tam-çözülmüş düz liste (106 paket, tüm transitive pinli).
    # Resolver'ı atlar → unsloth'un eski `transformers<=5.5.0` metadata kısıtı çakışmaz
    # (yerel env de fiilen bu durumda: transformers 5.10.2 runtime'da unsloth ile çalışıyor).
    .pip_install_from_requirements("requirements.lock.txt", extra_options="--no-deps")
    .env({
        "HF_HUB_ENABLE_HF_TRANSFER": "1",   # gated Gemma (~24GB) hızlı indirme
        "HF_HOME": "/cache/hf",             # model cache → kalıcı volume (her koşuda yeniden indirme yok)
        "PYTHONUNBUFFERED": "1",            # loss canlı görünsün
    })
    # Sadece eğitim script'i image'a; train_sft.py yerel import kullanmıyor.
    .add_local_dir("scripts", remote_path="/root/scripts")
)

# --- Volume'lar (main env, zaten kurulu) ---
data_vol = modal.Volume.from_name("hukuk-data")              # /data/sft_v0, /data/eval
out_vol = modal.Volume.from_name("hukuk-outputs")            # checkpoint + adapter
hf_cache = modal.Volume.from_name("hukuk-hf-cache", create_if_missing=True)  # model cache


@app.function(
    image=image,
    gpu="A100",                              # 40GB
    volumes={"/data": data_vol, "/outputs": out_vol, "/cache/hf": hf_cache},
    secrets=[modal.Secret.from_name("huggingface-secret")],   # HF_TOKEN → gated indirme
    timeout=6 * 60 * 60,                     # tam epoch ~2.5h; 6h tampon
)
def train(run_name: str = "v0", epochs: float = 1.0, max_steps: int = -1,
          extra_args: list[str] | None = None):
    import subprocess
    import sys

    cmd = [
        sys.executable, "/root/scripts/train_sft.py",
        "--data", "/data/sft_v0",
        "--run-name", run_name,
        "--output-dir", f"/outputs/{run_name}",
        "--epochs", str(epochs),
    ]
    if max_steps and max_steps > 0:
        cmd += ["--max-steps", str(max_steps)]
    if extra_args:
        cmd += extra_args

    print("[modal] çalıştırılıyor:", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)

    # Çıktıyı kalıcılaştır (yoksa container ölünce uçar).
    out_vol.commit()
    hf_cache.commit()
    print(f"[modal] bitti → adapter: hukuk-outputs:/{run_name}", flush=True)


@app.local_entrypoint()
def main(smoke: bool = False, epochs: float = 1.0, run_name: str = "v0"):
    if smoke:
        # Kredi-dostu sağlık kontrolü: 50 step, config + loss doğrulama.
        print("[modal] SMOKE: 50 step deneme koşusu (~$0.15)", flush=True)
        train.remote(run_name=f"{run_name}-smoke", epochs=1.0, max_steps=50)
    else:
        train.remote(run_name=run_name, epochs=epochs)
