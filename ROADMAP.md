# Yol haritası — ölçülmüş açıklardan işlere

> **Çerçeve (2026-09-06) — tez değil ÜRÜN.** **v1 = pratik olarak çalışan fine-tuned model
> release'i** (ağırlık + kod + veri + araştırma kaydı) · **v2 = aynı modelin API'si** ·
> **arxiv yan ürün, hedef değil.** Sıralı faz planı, kabul ölçütleri ve elenen seçenekler:
> [`docs/superpowers/specs/2026-09-06-v1-v2-roadmap-taslak.md`](docs/superpowers/specs/2026-09-06-v1-v2-roadmap-taslak.md)
> *(taslak — insan onayı bekliyor; eşikleri ADR-0050 gereği insan koyar)*.
>
> **Hedef:** daha iyi model. ~~Önce Gemini 3.1 Flash-Lite'ı geçmek, sonra Flash ve Pro'ya
> yetişmek.~~ 🚨 **BU CÜMLE BAYAT — ölçüldü 2026-08-06** (borç **YB5**): ürün rejiminde
> (harness AÇIK, ADR-0057 *eşit sınav*) **3.1 FL geçildi** — kütlede **+1,0 puan**, gürültü
> tabanının 3,4 katı ama **dar** — ve **3.5 FL bizi 6,7 puan geçiyor** (22 katı, **sağlam**).
> Kaynak: [`outputs/eval/g2-fl-harness/OZET.md`](outputs/eval/g2-fl-harness/OZET.md).
> **Güncel hedef cümlesi:** *3.5 Flash-Lite'ın kütlesine yetişmek — ve bunu **aşırı-reddi (B10)**
> kapatarak yapmak, çünkü açığın ölçülmüş kanalı orası (aşırı-red bizde rakibin ~2 katı).*
> ⛔ *"Aşırı-red kapansa %72,0'a çıkardık"* cümlesi **TAVAN/VARSAYIMSAL** damgalıdır; rakip
> kıyası ondan **kurulmaz**.
>
> Bu belge hedefi **ölçülmüş açıklara** bağlar — his değil, sayı.
>
> Yöntem disiplini (sabit seed, kayıtlı koşu, ön-kayıtlı kapı) **korunuyor**, ama
> gerekçesi değişti: artık bir hakemi ikna etmek için değil, **kendimizi
> kandırmamak** için.

## Şu anki açık

DEV, **harness kapalı**, hakem `gpt-4o-mini` (protokol: [MODEL_CARD](MODEL_CARD.md))

```
                  BİZ 4B   Gemini FL    açık
M1 sadık-cevap    71,6%     72,9%     ~kapandı  ✅
M2 Rej            0,833     0,848      −0,015   ⚠️ TEK KALEM — aşağıya bak  (ᴷ⁴; eski 0,893 ↔ 0,930)
A1                0,909     0,956      −0,047
M2b Rej           0,766     0,883      −0,117   ← EN BÜYÜK   (ᴷ³ yeniden puanlandı)
```

> ᴷ³ **M2b sütunu 2026-08-06'da yeniden puanlandı** ([#57](docs/record/research_log/2026-08-06-cekinme-aleti-onarimi.md)): eski payda hakemin **modelin
> cevabına bakarak** verdiği bir karardı, aynı sınav her modelde farklı payda veriyordu. Eski
> değerler `0,877 ↔ 1,000`. **İşaret ve sıralama değişmedi**, açıklık 12,3 → 11,7 puana daraldı.
>
> ᴷ⁴ **`M2 Rej` satırı da 2026-08-06'da yeniden puanlandı** (KARAR-3, ≈$0,11 · 10 koşu ·
> payda 55-63'ten **66/70**'e eşitlendi). ⚠️ **Bu düzeltme BİZİM LEHİMİZE ve öyle raporlanıyor:**
> en çok kayan özne **RAKİP** (Gemini −8,2 puan · biz −6,0), açıklık **3,7 → 1,5 puana daralıyor**.
> Kirli paydadan en çok Gemini yararlanıyordu. Kaynak:
> [`outputs/eval/karar3-m2-payda/`](outputs/eval/karar3-m2-payda/m2_payda_2026-08-06.json).
>
> ⚠️ **KUANTUM ŞERHİ — `M2 Rej`'deki `−0,015` TEK BİR KALEMDİR.** Payda eşitlenince (66) M2'nin
> kuantumu `1/66 = **1,52 puan**` oldu: `tgta_v1` **55/66** çekiniyor, Gemini **56/66**.
> Yani fark, aletin ifade edebileceği **en küçük sıfırdan farklı** değer — bir hakem yargısının
> dönmesi. Düzeltme öncesi açıklık ~2,4 kalemdi. **Sonuç değil, çözünürlük sınırı olarak okunur:**
> `τ_a` v2 bir kalem kazanırsa *"Gemini ile M2'de eşitlendik"* cümlesi **kurulmaz**.
> ⛔ Global kısıttaki **`0,3 A1 puanı`** gürültü tabanı bu ekseni **KORUMAZ** (A1 makrosu için
> yazılmıştır). Yerine yeni bir taban **uydurulmadı** — ikili oran ekseninde çözünürlük sınırı
> koymak **insan kararıdır** ve borç olarak [`docs/open_questions.md`](docs/open_questions.md)'ye
> düşüldü. Aynı şerh [`MODEL_CARD.md`](MODEL_CARD.md) *"How to read this honestly"* bölümünde.
> ⚠️ `A1` satırı **hâlâ yeniden puanlanmadı** (`valid_trap`ten etkilenmiyor; ayrı eksen).

⚠️ **Bu tablo rakiple kıyas içindir ve harness KAPALI — ÜRÜNÜN SAYISI DEĞİL.**
~~Rakip harness açıkken **hâlâ ölçülmedi** — o kıyas bugün de yok.~~
🆕 **2026-08-06'da ölçüldü** → aşağıdaki *ürün rejimi* tablosu. Eski cümle silinmedi: o gün
bilinen durum buydu.

### 🚨 Rakip — ÜRÜN REJİMİ (harness AÇIK, ADR-0057 "eşit sınav") *(2026-08-06, projede İLK KEZ)*

⭐ **Rakip kıyası BU tablodan kurulur**, yukarıdaki KAPALI tablodan değil.
Kaynak: [`outputs/eval/g2-fl-harness/OZET.md`](outputs/eval/g2-fl-harness/OZET.md) — eşit sınav
**varsayılmadı, ölçüldü**: `recall@10` üç öznede de birebir **0,875**.

| eksen | **BİZ** | 3.1 FL | **3.5 FL** |
| :--- | ---: | ---: | ---: |
| **M1 kütle (AÇIK)** | **%68,4** ~~%62,8~~ | %61,7 | **%69,5** |
| A1 · cevaplanan | **0,8288** | 0,7054 | 0,7940 |
| A1 · altın getirilen | **0,8729** | 0,7835 | 0,8607 |
| **aşırı-red** (↓ iyi) | **%17,50** ~~%23,75~~ | %12,5 | %12,5 |
| altın bağlamda ama sustu | **9/80** ~~14/80~~ *(gözle okuma 8/80)* | 8/80 | **6/80** |
| M2b Rej\* (önsözlü, k=4) | 0,809 | 0,809 | **0,926** |
| $/cevap (girdi+çıktı) | **$0** (yerel) | $0,002074 | $0,002175 |

**Okuma: sadakatte birinciyiz, çekinmede hâlâ gerideyiz — ama açıklık 2026-09-06'da daraldı.**
A1'in her iki kademesinde de iki rakibi de geçiyoruz; kütleyi kaybettiren şey **cevaplamamak**.
🔁 ~~*"rakibin iki katı gerideyiz"*~~ — dedektör onarımından sonra **9/80 ↔ 8/80 ↔ 6/80**
yani **aletle 3.1 FL'ın bir kalem gerisinde**, gözle okumayla (8/80) **başa baş**;
3.5 FL'ın iki-üç kalem gerisindeyiz
([#61](docs/record/research_log/2026-09-06-dedektor-onarimi-b10-yeniden.md)).
⚠️ Ve kütle satırındaki kazanç **modelden değil aletten** geldi: 3.5 FL açığı ~~−6,7~~ →
**−1,1 puan**. ⛔ *"3.5 FL ile eşitlendik"* cümlesi **kurulmuyor** — o 1,1 puanı koruyan bir
çözünürlük sınırı yok (0,3 tabanı A1 makrosu içindir; kütle = coverage × A1 ve coverage'ın
varyansı o tabanda yok, `OZET.md` §164).
⚠️ M2b satırında 3.5 FL'ın **%10,0 kesikliği** var (bizde ve 3.1 FL'de 0/80); ortak kesiksiz
alt kümede (n=60) açıklık **daralmıyor, genişliyor** → hüküm sağlam ama kesiklik yazılmadan
kurulamaz (OZET.md, tuzak 1.9).

### ⭐ Harness AÇIK — ürünün gerçek sayısı *(2026-08-05, [Part 1](docs/_arsiv/sprint3-part1.md) kapanışı)*

| eksen | KAPALI | AÇIK k=10 + onarılmış korpus + yeterlilik önsözü ⭐ |
| :--- | ---: | ---: |
| `recall@10` | — *(altın **kurgu gereği** verilir)* | **0,8750** |
| coverage | 0,7875 | **0,8250** ~~0,7625~~ |
| A1 (cevaplanan-only) | 0,9087 | **0,8288** (önsözsüz ablasyon: **0,8110**) |
| A1 · altın getirilen | 0,9087 | **0,8729** (önsözsüz ablasyon: **0,8593**) |
| **KÜTLE** | **%71,6** | **%68,4** ~~%62,8~~ ← ürünün dürüst sayısı (önsözsüz ablasyon: **%73,0** ~~%61,3~~ 🚨 artık **daha yüksek**) |
| uydurulmuş madde no | 0 | **0/83** (önsözsüz ablasyon: 0/118) |

**Ana protokol koşusu (RESMÎ, önsözlü):** `outputs/eval/olcum-bi/` ·
[#56](docs/record/research_log/2026-08-05-olcum-bosluklari.md) §5 (D1) ·
[ADR-0058](docs/adr/0058-b-i-kaynak-yeterliligi-onsozu-benimsendi.md)
**Önsözsüz ablasyon koşusu:** `outputs/eval/s2-harness-k10-etiketli/` ·
[#51](docs/record/research_log/2026-08-04-harness-acik-ilk-olcum.md) ·
[#54](docs/record/research_log/2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md) ·
[#55](docs/record/research_log/2026-08-05-s2-yururluk-alani.md)

**⛔ %71,6 → %61,3 bir gerileme DEĞİL** — ⚠️ *bu paragrafın tamamı ve ayrıştırması **önsözsüz**
çıpayla (%61,3) yapılmıştır; ADR-0058 sonrası ana protokolde açık **8,8 puandır** ve yeniden
ayrıştırılmamıştır.* İki ölçüm aynı şeyi ölçmüyor. KAPALI'da altın madde
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
| **atıf doğrulayıcı** | A1 0,909 → ~1,0 | ❌ **ÇÜRÜDÜ.** Uydurulmuş madde no **0/83** (önsözsüz ablasyon: 0/118) — yakalayacak sınıf **zaten boştu**. A1 açığı fabrikasyondan değil, altın gelmeyince *başka bir gerçek maddeden* cevaplamaktan geliyor (**5/80** — önsözsüz ablasyon: 7/80, borç B1) |
| **red kapısı** | M2b 0,766 ᴷ³ → ~1,0 | ❌ **ÇÜRÜDÜ (08-05, [#56](docs/record/research_log/2026-08-05-olcum-bosluklari.md)).** Eşleşmiş sınavda (`h2b@k=4`, 4 kaynak ↔ 4 kaynak) **0,735 < 0,766** ᴷ³ *(eski alet: 0,840 < 0,877 — işaret aynı)* — kapatmadı, **kötüleştirdi**. Kapı 2/80 reddetti; mekanizması ölçülmüş biçimde boş: `KANUN_YOK 0` ve **36/80 cevapta hiç atıf yok**. İddia *sınanmamış* değil, bu rejimde **ateşlenemez** |
| **retriever** | M1 · M4 | ✅ **KURULDU ve KAZANDIRDI.** `recall@10` **0,8750**, 759 ms/sorgu, CPU'da. Ama kendi bedelini de getirdi: bağlam uzadıkça sadakat düşüyor (**ölçüldü**, aşağı bak) |

⭐ **Sprintin asıl getirisi sayı değil, dört mekanizma:** `k` büyütmenin **ölçülmüş bedeli** ·
çekinmenin **yanlış sinyale** (konusal uyum, yeterlilik değil) kalibre olduğu · doğrulayıcının
fabrikasyonu değil **transkripsiyonu** yakaladığı · hakem gürültüsünün **tabanı**.

🆕 **08-05 ([#56](docs/record/research_log/2026-08-05-olcum-bosluklari.md)) beşinci mekanizmayı
ekledi ve o bir ÇARE:** *kaynak-yeterliliği önsözü* — sistem istemine tek satır
(*"cevaba başlamadan önce kaynak yetiyor mu söyle"*) kütleyi ~~**%61,3 → %62,8**~~ çıkardı ve
**çapraz tablonun dört hücresini birden** doğru yöne taşıdı (aşırı-red 16 → **14**,
isabetsizlik 7 → **5**). `recall@10` değişmedi — değişen tek şey **istem**.
✅ **BENİMSENDİ** — ADR-0058 (2026-08-06): ana protokolü değiştirdi, dolayısıyla tüm çıpalar
yeniden türetildi. Ürünün resmî sayısı **%68,4**; önsözsüz koşu artık **ablasyon kolu**
(**%73,0**).
🚨 **2026-09-06 — bu paragrafın GEREKÇESİ tersine döndü.** Dedektör onarılınca önsözün etkisi
**+1,5 p → −4,6 p** oldu: önsözlü %68,4, önsözsüz **%73,0**. Kıyas eşleşmiş (aynı 80 id,
**80/80 birebir aynı bağlam**, aynı `recall@10`). Ama önsözün diğer ayakları ayakta: A1
**0,8288 ↔ 0,8110**, isabetsizlik **5/80 ↔ 7/80**. ⛔ **Protokol DEĞİŞTİRİLMEDİ** — kendi ADR'sini
ve insan kararını ister (açık soru **S14**).
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
| **2.1b** 🆕 | **`τ_a` seyrelmesi HÂLÂ AÇIK** (M2b 0,987 → 0,766 ᴷ³; `τ_a` sayısı yeniden puanlamada **değişmedi**) — ama çare merge'de değil | Norm *kapsamı* çürütüldü: kol profilleri **orantılı**. Kalan en olası yer **`τ_a`'nın eğitim genliği** (‖τ_a‖ = 1,18 · 82 adım @1e-5) | eğitim işi (borç **B4**) |
| ~~**2.1c**~~ | ~~**AŞIRI-RED — altın madde bağlamdayken çekinme**~~ | 🛑 **TUR KAPANDI 2026-09-06** — ~~14/80~~ → **8/80** (gözle okuma; alet 9/80). Sayının **%43'ü aletin kendisiydi**, eğitim yapılmadı ([ADR-0062](docs/adr/0062-b10-turu-kapatildi-hedef-egitimsiz-karsilandi.md) · [#61](docs/record/research_log/2026-09-06-dedektor-onarimi-b10-yeniden.md)). ⛔ **Sıfırlanmadı**, küçüldü: 8/80 hâlâ 3.5 FL'ın **6/80**'inin üstünde | borç **B10** — *birinci sıradan indi*, açık sınır olarak durur |
| 2.2 | **`τ_a` şablon ezberledi** | M1 medyan cevabı **58 karakter** = şablonun kendisi; model cümleyi çekimliyor | [ADR-0051](docs/adr/0051-m2b-cift-kalibi-ve-chosen-uretimi.md) B planı · ~$2 |
| 2.3 | **muhakeme izi İngilizce** | 8/8 ölçüldü ([`kollar.md`](docs/record/kollar.md) #4) | veri turu |
| 2.4 | veri inceliği | 728 temiz negatif | hasat hattı kurulu, ucuz |

🔁 ~~**2.1c model tarafının yeni birinci sırası**~~ — **bu okuma 2026-09-06'da ÇÜRÜDÜ.**
*"Coverage kaybının büyük yarısı burada, B1'in ≈2,8 katı (14 ↔ 5)"* deniyordu. Ölçüt onarılınca
oran **8 ↔ 5**'e indi: aşırı-red hâlâ daha büyük ama **"büyük yarısı"** değil. Eski cümle
damgalanarak duruyor, çünkü bu turun sırasını o belirlemişti.

🚨 **Model tarafının yeni birinci sırası: B1 (isabet denetimi, 5/80)** — *gerçek ama soruya
uymayan madde*. Gerekçe: B10 birinci sıradan indi ve B1 ile arasındaki açıklık **2,8× → 1,6×**'e
daraldı; ayrıca B1 hiç çalışılmadı (eksen ADR-0055'te belirlendi, kod açılmadı).

⚠️ 2.1c ile 2.1b **birleştirilmedi** ve birleştirilmiyor: *"aşırı-red `τ_a` seyrelmesinden
geliyor"* makul ama **ölçülmemiş bir varsayım**; birleştirmek onu kayıtta sessizce gerçeğe
çevirirdi. ⭐ Bu turda bunun **ikinci bir kanıtı** çıktı: `τ_a` v1'in kendi aşırı-reddi onarımda
**hiç kıpırdamadı** (0,5750 → 0,5750), yani iki eksen aynı şeyi ölçmüyor.

> ✅ **B10 turu 2026-09-06'da KAPANDI — hedef EĞİTİMSİZ karşılandı**
> ([ADR-0062](docs/adr/0062-b10-turu-kapatildi-hedef-egitimsiz-karsilandi.md)).
>
> Görev 3'ün pilotu koştu ve planın **gözle-okuma** adımı kabul ölçütünü çürüttü
> ([#60](docs/record/research_log/2026-09-06-hasat-kabul-olcutu-coktu.md)): hasat önsözsüz
> rejimde koşuyor, o dalda `exact_reject` cevabın tamamını tarıyor ve **elenen kaynakların
> gerekçesini** (*"…İÇERMEMEKTEDİR"*) red sanıyordu → gözle okunan **10 kabulün 6'sı tam,
> atıflı CEVAP**. Görev 4 koşsaydı havuzun çoğunluğu ORPO'ya *"doğru cevap verme"* diye
> girecekti — turun hedefinin tam tersi.
>
> Alet onarıldı ve **80 kalem gözle okundu**
> ([#61](docs/record/research_log/2026-09-06-dedektor-onarimi-b10-yeniden.md) ·
> [ADR-0061](docs/adr/0061-cekinme-dedektoru-istem-rejimi-bagimliligi.md)):
> **B10 14/80 → 8/80** · coverage 0,7625 → **0,8250** · kütle %62,8 → **%68,4** ·
> `recall@10` **değişmedi** (70/80). Eski aletin 14 B10'unun **6'sı yanlış pozitifti**,
> **yanlış negatif yoktu**.
>
> **Tur bu yüzden kapandı:** ön-kayıtlı band **8-11/80** idi, **8/80'deyiz ve hiç eğitim
> yapılmadı**. Ayrıca hasat verimi gerçekte **0,0667** (raporlanan 0,1733 sahteydi) → 250 çift
> **5,3 saat ≈ $5,2**, planın D10 (3 saat) sınırını aşıyor.
> ⛔ **Aşırı-red SIFIRLANMADI, küçüldü** — 8/80 hâlâ 3.5 FL'ın **6/80**'inin üstünde ve
> MODEL_CARD Limitations'ında **açık sınır** olarak duruyor.
> ⛔ *"Aşırı-red eğitimle ne kadar iner"* sorusu **ÖLÇÜLMEDİ.**

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
  | cevap kalitesi | ❌ gerekmiyor — altın getirildiğinde A1 zaten **0,8705** (önsözsüz ablasyon: 0,8616) *(k=10; k=5'te 0,923)* |
  | belirsiz sorgu | ❌ çözmüyor — soruların ~%25'i (ölçüldü: **18/80**) konusunu hiç belirtmiyor |
  | **yürürlük · ilga · tadil · atıf zincirleri** | ✅ **düz vektör benzerliğinden okunamaz** — ama 5.1 bunun **ucuz** kısmını **bir veri alanıyla** çözdü |

  ⚠️ ᴷ⁴ **B3'ün (`k` süpürmesi) ÇEKİNME bacağı TANIMSIZ** (2026-08-06, KARAR-4 m.2):
  *"`k` büyütmek çekinmeye de mal oluyor"* (`Rej` 0,840 → 0,784) bir **hüküm değil, borç** —
  kör payda hakemi `k=10`'da kaynakların **%57'sini**, `k=4`'te %100'ünü görüyor, payda
  ekseni eşleşmiyor ([ADR-0057](docs/adr/0057-harness-rekabet-kapisi-esit-sinav.md)).
  Sadakat bacağı (A1 0,923 → 0,843, #54) **etkilenmiyor**; `k` süpürmesinin gerekçesi
  bugün yalnız ona dayanır. Kapatan şey klip borcu (≈$0,30, `docs/open_questions.md`).

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

## Opsiyonel: iddia katmanı (arxiv) — **yan ürün, hedef değil**

*"Merge, karışık ve ardışık SFT'den daha iyi korur"* iddiasını kanıtlayan
karşılaştırma — [`sprint2b.md`](docs/_arsiv/sprint2b.md)'de tarifi hazır, **ertelendi**.

Artefaktlar (`τ_g`, `τ_a`, veri, protokol) bozulmuyor; ~~arxiv'e karar verilirse istenen zaman
koşulur (~$19,64).~~

> 🚨 **DÜZELTME 2026-08-06 — CP4-CP5 harcamasının YETKİSİ YOK.** ARA KAPI **düştü**: ön-kayıtlı
> olan **formüldü**, sayı değil → eşik `0,90 × base M2b 0,961 = **0,8649**`, merge **0,766** →
> **9,9 puan altında** (eski 0,887 eşiğine karşı da düşüyor; paydalar **eşit**, 77 ↔ 77).
> ⛔ ADR-0050 gereği **alet** düzeltildi, **eşiğe dokunulmadı**.
> [ADR-0045](docs/adr/0045-ara-kapi-merge-onarim-kontrolu.md) ·
> [#58](docs/record/research_log/2026-08-06-payda-tekillesmesi.md) ·
> `outputs/eval/cp2-r-kor-payda/ara_kapi_esikleri_2026-08-06.json`.
> **CP4-CP5'i yetkilendiren kapı buydu** — koşulmadan önce yeni bir ön-kayıtlı ölçüt gerekir
> (karar sorusu **S1**). ⚠️ ADR-0052'nin hükmü (*ham TIES ≫ norm-dengeli*) bundan
> **etkilenmedi**: sıçrama +0,26 değişmedi.
> ⚠️ İkinci açık kalem: ön-kayıtlı metin CP4'e *"karışık **SFT**"* diyor ama `τ_a` **ORPO** ile
> eğitildi.

Bugün savunulabilir iddialar, eksik ölçümler (**P1** CP4/CP5 tabanları · **P2** üç-aileli hakem
paneli + κ · **P3** frozen TEST + güç analizi) ve venue tartışması:
[`docs/PAPER_TARGET.md`](docs/PAPER_TARGET.md) ·
[v1/v2 taslağı §6](docs/superpowers/specs/2026-09-06-v1-v2-roadmap-taslak.md).

⚠️ **Ürün için gerekli değil.** *"Daha iyi mi"* sorusunu ölçüm zaten cevaplıyor;
o karşılaştırma *"neden daha iyi"* sorusunu cevaplıyor. P2/P3 ürün yolunda **koşulmaz**,
model kartında **Limitations satırı** olarak yazılır.

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

### 🆕 Drop'ların v1/v2 karşılığı *(2026-09-06 — atılmadı, EŞLEŞTİRİLDİ)*

Üç drop yürürlükte; değişen tek şey **adlandırma ve kabul ölçütü**. Faz numaraları
[v1/v2 taslağı §5](docs/superpowers/specs/2026-09-06-v1-v2-roadmap-taslak.md)'ten gelir.

| drop | sürüm | hangi fazlar | çıkış ölçütü |
| :--- | :--- | :--- | :--- |
| — | *(ön iş)* | **Faz 0** ucuz düzeltmeler (0.1-0.6) · **Faz 1** B10 turu | Faz 0 belge/alet borçları · Faz 1'in iki ön-kayıtlı kapısı |
| 🟦 **A** | **v1** — model release'i | **Faz 2** v1 hazırlığı → **Faz 3** v1 RELEASE | taslak §3.2 **A** kalite · **B** frozen TEST bir kez · **C** dağıtım · **D** yeniden üretilebilirlik · **E** belge/lisans |
| 🟩 **B** | **v2** — API + sunum | **Faz 4** (FastAPI · atıf paneli · Docker · B6 canlı mevzuat · B9 yeniden indeksleme) | temiz konteynerde yalnız belgeyle kurulum; ölçüm rejimi ↔ servis rejimi sapması **ölçülür** |
| 🟪 **C** | v2 sonrası | [`VISION.md`](docs/VISION.md) Faz 4-5 | ayrı tur |

🚨 **v1'in tanımı model-only DEĞİL** (taslak §3.1, ölçülmüş gerekçe): resmî sayı %62,8
**retriever + yeterlilik önsözü** rejiminde üretiliyor (ADR-0058); bugün modeli indiren ikisine
de sahip değil, dolayısıyla **ablasyon sayısını** (%61,3) alır. *Yayımlanan sayıyı kimsenin
üretemediği bir release, bu repo'nun kendi disiplininin ihlalidir.* Taşıyıcı: tek komutluk CLI
(`hakhukuk sor "..."` → retriever + önsöz + llama.cpp + atıf doğrulayıcı). Web arayüzü/API **v2**.
⛔ **A/B/C kabul ölçütleri karşılanmazsa `v0.2` çıkar, `v1.0` çıkmaz.**

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
2b. rakip ürün rejiminde      ✅ ÖLÇÜLDÜ 2026-08-06 → 3.1 FL geçildi (dar) · 3.5 FL 6,7 p önde
3.  τ_a v2 / B10 turu (2.2)   ✅ KAPANDI 2026-09-06 (ADR-0062) — hedef EĞİTİMSİZ karşılandı:
                                 B10 14/80 → 8/80, kütle %62,8 → %68,4. τ_a v2 EĞİTİLMEDİ
3b. Faz 0 ucuz düzeltmeler    ▶ SIRADA — README/MODEL_CARD çıpaları ✅, ölçülmüş VRAM satırı ✅,
                                 M3 paydası, künye script'i, ADR-0059
4.  B1 — isabet denetimi      ▶ **YENİ BİRİNCİ SIRA** (5/80) — gerçek ama soruya uymayan madde;
                                 eksen ADR-0055'te belirlendi, kod hiç açılmadı
5.  Türkçe muhakeme (2.3)     veri turu — ⚠️ önce **istem katmanında** bedavaya denenir
6.  v1 → v2                   Faz 2-3 (release) → Faz 4 (API)
```

⭐ **3. sıra kapandı ama beklenen sebeple değil.** Tur *"aşırı-redi eğitimle düşür"* diye
başladı; **eğitim hiç yapılmadan** hedefe ulaşıldı, çünkü sayının **%43'ü ölçüm aletinin
kendisiydi**. Sıra bu yüzden **B1'e** geçiyor: B10 ile arasındaki açıklık **2,8× → 1,6×**'e
daraldı ve B1 hiç çalışılmadı.

⚠️ **Bunu yakalayan sayısal kapı değildi** — `kabul_orani 0,1733 > 0,10` kapısı hatayı
**geçirdi**. Yakalayan, planın **gözle okuma** adımıydı (ADR-0051, ikinci kez kendini ödedi).

⚠️ **Sıranın gerekçesi ölçümle DEĞİŞTİ.** 08-03'te 3. sıranın gerekçesi *"artık doğru girdi
dağılımını bilerek"* idi — yani bir **bilgi** gerekçesi. Bugün ona bir **büyüklük** gerekçesi
eklendi: aşırı-red **14/80** (önsözsüz ablasyon: 16/80) ve harness'la kapanmıyor. Sıra aynı kaldı, ama artık *"sonra da
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
> | *"M2b'yi kod kapatır"* | ❌ **ÇÜRÜDÜ (08-05)** — eşleşmiş sınavda **0,735 < 0,766** ᴷ³ *(eski alet 0,840 < 0,877)*; kapı ateşlenemiyor ([#56](docs/record/research_log/2026-08-05-olcum-bosluklari.md)) |
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
