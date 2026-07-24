# Faz 1 — Birleşik Skorkart

> **ANA = Groundedness** (kapı) · **İkincil = Muhakim** (bilgi) · **Sadelik = app sinyali** (model gate değil) · Ayrışma = Grounded↔Muhakim zıt.  
> ⚠️ Groundedness LLM-judge (insan-κ **kalibresiz**, Aşama C) → mutlak değil, model-vs-model **sıralama**. Muhakim = reward-model logit'i (mutlak % değil).

## ANA — Groundedness (FactScore claim-level + ALCE atıf)

| Model | Faithfulness ↑ | Hallucination ↓ | wrong_ref ↓ | cit_recall ↑ | n_claims | hakem/runs |
|---|---|---|---|---|---|---|
| gnd_gpt | 0.973 | 0.027 | 0.040 | 1.000 | 74 | gpt-4o-mini/1 |

## İkincil (bilgi) — Muhakim + Sadelik(app)

| Model | Muhakim·legal | Muhakim·statute | Sadelik (GPT 1-10, app) | Göz testi |
|---|---|---|---|---|
| gnd_gpt | +0.248 | +0.331 | — | `outputs/eval/gnd_gpt_goz_testi.md` |

- Muhakim = **ikincil** (derinlik/atıf; kısa-sade'ye yanlı → kapı değil).
- Sadelik = **app/vatandaş-modu** sinyali; model gate **değil** ([[eval-accuracy-gate]]).

## Ayrışma bayrağı (|Δz| ≥ 1.5) — Muhakim yanlılığı + insan denetimi

| Model | id | Faithfulness | Muhakim legal | Yön |
|---|---|---|---|---|
| gnd_gpt | 17 | 0.67 | +0.32 | Grounded↓ Muhakim↑ |
| gnd_gpt | 0 | 0.75 | +0.33 | Grounded↓ Muhakim↑ |
| gnd_gpt | 8 | 1.00 | -0.03 | Grounded↑ Muhakim↓ |
| gnd_gpt | 6 | 1.00 | -0.02 | Grounded↑ Muhakim↓ |
| gnd_gpt | 2 | 1.00 | +0.04 | Grounded↑ Muhakim↓ |

**5 soruda** Grounded↔Muhakim sert ayrışıyor. 'Grounded↑ Muhakim↓' = doğru ama kısa-sade cevap (Muhakim yanlılığı, K3 kanıtı).
