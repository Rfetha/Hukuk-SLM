# ADR-0057 — Harness Rekabet Kapısı: **eşit sınav** ilkesi

- **Tarih:** 2026-08-05
- **Durum:** kabul edildi
- **Karar veren:** insan
- **Kaynak ölçüm:** [#51](../record/research_log/2026-08-04-harness-acik-ilk-olcum.md) · [#54](../record/research_log/2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md) · [#55](../record/research_log/2026-08-05-s2-yururluk-alani.md)
- **Tadil eder:** [ADR-0056](0056-m2b-harness-acik-protokolu-ve-0055-cipasi.md) Karar 1 — `h2b`'nin `k`'sı
- **Bağlar:** [`superpowers/plans/2026-08-05-olcum-bosluklari.md`](../superpowers/plans/2026-08-05-olcum-bosluklari.md) Görev 4 · 6

## Bağlam

İnsan bir ürün şartı koydu:

> **"Harness'ın rekabet edebileceği her yerde AÇIK hâli, KAPALI hâlinden önde olmalı —
> ve ikisi aynı zorlukta eşit sınava girmeli ki harness'ın farkı ortaya çıksın."**

Şart doğru ama **doğrudan uygulanamaz**, çünkü bugün AÇIK ↔ KAPALI çoğu eksende **aynı sınava
girmiyor**. Somut örnek, gerçek koşudan (`id` eşleştirilerek, aynı model, aynı rejim):

```
SORU: "Mahkeme benim lehime bir karar verirse ne olur?"
ALTIN: İCRA VE İFLAS KANUNU Madde 31

KAPALI  5 kaynak: İİK 29 · 32 · 31 ← ALTIN · 33 · 30     → model CEVAPLADI
AÇIK   10 kaynak: TMK 182 · CMK 42 · Denizde Zabt 122 ·  → altın YOK, model ÇEKİNDİ
                  Yangın-Yersarsıntısı · CMK 35 · ...
```

İki kusur birden görünüyor: **(a)** KAPALI altını kurgu gereği alıyor, AÇIK aramak zorunda —
bu bir yarış değil; **(b)** kaynak sayıları bile eşit değil (5 ↔ 10), ve fazla bağlamın
sadakate mal olduğu **ölçüldü** (A1 0,9230 → 0,8426). Bu şartlarda çıkan farkı *"harness'ın
farkı"* diye okumak mümkün değil.

## Karar — üç kademeli eşit-sınav sınıflandırması

Harness'ın **üç parçası eşit sınava aynı ölçüde elverişli değildir.** Kural bu ayrımın
üstüne kurulur.

### Kademe 1 — **TAM EŞİT SINAV**: atıf doğrulayıcı + red kapısı

Aynı sorular · aynı kaynaklar · **aynı cevaplar**. Değişen tek şey: cevap üretildikten
**sonra** doğrulayıcı ve kapı uygulanıyor mu.

⭐ **Burada sınav birebir aynıdır** — çünkü bu iki parça girdiye değil **çıktıya** dokunuyor.
Ölçüm eldeki `detail.jsonl` üzerinde **post-hoc**, bedeli **$0**, ve harness'ın katkısı
**saf** olarak izole edilir.

```
KURAL:  kapı/doğrulayıcı AÇIK  ≥  KAPALI     (aynı cevap kümesinde)
```

### Kademe 2 — **EŞLEŞMİŞ SINAV**: retriever

Retriever, tanımı gereği **sınavı değiştirir** — kaynakları o seçiyor. Bu yüzden "birebir
aynı sınav" **imkânsızdır**; sağlanabilecek en fazlası şudur ve **şart koşulur**:

```
(a) aynı sorular          — küme değişmez (ADR-0054 K4)
(b) aynı kaynak SAYISI    — bağlam bütçesi eşit
(c) aynı altın koşulu     — ya ikisinde de var, ya ikisinde de yok
(d) aynı rejim            — seed · kırpma · düşünce bütçesi · hakem
```

Geriye kalan tek fark **çeldiricileri kimin seçtiği**dir — ve o zaten **ölçülmek istenen
şeydir**. Eşitlenirse ölçüm yok olur.

```
KURAL:  ON  ≥  OFF + 0,3 puan
        (0,3 = hakemin ölçülmüş yeniden-koşum gürültü tabanı, #55 §9)
```

⚠️ **Ve artık zorluk KONTROL EDİLİR, varsayılmaz** *(insanın eklediği şart)*. Her iki kol için
**çeldirici zorluğu** ölçülüp tablonun yanına yazılır:

```
zorluk göstergesi = çeldiricilerin altınla AYNI KANUNDAN gelme oranı
                    + soru↔çeldirici sözcük örtüşmesi (medyan)
```

⭐ **İlk okuma şimdiden elde ve yönü şaşırtıcı:** `sample_distractors` KAPALI'nın
çeldiricilerini **kasten zor** seçiyor — aynı kanun, madde numarasına göre **en yakın
komşular** (`raft_pack.py:75-91`). Yukarıdaki örnekte 4/4'ü altının komşusu. Yani **KAPALI'nın
sınavı daha zordur**, ve AÇIK'ın `k=5`'te onu geçmiş olması (0,9230 > 0,9087) **daha
değerlidir**, daha az değil. Bu, kuralın lehimize eğrilmediğinin kanıtı olarak kayda geçer.

### Kademe 3 — **EŞİTLENEMEZ**: kural uygulanmaz

| eksen | neden eşitlenemez |
| :--- | :--- |
| **M1 manşet kütle** | KAPALI altını **kurgu gereği** alır → yarış değil, **TAVAN** |
| **M4** | oracle: yalnız altın verilir; retriever devreye girerse o artık M4 değildir |
| **M3** · **M5** | bağlamın **yokluğuyla** tanımlı — AÇIK karşılığı **çelişki** |
| **M2** | `trap.jsonl`'de altın korpusta **var**; retriever bulunca çekinme koşulu **kendini yok eder** |

Bu eksenler **raporlanmaya devam eder** ama **TAVAN/tanımsız** damgasıyla. *"AÇIK burada
geride"* cümlesi bu satırlar için **kurulmaz**.

## 🔒 Anti-gaming — kapının zorunlu eki

**Kapı yürürlükteyken KAPALI kolunun kurgusu DONDURULUR:** `--distractors 4`,
`sample_distractors`'ın komşu-öncelikli seçimi ve `core_hard`/`trap` havuzları değiştirilemez.

**Neden zorunlu:** *"AÇIK, KAPALI'yı geçsin"* şartını geçmenin **en ucuz yolu KAPALI'yı
kötüleştirmektir** — çeldiricileri kolaylaştırmak AÇIK'ı kendiliğinden öne geçirir ve
**hiçbir yerde hata çıkmaz**. Bu repoda tam bu sınıf (*sessiz yanlışlık*) beş kez ısırdı.
KAPALI kolu değişmesi gerekirse **kapı önce askıya alınır**, iki kol yeniden türetilir, sonra
kapı açılır.

## Sonuçlar — bugün nitelenen eksenler ve durumları

| kademe | eksen | kaynak | OFF | ON | hüküm |
| :---: | :--- | :---: | ---: | ---: | :--- |
| 2 | **A1 · altın getirilen** | 5 ↔ 5 | 0,9087 | **0,9230** | ✅ **GEÇİYOR** *(k=5)* |
| 2 | **M2b Rej** | 4 ↔ 4 | **0,766** ᴷ³ ~~0,8770~~ | 0,735 (önsözsüz) · **0,809** (önsözlü) | ✅ **ölçüldü** — `h2b@k=4`, [#57](../record/research_log/2026-08-06-cekinme-aleti-onarimi.md) |
| 1 | kapı + doğrulayıcı katkısı | aynı cevaplar | — | ? | ⏸️ **ölçülecek**, post-hoc |

### ADR-0056 Karar 1'in tadili

ADR-0056 `h2b`'yi **`k=10`**'da tanımladı ve gerekçesi *"bağlam uzunluğu `h1` ile aynı
kalsın"* idi — yani **ürüne** eşitledi. Bu **yanlış çıpaya** eşitlemektir: `m2b`'nin
KAPALI hâli **4 kaynak** gösteriyor (`--distractors 4 --no-gold` → altın eklenmiyor).
10 ↔ 4 kıyasından çıkacak fark *"kapı mı yetersiz"* ile *"6 fazla madde mi"* arasında
**ayrılamaz**.

**Düzeltme:** `h2b` **iki `k`'da birden** koşulur.

```
h2b @k=4    ← EŞLEŞMİŞ sınav.  Kapının hükmü YALNIZ buradan okunur
h2b @k=10   ← ürünün gerçek ayarı. Bilgi olarak yanında durur, hüküm vermez
```

Bedeli **~$0,04** (bir üretim + bir hakem çağrısı). Bonus: aradaki fark, `k` büyütmenin
bedelini **çekinme ekseninde** de ölçer — bugüne dek yalnız **sadakat** ekseninde ölçülmüştü.

### Kabul edilen bedeller

- ⚠️ **Kademe 2'de "birebir aynı sınav" ASLA sağlanamaz** ve bu gizlenmiyor: çeldiricileri
  kimin seçtiği, ölçülmek istenen şeyin **ta kendisidir**. Eşitlenirse ölçüm yok olur.
  Sağlanan şey *"her şey eşit, tek değişken tedavi"*dir — daha fazlası değil.
- ⚠️ **Ürünün satıldığı ayar (`k=10`) Kademe 2 kapısını A1 ekseninde GEÇMİYOR** (0,8616 <
  0,9087). Bu bir çelişki değil **bilinçli takas**: `k=10` seçildi çünkü kütle daha yüksek
  (%56,9 → %59,5) — **sadakat verilip recall alındı**. Kapının ilk işi bu takası
  **görünür ve sayılı** kılmak oldu.
- ⚠️ Zorluk göstergesi bir **gösterge**dir, kanıt değil: iki çeldirici kümesinin
  "eşit zorlukta" olduğunu **ispatlamaz**, yalnız bariz bir eğrilik varsa **yakalar**.
