# Kol kaydı — her `τ_X` versiyonunun künyesi

> **Bu belge ne:** eğitilmiş her kolun (task-vector dalının) **tek kayıt yeri**. Bir artefakt
> diskte duruyorsa burada bir satırı vardır; satırı yoksa o artefakt **kimliksizdir ve kullanılmaz.**
>
> **Neden var:** bu hattın hata sınıfı sessiz yanlışlık. *"Bu sayı hangi kolun, hangi versiyonun
> sayısı"* sorusu **dosya adından** cevaplanabilmeli — o yüzden versiyon zincirin her halkasında
> taşınır: adaptör → merge → GGUF → eval etiketi.
>
> **Kural (2026-07-29):** repo dışı artefakt **yok**. Her şey repo kökü altında.
> Adaptörler git'te **değil** (`.gitignore: outputs/**/*.safetensors`, ayrıca 114 MB > GitHub'ın
> 100 MB dosya sınırı) ve **yedeklenmiyor** — bilinçli karar: adaptör veri + reçete + seed sabitken
> yeniden üretilebilir, yeri doldurulamaz varlıklar (veri · belgeler · eval çıktıları) zaten metin
> ve git'te. *(12B hattının adaptörleri bu kararın bedelini gösterdi: repo dışı devir paketi
> silindi, adaptörler kalıcı kayıp — kasıtlı, çünkü o hat emekli.)*

---

## ♻️ Yeniden üretilebilir artefaktlar — diskte tutulmaz (2026-08-03)

`models/merged/<ad>/` (bf16, ~8,8 GB/adet) **adaptör + base'den yeniden üretilir**:

```bash
python scripts/merge_lora.py --base Qwen/Qwen3.5-4B --adapter outputs/<kol> --out models/merged/<kol>
python scripts/merge_ties.py --base Qwen/Qwen3.5-4B --adapter tg=outputs/tg_v1 --adapter ta=outputs/ta_v1 \
       --no-norm-balance --out models/merged/tgta_v1     # ham TIES, ADR-0052
```

OSS geçişinde silinenler (~26 GB): `ta_v1` · `tg_ta_min` · `tg_ta_normdengeli` bf16
dizinleri. **GGUF'ları ve künyeleri duruyor** — ölçüm kaydı etkilenmedi.
Diskte tutulan: `tgta_v1` (yayımlanacak) · `tg_v1` (aktif kol).

**Asıl artefakt adaptördür** (`outputs/<kol>/`, ~114 MB) — o silinmez.

---

## Adlandırma

```
outputs/<kol>_v<N>/                      LoRA adaptörü        (asıl artefakt)
models/merged/<kol>_v<N>/                merge edilmiş bf16   (yeniden üretilebilir)
models/gguf/<kol>_v<N>-<QUANT>.gguf      taşıyıcıya giden     (yeniden üretilebilir)
eval etiketi: <mod>_<kol>_v<N>           ör. m1_tg_v1
```

**Kol kısaltmaları:** `tg` = `τ_grounding` · `ta` = `τ_abstention` · `base_a` = Taban A (karışık SFT) ·
`base_b1`/`base_b2` = Taban B'nin iki aşaması (ardışık SFT).

**Yeni versiyon ne zaman açılır:** eğitim rejiminde (veri · adım · lr · `r`/`alpha` · dropout ·
`target_modules` · precision · seed) **herhangi bir** değişiklik. Rejim aynıysa yeni versiyon
açılmaz — aynı artefakttır.

> ⚠️ **Versiyon karıştırma = merge geçersizliği.** `τ = θ_ft − θ_base` tanımı bütün kolların
> **aynı θ_base**'den ve **eşleşen rejimden** gelmesini şart koşar (`TASARIM.md` §4.1.1, ADR-0036).
> Farklı versiyonları birleştirmek hata vermez, sadece ölçtüğün şeyi yok eder.

---

## Kollar

| kol | ver | tarih | durum | rejim | `‖τ‖_F` | eval etiketi | kayıt |
| :--- | :-- | :--- | :--- | :--- | ---: | :--- | :--- |
| `τ_grounding` | **v1** | 2026-07-28 | 🟢 aktif | 1.083 adım · lr 1e-4 · r=16/α=32 · dropout 0.05 · 224 LoRA çifti · seed 3407 · veri `train/raft/` | **10.4589** | `*_tg` *(Sprint 1; v1 demektir)* | [#41](research_log/2026-07-29-cp6-tau-grounding-olcumu.md) |
| `τ_abstention` | **v1** | 2026-08-03 | 🟢 aktif | **70 adım (5 epoch)** · lr 1e-5 · beta 0.1 · etkin batch 64 · r=16/α=32 · dropout 0.05 · 224 LoRA çifti · `--fresh-adapter` · seed 3407 · veri `data/train/orpo_abstain_cp2c/` (726 çift + 145 replay) | **1.1806** | `*_ta_v1_th` | [#48 §16](research_log/2026-08-02-cp2c-modal-koprusu.md) |
| **`τ_g+τ_a` merge**<br>`HakHukuk-4B-v0.1` | **v1** | 2026-08-03 | 🟢 **ANA SONUÇ** | `tg_v1` + `ta_v1` · **ham TIES** (norm dengeleme **KAPALI**, [ADR-0052](../adr/0052-merge-norm-dengeleme-hukmu-tersine.md)) · trim_k 0,2 · λ 1,0 · eşzamanlı 2-yollu · 224/224 tensör | — *(merge, kol değil)* | `*_tg_ta_ham_th` ⚠️ | [#48 §24](research_log/2026-08-02-cp2c-modal-koprusu.md) |

### `τ_grounding` v1 — açık kalemler *(2026-07-29 gecesi, bütçeli kipte YENİDEN YAZILDI)*

⚠️ Aşağıdaki tablo **CP0.9'dan sonra baştan yazıldı**. Eski hâli thinking-off ölçümünden geliyordu
ve o protokol artık canlı değil (ADR-0043 m.4). Kaynak:
[`research_log` #43](research_log/2026-07-29-cp09-butceli-dusunce-cipalari.md).

| # | sebep | thinking-off | **bütçeli** | durum |
| :-- | :--- | :--- | :--- | :--- |
| 1 | **M5 anti-hedef ihlali** | 36.9 → **44.2** ❌ | 42.5 → **39.2** | ✅ **KAPANDI** — Kapı 6'yı bugün `τ_g` geçiyor, base geçemiyor |
| 2 | **A1 düşüşü** (cevapladığında hata) | 0.973 → 0.847 | 0.986 → **0.866** | 🟡 **duruyor** — ne kadarı meta-iddia artefaktı, CP1 söyleyecek |
| 3 | **RAFT şablonunun meta-iddiaları** (desteksiz iddiaların %58'i) | — | — | 🟡 hakem tarafında (ADR-0041, CP1) |
| 4 | **Akıl yürütme izi İngilizce** | 8/8 | 8/8 | 🟡 ürün vaadi *"okunabilir muhakeme"* karşılanmıyor; izli eğitim verisi gerektirir |
| 5 | 🆕 **M2b çöküşü** — gold yokken distractor'lardan cevap uyduruyor | 1.000 ✅ | **0.607** (fabrikasyon 0.393) | 🔴 **EN GÜÇLÜ sebep** — üstelik tam kendi eğitim ailesinde (RAG_MULTI) |

**Ne değişti:** eski tablonun *"en güçlü sebep"*i (M5 ihlali) bütçeli kipte **ortadan kalktı**;
yerine M2b geldi. Yani `τ_g` v2'nin gerekçesi artık *"ezberi azalt"* değil **"kaynak yokken sus"**.
Bu aynı zamanda `τ_a`'nın hedefiyle çakışıyor — v2 mi `τ_a` mı sorusu Sprint 2'nin açık kararı
([`sprint2.md`](../_arsiv/sprint2.md) ARA KAPI bölümü).

> **Kural (değişmedi):** v2 açılırsa **bütün açık kalemler aynı anda** kapatılır. Ayrı ayrı
> eğitmek iki kat para (~$5.5) ve iki kat kafes yeniden ölçümü demektir. ADR-0040 m.4 gereği
> yeniden eğitilen her kol **düşünme yeteneğini koruyacak** biçimde eğitilir.

### `τ_grounding` v1 — düşünce modu davranışı *(n=470'te DÜZELTİLDİ, 2026-07-29)*

⚠️ CP0'ın n=36'lık ölçümü *"`τ_g` düşünüyor ve duruyor, 35/36"* diyordu ve bu **genel bir kazanç**
sanılmıştı. n=470'te kazanç **eğitim istemi ailesine özgü** çıktı:

| istem ailesi | modlar | base zorunlu kapatma | `τ_g` | ort token base→`τ_g` |
| :--- | :--- | --: | --: | :--- |
| **RAG_MULTI** ← `τ_g`'nin eğitim biçimi | m1 · m2b · m3 | %91.7 | **%5.8** | 1098 → **476** |
| RAG_tek | m4 · m2 | %96.7 | %79.3 | 1116 → 1046 |
| BLIND | m5 | %100.0 | %95.0 | 1284 → 1146 |

Kendi ailesinde etki muazzam (token **yarıya**, kendi kendine kapanma %94); dışında marjinal.
CP0'ın örneklemi o aileden geldiği için genel görünmüştü. Ayrıntı: `research_log` #43 Bulgu 2.

**Maliyet ekseni:** `τ_g` toplamda **772 tok/cevap** (base 1135, Gemini 543) — kendi istem
ailesinde **476**, yani orada rakipten ucuz.

---

## `τ_g+τ_a` merge v1 — künye

**Ürün adı: `HakHukuk-4B-v0.1`** (insan kararı, 2026-08-03)

```
HakHukuk-4B-v0.1  ==  tgta_v1  ==  tg_v1 + ta_v1, ham TIES
```

İki ad **ayrı iş görür ve ikisi de kalır**: `tgta_v1` **iç izlenebilirlik** içindir (dosya
adından *"bu sayı hangi kolun, hangi sürümün"* sorusu cevaplanabilsin — bu belgenin varlık
sebebi); `HakHukuk-4B-v0.1` **dışa dönük** addır (model kartı · makale · anlatım).

⚠️ **Neden `v0.1`, `v1.0` değil:** bu yapılandırma **DEV'de 3 varyant arasından seçildi** ve
**tabanlara karşı henüz sınanmadı**. `v1.0` Kapı 5 geçildikten sonra açılır — geçilmezse zaten
açılmaz.

**Artefakt kimliği** (`tgta_v1`):

```
models/merged/tgta_v1/                   merge edilmiş bf16 (8,8 GB)
models/gguf/tgta_v1-q4_k_m.gguf          taşıyıcı, 2,59 GiB (base ile aynı boyut)
outputs/eval/cp3d-merge/KUNYE_tgta_v1.json   merge künyesi (normlar, TIES istatistikleri)
```

⚠️ **Eval çıktıları `*_tg_ta_ham_th` etiketiyle duruyor** (`outputs/eval/cp3-supurme-ham/`).
Yeniden adlandırılmadı: dosyaların içinde `"label"` alanları var ve ölçüm o etiketle koşuldu.
Sonradan düzeltmek, koşulan şeyi daha derli toplu göstermek için **ölçüm kaydını yeniden
yazmak** olurdu. Eşleme burada kayıtlı ve bağlayıcı olan budur:

```
tgta_v1  ==  outputs/eval/cp3-supurme-ham/*_tg_ta_ham_th_*          harness KAPALI
tgta_v1  ==  outputs/eval/s3-harness-acik/*_tgta_v1_h1_*            harness AÇIK (2026-08-04)
```

⚠️ **Aynı artefaktın iki ölçümü var, karıştırma.** `cp3-supurme-ham` harness KAPALI
(bağlam elle kuruluyor), `s3-harness-acik` harness AÇIK (bağlamı retriever seçiyor,
k=5). Rejim değişmezleri ikisinde de aynı; **tek fark bağlamın nereden geldiği** —
kıyas bu yüzden kurulabiliyor. Sayılar:
[research_log #51](research_log/2026-08-04-harness-acik-ilk-olcum.md) · kütle
**%71,6 (kapalı) ↔ %58,7 (açık)**, altın getirilen alt kümede A1 **0,934 > 0,909**.

**Harness artefaktı** (modelin parçası değil, ama ölçümün parçası):

```
data/index/mevzuat_bge_m3/               hibrit indeks · BAAI/bge-m3 · 40.496 madde · 83 MB
data/index/mevzuat_bge_m3/KUNYE.json     yöntem · model · pencere · korpus imzası
```

**Neden `v1` = ham TIES:** üç varyant DEV'de denendi, kazanan bu ([ADR-0052](../adr/0052-merge-norm-dengeleme-hukmu-tersine.md)).
Diğer ikisi **ablasyon**, versiyon numarası almazlar:

| varyant | geri ölçek | artefakt | M1 kütle | M2 Rej | M2b Rej | durum |
| :--- | ---: | :--- | ---: | ---: | ---: | :--- |
| **ham TIES** | — | `tgta_v1` | **71,6%** | 0,893 | **0,877** | 🟢 **ANA SONUÇ** |
| norm-dengeli `min` | 1,181 | `tg_ta_min` | 53,4% | 0,934 | 0,987 | ablasyon |
| norm-dengeli `ortalama` | 5,826 | `tg_ta_nb` | — | — | — | 🛑 dejenere, koşu geçersiz |

**Ölçülen — hepsi aynı protokol, hepsi geçerli koşu** (thinking on · 1024+512 · seed 3407 ·
chunk 900 · Q4_K_M + llama-server · DEV havuzu · hakem gpt-4o-mini, kapı openrouter/`OpenAI` pinli):

```
                 M1 kütle  aşırı-red      A1   M2 Rej  M2b Rej   tok/cevap (M1)
çıplak base        56,7%      0,425   0,9864   0,814    0,986        1192
tgta_v1 (BİZ)      71,6%      0,212   0,9087   0,893    0,877         714
Gemini 3.1 FL      72,9%      0,237   0,9561   0,930    1,000           —
τ_g v1             71,4%      0,175   0,8658   0,873    0,607           —
τ_a v1             41,2%      0,575   0,9697   0,984    0,987          ~1084
```

**Ne başardı:** `τ_g`'nin grounding'ini **tamamen** korurken (71,4% → 71,6%) onun M2b
çöküşünün **%71'ini onardı** (0,607 → 0,877). Ayrıca öz-sonlandırma geri geldi (M1'de 25/80
zorunlu kapatma, base 80/80) ve cevap başına maliyet base'e göre **%40 düştü**.

> 🛑 **Bu bir PARİTE İDDİASI DEĞİLDİR.** Gemini sütunu **çıpa**dır: harness KAPALI (retriever ·
> atıf doğrulayıcı · red kapısı yok — ADR-0019 bunları teze dahil ediyor), maliyet normalize
> edilmedi, ölçüm **DEV** havuzunda ve **merge yapılandırması DEV'de 3 varyant arasından
> seçildi**. Frozen TEST (`data/eval/canon/`) görülmedi. Aynı disiplin:
> [`sprint1-sonuc-tablosu.md`](sprint1/sprint1-sonuc-tablosu.md).
>
> ⚠️ Açıkça geride olduğumuz eksen **M2b: 0,877 ↔ 1,000**. Raporda böyle geçer.

