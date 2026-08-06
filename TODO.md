# TODO — HakHukuk

> **Harita.** *Ne* yapılacağını burası tutar. Part 1 kapandı ve **kayıt** oldu:
> [`sprint3-part1.md`](docs/_arsiv/sprint3-part1.md).
>
> **✅ Ölçüm boşlukları turu KAPANDI 2026-08-05** — `m2b` harness-AÇIK · B5 · B8 eğrisi ·
> B-i deneyi. Plan:
> [`2026-08-05-olcum-bosluklari.md`](docs/superpowers/plans/2026-08-05-olcum-bosluklari.md) ·
> sonuçlar: [**#56**](docs/record/research_log/2026-08-05-olcum-bosluklari.md).
> Çıkanlar: M2b iddiası **yapısal olarak öldü** (kapı bu rejimde ateşlenemiyor) → **eğitim borcu** ·
> B-i önsözü **başarılı** ama benimsenmedi (**YB1**) · `k` büyütmenin bedeli **iki eksende** ölçüldü.
>
> **▶ AKTİF PLAN: B10 aşırı-red turu** — `τ_a` v2 simetrik yeterlilik çifti + rakip kıyası.
> Plan (kutucuklar **tek durum kaynağıdır**):
> [`2026-08-06-asiri-red-tau-a-v2.md`](docs/superpowers/plans/2026-08-06-asiri-red-tau-a-v2.md) ·
> tasarım: [`2026-08-06-asiri-red-turu-design.md`](docs/superpowers/specs/2026-08-06-asiri-red-turu-design.md)
> adaylar ve ölçülmüş gerekçeleri `ROADMAP.md`'de ve borç kuyruğunda
> ([`sprint3-part1.md`](docs/_arsiv/sprint3-part1.md#post-sprint-3-sırası): **B10 · B1 · B4 · B8 ·
> B9 · B6** + **YB1 · YB2 · YB3**).
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

## 🎯 Vizyon — üç drop

```
🟦 A  model+harness → HF   ·   🟩 B  kurulabilir web app   ·   🟪 C  vatandaş platformu
```

Tasarım: [`docs/superpowers/specs/2026-08-03-yol-haritasi-design.md`](docs/superpowers/specs/2026-08-03-yol-haritasi-design.md)

## ✅ Sprint 3 **PART 1** — HARNESS · **KAPANDI 2026-08-05**

Tam kayıt, kapılar ve değişmezler [`sprint3-part1.md`](docs/_arsiv/sprint3-part1.md)'de.

> **Ürünün dürüst sayısı: kütle %61,3** (harness AÇIK, `k=10`, onarılmış korpus) ↔ %71,6
> (KAPALI = **tavan**, altın madde kurgu gereği verilir). Aradaki 10,2 puan **ayrıştırıldı**:
> ≈5,1 erişim ıskası (harness'ın) + ≈4,5 dikkat dağılması (modelin).
> GPU **$0** · hakem **$0,127** · 7 research_log · 3 ADR · 3 yeni tuzak.

- [ ] **Tasarım kararları** → ADR-0053+ *(kod yazılmadan çözülür)*
  - [x] **K1** gömme modeli → **`BAAI/bge-m3` + BM25, RRF hibriti** — ölçümle seçildi
        (`recall@10`: BM25 0,625 · e5-base 0,700 · bge-m3 0,800 · **hibrit 0,875**)
  - [x] **K2** chunk birimi → **TAM MADDE indekslenir**, 900 karakter kırpması yalnız
        bağlam **modele verilirken** ([ADR-0054](docs/adr/0054-harness-tasarim-kararlari-k2-k5.md))
        ⚠️ *önceki satır "örtüşen pencerelere bölünür" diyordu — o karar alınmadı, ADR-0054 bunu değiştirdi*
  - [x] **K3** korpus → **statikle başla**, canlı `bedesten` katmanı S3'ten sonra
        (ölçüm tekrarlanabilirliği). Sözleşme S3a'da sınandı: **4/4 GEÇERLİ**
  - [x] **K4** ⭐ harness AÇIK protokolü → küme **değişmez**, ayırt-edicilik etiketi eklenir,
        sayılar iki alt kümede ayrı raporlanır (ADR-0054) — ✅ **etiket turu koşuldu (S3, borç B2 kapandı)**
  - [x] **K5** red kapısı → [ADR-0038](docs/adr/0038-red-kapisi-esigi-kati.md) **katı**; aşırı-red ölçüldü
- [x] ⭐ **S3a ön-prob** — hibrit `recall@10` **0,875** · bedesten **GEÇERLİ** → research_log #49
- [x] **Adım 0** — modül-başına normalleştirme → 🔴 **REDDEDİLDİ**, kütle ≤ %56,2 < %71,6,
      hakem **$0** ([ADR-0053](docs/adr/0053-modul-basina-norm-kapsami-reddedildi.md) · #50)
- [x] **Adım 1** — retriever: `scripts/retriever.py` + indeks (40.496 madde) · `recall@10` **0,8750**
- [x] **Adım 2** — atıf doğrulayıcı: `scripts/atif_dogrula.py`, deterministik, **hakemsiz**
- [x] **Adım 3** — red kapısı: `scripts/red_kapisi.py`, ADR-0038 katı + 2 ablasyon
- [x] **Adım 4** — ⭐ **harness AÇIK ölçüm KOŞULDU** → kütle **%71,6 → ~~%58,7~~ %56,9**,
      ⭐ altın getirilince A1 **~~0,934~~ 0,923 > 0,909**, uydurulmuş atıf **0/89** → research_log #51
- [x] **S1** — `k` süpürmesi (B3): **`k=10` KABUL**, kütle **%56,9 → %59,5**; bedeli ölçüldü
      (altın getirilende A1 0,923 → 0,843) · 🚨 **tuzak 2.16** bulundu, 8 belge düzeltildi → #54
- [x] **S3** — ayırt-edicilik etiketi (B2): **62/18**, `recall@5` **0,8226 ↔ 0,5000**;
      ⭐⭐ ters çekinme kalibrasyonu bulundu → #53
- [x] **S2 keşif** — korpusun **%22,7'si yinelenen anahtar**; mülga aday kuralı doğrulandı → #52
- [x] **S2 kodlama** — `mulga`+ilga alanı **2.547 satır**, alt-madde kimliği **485 satır**,
      doğrulayıcıya **`MULGA`** hükmü, indeks yeni dizine kuruldu → **B7 kapandı**;
      kütle **%59,5 → %61,3**, A1 **+3,6 puan** → #52 + #55
      ⚠️ tablo-parçası eleme **kasten yapılmadı**: sınıf A modele **0/800** ulaşıyor
      → ölçülemez kazanç için ölçülmüş sayı harcanmaz (**borç B9**)
- [x] **S4** — isabet denetimi tasarımı (B1): [ADR-0055](docs/adr/0055-isabet-denetimi-ekseni.md),
      eksen = **kaynak-yeterliliği (cevap ÖNCESİ)**; cevap↔kaynak örtüşmesi **reddedildi**
      (B1'in çekirdek vakasında kör, sınıfı zaten boş) · **kod kasten açılmadı**

### 📌 Part 1'in bıraktığı — Part 2'nin girdisi

- **6 açık borç:** B10 (aşırı-red 16/80) · B1 (7/80) · B4 · B5 · B8 · B9 · B6
- **2 ölçüm boşluğu:** `m2b` harness AÇIK **hiç koşulmadı** · rakip harness AÇIK **hiç ölçülmedi**

Sıra ve ölçüm bağlamları: [`sprint3-part1.md`](docs/_arsiv/sprint3-part1.md#post-sprint-3-sırası) ·
Part 2'nin kararları ve ön-kayıtlı tahminleri: [ADR-0056](docs/adr/0056-m2b-harness-acik-protokolu-ve-0055-cipasi.md)

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
- [ ] 🚨 **v2.0 için YENİ donmuş set üret — S4'ten ÖNCE.** Sonra üretilirse yetişmez:
      o noktada TEST zaten harcanmış olur. CANON protokolü belgeli, ~$1 + yarım gün

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
