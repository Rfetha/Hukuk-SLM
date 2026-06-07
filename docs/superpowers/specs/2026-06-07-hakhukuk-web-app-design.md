# HakHukuk Web App — Tasarım Spesifikasyonu

**Tarih:** 2026-06-07  
**Kapsam:** Avukat portalı MVP (vatandaş portalı sonraki iterasyon)  
**Referans:** `github.com/willchen96/mike` (işlevsel referans — estetik değil)

---

## 1. Hedef ve Kapsam

Türk hukuk avukatlarına yönelik AI destekli çalışma ortamı. Tek platform, iki arayüz katmanı (avukat portalı + vatandaş portalı), aynı backend ve model. MVP'de avukat portalı önce çıkar.

**MVP özellikleri (kesilemez):**
- Hukuki soru-cevap sohbeti (AI streaming)
- Belge yükleme + OCR (mahkeme kararı, sözleşme, tebligat)
- Dilekçe taslağı üretimi (arabuluculuk, hakem heyeti, itiraz)
- TÜFE hesap aracı (kira artış yasal sınırı)
- Proje/dava bazlı belge organizasyonu

---

## 2. Sistem Mimarisi

**Yaklaşım:** Monorepo, tek FastAPI backend (api + inference aynı süreçte), Next.js TypeScript frontend.

```
hakhukuk/
├── frontend/                  # Next.js 14 + TypeScript + Tailwind
│   └── app/
│       ├── (auth)/            # login, register, onboarding
│       ├── avukat/            # avukat portalı (MVP)
│       │   ├── dashboard/
│       │   ├── dosyalar/
│       │   ├── sohbet/
│       │   ├── belgeler/
│       │   └── dilekce/
│       └── (vatandas)/        # sonraki iterasyon
│
└── backend/
    ├── app/
    │   ├── api/               # FastAPI routers
    │   │   ├── auth.py
    │   │   ├── chat.py
    │   │   ├── documents.py
    │   │   ├── dilekce.py
    │   │   └── tufe.py
    │   ├── inference/         # model wrapper (internal)
    │   │   └── engine.py      # llama.cpp / vLLM abstraction
    │   ├── models/            # SQLAlchemy ORM
    │   └── main.py
    ├── alembic/
    └── pyproject.toml         # uv ile yönetilir
```

**Veri akışı:** Next.js → FastAPI (REST + SSE streaming) → inference engine → Gemma 4 12B fine-tuned model.

**Belge akışı:** Upload → FastAPI → disk/object storage → OCR (Gemma 4 native vision, `visual_tokens=560-1120`) → metin `belgeler.ocr_text`'e yazılır → chat context'ine girer.

**Demo → Prodüksiyon geçişi:** Demo'da inference aynı makinede çalışır. GPU-as-a-Service'e geçince `inference/engine.py`'daki endpoint değişir — üst katmanlar habersiz. Kullanıcı kendi API anahtarı girmez; model domain-specific, servis sahibine aittir.

---

## 3. Veri Modeli

Şema yön gösterici; Alembic migration'larla evrilir.

```sql
users
  id, email, password_hash
  role          -- avukat | vatandas | admin
  full_name, bar_number
  created_at

subscriptions
  id, user_id → users
  plan          -- free | pro | enterprise
  status        -- active | cancelled
  period_start, period_end

dosyalar
  id, user_id → users
  baslik, aciklama
  kategori      -- kira | is | tuketici | diger
  created_at, archived_at

belgeler
  id, dosya_id → dosyalar
  filename, storage_path, mime_type, boyut
  ocr_text      -- çıkarılmış düz metin
  ocr_status    -- pending | done | failed
  created_at

sohbetler
  id, dosya_id → dosyalar  -- nullable (dosyasız sohbet olabilir)
  baslik, created_at

mesajlar
  id, sohbet_id → sohbetler
  rol           -- user | assistant
  icerik        -- text
  belge_refs    -- jsonb (context'e giren belgeler izlenebilir)
  created_at

dilekce_taslaklari
  id, dosya_id → dosyalar
  tur           -- arabuluculuk | hakem_heyeti | itiraz | diger
  icerik, model_versiyonu
  created_at
```

**Notlar:**
- `belgeler.ocr_text` → chat context + pgvector embedding için ham kaynak (Faz 2'de)
- `mesajlar.belge_refs` → "neden bunu söyledi" sorusunu yanıtlar, audit trail sağlar
- `subscriptions` şimdilik basit; Stripe entegrasyonu Faz 4'te

---

## 4. API Katmanı

```
POST /auth/register
POST /auth/login
POST /auth/refresh

GET    /dosyalar/
POST   /dosyalar/
GET    /dosyalar/{id}
PATCH  /dosyalar/{id}
DELETE /dosyalar/{id}

POST   /belgeler/upload          # multipart; OCR async kuyruğa girer
GET    /belgeler/{id}/status     # pending | done | failed

POST   /sohbetler/               # yeni sohbet (dosya_id opsiyonel)
GET    /sohbetler/{id}/mesajlar
POST   /sohbetler/{id}/mesaj     # SSE streaming response

POST   /dilekce/uret             # {dosya_id, tur, notlar} → streaming taslak
GET    /dilekce/{id}

GET    /tufe/hesapla             # {baslangic_tarihi, artis_orani} → yasal sınır
```

**Kritik kararlar:**
- **SSE streaming** — chat ve dilekçe üretimi token-by-token akar; Next.js `ReadableStream` ile alır
- **OCR async** — büyük PDF için zorunlu; `/belgeler/{id}/status` polling ile izlenir

---

## 5. Avukat Portalı — Ekran Akışı

```
/avukat/dashboard
  Son dosyalar, son sohbetler, hızlı eylemler

/avukat/dosyalar
  Liste (kategori filtresi)
  [+ Yeni Dosya]

/avukat/dosyalar/[id]          ← Ana çalışma ekranı
  ├── Sol panel : Belgeler
  │     Drag-drop upload, OCR durum göstergesi
  ├── Orta panel: Sohbet (SSE streaming)
  │     Bağlam notu: hangi belgeler context'te
  └── Sağ panel : Araçlar
        Dilekçe üret (tür → notlar → streaming taslak)
        TÜFE hesapla (tarih → yasal artış sınırı)

/avukat/ayarlar
  Profil, baro numarası, abonelik durumu
```

**Tasarım ilkesi:** Her şey dosya merkezli — avukat bir davayı açar, belge atar, sohbet eder, dilekçe üretir. Tab atlamak yok, context kaybolmaz.

**Frontend stack:**
- React Query — server state
- Zustand — UI state (panel boyutları, aktif dosya)
- `EventSource` — SSE streaming (native, library gerekmez)

---

## 6. Auth + Abonelik

**Auth:** JWT (access 15dk + refresh 7gün), bcrypt. Avukat kaydında baro numarası alınır (şimdilik format validation, ileride baro API doğrulaması).

**Planlar:**

| Plan | Dosya | Mesaj/ay | Belge/ay | Hedef |
|:--|:--|:--|:--|:--|
| Free | 3 | 50 | 5 | Deneme |
| Pro | Sınırsız | 500 | 50 | Bireysel avukat |
| Enterprise | Sınırsız | Sınırsız | Sınırsız | Hukuk bürosu |

**Limit enforcement:** FastAPI middleware her istekte `kullanim_sayaci` kontrol eder. Aşılınca `402` döner, frontend upgrade modal açar.

**Ödeme:** MVP'de manuel (havale/EFT, admin onayı). Stripe entegrasyonu Faz 4'te.

---

## 7. Faz Bağlantısı

Bu uygulama `VISION.md` Faz 3 (Serving + Agentic Workflow + App) kapsamında geliştirilir:

- **Model:** Faz 1 çıktısı (Gemma 4 12B fine-tuned, Q4_0 GGUF)
- **OCR:** Gemma 4 native vision (text-only SFT'den etkilenmez)
- **RAG:** Faz 2 çıktısı pgvector/graph bağlanır — `inference/engine.py` güncellenir
- **Vatandaş portalı:** Aynı backend, `/vatandas/` route grubu, sonraki iterasyon

---

## 8. Açık Kararlar (Şimdi Kilitleme)

| Konu | Durum |
|:--|:--|
| Object storage (belge dosyaları) | Local disk (demo) → S3-uyumlu (prod) |
| pgvector vs Graph RAG | Faz 2'de karar; `belgeler.ocr_text` her iki senaryoya hazır |
| Vatandaş portalı abonelik modeli | Faz 4'te tasarlanır |
| Baro numarası doğrulama API'si | Faz 4'te değerlendirilir |
