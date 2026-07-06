# v4 RECIPE — answerability-dedektörü (DTA-uyarlı ORPO) · 🔒 KİLİTLİ (grilling tamam 2026-07-06)

> **Durum:** ✅ **KİLİTLİ** (2026-07-06). Deep-research (#34) işlendi + grilling tamamlandı (5 açık-uç çözüldü, 2 karar onaylandı). Sıradaki = ADIM-plan koşumu (para-kapısı onayı).
> **Tez:** [[../research_log/2026-07-06-v4-tasarim-tezi-answerability]] (#33) · **kaldıraç kaynağı:** [[../v3/receteler]] + #34.
> **Neden gerek:** v3 KISMİ (ADR-0015) — M2b regresyon 0.53 + M2 base-altı 0.593 + OOD zayıf 0.483.
> **⭐ Literatür çıpası:** M2b = **Sufficient-Context** "RAG-suppresses-abstention" (Claude 84→52) + **RefusalBench** (frontier multi-doc <%50) = bilinen-genel mod; **DTA (ACL 2025) = belgelenmiş çözüm** (dört-kadran, ✘✘→IDK).

---

## 1. HEDEF (kabul edilmiş)
Her CANON kulvarında **lider VEYA berabere-tavan** (mutlak-1.0 DEĞİL), grounding dörtlüsü regresyonsuz.

**Kulvar-hedef tablosu (SCORECARD gap → v4 hedef):**

| Kulvar | v3 | Şu an lider | v4 hedef | Aksiyon-kaldıracı |
|---|---|---|---|---|
| M4 oracle grounding | 1.000 | **v3** | KORU 1.0 | — (dokunma) |
| M1 grounding (distractor) | 0.881 | ~v3 | KORU ≥0.88 | replay-denge |
| M3 boş-bağlam | 1.000 | tie | KORU 1.0 | — |
| M5 parametrik (↓) | 0.075 | **v3** (en düşük) | KORU ≤0.10 | — (yükseltme YASAK) |
| Register | 0.975 | tie 1.0 | ↑ 1.0 | GOLD-scrub disiplini |
| **M2** yanlış-kaynak | 0.593 | base 0.704 | **≥0.75** (base-üstü) | τ-temiz + yoğunluk |
| **M2b** çok-kaynak miss | 0.529 | base 1.0 | **≥0.90** (base-eş kabul) | RAFT çok-kaynak |
| **xkanun** genelleme | 0.656 | base 0.968 | **≥0.90** | aile-çeşitliliği |
| **ood** genelleme | 0.483 | base 0.889 | **≥0.75** | veri-ölçeği + OOD-negatif |

Öncelik (gap sırası): **M2b (0.47) > ood (0.41) > xkanun (0.31) > M2 (0.11) > register (0.03).**

## 2. KALDIRAÇLAR (deep-research revize; #34)
Çerçeve: "8 takası dengele" değil, **tek answerability-dedektörünü keskinleştir.** DTA çekirdek mekanizma.

- **A. DTA dört-kadran veri-kurgusu (1 NUMARA — düzeltildi).** ⚠️ Eski "ham veri-ölçeği" YANLIŞTI: literatür ham-volümün kurgu-fix'siz getiri vermediğini gösterdi (Sweet-Spot 2502.16825). Doğrusu **yapı > volüm.** Örnekleri iki sınıra göre böl: **parametrik-KB** (bağlamsız N-örnek → model biliyor mu) × **retrieval-KB** (judge: verilen kaynak(lar) cevaplıyor mu). Sadece **✘✘** (ne parametrik ne retrieval) → chosen=IDK. Hedef ~8-10K (DTA=10K precedent) AMA kadran-yapılandırılmış + **marj-kontrollü** çift (chosen µ+2σ, rejected µ−2σ; max-min DEĞİL, çok-zor-küçük-marj DEĞİL).
- **B. gold-absent (✘✘) oranı = SWEEP knob (sabit-% değil).** DTA IDK-ratio optimum ~0.7 ama grounding-tacımızı (M1/M4) korumak için **0.3-0.5 başla, sweep.** Sıfır YASAK (DTA ablation: ✘✘ çıkınca abstention 0.0'a çöker = bizim v3 M2b'nin tam nedeni). RAFT: gold-oranı veri-bağımlı, evrensel-% yok.
- **C. Chosen şablon fix (keskinleşti).** "en ilgili kaynağı SEÇ" → "**herhangi biri yeterli mi? değilse IDK**" (forced-selection kökü). + gold-absent çiftlerde **doğru-cevabı da REJECTED'a koy** (DTA: şanslı-tahmini cezalandır). Muhakemeli-red KAL (CoT-chosen düz-cevabı yeniyor, +9-15pt) ama yapı = yeterlilik-kontrolü.
- **D. OOD = held-out-val + ERA-evidence (yeni).** Salt aile-çeşitliliği YETMEZ — preference-abstention OOD'de ezberler (DTA'nın kendi zaafı; ERA 2×'liyor). Chosen'da kanıt-cümlesi işaretle + held-out OOD validation.
- **E. τ temiz-etiket (Reçete 4 = CRaFT static-conflict).** near-dup çelişik-etiket over-refusal yapar; certainty-filtre. 108 hi_overlap judge'la, kazara-cevaplayanı at. (<$0.10.)
- **F. Replay denge-knob'u (YEDEK).** ORPO'nun SFT-terimi = DTA aux-SFT'nin ref-free hali (DTA'da SFT-terimi çıkınca answer 63.7→38.8). M1/M4 düşerse replay↑.
- **G. (opsiyonel plato-kırıcı) online hard-negative (RAAT).** "relevant retrieval noise" (near-miss) en yıkıcı; adaptif-adversarial +2.08 F1. v4.1'e bırakılabilir.

## 3. ZEMİN — (A) v2b-continuation KESİNLEŞTİ (deep-research teyidi)
- **(A) v2b-continuation ORPO.** ✅ **KARAR: BU.** Kanıt: grounding'in hayatta kalması için preference'a **SFT-terimi eşlik etmeli** (DTA: aux-SFT çıkınca answer çöküyor); **ORPO bunu doğuştan + ref-free veriyor** (12GB kısıtına ideal). LoRA regularizer (full-FT over-refusal+forgetting yapar, LoRA hafifletir). v3 zaten prior'ın kırılabildiğini gösterdi (M1↑).
- **(B) base-joint-ORPO** — ELENDI (şimdilik). Continuation-vs-joint tavan farkına dair doğrudan kanıt yok; (A) kanıtlı ve ucuz. Yalnız v4 duvara toslarsa yeniden değerlendir.

## 4. KAPI (v4 başarı)
M2b ≥0.90 (regresyon kapalı) **+** M2 ≥0.704 (base-üstü) **+** xkanun ≥0.90 **+** ood ≥0.75 **+**
M4/M1/M3/register ≥v3 (regresyonsuz) **+** M5 ≤0.10 (anti-hedef korunmuş). → ADR-0016.

## 5. GRILLING KİLİTLİ KARARLAR (2026-07-06)

**KARAR-1: Tez-güdümlü 2-kadran (retrieval-merkezli) + ✗✓-aşı dilimi** (tam 4-kadran DTA DEĞİL).
- Kural: **retrieval-KB ✓ → cevapla · retrieval-KB ✗ → REDDET** (parametrik ne olursa). Tam parametrik-KB probing (δ/N) ATLANDI — tezimiz ✗✓'de ezberden-cevabı reddediyor (M5 düşük-kalsın). 
- **✗✓-aşı dilimi (küçük):** "ünlü/aşina kanun sorusu + kaynak-yok → chosen=reddet" → ezber-sızıntısına aşı.
- **Kadran-etiketleme ≈ BEDAVA:** retrieval-KB kurguyla biliniyor (replay=gold-present ✓ / trap=hard-neighbor ✗); judge SADECE gri-bant (hi_overlap) için (<$1).

**KARAR-2: ~8K çift, gold-absent (✘/abstain) oranı SWEEP 0.3 / 0.4 / 0.5.**
- DTA-10K'ya yakın ama grounding-tacı (M1/M4) için DTA'nın 0.7'sinden düşük. Sıfır YASAK (abstention çöker). En iyi oranı 3-değerli sweep seçer (küçük dev-set'te).

**KARAR-3 (marj-kontrolü, ref-free surrogat):** RM yok → marjı **iki-taraflı rejected-filtresiyle** kur:
degenerate rejected (boş/mojibake/tekrar) AT · near-correct rejected (gri-bant τ) AT · "emin-ama-yanlış" fabrikasyon TUT. ⚠️ µ±2σ'yı birebir kopyalamaz (kabul edilen yaklaşım).

**KARAR-4 (chosen = TEK şablon, C+D+E birleşti):**
- Grounding chosen: `[ilgili cümle birebir alıntı] → [cevap]` (RAFT-CoT).
- Abstain chosen: `Sağlanan kaynak [X]'i düzenliyor; soru [Y] hakkında, buna dair hüküm YOK → yanıtlayamam.` (kanıt = var/eksik uyuşmazlığı; forced-selection'ı öldürür + ERA-evidence gömer).
- gold-absent çiftlerde **doğru-cevap = REJECTED** (DTA: şanslı-tahmini cezalandır).

## 6. KAPI (v4 başarı) — değişmedi
M2b ≥0.90 **+** M2 ≥0.704 (base-üstü) **+** xkanun ≥0.90 **+** ood ≥0.75 **+** M4/M1/M3/register ≥v3 (regresyonsuz) **+** M5 ≤0.10 → ADR-0016.

## 7. MALİYET / PARA-KAPILARI (grilling tahmini)
Harvest (v2b 12B, Modal A100 ~1-2h) ~$5-15 · chosen (gpt-4o-mini ~8K) ~$3-5 · judge (eval+gri-bant) ~$1-2 · ORPO tam tur (Modal A100) ~$5-10 → **toplam ~$15-40.** Kesin sayı için önce **smoke (throughput kalibre).** **Hepsi onay-gerektirir** (Modal + judge para-kapısı).

## 8. ADIM PLANI (kilitli tasarım → koşum)
> **📋 TAM EXECUTION PLANI (taze-agent devralabilir, TDD + tam kod + komutlar):** [`../../superpowers/plans/2026-07-06-v4-execution.md`](../../superpowers/plans/2026-07-06-v4-execution.md) — 9 task, birim testler, para-kapıları işaretli. ⚠️ Düzeltme: harvest = **lokal RTX 5070 ($0)**, Modal yalnız ORPO.

- **ADIM 1 — kod:** `build_sft_v4.py` (2-kadran packer: replay=gold-present, trap=hard-neighbor + çapraz-kanun + ✗✓-aşı dilimi; `--gold-absent-frac` knob) + `gen_v4_chosen.py` (tek-şablon: grounding-alıntı / abstain-uyuşmazlık) + `build_orpo_v4.py` (rejected iki-taraflı filtre + doğru-cevap-rejected) + `judge_gray_band.py` (τ, gri-bant).
- **ADIM 2 — smoke (PARA-KAPISI):** küçük harvest + throughput/bütçe kalibre + 4/4 yeşil.
- **ADIM 3 — harvest ~8K (PARA-KAPISI):** rejected üretimi (Modal A100) + gri-bant judge + iki-taraflı filtre.
- **ADIM 4 — chosen üretimi:** tek-şablon (gpt-4o-mini) + doğru-cevap-rejected paketleme.
- **ADIM 5 — ORPO sweep (PARA-KAPISI):** gold-absent 0.3/0.4/0.5 → 3 tur (veya dev-set'le seç, 1 tam tur) · v2b-continuation.
- **ADIM 6 — eval (kanon 6-mod + genelleme + held-out OOD):** lokal generation → judge (PARA-KAPISI) → kapı (§6) → ADR-0016.

## İlgili
Deep-research bulguları [[../research_log/2026-07-06-v4-deep-research-bulgular]] (#34) · brief (tarihsel) [`deep_research_brief.md`](deep_research_brief.md) · tez [[../research_log/2026-07-06-v4-tasarim-tezi-answerability]] (#33) · v3 kaldıraç-kökeni [[../v3/receteler]].
