# ADR-0022 — Graf kapsamı: **yapısal/deterministik graf teze dahil**, çok-ajanlı GraphRAG hariç

**Statü:** Yürürlükte · **Tarih:** 2026-07-23
**Revize eder:** ADR-0019 (faz-sırası istisnası) — blanket graph yasağını daraltır
**İlgili:** ADR-0017 · ADR-0023 · spec §5 (harness), §5.1 (determinizm), §5.2 (adalet kuralı), §5.3, §11

## Bağlam

ADR-0019 harness dilimini teze dahil ederken **graph-RAG'i topluca dışarıda** bıraktı
(*"Parite iddiasına sıfır katkı, takvimin yarısını yer, iki ayrı hikâyeyi seyreltir"*).
Kullanıcı kapsamı yeniden açtı ve "graph-RAG" dediğini teyit etti.

Tarama sonucu **"graph-RAG" adı altında iki farklı iş** olduğunu gösterdi; ADR-0019 ikisini
ayırmadan yasaklamıştı. Ayrım yapılınca biri tezin maliyet iddiasıyla **hizalı**, diğeri
**ona karşı** çalışıyor.

## Değerlendirilen iki seçenek

**(a) Yapısal / deterministik graf.** Korpusun kendi yapısından çıkar: düğüm = kanun/madde;
kenar = hiyerarşi (kanun→madde→fıkra→bent), **atıf ağı** (maddeler arası çapraz referans),
**değişiklik/mülga zincirleri** (zamansal). Getirme = vektör araması → 1-2 hop genişletme.
İndeksleme döngüsünde **LLM yok.**

**(b) Tam / çok-ajanlı GraphRAG.** Chunk başına LLM ile varlık-ilişki çıkarımı, topluluk tespiti,
LLM üretimi topluluk özetleri; ya da LegalGraphRAG'in üç-ajanlı hattı
(Researcher → Auditor → Adjudicator).

| | (a) yapısal | (b) tam GraphRAG |
| :--- | :--- | :--- |
| İnşa | deterministik ayrıştırma | LLM çağrısı / chunk |
| Sorgu maliyeti | **~0 ek** | **~3× çıkarım** |
| Tez metriğine etkisi | nötr/olumlu | **olumsuz** (maliyet ekseni) |
| Determinizm (spec §5.1) | korur | bozar |
| Adalet kuralı (§5.2) maliyeti | ucuz | pahalı (rakiplere de verilecek) |
| Kapsamla ilişki | atıf-doğrulayıcı **zaten gerektiriyor** | yeni alt sistem |

## Karar

1. **(a) yapısal/deterministik graf TEZE DAHİL.** Harness = retriever + **yapısal graf** +
   Bedesten atıf-doğrulayıcı + red kapısı.
2. **(b) çok-ajanlı / LLM-indeksli GraphRAG KESİN DIŞARIDA** (future work, ürün Faz 2).
3. **OCR harness'a dahil DEĞİL** — ingestion katmanı, Faz 3 app. Harness metin *alır*.

### Neden (a) içeride

- **Zaten gerekiyordu.** ADR-0019 atıf-doğrulayıcıyı kapsama almıştı; bir atfı doğrulamak
  "Kanun X Madde Y"yi bir yapıya karşı çözmek demek — Türk mevzuatı **zaten bir graf**
  (hiyerarşi + atıf ağı + değişiklik zincirleri) ve Bedesten madde ağacını veriyor
  (`docs/BEDESTEN_API.md`). (a), doğrulayıcının kurduğu yapıyı getirmede de kullanmak.
- **Maliyet iddiasıyla hizalı.** Deterministik graf gezinmesi marjinal ~0 maliyet.
- **Determinizmi korur** (spec §5.1 harness'ın 2. ve 3. bileşeninin deterministik olmasını
  özellikle değerli buluyor).
- **Bedava eksen: zamansallık.** Mülga/değişik zincirleri CANON'da **yok**; rakiplerin
  yapamadığı, Bedesten'in veriyi zaten sunduğu bir kulvar (bkz. `knowledge/summary_citation_grounding.md`).
- **Temiz ablasyon:** "yapı-farkındalıklı getirme işe yarıyor mu?" (vektör vs vektör+graf).

### Neden (b) dışarıda

Tezin ana metriği **maliyet-normalize parite**. 3 ajanlı hat, cevap başına çıkarımı ~3×'ler ve
bu **doğrudan manşet metrikten** düşer. Üstelik adalet kuralı gereği rakiplere de aynı harness
verilecek → onların maliyeti de 3×. Yani (b) kaliteyi artırırken tezin ölçtüğü şeyi bozuyor.
LegalGraphRAG %6.3–19.1 kazanç raporluyor ama **maliyet/gecikme yükünü hiç raporlamıyor.**

## Ön-çalışma (2026-07-23 taraması)

- **SAT-Graph RAG** — *Ontology-Driven Graph RAG for Legal Norms* (FAIA251598, 2025):
  hiyerarşik + **zamansal** + açıkça **deterministik**; soyut "Work" vs sürümlenmiş "Expression"
  ayrımı Türk mevzuatına birebir oturur (kanun = Work, zaman içindeki hâlleri = Expression).
- **Citation Grounding** (arXiv 2606.00898): 100.8M karardan **deterministik** çıkarılmış atıf
  grafı (502M kenar, 21.736 mevzuat düğümü); atıf halüsinasyonunu **var mı / bağlama uygun mu /
  o tarihte yürürlükte miydi** diye ayırıyor. → (a)'nın doğrudan ön-çalışması.
- **LegalGraphRAG** (arXiv 2605.28120): = (b). SOTA iddiası var, maliyet raporu yok.

## Sonuç

- **ADR-0019 revize edildi:** "graph-RAG kesin hariç" → "**(a) dahil, (b) hariç**".
  ADR-0019'un gerekçesi (kapsam şişmesi, spec §11 "üç ayrı tez" riski) (b) için **hâlâ geçerli**;
  (a) için fazla genişti.
- **Adalet kuralı değişmedi (pazarlıksız):** yapısal graf dahil tüm harness, her özneye
  (rakipler dahil) **birebir aynı** uygulanır.
- **Spec §5.3 ve §11 güncellenecek** (o satırlar artık yanlış).
- **Yeni açık soru:** zamansal red kulvarı CANON'a eklenmeli mi? (v4 reçetesi + eval matrisi)
- Değişmeyen sınır: **Faz 3 (agents, app, serving) kapsam dışı.**

## İlgili

ADR-0019 · ADR-0017 · ADR-0023 · `docs/BEDESTEN_API.md` · `knowledge/summary_citation_grounding.md` ·
spec §5, §11, §12
