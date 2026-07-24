# Mimari/Metodoloji Karar Kayıtları (ADR)

Bu klasör, HakHukuk'ta **neden** belirli bir yol seçtiğimizi kaydeder — sadece *ne* yaptığımızı değil.
Amaç tek: **paper yazılırken** (ve altı ay sonra kendimize) *"şunu neden böyle yaptık, hangi
alternatifi neden eledik, sonuç ne oldu"* sorusu kanıtla cevaplanabilsin.

---

## ⚠️ 2026-07-24 — defter sadeleştirildi

Gemma 4 12B hattının **26 ADR'si (0001-0026) tek dosyada toplandı ve tekil dosyalar silindi:**

### 📕 [`gemma4-12b-dersler.md`](gemma4-12b-dersler.md)

Üç bölüm: **(A) Dersler** — base-bağımsız, taşınan bilgi; yeni hatta başlayan burayı okur ·
**(B) Karar kaydı** — 26 ADR'nin kararı, elenen alternatifleri, sonucu ve *yeni hattaki statüsü* ·
**(C) Ham kayda giriş noktaları.**

**Neden.** 26 ayrı dosya, yeni hatta başlayan için filtresiz bir yığındı ve çoğu 12B'ye özgüydü.
Karar: **okuma yüzeyi tek belgeye insin, içerik kaybolmasın.** Silinen dosyalar git geçmişinde
duruyor (`4d70a77` ve öncesi) — geri alınabilir.

**Atıf uyumu.** Repo genelinde ~560 yerde `ADR-00NN` göndermesi var (`research_log`, spec'ler,
`knowledge/`, script yorumları). O göndermeler **bozulmadı**: birleşik belge her ADR için bir çapa
taşıyor → `gemma4-12b-dersler.md#adr-0011` gibi.

> ⚠️ Bu, ADR-0024'ün *"`adr/` yerinde kalır, silinmez"* kuralından **bilinçli bir sapmadır**
> (kullanıcı kararı, 2026-07-24). Aynı kuralın diğer yarısı — **`docs/record/research_log/`
> asla taşınmaz/yeniden yazılmaz** — aynen yürürlüktedir.

---

## Dizin — yeni hat

| # | statü | konu |
| :-- | :--: | :--- |
| **[0027](0027-tasarim-kilitleri-paralel-kol-merge.md)** | 🟢 | ⭐⭐ **Tasarım kilitleri:** paralel kol + task-vector merge · iki matris (iç ablasyon harness-kapalı / dış parite) · DEV/TEST ayrımı · dört katmanlı hakem savunması · kapılı hibrit graf kolu. *(“iki boyut noktası” maddesi → **0028 ile süperseded**)* |
| **[0028](0028-tek-boyut-noktasi.md)** | 🟢 | ⭐ **Tek boyut noktası:** tez tek base'de tamamlanır (FT 10→6, sprint 6→5). İkinci boyut = tez sonrası, aynı reçeteyle. Bedeli — dış geçerlilik açığı kapanmıyor · kapasite ekseni ölçülemiyor · ADR-0018'in eğri şartı karşılanmıyor — **limitations'a yazılır** |
| **[0029](0029-model-erisim-kapisi.md)** | 🟢 | **Tek model erişim kapısı** (`scripts/llm_client.py`) — hakem paneli + rakipler tek yerden, geriye dönük uyumlu. Çok-aile **Sprint 2-3'te** gerekli, Sprint 1'de değil. İki kilit: parite fiyatı **birincil-kaynak liste fiyatıdır** (kapı marjı değil) · sağlayıcı yönlendirmesi pinlenir ve koşuya kaydedilir |

**Otorite tasarım belgesi:** [`TASARIM.md`](../../TASARIM.md) (repo kökü) — ne inşa edeceğimiz ve
neyi ölçeceğimiz. ADR-0027 onun kararlarını donmuş anlatı olarak kaydeder.
Kullanıcı taslağı `referans-design-doc.md` **temiz tutulur, değiştirilmez.**

**Eski hattan taşınan kararlar** (ADR-0004 Modal · 0005 veri stratejisi · 0007 lisans · 0008 `spawn` ·
0010 uzman register · 0011 CANON · 0013 mod matrisi · 0016 dış benchmark · 0017 tez çerçevesi ·
0018 soft gate · 0019 faz istisnası · 0020 rakip seti · 0022 graf kapsamı · 0024 emeklilik ·
0025 eval yolu · 0026 base parametre) → [`gemma4-12b-dersler.md`](gemma4-12b-dersler.md) Bölüm B.

---

## Neden ADR

Canlı planlar (`TASARIM.md`, `TODO.md`) **mevcut durumu** özetler — sık güncellenir, üzerine yazılır.
ADR ise **dondurulmuş anlatıdır**: bir kararın o ANki bağlamı + değerlendirilen seçenekler + gerekçe
+ sonuç. Plan *"ana metrik groundedness"* der; ADR *"şu üç alternatifi şu yüzden eledik, şu riski
kabul ettik"* der. **Paper'ın Methodology ve Limitations bölümleri ADR'lerden yazılır.**

## Format

Her ADR: `NNNN-kebab-baslik.md`.

- **Statü:** Önerildi | Kabul edildi | Yürürlükte | Süperseded (→ NNNN) | Geri alındı
- **Bağlam** — karar anında ne biliyorduk, hangi kısıt zorladı
- **Karar** — ne yaptık
- **Değerlendirilen alternatifler** — neyi neden elemedik/seçmedik *(paper için kritik kısım)*
- **Sonuç** — kanıt/sayı + kabul edilen risk + açık uçlar
- **İlgili** — plan satırı, commit, ilgili ADR

**Kararı değiştirirsek eskiyi silmeyiz** → "Süperseded" işaretler, yenisini ekleriz. Eski gerekçe
yanlış çıksa bile *neden öyle düşündüğümüz* paper malzemesidir.

## Diğer kayıt yerleri

- [`../record/research_log/README.md`](../record/research_log/README.md) — kronolojik deney günlüğü.
  **Kesintisiz akar**, taşınmaz, yeniden yazılmaz. Yeni hattın girdileri #39'dan devam eder.
- [`gemma4-12b-dersler.md`](gemma4-12b-dersler.md) — emekli hattın kararları + dersleri.
- `old-version-gemma4-12b/` — emekli hattın artefaktları (adaptörler, eval çıktıları, tur belgeleri).
