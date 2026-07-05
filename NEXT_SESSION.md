# DEVİR NOTU — 2026-07-04 (v2c REDDEDİLDİ · aktif iş = v3 ORPO)

## TEK CÜMLE
v2c reddedildi (near-miss abstention düz SFT ile düzelmedi, K3 negatif bulgu) →
**aktif iş v3 = ORPO** (preference optimizasyonu); **tüm v3 kararları tek otoritede:
[`docs/record/v3_recipe.md`](docs/record/v3_recipe.md)** (burada TEKRARLAMA).

## v2c SONUÇ — ❌ REDDEDİLDİ (detay: `docs/record/v2c_sonuclar.md`, ADR-0014)
- Birincil hedef **M2 yanlış-kaynak red = 0.407** « §6 hedefi 0.90 (v2b 0.346'dan +0.06; base 0.704'ün bile altında).
- Ek regresyon: **M1 A1 = 0.832 < kapı 0.904.**
- **K3 negatif bulgu:** "ucuz SFT counterfactual near-miss reddini restore eder" hipotezi ÇÜRÜDÜ →
  teslim düz SFT değil, **preference (ORPO)** olmalı.

## SIRADAKİ: v3 → `docs/record/v3_recipe.md`
Tasarım KİLİTLİ (8 düğüm, grilling ürünü). Offline pipeline kuruldu (ADIM 1-6): eval-aynası +
ORACLE framing + `MaskedORPOTrainer`. **Sıradaki iş = ADIM 7 Modal smoke** (v2b-continuation +
is_pref collator + OOM/NaN doğrulaması) → sonra tam ORPO run.

## AÇIK ENGEL (2026-07-04)
Modal erişimi gecesinde kesikti ("Could not connect to the Modal server"); harvest/eğitim
başlatılamadı. Ağ gelince: komutlar v3_recipe.md §HANDOFF'ta. Kod hazır.

## DOSYALAR
- **v3 OTORİTE:** `docs/record/v3_recipe.md` (v3 ADR-0015 bundan yazılacak)
- v2c skorkart: `docs/record/v2c_sonuclar.md` · v2b: `docs/record/v2b_sonuclar.md` · Kayıt: `docs/record/research_log.md` (2026-07-04)
- v3 kod: `scripts/{gen_v3_rejected,gen_v3_chosen,build_v3_devset,build_orpo_v3,train_orpo}.py` · `modal_train.py::{spawn_harvest,spawn_v3}`
- Eğitim = Modal A100 (`--detach`) · eval = lokal RTX 5070 (`source ~/code/global_venv/bin/activate`) · ADR: 0010–0014 (+ 0015 yazılacak)

> ❄️ v2c dondurulmuş planları: `docs/record/v2c_roadmap.md` + `v2c_fix_deep_research.md` (tarihsel, güncellenmez).
