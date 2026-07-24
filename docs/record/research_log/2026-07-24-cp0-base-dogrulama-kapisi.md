# #39 — CP0: base doğrulama kapısı (Qwen3.5-4B) · düşünce tuzağı · güç durumu tuzağı

**Tarih:** 2026-07-24 · **Faz:** Sprint 1 / Faz A · **Otorite:** `TASARIM.md` §8 · **Yürütme:** `sprint1.md` CP0-CP3
**Kararlar:** ADR-0030 (base + düşünce modu) · ADR-0031 (precision) · ADR-0032 (hakem paneli)
**Paper eşlemesi:** Methodology (base seçim protokolü) · **Limitations** (düşünce modu, tek base) ·
K3/negatif bulgular (dört sessiz-bozulma vakası) · **Results** (base çıpaları, CP2)

> **Bu girdi Faz A'nın tamamını kapsar** (CP0-CP3 + Kapı 0). CP2 base çıpaları ve dört sessiz-bozulma
> vakası aşağıda; başlıktaki "iki tuzak" CP0'a aitti, CP2/CP3 iki tuzak daha ekledi (red-regex ·
> teacher-jargon), toplam **dört**.

---

## Özet

Yeni hattın base'i **`Qwen/Qwen3.5-4B`** doğrulama kapısından **6/6** geçti. Kapı iki ayrı
**sessiz-bozulma** tuzağı yakaladı; ikisi de hata vermiyor, ikisi de sayı üretiyor, ikisi de yanlış:

1. **Düşünce kanalı tuzağı** — model varsayılan modda 1024 token'da bile `</think>` kapatmıyor;
   `message.content` **boş** dönüyor. Yakalanmasaydı CP2'nin 6 modu (480 çağrı) boş cevap üretecek
   ve red-regex o boşluklardan tablo dolduracaktı.
2. **Güç durumu tuzağı** — laptop pilde/tasarruf modundayken decode **7.9 t/s**, şarjda **134 t/s**.
   **17× fark, sıfır uyarı.** Tezin latency/throughput/`$`-per-sorgu ekseni doğrudan buna bakıyor.

---

## Künye — ölçüm koşulları

| kalem | değer |
| :--- | :--- |
| base | `Qwen/Qwen3.5-4B` · sha `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a` · HF lastModified 2026-03-02 |
| llama.cpp | `0cea362` · CUDA build, `-DCMAKE_CUDA_ARCHITECTURES=120` |
| donanım | RTX 5070 Ti Laptop, 12226 MiB, sm_120, sürücü 591.97, WSL2 |
| yığın | torch 2.10.0+cu130 · transformers 5.10.2 · unsloth 2026.6.1 · bitsandbytes 0.49.2 · triton 3.6.0 |
| seed | 3407 (protokol sabiti) |

## Base künyesi — mimari

`Qwen3_5ForConditionalGeneration`, `model_type=qwen3_5`. **Üç yapısal özellik kayda değer:**

| özellik | değer | sonucu |
| :--- | :--- | :--- |
| **hibrit dikkat** | 32 katman = **24 `linear_attention` + 8 `full_attention`** (interval 4) | KV yalnız 8 katmanda bağlamla büyür → uzun bağlam VRAM'i dense'e göre ucuz. ⚠️ 12B'nin KV matematiği taşınmaz (CLAUDE.md kuralı) |
| **VLM** | `vision_config` depth 24, hidden 1024 (~0.4B) | Metin görevinde ölü ağırlık; `all-linear` LoRA'yı oraya da takıyor (aşağıda) |
| **MTP** | `mtp_num_hidden_layers: 1` | llama.cpp'de `mtp_on_hybrid_qwen35` yolu var; kullanılmıyor |

Diğer: `hidden_size` 2560 · `num_attention_heads` 16 · `num_key_value_heads` 4 · `head_dim` 256 ·
`vocab_size` **248320** · `tie_word_embeddings: true` · `max_position_embeddings` 262144.

---

## Kapı sonuçları (TASARIM §8)

| # | kontrol | sonuç | kanıt |
| :-- | :--- | :--: | :--- |
| 1 | llama.cpp mimari desteği | ✅ | `LLM_ARCH_QWEN35` (`src/llama-arch.cpp:41`) · `conversion/qwen.py:623` `Qwen3_5TextModel` · tokenizer hash `qwen35` (`conversion/base.py:1453`). Server yüklendi ve üretti |
| 2 | şablon render'ı **gözle** | ✅ | aşağıdaki render bloğu; `enable_thinking` bayrağı **yok sayılmıyor** |
| 3 | turn işaretleri | ✅ | `<\|im_start\|>user\n` · `<\|im_start\|>assistant\n` — **eğitim** render'ında ikisi de var |
| 4 | Unsloth + sm_120 | ⚠️ koşullu | çekirdek engel çözüldü; **3 açık kalem** (aşağıda) |
| 5 | kuantizasyon | ✅ | `PURE=0` (QAT yok) · merdiven üretildi |
| 6 | lisans | ✅ | 201 satır **saf Apache-2.0**; model kartında yasak-kullanım/ek politika **yok** |

### Lisans notu

Gemma 4'ün durumundan **farklı** (ADR-0021 dipnotu): orada Apache-2.0'ın üstüne Google'ın
*Prohibited Use Policy + Intended Use Statement* katmanlanıyordu. Qwen3.5-4B'de `LICENSE` düz
Apache-2.0 metni ve model kartında `prohibit|acceptable use|use policy|restrict|must not|shall not`
kalıplarının **hiçbiri geçmiyor**. → "tamamen open-weight" iddiası bu base'de ek cümle gerektirmiyor.

---

## Şablon render'ı — gözle okunan çıktı (kapı 2)

`llama-server /apply-template`, girdi `[system: "SISTEM METNI", user: "KULLANICI SORUSU"]`:

```
--jinja YOK            → '<|im_start|>system\nSISTEM METNI<|im_end|>\n<|im_start|>user\nKULLANICI SORUSU<|im_end|>\n<|im_start|>assistant\n<think>\n'
--jinja VAR            → (birebir aynı)
  + enable_thinking=true  → (birebir aynı)
  + enable_thinking=false → '...<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

**İki ayrı sonuç:**

1. `--jinja` var/yok **aynı** render → bu llama.cpp sürümü gömülü jinja şablonunu zaten kullanıyor.
2. `enable_thinking` true/false **farklı** render → **bayrak gerçekten çalışıyor.**
   ⚠️ Bu, #38'in tam mekanizmasının bu base'de **tekrarlamadığı** anlamına gelir: Gemma 4'te minja
   `enable_thinking is defined` dalını yanlış değerlendirmiş, bayrak sessizce yok sayılmıştı.
   Qwen3.5'in şablonu **aynı jinja yapısını** taşıyor (`{%- if enable_thinking is defined and
   enable_thinking is false %}`) — yani risk aynıydı, sonuç farklı çıktı. **Varsayılmadı, ölçüldü.**

**Eğitim tarafı** (`transformers` `Qwen2Tokenizer.apply_chat_template`, assistant mesajı dahil):

```
'<|im_start|>system\nSISTEM<|im_end|>\n<|im_start|>user\nKULLANICI<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nASISTAN CEVABI<|im_end|>\n'
```

→ **Şablon, akıl yürütme izi olmayan assistant mesajına BOŞ düşünce bloğu ekliyor.** Bunun tasarım
sonucu var: SFT verimiz (`train/raft/`) akıl yürütme izi taşımadığı için **eğitim modele doğal
olarak düşünce-kapalı şekli öğretiyor.** Eval'i de kapalı koşmak bir kısıtlama değil, eğitim-eval
hizalamasıdır (ADR-0030).

**Turn işaretleri:** `--user-part='<|im_start|>user\n'` · `--assistant-part='<|im_start|>assistant\n'`.
İkisi de eğitim render'ında mevcut → `train_sft.py`'nin sessiz-bozulma assert'i geçer.

---

## 🚨 Bulgu 1 — düşünce kanalı `content`'i boşaltıyor

**Düzenek:** `llama-server` (Q4_K_M, `-ngl 99 -fa on`, ctx 4096, KV q8_0), tek RAG istemi
(TBK m.146 → "genel zamanaşımı süresi nedir"), `temperature=0`, `seed=3407`. Şarjda.

| koşul | `finish_reason` | completion_tok | `content` uzunluğu | `reasoning_content` | hız |
| :--- | :--- | ---: | ---: | ---: | ---: |
| düşünce **varsayılan** · `max_tokens=220` | `length` | 220 | **0** | 830 kar | 88.8 t/s |
| düşünce **varsayılan** · `max_tokens=1024` | `length` | 1024 | **0** | 3823 kar | 109.6 t/s |
| düşünce **kapalı** · `max_tokens=220` | `length` | 220 | 676 | 0 | 91.6 t/s |
| düşünce **kapalı** · `max_tokens=1024` | **`stop`** | **249** | 773 | 0 | 84.7 t/s |

**Mekanizma:** `add_generation_prompt` `<think>\n` açar. Bütçe içinde `</think>` kapanmazsa
llama-server ürettiğin **her şeyi** `reasoning_content`'e koyar ve `message.content` **boş** döner.
HTTP **200**, geçerli JSON, hiçbir katmanda hata yok.

**Neden kritik:** `gen_eval_grounded.py` `message.content` okuyordu → `''`. `score_abstention.py`'nin
deterministik regex'i boş string üzerinde çalışır ve **sayı üretir**. CP2 = 6 mod × 80 madde =
480 çağrı; varsayılan modda hepsi boş. Tablo dolar, koşu "başarılı" görünür, **her sayı geçersizdir.**
Bu, #38 ile **aynı sınıf** (sessiz içerik bozulması) ama **farklı mekanizma** (şablon yanlış render
edilmiyor; doğru render ediliyor ve model bütçeyi tüketiyor).

**Ek gözlem:** akıl yürütme **İngilizce** üretiliyor (*"Thinking Process: 1. Analyze the Request…"*)
— Türkçe görevde. Kayda geçti, izlenecek.

### Alınan önlem — kod

`scripts/gen_eval_grounded.py`:
- `--thinking {none,off,on}` → `chat_template_kwargs.enable_thinking` (yalnız HTTP taşıyıcı).
  `none` = bayrak gönderilmez (düşünmeyen modeller; 12B hattının davranışı, geriye dönük uyumlu).
- **Boş cevapta `SystemExit`** — teşhis mesajı `finish_reason` + `reasoning_content` uzunluğunu
  basar ve sebebi adlandırır. *Erken patla* (ADR-0026 ruhu).
- Detay çıktısına `finish_reason` ve `reasoning_len` alanları eklendi.
- Koşu sonunda **kesik cevap sayacı** (`finish_reason='length'` oranı) — yarım cevap hakeme yarım
  gider; bu bugüne kadar hiç raporlanmıyordu.

`scripts/diag_chat_template.sh` genişletildi: `--jinja` var/yok **ve** bayrak çalışıyor/yok sayılıyor
eksenlerini otomatik ayırıyor, render'ları `/tmp/diag_tpl/*.txt`'e yazıyor. Her yeni base için tekrar kullanılabilir.

---

## 🚨 Bulgu 2 — güç durumu performans sayılarını 17× bozuyor

Aynı ikili, `llama-bench`, aynı build, aynı dosyalar. **Tek fark: laptop pilde vs şarjda.**

| model | koşul | pp512 | tg |
| :--- | :--- | ---: | ---: |
| Qwen3.5-4B Q4_K_M `-fa on` | **tasarruf (pil)** | 836.39 ± 65.47 | **7.45 ± 0.26** |
| Qwen3.5-4B Q4_K_M `-fa on` | **şarj** | **4789.35 ± 813.79** | **134.34 ± 3.30** |
| Qwen3.5-4B Q4_K_M `-fa off` | tasarruf | 889.14 ± 61.13 | 7.92 ± 0.23 |
| Qwen3.5-4B Q4_K_M `-fa off` | şarj | 4188.56 ± 1014.41 | 117.93 ± 5.11 |
| Gemma 4 12B Q4_0 `-fa on` (referans) | tasarruf | 487.10 ± 25.45 | 5.50 ± 2.77 |
| Gemma 4 12B Q4_0 `-fa on` (referans) | **şarj** | **1766.89 ± 155.46** | **63.81 ± 2.89** |

GPU durumu: tasarruf **P4 · SM 180-225 MHz · bellek 9001 MHz · 33 W** ↔ şarj **P0 · SM 1515 MHz ·
bellek 14101 MHz · 130 W**. Decode **17×**, prefill **5.7×**.

**Yanlış teşhis kaydı (dürüstlük gereği).** İlk ölçüm tasarruf modunda alındı ve *"hibrit dikkatin
(Gated DeltaNet) decode yolu llama.cpp'de optimize değil"* diye yorumlandı. Referans 12B ölçümü de
**aynı tasarruf modunda** alındığı için hipotezi çürütmek yerine gürültüyle örttü. Doğru okuma
"ikisi de 15-20× yavaş → makine seviyesi" olmalıydı. Teşhis şarjdaki tekrarla düzeltildi.

**Sağlık kontrolü (şarj):** 134.34 t/s × 2.58 GiB ≈ **346 GB/s** efektif bant genişliği — bu donanım
için normal. 4B, 12B'ye göre decode'da **2.1×**, prefill'de **2.7×** hızlı; parametre oranının
beklediği yer. **Hibrit dikkat decode yolunda sorun yok.**

### Kural (yeni, bağlayıcı)

> **Hiçbir performans sayısı güç durumu kaydedilmeden raporlanmaz.** Her latency / throughput /
> `$`-per-sorgu ölçümüne `pstate` · `clocks.sm` · `clocks.mem` · `power.draw` yazılır.
> `scripts/measure_vram_stack.py` bunu otomatik yapıyor.

`-fa on` decode'da **%14** daha hızlı (134.34 vs 117.93) → **açık kalır.**

---

## 🚨 Bulgu 3 — red-regex `bulunmuyor`u görmüyordu (CP2 kalibrasyonu)

TASARIM §3.4 red-regex kalibrasyonunu **rakip aileleri** için zorunlu ön-adım ilan etmişti; CP2
ölçümü kuralın **kendi öznemizde de** gerektiğini gösterdi. Eski `score_abstention.py` regex'i
Türkçe'nin **şimdiki-zaman olumsuzunu** (`bulunmuyor`) kapsamıyordu — ve o, Qwen3.5-4B base'inin
**baskın red kalıbı**: 456 cevapta **194 kez**. Diğer fiillerde `-yor` çekimi vardı
(`düzenlemiyor`, `yer almıyor`, `içermiyor`); yalnız `bulunmak`/`kapsamak` eksikti.

**Etki ölçüldü** (eski regex → kalibre):

| mod | eski | kalibre | not |
| :--- | ---: | ---: | :--- |
| **M3** boş bağlam | **0.000** | **1.000** | base %100 doğru reddediyordu, regex hiç görmüyordu |
| **M2b** çok-kaynak-ıska | 0.662 | 0.938 | |
| M2 near-miss | 0.486 | 0.500 | |
| M4 oracle | 0.062 | 0.050 | koşul deyimi dışlaması (`hüküm bulunmazsa`) |

İkinci düzeltme: hukuk deyimi (`kanunda hüküm BULUNMAZSA`, `müdafi hazır BULUNMAZSA`) kanunun kendi
koşul dili, red değil → `(?!sa)` bakışı eledi. **Doğrulama** (§3.4): 15/15 ileri + 2/2 geri yön
elle spot-check. Kod kalibre edildi ve yorumla işaretlendi (rakip aileler eklendiğinde her aile için
tekrarlanacak).

## 🚨 Bulgu 4 — teacher jargonu `raft/` eğitim verisinde (#16 tekrarı)

`sprint1.md` *"(Mevcut set scrub'lı.)"* diyordu — o not yalnız `grounded_qa/` için doğruydu.
`data/train/raft/` (ilk eğitilecek `τ_grounding`'in verisi) **scrub'lı DEĞİLDİ**: cevaplarda
`GOLD`/`DISTRACTOR` etiketi **1301/17.323 (%7.51)**, öğrencinin girdisinde (system+user) **0/17.323**.
Yani model, karşılığı olmayan bir jetonu üretmeyi ezberleyecekti — `research_log` #16'nın birebir
tekrarı (orada %5.99'du). validation %6.44, test %7.48.

`scripts/scrub_teacher_jargon.py` yazıldı: etiketi **silmek yerine** öğrencinin gördüğü dağarcığa
çevirir (`GOLD`→"ilgili/doğru kaynak", `DISTRACTOR`→"ilgisiz"), satır **düşürmez** (düşürmek #14
topik-skew'ü tekrarlardı). `##begin_quote##` blokları **dokunulmadı** (kanun metninin birebir
alıntısı; terim hiç alıntı içinde geçmemiş). Sonuç: **1435 satır onarıldı, kalıntı 0**, alıntılar
bayt-bayt korundu, dilbilgisi gözle doğrulandı. Çıktı `data/train/raft_scrubbed/` — **orijinal
`data/train/raft/` ellenmedi** (hangisiyle eğitileceği karar).

## Bulgu 5 (küçük) — `.env` emekli base'i işaret ediyordu

`.env`'de `BASE_MODEL=google/gemma-4-12B-…` (emekli hat) duruyordu — ADR-0026'nın tam uyardığı
tuzak (gömülü/eskimiş default sessizce yanlış tokenizer). Script'ler `--model` gerektirdiği için
koşular kurtuldu (şans, tasarım değil). `Qwen/Qwen3.5-4B`'ye güncellendi + uyarı yorumu eklendi.

---

## CP2 — base çıpaları (Results kaynağı)

**Künye:** özne **Qwen3.5-4B** Q4_K_M · hakem **gpt-4o-mini** (`judge_gateway=openai`, tek aile —
iç kıyas, sprint1.md CP2) · **DEV havuzu** (core_hard 80, trap 70) · **seed 3407** · `--thinking off` ·
`max_new_tokens=512` · harness KAPALI. ⚠️ `.env`'e `OPENROUTER_API_KEY` eklenmişti ama CP2
**`LLM_GATEWAY=openai` ile pinlendi** — 6 modun hepsi tek sağlayıcı (ADR-0029; `judge_providers=[]`
= OpenAI-direct, çok-eleman değil). Çıktı: `outputs/eval/{gnd,abst,reg}_m*_base_summary.json`.

| mod | doğru davranış | faith_macro (ALL) | **A1 (cevaplanan)** | coverage | Rej(regex) | Rej(LLM) | register |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **M1** distractor | cevapla | 0.839 | **0.972** | **34/80 = %42.5** | — | — | 0.973 |
| **M4** oracle (tavan) | cevapla | 0.981 | 0.980 | 75/80 = %93.8 | — | — | 0.961 |
| **M2** near-miss | reddet | — | — | — | 0.567 | 0.633 | 0.964 |
| **M2b** çok-kaynak-ıska | reddet | — | — | — | 0.987 | 0.973 | 0.981 |
| **M3** boş bağlam | reddet | — | — | — | **1.000** | 1.000 | — |
| **M5** kör (anti-hedef) | — | 0.399 | — | — | — | — | 0.566 |

(faith = groundedness hakemi; Rej regex/LLM = `score_abstention.py` `rejection_exact`/`rejection_rate`,
geçerli-tuzak üzerinden; register = deterministik leksik proxy, hakemsiz.)

### Ana okuma — 12B'nin "kör red" deseni yeni base'de tekrarladı

**Base distractor altında az cevaplıyor:** M1'de 80 sorunun **46'sını reddetti**, yalnız 34'ünü
cevapladı (coverage **%42.5**). Ama **cevapladığında çok sadık**: A1 (cevaplanan-only) **0.972**,
ALL ortalaması ise çekinmeler yüzünden **0.839**'a iniyor. Bu, A1 kuralının (ADR-0011) neden zorunlu
olduğunun kanıtı — 12B'de ham 0.737 vs gerçek 0.904 farkı aynı mekanizmaydı.

**Ve yüksek M2/M2b/M3 reddi bu körlüğün yan ürünü, "iyi kalibrasyon" değil.** 12B çıpası %47.5
coverage / %52.5 kör-red demişti; yeni base **%42.5 / %57.5** ile aynı bandda. Yani base'in güçlü
görünen abstention sayıları (M2b 0.94, M3 1.00) kısmen "her şeyi reddetme" eğiliminden geliyor —
`τ_grounding`'in işi **coverage'ı yükseltirken sadakati korumak**, ve o zaman M2/M2b'nin gerçek
(körlükten arınmış) değerini görebileceğiz.

**M2 regex (0.567) < LLM (0.633) farkı:** hakem, "reddedip ARDINDAN açıklama olarak doğru cevabı da
veren" cevapları ABSTAIN sayıyor; regex yalnız red ifadesini görüyor. İki sayı **birlikte** okunur.

### Kapı 0 — KARAR: `τ_register` düşüyor

Register proxy RAG modlarında **0.96–0.98** (M1 0.973 · M2 0.964 · M2b 0.981 · M4 0.961; M5 0.566
beklenen — kör modda atıf işareti yok). TASARIM §7 ön-kayıtlı kuralı: *"yüksekse `τ_register`
**düşer**"* (12B'de 1.000'e oturmuştu). → **Kol 3→2, kafes 7→3 hücre** (τg · τa · τg+τa),
**FT bütçesi 6→5** (FT-3/`τ_register` düşer). Anlatı merdiveni iki basamağa iner; çatışan çift
zaten τg↔τa (TASARIM §6.3).

### CP3 — veri hazırlığı (aynı gün)

Token bütçesi (yeni tokenizer): **etkilenen %0.06** (10/17.323 kesik, 0 düşen; eşik %1) →
`max_seq_len=2048` korundu. Cevap medyanı 195 token (12B'de 196 — tokenizer Türkçe'yi neredeyse aynı
kodluyor). Smoke pack gözle doğrulandı (5 `[KAYNAK]`, RAFT 3-adım formatı, alıntı %99.25 context'te).
Aykırı değer: bir maddede **307.687 karakter** (ek/cetvel) — retriever chunk'lamada bakılacak.

---

## Kuantizasyon merdiveni

`convert_hf_to_gguf` → 441 tensör, f16 8.07 GiB. `PURE=0` (QAT checkpoint'i yok; ADR-0023'ün saf-Q4_0
kararı QAT'e özgüydü ve taşınmaz). `FIX_TOKENIZER=0` (`extra_special_tokens` zaten DICT).

| kuantizasyon | dosya | not |
| :--- | ---: | :--- |
| f16 | 8.07 GiB | ara artefakt + bf16 hizalama koşusu için saklandı |
| Q8_0 | 4.29 GiB | |
| Q6_K | 3.32 GiB | |
| Q5_K_M | 2.94 GiB | |
| Q4_K_M | 2.59 GiB | 5.13 BPW · duman testinde **3.09 GiB VRAM** @ ctx 4096, KV q8_0 |

VRAM × bağlam matrisi ayrı ölçüldü → `outputs/eval/vram_stack.json` (ADR-0031).

---

## Ortam — CP0.7 (kapı 4)

**Çözülen:** `bitsandbytes` NF4 yolu `libnvJitLink.so.13`'ü `LD_LIBRARY_PATH`'te arıyordu;
kütüphane **zaten kuruluydu** (`site-packages/nvidia/cu13/lib/libnvJitLink.so.13`), yalnız yolda
değildi. `~/code/global_venv/bin/activate`'e kalıcı export eklendi; temiz kabukta NF4 forward
doğrulandı. *Sprint belgesinin "bir haftayı yiyebilir" dediği kalem bir yol satırıydı.*

**Açık üç kalem:**

1. **`flash-linear-attention` + `causal-conv1d` kurulu değil** → *"The fast path is not available…
   falling back to torch implementation."* 32 katmanın **24'ü** linear attention; eğitimin çoğunluğu
   yavaş yolda koşacak. Faz B öncesi kurulmalı.
2. **`target_modules="all-linear"` görüntü kulesine LoRA takıyor.** Ölçülen: **38.756.352 / 2.642.481.664
   (%1,467)** eğitilebilir; takılan modüller `['down_proj','gate_proj','in_proj_a','in_proj_b',
   'in_proj_qkv','in_proj_z','k_proj','linear_fc1','linear_fc2','o_proj','out_proj','proj','q_proj',
   'qkv','up_proj','v_proj']` — `linear_fc1/linear_fc2/qkv/proj/out_proj` **`Qwen3_5VisionModel`'e ait.**
   Merge'i bozmaz (LoRA-B sıfır başlar, görüntü tarafına gradyan gelmez → ΔW=0) ama boşa parametre ve
   **CP4'ün "param sayısı makul mü" kontrolünün yakalayamayacağı** bir yanlışlık: sayı 0 değil, sadece
   yanlış yere dağılmış. → metin kulesi modül listesi **açıkça** verilecek.
3. **Unsloth `tokenizer` değil `Processor` döndürüyor** (VLM). `tok("metin")` çağrısı stringi *görsel*
   sanıp `RuntimeError: Unsupported image file` veriyor. `train_sft.py`'nin veri yolu Faz B'de
   bundan etkilenebilir — `text=` kwarg'ı ya da `tok.tokenizer` gerekecek.

---

## Base davranışı — CP2'ye taşınan gözlem

Düşünce kapalı, oracle bağlam verili tek örnekte base'in cevabı:

> *"Verilen kaynakta bu bilgi yer almıyor.* **Açıklama:** *Sizin sunduğunuz kaynak madde (Türk
> Borçlar Kanunu Madde 146), genel zamanaşımı süresinin **10 yıl** olduğunu belirtmektedir…"*

**Model hem reddediyor hem doğru cevaplıyor.** `score_abstention.py` bunu RED sayar. TASARIM §3.4
regex kalibrasyonunu **rakip aileleri** için zorunlu ön-adım ilan etmişti; bu ölçüm kuralın
**kendi öznemizde de** geçerli olduğunu gösteriyor. n=1 anekdot → CP2'de CANON n'iyle ölçülecek,
**ve kalibrasyon yapılmadan CP2'nin M2/M2b/M3 sayıları raporlanmayacak.**

12B hattının ilgili çıpası: base gold prompt'ta VARken **21/40 = %52,5** "yer almıyor" demişti
(#38 dönemi). Şekil benziyor, **sayılar taşınmaz** (farklı base, farklı protokol).

---

## Korpus ölçümü (CP3 hazırlığı)

`data/corpus/mevzuat_maddeler.jsonl` — 36.1 MiB dosya, **40.496 madde**, 28.4 MiB metin.
Madde uzunluğu: medyan **314** · p90 **1.598** · **max 307.687** karakter.
900-char eval-mirror granülerliğinde **60.297 chunk**.

⚠️ **max 307.687 karakter** tek bir maddede — muhtemelen ek/cetvel. Retriever ve chunk'lama
tasarımında ayrıca bakılacak aykırı değer (12B hattında kaynak bloğu medyanı 1.030, max 12.805
token'dı ve truncation'ın kök nedeni **oydu**, cevap değil — #15).

---

## Ders

1. **Kapı işini yaptı.** İki tuzak da CP0'da yakalandı; ikisi de CP2'de yakalansaydı geriye dönük
   fark edilemezdi (hata vermiyorlar, sayı üretiyorlar).
2. **"Aynı jinja yapısı" ≠ "aynı sonuç".** Qwen3.5'in şablonu #38'i patlatan dalı birebir taşıyor
   ama bayrak çalışıyor. Risk aynı, sonuç farklı — **her base için tekrar ölçülmeli, varsayılmamalı.**
3. **Referans ölçümü de aynı koşulda alınırsa hipotezi çürütmez, örter.** Kontrol grubunun
   *kontrol edilmeyen değişkeni paylaşması* klasik hata; burada güç durumuydu.
4. **Ortam borcu tahmin edilmez, ölçülür.** "Bir haftayı yiyebilir" denen kalem tek satırdı.

---

## Çıktı dosyaları

| ne | yol |
| :--- | :--- |
| GGUF merdiveni | `models/gguf/q35-4b-{f16,q8_0,q6_k,q5_k_m,q4_k_m}.gguf` (gitignored) |
| VRAM × bağlam matrisi | `outputs/eval/vram_stack.json` |
| şablon render'ları | `/tmp/diag_tpl/*.txt` (geçici; render metni bu girdide birebir var) |
| DEV havuzu (CP1) | `data/eval/dev/core_hard.jsonl` (80) · `trap.jsonl` (70) — TEST kesişimi 0 |
