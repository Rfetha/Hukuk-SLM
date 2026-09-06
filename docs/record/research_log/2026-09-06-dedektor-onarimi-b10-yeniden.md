# #61 — Dedektör onarıldı: B10 **14/80 → 8/80**, kütle **%62,8 → %68,4** — ve düzeltme BİZİM LEHİMİZE

- **Tarih:** 2026-09-06
- **Karar:** [ADR-0061](../../adr/0061-cekinme-dedektoru-istem-rejimi-bagimliligi.md) Karar 1
- **Önceki bulgu:** [#60](2026-09-06-hasat-kabul-olcutu-coktu.md)
- **Bedel:** hakem **$0** · GPU **$0** · yeniden puanlama tamamen deterministik
- **Test:** `112 passed, 2 xfailed` (çıpa: 99 passed, 1 xfailed) — ana oturumda **bağımsız doğrulandı**

## Onarım

`exact_reject`'in *"açılış hükmü yok"* dalı **11 satırla** değişti; `REJECT_RE`'ye **dokunulmadı**:

```python
# ÖNCE                                   # SONRA
return REJECT_RE.search(c)               if hukum is None and REJECT_RE.search(_ilk_esasli_ibare(c)):
#      ↑ TÜM METİN                           return True          # örtük OLUMSUZ açılış hükmü
                                         return REJECT_RE.search(_son_esasli_ibare(c))
```

Kural **#57/Ö2'nin aynısı, yalnız örtük kutupla**: ADR-0058 hükmü kurulmamışsa açılış hükmünü
*ilk esaslı ibare* taşır; oradaki red bağlayıcıdır, yoksa karar *son esaslı ibareye* düşer.
`hukum is True` dalı ve `mode="blind"` / `DISCLAIMER_RE` yolu **hiç değişmedi**.

⛔ **Elenen alternatif — karakter penceresi** (`c[:160]`): 13 vakanın 13'ünde çalışıyor **ama**
çıpa `id=19`'da payı yalnız **22 karakter**. Bu hattın hata sınıfı sessiz yanlışlık; o marj
kabul edilemez. Ayrıca elendi: *"yalnız son ibareye bak"* (13 vakanın 5'ini **ters yönde** kırıyor)
ve özne ayrımı (*"Diğer kaynaklar"* ↔ *"Verilen kaynaklar"* — semantik sınıflandırma, tuzak 2.9).

## ⭐ Gerçek B10 = **8/80** — 80 kalem GÖZLE okundu

Kalem kalem kayıt: [`outputs/eval/olcum-bi/B10_GOZLE_OKUMA_80.md`](../../../outputs/eval/olcum-bi/B10_GOZLE_OKUMA_80.md)

| ölçüt | çekinme | coverage | **B10** | kütle |
| :--- | ---: | ---: | ---: | ---: |
| ⭐ **gözle okuma (80/80)** | **13/80** | 0,8375 | **8/80** | **%69,6** |
| onarılmış alet | 14/80 | **0,8250** | **9/80** | **%68,4** |
| ~~eski alet (yayımlanmış)~~ | ~~19/80~~ | ~~0,7625~~ | ~~14/80~~ | ~~%62,8~~ |

**Eski aletin 14 B10'unun 6'sı yanlış pozitifti** (`id` 19 · 32 · 44 · 53 · 65 · 77).
🎁 **Yanlış negatif YOK** — gözle okunan 13 çekinmenin 13'ünü eski alet de yakalamıştı.
`recall@10 = 70/80` **üç ölçütte de aynı**: erişime dokunulmadı, değişen yalnız davranış ekseni.

## 🚨 Düzeltmenin yönü BİZİM LEHİMİZE — ve asimetri ÖLÇÜLDÜ, varsayılmadı

Kütle **+5,6 puan** yükseldi ve **rakip kolları hiç kıpırdamadı**. Bu, bu repo'nun en çok
şüphelendiği desendir, o yüzden ayrıca ölçüldü:

| kol | eski red | yeni red | fark | cevapta *"içermemekte"* geçen |
| :--- | ---: | ---: | ---: | ---: |
| `h1_fl31` (3.1 FL) | 10 | 10 | **0** | **3/80** |
| `h1_fl35` (3.5 FL) | 10 | 10 | **0** | **3/80** |
| `h2b_fl31_k4` | 43 | 42 | 1 | 19/80 |
| `h2b_fl35_k4` | 46 | 46 | **0** | 4/80 |

⭐ **Asimetri meşru ve mekanizması net:** hata **bizim kendi cevap şablonumuza** özgüydü.
`raft_scrubbed` şablonu her cevapta *"diğer kaynaklar … içermemektedir"* diye **eleme gerekçesi**
yazıyor; Gemini yazmıyor (80'de 3). Yani bozuk dedektör **sistematik olarak yalnız bizi
cezalandırıyordu** — üstelik cezalandırdığı şey **kendi eğitim şablonumuzun** izi.

### Rakip tablosu — sayılar, PARİTE İDDİASI DEĞİL

| M1 kütle (AÇIK, k=10) | değer |
| :--- | ---: |
| 3.1 FL | %61,7 *(değişmedi)* |
| **BİZ (onarılmış alet)** | **%68,4** ~~%62,8~~ |
| BİZ (gözle okuma) | %69,6 |
| 3.5 FL | %69,5 *(değişmedi)* |

⛔ ***"3.5 FL ile eşitlendik"* cümlesi KURULMUYOR.** Kalan açık **1,1 puan** ve bu ekseni koruyan
bir çözünürlük sınırı **YOK**: gürültü tabanı (0,3) **A1 makrosu** içindir, kütle = coverage × A1
ve **coverage'ın varyansı o tabanda yok** — bunu `g2-fl-harness/OZET.md` §164 zaten yazıyor.
Söylenebilecek tek şey: **3.1 FL'ı geçme marjı +1,0 → +6,7 puana genişledi**, 3.5 FL açığı
−6,7'den −1,1'e daraldı, ve **her ikisi de aletin düzeltilmesinden geldi, modelden değil.**

## 🚨 Turun ön-kayıtlı hedefi EĞİTİMSİZ karşılandı

Spec, sayı görülmeden B10 için **8-11/80** yazmıştı. Gözle okuma **8/80** veriyor — yani
`τ_a` v2 hiç eğitilmeden **hedefin alt ucundayız**. Turun öncülü (*"aşırı-red en büyük tek kayıp"*)
bu ölçümle **büyük ölçüde çözülüyor**: kayıp gerçekti ama **büyüklüğünün %43'ü aletin kendisiydi.**

⚠️ Bu, aşırı-redin yok olduğu anlamına gelmez — 8/80 hâlâ 3.5 FL'ın 6/80'inin üstünde.
Ama *"kütlenin büyük yarısı burada"* okuması artık **ayakta değil**.

## Yeniden puanlama — 82 dosya, $0

`harness_tablo.json` (9 tablodan 7'si değişti):

| koşu | coverage | B10 | kütle |
| :--- | :--- | ---: | :--- |
| `olcum-bi` ⭐ **resmî** | 0,7625 → **0,8250** | 14 → **9** | %62,8 → **%68,4** |
| `s2-harness-k10` | 0,7625 → 0,9000 | 16 → **5** | %61,5 → %73,2 |
| `s2-harness-k10-etiketli` *(ablasyon çıpası)* | 0,7625 → 0,9000 | 16 → **5** | %61,3 → **%73,0** |
| `s3-harness-k10` | 0,7750 → 0,9000 | 15 → **5** | %59,5 → %69,1 |
| `s3-harness-acik` | 0,7500 → 0,8875 | 14 → **6** | %56,9 → %69,4 |
| `olcum-h2b-k4` | 0,4500 → 0,5250 | — | — |
| `olcum-h2b-k10` | 0,5000 → 0,5500 | — | — |

`rejection_exact` **21 koşuda** düştü (en büyük: `m2_tg` 0,379 → **0,136** · `m2b_tg_v1_th`
0,506 → **0,325** · `m2_base_suff` 0,455 → **0,288**). 🎁 **`rejection_rate` (hakem) HİÇBİRİNDE
değişmedi** — pay hakemine dokunulmadığının bağımsız kanıtı.

🚨 **`g1-eslesmis-a1` — `base_vs_tgta` işaret DEĞİŞTİRDİ (ikinci kez):**
`base − tgta_v1` **−0,0038 → +0,0074** (kesişim 40 → 47); `uc_kol_tek_payda`'da aynı çift
−0,0038 → **+0,0184**. `fl_vs_tgta` 0,0261 → 0,0405 (**bizim aleyhimize** büyüdü).

82 yedek `*.ONCEKI-20260906` olarak yerinde, hiçbir eski değer silinmedi.

**$0 kanıtı:** yeniden hesap cerrahi — yalnız `reject_exact`/`rejection_exact` alanları
determinist regexle yeniden türetildi; `make_client()` hiç çağrılmadı, kör payda önbelleği
(`_artefakt/valid_trap_kor_onbellek.json`) **git'te değişmedi**, `judge_cost_usd` /
`valid_traps` alanları aynen duruyor.

## 🚨🚨 ADR-0058'İN GEREKÇESİ TERSİNE DÖNDÜ — yeni, kapatılmamış bulgu

Onarım, ana protokolün **kendi seçim gerekçesini** çürüttü.

| | eski (bozuk) alet | **onarılmış alet** |
| :--- | ---: | ---: |
| önsözlü — **resmî protokol** (`olcum-bi`) | %62,8 | **%68,4** |
| önsözsüz — **ablasyon** (`s2-harness-k10-etiketli`) | %61,3 | **%73,0** |
| **Δ(önsöz)** | **+1,5 p** ✅ | **−4,6 p** 🔴 |

[ADR-0058](../../adr/0058-b-i-kaynak-yeterliligi-onsozu-benimsendi.md) önsözü **tam da kütleyi
yükselttiği için** benimsemişti ([#56](2026-08-05-olcum-bosluklari.md) §D1: *"kütle %61,3 → %62,8"*).
Onarılmış aletle **düşürüyor**.

### Kıyas geçerli — doğrudan ham dosyalardan ölçüldü

⚠️ İki koşuda da `KUNYE.json` **yok** (borç **D-c**), o yüzden künyeye güvenilmedi:

```
n            80 ↔ 80
id kümesi    BİREBİR AYNI (kesişim 80/80)
soru metni   80/80 birebir aynı
context_shown 80/80 BİREBİR AYNI     ← değişen TEK şey istem
recall@10    0,875 ↔ 0,875
```

Yani ADR-0057'nin **eşit sınav** şartı bu çiftte tam olarak sağlanıyor: aynı sorular, aynı
kaynaklar, aynı sayıda kaynak, aynı rejim. Fark **yalnız istemden** geliyor.

### Diğer eksenler ne diyor

| eksen | önsözlü | önsözsüz | kim önde |
| :--- | ---: | ---: | :--- |
| kütle | 0,6838 | **0,7299** | önsözsüz **+4,6 p** |
| coverage | 0,8250 | **0,9000** | önsözsüz |
| A1 (cevaplanan) | **0,8288** | 0,8110 | önsözlü **+1,8 p** |
| A1 · altın getirilen | **0,8729** | 0,8593 | önsözlü **+1,4 p** |
| B10 (aşırı-red) | 9/80 | **5/80** | önsözsüz |
| B1 (isabetsizlik) | **5/80** | 7/80 | önsözlü |
| katı kapı reddi | 3/80 | **1/80** | önsözsüz |

⭐ **Takas net ve iki yönlü:** önsöz modeli **daha seçici** yapıyor (A1 ↑, B1 ↓) ama **daha
suskun** yapıyor (coverage ↓, B10 ↑). Bozuk alet suskunluğun bedelini **göremiyordu**, çünkü
önsözsüz kolun cevaplarını red sayıyordu — ve o kol **daha çok cevap ürettiği için daha çok
yanlış pozitif** alıyordu. Hatanın asimetrisi tam buradaydı.

### ⛔ Hüküm KURULMADI

Bu, ana protokolün değişmesi gereken bir bulgu **olabilir** ama:
- Protokol değişikliği **yeni bir ADR** ve **insan kararı** ister (ADR-0058 yürürlükte).
- Δ(önsöz) **−4,6 p** — ama bu ekseni koruyan bir **çözünürlük sınırı yok** (0,3 tabanı A1
  makrosu içindir; kütle = coverage × A1 ve coverage'ın varyansı o tabanda yok).
- ADR-0058'in benimsenme gerekçesi **yalnız kütle değildi**: çapraz tablonun dört hücresi
  (B10 16→14, B1 7→5) ve A1 kazancı da vardı. **A1 ve B1 hâlâ önsözün lehine.**

**Yayımlanan sayı bu turda DEĞİŞTİRİLMEDİ:** resmî protokol hâlâ önsözlü ⇒ **%68,4**.
Ablasyon **%73,0** olarak, bu şerhle birlikte yayımlanır.
⇒ Yeni açık soru; [`docs/open_questions.md`](../../open_questions.md) **S14**.

## Kapanmayan / şerhli kalemler

- 🟡 **1/80 uyuşmazlık — `id=32`:** onarılmış alet ÇEKİNME diyor, gözle okuma CEVAP. Model
  açılışta reddedip **gövdede kendi reddini yalanlıyor**. Bu #57/Ö2'nin **ayna vakası**.
  Rule of Three gereği **kapatılmadı** (tüm `outputs/eval`'da ölçülen örnek: **1**); sınır
  `xfail(strict=True)` testiyle çizildi — kural genişletilirse test patlar.
- 🚨 **17 `a1_*.txt` bu onarımdan ÖNCE de bayattı.** 9'u kasıtlı ADR-0044-öncesi damgalı çift;
  **8'i pre-v3 bir dedektörün ürünüydü** ve çoğu Gemini kolları — yani #57'nin Gemini
  kalibrasyonu `abst_*`'ı yeniden puanlamış ama `a1_*.txt` / `eslesmis_a1` artefaktlarını
  **atlamış**. Güncellendiler. ⚠️ Bu, *"aleti bir yerde düzeltmek yetmez"* dersinin **üçüncü
  tekrarıdır** (#57 → #60 → bu).
- 🟡 Çıpada **4 kalem** (`id` 31 · 36 · 57 · 68) red içermiyor ama esaslı hüküm de vermiyor
  (üretim döngüsü / salt atıf). *"Cevap"* sayıldılar; B10'un değil **sadakat ekseninin** borcu.
- ⛔ `cp2-on-eleme/abst_tiebreak_cevapli_m2` yeniden puanlanamadı: eşleşen `*_detail.jsonl` yok
  (küratasyon koşusu, ölçüm değil).
- ⛔ **Eşiklere DOKUNULMADI.** ADR-0061 Karar 2'nin yeniden türetmesi **insan onayı** bekliyor.

## 🐞 Süreç hatası — kendi hatam, kayda geçiyor

`be6768e` (belge commit'i) ajanın **uçuş hâlindeki** `scripts/score_abstention.py` (+36) ve
`tests/test_score_abstention.py` (+78) değişikliklerini **süpürüp commit etti** — ben iki ajan
paralel koşarken `git add -A` yaptım. Commit mesajı bu koddan söz etmiyor, yani **kayıt
yanıltıcıydı**. Bu girdi ve onu izleyen commit düzeltmedir.
**Ders:** paralel ajan koşarken `git add -A` yapılmaz; yalnız kendi dosyalarını `add` et.

## Ne değişti, ne değişmedi

| değişti | değişmedi |
| :--- | :--- |
| `exact_reject`'in **hüküm-yok** dalı | `REJECT_RE` · `hukum is True` dalı · `blind` yolu |
| 21 koşunun `rejection_exact`'i | **21 koşunun `rejection_rate`'i (hakem)** |
| 7 `harness_tablo` coverage/kütle/B10 | **`recall@10` — üç ölçütte de 70/80** |
| B10 **14 → 8** (gözle) / 9 (alet) | **Gemini kolları — düzeltme 0 kalem oynattı** |
