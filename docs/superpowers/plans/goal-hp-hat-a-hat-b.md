# `/goal` promptu — planın KALAN kısmı için

**Kullanım:** aşağıdaki bloğu olduğu gibi `/goal` komutuna yapıştır.
⚠️ `/goal` **4000 karakter** sınırı koyuyor; bu metin **3.997 karakter** (2026-09-08, **beşinci sürüm** — araç katmanı eklendi, ADR-0076).
Ayrıntı planın kendisinde: [`2026-09-07-hp-hat-a-hat-b.md`](2026-09-07-hp-hat-a-hat-b.md).

> 🔄 **Bu goal iki kez yenilendi.** İlk sürüm planın tamamını başlatıyordu; `v0.2` etiketlenince
> geri kalan iş **lineer bir sıraya** indi (ikinci·üçüncü sürüm). **Dördüncü sürüm
> (2026-09-08):** [ADR-0075](../../adr/0075-v1-sft-kapanir-v2-sequential-rl.md) ile `v1`
> **SFT hattıyla kapandı** — eğitim turları (`G14`·`G15`) **atlandı**, yerine **modeli
> yayınlama** adımı (`G17`) girdi. Bir goal promptunun işi *"şimdi ne yapılacak"*, *"neler
> oldu"* değil (o planın İCRA DURUMU bloğunda).

---

```
/goal Planı BİTİR: docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md
⭐ ÖNCE OKU: planın "İCRA DURUMU" bloğu — sıra + adımlar orada.
✅ BİTTİ: FAZ 1-2-3 → 🏷️ v0.2 · 143 test yeşil · harcanan $3,21.
🔒 v1 = ham base + SFT, SFT İLE KAPANIR (ADR-0075).
⛔ ATLANDI, açma: G14 (B1) · G15 (B4) · G2 (üçüncü hakem) · G8 (indeks, korpus 8,4×).
B1'de rakiplerden GERİDE DEĞİLİZ (8/80 ↔ 8·8·7·8); B4 MERGE kaybı, v2'de merge YOK. İkisi
de BORÇ olarak açık.

━━ SIRA 1 · G8/1b — KUNYE taşınabilirlik · $0
KUNYE.json MUTLAK YOL + mtime damgalıyor (retriever.py:143-152) ⇒ git clone sonrası HER
MAKİNEDE SystemExit. Yol repo-göreli, mtime → içerik hash.
verify: repo BAŞKA DİZİNE kopyalanır, retriever yükler, recall@10 0,9500.

━━ SIRA 2 · G12/6-7 — TUI gözle doğrula · $0 · GPU
llama-server aç, `python -m hakhukuk.tui`, ÜÇ soru sor. verify: üçünde de
rozet+atıf+kaynak+ibare EKRANDA GÖRÜLDÜ.

━━ SIRA 3 · G4 — Sonnet-5 ÖZNE olarak rakip havuzuna · ~$0,82 (ÖLÇÜLDÜ)
Frontier HİÇ ölçülmedi. Kapıyı ETKİLEMEZ (ADR-0072 m.2). Rejim F0.4'ün BİREBİR aynısı:
--reasoning-budget 1024 (--think-budget DEĞİL) · k=10 · 900 klip · seed 3407 · önsözsüz ·
n=80. KAPI: recall@10 = 0,9500, değilse HÜKÜM KURULMAZ. Red-regex YENİ AİLEDE kalibre edilir;
ÜÇ okuma (ALET / GÖZ-orta / GÖZ-katı).

━━ SIRA 4 · G16/2-4 — v1.0 KABUL TESTİ · ~$0,10 · ⛔ ARAÇSIZ
⛔⛔ DONMUŞ TEST TEK KEZ AÇILIR — açmadan ÖNCE İNSAN ONAYI AL. Adım 1 BİTTİ.
ADR-0069 ZORUNLU: ham kütle MANŞET · tavan kullanımı + iki setin recall@10'u yanında ·
⛔ rakip kıyası o orandan KURULMAZ. TEST tavanı ≈0,75 ⇒ ham kütle düşük çıkacak, BAŞARISIZLIK
DEĞİL. Geçerse v1.0, geçmezse damgalanıp yayımlanır (ADR-0065).
⛔ Araç katmanı GİRMEZ (ADR-0076 m.4).

━━ SIRA 5 · G18 — ARAÇ KATMANI · $0 · ADR-0076
🚨 İlk gerekçesi ÇÜRÜDÜ: isabetsizlik 8/80'in 8'inde, aşırı-red 4/80'in 4'ünde altın ZATEN
BAĞLAMDAYDI ⇒ araç ÇÖZMEZ, sorun SEÇİM. Tek ölçülmüş hedef recall kaybı 4/80. Beş araç yine
de konur; gerekçe ÜRÜN YETENEĞİ, ÖLÇÜLMEMİŞ ⇒ kazancı sayıya eklenmez.
🔒 KAPI ↔ KALDIRAÇ: atıf doğrulama · mülga süzgeci · durum sınıflandırma TOOL DEĞİLDİR,
döngü DIŞINDA koşulsuz çalışır (uydurma 0/114 oradan). 5 KALDIRAÇ: ara · madde_getir ·
madde_var_mi · kanun_bul · yururlukte_mi — LLM ÇAĞIRMAZ.
⛔ Döngü SINIRLI, sınıra dayanmak GÖRÜNÜR: Durum.ARAMA_TUKENDI (KESIK'le BİRLEŞTİRİLMEZ).
🚨 REGRESYON: araçsız yolda 80 kalem BİREBİR aynı (suskunluk [15,37,45,66,79]).

━━ SIRA 6 · G17 — MODELİ YAYINLA · $0 → 🏷️ v1.0 RELEASE
🚨 Ağırlıklar HİÇBİR YERDE yayında değil (.gitignore:41, HF linki YOK) ⇒ "açık kaynak model"
iddiası YARIM. HF reposu + kart + üç belgede indirme yolu. ⚠️ Kartın İLK EKRANINDA: model
TEK BAŞINA sayıyı ÜRETEMEZ, indeks yok (G8).

━━ ERTELENDİ: G11/2 (temiz makine kapısı) — G8'e bağlı, bugün TANIM GEREĞİ düşer.
🔮 SONRAKİ TUR: v2 = tgta_v1 üstüne GRPO + düşünce ayarı + araç kullanımının EĞİTİMİ.
⛔ Ödül ÇEKİNMEYİ KORUMALI; taban: uydurma 0/114 · aşırı-red 4/80 · kütle 0,8011.
🚨 BÜTÇE: OpenRouter $3,40 · Modal $29,19; ihtiyaç ~$0,92. GERÇEK FATURA raporlananın
1,6 KATI. ⚡ GPU ÖNCESİ `güç : ŞARJDA`. 🔒 HAKEM = gpt-4o-mini (ADR-0074).

KURALLAR: TDD (failing test → koş → gör → kod) · uzun koşu setsid nohup, |tail YOK · GPU
işini subagent'a ver · plan-göreli STATUS · sayı KAYNAKLANIR · çelişki İKİ YERDE damgalanır ·
gözle okuma bir KAPIDIR · kutucuk yalnız verify ALINDIKTAN sonra · yapısal ↔ davranışsal
AYRI commit · ADR 0077, log #65 · TÜRKÇE belge, İngilizce kod · ⛔ docs/record/** ve
docs/adr/** dokunulmaz.
⛔ DUR ve SOR: donmuş TEST · >$1 · yeni rejim · AÇIK KARAR damgası.
```

---

## Sıranın neden bu olduğu

| sıra | iş | neden burada |
| :--- | :--- | :--- |
| **1** | `KUNYE` taşınabilirlik | **$0, bağımsız, ve bugün ürünü kıran tek şey** — `git clone` yapan herkeste `SystemExit`. Planda zaten *"BEKLEMEZ"* damgalı. |
| **2** | TUI gözle doğrulama | **$0**, GPU ister ama kısa. Ürün yüzünün insan gözüyle görülmediği tek yer. |
| **3** 🆕 | Sonnet-5 öznesi | **Bağımsız ve kapıyı etkilemiyor** (ADR-0072 m.2) ⇒ istenen anda koşulabilir; erken konuldu çünkü havuzda **frontier sınıfı hiç yok**. ✅ Bedeli ölçüldü: **~$0,82**. |
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
