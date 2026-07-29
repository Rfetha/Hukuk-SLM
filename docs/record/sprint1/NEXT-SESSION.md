# NEXT SESSION — Sprint 1 kapandı (2026-07-29)

> **Bu belge ne:** oturumlar arası devir notu. **Sprint 1'in devri bitti.**
> ⚠️ Önceki içerik (CP6 hazırlığı) **tamamen değiştirildi** — CP6 koşuldu ve bitti.

---

## Durum

| | durum |
| :--- | :--- |
| Sprint 1 (CP0-CP7) | ✅ **KAPANDI** — [`sprint1.md`](../../../sprint1.md) arşiv, yürütme için kullanılmaz |
| Sprint 2 | 🔵 **planlanmadı** — yürütme belgesi henüz yok |

## Sprint 1 ne bıraktı

| ne | nerede |
| :--- | :--- |
| ⭐ **Üçlü sonuç tablosu** (base ↔ Gemini 3.1 FL ↔ `τ_g`) | [`sprint1-sonuc-tablosu.md`](sprint1-sonuc-tablosu.md) |
| CP5-CP6 kaydı | [`research_log` #41](../research_log/2026-07-29-cp6-tau-grounding-olcumu.md) |
| ⭐ Yürütme tuzakları (her koşudan önce oku) | [`yurutme-tuzaklari.md`](../yurutme-tuzaklari.md) |
| Artefakt | `outputs/tg/` (adaptör) · `models/merged/tg/` (bf16) · `models/gguf/tg-q4_k_m.gguf` |
| Yeni araç | `scripts/merge_lora.py` · `scripts/compare_runs.py` |

## 🔴 Sprint 2'nin ÖNÜNDEKİ karar

[`docs/open_questions.md`](../../open_questions.md) **§13.8** — RAFT meta-iddia artefaktı.
Kafesin 8 eval koşusunun hepsini etkiler: `τ_g` içeren her hücre sistematik ceza alır, `τ_a`
tekili almaz → **ADR-0037'nin Kapı 5 kıyası taraflanır.** Üç seçenek belgede; **`τ_abstention`
eğitilmeden önce** ve **veriye bakmadan** verilmeli (TASARIM §7 pre-registration).

## Sprint 2'ye devreden iş — *plan değil, girdi*

Sıra ve kapılar **Sprint 2 planı yazılırken** belirlenecek.

| iş | not |
| :--- | :--- |
| `rejected` yeniden hasadı | Bağımlılığı olan "çalışan çıkarım hattı" **CP6'da doğdu**. Yerel, $0. Mevcut `rejected` 12B'nin fabrikasyonları — olduğu gibi kullanmak yeni modele başka bir modelin hatalarını öğretir (TASARIM §4.1) |
| `τ_abstention` (ORPO) | 1.741 çift · **82 adım** (3 epoch) · lr 1e-5 · etkin batch 64 · **`--fresh-adapter` zorunlu** · rejim TASARIM §4.1.1 ile eşleşmeli |
| Tabanlar (karışık · ardışık SFT) | Kapı 5 ikisini de geçmeyi şart koşuyor (ADR-0037) |
| Rakip aileleri için red-regex kalibrasyonu | Para gerektirmez; kapanınca Gemini'nin regex satırları raporlanabilir |
| Sağlayıcı pinlemesi + rakip üretim maliyeti | Sprint 5 ön koşulu |

## Bütçe

Modal cap **$42.50** · Sprint 1 fiili ~**$5.5** (CP4 $0.15 + CP5 ~$5.5) · hakem toplam ~$0.30.
`τ_abstention` 82 adım — `τ_g`'nin 1.083 adımının yanında ihmal edilebilir.
