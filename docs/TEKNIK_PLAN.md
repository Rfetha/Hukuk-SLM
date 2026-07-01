# HakHukuk — Teknik Plan

> Bu doküman `VISION.md`'deki 5 fazlı yol haritasını teknik, uygulanabilir adımlara çevirir.
>
> **Kapsam:**
> - **Bölüm 1 — Yol Haritası:** Tüm fazlar (1-5), konu başlıkları + adım akışı.
> - **Bölüm 2 — Execute Planı:** Yalnızca **Faz 1** (fine-tuned hukuk SLM). Detaylı, adım adım.
> - **Bölüm 3 — Kilitli Kararlar** (grill-me oturumu, 2026-05-29).
>
> **Çerçeve:** Şimdilik **private repo + proprietary lisans** — ticari hak sahipte. Repo private, model ağırlıkları + model kartı ileride HF'te public olabilir. Akademik makale kapısı kapalı değil: ileride gerekirse açılır. Rigor/tekrar-üretilebilirlik (sabit seed, loglu koşular, temiz ablation) korunur. Faz sırası katıdır (`VISION.md §2`).

---

# BÖLÜM 1 — TÜM PROJE YOL HARİTASI

## Faz 1 — Hukuk Okuryazarı SLM — *AKTİF*
> ⚠️ **SÜPERSED (2026-06-13, ADR-0010) → güncel:** hedef "vatandaş diliyle konuşan" DEĞİL; birincil register = **uzman/hukukçu**, kaynak-dayalı. Vatandaş sadeleştirmesi = app-layer prompt modu (model eğitim hedefi değil). Correctness/grounding RAG'den gelir. Aşağıdaki eski ifade iz olarak korunuyor.
> ⚠️ **SÜPERSED (2026-06-14, V2_PLAN.md) → güncel plan:** aktif iş artık **v2b SFT** (base'den taze QLoRA), bu bölümdeki v0→v1 execute akışı tamamlandı/tarihsel. Güncel yön: `docs/V2_PLAN.md §9` + `NEXT_SESSION.md`.

**Hedef:** Türk hukuk diline adapte, **~~vatandaş diliyle~~ uzman-register ile** konuşan, ölçülebilir fine-tuned SLM. Kalite barı yüksek — üzerine kurulacak ekosistem (RAG, agent, UI) buna dayanacak.
**Baz model (güncellendi 2026-06-07):** **Gemma 4 12B** (`google/gemma-4-12B-it-qat-q4_0-unquantized`, Apache 2.0) — multimodal, 256K context. Deploy pipeline: QLoRA SFT → merge → Q4_0 GGUF (~6.5GB, 8GB VRAM end-user).

Adım akışı: Ortam → Smoke test → Veri toplama → Temizleme/format → Sadeleştirme → Base hazırlığı → v0 baseline → Grounded üretim → SFT iterasyonları → Eval → Ablation → Yayın.
→ Detay **Bölüm 2**.

## Faz 2 — Güncel Bilgi: RAG + Knowledge Graph
> **TurboQuant notu:** 256K context uzun kanun/içtihat metinleri için KV-cache kritik — TurboQuant (3-4 bit, eğitimsiz, online) Faz 2 RAG serving'de değerlendirilir. Bkz. `knowledge/summary_turboquant.md`.

1. Hukuk metni yapı çıkarımı (kanun→madde→fıkra→atıf parser)
2. Bedesten API ile bulk kanun çekimi (taze) + içtihat (yargi-mcp RE)
3. Graph DB (Neo4j/Memgraph) şema tasarımı
4. Embedding: `newmindai/Mursit-Base-TR-Retrieval` aday
5. Hibrit getirme (graph traversal + vektör)
6. Vanilla RAG vs Graph-RAG deneyi
7. Atıf doğrulama (halüsinasyon önleme)

> **İçtihat:** Tüm 15 kurum (Yargıtay, Danıştay, AYM×2, GİB, KİK, Rekabet, Sayıştay, BDDK, KVKK, Sigorta…) `yargi-mcp`'den reverse-engineer edilmiş, harita hazır: `docs/YARGI_KAYNAKLARI.md`. %100 in-house.

## Faz 3 — Model Serving + Agentic Workflow + App
> Agent altyapısı olmadan niş özellikler inşa edilemez — önce foundation kurulur.

**Serving:**
1. Model serving (vLLM + GGUF → FastAPI REST endpoint)
2. TurboQuant KV-cache entegrasyonu (256K context, 4.5× sıkıştırma)

**Agent + App:**
3. Agent framework (LangGraph/custom) — referans: `github.com/willchen96/mike`
4. Araç entegrasyonu (TÜFE API, RAG sorgu, Bedesten canlı)
5. Çok adımlı akışlar (soru → veri çek → hesapla → taslak üret)
6. Dilekçe şablon sistemi (Arabuluculuk, Hakem Heyeti, itiraz)
7. **Post-SFT RL altyapısı:** no-code UI ile hukukçu/kullanıcı feedback → DPO/RLHF döngüsü
8. **App:** Web first monorepo (Next.js 14 TS + FastAPI Python). Avukat portalı MVP → vatandaş portalı sonra. Spec: `docs/superpowers/specs/2026-06-07-hakhukuk-web-app-design.md`

**Multimodal Input:**
9. Belge fotoğrafı / OCR pipeline (`visual_tokens=560-1120`)
10. Sesli soru input pipeline (audio → hukuki yanıt)

## Faz 4 — Niş Uzmanlıklar
> Faz 3'teki agent altyapısı üstüne domain-specific özellikler eklenir.

1. İlk niş (Kira/İş/Tüketici — maddeleri zaten etiketli)
2. Niş veri (senaryo→dilekçe, GPT-4o-mini grounded)
3. Niş eval rubriği
4. Niş prototipi (agent framework üstünde)

## Faz 5 — Vatandaş Platformu
1. Web arayüzü (mobil öncelikli)
2. e-Devlet/UYAP entegrasyonu (yargi-mcp → in-house RE)
3. e-Tebligat asistanı
4. Sürekli iyileştirme döngüsü

---

# BÖLÜM 2 — FAZ 1 EXECUTE PLANI

> İşaretleme: **[İŞ]** = yapılacak somut iş. **ℹ️ Bilgi** = teknik öğretici not.
> **Ortam: WSL2 (Ubuntu 22.04)** — tüm işler buradan. Veri pipeline'ı da WSL2'ye taşınacak.

## Adım 1 — Geliştirme Ortamı
**Amaç:** RTX 5070 (12 GB, Blackwell sm_120) + QLoRA eğitimi için tekrar üretilebilir ortam.

- **[İŞ]** WSL2 (Ubuntu 22.04) → CUDA (**Blackwell-uyumlu sürüm**, 13.1 değil — kurulumda doğrulanacak) → uv + Python 3.11 → PyTorch (sm_120 destekli) → unsloth, bitsandbytes, transformers, trl, peft, datasets, accelerate, flash-attn.
- **[İŞ]** `requirements` kilitle, seed sabitle, W&B bağla.

> **ℹ️ Bilgi — Blackwell tuzağı:** RTX 5070 sm_120 + CUDA 13.1 çok yeni. `bitsandbytes`, `flash-attn`, `Unsloth` hepsi **son Blackwell-uyumlu wheel** gerektirir — eski sürümler sm_120 görmez. Kurulumda her kütüphanenin Blackwell-compat sürümünü doğrula; FINE_TUNING.md'deki "CUDA 12.1" geçersiz.

> **ℹ️ Bilgi — neden WSL2?** `bitsandbytes`/`flash-attn` Linux'ta çok daha az sorun. WSL2 = Windows içinde gerçek Linux çekirdeği, GPU görür.

**Çıktı:** `nvidia-smi` GPU'yu görüyor, kilitli ortam, Blackwell-compat stack.

## Adım 2 — Smoke Test
**Amaç:** Eğitim hattının uçtan uca çalıştığını kanıtlamak (kaliteden bağımsız).

- **[İŞ]** Küçük model (**Gemma 3 270M** veya benzeri) + ~100 örnek, 1-2 epoch.
- **[İŞ]** LoRA adapter kaydet → yükle → çıkarım. W&B'ye loss logla.

**Başarı:** Hatasız bitiyor, adapter kaydediliyor, çıktı üretiyor.

## Adım 3 — Veri Toplama
→ Detay: `docs/VERI_PLANI.md`

- **[İŞ]** Doğrulanmış Q&A: `OrionCAF` (18K, Apache) + `Renicames` (14.8K, Apache). sft_v0 zaten hazır: `data/processed/sft_v0/` (32.234 çift).
- **[İŞ]** Kanun zemini: `data/raw/mevzuat_maddeler.jsonl` zaten hazır (40.496 madde, 907 kanun).
- **[İŞ]** Bulk kanun çekimi (taze, kategorize): Bedesten API ile 916 kanunu `data/raw/mevzuat/{TUR}/` altına çek. Script: `scripts/bedesten_probe.py` → genişletilecek.

> **Lisans kuralı (katı):** Lexpera/Kazancı vb. ticari → yasak. Kapsam: güncel TC mevzuatı.

## Adım 4 — Veri Temizleme & Sadeleştirme
> ⚠️ **SÜPERSED (2026-06-08 / ADR-0010) → güncel:** "32K'yı sadeleştir" adımı **İPTAL** — sadeleştirme app-layer'a taşındı, model eğitim hedefi değil. Ayrıca 32K forum verisi v0'ı batırdı (base-altı doğruluk, research_log 2026-06-07/08) ve v1/v2b'ye **katılmadı**. Aşağıdaki adım iz olarak korunuyor; uygulanmadı.

**Amaç (tarihsel):** 32K uzman-dilli veriyi sadeleştir + temizle → sade-dil SFT setine dönüştür.

- **[İŞ] ~~32K'yı GPT-4o-mini ile sadeleştir:~~ İPTAL (ADR-0010)** uzman cevabı → vatandaş-dili cevap (~$13, OpenAI API key hazır). *(sadeleştirme app-layer prompt modu.)*
- **[İŞ]** Temizleme zinciri (Mecellem reçetesi): exact-hash → SemHash (0.75) → FineWeb → GlotLID (TR only) → Zemberek (suffix>%75, lemma>%50) → token ≤4096 → PII maskeleme.
- **[İŞ]** Kira(6098)/İş(4857)/Tüketici(6502) maddelerini `niş` alanıyla etiketle (Faz 3'e hazır).
- **[İŞ]** Train/val/test ayrımı (hash-split, test izole).

> **ℹ️ Bilgi — neden GPT-4o-mini ile sadeleştirme?** Elimizdeki 32K veri doğru ama uzman dilinde. Tüm üretim GPT-4o-mini ile yapılıyor (~$13 bulk). "Öğretmen" model üretiyor, biz küçük modele öğretiyoruz (distillation). Grounding var → EuroHPC tuzağı yok.

## Adım 5 — Grounded Üretim (Eksik veri tipleri)
**Amaç:** Elimizde olmayan veri tiplerini (terim sadeleştirme, senaryo→atıf, madde özeti) gerçek kanun maddelerinden üret.

- **[İŞ]** **Kanıt koşusu:** 50 örnek, GPT-4o-mini, gerçek madde → sade Q&A + Muhakim ile doğrula.
- **[İŞ]** Kanıt geçerse ölçekle: ~20K grounded örnek üret (GPT-4o-mini, ~$8-13).
- **[İŞ]** Her örnekte `kaynak_madde` alanı tut (halüsinasyon denetimi için).
- **[İŞ]** v0 + üretilen → birleşik `sft_v1`.

> **ℹ️ Bilgi — neden baseline önce, üretim sonra?** v0 baseline'ı (32K uzman veri) önce koşarız → Muhakim'de açığı görürüz (muhtemelen "doğru ama jargonlu") → üretimi **o açığa** yönlendiririz. Körlemesine üretim yok.

## Adım 6 — Base Model + System Prompt
> ⚠️ **SÜPERSED (2026-06-14, ADR-0010 + V2_PLAN §5.1) → güncel:** aşağıdaki "sade, anlaşılır Türkçe" system prompt v1-era'dır. v2b'de model gömülü `SYSTEM_PROMPT_RAG_MULTI` (uzman-register, RAFT çok-kaynak) taşır (`build_sft_v2b.py`) ve eğitim `--no-system` ile koşar (çift-system önlemi, ADR-0008). Aşağı iz olarak korunuyor.

- **[İŞ]** Base: **Gemma 4 12B** (`google/gemma-4-12B-it-qat-q4_0-unquantized`, Apache 2.0), NF4 ile yükle (QLoRA).
- **[İŞ]** Fine-tune → adapter merge → Q4_0 quantize (llama.cpp) → GGUF deploy (~6.5GB, 8GB VRAM hedef).
- **Not:** Gemma 4 12B encoder-free unified mimari — ayrı vision/audio encoder yok. `target_modules="all-linear"` kullanılır; text-only SFT multimodal yeteneği bozmaz. Model kartı teyitli: OCR (Türkçe dahil çok dilli), el yazısı tanıma, document/PDF parsing native destekli. Belge görseli kullanımında `visual_tokens=560-1120` (küçük metin okuma için yüksek budget şart).
- **[İŞ]** System prompt hazırla (her eğitim örneğine eklenir):
  ```
  Sen HakHukuk'sun. Türk hukuku hakkında sade, anlaşılır Türkçe bilgi verirsin.
  Emin olmadığın konularda "Bu konuda güncel mevzuata veya bir avukata danışmanızı öneririm" dersin.
  Asla kanun maddesi veya bilgi uydurmaz, tahmin etmezsin.
  Bu yanıt hukuki tavsiye değil, bilgilendirme amaçlıdır.
  ```

> **ℹ️ Bilgi — kimlik+davranış neden:** "Uydurma" davranışını Faz 2 RAG'dan önce bastırmak kritik. Model "bilmiyorum" demeli, uydurmamalı. Bu system prompt + eğitim örnekleriyle birlikte iki katmanlı güvence.

## Adım 7 — v0 SFT Baseline (Yerelde)
**Amaç:** İlk baseline ölçümü — üretim kararını bu verecek.

- **[İŞ]** Gemma 4 12B + QLoRA: `r=16, lora_alpha=32, lora_dropout=0.05, target_modules="all-linear"`, NF4, `gradient_checkpointing`.
- **[İŞ]** `batch=1, grad_accum=16` (efektif 16), `lr=2e-4`, `epochs=2`, `cosine`, `adamw_8bit`, `bf16`, `max_seq_len=2048`. W&B logla.
- **⚠️ VRAM:** 12B NF4 ~7GB + aktivasyonlar ~4-5GB → **toplam ~11-12GB**; batch=1 + gradient_checkpointing zorunlu.
- **[İŞ]** Muhakim ile ölç → açığı tespit et → Adım 5 üretimini yönlendir.

> **ℹ️ Bilgi — 12 GB RTX 5070:** Yerelde gerçek SFT mümkün (sadece smoke test değil). Hızlı iterasyon = yerelde, büyük ablation = bulutta.

**Çıktı:** v0 adapter + Muhakim skoru + "ne eksik" raporu.

## Adım 8 — İteratif SFT (v1, v2…)
- **[İŞ]** Grounded üretilen veriyi (Adım 5) ekle → sft_v1 oluştur → yeniden eğit.
- **[İŞ]** Her iterasyonda Muhakim skoru takip et (W&B grafiği).
- **Faz 1 bitti kriteri:**
  - Muhakim'de baseline'a göre **+%15 iyileşme**
  - Elle yazılan 10 vatandaş sorusundan **8'i sade + doğru** (göz testi)

## Adım 9 — Ablation Sweep (Bulut)
- **[İŞ]** Eksenler: LoRA rank {8,16,32} × veri karması × epoch {1,2,3}.
- **[İŞ]** Bulut sağlayıcı: Colab Pro+ (A100) veya Kaggle (T4×2, ücretsiz) — sırası gelince seçilir.

## Adım 10 — Yayın
- **[İŞ]** Model ağırlıkları HF'e push (isteğe bağlı public).
- **[İŞ]** Model kartı: HakHukuk kimliği + sorumluluk reddi + base attribution (**Gemma 4 12B**, Apache 2.0).
- **[İŞ]** Repo: **private** (kod/veri/script). Ticari hak sahipte.

---

# BÖLÜM 3 — KİLİTLİ KARARLAR (Grill-Me Oturumu, 2026-05-29)

| # | Karar | Sonuç |
| :-- | :--- | :--- |
| S1 | Kanun bulk çekimi | Tek seferlik, kategorize (`data/raw/mevzuat/{TUR}/`). Faz 1 için donmuş 40K yeter; bulk script Faz 2'de taze yeniden çalıştırılır |
| S2 | İçtihat | **Faz 2.** yargi-mcp'den RE edilmiş, harita hazır (`docs/YARGI_KAYNAKLARI.md`). %100 in-house |
| S3 | Niş | Faz 1 = **genel hukuk**. Niş maddeler etiketli (kira/iş/tüketici), Faz 3'e hazır |
| S4 | Üretim zamanı | **Baseline önce** (v0 → Muhakim → açığı gör → hedefli üret). İteratif |
| S5 | Üretim motoru | **GPT-4o-mini** (~$13 bulk, API key hazır). Gemini plan dışı |
| S6 | Sade dil | ⚠️ **SÜPERSED (2026-06-08 / ADR-0010).** ~~Veri + prompt ikisi birden; 32K uzman veri sadeleştirilir; sorumluluk reddi her yanıta gömülü.~~ → **Güncel:** sadeleştirme = **app-layer prompt modu** (veriye/loss'a girmez); v2b eğitimi `--no-system` (V2_PLAN §5.1). |
| S7 | Ortam | **WSL2 (Ubuntu 22.04).** Veri pipeline da WSL2'ye taşınır |
| S8 | Eğitim yeri | **Yerelde** smoke + baseline + iteratif SFT (12 GB RTX 5070 yeter). **Bulut** = ablation + final |
| S9 | Model kimliği | **(b) Kimlik + davranış + sorumluluk reddi:** "HakHukuk, sade Türkçe, uydurmam, emin olmadığımda söylerim" |
| S10 | İnsan eval | **Faz 1'de yok.** Muhakim + göz testi yeterli. İnsan feedback = Faz 4 RL altyapısına (no-code UI → DPO/RLHF) |
| S11 | Faz 1 bitti kriteri | ⚠️ **SÜPERSED (ADR-0001/0011/0012).** ~~Muhakim'de +%15 baseline üstü + göz testinde 10/8 vatandaş sorusu.~~ → **Güncel kapı:** A3 rejection ≥0.741 · A1∧A2 ≥0.875 · A4 paren ≥0.9 · CORE-KÖR gerilemesin (canon eval, V2_PLAN §6). Muhakim ikincil/yanlı; insan-κ descope. |
| S12 | Lisans/yayın | **Private repo** + proprietary. Model kartı + ağırlıklar HF'te public (isteğe bağlı). Ticari hak sahipte |
| S13 | Baz model değişikliği (2026-06-07) | **Qwen3.5-4B → Gemma 4 12B** (`gemma-4-12B-it-qat-q4_0-unquantized`). Gerekçe: 256K context, multimodal (gelecek fazlar), QAT → Q4_0 GGUF deploy kalitesi, Apache 2.0 |
| S14 | Deploy pipeline | FT (NF4 QLoRA) → merge (bf16) → Q4_0 quantize (llama.cpp) → GGUF ~6.5GB → 8GB VRAM end-user |
| S15 | TurboQuant | KV-cache quantization (arXiv:2504.19874). **Faz 1'de yok.** Faz 2-3 API serving'de değerlendirilecek; 256K context + 4.5× sıkıştırma. Bkz. `knowledge/summary_turboquant.md` |
| — | In-house ilkesi | 3. parti araç/repo **referans alınıp RE edilir**, runtime'da bağımlılık yok |
| — | Donanım (düzeltme) | **RTX 5070 Laptop, 12 GB, Blackwell sm_120, CUDA 13.1** (eski dokümanlar 8 GB/4070 diyordu — yanlış) |
| — | OSS app ref | `github.com/willchen96/mike` — işlevsel referans (estetik değil); avukat portalı tasarımında kullanıldı |
| S16 | App stack (2026-06-07) | **Monorepo: Next.js 14 + TypeScript (frontend) + FastAPI Python (backend + inference).** uv paket yönetimi. |
| S17 | App format + öncelik (2026-06-07) | **Web first. Avukat portalı önce**, vatandaş portalı sonraki iterasyon. Aynı backend, farklı route grubu. |
| S18 | Inference abstraction (2026-06-07) | `inference/engine.py` — demo'da local llama.cpp/vLLM, prod'da GPU-as-a-Service endpoint. Üst katmanlar (API routers) habersiz; sadece config değişir. |
| S19 | Auth (2026-06-07) | JWT access 15dk + refresh 7gün, bcrypt. Avukat kaydında baro numarası (şimdilik format validation). |
| S20 | Abonelik modeli (2026-06-07) | Free / Pro / Enterprise. MVP'de manuel ödeme (havale/EFT, admin onayı). Stripe entegrasyonu Faz 4. |

---

## Sıradaki adım
> ⚠️ **SÜPERSED (2026-07-01) → güncel durum:** aşağıdaki "WSL2 kurulumuna geç → Adım 1" talimatı **2026-05-29 tarihlidir ve TAMAMLANMIŞTIR** — ortam (Blackwell sm_120, `~/code/global_venv`) kuruldu, veri + v0 + v1 tamamlandı, v2b verisi hazır, tam eğitim başlatılıyor. **Güncel sıradaki iş:** `docs/V2_PLAN.md §9` + `NEXT_SESSION.md` (v2b tam eğitimi `modal run --detach ... spawn_v2b`).

*(Tarihsel/ilk talimat, iz olarak korunuyor)* WSL2 kurulumuna geç → **Adım 1** (Blackwell-uyumlu CUDA + Python + ML stack). Veri pipeline (`scripts/`) WSL2'ye taşınır, ardından **Adım 2** smoke test.
