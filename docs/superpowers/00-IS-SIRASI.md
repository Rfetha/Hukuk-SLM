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
> ⛔ Bir belgeyi sıradan çıkarmak ya da araya sokmak **insan kararıdır** — kendi başına yapma.

---

## Bir bakışta

```
✅ BİTTİ   ▸ 2026-09-06-faz0-olcum-zinciri.md            48/48 · $1,47 · KAPANDI
──────────────────────────────────────────────────────────────────────────────
▶️  ŞİMDİ  ▸ 2026-09-07-hp-hat-a-hat-b.md          89 kutucuk · **60 bitti**
             başlatıcı: goal-hp-hat-a-hat-b.md  (YENİLENDİ 2026-09-07, 3.873 krk)
             ✅ FAZ 1 HP (G1·G3) · ✅ FAZ 2 Hat A · ✅ FAZ 3 belge → 🏷️ **v0.2 ETİKETLENDİ**
             ⛔ G2·G4 ATLANDI (bütçe, ADR-0074) · ⛔ G8 BEKLETİLİYOR
             ⏳ KALAN 17 kutucuk, LİNEER SIRA (planın İCRA DURUMU bloğunda):
                1. G8 Adım 1b  KUNYE taşınabilirlik   $0
                2. G12 Adım 6-7 TUI gözle doğrula     $0 · GPU
                3. G14+G15 eğitim turları             ~$6,3 ⛔ DUR ve SOR
                4. G16 Adım 2-4 kabul testi           ~$0,10 ⛔⛔ donmuş TEST
──────────────────────────────────────────────────────────────────────────────
⏳ SONRA   ▸ 2026-09-08-mevzuat-kapsam-ve-tazelik.md      9 görev · 62 kutucuk
             spec: specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md (onaylı)
             korpus 40.496 → ~340.303 madde, 5 kat, her kat bir kapıdan
             ⚠️ G7 kat 4-5 tek adımda >$1 (Modal ~1,5 sa) — DUR ve SOR
             bitince → ana planın Görev 8'i AÇILIR → 🏷️ v0.2 yayını
──────────────────────────────────────────────────────────────────────────────
⏳ EN SON  ▸ 2026-09-07-hp-hat-a-hat-b.md · FAZ 4 Hat B   14 kutucuk · ~$7-15
             donmuş TEST kabul koşusu → 🏷️ v1.0 kapısı
```

---

## Görev 8 nedir — *"kullanıcı indeksi nereden alacak"*

Retriever olmadan ürün yok, ve retriever **indeks** olmadan çalışmaz. Ama indeks ikili bir
dosya ve **git'te değil**:

| | |
| :--- | :--- |
| indeks | `data/index/mevzuat_bge_m3_s2/gomme.npy` = **79 MB** |
| git'te mi | ⛔ **hayır** — `.gitignore:166` `data/index/**/*.npy` |
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

### ⚠️ Ama iki iş BEKLEMEZ — ikisi de doğruluk meselesi, boyut meselesi değil

| iş | neden beklemez |
| :--- | :--- |
| **Görev 8b** · mülga madde süzgeci | Bugün 800 getirilen kaynağın 2'si **yürürlükten kalkmış** madde ve vatandaşa gidiyor. Bu eksik özellik değil, **YANLIŞ CEVAP**. Korpus büyüyünce sayı da büyür — erken düzelt. |
| **Görev 8 Adım 1b** · `KUNYE` taşınabilirlik kilidi | `KUNYE.json` **mutlak yol + `mtime`** damgalıyor ve `retriever.py`:143-152 bunu yüklemede doğruluyor ⇒ `git clone` sonrası `mtime` checkout zamanı olur ve **her makinede `SystemExit`**. İndeks 79 MB da olsa 697 MB da olsa aynı çöküş. |

---

## Belge belge — ne olduğu ve durumu

| belge | tür | durum | ne der |
| :--- | :--- | :--- | :--- |
| [`plans/2026-09-06-faz0-olcum-zinciri.md`](plans/2026-09-06-faz0-olcum-zinciri.md) | plan | ✅ **48/48 KAPANDI** | Ölçüm zinciri onarıldı; v1.0 kapısının üç maddesi de DEV'de sayıyla geçti. Aletin **beş** kusuru bulundu. Artık **kayıt**tır — açılmaz, kutucuğu işaretlenmez. |
| [`plans/2026-09-07-hp-hat-a-hat-b.md`](plans/2026-09-07-hp-hat-a-hat-b.md) | plan | ▶️ **AÇIK, 60/89** | Yürüyen ana plan. **En üstünde İCRA DURUMU bloğu var — durum oradan okunur.** `v0.2` bu planla etiketlendi; kalan 17 kutucuk lineer sıraya indi. |
| [`plans/goal-hp-hat-a-hat-b.md`](plans/goal-hp-hat-a-hat-b.md) | başlatıcı | 🔄 **YENİLENDİ 2026-09-07** | Planın `/goal` promptu. İlk sürüm planın tamamını başlatıyordu; ikinci sürüm **yalnız kalan 17 kutucuğun lineer sırasını** taşıyor (3.873/4000 krk). Plan ilerledikçe **bu da yenilenir**. |
| [`specs/2026-09-06-yeni-belge-katmani-design.md`](specs/2026-09-06-yeni-belge-katmani-design.md) | spec | ✅ **plana döküldü** | Ana planın *niye bu sırada* olduğunun gerekçesi. Yeni iş üretmez; sıra tartışılırsa buraya bakılır. |
| [`specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md`](specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md) | spec | ✅ **plana döküldü** | Üç kilitli karar (K1 kapsam · K2 anlık görüntü + fark taraması · K3 kapsam kapısı). ⚠️ Plan yazılırken **iki sayısı ölçülerek çürütüldü** ve §7b'ye damgalandı. |
| [`plans/2026-09-08-mevzuat-kapsam-ve-tazelik.md`](plans/2026-09-08-mevzuat-kapsam-ve-tazelik.md) | plan | ⏳ **yazıldı, 0/62** | Yukarıdaki spec'in uygulaması. Ana plandan **sonra** koşar. |

---

## Bu sıranın dışında kalanlar

| iş | nerede | neden dışarıda |
| :--- | :--- | :--- |
| **T1** `models/` ~20 GB temizliği | Faz 0 planı §⏭️ | Ön koşulu S7'ydi; S7 kapandı (**yalnız merge GGUF**) ⇒ artık koşabilir, ama kimseyi bloke etmiyor |
| **Hat C** metodoloji yazısı | yeni-belge-katmani spec §7 | `v1.0` sonrası |
| **S9** `v2` barındırma · **S17** kuantizasyon eğrisi | — | Hiçbir planın kapsamında değil; açık soru olarak duruyor |
| `recall_taban.json` | ana plan §⏭️ | Faz 0'ın tek *"kaynaklanmadı"* ihlali. $0, ~15 dk — bir sonraki durakta ödenir |

---

## Bakım kuralı

Bir plan kapandığında **iki yer** güncellenir: planın kendi ✅ kapanış bloğu ve **bu dosyanın
"Bir bakışta" kutusu**. Sıra değişirse gerekçe buraya yazılır — sıra değişikliğinin *niye*si
başka hiçbir yerde durmuyor.
