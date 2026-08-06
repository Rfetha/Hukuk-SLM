# Yol haritası — ölçülmüş açıklardan işlere

> **Hedef:** daha iyi model. Önce Gemini 3.1 Flash-Lite'ı geçmek, sonra Flash ve
> Pro'ya yetişmek. Bu belge o hedefi **ölçülmüş açıklara** bağlar — his değil, sayı.
>
> Yöntem disiplini (sabit seed, kayıtlı koşu, ön-kayıtlı kapı) **korunuyor**, ama
> gerekçesi değişti: artık bir hakemi ikna etmek için değil, **kendimizi
> kandırmamak** için.

## Şu anki açık

DEV, **harness kapalı**, hakem `gpt-4o-mini` (protokol: [MODEL_CARD](MODEL_CARD.md))

```
                  BİZ 4B   Gemini FL    açık
M1 sadık-cevap    71,6%     72,9%     ~kapandı  ✅
M2 Rej            0,893     0,930      −0,037
A1                0,909     0,956      −0,047
M2b Rej           0,877     1,000      −0,123   ← EN BÜYÜK
```

⚠️ **Bu tablo rakiple kıyas içindir ve harness KAPALI.** Rakip harness açıkken
**hâlâ ölçülmedi** — o kıyas bugün de yok.

### ⭐ Harness AÇIK — ürünün gerçek sayısı *(2026-08-05, [Part 1](docs/_arsiv/sprint3-part1.md) kapanışı)*

| eksen | KAPALI | AÇIK k=10 + onarılmış korpus ⭐ |
| :--- | ---: | ---: |
| `recall@10` | — *(altın **kurgu gereği** verilir)* | **0,8750** |
| coverage | 0,7875 | **0,7625** |
| A1 (cevaplanan-only) | 0,9087 | **0,8042** |
| A1 · altın getirilen | 0,9087 | **0,8616** |
| **KÜTLE** | **%71,6** | **%62,8** ← ürünün dürüst sayısı (önsözsüz ablasyon: %61,3) |
| uydurulmuş madde no | 0 | **0/118** |

`outputs/eval/s2-harness-k10-etiketli/` · [#51](docs/record/research_log/2026-08-04-harness-acik-ilk-olcum.md) ·
[#54](docs/record/research_log/2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md) ·
[#55](docs/record/research_log/2026-08-05-s2-yururluk-alani.md)

**⛔ %71,6 → %61,3 bir gerileme DEĞİL** — iki ölçüm aynı şeyi ölçmüyor. KAPALI'da altın madde
bağlama **kurgu gereği** konuyor; AÇIK'ta **bulunması gerekiyor**. KAPALI bir rakip değil,
**tavan**. 10,2 puanlık açık ayrıştırıldı: **≈5,1 puan erişim ıskası** (harness'ın — altın 10/80
soruda hiç gelmiyor) + **≈4,5 puan dikkat dağılması** (modelin — altın bağlamdayken bile
A1 0,909 → 0,862). Çekinme **iki tarafta da aynı** (0,787 ↔ 0,771) → aşırı-red harness'ın
suçu değil, **model özelliği**.

⚠️ İki şerh bu sütunla **kalıcı** yolculuk eder: (a) 80 DEV altın etiketinin **3'ü** sayı
görüldükten *sonra* düzeltildi (kör hakem + ön-kayıtlı istem + konum-yanlılığı kontrolü +
insan onayı; manşeti **yükseltmedi**), (b) hakemin **yeniden-koşum gürültü tabanı ~0,3 A1
puanı** ölçüldü — bundan küçük hiçbir fark yorumlanmaz.

---

## 1. Harness — ✅ **KURULDU ve ÖLÇÜLDÜ (2026-08-05)** → [`sprint3-part1.md`](docs/_arsiv/sprint3-part1.md)

🚨 **Bu bölümün 2026-08-03'te yazılan gerekçesi ölçümle sınandı ve yarısı düştü.** Aşağıdaki
tablo iddiayı ve **hükmü** yan yana tutuyor — çünkü sprintin gerekçesi buydu ve tutmadıysa
kayda o şekilde geçer.

| bileşen | 08-03'te iddia | **ölçülen hüküm (08-05)** |
| :--- | :--- | :--- |
| **atıf doğrulayıcı** | A1 0,909 → ~1,0 | ❌ **ÇÜRÜDÜ.** Uydurulmuş madde no **0/118** — yakalayacak sınıf **zaten boştu**. A1 açığı fabrikasyondan değil, altın gelmeyince *başka bir gerçek maddeden* cevaplamaktan geliyor (**7/80**, borç B1) |
| **red kapısı** | M2b 0,877 → ~1,0 | ❌ **ÇÜRÜDÜ (08-05, [#56](docs/record/research_log/2026-08-05-olcum-bosluklari.md)).** Eşleşmiş sınavda (`h2b@k=4`, 4 kaynak ↔ 4 kaynak) **0,840 < 0,877** — kapatmadı, **kötüleştirdi**. Kapı 2/80 reddetti; mekanizması ölçülmüş biçimde boş: `KANUN_YOK 0` ve **36/80 cevapta hiç atıf yok**. İddia *sınanmamış* değil, bu rejimde **ateşlenemez** |
| **retriever** | M1 · M4 | ✅ **KURULDU ve KAZANDIRDI.** `recall@10` **0,8750**, 759 ms/sorgu, CPU'da. Ama kendi bedelini de getirdi: bağlam uzadıkça sadakat düşüyor (**ölçüldü**, aşağı bak) |

⭐ **Sprintin asıl getirisi sayı değil, dört mekanizma:** `k` büyütmenin **ölçülmüş bedeli** ·
çekinmenin **yanlış sinyale** (konusal uyum, yeterlilik değil) kalibre olduğu · doğrulayıcının
fabrikasyonu değil **transkripsiyonu** yakaladığı · hakem gürültüsünün **tabanı**.

🆕 **08-05 ([#56](docs/record/research_log/2026-08-05-olcum-bosluklari.md)) beşinci mekanizmayı
ekledi ve o bir ÇARE:** *kaynak-yeterliliği önsözü* — sistem istemine tek satır
(*"cevaba başlamadan önce kaynak yetiyor mu söyle"*) kütleyi **%61,3 → %62,8** çıkardı ve
**çapraz tablonun dört hücresini birden** doğru yöne taşıdı (aşırı-red 16 → **14**,
isabetsizlik 7 → **5**). `recall@10` değişmedi — değişen tek şey **istem**.
⚠️ **Benimsenmedi:** ana protokolü değiştirir, dolayısıyla tüm çıpalar yeniden türetilir →
**kendi ADR'sini ister**. Ürünün sayısı bugün hâlâ **%61,3**.
⚠️ Ve bu, *"deterministik koddan sonra sıra eğitimde"* okumasını **inceltir**: kalan açığın
kökü modelde ama **istem katmanından kısmen tetiklenebiliyor** — yani yetenek **var, varsayılan
değil**.

⭐ **Ve kategorik bir üstünlük:** canlı mevzuat API'si (`bedesten.adalet.gov.tr`,
çalışıyor, [`docs/BEDESTEN_API.md`](docs/BEDESTEN_API.md)). Harness'lı bir model
**bugünün mevzuatını** cevaplar. Kapalı ağırlıklı rakipler cevaplayamaz — bu bir
eksende ilerleme değil, farklı bir kategori.

Ayrıntılı faz tarifi: [`docs/VISION.md`](docs/VISION.md) Faz 2.

## 2. Model — ölçülmüş, ucuz düzeltmeler  *(2.1 harness'tan ÖNCE, gerisi sonra)*

| # | açık | kanıt | bedel |
| :-: | :--- | :--- | :--- |
| ~~2.1~~ | ~~**merge `τ_a`'yı seyreltiyor** → modül-başına norm~~ | 🔴 **ÖLÇÜLDÜ ve REDDEDİLDİ 2026-08-04** — kütle ≤ **%56,2** < gereken %71,6 ([ADR-0053](docs/adr/0053-modul-basina-norm-kapsami-reddedildi.md) · [#50](docs/record/research_log/2026-08-04-modul-basina-norm.md)) | hakem **$0** |
| **2.1b** 🆕 | **`τ_a` seyrelmesi HÂLÂ AÇIK** (M2b 0,987 → 0,877) — ama çare merge'de değil | Norm *kapsamı* çürütüldü: kol profilleri **orantılı**. Kalan en olası yer **`τ_a`'nın eğitim genliği** (‖τ_a‖ = 1,18 · 82 adım @1e-5) | eğitim işi (borç **B4**) |
| **2.1c** 🚨 ⭐ | **AŞIRI-RED — altın madde bağlamdayken çekinme** | **16/80** ve **`k`'dan bağımsız** (14 → 15 → 16). Harness KAPALI'da da aynı: **17/80**. Retriever ne kadar iyileşirse iyileşsin **kapanmıyor** | eğitim işi (borç **B10**) |
| 2.2 | **`τ_a` şablon ezberledi** | M1 medyan cevabı **58 karakter** = şablonun kendisi; model cümleyi çekimliyor | [ADR-0051](docs/adr/0051-m2b-cift-kalibi-ve-chosen-uretimi.md) B planı · ~$2 |
| 2.3 | **muhakeme izi İngilizce** | 8/8 ölçüldü ([`kollar.md`](docs/record/kollar.md) #4) | veri turu |
| 2.4 | veri inceliği | 728 temiz negatif | hasat hattı kurulu, ucuz |

🚨 **2.1c model tarafının yeni birinci sırası — ve gerekçesi ölçülmüş.** Coverage kaybının
**büyük yarısı** burada, B1'in (7/80) **iki katı**. Model, elinde doğru madde varken
cevap vermiyor; bunu harness KAPALI'da da yapıyordu (**17/80**) → bir harness gerilemesi
değil, **modelin kendi özelliği**. Bugünkü modelle kütlenin tavanı **~%71,6**.

⚠️ 2.1c ile 2.1b **birleştirilmedi**: *"aşırı-red `τ_a` seyrelmesinden geliyor"* makul ama
**ölçülmemiş bir varsayım**; birleştirmek onu kayıtta sessizce gerçeğe çevirirdi.

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
*"Denetlenebilir"* vaadindeki en somut açık bu ([`sprint3-part1.md`](docs/_arsiv/sprint3-part1.md) borç **B7**).

- **5.1 Yürürlük alanı** — ✅ **YAPILDI 2026-08-05** ([#55](docs/record/research_log/2026-08-05-s2-yururluk-alani.md)):
  `mulga` + `ilga_eden_kanun/madde/tarih` **2.547 satıra**, alt-madde kimliği **485 satıra**,
  doğrulayıcıya **`MULGA`** hükmü. `"İş Kanunu Madde 15"` artık üç red politikasında da
  **reddediliyor** → **B7 kapandı**. ⚠️ **Dürüst negatif:** bu DEV kümesinde `MULGA` **0 kez**
  tetiklendi — bir **ürün-güvenliği** özelliği, skor özelliği değil. Skor kazancı (+3,6 A1 puanı)
  aynı turun **alt-madde kimliği** kısmından, yani **erişim** kanalından geldi.
- **5.2 Graph-RAG** — kısıtı 2026-08-03'te **kalktı**, planı **yok**. Ölçülmüş gerekçesi var,
  ama beklenen yerde değil:

  | graf ne için | ölçüm ne diyor |
  | :--- | :--- |
  | erişim kalitesi | ❌ gerekmiyor — `recall@5` 0,750 → `@20` **0,925**, açığın çoğu **k** ile kapanıyor |
  | cevap kalitesi | ❌ gerekmiyor — altın getirildiğinde A1 zaten **0,862** *(k=10; k=5'te 0,923)* |
  | belirsiz sorgu | ❌ çözmüyor — soruların ~%25'i (ölçüldü: **18/80**) konusunu hiç belirtmiyor |
  | **yürürlük · ilga · tadil · atıf zincirleri** | ✅ **düz vektör benzerliğinden okunamaz** — ama 5.1 bunun **ucuz** kısmını **bir veri alanıyla** çözdü |

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
| A1 | **değişmez, hafif düşebilir** | altın getirildiğinde A1 zaten ~~0,934~~ **0,9230** (tuzak 2.16 düzeltmesi); model ilişki çıkarımına ihtiyaç duymuyor. Graf daha çok komşu getirir → bağlam uzar → dikkat dağılır |
| *"altın gelmedi ama cevapladı"* (14/80) | **hiç değişmez** | o sorular konusunu söylemiyor; graf **sorulmamış** olanı bulamaz |
| B7 (mülga atıf) | **çözer** | ama `mulga` boolean alanı da çözüyor — **1/20 maliyetle** (§5.1) |

⭐ **2026-08-05 — tahminin A1 satırındaki mekanizma bağımsız olarak ölçüldü.** *"Bağlam uzar →
dikkat dağılır"* dün bir **varsayımdı**. `k`'yı 5→10 yapmak tam olarak bunu yaptı ve altın
madde bağlamdayken A1 **0,9230 → 0,8426** düştü (#54, S1). Yani graf'ın en büyük riski artık
spekülasyon değil **bu repoda ölçülmüş bir sayı** — ve graf bağlamı k=10'dan **çok daha
fazla** uzatır. Buna karşılık *"14/80 hiç değişmez"* satırı **fazla karamsar** çıktı: o sınıf
salt `k` ile **7/80**'e indi, yani içinde erişimle kurtarılabilir bir pay varmış. Tahminin
ikisi de kayda geçiyor — tutan da, ıskalayan da.

**Yani graf bugün koşulsaydı, muhtemelen ölçülemez bir iyileşme üretirdi** — bu repo'nun
disiplininde en kötü mühendislik türü: işe yarayıp yaramadığını söyleyemediğin iş.
Karşılaştır: **`k`'yı 5→10 yapmak bir bayrak** — ön-kayıtlı tahmin kütleyi ~%65'e taşımaktı;
**ölçüldü 2026-08-05: %56,9 → %59,5** (erişim tahmini birebir tuttu, A1 tahmini 9 puan
ıskaladı; fark **dikkat dağılması**) ([`sprint3-part1.md`](docs/_arsiv/sprint3-part1.md) S1 · #54).

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
[`docs/superpowers/specs/2026-08-03-yol-haritasi-design.md`](docs/superpowers/specs/2026-08-03-yol-haritasi-design.md)

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

## ✅ SIRA KARARA BAĞLANDI (2026-08-03) — **ilk üçü bitti (2026-08-05)**

```
0.  modül-başına norm (2.1)   ✅ koşuldu → 🔴 REDDEDİLDİ (ADR-0053)
1.  HARNESS                   ✅ KURULDU  → sprint3-part1.md
2.  harness AÇIK ölçüm        ✅ ÖLÇÜLDÜ  → %62,8 (ürünün dürüst sayısı; önsözsüz ablasyon: %61,3)
3.  τ_a v2 (2.2)              ▶ sırada    — ve gerekçesi artık ölçülmüş: B10 (16/80)
4.  Türkçe muhakeme (2.3)     veri turu
```

⚠️ **Sıranın gerekçesi ölçümle DEĞİŞTİ.** 08-03'te 3. sıranın gerekçesi *"artık doğru girdi
dağılımını bilerek"* idi — yani bir **bilgi** gerekçesi. Bugün ona bir **büyüklük** gerekçesi
eklendi: aşırı-red **16/80** ve harness'la kapanmıyor. Sıra aynı kaldı, ama artık *"sonra da
yaparız"* değil **kütlenin büyük yarısı orada.**

**Part 2'nin kararları verildi ve kayda geçti:** [ADR-0056](docs/adr/0056-m2b-harness-acik-protokolu-ve-0055-cipasi.md) — `m2b` harness-AÇIK protokolü (altın ablasyonu), iki-sayı raporlaması, ön-kayıtlı tahminler, ADR-0055'in çıpa düzeltmesi. **Uygulama planı** `docs/superpowers/plans/` altına ayrıca yazılır.

**Gerekçe (2026-08-03):** üç açığımızdan ikisini (A1 · M2b) harness **deterministik kodla**
kapatıyor; eğitim ancak kısmen. Ayrıca retriever modelin gördüğü girdi dağılımını
değiştiriyor — önce eğitmek, yanlış dağılıma optimize etmek olurdu. Ve en önemlisi:
**retriever olmadan ortada ürün yok** — kullanıcının mevzuat metnini kendisi
yapıştırması gerekiyor.

> 🚨 **2026-08-05 — bu gerekçenin üç ayağı ölçüldü, ikisi düştü, biri ayakta:**
>
> | ayak | hüküm |
> | :--- | :--- |
> | *"A1'i kod kapatır"* | ❌ **ÇÜRÜDÜ** — uydurulmuş madde no **0/118**, doğrulayıcının yakalayacağı sınıf **boştu** |
> | *"M2b'yi kod kapatır"* | ❌ **ÇÜRÜDÜ (08-05)** — eşleşmiş sınavda **0,840 < 0,877**; kapı ateşlenemiyor ([#56](docs/record/research_log/2026-08-05-olcum-bosluklari.md)) |
> | *"retriever olmadan ürün yok"* | ✅ **AYAKTA ve ölçüldü** — `recall@10` 0,8750, ürünün ilk gerçek sayısı çıktı |
>
> 🚨 **08-05 itibarıyla iddianın İKİ ayağı da çürüdü, üçüncüsü ayakta.** Yani harness'ın
> gerekçesi artık *"iki açığı deterministik kodla kapatır"* değil, yalnız *"onsuz ürün yok"*.
>
> ⭐ **Sprint yine de doğru seçimdi, ama bildiğimiz sebepten değil.** Değerini *"iki açığı
> kapatmasından"* değil, **hangi açıkların gerçek olduğunu ölçmesinden** aldı: A1 açığının
> fabrikasyon olmadığını, asıl büyük kaybın **aşırı-red** olduğunu ve `k` büyütmenin bir
> **bedeli** olduğunu ancak harness açılınca öğrendik. Yanlış gerekçeyle alınmış doğru karar,
> kayda **öyle** geçer.

## Sırayı belirleyen argüman — ve nasıl çözüldü

Gerçek retriever ~5 gürültülü parça verecek — yani **M2b'ye benzeyen** koşullar.
**En zayıf olduğumuz eksen, üretimde en çok kullanılacak eksen.**

Bu iki yöne birden çekiyordu: *"M2b'yi modelde düzelt"* ↔ *"M2b'yi red kapısı zaten
kodla kapatıyor"*. **Kod tarafı seçildi** — çünkü deterministik, çünkü eğitim onu
ancak kısmen kapatır, ve çünkü retriever olmadan ölçtüğümüz dağılım üretimdeki
dağılım değil. Model tarafı (2.2 · 2.3) **iptal olmadı**, harness'tan sonraya
alındı; o zaman modelin gerçekten hangi girdiyi gördüğünü bilerek eğitiriz.
