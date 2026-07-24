# docs/record/ — Araştırma Kaydı (makale-sigortası)

> **Bu klasör ne:** Projeyi repo'dan geriye-dönük yeniden-kurup **paper yazabilmek** için tutulan kayıt.
> Hiçbir bulgu/sayı/tarih/karar burada kaybolmaz. ADR'ler *kararı* tutar (`docs/adr/`); burası
> *anlatıyı + sayıları + öğrenilen dersi* tutar. Aktif otorite = kronolojik `research_log/`.

> ⚠️ **HAT DEĞİŞİMİ (2026-07-24).** Base model Gemma 4 12B'den değiştirildi. **Kronolojik kayıt
> yerinde kaldı** (`research_log/` — kesintisiz akar, pazarlıksız kural, ADR-0024); ama **base'e
> çapalı artefaktlar taşındı:** tur özetleri, SCORECARD ve ölçüm çıktıları artık
> `old-version-gemma4-12b/record/` altında. Taşındı — **silinmedi.**

## Ana bölüm (yerinde)

| Bölüm | Ne için | Link |
|---|---|---|
| **research_log/** | Kronolojik deney günlüğü — her anlamlı deney/bulgu/karar ayrı dated dosya (birebir içerik). 38 girdi; yeni hat #39'dan devam eder. | [`research_log/`](research_log/README.md) |
| Künye + çerçeve | Model/ana-metrik/eğitim-yeri + eval modları (KÖR / madde-verili-oracle) tanımları | [`research_log/00-kunye-ve-cerceve.md`](research_log/00-kunye-ve-cerceve.md) |
| Paper eşlemesi | Her bulgunun paper'ın hangi bölümüne (K1 ablasyon / K3 negatif / methodology) yaradığı | [`research_log/99-paper-esleme.md`](research_log/99-paper-esleme.md) |

## Emekli hat — `old-version-gemma4-12b/record/` (12B, tarihsel)

| Bölüm | Ne için | Link |
|---|---|---|
| **ANA SKORKART** | **Tüm turlar × tüm eksenler tek tablo** (base/v2b/v2c/v3/Mecellem + genelleme) | [`SCORECARD.md`](../../old-version-gemma4-12b/record/SCORECARD.md) |
| **v2b/** | Tur özeti: RAFT-SFT, ✅ tüm kapılar geçti (tek açık M2 near-miss) | [`v2b/`](../../old-version-gemma4-12b/record/v2b/README.md) |
| **v2c/** | Tur özeti: near-miss abstention düz-SFT, ❌ REDDEDİLDİ (K3 negatif — Grounding-Abstention paradoksu) | [`v2c/`](../../old-version-gemma4-12b/record/v2c/README.md) |
| **v3/** | Tur özeti: near-miss fix ORPO ile, ⚠️ KISMİ (K3 onarıldı, M2 base-altı + M2b regresyon; ADR-0015) | [`v3/`](../../old-version-gemma4-12b/record/v3/README.md) |
| **v4/** | Tasarım draft: answerability-dedektörü — 🔒 kilitli ama **hiç koşulmadı** | [`v4/`](../../old-version-gemma4-12b/record/v4/README.md) |

⚠️ Bu tablodaki tüm sayılar **12B + bf16/NF4 protokolüne** aittir. Yeni base'in sayılarıyla
**aynı tabloya karıştırılmaz** — protokol satırı ayrı tutulur (ADR-0025).

## Nereden okumaya başlamalı
1. **Sıfırdan geliyorsan** → `~/code/hukuk-devir/DEVIR.md` (dersler + tuzaklar) ve
   `RECETELER_12B.md` (5 turun config + veri + sonuç tablosu). 40+ girdinin damıtılmış hâli.
2. Ne oldu (kronoloji) → [`research_log/README.md`](research_log/README.md).
3. Kararların gerekçesi → [`../adr/`](../adr/README.md).
4. Veri haritası → [`../../data/README.md`](../../data/README.md).
