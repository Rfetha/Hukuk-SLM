# CP7 — erken rakip önizlemesi: Gemini 3.1 Flash-Lite ↔ Qwen3.5-4B çıplak base

**Tarih:** ölçüm 2026-07-24/25 · belge 2026-07-25 · **Faz:** Sprint 1 / CP7
**Otorite:** [`TASARIM.md`](../../../TASARIM.md) · **yürütme:** [`sprint1.md`](../../../sprint1.md) CP7
**İlgili kararlar:** ADR-0029 (model erişim kapısı) · ADR-0030 (base + düşünce modu) · ADR-0032 (hakem paneli, aile-dışlama)
**Bağlam girdisi:** [`research_log #39`](../research_log/2026-07-24-cp0-base-dogrulama-kapisi.md) (CP2 base çıpaları)

**Paper eşlemesi:** *Results* için **erken sinyal** (Sprint 5 parite matrisinin bir dilimi, iddia değil) ·
*Methodology* (aile-dışlama, red-regex kalibrasyonunun rakip ailesinde tekrarı) ·
**Limitations** (tek hakem varyansı, sağlayıcı pinlemesinin kayda geçmemesi).


> ### 🔴 PROTOKOL DEĞİŞTİ (2026-07-29 akşamı, [ADR-0043](../../adr/0043-dusunce-modu-acik-butceli-kapatma.md))
> Bu önizlemenin iki öznesi de **`--thinking off`** ile ölçüldü. Hat artık **`--thinking on` +
> bütçeli zorunlu kapatma** (1024+512) koşuyor → buradaki sayılar **thinking-off kaydıdır**,
> yeni protokolde çıpa değildir. Gemini de dahil üç özne `sprint2.md` **CP0.9**'da yeniden koşulacak.

---

## Özet

Sprint 5'in dış parite matrisinden **bir dilim** öne çekildi: en ucuz frontier sınıfı model
(`google/gemini-3.1-flash-lite`) ile **çıplak base**imiz (`Qwen/Qwen3.5-4B` Q4_K_M, yerel, $0)
**aynı 6-mod CANON protokolünde**, aynı DEV havuzunda, aynı seed ve aynı hakemle koşuldu.

**Sonuç:** en ucuz frontier model çıplak base'i **ezmiyor.** Doğru kaynak eline verildiğinde (M4)
ve *cevapladığı* örneklerde (A1) iki özne başa baş. Açık **iki eksende** yoğunlaşıyor:
**coverage** (base aşırı temkinli) ve **near-miss abstention kalitesi** (M2). İkisi de tezin
planladığı iki kolun (`τ_grounding`, `τ_abstention`) ve **red-kapısı harness'ının** doğrudan hedefi.

---

## Künye — ölçüm koşulları

| kalem | değer |
| :--- | :--- |
| **veri havuzu** | **DEV** — `data/eval/dev/core_hard.jsonl` (80) · `trap.jsonl` (70). TEST (`data/eval/canon/`) **görülmedi** (TASARIM §3.2) |
| **seed** | **3407** (protokol sabiti) |
| **modlar** | 6-mod CANON (ADR-0011): M1 · M4 · M2 · M2b · M3 · M5 |
| **harness** | **KAPALI** — ikisi de çıplak, retriever/atıf-doğrulayıcı/red-kapısı yok |
| **hakem** | `gpt-4o-mini`, **OpenAI-direct** (`LLM_GATEWAY=openai`, `judge_gateway=openai`, `judge_providers=[]`) — **tek aile**, iç kıyas (sprint1.md CP2 gerekçesi) |
| **Özne 1** | `Qwen/Qwen3.5-4B` → `models/gguf/q35-4b-q4_k_m.gguf` (Q4_K_M, PURE=0), **yerel llama.cpp**, `--thinking off`, `max_new_tokens=512`, **marjinal maliyet $0** |
| **Özne 2** | `google/gemini-3.1-flash-lite` (**OpenRouter**), `--thinking none` (Qwen bayrağı gönderilmez; modelin varsayılan reasoning bandı), `max_new_tokens=512` |
| **üretim** | `scripts/run_gemini_benchmark.sh` · **470 cevap** (80+80+70+80+80+80) |
| **skorlama** | `scripts/{groundedness,score_abstention,score_register,rescore_answered}.py` |
| **tarih** | üretim + ilk skorlama 2026-07-24/25 · A1 yeniden hesabı + `m5_gem` yeniden koşusu 2026-07-25 |

### Aile-dışlama teyidi (ADR-0032) ✅

**Özne Google ailesi, hakem OpenAI ailesi** → *"bir özneyi kendi ailesinin hakemi notlamaz"* kuralı
**sağlanıyor.** Diğer özne (Qwen/Alibaba) de hakemden ayrık. Bu önizlemede **hiçbir özne kendi
ailesinin hakemiyle notlanmadı.**

> ⚠️ Kural sağlanmış olması **panel** ihtiyacını kaldırmaz: burada tek hakem var, self-preference
> ölçülmedi, κ raporlanmadı. Üç aileli panel **Sprint 3** (iç iddia) ve **Sprint 5** (parite) işi.

### Üretim sağlıklı mıydı? (boş/kesik cevap denetimi)

`gen_eval_grounded.py` detay çıktısındaki `finish_reason` + boş-cevap sayacı (ADR-0030 sonrası eklendi):

| mod | Qwen base | Gemini 3.1 FL |
| :--- | :--- | :--- |
| M1 | 77 `stop` · **3 `length`** | 79 `stop` · 1 `length` |
| M4 | 80 `stop` | 80 `stop` |
| M2 | 70 `stop` | 70 `stop` |
| M2b | 76 `stop` · **4 `length`** | 79 `stop` · 1 `length` |
| M3 | 80 `stop` | 80 `stop` |
| M5 | 68 `stop` · **12 `length`** | 80 `stop` |

**Boş cevap: 0/470 her iki öznede.** Kesik cevap (`length`) base'de 19/470, Gemini'de 2/470 —
kesik cevap hakeme yarım gider, yani **base'in aleyhine küçük bir sistematik yanlılık** var
(özellikle M5'te 12/80). Kayda geçirildi; `max_new_tokens` bandı Sprint 5'te tekrar bakılacak.

---

## Tam tablo — 6 mod × iki özne

Her satırın kaynak dosyası belirtildi. Tüm dosyalar `outputs/eval/` altında.
⚠️ **A1 ve coverage sayıları 2026-07-25'te YENİDEN hesaplandı** (aşağıdaki regex-kalibrasyon
düzeltmesi) — daha eski tablolardaki A1/coverage değerleri geçersizdir.

### M1 — distractor sadakati (5 kaynak: 1 gold + 4 hard-negative) · *doğru davranış: cevapla*

| metrik | **Qwen base** | **Gemini 3.1 FL** | kaynak dosya |
| :--- | ---: | ---: | :--- |
| faithfulness_macro (ALL) | 0.8385 | **0.8734** | `gnd_m1_{base,gem}_summary.json` |
| **A1 = faith_macro (cevaplanan-only)** | **0.9730** | 0.9729 | `a1_m1_{base,gem}.txt` |
| **coverage** (cevaplanan / toplam) | **35/80 = %43.75** | **61/80 = %76.25** | `a1_m1_{base,gem}.txt` |
| over_refusal_rate | 0.5625 | 0.2375 | `a1_m1_{base,gem}.txt` |
| cit_precision (ALL / cevaplanan) | 0.9775 / 0.9744 | 0.9900 / **1.0000** | `gnd_*_summary.json` · `a1_*.txt` |
| cit_recall_macro | 0.9750 | 0.9875 | `gnd_m1_*_summary.json` |
| wrong_ref_rate (cevaplanan) | 0.0143 | **0.0** | `a1_m1_*.txt` |
| toplam iddia (claim) | 398 | 309 | `gnd_m1_*_summary.json` |

### M4 — oracle tavanı (yalnız gold kaynak) · *doğru davranış: cevapla*

| metrik | **Qwen base** | **Gemini 3.1 FL** | kaynak dosya |
| :--- | ---: | ---: | :--- |
| faithfulness_macro (ALL) | **0.9810** | 0.9736 | `gnd_m4_{base,gem}_summary.json` |
| **A1 (cevaplanan-only)** | 0.9800 | **0.9793** | `a1_m4_{base,gem}.txt` |
| **coverage** | 76/80 = %95.00 | 78/80 = **%97.50** | `a1_m4_{base,gem}.txt` |
| over_refusal_rate | 0.0500 | 0.0250 | `a1_m4_*.txt` |
| cit_precision (ALL) · cit_recall_macro | 1.0000 · 1.0 | 1.0000 · 1.0 | `gnd_m4_*_summary.json` |
| toplam iddia | 270 | 306 | `gnd_m4_*_summary.json` |

### M2 — near-miss tek kaynak (n=70 tuzak) · *doğru davranış: reddet*

| metrik | **Qwen base** | **Gemini 3.1 FL** | kaynak dosya |
| :--- | ---: | ---: | :--- |
| geçerli tuzak / toplam | 60/70 | 57/70 | `abst_m2_{base,gem}_summary.json` |
| **Rej(regex)** = `rejection_exact` | 0.567 | **0.807** | ↑ |
| **Rej(LLM)** = `rejection_rate` | 0.633 | **0.842** | ↑ |
| fabrication_rate | 0.367 | **0.158** | ↑ |
| parametric_leak | 0.300 | **0.123** | ↑ |

### M2b — çok-kaynak ıska (gold ÇIKARILMIŞ, 4 distractor; n=80) · *doğru davranış: reddet*

| metrik | **Qwen base** | **Gemini 3.1 FL** | kaynak dosya |
| :--- | ---: | ---: | :--- |
| geçerli tuzak / toplam | 75/80 | 67/80 | `abst_m2b_{base,gem}_summary.json` |
| **Rej(regex)** | **0.987** | 0.970 | ↑ |
| **Rej(LLM)** | 0.973 | 0.970 | ↑ |
| fabrication_rate | 0.027 | 0.030 | ↑ |
| parametric_leak | 0.027 | 0.015 | ↑ |

### M3 — boş bağlam (n=80) · *doğru davranış: reddet*

| metrik | **Qwen base** | **Gemini 3.1 FL** | kaynak dosya |
| :--- | ---: | ---: | :--- |
| geçerli tuzak / toplam | 57/80 | 57/80 | `abst_m3_{base,gem}_summary.json` |
| **Rej(regex)** · **Rej(LLM)** | **1.000** · **1.000** | **1.000** · **1.000** | ↑ |
| fabrication_rate · parametric_leak | 0.0 · 0.0 | 0.0 · 0.0 | ↑ |

**İkisi de tavanda.** Boş bağlamda hiçbir özne uydurmadı.

### M5 — kör / parametrik (kaynak YOK) · ⚠️ **ANTİ-HEDEF** · *yükselmesi İSTENMEZ*

| metrik | **Qwen base** | **Gemini 3.1 FL** | kaynak dosya |
| :--- | ---: | ---: | :--- |
| faithfulness_macro (ALL) | **0.3992** | 0.5786 | `gnd_m5_{base,gem}_summary.json` |
| **A1 (cevaplanan-only)** | **0.2852** | 0.6213 | `a1_m5_{base,gem}.txt` |
| **coverage** | 30/80 = %37.50 | **19/80 = %23.75** | `a1_m5_*.txt` |
| over_refusal_rate | 0.6250 | 0.7625 | `a1_m5_*.txt` |
| cit_precision (ALL / cevaplanan) | 0.5698 / 0.5588 | 0.7917 / 0.8261 | `gnd_*` · `a1_*` |
| wrong_ref_rate (ALL / cevaplanan) | 0.3721 / 0.3722 | 0.1562 / 0.2105 | ↑ |
| cit_recall_macro | 0.7000 | 0.8625 | `gnd_m5_*_summary.json` |
| toplam iddia | 506 | 451 | ↑ |

> **Okuma kuralı (ADR-0011):** M5'te **yüksek faith = kötü**, çünkü kaynağı olmayan bir cevabı
> ikna edici biçimde üretmek demek. *"Güncellik kütüphanede, ağırlıkta değil."* Gemini'nin 0.5786'sı
> **onun için avantaj değil**, bizim protokolümüzde **anti-hedefte daha kötü** konumdur.
> ⚠️ Buna karşılık Gemini **daha az cevaplıyor** (coverage %23.75 vs %37.50) — yani "az konuşuyor
> ama konuştuğunda parametrik bilgisi daha sağlam". İki sayı **birlikte** okunur.

### Register (deterministik leksik proxy, hakemsiz — `reg_*_summary.json` `register_mean`)

| mod | **Qwen base** | **Gemini 3.1 FL** |
| :--- | ---: | ---: |
| M1 | 0.973 | 0.983 |
| M4 | 0.961 | 0.923 |
| M2 | 0.964 | 0.919 |
| M2b | 0.981 | 0.988 |
| M5 *(kör; düşük beklenir — atıf işareti yok)* | 0.566 | 0.523 |

**Uzman register'ında iki özne ayrışmıyor** (RAG modlarında 0.92-0.99 bandı). Bu, Kapı 0'ın
`τ_register`'ı düşürme kararını (#39) **dışarıdan da destekliyor**: en ucuz frontier model bile
bu eksende bizden ayrışmıyor, yani eksen ayırt edici değil.

---

## ⚠️ Bulgu 1 — hakem varyansı: aynı çıktı, üç farklı sayı

`m4_gem` groundedness'ı **üç kez** koşuldu (aynı 80 cevap, aynı hakem `gpt-4o-mini`, aynı prompt,
aynı `--mode data`). Üç `faithfulness_macro` okuması:

| koşu | faith_macro | cit_precision | total_claims | kaynak |
| :--- | ---: | ---: | ---: | :--- |
| 1 (ilk tam koşu) | **0.9870** | — | — | NEXT-SESSION.md §4 kaydı (özet dosyası üzerine yazıldı) |
| 2 | **0.9738** | 1.0 | 310 | `gnd_m4_gem_summary.run2-BOZUK-DETAY.json` |
| 3 (güncel) | **0.9736** | 1.0 | 306 | `gnd_m4_gem_summary.json` |

`m5_gem` da iki kez koşuldu:

| koşu | faith_macro | cit_precision | wrong_ref | total_claims | kaynak |
| :--- | ---: | ---: | ---: | ---: | :--- |
| 1 | 0.5832 | 0.7475 | 0.2121 | 451 | `gnd_m5_gem_summary.run1-BOZUK-DETAY.json` |
| 2 (güncel) | 0.5786 | **0.7917** | **0.1562** | 451 | `gnd_m5_gem_summary.json` |

**Okuma:**

- `m4_gem` faith'inin iki okuması **0.974'te kümeleniyor**, biri (0.987) uzakta → tek okuma
  **±0.013 bandında** oynayabiliyor.
- Varyans yalnız yargı katmanında değil: **iddia çıkarımı da kayıyor** (m4: 310 → 306 claim).
  Yani hem payda hem pay değişiyor.
- `m5_gem`'de faith neredeyse sabit (0.5832 → 0.5786, Δ0.005) ama **`cit_precision` 0.7475 → 0.7917
  (Δ0.044)** ve `wrong_ref_rate` 0.2121 → 0.1562 (Δ0.056) — **atıf doğrulama ekseni faith'ten daha
  oynak.** Bu beklenmedik ve kayda değer.

> ### 📌 Sonuç — Sprint 3'ün üç-aileli paneli tam bu yüzden var
>
> Tek hakemle alınan bir sayı **±0.01-0.05 bandında** anlamsızdır. Bu önizlemedeki
> *"M4'te fark yok" (0.981 vs 0.9736, Δ0.007)* ve *"A1'de fark yok" (0.9730 vs 0.9729, Δ0.0001)*
> okumaları **varyans bandının içinde** — yani "fark yok" ifadesi burada **doğru ve tek yönlü
> okunabilir olan tek ifade**: fark **ölçülemiyor**, "eşit" değil.
> Buna karşılık **coverage farkı (%43.75 vs %76.25 = 32.5 puan)** ve **M2 farkı (0.567 vs 0.807)**
> bandın **çok üstünde** — bunlar gerçek sinyal.
>
> **Kural (Sprint 3+ için bağlayıcı):** hakem-tabanlı bir eksende fark iddiası, **üç-aileli panel +
> κ + self-preference** ölçümü olmadan raporlanmaz (ADR-0032). Deterministik omurga (regex red +
> atıf doğrulama) bu kısıttan muaftır — iddia yüzeyinin çoğu zaten oradadır (TASARIM §3.4).

---

## ⚠️ Bulgu 2 — `rescore_answered.py` kalibre edilmemiş bir red-regex KOPYASI taşıyordu

**Ne oldu:** `scripts/rescore_answered.py` kendi içinde **ayrı bir** red-tespit regex'i tutuyordu.
#39'da (2026-07-24) `score_abstention.py`'nin regex'i kalibre edilmişti (`bulunmuyor` ailesi
eklendi, `bulunmazsa` gibi kanunun koşul dili `(?!sa)` bakışıyla elendi) — **ama kopya bu
kalibrasyonu almadı.** İki kaynak sessizce ayrıştı.

**Düzeltme:** kopya silindi, tek kaynaktan ithal ediliyor:

```python
from score_abstention import REJECT_RE as ABSTAIN_RE
```

**Ölçülen etki (480 cevap üzerinde eski kopya ↔ kalibre regex):** **3 ayrışma**, üçü de eski
kopyanın **yanlış-pozitifi** (cevabı yanlışlıkla "çekinme" sayması):

| tip | örnek | eski kopya | kalibre |
| :--- | :--- | :--- | :--- |
| gerçek cevabın red sanılması | `"kaynaklarda bu ..."` kalıbı | RED | cevap |
| kanunun koşul dili | `bulunmazsa` / `bulunmazsanız` | RED | cevap |

**Yön:** eski kopya cevapları çekinme sayıyordu → **coverage olduğundan DÜŞÜK, A1 paydası
olduğundan KÜÇÜK görünüyordu.** Etki küçük (3/480) ama **yönü sistematik** ve tam olarak
kalibrasyonsuz-regex hata sınıfının bir üyesi (#39 Bulgu 3 ile aynı sınıf, farklı yer).

**Somut sayı değişimi** (bu düzeltme + `m5_gem` yeniden koşusu sonrası):

| sayı | eski | **yeni** |
| :--- | ---: | ---: |
| M1 base coverage | 34/80 (%42.5) | **35/80 (%43.75)** |
| M1 base A1 | 0.972 | **0.9730** |
| M4 base coverage | 75/80 (%93.8) | **76/80 (%95.00)** |
| M4 gem coverage / A1 | *(ölçülmemişti)* | **78/80 (%97.50) / 0.9793** |
| M5 gem faith_macro (ALL) | 0.5832 | **0.5786** |
| M5 gem cit_precision | 0.7475 | **0.7917** |

> **Ders (kayda geçti):** *kalibre edilen her deterministik bileşenin **tek kaynağı** olmalı.*
> Bir regex'i iki dosyada tutmak, kalibrasyonu yarısına uygulamak demektir — ve **hata vermez**.
> Bu, #39'un dört sessiz-bozulma vakasının aynı ailesinden bir beşinci/altıncıdır.

---

## ⚠️ Bulgu 3 — Gemini için red-regex kalibrasyonu (TASARIM §3.4 zorunlu ön-adımı)

**Kural:** *"hiçbir abstention sayısı, red-tespit regex'i o özne ailesinde kalibre edilmeden
raporlanmaz."* Regex bizim base'imizde kalibre edilmişti (#39); Gemini'nin red dağarcığı farklı
olabilirdi. **Ölçüldü. Regex DEĞİŞTİRİLMEDİ** — değişiklik base çıpalarını da kaydırır, ayrı karar.

### 3a. İleri yön — regex Gemini'nin reddini kaçırıyor mu? **HAYIR**

`verdict` (LLM hakem) ile `reject_exact` (regex) **geçerli tuzaklarda** karşılaştırıldı:

| dosya | geçerli tuzak | **ayrışma** | LLM=ABSTAIN & regex=hayır | regex=RED & LLM≠ABSTAIN |
| :--- | ---: | ---: | ---: | ---: |
| `abst_m2_gem.jsonl` | 57 | **2** | 2 | 0 |
| `abst_m2b_gem.jsonl` | 67 | **0** | 0 | 0 |
| `abst_m3_gem.jsonl` | 57 | **0** | 0 | 0 |
| *(karşılaştırma)* `abst_m2_base.jsonl` | 60 | 6 | 5 | 1 |
| *(karşılaştırma)* `abst_m2b_base.jsonl` | 75 | 1 | 0 | 1 |
| *(karşılaştırma)* `abst_m3_base.jsonl` | 57 | 0 | 0 | 0 |

**Gemini'de toplam 2 ayrışma / 181 geçerli tuzak (%1.1).** İkisi de elle okundu
(`m2_gem` id=21, id=36) ve **ikisi de regex'in hatası DEĞİL:** model her ikisinde de near-miss
kaynaktan **cevap üretmiş** (TMK m.229 ve m.376 alıntılayarak), red cümlesi yok. Yani burada
**LLM hakem** "soruyu cevaplamadı" diye ABSTAIN etiketlemiş; regex doğru davranmış.

**Ayrıca tam sayım yapıldı:** geçerli tuzaklarda regex'in RED demediği **13 Gemini cevabının
tamamı** (M2: 11 · M2b: 2 · M3: 0) elle okundu. **Hiçbiri tanınmayan bir red değil** — hepsi
gerçek cevap (çoğu fabrication / off-source). → **Regex Gemini'nin reddini kaçırmıyor.**

`score_gemini_benchmark.sh`'in yerleşik recall kontrolü aynı sonucu veriyor:

```
gem : toplam(m2+m2b+m3)=230 · regex-RED=193 · red-gibi(ilk120)=184 · YAKALANMAYAN=4
base: toplam(m2+m2b+m3)=230 · regex-RED=190 · red-gibi(ilk120)=168 · YAKALANMAYAN=9
```

Gemini'nin 4 "yakalanmayanı" elle okundu: dördü de **gerçek cevap** (tarama regex'i `düzenle` /
`belirtil` kelimelerine cevap metninin içinde takılmış). **Yanlış negatif yok.**

### 3b. Geri yön — regex yanlışlıkla RED mi sayıyor? **HAYIR (18/18)**

`seed=3407` ile 168 regex-RED satırından **18** örneklendi ve tam metin okundu.
**18/18 gerçek red.** Örnekler:

- *"Verilen kaynaklarda bu konuyu düzenleyen madde bulunmuyor."* (kalıbın birebir kendisi)
- *"Paylaştığınız kaynak metinde, hükmün hangi durumlarda kesin hüküm sayılacağına dair bir bilgi
  bulunmamaktadır. Bu metin yalnızca karşı dava açılmasının şartlarını … düzenlemektedir."*
- *"Verilen kaynaklarda, satılanın elinden alınması (zapt) durumunda ürünün geri alınabileceğine
  dair bir düzenleme bulunmamaktadır."*

### 3c. Red dağarcığı dağılımı — Gemini'ninki base'in **alt kümesi**

Geçerli tuzaklarda regex'in eşleştirdiği kalıpların frekansı:

| kalıp | **Gemini 3.1 FL** | **Qwen base** |
| :--- | ---: | ---: |
| `bulunmuyor` | **110** | **138** |
| `bulunmamaktadır` | 27 | 59 |
| `bilgi bulunmamakta` | 25 | 11 |
| `yer almamakta` | 4 | 17 |
| `belirtilmemiş` | 0 | 16 |
| `içermez` | 0 | 5 |
| `içermemektedir` | 3 | 2 |
| `geçmemektedir` | 1 | 2 |
| `bilgi yok` | 0 | 2 |
| `düzenlenmemiş` | 1 | 1 |
| `belirtilmemekte` | 0 | 1 |

> ### 📌 Kalibrasyon sonucu — **Gemini için ek kalibrasyon GEREKMİYOR**
>
> Gemini'nin red dağarcığı bizim base'imizinkinin **dar bir alt kümesi** ve **aynı çekirdek fiil
> etrafında** yoğunlaşıyor (`bulunmuyor`/`bulunmamaktadır` = 137/171 = **%80**). #39'da bizim
> base'imiz için yapılan kalibrasyon **olduğu gibi transfer oluyor.**
>
> **Neden böyle:** Gemini sistem isteminin verdiği kanonik red cümlesini (*"Verilen kaynaklarda bu
> konuyu düzenleyen madde bulunmuyor."*) çoğu zaman **birebir** kullanıyor — talimat takibi güçlü.
> ⚠️ Bu **şansa dayalı bir sonuç değil ama garantisi de yok**: talimat takibi zayıf ya da farklı
> üslupta bir rakip ailede (ör. Anthropic/Meta) aynı transfer **beklenmemeli**. Kural her yeni
> özne ailesinde tekrar koşulur.
>
> ⚠️ **Yan gözlem (base tarafı, bu belgenin kapsamı dışı, kayıt için):** aynı taramada base'in 9
> "yakalanmayanından" **en az biri** gerçek bir red gibi duruyor — *"Verilen kaynak metni (TMK
> m.608) sadece miras reddinin geçişini ve ret süresini düzenler; …"* (kaynağı sınırlayan, örtük
> red). Regex bunu görmüyor. **Değiştirilmedi** — regex değişikliği tüm base çıpalarını kaydırır,
> ayrı bir karar ve ayrı bir yeniden-skorlama gerektirir. **Açık kalem olarak kayda geçti.**

---

## ⚠️ Bulgu 4 — sağlayıcı pinlemesi artefaktlarda kayıtlı DEĞİL

ADR-0029 *"`gen_providers` / `judge_providers` tek eleman olmalı"* diyor.

- **Hakem tarafı ✅:** tüm `*_summary.json` dosyalarında `judge_gateway: "openai"`,
  `judge_providers: []` → OpenAI-direct, **OpenRouter yok**, çok-eleman yok. Doğrulanabilir.
- **Üretim tarafı ⚠️:** `gen_eval_grounded.py` OpenRouter'a **ham HTTP** yolundan gidiyor
  (`--server-url`), `llm_client.py`'nin `LLM_PROVIDER_ORDER` pinlemesini ve `note_provider()`
  kaydını **kullanmıyor**. `.env`'de `LLM_PROVIDER_ORDER` **tanımlı değil.**
  → **Gemini üretiminin hangi upstream sağlayıcıda koştuğu artefaktlarda YOK.**
  "Google AI Studio" bilgisi yalnız `scripts/run_gemini_benchmark.sh`'in yorum satırında ve
  `NEXT-SESSION.md`'de duruyor — **koşu anında gözlenmiş ama kayda geçmemiş.**

> **Sonuç:** bu önizlemede **sağlayıcı pinlemesi doğrulanamıyor.** Önizleme için kabul edilebilir
> (fark coverage/M2'de ve 30 puan bandında; sağlayıcı kuantizasyonu bunu açıklamaz), **Sprint 5
> parite matrisi için kabul edilemez.**
> **Açık iş:** `gen_eval_grounded.py`'nin OpenRouter yolu `llm_client`'a bağlanmalı ya da
> `provider.order` + `allow_fallbacks=false` ham HTTP gövdesine eklenip **gerçekleşen sağlayıcı
> detay çıktısına yazılmalı.**

---

## Maliyet

**Hakem (gpt-4o-mini, OpenAI-direct, `judge_cost_usd` alanlarından toplandı):**

| taraf | gnd (m1+m4+m5) | abst (m2+m2b+m3) | toplam |
| :--- | ---: | ---: | ---: |
| Qwen base | 0.0419 + 0.0350 + 0.0493 = **$0.1262** | 0.0095 + 0.0175 + 0.0113 = **$0.0383** | **$0.1645** |
| Gemini 3.1 FL | 0.0376 + 0.0362 + 0.0457 = **$0.1195** | 0.0089 + 0.0166 + 0.0113 = **$0.0368** | **$0.1563** |

(+ atılan/yeniden koşulan `m4_gem` ve `m5_gem` koşuları: $0.0366 + $0.0458 ≈ **$0.082** ek.)

**Üretim:**
- **Qwen base: $0** (yerel llama.cpp, RTX 5070 Laptop — marjinal maliyet sıfır; donanım
  amortismanı ve elektrik parite muhasebesinde ayrıca ele alınacak, TASARIM §9).
- **Gemini 3.1 Flash-Lite: ölçülmedi.** `gen_eval_grounded.py` token/maliyet kaydı tutmuyor ve
  `llm_client.PRICE`'ta bu model **yok** → **birincil-kaynak liste fiyatı girilmeden maliyet
  raporlanmaz** (ADR-0029: ödenen tutar ≠ parite fiyatı). **Açık iş, Sprint 5'in ön koşulu.**

---

## İlk okuma — 5 madde (yeni coverage sayılarıyla doğrulandı)

1. **M4 oracle'da fark ÖLÇÜLEMİYOR.** 0.9810 (base) vs 0.9736 (Gemini), atıf **1.0 vs 1.0**,
   coverage %95.0 vs %97.5. Δ = 0.007 — **hakem varyans bandının (±0.013) içinde** (Bulgu 1).
   → *Doğru kaynak eline verildiğinde çıplak 4B base, en ucuz frontier modelle ayrışmıyor.*
   **Kapasite sorunu yok.**

2. **A1'de de fark ÖLÇÜLEMİYOR.** 0.9730 vs 0.9729 (Δ **0.0001**). *Cevapladığında* base tam
   olarak Gemini kadar sadık; atıf hassasiyetinde Gemini hafif önde (1.0 vs 0.9744) ve base'in
   0.0143 wrong_ref'i var.

3. **Asıl açık coverage'da — ve büyüdü.** **%43.75 vs %76.25 = 32.5 puan.** Base distractor
   gürültüsü altında 80 sorunun **45'ini reddediyor** (over_refusal 0.5625), Gemini 19'unu (0.2375).
   Bu 12B hattının **"kör red"** deseninin birebir tekrarı. **`τ_grounding`'in çekirdek hedefi tam
   burası** — 12B'de bu kol coverage'ı %47.5 → **%72.5** yapmıştı, yani Gemini bandına.

4. **M2 near-miss'te Gemini net önde.** Rej(regex) 0.567 → **0.807**, Rej(LLM) 0.633 → **0.842**,
   fabrication 0.367 → **0.158**, parametric_leak 0.300 → **0.123**. Fark 0.21-0.24 puan —
   **varyans bandının çok üstünde, gerçek sinyal.** Hedef: `τ_abstention` (Sprint 2) +
   **red-kapısı harness'ı** (Sprint 4).
   ⚠️ **Ama M2b'de fark yok** (0.987 vs 0.970 regex; 0.973 vs 0.970 LLM) ve **M3'te ikisi de tavanda
   (1.000)**. Yani base'in abstention'ı **tek-kaynak near-miss şeklinde** zayıf, çok-kaynak
   ıskada ve boş bağlamda değil. Bu, `τ_abstention` verisinin hangi şekli öğretmesi gerektiğini
   **doğrudan söylüyor.**

5. **M5 anti-hedefte base daha temiz.** faith 0.3992 vs 0.5786, A1 0.2852 vs 0.6213. Base kaynaksız
   sorulara **daha az ikna edici** cevap üretiyor — *"güncellik kütüphanede, ağırlıkta değil"*
   ilkesiyle uyumlu. **Ama nüans:** base **daha çok cevaplıyor** (coverage %37.5 vs %23.75) ve
   cevapladığında atıfları daha kötü (cit_precision 0.5588 vs 0.8261, wrong_ref 0.372 vs 0.211).
   Yani base'in düşük M5'i "daha iyi kalibre" değil, **"daha çok konuşup daha çok uyduruyor"**.
   Gemini az konuşuyor, konuştuğunda daha tutarlı. → **İkisi de bizim protokolümüzde istenmeyen
   davranışın farklı yüzleri**; `τ_grounding` sonrası M5 tekrar okunmalı (ön-kayıtlı beklenti: ↓/→).

---

## ⚠️ Çerçeve uyarıları — bu belge NE DEĞİLDİR

| uyarı | açıklama |
| :--- | :--- |
| **Sprint 5 parite İDDİASI DEĞİL** | Bu bir **önizleme**. Kazanan konfigürasyon henüz yok (Sprint 3'te doğar). Parite iddiası **harness × {açık/kapalı}** matrisiyle, **maliyet-normalize** edilerek, **dondurulmuş TEST setinde** ve **üç-aileli panelle** kurulur. |
| **Çıplak base** | Fine-tune **yok** (`τ_grounding` henüz eğitilmedi), harness **yok** (retriever/atıf-doğrulayıcı/red-kapısı yok). Bu, tezin **başlangıç noktası**, sonucu değil. |
| **Adalet kuralı UYGULANMADI — ve uygulanması gerekmiyor** | *"Harness rakibe de verilir"* kuralı burada devre dışı, çünkü **harness ikisinde de KAPALI.** Bu bir **model-düzeyi** kıyas — tam olarak CP2/CP6'nın koşulu (aynı harness/mod/n/seed/hakem). |
| **DEV havuzu, TEST değil** | Tüm sayılar `data/eval/dev/` üzerinde. Dondurulmuş `data/eval/canon/` **görülmedi** ve nihai raporda **bir kez** görülecek. |
| **Tek hakem** | Tek aile (`gpt-4o-mini`), κ yok, self-preference ölçülmedi. Bulgu 1'deki varyans bunun somut bedeli. |
| **M5 ANTİ-HEDEF** | Gemini'nin yüksek M5'i **onun için avantaj değil.** Bu eksende "yenmek" istenmiyor. |
| **Rakip snapshot'ı pinlenmedi** | `google/gemini-3.1-flash-lite` bir model kimliği; **tarihli snapshot** ve **upstream sağlayıcı** artefaktlarda kayıtlı değil (Bulgu 4). Sprint 5'te zorunlu. |
| **Daha yeni rakipler var** | 2026-07-21 itibarıyla `google/gemini-3.5-flash-lite`, `google/gemini-3.6-flash` mevcut. 3.1-flash-lite kullanıcı tercihi; benchmark tek komut, pin revize edilebilir. |

---

## Sonuç

> **En ucuz frontier model, çıplak base'i ezmiyor.**
>
> Tavanda (M4) ve *cevapladığında* (A1) fark **ölçülemiyor**; boş bağlamda (M3) ve çok-kaynak
> ıskada (M2b) ikisi de tavanda. Açık **tam olarak iki eksende** yoğunlaşıyor:
> **coverage** (%43.75 vs %76.25) ve **near-miss abstention** (0.567 vs 0.807).
>
> Bu iki eksen, tezin **zaten planladığı** iki kolun — `τ_grounding` (coverage'ı sadakati bozmadan
> yükseltmek) ve `τ_abstention` (near-miss reddi) — ve **red-kapısı harness'ının** doğrudan hedefidir.
> Yani ölçüm, tasarımı **doğruluyor**: iş yapılabilir ve nereye yapılacağı belli.

---

## Çıktı dosyaları

| ne | yol |
| :--- | :--- |
| üretim (470 cevap × 2 özne) | `outputs/eval/m{1,2,2b,3,4,5}_{base,gem}_detail.jsonl` |
| groundedness (M1/M4/M5) | `outputs/eval/gnd_m{1,4,5}_{base,gem}{,_summary}.json(l)` |
| abstention (M2/M2b/M3) | `outputs/eval/abst_m{2,2b,3}_{base,gem}{,_summary}.json(l)` |
| register | `outputs/eval/reg_m*_{base,gem}_summary.json` |
| **A1 = cevaplanan-only** | `outputs/eval/a1_m{1,4,5}_{base,gem}.txt` *(2026-07-25 kalibre regex)* |
| hakem varyansı yedekleri | `outputs/eval/gnd_m4_gem_summary.run2-BOZUK-DETAY.json` · `gnd_m5_gem_summary.run1-BOZUK-DETAY.json` |
| üretim + skorlama script'leri | `scripts/run_gemini_benchmark.sh` · `scripts/score_gemini_benchmark.sh` |
| yarış koruması (bu oturumda eklendi) | `scripts/runlock.py` |
| DEV havuzu | `data/eval/dev/core_hard.jsonl` (80) · `trap.jsonl` (70) — TEST kesişimi 0 |

⚠️ `outputs/eval/` **gitignore'da** — bu belgedeki sayılar artefaktlar silinse de burada korunur.

## Açık işler (bu belgeden çıkanlar)

1. **Sağlayıcı pinlemesi** — `gen_eval_grounded.py`'nin OpenRouter yolu `llm_client`'a bağlanmalı
   veya `provider.order`/`allow_fallbacks=false` + gerçekleşen sağlayıcının detay çıktısına yazılması.
   **Sprint 5'in ön koşulu** (Bulgu 4).
2. **Rakip üretim maliyeti** — `llm_client.PRICE`'a `google/gemini-3.1-flash-lite`'ın
   **birincil-kaynak liste fiyatı** tarihiyle girilmeli; `gen_eval_grounded.py` token sayacı tutmalı.
   **Sprint 5'in ön koşulu.**
3. **Base'in örtük reddi** — regex'in kaçırdığı *"kaynak sadece X'i düzenler"* kalıbı (Bulgu 3c
   yan gözlemi). Regex değişikliği **tüm base çıpalarını yeniden skorlamayı gerektirir** → ayrı karar.
4. **Kesik cevap bandı** — base'de 19/470 `finish_reason=length` (M5'te 12/80). `max_new_tokens=512`
   bandı Sprint 5 öncesi gözden geçirilmeli; kesik cevap hakeme yarım gider.
5. **`sprint1.md` CP2 tablosundaki M2 regex değeri (0.500)** `abst_m2_base_summary.json`'daki
   **0.567** ile uyuşmuyor (#39'un CP2 tablosu 0.567 diyor). Ara kalibrasyon durumundan kalmış
   olabilir — **kontrol edilmeli.**
