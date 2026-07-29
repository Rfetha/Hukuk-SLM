# Sprint 2 — ikinci kol, tabanlar ve zeminin düzeltilmesi

> **Otorite:** [`TASARIM.md`](TASARIM.md) · **bu sprint'in kararları:** ADR-0039 · ADR-0040 ·
> ADR-0041 · ADR-0042 · **tam iş listesi:** [`TODO.md`](TODO.md)
> **Önceki sprint:** [`sprint1.md`](sprint1.md) 🔒 kapalı ·
> ⭐ sonuçları [`sprint1-sonuc-tablosu.md`](docs/record/sprint1/sprint1-sonuc-tablosu.md)
>
> ### ⭐ HER KOŞUDAN ÖNCE OKU
> [`docs/record/yurutme-tuzaklari.md`](docs/record/yurutme-tuzaklari.md) — *"hata vermeden yanlış
> sonuç üreten"* kalıpların tek listesi. Bu hattın hata sınıfı **çökme değil, sessiz yanlışlık**.

---

## Sprint 2 tek cümlede

> **Sprint 3'ün birleştirme deneyinin muhtaç olduğu her şeyi üretmek — ve o deneyin adil
> olacağından emin olmak.**

Bitince şu soru cevaplanmış olur: *"İki kolumuz da tek başına ayakta mı, ve rakip yöntemleri
adil koşullarda ölçtük mü?"*

**Kapsam dışı, açıkça:** birleştirme (Sprint 3) · harness (Sprint 4) · parite iddiası (Sprint 5) ·
`τ_g`'ye dokunmak *(şartlı istisna: CP0'ın sonucu — ADR-0040 madde 3)*.

---

## Sprint 2'ye girerken bilinenler

| | durum |
| :--- | :--- |
| Eğitilmiş kol | **1** — `τ_g` (FT-1), 1.083 adım, `‖τ_g‖_F = 10.4589` |
| Çalışan hat | veri → eğitim → merge → GGUF → `llama-server` → eval → hakem, uçtan uca ✅ |
| Ölçüm zemini | DEV havuzu (80 core_hard + 70 trap), TEST (`eval/canon/`) **hiç görülmedi** |
| Çıpalar | base · Gemini 3.1 FL · `τ_g` — üçü de aynı protokolde, **harness kapalı** |
| Bütçe | Modal cap **$42.50** · harcanan ~**$5.8** · **kalan ~$36.7** |

### `τ_g`'nin bıraktığı üç negatif — hangisinin sahibi var

| # | ne bozuldu | base → `τ_g` | Sprint 2'deki sahibi |
| :-- | :--- | :--- | :--- |
| **1** | Cevapladığında hata oranı | %2.7 → **%17.4** *(meta düşülünce %9.9)* | ⚠️ **sahipsiz** — kısmen CP1 (ölçüm), kısmen CP0-b (hipotez), asıl çare Sprint 4 harness |
| **2** | Tuzak reddi (M2) | 0.633 → **0.458** | **FT-2 `τ_a`** — ön-kayıtlı beklenti, bunun için var |
| **3** | Parametrik sızıntı (M5 kütle) | %10.7 → **%14.6** | **FT-2** + **Kapı 6** (ADR-0039) |

---

## Checkpoint akışı

> **Sıra kapılara bağlı.** CP0 → CP1 → CP2 → CP3 → **ARA KAPI** → CP4 → CP5.
> Ara kapı geçilmeden rakip yöntemlere para harcanmaz (5/6 kararı, 2026-07-29).

| CP | ne | GPU | $ | kapı |
| :--- | :--- | :--- | ---: | :--- |
| **CP0** | Düşünce modu ölçümü (a: base thinking-on · b: `τ_g` hasar sensörü) | yerel | ~0.15 | 🟢🟡🔴 ADR-0040 |
| **CP0.5** | `causal-conv1d` hız ölçümü | yerel | 0 | 2× yoksa yazılmaz |
| **CP1** | Hakem istemi düzeltmesi + üç öznenin yeniden puanlanması | — | ~0.12 | ADR-0041 |
| **CP2** | `rejected` havuzunun base'den yeniden hasadı | yerel | 0 | ADR-0042 |
| **CP3** | **FT-2 = `τ_a`** eğitimi + tekil ölçümü | Modal | ~0.7 | 🔴 **ARA KAPI** |
| **CP4** | **FT-4** Taban A (karışık SFT) + ölçüm | Modal | ~5.7 | — |
| **CP5** | **FT-5/FT-6** Taban B (ardışık SFT) + on-policy kontrol + ölçüm | Modal | ~6.5 | — |
| | **toplam** | | **~$13.2** | kalan bütçe ~$23.5 |

---

## CP0 — Düşünce modu: ölçülecek, tartışılmayacak

**Karar belgesi:** [ADR-0040](docs/adr/0040-dusunce-modu-olculecek-on-kayitli-kural.md) ·
**TODO:** §1 · **GPU:** yerel ($0) · **Kayıt:** `research_log` #42

**Neden ilk sırada:** sonucu **RS-FT kararını**, `τ_a`'nın **referans noktasını** ve olası bir
`τ_g` v2'yi belirliyor. Sonra koşulursa, arkasındaki her şey yanlış varsayımla koşulmuş olur.

### CP0-a — base, DEV, `--thinking on`

```bash
# ⚠️ max-new-tokens 4096 — ADR-0030 ölçtü: 1024'te </think> KAPANMIYOR, content BOŞ dönüyor
python scripts/gen_eval_grounded.py \
  --server-url "$SRV" --server-model "$BASE_GGUF" \
  --thinking on --max-new-tokens 4096 --max-chunk-chars 900 \
  --data data/eval/dev/... --out outputs/eval/..._base_think.json
```

> ### 🚨 Geçerlilik ön şartı — sonuçtan ÖNCE kontrol edilir
> Kesik-cevap sayacı **> %5** ise **koşu geçersizdir.** Sonuç okunmaz, bütçe artırılır, tekrarlanır.
> *(Boş `content` zaten `gen_eval_grounded.py` içinde erken patlıyor — ADR-0030 madde 3.)*

**Ön-kayıtlı karar kuralı** — referans: `base --thinking off`, M2 Rej **0.6330** · M1 sadık-cevap
kütlesi **%42.6** · M5 ezber kütlesi **%10.7** · **249 token**/cevap:

```
YEŞİL  →  M2 Rej ≥ 0.78  VEYA  M1 kütle ≥ %57.6      (ikisi de +15 puan)
          VE  M5 ezber kütlesi ≤ %10.7                (Kapı 6 muhafızı)
SARI   →  kazanç var, eşiğin altında — ya da M5 muhafızı ihlal
KIRMIZI→  her iki eksende de kazanç ≤ +5 puan
```

| | eylem |
| :--- | :--- |
| 🟢 | **RS-FT Sprint 2'ye alınır.** ADR-0030 m.2 geri alınır, ADR-0035 yeniden açılır. Sprint 1'in **üç öznesi yeniden koşulur** (~$0.5). Takvim ~3-4 hafta uzar |
| 🟡 | Plan değişmez; thinking **rapor edilen eksen** olur. RS-FT Kapı 6 merdiveninin 4. basamağında bekler |
| 🔴 | ADR-0030 m.2 **kanıtla teyit**. Limitations'taki itiraf **bulguya** döner. RS-FT future-work |

**Token maliyeti kapı değil, raporlanır** — maliyet-normalize parite muhasebesine girer (ADR-0017).

> ⚠️ **YEŞİL sadece iyi haber değil.** Base *hiç eğitilmeden* `τ_a`'nın işinin çoğunu yapıyorsa,
> dış iddiada **üçüncü bir açıklama** belirir: kazanç ince-ayardan mı, harness'tan mı, yoksa
> **modelin zaten sahip olduğu düşünme yeteneğinden mi?** Çıkarsa daraltıcı bulgu olarak yazılır.

### CP0-b — `τ_g` hasar sensörü

`τ_g` `--thinking on` koşulur, **~20 çıktı gözle** incelenir. Kapı değil, **fiyat etiketi**:

| gözlem | anlamı | eylem |
| :--- | :--- | :--- |
| Düzgün akıl yürütüyor | Reçete yumuşak | `τ_g` olduğu gibi devam |
| İlk cümlede `</think>` kapatıyor / bozuk iz | **"Eğitim fazla sertti"** hipotezi güçlenir — 1.083 adım · lr 1e-4 · `all-linear` · r=16. **Sahipsiz doğruluk sorununun (negatif #1) da açıklaması olabilir** | `τ_g` v2 (yumuşak reçete + `build_replay_tr.py` replay karışımı) **masaya gelir** — ama **CP0-a'nın sonucu beklenir**: a YEŞİL ise `τ_g` zaten RS-FT kapsamında yeniden doğar, ayrı v2 israf olur |

> **Kalıcı kural (ADR-0040 m.4):** bundan sonra herhangi bir kol yeniden eğitilirse **düşünme
> yeteneğini koruyacak biçimde** eğitilir. Kapıyı açık tutmanın maliyeti eğitim anında ≈ sıfır,
> sonradan yüksek.

---

## CP0.5 — `causal-conv1d` hız kaldıracı

**Karar belgesi:** [ADR-0033](docs/adr/0033-egitim-hizi-fla-core-checkpointing-batch.md) ·
**GPU:** yerel · **Kayıt:** `research_log` #42

CP5'te ölçüldü: **6.8-7.0 s/it · 2.619 token/s · MFU ≈ %15.** Sebep büyük ölçüde `causal-conv1d`
kurulu olmaması — Qwen3.5-4B'nin **32 katmanının 24'ü** linear-attention ve PyTorch referans
yoluna düşüyor (*"The fast path is not available"*). Fallback **matematiksel olarak aynı**:
çıktı geçerli, yalnız yavaş.

**Yapılacak:** image'a eklenir, **bir smoke** ile s/it ölçülür.

> 🚨 **`fla-core` dersi (#40):** kazanç **ölçülmeden yazılmaz.** O turda "kesin hızlandırır"
> denen paket ölçülünce hiçbir şey değiştirmedi. `requirements.lock.txt` **korunur**;
> eklenen paket ve sürümü kayda geçer.

**Kapı:** ≥2× hızlanma yoksa **eklenmez**, ölçüm negatif bulgu olarak yazılır ve CP3-CP5 mevcut
hızla koşar. 2× çıkarsa Sprint 2'nin üç eğitim koşusunda ~5 saat + ~$12 tasarruf.

---

## CP1 — Hakem istemi düzeltmesi ve yeniden puanlama

**Karar belgesi:** [ADR-0041](docs/adr/0041-raft-meta-iddia-hakem-kurali.md) ·
**$:** ~0.12 · **Kayıt:** `research_log` #42

Groundedness hakem istemine kural satırı eklenir: *kaynak seçimi/eleme hakkındaki meta-cümleler
iddia olarak ayrıştırılmaz.* `base` · `Gemini 3.1 FL` · `τ_g` **üçü birden** yeniden puanlanır.

> ### 🚨 Üç uygulama şartı — üçü de zorunlu
> 1. **TÜM kollara aynı anda.** Tek kola uygulamak sayıyı doğrudan bizim lehimize kaydırır
> 2. **Eski skorlar saklanır** — istem değişikliği `cit_precision`/iddia sayısını kaydırıyor mu, ölçülür
> 3. **Ham sayılar da yayımlanır.** `τ_g`'nin kalan açığı (%9.9 vs %2.7, `CONTRADICTED` 1 → 11)
>    artefakt **değildir** ve maskelenmez

**Ek kontrol:** muafiyet sınırının doğru çizildiği **~20 örnek elle spot-check** ile doğrulanır —
kaynağın *içeriği* hakkındaki iddialar puanlanmaya devam etmeli.

**Etkilenmeyen:** abstention regex'i · atıf doğrulayıcı · register hakemi. Yığın pinlemesi
(ADR-0029/0032) **değişmez**.

---

## CP2 — `rejected` havuzunun yeniden hasadı

**Karar belgesi:** [ADR-0042](docs/adr/0042-rejected-havuzu-tek-kaynak-ve-on-policy-kontrol.md) ·
**GPU:** yerel ($0) · **Kayıt:** `research_log` #42

Mevcut havuz emekli **12B** hattının fabrikasyonları — yeni modele **başka bir modelin hatalarını**
öğretir. Yeniden hasat: **çıplak base**'den (`--thinking off`, seed **3407**, aynı üretim ayarları).

**Kabul kriteri:** `score_abstention.py` **RED saymıyor** — yani model tuzağa düşmüş, gerçek bir
negatif örnek.

**Tek havuz, tüm kollar** (`τ_a` · Taban A · Taban B'nin iki aşaması) aynı veriyi görür. Gerekçe:
ablasyonun anlamı veriyi sabit tutmaktan gelir.

**Künye kayda geçer:** base sha · `--thinking off` · sıcaklık/`top_p` · `max_new_tokens` · seed ·
tarih · kaç örnekten kaçı kabul edildi.

> ⚠️ **Bedel $0 ama süre gerektirir** — hasat boyutu burada ölçülür ve kaydedilir.

---

## CP3 — FT-2 `τ_abstention` + 🔴 ARA KAPI

**TODO:** §2 · **GPU:** Modal · **$:** ~0.7 · **Kayıt:** `research_log` #43

**Rejim** (`TASARIM.md` §4.1.1 ile eşleşmeli): 1.741 çift · **82 adım** (3 epoch) · lr **1e-5** ·
etkin batch **64** · **`--fresh-adapter` ZORUNLU**.

> ### 🚨 `--fresh-adapter` neden zorunlu
> Görev-vektörü tanımı `τ = θ_ft − θ_base`. `τ_a`, `τ_g`'nin **üstüne** eğitilirse elde edilen şey
> task-vector değil **ardışık SFT**'dir — yani ölçmek için kurduğumuz şeyin ta kendisi yok olur,
> ve bunu hiçbir hata mesajı söylemez.

Eğitimden sonra `τ_a` **tekil** olarak 6-mod CANON'da ölçülür (merge → GGUF → aynı runtime).
Bu sayı Kapı 5'in **(b) referans noktasıdır** — onsuz *"abstention korundu mu"* sorulamaz.

### 🔴 ARA KAPI — rakip yöntemlere geçmeden önce

```
τ_a TEKİL olarak M2 Rej'de base'i (0.6330) ANLAMLI biçimde geçmeli.
Eşik: M2 Rej ≥ 0.75            (+12 puan)
Muhafız: M1 A1  ≥ 0.90 × base  (0.876) — abstention öğretirken grounding çökmemeli
```

| sonuç | eylem |
| :--- | :--- |
| ✅ geçti | CP4-CP5'e devam — rakip yöntemler koşulur |
| ❌ kaldı | **DUR.** `τ_a` rejimi düzeltilir (epoch · lr · çift sayısı) ve tekrar koşulur. Rakiplere ~$12 harcanmaz |

**Gerekçe:** `τ_a` tutmazsa birleştirilecek ikinci kol yok, Kapı 5'in (b) referansı yok, ve iç
iddia ölçülemez. Rakipleri önce eğitmek, sonucu bilinmeyen bir deneye peşin para yatırmaktır.
82 adım — bekleme ucuz.

> ⚠️ **CP0-a YEŞİL çıktıysa** bu kapı yeniden değerlendirilir: base düşünerek tuzak reddini zaten
> yükseltiyorsa, `τ_a`'nın referans noktası 0.6330 değil o sayıdır — yoksa `τ_a`'ya haksız kredi
> verilir.

---

## CP4 — FT-4 Taban A: tek-aşamalı **karışık** SFT

**TODO:** §2 · **GPU:** Modal · **$:** ~5.7 · **Kayıt:** `research_log` #44

Grounding + abstention verisi **tek koşuda karıştırılarak** eğitilir. `rejected` havuzu CP2'den
(tek havuz kuralı). Ham base'den.

> ### 🚨 Adil kıyas şartı (ADR-0037)
> **Aynı seçim prosedürü tabanlara da uygulanır** — Taban A için de DEV'de en iyi checkpoint
> seçilir. Yoksa biz taranmış, onlar taranmamış olur ve `D > A` tipi **değersiz** bir iddia çıkar.

6-mod CANON'da ölçülür (harness **kapalı** — iç ablasyon).

---

## CP5 — FT-5/FT-6 Taban B: **ardışık** SFT + on-policy kontrol

**TODO:** §2 · **GPU:** Modal · **$:** ~6.5 · **Kayıt:** `research_log` #44

**FT-5** (aşama 1: grounding, ham base'den) → **FT-6** (aşama 2: abstention, FT-5'in üstüne).

**İki koşu, ADR-0042:**

| koşu | `rejected` kaynağı | nerede raporlanır |
| :--- | :--- | :--- |
| **FT-6 ana** | CP2 havuzu (base'den) | **ana tablo** — veri sabit, fark yönteme atfedilir |
| **FT-6 kontrol** | **FT-5'in kendi çıktısından** (on-policy) | **robustluk satırı** — ~$0.65 |

> ### 🚨 Neden kontrol koşusu var
> Ana koşuda Taban B **off-policy** veriyle eğitiliyor — negatif örnekler FT-5'in modelinin
> gerçekten söylediği şeyler değil → taban **zayıf eğitilir** → sapma **bizim lehimize**.
> *"Tabanı zayıf eğittiniz"* itirazı Kapı 5'in tamamını çürütebilir; $0.65'e sigortalanıyor.

**Ön-kayıtlı yorum kuralı:** on-policy taban, veri-sabit tabandan bileşik ölçütte **≥ +0.05**
iyiyse, Kapı 5'in *"iki tabanı da geç"* şartı **on-policy sürüm** üzerinden okunur — yani daha
güçlü tabana karşı kazanmamız gerekir.

---

## Sprint 2 çıkışında elde ne olacak

| | |
| :--- | :--- |
| Kol | **2** — `τ_g` (var) + `τ_a` (yeni), ikisi de ham base'den, ikisi de tekil ölçülmüş |
| Taban | **2** — karışık SFT · ardışık SFT (+ on-policy kontrol) |
| Zemin | Hakem istemi düzeltilmiş, üç özne yeniden puanlanmış · `rejected` havuzu temiz |
| Cevaplanmış | Düşünce modu bu protokolde ne kadar kazandırıyor · `τ_g` reçetesi fazla sert miydi |
| Sprint 3 hazır | Kapı 5'in (a) ve (b) referans noktaları · Kapı 6'nın base çıpası · iki taban |

---

## Kapılar özeti — bu sprint'te işleyenler

| kapı | nerede | kuralı |
| :--- | :--- | :--- |
| **CP0 düşünce kuralı** | CP0-a | ADR-0040 — 🟢🟡🔴 |
| **CP0.5 hız kapısı** | CP0.5 | ≥2× yoksa eklenmez (ADR-0033, `fla-core` dersi) |
| **ARA KAPI** | CP3 | `τ_a` M2 Rej ≥ 0.75 · M1 A1 ≥ 0.876 |
| **Kapı 5** | Sprint 3 | ADR-0037 (3 madde) — referansları burada üretiliyor |
| **Kapı 6** | Sprint 3 | ADR-0039 — M5 coverage ≤ %37.5 · ezber kütlesi ≤ %10.7 |

---

## Bütçe

| kalem | $ |
| :--- | ---: |
| Modal cap | 42.50 |
| Sprint 1 fiili | −5.80 |
| **Sprint 2 tahmini** | **−13.20** |
| kalan | **~23.50** |

⚠️ **CP0-a YEŞİL çıkarsa** bütçe yeniden hesaplanır: üç öznenin yeniden koşulması (~$0.5) +
RS-FT'nin üretim yükü + olası yeniden eğitimler. Takvim ~3-4 hafta uzar.
