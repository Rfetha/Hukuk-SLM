# HakHukuk — TODO

> **Milat 2026-06-13.** Geçmiş (tamamlanan işin anlatısı + sayılar) → `docs/record/research_log.md`.
> Bu dosya **ileriye dönük**: kalan görevler + Faz 2-5. Sabit eksen: `NEXT_SESSION.md`.
> Detaylı plan: `docs/TEKNIK_PLAN.md` · Veri: `docs/VERI_PLANI.md` · Kararlar: `docs/adr/`.

## Faz 1 — KALAN (aktif)

- [ ] **Benchmark RUN** — base/v0/v1 × {core_hard, trap}, RAG-modu → A1 groundedness + A3 abstention + A4 format → `bench_scorecard.py`. (Komutlar: `NEXT_SESSION.md`.)
- [ ] **G1 hakem-geçerliliği** — A1/A3 ikinci hakem `--judge-model gpt-4o` (alt-küme) → `judge_agreement.py cross` (κ) + `export`→elle→`author` (~30 yazar spotcheck). κ≥0.6 hedef.
- [ ] **Meta-analiz → v2 yönü** — v1 TRAP'te base'i geçti mi/geçemedi mi (AbstentionBench öngörüsü: SFT abstention'ı bozar). Sonuç v2 hedge-dilimi miktarını belirler.
- [ ] **v2 tasarla** — base'den TAZE QLoRA (v1 üstüne DEĞİL): **uzman-register** + **RAG-modu eğitim** (kaynak prompt'ta) + **%15-25 hedge/red** dilimi. Üretim `gen_grounded.py` hattını yeniden kullan, prompt/üslup değiş.
- [ ] **v2 eğit (Modal A100)** → benchmark'tan geçir → base/v1 ile kıyas (ablasyon).
- [ ] **Rakip baseline — BİZİM terazide** — `newmindai/Mecellem-Qwen3-4B-TR` (⚠️ continual-pretrain) + `newmindai/Llama-3.1-8B-Instruct-*` → aynı setler/hakem. Paperlarından sayı ALMA.
- [ ] **ADR-0010** — reframe (uzman birincil register) resmileştir + `VISION.md` ":14 default sade dil" ifadesini kapat.
- [ ] **Faz 1 kapanış + deploy** — kapı: A3/groundedness'te rakipleri ≥ → merge (bf16) → llama.cpp Q4_0 → GGUF ~6.5GB.
- [ ] _(Faz 2'ye ertelendi)_ Bulk kanun çekimi: Bedesten API → `data/raw/mevzuat/{TUR}/` (Faz 1 için donmuş 40K madde yeterli).

> **Faz 1 TAMAMLANANLAR (özet; detay → `docs/record/research_log.md`):** geliştirme ortamı (Blackwell sm_120) · eval terazisi + groundedness skorlayıcı · ham base ölçümü · **v0 SFT (forum verisi → battı, K3)** · grounded v1 verisi (21.458) + eğitim-öncesi kalite kapısı (faith 0.984) · **v1 SFT (Modal A100)** · 9 ADR · dış-rapor denetimi (ADR-0009) · **benchmark enstrümanı** (CORE-HARD+TRAP + A1/A3/A4 + G1/G2) · script hafifletme (`_legacy/`).

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
