# ADR 0014 — v2c RED kararı + fix yönü AÇIK (potansiyel durumlar, karar ertelendi)

- **Durum:** Yürürlükte (2026-07-03) — *v2c-reddi* kısmı KESİN; *fix-yönü* kısmı BİLİNÇLİ AÇIK (karar bir sonraki ADR'de).
- **Dayanak:** v2c 6-mod tam skorkart ([[v2c/sonuclar]], [[v2c/roadmap]] §6, research_log 2026-07-03) + fix literatür taraması ([[v2c/fix_deep_research]], + Gemini dış görüş-2).
- **İlgili:** ADR-0011 (canon eksen), ADR-0012 (v2 strateji ön-kayıt), ADR-0013 (5-mod matris). Genişletir: v2b sonuçları [[v2b/sonuclar]].

## Bağlam

v2c (Gemma 4 12B QLoRA, config=v2b, adapter `outputs/v2c/`) tek amaçla eğitildi: **v2b'nin bıraktığı tek gerçek açığı — M2 yanlış-kaynak reddini (0.346) — kapatmak**, Tier A veri-kolu (madde-komşusundan üretilen counterfactual + `abstain_trap` dilimleri) ile. Hedef §6'da ÜSTÜNLÜK'e yükseltilmişti (M2 ≥0.90, M1 ≥0.94), regresyon değil.

6-mod kanon eval tam kapandı (kanonik: cevaplanan-only A1 ADR-0011, eval-mirror 900, n=40/35, hakem gpt-4o-mini, seed 3407):

| Eksen | base | v2b | v2c | Kapı | Sonuç |
|---|---|---|---|---|---|
| M2 yanlış-kaynak red | 0.704 | 0.346 | **0.407** | ≥0.90 | ❌ |
| M1 grounding A1 @cov | 0.886@47.5% | 0.920@72.5% | **0.832@80%** | ≥0.904 | ❌ |
| M4 oracle · M2b · M3 · register · M5(anti) | ✓ | ✓ | **0.977·0.973·1.0·1.0·0.125** | koru | ✅ |

## Karar

### KESİN (bu ADR'de veriliyor)
1. **v2c REDDEDİLDİ.** İki bağımsız kapı birden düştü: birincil hedef M2=0.407 « 0.90 (v2b'den yalnız +0.06, base'in altında) **ve** §1 regresyon M1 A1=0.832 < 0.904. v2c prod adayı DEĞİL; `outputs/v2c/` referans/negatif-kanıt olarak saklanır.
2. **K3 negatif bulgusu kabul edildi (paper-değerli):** §3-E hipotezi "M2 reddi ucuz SFT counterfactual ile öğretilir" **ÇÜRÜK.** SFT coverage kazandırır (over-refusal↓) ama **near-miss discrimination'ı bozar** ("Grounding-Abstention paradoksu"). → near-miss abstention **SFT-tek-başına çözülemez**; SFT-üstü bir mekanizma (tercih-opt / loss-mask / knowledge-boundary) gerekiyor.
3. **Tavan + anti-hedef doğrulandı:** M4/M2b/M3/register korundu, M5 base altında (RAG'e dayanma kanıtı) → sorun modelin *yeteneği* değil, *yakın-yanlış kaynağı ayırt etme*si.

### AÇIK — BİLİNÇLİ ERTELENDİ (bu ADR karar VERMEZ)
Bir sonraki iterasyonun **adı, kapsamı ve yöntemi seçilmedi** (kullanıcı direktifi: "yeni kararı verme, v2d mi v3 mü düşünme; farklı dış faktör + deep research yapabiliriz"). Aşağıdaki **potansiyel durumlar** masada; seçim ayrı bir ADR'de, ek girdi (Gemini tartışması + olası ikinci deep-research) sonrası yapılacak.

## Potansiyel durumlar (seçenek havuzu — hiçbiri seçilmedi)

Kaynak: [[v2c/fix_deep_research]] (5 fix ailesi, kanıtlı) + Gemini dış görüş-2.

**P1 — Tercih-optimizasyonu (ORPO/DPO/KTO) hard-negatif üzerinde.** "Yanlış-kaynağa-cevap"=rejected, "çekimser"=chosen. ORPO ref-model'siz → QLoRA/12GB'ye en uygun. Risk: tercih çiftleri **M2-tipi near-miss dağılımından** üretilmezse yine off-topic öğrenir; format-bias; DPO tek-başına RAG-refusal'da ~%87 sınırlı.

**P2 — Knowledge-boundary hizalaması (DTA / RPO).** Failure'ı isim-isim tarif eden aile (DTA=Divide-Then-Align, ACL 2025): ✔✘ kadranı = "parametrik bilir ama retrieval yanlış" → near-miss'e-yapışma WA1 olarak cezalanır. Kanıt en güçlü (Abstain-F1 0→63, Acc 42→64). Risk: DPO ref-model yükü (12B+12GB'de lokal zor → Modal A100); yüksek veri-mühendisliği (4-kadran etiketleme); near-miss'i off-topic'ten **kendi verinle** ayırman şart (otomatik değil).

**P3 — Contrastive / hard-negatif SFT (RAAT / CaRT).** near-miss chunk'ı sistematik madenle, "counterfactual"ı ayrı sınıf yap (RAAT aux-head) veya terminate/answer'ı flip eden minimal-çiftler (CaRT). Saf-SFT bütçesi. Risk: **en yüksek veri-mühendisliği**; yanlış kurulan "kolay" negatifle mevcut durumu tekrar üretme riski.

**P4 — Abstention/calibration (R-Tuning / Sufficient-Context).** certain→cevapla, uncertain→"bilmiyorum". Saf-SFT, ucuz. Risk: odak **parametrik** bilgi sınırı; retrieval near-miss'i dolaylı; "yeterli bağlam" etiketi hukukta pahalı.

**P5 — RAFT/loss-masking — ⚠️ UYARILI.** Deep-research + DTA bağımsız gösterdi: **RAFT'ın no-golden kolu abstain ÖĞRETMİYOR, ezber öğretiyor** → bizim M2 fabrikasyonunu *besleyebilir*. Tek başına fix DEĞİL; ancak bir abstain-koluyla birleşirse.

**P6 — FT-DIŞI dış faktörler (yöntem değişmeden).** (a) İkinci/derin deep-research + Gemini-tartışması sonucu yön netleştirme; (b) veri-kompozisyonu odaklı deney (literatür: "model büyütmek abstention'ı çözmüyor, çözüm veri-kompozisyonunda" → asıl kaldıraç near-miss negatif *yoğunluğu/kalitesi*, yeni algoritma değil); (c) eval-tarafı: n≥100 güç + κ-vekili (n=40'ta bile red kesin ama fix-turunu ölçmek için gerekebilir); (d) M2 tuzak-seti near-miss dağılımının denetimi (8/35 invalid-trap oranı → tuzak-kalitesi fix-sinyalini bulandırıyor olabilir).

**Ortak kısıt (tüm P'ler):** hiçbir yöntem near-miss vs off-topic ayrımını *otomatik* yapmıyor → hepsi **kendi M2-near-miss negatif dağılımımızı** kurmayı gerektiriyor. Bu bir **veri-kompozisyon** sorusu, salt-algoritma değil.

## Sonuç (kanıt + kabul edilen risk + açık uçlar)

- **Kanıt:** tam skorkart `outputs/eval/*_v2c_*_summary.json` + `corr_bench_m5_v2c` + `reg_m1_v2c` + `abst_bench_m2b_v2b_n40` (v2b M2b@n40=0.969 teyit). Detay [[v2c/sonuclar]].
- **Kabul edilen risk:** v2c prod'a çıkmıyor; bir tur daha FT gerekiyor → zaman + Modal maliyeti. Fix-turu **para-kapısı + kullanıcı onayı** olmadan başlamaz.
- **Açık uçlar:** (1) fix yöntemi seçimi = sonraki ADR; (2) DTA'nın QLoRA-tek-adapter/12GB'de ref-model belleğiyle sığıp sığmadığı (yoksa ORPO-benzeri ref-free varyant?) — literatürde DTA ref-free yok; (3) near-miss negatif veri-üretim reçetesi tanımlı değil; (4) format-bias ölçümü (ayrım "kaynak-yeterliliği"nden mi yüzeysel biçimden mi öğreniliyor).
- **Süpersed etmez:** ADR-0011/0012/0013 geçerli; bu ADR onların üstüne v2c-sonucunu ve fix-yönü-açıklığını ekler.

## İlgili
- [[v2c/sonuclar]] · [[v2c/roadmap]] §6 · [[v2c/fix_deep_research]] · [[v2b/sonuclar]] · research_log 2026-07-03.
- ADR-0012 (v2 ön-kayıt: SFT=davranış, bilgi=RAG) — bu ADR onun "davranış" kolunun bir sınırını (near-miss abstention SFT-tek-başına yetmez) ampirik olarak işaretler.
