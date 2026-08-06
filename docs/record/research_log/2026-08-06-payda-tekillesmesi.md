# #58 — Payda tekilleşmesi: anahtar paylaşımı, iki rakip alet, ve **ARA KAPI'nın hükmü döndü**

**Tarih:** 2026-08-06 · **Checkpoint:** Görev 2, ikinci düzeltme dalgası · **GPU:** yok
**Hakem:** **$0,056** (15 kalem `gpt-4o`, payda) — diğer her ölçüm $0
**Karar belgeleri:** [ADR-0045](../../adr/0045-ara-kapi-merge-onarim-kontrolu.md) (hüküm döndü) ·
[ADR-0048](../../adr/0048-cevaba-kor-tuzak-gecerliligi.md) m.2 (alete alındı) ·
[ADR-0050](../../adr/0050-esik-degil-alet-duzeltilir.md) (bu turun bağlayıcı kuralı) ·
[ADR-0052](../../adr/0052-merge-norm-dengeleme-hukmu-tersine.md) · [ADR-0058](../../adr/0058-b-i-kaynak-yeterliligi-onsozu-benimsendi.md)
**Önceki halka:** [#57](2026-08-06-cekinme-aleti-onarimi.md) — K3, paydayı cevaba kör yapmıştı
**Yeni tuzaklar:** **2.17** (farklı sınavlar aynı payda kaydını paylaşır) · **2.18** (aynı ölçümün ikinci aleti)

> 🚨 **BU KAYDIN §1 REÇETESİ AYNI GÜN GERİ ALINDI.** "Anahtar tam kaynak metni üzerinde"
> reçetesi KARAR-4 m.1 ve [ADR-0060](../../adr/0060-onbellek-anahtari-hakem-istemine-esitlendi.md)
> ile **tersine çevrildi**; yürürlükteki reçete anahtarın **hakemin gördüğü** metne eşitlenmesidir.
> Bu kaydı tuzak 2.17'nin kaynağı olarak açıyorsan §1 ve §10'daki damgaları **oku**: teşhis ayakta,
> çare değişti. Eski metin silinmedi, üstü çizildi.

---

## Özet — bir cümlede

#57 paydayı **cevaba kör** yaptı; bu tur onu **tek** ve **doğru anahtarlı** yaptı, ve o
tekilleşme ARA KAPI'nın 2. gözlemini **✅'ten 🔴'ya** çevirdi.

---

## 1) K-1 — önbellek anahtarı klipli metnin üzerindeydi (tuzak **2.17**)

`gecerlilik_anahtari(soru, source)` `source[:3500]`'ü hash'liyordu. Sonuç: **farklı sınavlar
aynı payda kaydını paylaşıyordu.**

```
h2b@k=10  context_shown  medyan 7.174 · maks 10.281  →  79/80 kalem klipi AŞIYOR
h2b@k=4   context_shown  medyan 3.042 · maks  4.461  →  15/80 aşıyor
k4 ∩ k10 anahtar çakışması = 15 kalem  [5,11,12,16,18,28,36,42,43,46,48,57,59,62,66]
id=12:  k=4 uzunluk 4.461 · k=10 uzunluk 10.281 · ilk 3.500 AYNI · kaynak sayısı 4 ↔ 10
```

Özet dosyası bunu gizlemiyordu, **övünüyordu**: `"gecerlilik_devralinan": 15`.

~~**Onarım:** anahtar **tam** kaynak metni üzerinde; klip **yalnız hakeme giden istemi** kırpar.
Kusuru kilitleyen test (`..._ayirt_etmez`) **tersine çevrildi**.~~

> 🚨 **DAMGA 2026-08-06 — BU REÇETE AYNI GÜN TERSİNE ÇEVRİLDİ (KARAR-4 m.1 ·
> [ADR-0060](../../adr/0060-onbellek-anahtari-hakem-istemine-esitlendi.md)).** Üstü çizili metin
> **kayıt olarak durur, uygulanmaz.** Yürürlükteki reçete: anahtar **hakemin GÖRDÜĞÜ** metin
> üzerinde — `sha256(soru ‖ kaynak[:SOURCE_CLIP])`, `score_abstention.hakem_kaynagi()`.
> Gerekçe: tam-metin anahtarı tuzak 2.17'yi kapatırken **daha büyüğünü** açıyordu — hakemin
> ayırt edemediği bir farka göre bölünen anahtar *aynı istem → aynı cevap* değişmezini kırar
> (ölçüldü: 5.363 istemin 65'i >1 anahtara · 83 garantili gereksiz çağrı). Üstelik onarımın
> sayısal karşılığı **yoktu**: 15 çakışan çift yeniden ödendi, **15/15 aynı hüküm**.
> Tuzağın gerçek çaresi **klibi büyütmektir** (≈$0,30, `docs/open_questions.md`); ödenene kadar
> `k=10`'un paydası **TANIMSIZ** damgasıyla taşınır (ADR-0057), hüküm kurulmaz.
> Testler de tersine çevrildi: `test_gecerlilik_anahtari_HAKEM_ISTEMINE_ESIT` ·
> `test_hakem_isteminden_TASAN_METIN_ANAHTARA_GIRMEZ`.
> ⚠️ Çelişki **iki yerde** işaretli: burada ve `docs/record/yurutme-tuzaklari.md` tuzak **2.17**.

**Önbellek göçü — sezgi değil, özdeşlik.** Hakem istemi `kaynak[:3500]` ve bu dalgada
değişmedi; eski kayıt, o öneki paylaşan **her** tam metin için hakemin cevabının ta kendisi.
250 kayıt taşındı, **0 kayıp**, 15 çakışan grup. Eski dosya `.ONCEKI-KLIPLI-ANAHTAR`.

### ⚠️ K-1'in SAYISAL iddiası doğrulanmadı — ve bu bir bulgudur

Bulgu, `k=10`'un `Rej* = 0,723`'ünün **aşağı yanlı** olduğunu ve #56'nın *"k büyütmenin
çekinme bedeli"* manşetinin kısmen aletin eseri olduğunu söylüyordu. `k=10`'un devraldığı
15 payda **yeniden ödendi** ($0,056, `gpt-4o`, ortak önbellek dışında):

```
yeniden ödenen 15 kalemde payda dönen : 0
verdict dönen (pay hakemi hiç koşmadı): 0
valid_traps   65/80 → 65/80    ·    Rej* 0,723 → 0,723    (kılı kıpırdamadı)
```

**Sebep ölçülebilir ve önceden görülebilirdi:** klip sabitken çakışan çiftin hakem istemi
**bayt-bayt aynı**, dolayısıyla yeniden ödeme tanım gereği aynı cevabı verir. Yani anahtar
onarımı **yapısaldır** — gelecekteki sınav karışmasını keser — **sayısal değil**. `Rej*`'de
bir yanlılık varsa kaynağı anahtar **paylaşımı** değil, **3.500 klibi**dir; o **açık borç**
olarak fiyatıyla birlikte [`open_questions.md`](../../open_questions.md)'ye yazıldı (≈$0,30).

**Yan kazanım:** bu, payda hakeminin **yeniden koşum gürültüsünü** de ölçtü — 15/15 aynı,
yani `temperature=0` + `seed` bu eksende gerçekten kararlı.

## 2) K-3 — iki rakip alet, ve 900 klipi bir **kategori hatası** (tuzak **2.18**)

`valid_trap_cache.py` (klip **900**) ve `score_abstention.py` (klip **3500**) aynı cp09
koşularında **çelişen** kör payda üretiyordu:

| cp09 m2b Rej | cevaba bağlı | #46 (klip 900) | yürürlükteki (klip 3500) | fark |
| :--- | ---: | ---: | ---: | ---: |
| base | 0,986 | 0,949 | **0,961** | 1,2 p |
| Gemini 3.1 FL | 1,000 | 0,861 | **0,883** | 2,2 p |
| `τ_g` | 0,607 | 0,519 | **0,506** | 1,3 p |

Hepsi hakem gürültü tabanının (0,3 p) **4-7 katı**.

**İki klip aynı şey mi? HAYIR — ve bu ölçüldü.**

- **900** = ADR-0011'in eval-ayna klipi. `gen_eval_grounded --max-chunk-chars 900`,
  **üretim** zamanında, **her `[KAYNAK]` parçasına AYRI** uygulanır (satır 543/575).
  `context_shown` **zaten kırpılmış parçaların birleşimidir.**
- **3500** = `score_abstention.SOURCE_CLIP`, **skorlama** zamanında, hakeme giden **kaynak
  metninin tamamına**.

`valid_trap_cache.py` **parça sabitini birleşime** uyguluyordu. Bedeli (cp09 m2b, n=80,
`[KAYNAK` sayımı):

```
tam metin  : 320 kaynak
klip  900  : 147 kaynak   (%46)   ← #46'nın kör paydası bağlamın YARISINDAN karar vermiş
klip 3500  : 320 kaynak  (%100)
```

Aynı ölçüm `h2b@k=10`'da **3500'ün de yetmediğini** gösteriyor: 454/800 = **%57**.

**Onarım:** `valid_trap_cache.py` **ince sarmalayıcıya** indi (kendi klipi/anahtarı/hakem
çağrısı yok, hepsi `score_abstention`'dan; kalan tek işi `cp2c_kabul.sh`'in beklediği
`{mod}:{id}` görünümü). `rescore_abstention_cached.py` **silindi** — oranları ikinci bir
yerde bölüyordu **ve** `reject_exact`i satırda saklanmış (bayat dedektör) alandan okuyordu.
Yerine `score_abstention --pay-kaynagi onceki`. [#46](2026-07-30-cp2r-kor-payda.md)
**damgalandı, silinmedi**; ayakta kalan üç hükmü ayrıca yazıldı.

## 3) KARAR-2 — boş bağlamda payda **tanım gereği** n/n (ADR-0048 m.2 alete alındı)

Kural aletin **dışında** durduğu için M3 skorlaması varsayılan `--source-field referans` ile
**altın maddeyi** hakeme gösteriyor, hakem *"kaynak cevaplıyor"* deyip tuzağı geçersiz
sayıyordu. Altı koşu yeniden puanlandı, **hakem çağrısı yok, $0**:

| koşu | payda ESKİ → YENİ | Rej* ESKİ → YENİ |
| :--- | :--- | :--- |
| cp09 `m3_base_th` | 54 → **80** | 1,000 → 1,000 |
| cp09 `m3_gem_th` | 56 → **80** | 1,000 → 1,000 |
| **cp09 `m3_tg_v1_th`** | **39 → 80** | **0,923 → 0,800** 🔴 |
| sprint1 `m3_base` | 57 → **80** | 1,000 → 1,000 |
| sprint1 `m3_gem` | 57 → **80** | 1,000 → 1,000 |
| sprint1 `m3_tg` | 50 → **80** | 1,000 → 1,000 |

En büyük hareket **aleyhimize**: `τ_g`'nin M3'ü 12,3 puan düştü. Eski özetler
`.ONCEKI-20260806` olarak duruyor.

🔴 **`m2` kapanmadı** — fiyatı ölçüldü (**≈$0,11**, tek ödeme 10 koşuyu birden kapatır, çünkü
on koşunun m2 sınavı birebir aynı: 70/70 anahtar kesişimi). Bütçe tavanı aşılmasın diye
**durup soruldu**. Bir kestirme de **bilerek reddedildi**: #46'nın 66/70 damgası 52 kalemde
$0'a devralınabilirdi (metin ≤900 olduğu için hakem istemi bayt-bayt aynı) — ama o damga
`gateway=openai` ile üretildi, bugünkü ölçümler `gateway=openrouter`; ADR-0029/tuzak 2.7
hakem yığınının aynı olmasını şart koşuyor.

## 4) ⭐ K-2 — ARA KAPI 2. gözlemi yeniden türetildi ve **DÜŞTÜ**

Ön-kayıtlı olan **formül**di, sayı değil (`defter.md` m.1). ⛔ ADR-0050 gereği eşiğe, çarpana,
formüle **dokunulmadı**; yalnız bugünkü tek aletle yeniden bölündü:

```
eşik  = 0,90 × base M2b 0,961 = 0,8649
merge = 0,766   (ham TIES, cp3-supurme-ham/m2b_tg_ta_ham_th, payda 77)
   →  🔴 DÜŞTÜ, 9,9 puan altında
eski 0,887 eşiğine karşı da  →  🔴 DÜŞTÜ
paydalar EŞİT (77 ↔ 77)      →  kıyas geçerli, tuzak 2.6 tetiklenmiyor
```

Üç türetmenin tamamı:

| tarih | base M2b | eşik | merge | hüküm |
| :--- | ---: | ---: | ---: | :--- |
| 2026-07-29 (ADR-0045 ön-kayıt) | 0,986 *(cevaba bağlı)* | 0,887 | — | — |
| 2026-07-30 (#46, klip 900) | 0,949 | 0,8541 | 0,877 | ✅ GEÇTİ |
| **2026-08-06 (yürürlükte)** | **0,961** | **0,8649** | **0,766** | **🔴 DÜŞTÜ** |

**Bu kapı CP4-CP5 harcamasını yetkilendiren kapıydı — yetki bugünkü ölçümle YOK.** Üstelik
1. gözlemin (`τ_a` tekil M2) paydası onarılmadığı için satır ya `✅ ❌` ya `❌ ❌`; ADR-0045
§3'ün **ön-kayıtlı** yorum tablosunda **her iki hâlde de karar DUR**.

**ADR-0052'nin kendi hükmü etkilenmiyor:** *"ham TIES ≫ norm-dengeli"* ayakta. Değişen,
ham TIES'in **mutlak** olarak kapıyı geçip geçmediği. `τ_g`'nin M2b çöküşünü onarım oranı
**%71 → %57**'ye iniyor (0,607→0,877 ⇒ 0,506→0,766).

Türetme: `outputs/eval/cp2-r-kor-payda/ara_kapi_esikleri_2026-08-06.json`.
Damgalanan altı belge: ADR-0045 · ADR-0052 · `sprint2/defter.md` · `#48` ·
`research_log/README` (#46 ve #48) · `_arsiv/sprint2.md` · `TASARIM.md:337`.

## 5) Ö-B — ADR-0058'in ablasyon koşusu emekli dedektörün sayısını taşıyordu

`cp09-ab-ayrimi/abst_m2_base_suff` → `rejection_exact` **0,452 → 0,484** (id 53 ve 55 açılış
kuralıyla çekinmeye döndü). **3,2 puan = gürültü tabanının ~10 katı.** Hakem çağrısı yok, $0.
ADR-0058'in **hükmüne etkisi yok** (benimseme gerekçesi kütle/A1/B10 üzerine kurulu,
`rejection_exact` hiçbir eşiğe girmiyor) ama sayı kayıtta yanlış duruyordu. ADR-0058
damgalandı. Paydası **devralındı** ve özette öyle damgalandı — `m2` hâlâ açık borç.

## 6) Ö-C — kesiklik kapısı **simetrik** uygulandı (tuzak 1.9)

Repo kendi `tg_ta_nb` varyantını %5,2 kesiklikle geçersiz saymıştı; `h2b_fl35_k4` **%10,0**
kesikle manşet hükmün kurulduğu koldu ve şerhi yoktu (`finish_reason == "length"`; bizim
`forced_close`'umuz kesiklik değildir).

| kol | tam (n=68) | ortak kesiksiz alt küme (n=60) | fark |
| :--- | ---: | ---: | ---: |
| BİZ (önsözlü) | 0,809 | 0,800 | −0,009 |
| 3.1 FL | 0,809 | 0,817 | +0,008 |
| **3.5 FL** | **0,926** | **0,950** | **+0,024** |

**Açıklık daralmıyor, GENİŞLİYOR:** 11,7 → **15,0 puan**. Hüküm **ayakta ve güçlenmiş** —
ama şerh olmadan kurulamazdı. `OZET.md` hükmün kurulduğu satıra ve ayrı bir bölüme yazıldı.

## 7) Ö-D — açılış-hükmü kuralının maruziyeti **~8 kat** asimetrik

| kol | kural kapsamı | olumlu açılış | olumlu ∧ gövdede red |
| :--- | ---: | ---: | ---: |
| `h2b_fl35_k4` | **39/80** | 19 | **4** |
| `h1_fl35` | 56/80 | 54 | 1 |
| `h2b_fl31_k4` | 8/80 | 4 | 0 |
| BİZ önsözlü | **5/80** | 5 | 1 |
| BİZ önsözsüz | **0/80** | 0 | 0 |

Kaydın savunması *"bizim çıpalarımızda 0 satır değişti"* bir **gözlenen etki** argümanıydı,
**maruziyet** argümanı değil: kuralın çevirdiği 3 satırın **üçü de** manşet hükmün kurulduğu
kolda. Kural **değiştirilmedi** (ADR-0050); asimetri `open_questions.md`'ye yazıldı.

## 8) Ö-E — sınır çizildi, kural **onarılmadı**, gerekçe ölçüldü

İddia edilen kaçak: *"Verilen kaynaklar soruyu cevaplamaktadır. Kaynaklarda bu konu
düzenlenmiyor. Bu konuda güncel mevzuata başvurmanız gerekir."* → son esaslı ibarede
`REJECT_RE` yok → **cevapladı** sayılır. Şekil gerçek, ama **korpusta yok**:

```
olumlu açılışlı cevap toplam                                    96
gövdede red var, son ibarede YOK                                 3   → ÜÇÜ DE gerçekten dolu cevap
son ibaresi tavsiye/başvuru kalıbıyla biten                      4   → DÖRDÜ DE gerçekten dolu cevap
bu şekle uyan GERÇEK vaka                                        0
```

Ölçüm anlamsız çıktığı için kural **onarılmadı** (ADR-0050 ruhu: körlemesine genişletmek yeni
yanlış-pozitif üretir). Sınır bir **`xfail(strict=True)`** testiyle çizildi: kusuru
**kilitlemez**, kural düzelirse test **patlar** ve damganın kaldırılmasını zorlar.

## 9) Küçükler

- **k-1** — #57'nin *"m2b distractor (8 koşu)"* sayımı yanlıştı; `mode == "distractor_nogold"`
  tarandı, gerçek **10** (cp09 ×3 · cp3-supurme-ham/-min · cp3c · cp3e · sprint1 ×3; kürasyon
  koşuları ölçüm değil, dışarıda). *Doğrulama iddiadan güçlüydü, sayım yanlıştı.*
- **k-2** — bir önceki dalgada pay hakemi de yeniden koşmuştu ve paydası değişmeyen kalemlerde
  **6 verdict** dönmüştü. Bu dalgada **ayrıştırıldı**: `--pay-kaynagi onceki` pay hakemini hiç
  çağırmıyor, yani ölçülen her hareket **yalnız paydanındır**. K-1'in 0 hareketi bu sayede
  temiz okunabildi.
- **k-3** — `judge_cost_usd` iki hakemin toplamıydı; ayrıştırıldı (`pay_maliyet_usd` +
  `gecerlilik_maliyet_usd`). `global-kisitlar.md`'nin *"$0,04/koşu"* çıpası damgalandı:
  o yalnız **pay** tarafı. Payda birim maliyeti ölçüldü: **$0,0037/kalem** (3.500 karakter).
- **k-4** — tuzak listesine **2.17** ve **2.18** eklendi; 2.17'nin birim testi var
  (`test_farkli_sinavlar_ayni_payda_kaydini_PAYLASMAZ`).
- **k-5** — damgasız kalan canlı kayıtlar damgalandı: `TASARIM.md:337` ·
  `sprint2/defter.md` (ARA KAPI bloğu + ölçülen tablonun M2b sütunu + seyrelme satırı) ·
  `#48` · `research_log/README` (#46 · #48).
- **k-6** — `harness_tablo.py:137`'nin `id` ↔ liste-indeksi karışıklığı **gizil kusur** olarak
  `open_questions.md`'ye yazıldı; bugün çalışıyor (id'ler 0..n-1), seyrek id'de sessizce
  yanlış coverage verir. Düzeltilirse **önce düşen test**.

## 10) Alet tarafındaki kalıcı değişiklikler

| ne | niye |
| :--- | :--- |
| ~~`gecerlilik_anahtari` → **tam** kaynak~~ 🚨 **TERSİNE ÇEVRİLDİ aynı gün** → anahtar **hakemin gördüğü** metin (`kaynak[:SOURCE_CLIP]`) | ~~tuzak 2.17~~ → KARAR-4 m.1 · [ADR-0060](../../adr/0060-onbellek-anahtari-hakem-istemine-esitlendi.md); gerekçe §1'deki damgada. Tuzak 2.17'nin **teşhisi** ayakta, **çaresi** değişti |
| `payda_tanimdan_gecerli(mode)` | ADR-0048 m.2 aletin **içinde**; TANIM kararı içerik-adresli önbelleğe **sızmaz** |
| `--pay-kaynagi {hakem,onceki}` | paydanın etkisini payın gürültüsünden ayırmak (k-2) |
| `--payda-kaynagi {hakem,onceki}` | yalnız dedektör değiştiğinde paydayı sabit tutup `reject_exact`i tazelemek; devralınan payda özette **damgalanır** |
| `yedekle()` | yayımlanmış çıktının üstüne **sessizce** yazılmaz (`.ONCEKI-<tarih>`) |
| `llm_client.gateway_of()` | hiç çağrı yapmayan koşu kimlik istemesin; kapı adı iki yerde ayrı türetilirse sessizce ayrışır |
| `pay_maliyet_usd` / `gecerlilik_maliyet_usd` | k-3 |

## 11) Bütçe

| kalem | tutar |
| :--- | ---: |
| K-1 · k=10'un 15 devralınan paydası, `gpt-4o` | **$0,056** |
| KARAR-2/M3 · altı koşu | $0 |
| Ö-B · ablasyon koşusu | $0 |
| K-2 · ARA KAPI türetmesi | $0 |
| GPU | $0 |
| **TOPLAM** | **$0,056** |

**Harcanmayan, insana bırakılan:** m2 paydası ≈$0,11 · `SOURCE_CLIP` borcu ≈$0,30.
