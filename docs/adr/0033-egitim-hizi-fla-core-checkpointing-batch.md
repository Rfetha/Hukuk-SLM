# ADR-0033 — Eğitim hızı: `fla-core` zorunlu · checkpointing kapalı · batch 2×8 (bulut)

**Statü:** Yürürlükte · **Tarih:** 2026-07-25
**Otorite belge:** `TASARIM.md` §4.1 (kol başına QLoRA/LoRA) · **yürütme:** `sprint1.md` CP4
**İlgili:** ADR-0031 (precision — **dropout kilidi bu ADR'de gevşetiliyor**) · ADR-0030 (base) ·
ADR-0028 (tek boyut noktası, *"yerelde $0"* gerekçesi) · ADR-0026 (parametre sessizce varsayılmaz) ·
`gemma4-12b-dersler.md#adr-0004` (12B hattı Modal'daydı)
**Kanıt:** CP4 smoke ölçümleri, 2026-07-25 (aşağıdaki tablo) · `modal_diag.py` çıktısı

---

## Bağlam

Faz B'nin kapısı bir hız sorunuydu. Devir notu (`docs/record/sprint1/NEXT-SESSION.md` §2)
`τ_grounding` eğitimini A100-40GB'de **~36 s/it** ölçmüş, tam koşuyu ~11 saat / ~$25 diye
projekte etmiş ve kabul edilemez bulmuştu. Aynı not kök nedeni şöyle koymuştu:

> `fla` + `causal-conv1d` uzantıları **torch ≥ 2.11** istiyor; bizim lock torch 2.10 →
> Modal image'ı yerelden bağımsız kurulmalı (torch ≥2.11).

**Bu teşhis yanlıştı.** Ölçüldü ve çürütüldü (aşağıda). Doğru teşhis bambaşka bir yerdeydi ve
düzeltmesi pinli ortamı hiç bozmuyor.

---

## Bulgu 1 — `flash-linear-attention` ikiye bölünmüş; `fla-core` ZORUNLU

`flash-linear-attention` 0.5.x'te paket **bölündü**:

| paket | ne taşıyor |
| :--- | :--- |
| `flash-linear-attention` | yalnız `fla/layers`, `fla/models` |
| **`fla-core`** | **`fla/ops/gated_delta_rule`, `fla/modules`** — yani ÇEKİRDEKLER |

Bağ `Requires-Dist: fla-core==<sürüm>` ile kuruluyor. Image `--no-deps` ile kurduğu için
(pinli lock'u korumak adına, doğru bir tercih) **`fla-core` hiç kurulmadı.**

Sonuç, hattın klasik sessiz-bozulma sınıfının yeni bir vakası — ama bu kez **daha kötü**:

- `import fla` **çalışıyor** → `transformers`'ın kapısı
  `is_flash_linear_attention_available()` **True** dönüyor (sadece dağıtım sürümüne bakıyor),
- ama `from fla.modules import FusedRMSNormGated` **çöküyor** → model **hiç yüklenmiyor**.

Yani eksik `fla-core`, fla'nın **hiç olmamasından kötüdür**: "yavaş ama çalışır" yerine
"hiç çalışmaz". Üstelik hata mesajı kök nedeni **gizliyor** — `transformers`'ın tembel-modül
sarmalayıcısı her şeyi tek satıra indiriyor:

```
ModuleNotFoundError: Could not import module 'Qwen3_5ForConditionalGeneration'.
```

Bu satır A100'de, model indirildikten **sonra** görülüyordu → her teşhis denemesi ~25 dk A100.
→ **`modal_diag.py` yazıldı:** aynı image'ı en ucuz GPU'da açıp import zincirini tek tek deneyen
ve **gerçek istisnayı** basan teşhis koşusu. Bundan sonra bu sınıf hatalar saniyeler içinde
ve kuruşuna teşhis edilir.

### Sürüm teşhisi çürütüldü

`fla-core` metadata'sı (ölçüldü, PyPI wheel'inden okundu):

```
Requires-Dist: torch>=2.7.0; extra == "cuda"
Requires-Dist: triton>=3.3;  extra == "cuda"
```

Lock'ta **torch 2.10.0 + triton 3.6.0** var → **ikisi de fazlasıyla yeterli.**
**Ayrı bir torch ≥2.11 Modal image'ı kurmaya gerek YOK; pinli `requirements.lock.txt` korunuyor.**

### `causal-conv1d` bilerek YOK

fla'nın opsiyonel extra'sı (`extra == "conv1d"`), derleme ister. Kaynak okundu
(`transformers/models/qwen3_5/modeling_qwen3_5.py`): çekirdekler **ayrı ayrı** ikame ediliyor —
`causal_conv1d` yalnız depthwise conv'u etkiliyor, **pahalı özyineli çekirdek
(`chunk_gated_delta_rule`) yalnız `fla`'ya bağlı.**

⚠️ **Bunun bir yan etkisi var ve tuzaktır:** `is_fast_path_available` **her ikisini** istediği için
`causal_conv1d` yokken *"The fast path is not available … Falling back to torch implementation"*
uyarısı **yine basılır** — fla çalışıyor olsa bile. **Uyarıyı başarısızlık sanma; ölçüt `s/it`.**

---

## Bulgu 2 — hız kaldıraçları (ölçüm)

`fla-core` eklendikten sonra CP4 smoke (A100-40GB, bf16 taban + LoRA r=16, `max_seq_len=2048`,
batch 1 × grad-accum 16, 17.323 örnek → tam koşu 1083 adım):

| konfigürasyon | s/it (kararlı) | tam koşu | not |
| :--- | ---: | ---: | :--- |
| fla YOK (devir notu) | ~36 | ~11 sa | model yükleniyordu (eski image) |
| **`fla-core` + checkpointing AÇIK + batch 1×16 + dropout 0.05** | **10.5** | **~3.2 sa** | ÇIPA — ölçüldü: adım 10→20 arası 105 s |
| **`fla-core` + checkpointing KAPALI + batch 2×8 + dropout 0.05** | **5.4** | **~1.6 sa** | ✅ **SEÇİLEN** — 50/50 adım 6 dk 52 sn |

**Toplam kazanç 36 → 5.4 s/it = 6.4×**, ve reçetede değişen hiçbir şey yok.

> ### ⚠️ ÖLÇÜM GÜNCELLEMESİ (2026-07-28, CP5 tam koşusu)
>
> **Yukarıdaki 5.4 s/it, 50 adımlık smoke'tan çıkan bir PROJEKSİYONDU. 1083 adımlık gerçek
> koşuda kararlı hız 6.8-7.0 s/it** — ~%27 yavaş, tam koşu ~1.6 sa değil **~2.1 sa**.
> Marjinal hız olduğu için **warmup artefaktı değil** (adım 42→50: 56 sn / 8 = 7.0 · adım
> 50→135: 577 sn / 85 = 6.8). ⚠️ Nihai rakam koşu bitince `research_log` **#41**'e yazılır.
> Muhtemel sebep: 50 adım, 17.323 satırlık setin dizi-uzunluğu dağılımını temsil etmiyor.
>
> **Bağlamı: bu hız bu stack için NORMAL.** Ölçülen verim **2.619 token/s** (ort. 1.146 token ×
> 16 dizi ÷ 7.0 sn); A100-40GB'de yayımlanmış Unsloth rakamı **2.857 token/s** — %8 aşağısındayız.
> **MFU ≈ %15**; aynı kıyaslamada optimize bir framework %39.6 alıyor. Yani fark **framework
> tavanı**, konfigürasyon hatası değil.
>
> **`causal-conv1d` bu tablonun neresinde:** kurulu olmadığı için GatedDeltaNet katmanları
> PyTorch referans yoluna düşüyor (*"The fast path is not available"*). Bu yol **matematiksel
> olarak aynı** — loss/convergence etkilenmez, CP5 çıktısı geçerli — ama o katmanlar ~2-3× yavaş
> ve Qwen3.5-4B'nin **32 katmanının 24'ü** linear-attention. Düşük MFU'yu büyük ölçüde bu açıklıyor.
>
> ### Karar — `causal-conv1d` ERTELENDİ (kullanıcı, 2026-07-28)
>
> **CP5'e dokunulmuyor.** Gerekçe üç kalem:
> 1. **Çıktı geçerli** — fallback matematiksel olarak aynı, loss/convergence etkilenmiyor.
>    Yavaş üretiyoruz, yanlış üretmiyoruz.
> 2. **Bedel önemsiz** — bu koşuda ~$1 fazla; cap $42.50.
> 3. **Kesmek kumar** — koşan işi 10 dk yükleme + belirsizlik karşılığında %27 için durdurmak,
>    sebep henüz ölçülmemişken kötü takas.
>
> **Ama kapatılmadı, planlandı.** Sprint 2'de **4 koşu daha** var (`τa` + Taban A + Taban B×2).
> Kaldıraç orada **bir smoke ile ölçülecek** — 2× çıkarsa ~5 saat ve ~$12 tasarruf. `fla-core`
> dersi gereği (bu ADR'nin kendi konusu) **tahminle yazılmayacak, ölçülecek.**
> Eylem maddesi: `docs/open_questions.md` → Kod borçları.

### Kalite-nötrlüğün KANITI (teori değil, ölçüm)

İki koşu aynı seed (3407), aynı etkin batch (16), aynı veri sırası:

| | adım 10 loss | adım 50 loss |
| :--- | ---: | ---: |
| çıpa (checkpointing açık, batch 1×16) | **0.788** | — *(50'ye gelmeden durduruldu)* |
| seçilen (checkpointing kapalı, batch 2×8) | **0.7987** | 0.3537 |

Adım 10'da fark **0.011** — batching/padding sırasından gelen beklenen fark; öğrenme rejimi
değişmediğinin doğrudan işareti.

**Ve kaydedilen artefakt doğrular** (`/outputs/tg-smoke/checkpoint-50/adapter_config.json`):

```
r = 16 · lora_alpha = 32 · lora_dropout = 0.05 · use_rslora = False · bias = none
target_modules = 11 modül, in_proj_{qkv,z,a,b} DAHİL
```

`use_rslora = False` ayrıca ADR-0031'in ölçekleme kilidini teyit eder: `ΔW = (α/r)·BA` tanımı
bozulmadı → **task-vector tanımı sağlam.**

**`fla-core` tek başına 3.4× kazandırdı.** Devir notunun ~4-5 s/it beklentisi bir *projeksiyondu*,
ölçüm değildi; gerçek 10.5 s/it. Bu ADR'nin ilk kararı bu farkı kayda geçirmektir.

### 🔑 Seçim ölçütü: kaldıraç **kaliteye dokunuyor mu?**

Kullanıcı kuralı (2026-07-25): *"CP4'ü kaliteden kaybetmeden performans kazanalım."*
Kaldıraçlar bu eksende ikiye ayrılır ve **yalnız nötr olanlar alınır**:

| kaldıraç | gradyana etkisi | karar |
| :--- | :--- | :--- |
| `gradient_checkpointing=False` | **Aynı gradyan.** Aktivasyonu yeniden hesaplamak yerine bellekte tutar; tek bedeli VRAM | ✅ alınır |
| `batch↑ × grad_accum↓` (çarpım sabit) | Etkin batch 16 korunur; öğrenme rejimi aynı | ✅ alınır |
| `lora_dropout 0.05 → 0` | **Bir regülarizatörü kaldırır** | ❌ **reddedildi** |
| `causal-conv1d` | Aynı işlemin füzyonlu çekirdeği | ⏸ kapı açık (derleme bedeli) |
| H100 | Aynı matematik, farklı silikon | ⏸ sırada (maliyet nötr, süre yarı) |

Kaldıraçların ikisi de smoke logunun **kendi söylediği** şeylerden çıktı — ve ikisi de aynı kök
hatanın izi: **yerel 12 GB kartın kısıtları bulut koşusuna taşınmıştı.**

1. **`gradient_checkpointing`.** `train_sft.py` bunu `"unsloth"` ile açık tutuyordu ve yanındaki
   yorum sebebini yazıyordu: *"12GB için zorunlu"* — yani **yerel kart** için. A100-40GB'de
   bf16 4.57B ağırlık ~9.1 GB, eğitilebilir 29.9M (%0.65) → **ihtiyacımız olmayan bir bellek
   tasarrufu için hesap gücü ödeniyordu.** Log da bunu doğruluyor:
   *"Unsloth: Will smartly offload gradients to save VRAM!"*
2. **`batch = 1`.** Varsayılanın yanındaki yorum yine aynı şeyi söylüyor:
   *"dar VRAM → batch=1 + gradient_checkpointing ZORUNLU"*. Batch 1'de GPU boş çalışıyor.
   ⚠️ Etkin batch **16 = batch × grad_accum** bir **reçete sabitidir**; ikisi birlikte değiştirilir
   (2×8, 4×4 …), çarpım korunur. ⚠️ Batch'i çok büyütmenin ayrı bir riski var: sözlük **248.320**
   ve logit tensörü batch ile doğrusal büyüyor (ADR-0031'in geri alınan ölçümünün sebebi tam buydu)
   → 2×8 ile başlanır, ölçülerek artırılır.

---

## Karar

1. **`fla-core` image'a eklenir** (`einops`, `fla-core`, `flash-linear-attention`, `--no-deps`).
   `causal-conv1d` eklenmez. Pinli lock korunur, ayrı torch image kurulmaz.
2. **`--no-grad-checkpoint` bayrağı eklenir** ve **bulut koşularında kullanılır.**
   🚫 Yerel 12 GB kartta kullanılmaz (OOM).
3. **`--batch` / `--grad-accum` Modal sarmalayıcısından geçirilir**, bulut koşusu **2 × 8**
   ile başlar (etkin batch 16 korunur). Tek başına verilmeleri **erken patlar** — çarpımın
   sessizce kayması öğrenme rejimini değiştirir ve hiçbir yerde hata vermez.
4. **`lora_dropout = 0.05 KORUNUR.** ADR-0031'in kilidi **kırılmaz.**
   ⚠️ Bu, oturum içinde **geri alınan bir karardır**: önce dropout 0 seçilmiş ve bu ADR o hâliyle
   yazılmıştı; kullanıcının *"kaliteden kaybetmeden"* kuralı üzerine, koşu adım atmadan
   durdurulup geri alındı. Gerekçe aşağıda.
5. **Bütçe kararı (kullanıcı, 2026-07-25):** Modal cap **$35 → $42.50**.

### Neden `dropout = 0` reddedildi

LoRA dropout bir regülarizatördür; asıl işi tekrarlı geçişlerde ezberlemeyi kırmaktır. Bizim
rejimimizde **1 epoch** var (her örnek tam bir kez görülür) → beklenen kayıp **küçüktür**. Reddin
sebebi kaybın büyüklüğü değil, **atfedilebilirliği:**

> CP6'nın işi `τ_grounding`'in **yan hasarını** ölçmek (M2 / M2b / M5, CP2 çıpalarına karşı).
> Aynı koşuya bir reçete sapması karıştırılırsa *"kol mu bozdu, dropout mu"* sorusu **cevapsız
> kalır.** Hattın en pahalı dersleri tam bu sınıftandır: bir koşuda iki şeyi birden değiştirmek,
> ölçümü değil yalnız hızı satın alır.

Kaldıraç **silinmedi, ertelendi**: hız yetmezse ve gerekirse, `dropout=0` **kendi başına** ve
**ölçülerek** denenir — CP5/CP6 karışımında değil.

### Uygulama notu — sessiz-yok-sayma kapısı

`modal_train.py`'de `lora_dropout` varsayılanı **-1.0 = "dokunma"**, `0.0` değil.
Sebep: `0.0` geçerli bir DEĞER ve Python'da falsy → `if lora_dropout:` yazılsaydı
**dropout=0 bayrağı sessizce yok sayılır**, koşu 0.05 ile döner ve fark hiçbir yerde görünmezdi.
Bayrak bugün kullanılmıyor ama kapı doğru kuruldu; erteleme kaldırılırsa hazır.
Bu, ADR-0026'nın *"parametre sessizce varsayılmaz"* kuralının bu dosyadaki karşılığı —
aynı gerekçeyle `--batch`/`--grad-accum` çifti de birlikte-verilme kapısı taşıyor.

---

## Bedel — bu ADR Limitations'a bir şey EKLEMİYOR

Alınan iki kaldıraç da **reçete değişikliği değil**, bu yüzden `Limitations`'a girmezler:

- **`gradient_checkpointing=False`** matematiksel olarak **aynı gradyanı** üretir; yalnız
  aktivasyonları yeniden hesaplamak yerine bellekte tutar. Tek maliyeti VRAM.
- **`batch 2 × grad_accum 8`** etkin batch'i (16) korur; öğrenme rejimi aynıdır.

İkisi de yalnız *"yerel 12 GB kartta kullanılamaz"* notu taşır. ADR-0031'in forgetting frenleri
(**r=16 düşük rank · replay havuzu karışımda · 1 epoch · dropout 0.05**) **dördü de yerinde.**

⚠️ **Yine de karar kuralı yazılır (sonradan rasyonalize edilmesin):** CP6'da M5 anti-hedefi
belirgin **yükselirse** ya da M2b düşerse, bu artık bir hız kaldıracına atfedilemez —
`τ_grounding` kolunun **kendi yan hasarıdır** ve TASARIM'ın öngördüğü sonuçtur (`sprint1.md` CP6
ön-kayıtlı beklentisi). Kaldıraçları kalite-nötr tutmanın amacı tam olarak buydu: **CP6'nın
sonucu tek bir değişkene atfedilebilsin.**

⚠️ **ADR-0028'in *"yerelde $0"* gerekçesine dokunuyor mu?** Hayır — bu ADR eğitimin nerede
koştuğunu değiştirmiyor, yalnız Modal koşusunu ucuzlatıyor. ADR-0031'in karar kuralı (bf16 tabanın
yerel karta sığıp sığmadığı) **hâlâ açık** ve bu ADR onu kapatmıyor.

---

## Elenen alternatifler

| eleme | neden |
| :--- | :--- |
| **torch ≥2.11 ile ayrı Modal image** (devir notunun planı) | Teşhis yanlıştı: `fla-core` yalnız `torch≥2.7`/`triton≥3.3` istiyor. Gereksiz iş + pinli lock'tan sapma riski |
| **`causal-conv1d` derlemek** | Pahalı çekirdek zaten `fla`'dan geliyor; conv fallback'inin payı ölçülmedi ama küçük. Image'a nvcc/derleme sokmanın bedeli kazancından büyük görünüyor. **Kapı açık:** hız yetmezse ilk bakılacak yer burası |
| **`lora_dropout = 0`** | Unsloth'un fast-patch yolunu açardı, ama bir regülarizatörü kaldırır → CP6'nın yan-hasar ölçümünde **atfedilebilirliği bozar** (yukarıda). **Silinmedi, ertelendi:** gerekirse kendi başına ve ölçülerek denenir |
| **H100'e geçmek** | Kabaca 2× hız / 2× fiyat → maliyet nötr, süre yarı. Reçeteye dokunmuyor, **elenmedi — sırada bekliyor**; önce bedava kaldıraçlar ölçülür |
| **`packing=True`** | Kısa örnekleri tek diziye paketleyip throughput'u ciddi artırır, AMA `train_on_responses_only` maskelemesiyle etkileşir → sessiz bozulma riski, hattın en pahalı hata sınıfı. Ölçmeden dokunulmaz |
| **`max_seq_len` düşürmek** | Token bütçesi #39'da ölçüldü (etkilenen %0.06 @ 2048). Düşürmek eval-mirror'ı ve 900-char clip varsayımını kaydırır — hız için ölçüm geçerliliği verilmez |
