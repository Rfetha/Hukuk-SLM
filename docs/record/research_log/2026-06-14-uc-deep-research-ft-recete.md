### 2026-06-14 — 3. /deep-research (FT-reçete) YENİDEN koşuldu → v2b reçete kartı
Önceki koşu (`wjwzv3ney`) session-limit'e çarpıp inconclusive bitmişti; arka-plan workflow olarak yeniden koşuldu (26 kaynak, 109 iddia → 25 doğrulandı, **21-doğru / 4-çürük**). Reçete kartı → `V2_PLAN.md §5.1`. Öne çıkan numaralı bulgular:
1. **RAFT (2403.10131):** k=5 (1 gold+4 distractor), `##begin_quote##`+CoT. **P=%80 evrensel optimum DEĞİL** (alan-bağımlı 40–100%) → [60–100%] ablate. 4-distractor da İngilizce-QA ekstrapolasyonu.
2. **Hedge oranı SABİT DEĞİL — keyfi %15/%25 ÇÜRÜTÜLDÜ (1-2).** Veri-güdümlü: modelin bilmediği soru oranına eşle (R-Tuning tahmin-vs-etiket; AfH m=10/τ=0.1).
3. **K3-DESTEK:** v1 abstention çöküşü (0.74→0.00) literatürde birebir = **Cor-RAIT over-refusal** (known-acc %16–37 düşer: TriviaQA 45→28.6, NQ 24.6→15.9). Sebep static+dynamic conflict. Düzeltme = **CRaFT** certainty-aware etiket + high-certainty rehearsal. "honesty-SFT accuracy korur" garantisi **YOK (0-3)**.
4. **Forgetting:** LoRA az unutur ama sıfırlamaz; düşük rank+az epoch; `target_modules=all-linear` (MLP dahil, attn-only zayıf); LoRA LR≈full-FT×10. ⚠️ "LoRA reg'den güçlü" + "full-FT rank 10-100x" **çürütüldü (0-3)**.
5. **Replay %1–5** (alt-sınır; %1 bile belirgin). 🚫 **3e-4 re-warming KULLANMA** — v1 çöküşü rejimi, continual-PRETRAINING reçetesi (davranışsal SFT'ye taşınmaz).
6. **Cevapsız (araştırma sorusu 5/6):** KL-to-base + EAFT entropy-gating pratiği HİÇBİR claim'le desteklenmedi → opsiyonel/deneysel, reçeteye girmez. Birleşik etkileşim çalışması yok → kendi ablasyon.
**Paper-eşleme:** K3 negatif-bulgu (v1 çöküşü = literatürdeki Cor-RAIT over-refusal mekaniği, neden+kaynaklı). Methodology: v2b reçetesi kanıt-temelli, çelişkiler işaretli.
**Kaynaklar:** RAFT 2403.10131 · R-Tuning 2311.09677 · Alignment-for-Honesty 2312.07000 · CRaFT 2410.06913 (AAAI25) · LoRA-forgetting 2405.09673 · Thinking-Machines LoRA-blog · replay 2403.08763 / 2508.01908 · Beyond-Cosine 2503.02844 · EAFT 2601.02151.

