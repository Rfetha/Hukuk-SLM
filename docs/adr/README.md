# Mimari/Metodoloji Karar Kayıtları (ADR)

Bu klasör, HakHukuk'ta **neden** belirli bir yol seçtiğimizi kaydeder — sadece *ne* yaptığımızı değil.
Amaç tek: **paper yazılırken** (ve 6 ay sonra kendimize) "şunu neden böyle yaptık, hangi
alternatifi neden eledik, sonuç ne oldu" sorusu kanıtla cevaplanabilsin.

## Neden ADR (FAZ1_PLAN'daki "Kararlar (sabit)" varken)?
`FAZ1_PLAN.md > Kararlar (sabit)` **mevcut durumu** özetler (canlı, sık güncellenir, üzerine yazılır).
ADR ise **dondurulmuş anlatıdır**: bir kararın o ANki bağlamı + değerlendirilen seçenekler +
gerekçe + sonuç. FAZ1_PLAN "ana metrik groundedness" der; ADR "şu üç alternatifi şu yüzden eledik,
şu riski kabul ettik" der. Paper'ın *Methodology* ve *Limitations* bölümleri ADR'lerden yazılır.

## Format (hafif)
Her ADR: `NNNN-kebab-baslik.md`. Şablon:
- **Durum:** Önerildi | Kabul edildi | Yürürlükte | Süpersed (→ NNNN) | Geri alındı
- **Bağlam** — karar anında ne biliyorduk, hangi kısıt zorladı
- **Karar** — ne yaptık
- **Değerlendirilen alternatifler** — neyi neden elemeye/seçmedik (paper için kritik kısım)
- **Sonuç** — kanıt/sayı + kabul edilen risk + açık uçlar
- **İlgili** — `[[memory-slug]]`, FAZ1_PLAN satırı, commit, ilgili ADR

Kararı değiştirirsek eskiyi SİLMEYİZ → "Süpersed" işaretler, yenisini ekleriz (iz kalsın).

## Dizin
- [0001](0001-groundedness-ana-eval-metrigi.md) — Groundedness ana eval metriği (Muhakim ikincil; insan-κ descope)
- [0002](0002-v1-grounded-veri-kalite-kapisi.md) — v1 grounded SFT verisi: eğitim-öncesi kalite kapısı + bulgular
- [0003](0003-base-model-gemma-4-12b.md) — Base model: Gemma 4 12B (Qwen3.5-4B süpersed)
- [0004](0004-egitim-altyapisi-modal-a100.md) — Eğitim altyapısı: Modal serverless A100
- [0005](0005-veri-stratejisi.md) — Veri stratejisi: lisans-temiz + EDA-doğrula + grounded sentetik üretim
- [0006](0006-akademik-hedef-sistem-paper.md) — Akademik hedef: sistem paper'ı (benchmark yan iş)
- [0007](0007-repo-lisans-private-proprietary.md) — Repo & lisans: private + proprietary
- [0008](0008-modal-egitim-baslatma-spawn.md) — Modal eğitim başlatma: fire-and-forget `spawn` (WSL-kapanması cancel dersi)
- [0009](0009-v1-filtre-dogrulama-hedefli-audit.md) — `gen_grounded.py` filtresi doğrulandı: dokunma + hedefli v1-audit (404 şüpheli)

> İlk 7 ADR **geriye dönük** yazıldı (2026-06-08) — kararlar daha önce verildi, bağlam/alternatif/
> sonuç anlatısı paper için sonradan yapısallaştırıldı. Bundan sonraki kararlar **anında** ADR'lenir
> (0008 = ilk anında-ADR örneği).
