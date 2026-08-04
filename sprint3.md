# Sprint 3 — HARNESS: modeli ürüne çevirmek

> **Bu belge icra dokümanıdır ve `/goal sprint3.md` ile otonom koşulur.**
>
> ### ⭐ HER KOŞUDAN ÖNCE OKU
> [`docs/record/yurutme-tuzaklari.md`](docs/record/yurutme-tuzaklari.md) — bu hattın hata sınıfı
> **çökme değil, sessiz yanlışlık**. Sprint 2 buraya **6.10 · 6.11 · 6.12**'yi ekledi.

---

## 🎯 HEDEF

```
koşul     : harness kuruldu (retriever + atıf doğrulayıcı + red kapısı) ve
            HARNESS AÇIK ölçüm yapıldı, harness kapalıyla yan yana raporlandı
🛑 DURMA  : kırmızı kapı · geçerlilik kapısı düşerse · bütçe aşımı
            · ⛔ tasarım kararları çözülmeden kod yazılmaz (aşağıda)
kapsam    : adım 0-4.  Graph-RAG, ajanlar, vatandaş kipi bu hedefin DIŞINDA
bedel     : GPU $0 (harness CPU'da) · hakem ~$1 · gömme modeli indirme
```

## Neden harness — karar gerekçesi (insan, 2026-08-03)

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

### K2. Chunk birimi

Korpus **40.496 madde**, doğal chunk = madde. Ama uzun maddeler var ve **eval-ayna
kuralı 900 karakter** kırpıyor (ADR-0011). Kırpma retriever'da da mı uygulanacak,
yoksa tam madde mi getirilecek — **karar gerektirir**, sessizce seçilmez.

### K3. Statik korpus mu, canlı API mi

`data/corpus/mevzuat_maddeler.jsonl` **29 Temmuz anlık görüntüsü**. Canlı
`bedesten` API'si güncelliği verir ama gecikme + erişilebilirlik getirir
(⚠️ **Türk IP gerekir**, yurtdışı/VPN engelli).

**Öneri:** statikle başla (ölçüm tekrarlanabilir olsun), canlı katmanı sonra ekle.

### K4. ⭐ HARNESS AÇIK ölçüm protokolü — en önemli karar

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
S3a) ÖN-PROB                $0 · ~1 gün ← ⭐ PLANIN TEMELİNİ SINAR, önce koşar
0) MODÜL-BAŞINA NORM        1 sa · $0   ← bedava, harness'tan bağımsız
1) RETRIEVER                indeks + recall@k ölçümü
2) ATIF DOĞRULAYICI         deterministik, hakem gerekmez
3) RED KAPISI               ADR-0038 katı
4) HARNESS AÇIK ÖLÇÜM       ⭐ gerçek ürün sayımız — hiç görülmedi
   → 🛑 DUR, harness açık/kapalı tabloyu insana sun
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

- **Adım başlarken:** 🟡 KOŞUYOR + ne koşuyor
- **Adım biterken:** ✅/🔴 · **fiili sayılar** · çıktı nerede · hangi kayıt
- **Karar insana gittiğinde:** aynı gün ADR + `research_log`

*Sohbette kalan bulgu, kaybolmuş bulgudur.*

## Durum tablosu

| adım | durum | çıktı |
| :--- | :--- | :--- |
| **K1** gömme modeli | ✅ **çözüldü** | `bge-m3` + BM25 hibriti (RRF) — research_log #49 |
| **K2-K5** tasarım kararları | 🛑 **çözülecek** | ADR-0053+ · ⚠️ K4'e S3a'dan yeni girdi var |
| **S3a** ön-prob (recall@k + bedesten) | ✅ **KAPANDI** 2026-08-04 | hibrit `recall@10` **0,875** · bedesten ✅ GEÇERLİ · `outputs/eval/s3a-on-prob/` · research_log #49 |
| **0** modül-başına norm | 🟡 **sırada** | `models/gguf/` + `outputs/eval/` |
| **1** retriever | ⏳ | `scripts/` + recall@k |
| **2** atıf doğrulayıcı | ⏳ | `scripts/` |
| **3** red kapısı | ⏳ | `scripts/` |
| **4** harness AÇIK ölçüm | ⏳ | 🛑 **DUR, insana sun** |

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
