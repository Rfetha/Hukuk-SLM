# Faz 1 — Otonom Koşu Runbook

> Bu doküman, Faz 1 v0 zincirinin (Adım 1→3) otonom koşusunu tarif eder.
> Claude Code arka planda `scripts/run_phase1.sh`'i koşar; insan girişi gerekmez.

## Ne koşuyor

Tek driver, sıralı, `set -e` ile (herhangi adım patlarsa **durur**):

```
smoke (5-step eğitim) → base eval → v0 SFT (2 epoch) → v0 eval → rapor
```

| Adım | Komut | Çıktı |
|---|---|---|
| 0 — smoke | `train_sft.py --max-steps 5` | `outputs/smoke/` (pipeline yeşil mi) |
| 2 — base eval | `eval.py --label base` | `outputs/eval/base_*` |
| 3 — v0 train | `train_sft.py --run-name v0 --epochs 2` | `outputs/v0/` (LoRA adapter) |
| 3b — v0 eval | `eval.py --label v0 --adapter outputs/v0` | `outputs/eval/v0_*` |
| rapor | (inline) | `outputs/PHASE1_REPORT.md` |

## Nasıl başlatılır

```bash
bash scripts/run_phase1.sh            # tüm zincir
bash scripts/run_phase1.sh smoke      # sadece smoke (hızlı doğrulama)
bash scripts/run_phase1.sh from-base  # smoke atla
bash scripts/run_phase1.sh from-train # base eval'i de atla
```

Tüm çıktı hem ekrana hem **`outputs/phase1_run.log`**'a gider (arka planda izleme).

## Önkoşullar (hazır)

- venv: `~/code/global_venv` (Py3.12, torch 2.10+cu128, unsloth 2026.6.1, openai 2.41)
- GPU: RTX 5070 Ti 12GB (4-bit yükleme ~7.76GB → sığar)
- model: `google/gemma-4-12B-it-qat-q4_0-unquantized` (24GB, indirilmiş)
- veri: `data/processed/sft_v0/` (29K train / 1.6K val / 1.6K test)
- eval örneklemi: `data/eval/eval_sample_v1.jsonl` (30 soru, seed=3407, donmuş)
- `.env`: `OPENAI_API_KEY` set, `OPENAI_BUDGET_USD=5`, `JUDGE_MODEL=gpt-4o-mini`

## Nerede durur / nereye dikkat

- **Yeni kod hatası** → driver durur, log'da traceback. Claude uyanıp düzeltmeyi dener.
- **OOM** → `train_sft.py`'de `--grad-accum`/`--max-seq-len` düşür, smoke'tan tekrar.
- **OpenAI bütçe ($5) dolarsa** → hakem durur ama generation sürer; göz testi yine dökülür (skor=None).
- **İnternet yoksa** → eval hakemsiz koşar (generation OK), skor None.

## Bittiğinde nerede bakılır

- `outputs/PHASE1_REPORT.md` — base vs v0 skor tablosu + delta.
- `outputs/eval/{base,v0}_goz_testi.md` — sade dil göz testi (insan okuması).
- `outputs/eval/{base,v0}_detail.jsonl` — soru başına cevap + hakem skoru.
- `outputs/v0/` — eğitilmiş LoRA adapter (deploy/merge için).

## Beklenti (FAZ1_PLAN Adım 3)

v0 = "doğru ama jargonlu". Doğruluk base'e göre korunur/artar; **sadelik düşük
kalabilir** — sade dil iyileştirmesi Adım 4 (GPT-4o-mini ile 32K sadeleştirme).
Bu yüzden v0'da düşük sadelik skoru **başarısızlık değil, beklenen ara durum.**
