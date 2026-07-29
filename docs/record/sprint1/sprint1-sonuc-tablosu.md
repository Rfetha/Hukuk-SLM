# Sprint 1 sonuç tablosu — base ↔ Gemini 3.1 Flash-Lite ↔ `τ_grounding`

> **Bu belge ne:** Sprint 1'in **kalıcı sonuç kaydı**. Üç öznenin aynı protokoldeki karşılaştırması,
> türetilmiş okumalar ve geçerlilik şerhleri. *(Ham script çıktısı [`cp6-tablo.md`](cp6-tablo.md) —
> `compare_runs.py` yeniden koşunca **üzerine yazılır**; kalıcı olan bu belgedir.)*
>
> **Kaynak kayıtlar:** [`research_log` #39](../research_log/2026-07-24-cp0-base-dogrulama-kapisi.md)
> (base çıpaları) · [#41](../research_log/2026-07-29-cp6-tau-grounding-olcumu.md) (`τ_g` ölçümü) ·
> [`cp7-gemini-onizleme.md`](cp7-gemini-onizleme.md) (rakip)
>
> ⚠️ **Bu bir parite iddiası DEĞİL.** Model-düzeyi kıyas; harness kapalı, maliyet normalize edilmedi.
> Parite `harness × {açık/kapalı}` matrisiyle **Sprint 5**'te kurulur.
>
> ### 🔴 PROTOKOL DEĞİŞTİ (2026-07-29 akşamı) — bu tablo artık **çıpa değil**
> Bu tablonun üç sütunu da **`--thinking off`** ile üretildi. [ADR-0043](../../adr/0043-dusunce-modu-acik-butceli-kapatma.md)
> ile hat **`--thinking on` + bütçeli zorunlu kapatma** (1024+512) koşuyor. Yani buradaki
> sayılar **thinking-off protokolünün kalıcı kaydıdır** — silinmez, ama `τ_a` ve kafes hücreleri
> **bunlara karşı ölçülemez.** Yeni çıpalar `sprint2.md` **CP0.9**'da üretilecek ve iki kip
> yan yana raporlanacak. Sebep: base düşünce açıkken M1/M2/M5'te hiç sonlanmıyor
> (`research_log` [#42](../research_log/2026-07-29-cp0-dusunce-modu-sonlanmama.md)).
>
> ### 🔴 M5 SATIRLARI YANLIŞ SAYILMIŞTI (2026-07-29 gecesi) — [ADR-0044](../../adr/0044-mod-duyarli-feragat-kurali.md)
> Kör modun sistem istemi modele feragat cümlesini (*"…bir avukata danışmanızı öneririm"*)
> **emrediyor**; red-regex onu çekinme sayıyordu. Sonuç: **dolu cevaplar "reddetti" sayıldı**,
> M5 coverage sistematik olarak düşük, **ezber kütlesi ~3.4× küçük** ölçüldü — ve M5 **anti-hedef**
> olduğu için sapma **bizim lehimizeydi**. Etki alanı **yalnız M5**: M1/M4 hücrelerinin hepsi
> yeniden hesapta **birebir aynı** çıktı.
>
> Düzeltilmiş satırlar aşağıda ✅ ile, eskiler ~~üstü çizili~~ olarak duruyor — **hakem yeniden
> çağrılmadı**, `gnd_m5_*.jsonl` zaten 80 satırın hepsini taşıyordu, yalnız cevaplanan/çekinen
> ayrımı yeniden yapıldı (`sprint1-thinking-off/a1_m5_*_adr0044.txt`).
>
> **Sıralama korundu, sonuç değişmedi:** `τ_g` base'in üstünde kalıyor — fark **+3.9 → +7.3 puan**
> büyüdü. Kapı 6'nın çıpası bu sayılarla yeniden yazıldı (ADR-0039'un iki sayısı düştü, kuralı durdu).

---

## Künye — üç sütun da aynı koşulda

| | değer |
| :--- | :--- |
| protokol | 6-mod CANON (ADR-0011) · **harness KAPALI** |
| havuz | **DEV** (`data/eval/dev/`) — TEST (`eval/canon/`) hiç görülmedi |
| n | M1 80 · M4 80 · M2 70 · M2b 80 · M3 80 · M5 80 = **470 cevap/özne** |
| seed | **3407** · `--max-chunk-chars 900` (eval-mirror) · `max_new_tokens 512` |
| hakem | `gpt-4o-mini` · **OpenAI-direct** (`judge_gateway=openai`, tek aile — iç kıyas) |
| aile dışlama | Google özne ↔ OpenAI hakem ✅ · Qwen özne ↔ OpenAI hakem ✅ (ADR-0032) |
| `runs` | **1** — güven aralığı yok |

**Özneler:**

| sütun | ne | künye |
| :--- | :--- | :--- |
| **base** | `Qwen/Qwen3.5-4B` çıplak | Q4_K_M GGUF (2.59 GiB) · llama-server · `--thinking off` |
| **Gemini 3.1 FL** | `google/gemini-3.1-flash-lite` | OpenRouter · tarihli snapshot |
| **`τ_g`** | base + `τ_grounding` **merge** edilmiş | 1.083 adım · `‖τ_g‖_F = 10.4589` · aynı GGUF/runtime |

---

## Ana tablo

| eksen | base | Gemini 3.1 FL | **`τ_g`** |
| :--- | ---: | ---: | ---: |
| **M1** faith_macro (ALL) | 0.8385 | 0.8734 | 0.8371 |
| **M1 A1** (cevaplanan) | **0.9730** | 0.9729 | 0.8472 |
| **M1 coverage** | 35/80 = %43.8 | 61/80 = %76.2 | **68/80 = %85.0** |
| M1 cit_precision | 0.9775 | 0.9900 | 0.9500 |
| **M4** faith_macro (ALL) | **0.9810** | 0.9736 | 0.9771 |
| M4 A1 | 0.9800 | 0.9793 | 0.9794 |
| M4 coverage | 76/80 = %95.0 | 78/80 = %97.5 | 77/80 = %96.2 |
| M4 cit_precision | 1.0000 | 1.0000 | 1.0000 |
| **M2** Rej (LLM) | 0.6330 | **0.8420** | 0.4580 |
| M2 Rej (regex) | 0.5670 | ⚠️ 0.8070 | 0.4240 |
| M2 geçerli tuzak *(payda)* | 60 | 57 | 59 |
| **M2b** Rej (LLM) | 0.9730 | 0.9700 | **1.0000** |
| M2b Rej (regex) | 0.9870 | ⚠️ 0.9700 | **1.0000** |
| M2b geçerli tuzak *(payda)* | 75 | 67 | **80** |
| **M3** Rej | 1.0000 | 1.0000 | 1.0000 |
| M3 geçerli tuzak *(payda)* | 57 | 57 | 50 |
| ~~**M5** faith_macro~~ 🔴 | ~~0.3992~~ | ~~0.5786~~ | ~~0.4421~~ |
| ~~**M5 A1**~~ 🔴 *(ADR-0044 — aşağı bak)* | ~~0.2852~~ | ~~0.6213~~ | ~~0.4018~~ |
| ~~M5 coverage~~ 🔴 *(ADR-0044)* | ~~30/80 = %37.5~~ | ~~19/80 = %23.8~~ | ~~29/80 = %36.2~~ |
| **M5 A1** ✅ *(ADR-0044, aynı hakem)* | **0.3941** | 0.5783 | 0.4480 |
| **M5 coverage** ✅ *(ADR-0044)* | 75/80 = **%93.8** | 79/80 = **%98.8** | 79/80 = **%98.8** |
| **M5 ezber kütlesi** ✅ *(cov × A1, ANTİ-HEDEF ↓)* | **%36.9** | **%57.1** | **%44.2** |
| register proxy M1 | 0.9730 | 0.9830 | **1.0000** |
| register proxy M4 | 0.9610 | 0.9230 | 0.9750 |
| register proxy M2 | 0.9640 | 0.9190 | 0.9450 |
| register proxy M2b | 0.9810 | 0.9880 | **1.0000** |

⚠️ **Gemini'nin regex-red satırları raporlanamaz** — o aile için red-regex kalibrasyonu yapılmadı
(TASARIM §3.4). LLM-red satırı okunur. *(CP7'de spot-check yapıldı ve regex değiştirilmedi, ama
tam kalibrasyon borcu açık.)*
⚠️ **`Rej` paydaları özneye göre değişir** — oran payda ile birlikte okunur.

---

## Türetilmiş okumalar

### 1. Sadık-cevap kütlesi — tek sayıya indirgenmiş hâli

`coverage × A1`, yani 80 soruda teslim edilen *cevaplanmış ve sadık* cevap kütlesi. Coverage ile
sadakati ayrı ayrı okumak yanıltıyor; ikisi bir arada tek eksen veriyor.

| | base | Gemini 3.1 FL | **`τ_g`** |
| :--- | ---: | ---: | ---: |
| M1 sadık-cevap kütlesi | 34.1 → **%42.6** | 59.3 → **%74.2** | 57.6 → **%72.0** |

→ `τ_g` base'i **ikiye katladı**, rakibin **2.2 puan** altında.

### 2. Eşleştirilmiş alt küme — A1 düşüşü seçim yanlılığı mı?

Coverage değişince A1 kıyası elmayla-armut olur (base kendi seçtiği kolay dilimde ölçülür).
Kontrol: **üçünün de cevapladığı 27 ortak soru**.

| ortak 27 soru | A1 |
| :--- | ---: |
| base | **0.9774** |
| Gemini 3.1 FL | **0.9795** |
| **`τ_g`** | **0.8778** |

→ **Kolay sorularda da düşük.** Gerileme gerçek, seçim artefaktı değil.
*(Yalnız `τ_g`'nin cevapladığı 41 soruda A1 = 0.8271 — zor dilim ek olarak biraz daha düşük, ama
farkın kaynağı o değil.)*

### 3. İddia etiketleri — düşüşün ne kadarı ölçüm artefaktı

| M1, cevaplanan iddialar | base | **`τ_g`** |
| :--- | ---: | ---: |
| toplam iddia | 147 | 242 |
| `CONTRADICTED` *(gerçek hata)* | **1** | **11** |
| `NOT_IN_SOURCE` | 3 | **31** — bunun **18'i (%58) meta-iddia** |
| hatalı iddia oranı | %2.7 | **%17.4** |
| meta-iddia düşülürse | %2.7 | **%9.9** |

Meta-iddia = RAFT şablonunun 1. adımı (*"ilgili kaynak KAYNAK 3'tür çünkü diğerleri farklı konuda"*)
— kaynak **hakkında** cümle, kaynaktan değil. 🔴 Açık karar: `open_questions.md` **§13.8**.
**Sayılar düzeltilmedi**; düzeltme yapılırsa ön-kayıtlı olur ve **üç sütuna birden** uygulanır.

---

## Geçerlilik şerhleri

| # | şerh |
| :-- | :--- |
| 1 | **`runs=1`** — güven aralığı yok. Hakem gürültü bandı ölçüldü: `faith_macro` **±0.005**, `cit_precision` **±0.044** (aynı girdi, iki koşu — #41 §6). M1 cit_precision düşüşü (0.9775→0.9500) **bu bandın içinde, sinyal sayılmadı.** |
| 2 | **Tek hakem ailesi** — delta *model-vs-model sıralama* olarak geçerli, mutlak sayı olarak değil. Üç-aileli panel + `κ` Sprint 3'te. |
| 3 | **Rakip tarafında iki borç** — sağlayıcı/sürüm pinlemesi artefaktlarda kayıtlı değil; **üretim maliyeti ölçülmedi**. İkisi de Sprint 5 ön koşulu. |
| 4 | **DEV havuzu** — n=80/70 geçici, hedef n güç analizine bağlı (`open_questions.md` §13.3). |
| 5 | **12B sayıları bu tabloya karışmaz** — farklı base, farklı protokol; kalibrasyon çıpası, hedef değil. |

---

## Bir cümlelik okuma

Çıplak base ile en ucuz rakip arasındaki açık **tam iki eksendeydi**: **coverage** (%43.8 ↔ %76.2) ve
**near-miss abstention** (M2 0.633 ↔ 0.842). `τ_grounding` **birinciyi kapattı ve geçti** (%85.0),
**ikinciyi daha da açtı** (0.458) — ve bu tam olarak tezin iç iddiasının öngördüğü şey:
grounding ile abstention **çatışan beceriler**, ayrı kollarda eğitilip merge edilmeleri gerekiyor.
Sprint 1 o iddiayı sınamak için gereken **ilk hücreyi** üretti.
