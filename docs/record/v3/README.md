# v3 turu — near-miss abstention fix, ORPO (✅ KAPANDI = KISMİ)

> **Tek cümle:** v2c RED'inden sonra near-miss (topik-komşu yanlış-kaynak) abstention'ı **tercih-optimizasyonu
> (ORPO, v2b-adaptöründen DEVAM)** ile düzeltme turu. **Sonuç KISMİ / teslim değil:** K3'ü büyük ölçüde onardı
> (M2 0.35→0.59, M1 0.74→**0.88**) ama base-M2'yi geçmedi (0.593<0.704) + **M2b regresyon** (0.96→0.53,
> forced-source-selection bias). → v4 (negatif-aile çeşitliliği) gerekli.

## Sonuç otoritesi
- **ADR-0015** (`../../adr/0015-v3-orpo-kapi-karari-kismi-v4-yonu-net.md`) — kapı kararı + v4 yönü NET.
- research_log **entry #32** (`../research_log/2026-07-06-v3-eval-sonuc-kapi-karari.md`) — tam judge skorkartı + M2b teşhisi + proxy→judge dersi.

## Dosyalar
- [`sonuclar.md`](sonuclar.md) — **v3 tam skorkart + kapı gerekçesi + M2b teşhis + proxy→judge dersi** (v2b/v2c paraleli).
- [`recipe.md`](recipe.md) — v3'ün 8-düğüm KARAR/execution belgesi (✅ tarihsel; ADR-0015 bundan yazıldı).
- [`receteler.md`](receteler.md) — **v4 girdileri:** train'e-DOKUNAN 4 iş (#2b negatif-aile [v3 M2b teşhisiyle TETİKLENDİ] · #3b çok-kaynak · #4 replay · ADIM 4 τ-judge) + §v4 MİMARİ NOTLARI.

## Tur kronolojisi (research_log)
2026-07-03→07-06 girdileri: #25 (near-miss trap) · #26-27 (rejected harvest + ORPO hazır) · #28-29 (genelleme/OOD dilimleri) · #30 (eğitim bitti) · #31 (Mecellem konumlama) · **#32 (SONUÇ + kapı)**.

> Önceki tur: [`../v2c/`](../v2c/) (RED, ADR-0014) · Aktif iş: `NEXT_SESSION.md` (v4).
