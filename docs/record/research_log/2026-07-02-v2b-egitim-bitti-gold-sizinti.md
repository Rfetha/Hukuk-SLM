## 2026-07-02 — v2b tam eğitim BİTTİ + eval-mirror + 🔴 GOLD-sızıntı bulgusu

#### v2b tam eğitim tamamlandı (Modal A100, --detach)
- `spawn_v2b --run-name v2b --epochs 1` (app `ap-mjvVVy5ZycRX5q69zcM9Tu`). Reçete §5.1 kilitli: lr=1e-4, r=16/α=32, all-linear, warmup=0.05, --no-system, 3e-4 yasak.
- **Sonuç:** 1.083/1.083 step, **4h19m** (12.72s/it), **train_loss=0.30**, epoch 1, OOM/hata yok. Truncation fix pratikte teyit: **17.323 örnek / 0 düşürüldü** ("Removed 0"; eski veride 1.421 düşüyordu). Adapter (65.5M, 262MB) `hukuk-outputs:/v2b`.
- **Modal kart dersi:** A100/H100 için hesaba ödeme yöntemi (kart) ŞART — $30 kredi olsa bile kapı olarak kart isteniyor. Kart eklenince spawn başarılı (kredi karttan önce harcanır). Kayda değer: önceki koşularda sorulmamıştı → Modal politikası büyük GPU'lara kapıyı yakın zamanda getirmiş.

#### Eval-mirror uygulandı + doğrulandı (ADR-0013 gereği, D1 ÖNCESİ)
- `gen_eval_grounded.py`: `--max-chunk-chars` (default 900) eklendi; distractor modunda eğitimin `clip_sources_block`'u **AYNEN** import edilip uygulanıyor → dağılım garantili eşleşir (aynı `_norm`, gold baş satırı eşleşmesi). Eval referansı `##begin_quote##` taşımaz → gold da baştan 900'e kırpılır (context UZUNLUĞU eşleşmesi birincil amaç).
- **Dry-run doğrulama (n=6, modelsiz):** ham kaynak bloğu 6-9K char → clip ~2.6-4.2K char (≈1050 tok), **gold her örnekte korunuyor** (gold_var=True). v2b artık eğitildiği context uzunluğuyla ölçülür (haksız-uzun bağlam riski kapandı).

#### 🔴 GOLD-sızıntı bulgusu (bir sonraki FT'de düzeltilecek — veri kalitesi)
- **Belirti (M1 çıktısı):** v2b bazı cevaplarda "İlgili kaynak ... **GOLD** metnidir" diyor. Ama öğrenci context'te kaynakları `[KAYNAK N]` diye görür — "GOLD" diye etiket YOK → var-olmayan etikete atıf = kafa karıştırıcı artefakt. (Doğru örnek "KAYNAK 3'tür" der.)
- **Kök neden (ölçüldü):** eğitim hedeflerinin **%5.7'si (990/17.323)** cevabında birebir "GOLD" kelimesi taşıyor. Suçlu `gen_v2b_answers.py` teacher prompt'u: talimat (satır 33-39) baştan sona "GOLD" sözcüğünü kullanıyor ("GOLD, diğerleri distractor", "GOLD metinden alıntıla", "Yalnız GOLD'a dayan") ve gold kaynak teacher'a `GOLD madde ({gold_id}):` diye etiketle veriliyor (satır 59-62). Teacher bu iç-jargonu %5.7 cevaba sızdırmış, öğrenci ezberledi.
- **Düzeltme (v2c/sonraki FT — iki katman):**
  1. **Önleme (teacher prompt):** teacher talimatına "cevabında 'GOLD' kelimesini ASLA kullanma; kaynaklara yalnız `[KAYNAK N]` etiketi veya (KANUN ADI, Madde X) atfıyla referans ver" ekle. Teacher, öğrencinin gördüğü etiket-uzayında (KAYNAK N) akıl yürütmeli — gold'u da `[KAYNAK N]` etiketiyle sun, "GOLD" adını hiç geçirme.
  2. **Retro ucuz temizlik (re-gen'siz):** mevcut answers'ta regex scrub — "GOLD metni/metnidir" → "ilgili kaynak" (veya gold'un shuffle sonrası KAYNAK-no'su biliniyorsa doğru `[KAYNAK N]`'e map). %5.7 → hızlı ve güvenli.
- **Paper'a:** methodology/veri-kalitesi bulgusu — "teacher iç-etiket jargonu (GOLD) öğrenci çıktısına sızar; teacher öğrenci-etiket uzayında promptlanmalı." Küçük ama gerçek bir grounded-synthetic tuzağı.

#### 🔑 Eval retriever-kalitesi ayrımı (kavramsal netleşme — eval-mirror'ın gerçek anlamı)
- **Kilit içgörü (kullanıcı):** üretimde (Faz 2 RAG) modele tüm madde değil **retrieve edilmiş chunk** verilecek → 900-char clip bir eval artefaktı DEĞİL, üretimdeki RAG chunking'ini simüle ediyor. Bu eval-mirror'ın asıl gerekçesi (bkz. 2026-06-24: "gerçek RAG retriever tam kanunu değil chunk döner"). **900-char = doğru, korunur.**
- **Model = RAG'ın GENERATOR yarısı:** görevi "verilen chunk'ta cevap varsa dayanarak-atıf yap; yoksa çekin". Retriever'ın işi (doğru chunk'ı getirmek) modelin işi değil → eval bu ikisini AYIRMALI.
- **Clip yöntemi = simüle edilen retriever kalitesi:** first-900 clip = 🔴 aptal retriever (hep baştan kes, ilgili fıkra ortada/sondaysa kaçırır → model haklı çekinir ama modeli olduğundan kötü gösterir). **answer-anchored pencere** (aynı 900, gold penceresini core_hard referans cevabına lexical-anchor'la ortala) = 🟢 akıllı/semantik retriever → modelin gerçek grounding yeteneğini ölçer. → **D1 iyi-retriever koşusu answer-anchored ile yapılacak; M3/empty-context zaten kötü-retriever/abstention ekseni.**
- **M1 çekinme teşhisi (30 flush, lexical proxy):** 6 abstain'in dağılımı → **3 HAKLI** (core_hard kötü soru↔madde eşleşmesi; ör. KMK Md4 "ortak yerler" ama soru "pay iptali"), **2 OVER-REFUSAL** (cevap kırpılmışta VAR, yine reddetti — TKHK Md47), **1 CLIP-KURBANI** (CMK 142, first-900 aptal-retriever'ın kaçırdığı; answer-anchored çözer). → clip baskın değil; asıl sinyaller over-refusal + benchmark kötü-eşleşme.
- **Açık iş (benchmark):** core_hard'ta gevşek/yanlış soru↔madde eşleşmeleri var (en az 3/6 abstain vakası) → core_hard pairing denetimi ayrı temizlik işi.
#### D1 canon eval — 6-mod matris SONUÇ (n=40/35/30, gpt-4o-mini hakem; detay [`v2b/sonuclar.md`](../v2b/sonuclar.md))
| Mod | Eksen | v2b | base | v1 |
|---|---|---|---|---|
| M1 gold+distractor | A1 (cevaplanan) | **0.904** | 0.879 | — |
| M2 TRAP (yanlış-kaynak oracle) | A3 Rej\* | 0.346 | 0.786 | 0.000 |
| **M2b distractor-only (training-matched)** | A3 Rej\* | **0.96** (n=30) | — | — |
| M3 boş-kaynak | A3 Rej\* | **1.000** | 1.000 | — |
| M4 temiz oracle | A1 | **0.975** | 0.977 | 0.960 |
| M5 KÖR (blind) | A2 | **0.175** [.075,.30] | 0.225 | 0.300 |
- **Manşet:** v2b **TÜM KAPILARI GEÇTİ** — grounding (M1 0.904 base'i geçti, M4 0.975 tavanda) + format (cit_prec 0.925-0.975) + abstention (adil M2b 0.96 + M3 1.000) + forgetting-yok (M5 base ile CI-örtüşük, replay tuttu).
- **⭐ Off-distribution dersi (methodology):** M2-oracle 0.346, v2b'yi **eğitilmediği tek-kaynak promptunda** ölçtü. **Training-matched M2b = 0.96** (v2b eğitim modu: çok-kaynak, gold yok→çekin). Deployment=RAG çok-kaynak → **0.96 ADİL A3**, 0.346 cross-mode artefakt. Abstention v1 0.000 → **0.96 dirildi**.
- **A1 çekinme-ayrımı (methodology):** çekinme faith=0 alıp micro'yu çeker (ham 0.737); ADR-0011 "A1=cevaplananlarda" → gerçek 0.904. M1'deki 7 çekinme = 5 haklı (3'ü benchmark kötü-eşleşme) + 2 over-refusal (%5).
- **K3 güncellemesi:** v1'in "abstention 0.000 çöküşü" v2b'de **büyük ölçüde düzeldi** (adil-mod M2b 0.96, boş M3 1.000) — LoRA+düşük-rank+replay+RAFT-abstain reçetesi ÇALIŞTI. Kalan: yalnız "yanlış-ama-makul TEK kaynak" (M2 0.346) = robustness, gate-fail değil → v2c'de TRAP-tipi abstain dilimi.
- **Product A teyidi (ADR-0012):** M4 oracle 0.975 vs M5 blind 0.175 = %80 uçurum → bilgi ağırlıkta değil RAG'de; FT davranış (grounding+abstention+format) öğretiyor, kanun gömmüyor.
- **Eval altyapısı:** `gen_eval_grounded --max-chunk-chars` (mirror) + `--no-gold` (M2b) · `score_abstention --source-field` eklendi.
- **v2c açık işler (tasarım notu `v2b/sonuclar.md` sonu):** TRAP-tipi abstain dilimi + anti-parametric-leak counterfactual (M2 param_leak %61.5) + GOLD-scrub (%5.7) + off-by-one atıf + core_hard kötü-eşleşme temizliği + register ekseni. TEK v2c FT.

---

