## v2c icra — ADIM 6c: Modal eğitim BAŞLADI (smoke GREEN) + ADIM 2 erken sinyal (2026-07-02)
Otorite: `v2c/roadmap.md` §5 madde 6c. Kullanıcı onayı alındı ("smoke sonra tam koşu", 2026-07-02).

**Modal smoke → GREEN → tam koşu:**
- ⚠️ İlk smoke `--detach`'siz başlatıldı → ephemeral app entrypoint bitince kapandı, 0 task koştu (**kredi harcanmadı**). V2_PLAN§9 uyarısı doğrulandı: `modal run --detach` ŞART.
- Smoke (`--detach`, ap-jT66lrYqzGoNRNW0ZVx12w, run=v2c-smoke, 50 step): **veri doğru yüklendi** (train **17353**/val **963**), adapter **65.5M (0.55%)** = v2b, ~15s/step (A100-40GB), **step-10 loss=1.347** (v2b smoke 1.411 ile uyumlu), OOM/hata YOK. → config+veri VALİDE.
- **Tam koşu SPAWNED** (`--detach`, **app=ap-kKczVUwN4cMj6fodVkaLvK**, FunctionCall=fc-01KWHHWR578WWCXQJ6Q0D37PZ3, run=v2c, 1 epoch, data=/data/sft_v2c). ~4-4.5h/$15-18. Bitince adapter → `hukuk-outputs:/v2c` → `modal volume get hukuk-outputs /v2c ./outputs/v2c`. İzle: `modal app logs ap-kKczVUwN4cMj6fodVkaLvK`.

**ADIM 2 erken sinyal (C3 arka planda koşuyor) — cevaplanan-only A1 (yeni araç `scripts/rescore_answered.py`, ABSTAIN_RE ile çekinme ayır, ADR-0011, TÜM modellere tek kural):**
| Model | M1 A1 (cevaplanan) | coverage (cevaplanan/40) | ham macro (çekinme dahil) |
|---|---|---|---|
| v2b | **0.9195** (29 cevap) | **72.5%** | 0.792 |
| base (eval-mirror) | 0.886 (19 cevap) | **47.5%** | 0.483 |
- **🔑 Elmayla-elma çok daha güçlü:** v2b, base'i hem faithfulness'ta (0.92 vs 0.886) hem **coverage'da EZİYOR** (72.5% vs 47.5%): base kırpılmış-context'te **%52.5 çekiniyor** (over-refusal), v2b %27.5. Eski "0.879 vs 0.904" bu iki-boyutlu üstünlüğü gizliyordu. (⚠️ base'in yüksek çekinmesi ABSTAIN_RE-artefaktı mı → C3 bitince spot-check; script'in v2b'yi 0.9195 vermesi orijinal judge-teyitli 0.904'ten hafif yüksek çünkü ABSTAIN_RE 11 çekinme yakalıyor, judge 7 idi — kural tutarlı olduğu için kıyas geçerli.)
- **Kalan ADIM 2:** C3 bitince base/v1 tüm modlarda (M2/M2b/M3/M5) rescore + register + C4 Mecellem baseline (Tablo 1) → tam ADIM 2 yazımı.

---

