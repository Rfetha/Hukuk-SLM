# Sonraki Oturum — Durum + Başlangıç

**Proje:** HakHukuk / Hukuk-SLM — Türkçe hukuk SLM (çift kitle: profesyonel + vatandaş).
**Base:** Gemma 4 12B (`gemma-4-12B-it-qat-q4_0-unquantized`) + QLoRA → Q4_0 GGUF deploy.
**Önce oku:** `CLAUDE.md`, `docs/FAZ1_PLAN.md` (otoriter), `docs/PAPER_TARGET.md`, hafıza `[[eval-accuracy-gate]]` + `[[paper-target]]` + `[[cloud-gpu-modal]]`.

---

## NEREDE KALDIK (2026-06-08)

**Faz 1 Adım 4 (grounded veri) + KALİTE KAPISI BİTTİ. Adım 5 (v1 SFT, Modal A100) BAŞLIYOR.**

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

## SIRADA NE VAR — Adım 5: v1 SFT (Modal A100)

> ✅ Kalite kapısı geçildi (faith 0.984). ✅ `modal_train.py` artık `/data/sft_v1` + `run_name=v1` **default**.
> Kalan adımlar (tekrar kalite ön-kontrol GEREKMEZ — geçti):

1. **Modal'a yükle:** `sft_v1` → `hukuk-data` volume (`/data/sft_v1`).
   ```bash
   modal volume put hukuk-data data/processed/sft_v1 /sft_v1
   ```

2. **Smoke → tam koşu** (modal_train default'ları artık v1):
   ```bash
   modal run modal_train.py --smoke                 # 50 step, ~$0.15, config/loss doğrula
   modal run modal_train.py --epochs 1              # tam, ~5.5h ≈ $11.5 (run_name=v1 default)
   ```

3. **Adapter indir → eval LOKAL:**
   ```bash
   modal volume get hukuk-outputs /v1 ./outputs/v1
   # sonra base/v0/v1 groundedness scorecard (LOKAL, $0)
   ```

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
