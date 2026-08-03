# #48 — CP2-c: Modal köprüsü · sürekli besleme **1,84×** · `-np` ölçeklemesi **çalışmadı**

**Tarih:** 2026-08-02 · **Checkpoint:** `sprint2.md` CP2-c (hazırlık + üretim başlangıcı) ·
**Modal GPU:** smoke koşuları · **Hakem:** $0 (bu turda hakem çağrılmadı)
**Karar belgeleri:** [ADR-0047](../../adr/0047-cp2-hedef-750-modal-hasat.md) m.2 (taşıyıcı) · m.3 (verim kapısı) ·
[ADR-0049](../../adr/0049-sprint2-kalan-kararlarin-kilitlenmesi.md) m.5 (kabul zinciri)
**Yazılan:** `modal_train.py::harvest_cp2` + `spawn_cp2c` · ⭐ `scripts/cp2c_kabul.sh` ·
**düzeltilen:** `scripts/cp2_harvest.py` (verim kapısı + künye)

> ⚠️ **Başlıktaki *"`-np` ölçeklemesi çalışmadı"* ibaresi aynı gün ÇÜRÜDÜ.** Başlık ve sabahki
> bölümler **değiştirilmedi** (kayıt = o anki bilgi durumu); düzeltme bu dosyanın sonundaki
> **"16:19-16:47 · üretim denemesi ve verim kapısı olayı"** bölümünde. Aynı kartta `-np 64`,
> `-np 32`'den **hızlı** çıktı.

---

## Sorulan soru

CP2-c'nin hasadı Modal'da koşacak (ADR-0047 m.2, yerel şık #47'de ölçülüp elendi). Peki
**hangi kodla?** — ve `-np 32` gerçekten ne veriyor?

## ⭐ Eksik köprü: `modal_train.py` CP2'yi hiç tanımıyordu

`modal_train.py`'nin mevcut `harvest_rejected` fonksiyonu **eski** `scripts/gen_v3_rejected.py`'yi
çağırıyor. CP2 ise `scripts/cp2_harvest.py` kullanıyor: **bütçeli düşünce** (1024+512, zorunlu
kapatma) · **iki tip** (M2-tipi / M2b-tipi, ADR-0045 m.4) · **eş zamanlı** üretim. Yani Modal
tarafında CP2-c'nin koşacağı bir giriş noktası **yoktu**.

Yazıldı: `harvest_cp2` (uzak fonksiyon — GGUF'u volume'dan alır, `llama-server`'ı `-np` ile ayağa
kaldırır, `cp2_harvest.py`'yi HTTP üstünden sürer) + `spawn_cp2c` (yerel giriş noktası,
`spawn()` + `--detach`, tuzak 6.1).

## Taşıyıcı künyesi — ADR-0047 m.2 birebir korundu

```
imaj        ghcr.io/ggml-org/llama.cpp:server-cuda
llama-server version 10223 (11924d4c1)
model       models/gguf/q35-4b-q4_k_m.gguf   (Q4_K_M)
sha256      214826aaca724dc790bb0294dc77446505a40c8fe09d9f170260d6434600baf3
bayraklar   -fa on · --cache-type-k q8_0 · --cache-type-v q8_0 · --no-context-shift
ctx         8192 / slot
```

**vLLM/bf16 kullanılmadı** — bf16'da üretilen negatifler dağıtılan modelin hataları değildir
(ADR-0047 m.2). Taşıyıcı yerel ölçümlerle **aynı**; değişen yalnız kart ve `-np`.

## Üç kırılma ve onarımı — üçü de "GPU parası yandıktan sonra" sınıfı

### 1. Hazır imajın `ENTRYPOINT`'i

`ghcr.io/ggml-org/llama.cpp:server-cuda` imajının `ENTRYPOINT`'i `/app/llama-server`. Temizlenmezse
Modal'ın çalıştırıcısının verdiği `python …` komutu **ona argüman olur** ve konteyner
`error: invalid argument: python` ile ölür.

**Onarım:** `.entrypoint([])`. Belirti: konteyner saniyeler içinde ölür, GPU logu **hiç açılmaz**.

### 2. `requirements.lock.txt` bir **eğitim** lock'u

İçinde `openai` yok — hasat betiğinin HTTP istemcisi ona bağlı. Sonuç: `ModuleNotFoundError`,
**GPU ayrıldıktan sonra**, konteynerin içinde.

**Onarım:** `pip_install("openai==2.41.0")` — sürüm yerel ortamla eşitlendi.

### 3. Öbekli istemci slotları boş bekletiyordu

`cp2_harvest.py`'nin eş zamanlılığı `pool.map` **chunked** desenindeydi: her öbek en yavaş kalemini
bekliyor. Ölçüldü:

| | değer |
| :--- | --: |
| yapılan iş | **10.220** slot-saniye |
| ayrılan kapasite | **14.496** slot-saniye |
| **slot doluluğu** | **%70** |

**Onarım:** sürekli besleme (`FIRST_COMPLETED` + biten yerine yenisini doldur). ⚠️ **Gönderilen
istek, sıra, seed ve örnekleme aynı** — değişen yalnız zamanlama, yani üretilen veri etkilenmiyor.

## Hız ölçümleri

Hepsi aynı GGUF, aynı rejim (**düşünce 1024 + cevap 512, seed 3407**), tip belirtilmedikçe **m2**:

| koşu | `-np` | istemci | denenen | kümülatif s/üretim | marjinal s/üretim | regex kabul |
| :--- | --: | :--- | --: | --: | --: | --: |
| smoke m2 | 32 | öbekli | 64 | 3,65 | — | %18,8 |
| smoke m2b | 32 | öbekli | 64 | 3,43 | — | %25,0 |
| **smoke2** m2 | 32 | **sürekli** | 159 | **1,98** | **1,58** | %28,9 |
| np64 m2 | **64** | sürekli | 255 | 2,93 | **2,09** | %32,6 |

- **Sürekli besleme kazancı 1,84×** (3,65 → 1,98).
- Ortalama completion token **~1.108**; zorunlu kapatma her koşuda **tam** (159/159, 255/255).

## 🔴 NEGATİF BULGU — slot sayısını ikiye katlamak yardım etmedi, **%32 kötüleştirdi**

Hipotez ölçülebilirdi: 4B Q4 model **2,6 GB**; A100-40GB bant genişliği **1,55 TB/s** → ağırlık
okuma tavanı ~**19.000 tok/s**. Ölçülen toplam verim **307 tok/s** = tavanın **%1,6'sı**. Yani
darboğaz bant genişliği değil, **adım başına sabit maliyet** → `-np` artışı neredeyse doğrusal
kazanç vermeliydi.

**Vermedi.** `-np 32` kaldı — ADR-0047'nin serbest bıraktığı tek değişken zaten `-np` ve karttı.

### ⚠️ Ayrılamayan karıştırıcı — dürüstlük şerhi

`-np 32` koşusu, künyeye **kart adı eklenmeden önce** koştu; `-np 64` koşusu
`NVIDIA A100-SXM4-40GB`'de koştu. Modal'ın `gpu="A100"` takma adı hem **40GB** hem **80GB**
verebiliyor ve iki kartın bant genişliği oranı **1,31×** (1,55 ↔ 2,03 TB/s) — gözlenen fark ise
**1,32×**.

→ *"slot artışı işe yaramadı"* ile *"np64 yavaş karta düştü"* **ayrılamıyor.** Karar değişmiyor
(`-np 32` **ölçülen** hızlı olan), ama **nedensellik iddiası kurulmuyor.**

> ### ➕ EK NOT (2026-08-02, 16:47 sonrası) — bu karıştırıcı **ÇÖZÜLDÜ**
> Yukarıdaki metin **olduğu gibi duruyor**; aşağıdaki bölüm onu üstüne yazmaz, tamamlar.
> `-np 32` üretim denemesi künyeye `gpu_gercek` yazıldıktan **sonra** koştu ve kartı
> `NVIDIA A100-SXM4-40GB` çıktı — yani `-np 64` koşusuyla **aynı kart**. Aynı kartta ölçülen
> kararlı hızlar: `-np 32` **~2,4 s/üretim** (m2) ↔ `-np 64` **~2,09 s/üretim** (m2). Yani
> **aynı kartta slot artışı YARDIM EDİYOR**; yukarıdaki *"%32 kötüleşme"* okuması hem karttan
> hem de **yanlı tahmin ediciden** (kümülatif ortalama) doğmuştu. Detay ve tablolar: bu dosyanın
> sonundaki **"16:19-16:47 · üretim denemesi ve verim kapısı olayı"** bölümü ↓

**Sonuç:** künyeye `nvidia-smi`'den okunan `gpu_gercek` alanı eklendi (`modal_train.py`), bundan
sonraki her koşu kartını kaydeder. → yeni tuzak **6.7**.

## Bulunan ve düzeltilen iki kusur — `scripts/cp2_harvest.py`

### 1. Verim kapısı (ADR-0047 m.3) **atlanabiliyordu**

Kapı `limit` kontrolüne takılıyordu: `-np 64` koşusu **2,93 s/üretim** ile (eşik **2,88**) huniye
hak edilmemiş bir **"geçildi"** damgası bastı. Bir ön-kayıtlı kapının sessizce geçilmiş görünmesi,
kapının hiç olmamasından kötüdür.

**Onarım:** kapı artık `limit` kontrolünden **önce** değerlendiriliyor; hiç değerlendirilmediyse
künyedeki damga `değerlendirilmedi (koşu <gate_after_s>s'den kısa bitti)` diyor.

### 2. `--limit` eş zamanlılık kadar **aşıyor**

192 istendi → **255** üretildi. Sebep: `tried` **tamamlananı** sayıyor, uçuştaki istekler iptal
edilmiyor. Üretim ölçeğinde (7.500) sapma **<%1** — ama maliyet ile huni sayısı uyuşmazsa sebebi
budur, kayda geçiyor.

## İkinci eksik köprü: kabul zincirinin **sürücüsü yoktu**

ADR-0049 m.5 kabul tasarımı **B**'yi kilitlemişti, ama onu koşturan hiçbir betik yoktu.
`scripts/cp2c_kabul.sh` yazıldı:

```
cp2_audit.py           → gpt-4o-mini verdict      (ABSTAIN ise ELE)
                       → FABRICATE alt kümesi
                       → gpt-4o verdict TEYİT     (A tasarımında ~%9,5 kirlilik kalıyordu)
valid_trap_cache.py    → gpt-4o KÖR geçerlilik damgası (ADR-0048)
                       → birleştirme + kabul_huni.json
```

## ✅ Kabul oranı ADR-0049'un ön-kayıtlı hunisiyle tutuyor

Ön-kayıtlı huni *"regex ~%30 geçer"* diyordu; ölçülen **%28,9 – %32,6** (sürekli besleme koşuları).
Yani hedef 750 negatif = **7.500 üretim** varsayımı ayakta.

---

## ⚠️ #47'YE DÜZELTME — "kayıtlı 7 s/it yanlıştı" ifadesi **iki farklı rejimi** karşılaştırıyor

[#47](2026-07-30-cp2s-boru-hatti.md) *"kayıtlı 7 s/it **yanlıştı**, gerçek ~70"* diyor. Yanlış olan
kayıt değil, **kıyas**: iki sayı aynı rejime ait değil.

| | **6,8-7,0 s/it** | **~70 s/it** |
| :--- | :--- | :--- |
| yöntem | **SFT** | **ORPO** |
| efektif batch | **16** | **64** |
| kaynak | `τ_g`'nin gerçek 1.083 adımlık koşusu | CP2-s smoke'u |

Doğrulandı: `data/.../raft_scrubbed/train.jsonl` **17.323 satır ÷ 16 = 1.083 adım** — yani kayıtlı
SFT hızı `τ_g`'nin fiilen koştuğu adım sayısını üretiyor.

**Sonuç:**

- **CP4 / CP5'in SFT tahminleri AYAKTA** (~**$5,7** / ~**$6,5**) — onlar SFT koşuları.
- Yalnız **ORPO** kalemleri ~**4×** pahalılaştı (batch 64'te adım başına iş 4 kat büyük).
- CP3 (`τ_a`, ORPO, ~73 adım) için #47'nin **~$3,2** tahmini geçerli kalıyor.

*(#47'nin kendi dosyasına da bu düzeltmeye işaret eden bir not düşüldü — sessizce üstüne
yazılmadı, CLAUDE.md'nin çelişki kuralı.)*

---

## Ders

**Bir işi buluta taşımak, kodu taşımak değil — çalışma ortamının varsayımlarını taşımaktır.**
Üç kırılmanın üçü de kodun kendisiyle ilgili değildi: imajın entrypoint'i, lock dosyasının hangi
iş türü için üretildiği, ve istemcinin eş zamanlılık deseni. Üçü de **GPU ayrıldıktan sonra**
patlıyor ya da hiç patlamıyor, sadece pahalı oluyor.

İkinci ders: **künye eksikse ölçüm sonradan tamamlanamaz.** `gpu_gercek` alanı bir koşu geç
eklendiği için `-np` ölçeklemesinin negatif sonucu **nedensel olarak okunamaz hâle geldi** —
sayı duruyor, açıklaması yok.

## Paper eşlemesi

- **Methodology:** taşıyıcı kimliğinin koşular arası sabitlenmesi (imaj + sürüm + GGUF sha256 +
  bayraklar); on-policy hasadın dağıtılan taşıyıcıyla aynı kipte üretilmesi.
- **Limitations:** `-np` ölçeklemesinin negatif sonucu **kart karıştırıcısından ayrılamadı**;
  bulut sağlayıcısının GPU takma adı donanımı garanti etmiyor.
- **Negatif bulgu:** eş zamanlı slot sayısını ikiye katlamak, ağırlık-okuma tavanının %1,6'sında
  koşan bir 4B modelde verim **kazandırmadı** (≥ %32 kötüleşme gözlendi).

## Yeni yürütme tuzakları

**6.4** hazır imajın `ENTRYPOINT`'i · **6.5** lock dosyası iş türüne göredir ·
**6.6** öbekli eş zamanlı istemci slotları boş bekletir · **6.7** `gpu="A100"` iki farklı kart
verir · **6.8** kümülatif ortalamayı erken okuyup karar verme.

---
---

# Üretim hasadı — verim kapısı ve **tahmin edici düzeltmesi** (16:19 →)

> **Bu bölüm #48'in DEVAMIDIR**, üstüne yazmaz. Yukarısı sabahki köprü-kurma ve smoke
> ölçümlerini anlatıyor; burada ilk **üretim** denemesi, ön-kayıtlı verim kapısının gerçeklikle
> karşılaşması ve yeniden başlatılan `-np 64` koşusu var.
>
> **Doğan karar:** [**ADR-0050**](../../adr/0050-verim-kapisi-tahmin-edici-duzeltmesi.md) — verim
> kapısının **tahmin edicisi** düzeltildi, **eşik 2,88 s/üretim aynı kaldı**; ADR-0047 m.3'ü
> **tadil eder** (metni değişmedi, yanına not düşüldü). Yeni yürütme tuzağı: **6.9**.

**Tarih:** 2026-08-02, 16:19 → 16:47 · **App:** `ap-5f6rLHHFohhupMGvhkla9I` ·
**Kart:** `NVIDIA A100-SXM4-40GB` *(künyeden, `gpu_gercek`)* · **`-np` 32** ·
**`--limit` 3750/tip** = hedef 7.500 üretim · **Çıktı:** `hukuk-data:/cp2c/` ·
**GPU maliyeti:** ~**$1,2** *(⚠️ TAHMİN — panelden okunacak, tuzak 6.3: Modal sayısı defterden türetilmez)*

## 1. Ne oldu — verim kapısı **iki tipte de** tetiklendi

| tip | denenen | aday (regex) | oran | kümülatif s/üretim | geçen s | kapı damgası |
| :--- | --: | --: | --: | --: | --: | :--- |
| **m2** | 233 | 68 | **%29,2** | 2,89 | 672,9 | 🔴 `DURDU: 2.97 > 2.88 (202 üretimde)` |
| **m2b** | 235 | 45 | **%19,2** | 2,96 | 694,9 | 🔴 `DURDU: 2.95 > 2.88 (204 üretimde)` |

- Zorunlu kapatma **her iki tipte de tam**: 233/233 · 235/235.
- Ortalama completion token: m2 **1108,0** · m2b **1138,7**.
- **113 aday kaybolmadı** — `hukuk-data:/cp2c/` altında duruyor ve kabul aşamasında kullanılacak.

Kapı ön-kayıtlıydı (ADR-0047 m.3) ve **doğru çalıştı**: eşiği aştığını gördü, koşuyu durdurdu,
damgayı künyeye yazdı. Sorun kapının varlığında ya da eşiğinde değil, **ölçme aletindeydi.**

## 2. ⭐ METODOLOJİK BULGU — kapı doğru ölçüte, **yanlı bir tahmin ediciyle** bakıyordu

Kapı `geçen_süre ÷ tamamlanan` okuyordu — yani **t0'dan itibaren kümülatif ortalama**. Yüksek
eş zamanlılıkta `concurrency` kadar istek aynı anda başlar ve **aynı anda iner**; bu açılış
geçicisinin maliyeti kümülatif ortalamada **her kaleme paylaştırılır**. Sonuç: erken okumada hız
**sistematik olarak kötü** görünür. Bu, tuzak **6.8**'in kendisi — ama tuzağı bilmek onu koddan
çıkarmaya yetmemiş.

Aynı logdan pencere pencere **marjinal** hız (m2):

| pencere | üretim | süre | marjinal s/üretim |
| :--- | --: | --: | --: |
| 0 → 25 | 25 | 142 s | **5,70** ← açılış dalgası |
| 100 → 175 | 75 | 167 s | **2,22** |
| 100 → 200 | 100 | 238 s | **2,38** |
| 200 → 225 | 25 | 73 s | **2,90** ← kapı sonrası **boşalma** fazı |

→ m2'nin gerçek (kararlı) hızı ~**2,4 s/üretim**, yani eşiğin **altında**.
m2b'nin kararlı hızı ~**3,0 s/üretim** — m2'den ~**%25 yavaş**; çeldirici blokları prefill'i
uzatıyor.

> ### 🔍 Doğrudan kanıt — kapının kendi logu kendini çürütüyor
> Kapı **600. saniyede** `2,97` ile durdurdu. Aynı koşu **673. saniyede zaten `2,89`'daydı**.
> Yani ölçülen büyüklük kararlı hâline doğru **hâlâ inerken** karar verilmişti. Tahmin edici
> yanlı olduğu için kapı, ölçmek üzere kurulduğu şeyi (ölçekte s/üretim) ölçemiyordu.

7.500 üretimlik gerçek bir koşuda açılış dalgası toplam sürenin ~**%0,6'sı** — yani ölçekte
**amortize oluyor** ve kümülatif ortalama ile marjinal hız birbirine yakınsıyor. Yanlılık
tamamen **erken okuma** problemidir.

## 3. Karar (insan, 2026-08-02): **şık A — eşiğe dokunulmadı, tahmin edici düzeltildi**

→ [**ADR-0050**](../../adr/0050-verim-kapisi-tahmin-edici-duzeltmesi.md). Üç şık sunuldu, insan
**A**'yı seçti: *eşiğe dokunma, tahmin ediciyi düzelt.*

**❌ REDDEDİLEN (B) — eşiği 2,88 → 3,2 gevşetmek.** Sonucu gördükten sonra ön-kayıtlı bir eşiği
oynatmak, ön-kayıt kurumunun kendisini geçersiz kılar. Bu hattın Kapı 5 / ADR-0039 dersi tam
tersi yöndeydi: kapı ölçemez hâle gelince **kapı bölünür**, eşik gevşetilmez.

**❌ REDDEDİLEN (C) — CP2-c'yi negatif bulgu olarak kapatmak.** Yanlış olan taşıyıcı ya da hasat
tasarımı değil, **ölçen aletti**. Ölçüm aracının yanlılığını "sonuç" diye kaydetmek, kayda
geçen sayıyı kalıcı olarak yanlış yapar.

**✅ UYGULANAN (A) — kapı artık *kararlı* hızı okuyor.** `scripts/cp2_harvest.py`'de eşik,
boru hattı `concurrency` kalemle **dolduktan sonraki** süre ÷ o andan sonraki üretim üzerinden
değerlendiriliyor. Huniye `saniye_per_uretim_kararli` alanı eklendi; kümülatif
`saniye_per_uretim` **eski koşularla karşılaştırılabilirlik için yerinde duruyor** — silinmedi.

> **Ön-kayıtlı BÜYÜKLÜK değişmedi** (ölçekte s/üretim, eşik **2,88**). Değişen, o büyüklüğü
> ölçen aletin **yanlı** olduğunun anlaşılmasıdır. Ayrımı raporda korumak şart: eşiği kaydırmak
> ile tahmin ediciyi düzeltmek aynı şey değildir.

### İkinci kusur da düzeltildi — hak edilmemiş "geçildi" damgası

Kapı `--limit` kontrolüne takılıp **hiç değerlendirilmeden atlanabiliyordu**; bu durumda huniye
hak edilmemiş bir *"geçildi"* damgası düşüyordu. Sabahki `-np 64` testi (2,93 s/üretim, eşik
2,88) **tam bunu yapmıştı**. Artık kapı `limit` kontrolünden **önce** değerlendiriliyor; hiç
değerlendirilmediyse damga `değerlendirilmedi` diyor. *(Bu düzeltme yukarıda da kayıtlı; burada
olayla birlikte tekrar anılıyor çünkü yanlı tahmin edici ile aynı koşuda ısırdı.)*

## 4. `-np` seçiminin gerekçesi düzeltildi — karıştırıcı **çözüldü**

Bu dosyanın *"🔴 NEGATİF BULGU — slot sayısını ikiye katlamak %32 kötüleştirdi"* bölümü **yerinde
duruyor** ve şerhi de doğruydu: o sonuç **iki FARKLI kartı** karşılaştırmaktan doğmuştu.

Şimdi **aynı kartta** (`NVIDIA A100-SXM4-40GB`) ölçülenler:

| `-np` | tip | kararlı s/üretim |
| --: | :--- | --: |
| 32 | m2 | ~**2,4** |
| 32 | m2b | ~**3,0** |
| **64** | m2 | ~**2,09** |

→ **Aynı kartta slot artışı YARDIM EDİYOR.** Sabahki negatif bulgu iki ayrı hatanın toplamıydı:
(a) kart karıştırıcısı (tuzak 6.7), (b) kümülatif ortalamanın yanlılığı (tuzak 6.8).
`gpu_gercek` alanının eklenmesi karıştırıcıyı **aynı gün** çözebilir hâle getirdi — künye
disiplininin doğrudan getirisi.

## 5. Yeni koşu — `-np 64` (yeniden başlatma)

```
app          ap-LHKDDasU1MD6b4xG10WK8W          (17:05'te GEÇERLİ koşu olarak seçildi)
başlangıç    2026-08-02 16:47
çıktı        hukuk-data:/cp2c-64/
-np          64          · --limit 3750/tip = 7.500 üretim
kart         NVIDIA A100-SXM4-40GB              (künye · gpu_gercek)
kapı         düzeltilmiş (kararlı hız) · eşik 2,88 AYNI
beklenti     m2 ~2,09 · m2b ~2,6 kararlı → ~4,4 saat ≈ $11   (⚠️ TAHMİN)
```

> ### 🚨 AÇIK OLAY (2026-08-02, oturumda doğrulandı) — **iki detached iş aynı anda koşuyor ve aynı dosyaya yazıyor**
> `modal app list` + `modal container list` + iki app'in logu:
>
> | app | oluşturma | konteyner | `--out` | log |
> | :--- | :--- | :--- | :--- | :--- |
> | `ap-LHKDDasU1MD6b4xG10WK8W` | 16:47 +03 | `ta-01KZ1BP2X8SJQZEY0670S81NER` **CANLI** | `/data/cp2c-64/cp2c_m2.jsonl` | `devam=0 kayıt` · denenen=250'de kümülatif **1,67** / kararlı **1,47** |
> | `ap-5d1ssJOgSKZz1VNAQvxwhD` | 16:52 +03 | `ta-01KZ1BZA1CF9BWJQXZW2CVRA6R` **CANLI** | `/data/cp2c-64/cp2c_m2.jsonl` | `devam=24 kayıt` · denenen=25'te **5,08** (açılış dalgası) |
>
> İkisi de `-np 64`, ikisi de `A100-SXM4-40GB`, ikisi de **aynı çıktı dosyası** ve aynı
> `llama_server.log` yolu. İkincisi birincinin yazdığı **24 kaydı** `load_done` ile atlayarak
> başlamış; ama havuz sırası **seed'e bağlı ve deterministik** olduğu için ikisi büyük ölçüde
> **aynı kalemleri** üretip **aynı dosyaya** ekliyor. Sonuçları: (a) GPU maliyeti **iki katı**,
> (b) `cp2c_m2.jsonl`'de **yinelenen id** riski, (c) `KUNYE.json`/huni dosyasını **son biten iş
> yeniden yazar** → künyedeki sayaçlar dosyanın içeriğini tarif etmez. Yani provenansı korumak
> için ayrı dizin kullanma kararı (aşağıda) **bu çakışma tarafından delinmiş** olur.
>
> **✅ ÇÖZÜM (17:05).** `ap-5d1ssJOgSKZz1VNAQvxwhD` durduruldu (`modal app stop -y`);
> `ap-LHKDDasU1MD6b4xG10WK8W` sürdü. **Seçim ölçütü ilerlemedir, başlangıç saati değil:**
> durdurulan iş ~200 üretim **geride**ydi (log: `denenen=625` ↔ `denenen=~425`), yani onu
> tutmak yanmış GPU'yu bir kez daha yakmak olurdu. Bedel: ~20 dk fazladan GPU (**~$0,8**,
> panelden doğrulanacak).
>
> **Kalıcı iz — kabul zinciri bunu onarmak zorunda:** (a) `/cp2c-64/cp2c_m2.jsonl`'de
> **yinelenen id**'ler, (b) durdurulan süreç yazarken kesildiği için **yarım son satır**.
> İkisi de sessiz yanlışlık: zincir çökmeden yanlış sayı üretir. Onarım kabul zincirinden
> **önce**, ayrı ve kayıtlı bir adım olarak yapılır → **`scripts/cp2c_birlestir.py`**
> (id bazlı tekilleştirme · yarım **son** satırı atar · **ortadaki** bozuk satırda çöker,
> çünkü o bilinen kesilme kalıbı değildir · her kayda `kaynak`, dizine `BIRLESIM.json`).
> Karışım künyesi zaten gerekiyordu (aşağıda, iki dizin) — aynı araç onu da üretir.

*(⚠️ Bu kayıtta bir ara geçerli koşu olarak `ap-5d1ss…` / 16:52 yazılıydı; yukarıdaki ölçüt
uygulanınca `ap-LHKDD…` / 16:47 seçildi. Eski satır silinmedi, tabloda **iki app de** duruyor.)*

**Neden AYRI dizin — provenans.** Aynı dizine yazılsaydı künye `np: 64` derken **113 kayıt
`-np 32`'den** gelmiş olacaktı. İki dizin sayesinde iki künye de dürüst kalıyor. Kabul
aşamasında iki dosya **birleştirilecek ve karışım künyeye açıkça yazılacak**
(ADR-0047 m.2 `-np` ve kartı zaten serbest bırakıyor).

> ⚠️ **Risk:** m2b m2'den ~%25 yavaş olduğu için `-np 64`'te de **kapıya yakın** koşacak.
> Takılırsa m2 tam, m2b kısmi kalır.

## 6. ⚠️ Verim uyarısı — regex kabul oranı **tipe göre ayrışıyor**

ADR-0049'un ön-kayıtlı hunisi *"regex ~%30 geçer → 7.500 üretim → ~2.250 aday → ~750 temiz"*
varsayıyordu. Ölçülen:

| tip | regex kabul | varsayıma göre |
| :--- | --: | :--- |
| m2 | **%29,2** | ✅ uyumlu |
| m2b | **%19,2** | ⚠️ **altında** |
| iki tip birlikte | ~**%24** | ⚠️ altında |

→ 7.500 üretimde regex-aday beklentisi ADR'nin **2.250**'sinin altına inebilir; dolayısıyla
**750 temiz negatif hedefi risk altında.** Kesin sayı hasat bitince okunacak — **şimdiden hedef
değiştirilmiyor**, çünkü tahmine dayanarak ön-kayıtlı hedefi oynatmak bu bölümde reddedilen
davranışın aynısı olur. Bağlantı: ADR-0047'nin *"ön-eleme yeterli geçerli tuzak bırakmazsa hedef
otomatik iner"* koşullu geri alma maddesi.

---

## Ders (bu bölümün)

**Bir ön-kayıtlı kapı iki bağımsız şeydir: ölçtüğü BÜYÜKLÜK ve onu ölçen TAHMİN EDİCİ.**
Sonucu gördükten sonra büyüklüğe ya da eşiğe dokunmak ön-kaydı yakar; tahmin edicinin yanlı
olduğunu gösterip düzeltmek yakmaz — ama ancak **yanlılık sonuçtan bağımsız kanıtlanabiliyorsa**.
Burada kanıt koşunun kendi logundaydı: kapı 600. saniyede 2,97 diye durdurdu, aynı koşu 673.
saniyede 2,89'daydı. Bu ayrım raporda korunmazsa dışarıdan iki hareket **aynı** görünür.

İkinci ders: **künye disiplini geriye dönük ödüyor.** `gpu_gercek` alanı sabah bir negatif
bulguyu okunamaz hâle geldiği için eklenmişti; öğleden sonra aynı alan o bulgunun
karıştırıcısını **çözdü**.

## Paper eşlemesi (bu bölüm)

- **Methodology:** ön-kayıtlı yürütme kapılarında *büyüklük ↔ tahmin edici* ayrımı; kararlı-durum
  tahmin edicisi (`concurrency` doldurulduktan sonrası) ve kümülatif tahmin edicinin geriye dönük
  karşılaştırılabilirlik için **birlikte** raporlanması.
- **Limitations:** verim kapısı bir koşuyu **hatalı** durdurdu (~$1,2 GPU); ön-kayıtlı yürütme
  kuralları ölçüm yanlılığına karşı bağışık değil. Ayrıca `-np` ölçekleme sonucunun **düzeltilmiş**
  hâli raporlanır — ilk negatif bulgu iki karıştırıcı (kart + tahmin edici) taşıyordu.
- **Negatif bulgu (düzeltildi):** *"slot sayısını ikiye katlamak kötüleştirir"* iddiası **aynı
  kartta ölçülünce çöktü** — `-np 64` (m2 ~2,09) `-np 32`'den (m2 ~2,4) **hızlı**.

## 7. 🔴 ÜÇÜNCÜ EKSİK KÖPRÜ — hasat bitmeden bulundu: **m2b için `chosen` tarafı yok**

Hasat koşarken CP3'ün girdi zinciri önden denetlendi (tuzak 6.2'nin dersi: veri kapısı GPU'dan
önce). `cp2c_kabul.sh` bitiş satırı *"sıradaki: `build_orpo_v3.py` ile çift kur"* diyor. O betik
çifti şöyle kuruyor (satır 93-99):

```
src  = r["trap_text"][:900]
user = f"KAYNAK MADDE:\n{src}\n\nSORU: {r['soru']}"      ← ORACLE/M2 kalıbı, TEK madde
sys  = SYSTEM_PROMPT_RAG                                  ← RAG_MULTI DEĞİL
rejected = r["model_answer"]  ·  chosen = chosen_by_id[r["id"]]
```

Üç ayrı uyumsuzluk çıktı; ikisi mekanik, biri **tasarımsal**:

| # | ne | sınıf |
| :-- | :--- | :--- |
| 1 | **Alan adları tutmuyor.** CP2-c kaydı `rejected` / `context_shown` yazıyor, betik `model_answer` / `trap_text` okuyor. `abstained` alanı da yok (kabul zincirinde hakem zaten çekinmeleri elemiş oluyor) | mekanik — `KeyError` ile **çöker**, sessiz değil |
| 2 | **m2b'nin kalıbı ifade edilemiyor.** Betik sistem istemini ve `KAYNAK MADDE:` kalıbını **sabit** kuruyor; m2b'nin istemi `SYSTEM_PROMPT_RAG_MULTI` + `KAYNAKLAR:` çok-kaynak bloğu. Naif beslenirse hata vermez, yalnız kolu **eval'de hiç görülmeyen bir kalıpta** eğitir | 🔇 **sessiz yanlışlık** |
| 3 | **m2b için `chosen` metni HİÇ YOK** | 🔴 **tasarımsal boşluk** |

**(3)'ün kanıtı — mevcut `τ_a` eğitim seti sayıldı:**

```
data/train/orpo_abstain/train.jsonl        1.741 çift
  _kind=abstain  1.449  → sistem: "…sade, anlaşılır…"  · user: "KAYNAK MADDE:"   = M2 kalıbı
  _kind=ground     292  → sistem: "…uzman bir…"        · user: "KAYNAKLAR:"      = RAG_MULTI
```

RAG_MULTI kalıbı yalnız **grounding-replay** çiftlerinde var ve onların `rejected`'ı
placeholder + `is_pref=0`, yani OR terimi **maskeli** — çekinmeyi hiç öğretmiyorlar. Yani:

> **`τ_a`, bugüne dek M2b kalıbında tek bir çekinme çifti görmedi.**

Ve `data/_ham_ve_ara/orpo_chosen.jsonl`'deki `chosen` metinleri **oracle biçimli**:
*"Sağlanan {trap_kanun} MADDE 54 … hususunu düzenlemektedir; sorulan konu bu maddede yer
almamaktadır."* M2b'de **"sağlanan madde" diye tek bir şey yok** — 4 çeldirici var, gold hiç yok.
O metin m2b çiftine takılırsa doğru cevabın kendisi yanlış olur.

**Niçin bu can alıcı:** defterin negatif tablosunda `τ_a`'nın **gerçek** hedefi #4 —
*kaynak yokken susma (M2b)*, `τ_g` orada **0.986 → 0.607** çöküyor. m2b tipini hasat etme kararı
([ADR-0045](../../adr/0045-ara-kapi-merge-onarim-kontrolu.md) m.4) tam bunun içindi ve
**ARA KAPI'nın ikinci gözlemi** (merge M2b ≥ 0.854) bu eksende okunuyor. m2b yarısı çifte
dönüşemezse hasadın yarısı çöpe gider ve ARA KAPI, `τ_a`'nın hazırlanmadığı bir ekseni ölçer.

**(1) ve (2) zorunlu düzeltme** — seçim yok, eval-ayna kuralı kalıbı belirliyor: eğitim istemi
M2b eval istemiyle **birebir** olmalı, yani `SYSTEM_PROMPT_RAG_MULTI` + hasadın sakladığı
`context_shown` bloğu (hasat onu tam bu sebeple saklıyor — `cp2_harvest.py` satır 195-197).

**(3) bir karardır, kod değil → İNSANA SORULDU** (2026-08-02, hasat sürerken; CP3'ten önce
cevaplanması yeterli, hasadı bloklamıyor).

> ### ✅ KARAR (insan, 2026-08-02) — **şık A: şablon**, dış model kullanılmaz → [ADR-0051](../../adr/0051-m2b-cift-kalibi-ve-chosen-uretimi.md)
> Belirleyici gerekçe: hedef cümleyi **`SYSTEM_PROMPT_RAG_MULTI`'nin kendisi tarif ediyor**
> (*"İlgili kaynak YOKSA … 'Verilen kaynaklarda bu konuyu düzenleyen madde bulunmuyor' de"*),
> yani `chosen`'ın işi o talimatı örneklemek. Dış modele yazdırmak (**B**) yeni bilgi üretmez,
> yalnız o modelin üslubunu çifte sokar — `rejected` tarafı on-policy iken (ADR-0042) çift
> **iki modelin karışımı** olurdu. **C** (m2b'yi atmak) ADR-0045 m.4'ün gerekçesini iptal ederdi.
> Ölçülen: 45 gerçek kalemde **45/45 tekil** `chosen`. Kalıp-öğrenme riski **M1 A1 ≥ 0.880**
> muhafızıyla ölçülüyor ve ön-kayıtlı geri dönüş yolu B'dir (ADR-0051 m.3).
> (1) ve (2) karar değil zorunluluktu — eval-ayna kuralı gereği birlikte düzeltildi.

## 8. Kabul zinciri **mekanik smoke** — 5+5 kalem, $0,018 (hasat sürerken, hakem parası yanmadan)

CP2-s'in deseni tekrar edildi: *tam pilot değil, mekanik smoke* — **okunabilir sayı üretmeyecek
kadar küçük** tutuldu (çapalama riski). Amaç yalnız halkaların birbirine geçtiğini görmek.

**✅ Dört halka da çalıştı:** `cp2_audit` şema çevirisi (`--source-field` m2→`referans`,
m2b→`context_shown` doğru seçiliyor) · mini verdict · FABRICATE alt kümesinin gpt-4o'ya teyide
gitmesi · `valid_trap_cache.py`'nin beklediği `{mod}_{etiket}_detail.jsonl` dosya düzeni ·
kör damga · huni birleştirme + `kabul_huni.json`. Zincir **$3,68'lik koşuya hazır**.

> ### ⚠️ Smoke'ta m2b 0/5 çıktı — **ve bu gürültüydü** (aşağıda n=113 ile düzeltildi)
> 5 m2b adayının hiçbiri teyide gidemedi; metinler *"Verilen kaynakta bilirkişilik görevinin
> kime verilebileceği …"* diye başlayan **yumuşak çekinme**lerdi (tuzak 2.5'in regex↔hakem açığı).
> n=5'te *"m2b hakemde eriyor"* gibi okundu. **§9 bunu çürüttü** — n=45'te m2b hakem hayatta
> kalması m2'den **daha iyi** (%42,2 ↔ %38,2). Küçük örnekten yürüme uyarısı olarak burada
> duruyor; alarmın kendisi geçersiz.
>
> ADR-0048'in bulgusu ise tekrar göründü ve geçerli: **cevaba bağlı** geçerlilik ile **kör**
> damga aynı kalemlerde ayrıştı (m2b: cevaba bağlı 0/5 → kör damga **4/5 geçerli**).

## 9. Hasat verimi **ölçüldü** — n=113 gerçek kayıt, $0,018 (öne alınmış iş, israf yok)

§8'in alarmını sınamak için `/cp2c`'nin 113 gerçek adayı **tamamen** mini hakemden geçirildi
(bu iş kabul zincirinde zaten yapılacaktı; erken yapılması bedeli değiştirmiyor):

| tip | regex aday | mini FABRICATE | oran | ADR-0049 varsayımı |
| :--- | ---: | ---: | ---: | :--- |
| m2 | 68 | **26** | **%38,2** | ~%40 ✅ |
| m2b | 45 | **19** | **%42,2** | ~%40 ✅ |

**Hakem hayatta kalması sorun değil — iki tip de ön-kayıtlı huniye uyuyor.** §8'in alarmı
n=5 gürültüsüydü. Darboğaz **hakem değil, regex ön-filtresi**: m2 %31,3 geçirirken m2b **%19,2**
geçiriyor (ADR-0049 ikisi için de ~%30 varsaymıştı).

**Bunun sebebi base'in kendisi ve zaten ölçülüydü:** cevaba-kör base **M2b Rej 0.949** ↔
**M2 Rej 0.803** (CP2-r, [#46](2026-07-30-cp2r-kor-payda.md)). Base M2b'de zaten neredeyse hiç
uydurmuyor — yani *"m2b'den az negatif çıkar"* huninin kusuru değil, **hedef davranışın
kendisinin ölçüsü**. 7.500 üretimin 50/50 bölünmesi bu asimetriyi hesaba katmıyordu.

**Projeksiyon (⚠️ tahmin, fiili sayı kabul zincirinden okunacak):**

```
m2   3.750 × %31,3 = 1.174 aday × %38,2 = ~448 ham
m2b  3.750 × %19,2 =   720 aday × %42,2 = ~304 ham
/cp2c artığı                     113 aday          =  ~45 ham
                                          toplam ham ≈ 797
temiz (ADR-0049'un ham→temiz %83'ü)                  ≈ 660      hedef 750
```

→ **~%12 açık.** ADR-0047 m.1 hedefin altını **insana sorulacak** ilan ediyor. En ucuz kapatma:
bu koşu bittikten **sonra** ~1.500 üretimlik ek m2 turu (~40 dk, ~$1,6) — m2'nin üretim başına
verimi m2b'nin ~2 katı.

> ### 🐞 Ek tur **iki yoldan da yanlış çalışacaktı** — `--skip-first` eklendi
> Yukarıdaki tavsiye ilk yazıldığında *"ek tur ayrı dizine"* diyordu (tuzak 6.10 refleksi).
> Kontrol edilince ikisi de kırık çıktı:
>
> | yol | ne olur |
> | :--- | :--- |
> | **taze dizin** | `seen_ids` boş → havuz sırası **0'dan** başlar. Sıra `seed 3407` ile deterministik ve hasat onu **sırayla** yürüyor (doğrulandı: `/cp2c`'nin 68 kabulü havuz pozisyonu **1-229** arasında). Ek tur **aynı kalemleri** yeniden üretir |
> | **aynı dizin** | `load_done` çıktı dosyasından okuyor, o dosyada yalnız **KABUL edilenler** var (68), **denenenler** (233) yok. Ek turun ~%69'u zaten denenip elenmiş kalemleri **yeniden** üretir |
>
> İkisi de sessiz: hata yok, GPU yanar, sonra tekilleştirme havuzu küçültür ve *"neden az çıktı"*
> diye bakılır. **Çözüm:** `cp2_harvest.py --skip-first N` — havuz sırasındaki ilk N uygun kalemi
> atlar, N = önceki turun künyesindeki `denenen`. Taze dizinde koşar (provenans korunur, künyeye
> `skip_first` yazılır), sıra tam bıraktığı yerden devam eder. Havuz biterse **üretimden önce**
> çöker (tuzak 6.2 ilkesi).

## 10. ✅ HASAT KAPANDI — 16:47 → 20:09 (3,4 saat), iki tipte de kapı geçildi

```
taşıyıcı  llama.cpp 10223 (11924d4c1) · q35-4b-q4_k_m.gguf
          sha256 214826aa… · Q4_K_M · KV q8_0 · flash_attn · -np 64 · ctx_slot 8192
kart      NVIDIA A100-SXM4-40GB (gpu_gercek — etiket "A100" değil, tuzak 6.7)
rejim     düşünce 1024 + cevap 512 · seed 3407 · max_chunk_chars 900   (ADR-0043)
```

| tip | denenen | kabul (regex) | oran | kararlı s/üretim | zorunlu kapatma | kapı |
| :--- | --: | --: | --: | --: | :--- | :--- |
| m2 | 3.813 | **1.205** | %31,6 | **1,43** | 3.810/3.813 | ✅ geçildi |
| m2b | 3.813 | **708** | %18,6 | **1,59** | **3.813/3.813** | ✅ geçildi |

**Kapı damgası bu kez hak edilmiş:** ADR-0050'nin düzelttiği sıra sayesinde kapı `--limit`ten
**önce** değerlendirildi. Sabahki koşuda aynı damga hak edilmeden basılabiliyordu.

**Tahmin tam isabet.** ADR-0047 m.3'ün eşiği *"tahminin iki katı"* kuralıyla konmuştu; tahmin
**1,44 s/üretim**, m2'nin fiili kararlı hızı **1,43**. Sabahki `-np 32` turunun 2,9'a çıkması
taşıyıcının değil, slot sayısı + yanlı tahmin edicinin işiydi (ikisi de düzeltildi).

**Birleştirme (`cp2c_birlestir.py`):**

```
m2   cp2c-64 1.205 + cp2c 21 yeni  = 1.226 tekil   (47 yinelenen atıldı)
m2b  cp2c-64   708 + cp2c 10 yeni  =   718 tekil   (35 yinelenen atıldı)
                                     ─────────────
                          TOPLAM     1.944 aday    · yarım satır 0
```

> ### ✅ §5'in "kalıcı iz" endişesi GERÇEKLEŞMEDİ
> Durdurulan ikinci iş (`ap-5d1ss…`, 16:52-17:05) aynı dosyaya yazıyordu; çıktıda **ne yinelenen
> id ne yarım satır** çıktı — `cp2c-64/cp2c_m2.jsonl` 1.205 satır ve hepsi tekil, künyedeki
> `kabul` sayısıyla **birebir**. Modal volume'un commit semantiği durdurulan konteynerin
> yazımlarını taşımamış. **Yine de onarım adımı boşa değil:** iki dizin arasındaki **82 gerçek
> çakışmayı** o yakaladı (havuz sırası deterministik olduğu için `/cp2c`'nin 113 kaleminin
> 82'si yeni turda yeniden üretilmişti — tuzak **6.11**'in kanıtı).

## Doğan karar ve tuzak

- [**ADR-0050**](../../adr/0050-verim-kapisi-tahmin-edici-duzeltmesi.md) — verim kapısının tahmin
  edicisi düzeltildi, **eşik 2,88 aynı**; ADR-0047 m.3'ü **tadil eder** (m.3'ün metnine
  dokunulmadı, yanına not düşüldü).
- Yeni yürütme tuzağı **6.9** — *"ön-kayıtlı bir kapıyı kümülatif ortalamayla beslemek"*
  ([`yurutme-tuzaklari.md`](../yurutme-tuzaklari.md)). **6.8**'in kod tarafındaki kardeşi: 6.8
  *insanın* ara çıktıya bakıp koşu iptal etmesiydi, 6.9 *kapının* aynı yanlı sayıyla otomatik
  karar vermesi.

---

## 11. ✅ KABUL ZİNCİRİ KAPANDI — **362 temiz negatif**, hedefin yarısı · $5,11

```
        regex   →  mini      →  teyit      →  kör damga
m2      1226      430 (%35,1)   295 (%68,6)   272        · mini $0,147 · teyit $0,880
m2b      718      305 (%42,5)    90 (%29,5)    90        · mini $0,154 · teyit $1,079
                                            ──────
                                TOPLAM       362        · kör damga (1944 kalem) $2,849
                                                        · HAKEM TOPLAM $5,11
```

Dosya: `outputs/eval/cp2c-kabul/kabul_huni.json` · zincir `scripts/cp2c_kabul.sh` (tasarım B,
ADR-0049 m.5) · ön-filtre gpt-4o-mini · teyit + kör damga gpt-4o · `LLM_GATEWAY=openai` pinli.

**Ön-kayıtlı hedef 750'ye karşı %48.** İnsanın onayladığı yeniden-açma çizgisi (550) de kırıldı
→ ek tur koşuldu (§12).

### ⚠️ Nerede kaybettik — huni ADR-0049'un varsaydığından **iki kat** dar

ADR-0049 m.5'in projeksiyonu ~%50'lik tek bir teyit süzgeci varsayıyordu; ölçülen iki katmanlı
daralma çok daha sert, **ve mod başına ayrışıyor**:

| | m2 | m2b |
| :--- | ---: | ---: |
| regex → mini FABRICATE | %35,1 | %42,5 |
| mini → **teyit** FABRICATE | **%68,6** | **%29,5** |
| toplam temiz / regex adayı | %22,2 | %12,5 |
| **temiz / ÜRETİM** (kapasite planlaması için tek doğru sayı) | **%7,13** | **%2,36** |

Ayrışmanın kaynağı teyit katmanının **geçersiz** alt kümedeki davranışı:

| teyit FABRICATE | geçerli tuzakta | geçersiz tuzakta | toplam |
| :--- | ---: | ---: | ---: |
| m2 | 236/274 (%86) | 59/156 (%38) | 295/430 |
| m2b | 82/93 (%88) | **8/212 (%4)** | 90/305 |

**Geçerli tuzaklarda iki mod da ~%87** — teyit katmanı orada tutarlı. Fark yalnız geçersiz
kolonunda: m2'de mini'nin "kaynak cevaplıyor" dediklerinin %38'i yine de uydurma çıkıyor,
m2b'de %4. Yani m2b'de mini'nin yanlış-pozitifleri gpt-4o tarafından toptan eleniyor.

### ⭐ ADR-0048 LEHİNE KANIT — teyit ile kör damga güçlü örtüşüyor

Kör damga (cevaba **kör**, kalem düzeyinde) havuz genelinde:

| | havuz geneli geçerlilik | **teyitten geçmiş uydurmalarda** |
| :--- | ---: | ---: |
| m2 | 1012/1226 = **%82,5** | 272/295 = **%92,2** |
| m2b | 571/718 = **%79,5** | 90/90 = **%100** |

Yani "bu cevap uydurma" (cevaba bakan yargı) ile "bu tuzak geçerli" (cevaba kör yargı) **bağımsız
değil, uyumlu**. Mekanizma açık: kaynak soruyu gerçekten cevaplıyorsa modelin cevabı zaten
uydurma olmaz, dolayısıyla teyitten geçen küme geçerli tuzaklar bakımından **zenginleşmiş**
oluyor. Bu, ADR-0048'in kör damgayı otorite ilan etme kararını zayıflatmıyor — tersine, iki
bağımsız ölçümün aynı yöne bakması damganın gürültü değil sinyal ölçtüğünü gösteriyor.

⚠️ Karşı okuma da kayda geçsin: örtüşme **aynı hakem ailesinin** (gpt-4o) iki çağrısı arasında
ölçüldü, bağımsız aile değil. Öz-tutarlılık ile doğruluk burada ayrıştırılamaz.

### Planlama dersi

**Kapasite planı `regex kabul` üzerinden yapılamaz.** Bu turda 1.944 aday "hedefin %26 altındayız"
gibi görünüyordu; gerçek sayı 362, yani hedefin **%52 altında**. Aday sayısı hakem huninin
girdisidir, çıktısı değil; planlama birimi **temiz negatif / üretim** olmalı (m2 %7,13 ·
m2b %2,36). Bu oran ancak tam bir zincir koştuktan sonra bilinebildiği için, ADR-0047'nin
"`--limit` ile koş, verimi ölç" kararı doğru çıktı — ama ölçülmesi gereken verim hasat verimi
değil, **zincir sonu verimi**ymiş.

---

## 12. Ek tur — insan kararı **A** (2026-08-02 21:44)

Sunulan üç şık ve elenme gerekçeleri:

| # | şık | elendi mi | gerekçe |
| :-: | :--- | :-: | :--- |
| **A** | ek hasat turu koş | ✅ **seçildi** | ~$12, ~3 sa; ORPO adımını 35'ten ~70'e çıkarır |
| B | 362 ile devam et | ❌ | 362 → **35 adım**; ADR-0047'nin reddettiği 29-adım bölgesine bitişik. `τ_a` öğrenmezse CP3 ölçülemez olur, ARA KAPI'nın 1. gözlemi anlamsızlaşır |
| C | `grad-accum` 64→32 ile adımı ikiye katla | ❌ | bedava, ama efektif batch yarıya iner → `τ_g`'nin eğitim rejimiyle eşleşmez (ADR-0031). "Kollar aynı reçeteyle eğitildi" iddiası düşer |

```
app        ap-NpNr0GD8A1xO0Ywnrbz1nk  ·  fc-01KZ1WN4FVKA6JFP9TXGBWKQ81
başlangıç  2026-08-02 21:44
çıktı      hukuk-data:/cp2c-ek1/       ← AYRI dizin (provenans; birleştirme cp2c_birlestir.py)
skip-first 3813/tip                    ← 1. turun `denenen` sayısı
limit      3750/tip = 7.500 üretim
taşıyıcı   gguf sha256 214826aaca724dc7… · Q4_K_M · -np 64 · A100-SXM4-40GB · seed 3407
           → 1. turla BİREBİR (ADR-0047 m.2 taşıyıcı kimliği korundu)
beklenti   m2 ~267 · m2b ~89 → toplam ~718 temiz ≈ 70 ORPO adımı   ⚠️TAHMİN
```

**Boyut seçiminin gerekçesi.** 3.000/tip tam 551'e denk geliyordu — sıfır pay. Bu turda her
tahmin tutarlı biçimde iyimser çıktığı için (630 → 385 → 308 → gerçek 362) pay bırakıldı;
3.750 ayrıca 1. turun aynısı olduğu için künye ve provenans tek kalıp kalıyor.

### 🔴 DÖRDÜNCÜ EKSİK KÖPRÜ — `--skip-first` Modal tarafına hiç geçmemişti

`scripts/cp2_harvest.py`'ye `--skip-first` bu sabah eklenmişti (§9, tuzak 6.11), ama
`modal_train.py`'de **ne `spawn_cp2c` imzasında ne `harvest_cp2` komut kurulumunda** vardı.
Argüman kabul edilir, sessizce yok sayılır ve ek tur **1. turun ürettiği kalemleri baştan
üretirdi** — 3 saatlik GPU, tamamı yinelenen. §2/§7'nin aynı sınıfı: *köprünün ucu eksik.*

Onarım üç noktada: `spawn_cp2c(skip_first=0)` → `harvest_cp2(skip_first=0)` → `cmd +=
["--skip-first", …]`, artı künyeye `uretim_butcesi.skip_first` (provenans).

**Kanıt — logdan, koşu başladıktan sonra:**

```
[cp2] tip=m2 · mod=oracle · havuz=19284 · seed 3407 · devam=0 kayıt
[cp2] --skip-first 3813 → sıra 3813. kalemden başlıyor
[cp2] 15471 uygun kalem · eş zamanlılık=64        ← 19284 − 3813, tam
```

Havuz **tükenmedi**: 1. tur `--limit 3750` ile durdurulmuştu, her modda ~15.400 kalem el
değmemiş. Aynı seed → aynı karışım sırası → 1. turla çakışma yok.

**Genel ders (üç kez tekrarlandı, artık kalıp):** bu hatta bir bayrak *script'e* eklendiğinde iş
bitmiyor; **çağrı zinciri uçtan uca izlenmeden** ekleme tamamlanmış sayılmaz. Üçü de aynı
sessiz-yanlışlık sınıfı: hata vermez, yanlış sayı üretir.

---

## 13. ✅ EK TUR KAPANDI — 21:44 → **00:53** (3,15 sa), iki tipte de kapı geçildi

```
                1. TUR              EK TUR             fark
m2   denenen    3.813               3.813              —
     kabul      1.205 (%31,6)       1.192 (%31,3)      −0,3 puan
     kararlı    1,43 s/üretim       1,37 s/üretim      %4 hızlı
     kapatma    3.810/3.813         3.811/3.813        —
m2b  denenen    3.813               3.813              —
     kabul        708 (%18,6)         731 (%19,2)      +0,6 puan
     kararlı    1,59 s/üretim       1,54 s/üretim      %3 hızlı
     kapatma    3.813/3.813         3.813/3.813        —
kapı            geçildi             geçildi
```

Taşıyıcı **birebir** korundu: `gguf sha256 214826aa…` · Q4_K_M · `-np 64` ·
`A100-SXM4-40GB` · seed 3407 · künyede `uretim_butcesi.skip_first: 3813`.

### ⭐ `--skip-first` DOĞRULANDI — sıfır çakışma

Üç dizin birleştirildiğinde (`cp2c-ek1` + `cp2c-64` + `cp2c`):

```
m2   1192 yeni + 1205 yeni + 21 yeni  = 2.418 tekil  · 47 yinelenen atıldı
m2b   731 yeni +  708 yeni + 10 yeni  = 1.449 tekil  · 35 yinelenen atıldı
                                        ─────────────
                                        3.867 tekil  · yarım satır 0
```

**Ek turun 1.923 kaydının tamamı yeni** — atılan 82 yinelenen tümüyle 1. turun kendi iki
dizini arasındaki bilinen çakışma (§10). Yani tuzak **6.11**'in onarımı çalıştı: aynı seed ile
kurulan deterministik havuz sırasında 3.813 kalem atlanınca ek tur gerçekten **kaldığı yerden**
devam etti. Bu, bayrağın *"kabul edildi"* değil *"ölçüldü"* seviyesinde doğrulanmasıdır.

### Kabul zinciri ek turda **yalnız yeni kalemlere** koşuldu

1. turun 1.944 kalemi aynı hakemle, aynı istemle, `temperature 0`'da zaten yargılanmıştı;
yeniden ödemek ~**$2,26** boşa gider. Zincir `data/_ham_ve_ara/cp2c_ek1` (1.923 kalem) üzerine
koşuldu, çıktı `outputs/eval/cp2c-kabul-ek1/`. İki koşunun kabul dosyaları
`build_orpo_v3.py --rejected` çoklu-dosya arayüzünde birleşiyor; **id kümeleri ayrık** olduğu
için birleşim tek koşuya denk (yukarıdaki sıfır-çakışma ölçümü bunun kanıtı).

⚠️ Bu, kör damga önbelleğinin (`--onceki-onbellek`) tasarrufuna **ek**tir, onun yerine geçmez:
orada aynı kalemin damgası devralınıyor, burada aynı kalem zinciri hiç görmüyor.

---

## 14. OpenAI kredisi tükendi → **kapı OpenRouter'a alındı** (2026-08-03 09:37→09:43)

```
openai.RateLimitError: 429 — 'You have no credits remaining'
                              code: 'credit_balance_exhausted'
scripts/score_abstention.py:101 · m2 mini verdict'in İLK çağrısı
```

Ek turun kabul zinciri **başlayamadı**. Yanan para **$0**: hakemsiz dönüştürme adımı
(`m2_cp2c_detail.jsonl`) tamamlanmıştı, ilk hakem çağrısında düşüldü. Süreç durduruldu,
kilit dosyası yok, yarım çıktı yok.

**Kaybolan hiçbir şey yok:** ek turun 1.923 adayı diskte (`data/_ham_ve_ara/cp2c_ek1`),
Modal parası zaten harcanmıştı ve adaylar bozulmaz. 1. turun 362 temiz negatifi
`outputs/eval/cp2c-kabul/` altında duruyor.

**Gereken:** ~$5 hakem bütçesi (mini 1.923 ≈ $0,30 · teyit ~720 ≈ $1,90 · kör damga
1.923 ≈ $2,80). Modal cüzdanı ayrı ve dolu ($18,15) — bu bir GPU sorunu değil.

### Beklerken bedelsiz doğrulandı — CP3'ün çift kurma adımı hazır

`build_orpo_v3.py` 1. turun 362'siyle prova koşuldu (çıktı geçici dizine):

```
abstain_pairs 360 · grounding_replay 72 · total 432 · train 420 / validation 12
skipped: dev_excluded 2 · no_chosen 0 · abstained_no_contrast 0
karışım: m2 272 · m2b 88      hasat kaynağı: cp2c-64 357 · cp2c 3
```

`no_chosen: 0` — her m2 kaleminin eşi havuzda bulundu, ADR-0051'in m2b şablonu 88 kalemin
tamamında çalıştı. Çoklu `--rejected` arayüzü doğrulandı; ek turun dosyaları geldiğinde
dört dosya birlikte verilecek.

⚠️ Bu prova **B seçeneğinin bedelini de kesinleştiriyor**: 362 temiz → 432 kalem → `grad-accum
64` ile **~30 ORPO adımı**, yani ADR-0047'nin reddettiği 29-adım bölgesinin tam içi. Kredi
beklemek, azıyla eğitmekten ucuz.

### ✅ Çözüm — kapı değiştirildi, **sağlayıcı pinlendi**

İnsan OpenRouter bakiyesini gösterdi ($4,43). `llm_client.py` OpenRouter'ı zaten destekliyordu
ve anahtar `.env`'deydi; kod değişikliği gerekmedi. Ama ilk sınamada **sessiz bir sapma** çıktı:

```
LLM_GATEWAY=openrouter            gpt-4o-mini → sağlayıcı OpenAI
                                  gpt-4o      → sağlayıcı **Azure**     ← 1. tur OpenAI'ydi
LLM_GATEWAY=openrouter
LLM_PROVIDER_ORDER=OpenAI         gpt-4o-mini → OpenAI
                                  gpt-4o      → OpenAI · seen_providers ['OpenAI']
```

OpenRouter'ın yönlendirmesi pinlenmezse aynı model adı farklı servis yığınından gelir. Pin
mekanizması `llm_client.request_kwargs` içinde zaten vardı (`provider.order` +
`allow_fallbacks: false`), yalnız kullanılmamıştı. Ek tur **pinli** koşuyor.

⚠️ **Kayda geçen sapma:** 1. tur doğrudan OpenAI kapısından, ek tur OpenRouter üzerinden
koşuldu. Model ve servis eden kurum aynı; değişen **faturalama yolu**. Bu bir küratörlük
etiketi olduğu için (raporlanan metrik değil) risk sınırlı, ama huni oranları iki tur arasında
karşılaştırılırken bu fark anılmalıdır. `seen_providers` her koşuda künyeye yazılıyor.

### 💰 Kör damga daralttıldı — ölçülen bir israf kesildi

Bütçe $4,43, zincir tahmini $5,00'dı. Açık, gerçek bir israf kesilerek kapatıldı:

**Kabul ölçütü `teyit ∧ kör`** — teyitten düşen kalemin kör damgası **hiçbir yerde
kullanılmıyor**. Oysa `valid_trap_cache.py` havuzun tamamını damgalıyordu. 1. turda ölçülen
bedel: **1.944 damga, gereken 385** → $2,85'in ~**$2,25'i boşa**.

`--sadece-teyit <koşu-dizini>` eklendi (zincirde varsayılan **açık**, `KOR_TAM=1` ile eski
davranış). Ek turun tahmini:

```
mini   1.923 kalem   $0,30
teyit  ~720 kalem    $1,90
kör    ~360 kalem    $0,55      ← 1.923 değil
                     ─────
                     ~$2,75
```

**Bedeli ve nereye yazıldığı:** ek turun *havuz geneli* geçerlilik oranı ölçülmez, yalnız
kabul adaylarınınki. O oran 1. turda **n=1.944** ile zaten ölçüldü (m2 %82,5 · m2b %79,5) ve
§11'de duruyor. Künyeye `sadece_teyitten_gecenler` alanı yazılıyor ki oranın **neden yok**
olduğu sonradan cevapsız kalmasın.

---

## 15. ✅ CP2-c KAPANDI — **728 temiz negatif**, hedefin %97'si

```
              regex   →  mini        →  teyit       →  kör damga
1. tur  m2     1226      430 (%35,1)    295 (%68,6)    272
        m2b     718      305 (%42,5)     90 (%29,5)     90    = 362   $5,11
ek tur  m2     1192      401 (%33,6)    293 (%73,1)    266
        m2b     731      326 (%44,6)    105 (%32,2)    100    = 366   $2,86
                                                     ────────────────
                                                       TOPLAM  728    $7,97
```

Dosyalar: `outputs/eval/cp2c-kabul/kabul_huni.json` · `outputs/eval/cp2c-kabul-ek1/kabul_huni.json`

### İki turun huni oranları **örtüşüyor** — kapı değişikliği sayıyı kaydırmadı

Ek tur farklı bir kapıdan (OpenRouter, sağlayıcı `OpenAI` pinli) koştu. Kaygı, huninin
kaymasıydı; ölçüm aksini söylüyor:

| aşama | 1. tur | ek tur | fark |
| :--- | ---: | ---: | ---: |
| m2 mini kabul | %35,1 | %33,6 | −1,5 puan |
| m2b mini kabul | %42,5 | %44,6 | +2,1 puan |
| m2 kör damga geçerliliği (teyit sonrası) | %92,2 | %90,8 | −1,4 puan |
| m2b kör damga geçerliliği (teyit sonrası) | %100 | %95,2 | −4,8 puan |
| mini maliyeti (m2) | $0,147 | $0,142 | — |

Teyit adımında m2b lehine bir kayma var (%29,5 → %32,2) ama yön ve büyüklük, iki turun
**farklı havuz dilimlerinden** gelmesiyle de açıklanabilir (aynı seed, farklı sıra aralığı).
Kapıya atfedilemez; `judge_providers` her iki koşuda tek kaynak (`['OpenAI']`).

### Kör damga daraltmasının ölçülen bedeli

Ek turda damga **398** kaleme koşuldu (1.923 yerine): **$0,570**. 1. turda aynı iş 1.944 kalem
için $2,849'du. Kesilen israf ~**$2,28**, ölçülmüş. Kaybedilen bilgi: ek turun *havuz geneli*
geçerlilik oranı (1. turda n=1.944 ile ölçüldü, §11).

### CP3'ün girdisi — 726 çift, **65 ORPO adımı**

```
abstain_pairs 726 · grounding_replay 145 · total 871 · train 845 / validation 26
skipped: dev_excluded 2 · no_chosen 0 · abstained_no_contrast 0
mod karışımı:    m2 538 · m2b 188
hasat kaynağı:   cp2c-64 357 · cp2c-ek1 366 · cp2c 3
```

**65 adım** (845 ÷ grad-accum 64 = 13 adım/epoch × 5 epoch) — ADR-0047'nin ön-kayıtlı ~73
adımının **%89'u**, reddettiği 29-adım bölgesinden uzak. `no_chosen: 0`: her m2 kalemi havuzda
eşini buldu, ADR-0051'in m2b şablonu 188 kalemin tamamında çalıştı.

### 🔴 Bir tuzak daha — `sprint2.md`'deki hazır komutta yol yereldi

Belgede aylardır *"ateşe hazır"* diye duran CP3 komutu `--data data/train/orpo_abstain_cp2c`
diyordu; oysa `train_orpo` **konteyner yolu** bekliyor (`/data/<set>`, tuzak 3.6 — `hukuk-data`
volume'ü `/data`'ya bağlanır). Veri önce `modal volume put` ile yüklenmeliydi. Yakalandığı yer:
komut ateşlenmeden önce `spawn_orpo`/`train_orpo` imzalarının okunması. Yakalanmasaydı GPU
ayrıldıktan sonra patlardı. Komut düzeltildi ve veri `hukuk-data:/orpo_abstain_cp2c` altına
yüklendi.

*Ders (tuzak 6.12'nin kardeşi): "hazır komut" bloğu, **koşulmadığı sürece doğrulanmamış**
koddur. Belgede durması onu sınanmış yapmaz.*

---

## 16. ✅ CP3 · 3a — `τ_abstention` EĞİTİLDİ (2026-08-03 10:49 → 11:26, 36,5 dk)

```
app        ap-80DlzMmkEwTjerjwJlh1sO · fc-01KZ39K0CWEPPJRE41GK7S2V8N · A100-SXM4-40GB
veri       /data/orpo_abstain_cp2c · 845 train / 26 validation
rejim      5 epoch · lr 1e-5 (cosine) · beta 0.1 · grad-accum 64 · batch 1
           --fresh-adapter · --bf16-base · --lora-dropout 0.05 · 11 modül
adım       **70** (845÷64=13,2 → 14/epoch × 5) — ön-kayıtlı ~73'ün %96'sı
çıktı      hukuk-outputs:/ta_v1 → outputs/ta_v1
```

Unsloth bandı: `Trainable parameters = 29,908,992 of 4,569,174,528 (0.65% trained)` — ön-kayıtlı
sayı **birebir**.

### ⛔ Kapı log satırından değil ARTEFAKTTAN kuruldu

`modal app logs` kayan pencere döndürüyor; parametre bandı ilk denemede görünmedi. Kapı bunun
yerine üretilen dosya üzerinden kuruldu — **niyeti değil ürünü doğrulayan**, daha güçlü bir test:

| | `τ_g` (referans) | `τ_a` | |
| :--- | ---: | ---: | :-: |
| tensör | 448 | 448 | ✅ |
| parametre | 29.908.992 | 29.908.992 | ✅ |
| r / alpha / dropout | 16 / 32 / 0,05 | 16 / 32 / 0,05 | ✅ |
| target_modules | 11 | 11 | ✅ |

*Ders: bir kapının ölçütü mümkünse **artefakt** olmalı, log satırı değil. Log kaybolur, kayar,
tamponlanır; dosya kalır ve tekrar ölçülebilir.*

### ⭐⭐ ADR-0036'NIN GEREKÇESİ ÖLÇÜLDÜ — 8,87× norm asimetrisi

```
‖τ_grounding‖  = 10,4722      (1.083 adım @ lr 1e-4)
‖τ_abstention‖ =  1,1806      (   70 adım @ lr 1e-5)
                  ──────
oran            8,87×
```

ADR-0036 bu asimetriyi **öngörerek** yazılmıştı; şimdi gerçek kollarda ölçüldü. TIES'in
işaret-seçimi ve ayrık-ortalaması **kütle ağırlıklı** olduğundan, norm dengelenmezse `τ_a` tam
da iki becerinin çatıştığı parametrelerde silinir — ve sonuç *"çekinme korunmadı"* diye
okunurdu. Bu bir **ölçek artefaktı** olurdu, bulgu değil. Ana sonuç norm-dengeli koşar; ham
TIES ablasyon olarak raporlanır (ADR-0036).

### Eğitim eğrisi — çekinme öğrenilirken cevaplama unutulmadı

| epoch | 0,38 | 1,08 | 2,15 | 3,61 | 4,30 | **5 (eval)** |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| `loss` | 2,640 | 2,372 | 2,000 | 1,782 | 1,760 | **1,773** |
| `nll_loss` (forget-vekili) | 2,434 | 2,168 | 1,849 | 1,667 | 1,648 | **1,636** |
| `rewards/margins` | −0,1035 | −0,0955 | −0,0536 | −0,0323 | −0,0222 | **−0,0326** |
| `log_odds_chosen` | −1,573 | −1,476 | −0,949 | −0,614 | −0,476 | **−0,626** |
| `rewards/accuracies` | 0,175 | 0,160 | 0,190 | 0,147 | 0,201 | **0,143** |

`nll_loss` **baştan sona düştü** (2,434 → 1,636): kol çekinmeyi öğrenirken grounding'i
kaybetmedi — %20 replay'in görevi buydu ve yaptı.

### ⚠️ NOT DÜŞÜLECEK BULGU — tercih sıralaması hiç dönmedi

`rewards/accuracies` 5 epoch boyunca **0,14-0,20 bandında kaldı**, 0,5'i hiç geçmedi. Yani
eğitim sonunda model hâlâ örneklerin ~%85'inde **kendi akıcı uydurmasına**, kalıplı red
cümlesinden yüksek olasılık veriyor (`logps` −0,95 ↔ −1,28). Marj kapandı (−0,104 → −0,033,
%68) ama işaret değiştirmedi.

İki okuma mümkün ve **3c bunları ayırır**:
1. **Yetersiz eğitim** — 70 adım ve lr 1e-5, sıralamayı çevirmeye yetmedi.
2. **Metrik yanıltıcı** — `accuracies` token-olasılığı sıralamasını ölçüyor; ORPO'nun
   hedeflediği davranış (üretimde çekinme) düşük-olasılıklı bir cümleyi *seçmek* değil,
   uydurmanın olasılığını **bastırmak**. `log_odds_chosen` −1,573 → −0,626 (%60 iyileşme)
   tam da bunu gösteriyor olabilir.

⚠️ **Ön-kayıt niteliğinde:** ARA KAPI'nın 1. gözlemi (M2 Rej ≥ 0,923) **düşerse**, bu tablo
"kol öğrenmedi mi, yoksa yeterince mi öğrenmedi" sorusunun kanıtı olacak — ve okuma (1) ise
çare rejimdir (epoch/lr), veri değil. Sayı görülmeden bu yorum yapılmayacak.
