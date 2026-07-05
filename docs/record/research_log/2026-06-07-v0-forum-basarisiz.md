### 2026-06-07/08 — v0 (forum verisi) → BAŞARISIZ
- **Veri:** `data/processed/sft_v0/` — 29K, `turkish_law_qa_dataset` + `turkish-law-chatbot` (forum).
- **Sonuç:** modeli batırdı (base-altı doğruluk).
- **Post-mortem (2026-06-13 kanıtlandı):** "7 Kasım 1982'de yürürlüğe girmiştir." cevabı **154 farklı soruya birebir** yapıştırılmış; atıf oranı düşük (~%13.6 sıkı ölçüt). → forum verisi sistemik kirli.
- **Ders (paper K3 adayı):** kaynaksız QA verisi doğruluğu öğretmez, halüsinasyon hattı ezberletir.

