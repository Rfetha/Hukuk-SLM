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

## v2c icra — ADIM 1: C1-v2b register ölçümü (2026-07-02)
Otorite: [`v2c_roadmap.md`](v2c_roadmap.md) §5 (tek numaralı akış) · §7·AÇ-KOŞ-1 · G4.

**Ne:** `score_register.py` (v1 leksik-proxy, hakemsiz, deterministik) v2b'nin M1 detail'i üstünde koşuldu. Roadmap'in "register ekseni script VAR, koşulmadı" boşluğunun (G4) v2b yarısını kapatır — base/v1 yarısı ADIM 2'de (C3 rescore detail'i üretince, §5 ⛓️).

**Sonuç (kaynak: `outputs/eval/reg_m1_v2b_summary.json` + `reg_m1_v2b.jsonl`):**
| Model | n | register_mean | expert_frac(≥0.6) | citizen_frac(≤0.4) |
|---|---|---|---|---|
| **v2b (M1)** | 40 | **1.000** | **1.000** | **0.000** |

- **Dağılım teyidi:** 40/40 satır `expert_hits≥1` (min 1 · medyan 3 · max 5), `citizen_hits=0` istisnasız → mean=1.0 gerçek (nötr 0.5 masking değil; e+c=0 olan satır yok, hepsi expert-sinyalli).
- **Lesson:** v2b proxy-düzeyinde **tam uzman-register** — uzman-birincil reframe (ADR-0010) çıktıya yansımış; vatandaş-basit sızıntı yok. Bu bir **regresyon alt-sınırı** (§7·AÇ-KOŞ-1): v2c'nin `expert_frac` düşürmemesi / `citizen_frac` artırmaması gerekir, üstünlük değil (uzman-register zaten v2 tasarımı, §6 dışı).
- **Uyarı (yorumu sınırla):** proxy leksik — "uzman kelime var mı" ölçer, "doğru/anlaşılır mı" DEĞİL. Kanonik metrik = LLM-judge rubriği (ADR-0013, hâlâ TODO). base/v1 karşılaştırması olmadan mutlak 1.0 tek başına anlam taşımaz → ADIM 2 base/v1 üçlü tablosu şart.

---

## v2c icra — ADIM 3-5: C2 (position-bias) + B1 (GOLD-scrub) + B2/B3 (hijyen) (2026-07-02)
Otorite: [`v2c_roadmap.md`](v2c_roadmap.md) §5 madde 3-5. Hepsi GPU'suz kod/veri incelemesi — ADIM 2 GPU batch'i (C3+C4+C1-base/v1) arka planda koşarken paralel yapıldı. `v2c` branch'inde.

**ADIM 3 — C2 position-bias shuffle (G2 de test eder): sıfır-kod, ZATEN VAR.**
- `raft_pack.pack_context` satır 125 `rng.shuffle(chunks)` → gold, distractor'lar arasında randomize. rng per-örnek deterministik (`gen_eval_grounded` satır 210 `Random(seed+i)`) → tekrar-üretilebilir ama pozisyon sabit değil.
- **Ampirik teyit (v2b M1 detail, n=40):** gold `[KAYNAK n]` pozisyon dağılımı `{1:9, 2:9, 3:9, 4:9, 5:4}` (40/40 eşleşti) → 5 slota düzgün yayılmış, **pozisyon-bias YOK**. Bu, G2 off-by-one'ın "gold hep aynı slotta → etiket ezberi" maskesini de dışlar. **Kod değişikliği gerekmedi.**

**ADIM 4 — B1 GOLD-scrub (G3): TAMAMLANDI.**
- **(a) Teacher-prompt yasağı:** `gen_v2b_answers.py` `TEACHER_SYSTEM`'e "cevap metninde 'GOLD' kelimesini ASLA kullanma (hiçbir çekimle); 'ilgili kaynak/madde' veya '[KAYNAK N]' de" kuralı eklendi. ⛓️ ADIM 6b gen_answers'tan önce şart — yeni üretim temiz doğsun.
- **(b) Mevcut answers.jsonl scrub:** `data/processed/sft_v2b/answers.jsonl` — sızıntı **1157/19305 = %5.99** (v2b_sonuclar %5.7 tahminini doğruladı). Baskın kalıp: "GOLD metnidir" (603), "GOLD madde metnidir" (94), "GOLD maddesidir" (28), "GOLD kaynağıdır" (27). Sıralı (en-özgül-önce) regex + fallback token → **1157→0**, cümleler korundu ("…içeren GOLD metnidir" → "…içeren ilgili kaynak metnidir"). Yedek: `answers.jsonl.pre_scrub.bak`.

**ADIM 5 — B2 replay teyit + B3 core_hard: B2 DOĞRULANDI (dokunulmadı) · B3 BELGELENDİ (kaldırma ertelendi).**
- **B2:** `data/processed/replay_tr.jsonl` (n=600) = `AlicanKiraz0/Turkish-SFT-Dataset-v1.0` (MIT, license-clean), EDA-süzülü **genel/hukuk-DIŞI** TR instruction (yalnız 2/600 hukuk-terimli). Amaç = genel-yetenek koruması (anti-forgetting). Danışmanın "temiz Yargıtay" önerisi hukuk pattern'i pekiştirir = replay'in AMACINA aykırı → **mevcut replay uygun, DOKUNULMADI** (Claude-filtre "uygunsa dokunma").
- **B3:** core_hard kötü-eşleşme kesin vaka = **#28 & #29** (ikisi de "KAT MÜLKİYETİ KANUNU Madde 4"e bağlı, ama gold Md4 = "Ortak yerler" tanımı; sorular uyumsuzluk-yaptırımı/pay-iptali hakkında = ilgisiz). ⚠️ core_hard ŞİMDİ düzenlenirse koşan C3 batch + v2b sonuçları elmayla-elma olmaktan çıkar → **kaldırma n=120 final-kapı regen'ine ertelendi** (tüm modeller temiz sette birlikte koşulacak).

---

## v2c icra — ADIM 6a+6b: Tier A yeni-kod + v2c eğitim verisi İNŞA EDİLDİ (2026-07-02)
Otorite: [`v2c_roadmap.md`](v2c_roadmap.md) §5 madde 6a-6b · §7 AÇ-KOŞ-2/3. `v2c` branch. **Modal eğitimi (6c) = para-kapısı → kullanıcı onayı bekleniyor.**

**Yeni-kod (4 parça, hepsi çalışır+test-edildi):**
- `build_sft_v2b.py pack`: 2 yeni slice üretici — `counterfactual` (A2) + `abstain_trap` (A1). Dönüşüm kararı **AYRI `crng`** ile (ana P-roll/distractor rng akışı BOZULMAZ) → dönüşmeyen grounded/abstain satırlar v2b ile **byte-identik** → reuse geçerli + §1 regresyon güvenli. `--cf-frac/--trap-frac/--trap-k/--out-dir` args.
- `_gate`: counterfactual için referans = `cf_gold_text` (gerçek gold'a bakarsa haksız reddeder); abstain_trap = abstain gibi (ABSTAIN_RE).
- `gen_v2b_answers.py`: `ABSTAIN_TRAP_TEMPLATES` (5 varyant, hepsi ABSTAIN_RE-uyumlu) + `build_cf_answer` (cf_quote alıntıla+atıf) + worker dispatch + **`--reuse-answers`** (grounded'ı v2b'den al).

**Ampirik bulgu — Türk hukuk metni sayıları KELİME yazar (K3 malzemesi):** digit-regex CF olgusu grounded'ın sadece **%0.3'ünü** (49/15447) tuttu; kelime-sayı ("otuz gün", "yüzde yirmi") desteği eklenince tespit **%17.6'ya** çıktı. cf-frac=0.25'te CF=716 (cf_miss=3195). CF, hedeflenen ~1.5K'nın altında (olgu-kıtlığı) ama trap (birincil kaldıraç) hedefi tam tutturuyor → CF ikincil, grounded-seyreltmeyi (§1 risk) minimalde tutmak için bilinçli düşük.

**Kompozisyon (`data/processed/sft_v2c/packed.jsonl`, seed 3407, P=0.8, cf-frac 0.25, trap-frac 0.40):**
`{grounded 14742 (76%), counterfactual 716 (3.7%), abstain 2339 (12%), abstain_trap 1508 (7.8%)}` — abstain+trap=**19.9%** (§7 ~%20 ✓), trap/abstain=**39/61** (§7 40/60 ✓).

**gen_answers — API çağrısı=0:** 14742 grounded'ın HEPSİ v2b scrub'lı answers'tan (reuse-map=15458) alındı → **maliyet ~$0, grounding dağılımı birebir korundu.** cf/trap/abstain şablon.

**assemble (gate+replay+split) → `data/processed/sft_v2c/{train,validation,test}.jsonl`:**
- kept 18701 / red 604 (601 quote + 3 atıf). **Red'lerin TAMAMI grounded**, CF'te 0 red (716/716 gate geçti), trap'te 0 red. Red'ler **pre-existing v2b-mirası** (v2b 635 red; v2c daha AZ çünkü bazı red-grounded CF'e dönüştü). GOLD-scrub hiçbir quote'u bozmadı (quote-içinde-GOLD = 0).
- train=17353 (grounded 12720 · trap 1369 · abstain 2092 · cf 650 · replay 522) · val=963 · test=963.
- Örnek-teyit: CF cevabı counterfactual değeri kaynaktan alıntılıyor (ezber değil); trap cevabı yanlış kaynağı (KMK Md43) adıyla reddediyor. İkisi de hedefe uygun.

**Kalan:** 6c Modal `--detach` eğitim (config=v2b: lr=1e-4, r=16/α=32) → **PARA-KAPISI, onay bekleniyor.** Sonra 6d 6-mod eval (§6 üstünlük + §1 regresyon).

---

## 🔴 CANLI DURUM SNAPSHOT (2026-07-02, compact sigortası) — İKİ İŞ KOŞUYOR
> Bu blok, context-compaction'a karşı taze-agent devir notudur. Branch = **`v2c`**.

**1) v2c EĞİTİMİ — Modal A100, KOŞUYOR (ADIM 6c):**
- app=`ap-kKczVUwN4cMj6fodVkaLvK` · FunctionCall=`fc-01KWHHWR578WWCXQJ6Q0D37PZ3` · run=`v2c` · 1 epoch = **1085 step** (~15s/it, ~4-4.5h) · smoke green (step-10 loss=1.347).
- İzle: `modal app logs ap-kKczVUwN4cMj6fodVkaLvK` · durum: `modal app list`.
- Bitince: `modal volume get hukuk-outputs /v2c ./outputs/v2c` → adapter=`outputs/v2c`.

**2) C3 BASELINE — yerel RTX 5070, KOŞUYOR (ADIM 2):**
- nohup driver=`/tmp/claude-1000/-home-ersoy-code-Hukuk-SLM/5ce8b25c-e4fb-447b-aa40-af24802b11b2/scratchpad/run_c3_base_v1.sh` · log=aynı dizin `c3_run.log` · PID 57548.
- base'i 6 modda (M1/M4/M2b bitti · M2/M3/M5 sırada) sonra v1. Çıktı: `outputs/eval/bench_m{1..5}_{base,v1}_detail.jsonl` + skorlar.
- İzle: `grep -E '=== .* bitti ===' c3_run.log; tail -1 c3_run.log`.

**BİTİNCE YAPILACAK:**
- **C3 bitince → ADIM 2 tamamla:** her mod için `python scripts/rescore_answered.py --gnd gnd_bench_mX_{model}.jsonl --bench bench_mX_{model}_detail.jsonl --label mX_{model}` (cevaplanan-only, ADR-0011) · register: `score_register.py --details bench_m1_{base,v1}_detail.jsonl` · **C4 Mecellem baseline** (Tablo 1, `newmindai/Mecellem-Qwen3-4B-TR`, completion-style, yerel) · base over-refusal spot-check → research_log ADIM 2 tam tablo + roadmap §5 madde 2 ✅.
- **v2c eğitimi bitince → ADIM 6d eval:** adapter çek → 6-mod eval (v2b'nin komutları: `gen_eval_grounded.py` M1 `--distractors 4 --max-chunk-chars 900 --n 40`, M2 `--data trap.jsonl --with-source --n 35`, M2b `--distractors 4 --no-gold`, M3 `--empty-context`, M4 `--with-source`, M5 blind; skorla groundedness/score_abstention/score_correctness) → **§6 üstünlük** (M2≥0.90, M1≥0.94, A4≥0.95) + **§1 regresyon kapısı** (M1 0.904·M4 0.975·M2b 0.96·M3 1.0·M5≈0.175·A4 0.925 DÜŞMESİN). Kapı geçmezse v2c reddedilir.

**BİTEN ADIMLAR (v2c branch, commit'li):** ADIM 1 (register v2b=1.0) · ADIM 3 C2 (bias yok, sıfır-kod) · ADIM 4 B1 (GOLD-scrub 1157→0 + teacher yasağı; yedek `data/processed/sft_v2b/answers.jsonl.pre_scrub.bak`) · ADIM 5 B2/B3 (replay dokunulmadı; core_hard #28/#29 belgelendi, kaldırma n=120'ye ertelendi) · ADIM 6a yeni-kod (`build_sft_v2b.py` cf+trap slice + `_gate` cf-ref + kelime-sayı CF; `gen_v2b_answers.py` ABSTAIN_TRAP_TEMPLATES+build_cf_answer+`--reuse-answers`) · ADIM 6b veri (`data/processed/sft_v2c/` train 17353/val 963/test 963, API=$0).

**ELMAYLA-ELMA ERKEN SAYILAR (biten base modları vs v2b, aynı kural):** M1 base 0.886@cov%47.5 vs v2b 0.92@%72.5 · M4 base 0.971 vs 0.975 · M2b base 1.0 (aşırı-ret artefaktı) vs 0.96. → base bilgide eşit, **davranışta v2b üstün**; base her yerde over-refuse. base M2(yanlış-kaynak) bekleniyor (eski 0.786 = v2c'nin geçmesi gereken).

**pack reçetesi (tekrar üretmek gerekirse):** `build_sft_v2b.py pack --p 0.8 --distractors 4 --seed 3407 --cf-frac 0.25 --trap-frac 0.40 --out-dir data/processed/sft_v2c` → `gen_v2b_answers.py --packed .../packed.jsonl --out .../answers.jsonl --reuse-answers data/processed/sft_v2b/answers.jsonl --workers 1` → `build_sft_v2b.py assemble --answers .../answers.jsonl --out-dir data/processed/sft_v2c --replay data/processed/replay_tr.jsonl --replay-frac 0.03 --max-chunk-chars 900`.

---

## v2c icra — ADIM 6c: Modal eğitim BAŞLADI (smoke GREEN) + ADIM 2 erken sinyal (2026-07-02)
Otorite: `v2c_roadmap.md` §5 madde 6c. Kullanıcı onayı alındı ("smoke sonra tam koşu", 2026-07-02).

**Modal smoke → GREEN → tam koşu:**
- ⚠️ İlk smoke `--detach`'siz başlatıldı → ephemeral app entrypoint bitince kapandı, 0 task koştu (**kredi harcanmadı**). V2_PLAN§9 uyarısı doğrulandı: `modal run --detach` ŞART.
- Smoke (`--detach`, ap-jT66lrYqzGoNRNW0ZVx12w, run=v2c-smoke, 50 step): **veri doğru yüklendi** (train **17353**/val **963**), adapter **65.5M (0.55%)** = v2b, ~15s/step (A100-40GB), **step-10 loss=1.347** (v2b smoke 1.411 ile uyumlu), OOM/hata YOK. → config+veri VALİDE.
- **Tam koşu SPAWNED** (`--detach`, **app=ap-kKczVUwN4cMj6fodVkaLvK**, FunctionCall=fc-01KWHHWR578WWCXQJ6Q0D37PZ3, run=v2c, 1 epoch, data=/data/sft_v2c). ~4-4.5h/$15-18. Bitince adapter → `hukuk-outputs:/v2c` → `modal volume get hukuk-outputs /v2c ./outputs/v2c`. İzle: `modal app logs ap-kKczVUwN4cMj6fodVkaLvK`.

**ADIM 2 erken sinyal (C3 arka planda koşuyor) — cevaplanan-only A1 (yeni araç `scripts/rescore_answered.py`, ABSTAIN_RE ile çekinme ayır, ADR-0011, TÜM modellere tek kural):**
| Model | M1 A1 (cevaplanan) | coverage (cevaplanan/40) | ham macro (çekinme dahil) |
|---|---|---|---|
| v2b | **0.9195** (29 cevap) | **72.5%** | 0.792 |
| base (eval-mirror) | 0.886 (19 cevap) | **47.5%** | 0.483 |
- **🔑 Elmayla-elma çok daha güçlü:** v2b, base'i hem faithfulness'ta (0.92 vs 0.886) hem **coverage'da EZİYOR** (72.5% vs 47.5%): base kırpılmış-context'te **%52.5 çekiniyor** (over-refusal), v2b %27.5. Eski "0.879 vs 0.904" bu iki-boyutlu üstünlüğü gizliyordu. (⚠️ base'in yüksek çekinmesi ABSTAIN_RE-artefaktı mı → C3 bitince spot-check; script'in v2b'yi 0.9195 vermesi orijinal judge-teyitli 0.904'ten hafif yüksek çünkü ABSTAIN_RE 11 çekinme yakalıyor, judge 7 idi — kural tutarlı olduğu için kıyas geçerli.)
- **Kalan ADIM 2:** C3 bitince base/v1 tüm modlarda (M2/M2b/M3/M5) rescore + register + C4 Mecellem baseline (Tablo 1) → tam ADIM 2 yazımı.

---

## v2c icra — ADIM 2: base vs v2b tam tablo (C3 rescore + C1 register) — TAMAMLANDI (2026-07-02)
Otorite: `v2c_roadmap.md` §5 madde 2 + Tier C (C1/C3). **Kullanıcı kararı (2026-07-02): v1 ADIM 2'den DÜŞÜRÜLDÜ** — kıyas = **base vs v2b vs Mecellem (rakip)**; v1 bizim eski/terk-edilmiş turumuzdu (rakip değil), fazla iç-baseline. v1 6-mod re-run öldürüldü (base bittikten sonra), GPU boşa koşmadı. Bugünkü yarım `bench_m1_v1_detail.jsonl` (4 satır) çöpe; **Jun-13 tarihsel v1 eval'i (v2b-vs-v1 audit trail) KORUNDU.**

**Elmayla-elma protokolü:** base ve v2b AYNI harness/mod/n/seed(3407)/hakem(gpt-4o-mini) · A1 = cevaplanan-only (ABSTAIN_RE ile çekinme ayrıldı, `rescore_answered.py`, ADR-0011, TÜM modellere tek kural).

| Mod | Eksen | **base** | **v2b** | Yorum |
|---|---|---|---|---|
| **M1** | A1 grounding (cevaplanan, eval-mirror 900) | 0.886 · cov **47.5%** (19/40) | **0.920 · cov 72.5%** (29/40) | v2b İKİ boyutta üstün (faith + coverage) |
| **M4** | A1 grounding (oracle tavan) | 0.983 · cov 95% (38/40) | 0.975 · cov 100% (40/40) | tavan, bilgi ~eşit |
| **M2** | yanlış-kaynak abstention (rejection) | **0.704** | **0.346** ❌ | **v2b KAYBEDİYOR = G1, v2c'nin ana hedefi** |
| **M2b** | RAG-ıska abstention | 1.0 (n=40) | 0.96 (n=30)* | ikisi güçlü |
| **M3** | boş-kaynak abstention | 1.0 | 1.0 | tavan |
| **M5** | KÖR correctness (A2, düşük=iyi) | 0.225 | 0.175 | ikisi RAG'e dayanıyor (anti-hedef ✓) |
| **A4** | cit_precision (M1 cevaplanan) | 1.0 | 0.931 | base az cevaplıyor→trivial 1.0 |
| **register** | expert_frac (leksik-proxy) | 1.0 | 1.0 | ikisi tam-uzman |

\* **M2b n uyumsuzluğu:** v2b eski koşu n=30, base C3'te n=40. Roadmap "M2b n=40'a tamamla" diyor → v2b M2b n=40 regen **ADIM 6d'de** (v2c 6-mod eval'de v2b baseline'ı da n=40 yeniden ölçülecek). rejection 1.0 vs 0.96 headline geçerli.

**🔑 Üç ana bulgu (paper K1/K3 hammaddesi):**
1. **base BÜTÜN over-refuse ediyor** (kalibrasyon değil, körlük): M1'de gold PROMPT'TA VAR ama base 21/40=%52.5 "Verilen kaynaklarda bu konuyu düzenleyen madde bulunmuyor" diyor → **gerçek red, ABSTAIN_RE artefaktı DEĞİL** (spot-check teyitli). Gürültülü/kırpık context'te pes ediyor. v2b %27.5 → kalibre.
2. **base'in M2/M2b/M3 yüksek rejection'ı bu körlüğün YAN ÜRÜNÜ** — yanlış kaynağı da reddediyor çünkü her şeyi reddediyor. Yani base'in M2=0.704'ü "iyi kalibrasyon" değil "kör red" — ama v2c'nin geçmesi gereken sayı yine de bu.
3. **v2b'nin tek gerçek açığı M2=0.346** (param_leak): yanlış-ama-makul kaynak verilince ezberden doğru cevabı üretip **kaynağı reddetmiyor**. Bilgi (M4 oracle ~0.98 ikisi de) eşit → fark tamamen **davranışsal**. → v2c Tier A (A1 TRAP-abstain + A2 counterfactual) tam bunu hedefliyor.

**Kaynak dosyalar:** `outputs/eval/bench_m{1..5}_{base,v2b}_detail.jsonl` · `gnd_bench_m{1,4}_*` · `abst_bench_m{2,2b,3}_*_summary.json` · `corr_bench_m5_*_summary.json` · `reg_m1_*_summary.json`. Rescore aracı: `scripts/rescore_answered.py`.

**Kalan (ADIM 2'yi kapatmadan önce):** C4 = **Mecellem-Qwen3-4B-TR** rakip baseline (completion-style, foundation-kıyası) → paper Tablo 1. Ayrı alt-görev (aşağıda).

---

## v2c icra — ADIM 2 · C4 Mecellem rakip baseline → TABLO 1 — TAMAMLANDI (6/6 mod, 2026-07-02)
Otorite: `v2c_roadmap.md` §5 madde 2 (C4) + §7 C4. **ADIM 2 KAPANDI** — base·v2b·Mecellem tam 6-mod + register.

**Model & kurulum (paper Tablo 1):** `newmindai/Mecellem-Qwen3-4B-TR` (Qwen3-4B, CPT ~270B token, **instruction-tuned DEĞİL**, Apache-2.0). Kıyas = base/v2b ile AYNI harness/mod/n(40/35)/seed(3407)/hakem(gpt-4o-mini). Foundation-kıyası → **completion-style few-shot** (2 örnek: biri atıflı-cevap biri red; chat-template YOK, roadmap §7·C4). Yeni kod: `gen_eval_grounded.py --completion-fewshot` (izole dal, mevcut pipeline'a risksiz).

**🔧 Kritik bulgu — Mecellem checkpoint'i SIFIR lm_head taşıyor:** Unsloth 4-bit VE düz transformers bf16 ikisinde de ilk çıktı garbage ("!!!!" = token 0 tekrarı). Tanı: `lm_head.weight std=0.0` (tamamen sıfır), `embed_tokens std=0.0245` (sağlıklı). Config `tie_word_embeddings=True` diyor ama checkpoint ayrı (sıfır) bir lm_head da taşıdığı için transformers "ikisi farklı → tie etme" deyip sıfır head'i kullanıyor → tüm logitler eşit. **Fix:** yüklemeden sonra `lm_head.weight = embed_tokens.weight` elle bağla (std<1e-6 tespitiyle). Sonra düzgün, atıflı, kaynağa-sadık Türkçe üretiyor. → `gen_eval_grounded.build_model` completion-fewshot dalına kalıcı yazıldı. (Rakibi düzgün kurmak da elmayla-elma'nın parçası; bu, foundation-kıyas metodolojisinin K-methodology notu.)

### 📊 TABLO 1 — base · v2b · Mecellem (6-mod + register, elmayla-elma, n=40/35, seed 3407, gpt-4o-mini)
| Mod / eksen | base | **v2b (bizim)** | Mecellem (rakip) | Okuma |
|---|---|---|---|---|
| **M1** grounding (gürültü/mirror) | 0.886 · cov 47.5% | **0.920 · cov 72.5%** | 0.918 · **cov 35.0%** | v2b coverage'da 2× |
| **M4** grounding (oracle tavan) | 0.983 · cov 95% | 0.975 · **cov 100%** | 0.921 · **cov 45.0%** | rakip oracle'da bile %45 |
| **M2** yanlış-kaynak abstention | 0.704 | **0.346** ❌ | 1.0* | *kör-red (coverage-çöküş yan ürünü) |
| **M2b** RAG-ıska abstention | 1.0 | 0.96 | 0.919 | üçü de güçlü |
| **M3** boş-kaynak abstention | 1.0 | 1.0 | 1.0 | tavan, ayrışma yok |
| **M5** KÖR correctness (düşük=iyi tasarım) | 0.225 | 0.175 | **0.35** | rakip ezberden çok biliyor (CPT); bizde düşük=RAG-tasarımı |
| **register** expert_frac | 1.0 | 1.0 | 0.2 (mean 0.6) | rakip daha az uzman-register |

**⚠️ M2=1.0 yorumu (kritik, yanıltmasın):** Mecellem'in M2=1.0'ı "mükemmel kalibrasyon" DEĞİL — coverage çöküşünün diğer yüzü. Her şeyi reddettiği için (M1 cov %35, M4 %45) yanlış-kaynağı da reddediyor (base'in M2b=1.0 kör-red artefaktıyla aynı mekanizma). **Paper trade-off bulgusu:** yanlış-kaynak abstention ↔ coverage arasında gerilim → rakip "hepsini reddet" köşesinde (M2 mükemmel ama kullanılamaz, cov %35-45), v2b "yanlışı da cevapla" köşesinde (M2 0.346, cov yüksek). **v2c'nin hedefi = iyi köşe: yüksek M2 + yüksek coverage birlikte** (§6). M2'yi tek başına kıyaslama; M2 × coverage birlikte oku.

**🔑 Tablo 1'in 4 ana bulgusu (paper K1/K3):**
1. **Coverage rakibi eziyor:** Mecellem cevap verdiğinde sadık (M1 A1=0.918 ≈ v2b) ama oracle'da bile %45, gürültüde %35 cevaplıyor. v2b %100/%72.5 → **asıl deployment ekseninde (coverage) 2×**, eşit faithfulness'ta. Rakibin instruct-olmaması bağlamı kullanamama olarak yansıyor.
2. **Abstention'da rakip de iyi** (M2b 0.919, M3 1.0) — yani zayıflığı reddetme değil, **az-cevaplama**.
3. **M5 KÖR'de rakip yüksek** (0.35 vs v2b 0.175): 270B-token CPT'nin parametrik hukuk ezberi. Bizim tasarımda düşük M5 = **RAG'e-dayanma kanıtı** (anti-hedef, §6 Tip-C) → rakibin yüksek M5'i "üstünlük" değil farklı-tasarım (CPT ezber). Paper'da böyle çerçevele.
4. **register:** Mecellem expert_frac 0.2 (bizimki 1.0) — completion-style + CPT daha az resmî-atıf dili. Bizim uzman-register tasarımı net ayrışıyor.

**Metodoloji notu (K-methodology):** rakibi düzgün kurmak elmayla-elma'nın parçası. Mecellem checkpoint'i SIFIR lm_head taşıyor (std=0.0) + config tie=True → transformers "ikisi farklı→tie etme" deyip sıfır head kullanıyor → garbage "!!!!". Fix: yüklemeden sonra `lm_head.weight = embed_tokens.weight` elle tie (std<1e-6 tespitiyle), `gen_eval_grounded.build_model` completion-fewshot dalına kalıcı. Rakibi kırık kurup "biz kazandık" demek geçersiz olurdu.

**📄 Mecellem paper bağlamı (arXiv 2601.16018, "Mecellem Models: Turkish Models Trained from Scratch and Continually Pre-trained for the Legal Domain", newmindai) — 2026-07-02 tarandı:**
- **CPT-only, instruction-tuned DEĞİL** (§3.4.3 "CPT applied directly as continuation on Qwen3-Base"). SFT/chat-template/RLHF yok → completion-style kurulumumuz DOĞRU.
- **Qwen3-4B = TEK-fazlı CPT, 270.8B token** (academic+legal+legislation+web). 4-fazlı curriculum yalnız 1.7B'ye. Ağır CPT → yüksek M5 KÖR (0.35 parametrik ezber) tutarlı.
- **🔑 Onların eval'i SADECE PERPLEXITY** (%36.2 düşüş) + decoder→encoder çevirip MTEB-TR retrieval. **Hiç QA/grounding/abstention/RAG generatif eval'i YOK.** → **Mecellem'i generatif RAG eksenlerinde ilk ölçen BİZİZ** (paper katkısı: "generatif eksende ilk foundation ölçümü").
- **🔧 Sıfır-lm_head AÇIKLANDI:** model embedding/RAG-base olarak (decoder→encoder) konumlandığından generatif lm_head hiç eğitilmemiş/doğrulanmamış → sıfır kalmış. Tie-fix generatif kullanım için zorunlu. Paper metodoloji notu.
- **Konumlama:** embedding/RAG-pipeline base'i, chat/instruct değil → generatif kıyas "off-label" ama en yakın TR hukuk decoder foundation'ı = meşru foundation-baseline. Paper'da "foundation kıyası" + "off-label generatif ölçüm" diye çerçevele; "instruct elmayla-elma" DEME.
- Kaynak: `https://arxiv.org/abs/2601.16018` · HF `newmindai/Mecellem-Qwen3-4B-TR` (Apache-2.0).

**Kaynak dosyalar:** `outputs/eval/bench_m{1,4}_mecellem_detail.jsonl` · `gnd_bench_m{1,4}_mecellem*`. Driver: `scratchpad/run_mecellem.sh` (PID 6106 koşuyor).

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
