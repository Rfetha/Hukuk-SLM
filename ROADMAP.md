# Yol haritası — ölçülmüş açıklardan işlere

> **Hedef:** daha iyi model. Önce Gemini 3.1 Flash-Lite'ı geçmek, sonra Flash ve
> Pro'ya yetişmek. Bu belge o hedefi **ölçülmüş açıklara** bağlar — his değil, sayı.
>
> Yöntem disiplini (sabit seed, kayıtlı koşu, ön-kayıtlı kapı) **korunuyor**, ama
> gerekçesi değişti: artık bir hakemi ikna etmek için değil, **kendimizi
> kandırmamak** için.

## Şu anki açık

DEV, **harness kapalı**, hakem `gpt-4o-mini` (protokol: [MODEL_CARD](MODEL_CARD.md))

> ⚠️ **Bu tablo rakiple kıyas içindir ve harness KAPALI.** Harness AÇIK ürün sayısı
> 2026-08-04'te ilk kez ölçüldü: **sadık-cevap kütlesi %58,7** (kapalıda %71,6) — düşüşün
> tamamı erişimden. ⭐ Ama retriever altın maddeyi bulduğunda **A1 0,934 > 0,909**, yani
> **darboğaz model değil erişim**. Rakip harness açıkken **hâlâ ölçülmedi**.
> [research_log #51](docs/record/research_log/2026-08-04-harness-acik-ilk-olcum.md) ·
> [`sprint3.md`](sprint3.md)

```
                  BİZ 4B   Gemini FL    açık
M1 sadık-cevap    71,6%     72,9%     ~kapandı  ✅
M2 Rej            0,893     0,930      −0,037
A1                0,909     0,956      −0,047
M2b Rej           0,877     1,000      −0,123   ← EN BÜYÜK
```

⚠️ **Bu sayılar bir elimiz bağlıyken alındı.** Harness (erişim + atıf doğrulama +
red kapısı) hiç açılmadı — tez döneminde iç ablasyonun gereğiydi, artık değil.
**Gerçek ürün sayımızı henüz hiç görmedik.**

---

## 1. Harness — en büyük kazanç burada  ✅ **SEÇİLDİ (2026-08-03)** → [`sprint3.md`](sprint3.md)

| bileşen | hangi açığı kapatır | nasıl |
| :--- | :--- | :--- |
| **atıf doğrulayıcı** | A1 0,909 → ~1,0 | uydurulmuş madde numarası **deterministik** yakalanır; hakem gerekmez |
| **red kapısı** | **M2b 0,877 → ~1,0** | doğrulanamayan atıf varsa cevap reddedilir — **kod, model değil** |
| **retriever** | M1 · M4 | gerçek kullanımda maddeyi kimse vermiyor; şu an eval veriyor |

⭐ **Ve kategorik bir üstünlük:** canlı mevzuat API'si (`bedesten.adalet.gov.tr`,
çalışıyor, [`docs/BEDESTEN_API.md`](docs/BEDESTEN_API.md)). Harness'lı bir model
**bugünün mevzuatını** cevaplar. Kapalı ağırlıklı rakipler cevaplayamaz — bu bir
eksende ilerleme değil, farklı bir kategori.

Ayrıntılı faz tarifi: [`docs/VISION.md`](docs/VISION.md) Faz 2.

## 2. Model — ölçülmüş, ucuz düzeltmeler  *(2.1 harness'tan ÖNCE, gerisi sonra)*

| # | açık | kanıt | bedel |
| :-: | :--- | :--- | :--- |
| 2.1 | **merge `τ_a`'yı seyreltiyor** | M2b 0,987 (tekil) → 0,877 (merge) | modül-başına norm · **$0** · ~1 saat |
| 2.2 | **`τ_a` şablon ezberledi** | M1 medyan cevabı **58 karakter** = şablonun kendisi; model cümleyi çekimliyor | [ADR-0051](docs/adr/0051-m2b-cift-kalibi-ve-chosen-uretimi.md) B planı · ~$2 |
| 2.3 | **muhakeme izi İngilizce** | 8/8 ölçüldü ([`kollar.md`](docs/record/kollar.md) #4) | veri turu |
| 2.4 | veri inceliği | 728 temiz negatif | hasat hattı kurulu, ucuz |

**2.1 her hâlükârda yapılmalı** — bedava ve merge'in bilinen kusurunu kapatıyor.
**2.3 vatandaş kararıyla öne çıktı:** Türkçe düşünmeyen bir model, vatandaşa
"okunabilir muhakeme" veremez.

## 3. Boyut — kısıt kalktı

Tez tek boyut noktasına kilitliyordu ([ADR-0028](docs/adr/gemma4-12b-dersler.md)).
**O kısıt yok.** 8B/12B çıkabilir, birden çok boyut yayımlanabilir.

Ama önce 4B'yi tavana yaklaştırmak daha verimli: reçete büyük modele taşınır,
tersi taşınmaz.

## 4. Ürün katmanı

- **Vatandaş kipi** — sadeleştirme **istem katmanında**, eğitim hedefi değil.
  ⚠️ Sade dille *eğitmek* denendi ve **doğruluğu düşürdü** ([ADR-0010](docs/adr/gemma4-12b-dersler.md#adr-0010)).
  Ders: *sadelik, doğru cevabın sunum katmanıdır.*
- Model kartı ve sürüm akışı (`v0.1` → `v1.0`, kabul testiyle)

## 5. Korpus yürürlüğü — ve graph-RAG'in yeri *(2026-08-04'te ölçüldü)*

🚨 **Önce veri, sonra graf.** Ölçüldü: `"İŞ KANUNU Madde 15"` atfı doğrulamayı ve **katı
kapıyı geçiyor**, oysa o madde **mülga** (*"110- (Mülga: 22/5/2003/4857/120 md.)"*).
Korpusta yürürlük alanı **yok** — 4 alan var, ilga bilgisi serbest metnin içinde. Aynı ad
iki kanuna ait olabiliyor (`İŞ KANUNU` = **4857** yürürlükte **ve** **1475** mülga).
*"Denetlenebilir"* vaadindeki en somut açık bu ([`sprint3.md`](sprint3.md) borç **B7**).

- **5.1 Yürürlük alanı** — `mulga` + ilga eden kanun/madde; doğrulayıcı mülga atıfı
  **ayrı hüküm** olarak işaretler. Veri işi, ucuz, tek başına B7'yi kapatır.
- **5.2 Graph-RAG** — kısıtı 2026-08-03'te **kalktı**, planı **yok**. Bugün ilk kez
  **ölçülmüş** gerekçe kazandı, ama beklenen yerde değil:

  | graf ne için | ölçüm ne diyor |
  | :--- | :--- |
  | erişim kalitesi | ❌ gerekmiyor — `recall@5` 0,750 → `@20` **0,925**, açığın çoğu **k** ile kapanıyor |
  | cevap kalitesi | ❌ gerekmiyor — altın getirildiğinde A1 zaten **0,934** |
  | belirsiz sorgu | ❌ çözmüyor — soruların ~%25'i konusunu hiç belirtmiyor |
  | **yürürlük · ilga · tadil · atıf zincirleri** | ✅ **düz vektör benzerliğinden okunamaz** |

  **Sıra:** B7 (veri) → B3 (k süpürmesi) → B1 (isabet denetimi) → **graf**. Graf, 5.1
  yapıldıktan sonra *atıf zincirleri ve çapraz referans* için hak eder; erişim darboğazını
  çözmek için değil. ⚠️ [`VISION.md`](docs/VISION.md) Faz 2'deki *"hukuk ilişkiseldir"*
  gerekçesi **varsayımdı**; ölçülmüş hâli bu tablodur.

#### Mimari fark — bugün kurulan katman ↔ graf

⚠️ Graph-RAG top-k'nın **yerine geçmez, üstüne biner**: önce aday maddeleri bulman gerekir,
bugün kurulan katman tam olarak odur. Graf'la başlamak, **ölçülmemiş bir tabanın** üstüne
katman koymak olurdu.

| eksen | **bu (hibrit düz erişim)** | **graph-RAG** |
| :--- | :--- | :--- |
| birim | 40.496 bağımsız madde chunk'ı | düğüm + **kenar** (atıf · ilga · tadil · hiyerarşi) |
| sorgu | tek atış top-k (BM25 + bge-m3, RRF) | top-k **+ komşuluk gezinme** (1-2 hop) |
| kurulum | 10 dk indeks · 83 MB | yapı çıkarımı + ontoloji + Neo4j/Memgraph · **haftalar** |
| sorgu maliyeti | **759 ms**, CPU, GPU'ya girmiyor | + graf sorgusu; LLM-indeksliyse **~3× çıkarım** (VISION Faz 2) |
| çözdüğü | *"konuya en yakın madde hangisi"* | *"buna bağlı / bunu değiştiren / buna atıf yapan madde hangisi"* |
| **çözmediği** | ilişki · yürürlük · zincir | **belirsiz sorgu** ve **konusal yakınlık** — onun için yine vektör gerekir |

#### ⛔ ÖN-KAYITLI TAHMİN — graf bugünkü kümede ne yapardı *(2026-08-04, koşulmadan yazıldı)*

Bu tahmin **sınanabilsin** diye kaydediliyor. Graf bir gün kurulursa, `core_hard.jsonl`
üzerinde beklenen sonuç:

| eksen | tahmin | gerekçe |
| :--- | :--- | :--- |
| `recall@k` | **+0 … +2 puan** → n=80'de **ölçülemez** | sorular **madde başına** üretildi, altın **tek** madde. Graf gezinmesi *"A → atıf yaptığı B"* gerektiren **çok-hop** soruda kazanır; kümede o tip soru neredeyse yok. ±2 soru = **%2,5**, zaten gürültü |
| A1 | **değişmez, hafif düşebilir** | altın getirildiğinde A1 zaten **0,934**; model ilişki çıkarımına ihtiyaç duymuyor. Graf daha çok komşu getirir → bağlam uzar → dikkat dağılır |
| *"altın gelmedi ama cevapladı"* (14/80) | **hiç değişmez** | o sorular konusunu söylemiyor; graf **sorulmamış** olanı bulamaz |
| B7 (mülga atıf) | **çözer** | ama `mulga` boolean alanı da çözüyor — **1/20 maliyetle** (§5.1) |

**Yani graf bugün koşulsaydı, muhtemelen ölçülemez bir iyileşme üretirdi** — bu repo'nun
disiplininde en kötü mühendislik türü: işe yarayıp yaramadığını söyleyemediğin iş.
Karşılaştır: **`k`'yı 5→10 yapmak bir bayrak** ve kütleyi %58,7 → **~%65**'e taşıması
bekleniyor ([`sprint3.md`](sprint3.md) S1, ön-kayıtlı).

#### Graf gerçekten nerede kazanır — üçü de bugün ÖLÇÜLEMİYOR

1. **Çok-hop sorular** — *"kira artışında geçici madde var mı?"* → TBK 344 **+** geçici madde.
   DEV kümemizde yok; ölçmek için **ayrı soru kümesi** gerekir.
2. **Yürürlük zincirleri** — B7'nin büyük hâli: hangi hüküm neyi ilga etti, hangi tadil
   sırası geçerli.
3. **İçtihat ↔ mevzuat bağı** — Yargıtay kararları maddelere bağlanınca. Faz 2'nin asıl
   vaadi; `bedesten` aynı backend'den içtihadı da veriyor ([`BEDESTEN_API.md`](docs/BEDESTEN_API.md)).

⚠️ **Sonuç:** graf, *"retriever'ı iyileştirme"* işi değil — **ayrı bir yetenek**. Kurulursa
**kendi soru kümesiyle** ölçülür; bugünkü kümede ölçmek onu haksız yere başarısız gösterir.

---

## Opsiyonel: iddia katmanı (arxiv)

*"Merge, karışık ve ardışık SFT'den daha iyi korur"* iddiasını kanıtlayan
karşılaştırma — [`sprint2b.md`](docs/_arsiv/sprint2b.md)'de tarifi hazır, **ertelendi**.

Artefaktlar (`τ_g`, `τ_a`, veri, protokol) bozulmuyor; arxiv'e karar verilirse
istenen zaman koşulur (~$19,64).

⚠️ **Ürün için gerekli değil.** *"Daha iyi mi"* sorusunu ölçüm zaten cevaplıyor;
o karşılaştırma *"neden daha iyi"* sorusunu cevaplıyor.

---

## 🎯 VİZYON — üç drop

```
🟦 A   model + harness → HF        kendi sistemine kuracak kişi
🟩 B   kurulabilir web uygulaması  kullanmak isteyen kişi
🟪 C   vatandaş platformu          vatandaş
```

Her biri bir sonrakinin basamağı. Tam tasarım ve elenen seçenekler:
[`docs/specs/2026-08-03-yol-haritasi-design.md`](docs/specs/2026-08-03-yol-haritasi-design.md)

```
S3a ön-prob → S3 harness → S4 model → 🟦 A → S5 servis → 🟩 B → S6+ → 🟪 C
                                                                    ↻ bakım
```

⚠️ **Takvim yok, çıkış ölçütü var.** Aralıklı ritimde süre tahmini yanlış çıkar ve yapay
baskı yaratır. Bağlayıcı olan **sıra** ve her halkanın **çıkış ölçütü**dür.

## ⭐ Bakım halkası — model eskimesi kriz değil

1-2 yılda base modeller değişir, `v1.0` geriler. **Ama biz bir model değil REÇETE ürettik:**

```
yeni base  →  τ_g ~$4,4  →  τ_a ~$1,3  →  merge $0  →  eval ~$1
              ────────────────────────────────────────────────
              TOPLAM ~$7 · ~1 gün
```

Veri sabit, hiperparametreler künyede, merge kuralı ADR-0052'de, eval hattı otomatik.
**Disiplinin asıl getirisi bu.**

**Tetikleyici takvim değil, olay:** belirgin daha iyi bir ~4B base · kendi eval'imizde gerileme ·
mevzuat değişti → ⚠️ **İNDEKSİ tazele, modeli DEĞİL** (güncellik harness'ın işi).

## Rakip çerçevesi — ölçüt, hedef değil

1-2 yılda Gemini Flash-Lite bugünkü Flash olur; *"FL'i geçmek"* koşan bir hedef. **Yapısal
üstünlüğümüz bundan etkilenmiyor:** güncellik (kapalı ağırlık bugünün mevzuatını bilemez) ve
mahremiyet (hukuki sorular kişiseldir). İkisi de zamanla **büyüyor**.

## ✅ SIRA KARARA BAĞLANDI (2026-08-03)

```
0.  modül-başına norm (2.1)   1 sa · $0    ← bedava, harness'tan bağımsız
1.  HARNESS                    asıl iş      → sprint3.md
2.  harness AÇIK ölçüm         gerçek ürün sayımız — hiç görülmedi
3.  τ_a v2 (2.2)               artık doğru girdi dağılımını bilerek
4.  Türkçe muhakeme (2.3)      veri turu
```

**Gerekçe:** üç açığımızdan ikisini (A1 · M2b) harness **deterministik kodla**
kapatıyor; eğitim ancak kısmen. Ayrıca retriever modelin gördüğü girdi dağılımını
değiştiriyor — önce eğitmek, yanlış dağılıma optimize etmek olurdu. Ve en önemlisi:
**retriever olmadan ortada ürün yok** — kullanıcının mevzuat metnini kendisi
yapıştırması gerekiyor.

## Sırayı belirleyen argüman — ve nasıl çözüldü

Gerçek retriever ~5 gürültülü parça verecek — yani **M2b'ye benzeyen** koşullar.
**En zayıf olduğumuz eksen, üretimde en çok kullanılacak eksen.**

Bu iki yöne birden çekiyordu: *"M2b'yi modelde düzelt"* ↔ *"M2b'yi red kapısı zaten
kodla kapatıyor"*. **Kod tarafı seçildi** — çünkü deterministik, çünkü eğitim onu
ancak kısmen kapatır, ve çünkü retriever olmadan ölçtüğümüz dağılım üretimdeki
dağılım değil. Model tarafı (2.2 · 2.3) **iptal olmadı**, harness'tan sonraya
alındı; o zaman modelin gerçekten hangi girdiyi gördüğünü bilerek eğitiriz.
