# DEVİR NOTU — 2026-07-05 (v2c REDDEDİLDİ · v3 ORPO: harvest+paketleme KOŞTU · sırada ADIM 7 smoke)

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
Tasarım KİLİTLİ (8 düğüm). Offline pipeline + **harvest (ADIM 2) + paketleme (ADIM 6a) KOŞTU.**
- **Harvest:** `rejected.jsonl` n=1728, **1504 fab / fab_oranı 0.870**, mojibake %0.3 (pad-fix tuttu).
- **Paketleme:** `train.jsonl` **1741** (1449 abstain + 292 grounding) / val 53 → Modal volume'de.
- **Sıradaki tek iş = ADIM 7 Modal smoke (PARA-KAPISI, onay bekliyor):**
  `modal run --detach modal_train.py::train_orpo --run-name v3-smoke --max-steps 50` (~$0.15).
  Doğrular: v2b-continuation (`PeftModel is_trainable`) + is_pref collator-list + OOM/NaN/nll_loss.

## ÇÖZÜLEN ENGELLER (2026-07-05)
- Modal ağ engeli (2026-07-04 "Could not connect") KALKTI → harvest temiz koştu.
- **Modal detach kalıbı:** sade `.spawn()` (spawn_*) İPTAL olur → `modal run --detach ...::<function>` doğrudan çağır.
- Claude'un Bash'i artık dışa erişimli → Modal/HF/git doğrudan (`!` şart değil).

## DOSYALAR
- **v3 OTORİTE:** `docs/record/v3_recipe.md` (v3 ADR-0015 bundan yazılacak)
- v2c skorkart: `docs/record/v2c_sonuclar.md` · v2b: `docs/record/v2b_sonuclar.md` · Kayıt: `docs/record/research_log.md` (2026-07-05)
- v3 kod: `scripts/{gen_v3_rejected,gen_v3_chosen,build_v3_devset,build_orpo_v3,train_orpo}.py` · `modal_train.py::{harvest_rejected,train_orpo}` (doğrudan `--detach`)
- Eğitim = Modal A100 (`--detach`) · eval = lokal RTX 5070 (`source ~/code/global_venv/bin/activate`) · ADR: 0010–0014 (+ 0015 yazılacak)

> ❄️ v2c dondurulmuş planları: `docs/record/v2c_roadmap.md` + `v2c_fix_deep_research.md` (tarihsel, güncellenmez).
