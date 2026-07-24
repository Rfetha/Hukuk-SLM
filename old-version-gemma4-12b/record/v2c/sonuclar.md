# v2c — CANON Eval Sonuçları (6-mod matris + register + M5) — ❌ REDDEDİLDİ

> **Karar:** v2c **REDDEDİLDİ** (2026-07-03). Birincil hedef M2 (yanlış-kaynak red) tutmadı **VE** §1 regresyon
> kapısı M1 kırıldı. Bu doküman = ölçülen tam skorkart + RED gerekçesi + **K3 negatif bulgusu** + mekanizma.
> Otorite kronoloji: [[research_log/README]] · Karar defteri: v2c ADR · Skorkart: [[v2c/roadmap]] §6 · Fix seçenekleri: [[v2c/fix_deep_research]].

## Kurulum (tüm modlar ortak)
- **Model:** Gemma 4 12B + QLoRA adapter `outputs/v2c/` (config = v2b: r=16, α=32, lr=1e-4, batch=1, grad_accum=16, 1 epoch, replay %3). Eğitim = Modal A100.
- **Eval:** lokal RTX 5070, deterministik seed 3407, eval-mirror (900-char chunk clip), hakem gpt-4o-mini.
- **n:** core_hard n=40 (M1/M4/M5/M2b), trap n=35 (M2), E-set n=40 (M3).
- **A1 kuralı (ADR-0011):** cevaplanan-only — çekinmeler ABSTAIN_RE ile ayrılır, macro faithfulness yalnız cevaplanan satırlarda; "A1 @ coverage%" olarak raporlanır. Tüm modellere aynı kural.
- **Kaynak:** `outputs/eval/*_v2c_*` (+ `corr_bench_m5_v2c`, `reg_m1_v2c`, `abst_bench_m2b_v2b_n40`) · Mecellem = C4 completion-fewshot (research_log "ADIM 2 · TABLO 1").

---

## Matris — durum panosu (6/6 mod kapandı)

| Mod | Ne ölçer | Eksen | Durum | v2c manşet |
|---|---|---|---|---|
| **M1** Gold+distractor | grounding-under-noise | A1·A4·register | ✅ ölçüldü | A1(cevaplanan)=**0.832 @80%** ❌ |
| **M2** TRAP (yanlış-kaynak, no-gold) | abstention | A3 | ✅ ölçüldü | Rej\*=**0.407** ❌ (birincil hedef çöktü) |
| **M2b** distractor-only | abstention (RAG-ıska) | A3 | ✅ ölçüldü | Rej\*=**0.973** ✅ |
| **M3** Boş/kaynaksız | abstention (kaynak-eksik) | A3 | ✅ ölçüldü | Rej\*=**1.000** ✅ |
| **M4** Temiz gold-only (Oracle) | iyimser tavan | A1·A4 | ✅ ölçüldü | A1=**0.977 @100%** ✅ |
| **M5** KÖR/kaynaksız | parametrik ezber | A2 | ✅ ölçüldü | A2=**0.125** ✅ (anti-hedef: base 0.225 altında) |
| register | uzman dili | A4-yan | ✅ ölçüldü | expert-frac=**1.0** ✅ |

---

## KAPI SONUCU — ❌ v2c REDDEDİLDİ

| Eksen | Kaynak | v2c | Eşik | Sonuç |
|---|---|---|---|---|
| **M2 yanlış-kaynak abstention (birincil hedef)** | M2 = 0.407 | ❌ | ≥0.90 (§6 üstünlük) | **BAŞARISIZ** (v2b 0.346'dan +0.06; base 0.704'ün altında) |
| **M1 grounding A1 (§1 regresyon)** | M1 cevaplanan = 0.832 @80% | ❌ | ≥0.904 | **REGRESYON** (coverage↑ %80 ama faithfulness↓) |
| A4 format (cit_precision) | M1 0.872 · M4 0.975 | 🟡 | ≥0.95 | oracle'da geçer, gürültüde düşük |
| A3 abstention (adil, deployment) | M2b 0.973 · M3 1.000 | ✅ | ≥0.96/1.0 | **GEÇTİ** (tavan korundu) |
| Oracle grounding tavan | M4 = 0.977 | ✅ | ≥0.975 | **GEÇTİ** |
| register (uzman dili) | expert-frac 1.0 | ✅ | v2b'yi koru | **GEÇTİ** |
| Anti-hedef (parametrik ezber) | M5 = 0.125 vs base 0.225 | ✅ | base'i geçme | **TUTTU** (RAG'e dayanma kanıtı) |

**İki bağımsız kapı birden düştü** → v2c kabul edilemez. Tavan eksenleri korundu ama tek başına yetmez.

---

## 4-MODEL KARŞILAŞTIRMA (kanonik)

| Eksen | base | v2b | Mecellem | **v2c** | Yön |
|---|---|---|---|---|---|
| **M2 yanlış-kaynak red** | 0.704 | 0.346 | 1.0\* | **0.407** | ↑ iyi — hedef 0.90 |
| **M1 grounding A1 @cov** | 0.886 @47.5% | 0.920 @72.5% | 0.918 @35% | **0.832 @80%** | ↑ iyi |
| M4 oracle grounding | 0.983 | 0.975 | 0.921 | **0.977** | ↑ iyi |
| M2b RAG-ıska red | 1.0 | 0.96 | 0.919 | **0.973** | ↑ iyi |
| M3 boş-kaynak red | 1.000 | 1.000 | 1.000 | **1.000** | ↑ iyi |
| M5 KÖR (parametrik) | 0.225 | 0.175 | 0.35 | **0.125** | ↓ iyi (anti-hedef) |
| register (expert) | — | 1.0 | — | **1.0** | ↑ iyi |

> \* **Mecellem M2=1.0 kör-red artefaktı:** coverage %35–45'e çöküyor (oracle M4'te bile). Yani "her şeyi reddet"
> davranışı → gerçek ayrım yeteneği değil, coverage-çöküşü. v2c'nin %80 coverage'ıyla kıyaslanamaz (bkz research_log ADIM 2).

---

## Mod detayları

### M1 — Gold + 4 distractor (grounding-under-noise) ❌
| Dilim | n | faithfulness (macro) | Yorum |
|---|---|---|---|
| Ham (çekinmeler dahil) | 40 | 0.724 | ❌ yanıltıcı — çekinme faith=0 çeker |
| **Cevaplanan = GERÇEK A1** | 32 (%80 cov) | **0.832** | ❌ §1 kapı 0.904'ün ALTINDA (v2b 0.920'den DÜŞTÜ) |
- cit_precision_micro=0.872, wrong_ref_rate=0.128 → gürültüde yanlış-madde atfı arttı.
- **Kritik:** coverage 47.5%(base)→72.5%(v2b)→**80%(v2c)** yükselirken faithfulness 0.886→0.920→**0.832 düştü** = coverage-faithfulness takası v2c'de ters döndü.

### M2 — TRAP: konusal-komşu YANLIŞ tek-kaynak, no-gold (abstention) ❌ **BİRİNCİL BAŞARISIZLIK**
| Metrik | base | v2b | **v2c** |
|---|---|---|---|
| **Rej\*(LLM)** ↑ | 0.704 | 0.346 | **0.407** |
| Rej(exact) ↑ | — | 0.308 | **0.370** |
| fabrication ↓ | — | 0.654 | **0.593** |
- 27 geçerli tuzağın **16'sı fabricate** (çekinmek yerine yanlış kaynağa yapıştı).
- Örnek fabrikasyonlar: "Pilot uygulama ne zaman başlayacak?" → alakasız 4320 sK'den uydurdu; "Başkasının ormanına girebilir miyim?" → TMK 752'yi aşırı-genelledi.
- Tier A veri-kolu (counterfactual + abstain_trap) yanlış-kaynak reddini **restore edemedi** (v2b'den yalnız +0.06).

### M2b — distractor-only (bariz-off-topic RAG-ıska) ✅
- Rej\* = **0.973** (37 geçerli tuzak, fabrication 0.027).
- **v2b M2b @n40 teyidi:** 0.969 (aynı reçete, n=40) → M2b her iki modelde de sağlam.
- **Ayrım kanıtı:** M2b (kolay-negatif) ✅ vs M2 (zor-negatif) ❌ → sorun off-topic değil, **makul-komşu** kaynak.

### M3 — Boş/kaynaksız (E-set) ✅
- Rej\* = **1.000** (31 geçerli tuzak, 0 fabrikasyon) — bağlam yokken hiç uydurmuyor.

### M4 — Temiz gold-only (Oracle tavan) ✅
- A1 = **0.977 @100% cov** (115 claim, hallucination 0.026, cit_precision 0.975).
- Temiz kaynak verildiğinde grounding mükemmel → sorun yetenek değil, **gürültü/yanlış-kaynak ayrımı**.

### M5 — KÖR/kaynaksız (parametrik ezber) ✅ anti-hedef
- correct=**0.125** (cov 1.0, cond_acc 0.125, lenient 0.75, partial 0.625). Sayım: 5 CORRECT / 25 PARTIAL / 10 WRONG / 0 ABSTAIN.
- base 0.225'in ALTINDA → model bağlamsız kesin-madde bilgisi vermiyor, RAG'e dayanıyor (istediğimiz).

### register — uzman dili ✅
- expert-frac = **1.0** (v1-lexical-proxy, hakemsiz; kanonik LLM-rubriği ADR-0013 TODO). v2b'yi korudu (G4 tavan).

---

## K3 NEGATİF BULGUSU (paper-değerli) + mekanizma

**Hipotez (§3-E):** "M2 yanlış-kaynak reddini birkaç-yüzdelik ucuz SFT counterfactual + abstain_trap verisiyle öğretmek yeterli." → **ÇÜRÜDÜ.**

**Kanıt:** v2c'nin Tier A veri-kolu M2'yi yalnız 0.346→0.407'ye taşıdı (base 0.704'ün altında kaldı), üstelik M1 grounding'i 0.920→0.832'ye düşürdü.

**Mekanizma — "Grounding-Abstention paradoksu" (literatürce doğrulandı, [[v2c/fix_deep_research]]):**
- SFT modeli sürekli **cevap üretmeye** koşulladı → coverage arttı (over-refusal↓, iyi yön) ama **ayrım gücü** köreldi.
- Hukuk terminolojisi yüksek semantik örtüşme içerir: yanlış ve doğru belge aynı aktörleri/kavramları paylaşır.
- Test anında belgenin **konusal yakınlığı (topical adjacency)** latent-space'te ilgili başlıkları yüksek-aktivasyonla tetikliyor; model "yasal olarak gerçekten karşılıyor mu?" diye sorgulamak yerine yakınlığı yeşil-ışık sayıp üretiyor.
- **Bariz-alakasız** belge (M2b) bu döngüyü tetiklemiyor → reddedilebiliyor ✅. **Makul-komşu-ama-yanlış** belge (M2) dikkat mekanizmasını yanıltıyor → fabrikasyon ❌.

**Sonuç:** near-miss discrimination'ı SFT tek başına çözemez → tercih-optimizasyonu / loss-masking / knowledge-boundary hizalaması gerekiyor (fix aileleri: [[v2c/fix_deep_research]]).

---

## Paper haritası
- **K3 negatif bulgu** = "SFT coverage kazandırır ama near-miss abstention'ı bozar" → paper'ın negatif-sonuç bölümü (Grounding-Abstention paradoksu, Türkçe hukuk vakası).
- **Mecellem karşılaştırması** = rakip CPT-only modelin abstention/grounding mekanizmasızlığı → differansiyel-avantaj argümanı.
- **6-mod kanon + eval-mirror + cevaplanan-only A1** = metodoloji katkısı (near-miss vs off-topic ayrımını ölçen benchmark).
