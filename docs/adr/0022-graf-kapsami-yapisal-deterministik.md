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
   Bedesten atıf-doğrulayıcı + red kapısı. → **Manşet konfigürasyon.**
2. **(b) çok-ajanlı / LLM-indeksli GraphRAG MANŞET DIŞI** — ama *yasak değil*: bkz. §"Sınır nasıl
   çizilir" (opsiyonel Pareto noktası).
3. **OCR harness'a dahil DEĞİL** — ingestion katmanı, Faz 3 app. Harness metin *alır*.

### Sınır nasıl çizilir: **flu değil, etiketli** *(2026-07-23 netleştirmesi)*

Kullanıcı itirazı yerindeydi: *"ileride agentic de olabilir, neden net çiviliyoruz, ikisi de mümkün
olacak şekilde flu bırakamaz mıyız?"* — çivi **ürün yol haritasına değil, manşet iddiaya** çakılı.
Kapsamı **flu bırakmak** üç şeyi bozar:

1. **Adalet kuralı (§5.2):** harness'a ne koyarsan rakiplere de aynısı verilir. Sınır flu olursa
   *"bizde graf vardı, onlarda yoktu"* sorusu cevapsız kalır → kıyas **çürütülemez** hale gelir.
2. **Maliyet metriği:** manşet $/sorgu tekrar üretilemez olur.
3. **Ön-kayıt:** kapılar veriden önce yazıldı; kapsam sonradan esnerse sayıyı görüp kale direği
   kaydırılmış olur.

**Çözüm — flu sınır değil, ölçülmüş ikinci nokta.** Tez zaten bir **Pareto eğrisi**; (b) eğriyi
bozmaz, **etiketlenmiş ek bir nokta** olarak zenginleştirir:

```
kalite ▲
       │        ◆ + çok-ajanlı GraphRAG (~3× maliyet)   ← OPSİYONEL kol
       │   ★ FT + deterministik harness                 ← MANŞET (parite iddiası burada)
       │  ○ base + harness (E)
       └────────────────────────────────────────────►  maliyet
```

- **Manşet** deterministik kalır → parite iddiası kurulur, maliyeti dürüst sayılır.
- **(b) zaman kalırsa** ayrı, maliyeti **açıkça yazılmış** bir nokta olarak raporlanabilir.
- Yan kazanç: LegalGraphRAG'in **raporlamadığı** şeyi raporlamış oluruz (maliyet/gecikme) —
  literatürde açık boşluk.
- Aynı ilke **agentic (Faz 3)** için de geçerli: ürün yol haritasında serbest (`VISION.md` Faz 3-5
  hiç kısıtlanmadı), tez manşetinde yok.

Yani kural: **sınır net, kapsam genişletilebilir — ama her genişleme kendi maliyet etiketiyle
ayrı bir nokta olarak ölçülür, manşetin içine sessizce karışmaz.**

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
