# PARKING NOTE — 2026-07-08 — Benchmark manzarası + NewMind stack + GPU/compute istihbaratı

> ✅ **İŞLENDİ (2026-07-08) → `ADR-0016` + research_log **#35** (`2026-07-08-benchmark-manzara-newmind-stack.md`) + `knowledge/summary_eval_benchmark_literature.md` (§TR manzara) + memory `benchmark-positioning`/`eval-harness-decision`/`paper-target`.**
> Bu dosya ham kaynak/scratch olarak tutulur; otoriter kayıt yukarıdaki doclardır. İstenirse silinebilir.
> Tetik: "BigLaw-Bench'e modeli soksak mı?" sorusu → dış-benchmark & rakip taraması.

---

## 0. Ana soru & verdict

**Soru:** modeli `harveyai/biglaw-bench`'e (ya da benzeri "büyük" dış benchmark'a) sokup frontier'a göre konumlansak mı?

**Verdict: HAYIR (scoreboard olarak). Off-axis.**
- BigLaw-Bench = İngilizce + US/UK common law + elit associate draftlama. Bizimki = Türkçe + TR medeni hukuk + grounded QA.
- Farklı dil + farklı hukuk sistemi = **farklı ders.** Düşük skor "model kötü" değil "yanlış sınav" demek → **yorumlanamaz sayı = ispat değil gürültü.**
- BigLaw ayrıca **vendor/blog benchmark'ı** (peer-reviewed değil) → paper kredibilitesi için LegalBench'ten bile zayıf.

**Kullanım:** BigLaw & LegalBench → sadece **Related Work cite'ı** (koşma). LegalBench = `HazyResearch/legalbench`, NeurIPS 2023, hakemli ama yine İngilizce/US → TR-grounding ispatı vermez.

---

## 1. TR hukuk benchmark manzarası (2026-07)

**Senin ekseni (üretken TR hukuki cevap + grounding + abstention + citation + vatandaş↔uzman register) ölçen tanınmış benchmark YOK.** → **Boşluk = paper'ın asıl kozu.**

| Kaynak | Tip | Bize faydası |
|---|---|---|
| TR-MMLU / TurkishMMLU / MMLU-Pro-TR | Genel MC, "hukuk" alt-kategorili | On-language "genel hukuk bilgisi" sanity sayısı (lisans uyarısı ↓) |
| Cetvel / TurkBench / TARA / TrGLUE | Genel Türkçe LLM | Genel yetenek regresyon kontrolü, hukuk-spesifik değil |
| HukukBERT | Encoder, Legal Cloze Test + segmentasyon | Üretken değil, bizim eksen değil |
| Mecellem (aş.) | Retrieval/embedding | Rakip değil, Faz 2 retriever adayı |
| LEXam | 340 hukuk sınavı ama **İngilizce+Almanca** | TR değil |

### alibayram/turkish_mmlu — DİKKAT (kırmızı çizgi)
- 293K soru, 67 bölüm, hukuk dahil. **AMA:**
- **Lisans: CC BY-NC 4.0** → ticari kullanım YASAK (repo private+ticari).
- Kart: *"Telif hakkı içeren sorular bulunabilir"* → **EuroHPC'de yandığımız copyright poison** riski.
- **Karar:** ana benchmark/eğitim parçası YAPMA. En fazla dahili, tek-seferlik, yayınlanmayan sanity + hukuk dilimini EDA'dan geçir. Temiz istiyorsak hukuk-MC'yi public kaynaktan kendimiz kurarız.

---

## 2. NewMind AI stack anatomisi (`newmindai` HF org)

TR hukukta **tam yığın** kuruyorlar — senin en yakın referansın. Üç aile:

**A) Mursit** = embedding/retrieval (*kütüphaneci*). Mursit-Large/Base, ColBERT-hash, bge-m3. → Faz 2 retriever adayları.

**B) Mecellem** = generative decoder, **Apache-2.0**, `text-generation`:
- `Mecellem-Qwen3-1.7B-TR`, `Mecellem-Qwen3-4B-TR`
- 4B: Qwen3-4B base, **tek-faz CPT, 270.8B token** (hukuk + genel TR web). 36 layer, GQA, RoPE.
- ⚠️ **CPT-only** — instruction/QA hizalaması YOK. Bilgi enjekte edilmiş base.
- ✅ İndirilip koşulabilir → **gerçek head-to-head baseline'ımız.** ("CPT'li 4B base vs bizim task-aligned SFT/ORPO SLM, aynı üretken benchmark'ta" = adil, güçlü tablo.)
- **DÜZELTME:** önceki "Mecellem'in üretken decoder'ı yok" ifadesi YANLIŞTI. Paper decoder'ı *kendi eval'i için* encoder'a çeviriyor (o yüzden paper'da üretken sayı yok), ama **release edilen checkpoint generative.**

**C) Muhakim** = **reward/evaluator (JUDGE) modeli** — QA rakibi DEĞİL:
- Skywork-Reward-V2-Llama-3.1-8B üstüne, 8B, Apache-2.0.
- **5 boyutta puan:** statute reference accuracy · legal accuracy · case law reference quality · linguistic coherence · depth coverage.
- **Bu boyutlar bizim eksenlerle ~bire bir** (A1 groundedness, legal-accuracy kapısı).
- **Register düzeltmesi:** "sadelik/vatandaş-dili ekseni yok → avukatça derinlik ödüllendirir" bir KUSUR DEĞİL. Register hedefi **ADR-0010 ile uzman/avukat'a döndü** → Muhakim'in biası artık bizim eğitim hedefiyle HİZALI.

### Neden gündeme geldi (motivasyon — kayıt için)
Şu an **tüm skorlarımız tek hakemden (GPT-4o-mini)** → tek-hakem akademik olarak zayıf (RAGBench/RAGTruth insan/ikinci-hakem doğrulaması bekler). **Çapraz-hakem** kredibiliteyi artırır ("iki bağımsız hakem aynı yöne işaret ediyor"). Muhakim, TR-hukuka özel domain-spesifik bir çapraz-hakem **adayıydı** — AMA judge olarak kabul için önce **GPT-4o-mini ile agreement testi** geçmesi gerekirdi (kalibrasyon şartı).

### KARAR (2026-07-08): Muhakim'i JUDGE olarak KOŞMUYORUZ — cite ediyoruz.
> Çapraz-hakem ihtiyacı **gpt-4o (ikinci hakem) ile zaten karşılanıyor** → Muhakim'in agreement testi ERTELENDİ değil, GEREKSİZ. Model+script hazır bekliyor; ileride istenirse test edilebilir.
**Reddetme sebepleri:**
1. **Gerek yok.** Hakem-geçerliliği zaten karşılanıyor: kendi scorecard'ımız + law-MMLU sanity + var olan **cross-judge (gpt-4o-mini ↔ gpt-4o via `judge_agreement.py`)**. Muhakim marjinal değer katmıyor.
2. **Copyright/veri kirliliği bağı.** Muhakim `newmindai/EuroHPC-Legal` (116 QA) üstünde eğitilmiş/benchmarklanmış — o dataset'i EDA'da **zaten REDDETTİK** (mismatched Q&A, uydurma kanun, Osmanlıca içerik; bkz. VERI_PLANI). Reddettiğimiz veriyle kalibre edilmiş bir hakeme skorlarımızı bağlamak, reddetme gerekçemizle çelişir.
- `models/Muhakim` (15GB) indirili + `muhakim_judge.py` hazır DURUYOR → ileride istersek koşulabilir, ama şu an **beklemede/iptal.** Lokalde fire edilmedi (kullanıcı kararı).
- **Rolü:** Related Work **atıfı** (NewMind stack'inin judge bileşeni). Koşulan baseline DEĞİL, kıyaslanan rakip DEĞİL.

---

## 3. Compute / GPU istihbaratı

**NewMind "para yakmamış" — grant almış.** Kart: *EuroHPC JU project **etur46**, MareNostrum 5 (BSC Barcelona), 400× H100 / 100 node* + **TRUBA (TÜBİTAK)**. Çıktı Apache-2.0 (muhtemel grant şartı).

**Reality check:** biz MareNostrum ölçeği gerektirmiyoruz. 12B QLoRA = **tek GPU** işi (Modal planı zaten yeterli). Grant çabası ancak *from-scratch/CPT'ye* geçersek anlamlı.

**Bize açık iki kapı (ileride gerekirse):**
- **TRUBA (yerli, en gerçekçi):** 312 GPU (A100/H100/H200). İyi kuyruklar (kolyoz/palamut) kapalı — araştırma merkezi altyapı projesi / ULAKBİM sözleşmeli proje ister. Başvuru: ARDEB + bütçe → `ardeb@ulakbim.gov.tr`. Üniversite/TÜBİTAK afiliasyonu iyi kuyruğu açar.
- **EuroHPC AI Factories — Industrial Innovation track:** AI SME/startup'a **ÜCRETSİZ** (Playground / Fast Lane ≤50k GPU-saat / Large Scale). Ticari-private duruşumuza uyan yol BU (bilimsel-açık calls değil). ⚠️ **Türkiye 2026 uygunluğu doğrulanmadı** — teyit gerek.
- **IP uyarısı:** bilimsel calls açık-çıktı bekler → private/commercial ile çelişir. Industrial Innovation / pay-per-use IP'yi korur.

### MN5 ULUSAL çağrı fizibilitesi (2026-07-08, başvuru formu incelendi — TÜBİTAK ULAKBİM üzerinden MareNostrum 5)
Kaynak: `indico.truba.gov.tr/e/marenostrum5` · `mn5@ulakbim.gov.tr` · **rolling, son tarih 31 Ara 2026**, değerlendirme 15 iş günü.
**Uygunluk:** PI'ın Türkiye'de yerleşik kuruma bağlı olması yeter — **özel sektör/endüstri KABUL** → egeist.com.tr üzerinden PI olunabilir, üniversite ŞART DEĞİL. İş sözleşmesi tahsis bitiminden ≥3 ay sonra geçerli olmalı.
**Zorunlu:** kurumsal e-posta (gmail RED — `ferhat.ersoy@egeist.com.tr` mevcut ✅) · ARBİS CV PDF (her araştırmacı) · iş-zaman çizelgesi + kaynak yönetim planı (şablon) · proje özeti/etki (2000'er krkt) · ≤20 DOI referans · kaynak çekirdek-saat (1 GPU=20 çekirdek, H100 ACC) · sivil-amaç + KVKK.
**Zayıf noktalar (rekabette risk):**
1. **HPC track-record YOK** → form "önemli avantaj" diyor; en büyük eksik. Mitigasyon: önce TRUBA ile deneyim, ya da ekibe HPC'li akademisyen.
2. **Ölçek gerekçesi:** 12B QLoRA=tek GPU → pre-exascale MN5'i hak etmez, reddedilir. MN5 ancak from-scratch/CPT/dev-sweep gibi **büyük iş** için mantıklı. → "yükseğe çıkma" stratejisi buraya bağlı.
3. **Gizlilik vs yaygınlaştırma:** kabul halinde proje özeti+çıktılar kamuya açılabilir → private/proprietary ile kısmi çelişki (form gizlilik beyanına izin veriyor ama özet-görünürlük kaçınılmaz). Paper hedefiyle uyumlu, tam-gizlilikle değil.
**AKTİVASYON KOŞULU (2'si birlikte):** (a) kurumsal afiliasyon [egeist yeter, email hazır] + (b) ölçeğe-layık proje [from-scratch/CPT]. "Yükseğe girme" (üniversite/doktora) her iki zayıf noktayı birden çözer. Faz 1 için GEREKSİZ; ileride ölçek büyürse aktive.

---

## 4. Paper kredibilite stratejisi (özet)

- **Frontier'a göre konumlanma** → BigLaw değil, **kendi TR benchmark'ında frontier baseline** (GPT-4o/Claude/Gemini, blind+RAG). "Blind-vs-RAG ceiling" framing'i zaten bu.
- **Dış on-axis sayı** → TR-MMLU hukuk alt-kümesi (lisans-temiz sürümle) = genel yetenek sanity.
- **Head-to-head** → Mecellem-Qwen3-4B-TR ağırlıklarını biz koştururuz.
- **Judge kredibilitesi** → GPT-4o-mini + (agreement geçerse) Muhakim çapraz-judge.
- **Dış cite** → LegalBench + BigLaw-Bench (Related Work).
- **Katkı framing'i** → "mevcut TR hukuk stack'i retrieval'a odaklı (NewMind/Mecellem/Mursit); üretken cevabın grounding/abstention/citation kalitesini kimse ölçmüyor → ilk üretken TR hukuk grounding benchmark'ı + niş SLM biziz."

---

## 5. Doclara İŞLENECEK (sonraki oturum) — bekleyen düzeltmeler

- [ ] `knowledge/summary_eval_benchmark_literature.md`: "TR legal benchmark landscape (2026-07)" + "NewMind stack anatomisi" + "BigLaw/LegalBench = off-axis, cite-only" ekle.
- [ ] `CLAUDE.md`/memory `eval-harness-decision`: "Muhakim skipped" satırını **gerekçelendir** → yukarıdaki KARAR (gerek yok: scorecard+law-MMLU+cross-judge zaten var; + EuroHPC-Legal kirliliği bağı). Cite-only olarak kalır.
- [ ] Related Work atıf listesi netleşti: Mecellem, HukukBERT, Muhakim, METU-framework, LegalBench, LEXam, TurkishMMLU. Kıyas-seti (koşulan): base Gemma-12B + Mecellem-4B + frontier (GPT-4o/Claude blind+RAG).
- [ ] (opsiyonel) EuroHPC Türkiye uygunluğu + TRUBA başvuru fizibilitesi → ayrı araştırma. Faz 1 (12B QLoRA=tek GPU) için GEREKSİZ; ancak from-scratch/CPT'ye geçilirse.

### ✅ İptal olan / gerçekleşmeyen maddeler (repo taraması sonrası — parking notu §2'yi ezer)
- ~~"Mecellem decoder rakip framing'i yanlış, düzelt"~~ → **YANLIŞ ALARM.** Repo zaten Mecellem-4B'yi **6 modülde baseline koşmuş** (M1 faith 0.71 / M5 correct 0.35 / M2-M3 rej 1.0 …). Framing repo'da doğru; benim web-resmim eksikti.
- ~~"Muhakim agreement testi koş"~~ → **İPTAL** (yukarıdaki KARAR: gerek yok + veri kirliliği bağı).
- ~~"Mecellem head-to-head eklenmeli"~~ → **ZATEN VAR.**

---

## Kaynaklar

- BigLaw-Bench: github.com/harveyai/biglaw-bench
- LegalBench: github.com/HazyResearch/legalbench · NeurIPS 2023
- LEXam: lexam-benchmark.github.io
- Mecellem paper: arxiv.org/abs/2601.16018
- Mecellem-Qwen3-4B-TR: huggingface.co/newmindai/Mecellem-Qwen3-4B-TR
- Muhakim: huggingface.co/newmindai/Muhakim
- alibayram/turkish_mmlu: huggingface.co/datasets/alibayram/turkish_mmlu (CC BY-NC 4.0)
- TR-MMLU/TurkishMMLU: arxiv.org/abs/2407.12402 · MMLU-Pro-TR: huggingface.co/datasets/bezir/MMLU-pro-TR
- Cetvel: arxiv.org/abs/2508.16431 · TurkBench: arxiv.org/abs/2601.07020
- EuroHPC AI Factories access: eurohpc-ju.europa.eu/ai-factories/ai-factories-access-modes_en
- EuroHPC Development Access: eurohpc-ju.europa.eu/eurohpc-ju-call-proposals-development-access_en
- TRUBA docs: docs.truba.gov.tr · başvuru: ardeb@ulakbim.gov.tr
