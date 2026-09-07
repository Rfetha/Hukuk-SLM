# TODO — bugün koşulabilir olanlar

> Her satır bir [`ROADMAP.md`](ROADMAP.md) adımına bağlıdır. Bir satırın burada olması için
> **bugün koşulabilir** olması gerekir: bekleyen bir karara ya da bitmemiş bir işe bağlıysa
> buraya değil, ROADMAP'e yazılır.
> ⛔ Kutucuk yalnız `verify:` çıktısı **gerçekten alındıktan sonra** işaretlenir.

## Şimdi — Faz 4, LİNEER SIRA → 🏷️ `v1.0` RELEASE

- [ ] **1 · `KUNYE` taşınabilirlik** — `KUNYE.json` mutlak yol + `mtime` damgalıyor,
      `retriever.py`:143-152 doğruluyor ⇒ `git clone` sonrası **her makinede** `SystemExit`.
      Yol repo-göreli, `mtime` → içerik hash · **$0** → [ROADMAP · Faz 4](ROADMAP.md)
- [ ] **2 · TUI gözle doğrulama** — `python -m hakhukuk.tui`, üç soru, gözle gör ·
      **$0** (GPU) → [ROADMAP · Faz 4](ROADMAP.md)
- [ ] **3 · Sonnet-5 öznesi** — rakip havuzuna frontier sınıfı girer; kapıyı **etkilemez**
      (ADR-0072 m.2) · **~$0,82** *(ölçüldü)* → [ROADMAP · Faz 4](ROADMAP.md)
- [ ] **4 · Kabul testi** — ⛔⛔ donmuş TEST **tek kez** açılır, insan onayı şart;
      ADR-0069 raporlaması zorunlu · **~$0,10** → [ROADMAP · Faz 4](ROADMAP.md)
- [ ] **5 · Modeli YAYINLA** — 🚨 ağırlıklar bugün **hiçbir yerde yayında değil**;
      HF model reposu + kart + üç belgede indirme yolu · **$0** → [ROADMAP · Faz 4](ROADMAP.md)

## Sırada — `v2` *(plan henüz yazılmadı)*

- [ ] `v2` spec + planı: **`tgta_v1` üstüne GRPO + düşünce ayarı**
      → [ADR-0075](docs/adr/0075-v1-sft-kapanir-v2-sequential-rl.md) · [ROADMAP · v2](ROADMAP.md)
- [ ] ⛔ **Ön koşul:** ödül fonksiyonu + hedef bant + **durma kuralı** tur başlamadan
      ön-kayıtlanır (ADR-0050). Korunacak taban: uydurulmuş madde **0/114** ·
      aşırı-red **4/80** · kütle **0,8011**

## Ucuz ve bağımsız — herhangi bir sırada

- [ ] `recall_taban.json` yazılsın — Faz 0'ın tek *"kaynaklanmadı"* ihlali · **$0**, ~15 dk
- [ ] `models/` ~20 GB temizliği (T1) — S7 kapandı (yalnız merge GGUF yayımlanır) · **$0**
- [ ] **Korpus bütünlüğü:** `4857/Madde 111` **yineleniyor** ve iki kopyanın `mulga` alanı
      **çelişiyor** (biri `True`, biri `False`) — ölçüldü 2026-09-07 · **$0**
- [ ] `terazi` 1. soruda **aynı atfı iki kez** üretiyor; yinelenen atıf kullanıcıya iki
      uyarı gösterir · **$0**

## Bekliyor — bugün koşulamaz, sebebi yazılı

| iş | neyi bekliyor |
| :--- | :--- |
| **Görev 8** · indeks dağıtımı (HF dataset) | mevzuat kapsam planı — bugünkü 79 MB'ı paketlemek boşa iş (8,4× büyüyecek) |
| **Görev 11 Adım 2** · temiz makine kapısı | Görev 8 — indeks git'te yok, `git clone` çalışan ürün vermiyor |
| Üçüncü **hakem** ailesi · rakip kolunun ikinci hakemle puanlanması | bütçe — tahmini fatura $2,81 ([ADR-0074](docs/adr/0074-hakem-paneli-kuruldu-baglayici-hukum.md)) |
| **B1 · B4 eğitim turları** | ⛔ **atlandı, ertelenmedi** — `v1` SFT ile kapanıyor ([ADR-0075](docs/adr/0075-v1-sft-kapanir-v2-sequential-rl.md)); `B4` `v2`'de **konusuz** kalıyor |
| Sorumluluk ibaresinin nihai metni | hukukçu görüşü (**S10**) |
