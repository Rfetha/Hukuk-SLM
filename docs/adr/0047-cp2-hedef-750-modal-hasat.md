# ADR-0047 — CP2 hedefi **750 negatif** · hasat **Modal'da**, taşıyıcı değişmeden

**Statü:** Yürürlükte · **Tarih:** 2026-07-30
**Otorite belge:** `sprint2.md` CP2-c · **değiştirir:** `TASARIM.md` §4.1.1 (`τ_a` rejimi)
**Kapatır:** [ADR-0046](0046-cp2-kabul-olcutu-hakem-ve-havuz-on-elemesi.md) m.5 (hedef sayı açık kalemi)
**İlgili:** ADR-0042 (on-policy `rejected`) · ADR-0043 (bütçeli düşünce) · ADR-0045 (ARA KAPI) ·
ADR-0036 (norm-dengeli merge) · ADR-0037 (Kapı 5, taban adaleti)
**Kanıt:** `outputs/eval/cp2-rejected-hasat/KUNYE.json` (11,12 s/üretim · verim %5,0) ·
`research_log` [#44](../record/research_log/2026-07-30-cp05-cp1-cp2-zemin.md)

> ## ⚠️ ÖN-KAYIT ŞERHİ
> Karar **hiçbir hasat başlamadan**, `τ_a` eğitilmemişken, ARA KAPI'nın hiçbir sayısı
> okunmamışken verildi. **ARA KAPI'nın eşiklerine dokunulmadı** (M2 ≥ 0.934 · M1 A1 ≥ 0.888 ·
> merge M2b ≥ 0.887). Değişen: eğitim çiftlerinin **sayısı** ve hasadın **koştuğu donanım**.

---

## Bağlam — süre yapısal bir engel hâline geldi

Pilot iki sayı ölçtü: **11,12 s/üretim** ve gerçek verim **%5,0** (ADR-0046'nın ön-elemesiyle
tahminen %8,6). Hasat **tek akışta** koşuyordu — `llama-server` `-np` bayrağı olmadan tek slotla
açılıyor, yani 4B Q4_K_M modeli RTX 5070'te GPU'yu doyurmuyor. Sonuç:

| hedef | yerel seri |
| --: | --: |
| 1.495 | **54 sa** |
| 500 | 18 sa |
| 400 | 14 sa |

Bu süreler yürütülebilir değil. İki gerçek kaldıraç var — **paralellik** ve **hedef sayısı** —
ve bir sahte kaldıraç: **sentetik veri.**

### ❌ Sentetik `rejected` neden bir seçenek değil

`rejected`'ın tanımı: *bu modelin gerçekten yapacağı hata.* CP2'nin var oluş sebebi, eldeki
havuzun **emekli 12B hattının** fabrikasyonları olması — yani başka bir modelin hataları.
API'den (GPT/Gemini) üretmek **üçüncü bir modelin** hatalarını verir: aynı kusurun daha kötüsü.

Dahası ADR-0042 bu itiraza karşı CP5'e bir **on-policy kontrol koşusu** ($0,65) koydu. `rejected`
sentetik olursa o sigorta ana koşuya döner ve *"tabanı/kolu yanlış veriyle eğittiniz"* itirazı
**Kapı 5'in tamamını** çürütür. Sentetik veri "ucuza aynı şey" değil, **"ucuza yanlış şey"**.

> API'nin meşru yeri zaten planda: **ön-eleme** (ADR-0046 m.2) ve **kabul hakemi** (m.1). Bunlar
> veri *üretmez*, veri *seçer*. `chosen` tarafı da öğretmen-üretimi olabilir ve zaten öyledir —
> kusur `chosen`'da değil, `rejected`'da.

---

## Karar

### 1. Hedef negatif sayısı: **750** (1.495 değil)

| hedef | `τ_a` çift | 3 epoch adım | 5 epoch adım | Modal $ |
| --: | --: | --: | --: | --: |
| 1.495 | ~1.794 | **82** *(mevcut rejim)* | — | ~5,7 |
| **750** | **~937** | 44 | **~73** | **~3,0** |
| 500 | ~625 | 29 | 49 | ~2,1 |

**750 + 5 epoch → ~73 adım**, ön-kayıtlı 82'ye yakın. 500'de adım 29'a inerdi ve ARA KAPI
kalırsa *"kol mu kötüydü, 29 adım mı yetmedi"* **ayrılamaz** hâle gelirdi — kapı yine ölçmek için
kurulduğu şeyi ölçemezdi (ADR-0039 ve ADR-0045'in başına gelen). 1.495 rejimi korurdu ama kalan
bütçenin (~$22,9) dörtte birini yerdi ve CP4-CP5 zaten ~$12 istiyor.

⚠️ **Epoch 3 → 5 bir rejim değişikliğidir** ve `τ_a`'nın aşırı-uyum riskini artırır. Kabul edilen
bedel: **`‖τ_a‖_F` koşulsuz ölçülür ve raporlanır** (ADR-0036 zaten bunu emrediyor), ve DEV'de
seçim yapılır. Aşırı-uyum belirtisi görülürse epoch 3'e döner, adım 44 olarak raporlanır.

### 2. Hasat **Modal**'da koşar — taşıyıcı **DEĞİŞMEZ**

```
llama.cpp + Q4_K_M GGUF          ← taşıyıcı, aynen
-np 32 (yerel -np yok: tek slot) ← değişen tek şey
A100 40GB                        ← 4B Q4_K_M ağırlık 2,5 GB; hibrit mimaride KV ucuz
```

> ### 🚨 vLLM/bf16 **kullanılmaz**
> Hasat, kolların **dağıtılacağı** kiple aynı olmalı. bf16'da üretilen negatifler Q4_K_M modelinin
> hataları değil, başka bir sayısal modelin hatalarıdır — ADR-0042'nin on-policy gerekçesi yine
> çürür. Nicemleme davranışı değiştirir; bu hattın tamamı zaten o davranışı ölçmek üzerine kurulu.

**Beklenen:** ~1,4 saat · ~$3,0. ⚠️ **Tahmin, ölçüm değil.** llama.cpp yüksek batch'te vLLM gibi
ölçeklenmez; `-np 32` muhtemelen 32× değil **10-20×** verir.

### 3. Koşunun **ilk 10 dakikasında** gerçek verim ölçülür — tahmin tutmazsa durur

Huni çıktısı (`saniye_per_uretim`) ilk 10 dakikada okunur ve kalan süre yeniden hesaplanır.
Tahminin **2 katını** aşıyorsa koşu **durdurulur**, sayı negatif bulgu olarak yazılır, hedef ya da
donanım yeniden karara bağlanır. *Para akarken tahmine güvenilmez* — `fla-core` dersi (#40) ve
CP0.5 aynı şeyi söylüyor: **kazanç ölçülmeden yazılmaz.**

### 4. Sıra bozulmaz: **CP2-a kapısı önce**

Modal'a para göndermeden önce ADR-0046 m.3'ün uyum kapısı ($0,004) koşar. Kapı kalırsa ön-eleme
yapılmaz, verim %5,0'da kalır ve **bu ADR'nin süre/maliyet tablosu geçersizdir** — hedef yeniden
konuşulur.

### 5. ADR-0046 m.5'ten sapma — açıkça

m.5 *"hedef sayı ön-elemenin çıkardığı geçerli tuzak sayısından sonra"* diyordu. Karar **öncesine**
alındı çünkü belirleyici kısıt geçerli tuzak sayısı değil **duvar saati ve maliyet** çıktı.

**Koşullu geri alma:** ön-eleme, 750 negatife ulaşmaya yetecek geçerli tuzak bırakmıyorsa
(kabaca ≥ 8.700 geçerli tuzak gerekiyor — 750 ÷ %8,6), hedef **otomatik olarak** o sayının
elverdiği seviyeye iner ve `sprint2.md`'ye şerhle yazılır.

---

## ✅ 2026-07-30 — m.2 ÖLÇÜMLE DOĞRULANDI, geri-dönüş şıkkı kapandı

Modal payı kalmayınca (bkz. `yurutme-tuzaklari` **6.3**: defter iki cüzdanı topluyordu, gerçek
Modal kalanı **$7,27**'ydi) bu ADR'nin geri-dönüş şıkkı — *"yerel `-np 8`"* — denendi ve **elendi**.

`cp2_harvest.py` eş zamanlı üretime alındı, `llama-server` 8 slotla açıldı:

| | s/üretim | kazanç |
| :--- | --: | --: |
| seri | 11,12 | — |
| `-np 8` | **8,23** | **1,35×** *(beklenen 4-6×)* |

**Sebep:** zorunlu kapatma **9/9**. Her üretim iki istek; ikincisi 3.933 karakterlik izi baştan
**prefill** ediyor ve o compute-bound iş slotlar arası ölçeklenmiyor. Düzeltilemez — `</think>`'in
kapanmaması #42'de ölçülmüş bir base özelliği, zorunlu kapatma ADR-0043'ün rejim değişmezi.

Yerelde 750 negatif = **17,1 saat**. Hasat `load_done` ile devam ettirilebilir olsa da iki geceye
bölmek makul değil.

**Karar:** hasat **Modal'da kalır** (m.2 aynen). Zamanlama değişti — Modal fatura dönemi
**1 Ağustos**'ta yenilenip $42,50 açılınca koşulacak. Tahmini **1,5-3 saat / $3-6** (yerel verimden
türetildi; m.3'ün **ilk 10 dakika kapısı** bunu denetler).

**m.1 (hedef 750) ve `τ_a` rejimi (~73 adım / 5 epoch) DEĞİŞMEDİ** — bekleme, ön-kayıtlı hiçbir
sayıya dokunmadan hedefi korumanın yolu oldu.

---

## Reddedilen seçenekler

| seçenek | neden reddedildi |
| :--- | :--- |
| **Sentetik `rejected` (API)** | Üçüncü bir modelin hataları → ADR-0042'nin düzeltmek için var olduğu kusurun daha kötüsü; CP5'in on-policy sigortasını **bize karşı** çevirir, Kapı 5'i çürütür |
| **vLLM / bf16 ile Modal'da hızlı üretim** | Taşıyıcı değişir → negatifler dağıtılan modelin hataları olmaz; nicemleme davranışı değiştirir |
| **Yerel `-np 8` ile koş** | ✅ **2026-07-30'da ÖLÇÜLDÜ ve ELENDİ:** kazanç 4-6× değil **1,35×** (zorunlu kapatma 9/9 → ikinci istek izi baştan prefill ediyor). 750 hedefte **17,1 saat**. Geri-dönüş şıkkı **kapandı** |
| **Hedef 1.495'te kalsın** | Modal'da ~$5,7 = kalan bütçenin dörtte biri; CP4-CP5 ~$12 istiyor. 750 + 5 epoch, 82 adımın **%89'unu** ~yarı fiyata veriyor |
| **Hedef 500'e insin** | Adım 29'a iner → ARA KAPI kalırsa *"kol mu kötü, veri mi az"* ayrılamaz; kapı ölçemez hâle gelir |
| **Düşünce bütçesini hasatta düşür** | ADR-0043 rejim değişmezi; hasat dağıtım kipiyle aynı olmalı, yoksa on-policy gerekçe kendi künyesince çürür |

## Sonuçlar

- ✅ Süre **54 sa → ~1,4 sa**, maliyet **$0 → ~$3,0**.
- ✅ Taşıyıcı, düşünce bütçesi, seed, klip ve ARA KAPI eşikleri **değişmedi**.
- ⚠️ `τ_a` rejimi **82 → ~73 adım** ve **3 → 5 epoch**. `TASARIM.md` §4.1.1 güncellenir;
  `‖τ_a‖_F` ve aşırı-uyum belirtileri koşulsuz raporlanır. **Limitations'a girer.**
- ⚠️ Modal süre/maliyet **tahmin**; ilk 10 dakikada doğrulanır, 2× sapmada koşu durur.
- ⚠️ Hasat artık yerel değil → **künyeye Modal image sha, `-np` değeri ve gerçek verim yazılır**.
- ⏳ ADR-0046 m.3'ün uyum kapısı hâlâ **açık**; kalırsa bu ADR'nin tablosu geçersizdir.
