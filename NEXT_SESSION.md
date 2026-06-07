# Sonraki Oturum — Durum + Başlangıç

**Proje:** HakHukuk / Hukuk-SLM — Türkçe vatandaş-dilli hukuk SLM.
**Base:** Gemma 4 12B (`gemma-4-12B-it-qat-q4_0-unquantized`) + QLoRA → Q4_0 GGUF deploy.
**Önce oku:** `CLAUDE.md`, `docs/FAZ1_PLAN.md` (otoriter checklist), `docs/RUNBOOK_FAZ1.md`.

---

## ŞU AN ne oluyor (2026-06-07)

🔄 **v0 SFT eğitiliyor** — `scripts/run_phase1.sh train-first` arka planda koşuyor.
- Veri: `data/processed/sft_v0/` (32K jargon Q&A, OrionCAF 18K + Renicames 14K)
- Config: QLoRA r=16/alpha=32 all-linear, NF4 4-bit, batch=1 grad_accum=16, lr=2e-4, cosine, **1 epoch** (~1815 adım, ~23.5s/adım → ~12h)
- GPU: RTX 5070 Ti 12GB, ~10GB kullanımda (sığıyor)
- Zincir (otomatik, `set -e`): **v0 SFT → base eval → v0 eval → `outputs/PHASE1_REPORT.md`**

**Bittiğinde nereye bak:**
- `outputs/PHASE1_REPORT.md` — base vs v0 skor tablosu + delta
- `outputs/eval/{base,v0}_goz_testi.md` — sade dil göz testi (insan okuması)
- `outputs/v0/` — eğitilmiş LoRA adapter

## BİTEN (bu oturum)

- [x] Ortam (Adım 1): `~/code/global_venv`, Blackwell sm_120 stack, env smoke yeşil
- [x] Base model indirildi (24GB bf16, tam)
- [x] **Eval terazisi:** `scripts/eval.py` (GPT-4o-mini hakem: doğruluk+sadelik) + `make_eval_sample.py` → `data/eval/eval_sample_v1.jsonl` (sabit 30 soru)
- [x] **Driver:** `scripts/run_phase1.sh` + `docs/RUNBOOK_FAZ1.md`
- [x] **Smoke yeşil** (5-step) — ⚠️ Gemma 4 turn işareti bug'ı yakalandı/düzeltildi (`<|turn>user/model`, eski `<start_of_turn>` değil)

## SIRADA ne var (v0 bitince)

1. **v0 eval sonucunu oku** — `PHASE1_REPORT.md`. Beklenti: doğruluk korunur/artar, **sadelik düşük** ("doğru ama jargonlu" — beklenen, panik yok).
2. **Karar:** epoch 2 eklemeye değer mi? (Genelde HAYIR — asıl kazanım epoch değil veri.)
3. **Adım 4 — veriyi iyileştir** (asıl iş):
   - 4a: 32K uzman cevabı → GPT-4o-mini ile **sade vatandaş Türkçesi** (~$13)
   - 4b: **grounded üretim** — eksik tipler (terim sadeleştirme, senaryo→atıf, madde özeti) gerçek `mevzuat_maddeler.jsonl` maddelerinden. Önce 50 kanıt (25 GPT-4o-mini + 25 local bake-off) → geçerse ~20K'ya ölçekle.
   - → birleşik `data/processed/sft_v1/`
4. **Adım 5 — v1 SFT** (`sft_v1` ile yeniden eğit) → ölç → gerekirse v2…
5. **Adım 6 — bitiş + deploy:** kriter = base'e +%15 & göz 8/10 → en iyi adapter → merge (bf16) → llama.cpp Q4_0 → **GGUF ~6.5GB**.

## Hızlı komutlar

```bash
# Durum:
tail -f outputs/phase1_run.log
grep -oE "[0-9]+/1815 \[[^]]*\]" outputs/phase1_run.log | tail -1

# Zinciri yeniden başlat (gerekirse):
bash scripts/run_phase1.sh train-first      # eğit→base eval→v0 eval→rapor
bash scripts/run_phase1.sh from-train       # sadece eğit→v0 eval→rapor
V0_EPOCHS=2 bash scripts/run_phase1.sh from-train   # 2 epoch istenirse

# Tek tek:
python scripts/eval.py --label base                       # ham base
python scripts/eval.py --label v0 --adapter outputs/v0    # FT'li
```

**Not:** Eğitim/eval **yerel GPU** gerektirir (12GB). Cloud agent'ta GPU+model yok → orada koşmaz.
Bedesten/mevzuat.gov.tr çekimleri **Türk IP** ister (Faz 2). OpenAI hakem TR IP istemez.
