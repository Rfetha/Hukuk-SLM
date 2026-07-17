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
- [0010](0010-reframe-birincil-register-uzman.md) — Reframe: birincil register = uzman/hukukçu; sade dil app-layer'a taşındı (retroaktif yazıldı 2026-07-01, karar 2026-06-13)
- [0011](0011-eval-metodoloji-canon.md) — CANON eval metodolojisi (4 eksen, mod-stratifiye, literatür-doğrulamalı)
- [0012](0012-v2-strateji-on-kayit.md) — v2 strateji ön-kayıt (scope Product A; SFT=davranış, bilgi=RAG)
- [0013](0013-eval-matrisi-v2-genisletme.md) — CANON eval v2 genişletme: 5 mod matrisi (distractor + E-set + register)
- [0014](0014-v2c-red-karari-fix-yonu-acik.md) — v2c RED kararı (M2 0.407 + M1 regresyon) + K3 negatif bulgu; fix yönü AÇIK (potansiyel durumlar P1–P6, karar ertelendi)
- [0015](0015-v3-orpo-kapi-karari-kismi-v4-yonu-net.md) — v3 ORPO kapı kararı (KISMİ: M1↑ ama M2 base-altı + M2b regresyon); v4 yönü net
- [0016](0016-dis-benchmark-kapsami-rakip-konumlama.md) — Dış-benchmark kapsamı + rakip konumlama (BigLaw/LegalBench & Muhakim = cite-only)
- **[0017](0017-tez-cercevesi-maliyet-normalize-parite.md) — ⭐ TEZ ÇERÇEVESİ: maliyet-normalize parite + base model (Gemma 4 12B QAT) SABİT (2026-07-17)**
- [0018](0018-8gb-soft-gate-maliyet-egrisi.md) — 8 GB = soft gate (sert kısıt değil); erişilebilirlik = maliyet-performans eğrisi
- [0019](0019-faz-sirasi-istisnasi-harness-teze-dahil.md) — Faz sırası istisnası: harness dilimi (retriever+doğrulayıcı+kapı) teze dahil, graph-RAG hariç
- [0020](0020-rakip-seti-tavan-referansi.md) — Rakip seti: dağıtım-sınıfı kapalı modeller (Flash/Sonnet/5-mini) + tavan referansı (ADR-0016 revize)

> **⭐ Tez çerçevesi 2026-07-17'de değişti** — otorite belge `docs/superpowers/specs/2026-07-17-tez-cercevesi-design.md`. ADR-0017 çekirdek karar; 0018-0020 onu tamamlar. Önceki ADR'ler (özellikle 0006 "benchmark yan iş", 0016 rakip listesi) bu ışıkta okunur.

> İlk 7 ADR **geriye dönük** yazıldı (2026-06-08) — kararlar daha önce verildi, bağlam/alternatif/
> sonuç anlatısı paper için sonradan yapısallaştırıldı. Bundan sonraki kararlar **anında** ADR'lenir
> (0008 = ilk anında-ADR örneği).
