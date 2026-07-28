# Açık sorular — canlı sicil

> **Bu belge ne:** kararlaşmamış ama **kararlaşması gereken** sorular, her biri gerekçesi ve
> seçenekleriyle. Konuşa konuşa netleşecekler; netleşen soru buradan **silinmez**, cevabı ve ADR
> numarası yazılıp `✅ KAPANDI` işaretlenir — hangi soruyu ne zaman neye göre cevapladığımız
> makale malzemesi.
>
> **Otorite:** [`TASARIM.md`](../TASARIM.md) · **numaralandırma** onun §13'ünden devam eder
> (1-7 orada, 8'den itibarısı burada). §13 donmuş kayıt, **canlı liste burası.**
>
> **Kural:** bir soru veriye bakılarak cevaplanacaksa, **cevap kuralı veriden ÖNCE** yazılır.
> Sonra yazılan kural rasyonalizasyondur (pre-registration mantığı, `TASARIM.md` §7).

---

## 8. Tekil kafes hücreleri de TIES hattından geçecek mi? — ✅ **KAPANDI (2026-07-28)**

> ### CEVAP: **B — aynı hat**, artı bir `τ_g` düz kontrol hücresi.
>
> | hücre | nasıl üretilir | ne söyler |
> | :--- | :--- | :--- |
> | `τg` tek · `τa` tek | **aynı hat** — budama + o ayarın normalizasyonu + `λ` | çiftle **kıyaslanabilir** |
> | `τg+τa` | aynı hat | çatışma |
> | **`τg` DÜZ (kontrol)** | `λ=1`, budama yok, normalizasyon yok | 🔵 **budama + normalizasyonun kendi hasarını ayrı ölçer** |
>
> **Gerekçe.** Tekilin varlık sebebi **atıf**: `τg+τa` düşükse sebep çatışma mı, kol mu?
> Bu kıyasın anlamlı olması için tekil ile çiftin **aynı işlemlerden** geçmiş olması gerekir —
> yoksa aradaki fark üçüncü bir şeyi (budamanın/normalizasyonun hasarını) de içerir ve
> ayrıştırılamaz. B bunu garanti eder.
>
> **Neden bir de düz kontrol.** ADR-0036 ile hat artık *budama + normalizasyon* içeriyor;
> normalize edilmiş bir tekil hücre *"τ_g tek başına ne satın aldı"* sorusunu değil,
> *"τ_g'nin YÖNÜ, λ büyüklüğünde ne satın aldı"* sorusunu cevaplıyor. Düz kontrol farkı
> görünür kılar. **Yalnız `τ_g` için** — hasarın en görünür olacağı yer o (büyük norm, 1.083 adım)
> ve adaptör zaten elimizde: **ek eğitim yok, tek bir eval.**
>
> **Bedel:** kafes 3 → **4 hücre**, ADR-0036'nın iki ayarıyla **8 eval koşusu.** Merge bedava,
> eval değil — kabul edildi.

<details>
<summary>Kararın alındığı andaki soru (kayıt için korunuyor)</summary>

**Soru.** Kafesin tekil hücreleri (`τg tek`, `τa tek`) nasıl üretilecek — **düz adaptör**
(`λ=1`, budama yok) mı, yoksa çoklu hücrelerle **aynı merge hattından** geçmiş mi?

**Neden önemli.** Tek vektörde TIES'ın ② işaret-seçimi ve ③ ayrık-ortalama adımları anlamsız
(seçilecek çatışma yok); geriye yalnız ① budama + `λ` ölçeği kalıyor. Yani iki seçenek **farklı
sayı üretir.** Ve tekiller kafeste bir süs değil, **atıf aracı**: `τg+τa` düşük çıkarsa sebebin
"merge çatışması" mı yoksa "kol zaten öğrenememiş" mi olduğunu ancak tekile bakarak ayırıyoruz
(`TASARIM.md` §4.3). Tekil farklı bir hattan geçerse aradaki fark **üçüncü bir şeyi** de içerir:
budamanın kendi hasarını.

| seçenek | sonuç |
| :--- | :--- |
| **A — aynı hat** (tekil de budanır + `λ` uygulanır) | Fark yalnız *çatışmadan* gelir; atıf temiz. Ama "kolun tek başına ne öğrendiği" budanmış hâliyle ölçülür |
| **B — düz adaptör** (`λ=1`, budamasız) | Kolun ham yeteneği görünür. Ama `τg` → `τg+τa` düşüşü *çatışma + budama* karışımı olur, ayrıştırılamaz |
| **C — ikisi de** (ekstra hücre) | Budamanın hasarını **ayrı ölçer**; maliyeti yalnız eval (merge bedava) |

**İlk eğilim:** A — atfedilebilirlik en pahalı şeyimiz. C teknik olarak en bilgilendirici ve
maliyeti düşük; ciddiye alınmalı.
**Ne zaman:** Sprint 3'ten önce. **Bağlı:** `TASARIM.md` §4.3.

</details>

---

## 9. "Merge tabanlardan iyi" ne demek — sayıyla? — ✅ **KAPANDI (2026-07-28, [ADR-0037](adr/0037-ic-iddia-karar-kurali-kapi-5.md) — Kapı 5)**

> ### CEVAP — veriye bakılmadan yazıldı, hiçbir kafes hücresi üretilmemişti
>
> ```
> KAPI 5 — norm-dengeli ayarda, τg+τa şunların HEPSİNİ sağlamalı:
>   (a) M1/M4   ≥ 0.90 × (τg tek)              ← grounding korundu
>   (b) M2/M2b  ≥ 0.90 × (τa tek)              ← abstention korundu
>   (c) BİLEŞİK = min(grounding, abstention);  Taban A ve B'nin İKİSİ de geçilmeli
>   (d) M5 base'in ÜSTÜNE çıkmamalı
> ```
>
> **`min`, ortalama değil** — aritmetik ortalama **takasa izin verir** (grounding'i şişirip
> abstention'ı feda etmek "kazanç" görünür), oysa iddia tam olarak bunun olmadığını söylüyor.
> **X = Y = %90 simetrik** — asimetrik eşik bir beceriyi kayırır ve *"eşit koruyor mu"* iddiasını bozar.
>
> **Referans = tekil hücreler**, #8 gereği çiftle aynı hattan geçmiş hâlleri.
>
> **Çoklu karşılaştırma:** DEV'de bileşiği maksimize eden **tek** konfigürasyon TEST'e gider;
> tüm tarama eklerde yayımlanır. ⚠️ **Aynı prosedür tabanlara da uygulanır** — yoksa biz taranmış
> onlar taranmamış olur, kıyas haksız hâle gelir.
>
> **⚠️ Açık kalan:** güç analizi yok (`TASARIM.md` §13 soru 3). Kapı 5 bir **karar kuralıdır**,
> istatistiksel testin yerini tutmaz — limitations'a öyle yazılır.

<details>
<summary>Kararın alındığı andaki soru (kayıt için korunuyor)</summary>

**Soru.** İç iddianın karar kuralı ne? Hangi metrikte, ne kadar fark, hangi yönde?

**Neden önemli.** DEV'de `λ` · density · drop-rate taradıktan **sonra** kural yazmak,
sonucu rasyonalize etmektir. Proje pre-registration'ı zaten uyguluyor (`TASARIM.md` §7:
*"eşikler sonradan yazılırsa çıkan sonuç rasyonalize edilir"*) — ama **iç iddianın kendisi için
kural yazılmamış.** Kapı 0-3 var, "merge kazandı mı" kapısı yok.

Zorluk şu: iddia **tek metrik değil, çatışma**. `τg+τa`, grounding'i (M1/M4) *ve* abstention'ı
(M2/M2b) **aynı anda** korumalı. Tek bir skora indirgemek çatışmayı gizler; iki metriği ayrı
raporlamak da "kazandı mı" sorusunu cevapsız bırakır.

**Taslak öneri** (rakam yok, şekil var):

```
τg+τa  ŞUNLARIN HEPSİNİ sağlamalı:
  (a) M1/M4 ≥ X% · (τg tek)'in değeri        ← grounding korundu
  (b) M2/M2b ≥ Y% · (τa tek)'in değeri       ← abstention korundu
  (c) bileşik ölçütte Taban A ve Taban B'nin İKİSİNİ de geçmeli
  (d) M5 (anti-hedef) base'in üstüne çıkmamalı
```

**Cevaplanmamışlar:** X ve Y kaç · "bileşik ölçüt" nasıl tanımlanır (min? harmonik ortalama?) ·
DEV'deki `n` bu farkı görmeye yetiyor mu (§13 soru 3 ile bağlı — güç analizi yok) ·
tarama sonrası **hangi hücre** raporlanır (en iyi λ mi, önceden sabitlenmiş λ mi — çoklu
karşılaştırma sorunu).

**Ne zaman:** Sprint 3 taramasından **önce**, veriye bakmadan. **Bağlı:** `TASARIM.md` §4.4, §7.

</details>

---

## 10. Merge kütüphanesi — hazır mı, kendi mi? — ✅ **KAPANDI (2026-07-28) · 🔄 revize edilebilir**

> ### CEVAP: **kendi streaming merge'imiz** + zorunlu birim testi + `mergekit` çapraz kontrolü
>
> **Ayrı ADR açılmadı** — kullanıcı kararı açıkça *"ileride uyarılara göre değişebilir"*.
> Geri dönüşü kolay bir uygulama tercihi, dondurulmuş anlatı değil.
>
> **Neden kendi:**
> - ADR-0036'nın **norm-dengeli ön-adımı `mergekit`'in standart `ties`'ında yok.** Onu kullansak
>   bile `w_t = 1/‖τ_t‖`'yi elle hesaplayıp `weight` parametresine vermemiz gerekirdi — yani
>   kritik adım zaten bizde kalıyor.
> - Pinli `requirements.lock.txt`'e dokunulmuyor (`fla-core` dersi taze, `#40`).
> - `TASARIM.md` §4.2 algoritmayı zaten satır satır tarif ediyor; paper'da birebir yazılabilir.
> - **Ölçekle ilgili korku doğrulandı, iş küçük:** `‖τ_g‖` ölçümü (LoRA'dan ΔW çıkarma, katman
>   bazında dolaşma, Frobenius) **~20 satırda çalıştı** → `outputs/eval/tau_norm_tg.json`.
>
> **⚠️ ŞART — doğrulama testi zorunlu.** ADR-0036'daki 5 parametreli örnek birim testine
> çevrilir (ham TIES → p1 = 0.80 · norm-dengeli → p1 = 0.739 · p3 = 0.547) ve kodun çıktısıyla
> karşılaştırılır. TIES'ın işaret-seçimini yanlış yazmak **sessiz hata sınıfıdır** — sayı çıkar,
> yanlış çıkar. Bu hattın sicili (`#38` şablon, `#40` `fla-core`) bunu tavsiye değil zorunluluk yapar.
>
> **`mergekit` yine de kullanılır** — bağımsız **çapraz kontrol** olarak: ham TIES hücresi onunla
> da üretilip bizimkiyle karşılaştırılır. Ayrı ortama kurulur, lock'a girmez.
>
> ### 🔄 Revizyon tetikleri — bunlardan biri olursa `mergekit`'e geçilir
> 1. Birim testi elle hesaplanan değerleri **tutturamazsa**
> 2. `mergekit` çapraz kontrolü bizimkiyle **tolerans dışı** ayrışırsa
> 3. Streaming merge host RAM'de **OOM ederse** ya da kabul edilemez yavaşsa
> 4. Uygulamadığımız bir tekniğe ihtiyaç doğarsa (DARE varyantları, SLERP, model soup vb.)

<details>
<summary>Kararın alındığı andaki soru (kayıt için korunuyor)</summary>

**Soru.** `mergekit` mi, ~200 satırlık kendi streaming merge'imiz mi?

| seçenek | artı | eksi |
| :--- | :--- | :--- |
| **`mergekit`** | `ties` · `dare_ties` · `task_arithmetic` hazır ve test edilmiş · out-of-core/lazy yükleme var · tarama YAML ile ucuz | yeni bağımsızlık zinciri (pinlenebilir ama pinli `requirements.lock.txt`'e dokunur) · içeride ne olduğu bizim değil |
| **kendi** | `TASARIM.md` §4.2 zaten tarif ediyor (host RAM, tensör tensör, bf16 ΔW, kuantizasyon en son) · tam kontrol · makalede birebir yazılabilir | TIES'ı yanlış uygulamak **sessiz** bir hata sınıfı — işaret-seçimini yanlış yazarsan sayı çıkar ama yanlış çıkar |

**Not.** Hangisi seçilirse seçilsin, **doğrulama testi şart**: bilinen küçük bir örnekte
TIES'ın üç adımı elle hesaplanıp kodun çıktısıyla karşılaştırılmalı. Bu hattın sessiz-bozulma
sicili (`#38` şablon tuzağı, `#40` `fla-core`) bunu tavsiye değil zorunluluk yapıyor.

**Ne zaman:** Sprint 3 uygulamasından önce. **Bağlı:** `TASARIM.md` §4.2.

</details>

---

## 11. `τ_reasoning` / RS-FT tez kapsamına giriyor mu? — ✅ **KAPANDI (2026-07-28, [ADR-0035](adr/0035-tau-reasoning-rs-ft-kapsam-disi.md))**

> ### CEVAP: HAYIR — kapsam dışı, future work.
>
> Kollar **2** (`τ_grounding` · `τ_abstention`), kafes **3 hücre**, FT bütçesi **5 koşu**.
> **ADR-0030 madde 2 (düşünce modu KAPALI) yürürlükte kalır** — geri alma gerekçesi ortadan kalktı.
>
> **Kararı veren kanıt, tartışma değil ölçüm:**
> 1. Kullanıcının istediği ürün davranışı (*"kaynak şu şu → sonucum bu bu"*) **`τ_grounding`'in
>    eğitim hedefi.** `raft_scrubbed` sayıldı (n=17.323): `KAYNAK` bloğu **%97**, birebir alıntı
>    **%77**, numaralı çıkarım adımı **%76**. Ayrı kol bu biçim için gereksiz.
> 2. `τ_grounding`'in öğretmediği tek şey **maddeler arası zincir** — o da **harness'ın tasarlanmış
>    işi** (`TASARIM.md` §5: hibrit retriever **1-2 hop** + graf atıf ağı). Ağırlığa gömmek tekrar olur.
> 3. **Yeni karar değil, teyit:** `TASARIM.md` §10.2 *"CoT / gerekçe kolu"*nu zaten plandan
>    çıkarmıştı; bu ADR onu yeni kanıtla RS-FT varyantına genişletir.
>
> **Bedel (limitations'a yazılır):** çok adımlı akıl yürütme model düzeyinde eğitilmedi;
> zincirleme harness'a bırakıldı ve **ikisinin katkısı ayrı ayrı ölçülmedi.**
>
> **Elenen ama reddedilmeyen:** yalnız `pass@16` tanısını koşmak — ertelendi, tez sonrası.

<details>
<summary>Kararın alındığı andaki soru (kayıt için korunuyor)</summary>

**Soru.** `docs/ft-is-akisi.mmd`'de taslak olarak duran **rejection-sampling FT** kolu — üçüncü
task-vector olarak tez kapsamına girecek mi?

**Neden önemli — bu sorunun bedeli en büyük:**

- **Kapsam:** kol 2 → 3, kafes 3 → 7 hücre, eğitim koşusu 5'ten yukarı, araya **FAZ 0 kapıları**
  giriyor (M6 seti üretimi + deterministik zincir-verifier + `pass@16` tanısı + **Kapı R**).
- **Bir ADR'yi geri alıyor:** RS-FT düşünce izi üretmeyi gerektiriyor, ama **ADR-0030 madde 2**
  düşünce modunu KAPALI kilitledi — gerekçe kolaylık değildi: varsayılan modda model `</think>`'i
  kapatmıyor, `content` **boş** dönüyor (HTTP 200, sıfır hata), ve SFT verisi akıl yürütme izi
  taşımıyor (eğitim-eval hizalaması). Geri alınacaksa **ADR-0035** gerekir ve o iki sorunun
  ikisine de cevap vermelidir.
- **Kapı R zaten yazılmış:** `pass@16 = 0` çıkarsa yol **kapanıyor** — RS-FT'nin süzeceği doğru iz
  yok demektir. Yani bu soru kısmen ölçümle cevaplanacak, ama **ölçümü yapmaya değer mi** kararı
  bizde.

**Ne zaman:** Sprint 2 planlanmadan önce — Sprint 2'nin kapsamını doğrudan belirliyor.
**Bağlı:** `docs/ft-is-akisi.mmd`, `docs/model-soyagaci.mmd` (🟡 işaretli), ADR-0030 madde 2.

</details>

---

## 12. Kol vektörlerinin ÖLÇEĞİ nasıl eşitlenecek? — ✅ **KAPANDI (2026-07-28, [ADR-0036](adr/0036-tau-norm-asimetrisi-ve-norm-dengeli-merge.md))**

> ### CEVAP: `‖τ‖` koşulsuz ölçülür · kafes İKİ ayarda koşar · ana sonuç NORM-DENGELİ
>
> 1. **`‖τ‖` ölçümü koşulsuz** — her kol eğitilir eğitilmez Frobenius normu (katman + toplam)
>    `outputs/`'a yazılır, **sayı ne çıkarsa çıksın raporlanır.** `‖τ_g‖/‖τ_a‖` künye bilgisi.
> 2. **Kafes iki ayarda:** ham TIES (`w=1`) + norm-dengeli (`τ_t ← τ_t/‖τ_t‖` sonra TIES).
>    Merge bedava, bedel yalnız eval.
> 3. **Ana sonuç norm-dengeli, ham TIES ablasyon** — yan yana raporlanır, gizlenmez.
>
> **Gerekçe (sayısal):** TIES'ın ②işaret-seçimi ve ③ayrık-ortalaması **kütle ağırlıklı**.
> 6.6× normlu bir örnekte gerçek çatışma parametresinde küçük vektörün katkısı **tamamen
> siliniyor** (oy farkı 0.70); normalize edildiğinde yarış başa baş oluyor (0.132) ve başka
> bir parametrede katkı **6× büyüyor**. Yani müdahale etmezsek *"abstention eziliyor"* diye
> okuruz ama sebep çatışma değil ölçek — tezin ölçtüğü şey ölçülemez hâle gelir.
>
> **⚠️ DARE bu sorunu ÇÖZMEZ:** `(m⊙τ)/(1−p)` beklenen değeri korur → **oranı da korur.**
> DARE'in derdi çok-vektör girişimi, ölçek eşitleme değil. İki ayrı problem.
>
> **Bedel (limitations):** normalizasyon kolun *büyüklük* bilgisini atıyor · eval maliyeti ×2 ·
> TIES literatüründe normalizasyon standart adım değil → paper'da **varyant** olarak sunulur.

<details>
<summary>Kararın alındığı andaki soru (kayıt için korunuyor)</summary>

**Soru.** `τ_grounding` **17.323** satırda, `τ_abstention` **1.741** çiftte eğitiliyor — 10× fark.
`τ_g`'nin deltası büyük olasılıkla belirgin şekilde **daha büyük normlu** çıkacak. Merge'de bu
farkı düzeltecek miyiz, nasıl?

**Neden kritik — TIES'ın üç adımına ne yaptığı:**

| adım | norma duyarlı mı |
| :--- | :--- |
| ① budama (her vektörde kendi içinde top-k%) | ✅ duyarsız |
| ② işaret seçimi `γ = sgn(Σ τ̂)` | ❌ **kütle ağırlıklı → büyük normlu kol kazanır** |
| ③ ayrık ortalama (ham değerler toplanır) | ❌ **büyük normlu kol baskın** |

Hiçbir şey yapmazsak merge **otomatik olarak grounding lehine kayar** ve `τ_abstention` sistematik
olarak eziliyor görünür — ama sebep *çatışma* değil, *ölçek.* Bu doğrudan iç iddiayı vurur: jüri
haklı olarak *"abstention merge'de kayboldu mu, yoksa vektörünüz mü küçüktü?"* diye sorar.

| seçenek | not |
| :--- | :--- |
| **A — kol başına ağırlık `w_t`** (`mergekit`'in `weight` parametresi) | DEV'de taranabilir; ama `w_t` de bir serbestlik derecesi, #9'un karar kuralına dahil edilmeli |
| **B — norm normalizasyonu** `τ_t / ‖τ_t‖` | mekanik, tarama gerektirmez; kolun *büyüklük* bilgisini atar (bilgi mi, gürültü mü — bilinmiyor) |
| **C — hiçbiri, ham TIES** | savunulabilir tek koşul: asimetrinin ölçülüp **raporlandığı** durum |

⚠️ **Ön adım, ucuz ve şart:** her kolun `‖τ‖` değeri eğitim biter bitmez **ölçülüp kaydedilecek.**
Fark küçükse bu sorunun tamamı düşer; büyükse hangi seçenek olursa olsun rapora girer.

**Ne zaman:** Sprint 3 öncesi. **Bağlı:** #8, #9, `TASARIM.md` §4.2.

</details>

---

## 13. Kollar arası eğitim rejiminde ne eşleşmek ZORUNDA, ne serbest? — ✅ **KAPANDI (2026-07-28)**

> ### CEVAP: reçeteye saygı + ölçüm; zorla eşitleme TETİĞE bağlandı.
>
> | ayar | karar |
> | :--- | :--- |
> | precision · `lora_dropout` · `r`/`alpha` · seed | ✅ **eşleşti** (kod düzeltildi) |
> | `lr` (1e-4 vs 1e-5) · etkin batch (16 vs 64) | 🟢 **ORPO'nun reçetesi korunur**, fark **limitations'a** yazılır. Çalışan bir yöntemi kıyas uğruna bozmak kötü takas |
> | `max_seq_len` | ✅ **eşleşti** → ORPO 1536/1152'den **2048/1536**'ya çıkarıldı |
>
> **🔴 Kapatırken çıkan iki bulgu — ikisi de düzeltildi:**
>
> 1. **ORPO epoch başına yalnız 27 adım koşuyordu** (1.741 çift ÷ etkin batch 64). Kıyas:
>    `τ_g` **1.083** adım. Yani ~40× az güncelleme + 10× düşük lr = "farklı yörünge" değil
>    **farklı ölçekte eğitim**, ve `‖τ_a‖`'yı çökerterek #12'yi de zehirlerdi. 12B'de sorun
>    değildi çünkü ORPO **continuation**'dı (dürtmesi yetiyordu); ham base'den yeni davranış
>    öğretmek başka iş. → **`epochs` varsayılanı 1.0 → 3.0** (82 adım). `grad_accum`'a
>    dokunulmadı — OR-sinyali ≥64 istiyor, meşru.
> 2. **Sessiz kırpma:** `max_prompt_length=1152`'de prompt'ların **%4.4'ü**, `max_length=1536`'da
>    prompt+chosen'ın **%2'si** kırpılıyordu (ort 406 tok, p95 1120, max 1703). → **2048/1536**,
>    kırpma ~%0 ve `τ_g` tavanıyla aynı.
>
> **⚠️ TETİK — ne zaman zorla eşitleriz (ön-kayıtlı):**
> *"`τ_a` tekil hücresi M2/M2b'de base çıpasını **geçemezse**, 'ORPO ham base'den çalışmıyor'
> sonucuna varmadan ÖNCE eşleşmiş rejimde (lr 1e-4 / etkin batch 16) bir **tanı koşusu** yapılır."*
> Gerekçe: rejimi dışlamadan yöntemi mahkûm etmek atıf hatası olur.
>
> **Ölçüm borcu:** `τ_a` eğitilir eğitilmez `‖τ_a‖` ölçülüp `‖τ_g‖` ile karşılaştırılacak —
> bu zaten #12'nin gerektirdiği ölçüm, bedava geliyor.

<details>
<summary>Kararın alındığı andaki soru (kayıt için korunuyor)</summary>

**Soru.** İki kol bugün farklı ayarlarda koşuyor. Hangileri task-vector geçerliliği için
**eşleşmek zorunda**, hangileri yöntemin doğası gereği **serbest**?

| | `τ_grounding` (SFT) | `τ_abstention` (ORPO) | değerlendirme |
| :--- | ---: | ---: | :--- |
| precision | **bf16 taban** (ADR-0031) | ~~QLoRA NF4 sabit~~ → ✅ `--bf16-base` | 🔴 **ZORUNLU eşleşme** — farklı `θ_base` = task-vector tanımı bozulur · *düzeltildi* |
| `lora_dropout` | 0.05 (ADR-0033 `0`'ı reddetti) | ~~0.0 sabit~~ → ✅ `--lora-dropout` 0.05 | 🔴 **ZORUNLU** — atfedilebilirlik · *düzeltildi* |
| `target_modules` | varsayılanda `in_proj_*` **YOK** (elle veriliyor) | varsayılanda `in_proj_*` **YOK** | 🔴 **ZORUNLU** — ama sorun **paylaşılan**, ORPO'ya özgü değil; bkz. Kod borçları |
| `lora_r` / `alpha` | 16 / 32 | 16 / 32 | ✅ eşleşiyor |
| seed | 3407 | 3407 | ✅ eşleşiyor |
| lr | 1e-4 | 1e-5 | 🟡 **serbest?** — ORPO'nun kendi rejimi |
| etkin batch | 16 | 64 | 🟡 **serbest?** — reçete: OR-sinyali ≥64 ister |
| `max_seq_len` | 2048 | 1536 / prompt 1152 | 🟡 karar verilmedi |

İlk ikisi düzeltildi (aşağıda), üçüncüsü açık. Son üçü **gerçek soru**: lr/batch farkı meşru mu,
yoksa "iki kol farklı yörüngeden geldi" diye limitations'a mı yazılmalı?

⚠️ **Ayrıca ölçülmemiş bir varsayım:** ORPO bu hatta **hiç ham base'den koşmadı** — 12B'de
continuation'dı (`--adapter`, v2b üstüne). Teorik olarak doğru (ORPO'nun kaybı `L_SFT` terimi
içerir, referans model istemez — DPO'dan farkı bu) ve veri **%20 grounding replay** taşıyor,
ama bu hatta **ölçülmedi.** `τa` tekil hücresi tam olarak bunu ölçecek.

**Ne zaman:** Sprint 2 başlamadan. **Bağlı:** ADR-0031, ADR-0033, `TASARIM.md` §4.1.

</details>

---

## Kod borçları

### ✅ KAPANDI (2026-07-28) — `train_orpo.py` rejim sapması

`scripts/train_orpo.py` 12B dönemi ayarlarında kalmıştı ve `train_sft.py`'den **sessizce**
ayrışıyordu — hata vermez, sayı üretir, sayı kıyaslanamaz olurdu:

| ne | eskiden | şimdi |
| :--- | :--- | :--- |
| precision | `load_in_4bit=True` **sabit kodlu** (QLoRA NF4) | `--bf16-base` bayrağı, ADR-0031 birincil yolu |
| `lora_dropout` | `0.0` **sabit kodlu** | `--lora-dropout`, varsayılan **0.05** (ADR-0033) |

Bayraklar `modal_train.py`'ın `train_orpo` + `spawn_orpo` yollarından da geçiriliyor
(`bf16_base` · `lora_dropout` · `target_modules`), yoksa Modal'dan kullanılamazlardı.

### 🔴 AÇIK — `--target-modules` varsayılanı İKİ script'te de eksik

Düzeltme sırasında çıktı: **`train_sft.py` ve `train_orpo.py` aynı varsayılanı taşıyor** —
`q/k/v/o + gate/up/down`, yani **`in_proj_qkv/z/a/b` YOK.** Bu ORPO'ya özgü bir sapma değil,
**paylaşılan bir mayın**: Qwen3.5'te 24 linear-attention katmanı LoRA'sız kalır, hata vermeden.

> **⚠️ Bedeli artık ÖLÇÜLDÜ** (`τ_grounding`, 2026-07-28 → `outputs/eval/tau_norm_tg.json`):
> `in_proj_*` modülleri `‖τ‖`'nin **%26.8'ini** taşıyor (`in_proj_qkv` %16.8 + `in_proj_z` %10.0).
> Varsayılan liste kullanılsaydı **adaptasyonun dörtte biri hiç öğrenilmezdi.**
> Ayrıca LoRA çifti sayısı **224** çıktı ve ADR-0031'in mimari varsayımını birebir doğruladı:
> `8 full-attn × 4 + 24 linear-attn × 4 + 32 × 3 (MLP) = 224`.
> *(Yan bulgu: ağırlık MLP'de toplanıyor — `gate_proj` %34.5 + `up_proj` %23.2 = %58;
> `k_proj`/`v_proj` neredeyse hiç değişmemiş, %0.6 / %0.5.)*

Bugün tek koruma, listeyi **her çağrıda elle vermek** (CP5 komutu öyle yapıyor,
`NEXT-SESSION.md` §3 "asla düşürme" diye uyarıyor). Bu koruma değil, disiplin.

**Seçenekler:** (a) varsayılanı sil, `--target-modules` **zorunlu** yap → tanımsız base erken
patlar, ADR-0026'nın ruhu · (b) base'e göre liste tut → ADR-0026'ya aykırı (script base bilmemeli) ·
(c) olduğu gibi bırak + uyarı bas.
**Eğilim: (a).** ⚠️ `train_sft.py`'ye dokunmak CP5 koşarken **yapılmadı** — koşu bitince.

### 🟡 PLANLANDI — `causal-conv1d` hız kaldıracı, Sprint 2 öncesi ÖLÇÜLECEK

CP5'te ölçüldü: kararlı hız **6.8-7.0 s/it**, **2.619 token/s**, **MFU ≈ %15**. Sebep büyük
ölçüde `causal-conv1d`'nin kurulu olmaması — GatedDeltaNet katmanları PyTorch referans yoluna
düşüyor (*"The fast path is not available"*) ve Qwen3.5-4B'nin **32 katmanının 24'ü**
linear-attention. Fallback **matematiksel olarak aynı**: çıktı geçerli, yalnız yavaş.

**Karar (2026-07-28): CP5'e dokunulmadı** — gerekçe [ADR-0033](adr/0033-egitim-hizi-fla-core-checkpointing-batch.md)
ölçüm güncellemesinde.

**Yapılacak:** Sprint 2'nin **4 koşusundan önce** (`τa` + Taban A + Taban B×2) image'a
`causal-conv1d` eklenip **bir smoke ile s/it ölçülecek.** 2× çıkarsa ~5 saat + ~$12 tasarruf.
⚠️ Kazanç **ölçülmeden yazılmayacak** — bu ADR'nin kendi dersi (`fla-core` teşhisi tahminle
yapılmış ve yanlış çıkmıştı, `#40`).

⚠️ Ayrıca `requirements.lock.txt` **korunmalı**: `fla-core` düzeltmesinde olduğu gibi, yeni paket
pinli ortamı bozmamalı — önce sürüm uyumu kontrol edilir.

### ⚠️ Kalıcı uyarı — `--adapter` yolu

`train_orpo`'nun **`--adapter` (continuation) yolu Sprint 2'de KULLANILMAZ**; `--fresh-adapter`
zorunlu. `--adapter tg` yazmak ardışık SFT üretir, yani **Taban B**'yi kol diye kaydeder.
Kod bunu engellemiyor, sadece uyarı basıyor. `spawn_orpo` docstring'ine yazıldı.

**Bağlı:** #13.

---

## İleri notlar — karar değil, kaydedilmeye değer gözlem

### Sıfır marjinal maliyet asimetrik bir koz (2026-07-28)

**Gözlem.** Yerel çıkarımda maliyet modeli rakiplerinkiyle **aynı şekilde davranmıyor:**

```
Rakip :  $/sorgu = token fiyatı × token        → hop sayısıyla DOĞRUSAL artar
Bizde :  $/sorgu = eğitim_maliyeti / N         → hop sayısından BAĞIMSIZ
         gerçek bedel = LATENCY (elektrik ihmal)
```

**Sonucu:** sorgu başına ek çıkarım gerektiren teknikler (ajan döngüsü, iteratif getirme,
self-consistency, yeniden sıralama) **bizde ucuz, rakipte pahalı.** Adalet kuralı gereği aynı
döngü rakibe de verilirse onun `$/sorgu`'su katlanır, bizimki sabit kalır → makas **bizim lehimize**
açılır. Bu bir dezavantaj değil, **ürün fazında asimetrik avantaj.**

**Latency bütçesi (ölçülen + tahmin):** decode **122.9 t/s** → 300 token'lık cevap **~2.4 sn**;
3 hop ≈ **~8 sn** ⚠️ **tahmin** — her hop bağlamı büyüttüğü için prefill payı artar, **ölçülmedi.**
Avukat için araştırma gecikmesi olarak kabul edilebilir bantta.

**Tez metriğine etkisi yok:** `$/sorgu` değişmediği için **başabaş noktası N\* hop sayısından
etkilenmiyor.** Latency ayrıca raporlanan bir metrik (`TASARIM.md` §6.4), oraya yazılır.

### ⚠️ Düzeltme — §10.2'nin "çok-ajanlı" elemesi ne kapsıyor

`TASARIM.md` §10.2'nin *"çok-ajanlı / LLM-indeksli GraphRAG"* elemesi bu oturumda bir kez
**yanlış genişletildi** (sorgu-zamanı hop sayısına uygulandı). Doğru okuma: o satırın hedefi
grafı **LLM ile kurmak** — 40.496 madde × LLM çağrısı = büyük çevrimdışı maliyet + halüsinatif
kenar riski. **Sorgu-zamanı hop sayısı o cümlenin kapsamında değil**, ve yukarıdaki gerekçeyle
bizde maliyet sorunu da değil. Ajanlaştırmayı tezden eleyen şey **kapsam ve gecikme**, maliyet değil.

### İteratif getirme model değişikliği gerektirmeyebilir

Atıf doğrulayıcı zaten *"cevapta atıf var ama o madde bağlamda yoktu"* durumunu tespit ediyor
(red kapısının parçası). Bu sinyalle deterministik bir döngü kurulabilir: eksik maddeyi graf
getirir, model yeniden koşar. **Model *"m.350 lazım"* demeyi öğrenmek zorunda değil** — atıf
yapması yeterli. Alternatif (daha pahalı) yol, `τ_abstention`'ı 1 bitten *"yetersiz + şu eksik"*
işaretçisine genişletmek; yeni beceri değil, mevcudun uzantısı. Her ikisi de **ürün fazı**.

---

## Başka yerde duran açık kalemler — burada tekrarlanmaz

| ne | nerede |
| :--- | :--- |
| 7 tasarım sorusu (embedder · red eşiği · DEV n · zamansal eksen · hakem 3. aile · içtihat grafı · yinelemeli merge) | [`TASARIM.md`](../TASARIM.md) §13 |
| `τ_abstention` Sprint 1'e çekilsin mi | [`sprint1.md`](../sprint1.md) §Sprint 1 dışında kalanlar |
| Sağlayıcı pinlemesi · rakip üretim maliyeti · CP2 M2 regex uyuşmazlığı | [`docs/record/sprint1/NEXT-SESSION.md`](record/sprint1/NEXT-SESSION.md) §8 |
| `causal-conv1d` + H100 hız kaldıraçları | [ADR-0033](adr/0033-egitim-hizi-fla-core-checkpointing-batch.md) |
| Devir paketinin yedeksiz tek nüsha olması | [ADR-0034](adr/0034-emekli-hat-artefaktlarinin-repodan-cikarilmasi.md) |
