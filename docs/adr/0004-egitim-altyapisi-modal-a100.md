# ADR 0004 — Eğitim altyapısı: Modal serverless A100

- **Durum:** Yürürlükte (2026-06-08)
- **Geriye dönük kayıt.**

## Bağlam
Yerel rig RTX 5070 Laptop (12GB, Blackwell sm_120). 12B QLoRA yerelde `batch=1` +
gradient_checkpointing ile sıkışık ve yavaş; ayrıca sm_120 + CUDA 13.1 bleeding-edge → wheel derdi.
CLAUDE.md ilkesi: "yerel = prototip, gerçek eğitim = bulut." Bütçe minik ($30 kredi).

## Karar
Gerçek SFT eğitimi **Modal (serverless, `gpu="A100"` 40GB)** üzerinde. Yerel makine yalnız
prototip/smoke + **eval** + veri üretimi için. `modal_train.py`, `train_sft.py`'a **dokunmadan**
onu subprocess ile sarar (yerel/bulut tek script).

## Değerlendirilen alternatifler
- **Colab Pro A100 / Kaggle / RunPod** → ELENDİ. Modal: saniye-başı ödeme (kredi-dostu), kalıcı
  volume (model cache → her koşuda yeniden indirme yok), kod-olarak-altyapı (reprodüklenebilir image).
- **H100** → gereksiz; QLoRA compute-bound değil, ekstra güç boşa.
- **L4** → aynı $/epoch ama ~3× yavaş.
- **Eval'i de Modal'da koşmak** → REDDEDİLDİ; Muhakim 15GB reward modeli upload + GPU saati israfı.
  Eval lokalde ($0): adapter (~280MB) indir → yerelde değerlendir.

## Sonuç
- Smoke kanıtlandı: `modal run modal_train.py --smoke` (50 step) A100-40GB'de loss 2.108→0.976.
- Gerçek ölçüm: **~11 sn/step**, 1 epoch ≈ 1815 step ≈ **~5.5 saat ≈ ~$11.5** (ilk 2.5h tahmini yanlıştı).
- Image kritik detay: `pip_install_from_requirements(..., extra_options="--no-deps")` ŞART — lock
  tam-çözülmüş düz liste; resolver açılırsa unsloth'un `transformers<=5.5.0` metadata kısıtı çakışır.
- Auth/secrets kurulu (`huggingface-secret`, `openai-secret`). Modal'da CUDA 12.x stabil → Blackwell
  wheel derdi yok. (2026-06-08'de `--data` v0'a hard-code'luydu → ADR 0002 oturumunda v1'e parametrikleştirildi.)

## İlgili
`[[cloud-gpu-modal]]`, `modal_train.py`, `requirements.lock.txt`, ADR 0003
