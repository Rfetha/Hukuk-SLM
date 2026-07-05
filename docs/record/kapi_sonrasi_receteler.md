# Kapı-sonrası reçeteler — TRAIN'e DOKUNAN 4 iş (v3-eval sonrası tetiklenir)

**Durum: HENÜZ ÇALIŞTIRILMAYACAK.** Bu dosya, v3 ORPO turunun kapı-eval'i (ADIM 9)
sonucuna göre tetiklenecek 4 train-değişikliği için çalıştırılabilir reçetedir. Her biri
`data/processed/sft_v3/train.jsonl`'ı yeniden ürettiği için ancak ilgili tetik gerçekleşince
koşulur. SAFE eval-dilimleri (trap_xkanun, trap_ood) train'e dokunmaz; onlar ADIM 9'da koşar.

Ortak ön-koşul: `source ~/code/global_venv/bin/activate` · seed=3407 · `set -a; source .env; set +a`
(OPENAI_KEY için). Rebuild sonrası her zaman **yeniden ORPO train** gerekir:
```
python scripts/train_orpo.py --adapter outputs/v2b --data data/processed/sft_v3 --run-name <yeni-tur>
```
(Modal A100 — yerel 12GB'da 12B ORPO tur maliyetli; `docs/record` Modal notu.)

Mevcut taban (referans): `orpo_report.json` → abstain_pairs=1495, grounding_replay=299
(replay_frac=0.20), train=1741, hi_overlap_provisional=108.

---

## Reçete 1 — #2b: negatif-aile çeşitliliği (train-fix)

**Köken:** bizim (fix-lit değil; RGB/FaithEval "hard-negative çeşitliliği" prensibinin bizim
tuzak-ailesine uyarlaması). Paper-değil.

**Tetik:** v3 kapı-eval'inde model **bir tuzak-ailesinde çöküyorsa** — yani aynı-kanun
leksik-komşu tuzağında (canon `trap.jsonl`) abstention yüksek ama `trap_xkanun.jsonl`
(çapraz-kanun) veya `trap_ood.jsonl` (görülmemiş-kanun) abstention'ı belirgin düşükse
(ör. Δ ≥ 0.15). Bu, "v3 tek aileyi ezberledi, aile-ötesi genellemedi" demektir.

**Ne değişir (train.jsonl):** Şu an TÜM abstain-çiftlerinin `trap_text`'i aynı-kanun
max-Jaccard kardeşi (`build_sft_v3.py:pick_hard_neighbor`, eval-aynası). Bu reçete EĞİTİM
tuzak havuzuna **çapraz-kanun** (ve mümkünse temporal/çok-hop) near-miss'leri ekler →
abstain-çift dağılımı çok-aileli olur (ör. %70 aynı-kanun + %30 çapraz-kanun).

**Tam kod-değişikliği + komut:**
1. `build_sft_v3.py`'ye çapraz-kanun trap üreticisi ekle: `pick_hard_neighbor`'ın yanına
   `pick_hard_neighbor_xkanun(gold_rec, pool_recs, ...)` — `build_eval_ood.py:build_xkanun`
   mantığının TRAIN-seed (`data/processed/sft_v1/train.jsonl`) sorularına uygulanmış hali
   (TÜM havuzdan `kanun_no ≠ gold` max-Jaccard). `pack` alt-komutuna `--xkanun-frac 0.30`
   knob'u ekle → seed sorularının %30'unda trap = çapraz-kanun.
   ⚠️ TRAIN-seed sorusu kullan (test.jsonl DEĞİL) → eval sızıntısı olmasın.
2. Paketi yeniden üret + harvest + chosen + orpo:
   ```
   python scripts/build_sft_v3.py pack --xkanun-frac 0.30            # yeni packed_v3.jsonl
   python scripts/gen_v3_rejected.py --oracle --target 2500          # fabrikasyon (Modal GPU)
   python scripts/gen_v3_chosen.py                                   # abstain chosen (gpt-4o-mini)
   python scripts/build_orpo_v3.py --rejected data/processed/sft_v3/rejected.jsonl
   python scripts/train_orpo.py --adapter outputs/v2b --data data/processed/sft_v3 --run-name v3b
   ```

**Beklenen etki:** `trap_xkanun` + `trap_ood` abstention ↑ (aile-ötesi genelleme),
canon `trap` abstention korunur. Risk: çok-aileli negatif M1 grounding'i hafif düşürebilir
(replay dozu—Reçete 3—ile dengele).

**Maliyet:** gen_v3_rejected = GPU (Modal A100, ~1 tur harvest) + gen_v3_chosen gpt-4o-mini
(~2500 çift, <$2) + train_orpo bir tur (Modal). Kod-değişikliği ~40 satır.

---

## Reçete 2 — #3b: çok-kaynak / deploy-gerçekçi bağlam (RAFT train-fix)

**Köken:** RAFT (Zhang et al. 2024, retrieval-augmented FT — gold+distractor eğitimi).
fix-lit. Paper-değil-bizde ama literatür-türevi.

**Tetik:** Faz-2 RAG'a yaklaşınca VEYA v3 kapı-eval'inde M1 (gold+distractor çok-kaynak)
abstention/grounding, M2 (oracle tek-kaynak) ile kıyasla belirgin zayıfsa — yani model
tek temiz kaynakta iyi ama çok-chunk (distractor'lı, deploy-gerçekçi) bağlamda çöküyorsa.

**Ne değişir (train.jsonl):** Şu an abstain-çift prompt'u ORACLE tek-kaynak
(`build_orpo_v3.py:93` → `KAYNAK MADDE:\n{trap_text}`, `SYSTEM_PROMPT_RAG`). Bu reçete
prompt'u çok-chunk RAFT paketine çevirir (gold + N distractor, `SYSTEM_PROMPT_RAG_MULTI`,
`raft_pack.pack_context`) → eğitim bağlamı deploy (Faz-2 RAG) ile eşleşir.

**Tam kod-değişikliği + komut:**
1. `build_orpo_v3.py`: abstain-çift `src`/`user` kurgusunu (satır 93-97) `raft_pack.pack_context`
   + `format_sources_block` + `clip_sources_block(…, max_chunk_chars)` ile değiştir
   (gen_eval_grounded'ın M1 eval-aynası paketiyle BİREBİR). `--distractors 3` knob'u ekle.
   Grounding-replay zaten RAG_MULTI (satır 104-124) — değişmez.
2. ```
   python scripts/build_orpo_v3.py --rejected data/processed/sft_v3/rejected.jsonl --distractors 3
   python scripts/train_orpo.py --adapter outputs/v2b --data data/processed/sft_v3 --run-name v3-raft
   ```

**Beklenen etki:** M1 çok-kaynak abstention + grounding ↑ (train-eval bağlam eşleşmesi).
Risk: bağlam uzarsa 2048 token bütçesi zorlanır → `--max-chunk-chars 900` clip şart (mevcut).

**Maliyet:** rebuild ücretsiz (rejected/chosen zaten var) + train_orpo bir tur (Modal).
Kod-değişikliği ~25 satır.

---

## Reçete 3 — #4: grounding-replay dozu 0.20 → 0.35

**Köken:** bizim (forgetting-mitigation replay knob'u; genel CL literatürü türevi). Paper-değil.

**Tetik:** v3 eğitim/eval'inde `nll_loss` (chosen-NLL = forgetting vekili) **tırmanıyorsa** —
yani ORPO turu grounding/atıf yeteneğini unutma yönünde bozuyorsa (M1 grounding veya A4
atıf-format v2b'ye göre düşerse). Mevcut replay_frac=0.20 (299 replay / 1495 abstain).

**Ne değişir (train.jsonl):** grounding-replay (is_pref=0, SFT-replay, OR-terimi sıfırlanır)
satır sayısı ~299 → ~523 (0.35×1495). Abstain-çift sayısı sabit; interleave adımı sıklaşır.

**Tam komut (kod-değişikliği YOK — knob mevcut):**
```
python scripts/build_orpo_v3.py --rejected data/processed/sft_v3/rejected.jsonl --replay-frac 0.35
python scripts/train_orpo.py --adapter outputs/v2b --data data/processed/sft_v3 --run-name v3-r035
```

**Beklenen etki:** M1 grounding + A4 atıf-format korunur/toparlanır (unutma azalır);
abstention kazancı hafif yavaşlayabilir (replay ORPO-sinyalini seyreltir → beta ile dengele).

**Maliyet:** rebuild ücretsiz + train_orpo bir tur (Modal). Sıfır kod.

---

## Reçete 4 — ADIM 4: τ judge-kalibrasyonu (hi_overlap gürültü temizliği)

**Köken:** bizim (v3 ADIM 4 tasarımı; near-miss geçerlilik-bandı). Paper-değil.

**Tetik:** v3 kapı-eval'inde M2 (oracle yanlış-kaynak) abstention **zayıf** VE gürültülü-negatif
şüphesi varsa — yani `_hi_overlap` işaretli 108 çiftin bazılarında tuzak kardeş gerçekte
soruyu KAZARA cevaplıyor olabilir (ov_gold > τ_hi=0.35 → "hi_overlap"). Bu çiftlerde
"chosen=abstain" YANLIŞ etiket olur → modele yanlış-red öğretir, M2'yi kötüleştirir.

**Ne değişir (train.jsonl):** 108 hi_overlap-işaretli abstain-çiftinden gpt-4o-mini'nin
"tuzak soruyu gerçekten cevaplıyor" dediği (kazara-cevaplayan) alt-küme abstain havuzundan
ÇIKARILIR → train.jsonl'da yanlış-etiketli abstain-çift azalır (1495 → ~1495−k).

**Tam kod-değişikliği + komut:**
1. Yeni script `scripts/judge_hi_overlap.py`: `rejected.jsonl`'daki `judge_flag=="hi_overlap"`
   108 çifti al → her biri için gpt-4o-mini'ye `(soru, trap_text)` ver, rubrik:
   "Bu MADDE bu SORUYU tam cevaplıyor mu? (evet=kazara-cevaplar→ELE, hayır=geçerli near-miss→TUT)".
   Kararı `rejected.jsonl`'a `hi_overlap_verdict` alanı olarak yaz (ör. "answers"/"near_miss").
2. `build_orpo_v3.py`'ye `--drop-hi-overlap-answers` bayrağı ekle: abstain-çift kurarken
   (satır 82 döngüsü) `hi_overlap_verdict=="answers"` olanı `continue` ile atla.
3. ```
   python scripts/judge_hi_overlap.py                                     # 108 çift → verdict (gpt-4o-mini, <$0.10)
   python scripts/build_orpo_v3.py --rejected data/processed/sft_v3/rejected.jsonl --drop-hi-overlap-answers
   python scripts/train_orpo.py --adapter outputs/v2b --data data/processed/sft_v3 --run-name v3-tau
   ```

**Beklenen etki:** M2 oracle-yanlış-kaynak abstention ↑ (temiz negatif → doğru red sinyali);
train.jsonl'dan gürültülü-abstain çiftleri düşer. Paper-değerli: "near-miss geçerlilik-bandı
etiket kalitesini ölçtük" (K3 metodoloji).

**Maliyet:** gpt-4o-mini 108 çift (~216 kısa çağrı, <$0.10) + rebuild ücretsiz + train bir tur.
Kod: ~1 yeni script (~60 satır) + build_orpo_v3'e ~5 satır.

---

## Sıralama önerisi (birden çok tetik gelirse)
1. **Reçete 4 (τ)** önce — etiket kalitesi tabandır; kirli abstain-çift diğer ölçümleri bulanıklaştırır.
2. **Reçete 3 (replay 0.35)** — sıfır-kod, forgetting varsa hızlı düzeltir.
3. **Reçete 2 (RAFT)** — Faz-2 hazırlığı, bağlam-eşleşmesi.
4. **Reçete 1 (xkanun negatif)** — en pahalı (yeni harvest), aile-ötesi genelleme gerçekten çökerse.
