# #59 — M2 paydası kapandı · KARAR-4: anahtar hakem istemine geri eşitlendi · ARA KAPI 1. gözlem türetildi

**Tarih:** 2026-08-06 · **Tur:** Görev 2, üçüncü düzeltme dalgası
**Bedel:** GPU **$0** · hakem **$0,1054** *(bütçe ≈$0,11)* · rakip çıkarımı **$0**
**Çıktılar:** `outputs/eval/karar3-m2-payda/` · `outputs/eval/_artefakt/valid_trap_kor_onbellek.json`
**Kararlar:** KARAR-3 · KARAR-4 (ikisi de insan kararı) · [ADR-0045 §3](../../adr/0045-ara-kapi-merge-onarim-kontrolu.md) tamamlandı

> **İki cümlede:** `m2` paydası on koşuda birden ödendi ve **eşitlendi (66/70)** — düzeltme
> **bizim lehimize** çıktı ve öyle raporlanıyor. K-1'in tam-metin önbellek anahtarı **geri
> alındı**: daha büyük bir tuzağı açıyordu ve sayısal karşılığı yoktu; bedeli `k=10`
> paydasının **TANIMSIZ** damgasıyla açıkça ödendi.

---

## 1. KARAR-3 — `m2` paydası: on koşu, tek ödeme, **eşit payda**

`m2`, K3/KARAR-2'den sonra paydası hâlâ modele bağımlı kalan **tek** moddu: aynı 70 kalemlik
sınavda on kol **55-63** arası payda gösteriyordu. M3'ten farkı, paydanın tanımdan
çıkmaması — hakem çağrısı gerekiyordu.

**$0'lık kestirme (mevcut kör damgayı devralmak) reddedildi:** o ölçüm `gateway=openai`,
bugünkü koşular `openrouter` → tuzak 2.7 / ADR-0029 ihlali olurdu. Ucuz ve yanlış bir sayı,
pahalı ve doğru olandan kötüdür.

**Sınav paylaşımı ölçüldü, varsayılmadı:** on koşunun `(soru, referans)` anahtar kümesi
**70/70 kesişiyor** → tek ödeme hepsini kapatır. `--pay-kaynagi onceki` ile pay hakemi hiç
çağrılmadı; böylece paydanın etkisi payın gürültüsünden **ayrılabilir** kaldı.

| özne | payda eski → **yeni** | Rej* eski → **yeni** | Δ |
| :--- | ---: | ---: | ---: |
| çıplak base (bütçeli) | 59 → **66** | 0,814 → **0,803** | −1,1 p |
| Gemini 3.1 FL | 57 → **66** | 0,930 → **0,848** | **−8,2 p** |
| `τ_g` v1 | 55 → **66** | 0,873 → **0,833** | −4,0 p |
| base + yeterlilik önsözü | 62 → **66** | 0,968 → **0,924** | −4,4 p |
| **ham TIES = `tgta_v1`** | 56 → **66** | 0,893 → **0,833** | −6,0 p |
| norm-dengeli `min` | 61 → **66** | 0,934 → **0,909** | −2,5 p |
| ⭐ **`τ_a` v1** | 63 → **66** | 0,984 → **0,955** | −2,9 p |
| base (thinking-off) | 60 → **66** | 0,633 → **0,606** | −2,7 p |
| Gemini (thinking-off) | 57 → **66** | 0,842 → **0,758** | **−8,4 p** |
| `τ_g` (thinking-off) | 59 → **66** | 0,458 → **0,439** | −1,9 p |

### ✅ Sınav paylaşımı doğrulandı: **paydalar EŞİT** — ama bilgiyi taşıyan kontrol hangisi?

On koşunun `valid_traps` değeri **{66}** — tek eleman.

> ⚠️ **DÜZELTME 2026-08-06 (küçük k1).** İlk yazımda buna *"kendi kendini doğrulayan sınav"*
> denmişti; ifade **fazla güçlüydü** ve düzeltiliyor. **70/70 anahtar kesişimi** verildikten
> sonra payda eşitliği bir **teorem**, bağımsız bir gözlem değil: içerik-adresli önbellek aynı
> anahtara aynı kaydı döndürür, dolayısıyla `{66}` sözlük aramasının aritmetik sonucudur
> (maliyeti **$0**; 9 kolun 9'unda `gecerlilik_onbellekten = 70`).
> ⭐ **Bilgi taşıyan asıl kontrol, anahtar kesişiminin KENDİSİdir** (70/70) — o gerçekten
> düşebilirdi ve düşmedi. `{66}` kontrolü, kesişim ölçüldükten *sonra* çalışan bir tutarlılık
> kontrolüdür: bozuk/kirli bir önbellek ya da yanlış eşleşen bir koşu onu yine de ayrıştırırdı,
> yani **bedava bir alet denetimi** olarak değerli — ama *"sınav paylaşılıyor mu"* sorusuna
> bağımsız kanıt sunmaz.
> 🚨 **2. dalganın totolojisiyle AYNI SINIFTA DEĞİL:** o kontrol tanımı gereği düşemezdi
> (ölçtüğü şeyin kendisinden türetiliyordu). Bu kontrol **düşebilir** — yalnızca *yeni bilgi*
> ekleme payı, kesişim ölçüldükten sonra küçüktür. Ayrım kaydedildi çünkü ikisini aynı kefeye
> koymak, gerçekten değerli olan bedava denetimi de attırır.

### 🚨 Düzeltmenin yönü **BİZİM LEHİMİZE** — ve bu yüzden ayrıca yazılıyor

En çok kayan özne **RAKİP**: Gemini −8,2 puan, biz −6,0. `tgta_v1` ↔ Gemini açıklığı
**3,7 → 1,5 puana** daralıyor. Kirli paydadan en çok Gemini yararlanıyordu.
⚠️ Aynı sınıftaki [#46](2026-07-30-cp2r-kor-payda.md) düzeltmesi **ters yöne** gitmişti
(aleyhimize). İki turda da yön **seçilmedi**, ölçüldü — ve her ikisi de raporlandı.

### 🎁 Beklenmedik çapraz kontrol: iki alet **`m2`'de aynı paydayı** veriyor

#46 (emekli, klip **900**) `m2` paydasını **66/70** ölçmüştü; bugünkü alet (klip **3500**) de
**66/70** veriyor. Bu, K-3'ün teşhisini **daraltarak doğruluyor**: 900 klipi bir kategori
hatasıydı ama zararı **birleştirilmiş çok-kaynaklı bağlamda** (`m2b`, `h2b`) doğuyor.
`m2`'nin kaynağı tek bir altın madde (medyan **587** karakter) — iki klip de tamamını
gösteriyor, bu yüzden iki alet aynı hükmü veriyor.

---

## 2. ⭐ ARA KAPI 1. GÖZLEM — türetildi, **GEÇTİ**, ve ilk kez birim-tutarlı

Ön-kayıtlı olan **formül**; sayı bugünkü base ölçümünden türer. ⛔ ADR-0050 gereği
eşiğe/çarpana/formüle **hiç dokunulmadı**.

| bacak | formül | çıpa | eşik | `τ_a` tekil | hüküm |
| :--- | :--- | ---: | ---: | ---: | :--- |
| M2 Rej | `base M2 + 0,12` | 0,803 | **0,923** | **0,955** | ✅ **GEÇTİ** (+3,2 p) |
| muhafız M1 A1 | `0,90 × base A1` | 0,9777 | **0,8799** | **0,9697** | ✅ **GEÇTİ** |
| ön-kayıtlı ham sayılar | — | — | 0,934 · 0,888 | 0,955 · 0,9697 | ✅ **ikisi de** |

🚨 **Bu ✅ ilk kez BİRİM-TUTARLI.** Sprint 2 kapanışındaki `0,984 ≥ 0,923` kıyası **karışık
birimdeydi**: pay özneye bağlı paydadan (63/70), eşik #46'nın kör çıpasından. Hüküm aynı
kaldı, ama gerekçesi ilk kez sağlam.

**Marj — referans noktası EŞİĞİN üstü:** ~~+18,1 →~~ **+6,1 p → +3,2 p** (marj **~1,9× daraldı**).

> 🚨 **DÜZELTME 2026-08-06 (kusur Ö1) — bu cümlenin ilk hâli KARIŞIK BİRİMDEYDİ.** İronik
> biçimde *"ilk kez birim-tutarlı"* iddiasını taşıyan cümlenin **kendi marjı** iki farklı
> referans noktasından okunmuştu. Tanımlar (`#48:1103`):
> ```
> ÇIPANIN üstü  = Rej* − cevaba-kör base      +18,1 = 0,984 − 0,803
> EŞİĞİN üstü   = Rej* − eşik                  +3,2 = 0,955 − 0,923
> ```
> Yayımlanan `18,1 → 3,2` **iki okuma da değildi**. Eşleşen okumalar:
> ```
> EŞİĞİN üstü  (bu turun seçtiği):  +6,1 p → +3,2 p     ~1,9× daraldı
> ÇIPANIN üstü:                    +18,1 p → +15,2 p    ~1,2× daraldı
> ```
> ⚠️ Karışık hâli okuyan biri *"payda onarımı marjı **5,7 kat** eritti"* der ve `τ_a`'nın kapıyı
> **kıl payı** geçtiğini sanır. Gerçekte kol kapıyı **rahat** geçiyor — ki §2'nin teşhisi
> (*sorun `τ_a`'nın kalitesi değil, merge'in onu taşımaması*) tam buna dayanıyor.
> **Kural, kayda geçti:** bir marj/fark yazarken **referans noktası cümlede söylenir**.
> Aynı düzeltme `#48`, `research_log/README.md` ve `gorev-2-report.md`'de de yapıldı.

### ⇒ ADR-0045 §3'ün ön-kayıtlı tablosunda satır: **`✅ ❌` → DUR**

2. gözlem 🔴 düşmüştü (K-2: merge M2b **0,766 < 0,8649**). Tablonun kendi metniyle:
*"Kol tek başına iyi ama birleşince taşımıyor; iç iddianın öncülü sorunlu."*

**Türetme hükmü değiştirmedi** (iki olası satırda da DUR'du) **ama teşhisi belirledi:**
sorun `τ_a`'nın kalitesi **değil** — kol tek başına kapıyı rahat geçiyor — **merge'in onu
taşımaması**. Kapının §Sonuç'ta vaat ettiği *"kaldı ama neden kaldı"* teşhisi tam bu.
CP4-CP5 harcaması bu kapıdan **yetki almıyor**.

### ⭐ Kaydedilmemiş sonuç — **merge'in M2'ye katkısı `+0,020` → `+0,000`**

Payda eşitlenince yukarıdaki tablodan doğrudan okunan, ama hiçbir yerde **yazılmamış** bir
gözlem çıktı:

```
τ_g v1     55/66 = 0,833        (emekli birimde 0,873)
tgta_v1    55/66 = 0,833        (emekli birimde 0,893)
                                merge'in M2'ye katkısı  ~~+0,020~~ → +0,000
```

İki kol **birebir eşit** — aynı payda, aynı pay, aynı kalem sayısı. Emekli alette merge `τ_g`'yi
M2'de **+0,020** geçiyor görünüyordu; o fark tümüyle **paydaların farklı olmasından** geliyordu
(`τ_g` 55/55 değil 55/**55 payda**, `tgta_v1` 56/**56 payda** — özneye bağlı payda iki kolu farklı
sınavda ölçüyordu).

⭐ **Bu gözlem, ARA KAPI'nın teşhisini BAĞIMSIZ olarak güçlendiriyor.** §2'nin *"merge `τ_a`'yı
taşımıyor"* hükmü M2b ekseninden (`0,987 → 0,766`) türetilmişti. M2 ekseni şimdi aynı şeyi
**ikinci, bağımsız bir yerden** söylüyor: merge M2'de `τ_g`'nin **üstüne hiçbir şey koymuyor**,
oysa `τ_a` tek başına o eksende **0,955**. İki eksende de merge, çekinme kolunun kazanımını
taşımıyor.

⚠️ **Şerh (ADR-0057 · kuantum):** `+0,000` *"hiç fark yok"* demektir, *"fark ölçülemedi"*
demez — iki kol aynı 66 kalemde **aynı 55'inde** çekiniyor. Ama ters yön de doğrudur: bu eksende
`1/66 = 1,52 puanlık` bir kuantum var, dolayısıyla `+0,000` ile `±1 kalem` arasında ayrım
kurulamaz. Çözünürlük sınırı borç olarak `docs/open_questions.md`'de.

---

## 3. KARAR-4 — K-1'in anahtar onarımı **geri alındı**, bedeli damgayla ödendi

[#58](2026-08-06-payda-tekillesmesi.md) önbellek anahtarını `hash(soru, TAM kaynak)`'a
taşımıştı (tuzak 2.17). Aynı giriş **sayısal iddianın doğrulanmadığını** da yazmıştı:
15 çakışan çift yeniden ödendi, **15/15 aynı hüküm**.

**Sebebi yapısal:** klip sabitken çakışan çiftin hakem istemi **bayt-bayt aynı**. Yani
anahtar, hakemin **ayırt edemediği** bir farka göre bölünüyordu — bu, *aynı istem → aynı
cevap* değişmezini kırar. Ölçülen bedel: **5.363** ayrı istemin **65'i** birden fazla
anahtara düşüyor · **83 garantili gereksiz çağrı** · ve aynı istem iki kayda dönerse `Rej*`
**~1,5 puan** oynar ve *"k'nın çekinme bedeli"* diye okunur, oysa **saf gürültü**.

**Onarım (yapısal, $0):** klip artık tek yerde — `score_abstention.hakem_kaynagi()`. Pay
hakemi, payda hakemi ve önbellek anahtarı üçü de oradan besleniyor; ayrışamazlar.
Önbellek göçü kayıpsız: `.ONCEKI-KLIPLI-ANAHTAR` yedeği (250 kayıt) birleştirildi
(kesişim 162, **değer uyuşmazlığı 0**), `h2b k=4` ve `k=10` **80/80** önbellekten karşılanıyor
→ yeniden ödeme yok.

### 🔴 Bedeli: `k=10`'un paydası **TANIMSIZ** — ve bir hüküm BORCA döndü

`k=4` bağlamı `k=10`'unkinin **öneki** olduğu için ikisi tek payda kaydına düşer. Asıl sorun
bu değil, **klip**: ölçüldü (`[KAYNAK` sayımı, n=80) —

| sınav | tam kaynak | hakemin gördüğü | oran |
| :--- | ---: | ---: | ---: |
| `h2b@k=4` | 320 | 320 | **%100** ✅ |
| `h2b@k=10` | 800 | 454 | **%57** 🔴 |

Payda ekseni **eşleşmiyor** → [ADR-0057](../../adr/0057-harness-rekabet-kapisi-esit-sinav.md)
gereği bu satır **TANIMSIZ** damgalıdır ve ondan hüküm kurulmaz.

⇒ **#56'nın *"`k` büyütmenin çekinme bedeli"* hükmü (Rej 0,840 → 0,784) hüküm olmaktan çıktı,
BORCA döndü.** Sadakat eksenindeki bulgu (#54, A1 0,923 → 0,843) **etkilenmiyor** — o payda
paylaşmıyor. Borcu kapatan tek şey klibi büyütmektir (reçete + **≈$0,30**,
[`open_questions.md`](../../open_questions.md)).

⛔ Yumuşatılmadı: *"muhtemelen yine de geçerli"* yazılmadı. **Alet kuramadığı hükmü kurmaz.**

### Klibi büyütmek bu turda bilinçle reddedildi

Turun **üçüncü** alet değişikliği olurdu ve pay hakemi aynı klibi kullandığı için **tüm
çekinme sayıları yeniden oynardı**. Reçete + fiyat açık borç olarak duruyor.

---

## 4. Kod kusurları — biri #58'in kendi kestirmesini **otomatikleştirmişti**

### 🔴 K1 · `cp2c_kabul.sh` openai kapısıyla ORTAK önbelleğe yazıyordu

Önbellek anahtarı `sha256(soru ‖ kaynak)` — **hakem modelini de kapıyı da taşımıyor**; okuma
yolunda tek kontrol `if anahtar in onbellek` idi, kayıttaki `hakem` alanı **hiç
okunmuyordu**; ve `cp2c_kabul.sh:39` → `LLM_GATEWAY="${LLM_GATEWAY:-openai}"`.

**Başarısızlık biçimi:** zincir bir kez koşarsa sonraki herhangi bir openrouter ölçümü aynı
`(soru, kaynak)` çiftinde **openai paydasını sessizce devralır** ve özetine
`judge_gateway: "openrouter"` + `gecerlilik_maliyet_usd: 0.0` yazar. **Bu, KARAR-3'te elle
reddedilen kestirmenin ta kendisidir** — dalga kestirmeyi reddetmiş, sonra otomatikleştirmişti.

**Onarım:** kayıt artık `hakem` + `kapi` taşıyor; okuma yolu bugünkü `(gecerlilik_hakemi,
gateway)` ile karşılaştırıyor ve uyuşmazlıkta **DURUYOR**. Damgasız eski şema kaydı da
uyuşmazlıktır — *"bilinmiyor"* sessizce *"uyuyor"* olamaz. Mevcut 353 kayda `kapi: openrouter`
damgası **iki bağımsız kanıtla** vuruldu: (a) bu önbelleğe kör hakem çağrısı yapmış her koşu
özetinde `judge_gateway: openrouter`; (b) kayıtlı `hakem` değeri `openai/gpt-4o`, yani
openrouter'ın çözümlediği ad (openai kapısında `resolve()` çıplak `gpt-4o` verir).

⚠️ `cp2c_kabul.sh`'in openai varsayılanı **değiştirilmedi**: kabul ölçütünü hangi yığının
ürettiği bir **rejim kararıdır**, sessiz bir düzeltme değil. Artık iki yönde de fail-loud;
seçenekler `open_questions.md`'de.

### 🔴 K2 · `%71` onarım oranı üç canlı belgede eski aletin türetmesi — ikisi **damganın altında**

Oran `(merge − τ_g) / (base − τ_g)`, yani **üç girdiden herhangi biri** yeniden puanlanınca
kayar. ᴷ³ üçünü de yeniledi:

```
eski  (0,877 − 0,607) / (0,986 − 0,607) = %71,2
yeni  (0,766 − 0,506) / (0,961 − 0,506) = %57,1
```

Girdiler yerinde güncellenmiş, **türetilmiş nicelik güncellenmemişti** — üstelik iki satır
`ᴷ³` taşıyordu, yani *"gözden geçirildi"* diye **tasdik edilmiş** bir yanlış sayı.
**Damgasız olmaktan zararlı.** `MODEL_CARD.md` dışa dönük artefakt kartıdır ve oranı **14
puan fazla, bizim lehimize** ilan ediyordu.

Süpürge `grep` ile yapıldı ve **iki belge daha buldu**: `README.md` ve `README.tr.md` — ikisi
de dışa dönük, ikisi de `%71` diyordu. Bulgu listesi üç belge saymıştı, gerçek **beş**.

⭐ **Kural yazıldı:** `ᴷ³` damgası **türetilmiş nicelikleri de kapsar**. Bir girdiye damga
vururken ondan hesaplanan oran/fark/yüzdeler `grep` ile taranır.

### Ö5 · `gecerlilik_devralinan` **iki taban tabana zıt şeyi** sayıyordu

`--payda-kaynagi onceki` devralması (kendi eski skorlamasından **toptan**) ile önbellek
isabeti (**başka koşuyla sınav paylaşımı**) aynı sayacı artırıyordu. Ölçülen karışım:
`olcum-h2b-k10` → 65 (önbellek) · `cp09-ab-ayrimi` → 70 (önceki koşu). Tuzak 2.17'nin
öngördüğü kontrol tam bu alana dayanıyor ve **koşulamıyordu**. İki alan:
`gecerlilik_onbellekten` · `gecerlilik_onceki_kosudan`.

### k-3 · bütçe kesintisi damgasızdı

Bütçe dolunca `break` ediliyor, özete hiçbir damga düşmüyordu; `n` ve payda **sessizce**
küçülüyordu. `--payda-kaynagi hakem` artık gerçek para harcadığı için bu dalın
erişilebilirliği arttı. `butce_kesildi` alanı eklendi.

---

## 5. Yayılım — damgalanan yerler

| kusur | belgeler |
| :--- | :--- |
| **K2** `%71 → %57` | `MODEL_CARD.md` · `kollar.md` · `sprint2/defter.md` · **`README.md`** · **`README.tr.md`** *(son ikisi bulgu listesinde yoktu)* |
| **Ö2** emekli birimde ön-kayıtlı eşik | `research_log/2026-08-04-modul-basina-norm.md` |
| **Ö3** damgasız `0,607→0,877` | `open_questions.md` #12 |
| **Ö4** belge kendi içinde çelişiyor | `kollar.md` `τ_g` açık-kalemler tablosu |
| **KARAR-4 m.2** `k=10` TANIMSIZ | `#56` (tablo · başlık · YB3) · `research_log/README` #56 ve #58 · `ROADMAP.md` B3 |
| **KARAR-3** `m2` yeniden puanlandı | `MODEL_CARD.md` · `kollar.md` · `defter.md` · `ROADMAP.md` · `ADR-0045` · `#48` |
| **tuzak 2.17** reçetesi tersine | `yurutme-tuzaklari.md` (teşhis ayakta, çare değişti) |

---

## 6. Dersler

1. **Bir onarımın sayısal karşılığı yoksa, açtığı gürültü yolu net zarardır.** K-1 doğru bir
   tuzağı kapatıyordu ama ölçüm *"15/15 aynı hüküm"* dediğinde bu bir **sonuç**, dip not değil:
   onarımın kazancı sıfır, bedeli 83 gereksiz çağrı + 1,5 puanlık sahte oynama.
2. **Damga, türetilmiş niceliklere de yürür.** Girdileri yenileyip oranı unutmak, damgasız
   bırakmaktan **daha kötüdür** — sayı artık *tasdikli* yanlıştır.
3. **Bir sayaç iki şeyi sayıyorsa, ona dayanan kontrol koşulamaz.** Ö5 bir isimlendirme
   kusuru gibi görünüyordu; gerçekte tuzak 2.17'nin denetim mekanizmasını devre dışı bırakmıştı.
4. **Kestirmeyi elle reddetmek yetmez.** #58 §3 kestirmeyi gerekçeli reddetti, aynı dalga onu
   koda gömdü. Reddedilen bir yolun **kodda kapalı olduğu** ayrıca doğrulanmalı.
5. **Süpürge `grep` ile yapılır, gözle değil.** Ö3 bir önceki dalganın dosyayı açıp aradığı
   satırı görmemesiydi; bu turda aynı yöntem iki ek belge (`README` × 2) buldu.
