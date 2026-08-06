# G2 — Gemini Flash-Lite, harness AÇIK · ADR-0057 kademe tablosu

**Tarih:** 2026-08-06 · **git_sha:** `334880d` · **künye:** [`KUNYE.json`](KUNYE.json)

> **Bu tablo, projenin tarihinde rakibin İLK KEZ ürün rejiminde (harness AÇIK) ölçüldüğü yerdir.**
> Bugüne kadar *"FL'ı geçtik/geçemedik"* cümlesi kurulamıyordu: bizim sayımız harness AÇIK,
> FL'ınki KAPALI'ydı — iki ayrı sınav.
>
> ⚠️ **Birim: "puan" = YÜZDE PUANI.** Hakem gürültü tabanı **0,3 puan**. Bundan küçük fark
> **yorumlanmaz**.

## Sınavın gerçekten eşit olduğunun kanıtı

| eksen | BİZ | 3.1 FL | 3.5 FL | durum |
| :--- | :--- | :--- | :--- | :--- |
| sorular | `core_hard.jsonl` n=80 | aynı | aynı | ✅ |
| kaynak sayısı (h1) | 10 | 10 | 10 | ✅ |
| kaynak sayısı (h2b) | 4 | 4 | 4 | ✅ |
| **recall@10** | **0,875** | **0,875** | **0,875** | ✅ **birebir aynı** |
| altın sızması (h2b) | 0 | 0 | 0 | ✅ |
| seed · klip · bütçe | 3407 · 900 · 1024+512 | aynı | aynı | ✅ |
| yeterlilik önsözü (h1) | AÇIK | AÇIK | AÇIK | ✅ |
| hakem yığını | `openai/gpt-4o-mini` · `openrouter` · `[OpenAI]` | aynı | aynı | ✅ |

⭐ **`recall@10`'un üç öznede de birebir 0,875 çıkması tesadüf değil, kanıttır:** erişim modelden
bağımsızdır, yani üç özne de **aynı bağlamı** gördü. Harness'ın aynı olduğu varsayılmadı, ölçüldü.

---

## Kademe tablosu — her satırda hüküm

| kademe | eksen | kaynak | BİZ (AÇIK) | 3.1 FL | 3.5 FL | hüküm |
| :--: | :--- | :--: | ---: | ---: | ---: | :--- |
| **2** | **M1 kütle** (cov × A1) | 10 ↔ 10 | **%62,8** | %61,7 | **%69,5** | ✅ **EŞLEŞMİŞ** — 3.1 FL'ı **+1,0 puan** geçtik *(gürültünün 3,4 katı — dar)*; 3.5 FL bizi **−6,7 puan** geçiyor *(22 katı — sağlam)* |
| **2** | **A1 · altın getirilen** | 10 ↔ 10 | **0,8705** | 0,7835 | 0,8607 | ✅ **EŞLEŞMİŞ** — **her ikisini de geçtik** (+8,7 puan sağlam · +1,0 puan **dar**) |
| **2** | **A1 · cevaplanan** | 10 ↔ 10 | **0,8229** | 0,7054 | 0,7940 | ✅ **EŞLEŞMİŞ** — **her ikisini de geçtik** (+11,8 · +2,9 puan) |
| **2** | **aşırı-red** (↓ iyi) | 10 ↔ 10 | **%23,75** | **%12,5** | **%12,5** | ✅ **EŞLEŞMİŞ** — 🚨 **iki rakibin de ~2 KATI. Turun ana borcu (B10) doğrulandı.** |
| **2** | coverage (↑ iyi) | 10 ↔ 10 | 0,7625 | 0,8750 | 0,8750 | ✅ EŞLEŞMİŞ — aşırı-red'in aynası |
| **2** | altın geldi ama çekindi | 10 ↔ 10 | **14/80** | 8/80 | 6/80 | ✅ EŞLEŞMİŞ — B10'un çekirdeği: bağlamda altın **var**, model yine susuyor |
| **3** | **M2b Rej\*** (↑ iyi) | 4 ↔ 4 | 0,840 | 0,978 | 0,982 | ⛔ **TANIMSIZ — hüküm YOK.** Bizim M2b çıpamız **önsözsüz** koşuldu, FL kolları **önsözlü**. İstem ekseni **eşleşmiyor** (ADR-0057). |
| **3** | M2b fabrication (↓ iyi) | 4 ↔ 4 | 0,160 | 0,022 | 0,018 | ⛔ **TANIMSIZ** — aynı sebep |
| **3** | M2b Rej (regex) | 4 ↔ 4 | 0,820 | 0,911 | 0,768 | ⛔ **TANIMSIZ** — aynı sebep |
| **—** | muhakeme (reasoning tok) | — | **ölçülemiyor** | 789,4 (78/80) | 868,8 (41/80) | ⛔ **KISMEN TANIMSIZ** — bütçe eşleşik (1024), **ölçüm tek taraflı**: `llama-server` `reasoning_tokens` bildirmiyor |
| **—** | completion tok/cevap | 10 ↔ 10 | 803,9 | 970,5 | 573,6 | ⚠️ vekil eksen (düşünce iki tarafta da dâhil); 3.5 FL'ın düşük değeri **kesikten** kaynaklanıyor |
| **—** | kesik oranı | 10 ↔ 10 | %3,8 | %3,8 | **%10,0** | ⚠️ 3.5 FL önceki turun **%5 eşiğini aşıyor** — aşağıdaki şerh |
| **—** | **$/cevap** (liste fiyatı) | — | **$0** (yerel) | $0,001456 | $0,001434 | ✅ ADR-0017 maliyet ekseni **ilk kez rakiple aynı sınavda** dolduruldu |

### Kademe 3 satırları için hüküm kurulmadı

ADR-0057 gereği **"AÇIK burada geride" cümlesi kurulmamıştır.** M2b'de FL'ın sayısı bizimkinden
yüksek görünüyor, **ama bu bir üstünlük bulgusu değildir**: bizim M2b çıpamız
`--sufficiency-preamble` **olmadan** koşuldu, FL kolları **önsözle** koşuldu. Önsöz tam olarak
*"kaynak yetersizse söyle"* diyen istemdir — yani ölçülen eksenin kendisini değiştirir.
Repodaki **hiçbir** `m2b`/`h2b` koşusu önsöz kullanmıyor; eşleşme ancak bizim tarafımızda
**yeni bir önsözlü M2b koşusuyla** kurulabilir (yerel, API maliyeti $0). **Borç.**

### ⚠️ 3.5 FL kesik şerhi

3.5 FL iki koşusunda da **%10 kesik** (`finish_reason='length'`) verdi; 3.1 FL ve biz **%3,8**.
Aynı `1024 düşünce + 512 cevap` bütçesi altında 3.5 FL **daha çok muhakeme harcıyor**
(`reasoning_tokens` ort. 868,8 vs 789,4) ve cevabı kesiliyor. Bu, sınavın **ayarı** eşit olsa da
**etkisi**nin eşit olmadığı anlamına gelir. Sonuç: 3.5 FL'ın sayıları **aleyhine** eğilimlidir —
yani *"3.5 FL bizi 6,7 puan geçiyor"* hükmü **muhafazakârdır** (bütçe artsa fark muhtemelen açılır).
Bütçeyi 3.5 FL için artırmak **eşit sınavı bozacağı** için yapılmadı.

---

## ⭐ 3.1 FL ↔ 3.5 FL: giriş katmanı 16 günde ne kadar kaydı

Bu kıyas **tam eşleşmiştir** — aynı gün, aynı sorular, aynı harness, aynı istem, aynı bütçe,
aynı hakem yığını. Tek değişen model sürümü.

| eksen | 3.1 FL | 3.5 FL | fark | yorum |
| :--- | ---: | ---: | ---: | :--- |
| **M1 kütle** | %61,7 | **%69,5** | **+7,8 puan** | gürültü tabanının **26 katı** — gerçek |
| **A1 · cevaplanan** | 0,7054 | **0,7940** | **+8,9 puan** | sadakat belirgin yükseldi |
| **A1 · altın getirilen** | 0,7835 | **0,8607** | **+7,7 puan** | — |
| aşırı-red | %12,5 | %12,5 | **0** | çekinme davranışı **hiç değişmemiş** |
| M2b Rej\* | 0,978 | 0,982 | +0,4 puan | **gürültü içinde — yorumlanmaz** |
| kesik | %3,8 | %10,0 | +6,2 puan | 3.5 FL daha çok muhakeme harcıyor |
| liste fiyatı (çıktı) | $1,50/M | $2,50/M | **+%67** | kazanç bedava değil |

**Okuma:** Google'ın giriş katmanı 16 günde **kütlede +7,8 puan** kazandı ve kazanç tamamen
**sadakat** ekseninden geldi — çekinme davranışı milimetre oynamadı. Bu, `ROADMAP` §"Bakım
halkası"nın *"belirgin daha iyi bir base var mı"* sorusunun doğrudan verisidir: **rakip hareketli
bir hedef ve bizim tempomuzdan hızlı.**

⚠️ **Şerh:** iki modeli **farklı upstream sağlayıcı** servis etti (3.1 FL → `Google AI Studio`,
3.5 FL → `Google`). Üretim tarafında sağlayıcı **pinlenmiyor** (`LLM_PROVIDER_ORDER` yalnız hakem
kapısında etkili). Farkın bir kısmı sağlayıcı kaynaklı **olabilir**; bu ihtimal elenmedi.

---

## Bu turun asıl bulgusu

**Sadakatte öndeyiz, çekinmede iki katı geridiyiz.**

```
A1 · altın getirilen     BİZ 0,8705  >  3.5 FL 0,8607  >  3.1 FL 0,7835     ✅ birinciyiz
aşırı-red                BİZ %23,75  «  3.1 FL %12,5   =  3.5 FL %12,5      🚨 iki katı
altın bağlamda ama sustu BİZ 14/80   «  3.1 FL 8/80    «  3.5 FL 6/80       🚨 B10
```

Model, altın maddeyi **görüyor**, gördüğünde **rakiplerden daha sadık** cevaplıyor — ama
**gördüğü hâlde 14 kez susuyor**, rakip aynı bağlamda 6-8 kez susuyor. Kütledeki kaybımızın
kaynağı sadakat değil, **çekinme**. Bu, B10'un rakip karşısında ilk kez **sayıyla** doğrulanmasıdır:
*aşırı-red kapatılabilse kütlemiz `0,875 × 0,8229 = %72,0`'a çıkardı ve 3.5 FL'ı geçerdi.*

---

## Kaynak dosyalar

| sayı | dosya |
| :--- | :--- |
| BİZ h1 (çıpa) | `outputs/eval/olcum-bi/harness_tablo.json` · `a1_h1_tgta_v1_bi_k10.txt` |
| BİZ M2b (çıpa) | `outputs/eval/olcum-h2b-k4/abst_h2b_tgta_v1_h2b_k4_summary.json` |
| 3.1 FL | `harness_tablo_h1_fl31.json` · `a1_h1_fl31.txt` · `abst_h2b_fl31_k4_summary.json` |
| 3.5 FL | `harness_tablo_h1_fl35.json` · `a1_h1_fl35.txt` · `abst_h2b_fl35_k4_summary.json` |
| hakem ham çıktısı | `gnd_h1_fl31.jsonl` · `gnd_h1_fl35.jsonl` · `abst_h2b_*_k4.jsonl` |

⛔ **`cp09-butceli-1024-512`'deki eski FL sayıları (%72,9 · A1 0,9561) bu tabloya GİRMEZ** —
eski hakem yığınında (`gpt-4o-mini` / doğrudan `openai`, ADR-0041 öncesi istem) ve harness
KAPALI üretilmişlerdir. Aşağıdaki satır **yalnız kayıt sürekliliği** içindir:

| damga | koşu | kütle | A1 (cevaplanan) | hüküm |
| :--- | :--- | ---: | ---: | :--- |
| 🚫 **eski hakem yığını — HÜKÜM YOK** | 3.1 FL, harness **KAPALI**, cp09 | %72,9 | 0,9561 | kıyaslanamaz |
| ⚠️ güncel yığın, harness **KAPALI** | 3.1 FL, `g1-eslesmis-a1` gnd + yeni regex | %75,6 | 0,9605 | **TAVAN** — rejim eşleşmiyor, hüküm YOK |

⚠️ Harness KAPALI sayılar **TAVAN**dır, rakip değil: KAPALI'da altın madde bağlamda **garanti**
verilir. AÇIK'ta erişim onu %87,5 oranında bulur. İki ayar **aynı şeyi ölçmez**.
