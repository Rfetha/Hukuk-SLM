# FAZ 1 — Vatandaş-dilli Hukuk SLM — Nihai Execute Planı

> **Bu doküman Faz 1 için tek otoriter checklist'tir.** `TEKNIK_PLAN.md` ile çeliştiği yerde
> **bu doküman geçerlidir** (en güncel kararlar 2026-06-08). Strateji/gerekçe `TEKNIK_PLAN.md`,
> veri `VERI_PLANI.md`, akademik hedef `PAPER_TARGET.md`.
>
> **EN GÜNCEL DURUM (2026-06-08):** v0 eğitildi → doğruluk düştü; sebep ölçüldü (veri base'den
> düşük doğrulukta) → çözüm grounded üretim (kanıtlandı). **3 büyük karar:** (1) ana metrik =
> **groundedness** (Muhakim ikincil/yanlı), (2) **kısalık/sadelik model şartı YOK** — sadeleştirme
> app-layer, (3) Faz 1 hedefi = TR rakipleri geçen doğru+grounded SLM. Detay aşağıda + `[[eval-accuracy-gate]]`.

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
- **Eval terazisi (GÜNCELLENDİ 2026-06-08, `[[eval-accuracy-gate]]`).** Model hedefi = doğru+tam+kaynağa dayalı; kısalık/sadelik model şartı DEĞİL:
  - **ANA KAPI = Groundedness/sadakat → `scripts/groundedness.py` (KURULDU 4b):** akademik
    format — **FactScore** iki-aşamalı (claim-extract → kaynağa-karşı-verify) + **ALCE** gold-bağlı
    atıf sınıflama. Metrikler: faithfulness (SUPPORTED/iddia), hallucination, **wrong_ref_rate**
    (doğru kanun yanlış madde / bozuk ad — en tehlikeli), cit_precision/recall, unsupported. Stil-bağımsız.
    Yer-gerçeği: grounded veride kaynak madde (`--mode data`); modelde Faz 2 RAG (`--mode model`).
    `--runs N` count'u stabilize eder; `--judge-model gpt-4o` paper-grade. gnd_gpt: faithfulness **0.97** / hall **0.03**.
    **Açık (paper-grade):** #2 hakem self-preference (gpt-4o-mini üretti+yargıladı → şişme; gpt-4o'ya geç) +
    **#3 insan-κ kalibrasyonu = Aşama C** (avukat gerekir, kod kapatamaz → sayı o zamana dek **göreli** okunur).
  - **İKİNCİL (bilgi) = Muhakim** (ArmoRM 8B, çok-eksen). Derinlik/kapsam/atıf sinyalleri profesyonel-kullanım için raporlanır; **KAPI DEĞİL** çünkü kısa-sade doğru cevapları yanlı cezalıyor (elle doğrulandı: grounded id=8/id=6 doğru ama Muhakim ≈0). Bu yanlılık paper K3 kanıtı.
  - **Sadelik = MODEL GATE DEĞİL.** App/vatandaş-modu eval'ine taşındı (Faz 3, prompt config). GPT-4o-mini doğruluk hakemi de gürültülüydü → ana kapı değil.
  - Skorkart: `scripts/build_scorecard.py` (KURULDU — **ANA sütun = groundedness**, Muhakim ikincil'e indi) → `outputs/PHASE1_REPORT.md`. Ayrışma bayrağı artık Grounded↔Muhakim: "Grounded↑ Muhakim↓" = Muhakim'in kısa-sade-doğruya körlüğü (K3 otomatik kanıt). Muhakim indirme: `scripts/dl_muhakim.py`. `[[eval-harness-decision]]`
- **Grounded üretici = GPT-4o-mini** (kanıt koşusu $0.006, çok ucuz). Ama **local base bake-off** ile yan yana test edilir — local yeterliyse büyük üretimde (~20K + Faz 4 niş) ona geçilir. "Güvenmeden önce doğrula." (Not: "sadeleştirme öğretmeni" kavramı düştü — sadeleştirme app-layer.)
- **Eğitim yeri = yerel** (12GB RTX 5070 Ti, batch=1 + grad-ckpt yeter). Büyük ablation → bulut (Faz 1 sonrası, opsiyonel).
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

### Adım 4 — Veriyi iyileştir (GROUNDED — asıl iş) 🔄 *SIRADAKİ*
> Karar: doğruluk forumdan gelmez, **gerçek maddeden imal edilir.** Kısalık/sadelik HEDEF DEĞİL → model dolu+doğru kalsın. `scripts/gen_grounded.py` + `scripts/score_corpus.py` hazır.
- [x] **Kanıt koşusu (25 GPT-4o-mini):** gerçek madde → soru+doğru+atıflı cevap → grounded yaklaşımı çalışıyor.
- [x] **4b — Groundedness skorlayıcı KURULDU (`scripts/groundedness.py` + `build_scorecard.py`):** FactScore iki-aşamalı + ALCE gold-bağlı atıf. faithfulness 0.97 / hall 0.03 / wrong_ref 0.04. Scorecard ANA sütun = groundedness; ayrışma bayrağı K3 kanıtını otomatik üretiyor. Detay: TODO.md + `[[eval-accuracy-gate]]`. **Açık: #2 hakem gücü (gpt-4o), #3 insan-κ = Aşama C.**
- [ ] **4a — Sampling'i düzelt:** `usable()` değişiklik-stub'larını (id=17 tipi) ve `CITIZEN_LAWS` "ASKERİ CEZA" niş kirliliğini atmıyor → sıkılaştır + gerçek vatandaş konularına daralt.
- [ ] **4c — Local bake-off:** aynı maddelerden local Gemma üret → `groundedness.py` ile GPT'yle kıyas → ucuz+iyi öğretmen kazanır.
- [ ] **4d — Ölçekle ~20K:** kazanan üreticiyle, vatandaş-konulu maddelerden, her örnekte `kaynak_madde`. **`gen_grounded.py` template sızıntısını temizle** (id=18 `<...>` parantez, id=8 bozuk kanun adı → atıf kalitesi). + 32K'dan **savuşturmasız/dolu** olanları filtrele (sadeleştirme YOK) → birleşik `sft_v1`. Skorla: `groundedness.py --runs 3 --judge-model gpt-4o`.
- **Çıktı:** `data/processed/sft_v1/` (grounded + filtrelenmiş, doğru+dolu+atıflı).

### Adım 5 — v1 SFT + iterasyon
- [ ] `sft_v1` ile FT → **v1 adapter** → groundedness skorkartı → base/v0/rakiplerle kıyas.
- [ ] İhtiyaca göre v2… (veri ekle / ayar → ölç).
- **Çıktı:** doğru+grounded model + skor eğrisi.

### Adım 6 — Bitiş + deploy artefaktı
- [ ] Bitiş kriteri: **groundedness'te rakipleri ≥ + base'e göre +** (bkz. Hedef). Rakip baseline'ları skorkarta koş.
- [ ] Deploy: en iyi adapter → merge (bf16) → llama.cpp Q4_0 → **GGUF ~6.5GB** (8GB VRAM). Vatandaş sadeleştirmesi = app prompt (Faz 3).
- **Çıktı:** ✅ Faz 1 + GGUF.

## Döngü özeti
```
base ölç ✅ → FT(32K)=v0 ✅ [başarısız: veri base-altı doğruluk] → teşhis ✅
   └─ GROUNDED veri imal et (gerçek madde→doğru+atıflı) + 32K'dan dolu olanları filtrele = sft_v1
        └─ FT(v1) → groundedness skorkartı → [v2…]
             └─ rakipleri geç (groundedness) → merge → Q4_0 GGUF → Faz 1 bitti
                (sadeleştirme = app-layer prompt, modele gömülmez)
```
