# Mevzuat kapsamı ve tazelik — tasarım (spec)

**Tarih:** 2026-09-07 · **Statü:** insan onaylı (üç bölüm ayrı ayrı) · **Sonraki adım:** uygulama planı

**Soru neydi:** *"Kanun canlı ve çok geniş. Tümünü nasıl tutacağız, retriever nasıl olacak?"*

**Cevabın özü:** Canlılık **ürünün dışına** alınır. Korpus **sürümlenmiş bir anlık görüntüdür** ve
**tarihi künyede yazılıdır**; tazeleme ayrı bir iştir. Ürün her zaman *tarihi belli* bir korpusla
çalışır — canlı hukukla değil. Bu takas bilerek **tekrarlanabilirlik lehine** yapılmıştır.

---

## 1 · Bugünün ölçülmüş durumu — hiçbiri tahmin değil

| olgu | değer | nasıl ölçüldü |
| :--- | :--- | :--- |
| korpus | **892 kanun · 40.496 madde · 37 MB** | `data/corpus/mevzuat_maddeler.jsonl` sayımı |
| indeks | **79,1 MB** (fp16 · 1024 boyut) ≈ **2 KB/madde** | `gomme.npy` başlığı |
| gömme hızı | GPU **~65 madde/sn** · CPU **~4,1/sn** | `s3a-on-prob/recall_BAAI_bge-m3.json` · `recall_olc.py`:74 |
| 🚨 korpusun güncellik tarihi | **YOK** — tek bir tarih alanı bile yok | alan listesi: `kanun_no · kanun_adi · madde_no · text · mulga` |
| 🚨 `mulga` bayrağı | **VAR** (2.547 madde) ama `retriever.py` **kullanmıyor** | `grep mulga scripts/erisim_korpus/retriever.py` → 0 |
| 🚨 gerçek sızıntı | **800 getirilen kaynağın 2'si mülga** (%0,2) · 2/80 kalem (id 7 · 63) | `f02` koşusu × korpus çaprazı |

### Bedesten API — sözleşme ölçüldü (2026-09-07, canlı sorgu)

| tür | adet | | tür | adet |
| :--- | ---: | :-- | :--- | ---: |
| `KANUN` | **917** *(bizde 892 = %97)* | | `CB_KARAR` | 4.361 |
| `YONETMELIK` | **172** | | `KKY` | 4.043 |
| `TUZUK` | 110 | | `CB_GENELGE` | 29 |
| `KHK` | 63 | | `TEBLIG` | *(sorgu hata verdi)* |
| `CB_KARARNAME` | 56 | | | |

**Kısıtlar — ölçüldü:**
- `pageSize` **max 20** (50 ve 100 **boş** döner) ⇒ 1.318 belge ≈ **66 istek**
- 🚨 **`guncellemeTarihi` alanı VAR ama 60/60 örnekte `None`** — şemada bir alan görüp dolu
  varsaymak bu reponun avladığı hata sınıfı; **ölçülerek** düzeltildi
- ✅ **`kayitTarihi` 100/100 dolu ve hepsi benzersiz**, 2026-05-22 ↔ 09-03 arasına yayılmış
- ⚠️ **TR IP şart** — gov firewall yurtdışı/VPN'i bloke ediyor

---

## 2 · Kilitlenen üç insan kararı

| # | karar | gerekçe |
| :-- | :--- | :--- |
| **K1** | Kapsam **`YONETMELIK` dahil** genişler | vatandaşın *"nasıl başvururum, hangi belge"* soruları yönetmelikte. ⭐ Ve büyüme sanıldığı gibi 10× değil **~1,5×**: çekirdek katmanlar toplam **1.318 belge** |
| **K2** | Tazelik: **anlık görüntü + fark taraması** | vatandaşın makinesi API'ye **zorunlu** dokunmaz ⇒ TR IP şartı **bulaşmaz**, gecikme yok, **ölçüm yeniden üretilebilir** kalır |
| **K3** | Kapsam **kat kat** girer, her kat **bir kapıdan** geçer | daha çok belge = 10 slot için daha çok rakip; ADR-0068 aynı meseleyi ölçmüştü |

### K2'nin iki katmanı — insan düzeltmesi 2026-09-07

- **Bizim tarafta:** anlık görüntüyü periyodik tazeleyip **yayımlarız** (S8'in HF dataset'i).
  TR IP'si olmayan kullanıcı **bizim tazelediğimizi** indirir.
- **Kullanıcı cihazında:** `tazele(SOR)` varsayılan olarak açıktır ve **TR IP ister**;
  ⛔ **cihaz içi fallback YOKTUR** — IP yoksa tazeleme olmaz, kullanıcı elindeki anlık görüntüyle
  kalır **ve tarihini görür**.
- ⇒ Sistemin tamamında kullanıcı **asla tarihsiz kalmaz**.

⭐ **Mahremiyet neden bozulmuyor:** tazelik çağrısı **soruyu taşımaz**. `searchDocuments` yalnız
*"şu türde hangi belgeler var, `kayitTarihi` ne"* diye sorar; kullanıcının ne merak ettiğine dair
**tek bit** bilgi gitmez. Sızan tek şey *"bu IP korpusunu tazeliyor"*.

---

## 3 · Mimari — üç sorumluluk, üç zaman ölçeği

```
  bedesten API  (canlı, TR IP)
        │
        │  ① TAZELİK — periyodik; bizde VE (TR IP varsa) kullanıcıda
        │     66 istek → kayitTarihi farkı → yalnız değişeni indir
        ▼
  data/corpus/   ← SÜRÜMLENMİŞ ANLIK GÖRÜNTÜ · tarihi künyede
        │
        │  ② İNDEKSLEME — yalnız değişen maddeler yeniden gömülür
        ▼
  data/index/    ← korpus künyesine BAĞLI
        │
        │  ③ ERİŞİM — kullanıcının makinesinde, ağa dokunmaz
        ▼
     answer()
```

Üçü **farklı zaman ölçeğinde**: ① haftalar · ② tazelikten sonra · ③ her soruda.

---

## 4 · Bileşenler — dört birim, dar arayüz

| birim | tek sorumluluğu | bağımlılığı |
| :--- | :--- | :--- |
| `hakhukuk/mevzuat/kaynak.py` | **bedesten sözleşmesi**: `listele(tur) → [Kayit]` · `metin(mevzuatId) → str`. Sayfalama (max 20), sarmalama, TR IP tespiti, retry **burada gizli** | `requests` |
| `hakhukuk/mevzuat/tazelik.py` | **fark taraması**: yerel künye ↔ uzak `kayitTarihi` → `Fark(yeni, degisen, kaybolan)`. **Ağa dokunmaz** | `kaynak` · `tipler` |
| `hakhukuk/mevzuat/anlik.py` | **anlık görüntü**: sürümleme · künye · `sha256` · **geri alma** | `tazelik` |
| `hakhukuk/mevzuat/indeksle.py` | **artımlı gömme**: yalnız değişen maddeler; indeks künyesini korpus künyesine bağlar | `anlik` · `retriever` |

**Neden ayrı `kaynak.py`** *(POSD silme testi)*: silinirse bedesten'in tuhaflıkları — `pageSize`
max 20, `guncellemeTarihi` boş, TR IP şartı, `{"data": …, "applicationName": …}` sarmalaması —
**dört çağırana birden** yayılır.

### Ana arayüz

```
tazele(mod: Tazelik = Tazelik.SOR) -> Rapor
```

`Tazelik` enum: **`SOR`** (varsayılan — *"14 belge değişmiş, güncelleyeyim mi"*) · `OTOMATIK` · `KAPALI`.
⛔ **Bool bayrak yok** (CLAUDE.md §4): *"sor"* hâli bir `bool` ile ifade edilemez.

### İki sert kural

⛔ **TR IP yoksa cihaz içi fallback YOK.** `kaynak.py` `TrIpGerekli` atar; `tazele()` **yutmaz**,
`Rapor.durum = IP_YOK` döner ve kullanıcıya *"tazeleme yapılamadı; korpusun tarihi …"* denir.
Sessiz düşürme bu repoda hata sınıfının kendisidir.

⛔ **Kısmi tazeleme diske YAZILMAZ — hepsi ya da hiçbiri.** 14 belgeden 9'u inip ağ koparsa korpus
**bayt-bayt eski hâlinde** kalır. Aksi hâlde künyedeki tarih ile içerik ayrışır ve o ayrışma
**hata vermez**, yalnız sessizce yanlış olur.

---

## 5 · Kapsam kapısı — ön-kayıtlı, ŞİMDİ yazılıyor

Kapsam **kat kat** girer; her kattan sonra **aynı 80 soruyla** `recall@10` yeniden ölçülür
(**hakem gerekmez, $0**):

| kat | eklenen | yeni belge | ≈ madde |
| :--- | :--- | ---: | ---: |
| 1 | `KHK` + `CB_KARARNAME` | 119 | ~33.000 |
| 2 | `TUZUK` | 110 | ~4.000 |
| 3 | `YONETMELIK` | 172 | ~8.000 |
| **4** 🆕 | **`CB_KARAR`** | **4.361** | **~76.317** |
| **5** 🆕 | **`KKY`** | **4.043** | **~126.343** |

⚠️ **Kat 4-5, §7b'deki insan kararıyla 2026-09-07'de EKLENDİ.** Bu tablo başta üç kat
yazıyordu ve §7 hâlâ `CB_KARAR`+`KKY`'yi eleme satırında gösteriyordu — **o satır artık
geçersiz** ve çelişki §7'de de damgalandı.

```
recall@10 ≥ 0,9500  →  kat GİRER
recall@10 <  0,9500  →  ⛔ kat GİRMEZ, sebebi bulunana kadar
```

⛔ **Eşik koşudan ÖNCE yazıldı** (ADR-0050: *"sonucu gördükten sonra eşik değil alet düzeltilir"*).

### 🚨 Bu kapının sınırı — baştan yazılıyor

Kapı yalnız ***"eskiyi bozmadı"*** der; ***"yeniyi buluyor"* DEMEZ.** Yönetmelik düzeyinde
cevaplanan sorumuz **yok** — 80 sorunun hepsi kanun düzeyinde. ⇒ Kat 3 geçse bile *"yönetmelik
eklemek işe yaradı"* **kurulamaz**; yalnız *"zarar vermedi"* kurulur.
Yeni soru yazmak **ayrı bir tur** ve **insan onayı** ister (ADR-0067 usulü) · donmuş TEST'i de ilgilendirir.

---

## 6 · Test ve hata felsefesi

- `tazelik.py` **ağa dokunmadan** sınanır — sahte `kaynak`: yeni · değişen · kaybolan senaryoları
- ⭐ **`kayitTarihi` varsayımı bir TESTLE çivilenir.** Bugün onun bir *değişim sinyali* olduğu
  **kanıtlanmadı** (100/100 benzersiz **ama** kümeleniyor — 07-31'de 28 belge; toplu yeniden alım
  da olabilir). Test: iki anlık görüntü arasında `kayitTarihi` değişen belgenin **metni de gerçekten
  değişmiş mi?** Değişmemişse sinyal **gürültülü** demektir — ve bu **ölçülerek** öğrenilir.
- Kısmi yazma **testle yasaklanır**: ağ ortada koparsa korpus bayt-bayt eski kalmalı
- Mülga süzgeci (Görev 8b) korunur: getirilen hiçbir kaynak `mulga=True` olmamalı

**Hata felsefesi** (CLAUDE.md §5): TR IP yok → **edge'de reddet** · geçici ağ hatası →
**geri çekilmeli retry** · yarım indirme → **rollback**.

---

## 7 · Reddedilenler

| eleme | gerekçe |
| :--- | :--- |
| **Canlı API sorgusu (her soruda)** | her kullanıcı **TR IP** ister · API düşerse **ürün düşer** · kullanıcının **sorusu dışarı sızar** (mahremiyet vaadi biter) · ölçüm **yeniden üretilemez** olur |
| **Melez: yerel indeks + atıf doğrulaması** | soru sızmaz ama **hangi maddeye baktığı** sızar; ve `terazi.py`'nin **determinizmini** bozar — ağ düşerse cevap değişir |
| **Kapsamı büyütmemek** | vatandaşın *"nasıl başvururum"* soruları yönetmelikte; ve büyüme ölçüldü, **~1,5×** |
| **Tüm türleri tek seferde eklemek** | düşerse **hangi katın düşürdüğü bilinmez** — T5'in dersi: grup grup taşındığı için kırılma **hemen** görüldü |
| ~~`CB_KARAR` + `KKY` (8.404 belge)~~ | ⚠️ **BU ELEME GERİ ALINDI — insan kararı 2026-09-07, §7b:** *"tüm kanunlar, her şey ne varsa gelmeli"*. Gerekçenin **ikinci yarısı doğru çıktı ve duruyor**: indeksi 8,4× büyüttü ve S8'i **gerçekten** yeniden açtı. Bu kabul edilmiş bir maliyet, çürütülmüş bir gerekçe değil. |

---

## 7b · Kapsam "her şey" olunca — ölçüldü 2026-09-07 (insan kararı: `CB_KARAR` + `KKY` DAHİL)

Belge başına madde sayısı **canlı API'den örneklendi** (`mevzuatMaddeTree`, tür başına 6 belge):

| tür | belge | ort. madde | ≈ toplam |
| :--- | ---: | ---: | ---: |
| `KANUN` | 917 | 102,7 | 94.145 |
| `CB_KARARNAME` | 56 | **564,0** | 31.584 |
| **`CB_KARAR`** | 4.361 | 17,5 | **76.317** |
| **`KKY`** | 4.043 | 31,2 | **126.343** |
| `TUZUK` · `YONETMELIK` · `KHK` | 345 | — | 11.914 |
| **TOPLAM** | **9.722** | | **≈ 340.303** |

🚨 Bugün **40.496** ⇒ **8,4×**. `CB_KARAR` + `KKY` tek başına **202.660 madde** (toplamın %60'ı).

### Kaba kuvvet bu ölçekte AYAKTA — ölçüldü

| | bugün | 340k'da |
| :--- | ---: | ---: |
| disk (fp16) | 83 MB | **697 MB** |
| RAM (fp32) | 166 MB | **1.394 MB** |
| sorgu | **6,08 ms** *(ölçüldü; `CLAUDE.md` çıpası 8,2 ms)* | **~51 ms** |

⇒ **Vektör veritabanı hâlâ gereksiz.** 51 ms bir hukuk asistanında fark edilmez (model zaten
saniyeler harcıyor). `CLAUDE.md`'nin *"vektör db ölçüldü ve reddedildi"* kararı bu ölçekte de ayakta.

### 🚨 `fp16` denendi ve REDDEDİLDİ — iki sebeple

RAM'i yarıya indirmek için `retriever.py`:101'in `astype(np.float32)` satırını kaldırmak önerildi.
Ölçüldü (80 sentetik sorgu × 5 yineleme):

| | fp32 | fp16 |
| :--- | ---: | ---: |
| RAM | 166 MB | 83 MB ✅ |
| sorgu | **6,08 ms** | **270,06 ms** 🚨 **44,4×** |
| 340k'da | ~51 ms | **~2.269 ms** |
| ilk-10 **birebir aynı** | — | 🚨 **70/80** |

1. **Hız:** numpy `fp16` matris çarpımı BLAS yolunu kullanamıyor ⇒ 340k'da sorgu **2,3 saniye**.
2. **Daha ciddi — sonuçlar DEĞİŞİYOR:** 10/80 sorguda ilk-10 sırası farklı (ortak kalem 9,8/10).
   Bu bir *takas* değil, **ölçüm birimini değiştiren müdahale**: `recall@10` etkilenir ve
   yayımlanmış **0,9500** yeniden koşulmayı gerektirir.

⚠️ Ölçüm **sentetik** sorgu vektörleriyle yapıldı (gerçek `bge-m3` çıktısıyla değil) ⇒ fark gerçek
sorularda **daha küçük** olabilir. Ama hız tek başına yeterli sebep.
**Karar: `fp32` kalır.**

🆕 **Açık borç — RAM için başka kaldıraçlar:** `np.load(..., mmap_mode="r")` ile diskten eşleme ·
boyut indirgeme (1024 → 512, PCA/Matryoshka) · ürün ile ölçüm için **ayrı** indeks profilleri.
⛔ Üçü de bu spec'in dışında ve **hiçbiri ölçülmedi**.

### 🚨 DÜZELTME 2026-09-07 (plan yazımı) — *"~51 ms"* YALNIZ YOĞUN KOLU SAYIYORDU

Yukarıdaki *"sorgu 6,08 ms → 340k'da ~51 ms"* satırı `q @ gomme.T`'yi ölçtü. Ama retriever
**hibrit**: BM25 kolu da her sorguda koşuyor ve **baskın maliyet o**. Ölçüldü (aynı makine,
`rank_bm25.BM25Okapi`, 10 yineleme; 340k korpus = gerçek korpus ×9 kırpılarak sentezlendi):

| kol | 40.496 | 340.303 |
| :--- | ---: | ---: |
| **BM25** | **87,7 ms** | **713,8 ms** ← baskın |
| yoğun (`q @ G.T`) | 5,3 ms | 34,9 ms |
| RRF + argsort | 8,6 ms | 54,0 ms |
| **TOPLAM (gömücü hariç)** | **~102 ms** | **~803 ms** |

⇒ Yayımlanan sayı **16× iyimserdi**. İki sonuç:

1. **Karar DEĞİŞMİYOR, gerekçesi değişiyor.** 0,8 sn bir hukuk asistanında hâlâ fark edilmez
   (model saniyeler harcıyor) ⇒ vektör veritabanı hâlâ gereksiz. Ama *"51 ms"* diye
   savunulamaz; **~0,8 sn** diye savunulur.
2. **Optimizasyon yönü TERS ÇEVRİLDİ.** `fp16` tartışması yoğun kolu (%4) kurcalıyordu;
   asıl yük BM25'te (%89). RAM'de de öyle: BM25 kurulumu 40.496'da **+88 MB** ⇒ 340k'da
   **~741 MB**, yoğun indeksin 1.394 MB'ının üstüne. **Toplam ~2,1 GB.**
3. **Yükleme süresi bir borç:** `Retriever.yukle` BM25'i her açılışta yeniden kuruyor
   (docstring *"~10 sn"* diyor; ölçüldü **4,3 sn**) ⇒ 340k'da **~37 sn**. Kalıcılaştırmak
   gerekebilir — ölçülmedi, plan Görev 6'da kapıya bağlandı.

### 🚨 DÜZELTME 2026-09-07 — KORPUSTA KARARLI KİMLİK YOK (artımlı gömmenin ön koşulu)

§3 *"yalnız değişen maddeler yeniden gömülür"* diyor. Bunun için maddenin **kararlı bir
kimliği** olmalı. Ölçüldü — yok:

| aday anahtar | benzersiz | çakışan |
| :--- | ---: | ---: |
| `(kanun_no, madde_no)` | 32.281 | 🚨 **3.699** |
| `(kanun_no, madde_no, text)` | 39.379 | 🚨 **538** *(birebir yinelenen satırlar)* |

Bugün kimlik **satır sırasıdır** — `gomme.npy`'nin *i*. satırı korpusun *i*. satırıdır, başka
hiçbir bağ yok. Artımlı güncelleme bu zeminde **yanlış satırı tazeler ve hata vermez**: tam
olarak bu reponun avladığı sınıf. ⇒ Plan, artımlı gömmeden **önce** korpusa bedesten'in kendi
kimliğini (`mevzuat_id` + `madde_id`) ekliyor (Görev 3).

### S8 (dağıtım) YENİDEN AÇILIYOR

*"HF dataset'ten 79 MB indir"* kararı **697 MB**'a taşındı. Karar hâlâ (a) olabilir ama
*"dakikalar içinde kurulur"* cümlesi **düşer**; gömme süresi GPU'da ~1,5 saat, CPU'da ~23 saat
⇒ **(b) kurulumda üret seçeneği fiilen ölür.**

---

## 8 · Açık kalan — bu spec'in KAPATMADIĞI

- 🔓 **`kayitTarihi` gerçekten değişim sinyali mi** — §6'nın testi bunu ölçecek; **çıkmazsa
  tasarım değişir** (o zaman içerik `sha256` karşılaştırması gerekir, yani her belgeyi indirmek)
- 🔓 **`TEBLIG` sayısı** — sorgu hata verdi, ölçülemedi
- 🔓 **Yönetmelik düzeyinde eval sorusu yok** — kapı *"yeniyi buluyor"* diyemiyor (§5)
- 🔓 **Tazeleme sıklığı** — haftalık mı, aylık mı? Bugün veri yok: `kayitTarihi` dağılımı
  değişim **hızını** değil **yeniden alım** hızını gösteriyor olabilir
- 🔓 **Kat 3'ün FAYDASI ölçülemiyor** — insan kararı 2026-09-07: önce **$0'lık vekil**
  (*"yeni tür ilk-10'a giriyor mu, alakalı mı"*), **sonra** ADR-0067 usulüyle yeni soru turu
- 🔓 **RAM kaldıraçları ölçülmedi** — `mmap` · boyut indirgeme · ayrı indeks profilleri
- ⚠️ **Kapsam büyürse S8 yeniden okunur:** indeks 79 MB → ~120 MB tahmini; HF dataset kararı
  bu boyutta **ayakta**, ama `CB_KARAR`/`KKY` eklenirse **değil**
