# Sonraki Oturum — Durum + Başlangıç

**Proje:** HakHukuk / Hukuk-SLM — Türkçe hukuk SLM (çift kitle: profesyonel + vatandaş).
**Base:** Gemma 4 12B (`gemma-4-12B-it-qat-q4_0-unquantized`) + QLoRA → Q4_0 GGUF deploy.
**Önce oku:** `CLAUDE.md`, `docs/FAZ1_PLAN.md` (otoriter), `docs/PAPER_TARGET.md`, hafıza `[[eval-accuracy-gate]]` + `[[paper-target]]` + `[[cloud-gpu-modal]]`.

---

## ⏳ GECE BOYUNCA KOŞUYOR (2026-06-09): v1 SFT — Modal A100
- **App `ap-xdvPwcsAMyCEMe9Y5wNR1g`** (run_name=v1, 1 epoch, 1207 step, ~3.5h). Gece ~01:00'de step 62'deydi, loss ~0.95 plato, ETA ~3.4h → sabaha **BİTMİŞ** olmalı. **PC kapalıyken Modal'da bağımsız koşar** (spawn+detach kanıtlandı: IDE kapat-aç testi geçti, step 29→41→62 kesintisiz, cancellation yok).
- **⚠️ BAŞLATMA YÖNTEMİ — ÖNEMLİ DERS (ADR-0008):** `modal run [--detach] modal_train.py` (train.remote) client'a bağlı BEKLER → WSL/PC kapanınca client SIGTERM→Modal'a cancel → job ölür (v1 bu yüzden **4 kez** erken öldü, step 31/13/...). **ÇÖZÜM = fire-and-forget:**
  ```
  modal run --detach modal_train.py::spawn_train --epochs 1
  ```
  spawn = bekleyen client YOK (kapanınca cancel gönderecek şey yok) + --detach = app yaşar.
- **SABAH İLK İŞ:**
  1. Bitti mi: `modal app list` (`ap-xdvP...` durum?) + `modal app logs ap-xdvPwcsAMyCEMe9Y5wNR1g | tail` (`[modal] bitti` + eval_loss göründü mü; cancellation = öldü).
  2. Bittiyse adapter indir: `modal volume ls hukuk-outputs /v1` (adapter_model.safetensors) → `modal volume get hukuk-outputs /v1 ./outputs/v1`
  3. **ÖLMÜŞSE** (cancellation/stopped): yeniden `modal run --detach modal_train.py::spawn_train --epochs 1`. Checkpoint ≥200 varsa oto-resume kaldığı yerden (save_steps=200 + get_last_checkpoint).
  4. **Eval LOKAL (asıl karar):** base vs v1 groundedness scorecard (aşağıdaki Adım 6). v1 base'i geçti mi? → geçtiyse bitti; zayıfsa 2. epoch (kredi ~$18-20 → yeter).

---

## NEREDE KALDIK (2026-06-08)

**Faz 1 Adım 4 (grounded veri) + KALİTE KAPISI BİTTİ. Adım 5 (v1 SFT, Modal A100) BAŞLADI/KOŞUYOR.**

- v0 başarısız olmuştu (32K forum verisi base-altı doğruluk → modeli batırdı). Çözüm: doğruluğu **gerçek kanun maddesinden imal et** (grounded). Kanıtlandı.
- **`data/processed/sft_v1/` üretildi (21458 saf grounded Q&A):** train 19305 / val 1131 / test 1022, ~$1.16. 2716 vatandaş-çekirdek maddesi → madde başına 3-8 ayrık çift, GPT-4o-mini. **32K KATILMADI** (v0'ı batıran + kaynaksız). Üretici `scripts/gen_sft_v1.py` (incremental + resume + timeout).
- **EĞİTİM-ÖNCESİ KALİTE KAPISI GEÇİLDİ (ADR-0002):** `scripts/score_grounded_corpus.py` (madde-metni join → gerçek groundedness; `score_corpus.py` tek başına referans=cevap koyduğu için YANILTICIYDI — köprü o boşluğu kapatır). n=40 → **faithfulness 0.984** / hall 0.016 / cit_precision 1.0 / wrong_ref 0.0. Skorlayıcı meta/atıf-claim artefaktı `groundedness.py`'de giderildi (0.947→0.984; gerçek hata id=32 maskelenmedi → fix prensipli).
- **Karar defteri kuruldu: `docs/adr/` (7 ADR).** Yeni büyük karar = anında ADR. `[[adr-decision-log]]`

### Sabit kararlar (bu hafta alındı — docs + hafızada)
1. **Ana metrik = GROUNDEDNESS** (FactScore+ALCE, `scripts/groundedness.py`). Muhakim = ikincil/yanlı (kısa-sade'ye kör, K3 kanıtı). `[[eval-accuracy-gate]]`
2. **Sadelik MODEL ŞARTI YOK** → vatandaş sadeleştirmesi APP katmanı (Faz 3).
3. **Hedef = TR rakipleri geçen doğru+grounded SLM.** Rakip: `Mecellem-Qwen3-4B`, `Llama-3.1-8B`, GPT-4o tavan.
4. **Eğitim yeri = Modal** (serverless A100). Yerel RTX 5070 = prototip. `[[cloud-gpu-modal]]`
5. **İnsan-κ DESCOPE** (insan iş gücü yok) → yerine **hakem-uyumu** (gpt-4o-mini ↔ gpt-4o) + opsiyonel yazar-örneklem. Sayılar göreli.
6. **Öğretmen = GPT-4o-mini** (bake-off atlandı; faith 1.0 kanıtlı, ucuz).

---

## Adım 5: v1 SFT — DURUM (2026-06-09 gece)
> ✅ Kalite kapısı (faith 0.984) ✅ veri Modal volume'de (`/data/sft_v1`) ✅ smoke yeşil (eval_loss 0.95)
> ✅ tam koşu BAŞLADI ve gece koşuyor (yukarı bak). Tam koşu ~**3.5h ≈ ~$10** (5.5h değil; v1 daha küçük).
> Başlatma artık **`modal run --detach modal_train.py::spawn_train --epochs 1`** (ADR-0008).

Kalan: koşu bitsin → adapter indir (`modal volume get hukuk-outputs /v1 ./outputs/v1`) → Adım 6 eval.

> Kalite kapısını tekrar koşmak istersen (kanıtlı doğru köprü):
> `python scripts/score_grounded_corpus.py --data data/processed/sft_v1/train.jsonl --label sft_v1 --n 40`
> (`score_corpus.py`'yi TEK BAŞINA groundedness için kullanma — referans=cevap koyar, yanıltır.)

## SONRASI — Adım 6 (rakip + güvenilirlik + deploy)
- **Rakip baseline'ları BİZİM terazide ölç:** `Mecellem-Qwen3-4B`, `Llama-3.1-8B` → groundedness scorecard. ⚠️ paperlarından sayı ALMA — aynı sorular, aynı hakem, aynı seed.
- **Güvenilirlik (EN SON):** hakem-uyumu `groundedness.py --judge-model gpt-4o` ↔ gpt-4o-mini + opsiyonel yazar-örneklem.
- **Bitiş:** groundedness'te rakipleri ≥ → merge (bf16) → llama.cpp Q4_0 → GGUF ~6.5GB.

---

## NEREYE BAK (mevcut çıktılar)
- `data/processed/sft_v1/` — 21458 grounded çift (train/val/test); `raw_pool.jsonl` ham havuz
- `outputs/eval/gnd_sft_v1_fixed_summary.json` — v1 kalite kapısı (faith 0.984, fixed skorlayıcı)
- `docs/adr/` — 7 karar kaydı (ADR-0002 = v1 kalite kapısı + bulgular)
- `outputs/PHASE1_REPORT.md` — base vs v0 skorkart
- `outputs/v0/` — v0 LoRA adapter (başarısız referans)
- `modal_train.py` — Modal eğitim (v1 default, smoke kanıtlı)

## Hızlı komutlar
```bash
# Veri üretimi DURDUYSA (resume — kaldığı yerden, tekrar para ödemez):
cd ~/code/Hukuk-SLM && set -a && . ./.env && set +a && \
  nohup ~/code/global_venv/bin/python -u scripts/gen_sft_v1.py --max-pairs 8 --workers 4 > logs_genv1.log 2>&1 & disown
# Sadece split kur (üretim bittiyse, finalize):
python scripts/gen_sft_v1.py --split-only
# Groundedness (ANA metrik):
python scripts/groundedness.py --details <jsonl> --label <ad> --judge-model gpt-4o --runs 3
# Skorkart (ANA=groundedness, Muhakim ikincil):
python scripts/build_scorecard.py --labels <ad>
```

## Notlar
- **Eğitim = Modal A100** ($30 kredi, ~$11.5/epoch → ~2 koşu hakkı; smoke ile kredi koru).
- **Eval = LOKAL** ($0): groundedness (OpenAI hakem), Muhakim 8-bit yerelde. Muhakim'i Modal'a YÜKLEME.
- `.env` = `OPENAI_API_KEY` + `OPENAI_BUDGET_USD` (commit ETME).
- Bedesten/mevzuat.gov.tr **Türk IP** ister (Faz 2). OpenAI hakem TR IP istemez.
- Modal auth: `~/.modal.toml` profil `rfetha`; secrets `huggingface-secret` + `openai-secret` (DONE).
