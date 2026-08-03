# TODO — HakHukuk

> **Harita.** *Ne* yapılacağını burası, *hangi sırayla ve neye dikkat ederek*
> yapılacağını aktif icra belgesi söyler: **[`sprint3.md`](sprint3.md)** (`/goal sprint3.md`).
>
> Gerekçeler ve ölçülmüş açıklar: **[`ROADMAP.md`](ROADMAP.md)**
> Her koşudan önce: ⭐ [`docs/record/yurutme-tuzaklari.md`](docs/record/yurutme-tuzaklari.md)

---

## ✅ Bitti

| | sonuç |
| :--- | :--- |
| **Sprint 1** | `τ_grounding v1` · base/Gemini/`τ_g` aynı protokolde ölçüldü |
| **Sprint 2** | `τ_abstention v1` + merge → **`HakHukuk-4B-v0.1`** · ARA KAPI 🟢 · ADR-0039…0052 |
| **OSS geçişi** (2026-08-03) | Apache-2.0 · README · model kartı · yol haritası |

Kayıtlar: [`docs/record/research_log/`](docs/record/research_log/) ·
[`docs/adr/`](docs/adr/) · [`docs/record/kollar.md`](docs/record/kollar.md) ·
arşiv: [`docs/_arsiv/`](docs/_arsiv/)

---

## ▶ Şimdi — Sprint 3: HARNESS

Ayrıntı, kapılar ve değişmezler [`sprint3.md`](sprint3.md)'de.

- [ ] **Tasarım kararları** → ADR-0053+ *(kod yazılmadan çözülür)*
  - [x] **K2** chunk birimi → **madde** (atıf birimi olduğu için); uzun maddeler
        gömme için örtüşen pencerelere bölünür, madde kimliğiyle tekilleştirilir
  - [x] **K3** korpus → **canlı API şart**; ölçüm donmuş anlık görüntüde kalır
        (tekrarlanabilirlik) — iki mod, tek arayüz
  - [x] **K5** red kapısı → [ADR-0038](docs/adr/0038-red-kapisi-esigi-kati.md) **katı**; aşırı-red ölçülecek
  - [ ] **K1** gömme modeli → adaylar **recall@k** ile **ölçülür**, seçilmez
  - [ ] **K4** ⭐ harness AÇIK ölçüm protokolü → tasarlanıp ADR olarak sunulur
- [ ] **Adım 0** — modül-başına normalleştirme *(1 sa · $0)*
      kabul: M2b > 0,877 **ve** M1 kütlesi ≥ %71,6 *(ikisi birden)*
- [ ] **Adım 1** — retriever: indeks + `recall@k`
- [ ] **Adım 2** — atıf doğrulayıcı *(deterministik, hakem gerekmez)*
- [ ] **Adım 3** — red kapısı
- [ ] **Adım 4** — ⭐ **harness AÇIK ölçüm** — gerçek ürün sayımız, **hiç görülmedi**
      → 🛑 DUR, açık/kapalı tabloyu insana sun

---

## Sonra

### Model — harness'tan sonra, doğru girdi dağılımını bilerek

- [ ] **`τ_a` v2** — şablon ezberi ([ADR-0051](docs/adr/0051-m2b-cift-kalibi-ve-chosen-uretimi.md) B planı: `chosen`'ı hakemle üret) · ~$2
      *kanıt: M1 medyan cevabı **58 karakter** = şablonun kendisi*
- [ ] **Türkçe muhakeme** — iz şu an İngilizce (8/8 ölçüldü)
      *vatandaş ürünü "okunabilir muhakeme" vaat ediyor; bu bir **ürün** açığı*
- [ ] Veri turu — 728 temiz negatif inceydi; hasat hattı kurulu ve ucuz

### Ürün

- [ ] **Vatandaş kipi** — sadeleştirme **istem katmanında**
      ⚠️ Sade dille *eğitmek* denendi ve **doğruluğu düşürdü** ([ADR-0010](docs/adr/gemma4-12b-dersler.md#adr-0010))
- [ ] HF yayını — `HakHukuk-4B-v0.1` + model kartı
- [ ] Sürüm kabul testi — frozen TEST (`data/eval/canon/`) **bir kez**, `v1.0` öncesi

### Boyut — kısıt kalktı

- [ ] 8B/12B — tezin tek-boyut kilidi ([ADR-0028](docs/adr/gemma4-12b-dersler.md)) **yok**
      *önce 4B'yi tavana yaklaştır: reçete büyüğe taşınır, tersi taşınmaz*

---

## ⏸️ Opsiyonel — iddia katmanı (yalnız arxiv'e karar verilirse)

*"Merge, karışık ve ardışık SFT'den daha iyi korur"* iddiasını kanıtlayan karşılaştırma.
**Ürün için gerekli değil** — *"daha iyi mi"* sorusunu ölçüm zaten cevaplıyor; bu,
*"neden daha iyi"* sorusunu cevaplıyor.

Tam tarif hazır: [`docs/_arsiv/sprint2b.md`](docs/_arsiv/sprint2b.md) — artefaktlar
(`τ_g` · `τ_a` · veri · protokol) bozulmuyor, istenen zaman koşulur.

- [ ] **CP4** taban A, tek-aşamalı karışık · ~$16,36 *(3 epoch = merge'in **2,5×** hesabı)*
- [ ] **CP5** taban B, ardışık · ~$1,28
      ⭐ FT-5 **yeniden eğitilmez**: `τ_g v1` onun ta kendisi (~$4,4 tasarruf **ve** daha temiz kıyas)
- [ ] **CP5c** on-policy kontrol · ~$1,50 — *"tabanı zayıf eğittiniz"* itirazına sigorta
- [ ] **Kapı 5** kararı → 🛑 insana sun

⚠️ **Açık kalem:** ön-kayıtlı metin CP4'ü *"karışık **SFT**"* diyor ama `τ_a` **ORPO** ile
eğitildi. Saf SFT koşmak *yöntemi* değil *hedefi* ölçer ve Kapı 5'i çürütülebilir kılar.
Öneri: karışık ORPO (`is_pref` satır maskesi — `MaskedORPOTrainer` zaten destekliyor).

---

## Kalıcı kurallar

```
ölçüm     thinking on · 1024+512 · seed 3407 · chunk 900 · Q4_K_M + llama-server
havuz     DEV ile çalışılır; frozen TEST sürüm kabul testi, BİR KEZ
bütçe     Modal PANELDEN okunur, defterden türetilmez (tuzak 6.3)
kayıt     her bulgu AYNI GÜN research_log; her karar bir ADR
tek eksen tek metrik davranışı tarif etmiyorsa iki metrik: kütle = coverage × A1
```
