# #56 — Ölçüm boşlukları: m2b harness AÇIK · B5 · B8 · B-i

**Tarih:** 2026-08-05
**Plan:** [`superpowers/plans/2026-08-05-olcum-bosluklari.md`](../../superpowers/plans/2026-08-05-olcum-bosluklari.md)
**Kararlar:** [ADR-0057](../../adr/0057-harness-rekabet-kapisi-esit-sinav.md) *(eşit sınav kapısı)* ·
[ADR-0056](../../adr/0056-m2b-harness-acik-protokolu-ve-0055-cipasi.md) · [ADR-0055](../../adr/0055-isabet-denetimi-ekseni.md)

## Künye

```
model      models/gguf/tgta_v1-q4_k_m.gguf  (tgta_v1 = HakHukuk-4B-v0.1)
indeks     data/index/mevzuat_bge_m3_s2     korpus data/corpus/mevzuat_maddeler.jsonl (40.496)
rejim      thinking on · think-budget 1024 · max-new-tokens 512 · seed 3407
           max-chunk-chars 900 · CTX 8192 · KV q8_0/q8_0
hakem      openai/gpt-4o-mini · OpenRouter · sağlayıcı pinli (OpenAI)  — tuzak 2.7
koşular    outputs/eval/olcum-h2b-k4/ · olcum-h2b-k10/ · olcum-bi/
           (post-hoc: outputs/eval/s2-harness-k10-etiketli/)
maliyet    GPU $0 · hakem $0,0411 (Ö1) + $0,0339 (D1) = $0,075   bütçe ≤ $2
geçit      n=80 · kesik %3,8 · ALTIN_SIZAN=0 · kaynak={k} · üç koşuda da GEÇTİ
```

## 1. Ö1 — `m2b` harness AÇIK: **kapı KALDI**

Part 1'in iki gerekçesinden biri *"red kapısı M2b'yi kapatır"* idi ve **hiç sınanmamıştı**.
Sınandı.

```
kol                kaynak   Rej*   Rej_rgx  payda  geçersiz  kapı_red  atıfsız  zorluk
KAPALI m2b (çıpa)      4   0,877    0,846     65       15        -        -    1,0000
AÇIK  h2b k=4          4   0,840    0,820     50       30        2       36    0,4750  ← HÜKÜM
AÇIK  h2b k=10        10   0,784    0,706     51       29        4       34    0,4350    bilgi ⚠️TANIMSIZ
```

> ## 🚨 TANIMSIZ ᴷ⁴ — `k=10` SATIRININ PAYDASI (2026-08-06, KARAR-4 m.2)
> Kör payda hakemi kaynak metnini `SOURCE_CLIP = 3500` karakterle kırpılmış görüyor. Ölçüldü
> (`[KAYNAK` sayımı, n=80): **k=4 → 320/320 kaynağın %100'ü** · **k=10 → 454/800, yani %57'si**
> (bağlam medyanı 3.059 ↔ 7.200 karakter). Yani `k=10`'un tuzak-geçerliliği kaynakların
> **yarısından biraz fazlası** görülerek kararlaştırılmış; `k=4`'ünki tamamı görülerek.
> **Payda ekseni EŞLEŞMİYOR** → [ADR-0057](../../adr/0057-harness-rekabet-kapisi-esit-sinav.md)
> gereği bu satır **TANIMSIZ** damgalıdır: sayı kayıtta kalır, ondan **hüküm kurulmaz**.
> ⛔ Yumuşatılmaz — *"muhtemelen yine de geçerli"* denmez. Alet kuramadığı hükmü kurmaz.
> Kapatan şey klibi büyütmek; reçete + fiyat (≈$0,30) `docs/open_questions.md`'de **açık borç**.

> 🚨 ᴷ³ **BU GİRİŞİN M2b SAYILARI ESKİ ALETİN BİRİMİNDEDİR (2026-08-06 tespiti).** `valid_trap`
> paydası hakemin **modelin cevabını görerek** verdiği bir karardı. Yeniden puanlanmış değerler
> ([#57](2026-08-06-cekinme-aleti-onarimi.md)): AÇIK `h2b@k=4` **0,840 → 0,735** · KAPALI çıpa
> **0,877 → 0,766** · `k=10` **0,784 → 0,723**. ⭐ **BU GİRİŞİN HÜKMÜ AYAKTA:** `0,735 < 0,766`,
> işaret aynı, kapı yine KALDI. Aşağıdaki eski sayılar bilerek silinmedi (denetim izi).
> 🎁 Ve bu girişin *"geçersiz tuzak 30/80 ↔ 15/80"* gözlemi **aletin kusuruymuş**: aynı sınavda
> payda artık üç kolda da **eşit** (68). O paragrafın mekanizma açıklaması **çürüdü**.

⚖️ **ADR-0057 Kademe 2 kapısı: KALDI** (0,840 < 0,877 + 0,003). İki bağımsız tahmin edici de
aynı yönde (**−0,037** hakem · **−0,026** regex), ikisi de hakemin **~0,3 puanlık** yeniden-koşum
gürültü tabanının üstünde.

🚨 **Ve zorluk şerhi bulguyu ZAYIFLATMIYOR, GÜÇLENDİRİYOR.** KAPALI'nın 4 çeldiricisinin
**tamamı** altınla aynı kanundan (`sample_distractors` komşu-öncelikli seçiyor, `raft_pack.py:75-91`)
→ zorluk **1,0000**. AÇIK'ta bu oran **0,4750**; dağınık bağlamda *"kaynak yetmiyor"* demek daha
kolaydır. **AÇIK daha kolay sınava girdi ve yine de kaybetti.**

### Ön-kayıtlı tahminler (ADR-0056 Karar 2, sayı görülmeden yazıldı)

| | tahmin | çıkan | hüküm |
| :--- | :--- | :--- | :--- |
| **A** kapının katkısı | ≈0 (0-2/80) | k=4'te kapı **2/80** reddetti, biri cevaptı | ✅ **TUTTU** |
| **B** `Rej_model` | 0,30–0,60 | **0,840** | ❌ **TUTMADI** |

**A'nın mekanizması da ayrıca doğrulandı:** `KANUN_YOK 0 · MADDE_YOK 0` ve **36/80 cevabın hiç
atfı yok** (`atifsiz_gecen`). Kapı yalnız doğrulanamayan atıf varken ateşler; ateşleyecek şey yok.

⇒ **Part 1'in M2b iddiası "sınanmamış" değil, bu rejimde YAPISAL OLARAK ateşlenemez.**
ADR-0056 Karar 2'nin yazdığı sonuç işliyor: **M2b eğitim tarafına geçer.**

**B için ADR-0056'nın kendi kuralı geçerli:** *"tutmazsa 'tahmin kötüydü' değil **'payda
yanlıydı'** diye oku."* Tahmin, altın gelmeyen **10** sorudan türetilmişti; o alt küme #53'e göre
ağırlıkla "belirsiz" sınıfıydı ve model orada daha az çekiniyor. Gerçekte model tahmin edilenin
**iki katından fazla** çekiniyor.

### ~~🎁 `k`'nın bedeli ilk kez ÇEKİNME ekseninde sayıldı~~ → 🔴 HÜKÜM DÜŞTÜ, **BORCA DÖNDÜ**

> 🚨 **ᴷ⁴ 2026-08-06 (KARAR-4 m.2) — BU BAŞLIK ARTIK HÜKÜM DEĞİL.** Aşağıdaki kıyasın iki
> kolu **aynı paydayı ölçmüyor**: kör hakem `k=4`'te kaynakların %100'ünü, `k=10`'da
> **%57'sini** görüyor (454/800, ölçüldü). ADR-0057'nin kendi mekanizması: eşleşmeyen
> eksende **hüküm kurulmaz**. ⇒ *"`k` büyütmenin çekinme bedeli"* bir **BORÇ**tur — ölçülmüş
> bir bulgu değil. Eski sayı silinmedi. Kapatan şey klip borcu (≈$0,30, `open_questions.md`);
> sadakat eksenindeki bulgu (#54) bundan **etkilenmez**, o payda paylaşmıyor.

~~`k=4 → k=10`: Rej **0,840 → 0,784** (**−5,6 puan**). Bugüne dek `k`'nın bedeli yalnız **sadakat**
ekseninde ölçülmüştü (A1·altın getirilen 0,9230 → 0,8426, #54). **İki eksen aynı yöne bakıyor:**
daha çok bağlam = hem daha az sadakat hem daha az çekinme.~~

### ⭐ Beklenmedik: geçersiz tuzak **30/80 ↔ 15/80**

Altın **ablasyona rağmen** retriever, soruyu *fiilen cevaplayan* bir kaynağı **iki kat sık**
getiriyor (hakem "kaynak zaten cevaplıyor → tuzak geçersiz" diyor). Bu retriever lehine ayrı bir
kazançtır — ve paydaların (50/51 ↔ 65) neden farklı olduğunun cevabıdır. **Kaynak sayısı eşitlendi,
kaynak İÇERİĞİ eşitlenemedi** — ADR-0057 Kademe 2'nin kabul ettiği bedelin ölçülmüş hâli.

## 2. B5 — K2'nin bedeli (`harness_tablo.py`, post-hoc, $0)

`s2-harness-k10-etiketli`, n=80:

```
ALTIN_GELMEDI 10 · TAM 22 · KIRPILDI 46 · KIRPILDI_CEVAP_DISI 2      (toplam 80 ✓)
```

🚨 **Planın okuma cümlesi yapısal olarak imkânsızdı.** Plan *"`KIRPILDI_CEVAP_DISI`, B1'in
7/80'inden düşülür"* diyordu; oysa `k2_bedeli` altın gelmediyse `ALTIN_GELMEDI` döner, dolayısıyla
`KIRPILDI_CEVAP_DISI` **ancak altın getirildiyse** çıkabilir. B1'in 7'si ise tam ters popülasyon
(`altin_gelmedi_cevapladi`). **İki küme kesişemez.**

**Gerçek yer ölçüldü:** her iki vaka da `altin_geldi_cevapladi` (54) kovasında, ikisi de **0. sırada**
getirilmiş; yalnız biri sadakat kaybetmiş (0,75). ⇒ **B1 (7/80) ve B10 (16/80) el değmemiş kalıyor;
kırpmanın bedeli 2/80 ile dar bir şeride hapsolmuş.**

⚠️ Sınıflandırma **4 sınıflı** tutuldu, çünkü *"kırpıldı"* tek başına bir şey söylemiyor: 46 vaka
kırpılmış ama cevabın dayandığı cümle bağlamda duruyor. Tek sınıfa indirmek B5'i **23 kat**
şişirirdi.

## 3. B8 — yazım-hatası tolerans eğrisi (post-hoc, $0, **doğrulayıcı DONUK**)

Üç koşu birden süpürüldü:

```
koşu              eşik 1        eşik 2        eşik 3
s2-harness-k10    2 kurtarılan  2             2      · yanlış eşleme 0
h2b k=4           —  (KANUN_YOK yok)
h2b k=10          2 kurtarılan  2             2      · yanlış eşleme 0
```

🚨 **Ama eğri "eşik 3 güvenli" DEMİYOR — "bu veriyle karar verilemez" diyor.** Üç koşuda toplam
**4 `KANUN_YOK` atfı** var ve **hepsi aynı hatanın tekrarı**: `"Sanat Eseleri Kanunu"`
(FİKİR VE SANAT ESERLERİ KANUNU'ndan bir `R` düşmüş). **Toleransın risk tarafında sıfır gözlem
var.** ⇒ Tolerans **BENİMSENMEDİ** (ADR-0056 Karar 4); kapı **katı** kaldı.

🐞 **Betiğin ilk hâli sıfır üretiyordu ve sebebi bir ölçüm hatasıydı:** toleransı korpusun **tam
adlarına** uyguluyordu, oysa doğrulayıcı ≥2 sözcüklü **sonek** indeksiyle eşleştiriyor (model
resmî adın kısa hâlini yazıyor). `"Sanat Eseleri Kanunu"` → tam ada mesafe **11**, doğru soneke
mesafe **1**. Sonek uzayına taşındı. Ek koruma: tek sözcüklü soneke inilmiyor —
`mesafe("KANUNU","İŞ KANUNU") = 3`, eşik 3'te yüzlerce kanuna eşleşirdi.

⭐ **Hatanın üç koşuda da aynen tekrarlaması** onu rastlantı değil, modelin **tekrarlanabilir bir
transkripsiyon tiki** yapıyor — dolayısıyla çaresi de tolerans değil, dar ve hedefli olabilir.

## 4. ⚖️ HARNESS KAZANÇ TABLOSU — [ADR-0057](../../adr/0057-harness-rekabet-kapisi-esit-sinav.md)

**Her satırda adillik hükmü zorunludur.** Olmadığı için bugüne kadar *"harness kötüleştirdi"*
yanlış okuması kolaydı — oysa eksenlerin çoğunda KAPALI **rakip değil TAVAN**.

```
kademe  eksen                     kaynak    KAPALI    AÇIK     hüküm
──────  ────────────────────────  ───────   ──────    ─────    ─────────────────────
  1     kapı + doğrulayıcı        aynı      —         2/80     TAM EŞİT SINAV · katkı ≈0
  2     A1 · altın getirilen      5 ↔ 5     0,9087    0,9230   EŞLEŞMİŞ ✅ GEÇTİ (k=5)
  2     M2b Rej                   4 ↔ 4     0,8770    0,8400   EŞLEŞMİŞ ❌ KALDI (k=4)
  3     M1 manşet kütle           5 ↔ 10    %71,6     %61,3    TAVAN — hüküm YOK
  3     M4 / M3 / M5 / M2         —         —         —        TANIMSIZ
```

⚠️ **Kademe 3 satırları için *"AÇIK burada geride"* cümlesi KURULMAZ.** KAPALI orada altını
**kurgu gereği** alıyor; M4 yalnız altını verir, M3/M5 bağlamın **yokluğuyla** tanımlıdır,
M2'de retriever altını bulunca çekinme koşulu **kendini yok eder**. Bu ayrım yazılmazsa tablo
yanıltır.

⭐ **Kademe 2'nin iki satırı zıt yönde ve ikisi de gerçek:** retriever bulduğunda model daha
sadık (**+1,4 puan**), altın hiç yokken daha az çekingen (**−3,7 puan**). Harness *"iyi"* ya da
*"kötü"* değil — **bulduğunda kazandırıyor, bulamadığında kaybettiriyor.**

## 5. D1 — B-i deneyi: kaynak-yeterliliği önsözü ✅ **BAŞARILI**

[ADR-0055](../../adr/0055-isabet-denetimi-ekseni.md)'in **B-i** müdahalesi: sistem istemine tek
satır — *"Cevabına başlamadan ÖNCE, verilen kaynağın soruyu cevaplayıp cevaplamadığını tek
cümleyle belirt."* Aynı model, aynı indeks, aynı `k`, aynı rejim. **Değişen tek şey istem.**

```
                       ÇIPA (h1)   D1 (B-i)     fark
coverage                  0,7625     0,7625   ±0,0000
A1 cevaplanan             0,8042     0,8229   +0,0187
A1 · altın getirilen      0,8616     0,8705   +0,0089
kütle                     0,6132     0,6275   +0,0143
recall@10                 0,8750     0,8750   ±0,0000   ← retriever'a dokunulmadı
```

**Ön-kayıtlı kabul (ADR-0055 + ADR-0056 Karar 3): `kütle > %61,3` ✓ **VE** `yön doğru` ✓
→ BAŞARILI.**

⭐ **Asıl bulgu çapraz tabloda: dört hücre de eşzamanlı olarak doğru yöne gitti.**

```
                          çıpa   D1
altın geldi · cevapladı     54    56   (+2)
altın geldi · çekindi       16    14   (−2)   ← borç B10 (aşırı-red)
altın gelmedi · cevapladı    7     5   (−2)   ← borç B1 (isabetsizlik)
altın gelmedi · çekindi      3     5   (+2)
```

**Tek bir istem satırı, Part 1'in iki açık borcunu birden 2'şer kalem küçülttü.** Ve yön ayrımı
**keskinleşti**: belirsiz altkümede çekinme 0,2778 → **0,3333**, ayırt edicide 0,2258 →
**0,2097**; açıklık **5,2 → 12,4 puan**. [#53](2026-08-05-ayirt-edicilik-etiketi.md)'ün ölçtüğü kök
mekanizma — *çekinme sinyali konusal uyuma bakıyor, yeterliliğe değil* — tam bu eksende
**gerilemeye başladı**.

**Doğrulamalar:** `harness_tablo` A1 = `rescore_answered` A1 = **0,8229** birebir (tuzak 2.16) ·
`recall@10` **değişmedi** → değişenin yalnız istem olduğunun kanıtı · bayrak künyede **ve**
kodun kendi ABLASYON satırında görünüyor (dropped-flag sigortası).

⚠️ **İki şerh, ikisi de kayda giriyor:**
1. **Kod bu koşuyu ablasyon damgalıyor** (`"sistem istemi ana protokolden FARKLI, bu koşu ana
   tabloya girmez"`). **Benimsemek AYRI bir karardır** ve kendi ADR'sini ister — tıpkı B8
   toleransı gibi. **Ürünün sayısı %61,3 olarak kalır.**
2. **2/80'lik hücre hareketleri için ayrı bir gürültü tabanı ölçülmedi.** A1'deki +1,87 puan
   hakemin ölçülmüş tabanının (0,3) üstünde, ama hücre sayıları farklı bir tahmin edicidir.

## Ders

> **Deterministik kodun kapatabileceği açık kalmadı; kalan açığın tamamı modelin çekinme
> kararında — ve o karara en ucuz müdahale en pahalı iki borcu birden hareket ettirdi.**

Bu turun mekanizması şu: harness'ın üç parçasından **ikisinin gerekçesi öldü** (doğrulayıcı
ateşleyecek sınıf bulamıyor, kapı ateşleyecek atıf bulamıyor), **biri ayakta** (retriever —
onsuz ürün yok). Geriye kalan bütün açık, modelin *"bu kaynak yetiyor mu"* sorusunu
**soramamasından** geliyor:

- altın **bağlamdayken** çekiniyor (**16/80**),
- altın **yokken** çekinmiyor (`Rej` 0,840 < 0,877 — ᴷ³: **0,735 < 0,766**, işaret aynı),
- ~~bağlam **dağıldıkça** daha az çekiniyor (`k=4 → 10`: 0,840 → 0,784).~~
  🔴 **BU AYAK DÜŞTÜ** (KARAR-4 m.2): `k=10`'un paydası **TANIMSIZ** (yukarıdaki blok) →
  ADR-0057 gereği hüküm kurulmaz. Kalan **iki** ayak ayakta; teşhis onlarla taşınıyor.

~~Üçü~~ İkisi aynı kusurun ~~üç~~ iki yüzü. Ve D1 bunu **istem katmanından** kısmen düzeltebildiğini gösterdi —
demek ki yetenek **mevcut ama tetiklenmiyor**, yok değil. Bu, eğitim turunun hedefini
daraltıyor: *yeni bir yetenek öğretmek* değil, **var olan yeteneği varsayılan hâle getirmek**.

⚠️ **Ve bu turda bir tahminim çürüdü, olduğu gibi kayda geçiyor:** D1 koşulmadan önce
*"istem katmanı eğitilmiş bir refleksi değiştirmez, tavanı düşüktür"* demiştim. **Ölçüm bunu
çürüttü.**

## Açık kalanlar

| borç | durum |
| :--- | :--- |
| **B5** | ✅ **KAPANDI** — 2/80, ve gerekçesi (B1'i kirletiyor) **yapısal olarak imkânsız** çıktı |
| **B8** | 🔴 **AÇIK** — eğri ölçüldü ama **risk tarafında sıfır gözlem**; tolerans benimsenmedi |
| **B10** aşırı-red | 🔴 **AÇIK, ama ilk kez KIPIRDADI**: 16/80 → **14/80** (D1 ile, istem katmanında) |
| **B1** isabetsizlik | 🔴 **AÇIK, ama kıpırdadı**: 7/80 → **5/80** (D1 ile) |
| **B4** `τ_a` seyrelmesi | 🔴 **AÇIK** — dokunulmadı; ‖τ_a‖ = 1,18 |
| **B9** indeks hijyeni | 🔴 **AÇIK** — bilinçli, indeksi değiştirir |
| **B6** canlı bedesten | 🔴 **AÇIK** — ürün işi |

**Yeni doğan borçlar / kararlar:**

| # | ne | neden karar gerektiriyor |
| :--- | :--- | :--- |
| **YB1** | **B-i önsözü benimsensin mi?** Ölçüldü ve kazandırdı (+1,43 puan kütle), ama ana protokolü değiştirir → **tüm çıpalar yeniden türetilir** | Kabul edilirse `%61,3` çıpası ve ondan türeyen her kıyas yenilenir. **Kendi ADR'sini ister.** |
| **YB2** | **M2b artık bir eğitim borcudur** — kapı yolu ölçülerek kapandı | Part 1'in gerekçesi öldü; hedef listesi [ROADMAP](../../../ROADMAP.md) 2.1c'ye taşınmalı |
| **YB3** ᴷ⁴ | ~~**`k`'nın bedeli iki eksende birden ölçüldü**~~ → **TEK eksende ölçüldü (sadakat).** Çekinme ekseni **TANIMSIZ** (2026-08-06, KARAR-4 m.2): kör hakem `k=10`'da kaynakların **%57'sini** görüyor, `k=4`'te %100'ünü → ADR-0057, hüküm kurulmaz | `k=20` gerekçesi yalnız **sadakat** bulgusuyla zayıflıyor. Çekinme bacağı **açık borç**: klip ≈$0,30 ödenmeden hüküm yok |

**Sonraki tur için ön-kayıtlı soru** *(bu turun kendi dersinden doğdu — Part 1 tam burada hata
yapmıştı: çareyi ölçmeden gerekçe saydı)*:

> *"Yeterlilik-etiketli negatiflerle yeniden eğitilmiş bir `τ_a`, B10'u 14/80'in altına ve
> M2b `Rej`'i 0,877'nin üstüne çıkarır mı?"* — **bu bir tahmindir, ölçülmeden gerekçe sayılmaz.**
>
> 🚨 **BİRİM DAMGASI 2026-08-06 (Ö3).** Bu **ön-kayıtlı soru** aktif turun hedefini tanımlıyor
> ve emekli birimdeydi. Yürürlükteki birimde eşik: **M2b `Rej` > 0,766** ᴷ³ ~~0,877~~
> (KAPALI çıpa). ADR-0050: eşiğin **anlamı** korundu, yalnız **birimi** çevrildi.
> ⚠️ Emekli `0,877`'ye bakan okuyucu **gerçek bir iyileşmeyi başarısızlık ilan eder**.
