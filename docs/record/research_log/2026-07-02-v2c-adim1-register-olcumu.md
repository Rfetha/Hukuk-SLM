## v2c icra — ADIM 1: C1-v2b register ölçümü (2026-07-02)
Otorite: [`v2c/roadmap.md`](../v2c/roadmap.md) §5 (tek numaralı akış) · §7·AÇ-KOŞ-1 · G4.

**Ne:** `score_register.py` (v1 leksik-proxy, hakemsiz, deterministik) v2b'nin M1 detail'i üstünde koşuldu. Roadmap'in "register ekseni script VAR, koşulmadı" boşluğunun (G4) v2b yarısını kapatır — base/v1 yarısı ADIM 2'de (C3 rescore detail'i üretince, §5 ⛓️).

**Sonuç (kaynak: `outputs/eval/reg_m1_v2b_summary.json` + `reg_m1_v2b.jsonl`):**
| Model | n | register_mean | expert_frac(≥0.6) | citizen_frac(≤0.4) |
|---|---|---|---|---|
| **v2b (M1)** | 40 | **1.000** | **1.000** | **0.000** |

- **Dağılım teyidi:** 40/40 satır `expert_hits≥1` (min 1 · medyan 3 · max 5), `citizen_hits=0` istisnasız → mean=1.0 gerçek (nötr 0.5 masking değil; e+c=0 olan satır yok, hepsi expert-sinyalli).
- **Lesson:** v2b proxy-düzeyinde **tam uzman-register** — uzman-birincil reframe (ADR-0010) çıktıya yansımış; vatandaş-basit sızıntı yok. Bu bir **regresyon alt-sınırı** (§7·AÇ-KOŞ-1): v2c'nin `expert_frac` düşürmemesi / `citizen_frac` artırmaması gerekir, üstünlük değil (uzman-register zaten v2 tasarımı, §6 dışı).
- **Uyarı (yorumu sınırla):** proxy leksik — "uzman kelime var mı" ölçer, "doğru/anlaşılır mı" DEĞİL. Kanonik metrik = LLM-judge rubriği (ADR-0013, hâlâ TODO). base/v1 karşılaştırması olmadan mutlak 1.0 tek başına anlam taşımaz → ADIM 2 base/v1 üçlü tablosu şart.

---

