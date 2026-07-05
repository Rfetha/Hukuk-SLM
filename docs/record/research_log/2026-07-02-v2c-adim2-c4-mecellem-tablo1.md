## v2c icra — ADIM 2 · C4 Mecellem rakip baseline → TABLO 1 — TAMAMLANDI (6/6 mod, 2026-07-02)
Otorite: `v2c/roadmap.md` §5 madde 2 (C4) + §7 C4. **ADIM 2 KAPANDI** — base·v2b·Mecellem tam 6-mod + register.

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

