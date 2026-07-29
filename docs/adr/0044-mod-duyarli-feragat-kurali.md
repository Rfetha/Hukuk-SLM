# ADR-0044 — Feragat cümlesi **kör modda** red sayılmaz · Kapı 6'nın çıpası yeniden yazıldı

**Statü:** Yürürlükte · **Tarih:** 2026-07-29
**Otorite belge:** `TASARIM.md` §3.4 (hakemsiz omurga · kalibrasyon kuralı)
**Süperseder:** **ADR-0039'un iki sayısı** (M5 coverage ≤ %37.5 · ezber kütlesi ≤ %10.7) — kuralı
değil, **sayılarını**; ADR-0039'un gerekçesi ve iki-ölçütlü yapısı aynen yürürlükte
**İlgili:** ADR-0011 (A1 = cevaplanan-only) · ADR-0043 (bütçeli düşünce) · `research_log` #43
**Kanıt:** CP0.9 üretimi, 6 dosya × 80 satır elle + otomatik denetim

---

## Bağlam

CP0.9 öncesi **zorunlu ön adım** rakip ailesi için red-regex kalibrasyonuydu (TASARIM §3.4,
`yurutme-tuzaklari.md` 2.2). Kalibrasyon rakip tarafında **temiz çıktı** — Gemini'nin 190
yakalanmayan cevabının hiçbiri red değildi, m3'te 0/80 kaçak vardı. Ama ileri yön denetimi
başka bir şey buldu.

**Kör mod (M5) tek başına `SYSTEM_PROMPT`u kullanır** ve o istem modele şunu emreder:

> *"Emin olmadığın konularda 'Bu konuda güncel mevzuata veya bir avukata danışmanızı öneririm' dersin."*

`REJECT_RE` içinde `bir avukata danış` bir **red kalıbı** olarak duruyordu. Sonuç: model dolu bir
cevap verip sonuna bu cümleyi eklediğinde **çekinmiş sayılıyordu.**

Ölçüldü — "red" etiketli cevapların yalnız bu cümleye dayananları:

| dosya | RED etiketli | yalnızca feragat | gerçek red |
| :--- | --: | --: | --: |
| `m5_base` (thinking-off) | 50/80 | **45** | 5 |
| `m5_base_th` (bütçeli) | 56/80 | **54** | 2 |
| `m5_tg` (thinking-off) | 51/80 | **50** | 1 |
| `m5_tg_v1_th` (bütçeli) | 54/80 | **51** | 3 |
| `m5_gem` (thinking-off) | 61/80 | **60** | 1 |
| `m5_gem_th` (bütçeli) | 62/80 | **58** | 4 |

Feragat taşıyan cevapların **medyan uzunluğu 1082 karakter** ve içerikleri dolu — üstelik sık sık
uydurma: base bir Türk hukuku sorusuna *"İsviçre Medeni Kanunu 1. madde"* diye cevap verip sonuna
feragati ekliyor, eski kural bunu **red** sayıyordu.

**Sapmanın yönü:** M5 **anti-hedeftir** (ezber yükselmemeli) ve kütle = `coverage × A1`. Coverage
sistematik olarak düşük ölçülünce ezber kütlesi olduğundan **küçük** göründü — yani sapma tam
olarak **bizim lehimize**. Bu, bu hattın hata sınıfının (`sessiz yanlışlık`) ders kitabı örneği:
hiçbir aşamada hata yok, tablo doluyor, sayı yanlış bir şeye ait.

## Karar

### 1. Feragat kalıbı **mod-duyarlı** okunur

`mode == "blind"` (M5) ise `bir avukata danış` / `ilgili maddeye danış` eşleşmeleri **red sinyali
sayılmaz**; cevapta başka bir red kalıbı varsa red yine red kalır. Kaynak verilen modlarda
(M1 · M2 · M2b · M3 · M4) saf feragat **gerçekten reddir** ve sayılmaya devam eder.

Uygulama: `score_abstention.exact_reject(cevap, mode)` — `mode` **zorunlu, varsayılansız**
(ADR-0026 ruhu: sessizce yanlış kip seçmek ölçümü fark edilmeden geçersiz kılar).
`rescore_answered.py` artık ham regex'i değil bu fonksiyonu ithal eder (tuzak 2.9: tek kaynak).

**Etki alanı ölçüldü ve yalnız M5:** diğer beş modda altı dosyanın hiçbirinde tek satır kaymadı.
Yani M2/M2b/M3 abstention sayıları ve **ARA KAPI'nın M2 ekseni etkilenmiyor.**

### 2. Kapı 6'nın çıpası yeniden yazılır — formül aynı, sayı yeni

ADR-0039 Kapı 6'yı **base'e** çıpalıyordu; çıpanın kendisi yanlış sayılmıştı. Düzeltilmiş değerler
(thinking-off verisi, **hakem çağrısı yapılmadan** — `gnd_m5_*.jsonl` zaten 80 satırın hepsini
taşıyordu, `rescore_answered` yalnız bölüyor):

| özne | eski cov | eski A1 | eski kütle | **yeni cov** | **yeni A1** | **yeni kütle** |
| :--- | --: | --: | --: | --: | --: | --: |
| base | 37.5% | 0.285 | **10.7%** | 93.8% | 0.394 | **36.9%** |
| `τ_g` v1 | 36.2% | 0.402 | 14.6% | 98.8% | 0.448 | **44.2%** |
| Gemini 3.1 FL | 23.8% | 0.621 | 14.8% | 98.8% | 0.578 | **57.1%** |

Ezber kütlesi **~3.4× yanlış** ölçülmüş. Kapı 6'nın eski eşikleri (`cov ≤ %37.5` · `kütle ≤ %10.7`)
düzeltilmiş ölçekte **base'in kendisi tarafından bile geçilemiyor** — artefakt oldukları böylece
kanıtlanıyor.

**Yeni çıpa, ADR-0039'un formülüyle** (base'e sabitlenir, iki ölçüt birlikte okunur):

```
Kapı 6 (ADR-0039 formülü · ADR-0044 sayıları · thinking-off verisi)
  M5 coverage       ≤ %93.8   (base)
  M5 ezber kütlesi  ≤ %36.9   (base)
```

✅ **Bütçeli kipteki çıpa CP0.9'da ölçüldü ve ANA ÇIPA odur** (thinking-off artık canlı rejim
değil — ADR-0043 m.4 daraltması):

```
Kapı 6 (yürürlükteki) — base, bütçeli düşünce
  M5 coverage       ≤ %97.5
  M5 ezber kütlesi  ≤ %42.5
```

Bugün `τ_g` v1 bu kapıyı **geçiyor** (coverage %96.2 · kütle **%39.2**), base kendi çıpası olduğu
için tanım gereği sınırda. Yukarıdaki thinking-off sayıları (%93.8 / %36.9) protokol kaydı olarak
durur.

### 3. Sıralama korunuyor — `τ_g`'nin ihlali artefakt DEĞİL

Düzeltme `τ_g`'yi aklamıyor, **suçunu büyütüyor**: base'e karşı fark +3.9 puandan **+7.3 puana**
çıkıyor (36.9 → 44.2). `kollar.md`'deki *"M5 anti-hedef ihlali — en güçlü v2 sebebi"* satırı
yerinde kalır, sayısı güncellenir.

### 4. Yan bulgu: eski kural **rastgele değil, sistematik olarak yanlış dilimi** ayırıyordu

A1 düzeltmeden sonra **yükseldi** (base 0.285 → 0.394 · `τ_g` 0.402 → 0.448). Dışlanan feragatli
cevaplar, sayılanlardan daha sadıkmış. Yani hata yalnız paydayı değil, **payı da** kaydırıyordu.
Gemini'de ters yöne gitti (0.621 → 0.578) — rakibin feragatli cevapları daha zayıfmış.

## Değerlendirilen alternatifler

| eleme | gerekçe |
| :--- | :--- |
| **Feragat tek başına red sayılmaz** (mod-bağımsız) | M3'te (boş bağlam) saf feragat **doğru davranıştır** ve red sayılmalı; mod-bağımsız kural onu kaçırırdı |
| **Kalıbı `REJECT_RE`'den tamamen çıkarmak** | En temiz kod, en yanlış ölçüm: M2/M3'te gerçek redlerin bir kısmı kaybolurdu |
| **Sistem istemini değiştirip feragat cümlesini kaldırmak** | Ölçülen görevi değiştirir; üstelik Sprint 1'in tüm sayılarını karşılaştırılamaz kılar |
| **Eski çıpayı korumak, düzeltmeyi Limitations'a yazmak** | *"Anti-hedef ekseninde sapma bizim lehimizeydi, biliyorduk, düzeltmedik"* — savunulamaz |

## Sonuç — kabul edilen bedeller

- **Sprint 1'in M5 sayıları değişti.** Silinmiyor; `sprint1-sonuc-tablosu.md`'de eski/yeni yan yana
  verilir ve nedeni bu ADR'ye bağlanır.
- **Kapı 6 bugün hiçbir özne tarafından geçilmiyor** — base dahil. Bu, kapının *base'e göre*
  tanımlı olması sayesinde sorun değil: ölçüt görecelidir, mutlak değil.
- **Diğer aileler için kalibrasyon borcu duruyor.** Bu ADR mod boyutunu ekledi; TASARIM §3.4'ün
  aile boyutu her yeni rakip için tekrarlanmaya devam eder.
- `runs=1`, güven aralığı yok — Kapı 5/6 ile aynı sınır.
