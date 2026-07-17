## 2026-07-08 · Dış-benchmark manzarası + NewMind stack anatomisi (yan-iş tarama)

**Ne yapıldı:** "Modeli BigLaw-Bench'e (harveyai) soksak mı, frontier'a göre konumlansak mı?" sorusundan başlayan dış-benchmark + rakip-manzara taraması (web-search + HF model kartları). Karar → **ADR-0016**. Ham kaynak/parking: `_PARKING-2026-07-08-benchmark-gpu-newmind-scan.md` (işlendi).

**Bulgular:**

**1. BigLaw-Bench / LegalBench = off-axis → cite-only.** BigLaw (Harvey, vendor/blog benchmark, İngilizce US/UK common-law, elit associate draftlama) ve LegalBench (HazyResearch, NeurIPS 2023, hakemli ama yine İngilizce/US, 162 task IRAC) → TR medeni-hukuk üretken modelimizin ekseninde değil. Düşük skor yorumlanamaz (model mi kötü, sınav mı yanlış — ayrılamaz). LEXam (340 sınav) = İngilizce+Almanca, yine değil. **Büyük + yanlış-eksen = büyük gürültü**; "büyük benchmark kredibilite verir" içgüdüsü doğru ama enstrüman yanlış.

**2. TR hukuk benchmark manzarası — üretken grounding/abstention benchmark'ı YOK.** Tanınan setler başka eksende: TR-MMLU/TurkishMMLU/MMLU-Pro-TR (genel MC, "hukuk" alt-kategorili), Cetvel/TurkBench/TARA/TrGLUE (genel Türkçe LLM), HukukBERT (encoder Legal Cloze). Boşluk = katkımız (paper-target ile tutarlı).

**3. alibayram/turkish_mmlu — lisans/poison bayrağı.** 293K soru (hukuk dahil) AMA **CC BY-NC 4.0** (ticari yasak) + "telif içeren sorular bulunabilir" (EuroHPC-Legal'de yandığımız poison türü). → eğitim/ana-benchmark'a KOYMA.

**4. NewMind AI stack anatomisi** (`newmindai` HF org) — TR hukuk tam yığın, ama farklı eksen:
- **Mursit** = embedding/retrieval ailesi (ColBERT-hash, bge-m3, Mursit-Large/Base). → Faz-2 retriever adayı.
- **Mecellem-Qwen3-1.7B/4B-TR** = generative decoder, Apache-2.0, `text-generation`. 4B: Qwen3-4B base, tek-faz **CPT 270.8B token** (hukuk+genel TR). **CPT-only, instruction/QA hizalaması yok** → chat-template güvenilir takip etmez (repo `gen_eval_grounded.py` notu teyitli). Bizde ZATEN 6-mod baseline koşulu (research_log #23/#31, SCORECARD): M1 faith 0.71 / M5 correct 0.35 / M2-M3 rej 1.0. ✅ head-to-head var.
- **Muhakim** = **reward/evaluator (judge) modeli** — cevap üretmez, PUANLAR. Skywork-Reward-V2-Llama-3.1-8B, 8B, Apache-2.0. 5 eksen: statute_reference, legal_accuracy, case_law_reference, linguistic_coherence, depth_coverage. `EuroHPC-Legal` (116 QA) ile eğitilmiş/benchmarklı → **bizim reddettiğimiz dataset.** "Sadelik ekseni yok" ama register hedefi ADR-0010 ile uzman'a döndüğü için artık HİZALI, kusur değil.

**5. Muhakim judge kararı:** cite-only, koşulmuyor (ADR-0016 §3). Hakem-geçerliliği zaten cross-family judge planıyla (gpt-4o-mini + gpt-4o/Claude/Gemini) karşılanıyor; + EuroHPC-Legal kirliliği. `models/Muhakim` (15GB) + `muhakim_judge.py` hazır bekliyor. Motivasyon kaydı: tek-hakem akademik olarak zayıf → çapraz-hakem kredibilite artırır → Muhakim domain-spesifik adaydı ama gpt-4o/Claude/Gemini bu rolü zaten dolduruyor.

**6. Compute/grant istihbaratı (MN5/EuroHPC/TRUBA):** NewMind MareNostrum 5'i (EuroHPC project **etur46**, 400×H100/100 node) + TRUBA ile kullanmış — **cepten para değil, grant.** Çıktı Apache-2.0 (grant şartı). Bize açık yollar:
- **TRUBA** (yerli, en gerçekçi): 312 GPU (A100/H100/H200); iyi kuyruklar (kolyoz/palamut) akademik/altyapı-proje ister; ARDEB → `ardeb@ulakbim.gov.tr`.
- **EuroHPC AI Factories — Industrial Innovation**: AI SME'ye ücretsiz (Playground/Fast Lane ≤50k GPU-saat/Large Scale); TR uygunluğu doğrulanmadı.
- **MN5 ULUSAL çağrı** (TÜBİTAK ULAKBİM, `indico.truba.gov.tr/e/marenostrum5`, rolling — son tarih **31 Ara 2026**, değerlendirme 15 iş günü): **özel-sektör PI KABUL** (egeist yeter, üniversite şart değil); **kurumsal e-posta zorunlu** (gmail RED — `ferhat.ersoy@egeist.com.tr` hazır ✅); ARBİS CV + proje önerisi + iş-zaman çizelgesi. ⚠️ zayıf noktalar: (a) HPC track-record yok ("önemli avantaj" eksik), (b) 12B QLoRA=tek GPU → pre-exascale'i hak etmez (ancak from-scratch/CPT için mantıklı), (c) kabulde özet+çıktı kamuya açılabilir (private/proprietary ile kısmi çelişki). **Aktivasyon = kurumsal afiliasyon + ölçeğe-layık proje** ("yükseğe girme"/üniversite her iki zayıfı çözer). Faz-1 için gereksiz.

**Sonuç / ders:** Dış "büyük benchmark" kredibilite sağlamaz eğer eksende değilse. Kredibilite = kendi canon setinde frontier+rakip baseline + cross-family judge. Repo bu konumlamayı zaten büyük ölçüde tutuyordu (research_log #31, TODO); bu tarama onu dış-manzarayla sağlamlaştırdı + Muhakim/BigLaw/alibayram kapsam kararlarını netleştirdi (ADR-0016).

**Kaynak:** ADR-0016 · `_PARKING-2026-07-08-benchmark-gpu-newmind-scan.md` · HF: `newmindai/Mecellem-Qwen3-4B-TR`, `newmindai/Muhakim` · `knowledge/summary_eval_benchmark_literature.md` (§TR manzara) · MN5 çağrı: `indico.truba.gov.tr/e/marenostrum5`.
