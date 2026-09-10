# `docs/superpowers/` — iş sırası

> Bu klasörün **giriş dosyası**. Neyin ne zaman koşacağını söyleyen TEK yer.
> *(`00-` öneki kasten: dosya adı sıralamasında `plans/` ve `specs/`'in **üstüne**, listenin
> en başına çıksın diye. 2026-09-08'de kısa bir süre `README.md` idi — GitHub klasör görünümü
> için doğruydu ama IDE ağacında en dibe düşüp adını kaybediyordu; günlük bakılan yer IDE.)*

> **Bu dosya bir HARİTA, bir plan değil.** Kutucuk taşımaz. Söylediği tek şey: *elimdeki beş
> belgeden hangisi şimdi, hangisi sonra, ve hangisi neyi bekliyor.*
> Sıra **insan tarafından kilitlendi** (2026-09-07). Bir planın *içindeki* adım sırası o planın
> kendi meselesi; burası **planlar arası** sırayı bağlar.
>
> Bir belgeyi sıradan çıkarmak ya da araya sokmak **insan kararıdır** — kendi başına yapma.

---

## Bir bakışta

```
BİTTİ     2026-09-06-faz0-olcum-zinciri.md            48/48 · $1,47 · KAPANDI
──────────────────────────────────────────────────────────────────────────────
ŞİMDİ     2026-09-07-hp-hat-a-hat-b.md          99 kutucuk · 87 bitti
          başlatıcı: goal-hp-hat-a-hat-b.md  (3.995 karakter)
          FAZ 1-2-3-4 bitti → sürüm v0.3 ETİKETLENDİ (2026-09-09)
          FAZ 5 (dağıtım) AÇILDI 2026-09-10 — G19 API + G20 konteyner
          G2 ATLANDI (bütçe, ADR-0074) · G8 BEKLETİLİYOR (Adım 1b hariç, o bitti)
          G14+G15 EĞİTİM TURLARI ATLANDI (ADR-0075) — v1 SFT ile kapanır
          LİNEER SIRANIN DURUMU (planın İCRA DURUMU bloğunda):
             1. G8 Adım 1b  KUNYE taşınabilirlik   BİTTİ · recall@10 0,9500
             2. G12 Adım 6-7 TUI gözle doğrula     AÇIK — insan gözü kapısı
             3. G4  Sonnet-5 öznesi                BİTTİ · $1,1932 · Sonnet ÖNDE
             4. G16 Adım 2-4 kabul testi           BİTTİ · TEST kütle 0,5804
                                                   v1.0 VERİLMEDİ → v0.3 (ADR-0077)
             5. G18 araç katmanı                   BİTTİ · regresyon 80/80 birebir
             6. G17 modeli YAYINLA                 BİTTİ · HF'te, şu an ÖZEL
             7. G19 HTTP API (FastAPI)             5/6 — kod bitti, göz kapısı açık
             9. G20 konteyner dağıtımı             AÇIK — 5 karar kilitli (ADR-0078)
                                                   Adım 0 bir GPU KAPISI
          (8 = tickets; plan kutucuğu değil, numara goal ile aynı kalsın diye)
          AÇIK KUSURLAR: plans/post-hp-hat-b-tickets.md (on üç ticket)
──────────────────────────────────────────────────────────────────────────────
   SONRA   ▸ 2026-09-08-mevzuat-kapsam-ve-tazelik.md      9 görev · 62 kutucuk
             spec: specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md (onaylı)
             korpus 40.496 → ~340.303 madde, 5 kat, her kat bir kapıdan
                G7 kat 4-5 tek adımda >$1 (Modal ~1,5 sa) — DUR ve SOR
             bitince → ana planın Görev 8'i AÇILIR →    v0.2 yayını
──────────────────────────────────────────────────────────────────────────────
   EN SON  ▸ v2 — plan HENÜZ YAZILMADI · karar: ADR-0075
             tgta_v1 (bf16, 8,8 GB) = yeni başlangıç → GRPO + düşünce ayarı → v2.0
             mümkün çünkü DOĞRULANABİLİR ÖDÜL hazır (terazi.py deterministik)
                ön koşul: ödül fonksiyonu çekinmeyi KORUMALI (ADR-0010'un RL hâli)
```

---

## `v1` ↔ `v2` çizgisi — insan kararı 2026-09-08 ([ADR-0075](../adr/0075-v1-sft-kapanir-v2-sequential-rl.md))

```
v1   ham base ──► SFT (τ_g) + ORPO (τ_a) ──► ham TIES ──► tgta_v1 ──► YAYIN
v2   tgta_v1 (bf16) ──► GRPO + düşünce (thinking) ayarı ──► v2.0
```

**`v1` SFT ile KAPANIR** — `B1`/`B4` eğitim turları koşulmaz. İkisinin de gerekçesi ölçülmüş
ve **birbirinden farklı**: `B1`'de rakiplerden **geride değiliz** (8/80 ↔ 8·8·7·8) ve otomatik
metrik yok; `B4` ise bir **merge** kaybı (`τ_a` tek başına 0,987) ve `v2`'de merge olmadığı
için **konusuz** kalıyor.

### Araç katmanı `v1`'e dahil — [ADR-0076](../adr/0076-kapi-kaldirac-ayrimi-arac-katmani.md)

**KAPI ↔ KALDIRAÇ ayrımı:** atıf doğrulama · mülga süzgeci · durum sınıflandırma **TOOL
DEĞİLDİR** — döngünün dışında **koşulsuz** çalışır (uydurulmuş madde **0/114** garantisi
oradan gelir). Model yalnız **deterministik kaldıraçları** çağırır: `ara` · `madde_getir` ·
`madde_var_mi` · `kanun_bul` · `yururlukte_mi`.
Döngü **sınırlı** (`AZAMI_ADIM`) ve sınıra dayanmak **görünür**: `Durum.ARAMA_TUKENDI`.
Sebep: bu hattın en pahalı hata sınıfı *"hata vermeden yanlış"* — 17 tuzağın **hepsi** o
sınıftan, ve agentic akış tam o riski büyütür.
**Kapı koşusuna GİRMEZ** (ADR-0076 m.4): %80,1 ve eşik **araçsız** ölçüldü, rakipler araç
kullanamaz ⇒ araçlı koşmak ADR-0057'nin eşit sınavını ihlal eder. Sıra: **kabul testi →
araç katmanı → yayın.**
`v1`'de araç kullanımı **istem katmanındadır** (eğitilmedi, güvenilirliği düşük olacak);
**öğrenilmesi `v2`'nin işi** — GRPO ödülüne *"doğru aracı doğru anda çağırdı mı"* girer.
~~**CLI + TUI yeterli** (insan kararı) — HTTP API ve web arayüzü `v2`.~~
**BU CÜMLE 2026-09-09'da DEĞİŞTİ (insan kararı):** HTTP API `v1` tarafına alındı ve ana plana
**Görev 19** olarak girdi. Gerekçe teknik değil, tercihtir; öyle yazılıyor.
**S9 açılmadı:** API **yerel ve tek kullanıcı** (`127.0.0.1`, kimlik yok, hız sınırı yok).
Barındırma, mahremiyet vaadi ve TR IP kısıtı soruları `v2`'de açık duruyor. Web arayüzü hâlâ `v2`.

**2026-09-10'da ikinci kez genişledi (insan kararı):** **konteyner dağıtımı** da `v1` tarafına
alındı ve ana plana **Görev 20** olarak girdi ([ADR-0078](../adr/0078-konteyner-dagitimi-rejim-kilidi.md)).
**Konteyner web arayüzü değildir**; *"web arayüzü hâlâ `v2`"* cümlesi **yürürlükte kalır** ve
**S9 yine açılmadı** — `llama` yalnız iç ağda, `app` yalnız `127.0.0.1`'e yayımlanır.
Gerekçe bu kez teknik ve **ölçülmüş**: ticket 2, sunucu bayrağının **cevabı değiştirdiğini**
gösterdi (`q8_0` ↔ fp16, aynı seed, farklı `sha256`), ve bağlayıcı yapılandırmayı bugün hiçbir
şey zorlamıyor. `compose.yaml` onu zorlayan **ilk artefakttır** — paketleme burada kolaylık
değil, **rejim kilidi**.

**Bedeli:** `τ = θ_ft − θ_base` tanımı tüm kolların aynı base'i paylaşmasını şart koşar ⇒
`tgta_v1`'i yeni başlangıç almak bunu bozar ⇒ **ADR-0027'nin task-vector hattı `v1`'de
DONDURULUR**, `v2`'ye taşınmaz. `v2`'nin iddiası merge değil **RL kazancıdır**.
`B1` ve `B4` **borç olarak açık kalır** — koşulmadılar, ne verecekleri **bilinmiyor**.

---

## Görev 8 nedir — *"kullanıcı indeksi nereden alacak"*

Retriever olmadan ürün yok, ve retriever **indeks** olmadan çalışmaz. Ama indeks ikili bir
dosya ve **git'te değil**:

| | |
| :--- | :--- |
| indeks | `data/index/mevzuat_bge_m3_s2/gomme.npy` = **79 MB** |
| git'te mi | **hayır** — `.gitignore:166` `data/index/**/*.npy` |
| korpus | `data/corpus/mevzuat_maddeler.jsonl` = 37 MB, git'te **var** |
| sıfırdan üretmek | 40.496 maddeyi `bge-m3` ile gömmek: GPU ~10 dk, **CPU ~2 sa 45 dk** |

⇒ `git clone` yapan biri **çalışan bir ürün elde etmiyor**. Görev 8 bu boşluğu kapatıyor:
`hakhukuk/kurulum.py` indeksi **HF dataset'ten indirir** (karar S8 → **(a)**, 2026-09-07).

## Neden Görev 8 bekliyor — tek sebep, ölçülmüş

Görev 8 *"indeksi kullanıcıya nasıl dağıtırız"* sorusunu kapatıyor. Bugün cevabı yazsak
**yanlış boyutu** paketlemiş oluruz:

| | bugünkü korpus | insan kararıyla genişleyen korpus |
| :--- | ---: | ---: |
| belge | 892 | **9.722** |
| madde | 40.496 | **340.303** (8,4×) |
| indeks | 83 MB | **~697 MB** |

83 MB'ı HF dataset'e koymakla 697 MB'ı koymak **aynı iş değil** (S8'in *"(b) kurulumda üret"*
seçeneği bu yüzden öldü: gömme CPU'da ~23 saat). ⇒ Görev 8, korpus kararı koda dökülmeden
koşmaz. Kaynak: [spec §7b](specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md).

### Ama iki iş BEKLEMEZ — ikisi de doğruluk meselesi, boyut meselesi değil

| iş | neden beklemez |
| :--- | :--- |
| **Görev 8b** · mülga madde süzgeci | Bugün 800 getirilen kaynağın 2'si **yürürlükten kalkmış** madde ve vatandaşa gidiyor. Bu eksik özellik değil, **YANLIŞ CEVAP**. Korpus büyüyünce sayı da büyür — erken düzelt. |
| **Görev 8 Adım 1b** · `KUNYE` taşınabilirlik kilidi | **BİTTİ 2026-09-09.** `KUNYE.json` mutlak yol + `mtime` damgalıyordu ve `retriever.py` bunu yüklemede doğruluyordu ⇒ `git clone` sonrası her makinede `SystemExit`. Yol indeks dizinine **göreli**, `mtime` vekili **sha256** oldu. Doğrulandı: kopyalanmış ağaçtan yüklendi, `recall@10` **0,9500**. |

---

## Belge belge — ne olduğu ve durumu

| belge | tür | durum | ne der |
| :--- | :--- | :--- | :--- |
| [`plans/2026-09-06-faz0-olcum-zinciri.md`](plans/2026-09-06-faz0-olcum-zinciri.md) | plan | **48/48 KAPANDI** | Ölçüm zinciri onarıldı; v1.0 kapısının üç maddesi de DEV'de sayıyla geçti. Aletin **beş** kusuru bulundu. Artık **kayıt**tır — açılmaz, kutucuğu işaretlenmez. |
| [`plans/2026-09-07-hp-hat-a-hat-b.md`](plans/2026-09-07-hp-hat-a-hat-b.md) | plan | **AÇIK, 87/99** | Yürüyen ana plan. **En üstünde İCRA DURUMU bloğu var — durum oradan okunur.** `v0.2` ve `v0.3` bu planla etiketlendi. İş sırasının yedisinden beşi kapandı. Açık üçü: **SIRA 2** (insan gözüyle TUI doğrulaması), **SIRA 7** (Görev 19, HTTP API) ve **SIRA 9** (Görev 20, konteyner dağıtımı) — son ikisinin kararları kilitli, kodu yazılmadı. |
| [`plans/post-hp-hat-b-tickets.md`](plans/post-hp-hat-b-tickets.md) | ticket | **AÇIK, 13 ticket** | Ana planın yürütülmesi sırasında çıkan ve o planın kapsamında **çözülmeyen** kusurlar. En ağırı: ürün yolunda cevapların ~%5'i **boş** dönüyor ve bu, ADR-0040'ın geçerlilik kapısını geçmez. |
| [`plans/goal-hp-hat-a-hat-b.md`](plans/goal-hp-hat-a-hat-b.md) | başlatıcı | **YENİLENDİ 2026-09-10** | Planın `/goal` promptu (3.995 karakter, sınır 4.000). Plan ilerledikçe **bu da yenilenir**; bugünkü hâli dokuz sıralık düzeni taşıyor, açık üçü SIRA 2 · 7 · 9. |
| [`specs/2026-09-06-yeni-belge-katmani-design.md`](specs/2026-09-06-yeni-belge-katmani-design.md) | spec | **plana döküldü** | Ana planın *niye bu sırada* olduğunun gerekçesi. Yeni iş üretmez; sıra tartışılırsa buraya bakılır. |
| [`specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md`](specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md) | spec | **plana döküldü** | Üç kilitli karar (K1 kapsam · K2 anlık görüntü + fark taraması · K3 kapsam kapısı). Plan yazılırken **iki sayısı ölçülerek çürütüldü** ve §7b'ye damgalandı. |
| [`plans/2026-09-08-mevzuat-kapsam-ve-tazelik.md`](plans/2026-09-08-mevzuat-kapsam-ve-tazelik.md) | plan | **yazıldı, 0/62** | Yukarıdaki spec'in uygulaması. Ana plandan **sonra** koşar. |

---

## Bu sıranın dışında kalanlar

| iş | nerede | neden dışarıda |
| :--- | :--- | :--- |
| **T1** `models/` ~20 GB temizliği | Faz 0 planı §| Ön koşulu S7'ydi; S7 kapandı (**yalnız merge GGUF**) ⇒ artık koşabilir, ama kimseyi bloke etmiyor |
| **Hat C** metodoloji yazısı | yeni-belge-katmani spec §7 | `v1.0` sonrası |
| **S9** `v2` barındırma · **S17** kuantizasyon eğrisi | — | Hiçbir planın kapsamında değil; açık soru olarak duruyor |
| `recall_taban.json` | ana plan §| Faz 0'ın tek *"kaynaklanmadı"* ihlali. $0, ~15 dk — bir sonraki durakta ödenir |

---

## Bakım kuralı

Bir plan kapandığında **iki yer** güncellenir: planın kendi kapanış bloğu ve **bu dosyanın
"Bir bakışta" kutusu**. Sıra değişirse gerekçe buraya yazılır — sıra değişikliğinin *niye*si
başka hiçbir yerde durmuyor.

Bir planın yürütülmesi sırasında çıkan ve o planın kapsamında **çözülmeyen** kusur, plana
sıkıştırılmaz: [`plans/post-hp-hat-b-tickets.md`](plans/post-hp-hat-b-tickets.md) gibi ayrı bir
ticket dosyasına yazılır ve buradaki tabloya bir satır olarak girer. Planın kapsamı ile borcun
kaydı ayrı tutulur; yoksa plan hiç kapanmaz.
