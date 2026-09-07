# İş sırası — `docs/superpowers/` neyin ne zaman koşacağını söyleyen TEK dosya

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
▶️  ŞİMDİ  ▸ 2026-09-07-hp-hat-a-hat-b.md                89 kutucuk · 2 bitti
             başlatıcı: goal-hp-hat-a-hat-b.md  (/goal'a yapıştır, 3.936 krk)
             FAZ 1 HP → FAZ 2 Hat A (paralel) → FAZ 3 belge katmanı → 🏷️ v0.2
             ⛔ Görev 8 (indeks dağıtımı) BURADA KOŞMAZ — aşağı bak
──────────────────────────────────────────────────────────────────────────────
⏳ SONRA   ▸ mevzuat kapsam + tazelik planı              ← spec HAZIR, plan YAZILIYOR
             spec: specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md
             bitince → Görev 8 GENİŞLETİLMİŞ korpusla koşar → 🏷️ v0.2 yayını
──────────────────────────────────────────────────────────────────────────────
⏳ EN SON  ▸ 2026-09-07-hp-hat-a-hat-b.md · FAZ 4 Hat B   14 kutucuk · ~$7-15
             donmuş TEST kabul koşusu → 🏷️ v1.0 kapısı
```

---

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
| **Görev 8 Adım 1b** · `KUNYE` taşınabilirlik kilidi | Mutlak yol damgalayan künye başka makinede yeniden üretilemez. Korpus boyutundan bağımsız. |

---

## Belge belge — ne olduğu ve durumu

| belge | tür | durum | ne der |
| :--- | :--- | :--- | :--- |
| [`plans/2026-09-06-faz0-olcum-zinciri.md`](plans/2026-09-06-faz0-olcum-zinciri.md) | plan | ✅ **48/48 KAPANDI** | Ölçüm zinciri onarıldı; v1.0 kapısının üç maddesi de DEV'de sayıyla geçti. Aletin **beş** kusuru bulundu. Artık **kayıt**tır — açılmaz, kutucuğu işaretlenmez. |
| [`plans/2026-09-07-hp-hat-a-hat-b.md`](plans/2026-09-07-hp-hat-a-hat-b.md) | plan | ▶️ **AÇIK, 2/89** | Yürüyen ana plan. Borç kuyruğunu ve dokuz açık kararı taşır (yedisi 2026-09-07'de kapandı). |
| [`plans/goal-hp-hat-a-hat-b.md`](plans/goal-hp-hat-a-hat-b.md) | başlatıcı | ▶️ **canlı** | Yukarıdaki planın `/goal` promptu. 4000 karakter sınırına sıkıştırılmış. Plan değişince **bu da güncellenir**. |
| [`specs/2026-09-06-yeni-belge-katmani-design.md`](specs/2026-09-06-yeni-belge-katmani-design.md) | spec | ✅ **plana döküldü** | Ana planın *niye bu sırada* olduğunun gerekçesi. Yeni iş üretmez; sıra tartışılırsa buraya bakılır. |
| [`specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md`](specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md) | spec | ⏳ **onaylandı, PLANI YOK** | Üç kilitli karar (K1 kapsam · K2 anlık görüntü + fark taraması · K3 kapsam kapısı). Sıradaki plan yazma işi budur. |

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
