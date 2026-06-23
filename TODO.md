# HakHukuk — TODO

> **Milat 2026-06-13.** Geçmiş (tamamlanan işin anlatısı + sayılar) → `docs/record/research_log.md`.
> Bu dosya **ileriye dönük**: kalan görevler + Faz 2-5. Sabit eksen: `NEXT_SESSION.md`.
> Detaylı plan: `docs/TEKNIK_PLAN.md` · Veri: `docs/VERI_PLANI.md` · Kararlar: `docs/adr/`.

## Faz 1 — KALAN (aktif) · v2 planı = `docs/V2_PLAN.md`

- [ ] **2 deep-research'ü sentezle** (v2 teknikleri + hukuk-veri/eğitim) → `docs/V2_PLAN.md`'yi güncelle. v2 reçetesi netleşsin.
- [ ] **v2a = base + mühendislik promptu (SFT YOK)** → canon'dan geçir. İlk dene (ucuz, yan-hasarsız). v1'i döverse → "SFT gereksiz" bulgusu.
- [ ] **Önkoşul (v2-eval'den önce):** register/altitude ekseni + **E (kaynak-eksik) eval seti** (`V2_PLAN §7`).
- [ ] **Gerekirse v2b = hafif SFT** (RAFT/oracle-mod + ağır hedge ~%20-25 + uzman register + düşük LoRA rank) → Modal A100 → canon. Ablasyon: dozaj + confound (`V2_PLAN §5`).
- [ ] **Başarı kapısı:** A3≥0.741 + A1∧A2≥0.875 + A4 koru (`V2_PLAN §6`).
- [ ] **Rakip baseline — BİZİM canon terazide** — `Mecellem-Qwen3-4B` (⚠️ continual-pretrain) + `Llama-3.1-8B-Instruct` → aynı set/hakem. Paperlarından sayı ALMA.
- [ ] **ADR-0010** — reframe resmileştir (pilot DOĞRULADI) + `VISION.md §1` "default sade dil" ifadesini kapat.
- [ ] **Paper öncesi sağlamlaştırma:** G1 cross-**family** judge (Claude/Gemini, κ) · paired McNemar · OOD unseen-statute dilimi · n=100/75 · A1/A2 operasyonel tanım.
- [ ] **Faz 1 kapanış + deploy** — kapı geçilince → merge (bf16) → llama.cpp Q4_0 → GGUF ~6.5GB. *(Provokatif: Product A ise "deliverable = base+RAG+prompt" olabilir — V2_PLAN §8.)*
- [ ] _(SONRA)_ outputs/eval/ klasör düzeni (raw/scored/summary nestele) · _(Faz 2)_ Bedesten bulk kanun çekimi.

> **Faz 1 TAMAMLANANLAR (özet; detay → `docs/record/research_log.md`):** ortam (Blackwell sm_120) · **CANON eval** (4 eksen A1/A2/A3/A4 mod-stratifiye, ADR-0011, /deep-research-doğrulamalı) · **v0 SFT (forum → battı, K3)** · grounded v1 verisi (21.458, faith 0.984) · **v1 SFT (Modal A100)** · **CANON PİLOT base vs v1 → scope=Product A** (ADR-0012; v1 net-negatif, abstention 0.74→0.00) · 12 ADR · dış-rapor denetimi (ADR-0009).

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
