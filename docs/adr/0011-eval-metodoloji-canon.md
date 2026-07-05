# ADR 0011 — CANON eval metodolojisi (4 eksen, mod-stratifiye, literatür-doğrulamalı)

- **Durum:** Yürürlükte (2026-06-13)
- Karar 2026-06-13 akşam grill + /deep-research (22 kaynak, 8/8 nokta doğrulandı) sonrası verildi.

## Bağlam
Pilot benchmark (ADR-0001 groundedness) tek-eksenliydi ve KÖR modda yanlış metrik kullanıyordu
(kaynak verilmemiş cevabı "kaynağa sadakatsiz" diye cezaladı). Kullanıcı "model çıplak kanunu bilmeli
yoksa neden kanunla FT ettik?" itirazıyla **correctness** eksenini ayrı ölçmeyi gündeme getirdi.
8 tasarım kararı grill ile çözüldü, ardından `/deep-research` ile literatüre karşı doğrulandı.

## Karar — CANON HakHukuk Eval Suite

**4 eksen, AYRI raporlanır (ortalanmaz — ALCE / RAGBench-TRACe / Wallat "Correctness is not Faithfulness"):**
- **A1 Groundedness** — verilen kaynağa sadakat (FactScore+ALCE, `groundedness.py`). **Yalnız Oracle**; KÖR'de TANIMSIZ (kaynak yok → sadakat ölçülemez).
- **A2 Correctness** — cevap GERÇEK maddeye göre doğru mu (`score_correctness.py`, YENİ). KÖR+Oracle. CORRECT/PARTIAL/WRONG/ABSTAIN, response-level. **Referans = gerçek madde metni** (sentetik gold değil).
- **A3 Abstention** — TRAP'te uydurmadan red (`score_abstention.py`, RGB negative-rejection). Tavan yok = asıl ayırt edici.
- **A4 Format** — atıf tutarlılığı (`score_format.py`, deterministik). KÖR+Oracle.
- **A1∧A2 Grounded-Accuracy** — TÜRETİLMİŞ İKİNCİL diagnostik (manşet DEĞİL): grounded(hallucination==0) ∧ correct(CORRECT).

**Mod-stratifiye hücreler (her model):** CORE×KÖR→A2,A4 · CORE×Oracle→A1,A2,A1∧A2,A4 · TRAP×Oracle→A3+TRAP-A2(diag). Paired (aynı 40 soru, seed=3407).

**8 karar:** Q1 referans=gerçek madde · Q2 KÖR in-distribution held-out kabul (OOD tetiklenirse) · Q3 response-level 4'lü · Q4 payda=tüm (+coverage/conditional-acc yan) · Q5 grounded=hallucination==0, runs≥3 · Q6 pilot 40/35 (paper 100/75) · Q7 TRAP-A2 diagnostik · Q8 pilot gpt-4o-mini runs=1 (paper runs≥3 + cross-judge).

## /deep-research akademik doğrulama (4 zorunlu düzeltme işlendi)
1. **A1∧A2 "manşet"ten "ikincil diagnostik"e** indirildi (alan ayrı raporlar; Trust-Score ortalar=zıt → atıflanmaz).
2. **A3 abstention çöküşü (0.79→0.00) = ÖZGÜN K3 bulgusu, replikasyon DEĞİL.** Yayınlı FT-harm lit (Know-Your-Limits TACL/CRaFT/R-Tuning) abstention-ODAKLI tuning'den OVER-refusal belgeler; bizimki generic-SFT'den UNDER-refusal (zıt). AbstentionBench "%24" reasoning-FT içindir → direkt destek diye atıflanmaz (verification'da çürütüldü).
3. **G1 cross-judge CROSS-FAMILY** (Claude/Gemini), gpt-4o DEĞİL — self-preference familiarity-kaynaklı, aynı-aile gidermez (Wataoka).
4. **n istatistiği:** bootstrap %95 GA (corr'da eklendi) + paired McNemar (analiz). Paper-cetveli n=100/75.

**Paper öncesi 2 kontrol (nota):** (Point 5) risk-coverage açık raporla; (Point 8) OOD unseen-statute + insan-yazımı dilim.

## Değerlendirilen alternatifler
- **A1 ve A2'yi tek skora ezmek** → REDDEDİLDİ (literatür ayrı raporlar; orthogonality kanıtlı — Wallat).
- **A2 referansı = sentetik gold cevap** → REDDEDİLDİ (doğrulanmamış; "GPT'ye benzedi mi" ölçer). Gerçek madde seçildi.
- **KÖR'de A1 (faithfulness) ölçmek** → REDDEDİLDİ (kaynak yok → tanımsız; sabahki ölçüm hatasıydı).
- **Conditional accuracy (sadece denenende payda)** → REDDEDİLDİ ana metrik olarak (over-refusal'ı gizler); yan-rapor olarak tutuldu.

## Sonuç
- Yeni: `scripts/score_correctness.py` (A2 + coverage + bootstrap CI + gold-join). Güncel: `bench_scorecard.py` (mod-stratifiye, A2+A1∧A2, A1 KÖR'den çıkarıldı, akademik limitations).
- Eksen numarası gap kapandı: A1/A2/A3/A4 sıralı → "eksen-kaydırma" görevi GEREKSİZ.
- Pilot koşu: base/v0/v1 → kalibrasyon + v1'i gömme; sonra base-vs-final aynı cetvelle.

## İlgili
`[[adr-decision-log]]`, ADR-0001 (groundedness), ADR-0002 (kalite kapısı), `docs/record/research_log/README.md` (2026-06-13 akşam canon girdisi), `knowledge/summary_eval_benchmark_literature.md`
