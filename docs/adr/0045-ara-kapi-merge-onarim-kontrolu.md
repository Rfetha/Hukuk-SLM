# ADR-0045 — ARA KAPI'ya **merge onarım kontrolü** eklendi · ön-kayıtlı eşik değişmedi

**Statü:** Yürürlükte · **Tarih:** 2026-07-29
**Otorite belge:** `sprint2.md` CP3 · `TASARIM.md` §7 (kapılar)
**İlgili:** ADR-0037 (Kapı 5) · ADR-0042 (tek havuz) · **ADR-0043** (bütçeli düşünce — bu ADR'nin sebebi) ·
ADR-0036 (rejim eşleşmesi) · ADR-0027 (kol tanımı: her kol **ham base**'den)
**Kanıt:** `research_log` [#43](../record/research_log/2026-07-29-cp09-butceli-dusunce-cipalari.md)

> ## ⚠️ ÖN-KAYIT ŞERHİ — bu ADR'nin savunmasının tamamı
> Değişiklik **2026-07-29'da**, `τ_a` **henüz eğitilmemişken**, **hiçbir merge hücresi
> üretilmemişken** ve **hiçbir taban koşulmamışken** yapıldı. Eklenen kontrolün uygulanacağı
> veri **henüz yoktur**. Ön-kayıtlı **eşik sayısına dokunulmadı** (M2 ≥ 0.934 · muhafız ≥ 0.888);
> yalnızca **ikinci bir gözlem** eklendi ve **yorum kuralı önceden yazıldı.**

---

## Bağlam — kapı, ölçmek için kurulduğu şeyi ölçemez hâle geldi

ARA KAPI, `τ_a`'nın *"birleştirmeye değer bir çekinme kolu"* olup olmadığını **CP4-CP5'e ~$12
harcamadan önce** sınamak için kuruldu. Ön-kayıtlı biçimi: **`M2 Rej ≥ base + 12 puan`**.

Formül, `τ_g`'nin çekinmeyi **base'in altına** düşürdüğü thinking-off dünyasında yazılmıştı
(0.633 → 0.458). CP0.9 iki şeyi birden değiştirdi:

**1. Base bütün çekinme modlarında tavana yaklaştı.**

| mod | base (bütçeli) | tavana kalan | `+12 puan` |
| :--- | --: | --: | :--- |
| M2 | 0.814 | 0.186 | mümkün ama kalan boşluğun **%65'ini** yer |
| M2b | 0.986 | 0.014 | **imkânsız** |
| M3 | 1.000 | 0 | **imkânsız** |

**2. `τ_a`'nın onaracağı delik kendi üstünde değil.** ADR-0027 gereği her kol **ham base**'den
eğitilir; `τ_a` yola 0.814/0.986/1.000'den çıkar. Delik **`τ_g`'de**: M2b **0.986 → 0.607**
(fabrikasyon 0.393), üstelik tam `τ_g`'nin eğitim ailesinde (RAG_MULTI).

Yani `τ_a`'yı **tek başına** ölçmek, sorulmak istenen soruyu sormuyor. Sorulmak istenen soru:
***`τ_a`, `τ_g` ile birleştiğinde o deliği onarıyor mu?***

## Karar

### 1. Ön-kayıtlı eşik **AYNEN DURUYOR**

```
τ_a TEKİL  ·  M2 Rej ≥ 0.934   (base 0.814 + 12 puan)
             M1 A1  ≥ 0.888   (0.90 × base 0.986)
```

Veri görüldükten sonra eşik gevşetmek, kapının bütün anlamını yok eder. **Tavan riski
şerhiyle birlikte raporlanır**, değiştirilmez.

### 2. Yanına **merge onarım kontrolü** eklenir

CP3'te `τ_a` eğitildikten sonra, **`τ_g` + `τ_a` 2-yollu merge** DEV'de koşulur ve **M2b**
okunur. Maliyeti neredeyse sıfır: `TASARIM.md`'nin kendi ifadesiyle *"merging itself costs no
training compute"* — bir merge (host RAM, akıtmalı) + bir Q4_K_M + bir DEV koşusu = **GPU $0,
hakem ~$0.15**.

Rejim: **norm-dengeli TIES** (ADR-0036'nın ana ayarı) · aynı taşıyıcı · aynı değişmezler.
Bu **DEV** ölçümüdür; dondurulmuş CANON'a dokunulmaz.

### 3. Yorum kuralı — **şimdi yazıldı, sonuç görülmeden**

| tekil M2 ≥ 0.934 | merge M2b onarımı | karar |
| :--- | :--- | :--- |
| ✅ | ✅ | **Güçlü yeşil** — CP4-CP5 koşulur |
| ❌ | ✅ | **Devam** — kapı tavan-sınırlıydı; gerekçe merge kanıtıdır ve **açıkça öyle raporlanır** |
| ✅ | ❌ | **DUR** — kol tek başına iyi ama birleşince taşımıyor; iç iddianın öncülü sorunlu |
| ❌ | ❌ | **DUR** — `τ_a` rejimi düzeltilir (epoch · lr · çift sayısı), rakiplere para harcanmaz |

**"Onarım" ne demek — ön-kayıtlı:** merge hücresinin M2b'si **`τ_g`'nin 0.607'sinden anlamlı
biçimde yukarıda ve base'in 0.986'sının %90'ının üstünde** olmalı → **M2b ≥ 0.887**.
*(0.90× çarpanı ARA KAPI'nın muhafız formülüyle aynı; yeni bir sabit uydurulmadı.)*

> ## 🚨 2. GÖZLEMİN HÜKMÜ — ÜÇ KEZ TÜRETİLDİ, SON HÂLİ **DÜŞTÜ** (2026-08-06)
>
> Ön-kayıtlı olan **formül** (`base M2b × 0.90`); sayı, base'in o günkü ölçümünden türer.
> ⛔ ADR-0050 gereği çarpana, formüle ve eşiğe **hiç dokunulmadı** — yalnız yeniden türetildi.
>
> | tarih | base M2b | eşik | merge (ham TIES) | hüküm |
> | :--- | ---: | ---: | ---: | :--- |
> | 2026-07-29 (bu ADR) | 0,986 *(cevaba bağlı payda)* | 0,887 | — | ön-kayıt |
> | 2026-07-30 ([#46](../record/research_log/2026-07-30-cp2r-kor-payda.md), klip 900) | 0,949 | 0,8541 | 0,877 | ✅ GEÇTİ |
> | **2026-08-06 (yürürlükte, K3+K-1)** | **0,961** | **0,8649** | **0,766** | **🔴 DÜŞTÜ (−9,9 p)** |
>
> Eski 0,887 eşiğine karşı da **düşüyor**. Paydalar eşit (77 ↔ 77) → kıyas geçerli.
> Ortadaki satır emekli bir aletin sayısıdır (900 klipi kategori hatası — #46'daki damga).
>
> **Yorum kuralının uygulanması:** ~~1. gözlemin paydası bu dalgada onarılmadı → satır ya
> `✅ ❌` ya `❌ ❌`~~ → **ÖDENDİ VE TÜRETİLDİ (KARAR-3, 2026-08-06, hakem $0,1054).**
> *"Güçlü yeşil"* okuması bugünkü ölçümle **yoktur** ve CP4-CP5 harcaması bu kapıdan
> **yetki almıyor**.
>
> Türetme: `outputs/eval/cp2-r-kor-payda/ara_kapi_esikleri_2026-08-06.json` ·
> `outputs/eval/karar3-m2-payda/m2_payda_2026-08-06.json` ·
> [#58](../record/research_log/2026-08-06-payda-tekillesmesi.md) ·
> [#59](../record/research_log/2026-08-06-m2-paydasi-ve-karar-4.md)

> ## ✅ 1. GÖZLEMİN HÜKMÜ — TÜRETİLDİ, **GEÇTİ** (2026-08-06, KARAR-3)
>
> `m2` paydası on koşuda birden yeniden ödendi (aynı 70 kalemlik sınav; payda **55-63 → 66/70**,
> her kolda **eşit** — kendi kendini doğrulayan sınav). Ön-kayıtlı olan **formül**; sayı bugünkü
> base ölçümünden türer. ⛔ ADR-0050 gereği eşiğe/çarpana/formüle **hiç dokunulmadı**.
>
> | bacak | formül | çıpa | eşik | `τ_a` tekil | hüküm |
> | :--- | :--- | ---: | ---: | ---: | :--- |
> | M2 Rej | `base M2 + 0,12` | base **0,803** | **0,923** | **0,955** | ✅ **GEÇTİ** (+3,2 p) |
> | muhafız M1 A1 | `0,90 × base A1` | base **0,9777** | **0,8799** | **0,9697** | ✅ **GEÇTİ** |
> | *(ön-kayıtlı ham sayılara karşı)* | — | — | 0,934 · 0,888 | 0,955 · 0,9697 | ✅ **ikisi de** |
>
> 🚨 **Bu ✅ ilk kez BİRİM-TUTARLI.** Sprint 2 kapanışındaki `0,984 ≥ 0,923` kıyası **karışık
> birimdeydi**: pay özneye bağlı paydadan (63/70), eşik [#46](../record/research_log/2026-07-30-cp2r-kor-payda.md)'nın
> kör çıpasından geliyordu. Şimdi iki taraf da aynı aletten okunuyor.
>
> ### § 3'ün ön-kayıtlı tablosunda satır: **`✅ ❌` → DUR**
> Tablonun kendi metniyle: *"Kol tek başına iyi ama birleşince taşımıyor; iç iddianın öncülü
> sorunlu."* Türetme hükmü **değiştirmedi** (iki olası satırda da DUR'du) ama **hangi** satır
> olduğunu belirledi — ve bu teşhis: sorun `τ_a`'nın kalitesi **değil**, merge'in onu
> **taşımaması**. Kapının §Sonuç'ta vaat ettiği *"kaldı ama neden kaldı"* teşhisi tam bu.

### 4. CP2 hasadı **iki tipi birden** toplar

`rejected` havuzu artık hem **M2-tipi** (tuzak madde **verilmiş**, kaynak soruyu cevaplamıyor)
hem **M2b-tipi** (gold **hiç yok**, yalnız distractor) negatifleri içerir. Gerekçe: `τ_a`'nın
iki eksende de çalışması gerekiyor ve ADR-0042'nin **tek havuz** kuralı gereği aynı veri
`τ_a` · Taban A · Taban B'nin ikinci aşamasına gider. Karışım oranı ve her tipten kaç örnek
kabul edildiği **künyeye yazılır**.

## Değerlendirilen alternatifler

| eleme | gerekçe |
| :--- | :--- |
| **Eşiği tavan-duyarlı hâle getirmek** (`base + 0.50 × (1 − base)` = 0.907) | Metrik olarak daha dürüst, ama **veri görüldükten sonra ön-kayıtlı sayıyı değiştirmek**. Kapının kredibilitesi tam olarak dokunulmamış olmasından geliyor |
| **Bileşik ölçüte geçmek** (`min(M2, M2b)`) | `τ_g`'nin açığını güzel yakalıyor (0.607) **ama** base'i 0.814'e sabitlediği için aynı tavan sorununu geri getiriyor — sorunu çözmüyor, taşıyor |
| **ARA KAPI'yı M2b'ye taşımak** | base 0.986 → `+12 puan` **matematiksel olarak imkânsız**; kapı tanımsız hâle gelir |
| **Kapıyı tamamen kaldırmak** | ~$12'lik taban eğitimlerine sonucu bilinmeyen bir deneye peşin yatırım demek; kapının var oluş sebebi bu |
| **Merge kontrolünü Sprint 3'e bırakmak** | Kapının koruduğu para **Sprint 3'ten önce** harcanıyor. Kontrolü sonraya bırakmak, sigortayı kaza sonrası yaptırmaktır |

## Sonuç — kabul edilen bedeller

- **Kapı artık iki gözlemli**, yani daha karmaşık. Karşılığında *"kaldı ama neden kaldı"*
  sorusu **teşhis edilebilir** hâle geliyor — tek gözlemli hâlinde edilemiyordu.
- **Merge, Sprint 3'ten önce bir kez koşuluyor.** Bu bir kafes hücresi **değil**, bir kapı
  ölçümüdür ve **DEV**'de yapılır; Sprint 3'ün 8 hücresi ayrıca ve aynı protokolde koşulur.
  ⚠️ Aynı merge tekrar Sprint 3'te üretilirse **aynı rejimle** üretilmeli (ADR-0036).
- **`τ_a` kalırsa** ve merge de onarmazsa, iç iddianın öncülü sorgulanır — bu **negatif bulgu
  olarak birinci sınıftır** ve Sprint 3 açılmadan öğrenilmiş olur.
- `runs=1`, güven aralığı yok — Kapı 5/6 ile aynı sınır.
