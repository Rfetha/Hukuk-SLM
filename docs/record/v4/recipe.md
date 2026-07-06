# v4 RECIPE — answerability-dedektörü (DTA-uyarlı ORPO) · DRAFT-v2 (deep-research revize edildi; grilling'e hazır)

> **Durum:** DRAFT-v2 (2026-07-06). **Deep-research revizyonu İŞLENDİ** (bulgular [[../research_log/2026-07-06-v4-deep-research-bulgular]] #34). Sıradaki = grilling → kilit.
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

## 5. MALİYET / PARA-KAPILARI
- Harvest (rejected üretimi, ~6-8K) = Modal A100 GPU · chosen üretimi = gpt-4o-mini (~$2-4) · ORPO tam tur = Modal A100 · full judge = gpt-4o-mini (~$1). **Hepsi onay-gerektirir.** v3'ten belirgin büyük (veri 4×).
- Kod-değişikliği: build_sft_v3 xkanun-üretici (~40 sat) + build_orpo_v3 RAFT-bağlam (~25) + gen_v3_chosen şablon (~20) + judge_hi_overlap (~60 yeni). 

## 6. AÇIK SORULAR — ✅ DEEP-RESEARCH CEVAPLADI (#34)
6 sorunun hepsi cevaplandı (özet [[../research_log/2026-07-06-v4-deep-research-bulgular]]):
1. Ölçek → **yapı>volüm** (~8-10K ama kadran+marj-kontrollü; ham-volüm tek başına çalışmaz).
2. gold-absent → **sweep 0.3-0.5** (sabit-% yok; sıfır=abstention çöker).
3. OOD → **held-out-val + ERA-evidence** (salt çeşitlilik ezberler).
4. Zemin → **(A) continuation** (SFT-terimi-eşliği şart; ORPO ref-free verir).
5. Chosen → **CoT-red + yeterlilik-yapısı + doğru-cevap-rejected** (DTA).
6. Plato → **DTA dört-kadran (ORPO-uyarlı) çekirdek** + CRaFT-τ + opsiyonel RAAT-online.

**Grilling'e KALAN açık uçlar:** (a) kadran etiketleme maliyeti (retrieval-KB judge = gpt-4o-mini × kaç örnek?); (b) parametrik-KB eşiği δ ve N-örnek sayısı; (c) marj-kontrolü ORPO'da nasıl operasyonelleşir (reward-proxy yok — sürrogat?); (d) 8-10K harvest'in Modal-GPU bütçesi; (e) ERA-evidence chosen'a nasıl gömülür.

## 7. SIRADAKİ ADIM
Recipe DRAFT-v2 hazır (deep-research işlendi) → **grilling** (§6 kalan açık uçlar + kaldıraç parametreleri) → recipe KİLİTLE → ADIM-plan → para-kapısı onayı → koş.
Deep-research brief (tarihsel, koştu): [`deep_research_brief.md`](deep_research_brief.md).
