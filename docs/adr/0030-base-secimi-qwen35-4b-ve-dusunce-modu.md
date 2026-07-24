# ADR-0030 — Base seçimi: Qwen3.5-4B · ve düşünce modu KAPALI koşulur

**Statü:** Yürürlükte · **Tarih:** 2026-07-24
**Otorite belge:** `TASARIM.md` §8 (doğrulama kapısı) · §3.1 (CANON) · `sprint1.md` CP0
**İlgili:** ADR-0026 (base bir parametredir) · ADR-0027 (çalışma varsayımı Qwen3.5-4B) ·
ADR-0028 (tek boyut noktası) · ADR-0025 (eval yolu llama.cpp) · ADR-0023 (saf-Q4_0 QAT'e özgü)
**Kanıt:** `research_log` [#39](../record/research_log/2026-07-24-cp0-base-dogrulama-kapisi.md)

---

## Bağlam

ADR-0027 base'i **çalışma varsayımı** olarak bıraktı ve TASARIM §8'de altı maddelik sert bir
doğrulama kapısına bağladı: *hiçbir koşu kapıdan geçmeden başlamaz.* Kapı 2026-07-24'te koşuldu.

Kapının varlık sebebi `research_log` #38'di: Gemma 4'te minja motoru şablonun bir dalını yanlış
render etti, model hiç durmadı, server 200 döndü, JSON geldi — ve **bir CANON koşusu sessizce
çöpe gitti.** Aynı sınıf hata bu base'de de arandı.

---

## Karar

### 1. Base = `Qwen/Qwen3.5-4B`, sha `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`

Kapı **6/6** yeşil (kanıtlar #39'da):

| # | kontrol | sonuç |
| :-- | :--- | :--- |
| 1 | llama.cpp mimari | `LLM_ARCH_QWEN35` + `conversion/qwen.py` `Qwen3_5TextModel`; yüklendi, üretti |
| 2 | şablon render'ı gözle | doğru render; `enable_thinking` bayrağı **yok sayılmıyor** |
| 3 | turn işaretleri | `<\|im_start\|>user\n` · `<\|im_start\|>assistant\n`, eğitim render'ında mevcut |
| 4 | Unsloth + sm_120 | `Qwen3_5` patch'leniyor; NF4 forward geçti; **3 açık kalem** (aşağıda) |
| 5 | kuantizasyon | merdiven üretildi; `PURE=0`, `FIX_TOKENIZER=0` |
| 6 | lisans | **saf Apache-2.0**, ek kullanım politikası yok |

⚠️ **İsim düzeltmesi.** ADR-0027 ve TASARIM §8/§2 "Qwen3.5-4B-**Instruct**" diyor. HF'de öyle bir
repo **yok**: instruct varyantın adı düz **`Qwen/Qwen3.5-4B`**, pretrain olan `Qwen/Qwen3.5-4B-Base`.
Belgelerdeki ad hatalı; bu ADR düzeltir.

### 2. Düşünce modu **KAPALI** koşulur — eğitimde ve eval'de

`--thinking off` → `chat_template_kwargs.enable_thinking=false`.

**Gerekçe ölçüldü** (#39, 4 koşullu düzenek): varsayılan modda model 1024 token bütçesinde bile
`</think>` kapatmıyor; llama-server ürettiğin her şeyi `reasoning_content`'e koyuyor ve
`message.content` **boş** dönüyor — HTTP 200, geçerli JSON, sıfır hata.

| koşul | `finish_reason` | `content` | `reasoning_content` |
| :--- | :--- | ---: | ---: |
| varsayılan · 1024 tok | `length` | **0 kar** | 3823 kar |
| **kapalı** · 1024 tok | **`stop`** (249 tok) | 773 kar | 0 |

**Asıl gerekçe kolaylık değil, eğitim-eval hizalaması.** Modelin kendi şablonu, akıl yürütme izi
taşımayan bir assistant mesajını `<|im_start|>assistant\n<think>\n\n</think>\n\nCEVAP<|im_end|>`
diye render ediyor. SFT verimiz (`train/raft/`, `orpo_abstain/`, `grounded_qa/`) akıl yürütme izi
**taşımıyor** → eğitim modele zaten düşünce-kapalı şekli öğretiyor. Eval'i açık koşmak, modeli
eğitilmediği biçimde ölçmek olurdu — protokolün `900-char` eval-mirror kuralıyla aynı mantık
(ADR-0013).

**İkincil gerekçe — maliyet.** Tezin dış iddiası maliyet-normalize parite (ADR-0017). Düşünce
token'ı ödenen token'dır; `$`/sorgu metriğine doğrudan yazılır. Kapalı modda tek cevap **249 token**,
açık modda 1024'te hâlâ bitmemişti.

### 3. Kod: boş cevap **erken patlar**

`gen_eval_grounded.py` boş `content` gördüğünde `SystemExit` verir ve `finish_reason` +
`reasoning_content` uzunluğunu basarak sebebi adlandırır. `--thinking {none,off,on}` bayrağı eklendi
(`none` = bayrak gönderilmez → 12B hattıyla geriye dönük uyumlu). Detay çıktısına `finish_reason`
ve `reasoning_len` alanları, koşu sonuna **kesik cevap sayacı** eklendi.

**Neden kod:** bayrağı unutmak mümkün ve unutmanın cezası sessiz. ADR-0026'nın *"tanımsız base erken
patlamalı"* ilkesinin aynısı: kapıyı belgeye değil koda koy.

---

## Elenen alternatifler

| eleme | neden |
| :--- | :--- |
| **Düşünce AÇIK koşmak** | Eğitim verisinde akıl yürütme izi yok → eğitim-eval uyumsuzluğu. Ayrıca `$`/sorgu metriğini şişirir ve `max_new_tokens` bütçesini belirsizleştirir (1024'te hâlâ bitmiyordu). *Ayrı bir eksen olarak ölçmek meşru ama Sprint 1'in işi değil; açık bırakıldı* |
| **Şablonu yamalamak (`.jinja`)** | Gerekmiyor — render **doğru**, bayrak **çalışıyor**. #38'de yama gerekmişti çünkü orada bayrak sessizce yok sayılıyordu. Gereksiz yama, sonraki base'lerde taşınacak bir borç olurdu |
| **Başka bir base'e geçmek** (düşünen+VLM olmayan) | Kapı 6/6 geçti; üç komplikasyonun (düşünce · VLM · hibrit dikkat) üçü de ölçüldü ve yönetilebilir çıktı. Base değiştirmek ADR-0027'yi ve CP0'ın tamamını yeniden açardı — kanıtlanmış bir sorun yokken |
| **`--jinja` bayrağını zorunlu kılmak** | Ölçüldü: `--jinja` var/yok **aynı** render. Bu llama.cpp sürümü gömülü jinja'yı zaten kullanıyor. Kayda geçti; sürüm değişirse tekrar ölçülecek |

---

## Sonuçlar / açık kalemler

**Faz B öncesi kapatılacak (CP0.7 borcu):**

1. `flash-linear-attention` + `causal-conv1d` **kurulu değil** → *"fast path is not available,
   falling back to torch"*. 32 katmanın **24'ü** linear attention; eğitim yavaş yolda koşar.
2. **`target_modules="all-linear"` görüntü kulesine LoRA takıyor.** Ölçülen 38.756.352 / 2.642.481.664
   (%1,467); modüller arasında `linear_fc1`/`linear_fc2`/`qkv`/`proj`/`out_proj` = `Qwen3_5VisionModel`.
   Merge'i bozmaz (ΔW=0) ama **CP4'ün "param sayısı makul mü" kontrolü bunu yakalayamaz** — sayı 0
   değil, yanlış dağılmış. Metin kulesi modül listesi açıkça verilecek.
3. Unsloth VLM'de `tokenizer` değil **`Processor`** döndürüyor; `tok("metin")` stringi görsel sanıyor.

**CP2'ye taşınan:** base tek örnekte **hem reddedip hem doğru cevaplıyor**
(*"kaynakta yer almıyor… Açıklama: … 10 yıl olduğunu belirtmektedir"*). `score_abstention.py` bunu
RED sayar. TASARIM §3.4 regex kalibrasyonunu rakipler için zorunlu kılmıştı; **kendi öznemizde de
zorunlu.** Kalibrasyon yapılmadan CP2'nin M2/M2b/M3 sayıları raporlanmaz.

**Limitations'a yazılacak:** modeli üreticinin gönderdiği varsayılan modda (düşünce açık) değil,
kapalı modda ölçüyoruz. Gerekçe eğitim-eval hizalaması ve maliyet muhasebesi; ama bu, base'in
tam kapasitesini ölçmediğimiz anlamına gelir ve **dürüstçe yazılır**. Aynı kural adalet gereği
rakiplere de uygulanır: düşünen rakipler de aynı politikayla koşulur ya da fark raporlanır.
