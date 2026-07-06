# DEVİR NOTU — 2026-07-06 · v3 KAPANDI (KISMİ, ADR-0015) → sıradaki = v4 kararı

> **Bu dosya = sabit eksen / canlı devir notu.** Yalnız GÜNCEL durum + sıradaki somut adım.
> Geçmiş anlatı → `docs/record/research_log/README.md` · Kararlar → `docs/adr/` · Görevler → `TODO.md`.

## 🎯 TEK CÜMLE
v3 (v2b-adaptöründen DEVAM eden ORPO turu) **K3'ü büyük ölçüde onardı ama teslim değil** —
M2 near-miss reddi base'i geçmedi + M2b'de yeni regresyon çıktı → **sıradaki iş v4 (yönü NET, reçete+onay bekliyor).**

## ✅ v3 SONUÇ (ADIM 9 tam judge — kapandı)
- **Otorite:** ADR-0015 (`docs/adr/0015-v3-orpo-kapi-karari-kismi-v4-yonu-net.md`) + research_log **entry #32**
  (`2026-07-06-v3-eval-sonuc-kapi-karari.md`). Judge: gpt-4o-mini, 14 koşu, 0 hata, ~$0.08.
- **Skorkart (v3-final = 2 epoch):**

  | Eksen | base | v2b | v2c ❌ | **v3** | verdikt |
  |---|---|---|---|---|---|
  | M1 grounding faithfulness | 0.662 | 0.737 | 0.681 | **0.881** | ✅ arttı (base+v2b'yi geçti) |
  | M4 oracle grounding | 0.978 | 0.968 | 0.974 | **1.000** | ✅ tavan |
  | **M2 yanlış-kaynak red** (hedef) | 0.704 | 0.346 | 0.407 | **0.593** | ❌ base-altı (v2c +0.19) |
  | **M2b RAG-multi miss** | 1.0 | 0.96 | 0.973 | **0.529** | ❌ REGRESYON |
  | M3 boş-bağlam | 1.0 | 1.0 | 1.0 | **1.000** | ✅ tavan |
  | M5 anti-parametrik (düşük=iyi) | 0.225 | 0.175 | 0.125 | **0.075** | ✅ base-altı |
  | Register uzman_frac | 1.0 | 1.0 | 1.0 | **0.975** | ✅ korundu |

  Genelleme (judge): xkanun base .968 / v2b .387 / **v3 .656** · ood base .889 / v2b .115 / **v3 .483** (OOD en kırılgan).
- **🔬 M2b regresyon kökü (paper-değerli):** ORPO muhakemeli-red şablonu "en ilgili kaynağı SEÇ" refleksi öğretti →
  M2'de doğru (tek yanlış kaynak), M2b'de yanlış (çok distractor, doğrusu yok → "hiçbiri değil→reddet" diyemiyor,
  en yakını seçip uyduruyor: *"İlgili kaynak KAYNAK X'tür çünkü..."*). **Abstention tek beceri değil AİLE.**

## ➡️ SIRADAKİ = v4 (yönü NET; reçete + PARA-KAPISI + onay ayrı)
- **Birincil:** ORPO rejected setine **multi-distractor-no-gold (#2b, M2b-tipi)** + **OOD held-out** hard-negatifleri ekle
  → "cevap hiçbirinde yok→reddet" becerisini de eğit. Motor = OOD-odaklı hard-negative mining.
- **İkincil:** M2'yi base-üstüne itmek için near-miss negatif yoğunluğu/kalitesi (veri-kompozisyon).
- **⚠️ v2b-SFT ile "düzeltme" YASAK** (K3 tuzağı — abstention hep preference'ın işi).
- **Yöntem sabit:** yine ORPO (ref-free, 12GB-uyumlu). base-joint-ORPO yalnız v2b-continuation tavanı kanıtlanırsa alternatif.
- **Reçete taslağı:** `docs/record/v3/receteler.md` (§Reçete 1-4 + §v4 MİMARİ NOTLARI). v4 açılınca ADIM 4 τ temiz-etiket de burada.

## 🚦 STANDING KURALLAR (her oturum)
- **Para-kapıları (onaysız KOŞMA):** Modal eğitim · GPT-judge (gpt-4o-mini scoring: `groundedness.py`/`score_abstention.py`/`score_correctness.py`).
- **OPENAI_API_KEY** `.env`'de — **asla echo etme.** venv: `source ~/code/global_venv/bin/activate` (aynı komut içinde).
- **v2b/v2c/v3 ağırlıklarına dokunma** (negatif/referans kanıt). `data/` + `outputs/eval` gitignored → script'ten üret.
- Eğitim = Modal A100 (`modal run --detach`) · eval generation = lokal RTX 5070.

## 📁 v3 ARTEFAKTLARI (güvende)
- Adapter: `outputs/v3/adapter_model.safetensors` (final/2ep) + `checkpoint-28/` (1ep) — Modal volume'de de var.
- Eval: `outputs/eval/{gnd,abst,corr,reg}_bench_*_v3*_summary.json` + per-item `abst_bench_m2b_v3.jsonl` (M2b teşhis).
- Kod: `scripts/{gen_v3_rejected,gen_v3_chosen,build_orpo_v3,train_orpo}.py` · `gen_eval_grounded.py` (eval) · judge script'leri.

## v3 turu belgeleri
- **Sonuç otoritesi:** ADR-0015 + research_log #32. · Tur özeti: `docs/record/v3/README.md`.
- Execution kaydı (tarihsel): `docs/record/v3/recipe.md` (8-düğüm tasarım) · Eğitim: entry #30. · Konumlama: entry #31.
- Önceki turlar: `docs/record/v2b/` (kabul) · `docs/record/v2c/` (RED, ADR-0014).
