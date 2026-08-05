# #53 — S3: ayırt-edicilik etiketi (borç B2) · ADR-0054/K4'ün kör turu

**Tarih:** 2026-08-05 · **Sprint:** [`sprint3-part1.md`](../../../sprint3-part1.md) **S3**
**Hakem:** `gpt-4o-mini` · kapı OpenRouter · `LLM_PROVIDER_ORDER=OpenAI` pinli · `temperature=0`
**Çıktı:** `outputs/eval/s3-ayirt-edicilik/` · **Betik:** `scripts/ayirt_edicilik_etiketle.py`

> ⛔ **BU BÖLÜM ETİKETLEME KOŞULMADAN ÖNCE YAZILDI** — ADR-0054/K4'ün açık şartı:
> *"Hakem istemi ADR'ye ve `research_log`'a etiketleme koşulmadan önce yazılır."*
> Aşağıdaki istem, koşudan sonra **değiştirilmedi**; sonuç bölümü ayrı ve altında.

## Neden bu tur var

`recall@5` = 0,750 sayısı **retriever'ın değil bu kümenin** tavanı olabilir (tuzak 7.4,
[#49](2026-08-04-s3a-on-prob.md)). `core_hard.jsonl` altın madde elde tutularak üretildi;
soruların bir kısmı tek başına hangi kanuna ait olduğunu söylemiyor. Küme **değiştirilmiyor**
(sayı görüldükten sonra küme değiştirmek *"cilaladılar"* diye okunur — tuzak 6.9'un veri
tarafı); yerine etiket ekleniyor ve sayılar **iki alt kümede ayrı** raporlanıyor.

## Ön-kayıtlı ölçüt — ADR-0054/K4'ten birebir

> *Soru tek başına okunduğunda, hangi kanun/konu alanına ait olduğu anlaşılıyor mu?
> (Bir hukukçu soruyu görüp 1-2 kanuna daraltabiliyorsa **EVET**.)*

## Ön-kayıtlı hakem istemi (birebir)

```
[system]
Sen Türk hukukunda deneyimli bir hukukçusun. Sana YALNIZCA bir soru metni verilecek. Sorunun
cevabını vermen istenmiyor; sorunun kendisi hakkında tek bir yargıda bulunacaksın.

ÖLÇÜT: Soru tek başına okunduğunda, hangi kanun/konu alanına ait olduğu anlaşılıyor mu?
(Bir hukukçu soruyu görüp 1-2 kanuna daraltabiliyorsa EVET.)

Kurallar:
- Soruda kanun adı, kurum adı ya da alana özgü terim geçiyorsa (ör. 'kıdem tazminatı',
  'tutuklama', 'kira sözleşmesi') daraltma mümkündür → EVET.
- Soru genel bir usul cümlesiyse ve konusu belirtilmemişse (ör. 'Başvurum kabul edilirse ne
  olur?', 'Süresi ne kadardır?') daraltma mümkün değildir → HAYIR.
- Kararını yalnız soru metnine dayandır. Tahmin ettiğin bir bağlam varsayma.

Yanıtı SADECE şu JSON ile ver: {"ayirt_edici": true|false, "alan": "<daraltabildiğin
kanun/alan, en fazla 2 tane; daraltamıyorsan boş string>", "gerekce": "<tek cümle>"}

[user]
SORU:
{soru}
```

## 🚨 Körlük — nasıl sağlandı

Hakeme giden yük **tek argümanlı** bir fonksiyondan üretiliyor (`_istem(soru)`); altın madde,
`kanun_adi`, `kanun_no`, `madde_no` ve retriever'ın sonucu bu yükte **hiç bulunmuyor**. Yani
körlük bir söz değil, **çağrı imzasının kısıtı**.

Bu, tuzak **2.14**'ün tersi yönde uygulanması: orada `valid_trap` etiketi öznenin cevabıyla
**aynı çağrıda** istendiği için hakem cevaba çapalanmış ve etiket kalemin değil **öznenin**
özelliği olmuştu (aynı 80 kalemde 54/56/39). Burada etiket kalemin özelliği: bir kez, kör,
önbelleğe alınır, bütün koşular onu **okur**.

## ⚠️ Kaydedilen iki çekince

1. **Ölçülen büyüklük ön-kayıtlı değil.** Bu ekseni ölçme fikri, S3a'da kaçan soruları
   **görerek** doğdu. Ayrım korunuyor: **alet** sonuca göre ayarlanmadı (hakem kör, istem
   önceden yazılı, küme değişmedi) — ADR-0054'ün kaydettiği çekincenin aynısı.
2. **Sıra sapması.** ADR-0054 bu turun harness-AÇIK ölçümünden **önce** koşulmasını
   yazmıştı; fiilen **sonra** koşuldu (borç B2). Körlük bundan etkilenmiyor (hakem zaten
   erişim sonucunu görmüyor), ama sapma gizlenmiyor.

---

## Sonuç — koşuldu 2026-08-05, hakem **$0,0069**

**Etiket dağılımı: 62 ayırt edici · 18 belirsiz (%22,5).** S3a'nın gözle yaptığı *"~%25'i
konusunu söylemiyor"* tahmini **tuttu**. Sağlayıcı tek eleman (`["OpenAI"]`) → yönlendirme
pinli (tuzak 2.7). Çıktı: `outputs/eval/s3-ayirt-edicilik/etiketler.jsonl` + `ozet.json`.

### Harness AÇIK (k=5, `tgta_v1`) sayıları iki alt kümede

> ⚠️ **2026-08-05, aynı gün düzeltildi.** Bu tablo ilk yazıldığında `harness_tablo.py`'nin
> **A1'i cevaplanan-only değil ham makro** olarak hesapladığı henüz bilinmiyordu
> ([#54](2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md) Bölüm 1, tuzak **2.16**). Aşağıdaki
> sayılar **düzeltilmiş** aletten; eski değerler üstü çizili olarak duruyor.

| eksen | **ayırt edici** (n=62) | **belirsiz** (n=18) | tüm küme (n=80) |
| :--- | ---: | ---: | ---: |
| `recall@1` | 0,5323 | 0,1667 | 0,4500 |
| `recall@3` | 0,7419 | 0,3333 | 0,6500 |
| **`recall@5`** | **0,8226** | **0,5000** | **0,7500** |
| coverage | 0,6935 | **0,9444** | 0,7500 |
| A1 (cevaplanan-only) | ~~0,8741~~ **0,8651** | **0,4909** | ~~0,7823~~ **0,7591** |
| A1 · altın getirilen | ~~0,9454~~ **0,9336** | ~~0,8796~~ **0,8796** | ~~0,9344~~ **0,9230** |
| **kütle** | ~~%60,6~~ **%60,0** | **%46,4** | ~~%58,7~~ **%56,9** |

Düzeltme okumaları **değiştirmedi** — iki alt küme arasındaki ayrışma aynı büyüklükte kaldı.

### Okuma 1 — tuzak 7.4 sayıyla doğrulandı

`recall@5` iki alt küme arasında **32,3 puan** ayrışıyor (0,8226 ↔ 0,5000). Yani
*"`recall@5` = 0,750"* retriever kabiliyetinin değil, **kümenin kompozisyonunun** sayısı.
Ayırt edici sorularda retriever k=5'te maddeyi **%82** buluyor. Bundan sonra hiçbir harness
sayısı bu ayrım yapılmadan raporlanmaz.

### Okuma 2 — ⭐⭐ BEKLENMEDİK: çekinme **ters** yönde çalışıyor

Erişim ↔ davranış çaprazı, alt kümelere ayrılınca:

```
                        altın geldi   altın geldi   altın GELMEDİ   altın GELMEDİ
                        → cevapladı   → çekindi     → CEVAPLADI     → çekindi
AYIRT EDİCİ (n=62)          37            14              6              5
BELİRSİZ    (n=18)           9             0              8              1
```

| alt küme | erişim başarısı (`recall@5`) | model çekinme oranı |
| :--- | ---: | ---: |
| ayırt edici | **0,8226** | **19/62 = %30,6** |
| belirsiz | **0,5000** | **1/18 = %5,6** |

**Model, erişimin en çok başarısız olduğu sorularda en az çekiniyor.** Güvenli bir sistemde
bunun tersi olmalıydı. İki uç birlikte okunmalı:

- **Belirsiz tarafta yetersiz-red:** 18 sorunun **17'si** cevaplanıyor, 9'unda altın madde
  bağlamda **yok**. Bu 8 vaka, B1'in ("gerçek ama soruya uymayan madde") **14 vakasının
  8'i** — yani B1 kümenin yalnız **%22,5'inde yoğunlaşmış**.
- **Ayırt edici tarafta aşırı-red:** 14 soruda altın madde **bağlamda olmasına rağmen**
  çekinilmiş. Coverage kaybının bu yarısı erişimden değil **modelden** geliyor.

**Mekanizma tahmini (sınanmadı):** belirsiz bir soru (*"Mahkeme ne zaman davayı sona
erdirir?"*) konusal olarak makul görünen bir madde getirir ve model onu cevaplar; ayırt edici
bir soruda retriever ıskaladığında getirilen bağlam **açıkça alakasızdır** ve model çekinir.
Yani çekinme sinyali bağlamın **konusal uyumundan** geliyor, **soruyu cevaplamaya yeterli
olup olmadığından** değil. → doğrudan **S4**'ün (isabet denetimi) tasarım girdisi.

### ⭐ Okuma 2-b — aynı gün: **`k=10` bu tersliği büyük ölçüde DÜZELTİYOR** ([#54](2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md))

| coverage | k=5 | k=10 |
| :--- | ---: | ---: |
| ayırt edici (n=62) | 0,6935 | **0,7903** |
| belirsiz (n=18) | **0,9444** | **0,7222** |
| sıralama | ❌ **ters** (belirsizde +25,1 puan fazla cevaplıyor) | ✅ **doğru** (ayırt edicide +6,8 puan) |

Belirsiz alt kümede çekinme **1/18 → 5/18**'e çıktı. Yani model, on parça bağlamda hiçbiri
soruyu karşılamayınca **fark edebiliyor** — beş parçada fark edemiyordu. Bu, yukarıdaki
mekanizma tahminini **destekliyor**: sinyal *"yeterlilik"* değil ama daha geniş bir aday
kümesi yeterlilik yargısını **kolaylaştırıyor**. Terslik tamamen kapanmadı, **yön düzeldi**.

### Okuma 3 — altın getirildiğinde model her iki kümede de sadık

A1 · altın getirilen: **0,9454** (ayırt edici) ↔ **0,8796** (belirsiz). İkisi de yüksek.
#51'in *"darboğaz model değil erişim"* okuması alt küme kırılımında da **ayakta**.

## Paper eşlemesi

**Methodology:** erişim sayılarının soru-belirginliğine göre ayrıştırılması; kör etiketleme
protokolü. **Negatif/sınır bulgusu:** çekinme kalibrasyonu erişim başarısıyla **ters**
korele — abstention'ın *"kaynak yeterli mi"* değil *"kaynak konusal mı"* sinyaline
dayandığının ilk kanıtı. **Limitations:** `recall@k` mutlak sayı olarak raporlanamaz.
