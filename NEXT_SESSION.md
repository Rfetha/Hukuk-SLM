# DEVİR NOTU — 2026-06-14 akşamı (RPD reset bekleniyor)

## TEK CÜMLE
B2 teacher veri üretimi **Tier 1 günlük 10K istek tavanına** çarptı (14.800/19.305). RPD reset'inden
sonra (gece yarısı UTC) **resume ile bitir → assemble → Modal eğitimi (C1 hazır)**.

## ŞU AN NEREDEYİZ
- **A-track ✅ BİTTİ** — base baseline ölçüldü: M1 (gold+4distractor) faithfulness **0.879**,
  M3 (empty-context) abstention **1.000**. (`outputs/eval/gnd_bench_m1_base_summary.json`)
- **B-track ⏸️ DURDU (RPD)** — `data/processed/sft_v2b/answers.jsonl` = **14.800/19.305**
  (11.781 grounded + 3.019 abstain, 0 bozuk satır). Süreç ölü.
- **C-track ✅ HAZIR** — `modal_train.py::spawn_v2b` + `train_sft.py` 3e-4 kilidi + warmup flag.

## ⚠️ NEDEN ŞİMDİ DURUP EĞİTEMEYİZ (önemli)
Seed dosyası **kanuna göre SIRALI** (shuffle değil). İlk 14.800 = rastgele örnek DEĞİL →
**İCRA VE İFLAS KANUNU (2.727 örnek, datasetin ~%14'ü) ve KAT MÜLKİYETİ KANUNU üretilende SIFIR.**
Slice oranı (80/20) korunmuş ama topik dağılım bozuk. → tam seti bitirmek ZORUNLU.

## RESET SONRASI YAPILACAKLAR (sırayla)

### 1) B2'yi resume et (RPD boşalınca)
```bash
cd ~/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && set -a && . ./.env && set +a
nohup python scripts/gen_v2b_answers.py --workers 4 > /tmp/b2_parallel.log 2>&1 &
```
- 14.800'ü atlar, kalan ~4.505'i (İİK dahil) üretir. ~1 saat.
- **RPD hâlâ doluysa** crawl/HATA görürsün (~7/dk) → biraz daha bekle.
- **Akıyorsa** ~80/dk (4 worker, Tier 1 TPM 200K güvenli). Takip:
```bash
watch -n 30 'cd ~/code/Hukuk-SLM && n=$(wc -l < data/processed/sft_v2b/answers.jsonl); echo "B2: $n/19305 | süreç: $(ps aux|grep gen_v2b|grep -v grep|wc -l) | hata: $(grep -c HATA /tmp/b2_parallel.log)"'
```

### 2) B2 bitince (süreç:0, sayı=19305) → assemble (gate elemesi)
```bash
python scripts/build_sft_v2b.py assemble --answers data/processed/sft_v2b/answers.jsonl \
  --replay data/processed/replay_tr.jsonl --replay-frac 0.03
# → train/validation/test.jsonl + assemble_report.json (gate ~%92 grounded geçer)
# NOT: replay dosyası yoksa replay ATLANIR (uyarı basar) — forgetting riski, sonra ekle.
```

### 3) Veriyi Modal'a yükle + smoke eğitim
```bash
modal volume put hukuk-data data/processed/sft_v2b /sft_v2b
modal run modal_train.py::spawn_v2b --smoke     # 50 step, ~$0.15, loss düşüyor mu
```

### 4) Loss sağlamsa TAM eğitim (fire-and-forget)
```bash
modal run modal_train.py::spawn_v2b --run-name v2b --epochs 1
# reçete §5.1 gömülü: lr=1e-4, r=16/α=32, all-linear, warmup=0.05, --no-system (veri system'i taşır)
# 3e-4 YASAK (kilit aktif). İzle: modal app logs <app-id>
```

### 5) Adapter'ı çek → D1 canon eval (base'le kıyas)
```bash
modal volume get hukuk-outputs /v2b ./outputs/v2b
# M1: python scripts/gen_eval_grounded.py --label bench_m1_v2b --adapter outputs/v2b \
#       --data data/eval/core_hard.jsonl --distractors 4 --n 40
#     python scripts/groundedness.py --details outputs/eval/bench_m1_v2b_detail.jsonl --label bench_m1_v2b --mode data
# M3: python scripts/gen_eval_grounded.py --label bench_m3_v2b --adapter outputs/v2b \
#       --data data/eval/core_hard.jsonl --empty-context --n 40
# KAPI (§6): M1 faith ≥0.879 KORU · M3 abstention =1.000 KORU · +uzman-register/format eklendi mi
```

## AÇIK İYİLEŞTİRME (opsiyonel, sonra)
- B2/pack **shuffle** etmiyor → yarıda-kesilme topik-skew yapıyor. İleride pack seed'leri shuffle'lasın
  ki herhangi bir partial state temsili kalsın. (Bu sefer %100 bitireceğimiz için kritik değil.)

## DOSYALAR
- Plan: `docs/V2_PLAN.md` (§5.1 reçete · §5.2 pipeline · §9 execution)
- Kayıt: `docs/record/research_log.md` (2026-06-14 girdileri: B1 bug · A baseline · C1 prep · RPD)
- ADR: 0011 (canon eval) · 0012 (scope) · 0013 (5-mod matris)
