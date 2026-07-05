### 2026-06-13 (gece) — ⭐⭐⭐ CANON PİLOT: base vs v1 → scope kararı (Product A) + v2 yönü
**Kurulum:** CANON eval (ADR-0011), base vs v1, n=40/35, 3 hücre paired, gpt-4o-mini hakem. Rapor: `outputs/BENCHMARK_REPORT.md`. Plan: `docs/V2_PLAN.md`.

| hücre | metrik | base | v1 |
|---|---|---|---|
| CORE-KÖR | A2 doğru (CI95) | 0.225 [.10,.35] | 0.300 [.17,.45] |
| | A2 lenient | **0.850** | 0.675 |
| CORE-Oracle | A1 faith | 0.977 | 0.960 |
| | A2 doğru | **0.925** | 0.800 |
| | **A1∧A2 🟢** | **0.875** | 0.775 |
| | A4 paren | 0.025 | **0.975** |
| TRAP | **A3 Rej\*** | **0.741** | **0.000** |
| | fabrication | 0.259 | 1.000 |
| | TRAP-A2 (diag) | 0.114 | 0.114 |

**Bulgular:**
1. **Scope A/B → PRODUCT A.** CORE-KÖR A2: v1≈base (0.30 vs 0.225, CI çakışık, lenient base lehine) → **FT kanun gömmüyor.** İkisi de kör hukukta kötü (~%25). Reframe (ADR-0010) DOĞRULANDI.
2. **v1 oracle'da bile base'den KÖTÜ.** A1∧A2 grounded-acc 0.775 < **0.875**. SFT yardım etmedi, **aktif zarar verdi** — tek kazanım kozmetik format.
3. **Abstention çöküşü teyit:** A3 0.741→0.000. **TRAP-A2 ikisi de 0.114 ama farklı sebep:** base çekiniyor (cevaplamıyor), v1 cevaplıyor ama **%88 yanlış = halüsinasyon** (doğru-ezber DEĞİL) → v2 hedge dozajı BÜYÜK.
4. **Kök ders (K3):** SFT bilgi değil ÜSLUP öğretir; base = güçlü okuyucu+kalibre model; v1 onun gücünü dar format için takas etti. base'in değeri genel yetenek (okuma+kalibrasyon).

**Karar (ADR-0012 dolduruldu):** scope = **Product A** (doğruluk RAG'dan). v2 = base'in gücünü KORU, yalnız 3 dar iş (abstention-koru + uzman-register + format). İki aday: **v2a=base+prompt (SFT yok)** vs **v2b=hafif-SFT**; önce v2a (ucuz, yan-hasarsız) dene. Başarı kapısı: A3≥0.741 + A1∧A2≥0.875 + A4 korunsun. **Detay: `docs/V2_PLAN.md`.**

