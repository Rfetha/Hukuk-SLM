# ADR-0073 — M5'in ölçüm rejimine **DRY** eklendi · kapsam **yalnız M5**

**Tarih:** 2026-09-07 · **Statü:** ✅ yürürlükte · **Karar:** insan
**Bağlı:** [ADR-0040](0040-dusunce-modu-olculecek-on-kayitli-kural.md) (geçerlilik kapısı %5) ·
[ADR-0039](0039-kapi-6-parametrik-sizinti.md) (M5 çıpası **base**, rakip değil) ·
[ADR-0057](0057-harness-rekabet-kapisi-esit-sinav.md) (eşit sınav) ·
[ADR-0050](0050-verim-kapisi-tahmin-edici-duzeltmesi.md) (**alet düzeltilir, eşik oynatılmaz**) ·
[ADR-0064](0064-v1-kapisi-uc-maddeli-on-kayit.md) madde (3) ·
[#42](../record/research_log/2026-07-29-cp0-dusunce-modu-sonlanmama.md)

## Bağlam — kapı kaldı ve reçetesi uymadı

`tgta_v1`'in M5 koşusu (2026-09-07, şarjda, 80/80) **geçerlilik kapısından kaldı**:
kesik **5/80 = %6,2 > %5**, `EXIT=2`. **Hakem çağrılmadı** — kapı parayı korudu.

Beş kalem **gözle okundu** ve **deterministik** bir kuyruk-tekrarı dedektörüyle bağımsız
doğrulandı; ikisi **aynı hükmü** verdi:

| sınıf | kalem | kanıt |
| :--- | :--- | :--- |
| bütçe kesilmesi | 27 · 43 | 27: düşünce 1536'nın tamamını yaktı, cevap **3 karakter** (`"Kat"`) |
| 🚨 **yozlaşmış tekrar** | 28 · 74 · 54 | ibare **×21** · **×19** · **×82** |

ADR-0040'ın reçetesi *"MAXTOK büyütülüp tekrar koşulur"* **üç kalemde ölçülmüş biçimde
etkisizdir**: `temperature=0` açgözlü kod çözmede döngüye girmiş model **matematiksel olarak
çıkamaz** — büyük bütçe **daha uzun bir döngü** üretir. #42 aynı sınıfta bütçeyi **8× artırmış
(4096 → 32768) ve hiçbir şey değişmemişti**.

⇒ Ön-kayıtlı kural, kapsamadığı bir kusur sınıfına çarptı. Karar **insana** taşındı.

## Ölçüm — ablasyon, **$0, hakem yok**

5 suçlu kalem · aynı GGUF · aynı seed 3407 · aynı bütçe 1536 · aynı istem ·
**değişen yalnız sunucunun örnekleme bayrakları**.
✅ **Kontrol kapısı: 5/5 BAYT-BAYT aynı** — alt küme resmî koşuyu birebir üretti, dolayısıyla
fark **kola** aittir.

| kol | kesik | döngü | ort token |
| :--- | ---: | ---: | ---: |
| `kontrol` *(bugünkü rejim)* | **5/5** | **3** | 1843 |
| **`dry`** `0.8 / 1.75 / 2` | **0/5** | **0** | 1553 |
| `rep11` `--repeat-penalty 1.1` | 1/5 | 0 | 1508 |

## Karar

**1. M5'in ölçüm rejimi `--dry-multiplier 0.8 --dry-base 1.75 --dry-allowed-length 2` içerir.**
Kapsam **yalnız M5**. `m1 · m4 · m2 · m2b · m3 · h1 · h2b` **değişmez**.

**2. İki kol da (bizim + base) aynı bayraklarla yeniden koşulur** — ADR-0057.

**3. ⛔ Kapı eşiği OYNAMADI.** Değişen **alet**tir. ADR-0050'nin kendi hükmü:
*"sonucu gördükten sonra **EŞİK değil ALET** düzeltilir."* %5 eşiği yerinde; `M5 ≤ base`
kuralı (ADR-0039) yerinde; δ yerinde.

### Neden kapsam **yalnız M5** — teknik zorunluluk, tercih değil

**DRY bir `llama.cpp` örnekleyicisidir; Gemini'ye uygulanamaz.** Rakip içeren hiçbir modda
**eşitlenemez** ⇒ oralarda kalıcı olarak kapalı kalmak zorundadır (aksi hâlde biz cezalı,
rakip cezasız koşar ve ADR-0057 bozulur).

**M5 rakip içermez.** ADR-0039 §2 çıpayı açıkça **base**'e bağlamış ve **rakip çıpasını
REDDETMİŞTİ** (*"modeli aldığımız noktadan kötüye götürmemeliyiz"*). Base de bizim gibi yerel
`llama.cpp` ⇒ DRY **iki kola da eşit** uygulanabilir. Kapsam sınırı bu asimetriden doğuyor.

### Neden DRY, `repeat_penalty` değil
```
ceza = çarpan × taban^(eşleşen_dizi_uzunluğu − serbest_uzunluk) = 0,8 × 1,75^(n−2)
```
Tekrarlanan **dizinin** uzunluğuyla üstel büyür ⇒ **2 token'a kadar tekrar serbest**.
Hukuk metninde *"madde"*, *"kanun"* ve kanun numaraları **meşru olarak** tekrarlar ve ceza
almaz; 20+ token'lık döngü ezilir. `repeat_penalty` yakın penceredeki **her** token'ı
bağlamına bakmadan cezalandırır — bu alanda yan hasarlıdır, ve ölçümde de **1 kesik bıraktı**.

⭐ **Determinizm korunur.** İki ceza da logit'i **seçimden önce** değiştirir ⇒ `temperature=0`
bozulmaz, koşu seed ile yeniden üretilebilir kalır. #42'nin yarısını kurtaran `temp 0.6` bunu
**bozardı**; ucuz kaldıraç aynı zamanda **metodolojik olarak temiz** olandır.

## 🚨 Kabul edilen bedel — sayıdan ayrılamaz şerh

**DRY modeli DOĞRU yapmadı, AKICI yaptı.** Kör modda cevaplar artık tam ve akıcı — ve
**yanlış**: İş K. **31** → *"35. ve 36. Maddeler"* · İİK **79/a** → *"110. Madde"* ·
KMK **33** → *"Kanun No 633, 10. Madde"* · TBK **230** → *"6502 Sayılı Tüketici Kanunu"*.
M5'in ölçmek için var olduğu şey **tam olarak budur**.

⇒ **Döngü kalemi ile akıcı-yanlış kalem hakemden aynı notu almaz.** Dolayısıyla:
- 🚨 **DRY'li M5, DRY'siz M5 ile AYNI BİRİMDE DEĞİLDİR.** Eski M5 sayıları
  (`m5_base_th` · `m5_gem_th` · `m5_tg_v1_th`, cp09) **kıyaslanamaz** ve kıyas **kurulmaz**.
- ✅ Bugün koşulan **iki kol aynı birimdedir** (ikisi de DRY, aynı seed/bütçe/istem) ⇒
  madde (3)'ün hükmü **bu iki kol arasında** kurulur.
- ⚠️ M5'in **mutlak** değeri yayımlanırken *"DRY'li rejim"* damgası **zorunlu**.

## Reddedilenler

- **DRY'yi tüm yerel modlara** — REDDEDİLDİ: rakipler DRY alamaz ⇒ M1/h1'de **eşit sınav
  bozulur** (ADR-0057); manşet kütle (%80,1) ve dört rakip çıpası yeniden koşulur (~$1,5+) ve
  **yine eşitlenemez**.
- **MAXTOK'u büyütüp tekrar koş** — REDDEDİLDİ: üç kalemde **ölçülmüş biçimde etkisiz**
  (#42: 8× artış, sıfır değişim). GPU yakar, oran düşmez.
- **`temperature > 0`** — REDDEDİLDİ: determinizmi ve seed ile yeniden üretilebilirliği
  bozar; DRY aynı işi `temp=0`'da yapıyor.
- **M5'i *"bu kipte ölçülemiyor"* diye raporla** (#42 emsali) — REDDEDİLDİ: dürüst ama
  kapı maddesi (3)'ü **sayısız** bırakır ⇒ `v1.0` hükmü eksik kalır. Ölçülebilir bir yol
  **$0,08'e** varken ölçmemek tercih edilmedi.
- **`repeat_penalty 1.1`** — REDDEDİLDİ: hukuk metninde bağlamsız token cezası yan hasarlı,
  ve ölçümde **1 kesik bıraktı** (DRY 0).

## Ön-kayıt şerhi

Bu ADR, DRY'li koşuların **üretimi sürerken** ve **hiçbir M5 puanı görülmeden** yazıldı.
Hüküm kuralı yeni değil — ADR-0039'un `M5 ≤ base` kuralı **değiştirilmedi**; bu ADR yalnız
**hangi aletle ölçüleceğini** söyler.
