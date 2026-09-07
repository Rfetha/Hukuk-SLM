# ROADMAP — ne, neden, hangi ölçülmüş boşluk

> **Yön belgesi.** Her adım bir **ölçülmüş boşluğa** bağlıdır; hiçbir satır *"iyi olurdu"*
> gerekçesiyle burada değil. Kutucuklu iş listesi için: [`TODO.md`](TODO.md).
> Bu turun ayrıntılı planı: [`docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md`](docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md)
> · sıra: [`docs/superpowers/00-IS-SIRASI.md`](docs/superpowers/00-IS-SIRASI.md)

## Kritik yol

```
✅ Faz 0  ölçüm zinciri onarıldı            48/48 · $1,47
✅ Faz 1  hakem paneli (İKİ aile)           $3,155 · ⛔ üçüncü aile ATLANDI (bütçe)
✅ Faz 2  Hat A — ürün paketleme            $0 · hakhukuk/ paketi, CLI + TUI
▶️ Faz 3  belge katmanı                     $0  ────────────────►  🏷️ v0.2
⏳        mevzuat kapsam + tazelik           korpus 40.496 → ~340.303 · ayrı plan
⏳ Faz 4  Hat B — model                      ~$7-15 · Modal  ────►  🏷️ v1.0 kapısı
⏳ v2     uygulama katmanı                   S9 açık
```

---

## ✅ Faz 0 — ölçüm zinciri *(kapandı 2026-09-07)*

**Ölçülmüş boşluk:** yayımlanan sayılar *"hata vermeden yanlış"* sınıfından **beş kusur**
taşıyordu. **Sonuç:** kütle %68,4 → **%80,1**, ağırlıklar hiç değişmeden.
`verify:` [ADR-0064](docs/adr/) · [#62](docs/record/research_log/2026-09-06-faz0-olcum-zinciri.md)

## ✅ Faz 1 — hakem paneli *(kapandı 2026-09-07)*

**Ölçülmüş boşluk:** her sayı `gpt-4o-mini`'nin **tek başına** hükmüydü; κ yok, öz-tercih
ölçülmemiş (ADR-0064 *"Ne KURULMAZ"* m.2).
**Sonuç:** κ **eşiğin altında** (0,534 · 0,409), kayma **tek yönlü**, manşet hakem seçimine
duyarlı (0,8011 ↔ 0,6940). Bağlayıcı hakem `gpt-4o-mini` **kaldı** — eşit sınav gereği.
**Bedel:** $3,155 gerçek fatura ($1,977 raporlanan · kapı marjı **1,6×**).
⛔ **Kapanmayan:** üçüncü aile (Google) ve rakip kolunun ikinci hakemle puanlanması —
insan kararı, bakiye $3,45.
`verify:` [ADR-0074](docs/adr/0074-hakem-paneli-kuruldu-baglayici-hukum.md) · [#64](docs/record/research_log/2026-09-07-hakem-paneli-iki-aile.md) · [`KAPPA.md`](outputs/eval/hp-hakem-paneli/KAPPA.md)

## ✅ Faz 2 — Hat A, ürün paketleme *(kapandı 2026-09-07, $0)*

**Ölçülmüş boşluk (2026-09-07):** servis katmanı **kod olarak yoktu**
(`grep -rlE "fastapi|uvicorn|flask|gradio" scripts/` → 0); modeli indiren kişi yayımlanan
sayıyı **üretemiyordu**; istem **beş dosyada** kopyalıydı ve biri **sürüklenmişti**.

| ne | neden | verify |
| :--- | :--- | :--- |
| `hakhukuk/istem.py` | istem 5 kopya, biri sürüklenmiş (S18) | `grep -rc "Sen HakHukuk'sun" scripts/` → **0** · sapma 0/10 |
| `hakhukuk/tipler.py` | `bool` üç durumu kaybediyordu | 4 durumlu enum, donmuş dataclass |
| `hakhukuk/terazi.py` | dedektör **üç kez** fazla-red saydı | 80 kalem: suskunluk **[15,37,45,66,79]** = gözle okunan kümeyle birebir |
| `hakhukuk/servis.py` | tek derin modül; boş getirmede model **çağrılmaz** | uçtan uca 3 soru: durum CEVAP/ÇEKİNCELİ, uydurma doğrulama **0** |
| `hakhukuk/cli.py` · `tui.py` | ürün yüzü; ibare **tek kaynakta** | 140 test yeşil |
| yürürlük süzgeci | 800 kaynağın **2'si mülgaydı** | sızıntı **2 → 0**, `recall@10` **0,9500** değişmedi |
| `scripts/yeniden_uret.sh` | manşeti **kimse** yeniden üretemiyordu | `bash -n` temiz · iki geçerlilik kapısı gömülü |

## ▶️ Faz 3 — belge katmanı *($0)* → 🏷️ `v0.2`

**Ölçülmüş boşluk:** `PRODUCT.md` · `ROADMAP.md` · `TODO.md` · `docs/MIMARI.md` **yoktu**
(2026-09-06'da silinen doküman katmanının yerine hiçbir şey konmamıştı).
`verify:` dört belge var · kırık link kalmadı · ⛔ `docs/record/**` ve `docs/adr/**`
**değişmedi** (`git diff --stat` → 0).

## ⏳ Mevzuat kapsam + tazelik *(ayrı plan, 62 kutucuk)*

**Ölçülmüş boşluk:** korpus **892 kanun · 40.496 madde** — yönetmelik/tüzük/KHK **yok**; ve
korpusta **tek bir tarih alanı bile yoktu** (2026-09-07'de eklendi: `data/corpus/KUNYE.json`).
**Hedef:** ~**340.303** madde (**8,4×**), indeks 83 MB → **~697 MB**.
⛔ **Bağımlılık:** ana planın **Görev 8'i (indeks dağıtımı) bunu bekliyor** — bugünkü 79 MB'ı
paketlemek, birkaç hafta sonra atılacak bir iştir.
`verify:` [`plans/2026-09-08-mevzuat-kapsam-ve-tazelik.md`](docs/superpowers/plans/2026-09-08-mevzuat-kapsam-ve-tazelik.md)

## ⏳ Faz 4 — Hat B, model *(~$7-15, Modal)* → 🏷️ `v1.0` kapısı

| ne | neden (ölçülmüş boşluk) | bedel |
| :--- | :--- | ---: |
| **B1 — isabetsizlik** | **8/80** ve rakiplerden **iyi değil** (8 ↔ 8 ↔ 7 ↔ 8); hiç çalışılmadı | ~$3-7 |
| **B4 — `τ_a` merge'de seyreliyor** | 0,987 → 0,766 (**−22,1 p**); ‖τ‖ oranı **8,87×** | ~$3-5 |
| **Kabul testi** | donmuş TEST **hiç açılmadı** ⇒ `v1.0` verilmedi | ~$0,1 |

⚠️ Kabul testinin erişim tavanı **≈0,75** (DEV 0,95 değil) — ADR-0069'un raporlaması **zorunlu**.
⛔ Donmuş TEST **tek kez** açılır.

## ⏳ `v2` — uygulama katmanı

Canlı `bedesten` API (**B6**, ⚠️ TR IP şart) · tam kapsam · tazelik boru hattı · HTTP API +
barındırma (**S9 açık**) · tablo/cetvel satırları (**B9** — ~7.966 satır madde diye indeksli).

---

## 🔓 Açık kararlar

| # | soru | durum |
| :-- | :--- | :--- |
| **S9** | `v2` nasıl barındırılır? | 🔓 açık — bu planın dışında |
| **S10** | sorumluluk ibaresinin **nihai hukuki metni** | 🔓 açık — geçici metin yürürlükte, hukukçu görüşü bekliyor |
| **S12** | KARAR-6 paralel slot (`-np`) | ⏸️ ertelendi — `τ_a` v2 turuna |
| **S17** | kuantizasyon eğrisi ölçülsün mü? | 🔓 açık — bu planın dışında |
| ~~S5·S7·S8·S16·S18~~ | — | ✅ kapandı 2026-09-07 |
