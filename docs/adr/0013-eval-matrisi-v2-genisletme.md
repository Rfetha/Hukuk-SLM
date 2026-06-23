# ADR 0013 — CANON eval v2 genişletme (mod matrisi: distractor + E-set + register)

- **Durum:** Yürürlükte (2026-06-14)
- **Genişletir:** ADR-0011 (canon 4 eksen). Eksenleri DEĞİŞTİRMEZ; **eval modlarını** (context koşulları) deployment'a hizalar.
- Dayanak: v2 SFT hedef tanımı (`V2_PLAN §3.1`) + scope=Product A (ADR-0012) + FT-reçete /deep-research (RAFT) + Sufficient-Context (2411.06037).

## Bağlam
ADR-0011 4 ekseni (A1/A2/A3/A4) ve 3 hücreyi (CORE-KÖR / CORE-Oracle / TRAP) sabitledi. Ama v2b SFT hedefi
(`V2_PLAN §3.1`) ile mevcut eval arasında **dağılım uyumsuzluğu** ortaya çıktı:
1. **Oracle modu TEK temiz kaynak** veriyor (`gen_eval_grounded.py --with-source` → sadece gold). Ama v2b
   RAFT ile **1 gold + 4 distractor** eğitiliyor; "distractor'ı yok say" becerisi (SFT hedef #1) **ölçülmüyor**.
   Üstelik gerçek RAG çok-chunk gürültülü → mevcut Oracle **deployment'tan KOLAY/iyimser**.
2. **Abstention tek tetikli:** A3 = TRAP (yanlış kaynak). Ama deployment'ta ikinci tetik var: **hiç/yetersiz
   kaynak** (retrieval boş). Ayrı set yok.
3. **Register ölçülmüyor:** v2 hedefi uzman-register (prompt'ta), ama "uzman mı vatandaş-basit mi" sinyali yok.

**İlke (tasarımın çıkış noktası):** *eval dağılımı = deployment dağılımı + her SFT hedefi için bir mod.*
Eğitim (RAFT gold+distractor) ile eval aynı dünyada olmalı.

## Karar — 5 eval modu × eksen matrisi

| Eval modu (= deployment durumu) | Ölçer | A1 | A2 | A3 | A4 | Reg | Mevcut |
|---|---|---|---|---|---|---|---|
| **M1 Gold+distractor** (RAG-isabet, gürültülü) | grounding-under-noise | ✓ | ✓ | – | ✓ | ✓ | 🔴 YOK → kur |
| **M2 Distractor-only** (RAG-ıska) = TRAP | abstention (yanlış-kaynak) | – | – | ✓ | – | – | ✅ var |
| **M3 Boş/kaynaksız** = E-set | abstention (kaynak-eksik) | – | – | ✓ | – | – | 🔴 YOK → kur |
| **M4 Temiz gold-only** (mevcut Oracle) | iyimser tavan (REFERANS) | ✓ | ✓ | – | ✓ | – | ✅ var (manşet DEĞİL) |
| **M5 KÖR/kaynaksız** | parametrik ezber (ablasyon) | – | ✓ | – | – | – | ✅ var |

**Eksenler değişmez** (ADR-0011): A1 groundedness · A2 correctness · A3 rejection · A4 format · **A-register (YENİ)**.
Ek alt-kontrol: **verbatim-faithfulness** — alıntılanan cümle gerçekten cited chunk'ta mı (string ⊂ check).

**Manşet kayması:** v2b'nin grounding manşeti artık **M1 (distractor'lı)**, M4 değil. M4 = iyimser-tavan referansı
olarak kalır (deployment'ı temsil etmez). A3 manşeti = M2 ∪ M3.

## İki dürüst BİLİNMEYEN (şimdi yaklaşık, sonra sıkılaştır)
1. **Distractor dağılımı** retriever'a bağlı (RAG corpus = Adım 0 henüz yok). → şimdi **hard-negative yaklaşık**
   (aynı kanun, komşu madde no), `k=4`. RAG kurulunca gerçek-retriever dağılımıyla **kalibre et.**
2. **Register skorlama rubriği** yazılacak. Çapa: **Muhakim** `linguistic-coherence` boyutu + leksik/uzunluk
   sinyali. Metot tasarlanacak (LLM-judge rubrik). Eksen gerekli olduğu kesin, ölçüm metodu açık.

## Skorlayıcı/script etkisi
- `gen_eval_grounded.py`: **`--distractors N` modu ekle** (gold + N hard-negative, shuffle) → M1.
- **E-set üret** (`data/eval/empty.jsonl` veya context-boş bayrak) → M3; `score_abstention.py` yeniden kullanılır.
- **Register skorlayıcı** (`score_register.py`, YENİ) → A-register.
- `bench_scorecard.py`: 5-mod × eksen tablosu; M1 manşet, M4 referans işaretle.

## Değerlendirilen alternatifler
- **M4 (temiz Oracle) manşet tutmak** → REDDEDİLDİ (deployment'tan kolay, iyimser; v2b distractor-robustness'ı gizler).
- **Distractor'ı rastgele örneklemek** → REDDEDİLDİ (gerçek retriever hard-negative döner; rastgele eval'i kolaylaştırır).
- **Register'ı A4'e gömmek** → REDDEDİLDİ (format ≠ register; ayrı eksen, orthogonality ADR-0011 ilkesi).
- **E-set'i TRAP'e katmak** → REDDEDİLDİ (farklı tetik: yanlış-kaynak vs kaynak-yok; ayrı raporlanmalı).

## Sonuç / yapılacak (V2_PLAN §9-A ile aynı)
- A2: `gen_eval_grounded.py --distractors` (M1) · A3: E-set (M3) · A4: `score_register.py` (A-register).
- v2b eval dağılımı = v2b eğitim dağılımı (RAFT) — eşleşme zorunlu.
- Manşet = M1 (grounded-under-noise) + M2∪M3 (abstention). Kapılar ADR-0011/§6 korunur.
