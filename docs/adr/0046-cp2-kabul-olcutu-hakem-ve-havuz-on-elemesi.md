# ADR-0046 — CP2 hasadının kabul ölçütü **regex'ten hakeme** taşındı · havuz **üretimden önce** eleniyor

**Statü:** Yürürlükte · **Tarih:** 2026-07-30
**Otorite belge:** `sprint2.md` CP2 · `TASARIM.md` §4.1.1 (`τ_a` rejimi)
**Değiştirir:** [ADR-0042](0042-rejected-havuzu-tek-kaynak-ve-on-policy-kontrol.md) — *kabul ölçütü* maddesi
**İlgili:** ADR-0043 (bütçeli düşünce — hasadın kipi) · ADR-0044 (mod-duyarlı red kuralı) ·
ADR-0045 m.4 (iki tipli hasat) · ADR-0011 (A1 = cevaplanan-only)
**Kanıt:** `research_log` [#44](../record/research_log/2026-07-30-cp05-cp1-cp2-zemin.md) ·
`outputs/eval/cp2-rejected-hasat/KUNYE.json`
**Tuzak kaydı:** `yurutme-tuzaklari.md` **4.7** (kabul ölçütü ≠ raporlanan metrik) · **4.8** (tuzak havuzunun kendisi geçersiz)

> ## ⚠️ ÖN-KAYIT ŞERHİ
> Karar **hiçbir üretim hasadı başlamadan**, `τ_a` **eğitilmemişken** ve ARA KAPI'nın hiçbir
> sayısı okunmamışken verildi. **ARA KAPI'nın eşiklerine dokunulmadı** (M2 ≥ 0.934 · M1 A1 ≥
> 0.888 · merge M2b ≥ 0.887 — ADR-0045). Değişen yalnız *eğitim verisinin nasıl toplandığı*.

---

## Bağlam — pilot, ölçütün ölçtüğünü sandığı şeyi ölçmediğini gösterdi

ADR-0042 kabul ölçütünü **`score_abstention.exact_reject` RED saymıyorsa kabul** diye yazmıştı —
yani **regex**. Oysa `τ_a`'nın raporlanacağı ve ARA KAPI'nın okuyacağı sayı **LLM hakemi**
(`rejection_rate`). CP0.9'da ikisinin farkı base M2'de **0.61 → 0.814 = 20 puan**.

120 üretimlik pilot, kabul edilen 36 adayı LLM red hakemine verdi (`abst_kontrol_m2`, n=36,
gpt-4o-mini, $0.0042):

```
regex ölçütü kabul etti     : 36/120  (%30)
  bunlardan geçersiz tuzak  : 15      (%42 — kaynak soruyu gerçekten cevaplıyor)
  geçerli tuzakta ABSTAIN   : 15/21   (0.714)  ← havuza YANLIŞ tarafla giriyor
  gerçek fabrikasyon        :  6/21   (0.286)
gerçek verim                :  6/120  = %5,0   (ölçütün bildirdiğinin altıda biri)
```

### İki bağımsız kusur, iki farklı yön

| # | kusur | ORPO'da ne öğretirdi | tespit edilebilir miydi |
| :-- | :--- | :--- | :--- |
| **1** | kabul edilenlerin %71'i gerçekte ABSTAIN | `rejected` = çekinme → **çekinmeyi cezalandır** | hayır — hiçbir yerde hata vermez |
| **2** | havuzun %42'si geçersiz tuzak | `chosen` = "çekiniyorum" ama kaynak cevaplıyor → **cevaplanabilir soruda sus** | hayır |

Kusur 1 `τ_a`'nın M2'sini düşürür; kusur 2 M1 A1 muhafızını (≥ 0.888) tehdit eder. **Aynı
dilimden üretildikleri için kusur 2 `chosen` tarafını da vurur** — yani mevcut
`data/train/orpo_abstain/train.jsonl` (1.741 çift) de bu kusuru taşıyor.

### Kaçışın anatomisi — *"regex'i genişletelim"* neden yetmiyor

15 kaçak elle sınıflandı:

| mekanizma | n | örnek | regex'le kapanır mı |
| :--- | --: | :--- | :--- |
| morfolojik boşluk | **10** | `belirtilmemekle`, `içermediği`, `tanımlamamaktadır`, `yer verilmemiştir` | ✅ |
| leksik işaretsiz | **5** | model kaynağı doğru aktarıyor, soruyu hiç cevaplamıyor | ❌ **asla** |

Türkçe eklemeli; `REJECT_RE` yüzey biçimlerini tek tek sayıyor ve her genişletmede bir sonraki
eki kaçırıyor. Üçte biriyse desenle kapanmıyor: **çekinme sözcükte değil, anlamda.**

### Elenen alternatif — çevrimdışı örtüşme filtresi (ölçüldü)

`orpo_packed`'in sakladığı `ov_gold` / `ov_q` / `judge_flag` alanları 36 etiketli örnekte sınandı:

| `ov_gold` eşiği | kalan geçerli | kalan geçersiz | geçersiz oranı | kaybedilen geçerli |
| --: | --: | --: | --: | --: |
| — (filtresiz) | 21 | 15 | **%42** | 0 |
| ≤ 0.20 | 16 | 7 | **%30** | **5 (%24)** |

Verime net etkisi **%5,0 → ~%6,0**; `judge_flag` bu ayrımda tamamen bilgisiz. **Elendi.**

---

## Karar

### 1. Kabul ölçütü **LLM hakemidir**; regex ucuz ön-filtre olarak kalır

```
üretim → regex ön-filtre (RED ise ele, bedava)
       → LLM red hakemi   (ABSTAIN ise ele) → kabul = FABRICATE
```

Gerekçe **anatomiden** gelir, tercihten değil: kaçışın 5/15'i hiçbir desenle kapanmaz, ve kabul
ölçütü raporlanan metrikle aynı olmadıkça `yurutme-tuzaklari` **4.7** her turda yeniden kurulur.
Regex'in ayakta kalma sebebi ölçüt değil **maliyet**: reddedilenlerin çoğunu bedavaya eler.

**Maliyet:** yalnız regex'i geçen adaylar hakeme gider (~%30) → hedef 500 negatif için ≈ **$0.4**.

### 2. Havuz **üretimden önce** hakemle elenir

Geçerlilik, cevaba bakmadan `(soru, tuzak madde[:900])` çiftinden sorulur — GPU'ya girmeden.
Ölçülen birim maliyet **$0.000117/kalem** → 8.000 kalemlik eleme ≈ **$0.94**.

| | verim | dk/negatif |
| :--- | --: | --: |
| ön-elemesiz (ölçülen) | %5,0 | 3,71 |
| ön-elemeli (tahmin: %42 geçersiz kalkar) | %8,6 | 2,16 |

**Bu, ADR-0042'nin *"tek havuz, tüm kollar"* kuralını bozmaz** — havuz süzülür, bölünmez;
`τ_a`, Taban A ve Taban B'nin iki aşaması aynı süzülmüş havuzu görür.

### 3. Ön-eleme koşulmadan önce **uyumu ölçülür** — yoksa hiç koşulmaz

Ön-eleme hakemi cevabı **görmez**; `score_abstention`'ın hakemi görür. İkisi ayrışırsa havuzu bir
ölçütle eler, sonucu başkasıyla raporlarız — 4.7'nin bir katman yukarısı. Bu yüzden `--against`
kipi, etiketli 36 pilot örneğinde uyumu ve κ'yı raporlar (**≈$0.004**).

> **Kapı:** uyum yetersizse ön-eleme **koşulmaz**. Yanlış ölçütle elenmiş havuz, elenmemiş
> havuzdan **kötüdür**: hangi örneğin neden düştüğü artık bilinmez.

Betik: `scripts/cp2_prefilter.py` — dilim, seed (3407), karıştırma ve 900-kar klip
`cp2_harvest.py` ile **birebir**; geçerlilik sorusu `score_abstention.JUDGE_SYSTEM`den
**import edilir** (kopyalanmaz — sürüklenmesin).

### 4. `chosen` tarafının denetimi **ayrı iş değil**, m.2'nin çıktısıdır

Ön-eleme dilimin tamamını etiketler; geçersiz çıkan tuzağın **çifti düşer**. `chosen` metni zaten
diskte (`orpo_chosen.jsonl`) — yeniden üretim yok. Havuz **baştan kurulmaz, süzülür.**

### 5. Hedef negatif sayısı **m.2'nin sayısından sonra** karara bağlanır — ⏳ AÇIK

Bugün 1.495 (mevcut rejim: 1.741 çift · 82 adım · 3 epoch · lr 1e-5) ile 500 arasında seçim
yapmak **tahminle** karar vermek olur. Ön-eleme, havuzda kaç **geçerli** tuzak kaldığını sayıyla
verir; hedef ondan çıkar.

⚠️ **Bu kalem `TASARIM.md` §4.1.1'i değiştirebilir**: 500 negatif → ~625 çift → `3 epoch ÷ 64`
ile **29 adım** (82 değil). Ayrı ve açık bir karar olarak yazılacak.

---

## Kapsam sınırı — m2b tipi bu ADR'nin dışında

Ön-eleme **m2 tipine** kurulmuştur: tuzak, havuzda duran tek bir `trap_text`. m2b'nin "tuzağı"
hasat anında tohumlu RNG ile kurulan distractor paketidir — çevrimdışı etiketlenemez.

Ve m2b'de daha derin bir soru var: pilotta 25 adayın **24'ü geçersiz tuzak** çıktı. İki okuma
ayrılamadı — (a) seçim etkisi (denetlenen küme tanım gereği *modelin cevapladığı* örnekler),
(b) `--no-gold` bağlamı **cevaplanamaz olmayabiliyor** (distractor'lar aynı kanundan; komşu madde
soruyu fiilen cevaplıyor olabilir). (b) doğruysa **M2b bir metrik olarak** sorunludur ve
**ADR-0045'in merge onarım eşiği (M2b ≥ 0.887) onun üstünde durur.**

**Bu ADR bunu çözmez, işaretler.** Ucuz kontrol: ~20 DEV m2b örneğinin elle gözden geçirilmesi.

---

## Reddedilen seçenekler

| seçenek | neden reddedildi |
| :--- | :--- |
| **Regex'i genişlet, ölçüt kalsın** | Kaçışın **5/15'i** leksik işaretsiz — hiçbir desenle kapanmaz. Üçte biri havuza yine yanlış tarafla girer, ve hata **sessizdir**. |
| **Çevrimdışı `ov_gold` filtresi** | **Ölçüldü:** geçersiz %42 → %30, ama geçerlilerin **%24'ü** kurban; net verim %5,0 → %6,0. Elendi. |
| **Ölçütü değiştirmeden 92 saat koş** | `1.495 ÷ 0,05 = 29.900 üretim > havuzdaki 19.284 kalem` — hedef **yapısal olarak ulaşılamaz**; üstelik kabul edilenlerin %71'i yanlış etiketli olurdu. |
| **Havuzu tamamen yeniden üret** | `chosen` metni ve tuzak eşlemesi zaten geçerli; kusur **seçimde**, üretimde değil. Süzmek yeter — ve `chosen`'ı yeniden üretmek ADR-0042'nin tek-havuz kuralını riske atardı. |

## Sonuçlar

- ✅ Kabul ölçütü ile raporlanan metrik **aynı** — 4.7 kapanır.
- ✅ `chosen` tarafındaki gizli kusur (4.8) **aynı koşuda** temizlenir.
- ✅ Yerel GPU süresi ~**%42** kısalır; para maliyeti ≈ **$1,35** (eleme $0,94 + kabul $0,4).
- ⚠️ Ön-eleme hakeminin **kendi hata payı** vardır ve bu pay havuza girer. Uyum ölçümü (m.3)
  bunu görünür kılar ama sıfırlamaz — **Limitations'a yazılır.**
- ⏳ Hedef negatif sayısı ve `τ_a`'nın adım rejimi **açık** (m.5).
- ⏳ M2b'nin metrik olarak sağlamlığı **açık** (kapsam sınırı).
