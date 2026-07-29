# ADR-0049 — Sprint 2'nin kalan beş kararı kilitlendi (eşik türetme · önbellek hakemi · M2b tabanı · smoke · kabul tasarımı)

**Statü:** Yürürlükte · **Tarih:** 2026-07-30
**Otorite belge:** `sprint2.md` · **Yöntem:** yapılandırılmış karar görüşmesi (`/grill-me`), beş dal tek tek kapatıldı
**Tamamlar:** [ADR-0048](0048-cevaba-kor-tuzak-gecerliligi.md) (bu ADR onun uygulama kararlarıdır) ·
[ADR-0045](0045-ara-kapi-merge-onarim-kontrolu.md) m.2 · [ADR-0046](0046-cp2-kabul-olcutu-hakem-ve-havuz-on-elemesi.md) m.1 ·
[ADR-0047](0047-cp2-hedef-750-modal-hasat.md)
**Kanıt:** `research_log` [#45](../record/research_log/2026-07-30-cp2a-hakem-capalanmasi.md) ·
`outputs/eval/cp2-on-eleme/KUNYE.json`

> ## ⚠️ ÖN-KAYIT ŞERHİ
> Beş karar da **`τ_a` eğitilmemişken**, hiçbir merge hücresi üretilmemişken, hiçbir hasat
> başlamamışken ve **ARA KAPI okunmamışken** verildi. Karar 1 bir eşiği **hareket ettiriyor** ve
> yönü **bizim lehimize** — bu yüzden savunması aşağıda ayrıca yazıldı.

---

## Kilitlenen ölçülmüş olgu (bu kararların dayanağı)

Üç modda da eval bağlamı **özneler arası bit-birebir aynı** (doğrulandı: m2 70/70 · m2b 80/80 ·
m3 80/80, 0 fark). Yani `valid_trap` saf bir **kalem özelliğidir** ve ADR-0048'in düzeltmesi
temiz uygular. Bu, yeniden puanlamanın kapsamını **21 koşudan 150 kaleme** indirir.

---

## Karar 1 — ARA KAPI eşikleri **düzeltilmiş cevaba-kör çıpadan yeniden türetilir**

**Ön-kayıtlı olan FORMÜL, sayı değil.** `sprint2.md` bunu zaten yazmıştı (*"Sayılar CP0.9'dan geldi
— formül ön-kayıtlıydı, sayı değil"*) ve **emsal var**: eşikler thinking-off → bütçeli geçişinde
0.75/0.876 → **0.934/0.888** olarak bir kez taşındı ve bu meşru sayıldı.

```
M2 eşiği     = düzeltilmiş base M2 + 12 puan
M1 A1 muhafızı = 0.90 × base M1 A1        ← DEĞİŞMEZ (groundedness; valid_trap'e dokunmaz)
M2b onarım   = 0.90 × düzeltilmiş base M2b
```

**Beklenen yön ve dürüst şerh.** Mevcut çıpa `48/59 = 0.814`; cevaba-kör paydayla geçerli sayısı
59'dan **yukarı** çıkacağı için çıpa **~0.79'a** inecek → eşik **0.934 → ~0.91**. Yani düzeltme
kapıyı `τ_a` için **kolaylaştırıyor.** Savunma üç maddeli:

1. `τ_a` **henüz yok** — sonucu bilmeden düzeltiyoruz, gamelenemez.
2. Aynı düzeltme **base'e, rakibe ve her hücreye** aynı biçimde uygulanıyor; kıyas simetrisi korunur.
3. Bozuk bir ölçümden türeyen eşiği korumak *ön-kayıtlılığı korumak* değil, **hatayı korumaktır**.

**Eski eşiklere karşı sonuç da raporlanır** — hangi sayının hangi paydayla üretildiği görünür kalır.

## Karar 2 — 150 kalemlik cevaba-kör `valid_trap` önbelleğini **gpt-4o** kurar

| | |
| :--- | :--- |
| kapsam | m2 **70** kalem `(soru, referans)` · m2b **80** kalem `(soru, context_shown)` · m3 **0** — tanım gereği 80/80 (ADR-0048 m.2) |
| hakem | **gpt-4o**, cevaba **kör**, temperature 0, seed 3407, clip 900 |
| maliyet | ~**$0,29**, **bir kez** — commit edilir, sonsuza kadar okunur |
| besledikleri | 3 mevcut özne · `τ_a` · Taban A/B · Sprint 3'ün 8 hücresi |

**Skorlama hakemi `gpt-4o-mini` olarak KALIR** — rejim değişmezi bozulmuyor. Gerekçe:
`valid_trap` bir **kürasyon etiketi** (veri özelliği), puanlama yargısı değil. Aile dışlaması
(ADR-0032) tetiklenmiyor: o kural **özne notlamayla** ilgili, veri kürasyonuyla değil.

`verdict` (ABSTAIN/FABRICATE) **yeniden hesaplanmaz** — o cevap hakkındadır, cevaba bağlı olması
**meşrudur**, kirlenme yok. Yani yeniden puanlama = önbellek + **saf aritmetik ($0)**.

**Sapma kayda geçer:** bir metriğin paydası pinlenmiş hakemden farklı bir hakemle üretiliyor.
Önbellek dosyası commit edilir, her etiket denetlenebilir.

## Karar 3 — M2b kapı olarak **kalır**; taban **40/80**

M2b'nin kurgusal zayıflığı (distractor'lar aynı kanundan) merge onarım kontrolünü bozmaz, çünkü
kontrol **aynı kalemler üzerinde bir karşılaştırmadır** (`τ_g` 0.607 ↔ base 0.986): zayıflık
ikisini **eşit** etkiler → **seviyeyi** bozar, **açığı** bozmaz.

> **Ön-kayıtlı kural:** cevaba-kör geçerli tuzak sayısı **40/80'in (%50) altına** düşerse mod,
> tasarlandığı mod olmaktan çıkar (eval-ayna ilkesi kırılır) → merge onarım kontrolü
> **tanımlayıcı** olarak raporlanır ve **ARA KAPI'nın 2. gözlemi olmaktan çıkar.**

## Karar 4 — Boru hattı **5 adımlık mekanik smoke** ile sınanır (tam pilot CP3 DEĞİL)

`τ_a` yolu (`--fresh-adapter` → norm-dengeli TIES → GGUF → runtime) **hiç koşmadı** ve Sprint 3'ün
**8 hücresi** o yolun üzerinde. Sınama: `τ_a`'yı **5 adım** eğit → `τ_g+τ_a` merge → GGUF →
**3 cevap** üret. ~**$0,15**.

**Neden tam pilot değil:** tam pilot okunabilir bir performans sayısı üretir ve eşikler henüz
yeniden türetilmemişken o sayı **çıpalama riski** taşır. Mekanik smoke bu riski **yapısal olarak**
taşımaz — ölçtüğü şey *"çalışıyor mu"*, *"iyi mi"* değil.

## Karar 5 — CP2-c kabul tasarımı: **B** (mini ön-filtre → gpt-4o teyit → gpt-4o kör geçerlilik)

```
üretim (7.500)
  → regex ön-filtre                       bedava, ~%30 geçer
  → gpt-4o-mini verdict                   ~2.250 × $0,000117 = $0,26
  → gpt-4o verdict TEYİT (kabul edilende) ~900 × $0,0019     = $1,71
  → gpt-4o KÖR geçerlilik damgası         ~900 × $0,0019     = $1,71
                                          ────────────────────────────
                                          ham ~900 → temiz ~750 · $3,68
```

**Reddedilen A ($2,0):** mini↔4o verdict uyumu 0,857 ve ayrışan 3 kalemin **2'si
mini=FABRICATE / 4o=ABSTAIN** — mini, 4o'nun reddedeceğini kabul ediyor. Artık kirlilik **~%9,5**
ve kör geçerlilik adımı bunu **yakalamıyor** (ayrışma verdict'te). Bir gündür düzelttiğimiz hata
sınıfının aynısını %9,5 oranında havuza sokmak, $1,7 tasarruf için kötü bir takas.

**Reddedilen C ($6,0):** aynı sonucu $2,3 fazlaya alıyor; kalan bütçede CP4-CP5 ~$12 istiyor.

**Yan kazanç:** `chosen` tarafı aynı kör damgayla **bedava** süzülür (ADR-0048 m.5'in gereğini
ayrı koşu olmadan karşılar).

---

## Sonuçlar

- ✅ Kapsam **21 koşu → 150 kalem**: bağlamın özneler arası aynı olduğu ölçüldü.
- ✅ ARA KAPI **okunabilir** hâle geliyor; eşik `τ_a` yokken, formülden, düzeltilmiş çıpayla türer.
- ✅ CP2-b **iptal** (ADR-0048 m.4) → akış ve bütçe yeniden yazıldı.
- ⚠️ **Eşik hareket ediyor ve yönü lehimize** — üç maddeli savunma yukarıda, eski eşiğe karşı
  sonuç da raporlanacak. **Limitations'a girer.**
- ⚠️ Paydanın hakemi (gpt-4o) skorlama hakeminden (gpt-4o-mini) **farklı** — kayda geçti, önbellek
  commit edilir.
- ⚠️ M2b'nin 40/80 tabanı **ön-kayıtlı**; altına düşerse ADR-0045'in 2. gözlemi tanımlayıcıya iner.
- ⏳ M1 A1 muhafızının (0.888) CP1'in yeni hakemiyle yeniden türetilmesi **ayrı** ve hâlâ açık —
  `valid_trap` onu etkilemiyor (groundedness ekseni), ama CP1'in istem değişikliği etkiliyor.
