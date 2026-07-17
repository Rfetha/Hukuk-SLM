# ADR-0019 — Faz sırası istisnası: harness dilimi teze dahil, graph-RAG hariç

**Statü:** Yürürlükte · **Tarih:** 2026-07-17
**İlgili:** ADR-0017 · `VISION.md §2` (faz sırası) · `CLAUDE.md` (Phase ordering) · spec §5, §10

## Bağlam
`VISION.md §2` + `CLAUDE.md` sert kural: *"Faz 1 bitmeden Faz 2'ye (RAG/Graph) atlama."* Yeni tez (ADR-0017) tam da bunu gerektiriyor: **maliyet-normalize parite iddiası harness olmadan kurulamaz** — çünkü adil kıyas "rakip + aynı harness" (D vs B) ve tezin ana ablasyonu "base + harness" (E). Faz sırası ya tez lehine esneyecek ya tez küçülecek.

## Karar
**Faz sırası TEK bir istisnayla esnetilir:** Faz 2'nin **retriever + atıf-doğrulayıcı + red-kapısı** dilimi **teze dahildir.**

- ✅ **Dahil:** hibrit retriever (BM25 + TR embedding), Bedesten API atıf-doğrulayıcı (deterministik), red kapısı.
- ❌ **Hariç (kesin future-work):** graph-RAG / Knowledge Graph (Neo4j/Memgraph), vanilla-vs-graph-RAG karşılaştırması (eski "Katkı 3"). Parite iddiasına sıfır katkı, takvimin yarısını yer, iki ayrı hikâyeyi seyreltir.
- ❌ **Hariç:** Faz 3 (agents, app, serving) — kapsam dışı.

## Sonuç
- Harness üç bağımsız bileşen; her biri ayrı ablasyon edilebilir (spec §5).
- **Adalet kuralı (pazarlıksız):** harness tüm öznelere birebir aynı uygulanır — sadece kendi modelimize verirsek tez ölür.
- Harness ile v4 iş bölümü: harness = deterministik atıf-doğrulama; v4 = semantik answerability (atıfsız halüsinasyon + base-only dağıtım güvenliği). Çelişmez, tamamlar (spec §5, NEXT_SESSION).
- Graph-RAG'in tez sonrası değeri korunur (ürün vizyonu Faz 2, `VISION.md`).
