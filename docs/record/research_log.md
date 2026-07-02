# HakHukuk — Araştırma Kaydı (kronolojik)

> **Bu dosya ne:** Projenin **deney günlüğü** — ne yaptık, ne çıktı, ne karar verdik, paper'ın hangi
> bölümüne yarar. Tek dosya, kronolojik, **paper/rapor hammaddesi.** ADR'ler *kararı* tutar; bu dosya
> *anlatıyı + sayıları + öğrenilen dersi* tutar. Yeni anlamlı deney/bulgu → buraya bir girdi.
>
> **Paper haritası:** K1=ablasyon (base→+SFT→+madde-verili/oracle), K3=ayrışma bulguları (beklenmedik negatif sonuçlar).
> Detaylı hedef: `docs/PAPER_TARGET.md`. Kararlar: `docs/adr/`.

---

## Künye
- **Model:** Gemma 4 12B (`gemma-4-12B-it-qat-q4_0-unquantized`) + QLoRA → (Faz 3) Q4_0 GGUF.
- **Ana metrik:** groundedness — FactScore (claim böl→doğrula) + ALCE (atıf prec/recall, wrong_ref), `scripts/groundedness.py`. Hakem: gpt-4o-mini (paper'da cross-judge gpt-4o).
- **Eğitim yeri:** Modal A100. **Eval:** lokal ($0, OpenAI hakem).
- **Birincil kitle (2026-06-13 reframe):** UZMAN (avukat/hukukçu). Vatandaş = app-layer ikinci register.
- **Eval modları (terim — 2026-06-13 düzeltildi):** **KÖR** = madde prompt'ta yok, model ezberden cevaplar (parametrik bilgi testi). **MADDE-VERİLİ (oracle-context)** = doğru maddenin metni `--with-source` ile ELLE prompt'a konur. ⚠️ Bu **gerçek RAG DEĞİL** — retriever/DB yok (henüz). "Mükemmel getirme" simülasyonu, yani gerçek RAG'ın **iyimser tavanı** (gerçek retriever yanlış/eksik getirir → skorlar bundan düşük olur). Eskiden "RAG modu" deniyordu; yanıltıcı olduğu için "madde-verili" olarak yeniden adlandırıldı. Yalnız "Faz 2 RAG" ibareleri gelecekteki gerçek retriever sistemini kasteder.

---

## Zaman çizelgesi

### ~2026-05/06 — Çerçeve + planlama
- Private repo + proprietary lisans (ADR-0007). Base = Gemma 4 12B (ADR-0003). Eğitim = Modal A100 (ADR-0004).
- Veri kuralı: yalnız güncel TC mevzuatı; Lexpera/Kazancı ASLA. EDA-doğrula (newmindai/EuroHPC reddedildi — çöp). (ADR-0005)
- Akademik hedef: niş + sistem paper'ı (ADR-0006), `docs/PAPER_TARGET.md`.

### 2026-06-07/08 — v0 (forum verisi) → BAŞARISIZ
- **Veri:** `data/processed/sft_v0/` — 29K, `turkish_law_qa_dataset` + `turkish-law-chatbot` (forum).
- **Sonuç:** modeli batırdı (base-altı doğruluk).
- **Post-mortem (2026-06-13 kanıtlandı):** "7 Kasım 1982'de yürürlüğe girmiştir." cevabı **154 farklı soruya birebir** yapıştırılmış; atıf oranı düşük (~%13.6 sıkı ölçüt). → forum verisi sistemik kirli.
- **Ders (paper K3 adayı):** kaynaksız QA verisi doğruluğu öğretmez, halüsinasyon hattı ezberletir.

### 2026-06-08 — Grounded pivot → v1 verisi + kalite kapısı
- **Hamle:** doğruluğu **gerçek kanun maddesinden imal et** (madde → GPT-4o-mini Q&A üretir → doğrula).
- **Veri:** `data/processed/sft_v1/` — **21.458 grounded Q&A** (train 19.305 / val 1.131 / test 1.022), ~$1.16. Kaynak = 2.759 madde, **10 çekirdek kanun** (TMK,TBK,İİK,İş,TKHK,Aile,HMK,KatMülk,TCK,CMK). Üslup: **kısa, sade, vatandaş** (üretim promptu öyle diyor). 32K forum KATILMADI.
- **Filtre:** `gen_grounded.py::usable()` ham 40K'dan değişiklik/stub/mülga maddelerini eler (40K→21K→çekirdek 2.759).
- **Eğitim-öncesi kalite kapısı (ADR-0002):** `score_grounded_corpus.py`, n=40 → **faithfulness 0.984**, hall 0.016, cit_precision 1.0, wrong_ref 0.0. → veri temiz.

### 2026-06-09 — v1 SFT eğitimi (Modal A100)
- 1 epoch, 1207 step, ~3.5h ≈ ~$10. **Başlatma dersi (ADR-0008):** `modal run --detach ...::spawn_train` (fire-and-forget); `train.remote` client'a bağlı bekler → WSL kapanınca cancel → job ölür (4 kez yandı). Çözüm: `spawn()`.
- Adapter → `outputs/v1/` (checkpoint-1207).

### 2026-06-12 — Dış v2-analiz raporu değerlendirildi → ADR-0009
- Rapor "filtre gevşek, %3 değişiklik dili kaçıyor, fix=STUB'ı gövdeye yay" dedi.
- **Gerçek `usable()` import edilip 40K'da koşuldu → iddia FABRİKASYON** (AMEND/STUB zaten tüm gövdede; kaçak %0). Fix no-op. Filtreye DOKUNULMADI.
- Yan ürün: `outputs/eval/v1_suspect_sources.json` (404 şüpheli kaynak: 341 kısa + 65 mülga-gövde) → hedefli v1-audit için.
- **Ders (paper Methodology):** bir agent "çalıştırıp ölçtüm" dese bile gerçek modülü import edip doğrula.

### 2026-06-13 — ⭐ base vs v1 eval: KÖR vs MADDE-VERİLİ (asıl bulgu)
**Kurulum:** `gen_eval_grounded.py` — model soruyu cevaplar, gerçek madde **referans** (yer-gerçeği) olarak skorlanır. İki mod: KÖR (madde prompt'ta yok, parametrik) / MADDE-VERİLİ (oracle-context, `--with-source`, etiketli madde ELLE prompt'a konur — gerçek RAG/retriever DEĞİL). n=20, gpt-4o-mini hakem.
> ⚠️ **Kaynak dosyaları silindi (2026-06-13 akşam):** bu n=20 keşif koşusunun detay/skor dosyaları (`eval_*`, `rag_*`, `ragL_*`) eval/ temizliğinde KESİN SİLİNDİ. Sayılar yalnız bu tabloda kayıtlı. Yerine **akşam n=40 KÖR + oracle benchmark** geçer (daha temiz, dosyaları duruyor).

| metrik | KÖR base | KÖR v1 | madde-verili base | madde-verili v1 |
|---|---|---|---|---|
| faithfulness | 0.571 | 0.520 | **0.980** | **0.971** |
| hallucination | 0.429 | 0.480 | 0.020 | 0.029 |
| cit_precision | 0.833 | 0.200 | 0.950 | 0.850 |
| wrong_ref | 0.125 | 0.800 | 0.050 | 0.150 |
| cit_recall | 0.900 | 0.450 | 1.000 | 0.900 |

**Bulgular:**
1. **KÖR test yanıltıcıydı.** Madde verilince faithfulness 0.52→0.97, halüsinasyon 0.48→0.03. v1'in "felaketi" (KÖR wrong_ref 0.80) **test artefaktı** — model ezberden madde no uyduruyordu.
2. **Etiket hatası:** madde-verili modda madde *metni* verilip *etiketi* (Kanun+no) verilmeyince model numarayı yine uydurdu. Etiket eklenince (`ragL`) atıflar düzeldi. → **Faz 2 RAG dersi (gerçek retriever): getirilen chunk atıf metadatasını taşımalı.**
3. **Madde-verili modda v1 ≈ base** (faith 0.971 vs 0.980; v1 cit_precision 0.85 < base 0.95). **SFT ana metrikte base'i GEÇMEDİ, atıfta hafif geriletti.**

**Reframe (bugün netleşti):** birincil kitle = uzman; doğruluk RAG'dan; sadelik app-layer. → "v1 kısa/sade" satış noktası değil.

**Strateji kararı (subagent analizi):** v1'i **eğitim hedefi olarak reddet**, grounding altyapısını koru → **dar v2** kur:
- **Madde-verili modda** eğit (deploy'da retriever maddeyi getirecek; KÖR eğitim wrong_ref 0.80'in sebebi).
- **Uzman-register** (v1 vatandaş-register'ı yanlış kitle).
- **%15-25 hedge/red** örneği (v1'de %1.1 → SFT'nin tek base+prompt'la zor taklit edilen meşru rolü: kaynak-yokken uydurma yerine "maddede yok/danış").
- **Başarı kapısı:** faithfulness DEĞİL (tavan) → **wrong_ref ≤0.05 + hedge-isabeti + atıf-format tutarlılığı.**
- **Versiyonlama:** v2 = **base'den taze QLoRA** (v1 üstüne DEĞİL). v0/v1/v2 = deney nesli, ağırlık atası değil. v1 arşivlenir (ablasyon referansı).

**Açık doc çelişkisi:** VISION.md §1 "default output = vatandaş dili / terim→sade çeviri" reframe ile çelişiyor → ADR-0010 + VISION düzeltmesi bekliyor.

### 2026-06-13 (akşam) — ⭐⭐ BENCHMARK RUN: base/v0/v1 × CORE-HARD+TRAP (madde-verili/oracle, n=40/35)
**Kurulum:** literatüre-dayalı setler (`data/eval/{core_hard,trap}.jsonl`), **madde-verili/oracle** modu (`--with-source`; doğru/tuzak madde ELLE prompt'a konur — gerçek RAG değil), gpt-4o-mini hakem. CORE-HARD = doğru madde verilir, doğruluk ölç (A1+A4). TRAP = konu-yakını YANLIŞ madde verilir, abstention ölç (A3). Skorlar: `outputs/eval/{gnd,abst,fmt}_bench_*_summary.json`, birleşik `outputs/BENCHMARK_REPORT.md`.

| eksen | metrik | base | v0 | v1 |
|---|---|---|---|---|
| **A1** (CORE) | faithfulness | **0.976** | 0.920 | 0.960 |
| | hallucination | 0.024 | 0.080 | 0.041 |
| | wrong_ref | 0.000 | 0.000 | 0.026 |
| **A3** (TRAP) ⭐ | **Rej\*(LLM)↑** | **0.786** | **0.000** | **0.000** |
| | Rej(exact)↑ | 0.679 | 0.000 | 0.000 |
| | fabrication↓ | 0.214 | 1.000 | 1.000 |
| | param_leak | 0.286 | 0.769 | **1.000** |
| | valid_traps | 28/35 | 26/35 | 26/35 |
| **A4** (CORE) | cite_present | 0.925 | 0.125 | 0.975 |
| | paren_cite | 0.025 | 0.000 | **0.975** |
| | med_len (kar) | 308 | 152 | 152 |

**Bulgular:**
1. **⭐ SFT abstention'ı YOK ETTİ — felaket niteliğinde, öngörüden çok sert.** AbstentionBench "~%24 bozar" diyordu; biz **0.786 → 0.000 tam çöküş** ölçtük (hem v0 hem v1, tuzakların %100'ünde uydurdu). **v1 param_leak=1.000** = verilen yanlış kaynağı tamamen yok sayıp ezberden cevapladı. → güçlü, yayınlanabilir **K3 negatif bulgu**: temiz grounded SFT (v1) bile abstention'ı sıfırlıyor.
2. **v1'in SFT'den TEK kazanımı = atıf FORMATI.** `paren_cite` 0.025→**0.975** ("(KANUN, Madde X)" kalıbı). Ama format kozmetik; A1 faithfulness'ta base'i GEÇMEDİ (0.960<0.976), wrong_ref'i SIFIRDAN 0.026'ya çıkardı. **Takas berbat:** kozmetik format ↔ asıl-eksen (A3) sıfırlandı.
3. **v0 ayrıca bozuk:** cite_present 0.125 (neredeyse hiç atıf), kısa (152 kar) → forum-register çöküşü A4'te de net. v0 < v1 < base.
4. **A1 madde-verili tavanı teyit:** üçü de 0.92–0.98 (ayırmıyor). K1 ablasyonda "+SFT" satırı faithfulness'la boş çıkar — SFT etkisini A3(yıkıcı)+A4(format)'ta göster. (Not: bu tavan oracle; gerçek RAG retriever-hatasıyla daha düşük olur.)
5. **Payda notu:** `valid_traps`<35 çünkü hakem "yanlış kaynak aslında cevaplıyor" derse tuzak elenir (`source_answers`→geçersiz). base 7, v0/v1 9 elendi; fark küçük, 0.786-vs-0.000 başlığını değiştirmez.

**Karar pekişti:** v2 **mutlaka ciddi hedge/abstention dilimi (%15-25) + madde-verili modda eğitim** içermeli — çöküş "0.000" olduğu için ufak SFT bile siliyor. **v2 başarı kapısı = A3 rejection_rate ≥ base (0.786)** (faithfulness DEĞİL, tavan). Format kazanımı (A4) v1'den miras ama abstention bedeline değmez → tek başına satılamaz.
**Sıradaki:** G1 cross-judge (gpt-4o alt-küme) bu A3 çöküşünü teyit etmeli (κ); sonra v2 veri tasarımı.

### 2026-06-13 (gece) — ⭐ CANON eval metodolojisi kilitlendi (grill + /deep-research → ADR-0011)
**Tetik:** kullanıcı itirazı — "model çıplak kanunu bilmeli, yoksa neden kanunla FT ettik?" + sabahki KÖR ölçümünün **metrik hatası** (kaynaksız cevabı "kaynağa sadakatsiz" diye cezaladık → faithfulness KÖR'de TANIMSIZ).
**Süreç:** 8 tasarım kararı grill-me ile çözüldü → `/deep-research` (22 kaynak, 8/8 nokta) ile literatüre doğrulatıldı → 4 düzeltme işlendi.

**CANON (ADR-0011):** 4 eksen AYRI (ortalanmaz): **A1** Groundedness (yalnız Oracle), **A2** Correctness (KÖR+Oracle, ref=gerçek madde), **A3** Abstention (TRAP), **A4** Format; **A1∧A2** türetilmiş ikincil. Mod-stratifiye: CORE×KÖR, CORE×Oracle, TRAP×Oracle (paired). Pilot 40/35 (paper 100/75).

**Akademik verdict (deep-research):** 6/8 nokta "olduğu gibi savunulabilir" (ALCE, RAGBench-TRACe, Wallat, RGB, FaithEval, selective-prediction); 4 düzeltme:
1. A1∧A2 manşet→ikincil (alan ayrı raporlar; Trust-Score ortalar=zıt).
2. **A3 çöküşü = ÖZGÜN K3 bulgusu, replikasyon DEĞİL** — yayınlı FT-harm OVER-refusal'dır, bizimki UNDER-refusal (zıt yön); AbstentionBench %24 reasoning-FT için (çürütüldü, direkt destek değil).
3. G1 cross-judge CROSS-FAMILY (Claude/Gemini), gpt-4o değil (Wataoka self-preference familiarity-kaynaklı).
4. bootstrap GA + paired McNemar; OOD unseen-statute dilimi paper öncesi.

**Kod:** `score_correctness.py` (YENİ: A2 + coverage/conditional-acc + bootstrap CI + TRAP gold-join 35/35 test). `bench_scorecard.py` canon'a güncellendi (mod-stratifiye, A1 KÖR'den çıkarıldı). Smoke: derleme OK, CI [0.625,0.875]@n40.
**Sıradaki:** pilot koşu base/v1 (manuel onay sonrası) → analiz → v2 hazırlığı.

### 2026-06-13 (gece) — ⭐⭐⭐ CANON PİLOT: base vs v1 → scope kararı (Product A) + v2 yönü
**Kurulum:** CANON eval (ADR-0011), base vs v1, n=40/35, 3 hücre paired, gpt-4o-mini hakem. Rapor: `outputs/BENCHMARK_REPORT.md`. Plan: `docs/V2_PLAN.md`.

| hücre | metrik | base | v1 |
|---|---|---|---|
| CORE-KÖR | A2 doğru (CI95) | 0.225 [.10,.35] | 0.300 [.17,.45] |
| | A2 lenient | **0.850** | 0.675 |
| CORE-Oracle | A1 faith | 0.977 | 0.960 |
| | A2 doğru | **0.925** | 0.800 |
| | **A1∧A2 🟢** | **0.875** | 0.775 |
| | A4 paren | 0.025 | **0.975** |
| TRAP | **A3 Rej\*** | **0.741** | **0.000** |
| | fabrication | 0.259 | 1.000 |
| | TRAP-A2 (diag) | 0.114 | 0.114 |

**Bulgular:**
1. **Scope A/B → PRODUCT A.** CORE-KÖR A2: v1≈base (0.30 vs 0.225, CI çakışık, lenient base lehine) → **FT kanun gömmüyor.** İkisi de kör hukukta kötü (~%25). Reframe (ADR-0010) DOĞRULANDI.
2. **v1 oracle'da bile base'den KÖTÜ.** A1∧A2 grounded-acc 0.775 < **0.875**. SFT yardım etmedi, **aktif zarar verdi** — tek kazanım kozmetik format.
3. **Abstention çöküşü teyit:** A3 0.741→0.000. **TRAP-A2 ikisi de 0.114 ama farklı sebep:** base çekiniyor (cevaplamıyor), v1 cevaplıyor ama **%88 yanlış = halüsinasyon** (doğru-ezber DEĞİL) → v2 hedge dozajı BÜYÜK.
4. **Kök ders (K3):** SFT bilgi değil ÜSLUP öğretir; base = güçlü okuyucu+kalibre model; v1 onun gücünü dar format için takas etti. base'in değeri genel yetenek (okuma+kalibrasyon).

**Karar (ADR-0012 dolduruldu):** scope = **Product A** (doğruluk RAG'dan). v2 = base'in gücünü KORU, yalnız 3 dar iş (abstention-koru + uzman-register + format). İki aday: **v2a=base+prompt (SFT yok)** vs **v2b=hafif-SFT**; önce v2a (ucuz, yan-hasarsız) dene. Başarı kapısı: A3≥0.741 + A1∧A2≥0.875 + A4 korunsun. **Detay: `docs/V2_PLAN.md`.**

### 2026-06-14 — v2 için 2 /deep-research → V2_PLAN.md zenginleştirildi
**(1) v2-teknik** (24 kaynak): v2a=base+prompt+RAG+**Sufficient-Context selective-generation** (FT'siz +%2-10, ICLR25) güçlü destekli → ÖNCE bu. v2b=**RAFT** (context-grounding, param_leak fix) + **R-Tuning** boundary-refusal, cevaplanabilir dilimle DENGELİ (yalnız-belirsizlik known-acc'yi %52'ye çökertir). Light-touch: EAFT/düşük-rank/replay/KL. **Register loss'a GİRMEZ** (prompt). **DPO "daha az yıkıcı" ÇÜRÜDÜ** (forgetting-direnci on-policy PPO'ya özgü). v1 0.000-abstention = full-FT'nin bilinen mekaniği (SEAT/FLAME, "Confident Conflicts").
**(2) hukuk-veri** (12 bulgu): **CPT bilgi gömer (SFT gömmez)** — SaulLM +%7 ama 54B/540B-token. Bütçe yolu = **EntiGraph sentetik-CPT** (RAG-lift'in >%80'i, RAG ile BİRLEŞİR) → v2c opsiyonel. Naive CPT genel-reasoning bozar → karışım şart. Türkçe çapa: **Mecellem 4-faz CPT**, **Muhakim 5-boyut reward** (eval scaffold). DISC-LawLLM = RAG-coupled syllogism deseni. SaulLM 3-turn sentetik = davranış-veri şablonu.
**Sonuç:** V2_PLAN.md = 3-adım karar ağacı (v2a prompt → v2b RAFT-SFT → v2c sentetik-CPT). İlk somut iş: **v2a'yı koş.**

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

### 2026-06-14 — v2 plan oturumu: SaulLM okuması + SFT hedef + veri pipeline + eval matrisi (ADR-0013)
Strateji oturumu, `docs/V2_PLAN.md`'yi execute-edilebilir hale getirdi. Kararlar/çıktılar:
- **SaulLM okundu** (`knowledge/summary_saullm.md`): bilgiyi **CPT** gömdü (SFT değil) → "SFT bilgi gömmüyor" bulgumuzu doğruladı; SaulLM peer-açık-modelleri yendi, **frontier'ı değil**; replay %2 + DPO-fayda-yok bizim bulgularla uyumlu. → ağırlık-temelli bilgi = CPT yolu (bizde v2c EntiGraph).
- **Kullanıcı kararı: PLAN A** = SFT (davranış) + RAG (bilgi, sonra), CPT'siz; yön = **direkt v2b** (v2a baseline'a indi). `V2_PLAN` banner + §4.
- **SFT hedef tanımı** (`V2_PLAN §3.1/§3.2`): 4 davranış (grounding/abstention/format/correctness-koru) ↔ 4 canon ekseni; bilgi-ezber ve register-loss bilinçli DIŞARIDA. base-vs-SFT örnek senaryolar = gold-cevap şablonu.
- **HEDGE MEKANİZMASI DÜZELTİLDİ** (`V2_PLAN §5.2`): RAG-grounded model için abstention = **context-yeterliliği** (Sufficient-Context 2411.06037), **parametrik base-prob DEĞİL** (R-Tuning closed-book için). Deterministik → "hedge oranı" = **(1-P)**; base-prob İPTAL; tek knob P (~%80, ablate). *(Önceki base-prob önerisi düzeltildi.)*
- **Veri durumu:** hammadde HAZIR (40.496 madde + 19.305 soru↔gold tohumu); **v2b eğitim çiftleri ÜRETİLMEDİ** (v1 cevapları kaynaksız/vatandaş-register/CoT-quote yok → kullanılamaz). Pipeline §5.2, script `build_sft_v2b.py` (Adım1/3/4/5 deterministik) + teacher-LLM (Adım2).
- **ADR-0013 yazıldı:** canon eval v2 = **5 mod matrisi** (M1 gold+distractor [YENİ, v2b manşeti] · M2 TRAP · M3 E-set [YENİ] · M4 temiz-Oracle [referans] · M5 KÖR) + A-register ekseni. Mevcut Oracle distractor içermiyor → deployment'tan kolay; düzeltilecek. İki bilinmeyen: distractor-dağılımı (retriever'a bağlı) + register-rubriği (Muhakim çapası).
- **Execution sırası** `V2_PLAN §9` (A eval-altyapı ∥ B veri → C eğit → D ölç → E sonrası). İlk iş: A1 (✅ ADR-0013) + B1 (build script).
- **Yol haritası ufku (OPSİYON, karar değil):** SFT → RAG → (gerekirse) **RLHF/GRPO**; reward = canon-skorlayıcılar (RLVR) + Muhakim, ayrı RM gerekmez; RAG'dan sonra (deployment dağılımı). on-policy PPO forgetting-direnci = teorik artı.
**Paper-eşleme:** methodology (eval-dist=deploy-dist ilkesi, mod matrisi) + K3 (SaulLM CPT-vs-SFT ayrımı bizim bulguyu evrenselleştirir).

### 2026-06-14 — v2b execution: compute'suz blocker'lar temizlendi (kod + doğrulama)
§9 execution sırasındaki benim-tarafımdaki tüm işler yazıldı + GERÇEK/sentetik veriyle doğrulandı (GPU yok):
- **`scripts/raft_pack.py`** (YENİ, ortak): RAFT context paketleme — gold + hard-negative distractor (aynı kanun komşu madde). Eval ↔ eğitim AYNI modül + AYNI sistem promptu (`SYSTEM_PROMPT_RAG_MULTI`) → dağılım eşleşir (ADR-0013).
- **A2/A3** `gen_eval_grounded.py`: `--distractors N` (M1, gold+N distractor) + `--empty-context` (M3, E-set boş bağlam). detail'e `context_shown`+`mode` eklendi. *(Tam gen GPU ister; paketleme B1 ile doğrulandı.)*
- **A4** `scripts/score_register.py` (YENİ): uzman-vs-vatandaş leksik proxy. Doğrulama: uzman cevap→1.00 (E7/C0), vatandaş→0.00 (E0/C7). Kanonik=LLM-judge (TODO).
- **B1** `scripts/build_sft_v2b.py` (YENİ): `pack` (Adım1) + `assemble` (Adım3/4/5). **Koştu:** 19.305 tohum → 15.458 grounded / 3.847 abstain (P=0.8 ✓), grounded=gold+4distractor gold-içinde, abstain=gold-çıkarılmış. Kapı testi: 4 sentetik→2 geçti/2 elendi (kötü-quote + uydurma-abstain doğru elendi).
- **B2** `scripts/gen_v2b_answers.py` (YENİ): teacher-LLM (grounded→gpt-4o-mini CoT+verbatim-quote+atıf, abstain→şablon bedava). abstain-yolu + assemble zinciri doğrulandı. **Koşmak=kullanıcı** (OPENAI_API_KEY, ~15K çağrı).
- Artefakt: `data/processed/sft_v2b/packed.jsonl` (19.305, B1 çıktısı). Sentetik test dosyaları temizlendi.
**Kalan (yalnız compute/kullanıcı):** B2 koş (API) → assemble → C1 Modal A100 eğit → D canon ölç. Kod tarafı %100 hazır.

### 2026-06-14 — A+B paralel koşu + B1 veri-bozukluğu bug'ı (smoke yakaladı)
Kullanıcı "A+B paralel başlat" dedi. A (GPU eval) lokal RTX 5070 Ti'de (12GB boş), B (API) gpt-4o-mini.
- **A-track:** M1 (gold+4 distractor) + M3 (empty-context) base baseline — `gen_eval_grounded.py`, lokal 4-bit 12B, ardışık (tek GPU).
- **B-track BUG (kritik, smoke yakaladı):** B2 smoke (20 satır) → assemble gate **16/16 grounded RED** ("alıntı gold'da değil"). Kök-neden: **B1 pack yanlış alanı gold_text sanıyordu** — `sft_v1/train.jsonl`'deki `source` alanı madde metni DEĞİL, provenance etiketi (`'grounded_gpt-4o-mini'`). Gerçek madde metni sft_v1'de YOK; `mevzuat_maddeler.jsonl`'den `(kanun_no|madde_no)` ile JOIN edilmeli (gen_eval_grounded zaten öyle yapıyor — eğitim tarafı atlanmış). JOIN kapsamı %100 (19.305/19.305, format uyumlu "MADDE 6").
- **Düzeltme:** `build_sft_v2b.py`'ye `load_madde_index` + `extract_seed(rec, madde_idx)` JOIN eklendi; gate'e tırnak-soyutlama (`strip`) — teacher metni `"..."` sarınca eşleşme kırılıyordu. Pack yeniden koştu → gold_text artık gerçek (TKHK M6 "Vitrinde... satışından kaçınılamaz" ↔ soru eşleşiyor). Smoke tekrar → **gate 19/20 geçti** (1 ret = teacher distractor'dan alıntı yaptı, gate DOĞRU eledi = kapının asıl işi).
- **Ders (paper/methodology):** smoke-test (~16 çağrı, cent'ler) tam B2 (~15K çağrı, ~$9) öncesi veri-bozukluğunu yakaladı → "EDA-verify her dataset" disiplini burada da ödedi. Gold-text-as-provenance-tag = sessiz bozukluk; deterministik gate (verbatim⊂gold) onu görünür yaptı. → tam B2 başlatıldı.

#### A-track BASELINE sonuçları (base, gemma-4-12B, n=40, gpt-4o-mini judge)
v2b SFT'nin **yeneceği/koruyacağı** çıpa sayıları (yeni M1/M3 modları, ADR-0013):
- **M1 (gold+4 distractor, A1 groundedness):** faithfulness_micro=**0.879**, hallucination_micro=0.122, cit_precision_micro=0.905, wrong_ref_rate=0.095, faithfulness_macro=0.742. Dosya `outputs/eval/gnd_bench_m1_base_summary.json`. → Base distractor-gürültüsünde %88 sadık; v2b bunu **koru/artır**.
- **M3 (empty-context, A3 abstention, deterministik):** rejection_rate=**1.000** (40/40), fabrication=0.000. → **Base boş bağlamda kusursuz çekiniyor.** v2b'nin asıl riski bu sayıyı BOZMAK (v1 abstention çöküşü 0.74→0.00 = Cor-RAIT over-refusal'ın TERSİ: SFT burada fabrikasyona kaydı). CRaFT/replay reçetesi tam bunu korumak için.
- **Okuma:** base zaten iyi bir RAG-okuyucu+çekinici. v2b'nin işi yeni yetenek eklemek değil, bu iki davranışı (faithful-when-grounded ∧ abstain-when-empty) SFT sonrası KORUYABİLDİĞİNİ + uzman-register + verbatim-quote format eklemek. Headline ablasyon: base vs v2b, AYNI M1/M3 modunda.

#### C1 EĞİTİM ALTYAPISI hazırlandı (B akarken, kod-only)
v2b Modal eğitim hattı kuruldu — mevcut v1 altyapısı (`train_sft.py` + `modal_train.py`) reçeteye (§5.1) uyarlandı:
- **`train_sft.py`:** (a) `--warmup-ratio` flag (sweep, §5.1-C %3-5); (b) `--allow-high-lr` + **3e-4 GÜVENLİK KİLİDİ** — lr≥3e-4 normalde `SystemExit` (v1 abstention-çöküşü rejimi = continual-pretrain re-warming, 2403.08763/2503.02844; davranışsal SFT'de yasak). Test: 1e-4/2e-4 geçer, 3e-4 blok, `--allow-high-lr` açar.
- **`modal_train.py::spawn_v2b`:** fire-and-forget v2b entrypoint, reçete varsayılanları (lr=1e-4 = LoRA≈10x-full-FT, r=16/α=32, warmup=0.05, 1 epoch, `--no-system`). **Kilit tasarım:** `--no-system` zorunlu çünkü v2b verisi `SYSTEM_PROMPT_RAG_MULTI`'yi `messages[0]`'da TAŞIR (assemble gömüyor) → v1 gibi system eklenirse ÇİFT system olur. Ablasyon (C2) için lr/rank/data parametrik.
- **Çalıştırma sırası (B+assemble bitince):**
  1. `modal volume put hukuk-data data/processed/sft_v2b /sft_v2b`
  2. `modal run modal_train.py::spawn_v2b --smoke` (50 step, ~$0.15, loss düşüyor mu)
  3. `modal run modal_train.py::spawn_v2b --run-name v2b --epochs 1` (tam, fire-and-forget)
  4. `modal volume get hukuk-outputs /v2b ./outputs/v2b` → D1 canon eval (M1/M3 v2b)
- **Henüz YOK:** v2b train.jsonl (B2→assemble üretecek) → smoke ancak ondan sonra. requirements.lock + volume'lar v1'den hazır.

#### B2 paralelizasyon + Tier 1 RPD duvarı + topik-skew dersi
- **Paralelize edildi:** `gen_v2b_answers.py` `--workers` (ThreadPool + yazım-lock + resume korundu). İki bug bulundu+çözüldü: (a) **timeout'suz OpenAI client** paralel koşuda asılı sokette tüm worker'ları kilitliyor → `timeout=30, max_retries=0` (kendi exp-backoff'umuz var); (b) **6 worker Tier 1 TPM 200K tavanına biniyor** → 429 → default 4 worker (~160K TPM güvenli). Ağ-değişimine dayanıklılık kanıtlandı (stale-conn timeout→retry self-heal).
- **🔴 Tier 1 RPD duvarı (10.000 istek/gün):** ~10K çağrıdan sonra `429 ... requests per day (RPD): Limit 10000, Used 10000`. Bugün B2 14.800/19.305'te durdu. Reset ~gece yarısı UTC. (İlk RPD tahminim doğruymuş; v1 muhtemelen <10K veya güne yayılmıştı.)
- **🔴 TOPİK-SKEW dersi (kullanıcı yakaladı):** seed dosyası (`sft_v1/train.jsonl`) **kanuna göre SIRALI** (id boyunca 18 kanun-değişimi = blok blok), shuffle DEĞİL. → ilk 14.800'ü almak rastgele örnek değil: **İCRA VE İFLAS KANUNU (2.727, ~%14) ve KAT MÜLKİYETİ üretilende SIFIR.** Slice oranı (80/20) korunur ama **topik dağılım bozulur.** → "eldekiyle eğit" İPTAL; tam set ZORUNLU. **Ders:** partial-tolerant pipeline için seed'ler pack'te SHUFFLE'lanmalıydı; aksi halde yarıda-kesilme = sistematik kapsama deliği. (Paper-methodology: veri-üretim sırası temsililiği.)
- **Karar:** RPD reset bekle → resume (kalan ~4.505, İİK dahil) → assemble → C1. Devir notu: `NEXT_SESSION.md`.

---

## 2026-06-24 — v2b veri tamamlandı + replay + uzun-madde truncation fix

#### B2 tam set bitti, topik-skew onarıldı
- RPD reset sonrası `gen_v2b_answers.py` resume ile **19.305/19.305** cevap üretildi (grounded 15.458 / abstain 3.847, 0 boş). Önceki 14.800-kısmi koşunun atladığı **İCRA VE İFLAS KANUNU artık 2.727, KAT MÜLKİYETİ 552** (sıralı-seed topik-skew deliği kapandı). assemble: kept 18.670 / rejected 635 (630 "alıntı gold'da değil" + 5 atıf-no) → ~%3.3 deterministik ret.

#### Replay seti (forgetting sigortası, §5.1-D)
- `scripts/build_replay_tr.py` (YENİ): kaynak `AlicanKiraz0/Turkish-SFT-Dataset-v1.0` (**MIT** → license-clean), genel TR instruction (hukuk-DIŞI). EDA-doğrulandı (HARD RULE): 5.579 satır, %99.8 TR, 0 İngilizce, 0 boş, tek-tip system prompt. Süzme: hukuk-ele + token≤1500 (truncation YOK) + dedup → havuz 662 → **600 örnek** (token median 725). assemble `--replay 0.03` → train mix'e **577 replay** (grounded 13.350 / abstain 3.455 / replay 518). Gerekçe: v1 abstention çöküşüne karşı LoRA+düşük-rank+**replay** kanıtlı üçlüsünün üçüncü ayağı.

#### 🔴 Uzun-madde truncation fix (smoke yakaladı — paper-methodology)
- **Bulgu (smoke logu):** `max_seq_len=2048` ile Unsloth **1.421/17.323 (%8.2)** örneği "tüm label -100 (cevap truncate)" diye düşürdü; ayrıca toplam **2.010 (%11.6)** örnek >2048 = cevap kısmen kesik (gizli zarar: yarım-cevap öğretimi).
- **Kök neden (ölçüldü):** suçlu cevap değil. grounded ANSWER token median **196** (max 873) ama KAYNAK bloğu median 1.030, **max 12.805** — tek bir maddenin tüm metni (gold/distractor) 12K token olabiliyor. Gerçek RAG retriever tam kanunu değil **chunk** döner → tam-metin distractor zaten gerçek-dışı.
- **Fix:** `build_sft_v2b.py` → `clip_sources_block` (+`--max-chunk-chars`, default **900**≈243 tok). Her [KAYNAK i] maddesini 900 char'a kırpar; **gold chunk'ta cevabın `##begin_quote##` span'i pencere içinde KORUNUR** (yoksa context'te-olmayanı-alıntıla = halüsinasyon öğretimi). Cevap (target) ASLA kırpılmaz. Re-generate YOK (mevcut answers üzerinde post-hoc).
- **Doğrulama:** >2048 **%11.6 → %0.03** (5 örnek), gold quote context'te **13.350/13.350 (%100)**. max_seq_len=2048 kalır → maliyet sabit (~4h/$15, 994 step × ~15.75s/step ölçüldü). Örneklerin ~%100'ü korunur. *(ADR-0013 eval=train dağılımı için: aynı 900-cap raft_pack/gen_eval_grounded'e D1 ÖNCESİ aynalanmalı — açık iş.)*

#### Modal detach dersi (PC-kapanma dayanıklılığı)
- `modal run modal_train.py::spawn_v2b` (detach'siz) = local entrypoint bitince app `stopped`, **0 task** → spawn'lı fonksiyon ölüyor (gözlemlendi). **`modal run --detach`** = app bulutta `ephemeral`+task, client/PC/WSL kopsa da sürer → izle `modal app logs <app-id>`. (Önceki "PC kapayınca patladı" sorununun kökü buydu; ADR-0008 fire-and-forget ancak --detach ile geçerli.)
- **Smoke sağlık:** step10 loss=**1.411**, grad_norm 16.76, lr 9.6e-05 (warmup→1e-4), A100-40GB OOM yok, LoRA 65.5M (%0.55).

---

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
#### D1 canon eval — 6-mod matris SONUÇ (n=40/35/30, gpt-4o-mini hakem; detay [`v2b_sonuclar.md`](v2b_sonuclar.md))
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
- **v2c açık işler (tasarım notu `v2b_sonuclar.md` sonu):** TRAP-tipi abstain dilimi + anti-parametric-leak counterfactual (M2 param_leak %61.5) + GOLD-scrub (%5.7) + off-by-one atıf + core_hard kötü-eşleşme temizliği + register ekseni. TEK v2c FT.

---

## Açık kararlar / sıradaki
- [ ] 🎯 **HEDEF YÜKSELTİLDİ (2026-07-02, kullanıcı direktifi): v2c kapısı = REGRESYON değil ÜSTÜNLÜK.** "base'in altına düşme" yetmez → **base'i anlamlı-eksenlerde NET geç** ("küçük fark yeterli değil"). Ezilebilir eksen hedefleri: M2 yanlış-kaynak abstention **≥0.90** (base 0.786, v2b 0.346 → kayıptan net kazanca çevir), M1 grounding **≥0.94** (base 0.879), A4 **≥0.95**. Tavan eksenleri (M3/M4/M2b) BOZULMADAN korunur ("ezdik" denmez). M5 KÖR = anti-hedef (düşük İYİ). NET fark = effect size **+** n≥100 + base-rescore + κ-vekili (ikisi de şart). Detay/tablo: `v2c_roadmap.md §6`.
- [ ] ✅ **v2c aç-koş EKİ yazıldı (2026-07-02):** roadmap'in 3 niyet-düzeyi boşluğu (register metriği · A2 counterfactual yöntemi · A1 TRAP-abstain dilim speci) çalıştırılabilir seviyeye çekildi → `v2c_roadmap.md §7`. Bulgular: (1) **register script ZATEN VAR** (`score_register.py` leksik-proxy, hakemsiz) — "hiç ölçülmedi" stale idi, gerçek gap = koşulmadı + kanonik LLM-judge rubriği TODO; (2) **A1 yanlış-komşu kaynağı `trap.jsonl`'dan ALINAMAZ** (eval sızıntısı) → madde havuzundan `madde_ord` komşusuyla üret; (3) **n≥100 karşılanmıyor** (core=40/trap=35) → `gen_eval_grounded.py --n 120`. Kalan yeni-kod: pack'e 2 slice üretici (`counterfactual`+`abstain_trap`) + `_gate` cf-referans + `ABSTAIN_TRAP_TEMPLATES`.
- [ ] 🔴 **GOLD-sızıntı düzeltmesi (v2c/sonraki FT)** — `gen_v2b_answers.py` teacher prompt'unda "GOLD" jargonunu yasakla (öğrenci-etiket uzayı = `[KAYNAK N]`) + mevcut answers'ta regex scrub. %5.7 hedef etkilendi (2026-07-02 girdisi).
- [x] ~~ADR-0010: reframe (uzman birincil register) + VISION.md §1 düzeltmesi.~~ → 2026-07-01 yazıldı (`docs/adr/0010-reframe-birincil-register-uzman.md`).
- [x] ~~n=40 + zor sette base vs v1 teyit~~ → 2026-06-13 akşam BENCHMARK RUN ile yapıldı (A1 tavan teyit, A3 SFT çöküşü ölçüldü).
- [ ] v2 tasarımı: madde-verili modda veri üretimi + hedge dilimi + uzman register prompt. **Ablasyon gerekli:** hedge dozajı (%15 vs %25) + eğitim-modu-vs-hedge confound ayrımı (pilot bunları çözemez, v2 ablasyonu çözecek).
- [ ] **Register/altitude ekseni EKSİK (brainstorm 2026-06-13 gece).** Pilot correctness/grounded/abstention ölçüyor ama "çıktı uzman-register mı vatandaş-basit mi" ölçmüyor. v2 hedefi=uzman-register → v2 DEĞERLENDİRMESİNDEN önce register sinyali eklenmeli (yeni eksen veya A4'e altitude metriği). Pilotu bloklamaz; v2-eval'i bloklar.
- [ ] Kaynak-eksik eval seti (hedge-isabeti ölçmek için) — yeni.
- [ ] Rakip baseline (Mecellem-Qwen3-4B, Llama-3.1-8B) bizim terazide, madde-verili modu. → **v2c_roadmap Tier C4'e bağlandı** (C3 base-rescore ile aynı ölçüm-oturumu, çıktı=PAPER_TARGET §4 Tablo 1; Mecellem=foundation-kıyası, instruct değil).
- [ ] MCQ ekseni (hakem-bağımsız) — paper sağlamlaştırma. (cross-judge + ~30 yazar spot-check → aşağı "Paper öncesi" maddesine taşındı; cross-judge gpt-4o değil **cross-family** olacak.)
- [ ] **outputs/eval/ klasör düzeni (SONRA).** Düz dizin göz yoruyor → `raw/` (bench_*_detail), `scored/` (gnd_*, abst_*), `summary/` (*_summary.json) alt-klasörlerine nestele. DİKKAT: skriptlerin `outputs/eval/` yollarını güncelle (gen_eval_grounded out-dir, groundedness/score_*/bench_scorecard okuma yolları). Dosya şeması sabitlenince tek seferde yap, v2'den önce.
- [x] ~~Eksen yeniden-numaralandırma (GÜN SONU)~~ → GEREKSİZ (ADR-0011): boş A2 slotu **Correctness** ile doldu, A1/A2/A3/A4 sıralı, gap yok. Kaydırmaya gerek kalmadı.
- [ ] **CANON pilot koşu (base/v1) — manuel onay sonrası.** Üret: CORE-KÖR + CORE-Oracle + TRAP (paired) → skorla A1/A2/A3/A4 + A1∧A2 → `bench_scorecard.py`.
- [ ] **Paper öncesi:** G1 cross-family judge (Claude/Gemini, κ) · paired McNemar · OOD unseen-statute dilimi · n=100/75 · A1/A2 operasyonel tanım yazımı.

## Paper'a ne yarar (eşleme)
- **K1 ablasyon:** base → +SFT → +madde-verili (oracle) tablosu. **Uyarı:** faithfulness'la ölçülürse "+SFT" satırı boş çıkar (tavan); SFT katkısını wrong_ref/hedge/format eksenlerinde göster. (oracle = gerçek RAG'ın iyimser tavanı.)
- **K3 ayrışma/negatif bulgular:** (a) v0 forum verisi çöküşü (154x ezber), (b) **KÖR-vs-madde-verili: parametrik madde-no ezberi imkansız, oracle-tavan SFT'yi faithfulness'ta gereksizleştirir** — güçlü, yayınlanabilir negatif bulgu, (c) etiketsiz-chunk → uydurma atıf.
- **Methodology:** grounded veri imali, kalite kapısı köprüsü, dış-iddia doğrulama disiplini.
