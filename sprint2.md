# Sprint 2 — ikinci kol, tabanlar ve zeminin düzeltilmesi

> **Otorite:** [`TASARIM.md`](TASARIM.md) · **bu sprint'in kararları:** ADR-0039 · ADR-0040 ·
> ADR-0041 · ADR-0042 · **ADR-0043** · **ADR-0044** · **ADR-0045** · **tam iş listesi:** [`TODO.md`](TODO.md)
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

> **Durum (2026-07-29 sonu):** CP0 ✅ · CP0.9 ✅ · protokol kilitli (thinking-on, bütçeli) ·
> çıpalar üretildi · ADR-0044 ile ölçüm hatası düzeltildi. **Sıradaki iş CP1.**

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
| **CP1** | Hakem istemi düzeltmesi (ADR-0041) + **üç öznenin bütçeli-kip sayılarının** yeniden puanlanması | — | ~0.12 | `τ_g`'nin A1 açığının ne kadarı meta-iddia artefaktı — negatif #1'in sahibi |
| **CP0.5** | `causal-conv1d` hız ölçümü | yerel | 0 | ≥2× yoksa **eklenmez**, negatif bulgu yazılır |
| **CP2** | `rejected` hasadı — bütçeli kipte, base'den, ⚠️ **süre ~4×** | yerel | 0 | `τ_a` + iki tabanın **tek** veri havuzu |
| **CP3** | `τ_a` eğitimi (82 adım, lr 1e-5, **`--fresh-adapter` ZORUNLU**) + tekil ölçüm | Modal | ~0.7 | 🔴 **ARA KAPI** |
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

### 5. Açık kalemler (bu sprint'i durdurmaz, ama unutulmamalı)

- **İz İngilizce** — ürünün *"okunabilir muhakeme"* vaadi karşılanmıyor; `τ_g` v2'nin gerekçesi
- **Düşünce ↔ zorunlu kapatma ayrılamıyor** (base'in %94.7'si zorla kapatıldı) — Limitations
- **`τ_g` v2 mi `τ_a` mı?** ⏳ Önce `τ_a` denenir (ADR-0045 merge kontrolü tam bunu sınıyor); v2 kararı **Sprint 2 sonu**, kafes kurulmadan önce
- **Kapı 6'yı bugün base geçemiyor** (kendi çıpası olduğu için sorun değil, ama raporlanacak)

---

## Checkpoint akışı

> **Sıra kapılara bağlı.** CP0 ✅ → CP0.9 ✅ → **CP1** → CP2 → CP3 → **ARA KAPI** → CP4 → CP5.
> Ara kapı geçilmeden rakip yöntemlere para harcanmaz (5/6 kararı, 2026-07-29).
>
> ✅ **Çözüldü ([ADR-0045](docs/adr/0045-ara-kapi-merge-onarim-kontrolu.md)):** ön-kayıtlı eşik
> durdu, yanına merge onarım kontrolü eklendi; CP2 hasadı **iki tipi birden** toplayacak.

| CP | ne | GPU | $ | kapı |
| :--- | :--- | :--- | ---: | :--- |
| **CP0** | ✅ Düşünce modu — **koşuldu**: base sonlanmıyor, `τ_g` sonlanıyor → **thinking AÇIK, bütçeli** | yerel | **0** | ADR-0043 |
| **CP0.9** | ✅ **Üç çıpa bütçeli kipte yeniden koşuldu** + ADR-0044 + A/B ablasyonu · **ADR-0040 hükmü 🟡 SARI** | yerel | **0.49** | ✅ geçti |
| **CP0.5** | `causal-conv1d` hız ölçümü | yerel | 0 | 2× yoksa yazılmaz |
| **CP1** | Hakem istemi düzeltmesi + üç öznenin yeniden puanlanması | — | ~0.12 | ADR-0041 |
| **CP2** | `rejected` havuzunun base'den yeniden hasadı | yerel | 0 | ADR-0042 |
| **CP3** | **FT-2 = `τ_a`** eğitimi + tekil ölçüm + **merge onarım kontrolü** | Modal | ~0.85 | 🔴 **ARA KAPI** |
| **CP4** | **FT-4** Taban A (karışık SFT) + ölçüm | Modal | ~5.7 | — |
| **CP5** | **FT-5/FT-6** Taban B (ardışık SFT) + on-policy kontrol + ölçüm | Modal | ~6.5 | — |
| | **toplam** | | **~$13.66** | kalan bütçe ~$23.04 |

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

## CP0.5 — `causal-conv1d` hız kaldıracı

**Karar belgesi:** [ADR-0033](docs/adr/0033-egitim-hizi-fla-core-checkpointing-batch.md) ·
**GPU:** yerel · **Kayıt:** `research_log` #44

CP5'te ölçüldü: **6.8-7.0 s/it · 2.619 token/s · MFU ≈ %15.** Sebep büyük ölçüde `causal-conv1d`
kurulu olmaması — Qwen3.5-4B'nin **32 katmanının 24'ü** linear-attention ve PyTorch referans
yoluna düşüyor (*"The fast path is not available"*). Fallback **matematiksel olarak aynı**:
çıktı geçerli, yalnız yavaş.

**Yapılacak:** image'a eklenir, **bir smoke** ile s/it ölçülür.

> 🚨 **`fla-core` dersi (#40):** kazanç **ölçülmeden yazılmaz.** O turda "kesin hızlandırır"
> denen paket ölçülünce hiçbir şey değiştirmedi. `requirements.lock.txt` **korunur**;
> eklenen paket ve sürümü kayda geçer.

**Kapı:** ≥2× hızlanma yoksa **eklenmez**, ölçüm negatif bulgu olarak yazılır ve CP3-CP5 mevcut
hızla koşar. 2× çıkarsa Sprint 2'nin üç eğitim koşusunda ~5 saat + ~$12 tasarruf.

---

## CP1 — Hakem istemi düzeltmesi ve yeniden puanlama

**Karar belgesi:** [ADR-0041](docs/adr/0041-raft-meta-iddia-hakem-kurali.md) ·
**$:** ~0.12 · **Kayıt:** `research_log` #44

Groundedness hakem istemine kural satırı eklenir: *kaynak seçimi/eleme hakkındaki meta-cümleler
iddia olarak ayrıştırılmaz.* `base` · `Gemini 3.1 FL` · `τ_g` **üçü birden** yeniden puanlanır.

> ### 🚨 Üç uygulama şartı — üçü de zorunlu
> 1. **TÜM kollara aynı anda.** Tek kola uygulamak sayıyı doğrudan bizim lehimize kaydırır
> 2. **Eski skorlar saklanır** — istem değişikliği `cit_precision`/iddia sayısını kaydırıyor mu, ölçülür
> 3. **Ham sayılar da yayımlanır.** `τ_g`'nin kalan açığı (%9.9 vs %2.7, `CONTRADICTED` 1 → 11)
>    artefakt **değildir** ve maskelenmez

**Ek kontrol:** muafiyet sınırının doğru çizildiği **~20 örnek elle spot-check** ile doğrulanır —
kaynağın *içeriği* hakkındaki iddialar puanlanmaya devam etmeli.

**Etkilenmeyen:** abstention regex'i · atıf doğrulayıcı · register hakemi. Yığın pinlemesi
(ADR-0029/0032) **değişmez**.

---

## CP2 — `rejected` havuzunun yeniden hasadı

**Karar belgesi:** [ADR-0042](docs/adr/0042-rejected-havuzu-tek-kaynak-ve-on-policy-kontrol.md) ·
**GPU:** yerel ($0) · **Kayıt:** `research_log` #44

Mevcut havuz emekli **12B** hattının fabrikasyonları — yeni modele **başka bir modelin hatalarını**
öğretir. Yeniden hasat: **çıplak base**'den, seed **3407**, aynı üretim ayarları.

> ⚠️ **`--thinking off` DEĞİL** (ADR-0043, 2026-07-29): hasat, kolların eğitileceği ve
> dağıtılacağı kiple aynı olmalı → **bütçeli düşünce (1024 + 512)**. Aksi hâlde negatif örnekler
> modelin gerçekten ürettiği çıktılar olmaz ve ADR-0042'nin kendi *on-policy* gerekçesi çürür.

**Kabul kriteri:** `score_abstention.py` **RED saymıyor** — yani model tuzağa düşmüş, gerçek bir
negatif örnek.

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

**Rejim** (`TASARIM.md` §4.1.1 ile eşleşmeli): 1.741 çift · **82 adım** (3 epoch) · lr **1e-5** ·
etkin batch **64** · **`--fresh-adapter` ZORUNLU**.

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
| **CP0.5 hız kapısı** | CP0.5 | ≥2× yoksa eklenmez (ADR-0033, `fla-core` dersi) |
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
| **Sprint 2 tahmini** | **−13.66** |
| kalan | **~23.04** |

⚠️ **Açık kalemler bütçeye henüz girmedi:** düşünce modu token maliyetini **4.5×** artırdı
(249 → 1135 tok/cevap, base) — Modal'da koşulan her üretim işi bu oranda uzar. Ve `τ_g` v2 açılırsa
(**5 gerekçe**: [`kollar.md`](docs/record/kollar.md)) eğitim ~$5.5 + yeniden ölçüm ~$0.15 eklenir.
