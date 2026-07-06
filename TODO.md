# HakHukuk — TODO

> **Milat 2026-06-13.** Geçmiş (tamamlanan işin anlatısı + sayılar) → `docs/record/research_log/README.md`.
> Bu dosya **ileriye dönük**: kalan görevler + Faz 2-5. Sabit eksen: `NEXT_SESSION.md`.
> Detaylı plan: `docs/TEKNIK_PLAN.md` · Veri: `docs/VERI_PLANI.md` · Kararlar: `docs/adr/`.

## Faz 1 — KALAN (aktif) · **aktif iter = v4 ORPO (yönü NET, reçete+onay bekliyor)**

> **DURUM (2026-07-06):** v3 (ORPO, v2b-devamı) **KAPANDI = KISMİ / teslim değil** (ADR-0015, research_log #32).
> K3'ü onardı (M2 0.35→0.59, M1 0.74→**0.88**) ama base-M2'yi geçmedi (0.593<0.704) + **M2b regresyon** (0.96→0.53,
> forced-source-selection bias). → **sıradaki iş v4** (aşağıda). Kapı tanımı artık ADR-0011 (canon) + ADR-0015 (v4 hedef).

- [x] ~~v2b = hafif RAFT-SFT~~ → **TAMAM (2026-07-02):** tam eğitim + 6-mod canon, tüm kapılar geçti (`docs/record/v2b/sonuclar.md`).
- [x] ~~v2c = near-miss abstention (düz SFT)~~ → **REDDEDİLDİ (2026-07-03):** M2 0.407 + M1 regresyon; K3 negatif bulgu (ADR-0014).
- [x] ~~v3 = ORPO (near-miss preference fix)~~ → **KISMİ, KAPANDI (2026-07-06):** M2 0.593 (K3 onarıldı, base-altı) + M1 0.881 (arttı) ama M2b 0.529 regresyon. Teslim değil. Sonuç: ADR-0015 + research_log #32.
- [ ] 🟢 **v4 = ORPO negatif-aile çeşitliliği (AKTİF — reçete + PARA-KAPISI + onay bekliyor).** Teşhis-güdümlü (v3 M2b forced-selection):
  - **#2b (birincil):** ORPO rejected setine **multi-distractor-no-gold (M2b-tipi)** + **OOD held-out** hard-negatifleri ekle → `train.jsonl` rebuild + yeniden ORPO. "Cevap hiçbirinde yok→reddet" becerisini eğit. Motor = OOD-odaklı hard-negative mining.
  - **M2 base-üstü (ikincil):** near-miss negatif yoğunluğu/kalitesi (veri-kompozisyon kaldıracı).
  - **ADIM 4 τ hi_overlap temiz-etiket:** 108 `hi_overlap` çifti judge τ ile "kazara-cevaplayan" tuzaklardan temizle (`receteler.md` Reçete 4, <$0.10). v4 açılınca uygula.
  - ⚠️ **v2b-SFT ile düzeltme YASAK** (K3). Yöntem = yine ORPO (ref-free); base-joint-ORPO yalnız v2b-continuation tavanı kanıtlanırsa. Reçete: `docs/record/v3/receteler.md` (§Reçete 1-4 + §v4 MİMARİ NOTLARI).
  - _(düşük öncelik, tetik gerçekleşmedi)_ #4 replay 0.20→0.35 (forget YOK çıktı) · #3b çok-kaynak train (Faz-2 RAG yakını).
- [ ] **Başarı kapısı (v4):** M2 ≥ base 0.704 (grounding-korumalı) **+ M2b regresyon kapalı (≥0.9)** + M1/M4/register tavan korunmuş + M5 base-altı. (ADR-0011 canon + ADR-0015.)
- [ ] **Rakip baseline — BİZİM canon terazide** — `Mecellem-Qwen3-4B` (⚠️ continual-pretrain) + `Llama-3.1-8B-Instruct` → aynı set/hakem. Paperlarından sayı ALMA.
- [x] ~~**ADR-0010** — reframe resmileştir~~ → **YAZILDI (2026-07-01):** `docs/adr/0010-reframe-birincil-register-uzman.md` (Yürürlükte, karar 2026-06-13); `VISION.md §1` güncellendi.
- [ ] **Paper öncesi sağlamlaştırma:** G1 cross-**family** judge (Claude/Gemini, κ) · paired McNemar · OOD unseen-statute dilimi · n=100/75 · A1/A2 operasyonel tanım.
- [ ] **MCQ ekseni (hakem-bağımsız doğrulama)** — LLM-judge'a bağımlı olmayan çoktan-seçmeli eksen → paper sağlamlaştırma. *(research_log eski "Açık kararlar" bölümünden taşındı, 2026-07-05 record-restructure.)*
- [ ] **Register ekseni kanonik LLM-judge rubriği (ADR-0013)** — şu an leksik-proxy (`score_register.py`); paper için judge-rubrikli uzman-vs-vatandaş ölçümü (leksik önkoşul yukarıda: register/altitude ekseni). *(aynı restructure'da taşındı.)*
- [ ] **Faz 1 kapanış + deploy** — kapı geçilince → merge (bf16) → llama.cpp Q4_0 → GGUF ~6.5GB. *(Provokatif: Product A ise "deliverable = base+RAG+prompt" olabilir — V2_PLAN §8.)*
- [ ] _(SONRA)_ outputs/eval/ klasör düzeni (raw/scored/summary nestele) · _(Faz 2)_ Bedesten bulk kanun çekimi.
- [ ] _(EVAL-HIZ, v4/gelecek turlar için)_ **`gen_eval_grounded.py` load-once batched runner.** Şu an tek-atışlık: her mod ayrı process → 12B her koşuda yeniden yüklenir (~2-3 dk × ~14 mod-koşu = ~20-30 dk boşa reload). Wrapper: modeli BİR kez yükle → mod/data listesi üzerinde döngüle (M1/M4/M2/M2b/M3/M5 + trap dilimleri). Kazanç ~20-30 dk/tur. ⚠️ Cache'li v2c/v2b protokol paritesini BOZMA (aynı flag/seed/eval-mirror 900, aynı detail çıktısı). v3 ADIM 9'da fark edildi (2026-07-05); şimdiki koşuyu bozmamak için ertelendi.

> **Faz 1 TAMAMLANANLAR (özet; detay → `docs/record/research_log/README.md`):** ortam (Blackwell sm_120) · **CANON eval** (4 eksen A1/A2/A3/A4 mod-stratifiye, ADR-0011, /deep-research-doğrulamalı) · **v0 SFT (forum → battı, K3)** · grounded v1 verisi (21.458, faith 0.984) · **v1 SFT (Modal A100)** · **CANON PİLOT base vs v1 → scope=Product A** (ADR-0012; v1 net-negatif, abstention 0.74→0.00) · 12 ADR · dış-rapor denetimi (ADR-0009).

## Faz 2: RAG + Knowledge Graph
> **Not:** Uzun context (256K) KV-cache için **TurboQuant** (arXiv:2504.19874) — `knowledge/summary_turboquant.md`.
- [ ] Hukuk metni yapı çıkarımı (kanun/madde/fıkra/atıf parser)
- [ ] Graph DB seçimi (Neo4j vs Memgraph vs FalkorDB)
- [ ] Embedding modeli (TR-MTEB lideri)
- [ ] Hybrid retrieval prototipi
- [ ] Vanilla RAG vs Graph-RAG karşılaştırma deneyi

## Faz 3: Model Serving + Agentic Workflow + App
> Agent altyapısı olmadan niş özellikler inşa edilemez — önce foundation kurulur. Spec: `docs/superpowers/specs/2026-06-07-hakhukuk-web-app-design.md`

### Serving
- [ ] Model serving (vLLM + GGUF → FastAPI REST endpoint)
- [ ] TurboQuant KV-cache entegrasyonu (256K context, 4.5× sıkıştırma)

### Agent + App
- [x] App format kararı → **Web first, monorepo (Next.js 14 TS + FastAPI Python)**
- [x] Uygulama tasarım spesifikasyonu yazıldı
- [ ] Monorepo iskelet: `frontend/` (Next.js 14 + TS + Tailwind) + `backend/` (FastAPI + uv + Alembic)
- [ ] `inference/engine.py` — llama.cpp / vLLM abstraction (demo=local, prod=GPU endpoint)
- [ ] PostgreSQL + SQLAlchemy modelleri + Alembic migration
- [ ] Backend rotaları: `auth` (JWT/bcrypt), `documents` (dosyalar + upload/OCR), `chat` (SSE), `dilekce` (SSE taslak), `tufe`, abonelik limit middleware
- [ ] Frontend avukat portalı: auth/onboarding, dashboard, dosyalar + [id] (üç panel), belge upload+OCR, SSE chat, dilekçe UI, TÜFE UI, ayarlar
- [ ] Agent: framework kararı (LangGraph/custom), RAG sorgu tool (Bedesten canlı), çok-adımlı akış, no-code RL UI (feedback → DPO/RLHF)

### Multimodal Input
- [ ] Belge fotoğrafı / OCR pipeline (visual_tokens=560-1120)
- [ ] Sesli soru input pipeline (audio → hukuki yanıt)

## Faz 4: Niş Uzmanlıklar
- [ ] İlk niş seçimi (Kira / İş / Tüketici)
- [ ] Niş veri üretimi (senaryo → dilekçe taslağı, grounded)
- [ ] Niş eval rubriği
- [ ] Niş prototipi (agent framework üstünde)

## Faz 5: Vatandaş Platformu
- [ ] Web arayüzü (mobil öncelikli, sade)
- [ ] e-Devlet/UYAP entegrasyonu (yargi-mcp → in-house RE)
- [ ] e-Tebligat bildirim asistanı
- [ ] HITL döngüsü (gönüllü avukat feedback → DPO)
- [ ] Monitoring + sürekli iyileştirme pipeline
