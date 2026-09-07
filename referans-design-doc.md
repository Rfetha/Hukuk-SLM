> ⚰️ **SİLİNMESİ KARARLAŞTIRILDI — ama HENÜZ DEĞİL (2026-09-07).**
>
> İnsan kararı (spec §9): bu belge **silinir**, yerine `docs/MIMARI.md` yazılır.
> ⛔ **Engel:** `docs/MIMARI.md` **henüz yok** — sıradaki planın **Görev 13 Adım 4**'ü.
> Yerine geçecek belge yazılmadan silmek, mimari anlatımı **hiçbir yerde bırakmamak** olurdu.
>
> ⚠️ **Bu arada: içeriğine GÜVENME.** 2026-07-29'dan beri dokunulmadı; sayıları
> *"örnekleyici yer tutucu"*dur ve **bilerek** hiçbir yere taşınmadı. Bugünkü sayılar için
> [`CLAUDE.md`](CLAUDE.md) manşetine bak.
>
> 🔒 Kullanıcının orijinal taslağı — **düzenlenmez**, olduğu gibi durur.

# System Design Document: Local Legal AI Engine (Law-FT Stack)

## 1. Mimari Vizyon ve Genel Bakış

Law-FT Stack; tamamen lokal çalışan, gizlilik odaklı (Privacy-First), modüler ve mikroservis mimarisine dayalı bir Hukuk Yapay Zekası Asistanıdır.

Sistemin temel amacı; Türk Hukuku mevzuatı, Yargıtay/Danıştay içtihatları ve dilekçe taramaları üzerinde aşamalı QLoRA ve Model Merging yöntemleriyle evrimleştirilmiş Law-FT SLM (Small Language Model) ile Graph-RAG ilişkisel bilgi ağını birleştirmektir.

Girdi tarafında Polimorfik Esneklik sunulur: Kullanıcı dümdüz metin yazıp sohbet edebilir, PDF/evrak yükleyebilir veya sesli dikte verebilir. Sistem, 8 GB VRAM sınırına sahip lokal istemci cihazlarda sıfır veri sızıntısıyla, yüksek hızda gerekçeli hukuki analiz ve dilekçe incelemesi sunar.

---

## 2. Proje Motivasyonu & Akademik Hedefler (Thesis Objective)

Bu projenin temel motivasyonu ve yüksek lisans tezi hedefi, Küçük Dil Modellerinin (SLM) yerel ortamlarda, sınır (frontier) modellerin kabiliyetlerine ulaşabileceğini kanıtlamaktır.

Hukuk gibi veri gizliliğinin en üst düzeyde olduğu alanlarda, bulut tabanlı API'lere (OpenAI, Anthropic vb.) bağımlılık büyük bir risk ve maliyet oluşturur. Bu proje, şu 3 temel sorunu çözmeyi hedefler:

* **%100 Veri Gizliliği (Absolute Security):** Tüm işlemlerin (OCR, STT, RAG ve Inference) hava boşluklu (air-gapped) yerel makinede çalışmasıyla müşteri/müvekkil verilerinin asla dışarı çıkmaması.
* **Sıfır Operasyonel Maliyet (Zero OPEX / 0 Billing):** Her API çağrısı için ücret ödemek yerine, sistemin mevcut donanım yatırımıyla (CAPEX) sınırsız kullanılabilmesi.
* **Sıfır Bağımlılık (Zero External Dependency):** İnternet bağlantısı kopsa veya bulut sağlayıcıları çökse bile kesintisiz hizmet verebilme yeteneği.

Sistem, spesifik bir alanda (Türk Hukuku) özelleştirilmiş ince ayar (Law-FT) ve optimize edilmiş bir donanım/yazılım mimarisiyle, devasa genel amaçlı modellerin performansına yerel kaynaklarla erişilebileceğini gösteren bir kavram kanıtı (Proof of Concept) niteliğindedir.

---

## 3. Model Yaşam Döngüsü: Sequential Law-FT Pipeline

Modelemizi sıfırdan eğitmek yerine, kademeli LoRA adaptasyonu ve Mergekit (SLERP, TIES, DARE) kullanarak aşamalı olarak evrimleştiriyoruz.

```text
[ Base Model: Qwen3.5-4B-Instruct ]
             │
             ▼
  ┌──────────────────────────┐
  │  Aşama 1: Domain SFT     │ ──► [Veri Seti: Türk Mevzuatı & İçtihat Metinleri]
  └─────────────┬────────────┘
                │ QLoRA Adapter 1
                ▼
  ┌──────────────────────────┐
  │  Merge Stage 1           │ ──► [Teknik: TIES-Merging veya SLERP]
  └─────────────┬────────────┘
                │
                ▼
    [ Model: Law-FT-Base-v2 ]
                │
                ▼
  ┌──────────────────────────┐
  │  Aşama 2: Reasoning SFT  │ ──► [Veri Seti: Distractor Filtering + CoT Hukuki Akıl Yürütme]
  └─────────────┬────────────┘
                │ QLoRA Adapter 2
                ▼
  ┌──────────────────────────┐
  │  Merge Stage 2           │ ──► [Teknik: DARE-TIES veya SLERP]
  └─────────────┬────────────┘
                │
                ▼
   [ Model: Law-FT Custom Base ]
                │
                ▼
  ┌──────────────────────────┐
  │  Aşama 3: Quantization   │ ──► [Teknik: llama.cpp GGUF Q4_K_M Export]
  └──────────────────────────┘

```

### A. Aşamalı Fine-Tuning ve Birleştirme Adımları

* **Aşama 1 — Domain SFT (Türk Hukuku Terminoloji & Bilgi Katmanı):**
* *Amaç:* Base modele Türk Hukuku dilini, terminolojisini, mevzuat yapısını ve Yargıtay emsal karar formatlarını öğretmek.
* *İşlem:* Qwen3.5-4B-Instruct üzerine QLoRA eğitilir (Adapter_v1).
* *Merge 1:* Base Model + Adapter_v1 birleştirilerek dondurulur ve Law-FT-Base-v2 oluşturulur.


* **Aşama 2 — Reasoning & Distractor Filtering SFT (Hukuki Akıl Yürütme Katmanı):**
* *Amaç:* Modele Graph-RAG'den gelen gürültülü verileri eleme (Distractor Filtering) ve sorun-inceleme-gerekçe-sonuç zinciriyle Adım Adım Hukuki Çıkarım (Chain-of-Thought) yapmayı öğretmek.
* *İşlem:* Law-FT-Base-v2 üzerine 2. Aşama QLoRA eğitilir (Adapter_v2).
* *Merge 2:* Law-FT-Base-v2 + Adapter_v2 birleştirilerek nihai Law-FT Custom Base elde edilir.


* **Aşama 3 — Edge Deployment (Kuantizasyon Katmanı):**
* *Amaç:* Cihaz üzerinde (8 GB VRAM) çıkarım sağlayabilmek.
* *İşlem:* Tam ağırlıklı Law-FT Custom Base modeli llama.cpp formatına çevrilip GGUF Q4_K_M olarak kuantize edilerek local inference engine'e dağıtılır.



---

## 4. Adaptör Birleştirme (Merging) ve Kuantizasyon Derin Teknik Analizi

Adaptör ağırlıklarını taban model ile birleştirmenin (merge) arkasındaki matematiksel ve mühendislik teknikleri 3 ana başlık altında ele alınır:

### 4.1. Ağırlık Birleştirme Matematiği (Linear MoE & Fusing)

LoRA (Low-Rank Adaptation) tekniğinde, modelin ana ağırlık matrisi ($W_0$) dondurulur. Güncellemeler ise çok daha düşük rütbeli iki matris olan $A$ ve $B$ içinde eğitilir.

Çıkarım (inference) sırasında bir katmanın toplam girdisi ($x$) ile çarpımı şu şekildedir:


$$h = W_0x + \Delta Wx = W_0x + \frac{\alpha}{r}(BA)x$$

* $r$: Low-rank derecesi (örn: 8, 16, 64)
* $\alpha$: Ölçeklendirme (scaling) katsayısı

Merge İşlemi (Fusing): `merge_and_unload()` fonksiyonu çağrıldığında, matris çarpımı ($B \times A$) hesaplanır, $\frac{\alpha}{r}$ ile ölçeklenir ve doğrudan ana matrise eklenir:


$$W_{\text{yeni}} = W_0 + \left(\frac{\alpha}{r} \times (B \times A)\right)$$

* *Teknik Sonuç:* Bu işlemden sonra $A$ ve $B$ matrisleri bellekten silinir. Model artık standart bir Transformer modeli gibi davranır; çıkarım sırasında ek gecikme (latency penalty) tamamen sıfırlanır.

### 4.2. Dequantization ve Ölçekleme Çelişkisi (4-Bit Merge Sınırı)

Doğrudan 4-bit (NF4/INT4) taban modele LoRA birleştirmeye çalışmak, Kuantizasyon Blok Yapısı nedeniyle teknik olarak başarısız olur ve modelin çıktılarının bozulmasına (gibberish) yol açar.

* **Blok Bazlı Ölçekleme (Block-wise Quantization):** 4-bit modellerde ağırlıklar tek tek değil, genellikle 64'lü veya 128'li bloklar halinde sıkıştırılır. Her bloğun kendine ait bir Ölçek Çarpanı (Scale Factor) ve Sıfır Noktası (Zero Point) vardır.
* **Hassasiyet Kaybı:** FP16 hassasiyetindeki LoRA matrisi ($B \times A$), 4-bitlik blok yapısına doğrudan eklenemez. Önce 4-bitlik matrisin FP16'ya geri dönüştürülmesi (dequantize) gerekir.
* **Çifte Hata Akümülasyonu (Double Quantization Error):** 4-bit model geri dönüştürüldüğünde orijinal FP16 değerlerini tam olarak alamaz ($\text{quantization error}_1$). Bu dönüştürülmüş hatalı değerlerin üzerine LoRA matrisi eklenip model tekrar 4-bit'e zorlanırsa ($\text{quantization error}_2$), çifte hata birikimi oluşur.
* **Uygulama Kuralı:** Başarılı bir birleştirme (merge) işlemi için taban model kesinlikle FP16 / BF16 hassasiyetinde kalmalı, LoRA adaptörü bu FP16 taban modele birleştirilmeli ve kuantizasyon (GGUF Q4_K_M) işlemi bu nihai birleşmiş model üzerinden en son aşamada yapılmalıdır.

### 4.3. Çalışma Zamanı Birleştirme Teknikleri (On-the-Fly / Zero-Merge)

Disk üzerinde kalıcı bir birleştirme yapılmak istenmeyen durumlar için çıkarım motorları şu yöntemleri kullanır:

* **Multi-LoRA Serving (Çoklu Adaptör Sunumu):** Aynı 4-bit taban model VRAM'e tek bir kez yüklenir. Eşzamanlı gelen isteklerde ilgili LoRA adaptörleri dinamik olarak devreye girer ($W_0x + B_AxA_x$ vs $W_0x + B_BxB_x$). VRAM kullanımında yüksek verimlilik sağlar.
* **Truncated/Linear Fusion (Bellekte Geçici Birleştirme):** Model RAM/VRAM üzerinde çalışma anında FP16'ya açılır, LoRA eklenir ve çıkarım motoru birleşik modeli geçici bellek bölgesinde tutar.

---

## 5. Model Prompting & Jinja Chat Template Yapılandırması

Modelin çıkarım motorları (llama.cpp, vLLM, Hugging Face) ve ince ayar (fine-tuning) süreçlerinde doğru token sınırlandırmalarıyla çalışabilmesi için Qwen3.5 ChatML tabanlı Jinja Şablonu kullanılır.

### A. Esnek ve Geliştirilebilir Base Jinja Template

Aşağıdaki şablon; varsayılan hukuki sistem prompt'unu barındırır, RAG bağlamını enjekte etmeye izin verir ve gelecekte araç kullanımı (Tool Calling / Function Calling) eklenebilecek modüler bir yapıya sahiptir:

```jinja
{%- if messages[0]['role'] == 'system' %}
    {%- set system_message = messages[0]['content'] %}
    {%- set loop_messages = messages[1:] %}
{%- else %}
    {%- set system_message = 'Sen Türk Hukuku alanında uzmanlaşmış Law-FT yapay zeka asistanısın. Sana sunulan mevzuat ve içtihat bağlamını (RAG) kullanarak, gürültülü bilgileri eleyip gerekçeli ve doğru hukuki analizler üretirsin.' %}
    {%- set loop_messages = messages %}
{%- endif %}

{{- '<|im_start|>system\n' + system_message + '<|im_end|>\n' }}
{%- for message in loop_messages %}
    {%- if message['role'] == 'user' %}
        {{- '<|im_start|>user\n' + message['content'] + '<|im_end|>\n' }}
    {%- elif message['role'] == 'assistant' %}
        {{- '<|im_start|>assistant\n' }}
        {%- if message.content is string %}
            {{- message['content'] }}
        {%- endif %}
        {{- '<|im_end|>\n' }}
    {%- endif %}
{%- endfor %}
{%- if add_generation_prompt %}
    {{- '<|im_start|>assistant\n' }}
{%- endif %}

```

---

## 6. Model Evaluation & Rakip (Baseline) Benchmark Matrisi

Sistemin başarısı; amiral gemisi devasa modellerle değil, sektörde yaygın kullanılan Workhorse / Flash sınıfı kapalı bulut modelleri ve un-tuned base model ile kıyaslanarak kanıtlanacaktır.

### A. Kıyaslama Yapılacak Modeller Matrisi

| Model Ailesi | Seçilen Rakip Model | Tez İçin Seçilme Gerekçesi |
| --- | --- | --- |
| **Google Gemini** | Gemini 3.5 Flash / Flash-Lite | Hız, operasyonel maliyet ve genel zeka dengesinde sektör standardı referans model. |
| **OpenAI GPT** | GPT-4o-mini / GPT-4o | Sektörün en yaygın benchmark referansı. |
| **Anthropic Claude** | Claude 3.5 Haiku / Sonnet | Karmaşık hukuki akıl yürütme (Reasoning) ve uzun metin analizi kulvarındaki temsilci. |
| **Open-Source (Local)** | Qwen3.5-4B (Base / Un-tuned) | Ablation Study kontrol grubu. Fine-Tuning ve Merging'in net katkısını ölçmek için. |

### B. Başarı Metrikleri ve Değerlendirme Metodolojisi

* **Hukuki Akıl Yürütme ve Bilgi (TRLawBench / ÖSYM Adli Yargı):** Mevzuat ve emsal karar bilgisi ölçümü, soru-cevap doğruluk yüzdesi ($\%$ Accuracy).
* **Hakemli Kör Değerlendirme (LLM-as-a-Judge / Blind Eval):** 100 adet anonimleştirilmiş gerçek hukuki senaryoda üretilen yanıtlar, hangi modele ait olduğu gizlenerek üst seviye bir hakem modele (Örn: Gemini 3.1 Pro) sunulur. Kriterler: Hukuki Doğruluk, Halüsinasyon Oranı, Distractor Filtering (RAG gürültüsünü eleme) ve CoT Mantık Kalitesi (1-10 puan).
* **Lokal Donanım Metrikleri (Edge Performance):** Saniyedeki Token Hızı ($\text{Tokens/sec}$), İlk Tokena Kadar Geçen Süre ($\text{TTFT - Time To First Token}$), Peak VRAM / RAM Tüketimi (MB/GB).

---

## 7. Modülerlik ve Interface Kontratları

Tüm işleme servisleri soyut arayüzler (Agnostic Interfaces) arkasına gizlenmiştir.

* **A. OCR Interface (`/api/v1/ocr`)**
* *Endpoint:* `POST /api/v1/ocr/process`
* *Request:* `{"document_bytes": "base64...", "output_format": "markdown", "language": "tr"}`
* *Response:* `{"status": "success", "data": {"content": "# NÖBETÇİ İŞ MAHKEMESİ...", "confidence_score": 0.98}}`


* **B. STT Interface (`/api/v1/stt`)**
* *Endpoint:* `POST /api/v1/stt/transcribe`
* *Request:* `{"audio_bytes": "base64...", "language": "tr", "temperature": 0.0}`
* *Response:* `{"status": "success", "data": {"transcript": "Müvekkilimin iş akdi...", "duration_seconds": 18.5}}`


* **C. Graph-RAG Interface (`/api/v1/graph`)**
* *Endpoint:* `POST /api/v1/graph/query`
* *Request:* `{"query": "Gece vardiyasında hamile çalışan hakları", "mode": "hybrid", "top_k": 5}`
* *Response:* `{"status": "success", "data": {"context_chunks": [...], "entities_found": [...], "graph_nodes": [...]}}`



---

## 8. Katmanlı Donanım Matrisi & VRAM Bütçesi

Sistem, istemcinin GPU kapasitesine göre dinamik olarak en uygun Law-FT sürümünü çalıştırır.

| Donanım Tier | GPU VRAM Bütçesi | Target Base Model (Law-FT) | Kuantizasyon | Tahmini Net VRAM Tüketimi |
| --- | --- | --- | --- | --- |
| **Tier 1 (Base)** | < 8 GB | Law-FT-4B (Merged Custom) | GGUF Q4_K_M | ~3.8 GB |
| **Tier 2** | < 12 GB | Law-FT-9B (Merged Custom) | GGUF Q4_K_M | ~6.2 GB |
| **Tier 3** | < 16 GB | Law-FT-14B (Merged Custom) | GGUF Q5_K_M | ~10.5 GB |
| **Tier 4** | < 24 GB | Law-FT-32B (Merged Custom) | GGUF Q4_K_M | ~18.0 GB |

### Tier 1 (8 GB VRAM) Detaylı Bellek Profillemesi

```text
[ Toplam VRAM Kullanım Bütçesi: ~5.8 GB / 8.0 GB ]

┌─────────────────────────────────────────────────────────────┬────────┐
│ Bileşen / Modül                                             │ VRAM   │
├─────────────────────────────────────────────────────────────┼────────┤
│ llama.cpp (Law-FT-4B Custom Base GGUF Q4_K_M)               │ 2.8 GB │
│ KV Cache (16K Context Window + Gated DeltaNet)              │ 1.0 GB │
│ Graph-RAG / Embedding Engine (Local Vector Store)           │ 0.6 GB │
│ Faster-Whisper / Surya OCR (Lazy Load / CPU Fallback)       │ 0.8 GB │
│ OS & Desktop GUI Reserve                                    │ 0.6 GB │
└─────────────────────────────────────────────────────────────┴────────┘

```

---

## 9. Docker Compose Orkestrasyon Yapısı

```yaml
version: '3.8'

networks:
  legal-ai-net:
    driver: bridge

volumes:
  llama_models:
  lightrag_data:

services:
  # 1. LLM INFERENCE ENGINE (llama.cpp)
  inference-engine:
    image: ghcr.io/ggerganov/llama.cpp:server-cuda
    container_name: legal_llm_engine
    environment:
      - LLAMA_ARG_MODEL=/models/law-ft-4b-custom-base-q4_k_m.gguf
      - LLAMA_ARG_CTX_SIZE=16384
      - LLAMA_ARG_N_GPU_LAYERS=99
      - LLAMA_ARG_HOST=0.0.0.0
      - LLAMA_ARG_PORT=8080
    volumes:
      - llama_models:/models
    ports:
      - "8080:8080"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    networks:
      - legal-ai-net
    restart: unless-stopped

  # 2. GRAPH-RAG ENGINE (HKUDS LightRAG)
  graph-rag:
    image: legalai/lightrag-service:latest
    container_name: legal_graph_rag
    environment:
      - LLM_BINDING=openai_with_ollama
      - LLM_BINDING_HOST=http://inference-engine:8080
      - WORKING_DIR=/data/lightrag
    volumes:
      - lightrag_data:/data/lightrag
    ports:
      - "9621:9621"
    depends_on:
      - inference-engine
    networks:
      - legal-ai-net
    restart: unless-stopped

  # 3. OCR SERVICE (Surya / Marker)
  ocr-service:
    image: legalai/ocr-service:v1
    container_name: legal_ocr
    ports:
      - "5001:5001"
    networks:
      - legal-ai-net
    restart: unless-stopped

  # 4. STT SERVICE (Faster-Whisper)
  stt-service:
    image: legalai/stt-whisper-service:v1
    container_name: legal_stt
    environment:
      - MODEL_SIZE=medium
      - DEVICE=cpu # GPU VRAM'ini LLM'e bırakmak için CPU'da çalıştırılır
    ports:
      - "5002:5002"
    networks:
      - legal-ai-net
    restart: unless-stopped

```

---

## 10. End-to-End Polimorfik Veri Akış Pipeline'ı

```text
                             ┌─────────────────────────────────────────────────────────┐
                             │                  TAURI DESKTOP APP                      │
                             └────────────────────────────┬────────────────────────────┘
                                                          │
                                         (1. Girdi Tipine Göre Yönlendirme)
                                                          │
                ┌───────────────────────────────────────────┼───────────────────────────────────────────┐
                ▼                                           ▼                                           ▼
      [ Senaryo A: Dümdüz Metin ]                 [ Senaryo B: PDF/Görsel ]                   [ Senaryo C: Ses Kaydı ]
      (Chat / Soru / Prompt)                      (Dilekçe / Mahkeme Evrakı)                  (Duruşma / Avukat Dikte)
                │                                           │                                           │
                │                                           ▼                                           ▼
                │                                (2a. OCR POST Request)                      (2b. STT POST Request)
                │                                http://ocr-service:5001                    http://stt-service:5002
                │                                           │                                           │
                │                                           ▼                                           ▼
                │                                 [ Temiz Markdown Metni ]                    [ Temiz Dikte Metni ]
                │                                           │                                           │
                └───────────────────────────────────────────┴───────────────────────────────────────────┘
                                                          │
                                                          ▼
                                          (3. Normalize Edilmiş Hukuki Metin)
                                                          │
                                                          ▼
                                          (4. Graph Context Query - LightRAG)
                                          http://graph-rag:9621/api/v1/graph
                                                          │
                                                          ▼
                                   [ Hukuk Düğümleri (Mevzuat + İçtihat) + Context ]
                                                          │
                                                          ▼
                                         (5. Final Prompt Assembly & Law-FT)
                                                          │
                                                          ▼
                                         (6. Inference Request / SSE Streaming)
                                          http://inference-engine:8080/v1/chat/completions
                                                          │
                                                          ▼
                                         [ Law-FT Custom Merged Base Model ]
                                         (Gürültüyü Eler & CoT Yanıt Üretir)
                                                          │
                                                          ▼
[ Kullanıcı ] ◄────────────────────────────── (7. Real-time Akıcı Yanıt) ◄────────────────────────────── [ Tauri UI ]

```
