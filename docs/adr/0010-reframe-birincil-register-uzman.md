# ADR 0010 — Reframe: birincil register = uzman/hukukçu (sade dil app-layer'a taşındı)

- **Durum:** Yürürlükte (karar 2026-06-13)
- **Geriye dönük kayıt:** Bu ADR **2026-07-01'de yazıldı**; karar **2026-06-13'te** alınmıştı (bkz. `docs/record/research_log/README.md` 2026-06-13 girdileri). Karar birçok belgede (VISION.md §1, V2_PLAN.md, ADR-0012 Sonuç, research_log) "pending ADR-0010" olarak referanslanıyordu ama ADR'si yazılmamıştı; bu dosya o boşluğu doldurur.

## Bağlam
Projenin ilk çerçevesi (VISION.md, TEKNIK_PLAN.md, FAZ1_PLAN.md, VERI_PLANI.md) birincil kitleyi
**vatandaş** olarak alıyordu: model çıktısının varsayılan davranışı "hukuki terim → sade Türkçe çeviri"
idi ve SFT verisi vatandaş-register'ında üretiliyordu.

İki ampirik bulgu bu çerçeveyi çürüttü:
1. **v0 (forum verisi) çöküşü** — sade/kısa cevaba doğru eğitim doğruluğu düşürdü (legal_acc 0.362→0.124).
   Plainness'i ağırlığa gömmek correctness'i bozuyor (research_log 2026-06-08; ADR-0001 K3 gerekçesi).
2. **v1 (grounded, vatandaş-register) eval'i (2026-06-13)** — madde-verili/oracle modda v1 ≈ base
   (faithfulness'ta base'i GEÇMEDİ), tek kazanım kozmetik atıf formatıydı; buna karşılık abstention
   çöktü (TRAP Rej* 0.741→0.000). "v1 kısa/sade" bir satış noktası değil, correctness pahasına gelen
   bir takas olarak görüldü.

Aynı gün (2026-06-13) yapılan reframe: **doğruluk/güncellik modelin beyninde değil RAG/kütüphanede**
(VISION.md tasarım prensibi) → o zaman modelin işi "sade konuşmak" değil, "kaynağı disiplinli okuyan +
kalibre + çekinen uzman okuyucu" olmak. Sade dil, doğru cevabın *sunum katmanıdır*, eğitim hedefi değil.

## Karar
- **Birincil kitle = UZMAN (avukat/hukukçu).** Model çıktısı hassas, atıflı, uzman-register'ında olur.
- **Vatandaş sadeleştirmesi = app-layer prompt modu** (inference/uygulama katmanında prompt config ile
  "vatandaş modu"). **Model eğitim hedefi DEĞİL** — SFT loss'u register'ı optimize etmez (hiçbir FT
  yöntemi register'ı correctness kaybı olmadan kontrol edemiyor; v1'in "kısa-kesin koşul-atlama" hatası).
  Uzman register **prompt'ta** kalır; eğitim cevapları uzman tonunda yazılır ama optimize edilen sinyal
  correctness/grounding/abstention'dır (bkz. V2_PLAN §3.1).
- **Correctness/grounding RAG'den gelir** (Product A, ADR-0012). SFT bilgi gömmez; davranış (grounding +
  abstention + format) öğretir.

## Değerlendirilen alternatifler
- **Vatandaş-register'ı model hedefi tutmak** → REDDEDİLDİ. v0/v1 kanıtı: plainness'i ağırlığa gömmek
  correctness'i bozuyor; register-loss over-refusal/koşul-atlama getiriyor.
- **İki ayrı model (uzman + vatandaş)** → REDDEDİLDİ. Tek doğru+grounded model + prompt-zamanı
  sadeleştirme daha ucuz ve bakımı kolay (PAPER_TARGET §1 "tek modelden iki kitle").
- **Sade dili RAG sonrası ayrı bir sadeleştirici modele bırakmak** → ERTELENDİ (app-layer, Faz 3).

## Sonuçlar
- VISION.md §1 "Kitle: Uzman + Vatandaş" satırı bu ADR ile resmileşti (⚠️ REVİZE notu → Yürürlükte).
- Eski "default sade dil / terim→sade çeviri" ifadeleri (TEKNIK_PLAN.md, FAZ1_PLAN.md, VERI_PLANI.md,
  FINE_TUNING.md) **süpersed** — ilgili belgelere SÜPERSED notu düşüldü (2026-07-01 doc-denetimi).
- v2b SFT hedefi (V2_PLAN §3.1): grounding + abstention-koru + atıf-format + correctness-koru; register
  bilinçli olarak loss dışında.
- **Kabul edilen açık:** register hâlâ **değerlendirilmeli** (uzman mı vatandaş-basit mi) — bir eval
  ekseni gerekiyor (A-register, ADR-0013). Ölçüm metodu (LLM-judge rubriği) açık.

## İlgili
`VISION.md §1`, `docs/record/research_log/README.md` (2026-06-13), ADR-0011 (canon eval), ADR-0012 (scope Product A),
ADR-0013 (A-register ekseni), `docs/V2_PLAN.md §3.1`, `docs/PAPER_TARGET.md`.
