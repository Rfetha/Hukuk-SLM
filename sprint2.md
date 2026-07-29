# Sprint 2 — ikinci kol, tabanlar ve zeminin düzeltilmesi

> **Otorite:** [`TASARIM.md`](TASARIM.md) · **bu sprint'in kararları:** ADR-0039 · ADR-0040 ·
> ADR-0041 · ADR-0042 · **ADR-0043** · **ADR-0044** · **ADR-0045** · **ADR-0046** · **ADR-0047** ·
> **tam iş listesi:** [`TODO.md`](TODO.md)
> **Önceki sprint:** [`sprint1.md`](sprint1.md) 🔒 kapalı ·
> ⭐ sonuçları [`sprint1-sonuc-tablosu.md`](docs/record/sprint1/sprint1-sonuc-tablosu.md)
>
> ### ⭐ HER KOŞUDAN ÖNCE OKU
> [`docs/record/yurutme-tuzaklari.md`](docs/record/yurutme-tuzaklari.md) — *"hata vermeden yanlış
> sonuç üreten"* kalıpların tek listesi. Bu hattın hata sınıfı **çökme değil, sessiz yanlışlık**.

---

## Sprint 2 tek cümlede

> **Sprint 3'ün birleştirme deneyinin muhtaç olduğu her şeyi üretmek — ve o deneyin adil
> olacağından emin olmak.**

Bitince şu soru cevaplanmış olur: *"İki kolumuz da tek başına ayakta mı, ve rakip yöntemleri
adil koşullarda ölçtük mü?"*

**Kapsam dışı, açıkça:** birleştirme (Sprint 3) · harness (Sprint 4) · parite iddiası (Sprint 5) ·
`τ_g`'ye dokunmak.

⚠️ **Güncelleme (CP0.9):** v2'nin gerekçesi **çıktı** — M2b 0.986 → **0.607**
([`kollar.md`](docs/record/kollar.md) kalem 5). Yine de bu sprint'te açılmıyor: doğal karar anı
**Sprint 2 sonu, Sprint 3'ün kafesi kurulmadan önce** (versiyon karıştırmak merge'i geçersiz kılar).
Önce `τ_a` denenir — M2b ikisinin de hedefi, çakışma orada çözülür.

---

## Sprint 2'ye girerken bilinenler

| | durum |
| :--- | :--- |
| Eğitilmiş kol | **1** — `τ_g` **v1** (FT-1), 1.083 adım, `‖τ_g‖_F = 10.4589` · künye: [`kollar.md`](docs/record/kollar.md) |
| Çalışan hat | veri → eğitim → merge → GGUF → `llama-server` → eval → hakem, uçtan uca ✅ |
| Ölçüm zemini | DEV havuzu (80 core_hard + 70 trap), TEST (`eval/canon/`) **hiç görülmedi** |
| Çıpalar | ✅ **CP0.9'da yeniden üretildi** — base · `τ_g` v1 · Gemini 3.1 FL, bütçeli kipte, `outputs/eval/cp09-butceli-1024-512/` |
| **Protokol** | **thinking AÇIK, bütçeli**: düşünce 1024 + cevap 512, zorunlu kapatma (ADR-0043) — rejim değişmezi. **thinking-off artık canlı rejim DEĞİL** (ADR-0043 m.4 daraltıldı) |
| Bütçe | Modal cap **$42.50** · harcanan **$6.29** · **kalan $36.21** |

### ⭐ Yürürlükteki çıpalar (bütçeli kip, DEV, harness kapalı)

| ölçüt | yön | base | `τ_g` v1 | Gemini 3.1 FL |
| :--- | :-: | --: | --: | --: |
| M1 sadık-cevap kütlesi % | ↑ | 56.7 | **71.4** | 72.9 |
| M1 A1 | ↑ | **0.986** | 0.866 | 0.956 |
| M2 Rej (LLM) | ↑ | 0.814 | 0.873 | **0.930** |
| M2b Rej (LLM) | ↑ | 0.986 | **0.607** 🔴 | 1.000 |
| M3 Rej | ↑ | 1.000 | 0.923 | 1.000 |
| M5 ezber kütlesi % *(ANTİ-HEDEF)* | ↓ | 42.5 | **39.2** | 54.4 |
| ort token/cevap | ↓ | 1135 | 772 | **543** |

Kaynak: `research_log` [#43](docs/record/research_log/2026-07-29-cp09-butceli-dusunce-cipalari.md) ·
tablo `scripts/cp09_tablo.py` ile dosyalardan üretilir.

### `τ_g`'nin negatifleri — **bütçeli kipte tablo değişti**

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
> buna göre karara bağlanmalı — **CP2 hasadına başlamadan önce.**

---

## 🎯 SONRAKİ OTURUM — buradan nereye

> **Durum (2026-07-30):** CP0 ✅ · CP0.9 ✅ · CP1 ✅ · CP0.5 ✅ · CP2 **pilot koştu, kusur
> bulundu, karar verildi ([ADR-0046](docs/adr/0046-cp2-kabul-olcutu-hakem-ve-havuz-on-elemesi.md)),
> uygulama BAŞLAMADI.** Protokol kilitli (thinking-on, bütçeli), çıpalar yerinde.
> **Sıradaki iş: ADR-0046 m.3 — ön-eleme uyum ölçümü (~$0,004).**

### Elde ne var / ne yok — tek bakış

| | durum |
| :--- | :--- |
| **Ölçüm zemini** | ✅ Hakem istemi düzeltildi (CP1) · üç özne bütçeli kipte yeniden puanlandı · `causal-conv1d` kapısı karara bağlandı |
| **`τ_a` eğitim verisi** | ⚠️ **Diskte var ama kusurlu** — `data/train/orpo_abstain/train.jsonl` (1.741 çift): `rejected` emekli 12B hattından (off-policy), `chosen` %42 geçersiz tuzak dilimindan |
| **Yeni havuz** | 🔴 **Toplanmadı** — pilot 120+120 üretim koştu, üretim hasadı bilerek başlatılmadı |
| **Karar** | ✅ Verildi — ADR-0046 (ölçüt hakeme · havuz üretimden önce elenir · `chosen` aynı koşuda süzülür) |
| **Hedef + donanım** | ✅ Karara bağlandı — ADR-0047: **750 negatif · Modal `-np 32` · ~1,4 sa · ~$3** (yerel seri 54 sa'ydı). `τ_a` rejimi **~73 adım / 5 epoch** |
| **Açık kalan** | ⏳ M2b metrik olarak sağlam mı · ⏳ pilot CP3 koşulsun mu · ⏳ `cp2_harvest.py` eş zamanlı üretime alınmalı |

### 0. Oturuma başlarken oku (bu sırayla)

1. [`docs/record/yurutme-tuzaklari.md`](docs/record/yurutme-tuzaklari.md) — **her koşudan önce**
2. Bu belgenin *"Yürürlükteki çıpalar"* + *"`τ_g`'nin negatifleri"* tabloları
3. [`research_log` #43](docs/record/research_log/2026-07-29-cp09-butceli-dusunce-cipalari.md)
4. `outputs/eval/README.md` — koşu klasörü düzeni; **yeni koşu = yeni klasör + `KUNYE.json`**

### 1. ✅ KARAR VERİLDİ — [ADR-0045](docs/adr/0045-ara-kapi-merge-onarim-kontrolu.md)

Base bütün çekinme modlarında tavana yaklaştığı için (M2 0.814 · M2b 0.986 · M3 1.000)
`base + 12 puan` formülü **her modda kırık**. Ayrıca `τ_a` ham base'den eğitildiği için
onaracağı delik **kendi üstünde değil, `τ_g`'de**.

**Karar:** ön-kayıtlı eşiğe **dokunulmadı**; yanına neredeyse bedava ikinci bir gözlem eklendi.

```
1) τ_a TEKİL      → M2 Rej ≥ 0.934 · M1 A1 ≥ 0.888     (ön-kayıtlı, tavan riskli)
2) τ_g+τ_a MERGE  → M2b ≥ 0.887 mi?  (τ_g 0.607'den onarım · 0.90 × base 0.986)
```

| 1 | 2 | karar |
| :-: | :-: | :--- |
| ✅ | ✅ | güçlü yeşil → CP4-CP5 |
| ❌ | ✅ | devam — kapı tavan-sınırlıydı, gerekçe merge kanıtı (**açıkça öyle raporlanır**) |
| ✅ | ❌ | **DUR** — kol tek başına iyi ama birleşince taşımıyor |
| ❌ | ❌ | **DUR** — `τ_a` rejimi düzeltilir, rakiplere para harcanmaz |

**CP2'ye etkisi:** hasat **iki tipi birden** toplar — M2-tipi (tuzak verilmiş) + M2b-tipi
(gold hiç yok). Karışım oranı künyeye yazılır.

### 2. Sonra sırayla

| # | iş | GPU | $ | çıktı |
| :-- | :--- | :--- | ---: | :--- |
| **CP1** ✅ | Hakem istemi düzeltmesi (ADR-0041) + **üç öznenin bütçeli-kip sayılarının** yeniden puanlanması | — | **0.15** | ✅ **koşuldu:** `τ_g`'nin A1 açığının **%59'u** meta-iddia artefaktıymış (0.120 → 0.049). Kalan %41 gerçek, maskelenmiyor |
| **CP0.5** ✅ | `causal-conv1d` hız ölçümü | yerel | **0** | ✅ **koşuldu:** tavan **1.254×** < 2.0× → **eklenmedi**, negatif bulgu #44'te |
| **CP2-a** ⏳ | **Ön-eleme uyum ölçümü** — `cp2_prefilter.py --against`, 36 etiketli örnek | — | **0.004** | ADR-0046 m.3 **kapısı**: uyum yetersizse ön-eleme koşulmaz |
| **CP2-b** ⏳ | Havuz ön-elemesi (`(soru, tuzak madde)` → geçerlilik) + **hedef sayı kararı** | — | **0.94** | ADR-0046 m.2 · m.5 |
| **CP2-c** ⏳ | Üretim hasadı — **hedef 750**, regex ön-filtre → **hakem kabulü** | **Modal** `-np 32` | **~3.4** | ADR-0046 m.1 + [**ADR-0047**](docs/adr/0047-cp2-hedef-750-modal-hasat.md) · ~1.4 sa |
| **CP3** | `τ_a` eğitimi (**~73 adım / 5 epoch**, lr 1e-5, **`--fresh-adapter` ZORUNLU**) + tekil ölçüm | Modal | ~0.7 | 🔴 **ARA KAPI** |
| **CP4** | Taban A — karışık SFT | Modal | ~5.7 | Kapı 5'in (a) referansı |
| **CP5** | Taban B — ardışık SFT + on-policy kontrol | Modal | ~6.5 | Kapı 5'in (a) referansı |

**ARA KAPI geçilmeden CP4-CP5'e para harcanmaz.**

### 3. Her koşuda uyulacak değişmezler

```
thinking ON · düşünce 1024 + cevap 512 · seed 3407 · --max-chunk-chars 900
n = 80/80/70/80/80/80 · DEV havuzu · taşıyıcı: Q4_K_M GGUF + llama-server
çıktı: outputs/eval/<koşu-adı>/ + KUNYE.json
hakem: gpt-4o-mini · LLM_GATEWAY=openai (pinli) · red kuralı mod-duyarlı (ADR-0044)
```

### 4. Sprint 2 bittiğinde elde ne olacak

2 kol (`τ_g` v1 + `τ_a`) · 2 taban (karışık + ardışık, + on-policy kontrol) · hepsi aynı
protokolde, aynı veriyle, tekil ölçülmüş → **Sprint 3'ün kafesi kurulabilir.**

### 5. Açık kalemler

**🔴 Bu sprint'i DURDURANLAR — karar/ölçüm bekliyor**

| # | kalem | kim çözer |
| :-- | :--- | :--- |
| ~~1~~ | ~~**Hedef negatif sayısı**~~ | ✅ **KAPANDI — [ADR-0047](docs/adr/0047-cp2-hedef-750-modal-hasat.md): 750, Modal, ~73 adım / 5 epoch.** ⚠️ Koşullu geri alma: ön-eleme ≥ ~8.700 geçerli tuzak bırakmazsa hedef otomatik iner |
| 2 | **M2b metrik olarak sağlam mı** — `--no-gold` bağlamı gerçekten cevaplanamaz mı? ADR-0045'in merge onarım eşiği (M2b ≥ 0.887) bunun üstünde duruyor | ~20 DEV örneği elle, ücretsiz |
| 3 | **Pilot CP3 koşulsun mu** — eldeki off-policy setle, Modal'da, ~$0.85. *Öneri: EVET* — `τ_a` boru hattı (`--fresh-adapter` → merge → GGUF → eval) ve **`τ_g`+`τ_a` TIES merge hiç koşmadı**; Sprint 3'ün 8 hücresi o merge yolunun üstünde. Şerh: kafes hücresi olarak raporlanmaz, ARA KAPI okuması değildir | insan kararı ⏳ |
| 4 | **`cp2_harvest.py` eş zamanlı üretime alınmalı** — bugün seri; Modal `-np 32`'nin karşılığı `ThreadPoolExecutor` + dosya yazımına kilit. Kabul mantığı kalem-başına bağımsız olduğu için temiz paralelleşiyor | kod, CP2-c öncesi |

**⚪ Durdurmaz, unutulmamalı**

- **İz İngilizce** — ürünün *"okunabilir muhakeme"* vaadi karşılanmıyor; `τ_g` v2'nin gerekçesi
- **Düşünce ↔ zorunlu kapatma ayrılamıyor** (base'in %94.7'si zorla kapatıldı) — Limitations
- **Ön-eleme hakeminin kendi hata payı havuza girer** (ADR-0046 sonuçlar) — Limitations
- **`τ_g` v2 mi `τ_a` mı?** ⏳ Önce `τ_a` denenir (ADR-0045 merge kontrolü tam bunu sınıyor); v2 kararı **Sprint 2 sonu**, kafes kurulmadan önce
- **Kapı 6'yı bugün base geçemiyor** (kendi çıpası olduğu için sorun değil, ama raporlanacak)

---

## Checkpoint akışı

> **Sıra kapılara bağlı.** CP0 ✅ → CP0.9 ✅ → CP1 ✅ → CP0.5 ✅ →
> **CP2** *(pilot ✅ · karar ✅ · uygulama ⏳ **BURADAYIZ**)* → CP3 → **ARA KAPI** → CP4 → CP5.
> Ara kapı geçilmeden rakip yöntemlere para harcanmaz (5/6 kararı, 2026-07-29).
>
> **DURUM (2026-07-30):** CP2 pilotu, hasadın **ön-kayıtlı kabul ölçütünün** ölçtüğünü sandığı
> şeyi ölçmediğini gösterdi (`research_log` [#44](docs/record/research_log/2026-07-30-cp05-cp1-cp2-zemin.md)).
> Üretim hasadı **bilerek başlatılmadı**.
> ✅ **Karara bağlandı — [ADR-0046](docs/adr/0046-cp2-kabul-olcutu-hakem-ve-havuz-on-elemesi.md):**
> kabul ölçütü **LLM hakemi** (regex ucuz ön-filtre kalır) · havuz **üretimden önce** elenir
> (≈$0,94) · `chosen` tarafı **aynı koşuda** süzülür.
> ✅ **Ve [ADR-0047](docs/adr/0047-cp2-hedef-750-modal-hasat.md):** hedef **750**, hasat
> **Modal `-np 32`** (taşıyıcı Q4_K_M GGUF, vLLM **değil**), `τ_a` rejimi **~73 adım / 5 epoch**.
> ❌ Sentetik `rejected` **reddedildi** — üçüncü bir modelin hataları, Kapı 5'i çürütür.
>
> **Sıradaki iş: CP2-a uyum kapısı ($0,004). Hiçbiri koşulmadı; insan onayı bekleniyor.**
>
> ✅ **Ayrıca çözüldü ([ADR-0045](docs/adr/0045-ara-kapi-merge-onarim-kontrolu.md)):** ön-kayıtlı
> eşik durdu, yanına merge onarım kontrolü eklendi; CP2 hasadı **iki tipi birden** toplayacak.

| CP | ne | GPU | $ | kapı |
| :--- | :--- | :--- | ---: | :--- |
| **CP0** | ✅ Düşünce modu — **koşuldu**: base sonlanmıyor, `τ_g` sonlanıyor → **thinking AÇIK, bütçeli** | yerel | **0** | ADR-0043 |
| **CP0.9** | ✅ **Üç çıpa bütçeli kipte yeniden koşuldu** + ADR-0044 + A/B ablasyonu · **ADR-0040 hükmü 🟡 SARI** | yerel | **0.49** | ✅ geçti |
| **CP0.5** | ✅ `causal-conv1d` hız ölçümü — **kapı KALDI** (tavan 1.254× < 2.0×) → **eklenmedi** | yerel | **0** | ✅ karara bağlandı |
| **CP1** | ✅ Hakem istemi düzeltmesi + üç öznenin yeniden puanlanması · `τ_g` A1 açığının **%59'u artefaktmış** | — | **0.15** | ✅ ADR-0041 uygulandı |
| **CP2 pilot** | ✅ **KOŞULDU, KUSUR BULDU** — kabul ölçütü (regex) raporlanan metrikle (LLM hakemi) aynı değil; gerçek verim **%5**, hedef mevcut havuzdan **ulaşılamaz** | yerel | **0.01** | ✅ [ADR-0046](docs/adr/0046-cp2-kabul-olcutu-hakem-ve-havuz-on-elemesi.md) |
| **CP2-a** | ⏳ Ön-eleme **uyum ölçümü** (36 etiketli örnek) — ön-eleme hakemi ile denetim hakemi aynı şeyi mi diyor | — | **0.004** | ⏳ **ADR-0046 m.3 kapısı** |
| **CP2-b** | ⏳ Havuz ön-elemesi (8.000 kalem) + `chosen` süzme + **hedef sayı kararı** | — | **0.94** | ⏳ m.2 · m.5 |
| **CP2-c** | ⏳ Üretim hasadı — **hedef 750**, Modal `-np 32`, taşıyıcı Q4_K_M GGUF (vLLM **değil**) | **Modal** | **~3.4** | ⏳ m.1 + [ADR-0047](docs/adr/0047-cp2-hedef-750-modal-hasat.md) · ilk 10 dk verim kapısı |
| **CP3** | **FT-2 = `τ_a`** eğitimi + tekil ölçüm + **merge onarım kontrolü** | Modal | ~0.85 | 🔴 **ARA KAPI** |
| **CP4** | **FT-4** Taban A (karışık SFT) + ölçüm | Modal | ~5.7 | — |
| **CP5** | **FT-5/FT-6** Taban B (ardışık SFT) + on-policy kontrol + ölçüm | Modal | ~6.5 | — |
| | **toplam** | | **~$14.99** | kalan bütçe ~$22.9 |

---

## CP0 — Düşünce modu ✅ **KOŞULDU** — ölçüm üretilemedi, karar başka yerden geldi

**Karar belgeleri:** [ADR-0040](docs/adr/0040-dusunce-modu-olculecek-on-kayitli-kural.md) (ön-kayıtlı kural)
→ [**ADR-0043**](docs/adr/0043-dusunce-modu-acik-butceli-kapatma.md) (sonuç) ·
**GPU:** yerel ($0) · **Kayıt:** [`research_log` #42](docs/record/research_log/2026-07-29-cp0-dusunce-modu-sonlanmama.md) ·
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
`τ_g` v2 bu gerekçeyle **açılmıyor** (diğer dört gerekçe: [`kollar.md`](docs/record/kollar.md)).

⚠️ Yan bulgu: iz **8/8 İngilizce**, cevap **8/8 Türkçe** → ürün *"okunabilir iz"* hedefi için
eğitim verisine iz gerekir; v2'nin 4. gerekçesi.

### ⚠️ Bunun Sprint 2'ye faturası

| ne | sonuç |
| :--- | :--- |
| **Sprint 1'in üç çıpası** | ✅ **CP0.9'da koşuldu** — 1.410 cevap, GPU $0, hakem **$0.45** |
| **ARA KAPI'nın referansı** | ✅ **0.814** (base, bütçeli) → eşik **0.934** · muhafız **0.888** |
| **`rejected` hasadı (CP2)** | `--thinking off` değil, **bütçeli düşünce** kipinde (ADR-0042 üst notu) |
| **Maliyet ekseni** | ✅ ölçüldü: 249 → **1135 tok/cevap (4.5×)**; `τ_g` **772**, kendi istem ailesinde **476** |
| **Ön-kayıtlı 🟢🟡🔴 kuralı** | ✅ koşuldu → **🟡 SARI**; RS-FT kapsam dışı kalıyor |

> **Kalıcı kural (ADR-0040 m.4):** bundan sonra herhangi bir kol yeniden eğitilirse **düşünme
> yeteneğini koruyacak biçimde** eğitilir. Kapıyı açık tutmanın maliyeti eğitim anında ≈ sıfır,
> sonradan yüksek.

---

## CP0.9 — Üç çıpa bütçeli kipte ✅ **KOŞULDU** (2026-07-29)

**Karar belgeleri:** [ADR-0043](docs/adr/0043-dusunce-modu-acik-butceli-kapatma.md) m.4 ·
🆕 [**ADR-0044**](docs/adr/0044-mod-duyarli-feragat-kurali.md) · **GPU:** yerel ($0) ·
**$:** 0.49 (hakem; 0.45 ana + 0.05 ablasyon) · **Kayıt:** [`research_log` #43](docs/record/research_log/2026-07-29-cp09-butceli-dusunce-cipalari.md) ·
**Çıktı:** `outputs/eval/cp09-butceli-1024-512/` (+ `KUNYE.json`)

1.410 cevap (3 özne × 470), üç geçerlilik kapısı da geçti: kesik **%3.6 · %3.6 · %0.0**,
düşünce kanalı **470/470**. Sayılar yukarıdaki *"Yürürlükteki çıpalar"* tablosunda.

### ⭐ Bu turun dört kalıcı bulgusu

**1. Anti-hedef ekseni 3.4× yanlış ölçülüyormuş → [ADR-0044](docs/adr/0044-mod-duyarli-feragat-kurali.md).**
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

**Karar belgesi:** [ADR-0033](docs/adr/0033-egitim-hizi-fla-core-checkpointing-batch.md) ·
**GPU:** yerel ($0) · **Kayıt:** [`research_log` #44](docs/record/research_log/2026-07-30-cp05-cp1-cp2-zemin.md) ·
**Betik:** `scripts/cp05_conv1d_ceiling.py` · **Çıktı:** `outputs/eval/_artefakt/cp05_conv1d_ceiling*.json`

CP5'te ölçülmüştü: **6.8-7.0 s/it · 2.619 token/s · MFU ≈ %15.** Şüpheli `causal-conv1d`
kurulu olmaması — Qwen3.5-4B'nin **32 katmanının 24'ü** linear-attention ve PyTorch referans
yoluna düşüyor (*"The fast path is not available"*). Fallback **matematiksel olarak aynı**.

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

**Karar belgesi:** [ADR-0041](docs/adr/0041-raft-meta-iddia-hakem-kurali.md) ·
**$:** 0.15 fiili *(planlanan 0.12)* · **Kayıt:** [`research_log` #44](docs/record/research_log/2026-07-30-cp05-cp1-cp2-zemin.md) ·
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

> ⏳ **Açık kalan:** ARA KAPI'nın M1 A1 muhafızı **0.888** sayısı, CP0.9'un **eski hakem**
> çıpasından türedi. Yeni hakemle base 0.986 → farklı bir sayı verirse muhafız 0.888 mi 0.880 mi
> olmalı? `τ_a` bu bantta çıkmadıkça karar **ısırmıyor** — o yüzden iki eşiğe karşı da raporlanır.

---

## CP2 — `rejected` havuzunun yeniden hasadı — 🟡 **PİLOT KOŞTU · KARAR VERİLDİ · HASAT BAŞLAMADI**

> **Nerede durduğumuz, tek satırda:** *ne yapılacağı* belli (ADR-0046), *yapılmadı*. Sıradaki
> tek iş **CP2-a uyum kapısı** (~$0,004) — ve o kapı **kalabilir**, bu durumda ön-eleme koşulmaz
> ve hedef sayı yeniden konuşulur.

**Karar belgeleri:** [ADR-0042](docs/adr/0042-rejected-havuzu-tek-kaynak-ve-on-policy-kontrol.md)
→ **[ADR-0046](docs/adr/0046-cp2-kabul-olcutu-hakem-ve-havuz-on-elemesi.md)** (kabul ölçütünü değiştirir) ·
**GPU:** yerel ($0) · **Kayıt:** [`research_log` #44](docs/record/research_log/2026-07-30-cp05-cp1-cp2-zemin.md) ·
**Betikler:** `scripts/cp2_harvest.py` · `cp2_pilot.sh` · `cp2_audit.py` · `cp2_prefilter.py` *(yazıldı, koşulmadı)* ·
**Çıktı:** `outputs/eval/cp2-rejected-hasat/` (+ `KUNYE.json`, durum 🔴 PİLOT)

Mevcut havuz emekli **12B** hattının fabrikasyonları — yeni modele **başka bir modelin hatalarını**
öğretir. Yeniden hasat: **çıplak base**'den, seed **3407**, aynı üretim ayarları.

> ⚠️ **`--thinking off` DEĞİL** (ADR-0043, 2026-07-29): hasat, kolların eğitileceği ve
> dağıtılacağı kiple aynı olmalı → **bütçeli düşünce (1024 + 512)**. Aksi hâlde negatif örnekler
> modelin gerçekten ürettiği çıktılar olmaz ve ADR-0042'nin kendi *on-policy* gerekçesi çürür.

> ### 🚨 KABUL KRİTERİ DEĞİŞTİ — [ADR-0046](docs/adr/0046-cp2-kabul-olcutu-hakem-ve-havuz-on-elemesi.md) (2026-07-30)
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
> ✅ **Hedef KARARA BAĞLANDI: 750 · Modal** — [ADR-0047](docs/adr/0047-cp2-hedef-750-modal-hasat.md).
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
> ⚠️ **Kapsam:** ön-eleme **m2 tipine** kuruldu. m2b'nin tuzağı hasat anında RNG ile kuruluyor,
> çevrimdışı etiketlenemez — ve pilotta 25 adayın 24'ü geçersiz çıktı. Bu, M2b'nin **metrik
> olarak** sağlamlığını sorgulatıyor; ADR-0045'in merge onarım eşiği (M2b ≥ 0.887) onun üstünde
> duruyor. Ucuz kontrol: ~20 DEV m2b örneğini elle gözden geçir.

> ### 🆕 İKİ TİP birden toplanır ([ADR-0045](docs/adr/0045-ara-kapi-merge-onarim-kontrolu.md) m.4)
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

---

## CP3 — FT-2 `τ_abstention` + 🔴 ARA KAPI

**TODO:** §2 · **GPU:** Modal · **$:** ~0.85 · **Kayıt:** `research_log` #45

**Rejim** — ⚠️ [ADR-0047](docs/adr/0047-cp2-hedef-750-modal-hasat.md) ile **değişti**
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
> ve bunu hiçbir hata mesajı söylemez.

Eğitimden sonra `τ_a` **tekil** olarak 6-mod CANON'da ölçülür (merge → GGUF → aynı runtime).
Bu sayı Kapı 5'in **(b) referans noktasıdır** — onsuz *"abstention korundu mu"* sorulamaz.

### 🔴 ARA KAPI — rakip yöntemlere geçmeden önce

```
τ_a TEKİL olarak base'i ANLAMLI biçimde geçmeli.
Eşik:    M2 Rej  ≥ base + 12 puan  →  ≥ 0.934
Muhafız: M1 A1   ≥ 0.90 × base     →  ≥ 0.888
```

✅ **Sayılar CP0.9'dan geldi** (formül ön-kayıtlıydı, sayı değil). Eski eşikler (0.75 / 0.876)
thinking-off protokolündendi ve **düştü**.

> ### 🚨 Tavan riski — şimdi kayda geçiyor, sonra değil
> Base geçerli 59 tuzağın **48'ini zaten reddediyor**. +12 puan, kalan **11 hatanın 7'sinin**
> düzeltilmesi demek — tavana **6.6 puan** kala. `τ_a` bu kapıda kalırsa sebebi kolun kötülüğü
> değil **base'in tavana yakınlığı** olabilir; kapı, ölçmek için kurulduğu şeyi ölçemez hâle gelir.
> Kapı 5'in ADR-0039'da başına gelen şeyin aynısı. Sayı ön-kayıtlı formülden geldiği için
> **değiştirilmedi** — ama bu şerh sonuçla birlikte raporlanır.
>
> ### ✅ İkinci gözlem: merge onarım kontrolü ([ADR-0045](docs/adr/0045-ara-kapi-merge-onarim-kontrolu.md))
> Tek gözlemli kapı *"kaldı ama neden kaldı"* sorusunu teşhis edemiyordu. `τ_a` eğitildikten
> sonra **`τ_g` + `τ_a` norm-dengeli TIES merge** DEV'de koşulur ve **M2b** okunur:
> **onarım eşiği M2b ≥ 0.887** (0.90 × base 0.986 — muhafız formülüyle aynı çarpan).
> Maliyet: merge eğitim compute'u gerektirmiyor → **GPU $0 + hakem ~$0.15**.
> Bu bir **kafes hücresi değil, kapı ölçümüdür** ve DEV'de yapılır; Sprint 3'ün 8 hücresi ayrıca
> ve aynı rejimle koşulur (ADR-0036).

| tekil M2 ≥ 0.934 | merge M2b ≥ 0.887 | eylem |
| :-: | :-: | :--- |
| ✅ | ✅ | **Güçlü yeşil** — CP4-CP5 koşulur |
| ❌ | ✅ | **Devam** — kapı tavan-sınırlıydı; gerekçe merge kanıtı, raporda açıkça öyle yazılır |
| ✅ | ❌ | **DUR** — kol tek başına iyi ama birleşince taşımıyor; iç iddianın öncülü sorunlu |
| ❌ | ❌ | **DUR** — `τ_a` rejimi düzeltilir (epoch · lr · çift sayısı). Rakiplere ~$12 harcanmaz |

**Gerekçe:** `τ_a` tutmazsa birleştirilecek ikinci kol yok, Kapı 5'in (b) referansı yok, ve iç
iddia ölçülemez. Rakipleri önce eğitmek, sonucu bilinmeyen bir deneye peşin para yatırmaktır.
82 adım — bekleme ucuz.

> ✅ **CP0.9 koşuldu, endişe doğrulandı:** base bütçeli düşünceyle tuzak reddini **kendi başına**
> 0.633 → **0.814**'e taşıdı. `τ_a` eski çıpaya (0.6330) karşı ölçülseydi **haksız kredi** alırdı;
> referans artık 0.814 ve eşik ondan türetildi.

---

## CP4 — FT-4 Taban A: tek-aşamalı **karışık** SFT

**TODO:** §2 · **GPU:** Modal · **$:** ~5.7 · **Kayıt:** `research_log` #46

Grounding + abstention verisi **tek koşuda karıştırılarak** eğitilir. `rejected` havuzu CP2'den
(tek havuz kuralı). Ham base'den.

> ### 🚨 Adil kıyas şartı (ADR-0037)
> **Aynı seçim prosedürü tabanlara da uygulanır** — Taban A için de DEV'de en iyi checkpoint
> seçilir. Yoksa biz taranmış, onlar taranmamış olur ve `D > A` tipi **değersiz** bir iddia çıkar.

6-mod CANON'da ölçülür (harness **kapalı** — iç ablasyon).

---

## CP5 — FT-5/FT-6 Taban B: **ardışık** SFT + on-policy kontrol

**TODO:** §2 · **GPU:** Modal · **$:** ~6.5 · **Kayıt:** `research_log` #46

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

---

## Kapılar özeti — bu sprint'te işleyenler

| kapı | nerede | kuralı |
| :--- | :--- | :--- |
| ~~CP0 düşünce kuralı~~ | CP0 ✅ | **Kapandı** — karar [ADR-0043](docs/adr/0043-dusunce-modu-acik-butceli-kapatma.md) (thinking AÇIK, bütçeli) |
| ~~ADR-0040 🟢🟡🔴~~ | CP0.9 ✅ | **🟡 SARI** — M2 eşiği geçti (0.814≥0.78), M5 muhafızı İHLAL (%36.9→%42.5). **RS-FT kapsam dışı kalıyor**, ADR-0035 açılmıyor |
| ~~CP0.5 hız kapısı~~ | CP0.5 ✅ | **KALDI** — tavan 1.254× < 2.0× → `causal-conv1d` **eklenmedi**, `requirements.lock.txt` korundu |
| **CP2-a uyum kapısı** | CP2-a | Ön-eleme hakemi ≟ denetim hakemi, 36 etiketli örnekte. **Yetersizse ön-eleme koşulmaz** ve ADR-0047'nin süre/maliyet tablosu geçersizdir ([ADR-0046](docs/adr/0046-cp2-kabul-olcutu-hakem-ve-havuz-on-elemesi.md) m.3) |
| **CP2-c verim kapısı** | CP2-c | Modal koşusunun **ilk 10 dakikasında** gerçek `s/üretim` okunur; tahminin **2 katını** aşarsa koşu **DURUR**, sayı negatif bulgu olarak yazılır ([ADR-0047](docs/adr/0047-cp2-hedef-750-modal-hasat.md) m.3) |
| **ARA KAPI** | CP3 | `τ_a` tekil **M2 ≥ 0.934 · M1 A1 ≥ 0.888** ⚠️ tavan riski **+** `τ_g+τ_a` merge **M2b ≥ 0.887** ([ADR-0045](docs/adr/0045-ara-kapi-merge-onarim-kontrolu.md)) |
| **Kapı 5** | Sprint 3 | ADR-0037 (3 madde) — referansları burada üretiliyor |
| **Kapı 6** | Sprint 3 | **ADR-0044 sayıları** — M5 coverage ≤ **%97.5** · ezber kütlesi ≤ **%42.5** (base, bütçeli kip) |

---

## Bütçe

| kalem | $ |
| :--- | ---: |
| Modal cap | 42.50 |
| Sprint 1 fiili | −5.80 |
| CP0 fiili *(planlanan ~0.15)* | **0** — hakem hiç çağrılmadı, cevap üretilemedi |
| **CP0.9** fiili *(planlanan 0.60)* | **−0.49** — GPU yerelde $0; 0.45 hakem + 0.05 A/B ablasyonu |
| **CP1** fiili *(planlanan 0.12)* | **−0.15** — 0.113 yeniden puanlama + 0.037 hakem-gürültüsü kontrol koşusu |
| **CP0.5** fiili *(planlanan 0)* | **0** — ölçüm yerelde, `causal-conv1d` derlenmedi (gerek kalmadı) |
| **CP2 pilot** fiili *(planlanan 0)* | **−0.01** — GPU yerelde $0; kabul edilen adayların LLM hakemiyle denetimi |
| **CP2-a** tahmini *(ADR-0046 m.3)* | **−0.004** — ön-eleme uyum kapısı, 36 örnek |
| **CP2-b** tahmini *(ADR-0046 m.2)* | **−0.94** — havuz ön-elemesi, ~8.000 kalem |
| **CP2-c** tahmini *(ADR-0047)* | **−3.4** — Modal A100 `-np 32` ~1.4 sa ≈ $3.0 + hakem kabulü ~$0.4 |
| **CP3-CP5** tahmini | **−13.05** — 0.85 + 5.7 + 6.5 |
| kalan cap | **~$5.5** (CP2-CP5 tamamı koşarsa) · bugün itibarıyla harcanmamış **~22.9** |

⚠️ **CP2-c ilk kez Modal'da koşan bir HASAT işi** — önceki hasat planı yerel/$0 idi. Süre tahmini
tutmazsa (ilk 10 dk kapısı) koşu durur; harcanan kısım künyeye yazılır.

⚠️ **Açık kalemler bütçeye henüz girmedi:** düşünce modu token maliyetini **4.5×** artırdı
(249 → 1135 tok/cevap, base) — Modal'da koşulan her üretim işi bu oranda uzar. Ve `τ_g` v2 açılırsa
(**5 gerekçe**: [`kollar.md`](docs/record/kollar.md)) eğitim ~$5.5 + yeniden ölçüm ~$0.15 eklenir.
