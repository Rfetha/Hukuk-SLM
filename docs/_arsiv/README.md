# Arşiv — tarihî belgeler

Buradaki hiçbir belge **silinmedi**; içlerindeki ölçümler, elenen alternatifler ve
gerekçeler hâlâ değerli. Ama artık **yürürlükte değiller**.

| belge | neydi | neden arşivde |
| :--- | :--- | :--- |
| [`sprint1.md`](sprint1.md) | `τ_grounding` + üç çıpa | ✅ kapandı 2026-07-29 |
| [`sprint2.md`](sprint2.md) | `τ_abstention` + merge + ARA KAPI | ✅ kapandı 2026-08-03, 🟢 güçlü yeşil |
| [`sprint2b.md`](sprint2b.md) | CP4-CP5 tabanları (iddia katmanı) | ⏸️ **ertelendi** — arxiv'e karar verilirse **olduğu gibi koşulur**; tarifi, maliyet aritmetiği ve *FT-5 = `τ_g`* bulgusu içinde |
| [`sprint3-part1.md`](sprint3-part1.md) | HARNESS — retriever + atıf doğrulayıcı + red kapısı, ve ilk harness-AÇIK ölçümü | ✅ kapandı 2026-08-05. **Kökten buraya 2026-08-06'da taşındı** — kapanmış icra belgesi kökte kalmıştı, sprint1/2/2b ise zaten arşivdeydi. Ürünün dürüst sayısı (**kütle %61,3**), dört ölçülmüş mekanizma ve **açık borç kuyruğu** (B1 · B7 · B9 · B10 …) içinde |
| [`V2_PLAN.md`](V2_PLAN.md) | 12B hattının v2 reçetesi | hat emekli (ADR-0027) |
| [`TEKNIK_PLAN.md`](TEKNIK_PLAN.md) | eski icra planı | yerini `sprint*.md` + `ROADMAP.md` aldı |
| [`superpowers/`](superpowers/) | 12B dönemi planları + tez çerçevesi speci | çerçeve 2026-08-03'te aşıldı |
| [`devir-notu-2026-07-29.md`](devir-notu-2026-07-29.md) | Sprint 1 → Sprint 2 oturum devir notu | görevi bitti 2026-08-03; **2026-08-05'te `docs/record/sprint1/`'den taşındı** — bir **plan/devir** belgesiydi, kayıt değil. `record/` *ne olduğunu* tutar, *ne yapılacağını* değil. Kararları [ADR-0039…0042](../adr/)'de yaşıyor |
| [`ft-is-akisi.mmd`](ft-is-akisi.mmd) | uçtan uca iş akışı şeması | kendini SÜPERSEDED ilan etmişti (ADR-0035); tez kafesine göre çizilmiş. Güncel artefakt şeması: [`../model-soyagaci.mmd`](../model-soyagaci.mmd) |

**Güncel yön:** [`ROADMAP.md`](../../ROADMAP.md) · artefakt kimlikleri:
[`kollar.md`](../record/kollar.md)

⚠️ **`docs/record/` ve `docs/adr/` arşiv DEĞİLDİR** — onlar yürürlükteki araştırma
kaydı ve karar defteridir.

### 📁 Belge türü → yeri *(2026-08-05'te netleştirildi)*

| tür | nerede | ne tutar |
| :--- | :--- | :--- |
| **kayıt** | `docs/record/` | *ne oldu, sayı neydi* — geriye dönük, kutucuk yok |
| **karar** | `docs/adr/` | *neden böyle, hangi alternatif elendi* |
| **spec** | `docs/superpowers/specs/` | *ne kuracağız, hangi alternatif elendi* — `brainstorming`/`grill` çıktısı |
| **plan** | `docs/superpowers/plans/` | *ne yapılacak* — `- [ ]` kutucuklu, uygulanınca üstüne ✅ kapanış kutusu konur |
| **icra** | repo kökü `sprint*.md` | **yalnız AÇIK sprintin** canlı belgesi |
| **arşiv** | `docs/_arsiv/` | yürürlükten kalkmış her tür |

**İki kural:**

1. Bir belge *"sırada ne var"* diyorsa **plandır** ve `record/` altında duramaz.
2. **Kapanan icra belgesi arşive taşınır** — kökte yalnız açık olan durur *(2026-08-06'da
   netleşti: `sprint3-part1.md` kapandığı hâlde kökte kalmıştı, oysa sprint1/2/2b arşivdeydi;
   aynı durumdaki iki belge iki yerdeydi)*. Taşırken **gelen ve giden bağlantılar yeniden
   hesaplanır** — depoda kırık bağlantı sayısı taşımadan önce de sonra da **0**'dır.
