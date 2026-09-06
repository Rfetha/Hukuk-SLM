# ADR-0052 — Norm dengelemenin hükmü tersine: ana sonuç **ham TIES**

- **Tarih:** 2026-08-03
- **Durum:** kabul edildi
- **Tadil eder:** [ADR-0036](0036-tau-norm-asimetrisi-ve-norm-dengeli-merge.md) (metnine dokunulmadı, hükmü değişti)
- **Kaynak ölçüm:** [research_log #48 §22-§24](../record/research_log/2026-08-02-cp2c-modal-koprusu.md)

## Bağlam

ADR-0036, `τ` vektörlerinin merge öncesi **birim norma indirilmesini** şart koşuyordu.
Gerekçesi: kollar çok farklı ölçekte eğitiliyor, TIES kütle-ağırlıklı çalışıyor, bu yüzden
küçük-normlu kol **tam da becerilerin çatıştığı parametrelerde silinir** ve *"çekinme
korunmadı"* sonucu bir **ölçek artefaktından** okunur.

Bu gerekçenin **ölçülmüş** kısmı ile **varsayılmış** kısmı vardı:

| öncül | o gün | bugün |
| :--- | :--- | :--- |
| kollar farklı ölçekte | varsayım | ✅ **ölçüldü**: ‖τ_g‖ 10,47 ↔ ‖τ_a‖ 1,18 = **8,87×** |
| TIES kütle-ağırlıklı | doğru | ✅ doğru — ama **ayrık ortalamada**, işaret seçiminde değil |
| küçük kol **silinir** | **varsayım** | ❌ **çürütüldü** |
| ⇒ dengeleme gerekli | çıkarım | ❌ **tersi ölçüldü** |

## Ölçüm

Üç varyant, aynı kollar, aynı rejim, DEV havuzu, tek değişken:

```
varyant     norm katsayıları      geri ölçek   M1 kütle   M2 Rej   M2b Rej   kesik
ortalama    tg 0,096 · ta 0,847      5,826         —         —        —      %5,2 🛑
min         tg 0,096 · ta 0,847      1,181       53,4%     0,934    0,987    %0,6
ham         tg 1,0   · ta 1,0        1,000       71,6%     0,893    0,877    %0,4
τ_g (kıyas) —                        —           71,4%     0,873    0,607
τ_a (kıyas) —                        —           41,2%     0,984    0,987

🚨 ᴷ⁴ M2 Rej sütunu da EMEKLİ BİRİMDE (payda özneye bağlıydı → 66'ya eşitlendi, #58/KARAR-4):
   min 0,934 → 0,909 · ham 0,893 → 0,833 · τ_g 0,873 → 0,833 · τ_a 0,984 → 0,955
```

**Ham TIES `τ_a`'yı silmedi:** M2b 0,607 → **0,877** ᴷ³ (çöküşün %71'i onarıldı
🚨 ᴷ³ türetmesi: `(0,766−0,506)/(0,961−0,506)` = **%57**, ~~%71~~), üstelik
> ᴷ³ **PAYDA ONARILDI 2026-08-06 — bu ADR'nin sayıları eski aletin birimindedir.** `valid_trap`
> paydası hakemin **modelin cevabını görerek** verdiği bir karardı; aynı sınav her modelde farklı
> payda veriyordu. Yeniden puanlanmış değerler ([#57](../record/research_log/2026-08-06-cekinme-aleti-onarimi.md)):
> `τ_g` **0,607 → 0,506** · ham TIES **0,877 → 0,766** · `τ_a` **0,987 → 0,987 (değişmedi)**.
> **Sıçrama +0,26 ile aynı kaldı → BU ADR'NİN HÜKMÜ AYAKTA.** Metindeki eski sayılar
> bilerek silinmedi (denetim izi).
>
> 🚨 **EK DAMGA 2026-08-06 (kusur Ö3-d) — bu bloğun kapsamı EKSİKTİ.** ᴷ³ yalnız **M2b**
> sütununu kapsıyordu; **M2 Rej** sütunu ayrı bir onarımdan (**ᴷ⁴**, M2 paydası 66'ya eşitlendi,
> [#58](../record/research_log/2026-08-06-payda-tekillesmesi.md) · KARAR-4) geçmiş ve damgasız
> kalmıştı. Çeviri ölçüm bloğuna yazıldı.
> Ayrıca **türetilmiş nicelik** damgalandı: onarım oranı ~~%71~~ → **%57** (girdiler yerinde
> güncellenmiş, onlardan türeyen oran güncellenmemişti — bu turun kendi kuralının ihlali).
> ⭐ Yürürlükteki çıpa: [`kollar.md`](../record/kollar.md).


grounding **tamamen** korunarak (71,4% → 71,6%).

**Norm dengeleme ise `τ_g`'yi ezdi:** grounding 71,4% → 53,4%. Yüksek geri ölçekte
(`ortalama`) model **dejenere** oldu (tekrarlama döngüleri, koşu geçersiz).

## Karar

1. **Ana sonuç `--no-norm-balance` (ham TIES) ile üretilir.** Norm-dengeli varyant
   **ablasyon** olarak raporlanır — ADR-0036'nın atadığı rollerin **yer değiştirmesi**.
2. **ADR-0036 silinmez, tadil edilir.** Gerekçesi (asimetri gerçek ve ölçüldü) ayakta;
   çürütülen şey **çıkarımıdır** ("silinir ⇒ dengele"). ADR-0050 kalıbı: *sonucu gördükten
   sonra EŞİK değil ALET düzeltilir* — burada düzelen, ölçek artefaktı hipotezinin kendisi.
3. **`‖τ‖` koşulsuz ölçülmeye devam eder** (ADR-0036'nın bu maddesi aynen korunur). Asimetri
   raporun bir bulgusu; sadece ondan çıkarılan reçete değişti.
4. **Geri-ölçek kuralı artık açık parametre:** `merge_ties.py --geri-olcek
   {ortalama|min|max|<kol>}`, künyeye `geri_olcek_kurali` alanı yazılır.
5. **Merge yapılandırması DEV'de seçildi** — makalede böyle beyan edilir; frozen TEST'e
   dokunulmadı.

## Reddedilenler

| # | seçenek | neden reddedildi |
| :-: | :--- | :--- |
| A | ADR-0036'yı koru, `λ` ile ince ayar | geri ölçek **toplam gücü** ayarlıyor, **oranı** değil; eşit oranla grounding geri gelmiyor (ölçek düşükse `τ_g` zayıf, yüksekse model bozuluyor) — §22'de ölçüldü |
| B | `MAXTOK`'u büyütüp dejenere koşuyu kurtar | kesiklik bütçe darlığı değil **model hasarıydı** (tekrarlama döngüleri); ayrıca ADR-0043 rejim değişmezini kırar ve tüm çıpaları kıyaslanamaz kılar |
| C | `τ_a`'yı yeniden eğit | kol ön-kayıtlı kapısını **geçti** (M2 0,984); sorun merge aritmetiğindeydi ve orada $0'a çözüldü |
| D | modül-başına normalleştirme | denenmedi — ham TIES zaten hedefi tutturdu. Açık soru olarak `open_questions.md`'de kalır |

## Sonuç

**ARA KAPI kapatılabilir hâle geldi:** 1. gözlem M2 Rej 0,984 ≥ 0,923 ✅ *(🚨 ᴷ⁴ 2026-08-06:
**0,955 ≥ 0,923** ✅ — bu ayak **ayakta**, KARAR-3)* · 2. gözlem merge
M2b 0,877 ≥ 0,854 ✅ *(🚨 ᴷ³: **0,766 < 0,8649** 🔴 **DÜŞTÜ** — aşağıya bak)* ·
⇒ satır **`✅ ❌` → DUR**, ve §20'nin ön-kayıtlı uyarısı karşılandı (merge M1 kütlesi 71,6%,
`τ_g` ile eşit — merge bir *"her şeye hayır diyen"* model değil).

> 🚨 **2. GÖZLEM YENİDEN TÜRETİLDİ 2026-08-06 (kusur K-2) — HÜKÜM DEĞİŞTİ.** Yukarıdaki ✅
> o günün aletiyle doğrudur ve **silinmedi**. Düzeltilmiş cevaba-kör paydayla aynı ön-kayıtlı
> formül: `eşik = 0,90 × base M2b 0,961 = **0,8649**` · `merge M2b = **0,766**` →
> **🔴 DÜŞTÜ, 9,9 puan altında** (eski 0,887 eşiğine karşı da düşüyor; paydalar eşit 77↔77).
> ⛔ ADR-0050: eşiğe/çarpana/formüle dokunulmadı, yalnız yeniden türetildi.
> Türetme: `outputs/eval/cp2-r-kor-payda/ara_kapi_esikleri_2026-08-06.json` ·
> [#58](../record/research_log/2026-08-06-payda-tekillesmesi.md).
>
> **Bu ADR'nin KENDİ hükmü etkilenmiyor.** ADR-0052 *"ham TIES ≫ norm-dengeli"* diyor ve bu
> ayakta: aynı düzeltilmiş aletle ham 0,766 ↔ norm-dengeli koşunun dejenerasyonu değişmedi.
> Değişen, ham TIES'in **mutlak** olarak ARA KAPI'yı geçip geçmediği. `τ_g`'nin M2b çöküşünün
> onarım oranı da düştü: 0,607→0,877 (%71 onarım) ⇒ **0,506→0,766** (%57 onarım).

⚠️ Bu, iç iddianın **kanıtlandığı** anlamına gelmez: iddia **karşılaştırmalıdır** (merge >
karışık SFT ve ardışık SFT). O karşılaştırma CP4-CP5'tir ve insan onayı bekler.
