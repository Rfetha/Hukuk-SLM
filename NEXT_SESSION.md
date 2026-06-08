# Sonraki Oturum — Durum + Başlangıç

**Proje:** HakHukuk / Hukuk-SLM — Türkçe hukuk SLM (çift kitle: profesyonel + vatandaş).
**Base:** Gemma 4 12B (`gemma-4-12B-it-qat-q4_0-unquantized`) + QLoRA → Q4_0 GGUF deploy.
**Önce oku:** `CLAUDE.md`, `docs/FAZ1_PLAN.md` (otoriter), `docs/PAPER_TARGET.md`, hafıza `[[eval-accuracy-gate]]` + `[[paper-target]]`.

---

## NEREDE KALDIK (2026-06-08)

Faz 1 v0 eğitildi → **başarısız** (doğruluk düştü). Sebep ölçüldü, çözüm (grounded) kanıtlandı, eval felsefesi yeniden kuruldu. Eğitim YOK, kod bekliyor.

### 3 BÜYÜK KARAR (bu oturumda alındı — hepsi docs + hafızada)
1. **Ana metrik = GROUNDEDNESS / kaynağa sadakat** (LLM-judge: "uydurma kanun/çelişki var mı?"). Ürün riski = halüsinasyon. **Muhakim = ikincil sinyal**, kapı değil (kısa-sade'ye yanlı — paper K3 kanıtı).
2. **KISALIK/SADELİK MODEL ŞARTI YOK.** Model dolu+doğru kalır. **Vatandaş sadeleştirmesi = APP katmanı** (prompt config, Faz 3). v0 tuzağı: modeli sade yapmak doğruluğu düşürdü.
3. **Faz 1 hedefi = TR rakipleri geçen doğru+grounded SLM.** Rakip: `newmindai/Mecellem-Qwen3-4B-TR` (+ `Llama-3.1-8B-Instruct-*` + GPT-4o tavan).

### Ölçülen kanıtlar (Muhakim legal_acc)
| Ne | legal_acc | Not |
|---|---|---|
| base (ham Gemma) | **+0.362** | referans |
| 32K eğitim verisi (kendisi) | +0.274 | **base-altı** → v0'ı batıran sebep |
| v0 (model) | +0.124 | başarısız |
| grounded-GPT veri | (Muhakim 0.248 = yanlı) | **groundedness 10/10**, elle doğru ✅ |

## ✅ BU SESSION'DA YAPILDI (2026-06-08, ikinci tur)

**Adım 4b — Groundedness skorlayıcı KURULDU + scorecard'a entegre.**
- `scripts/groundedness.py` (YENİ): akademik format — **FactScore** iki-aşamalı (claim-extract → kaynağa-karşı-verify, count'u stabilize eder) + **ALCE** gold-bağlı atıf sınıflama (CORRECT / **WRONG_REF** = yanlış maddeye yönlendirme / UNVERIFIABLE). Metrikler: faithfulness, hallucination, wrong_ref_rate, cit_precision/recall, unsupported. Bayraklar: `--runs N`, `--judge-model` (paper: gpt-4o), `--mode data|model`.
- `scripts/build_scorecard.py` (YENİDEN): **ANA sütun = groundedness**, Muhakim ikincil'e indi. Ayrışma bayrağı Grounded↔Muhakim → "Grounded↑ Muhakim↓" K3 kanıtını otomatik üretiyor.
- Ölçüm: gnd_gpt **faithfulness 0.97 / hallucination 0.03 / wrong_ref 0.04** (gpt-4o-mini, runs=1). Metrik gerçek kusurları yakalıyor (id=17 stub-halüsinasyon, id=2/12 yanlış atıf).
- **Açık kalanlar (paper-grade, bilerek):** **#2** hakem self-preference (gpt-4o-mini üretti+yargıladı → şişme + id=17'de kısmi sızıntı; büyük koşuda `--judge-model gpt-4o`). **#3 insan-κ kalibrasyonu = Aşama C** (≥2 avukat gerekir, kod kapatamaz → sayıyı **göreli** oku, "%97 doğru" mutlak iddia HENÜZ değil).

## SIRADA NE VAR — Adım 4 kalan (grounded veri → v1)

`gen_grounded.py`, `groundedness.py`, `build_scorecard.py`, `muhakim_judge.py`, `score_corpus.py`, `dl_muhakim.py` **hazır**. Sıra:

1. **4a — Sampling'i düzelt** — `gen_grounded.py` `usable()` değişiklik-stub'larını (id=17 tipi: "...madde değiştirilmiştir" listeleri) atmıyor + `CITIZEN_LAWS` "ASKERİ CEZA"yı yakalıyor (niş). İkisini sıkılaştır → gerçek vatandaş konuları (kira/iş/icra/aile/tüketici/ceza-genel).
2. **4c — Local bake-off** — `gen_grounded.py --backend local` aynı maddelerden üret → `groundedness.py` ile GPT'yle kıyas → ucuz+iyi öğretmen kazanır.
3. **4d — ~20K'ya ölçekle** — kazanan üreticiyle, vatandaş maddelerinden, her örnekte `kaynak_madde`. **Template sızıntısını temizle** (id=18 `<...>` parantez, id=8 bozuk kanun adı). + 32K'dan **savuşturmasız/dolu** olanları filtrele (sadeleştirme YOK) → `data/processed/sft_v1/`.
4. **v1 SFT** (`from-train` benzeri) → `groundedness.py --runs 3 --judge-model gpt-4o` skorkartı → base/v0/rakiplerle kıyas.

## NEREYE BAK (mevcut çıktılar)
- `outputs/PHASE1_REPORT.md` — base vs v0 skorkart
- `outputs/eval/muhakim_*.jsonl` — Muhakim skorları (base/v0/corpus32k/gnd_gpt)
- `outputs/eval/gnd_gpt_detail.jsonl` — 25 grounded örnek (groundedness 10/10)
- `outputs/v0/` — v0 LoRA adapter

## Hızlı komutlar
```bash
# Grounded üret (sampling düzeltildikten sonra):
python scripts/gen_grounded.py --backend gpt   --n 25 --label gnd_gpt   --judge
python scripts/gen_grounded.py --backend local --n 25 --label gnd_local --judge   # GPU
# ANA: Groundedness skoru (FactScore+ALCE, claim-level):
python scripts/groundedness.py --details outputs/eval/gnd_gpt_detail.jsonl --label gnd_gpt
python scripts/groundedness.py --details outputs/eval/gnd_gpt_detail.jsonl --label gnd_gpt \
       --judge-model gpt-4o --runs 3        # paper-grade (güçlü hakem + stabil)
# İKİNCİL: Muhakim skor:
python scripts/muhakim_judge.py --details outputs/eval/gnd_gpt_detail.jsonl
# Skorkart (ANA=groundedness, Muhakim ikincil):
python scripts/build_scorecard.py --labels gnd_gpt
# Korpus skorla (veriyi eğitmeden ölç):
python scripts/score_corpus.py --data <jsonl> --label <ad> --n 40
```

## Notlar
- Eğitim/eval **yerel GPU** (12GB). Muhakim 8-bit (~8GB), SLM ile SIRALI koş (çakışma yok).
- Muhakim yerelde: `models/Muhakim/` (gitignore'lu). Yoksa `python scripts/dl_muhakim.py`.
- `.env` = `OPENAI_API_KEY` + `OPENAI_BUDGET_USD` (commit ETME).
- Bedesten/mevzuat.gov.tr **Türk IP** ister (Faz 2). OpenAI hakem TR IP istemez.
