# ADR-0048 — Tuzak geçerliliği **cevaba kör, kalem düzeyinde, bir kez** hesaplanır · ön-eleme koşulmaz

**Statü:** Yürürlükte · **Tarih:** 2026-07-30
**Otorite belge:** `TASARIM.md` §3.4 (hakem savunması) · `sprint2.md` CP2
**Değiştirir:** [ADR-0046](0046-cp2-kabul-olcutu-hakem-ve-havuz-on-elemesi.md) **m.2 ve m.4 SÜPERSED** (m.1 ve m.3 ayakta)
**Etkiler:** ADR-0037 (Kapı 5 çekinme ekseni) · ADR-0045 (ARA KAPI) · ADR-0040 (🟡 hüküm) · ADR-0011 (A1/coverage) · ADR-0047 (aritmetik)
**Kanıt:** `research_log` [#45](../record/research_log/2026-07-30-cp2a-hakem-capalanmasi.md) ·
`outputs/eval/cp2-on-eleme/KUNYE.json` · iç kontrol: `outputs/eval/cp09-butceli-1024-512/abst_m3_*_summary.json`
**Tuzak kaydı:** `yurutme-tuzaklari.md` **2.14** · **2.15** · **4.8 güncellendi** · **2.6 yetersiz işaretlendi**

> ## ⚠️ ÖN-KAYIT ŞERHİ
> Karar **`τ_a` eğitilmemişken**, hiçbir merge hücresi üretilmemişken ve **ARA KAPI okunmamışken**
> verildi. **Hiçbir eşiğe dokunulmadı** (ARA KAPI M2 ≥ 0.934 · M1 A1 ≥ 0.888 · merge M2b ≥ 0.887 ·
> Kapı 5 · Kapı 6). Değişen: bu eşiklerin okunacağı **paydanın nasıl hesaplandığı** — ve bu
> düzeltme her özneye, her kola, her hücreye **aynı biçimde** uygulanır.

---

## Bağlam — ölçmek için kurulan kapı, ölçüm aracının kendisini kırdı

ADR-0046 m.3, üretim ön-elemesini bir uyum kapısına bağlamıştı: *cevabı görmeyen ön-eleme hakemi ile
cevabı gören denetim hakemi `source_answers` ekseninde aynı şeyi mi söylüyor?* Kapı $0,12'ye koştu
ve **iki şey birden** buldu.

### 1. Çapalanma ölçüldü — ve hakem gücüne bağlı

Aynı 36 kalem, 2×2 tek değişkenli tasarım (`n=36`, seed 3407, trap_clip 900):

| hakem | cevabı görüyor | geçerli tuzak | kayma |
| :--- | :-: | --: | --: |
| `gpt-4o-mini` | ❌ | 80,6% | |
| `gpt-4o-mini` | ✅ | **58,3%** | **−22,3 p** |
| `gpt-4o` | ❌ | 91,7% | |
| `gpt-4o` | ✅ | 83,3% | −8,4 p |

Cevabı görmek her iki hakemi de aşağı çekiyor, ama **mini'yi üç kat şiddetli**. Sebep yapısal:
denetlenen küme tanım gereği *modelin kendinden emin cevap verdiği* örnekler, hakem her seferinde
dolu bir cevap görüp *"demek ki kaynak cevaplıyormuş"* diye geriye çıkarım yapıyor.
κ(`gpt-4o` görmez ↔ `gpt-4o-mini` görür) = **0,097**.

### 2. ⭐ Asıl bulgu: `valid_trap` kalemin değil, **öznenin** özelliği olmuş

`valid_trap` çekinme metriğinin **paydası** — ve her özne için **yeniden** yargılanıyor.

**İç kontrol (hakem kıyası gerektirmeyen kanıt).** `cp09-butceli-1024-512/`, M3, üç özne,
**id kümeleri birebir aynı**:

| koşu | n | `valid_trap` |
| :--- | --: | --: |
| `abst_m3_base_th` | 80 | 54 |
| `abst_m3_gem_th` | 80 | 56 |
| `abst_m3_tg_v1_th` | 80 | **39** |

Aynı 80 kalemin **19'unda** etiket özneye göre değişiyor. **Ve M3'te doğru cevap tanım gereği
biliniyor** — `gen_eval_grounded.py:473-476`, `--empty-context` altında bağlam
`"(İlgili kaynak bulunamadı.)"`, yani kaynak metni **yok**: `valid_trap` **80/80** olmalıydı.

Etiketin kendi gerekçesiyle çelişmesi sistematik: `cp09` çekinme koşularında `valid_trap=False`
etiketli **172** kalemin **37'sinde (%22)** gerekçe *"kaynak bu bilgiyi vermiyor / belirtilmemiş"*
diyor.

### 3. Sapma tek yönlü değil — **yön değiştiriyor**

| koşu | RED (raporlanan) | RED (filtresiz) | fark |
| :--- | --: | --: | --: |
| m2b gem | 1,000 | 0,850 | **+0,150** |
| m2b `τ_g` | 0,607 | 0,525 | +0,082 |
| m3 `τ_g` | 0,923 | 0,800 | **+0,123** |
| m3 base / gem | 1,000 | 1,000 | +0,000 |

- **M2b'de rakibi bizden çok kayırıyor** → `gem` ↔ `τ_g` açığı 0,325 iken **0,393** raporlanmış:
  **aleyhimize 7 puan**.
- **M3'te tersi** → açık 0,200 iken **0,077** raporlanmış: **lehimize 12 puan**.

Ön-kayıtlı bir karar kuralı için gürültünün en kötü türü: **kapının hangi tarafa kaydığı önceden
bilinemez.**

---

## Karar

### 1. Tuzak geçerliliği **cevaba kör, kalem düzeyinde, bir kez** hesaplanır ve önbelleğe alınır

```
ESKİ: her özne skorlanırken hakem (soru, kaynak, ÖZNENİN CEVABI) görüp valid_trap üretir
YENİ: valid_trap bir kez (soru, kaynak) çiftinden üretilir → kalem düzeyinde önbellek
      özne skorlaması onu OKUR, yeniden sormaz
```

Gerekçe tanımdan gelir: *bir tuzağın geçerliliği kalemin değişmez bir özelliğidir; öznenin
cevabına bağlı olamaz.* Bu bir kalibrasyon tercihi değil, tanım hatasının düzeltilmesi.

### 2. Mod tanımından çıkan geçerlilik **hakeme sorulmaz, sabitlenir**

M3 (`--empty-context`) bağlamı boştur → `valid_trap = True`, **80/80**, hakem çağrısı yok.
Gereksiz gürültü **ve** para.

### 3. **Hakem cevabı görüyor mu** — dört katmanlı savunmaya YENİ eksen

`TASARIM.md` §3.4'ün dört katmanı (hakemsiz omurga · 3-aile panel · aile dışlaması · öz-tercih)
bu eksenİ kapsamıyordu. Filtre/payda üreten her hakem çağrısı bundan sonra şu soruyla denetlenir:
*bu etiket öznenin cevabından etkilenebilir mi?* Etkilenebiliyorsa **cevaba kör** hesaplanır.

### 4. Ön-eleme **KOŞULMAZ** — ADR-0046 m.2 SÜPERSED

Ön-eleme 36 kalemden 7'sini kesiyor; güçlü hakem referansında o 7'nin isabeti **0,14** (1/7) ve
**6 geçerli tuzak** boşa atılıyor. Her iki referansta filtre, eleyeceği geçersizden **daha fazla
geçerli** tuzak atıyor. Ayrıca premisi (%42 geçersiz) artefakt çıktı — gerçek **%8,3–16,7**.

### 5. `chosen` tarafının ayrı denetimi **gereksiz** — ADR-0046 m.4 SÜPERSED

Havuz %42 değil ~%17 kusurlu ve düzeltme m.1'in kabul hakemine gömülüdür. Ayrı bir denetim koşusu
gerekçesini kaybetti.

### 6. Etkilenen kayıtlar **yeniden puanlanır, silinmez**

`outputs/eval/*/abst_*_summary.json` — **22 çekinme koşusunun 21'i** cevabı gören kipte puanlandı
(`sprint1-thinking-off/` · `cp09-butceli-1024-512/` · `cp09-ab-ayrimi/` · `cp2-rejected-hasat/`).
Hepsinin paydası özneye bağlı. **Eski sayılar korunur ve yanına düzeltilmiş sayı yazılır** — hangi
sayının hangi paydayla üretildiği görünür kalır.

**Doğrudan düzelen:** M3 için doğru payda 80/80 → base **1,000** · gem **1,000** · `τ_g` **0,800**.
#43'te `τ_g` için 0,923 yazılmıştı; çelişki **#43 ve #45'te işaretlendi**.

### 7. Ön-kayıtlı eşikler **değişmiyor** — hüküm kontrol edildi

ADR-0040'ın 🟡 hükmü M2 eşiğine (0,814 ≥ 0,78) dayanıyordu; **filtresiz değer 0,786 — eşiği hâlâ
geçiyor, hüküm değişmiyor.** ARA KAPI ve Kapı 5 eşiklerine dokunulmadı; düzeltme her özneye aynı
biçimde uygulandığı için kıyas simetrisi korunur.

> 🚨 **ᴷ⁴ ÜÇÜNCÜ KEZ KONTROL EDİLDİ 2026-08-06 (Ö3).** `m2` paydası özneye bağlı olmaktan çıkıp
> **66/70**'e eşitlendi (KARAR-3, [#59](../record/research_log/2026-08-06-m2-paydasi-ve-karar-4.md)):
> base M2 **0,814 → 0,803**. **Eşiği hâlâ geçiyor (0,803 ≥ 0,78) → ADR-0040'ın 🟡 hükmü ayakta.**
> ⛔ Eşiğe dokunulmadı (ADR-0050) — yalnız girdi yeniden puanlandı. Eski değerler silinmedi.
> ⚠️ ARA KAPI için aynı şey **söylenemez**: 2. gözlem ᴷ³ ile düştü (bkz. ADR-0045 · ADR-0052).

---

## Bunun ADR-0047 aritmetiğine etkisi — **lehimize**

`gpt-4o` aynı 36 kalemde **12** gerçek negatif buluyor, mini **6**. Yani verim %5,0 değil **%10,0**
— mini geçerli tuzakları geçersiz sayarak gerçek fabrikasyonların yarısını çöpe atıyordu.

| | eski varsayım | ölçülen |
| :--- | --: | --: |
| verim | %8,6 *(tahmin)* | **%10,0** |
| 750 hedef için üretim | 8.721 | **7.500** |
| tek akış süre | — | 23,2 sa |
| Modal `-np 32` (10-20×) | ~1,4 sa | **~1,2-2,3 sa** |
| ön-eleme maliyeti | $1,26 | **$0** |

ADR-0047'nin ~1,4 sa tahmini **ayakta, ama başka sebeple.** Koşullu geri alma tetiklenmedi
(havuz 19.284 kalem ≫ 7.500).

## ⏳ Açık bırakılan — kabul hakeminin seçimi

Verdict ekseninde iki hakemin uyumu **0,857** (36'da 3 ayrışma) — yani ADR-0046 m.1'in dayandığı
eksen **sağlam**. Ama hangi hakemin kabul kararını vereceği açık:

| tasarım | maliyet | sorun |
| :--- | --: | :--- |
| saf `gpt-4o` | ~$4,3 | pahalı |
| saf `gpt-4o-mini` | ~$0,26 | fabrikasyonların yarısını kaçırır → GPU süresi 2× |
| **hibrit** *(önerilen, karara bağlanmadı)* | ~$2,0 | kabul = yalnız verdict (mini) · geçerlilik nihai kümede bir kez `gpt-4o` ile · ham ~900 → temiz ~750 |

**Bu ADR bunu çözmez.** Hibrit tasarım insan onayına sunulacak ve kendi ADR'sini alacak.

---

## Reddedilen seçenekler

| seçenek | neden reddedildi |
| :--- | :--- |
| **Ön-elemeyi zayıflığına rağmen koş** (FN=0, "bedeli sıfır") | FN=0, *zayıf* referansa göreydi. Güçlü hakem referansında filtre **net zararlı**: kestiği 7 kalemin 6'sı geçerli tuzak (isabet 0,14) |
| **Etkilenen 21 koşuyu sil, baştan puanla** | Eski sayılar makale kanıtı; hangi sayının hangi paydayla üretildiği **görünür kalmalı**. Yeniden puanlama eskinin *yanına* yazılır |
| **`valid_trap`'i tamamen kaldır, tüm kalemleri paydaya al** | Geçersiz tuzakta çekinmek YANLIŞ davranıştır; payda gerçekten süzülmeli. Kusur süzmede değil, süzgecin **öznenin cevabını görmesinde** |
| **Eşikleri düzeltilmiş paydaya göre yeniden hesapla** | Veri görüldükten sonra eşik oynatmak kapının anlamını yok eder. Düzeltme **her özneye aynı** uygulanıyor, simetri korunuyor → eşikler durur |
| **2.6 yeterliydi, yeni tuzak gerekmez** | 2.6 kaymayı *görünür* kılıyordu (*"oranı paydayla yaz"*), **gidermiyordu**; nedenini, tanımsal kanıtını ve yön değiştirdiğini kaçırmıştı → **yetersiz** işaretlendi |

## Sonuçlar

- ✅ Ön-eleme koşulmadı → **$1,26 harcanmadı**, ve ondan büyük bir tasarım hatası önlendi.
- ✅ Verim %5,0 → **%10,0**; ADR-0047'nin süre bütçesi rahatladı.
- ✅ ADR-0046 m.1 (kabul ölçütü hakeme) **verdict ekseninde 0,857 uyumla** doğrulandı.
- ⚠️ **21 çekinme koşusu yeniden puanlanacak** — iş yükü, ama para yükü değil (girdi diskte).
- ⚠️ Çapalanma büyüklüğü **hakem gücüne bağlı** (mini 22,3p ↔ `gpt-4o` 8,4p): ucuz hakemle ölçülen
  her çekinme sayısı bu belirsizliği taşır → **Limitations**.
- ⚠️ M3 için `τ_g` 0,923 → **0,800**: `τ_g`'nin çekinme profili raporlanandan **kötü**.
- ⏳ Kabul hakeminin seçimi (hibrit) **açık**, insan onayı bekliyor.
- ⏳ M2b'nin metrik olarak sağlamlığı (ADR-0046 kapsam sınırı) **hâlâ açık** ve bu bulgu onu
  daha da acil kılıyor: M2b'nin paydası da özneye bağlıydı.
