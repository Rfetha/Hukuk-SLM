# DEVİR NOTU — 2026-07-02 (v2b eval BİTTİ+geçti · sıradaki = v2c)

## TEK CÜMLE
v2b tam eğitim + 6-mod canon eval bitti, **tüm KAPILAR geçti** → sıradaki iş v2c;
**tüm v2c kararları tek otoritede: [`docs/record/v2c_roadmap.md`](docs/record/v2c_roadmap.md)** (burada TEKRARLAMA).

## v2b SONUÇ — TÜM KAPILAR GEÇTİ ✅ (detay: `docs/record/v2b_sonuclar.md`)
| Mod | Ölçüm | v2b | base | v1 |
|---|---|---|---|---|
| M1 distractor | A1 (cevaplanan) | **0.904** | 0.879 | — |
| M2b distractor-only (adil A3) | Rej* | **0.96** (n=30) | — | — |
| M3 boş | Rej* | **1.000** | 1.000 | — |
| M4 oracle | A1 | **0.975** | 0.977 | 0.960 |
| M5 KÖR | A2 | 0.175 | 0.225 | 0.300 |
| M2 TRAP-oracle (off-dist) | Rej* | 0.346 | 0.786 | 0.000 |
- v1'e karşı net kazandı: grounding korundu+aştı, abstention **dirildi** (0.000→0.96), unutma yok (replay).
- 2 methodology dersi: abstention'ı **eğitim moduyla ölç** (M2 0.346 artefakt, M2b 0.96 gerçek) · A1'i **cevaplananlarda** oku.

## SIRADAKİ: v2c → `docs/record/v2c_roadmap.md`
Regresyon kapısı, G1–G4 açıklar, Tier A/B/C/D/E ve execution sırası **hepsi roadmap'te.**
**İlk iş (roadmap §5):** Tier C (FT'siz eval adaleti: register ölç · shuffle teyit · base yeniden-skor) → Tier B (veri hijyeni) → Tier A (tek v2c SFT) → 6-mod regresyon eval.

## DOSYALAR
- **v2c OTORİTE:** `docs/record/v2c_roadmap.md` (v2c ADR bundan yazılacak)
- v2b scorecard: `docs/record/v2b_sonuclar.md` · Kayıt: `docs/record/research_log.md` (2026-07-02)
- Eval kod: `gen_eval_grounded.py` (`--max-chunk-chars` · `--no-gold`) · `score_abstention.py` (`--source-field`)
- Eğitim: `modal_train.py::spawn_v2b` · `train_sft.py` · ADR: 0010–0013 (+ v2c ADR yazılacak)
