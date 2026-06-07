# HakHukuk — TODO

## Faz 1: LLM Temeli (Aktif)
> Detaylı execute planı: `docs/TEKNIK_PLAN.md`. Veri planı: `docs/VERI_PLANI.md`.

- [x] Baz model kararı → **Gemma 4 12B** (`gemma-4-12B-it-qat-q4_0-unquantized`, QLoRA → Q4_0 GGUF deploy, Apache 2.0, Unsloth destekli)
- [x] Veri envanteri + EDA → OrionCAF + Renicames doğrulandı, EuroHPC reddedildi
- [x] SFT v0 inşası → `data/processed/sft_v0/` (~32K, hash-split, chat-template)
- [x] Otoriter kanun zemini → `data/raw/mevzuat_maddeler.jsonl` (40.853 madde) + Bedesten API (canlı, RE edildi)
- [ ] **Geliştirme ortamı (Adım 1):** WSL2 + Blackwell-uyumlu CUDA + uv + PyTorch(sm_120) + Unsloth/bitsandbytes/flash-attn → smoke test
- [ ] Bulk kanun çekimi: Bedesten API → `data/raw/mevzuat/{TUR}/` kategorize
- [ ] v0 baseline SFT (Gemma 4 12B + QLoRA, NF4 yükleme, batch=1) → Muhakim ile ölç → açığı belirle
- [ ] 32K uzman cevabı → sade dil (GPT-4o-mini, ~$13)
- [ ] Grounded üretim kanıt koşusu (50 örnek, gerçek madde → GPT-4o-mini → doğrula)
- [ ] Ölçekle → sft_v1 → iteratif SFT
- [ ] Benchmark/eval: Muhakim + göz testi (10 vatandaş sorusundan 8) + staj sınavı havuzu
- [ ] **Faz 1 bitti kriteri:** Muhakim'de baz modele +%15 ve göz testi 8/10

## Faz 2: RAG + Knowledge Graph
> **Not:** Uzun context (256K) KV-cache büyümesi için **TurboQuant** (arXiv:2504.19874) değerlendirilecek — bkz. `knowledge/summary_turboquant.md`.
- [ ] Hukuk metni yapı çıkarımı (kanun/madde/fıkra/atıf parser)
- [ ] Graph DB seçimi (Neo4j vs Memgraph vs FalkorDB)
- [ ] Embedding modeli (TR-MTEB lideri)
- [ ] Hybrid retrieval prototipi
- [ ] Vanilla RAG vs Graph-RAG karşılaştırma deneyi

## Faz 3: Model Serving + Agentic Workflow + App
> Agent altyapısı olmadan niş özellikler inşa edilemez — önce foundation kurulur.

### Serving
- [ ] Model serving altyapısı (vLLM + GGUF → FastAPI REST endpoint)
- [ ] TurboQuant KV-cache entegrasyonu (256K context, 4.5× sıkıştırma)

### Agent + App
> Spec: `docs/superpowers/specs/2026-06-07-hakhukuk-web-app-design.md`

- [x] App format kararı → **Web first, monorepo (Next.js 14 TS + FastAPI Python)**
- [x] Uygulama tasarım spesifikasyonu yazıldı

#### Altyapı
- [ ] Monorepo iskelet: `frontend/` (Next.js 14 + TS + Tailwind) + `backend/` (FastAPI + uv + Alembic)
- [ ] `inference/engine.py` — llama.cpp / vLLM abstraction (demo=local, prod=GPU endpoint)
- [ ] PostgreSQL bağlantısı + SQLAlchemy modelleri (users, subscriptions, dosyalar, belgeler, sohbetler, mesajlar, dilekce_taslaklari)
- [ ] Alembic migration kurulumu

#### Backend — API Rotaları
- [ ] `auth.py` — POST /auth/register, /login, /refresh (JWT 15dk+7gün, bcrypt)
- [ ] `documents.py` — GET/POST /dosyalar/, GET/PATCH/DELETE /dosyalar/{id}
- [ ] `documents.py` — POST /belgeler/upload (multipart, async OCR kuyruğu) + GET /belgeler/{id}/status
- [ ] `chat.py` — POST /sohbetler/, GET /sohbetler/{id}/mesajlar, POST /sohbetler/{id}/mesaj (SSE streaming)
- [ ] `dilekce.py` — POST /dilekce/uret (SSE streaming taslak), GET /dilekce/{id}
- [ ] `tufe.py` — GET /tufe/hesapla (tarih + oran → yasal sınır)
- [ ] Abonelik limit middleware (kullanim_sayaci → 402 + upgrade yönlendirmesi)

#### Frontend — Avukat Portalı
- [ ] `(auth)/` — login, register, onboarding sayfaları
- [ ] `avukat/dashboard` — son dosyalar, son sohbetler, hızlı eylemler
- [ ] `avukat/dosyalar` — liste + kategori filtresi + yeni dosya
- [ ] `avukat/dosyalar/[id]` — üç panel (belgeler | sohbet | araçlar)
- [ ] Belge upload + OCR durum göstergesi (drag-drop + polling)
- [ ] SSE chat stream (`EventSource` native)
- [ ] Dilekçe üretimi UI (tür seç → notlar → streaming taslak)
- [ ] TÜFE hesap aracı UI
- [ ] `avukat/ayarlar` — profil, baro no, abonelik durumu

#### Agent + Gelişmiş
- [ ] Agent framework kararı (LangGraph / custom)
- [ ] RAG sorgu tool (Bedesten canlı → madde getir)
- [ ] Çok adımlı agent akışı (soru → veri çek → hesapla → taslak üret)
- [ ] No-code RL UI (hukukçu/kullanıcı feedback → DPO/RLHF döngüsü)

### Multimodal Input
- [ ] Belge fotoğrafı / OCR pipeline (mahkeme kararı, sözleşme, tebligat; visual_tokens=560-1120)
- [ ] Sesli soru input pipeline (audio → hukuki yanıt)

## Faz 4: Niş Uzmanlıklar
> Agent framework Faz 3'te kurulu — nişler onun üstüne inşa edilir.
- [ ] İlk niş seçimi (Kira / İş / Tüketici)
- [ ] Niş veri üretimi (senaryo → dilekçe taslağı, GPT-4o-mini grounded)
- [ ] Niş eval rubriği (doğruluk, sade dil, atıf)
- [ ] Niş prototipi (agent framework üstünde)

## Faz 5: Vatandaş Platformu
- [ ] Web arayüzü (mobil öncelikli, sade)
- [ ] e-Devlet/UYAP entegrasyonu (yargi-mcp → in-house RE)
- [ ] e-Tebligat bildirim asistanı
- [ ] HITL döngüsü (gönüllü avukat feedback → DPO)
- [ ] Monitoring + sürekli iyileştirme pipeline
