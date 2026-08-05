# #40 — CP4: Faz B'nin kapısı bir paket bölünmesiydi · 36 → 5.4 s/it

**Tarih:** 2026-07-25 · **Faz:** Sprint 1 / Faz B / CP4 (smoke)
**Karar:** [ADR-0033](../../adr/0033-egitim-hizi-fla-core-checkpointing-batch.md)
**Önceki:** [#39](2026-07-24-cp0-base-dogrulama-kapisi.md) (Faz A) · devir notu [`docs/_arsiv/devir-notu-2026-07-29.md`](../../_arsiv/devir-notu-2026-07-29.md) *(2026-08-05'te arşive taşındı — plan belgesiydi, kayıt değil)*
**Paper eşlemesi:** *Methodology* (eğitim konfigürasyonu + reçetenin neden bozulmadığı) ·
**negatif/şaşırtıcı bulgu** (yanlış teşhis + sessiz-bozulmanın yeni bir biçimi) ·
*Reproducibility* (ölçülen s/it ve maliyet)

---

## Özet

Faz B, devir notunda **~36 s/it** (→ ~11 sa / ~$25) diye ölçülmüş bir hız engeliyle bloke edilmişti.
Teşhis *"`fla` torch ≥2.11 istiyor, yerelden bağımsız bir Modal image kurulmalı"* idi.
**Bu teşhis yanlıştı.** Gerçek sebep bir **paket bölünmesi**ydi ve düzeltmesi pinli ortama hiç
dokunmuyor. Düzeltme + iki **kalite-nötr** kaldıraçla hız **36 → 5.4 s/it (6.4×)**, tam koşu
projeksiyonu **~11 sa / $25 → ~1.6 sa / ~$4**. Reçetede değişen hiçbir şey yok.

---

## Bulgu 1 — `flash-linear-attention` bölünmüş; `fla-core` olmadan fla'sız durumdan KÖTÜ

Qwen3.5'in 32 katmanının 24'ü linear-attention. Triton çekirdeği yoksa `transformers` torch
referans uygulamasına düşüyor → ölçülen ~36 s/it.

Paket 0.5.x'te **ikiye bölünmüş** (PyPI wheel metadata'sından okundu):

| paket | içerik |
| :--- | :--- |
| `flash-linear-attention` 0.5.1 | yalnız `fla/layers`, `fla/models` |
| **`fla-core` 0.5.1** | **`fla/ops/gated_delta_rule`, `fla/modules`** — çekirdekler |

Bağ `Requires-Dist: fla-core==0.5.1` ile kuruluyor. Image `--no-deps` kullandığı için
(pinli lock'u korumak adına, doğru bir tercih) **`fla-core` hiç kurulmadı.**

**Sessiz-bozulmanın yeni bir biçimi — bu kez "kötüden de kötü":**

- `import fla` **çalışıyor** → `transformers.utils.import_utils.is_flash_linear_attention_available()`
  yalnız **dağıtım sürümüne** bakıyor (`_is_package_available("fla") and version >= 0.2.2`) → **True**,
- ama `from fla.modules import FusedRMSNormGated` **çöküyor** → **model hiç yüklenmiyor.**

Yani eksik `fla-core`, fla'nın **hiç olmamasından kötüdür**: "yavaş ama çalışır" yerine
"hiç çalışmaz". Ve hata mesajı kök nedeni **gizliyor** — `transformers`'ın tembel-modül
sarmalayıcısı her şeyi tek satıra indiriyor:

```
ModuleNotFoundError: Could not import module 'Qwen3_5ForConditionalGeneration'.
Are this object's requirements defined correctly?
```

Bu satır A100'de, **model indirildikten sonra** görülüyordu → her teşhis denemesi ~25 dk A100.
→ **`modal_diag.py` yazıldı:** aynı image'ı en ucuz GPU'da açıp import zincirini tek tek deneyen
ve **gerçek istisnayı** basan teşhis koşusu. Bu sınıf artık saniyeler ve kuruşlarla teşhis edilir.

### Sürüm teşhisi çürütüldü

`fla-core` metadata'sı: `torch>=2.7.0` · `triton>=3.3` (cuda extra).
Lock'ta **torch 2.10.0 + triton 3.6.0** → **fazlasıyla yeterli.**
**Ayrı bir torch ≥2.11 image'ı gereksizdi; `requirements.lock.txt` korundu.**

### `causal-conv1d` bilerek dışarıda — ve bir uyarı tuzağı

Kaynak okundu (`transformers/models/qwen3_5/modeling_qwen3_5.py`): çekirdekler **ayrı ayrı**
ikame ediliyor. `causal_conv1d` yalnız depthwise conv'u etkiliyor; **pahalı özyineli çekirdek
(`chunk_gated_delta_rule`, satır 535) yalnız `fla`'ya bağlı.**

⚠️ Ama `is_fast_path_available = all((causal_conv1d_fn, causal_conv1d_update,
chunk_gated_delta_rule, fused_recurrent_gated_delta_rule))` **her ikisini** istiyor →
`causal_conv1d` yokken *"The fast path is not available … Falling back to torch implementation"*
uyarısı **fla çalışıyorken de basılır.** **Uyarı ölçüt değildir; ölçüt `s/it`.**

---

## Bulgu 2 — hız kaldıraçları: iki ayar da **yerel kartın kısıtıydı, buluta taşınmıştı**

**Ölçüm koşulları:** Modal **A100-40GB** · `Qwen/Qwen3.5-4B` · bf16 donuk taban + LoRA
(`--bf16-base`, ADR-0031) · r=16 α=32 · 11 modül (`in_proj_*` dahil) · **29.908.992 eğitilebilir
param (%0.65)** · `max_seq_len=2048` · lr 1e-4 cosine · warmup 0.05 · `adamw_8bit` · **seed 3407** ·
veri `/data/raft_scrubbed` (17.323 train) · `--no-system` · 50 adım smoke.

| konfigürasyon | s/it (kararlı) | tam koşu (1083 adım) | kaynak |
| :--- | ---: | ---: | :--- |
| fla YOK | ~36 | ~11 sa · ~$25 | devir notu, önceki oturum |
| `fla-core` + checkpointing AÇIK + batch 1×16 | **10.5** | ~3.2 sa · ~$7.6 | ÇIPA — adım 10→20 arası 105 s |
| **`fla-core` + checkpointing KAPALI + batch 2×8** | **5.4** | **~1.6 sa · ~$4** | ✅ 50/50 adım **6 dk 52 sn** |

`fla-core` tek başına **3.4×**; iki kaldıraç birlikte **toplam 6.4×**.

⚠️ Devir notunun *"~4-5 s/it beklenir"* ifadesi bir **projeksiyondu, ölçüm değildi.**
`fla-core` sonrası gerçek 10.5 s/it çıktı; 4-5 bandına ancak kaldıraçlarla inildi. Kayda geçer:
**projeksiyon ile ölçümü aynı cümlede kullanmamak gerekiyor.**

İki kaldıracın da kökü aynı: **`train_sft.py`'nin varsayılanları yerel 12 GB kart için konmuştu**
ve yorumları bunu açıkça yazıyordu — *"12GB için zorunlu"*, *"dar VRAM → batch=1 ZORUNLU"* —
ama bulut koşusuna olduğu gibi taşınmıştı. A100-40GB'de bf16 4.57B ağırlık ~9.1 GB; ihtiyacımız
olmayan bellek tasarrufu için hesap gücü ve boş GPU ödeniyordu.

---

## Bulgu 3 — kalite-nötrlük iddiası ÖLÇÜLDÜ

Kullanıcı kuralı: *"CP4'ü kaliteden kaybetmeden performans kazanalım."*
Kaldıraçlar bu eksende ayrıldı ve **`lora_dropout = 0` REDDEDİLDİ** (Unsloth'un fast-patch yolunu
açardı; logu *"You are using dropout = 0.05 … causing a performance hit"* diyor). Red sebebi
kaybın büyüklüğü değil **atfedilebilirlik**: CP6'nın işi `τ_grounding`'in yan hasarını ölçmek;
aynı koşuya bir reçete sapması karışırsa *"kol mu bozdu, dropout mu"* sorusu cevapsız kalır.

**Alınan iki kaldıraç kalite-nötr — ve bu teori değil, ölçüm:**

| | adım 10 loss | adım 50 loss | grad_norm (50) |
| :--- | ---: | ---: | ---: |
| çıpa (checkpointing açık, batch 1×16) | **0.788** | — *(durduruldu)* | — |
| seçilen (checkpointing kapalı, batch 2×8) | **0.7987** | **0.3537** | 0.5384 |

Aynı seed, aynı etkin batch (16), aynı veri → adım 10'da fark **0.011**, batching/padding
sırasından gelen beklenen sapma.

**Kaydedilen artefakt doğruluyor** (`hukuk-outputs:/tg-smoke/checkpoint-50/adapter_config.json`):

```
r = 16 · lora_alpha = 32 · lora_dropout = 0.05 · use_rslora = False · bias = none
target_modules = 11 modül, in_proj_{qkv,z,a,b} DAHİL
```

`use_rslora = False` ayrıca ADR-0031'in ölçekleme kilidini teyit eder: `ΔW = (α/r)·BA` bozulmadı
→ **task-vector tanımı sağlam** (iç iddianın aleti).

---

## Bulgu 4 — bu oturumda iki yol tuzağı bir koşu yaktı

1. **`--data` konteyner yoludur, volume yolu değil.** `hukuk-data` volume'ü `/data`'ya bağlanıyor,
   yani volume'deki `/raft_scrubbed` konteynerde **`/data/raft_scrubbed`**. `modal_train.py`'nin
   docstring'i `--data /<set>` diyerek yanlış yönlendiriyordu. Hata **model yüklendikten sonra**
   patlıyordu → ~10 dk A100.
   → **Veri kapısı model yüklemesinin önüne alındı**; artık saniyede patlıyor ve üst dizin içeriğini
   basıyor. Docstring düzeltildi.
2. **`--target-modules` verilmezse `in_proj_*` düşer.** `train_sft.py`'nin varsayılan listesi
   yalnız klasik attention + MLP taşıyor → **24 linear-attention katmanı LoRA'sız kalır**, hata
   vermeden. (`all-linear` de kullanılamıyor: Qwen3.5 bir VLM, görüntü kulesine takıyor — #39.)

---

## Yan iş — CP7 oturumundan taşınan iki kod düzeltmesi

- **Yarış koruması (`scripts/runlock.py`).** Aynı `--label` ile paralel iki skorlama süreci çıktı
  dosyasını sessizce bozuyordu (#39'un sessiz-bozulma sınıfının beşinci vakası; `gnd_m4_gem.jsonl`
  6 satıra, `gnd_m5_gem.jsonl` 0 satıra düşmüştü). `groundedness.py` · `score_abstention.py` ·
  `score_register.py` · `gen_eval_grounded.py` artık çıktıyı açmadan `.lock` alıyor ve ikinci süreç
  **para harcamadan erken patlıyor.** Test edildi.
- **`rescore_answered.py` kalibrasyonu ithal ediyor.** Kendi KOPYA red-regex'ini taşıyordu ve
  docstring'i *"score_abstention ile AYNI"* diyordu — ama #39'un kalibrasyonu yalnız
  `score_abstention.py`'ye işlenmişti, kopya eski kalmıştı. Ölçülen fark (480 cevap): **3 ayrışma,
  üçü de eski kopyanın YANLIŞ-POZİTİFİ** (`kaynaklarda bu …` bir CEVABI red saydı;
  `bulunmazsa` / `bulunmazsanız` kanunun koşul dilini red saydı). Yön tek taraflı: **coverage
  olduğundan düşük** görünüyordu — ve coverage `τ_grounding`'in hedef metriği.
  → Artık `from score_abstention import REJECT_RE`. Etkilenen sayılar CP7 belgesinde yeniden hesaplandı.

---

## Ders

1. **Bir bağımlılık "kurulu" olabilir ve yine de yok olabilir.** Paket bölünmesi + `--no-deps`,
   varlık denetimini (`is_*_available`) yanıltır. Denetim **dağıtım adına** bakıyorsa, gerçek
   ölçüt **import zincirini denemektir.**
2. **Tembel-modül sarmalayıcıları kök nedeni yutar.** Pahalı bir donanımda teşhis etmeye
   çalışmak yerine, **ucuz bir teşhis koşusu yaz** (`modal_diag.py`).
3. **Varsayılanlar taşındıkları bağlamı taşımaz.** `batch=1` ve `gradient_checkpointing` yerel
   12 GB kartın kurallarıydı; buluta olduğu gibi taşınınca 2× hız kaybı olarak geri döndü.
   Yorum satırları sebebi zaten yazıyordu — **okunmadı.**
4. **Hız ile ölçüm geçerliliğini takas etme.** Kaldıraçlar *"gradyanı değiştiriyor mu"* diye
   ayrıldı; değiştirenler (dropout, packing, seq-len) hız uğruna alınmadı — çünkü CP6'nın sonucu
   **tek bir değişkene atfedilebilmeli.**
5. **Ucuz denetimi pahalı adımın önüne koy.** Veri kapısı model yüklemesinden önce; kilit,
   hakem döngüsünden önce. İkisi de aynı ilkenin uygulaması.
