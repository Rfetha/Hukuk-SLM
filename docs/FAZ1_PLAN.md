# FAZ 1 — ~~Vatandaş-dilli~~ Uzman-register Hukuk SLM — Nihai Execute Planı

> ⚠️ **SÜPERSED BAŞLIK (2026-06-13, ADR-0010):** "Vatandaş-dilli" → birincil register **uzman/hukukçu**; vatandaş sadeleştirmesi app-layer. Eski başlık iz olarak korunuyor.
> ⚠️ **DURUM GÜNCELLENDİ (2026-07-01):** bu dosyanın "v0/v1" execute akışı **tamamlandı**. v1 SFT Modal A100'de koştu (2026-06-09), canon pilot v1'i eğitim hedefi olarak reddetti (ADR-0012); aktif iş artık **v2b SFT**. **Güncel otoriter plan: `docs/V2_PLAN.md` + `NEXT_SESSION.md`.** Bu dosya Faz-1 v0/v1 tarihçesi olarak korunuyor.

> **Bu doküman Faz 1 (v0/v1) için tek otoriter checklist'tir.** `TEKNIK_PLAN.md` ile çeliştiği yerde
> **bu doküman geçerlidir** (en güncel kararlar 2026-06-08). Strateji/gerekçe `TEKNIK_PLAN.md`,
> veri `VERI_PLANI.md`, akademik hedef `PAPER_TARGET.md`.
>
> **~~EN GÜNCEL DURUM (2026-06-08)~~ — TARİHSEL (v1-era):** v0 başarısız (veri base-altı) → grounded çözüm kanıtlandı →
> **Adım 4 BİTTİ: ~21K saf grounded `sft_v1` üretildi** (GPT-4o-mini, incremental+resume). ~~**SIRADAKİ =
> Adım 5: v1 SFT (Modal A100).**~~ → **v1 SFT KOŞTU (2026-06-09); güncel iş v2b, bkz. V2_PLAN.md.** 4 büyük karar: (1) ana metrik = **groundedness** (Muhakim ikincil/yanlı);
> (2) **sadelik model şartı YOK** — app-layer (ADR-0010); (3) hedef = TR rakipleri geçen doğru+grounded SLM;
> (4) eğitim = **Modal**, insan-κ **descope** (hakem-uyumu). Detay + `[[eval-accuracy-gate]]` + `[[cloud-gpu-modal]]`.

## Hedef
Gemma 4 12B'yi Türk hukukunda **doğru + tam + kaynağa dayalı** cevap veren, **diğer TR hukuk
rakiplerinden iyi hizmet veren** bir law-domain SLM'e QLoRA ile fine-tune et.
(Bu, `[[paper-target]]` boru hattının ilk halkası: encoder-free SLM → RAG → agent.)

**⚠️ KISALIK/SADELİK MODEL ŞARTI DEĞİL (karar 2026-06-08, `[[eval-accuracy-gate]]`).** Çift kitle:
profesyonel + vatandaş. Model **dolu+doğru** kalır; **vatandaş sadeleştirmesi APP katmanında**
(prompt config, vatandaş modu) yapılır. v0 tuzağı: modeli sade/kısa yapmak doğruluğu düşürdü.

**Bitiş kriteri (rakip-göreli, GÜNCELLENDİ 2026-06-08):** skorkartta (`build_scorecard.py`)
- **ANA = Groundedness/sadakat:** rakip baseline'lara ≥ ve ham base'e göre + (uydurma kanun/çelişki yok).
- **İkincil (bilgi) = Muhakim** çok-eksen (derinlik/atıf — profesyonel sinyali, KAPI değil; kısa-sade'ye yanlı).
- **Sadelik:** model gate DEĞİL → yalnızca app/vatandaş-modu eval'inde ölçülür (Faz 3).
- **Rakip baseline'lar:** `newmindai/Mecellem-Qwen3-4B-TR` (en yakın decoder; ⚠️ continual-pretrain,
  instruction-tuned değil — "foundation karşılaştırması" diye çerçevele) + en az bir instruction-tuned
  legal varyant (`newmindai/Llama-3.1-8B-Instruct-*`) + GPT-4o (tavan). Aynı 30+ soru, aynı hakemler.
- _Eski "sınav +%15" ve "sadelik açık üstün" kriterleri askıda; yerine groundedness-kapılı rakip skorkartı._

## Önkoşullar
- [x] Ortam: WSL2 + Blackwell sm_120 stack → `~/code/global_venv` (Py3.12, torch 2.10+cu128, unsloth 2026.6.1, bnb 0.49.2). env smoke yeşil, `requirements.lock.txt` kilitli.
- [x] Veri: `data/processed/sft_v0/` (32.234 Q&A, OrionCAF 18K+Renicames 14K, doğru ama **jargonlu**, medyan 30 kelime) + `data/raw/mevzuat_maddeler.jsonl` (40.853 madde, grounding zemini).
- [x] Base indir: `google/gemma-4-12B-it-qat-q4_0-unquantized` (24GB bf16) — **indirildi, tam.**
- [x] **Otonom driver:** `scripts/run_phase1.sh` (smoke→train→base eval→v0 eval→rapor, `set -e`, `V0_EPOCHS` env, `PYTHONUNBUFFERED`). Runbook: `docs/RUNBOOK_FAZ1.md`.

## Kararlar (sabit)
> 📒 **Gerekçeli karar kayıtları → `docs/adr/`** (neden/alternatif/sonuç; paper Methodology+Limitations kaynağı). Bu bölüm canlı *özet*; ADR = dondurulmuş anlatı. `[[adr-decision-log]]`
- **Eval terazisi (GÜNCELLENDİ 2026-06-08, `[[eval-accuracy-gate]]`).** Model hedefi = doğru+tam+kaynağa dayalı; kısalık/sadelik model şartı DEĞİL:
  - **ANA KAPI = Groundedness/sadakat → `scripts/groundedness.py` (KURULDU 4b):** akademik
    format — **FactScore** iki-aşamalı (claim-extract → kaynağa-karşı-verify) + **ALCE** gold-bağlı
    atıf sınıflama. Metrikler: faithfulness (SUPPORTED/iddia), hallucination, **wrong_ref_rate**
    (doğru kanun yanlış madde / bozuk ad — en tehlikeli), cit_precision/recall, unsupported. Stil-bağımsız.
    Yer-gerçeği: grounded veride kaynak madde (`--mode data`); modelde Faz 2 RAG (`--mode model`).
    `--runs N` count'u stabilize eder; `--judge-model gpt-4o` paper-grade. gnd_gpt: faithfulness **0.97** / hall **0.03**.
    **Açık (paper-grade):** #2 hakem self-preference → büyük koşuda `--judge-model gpt-4o`.
    **#3 insan-κ → DESCOPE (2026-06-08):** fiziksel insan iş gücü yok → avukat-κ ŞART DEĞİL (gelecek iş).
    Yerine SIFIR-EMEK vekil: **hakem-uyumu** (gpt-4o-mini ↔ gpt-4o inter-judge agreement) + `--runs N`
    kararlılık + opsiyonel yazar-örneklem. Sayılar **göreli** okunur; meşru çünkü iddia = kaynağa-sadakat
    + rakip-göreli üstünlük, mutlak hukuki geçerlilik değil → avukat gerekmez.
  - **İKİNCİL (bilgi) = Muhakim** (ArmoRM 8B, çok-eksen). Derinlik/kapsam/atıf sinyalleri profesyonel-kullanım için raporlanır; **KAPI DEĞİL** çünkü kısa-sade doğru cevapları yanlı cezalıyor (elle doğrulandı: grounded id=8/id=6 doğru ama Muhakim ≈0). Bu yanlılık paper K3 kanıtı.
  - **Sadelik = MODEL GATE DEĞİL.** App/vatandaş-modu eval'ine taşındı (Faz 3, prompt config). GPT-4o-mini doğruluk hakemi de gürültülüydü → ana kapı değil.
  - Skorkart: `scripts/build_scorecard.py` (KURULDU — **ANA sütun = groundedness**, Muhakim ikincil'e indi) → `outputs/PHASE1_REPORT.md`. Ayrışma bayrağı artık Grounded↔Muhakim: "Grounded↑ Muhakim↓" = Muhakim'in kısa-sade-doğruya körlüğü (K3 otomatik kanıt). Muhakim indirme: `scripts/dl_muhakim.py`. `[[eval-harness-decision]]`
- **Grounded üretici = GPT-4o-mini** (KESİNLEŞTİ 2026-06-08). Kanıtlı faithfulness 1.0, 20K üretim ~$1.2 → para engel değil, kalite kanıtlı. **Yerel Gemma bake-off ATLANDI** (gereksiz). Üretici: `scripts/gen_sft_v1.py` (incremental yazma + resume + timeout). (Not: "sadeleştirme öğretmeni" düştü — sadeleştirme app-layer.)
- **Eğitim yeri = Modal (serverless A100), `[[cloud-gpu-modal]]`** (KARAR 2026-06-08). Yerel RTX 5070 = sadece prototip/smoke. v1 SFT → Modal A100-40GB (~5.5h/epoch ≈ $11.5, $30 kredi). **Eval + veri üretimi LOKAL/OpenAI** kalır. `modal_train.py` smoke kanıtlandı; auth+secret tamam.
- **Bulk kanun çekimi → Faz 2'ye ertelendi** (donmuş 40K madde Faz 1 için yeterli, çizelge S1).

## Akış

### Adım 1 — Eval terazisi kur ✅
- [~] ~~Staj/baro sınavı soru havuzu~~ → **ertelendi** (HF'de hazır MCQ havuzu yok; EDA edildi. Gerekirse sonra derlenir — `[[eval-harness-decision]]`).
- [x] Göz testi + hakem seti: `data/eval/eval_sample_v1.jsonl` (sabit-seed 30 gerçek vatandaş sorusu + avukat referans cevabı, `make_eval_sample.py`). base+v0 **aynı sorularla** ölçülür.
- [x] `scripts/eval.py`: model → cevap üret → **GPT-4o-mini hakem** (doğruluk + sadelik rubriği) → skor + göz testi md dökümü. `$OPENAI_BUDGET_USD` guard.
- **Çıktı:** ✅ çalışan terazi (revize omurga = izole sample + GPT-4o-mini hakem + göz testi).

### Adım 2 — Ham base ölç (referans) ✅
- [x] Fine-tune'suz Gemma 4 12B → `eval_sample_v1`. **base: GPT doğruluk 7.87 / sadelik 6.47; Muhakim legal_acc +0.362.**
- **Çıktı:** base referans skoru (`outputs/eval/base_*`).

### Adım 3 — v0 SFT (eldeki 32K veri) ✅ *BİTTİ — başarısız, ders alındı*
- [x] `scripts/train_sft.py`: Unsloth FastModel, NF4 4-bit, r=16/alpha=32, batch=1 ga=16, lr=2e-4, cosine, max_seq=2048. ⚠️ Gemma 4 turn işaretleri `<|turn>user/model`.
- [x] 1 epoch (1815 adım, loss 1.35→0.63). **Sonuç: GPT doğruluk 7.87→6.13, Muhakim legal_acc 0.362→0.124.**
- [x] **Teşhis (ölçüldü, tahmin değil):** 32K = forum savuşturmaları (medyan 21-30 kelime), **kendi legal_acc'ı 0.274 < base 0.362** → modelden düşük doğrulukta veriyle eğittik → doğruluk çöktü + 1 echo dejenerasyon. **Ders: veri sorunu, ayar değil (epoch/lr çözmez).**
- **Çıktı:** `outputs/v0` + `outputs/PHASE1_REPORT.md`.

### Adım 4 — Veriyi iyileştir (GROUNDED — asıl iş) ✅ *BİTTİ*
> Karar: doğruluk forumdan gelmez, **gerçek maddeden imal edilir.** Kısalık/sadelik HEDEF DEĞİL → model dolu+doğru kalsın.
- [x] **Kanıt koşusu (25 GPT-4o-mini):** gerçek madde → soru+doğru+atıflı cevap → grounded yaklaşımı çalışıyor.
- [x] **4b — Groundedness skorlayıcı KURULDU (`scripts/groundedness.py` + `build_scorecard.py`):** FactScore iki-aşamalı + ALCE gold-bağlı atıf. faithfulness 0.97 / hall 0.03 / wrong_ref 0.04. Scorecard ANA sütun = groundedness; ayrışma bayrağı K3 kanıtını otomatik üretiyor.
- [x] **4a — Sampling düzeltildi (`gen_grounded.py`):** substring `CITIZEN_LAWS` → tam-ad `ALLOWED_LAWS` (10 vatandaş kanunu); `usable()` mülga+`STUB_MARKERS`+`AMEND_RE` ile id=17 tipi maddeleri eler; template `<...>` sızıntısı düzeltildi. Doğrulandı: havuz 2759 madde / ASKERİ 0; gnd_gpt2 faith 1.0 / hall 0.0 / wrong_ref 0.0.
- [x] **4c — Bake-off ATLANDI:** öğretmen = GPT-4o-mini (kanıtlı, ucuz). Yerel Gemma kıyası gereksiz.
- [x] **4d — ~21K grounded üretildi (`scripts/gen_sft_v1.py`):** 2759 vatandaş maddesi → madde başına 3-8 ayrık çift. **Incremental yazma (`fsync`) + resume** (WSL-safe) + 4 worker + 60sn timeout. **32K KATILMADI** (v0'ı batıran + kaynaksız → groundedness puanlanamaz; v1 = saf grounded). → `data/processed/sft_v1/{raw_pool,train,validation,test}.jsonl`.
- **Çıktı:** `data/processed/sft_v1/` (saf grounded, doğru+dolu+atıflı, her örnekte `kaynak_madde`).

### Adım 5 — v1 SFT (Modal A100) + iterasyon ✅ *TAMAMLANDI (2026-06-09)*
> **DURUM (2026-07-01):** v1 SFT Modal A100'de koştu (1 epoch, 1207 step, ~3.5h ≈ $10). Canon pilot (ADR-0012) v1'i **eğitim hedefi olarak reddetti** (abstention 0.741→0.000, oracle'da bile base-altı) → aktif iş **v2b** (base'den taze QLoRA). Detay: `docs/record/research_log.md` 2026-06-09/13, `docs/V2_PLAN.md`.
- [x] **Kalite ön-kontrol:** `score_grounded_corpus.py` ile `sft_v1` örneklemi puanlandı (n=40, faithfulness 0.984). Grounded olduğu için temiz çıktı (ADR-0002).
- [x] **Modal'a yükle:** `sft_v1` → `hukuk-data` volume.
- [x] **modal_train.py → v1:** smoke + tam koşu (Modal A100, spawn/detach — ADR-0008).
- [x] **Adapter indir → eval LOKAL:** `outputs/v1/`; canon pilot base/v0/v1 kıyası yapıldı (`outputs/BENCHMARK_REPORT.md`).
- [x] v2 kararı → **v2b** (V2_PLAN); v1 üstüne DEĞİL, base'den taze.
- **Çıktı:** v1 adapter + canon pilot → scope=Product A kararı.

### Adım 6 — Rakip kıyas + güvenilirlik + deploy
> ⚠️ **v2b tamamlanmadan başlatılmaz.** Güncel birincil skorlayıcı = `bench_scorecard.py` (canon), `build_scorecard.py` değil.
- [ ] **Rakip baseline'ları BİZİM terazide ölç:** `Mecellem-Qwen3-4B`, `Llama-3.1-8B` → canon scorecard (paperlarından sayı ALMA).
- [ ] **Güvenilirlik katmanı (EN SON):** hakem-uyumu (gpt-4o-mini ↔ gpt-4o) + opsiyonel yazar-örneklem. Avukat-κ descope.
- [ ] Bitiş kriteri: **groundedness'te rakipleri ≥ + base'e göre +.**
- [ ] Deploy: en iyi adapter → merge (bf16) → llama.cpp Q4_0 → **GGUF ~6.5GB** (8GB VRAM). Vatandaş sadeleştirmesi = app prompt (Faz 3).
- **Çıktı:** ✅ Faz 1 + GGUF.

## Döngü özeti
```
base ölç ✅ → FT(32K)=v0 ✅ [başarısız: veri base-altı doğruluk] → teşhis ✅
   └─ GROUNDED veri imal et (gerçek madde→doğru+atıflı) = sft_v1 ~21K ✅ [32K dahil DEĞİL]
        └─ kalite ön-kontrol → Modal A100 FT(v1) → groundedness skorkartı → [v2…]
             └─ rakipleri geç (groundedness) → güvenilirlik (hakem-uyumu) → merge → Q4_0 GGUF → Faz 1 bitti
                (sadeleştirme = app-layer prompt, modele gömülmez; avukat-κ descope)
```
