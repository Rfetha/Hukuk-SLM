# ADR-0076 — **KAPI ↔ KALDIRAÇ** ayrımı ve araç katmanı (`v1`'e dahil)

**Tarih:** 2026-09-08
**Statü:** ✅ yürürlükte
**Karar:** insan
**Bağlı:** [ADR-0057](0057-harness-rekabet-kapisi-esit-sinav.md) (eşit sınav) ·
[ADR-0040](0040-kesiklik-kapisi.md) (kesiklik kapısı) ·
[ADR-0075](0075-v1-sft-kapanir-v2-sequential-rl.md) (`v1` SFT ile kapanır) ·
`hakhukuk/terazi.py` · `hakhukuk/servis.py`

## Bağlam

Bugünkü ürün akışı **tek atış ve sabit**:

```
soru → retriever (HER ZAMAN) → 10 madde → model → cevap → terazi (HER ZAMAN)
```

Model hiçbir şeye karar vermiyor: arayıp aramayacağına, tekrar arayacağına, bir maddenin
metnini okuyup okumayacağına.

## 🚨 Ölçüm, bu ADR'nin İLK GEREKÇESİNİ ÇÜRÜTTÜ — düzeltilerek bırakılıyor

Taslak şöyle diyordu: *"isabetsizlik 8/80 — model `TBK 214` ile `TBK 217`'yi yan yana
okuyabilseydi farkı görürdü."* **Ölçüldü ve yanlış çıktı** (2026-09-08,
`h1_tgta_v1_f02_nb_detail.jsonl` → `harness.altin_sirasi`):

| eksen | büyüklük | altın madde bağlamda mıydı | araç çözer mi |
| :--- | ---: | :--- | :--- |
| isabetsizlik | 8/80 | **8/8 EVET** — biri **1. sırada** | ❌ sorun erişim değil, **SEÇİM** |
| aşırı-red | 4/80 | **4/4 EVET** — üçü **1. sırada** | ❌ model bakıyor, kullanmıyor |
| uydurulmuş madde | **0**/114 | — | ❌ çözülecek sorun yok |
| **recall kaybı** | **4/80** | ❌ hiç gelmedi | ✅ `ara` **deneyebilir** — tek somut hedef |

⇒ **Araçların eval setindeki toplam hedefi 4 kalemdir** ve `ara`'nın onları bulacağı
**garanti değildir** (aynı retriever, aynı indeks, yalnız farklı sorgu).
İsabetsizlik ve aşırı-red **muhakeme** sorunlarıdır; çareleri eğitim (`B1` turu — atlandı,
ADR-0075) ya da RL (`v2`).

## Kararın dayandığı gerekçe — ve sınırı

**İnsan kararı 2026-09-08: beş araç da konur.** Gerekçe **eval kazancı değil, ürün
yeteneğidir** — eval seti *"soru → altın madde"* biçimindedir ve gerçek kullanımın
sorduğu şeyleri **ölçmez**: *"TBK 217 nedir"* · *"bu madde yürürlükte mi"* ·
*"İş Kanunu kaç numaralı"* · takip soruları.

⚠️ **Bu gerekçe ÖLÇÜLMEMİŞTİR ve öyle damgalanır.** Bu hatta spekülatif gerekçe daha önce
**iki kez** çürüdü (*"istem katmanı tavanı düşük"* · *"norm dengeleme şart"*). ⇒ Araç
katmanının kazancı **yayımlanan hiçbir sayıya eklenmez**; işe yarayıp yaramadığı ancak
gerçek kullanımda ya da yeni bir ölçüm birimiyle görülür.
⛔ Ve `v1.0` kapısı bu katman **olmadan** koşulur (m.4).

## Karar

### 1. İki sınıf ayrılır ve **karıştırılmaz**

| sınıf | ne | kim karar verir | örnek |
| :--- | :--- | :--- | :--- |
| 🔒 **KAPI** | güvenlik kontrolü | **hiç kimse** — koşulsuz çalışır | atıf doğrulama · mülga süzgeci · durum sınıflandırma · kesiklik damgası |
| 🔧 **KALDIRAÇ** | modelin gücünü artıran deterministik araç | **model** — çağırır ya da çağırmaz | `ara` · `madde_getir` · `madde_var_mi` · `kanun_bul` · `yururlukte_mi` |

🚨 **KAPI'lar TOOL YAPILAMAZ.** Bugünkü en güçlü sayı — **uydurulmuş madde 0/114**
(rakipler 1 · 4 · 4) — `terazi.siniflandir()`'in **her cevapta koşulsuz** çalışmasından gelir.
Tool'a çevrilirse model onu çağırmayı **unuttuğu an** garanti buharlaşır; ve model unutur.
⇒ KAPI'lar tool döngüsünün **DIŞINDA**, döngü bittikten **sonra** çalışır.

### 2. Araçlar **deterministiktir** — halüsinasyon üretemezler

| araç | döner | besleyen mevcut kod |
| :--- | :--- | :--- |
| `ara(sorgu, k)` | hibrit BM25+dense sonuç | `retriever.getir()` |
| `madde_getir(kanun_no, madde_no)` | tam madde metni | korpus indeksi |
| `madde_var_mi(kanun_no, madde_no)` | **var/yok** (tek bit) | `madde_anahtar.madde_anahtari` |
| `kanun_bul(ad)` | *"İş Kanunu"* → `4857` | korpus |
| `yururlukte_mi(kanun_no, madde_no)` | mülga mı | korpus `mulga` alanı |

⚠️ **Beş aracın ölçülmüş hedefi eşit DEĞİLDİR** ve bu ayrım korunur:

| araç | ölçülmüş hedef | not |
| :--- | :--- | :--- |
| `ara` | **4/80** recall kaybı | tek ölçülmüş hedef; başarısı **garanti değil** |
| `madde_getir` | ❌ yok | ürün yeteneği — *"TBK 217 nedir"* |
| `madde_var_mi` | ❌ yok — **uydurma zaten 0/114** | modelin kendini yazmadan önce denetlemesi; bizim kolda **boşta çalışır**, değeri `v2`'de belirir |
| `kanun_bul` | ❌ yok | isim→numara ezberden yapılmasın |
| `yururlukte_mi` | ❌ yok | mülga bilgisi zaten KAPI'da süzülüyor; bu araç **kullanıcıya söylemek** için |

⛔ *"`madde_var_mi` B1'i çözer"* cümlesi **KURULMAZ** — B1 vakalarında altın **zaten
bağlamdaydı** ve uydurulmuş madde sayımız **0/114**. Araç var olmayan bir maddeyi yakalar;
B1'de madde **gerçek**, sadece **yanlış**.

⚠️ Liste kapalı değildir: gerekçesi yazılmak şartıyla yeni deterministik araç eklenebilir.
⛔ Ama **hiçbir araç LLM çağırmaz** — araç katmanı deterministik kalır, yoksa hata kaynağı olur.

### 3. 🚨 Döngü SINIRLI ve sınıra dayanmak **GÖRÜNÜR**

Tool döngüsü **en fazla `AZAMI_ADIM`** tur döner. Sınıra dayanan cevap **sessizce teslim
edilemez** — yeni bir durum alır:

```python
Durum.ARAMA_TUKENDI  # araç bütçesi bitti, dayanak TAM DEĞİL — kullanıcıya söylenir
```

**Neden yeni durum, neden `KESIK` değil:** `KESIK` *"üretim bütçesi bitti, cümle yarım"*
demek; `ARAMA_TUKENDI` *"cümle tam ama dayanağı eksik olabilir"* demek. Kullanıcıya
söyledikleri **farklı**, dolayısıyla ayrı hâllerdir (CLAUDE.md §9: kapalı küme → sum type).

**Gerekçe:** bu hattın en pahalı hata sınıfı *"hata vermeden yanlış sayı/cevap üretmek"* —
`yurutme-tuzaklari.md`'deki **17 tuzağın hepsi** bu sınıftan. Agentic akış tam olarak bu
riski büyütür: döngü sessizce tükenirse kullanıcı **eksik dayanaklı bir cevabı tam sanır**.

### 4. ⛔ Araç katmanı KAPI KOŞUSUNA GİRMEZ — sıralama bağlayıcı

Yayımlanan **%80,1** ve `v1.0` kapısının eşiği **araçsız** rejimde ölçüldü; rakip çıpaları
(`3.1 FL` · `3.5 FL` · `3.5 Flash`) da **araçsız** koşuldu. Araç katmanı üretim davranışını
değiştirir ⇒ kapıyı araçlı koşmak [ADR-0057](0057-harness-rekabet-kapisi-esit-sinav.md)'nin
**eşit sınav** kuralını ihlal eder: bizim kol araç kullanır, rakip kullanamaz.

⇒ **Sıra bağlayıcıdır:**

```
1. kabul testi  (ARAÇSIZ — bugünkü ölçüm zinciriyle birebir aynı rejim)   → v1.0 hükmü
2. araç katmanı (ürün özelliği olarak eklenir)
3. yayın        (model + araç katmanı birlikte)
```

⚠️ Araç katmanının **kendi kazancı ayrıca ölçülebilir** ve bu ilginç bir sayı olur — ama o
ölçüm `v1.0` kapısının **yanında** raporlanır, **içinde** değil; ve rakip kıyası ondan
**kurulmaz**.

## Kapsam — `v1`'e ne giriyor, ne girmiyor

| | durum |
| :--- | :--- |
| CLI + TUI | ✅ **var, yeterli** — insan kararı 2026-09-08 |
| araç katmanı (`hakhukuk/araclar.py` + `servis` çok adımlı mod) | ▶️ **`v1`'e dahil** |
| HTTP API · web arayüzü | ⛔ **`v2`** (S9 açık) |
| araç kullanımının **eğitimi** | ⛔ **`v2`** — GRPO ödülüne *"doğru aracı doğru anda çağırdı mı"* girer (ADR-0075) |

⚠️ `v1`'de araç kullanımı **istem katmanındadır** (`Qwen3.5` tool calling'i base yeteneği).
Eğitilmediği için güvenilirliği düşük olacaktır ve bu **beklenen** bir durumdur; `v2`'de
öğrenilir. ⛔ Bu yüzden araçlar KAPI'ların yerine geçmez — **kapılar her hâlükârda çalışır**.

## Reddedilenler

| seçenek | neden reddedildi |
| :--- | :--- |
| Atıf doğrulamayı tool yapmak | Model çağırmayı unutur ⇒ **0/114** garantisi buharlaşır |
| Döngüyü sınırsız bırakmak | Maliyet ve gecikme kontrolsüz; ve sessiz tükenme *"hata vermeden yanlış"* sınıfını büyütür |
| `ARAMA_TUKENDI` yerine `KESIK` kullanmak | İki hâl kullanıcıya **farklı şey** söyler; birleştirmek ayrımı kaybeder (`bool`'un üç durumu kaybetmesiyle aynı hata) |
| Araç katmanını kapı koşusuna dahil etmek | ADR-0057 ihlali — rakip araç kullanamaz, sınav eşit olmaz |
| HTTP API'yi `v1`'e almak | İnsan kararı: CLI + TUI yeterli; API `v2`'nin işi |
