# ADR 0002 — v1 grounded SFT verisi: eğitim-öncesi kalite kapısı + bulgular

- **Durum:** Yürürlükte (2026-06-08)

## Bağlam
v0 SFT, ~32K forum/karışık veriyle eğitildi ve **doğruluğu düşürdü** (legal_acc 0.362→0.124). Ders:
**çöp veri → çöp model**, ve veri kaynaksız olduğu için groundedness ile *puanlanamıyordu* bile.
v1 için ~21K **saf grounded** çift üretildi (`gen_sft_v1.py`, GPT-4o-mini, her çift gerçek bir
mevzuat maddesine dayalı). v0 hatasını tekrarlamamak için **eğitime para harcamadan ÖNCE** verinin
kendisinin kapıyı geçtiğini kanıtlamak gerekti (Modal A100 ~$11.5/epoch).

## Karar
**Eğitimden önce, veri-üstü groundedness kalite kapısı uygulanır** (ADR 0001'in metriği veriye):
- Köprü: `scripts/score_grounded_corpus.py` — train örneğini al → her kayıt için
  `mevzuat_maddeler.jsonl`'den `kanun_no|madde_no` ile **gerçek madde metnini** join et →
  `referans` alanına koy → `groundedness.py --mode data`. (Mevcut `score_corpus.py` `referans=cevap`
  koyuyordu → hakem cevabı kendi kaynağı sanıp faith'i sahte-yüksek gösterecekti; köprü bunu kapatır.)
- **Geçme eşiği: faithfulness ≥ 0.80** ve sistematik (sınıf-düzeyi) bozukluk yok.
- **Eval örneğini cherry-pick edip düzeltmek YASAK** — düzeltme sınıf-düzeyinde yapılır (üretim
  filtresi / skorlayıcı), yoksa metrik geçersizleşir (paper integrity).

## Değerlendirilen alternatifler
- **Köprüsüz, doğrudan Adım 5'e geç** (gen_grounded 4a'da faith=1.0 vermişti) → REDDEDİLDİ; v0
  dersinden sonra "üretmeden önce ölç" disiplini ucuz sigorta (40 örnek ~$0.01).
- **Tüm 19K'yı groundedness'ten geçirip <0.5 olanı at** → ERTELENDİ; ~$5-10, %2.5 izole hata için aşırı.

## Sonuç (ölçüm 2026-06-08, n=40, gpt-4o-mini hakem)
- **faithfulness 0.947 / hallucination 0.053 / unsupported 0.040 / cit_precision 1.00 /
  wrong_ref_rate 0.00 / cit_recall 1.00** → kapı **GEÇİLDİ**. v0 felaketinin izi yok.
- Düşük uçtaki 3 örneğin elle analizi **üç ayrı sınıf** ortaya çıkardı:
  1. **Gerçek veri hatası** (id=32, İcra İflas m.301): madde süre/yön içermezken model boşluğu
     uydurup maddeyi *ters* aktardı (CONTRADICTED). İzole (~%2.5), sistematik değil.
  2. **Bulanık aktarım** (id=2, TBK m.224): öz doğru ama "9 gün + bilirkişi" şartı "ayıbı bilmediği
     süre" diye flulaştı. Sınırda, halüsinasyon değil.
  3. **Skorlayıcı artefaktı** (id=15, CMK m.99): cevap doğru; düşük skor claim-bölme yan etkisi —
     zararsız meta-iddia ("CMK'ya tabidir") NOT_IN_SOURCE sayıldı + atıf-claim'i paydayı şişirdi.
     Veri kusuru YOK → gerçek faithfulness 0.947'nin **alt sınır** olduğunu gösterir.

## Aksiyonlar (sınıf-düzeyi, eval-leak'siz)
- **Sınıf 3 → ÇÖZÜLDÜ (2026-06-08).** `groundedness.py > EXTRACT_SYSTEM`'e prensipli kural eklendi:
  meta/atıf iddiaları ("X kanununa tabidir", "Y maddesi düzenler") olgu iddiası değil → çıkarılmaz
  (FactScore'un "atomik olgu" tanımının doğal uzantısı; eval'e uydurmak DEĞİL). Aynı 40 örnek
  yeniden skorlandı: **faithfulness 0.947 → 0.984**, hallucination 0.053 → 0.016, claims 75 → 62.
  **Doğrulama:** id=15/id=2 (artefakt) 0.5 → 1.0; id=32 (gerçek hata) **0.0 olarak kaldı** → fix
  gerçek hatayı maskelemiyor, yalnız ölçüm gürültüsünü temizliyor. Eski 0.947 bir **alt sınırdı**.
- **Sınıf 1 → AÇIK (Faz 2 üretim diline).** "Soru süre/sayı ister + madde içermez → model uydurur"
  deseni. Tek-seferlik korpus filtresi yerine `gen_grounded` prompt'una "madde bu bilgiyi
  içermiyorsa o soruyu üretme" kuralı eklenecek (kalıcı). %1.6 izole, v1 eğitimini bozmaz.

## İlgili
ADR 0001, `[[phase1-execution-state]]`, `scripts/score_grounded_corpus.py`, `scripts/groundedness.py`
