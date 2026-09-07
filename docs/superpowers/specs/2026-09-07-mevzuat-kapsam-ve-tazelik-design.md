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

| kat | eklenen | yeni belge |
| :--- | :--- | ---: |
| 1 | `KHK` + `CB_KARARNAME` | 119 |
| 2 | `TUZUK` | 110 |
| 3 | `YONETMELIK` | 172 |

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
| **`CB_KARAR` + `KKY` (8.404 belge)** | bu turda **kapsam dışı**: vatandaş sorularına uzak, ve indeksi **~7×** büyütür ⇒ S8 (dağıtım) kararını yeniden açar |

---

## 8 · Açık kalan — bu spec'in KAPATMADIĞI

- 🔓 **`kayitTarihi` gerçekten değişim sinyali mi** — §6'nın testi bunu ölçecek; **çıkmazsa
  tasarım değişir** (o zaman içerik `sha256` karşılaştırması gerekir, yani her belgeyi indirmek)
- 🔓 **`TEBLIG` sayısı** — sorgu hata verdi, ölçülemedi
- 🔓 **Yönetmelik düzeyinde eval sorusu yok** — kapı *"yeniyi buluyor"* diyemiyor (§5)
- 🔓 **Tazeleme sıklığı** — haftalık mı, aylık mı? Bugün veri yok: `kayitTarihi` dağılımı
  değişim **hızını** değil **yeniden alım** hızını gösteriyor olabilir
- ⚠️ **Kapsam büyürse S8 yeniden okunur:** indeks 79 MB → ~120 MB tahmini; HF dataset kararı
  bu boyutta **ayakta**, ama `CB_KARAR`/`KKY` eklenirse **değil**
