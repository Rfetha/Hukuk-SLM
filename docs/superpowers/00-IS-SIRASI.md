# `docs/superpowers/` — iş sırası

> Bu klasörün **giriş dosyası**. Neyin ne zaman koşacağını söyleyen TEK yer.
> *(`00-` öneki kasten: dosya adı sıralamasında `plans/` ve `specs/`'in **üstüne**, listenin
> en başına çıksın diye. 2026-09-08'de kısa bir süre `README.md` idi — GitHub klasör görünümü
> için doğruydu ama IDE ağacında en dibe düşüp adını kaybediyordu; günlük bakılan yer IDE.)*

> **Bu dosya bir HARİTA, bir plan değil.** Kutucuk taşımaz. Söylediği tek şey: *elimdeki altı
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
BİTTİ     2026-09-07-hp-hat-a-hat-b.md    115/115 · KAPANDI 2026-09-12
──────────────────────────────────────────────────────────────────────────────
ŞİMDİ     (yeni plan AÇILMADI — devir tablosu kapanan planın KAPANIŞ bloğunda)
          2026-09-10: bitmiş 14 görev record/…-kapanan-gorevler.md'ye TAŞINDI
             plan 2.337 → 1.343 satır; dosyadaki kutucuk 40, payda 115
             (75 kutucuk kayda gitti; 2026-09-10 G21+G22 ile 16 kutucuk eklendi)
          başlatıcı: goal-hp-hat-a-hat-b.md  (3.997 karakter, İCRA MODU)
             insan onayı 2026-09-10: TASARIM FAZI BİTTİ. goal artık planın
             kalanını sub-agent-driven YÜRÜTÜR; kapı yoksa otonom akar,
             yalnız DUR listesinde (insan gözü · donmuş TEST · rejim · >$1 ·
             push · HF · açık karar · plan dışı iş) durur

          ── 2026-09-11 TURU · 88 → 112 kutucuk ───────────────────────────
             G21  11/11  ürün yüzeyi        7 kusur kapandı · göz kapısı GEÇTİ
             G22   5/5   rejim + KV         iki DUR-ve-SOR insana soruldu, ikisi
                                            de ONAYLANDI · $0,045067 harcandı
             G12   6-7   TUI göz kapısı     GEÇTİ (insan teyidi)
             G19   6     API göz kapısı     GEÇTİ (insan teyidi)
             G20   1-5   konteyner kodu     207 test · compose AYRIŞTIRILARAK çivili
             178 → 274 test yeşil · 43 commit YEREL (push EDİLMEDİ)
             ADR 0079 · 0080 · 0081 · 0082 · kayıt #66 · tuzak 1.11 · 1.12 · 1.13

             ⭐ TURUN DERSİ: ürün yüzeyini temizlemek ÖLÇÜM AYGITINDA üç kusur
             buldu. En ağırı — atıf doğrulayıcı kanun adını gevşek eşleştirip
             YANLIŞ kanuna DOGRULANDI basıyordu (7/16 → 0/16). Onarıldı,
             çıpalar yeniden puanlandı: 0/114 ve donmuş TEST 0/52 OYNAMADI,
             ama korunmanın ALETTEN değil ÖRNEKLEMDEN geldiği ortaya çıktı.
             İnsan kararıyla rakipler de yeniden puanlandı ⇒ 3.1 Flash-Lite
             1/152 → 0/153. ALEYHİMİZE ve öyle yazıldı; karşılığında EŞİT
             SINAV alındı (ADR-0057).

             ⭐ GÖZ KAPISININ BİLANÇOSU: 273 test YEŞİLKEN duran DÖRT kusuru
             bakan göz yakaladı — çift tırnak · madde biçimi · hakhukuk-api
             çalışmıyor · pyproject'in latent kurulum hatası. Hiçbirini
             sayısal kapı görmedi.

          ── YAPILDI (önceki turlar) ──────────────────────────────────────
             FAZ 1-2-3-4            v0.3 ETİKETLENDİ (2026-09-09)
             G8 Adım 1b   KUNYE taşınabilirlik    recall@10 0,9500
             G4           Sonnet-5 öznesi         $1,1932 · Sonnet ÖNDE
             G16          kabul testi             TEST kütle 0,5804 ⇒ v1.0
                                                  VERİLMEDİ → v0.3 (ADR-0077)
             G18          araç katmanı            regresyon 80/80 birebir
             G17          modeli YAYINLA          HF'te, şu an ÖZEL
             G19 Adım 1-5 HTTP API kodu           178 test yeşil (2026-09-10)
             G20 Adım 0   GPU kapısı              GEÇTİ — konteyner GPU'yu
                                                  host ile BİREBİR görüyor

          ── YAPILMADI · YOK — üçü de 2026-09-12'de KAPANDI ───────────────
             G20 Adım 6  docker compose up   ✅ KAPANDI 2026-09-11 (aşağıdaki
                            kusur onarıldıktan sonra). Konteyner UÇTAN UCA
                            ÇALIŞIYOR: HTTP 200, iki farklı soruyla doğrulandı.
                            ── önceki hâli ─────────────────────────────────
                                                 ⚠️ KISMEN KOŞTU 2026-09-11:
                            `indir` kutusu ÇIKIŞ 0 ile bitti — sha256 + bayt
                            kapısı GERÇEKTEN ateşlendi ve TUTTU; indeks
                            volume'de bulundu (HF yedeğine gidilmedi).
                            `llama` başlayamadı: 8080'i hazırlık için açılmış
                            bir llama-server tutuyordu (kapatıldı).
                            İmaj boyutu ÖLÇÜLDÜ: hakhukuk 2,13 GB · llama
                            6,99 GB · torch 2.14.0+cpu (CUDA tekerleği YOK).
             G20 Adım 7  konteyner göz kapısı   ✅ GEÇTİ 2026-09-12 (insan teyidi).
                            İnsan 422'nin gerçekten konteynerden gelip
                            gelmediğini SORGULADI; üç kanıtla doğrulandı.
             G20 Adım 8  belgeler + sürüm       ✅ KAPANDI 2026-09-11. Damga İŞİNİ
                            YAPTI: Adım 6 koştuğunda konteynerin her soruda
                            HTTP 500 verdiği ortaya çıktı (kusur 32). Onarım
                            sonrası damga ÖLÇÜLEN GERÇEKLE değiştirildi.

          ── AÇILMAYACAK / BEKLİYOR (karar) ───────────────────────────────
             G2           üçüncü hakem ailesi    ATLANDI — bütçe (ADR-0074)
             G14 + G15    eğitim turları         ATLANDI — v1 SFT ile kapanır
                                                 (ADR-0075)
             G8           indeks dağıtımı        BEKLETİLİYOR — korpus 8,4×
                                                 büyüyecek (Adım 1b hariç)

          AÇIK KUSURLAR: planın SONUNDAKİ bölüm — ARTIK YİRMİ SEKİZ, KUTUCUK
                         TAŞIMAZ. 2026-09-11'de on biri KAPANDI (1·2·3·4·5b·
                         7·8·12a·13·14·15·16·17·18·19·20·21·22·26·28), on beşi
                         YENİ DOĞDU (14-28) ve çoğu ölçüm aygıtından.
                         Eskisi: on üç, 11'i G21+G22'ye ALINDI, üçü DEVREDİLDİ: kusur 6 ve 12b
                         → v2 (borç B1 · B11) · kusur 11 → "sıranın dışında".
                         Kapanışta açık kalan her kusur ADIYLA devredilir;
                         devredilmemiş kusur KAPANIŞI GEÇERSİZ KILAR
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
| [`plans/2026-09-07-hp-hat-a-hat-b.md`](plans/2026-09-07-hp-hat-a-hat-b.md) | plan | **AÇIK, 88/115** | Yürüyen ana plan. **En üstünde İCRA DURUMU bloğu var — durum oradan okunur.** `v0.2` ve `v0.3` bu planla etiketlendi. İş sırasının yedisinden beşi kapandı. Açık üçü: **SIRA 2** (insan gözüyle TUI doğrulaması), **SIRA 7** (Görev 19 Adım 6 — kod bitti, göz kapısı açık) ve **SIRA 9** (Görev 20, konteyner — Adım 0 GEÇTİ). Plan kapsamı dışındaki on üç kusur da bu dosyanın **sonunda**, kutucuksuz. |
| [`plans/goal-hp-hat-a-hat-b.md`](plans/goal-hp-hat-a-hat-b.md) | başlatıcı | **İCRA MODU 2026-09-10** | Planın `/goal` promptu (3.997 karakter, sınır 4.000). **Tasarım fazı kapandıktan sonra icraya hizalandı**: alt-ajan sürümlü, kapı yoksa otonom akar. Açık beş sıra: **2 · 7 · 9 · 10 · 11**; ikisi (2 ve 7) insan gözü kapısıdır. |
| [`specs/2026-09-06-yeni-belge-katmani-design.md`](specs/2026-09-06-yeni-belge-katmani-design.md) | spec | **plana döküldü** | Ana planın *niye bu sırada* olduğunun gerekçesi. Yeni iş üretmez; sıra tartışılırsa buraya bakılır. |
| [`specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md`](specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md) | spec | **plana döküldü** | Üç kilitli karar (K1 kapsam · K2 anlık görüntü + fark taraması · K3 kapsam kapısı). Plan yazılırken **iki sayısı ölçülerek çürütüldü** ve §7b'ye damgalandı. |
| [`record/2026-09-10-…-kapanan-gorevler.md`](../record/2026-09-10-hp-hat-a-hat-b-kapanan-gorevler.md) | kayıt | **taşındı 2026-09-10** | Ana planın **bitmiş on dört görevinin** tam metni. Plan 2.337 → 1.343 satıra indi; yerlerinde kapanış blokları var. **Plan değildir** — kutucukları tarihseldir, açılmaz. Atlanan (G2·G14·G15) ve bekletilen (G8) görevler **planda kaldı**. |
| [`plans/2026-09-08-mevzuat-kapsam-ve-tazelik.md`](plans/2026-09-08-mevzuat-kapsam-ve-tazelik.md) | plan | **yazıldı, 0/62** | Yukarıdaki spec'in uygulaması. Ana plandan **sonra** koşar. |

---

## Bu sıranın dışında kalanlar

| iş | nerede | neden dışarıda |
| :--- | :--- | :--- |
| **T1** `models/` ~20 GB temizliği | Faz 0 planı §| Ön koşulu S7'ydi; S7 kapandı (**yalnız merge GGUF**) ⇒ artık koşabilir, ama kimseyi bloke etmiyor |
| **kusur 11** · `hakhukuk` paketi tek başına kurulamıyor | ana planın `AÇIK KUSURLAR` bölümü | **Ana plandan DEVREDİLDİ 2026-09-10.** `servis.py`:46 çalışma anında `scripts/`'e köprü kuruyor, `pyproject.toml`'un *"`scripts/` DIŞARIDA"* cümlesi geçersiz. Onarımı **yapısaldır**: aynı dosyayı 26 dosyanın yol köprüsü ve tüm ölçüm hattı kullanıyor ⇒ **kendi turu ve kendi regresyon koşusu**. [ADR-0078](../adr/0078-konteyner-dagitimi-rejim-kilidi.md) m.5 bugün onarmamaya karar verdi |
| **Hat C** metodoloji yazısı | yeni-belge-katmani spec §7 | `v1.0` sonrası |
| **S9** `v2` barındırma · **S17** kuantizasyon eğrisi | — | Hiçbir planın kapsamında değil; açık soru olarak duruyor |
| `recall_taban.json` | ana plan §| Faz 0'ın tek *"kaynaklanmadı"* ihlali. $0, ~15 dk — bir sonraki durakta ödenir |

---

## Bakım kuralı

Bir plan kapandığında **iki yer** güncellenir: planın kendi kapanış bloğu ve **bu dosyanın
"Bir bakışta" kutusu**. Sıra değişirse gerekçe buraya yazılır — sıra değişikliğinin *niye*si
başka hiçbir yerde durmuyor.

~~Bir planın yürütülmesi sırasında çıkan ve o planın kapsamında **çözülmeyen** kusur, plana
sıkıştırılmaz: ayrı bir ticket dosyasına yazılır ve buradaki tabloya bir satır olarak girer.~~

**BU KURAL 2026-09-10'da DEĞİŞTİ (insan kararı).** Ayrı ticket dosyası **kaldırıldı**;
`plans/post-hp-hat-b-tickets.md` silindi ve on üç kusur ana planın sonundaki
[AÇIK KUSURLAR](plans/2026-09-07-hp-hat-a-hat-b.md#açık-kusurlar--kayıt-ve-devir)
bölümüne taşındı. Gerekçe teknik değil, tercihtir; öyle yazılıyor.
**Kuralın koruduğu şey ayakta:** *"planın kapsamı ile borcun kaydı ayrı tutulur, yoksa plan hiç
kapanmaz"*. Ayrım artık dosyayla değil **kutucukla** sağlanıyor — kusur bölümü `- [ ]` taşımaz
ve paydaya girmez. Bu şart düşerse kural da düşer ve plan kapanamaz hâle gelir.
