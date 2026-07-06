# v4 turu — answerability-dedektörü (kapsamlı ORPO) · 🟡 TASARIM (DRAFT)

> **Tek cümle:** v3'ün KISMİ sonucundan sonra (M2b regresyon + M2 base-altı + OOD zayıf), v4 =
> **tek answerability-discrimination becerisini keskinleştiren kapsamlı tur.** Amaç: her CANON kulvarında
> **lider veya berabere-tavan** (mutlak-1.0 değil), grounding dörtlüsü (M4/M1/M3/M5) **regresyonsuz.**

> **⚠️ DURUM: TASARIM DRAFT.** Bu klasör v4'ün grilling-öncesi taslağıdır. **Sonraki adım = tasarımı
> deep-research'e sokup revize etmek** (kullanıcı direktifi 2026-07-06). Kilitli değil.

## Tez (neden bu tur)
9 kulvar = 1 zor beceri (answerability: "bağlam soruyu cevaplıyor mu?") + 1 dik beceri (register). Tek becerinin
iç-takası olmaz → mükemmele yakın ayrım her kulvarı birden kazandırır; frontier = kusur-artefaktı.
Tam tez: [[../research_log/2026-07-06-v4-tasarim-tezi-answerability]] (#33).

## Dosyalar
- [`recipe.md`](recipe.md) — v4 tasarım taslağı: hedef, kaldıraçlar (judge-önceliklendirmesi), zemin çatalı, kapı, açık sorular (deep-research'e).
- Kaldıraç kaynakları: [[../v3/receteler]] (4 reçete + §v4 mimari notları) — v4 recipe bunları sentezler.

## Kabul edilen aksiyomlar (kilit)
1. En zor kulvarlarda ~0.90 yeterli (mutlak-1.0 hedef değil).
2. "Berabere-tavan VEYA lider" = başarı; geçilemeyende eş olmak yeter.
3. 1 numaralı kaldıraç = **veri-ölçeği + tüm present/absent ailelerini kapsama** (v3 train=1741 çok az; over-refuse yerel-optimumundan çıkış).

## Önceki turlar
[[../v2b/README]] (kabul) · [[../v2c/README]] (RED, ADR-0014) · [[../v3/README]] (KISMİ, ADR-0015) · birleşik skorlar [[../SCORECARD]].
