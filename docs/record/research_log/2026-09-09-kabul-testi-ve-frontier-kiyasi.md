# #65 — Donmuş TEST açıldı, frontier havuza girdi, iki alet kusuru daha

**Tarih:** 2026-09-09 · **Bedel:** $1,2127 (OpenRouter) + $0 (yerel GPU)
**Çıktılar:** `outputs/eval/hp-rakip-havuzu/` · `outputs/eval/g16-kabul-testi/`
**Kararlar:** [ADR-0077](../../adr/0077-v1-0-verilmedi-v0-3.md)

## 1. `KUNYE` taşınabilirliği — indeks artık her makinede yükleniyor

`data/index/**/KUNYE.json` korpusu **mutlak yol + `(bayt, mtime)`** ile damgalıyordu ve
`retriever.yukle` bunu doğruluyordu ⇒ `git clone` sonrası **her makinede** `SystemExit`.
Yol **indeks dizinine göreli**, `mtime` vekili **sha256** oldu; künyeye önek sözleşmesi ve
`model_revision` eklendi.
`verify:` repo başka bir dizine kopyalandı, korpusun `mtime`'ı `git checkout` gibi tazelendi,
indeks oradan yüklendi → **`recall@10` 0,9500 (76/80)** — yeniden gömerek ölçülen değerin
birebir aynısı, **bağımsız çapraz kontrol**. Kontrol koşusu: HEAD'deki kod aynı koşulda
`korpus bulunamadı` ile patlıyor.
🆕 `scripts/erisim_korpus/recall_indeksten.py` — `recall_olc.py` korpusu sıfırdan gömdüğü için
*"dağıtılan indeks doğru mu"* sorusu bugüne kadar **ölçülemiyordu**.

## 2. Frontier havuza girdi: `anthropic/claude-sonnet-5` — ve **önde**

F0.4'ün birebir aynı rejimi (n=80, seed 3407, k=10, 900 klip, `--reasoning-budget 1024`,
önsözsüz, hakem `gpt-4o-mini`). Eşit sınav kanıtı: `recall@1/3/5/10` = 0,5250 / 0,7625 /
0,8250 / **0,9500** — dört basamak da bizim kolla birebir; kesiklik 4/80 ↔ 4/80.

**Zorunlu ön adım — red dedektörü yeni ailede kalibre edildi** (8/8 kalem gözle okundu):
alet 8 çekinme sayıyor, **3'ü açık yanlış pozitif** (id 17 · 35 · 41 — tam, alıntılı, doğru
cevaplar). Kusur **ADR-0061'in birebir aynı sınıfı**, aile değişti: dedektör **son esaslı
ibareyi** tarıyor, bu ailenin şablonu cevabı **şerh cümlesiyle** kapatıyor. id 35: *"nafaka
davaları basit yargılama usulüne tabidir"* açılışı ↔ *"…açıkça başka bir usul **belirtilmediği**
sürece…"* kapanışı ⇒ olumlu hükmün **içindeki** olumsuzlama red sayılmış.
⛔ `REJECT_RE`'ye dokunulmadı; düzeltme GÖZ okumalarında.

| okuma | BİZ `tgta_v1` | Sonnet-5 | fark |
| :--- | ---: | ---: | ---: |
| ALET | **0,8011** | 0,7911 | +1,00 p bize |
| GÖZ-orta | 0,8011 | **0,8223** | −2,12 p |
| **GÖZ-katı** | 0,8011 | **0,8348** | **−3,37 p** |

**Öne geçtiğimiz tek okuma, önde olmadığımızı bildiğimiz okumadır.** Aynı düzeltmeyi F0.4'te
Gemini ailesinin **lehine** yapmıştık; burada kendi **aleyhimize** uygulandı.

🚨 **B1 hakkındaki cümlemiz çürüdü.** *"Rakiplerden geride değiliz (8/80 ↔ 8·8·7·8)"* yalnız
**Gemini havuzunda** doğruydu: `wrong_ref_rate` **BİZ 0,0769 ↔ Sonnet 0,0083 = 9,3× geride**.
Deterministik doğrulayıcı ise *uydurma madde* ekseninde bizi önde gösteriyor (**0/114 ↔ 2/163**).
İkisi çelişmiyor, **farklı şey sayıyor**: madde **uydurmuyoruz**, var olan **yanlış** maddeye
atıf yapıyoruz. Karar değişmedi (G14 atlandı, ADR-0075) ama **gerekçesi düştü**; B1 borç.

**Bedel dersi:** tam koşu **$1,1932** tuttu, tahmin **$0,82** idi (+%45, `$1` kapısı aşıldı).
5 kalemlik duman koşusundan **×16 doğrusal ekstrapolasyon**, cevap uzunluğu soruya göre değişen
bir özne için **kapı kurmaya yetmiyor** (706,6 completion token/cevap × $10,00/M çıktı).
⇒ Tabakalanmış duman koşusu ya da **%50 emniyet payı**.

## 3. Donmuş TEST açıldı (insan onaylı, tek kez) — ham kütle **0,5804**

n=40, araçsız (ADR-0076 m.4), rejim DEV ile birebir, kesiklik **%2,5** (kapı %5).

| | TEST | DEV |
| :--- | ---: | ---: |
| ham kütle | **0,5804** | 0,8011 |
| tavan `recall@10` | 0,7500 | 0,9500 |
| tavan kullanımı | 0,7739 | 0,8433 |
| uydurulmuş madde | **0/52** | 0/114 |
| `wrong_ref_rate` | 0,2424 | 0,0769 |

**Düşüşün ayrıştırılması:** toplam −22,07 p · tavan-eşdeğer beklenti 0,6324 ⇒ **tavanın
açıkladığı −16,87 p (%76)**, **açıklamadığı −5,20 p (%24)**. ADR-0069'un öngörüsü doğrulandı
**ama tam değil** — model görülmemiş veride tavanını da daha kötü kullanıyor.
*"Hepsi bileşim"* denmedi.

**Gözle okuma kapısı:** 9/40 çekinmenin dokuzu da okundu, **yanlış pozitif 0** ⇒ ALET = GÖZ.
Alet bizim ailemizde doğru, başka ailelerde değil — F0.4'ün bulgusu TEST'te de sürüyor.

## 4. 🚨 Donmuş TEST'in yakaladığı kusur — `atif_dogrula.py`

Alet önce **MÜLGA 2** dedi. Okundu: tek kalemden (id 32). Altın `İŞ KANUNU (4857) Madde 111`,
**1. sırada** getirilmiş, model **doğru** cevaplamış ve *"İş Kanunu Madde 111"* diye
**kanun numarasız** atıf yapmış. Korpusta bu ada **iki** kanun uyuyor: 4857 (yürürlükte) ve
**1475 (mülga)**. `dogrula()` adayları `sorted()` ile geziyor ve **ilk taşıyanı** döndürüyordu
⇒ 1475 kazanıyor, **doğru cevap MÜLGA damgası yiyordu**. Vatandaşa giden rozet buna bağlı.

Kodun kendi ilkesi — *"yürürlükte tek satır bile varsa mülga sayılmaz"* — tek bir `kanun_no`
**içinde** vardı, **adaylar arasında** yoktu. Bir seviye yukarı taşındı (TDD: kırmızı görüldü).
TEST atıf `DOGRULANDI` **50→52**, `MULGA` **2→0**. Manşet **değişmedi**; DEV ve Sonnet kolları
**oynamadı**.

⭐ **Ders:** donmuş seti açmanın bedeli tek seferliktir; karşılığında **yayına gidecek bir rozet
hatası** yakalandı. ADR-0051 üçüncü kez kendini ödedi.

## 5. Hüküm: `v1.0` verilmedi → `v0.3` ([ADR-0077](../../adr/0077-v1-0-verilmedi-v0-3.md))

Donmuş TEST için **ön-kayıtlı sayısal eşik yoktu** ve sayı görüldükten sonra eşik yazmak
ADR-0050'nin yasağıdır. Hüküm **ADR-0064'ün kendi metnine** dayandırıldı: orada `v1.0` için
eksik iki şey sayılı — *(a) kabul testi koşmadı* **bugün kapandı**, *(b) tek hakem ailesi*
**açık** (κ 0,534 < 0,6, üçüncü hakem atlandı). ⇒ `v1.0`'ı bloke eden **model değil, ölçüm
aygıtı**.

## Paper eşlemesi

Methodology (kabul testi + tavan kullanımı) · **Negatif bulgu** (frontier önde; B1 hükmümüz
havuza bağlıymış) · Limitations (tek hakem ailesi, κ eşik altı, n=40 Wilson aralıkları geniş).
