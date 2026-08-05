# Arşiv — tarihî belgeler

Buradaki hiçbir belge **silinmedi**; içlerindeki ölçümler, elenen alternatifler ve
gerekçeler hâlâ değerli. Ama artık **yürürlükte değiller**.

| belge | neydi | neden arşivde |
| :--- | :--- | :--- |
| [`sprint1.md`](sprint1.md) | `τ_grounding` + üç çıpa | ✅ kapandı 2026-07-29 |
| [`sprint2.md`](sprint2.md) | `τ_abstention` + merge + ARA KAPI | ✅ kapandı 2026-08-03, 🟢 güçlü yeşil |
| [`sprint2b.md`](sprint2b.md) | CP4-CP5 tabanları (iddia katmanı) | ⏸️ **ertelendi** — arxiv'e karar verilirse **olduğu gibi koşulur**; tarifi, maliyet aritmetiği ve *FT-5 = `τ_g`* bulgusu içinde |
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
| **plan** | `docs/plans/` | *ne yapılacak* — `- [ ]` kutucuklu, uygulanınca üstüne ✅ kapanış kutusu konur |
| **icra** | repo kökü `sprint*.md` | sprintin canlı belgesi; kapanınca **kayda** dönüşür |
| **arşiv** | `docs/_arsiv/` | yürürlükten kalkmış her tür |

**Kural:** bir belge *"sırada ne var"* diyorsa **plandır** ve `record/` altında duramaz.
