# v2c FIX — Deep Research (literatür temelli seçenek taraması)

> ❄️ **DONDURULDU (2026-07-05).** Bu tarama v2c RED'i sonrası fix seçeneklerini topladı; kararı
> **[[v3/recipe]]** (ORPO) verdi. Tarihsel referans — güncellenmez. Kronoloji: [[research_log/README]].

> **Amaç:** v2c'nin RED sebebi olan başarısızlığı (aşağıda "Teşhis") literatürle eşleştirip **fix seçeneklerini** kanıtlarıyla toplamak.
> **Not (kısıt):** Bu doküman **karar vermez** — sadece seçenekleri ve kanıtı sunar. Yeni iterasyon (v2d/v3) adı/kararı v2c ADR sürecinde, dış görüşler (bu tarama + Gemini) alındıktan sonra ayrıca verilecek.
> **Kaynak:** İç deep-research ajanı (WebSearch/WebFetch), 2026-07-03. Aşağıdaki tüm arXiv/venue referansları ajan tarafından toplandı.

---

## 🔷 GEMINI'YE BRIEF (bu bloğu Gemini'ye ver, sonra raporu tartış)

Türkçe hukuk alanında bir SLM eğitiyoruz: **Gemma 4 12B**, **QLoRA** (r=16, α=32), tek adapter, tek GPU (RTX 5070 Laptop, ~12GB) prototip / gerçek eğitim Modal A100. Faz 1 = fine-tuned + benchmark'lı taban model. Faz 2'de RAG gelecek (mevzuat kütüphanesi); yani **güncellik modelde değil, kütüphanede** olacak. Rakip: **Mecellem** (newmindai/Mecellem-Qwen3-4B-TR — sadece CPT, instruction-tuned değil, abstention/grounding mekanizması yok).

**Değerlendirme (6-mod kanon):**
- M1 = gold+distractor karışık bağlamda grounding (faithfulness)
- M2 = konusal KOMŞU ama YANLIŞ tek kaynak, gold yok → doğru davranış = **abstain** (wrong-source abstention)
- M2b = bariz ALAKASIZ distractor, gold yok → doğru davranış = abstain (RAG-miss)
- M3 = boş bağlam → abstain
- M4 = tek temiz gold (oracle grounding)
- M5 = bağlamsız blind (parametrik doğruluk — bizim için **anti-hedef**, RAG modeli olduğumuz için düşük olması iyi)
- A1 = cevaplanan-satırlarda faithfulness (abstain'ler ayrılır); "A1 @ coverage%" olarak raporlanır.
- A4 = atıf-format doğruluğu.

**v2c SONUÇLARI (RED):**
| Mod | v2c | Kapı | Durum |
|---|---|---|---|
| M1 A1 (grounding) | 0.832 @ %80 cov | ≥0.904 (regresyon) | ❌ |
| M4 A1 (oracle) | 0.977 @ %100 | — | ✅ |
| M2b (RAG-miss abstain) | 0.973 | — | ✅ |
| **M2 (wrong-source abstain)** | **0.407** | ≥0.90 (üstünlük) | ❌ |
| M3 (empty abstain) | 1.000 | — | ✅ |
| Register | 1.0 (expert) | — | ✅ |

**TEŞHİS (K3 negatif bulgu):** SFT modele **coverage** kazandırdı (soruları daha çok yanıtlıyor: base %47.5 → v2b %72.5 → v2c %80; over-refusal düştü = iyi) ama **discrimination** kaybettirdi. Bariz-alakasız kaynağı reddediyor (M2b ✅ 0.973) ama **konusal-komşu-ama-yanlış** tek kaynağa (M2) "yapışıp" cevap uyduruyor (27 geçerli trap'in 16'sında fabricate). Örnek: "Pilot uygulama ne zaman başlayacak?" → alakasız 4320 sK'den uyduruyor; "Başkasının ormanına girebilir miyim?" → TMK 752'yi aşırı-genelliyor. Ucuz SFT counterfactual (birkaç %) bu ayrımı öğretmeye yetmedi → §3-E hipotezi ("ucuz SFT counterfactual yeter") ÇÜRÜDÜ.

**Gemini'ye soru:** Aşağıdaki 5 fix ailesinden, *coverage'ı düşürmeden near-miss discrimination'ı geri getirmek* için **QLoRA/tek-adapter/tek-GPU** bütçesinde hangisi(leri) en makul? Veri-kompozisyonu (near-miss oranı) hakkında ne önerirsin? Gözden kaçırdığımız bir aile/risk var mı?

---

## Teşhisin literatürdeki yeri

Çekirdek olgu literatürde iyi tanınıyor: **RAG/SFT "coverage kazandırır ama abstention'ı bozar"**, ve **plausibly-adjacent-wrong (near-miss) bağlam** en zor sınıf. Aşağıdaki 5 aile bu ekseni farklı açılardan hedefliyor.

---

## Aile 1 — Preference optimization on hard negatives (ORPO / DPO / KTO)

**(a) Fikir.** "Yanlış-kaynağa-cevap" = rejected, "abstain/IDK" = chosen çiftlerinde tercih optimizasyonu. ORPO tek aşamada (SFT+pref, reference-model'siz); DPO iki aşama + referans modeli; KTO çiftlenmemiş binary sinyalle.

**(b) Makaleler.**
- ORPO — *Monolithic Preference Optimization without Reference Model*, Hong et al., arXiv:2403.07691 (2024).
- DPO — Rafailov et al., NeurIPS 2023, arXiv:2305.18290.
- KTO — *Model Alignment as Prospect Theoretic Optimization*, Ethayarajh et al., arXiv:2402.01306.

**(c) Kanıt.** ORPO: log-odds-ratio terimi rejected'a zayıf ceza, chosen'a güçlü uyum → SFT sinyalini (coverage) korurken ayrım açar (SFT+ayrım tek geçiş). KTO: binary sinyalle 1B–30B'de DPO'yu eşliyor/aşıyor, **imbalanced/azaltılmış veriye dayanıklı** (az abstain-pozitif olan hukuki veriye uygun). Uyarı: *Leveraging RAG for Training-Free Alignment* (arXiv:2605.11217) — ham DPO refusal'ı iyileştiriyor ama **sınırlı (~%87 strict-refusal)**; tek başına near-miss'i garanti kapatmıyor.

**(d) QLoRA uyumu.** ORPO en uygun: **ref-model yok** → tek forward, minimal VRAM, SFT+pref tek adapter. DPO ref-model ister (bellek+pass). KTO veri toplama en ucuz (çiftlenmemiş).

**(e) Risk.** Tercih çifti kalitesi kritik; rejected="fabricate-from-wrong-chunk" örnekleri **M2-tipi near-miss dağılımından** üretilmezse yine sadece off-topic öğrenir. Format-bias riski (*From Lists to Emojis*, arXiv:2409.11704).

---

## Aile 2 — Retrieval-token / context-loss masking (RAFT)

**(a) Fikir.** golden+distractor karışımıyla eğit; cevabı yalnız golden'dan üret, alıntıyı verbatim işaretle (`##begin_quote##`), CoT gerekçe; bir kısım örnekte golden'ı çıkar.

**(b) Makale.** *RAFT: Adapting LM to Domain Specific RAG*, Zhang et al., arXiv:2403.10131 (2024).

**(c) Kanıt + KRİTİK SINIR.** Recipe: **1 golden + 4 distractor**, golden-çıkarma fraksiyonu P (optimal 40–100 arası; P=80% RAG'i iyileştiriyor). Kazanç: HotpotQA %6.38→**%35.28**, PubMed %59.7→**%73.3**. **AMA (senin failure'ınla birebir):** RAFT golden yokken **abstain ÖĞRETMİYOR**, tersine "golden'ı çıkararak cevabı *ezberlemeye* zorluyoruz" (§3). Yani no-golden kolu = parametrik ezber, abstain değil → M2'deki "plausible chunk'a yapış, uydur" davranışını **besleyebilir**. DTA (Aile 5) de bunu bağımsız doğruluyor: "RAFT tamamen gürültülü bağlamda bile cevap vermeye koşulluyor, açıkça prompt'lansa bile IDK diyemiyor."

**(d) QLoRA uyumu.** Yüksek (saf SFT, ekstra bellek yok). Loss-masking de SFT-loss düzeyinde → uyumlu.

**(e) Risk.** **Abstention'ı doğrudan çözmez** → near-miss için ek abstain-kolu şart. Format ezberi (quote sözdizimi).

---

## Aile 3 — Abstention / calibration (R-Tuning, Sufficient-Context)

**(a) Fikir.** Bilinen/bilinmeyen sınırını veriden çıkar; certain→cevapla, uncertain→"bilmiyorum"; refusal'ı meta-beceri yap.

**(b) Makaleler.**
- R-Tuning — *Instructing LLMs to Say 'I Don't Know'*, Zhang et al., NAACL 2024, arXiv:2311.09677.
- *Sufficient Context: A New Lens on RAG*, Joren et al., ICLR 2025, arXiv:2411.06037.

**(c) Kanıt.** R-Tuning: certain'e "I am sure", uncertain'e GT+"I am unsure". Unanswerable'da refusal **%87–99** (vanilla ~0), **answerable'da coverage/accuracy korunuyor** → coverage-düşürmeden-discrimination-kazanç doğrudan kanıtı. Sınır: odak **parametrik** bilgi sınırı; retrieval near-miss'i (M2) dolaylı. Sufficient-Context: ölçüm "relevant" değil "yeterli bilgi var mı" ekseninde; bulgu birebir bizim: **"RAG paradoksal olarak abstain'i düşürüyor"**, açık-kaynak modeller (**Gemma** dahil) yeterli bağlamda bile halüsine/abstain ediyor. Sufficient-context sinyaliyle guided-abstention aynı coverage'da **selective-accuracy +2–10 puan**.

**(d) QLoRA uyumu.** R-Tuning saf SFT → çok uygun, sıfır ekstra bellek. Sufficient-Context = sinyal/kılavuz (ek yeterlilik-sınıflandırıcı / self-confidence) → hafif ek bileşen.

**(e) Risk.** "certain/uncertain" etiketini **domainde** doğru üretmek gerek; near-miss'i "uncertain"e koymazsan kaçırır. Over-refusal (coverage↓) riski düşük raporlanmış ama domain-shift'te değişebilir.

---

## Aile 4 — Contrastive / hard-negative SFT (RAAT, CaRT)

**(a) Fikir.** Rastgele negatif zayıf gradyan; **hard/near-miss negatif** (konusal komşu-yanlış chunk) ile eğit. Counterfactual minimal-pair: tek fark = gerekli bilginin var/yok olması → nedensel sinyali izole et.

**(b) Makaleler.**
- RAAT — *Enhancing Noise Robustness of RALMs with Adaptive Adversarial Training*, Fang et al., ACL 2024, arXiv:2405.20978.
- CaRT — *Teaching LLM Agents to Know When They Know Enough*, arXiv:2510.08517 (2025).
- (destek) *Long-Context LLMs Meet RAG* arXiv:2410.05983; *Hard Negative Mining for Domain-Specific Retrieval* arXiv:2505.18366.

**(c) Kanıt.** RAAT: gürültüyü **üç sınıf** (relevant/irrelevant/**counterfactual**) + **multi-class auxiliary head** → model gürültüyü içeriden tanır; adaptif adversarial. LLaMA-2-7B'de gürültülü koşulda **+2.1 F1 / +2.5 EM**. "counterfactual" sınıfı = M2 near-miss'ine en yakın. CaRT: terminate/answer'ı **flip eden** minimal-counterfactual çiftleri + preference-contrastive → **coverage'ı çökertmeden** should-answer vs should-abstain ayrımını iyileştiriyor. Ölçek bulgusu: **model büyütmek abstention'ı tutarlı iyileştirmiyor; abstain→yanlış kayışı, doğru→yanlış kayışından daha zor düzeliyor** → çözüm **veri-kompozisyonunda**, parametre sayısında değil. Evrensel "kaç kat negatif" eğrisi yok (çıpalar: RAFT 1:4, RAAT 3-sınıf denge).

**(d) QLoRA uyumu.** Contrastive/hard-neg SFT → uygun. RAAT aux-head = küçük ek (LoRA+küçük kafa). CaRT preference tabanlı → Aile 1 altyapısını paylaşır.

**(e) Risk.** **En yüksek veri-mühendisliği maliyeti** (near-miss chunk'ı retriever'la sistematik madenlemek). Yanlış kurulan "kolay" negatiflerle mevcut durumu (off-topic çözülür, near-miss çözülmez) tekrar üretme riski birebir burada.

---

## Aile 5 — Knowledge-boundary preference (DTA / RPO) — failure'ı isim isim tarif eden aile

**(a) Fikir.** RAG'i iki eksende dörde böl: parametrik-sınır (KB_param) × retrieval-sınır (KB_r). Her kadran için özel tercih çiftleri, DPO ile hizala. İkisinin de dışında → IDK chosen, GT dahil tüm cevaplar rejected.

**(b) Makaleler.**
- DTA — *Divide-Then-Align: Honest Alignment based on the Knowledge Boundary of RAG*, Xie et al., **ACL 2025 Main**, arXiv:2505.20871 · kod: github.com/JiananXie/Divide-Then-Align
- RPO — *Retrieval Preference Optimization for Robust RAG*, Yan et al., ACL 2025, arXiv:2501.13726.

**(c) Kanıt (en güçlü, birebir eksende).** DTA dört kadran: **✔✘ kadranı** (parametrik bilir ama retrieval yanlış) → rejected'a hem "noisy bağlamdan yanlış cevap (WA1)" hem "aşırı-muhafazakâr IDK" → **near-miss-wrong'a-yapışma tam WA1 olarak cezalanıyor**; ✘✘'de GT bile rejected (over-coverage kırılır). Sayılar (LLaMA-2-7B): Accuracy **42.2→64.1**, **Abstain-F1 0.0→63.3**, Precision 42.2→65.5 → abstention'ı sıfırdan kazanırken accuracy de yükseliyor (trade-off'u çözen en net tablo). Loss: **L = L_DPO + β·L_SFT + γ·L_class** (SFT=coverage koru, DPO=ayrım aç, class=kadran öğret). Veri: 10k tercih (2.5k–10k ablasyon). **Uyarı:** DTA golden-olmayanı **tek tip** işliyor → M2b(off-topic)/M2(near-miss) ayrımını otomatik yapmaz; kadran verisini **kendi near-miss dağılımınla** doldurmalısın. RPO: retrieval-relevance'ı **örtük reward'a** gömüp tek modelde değerlendirme+üretim → ayrı "bağlam kaliteli mi" adımı gerekmez (tek-adapter için mimari olarak ilginç).

**(d) QLoRA uyumu.** DTA = DPO tabanlı → ref-model yükü (Aile 1 DPO gibi); ama SFT terimi içinde → ayrı SFT aşaması gerekmez, tek adapter mümkün. RPO örtük-reward → ekstra reward-model VRAM'i yok.

**(e) Risk.** Yüksek veri-mühendisliği (kadran etiketleme: her örnek parametrik-bilir-mi + retrieval-yeterli-mi çift-etiketi). Near-miss açıkça modellenmezse DTA da genel-negatif davranışına kayar.

---

## Ek — Rakip (Mecellem) bağlamı

- **Mecellem** (arXiv:2601.16018): paper'da **grounding/abstention/refusal/hallucination için hiçbir mekanizma yok.** Decoder'lar (Qwen3-1.7B/4B) **yalnız CPT** (4-faz curriculum), **instruction-tuned değil, DPO/RLHF yok.** Muhakim (ArmoRM-Turkish-Legal) sadece **değerlendirme reward modeli**; eğitimde tercih-opt için kullanılmıyor. Değerlendirme retrieval-metrik+perplexity ağırlıklı; **source-faithfulness / yanlış-bağlamdan-cevap ölçümü yok.** → abstention/near-miss discrimination Mecellem'in **boş bıraktığı eksen**; differansiyel avantaj alanı açık.
- *Benchmarking Source-Sensitive Reasoning in Turkish under Evidential Trust Manipulation* (arXiv:2604.24665): Türkçe modeller (Gemma-3-27B dahil) kaynak-güvenilirliğine göre davranış ayarlamada **near-chance (~%50–58)** → "plausible-wrong kaynağa yapışma" gözlemimizle aynı aile.

---

## KARŞILAŞTIRMA TABLOSU

| Aile | Coverage-koruma | Discrimination (near-miss) | QLoRA/tek-GPU | Veri-maliyeti | Kanıt-gücü |
|---|---|---|---|---|---|
| **1. Pref-opt (ORPO/DPO/KTO)** | Yüksek (ORPO SFT-içi; KTO imbalanced-dayanıklı) | Orta-Yüksek (çift kalitesi) | ORPO/KTO çok yüksek (ref-yok); DPO orta | Orta | Orta (DPO tek başına ~%87 sınırlı) |
| **2. RAFT + loss-mask** | Yüksek (saf SFT) | **Düşük** (no-golden'ı ezber öğretir) | Çok yüksek | Orta | Yüksek robustness, **abstention için negatif** |
| **3. R-Tuning / Suff-Ctx** | **Yüksek** (answerable korunur; +2–10) | Orta-Yüksek (parametrik-odak; retrieval dolaylı) | R-Tuning çok yüksek | Düşük-Orta | Yüksek (coverage-koru+refusal doğrudan) |
| **4. Contrastive (RAAT/CaRT)** | Orta-Yüksek (CaRT koruyor) | **Yüksek** (counterfactual ayrı sınıf/flip) | Yüksek (aux-head küçük) | **Yüksek** (near-miss madenleme) | Yüksek; ölçek eğrisi net değil |
| **5. Knowledge-boundary (DTA/RPO)** | **Yüksek** (L_SFT; Acc 42→64) | **En yüksek** (WA1 cezası; Abstain-F1 0→63) | Orta (DTA=DPO ref; RPO örtük) | **Yüksek** (çift-eksen kadran) | **En güçlü** (failure'ı isim isim; ACL 2025) |

---

## AÇIK SORULAR

1. **Near-miss ≠ off-topic:** DTA/RAFT golden-olmayanı tek-tip işliyor; M2(near-miss)/M2b(off-topic) ayrımını hiçbiri *otomatik* çözmüyor → hepsinde **negatif/kadran verisini kendi near-miss dağılımınla doldurmak** gerekiyor. Evrensel "kaç % near-miss" yok (çıpalar: RAFT 1:4, RAAT 3-sınıf, DTA 10k/4-kadran).
2. **Ölçek eğrisi belirsiz:** "kaç kat counterfactual" için net scaling-curve yok; tersine — **model büyütmek abstention'ı iyileştirmiyor** → çözüm veri-kompozisyonunda.
3. **Gemma-özel:** Sufficient-Context, Gemma dahil açık modellerin "yeterli bağlamda bile halüsine/abstain" eğilimini raporluyor → Gemma 4 12B'de over-refusal↔over-answer dengesi ampirik açık.
4. **DPO ref-maliyeti vs ORPO:** DTA'nın DPO+SFT+class kaybı QLoRA tek-adapter+12GB'de ref-model belleğiyle sığar mı, yoksa ORPO-benzeri ref-free varyanta uyarlanmalı mı? (DTA'nın ref-free versiyonu literatürde yok.)
5. **Format-ezberi:** RAFT (quote), R-Tuning ("sure/unsure"), abstain-metni → biçim-bias'ına (arXiv:2409.11704) açık; ayrımın "kaynak-yeterliliği"nden mi yüzeysel biçimden mi öğrenildiği ölçülmeli.

---

## Kaynaklar
ORPO 2403.07691 · DPO 2305.18290 · KTO 2402.01306 · RAFT 2403.10131 · R-Tuning 2311.09677 · Sufficient-Context 2411.06037 · RAAT 2405.20978 · CaRT 2510.08517 · DTA 2505.20871 (kod: github.com/JiananXie/Divide-Then-Align) · RPO 2501.13726 · RAG training-free alignment 2605.11217 · Mecellem 2601.16018 · Turkish Source-Sensitive 2604.24665 · Format-bias 2409.11704

---

## Dış görüş 2 (Gemini) — işlendi 2026-07-03

> Gemini'ye yukarıdaki "GEMINI'YE BRIEF" bloğu verildi. Aşağıda **işe yarar sentez** + **ayıklanan gürültü/hatalar** ayrı.
> ⚠️ **KARAR NOTU:** Gemini raporu bir 3-adımlı hibrit stratejiyi "kararlaştırılmıştır" diye sundu. **Biz bunu KARAR olarak ALMIYORUZ** (kullanıcı kısıtı: yeni iterasyon kararını verme). Aşağıdaki hibrit = güçlü bir **seçenek/öneri**, ADR-0014'teki P1–P6 havuzuna girdi; seçim ayrı ADR'de.

### ✅ Gemini'nin değerli kattığı (bizim taramamızın üstüne)
1. **Fizibilite kaldıracı — lokal vs bulut ayrımı:** DTA (DPO tabanlı) **aktif + referans modeli aynı anda** yükler → **12B @ 12GB lokal RTX 5070'de OOM.** ORPO ref-model'siz → lokalde sığar. Sonuç: **ORPO = lokal prototip, DTA = Modal A100** doğal iş bölümü. (Bizim taramada "DTA ref-yükü" vardı ama bu lokal-OOM/A100-ayrımı Gemini'nin net katkısı.)
2. **3-adımlı hibrit sentez (SEÇENEK, karar değil):**
   - **Adım 1 — Veri:** M2 tuzakları için **minimal-çift** set: (doğru bağlam→atıflı doğru yanıt) ∥ (yakın/yanlış bağlam→"bilgi yetersiz, çekimserim").
   - **Adım 2 — Lokal ORPO:** chosen="çekimserim", rejected="yanlış-belgeden-uydurulan cevap" → ref-free, RTX 5070'de prototip.
   - **Adım 3 — Modal DTA:** 4-kadran DPO ile A100'de sıkılaştır (parametrik ezberi maskele, RAG'e mutlak sadakat).
   - → Bu, bizim P1(ORPO)+P2(DTA)'yı **veri-paylaşımlı boru hattı** olarak birleştiriyor; makul ama **maliyeti/gerekliliği kanıtlanmadı** (iki-aşamalı FT = iki tur maliyet).
3. **Doğrulanan örtüşme:** Gemini bağımsızca aynı sonuca vardı — RAFT'ın no-golden kolu ezber öğretir (bizim sorunu besler); çözüm parametre değil **veri-kompozisyonu** (minimal-çift yoğunluğu); Mecellem'in abstention mekanizması yok → differansiyel-avantaj alanı.

### ⚠️ Ayıklanan gürültü / hatalar (Gemini halüsinasyonu — KULLANMA)
1. **Baştaki koca "v2c=SNMPv2c / Sentinel LDK şifreli .v2c / Verilog-to-C / 20CRv2c" bölümü = TAM HALÜSİNASYON.** Gemini "v2c" string'ini alakasız ürünlerle eşleştirmiş. Bizim v2c = "Version 2, Revision C", o kadar. "Tescilli/şifreli/kapalı-kaynak lisans dosyası" analojisi **anlamsız** (repo private olması ayrı mesele; SNMP/Sentinel benzetmesi sıfır bilgi taşıyor).
2. **İsim hatası: "DTA = Domain-Targeted Alignment" YANLIŞ.** Doğru: **DTA = Divide-Then-Align** (Xie et al., ACL 2025, arXiv:2505.20871). Gemini açılımı uydurmuş. Kadran mantığı doğru aktarılmış ama isim yanlış.
3. **"kararlaştırılmıştır" dili:** Gemini kendi önerisini verilmiş-karar gibi yazdı. Değil. Bizde karar açık (ADR-0014).
4. **Sayı teyidi:** Gemini'nin skor tablosu bizim gerçek skorkartla tutarlı (M2 0.407, M1 0.832, M2b 0.973 vb.) — brief'i doğru okumuş; ek/uydurma sayı yok. ✅

### Net çıkarım (iki dış görüş + iç tarama ortak paydası — yine KARAR DEĞİL)
- **near-miss abstention'ın kaldıracı = veri-kompozisyonu** (kendi M2-near-miss negatif dağılımın), salt-algoritma değil — üç kaynak da hemfikir.
- **ORPO (lokal, ref-free) ↔ DTA (A100, knowledge-boundary)** en çok öne çıkan iki yöntem; hibrit boru hattı mümkün ama iki-tur-maliyet açık soru.
- **RAFT tek başına eleniyor** (no-golden ezber riski), P4/P5 destek-rol.
- Bunların hepsi ADR-0014 P1–P6'ya işlendi; **seçim + ikinci deep-research (istenirse) sonraki tur.**
