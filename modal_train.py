#!/usr/bin/env python
"""
HakHukuk — Modal sarmalayıcı (bulut eğitim). **Base-agnostik.**

`scripts/train_sft.py` / `scripts/train_orpo.py`'a DOKUNMADAN onları Modal GPU'sunda
subprocess ile koşar. Yerel kart sadece prototip/eval; gerçek eğitim burada.

⚠️ **Model adı bu dosyada YOK.** `--model` zorunlu parametre; verilmezse hata verir.
Sessizce yanlış base'e düşmek, saatler süren bir koşuyu çöpe çevirir.

⚠️ GPU da parametre: `HUKUK_GPU` env (varsayılan `A100`). Küçük base'de `L4`/`A10G` yeter,
büyükte `A100-80GB`/`H100`. Modal'da GPU dekoratör-zamanlı → env ile seçilir:
    HUKUK_GPU=L4 modal run modal_train.py::spawn_sft --model <repo> --data /data/<set>

⚠️ **`--data` KONTEYNER İÇİ YOLDUR, volume yolu DEĞİL.** `hukuk-data` volume'ü `/data`'ya
bağlanır (aşağıdaki VOLUMES), yani volume'deki `/<set>` konteynerde `/data/<set>` olur.
`--data /<set>` yazmak `FileNotFoundError: Unable to find '/<set>/train.jsonl'` verir — ve bu hata
(düzeltilmeden önce) model yüklendikten SONRA patlıyordu, yani ~10 dk GPU yakıyordu. Artık
`train_sft.py` veriyi model yüklemeden önce denetliyor.

Kullanım:
  # 0) Veriyi bir kez volume'a yükle  (volume kökü → /<set>)
  modal volume put hukuk-data data/train/<set> /<set>

  # 1) Önce SMOKE (~50 step, config+loss doğrulama)   ← DİKKAT: /data/<set>
  modal run --detach modal_train.py::spawn_sft --model <hf-repo> --data /data/<set> --smoke \
      --user-part '<|turn>user\n' --assistant-part '<|turn>model\n'

  # 2) Loss düşüyorsa tam koşu (aynı --user-part/--assistant-part ile)
  modal run --detach modal_train.py::spawn_sft --model <hf-repo> --data /data/<set> --run-name r1 \
      --epochs 1 --user-part '...' --assistant-part '...'

  # 3) Bitince adapter'ı yerele çek
  modal volume get hukuk-outputs /r1 ./outputs/r1
"""
import os

import modal

app = modal.App("hukuk-sft")

# GPU seçimi — base'e göre değişir, bu yüzden env'den. Dekoratör import-zamanı okur.
GPU = os.environ.get("HUKUK_GPU", "A100")

# --- Ortam: requirements.lock.txt'teki pinli sürümler ---
# ⚠️ --no-deps ZORUNLU: lock zaten tam-çözülmüş düz liste (tüm transitive pinli). Resolver'ı
# atlar → unsloth'un eski `transformers<=…` metadata kısıtı çakışmaz. (Yerel env de fiilen
# bu durumda: lock'taki transformers runtime'da unsloth ile çalışıyor.)
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install_from_requirements("requirements.lock.txt", extra_options="--no-deps")
    .env({
        "HF_HUB_ENABLE_HF_TRANSFER": "1",   # büyük/gated ağırlıklar için hızlı indirme
        "HF_HOME": "/cache/hf",             # model cache → kalıcı volume (her koşuda yeniden indirme yok)
        "PYTHONUNBUFFERED": "1",            # loss canlı görünsün
        "UNSLOTH_DISABLE_STATISTICS": "1",  # açılış telemetri çağrısı hang/timeout'unu önle
    })
    # ⚠️ Qwen3.5 HİBRİT linear-attention: 32 katmanın 24'ü linear-attention. Triton çekirdeği yoksa
    # transformers torch reference fallback'e düşer (özyineli durumu her timestep materyalize eder)
    # → A100-40GB'de ~36 s/it (ölçüldü, #39) = tam koşu ~10 sa.
    #
    # 🚨 **`fla-core` ZORUNLU — `flash-linear-attention` TEK BAŞINA İŞE YARAMAZ, HATTA ZARARLI.**
    # Paket 0.5.x'te İKİYE BÖLÜNDÜ (ölçüldü 2026-07-25, CP4): `flash-linear-attention` yalnız
    # `fla/layers` + `fla/models` taşıyor; ÇEKİRDEKLER (`fla.ops.gated_delta_rule`, `fla.modules`)
    # `fla-core`'da ve oraya `Requires-Dist: fla-core==<sürüm>` ile bağlanıyor. `--no-deps` bu bağı
    # kesiyor → konteynerde `import fla` ÇALIŞIYOR (dolayısıyla transformers'ın
    # `is_flash_linear_attention_available()` kapısı **True** dönüyor) ama `fla.modules` YOK
    # → `from fla.modules import FusedRMSNormGated` çöküyor ve model HİÇ yüklenmiyor.
    # Yani eksik `fla-core`, fla'nın hiç olmamasından KÖTÜ: yavaş-ama-çalışır yerine hiç-çalışmaz.
    # (Hata `transformers`'ın tembel-modül sarmalayıcısı yüzünden kök nedeni gizleyen tek satıra
    #  dönüşüyor: "Could not import module 'Qwen3_5ForConditionalGeneration'". Teşhis: modal_diag.py)
    #
    # Sürüm uyumu ÖLÇÜLDÜ: `fla-core` yalnız `torch>=2.7` + `triton>=3.3` istiyor; lock'ta
    # torch 2.10.0 + triton 3.6.0 var → **yeterli.** ⚠️ Devir notundaki *"fla torch>=2.11 istiyor,
    # ayrı bir Modal image kurulmalı"* teşhisi YANLIŞTI — pinli lock korunuyor, ayrı image gerekmiyor.
    #
    # `causal-conv1d` BİLEREK YOK: fla'nın opsiyonel extra'sı (`extra == "conv1d"`), derleme ister.
    # Yokluğunda yalnız depthwise conv torch'a düşer; PAHALI çekirdek (`chunk_gated_delta_rule`)
    # fla'dan gelir. ⚠️ Bu yüzden "fast path is not available" UYARISI YİNE BASILIR — uyarıyı
    # başarısızlık sanma, ölçüt **s/it**.
    .pip_install("einops", "fla-core", "flash-linear-attention", extra_options="--no-deps")
    .add_local_dir("scripts", remote_path="/root/scripts")
)

data_vol = modal.Volume.from_name("hukuk-data")
out_vol = modal.Volume.from_name("hukuk-outputs")
hf_cache = modal.Volume.from_name("hukuk-hf-cache", create_if_missing=True)
VOLUMES = {"/data": data_vol, "/outputs": out_vol, "/cache/hf": hf_cache}
SECRETS = [modal.Secret.from_name("huggingface-secret")]   # HF_TOKEN → gated indirme


def _require(name: str, value):
    """Sessiz yanlış-base'e düşmeyi engelle: kritik parametre boşsa erken patla."""
    if not value:
        raise SystemExit(
            f"[modal] 🚫 --{name} ZORUNLU. Base/veri bu dosyada gömülü DEĞİL "
            f"(bilerek: yanlış modele sessizce düşmek bir koşuyu çöpe çevirir)."
        )
    return value


def _run_with_commits(cmd, vols, every_s: int):
    """Alt süreci koştur + periyodik commit. Kesinti olursa son commit'li checkpoint'ten
    resume edilir (train_sft/train_orpo `get_last_checkpoint` ile otomatik).
    Tek-seferlik son commit YETMEZ — kesinti commit'ten önce olursa checkpoint uçar."""
    import subprocess
    import time

    print("[modal] çalıştırılıyor:", " ".join(cmd), flush=True)
    proc = subprocess.Popen(cmd)
    while proc.poll() is None:
        time.sleep(every_s)
        for v in vols:
            try:
                v.commit()
            except Exception as e:
                print(f"[modal] ara commit atlandı (önemsiz): {e}", flush=True)
        print("[modal] ara commit → checkpoint kalıcı (resume güvencesi)", flush=True)
    if proc.returncode != 0:
        raise SystemExit(f"[modal] HATA çıkış kodu={proc.returncode}")
    for v in vols:
        v.commit()


# ── SFT (QLoRA) ───────────────────────────────────────────────────────────────
@app.function(image=image, gpu=GPU, volumes=VOLUMES, secrets=SECRETS,
              timeout=6 * 60 * 60)
def train(model: str, data_path: str, run_name: str, user_part: str, assistant_part: str,
          epochs: float = 1.0, max_steps: int = -1, extra_args: list[str] | None = None):
    import sys
    cmd = [
        sys.executable, "/root/scripts/train_sft.py",
        "--model", model,
        "--data", data_path,
        "--run-name", run_name,
        "--output-dir", f"/outputs/{run_name}",
        "--epochs", str(epochs),
        # Maskeleme sınırları — train_sft.py bunları render'a karşı ASSERT eder;
        # yanlışsa eğitim başlamadan patlar (sessizce bozuk eğitmekten iyidir).
        "--user-part", user_part,
        "--assistant-part", assistant_part,
    ]
    if max_steps and max_steps > 0:
        cmd += ["--max-steps", str(max_steps)]
    if extra_args:
        cmd += extra_args
    _run_with_commits(cmd, [out_vol, hf_cache], every_s=900)
    print(f"[modal] SFT bitti → adapter: hukuk-outputs:/{run_name}", flush=True)


# ── ORPO (tercih öğrenmesi; adapter-continuation veya taze) ───────────────────
@app.function(image=image, gpu=GPU, volumes=VOLUMES, secrets=SECRETS,
              timeout=6 * 60 * 60)
def train_orpo(model: str, data_path: str, run_name: str, adapter: str | None = None,
               epochs: float = 1.0, max_steps: int = -1, beta: float = 0.1,
               lr: float = 1e-5, grad_accum: int = 64, save_steps: int = 100,
               bf16_base: bool = False, lora_dropout: float = -1.0,
               target_modules: str = ""):
    import sys
    cmd = [
        sys.executable, "/root/scripts/train_orpo.py",
        "--model", model,
        "--data", data_path,
        "--run-name", run_name,
        "--output-dir", f"/outputs/{run_name}",
        "--epochs", str(epochs), "--beta", str(beta), "--lr", str(lr),
        "--grad-accum", str(grad_accum), "--save-steps", str(save_steps),
    ]
    # ⚠️ REJİM EŞLEŞMESİ (τ_g ile merge edilebilirlik şartı) — sessizce ayrışırsa iki task-vector
    # farklı θ_base'den türer ve kıyaslanamaz olur. Bkz. docs/open_questions.md #13.
    if bf16_base:
        cmd += ["--bf16-base"]
    if lora_dropout >= 0:            # 0.0 geçerli DEĞER → `if lora_dropout:` yazılamaz (falsy tuzağı)
        cmd += ["--lora-dropout", str(lora_dropout)]
    if target_modules:               # varsayılan liste `in_proj_*` içermez → 24 katman LoRA'sız kalır
        cmd += ["--target-modules", *target_modules.split()]
    # adapter verilirse continuation (önceki turun kazanımı taşınır), yoksa base'e taze adapter.
    cmd += ["--adapter", adapter] if adapter else ["--fresh-adapter"]
    if max_steps and max_steps > 0:
        cmd += ["--max-steps", str(max_steps)]
    _run_with_commits(cmd, [out_vol, hf_cache], every_s=900)
    print(f"[modal] ORPO bitti → adapter: hukuk-outputs:/{run_name}", flush=True)


# ── REJECTED HARVEST (inference, eğitim değil — ucuz) ─────────────────────────
# Bir modeli zor near-miss tuzaklarında koşturup GERÇEK fabrikasyonları toplar (ORPO rejected).
@app.function(image=image, gpu=GPU, volumes=VOLUMES, secrets=SECRETS,
              timeout=3 * 60 * 60)
def harvest_rejected(model: str, packed: str, out: str, adapter: str | None = None,
                     target: int = 1500, batch: int = 16, max_new_tokens: int = 96):
    import sys
    cmd = [
        sys.executable, "/root/scripts/gen_v3_rejected.py",
        "--model", model, "--packed", packed, "--out", out,
        "--oracle", "--batch", str(batch), "--target", str(target),
        "--max-new-tokens", str(max_new_tokens),
    ]
    if adapter:
        cmd += ["--adapter", adapter]
    _run_with_commits(cmd, [data_vol, hf_cache], every_s=300)
    print(f"[modal] harvest bitti → hukuk-data:{out}", flush=True)


# ── Yerel giriş noktaları ─────────────────────────────────────────────────────
# ⚠️ HEPSİ spawn() kullanır, remote() DEĞİL (ADR-0008): remote() client'a bağlı BEKLER →
# PC/WSL kapanınca client SIGTERM alıp Modal'a cancel yollar (bu 4 koşuyu öldürdü).
# spawn() job'ı kuyruğa atıp hemen döner — client kapanması işi ETKİLEMEZ.

@app.local_entrypoint()
def spawn_sft(model: str = "", data: str = "", run_name: str = "r1",
              user_part: str = "", assistant_part: str = "",
              epochs: float = 1.0, smoke: bool = False,
              lr: float = 0.0, lora_r: int = 0, lora_alpha: int = 0,
              warmup_ratio: float = 0.0, no_system: bool = False,
              bf16_base: bool = False, target_modules: str = "",
              lora_dropout: float = -1.0, no_grad_checkpoint: bool = False,
              batch: int = 0, grad_accum: int = 0):
    """QLoRA SFT — fire-and-forget. Önce --smoke (para-kapısı), sonra tam koşu.

    --user-part / --assistant-part: base'in chat şablonundaki turn işaretleri.
    ⚠️ Bunlar base'e göre DEĞİŞİR ve yanlışsa responses-only maskeleme sessizce çalışmaz
    (loss tüm diziden akar = eğitim çöpe gider). Doğrusunu `diag_chat_template.sh` ile
    /apply-template render'ından oku. train_sft.py ayrıca render'a karşı assert eder.
    """
    _require("model", model); _require("data", data)
    _require("user-part", user_part); _require("assistant-part", assistant_part)
    extra = []
    if no_system:            # veri system prompt'unu zaten taşıyorsa çift-system'i önle
        extra += ["--no-system"]
    if lr:                   # ⚠️ lr ≥ 3e-4 train_sft.py'de kilitli (abstention çöküşü rejimi)
        extra += ["--lr", str(lr)]
    if lora_r:
        extra += ["--lora-r", str(lora_r)]
    if lora_alpha:
        extra += ["--lora-alpha", str(lora_alpha)]
    if warmup_ratio:
        extra += ["--warmup-ratio", str(warmup_ratio)]
    if bf16_base:            # ⚠️ ADR-0031 birincil: bf16 donuk taban + LoRA (QLoRA değil)
        extra += ["--bf16-base"]
    if target_modules:       # ⚠️ Qwen3.5 VLM: all-linear görüntü kulesine takar (#39) → metin kulesi listesi
        extra += ["--target-modules", *target_modules.split()]
    # ⚠️ ADR-0033 hız kaldıraçları. `lora_dropout` varsayılanı -1.0 = "dokunma" (script'in 0.05'i
    # kalır); 0.0 geçerli bir DEĞER olduğu için `if lora_dropout:` yazılamaz — 0.0 falsy'dir ve
    # bayrak sessizce yok sayılırdı. Tam da kaçınmaya çalıştığımız sessiz-yok-sayma sınıfı.
    if lora_dropout >= 0:
        extra += ["--lora-dropout", str(lora_dropout)]
    if no_grad_checkpoint:   # yalnız A100/H100 — yerel 12 GB kartta OOM
        extra += ["--no-grad-checkpoint"]
    # ⚠️ batch × grad_accum ÇARPIMI SABİT TUTULMALI (etkin batch = 16, reçete sabiti).
    # batch=1 varsayılanı YEREL 12 GB kartın kuralıydı; A100'de GPU boş çalışıyor.
    # İkisi birlikte verilir ki çarpım gözle denetlenebilsin.
    if batch:
        extra += ["--batch", str(batch)]
    if grad_accum:
        extra += ["--grad-accum", str(grad_accum)]
    if bool(batch) != bool(grad_accum):
        raise SystemExit("[modal] 🚫 --batch ve --grad-accum BİRLİKTE verilir "
                         "(etkin batch = çarpımları; tek başına vermek onu sessizce kaydırır).")

    parts = dict(user_part=user_part, assistant_part=assistant_part)
    if smoke:
        print(f"[modal] SMOKE: 50 step (config+loss doğrulama) · gpu={GPU}", flush=True)
        call = train.spawn(model=model, data_path=data, run_name=f"{run_name}-smoke",
                           epochs=1.0, max_steps=50, extra_args=extra, **parts)
    else:
        call = train.spawn(model=model, data_path=data, run_name=run_name,
                           epochs=epochs, extra_args=extra, **parts)
    print(f"[modal] SPAWNED ✓ {call.object_id} | model={model} data={data} "
          f"run={run_name} epochs={epochs} gpu={GPU} smoke={smoke}", flush=True)
    print(f"[modal] Bağımsız koşuyor. İzle: modal app logs hukuk-sft | "
          f"Bitince: modal volume get hukuk-outputs /{run_name} ./outputs/{run_name}", flush=True)


@app.local_entrypoint()
def spawn_orpo(model: str = "", data: str = "", run_name: str = "orpo1",
               adapter: str = "", epochs: float = 1.0, smoke: bool = False,
               beta: float = 0.1, lr: float = 1e-5, grad_accum: int = 64,
               save_steps: int = 100, bf16_base: bool = False,
               lora_dropout: float = -1.0, target_modules: str = ""):
    """ORPO tercih öğrenmesi — fire-and-forget.

    --adapter verilirse o turun kazanımı taşınır (continuation); boşsa base'e taze adapter.
    İzlenecek metrik: nll_loss trendi = forget-vekili (tırmanırsa grounding riski).

    ⚠️ τ_abstention KOLU olarak koşarken: `--adapter` VERİLMEZ (taze = ham base'den) ve
    `--bf16-base --lora-dropout 0.05 --target-modules '<τ_g ile aynı liste>'` verilir.
    Aksi hâlde τ_g ile merge edilemez — bkz. docs/open_questions.md #13.
    """
    _require("model", model); _require("data", data)
    common = dict(bf16_base=bf16_base, lora_dropout=lora_dropout,
                  target_modules=target_modules)
    if smoke:
        print(f"[modal] ORPO SMOKE: 50 step (format+loss+OOM doğrulama) · gpu={GPU}", flush=True)
        call = train_orpo.spawn(model=model, data_path=data, run_name=f"{run_name}-smoke",
                                adapter=adapter or None, epochs=1.0, max_steps=50,
                                beta=beta, lr=lr, grad_accum=grad_accum, **common)
    else:
        call = train_orpo.spawn(model=model, data_path=data, run_name=run_name,
                                adapter=adapter or None, epochs=epochs, beta=beta,
                                lr=lr, grad_accum=grad_accum, save_steps=save_steps, **common)
    print(f"[modal] ORPO SPAWNED ✓ {call.object_id} | model={model} "
          f"adapter={adapter or '(taze)'} beta={beta} lr={lr} ga={grad_accum} gpu={GPU}", flush=True)


@app.local_entrypoint()
def spawn_harvest(model: str = "", packed: str = "", out: str = "", adapter: str = "",
                  target: int = 1500, batch: int = 16, max_new_tokens: int = 96):
    """Fabrikasyon (rejected) toplama — inference, ucuz. Bitince yerele çek:
      modal volume get hukuk-data <out> ./data/...
    """
    _require("model", model); _require("packed", packed); _require("out", out)
    call = harvest_rejected.spawn(model=model, packed=packed, out=out,
                                  adapter=adapter or None, target=target,
                                  batch=batch, max_new_tokens=max_new_tokens)
    print(f"[modal] HARVEST SPAWNED ✓ {call.object_id} | target={target} gpu={GPU}", flush=True)
