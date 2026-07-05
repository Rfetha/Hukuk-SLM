### 2026-06-13 (akşam) — ⭐⭐ BENCHMARK RUN: base/v0/v1 × CORE-HARD+TRAP (madde-verili/oracle, n=40/35)
**Kurulum:** literatüre-dayalı setler (`data/eval/{core_hard,trap}.jsonl`), **madde-verili/oracle** modu (`--with-source`; doğru/tuzak madde ELLE prompt'a konur — gerçek RAG değil), gpt-4o-mini hakem. CORE-HARD = doğru madde verilir, doğruluk ölç (A1+A4). TRAP = konu-yakını YANLIŞ madde verilir, abstention ölç (A3). Skorlar: `outputs/eval/{gnd,abst,fmt}_bench_*_summary.json`, birleşik `outputs/BENCHMARK_REPORT.md`.

| eksen | metrik | base | v0 | v1 |
|---|---|---|---|---|
| **A1** (CORE) | faithfulness | **0.976** | 0.920 | 0.960 |
| | hallucination | 0.024 | 0.080 | 0.041 |
| | wrong_ref | 0.000 | 0.000 | 0.026 |
| **A3** (TRAP) ⭐ | **Rej\*(LLM)↑** | **0.786** | **0.000** | **0.000** |
| | Rej(exact)↑ | 0.679 | 0.000 | 0.000 |
| | fabrication↓ | 0.214 | 1.000 | 1.000 |
| | param_leak | 0.286 | 0.769 | **1.000** |
| | valid_traps | 28/35 | 26/35 | 26/35 |
| **A4** (CORE) | cite_present | 0.925 | 0.125 | 0.975 |
| | paren_cite | 0.025 | 0.000 | **0.975** |
| | med_len (kar) | 308 | 152 | 152 |

**Bulgular:**
1. **⭐ SFT abstention'ı YOK ETTİ — felaket niteliğinde, öngörüden çok sert.** AbstentionBench "~%24 bozar" diyordu; biz **0.786 → 0.000 tam çöküş** ölçtük (hem v0 hem v1, tuzakların %100'ünde uydurdu). **v1 param_leak=1.000** = verilen yanlış kaynağı tamamen yok sayıp ezberden cevapladı. → güçlü, yayınlanabilir **K3 negatif bulgu**: temiz grounded SFT (v1) bile abstention'ı sıfırlıyor.
2. **v1'in SFT'den TEK kazanımı = atıf FORMATI.** `paren_cite` 0.025→**0.975** ("(KANUN, Madde X)" kalıbı). Ama format kozmetik; A1 faithfulness'ta base'i GEÇMEDİ (0.960<0.976), wrong_ref'i SIFIRDAN 0.026'ya çıkardı. **Takas berbat:** kozmetik format ↔ asıl-eksen (A3) sıfırlandı.
3. **v0 ayrıca bozuk:** cite_present 0.125 (neredeyse hiç atıf), kısa (152 kar) → forum-register çöküşü A4'te de net. v0 < v1 < base.
4. **A1 madde-verili tavanı teyit:** üçü de 0.92–0.98 (ayırmıyor). K1 ablasyonda "+SFT" satırı faithfulness'la boş çıkar — SFT etkisini A3(yıkıcı)+A4(format)'ta göster. (Not: bu tavan oracle; gerçek RAG retriever-hatasıyla daha düşük olur.)
5. **Payda notu:** `valid_traps`<35 çünkü hakem "yanlış kaynak aslında cevaplıyor" derse tuzak elenir (`source_answers`→geçersiz). base 7, v0/v1 9 elendi; fark küçük, 0.786-vs-0.000 başlığını değiştirmez.

**Karar pekişti:** v2 **mutlaka ciddi hedge/abstention dilimi (%15-25) + madde-verili modda eğitim** içermeli — çöküş "0.000" olduğu için ufak SFT bile siliyor. **v2 başarı kapısı = A3 rejection_rate ≥ base (0.786)** (faithfulness DEĞİL, tavan). Format kazanımı (A4) v1'den miras ama abstention bedeline değmez → tek başına satılamaz.
**Sıradaki:** G1 cross-judge (gpt-4o alt-küme) bu A3 çöküşünü teyit etmeli (κ); sonra v2 veri tasarımı.

