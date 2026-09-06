# Sprint 2 defteri — sayılar, elenen seçenekler, eşik türetmeleri

> **Amaç:** Sprint 2'nin tarihi — sayılar, elenen seçenekler ve eşik türetmeleri.
> [`sprint2.md`](../../_arsiv/sprint2.md) **icra dokümanıdır, bu defter kayıt.**
>
> **Emsal biçim:** [`sprint1-sonuc-tablosu.md`](../sprint1/sprint1-sonuc-tablosu.md).
> **Kaynak kayıtlar:** `research_log` [#42](../research_log/2026-07-29-cp0-dusunce-modu-sonlanmama.md) ·
> [#43](../research_log/2026-07-29-cp09-butceli-dusunce-cipalari.md) ·
> [#44](../research_log/2026-07-30-cp05-cp1-cp2-zemin.md) ·
> [#45](../research_log/2026-07-30-cp2a-hakem-capalanmasi.md) ·
> [#46](../research_log/2026-07-30-cp2r-kor-payda.md) ·
> [#47](../research_log/2026-07-30-cp2s-boru-hatti.md) ·
> [#48](../research_log/2026-08-02-cp2c-modal-koprusu.md)
> **Kararlar:** ADR-0039 · 0040 · 0041 · 0042 · **0043** · **0044** · **0045** · **0046** ·
> **0047** · **0048** · **0049**
>
> ⚠️ **Bu bir parite iddiası DEĞİL.** Harness kapalı, maliyet normalize edilmedi (ADR-0019/0017).
>
> **Bu defter 2026-08-02'de kuruldu:** `sprint2.md` 731 satıra çıkmış, icra dokümanı olmaktan
> çıkmıştı. Aşağıdaki içeriğin tamamı oradan **birebir taşındı** — hiçbir sayı, elenen seçenek,
> eşik türetmesi veya negatif bulgu silinmedi.

---

## Sprint 2 tek cümlede

> **Sprint 3'ün birleştirme deneyinin muhtaç olduğu her şeyi üretmek — ve o deneyin adil
> olacağından emin olmak.**

Bitince şu soru cevaplanmış olur: *"İki kolumuz da tek başına ayakta mı, ve rakip yöntemleri
adil koşullarda ölçtük mü?"*

**Kapsam dışı, açıkça:** birleştirme (Sprint 3) · harness (Sprint 4) · parite iddiası (Sprint 5) ·
`τ_g`'ye dokunmak.

⚠️ **Güncelleme (CP0.9):** v2'nin gerekçesi **çıktı** — M2b 0.986 → **0.607**
([`kollar.md`](../kollar.md) kalem 5). Yine de bu sprint'te açılmıyor: doğal karar anı
**Sprint 2 sonu, Sprint 3'ün kafesi kurulmadan önce** (versiyon karıştırmak merge'i geçersiz kılar).
Önce `τ_a` denenir — M2b ikisinin de hedefi, çakışma orada çözülür.

---

## Sprint 2'ye girerken bilinenler

| | durum |
| :--- | :--- |
| Eğitilmiş kol | **1** — `τ_g` **v1** (FT-1), 1.083 adım, `‖τ_g‖_F = 10.4589` · künye: [`kollar.md`](../kollar.md) |
| Çalışan hat | veri → eğitim → merge → GGUF → `llama-server` → eval → hakem, uçtan uca ✅ |
| Ölçüm zemini | DEV havuzu (80 core_hard + 70 trap), TEST (`eval/canon/`) **hiç görülmedi** |
| Çıpalar | ✅ **CP0.9'da yeniden üretildi** — base · `τ_g` v1 · Gemini 3.1 FL, bütçeli kipte, `outputs/eval/cp09-butceli-1024-512/` |
| **Protokol** | **thinking AÇIK, bütçeli**: düşünce 1024 + cevap 512, zorunlu kapatma (ADR-0043) — rejim değişmezi. **thinking-off artık canlı rejim DEĞİL** (ADR-0043 m.4 daraltıldı) |
| Bütçe | **İKİ CÜZDAN — karıştırılmaz.** Modal GPU: workspace limiti **$42.50**, harcanan **$35.23**, **kalan $7.27** *(Modal panelinden, 2026-07-30 — büyük kısmı emekli 12B hattı, bu defterde görünmüyor)*. OpenAI hakem: ayrı cüzdan, Sprint 2'de **$1.00** harcandı |

---

## ⭐ Yürürlükteki çıpalar (bütçeli kip, DEV, harness kapalı)

| ölçüt | yön | base | `τ_g` v1 | Gemini 3.1 FL | payda |
| :--- | :-: | --: | --: | --: | :--- |
| M1 sadık-cevap kütlesi % | ↑ | 56.7 | **71.4** | 72.9 | — |
| M1 A1 *(CP1 hakemi)* | ↑ | **0.9777** | 0.9283 | 0.9421 | — |
| **M2 Rej (LLM)** | ↑ | 0.803 | 0.833 | **0.848** | **66/70** kör |
| **M2b Rej (LLM)** | ↑ | 0.949 | **0.519** 🔴 | 0.861 | **79/80** kör |
| **M3 Rej** | ↑ | 1.000 | **0.800** | 1.000 | **80/80** tanım |
| M5 ezber kütlesi % *(ANTİ-HEDEF)* | ↓ | 42.5 | **39.2** | 54.4 | — |
| ort token/cevap | ↓ | 1135 | 772 | **543** | — |

✅ **Çekinme satırları CP2-r'de cevaba-kör paydayla DÜZELTİLDİ** ([#46](../research_log/2026-07-30-cp2r-kor-payda.md) ·
`outputs/eval/cp2-r-kor-payda/`). M1 A1 satırı **CP1'in yeni hakemindendir** (eski: 0.986 / 0.866 / 0.956).
Eski özneye-bağlı sayılar `cp09-butceli-1024-512/`'de **yerinde duruyor** — silinmedi, yanına yazıldı.

Kaynak: `research_log` [#43](../research_log/2026-07-29-cp09-butceli-dusunce-cipalari.md) ·
tablo `scripts/cp09_tablo.py` ile dosyalardan üretilir.

> ### ✅ ÇEKİNME SATIRLARI DÜZELTİLDİ (CP2-r) — [ADR-0048](../../adr/0048-cevaba-kor-tuzak-gecerliligi.md)
> Bu üç satırın **paydası özneye bağlı**: `valid_trap` her özne için, hakem o öznenin **cevabını
> görerek** yeniden yargılanmış. Aynı 80 M3 kaleminde 54/56/**39** — ve M3'te bağlam **boş**
> olduğundan doğru payda tanım gereği **80/80**'dir.
>
> **Bilinen düzeltmeler:** M3 `τ_g` **0.923 → 0.800**. M2/M2b filtresiz değerler: M2 base 0.786 ·
> `τ_g` 0.800 · Gemini 0.814 — M2b base 0.950 · `τ_g` 0.525 · Gemini 0.850.
> Sapma **yön değiştiriyor**: M2b'de aleyhimize ~7p, M3'te lehimize ~12p.
>
> ✅ **CP2-r koştu ($0,23).** Paydalar: m2 **66/70** · m2b **79/80** · m3 **80/80** (tanım).
> Yukarıdaki tablo artık düzeltilmiş sayıları taşıyor ve **karar dayanağıdır**.
>
> ⭐ **Düzeltme 6 karşılaştırmanın 4'ünde ALEYHİMİZE çıktı** — en çok kayan özne **rakip**
> (Gemini M2 −0,082 · M2b −0,139). `τ_g`'nin base'e açığı üç modda da **büyüdü**
> (m2b 0,379 → **0,430** · m3 0,077 → **0,200**).

## `τ_g`'nin negatifleri — **bütçeli kipte tablo değişti**

| # | ne | thinking-off | **bütçeli** | Sprint 2'deki sahibi |
| :-- | :--- | :--- | :--- | :--- |
| **1** | Cevapladığında hata (M1 A1) | 0.973 → 0.847 | 0.986 → **0.866** | ⚠️ **duruyor** — sahipler CP1 (meta-iddia ölçümü) + Sprint 4 harness |
| **2** | Tuzak reddi (M2) | 0.633 → **0.458** ❌ | 0.814 → **0.873** ✅ | ✅ **KAPANDI** — `τ_a`'nın ön-kayıtlı gerekçesi buharlaştı |
| **3** | Parametrik sızıntı (M5) | 36.9 → **44.2** ❌ | 42.5 → **39.2** ✅ | ✅ **KAPANDI** — `τ_g` Kapı 6'yı bugün geçiyor, base geçemiyor |
| **4** | 🆕 **Kaynak yokken susma (M2b)** | 0.973 → 1.000 ✅ | 0.986 → **0.607** 🔴 | 🔴 **YENİ** — `τ_a`'nın gerçek hedefi burası |

> ### 🚨 Sprint 2'nin ekseni kaydı
> `τ_a`, negatif #2 için tasarlanmıştı. O negatif bütçeli kipte **yok**. Kolun gerçek açığı artık
> **M2b**: gold hiç yokken distractor'lardan cevap uyduruyor (fabrikasyon 0.393), üstelik tam
> kendi eğitim ailesinde (RAG_MULTI). `τ_a`'nın veri tasarımı ve ARA KAPI'nın okunacağı mod
> buna göre karara bağlandı — **CP2 hasadına başlamadan önce.**

---

## Elde ne var / ne yok — sprint ortası durum tespiti (2026-07-30)

| | durum |
| :--- | :--- |
| **Ölçüm zemini** | ⚠️ **Kusur bulundu ve düzeltme kararı verildi:** `valid_trap` özne başına yeniden yargılanıyordu → **22 çekinme koşusunun 21'inin paydası özneye bağlı** (ADR-0048). Bağlamın özneler arası **bit-birebir aynı** olduğu ölçüldü → düzeltme **150 kalemlik** tek önbellekle çözülüyor |
| **Hakem istemi** | ✅ Düzeltildi (CP1) · üç özne bütçeli kipte yeniden puanlandı |
| **`causal-conv1d`** | ✅ Kapı KALDI (tavan **1.254×**) → eklenmedi |
| **`τ_a` eğitim verisi** | ⚠️ **Diskte var ama kusurlu** — `data/train/orpo_abstain/train.jsonl` (**1.741 çift**): `rejected` emekli 12B hattından (off-policy). *`chosen` için "**%42** geçersiz" iddiası ise **çürüdü** — zayıf hakemin çapalanma artefaktıydı, gerçek **~%17*** |
| **Yeni havuz** | 🔴 **Toplanmadı** — pilot **120+120** üretim koştu, hasat bilerek başlatılmadı |
| **Hasat verimi** | ✅ **%5,0 → %10,0** — mini geçerli tuzakları geçersiz sayıp fabrikasyonların yarısını çöpe atıyordu. **750 hedef = 7.500 üretim** |
| **Hedef + donanım** | ✅ ADR-0047: **750 negatif · Modal `-np 32`** · taşıyıcı Q4_K_M GGUF sabit · `τ_a` rejimi **~73 adım / 5 epoch** |
| **Açık kalan** *(o gün)* | ⏳ Yalnız **`cp2_harvest.py` eş zamanlı üretime alınmalı** (kod, CP2-c ön koşulu). *M1 A1 muhafızı CP2-r'de **0.880** olarak kapandı.* |

> 🔒 **CP2-c 1 AĞUSTOS'A ERTELENDİ** *(2026-07-30 kararı, 2026-08-02'de uygulandı)*
> Modal bütçesi tükendi (kalan **$7,27**, tuzak 6.3) ve eğitim hızı kayıtlının **10 katı** yavaş
> çıktı (**70 s/it**, 7 değil → ⚠️ bu kıyas #48'de düzeltildi: 7 s/it **SFT**, 70 s/it **ORPO**)
> → CP3 tek başına ~**$3,2**. Yerel hasat **ölçülüp elendi**: `-np 8` yalnız **1,35×** veriyor
> (zorunlu kapatma 9/9 → ikinci istek izi baştan prefill ediyor) → 750 negatif **17,1 saat**.
> **Karar:** fatura dönemi yenilenince Modal'da koşulacak (**~1,5-3 sa, ~$3-6**).
> **Hiçbir ön-kayıtlı sayı değişmedi** — hedef 750, `τ_a` ~73 adım, üç eşik yerinde.

---

## ⭐ ADR-0049 ile kilitlenen beş karar

| # | karar | sayı |
| :-- | :--- | :--- |
| 1 ✅ | ARA KAPI eşikleri **düzeltilmiş cevaba-kör çıpadan yeniden türetilir** — ön-kayıtlı olan **formül**, sayı değil (emsal: 0.75/0.876 → 0.934/0.888) | ✅ **türetildi:** M2 **0.923** · A1 **0.880** · M2b **0.854**. Hareket tahminden küçük (1,1 p) ve düzeltmenin **net etkisi aleyhimize** — 6 karşılaştırmanın 4'ü |
| 2 | 150 kalemlik kör `valid_trap` önbelleğini **gpt-4o** kurar, **bir kez** · skorlama hakemi **mini kalır** · `verdict` yeniden hesaplanmaz | **$0,29** · m2 70 + m2b 80 + m3 **0** (tanım gereği 80/80) |
| 3 | **M2b kapı olarak kalır** — karşılaştırma kalem-içi, zayıflık seviyeyi bozar açığı bozmaz. Ön-kayıtlı taban | **40/80**; altında merge onarımı **tanımlayıcıya** iner |
| 4 | Boru hattı **5 adımlık mekanik smoke** ile sınanır — tam pilot CP3 **değil** (okunabilir sayı = çıpalama riski) | **$0,15** |
| 5 | CP2-c kabul: **B** = mini ön-filtre → gpt-4o verdict **teyit** → gpt-4o **kör** geçerlilik damgası | **$3,68** · artık kirlilik ~0 (A'da %9,5 kalıyordu) |

### Karar 5'in elenen iki tasarımı (ADR-0049 m.5)

**Seçilen B ($3,68):**

```
üretim (7.500)
  → regex ön-filtre                       bedava, ~%30 geçer
  → gpt-4o-mini verdict                   ~2.250 × $0,000117 = $0,26
  → gpt-4o verdict TEYİT (kabul edilende) ~900 × $0,0019     = $1,71
  → gpt-4o KÖR geçerlilik damgası         ~900 × $0,0019     = $1,71
                                          ────────────────────────────
                                          ham ~900 → temiz ~750 · $3,68
```

**❌ Reddedilen A ($2,0):** mini↔4o verdict uyumu **0,857** ve ayrışan 3 kalemin **2'si
mini=FABRICATE / 4o=ABSTAIN** — mini, 4o'nun reddedeceğini kabul ediyor. Artık kirlilik **~%9,5**
ve kör geçerlilik adımı bunu **yakalamıyor** (ayrışma verdict'te). Bir gündür düzelttiğimiz hata
sınıfının aynısını %9,5 oranında havuza sokmak, $1,7 tasarruf için kötü bir takas.

**❌ Reddedilen C ($6,0):** aynı sonucu **$2,3 fazlaya** alıyor; kalan bütçede CP4-CP5 ~$12 istiyor.

**Yan kazanç (B):** `chosen` tarafı aynı kör damgayla **bedava** süzülür (ADR-0048 m.5'in gereğini
ayrı koşu olmadan karşılar).

---

## ⭐ Eşiklerin türetilmesi — **0.923 / 0.880 / 0.854** ᴷ³

> 🚨 **DAMGA 2026-08-06 (K-2/K-3): bu üç sayı EMEKLİ BİR ALETİN türetmesidir.** Silinmedi.
> Aşağıdaki türetme `valid_trap_cache.py` + `rescore_abstention_cached.py` ile yapıldı;
> ikisi de emekli edildi ve **900 klipi bir kategori hatasıydı** (parça sabiti birleşime
> uygulanmış; hakem cp09 m2b'de 320 kaynağın 147'sini görüyordu, %46). Bugünkü tek aletle:
>
> | eşik | formül (ön-kayıtlı, DEĞİŞMEDİ) | bu bölüm | **yürürlükte 2026-08-06** |
> | :--- | :--- | ---: | ---: |
> | M2 tekil | base M2 + 0,12 | 0,923 | **0,934** ⚠️ payda ONARILMADI, askıda |
> | M1 A1 muhafızı | base A1 × 0,90 | 0,880 | **0,8878** *(valid_trap'ten etkilenmez)* |
> | merge M2b | base M2b × 0,90 | 0,8541 | **0,8649** |
>
> ⛔ ADR-0050: formüle/çarpana **dokunulmadı**, yalnız yeniden bölündü.
> Türetme: `outputs/eval/cp2-r-kor-payda/ara_kapi_esikleri_2026-08-06.json` ·
> [#58](../research_log/2026-08-06-payda-tekillesmesi.md).
> **Merge onarımı bu yeni eşikte DÜŞÜYOR (0,766 < 0,8649).**


```
M2 eşiği       = düzeltilmiş base M2 + 12 puan
M1 A1 muhafızı = 0.90 × base M1 A1        ← DEĞİŞMEZ (groundedness; valid_trap'e dokunmaz)
M2b onarım     = 0.90 × düzeltilmiş base M2b
```

> ### ✅ EŞİKLER TÜRETİLDİ (CP2-r) — [ADR-0049](../../adr/0049-sprint2-kalan-kararlarin-kilitlenmesi.md) m.1
> Eski **0.934**, `valid_trap`'in özneye bağlı olduğu paydadan (`48/59 = 0.814`) türemişti.
> Cevaba-kör paydayla (66/70) çıpa **0.803** → eşik **0.923**. Tahmin ~0.91'di; hareket
> tahminden **çok küçük: 1,1 puan.** Merge onarım eşiği **0.887 → 0.8541** (base M2b 0.949 × 0.90).
>
> **Ön-kayıtlı olan FORMÜL** (`base + 12 puan`), sayı değil — ve emsal var: eşikler thinking-off →
> bütçeli geçişinde bir kez zaten taşındı (0.75 → 0.934).
>
> ⭐ **VE ÖLÇÜM SAVUNMAYI DOĞRULADI:** düzeltme **6 karşılaştırmanın 4'ünde ALEYHİMİZE** çıktı.
> `τ_g`'nin base'e açığı üç modda da büyüdü (m2b **0,379 → 0,430** · m3 **0,077 → 0,200**), ve en
> çok kayan özne **rakip** oldu (Gemini M2 −0,082 · M2b −0,139 — kirli paydadan en çok o
> yararlanıyordu). Net etki **aleyhimize**; eşiğin 1,1 puan kolaylaşması bunun yanında küçük.
>
> ✅ **M1 A1 muhafızı KAPANDI: 0.880.** `valid_trap`'ten bağımsız — CP1'in yeni hakemi base A1'i
> 0.986 → **0.9777**'ye taşıdı, muhafız = 0.9777 × 0.90. *(#44'te "ısırmıyor" diye açık
> bırakılmıştı.)*

> ### 🚨 Tavan riski — şimdi kayda geçiyor, sonra değil
> Base geçerli 59 tuzağın **48'ini zaten reddediyor**. +12 puan, kalan **11 hatanın 7'sinin**
> düzeltilmesi demek — tavana **6.6 puan** kala. `τ_a` bu kapıda kalırsa sebebi kolun kötülüğü
> değil **base'in tavana yakınlığı** olabilir; kapı, ölçmek için kurulduğu şeyi ölçemez hâle gelir.
> Kapı 5'in ADR-0039'da başına gelen şeyin aynısı. Sayı ön-kayıtlı formülden geldiği için
> **değiştirilmedi** — ama bu şerh sonuçla birlikte raporlanır.

**Eski eşikler 0.934 / 0.888 / 0.887 — sonuç ikisine karşı da raporlanır** (ADR-0049 m.1).
✅ **Sayılar CP0.9'dan geldi** (formül ön-kayıtlıydı, sayı değil). Eski eşikler (0.75 / 0.876)
thinking-off protokolündendi ve **düştü**.

> ✅ **CP0.9 koşuldu, endişe doğrulandı:** base bütçeli düşünceyle tuzak reddini **kendi başına**
> 0.633 → **0.814**'e taşıdı. `τ_a` eski çıpaya (0.6330) karşı ölçülseydi **haksız kredi** alırdı;
> referans artık 0.814 ve eşik ondan türetildi.

---

## ⭐ ADR-0045'in karar tablosu — neden iki gözlem

Base bütün çekinme modlarında tavana yaklaştığı için (M2 0.814 · M2b 0.986 · M3 1.000)
`base + 12 puan` formülü **her modda kırık**. Ayrıca `τ_a` ham base'den eğitildiği için
onaracağı delik **kendi üstünde değil, `τ_g`'de**.

**Karar:** ön-kayıtlı eşiğe **dokunulmadı**; yanına neredeyse bedava ikinci bir gözlem eklendi.

```
1) τ_a TEKİL      → M2 Rej ≥ 0.923 · M1 A1 ≥ 0.880   ✅ CP2-r'de türetildi
2) τ_g+τ_a MERGE  → M2b ≥ 0.854 mi?  (τ_g 0.519'dan onarım · 0.90 × base 0.949)
```

> ### ✅ İkinci gözlem: merge onarım kontrolü ([ADR-0045](../../adr/0045-ara-kapi-merge-onarim-kontrolu.md))
> Tek gözlemli kapı *"kaldı ama neden kaldı"* sorusunu teşhis edemiyordu. `τ_a` eğitildikten
> sonra **`τ_g` + `τ_a` norm-dengeli TIES merge** DEV'de koşulur ve **M2b** okunur:
> **onarım eşiği M2b ≥ 0.854** (0.90 × base **0.949**, cevaba-kör — muhafız formülüyle aynı çarpan;
> eski 0.887 çıpası 0.986'dan türemişti, CP2-r düzeltti).
> Maliyet: merge eğitim compute'u gerektirmiyor → **GPU $0 + hakem ~$0.15**.
> Bu bir **kafes hücresi değil, kapı ölçümüdür** ve DEV'de yapılır; Sprint 3'ün 8 hücresi ayrıca
> ve aynı rejimle koşulur (ADR-0036).

**Gerekçe:** `τ_a` tutmazsa birleştirilecek ikinci kol yok, Kapı 5'in (b) referansı yok, ve iç
iddia ölçülemez. Rakipleri önce eğitmek, sonucu bilinmeyen bir deneye peşin para yatırmaktır.
82 adım — bekleme ucuz.

**CP2'ye etkisi:** hasat **iki tipi birden** toplar — M2-tipi (tuzak verilmiş) + M2b-tipi
(gold hiç yok). Karışım oranı künyeye yazılır.

---

# Biten checkpoint'ler — tam sonuç kayıtları

## CP0 — Düşünce modu ✅ **KOŞULDU** — ölçüm üretilemedi, karar başka yerden geldi

**Karar belgeleri:** [ADR-0040](../../adr/0040-dusunce-modu-olculecek-on-kayitli-kural.md) (ön-kayıtlı kural)
→ [**ADR-0043**](../../adr/0043-dusunce-modu-acik-butceli-kapatma.md) (sonuç) ·
**GPU:** yerel ($0) · **Kayıt:** [`research_log` #42](../research_log/2026-07-29-cp0-dusunce-modu-sonlanmama.md) ·
**Betikler:** `scripts/cp0_thinking_gen.sh` · `scripts/cp0_thinking_score.sh`

> ### 🚨 Olan şu: base `--thinking on` altında **DURMUYOR**
> M1 · M2 · M5'te `</think>` **hiç kapanmıyor**, `content` boş dönüyor. Kesilme değil
> **sonlanmama**: model cevaplamak ile çekinmek arasında salınıp aynı muhakeme satırını
> **219 kez** tekrarlıyor. Üç açıklama elendi — bütçe **8×** (4096→32768) ❌ · `temp 0.6` 🟡 (yarısı)
> · **Q8_0** ❌. Ve karar eksenlerinin üçü (M1 kütle · M2 Rej · M5 ezber) **tam o üç modda.**
>
> Döngü **belirsizlikle** geliyor: cevabın açık olduğu **M4** (3/3, ort 3.932 tok) ve reddin açık
> olduğu **M3** (3/3, ort 1.126 tok) sorunsuz sonlanıyor.

### Çözüm — bütçeli düşünce (ADR-0043)

```bash
# üretim: 6 mod, düşünce 1024 + cevap 512, zorunlu kapatma, kesik kapısı dahil
THINK_BUDGET=1024 MAXTOK=512 bash scripts/cp0_thinking_gen.sh models/gguf/<gguf> <etiket>
# puanlama: .env yükler, hakem/gateway pinli, ADR-0040 kuralını otomatik uygular
bash scripts/cp0_thinking_score.sh <etiket>
```

Model `</think>`'i bütçe içinde kapatmazsa iz + `</think>` isteme yapıştırılır ve üretim
`/completions` ile sürdürülür → cevap **zorunlu olarak** yazılır (`--think-budget`, `forced_close`).
**Bütçe ön-kayıtlı ve rejim değişmezi** — `TASARIM.md` §4.1.1'e işlendi.

### CP0-b — `τ_g` hasar sensörü ✅ **hasar YOK, tersi çıktı**

`τ_g` v1 aynı istemlerde **35/36 kendi kapatıyor**, medyan **452 token**, düşünce izinde döngü
**yok**, iz yapılı (kaynakları tek tek eleyip gerekçesiyle seçiyor) — base aynı iki istemde
108K/119K karakter üretip hiç bitirmiyor. → *"reçete fazla sertti"* hipotezi **desteklenmedi**;
`τ_g` v2 bu gerekçeyle **açılmıyor** (diğer dört gerekçe: [`kollar.md`](../kollar.md)).

⚠️ Yan bulgu: iz **8/8 İngilizce**, cevap **8/8 Türkçe** → ürün *"okunabilir iz"* hedefi için
eğitim verisine iz gerekir; v2'nin 4. gerekçesi.

### ⚠️ Bunun Sprint 2'ye faturası

| ne | sonuç |
| :--- | :--- |
| **Sprint 1'in üç çıpası** | ✅ **CP0.9'da koşuldu** — 1.410 cevap, GPU $0, hakem **$0.45** |
| **ARA KAPI'nın referansı** | ⚠️ **SÜPERSED** — o gün 0.814 → eşik 0.934 · muhafız 0.888 idi. CP2-r cevaba-kör paydayla base'i **0.803**'e taşıdı → yürürlükteki eşikler **0.923 / 0.880 / 0.854** |
| **`rejected` hasadı (CP2)** | `--thinking off` değil, **bütçeli düşünce** kipinde (ADR-0042 üst notu) |
| **Maliyet ekseni** | ✅ ölçüldü: 249 → **1135 tok/cevap (4.5×)**; `τ_g` **772**, kendi istem ailesinde **476** |
| **Ön-kayıtlı 🟢🟡🔴 kuralı** | ✅ koşuldu → **🟡 SARI**; RS-FT kapsam dışı kalıyor |

> **Kalıcı kural (ADR-0040 m.4):** bundan sonra herhangi bir kol yeniden eğitilirse **düşünme
> yeteneğini koruyacak biçimde** eğitilir. Kapıyı açık tutmanın maliyeti eğitim anında ≈ sıfır,
> sonradan yüksek.

---

## CP0.9 — Üç çıpa bütçeli kipte ✅ **KOŞULDU** (2026-07-29)

**Karar belgeleri:** [ADR-0043](../../adr/0043-dusunce-modu-acik-butceli-kapatma.md) m.4 ·
🆕 [**ADR-0044**](../../adr/0044-mod-duyarli-feragat-kurali.md) · **GPU:** yerel ($0) ·
**$:** 0.49 (hakem; 0.45 ana + 0.05 ablasyon) · **Kayıt:** [`research_log` #43](../research_log/2026-07-29-cp09-butceli-dusunce-cipalari.md) ·
**Çıktı:** `outputs/eval/cp09-butceli-1024-512/` (+ `KUNYE.json`)

1.410 cevap (3 özne × 470), üç geçerlilik kapısı da geçti: kesik **%3.6 · %3.6 · %0.0**,
düşünce kanalı **470/470**. Sayılar yukarıdaki *"Yürürlükteki çıpalar"* tablosunda.

### ⭐ Bu turun dört kalıcı bulgusu

**1. Anti-hedef ekseni 3.4× yanlış ölçülüyormuş → [ADR-0044](../../adr/0044-mod-duyarli-feragat-kurali.md).**
Kör modun sistem istemi feragat cümlesini **emrediyor**, red-regex onu çekinme sayıyordu → dolu
cevaplar "reddetti" sayıldı. Ezber kütlesi base'de %10.7 → **%36.9**. Sapma **bizim lehimizeydi**.
Etki alanı yalnız M5; `τ_g`'nin ihlali aklanmadı, **büyüdü** (+3.9 → +7.3 puan).

**2. Düşünce ayırt etme yeteneğini artırıyor — biçim değil.** Ablasyon koşuldu ($0.046): sisteme
*"önce kaynağın soruyu cevaplayıp cevaplamadığını belirt"* eklenip thinking-off koşuldu. M2 Rej
**0.968**'e çıktı ama M1 kütlesi **28.2**'ye düştü (aşırı-red 0.6875) — tek eksende kaydırma.
Bütçeli düşünce iki ekseni birden taşıyor (M1 42.6→56.7 **ve** M2 0.633→0.814).
→ **prompt-mühendisliği alternatifi elendi; 4.5× token'ın karşılığı var.**

**3. Sonlanma kararlılığı eğitim istemi ailesine özgü.** `τ_g` kendi RAG_MULTI ailesinde zorunlu
kapatmayı **%91.7 → %5.8**'e indiriyor, token 1098 → **476**; dışında marjinal (%96.7 → %79.3).
CP0'ın n=36 örneklemi o aileden geldiği için genel kazanç sanılmıştı.

**4. ADR-0040 hükmü: 🟡 SARI.** M2 eşiği **geçti** (0.814 ≥ 0.78, +18.1p), M1 kütlesi 0.9 puan
kaldı (%56.7 < %57.6), **M5 muhafızı İHLAL** (%36.9 → %42.5). Hüküm ADR-0044'ten bağımsız sağlam.
→ **RS-FT Sprint 2 kapsamına girmiyor**, ADR-0035 açılmıyor, plan değişmiyor.

### Yan çıktılar

`scripts/cp09_gemini_gen.sh` · `scripts/watch_cp09.sh` · `scripts/cp09_tablo.py` (yeni) ·
`gen_eval_grounded.py --reasoning-budget` (rakip tarafı bütçe, ADR-0043 m.3'ün karşılığı) ·
`--sufficiency-preamble` (ablasyon bayrağı) · `outputs/eval/` **koşu klasörü düzeni + `KUNYE.json`**.

---

## CP0.5 — `causal-conv1d` hız kaldıracı ✅ **KOŞULDU — KAPI KALDI** (2026-07-30)

**Karar belgesi:** [ADR-0033](../../adr/0033-egitim-hizi-fla-core-checkpointing-batch.md) ·
**GPU:** yerel ($0) · **Kayıt:** [`research_log` #44](../research_log/2026-07-30-cp05-cp1-cp2-zemin.md) ·
**Betik:** `scripts/cp05_conv1d_ceiling.py` · **Çıktı:** `outputs/eval/_artefakt/cp05_conv1d_ceiling*.json`

CP5'te ölçülmüştü: **6.8-7.0 s/it · 2.619 token/s · MFU ≈ %15.** Şüpheli `causal-conv1d`
kurulu olmaması — Qwen3.5-4B'nin **32 katmanının 24'ü** linear-attention ve PyTorch referans
yoluna düşüyor (*"The fast path is not available"*). Fallback **matematiksel olarak aynı**.

> ⚠️ **Bu s/it değeri #48'de yeniden yorumlandı:** 6,8-7,0 s/it **SFT · efektif batch 16**'dır
> (`τ_g`'nin 1.083 adımlık koşusu). CP2-s'in ölçtüğü ~70 s/it ise **ORPO · efektif batch 64**.
> İki sayı farklı rejimlere ait; kayıt **yanlış değil**, kıyas yanlıştı.

### Sonuç: **tavan 1.254× · kapı 2.0× → EKLENMEDİ**

Paket **derlenmedi** — gerek kalmadı. Hızlı-yol dalına **bedeli sıfır saplama** konarak kazancın
üst sınırı doğrudan ölçüldü: gerçek çekirdek bundan hızlı olamaz.

| ölçüm | değer |
| :--- | --: |
| tavan (batch 2 × 2048) | **1.254×** |
| dört şekilde kararlı | 1.196 – 1.254× |
| kapı | **≥ 2.0×** |

Teşhis kaynaktan okundu: çekirdekler **bağımsız ikame ediliyor** ve pahalı özyineli çekirdek
zaten `fla`'dan geliyor — *"fast path is not available"* uyarısı yalnızca `warning_once`,
yani darboğazın adresi değil. Katman-seviyesi tavan model-seviyesinin **üst sınırı** olduğu için
ölçüm bağlayıcı (conv 32 katmanın 24'ünde var; kalanı yalnız paydayı büyütür).

⚠️ **Sapma kontrolü de koşuldu:** yerelde `fla` Triton çekirdeği gerçekten bağlıydı — bozuk bir
`fla` ölçümü **benim sonucumun lehine** saptırırdı.

**Sonuçlar:** `requirements.lock.txt` **korundu** · CP3-CP5 mevcut hızla koşar ·
**MFU ≈ %15 framework tavanı olarak Limitations'a girer** · `fla-core` dersi (#40) bir kez daha
doğrulandı: *kazanç ölçülmeden yazılmaz.*

---

## CP1 — Hakem istemi düzeltmesi ve yeniden puanlama ✅ **KOŞULDU** (2026-07-30)

**Karar belgesi:** [ADR-0041](../../adr/0041-raft-meta-iddia-hakem-kurali.md) ·
**$:** 0.15 fiili *(planlanan 0.12)* · **Kayıt:** [`research_log` #44](../research_log/2026-07-30-cp05-cp1-cp2-zemin.md) ·
**Betikler:** `scripts/cp1_rescore_meta.sh` · `cp1_delta.py` · `cp1_spotcheck.py` ·
**Çıktı:** `outputs/eval/cp1-hakem-meta-iddia/` (+ `KUNYE.json`)

Groundedness hakem isteminin 1. adımına kural satırı eklendi: *kaynak seçimi/eleme hakkındaki
meta-cümleler iddia olarak ayrıştırılmaz* (`scripts/groundedness.py`, `EXTRACT_SYSTEM`).
`base` · `Gemini 3.1 FL` · `τ_g` **üçü birden** yeniden puanlandı. **Üretim yok** — girdi CP0.9'un
cevapları; değişen yalnız hakemin 1. aşama istemi.

### Sonuç: `τ_g`'nin A1 açığının **%59'u biçim artefaktıymış**

| ölçüt | eski hakem | **yeni hakem** |
| :--- | --: | --: |
| `τ_g`'nin base'e A1 açığı | 0.120 | **0.049** |
| `τ_g` hatalı iddia oranı | %18.1 | **%9.6** *(ADR-0041 %9.9 demişti)* |

**Kalan %41 gerçek ve maskelenmiyor** — üç uygulama şartının üçü de tutuldu: (1) üç özneye aynı
anda, (2) eski skorlar `cp09-butceli-1024-512/`'de duruyor (artık **ham/kontrol**), (3) ham
sayılar yayımlandı.

**Kapsam ampirik olarak daraltıldı:** meta-cümle taraması yapıldı → yalnız **M1**'de var
(base 36/80 · `τ_g` 58/80 · **Gemini 0/80**); M4/M5'te 0/80. Bu yüzden yeniden puanlama M1 ile
sınırlı tutuldu ve maliyet ADR-0041'in tahminine oturdu.

⚠️ **Hedef-dışı etki gürültünün 3 katı ve raporlanıyor:** aynı istemle ikinci koşu −10 iddia
(gürültü) verirken istem değişikliği −30 iddia getirdi ($0.037'lik ayrı kontrol koşusu).

⚠️ **Spot-check yanıltıcı çıktı, sayı olarak kullanılmadı.** `cp1_spotcheck.py` birebir metin
karşılaştırıyor, oysa hakem iddiaları **yeniden ifade ediyor** → `τ_g` için 106 "yeni eklenen"
iddia göründü. Yerine meta-taşıyan ↔ meta-taşımayan **kontrol grubu** ölçümü yapıldı (#44).

**Etkilenmeyen (doğrulandı):** abstention regex'i · atıf doğrulayıcı · register hakemi.
Yığın pinlemesi (ADR-0029/0032) değişmedi.

> ✅ **KAPANDI (CP2-r):** muhafız **0.880**. CP1'in yeni hakemi base A1'i 0.986 → **0.9777**'ye
> taşıdı, muhafız = 0.9777 × 0.90. Sonuç eski **0.888**'e karşı da raporlanır.

---

## CP2 — `rejected` havuzunun yeniden hasadı

**Karar belgeleri:** [ADR-0042](../../adr/0042-rejected-havuzu-tek-kaynak-ve-on-policy-kontrol.md)
→ **[ADR-0046](../../adr/0046-cp2-kabul-olcutu-hakem-ve-havuz-on-elemesi.md)** (kabul ölçütünü değiştirir) ·
**GPU:** yerel ($0) · **Kayıt:** [`research_log` #44](../research_log/2026-07-30-cp05-cp1-cp2-zemin.md) ·
**Betikler:** `scripts/cp2_harvest.py` · `cp2_pilot.sh` · `cp2_audit.py` · `cp2_prefilter.py` *(yazıldı, koşulmadı)* ·
**Çıktı:** `outputs/eval/cp2-rejected-hasat/` (+ `KUNYE.json`, durum 🔴 PİLOT)

Mevcut havuz emekli **12B** hattının fabrikasyonları — yeni modele **başka bir modelin hatalarını**
öğretir. Yeniden hasat: **çıplak base**'den, seed **3407**, aynı üretim ayarları.

> ⚠️ **`--thinking off` DEĞİL** (ADR-0043, 2026-07-29): hasat, kolların eğitileceği ve
> dağıtılacağı kiple aynı olmalı → **bütçeli düşünce (1024 + 512)**. Aksi hâlde negatif örnekler
> modelin gerçekten ürettiği çıktılar olmaz ve ADR-0042'nin kendi *on-policy* gerekçesi çürür.

> ### 🚨 KABUL KRİTERİ DEĞİŞTİ — [ADR-0046](../../adr/0046-cp2-kabul-olcutu-hakem-ve-havuz-on-elemesi.md) (2026-07-30)
> **Eski (ADR-0042, artık geçersiz):** *"`score_abstention.py` RED saymıyor"* → yani **regex**.
> Pilot ölçtü: bu ölçütün kabul ettiklerinin **%71'i gerçekte ABSTAIN**, **%42'si geçersiz tuzak**;
> gerçek verim %30 değil **%5,0**. Kaçışın **5/15'i leksik olarak işaretsiz** — hiçbir desen
> yakalayamaz, yani regex'i genişletmek çözüm değil.
>
> **Yeni:**
> ```
> üretim → regex ön-filtre (RED ise ele, bedava)
>        → LLM red hakemi   (ABSTAIN ise ele)   → KABUL = FABRICATE
> ```
> Ölçüt artık **raporlanan metrikle aynı** (`rejection_rate`, gpt-4o-mini) — `yurutme-tuzaklari`
> **4.7** kapanır.
>
> **Ve havuz üretimden ÖNCE elenir:** geçerlilik `(soru, tuzak madde[:900])`'den sorulur, GPU'ya
> girmeden — ≈**$0,94 / 8.000 kalem**, verim %5,0 → **%8,6**, yerel GPU süresi ~%42 kısalır.
> Geçersiz çıkan tuzağın **çifti düşer** → aynı dilimden üretilmiş `chosen` tarafı (**tuzak 4.8**)
> ayrı bir iş olmadan temizlenir. Havuz **baştan kurulmaz, süzülür** — tek-havuz kuralı korunur.
>
> ⚠️ **Ön koşul (m.3):** ön-eleme hakemi cevabı görmez, denetim hakemi görür. Ayrışırlarsa havuzu
> bir ölçütle elemiş, sonucu başkasıyla raporlamış oluruz. **Uyum önce 36 etiketli örnekte
> ölçülür (~$0,004); yetersizse ön-eleme koşulmaz.**
> Betik: `scripts/cp2_prefilter.py` (dilim · seed · klip `cp2_harvest.py` ile birebir;
> geçerlilik sorusu `score_abstention.JUDGE_SYSTEM`den **import edilir**).
>
> ✅ **Hedef KARARA BAĞLANDI: 750 · Modal** — [ADR-0047](../../adr/0047-cp2-hedef-750-modal-hasat.md).
> Süre yürütülebilir değildi (yerel seri: 1.495 → **54 sa**, 500 → 18 sa). Sebep: `llama-server`
> `-np` bayrağı olmadan **tek slotla** koşuyordu, 4B Q4_K_M modeli GPU'yu doyurmuyordu.
>
> | hedef | `τ_a` çift | 3 epoch | **5 epoch** | Modal $ |
> | --: | --: | --: | --: | --: |
> | 1.495 | ~1.794 | 82 *(mevcut)* | — | ~5,7 |
> | **750** | **~937** | 44 | **~73** | **~3,0** |
> | 500 | ~625 | 29 | 49 | ~2,1 |
>
> **750 + 5 epoch → ~73 adım**, ön-kayıtlı 82'nin %89'u, yarı fiyata. 500'de adım 29'a inerdi ve
> ARA KAPI kalırsa *"kol mu kötüydü, veri mi azdı"* **ayrılamazdı** — kapı yine ölçemez hâle gelirdi.
>
> **Taşıyıcı DEĞİŞMEZ:** Modal'da da `llama.cpp + Q4_K_M GGUF`, değişen tek şey `-np 32` ve kart.
> **vLLM/bf16 kullanılmaz** — bf16'da üretilen negatifler dağıtılan modelin hataları değildir.
>
> ⚠️ **Süre/maliyet TAHMİN.** llama.cpp yüksek batch'te vLLM gibi ölçeklenmez (`-np 32` muhtemelen
> 10-20×). **İlk 10 dakikada gerçek verim okunur; tahminin 2 katını aşarsa koşu DURUR** ve sayı
> negatif bulgu olarak yazılır.
>
> ⚠️ **Epoch 3 → 5 bir rejim değişikliğidir** — aşırı-uyum riski. Bedel kabul edildi: `‖τ_a‖_F`
> koşulsuz raporlanır, seçim DEV'de yapılır, belirti görülürse epoch 3'e dönülür (adım 44).
>
> ❌ **Sentetik `rejected` (API ile üretim) REDDEDİLDİ.** `rejected`'ın tanımı *"bu modelin
> gerçekten yapacağı hata"*. API'den üretmek **üçüncü bir modelin** hatalarını verir — CP2'nin
> düzeltmek için var olduğu kusurun daha kötüsü. Üstelik ADR-0042 bu itiraza karşı CP5'e
> on-policy kontrol koşusu koymuştu; `rejected` sentetik olursa o sigorta **bize karşı** çalışır
> ve Kapı 5'in tamamı çürür. *(API'nin meşru yeri zaten planda: ön-eleme ve kabul hakemi — onlar
> veri üretmiyor, veri seçiyor.)*
>
> ✅ **M2b ENDİŞESİ ÇÖZÜLDÜ (CP2-r).** Pilotta m2b'de 25 adayın 24'ü geçersiz çıkmıştı ve bu
> M2b'yi metrik olarak sorgulatıyordu. Cevaba-kör ölçüm **79/80 geçerli** dedi — o bulgu **kirli
> hakem artefaktıydı**. Merge onarım eşiği (**M2b ≥ 0.854**) sağlam zemin üstünde duruyor.
> ⚠️ Şerh: pilot **havuz** kalemlerinde, CP2-r **DEV** kalemlerinde ölçtü — aynı kurgu, farklı
> küme. Havuz tarafı CP2-c'de aynı kör damgayla ayrıca ölçülecek.

> ### 🆕 İKİ TİP birden toplanır ([ADR-0045](../../adr/0045-ara-kapi-merge-onarim-kontrolu.md) m.4)
> | tip | üretim | neden |
> | :--- | :--- | :--- |
> | **M2-tipi** | `--with-source`, tuzak madde **verilmiş** | ARA KAPI'nın ön-kayıtlı ekseni |
> | **M2b-tipi** | `--distractors 4 --no-gold`, gold **hiç yok** | `τ_g`'nin gerçek açığı (0.607) |
>
> `τ_a`'nın iki eksende de çalışması gerekiyor. Karışım oranı ve her tipten kaç örnek kabul
> edildiği **künyeye yazılır**.

**Tek havuz, tüm kollar** (`τ_a` · Taban A · Taban B'nin iki aşaması) aynı veriyi görür. Gerekçe:
ablasyonun anlamı veriyi sabit tutmaktan gelir.

**Künye kayda geçer:** base sha · **düşünce bütçesi (1024+512) + zorunlu kapatma oranı** · sıcaklık/`top_p` · `max_new_tokens` · seed ·
tarih · kaç örnekten kaçı kabul edildi.

> ⚠️ **Bedel $0 ama süre CP0.9'dan sonra ~4× arttı.** İki sebep birleşiyor: (a) base'in
> fabrikasyon oranı bütçeli kipte **0.367 → 0.186** düştü, yani aynı havuz için kabaca **iki
> katı örnek** gerekiyor; (b) cevap başına token **4.5×**. Hasat boyutu burada ölçülür ve
> kaydedilir — ama plan yaparken bu iki çarpan hesaba katılmalı.

### CP2 pilot ✅ **KOŞTU, KUSUR BULDU** ($0.01, yerel)

Kabul ölçütü (regex) raporlanan metrikle (LLM hakemi) aynı değil; gerçek verim **%5**, hedef mevcut
havuzdan **ulaşılamaz** (29.900 üretim > 19.284 kalem, ≈92 saat). → [ADR-0046](../../adr/0046-cp2-kabul-olcutu-hakem-ve-havuz-on-elemesi.md),
yeni tuzaklar **4.7 · 4.8**.

### CP2-a ✅ **KOŞTU — ölçüm aracının kendisini kırdı** ($0.121)

2×2 hakem tasarımı: çapalanma mini'de **22,3p**, gpt-4o'da **8,4p** → *%42 geçersiz* premisi
**artefakt** (gerçek %8,3–16,7). Ve `valid_trap` **özneye bağlı** çıktı →
[ADR-0048](../../adr/0048-cevaba-kor-tuzak-gecerliligi.md) + [ADR-0049](../../adr/0049-sprint2-kalan-kararlarin-kilitlenmesi.md).
Ön-eleme uyum kapısı **KALDI**: hakemler %58,3-%91,7 arasında dağıldı → ön-eleme **koşulmadı**.

### ~~CP2-b~~ ❌ **İPTAL** — ADR-0048 m.4

Havuz ön-eleme filtresi **net zararlı**: kestiği **7 kalemin 6'sı geçerli tuzak** (isabet **0,14**),
6 geçerli tuzak boşa giderdi. $0 harcandı.

### CP2-r ✅ **KOŞTU** ($0.23) — [#46](../research_log/2026-07-30-cp2r-kor-payda.md)

230 kalemlik cevaba-kör `valid_trap` önbelleği (m2 **66/70** · m2b **79/80** · m3 **80/80** tanım)
→ 9 koşu **saf aritmetikle** yeniden puanlandı ($0, `verdict` yeniden hesaplanmadı).
**Eşikler türetildi: 0.923 / 0.880 / 0.854.** M2b kurgu tabanı **79/80 ≫ 40/80 GEÇİLDİ**.
Düzeltme **4/6 karşılaştırmada aleyhimize**.

### CP2-s ✅ **KOŞTU** (~$0.20 fiili, durduruldu) — [#47](../research_log/2026-07-30-cp2s-boru-hatti.md)

`τ_a` 50 adım (`--fresh-adapter`, eğitilebilir **29.908.992 / 4.569.174.528 = %0,65**) →
norm-dengeli TIES **224/224** → GGUF **Q4_K_M 2,59 GiB** → `llama-server` **3/3 dolu cevap**.
🔴 **Norm-dengeli k-yollu TIES'in kodu HİÇ YOKTU** → `scripts/merge_ties.py` yazıldı;
`TIES(τ,−τ)=0` testi bir **işaret hatası** yakaladı (`|ortalama| = 1,023` → 0).
Norm-dengeleme küçük kolu kurtarıyor: **0,656 → 0,734**. Eşzamanlı ≠ iteratif (max fark **2,9766**).
`‖τ_tg‖_F = 10,472179` (artefakt 10,458926, %0,13 bf16 farkı → bağımsız doğrulandı).
Merge istatistikleri: `trim_k=0,20` · geri ölçek **5,526** · çatışan parametre **%0,16** ·
sıfır kalan **%67,3**. Yeni tuzaklar **6.1 · 6.2 · 6.3**.

### CP2-c hazırlığı ✅ (2026-08-02) — [#48](../research_log/2026-08-02-cp2c-modal-koprusu.md)

`modal_train.py::harvest_cp2` + `spawn_cp2c` yazıldı (eksik köprü) · `scripts/cp2c_kabul.sh`
yazıldı (kabul zincirinin sürücüsü yoktu) · sürekli besleme **1,84×** (3,65 → **1,98** s/üretim) ·
🔴 **negatif bulgu: `-np` 32→64 %32 kötüleştirdi** (2,93 s/üretim), karıştırıcı (kart) ayrılamadı ·
verim kapısı `limit`e takılıp atlanabiliyordu → düzeltildi · regex kabul **%28,9-%32,6**.

> ⚠️ **Bu satırdaki `-np` negatif bulgusu AYNI GÜN ÇÜRÜDÜ** (aşağıdaki 16:19-16:47 kaydı).
> Sayı silinmiyor — o anki bilgi durumu buydu; ama karıştırıcı çözüldü ve sonuç tersine döndü.

---

## CP2-c üretim denemesi ve **verim kapısı olayı** 🔴 (2026-08-02, 16:19-16:47)

**Kayıt:** [`research_log` #48](../research_log/2026-08-02-cp2c-modal-koprusu.md), *"16:19-16:47 ·
üretim denemesi ve verim kapısı olayı"* bölümü ·
**Karar belgeleri:** [ADR-0047](../../adr/0047-cp2-hedef-750-modal-hasat.md) m.2 (taşıyıcı) ·
m.3 (verim kapısı) · [ADR-0049](../../adr/0049-sprint2-kalan-kararlarin-kilitlenmesi.md) m.5 ·
⭐ **doğan karar:** [ADR-0050](../../adr/0050-verim-kapisi-tahmin-edici-duzeltmesi.md) (tahmin edici
düzeltildi, **eşik 2,88 aynı**; ADR-0047 m.3'ü tadil eder) · yeni tuzak **6.9** ·
**Düzeltilen:** `scripts/cp2_harvest.py` (verim kapısının tahmin edicisi + kapı sırası)

### 1. Olay — `-np 32` üretim denemesi koştu, kapı **iki tipte de** tetiklendi

```
app       ap-5f6rLHHFohhupMGvhkla9I
saat      16:19 → 16:47
kart      NVIDIA A100-SXM4-40GB      (künyeden, gpu_gercek)
-np       32   ·  --limit 3750/tip  = hedef 7.500 üretim
çıktı     hukuk-data:/cp2c/
```

| tip | denenen | aday (regex) | oran | kümülatif s/üretim | geçen s | kapı damgası |
| :--- | --: | --: | --: | --: | --: | :--- |
| **m2** | 233 | 68 | **%29,2** | 2,89 | 672,9 | 🔴 `DURDU: 2.97 > 2.88 (202 üretimde)` |
| **m2b** | 235 | 45 | **%19,2** | 2,96 | 694,9 | 🔴 `DURDU: 2.95 > 2.88 (204 üretimde)` |

- Zorunlu kapatma **her iki tipte tam**: 233/233 · 235/235.
- Ortalama completion token: m2 **1108,0** · m2b **1138,7**.
- ✅ **113 aday kaybolmadı** — `hukuk-data:/cp2c/` altında duruyor, kabul aşamasında kullanılacak.
- **Fiili GPU maliyeti ~$1,2** — ⚠️ **TAHMİN**, panelden okunacak (tuzak **6.3**: Modal sayısı
  defterden türetilmez).

Kapı ön-kayıtlıydı ve **doğru çalıştı**: eşiği aştığını gördü, durdurdu, damgayı künyeye yazdı.
Sorun kapının varlığında değil, **ölçme aletindeydi.**

### 2. ⭐ Kapı doğru **ölçüte** bakıyordu ama **yanlı bir tahmin ediciyle** ölçüyordu

Kapı `geçen_süre ÷ tamamlanan` (t0'dan **kümülatif**) okuyordu. Yüksek eş zamanlılıkta
`concurrency` kadar istek **aynı anda başlar ve aynı anda iner**; bu **açılış geçicisi**
kümülatif ortalamada **her kaleme paylaştırılır** → erken okumada hız sistematik olarak **kötü**
görünür. Aynı logdan pencere pencere **marjinal** hız (m2):

| pencere | üretim | süre | marjinal s/üretim |
| :--- | --: | --: | --: |
| 0 → 25 | 25 | 142 s | **5,70** ← açılış dalgası |
| 100 → 175 | 75 | 167 s | **2,22** |
| 100 → 200 | 100 | 238 s | **2,38** |
| 200 → 225 | 25 | 73 s | **2,90** ← kapı sonrası **boşalma** fazı |

→ m2'nin gerçek hızı ~**2,4 s/üretim** — eşiğin **ALTINDA**.
→ m2b'nin kararlı hızı ~**3,0 s/üretim**, m2'den ~**%25 yavaş** (çeldirici blokları prefill'i
uzatıyor).

> ### 🔍 Doğrudan kanıt — kapının kendi logu kendini çürütüyor
> Kapı **600. saniyede** `2,97` ile durdurdu; **aynı koşu 673. saniyede zaten `2,89`'daydı**.
> Ölçülen büyüklük kararlı hâline doğru **hâlâ inerken** karar verilmişti.

7.500 üretimlik gerçek koşuda açılış dalgası toplam sürenin ~**%0,6'sı** → ölçekte **amortize
oluyor**. Yani yanlılık tamamen **erken okuma** problemi.

### 3. Karar (insan, 2026-08-02): **eşiğe DOKUNULMADI, tahmin edici düzeltildi**

**❌ REDDEDİLEN — eşiği 2,88 → 3,2 gevşetmek.** Sonucu gördükten sonra ön-kayıtlı bir eşiği
oynatmak, ön-kayıt kurumunun kendisini geçersiz kılar. Bu hattın ADR-0039 dersi tersi yöndeydi:
kapı ölçemez hâle gelince **kapı bölünür**, eşik gevşetilmez.

**❌ REDDEDİLEN — CP2-c'yi negatif bulgu olarak kapatmak.** Yanlış ölçen **kapının kendisiydi**,
taşıyıcı ya da hasat tasarımı değil. Ölçüm aracının yanlılığını "sonuç" diye kaydetmek, kayda
geçen sayıyı kalıcı olarak yanlış yapar.

**✅ UYGULANAN.** `scripts/cp2_harvest.py`'de kapı artık **kararlı hızı** okuyor: boru hattı
`concurrency` kalemle **dolduktan sonraki** süre ÷ o andan sonraki üretim. Huniye
`saniye_per_uretim_kararli` alanı eklendi; kümülatif `saniye_per_uretim` **eski koşularla
karşılaştırılabilirlik için duruyor** (silinmedi).

> **Ön-kayıtlı BÜYÜKLÜK değişmedi** — ölçekte s/üretim, eşik **2,88**. Değişen, o büyüklüğü ölçen
> **aletin yanlı** olduğunun anlaşılmasıdır. Ayrım raporda korunur: *eşiği kaydırmak* ile
> *tahmin ediciyi düzeltmek* aynı şey değildir.

**İkinci kusur da düzeltildi:** kapı `--limit` kontrolüne takılıp **atlanabiliyordu** → huniye
hak edilmemiş *"geçildi"* damgası düşüyordu. Sabahki `-np 64` testi (**2,93** s/üretim, eşik
2,88) tam bunu yapmıştı. Artık kapı **önce** değerlendiriliyor; hiç değerlendirilmediyse damga
`değerlendirilmedi` diyor.

### 4. `-np` seçiminin gerekçesi düzeltildi — **karıştırıcı ÇÖZÜLDÜ**

[#48](../research_log/2026-08-02-cp2c-modal-koprusu.md)'de kayıtlı *"slot sayısını ikiye
katlamak %32 kötüleştirdi"* sonucu **iki FARKLI kartı** karşılaştırmaktan doğmuştu (o dürüstlük
şerhi #48'de **zaten vardı**). Aynı kartta (`NVIDIA A100-SXM4-40GB`) ölçülenler:

| `-np` | tip | kararlı s/üretim |
| --: | :--- | --: |
| 32 | m2 | ~**2,4** |
| 32 | m2b | ~**3,0** |
| **64** | m2 | ~**2,09** |

→ **Aynı kartta slot artışı YARDIM EDİYOR.** Sabahki negatif bulgu iki hatanın toplamıydı:
(a) kart karıştırıcısı (tuzak **6.7**), (b) kümülatif ortalamanın yanlılığı (tuzak **6.8**).
Eski kayıt **üstüne yazılmadı**, ek not olarak düzeltildi.

### 5. Yeni koşu — `-np 64` (KOŞUYOR)

```
app          ap-5d1ssJOgSKZz1VNAQvxwhD        (insan kaydı: geçerli koşu)
başlangıç    2026-08-02 16:52
çıktı        hukuk-data:/cp2c-64/
kart         NVIDIA A100-SXM4-40GB
-np          64   ·  --limit 3750/tip = 7.500 üretim
kapı         düzeltilmiş (kararlı hız) · eşik 2,88 AYNI  → ADR-0050
beklenti     m2 ~2,09 · m2b ~2,6 kararlı → ~4,4 saat ≈ $11   (⚠️ TAHMİN, panelden okunacak)
```

> ### 🚨 AÇIK — **iki detached iş aynı anda, aynı dosyaya** (2026-08-02 oturumunda doğrulandı)
> `ap-LHKDDasU1MD6b4xG10WK8W` (16:47, konteyner `ta-01KZ1BP2X8SJQZEY0670S81NER`) **ve**
> `ap-5d1ssJOgSKZz1VNAQvxwhD` (16:52, konteyner `ta-01KZ1BZA1CF9BWJQXZW2CVRA6R`) **ikisi de canlı**;
> ikisinin de `--out` yolu `/data/cp2c-64/cp2c_m2.jsonl`. İkincisi `devam=24 kayıt` ile başlamış.
> Kaynak: `modal app list` · `modal container list` · iki app'in logu. Sonuç: **çift GPU maliyeti**,
> **yinelenen id riski**, ve `KUNYE.json`/huniyi **son biten iş yeniden yazar** → künye dosyayı
> tarif etmez. Bu, ayrı dizin kararının koruduğu **provenansı deler**. Karar **insanda**; hiçbir iş
> durdurulmadı. Kabul zinciri her hâlükârda **id bazlı tekilleştirme** yapmak zorunda.

**Neden AYRI dizin — provenans.** Aynı dizine yazılsaydı künye `np: 64` derken **113 kayıt
`-np 32`'den** gelmiş olacaktı. İki dizin sayesinde **iki künye de dürüst kalıyor**; kabul
aşamasında iki dosya birleştirilip **karışım künyeye açıkça yazılacak** (ADR-0047 m.2 `-np` ve
kartı zaten serbest bırakıyor).

> ⚠️ **Risk notu:** m2b m2'den ~%25 yavaş olduğu için `-np 64`'te de **kapıya yakın** koşacak.
> Takılırsa **m2 tam, m2b kısmi** kalır.

### 6. ⚠️ Verim uyarısı — regex kabul oranı **tipe göre ayrışıyor** (sayı uydurulmuyor)

ADR-0049'un ön-kayıtlı hunisi *"regex ~%30 geçer → 7.500 üretim → ~2.250 aday → ~750 temiz"*
varsayıyordu. Ölçülen:

| tip | regex kabul | varsayıma göre |
| :--- | --: | :--- |
| m2 | **%29,2** | ✅ uyumlu |
| m2b | **%19,2** | ⚠️ **altında** |
| iki tip birlikte | ~**%24** | ⚠️ altında |

→ 7.500 üretimde regex-aday beklentisi ADR'nin **2.250**'sinin altına inebilir → **750 temiz
negatif hedefi RİSK ALTINDA.** Kesin sayı hasat bitince okunacak; **şimdiden hedef
değiştirilmiyor** (tahmine dayanarak ön-kayıtlı hedefi oynatmak, m.3'te reddedilen davranışın
aynısı olur). Bağlantı: ADR-0047'nin *"ön-eleme yeterli geçerli tuzak bırakmazsa hedef otomatik
iner"* **koşullu geri alma** maddesi.

### Ders

**Bir ön-kayıtlı kapı iki bağımsız şeydir: ölçtüğü BÜYÜKLÜK ve onu ölçen TAHMİN EDİCİ.**
Sonucu gördükten sonra büyüklüğe/eşiğe dokunmak ön-kaydı yakar; tahmin edicinin yanlı olduğunu
gösterip düzeltmek yakmaz — ama ancak **yanlılık sonuçtan bağımsız kanıtlanabiliyorsa**. Burada
kanıt koşunun kendi logundaydı (600. sn 2,97 ↔ 673. sn 2,89). Bu ayrım raporda korunmazsa
dışarıdan iki hareket **aynı** görünür.

---

## Ölçülmüş ve elenmiş seçenekler — tekrar denenmez

| ne | sonuç |
| :--- | :--- |
| **Yerel `-np 8` hasat** | ❌ **1,35×** (seri 11,12 → 8,23 s/üretim; beklenen 4-6×) → 750 negatif **17,1 saat** (500 → 11,4 sa · 350 → 8,0 sa · 200 → 4,6 sa). Sebep: zorunlu kapatma **9/9**, ikinci istek **3.933 karakterlik** izi baştan prefill ediyor; ~2.150 tok/üretim, toplam **~260 tok/s**. **Düzeltilemez** — ADR-0043 rejim değişmezi (#47) |
| ~~**`-np 64` (Modal)**~~ | ⚠️ **BU SATIR ÇÜRÜDÜ (2026-08-02 16:47).** Eski kayıt: *"%32 kötüleşme (1,98 → 2,93 s/üretim), kart karıştırıcısından ayrılamadı"*. Aynı kartta (`A100-SXM4-40GB`) kararlı hız ölçülünce **`-np 64` HIZLI çıktı** (m2 ~2,09 ↔ `-np 32` m2 ~2,4). İki karıştırıcı vardı: kart (tuzak 6.7) + kümülatif ortalamanın yanlılığı (tuzak 6.8). → **elenmiş değil, yürürlükte** (#48 · defter 16:19-16:47 kaydı) |
| **Öbekli eş zamanlı istemci** | ❌ slot doluluğu **%70** (10.220/14.496 slot-s) → sürekli beslemeyle **1,84×** (#48) |
| **Havuz ön-elemesi** | ❌ **net zararlı** (isabet **0,14**) → koşulmuyor (ADR-0048 m.4) |
| **Çevrimdışı örtüşme filtresi** | ❌ elendi — `ov_gold` eşiği geçersiz oranını **%42 → %30** indirirken geçerli tuzakların **%24'ünü** kurban ediyor; verime net etki **%5.0 → ~%6.0**, `judge_flag` bilgisiz (ADR-0046 *elenen alternatif* · [`open_questions.md`](../../open_questions.md) CP2 bölümü kalem 2) |
| **Sentetik `rejected` (API)** | ❌ **YASAK** — üçüncü bir modelin hataları, Kapı 5'i çürütür (ADR-0042) |
| **`causal-conv1d`** | ❌ tavan **1,254×** < 2,0× kapısı → eklenmedi (CP0.5) |
| **Kaynak-yeterliliği önsözü (prompt alternatifi)** | ❌ M2'yi 0.968'e çıkarıyor ama M1 kütlesini **28.2**'ye düşürüyor (aşırı-red 0.6875) — tek eksende kaydırma (CP0.9 ablasyonu) |
| **Bütçeyi artırmak (düşünce sonlanmaması)** | ❌ 4096→32768 (**8×**) hiçbir şey değiştirmedi · `temp 0.6` yarısını kurtardı 🟡 · **Q8_0** ❌ (CP0) |
| **Kabul tasarımı A ($2,0)** | ❌ artık kirlilik **~%9,5**, kör damga yakalamıyor (ADR-0049 m.5) |
| **Kabul tasarımı C ($6,0)** | ❌ aynı sonuç **$2,3 fazlaya** (ADR-0049 m.5) |

---

## Doğrulanmış boru hattı (CP2-s)

```
τ_a eğitimi (--fresh-adapter, %0,65 eğitilebilir)  ✅ Modal'da koştu
norm-dengeli k-yollu TIES  (scripts/merge_ties.py) ✅ 224/224 tensör, gerçek ağırlıklarda
  operatör 4 özellikle sınandı; TIES(τ,−τ)=0 testi bir İŞARET HATASI yakaladı ve düzeltildi
GGUF Q4_K_M                                        ✅ 2,59 GiB, PURE=0
llama-server + 3 cevap                             ✅ 3/3 dolu
```

⚠️ Doğrulanmamış tek halka: **adaptörün volume'a yazılması** (smoke 6/50 adımda durduruldu,
`save_steps=100`). Risk düşük — aynı yol `train_sft.py`'de defalarca koştu (`tg_v1` onunla
üretildi). CP3 zaten kullanacak.

### CP3'te ölçülecek iki tahmin (#47)

1. **Norm asimetrisi.** `adım × lr` kabası `τ_g` 1083×1e-4 = **0,108** ↔ `τ_a` 73×1e-5 =
   **0,00073** → **~148×** olabilir (CP2-s'in sentetik kolunda **18×**'ti). Doğruysa ADR-0036'nın
   norm-dengelemesi sanılandan çok daha ağır iş yapıyor. `‖τ_a‖_F` **koşulsuz** raporlanır.
2. **Çatışan parametre oranı.** Sentetikte **%0,16** çıktı ama o kol `τ_g`'nin ölçeklenmiş
   kopyasıydı (yüksek korelasyon). Gerçek `τ_g` ↔ `τ_a` çatışması ADR-0036'nın **asıl merak
   ettiği** sayı.

---

## Kapanmış açık kalemler

| # | kalem | nasıl kapandı |
| :-- | :--- | :--- |
| 1 | **Hedef negatif sayısı** | ✅ [ADR-0047](../../adr/0047-cp2-hedef-750-modal-hasat.md): **750**, Modal, **~73 adım / 5 epoch**. ⚠️ Koşullu geri alma: ön-eleme ≥ ~8.700 geçerli tuzak bırakmazsa hedef otomatik iner *(ön-eleme koşulmadı, kalem düştü)* |
| 2 | **M2b metrik olarak sağlam mı** | ✅ CP2-r: cevaba-kör geçerli tuzak **79/80** — kurgu endişesi desteklenmedi, pilotun *"24/25 geçersiz"* bulgusu **kirli hakem artefaktıydı** |
| 3 | **M1 A1 muhafızı** | ✅ CP2-r: **0.880** (base A1 0.9777 × 0.90) |
| 4 | **`cp2_harvest.py` eş zamanlı üretime alınmalı** | ✅ #47'de `--concurrency` + `ThreadPoolExecutor` + yazım kilidi; #48'de **sürekli beslemeye** çevrildi (1,84×) |
| 5 | **Modal hasat köprüsü** | ✅ #48: `modal_train.py::harvest_cp2` + `spawn_cp2c` |
| 6 | **Kabul zincirinin sürücüsü** | ✅ #48: `scripts/cp2c_kabul.sh` (ADR-0049 m.5 tasarım B) |
| — | **Pilot CP3 koşulsun mu** (eldeki off-policy setle, ~$0.85) | ⏳ **İnsan kararı — hâlâ açık.** Öneri EVET'ti; gerekçe: `τ_a` boru hattı + `τ_g+τ_a` TIES merge hiç koşmamıştı. CP2-s bu gerekçenin **mekanik kısmını** karşıladı (zincir 4/4 doğrulandı) → kalemin aciliyeti düştü. Şerh: kafes hücresi olarak raporlanmaz, ARA KAPI okuması değildir |

### ⚪ Durdurmaz, unutulmamalı

- **İz İngilizce** — ürünün *"okunabilir muhakeme"* vaadi karşılanmıyor; `τ_g` v2'nin gerekçesi
- **Düşünce ↔ zorunlu kapatma ayrılamıyor** (base'in %94.7'si zorla kapatıldı) — Limitations
- **Ön-eleme hakeminin kendi hata payı havuza girer** (ADR-0046 sonuçlar) — Limitations
- **`τ_g` v2 mi `τ_a` mı?** ⏳ Önce `τ_a` denenir (ADR-0045 merge kontrolü tam bunu sınıyor); v2
  kararı **Sprint 2 sonu**, kafes kurulmadan önce
- **Kapı 6'yı bugün base geçemiyor** (kendi çıpası olduğu için sorun değil, ama raporlanacak)
- ~~**`-np` ölçeklemesinin karıştırıcısı** — kart ayrılamadı (#48), Limitations~~ → ✅ **ÇÖZÜLDÜ
  (2026-08-02 16:47):** aynı kartta `-np 64` hızlı çıktı. Limitations'a giren şey artık
  *"karıştırıcı vardı ve çözüldü"* + **verim kapısının bir koşuyu hatalı durdurması** (~$1,2)
- **Verim kapısı ~$1,2'lik bir koşuyu hatalı durdurdu** — ön-kayıtlı yürütme kuralları ölçüm
  yanlılığına bağışık değil; Limitations
- **m2b regex kabul oranı %19,2** (huninin ~%30 varsayımının altında) — 750 hedefi risk altında,
  kesin sayı hasat sonunda okunacak

---

## Kapılar özeti — bu sprint'te işleyenler

| kapı | nerede | kuralı |
| :--- | :--- | :--- |
| ~~CP0 düşünce kuralı~~ | CP0 ✅ | **Kapandı** — karar [ADR-0043](../../adr/0043-dusunce-modu-acik-butceli-kapatma.md) (thinking AÇIK, bütçeli) |
| ~~ADR-0040 🟢🟡🔴~~ | CP0.9 ✅ | **🟡 SARI** — M2 eşiği geçti (0.814≥0.78), M5 muhafızı İHLAL (%36.9→%42.5). **RS-FT kapsam dışı kalıyor**, ADR-0035 açılmıyor |
| ~~CP0.5 hız kapısı~~ | CP0.5 ✅ | **KALDI** — tavan 1.254× < 2.0× → `causal-conv1d` **eklenmedi**, `requirements.lock.txt` korundu |
| ~~CP2-a uyum kapısı~~ | CP2-a ✅ | **KALDI** — hakemler %58,3-%91,7 arasında dağıldı; ön-eleme **koşulmadı** ([ADR-0048](../../adr/0048-cevaba-kor-tuzak-gecerliligi.md) m.4) |
| ~~M2b kurgu tabanı~~ | CP2-r ✅ | **GEÇİLDİ: 79/80 ≫ 40/80** → merge onarımı ARA KAPI'nın 2. gözlemi olarak KALIR. *(Kural: cevaba-kör geçerli tuzak < 40/80 ise M2b tasarlandığı mod olmaktan çıkar → ADR-0045'in merge onarım kontrolü **tanımlayıcıya** iner ([ADR-0049](../../adr/0049-sprint2-kalan-kararlarin-kilitlenmesi.md) m.3))* |
| **CP2-c verim kapısı** | CP2-c | Modal koşusunun **ilk 10 dakikasında** gerçek `s/üretim` okunur; tahminin **2 katını** aşarsa koşu **DURUR**, sayı negatif bulgu olarak yazılır ([ADR-0047](../../adr/0047-cp2-hedef-750-modal-hasat.md) m.3). ⚠️ İki kez düzeltildi: (a) `limit`e takılıp **atlanabiliyordu**, (b) **kümülatif** ortalamayla ölçüyordu → 16:19 koşusunu **hatalı** durdurdu. Artık **kararlı hız** okunur (`saniye_per_uretim_kararli`); **eşik 2,88 değişmedi** |
| **ARA KAPI** | CP3 | `τ_a` tekil **M2 ≥ 0.923 · M1 A1 ≥ 0.880** **+** `τ_g+τ_a` merge **M2b ≥ 0.854** — ✅ üçü de CP2-r'de türetildi. Eski 0.934/0.888/0.887'ye karşı da raporlanır. 🚨 **ᴷ³ 2026-08-06: yürürlükteki eşikler 0.934 (askıda) / 0.8878 / 0.8649; merge 0,766 ile DÜŞÜYOR** — [#58](../research_log/2026-08-06-payda-tekillesmesi.md) |
| **Kapı 5** | Sprint 3 | ADR-0037 (3 madde) — referansları burada üretiliyor |
| **Kapı 6** | Sprint 3 | **ADR-0044 sayıları** — M5 coverage ≤ **%97.5** · ezber kütlesi ≤ **%42.5** (base, bütçeli kip) |

---

## Bütçe — **İKİ CÜZDAN, ayrı tutulur**

> ### 🚨 2026-07-30'da düzeltildi: tablo iki cüzdanı tek satırda topluyordu
> Eski tablo *"Modal cap $42.50 · harcanan $6.57 · kalan $35.93"* diyordu. **Yanlıştı.** Oradaki
> harcamaların neredeyse tamamı **OpenAI hakem** ücretiydi (GPU yereldeydi, $0), Modal'ın gerçek
> durumu ise panelde: **$35.23 / $42.50 harcanmış, kalan $7.27.** Aradaki ~$28 **emekli 12B
> hattının** eğitim koşuları — bu defterde hiç görünmüyordu. → tuzak **6.3**
>
> **Kural:** GPU ve hakem maliyetleri aynı satırda toplanmaz. Modal sayısı **panelden** okunur,
> defterden türetilmez.

### A. Modal GPU — workspace limiti $42.50

| kalem | $ |
| :--- | ---: |
| emekli 12B hattı + Sprint 1 (`τ_g`) — panelden | **−35.23** |
| **KALAN (panel, 2026-07-30)** | **$7.27** |
| CP0 · CP0.9 · CP0.5 · CP1 · CP2 pilot · CP2-a · CP2-r | **0** — hepsi yerelde ya da yalnız hakem |
| **CP2-s** smoke *(planlanan ~−0.20 · fiili, durduruldu)* | **−0.35** |
| **CP2-c** hasat *(2026-07-30 tahmini)* | ~**−3.00** *(bant ~$3-6)* |
| **CP3** `τ_a` *(eski tahmin −0.85 → ORPO ~70 s/it ölçümüyle)* | ~**−3.20** |
| **ARA KAPI'ya kadar toplam** *(eski tahminlerle)* | ~**$4.05 → sığıyor**, ~**$3.2** pay kalır *(#47'nin yeni sayılarıyla ~$6.55 → pay ~$0.7)* |
| ~~CP4 Taban A~~ · ~~CP5 Taban B~~ | ~~−12.20~~ 🔴 **2026-07-30'daki $7,27 limitiyle İMKÂNSIZDI** |
| **toplam kalan** *(2026-07-30 defteri)* | ~**$20.2** · fiili harcanan **$6.57** · cap sonrası ~**$15.7** ⚠️ bu satır **iki cüzdanı topluyordu** — tuzak 6.3, düzeltmesi yukarıda |
| ~~**CP2-c fiili** *(2026-08-02, koşuyor)*~~ | ~~~**−10.4** beklenti · `-np 32` · 7.500 üretim · ~4,2 sa~~ → koşu **kapıya takıldı**, aşağıya bölündü |
| **CP2-c denemesi** *(`-np 32`, 16:19-16:47, 🔴 kapı tetiklendi)* | ~**−1.2** ⚠️ **tahmin — panelden okunacak** (tuzak 6.3) · 468 üretim · **113 aday** korundu |
| **CP2-c hasat** *(`-np 64`, 16:48'de başladı, KOŞUYOR)* | ~**−11** beklenti · 7.500 üretim · ~4,4 sa · `hukuk-data:/cp2c-64/` |

> 🔴 **2026-07-30 kararı:** CP4-CP5 artık onay meselesi değil, **LİMİT** meselesi — $7.27 içine
> sığmıyor. **ARA KAPI'ya ulaşmak yeterli**; CP4-CP5 fatura döneminin yenilenmesini bekler.
> ✅ **1 Ağustos'ta fatura dönemi yenilendi** (panelden doğrulanır) → plan: CP2-c + CP3 + CP4-CP5
> ≈ **$21**, $42,50'ye sığar.

### B. OpenAI hakem — ayrı cüzdan

| kalem | $ |
| :--- | ---: |
| CP0.9 | −0.49 |
| CP1 | −0.15 |
| CP2 pilot | −0.01 |
| CP2-a | −0.121 |
| CP2-r | −0.23 |
| **Sprint 2'de harcanan** | **−$1.00** |
| CP2-c kabul tasarımı B *(planlanan)* | ~−3.68 |
| CP3 merge onarım ölçümü *(planlanan)* | ~−0.15 |

⚠️ **Açık kalem:** düşünce modu token maliyetini **4.5×** artırdı (249 → 1135 tok/cevap) — Modal'da
koşan her üretim işi bu oranda uzar. Ve `τ_g` v2 açılırsa eğitim ~$5.5 eklenir (**5 gerekçe**:
[`kollar.md`](../kollar.md)).

---

# Henüz koşmamış — tasarımı burada saklanan checkpoint'ler

> Bunlar **kayıt değil, spec**. `sprint2.md`'nin koşulabilir kalması için oradan buraya alındılar;
> ARA KAPI yeşilse ikinci bir `/goal` ile açılırlar.

## CP3 — FT-2 `τ_abstention` + 🔴 ARA KAPI

**TODO:** §2 · **GPU:** Modal · **$:** ~3.20 *(#47/#48 ölçümüyle; eski tahmin ~0.85)* ·
**Kayıt:** yeni `research_log` girdisi (numaralandırma **#48'den devam**)

**Rejim** — ⚠️ [ADR-0047](../../adr/0047-cp2-hedef-750-modal-hasat.md) ile **değişti**
(`TASARIM.md` §4.1.1 güncellenecek):

| | eski (ön-kayıtlı) | **yeni (ADR-0047)** |
| :--- | :--- | :--- |
| negatif | 1.495 | **750** |
| çift | 1.741 | **~937** |
| epoch | 3 | **5** |
| adım | 82 | **~73** |
| lr · etkin batch | 1e-5 · 64 | **aynı** |

**`--fresh-adapter` ZORUNLU.** Epoch 3 → 5 aşırı-uyum riski taşır: `‖τ_a‖_F` koşulsuz raporlanır,
seçim DEV'de yapılır, belirti görülürse epoch 3'e dönülür ve adım **44** olarak raporlanır.

> ### 🚨 `--fresh-adapter` neden zorunlu
> Görev-vektörü tanımı `τ = θ_ft − θ_base`. `τ_a`, `τ_g`'nin **üstüne** eğitilirse elde edilen şey
> task-vector değil **ardışık SFT**'dir — yani ölçmek için kurduğumuz şeyin ta kendisi yok olur,
> ve bunu hiçbir hata mesajı söylemez. → tuzak **3.8**

Eğitimden sonra `τ_a` **tekil** olarak 6-mod CANON'da ölçülür (merge → GGUF → aynı runtime).
Bu sayı Kapı 5'in **(b) referans noktasıdır** — onsuz *"abstention korundu mu"* sorulamaz.

## CP4 — FT-4 Taban A: tek-aşamalı **karışık** SFT

**TODO:** §2 · **GPU:** Modal · **$:** ~5.7 *(SFT tahmini #48'de doğrulandı — ayakta)* ·
**Kayıt:** yeni `research_log` girdisi (numaralandırma **#48'den devam**)

Grounding + abstention verisi **tek koşuda karıştırılarak** eğitilir. `rejected` havuzu CP2'den
(tek havuz kuralı). Ham base'den.

> ### 🚨 Adil kıyas şartı (ADR-0037)
> **Aynı seçim prosedürü tabanlara da uygulanır** — Taban A için de DEV'de en iyi checkpoint
> seçilir. Yoksa biz taranmış, onlar taranmamış olur ve `D > A` tipi **değersiz** bir iddia çıkar.

6-mod CANON'da ölçülür (harness **kapalı** — iç ablasyon).

## CP5 — FT-5/FT-6 Taban B: **ardışık** SFT + on-policy kontrol

**TODO:** §2 · **GPU:** Modal · **$:** ~6.5 *(SFT tahmini #48'de doğrulandı — ayakta)* ·
**Kayıt:** yeni `research_log` girdisi (numaralandırma **#48'den devam**)

**FT-5** (aşama 1: grounding, ham base'den) → **FT-6** (aşama 2: abstention, FT-5'in üstüne).

**İki koşu, ADR-0042:**

| koşu | `rejected` kaynağı | nerede raporlanır |
| :--- | :--- | :--- |
| **FT-6 ana** | CP2 havuzu (base'den) | **ana tablo** — veri sabit, fark yönteme atfedilir |
| **FT-6 kontrol** | **FT-5'in kendi çıktısından** (on-policy) | **robustluk satırı** — ~$0.65 |

> ### 🚨 Neden kontrol koşusu var
> Ana koşuda Taban B **off-policy** veriyle eğitiliyor — negatif örnekler FT-5'in modelinin
> gerçekten söylediği şeyler değil → taban **zayıf eğitilir** → sapma **bizim lehimize**.
> *"Tabanı zayıf eğittiniz"* itirazı Kapı 5'in tamamını çürütebilir; $0.65'e sigortalanıyor.

**Ön-kayıtlı yorum kuralı:** on-policy taban, veri-sabit tabandan bileşik ölçütte **≥ +0.05**
iyiyse, Kapı 5'in *"iki tabanı da geç"* şartı **on-policy sürüm** üzerinden okunur — yani daha
güçlü tabana karşı kazanmamız gerekir.

---

## Sprint 2 çıkışında elde ne olacak

| | |
| :--- | :--- |
| Kol | **2** — `τ_g` (var) + `τ_a` (yeni), ikisi de ham base'den, ikisi de tekil ölçülmüş |
| Taban | **2** — karışık SFT · ardışık SFT (+ on-policy kontrol) |
| Zemin | Hakem istemi düzeltilmiş, üç özne yeniden puanlanmış · `rejected` havuzu temiz |
| Cevaplanmış | ✅ `τ_g` reçetesi fazla sert **değildi** — ama kazanç **yalnız kendi istem ailesinde** (#43) · ✅ düşünce modu **bütçesiz çalışmıyor** · ✅ bütçeli düşünce **ayırt etmeyi** artırıyor, biçim değil (ablasyon) · ✅ ADR-0040 **🟡** |
| Sprint 3 hazır | Kapı 5'in (a) ve (b) referans noktaları · Kapı 6'nın base çıpası · iki taban |

2 kol (`τ_g` v1 + `τ_a`) · 2 taban (karışık + ardışık, + on-policy kontrol) · hepsi aynı
protokolde, aynı veriyle, tekil ölçülmüş → **Sprint 3'ün kafesi kurulabilir.**

---

# 🟢 SPRINT 2 KAPANIŞI — 2026-08-03

## ARA KAPI: GÜÇLÜ YEŞİL

```
1. GÖZLEM  τ_a tekil  M2 Rej = 0,984  ≥ 0,923   ✅   ← ᴷ⁴ (payda 66): 0,955 ≥ 0,923 ✅ AYAKTA
           muhafız    M1 A1  = 0,9697 ≥ 0,880   ✅
2. GÖZLEM  tgta_v1    M2b    = 0,877  ≥ 0,854   ✅   geçerli koşu (kesik %0,4)
§20 şartı  merge cevaplamayı bıraktı mı?         ❌   HAYIR (71,6% ↔ τ_g 71,4%)
```

> 🚨 **ARA KAPI 2. GÖZLEMİ YENİDEN TÜRETİLDİ 2026-08-06 (kusur K-2) — HÜKÜM DEĞİŞTİ.**
> Yukarıdaki ✅ **o günün aletiyle doğrudur ve silinmedi.** Düzeltilmiş cevaba-kör paydayla
> (K3 + K-1) aynı ön-kayıtlı formül şunu veriyor:
> `eşik = 0,90 × base M2b 0,961 = **0,8649**` · `merge (ham TIES) M2b = **0,766**`
> → **🔴 DÜŞTÜ, 9,9 puan altında.** Eski eşiğe (0,887) karşı da düşüyor. Paydalar eşit
> (77 ↔ 77), yani kıyas geçerli. ⛔ ADR-0050 gereği eşiğe/çarpana/formüle **dokunulmadı**;
> bu satırın kendi kuralı (m.1) zaten *"ön-kayıtlı olan formül, sayı değil"* diyordu.
> Türetme: `outputs/eval/cp2-r-kor-payda/ara_kapi_esikleri_2026-08-06.json` ·
> [#58](../research_log/2026-08-06-payda-tekillesmesi.md).
> **Bu kapı CP4-CP5 harcamasını yetkilendiren kapıydı — yetki bugünkü ölçümle YOK.**
>
> ⚠️ ~~1. GÖZLEM'in paydası hâlâ modele bağımlı — askıda.~~ → ✅ **ÖDENDİ VE TÜRETİLDİ
> 2026-08-06 (KARAR-3, hakem $0,1054).** m2 paydası on koşuda birden eşitlendi (**66/70**,
> eskiden 55-63). Aynı ön-kayıtlı formülle:
> `eşik = base M2 0,803 + 0,12 = **0,923**` · `τ_a tekil M2 = **0,955**` → **✅ GEÇTİ (+3,2 p)**;
> muhafız `A1 0,9697 ≥ 0,90 × 0,9777 = 0,8799` → **✅**. Ön-kayıtlı ham sayılara karşı da
> geçiyor (0,955 ≥ 0,934 · 0,9697 ≥ 0,888). ⛔ ADR-0050: eşiğe/çarpana/formüle dokunulmadı.
> 🚨 **Not — bu ✅ ilk kez BİRİM-TUTARLI:** yukarıdaki 0,984 ≥ 0,923 kıyası **karışık birimdi**
> (pay özneye bağlı paydadan, eşik #46'nın kör çıpasından). Şimdi iki taraf da aynı aletten.
>
> ### ⇒ ADR-0045 §3'ün ön-kayıtlı tablosunda satır: **✅ ❌ → DUR**
> *"Kol tek başına iyi ama birleşince taşımıyor; iç iddianın öncülü sorunlu."* Karar iki
> olası satırda da DUR'du, ama artık **hangi** satır olduğu belli: sorun `τ_a`'nın kalitesi
> değil, **merge'in onu taşımaması**. CP4-CP5 harcaması bu kapıdan yetki **almıyor**.
> Türetme: `outputs/eval/karar3-m2-payda/m2_payda_2026-08-06.json`.

🛑 **CP4-CP5 koşulmadı** — insan başka bir zamana erteledi. Yeni `/goal` gerektirir.

## Ölçülen tablo — hepsi aynı protokol, hepsi geçerli koşu

```
özne          cevaplanan  aşırı-red      A1   M1 kütle  M2 Rej ᴷ⁴  M2b Rej ᴷ³  tok/cevap
base             46/80       0,425   0,9864     56,7%    0,803      0,961        1192
Gemini 3.1 FL    61/80       0,237   0,9561     72,9%    0,848      0,883          —
τ_g v1           66/80       0,175   0,8658     71,4%    0,833      0,506 🔴       —
τ_a v1           34/80       0,575   0,9697     41,2% 🔴 0,955      0,987        ~1084
tgta_v1 ⭐       63/80       0,212   0,9087     71,6% ✅ 0,833      0,766 ✅       714

ᴷ⁴ M2 eski (özneye bağlı payda 55-63): base 0,814 · Gemini 0,930 · τ_g 0,873 · τ_a 0,984 · tgta_v1 0,893
```

> 🚨 **DAMGA 2026-08-06 — `M2b Rej` sütununun TAMAMI emekli birimde.** Paydası modelin
> cevabına bakan hakemden geliyordu (K3, [#57](../research_log/2026-08-06-cekinme-aleti-onarimi.md)).
> Yürürlükteki payda **77/80**, aynı sınavı paylaşan her kolda eşit. Çeviri:
> base **0,986 → 0,961** · Gemini **1,000 → 0,883** · `τ_g` **0,607 → 0,506** ·
> `τ_a` **0,987 → 0,987 (değişmedi)** · `tgta_v1` **0,877 → 0,766** (ve ✅'i **🔴** olur — K-2).
> ᴷ⁴ ~~`M2 Rej` sütunu HÂLÂ ONARILMADI~~ → **ONARILDI 2026-08-06 (KARAR-3, $0,1054).** Aynı 70
> kalemlik sınavda on kol **55-63** arası payda gösteriyordu; hepsi **66/70**'e eşitlendi.
> ⚠️ **Bu düzeltmenin yönü BİZİM LEHİMİZE ve öyle raporlanıyor:** en çok kayan özne **RAKİP**
> (Gemini −8,2 puan ↔ biz −6,0), `tgta_v1`–Gemini açıklığı **3,7 → 1,5 puana** daralıyor —
> kirli paydadan en çok Gemini yararlanıyordu (#46'nın aynı sınıftaki bulgusunun **tersi** yön,
> o tur aleyhimizeydi). Kaynak: `outputs/eval/karar3-m2-payda/m2_payda_2026-08-06.json`.
> `A1` / `M1 kütle` / `aşırı-red` sütunları `valid_trap`'ten **etkilenmez**, aynen geçerli.

## Sprint 2'nin dört ana bulgusu

**1. Grounding-Abstention paradoksu simetrik.** Defterde #07 *"grounding eğitimi çekinmeyi
öldürür"* vardı; bu sprint eşini ölçtü — `τ_a` grounding'i çıplak base'in **altına** indirdi
(41,2% ↔ 56,7%). İç iddianın öncülü artık varsayım değil **veri**.

**2. Merge çatışan becerileri birlikte taşıyor.** `tgta_v1`, `τ_g`'nin grounding'ini **tamamen**
koruyup (71,4% → 71,6%) onun M2b çöküşünün **%57'sini** ~~%71'ini~~ onardı
(**0,506 → 0,766** ᴷ³ ~~0,607 → 0,877~~).

> 🚨 ᴷ³ **BU SATIRIN M2b SAYILARI ESKİ ALETİN BİRİMİNDEYDİ** (düzeltildi 2026-08-06, kusur K2).
> Kör-payda onarımı üç girdiyi de yeniledi (base 0,986→0,961 · `τ_g` 0,607→0,506 · merge
> 0,877→0,766), bu yüzden `(merge − τ_g)/(base − τ_g)` oranı da **%71,2 → %57,1** oldu.
> Sıçramanın kendisi değişmedi (**+0,26**). Eski sayılar denetim izi olarak duruyor.

**3. ADR-0036'nın hükmü tersine döndü → [ADR-0052](../../adr/0052-merge-norm-dengeleme-hukmu-tersine.md).**
Norm dengeleme *gerekli* diye yazılmıştı; ölçüm `τ_g`'yi ezdiğini (71,4% → 53,4%) ve yüksek
ölçekte modeli **dejenere** ettiğini gösterdi. Gerekçesi (8,87× asimetri) ayakta, çıkarımı
(*"dengelenmezse `τ_a` silinir"*) çürütüldü. **Ana sonuç artık ham TIES.**

**4. Ön-kayıt dört kez tuttu.** #48 §16 (`rewards/accuracies` yanıltıcı olabilir) · §17 (A1
cevaplanan-only olduğu için coverage çöküşünü gizler) · §20 (aynı kör nokta merge tarafında da
var) — üçü de sayı görülmeden yazıldı, üçü de doğrulandı. Dördüncüsü: ADR-0040 geçerlilik
kapısı, bozuk bir modelin sayılarına güvenilmeden önce yakaladı.

## Yeni yürütme tuzakları

| # | özet |
| :-- | :--- |
| **6.10** | iki detached iş aynı çıktı dizinine yazar |
| **6.11** | devam mekanizması yalnız KABUL edilenleri hatırlar → ek tur sessizce boşa gider |
| **6.12** | bayrak script'e eklenir, çağrı zincirine eklenmez (bu turda **dört kez** çıktı) |

## Bedel

```
Modal GPU     ~$9-10   (hasat 2 tur + τ_a eğitimi)   ⚠️ panelden okunacak
OpenAI hakem   $5,11   (kredi TÜKENDİ 2026-08-03 09:37)
OpenRouter     $2,97   (ek tur kabul zinciri + tüm CP3 evalleri + süpürme)
merge süpürme  GPU $0 · hakem $0,11 · ~2 saat        (3 varyant, DEV)
```

## Sprint 3'e devredilen

- **`tgta_v1`** — ana sonuç merge, kimliği [`kollar.md`](../kollar.md)'de
- **`τ_a` v1** — 70 adım, `‖τ_a‖_F` = 1,1806, 726 çift
- **`scripts/cp3_merge_dene.sh`** — varyant → GGUF → 3 eksen eval → puanlama, tek komut
- **`merge_ties.py --geri-olcek {ortalama|min|max|<kol>}`** + künyede `geri_olcek_kurali`
- **Açık soru:** modül-başına normalleştirme denenmedi (`open_questions.md`) — ham TIES'in
  `τ_a`'yı seyreltmesini (0,987 → 0,877 ᴷ³ **düzeltilmiş: 0,987 → 0,766**) telafi edebilir
- **Açık iş:** CP4 (karışık SFT) + CP5 (ardışık SFT) — iç iddianın **gerçek** sınavı
