# GOAL — `v1-son-iş` (adım 4b)

> `/goal` olarak verilecek prompt. **Plan değil, planı işaret eder.** Sınır: <4000 krk.
> **v2 — 2026-09-12:** para tavanı $6→$8; 6.3b · 6.3c · 6.6b eklendi; 5 ve 6.1 kapandı.

---

İCRA: `docs/superpowers/plans/2026-09-12-v1-son-is.md` — **60 kutucuk, 8'i kapalı**.
`superpowers:subagent-driven-development` ile sür. Planı ve `.superpowers/sdd/progress.md`
defterini **oku**. Adım 5 ve 6.1 BİTTİ — yeniden koşma. Sıradaki **6.2**.

## Sıra — insan kilitli, DEĞİŞTİRME
6.2 G8 · 6.3 kusur29+konteyner · 6.3b ürün yolu kütlesi · 6.3c S17 · 6.4 duman+para ·
6.5 3.5Flash 2.hakem · 6.6 kusur23 · 6.6b öz-tercih · 6.7 kapı · 6.8 ADR-0084+#68 ·
7 push · 8 public · 9 HF görünürlüğü.

## DUR — yalnız burada dur, insana sor
① para tavanı aşıldı: `min(tahmin×1,5 ; $8,00)` ya da kalemin alt-tavanı
② kapı `DÜŞTÜ` ya da `BELİRSİZ` (6.7.5)
③ HF public yapılmadan ÖNCE (9.1)
④ denklik/kimlik kanıtı tutmadı
Başka yerde durma.

## Ön-kayıt — DEĞİŞTİRİLEMEZ (plan §2)
- Kapı m.1 **her hakemin kendi içinde**: `kütle ≥ 3.5 Flash − 0,020`.
- ⭐ **GÖZ-katı miras alınır.** Bağlayıcı çıpa **0,7425**, aletin ham `0,6925` DEĞİL
  (ADR-0064:46). `3.5 Flash` id **28** + **3 çekinceli cevap** = cevap sayılır. Düzeltme
  **hakemden bağımsız** (coverage'ı oynatır, A1'i değil) ⇒ Anthropic koşusu aynı kalem
  listesini miras alır. Alınmazsa eşik `0,6725`'e düşer, kapı **sahte geçer**.
- Çözünürlük: `n=80` ⇒ adım **1,25 p**. `|marj|<1,25 p` ⇒ **BELİRSİZ**, her iki yönde bağlar.
  Sonuç `v0.4`, gerekçe *"ölçemedik"*.
- **6.3b ürün yolu sayısı kapıya GİRMEZ** (çıpa ölçüm hattında ölçüldü ⇒ eşit sınav değil);
  kartta ikinci, etiketli satır.
- **6.3c eğrisi artefaktı DEĞİŞTİRMEZ** (ADR-0071 tek GGUF yürürlükte).
- **6.6b yalnız Anthropic ailesi**; Google hücresi aile dışlamasıyla ölçülemez, açık kalır.
  Sonucu hiçbir hükme girmez, rakip tablosuna yazılmaz.
- Duman koşusu **tabakalanmış** (kısa·orta·uzun) — tuzak 1.11: `n=5` tahmini %45 saptı.

## Kaynaklı sayılar
κ 0,534 / 0,409 · eşik 0,6 (`outputs/eval/hp-hakem-paneli/KAPPA.md`)
BİZ kütle: gpt-4o-mini **0,8011** ↔ sonnet-5 **0,6940**; coverage **0,9375** ikisinde de
`3.5 Flash` GÖZ-katı **0,7425** → eşik **0,7225**; bugünkü marj **+5,86 p**
Bütçe: 6.3b $0,0417(≤$0,10) · 6.3c $0,0834(≤$0,20) · 6.5 $2,81 · 6.6b $1,86(≤$3,00)
⇒ toplam **$4,795**, üst sınır **$8,00**. Bakiye $2,04, oto-yükleme <3 → +10
Donmuş TEST **0,5804** (n=40) — **DOKUNMA**, tek hakemli kalır
Ağırlık `sha256 755e15e9…` değişmiyor; depo adı `HakHukuk-4B-v0.3-Q4_K_M` **aynı kalır**
İndeks deposu: `Rfetha/HakHukuk-mevzuat-bge-m3-s2` (dataset, **baştan public**)

## Kurallar
- **Üretim yeniden koşulmaz** — aynı cevaplar, yalnız hakem (ADR-0017). İstisna: 6.3b · 6.3c
  yeni üretim ister (yerel GPU, $0).
- Hakem çağrısı **bir kez**; `harness_tablo.py` aynı jsonl'den **iki kez**, çıktı bayt-bayt
  aynı olmalı (kusur 23, $0). Ayrışırsa sayı yayımlanmaz.
- Manşet **koşulsuz ARALIK**: *"%69,4-80,1 (sonnet-5 ↔ gpt-4o-mini)"* — geçse de düşse de.
  Dört yer: `CLAUDE.md` · `MODEL_CARD.md` · `README.md` · `README.tr.md`. Üç rakip kolu tek
  hakemli kalır ve öyle damgalanır (ADR-0057).
- Kapı geçerse `v1.0`, `DÜŞTÜ`/`BELİRSİZ` ise `v0.4` — HF **her hâlükârda açılır**.
- Kusur 25: tüm paydalar `DOGRULANDI`; yalnız Sonnet-5 hücresi yeniden ifade edilir.
- Künye alanları **koşan süreçten** okunur (`/proc/<pid>/cmdline`) — sabit dize kanıt değil.
- Gözle okuma bir kapıdır. Geçen tur süit yeşilken **dört kusur** yakalandı.
- Her bulgu anında `research_log` (#68) + ADR (**0084**). Türkçe yaz.
- `scripts/` değişirse `tests/conftest.py` **birlikte** değişir.

## YAPILMAZ
korpus büyütme (kendi turu) · model eğitimi · üçüncü hakem ailesi · donmuş TESTi 2. hakemle
puanlama · kusur 5a/27 (→v2) · `api.py` `HOST` · indeksi yeniden kurmak.
Ölçülemeyen üç kalem (gerekçesi planda): uzun madde chunk'laması · eğitimin aşırı-red etkisi ·
indeksin `model_revision`'ı.

Kapanışta açık kalan **her** kusur **adıyla** devredilir, yoksa kapanış geçersizdir.
