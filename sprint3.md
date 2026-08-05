# Sprint 3 — HARNESS: modeli ürüne çevirmek

> ## 📍 DURUM 2026-08-05 — **S1 ✅ · S3 ✅ · sırada S2**
>
> **S3a ✅ · Adım 0 🔴 · Adım 1-4 ✅ · S1 ✅ · S3 ✅.**
>
> 🚨 **Bu sprintin manşet sayısı düzeltildi.** `harness_tablo.py` `A1` diye **cevaplanan-only**
> değil **ham makro** yazıyordu (tuzak **2.16**) ve harness KAPALI çıpası doğru metrikteydi →
> ON/OFF kıyası **elmayla armuttu**. Düzeltilmiş resmî sayılar:
>
> ```
>                        KAPALI (m1)   AÇIK k=5        AÇIK k=10  ← ürünün ayarı
> A1 (cevaplanan-only)      0,9087    0,7591          0,7681
> KÜTLE                     %71,6     %56,9 (~~58,7~~) %59,5
> A1 · altın getirilen      0,9087    0,9230 (~~9344~~) 0,8426
> ```
>
> **S1: `k=10` kabul edildi** (+2,6 puan kütle) — ama tahminin (~%65) altında; sebebi ölçüldü:
> **dikkat dağılması** altın getirilende A1'i 8 puan düşürüyor. **S3: 62/18 etiket** — model
> erişimin en çok battığı yerde en az çekiniyor (k=10 bunu kısmen düzeltiyor).
> Ayrıca **korpusun kendisi bozuk çıktı** (anahtarların %22,7'si yineleniyor) → S2 büyüdü.
>
> **Bugünün bedeli:** GPU **$0** (yerel) · hakem **$0,047** *(sprint toplamı $0,085 ≤ $2)*.
> Kayıt: [#52](docs/record/research_log/2026-08-05-korpus-butunlugu.md) ·
> [#53](docs/record/research_log/2026-08-05-ayirt-edicilik-etiketi.md) ·
> [#54](docs/record/research_log/2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md)
>
---

# ▶ SIRADAKİ — `/goal sprint3.md` BUNU KOŞAR

> **Adım 0-4 kapandı. Bu belgenin canlı kısmı artık aşağısı.** Sıra **ölçülmüş**
> borçlardan türetildi (tam gerekçe: [açık borçlar](#-sprint-3ün-açık-borçları)).
> Her iş **doğrulanabilir hedef** olarak yazıldı; tahminler **sayı görülmeden** kaydedildi.

```
🛑 DURMA : geçerlilik kapısı düşerse · kütle DÜŞERSE (aşağıdaki ön-kayıtlı eşikler)
           · korpusa yazmadan önce (S2) yedek yoksa · bütçe: hakem toplam ≤ $2
kapsam   : S1-S4.  Graph-RAG, ajanlar, vatandaş kipi HÂLÂ DIŞINDA
           graf gerekçesi ve ön-kayıtlı tahmini: ROADMAP.md §5.2 — ayrı yetenek,
           ayrı soru kümesiyle ölçülür; bu kümede ölçmek haksız yere başarısız gösterir
```

> ### ⚠️ SIRA BAĞLAYICI — S1 mutlaka S2'den ÖNCE
> **S2 korpusu değiştiriyor.** Sonucu: (a) `retriever.py`'nin bayat-indeks kapısı patlar
> ve indeks yeniden kurulur (~10 dk), (b) daha önemlisi — k=5 sayısı **eski** korpusta
> ölçüldü; k=10'u **yeni** korpusta ölçersek `k` farkıyla **korpus** farkı birbirine
> karışır ve hiçbir yerde hata çıkmaz. Bu, tam olarak bu hattın hata sınıfı.
> **S1 bitmeden korpusa dokunulmaz.**

### S1 — `k` süpürmesi *(borç B3)* — ✅ **KAPANDI 2026-08-05 · `k=10` KABUL** · [research_log #54](docs/record/research_log/2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md)

> **Bedel:** GPU **$0** (yerel, şarjda) · hakem **$0,0403**. Geçerlilik kapısı ✅ (kesik %2,5),
> örneklem birebir aynı 80 soru ✅, CTX ✅ (en uzun istem 3.582 tok → 5.118 < 8.192).

🚨 **Ama önce: bu sprintin yayınlanmış kütle sayısı YANLIŞ metrikle üretilmiş.**
`harness_tablo.py` `A1` diye **cevaplanan-only** değil **ham makro** yazıyordu (tuzak **2.16**).
Çekinmeler de hakemden puan alıyor ve **sapma yön değiştiriyor**: k=5'te makroyu yukarı
(0,9091), k=10'da aşağı (0,6819) çekmiş. Harness KAPALI çıpası doğru metrikteydi → **ON/OFF
kıyası elmayla armuttu.** [ADR-0050](docs/adr/0050-verim-kapisi-tahmin-edici-duzeltmesi.md)
kuralı uygulandı: **eşik değil ALET** düzeltildi, iki kola **simetrik**, eşik aynı koşudan
yeniden türetildi (%58,7 → **%56,9**).

| eksen | KAPALI (m1) | AÇIK **k=5** | AÇIK **k=10** |
| :--- | ---: | ---: | ---: |
| altın getirilen | garanti | 60/80 | **70/80** |
| coverage | 0,7875 | 0,7500 | **0,7750** |
| **A1 (cevaplanan-only)** | 0,9087 | ~~0,7823~~ **0,7591** | **0,7681** |
| A1 · altın getirilen | 0,9087 | ~~0,9344~~ **0,9230** | **0,8426** ⬇ |
| **kütle** | **%71,6** | ~~%58,7~~ **%56,9** | **%59,5** |
| katı kapı reddi | 2/80 | 1/80 | 1/80 |
| uydurulmuş madde no | 0 | 0/89 | **0/120** |

**Kabul karşılandı** (k=10 > k=5: +2,6 puan) ama **ön-kayıtlı tahminin (~%65) altında.**
Sebep ölçüldü — ret şıkkının sorduğu soru cevaplandı: **dikkat dağılması.** Altın madde
bağlamdayken bile, yanına 5 madde daha konunca A1 **8 puan** düşüyor (0,9230 → 0,8426).
Net kazanç, erişimin kazandırdığı **+10 sorunun** bu bedeli aşmasından geliyor.
→ **`k=20` için gerekçe zayıf:** `recall@20` yalnız +5 puan getirirken bağlam bir kat daha
uzar ve bu bedel ölçülmüş biçimde büyür.

**İki kazanç daha:**
- **B1'in sınıfı yarıya indi** — *altın gelmeden cevapladı* **14 → 7**. Ama **aşırı-red
  değişmedi** (14 → 15): altın bağlamdayken çekinilen soru sayısı k'dan **bağımsız**.
- ⭐⭐ **Ters çekinme kalibrasyonu düzeliyor** (S3'ün bulduğu terslik): belirsiz alt kümede
  coverage **0,944 → 0,722**, ayırt edicide **0,694 → 0,790** — sıralama ❌ tersten ✅ doğruya.

**Yeni borç B8:** atıf doğrulayıcısı **ilk kez** bir şey yakaladı ve o bir **yazım hatası** —
model bağlamdaki `FİKİR VE SANAT ESERLERİ KANUNU`'nu `…ESELERİ…` diye kopyalamış (bir harf),
madde no'ları doğru. Katı kapı doğru bir cevabı **tek karakter** yüzünden reddediyor.

<details><summary>S1'in ön-kayıtlı planı (kayıt, üzerine yazılmadı)</summary>

```
1. k ∈ {5, 10} için harness AÇIK koş (k=5 zaten var, yalnız k=10 koşulacak)
   → verify: geçerlilik kapısı geçiyor (kesik ≤ %5) ve bağlam CTX 8192'ye sığıyor
2. harness_tablo.py ile iki k'yı yan yana koy
   → verify: erişim/davranış çapraz tablosu k=10'da altın-getirildi sayısını yükseltiyor
3. kütleyi karşılaştır
```

**⛔ ÖN-KAYITLI TAHMİN (2026-08-04, sayı görülmeden):** bugünkü çapraz tablodan türetildi —
altın getirildiğinde cevaplama oranı 46/60 = **0,767**, altın getirilenlerde A1 **0,934**,
getirilmeyenlerde A1 **0,284** *(0,7823×60 − 0,934×46)/14 ile türetildi)*.

| k | beklenen altın getirilen | beklenen coverage | beklenen A1 | **beklenen kütle** |
| ---: | ---: | ---: | ---: | ---: |
| 5 *(ölçüldü)* | 60/80 | 0,750 | 0,782 | **%58,7** |
| **10** | ~70/80 | ~0,76 | ~0,86 | **~%65** |
| 20 | ~74/80 | ~0,76 | ~0,89 | ~%68 · ⚠️ 20×900 kar ≈ 6K token, düşünce bütçesiyle CTX'e sığmaz |

**Kabul:** k=10 kütlesi **> %58,7**. **Ret:** kütle düşerse → k=5 kalır, sebebi
(bağlam uzunluğu mu, dikkat dağılması mı) **gözle okunur**, uydurulmaz.

</details>

### S3 — Ayırt-edicilik etiketi *(borç B2)* — ✅ **KAPANDI 2026-08-05** · [research_log #53](docs/record/research_log/2026-08-05-ayirt-edicilik-etiketi.md)

> S1 koşarken paralel koşuldu (hakem API'si, GPU'ya ve korpusa dokunmuyor). Hakem **$0,0069**.
> İstem koşudan **önce** kayda geçti; körlük çağrı imzasının kısıtı (`_istem(soru)`).

**Etiket: 62 ayırt edici · 18 belirsiz (%22,5)** — S3a'nın gözle tahmini tuttu.

| eksen (k=5) | ayırt edici (n=62) | belirsiz (n=18) |
| :--- | ---: | ---: |
| `recall@5` | **0,8226** | **0,5000** |
| coverage | 0,6935 | 0,9444 |
| A1 | 0,8651 | 0,4909 |
| kütle | %60,0 | %46,4 |

**Tuzak 7.4 sayıyla doğrulandı:** `recall@5` iki alt küme arasında **32,3 puan** ayrışıyor →
*"recall@5 = 0,750"* retriever'ın değil **kümenin kompozisyonunun** sayısı.

⭐⭐ **Beklenmedik:** model, erişimin **en çok battığı** yerde **en az** çekiniyor (belirsizde
%5,6, ayırt edicide %30,6). B1'in 14 vakasının **8'i** kümenin %22,5'inde yoğunlaşmış.
Mekanizma tahmini: çekinme sinyali bağlamın **konusal uyumundan** geliyor, **yeterliliğinden**
değil → doğrudan **S4** girdisi. *(k=10 bu tersliğin yönünü düzeltiyor — S1'e bak.)*

### S2 — Yürürlük alanı *(borç B7)* 🚨 ürün-güvenliği · 🟡 **SIRADAKİ**

```
1. Korpustaki "(Mülga: ...)" kalıbını ayrıştır → `mulga` + ilga eden kanun/madde alanı
   → verify: 1475/15 mulga=true, 1475/14 mulga=false (kıdem tazminatı yürürlükte)
2. atif_dogrula.py: mülga maddeye atıf ayrı hüküm (MULGA), DOGRULANDI değil
   → verify: "İŞ KANUNU Madde 15" → MULGA · red kapısı REDDEDER
3. Harness AÇIK koşuyu YENİDEN puanlama — kaç cevap etkileniyor, sayılır
```

⚠️ **Korpusa yazmadan önce yedek.** Ve `retriever.py`'nin bayat-indeks kapısı korpus
değişince **patlar** — indeks yeniden kurulur (~10 dk, GPU'da).
**Kabul:** en az bir gerçek mülga atıf yakalanıyor **ve** yanlış-pozitif sıfır (gözle).

#### ⚠️ 2026-08-05 — S2'nin salt-okunur keşfi koşuldu, **S2 büyüyor** ([research_log #52](docs/record/research_log/2026-08-05-korpus-butunlugu.md))

S1 koşarken korpus **okundu** (yazılmadı — sıra kısıtı korundu). Aday kural ölçüldü **ve
korpusun kendisinde aranmayan bir kusur çıktı:**

- ✅ **Aday kural sprint'in verify kalemini geçiyor.** Naif *"metinde `(Mülga` geçiyor"*
  **3.652** madde yakalıyor; baştaki ayrıştırma artığı atıldıktan sonra *"`(Mülga` ile
  **başlıyor**"* **2.496** → aradaki **1.156** yalnız bir **fıkrası** mülga olan maddeler,
  yani naif kuralın **yanlış pozitifi**. Verify: `1475/15` ✅ mülga · `1475/14` ✅ yürürlükte
  (kıdem tazminatı) · `4857/15` ✅ yürürlükte.
- 🚨 **Ama `mulga` alanı B7'nin yalnız YARISINI kapatıyor.** `(kanun_no, madde_no)`
  anahtarlarının **%22,7'si yineleniyor** (9.192 fazladan satır) — iki sebep: **(a)** `3520`
  bir madde-numarası **tablosudur**, 1.166 hücresi "madde" diye indekslenmiş; **(b)**
  alt-madde soneki `madde_no`'ya değil **metne** düşüyor (`2004/309` **27 kez**, çünkü
  `309/a`, `309/b`… hepsi `Madde 309`). B7'nin `İŞ KANUNU Madde 15` vakasında `DOGRULANDI`
  damgası **39 karakterlik yanlış ayrıştırılmış bir parçaya** basılmış.
- ✅ **S1 bundan etkilenmedi, ölçüldü:** 5/80 soru yinelenen anahtarlı; temiz alt kümede
  `recall@5` **0,7467** ↔ tüm küme **0,7500**.

**S2'nin kapsamı güncellendi:** (1) `mulga` + ilga alanı · (2) **alt-madde soneki
`madde_no`'ya taşınır** · (3) **tablo-parçası satırları elenir**. ⚠️ (3) indeksi ~1.166 satır
küçültür → `recall@k` **değişebilir**, bu yüzden S1'in eski korpusta bitmesi şarttı.

#### ✅ S2 KAPANDI 2026-08-05 — kapsam **menüden değil ölçümden** seçildi

Yukarıdaki (3) **yapılmadı**, ve bu bir atlama değil **ölçülmüş bir karar**. Kapsam sorusu
*"korpus ne kadar bozuk"* değil, **"modelin GÖRDÜĞÜ bağlamda çöp var mı"** diye soruldu —
k=10 koşusunun `context_shown` alanı, yani modele giden metnin kendisi ayrıştırıldı:

| bozulma sınıfı | korpusta | **modele ulaşan blok** | karar |
| :--- | ---: | :--- | :--- |
| **A — tablo/cetvel parçası** | ~7.966 satır | **0 / 800** ❌ | **ertelendi → borç B9** |
| **B — alt-madde soneki** | **485 satır** | **14 / 800 · 12 soru** ✅ | ✅ yapıldı |

Sınıf A'yı elemek **ölçülemez bir kazanç için ölçülmüş bir sayıyı harcamak** olurdu: parçalar
öylesine kısa (`", Ek"` = 4 karakter) ki ne BM25 ne yoğun vektör onları üste çıkarıyor.
⚠️ Ayrıca *"anahtar yinelenmesi"* (%29,4) ile *"bağlam kirlenmesi"* (%1,8) **aynı şey değil** —
retriever yinelenen anahtarın **doğru** satırını getiriyordu.

**Yapılan** ([`scripts/korpus_yururluk.py`](scripts/korpus_yururluk.py), atomik yazma):
`mulga` + ilga eden kanun/madde/tarih → **2.547 satır** (%99,6 kaynaklı) · alt-madde kimliği
→ **485 satır** · `atif_dogrula.py`'ye **`MULGA`** hükmü (`red_kapisi` değişmedi — `DOGRULANDI`
dışındaki her hükmü zaten reddediyor).

**Kabul ölçütü geçti:** `1475/15` MULGA · `1475/14` yürürlükte · *"İş Kanunu Madde 15"* katı
kapıda **REDDEDİLDİ** · yanlış-pozitif sıfır (3 örneklem turu, gözle).

🐞 **İki kural doğrulama hedefine çarpıp düzeldi — ikisi de sessizce yanlış veri üretecekti:**
1. **Sonek kuralı %80 eksikti.** Yalnız küçük harf aranıyordu; en sık sonek **büyük `/A`**
   (249 satır). 98 sanılan sınıf gerçekte **485**.
2. **İlga kaynağı tarihi kanun sanıyordu.** `"22/5/2003/4857/120 md."` içinden `2003/4857`
   okunuyordu — tarihin son parçası kanun numarası oluyordu. `1475/15`'in ilga kaynağı
   `4857 md.120` yerine `2003 md.4857` çıkmıştı. **Sprint'in kendi verify kalemi ele verdi.**

⚠️ **DÜRÜST NEGATİF SONUÇ:** mevcut k=5 ve k=10 koşuları yeniden puanlandı → **hükmü değişen
cevap 0/80**, MULGA sayısı **0**. Açık **mekanik olarak** kapandı, ama bu DEV kümesinde
**ölçülen görülme sıklığı sıfır**. B7 bir **ürün-güvenliği** özelliği, bir skor özelliği
değil — öyle raporlanıyor.

✅ **Eval etiketleri düzeltilmedi, çünkü gerek kalmadı:** onarım öncesi altın `2004/Madde 31`
anahtarını **`31/a` satırı da** karşılayabiliyordu; artık ikisi ayrı. Havuz iki eval kümesinde
de **80/80** ve **40/40** korunuyor → yer doğruluğu **sıkılaştı**, kıyaslanabilirlik bozulmadı.

⚠️ İndeks **yeni dizine** kuruldu (`data/index/mevzuat_bge_m3_s2`); eskisi yerinde bırakıldı
ki S2 öncesi sayılar yeniden üretilebilsin. `madde_no` gömülen metnin parçası
(`kanun_adi + madde_no + text`), o yüzden 485 satırın gömmesi değişti → **harness k=10
yeniden koşuluyor**.

### S4 — İsabet denetimi tasarımı *(borç B1)* ⭐ en zor, en değerli

Bugünkü açığın **tamamı** burada: atıf gerçek, doğrulanır, kapıdan geçer, **soruya uymaz**.
Bu tur **kod değil tasarım** işidir — ≥2 alternatif trade-off'uyla sunulur, ADR yazılır,
sonra kodlanır. *(Aday eksen: getirilen parça ile cevabın örtüşmesi · kaynak-yeterliliği
sinyali · ikinci geçiş yeniden-sıralama.)*

**⚠️ 2026-08-05 — S1 ve S3 S4'ün girdisini değiştirdi:**
- Sınıfın büyüklüğü **14/80 → 7/80** (k=10 ile). Yani S4 artık **daha küçük** bir açığı
  hedefliyor; buna karşılık **aşırı-red** (altın bağlamdayken çekinme) **15/80** ile k'dan
  bağımsız duruyor ve coverage kaybının **daha büyük** yarısı orada.
- S3'ün mekanizma bulgusu doğrudan tasarım girdisi: çekinme sinyali bağlamın **konusal
  uyumundan** geliyor, **soruyu cevaplamaya yeterliliğinden** değil. *"Kaynak-yeterliliği
  sinyali"* aday ekseni bu yüzden **birinci sıraya** çıkıyor.
- Yeni aday eksen: **soru-belirginliği sinyali** (S3'ün etiketi ürüne taşınır — belirsiz
  soruda cevap yerine **açıklama iste**).

#### ✅ S4 KAPANDI 2026-08-05 — [ADR-0055](docs/adr/0055-isabet-denetimi-ekseni.md) yazıldı, **kod açılmadı**

**Karar: isabet denetimi cevap-SONRASI örtüşme ekseninde değil, cevap-ÖNCESİ
KAYNAK-YETERLİLİĞİ ekseninde kurulur.**

Gerekçe, S1+S3'ün birlikte ölçtüğü şeyden çıktı: **B1 ile aşırı-red aynı madalyonun iki
yüzü** — biri yetersiz kaynakta cevaplıyor (7/80), diğeri yeterli kaynakta çekiniyor
(15/80). Tek bir eksik sinyal iki hatayı birden üretiyor.

❌ **Reddedilen (A) — cevap↔kaynak örtüşme denetimi:** B1'in **çekirdek vakasında kör**.
B1'de model *başka bir gerçek maddeden* cevaplıyor ve cevabı gerçekten o maddede temelli →
örtüşme **yüksek** çıkar, denetim yakalaması gereken 7 vakaya tam not verir. Üstelik
uydurma madde no **0/120 ölçüldü**; bu denetimin sınıfı zaten **boş**. *Ölçülmüş boş bir
sınıfa deterministik denetim yazmak, S2'de sınıf A'yı elemekle aynı hata olurdu.*

🔁 **Ayrı tutulan (C) — ikinci geçiş yeniden-sıralama:** isabet denetimi değil **erişim
iyileştirmesi**; ama dikkat dağılmasının (0,9230 → 0,8426) ölçülmüş çaresi olabilir. Kendi
ön-kayıtlı tahminiyle **ayrı** ölçülür — B ile aynı turda ölçülürse hangisinin kazandırdığı
ayrılamaz.

**İlk deney bedeli sıfır:** `gen_eval_grounded.py`'de `--sufficiency-preamble` bayrağı
**zaten var**. Ön-kayıtlı kabul: *kütle artar **ve** çekinme sıralaması belirsiz alt kümede
ayırt ediciyi geçer*; düşerse B-i elenir, çapraz-kodlayıcıya geçilir.

---

> **Bu belge icra dokümanıdır ve `/goal sprint3.md` ile otonom koşulur.**
>
> ### ⭐ HER KOŞUDAN ÖNCE OKU
> [`docs/record/yurutme-tuzaklari.md`](docs/record/yurutme-tuzaklari.md) — bu hattın hata sınıfı
> **çökme değil, sessiz yanlışlık**. Sprint 2 buraya **6.10 · 6.11 · 6.12**'yi ekledi.

---

## 🎯 HEDEF — ✅ **SAĞLANDI 2026-08-04** *(kayıt; canlı iş yukarıdaki ▶ SIRADAKİ)*

```
koşul     : harness kuruldu (retriever + atıf doğrulayıcı + red kapısı) ve
            HARNESS AÇIK ölçüm yapıldı, harness kapalıyla yan yana raporlandı
🛑 DURMA  : kırmızı kapı · geçerlilik kapısı düşerse · bütçe aşımı
            · ⛔ tasarım kararları çözülmeden kod yazılmaz (aşağıda)
kapsam    : adım 0-4.  Graph-RAG, ajanlar, vatandaş kipi bu hedefin DIŞINDA
bedel     : GPU $0 (harness CPU'da) · hakem ~$1 · gömme modeli indirme
```

## Neden harness — karar gerekçesi (insan, 2026-08-03)

> ### ⚠️ 2026-08-04 — bu dört gerekçe ÖLÇÜLDÜ, ikisi ayakta değil
>
> Metin **olduğu gibi bırakıldı** (karar o gün bu gerekçelerle verildi, kayıt bu).
> Ölçümün hükmü:
>
> | # | gerekçe | hüküm |
> | :-- | :--- | :--- |
> | 1 | ortada ürün yok | ✅ **doğruydu** — retriever kuruldu, kullanıcı artık madde yapıştırmıyor |
> | 2 | iki açığı **kod** kapatır | ❌ **A1 ayağı ÇÜRÜDÜ** · ⏸ **M2b ayağı sınanmadı** |
> | 3 | şimdi eğitmek yanlış dağılıma eğitmek olur | ❌ **ZAYIFLADI** — retriever bağlamı daha *az* tuzaklı çıktı |
> | 4 | canlı mevzuat = kategori farkı | ⏸ **SINANMADI** — canlı katman kurulmadı (borç B6) |
>
> **2 neden çürüdü:** *"A1 0,909 → atıf doğrulayıcı uydurulan madde numarası yakalar"*
> diyordu. Ölçüldü: **uydurulmuş madde numarası SIFIR** (harness açık 89/89 doğrulandı,
> kapalı 87/89 — kalan 2'si "ayrıştırılamadı", uydurma değil). Doğrulayıcının yakalayacağı
> bir şey yoktu; model numara uydurmuyor, bağlamdaki etiketi kopyalıyor. A1'in açığı
> fabrikasyondan **gelmiyormuş** — **14/80** soruda altın gelmeden *başka bir gerçek*
> maddeden cevaplanmasından geliyor. O atıf doğrulanır, kapıdan geçer, soruya uymaz
> → **borç B1**. `M2b` ayağı ise çürümedi, **harness açık m2b hiç koşulmadı**.
>
> **3 neden zayıfladı:** *"gerçek retriever ~5 gürültülü parça verecek"* deniyordu.
> Ölçüldü: retriever bağlamında A1 **0,9344**, elle kurulmuş çeldiricili m1 bağlamında
> **0,9087**. m1'in 4 hard-negative çeldiricisi retriever'ın 5 konusal maddesinden
> **daha** tuzaklıymış. *"Önce harness, sonra eğitim"* sıralamasının bu dayanağı düştü.
>
> > 🚨 **2026-08-05 — bu paragrafın sayısı iki kez düzeltildi.** (a) 0,9344 yanlış metrikle
> > üretilmişti, doğrusu **0,9230** (tuzak 2.16). (b) Daha önemlisi: bulgu **k'ya bağlıymış**.
> > `k=10`'da aynı sayı **0,8426 < 0,9087** — yani retriever bağlamı m1'in çeldiricili
> > bağlamından **daha az tuzaklı değil**, yalnız **k=5'te** öyleydi. *"3 neden zayıfladı"*
> > hükmü bu yüzden **geri alınıyor**: bağlam uzadıkça tuzaklılık artıyor ve bu ölçüldü
> > ([#54](docs/record/research_log/2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md)).
>
> Kaynak: [research_log #51](docs/record/research_log/2026-08-04-harness-acik-ilk-olcum.md)
> · düzeltme [#54](docs/record/research_log/2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md)

**1. Şu an ortada ürün yok.** Model çalışsın diye kullanıcının **mevzuat metnini
kendisi yapıştırması** gerekiyor. Vatandaş bunu yapamaz — hangi maddeyi arayacağını
bilse zaten asistana ihtiyacı olmazdı.

**2. Üç açığımızdan ikisini kod kapatıyor, eğitim değil.**

```
M2b 0,877 → red kapısı        doğrulanamayan atıf = cevap reddedilir   deterministik
A1  0,909 → atıf doğrulayıcı  uydurulan madde numarası yakalanır       deterministik
```

**3. Şimdi eğitmek yanlış dağılıma eğitmek olur.** Eval şu an modele temiz bir madde
veriyor; gerçek retriever ~5 gürültülü parça verecek. Modeli bugünkü girdiye göre
optimize edip yarın girdiyi değiştirmek işi iki kez yapmaktır.

**4. Kategori farkı.** Canlı mevzuat API'si çalışıyor. Harness'lı model **bugünün
mevzuatını** cevaplar; kapalı ağırlıklı rakipler cevaplayamaz. Model reçetesiyle
elde edilemeyecek üstünlük.

---

## ⛔ TASARIM KARARLARI — kod yazılmadan çözülür

### K1. Gömme modeli (embedder) — ✅ **ÇÖZÜLDÜ 2026-08-04** (S3a ön-probu)

**Karar: `BAAI/bge-m3`, BM25 ile RRF hibriti içinde.** Ölçümle seçildi, etiketle değil.

| yöntem | recall@10 | recall@20 | kaçan (80'de) |
| :--- | ---: | ---: | ---: |
| BM25 | 0,625 | 0,750 | 20 |
| `intfloat/multilingual-e5-base` | 0,700 | 0,750 | 20 |
| `BAAI/bge-m3` | 0,800 | 0,863 | 11 |
| ⭐ **hibrit** (BM25 + bge-m3, RRF) | **0,875** | **0,925** | **6** |

BM25 tek başına en zayıf ama hibritte bge-m3'e **+0,075** ekliyor — iki yöntem farklı
soruları kaçırıyor. Maliyet: bge-m3 CPU'da indeksleme ~2-3 sa (bir kerelik), sorgu anında
kaba kuvvet arama **8,2 ms** / indeks **83 MB** fp16 → **vektör veritabanı gerekmiyor**
(bu ölçekte ANN bile gereksiz; gerekçe research_log #49 §7).

⚠️ **Sayılar bu soru kümesinin tavanı, retriever'ın değil** — aşağıya bak (S3a sonucu).

### K2. Chunk birimi — ✅ **ÇÖZÜLDÜ** ([ADR-0054](docs/adr/0054-harness-tasarim-kararlari-k2-k5.md))

**Tam madde indekslenir; 900 karakter kırpması yalnız bağlam modele verilirken uygulanır**
— yani bugünkü eval'de uygulandığı noktada. Eval-ayna kuralının öznesi **modelin girdisi**,
indeks değil; indeksi de kırpmak uzun maddelerin sonundaki hükümleri **aranamaz** yapardı.

**Bedel (kabul edildi, ölçülecek):** retriever'ın eşleştiği metin ≠ modelin gördüğü metin.
*"Getirildi ama cevap kırpılan kısımdaydı"* vakası harness-AÇIK tablosunda **ayrı sayılır**.
**Yan sonuç:** S3a sayıları tam madde üzerinde ölçüldü → aynen geçerli.

### K3. Statik korpus mu, canlı API mi — ✅ **ÇÖZÜLDÜ** (statikle başla)

Harness `data/corpus/mevzuat_maddeler.jsonl` üzerine kurulur; canlı `bedesten` katmanı
S3'ten **sonra**. Gerekçe ölçüm tekrarlanabilirliği — canlı içerik koşular arasında
değişirse harness-AÇIK sayıları kıyaslanamaz. S3a sözleşmenin geçerli olduğunu doğruladı,
yani bu bir **risk** değil **sıralama** kararı.

### K4. ⭐ HARNESS AÇIK ölçüm protokolü — ✅ **ÇÖZÜLDÜ** ([ADR-0054](docs/adr/0054-harness-tasarim-kararlari-k2-k5.md))

**`core_hard.jsonl` DEĞİŞTİRİLMEZ.** Her soruya *"kendi başına ayırt edici mi"* etiketi
eklenir, harness sayıları **iki alt kümede ayrı** raporlanır. Etiket **erişim sonucundan
kör** bir hakemle atanır (hakem soruyu görür, altın maddeyi ve retriever'ın onu bulup
bulmadığını görmez); istem etiketleme koşulmadan önce yazılır.

Neden küme değiştirilmiyor: sayı görüldükten sonra küme değiştirmek *"cilaladılar"* diye
okunur — tuzak 6.9'un veri tarafındaki karşılığı: **sonucu gördükten sonra ölçüt değil
alet düzeltilir.** Etiket kümeyi değiştirmeden aleti keskinleştiriyor.

⚠️ **Kaydedilen çekince:** bu ekseni ölçme fikri sonuçtan doğdu (kaçan sorular görülerek).
Ayrım korunuyor: ölçülen büyüklük ön-kayıtlı değil, ama **alet sonuca göre ayarlanmadı**.

Aşağıdaki ölçüm tasarımı yürürlükte:

Mevcut modlar modele bağlamı **doğrudan** veriyor: m1 altın madde · m2 yanlış madde ·
m2b çeldiriciler. Harness açıkken bağlamı **retriever** belirler. Bu **yeni bir
ölçüm** ve tasarlanması gerekir:

```
soru → retrieve(k) → model cevaplar → atıf doğrula → kapı → cevap / red
```

Ölçülecekler:
- **recall@k** — retriever altın maddeyi buluyor mu (modelden bağımsız)
- **uçtan uca** — DEV sorularında, oracle bağlam yerine getirilen bağlamla
- **kapı isabeti** — korpusta cevabı olmayan sorularda kapı reddediyor mu

⚠️ Harness açık/kapalı sayılar **yan yana** raporlanır; harness kapalı olan
tarihî çıpalarla (base · Gemini · `τ_g` · `τ_a`) kıyaslanabilirliği korur.

### K5. Red kapısı eşiği

[ADR-0038](docs/adr/0038-red-kapisi-esigi-kati.md): **katı** — tek doğrulanamayan
atıf tüm cevabı reddettirir. Karar duruyor; harness açıkken **aşırı-red** yaratıp
yaratmadığı ölçülecek (kütle ekseni).

---

## ▶ ADIMLAR

```
S3a) ÖN-PROB                ✅ KAPANDI  hibrit recall@10 0,875 · bedesten GEÇERLİ
0) MODÜL-BAŞINA NORM        🔴 REDDEDİLDİ  kütle ≤ %56,2 < %71,6 · hakem $0
1) RETRIEVER                ✅ BİTTİ    bileşen + indeks, recall@10 0,8750 birebir
2) ATIF DOĞRULAYICI         ✅ BİTTİ    deterministik, hakemsiz · 4+1 sessiz hata düzeltildi
3) RED KAPISI               ✅ BİTTİ    ADR-0038 katı + 2 ablasyon
4) HARNESS AÇIK ÖLÇÜM       🛑 ÖLÇÜLDÜ  ürün sayısı ilk kez görüldü → İNSANA SUNULDU
```

### 🛑 Adım 4 sonucu — harness AÇIK ↔ KAPALI, aynı model (`tgta_v1`)

> 🚨 **2026-08-05 düzeltmesi:** aşağıdaki A1/kütle sayıları **yanlış metrikle** üretilmişti
> (tuzak **2.16** — `A1` diye ham makro). Tablo **kayıt olarak duruyor**, doğruları üstü
> çizili yanına yazıldı. Ürünün güncel ayarı **k=10** — güncel tablo [S1'de](#s1--k-süpürmesi-borç-b3--kapandı-2026-08-05--k10-kabul--research_log-54).

| eksen | harness **KAPALI** (m1) | harness **AÇIK** (h1, k=5) |
| :--- | ---: | ---: |
| altın madde bağlamda | **garanti** (kurgu) | **60/80** — `recall@5` 0,750 |
| coverage | 0,7875 | **0,7500** |
| A1 (cevaplanan-only) | 0,9087 | ~~0,7823~~ → **0,7591** |
| **kütle = coverage × A1** | **%71,6** | ~~%58,7~~ → **%56,9** |
| ⭐ A1 · **altın getirilen** alt küme | 0,9087 | ~~0,9344~~ → **0,9230** |
| doğrulanan atıf | 87/89 | **89/89** |
| **uydurulmuş madde numarası** | 0 | **0** |
| katı kapı reddi | 2/80 | **1/80** |

**Üç okuma** (tamamı [research_log #51](docs/record/research_log/2026-08-04-harness-acik-ilk-olcum.md)):

1. **Ürün sayısı oracle sayısından düşük — ve olması gereken bu.** Düşüşün tamamı erişimden:
   soruların %25'inde altın madde ilk 5'e girmiyor. Ölçüm dürüstleşti.
2. ⭐ **Retriever doğru maddeyi bulduğunda model DAHA sadık** (A1 0,9344 > 0,9087). Yani
   *"gerçek retriever daha gürültülü bağlam verir"* varsayımı — S3'e girerken yazdığımız
   gerekçelerden biri — **bu ölçümde doğrulanmadı**. Darboğaz model değil **erişim**.
3. ⚠️ **Kapının sınırı.** Model madde numarası **uydurmuyor** (0/89), bağlamdaki etiketi
   kopyalıyor; bu yüzden katı kapı yalnız 1 cevap reddetti. Asıl hata şurada: **14/80**
   soruda altın gelmeden cevaplandı — atıf **gerçek**, doğrulanır, kapıdan geçer, ama
   soruya uymuyor. Atıf doğrulayıcısı *"uydurulmuş atıf"*ı çözüyor, *"gerçek ama soruya
   uymayan madde"*yi çözmüyor. **S3'ün asıl açığı bu.**

```
altın geldi   → cevapladı   46
altın geldi   → çekindi     14
altın GELMEDİ → cevapladı   14   ← A1'i düşüren sınıf
altın GELMEDİ → çekindi      6
```

### S3a — ÖN-PROB · $0 · ~1 gün · ⭐ ÖNCE BU

1-2 aylık bir sprinte girmeden **planın iki temel varsayımını** sınar. İkisi de model çağrısı,
hakem ve GPU **gerektirmez**.

#### Prob 1 — `recall@k`: retriever altın maddeyi buluyor mu

DEV soruları maddelerden üretildi; her sorunun altın `kanun_adi + madde_no`'su **biliniyor**.
Saf bilgi-erişim ölçümü.

**Sırayla, ucuzdan pahalıya:**

```
1. BM25             gömme YOK · indeks dakikalar · TAMAMEN BEDAVA
2. multilingual-e5  CPU · model indirme
3. bge-m3           CPU · uzun bağlam
4. hibrit           BM25 + yoğun — ilk üçü yetmezse
```

> **BM25 neden ilk:** hukuk metni ayırt edici terimlerle dolu (kanun adları, madde numaraları).
> Sözlüksel arama burada beklenenden güçlü olabilir ve **taban çizgisi** kurar. Yoğun gömme
> BM25'i geçemiyorsa gömme modeli seçmenin anlamı yok. *(Bu aynı zamanda K1'i çözer.)*
>
> ⚠️ **2026-08-04 — öngörü tersine çıktı.** BM25 *"beklenenden güçlü"* değil, **en zayıf**
> yöntem oldu: `recall@10` **0,625** — ön-kayıtlı **"<%70 → DUR"** bölgesinde. Yoğun gömme
> onu her k'da geçti (bge-m3 0,800). **Ama merdivenin mantığı yine de işe yaradı:** BM25 tek
> başına zayıfken hibritte bge-m3'e **+0,075** ekledi (0,800 → **0,875**) — iki yöntem
> **farklı** soruları kaçırıyor. Yani *"taban çizgisi kur"* gerekçesi tuttu, *"tek başına
> yetebilir"* öngörüsü tutmadı.

**⛔ ÖN-KAYITLI KARAR EŞİKLERİ — sayı görülmeden yazıldı:**

| `recall@10` | S3 ne olur |
| :--- | :--- |
| **≥ %90** | plan tarif edildiği gibi koşar |
| **%70-90** | **hibrit** eklenir, S3 büyür |
| **< %70** | 🛑 **DUR, insana sor** — sorun korpus yapısında, S3'e girilmez |

`recall@1/5/10/20` eğrisi de çıkarılır → modele kaç parça verileceğini o belirler.

#### Prob 2 — bedesten sözleşmesi hâlâ geçerli mi

```
scripts/bedesten_probe.py  →  arama · tam metin · madde ağacı
⚠️ Türk IP gerekiyor (gov firewall)
```

Güncellik iddiamızın **tek dayanağı** bu ve sözleşme 2026-06-07'den beri doğrulanmadı.
Değişmişse: retriever statik korpusla sürer ama **güncellik iddiası DÜŞER** →
[`ROADMAP.md`](ROADMAP.md) + [`MODEL_CARD.md`](MODEL_CARD.md) düzeltilir.

#### 📋 Uygulama planı hazır

[`docs/plans/2026-08-03-s3a-on-prob.md`](docs/plans/2026-08-03-s3a-on-prob.md) — 5 görev,
TDD adımlarıyla, gerçek kodla. İlk görev **madde anahtarı normalleştirme**: altın etiketi
korpusa bağlayan çekirdek, kendi testleriyle. *(Plan yazılırken burada bir hata bulundu:
`Geçici Madde 1` ile `Madde 1` aynı sayılınca 40.496 madde 27.706 anahtara düşüyor ve
recall sessizce şişiyor — test olarak çivilendi.)*

⚠️ **S3'ün planı YAZILMADI, bilinçli.** S3a'nın sonucu S3'ün şeklini belirliyor; probu
koşmadan S3 planı yazmak, probun engellemek için var olduğu şeyi yapmak olur.

#### S3a çıkış ölçütü — ✅ **KAPANDI 2026-08-04**

```
✅ recall@1/5/10/20 eğrisi ölçüldü, en iyi yöntem seçildi (K1 çözüldü)
✅ eşik kararı verildi ve S3'ün boyutu buna göre kesinleşti
✅ bedesten sözleşmesi sınandı, sonucu kayda geçti
→ research_log #49 · çıktılar outputs/eval/s3a-on-prob/
```

**Eşik kararı: `recall@10` = 0,875 → %70-90 bandı → 🟡 HİBRİT, S3 büyür.**
Merdivenin 4. basamağı S3a içinde koşulduğu için "S3 büyür" = **retriever hibrit olur**,
ayrı bir keşif turu değil.

**Bedesten: ✅ GEÇERLİ** (4/4 çağrı `SUCCESS`, İş Kanunu M1 `guncellemeTarihi` 2026-05-07)
→ güncellik iddiası ayakta, `ROADMAP.md`/`MODEL_CARD.md` düzeltmesi **gerekmiyor**.
⚠️ Prob betiğinin kendisi bozuktu (`documentId` arıyordu, alan `mevzuatId`) ve API
çalışırken *"sözleşme bozuk"* raporluyordu — düzeltildi, **tuzak 7.1**.

#### ⭐ S3a'nın planlanmamış bulgusu — insana

**DEV soru kümesi erişim ölçümü için yetersiz belirlenmiş.** Kaçırılan soruların hemen
tamamı hangi kanuna ait olduğunu söylemiyor (*"Başvurum kabul edilirse ne olur?"*,
*"El konulan gönderilerim ne olacak?"*). Ölçüldü: aynı BM25, aday havuzu altının **kendi
kanunuyla** sınırlanınca `recall@10` **0,625 → 0,875**.

`core_hard.jsonl` altın madde elde tutularak üretildi — **grounded QA kümesi, retrieval
kümesi değil.** Sonuç: `recall@k` sayılarımız retriever kabiliyetinin değil **bu kümenin**
tavanı. → **tuzak 7.4**, ve **K4'ü (harness-AÇIK protokolü) doğrudan etkiliyor**:
protokol bu kümeyle mi kurulacak, yoksa ayırt edici sorulardan oluşan bir alt küme mi
gerekiyor? ⚠️ Sayı görüldükten sonra küme değiştirmek dışarıdan *"cilaladılar"* diye
okunur — **karar insanın, ADR'ye yazılır.** Öneri: küme **değiştirilmez**, yanına
"kendi başına ayırt edici mi" etiketi eklenir, sayılar iki alt kümede **ayrı** raporlanır.

---

### Adım 0 — modül-başına normalleştirme *(harness'tan bağımsız, önce yapılır)*

Merge'in **bilinen** kusuru: `τ_a` seyreliyor (tekil 0,987 → merge 0,877).
Normalleştirme şu an **global** (tek `‖τ‖_F`). Ölçüldü: iki kolun da en büyük normu
**aynı MLP yüzeyinde** — `gate_proj` (τ_g 6,150 ↔ τ_a 0,621) · `up_proj`
(5,047 ↔ 0,628). Global norm bunu göremiyor.

```
python scripts/merge_ties.py --base Qwen/Qwen3.5-4B \
  --adapter tg=outputs/tg_v1 --adapter ta=outputs/ta_v1 \
  --norm-kapsam modul ...                       ← ~20 satır, henüz YOK
bash scripts/cp3_merge_dene.sh models/merged/<yeni> modul
```

**Kabul:** M2b > 0,877 **ve** M1 kütlesi ≥ %71,6 (ikisi birden — tek eksen yeter değil).
Tutmazsa `v0.1` yerinde kalır, kayıp 1 saat. `open_questions.md`'de açık soru olarak
duruyor.

#### 🔴 KAPANDI (2026-08-04) — reddedildi · [ADR-0053](docs/adr/0053-modul-basina-norm-kapsami-reddedildi.md) · research_log #50

`--norm-kapsam {global,modul}` **yazıldı** (`scripts/merge_ties.py`), merge koştu (224/224).

**① Adım 0'ın gerekçesi ölçümde durmuyor.** *"İki kolun da en büyük normu aynı MLP
yüzeyinde, global norm bunu göremiyor"* — ölçüldü: kolların modül profilleri neredeyse
**orantılı**, τ_g/τ_a oranı 11 yüzeyin hepsinde **7,2–10,1**. Global normalleştirmeden
sonra payları zaten eşitleniyor (τ̂_a/τ̂_g = **0,88–1,24**). Yani `τ_a` bir **kapsam
artefaktı** yüzünden silinmiyor.

**② Ama modül-başına kapsam yine de no-op değil** — ölçüldü, ağırlık uzayında:
`‖W_modül − W_global‖ / ‖W_global − base‖` = **0,272**. Yön %27 değişiyor, **genlik
değişmiyor** (‖Δ‖ 1,3835 ↔ 1,3865). Farkın kaynağı TIES'in doğrusal-olmayan işaret
seçimi. Bu yüzden eval **koşuluyor** — akıl yürütmeyle değil ölçümle kapanacak.

**Bütçe sırası:** kabul bir **VE** koşulu ve genlik `min`'le aynı olduğu için düşmesi
beklenen eksen **kütle**. Bu yüzden önce **yalnız m1** koşuluyor; kütle düşerse m2b/m2
üretimi ve hakem parası harcanmıyor.

**③ SONUÇ 🔴 — kabul ölçütü düştü, hakem hiç çağrılmadı.** Geçerlilik kapısı geçildi
(kesik %1,2). Cevaplanan **45/80** → coverage **%56,2**. Kütle = coverage × A1 olduğundan,
**A1 = 1,000 olsa bile** kütle ≤ %56,2 < gereken **%71,6**. A1'i ölçmek sonucu
değiştiremezdi → m2b/m2 koşulmadı, **hakem maliyeti $0**.

| varyant | cevaplanan | A1 | **kütle** | M2b red |
| :--- | ---: | ---: | ---: | ---: |
| `ham` = yayınlanan `tgta_v1` | 63/80 | 0,909 | **%71,6** | 0,877 |
| `min` (global norm-dengeli) | 43/80 | 0,994 | **%53,4** | 0,987 |
| **`modulmin`** (bu adım) | **45/80** | ölçülmedi | **≤ %56,2** | ölçülmedi |

Modül-başına kapsam global `min`'i **tekrarladı**. %27'lik yön farkı aşırı-reddi
kurtarmadı — çünkü aşırı-reddi yaratan **yön değil genlik**: her iki kapsamda da `τ_g`
kendi eğitim genliğinin ~1/9'una iniyor ve zeminleme zayıflıyor.

**`v0.1` yerinde kalıyor.** `--norm-kapsam` bayrağı kodda kaldı (varsayılan `global`).
⚠️ `τ_a`'nın merge'de seyrelmesi **hâlâ açık** — çözüm merge parametresinde değil,
muhtemelen `τ_a`'nın **eğitim genliğinde** (82 adım @1e-5 çok kısaydı).

---

## Değişmezler

```
ölçüm     thinking on · 1024+512 · seed 3407 · chunk 900 · Q4_K_M + llama-server
havuz     data/eval/dev/ — DEV. frozen TEST (data/eval/canon/) sürüm kabul testi,
          yayın öncesi BİR KEZ
hakem     gpt-4o-mini · kapı openrouter · LLM_PROVIDER_ORDER=OpenAI PİNLİ
harness   CPU'da — gömme, indeks, doğrulayıcı GPU'ya GİRMEZ (sığar/sığmaz farkı)
🛑 geçerlilik kapısı: kesik > %5 → koşu geçersiz, puanlamaya para harcanmaz
```

> ### 🚨 TEK EKSENLE OKUMA — Sprint 2'nin en pahalı dersi
> A1 **cevaplanan-only**; çekinerek kazanmayı ödüllendirir. Ölçüldü: `τ_a` A1
> **0,9697** (en yüksek) ama kütle %41,2 · dejenere merge A1 **1,0000** (tavan) ama
> 80 sorudan **2'sini** cevaplıyordu.
>
> **Her tabloda kütle = coverage × A1.** Red kapısı **tanımı gereği** aşırı-red
> üretebilir — bu eksen olmadan kapı "başarılı" görünür.

> ### 🚨 Geçerlilik kapısı düşerse reçeteye körü körüne uyma
> Kapı *"`MAXTOK` büyüt"* der. Sprint 2'de kesiklerin tamamı **tekrarlama
> döngüsüydü** — bütçe darlığı değil model hasarı. Ayrıca `MAXTOK` bir **rejim
> değişmezi** (ADR-0043). **Önce kesikleri gözle oku.**

---

## Koşu öncesi kısa liste

- [ ] Modal panelden bakiye (defterden türetme — 6.3) · **kalan ~$22,31**
- [ ] Eklenen her bayrak **çağrı zinciri uçtan uca** izlendi mi: betik →
      orkestratör → komut → **künye** (6.12: Sprint 2'de **dört kez** ısırdı)
- [ ] Eval sonrası: kesik oranı %5 altında mı · **kütle** A1'in yanında mı
- [ ] Her bulgu **aynı gün** `research_log` + gerekirse ADR (numaralandırma
      **0053**'ten, `research_log` **#49**'dan devam)

## 📌 BU BELGE CANLI TUTULUR

⚠️ **Canlı kısım artık başlıktaki [▶ SIRADAKİ](#-sıradaki--goal-sprint3md-bunu-koşar)
bölümü.** Adım 0-4 kapandı; onların metinleri **kayıt** olarak duruyor, üzerine yazılmaz.

- **Adım başlarken:** 🟡 KOŞUYOR + ne koşuyor
- **Adım biterken:** ✅/🔴 · **fiili sayılar** · çıktı nerede · hangi kayıt
- **Karar insana gittiğinde:** aynı gün ADR + `research_log`

*Sohbette kalan bulgu, kaybolmuş bulgudur.*

## Durum tablosu

| adım | durum | çıktı |
| :--- | :--- | :--- |
| **K1** gömme modeli | ✅ **çözüldü** | `bge-m3` + BM25 hibriti (RRF) — research_log #49 |
| **K2-K5** tasarım kararları | ✅ **KİLİTLENDİ** 2026-08-04 | [ADR-0054](docs/adr/0054-harness-tasarim-kararlari-k2-k5.md) — ⛔ kilidi açıldı, Adım 1-4 kodlanabilir |
| **S3a** ön-prob (recall@k + bedesten) | ✅ **KAPANDI** 2026-08-04 | hibrit `recall@10` **0,875** · bedesten ✅ GEÇERLİ · `outputs/eval/s3a-on-prob/` · research_log #49 |
| **0** modül-başına norm | 🔴 **REDDEDİLDİ** 2026-08-04 | kütle ≤ %56,2 < %71,6 · hakem **$0** · [ADR-0053](docs/adr/0053-modul-basina-norm-kapsami-reddedildi.md) · research_log #50 |
| **1** retriever | ✅ **BİTTİ** 2026-08-04 | `scripts/retriever.py` + `data/index/mevzuat_bge_m3/` (40.496 madde, 83 MB) · bileşen S3a sayısını birebir üretti: **recall@10 0,8750 · @20 0,9250** · 759 ms/sorgu (CPU) |
| **2** atıf doğrulayıcı | ✅ **BİTTİ** 2026-08-04 | `scripts/atif_dogrula.py` — hakemsiz. Gerçek çıktıda 56 atıf · 53 doğrulandı · **0 yanlış alarm** · pozitif kontrol geçti. Gözle denetim **dört** yanlış-alarm hatası buldu (ad çakışması · başlık biçimi · Türkçe `upper()` · ada kaçan sözcük) |
| **3** red kapısı | ✅ **BİTTİ** 2026-08-04 | `scripts/red_kapisi.py` — ADR-0038 katı + `cogunluk`/`cerrahi` ablasyonları, üçü post-hoc aynı kümede |
| **4** harness AÇIK ölçüm | ✅ **ÖLÇÜLDÜ 2026-08-04** ⚠️ sayıları 08-05'te düzeltildi | kütle **%71,6 → ~~%58,7~~ %56,9** · ⭐ altın getirilince A1 **~~0,9344~~ 0,9230 > 0,9087** · uydurulmuş atıf **0/89** · `outputs/eval/s3-harness-acik/` · research_log **#51** + düzeltme **#54** |
| **S1** `k` süpürmesi (B3) | ✅ **KAPANDI 2026-08-05 — `k=10` KABUL** | kütle **%56,9 → %59,5** (+2,6) · `recall@10` **0,875** (70/80) · ⚠️ bedeli ölçüldü: altın getirilende A1 **0,9230 → 0,8426** (dikkat dağılması) · B1 sınıfı **14 → 7**, aşırı-red **14 → 15** (değişmedi) · 🚨 **tuzak 2.16** bulundu ve 8 belge düzeltildi · hakem **$0,0403** · `outputs/eval/s3-harness-k10/` · research_log **#54** |
| **S3** ayırt-edicilik etiketi (B2) | ✅ **KAPANDI 2026-08-05** | kör hakem, istem ön-kayıtlı · **62 ayırt edici / 18 belirsiz (%22,5)** · `recall@5` **0,8226 ↔ 0,5000** (tuzak 7.4 doğrulandı) · ⭐⭐ **ters çekinme kalibrasyonu** bulundu (belirsizde %5,6, ayırt edicide %30,6 çekinme) · hakem **$0,0069** · `outputs/eval/s3-ayirt-edicilik/` · research_log **#53** |
| **S2** yürürlük alanı (B7) | ✅ **KAPANDI 2026-08-05 — B7 KAPANDI** | `mulga`+ilga alanı **2.547 satır** (%99,6 kaynaklı) · alt-madde kimliği **485 satır** · `atif_dogrula.py`'ye **`MULGA`** hükmü (`red_kapisi` değişmedi) · kabul 3/3 ✅ (1475/15 MULGA · 1475/14 yürürlükte · katı kapı REDDETTİ · yanlış-pozitif 0) · ⭐ **kapsam ölçümden seçildi:** sınıf A modele **0/800** ulaşıyor → elenmedi (**B9**) · 🐞 iki kural verify hedefine çarpıp düzeldi (sonek **%80 eksikti**: 98 → **485**; ilga kaynağı **tarihi kanun sanıyordu**) · ⚠️ **dürüst negatif:** `MULGA` **0**, hükmü değişen cevap **0/80** — mekanik kapandı, bu kümede tetiklenmedi · hakem **$0** · research_log **#52 + #55** |
| **S4** isabet denetimi tasarımı (B1) | ✅ **KAPANDI 2026-08-05 — kod açılmadı** | [ADR-0055](docs/adr/0055-isabet-denetimi-ekseni.md): denetim **kaynak-yeterliliği** ekseninde kurulur · ❌ cevap↔kaynak örtüşme **reddedildi** (B1'in çekirdek vakasında kör; sınıfı zaten boş — uydurma no **0/120**) · 🔁 yeniden-sıralama **ayrı tur** (dikkat dağılmasının çaresi, ama karıştırılırsa ikisi de yorumlanamaz) · ilk deney **$0** (`--sufficiency-preamble` bayrağı zaten var) · ön-kayıtlı kabul yazıldı |

## 📌 Sprint 3'ün açık borçları — karar insanda

Hiçbiri Sprint 3'ü durdurmadı; hepsi **ölçülerek** ortaya çıktı ve S4'ün şeklini belirliyor.

| # | borç | neden önemli |
| :--- | :--- | :--- |
| **B1** ⭐ | **"Gerçek ama soruya uymayan madde"** — atıf doğrulayıcısı bunu yakalayamıyor. ~~14/80~~ → **7/80** (k=10 ile yarıya indi). | Ürün vaadi *"denetlenebilir"*. Bugün fabrikasyona karşı denetlenebilir, **isabetsizliğe karşı değil**. ⚠️ **2026-08-05 güncelleme:** A1 düşüşünün *tamamı* burada **değil** — **aşırı-red** (altın bağlamdayken çekinme, **15/80**) k'dan bağımsız ve coverage kaybının daha büyük yarısı orada. S4 iki eksene birden bakmalı. |
| ~~**B2**~~ ✅ | **KAPANDI 2026-08-05** — ayırt-edicilik etiketi koşuldu (kör hakem, ön-kayıtlı istem). **62/18**. | Tuzak 7.4 **sayıyla** doğrulandı: `recall@5` **0,8226 ↔ 0,5000** (32,3 puan). Bundan sonra hiçbir harness sayısı bu ayrım yapılmadan raporlanmaz. research_log **#53** |
| ~~**B3**~~ ✅ | **KAPANDI 2026-08-05** — `k=10` süpürüldü ve **kabul edildi** (kütle %56,9 → **%59,5**). | Kazanç tahminin (~%65) **altında**; bedeli ölçüldü: dikkat dağılması A1'i **8 puan** düşürüyor. `k=20` için gerekçe **zayıf**. research_log **#54** |
| **B4** | **`τ_a` merge'de seyreliyor** (0,987 → 0,877). Adım 0 bunun norm *kapsamı* olmadığını gösterdi. | Çözüm merge parametresinde değil, muhtemelen `τ_a`'nın **eğitim genliğinde** (82 adım @1e-5 kısa, ‖τ_a‖ = 1,18). Yani bir S4 eğitim işi. |
| **B5** | **K2'nin bedeli ölçülmedi**: *"getirildi ama cevap 900 karakter kırpmasının ötesindeydi"* vakası. İz kaydediliyor ama sayılmadı. | ADR-0054 bunu ayrı vaka sınıfı olarak saymayı şart koşmuştu. |
| **B6** | **Canlı `bedesten` katmanı** eklenmedi (K3: bilinçli erteleme). | Güncellik iddiası ayakta ama **kanıtlanmış değil** — S3a sözleşmenin çalıştığını doğruladı, ürün onu henüz kullanmıyor. |
| ~~**B7**~~ ✅ | **KAPANDI 2026-08-05 (S2).** Korpusa `mulga` + ilga eden kanun/madde/tarih eklendi (**2.547 satır**), alt-madde kimliği onarıldı (**485 satır**), `atif_dogrula.py`'ye **`MULGA`** hükmü kondu. `"İş Kanunu Madde 15"` artık üç red politikasında da **REDDEDİLİYOR**. ⚠️ **Dürüst negatif:** iki koşu yeniden puanlandı → `MULGA` **0**, hükmü değişen cevap **0/80**; açık mekanik olarak kapandı ama bu DEV kümesinde **tetiklenmedi** (`core_hard` yürürlükteki maddelerden üretildi, beklenebilirdi). **B7 bir ürün-güvenliği özelliği, skor özelliği değil.** research_log **#55**. Özgün kayıt aşağıda duruyor. |
| **B9** 🆕 | **Korpusta madde kimliği bozuk — tablo/cetvel parçaları madde diye indeksli** (~7.966 satır, `3520`'de yoğun; `", Ek"` gibi 4 karakterlik hücreler). S2'de **kasten elenmedi**. | ⭐ **Ölçüldü: modele 0/800 blok ulaşıyor** — parçalar öylesine kısa ki ne BM25 ne yoğun vektör üste çıkarıyor. Elemek **ölçülemez bir kazanç için ölçülmüş bir sayıyı harcamak** olurdu (indeks değişir → `recall@k` kayar → k=5/k=10 kıyası geçersizleşir). İndeks hijyeni olarak **kendi başına ve ayrıca ölçülerek** yapılır. ⚠️ Not: *"anahtar yinelenmesi %29,4"* ile *"bağlam kirlenmesi %1,8"* **ikisi de doğru** — farklı nesneleri ölçüyorlar. research_log **#55** |
| ~~**B7 özgün kayıt**~~ | **MÜLGA maddeye yapılan atıf doğrulamayı ve katı kapıyı GEÇİYOR.** Ölçüldü 2026-08-04: `"İŞ KANUNU Madde 15"` → `DOGRULANDI` (kanun_no **1475**) → kapı ✅. Oysa korpustaki metni: *"110- (Mülga: 22/5/2003/4857/120 md.)"*. | **Ürün-güvenliği açığı, akademik değil.** Vaadimiz *"denetlenebilir"*; burada sistem **yürürlükten kalkmış** bir hükme yapılan atıfı **doğrulanmış** damgalıyor. Korpusta yürürlük alanı **yok** — 4 alan var (`kanun_adi · kanun_no · madde_no · text`) ve ilga bilgisi yalnız **serbest metnin içinde**. Aynı ad iki kanuna ait olabildiği için (`İŞ KANUNU` = 4857 yürürlükte **ve** 1475 mülga) doğrulayıcı ayırt edemiyor. |

| **B8** | **Katı kapı, tek karakterlik yazım hatasına takılıyor.** Ölçüldü 2026-08-05 (k=10): model bağlamdaki `FİKİR VE SANAT ESERLERİ KANUNU`'nu `…ESELERİ…` diye kopyaladı (bir harf düştü); madde no'ları **doğru**, kanun bağlamda **var** → `KANUN_YOK` → tüm cevap **reddedildi**. Ayrıştırıcı ayrıca adın başını düşürüyor (`Fikir ve` atılıp `Sanat Eseleri Kanunu`). | Doğrulayıcının **ilk gerçek yakalayışı** ve o bir fabrikasyon değil **transkripsiyon hatası**. ADR-0038 kalibrasyonu resmî adın *kısa hâlini* çözmüştü, **yazım hatasını** çözmüyor. Katı kapıda her yanlış negatif **doğrudan coverage kaybı**. ⚠️ Tolerans (düzenleme uzaklığı) kapıyı **gevşetir** — ölçülmeden karar verilmez. |

### 🚨 B7 hakkında — bu, graph-RAG'in ölçülmüş gerekçesi

Bugüne kadar graph-RAG *"hukuk ilişkiseldir"* diye **varsayımla** savunuluyordu
([`VISION.md`](docs/VISION.md) Faz 2). Bugün ilk kez **ölçülmüş** bir gerekçe çıktı ve
beklenen yerde değil:

- ❌ **Erişim kalitesi için değil.** Recall eğrisi `@5` 0,750 → `@10` 0,875 → `@20` 0,925
  diyor; kalan açığın çoğu **k'yı büyütmekle** kapanıyor (borç B3, bedeli ~0). Ayrıca
  soruların ~%25'i konusunu hiç belirtmiyor — graf, belirsiz sorguyu düzeltemez.
- ❌ **Cevap kalitesi için de değil.** Altın getirildiğinde A1 zaten **0,934**; model
  ilişki çıkarımına ihtiyaç duymuyor.
- ✅ **Yürürlük ve atıf zincirleri için.** İlga/tadil ilişkisi, aynı adı taşıyan mülga
  kanunlar, *"yerine işlenmiştir"* kabuk maddeleri — **bunların hiçbiri düz vektör
  benzerliğinden okunamaz.** B7 tam bu sınıf.

⚠️ **Ama acil çözüm graf değil.** B7'nin ucuz çaresi korpusa **yürürlük alanı** eklemek
(`mulga: true/false` + ilga eden kanun/madde) — bu bir **veri** işi, graf değil. Graf, o
alan varken **atıf zincirleri** ve **çapraz referans** için hak eder. Sıralama:
**B7 (veri) → B3 (k) → B1 (isabet) → graf**.

📌 **Graf'ın mimari farkı, ön-kayıtlı tahmini ve gerçekten kazanacağı üç yer
[`ROADMAP.md` §5.2](ROADMAP.md)'de.** Özeti: bugünkü kümede graf **ölçülemez** bir
iyileşme üretirdi (sorular tek-madde, çok-hop yok, n=80'de ±2 soru gürültü) — bu yüzden
bugün koşulmadı; kurulursa **kendi soru kümesiyle** ölçülür.

## Bağlantılar

| ne | nerede |
| :--- | :--- |
| Ürün yol haritası | [`ROADMAP.md`](ROADMAP.md) · [`docs/VISION.md`](docs/VISION.md) Faz 2 |
| Model kartı ve sınırlar | [`MODEL_CARD.md`](MODEL_CARD.md) |
| Artefakt kimlikleri | ⭐ [`docs/record/kollar.md`](docs/record/kollar.md) |
| Mevzuat API sözleşmesi | [`docs/BEDESTEN_API.md`](docs/BEDESTEN_API.md) |
| Sprint 2 kapanışı | [`sprint2.md`](docs/_arsiv/sprint2.md) · [`defter.md`](docs/record/sprint2/defter.md) |
| Ertelenen iddia katmanı | [`sprint2b.md`](docs/_arsiv/sprint2b.md) — arxiv'e karar verilirse |
| **Koşu öncesi tuzaklar** | ⭐ [`yurutme-tuzaklari.md`](docs/record/yurutme-tuzaklari.md) |
