# NEXT SESSION — kaldığımız yer (2026-07-25 kapanış)

> **Bu belge ne:** oturum kapanırken elde kalan işlerin devir notu. Sayılar ölçüldü ve **burada
> korunuyor** — `outputs/eval/` gitignore'da ve bir sonraki koşuda üzerine yazılabilir.
> **Otorite:** [`TASARIM.md`](../../../TASARIM.md) · **yürütme:** [`sprint1.md`](../../../sprint1.md)
> **Bulgular:** [`research_log #39`](../research_log/2026-07-24-cp0-base-dogrulama-kapisi.md)

---

## 1. Durum özeti

| | durum |
| :--- | :--- |
| **Sprint 1 / Faz A** | ✅ **TAMAMLANDI** — 6/6 çıkış ölçütü (CP0 · CP1 · CP2+Kapı 0 · hakem paneli · CP3 · #39) |
| **CP7 — Gemini önizlemesi** | 🟡 **%90** — 6 modun tüm skorları ALINDI, kayıt belgesi yazılmadı, A1 (m4_gem) eksik |
| **Sprint 1 / Faz B** | 🔴 **BAŞLAMADI** — CP4 smoke bir kez denendi, **kritik engel bulundu** (aşağıda) |

**Kararlar bu oturumda kilitlendi:** ADR-0030 (base + düşünce modu) · ADR-0031 (precision) ·
ADR-0032 (hakem paneli). `sprint1.md` ve `TODO.md` Faz A sonuçlarıyla güncellendi.

---

## 2. ⚠️ ÖNCE OKU — Faz B'yi bloke eden kritik bulgu

**`τ_grounding` eğitimi Modal A100-40GB'de ~36 s/it ölçüldü** (step 7-9 istikrarlı 36-37 sn).
Beklenen ~4-5 s/it idi → **~11 saat / ~$25**, kabul edilemez.

**Kök neden:** `flash-linear-attention` + `causal-conv1d` **Modal image'ında YOK** →
Qwen3.5'in **32 katmanının 24'ü linear-attention** ve torch-fallback'te koşuyor
(log: *"fast path is not available ... Falling back to torch implementation"*).

> ⚠️ **Bu bir güç-durumu (laptop pil/fan) sorunu DEĞİL.** Ölçüm Modal A100'de alındı.
> (#39'daki 17× güç tuzağı ayrı bir konu ve yerel ölçümler için hâlâ geçerli.)

**Çözüm yolu — sıradaki oturumun ilk işi:**
`fla` + `causal-conv1d` uzantıları **torch ≥ 2.11** istiyor; bizim `requirements.lock.txt`
**torch 2.10** (yerel Blackwell/sm_120 için gerekli). **Ama Modal A100 = sm_80, Blackwell değil**
→ Modal image'ı yerelden **bağımsız** kurulabilir: torch ≥2.11 + `flash-linear-attention` +
`causal-conv1d`. Bu fast-path'i açar → beklenen ~4-5 s/it → ~1.5 saat.

**Plan:** taze bir subagent'a *"torch ≥2.11 + fast-path Modal image kur, CP4 smoke ile s/it
doğrula, sonra CP5"* görevi ver. **CP4 smoke s/it'i görmeden CP5'e para harcama.**

---

## 3. Kalan iş — CP7 (Gemini) · ~30 dk, ucuz

### 3.1 Elde ne var

**Üretim TAM** (`outputs/eval/m*_gem_detail.jsonl`, 470 cevap, boş yok, hepsi `finish_reason=stop`).
**Hakem skorları TAM** — 6 modun `_gem_summary.json` dosyaları mevcut.

### 3.2 ⚠️ Eksik iki kalem

1. **A1 rescore `m4_gem`** — `gnd_m4_gem.jsonl` detay dosyası **yarış sonucu bozuldu** (aşağıdaki
   ders). `m1_gem` A1 alındı (0.9729, 61/80). `m4_gem` için `groundedness.py` yeniden koşulmalı
   (~$0.035), sonra `rescore_answered.py`.
   ```bash
   source ~/code/global_venv/bin/activate && set -a && . ./.env && set +a && export LLM_GATEWAY=openai
   python scripts/groundedness.py --details outputs/eval/m4_gem_detail.jsonl --label m4_gem --mode data
   python scripts/rescore_answered.py --gnd outputs/eval/gnd_m4_gem.jsonl --bench outputs/eval/m4_gem_detail.jsonl --label m4_gem
   ```
2. **Kayıt belgesi** — `docs/record/sprint1/cp7-gemini-onizleme.md` (tablo + yorum). Sayılar §4'te hazır.

### 3.3 🚨 Bu oturumun operasyonel dersi — YARIŞ KORUMASI YOK

**Aynı label ile iki skorlama süreci paralel koşarsa detay dosyası bozulur.** Bu oturumda üç kez
oldu (ana ajanın orphan shell'i + subagent aynı `_gem` label'ına yazdı): `gnd_m4_gem.jsonl` 74/80
geçerli + 3 bozuk satır, `gnd_m5_gem.jsonl` 81 satır (1 bozuk). **Hata vermedi** — summary yazıldı
ve sayı üretti. Bu, #39'daki sessiz-bozulma sınıfının **beşinci** vakası.

> **Alınacak önlem (sıradaki oturumda koda gir):** `groundedness.py`/`score_abstention.py` çıktı
> dosyasına yazmadan önce **kilit dosyası** (`.lock`) alsın ya da aynı label için canlı süreç varsa
> **erken patlasın**. ADR-0026 ruhu: sessizce bozulmaktansa erken dur.

**Ayrıca yapıldı (bu oturum):** API timeout dayanıklılığı — `llm_client.py` + `gen_eval_grounded.py`
artık `max_retries=8`, `timeout=120s` (env: `LLM_MAX_RETRIES`/`LLM_TIMEOUT_S`). *"m5 got cut by
timeout"* sınıfı kırılma bir daha koca koşuyu düşürmemeli.

---

## 4. 📊 ÖLÇÜLEN SAYILAR — kaybolmasın (asıl değer bu)

**Künye:** DEV havuzu (core_hard 80 · trap 70) · seed **3407** · hakem **gpt-4o-mini**
(`LLM_GATEWAY=openai`, tek aile — iç kıyas) · **harness KAPALI** (ikisi de çıplak) ·
ölçüm tarihi **2026-07-24/25**.

**Özne 1:** `Qwen/Qwen3.5-4B` Q4_K_M, yerel llama.cpp, `--thinking off`, $0
**Özne 2:** `google/gemini-3.1-flash-lite` (OpenRouter, provider **Google AI Studio**)

| mod | doğru davranış | **Qwen base** | **Gemini 3.1 FL** | fark |
| :--- | :--- | ---: | ---: | :--- |
| **M1** distractor · faith_macro(ALL) | cevapla | 0.839 | **0.873** | Gemini +0.034 |
| **M1** cit_precision | | 0.978 | **0.990** | ~eşit |
| **M1** A1 (cevaplanan-only) | | **0.972** | 0.973 | **başa baş** |
| **M1** coverage | | **34/80 = %42.5** | **61/80 = %76.2** | Gemini +%33.7 |
| **M4** oracle · faith_macro | cevapla | **0.981** | 0.974 | ~eşit (base hafif önde) |
| **M4** cit_precision | | 1.000 | 1.000 | eşit |
| **M4** coverage | | 75/80 = %93.8 | 78/80 = %97.5 | ~eşit |
| **M2** near-miss · Rej(regex) | **reddet** | 0.567 | **0.807** | Gemini +0.24 |
| **M2** Rej(LLM) | | 0.633 | **0.842** | Gemini +0.21 |
| **M2b** çok-kaynak · Rej(regex) | **reddet** | **0.987** | 0.970 | ~eşit |
| **M2b** Rej(LLM) | | 0.973 | 0.970 | eşit |
| **M3** boş bağlam · Rej | **reddet** | **1.000** | **1.000** | eşit (ikisi tavan) |
| **M5** kör · faith (ANTİ-HEDEF) | ↑ istenmez | **0.399** | 0.583 | base daha "temiz" |
| **M5** cit_precision | | 0.570 | 0.748 | |
| **register** (M1 · M4 · M2 · M2b) | | 0.973 · 0.961 · 0.964 · 0.981 | 0.983 · 0.923 · 0.919 · 0.988 | ~eşit |

> ⚠️ **`m4_gem` faith için iki okuma var:** 0.987 (ilk tam koşu) ve **0.974** (ikinci koşu, üstteki
> tabloda). Fark hakem varyansı — yarış olayından bağımsız, ikisi de n=80 tam koşu. **Tabloda
> ikincisi kullanıldı; belgede bu varyans not edilmeli** (tek-hakem sınırının somut kanıtı).

### İlk okuma — yoruma temel

1. **M4 oracle'da fark yok** (0.981 vs 0.974, atıf 1.0 vs 1.0). Doğru kaynak eline verildiğinde
   **çıplak 4B base, frontier'ın en ucuz modeliyle başa baş.** Kapasite sorunu yok.
2. **A1'de de fark yok** (0.972 vs 0.973) — *cevapladığında* base tam olarak Gemini kadar sadık.
3. **Asıl açık coverage'da: %42.5 vs %76.2.** Base distractor gürültüsü altında aşırı temkinli,
   "kör red"e kaçıyor. **Bu tam olarak `τ_grounding`'in hedefi** — 12B hattında bu kol coverage'ı
   %47.5 → **%72.5** yapmıştı, yani neredeyse Gemini bandına.
4. **M2 near-miss'te Gemini net önde** (0.842 vs 0.633) — abstention kalitesi. Bu `τ_abstention`
   (Sprint 2) ve **red kapısı harness'ının** (Sprint 4) hedefi.
5. **M5 anti-hedefte base daha iyi** (0.399 vs 0.583): base parametrik ezberden daha az konuşuyor —
   *"güncellik kütüphanede, ağırlıkta değil"* ilkesiyle uyumlu. Gemini'nin yüksek M5'i onun için
   avantaj değil, bizim protokolümüzde **anti-hedef**.

**Zorluk okuması:** en ucuz frontier model bizi ezmiyor. Tavanda eşit, sadakatte eşit; açık
**coverage** ve **near-miss abstention**'da — ikisi de tezin planladığı iki kolun (τg, τa) ve
harness'ın doğrudan hedefi. **İş yapılabilir görünüyor.**

⚠️ **Çerçeve uyarısı:** bu **çıplak base**, henüz FT yok, harness yok. Ve bu **Sprint 5 parite
iddiası DEĞİL** — önizleme. Adalet kuralı (harness rakibe de verilir) burada uygulanmadı çünkü
harness ikisinde de kapalı (model-düzeyi kıyas, CP2/CP6 ile aynı koşul).

---

## 5. Sıradaki oturumun iş sırası

| # | iş | süre/maliyet | not |
| :-- | :--- | :--- | :--- |
| 1 | **CP7'yi kapat** — `m4_gem` gnd+A1 yeniden koş, `cp7-gemini-onizleme.md` yaz | ~30 dk · ~$0.04 | sayılar §4'te hazır |
| 2 | **Yarış koruması** — skorlama scriptlerine kilit/erken-patlama | ~20 dk · $0 | §3.3 |
| 3 | **Modal fast-path image** — torch ≥2.11 + `fla` + `causal-conv1d`, CP4 smoke ile s/it doğrula | ? · ~$0.15 | **Faz B'nin kapısı**, §2 |
| 4 | CP5 — `τ_grounding` tam eğitim (spawn + `--detach`) | ~1.5 sa · ~$3.6 | ancak s/it yeşilse |
| 5 | CP6 — ölçüm + `research_log #40` | ~1 sa · ~$0.25 | CP2 çıpalarıyla elmayla elma |

**Bütçe:** Modal ~$8.20 kalan ($35 cap; kullanıcı $42.50'ye çıkarmayı planladı).
OpenAI hakem bütçesi `.env`'de `OPENAI_BUDGET_USD=5` — bu oturumda ~$0.35 harcandı.

---

## 6. Bu oturumda değişen dosyalar (commit edilmedi)

**Yeni:** `docs/adr/003{0,1,2}-*.md` · `docs/record/research_log/2026-07-24-cp0-base-dogrulama-kapisi.md` ·
`docs/record/sprint1/` · `scripts/{measure_vram_stack,scrub_teacher_jargon}.py` ·
`scripts/{run,score}_gemini_benchmark.sh` · `data/train/raft_scrubbed/` · `outputs/`

**Değişen:** `sprint1.md` · `TODO.md` · `docs/adr/README.md` · `docs/record/research_log/README.md` ·
`scripts/{gen_eval_grounded,llm_client,score_abstention,train_sft,diag_chat_template,setup_cuda_toolkit}.py|sh` ·
`modal_train.py`

⚠️ `scripts/train_sft.py` ve `modal_train.py`'de **yarım kalmış Faz B değişiklikleri var**
(bf16 taban bayrağı denemesi). Sıradaki oturumda **önce `git diff` ile gözden geçir** — yarım
bırakılmış bir bayrak eğitimi sessizce bozabilir.

**Eğitim verisi kararı açık:** `data/train/raft/` (orijinal, %7.51 teacher-jargon sızıntılı) vs
**`data/train/raft_scrubbed/`** (temiz, 1435 satır onarıldı). **Öneri: `raft_scrubbed` kullan.**
