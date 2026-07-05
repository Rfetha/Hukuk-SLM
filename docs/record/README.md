# docs/record/ — Araştırma Kaydı (makale-sigortası)

> **Bu klasör ne:** Projeyi repo'dan geriye-dönük yeniden-kurup **paper yazabilmek** için tutulan kayıt.
> Hiçbir bulgu/sayı/tarih/karar burada kaybolmaz. ADR'ler *kararı* tutar (`docs/adr/`); burası
> *anlatıyı + sayıları + öğrenilen dersi + tur-özetlerini* tutar. Aktif otorite = kronolojik `research_log/`.

## Ana bölümler

| Bölüm | Ne için | Link |
|---|---|---|
| **research_log/** | Kronolojik deney günlüğü — her anlamlı deney/bulgu/karar ayrı dated dosya (birebir içerik) | [`research_log/`](research_log/README.md) |
| **v2b/** | Tur özeti: hafif RAFT-SFT, ✅ tüm kapılar geçti (tek açık M2 near-miss) | [`v2b/`](v2b/README.md) |
| **v2c/** | Tur özeti: near-miss abstention denemesi, ❌ REDDEDİLDİ (K3 negatif — Grounding-Abstention paradoksu) | [`v2c/`](v2c/README.md) |
| **v3/** | Tur özeti: near-miss fix ORPO ile, 🟢 aktif (harvest+paketleme koştu, Modal smoke bekliyor) | [`v3/`](v3/README.md) |

## Kesişen (cross-cutting) dosyalar

| Dosya | Ne için | Link |
|---|---|---|
| Künye + çerçeve | Model/ana-metrik/eğitim-yeri + eval modları (KÖR / madde-verili-oracle) tanımları | [`research_log/00-kunye-ve-cerceve.md`](research_log/00-kunye-ve-cerceve.md) |
| Paper eşlemesi | Her bulgunun paper'ın hangi bölümüne (K1 ablasyon / K3 negatif / methodology) yaradığı | [`research_log/99-paper-esleme.md`](research_log/99-paper-esleme.md) |

## Nereden okumaya başlamalı
1. Güncel durum + sıradaki iş → `../../NEXT_SESSION.md` + `../../TODO.md`.
2. Ne oldu (kronoloji) → [`research_log/README.md`](research_log/README.md).
3. Belirli bir tur → ilgili tur klasörü README'si (yukarıdaki tablo).
4. Kararların gerekçesi → `../adr/`.
