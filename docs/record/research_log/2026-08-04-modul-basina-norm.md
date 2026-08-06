# #50 — Adım 0: modül-başına norm kapsamı 🔴 · gerekçe çürüdü, kütle ekseni kararı $0'a verdi

**Tarih:** 2026-08-04 · **Sprint:** [`sprint3-part1.md`](../../_arsiv/sprint3-part1.md) Adım 0 ·
**Karar:** [ADR-0053](../../adr/0053-modul-basina-norm-kapsami-reddedildi.md)
**Bedel:** GPU yerel (bedava) · **hakem $0** · **Çıktılar:** `outputs/eval/cp3f-modul-norm/`

> **Soru:** Merge'de `τ_a` seyreliyor (tekil M2b 0,987 → merge 0,877). Normalleştirmenin
> **kapsamı** global (tek `‖τ‖_F`). Modül-başına kapsam bunu düzeltir mi?
> **Ön-kayıtlı kabul:** M2b > 0,877 **ve** M1 kütlesi ≥ %71,6 — ikisi birden.

## 1. Önce bedava kısım: gerekçe ölçümde durmuyor

Adım 0'ın metni şöyleydi: *"iki kolun da en büyük normu **aynı MLP yüzeyinde** —
`gate_proj` (τ_g 6,150 ↔ τ_a 0,621) · `up_proj` (5,047 ↔ 0,628). **Global norm bunu
göremiyor.**"*

Kayıtlı norm kırılımından (`outputs/eval/cp3d-merge/KUNYE_tgta_v1.json`) okundu — hiçbir
ağırlık yüklenmeden:

| modül | ‖τ_g‖ | ‖τ_a‖ | oran g/a | **global norm sonrası** τ̂_a/τ̂_g |
| :--- | ---: | ---: | ---: | ---: |
| gate_proj | 6,1504 | 0,6208 | 9,91 | 0,90 |
| up_proj | 5,0471 | 0,6276 | 8,04 | 1,10 |
| in_proj_qkv | 4,2924 | 0,4948 | 8,68 | 1,02 |
| in_proj_z | 3,3024 | 0,3536 | 9,34 | 0,95 |
| down_proj | 2,7384 | 0,3378 | 8,11 | 1,09 |
| q_proj | 2,5327 | 0,2839 | 8,92 | 0,99 |
| o_proj | 1,2990 | 0,1666 | 7,80 | 1,14 |
| k_proj | 0,8326 | 0,0977 | 8,52 | 1,04 |
| v_proj | 0,7480 | 0,1042 | 7,18 | **1,24** |
| in_proj_a | 0,3056 | 0,0303 | 10,08 | **0,88** |
| in_proj_b | 0,2985 | 0,0303 | 9,84 | 0,90 |

**Kolların modül profilleri neredeyse orantılı** — oran 11 yüzeyin hepsinde 7,18-10,08.
Global normalleştirme, iki kolun modül paylarını **zaten eşitliyor** (0,88-1,24). Yani
*"global norm bunu göremiyor"* önermesi yanlış: profil orantılı olduğu için görüyor.
`τ_a` bir **kapsam artefaktı** yüzünden silinmiyor.

**Ders:** *"iki kolun da en büyük normu aynı yüzeyde"* gözlemi **tek başına** bir kapsam
sorunu kanıtlamıyor — kanıtlayan şey profillerin **orantısız** olması olurdu ve o
ölçülmemişti. Aynı sayıya bakıp farklı sonuç çıkarmak mümkündü; ayırt eden **oran sütunu**.

## 2. Ama kapsam değişikliği no-op da değil

Gerekçe çürüdü diye deney iptal edilmedi — bu repoda kararı ölçüm verir (ADR-0052'nin
kendisi *ölçümün bir reçeteyi tersine çevirmesiyle* doğdu). Önce ucuz bir ara kapı:
iki merge üretildi (aynı kollar, aynı `--geri-olcek min`, **tek değişken kapsam**) ve
ağırlık uzayında karşılaştırıldı.

```
‖W_modül − W_global‖              = 0,3772
‖W_global − base‖                 = 1,3865
‖W_modül  − base‖                 = 1,3835
GÖRELİ FARK = 0,3772 / 1,3865     = 0,272
```

**Yön %27,2 farklı, genlik aynı (%0,2).** Fark TIES'in doğrusal-olmayan işaret
seçiminden geliyor (katsayı oranları ±%20 oynayınca kolların dengede olduğu
parametrelerde işaret dönebiliyor). Yani deney gerçek — eval koşuldu.

## 3. Eval: kabul ölçütü 🔴 DÜŞTÜ — ve hakem hiç çağrılmadı

`models/merged/tg_ta_modulmin` → Q4_K_M (2.783.446.720 bayt, `tgta_v1` ile **birebir
aynı boyut**) → llama-server. Rejim değişmezleri sabit: thinking on · 1024 düşünce +
512 cevap · seed 3407 · chunk 900 · CTX 8192 · KV q8_0.

**Geçerlilik kapısı geçildi:** n=80, kesik **1** (%1,2 < %5), ort. completion 1105,0 tok,
düşünce kanalı 80/80, zorla kapatma 80/80.

Kabul bir **VE** koşulu ve genlik `min` ile aynı olduğu için düşmesi beklenen eksen
**kütle**ydi. Bu yüzden önce yalnız **m1** koşuldu; ve çekinme tespiti **regex tabanlı**
(`score_abstention.exact_reject`, hakem gerekmez):

```
cevaplanan 45/80  →  coverage %56,2
kütle = coverage × A1  ≤  %56,2        (A1 = 1,000 olsa BİLE)
gereken                   ≥ %71,6
```

**Kütle tavanı ölçütün 15,4 puan altında.** A1'i ölçmek sonucu değiştiremezdi → hakem
çağrılmadı, m2b/m2 üretimi koşulmadı. **Toplam hakem maliyeti: $0.**

| varyant | cevaplanan | A1 | **kütle** | M2b red |
| :--- | ---: | ---: | ---: | ---: |
| `ham` = yayınlanan `tgta_v1` | 63/80 | 0,909 | **%71,6** | 0,877 |
| `min` (global norm-dengeli) | 43/80 | 0,994 | **%53,4** | 0,987 |
| **`modulmin`** | **45/80** | ölçülmedi | **≤ %56,2** | ölçülmedi |

Modül-başına kapsam global `min`'i **tekrarladı** (43 → 45 cevap). %27'lik yön farkı
aşırı-reddi kurtarmadı — çünkü aşırı-reddi yaratan **yön değil genlik**: her iki kapsamda
da `τ_g`, kendi eğitim genliğinin ~1/9'una iniyor ve zeminleme zayıflıyor.

## 4. Sonuç ve kalan açık

**Modül-başına norm kapsamı reddedildi ([ADR-0053](../../adr/0053-modul-basina-norm-kapsami-reddedildi.md)).**
`HakHukuk-4B-v0.1` yerinde. `open_questions.md`'deki modül-başına sorusu artık **açık soru
değil, ölçülmüş red.**

⚠️ **`τ_a`'nın merge'de seyrelmesi hâlâ açık.** Bu tur onu norm *kapsamının* çözmediğini
gösterdi. Kalan adaylar: trim eşiği (`--trim-k`) · λ · farklı operatör (DARE/lineer) ·
ya da en doğrudan olanı — **`τ_a`'yı daha yüksek genlikte eğitmek** (82 adım @1e-5 çok
kısaydı; norm 1,18 bu yüzden küçük). Sonuncusu merge parametresi değil **eğitim**
parametresi ve muhtemelen doğru yer orası.

## 5. Genelleştirilebilir ders — bileşik kabul ölçütünde sıralama

Kabul `A ve B` biçimindeyse, **önce en ucuz ve düşmesi en muhtemel ayağı** ölç. Burada:
- kütle ayağı **regex** ile ölçülüyor (bedava), M2b ayağı **hakem** istiyor (paralı);
- ve önceki turdan (global `min`) kütlenin kırılgan eksen olduğu biliniyordu.

Sıralama tersine olsaydı: m2b hakemle ölçülür (~$0,3), muhtemelen 0,98 çıkar, *"bir eksen
geçti"* hissi doğar, sonra m1 koşulur ve zaten düşerdi. Aynı sonuç, artı para, artı
tek-eksenle-okuma riski. **Kütle ekseni burada sadece doğru cevabı değil, ucuz cevabı da
verdi.**

## Paper eşlemesi

**Negatif bulgu:** modül-başına normalizasyon reddi — hem gerekçesinin çürütülmesi hem de
ölçümün geçmemesi. **Methodology:** merge varyantlarını eval'e sokmadan önce **ağırlık
uzayında** ayırt etme kapısı (`‖W_a − W_b‖ / ‖W_b − base‖`) ve bileşik kabul ölçütünde
maliyet-sıralı ölçüm. **Limitations:** `τ_a`'nın seyrelmesi açık kalıyor.
