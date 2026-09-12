# `docs/superpowers/` — iş sırası

> Bu klasörün **giriş dosyası** ve **tek durum kaynağı**. Neyin şimdi, neyin sonra olduğunu
> söyleyen tek yer.
>
> **Bu dosya bir HARİTA, bir plan değildir.** Kutucuk taşımaz. Bir işi sıradan çıkarmak ya da
> araya sokmak **insan kararıdır** — kendi başına yapma.

---

## Bir bakışta

| # | iş | durum |
| :-- | :--- | :--- |
| **1** | **`v1-son-iş`** — `v1.0`'ı kapatan tur | ⏭️ **SIRADAKİ** · planı **yazılmadı**, grill'den çıkacak |
| **2** | **`v2-RL-GRPO`** — `tgta_v1` üstüne GRPO + düşünce ayarı | ⏸️ **DURUYOR** · planlanmadı, açılmayacak |

**Klasör 2026-09-12'de boşaltıldı.** Kapanan iki plan ve iki spec **silindi**; taşıyıcı içerikleri
[ADR-0083](../adr/0083-kusur-sicili-adrye-tasindi.md)'e alındı — **32 kusurun sicili**, **devir
tablosu** ve silinen tasarımın **mimari özü**. Gerekçe ve kabul edilen bedel (29 bağlantının 9'u
öldü) o ADR'de yazılı.

---

## 1 · `v1-son-iş` — SIRADAKİ

### `v1.0`'ı bugün ne engelliyor — **tek şey**

**Engel model değil, ÖLÇÜM AYGITI.** [ADR-0077](../adr/0077-v1-0-verilmedi-v0-3.md):
[ADR-0064](../adr/0064-v1-kapisi-uc-maddeli-on-kayit.md)'ün saydığı iki eksikten **(a) kabul
testi** 2026-09-09'da **kapandı**; geriye **(b)** kaldı — *her sayı hâlâ **tek hakem ailesinin**
hükmü*. κ `tam_sadık` **0,534** · `atıf_temiz` **0,409**, aracın eşiği **0,6**.

Borcun kapanma koşulu [ADR-0074](../adr/0074-hakem-paneli-kuruldu-baglayici-hukum.md)'te
**tek cümledir**:

> *"`3.5 Flash` kolunun **aynı ikinci hakemle** puanlanması."*

| | |
| :--- | ---: |
| bedel (ADR-0074'te ölçülmüş) | **$2,81** |
| OpenRouter bakiyesi (2026-09-12) | **$2,0410** |
| **açık** | **−$0,77** |

⚠️ Tahmin **tabakalanmış duman koşusundan yeniden türetilmeli** — tuzak **1.11**: 2026-09-09'da
`n=5`'ten yapılan doğrusal tahmin **$0,82** dedi, gerçek **$1,1932** tuttu ve `$1` kapısı
**%45** aşıldı.

### Turun içeriği — grill belirleyecek

Girdiler hazır, **plan yazılmadı**:

| girdi | nerede |
| :--- | :--- |
| silinen tasarımın **mimari özü** + grill'e girecek **9 madde** | [ADR-0083](../adr/0083-kusur-sicili-adrye-tasindi.md) §EK |
| **8 açık kusur** — 5a · 10 · 23 · 24 · 25 · 27 · 29 · 31 | [ADR-0083](../adr/0083-kusur-sicili-adrye-tasindi.md) |
| **3 devredilen** — **6** → `B1` · **11** → paket · **12b** → `B11` | ″ |
| κ borcu | ADR-0074 · ADR-0077 |

⭐ **Grill'e girmeden bilinmesi gereken tek düzeltme:** silinen tasarımın hedef sayısı
(**340.303 madde**) **yanlıştı** — `KANUN` satırı `917 × 102,7` sayıyordu, oysa korpustan ölçülen
gerçek oran **45,4 madde/belge**. Düzeltilince hedef **~287,6-287,8 bin** oluyor ve tasarımın
kendi kat merdiveninin **288.156**'sıyla **%0,13-0,20** farkla örtüşüyor. **Merdiven baştan
doğruymuş**; hedefi kaydıran tek bir satırdı. Ayrıntı ve üçüncü tutarsızlık ADR-0083 §EK'te.

### Sıra — insan tarafından kilitli (2026-09-12)

```
1 · inceleme          BİTTİ
2 · tazeleme          BU TUR — docs/superpowers boşaltıldı, işaretçiler onarıldı
3 · 00-IS-SIRASI      BU DOSYA
4 · GRILL             tek yeni plan, YALNIZ v1-son-iş        ← insan oturumu
5 · master'a al, push
6 · planı EXECUTE
7 · bekleyen commit'leri push
8 · PUBLIC kontrolü   repo + HF
9 · her şey PUBLIC    HF görünürlüğü açılır
```

---

## 2 · `v2-RL-GRPO` — DURUYOR, planlanmayacak

```
v1   ham base ──► SFT (τ_g) + ORPO (τ_a) ──► ham TIES ──► tgta_v1 ──► YAYIN
v2   tgta_v1 (bf16) ──► GRPO + düşünce (thinking) ayarı ──► v2.0
```

**`v1` SFT ile KAPANIR** ([ADR-0075](../adr/0075-v1-sft-kapanir-v2-sequential-rl.md)) —
`B1`/`B4` eğitim turları **koşulmaz**. İkisinin gerekçesi ayrıdır ve ölçülmüştür: `B1`'de
rakiplerden **geride değildik** (8/80 ↔ 8·8·7·8); `B4` bir **merge** kaybıdır ve `v2`'de merge
olmadığı için **konusuz** kalır.

**Bedeli yazılıdır:** `τ = θ_ft − θ_base` tanımı tüm kolların **aynı base'i** paylaşmasını şart
koşar ⇒ `tgta_v1`'i yeni başlangıç almak bunu bozar ⇒ **task-vector hattı `v1`'de DONDURULUR**,
`v2`'ye taşınmaz. `v2`'nin iddiası merge değil **RL kazancıdır**.

**`v2`'ye devredilenler:** `B1` (misattribution — ⚠️ bu turda **ağırlaştı**: fp16 rejiminde
`wrong_ref_rate` **2,0×** kötüleşiyor) · `B11` (iskele işaretlerinin **kaynağı** eğitim verisi) ·
araç kullanımının **öğrenilmesi** (GRPO ödülüne *"doğru aracı doğru anda çağırdı mı"* girer) ·
**S9** (barındırma) · web arayüzü.

---

## Durum künyesi — 2026-09-12

```
sürüm      v0.3 (ürün) · artefakt HakHukuk-4B-v0.1 · ağırlıklar HF'te ÖZEL
test       281 yeşil, 2 xfail
dal        master push'lu · docs-tazeleme açık
kayıt      ADR 0001-0083 · research_log #1-#67 · tuzak defteri 1.1-7.x
```

**Kapanan son tur** (`hp` → Hat A → Hat B, **115/115**, 2026-09-12): hakem paneli kuruldu ve κ
**ilk kez** ölçüldü · Sonnet-5 rakip havuzuna girdi ve **önde** (0,8348 ↔ 0,8011) · donmuş TEST
**tek kez** açıldı (0,5804) · `hakhukuk/` paketi doğdu (CLI · TUI · HTTP API · araç katmanı) ·
konteyner **uçtan uca çalışıyor** · ürün yolunda boş cevap **4/80 → 0/80**.
Anlatısı [#66](../record/research_log/2026-09-11-urun-yuzeyi-ve-aygit-kusurlari.md) ve
[#67](../record/research_log/2026-09-12-konteyner-ve-alet-onarimlari.md)'de.

### O turun üç dersi — sıradaki tur bunları taşır

**① Ürün yüzeyini temizlemek ÖLÇÜM AYGITINDA kusur bulur.** Atıf doğrulayıcı kanun adını gevşek
eşleştirip **yanlış kanuna `DOGRULANDI`** basıyordu (tuzak **1.13**). Onarıldı (**7/16 → 0/16**),
çıpalar yeniden puanlandı: `0/114` ve donmuş TEST `0/52` **oynamadı** — ama korunmanın **aletten
değil ÖRNEKLEMDEN** geldiği ortaya çıktı.

**② Aleyhe çıkan sonuç da yazılır.** Rakipler de yeniden puanlandı: `3.1 Flash-Lite`
**1/152 → 0/153**. Tek deterministik üstünlüğümüzde artık **eşitiz**; karşılığında **eşit sınav**
alındı ([ADR-0057](../adr/0057-harness-rekabet-kapisi-esit-sinav.md)).

**③ Sayısal kapı TESTİN KÖRLÜĞÜNÜ görmez.** Üç insan gözü kapısı, **süit yeşilken duran dört
kusuru** yakaladı (**26 · 27 · 28 · 30**) ve **ikisi aynı gün yazılan koddandı** — testler onları
görmedi çünkü kusurun *görülmediği* varsayımla yazılmışlardı.

---

## Bakım kuralı

Bir iş kapandığında **iki yer** güncellenir: işin kendi kapanış kaydı ve **bu dosyanın
"Bir bakışta" tablosu**. Sıra değişirse **gerekçe buraya yazılır** — sıra değişikliğinin *niçin*i
başka hiçbir yerde durmuyor.

**Kapanan plan yeniden işletilmez.** Kapanış anında açık kalan **her** kusur **adıyla** devredilir;
devredilmemiş açık kusur varsa **kapanış geçersizdir**. Sicil ve devir
[ADR-0083](../adr/0083-kusur-sicili-adrye-tasindi.md)'te.
