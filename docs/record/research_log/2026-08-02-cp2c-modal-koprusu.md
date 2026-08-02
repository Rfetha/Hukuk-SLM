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

## Doğan karar ve tuzak

- [**ADR-0050**](../../adr/0050-verim-kapisi-tahmin-edici-duzeltmesi.md) — verim kapısının tahmin
  edicisi düzeltildi, **eşik 2,88 aynı**; ADR-0047 m.3'ü **tadil eder** (m.3'ün metnine
  dokunulmadı, yanına not düşüldü).
- Yeni yürütme tuzağı **6.9** — *"ön-kayıtlı bir kapıyı kümülatif ortalamayla beslemek"*
  ([`yurutme-tuzaklari.md`](../yurutme-tuzaklari.md)). **6.8**'in kod tarafındaki kardeşi: 6.8
  *insanın* ara çıktıya bakıp koşu iptal etmesiydi, 6.9 *kapının* aynı yanlı sayıyla otomatik
  karar vermesi.
