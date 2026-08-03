# `docs/record/` — araştırma kaydı

Bu klasör **ne olduğunu** tutar. Kararların *neden*i `docs/adr/`'de, yapılacaklar `TODO.md`'de,
tasarım `TASARIM.md`'de.

| ne | nerede |
| :--- | :--- |
| **Yeni hattın kronolojisi** (girdiler #39'dan devam) | [`research_log/`](research_log/) |
| **Gemma 4 12B hattının tam kronolojisi + sayıları** | [`gemma4-12b-kronoloji.md`](gemma4-12b-kronoloji.md) |
| Emekli hattın **damıtılmış dersleri** + karar kaydı | [`../adr/gemma4-12b-dersler.md`](../adr/gemma4-12b-dersler.md) |
| **Eğitilmiş kolların künyesi + versiyonlama** | [`kollar.md`](kollar.md) — `τ_X` adaptörleri, rejim, `‖τ‖`, açık kalemler |
| Emekli hattın artefaktları | ⚠️ **Adaptörler kalıcı KAYIP** (repo dışı paket 2026-07-29'da silindi, kasıtlı — ADR-0034 üst notu). Metinler git geçmişinde: `git show a19fc25^:old-version-gemma4-12b/<yol>` |

## Hangi belge ne işe yarar

**`gemma4-12b-kronoloji.md`** — *ne oldu ve kaç çıktı.* 38 girdinin birleşik hâli; protokol künyesi,
her turun tam skorkartı, ölçüm dosyalarının yolları, ders ve paper eşlemesi (arxiv opsiyonel). **Sayılar birebir korundu.**
OSS şeffaflık kaydının çekirdeği — ve arxiv yazılırsa **Results**'ın ham maddesi.

**`../adr/gemma4-12b-dersler.md`** — *bundan ne öğrendik.* Base-bağımsız dersler (veri · eğitim
davranışı · değerlendirme · operasyonel tuzaklar · metodoloji) + 26 ADR'nin karar kaydı.
Yöntem ve sınırların kaydı — arxiv yazılırsa **Methodology**/**Limitations**'ın ham maddesi. **Yeni hatta başlayan
önce burayı okur.**

**`research_log/`** — yeni hattın canlı günlüğü. Kurallar orada.

---

> ⚠️ **2026-07-24 — birleştirme notu.** 38 tekil `research_log` girdisi ve 26 tekil ADR dosyası
> kullanıcı kararıyla ikişer belgede toplandı; tekil dosyalar silindi (git geçmişinde duruyor,
> `4d70a77` ve öncesi). Bu, ADR-0024'ün *"kayıt yerinde kalır"* kuralından **bilinçli bir sapmadır**
> — gerekçe: 64 belgelik okuma yüzeyi yeni hatta başlayan için filtresiz bir yığındı. Kuralın özü
> (**içerik silinmez, sayılar kaybolmaz**) korundu.
