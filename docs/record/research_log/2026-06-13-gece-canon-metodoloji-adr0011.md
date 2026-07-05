### 2026-06-13 (gece) — ⭐ CANON eval metodolojisi kilitlendi (grill + /deep-research → ADR-0011)
**Tetik:** kullanıcı itirazı — "model çıplak kanunu bilmeli, yoksa neden kanunla FT ettik?" + sabahki KÖR ölçümünün **metrik hatası** (kaynaksız cevabı "kaynağa sadakatsiz" diye cezaladık → faithfulness KÖR'de TANIMSIZ).
**Süreç:** 8 tasarım kararı grill-me ile çözüldü → `/deep-research` (22 kaynak, 8/8 nokta) ile literatüre doğrulatıldı → 4 düzeltme işlendi.

**CANON (ADR-0011):** 4 eksen AYRI (ortalanmaz): **A1** Groundedness (yalnız Oracle), **A2** Correctness (KÖR+Oracle, ref=gerçek madde), **A3** Abstention (TRAP), **A4** Format; **A1∧A2** türetilmiş ikincil. Mod-stratifiye: CORE×KÖR, CORE×Oracle, TRAP×Oracle (paired). Pilot 40/35 (paper 100/75).

**Akademik verdict (deep-research):** 6/8 nokta "olduğu gibi savunulabilir" (ALCE, RAGBench-TRACe, Wallat, RGB, FaithEval, selective-prediction); 4 düzeltme:
1. A1∧A2 manşet→ikincil (alan ayrı raporlar; Trust-Score ortalar=zıt).
2. **A3 çöküşü = ÖZGÜN K3 bulgusu, replikasyon DEĞİL** — yayınlı FT-harm OVER-refusal'dır, bizimki UNDER-refusal (zıt yön); AbstentionBench %24 reasoning-FT için (çürütüldü, direkt destek değil).
3. G1 cross-judge CROSS-FAMILY (Claude/Gemini), gpt-4o değil (Wataoka self-preference familiarity-kaynaklı).
4. bootstrap GA + paired McNemar; OOD unseen-statute dilimi paper öncesi.

**Kod:** `score_correctness.py` (YENİ: A2 + coverage/conditional-acc + bootstrap CI + TRAP gold-join 35/35 test). `bench_scorecard.py` canon'a güncellendi (mod-stratifiye, A1 KÖR'den çıkarıldı). Smoke: derleme OK, CI [0.625,0.875]@n40.
**Sıradaki:** pilot koşu base/v1 (manuel onay sonrası) → analiz → v2 hazırlığı.

