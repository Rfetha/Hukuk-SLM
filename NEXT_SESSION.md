# DEVİR NOTU — 2026-07-05 (v3 ORPO: ADIM 8 BİTTİ · reorg BİTTİ+push · ADIM 9 eval generation YARIDA — PC kapatıldı)

## ⏳ CANLI DURUM (compact/yeni-oturum ÖNCE BUNU OKU)
- **ADIM 8 tam ORPO ✅ BİTTİ** (Modal `ap-6mWKR1039jy99a9xl4Gtcv`, 56/56 step, 2 epoch). **nll_loss 7.65→2.96 (forget YOK)** + **margins -0.31→~0 (M2 öğrenildi)**. Sonuç kaydı: `docs/record/research_log/2026-07-05-v3-adim7-8-orpo-egitim-bitti.md`.
- **Adapter'lar LOKALDE ÇEKİLDİ:** `outputs/v3/adapter_model.safetensors` (final=2ep) + `outputs/v3/checkpoint-28/` (1ep), her ikisi 262 MB, teyitli. (Modal volume'de de duruyor.)
- **docs/record REORG ✅ BİTTİ + COMMIT+PUSH** (`e837e6a`): research_log.md → `research_log/` (30 dated entry + index), v2b/v2c/v3 klasörleri, pointer'lar güncel, kırık-link=0. Sil-listesi (9 ölü TODO) ONAYLANDI.

## 🔴 ADIM 9 EVAL — GENERATION YARIDA KALDI (PC kapatıldı; RESUME planı)
**Yöntem:** lokal RTX 5070 generation (para $0) → sonra GPT-judge (para-kapısı, ONAY GEREKİR). `gen_eval_grounded.py` tek-atışlık (her mod 12B reload). venv: `source ~/code/global_venv/bin/activate`.

**✅ ÜRETİLMİŞ detail (güvende, `outputs/eval/`):**
- v3-final 6/6: `bench_{m1(40),m4(40),m2(35),m2b(40),m3(40),m5(40)}_v3_detail.jsonl`
- v3-ckpt28: `bench_m1_v3ck28_detail.jsonl` ⚠️ **YARIM (29/40) — YENİDEN ÜRET** (kesildi).

**⏳ KALAN generation (resume'da koş):**
1. v3-ckpt28: **M1 (yeniden, yarım)** + **M2** — kapı-eksenleri, 1-vs-2 epoch kıyası.
2. Genelleme (M2-modu = `--data <trap> --with-source`): `trap_xkanun.jsonl` + `trap_ood.jsonl` → **v3-final + base + v2b** (6 koşu; base/v2b kanon detail'leri zaten cache'te, sadece bu 2 yeni dilim).
3. Register (BEDAVA): `score_register.py --details outputs/eval/bench_m1_v3_detail.jsonl --label bench_m1_v3` (+ v3ck28).

**Mod→flag matrisi (v2c detail'leriyle DOĞRULA — özellikle M2/M2b):**
`M1`=`--distractors 3 --max-chunk-chars 900` · `M4`=`--with-source` · `M2`=`--data data/eval/trap.jsonl --with-source` · `M2b`=`--distractors 3 --no-gold` · `M3`=`--empty-context` · `M5`=(kaynak-flag yok, kör). Sabit: seed 3407, etiket `bench_{mod}_{model}`.

**🚦 SONRA = JUDGE (PARA-KAPISI, ~<$1, ONAY GEREKİR — sormadan koşma):**
- grounding (M1/M4): `groundedness.py --details ... --label ... --mode data`
- abstention (M2/M2b/M3 + trap_xkanun/trap_ood): `score_abstention.py --details ... --label ...`
- M5: `score_correctness.py --details ... --ref-mode gold --eval-set ...`
- Hepsi gpt-4o-mini (`OPENAI_API_KEY` env, asla echo etme).

**KAPI (Q1):** M2≥0.704 + M1 A1≥0.904 + tavan koru (M4/M2b/M3/register) + M5 base-altı. Kanon kıyas sütunları (base/v2b/v2c/Mecellem) `outputs/eval/*_summary.json`'da CACHE'te. 2 SMK trap (ov~0.55) kazara-cevaplama spot-check. Kapı sonrası → ADR-0015 + research_log entry.

**Resume nasıl:** yeni oturumda generation subagent'ı aynı görevle yeniden başlat (üretilmiş dosyaları atlar, yarım m1_v3ck28'i ezer) VEYA kalan ~8 koşuyu elle sıra ile. Judge'a GEÇMEDEN kullanıcı onayı al.
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
