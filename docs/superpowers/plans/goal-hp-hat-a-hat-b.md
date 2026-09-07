# `/goal` promptu — planın KALAN kısmı için

**Kullanım:** aşağıdaki bloğu olduğu gibi `/goal` komutuna yapıştır.
⚠️ `/goal` **4000 karakter** sınırı koyuyor; bu metin **3.988 karakter** (2026-09-07, **üçüncü sürüm** — SIRA 3 eklendi).
Ayrıntı planın kendisinde: [`2026-09-07-hp-hat-a-hat-b.md`](2026-09-07-hp-hat-a-hat-b.md).

> 🔄 **Bu goal 2026-09-07'de YENİLENDİ.** İlk sürüm planın tamamını başlatıyordu; **60/89
> kutucuk bitti** (`v0.2` etiketlendi) ve geri kalan iş **lineer bir sıraya** indi. Yeni metin
> yalnız o sırayı taşıyor — bitmiş fazları tekrar anlatmıyor, çünkü bir goal promptunun işi
> *"şimdi ne yapılacak"*, *"neler oldu"* değil (o planın İCRA DURUMU bloğunda).

---

```
/goal Planı BİTİR: docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md
⭐ ÖNCE OKU: planın en üstündeki "İCRA DURUMU" bloğu — 62/89 BİTTİ. Sıra LİNEER, atlanmaz.
Adımların tamamı planın kendi görev bölümünde; burada sıra + kapılar var.
✅ BİTTİ (dokunma): FAZ 1-2-3 → 🏷️ v0.2 ETİKETLENDİ · 143 test yeşil · harcanan $3,155.
⛔ ATLANDI: G2 üçüncü hakem (bütçe, ADR-0074) · G8 indeks dağıtımı (korpus 8,4× büyüyecek).

━━ SIRA 1 · G8 Adım 1b — KUNYE taşınabilirlik · $0 · GPU YOK
KUNYE.json MUTLAK YOL + mtime damgalıyor, retriever.py:143-152 doğruluyor ⇒ git clone
sonrası HER MAKİNEDE SystemExit. Yap: yol repo-göreli · mtime → içerik hash · künyeye
bge-m3 revision. verify: repo BAŞKA DİZİNE kopyalanır, retriever yükler, recall@10=0,9500.

━━ SIRA 2 · G12 Adım 6-7 — TUI gözle doğrula + commit · $0 · GPU İSTER
llama-server aç, `python -m hakhukuk.tui`, ÜÇ soru sor, kapat. verify: üçünde de
rozet+atıf+kaynak+sorumluluk ibaresi EKRANDA GÖRÜLDÜ.

━━ SIRA 3 · G4 — Sonnet-5 ÖZNE olarak rakip havuzuna girer 🆕 (karar KİLİTLİ)
Havuzda yalnız Gemini var; frontier sınıfı HİÇ ölçülmedi. Kapıyı ETKİLEMEZ (ADR-0072 m.2:
eşik oynamaz, çıpa 3.5 Flash kalır, yeni özne yalnız RAPORLANIR).
✅ BEDEL ÖLÇÜLDÜ: tam koşu ~$0,82 (duman 5 kalem = $0,0512, bakiye farkından) ⇒ $1
kapısının ALTINDA, doğrudan koşulabilir. Planın "~$0,35"i Gemini fiyatıyla, YANLIŞTI.
Rejim F0.4'ün BİREBİR aynısı: --reasoning-budget 1024 (--think-budget DEĞİL) · k=10 ·
900 klip · seed 3407 · önsözsüz · n=80.
KAPI: recall@10 hepsinde 0,9500 — değilse harness eşleşmemiş, HÜKÜM KURULMAZ.
⚠️ Red-regex YENİ AİLEDE KALİBRE EDİLİR (F0.4'te Gemini'de 6 y.pozitif, bizde 0);
özne başına ALET / GÖZ-orta / GÖZ-katı ÜÇ okuma raporlanır.

━━ SIRA 4 · G14 (B1, 6 kutucuk) + G15 (B4, 4) · Modal ~$6,3
⛔ DUR ve SOR: koşulsun mu? B1 8/80, rakipler 8·8·7·8 ⇒ GERİDE DEĞİLİZ. B10'un dersi:
hedef iki kaleme daraldı, tur kapatıldı. Koşulacaksa ÖN-KAYIT zorunlu. Atlanırsa planda
"atlandı + gerekçe" damgası, sonra SIRA 5.

━━ SIRA 5 · G16 Adım 2-4 — v1.0 KABUL TESTİ · ~$0,10 · EN SON
⛔⛔ DONMUŞ TEST TEK KEZ AÇILIR — açmadan ÖNCE İNSAN ONAYI AL.
Adım 1 BİTTİ (DEV'de üç madde + Wilson şerhleri türetildi).
ADR-0069 ZORUNLU: ham kütle MANŞET · tavan kullanımı yanında · her iki setin recall@10'u
yanında · ⛔ rakip kıyası o orandan KURULMAZ. TEST tavanı ≈0,75 (DEV 0,95) ⇒ ham kütle
düşük çıkacak, BAŞARISIZLIK DEĞİL. Geçerse v1.0; geçmezse sayı DAMGALANARAK yayımlanır
ve v0.x devam (ADR-0065). Hüküm ADR + research_log + MODEL_CARD'da AYNI sayıyla.

━━ ERTELENDİ: G11 Adım 2 (temiz makine kapısı) — G8'e bağlı, bugün TANIM GEREĞİ düşer.

🚨 BÜTÇE: OpenRouter $3,45 · Modal $29,19. Kalan planın OpenRouter ihtiyacı ~$0,30
(+SIRA 3'ün ölçülmemiş bedeli). ⚠️ GERÇEK FATURA raporlanan judge_cost'un 1,6 KATI.
⚡ HER GPU KOŞUSUNDAN ÖNCE künyede `güç : ŞARJDA` DOĞRULA (pilde 12× yavaş).
🔒 BAĞLAYICI HAKEM = openai/gpt-4o-mini (ADR-0074) — kapının İKİ TARAFI da onunla ölçüldü.
İkinci hakemle kütle 0,6940 ölçüldü ama YAYIMLANMAZ: eşit sınav yok.

KURALLAR: TDD (önce failing test, koş, gör, sonra kod) · uzun koşu setsid nohup, |tail YOK ·
GPU işini subagent'a ver · her adımda plan-göreli STATUS · sayı hatırlanmaz KAYNAKLANIR ·
çelişki İKİ YERDE damgalanır · gözle okuma bir KAPIDIR · kutucuk yalnız verify ALINDIKTAN
sonra · yapısal ↔ davranışsal AYRI commit · sıradaki ADR 0075, log #65 · belge/commit
TÜRKÇE, kod İngilizce · ⛔ docs/record/** ve docs/adr/** TARİHSEL KAYIT, dokunulmaz.

⛔ DUR ve SOR: donmuş TEST · SIRA 4'ün koşulması · tek adımda >$1 · yeni rejim kararı ·
bir AÇIK KARAR damgasını kendi başına kapatmak.
```

---

## Sıranın neden bu olduğu

| sıra | iş | neden burada |
| :--- | :--- | :--- |
| **1** | `KUNYE` taşınabilirlik | **$0, bağımsız, ve bugün ürünü kıran tek şey** — `git clone` yapan herkeste `SystemExit`. Planda zaten *"BEKLEMEZ"* damgalı. |
| **2** | TUI gözle doğrulama | **$0**, GPU ister ama kısa. Ürün yüzünün insan gözüyle görülmediği tek yer. |
| **3** 🆕 | Sonnet-5 öznesi | **Bağımsız ve kapıyı etkilemiyor** (ADR-0072 m.2) ⇒ istenen anda koşulabilir; erken konuldu çünkü havuzda **frontier sınıfı hiç yok**. ✅ Bedeli ölçüldü: **~$0,82**. |
| **4** | `B1` · `B4` eğitim turları | **Para ve saat harcayan tek blok** ⇒ karar noktası. Sonucu belirsiz; atlanırsa 5'e geçilir. |
| **5** | Donmuş TEST | ⛔ **TEK KEZ açılır.** 4 koşulacaksa model değişir; test ondan **sonra** açılmalı — yoksa iyileşmiş modeli ölçecek el değmemiş set kalmaz. |

⚠️ **G11 Adım 2 (temiz makine kapısı) sıraya girmiyor:** `git clone` + `uv sync` + tek komutun
çalışması **indeksin dağıtılmasına** bağlı (G8) ve G8 korpus kararını bekliyor. Bugün koşulsa
**tanım gereği düşer**; bu bir eksiklik değil, bilinen bir bağımlılık.

## Bu goal neyi kasten dışarıda bırakıyor

| iş | nerede | neden burada değil |
| :--- | :--- | :--- |
| **G2** üçüncü **hakem** ailesi | plan, ⛔ ATLANDI damgalı | Bütçe kararı — [ADR-0074](../../adr/0074-hakem-paneli-kuruldu-baglayici-hukum.md)'de sayıyla. ⚠️ **G4 artık burada değil: SIRA 3'e alındı** (özne bedeli ≠ hakem bedeli) |
| **G8** indeks dağıtımı | plan, ⛔ BEKLETİLİYOR | Korpus **8,4×** büyüyecek; bugünkü 79 MB'ı paketlemek boşa iş |
| **T1** `models/` ~20 GB temizliği | Faz 0 planı §⏭️ | S7 kapandı ⇒ koşabilir, ama kimseyi bloke etmiyor |
| **Hat C** metodoloji yazısı | spec §7 | `v1.0` sonrası |
| **S9** `v2` barındırma · **S17** kuantizasyon eğrisi | [`ROADMAP.md`](../../../ROADMAP.md) | Bu planın dışında |
| `recall_taban.json` · korpus `4857/Madde 111` çelişkisi · `terazi` yinelenen atıf | [`TODO.md`](../../../TODO.md) | **$0**, bağımsız; sıraya girmeden herhangi bir anda ödenebilir |
