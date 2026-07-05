## 2026-06-24 — v2b veri tamamlandı + replay + uzun-madde truncation fix

#### B2 tam set bitti, topik-skew onarıldı
- RPD reset sonrası `gen_v2b_answers.py` resume ile **19.305/19.305** cevap üretildi (grounded 15.458 / abstain 3.847, 0 boş). Önceki 14.800-kısmi koşunun atladığı **İCRA VE İFLAS KANUNU artık 2.727, KAT MÜLKİYETİ 552** (sıralı-seed topik-skew deliği kapandı). assemble: kept 18.670 / rejected 635 (630 "alıntı gold'da değil" + 5 atıf-no) → ~%3.3 deterministik ret.

#### Replay seti (forgetting sigortası, §5.1-D)
- `scripts/build_replay_tr.py` (YENİ): kaynak `AlicanKiraz0/Turkish-SFT-Dataset-v1.0` (**MIT** → license-clean), genel TR instruction (hukuk-DIŞI). EDA-doğrulandı (HARD RULE): 5.579 satır, %99.8 TR, 0 İngilizce, 0 boş, tek-tip system prompt. Süzme: hukuk-ele + token≤1500 (truncation YOK) + dedup → havuz 662 → **600 örnek** (token median 725). assemble `--replay 0.03` → train mix'e **577 replay** (grounded 13.350 / abstain 3.455 / replay 518). Gerekçe: v1 abstention çöküşüne karşı LoRA+düşük-rank+**replay** kanıtlı üçlüsünün üçüncü ayağı.

#### 🔴 Uzun-madde truncation fix (smoke yakaladı — paper-methodology)
- **Bulgu (smoke logu):** `max_seq_len=2048` ile Unsloth **1.421/17.323 (%8.2)** örneği "tüm label -100 (cevap truncate)" diye düşürdü; ayrıca toplam **2.010 (%11.6)** örnek >2048 = cevap kısmen kesik (gizli zarar: yarım-cevap öğretimi).
- **Kök neden (ölçüldü):** suçlu cevap değil. grounded ANSWER token median **196** (max 873) ama KAYNAK bloğu median 1.030, **max 12.805** — tek bir maddenin tüm metni (gold/distractor) 12K token olabiliyor. Gerçek RAG retriever tam kanunu değil **chunk** döner → tam-metin distractor zaten gerçek-dışı.
- **Fix:** `build_sft_v2b.py` → `clip_sources_block` (+`--max-chunk-chars`, default **900**≈243 tok). Her [KAYNAK i] maddesini 900 char'a kırpar; **gold chunk'ta cevabın `##begin_quote##` span'i pencere içinde KORUNUR** (yoksa context'te-olmayanı-alıntıla = halüsinasyon öğretimi). Cevap (target) ASLA kırpılmaz. Re-generate YOK (mevcut answers üzerinde post-hoc).
- **Doğrulama:** >2048 **%11.6 → %0.03** (5 örnek), gold quote context'te **13.350/13.350 (%100)**. max_seq_len=2048 kalır → maliyet sabit (~4h/$15, 994 step × ~15.75s/step ölçüldü). Örneklerin ~%100'ü korunur. *(ADR-0013 eval=train dağılımı için: aynı 900-cap raft_pack/gen_eval_grounded'e D1 ÖNCESİ aynalanmalı — açık iş.)*

#### Modal detach dersi (PC-kapanma dayanıklılığı)
- `modal run modal_train.py::spawn_v2b` (detach'siz) = local entrypoint bitince app `stopped`, **0 task** → spawn'lı fonksiyon ölüyor (gözlemlendi). **`modal run --detach`** = app bulutta `ephemeral`+task, client/PC/WSL kopsa da sürer → izle `modal app logs <app-id>`. (Önceki "PC kapayınca patladı" sorununun kökü buydu; ADR-0008 fire-and-forget ancak --detach ile geçerli.)
- **Smoke sağlık:** step10 loss=**1.411**, grad_norm 16.76, lr 9.6e-05 (warmup→1e-4), A100-40GB OOM yok, LoRA 65.5M (%0.55).

---

