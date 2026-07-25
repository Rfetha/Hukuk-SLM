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
| **[0030](0030-base-secimi-qwen35-4b-ve-dusunce-modu.md)** | 🟢 | ⭐ **Base = `Qwen/Qwen3.5-4B`** (sha pinli), §8 kapısı **6/6**. Ad düzeltmesi: HF'de `-Instruct` yok. **Düşünce modu KAPALI koşulur** — varsayılan modda model `</think>`'i kapatmıyor, `content` BOŞ dönüyor (HTTP 200, sıfır hata). Gerekçe kolaylık değil **eğitim-eval hizalaması**: SFT verisi akıl yürütme izi taşımıyor, şablon zaten boş düşünce bloğu üretiyor. Boş cevapta **kod erken patlıyor** |
| **[0031](0031-precision-inference-q4km-egitim-bf16-lora.md)** | 🟡 | **Precision:** dağıtım **Q4_K_M** sabit (kullanıcı kararı; Q8_0 <8 GB'a sığıyor ama başlık bırakmıyor + decode %28 yavaş) · eğitim **bf16 taban + LoRA**, QLoRA değil. VRAM × bağlam matrisi **ölçüldü** → TASARIM §12 borcu kapandı. ⚠️ Eğitim kolu **ölçüme bağlı**, karar kuralı önceden yazılı |
| **[0032](0032-hakem-paneli-uc-aile-ve-aile-dislama.md)** | 🟢 | **Hakem paneli = OpenAI · Anthropic · Google** (özne ailesi Qwen'den ayrık). Aile-dışlama haritası çizildi; **asimetri** (bizde 3 hakem, rakipte 2) ve **kendi öznemizde self-preference ölçülemiyor** sınırı önceden yazıldı. `TASARIM.md` §13 açık soru **5'i kapatır.** Sürüm pinleme + harcama **Sprint 3** |
| **[0033](0033-egitim-hizi-fla-core-checkpointing-batch.md)** | 🟢 | **Eğitim hızı — Faz B'nin kapısı açıldı.** Devir notunun *"fla torch≥2.11 istiyor"* teşhisi **çürütüldü**: `flash-linear-attention` 0.5.x'te bölünmüş, çekirdekler **`fla-core`**'da ve `--no-deps` onu atlıyordu → `import fla` çalıştığı için transformers fast-path'i **açık sanıp çöküyordu** (fla'sız durumdan kötü). Düzeltmeyle **36 → 10.5 s/it (3.4×)**, pinli lock korundu. Kalan kaldıraçlar **kalite-nötr olanlarla sınırlandı** (checkpointing kapalı · batch 2×8, etkin batch 16 sabit); **`dropout=0` REDDEDİLDİ** — CP6'nın yan-hasar ölçümünde atfedilebilirliği bozardı. Teşhis aracı: `modal_diag.py`. Bütçe $35 → **$42.50** |

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
