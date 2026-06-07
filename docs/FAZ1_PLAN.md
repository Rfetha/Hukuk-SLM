# FAZ 1 — Vatandaş-dilli Hukuk SLM — Nihai Execute Planı

> **Bu doküman Faz 1 için tek otoriter checklist'tir.** `TEKNIK_PLAN.md` ile çeliştiği yerde
> (özellikle eval = Muhakim, ve "bulk kanun çekimi önce") **bu doküman geçerlidir** (kararlar 2026-06-07).
> Strateji/gerekçe için `TEKNIK_PLAN.md`, veri için `VERI_PLANI.md`.

## Hedef
Gemma 4 12B'yi Türk hukukunda **doğru + sade Türkçe** konuşacak şekilde QLoRA ile fine-tune et.
**Bitiş kriteri:** sınav havuzunda baz modele göre **+%15** ve **göz testi 8/10**.

## Önkoşullar
- [x] Ortam: WSL2 + Blackwell sm_120 stack → `~/code/global_venv` (Py3.12, torch 2.10+cu128, unsloth 2026.6.1, bnb 0.49.2). env smoke yeşil, `requirements.lock.txt` kilitli.
- [x] Veri: `data/processed/sft_v0/` (32.234 Q&A, OrionCAF 18K+Renicames 14K, doğru ama **jargonlu**, medyan 30 kelime) + `data/raw/mevzuat_maddeler.jsonl` (40.853 madde, grounding zemini).
- [x] Base indir: `google/gemma-4-12B-it-qat-q4_0-unquantized` (24GB bf16) — **indirildi, tam.**
- [x] **Otonom driver:** `scripts/run_phase1.sh` (smoke→train→base eval→v0 eval→rapor, `set -e`, `V0_EPOCHS` env, `PYTHONUNBUFFERED`). Runbook: `docs/RUNBOOK_FAZ1.md`.

## Kararlar (sabit)
- **Eval terazisi = Muhakim DEĞİL.** Omurga = **staj/baro sınavı havuzu** (çoktan seçmeli, objektif %, $0) + **göz testi** (sade dil, milestone) + ara sıra **GPT-4o-mini hakem** (~5 kuruş). Gerekçe: `[[eval-harness-decision]]`.
- **Sadeleştirme öğretmeni = GPT-4o-mini** (32K ≈ $13, ucuz sigorta). Ama **local base 25-örnek bake-off** ile yan yana test edilir — local yeterliyse ileriki *büyük* üretimlerde (4b ~20K + Faz 4 niş) ona geçilir. "Güvenmeden önce doğrula."
- **Eğitim yeri = yerel** (12GB RTX 5070 Ti, batch=1 + grad-ckpt yeter). Büyük ablation → bulut (Faz 1 sonrası, opsiyonel).
- **Bulk kanun çekimi → Faz 2'ye ertelendi** (donmuş 40K madde Faz 1 için yeterli, çizelge S1).

## Akış

### Adım 1 — Eval terazisi kur ✅
- [~] ~~Staj/baro sınavı soru havuzu~~ → **ertelendi** (HF'de hazır MCQ havuzu yok; EDA edildi. Gerekirse sonra derlenir — `[[eval-harness-decision]]`).
- [x] Göz testi + hakem seti: `data/eval/eval_sample_v1.jsonl` (sabit-seed 30 gerçek vatandaş sorusu + avukat referans cevabı, `make_eval_sample.py`). base+v0 **aynı sorularla** ölçülür.
- [x] `scripts/eval.py`: model → cevap üret → **GPT-4o-mini hakem** (doğruluk + sadelik rubriği) → skor + göz testi md dökümü. `$OPENAI_BUDGET_USD` guard.
- **Çıktı:** ✅ çalışan terazi (revize omurga = izole sample + GPT-4o-mini hakem + göz testi).

### Adım 2 — Ham base ölç (referans) 🔄
- [ ] Fine-tune'suz Gemma 4 12B → `eval_sample_v1` → **referans skor** (doğruluk+sadelik). **Not:** sıra çevrildi — base eval, v0 eğitiminden SONRA koşar (base donuk, sıra skoru etkilemez); uzun işi öne aldık.
- **Çıktı:** base skoru.

### Adım 3 — v0 SFT (eldeki 32K jargon veri) 🔄 *ŞU AN KOŞUYOR*
- [x] `scripts/train_sft.py`: Unsloth FastModel, NF4 4-bit, `r=16/alpha=32/dropout=0.05` all-linear, batch=1 grad_accum=16, lr=2e-4, cosine, adamw_8bit, bf16, max_seq=2048, system prompt. **Smoke (5-step) yeşil.** ⚠️ Gemma 4 turn işaretleri `<|turn>user/model` (eski `<start_of_turn>` değil) — düzeltildi.
- [~] Eğit → **v0 adapter** → ölç. **KARAR: 2 yerine 1 epoch** (~1815 adım, ~12h; ~23.5s/adım ölçüldü) — hızlı geri bildirim, gerekirse epoch 2 sonra. *Şu an eğitiliyor.*
- [ ] Bariz bir **eğitim ayarı** hatası/fırsatı varsa (epoch/lr/seq) aynı veriyle tekrar eğit. (Veri sabit; veri iyileştirme = Adım 4.)
- **Beklenen açık:** "doğru ama jargonlu" (sadelik düşük çıkacak — beklenen, çare Adım 4 veri işi). **Çıktı:** `outputs/v0` adapter + `outputs/PHASE1_REPORT.md` (base vs v0 + delta).

### Adım 4 — Veriyi iyileştir
- [ ] **4a — 32K sadeleştir:** her uzman cevap → GPT-4o-mini → sade vatandaş Türkçesi (doğruluk korunur). ~$13.
- [ ] **4b — Grounded üretim:** eksik tipler (terim sadeleştirme, senaryo→atıf, madde özeti) gerçek maddelerden üret. Önce **50 kanıt** (25 GPT-4o-mini + 25 local base bake-off) → geçerse ~20K'ya ölçekle. Her örnekte `kaynak_madde`.
- [ ] sade 32K + grounded → birleşik **`sft_v1`**.
- **Çıktı:** `data/processed/sft_v1/`.

### Adım 5 — v1 SFT + iterasyon
- [ ] `sft_v1` ile yeniden FT → **v1 adapter** → ölç.
- [ ] İhtiyaca göre v2, v3… (veri ekle / ayar düzelt → ölç).
- **Çıktı:** sade model + skor eğrisi.

### Adım 6 — Bitiş + deploy artefaktı
- [ ] Bitiş kriteri: sınav **+%15** + göz **8/10**.
- [ ] Deploy: en iyi adapter → merge (bf16) → llama.cpp Q4_0 → **GGUF ~6.5GB** (8GB VRAM end-user).
- **Çıktı:** ✅ Faz 1 + GGUF.

## Döngü özeti
```
base ölç → FT(32K jargon)=v0 → ölç [ayar düzeltmesi varsa tekrar]
   └─ veriyi iyileştir (sadeleştir + grounded) = sft_v1
        └─ FT(v1) → ölç → [ihtiyaca göre v2…]
             └─ +%15 & göz 8/10 → merge → Q4_0 GGUF → Faz 1 bitti
```
