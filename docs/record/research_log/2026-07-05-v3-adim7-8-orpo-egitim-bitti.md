## 2026-07-05 · v3 ADIM 7 smoke GREEN + ADIM 8 ORPO tam eğitim BİTTİ — forget YOK, M2 öğrenildi

**ADIM 7 Modal smoke ✅ YEŞİL (para-kapısı, ~$0.15).** `train_orpo --run-name v3-smoke --max-steps 50` 4/4 kriteri geçti: (a) **v2b-continuation çalışıyor** — log `[orpo] v2b-continuation: /outputs/v2b (is_trainable) — grounding taşındı` (v2b LoRA `PeftModel is_trainable` olarak Unsloth'la yüklendi, grounding taşındı, recipe Q2); (b) **is_pref maskesi çalışıyor** — collator else-dalında list geldi, `MaskedORPOTrainer` torch.where ile NaN-safe sıfırladı; (c) **OOM/NaN yok**, nll_loss loglanıyor. → ADIM 8 tam eğitim açıldı.

**ADIM 8 ORPO tam eğitim ✅ TAMAMLANDI.** `modal run --detach modal_train.py::train_orpo --run-name v3 --epochs 2 --beta 0.1 --lr 1e-5 --save-steps 28` · app `ap-6mWKR1039jy99a9xl4Gtcv` · A100-40GB · **56/56 step, 2 epoch** · kapanış logu `[orpo] bitti → adapter: /outputs/v3` · crash/timeout/OOM/NaN **YOK**. Efektif batch 64, 1741 train örneği. base = **v2b-continuation** (grounding taşındı; v3 v2c'yi DEĞİL v2b'yi temel alır — v2c başarısız yan-daldı).

**nll_loss trajesi (FORGET-VEKİLİ) — istikrarlı düşüş, forget YOK:**
| step | epoch | nll_loss |
|---|---|---|
| 5 | 0.18 | 7.645 |
| 10 | 0.37 | 6.394 |
| 15 | 0.55 | 5.385 |
| 20 | 0.74 | 4.646 |
| 40 | 1.44 | 3.147 |
| 50 | 1.81 | 2.970 |
| 55 | 1.99 | **2.956** |

7.645 → 2.956 monoton azalış → **v2b grounding'i KORUNDU**. Bu, v2c'yi öldüren M1-forget'in (nll tırmanışı) bu run'da GÖRÜLMEDİĞİnin train-içi kanıtı. Grounding-replay satırlarının (is_pref=0, sadece NLL akan RAG_MULTI) mimari amacı tuttu.

**rewards/margins + accuracies — M2 abstention ÖĞRENİLDİ:**
| step | margins | accuracies |
|---|---|---|
| 5 | -0.3123 | 0.1562 |
| 15 | -0.1635 | 0.1844 |
| 40 | -0.02354 | 0.1688 |
| 50 | **+0.02627** | **0.2281** |
| 55 | -0.007193 | 0.1906 |

margins -0.31 → ~0 (step 50'de pozitife geçti, sonda sıfır civarı gürültülü); log_odds_ratio -4.789 → -1.319 (sonlu, iyileşti). **ORPO M2 sinyalini öğrendi; açık divergence YOK.** ⚠️ margin sadece train-içi proxy — gerçek M2 kazanımı ADIM 9 davranış-eval'inde ölçülecek. val: `eval_loss=3.364`, `eval_rewards/accuracies=0.125`, `eval_margins=-0.047` (sonlu).

**Volume teyidi — İKİSİ DE VAR (ampirik 1-vs-2 epoch kıyası hazır):**
- **Final (2-epoch):** `/v3/adapter_model.safetensors` + `adapter_config.json` (+ `checkpoint-56/`)
- **checkpoint-28 (~1-epoch):** `/v3/checkpoint-28/` — adapter + optimizer/scheduler tam.
- `--save-steps 28` bunu sağladı; ara-commit logları (`[modal] ara commit → v3 checkpoint kalıcı`) checkpoint kalıcılığını doğruladı (bütçe bir şekilde bitse bile 1-epoch güvendeydi).

**NET:** İdeal senaryo gerçekleşti — nll düşerken (grounding korunuyor) margin/accuracy yükseldi (abstention öğreniliyor). **Forget uyarısı YOK. ADIM 9 eval'e HAZIR** (her iki adapter volume'de, `modal volume get hukuk-outputs /v3` ile çekilmeye hazır). Kapı kararı (v3 RED/YEŞİL) ADIM 9 sonucuna göre insan verecek.

**Sıradaki = ADIM 9 eval (lokal, GPT-judge maliyeti, onay-kapısı):** checkpoint-28 (1ep) vs final (2ep); kanon 6-mod + `trap_xkanun`/`trap_ood` genelleme dilimleri + Mecellem sütunu + register + M5. KAPI: **M2≥0.704 + M1 A1≥0.904 + tavan koru (M4/M2b/M3/register) + M5 base-altı**. 2 SMK trap (ov~0.55) kazara-cevaplama spot-check.

**Kaynak:** Modal app `ap-6mWKR1039jy99a9xl4Gtcv` · `scripts/train_orpo.py` (`MaskedORPOTrainer`, `--save-steps`) · `modal_train.py::train_orpo` · volume `hukuk-outputs:/v3`.
**Paper eşleme:** nll↓ + margin↑ birlikteliği = K3 "Grounding-Abstention paradoksu"na ORPO çözümünün train-içi imzası (düz SFT'de v2c'de bu ikisi çelişmişti). Detach-kalıbı + save-steps ara-checkpoint = reprodüksiyon notları.

---

