# #57 — Çekinme aletinin onarımı: M2b'nin paydası modele bağımlıydı

**Tarih:** 2026-08-06 · **Dal:** `asiri-red` · **Commit'ler:** `ff64682` · `0ca4d64` · `c1e99a8`
**Tetikleyen:** Görev 2'nin (rakip modeli ürün rejiminde ölçme) bağımsız incelemesi — 4 kritik + 8 önemli kusur.

> ⚠️ **Birim:** *"puan"* = **yüzde puanı**. Hakem gürültü tabanı `0,3 puan` = `0,003 kesir`.

---

## Manşet

**Bir turda çekinme dedektörü ÜÇ kez değişti ve dördüncüsünde paydanın kendisinin bozuk olduğu
bulundu.** Ölçüm aleti değişikliği CLAUDE.md gereği kayda geçer; bu giriş o kaydı tutuyor.

1. `b8938a6` — red-regex Gemini ailesi için kalibre edildi (kanunun **koşul kipi** yanlış-pozitifi)
2. `334880d` — ADR-0058 **açılış yeterlilik hükmü** BAĞLAYICI sayıldı
3. `ff64682` — açılış hükmü **bağlayıcı olmaktan çıkarıldı** (yanlış-negatif üretiyordu)
4. `ff64682` — 🚨 **`valid_trap` paydası cevaba KÖR hâle getirildi** — asıl bulgu bu

---

## 🚨 K3 — Paydanın modele bağımlı olması

`score_abstention.judge()` hakeme soruyu, kaynağı **ve modelin cevabını** tek çağrıda veriyor,
`source_answers`'ı (= *tuzak geçerli mi*) aynı JSON'da istiyordu. Oysa bir tuzağın geçerliliği
`(soru, bağlam)`'ın fonksiyonudur — hangi modelin skorlandığına bağlı **olamaz**.

**Ölçüm.** `h2b@k=4` sınavı üç kolda **bayt-bayt aynı** (`soru`, `context_shown`, `referans`).
Buna rağmen:

```
valid_traps      3.1 FL 45   ·   3.5 FL 56   ·   BİZ 50        ← aynı sınav, üç ayrı payda
80 kalemin 19'unda üç kol FARKLI source_answers kararı alıyor  (%24)
BİZİM Rej'imiz paydaya göre 12,9 puan oynuyor: 0,746 ↔ 0,840 ↔ 0,875
```

Bu, ön-kayıtlı bir kapı için gürültünün en kötü türü: **sapma yön değiştiriyor.**

⚠️ **Aynı hata #45'te M2/M3 için görülmüştü** ve ADR-0048/0049 ile **ayrı bir betiğe**
(`valid_trap_cache.py` + `rescore_abstention_cached.py`) çözüm yazılmıştı — ama **aletin kendisi
düzeltilmemişti**. Ders: *bir hatayı yan yolda kapatmak, ana yolda açık bırakır.* Yeni koşular
bozuk aleti kullanmaya devam etti ve hata 3 ay sonra rakip kıyasında yeniden çıktı.

**Onarım.** Payda artık ayrı, **cevaba kör** bir çağrıdan geliyor ve **içerik-adresli** bir
önbellekte kalem başına **bir kez** ödeniyor (anahtar `sha256(soru ‖ kaynak[:3500])`).
`{mod}:{id}` anahtarı **kasten kullanılmadı**: aynı `id` farklı koşuda farklı bağlam taşıyabiliyor
(`h2b` k=4 ↔ k=10 tam bu). Payda hakemi ADR-0049 m.2 gereği **`gpt-4o`**; pay (`verdict`) hakemi
**`gpt-4o-mini` olarak KALDI** ve `JUDGE_SYSTEM` **değiştirilmedi** — istem budansa `verdict`
dağılımı da kayardı ve her tarihsel sayı kıyaslanamaz olurdu.

### ⭐ Doğrulama: aynı sınavı paylaşan kollarda payda artık EŞİT

```
h2b@k=4  (BİZ · 3.1 FL · 3.5 FL)      50 / 45 / 56   →   68 / 68 / 68     ✅
m2b distractor (10 koşu)              61 … 80 saçılım →   hepsi 77         ✅
h2b@k=10 (tek kol, kendi sınavı)      51             →   65
```

*(⚠️ düzeltme 2026-08-06, kusur k-1: satır **8 koşu** diyordu, gerçek **10** — cp09 ×3 · cp3-supurme-ham · cp3-supurme-min · cp3c-ta-v1 · cp3e-merge · sprint1 ×3. `mode == "distractor_nogold"` taranarak sayıldı; kürasyon koşuları (cp2c ×4, kontrol_m2b) ölçüm değil, dışarıda. Doğrulama iddiadan güçlüydü, sayım yanlıştı.)*

Önbellek 16 koşuda **250 ayrık** `(soru, kaynak)` kalemi taşıyor; beklenen ayrık sayı da
**250** (eksik anahtar 0). Önbellek olmasa 1225 hakem çağrısı gerekirdi — **975 çağrı ödenmedi.**

---

## 📊 ÇEVİRİ TABLOSU — eski alet → yeni alet

**Bu tablo yayılım borcunun tek kaynağıdır.** Belgelerde geçen eski sayı **silinmez**, yanına
bu tabloya işaret eden bir damga konur.

| koşu / özne | valid_traps eski → yeni | **Rej\* eski → yeni** | Rej(regex) eski → yeni |
| :--- | ---: | ---: | ---: |
| ⭐ `tgta_v1` **M2b (harness KAPALI)** `cp3-supurme-ham` | 65 → **77** | **0,877 → 0,766** | 0,846 → 0,740 |
| ⭐ `tgta_v1` **h2b@k=4 (harness AÇIK, önsözSÜZ)** | 50 → **68** | **0,840 → 0,735** | 0,820 → 0,647 |
| ⭐ `tgta_v1` **h2b@k=4 (harness AÇIK, ÖNSÖZLÜ)** 🆕 | — → **68** | — → **0,809** | — → 0,559 |
| `tgta_v1` h2b@k=10 | 51 → **65** | 0,784 → **0,723** | 0,706 → 0,569 |
| `τ_g` (`m2b_tg_v1_th`) | 61 → **77** | **0,607 → 0,506** | 0,590 → 0,506 |
| `τ_a` (`m2b_ta_v1_th`) | 77 → **77** | **0,987 → 0,987** *(değişmedi)* | 0,987 → 0,987 |
| `tg_ta_min` (norm-dengeli) | 79 → **77** | 0,987 → **0,987** | 0,987 → 0,987 |
| `tg_ta_nb` | 80 → **77** | 1,000 → **1,000** | 1,000 → 1,000 |
| base (cp09 `m2b_base_th`) | 72 → **77** | 0,986 → **0,961** | 0,986 → 0,935 |
| Gemini (cp09 `m2b_gem_th`) | 65 → **77** | 1,000 → **0,883** | 0,969 → 0,818 |
| base (sprint1 `m2b_base`) | 75 → **77** | 0,973 → **0,948** | 0,987 → 0,961 |
| Gemini (sprint1 `m2b_gem`) | 67 → **77** | 0,970 → **0,883** | 0,970 → 0,857 |
| `τ_g` (sprint1 `m2b_tg`) | 80 → **77** | 1,000 → **1,000** | 1,000 → 1,000 |
| 3.1 FL `h2b_fl31_k4` | 45 → **68** | 0,978 → **0,809** | 0,911 → 0,632 |
| 3.5 FL `h2b_fl35_k4` | 56 → **68** | 0,982 → **0,926** | 0,768 → 0,662 |
| `kontrol_m2b` (cp2 hasat) | 1 → **12** | 0,000 → **0,500** | 0,000 → 0,000 |

**16 koşu yeniden puanlandı.** Eski özetler `abst_*_summary.json.ONCEKI-PAYDA` olarak
**silinmeden** yanlarında duruyor.

### Hükümlerin çoğu AYAKTA — ama gerekçelerinin sayıları değişti

- ✅ **ADR-0052 (ham TIES ana sonuç) AYAKTA.** *"Ham TIES `τ_a`'yı silmedi"* kanıtı
  `0,607 → 0,877` idi; yeni aletle `0,506 → 0,766`. **Sıçrama aynı (+0,26).** Hüküm değişmiyor.
- ✅ **#56'nın *"red kapısı ateşlenemiyor"* hükmü AYAKTA.** Kanıt `0,840 < 0,877` idi;
  yeni aletle `0,735 < 0,766`. **İşaret aynı.**
- ✅ **Görev 7 kol kapısı (`M2b Rej ≥ 0,95`) DEĞİŞMİYOR** — referansı `τ_a` = 0,987 ve
  yeniden skorlamada **birebir aynı kaldı** (n=77, önce de sonra da 0,987).
- ⚠️ **Görev 9 kapısı (`M2b Rej ≥ 0,840`) ESKİ ALETİN BİRİMİNDE.** ADR-0050 kuralı:
  *sonucu gördükten sonra eşik değil ALET düzeltilir.* Burada alet düzeltildi → **eşik yeni
  çıpadan yeniden türetilmeli.** Yeni çıpa yazıldı, **eşiğe dokunulmadı** (insan kararı).

### 🚨 Kapanmayan: M2 ve M3'ün paydası HÂLÂ modele bağımlı

Bu tur yalnız `m2b`/`h2b` yeniden puanlandı. `m2` ve `m3` özetleri eski paydayı taşıyor ve
bozukluk orada da görünür durumda — cp09'un **aynı** M3 sınavında:

```
m3_base_th 54  ·  m3_gem_th 56  ·  m3_tg_v1_th 39      ← 17 kalemlik saçılım
```

⚠️ ADR-0048 m.2'ye göre M3'ün paydası **tanım gereği 80/80** olmalı (bağlam boş, kaynak metni
yok) — yani bu üç sayının **üçü de yanlış**. Kapatması hakemsizdir (para gerektirmez).
**Borç.**

---

## Ö2 — Açılış yeterlilik hükmünün bağlayıcılığı yanlış-negatif üretiyordu

`334880d` olumlu açılış hükmünü (*"Verilen kaynaklar soruyu cevaplamaktadır."*) **bağlayıcı**
saymıştı. Yapısal kusur: bu, **modelin kendi beyanını gerçek davranışının önüne koyar** — ve
model hükmü yanlış kurabiliyor. Ölçülen vaka `h2b_fl35_k4` id=5, cevap kendi açılışını cümle
sonunda yalanlıyor:

> *"Verilen kaynaklar soruyu **cevaplamaktadır**. … özel bir madde **bulunmamaktadır** …
> Bu nedenle verilen kaynaklarda bu konuyu düzenleyen **yeterli madde bulunmuyor**."*

**Düzeltilmiş kural:** açılış hükmü bağlayıcı değil; çelişkide **gövde öncelikli** ve gövdenin
hükmünü **son esaslı ibare** taşır. Ayrım ölçülen beş vakanın tam olarak ayrımıdır:

```
çekinme    : olumsuzlama SONUÇ konumunda      "Bu nedenle / Dolayısıyla … bulunmuyor"
dolu cevap : olumsuzlama KARŞITLIKLA çözülmüş  "…bulunmamaktadır; ANCAK … m.80 kapsamındadır"
```

**Etki kapalı ve ölçüldü:** yalnız *"olumlu açılış + gövdede REJECT_RE"* kesişimi davranış
değiştirebilir; tüm `outputs/eval`'da bu kesişim **5 cevap**, **3'ü** çekinmeye döndü (hepsi
`g2-fl-harness/h2b_fl35_k4`, 43 → 46) ve yön **rakibin lehine**. Çıpalarımız
(`olcum-bi` 19 · `olcum-h2b-k4` 44 · `olcum-h2b-k10` 40) **değişmedi**.

⚠️ **Olumsuz kutup bağlayıcı KALDI ve bu bir ölçüm sonucudur:** repo genelindeki **28** olumsuz
açılışlı cevabın hepsi 500 karakterin altında — yani *"yetersiz dedim ama cevapladım"* vakası yok.

### Dedektör sürümlerinin gerçek repo etkisi (rapordaki tarama eksikti)

| geçiş | etkilenen satır | etkilenen dosya |
| :--- | ---: | ---: |
| `v0` (G2 öncesi) → `v2` (`334880d`) | **18** | **11** |
| `v2` → `v3` (`ff64682`, bu giriş) | **3** | **1** |
| `v0` → `v3` (net) | **15** | **11** |

Görev 2 raporu *"tüm `outputs/eval` tarandı"* diyerek **8 dosya** saymıştı; gerçek sayı **11**.
Sayılmayanlar: `cp09/m2b_gem_th` (65→64) · `sprint1/m2b_gem` (67→66) · `g2/h1_fl31` (11→10).

---

## K1 — `reasoning_tokens`: `None` ile `0` karıştırıldı

Künye *"dolu 78/80 · 41/80"* diyordu. Gerçekte sunucu alanı **80/80 bildirmiş**; bazı kalemlerde
değer **gerçekten 0** (model hiç muhakeme yapmamış). Eski ortalamalar yalnız `rt>0` olan
kalemlerin **koşullu** ortalamasıydı.

| koşu | doğru ort (n=80) | medyan | sıfır olan | künyedeki YANLIŞ |
| :--- | ---: | ---: | ---: | ---: |
| `h1_fl31` | **769,6** | 735 | 2 | ~~789,4~~ |
| `h1_fl35` | **445,2** | **198** | **39** | ~~868,8~~ |
| `h2b_fl31_k4` | 626,9 | 596 | 0 | — |
| `h2b_fl35_k4` | **454,4** | 344 | 38 | ~~865,6~~ |

🚨 **OZET'teki *"3.5 FL daha çok muhakeme harcıyor"* cümlesi TERSİNE YANLIŞTI** ve kaldırıldı:
3.5 FL, 3.1 FL'in **%42 azını** harcıyor. Gerçek şekil **iki kutuplu**: 39 kalemde 0, 8 kalemde
kaçak (1103-1475).

## K2 — Muhakeme bütçesi rakip tarafında UYGULANMIYOR

Kesik kalemlerin muhakeme token'ları `fl35 [1473,1103,1475,1405,1472,1473,1470,1472]` ·
`fl31 [1157,1267,1222]` — **hepsi 1024'ün üstünde**, görülen en büyük **1475**.
`extra["reasoning"]={"max_tokens":1024}` sağlayıcı tarafından **yok sayılıyor**; tek bağlayıcı
sınır `max_tokens=1536`. **Rakipte muhakeme cevabın 512'lik payını yiyor**; bizde ADR-0043
gereği ayrık bütçe + zorunlu kapanış var.

→ *"Bütçe eşleşik"* **yanlıştı**: **nominal** bütçe aynı, **etkin** bütçe değil. ADR-0057
anlamında bir eksen uyuşmazlığı. **Ve 3.5 FL'ın %10 kesikliğinin gerçek sebebi budur —
modelin özelliği değil, rejimin.**

## Ö1 — Kesiklik şerhinin yönü ölçülmeden yazılmıştı, ve tersti

| | kütle (80) | kütle (n=68 ortak kesiksiz) | Δ |
| :--- | ---: | ---: | ---: |
| BİZ | 0,6275 | **0,6579** | **+3,0 p** |
| 3.1 FL | 0,6172 | 0,6516 | +3,4 p |
| 3.5 FL | 0,6948 | 0,7002 | **+0,5 p** |

Kesikliği kaldırmak **bize 3.5 FL'dan 6 kat çok yarıyor**; fark **6,7 → 4,2 puana daralıyor**.
Yani hüküm *"muhafazakâr"* değil, **bizim aleyhimize** eğilimliydi. Artık her sayı **hem 80'de
hem n=68'de** raporlanıyor; kol düşürülmedi (kesiklik K2 gereği rejimin kusuru, kolun değil).

## Ö7 — `$/cevap` yalnız çıktıydı; girdi dahil edilince sıralama TERSİNE dönüyor

Girdi token'ı **ölçüldü** (OpenRouter'a aynı istem gönderilip `usage.prompt_tokens` okundu —
tahmin değil): h1 için **2471** token.

| | girdi $ | çıktı $ | **toplam $/cevap** |
| :--- | ---: | ---: | ---: |
| 3.1 FL | 0,000618 | 0,001456 | **0,002074** |
| 3.5 FL | 0,000741 | 0,001434 | **0,002175** |

3.5 FL yalnız çıktıya bakılınca **%1,5 ucuz**, girdi dahil edilince **%4,9 pahalı**.

---

## Küçük düzeltmeler

- **"Çekinme milimetre oynamadı"** toplam eşitliğinden kurulmuştu. Kalem düzeyinde örtüşme
  **8/10** (Jaccard 0,667): yalnız 3.1 FL `[43,59]`, yalnız 3.5 FL `[0,21]`. Doğru okuma:
  *aşırı-red **oranı** değişmedi, **hangi kalemlerde** olduğu değişti.*
- **Gürültü tabanı eksen karıştırıyor.** `0,3 puan` **A1** için ölçüldü; *"22/26 katı"*
  çarpanları **kütle** üzerinde kurulmuş. Kütle = coverage × A1 ve coverage'ın kendi varyansı
  o tabanda yok → çarpanlar **üst sınırdır**, ölçü değil.
- **Kendi karşıolgumuz damgasızdı** (*"aşırı-red kapatılsa %72,0"*). **TAVAN/VARSAYIMSAL**
  damgası basıldı: (a) çekinilen 19 kalem sınavın **en zor** ucu, cevaplanan A1'i onlara
  uygulamak seçim yanlılığını yok sayar; (b) `0,875` paydası altın **gelmeyen** 10 kalemde de
  doğru cevaplamayı gerektirir, tek-altın yer-gerçeğinde onlar **0** alır.
- **Künye koşan kodu tarif etmiyordu:** dört koşuya da `334880d` yazılmıştı, oysa o commit
  **dört koşudan da sonra** atıldı. Gerçek: dördü de `d88786c`, `h2b_fl31_k4` ayrıca
  **commit edilmemiş ağaçla** koştu. Rejim etkilenmedi (yalnız retry sarmalayıcısı).
- **Önbellek yazımı kayıpsız yapıldı** (`flock` + `os.replace`). Bu turda kayıp **olmadı**
  (skorlama sıralıydı) ama kusur gerçek: kilitsiz sürümde 8 eşzamanlı süreçte **2 kalem
  sessizce kayboldu** ve 2 süreç yarım JSON okuyup çöktü. Test kilitsiz sürümde **düştüğü
  doğrulanarak** eklendi.

---

## Ö5 — M2b ekseni EŞLEŞTİ (yerel koşu, $0)

Bizim M2b çıpamız önsözsüzdü, G2'nin dört FL koşusu önsözlüydü → M2b satırı ADR-0057 gereği
**TANIMSIZ** damgalıydı. Kapatıldı: `outputs/eval/g2b-m2b-onsozlu/`, önsözlü `h2b@k=4`,
80/80, **kesik %0,0** (geçerlilik kapısı geçildi), zorunlu kapanış 55/80.

```
Ö5 önsözlü M2b:  valid_traps = 68 · Rej* = 0,809 · Rej(regex) = 0,559
```

⚠️ Koşu **pilde** başladı (GPU 32 W'a kısıldı, ~9 tok/s; çıpa koşusu şarjdayken 42 tok/s).
Ölçümü etkilemez (`temperature=0`, `seed=3407`), yalnız süreyi — künyeye yazıldı.

---

## Bütçe — bu onarımın bedeli

| kalem | tutar | kaynak |
| :--- | ---: | :--- |
| kör payda hakemi (`gpt-4o`, 250 ayrık kalem, **bir kez**) | **$0,8021** | özetlerdeki `gecerlilik_maliyet_usd` |
| pay hakemi (`gpt-4o-mini`, 16 koşu) | ~$0,29 | `judge_cost_usd` |
| girdi-token ölçümü (Ö7, 160 çağrı) | ~$0,09 | ölçüm koşusu |
| **TOPLAM** | **~$1,18** | ⚠️ **plansız** — tur defterinde karşılığı yoktu |

Önbellek olmasaydı payda 1225 çağrı ederdi (≈ **$3,93**); **$3,13 tasarruf**.

---

**Ders (bu hattın tekrar eden hata sınıfı):** *ölçüm aletinin bir kolunu düzeltip diğerini
bırakmak, hatayı kapatmaz — taşır.* ADR-0048 paydayı yan bir betikte düzeltti, ana alet bozuk
kaldı ve aynı hata üç ay sonra rakip kıyasında yeniden çıktı. Alet düzeltmesi **aletin
kendisinde** yapılır.
