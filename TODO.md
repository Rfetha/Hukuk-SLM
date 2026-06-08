# HakHukuk — TODO

## Faz 1: LLM Temeli (Aktif)
> Detaylı execute planı: `docs/TEKNIK_PLAN.md`. Veri planı: `docs/VERI_PLANI.md`.

- [x] Baz model kararı → **Gemma 4 12B** (`gemma-4-12B-it-qat-q4_0-unquantized`, QLoRA → Q4_0 GGUF deploy, Apache 2.0, Unsloth destekli)
- [x] Veri envanteri + EDA → OrionCAF + Renicames doğrulandı, EuroHPC reddedildi
- [x] SFT v0 inşası → `data/processed/sft_v0/` (~32K, hash-split, chat-template)
- [x] Otoriter kanun zemini → `data/raw/mevzuat_maddeler.jsonl` (40.853 madde) + Bedesten API (canlı, RE edildi)
- [x] **Geliştirme ortamı (Adım 1):** WSL2 + Blackwell sm_120 stack → `~/code/global_venv` (Py3.12, torch 2.10+cu128, unsloth 2026.6.1, bnb 0.49.2 NF4, xformers fallback). env smoke yeşil, `requirements.lock.txt` donduruldu
- [x] **Eval terazisi kuruldu:** `scripts/eval.py` (GPT-4o-mini hakem) + `make_eval_sample.py` → `data/eval/eval_sample_v1.jsonl` (sabit-seed 30 soru). `$OPENAI_BUDGET_USD=5` guard. + `scripts/muhakim_judge.py` (Muhakim ArmoRM 8B) + `scripts/build_scorecard.py` + `scripts/score_corpus.py`.
- [x] **Otonom driver + smoke:** `scripts/run_phase1.sh` (stage'ler, `PYTHONUNBUFFERED`) + `docs/RUNBOOK_FAZ1.md`. ⚠️ Gemma 4 turn işaretleri `<|turn>user/model`.
- [x] **Ham base ölçümü:** **base: GPT doğruluk 7.87 / sadelik 6.47 / Muhakim legal_acc +0.362.**
- [x] **v0 baseline SFT** (1 epoch, loss 1.35→0.63) → **BAŞARISIZ: doğruluk düştü** (GPT 7.87→6.13, Muhakim 0.362→0.124). **Teşhis ölçüldü:** 32K verisinin kendi legal_acc'ı **0.274 < base** → modelden düşük doğrulukta veri → çöktü. Veri sorunu, ayar değil.
- [x] **⚠️ KARAR 2026-06-08 (`[[eval-accuracy-gate]]`):** (1) ana metrik = **groundedness** (uydurma yok), Muhakim ikincil/yanlı; (2) **kısalık/sadelik MODEL ŞARTI YOK** — sadeleştirme app-layer prompt; (3) Faz 1 hedefi = TR rakipleri (Mecellem-Qwen3-4B vb.) geçen doğru+grounded SLM.
- [x] **Grounded kanıt koşusu (25 GPT-4o-mini):** gerçek madde → doğru+atıflı cevap. ✅ yaklaşım çalışıyor. (`scripts/gen_grounded.py`)
- [x] **Adım 4b — Groundedness skorlayıcı kuruldu (`scripts/groundedness.py`):** akademik format — **FactScore** iki-aşamalı (claim-extract → verify) + **ALCE** gold-bağlı atıf (CORRECT/WRONG_REF/UNVERIFIABLE). Metrikler: faithfulness, hallucination, **wrong_ref_rate** (yanlış maddeye yönlendirme), cit_precision/recall, unsupported (makul-ama-kaynaksız ayrımı). `--runs N` (count stabilize), `--judge-model` (paper: gpt-4o), `--mode data|model`. **build_scorecard.py → ANA sütun=groundedness, Muhakim ikincil'e indi.** gnd_gpt: faithfulness 0.97 / halüsinasyon 0.03; ayrışma bayrağı K3'ü otomatik üretiyor (id=8/6 grounded=1.0 ama Muhakim≈0).
- [ ] **Skorlayıcı açık kalanlar (paper-grade):** #2 hakem gücü → büyük koşuda `--judge-model gpt-4o` (gpt-4o-mini self-preference + id=17 stub'da kısmi sızıntı); **#3 insan-κ kalibrasyonu (≥2 avukat) = Aşama C** (kod kapatamaz, sayı o zamana dek göreli okunur).
- [x] **Adım 4a — sampling düzeltildi (`gen_grounded.py`):** substring `CITIZEN_LAWS` → **tam-ad `ALLOWED_LAWS`** (10 vatandaş-çekirdek kanun); `usable()` sıkılaştırıldı (mülga + `STUB_MARKERS` + `AMEND_RE` = id=17 tipi değişiklik/ilga maddeleri elenir); template `<...>` yer-tutucu sızıntısı düzeltildi (GEN_TEMPLATE atıf biçimi + `clean_text()`). Doğrulandı: havuz 2759 madde / ASKERİ sızıntı 0; gnd_gpt2 (25 örnek) **faithfulness 1.0 / hallucination 0.0 / wrong_ref 0.0** (gpt-4o-mini, runs=1).
- [x] **Bulut GPU sağlayıcı kararı (2026-06-08): Modal** (serverless, `@app.function(gpu=...)`). Yerel RTX 5070 = sadece prototip. 4c bake-off + 4d local üretim + v1 SFT → Modal A100/H100. Auth `modal setup` (kullanıcı). Bkz hafıza `[[cloud-gpu-modal]]`.
- [ ] **SIRADAKİ — Adım 4 kalan (Modal'da koşulacak):** (c) local Gemma bake-off (groundedness'le GPT'yle kıyas, Modal GPU); (d) ~20K'ya ölçekle (2759 madde → madde başına ~7 varyasyon) + 32K'dan dolu/savuşturmasız olanları filtrele → `sft_v1`
- [ ] v1 SFT → groundedness skorkartı → rakip baseline'larla kıyas
- [ ] **Faz 1 bitti kriteri:** groundedness'te rakipleri ≥ + base'e göre + (eski "+%15/göz 8/10" askıda)
- [ ] _(Faz 2'ye ertelendi)_ Bulk kanun çekimi: Bedesten API → `data/raw/mevzuat/{TUR}/` (çizelge S1: Faz 1 için donmuş 40K madde yeterli)

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
