# `/goal` promptu — planın KALAN kısmı için

**Kullanım:** aşağıdaki bloğu olduğu gibi `/goal` komutuna yapıştır.
⚠️ `/goal` **4000** sınırı koyuyor (bayt olarak sayıldı); bu metin **3.994 bayt** (2026-09-09, **altıncı sürüm** — `$1` kapısı ↔ `1,6×` çelişkisi giderildi).
Ayrıntı planın kendisinde: [`2026-09-07-hp-hat-a-hat-b.md`](2026-09-07-hp-hat-a-hat-b.md).

> 🔄 **Bu goal iki kez yenilendi.** İlk sürüm planın tamamını başlatıyordu; `v0.2` etiketlenince
> geri kalan iş **lineer bir sıraya** indi (ikinci·üçüncü sürüm). **Dördüncü sürüm
> (2026-09-08):** [ADR-0075](../../adr/0075-v1-sft-kapanir-v2-sequential-rl.md) ile `v1`
> **SFT hattıyla kapandı** — eğitim turları (`G14`·`G15`) **atlandı**, yerine **modeli
> yayınlama** adımı (`G17`) girdi. Bir goal promptunun işi *"şimdi ne yapılacak"*, *"neler
> oldu"* değil (o planın İCRA DURUMU bloğunda).
>
> **Altıncı sürüm (2026-09-09) — ajanı YANLIŞ YERDE DURDURACAK bir çelişki giderildi.** Beşinci
> sürüm aynı metinde hem *"SIRA 3 ~$0,82, `$1` kapısının altında"* hem *"gerçek fatura
> raporlananın **1,6 katı**"* diyordu; bunu okuyan ajan `0,82 × 1,6 = 1,31 > 1` diye çarpıp
> *DUR ve SOR* kuralına takılırdı. **Çarpım yanlış:** `$0,82` `judge_cost_usd`'den değil
> **bakiye farkından** okundu (`16,5520 → 16,6032`), yani **zaten gerçek faturanın kendisi** —
> `1,6×` yalnız **liste fiyatı türevi** olan `judge_cost_usd`'ye uygulanır. Artık ikisi de
> açıkça öyle yazıyor ve `DUR ve SOR` satırı `>$1 (SIRA 3 HARİÇ, ölçüldü)` diyor.
> Aynı turda eklenen iki ölçülmüş gerçek: `textual` **8.2.8 kurulu** (plan *"kurulu değil"*
> diyordu — bayattı) · `HF_TOKEN` **`.env`'de yok** ⇒ SIRA 6 insandan anahtar ister.

---

```
/goal Planı BİTİR: docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md
⭐ ÖNCE OKU: planın "İCRA DURUMU" bloğu — sıra + adımlar orada.
✅ BİTTİ: FAZ 1-2-3 → 🏷️ v0.2 · 143 test yeşil · $3,21. 🔒 v1 = ham base + SFT, SFT İLE
KAPANIR (ADR-0075). ⛔ ATLANDI, açma: G14 (B1) · G15 (B4) · G2 (3. hakem) · G8 (indeks).
B1: rakiplerden GERİDE DEĞİLİZ (8/80 ↔ 8·8·7·8); B4: MERGE kaybı, v2'de merge YOK. İkisi BORÇ.

━━ SIRA 1 · G8/1b — KUNYE taşınabilirlik · $0
KUNYE.json MUTLAK YOL + mtime damgalıyor (retriever.py:143-152) ⇒ git clone sonrası HER
MAKİNEDE SystemExit. Yol repo-göreli, mtime → içerik hash.
verify: repo BAŞKA DİZİNE kopyalanır, retriever yükler, recall@10 0,9500.

━━ SIRA 2 · G12/6-7 — TUI gözle doğrula · $0 · GPU
llama-server aç, `python -m hakhukuk.tui`, ÜÇ soru sor (textual 8.2.8 KURULU).
verify: üçünde de rozet+atıf+kaynak+ibare EKRANDA GÖRÜLDÜ.

━━ SIRA 3 · G4 — Sonnet-5 ÖZNE olarak rakip havuzuna · ~$0,82
✅ $1 KAPISI AÇIK: $0,82 BAKİYE farkı = ZATEN gerçek fatura ⇒ 1,6× ÇARPMA, sormadan KOŞ.
Frontier HİÇ ölçülmedi. Kapıyı ETKİLEMEZ (ADR-0072 m.2). Rejim F0.4'ün BİREBİR aynısı:
--reasoning-budget 1024 (--think-budget DEĞİL) · k=10 · 900 klip · seed 3407 · önsözsüz ·
n=80. KAPI: recall@10 = 0,9500, değilse HÜKÜM KURULMAZ. Red-regex YENİ AİLEDE kalibre edilir;
ÜÇ okuma (ALET/GÖZ-orta/GÖZ-katı).

━━ SIRA 4 · G16/2-4 — v1.0 KABUL TESTİ · ~$0,10 · ⛔ ARAÇSIZ (ADR-0076 m.4)
⛔⛔ DONMUŞ TEST TEK KEZ AÇILIR — açmadan ÖNCE İNSAN ONAYI AL. Adım 1 BİTTİ.
ADR-0069: ham kütle MANŞET · tavan kullanımı + iki setin recall@10'u yanında · ⛔ rakip
kıyası o orandan KURULMAZ. TEST tavanı ≈0,75 ⇒ kütle düşük çıkacak, BAŞARISIZLIK DEĞİL.
Geçerse v1.0, geçmezse damgalanıp yayımlanır (ADR-0065).

━━ SIRA 5 · G18 — ARAÇ KATMANI · $0 · ADR-0076
🚨 Gerekçesi ÇÜRÜDÜ: isabetsizlik 8/8, aşırı-red 4/4 — altın ZATEN BAĞLAMDAYDI ⇒ sorun
SEÇİM. Tek ölçülmüş hedef recall kaybı 4/80. Yine de konur; gerekçe ÜRÜN YETENEĞİ,
ÖLÇÜLMEMİŞ ⇒ kazancı sayıya EKLENMEZ.
🔒 KAPI ↔ KALDIRAÇ: atıf doğrulama · mülga süzgeci · durum sınıflandırma TOOL DEĞİLDİR,
döngü DIŞINDA koşulsuz çalışır (uydurma 0/114 oradan). 5 KALDIRAÇ: ara · madde_getir ·
madde_var_mi · kanun_bul · yururlukte_mi — LLM ÇAĞIRMAZ.
⛔ Döngü SINIRLI, sınır GÖRÜNÜR: Durum.ARAMA_TUKENDI (KESIK'le BİRLEŞTİRİLMEZ).
🚨 REGRESYON: araçsız yolda 80 kalem BİREBİR aynı (suskunluk [15,37,45,66,79]).

━━ SIRA 6 · G17 — MODELİ YAYINLA · $0 → 🏷️ v1.0 RELEASE
🚨 Ağırlıklar hiçbir yerde yayında DEĞİL (.gitignore:41, HF linki YOK) ⇒ "açık kaynak"
iddiası YARIM. HF reposu + kart + üç belgede indirme yolu. ⚠️ Kartın İLK EKRANINDA: model
TEK BAŞINA sayıyı ÜRETEMEZ, indeks yok (G8). ⛔ HF_TOKEN .env'de YOK — İNSANDAN İSTE.

━━ ERTELENDİ: G11/2 temiz makine kapısı — G8'e bağlı, bugün TANIM GEREĞİ düşer.
🔮 SONRAKİ TUR (plan DIŞI): v2 = tgta_v1 üstüne GRPO + araç kullanımının EĞİTİMİ.
Taban: uydurma 0/114 · aşırı-red 4/80 · kütle 0,8011.
🚨 BÜTÇE: OpenRouter $3,40 · Modal $29,19; ihtiyaç ~$0,92. 1,6× SADECE judge_cost_usd'ye
(liste fiyatı), BAKİYEYE DEĞİL. ⚡ GPU ÖNCESİ `güç : ŞARJDA`. 🔒 HAKEM = gpt-4o-mini.

KURALLAR: TDD (failing test → koş → gör → kod) · uzun koşu setsid nohup, |tail YOK · GPU
işini subagent'a ver · plan-göreli STATUS · sayı KAYNAKLANIR · çelişki İKİ YERDE damgalanır ·
gözle okuma bir KAPIDIR · kutucuk yalnız verify ALINDIKTAN sonra · yapısal ↔ davranışsal
AYRI commit · ADR 0077, log #65 · TÜRKÇE belge, İngilizce kod · ⛔ docs/record/** ve
docs/adr/** dokunulmaz.
⛔ DUR ve SOR: donmuş TEST · yeni rejim · AÇIK KARAR damgası · >$1 (SIRA 3 HARİÇ, ölçüldü).
```

---

## Sıranın neden bu olduğu

| sıra | iş | neden burada |
| :--- | :--- | :--- |
| **1** | `KUNYE` taşınabilirlik | **$0, bağımsız, ve bugün ürünü kıran tek şey** — `git clone` yapan herkeste `SystemExit`. Planda zaten *"BEKLEMEZ"* damgalı. |
| **2** | TUI gözle doğrulama | **$0**, GPU ister ama kısa. Ürün yüzünün insan gözüyle görülmediği tek yer. |
| **3** 🆕 | Sonnet-5 öznesi | **Bağımsız ve kapıyı etkilemiyor** (ADR-0072 m.2) ⇒ istenen anda koşulabilir; erken konuldu çünkü havuzda **frontier sınıfı hiç yok**. ✅ Bedeli **bakiye farkından** ölçüldü: **~$0,82** — bu `judge_cost_usd` türevi değil, **faturanın kendisi** ⇒ `1,6×` ile çarpılmaz, `$1` kapısı **açık**. |
| **4** | Donmuş TEST | ⛔ **TEK KEZ açılır** ve ⛔ **ARAÇSIZ** koşulur — rakipler araç kullanamaz (ADR-0076 m.4, eşit sınav). Eğitim turları atlandığı için model artık değişmeyecek ⇒ testi şimdi açmanın önünde engel yok. |
| **5** 🆕 | Araç katmanı | Davranışı değiştirir ⇒ kapıdan **sonra**. ⚠️ Eval hedefi **4 kalem** ve garanti değil; gerekçe **ürün yeteneği**, ölçülmemiş — ADR-0076'da öyle damgalı. |
| **6** 🆕 | Modeli yayınla | Kapı sonucu **adı belirler** (`v1.0` ya da `v0.2`) ⇒ yayın en sonda. |

⚠️ **G11 Adım 2 (temiz makine kapısı) sıraya girmiyor:** `git clone` + `uv sync` + tek komutun
çalışması **indeksin dağıtılmasına** bağlı (G8) ve G8 korpus kararını bekliyor. Bugün koşulsa
**tanım gereği düşer**; bu bir eksiklik değil, bilinen bir bağımlılık.

## Bu goal neyi kasten dışarıda bırakıyor

| iş | nerede | neden burada değil |
| :--- | :--- | :--- |
| **G2** üçüncü **hakem** ailesi | plan, ⛔ ATLANDI damgalı | Bütçe kararı — [ADR-0074](../../adr/0074-hakem-paneli-kuruldu-baglayici-hukum.md)'de sayıyla. ⚠️ **G4 artık burada değil: SIRA 3'e alındı** (özne bedeli ≠ hakem bedeli) |
| **G8** indeks dağıtımı | plan, ⛔ BEKLETİLİYOR | Korpus **8,4×** büyüyecek; bugünkü 79 MB'ı paketlemek boşa iş |
| **G14** `B1` · **G15** `B4` eğitim turları | plan, ⛔ ATLANDI | [ADR-0075](../../adr/0075-v1-sft-kapanir-v2-sequential-rl.md): `v1` SFT ile kapanır; `B4` `v2`'de **konusuz** kalır. İkisi de **borç olarak açık** |
| **`v2`** GRPO + düşünce ayarı | plan **yazılmadı** | ADR-0075'te karara bağlandı; spec + plan sonraki turda |
| **T1** `models/` ~20 GB temizliği | Faz 0 planı §⏭️ | S7 kapandı ⇒ koşabilir, ama kimseyi bloke etmiyor |
| **Hat C** metodoloji yazısı | spec §7 | `v1.0` sonrası |
| **S9** `v2` barındırma · **S17** kuantizasyon eğrisi | [`ROADMAP.md`](../../../ROADMAP.md) | Bu planın dışında |
| `recall_taban.json` · korpus `4857/Madde 111` çelişkisi · `terazi` yinelenen atıf | [`TODO.md`](../../../TODO.md) | **$0**, bağımsız; sıraya girmeden herhangi bir anda ödenebilir |
