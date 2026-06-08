# ADR 0005 — Veri stratejisi: lisans-temiz kaynak + EDA-doğrula + grounded sentetik üretim

- **Durum:** Yürürlükte (2026-06-08)
- **Geriye dönük kayıt** (kararlar mayıs sonu–haziran başı birikti).

## Bağlam
İki kısıt çakışıyor: (1) **lisans-temizlik** — ticari kaynaklar (Lexpera, Kazancı) telif zehiri,
repo private olsa da yasak; (2) **veri açığı** — vatandaş-dilli, niş, senaryo→statü çiftleri hazır
dataset olarak yok. Üstüne acı ders: "iyi görünen" açık dataset'ler içerikçe çöp çıkabiliyor.

## Karar
- **Yalnız açık/kamu kaynak:** Mevzuat.gov.tr, Resmi Gazete, Yargıtay açık portal, Apache-2.0 HF
  dataset'leri. PII maskele. Ground truth = Mevzuat.gov.tr.
- **Her dataset'i güvenmeden ÖNCE EDA ile örnekle-doğrula** (sert kural).
- **Eksik veri = grounded sentetik üretim:** gerçek madde metni → LLM çift üretir → groundedness ile
  doğrula (ADR 0002). Üretici = GPT-4o-mini (faithfulness kanıtlı, ~20K ≈ $1.2 → para engel değil).
- **Canlı mevzuat kaynağı = `bedesten.adalet.gov.tr` JSON API** (auth-free, TR-IP şart), frozen
  `muhammetakkurt/mevzuat-gov-dataset` (907 laws, Eyl 2024) yerine freshness/kapsam gerektiğinde.

## Değerlendirilen alternatifler
- **`newmindai/EuroHPC-Legal`** (43K, Apache-2.0, "harika görünüyordu") → REDDEDİLDİ. Örnekleme
  çöp gösterdi: eşleşmeyen Q&A, halüsine kanunlar, Osmanlı-dönemi içerik. **EDA-doğrula kuralının
  doğuş anı.**
- **Eski 32K forum/karışık veri (v0)** → REDDEDİLDİ. Doğruluğu düşürdü + kaynaksız (puanlanamaz).
  v1'e KATILMADI (ADR 0002).
- **Yerel Gemma ile sentetik üretim bake-off'u** → ATLANDI; GPT-4o-mini kanıtlı + ucuz, gereksiz.
- **Osmanlı/Mecelle-dönemi içerik** → kapsam dışı; scope = yürürlükteki Türkiye Cumhuriyeti mevzuatı.

## Sonuç
- Doğrulanmış-kullanılabilir: `OrionCAF/turkish_law_qa_dataset`, `Renicames/turkish-law-chatbot`
  (Apache-2.0). v1 = ~21K saf grounded (`gen_sft_v1.py`), 40K madde havuzu (`mevzuat_maddeler.jsonl`).
- Bulk kanun çekimi Faz 2'ye ertelendi (donmuş 40K madde Faz 1 için yeterli).
- Araçlar: `scan_hf_datasets.py`, `eda_datasets.py`, `bedesten_probe.py`.

## İlgili
`docs/VERI_PLANI.md`, `docs/BEDESTEN_API.md`, ADR 0002, ADR 0007
