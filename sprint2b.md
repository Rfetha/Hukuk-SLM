# Sprint 2b — TABANLAR: iç iddianın gerçek sınavı

> **Bu belge icra dokümanıdır ve `/goal sprint2b.md` ile otonom koşulur.**
> Sprint 2 kapandı ([`sprint2.md`](sprint2.md), ARA KAPI 🟢); geriye **CP4-CP5** kaldı.
>
> ### ⭐ HER KOŞUDAN ÖNCE OKU
> [`docs/record/yurutme-tuzaklari.md`](docs/record/yurutme-tuzaklari.md) — bu hattın hata sınıfı
> **çökme değil, sessiz yanlışlık**. Sprint 2 buraya **6.10 · 6.11 · 6.12**'yi ekledi.

---

## 🎯 HEDEF

```
koşul     : CP4 ve CP5 eğitildi, aynı protokolde ölçüldü ve Kapı 5 kararı raporlandı
🛑 DURMA  : herhangi bir kırmızı kapı · geçerlilik kapısı düşerse · bütçe aşımı
            · ⛔ AŞAĞIDAKİ AÇIK KARAR çözülmeden CP4 BAŞLATILMAZ
kapsam    : CP4 (karışık) · CP5 (ardışık + on-policy kontrol) · Kapı 5 okuması
            Sprint 3'ün 8 hücreli kafesi bu hedefin DIŞINDA
bedel     : ~$19,64 / kalan bütçe $22,31 (panelden) · pay ~$2,67 · ~10 saat
```

**Neden bu sprint var:** ARA KAPI *"bu yola para harcamaya değer"* dedi, **iddiayı kanıtlamadı**.
İddia **karşılaştırmalı**: *merge, aynı veriyle karışık SFT'den ve ardışık SFT'den daha iyi
korur*. O karşılaştırma budur.

---

## ⛔ AÇIK KARAR — CP4 başlamadan çözülmeli (insan)

**Sorun:** ön-kayıtlı metin CP4'ü *"tek-aşamalı karışık **SFT**"* diye tarif ediyor. Ama kollar
farklı hedeflerle eğitildi:

```
τ_g  = SFT            (raft grounding verisi, 1.083 adım)
τ_a  = ORPO           (tercih çiftleri, 70 adım)
merge = TIES(τ_g, τ_a)
```

CP4'ü **saf SFT** koşarsak, tabanın çekinme tarafı yalnız `chosen` metnini görür — `rejected`'ı
hiç görmez. O zaman kıyas **yöntemi** (merge ↔ karışık) değil **hedefi** (ORPO ↔ SFT)
ölçer. Hakem bunu yakalar ve Kapı 5'in tamamını çürütür.

| # | seçenek | ne olur | bedel |
| :-: | :--- | :--- | :--- |
| **A** | CP4 = **karışık ORPO** — grounding satırları `is_pref=0`, çekinme çiftleri `is_pref=1`, **tek koşu** | Hedef kollarla **eşleşir**; fark yalnız *"ayrı eğit+merge"* ↔ *"birlikte eğit"* olur. `MaskedORPOTrainer` bunu **zaten destekliyor** (is_pref=0 → saf SFT kaybı) | **$5,45** (1 ep) → **$27,26** (5 ep) ⚠️ epoch kararı bütçe bölümünde |
| B | CP4 = saf SFT (ön-kayıtlı metne harfi harfine sadık) | Hedef karışır, iddia savunulamaz | ~$5,7 |
| C | İkisini de koş | Kusursuz ama +$5,7 ve +4 saat | ~$11,7 |

**Önerim: A.** Ön-kayıtlı metinden sapma, ama **iddiayı korumak için** — ve sapmanın kendisi
ADR'ye yazılır. B, ucuz görünüp sonucu değersiz kılar.

🛑 **İnsan A/B/C demeden CP4 başlatılmaz.**

---

## ▶ SIRADAKİ İŞ

```
0) AÇIK KARAR çözülür → ADR yazılır (numaralandırma 0053'ten devam)
1) CP4 veri seti kurulur   → doğrulanır → volume'a yüklenir
2) CP4 eğitilir            → artefakt kapısı → materyalize → GGUF → 3 eksen eval
3) CP5 FT-6 → τ_g v1'in ÜSTÜNE eğitilir (FT-5 zaten var) → aynı zincir
4) CP5 FT-6 on-policy kontrol koşusu (~$1,5)
5) Kapı 5 okunur ve raporlanır → 🛑 DUR, insana sun
```

---

## CP4 — Taban A: tek-aşamalı **karışık**

**Ham base'den.** `rejected` havuzu CP2-c'den (tek havuz kuralı, ADR-0042).

```
veri     grounding  data/train/raft/train.jsonl        17.323 satır → is_pref=0
         çekinme    CP2-c'nin 726 çifti                          → is_pref=1
         ⚠️ karışım oranı KARARA BAĞLI — τ_a'nın gördüğü oran %20 replay'di;
            taban için doğru oran "her iki beceriyi de gören tek koşu"dur
rejim    ⚠️ τ_g ve τ_a ile EŞLEŞMELİ (aşağıdaki değişmezler)
çıktı    hukuk-outputs:/base_a_v1  →  kollar.md'ye künye
```

> ### 🚨 Adil kıyas şartı (ADR-0037)
> **Aynı seçim prosedürü tabana da uygulanır.** Biz merge'i DEV'de **3 varyant** arasından
> seçtik ([ADR-0052](docs/adr/0052-merge-norm-dengeleme-hukmu-tersine.md)). Taban A için de
> DEV'de en iyi checkpoint/ayar seçilir — yoksa *"biz taranmış, onlar taranmamış"* olur ve
> `D > A` iddiası **değersizdir**. Kaç varyant denendiyse **raporda sayısıyla** geçer.

## CP5 — Taban B: **ardışık** + on-policy kontrol

```
FT-5   aşama 1: grounding, HAM BASE'den    → ✅ ZATEN VAR: τ_g v1 (outputs/tg_v1)
       tarifi birebir aynı (raft · ham base · SFT · 11 modül · seed 3407)
       yeniden eğitmek ~$4,4 yakmak olurdu — ve aynı şeyi üretirdi
FT-6   aşama 2: çekinme, FT-5'in ÜSTÜNE    → hukuk-outputs:/base_b2_v1
       --adapter outputs/tg_v1  VERİLİR    (τ kolu DEĞİL — kasten ardışık SFT)
```

> ⭐ **FT-5 = `τ_g v1` olması kıyası GÜÇLENDİRİYOR.** Ardışık tabanın birinci aşaması ile
> merge'in `τ_g` kolu **birebir aynı artefakt** olur; tek fark ikinci aşamada *"üstüne eğit"*
> ↔ *"ayrı eğit ve birleştir"*. Kıyas böylece tam olarak **yöntemi** ölçer, eğitim
> gürültüsünü değil.

| koşu | `rejected` kaynağı | nerede raporlanır |
| :--- | :--- | :--- |
| **FT-6 ana** | CP2-c havuzu (base'den) | **ana tablo** — veri sabit, fark yönteme atfedilir |
| **FT-6 kontrol** | **FT-5'in kendi çıktısından** (on-policy) | **robustluk satırı** · ~$0,65 |

> ### 🚨 Kontrol koşusu neden var
> Ana koşuda Taban B **off-policy** veriyle eğitiliyor — negatifler FT-5'in gerçekten söylediği
> şeyler değil → taban **zayıf eğitilir** → sapma **bizim lehimize**. *"Tabanı zayıf eğittiniz"*
> itirazı Kapı 5'i çürütebilir; $0,65'e sigortalanıyor.
>
> **Ön-kayıtlı yorum kuralı:** on-policy taban, veri-sabit tabandan bileşik ölçütte **≥ +0,05**
> iyiyse, Kapı 5'in *"iki tabanı da geç"* şartı **on-policy sürüm** üzerinden okunur.

---

## Rejim değişmezleri — SAPMA = KIYAS GEÇERSİZ

```
base            Qwen/Qwen3.5-4B  sha 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
LoRA            r=16 · alpha=32 · dropout 0.05 · bf16 taban (--bf16-base)
target-modules  q_proj k_proj v_proj o_proj in_proj_qkv in_proj_z in_proj_a in_proj_b
                gate_proj up_proj down_proj                              ← 11, ZORUNLU
seed            3407
```

**⛔ ARTEFAKT KAPISI** (log satırı değil — Sprint 2'de log kayan pencere döndürdü, #48 §16):

```
adapter_model.safetensors  →  448 tensör · 29.908.992 parametre
adapter_config.json        →  r=16 · alpha=32 · dropout 0.05 · 11 modül
tutmazsa DUR — kıyas edilemez.
```

## Eval protokolü — CP0.9 künyesinden birebir

```
taşıyıcı : GGUF Q4_K_M + llama-server · -c 8192 -ngl 99 -fa on · KV q8_0/q8_0
üretim   : --thinking on --think-budget 1024 --max-new-tokens 512 --max-chunk-chars 900
           temperature 0.0 · seed 3407
havuz    : data/eval/dev/ — DEV; frozen TEST (data/eval/canon/) GÖRÜLMEZ
modlar   : m1 · m2 · m2b  (⚠️ ÜÇÜ BİRDEN — gerekçe aşağıda)
hakem    : gpt-4o-mini · kapı openrouter · LLM_PROVIDER_ORDER=OpenAI PİNLİ
🛑 geçerlilik kapısı: kesik oranı > %5 → KOŞU GEÇERSİZ, puanlamaya para harcanmaz
```

**Araç hazır:** `scripts/cp3_merge_dene.sh <merged-dizin> <etiket>` — GGUF → 3 eksen → puanlama,
tek komut, kapı düşerse zincir kırılır.

> ### 🚨 TEK EKSENLE ÇEKİNME OKUNMAZ — Sprint 2'nin en pahalı dersi
> **A1 cevaplanan-only'dir; çekinerek kazanmayı ödüllendirir.** Ölçüldü:
> `τ_a` A1 **0,9697** (tüm öznelerin en yükseği) ama kütle %41,2 · dejenere merge A1 **1,0000**
> (teorik tavan) ama **80 sorudan 2'sini** cevaplıyordu.
>
> **Her tabloda `sadık-cevap kütlesi = coverage × A1` raporlanır.** Kapı eşikleri değişmez;
> değişen, aynı gözlemin ikinci bir eksende de gösterilmesidir.

> ### 🚨 Geçerlilik kapısı düşerse reçeteye KÖRÜ KÖRÜNE uyma
> Kapı *"`MAXTOK` büyüt"* der. Sprint 2'de kesiklerin **tamamı tekrarlama döngüsüydü** — yani
> bütçe darlığı değil **model hasarı**; bütçe büyütmek daha uzun döngü üretirdi. Ayrıca
> `MAXTOK` bir **rejim değişmezidir** (ADR-0043): değiştirmek tüm çıpaları kıyaslanamaz kılar.
> **Önce kesikleri gözle oku:** döngü mü, gerçek uzun cevap mı?

---

## 🚦 KAPI 5 — iç iddianın karar kuralı

[ADR-0037](docs/adr/0037-ic-iddia-karar-kurali-kapi-5.md) · ölçüm **ham TIES** ayarında
([ADR-0052](docs/adr/0052-merge-norm-dengeleme-hukmu-tersine.md), ADR-0036'nın hükmü tersine)

```
(a) grounding  M1/M4  ≥ 0,90 × (τ_g tek)
(b) abstention M2/M2b ≥ 0,90 × (τ_a tek)
(c) bileşik = min(grounding, abstention) → Taban A ve Taban B'nin İKİSİ de geçilmeli
```

**Kıyas noktaları — Sprint 2'de ölçüldü:**

```
özne          M1 kütle   M2 Rej   M2b Rej
τ_g v1          71,4%     0,873    0,607
τ_a v1          41,2%     0,984    0,987
tgta_v1 ⭐      71,6%     0,893    0,877     ← iddianın öznesi = HakHukuk-4B-v0.1
Taban A            ?        ?        ?      ← CP4
Taban B            ?        ?        ?      ← CP5
```

⚠️ Kapı 5 bir **karar kuralıdır, istatistiksel test değil** — güç analizi yok, tek koşu.

---

## 💰 BÜTÇE ve HESAP PLANI — panelden okundu, plan kilitlendi

```
Modal  KALAN $22,31   ← usage limit $42,50 − harcanan $20,19    ⭐ BAĞLAYICI OLAN BU
       (kredi $9,81 yalnız ön-ödemeli kısım — tavan değil)
OpenAI $0 — kredi tükendi (2026-08-03)
OpenRouter ~$1,4 · eval hakemi · sağlayıcı `OpenAI` PİNLİ
```

⚠️ **Kredi ≠ bütçe.** Krediler bitince fatura karta gider, tavan `usage limit`tir.

### Ölçülen maliyet — tahmin değil, `τ_a` koşusundan türetildi

`τ_a`: 845 örnek × 5 epoch = 4.225 geçiş, `train_runtime` **2.188 s** → **0,518 s/örnek-geçiş**.
`τ_g`: 1.083 adım × **7,0 s/it** (defter, SFT batch 16) → 7.581 s.

```
MERGE'İN TOPLAM EĞİTİMİ — iddianın öznesi bu kadar hesap gördü
  τ_g   17.323 geçiş · 2,11 sa · ~$4,42
  τ_a    4.225 geçiş · 0,61 sa · ~$1,28
  ───────────────────────────────────────
  TOPLAM 21.548 geçiş · 2,71 sa · ~$5,70          ← "1,00× merge" referansı
```

### 🔒 KİLİTLENEN PLAN — CP4 **3 epoch** (insan kararı, seçenek iv)

| iş | detay | ~$ |
| :--- | :--- | ---: |
| **CP4** karışık ORPO · **3 epoch** | 54.147 geçiş = **2,51× merge** · 7,79 sa | **16,36** |
| **CP5** FT-6 (`τ_g` üstüne) · 5 epoch | 4.225 geçiş · 0,61 sa | 1,28 |
| **CP5c** on-policy kontrol | hasat + eğitim | ~1,50 |
| hakem | 3 özne × 3 eksen | ~0,50 |
| | **TOPLAM** | **~19,64** |
| | **kalan pay** | **~2,67** |

**Neden 3 epoch — "eşit" değil, itirazı kapatan sayı.** Asıl mesele *"tabanı az eğittiniz"*
itirazını kapatmak. 3 epoch şu cümleyi satın alıyor:

> **Tek-aşamalı taban, merge'in iki kolunun toplamının 2,5 katı eğitim hesabı gördü —
> ve yine de kaybetti.**

Elenenler: **1,19 epoch** (tam 1,00× — teknik olarak "eşit" ama *"sınırda tuttunuz"*
itirazına açık) · **3,5 epoch** (2,93× ama pay **−$0,05**; bir yeniden koşu bütçeyi bitirir).

⚠️ **Epoch bir rejim değişmezi DEĞİL.** O kural birleştirilecek **kollar** içindir
(TASARIM §4.1.1); tabanlar birleştirilmiyor. Sabit tutulması gereken **veri** (ADR-0042 tek
havuz) ve **seçim prosedürü**dür (ADR-0037). Taban lehine sapma **kasıtlıdır** ve raporda
böyle geçer.

⚠️ Bu sayılar **karışık ORPO** varsayar (açık kararın **A** şıkkı). Saf SFT seçilirse maliyet
de gerekçe de yeniden hesaplanır.

### ⭐ CP5'in FT-5'i yeniden eğitilmeyecek — `τ_g v1` onun ta kendisi

Tarifi *"aşama 1: grounding, ham base'den"*; `τ_g v1` **tam olarak budur** (raft · ham base ·
SFT · aynı 11 modül · seed 3407). ~**$4,4 tasarruf** — ve **daha temiz bilim**: ardışık tabanın
1. aşaması ile merge'in `τ_g` kolu **birebir aynı artefakt** olur, tek fark 2. aşamada
*"üstüne eğit"* ↔ *"ayrı eğit ve birleştir"*. Kıyas tam olarak **yöntemi** ölçer.

## Koşu öncesi kısa liste — Sprint 2'nin ısırdığı yerler

- [ ] **Modal panelden bakiye** okundu mu (defterden türetme — 6.3)
- [ ] `modal app list` — **başka canlı iş yok** (6.10: iki detached iş aynı dizine yazar)
- [ ] `--data` **konteyner yolu** mu (`/data/<set>`) ve `modal volume put` yapıldı mı (3.6)
- [ ] `--target-modules` verildi mi · `--adapter` doğru mu (CP4/FT-5 **taze**, FT-6 **üstüne**)
- [ ] Eklenen her bayrak **çağrı zinciri uçtan uca** izlendi mi — betik → orkestratör → komut →
      **künye** (6.12: bu turda **dört kez** ısırdı)
- [ ] `modal run --detach` (6.1) · *"SPAWNED"* işin koştuğunu **kanıtlamaz**
- [ ] Eğitim bitince **artefakt kapısı**: 448 tensör / 29.908.992 parametre
- [ ] Eval sonrası: kesik oranı %5 altında mı · **kütle** A1'in yanında mı

---

## 📌 BU BELGE CANLI TUTULUR

`/goal` ile otonom koşuluyor; bir sonraki ajanın tek gerçeklik kaynağı burası.

- **CP başlarken:** 🟡 KOŞUYOR + **app id** + başlangıç saati
- **CP biterken:** ✅/🔴 · **fiili sayılar** · çıktı nerede · hangi `research_log` girdisi
- **Kapı tetiklendiğinde / karar insana gittiğinde:** **aynı gün** ADR + `research_log`

*Sohbette kalan bulgu, kaybolmuş bulgudur.*

---

## Durum tablosu

| CP | durum | $ | çıktı nerede |
| :--- | :--- | ---: | :--- |
| **0** açık karar (A/B/C) | 🛑 **İNSAN BEKLENİYOR** | 0 | → ADR-0053 |
| **CP4** Taban A (karışık) | ⏳ | ~6 | `hukuk-outputs:/base_a_v1` |
| ~~**CP5a** FT-5~~ | ✅ **GEREKMİYOR** — `τ_g v1` bunun ta kendisi | **0** *(~$4,4 tasarruf)* | `outputs/tg_v1` |
| **CP5b** FT-6 (çekinme, üstüne) | ⏳ | ~3 | `hukuk-outputs:/base_b2_v1` |
| **CP5c** FT-6 on-policy kontrol | ⏳ | ~0.65 | robustluk satırı |
| **Kapı 5** karar | ⏳ | ~0.5 hakem | 🛑 **DUR, insana sun** |

---

## Bağlantılar

| ne | nerede |
| :--- | :--- |
| Sprint 2'nin kapanışı ve tam tablosu | [`sprint2.md`](sprint2.md) · [`defter.md`](docs/record/sprint2/defter.md) |
| Artefakt kimlikleri (`tg_v1` · `ta_v1` · **`tgta_v1`**) | ⭐ [`kollar.md`](docs/record/kollar.md) |
| Bu sprint'in kaynağı | [#48 §11-§24](docs/record/research_log/2026-08-02-cp2c-modal-koprusu.md) |
| Kararlar | ADR-[0037](docs/adr/0037-ic-iddia-karar-kurali-kapi-5.md) · [0042](docs/adr/0042-rejected-havuzu-tek-kaynak-ve-on-policy-kontrol.md) · [0043](docs/adr/0043-dusunce-modu-acik-butceli-kapatma.md) · **[0052](docs/adr/0052-merge-norm-dengeleme-hukmu-tersine.md)** |
| Otorite tasarım | [`TASARIM.md`](TASARIM.md) · canlı defter [`open_questions.md`](docs/open_questions.md) |
| **Koşu öncesi tuzaklar** | ⭐ [`yurutme-tuzaklari.md`](docs/record/yurutme-tuzaklari.md) |
