## v2c icra — ADIM 2: base vs v2b tam tablo (C3 rescore + C1 register) — TAMAMLANDI (2026-07-02)
Otorite: `v2c/roadmap.md` §5 madde 2 + Tier C (C1/C3). **Kullanıcı kararı (2026-07-02): v1 ADIM 2'den DÜŞÜRÜLDÜ** — kıyas = **base vs v2b vs Mecellem (rakip)**; v1 bizim eski/terk-edilmiş turumuzdu (rakip değil), fazla iç-baseline. v1 6-mod re-run öldürüldü (base bittikten sonra), GPU boşa koşmadı. Bugünkü yarım `bench_m1_v1_detail.jsonl` (4 satır) çöpe; **Jun-13 tarihsel v1 eval'i (v2b-vs-v1 audit trail) KORUNDU.**

**Elmayla-elma protokolü:** base ve v2b AYNI harness/mod/n/seed(3407)/hakem(gpt-4o-mini) · A1 = cevaplanan-only (ABSTAIN_RE ile çekinme ayrıldı, `rescore_answered.py`, ADR-0011, TÜM modellere tek kural).

| Mod | Eksen | **base** | **v2b** | Yorum |
|---|---|---|---|---|
| **M1** | A1 grounding (cevaplanan, eval-mirror 900) | 0.886 · cov **47.5%** (19/40) | **0.920 · cov 72.5%** (29/40) | v2b İKİ boyutta üstün (faith + coverage) |
| **M4** | A1 grounding (oracle tavan) | 0.983 · cov 95% (38/40) | 0.975 · cov 100% (40/40) | tavan, bilgi ~eşit |
| **M2** | yanlış-kaynak abstention (rejection) | **0.704** | **0.346** ❌ | **v2b KAYBEDİYOR = G1, v2c'nin ana hedefi** |
| **M2b** | RAG-ıska abstention | 1.0 (n=40) | 0.96 (n=30)* | ikisi güçlü |
| **M3** | boş-kaynak abstention | 1.0 | 1.0 | tavan |
| **M5** | KÖR correctness (A2, düşük=iyi) | 0.225 | 0.175 | ikisi RAG'e dayanıyor (anti-hedef ✓) |
| **A4** | cit_precision (M1 cevaplanan) | 1.0 | 0.931 | base az cevaplıyor→trivial 1.0 |
| **register** | expert_frac (leksik-proxy) | 1.0 | 1.0 | ikisi tam-uzman |

\* **M2b n uyumsuzluğu:** v2b eski koşu n=30, base C3'te n=40. Roadmap "M2b n=40'a tamamla" diyor → v2b M2b n=40 regen **ADIM 6d'de** (v2c 6-mod eval'de v2b baseline'ı da n=40 yeniden ölçülecek). rejection 1.0 vs 0.96 headline geçerli.

**🔑 Üç ana bulgu (paper K1/K3 hammaddesi):**
1. **base BÜTÜN over-refuse ediyor** (kalibrasyon değil, körlük): M1'de gold PROMPT'TA VAR ama base 21/40=%52.5 "Verilen kaynaklarda bu konuyu düzenleyen madde bulunmuyor" diyor → **gerçek red, ABSTAIN_RE artefaktı DEĞİL** (spot-check teyitli). Gürültülü/kırpık context'te pes ediyor. v2b %27.5 → kalibre.
2. **base'in M2/M2b/M3 yüksek rejection'ı bu körlüğün YAN ÜRÜNÜ** — yanlış kaynağı da reddediyor çünkü her şeyi reddediyor. Yani base'in M2=0.704'ü "iyi kalibrasyon" değil "kör red" — ama v2c'nin geçmesi gereken sayı yine de bu.
3. **v2b'nin tek gerçek açığı M2=0.346** (param_leak): yanlış-ama-makul kaynak verilince ezberden doğru cevabı üretip **kaynağı reddetmiyor**. Bilgi (M4 oracle ~0.98 ikisi de) eşit → fark tamamen **davranışsal**. → v2c Tier A (A1 TRAP-abstain + A2 counterfactual) tam bunu hedefliyor.

**Kaynak dosyalar:** `outputs/eval/bench_m{1..5}_{base,v2b}_detail.jsonl` · `gnd_bench_m{1,4}_*` · `abst_bench_m{2,2b,3}_*_summary.json` · `corr_bench_m5_*_summary.json` · `reg_m1_*_summary.json`. Rescore aracı: `scripts/rescore_answered.py`.

**Kalan (ADIM 2'yi kapatmadan önce):** C4 = **Mecellem-Qwen3-4B-TR** rakip baseline (completion-style, foundation-kıyası) → paper Tablo 1. Ayrı alt-görev (aşağıda).

---

