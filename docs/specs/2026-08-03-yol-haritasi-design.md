# Yol haritası tasarımı — modelden platforma

- **Tarih:** 2026-08-03
- **Statü:** onaylandı (insan)
- **Kapsam:** `HakHukuk-4B-v0.1`'den vatandaş platformuna giden sprint zinciri
- **Yürürlükteki özet:** [`../../ROADMAP.md`](../../ROADMAP.md) · aktif icra: [`../../sprint3.md`](../../sprint3.md)

---

> ## 📐 BU BELGE BİR YOL HARİTASI, UYGULAMA SPEC'İ DEĞİL
>
> Kapsamı S3a'dan S6+'ya uzanıyor (A → B → C) — **tek bir uygulama planına sığmaz** ve
> sığdırılmaya çalışılmamalı. Her halka kendi spec → plan → uygulama döngüsünü hak ediyor.
>
> **İlk uygulanabilir birim: S3a + S3** (ön-prob + harness) — tarifi
> [`../../sprint3.md`](../../sprint3.md)'de. Uygulama planı **oraya** yazılır.
>
> S4 ve sonrası burada **niyet ve çıkış ölçütü** düzeyinde duruyor; sırası gelince kendi
> spec'ini alacak. Bu bilinçli: aralıklı ritimde uzak halkaların ayrıntısını şimdi yazmak,
> yanlış varsayımları belgeye çivilemek olur.

## Bağlam

Proje 2026-08-03'te **yüksek lisans tezi** olmaktan çıkıp **açık kaynak ürüne** döndü. Elde
çalışan bir model var (`HakHukuk-4B-v0.1`), ama **ürün yok**: kullanıcının mevzuat metnini
kendisi yapıştırması gerekiyor.

Bu belge, oradan vatandaşın kullandığı bir platforma giden yolu tanımlar.

### Kabul edilen kısıtlar

```
ritim    aralıklı — bir sprint ≈ 1-2 ay, takvim taahhüdü YOK
kişi     tek
bütçe    Modal kalan $22,31 (usage limit) · barındırma henüz üstlenilmedi
hedef    vatandaş (uzman değil) · yerel-öncelikli · mahremiyet bir özellik
```

⚠️ **Takvim yazılmaz, çıkış ölçütü yazılır.** Aralıklı çalışmada süre tahmini hem yanlış çıkar
hem yapay baskı yaratır. Bağlayıcı olan **sıra** ve her halkanın **çıkış ölçütü**dür.

---

## Vizyon — üç drop

```
🟦 A   model + harness → HF        kendi sistemine kuracak kişi
🟩 B   kurulabilir web uygulaması  kullanmak isteyen kişi
🟪 C   vatandaş platformu          vatandaş
```

Her biri bir sonrakinin basamağı: A olmadan B'nin dağıtacağı bir şey, B olmadan C'nin üstüne
kuracağı bir şey yok.

---

## Zincir

```
S3a  ÖN-PROB      recall@k + bedesten sözleşmesi        $0 · ~1 gün
       ↓          planın temeli sınanır, S3 buna göre boyutlanır
S3   HARNESS      retriever · atıf doğrulayıcı · red kapısı
       ↓          drop YOK — ölçüm repoya düşer
S4   MODEL        τ_a v2 · Türkçe muhakeme · donmuş TEST kabul
       ↓
     🟦 DROP A    HakHukuk-4B-v1.0 + harness BİRLİKTE
       ↓
S5   SERVİS       FastAPI + TS · Docker · SQLite
       ↓
     🟩 DROP B    kurulabilir web uygulaması
       ↓
S6+  PLATFORM     C1 belge → C2 niş → C3 e-Devlet → C4 canlı → C5 HITL
       ↓
     🟪 DROP C
     ↻ BAKIM      yeni base çıktıkça reçete yeniden koşulur (~$7)
```

### Neden A'da model ve harness BİRLİKTE

Ağırlık değişmeden yapılan "kod drop"u zayıf bir yayındır ve dikkati böler. Harness'sız ağırlık
yayımlamak da yarım iş — kullanıcı yine mevzuatı kendi yapıştırır. **A tek parça:** *"4B model +
harness, şu sayılarla, çalışır hâlde."*

Harness'ın katkısı yine izole ölçülür: S3'te **harness-açık ↔ harness-kapalı** tablosu üretilip
repoya konur ve A'nın model kartına girer.

---

## S3a — ÖN-PROB

İki varsayımı sınar. İkisi de model çağrısı, hakem ve GPU **gerektirmez**.

### Prob 1 — `recall@k`

DEV soruları maddelerden üretildi; her sorunun altın `kanun_adi + madde_no`'su **biliniyor**.
Ölçüm saf bilgi-erişim işi.

Sırayla, ucuzdan pahalıya: **BM25** → `multilingual-e5` → `bge-m3` → hibrit.

> **BM25 neden ilk:** hukuk metni ayırt edici terimlerle dolu (kanun adları, madde numaraları).
> Sözlüksel arama burada beklenenden güçlü olabilir ve **taban çizgisi** kurar. Yoğun gömme
> BM25'i geçemiyorsa gömme modeli seçmenin anlamı yok.

**Ön-kayıtlı karar eşikleri:**

| `recall@10` | S3 ne olur |
| :--- | :--- |
| **≥ %90** | plan tarif edildiği gibi koşar |
| **%70-90** | hibrit eklenir, S3 büyür |
| **< %70** | 🛑 **DUR** — sorun korpus yapısında, S3'e girilmez |

`recall@1/5/10/20` eğrisi de çıkarılır: modele kaç parça verileceğini o belirler.

### Prob 2 — bedesten sözleşmesi

`scripts/bedesten_probe.py` ile arama + tam metin + madde ağacı sınanır.
⚠️ **Türk IP gerekiyor.**

Değişmişse: retriever statik korpusla sürer, ama **güncellik iddiası düşer** →
`ROADMAP.md` + `MODEL_CARD.md` düzeltilir.

---

## S3 — HARNESS

### Adım 0 — modül-başına normalleştirme *(harness'tan bağımsız, önce yapılır)*

Merge'in **bilinen** kusuru: `τ_a` seyreliyor (tekil M2b 0,987 → merge 0,877). Normalleştirme
şu an **global** (tek `‖τ‖_F`). Ölçüldü: iki kolun da en büyük normu **aynı MLP yüzeyinde** —
`gate_proj` (τ_g 6,150 ↔ τ_a 0,621) · `up_proj` (5,047 ↔ 0,628). Global norm bunu göremiyor.

```
~20 satır (merge_ties.py) · 1 saat · GPU $0
kabul: M2b > 0,877 VE M1 kütlesi ≥ %71,6  (ikisi birden — tek eksen yeter değil)
tutmazsa v0.1 yerinde kalır, kayıp 1 saat
```

Kazanan yapılandırma S4'ün yeniden merge'inde kullanılır.

### Bileşenler

**1. Retriever** — çevrimdışı indeks (CPU) → soru → top-k madde. İki arka uç, tek arayüz:
statik anlık görüntü (**ölçüm**, tekrarlanabilir) · canlı bedesten API (**sunum**, güncel).

> ⚠️ **En sessiz kırılma noktası:** model bugüne kadar hep `KAYNAKLAR:\n[KAYNAK n]\n<kanun>
> Madde <no>\n<900 karaktere kırpılmış metin>\n\nSORU:` biçimini gördü. **Retriever tam bu
> biçimi üretmek zorunda** — farklı biçim = model dağılım dışında = tüm ölçümler kıyaslanamaz.
> Eval-ayna ilkesinin harness'a uygulanması.

**Chunk birimi = madde** (K2 kararı). Gerekçe uzunluk değil: **madde atıf birimidir**. Erişim
birimi ile atıf birimi ayrışırsa doğrulama karışır. Uzun maddeler (%20,6'sı >900 karakter)
gömme için örtüşen pencerelere bölünür, **madde kimliğiyle tekilleştirilir**.

⚠️ 900 karakter kırpmanın gizli bedeli ölçülecek: kaç DEV sorusunun cevabı 900. karakterden
sonra kalıyor? Kırpma **ölçüm karşılaştırılabilirliği** için var, ürün kalitesi için değil.

**2. Atıf doğrulayıcı** — deterministik, hakem yok.

```
cevaptan atıfları ayıkla   → "X Kanunu Madde N"
korpusta var mı?           → yoksa UYDURMA
getirilen kümede miydi?    → değilse model ezberden konuşmuş
```

⚠️ Türkçe ayıklama tuzaklı ve **bizi zaten ısırdı**: korpusta hem `Madde 75` hem `MADDE 64` var;
ADR-0051'de büyük/küçük harfe duyarlı regex 45 kalemin 15'ini sessizce düşürmüştü.
**Ayıklayıcı kendi test setiyle gelir.**

**3. Red kapısı** — ADR-0038 katı: tek doğrulanamayan atıf tüm cevabı reddettirir.
**Bedeli ölçülür:** kaç doğru cevabı da kesiyor?

### Çıkış ölçütü

```
✅ Adım 0 sonuçlandı (modül-başına norm kabul edildi ya da reddedildi)
✅ recall@k ölçüldü ve raporlandı
✅ doğrulayıcı kendi test setiyle geçiyor
✅ kapı çalışıyor ve BEDELİ ölçülü (aşırı-red + kütle)
✅ harness AÇIK ölçüm yapıldı, harness KAPALI ile YAN YANA yayımlandı
✅ tek slot 8192 ctx gerçek VRAM tepe değeri ölçüldü → README "asgari donanım"
```

---

## S4 — MODEL → 🟦 DROP A

### İşler

1. **`τ_a` v2** — şablon ezberini kır ([ADR-0051](../adr/0051-m2b-cift-kalibi-ve-chosen-uretimi.md) B planı: `chosen`'ı hakemle üret) · ~$2
   *kanıt: M1 medyan cevabı 58 karakter = şablonun kendisi; model cümleyi çekimliyor*
2. **Türkçe muhakeme** — iz şu an İngilizce (8/8). Vatandaşa *"okunabilir muhakeme"* vaat eden
   ürün için **ürün açığı**. Üç yol: (a) eğitim verisine Türkçe iz · (b) mevcut izleri çevir ·
   (c) istem katmanında zorla. ⭐ **Önce (c) bedavaya denenir** — tutarsa eğitime hiç girilmez.
3. **Yeniden merge** — yeni `τ_a` eski merge'i geçersiz kılar. **S3 Adım 0'da kazanan
   yapılandırmayla** yeniden merge edilir ve doğrulanır. GPU $0, ~2 saat.
   *Unutulursa S4 yarım kalır.*

### ⛔ v1.0 kabul ölçütü — TEST harcanmadan ÖNCE yazıldı

```
v1.0 ancak HEPSİ sağlanırsa:
  1. hiçbir eksende v0.1'e göre GERİLEME yok
        M1 kütle ≥ 71,6%  ·  M2 ≥ 0,893  ·  M2b ≥ 0,877
  2. bilinen zayıflık İYİLEŞMİŞ:  M2b > 0,877
  3. geçerlilik kapısı geçildi:   kesik ≤ %5
  4. harness açık/kapalı tablo yayımlandı

Karşılanmazsa → v0.x kalır, DROP A OLMAZ.
```

### Donmuş TEST — karar (a)

`data/eval/canon/` (40+35) v1.0'da **bir kez** harcanır. **v2.0 için yeni bir donmuş set
üretilir** — CANON protokolü belgeli, korpus elimizde, ~$1 + yarım gün.
⚠️ Üretimi **S4'ten önce** yapılır; sonra yapılırsa v2.0'a yetişmez.

*Elenenler:* TEST'i hiç harcamamak (model kartındaki sayı seçim yanlılığı taşır) ·
görülmüş seti şerhle tekrar kullanmak (dürüst ama zayıflayan ölçüm).

### DROP A içeriği

```
HF     ağırlıklar (GGUF Q4_K_M + bf16) · model kartı · harness kurulum
repo   harness kodu · ölçüm çıktıları · künyeler
kart   harness açık/kapalı tablo · SINIRLAR · yasal uyarı
       + "merge yapılandırması DEV'de 3 varyant arasından seçildi" beyanı
```

---

## S5 — SERVİS → 🟩 DROP B

### Mimari

```
web arayüz → API (FastAPI) → harness → llama-server (GGUF)
                                ↓
                          indeks + korpus
```

S3 harness'ı çalışan kod bırakır; S5 onu **kurulabilir** hâle getirir. Yeni algoritma yok.

### Yığın

| katman | seçim | gerekçe |
| :--- | :--- | :--- |
| arka uç | **FastAPI** | harness zaten Python, dil sınırı yok |
| ön yüz | **TypeScript** (hafif) | SSR ihtiyacı yok |
| veritabanı | ⭐ **SQLite** | kendi sunucusuna kuran için tek dosya, servis yok, yedek = kopyala. Postgres ihtiyacı C'de doğar |
| model | **llama.cpp** | alt katman zaten kurulu, GGUF üretiliyor |
| paket | **Docker Compose** | tek `up`; ⚠️ Windows'ta GPU geçirme belgelenir |

**Donanım:** LLM **GPU** ister; harness **CPU**'da — *"harness GPU'ya girmez"* kuralı
sığar/sığmaz farkını yaratan şey.

```
tek kullanıcı (1 slot · 8192 ctx · KV q8_0) — HESAP, ölçüm değil:
  ağırlık Q4_K_M   2,59 GiB
  KV önbelleği     ~0,5 GB
  hesap tamponları ~0,3 GB
                   ────────
                   ~3,5 GB   →  6 GB VRAM rahat yeter
                                4 GB'de -c 4096 ile muhtemelen çalışır
```

⚠️ Bu sayılar **hesap**. S3'te uçtan uca koşarken **gerçek tepe değer ölçülüp** README'ye
"asgari donanım" olarak yazılır. (Eval'de `-np 4` kullanıldı — 230 cevap paralel üretildiği
için; tek kullanıcıda 1 slot yeter ve KV maliyeti dörtte bire iner.)

**Artefakt yerleşimi:** kod imajda · **ağırlık (2,59 GiB) ilk açılışta HF'den, volume'da** ·
korpus + indeks aynı volume. Gerekçe: sürüm bağımsızlığı (app `v1.3` ↔ model `v1.0`), imaj
boyutu (~500 MB ↔ ~5 GB), standart pratik. **Çevrimdışı kurulum yolu belgelenir** — mahremiyet
vaadi olan üründe tutarlılık meselesi.

### Kapsam

```
✅ hesap + oturum · sohbet geçmişi · atıf paneli · görünür red
❌ mobil uygulama · belge yükleme · BİZİM işlettiğimiz canlı servis   → C
```

> **Arayüzün asıl işi:** ürünün farkı *"cevap veriyor"* değil **"cevabını doğrulatabiliyorsun"**.
> Kullanılan kaynaklar ✅ işaretli ve `mevzuat.gov.tr`'ye tıklanabilir olmalı. **Red görünür
> olmalı** — çoğu asistan bunu başarısızlık gibi saklar; bizde **ürünün vaadi bu**.

### Çıkış ölçütü

```
✅ SIFIRDAN kurulum yalnız belgeyle, TEMİZ KONTEYNERDE çalışıyor
   (kendi makinemde doğrulanamaz — her şey kurulu)
✅ red görünür ve gerekçeli · atıflar tıklanabilir
✅ yasal uyarı arayüzde, dipnotta değil
```

---

## S6+ — PLATFORM → 🟪 DROP C

```
C1  belge katmanı     okuma (sözleşme incele) → yazma (dilekçe üret)
                      ⚠️ mevcut modelin EĞİTİLMEDİĞİ işler — ayrı veri, ayrı ölçüm.
                         Vaat edilerek değil, ölçülerek eklenir
C2  niş derinlik      kira · iş · tüketici
C3  e-Devlet / UYAP   kullanıcının kendi dosyası
C4  canlı servis      ⬇️ barındırma kararı
C5  HITL              gönüllü avukat geri bildirimi → ORPO
```

### C4'ün bedeli — açıkça

GPU'lu VPS **~$100-300/ay, süregelen**. Aralıklı çalışan bir projede bu bir yükümlülük.

**Ucuz ve dürüst yol:** C4'ü *"bizim işlettiğimiz platform"* değil, **kendi kurduğun uygulama +
hız sınırlı bir tanıtım örneği** olarak kur. B zaten kurulabilir; C4 ona kayıt istemeyen bir
vitrin ekler. Vatandaş platformu vaadi böyle karşılanır, aylık faturaya girmeden.

---

## ⭐ Model bakım halkası

**Sorun gerçek:** 1-2 yılda base modeller değişir, `v1.0` geriler.

**Ama biz bir model değil bir REÇETE ürettik:**

```
yeni base  →  τ_g yeniden eğit   ~$4,4  (1.083 adım, reçete yazılı)
           →  τ_a yeniden eğit   ~$1,3  (70 adım)
           →  merge              $0     (ham TIES, ADR-0052)
           →  eval               ~$1    (hat kurulu)
              ────────────────────────
              TOPLAM ~$7 · ~1 gün
```

> Tüm o disiplinin **asıl getirisi budur**. Sabit seed, künye, ADR ve araştırma kaydı *"makale
> yazarken lazım olur"* diye tutulmuyordu — onlar sayesinde **model eskimesi bir kriz değil,
> bir günlük iş.**

**Tetikleyici takvim değil, olay:**

```
belirgin daha iyi bir ~4B base çıktı   → reçeteyi koştur, ölç, kıyasla
kendi eval'imizde gerileme             → incele
mevzuat değişti                        → İNDEKSİ tazele (model DEĞİL)
```

Üçüncüsü kritik: **güncellik harness'ın işi, ağırlığın değil.** Bu ayrım en baştan doğru kuruldu.

---

## Rakip çerçevesi — ölçüt, hedef değil

1-2 yılda Gemini Flash-Lite bugünkü Flash olur. *"FL'i geçmek"* koşan bir hedef.

**Yapısal üstünlüğümüz bundan etkilenmiyor: güncellik.** Kapalı ağırlıklı hiçbir model bugünün
mevzuatını bilemez; canlı API'li bir sistem bilir. Bu bir yarış değil **kategori farkı** — ve
zamanla **büyüyor**, çünkü onların ağırlıkları eskiyor.

İkinci yapısal fark: **mahremiyet**. Hukuki sorular kişiseldir; yerel çalışan bir sistemin
verdiği garantiyi bulut API'si veremez.

Rakip sayıları **ölçüt** olarak kalır, **hedef** olarak değil.

---

## Bütçe

```
S3a → S5   ~$5 toplam (hakem) · GPU $0 (hepsi yerel)
kalan      Modal $22,31
C4         barındırma — ayrıca karar verilir
bakım      ~$7/tur
```

**Asıl kısıt para değil, zaman.**

---

## Sözü geçen kararlar

| | |
| :--- | :--- |
| K2 chunk birimi = **madde** | atıf birimi olduğu için |
| K3 korpus | canlı API **şart**; ölçüm donmuş anlık görüntüde |
| K5 red kapısı | [ADR-0038](../adr/0038-red-kapisi-esigi-kati.md) katı; aşırı-red ölçülür |
| donmuş TEST | v1.0'da harcanır, **v2.0 için yeni set üretilir** |
| S5 veritabanı | SQLite |
| belge katmanı | C'ye |
| ⚠️ Mike (mikeoss) | **AGPL-3.0** — fikir olarak bakılır, **kod kopyalanamaz** (Apache-2.0 ile uyumsuz) |

**Açık kalanlar** (sırası gelince çözülür): K1 gömme modeli (recall@k ile ölçülür) ·
K4 harness-açık ölçüm protokolü (ADR olarak sunulur) · S5 paketleme ayrıntıları ·
Türkçe muhakeme yöntemi.
