# ADR-0039 — **Kapı 6**: parametrik sızıntı kendi kapısına ayrıldı · ADR-0037 madde (d) düşer

**Statü:** Yürürlükte · **Tarih:** 2026-07-29
**Otorite belge:** `TASARIM.md` §7 (kapılar) · §1.2 (iç iddia)
**İlgili:** **ADR-0037 (Kapı 5) — madde (d) BU ADR ile kaldırıldı** · ADR-0011 (6-mod CANON,
M5 anti-hedef) · ADR-0027 (kol tanımı)
**Kanıt:** `research_log` [#41](../record/research_log/2026-07-29-cp6-tau-grounding-olcumu.md) ·
[`sprint1-sonuc-tablosu.md`](../record/sprint1/sprint1-sonuc-tablosu.md)
**Ön-kayıt şerhi:** Bu değişiklik **2026-07-29'da**, `base` ve `τ_g`'nin **tekil** M5 sayıları
görülmüşken, **hiçbir kafes/merge hücresi üretilmemişken** yapıldı. Savunmanın tamamı bu cümleye
dayanır — değiştirilen kuralın uygulanacağı veri henüz yoktur.

---

## Bağlam — ölçülen çıkmaz

ADR-0037'nin Kapı 5'i dört maddeliydi; dördüncüsü:

```
(d) M5 (anti-hedef) base'in ÜSTÜNE ÇIKMAMALI
```

CP6 (#41) `τ_g`'yi ölçtü. M5 — modele **hiç kaynak verilmeden** sorulan mod, yani *"cevabı
ağırlıklarından mı üretiyor"* sınavı — şöyle çıktı:

| M5 ekseni | base | Gemini 3.1 FL | **`τ_g`** |
| :--- | ---: | ---: | ---: |
| A1 (cevaplananların sadakati) | 0.2852 | 0.6213 | **0.4018** ↑ |
| coverage (kaç soruya konuştu) | %37.5 | %23.8 | %36.2 ↓ *(hafif iyi)* |
| **ezber kütlesi** (`coverage × A1`) | **%10.7** | %14.8 | **%14.6** ↑ |

**Sonuç:** `τ_g` (d)'yi ihlal ediyor. (d) sert veto olduğu için **`τ_g` içeren her kafes hücresi**
— yani ölçmek üzere kurulmuş olan `τg+τa` dahil — (a)(b)(c)'yi geçse bile Kapı 5'ten kalır.
**Kapı, ölçmek için kurulduğu şeyi ölçemeden kapanır.**

İkinci bir kusur: **(d) hangi M5 metriğini kastettiğini yazmıyordu.** A1 ve `faith_macro` ihlal
ediliyor, coverage ise iyileşiyor. Metrik sonradan seçilirse işimize gelen seçilir.

## Karar

### 1. Madde (d) Kapı 5'ten **çıkarılır** — Kapı 5 üç maddeye iner

```
KAPI 5 — İÇ İDDİA (merge çatışan becerileri koruyor mu?)
  (a) M1/M4   ≥ 0.90 × (τg tek)
  (b) M2/M2b  ≥ 0.90 × (τa tek)
  (c) BİLEŞİK = min(grounding, abstention),
      Taban A ve Taban B'nin İKİSİ de geçilmeli
```

**Gerekçe gevşetme değil, sınıflandırma düzeltmesi.** İç iddia *"bağımsız eğitilmiş kollar +
görev-vektörü merge, **çatışan** becerileri korur mu"* sorusudur. M5 o çatışmanın tarafı değil:
`τ_a` M5'i **düşürür** (reddetmeyi öğrenen model kaynaksızken de az konuşur), `τ_g` yükseltir —
ikisi zıt yönde çekmiyor, `τ_a` zaten aynı yöne itiyor. M5, *"ağırlık mı sızdırıyor"* sorusudur;
dış iddianın ve ürün kısıtının konusudur (`CLAUDE.md`: *"güncellik kütüphanede, ağırlıkta değil"*).
İki ayrı iddiayı tek kapıya bağlamak tasarım hatasıydı.

**Ayırmanın ölçülebilir faydası:** ayrı olunca sonuç cümlesi
*"merge becerileri korudu ✅, ama model parametrik sızıntıyı artırdı ❌"* olur. Tek kapıda ikisi
birbirine karışır ve **hangisinden kalındığı kaybolur.**

### 2. **Kapı 6 — parametrik sızıntı** (YENİ)

```
KAPI 6 — PARAMETRİK SIZINTI
  hedef        : M5 coverage → sıfıra yakın
  geçme şartı  : İKİSİ de base'i GEÇMEYECEK
                   M5 coverage    ≤ %37.5   (base)
                   M5 ezber kütlesi ≤ %10.7 (base, = coverage × A1)
  yayın şartı  : her hücre M5'in ÜÇ sayısını da (coverage · A1 · kütle)
                 base'e göre farkıyla birlikte yayımlar
```

**Çıpa base'dir, rakip değil.** Değerlendirilen ve **reddedilen** alternatif, rakip çıpasıydı
(`M5 A1 ≤ Gemini 0.6213`); `τ_g` onu geçiyordu. Reddedilme gerekçesi kullanıcı kararı ve doğrudur:
**modeli aldığımız noktadan kötüye götürmemeliyiz.** Rakip çıpası, kaçırılan eşiği taşımak olurdu.

**Neden iki sayı, tek sayı değil.** M5'te iki ayrı kabahat var ve tek metrik ikisini gizler:

| kabahat | ölçüsü | hedefi |
| :--- | :--- | :--- |
| Susması gerekirken konuşmak | **coverage** | **sıfıra yakın** — gerçekten sıfırlanabilir |
| Konuştuğunda kanunu ezberden bilmek | **A1** | base'i geçmemek — *sıfır hedefi anlamsız*, çünkü A1=0 demek "konuşuyor ve hep yanlış" demektir, o daha kötü |
| İkisinin bileşimi | **kütle = coverage × A1** | base'i geçmemek — tek eksende okunabilir hâli |

`faith_macro` **kullanılmaz**: cevaplanmayanları da içerdiği için coverage'a bulaşır.

### 3. Orijinal (d) silinmez — raporlama şartı olarak yaşar

Her kafes hücresi **iki ölçüte karşı da** raporlanır: Kapı 6 (yukarıdaki) **ve** orijinal (d)
(`M5 ≤ base`, ki bu Kapı 6'nın ilk iki satırıyla aynı — yani pratikte katılık **korunmuştur**).
Bugünkü durum aynen yazılır: **`τ_g` bu kapıdan kalıyor.**

### 4. Kalınca ne yapılacağı — ön-kayıtlı merdiven

Kapı, kalınca ne yapılacağı yazılmadıysa temennidir. Ucuzdan pahalıya:

| # | ne | bedel | not |
| :-- | :--- | :--- | :--- |
| 1 | **`τ_a` düzeltebilir** — reddetmeyi öğrenen model kaynaksızken de az konuşur | $0 (zaten koşulacak) | en muhtemel |
| 2 | **Merge ağırlığı** — `τ_g`'nin payını azaltmak sızıntıyı da azaltır (grounding'i de) | $0, merge bedava; DEV'de zaten taranacak | |
| 3 | **Harness** — üründe modele **her zaman** kaynak verilir; getirme boş dönerse red kapısı çalışır. Ürün M5 koşullarında hiç çalışmaz | Sprint 4'te zaten var | yapısal cevap |
| 4 | **`τ_g` v2** — kaynağa daha sıkı bağlı veri / yumuşak reçete | ~$5.5 | son çare; bkz. ADR-0040 madde 3 |

Dördü de tutmazsa: *"ince-ayarımız parametrik sızıntıyı base'e göre artırdı"* **negatif bulgu
olarak** raporlanır. Bu projede negatif bulgu birinci sınıf sonuçtur.

## Değerlendirilen alternatifler

| eleme | gerekçe |
| :--- | :--- |
| **(d)'yi yerinde gevşetmek** (base → rakip çıpası) | En zayıf savunma: gerekçe doğru olsa bile *"eşiği kaçırınca taşıdılar"* okuması meşru kalır. Ayrıca kullanıcı kararı açık: base'den kötüye gidilmez |
| **(d)'ye hiç dokunmamak**, ihlali olduğu gibi raporlamak | Dürüstlük tavanı, ama iç iddiayı M5 yüzünden "başarısız" göstermek ölçtüğü şeyi yanlış raporlamaktır. İki ayrı sorunun cevabı tek "kaldı"ya çökerdi |
| **M5'i bileşiğe üçüncü terim olarak katmak** (`min(g, a, 1−m5)`) | Kapıyı okunmaz yapar ve yine iki iddiayı karıştırır; ayrıca `min` bileşiğinin ADR-0037'deki takas-önleme gerekçesi M5 için geçerli değil |
| **Metrik = `faith_macro`** | Cevaplanmayanları içerir → coverage'a bulaşır; iki kabahati ayrıştıramaz |
| **Metrik = yalnız coverage** | *"Kaç kez körlemesine konuştu"* der, *"ne kadar ezberlemiş"* demez. Anti-hedefin asıl sorduğu ikincisi |

## Sonuç — kabul edilen bedel

- **`τ_g` bugün Kapı 6'dan kalıyor** ve bu makalede yazılı olacak.
- Kapı 5 artık iç iddiayı ölçebiliyor; Kapı 6 ürün kısıtını ayrı ölçüyor.
- ⚠️ **Güç analizi yok** (ADR-0037'den devralınan sınır): Kapı 6 de bir **karar kuralıdır**,
  istatistiksel test değil. `runs=1`, güven aralığı yok. Limitations'a bu hâliyle yazılır.
- ⚠️ M5 coverage'ın `τ_g`'de **düşmüş** olması (%37.5 → %36.2) kayda geçer: ihlal
  *"daha çok konuşuyor"*dan değil, *"konuştuğunda daha çok tutturuyor"*dan geliyor. Yani sorun
  ezberdir, gevezelik değil.
