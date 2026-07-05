# DEVİR NOTU — 2026-07-05 (v3 ORPO: ADIM 8 eğitim BİTTİ · reorg BİTTİ · sırada ADIM 9 eval)

## ⏳ CANLI DURUM (compact-sonrası ÖNCE BUNU OKU)
- **ADIM 8 tam ORPO ✅ BİTTİ** (Modal `ap-6mWKR1039jy99a9xl4Gtcv`, 56/56 step, 2 epoch). Traje ideal gerçekleşti: **nll_loss 7.65→2.96 (forget YOK)** + **margins -0.31→~0 (M2 öğrenildi)**, NaN/OOM yok. Sonuç kaydı: `docs/record/research_log/2026-07-05-v3-adim7-8-orpo-egitim-bitti.md`.
- **Adapter'lar volume'de HAZIR:** `hukuk-outputs:/v3` → **final (2ep) `adapter_model.safetensors` + `checkpoint-28` (~1ep)** İKİSİ de var. Çekmek için: `modal volume get hukuk-outputs /v3 ./outputs/v3` (LoRA adapter, küçük; para yok).
- **docs/record REORG ✅ BİTTİ** (subagent): research_log.md → `research_log/` (29 dated entry + index, byte-eşdeğer kanıtlı), v2b/v2c/v3 versiyon klasörleri (git mv), 14 dış pointer güncel, kırık-link=0. ⚠️ COMMIT EDİLMEDİ — insan commit'ler. Sil-listesi (9 ölü TODO) onay bekliyor (aşağı bak).
- **SIRADA = ADIM 9 eval (lokal, GPT-judge maliyeti, ONAY-KAPISI):** checkpoint-28 (1ep) vs final (2ep) kıyası.
- **Eval-dilimleri HAZIR (train'e dokunmadı):** `data/eval/trap_xkanun.jsonl` (35, çapraz-kanun) + `trap_ood.jsonl` (35, held-out sentetik-soru). ⚠️ trap_ood'da 2 SMK tuzağı ov~0.55 → kazara-cevaplama spot-check. temporal/çok-hop = defer (veri yok).
- **Kapı-sonrası reçeteler:** `docs/record/v3/receteler.md` (4 train-fix, v3-eval tetikler).
- **ADIM 9 komutları:** M1 `gen_eval_grounded.py --label bench_m1 --adapter outputs/v3 --distractors 3 --max-chunk-chars 900` · M2 `... --distractors 3 --no-gold ...`. Kanon 6-mod + trap_xkanun/trap_ood genelleme + Mecellem sütunu. KAPI: M2≥0.704 + M1 A1≥0.904 + tavan koru + M5 base-altı.

## TEK CÜMLE
v2c reddedildi (near-miss abstention düz SFT ile düzelmedi, K3 negatif bulgu) →
**aktif iş v3 = ORPO** (preference optimizasyonu); **tüm v3 kararları tek otoritede:
[`docs/record/v3/recipe.md`](docs/record/v3/recipe.md)** (burada TEKRARLAMA).

## v2c SONUÇ — ❌ REDDEDİLDİ (detay: `docs/record/v2c/sonuclar.md`, ADR-0014)
- Birincil hedef **M2 yanlış-kaynak red = 0.407** « §6 hedefi 0.90 (v2b 0.346'dan +0.06; base 0.704'ün bile altında).
- Ek regresyon: **M1 A1 = 0.832 < kapı 0.904.**
- **K3 negatif bulgu:** "ucuz SFT counterfactual near-miss reddini restore eder" hipotezi ÇÜRÜDÜ →
  teslim düz SFT değil, **preference (ORPO)** olmalı.

## SIRADAKİ: v3 → `docs/record/v3/recipe.md`
Tasarım KİLİTLİ (8 düğüm). Offline pipeline + **harvest (ADIM 2) + paketleme (ADIM 6a) KOŞTU.**
- **Harvest:** `rejected.jsonl` n=1728, **1504 fab / fab_oranı 0.870**, mojibake %0.3 (pad-fix tuttu).
- **Paketleme:** `train.jsonl` **1741** (1449 abstain + 292 grounding) / val 53 → Modal volume'de.
- **ADIM 7 smoke ✅ YEŞİL (4/4)** → **ADIM 8 tam eğitim ✅ BİTTİ** (yukarı CANLI DURUM). Sonraki insan-karar: ADIM 9 eval (lokal, GPT-judge maliyeti).

## ÇÖZÜLEN ENGELLER (2026-07-05)
- Modal ağ engeli (2026-07-04 "Could not connect") KALKTI → harvest temiz koştu.
- **Modal detach kalıbı:** sade `.spawn()` (spawn_*) İPTAL olur → `modal run --detach ...::<function>` doğrudan çağır.
- Claude'un Bash'i artık dışa erişimli → Modal/HF/git doğrudan (`!` şart değil).

## DOSYALAR
- **v3 OTORİTE:** `docs/record/v3/recipe.md` (v3 ADR-0015 bundan yazılacak)
- v2c skorkart: `docs/record/v2c/sonuclar.md` · v2b: `docs/record/v2b/sonuclar.md` · Kayıt: `docs/record/research_log/README.md` (2026-07-05)
- v3 kod: `scripts/{gen_v3_rejected,gen_v3_chosen,build_v3_devset,build_orpo_v3,train_orpo}.py` · `modal_train.py::{harvest_rejected,train_orpo}` (doğrudan `--detach`)
- Eğitim = Modal A100 (`--detach`) · eval = lokal RTX 5070 (`source ~/code/global_venv/bin/activate`) · ADR: 0010–0014 (+ 0015 yazılacak)

> ❄️ v2c dondurulmuş planları: `docs/record/v2c/roadmap.md` + `v2c/fix_deep_research.md` (tarihsel, güncellenmez).
