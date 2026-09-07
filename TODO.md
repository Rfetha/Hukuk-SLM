# TODO — bugün koşulabilir olanlar

> Her satır bir [`ROADMAP.md`](ROADMAP.md) adımına bağlıdır. Bir satırın burada olması için
> **bugün koşulabilir** olması gerekir: bekleyen bir karara ya da bitmemiş bir işe bağlıysa
> buraya değil, ROADMAP'e yazılır.
> ⛔ Kutucuk yalnız `verify:` çıktısı **gerçekten alındıktan sonra** işaretlenir.

## Şimdi — Faz 3 kapanışı → 🏷️ `v0.2`

- [ ] `MODEL_CARD.md` yeni manşetle güncellensin · *"ESKİ BİRİM"* bandı kalksın ·
      **tek aile hakem** borcu Limitations'a girsin → [ROADMAP · Faz 3](ROADMAP.md#-faz-3--belge-katmanı-0--️-v02)
- [ ] Kırık linkler onarılsın (`CLAUDE.md` · `README*.md`) — ⛔ `docs/record/**` ve
      `docs/adr/**`'ye **DOKUNMA** → [ROADMAP · Faz 3](ROADMAP.md)
- [ ] `v0.2` etiketi → [ROADMAP · Faz 3](ROADMAP.md)

## Sırada — Faz 4, Hat B → 🏷️ `v1.0`

- [ ] **B1 · isabetsizlik** turu: 8/80, rakiplerden iyi değil, hiç çalışılmadı
      → [ROADMAP · Faz 4](ROADMAP.md#-faz-4--hat-b-model-7-15-modal--️-v10-kapısı)
- [ ] **B4 · `τ_a` genlik** turu: merge'de 0,987 → 0,766 → [ROADMAP · Faz 4](ROADMAP.md)
- [ ] **Kabul testi**: donmuş TEST **tek kez** açılır; ADR-0069 raporlaması zorunlu
      → [ROADMAP · Faz 4](ROADMAP.md)

## Ucuz ve bağımsız — herhangi bir sırada

- [ ] `recall_taban.json` yazılsın — Faz 0'ın tek *"kaynaklanmadı"* ihlali · **$0**, ~15 dk
- [ ] `models/` ~20 GB temizliği (T1) — S7 kapandı (yalnız merge GGUF yayımlanır) · **$0**
- [ ] 🆕 **Korpus bütünlüğü:** `4857/Madde 111` **yineleniyor** ve iki kopyanın `mulga` alanı
      **çelişiyor** (biri `True`, biri `False`) — ölçüldü 2026-09-07 · **$0**
- [ ] 🆕 `terazi` 1. soruda **aynı atfı iki kez** üretiyor (`('', 'Madde 31', False)` ×2);
      yinelenen atıf kullanıcıya iki uyarı gösterir · **$0**

## Bekliyor — bugün koşulamaz, sebebi yazılı

| iş | neyi bekliyor |
| :--- | :--- |
| **Görev 8** · indeks dağıtımı (HF dataset) | mevzuat kapsam planı — bugünkü 79 MB'ı paketlemek boşa iş (8,4× büyüyecek) |
| **Görev 11 Adım 2** · temiz makine kapısı | Görev 8 — indeks git'te yok, `git clone` çalışan ürün vermiyor |
| Üçüncü hakem ailesi · rakip kolunun yeniden puanlanması | bütçe — bakiye $3,45, tahmini fatura $2,81 ([ADR-0074](docs/adr/0074-hakem-paneli-kuruldu-baglayici-hukum.md)) |
| Sorumluluk ibaresinin nihai metni | hukukçu görüşü (**S10**) |
