# `/goal` promptu — planın KALAN kısmı için

**Kullanım:** aşağıdaki bloğu olduğu gibi `/goal` komutuna yapıştır.
⚠️ `/goal` **4000 karakter** sınırı koyuyor; bu metin **3.873 karakter** (2026-09-07, ikinci sürüm).
Ayrıntı planın kendisinde: [`2026-09-07-hp-hat-a-hat-b.md`](2026-09-07-hp-hat-a-hat-b.md).

> 🔄 **Bu goal 2026-09-07'de YENİLENDİ.** İlk sürüm planın tamamını başlatıyordu; **60/89
> kutucuk bitti** (`v0.2` etiketlendi) ve geri kalan iş **lineer bir sıraya** indi. Yeni metin
> yalnız o sırayı taşıyor — bitmiş fazları tekrar anlatmıyor, çünkü bir goal promptunun işi
> *"şimdi ne yapılacak"*, *"neler oldu"* değil (o planın İCRA DURUMU bloğunda).

---

```
/goal Planı BİTİR: docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md
⭐ ÖNCE OKU: planın en üstündeki "İCRA DURUMU" bloğu — 60/89 kutucuk BİTTİ.
Kalan 17 kutucuk ve sırası AŞAĞIDA. Sıra LİNEER, atlanmaz.

✅ BİTTİ (dokunma): FAZ 1 hakem paneli (G1·G3) · FAZ 2 Hat A (G5-G12) ·
FAZ 3 belge katmanı (G13) → 🏷️ v0.2 ETİKETLENDİ · 143 test yeşil · harcanan $3,155.
⛔ BİLİNÇLİ ATLANDI (12 kutucuk, açma): G2·G4 (bütçe, ADR-0074) · G8 (korpus 8,4× büyüyecek).

━━ SIRA 1 · G8 Adım 1b — KUNYE taşınabilirlik kilidi · $0 · GPU YOK
KUNYE.json korpusu MUTLAK YOL + mtime ile damgalıyor, retriever.py:143-152 yüklemede
doğruluyor ⇒ git clone sonrası mtime checkout zamanı olur, HER MAKİNEDE SystemExit.
Yap: mutlak yol → repo-göreli · mtime → içerik hash · künyeye bge-m3 revision + önek
sözleşmesi. verify: repo BAŞKA DİZİNE kopyalanır, retriever hatasız yükler,
recall@10 = 0,9500 (ölçülmüş çıpa). TDD: önce failing test.

━━ SIRA 2 · G12 Adım 6-7 — TUI gözle doğrula + commit · $0 · GPU İSTER
llama-server aç (bayraklar: -ngl 99 -fa on --cache-type-k q8_0 --cache-type-v q8_0
-c 8192 --port 8080), `python -m hakhukuk.tui`, ÜÇ soru sor, gözle gör, kapat.
verify: üç soruda da rozet+atıf+kaynak+sorumluluk ibaresi ekranda GÖRÜLDÜ.

━━ SIRA 3 · G14 (B1 isabetsizlik, 6 kutucuk) + G15 (B4 τ_a genliği, 4) · Modal ~$6,3
⛔ DUR ve SOR: bu turlar KOŞULSUN MU? İnsan kararı. Gerekçe: B1 8/80 ve rakipler de
8·8·7·8 ⇒ GERİDE DEĞİLİZ. B10 turunun dersi: hedef iki kaleme daraldı, tur kapatıldı.
Koşulacaksa Adım 1 ÖN-KAYIT zorunlu (hedef bant + durma kuralı, KOŞUDAN ÖNCE).
Atlanacaksa planda "atlandı + gerekçe" damgası, sonra SIRA 4.

━━ SIRA 4 · G16 Adım 2-4 — v1.0 KABUL TESTİ · ~$0,10 · EN SON
⛔⛔ DONMUŞ TEST (data/eval/canon/) TEK KEZ AÇILIR — açmadan ÖNCE İNSAN ONAYI AL.
Adım 1 BİTTİ: DEV'de üç madde + Wilson şerhleri türetildi (kütle 0,8011 · isabetsizlik
8/80 aralık [4-15]/80 · M5 aralıkları ÖRTÜŞÜYOR ⇒ hüküm nokta tahminle).
ADR-0069 RAPORLAMASI ZORUNLU: ham kütle MANŞET · tavan kullanımı = kütle÷recall@10
YANINDA · her iki setin recall@10'u yanında · ⛔ rakip kıyası o orandan KURULMAZ.
TEST tavanı ≈0,75 (DEV 0,95) ⇒ ham kütle düşük çıkacak, bu BAŞARISIZLIK DEĞİL.
Geçerse v1.0 + HakHukuk-4B-v1.0-Q4_K_M.gguf; geçmezse sayı DAMGALANARAK yayımlanır,
v0.x devam (ADR-0065). Hüküm ADR + research_log + MODEL_CARD'da AYNI sayıyla.

━━ ERTELENDİ: G11 Adım 2 (temiz makine kapısı) — G8'e bağlı, indeks git'te yok,
BU TURDA GEÇEMEZ. Planda gerekçesiyle damgalı; açma.

🚨 BÜTÇE — ÖLÇÜLDÜ: OpenRouter $3,45 · Modal $29,19. ⚠️ GERÇEK FATURA raporlanan
judge_cost'un 1,6 KATI (kapı marjı, ölçüldü). Tahmini ×1,6 yapmadan harcama.
⚡ HER GPU KOŞUSUNDAN ÖNCE künyede `güç : ŞARJDA` DOĞRULA (pilde 12× yavaş).
🔒 BAĞLAYICI HAKEM = openai/gpt-4o-mini (ADR-0074). Değiştirme: kapının İKİ TARAFI da
onunla ölçüldü. İkinci hakemle kütle 0,6940 ölçüldü ama YAYIMLANMAZ — eşit sınav yok.

KURALLAR: TDD (önce failing test, koş, gör, sonra asgari kod) · uzun koşu setsid nohup,
|tail YOK · GPU işini subagent'a ver · her adımda plan-göreli STATUS · sayı hatırlanmaz
KAYNAKLANIR · çelişki İKİ YERDE damgalanır · gözle okuma bir KAPIDIR · kutucuk yalnız
verify: çıktısı ALINDIKTAN sonra · yapısal ↔ davranışsal AYRI commit · sıradaki ADR 0075,
research_log #65 · belge/commit TÜRKÇE, kod İngilizce · ⛔ docs/record/** ve docs/adr/**
TARİHSEL KAYIT, dokunulmaz.

⛔ DUR ve SOR: donmuş TEST'in açılması · SIRA 3'ün koşulup koşulmayacağı · tek adımda
>$1 · yeni rejim kararı · bir AÇIK KARAR damgasını kendi başına kapatmak.
```

---

## Sıranın neden bu olduğu

| sıra | iş | neden burada |
| :--- | :--- | :--- |
| **1** | `KUNYE` taşınabilirlik | **$0, bağımsız, ve bugün ürünü kıran tek şey** — `git clone` yapan herkeste `SystemExit`. Planda zaten *"BEKLEMEZ"* damgalı. |
| **2** | TUI gözle doğrulama | **$0**, GPU ister ama kısa. Ürün yüzünün insan gözüyle görülmediği tek yer. |
| **3** | `B1` · `B4` eğitim turları | **Para ve saat harcayan tek blok** ⇒ karar noktası. Sonucu belirsiz; atlanırsa 4'e geçilir. |
| **4** | Donmuş TEST | ⛔ **TEK KEZ açılır.** 3 koşulacaksa model değişir; test ondan **sonra** açılmalı — yoksa iyileşmiş modeli ölçecek el değmemiş set kalmaz. |

⚠️ **G11 Adım 2 (temiz makine kapısı) sıraya girmiyor:** `git clone` + `uv sync` + tek komutun
çalışması **indeksin dağıtılmasına** bağlı (G8) ve G8 korpus kararını bekliyor. Bugün koşulsa
**tanım gereği düşer**; bu bir eksiklik değil, bilinen bir bağımlılık.

## Bu goal neyi kasten dışarıda bırakıyor

| iş | nerede | neden burada değil |
| :--- | :--- | :--- |
| **G2** üçüncü hakem · **G4** rakip havuzu | plan, ⛔ ATLANDI damgalı | Bütçe kararı (insan, 2026-09-07) — [ADR-0074](../../adr/0074-hakem-paneli-kuruldu-baglayici-hukum.md)'de sayıyla yazılı |
| **G8** indeks dağıtımı | plan, ⛔ BEKLETİLİYOR | Korpus **8,4×** büyüyecek; bugünkü 79 MB'ı paketlemek boşa iş |
| **T1** `models/` ~20 GB temizliği | Faz 0 planı §⏭️ | S7 kapandı ⇒ koşabilir, ama kimseyi bloke etmiyor |
| **Hat C** metodoloji yazısı | spec §7 | `v1.0` sonrası |
| **S9** `v2` barındırma · **S17** kuantizasyon eğrisi | [`ROADMAP.md`](../../../ROADMAP.md) | Bu planın dışında |
| `recall_taban.json` · korpus `4857/Madde 111` çelişkisi · `terazi` yinelenen atıf | [`TODO.md`](../../../TODO.md) | **$0**, bağımsız; sıraya girmeden herhangi bir anda ödenebilir |
