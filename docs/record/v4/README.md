# v4 turu — answerability-dedektörü (DTA-uyarlı ORPO) · 🟡 TASARIM (DRAFT-v2, deep-research işlendi)

> **Tek cümle:** v3'ün KISMİ sonucundan sonra (M2b regresyon + M2 base-altı + OOD zayıf), v4 =
> **tek answerability-discrimination becerisini keskinleştiren kapsamlı tur.** Amaç: her CANON kulvarında
> **lider veya berabere-tavan** (mutlak-1.0 değil), grounding dörtlüsü (M4/M1/M3/M5) **regresyonsuz.**

> **⚠️ DURUM: DRAFT-v2 (deep-research İŞLENDİ).** Bulgular [[../research_log/2026-07-06-v4-deep-research-bulgular]] (#34)
> recipe'e işlendi (DTA dört-kadran çekirdek, yapı>volüm, zemin-A kesin). **Sonraki adım = grilling → kilit.** Kilitli değil.

## Tez (neden bu tur)
9 kulvar = 1 zor beceri (answerability: "bağlam soruyu cevaplıyor mu?") + 1 dik beceri (register). Tek becerinin
iç-takası olmaz → mükemmele yakın ayrım her kulvarı birden kazandırır; frontier = kusur-artefaktı.
Tam tez: [[../research_log/2026-07-06-v4-tasarim-tezi-answerability]] (#33).

## Dosyalar
- [`recipe.md`](recipe.md) — v4 tasarım taslağı: hedef, kaldıraçlar (judge-önceliklendirmesi), zemin çatalı, kapı, açık sorular.
- [`deep_research_brief.md`](deep_research_brief.md) — **`/deep-research`'e verilecek hazır brief** (bağlam + kısıt + 6 soru + çıktı-formatı). ⏳ tetikleme kullanıcıda.
- Kaldıraç kaynakları: [[../v3/receteler]] (4 reçete + §v4 mimari notları) — v4 recipe bunları sentezler.

## Kabul edilen aksiyomlar (kilit)
1. En zor kulvarlarda ~0.90 yeterli (mutlak-1.0 hedef değil).
2. "Berabere-tavan VEYA lider" = başarı; geçilemeyende eş olmak yeter.
3. 1 numaralı kaldıraç = **veri-ölçeği + tüm present/absent ailelerini kapsama** (v3 train=1741 çok az; over-refuse yerel-optimumundan çıkış).

## Önceki turlar
[[../v2b/README]] (kabul) · [[../v2c/README]] (RED, ADR-0014) · [[../v3/README]] (KISMİ, ADR-0015) · birleşik skorlar [[../SCORECARD]].
