# ADR-0053 — Modül-başına norm kapsamı **reddedildi**: gerekçe çürüdü, ölçüm de geçmedi

- **Tarih:** 2026-08-04
- **Durum:** kabul edildi
- **İlgili:** [ADR-0036](0036-tau-norm-asimetrisi-ve-norm-dengeli-merge.md) ·
  [ADR-0052](0052-merge-norm-dengeleme-hukmu-tersine.md) (hüküm: ana sonuç **ham TIES**)
- **Kaynak ölçüm:** [research_log #50](../record/research_log/2026-08-04-modul-basina-norm.md)
- **Kapatır:** `sprint3-part1.md` Adım 0 · `open_questions.md`'deki *"modül-başına normalizasyon"* açık sorusu

## Bağlam

`merge_ties.py`'nin normalleştirme **kapsamı** globaldi (tüm `τ` için tek `‖τ‖_F`) ve bu,
ADR-0036 metnindeki `τ/‖τ‖` ifadesinin birebir okunuşuydu. Modül-başına kapsam
**alınmamış bir alternatif** olarak açık soruda duruyordu.

`sprint3-part1.md` Adım 0'ın gerekçesi şuydu:

> Merge'in bilinen kusuru: `τ_a` seyreliyor (tekil 0,987 → merge 0,877). İki kolun da en
> büyük normu **aynı MLP yüzeyinde** — `gate_proj` (τ_g 6,150 ↔ τ_a 0,621) · `up_proj`
> (5,047 ↔ 0,628). **Global norm bunu göremiyor.**

**Kabul ölçütü (ön-kayıtlı):** M2b > 0,877 **ve** M1 kütlesi ≥ %71,6 — ikisi birden.

## Ölçüm

### 1. Gerekçe çürüdü (bedava, ağırlık okunmadan)

Kolların **modül profilleri neredeyse orantılı**. `τ_g/τ_a` oranı 11 yüzeyin hepsinde
**7,18 – 10,08** arasında; global normalleştirmeden sonra iki kolun modül payları zaten
eşitleniyor:

| modül | ‖τ_g‖ | ‖τ_a‖ | oran | global norm sonrası τ̂_a/τ̂_g |
| :--- | ---: | ---: | ---: | ---: |
| gate_proj | 6,1504 | 0,6208 | 9,91 | **0,90** |
| up_proj | 5,0471 | 0,6276 | 8,04 | **1,10** |
| in_proj_qkv | 4,2924 | 0,4948 | 8,68 | **1,02** |
| down_proj | 2,7384 | 0,3378 | 8,11 | **1,09** |
| v_proj *(uçtaki)* | 0,7480 | 0,1042 | 7,18 | **1,24** |
| in_proj_a *(uçtaki)* | 0,3056 | 0,0303 | 10,08 | **0,88** |

Yani `τ_a` bir **kapsam artefaktı** yüzünden silinmiyor. Global norm *"bunu göremiyor"*
önermesi ölçümde durmuyor: profil orantılı olduğu için global norm onu zaten görüyor.

### 2. Ama kapsam değişikliği no-op da değil (ağırlık uzayında)

İki merge üretildi (aynı kollar, aynı `--geri-olcek min`, tek fark kapsam):

```
‖W_modül − W_global‖ / ‖W_global − base‖ = 0,272     ← yön %27 farklı
‖W_modül − base‖ = 1,3835   ‖W_global − base‖ = 1,3865   ← genlik AYNI (%0,2)
```

Fark TIES'in **doğrusal-olmayan** işaret seçiminden geliyor. Bu yüzden karar akıl
yürütmeyle kapatılmadı, eval koşuldu.

### 3. Eval — kabul ölçütü DÜŞTÜ

`tg_ta_modulmin` → Q4_K_M → llama-server, rejim değişmezleri sabit (thinking on ·
1024+512 · seed 3407 · chunk 900 · CTX 8192). Geçerlilik kapısı **geçildi** (kesik %1,2).

```
cevaplanan 45/80  →  coverage %56,2
kütle = coverage × A1  ≤  %56,2      (A1 = 1,000 olsa BİLE)
gereken                   ≥ %71,6
```

🔴 **Kütle ayağı, A1 hakeme hiç gitmeden düştü.** Karşılaştırma:

| varyant | cevaplanan | A1 | **kütle** | M2b red |
| :--- | ---: | ---: | ---: | ---: |
| `ham` = yayınlanan `tgta_v1` | 63/80 | 0,909 | **%71,6** | 0,877 |
| `min` (global norm-dengeli) | 43/80 | 0,994 | **%53,4** | 0,987 |
| **`modulmin` (bu ADR)** | **45/80** | ölçülmedi | **≤ %56,2** | ölçülmedi |

Modül-başına kapsam, global `min`'in davranışını **tekrarladı** (43 → 45 cevap). %27'lik
yön farkı aşırı-reddi kurtarmadı — çünkü aşırı-reddi yaratan şey **yön değil genlik**:
her iki kapsamda da `τ_g` kendi eğitim genliğinin ~1/9'una iniyor ve zeminleme zayıflıyor.

## Karar

**Modül-başına norm kapsamı REDDEDİLDİ.** `HakHukuk-4B-v0.1` (`tgta_v1`, ham TIES)
yerinde kalıyor. ADR-0052'nin hükmü sağlam: ana sonuç ham TIES.

`--norm-kapsam {global,modul}` bayrağı **kodda kalıyor** — reddedilen alternatifin
tekrar ölçülebilir olması bu repoda kayıt değeri taşıyor; varsayılan `global`.

## Sonuçlar

- ✅ `sprint3-part1.md` Adım 0 kapandı 🔴; sprint'in ağırlığı harness'a (Adım 1-4) kayıyor.
- ✅ `open_questions.md`'deki modül-başına sorusu **kapandı** — açık soru değil, ölçülmüş red.
- ⚠️ `τ_a`'nın merge'de seyrelmesi (0,987 → 0,877) **hâlâ açık**. Bu ADR onu norm
  kapsamının çözmediğini gösteriyor; çözüm başka yerde (trim eşiği · λ · farklı operatör ·
  ya da `τ_a`'yı daha yüksek genlikte eğitmek) aranmalı.
- 💰 Hakem maliyeti **$0**. Kabul bir **VE** koşulu olduğu için önce düşmesi beklenen eksen
  (kütle) koşuldu ve regex tabanlı coverage, A1 hiç ölçülmeden kararı verdi. Bu sıralama
  genel kural olarak kaydedilmeye değer: **bileşik kabul ölçütünde önce en ucuz ve en
  kırılgan ayağı ölç.**

## Reddedilen alternatifler

- **Yine de m2b/m2 koşup tam satırı doldurmak** — kütle tavanı ölçütün altında olduğu için
  sonuç değişmezdi; ön-kayıtlı disiplin *"geçersiz/düşmüş koşuya para harcanmaz"* diyor.
- **`--geri-olcek` kuralını modül-başına ayrı süpürmek** — genlik sorunu kapsamdan bağımsız
  (§3), süpürme aynı duvara çarpardı. `ortalama` zaten ölçülüp dejenere olmuştu (#48 §21).
