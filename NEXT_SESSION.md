# BURADAYIZ — milat 2026-06-13

**Proje:** HakHukuk / Hukuk-SLM — Türkçe hukuk SLM. **Base:** Gemma 4 12B (`gemma-4-12B-it-qat-q4_0-unquantized`) + QLoRA → Q4_0 GGUF.
**Birincil kitle = UZMAN** (hukukçu); vatandaş = app-layer prompt modu (pending ADR-0010).
**Ana metrik = groundedness (A1) + abstention/Rejection-Rate (A3).**

**Önce oku:** `docs/record/research_log.md` (GEÇMİŞ — ne oldu, neden), bu dosya (ŞİMDİ + sıradaki), `TODO.md` (görevler), `CLAUDE.md` (kurallar). Geçmiş bu dosyada DEĞİL — research_log'da.

---

## DURUM (milat)
- ✅ **Benchmark enstrümanı KURULDU + smoke yeşil.** Setler `data/eval/{core_hard,trap}.jsonl` (literatüre dayalı: karmaşıklık-seçili + topic-near hard-negative). Skorlayıcılar: A1 `groundedness.py`, A3 `score_abstention.py` (Rej*+Rej), A4 `score_format.py`, birleştirici `bench_scorecard.py`, hakem-geçerliliği `judge_agreement.py` (G1 cross-judge κ + yazar spotcheck).
- ✅ **v1 SFT = YANLIŞ HEDEF.** RAG modda base≈v1 (faith ~0.97, tavan); v1 vatandaş-register + atıfta hafif geriletti. Veri temiz ama **eğitim hedefi yanlış**. v1 arşiv (ablasyon referansı). Adapter `outputs/v1/`.
- ✅ **Reframe:** birincil kitle = uzman; sadelik app-layer; doğruluk RAG'dan.
- 🔜 **v2 = base'den TAZE QLoRA** (v1 üstüne değil): uzman-register + RAG-modu + %15-25 hedge dilimi. Yönü benchmark RUN'ı çizecek.

## SIRADAKİ İLK İŞ (sırayla)
1. **Benchmark RUN** — base/v0/v1 × {core_hard, trap}, RAG-modu → A1+A3+A4 → scorecard. (Komutlar aşağıda. ~2-2.5h GPU.)
2. **G1 cross-judge** — A1/A3'ü `--judge-model gpt-4o` ile alt-kümede tekrar koş → `judge_agreement.py cross` (κ). + `export`→elle→`author` (~30 yazar etiketi).
3. **META-ANALİZ → v2 yönü.** Literatür öngörüsü (AbstentionBench): SFT abstention'ı bozar → v1, TRAP'te base'den DÜŞÜK olmalı. Bunu test et. Sonuç v2 hedge-dilimi miktarını belirler.
4. **v2 tasarla + Modal'da eğit** → benchmark'tan geçir → base/v1 ile kıyas.
5. (Sonra) Rakip baseline (Mecellem-Qwen3-4B, Llama-3.1-8B) bizim terazide.

## SABİT EKSEN (değişmez — yeni developer buna uyar)
- Ana metrik = **groundedness (A1, RAG'da tavan) + abstention (A3, asıl ayırt edici)**. Faithfulness'ı "geçmeyi" hedef yapma (tavan); ayırt edici = A3.
- Birincil kitle = **uzman**. Eğitim = **Modal A100**. Eval = **lokal** ($0, OpenAI hakem).
- Veri: yalnız güncel TC mevzuatı; Lexpera/Kazancı ASLA.
- **Her bulgu → `docs/record/research_log.md`; her büyük karar → `docs/adr/`.** (Makale sigortası.)
- Python: `source ~/code/global_venv/bin/activate` (aynı komut içinde).

## RUN KOMUTLARI (kopyala-çalıştır)
```bash
cd ~/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && set -a && . ./.env && set +a
# 1) ÜRETİM (base/v0/v1 × core+trap, RAG-modu) — arka plan
nohup bash -c '
  GV=~/code/global_venv/bin/python
  for m in "base:" "v0:--adapter outputs/v0" "v1:--adapter outputs/v1"; do
    name="${m%%:*}"; arg="${m#*:}"
    $GV -u scripts/gen_eval_grounded.py --label "bench_core_$name" --data data/eval/core_hard.jsonl --n 40 --max-new-tokens 256 --with-source $arg
    $GV -u scripts/gen_eval_grounded.py --label "bench_trap_$name" --data data/eval/trap.jsonl     --n 35 --max-new-tokens 256 --with-source $arg
  done; echo "[ÜRETİM BİTTİ]"' > logs_bench.log 2>&1 &
# 2) SKORLA (üretim bitince) — her model için
for m in base v0 v1; do
  python scripts/groundedness.py    --details outputs/eval/bench_core_${m}_detail.jsonl --label bench_core_${m} --mode data
  python scripts/score_abstention.py --details outputs/eval/bench_trap_${m}_detail.jsonl --label bench_trap_${m}
  python scripts/score_format.py     --details outputs/eval/bench_core_${m}_detail.jsonl --label bench_core_${m}
done
# 3) SCORECARD
python scripts/bench_scorecard.py --models base v0 v1   # → outputs/BENCHMARK_REPORT.md
```

---

## 📋 HAND-OFF PROMPTU (yeni terminale/oturuma yapıştır)
> Yeni bir Claude Code oturumu açtığında bunu ilk mesaj olarak ver:

```
HakHukuk projesinde devam ediyoruz. Önce şunları oku: NEXT_SESSION.md (buradayız + sıradaki iş),
docs/record/research_log.md (geçmiş), CLAUDE.md (kurallar — özellikle Documentation discipline).

Durum: benchmark enstrümanı kuruldu (CORE-HARD+TRAP setleri, A1 groundedness / A3 abstention /
A4 format skorlayıcıları, G1 cross-judge), smoke yeşil. v1 SFT'nin yanlış hedef olduğu ölçüldü
(RAG'da base≈v1). Sıradaki iş: NEXT_SESSION'daki RUN KOMUTLARI ile base/v0/v1 benchmark'ını koş,
sonuçları skorla, meta-analiz yap, v2 yönünü çiz. Ana metrik = groundedness + abstention;
birincil kitle = uzman. Python için `source ~/code/global_venv/bin/activate`. Her bulguyu
research_log'a, her kararı ADR'ye yaz. Başlamadan önce GPU boş mu + .env var mı teyit et.
```
