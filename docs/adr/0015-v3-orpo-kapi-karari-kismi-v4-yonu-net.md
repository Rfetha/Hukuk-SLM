# ADR 0015 — v3 ORPO kapı kararı: KISMİ (teslim değil) + v4 yönü NET

- **Durum:** Yürürlükte (2026-07-06). *v3-teslim-değil* KESİN; *v4-yönü* ADR-0014'ün aksine AÇIK değil **NET** (bu ADR yönü veriyor, tam reçete ayrı turda).
- **Dayanak:** v3 tam judge skorkartı ([[2026-07-06-v3-eval-sonuc-kapi-karari]], research_log entry #32) + M2b per-item teşhis (`outputs/eval/abst_bench_m2b_v3.jsonl`).
- **İlgili:** ADR-0014 (v2c RED + P1-ORPO seçildi) → bu ADR onun sonucunu verir. ADR-0011 (canon eksen), ADR-0012 (SFT=davranış/bilgi=RAG). Genişletir: [[v2b/sonuclar]], entry #30 (eğitim).

## Bağlam

v3 = ADR-0014'te seçilen **P1 yolu** (tercih-optimizasyonu / ORPO, hard-negatif üzerinde): v2b adaptöründen DEVAM eden ORPO turu (`train_orpo.py:132` PeftModel is_trainable, düşük lr). Tek amaç: v2b'nin bıraktığı + v2c'nin düz-SFT ile düzeltemediği (K3) tek gerçek açığı — **M2 yanlış-kaynak near-miss reddini** — grounding'i bozmadan kapatmak. Eğitim ADIM 8'de bitti (nll 7.65→2.96 forget-yok, margin -0.31→~0; entry #30). ADIM 9 lokal generation + gpt-4o-mini judge tamamlandı.

6-mod canon + 2 genelleme dilimi tam kapandı (cevaplanan-only A1, 900-char mirror, n=40/35, seed 3407, hakem gpt-4o-mini):

| Eksen | base | v2b | v2c | **v3** | Kapı | Sonuç |
|---|---|---|---|---|---|---|
| M1 grounding A1 | 0.662 | 0.737 | 0.681 | **0.881** | regresyon yok | ✅ arttı |
| M4 oracle | 0.978 | 0.968 | 0.974 | **1.000** | koru | ✅ |
| **M2 yanlış-kaynak red** | 0.704 | 0.346 | 0.407 | **0.593** | ≥0.704 | ❌ base-altı |
| **M2b RAG-multi miss** | 1.0 | 0.96 | 0.973 | **0.529** | koru | ❌ regresyon |
| M3 boş-bağlam | 1.0 | 1.0 | 1.0 | **1.000** | koru | ✅ |
| M5 anti-parametrik | 0.225 | 0.175 | 0.125 | **0.075** | base-altı | ✅ |
| Register uzman | 1.0 | 1.0 | 1.0 | **0.975** | koru | ✅ |

Genelleme (judge): xkanun base 0.968 / v2b 0.387 / **v3 0.656** · ood base 0.889 / v2b 0.115 / **v3 0.483**.

## Karar

### KESİN (bu ADR'de veriliyor)

1. **v3 teslim-adayı DEĞİL — strict kapı düştü.** İki gerçek borç: (a) **M2 = 0.593 < base 0.704** (birincil hedefte base geçilmedi); (b) **M2b regresyonu 0.96→0.529** (yeni açık). `outputs/v3/` prod'a çıkmaz; en-iyi-tur referansı + v4 başlangıç adaptörü olarak saklanır.

2. **AMA v3 ≠ v2c: kategorik ilerleme, RED değil "KISMİ".** v2c her yerde regresyondu (M1↓ + M2 base-altı); v3 **K3'ü büyük ölçüde tersine çevirdi** (M2 0.35→0.59, +0.19) **ve grounding'i yükseltti** (M1 0.74→0.88, base'i de geçti). ADR-0014'ün P1 hipotezi (ORPO M2'yi düz-SFT'den iyi öğretir) **DOĞRULANDI**; sadece base-üstüne henüz taşımadı.

3. **ORPO grounding'i bozmaz — yükseltir.** M1 0.737→0.881 + M4 1.0: SFT-terimi (chosen grounding) + preference birlikte forget yapmadı. ADR-0012'nin "SFT=davranış" kolu için pozitif kanıt.

4. **YENİ NEGATİF BULGU (paper-değerli) — M2b forced-source-selection.** M2b'de v3, 34 geçerli tuzağın 16'sında FABRICATE etti; örüntü birebir aynı ("İlgili kaynak KAYNAK X'tür çünkü... diğerleri elenmiştir"). **Kök:** ORPO muhakemeli-red şablonu "kaynakları değerlendir→en ilgilisini SEÇ" adımını öğretti; M2'de (tek yanlış kaynak) doğru, ama M2b'de (çok distractor, doğrusu yok) "hiçbiri değil→reddet" yerine en yakın distractor'ı seçip uyduruyor. **Ders: abstention tek beceri değil AİLE** (tek-kaynak-near-miss ≠ multi-miss ≠ boş-bağlam); tek-aile preference eğitimi komşu-aileyi bozabilir. K3'e alt-bulgu.

### v4 YÖNÜ — NET (ADR-0014'teki "açık" değil; tam reçete + para-kapısı ayrı)

Fix artık seçenek-havuzu değil, **teşhis-güdümlü**:
- **#2b negatif-aile çeşitliliği (birincil):** ORPO rejected setine **multi-distractor-no-gold (M2b-tipi)** + **OOD held-out** hard-negatifleri ekle → "cevap hiçbirinde yok→reddet" becerisini de eğit. Motor = OOD-odaklı hard-negative mining ([[../v3/receteler]] §v4 mimari notları).
- **M2'yi base-üstüne itme (ikincil):** near-miss negatif yoğunluğu/kalitesi (veri-kompozisyon kaldıracı; ADR-0014 P6-b).
- **⚠️ v2b-SFT ile "düzeltme" YASAK** (K3 tuzağı — abstention hep preference'ın işi).
- **Yöntem sabit:** yine ORPO (ref-free, 12GB-uyumlu); base-joint-ORPO yalnız v2b-continuation tavanı kanıtlanırsa alternatif.

## Değerlendirilen alternatifler

- **v3'ü teslim kabul et (RAG-gerçekçi bileşik base'i ezdiği için):** REDDEDİLDİ — M2b regresyonu prod-riski (multi-kaynak RAG senaryosu Faz-2'nin ana modu), önce kapatılmalı.
- **Hemen v4 reçetesi yaz (teşhissiz):** REDDEDİLDİ — M2b kökü (forced-selection) belirlenmeden veri kurmak kör atış; teşhis bu ADR'de yapıldı, artık hedef net.
- **1-epoch (ck28) tercih:** REDDEDİLDİ — final M2 0.593 > ck28 0.519; marjinal M1/register kaybı kabul edilebilir.

## Sonuç
- **Kanıt:** `outputs/eval/{gnd,abst,corr,reg}_bench_*_v3*_summary.json` + `abst_bench_m2b_v3.jsonl` (per-item teşhis) + genelleme `abst_bench_{xkanun,ood}_{base,v2b,v3}`. Judge maliyet ~$0.08. Detay [[2026-07-06-v3-eval-sonuc-kapi-karari]].
- **Kabul edilen risk:** bir tur daha FT (v4) gerekiyor → zaman + Modal maliyeti; **para-kapısı + kullanıcı onayı olmadan başlamaz.**
- **Süpersed etmez:** ADR-0011/0012/0014 geçerli; bu ADR 0014'ün P1-seçimini sonuçlandırır (ORPO çalışır, tek-aile yetmez) ve v4 yönünü daraltır.

## İlgili
- [[2026-07-06-v3-eval-sonuc-kapi-karari]] (entry #32) · entry #30 (eğitim) · entry #31 (konumlama) · entry #24 (K3) · [[../v3/receteler]] §v4 · ADR-0014 (P1 seçimi).
