# ANA SKORKART — tüm turlar × tüm eksenler (birleşik)

> **Ne:** Projedeki tüm deneysel modellerin CANON eval skorlarının **tek kanonik tablosu.** Sayılar
> `outputs/eval/*_summary.json`'dan gelir (⚠️ **gitignored** → script'ten üretilir); bu dosya onların
> git-takipli, paper-hazır konsolidasyonu. Her hücre bir summary dosyasına dayanır (aşağıda kaynak eşlemesi).
> **Güncelleme kuralı:** yeni tur judge'landığında bu tablo + ilgili `vN/sonuclar.md` birlikte güncellenir.
> **Otorite:** kapı kararları `docs/adr/` · tur detayları `docs/record/vN/sonuclar.md` · kronoloji `research_log/`.

## Protokol (tüm hücreler ortak, aksi belirtilmedikçe)
Gemma 4 12B + QLoRA · eval-mirror 900-char · seed 3407 · hakem gpt-4o-mini · A1=cevaplanan-only macro (ADR-0011) ·
n: core_hard 40 (M1/M4/M5/M2b), trap 35 (M2 + genelleme), E-set 40 (M3).
⚠️ **Mecellem** = `newmindai/Mecellem-Qwen3-4B-TR` (CPT foundation base, instruction-tuned DEĞİL) → **completion-fewshot** (2-shot, chat-template yok) ile ölçüldü; aynı set/mod/n/seed/hakem ama **birebir kıyas değil** (entry #31).

---

## TABLO 1 — Kanon 6-mod + register (yön: ↑ iyi, ↓ iyi)

| Eksen | Ne ölçer | base | v2b | v2c ❌ | **v3 ⚠️** | v3ck28 | Mecellem¹ |
|---|---|---|---|---|---|---|---|
| **M1** grounding faithfulness ↑ | distractor-altında sadakat | 0.662 | 0.737 | 0.681 | **0.881** | 0.899 | 0.713 |
| **M4** oracle grounding ↑ | temiz-kaynak tavanı | 0.978 | 0.968 | 0.974 | **1.000** | — | 0.783 |
| **M2** yanlış-kaynak red ↑ | near-miss abstention (HEDEF) | 0.704 | 0.346 | 0.407 | **0.593** | 0.519 | 1.000\* |
| **M2b** çok-kaynak miss red ↑ | RAG-ıska abstention | 1.000 | 0.969² | 0.973 | **0.529** | — | 0.919 |
| **M3** boş-bağlam red ↑ | kaynak-eksik abstention | 1.000 | 1.000 | 1.000 | **1.000** | — | 1.000 |
| **M5** kör/parametrik doğ. ↓ | ezber (ANTİ-hedef) | 0.225 | 0.175 | 0.125 | **0.075** | — | 0.350 |
| **register** uzman_frac ↑ | uzman dili (vatandaş değil) | 1.000 | 1.000 | 1.000 | **0.975** | 1.000 | 0.200 |

¹ completion-fewshot (yukarı). ² v2b M2b = n40 apples-to-apples ölçüm. \* Mecellem M2=1.0 = few-shot red-taklidi + aşırı-reddetme (M4 0.78 ile paket; patoloji, entry #31 B4).

## TABLO 2 — Genelleme dilimleri (M2-modu, held-out; base/v2b/v3)

| Dilim | Ne test eder | base | v2b | **v3** |
|---|---|---|---|---|
| **xkanun** çapraz-kanun | yapısal tuzak (kolay-red) | 0.968 | 0.387 | **0.656** |
| **ood** held-out novel soru | en zor (ilke vs kalıp) | 0.889 | 0.115 | **0.483** |

Örüntü: v3 >> batık-SFT (v2b) her yerde · v3 < base her yerde · **OOD en kırılgan** (v3'ün v4-borcu #2b).

---

## Kupa durumu (her eksende lider)
- **Grounding (M1/M4):** 🏆 **v3** (0.881 / 1.000) — hem base'i hem v2b'yi geçti.
- **M2 near-miss red:** base 0.704 > v3 0.593 (base önde ama aşırı-reddetmeyle; v3 grounding-korumalı).
- **M2b:** base 1.0 > v2b/v2c ~0.97 > **v3 0.529 (regresyon)**.
- **Anti-parametrik (M5, düşük iyi):** 🏆 **v3** (0.075) — en az ezber (RAG'e-dayanma kanıtı).
- **Register:** base/v2b/v2c/ck28 = 1.0 tavan; v3 0.975; Mecellem 0.2 (asistan değil).

## Tur özeti (karar + otorite)
| Tur | Yöntem | Karar | Otorite |
|---|---|---|---|
| v0 | forum SFT | battı (K3 ezber) | research_log #02 |
| v1 | grounded SFT | net-negatif (abstention 0.74→0.00) | #06-09 |
| **v2b** | RAFT-SFT | ✅ kabul (tüm kapı) | [[v2b/sonuclar]], #16 |
| **v2c** | near-miss düz-SFT | ❌ RED (K3 negatif) | ADR-0014, [[v2c/sonuclar]], #24 |
| **v3** | ORPO (v2b-devamı) | ⚠️ KISMİ (K3 onarıldı, M2 base-altı + M2b regresyon) | ADR-0015, [[v3/sonuclar]], #32 |
| **v4** | ORPO + negatif-aile çeşitliliği | 🟢 planlı (yönü NET) | [[v3/receteler]], `NEXT_SESSION.md` |

## v1 (tarihsel not — farklı protokol)
v1 canon-öncesi `trap` setiyle ölçüldü (bugünkü M2 değil): trap-red v1=0.000 vs base=0.741 → SFT abstention'ı yok etti (K3, #07). Yeni protokolle yeniden ölçülmedi (v1 terk edildi).

## Kaynak eşlemesi (summary dosya → hücre)
`gnd_bench_m{1,4}_{model}` → M1/M4 (`faithfulness_micro`) · `abst_bench_m{2,2b,3}_{model}` + `abst_bench_{xkanun,ood}_{model}` → red (`rejection_rate`) · `corr_bench_m5_{model}` → M5 (`correct_rate`) · `reg_[bench_]m1_{model}` → register (`expert_frac(>=0.6)`). Mecellem = `*_mecellem` (completion-fewshot). v2b M2b apples-to-apples = `abst_bench_m2b_v2b_n40`.
