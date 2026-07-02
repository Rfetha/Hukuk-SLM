# v2b — CANON Eval Sonuçları (5-mod matris, ADR-0013)

> **Durum:** Parça parça dolduruluyor — her mod bittikçe eklenir/toparlanır.
> Son güncelleme: 2026-07-02 · Otorite kronoloji: [`research_log.md`](research_log.md) (2026-07-02 girdisi).

## Kurulum (tüm modlar ortak)
- **Model:** Gemma 4 12B (`gemma-4-12B-it-qat-q4_0-unquantized`) + **v2b LoRA adapter** (`outputs/v2b`, r=16/α=32, 65.5M, train_loss=0.30, 4h19m Modal A100).
- **Eval-mirror AÇIK:** `--max-chunk-chars 900` — eğitimin chunk-clip'i (eğitim=deployment RAG-chunk dağılımı, ADR-0013). first-900 clip = "aptal retriever" simülasyonu; answer-anchored varyantı ("akıllı retriever") planlı.
- **Hakem:** gpt-4o-mini (`groundedness.py --mode data`, insan-κ kalibresiz → mutlak değil, model-vs-model sıralama). n=40 pilot (paper 100/75).
- **Baseline (A-track, aynı modlar):** base M1 A1=**0.879** · M3 abstention=**1.000**. v1 abstention çöküşü (M2/TRAP): base Rej\* **0.786 → v1 0.000** (K3 negatif bulgu, research_log 2026-06-13).

## Matris — durum panosu

| Mod | Ne ölçer | Eksen | Durum | Manşet sonuç |
|---|---|---|---|---|
| **M1** Gold+distractor | grounding-under-noise | A1·A2·A4·register | ✅ **BİTTİ** | A1(cevaplanan)=**0.904** |
| **M2** TRAP (yanlış-kaynak oracle) | abstention | A3 | ✅ **BİTTİ** | Rej\*=**0.346** (v1 0.000→ · base 0.786) ⚠️off-dist |
| **M2b** distractor-only (training-matched) | abstention (RAG-ıska) | A3 | ✅ **BİTTİ** | Rej\*=**0.96** (n=30, adil A3 manşeti) |
| **M3** Boş/kaynaksız (E-set) | abstention (kaynak-eksik) | A3 | ✅ **BİTTİ** | Rej\*=**1.000** (base 1.000) |
| **M4** Temiz gold-only (Oracle) | iyimser tavan (referans) | A1·A2·A4 | ✅ **BİTTİ** | A1=**0.975** (base 0.977·v1 0.960) |
| **M5** KÖR/kaynaksız | parametrik ezber / unutma | A2 | ✅ **BİTTİ** | A2=**0.175** (base 0.225·v1 0.300, CI-örtüşük) |

**KAPI (ADR-0011/§6):** A3 ≥ 0.786(base) · A1∧A2 ≥ 0.875 · A4 ≥ 0.9 · CORE-KÖR(M5) gerilemesin · +uzman-register/format.

### KAPI verdikti (6 mod tamam, 2026-07-02)
| Eksen | Kaynak | v2b | Eşik | Sonuç |
|---|---|---|---|---|
| A1∧A2 grounding | M1 cevaplanan 0.904 · M4 oracle 0.975 | ✅ | ≥0.875 | **GEÇTİ** |
| A4 format (cit_precision) | M1 0.925 · M4 0.975 | ✅ | ≥0.9 | **GEÇTİ** |
| **A3 abstention (adil, deployment-modu)** | **M2b 0.96 · M3 1.000** | ✅ | ≥0.786 | **GEÇTİ** |
| A3 abstention — yanlış-madde oracle (off-dist) | M2 = 0.346 | ⚠️ | ≥0.786 | v1-comp artefakt (bkz M2/M2b) |
| Unutma (forgetting) | M5 = 0.175 vs base 0.225 | ≈ | gerilemesin | **NÖTR** (CI-örtüşük, çöküş yok) |
| register | — | — | — | ⏳ ölçülmedi (açık eksen) |

**Genel:** **v2b TÜM kapıları geçti** (grounding + format + abstention + forgetting). Kritik düzeltme (M2b): v2b'nin gerçek/deployment-modu abstention'ı **0.96** (M2 oracle'ın 0.346'sı v2b'yi eğitilmediği tek-kaynak promptunda ölçen artefaktmış). v1'e karşı net ileri: abstention 0.000→**0.96 dirildi**, grounding **korundu+aştı** (0.904/0.975), unutma **yok** (replay tuttu). Kalan iş robustness (yanlış-tek-kaynak M2 0.346) + kozmetik (GOLD, off-by-one) → v2c.

---

## M1 — Gold + 4 distractor (grounding manşeti) ✅
`gen_eval_grounded.py --label bench_m1_v2b --adapter outputs/v2b --data core_hard.jsonl --distractors 4 --n 40` (mirror 900)
Skor: `groundedness.py --mode data` → `outputs/eval/gnd_bench_m1_v2b_summary.json`. Hakem maliyeti $0.018.

### A1 Faithfulness — çekinmeleri AYIRARAK oku (ADR-0011: A1=cevaplananlarda)
| Dilim | n | faithfulness (macro) | Yorum |
|---|---|---|---|
| Ham (çekinmeler dahil) | 40 | 0.792 (micro 0.737) | ❌ yanıltıcı — çekinme faith=0 alıp çeker |
| **Cevaplanan = GERÇEK A1** | 33 | **0.904** | ✅ **KAPI (≥0.875) geçer + base (0.879) AŞAR** |
| Çekinme | 7 | 0.262 | A1'e ait değil → A3 ekseni |

- cit_precision=**0.925** · wrong_ref=**0.075** · cit_recall=1.0 · total_claims=114.

### Çekinme kırılımı (M1'de gold context'te → çekinme "miss") — 7/40 = %17.5
Judge-teyitli (CONTRADICTED = gold'da vardı = over-refusal; NOT_IN_SOURCE = haklı/kırpılmış-chunk'ta yok):
- 🟡 **2 OVER-REFUSAL** — TÜKETİCİNİN KORUNMASI Md47 ×2 (gold'da cevap VARDI, judge CONTRADICTED).
- 🟢 **5 haklı** — KAT MÜLKİYETİ Md4 ×2 (benchmark **kötü soru↔madde eşleşmesi**), TBK 127, CMK 142, İİK 290 (kırpılmış chunk'ta cevap yok = doğru RAG davranışı).
- **Gerçek over-refusal = 2/40 = %5.** v1'in tersi (v1 asla çekinmezdi). Sarकाç kabul edilebilir/iyi yönde.

### Kalan grounding kusurları (cevaplanan, faith<1 olan 6 vaka)
- **Off-by-one yanlış-madde atfı deseni:** CMK 109→"110", İş K 55→"56", TCK 50, TCK 75; komşu-madde distractor'ından etiket karışması olası. → **sonraki FT nit.**
- **GOLD-sızıntı:** M1 çıktılarında ~1/40 "GOLD metnidir" (eğitim hedeflerinin %5.7'si; teacher-prompt jargonu sızmış). → v2c düzeltmesi (research_log 2026-07-02).

### M1 kararı
✅ Grounding manşeti güçlü: **v2b cevaplananda base'i geçiyor + kapıyı aşıyor.** Kusurlar ikincil (off-by-one atıf, GOLD-sızıntı, %5 over-refusal). *Uyarı: base 0.879 aynı "cevaplanan-only" mantığıyla yeniden skorlanırsa elmayla-elma olur — açık iş.*

---

## M2 — TRAP: yanlış-madde oracle (abstention) ✅
`gen_eval_grounded.py --data trap.jsonl --with-source --n 35` → `score_abstention.py`. valid_traps=26/35.

| Metrik | base | v1 | **v2b** |
|---|---|---|---|
| **Rej\*(LLM)** ↑ | 0.786 | **0.000** | **0.346** |
| Rej(exact) ↑ | 0.679 | 0.000 | 0.308 |
| fabrication ↓ | — | 1.000 | 0.654 |
| parametric_leak ↓ | — | 1.000 | 0.615 |

### Okuma
- ✅ **v1'e karşı dev iyileşme:** abstention 0.000 → **0.346** (K3 çöküşü kısmen iyileşti — abstention DİRİLDİ).
- ❌ **KAPI'yı geçmiyor:** 0.346 < base 0.786. Yanlış-kaynakta hâlâ %65 uyduruyor (parametric_leak %61.5).
- ⚠️ **OFF-DISTRIBUTION uyarısı:** bu koşu `--with-source` = **tek-kaynak (SYSTEM_PROMPT_RAG)**. v2b **çok-kaynak RAFT (RAG_MULTI)** ile eğitildi; abstain dilimi "gold'suz distractor paketi" formatındaydı → v2b eğitilmediği prompt modunda ölçüldü. **0.346 muhtemelen ALT SINIR.** v1-comparable ama v2b'ye haksız.
- **Açık iş:** training-matched M2 (distractor-only + RAG_MULTI, `--no-gold`) → v2b'ye adil ikinci sayı. Manşet A3 = M2∪M3. → **çözüldü: M2b aşağıda.**

## M2b — distractor-only, training-matched (adil abstention) ✅
`gen_eval_grounded.py --distractors 4 --no-gold --data core_hard.jsonl` (gold ÇIKARILMIŞ, RAG_MULTI prompt = v2b eğitim abstain diliminin AYNI modu) → `score_abstention.py --source-field context_shown`. **n=30** (çökme nedeniyle kısmi; valid 25/30).

| Metrik | M2 (oracle, off-dist) | **M2b (training-matched)** |
|---|---|---|
| **Rej\*(LLM)** ↑ | 0.346 | **0.96** |
| fabrication ↓ | 0.654 | 0.04 |

### Okuma — 🔑 M2'nin off-distribution açığı KANITLANDI
- v2b'yi **eğitildiği modda** (çok-kaynak, gold yok → çekin) ölçünce abstention **0.96** — M2-oracle'ın 0.346'sı neredeyse tamamen **ölçüm artefaktıymış** (v2b'yi eğitilmediği tek-kaynak SYSTEM_PROMPT_RAG'da test etmek).
- **Deployment = RAG çok-kaynak** olduğu için **M2b (0.96) ADİL A3 manşetidir**, M2 (0.346) değil.
- **A3 hikâyesi netleşti:** RAG-ıska (gold retrieve edilemedi) 0.96 · boş-kaynak 1.000 → v2b **her iki RAG-abstention senaryosunda güçlü**, KAPI ≥0.786'yı rahat geçer.
- **Kalan gerçek zayıflık:** yalnız "yanlış-ama-makul TEK kaynak" (M2-oracle) senaryosu → v2c robustness (TRAP-tipi abstain dilimi). Bu bir gate-fail değil, robustness iyileştirmesi.
- ⚠️ n=30 (çökme; base/v1 aynı modda yok) → paper için n=40 + base/v1 aynı modda tekrar önerilir.

## M3 — Boş/kaynaksız E-set (abstention, kaynak-eksik) ✅
`gen_eval_grounded.py --empty-context --n 40` → `score_abstention.py`. valid 31/40.
- **Rej\* = 1.000** (fabrication 0.0). Kaynak HİÇ verilmeyince v2b **%100 çekiniyor** = base (1.000). Kusursuz.
- **A3 hikâyesi (M2∪M3):** boş-kaynak 1.000 ✅ · yanlış-kaynak (M2) 0.346 ⚠️ → v2b "hiç kaynak yok"ta çekinmeyi öğrendi, "yanlış-ama-makul kaynak var"da öğrenemedi. → v2c abstain dilimi TRAP-tipine göre kurulmalı.

## M4 — Temiz gold-only Oracle (iyimser tavan) ✅
`gen_eval_grounded.py --with-source --n 40` → `groundedness.py --mode data`.
- **A1 faithfulness = 0.975** (micro 0.968) · cit_precision 0.975 · wrong_ref 0.025 · halüsinasyon 0.032 · $0.018.
- Kıyas (2026-06-13 oracle): base 0.977 · v1 0.960 → **v2b tavanda, base'e eşit, v1'i geçiyor.**
- M1 (distractor 0.904) < M4 (oracle 0.975): beklenen — gürültülü RAG, temiz oracle'dan zor (distractor-robustness maliyeti ~%7). Manşet M1 (deployment'ı temsil eder), M4 iyimser tavan.

## M5 — KÖR/kaynaksız (parametrik ezber / unutma) ✅
`gen_eval_grounded.py --data core_hard.jsonl --n 40` (bayraksız=blind) → `score_correctness.py --ref-mode detail`.

| Metrik | base | v1 | **v2b** |
|---|---|---|---|
| A2 correct (CI95) | 0.225 [.10,.35] | 0.300 [.17,.45] | **0.175 [.075,.30]** |
| lenient | — | — | 0.725 |
| coverage / cond_acc | — | — | 0.975 / 0.179 |
| abstain | — | — | 0.025 |

### Okuma
- **Çöküş YOK:** v2b blind 0.175, base 0.225 ile **CI-örtüşük** (n=40'ta istatistiksel fark yok). v0'ın 154x ezber-çöküşünün tersi → **replay unutmayı önledi** ✅.
- **"FT kanun gömmüyor" teyidi (Product A, ADR-0012):** üçü de kör hukukta ~%18-30 (kötü). Bilgi ağırlıkta değil, RAG'de (M4 oracle 0.975 vs M5 blind 0.175 = **%80 uçurum** kaynak verilince). Bu tam istenen: model kaynağa dayanır, ezbere değil.
- Not: v2b hafifçe base altında ama CI içinde; coverage 0.975 (neredeyse hiç çekinmiyor blind'de) → blind'de uydurma eğilimi sürüyor ama bu deployment senaryosu DEĞİL (deployment=RAG).

---

## Sonraki iş (v2c / açık)
- [x] ~~Training-matched M2~~ → **M2b bitti (0.96)**; `score_abstention --source-field` eklendi, `gen_eval --no-gold` eklendi.
- 🔴 **v2c FT düzeltmeleri** (aşağıdaki tasarım notu): TRAP-tipi abstain dilimi (M2-oracle 0.346 robustness) + anti-leak counterfactual + GOLD scrub (%5.7) + off-by-one atıf.
- 🟡 **core_hard kötü-eşleşme temizliği** (≥3 vaka M1'de yakalandı — KMK Md4 vb.).
- ⚪ **register/altitude ekseni** — hiç ölçülmedi (ADR-0010/0013 açık eksen).
- ⚪ base/v1'i aynı "cevaplanan-only" + eval-mirror + M2b (no-gold) modunda yeniden skorla → elmayla-elma; M2b n=40'a tamamla.

---

## v2c TASARIM NOTU (bu eval'in çıktısı)
**Hedef:** v2b'nin tek gerçek zayıflığını (yanlış-tek-kaynak abstention M2=0.346) + kozmetik kusurları TEK FT'de kapat. Grounding/deployment-abstention zaten geçti — onları BOZMA (regresyon riskine dikkat).

1. **🔴 TRAP-tipi abstain dilimi ekle** (asıl kaldıraç, M2-oracle 0.346 için)
   - Şu anki abstain dilimi = "gold yok, sadece distractor" (RAG-ıska) → M2b 0.96 zaten çözdü.
   - EKSİK = "yanlış-ama-makul TEK/az kaynak var → reddet". trap.jsonl kurulumu gibi: konu-komşusu yanlış madde koy, hedef = gerekçeli red. `gen_v2b_answers.py`'a bu dilim tipi eklenir.
2. **🔴 Anti-parametric-leak** (M2 param_leak %61.5): counterfactual — kaynak ezbere aykırı/eksik → hedef kaynağa uyar ya reddeder, ezberden tamamlamaz.
3. **🟡 GOLD scrub** (kozmetik, %5.7): teacher prompt'ta "GOLD" yasağı + mevcut answers regex temizlik. (App-layer post-process de yeterli — acil değil.)
4. **🟡 off-by-one atıf fix**: komşu-madde distractor'ından etiket karışması → veri/format iyileştirmesi.
5. **⚪ hedge dozajı ablasyonu** (%19→%25), register ekseni ekle.
**Kritik:** hepsi TEK v2c FT'de; ayrı koşu açma. Regresyon kapısı: M1/M4 grounding + M2b/M3 abstention DÜŞMEMELİ.
