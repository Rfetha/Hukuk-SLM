# #41 — CP6: `τ_grounding` ölçümü — kör red kırıldı, bedeli cevap başına sadakat

**Tarih:** 2026-07-29 · **CP:** Sprint 1 / CP6 (son iş) · **Otorite:** [`TASARIM.md`](../../../TASARIM.md) ·
**Yürütme:** [`sprint1.md`](../../../sprint1.md) CP6

> **Bir cümlede:** `τ_grounding` base'in kör reddini kırdı (M1 coverage **%43.8 → %85.0**) ve teslim
> edilen sadık cevap kütlesini **%42.6 → %72.0** çıkardı — Gemini 3.1 Flash-Lite'ın (%74.2) 2 puan
> altı; ama cevap başına sadakat düştü (**A1 0.973 → 0.847**) ve düşüşün yarısı **gerçek**, yarısı
> hakem tarafındaki bir **biçim artefaktı**.

---

## 1. Künye — protokol sabitleri

| | değer |
| :--- | :--- |
| özne | `τ_grounding` = Qwen3.5-4B + LoRA(r=16, α=32) **merge edilmiş**, **Q4_K_M GGUF** |
| taşıyıcı | llama.cpp `llama-server` · `--ctx-size 4096 --cache-type-k/-v q8_0` |
| üretim | `--thinking off` · `max_new_tokens=512` · **seed 3407** · `--max-chunk-chars 900` (eval-mirror) |
| havuz | **DEV** (`data/eval/dev/`) — TEST (`eval/canon/`) **görülmedi** |
| n | M1 80 · M4 80 · M2 70 · M2b 80 · M3 80 · M5 80 = **470 cevap** |
| hakem | `gpt-4o-mini` · `LLM_GATEWAY=openai` · `judge_providers=[]` (OpenAI-direct, tek aile) |
| harness | **KAPALI** |
| maliyet | hakem **$0.1506** · GPU **$0** (yerel) |
| çıktı | `outputs/eval/{gnd,abst,reg,a1}_m*_tg*` · tablo: [`cp6-tablo.md`](../sprint1/cp6-tablo.md) |

**Kıyas çıpaları:** `*_base` (CP2, #39) ve `*_gem` (CP7, Gemini 3.1 Flash-Lite) — **aynı hakem,
aynı havuz, aynı n, aynı seed, aynı runtime, harness kapalı.** Rakip yeniden koşulmadı; sayıları
sabittir ve her tabloda yeniden kullanılır.

**CP5 künyesi (öznenin üretimi):** 1.083 adım · A100-40GB · **6.8-7.0 s/it** *(ADR-0033'ün 5.4'ü
smoke projeksiyonuydu)* · 2.619 tok/s · MFU ≈ %15 · **`‖τ_g‖_F = 10.4589`** · **224 LoRA çifti**
(`8 full-attn×4 + 24 linear-attn×4 + 32×3 MLP` — mimari varsayımı birebir doğruladı).

---

## 2. Eksik halka kapandı — adaptör → GGUF zinciri

`setup_llamacpp.sh` HF repo alıyordu, adaptör almıyordu; aradaki adım **yoktu**.

```
outputs/tg (LoRA) + Qwen/Qwen3.5-4B  →  scripts/merge_lora.py  →  models/merged/tg (bf16)
   →  QUANT=Q4_K_M PURE=0 setup_llamacpp.sh  →  models/gguf/tg-q4_k_m.gguf  →  llama-server
```

**`merge_lora.py` akıtmalı** (tensör-tensör), `PeftModel.merge_and_unload()` **değil** — CLAUDE.md
merge doktrini ("host RAM, streaming") ve Sprint 3'ün k-yollu TIES'i aynı raydan geçecek.
`ΔW = (α/r)·B@A`, float32'de toplanıp özgün dtype'a dönüyor. 41 sn, tepe RSS 9.86 GB.
⚠️ **WSL2 15.9 GB görüyor** (host 32 GB; `.wslconfig`'de `memory=` yok → varsayılan %50).

**İki teyit kapısı geçildi:**

| kapı | beklenen | ölçülen |
| :--- | :--- | :--- |
| `‖merged − base‖_F` ≈ `‖τ_g‖` | 10.4589 | **10.4966** (+%0.36 — bf16 yuvarlama gürültüsü) |
| GGUF boyutu = base | 2.59 GiB | **2.59 GiB** ✅ (LoRA merge parametre sayısını değiştirmez) |
| görüntü kulesi · `mtp` · embed | Δ = 0 | **tam olarak 0** — metin kulesi dışına sızma yok |

**`setup_llamacpp.sh` iki düzeltme aldı:** (a) artık **yerel dizin** de alıyor; (b) `cd "$LC"`
yüzünden göreli yol çözülmüyordu **ve `set -e`, `snap=$(ls …)` atamasında mesajsız öldürüyordu** —
hattın klasik sessiz-ölüm deseni, `|| true` ile kapatıldı.

---

## 3. Sonuç — üçlü tablo

Kaynak: [`docs/record/sprint1/cp6-tablo.md`](../sprint1/cp6-tablo.md) (`scripts/compare_runs.py` üretti).

| eksen | base | Gemini 3.1 FL | **`τ_g`** | ön-kayıt | tuttu mu |
| :--- | ---: | ---: | ---: | :---: | :---: |
| **M1** coverage | 35/80 = %43.8 | 61/80 = %76.2 | **68/80 = %85.0** | ↑↑ | ✅ |
| **M1 A1** (cevaplanan) | 0.9730 | 0.9729 | **0.8472** | ↑↑ | ❌ **düştü** |
| M1 faith_macro (ALL) | 0.8385 | 0.8734 | 0.8371 | ↑↑ | → |
| M1 cit_precision | 0.9775 | 0.9900 | 0.9500 | — | ↓ *(gürültü bandında)* |
| **M4** A1 / coverage | 0.9800 / %95.0 | 0.9793 / %97.5 | 0.9794 / %96.2 | → | ✅ tavan |
| **M2** Rej (LLM) | 0.6330 | 0.8420 | **0.4580** | ↓↓ | ✅ |
| **M2b** Rej (LLM) | 0.9730 | 0.9700 | **1.0000** | ↑ | ✅ |
| **M3** Rej | 1.0000 | 1.0000 | 1.0000 | → | ✅ tavan |
| **M5 A1** *(ANTİ-HEDEF)* | 0.2852 | 0.6213 | **0.4018** | ↓/→ | ❌ **yükseldi** |
| M5 coverage | 30/80 = %37.5 | 19/80 = %23.8 | 29/80 = %36.2 | ↓/→ | ✅ |
| register proxy (RAG modları) | 0.961-0.981 | 0.919-0.988 | **0.945-1.000** | → | ✅ |

⚠️ `Rej` paydaları modele göre değişir (`valid_traps`: M2 60/57/**59** · M2b 75/67/**80** ·
M3 57/57/**50**) — oran payda ile birlikte okunur.
⚠️ **Gemini'nin regex-red sayıları raporlanamaz** — o aile için kalibrasyon yapılmadı
(TASARIM §3.4); yalnız LLM-red satırı okunur. Borç açık.

---

## 4. Ana okuma

### 4.1 Kör red kırıldı — hattın ana kazancı

Base 80 sorunun **45'ini reddediyordu** (gold **promptta varken**) — #39'un "kör red" teşhisi.
`τ_g` bunu 12'ye indirdi. **Teslim edilen sadık cevap kütlesi** (cevaplanan × A1, 80 üzerinden):

| | base | Gemini 3.1 FL | **`τ_g`** |
| :--- | ---: | ---: | ---: |
| sadık-cevap kütlesi | 34.1 → **%42.6** | 59.3 → **%74.2** | 57.6 → **%72.0** |

`τ_g` bu eksende **base'i ikiye katladı** ve rakibin 2 puan altına geldi.

### 4.2 Ama A1 düşüşü **seçim yanlılığı değil** — eşleştirilmiş alt küme

"Zor soruları da cevapladığı için ortalama düştü" savunması sınandı. Her ikisinin de cevapladığı
**ortak 27 soruda**:

| ortak 27 soru | A1 |
| :--- | ---: |
| base | **0.9774** |
| Gemini | **0.9795** |
| **`τ_g`** | **0.8778** |

**Kolay sorularda da ~0.10 düşük.** Gerileme gerçek. *(Yalnız `τ_g`'nin cevapladığı 41 soruda
A1 = 0.8271 — yani zor dilim ek olarak biraz daha düşük, ama farkın kaynağı o değil.)*

### 4.3 Düşüşün **yarısı hakem tarafında bir biçim artefaktı** — ⚠️ kafesin tamamını etkiler

M1'de cevaplanan iddiaların etiket dökümü:

| | base | **`τ_g`** |
| :--- | ---: | ---: |
| toplam iddia | 147 | 242 |
| `CONTRADICTED` *(gerçek hata)* | **1** | **11** |
| `NOT_IN_SOURCE` | 3 | **31** — bunun **18'i (%58) meta-iddia** |
| hatalı iddia oranı | %2.7 | **%17.4** |
| meta-iddia düşülürse | %2.7 | **%9.9** |

Meta-iddia = RAFT şablonunun **1. adımı**: *"İlgili kaynak KAYNAK 3'tür çünkü diğer kaynaklar farklı
konuları ele almaktadır."* Bu cümle **kaynak hakkında**, kaynaktan değil — hakem haklı olarak
`NOT_IN_SOURCE` diyor. Ama `τ_g` onu yazmak **zorunda**: eğitim verisinin %77'si bu biçimde
(`train/raft/`, ADR-0013).

**Neden kritik:** kafesin **8 eval koşusunun** hepsi bu hakemden geçecek. `τ_g` içeren her hücre
sistematik ceza alacak, `τ_a` tekili almayacak → **Kapı 5'in iç-iddia kıyası bozulur** (ADR-0037
`min`(grounding, abstention) kuralı taraflı bir grounding sayısı üzerinde çalışır).
→ **Açık soru olarak kayda geçti** (`docs/open_questions.md` §13.8). Sayılar **düzeltilmedi** —
düzeltme yapılacaksa ön-kayıtlı olur ve **base + Gemini dahil tüm kollara** yeniden uygulanır (~$0.12).

### 4.4 M2 düştü — ön-kayıtlı, panik değil; **ama M2b 1.000**

M2 (near-miss, tek kaynak, oracle çerçevesi) **0.633 → 0.458**. Bu şekil eğitim verisinde **hiç yok**.
Ön-kayıt tam bunu bekliyordu (`sprint1.md` CP6).

**M2 ve M2b birlikte okunur** (ADR-0011 disiplini): eğitim-eşleşmeli **M2b 0.973 → 1.000** ve
**M3 1.000** sabit. Yani model "gold yoksa reddet" davranışını **öğrendiği çerçevede kusursuz**
yapıyor, öğrenmediği çerçevede kaybediyor. 12B'de aynı desen vardı (M2-oracle 0.346 ↔ M2b 0.96).
→ **`τ_abstention` kolunun ve merge'ün varlık gerekçesi tam olarak bu.**

⚠️ M2b'nin **paydası da büyüdü** (75 → 80): base'de 5 tuzak "geçersiz" sayılmıştı (kaynak cevaplıyor);
`τ_g`'de hiçbiri geçersiz değil. Yani 1.000 daha zor bir paydada alınmış.

### 4.5 ❌ **ANTİ-HEDEF İHLALİ — M5 yükseldi**

| M5 (kör, bağlamsız) | base | Gemini | **`τ_g`** |
| :--- | ---: | ---: | ---: |
| **A1** (cevaplanan) | 0.2852 | 0.6213 | **0.4018** |
| cit_precision | 0.5588 | 0.8261 | **0.6786** |
| coverage | %37.5 | %23.8 | %36.2 |

Coverage sabit (kör cevaplama artmamış) ama **cevapladığında daha doğru**: A1 **+0.117**, atıf
kesinliği **+0.120**. Hakem gürültü bandının (≈±0.005 faith) çok üstünde.

**Bu ön-kayıtlı beklentinin ihlali ve birinci sınıf bir negatif bulgu.** RAFT eğitimi kanun metnini
bol miktarda gösterdi; bir kısmı **ağırlıklara** yerleşti. CLAUDE.md'nin çekirdek kısıtı —
*"güncellik kütüphanede yaşar, modelin beyninde değil"* — bu eksende **kısmen delindi**.
Limitations'a yazılacak; `τ_a` ve merge hücrelerinde **tekrar ölçülmeli** (birikiyor mu?).

---

## 5. Sprint 1'in üç çıkış sorusu

1. **Hat çalışıyor mu?** ✅ veri → eğitim → **merge → GGUF** → eval, yeni base'de uçtan uca. Eksik
   halka (adaptör→GGUF) bu oturumda yazıldı ve iki kapıyla doğrulandı.
2. **`τ_g` ne satın aldı?** Kör reddin kırılması: coverage **+41.2 puan**, sadık-cevap kütlesi
   **%42.6 → %72.0**, M2b **1.000**, register korundu.
3. **Yan hasar ne kadar?** İki eksende gerçek: **A1 −0.126** (eşleştirilmiş alt kümede −0.10, yani
   seçim değil) ve **M5 anti-hedefi +0.117**. Üçüncüsü ölçüm artefaktı (§4.3), gerçek değil.

---

## 6. Yan bulgular

**Hakem gürültü bandı — bedava tahmin.** `gnd_m4_gem_summary.run2-BOZUK-DETAY.json` ve
`gnd_m5_gem_summary.run1-BOZUK-DETAY.json` aynı cevaplar üzerinde **ikinci hakem koşusu** (detay
dosyaları üzerine yazıldığı için yeniden adlandırılmışlar; **hiçbir belgede geçmiyorlardı**):

| eksen | koşu A | koşu B | fark |
| :--- | ---: | ---: | ---: |
| M4 faith_macro | 0.9736 | 0.9738 | **0.0002** |
| M5 faith_macro | 0.5786 | 0.5832 | **0.0046** |
| M5 **cit_precision** | 0.7917 | 0.7475 | **0.0442** |

→ `faithfulness_macro` tekrar-kararlı (≤0.005); **`cit_precision` tavan dışı bölgede ±0.04 oynuyor.**
CP6'da M1 cit_precision düşüşü (0.9775 → 0.9500) bu bandın içinde — **sinyal sayılmadı.**
⚠️ Tüm koşular `runs=1`; güven aralığı yok (§13.3 güç analizi hâlâ açık).

**Kesiklik `τ_g` aleyhine yanlılık yaratmıyor** (`finish_reason='length'`): M1 base 3/80 → `τ_g`
**0/80** · M2b base 4/80 → **0/80** · M5 base 12/80 → 10/80. RAG modlarında `τ_g` hiç kesilmedi.

**Belge çelişkileri işaretlendi** (sessizce üzerine yazılmadı) — `sprint1.md` CP2 "GERÇEKLEŞEN"
tablosu artefakt JSON'larla **dört yerde** uyuşmuyor:

| eksen | `sprint1.md` | **artefakt (otorite)** | `research_log` #39 |
| :--- | ---: | ---: | ---: |
| M1 coverage | %56 | **%43.8 (35/80)** | %42.5 (34/80) |
| M1 A1 | *(yok)* | **0.973** | 0.972 |
| M2 Rej(regex) | 0.500 | **0.567** | 0.567 |
| M2b Rej(regex) | 0.938 | **0.987** | 0.987 |

#39 ile artefakt arasındaki 1 örneklik fark **açıklanmadı** — muhtemel sebep red-regex
kalibrasyonundan sonra `rescore_answered.py`'nin yeniden koşması, ama **doğrulanmadı.**
CP6 tablosu artefakt JSON'larından üretildi.

**`--thinking off` `sprint1.md` CP2 komut bloğundan atlanmıştı** (koşu onunla yapıldı, künye #39'da).
Blok düzeltildi; CP6 aynı bayrakla koştu — elmayla elma korundu.

---

## 7. Paper eşlemesi

- **Results** — §3'ün üçlü tablosu; iç iddianın ilk hücresi (`τg` tekili).
- **Negatif bulgu (birinci sınıf)** — §4.5 M5 anti-hedef ihlali: RAFT eğitimi parametrik bilgi
  sızdırdı. §4.4 M2 çöküşü (ön-kayıtlı, `τ_a`'nın gerekçesi).
- **Methodology** — §4.2 eşleştirilmiş alt küme kontrolü (coverage değişince A1 kıyası nasıl yapılır);
  §2 merge→GGUF zincirinin iki doğrulama kapısı.
- **Limitations** — §4.3 biçim artefaktı (RAFT meta-iddiaları groundedness hakeminde cezalanıyor);
  §6 `runs=1`, güven aralığı yok; rakip tarafında regex kalibrasyonu ve sağlayıcı pinlemesi eksik.

---

## 8. Sonraki

- **Sprint 1 kapanır.** CP6 son işti.
- 🔴 **Açık ve Sprint 2'yi bekletebilir:** §13.8 (biçim artefaktı) — karar `τ_a` eğitiminden **önce**
  verilmeli, yoksa kafesin 8 koşusu taraflı bir grounding sayısıyla üretilir.
- 🟡 Gemini ailesi için **red-regex kalibrasyonu** (para gerektirmez) — kapanınca rakibin regex
  satırları raporlanabilir hâle gelir.
- 🟡 Rakip tarafında **sağlayıcı/sürüm pinlemesi + üretim maliyeti** kaydı (Sprint 5 ön koşulu).
