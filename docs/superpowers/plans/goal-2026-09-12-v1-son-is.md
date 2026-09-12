# GOAL — `v1-son-iş` (adım 4b)

> `/goal` olarak verilecek prompt. **Plan değil, planı işaret eder.** Sınır: <4000 krk.

---

İCRA: `docs/superpowers/plans/2026-09-12-v1-son-is.md` — 46 kutucuk, adım 5→9.
`superpowers:subagent-driven-development` ile sür. Planı ve `docs/adr/0083`'ü **oku**.

## Sıra — insan tarafından kilitli, DEĞİŞTİRME
5 master'a al+push · 6 execute · 7 push · 8 public kontrolü · 9 HF görünürlüğü.

## DUR listesi — yalnız burada dur, insana sor
① para tavanı `min(tahmin×1,5 ; $6,00)` aşıldı (6.4.4)
② kapı `DÜŞTÜ` ya da `BELİRSİZ` (6.7.5)
③ HF public yapılmadan ÖNCE (9.1)
④ `retriever.py` denklik kanıtı tutmadı (6.1.4)
Başka yerde durma. Geçen tur 115 kutucuk yalnız DUR listesinde durdu.

## Ön-kayıt — koşudan önce yazıldı, DEĞİŞTİRİLEMEZ (plan §2)
- Kapı m.1 **her hakemin kendi içinde**: `kütle ≥ 3.5 Flash − 0,020`.
- ⭐ **GÖZ-katı miras alınır.** Bağlayıcı çıpa **0,7425**, aletin ham `0,6925` DEĞİL
  (ADR-0064:46). Fark çekinme dedektörünün fazla red saymasından: `3.5 Flash` id **28**
  + **3 çekinceli cevap** = cevap sayılır. Düzeltme **hakemden bağımsız** (coverage'ı
  oynatır, A1'i değil) ⇒ Anthropic koşusu **aynı kalem listesini** miras alır, yalnız A1
  yeniden hesaplanır. Miras alınmazsa eşik `0,6725`'e düşer ve kapı **sahte geçer**.
- Çözünürlük: `n=80` ⇒ adım **1,25 p**. `|marj|<1,25 p` ⇒ **BELİRSİZ** (her iki yönde
  bağlar; kıl payı geçen kapı da `v1.0` üretmez). Sonuç `v0.4`, gerekçe *"ölçemedik"*.
- Duman koşusu **tabakalanmış** (kısa·orta·uzun) — tuzak 1.11: `n=5`'ten tahmin $0,82
  dedi, gerçek $1,1932, $1 kapısı %45 aşıldı.

## Kaynaklı sayılar
κ tam_sadık **0,534** · atıf_temiz **0,409** · eşik 0,6 (`outputs/eval/hp-hakem-paneli/KAPPA.md`)
BİZ kütle: gpt-4o-mini **0,8011** ↔ claude-sonnet-5 **0,6940** (−10,71 p); coverage **0,9375** ikisinde de
`3.5 Flash` GÖZ-katı **0,7425** → eşik **0,7225**; bugünkü marj **+5,86 p**
κ borcu tahmini **$2,81** · bakiye **$2,0410** · otomatik yükleme <3 → +10
Donmuş TEST ham kütle **0,5804** (n=40) — **DOKUNMA**, tek hakemli kalır
Ağırlık `sha256 755e15e9…` **değişmiyor**; HF depo adı `Rfetha/HakHukuk-4B-v0.3-Q4_K_M` **aynı kalır**

## Kurallar
- **Üretim yeniden koşulmaz** — aynı 80 cevap, yalnız hakem değişir (ADR-0017).
- Hakem çağrısı **bir kez**; `harness_tablo.py` aynı jsonl'den **iki kez** koşar, çıktı
  **bayt-bayt aynı** olmalı (kusur 23'ün ikinci sınaması, $0). Ayrışırsa sayı yayımlanmaz.
- Manşet **koşulsuz ARALIK**: *"%69,4-80,1 (`claude-sonnet-5` ↔ `gpt-4o-mini`)"* — geçse de
  düşse de. Dört yer: `CLAUDE.md` · `MODEL_CARD.md` · `README.md` · `README.tr.md`.
  Üç rakip kolu **tek hakemli** kalır ve öyle damgalanır (ADR-0057).
- Kapı geçerse `v1.0`, `DÜŞTÜ`/`BELİRSİZ` ise **`v0.4`** — HF **her hâlükârda açılır**
  (görünürlük açık kusurlara bağlıydı, kapıya değil).
- Gözle okuma bir kapıdır. Geçen tur süit yeşilken **dört kusur** yakalandı.
- Her bulgu **anında** `docs/record/research_log/` (#68) + ADR (**0084**). Türkçe yaz.
- `yol köprüsü`: `scripts/` değişirse `tests/conftest.py` **birlikte** değişir.

## DUR — bu turda YAPILMAZ
korpus büyütme (ADR-0083 §EK, kendi turu) · model eğitimi · üçüncü hakem ailesi ·
donmuş TEST'i ikinci hakemle puanlama · kusur 5a ve 27 (→`v2`) · `api.py`'nin `HOST`'u.

Kapanışta açık kalan **her** kusur **adıyla** devredilir, yoksa kapanış geçersizdir.
