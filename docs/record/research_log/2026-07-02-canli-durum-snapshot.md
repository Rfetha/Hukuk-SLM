## 🔴 CANLI DURUM SNAPSHOT (2026-07-02, compact sigortası) — İKİ İŞ KOŞUYOR
> Bu blok, context-compaction'a karşı taze-agent devir notudur. Branch = **`v2c`**.

**1) v2c EĞİTİMİ — Modal A100, KOŞUYOR (ADIM 6c):**
- app=`ap-kKczVUwN4cMj6fodVkaLvK` · FunctionCall=`fc-01KWHHWR578WWCXQJ6Q0D37PZ3` · run=`v2c` · 1 epoch = **1085 step** (~15s/it, ~4-4.5h) · smoke green (step-10 loss=1.347).
- İzle: `modal app logs ap-kKczVUwN4cMj6fodVkaLvK` · durum: `modal app list`.
- Bitince: `modal volume get hukuk-outputs /v2c ./outputs/v2c` → adapter=`outputs/v2c`.

**2) C3 BASELINE — yerel RTX 5070, KOŞUYOR (ADIM 2):**
- nohup driver=`/tmp/claude-1000/-home-ersoy-code-Hukuk-SLM/5ce8b25c-e4fb-447b-aa40-af24802b11b2/scratchpad/run_c3_base_v1.sh` · log=aynı dizin `c3_run.log` · PID 57548.
- base'i 6 modda (M1/M4/M2b bitti · M2/M3/M5 sırada) sonra v1. Çıktı: `outputs/eval/bench_m{1..5}_{base,v1}_detail.jsonl` + skorlar.
- İzle: `grep -E '=== .* bitti ===' c3_run.log; tail -1 c3_run.log`.

**BİTİNCE YAPILACAK:**
- **C3 bitince → ADIM 2 tamamla:** her mod için `python scripts/rescore_answered.py --gnd gnd_bench_mX_{model}.jsonl --bench bench_mX_{model}_detail.jsonl --label mX_{model}` (cevaplanan-only, ADR-0011) · register: `score_register.py --details bench_m1_{base,v1}_detail.jsonl` · **C4 Mecellem baseline** (Tablo 1, `newmindai/Mecellem-Qwen3-4B-TR`, completion-style, yerel) · base over-refusal spot-check → research_log ADIM 2 tam tablo + roadmap §5 madde 2 ✅.
- **v2c eğitimi bitince → ADIM 6d eval:** adapter çek → 6-mod eval (v2b'nin komutları: `gen_eval_grounded.py` M1 `--distractors 4 --max-chunk-chars 900 --n 40`, M2 `--data trap.jsonl --with-source --n 35`, M2b `--distractors 4 --no-gold`, M3 `--empty-context`, M4 `--with-source`, M5 blind; skorla groundedness/score_abstention/score_correctness) → **§6 üstünlük** (M2≥0.90, M1≥0.94, A4≥0.95) + **§1 regresyon kapısı** (M1 0.904·M4 0.975·M2b 0.96·M3 1.0·M5≈0.175·A4 0.925 DÜŞMESİN). Kapı geçmezse v2c reddedilir.

**BİTEN ADIMLAR (v2c branch, commit'li):** ADIM 1 (register v2b=1.0) · ADIM 3 C2 (bias yok, sıfır-kod) · ADIM 4 B1 (GOLD-scrub 1157→0 + teacher yasağı; yedek `data/processed/sft_v2b/answers.jsonl.pre_scrub.bak`) · ADIM 5 B2/B3 (replay dokunulmadı; core_hard #28/#29 belgelendi, kaldırma n=120'ye ertelendi) · ADIM 6a yeni-kod (`build_sft_v2b.py` cf+trap slice + `_gate` cf-ref + kelime-sayı CF; `gen_v2b_answers.py` ABSTAIN_TRAP_TEMPLATES+build_cf_answer+`--reuse-answers`) · ADIM 6b veri (`data/processed/sft_v2c/` train 17353/val 963/test 963, API=$0).

**ELMAYLA-ELMA ERKEN SAYILAR (biten base modları vs v2b, aynı kural):** M1 base 0.886@cov%47.5 vs v2b 0.92@%72.5 · M4 base 0.971 vs 0.975 · M2b base 1.0 (aşırı-ret artefaktı) vs 0.96. → base bilgide eşit, **davranışta v2b üstün**; base her yerde over-refuse. base M2(yanlış-kaynak) bekleniyor (eski 0.786 = v2c'nin geçmesi gereken).

**pack reçetesi (tekrar üretmek gerekirse):** `build_sft_v2b.py pack --p 0.8 --distractors 4 --seed 3407 --cf-frac 0.25 --trap-frac 0.40 --out-dir data/processed/sft_v2c` → `gen_v2b_answers.py --packed .../packed.jsonl --out .../answers.jsonl --reuse-answers data/processed/sft_v2b/answers.jsonl --workers 1` → `build_sft_v2b.py assemble --answers .../answers.jsonl --out-dir data/processed/sft_v2c --replay data/processed/replay_tr.jsonl --replay-frac 0.03 --max-chunk-chars 900`.

---

