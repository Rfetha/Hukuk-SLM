# HakHukuk Eval Suite — CANON Scorecard

> LLM-judge (gpt-4o-mini), model-vs-model SIRALAMA (mutlak değil). Eksenler AYRI (ortalanmaz). Setler: CORE-HARD (karmaşıklık-seçili) + TRAP (topic-near hard-negative). Mod: KÖR (ezberden) / Oracle (gerçek RAG değil, doğru/tuzak madde elle verili — gerçek RAG'ın iyimser tavanı).

## Hücre 1 — CORE × KÖR · *kanunu ezberden biliyor mu* (A1 burada TANIMSIZ: kaynak yok)
**CORE-KÖR**

| model | A2 correct↑ | CI95 | A2 lenient | abstain | A4 cite | A4 paren | med_len |
|---|---|---|---|---|---|---|---|
| **base** | 0.225 | [0.10,0.35] | 0.850 | 0.000 | 0.650 | 0.050 | 812 |
| **v1** | 0.300 | [0.17,0.45] | 0.675 | 0.000 | 1.000 | 1.000 | 117 |

## Hücre 2 — CORE × Oracle · *madde verilince doğru+dayanaklı mı*
**CORE-Oracle**

| model | A1 faith | A1 hall | A1 wrong_ref | A2 correct↑ | CI95 | A1∧A2🟢 | A4 paren |
|---|---|---|---|---|---|---|---|
| **base** | 0.977 | 0.023 | 0.000 | 0.925 | [0.85,1.00] | 0.875 (n=40) | 0.025 |
| **v1** | 0.960 | 0.041 | 0.026 | 0.800 | [0.68,0.93] | 0.775 (n=40) | 0.975 |
> A1∧A2 = TÜRETİLMİŞ İKİNCİL diagnostik (per-axis sayılar birincil). grounded=hallucination==0 ∧ correct=CORRECT.

## Hücre 3 — TRAP × Oracle · ⭐ *yanlış madde verilince reddedebiliyor mu* (asıl ayırt edici)
**TRAP-Oracle**

| model | A3 Rej*↑ | A3 Rej_exact↑ | A3 fab↓ | param_leak | valid | TRAP-A2 correct(diag) |
|---|---|---|---|---|---|---|
| **base** | 0.741 | 0.704 | 0.259 | 0.296 | 27 | 0.114 |
| **v1** | 0.000 | 0.000 | 1.000 | 1.000 | 27 | 0.114 |
> Rej*↑=uydurmadan 'kaynak yetersiz' diyebilme. TRAP-A2 = abstain etmeyenlerin gerçek-gold'a göre doğruluğu (diagnostik: fabrication 'yanlış-uydurma' mı 'doğru-ezber ama dayanaksız' mı).

## G1 — Hakem geçerliliği (paper öncesi)
> ⚠️ Cross-judge **CROSS-FAMILY** olmalı (Claude/Gemini) — gpt-4o aynı-aile, self-preference'ı gidermez (Wataoka). Hem raw-agreement hem Cohen's κ raporla (κ≥0.6 bar). + ~30 yazar spot-check.

## Limitations / Future (akademik dürüstlük — deep-research 2026-06-13 ile teyitli)
- **A3 abstention çöküşü = BİZİM ÖZGÜN K3 negatif bulgumuz**, replikasyon DEĞİL. Yayınlı FT-harm lit (Know-Your-Limits/CRaFT/R-Tuning) abstention-ODAKLI tuning'den OVER-refusal belgeler; bizimki generic-SFT'den UNDER-refusal (zıt yön) → özgün sun.
- **A1∧A2 conjunction'ın temiz kanonik öncülü YOK** (Trust-Score ortalar=zıt felsefe) → ikincil tut, hallucination==0 eşiğini açıkça gerekçelendir.
- **n=40/35 PİLOT** → underpowered; bootstrap GA (corr'da var) + **paired McNemar** (blind-vs-oracle / base-vs-v1) raporla; **paper-cetveli n=100/75**.
- **Kontaminasyon kontrolü:** sorular sentetik-üretici + eğitim kanunlarıyla in-distribution (held-out). Memorization vs generalization ayrımı için **OOD unseen-statute dilimi** (+insan-yazımı dilim) paper öncesi şart.
- **A1/A2 operasyonel tanımları açık yazılmalı** (ALCE/RAGBench/Wallat çizgiyi farklı çeker).
- **G3 Completeness / G4 span-level — future.** Oracle = gerçek RAG'ın iyimser tavanı (retriever-hatasız).
- LLM-judge mutlak değil + 'LLM-judge=human' ABARTILMAMALI (deep-research'te o iddia çürütüldü) → **model-vs-model SIRALAMA.**
