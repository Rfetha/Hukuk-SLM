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
        "UNSLOTH_DISABLE_STATISTICS": "1",  # açılış telemetri çağrısı (HF stats) hang/timeout'unu önle
    })
    # Sadece eğitim script'i image'a; train_sft.py yerel import kullanmıyor.
    .add_local_dir("scripts", remote_path="/root/scripts")
)

# --- Volume'lar (main env, zaten kurulu) ---
data_vol = modal.Volume.from_name("hukuk-data")              # /data/sft_v1 (yükle: modal volume put), /data/eval
out_vol = modal.Volume.from_name("hukuk-outputs")            # checkpoint + adapter
hf_cache = modal.Volume.from_name("hukuk-hf-cache", create_if_missing=True)  # model cache


@app.function(
    image=image,
    gpu="A100",                              # 40GB
    volumes={"/data": data_vol, "/outputs": out_vol, "/cache/hf": hf_cache},
    secrets=[modal.Secret.from_name("huggingface-secret")],   # HF_TOKEN → gated indirme
    timeout=6 * 60 * 60,                     # tam epoch ~2.5h; 6h tampon
)
def train(run_name: str = "v1", epochs: float = 1.0, max_steps: int = -1,
          data_path: str = "/data/sft_v1", extra_args: list[str] | None = None):
    import subprocess
    import sys
    import time

    cmd = [
        sys.executable, "/root/scripts/train_sft.py",
        "--data", data_path,
        "--run-name", run_name,
        "--output-dir", f"/outputs/{run_name}",
        "--epochs", str(epochs),
    ]
    if max_steps and max_steps > 0:
        cmd += ["--max-steps", str(max_steps)]
    if extra_args:
        cmd += extra_args

    print("[modal] çalıştırılıyor:", " ".join(cmd), flush=True)
    # Popen + periyodik commit: eğitim sürerken ara checkpoint'leri (save_steps=200) buluta
    # kalıcılaştır. Kesinti olursa son commit'li checkpoint'ten resume edilir (train_sft
    # get_last_checkpoint ile otomatik). Tek-seferlik son commit yeterli DEĞİL — kesinti
    # commit'ten önce olursa checkpoint uçar.
    proc = subprocess.Popen(cmd)
    while proc.poll() is None:
        time.sleep(900)  # 15 dk
        try:
            out_vol.commit()
            print("[modal] ara commit → checkpoint kalıcı (resume güvencesi)", flush=True)
        except Exception as e:
            print(f"[modal] ara commit atlandı (önemsiz): {e}", flush=True)
    if proc.returncode != 0:
        raise SystemExit(f"[modal] train_sft HATA çıkış kodu={proc.returncode}")

    # Final: adapter + cache kalıcılaştır.
    out_vol.commit()
    hf_cache.commit()
    print(f"[modal] bitti → adapter: hukuk-outputs:/{run_name}", flush=True)


@app.local_entrypoint()
def main(smoke: bool = False, epochs: float = 1.0, run_name: str = "v1",
         data_path: str = "/data/sft_v1"):
    if smoke:
        # Kredi-dostu sağlık kontrolü: 50 step, config + loss doğrulama.
        print("[modal] SMOKE: 50 step deneme koşusu (~$0.15)", flush=True)
        train.remote(run_name=f"{run_name}-smoke", epochs=1.0, max_steps=50,
                     data_path=data_path)
    else:
        train.remote(run_name=run_name, epochs=epochs, data_path=data_path)


@app.local_entrypoint()
def spawn_train(epochs: float = 1.0, run_name: str = "v1", data_path: str = "/data/sft_v1"):
    """FIRE-AND-FORGET tam koşu. train.remote()/--detach client'a bağlı BEKLER → WSL/PC kapanınca
    client SIGTERM alıp Modal'a cancel yollar (4 kez bu yüzden öldü). train.spawn() ise job'ı
    kuyruğa atıp HEMEN döner — client/PC kapanması işi ETKİLEMEZ (gerçek bağımsız çalışma).

      modal run modal_train.py::spawn_train --epochs 1
    """
    call = train.spawn(run_name=run_name, epochs=epochs, data_path=data_path)
    print(f"[modal] SPAWNED ✓ FunctionCall={call.object_id} | run={run_name} epochs={epochs}",
          flush=True)
    print("[modal] Job Modal'da BAĞIMSIZ koşuyor; client/PC kapanması etkilemez.", flush=True)
    print(f"[modal] İzle: modal app logs <app-id> | Bitince: hukuk-outputs:/{run_name}", flush=True)


# ── v3 ADIM 2 — REJECTED HARVEST (inference, EĞİTİM DEĞİL, ucuz) ──────────────
# v2b modelini zor near-miss trap'lerde ORACLE framing'de (eval M2 birebir) koşturup GERÇEK
# fabrikasyonları toplar (ORPO rejected). Lokal RTX 5070 ~20s/örnek çok yavaş → A100'de hızlı.
# ÖN KOŞUL (yerelden bir kez):
#   modal volume put hukuk-data data/processed/sft_v3/packed_v3.jsonl /sft_v3/packed_v3.jsonl
#   (v2b adapter zaten hukuk-outputs:/v2b — eğitim çıktısı)
@app.function(
    image=image,
    gpu="A100",
    volumes={"/data": data_vol, "/outputs": out_vol, "/cache/hf": hf_cache},
    secrets=[modal.Secret.from_name("huggingface-secret")],
    timeout=3 * 60 * 60,
)
def harvest_rejected(target: int = 1500, batch: int = 16, max_new_tokens: int = 96,
                     packed: str = "/data/sft_v3/packed_v3.jsonl",
                     out: str = "/data/sft_v3/rejected.jsonl",
                     adapter: str = "/outputs/v2b"):
    import subprocess
    import sys
    import time

    cmd = [
        sys.executable, "/root/scripts/gen_v3_rejected.py",
        "--packed", packed, "--out", out, "--adapter", adapter,
        "--oracle", "--batch", str(batch), "--target", str(target),
        "--max-new-tokens", str(max_new_tokens),
    ]
    print("[modal] harvest:", " ".join(cmd), flush=True)
    proc = subprocess.Popen(cmd)
    while proc.poll() is None:
        time.sleep(300)                      # 5 dk: ara commit → resume/pull güvencesi
        try:
            data_vol.commit()
            print("[modal] ara commit → rejected.jsonl kalıcı", flush=True)
        except Exception as e:
            print(f"[modal] ara commit atlandı: {e}", flush=True)
    if proc.returncode != 0:
        raise SystemExit(f"[modal] harvest HATA çıkış={proc.returncode}")
    data_vol.commit()
    hf_cache.commit()
    print(f"[modal] harvest bitti → hukuk-data:{out}", flush=True)


# ── v3 ADIM 8 — ORPO EĞİTİM (PARA-KAPISI; smoke ADIM 7 önce) ──────────────────
# ÖN KOŞUL: build_orpo_v3.py çıktısı (train/validation.jsonl) Modal'da:
#   modal volume put hukuk-data data/processed/sft_v3/train.jsonl /sft_v3/train.jsonl
#   modal volume put hukuk-data data/processed/sft_v3/validation.jsonl /sft_v3/validation.jsonl
@app.function(
    image=image, gpu="A100",
    volumes={"/data": data_vol, "/outputs": out_vol, "/cache/hf": hf_cache},
    secrets=[modal.Secret.from_name("huggingface-secret")],
    timeout=6 * 60 * 60,
)
def train_orpo(run_name: str = "v3", epochs: float = 1.0, max_steps: int = -1,
               beta: float = 0.1, lr: float = 1e-5, grad_accum: int = 64):
    import subprocess
    import sys
    import time
    cmd = [
        sys.executable, "/root/scripts/train_orpo.py",
        "--data", "/data/sft_v3", "--adapter", "/outputs/v2b",
        "--run-name", run_name, "--output-dir", f"/outputs/{run_name}",
        "--epochs", str(epochs), "--beta", str(beta), "--lr", str(lr),
        "--grad-accum", str(grad_accum),
    ]
    if max_steps and max_steps > 0:
        cmd += ["--max-steps", str(max_steps)]
    print("[modal] ORPO:", " ".join(cmd), flush=True)
    proc = subprocess.Popen(cmd)
    while proc.poll() is None:
        time.sleep(900)
        try:
            out_vol.commit(); print("[modal] ara commit → v3 checkpoint kalıcı", flush=True)
        except Exception as e:
            print(f"[modal] ara commit atlandı: {e}", flush=True)
    if proc.returncode != 0:
        raise SystemExit(f"[modal] ORPO HATA çıkış={proc.returncode}")
    out_vol.commit(); hf_cache.commit()
    print(f"[modal] ORPO bitti → hukuk-outputs:/{run_name}", flush=True)


@app.local_entrypoint()
def spawn_v3(run_name: str = "v3", epochs: float = 1.0, smoke: bool = False,
             beta: float = 0.1, lr: float = 1e-5, grad_accum: int = 64):
    """v3 ORPO — FIRE-AND-FORGET. ÖNCE --smoke (ADIM 7 para-kapısı, ~50 step ~$0.15):
      modal run modal_train.py::spawn_v3 --smoke
      modal run modal_train.py::spawn_v3 --run-name v3 --epochs 1
    Bitince: modal volume get hukuk-outputs /v3 ./outputs/v3
    """
    if smoke:
        print("[modal] v3 ORPO SMOKE: 50 step (format+loss+OOM doğrulama, ~$0.15)", flush=True)
        call = train_orpo.spawn(run_name=f"{run_name}-smoke", epochs=1.0, max_steps=50,
                                beta=beta, lr=lr, grad_accum=grad_accum)
    else:
        call = train_orpo.spawn(run_name=run_name, epochs=epochs, beta=beta, lr=lr,
                                grad_accum=grad_accum)
    print(f"[modal] v3 SPAWNED ✓ FunctionCall={call.object_id} | run={run_name} "
          f"beta={beta} lr={lr} grad_accum={grad_accum} smoke={smoke}", flush=True)
    print("[modal] İzle: modal app logs hukuk-sft | forget-vekili: nll_loss trendi (tırmanırsa M1-risk)",
          flush=True)


@app.local_entrypoint()
def spawn_harvest(target: int = 1500, batch: int = 16, max_new_tokens: int = 96):
    """FIRE-AND-FORGET rejected harvest (inference). Bitince yerele çek:
      modal volume get hukuk-data /sft_v3/rejected.jsonl ./data/processed/sft_v3/rejected.jsonl
    """
    call = harvest_rejected.spawn(target=target, batch=batch, max_new_tokens=max_new_tokens)
    print(f"[modal] HARVEST SPAWNED ✓ FunctionCall={call.object_id} | target={target} batch={batch}",
          flush=True)
    print("[modal] Bağımsız koşuyor; client/PC kapanması etkilemez. İzle: modal app logs hukuk-sft",
          flush=True)


# v2b REÇETE varsayılanları (docs/V2_PLAN.md §5.1). v1'den farklar:
#  · --no-system  → v2b verisi SYSTEM_PROMPT_RAG_MULTI'yi messages[0]'da TAŞIR (çift system'i önle)
#  · lr=1e-4      → LoRA ≈ full-FT'nin 10x'i; v1'in 2e-4'ünden NAZİK (3e-4 YASAK = train_sft kilidi)
#  · r=16/α=32    → düşük rank, az-unutan davranışsal SFT (sweep: r=8/16)
#  · 1 epoch · warmup %5 · replay veride hazır (assemble --replay)
@app.local_entrypoint()
def spawn_v2b(run_name: str = "v2b", epochs: float = 1.0, lr: float = 1e-4,
              lora_r: int = 16, lora_alpha: int = 32, warmup_ratio: float = 0.05,
              data_path: str = "/data/sft_v2b", smoke: bool = False):
    """v2b davranışsal RAFT-SFT — FIRE-AND-FORGET, reçete §5.1 varsayılanları.

    ÖN KOŞUL: veri Modal volume'da olmalı:
      modal volume put hukuk-data data/processed/sft_v2b /sft_v2b

      # 1) Önce SMOKE (~50 step, config+loss doğrula, ~$0.15):
      modal run modal_train.py::spawn_v2b --smoke
      # 2) Loss düşüyorsa TAM koşu:
      modal run modal_train.py::spawn_v2b --run-name v2b --epochs 1
      # 3) Ablasyon (C2): farklı rank/lr veya ayrı veri dizini + ayrı --run-name
      modal run modal_train.py::spawn_v2b --run-name v2b-r8 --lora-r 8 --lora-alpha 16

    Bitince adapter: hukuk-outputs:/<run-name> → yerele çek:
      modal volume get hukuk-outputs /<run-name> ./outputs/<run-name>
    """
    extra = [
        "--no-system",                       # v2b veri system'i zaten taşır
        "--lr", str(lr),
        "--lora-r", str(lora_r),
        "--lora-alpha", str(lora_alpha),
        "--warmup-ratio", str(warmup_ratio),
    ]
    if smoke:
        print("[modal] v2b SMOKE: 50 step (config+loss doğrulama, ~$0.15)", flush=True)
        call = train.spawn(run_name=f"{run_name}-smoke", epochs=1.0, max_steps=50,
                           data_path=data_path, extra_args=extra)
    else:
        call = train.spawn(run_name=run_name, epochs=epochs, data_path=data_path,
                           extra_args=extra)
    print(f"[modal] v2b SPAWNED ✓ FunctionCall={call.object_id} | run={run_name} "
          f"lr={lr} r={lora_r} α={lora_alpha} warmup={warmup_ratio} epochs={epochs}", flush=True)
    print(f"[modal] reçete §5.1: 3e-4 YASAK (kilit aktif) · all-linear · replay veride · {data_path}",
          flush=True)
    print(f"[modal] İzle: modal app logs <app-id> | Bitince: hukuk-outputs:/{run_name}", flush=True)
