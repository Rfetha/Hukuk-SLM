# DEVİR NOTU — 2026-07-24 · e2e altyapısı kuruluyor · E4B geçiş kararı ölçüme bağlı

> ## 🔴 CANLI DURUM (2026-07-24, oturum sonu)
>
> **Nerede kaldık:** `llama.cpp` CUDA build'i koşuyor (~%76, CUDA objesi 141/186).
> Bitince script **otomatik** GGUF üretimine geçiyor. Komut idempotent:
> ```
> bash scripts/setup_llamacpp.sh all      # klon + CUDA build + 12B/E4B GGUF
> ```
> Log: son çalıştırmanın çıktısı; kontrol: `ls ~/code/llama.cpp/build-cuda/bin/llama-server`
>
> **Neden bu iş:** E4B'yi 4-bit koşturabilen **tek yol llama.cpp** çıktı (Unsloth `gemma4`'ü
> tanımıyor, transformers+bitsandbytes ağırlık dönüşümünde patlıyor, bf16 12 GB'a sığmıyor).
> Bu ADR-0025'e dönüştü ve stratejik olarak da doğru: **adalet kuralı artık yapısal garanti**
> (bizim model + rakipler aynı `OpenAI()` istemcisinden; `llama-server` ve OpenRouter ikisi de uyumlu).
>
> **Kalan zincir:** build → GGUF → `llama-server` + duman testi → **B1 regex kalibrasyonu (ZORUNLU)**
> → CANON 6-mod generation (E4B + 12B, $0) → hakem skorlama (~$0.20, **onaylı**) → **e2e sonucu**
>
> **e2e sonucu ne yapacak:**
> - E4B kullanılabilir → **FAZ C**: `_archive_12b/` emekliliği (ADR-0024) + rename (eskiler `v0.x`,
>   yeni hat `v1`) + yeni hat kurulumu + doküman finali + geçiş ADR'si
> - E4B belirgin kötü → ADR-0018 soft-gate'i yeniden değerlendir (dürüst taban 12 GB mı?), 12B kalır
>
> **Görev listesi task sisteminde** (A2–A4, B1–B5, C1+C2, C3+C4+C5, D1–D4). Faz D = revizyon
> sonrası büyük işler: harness kurulumu (tezin en büyük eksiği) · rakip baseline · KV-bit eğrisi ·
> v1 reçetesi.
>
> ### Bugünün kritik teknik bulguları (tekrar keşfetme)
> - `transformers < 5.x` **`gemma4`'ü hiç tanımıyor** → tüm eval'ler 5.x'e bağlı, lockfile hayati
> - Gemma 4 `tokenizer_config.json`'da `extra_special_tokens` **liste**, transformers 4.x dict
>   bekliyor → `AttributeError`. Yama `setup_llamacpp.sh` içinde otomatik.
> - transformers 5.x: `apply_chat_template(return_tensors='pt')` artık `BatchEncoding` döndürüyor
>   → `return_dict=True` + `**enc` şart
> - nvcc: pip paketi **yalnız ptxas** içeriyor · sistemde CUDA yok · Linux için hazır llama.cpp
>   CUDA binary'si yok · NVIDIA Vulkan ICD'si yok → NVIDIA redistributable tarball'ları
>   (`scripts/setup_cuda_toolkit.sh`, sudo'suz) + **`lib/` → `lib64/` symlink'i şart**
> - **Scratchpad oturum-kapsamlı ve TEMİZLENİYOR** — 22 GiB build+GGUF bu yüzden kaybedildi.
>   Kalıcı konumlar: `~/code/llama.cpp` · `~/code/llamacpp_venv` · `~/code/cuda-12.9` · `models/gguf/`
> - **`global_venv`'e dış araç kurma** — 6 paket bozulmuştu (torch/transformers/hf-hub/numpy/
>   protobuf/torchvision), lockfile'dan onarıldı. Dış bağımlılıklar İZOLE venv'e.
>
> ### Ölçülmüş sayılar (projeksiyon değil)
> - 12B Q4_0 `--pure` = **6.26 GiB** · varsayılan (+`token_embd` Q6_K) = 6.50 GiB · f16 = 22.20 GiB
> - E4B: decoder 4.56B + **PLE 2.90B** + vision 169M + audio 309M = **7.94B** (bf16 14.79 GiB)
> - Çalışırken VRAM (12B, Q4_0+`-fa`+KV q8_0): 32K→7.17 · **128K→7.55** · 256K→8.05 GB
> - ⚠️ **8 GB kartın 8 GB'ı kullanıcıya ait değil** — masaüstü+tarayıcı 0.5-1.5 GB → 12B pratikte
>   sığmıyor (KV'ye 0.03 GB kalıyor), **E4B@128K 5.82 GB** her senaryoda sığıyor. E4B kolunun sebebi bu.

---

# (önceki) DEVİR NOTU — 2026-07-23 · doküman hizalaması YAPILDI · base ölçümle teyit

> ## 🆕 2026-07-23 OTURUMU — ne oldu
> Kullanıcı projeyi arşivleyip (`vOLD-archived`) **sıfırdan başlamayı** sorguladı. Üç sebep vardı:
> sonuçlar ikna etmiyor · base şüphesi · tez değişti kod eski. **Sonuç: arşivleme YAPILMADI** —
> base ayağı ölçümle düştü, diğer ikisi doküman revizyonuyla karşılandı.
>
> **Kararlar (yeni ADR'ler):**
> - **ADR-0021** Base = Gemma 4 12B **teyit**, ama gerekçe değişti. Sunk-cost sıfırlanarak yeniden
>   soruldu. Gerçek gerekçe: resmî **QAT Q4_0** + **8 GB'da bağlam tavanı 176K vs 91K (1.9×)**.
>   ⚠️ Kendi "18× KV avantajı" iddiam **çürütüldü** (Qwen3.5 hibrit DeltaNet'e geçmiş → 2.5-3.7×).
>   ⚠️ "Multimodal/encoder-free" gerekçesi **ağırlıkla çürütüldü** (audio = 1 tensör/2.46M → encoder
>   yok, algılama decoder'da → `all-linear` LoRA tam oraya dokunuyor). Lisans: Apache-2.0 **+
>   Prohibited Use Policy** (saf değil).
> - **ADR-0022** Graf: **(a) yapısal/deterministik İÇERİDE** (hiyerarşi + atıf + mülga/değişik
>   zamansal zincirleri, ~0 marjinal maliyet) · **(b) çok-ajanlı GraphRAG DIŞARIDA** (~3× çıkarım →
>   parite iddiasını kendi metriğinden bozar). ADR-0019'un blanket yasağını daraltır.
> - **ADR-0023** Dağıtım config: **saf Q4_0** (token_embd Q6_K'ya yükseltilmez — QAT Q4_0 için
>   kalibre) + `-fa` + **KV q8_0** → **6.97 GB sabit / ~250K bağlam**. Harness **GPU'ya girmez**.
>   TurboQuant llama.cpp'de **yok** → önce `--cache-type-k/-v`, TurboQuant sonra.
> - **ADR-0018 karar-3 gerekçesi düzeltildi:** darboğaz KV değil **ağırlık** (KV = ağırlığın %18'i).
>
> **Yapılan işler:** `scripts/kv_cache_compare.py` (tüm sayıların kaynağı) · research_log #37 ·
> `knowledge/summary_citation_grounding.md` · spec + VISION + PAPER_TARGET + TEKNIK_PLAN +
> FINE_TUNING + CLAUDE.md + sunum revizyonu · `outputs/` temizliği (4.5G→2.5G) · v4 reçetesine
> R1/R2/R3 revizyon notları.
>
> **Açık ölçüm borçları:** ① Q4_0 GGUF üretilmedi (ağırlık 6.27 GB projeksiyon) ② CUDA ctx +
> compute buffer **tahmin** → gerçek RTX 5070 ölçümü ③ KV q8_0'ın CANON kalitesine bedeli ④ **eval
> ≠ dağıtım** (CANON bf16'da, dağıtım Q4_0+q8_0) ⑤ multimodal probe hiç koşulmadı ⑥ zamansal eksen
> CANON'da yok.
>
> **Bekleyen karar:** sürüm rename (v4→**v1**, eskiler **v0.x**) — onaylandı, henüz uygulanmadı
> (1.531 doküman geçişi + ~120 gitignored artefakt + 5 dizin; yedek→kuru-koşum→uygula→doğrula).

---

# (önceki devir notu) 2026-07-17 · TEZ YENİDEN ÇERÇEVELENDİ

> **Bu dosya = sabit eksen / canlı devir notu.** Yalnız GÜNCEL durum + sıradaki somut adım.
> Geçmiş anlatı → `docs/record/research_log/README.md` · Kararlar → `docs/adr/` · Görevler → `TODO.md`.

## 🎯 TEK CÜMLE
Proje **içeri dönük** ("FT base'i geçiyor mu?") olmaktan çıkıp **dışarı dönük** hale getirildi:
*dar bir domainde (TR hukuku) SLM+harness, kapalı ticari modellerin dağıtım sınıfına
**maliyet-normalize paritede** ne kadar yaklaşır — ve bunun ne kadarını FT, ne kadarını harness sağlar?*
v0→v3 = bu tezin **proof-of-concept**'i (çöpe gitmiyor, FT kolu oluyor).

## 📌 OTORİTE BELGE
**`docs/superpowers/specs/2026-07-17-tez-cercevesi-design.md`** (13 bölüm). Bu devir notu onun özeti.
Commit'ler: `14d22e3` (spec) + `863070e` (revizyon). **Durum: kullanıcı ONAY AŞAMASINDA — GO öncesi soruları var.**

## 🧭 KİLİTLİ KARARLAR (spec'ten)
- **Ana iddia:** maliyet-normalize parite (kalite × maliyet Pareto). Cümle: *"bu maliyetle, buraya kadar."*
- **Rakipler = kapalı ticari, dağıtım sınıfı:** Gemini 3 Flash · Claude Sonnet · GPT-5-mini.
  **Tavan referansı** (rakip DEĞİL, grafikte tek çizgi): Opus / Gemini 3.5 Pro. Nemotron kapsam dışı.
- **Base = Gemma 4 12B QAT — KESİN.** Qwen geçişi + çok-base kolu İKİSİ DE düştü. Düşük-spec derdi
  base değil KV-cache → TurboQuant kolu. Dış geçerlilik = **kapatılmayan sınır** (dürüst limitations).
- **Harness = retriever + Bedesten atıf-doğrulayıcı + red kapısı.** Graph-RAG KESİN dışarıda (future work).
- **8GB = soft gate** (≤8GB tercih, aşan config'ler kayıpla raporlanır), sert kısıt değil.
- **Rakip inference = OpenRouter** (tek anahtar, `base_url`, mevcut `OpenAI()` uyumlu). Key kullanıcıda VAR.
- **Katmanlı kapsam:** her katman tek başına savunulabilir tez. HPC (TÜBİTAK ULAKBİM → MareNostrum5)
  YÜKSELTEÇ, bağımlılık değil. HPC sübvansiyonu maliyet iddiasından İZOLE (GPU-saat piyasa fiyatı). CPT = non-goal.

## 🔬 DENEY IZGARASI (2 boyut: özne × harness)
|  | harness yok | harness var |
|---|---|---|
| **Rakipler** | A | **B** |
| **Bizim FT** (v3/v4) | C | **D** |
| **base** | (mevcut) | **E** ← tezin ana ablasyonu |

- Adil kıyas = **D vs B** (rakip + AYNI harness). "D>A" değersiz (harness'ı sadece kendine verme).
- **Mecellem** = ızgara dışı "açık referans" (yeni koşu YOK). **Tavan** = grafik referans çizgisi.
- Adalet kuralı: harness tüm öznelere BİREBİR aynı uygulanır.

## 🚦 KAPILAR (ön-kayıtlı, eşikler veriden ÖNCE yazıldı)
- **KAPI 1** (rakip baseline sonrası): maks(rakip M2) ≥0.90 → boşluk yok, v4 gereksiz · ≤0.80 → boşluk gerçek, v4 haklı · gri → ood'a bak. *(Referans: base M2=0.704, v3=0.593.)*
- **KAPI 2** (harness ablasyonu, İKİ BOYUTLU — bkz. NOT): harness'lı marj (D vs E) **VE** base-only marj (v4-çıplak vs C). İkisinden biri anlamlıysa FT haklı.
- **KAPI 3** (v4 git/gitme): Kapı1="gerçek" ∧ Kapı2="değer katıyor" → v4 koşar; yoksa koşulmaz (tez zaten tam).

## ⚙️ v4 RECIPE — DEĞİŞMİYOR, rolü değişiyor
- Recipe `docs/record/v4/recipe.md` **KİLİTLİ kalır** (DTA 2-kadran, gold-absent sweep 0.3/0.4/0.5, v2b-continuation). Teknik gövde yeni hedefle çelişmiyor.
- **Yeni rol:** v4 = harness'ın deterministik olarak çözemediği **semantik answerability** katmanı
  (atıfsız halüsinasyon + base-only dağıtım güvenliği). "M2b'yi düzelt" → "harness'a ortogonal 2. savunma katmanı."
- Eskiden zorunlu Faz-1-kapanışı; şimdi **koşullu** (Kapı 1∧2). Kapı-sonrası recipe hedef tablosuna
  "rakip-lider" + "harness-sonrası" sütunları eklenecek (ŞİMDİ değil, ölçüm gelince).

## ➡️ SIRADAKİ İŞ (GO bekliyor)
**1. Doküman hizalaması** (kullanıcı "tüm docları işle" dedi — GO öncesi sorularını bekliyoruz). Spec §10'daki 7 çelişki + 4 yeni ADR:
   - `CLAUDE.md`: faz-sırası istisnası (harness dilimi teze dahil, graph hariç) · 8GB soft-gate · OCR gerekçe-kayması düzelt
   - `VISION.md`: birincil katkı = parite+iş bölümü (benchmark=altyapı) · multimodal gerekçe-kayması (satır 35)
   - `TEKNIK_PLAN.md:192`: ADR-0003'e hizala (multimodal gerekçe değil)
   - Yeni ADR'ler: tez-çerçevesi · base-sabit+limitations · faz-sırası-istisnası · rakip-seti
   - Sunum (`docs/sunum/`): Faz 3 OCR vaatlerini gerçekle hizala (OmniDocBench 0.164, OCRTurk)
**2. Kapı 1 koşumu** (doküman sonrası): OpenRouter kur → rakipleri mevcut CANON'da çıplak ölç → M2/ood. ~$5. **⚠️ REGEX KALİBRASYONU ZORUNLU ÖN-ADIM** (spec §6.1: `rejection_exact` Gemma'ya göre yazılı, rakip reddini eksik sayar → bizim lehimize kayar → hiçbir sayı öncesinde raporlanmaz).
   - **Hangi sayı nereye (netleştirme — 2026-07-18):** KAPI 1 = YALNIZ rakipleri ölç (Gemini 3 Flash · Claude Sonnet · GPT-5-mini). Bizim taraf ZATEN ölçülü (`SCORECARD.md` = base·v2b·v2c·v3) — yeniden koşulmaz. **v1/v0 aday DEĞİL** (eski protokol / çökmüş = negatif bulgu). **v4 kapıdan SONRA** gelir (KAPI 3), aynı batch'te değil. **gpt-4o-mini = HAKEM** (yarışmacı değil, her turda kalır).
   - **Sunum kartını doldur (`docs/sunum/` sf14 "Tam Karşılaştırma"):** rakip sütunları (Gemini/Sonnet/GPT-5-mini) hazır & boş ("KAPI 1 — ölçülecek"). Sayı gelince → `scratchpad/gen_deck.js` sf14 bloğu: `COLS[]` rakip girdilerine `vi` ver + `rows[].[3]`'e rakip skorlarını ekle → `node gen_deck.js` → LibreOffice ile PDF. Kart zaten `heat()` ile otomatik renklendirir.

## 🚦 STANDING KURALLAR (değişmedi)
- **Para-kapıları (onaysız KOŞMA):** Modal eğitim · GPT-judge scoring · **YENİ: OpenRouter rakip inference.**
- **OPENAI_API_KEY / OPENROUTER_API_KEY** `.env`'de — **asla echo etme.** venv: `source ~/code/global_venv/bin/activate`.
- **Final adapter'lara + `v3/checkpoint-28`'e dokunma.** *(Kural 2026-07-23'te daraltıldı: eskiden "v2b/v2c/v3 ağırlıklarına dokunma" idi; ara checkpoint'ler kullanıcı onayıyla silindi — v2c RED, v3/ck56 = final'in kopyası.)* Korunan: tüm `*/adapter_model.safetensors`, **`v3/checkpoint-28`** (SCORECARD'da `v3ck28` sütunu ölçülü), **`v2b/`** (v4'ün zemini). `data/` + `outputs/eval` gitignored → script'ten üret; `outputs/eval` **silinmez** (59 summary = SCORECARD kaynağı, 101 jsonl = spot-check kanıtı).
- Eğitim = Modal A100 · eval generation = lokal RTX 5070.

## 📁 ELDE VAR (çöpe gitmeyen altyapı)
- **Hakem:** `judge_agreement.py` (cross-judge κ Cohen + Pearson + spot-check) · `rejection_exact` hakemsiz (score_abstention.py:40-51) · **59 summary** birikmiş.
- **Eval:** 6-mod CANON (`build_eval_sets.py`, `bench_scorecard.py`, 5× `score_*.py`) · SCORECARD.md birleşik tablo.
- **Harness tohumu:** Bedesten kontrat (`docs/BEDESTEN_API.md`) + probe (`bedesten_probe.py`) · `raft_pack.py` (retriever'ı simüle ediyor, gerçeği kurulacak).
- **FT hattı:** v2b→v3 adaptörleri (`outputs/`) + train/gen script'leri · v4 execution planı (`docs/superpowers/plans/2026-07-06-v4-execution.md`).

## v3 turu (önceki durum, referans)
Otorite: ADR-0015 + research_log #32 · SCORECARD.md. v3 KISMİ: M1↑0.881, M5↓0.075 (iyi) ama M2=0.593 base-altı + M2b=0.529 regresyon. Kök: "en ilgili kaynağı SEÇ" refleksi → abstention tek beceri değil AİLE.
