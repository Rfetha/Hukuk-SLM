# #42 — CP0: düşünce modu ölçülemedi, çünkü model **durmuyor** — ve bunu kol çözüyor

**Tarih:** 2026-07-29 · **CP:** Sprint 2 / CP0 · **Otorite:** [`TASARIM.md`](../../../TASARIM.md) ·
**Yürütme:** [`sprint2.md`](../../../sprint2.md) CP0 · **Karar belgeleri:** [ADR-0040](../../adr/0040-dusunce-modu-olculecek-on-kayitli-kural.md)
(ön-kayıtlı kural) → [ADR-0043](../../adr/0043-dusunce-modu-acik-butceli-kapatma.md) (sonuç)

> **Bir cümlede:** `--thinking on` altında çıplak base **6 moddan 3'ünde hiç cevap üretmiyor** —
> kesilme değil **sonlanmama**: model cevaplamak ile çekinmek arasında karar veremeyip aynı
> muhakemeyi 219 kez tekrarlıyor; bütçeyi **8× artırmak, örneklemeyi değiştirmek ve kuantizasyonu
> yükseltmek** üçü de çözmedi — **ama `τ_grounding` aynı istemlerde düşünüp duruyor** (35/36,
> medyan 510 token), yani eğitim düşünmeyi öldürmemiş, **kararlı hâle getirmiş.**

---

## 1. Künye

| | değer |
| :--- | :--- |
| özneler | `Qwen/Qwen3.5-4B` **çıplak base** (Q4_K_M ve Q8_0 GGUF) · **`τ_g` v1** (merge edilmiş, Q4_K_M) |
| taşıyıcı | llama.cpp `llama-server` · `-ngl 99 -fa on --no-context-shift` · KV q8_0/q8_0 |
| ctx | **8192-40960** *(Sprint 1'in 4096'sı düşünce bütçesinin yanına sığmıyor — sapma bilinçli, istem birebir aynı)* |
| üretim | `--thinking on` · `temperature 0` · **seed 3407** · `--max-chunk-chars 900` (eval-mirror) |
| havuz | **DEV** (`data/eval/dev/`) — TEST (`eval/canon/`) **görülmedi** |
| n | teşhis koşuları: mod başına **1-8 örnek** (tam CANON değil — kapı ölçümü değil, mekanizma tespiti) |
| hakem | **çağrılmadı** — puanlanacak cevap üretilemedi |
| maliyet | **$0** (yerel GPU, hakem yok) |
| güç | şarjda *(tuzak 1.6)* |
| çıktı | `outputs/eval/cp0_server_*.log` · teşhis dosyaları oturum scratchpad'inde *(kalıcı değil — sayılar bu belgede)* |

**Referans (thinking-off, Sprint 1 protokolü):** M2 Rej **0.6330** · M1 sadık-cevap kütlesi
**%42.6** · M5 ezber kütlesi **%10.7** · **249 token**/cevap
([`sprint1-sonuc-tablosu.md`](../sprint1/sprint1-sonuc-tablosu.md)).

---

## 2. 🚨 Bulgu 1 — `</think>` hiç kapanmıyor: kesilme değil **sonlanmama**

CP0-a'nın ilk smoke'u (`--max-new-tokens 4096`, M1) **ilk örnekte** patladı:

```
🚫 BOŞ cevap — örnek 0 (distractor), finish_reason='length', reasoning_content=15125 kar
```

`sprint2.md`'nin komut bloğu 4096'yı *"ADR-0030 ölçtü: 1024 yetmiyor"* gerekçesiyle yazmıştı.
**Yetmedi.** Bütçe 32768'e (**8×**) çıkarıldığında da:

| örnek | `finish_reason` | completion_tok | düşünce izi | `content` |
| :-- | :--- | ---: | ---: | ---: |
| 0 | `length` | **32.768** | 108.568 kar | **0** |
| 1 | `length` | **32.768** | 119.114 kar | **0** |

**Mekanizma bütçe değil, döngü.** İzin satır analizi:

| | satır | benzersiz | oran |
| :--- | ---: | ---: | ---: |
| örnek 0 | 1.456 | 225 | **%15.5** |
| örnek 1 | 994 | 216 | **%21.7** |

En çok tekrarlanan satırlar, ne olduğunu tek başına anlatıyor:

```
219× *   Okay, I will check the instruction again. "İlgili kaynak YOKSA cevap uydurma".
112× *   If I say "Verilen kaynaklarda bu konuyu düzenleyen madde bulunmuyor", it is the most accurate…
111× *   So I will use **KAYNAK 2**.
111× *   Wait, I need to check if I should say "Verilen kaynaklarda bu konuyu düzenleyen madde bulunmuyor"…
```

**Döngünün çekim merkezi bizim sistem istemimizdeki çekimserlik talimatı.** Model *"kaynaktan
cevapla"* ile *"kaynakta yoksa 'bulunmuyor' de"* arasında salınıyor; `temperature=0` greedy
decoding'de kaçış yok, aynı duruma dönüp duruyor.

> ⚠️ Bu **#38/#39 ile aynı sınıf** (sessiz içerik bozulması) ama **üçüncü bir mekanizma**: şablon
> doğru render ediliyor (#39 doğruladı), model bütçeyi tüketmiyor — **hiç bitirmiyor**.

---

## 3. Bulgu 2 — döngü **belirsizlikle** geliyor, modla değil

Aynı ayarlarla (8192 token) 4 mod, 3'er örnek:

| mod | ne soruyor | sonuç | ort completion_tok |
| :--- | :--- | :--- | ---: |
| **M4** oracle (tek gold) | cevap **açıkça** var | ✅ 3/3 sonlandı | **3.932** |
| **M3** boş bağlam | red **açıkça** doğru | ✅ 3/3 sonlandı, 3/3 temiz red | **1.126** |
| **M2** yakın-ıska tuzak | cevaplasam mı, reddetsem mi? | ❌ örnek 1'de düştü (28.441 kar iz) | — |
| **M5** kör (kaynak yok) | ezberden mi konuşsam? | ❌ örnek 0'da düştü (27.798 kar iz) | — |
| **M1** 5 kaynak (1 gold + 4 çeldirici) | hangisi ilgili? | ❌ 0/2 (32k'da bile) | — |

**Örüntü:** cevabın ya da reddin **açık** olduğu modlarda sorun yok; **karar belirsizse** model
duramıyor. Ve bu tam olarak ADR-0040'ın karar eksenlerinin bulunduğu yer — M1 kütlesi, M2 reddi,
M5 ezberi. **Yani ölçülemeyen üç sayı, tam da karar için gereken üç sayıydı.**

---

## 4. Bulgu 3 — üç alternatif açıklama **elendi**

| hipotez | test | sonuç |
| :--- | :--- | :--- |
| "bütçe yetersiz" | 4096 → **32768** (8×) | ❌ 2/2 yine düştü |
| "greedy decoding suçlu" | `temp 0.6 · top_p 0.95 · top_k 20` (Qwen'in düşünce modu önerisi), 8192 | 🟡 **yarısı**: örnek 0 sonlandı (**6.918 tok**), örnek 1 düştü |
| "Q4_K_M kuantizasyon artefaktı" | **Q8_0** GGUF (2× hassasiyet), temp 0, 8192 | ❌ **2/2 düştü** (28.568 / 28.419 kar iz) |

Örneklemenin yarısını kurtarması dikkate değer ama **çözüm değil**: hem %50 başarısızlık kalıyor,
hem sonlanan örnek **6.918 token** yakıyor, hem de protokolü kirletiyor — Sprint 1'in üç çıpası
`temperature=0` ile üretildi, örneklemeyi değiştirmek düşünce kazancını örnekleme değişikliğiyle
karıştırırdı.

Sonlanan `temp 0.6` örneğinin cevabı da ayrıca öğretici: gold kaynak **promptta VARken**
*"Verilen kaynaklarda genel bir hüküm bulunmamasına rağmen…"* diye başlıyor — yarı-çekimser.

---

## 5. ⭐ Bulgu 4 — `τ_g` v1 düşünüyor **ve duruyor**

ADR-0040 madde 3'ün "hasar sensörü" hasar aramaya gitti, **tersini buldu.** Aynı M1 istemleri,
aynı sunucu ayarları, `temp 0`, 8192 bütçe, n=8:

| # | `finish_reason` | completion_tok | düşünce izi | `content` |
| :-- | :--- | ---: | ---: | ---: |
| 0 | stop | 452 | 955 kar | 732 kar |
| 1 | stop | 563 | 1.568 | 604 |
| 2 | **length** | 8.192 | 1.000 | **8.625** *(bkz. §6)* |
| 3 | stop | 449 | 1.164 | 513 |
| 4 | stop | 434 | 819 | 870 |
| 5 | stop | 435 | 918 | 672 |
| 6 | stop | 477 | 1.062 | 820 |
| 7 | stop | 429 | 1.110 | 641 |

- **7/8 sonlandı** · sağlıklı 7'de **medyan 452, ort 463 token** (aralık 429-563 — çok dar)
- düşünce izinde **tekrar döngüsü YOK** — benzersiz/toplam satır oranı **8/8 dosyada 1.000**
- `</think>`'i **erken kapatma** da yok: her örnekte iz gerçekten dolu (819-1.568 kar)

**Base ile yan yana, aynı iki istem:**

| | base | **`τ_g` v1** |
| :--- | ---: | ---: |
| örnek 0 düşünce izi | **108.568 kar**, kapanmadı | **955 kar**, kapandı |
| örnek 1 düşünce izi | **119.114 kar**, kapanmadı | **1.568 kar**, kapandı |

**İzin kalitesi yapılı** — istenen eleme davranışının ta kendisi:

```
- KAYNAK 1: Discusses the effect of judgments on property — not directly about court decisions in favor
- KAYNAK 3: Specifically addresses court decisions in favor of the plaintiff — this is the most relevant
I should quote the relevant portion from KAYNAK 3 and cite it properly.
```

**Yorum:** `τ_g`'nin eğitim verisinde akıl yürütme izi **yok** (`<think>\n\n</think>` boş bloklar).
ADR-0040 *"izsiz veriyle eğitmek yeteneği aktif bastırır"* diye korkuyordu — **ölçümde tersi çıktı.**
RAFT eğitimi modele **kararlı bir prosedür** verdi (önce kaynağı seç → sonra alıntıla → sonra atıf
ver) ve döngünün beslendiği kararsızlık ortadan kalktı. → *"reçete fazla sertti, `τ_g` v2 gerekir"*
hipotezi **desteklenmedi**; v2'nin diğer dört gerekçesi ([`kollar.md`](../kollar.md)) yerinde duruyor.

**Ek gözlem — asimetri:** iz **8/8 İngilizce**, cevap **8/8 Türkçe**. Eğitim cevap kanalını
Türkçeleştirmiş, düşünce kanalına dokunmamış. İzler ürün yüzeyinde görünecekse (kullanıcı kararı,
ADR-0043) bu bir **eğitim hedefi** hâline gelir.

---

## 6. 🚨 Bulgu 5 — yeni sessiz bozulma: 900-kar klip numaralı listeyi ortadan kesiyor

`τ_g`'nin tek başarısız örneği (yukarıda #2) düşünce arızası **değil**: düşünce izi kusursuzdu
(9 satır, doğru kaynağı seçmiş). Bozulan **cevap**:

Eval-aynası klipi (900 kar) KAYNAK 3'ü (CMK m.153) **numaralı suç listesinin ortasında** kesmiş —
kaynak bloğu literal olarak `"…Karşı Suçlar (madde 309, 310, 311,"` ile bitiyor. Model *"maddeyi
birebir alıntıla"* talimatı altında yarım kalan diziyi **kendisi sürdürüyor**: `…1682, 1683, 1684`
diye 8192 token sınırına kadar. Cevabın ilk %12.3'ü sağlıklı, gerisi çöp.

**Neden tehlikeli:** hata yok, cevap dolu, hakem onu puanlar. Ve **satır-bazlı döngü metriği
kaçırıyor** (2 satır, 8.625 karakter). Yakalayan tek şey `finish_reason='length'` sayacı.

**Yeni mi?** Sprint 1'in thinking-off `τ_g` koşusunda **0/80** kesik vardı (512 token bütçe) —
yani bu davranış düşünce açıkken ve büyük bütçede ortaya çıkıyor.
→ `yurutme-tuzaklari.md` **1.9** olarak kayda geçti.

---

## 7. Çözüm — **bütçeli düşünce** (zorunlu kapatma)

Model kendi durmuyorsa **biz durdururuz.** İki geçiş:

1. Düşünceye **N token** izin ver (sohbet API'si, `enable_thinking=true`)
2. `content` boş döndüyse: `/apply-template`'in ürettiği **ham istem** + üretilen iz + `</think>\n\n`
3. `/completions` ile devam ettir → model o noktadan sonra **cevabı yazmak zorunda**

Sohbet API'si mid-mesaj devam ettiremediği için ikinci geçiş metin-tamamlama uç noktasından gider.
Kod: `gen_eval_grounded.py` → `--think-budget N` · `render_prompt()` · `GenOut(…, forced_close)`.
Detay çıktısına `completion_tokens` ve `forced_close` alanları eklendi.

**Doğrulama (base, Q4_K_M, `--think-budget 1024 --max-new-tokens 512`, M1, n=2):**

| örnek | zorla kapatıldı | token | cevap |
| :-- | :--- | ---: | :--- |
| 0 | ✅ | 1.081 | *"…Verilen kaynaklarda bu konuyu düzenleyen madde bulunmuyor."* (tutarlı red) |
| 1 | ✅ | 1.315 | 3 maddelik atıflı analiz — `[KAYNAK 2] Madde 285` / `[KAYNAK 3] Madde 286` |

**Kesilmiş düşünceden çöp çıkmıyor** — cevaplar tutarlı, atıflı, biçimli. Bu ölçümü üretilebilir
kılan tek yol; ve ürün tarafında zaten gerekli (tüketici donanımında sınırsız düşünme yok).

---

## 8. Maliyet ekseni (ADR-0017)

`completion_tokens` artık her satırda kayıtlı. Ölçülenler:

| kip | token/cevap | referansa oran |
| :--- | ---: | ---: |
| thinking **off** (Sprint 1) | **249** | 1× |
| bütçeli düşünce 1024+512 (base) | **~1.198** | **~4.8×** |
| `τ_g` v1, doğal sonlanma | **~463** | **~1.9×** |
| thinking on, bütçesiz — M3 | 1.126 | 4.5× |
| thinking on, bütçesiz — M4 | 3.932 | **15.8×** |
| thinking on, `temp 0.6`, sonlanan tek örnek | 6.918 | **27.8×** |

→ Maliyet-normalize parite muhasebesine **bu satırlar** girer. Ayrıca dikkat: `τ_g` base'in
bütçesinin **yarısından azını** harcıyor — düşünce maliyeti de kolla düşüyor.

---

## 9. ADR-0040'ın ön-kayıtlı kuralına ne oldu

Kural üç sayı istiyordu (M2 Rej · M1 kütle · M5 ezber kütlesi) ve **üçü de üretilemedi.**
Geçerlilik ön şartı *"kesik > %5 → bütçeyi artır, tekrarla"* diyordu; bütçe 8× artırıldı, sonuç
değişmedi — çünkü **kesilme değil sonlanmama**. Kural bu dalı öngörmemişti.

**Sonuç 🟢/🟡/🔴 değil — "ölçüm bu kipte üretilemiyor" + mekanizma.** Kararın kendisi
[ADR-0043](../../adr/0043-dusunce-modu-acik-butceli-kapatma.md)'te: düşünce modu **AÇIK**, bütçeli
kapatma ile — ve bu karar **ölçümle değil, ürün gereksinimiyle** alındı (kullanıcı: *"final model
think edebiliyor ve token'ları okunabiliyor olmak ZORUNDA"*). Ön-kayıtlı 🟢🟡🔴 kuralı bütçeli
kipte **yeniden koşulacak** ve sonucu raporlanacak; kararı değil, **RS-FT'nin gerekliliğini**
belirleyecek.

---

## 10. Paper eşlemesi

- **Negatif/şaşırtıcı bulgu (birinci sınıf)** — §3: düşünen bir SLM, çekimserlik talimatı içeren
  RAG isteminde greedy decoding altında **sonlanmıyor**; kuantizasyondan ve bütçeden bağımsız.
- **Results / iç iddia** — §5: **ince-ayar akıl yürütmeyi stabilize etti.** Kol, base'in
  yapamadığını yapıyor (35/36 sonlanma, %2.7'lik iz maliyeti). Merge iddiasının yanında duran,
  planlanmamış ama ölçülmüş bir yan sonuç.
- **Methodology** — §7: bütçeli düşünce protokolü (zorunlu kapatma), ön-kayıtlı bütçe ve rejim
  değişmezi olarak kaydı.
- **Limitations** — §5 iz dili (İngilizce iz ↔ Türkçe cevap) · §6 klip artefaktı · n küçük
  (1-8 örnek, mekanizma tespiti; kapı ölçümü değil) · `runs=1`.

---

## 11. Sonraki

1. **Sprint 1'in üç çıpası yanlış protokolde kaldı.** base · Gemini 3.1 FL · `τ_g` v1 hepsi
   `--thinking off` ile ölçüldü. Hat thinking-on'a geçtiğine göre `τ_a`'nın referans noktası
   0.6330 **değil**; üçü de bütçeli kipte yeniden koşulmalı (**1.410 cevap**, GPU $0 yerel,
   Gemini + hakem ≈ **$0.5-0.6**).
2. **CP0-a/CP0-b bütçeli kipte tam n ile koşulacak** — yerelde uzun sürdüğü için **Modal**'a
   taşınıyor; taşıyıcı **değişmeden** (aynı llama.cpp + aynı GGUF + aynı bayraklar, tuzak 1.7).
3. **Türkçe iz** bir eğitim hedefi olarak masada — kararı ölçüm sonrası, `τ_g` v2'nin diğer üç
   gerekçesiyle **birlikte** verilecek ([`kollar.md`](../kollar.md)).
