# ADR 0012 — v2 stratejisi + scope A/B (ÖN-KAYITLI / pre-registered, durum=BEKLEMEDE)

- **Durum:** ✅ YÜRÜRLÜKTE (2026-06-13 gece, pilot SONRASI dolduruldu). Karar kuralları pilot ÖNCESİ yazıldı (pre-registration); pilot **Product A + büyük-hedge** dallarını ateşledi. Detay plan: `docs/V2_PLAN.md`.
- **Neden ön-kayıt:** karar kuralını veriyi görmeden sabitlemek post-hoc rasyonalizasyonu önler (akademik dürüstlük, paper-sigortası). Pilot çıkınca yorumu eğip "zaten böyle diyecektim" demeyiz.

## Bağlam
v1 SFT ölçüldü (akşam benchmark): A1 madde-verili tavanda (base≈v1), A3 abstention çöktü (0.79→0.00),
A4 format v1'in tek kazanımı. Kullanıcı itirazı: "model çıplak kanunu bilmeli, yoksa neden kanunla FT
ettik?" → **scope A/B forku** açıldı:
- **Ürün A (RAG-asistanı):** doğruluk RAG'dan; model = iyi okuyucu + abstention + register. SFT'nin işi dar.
- **Ürün B (kanunu bilen model):** kanun ağırlığa gömülü; KÖR doğruluk asıl metrik; SFT bilgi katmalı.

CANON pilot (base vs v1, ADR-0011) bu forku verecek **iki teşhisle:** CORE-KÖR A2 (FT kanun öğretti mi)
+ TRAP-A2 (abstention çöküşü uydurma mı doğru-ezber mi). Karar bu sonuçlara bağlı → ön-kayıt.

## Karar KURALLARI (pilot doldurunca uygulanır)

**Eksen 1 — scope A/B (CORE-KÖR A2: v1 vs base):**
- `v1 ≈ base` (FT bilgi katmamış) → **Ürün A ağırlık.** Doğruluk RAG'dan; v2-SFT *küçük/dar* (yalnız abstention+register), kanun-bilgisi öğretmeye çalışma. ADR-0010 reframe DOĞRULANIR.
- `v1 > base anlamlı` (FT bilgi katmış) → **Ürün B yaşıyor.** v2-SFT bilgi+register; KÖR doğruluk birincil hedef olur. ADR-0010 reframe ZAYIFLAR → gözden geçir.
- `v1 < base` (FT bilgiyi BOZMUŞ) → forgetting sinyali → v2 daha hafif/seçici SFT, LoRA r düşür.

**Eksen 2 — hedge dozajı (TRAP-A2: abstain-etmeyenlerin gold'a doğruluğu):**
- `doğru-ezber baskın` (cevaplar gold'a göre DOĞRU, sadece kaynak-kontrolü yok) → bilgi sağlam → **hedge dozajı KÜÇÜK** (~%10-15, yalnız "kaynağa bak" davranışı öğret).
- `halüsinasyon baskın` (cevaplar gold'a göre YANLIŞ) → bilgi de bozuk → **hedge dozajı BÜYÜK** (~%20-25) + bilgi düzeltme.

**Sabit (pilottan bağımsız, ADR-0011 + reframe'den):**
- v2 = base'den TAZE QLoRA (v1 üstüne değil). Madde-verili modda eğit. Uzman-register.
- Başarı kapısı = **A3 rejection_rate ≥ base** + A1∧A2 base'in altına düşmesin + A4 korunsun.
- v2 değerlendirmesinden ÖNCE: register/altitude ekseni + E (kaynak-eksik) seti eklenmeli.
- Confound ayrımı (eğitim-modu vs hedge-dilimi) + hedge dozajı kesinleşmesi → **v2 ablasyonu** (v2a/v2b).

## Değerlendirilen alternatifler
- **Kararı pilot sonrası tek seferde yazmak** → daha az disiplinli; post-hoc kayma riski. Ön-kayıt tercih edildi.
- **İlaç setini (v2 verisi) şimdi hazırlamak** → REDDEDİLDİ: reçete pilota bağlı; Ürün A çıkarsa komple çöpe gidebilir. Pilot+yorum sonrası hazırlanır.

## Sonuç (pilot DOLDURDU — 2026-06-13 gece)
- [x] **CORE-KÖR A2:** base 0.225 vs v1 0.300 (CI çakışık, lenient base lehine) → **v1≈base → PRODUCT A dalı.** FT kanun gömmüyor; doğruluk RAG'dan. Üstelik v1 oracle'da bile base'den kötü (A1∧A2 0.775<0.875) → SFT net-negatif.
- [x] **TRAP-A2:** base 0.114 / v1 0.114 ama v1 cevapları %88 yanlış → **halüsinasyon baskın → hedge dozajı BÜYÜK (~%20-25)** dalı.
- [x] **Karar:** v2 = base'in gücünü koru, 3 dar iş (abstention-koru + uzman-register + format). İki aday yol: **v2a=base+prompt (önce, SFT yok)** vs **v2b=hafif-SFT**. Başarı kapısı: A3≥0.741 + A1∧A2≥0.875 + A4 korunsun.
- [x] ADR-0010 (reframe) **DOĞRULANDI** (uzman birincil + doğruluk RAG'dan); VISION.md §1 düzeltmesi sırada.
- → Detaylı execute planı: **`docs/V2_PLAN.md`**.

## İlgili
ADR-0011 (canon eval — forku veren pilot), ADR-0010 (reframe — bu fork onu test eder), `[[paper-target]]`, `docs/record/research_log/README.md` (2026-06-13 gece + pilot girdisi).
