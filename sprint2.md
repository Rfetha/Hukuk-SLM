# Sprint 2 — ikinci kol, tabanlar ve zeminin düzeltilmesi

> **Bu belge icra dokümanıdır.** Sayılar, elenen seçenekler, eşik türetmeleri ve biten CP'lerin tam
> sonuç metinleri **[`docs/record/sprint2/defter.md`](docs/record/sprint2/defter.md)**'de.
>
> ### ⭐ HER KOŞUDAN ÖNCE OKU
> [`docs/record/yurutme-tuzaklari.md`](docs/record/yurutme-tuzaklari.md) — *"hata vermeden yanlış
> sonuç üreten"* kalıpların tek listesi. Bu hattın hata sınıfı **çökme değil, sessiz yanlışlık**.

---

## 🎯 HEDEF  (`/goal sprint2.md` bunu okur)

```
koşul     : ARA KAPI'ya ulaşıldı ve iki gözlem ölçülüp raporlandı
🛑 DURMA  : 🔴 ARA KAPI · herhangi bir kırmızı kapı · bütçe aşımı → İNSANA SOR, geçme
kapsam    : CP2-c → kabul zinciri → CP3 → ARA KAPI.  CP4-CP5 bu hedefin DIŞINDA
            (kapı yeşilse ikinci bir /goal ile açılır)
```

⚠️ `/goal` semantiği *"koşul sağlanana kadar çalışmaya devam et"*tir. Sprint 2'nin **ortasında
durması gereken** 🔴 ARA KAPI var ve hemen altında ~**$12**'lik iş duruyor. Bu yüzden HEDEF
Sprint 2'nin tamamını değil, **ARA KAPI'ya kadarki kısmı** kapsar.

---

## 📌 BU BELGE CANLI TUTULUR — sprint akarken güncellenir, sonunda değil

**Niçin:** bu belge `/goal` ile **otonom** koşuluyor; bir sonraki ajanın tek gerçeklik kaynağı
burası. Güncellenmezse ajan **geçmiş bir duruma göre** iş yapar — yanlış app'i bekler, biten bir
CP'yi tekrar koşar, tetiklenmiş bir kapıyı görmez.

- **CP başlarken:** durum tablosundaki satır → 🟡 **KOŞUYOR** + **app id** + **başlangıç saati**.
- **CP biterken:** durum ✅/🔴 · **fiili sayılar** (tahmin değil) · çıktının **nerede** olduğu ·
  hangi **`research_log` girdisine** yazıldığı.
- **Kapı tetiklendiğinde / karar insana gittiğinde:** karar ve gerekçesi **aynı gün** ilgili
  **ADR + `research_log`**'a yazılır, `sprint2.md`'de **tek satırla** işaretlenir.
  *Sohbette kalan bulgu, kaybolmuş bulgudur* (CLAUDE.md, sert kural).

---

## ▶ SIRADAKİ İŞ

```
CP   : CP2-c hasat (-np 64) — 🟡 KOŞUYOR, bitmesi bekleniyor
       app ap-LHKDDasU1MD6b4xG10WK8W · 16:47 başladı
       ölçülen: kararlı 1,46-1,50 s/üretim (eşik 2,88) · kabul ~%33 · hata 0
       → 7.500 üretim ≈ 3,1 sa ≈ ~$7,8 (⚠️ beklenti, fiili panelden)
✅ ÇÖZÜLDÜ (17:05): 16:52'de AYNI dosyaya yazan ikinci iş (ap-5d1ssJOgSKZz1VNAQvxwhD)
       DURDURULDU — 200 üretim geride olduğu için o seçildi. Fazladan ~20 dk GPU (~$0,8).
       ⚠️ KALICI İZ: /cp2c-64/cp2c_m2.jsonl'de YİNELENEN id'ler var + durdurulan süreç
       yazarken kesilmiş olabilir (son satır yarım JSON olabilir). Kabul zinciri
       İNDİRİRKEN: (1) bozuk son satırı at, (2) id bazlı TEKİLLEŞTİR. Ayrıntı #48 §5.
ÖN   : modal app list | grep ap-LHKDDasU1MD6b4xG10WK8W    ← BAŞKA canlı iş OLMAMALI
       modal volume ls hukuk-data /cp2c-64     ← KUNYE.json çıktıysa BİTTİ (tuzak 6.1)
OKU  : her iki huninin  saniye_per_uretim_kararli  +  verim_kapisi damgası  +  kabul sayıları
       🛑 kapı KIRMIZI ise DUR, insana sor — koşuyu kendi başına yeniden başlatma
SONRA: (1) İNDİR  → modal volume get hukuk-data /cp2c-64 · /cp2c
       (2) ONAR+BİRLEŞTİR — ✅ araç hazır, sentetik veriyle iki yolu da sınandı:
           python scripts/cp2c_birlestir.py --out data/_ham_ve_ara/cp2c_birlesik \
                  <indirilen>/cp2c-64 <indirilen>/cp2c
           yapar: id bazlı TEKİLLEŞTİRME · yarım SON satırı atar · ortadaki bozuk
           satırda ÇÖKER (bilinen kesilme kalıbı değil) · karışımı BIRLESIM.json'a
           ve her kayda `kaynak` alanına yazar (ADR-0047 m.2 -np ve kartı serbest)
       (3) KABUL ZİNCİRİ:
KOMUT: bash scripts/cp2c_kabul.sh data/_ham_ve_ara/cp2c_birlesik
BİTİŞ: outputs/eval/cp2c-kabul/kabul_huni.json yazıldı ve temiz negatif sayısı ~750
       (hedefin altındaysa DUR ve insana sor — ADR-0047 m.1)
       ⚠️ VERİM ÖLÇÜLDÜ (n=113 gerçek aday, $0,018 — #48 §9). Hakem tarafı SORUN DEĞİL:
       mini FABRICATE m2 %38,2 · m2b %42,2, ikisi de ADR-0049'un ~%40 varsayımında.
       Darboğaz REGEX ön-filtresi: m2 %31,3 ↔ m2b %19,2 (huni ikisine de ~%30 diyordu).
       Sebebi base'in kendisi ve zaten ölçülüydü: kör base M2b Rej 0.949 ↔ M2 0.803 —
       base M2b'de zaten uydurmuyor, yani 50/50 bölüşüm bu asimetriyi hesaba katmamış.
       ✅ m2 KAPANDI 18:2x: denenen 3.813 · kabul 1.205 (%31,6) · kararlı 1,43 s/üretim
          · kapı "geçildi" (bu kez --limit'ten ÖNCE bakıldı) · zorunlu kapatma 3.810/3.813
       → PROJEKSİYON ~630 temiz (hedef 750, ~%16 açık) ⚠️tahmin
         m2 1.205×%38,2≈460 · m2b ~600×%42,2≈253 · /cp2c 45  → ham ~758 × %83 ≈ 630
       → önerilen kapatma: koşu bittikten SONRA ~1.500 üretimlik ek m2 turu (~40dk ~$1,6).
         ⚠️ TAZE dizin + `--skip-first <önceki turun denenen sayısı>` ZORUNLU: havuz sırası
         deterministik ve hasat onu SIRAYLA yürüyor, `--skip-first` olmadan ek tur aynı
         kalemleri yeniden üretir (aynı dizine koşmak da çare değil — `load_done` yalnız
         KABUL edilenleri biliyor, denenenleri değil). Bayrak eklendi. Detay #48 §9
         Fiili sayı gelince karar insana (ADR-0047 m.1)
YAZ  : (📌 canlı belge kuralı) iş biter bitmez → #48'e sonuç bölümü · defter.md'ye kabul huni
       satırı · ⭐ AŞAĞIDAKİ DURUM TABLOSUNDA CP2-c satırlarını güncelle (durum ✅/🔴, fiili
       sayılar, çıktı yolu, hangi research_log girdisi) · kapı tetiklendiyse ADR + #48 aynı gün
EN SONRA: CP3 — komut ön-denetlendi, aşağıda hazır (⚠️ önce AÇIK KARAR çözülmeli)
```

**CP3 komutu — ateşe hazır** (arayüz `--help` ile doğrulandı; base ADR-0030, modül listesi ADR-0031):

```bash
# 1) çiftleri kur (kabul zinciri bittikten sonra)
python scripts/build_orpo_v3.py \
  --rejected outputs/eval/cp2c-kabul/cp2c_kabul_m2.jsonl \
             outputs/eval/cp2c-kabul/cp2c_kabul_m2b.jsonl \
  --out-dir data/train/orpo_abstain_cp2c

# 2) τ_a — TAZE adapter (--adapter VERİLMEZ ⇒ spawn_orpo --fresh-adapter'a çevirir)
modal run --detach modal_train.py::spawn_orpo \
  --model Qwen/Qwen3.5-4B \
  --data data/train/orpo_abstain_cp2c --run-name ta_v1 \
  --epochs 5 --lr 1e-5 --beta 0.1 --grad-accum 64 --bf16-base --lora-dropout 0.05 \
  --target-modules "q_proj k_proj v_proj o_proj in_proj_qkv in_proj_z in_proj_a in_proj_b gate_proj up_proj down_proj"
```

> ⚠️ `--target-modules` **atlanamaz** (tuzak 3.1): varsayılan liste `in_proj_*`'ı kaçırır →
> 24 linear-attention katmanı LoRA'sız kalır, **hata vermeden**; ölçülen bedel `‖τ_g‖`'nin **%26,8**'i.
> ⚠️ `--adapter` **verilmez**: `τ = θ_ft − θ_base` tanımı her kolun **ham base**'den gelmesini
> şart koşar; adapter verilirse bu ardışık SFT olur ve `τ_g` ile merge edilemez.
> ✅ Beklenen: eğitilebilir **29.908.992 / 4.569.174.528 = %0,65** (CP2-s'te doğrulandı) —
> ilk logda bu sayı çıkmıyorsa **DURDUR**.

**CP3'ün geri kalanı — ⚠️ tekil kol da GGUF'tan ölçülür.** `outputs/eval/cp09-butceli-1024-512/KUNYE.json`
öznelerin `models/gguf/*-q4_k_m.gguf` + `llama-server` üzerinden ölçüldüğünü kayda geçiriyor
(*"tuzak 1.7: özne hep aynı taşıyıcıdan"*). Yani `τ_a` **adapter olarak eval edilmez** —
çıpalarla kıyaslanabilmesi için aynı materyalize→merge→GGUF→Q4_K_M yolundan geçer
(TASARIM.md: singleton'lar **çiftle aynı boru hattından** üretilir; CP2-s bu yolu 4/4 doğruladı).

```
3a  τ_a eğitimi           → adapter
3b  τ_a TEKİL materyalize  merge_ties.py --adapter ta=<dizin> (k=1) → bf16 → GGUF Q4_K_M
3c  τ_a tekil eval         M2 Rej ≥ 0.923 · muhafız M1 A1 ≥ 0.880
3d  τ_g+τ_a merge          merge_ties.py --adapter tg=… --adapter ta=…  (norm-dengeli, k=2)
3e  merge eval             M2b ≥ 0.854
```

**Eval değişmezleri — CP0.9 künyesinden birebir** (sapma karşılaştırmayı geçersiz kılar):

```
taşıyıcı : llama-server, -c 8192 -ngl 99 -fa on, KV q8_0/q8_0
üretim   : --thinking on --think-budget 1024 --max-new-tokens 512 --max-chunk-chars 900
           temperature 0.0 · seed 3407
havuz    : data/eval/dev/  (80 core_hard + 70 trap) — DEV; TEST görülmez
n        : m1 80 · m4 80 · m2 70 · m2b 80 · m3 80 · m5 80
hakem    : gpt-4o-mini · LLM_GATEWAY=openai PİNLİ · red kuralı mod-duyarlı (ADR-0044)
🛑 geçerlilik kapısı: kesik oranı > %5 → KOŞU GEÇERSİZ (çıpalar %3,6 / %3,6 / %0,0)
```

### ✅ ÇÖZÜLDÜ (2026-08-02, insan) — m2b çiftinin `chosen` tarafı → **şablon** ([ADR-0051](docs/adr/0051-m2b-cift-kalibi-ve-chosen-uretimi.md))

> **Onaylanan: A.** Hedef cümleyi sistem isteminin kendisi tarif ediyor; dış model (B) yeni bilgi
> üretmeden üslup kirliliği ekliyordu, C hasadın yarısını çöpe atıyordu. Ölçülen **45/45 tekil**
> `chosen`. Kalıp-öğrenme riski **M1 A1 ≥ 0.880** muhafızıyla ölçülüyor; ön-kayıtlı geri dönüş B.
> **Ayrıca onaylandı: ek hasat turu KOŞULMAYACAK** — ~665 temiz ≈ **65 adım**, ön-kayıtlı 73'ün
> %89'u ve ADR-0047'nin reddettiği 29-adım bölgesinden uzak. ⚠️ Fiili sayı **550'nin altına**
> düşerse karar yeniden açılır (o noktada adım ~54) → `--skip-first 3813`, ~29 dk, ~$1,2.

<details><summary>Kararın gerekçesi ve elenen seçenekler (arşiv)</summary>

Hasat koşarken CP3'ün girdi zinciri önden denetlendi (tuzak 6.2). `build_orpo_v3.py` çifti
**yalnız ORACLE/M2 kalıbında** kurabiliyor ve `orpo_chosen.jsonl`'deki red metinleri
*"Sağlanan {tuzak madde} … bu maddede yer almamaktadır"* biçiminde — **m2b'de "sağlanan madde"
yok** (4 çeldirici, gold hiç yok). Sayıldı: mevcut `τ_a` setindeki **1.449 çekinme çiftinin
tamamı M2 kalıbı**; RAG_MULTI kalıbı yalnız `is_pref=0` replay'de var. Yani **`τ_a` bugüne dek
M2b kalıbında tek bir çekinme çifti görmedi** — oysa defterdeki negatif #4'e göre `τ_a`'nın
**gerçek hedefi** orası ve **ARA KAPI'nın 2. gözlemi** o eksende okunuyor. Ayrıntı: [#48 §7](docs/record/research_log/2026-08-02-cp2c-modal-koprusu.md).

*Alan adı uyumsuzluğu (`rejected`↔`model_answer`, `context_shown`↔`trap_text`) ve m2b kalıbının
`RAG_MULTI` olması **karar değil, zorunluluk** — eval-ayna kuralı belirliyor, cevap gelince
köprüyle birlikte yazılır.*

| # | seçenek | bedel | risk |
| :-: | :--- | :--- | :--- |
| **A** | m2b `chosen`'ı **şablonla** üret, yuvaları hasadın `context_shown`'undaki gerçek kanun adlarından doldur | **$0** | metin fazla kalıplı olursa kol **üslup** öğrenir, muhakeme değil → M2b şişer |
| **B** | m2b `chosen`'ı **hakemle üret** (gpt-4o-mini, ~750 kalem) | ~**$0,4** | dış modelin üslubu `chosen` tarafına girer (kaynak tarafı zaten kendi hasadımız) |
| **C** | m2b'yi çiftlerin **dışında** bırak, `τ_a` yalnız M2'de eğitilsin | $0 | hasadın **yarısı çöpe**; ARA KAPI, `τ_a`'nın hazırlanmadığı bir ekseni ölçer |

**Öneri: A** — ve **A lehine yeni kanıt:** red cümlesini `SYSTEM_PROMPT_RAG_MULTI`'nin **kendisi
tarif ediyor** (*"İlgili kaynak YOKSA … 'Verilen kaynaklarda bu konuyu düzenleyen madde
bulunmuyor' de"*). Yani hedef davranış istemde zaten yazılı; `chosen`'ın işi onu örneklemek.
Üslup riski ayrıca M1 muhafızı (A1 ≥ 0.880) ile ölçülüyor.

**Uygulama:** `build_orpo_v3.py` genişletildi (çoklu `--rejected` · şema ayrımı · m2b için
RAG_MULTI kalıbı + `m2b_chosen()` şablonu · künyeye mod ve hasat-kaynağı karışımı). Gerçek 113
kayıtla **$0 prova koştu**: 113 çift (m2 68 · m2b 45), **45/45 tekil `chosen`**. Emekli `gen_v3`
yolu **birebir korundu** (1495/299/1794 — kayıtlı `orpo_report.json` ile özdeş).
🐞 Provada bir **sessiz** kusur yakalandı ve düzeltildi: külliyatta hem `Madde 75` hem
`MADDE 64` yazımı var, şablonun regexi büyük/küçük harfe duyarlıydı → 45 kalemin **15'i**
kısa yedek metne düşüyordu (hata yok, yalnız zayıf hedef). `re.IGNORECASE` → 0/45.

</details>

**Maliyet:** kabul zinciri OpenAI hakem ~**$3,68** (ADR-0049 m.5, tasarım B) · o adımda GPU **$0**
(koşan hasadın kendi beklentisi ~$11, durum tablosunda).

---

## Durum tablosu

*(tek satırlık; tam sonuç metinleri ve sayılar [`defter.md`](docs/record/sprint2/defter.md)'de)*

| CP | durum | $ | çıktı nerede |
| :--- | :--- | ---: | :--- |
| **CP0** düşünce modu | ✅ base sonlanmıyor → thinking AÇIK, bütçeli (ADR-0043) | 0 | `outputs/eval/cp0-*` · [#42](docs/record/research_log/2026-07-29-cp0-dusunce-modu-sonlanmama.md) |
| **CP0.9** üç çıpa | ✅ 1.410 cevap · ADR-0044 · ADR-0040 hükmü **🟡 SARI** | 0.49 | `outputs/eval/cp09-butceli-1024-512/` · [#43](docs/record/research_log/2026-07-29-cp09-butceli-dusunce-cipalari.md) |
| **CP0.5** `causal-conv1d` | ✅ **kapı KALDI** (tavan 1.254× < 2.0×) → eklenmedi | 0 | `outputs/eval/_artefakt/` · [#44](docs/record/research_log/2026-07-30-cp05-cp1-cp2-zemin.md) |
| **CP1** hakem istemi | ✅ `τ_g`'nin A1 açığının **%59'u artefaktmış** (ADR-0041) | 0.15 | `outputs/eval/cp1-hakem-meta-iddia/` · [#44](docs/record/research_log/2026-07-30-cp05-cp1-cp2-zemin.md) |
| **CP2 pilot** | ✅ kusur buldu: kabul ölçütü ≠ raporlanan metrik → ADR-0046 | 0.01 | `outputs/eval/cp2-rejected-hasat/` · [#44](docs/record/research_log/2026-07-30-cp05-cp1-cp2-zemin.md) |
| **CP2-a** uyum kapısı | ✅ **kapı KALDI** · `valid_trap` özneye bağlı çıktı → ADR-0048/0049 | 0.121 | `outputs/eval/cp2-on-eleme/` · [#45](docs/record/research_log/2026-07-30-cp2a-hakem-capalanmasi.md) |
| ~~**CP2-b**~~ | ❌ **İPTAL** — ön-eleme net zararlı (isabet 0,14), ADR-0048 m.4 | 0 | — |
| **CP2-r** | ✅ cevaba-kör payda · **eşikler türetildi 0.923 / 0.880 / 0.854** | 0.23 | `outputs/eval/cp2-r-kor-payda/` · [#46](docs/record/research_log/2026-07-30-cp2r-kor-payda.md) |
| **CP2-s** | ✅ boru hattı 4/4 · 🔴 TIES kodu yoktu → `merge_ties.py` yazıldı | ~0.35 | `outputs/eval/cp2-s-boru-hatti-smoke/` · [#47](docs/record/research_log/2026-07-30-cp2s-boru-hatti.md) |
| **CP2-c** `-np 32` denemesi | 🔴 **VERİM KAPISI TETİKLENDİ** 16:19-16:46 (m2 `2,97>2,88` · m2b `2,95>2,88`) — kapı *yanlı tahmin ediciyle* ölçüyordu (gerçek kararlı hız m2 ~2,4), **tahmin edici düzeltildi, eşiğe DOKUNULMADI** → [ADR-0050](docs/adr/0050-verim-kapisi-tahmin-edici-duzeltmesi.md) · **113 kabul kaydı korundu** | ~1.2 ⚠️**beklenti** — fiilisi **panelden** okunacak (tuzak 6.3) | app `ap-5f6rLHHFohhupMGvhkla9I` → `hukuk-data:/cp2c/` · [#48](docs/record/research_log/2026-08-02-cp2c-modal-koprusu.md) |
| **CP2-c hasat** | 🟡 **KOŞUYOR** — 2026-08-02 **16:47**, `-np 64`, `--limit 3750`/tip. **m2 ✅ BİTTİ 18:2x**: denenen **3.813** · kabul **1.205 (%31,6)** · kararlı **1,43** · kapı **"geçildi"** (hak edilmiş: `--limit`'ten önce bakıldı) · zorunlu kapatma 3.810/3.813. **m2b 🟡 koşuyor** (kararlı ~1,78 · kabul ~%16) · hata **0** · ✅ 17:05'te aynı dosyaya yazan ikinci iş (`ap-5d1ss…`) durduruldu → çıktıda **id tekilleştirmesi şart** (#48 §5) | ~7.8 ⚠️beklenti (+~0.8 çift iş) | app `ap-LHKDDasU1MD6b4xG10WK8W` → `hukuk-data:/cp2c-64/` · [#48](docs/record/research_log/2026-08-02-cp2c-modal-koprusu.md) |
| **CP2-c kabul** | ▶ **SIRADAKİ** — `cp2c_kabul.sh`, tasarım B (ADR-0049 m.5) | ~3.68 | `outputs/eval/cp2c-kabul/` |
| **CP3** `τ_a` + merge | ⏳ ADR-0047 rejimi (~73 adım / 5 epoch) · **`--fresh-adapter` ZORUNLU** | ~3.20 + 0.15 | → 🔴 **ARA KAPI** |
| ~~CP4 · CP5~~ | 🔒 **BU HEDEFİN DIŞINDA** — ARA KAPI yeşilse ikinci `/goal` | ~12.2 | spec: [`defter.md`](docs/record/sprint2/defter.md) |

**Bütçe — İKİ CÜZDAN, karıştırılmaz (tuzak 6.3).** Modal sayısı **panelden** okunur, defterden
türetilmez. Sprint 2'de OpenAI hakem harcaması bugüne dek **$1.00**. Tam tablolar defterde.

> ⚠️ **Yukarıdaki GPU sayıları BEKLENTİ, ölçüm değil.** `-np 32` denemesinin (16:19-16:46) fiili
> maliyeti **panelden okunacak** — tahmin ~$1,2, defterden türetilmedi. Aynısı koşan `-np 64`
> hasadı için de geçerli (~$11 beklenti). Panelden okunan sayı geldiğinde bu satır güncellenir.

---

## 🔴 ARA KAPI — rakip yöntemlere geçmeden önce

**İki gözlem** ([ADR-0045](docs/adr/0045-ara-kapi-merge-onarim-kontrolu.md) ·
[ADR-0049](docs/adr/0049-sprint2-kalan-kararlarin-kilitlenmesi.md) m.1). Eşikler CP2-r'de
**türetildi**; ön-kayıtlı olan **formül**, sayı değil.

```
1) τ_a TEKİL      M2 Rej ≥ 0.923   (cevaba-kör base 0.803 + 12 puan)
   muhafız        M1 A1  ≥ 0.880   (CP1 hakemi, base A1 0.9777 × 0.90)
2) τ_g+τ_a MERGE  M2b    ≥ 0.854   (cevaba-kör base 0.949 × 0.90) — norm-dengeli TIES, DEV
```

**Eski eşiklere (0.934 / 0.888 / 0.887) karşı DA raporlanır** — ADR-0049 m.1.

| tekil M2 ≥ **0.923** | merge M2b ≥ **0.854** | eylem |
| :-: | :-: | :--- |
| ✅ | ✅ | **Güçlü yeşil** — CP4-CP5 koşulur |
| ❌ | ✅ | **Devam** — kapı tavan-sınırlıydı; gerekçe merge kanıtı, raporda **açıkça öyle yazılır** |
| ✅ | ❌ | **DUR** — kol tek başına iyi ama birleşince taşımıyor; iç iddianın öncülü sorunlu |
| ❌ | ❌ | **DUR** — `τ_a` rejimi düzeltilir (epoch · lr · çift sayısı). Rakiplere ~$12 harcanmaz |

> ### 🚨 Tavan riski — sonuçla birlikte raporlanır
> Base geçerli 59 tuzağın **48'ini zaten reddediyor**. +12 puan, kalan **11 hatanın 7'sinin**
> düzeltilmesi demek — tavana **6.6 puan** kala. `τ_a` bu kapıda kalırsa sebebi kolun kötülüğü
> değil **base'in tavana yakınlığı** olabilir. Sayı ön-kayıtlı formülden geldiği için
> **değiştirilmedi.**

**Her iki 🛑 durumda: DUR, insana sun.** ARA KAPI geçilmeden CP4-CP5'e para harcanmaz.

---

## Değişmezler — her koşuda uyulacak

```
thinking ON · düşünce 1024 + cevap 512 · seed 3407 · --max-chunk-chars 900
n = 80/80/70/80/80/80 · DEV havuzu · TEST (eval/canon/) hiç görülmez
taşıyıcı: Q4_K_M GGUF (q35-4b-q4_k_m.gguf) + llama-server — vLLM/bf16 YASAK (ADR-0047 m.2)
çıktı: outputs/eval/<koşu-adı>/ + KUNYE.json   (künyeye gpu_gercek dahil — tuzak 6.7)
hakem: gpt-4o-mini · LLM_GATEWAY=openai (pinli) · red kuralı mod-duyarlı (ADR-0044)
eğitim: --target-modules zorunlu · --fresh-adapter zorunlu · spawn() + modal run --detach
verim kapısı: KARARLI hız okunur (açılış geçicisi hariç) · eşik 2,88 s/üretim — ADR-0050
              (ADR-0047 m.3'ün eşiği AYNI; düzelen yalnız tahmin edici)
```

> ### 📌 2026-08-02 · verim kapısı olayı — **eşiğe dokunulmadı, tahmin edici düzeltildi**
> `-np 32` koşusu kapıya takıldı; kapı `geçen÷tamamlanan` (kümülatif) okuyordu ve açılış dalgasını
> her kaleme paylaştırıyordu. Kanıt: 600. sn `2,97` ile durdurdu, **aynı koşu 673. sn'de 2,89**'daydı.
> Reddedilenler: **B** eşiği 3,2'ye gevşetmek (çıpalama) · **C** CP2-c'yi negatif bulgu sayarak
> kapatmak (teşhis yanlış: taşıyıcı değil **alet** hatalıydı). Uygulanan: **A**.
> Karar → [**ADR-0050**](docs/adr/0050-verim-kapisi-tahmin-edici-duzeltmesi.md) · tuzak **6.9** ·
> detay [`defter.md`](docs/record/sprint2/defter.md) 16:19-16:47 kaydı · [#48](docs/record/research_log/2026-08-02-cp2c-modal-koprusu.md)

---

## Bağlantılar

| ne | nerede |
| :--- | :--- |
| **Sayılar · elenen seçenekler · eşik türetmeleri · biten CP'ler** | ⭐ [`docs/record/sprint2/defter.md`](docs/record/sprint2/defter.md) |
| Otorite tasarım | [`TASARIM.md`](TASARIM.md) · canlı karar defteri [`docs/open_questions.md`](docs/open_questions.md) |
| Bu sprint'in kararları | ADR-[0039](docs/adr/0039-kapi-6-parametrik-sizinti.md) · [0040](docs/adr/0040-dusunce-modu-olculecek-on-kayitli-kural.md) · [0041](docs/adr/0041-raft-meta-iddia-hakem-kurali.md) · [0042](docs/adr/0042-rejected-havuzu-tek-kaynak-ve-on-policy-kontrol.md) · [0043](docs/adr/0043-dusunce-modu-acik-butceli-kapatma.md) · [0044](docs/adr/0044-mod-duyarli-feragat-kurali.md) · [0045](docs/adr/0045-ara-kapi-merge-onarim-kontrolu.md) · [0046](docs/adr/0046-cp2-kabul-olcutu-hakem-ve-havuz-on-elemesi.md) · [0047](docs/adr/0047-cp2-hedef-750-modal-hasat.md) · [0048](docs/adr/0048-cevaba-kor-tuzak-gecerliligi.md) · [0049](docs/adr/0049-sprint2-kalan-kararlarin-kilitlenmesi.md) · **[0050](docs/adr/0050-verim-kapisi-tahmin-edici-duzeltmesi.md)** (verim kapısı: kararlı hız, eşik 2,88 aynı) · **[0051](docs/adr/0051-m2b-cift-kalibi-ve-chosen-uretimi.md)** (m2b çifti: eval-ayna kalıbı + şablon `chosen`) |
| Kronolojik kayıt | [`research_log`](docs/record/research_log/README.md) — bu sprint: #42-#48 |
| **Koşu öncesi tuzak listesi** | ⭐ [`docs/record/yurutme-tuzaklari.md`](docs/record/yurutme-tuzaklari.md) |
| Kol künyeleri | [`docs/record/kollar.md`](docs/record/kollar.md) |
| Önceki sprint | [`sprint1.md`](sprint1.md) 🔒 · sonuçları [`sprint1-sonuc-tablosu.md`](docs/record/sprint1/sprint1-sonuc-tablosu.md) |
| Tam iş listesi | [`TODO.md`](TODO.md) |

---

> ### 🗑️ `DEVIR-1-AGUSTOS.md` silindi (2026-08-02)
> Geçici devir notuydu, görevi bitti (Modal fatura dönemi yenilendi, CP2-c koşmaya başladı).
> İçeriği [`research_log` #48](docs/record/research_log/2026-08-02-cp2c-modal-koprusu.md) ·
> [`defter.md`](docs/record/sprint2/defter.md) · bu belgeye taşındı; hiçbir sayı kaybolmadı.
> Silmeden önce her kalemi #48/ADR/defter'de kayıtlı olduğu **teyit edildi**.
