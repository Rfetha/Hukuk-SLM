# Sprint 2 — ikinci kol, tabanlar ve zeminin düzeltilmesi

> **Otorite:** [`TASARIM.md`](TASARIM.md) · **bu sprint'in kararları:** ADR-0039 · ADR-0040 ·
> ADR-0041 · ADR-0042 · **ADR-0043** · **tam iş listesi:** [`TODO.md`](TODO.md)
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
`τ_g`'ye dokunmak *(CP0 koşuldu: v2 gerekçesi **çıkmadı**, açık kalemler [`kollar.md`](docs/record/kollar.md)'de bekliyor)*.

---

## Sprint 2'ye girerken bilinenler

| | durum |
| :--- | :--- |
| Eğitilmiş kol | **1** — `τ_g` **v1** (FT-1), 1.083 adım, `‖τ_g‖_F = 10.4589` · künye: [`kollar.md`](docs/record/kollar.md) |
| Çalışan hat | veri → eğitim → merge → GGUF → `llama-server` → eval → hakem, uçtan uca ✅ |
| Ölçüm zemini | DEV havuzu (80 core_hard + 70 trap), TEST (`eval/canon/`) **hiç görülmedi** |
| Çıpalar | base · Gemini 3.1 FL · `τ_g` v1 — ⚠️ **hepsi `--thinking off`**, yani ADR-0043'ten sonra **referans değil** (CP0.9'da yeniden koşulacak) |
| **Protokol** | 🆕 **thinking AÇIK, bütçeli**: düşünce 1024 + cevap 512, zorunlu kapatma (ADR-0043) — rejim değişmezi |
| Bütçe | Modal cap **$42.50** · harcanan ~**$5.8** · **kalan ~$36.7** |

### `τ_g`'nin bıraktığı üç negatif — hangisinin sahibi var

| # | ne bozuldu | base → `τ_g` | Sprint 2'deki sahibi |
| :-- | :--- | :--- | :--- |
| **1** | Cevapladığında hata oranı | %2.7 → **%17.4** *(meta düşülünce %9.9)* | ⚠️ **sahipsiz** — CP0-b hipotezi **çürütüldü** (reçete sert değil: `τ_g` düşünüyor ve duruyor, #42); kalan sahipler CP1 (ölçüm) + Sprint 4 harness |
| **2** | Tuzak reddi (M2) | 0.633 → **0.458** | **FT-2 `τ_a`** — ön-kayıtlı beklenti, bunun için var |
| **3** | Parametrik sızıntı (M5 kütle) | %10.7 → **%14.6** | **FT-2** + **Kapı 6** (ADR-0039) |

---

## Checkpoint akışı

> **Sıra kapılara bağlı.** CP0 ✅ → **CP0.9** → CP1 → CP2 → CP3 → **ARA KAPI** → CP4 → CP5.
> *(CP0.9 yeni: ADR-0043 protokolü değiştirdi, çıpalar yeniden üretilmeden `τ_a` ölçülemez.)*
> Ara kapı geçilmeden rakip yöntemlere para harcanmaz (5/6 kararı, 2026-07-29).

| CP | ne | GPU | $ | kapı |
| :--- | :--- | :--- | ---: | :--- |
| **CP0** | ✅ Düşünce modu — **koşuldu**: base sonlanmıyor, `τ_g` sonlanıyor → **thinking AÇIK, bütçeli** | yerel | **0** | ADR-0043 |
| **CP0.9** | 🆕 **Üç çıpanın yeniden koşulması** (base · Gemini · `τ_g` v1, bütçeli kipte) | yerel/Modal | ~0.6 | ADR-0043 m.4 |
| **CP0.5** | `causal-conv1d` hız ölçümü | yerel | 0 | 2× yoksa yazılmaz |
| **CP1** | Hakem istemi düzeltmesi + üç öznenin yeniden puanlanması | — | ~0.12 | ADR-0041 |
| **CP2** | `rejected` havuzunun base'den yeniden hasadı | yerel | 0 | ADR-0042 |
| **CP3** | **FT-2 = `τ_a`** eğitimi + tekil ölçümü | Modal | ~0.7 | 🔴 **ARA KAPI** |
| **CP4** | **FT-4** Taban A (karışık SFT) + ölçüm | Modal | ~5.7 | — |
| **CP5** | **FT-5/FT-6** Taban B (ardışık SFT) + on-policy kontrol + ölçüm | Modal | ~6.5 | — |
| | **toplam** | | **~$13.65** | kalan bütçe ~$23.05 |

---

## CP0 — Düşünce modu ✅ **KOŞULDU** — ölçüm üretilemedi, karar başka yerden geldi

**Karar belgeleri:** [ADR-0040](docs/adr/0040-dusunce-modu-olculecek-on-kayitli-kural.md) (ön-kayıtlı kural)
→ [**ADR-0043**](docs/adr/0043-dusunce-modu-acik-butceli-kapatma.md) (sonuç) ·
**GPU:** yerel ($0) · **Kayıt:** [`research_log` #42](docs/record/research_log/2026-07-29-cp0-dusunce-modu-sonlanmama.md) ·
**Betikler:** `scripts/cp0_thinking_gen.sh` · `scripts/cp0_thinking_score.sh`

> ### 🚨 Olan şu: base `--thinking on` altında **DURMUYOR**
> M1 · M2 · M5'te `</think>` **hiç kapanmıyor**, `content` boş dönüyor. Kesilme değil
> **sonlanmama**: model cevaplamak ile çekinmek arasında salınıp aynı muhakeme satırını
> **219 kez** tekrarlıyor. Üç açıklama elendi — bütçe **8×** (4096→32768) ❌ · `temp 0.6` 🟡 (yarısı)
> · **Q8_0** ❌. Ve karar eksenlerinin üçü (M1 kütle · M2 Rej · M5 ezber) **tam o üç modda.**
>
> Döngü **belirsizlikle** geliyor: cevabın açık olduğu **M4** (3/3, ort 3.932 tok) ve reddin açık
> olduğu **M3** (3/3, ort 1.126 tok) sorunsuz sonlanıyor.

### Çözüm — bütçeli düşünce (ADR-0043)

```bash
# üretim: 6 mod, düşünce 1024 + cevap 512, zorunlu kapatma, kesik kapısı dahil
THINK_BUDGET=1024 MAXTOK=512 bash scripts/cp0_thinking_gen.sh models/gguf/<gguf> <etiket>
# puanlama: .env yükler, hakem/gateway pinli, ADR-0040 kuralını otomatik uygular
bash scripts/cp0_thinking_score.sh <etiket>
```

Model `</think>`'i bütçe içinde kapatmazsa iz + `</think>` isteme yapıştırılır ve üretim
`/completions` ile sürdürülür → cevap **zorunlu olarak** yazılır (`--think-budget`, `forced_close`).
**Bütçe ön-kayıtlı ve rejim değişmezi** — `TASARIM.md` §4.1.1'e işlendi.

### CP0-b — `τ_g` hasar sensörü ✅ **hasar YOK, tersi çıktı**

`τ_g` v1 aynı istemlerde **35/36 kendi kapatıyor**, medyan **452 token**, düşünce izinde döngü
**yok**, iz yapılı (kaynakları tek tek eleyip gerekçesiyle seçiyor) — base aynı iki istemde
108K/119K karakter üretip hiç bitirmiyor. → *"reçete fazla sertti"* hipotezi **desteklenmedi**;
`τ_g` v2 bu gerekçeyle **açılmıyor** (diğer dört gerekçe: [`kollar.md`](docs/record/kollar.md)).

⚠️ Yan bulgu: iz **8/8 İngilizce**, cevap **8/8 Türkçe** → ürün *"okunabilir iz"* hedefi için
eğitim verisine iz gerekir; v2'nin 4. gerekçesi.

### ⚠️ Bunun Sprint 2'ye faturası

| ne | sonuç |
| :--- | :--- |
| **Sprint 1'in üç çıpası** | `--thinking off` ile ölçüldü → **yeniden koşulacak** (base · Gemini · `τ_g` v1 × 6 mod = 1.410 cevap; GPU $0, Gemini + hakem ≈ **$0.5-0.6**) |
| **ARA KAPI'nın referansı** | `τ_a` artık **0.6330'a karşı ölçülmez** — yeni protokoldeki base sayısına karşı ölçülür |
| **`rejected` hasadı (CP2)** | `--thinking off` değil, **bütçeli düşünce** kipinde (ADR-0042 üst notu) |
| **Maliyet ekseni** | 249 → **~1.198 token/cevap (~4.8×)**, ADR-0017 muhasebesine girer |
| **Ön-kayıtlı 🟢🟡🔴 kuralı** | İptal değil — bütçeli kipte koşulacak, artık *"thinking açılsın mı"*yı değil **RS-FT gerekliliğini** belirliyor |

> **Kalıcı kural (ADR-0040 m.4):** bundan sonra herhangi bir kol yeniden eğitilirse **düşünme
> yeteneğini koruyacak biçimde** eğitilir. Kapıyı açık tutmanın maliyeti eğitim anında ≈ sıfır,
> sonradan yüksek.

---

## CP0.9 — Üç çıpanın bütçeli kipte yeniden koşulması 🆕

**Karar belgesi:** [ADR-0043](docs/adr/0043-dusunce-modu-acik-butceli-kapatma.md) madde 4 ·
**GPU:** yerel/Modal · **$:** ~0.6 (Gemini + hakem) · **Kayıt:** `research_log` #43

Sprint 1'in üç öznesi `--thinking off` ile ölçüldü. Protokol değiştiğine göre **hiçbiri artık
çıpa değil** — `τ_a` bunlara karşı ölçülürse elmayla armut kıyaslanır ve ARA KAPI yanlış okunur.

| özne | ne koşacak |
| :--- | :--- |
| **base** | 6 mod × DEV · bütçeli düşünce (1024+512) · seed 3407 · 900-kar klip |
| **`τ_g` v1** | aynı protokol, `models/gguf/tg_v1-q4_k_m.gguf` |
| **Gemini 3.1 FL** | aynı protokol *(rakip tarafında düşünce bütçesi karşılığı künyeye yazılır)* |

**Toplam 1.410 cevap.** GPU yerelde $0 ama uzun (cevap başına ~1.198 token) → **Modal**'a taşınır;
taşıyıcı **değişmez** (aynı llama.cpp + aynı GGUF + aynı bayraklar — tuzak 1.7).

> ### 🚨 Koşudan önce
> Kesik-cevap oranı **> %5** ise koşu geçersiz (betik otomatik durduruyor) · zorunlu kapatma oranı
> künyeye yazılır · `completion_tokens` ortalaması ADR-0017 muhasebesine girer · Sprint 1'in
> thinking-off sayıları **silinmez**, iki kip yan yana raporlanır.

**Çıktısı:** ARA KAPI'nın iki eşiği (M2 Rej ≥ base+12 puan · M1 A1 ≥ 0.90×base) **sayıyla** dolar,
ve ADR-0040'ın 🟢🟡🔴 kuralı bütçeli kipte koşulup **RS-FT gerekliliğini** belirler.

---

## CP0.5 — `causal-conv1d` hız kaldıracı

**Karar belgesi:** [ADR-0033](docs/adr/0033-egitim-hizi-fla-core-checkpointing-batch.md) ·
**GPU:** yerel · **Kayıt:** `research_log` #43

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
**$:** ~0.12 · **Kayıt:** `research_log` #43

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
**GPU:** yerel ($0) · **Kayıt:** `research_log` #43

Mevcut havuz emekli **12B** hattının fabrikasyonları — yeni modele **başka bir modelin hatalarını**
öğretir. Yeniden hasat: **çıplak base**'den, seed **3407**, aynı üretim ayarları.

> ⚠️ **`--thinking off` DEĞİL** (ADR-0043, 2026-07-29): hasat, kolların eğitileceği ve
> dağıtılacağı kiple aynı olmalı → **bütçeli düşünce (1024 + 512)**. Aksi hâlde negatif örnekler
> modelin gerçekten ürettiği çıktılar olmaz ve ADR-0042'nin kendi *on-policy* gerekçesi çürür.

**Kabul kriteri:** `score_abstention.py` **RED saymıyor** — yani model tuzağa düşmüş, gerçek bir
negatif örnek.

**Tek havuz, tüm kollar** (`τ_a` · Taban A · Taban B'nin iki aşaması) aynı veriyi görür. Gerekçe:
ablasyonun anlamı veriyi sabit tutmaktan gelir.

**Künye kayda geçer:** base sha · **düşünce bütçesi (1024+512) + zorunlu kapatma oranı** · sıcaklık/`top_p` · `max_new_tokens` · seed ·
tarih · kaç örnekten kaçı kabul edildi.

> ⚠️ **Bedel $0 ama süre gerektirir** — hasat boyutu burada ölçülür ve kaydedilir.

---

## CP3 — FT-2 `τ_abstention` + 🔴 ARA KAPI

**TODO:** §2 · **GPU:** Modal · **$:** ~0.7 · **Kayıt:** `research_log` #44

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
τ_a TEKİL olarak M2 Rej'de base'i ANLAMLI biçimde geçmeli.
Eşik: M2 Rej ≥ base + 12 puan
Muhafız: M1 A1 ≥ 0.90 × base — abstention öğretirken grounding çökmemeli
```

> ⚠️ **Sayılar CP0.9'dan gelecek** (ADR-0043). Eski çıpalar — base M2 Rej **0.6330**, eşik 0.75,
> muhafız 0.876 — `--thinking off` protokolündendi ve **artık referans değil.** Bütçeli kipteki
> base sayısı ölçülür ölçülmez bu iki eşik **aynı formülle** (+12 puan · 0.90×) yeniden yazılır;
> formül ön-kayıtlı, sayı değil.

| sonuç | eylem |
| :--- | :--- |
| ✅ geçti | CP4-CP5'e devam — rakip yöntemler koşulur |
| ❌ kaldı | **DUR.** `τ_a` rejimi düzeltilir (epoch · lr · çift sayısı) ve tekrar koşulur. Rakiplere ~$12 harcanmaz |

**Gerekçe:** `τ_a` tutmazsa birleştirilecek ikinci kol yok, Kapı 5'in (b) referansı yok, ve iç
iddia ölçülemez. Rakipleri önce eğitmek, sonucu bilinmeyen bir deneye peşin para yatırmaktır.
82 adım — bekleme ucuz.

> ⚠️ **Bu kapı CP0.9'a bağlandı** (ADR-0043): base bütçeli düşünceyle tuzak reddini zaten
> yükseltiyorsa, `τ_a`'nın referans noktası 0.6330 değil **o sayıdır** — yoksa `τ_a`'ya haksız
> kredi verilir. CP0.9 koşulmadan ARA KAPI okunamaz.

---

## CP4 — FT-4 Taban A: tek-aşamalı **karışık** SFT

**TODO:** §2 · **GPU:** Modal · **$:** ~5.7 · **Kayıt:** `research_log` #45

Grounding + abstention verisi **tek koşuda karıştırılarak** eğitilir. `rejected` havuzu CP2'den
(tek havuz kuralı). Ham base'den.

> ### 🚨 Adil kıyas şartı (ADR-0037)
> **Aynı seçim prosedürü tabanlara da uygulanır** — Taban A için de DEV'de en iyi checkpoint
> seçilir. Yoksa biz taranmış, onlar taranmamış olur ve `D > A` tipi **değersiz** bir iddia çıkar.

6-mod CANON'da ölçülür (harness **kapalı** — iç ablasyon).

---

## CP5 — FT-5/FT-6 Taban B: **ardışık** SFT + on-policy kontrol

**TODO:** §2 · **GPU:** Modal · **$:** ~6.5 · **Kayıt:** `research_log` #45

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
| Cevaplanmış | ✅ `τ_g` reçetesi fazla sert **değildi** (kol düşünüyor ve duruyor) · ✅ düşünce modu bu protokolde **bütçesiz çalışmıyor** · ⏳ bütçeli düşünce ne kazandırıyor (CP0.9) |
| Sprint 3 hazır | Kapı 5'in (a) ve (b) referans noktaları · Kapı 6'nın base çıpası · iki taban |

---

## Kapılar özeti — bu sprint'te işleyenler

| kapı | nerede | kuralı |
| :--- | :--- | :--- |
| ~~CP0 düşünce kuralı~~ | CP0 ✅ | **Kapandı** — ölçüm üretilemedi, karar [ADR-0043](docs/adr/0043-dusunce-modu-acik-butceli-kapatma.md) (thinking AÇIK, bütçeli). ADR-0040'ın eşiği CP0.9'da koşulacak, artık **RS-FT gerekliliğini** belirliyor |
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
| CP0 fiili *(planlanan ~0.15)* | **0** — hakem hiç çağrılmadı, cevap üretilemedi |
| **CP0.9** üç çıpanın yeniden koşulması *(YENİ, ADR-0043)* | −0.60 |
| **Sprint 2 tahmini** | **−13.65** |
| kalan | **~23.05** |

⚠️ **Açık kalemler bütçeye henüz girmedi:** düşünce modu token maliyetini **~4.8×** artırdı
(249 → ~1.198 tok/cevap) — Modal'da koşulan her üretim işi bu oranda uzar. Ve `τ_g` v2 açılırsa
(4 gerekçe: [`kollar.md`](docs/record/kollar.md)) eğitim ~$5.5 + yeniden ölçüm ~$0.15 eklenir.
