## 2026-07-03 — v2c TAM SKORKART (6/6 mod) + ❌ RED kararı + K3 negatif bulgu

**Ne:** v2c (Gemma 4 12B QLoRA, config=v2b, adapter `outputs/v2c/`) 6-mod kanon eval TAM kapandı (M5 + register + v2b-M2b-n40 son parçalar bugün koştu). **Sonuç: v2c REDDEDİLDİ.** Detay tablo/gerekçe: [[v2c/sonuclar]] · skorkart [[v2c/roadmap]] §6.

**Tam skorkart (kanonik: cevaplanan-only A1 ADR-0011, eval-mirror 900, n=40/35, hakem gpt-4o-mini, seed 3407):**

| Eksen | base | v2b | Mecellem | **v2c** | Kapı | Sonuç |
|---|---|---|---|---|---|---|
| M2 yanlış-kaynak red | 0.704 | 0.346 | 1.0\* | **0.407** | ≥0.90 | ❌ birincil çöktü |
| M1 grounding A1 @cov | 0.886@47.5% | 0.920@72.5% | 0.918@35% | **0.832@80%** | ≥0.904 | ❌ regresyon |
| M4 oracle grounding | 0.983 | 0.975 | 0.921 | **0.977** | ≥0.975 | ✅ |
| M2b RAG-ıska red | 1.0 | 0.96 | 0.919 | **0.973** | ≥0.96 | ✅ |
| M3 boş-kaynak red | 1.000 | 1.000 | 1.000 | **1.000** | 1.0 | ✅ |
| M5 KÖR (parametrik) | 0.225 | 0.175 | 0.35 | **0.125** | anti-hedef | ✅ (base altında) |
| register (expert-frac) | — | 1.0 | — | **1.0** | v2b'yi koru | ✅ |

> \* Mecellem M2=1.0 kör-red artefaktı (coverage %35–45'e çöker, M4 oracle'da bile) → gerçek ayrım değil.
> Kaynak: `outputs/eval/{gnd_bench_m1_v2c,gnd_bench_m4_v2c,abst_bench_m2_v2c,abst_bench_m2b_v2c,abst_bench_m3_v2c,corr_bench_m5_v2c,reg_m1_v2c}_summary.json` + `abst_bench_m2b_v2b_n40` (v2b M2b @n40 = 0.969, karşılaştırma teyidi).

**RED gerekçesi:** iki bağımsız kapı birden düştü — (1) birincil hedef M2=0.407 « 0.90 (v2b'den +0.06, base 0.704'ün altında); (2) §1 regresyon M1 A1=0.832 < 0.904. Tavan korundu (M4/M2b/M3/register) + anti-hedef tuttu (M5 0.125) ama tek başına yetmez.

**🔴 K3 NEGATİF BULGU (paper-değerli):** §3-E hipotezi "M2 reddi ucuz SFT counterfactual + abstain_trap ile öğretilir" **ÇÜRÜDÜ.** Tier A veri-kolu M2'yi yalnız 0.346→0.407'ye taşıdı, üstelik M1'i 0.920→0.832 düşürdü. **Mekanizma = "Grounding-Abstention paradoksu":** SFT modeli cevap-üretmeye koşulladı → coverage↑ (47.5→80%, over-refusal↓ iyi) ama near-miss **ayrım gücü** köreldi. Hukukta yüksek semantik örtüşme → konusal-komşu yanlış kaynak (M2) latent-space'i yüksek-aktive edip fabrikasyona sürüklüyor (27 tuzağın 16'sı); bariz-off-topic (M2b) tetiklemediği için reddediliyor. → **near-miss discrimination SFT-tek-başına çözülemez.**

**Fix seçenekleri çerçevelendi (KARAR YOK):** literatür deep-research → [[v2c/fix_deep_research]] (5 aile: ORPO/DPO hard-negative · RAFT/loss-mask · R-Tuning/Suff-Context · RAAT/CaRT contrastive · DTA/RPO knowledge-boundary). Dış görüş-2 (Gemini) alındı, aynı dosyaya işlendi. En güçlü eşleşme: **DTA (Divide-Then-Align, ACL 2025)** failure'ı isim-isim tarif ediyor (Abstain-F1 0→63 + Acc 42→64); **RAFT'ın no-golden kolu abstain öğretmiyor** (bizim sorunu besleyebilir). **Yeni iterasyon adı/kararı VERİLMEDİ** (kullanıcı kısıtı) → seçenekler v2c ADR'ında "potansiyel durumlar". Herhangi yeni FT = Modal para-kapısı + kullanıcı onayı.

**Paper eşleme:** K3 negatif-sonuç bölümü (Grounding-Abstention paradoksu, TR hukuk vakası) + Mecellem differansiyel-avantaj (CPT-only, abstention mekanizması yok) + 6-mod kanon metodoloji (near-miss vs off-topic ayrımını ölçen benchmark).

---

