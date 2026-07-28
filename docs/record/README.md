# `docs/record/` — araştırma kaydı

Bu klasör **ne olduğunu** tutar. Kararların *neden*i `docs/adr/`'de, yapılacaklar `TODO.md`'de,
tasarım `TASARIM.md`'de.

| ne | nerede |
| :--- | :--- |
| **Yeni hattın kronolojisi** (girdiler #39'dan devam) | [`research_log/`](research_log/) |
| **Gemma 4 12B hattının tam kronolojisi + sayıları** | [`gemma4-12b-kronoloji.md`](gemma4-12b-kronoloji.md) |
| Emekli hattın **damıtılmış dersleri** + karar kaydı | [`../adr/gemma4-12b-dersler.md`](../adr/gemma4-12b-dersler.md) |
| Emekli hattın artefaktları (adaptör, eval çıktıları, tur belgeleri, SCORECARD) | `~/code/hukuk-devir/` *(repo dışı — ADR-0034)* · metinler ayrıca `git show a0575e6:old-version-gemma4-12b/<yol>` |

## Hangi belge ne işe yarar

**`gemma4-12b-kronoloji.md`** — *ne oldu ve kaç çıktı.* 38 girdinin birleşik hâli; protokol künyesi,
her turun tam skorkartı, ölçüm dosyalarının yolları, paper eşlemesi. **Sayılar birebir korundu.**
Paper'ın **Results** bölümünün ham maddesi.

**`../adr/gemma4-12b-dersler.md`** — *bundan ne öğrendik.* Base-bağımsız dersler (veri · eğitim
davranışı · değerlendirme · operasyonel tuzaklar · metodoloji) + 26 ADR'nin karar kaydı.
Paper'ın **Methodology** ve **Limitations** bölümlerinin ham maddesi. **Yeni hatta başlayan
önce burayı okur.**

**`research_log/`** — yeni hattın canlı günlüğü. Kurallar orada.

---

> ⚠️ **2026-07-24 — birleştirme notu.** 38 tekil `research_log` girdisi ve 26 tekil ADR dosyası
> kullanıcı kararıyla ikişer belgede toplandı; tekil dosyalar silindi (git geçmişinde duruyor,
> `4d70a77` ve öncesi). Bu, ADR-0024'ün *"kayıt yerinde kalır"* kuralından **bilinçli bir sapmadır**
> — gerekçe: 64 belgelik okuma yüzeyi yeni hatta başlayan için filtresiz bir yığındı. Kuralın özü
> (**içerik silinmez, sayılar kaybolmaz**) korundu.
