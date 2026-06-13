# ADR 0009 — `gen_grounded.py` filtresi doğrulandı: filtreye dokunma + hedefli v1-audit

- **Durum:** Yürürlükte (2026-06-13)
- **İlgili:** [[ADR-0002]] (v1 kalite kapısı), `scripts/gen_grounded.py`, `outputs/eval/v1_suspect_sources.json`

## Bağlam
Bir dış agent v2 analiz raporu sundu. Amiral-gemisi "yeni bulgu": `usable()` filtresi gevşek,
değişiklik/STUB kontrolünü maddenin yalnızca ilk 200 karakterine (`head = low[:200]`) yapıyor,
bu yüzden **%3 (84 madde) gövdesinde değişiklik dili kaçıyor**; "tek satır fix = STUB_MARKERS'ı
head yerine tüm gövdeye yay" önerildi. Rapor bunu "filtreyi fiilen çalıştırdım, gerçek ölçüm" diye
sundu.

## Bulgu — hipotez vs gerçek (gerçek `usable()` import edilip 40K ham veride koşuldu)

| Raporun iddiası | Gerçek ölçüm | Hüküm |
|---|---|---|
| %3 (84 md) gövdede değişiklik dili kaçıyor | **%0** | ❌ Fabrikasyon |
| STUB_MARKERS head-only; fix = gövdeye yay | Zaten `any(m in low ...)` = **tüm gövde**; fix no-op | ❌ Yanlış |
| (ima) mülga gövde kaçağı | **%2.4 (65 md)** head-only'den kaçıyor | ✅ Gerçek, ama elememeli |
| %12.4 kısa madde geçiyor | **%12.4 (341 md)** | ✅ Tek sağlam bulgu |

`gen_grounded.py:121,124` zaten `STUB_MARKERS` ve `AMEND_RE`'yi tüm gövdede (`low`) arıyor.
Yalnız `mülga`/`yürürlükten kaldırıl` ve `startswith("(")` kontrolleri head-only — ve bu **kasıtlı doğru**:
gövde ortasındaki "mülga" çoğunlukla başka maddeye atıf veya kısmen-mülga (örn. **HMK m.38**: 6-7.
fıkraları mülga ama 1-5. fıkralar geçerli canlı hüküm). Bunları elemek **yanlış-pozitif** = iyi kaynağı çöpe atmak.

## Karar
1. **Filtreye DOKUNULMAZ.** Raporun "fix"i no-op + yanlış-pozitif riski taşıyor. `head`-only mülga
   kontrolü kasıtlı tasarım; korunur.
2. **Ders (süreç):** Bir agent "kodu çalıştırıp ölçtüm" dese bile sayıyı gerçek modülü import edip
   doğrula. Raporun "fiili ölçümü" kendi hatalı re-implementasyonuydu.
3. **Hedefli v1-audit** kurulur (kör tarama değil): 404 şüpheli kaynak (`short` 341 + `mulga_body` 65)
   → `outputs/eval/v1_suspect_sources.json`. v1 verisi indiğinde **yalnız bu maddelerden üretilen
   Q&A çiftlerinin atıfı tutmuş mu, yoksa ince/mülga maddeye uydurmuş mu** kontrol edilir.

## Raporun korunan değerli kısımları (ayrı izlenir)
- **MCQ ekseni** (kaynaksız parametrik bilgi ölçümü; groundedness'i değiştirmez, ekler) → TODO/ileride ADR.
- v0 post-mortem somut sayıları (154x "1982" cevabı, atıf %13.6) → [[ADR-0002]] doğrulayıcı dipnot.
- Rakip baseline (bizim terazide) + cross-judge (gpt-4o) → zaten NEXT_SESSION Adım 6.

## Sonuç
Filtre sağlam; v1 kaynak havuzu çoğunlukla temiz. Açık iş = v1 verisi inince 404 şüpheliyi hedefli denetle.
