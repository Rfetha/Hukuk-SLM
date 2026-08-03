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

### K1. Gömme modeli (embedder)

Türkçe hukuk metni · **CPU'da** koşacak (harness GPU'ya girmez — bu, sığar/sığmaz
farkı). Adaylar ölçülmeli, seçilmemeli:

| aday | not |
| :--- | :--- |
| `intfloat/multilingual-e5-*` | güçlü çok-dilli taban, yaygın |
| `BAAI/bge-m3` | uzun bağlam, çok-dilli |
| Türkçe-özel modeller | varsa ölçülür — "Türkçe" etiketi tek başına kanıt değil |

**Ölçüt:** DEV sorularında **recall@k** — altın madde ilk k içinde mi. Bu bedava
ölçülür (etiket zaten elimizde), model çağrısı gerekmez.

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
0) MODÜL-BAŞINA NORM        1 sa · $0   ← bedava, harness'tan bağımsız
1) RETRIEVER                indeks + recall@k ölçümü
2) ATIF DOĞRULAYICI         deterministik, hakem gerekmez
3) RED KAPISI               ADR-0038 katı
4) HARNESS AÇIK ÖLÇÜM       ⭐ gerçek ürün sayımız — hiç görülmedi
   → 🛑 DUR, harness açık/kapalı tabloyu insana sun
```

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
| **K1-K5** tasarım kararları | 🛑 **çözülecek** | ADR-0053+ |
| **0** modül-başına norm | ⏳ | `models/gguf/` + `outputs/eval/` |
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
