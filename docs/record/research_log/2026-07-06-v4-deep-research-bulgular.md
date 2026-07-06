# 2026-07-06 · v4 deep-research bulguları — DTA/Sufficient-Context/RAFT sentezi + taslak revizyonu

> **Bağlam:** v4 tasarım taslağı ([[../v4/recipe]]) için `/deep-research` koştu (16 kaynak, 70 iddia,
> 23 confirmed / 2 killed, 3-oy adversarial). Sentez-agent'ı stub döndü → bulgular journal'dan çıkarıldı.
> Bu entry = 6 soruya göre organize edilmiş **künyeli bulgular + v4 recipe REVİZYON listesi.** Kaynaklar §sonda.
> **En büyük keşif: DTA (Divide-Then-Align, ACL 2025) bizim problemimizin literatürdeki tam karşılığı.**

## ⭐ Baş bulgu — M2b regresyonumuz İSİMLİ, GENEL bir başarısızlık modu (bug değil)
- **Sufficient Context (ICLR 2025):** RAG paradoksal olarak abstention'ı **bastırır** — Claude 3.5 Sonnet
  abstain oranı RAG'la **84.1%→52%** düşer; bağlam yetersizken model reddetmek yerine yanlış cevap uydurur.
  **Bu tam bizim v3 M2b'miz (0.96→0.53).** Büyük modeller (Gemini 1.5/GPT-4o/Claude 3.5) yeterli-bağlamda
  iyi ama yetersiz-bağlamda uyduruyor.
- **RefusalBench (2510.10390):** çok-belge reddi tek-belgeden dramatik zor — **tüm frontier modeller multi-doc'ta
  <%50 red doğruluğu** (en iyi DeepSeek-R1 %47.4); Claude-4-Sonnet tek→çok belgede **73.0→36.1** çöküyor.
  → v3 M2b regresyonu **train artefaktı değil, yapısal-genel bir mod.** (Yan sonuç: base'in M2b=1.0'ı, frontier
  bile %50 yapamazken, kesin **over-refuse** — bizim "base red'i patoloji" tezini doğrular.)
- **Paper değeri:** bizim "answerability discrimination" tezimiz (entry #33) literatürde **Sufficient Context**
  olarak formalize; M2b = bilinen-zor problem; **DTA = belgelenmiş çözüm.**

## Soru-1 — Preference-veri ölçek-getiri eğrisi ⚠️ TEZ DÜZELTİLDİ
- **DTA tam 10.000 çift** kullanıyor [DTA]. Bizim 1741 → bu mertebe hedef.
- **AMA ham ölçek tek başına ÇALIŞMAZ:** max-min çift-kurgusu örnek 5→200 ölçeklenince **iyileşmiyor, bozabiliyor**
  (2502.16825; ⚠️ bu iddia workflow'da *killed* = tartışmalı, ama nüansı doğrulandı). Optimal çift **iyi-ayrık ama
  maksimal-ayrık DEĞİL** (chosen µ+2σ, rejected µ−2σ → max-min'den +3pp); **küçük-marjlı ("çok-zor") çiftler
  underfit ediyor** (%34.6 vs %48.2 LC-winrate).
- **REVİZYON:** *"Veri-ölçeği 1 numara"* tezimiz **eksikti** → doğrusu **"kurgu-kaliteli ölçek."** Volüm değil,
  **çift-yapısı (kadran + kontrollü marj)** kaldıraç. Hedef ~8-10K AMA DTA-tarzı yapılandırılmış, marj-kontrollü.

## Soru-2 — Gold-absent (✘✘) oranı: TUNED knob, sabit-% DEĞİL
- **DTA "IDK-ratio" ~0.7 optimum;** 0.1-0.7 arası abstain-F1'i **monoton artırıyor**, 0.9'da over-abstention.
- **✘✘'i tamamen çıkarınca abstention SIFIRA çöküyor** (tüm metrik 0.0) ama recall/denoise yapay yükseliyor
  → **gold-absent örnek ZORUNLU ama sınırlı.** (Bu ablation = bizim v3'ün tam hikâyesi: train'de ✘✘ yoktu → M2b çöktü.)
- **RAFT:** gold-içeren oran P% **veri-setine bağlı** (NQ %40, TriviaQA %60, HotpotQA %100) → gold-absent %0-60,
  **evrensel sabit-% YOK.**
- **REVİZYON:** gold-absent oranını **sweep et (başlangıç 0.3-0.5**, DTA'nın 0.7'sinden düşük çünkü grounding tacımızı
  —M1/M4— koruma önceliğimiz var); sıfır = M2b kırık kalır. Taslaktaki "keyfi %X yok" uyarısı doğrulandı.

## Soru-3 — OOD/görülmemiş-kanun mining: bilinen zor, ERA-tarzı gerekir
- **Abstention-SFT domain-ötesi kötü genelliyor** (Abstention survey 2407.18418). **DTA bile refusal-örüntülerini
  EZBERLİYOR → OOD'de over-abstain** (Wiki-Event); **ERA (2604.20854) OOD Answer-F1'i 2×'liyor**, Abstention-F1'i korurken.
- **REVİZYON:** OOD zayıflığımız (0.483) preference-abstention'ın **bilinen kusuru.** Sızıntı-kontrolümüz
  (train-seed sorusu, kanun_no≠gold) doğru ama **yetersiz** → ekle: **held-out OOD validation** + **ERA-tarzı
  evidence-grounding** (chosen'da kanıt-cümlesini işaretle). Salt çeşitlilik ezberi engellemez.

## Soru-4 — Zemin: (A) continuation DOĞRULANDI
- **DTA DPO-tabanlı + chosen'a auxiliary SFT-loss ŞART;** SFT-terimini çıkarınca answer-quality **63.7→38.8 çöküyor**
  → grounding'in hayatta kalması için **preference'a SFT-terimi eşlik etmeli.** **ORPO bunu doğuştan yapıyor**
  (nll-terimi + ref-free bonus) → bizim mimari zaten doğru.
- **LoRA regularizer:** full-FT → over-refusal + forgetting; **LoRA ikisini de hafifletip abstention'ı artırıyor**
  → QLoRA seçimi doğrulandı. **DPO > SFT red'de** (7B'de 3.4×) → preference-tercihi doğrulandı (K3 teyidi).
- **REVİZYON:** **(A) v2b-continuation KAL** (base-joint'e gerek yok). Kanıt SFT-terimi-eşliğini destekliyor, ORPO
  bunu ref-free veriyor = 12GB kısıtına ideal.

## Soru-5 — Chosen yapısı: muhakemeli-red DOĞRU ama yeniden-yapılandır
- **CoT-chosen (gerekçe + birebir atıf) düz-cevabı yeniyor:** RAFT+CoT, RAFT-CoT'suz'a karşı **+9.66 HotpotQA,
  +14.93 HuggingFace**; düz-cevap hızlı overfit. **Muhakeme-izleri davranışı nedensel şekillendiriyor** (2603.12397);
  aynı final-cevapta bile **red-gerekçesinin YAPISI** genellemeyi belirliyor.
- **DTA ✘✘ şablonu:** chosen = açık IDK; **rejected'a doğru-cevap DA konuyor** ("şanslı tahmin"i cezalandır).
- **REVİZYON (chosen-fix keskinleşti):** muhakemeli-red KAL ama "en ilgili kaynağı **SEÇ**" (forced-selection bug'ının
  kökü) → **"herhangi bir kaynak yeterli mi? değilse IDK"**e çevir. + gold-absent çiftlerde **doğru-cevabı rejected'a
  ekle** (DTA tekniği) → confabulation'ı doğrudan cezalandır.

## Soru-6 — Platoyu kırmak: DTA dört-kadran = çekirdek mekanizma
- **DTA dört-kadran** (parametrik-KB × retrieval-KB, var/yok): sadece ✘✘→"IDK" chosen. RAFT-modeli üstüne
  uygulanınca **abstain-F1 0.0→63.3, acc 42.2→64.1 — grounding'i çökertmeden** (RAFT'ı "hep cevapla"dan kurtarır).
  ⚠️ **DTA ref-model ister (DPO)** → biz **veri-kurgu reçetesini ORPO'ya uyarlarız** (kadran-mekanizması substrate-bağımsız).
- **RAAT:** "relevant retrieval noise" (yüzeysel-ilgili ama cevapsız = **near-miss**) **en yıkıcı** gürültü →
  tam bizim tuzak- tipimiz; **adaptif-adversarial (online en-zor-gürültü) +2.08 F1** → online hard-negative mining.
- **CRaFT/RAIT:** over-refusal'ın nedeni **"static conflict"** (near-duplicate örneklere çelişik etiket) → certainty
  ile filtrele. **Bu bizim τ-temizlik kaldıracının (Reçete 4) literatür-karşılığı.**
- **Sufficiency-gating tek başına +2-10% ama "plato-kırıcı değil."**
- **REVİZYON:** v4 çekirdeği taslaktaki "RAFT çok-kaynak"tan daha güçlü → **DTA dört-kadran veri-kurgusu (ORPO-uyarlı,
  ref-free)** = answerability-dedektörünün operasyonelleşmiş hali. + τ-temizlik (CRaFT) + opsiyonel online-hard-neg (RAAT).

## Frontier notu (tez teyidi)
"Doğruluk-red arası ters-ilişki, hiçbir frontier >%80 ikisinde birden" iddiası [RefusalBench] workflow'da
**adversarial-refuted (killed)** → **frontier'ın DOĞA-KANUNU olmadığı** tezimizi (entry #33) destekler. Yine de
ampirik olarak >%80-ikili henüz kimse yapmamış → hedefimiz (~0.90-abstention + korunmuş-grounding) **iddialı ama
duvar değil.**

## v4 RECIPE REVİZYON ÖZETİ (recipe'e işlenecek)
1. **Lever-1 düzelt:** "ham veri-ölçeği" → **"DTA-dört-kadran + marj-kontrollü kurgu"** (~8-10K, yapı>volüm).
2. **Kadran-veri kur:** parametrik-KB (bağlamsız N-örnek) × retrieval-KB (judge: top-k cevaplıyor mu) → ✘✘→IDK.
3. **gold-absent oranı sweep 0.3-0.5** (grounding-koru; sıfır yasak, 0.7 DTA-üstü riskli bizde).
4. **chosen-fix keskinleş:** "seç"→"yeterli mi? değilse IDK" + gold-absent'te **doğru-cevap=rejected**.
5. **OOD:** held-out val + ERA-evidence-grounding (salt çeşitlilik yetmez).
6. **Zemin (A) continuation KAL** (ORPO SFT-terimi = DTA'nın aux-SFT'sinin ref-free hali).
7. **τ-temizlik** = CRaFT static-conflict → tut. **online hard-neg (RAAT)** = opsiyonel plato-kırıcı.

## Kaynaklar (16, hepsi primary)
DTA (arXiv:2505.20871, ACL 2025) · Sufficient Context (arXiv:2411.06037, ICLR 2025) · RefusalBench (arXiv:2510.10390) ·
Preference Sweet Spot (arXiv:2502.16825) · Reasoning-Traces-Shape-Generalization (arXiv:2603.12397) · RAFT (arXiv:2403.10131) ·
RAAT (arXiv:2405.20978, ACL 2024) · CorCer-RAIT/CRaFT (arXiv:2410.06913, AAAI 2025) · ERA (arXiv:2604.20854) ·
Abstention Survey (arXiv:2407.18418) · RALM-know-when (arXiv:2509.01476) · ORPO (arXiv:2403.07691, EMNLP 2024).

## Paper eşleme
- **Related Work + Method:** DTA/Sufficient-Context/RAFT çerçevesi; bizim katkı = ORPO-ref-free-uyarlama + Türkçe-hukuk + register.
- **K3 genişletme:** M2b = Sufficient-Context'in "RAG suppresses abstention"ının bizde tekrarı (bağımsız doğrulama).
- İlgili: entry #33 (tez), #32 (v3 sonuç/M2b teşhis), [[../v4/recipe]] (revize edilecek).
