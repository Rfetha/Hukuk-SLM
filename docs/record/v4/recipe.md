# v4 RECIPE — answerability-dedektörü (kapsamlı ORPO) · DRAFT (deep-research revizyonu bekliyor)

> **Durum:** TASARIM DRAFT (2026-07-06). Grilling + deep-research revizyonu SONRA. Kilitli değil.
> **Tez:** [[../research_log/2026-07-06-v4-tasarim-tezi-answerability]] (#33) · **kaldıraç kaynağı:** [[../v3/receteler]].
> **Neden gerek:** v3 KISMİ (ADR-0015) — M2b regresyon 0.53 + M2 base-altı 0.593 + OOD zayıf 0.483.

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

## 2. KALDIRAÇLAR (judge-önceliklendirmesi; hepsi tek turda)
Çerçeve: "8 takası dengele" değil, **tek answerability-dedektörünü keskinleştir** — her çift present/absent sınırını netleştirir.

- **A. Veri-ölçeği + tüm-aile kapsama (1 NUMARA).** train 1741 → ~6-8K çift. Negatif aileleri: aynı-kanun near-miss (✓ var) + çapraz-kanun + **çok-distractor-gold-yok** + OOD-novel. (+ mümkünse temporal/çok-hop — şu an veri-boşluğu.)
- **B. Çok-kaynak RAFT bağlam (M2b fix).** abstain-çift = çok-distractor-**gold-yok** · grounding-replay = çok-kaynak-**gold-var** → aynı formatta present/absence ayrımı. (Reçete 2 türevi.)
- **C. Chosen şablon fix.** red-muhakemesi "en ilgili kaynağı SEÇ" → "**herhangi biri gerçekten cevaplıyor mu? yoksa reddet**" → forced-selection bias kökü kurur. (gen_v3_chosen.py.)
- **D. τ temiz-etiket (Reçete 4).** 108 hi_overlap çiftini judge'la, kazara-cevaplayanı at → M2 sinyali keskin. (<$0.10.)
- **E. Replay denge-knob'u (Reçete 3, YEDEK).** M1/M4 düşerse 0.20↑ ile karşı-ağırlık. Baştan açma, izle.

## 3. ZEMİN ÇATALI — AÇIK (grilling'de karar)
- **(A) v2b-continuation ORPO** (v3 gibi) — kanıtlı grounding-koruma (M1 0.881). **Öneri: BU** — v3 v2b-prior'ının kırılabildiğini gösterdi (tavan değil), darboğaz zemin değil **veri.**
- **(B) base-joint-ORPO** — grounding+abstention'ı base'den birlikte. Daha yüksek tavan potansiyeli ama grounding'i sıfırdan taşıma riski + pahalı. **Sadece** (A) duvara toslarsa.
- **Karar durumu:** ön-öneri (A); deep-research + grilling teyit edecek.

## 4. KAPI (v4 başarı)
M2b ≥0.90 (regresyon kapalı) **+** M2 ≥0.704 (base-üstü) **+** xkanun ≥0.90 **+** ood ≥0.75 **+**
M4/M1/M3/register ≥v3 (regresyonsuz) **+** M5 ≤0.10 (anti-hedef korunmuş). → ADR-0016.

## 5. MALİYET / PARA-KAPILARI
- Harvest (rejected üretimi, ~6-8K) = Modal A100 GPU · chosen üretimi = gpt-4o-mini (~$2-4) · ORPO tam tur = Modal A100 · full judge = gpt-4o-mini (~$1). **Hepsi onay-gerektirir.** v3'ten belirgin büyük (veri 4×).
- Kod-değişikliği: build_sft_v3 xkanun-üretici (~40 sat) + build_orpo_v3 RAFT-bağlam (~25) + gen_v3_chosen şablon (~20) + judge_hi_overlap (~60 yeni). 

## 6. AÇIK SORULAR → DEEP-RESEARCH'E
1. **Veri-ölçeği vs kalite:** 6-8K çift optimal mi, yoksa daha az-ama-daha-zor mu? Preference-veri ölçek-getiri eğrisi ne (hukuki RAG-refusal'da)?
2. **RAFT-abstain oranı:** çok-kaynak-gold-yok çiftlerinin ideal payı? (fazlası over-refuse'a iter — presence/absence dengesi.)
3. **OOD hard-negative mining yöntemi:** held-out kanun/konu dağılımından novel-soru üretiminin en sağlam yolu (sızıntısız)?
4. **Zemin (A vs B) literatür kanıtı:** continuation vs joint-preference tavan farkı üzerine bulgu var mı?
5. **Chosen-şablon:** "yokluğu tespit" muhakemesi için en etkili prompt yapısı (CoT-red vs kısa-red)?
6. **Plato kırma:** DPO/ORPO'nun RAG-refusal ~%87 platosunu aşan teknikler (Cor-RAIT, DTA, iteratif hard-negative) — bizim kısıta (12GB, ref-free) uygun olanı?

## 7. SIRADAKİ ADIM
Bu draft → **deep-research'e sok** → dönüşle grilling → recipe KİLİTLE → ADIM-plan → para-kapısı onayı → koş.
**Deep-research brief HAZIR (kopyala/tetikle):** [`deep_research_brief.md`](deep_research_brief.md) — §6 soruları + proje-bağlamı + kısıtlar + çıktı-formatı tek self-contained prompt. Tetikleme kullanıcıda.
