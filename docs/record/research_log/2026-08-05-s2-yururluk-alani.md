# #55 — S2: yürürlük alanı + madde kimliği (borç B7) · kapsam **menüden değil ölçümden**

**Tarih:** 2026-08-05 · **Sprint:** [`sprint3.md`](../../../sprint3.md) **S2**
**Betikler:** `scripts/korpus_yururluk.py` (yeni) · `scripts/atif_dogrula.py` (MULGA hükmü)
**Veri:** `data/corpus/mevzuat_maddeler.jsonl` (yazıldı, yedek alındı) ·
**İndeks:** `data/index/mevzuat_bge_m3_s2` (yeni dizin; eskisi korundu)

## 1. Kapsam kararı — yanlış soruyu sormaktan dönüldü

[#52](2026-08-05-korpus-butunlugu.md) korpusun bozuk olduğunu bulmuş ve S2'yi üç işe
büyütmüştü: `mulga` · alt-madde soneki · tablo-parçası eleme. Üçüncüsü indeksi değiştirip
o günkü `recall@k` sayılarını geçersiz kılacaktı, yani ucuz değildi.

Kapsam kararı **doğru soruya çevrilerek** verildi. Yanlış soru: *"korpus ne kadar bozuk?"*
Doğru soru: **"modelin GÖRDÜĞÜ bağlamda çöp var mı?"** — çünkü korpusta duran ama hiç
getirilmeyen bir satırın ürüne maliyeti yoktur. Ölçüm, k=10 koşusunun `context_shown`
alanı ayrıştırılarak **modele giden metnin kendisi** üzerinde yapıldı.

| bozulma sınıfı | korpusta | **modele ulaşan blok** | altın etiketi | karar |
| :--- | ---: | :--- | ---: | :--- |
| **A — tablo/cetvel parçası** | ~7.966 satır | **0 / 800** | — | **ertelendi (B9)** |
| **B — alt-madde soneki** | **485 satır** | **14 / 800 · 12 soru** | 3/80 | ✅ **yapıldı** |

**Sınıf A neden ulaşmıyor:** parçalar çok kısa — `", Ek"` (4 karakter),
`"7/8/2003 5162 4, Ek"` (19). Ne BM25 ne yoğun vektör onları üste çıkarıyor, RRF de
çıkaramıyor. Korpusu şişiriyorlar, **ölçülmüş erişim etkileri sıfır**.

Elemek **ölçülemez bir kazanç için ölçülmüş bir sayıyı harcamak** olurdu — bu repoda
[ROADMAP §5.2](../../../ROADMAP.md)'nin graph-RAG'i ertelerken kullandığı ölçütün aynısı.

### ⚠️ Yinelenme ≠ kirlenme

İlk sayım `(kanun_adi|madde_no)` anahtarı üzerinden yapılınca k=10'da *"26/80 soru bozuk
parça görüyor"* çıktı; `context_shown` üzerinden **6/80** (sonek kuralı düzeltilince 12/80).
Fark şu: **anahtar yinelenmiş olsa bile retriever o anahtarın doğru satırını getiriyordu.**
Biri korpusun özelliği, diğeri bağlamın. **Sayının hangi nesne üzerinde ölçüldüğü, sayının
kendisinden önemli** — aynı korpus için %29,4 ile %1,8 arasında gezinen iki doğru sayı var.

## 2. Yapılan iş

`scripts/korpus_yururluk.py` — **atomik yazma**: geçici dosyaya yaz → doğrula → `os.replace`.
Doğrulama düşerse korpus **değişmez** (POSD rollback gate).

| dönüşüm | satır | not |
| :--- | ---: | :--- |
| `mulga` + `ilga_eden_kanun/madde` + `ilga_tarihi` | **2.547** | ilga kaynağı çıkarılan **%99,6** |
| alt-madde soneki `madde_no`'ya taşındı | **485** | `Madde 31` → `Madde 31/a` |

`scripts/atif_dogrula.py` — **`MULGA`** hükmü. `_hukum` artık anahtar **seti** değil
**indeks sözlüğü** alıyor; maddenin *varlığı* ile *yürürlüğü* tek aramada görülüyor, yeni
parametre açılmadı. `all(mulga)` kullanıldı: bir anahtar birden çok satıra düşebiliyor,
yürürlükte **tek** satır varsa atıf mülga sayılmaz — geçerli atıfları yanlış reddetmemek için.
`red_kapisi.py`'ye **dokunulmadı**: `DOGRULANDI` dışındaki her hükmü zaten kötü sayıyor.

### Kabul ölçütü — geçti

```
1475/15 mulga=True · 1475/14 mulga=False (kıdem tazminatı yürürlükte)   ✅
"İş Kanunu Madde 15" → MULGA · katı/çoğunluk/cerrahi üçünde de REDDEDİLDİ ✅
yanlış-pozitif sıfır — 3 örneklem turu, gözle                            ✅
```

## 3. 🐞 İki kural doğrulama hedefine çarpıp düzeldi

İkisi de **hata vermeden yanlış veri üretecekti** — bu hattın imza failure class'ı.

**(a) Sonek kuralı %80 eksikti.** Yalnız küçük harf aranıyordu (`[a-zçğıöşü]`). Korpusta en
sık sonek **büyük `/A`** — 249 satır. 98 satırlık bir sınıf sanılan şey gerçekte **485**.
Kaçan 387 satır, düzeltme yapılmış gibi görünen bir korpus bırakacaktı.

**(b) İlga kaynağı, tarihin son parçasını kanun sanıyordu.** `"22/5/2003/4857/120 md."`
içinden `2003/4857` okunuyordu, çünkü tarih ile kanun arasındaki ayraç yalnız **tire**
sanılmıştı — oysa **bölü** de olabiliyor. `1475/15`'in ilga kaynağı `4857 md.120` yerine
**`2003 md.4857`** çıkmıştı.

⭐ **Sprint'in kendi verify kalemi ele verdi.** `1475/15`'i hedef olarak yazmak bir tören
değildi; iki kuralı da o hedef düşürdü. Ön-kayıtlı doğrulama hedefinin değeri tam olarak bu.

## 4. ⚠️ Dürüst negatif sonuç — B7 bir skor özelliği değil

Mevcut k=5 ve k=10 koşuları yeni korpusa karşı **yeniden puanlandı**:

```
              k=5              k=10
MULGA          0                0
hükmü DEĞİŞEN cevap  0/80       0/80
```

Yani açık **mekanik olarak** kapandı ama bu DEV kümesinde **ölçülen görülme sıklığı sıfır**.
B7 bir **ürün-güvenliği** özelliğidir, bir metrik iyileştirmesi değil — öyle raporlanıyor.
Bunun kaydedilmesi şart: aksi hâlde ileride *"S2 hiçbir şeye yaramadı"* diye okunur, oysa
ölçülen şey *"bu kümede tetiklenmedi"*dir. Mülga atıf riski soru dağılımına bağlıdır ve
`core_hard` yürürlükteki maddeler üzerinden üretilmiştir — sıfır çıkması **beklenebilirdi**.

## 5. Eval etiketleri düzeltilmedi — çünkü gerek kalmadı

Onarım öncesi altın anahtar `2004/Madde 31`'i **`31/a` satırı da** karşılayabiliyordu; artık
ikisi ayrı kayıt. Havuz iki eval kümesinde de korunuyor: `dev` **80/80**, `canon` **40/40**.
Yani soru kümesi değişmedi, **yer doğruluğu sıkılaştı** — bir kalem artık yanlış satırla
"bulundu" sayılamıyor. ADR-0054/K4'ün *"küme değişmez"* kuralı ihlal edilmedi.

## 6. İndeks — yeni dizine kuruldu

`madde_no`, gömülen metnin parçası (`kanun_adi + madde_no + text`), o yüzden 485 satırın
gömmesi değişti ve bayat-indeks kapısı **tasarlandığı gibi patladı**
(`37903062 → 38751499 bayt`). İndeks **`data/index/mevzuat_bge_m3_s2`**'ye kuruldu;
eskisi **silinmedi** — S2 öncesi sayıların yeniden üretilebilmesi için. Harness AÇIK k=10
yeni indeksle **yeniden koşuluyor**.

## 7. ⛔ ÖN-KAYITLI TAHMİN — S2 sonrası koşu *(sayı görülmeden yazıldı)*

Korpus değişti, indeks yeniden kuruldu, harness k=10 yeniden koşuluyor. **Ne beklediğim,
sonuç dosyası açılmadan:**

| eksen | tahmin | gerekçe |
| :--- | :--- | :--- |
| `recall@10` | **0,875 ± 0,025** (±2 soru) — pratikte **değişmez ya da 1-2 soru DÜŞER** | Gömülen metni değişen satır **485/40.496 = %1,2**. Ama altın eşleşmesi **sıkılaştı**: eskiden `2004/Madde 31` altınını **`31/a` satırı da** karşılayabiliyordu, artık yalnız gerçek `Madde 31`. Bu **3 soruda** yer doğruluğu katılaştı → düşerse **ölçüm daha doğru olduğu için** düşer, retriever kötüleştiği için değil. |
| kütle | **%59,5 ± 1 puan** | `recall` neredeyse sabitse coverage de sabit; A1'i etkileyecek bir şey değişmedi |
| `MULGA` | **0** | zaten ölçüldü (§4) — bu küme mülga maddeye atıf yapmıyor |
| bağlamdaki bozuk blok | **14/800 → 0/800** | sonek onarımı tam bu bloklara dokundu |

⚠️ **Düşüş senaryosunun okunma kuralı önceden yazılıyor** (sonradan gerekçe uydurmamak için):
`recall@10` düşer **ve** düşen sorular §7'de listelenen **id 0/41/74** arasındaysa → bu
**ölçüm düzelmesidir**, gerileme değil; eski sayı yanlış satırla "bulundu" sayıyordu.
Düşen sorular **başkalarıysa** → onarım erişimi bozmuştur, ayrıca incelenir.

## 8. 🚨 Kendi hatamın düzeltmesi — *"eval etiketleri düzeltilmedi, gerek kalmadı"* YANLIŞTI

§5'te *"altın anahtarların hiçbiri kaybolmadı, havuz 80/80 korundu, gerek yok"* yazmıştım.
Dayanak **doğru ama yetersizdi**: anahtar yaşıyor, ama **iki satırdan yanlış olanı**
gösteriyor. Onarım öncesi `2004/Madde 97` anahtarı hem gerçek `Madde 97`'yi hem `97/a`'yı
taşıyordu; eval kalemi `97/a`'dan üretilmiş olsa bile etiket `Madde 97` kalıyordu.

`referans` alanının `/` ile başlamasına bakarak **3** kalem bulmuştum (id 0/41/74). Doğru
kural — *"altın anahtarın sonekli bir kardeşi var mı"* — **5** buluyor: **0 · 41 · 45 · 74 · 76**.
İkisini kaçırmamın sebebi: `referans` alanı çift satırlı anahtarda **diğer** satırı çözüyordu.

### Kanıtlı vaka — id=76

```
soru      : "Borçlu ile başka birinin aynı taşınır malı elinde bulundurmaları
             durumunda kim mal sahibi sayılır?"
cevabı    : Madde 97/a — "Bir taşınır malı elinde bulunduran kimse onun maliki sayılır"
altın     : Madde 97   ← BAYAT ETİKET (istihkak iddiasına itiraz usulü, başka konu)
retriever : 97/a'yı 1. SIRAYA koydu · model doğru cevapladı
puanlama  : hem "erişim ıskası" hem "sadakatsiz" sayıldı
```

Yani S2 sonrası `recall@10`'un 0,8750 → **0,8625** düşüşünün **tamamı bu tek kalem** ve
sebebi retriever değil **etiket**.

### ⛔ ÖN-KAYITLI DENETİM İSTEMİ — koşulmadan önce yazıldı

⚠️ **Bu denetim sayı görüldükten sonra yapılıyor ve düzeltmesi bizim lehimize.** Tuzak
**6.9**'un *"cilaladılar"* riski tam burada. Karar **insana soruldu** (2026-08-05: *"beşini de
denetle ve düzelt"*), ve usul buna göre sıkılaştırıldı:

- şüpheli kalemler **elle seçilmez** — kuralla bulunur (`supheli_kalemler`)
- hakem **kördür**: madde numarası, kanun adı ve mevcut altın etiket yüke **girmez**
- **konum yanlılığına karşı** altın, tek id'de A'ya çift id'de B'ye konur
- hakem **"belirsiz"** diyebilir; belirsizde etiket **DEĞİŞMEZ**

```
[system]
Sen Türk hukukunda deneyimli bir hukukçusun. Sana bir SORU ve iki KANUN METNİ
verilecek. Görevin soruyu cevaplamak değil; soruyu HANGİ metnin karşıladığını söylemek.

ÖLÇÜT: Soruda sorulan bilgi hangi metinde AÇIKÇA düzenlenmiştir?

Kurallar:
- Yalnız verilen iki metne bak. Dışarıdan bilgi ekleme.
- İkisi de karşılıyorsa, soruyu DOĞRUDAN ve TAM karşılayanı seç.
- Hiçbiri karşılamıyorsa ya da ayırt edemiyorsan "belirsiz" de. Emin değilsen "belirsiz".

Yanıtı SADECE şu JSON ile ver:
{"secim": "A" | "B" | "belirsiz", "gerekce": "<tek cümle>"}

[user]
SORU:
{soru}

[KAYNAK A]
{metin_a}

[KAYNAK B]
{metin_b}
```

**Betik:** `scripts/altin_etiket_denetle.py` · **çıktı:** `outputs/eval/s2-etiket-denetimi/`

### Denetimin sonucu — ve bir kırmızı bayrak

```
DÜZELT     id 0 → Madde 31/a · id 74 → Madde 79/a · id 76 → Madde 97/a
DEĞİŞMEZ   id 41 (Madde 31) · id 45 (MADDE 73)
```

🚩 **İlk koşuda hakem BEŞİNDE DE "A" dedi.** Konum rastgeleleştirilmiş olmasına rağmen tek
yönlü seçim, klasik **konum yanlılığı** işaretidir; bu hükümlere dayanıp eval kümesini
değiştirmek olmazdı. Kontrol koşuldu (`--konum-ters`, koda **kalıcı** girdi): A/B ters
çevrildi, hakem bu kez **beşinde de "B"** dedi ve **hükümler birebir aynı** kaldı → hakem
konumu değil **içeriği** izliyor. Hep-A deseni, doğru olanın her seferinde A'ya düşmesindenmiş.

🐞 Denetim ayrıca **kendi kodumda bir hata** buldu: id 0 ile id 41 **aynı altın anahtarı**
paylaşıyor ama farklı maddelerden üretilmişler. `--uygula` anahtara göre eşliyordu, ikisini
birden bozacaktı. Eşleme **soru metnine** çevrildi + *"beklenen düzeltme ≠ eşleşen kalem"*
durumunda betik **eval'e dokunmadan ölüyor**. Hakem maliyeti koşu başına **$0,0009**.

## 9. ⭐ SONUÇ — S2 sonrası, düzeltilmiş etiketlerle

**Künye:** `tgta_v1` Q4_K_M · harness AÇIK · `k=10` · indeks `mevzuat_bge_m3_s2` ·
thinking on · 1024+512 · seed 3407 · ctx 8192 · kesik **%2,5** (kapı ✅) ·
hakem `openai/gpt-4o-mini` @ **openrouter**, sağlayıcı pin `OpenAI` · **$0,0398** ·
`outputs/eval/s2-harness-k10-etiketli/`

| eksen | S2 öncesi (k=10) | S2 sonrası, etiket düz. | Δ |
| :--- | ---: | ---: | ---: |
| `recall@10` | 0,8750 | **0,8750** | 0 |
| coverage | 0,7750 | **0,7625** | −1 soru |
| **A1** (cevaplanan) | 0,7681 | **0,8042** | **+3,6 p** |
| A1 · altın getirilen | 0,8426 | **0,8616** | +1,9 p |
| **kütle** | **%59,5** | **%61,3** | **+1,8 p** |
| bozuk blok (bağlam) | 14/800 | **0/800** | −14 |
| `MULGA` hükmü | — | **0** | — |
| B1 sınıfı (altın gelmedi, cevapladı) | 7 | **7** | 0 |
| aşırı-red (altın geldi, çekindi) | 15 | **16** | +1 |

### ✅ Ön-kayıtlı tahminin denetimi

| tahmin (§7) | gerçekleşen | hüküm |
| :--- | :--- | :--- |
| `recall@10` 0,875 ± 0,025 | **0,8750** | ✅ tuttu |
| kütle %59,5 ± 1 puan | **%61,3** | ❌ **TUTMADI — bandın 0,8 puan ÜSTÜ** |
| `MULGA` 0 | **0** | ✅ tuttu |
| bozuk blok 14 → 0 | **0/800** | ✅ tuttu |

⚠️ **Kütle tahmini neden tutmadı, ve gerekçesi neden yanlıştı.** *"A1'i etkileyecek bir şey
değişmedi"* demiştim. Yanlış: gömülen metin değişince **getirilen bağlam da değişti**, A1 de
bağlam üzerinden ölçülüyor. Onarım A1'i **atıf kanalından değil erişim kalitesi kanalından**
iyileştirdi — model artık aynı soruda **daha isabetli metni** okuyor. §4'ün *"skor özelliği
değil"* hükmü **atıf hükümleri için** ayakta (`MULGA` 0, hüküm değişimi 0/80); **erişim
için ayakta değil**. İki kanal, iki ayrı sonuç.

### 🚨 Etiket düzeltmesi manşet sayıyı YÜKSELTMEDİ

Kullanıcıya *"kütle biraz daha artar"* demiştim — **yanlıştı ve mekanizması yanlıştı**.
Altın etiket **A1'e de coverage'a da girmiyor** (A1 `context_shown`'a karşı ölçülüyor), bu
yüzden düzeltmenin **kütleye etkisi tanımı gereği sıfır**. Etkisi yalnız iki yerde:
**erişim metrikleri** (`recall@10` 0,8625 → **0,8750**) ve **teşhis çapraz tablosu**
(B1 sınıfı 8 → **7**).

### 🎁 Bedava ölçüm — hakemin yeniden-koşum gürültüsü

İki koşunun cevapları **bit-birebir aynı** (80/80 cevap, 80/80 bağlam özdeş — üretim
deterministik). Tek değişen altın etiketti. Dolayısıyla hakem yeniden koşulduğunda çıkan
fark **saf hakem gürültüsüdür** ve ilk kez sayısı var:

```
iddia sayısı   276 → 268
A1             0,8069 → 0,8042   (0,27 puan)
kütle          %61,53 → %61,32   (0,21 puan)
```

**Kullanım kuralı:** `n=80`, `temperature=0`, aynı girdi ⇒ **A1'de ~0,3 puanlık hareket
gürültüdür.** Bunun altındaki farklar yorumlanmaz. S2'nin +3,6 puanı bu tabanın **on katı**
— gerçek. (⚠️ Tek gözlem, güven aralığı değil; alt sınır tahmini olarak okunur.)

## Paper eşlemesi

**Methodology:** kapsam kararının *"veri ne kadar bozuk"* değil *"bozukluk modele ulaşıyor
mu"* diye ölçülmesi; aynı korpus için %29,4 (anahtar yinelenmesi) ve %1,8 (bağlam kirlenmesi)
sayılarının ikisinin de doğru ama farklı nesneleri ölçmesi. **Limitations / Data:** yürürlük
bilgisi korpusta yoktu; atıf doğrulayıcı *var mı* sorusunu yanıtlıyor, *geçerli mi* sorusunu
yanıtlamıyordu. **Negatif bulgu:** ürün-güvenliği düzeltmesinin mevcut değerlendirme
kümesinde **atıf kanalından** ölçülen etkisi **sıfır** — güvenlik özellikleri skor üzerinden
savunulamaz. (Erişim kanalından etkisi sıfır **değil**: A1 +3,6 puan — §9.)
**Reproducibility:** aynı girdide hakem yeniden-koşum gürültüsü **A1'de ~0,3 puan** olarak
ölçüldü (§9) — LLM-hakemli her tablonun altına yazılması gereken taban.
**Threats to validity:** eval altın etiketleri **sayı görüldükten sonra** düzeltildi; usul
sıkı tutuldu (kural-tabanlı seçim · kör hakem · ön-kayıtlı istem · konum-yanlılığı kontrolü ·
insan onayı) ama şerh kalıcıdır — ve düzeltme manşet sayıyı **yükseltmedi**.
