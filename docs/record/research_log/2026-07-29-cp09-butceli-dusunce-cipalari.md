# #43 — CP0.9: üç çıpa bütçeli düşünce kipinde · anti-hedef ekseni 3.4× yanlış ölçülüyormuş

**Tarih:** 2026-07-29 · **Checkpoint:** `sprint2.md` CP0.9 · **GPU:** yerel RTX 5070 Ti ($0) ·
**Karar belgeleri:** [ADR-0043](../../adr/0043-dusunce-modu-acik-butceli-kapatma.md) (protokol) ·
[**ADR-0044**](../../adr/0044-mod-duyarli-feragat-kurali.md) (bu turda doğdu)
**Betikler:** `cp0_thinking_gen.sh` · **`cp09_gemini_gen.sh`** (yeni) · `cp0_thinking_score.sh` ·
**`watch_cp09.sh`** (yeni)
**Çıktılar:** `outputs/eval/cp09-butceli-1024-512/` (künye: `KUNYE.json`)

---

## Neden koşuldu

ADR-0043 protokolü değiştirdi (thinking AÇIK, bütçeli zorunlu kapatma). Sprint 1'in üç çıpası
`--thinking off` ile ölçülmüştü → **hiçbiri artık çıpa değil**. `τ_a` bunlara karşı ölçülürse
ARA KAPI yanlış okunur.

## Künye — rejim değişmezleri

| | |
| :--- | :--- |
| Havuz | DEV (`data/eval/dev/`, 80 core_hard + 70 trap) · TEST hâlâ **görülmedi** |
| n | 80/80/70/80/80/80 = **470 cevap × 3 özne = 1.410** |
| Düşünce | **1024** tok, zorunlu kapatma · cevap **512** tok (ADR-0043, ön-kayıtlı) |
| Diğer | seed **3407** · `--max-chunk-chars 900` · temp 0 |
| Taşıyıcı | base/`τ_g`: Q4_K_M GGUF + `llama-server` (`-c 8192`, KV q8_0) — Sprint 1 ile aynı (tuzak 1.7) |
| Rakip | `google/gemini-3.1-flash-lite` @ OpenRouter, provider **Google AI Studio** pinli |
| Güç | şarjda (tuzak 1.6) |

**Rakip tarafı düşünce bütçesi — yeni karar.** `sprint2.md` bunu parantezde bırakmıştı. ADR-0043
m.3 bütçeyi *"bütün rakipler"* için rejim değişmezi ilan ettiğine göre Gemini de **1024+512**
koşar: bizde istemci-taraflı zorunlu kapatma (`--think-budget`), rakipte sunucu-taraflı
(`reasoning.max_tokens`, `gen_eval_grounded.py --reasoning-budget`). Rakibi düşüncesiz koşmak
sapmayı **bizim lehimize** kaydırırdı (tuzak 2.2 sınıfı). `reasoning_tokens` künyeye yazılır —
Google izi **metin olarak vermiyor**, yalnız token sayısı; karakter sayacıyla aynı alana yazmak
sessiz yanlışlık üretirdi, bu yüzden ayrı alan.

## Geçerlilik kapıları — üçü de geçti

| özne | n | kesik | ort tok | zorunlu kapatma |
| :--- | --: | --: | --: | --: |
| base | 470/470 | 17 (**%3.6**) | **1135** | 445/470 |
| `τ_g` v1 | 470/470 | 17 (**%3.6**) | **772** | 209/470 |
| Gemini 3.1 FL | 470/470 | 0 (**%0.0**) | **543** | — (sunucu bütçesi) |

Düşünce kanalı **470/470** kullanıldı (üç öznede de) — `enable_thinking` işledi.

---

## Bulgu 1 ⭐ — Anti-hedef ekseni **3.4× yanlış** ölçülüyormuş (ADR-0044)

Zorunlu ön adım rakip ailesi için red-regex kalibrasyonuydu. Rakip tarafı **temiz çıktı**
(190 yakalanmayan Gemini cevabının hiçbiri red değil, m3'te 0/80 kaçak). Ama ileri yön denetimi
başka bir şey buldu:

**Kör mod (M5) tek başına `SYSTEM_PROMPT`u kullanır ve o istem feragat cümlesini EMREDER**
(*"…bir avukata danışmanızı öneririm dersin"*). `REJECT_RE` o cümleyi red kalıbı sayıyordu →
model dolu cevap verip sonuna feragati ekleyince **çekinmiş** sayılıyordu.

| dosya | RED etiketli | yalnızca feragat | gerçek red |
| :--- | --: | --: | --: |
| `m5_base` (off) | 50/80 | **45** | 5 |
| `m5_base_th` | 56/80 | **54** | 2 |
| `m5_tg` (off) | 51/80 | **50** | 1 |
| `m5_gem_th` | 62/80 | **58** | 4 |

Feragatli cevapların **medyan uzunluğu 1082 karakter**, içerikleri dolu — üstelik sık sık uydurma
(base bir Türk hukuku sorusuna *"İsviçre Medeni Kanunu 1. madde"* diyip feragati ekliyor, eski
kural bunu **red** sayıyor).

**Düzeltilmiş Kapı 6 çıpası** (thinking-off verisi, **hakem çağrısı yapılmadan** — `gnd_m5_*.jsonl`
zaten 80 satırın hepsini taşıyordu):

| özne | eski cov | eski A1 | eski kütle | yeni cov | yeni A1 | **yeni kütle** |
| :--- | --: | --: | --: | --: | --: | --: |
| base | 37.5% | 0.285 | 10.7% | 93.8% | 0.394 | **36.9%** |
| `τ_g` v1 | 36.2% | 0.402 | 14.6% | 98.8% | 0.448 | **44.2%** |
| Gemini | 23.8% | 0.621 | 14.8% | 98.8% | 0.578 | **57.1%** |

**Üç sonuç:**
1. Sapma **bizim lehimizeydi** — anti-hedefte küçük görünmek işimize gelirdi.
2. `τ_g`'nin ihlali **artefakt değil, büyüdü**: base'e fark +3.9 → **+7.3 puan**.
3. Hata **rastgele değil**: A1 düzeltmeden sonra *yükseldi* (base 0.285→0.394) — dışlanan dilim
   sayılandan daha sadıkmış, yani paydayı da payı da kaydırıyordu.

**Etki alanı yalnız M5** — diğer beş modda altı dosyanın hiçbirinde tek satır kaymadı; ARA KAPI'nın
M2 ekseni etkilenmiyor.

> **Paper eşlemesi:** Methodology (hakemsiz omurganın kalibrasyon protokolü) + Limitations
> (anti-hedef ölçütü bir kez yanlış sayıldı, düzeltildi, iki sürüm de raporlanıyor).

## Bulgu 2 ⭐ — Sonlanma kararlılığı **eğitim istemi ailesine özgü**

CP0 (#42) n=36'da *"`τ_g` düşünüyor ve duruyor, ince-ayar akıl yürütmeyi stabilize etmiş"*
demişti. n=470'te bu **yalnız kendi istem ailesinde** doğru:

| istem ailesi | modlar | base zorla | `τ_g` zorla | ort tok base→`τ_g` |
| :--- | :--- | --: | --: | :--- |
| **RAG_MULTI** ← `τ_g`'nin eğitim biçimi | m1 · m2b · m3 | %91.7 | **%5.8** | 1098 → **476** |
| RAG_tek | m4 · m2 | %96.7 | %79.3 | 1116 → 1046 |
| BLIND | m5 | %100.0 | %95.0 | 1284 → 1146 |

Kendi ailesinde etki muazzam (zorunlu kapatma **%91.7 → %5.8**, token **yarıya iner**); dışında
marjinal. CP0'ın örneklemi o aileden geldiği için genel bir kazanç gibi görünmüştü.
`kollar.md`'deki not bu kırılımla düzeltildi.

> **Paper eşlemesi:** ablasyon (ince-ayarın kazandırdığı şey **dağılım-içi**) + Limitations
> (dağılım-dışı sonlanma hâlâ protokol müdahalesine muhtaç).

## Bulgu 3 — Maliyet ekseni rakibin lehine

`base 1135` · `τ_g 772` · `Gemini 543` tok/cevap. Rakip 1024'lük bütçeyi **doldurmuyor** (ort 444
düşünce token'ı) ve kendi duruyor. Base rakibin **2.09 katı** token harcıyor; `τ_g` bunu 1.42'ye
indiriyor. ADR-0017 maliyet-normalize parite muhasebesine bu üç sayı girer.

## Bulgu 4 — base n=3'te sonlanıyor görünüyordu, n=80'de sonlanmıyor

CP0 M4'te 3/3, M3'te 3/3 *"kendi kapatıyor"* demişti. n=80'de M4 **76/80 zorla**, M3 **60/80**.
Yani sonlanmama belirsizliğe özgü bir kenar durum değil, base'in bu istem ailelerindeki **genel
davranışı** — ADR-0043'ün bütçeli kapatma kararı n=3'te göründüğünden **daha zorunluymuş**.

> **Yeni tuzak:** n=3 smoke, n=470'i temsil etmiyor. `yurutme-tuzaklari.md`'ye satır eklendi.

---

## Puanlama sonuçları

Hakem: `gpt-4o-mini` · OpenAI-direct · gateway PİNLİ · `runs=1` · **maliyet $0.447** (+ ablasyon $0.046 = **$0.492**).
Tablo `scripts/cp09_tablo.py` ile **dosyalardan** üretilir (elle kopyalama yok).

| ölçüt | yön | base off | **base bütçeli** | `τ_g` off | **`τ_g` bütçeli** | Gemini off | **Gemini bütçeli** |
| :--- | :-: | --: | --: | --: | --: | --: | --: |
| **M1** sadık-cevap kütlesi % | ↑ | 42.6 | **56.7** | 72.0 | **71.4** | 74.2 | **72.9** |
| M1 coverage % | · | 43.8 | 57.5 | 85.0 | 82.5 | 76.2 | 76.2 |
| M1 A1 | ↑ | 0.973 | 0.986 | 0.847 | 0.866 | 0.973 | 0.956 |
| **M4** oracle kütlesi % | ↑ | 93.1 | 95.9 | 94.3 | 94.7 | 95.5 | 93.7 |
| **M2** Rej (LLM) | ↑ | 0.633 | **0.814** | 0.458 | **0.873** | 0.842 | **0.930** |
| M2 geçerli tuzak (payda) | · | 60 | 59 | 59 | 55 | 57 | 57 |
| M2 fabrikasyon | ↓ | 0.367 | 0.186 | 0.542 | 0.127 | 0.158 | 0.070 |
| **M2b** Rej (LLM) | ↑ | 0.973 | 0.986 | 1.000 | **0.607** 🔴 | 0.970 | 1.000 |
| **M3** Rej (LLM) | ↑ | 1.000 | 1.000 | 1.000 | 0.923 | 1.000 | 1.000 |
| **M5** ezber kütlesi % *(ANTİ-HEDEF)* | ↓ | 36.9 | 42.5 | 44.2 | **39.2** | 57.1 | 54.4 |
| **ort token/cevap** | ↓ | — | 1135 | — | **772** | — | 543 |
| zorunlu kapatma % | · | 0 | 94.7 | 0 | 44.5 | 0 | 0 |

*(off sütununda token yok — o alan Sprint 1'de kaydedilmiyordu. M5 satırları her iki protokolde
de ADR-0044 kuralıyla.)*

> ⚠️ **ÇELİŞKİ İŞARETİ (2026-07-30, [#45](2026-07-30-cp2a-hakem-capalanmasi.md)).** Bu tablodaki
> **M2 / M2b / M3 Rej** satırlarının paydası (`valid_trap`) hakem tarafından **özne başına yeniden
> yargılanıyor** ve hakem o öznenin cevabını görüyor → payda özneye bağlı. Aynı 80 M3 kaleminde
> `valid_trap` = base 54 · Gemini 56 · `τ_g` **39**. **M3'te bağlam boş** olduğundan doğru payda
> tanım gereği **80/80**'dir; dolayısıyla bu satırın doğru okunuşu base **1.000** · Gemini **1.000**
> · `τ_g` **0.800** — yukarıdaki **0.923 fazla iyimser.** M2/M2b satırları da aynı kusuru taşıyor
> (filtresiz: M2 base 0.786 · `τ_g` 0.800 · Gemini 0.814 — M2b base 0.950 · `τ_g` 0.525 ·
> Gemini 0.850). Sapma tek yönlü değil: M2b'de aleyhimize ~7p, M3'te lehimize ~12p.
> **ADR-0040'ın 🟡 hükmü değişmiyor** — M2 eşiği filtresiz de geçiliyor (0.786 ≥ 0.78).
> Sayılar düzeltilmeden **üzerine yazılmadı**; düzeltme kararı ADR-0048'e bağlı.

### ADR-0040 hükmü: **🟡 SARI** — muhafız düştü, eşik geçti

| ölçüt | ref (off) | bütçeli | eşik | sonuç |
| :--- | --: | --: | :--- | :--- |
| M2 Rej (LLM) | 0.633 | **0.814** | ≥ 0.78 | ✅ geçti (+18.1p) |
| M1 kütle | %42.6 | **%56.7** | ≥ %57.6 | ❌ 0.9 puan kaldı (+14.1p) |
| M5 ezber kütlesi | %36.9 *(ADR-0044)* | **%42.5** | ≤ ref | ❌ **İHLAL** (+5.6p) |

Hüküm **ADR-0044'ten bağımsız olarak sağlam**: muhafız hem eski (10.7) hem düzeltilmiş (36.9)
referansta ihlal ediliyor. → **RS-FT Sprint 2 kapsamına GİRMİYOR**, ADR-0035 açılmıyor, plan
değişmiyor. Düşünce artık **raporlanan bir eksen**: kazancı (tuzak reddi +18.1p, fabrikasyon
yarıya) ve bedeli (ezber +5.6p, token 4.5×) tabloda yan yana durur.

> ⚠️ **Ön okumam yanlış gerekçeyle doğru çıktı.** 🟡 tahmin etmiştim ama M2 bacağının düşeceğini
> sanarak: Sprint 1'e bakıp regex→LLM farkını +13.3 puan varsaymıştım, gerçekte **+20.4 puan**
> (regex 0.61 → LLM 0.814). M1 bacağının aritmetik tavanı (%57.5) doğruydu. Hükmü belirleyen
> M5 muhafızı oldu.

### Bulgu 5 ⭐ — Düşünce **ayırt etme yeteneğini** artırıyor, biçim yanlılığı değil

M2'de 11 `FABRICATE→ABSTAIN` kazancı, 2 ters kayıp (n=57 ortak geçerli tuzak). Cevaplar
kaynak-yeterliliği beyanıyla açılma oranı %54.3 → **%72.9**, ortalama uzunluk 416 → **300** karakter.

İki mekanizma aday: **(A)** muhakeme gerçekten kaynağı soruyla karşılaştırıyor · **(B)** zorunlu
kapatma şablonu reddi kolaylaştırıyor. Bu koşu ikisini **ayıramaz** — 70 örneğin 69'u zorla
kapatıldı (düşünce izi ort. 3927 karakter, bütçe doldu), kendi duran kontrol grubu **1 örnek**.

**Ama (B) tek başına elendi:** aynı protokol M1'de **ters yöne** gidiyor — red %56.2 → %42.5, yani
cevaplamanın doğru olduğu yerde model **daha çok cevaplıyor**. Saf bir şablon yanlılığı iki
eksende zıt yönde hareket üretemez. Bedeli: m2'de 249 → 1116 token (**4.5×**).

> **Paper eşlemesi:** Results (düşünce ekseni) + Limitations (düşünce ↔ zorunlu kapatma bu
> tasarımda ayrılamıyor; ayrım ancak izli veriyle eğitilmiş, kendi duran bir kolda ölçülebilir).

### Bulgu 5-b ⭐ — Ablasyon: kazanç **biçimden gelmiyor** (koşuldu, $0.046)

Bulgu 5'in (B) şıkkı ayrıca test edildi: sistem istemine *"cevabına başlamadan önce kaynağın
soruyu cevaplayıp cevaplamadığını belirt"* satırı eklenip **thinking-off** koşuldu
(`--sufficiency-preamble`, `outputs/eval/cp09-ab-ayrimi/`). Amaç: düşüncenin ürettiği **biçimi**
muhakeme olmadan taklit etmek.

| kol | M1 kütle ↑ | M1 coverage | M2 Rej ↑ | ort token |
| :--- | --: | --: | --: | --: |
| base thinking-off | 42.6% | 43.8% | 0.633 | ~249 |
| base **bütçeli düşünce** | **56.7%** | 57.5% | **0.814** | 1116 |
| base **önsöz + thinking-off** | **28.2%** 🔴 | 31.3% | **0.968** | **116** |

Önsöz M2'de 0.968'e çıkıyor — düşünceden de, Gemini'den de yüksek — ama **aşırı-red oranı 0.6875**:
M1'de cevaplaması gereken 80 sorunun yalnız 25'ini cevaplıyor ve base'in kendi thinking-off
hâlinden **14.4 puan** geriye düşüyor.

**Ayrım tamamlandı:**
- **Önsöz** tek eksende kaydırıyor — M2'de +33.5p alırken M1'de −14.4p veriyor. Bu ayırt etme değil,
  **red eşiğini indirmek**; kesinlik/kapsam ödünleşmesinde başka bir çalışma noktası.
- **Bütçeli düşünce** iki ekseni **aynı anda** yukarı taşıyor (M1 42.6→56.7 **ve** M2 0.633→0.814).
  Bir eşik kaydırması tanım gereği bunu yapamaz.

→ **Mekanizma (A) doğrulandı: düşünce gerçekten ayırt etme yeteneğini artırıyor, 4.5× token'ın
karşılığı var.** İkincil sonuç: `τ_a`'nın işi de bir istem satırıyla yapılamaz — **kör red ucuz,
ayırt etme pahalı.**

⚠️ Şerh: paydalar farklı (`valid_traps` 62 / 59 / 60 — tuzak 2.6) · `runs=1` · önsöz bir
**ablasyon kolu**, ana tabloya girmez (`--sufficiency-preamble` künyeye uyarı basar).

> **Paper eşlemesi:** Results — "düşünce mi biçim mi" sorusunun ölçülmüş cevabı; prompt-mühendisliği
> alternatifinin **elenmiş** olması iddiayı güçlendirir.

### Bulgu 6 ⭐ — `τ_g`'nin üç negatifinden ikisi bütçeli kipte **kapandı**, yerine yenisi doğdu

`sprint2.md`'nin açılış tablosu thinking-off'tan geliyordu:

| negatif | thinking-off | **bütçeli** | durum |
| :--- | :--- | :--- | :--- |
| #2 tuzak reddi | 0.633 → **0.458** (base'in altında) | 0.814 → **0.873** (base'in üstünde) | ✅ **kapandı** |
| #3 parametrik sızıntı | 36.9 → **44.2** (base'i aşıyor) | 42.5 → **39.2** (base'in altında) | ✅ **kapandı** |
| #1 cevap başına hata (A1) | 0.973 → 0.847 | 0.986 → 0.866 | ⚠️ duruyor |
| **YENİ:** M2b (gold yok) | 0.973 → **1.000** | 0.986 → **0.607** | 🔴 **yeni açık** |

`τ_a`'nın ön-kayıtlı gerekçesi (#2) bütçeli kipte ortadan kalktı; kolun eksiği artık *"tuzağı
reddet"* değil **"kaynak yokken sus"**. Üstelik yeni açık tam olarak `τ_g`'nin eğitim ailesinde
(RAG_MULTI) — kendi dağılımında hem en iyi (M1 kütle, kendi kendine kapanma) hem en kırılgan.

### ARA KAPI'nın eşikleri — formül ön-kayıtlı, sayı artık belli

`sprint2.md`: `M2 Rej ≥ base + 12 puan` · `M1 A1 ≥ 0.90 × base`.

| | eski (off) | **yeni (bütçeli)** |
| :--- | --: | --: |
| eşik (M2 Rej) | 0.75 | **0.934** |
| muhafız (M1 A1) | 0.876 | **0.888** |

⚠️ **Tavan riski, şimdi kayda geçiyor:** base geçerli 59 tuzağın 48'ini zaten reddediyor; +12 puan,
kalan 11 hatanın **7'sinin** düzeltilmesi demek — tavana 6.6 puan kala. `τ_a` bu kapıda kalırsa
sebebi kolun kötülüğü değil **base'in tavana yakınlığı** olabilir; kapı ölçmek için kurulduğu şeyi
ölçemez hâle gelir (Kapı 5'in ADR-0039'da başına gelen şey). Sayı ön-kayıtlı formülden geldiği için
**değiştirilmedi**.

### Kapı 6'nın bütçeli-kip çıpası

base: M5 coverage **%97.5** · ezber kütlesi **%42.5**. (ADR-0044'ün thinking-off çıpası %93.8 /
%36.9 idi.) Bugün `τ_g` bu kapıyı **geçiyor** (39.2 < 42.5), base geçemiyor — kapı base'e göreceli
tanımlı olduğu için bu bir çelişki değil.

### Bulgu 7 — CP2'nin hasat verimi yarıya indi

`rejected` havuzu modelin tuzağa **düştüğü** cevaplardan hasat ediliyor; base'in fabrikasyon oranı
**0.367 → 0.186**. Aynı havuz için kabaca **iki katı örnek** gerekecek, üstelik cevap başına 4.5×
token. CP2 *"$0 ama süre gerektirir"* diye planlanmıştı — süre tahmini ~4× yukarı.
