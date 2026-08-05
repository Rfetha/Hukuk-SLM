# #52 — Korpusun kendisi bozuk: satırların %22,7'si yinelenen anahtar · ve B7'nin mekanizması düzeltildi

**Tarih:** 2026-08-05 · **Sprint:** [`sprint3.md`](../../../sprint3.md) **S2**'nin keşif turu
**Bedel:** $0 — tamamı salt-okunur korpus ölçümü, model/hakem/GPU yok
**Kaynak:** `data/corpus/mevzuat_maddeler.jsonl` (40.496 satır, 4 alan)

> S2 (*"korpusa yürürlük alanı ekle"*) için `(Mülga: …)` kalıbını ayrıştırmaya hazırlanırken
> ölçüldü. **Aranan şey bulundu ama yanında aranmayan bir şey çıktı:** korpusun madde
> kimliği güvenilir değil. Bu, B7'nin `research_log` #51'de kaydedilen mekanizmasını
> **düzeltiyor** — açık orada anlatıldığından bir kat daha derin.

## 1. Ölçüm — anahtar bütünlüğü

`madde_anahtari(kanun_no, madde_no)` ile normalleştirilmiş anahtarlar:

| büyüklük | sayı | oran |
| :--- | ---: | ---: |
| satır | 40.496 | — |
| **benzersiz anahtar** | **31.304** | — |
| yinelenen anahtar | 4.188 | — |
| **fazladan satır** (aynı anahtara ikinci+ kayıt) | **9.192** | **%22,7** |
| `text` < 60 karakter | 7.289 | %18,0 |
| ↳ bunlardan `(Mülga` içeren | 1.321 | — |

En çok yinelenen 5 anahtar: `3520/Geçici 1` **×162** · `3520/1` ×135 · `3520/2` ×94 ·
`3520/3` ×70 · `2004/309` ×27.

## 2. İki ayrı bozulma sınıfı — aynı sayının içinde

Yinelenme tek bir sebepten değil. Ayrıştırıldı:

### A) Tablo parçalanması — **sahte madde** üretiyor

`3520` = *"BAZI KANUNLARIN MADDE NUMARALARININ DEĞİŞTİRİLMESİ HAKKINDA KHK"*. Bu belge özünde
bir **tablodur** (eski madde no ↔ yeni madde no). Ayrıştırıcı 1.166 tablo hücresini "madde"
sanmış:

```
kanun 3520 → korpusta 1.166 satır (tüm korpusun %2,9'u, TEK kanundan)
'Geçici Madde 1' etiketli 162 parçadan örnekler:
  len=12  '2.1.1961 203'
  len=22  '9.7.1953 6124 Muvakkat'
  len=23  '10.6.1930 1702 Muvakkat'
```

Bunlar madde değil, **tablo hücresi**. İndekste yer kaplıyorlar ve retriever'ın top-k
yuvalarında gerçek maddelerle yarışıyorlar.

### B) Alt-madde soneki kayboluyor — **gerçek maddelerin kimliği çakışıyor**

`2004` (İcra ve İflas) `Madde 309` **27 kez** geçiyor. Bunlar çöp değil, **gerçek ve farklı**
maddeler — sonek `madde_no` alanında değil **metnin içinde** duruyor:

```
'– (Değişik: 28/2/2018-7101/39 md.) İflâsına hükmedilmiş olan bir borçlu…'   ← 309
'/a- (Ek: 17/7/2003-4949/84 md.) Malvarlığının terki suretiyle konkordato…'  ← 309/a
'/b - (Ek: 17/7/2003-4949/84 md.) …'                                          ← 309/b
'/c- …'  '/ç- …'
```

Bu sınıf daha sinsi: **atıf doğrulayıcısı `Madde 309` ile `Madde 309/a`'yı ayırt edemez**, ve
`recall@k` ölçümünde altın `309/a` iken getirilen `309` **isabet sayılır**.

## 3. ⭐ Bu, S1'in (k süpürmesi) sayılarını kirletiyor mu — **HAYIR, ölçüldü**

Kirlilik gerçek ama DEV kümesine az dokunuyor. 80 sorunun altın anahtarı korpusta kaç kez
geçiyor diye bakıldı: **5/80** soruda yinelenen anahtar var (`2004/31` ×2 · `2004/79` ×2 ·
`2004/97` ×2 · `6502/73` ×2).

| alt küme | n | `recall@1` | `recall@5` |
| :--- | ---: | ---: | ---: |
| tüm küme | 80 | 0,4500 | **0,7500** |
| **temiz** (anahtar tekil) | 75 | 0,4533 | **0,7467** |
| yinelenen anahtarlı | 5 | 0,4000 | 0,8000 |

Temiz alt küme tüm kümeyle **aynı** (Δ = 0,0033). → **S1'in k=5 ↔ k=10 kıyası ayakta**,
ölçüm bu kusurdan sistematik yarar görmüyor. *(Ve zaten iki k aynı indekste ölçülüyor.)*

## 4. 🚨 B7'nin mekanizması — #51'e düzeltme

`research_log` #51 B7'yi şöyle kaydetmişti: *"korpusta yürürlük alanı yok, ilga bilgisi yalnız
serbest metnin içinde"*. **Doğru ama eksik.** `İŞ KANUNU Madde 15` → `1475` kaydına bakıldı:

```
1475 korpusta 9 satır. 'Madde 1' ÜÇ kez, 'Geçici Madde 1' İKİ kez geçiyor.
  Madde 15  len=39   '110- (Mülga: 22/5/2003/4857/120 md.) Ek'      ← doğrulayıcının DOGRULANDI dediği kayıt
  Madde 1   len=54   '13/E- (Mülga: 22/5/2003/4857/120 md.) Kıdem tazminatı:'
  Madde 111 len=2199 '112- (Mülga: …) 1475 SAYILI ANA KANUNA İŞLENEMEYEN HÜKÜMLER…'
  Madde 14  len=5934 '– (Değişik birinci fıkra: …) Bu Kanuna tabi işçilerin…'   ← gerçek, yürürlükte
```

Yani doğrulayıcının *"var, doğrulandı"* dediği kayıt **39 karakterlik yanlış ayrıştırılmış bir
parça** — `madde_no` "Madde 15" diyor, metin "110-" ile başlıyor. **İki kusur üst üste binmiş:**
(a) yürürlük alanı yok, (b) eşleşilen kaydın kimliği zaten yanlış. `mulga` alanı eklemek (a)'yı
kapatır, **(b)'yi kapatmaz**.

Ad çakışması da doğrulandı: **9 `kanun_adi` birden fazla `kanun_no` taşıyor**, `İŞ KANUNU` →
`{1475, 4857}` bunlardan biri.

## 5. S2'nin aday kuralı — ölçüldü, sprint'in verify kalemini geçiyor

Naif kural (*"metinde `(Mülga` geçiyorsa mülga"*) **yanlış**: madde bütün olarak yürürlükte
olup yalnız bir **fıkrası** mülga olabiliyor.

| kural | eşleşen madde |
| :--- | ---: |
| `(Mülga` **geçiyor** (naif) | 3.652 |
| baştaki ayrıştırma artığı atıldıktan sonra `(Mülga` ile **başlıyor** | **2.496** |
| **fark = naif kuralın yanlış pozitifi** | **1.156** |

Sprint S2'nin verify kalemi, aday kuralla:

```
1475 / Madde 15  → mulga=True    '110- (Mülga: 22/5/2003/4857/120 md.) Ek'
1475 / Madde 14  → mulga=False   kıdem tazminatı, yürürlükte           ✅
4857 / Madde 15  → mulga=False   yürürlükteki İş Kanunu                ✅ (ad çakışması kanun_no ile çözülüyor)
```

## 6. Ders — ölçüm aracının kendisi de sessizce yanlış olabilir (tuzak 7.1'in tekrarı)

Bu turda **kendi kontrol betiğim** yanlış sayı üretti: `(altin_sirasi or 99) < 5` yazdım;
`altin_sirasi == 0` **falsy** olduğu için 1. sıradaki her isabet **kaçırılmış** sayıldı.
Temiz alt kümenin `recall@5`'i **0,2933** çıktı (gerçek **0,7467**) ve bu sayı *"kirlilik
recall'ı şişiriyor"* diye okunabilirdi — yani bulguyu **ters yönde** doğrulamış görünürdü.
Yakalanma sebebi aritmetik tutarsızlık: 22 + 5 ≠ 60. Hata vermedi, uyarı vermedi.

→ **tuzak 7.5** olarak kaydedildi.

## 7. Hüküm ve sıra

- **S1 etkilenmiyor**, ölçüldü (§3) — k süpürmesi planlandığı gibi koşuyor.
- **S2 büyüyor.** *"`mulga` alanı ekle"* B7'nin yarısını kapatıyor. Diğer yarısı **madde
  kimliği**: alt-madde soneki (`309/a`) `madde_no`'ya taşınmalı ve tablo-parçası satırları
  (sınıf A) korpustan **elenmeli**. İkisi de veri işi, graf değil.
- ⚠️ **İndeks yeniden kurulacak** (korpus değişiyor) — retriever'ın bayat-indeks kapısı zaten
  patlar. Sınıf A elenirse indeks **~1.166 satır küçülür** ve `recall@k` **değişebilir**;
  o yüzden S1'in k süpürmesi **eski korpusta** bitmeden korpusa dokunulmuyor
  (sprint3.md'nin sıra kısıtı, şimdi ikinci bir gerekçeyle daha).

## Paper eşlemesi

**Limitations / Data:** erişim sayıları bir korpusun üstünde ölçülür; o korpusun madde
kimliğinin **%22,7 oranında yinelendiği** ölçülmeden `recall@k` mutlak bir kabiliyet sayısı
gibi okunamaz. **Methodology:** yürürlük tespitinde naif kalıp eşleşmesi ile fıkra/madde
ayrımının farkı (1.156 yanlış pozitif). **Negatif bulgu:** *"korpus temiz"* varsayımı
sınanmamıştı ve tutmadı.
