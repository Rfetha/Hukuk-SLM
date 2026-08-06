# ADR-0055 — İsabet denetimi hangi eksende kurulur (borç B1) · **yeterlilik sinyali**

**Tarih:** 2026-08-05 · **Durum:** ✅ kabul (tasarım; kod açılmadı) · **Sprint:** [`sprint3-part1.md`](../_arsiv/sprint3-part1.md) **S4**
**İlgili:** [ADR-0054](0054-harness-tasarim-kararlari-k2-k5.md) · [#53](../record/research_log/2026-08-05-ayirt-edicilik-etiketi.md) · [#54](../record/research_log/2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md)

> ⚠️ **[ADR-0058](0058-b-i-kaynak-yeterliligi-onsozu-benimsendi.md) (2026-08-06) tadil etti** —
> B-i artık ablasyon değil, ana protokol.

## Bağlam — ölçülmüş açık

Harness AÇIK (k=10) ölçümünden sonra kalan kayıp **iki uçtan** geliyor ve ikisi de
*"kaynak var mı"* değil *"kaynak bu soruyu karşılıyor mu"* sorusunda düğümleniyor:

| açık | büyüklük | k ile değişiyor mu | kaynağı |
| :--- | ---: | :--- | :--- |
| **B1** — atıf gerçek, doğrulanır, kapıdan geçer, **soruya uymaz** | **7/80** | ✅ 14→7 (k=5→10) | erişim ıskalayınca model *başka gerçek* maddeden cevaplıyor |
| **aşırı-red** — altın **bağlamdayken** çekinme | **15/80** | ❌ 14→15, **bağımsız** | model |

⭐ **İkisi aynı madalyonun iki yüzü.** Biri yetersiz kaynakta **cevaplıyor**, diğeri yeterli
kaynakta **çekiniyor**. [#53](../record/research_log/2026-08-05-ayirt-edicilik-etiketi.md)
mekanizmayı ölçtü: çekinme sinyali bağlamın **konusal uyumundan** geliyor, **soruyu
cevaplamaya yeterliliğinden** değil — model, erişimin en çok battığı belirsiz sorularda
**en az** çekiniyor (k=5'te %5,6 ↔ %30,6). `k=10` yönü düzeltiyor ama kapatmıyor.

Yani tek bir eksik sinyal iki hatayı birden üretiyor: **kaynak-yeterliliği**.

## Değerlendirilen seçenekler

### ❌ A — Cevap ↔ kaynak örtüşme denetimi (post-hoc, deterministik) — **REDDEDİLDİ**

Model X maddesine atıf yapıp cevap verdikten sonra, cevabın X'in metniyle desteklenip
desteklenmediği ölçülür (cümle-düzeyi NLI ya da gömme benzerliği); eşiğin altındaysa reddedilir.

**Neden çekici:** deterministik, çıkarım anında hakem parası yok, "atıf X ama içerik
parametrik bellekten" vakasını yakalar.

**REJECTED — B1'in tam da çekirdek vakasında kör.** B1'de model *başka bir gerçek maddeden*
cevaplıyor: o maddeye atıf yapıyor **ve cevabı gerçekten o maddede temelli**. Yani
cevap↔kaynak örtüşmesi **yüksek** çıkar. Denetim, yakalaması gereken 7 vakada tam not verir.
Ayrıca uydurma madde numarası **0/120 ölçüldü**, yani bu denetimin yakalayacağı sınıf
korpusta zaten boş. *Ölçülmüş boş bir sınıfa deterministik denetim yazmak, S2'de sınıf A'yı
elemekle aynı hata olurdu.*

### ✅ B — Soru ↔ kaynak **yeterlilik** sinyali (cevap ÖNCESİ) — **SEÇİLDİ**

Cevap üretilmeden önce, getirilen bağlamın soruyu karşılamaya **yeterli** olup olmadığı
puanlanır. Yetersizse model cevaplamaz.

**Neden bu:** **tek sinyal iki hatayı birden** hedefliyor — B1 *"yetersizken cevapladı"*,
aşırı-red *"yeterliyken çekindi"*. A ve C yalnız bir yönü tutuyor. Ayrıca #53'ün ölçtüğü
mekanizmanın **doğrudan karşılığı**: bugün karar *konusal uyuma* bakıyor, olması gereken
*yeterlilik*.

⚠️ **Bilinen risk, ön-kayda geçiyor:** yeterlilik yargısı **aynı modele** sorulursa aynı
bozuk sezgi geri gelebilir — model *"konusal olarak uyuyor, demek ki yeterli"* der. Bu
yüzden sinyal **üç ayrı kaynaktan** alınabilir ve hangisinin çalıştığı **ölçülür**:

| kaynak | maliyet | risk |
| :--- | :--- | :--- |
| **B-i** modelin kendisi, `--sufficiency-preamble` ile *(bayrak `gen_eval_grounded.py`'de **zaten var**)* | **$0**, ek çıkarım yok | aynı bozuk sezginin dönmesi |
| **B-ii** çapraz-kodlayıcı (cross-encoder) yeniden-puanlama | CPU, harness içinde | ayrı model, ayrı kalibrasyon |
| **B-iii** hakem | para + gecikme | ürün akışına hakem sokmak |

**İlk deney B-i'dir, çünkü bedeli sıfır ve red şıkkı nettir:** ön-söz çekinme
kalibrasyonunun **yönünü** düzeltmiyorsa (belirsiz alt kümede çekinme ayırt ediciyi
geçmiyorsa) B-i düşer ve B-ii'ye geçilir.

### 🔁 C — İkinci geçiş yeniden-sıralama — **AYRI İŞ, REDDEDİLMEDİ**

Getirilen `k` parça modele gösterilmeden önce çapraz-kodlayıcıyla yeniden sıralanır, ilk
`n < k` gösterilir.

**Neden ayrı tutuluyor:** bu bir **isabet denetimi değil, erişim iyileştirmesidir** — hüküm
üretmez. Ama [#54](../record/research_log/2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md)'ün
ölçtüğü **dikkat dağılmasına** (altın bağlamdayken A1 **0,9230 → 0,8426**) doğrudan çare
olabilir: `k`'yı recall için yüksek tutup modele giden bağlamı kısaltır. **Kendi hedefiyle,
kendi ön-kayıtlı tahminiyle ayrıca ölçülür** — B ile aynı turda ölçülürse hangisinin
kazandırdığı ayrılamaz (ADR-0017'nin *"aynı anda iki şey değişmez"* kuralı).

### 🔁 D — Soru-belirginliği kapısı — **ERTELENDİ**

[#53](../record/research_log/2026-08-05-ayirt-edicilik-etiketi.md)'ün kör etiketi ürüne
taşınır: soru tek başına alanını söylemiyorsa cevap yerine **açıklama istenir**.

**Neden ertelendi:** ürün davranışı değişikliği (UX kararı, teknik karar değil) ve kümenin
yalnız **%22,5'ini** kapsıyor. Ama B'nin ölçümünde **alt küme kırılımı zorunlu** —
yeterlilik sinyalinin belirsiz sorularda mı yoksa ayırt edici sorularda mı çalıştığı,
sinyalin ne olduğunu söyler.

## Karar

**İsabet denetimi, cevap-sonrası örtüşme ekseninde değil, cevap-öncesi
KAYNAK-YETERLİLİĞİ ekseninde kurulur (B).** İlk deney bedeli sıfır olan **B-i**'dir.

**Ön-kayıtlı kabul ölçütü — sayı görülmeden yazıldı:**

> 🔁 **ÇIPASI TADİL EDİLDİ 2026-08-05 — [ADR-0056](0056-m2b-harness-acik-protokolu-ve-0055-cipasi.md) Karar 3.**
> Aşağıdaki `%59,5` **S2-öncesi korpustan**; B-i **S2 korpusunda** koşacak. Güncel çıpa
> **%61,3**. Eşiğin kendisi (*"kütle ARTAR"*), yön ölçütü ve red şıkkı **değişmedi** — ve
> eşik böylece **zorlaştı**, gevşemedi. Özgün metin üzerine yazılmadı.

```
BAŞARILI  : kütle ARTAR  (bugünkü resmî: k=10 · %59,5 → 🔁 GÜNCEL ÇIPA: %61,3)
            VE çekinme sıralaması DOĞRU yönde: belirsiz alt kümede çekinme
            oranı ≥ ayırt edici alt kümede  (bugün k=10'da hâlâ ters yönde değil
            ama fark kapanmadı — #53 Okuma 2-b)
KISMİ     : kütle sabit ± 1 puan, ama sıralama düzeliyor → sinyal doğru, eşik yanlış
BAŞARISIZ : kütle DÜŞER ya da sıralama bozulur → B-i düşer, B-ii'ye geçilir
```

⚠️ **A1 cevaplanan-only raporlanır ve `rescore_answered` ile çapraz kontrol edilir**
(tuzak **2.16** — bu kapının hükmü bir kez zaten metrik hatasıyla tersine döndü).

## Sonuçlar

- **Kod bu ADR'den önce yazılmadı** — sprint3 S4'ün açık şartı.
- B'nin üç kaynağı bir **sıra**dır, bir menü değil: B-i düşmeden B-ii'ye geçilmez, yoksa
  hangi sinyalin işe yaradığı ölçülemez.
- **C ayrı bir tur olarak ROADMAP'e girer** — dikkat dağılmasının ölçülmüş çaresi olduğu
  için değeri yüksek, ama B ile karıştırılırsa ikisi de yorumlanamaz.
- **Aşırı-red'in model tarafı bu ADR'nin kapsamı dışında:** 15/80'in bir kısmı harness'la
  değil **eğitimle** kapanır (borç **B4**, `τ_a` seyreltme). Bu ADR harness tarafını
  kapsıyor; eğitim tarafı ayrı bir sprintin konusu.
