# ADR 0001 — Groundedness ana eval metriği (Muhakim ikincil; insan-κ descope)

- **Durum:** Yürürlükte (2026-06-08)
- **Geriye dönük kayıt** — karar 2026-06-08'de verildi, ADR olarak 2026-06-08'de yazıldı.

## Bağlam
İlk eval çerçevesi "doğruluk **+ sadelik** = ikili kapı" idi (GPT-4o-mini hakem 1-10). İki sorun
çıktı: (1) v0 deneyinde modeli sade/kısa yapmaya çalışmak **doğruluğu düşürdü** (legal_acc
0.362→0.124), yani sadelik bir model-hedefi olarak doğrulukla çelişiyordu; (2) GPT-4o-mini'nin
serbest 1-10 doğruluk puanı gürültülüydü ve tekrar-üretilebilir değildi. Paper hedefi (sistem +
çift-eksen benchmark, `[[paper-target]]`) ölçülebilir, literatüre oturan, stil-bağımsız bir
sadakat metriği gerektiriyordu.

## Karar
**Ana eval kapısı = groundedness / kaynağa-sadakat**, `scripts/groundedness.py` ile operasyonelleştirildi:
- **FactScore** (Min+2022) iki-aşamalı claim-level faithfulness: cevabı atomik iddialara böl →
  her iddiayı kaynak maddeye karşı SUPPORTED / CONTRADICTED / NOT_IN_SOURCE etiketle. İki ayrı
  çağrı claim-count kaymasını stabilize eder.
- **ALCE** (Gao+2023) gold-bağlı atıf precision/recall + **wrong_ref_rate** (doğru kanun yanlış
  madde / bozuk ad — hukuken en tehlikeli hata).
- **Sadelik MODEL gate'i DEĞİL** → app/vatandaş-modu katmanına taşındı (prompt config, Faz 3).
  Model dolu+doğru kalır; sadeleştirme runtime'da.
- **İnsan-κ (≥2 avukat, Cohen's κ) DESCOPE** → fiziksel iş gücü yok. Yerine sıfır-emek vekil:
  **hakem-uyumu** (gpt-4o-mini ↔ gpt-4o inter-judge agreement) + `--runs N` kararlılığı.

## Değerlendirilen alternatifler
- **Muhakim'i (newmindai, ArmoRM 8B reward) ana kapı yapmak** → REDDEDİLDİ. Kısa-sade-doğru
  cevapları yanlı cezalıyor (elle doğrulandı: grounded id=8/id=6 doğru ama Muhakim ≈0). Bu körlük
  paper'ın **K3 bulgusu**nun otomatik kanıtı; o yüzden ikincil sinyal olarak *raporlanır* ama karar
  vermez.
- **GPT-4o-mini serbest 1-10 doğruluk puanı** → REDDEDİLDİ (gürültülü, kalibresiz, paper-zayıf).
- **Avukat-anotasyonlu mutlak doğruluk** → ERTELENDİ (Aşama C, gelecek iş). Kapasite yok; ayrıca
  iddiamız "kaynağa-sadakat + rakibe göre GÖRELİ üstünlük", mutlak hukuki geçerlilik değil.

## Sonuç
- gnd_gpt ölçümü: faithfulness **0.97** / hallucination **0.03** / wrong_ref **0.04**.
- Skorkart yeniden kuruldu: ANA sütun groundedness, Muhakim ikincil (`build_scorecard.py`).
- **Kabul edilen açıklar (paper'da dürüst yazılacak, kod kapatamaz):** (#2) hakem self-preference —
  gpt-4o-mini hem üretti hem yargıladı → şişme riski; büyük koşuda `--judge-model gpt-4o`/cross-family.
  (#3) insan altın-standart yok → sayılar **göreli** (sıralama), mutlak "%97 doğru" değil.

## İlgili
`[[eval-accuracy-gate]]`, `[[paper-target]]`, FAZ1_PLAN.md > Kararlar (sabit), → ADR 0002 (kapının veriye uygulanışı)
