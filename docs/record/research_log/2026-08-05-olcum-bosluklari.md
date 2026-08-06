# #56 — Ölçüm boşlukları: m2b harness AÇIK · B5 · B8 · B-i

**Tarih:** 2026-08-05
**Plan:** [`superpowers/plans/2026-08-05-olcum-bosluklari.md`](../../superpowers/plans/2026-08-05-olcum-bosluklari.md)
**Kararlar:** [ADR-0057](../../adr/0057-harness-rekabet-kapisi-esit-sinav.md) *(eşit sınav kapısı)* ·
[ADR-0056](../../adr/0056-m2b-harness-acik-protokolu-ve-0055-cipasi.md) · [ADR-0055](../../adr/0055-isabet-denetimi-ekseni.md)

## Künye

```
model      models/gguf/tgta_v1-q4_k_m.gguf  (tgta_v1 = HakHukuk-4B-v0.1)
indeks     data/index/mevzuat_bge_m3_s2     korpus data/corpus/mevzuat_maddeler.jsonl (40.496)
rejim      thinking on · think-budget 1024 · max-new-tokens 512 · seed 3407
           max-chunk-chars 900 · CTX 8192 · KV q8_0/q8_0
hakem      openai/gpt-4o-mini · OpenRouter · sağlayıcı pinli (OpenAI)  — tuzak 2.7
koşular    outputs/eval/olcum-h2b-k4/ · olcum-h2b-k10/ · olcum-bi/
           (post-hoc: outputs/eval/s2-harness-k10-etiketli/)
maliyet    GPU $0 · hakem $0,041 (Ö1) + $TBD (D1)   bütçe ≤ $2
geçit      n=80 · kesik %3,8 · ALTIN_SIZAN=0 · kaynak={k} · üç koşuda da GEÇTİ
```

## 1. Ö1 — `m2b` harness AÇIK: **kapı KALDI**

Part 1'in iki gerekçesinden biri *"red kapısı M2b'yi kapatır"* idi ve **hiç sınanmamıştı**.
Sınandı.

```
kol                kaynak   Rej*   Rej_rgx  payda  geçersiz  kapı_red  atıfsız  zorluk
KAPALI m2b (çıpa)      4   0,877    0,846     65       15        -        -    1,0000
AÇIK  h2b k=4          4   0,840    0,820     50       30        2       36    0,4750  ← HÜKÜM
AÇIK  h2b k=10        10   0,784    0,706     51       29        4       34    0,4350    bilgi
```

⚖️ **ADR-0057 Kademe 2 kapısı: KALDI** (0,840 < 0,877 + 0,003). İki bağımsız tahmin edici de
aynı yönde (**−0,037** hakem · **−0,026** regex), ikisi de hakemin **~0,3 puanlık** yeniden-koşum
gürültü tabanının üstünde.

🚨 **Ve zorluk şerhi bulguyu ZAYIFLATMIYOR, GÜÇLENDİRİYOR.** KAPALI'nın 4 çeldiricisinin
**tamamı** altınla aynı kanundan (`sample_distractors` komşu-öncelikli seçiyor, `raft_pack.py:75-91`)
→ zorluk **1,0000**. AÇIK'ta bu oran **0,4750**; dağınık bağlamda *"kaynak yetmiyor"* demek daha
kolaydır. **AÇIK daha kolay sınava girdi ve yine de kaybetti.**

### Ön-kayıtlı tahminler (ADR-0056 Karar 2, sayı görülmeden yazıldı)

| | tahmin | çıkan | hüküm |
| :--- | :--- | :--- | :--- |
| **A** kapının katkısı | ≈0 (0-2/80) | k=4'te kapı **2/80** reddetti, biri cevaptı | ✅ **TUTTU** |
| **B** `Rej_model` | 0,30–0,60 | **0,840** | ❌ **TUTMADI** |

**A'nın mekanizması da ayrıca doğrulandı:** `KANUN_YOK 0 · MADDE_YOK 0` ve **36/80 cevabın hiç
atfı yok** (`atifsiz_gecen`). Kapı yalnız doğrulanamayan atıf varken ateşler; ateşleyecek şey yok.

⇒ **Part 1'in M2b iddiası "sınanmamış" değil, bu rejimde YAPISAL OLARAK ateşlenemez.**
ADR-0056 Karar 2'nin yazdığı sonuç işliyor: **M2b eğitim tarafına geçer.**

**B için ADR-0056'nın kendi kuralı geçerli:** *"tutmazsa 'tahmin kötüydü' değil **'payda
yanlıydı'** diye oku."* Tahmin, altın gelmeyen **10** sorudan türetilmişti; o alt küme #53'e göre
ağırlıkla "belirsiz" sınıfıydı ve model orada daha az çekiniyor. Gerçekte model tahmin edilenin
**iki katından fazla** çekiniyor.

### 🎁 `k`'nın bedeli ilk kez ÇEKİNME ekseninde sayıldı

`k=4 → k=10`: Rej **0,840 → 0,784** (**−5,6 puan**). Bugüne dek `k`'nın bedeli yalnız **sadakat**
ekseninde ölçülmüştü (A1·altın getirilen 0,9230 → 0,8426, #54). **İki eksen aynı yöne bakıyor:**
daha çok bağlam = hem daha az sadakat hem daha az çekinme.

### ⭐ Beklenmedik: geçersiz tuzak **30/80 ↔ 15/80**

Altın **ablasyona rağmen** retriever, soruyu *fiilen cevaplayan* bir kaynağı **iki kat sık**
getiriyor (hakem "kaynak zaten cevaplıyor → tuzak geçersiz" diyor). Bu retriever lehine ayrı bir
kazançtır — ve paydaların (50/51 ↔ 65) neden farklı olduğunun cevabıdır. **Kaynak sayısı eşitlendi,
kaynak İÇERİĞİ eşitlenemedi** — ADR-0057 Kademe 2'nin kabul ettiği bedelin ölçülmüş hâli.

## 2. B5 — K2'nin bedeli (`harness_tablo.py`, post-hoc, $0)

`s2-harness-k10-etiketli`, n=80:

```
ALTIN_GELMEDI 10 · TAM 22 · KIRPILDI 46 · KIRPILDI_CEVAP_DISI 2      (toplam 80 ✓)
```

🚨 **Planın okuma cümlesi yapısal olarak imkânsızdı.** Plan *"`KIRPILDI_CEVAP_DISI`, B1'in
7/80'inden düşülür"* diyordu; oysa `k2_bedeli` altın gelmediyse `ALTIN_GELMEDI` döner, dolayısıyla
`KIRPILDI_CEVAP_DISI` **ancak altın getirildiyse** çıkabilir. B1'in 7'si ise tam ters popülasyon
(`altin_gelmedi_cevapladi`). **İki küme kesişemez.**

**Gerçek yer ölçüldü:** her iki vaka da `altin_geldi_cevapladi` (54) kovasında, ikisi de **0. sırada**
getirilmiş; yalnız biri sadakat kaybetmiş (0,75). ⇒ **B1 (7/80) ve B10 (16/80) el değmemiş kalıyor;
kırpmanın bedeli 2/80 ile dar bir şeride hapsolmuş.**

⚠️ Sınıflandırma **4 sınıflı** tutuldu, çünkü *"kırpıldı"* tek başına bir şey söylemiyor: 46 vaka
kırpılmış ama cevabın dayandığı cümle bağlamda duruyor. Tek sınıfa indirmek B5'i **23 kat**
şişirirdi.

## 3. B8 — yazım-hatası tolerans eğrisi (post-hoc, $0, **doğrulayıcı DONUK**)

Üç koşu birden süpürüldü:

```
koşu              eşik 1        eşik 2        eşik 3
s2-harness-k10    2 kurtarılan  2             2      · yanlış eşleme 0
h2b k=4           —  (KANUN_YOK yok)
h2b k=10          2 kurtarılan  2             2      · yanlış eşleme 0
```

🚨 **Ama eğri "eşik 3 güvenli" DEMİYOR — "bu veriyle karar verilemez" diyor.** Üç koşuda toplam
**4 `KANUN_YOK` atfı** var ve **hepsi aynı hatanın tekrarı**: `"Sanat Eseleri Kanunu"`
(FİKİR VE SANAT ESERLERİ KANUNU'ndan bir `R` düşmüş). **Toleransın risk tarafında sıfır gözlem
var.** ⇒ Tolerans **BENİMSENMEDİ** (ADR-0056 Karar 4); kapı **katı** kaldı.

🐞 **Betiğin ilk hâli sıfır üretiyordu ve sebebi bir ölçüm hatasıydı:** toleransı korpusun **tam
adlarına** uyguluyordu, oysa doğrulayıcı ≥2 sözcüklü **sonek** indeksiyle eşleştiriyor (model
resmî adın kısa hâlini yazıyor). `"Sanat Eseleri Kanunu"` → tam ada mesafe **11**, doğru soneke
mesafe **1**. Sonek uzayına taşındı. Ek koruma: tek sözcüklü soneke inilmiyor —
`mesafe("KANUNU","İŞ KANUNU") = 3`, eşik 3'te yüzlerce kanuna eşleşirdi.

⭐ **Hatanın üç koşuda da aynen tekrarlaması** onu rastlantı değil, modelin **tekrarlanabilir bir
transkripsiyon tiki** yapıyor — dolayısıyla çaresi de tolerans değil, dar ve hedefli olabilir.

## 4. D1 — B-i deneyi (kaynak-yeterliliği önsözü)

*(bu bölüm koşu bitince doldurulacak)*

## Ders

*(bu bölüm D1 sonrası yazılacak)*

## Açık kalanlar

*(bu bölüm D1 sonrası yazılacak)*
