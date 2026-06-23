# V2_PLAN — HakHukuk v2 yön + deney planı

> **Bu dosya ne:** v2'nin **ileriye dönük execute planı** (ne yapacağız, neden, nasıl ölçeceğiz).
> Kanıt/sayılar `docs/record/research_log.md`'de (kronoloji), kararlar `docs/adr/`'de. Bu dosya = *plan*.
> **Dayanak:** CANON pilot base vs v1 (2026-06-13, `outputs/BENCHMARK_REPORT.md`) + 3 /deep-research
> (v2-teknik 24 kaynak · hukuk-veri 12 bulgu · FT-reçete 26 kaynak/21-doğru, 2026-06-14) + SaulLM okuması (`knowledge/summary_saullm.md`).
> **SEÇİLEN YÖL (2026-06-14, kullanıcı kararı):** **PLAN A = SFT (davranış) + RAG (bilgi, sonra)**, CPT'siz. Yön = **direkt v2b SFT** (v2a prompt-only baseline'a indi). SFT bilgi GÖMMEZ — daha *akıllı* değil daha *disiplinli* model. Bilgi/doğruluk RAG'dan; frontier'ı *grounded+abstention+offline* dar ekseninde yener (genel yetenekte değil).

---

## 1. Teşhis (pilot ne dedi)

| eksen (hücre) | base | v1 | okuma |
|---|---|---|---|
| CORE-KÖR A2 (ezberden bilgi) | 0.225 | 0.300 | ≈ eşit (CI çakışık) → FT kanun gömmüyor; ikisi de kötü |
| CORE-Oracle **A1∧A2** (doğru+dayanaklı) | **0.875** | 0.775 | **base > v1** — oracle'da bile v1 kötü |
| TRAP **A3** (abstention) | **0.741** | 0.000 | çöküş |
| TRAP-A2 (uydurmalar) | 0.114 | 0.114 | v1 uydurmaları %88 yanlış = halüsinasyon |
| A4 paren (format) | 0.025 | **0.975** | v1'in TEK kazanımı (kozmetik) |

## 2. Ana ders — literatürle DOĞRULANDI

- **SFT bilgi DEĞİL davranış öğretir** (LIMA Superficial-Alignment; Gekhman EMNLP24: yeni bilgi yavaş öğrenilir + halüsinasyonu lineer artırır; Mix-CPT). v1 0.000-abstention = full-FT'nin bilinen mekanik sonucu (SEAT/FLAME; "Confident Conflicts" → yıkıcı gradient).
- **base = güçlü okuyucu + kalibre model;** v1 onun gücünü dar format için takas etti.
- **Bilgi ≠ format ayrıştırılmalı:** bilgi → CPT veya RAG; SFT → yalnız format/davranış/abstention.

## 3. Karar: scope = PRODUCT A (ADR-0012)

Doğruluk **RAG'dan.** v2 = base'in gücünü KORU, yalnız 3 dar iş ekle: **(a) abstention-koru, (b) uzman-register, (c) atıf-format** — correctness'i BOZMADAN, kanun gömmeden.

## 3.1 SFT HEDEF TANIMI (ne öğretiyoruz)

**Tek cümle:** *"Verilen kaynaktan (RAG context) doğru maddeyi seç, distractor'ları yok say, ilgili span'i verbatim alıntıla, atıf formatıyla ver, gerekçelendir; kaynak yetersizse uydurma, çekin."* → model *"hukuku bilen"* değil *"kaynağı disiplinli okuyan + kalibre + çekinen okuyucu"* olur.

| # | Davranış hedefi | Canon ekseni | Kapı |
|---|---|---|---|
| 1 | **Grounding:** yalnız kaynaktan; distractor'ı yok say; ilgili span'i `##begin_quote##` verbatim alıntıla (RAFT) | A1 | A1∧A2 ≥0.875 |
| 2 | **Abstention:** kaynakta yoksa "maddede yok/yetersiz" de, uydurma (R-Tuning/CRaFT, veri-güdümlü) | A3 | ≥0.741 — **asıl kapı** |
| 3 | **Atıf formatı:** `(KANUN, Madde X)` tutarlı + CoT gerekçe | A4 | ≥0.9 |
| 4 | **Correctness koru:** base'in okuma/çıkarım gücü bozulmasın | A2 (KÖR+Oracle) | KÖR'ü geriletme |

**Hedef OLMAYANLAR (bilinçli dışarıda):**
- ❌ **Kanun bilgisini ezberletmek** — CPT'nin işi; v1 deneyip çöktü. SFT verisinde madde no/içerik her zaman prompt'taki kaynakta verili, ezber YOK.
- ❌ **Register'ı loss hedefi yapmak** — hiçbir FT yöntemi register'ı correctness kaybı olmadan kontrol edemiyor (v1'in "kısa-kesin koşul-atlama" hatası). Uzman register **prompt'ta** kalır; eğitim cevapları uzman tonunda yazılır ama optimize edilen sinyal correctness'tir.

## 3.2 DAVRANIŞ SPESİFİKASYONU — base vs SFT (gold-cevap şablonu)

> İllüstratif tasarım hedefi (ölçülmüş çıktı değil). Veri üretiminde gold-cevap deseni olarak kullan. base **kötü değil** (güçlü okuyucu+kalibre) ama **tutarsız**; SFT **disiplin** katar.

**S1 — Oracle mod (kaynak verili, cevaplanabilir).** Soru: maaş ödenmiyor, kıdem tazminatı? Kaynak: İş K. m.24 (gold) + 4 distractor.
- 🔵 base: doğru ama **atıfsız**, alıntısız, vatandaş-register, **kaynak-dışı tavsiye ekler** ("ihtarname çek").
- 🟢 SFT: gold'u distractor'dan **seçer** → CoT gerekçe → `##begin_quote##` **verbatim** → `(İş Kanunu, Madde 24/II-e)`; kaynak-dışı ekleme yok. → **A1+A4**.

**S2 — TRAP (gold madde YOK, sadece distractor). ASIL FARK.** Soru: komşu gürültüsü, kira feshi maddesi?
- 🔵 base: çoğu kez çekinir (A3≈0.74) **ama bazen parametrik hafızadan madde no uydurur** → tutarsız.
- 🟢 SFT: **"Verilen kaynaklarda bu hususu düzenleyen madde yok, atıf yapmam doğru olmaz."** → **A3** (v1 burada 0.74→0.00 çökmüştü; v2b amacı bu davranışı *tutarlı* kılmak). Frontier de tam burada zayıf.

**S3 — KÖR mod (hiç kaynak yok). İkisi de zayıf, farklı şekilde.** Soru: velayette çocuğun görüşü kaç yaşında, madde?
- 🔵 base: madde no **uydurma riski yüksek** (kör ~%25), kendinden emin yanlış olabilir.
- 🟢 SFT: **"Önümde doğrulayabileceğim kaynak yok; madde no'yu ezberden vermem hatalı olur."** → ezberden uydurmaz; doğruluğu artırmaz (bilgi yok) ama **kendinden emin yanlışı/halüsinasyonu önler**. Asıl çözüm RAG.

**Özet — SFT ne değiştirir:** distractor-ayırma (kayar→**seçer**) · atıf (tutarsız→**tutarlı**) · kaynak-yokken (bazen uydurur→**tutarlı çekinir**) · kaynak-dışı tavsiye (ekler→**eklemez**) · register (karışık→**uzman**) · **bilgi/kör doğruluk DEĞİŞMEZ (~%25)** çünkü bilgi RAG'dan. **SFT daha akıllı değil, daha disiplinli yapar — frontier'ın zayıf olduğu eksen tam bu.**

---

## 4. v2 KARAR AĞACI (kanıt-temelli, ucuzdan pahalıya)

> **NOT (2026-06-14 kararı):** kullanıcı **direkt v2b SFT** seçti. Aşağıdaki ağaçta v2a artık *birincil kapı değil* → ucuz **baseline/ablasyon** olarak tutuluyor (v2b'nin SFT katkısını izole etmek için "SFT'siz" referans). Birincil iş = **Adım 2 (v2b)**.

### Adım 0 — RAG corpus (asıl correctness mekanizması, her şartta)
Temiz statute/içtihat corpusu: **madde-bazlı chunk + atıf metadatası + değişiklik/mülga işleme** (Bedesten/Mevzuat). DISC-LawLLM (civil-law Çin) triplet deseni: kanun=büyük öncül, olay=küçük öncül, sonuç. *(Faz 2 RAG ile örtüşür.)*

### Adım 1 — v2a = base + PROMPT + RAG + selective-generation · **BASELINE/ABLASYON** ⚪ (artık birincil değil)
- **SFT YOK.** Mühendislik sistem promptu (yalnız kaynaktan cevapla; yoksa "maddede yok" de; "(KANUN, Madde X)"; uzman dili) + **Sufficient-Context selective-generation katmanı** (kalibre güven + "yeterli-bağlam" autorater → yönlendirilmiş abstention).
- Kanıt: Google ICLR25 — generator fine-tune ETMEDEN cevaplanan-doğruluk **+%2-10** (Gemma dahil). En ucuz, en yüksek kaldıraç. Yan-hasarsız.
- **Hipotez:** base zaten kalibre+okuyucu → prompt+selective-layer format+register+abstention'ı verir.
- → canon'dan geçir. v1'i döverse: **"SFT gereksiz" = dev bulgu.**

### Adım 2 — v2b = hafif RAFT-SFT · **BİRİNCİL İŞ** 🟢 (seçilen yol)
- **RAFT** (ICML24): gold+distractor doc → distractor'ı yok say, ilgili span'i **verbatim alıntıla**, CoT. param_leak + context-ignoring'i düzeltir; bilgi-gömme DEĞİL.
- **+ R-Tuning** knowledge-boundary refusal (doğru-bildiği→"eminim", yanlış→"emin değilim") — naive relabeling DEĞİL (→ over-refusal: static+dynamic conflict).
- **DENGE ZORUNLU:** hedge dilimi, **cevaplanabilir-bağlamlı dilimle** dengelenmeli — yalnız belirsizlik öğretmek known-accuracy'yi %52'ye çökertir (US-Tuning). *(Tek-kanonik-yüzde YOK; ilke = denge; oran ablasyonla.)*
- **Light-touch reg (kanıtlı çekirdek):** düşük LoRA rank / az epoch / replay-data-mixing. LoRA+replay → 0.000 değil (worst-case bounded). *(EAFT + KL-to-base KANITLANMADI → reçete dışı, ayrı ablasyon — §5.1-E.)*
- **Veri:** SaulLM 3-turn sentetik şablonu (gerçek doküman → çok-turlu instruction) + LLM-judge tercih çiftleri.
- **Register LOSS'A GİRMEZ** — prompt'ta kalır (hiçbir FT yöntemi register'ı correctness kaybı olmadan kontrol edemiyor; v1'in "kısa-kesin koşul-atlama" hatası tam bu).

### Adım 3 — v2c = sentetik CPT (EntiGraph) · OPSİYONEL/SONRA, bilgi kaldıracı 🔴
- **Sadece RAG bilgi-yeterliliğinde kanıtlanmış eksiklik varsa.** CPT, SFT'nin başaramadığı bilgiyi gömer (SaulLM +%7) ama o 54B/540B-token; bizde **EntiGraph** (Stanford ICLR25): küçük statute corpusunu çeşitli sentetik corpusa genişlet → CPT → RAG-lift'in >%80'i, **RAG ile BİRLEŞİR.**
- ⚠️ Ağır caveat: EntiGraph legal/Türkçe'de doğrulanmadı (extrapolation); naive CPT genel-reasoning'i bozar (Taiwan civil-law, Law-Neo) → **genel-veri karışımı şart.** Yüksek maliyet/risk. **Türkçe çapa: Mecellem 4-faz CPT** reçetesi (Qwen3-1.7B/4B, instruction değil CPT).

### DROP listesi (kanıtla elendi)
- **DPO "daha az yıkıcı" varsayımı** → çürüdü (forgetting-direnci on-policy RL/PPO'ya özgü; off-policy DPO miras almıyor). *(SaulLM DPO'yu ölçekte pipeline'ın 3. aşaması olarak kullanır — ama forgetting-fix diye değil.)*
- **Ağır bilgi-SFT** → belgelenmiş anti-pattern (strong base + RAG kurulumunda).

## 5. v2 veri tasarımı (v2b'ye gidersek)

- **Davranış-hedefli sentetik** (bilgi-ezber değil): gerçek madde → 3-turlu instruction (SaulLM şablonu) + abstention/hedge örnekleri (R-Tuning boundary) + uzman-register örnekleri.
- **RAFT formatı:** her örnekte gold madde + distractor maddeler, cevap verbatim-alıntılı + CoT.
- **Hedge dilimi VERİ-GÜDÜMLÜ** (keyfi % DEĞİL — §5.1-B): base'i prob et → bilmediği soru oranına eşle (R-Tuning/CRaFT), cevaplanabilir dilimle dengeli.
- **Kalite kapısı:** mevcut grounded üretim hattı + faithfulness doğrulama (v1'deki gibi, faith≥0.95).

## 5.1 v2b REÇETE KARTI (FT-reçete /deep-research, 2026-06-14, 26 kaynak / 21-doğru-4-çürük)

> Modal A100 · Gemma 4 12B · QLoRA. Her satır: değer + gerekçe + kaynak + ⚠️çelişki.
> **Çekirdek ders:** literatür "minimal-forgetting davranışsal SFT" için tam reçete VERMİYOR — yön net, kesin değerler **proje-içi sweep** gerektirir. v1 çöküşü (0.74→0.00) literatürde birebir var (Cor-RAIT over-refusal).

**A) Format (RAFT, 2403.10131)**
- `k=5`: örnek başına **1 gold + 4 distractor**; test-time aynı format.
- `P` (oracle'lı örnek oranı): **başlangıç %80**, ama EVRENSEL OPTİMUM DEĞİL (alan-bağımlı, 40–100% ölçülmüş) → **[60–100%] ablate**. `(1-P)` örnekleri SADECE distractor (oracle yok) → RAG performansını artırır.
- Cevap: `##begin_quote##` **verbatim alıntı** + CoT + `##Answer`.
- ⚠️ 4-distractor + %80, RAFT'ın İngilizce-QA setlerinden ekstrapolasyon; hukuk-RAG'da kanıtlı değil → ablate edilebilir.

**B) Abstention — EN KRİTİK (v1 çöküşü buradaydı)**
- Hedge oranı **SABİT DEĞİL** — keyfi %15/%25 **ÇÜRÜTÜLDÜ (1-2)**. → **VERİ-GÜDÜMLÜ:** modelin gerçekten bilmediği soru oranına eşle. R-Tuning (2311.09677): parametrik tahmin gold'la eşleşirse "eminim" (D1), yoksa "emin değilim" (D0). AfH (2312.07000): m=10 örnek, τ=0.1.
- **Naive correctness-only refusal (Cor-RAIT) = v1 çöküşünün birebir karşılığı:** over-refusal, known-acc %16–37 göreli düşer (TriviaQA 45→28.6, NQ 24.6→15.9). Sebep: static + dynamic conflict. → **KULLANMA.**
- Bunun yerine **CRaFT (AAAI25 / 2410.06913): certainty-aware etiketleme + high-certainty rehearsal** (zor-ama-bilinen sorularda over-refusal'ı önler).
- Hedge dilimi cevaplanabilir dilimle **DENGELİ**; **over-conservativeness ölç** = N7/(N1+N4+N7), honesty = ½(prudence + (1−over-consv)).
- ⚠️ "honesty-SFT accuracy'yi korur" garantisi **YOK (0-3 çürütüldü)** → A1∧A2 kapısını HER ablasyonda ölç.

**C) Forgetting kontrolü (QLoRA hiperparam)**
- **LoRA** (full-FT'den az unutur, ama sıfırlamaz) → **düşük rank + az epoch**. ⚠️ "LoRA explicit-reg'den güçlü" + "full-FT rank 10-100x mekanizması" **çürütüldü (0-3)** — LoRA'yı tek anti-forgetting mekanizması sayma, KL/replay ile birlikte.
- `target_modules = all-linear` (**MLP DAHİL**; attention-only zayıf: attn-r256 < MLP-r128). (Thinking Machines)
- `LoRA LR ≈ full-FT LR'nin 10x'i` (ör. full-FT ~1e-5 → LoRA ~1e-4). ⚠️ tek kaynak (TM blogu, peer-review değil); 15x "preliminary" → kendi LR sweep'inle teyit.
- Somut başlangıç (literatür tam vermiyor, **sweep şart**): `r=8/16`, `alpha=16/32`, `1 epoch`, `warmup %3-5`.
- 🚫 **AGRESİF LR (3e-4 re-warming) KULLANMA** — tam da v1 abstention çöküşü rejimi; o continual-PRETRAINING reçetesidir (2403.08763), davranışsal SFT'ye taşıma (2503.02844: re-warming forgetting'i artırır).

**D) Replay / data-mixing**
- Genel/instruction **replay karıştır: başlangıç %1–5** (ucuz; %1 bile forgetting'i belirgin azaltır, 2403.08763). Türkçe-hukuk register base'den uzaksa "güçlü shift" → %5'e yakın, gerekirse ↑%25.
- LoRA + replay → worst-case bounded (0.000 DEĞİL).
- ⚠️ Oranlar continual-PRETRAINING'den → **ALT-SINIR**; davranışsal SFT'de abstention çöküşü daha keskin olabilir.

**E) Reg eklentileri — KANITLANMADI (opsiyonel, deneysel)**
- **KL-to-base** ve **EAFT entropy-gating** (2601.02151): bu turda HİÇBİR claim destekledi (araştırma sorusu 5 **boşta**). Uygulanırsa dayanaksız-deneysel; reçeteye koyma, ayrı ablasyon yap.

**Birleşik sıra:** Tam birleşik etkileşim çalışması (RAFT+R-Tuning+replay+low-rank) **YOK**. En yakın kanıtlı çekirdek = **R-Tuning + CRaFT-düzeltme**. Kendi ablasyonunla doğrula.

**Açık (sweep/deney kapatır):** kesin r/alpha/epoch/warmup · P hukuk-RAG'da · Türkçe-hukuk shift gücü (replay %5 mi %25 mi) · KL/EAFT pratik etkisi.

## 5.2 v2b VERİ HAZIRLIK PİPELINE'I (2026-06-14 — kullanıcı sonra başlatacak)

**Girdi (HAZIR):** `data/raw/mevzuat_maddeler.jsonl` (40.496 madde = distractor havuzu + gold metin) · `data/processed/sft_v1/train.jsonl` (19.305 soru↔gold tohumu — **soruları al, v1 cevaplarını AT**: kaynaksız/vatandaş-register/CoT-quote yok).

```
Adım 1 — RAFT context paketle (her tohum için)
  · gold madde + 4 distractor örnekle
  · distractor = HARD-NEGATIVE (aynı kanun, komşu madde no) — gerçek retriever'ı taklit, rastgele değil
  · context = shuffle([gold] + 4 distractor)
  · dilime ata:  P% → gold context'TE (grounded)  |  (1-P)% → gold ÇIKARILMIŞ (abstention)
Adım 2 — Gold cevap üret (teacher-LLM + kapı) [API/Modal, ayrı]
  · grounded: (soru+gold) → CoT + ##begin_quote## [gold'dan birebir span] + ##Answer + (KANUN, m.X), uzman register
  · abstention: "Verilen kaynaklarda ... yok; atıf yapmam doğru olmaz" — çeşitli parafraz, uzman register (LLM-bilgisi GEREKMEZ)
Adım 3 — Kalite kapıları: verbatim-quote ⊂ gold (string) · faithfulness ≥0.95 (groundedness hakemi) · atıf madde_no==gold · dedup
Adım 4 — Replay karıştır (%1-5 genel TR instruction → forgetting'e karşı, §5.1-D)
Adım 5 — Split + chat-template + sistem promptu → data/processed/sft_v2b/{train,val,test}.jsonl  (gold madde_no'yu sakla → eval eşlemesi)
```

**Script:** Adım 1+3+4+5 = deterministik → `scripts/build_sft_v2b.py`. Adım 2 = teacher-LLM üretimi (ayrı, `gen_grounded.py` hattı uyarlanır).

**⚠️ HEDGE MEKANİZMASI DÜZELTİLDİ (önemli):** Önceki "base-prob (R-Tuning)" yaklaşımı **yanlış araçtı** — R-Tuning/CRaFT *closed-book parametrik* bilgi-sınırı içindir. Bizim model **RAG/context** üzerinde çalışıyor; istediğimiz abstention = **"verilen KAYNAKTA cevap var mı?"** (context-yeterliliği, **Sufficient-Context** 2411.06037), parametrik "biliyor muyum" değil. Bu **deterministik**: Adım 1'de gold'u koyup/çıkararak dilimi BİZ kontrol ediyoruz → **base-prob adımı İPTAL.** Sonuç: **"hedge oranı" = (1-P)** → RAFT'ın gold'suz dilimi = bizim abstention dilimimiz. İki karar tek knob'a indi: **P** (grounded:abstention; ~%80:20 başlangıç, [60-100%] ablate; deployment retrieval-miss oranını taklit etmeli). *(R-Tuning/CRaFT yalnız KÖR/E-set parametrik-kalibrasyon için ikincil kalır.)*

**Knob'lar (ablasyon):** P (grounded:abstention) · k (distractor sayısı/zorluk) · replay %.

---

## 6. Başarı kapıları (canon terimleriyle)

- **A3 rejection_rate ≥ base (0.741)** — abstention koru (asıl kapı).
- **A1∧A2 ≥ base (0.875)** — doğruluğu BOZMA.
- **A4 paren ≥ 0.9** — format koru. **CORE-KÖR A2'yi geriletme.**
- **+ Register sinyali** (önkoşul) · ikincil scaffold: **Muhakim** 5-boyut reward (statute-ref / legal-acc / case-law-ref / linguistic-coherence / depth) — bizim hakemle çapraz.

## 7. Önkoşullar (v2-eval'den ÖNCE inşa edilecek)

- [ ] 🔴 **Çok-chunk (distractor'lı) Oracle modu** — mevcut Oracle TEK temiz kaynak veriyor (`gen_eval_grounded.py --with-source` → sadece gold), distractor yok. SFT hedef #1 "distractor'ı yok say" (RAFT 1 gold+4 distractor) eğitiliyor ama ölçülmüyor; üstelik gerçek RAG çok-chunk gürültülü → mevcut eval **deployment'tan kolay/iyimser**. **Ekle:** RAFT-tarzı gold+distractor context modu → grounding'i gürültü altında ölç (A1). *(v2b eğitim dağılımıyla eval dağılımı eşleşsin.)*
- [ ] **Register/altitude ekseni** — "uzman mı vatandaş-basit mi" ölçen sinyal (yeni eksen / A4-altitude).
- [ ] **E (kaynak-eksik) eval seti** — TRAP=yanlış kaynak; E=hiç kaynak. v2 hedge'i ölçmek için; v2 hedge verisiyle birlikte kur.
- [ ] **v2a mühendislik promptu** + selective-generation katmanı (yazılıp iterate edilecek).
- [ ] (paper öncesi) G1 cross-family κ · paired McNemar · OOD dilimi · n=100/75.

## 8. Açık sorular (deneyle kapanır, planla değil)

- **Hedge dilimi nasıl belirlenir?** → ✅ ÇÖZÜLDÜ (§5.2): context-yeterliliği = deterministik = **(1-P)**; base-prob İPTAL. Geriye tek knob **P** kaldı (ablasyon, karar değil).
- **v2b canon'da base'i geçer mi?** (asıl kapı A3≥0.741 + A1∧A2≥0.875) → KOŞ. *(v2a = SFT'siz baseline referansı.)*
- **P optimumu** (grounded:abstention) hukuk-RAG'da kaç? → v2b ablasyonu [60-100%].
- **CPT (v2c) gerekli mi?** → ancak RAG bilgi-yetersizliği kanıtlanırsa; 12B/Türkçe'de ROI belirsiz. Karar = bütçe + RAG sonucu.

## 9. EXECUTION SIRASI (ne önce, neye bağlı)

> Durum: strateji+veri planı HAZIR (§1-8). Execution adım-0'da. Kullanıcı sonra başlatacak.
> 🔴 = bloke edici · 🟢 = paralel koşabilir · ⚪ = sonra/opsiyonel

```
A. EVAL ALTYAPISI (v2b'yi DOĞRU ölçmek için — eğitimden önce kurulmalı)
   A1 ✅ ADR-0013: canon eval v2 matrisi sabitlendi (5 mod × eksen)         [2026-06-14]
   A2 ✅ M1 distractor modu — gen_eval_grounded.py --distractors N (+ortak raft_pack.py)  [2026-06-14, paketleme doğrulandı; tam gen GPU ister]
   A3 ✅ M3 E-set — gen_eval_grounded.py --empty-context (boş bağlam→abstention)  [2026-06-14]
   A4 ✅ A-register — score_register.py (v1 leksik proxy; LLM-judge=TODO)    [2026-06-14, uzman/vatandaş ayrımı doğrulandı]

B. v2b VERİ (A'ya paralel; A2 ile AYNI raft_pack → dağılım eşleşir)
   B1 ✅ build_sft_v2b.py pack+assemble — Adım 1/3/4/5 (RAFT paketle + kapı + replay + split)  [2026-06-14, pack 19.305→80/20 + kapı doğrulandı]
   B2 🟡 Adım 2 — teacher-LLM cevap üretimi: SCRIPT HAZIR `gen_v2b_answers.py` (grounded→gpt-4o-mini, abstain→şablon). KOŞMAK = SEN (OPENAI_API_KEY, ~15K çağrı maliyet). abstain-yolu doğrulandı.
   B3 🟡 Kalite kapısı: deterministik kısım build_sft_v2b assemble'da ✅; faith≥0.95 LLM-judge AYRI (groundedness hattı)

C. EĞİTİM (B bitince)
   C1 🔴 Modal A100 QLoRA — reçete kartı (§5.1): r=8/16, all-linear, LoRA-LR≈10x, 1 epoch, replay, 3e-4 YASAK
   C2 ⚪ Ablasyon: P [60/80/100] · replay [%1/5] · rank [8/16]

D. DEĞERLENDİRME (A + C bitince)
   D1 🔴 canon koş (base / v1 / v2a-baseline / v2b) → bench_scorecard.py
   D2 🔴 Kapı kontrolü: A3≥0.741 · A1∧A2≥0.875 · A4≥0.9 · KÖR gerilemesin (§6)
   D3 🟢 Bulgu→research_log · karar→ADR

E. SONRASI (koşula bağlı)
   E1 ⚪ RAG corpus (Adım 0) — asıl correctness mekanizması (Faz 2 ile örtüşür)
   E2 ⚪ v2c sentetik-CPT — yalnız RAG bilgi-yetersizliği KANITLANIRSA
   E3 ⚪ Paper-grade: cross-family κ · McNemar · OOD · n=100/75 · rakip baseline
```

**Kritik yol:** `A1+A2 (eval) ∥ B1→B2→B3 (veri) → C1 (eğit) → D1→D2 (ölç)`. İlk başlatılacak: **A1 (ADR-0013) + B1 (build script)** — ikisi paralel, birbirini beklemez.

### Yol haritası ufku (OPSİYON — net karar DEĞİL)
İki ayrı hat: **ağırlık** (pretrain→SFT→RLHF, modeli değiştirir) · **sistem** (RAG = çalışma-anı sarmalayıcı, ağırlığa dokunmaz, dik). Olası sıra:
```
1. SFT   → davranış (grounding/abstention/format)          ← ŞİMDİ
2. RAG   → asıl correctness mekanizması (context verir)
3. RLHF  → model+RAG sistemini ince-ayar (OPSİYONEL/v3)     ← yalnız SFT+RAG platoya vurur + gösterilemeyen kalibrasyon açığı kalırsa
```
- **RLHF RAG'dan SONRA:** RAG-context'li promptlarla koşulmalı ki *deployment dağılımını* optimize etsin (context'siz = yanlış dünya).
- **Reward kaynağı (yazmaya gerek olmayabilir):** (a) **canon skorlayıcılarımız = doğrulanabilir ödül** (RLVR/GRPO — `groundedness.py`/`score_abstention.py`/`score_format.py` zaten kapıları kodluyor), (b) **Muhakim** hazır 5-boyut hukuk RM. Ayrı RM eğitimi şart değil.
- **on-policy PPO/GRPO'nun forgetting-direnci var** (DPO miras almıyor) → abstention korumada teorik artı. Ama ağır → Modal A100.

## İlgili
ADR-0011 (canon eval), ADR-0012 (scope A/B), ADR-0013 (eval v2 matrisi: 5 mod), ADR-0010 (reframe), `research_log.md` (pilot+araştırma girdileri), `outputs/BENCHMARK_REPORT.md`.
**Kaynak literatür:** Sufficient-Context (arXiv 2411.06037) · RAFT (2403.10131) · R-Tuning · US-Tuning · SEAT (2506.14387) · EAFT (2601.02151) · Gekhman (2405.05904) · Mix-CPT (2407.10804) · EntiGraph (2409.07431) · SaulLM (2403.03883 / 2407.19584) · DISC-LawLLM (2309.11325) · Mecellem (2601.16018) · Muhakim (HF newmindai/Muhakim).
