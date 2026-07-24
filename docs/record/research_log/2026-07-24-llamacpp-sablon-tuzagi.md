# 2026-07-24 — llama.cpp hattı ayağa kalktı; **sessiz şablon tuzağı** yakalandı; çekimserlik talimatı M4'ü kırıyor

**Paper eşlemesi:** Yöntem §Deney Kurulumu (ölçüm protokolü + dağıtım artefaktı) · Sınırlılıklar
(araç-kaynaklı ölçüm hataları) · Tartışma (istem tasarımı ↔ çekimserlik/grounding gerilimi)

**Bağlam:** ADR-0025 eval generation yolunu Unsloth NF4'ten llama.cpp + saf Q4_0 GGUF'a taşıdı.
Bu girdi, o hattın ilk uçtan uca ayağa kaldırılışını ve yolda çıkan üç bulguyu kaydeder.

---

## 1. Altyapı: CUDA build'i bir LINK hatası düşürüyordu (çözüldü)

Build "ölmüş" görünüyordu; gerçekte **link aşamasında patlamıştı** ve script'in `tail -5`'i asıl
satırı gizlemişti. Kök neden: `libggml-cuda.so`, `libcudart.so.12` + `libcublas.so.12`'ye referans
veriyor; bunlar sistemde kurulu değil, sudo'suz redistributable dizininde (`~/code/cuda-12.9/lib`).
ld onları bulamıyor → ~200 `undefined reference to cudaFree@libcudart.so.12`.

**Düzeltme (kalıcı, `scripts/setup_llamacpp.sh`):**
```
-DCMAKE_EXE_LINKER_FLAGS="-L$CUDA_HOME/lib -Wl,-rpath,$CUDA_HOME/lib"
-DCMAKE_SHARED_LINKER_FLAGS=<aynısı>
```
`-rpath` ayrıca **çalışma anı** için şart — o olmadan binary üretilir ama açılışta "not found" verir.

Ürünler: `~/code/llama.cpp/build-cuda/bin/{llama-server,llama-cli,llama-quantize}`, sm_120 çalışıyor
(`--list-devices` → RTX 5070 Ti Laptop, 12226 MiB).

---

## 2. ⭐⭐ SESSİZ ŞABLON TUZAĞI — bir CANON koşusunu fark edilmeden çöpe çevirecekti

### Belirti
İlk duman testinde model **hiç durmadı**: cevabı verdikten sonra `<|turn>user` üretip kendi
kendine soru-cevap oynamaya devam etti (220 token, `finish_reason=length`). Bazı çağrılarda
llama.cpp'nin kendi ayrıştırıcısı 500 döndü:
`The model produced output that does not match the expected peg-gemma4 format`.

### Kök neden
Gemma 4'ün resmî sohbet şablonu, **düşünme kapalıyken** üretim isteminin sonuna *boş bir düşünce
kanalı* iliştirir (şablon satır 358-361):

```jinja
{{- '<|turn>model\n' -}}
{%- if not enable_thinking | default(false) -%}
    {{- '<|channel>thought\n<channel|>' -}}      {# reasoning'i bastıran ön-doldurma #}
{%- endif -%}
```

llama.cpp'nin **minja** motoru tanımsız `enable_thinking`'i "tanımlı ve doğru" sayıyor. Sonuç tam
tersine dönüyor: sistem turuna `<|think|>` **giriyor**, ön-doldurma ise **yazılmıyor**.

| ne üretiliyor | doğru | llama.cpp (yamasız) |
| :--- | :--- | :--- |
| sistem turu başı | (yok) | `<\|think\|>` ❌ |
| üretim istemi sonu | `<\|turn>model\n<\|channel>thought\n<channel\|>` | `<\|turn>model\n` ❌ |

### Kanıt — ham `/completion` (sohbet ayrıştırıcısı devre dışı), `scripts/diag_raw_completion.sh`

| istem biçimi | model çıktısı | duruş |
| :--- | :--- | :--- |
| `<\|turn>model\n` (yamasız) | `<\|channel>` açıp girdiyi tekrarlıyor, bozuluyor | `limit` |
| **`<\|turn>model\n<\|channel>thought\n<channel\|>`** | **"genel zamanaşımı süresi 10 yıldır" — doğru** | **`eos`** ✅ |
| sistem turu + `<\|think\|>` | yine bozuk çıkış | `eos` |

### Sonuç: model, GGUF ve saf Q4_0 SAĞLAM
Hata tamamen araç tarafında. `--pure` Q4_0 (ADR-0023) şüphe altına girmişti — **aklandı**.

### Düzeltme
`configs/gemma4_nothink.jinja` = resmî şablon + başına `{%- set enable_thinking = false -%}`.
`llama-server --chat-template-file configs/gemma4_nothink.jinja` ile veriliyor.
Doğrulandı (`scripts/diag_template_load.sh`): render tam olarak
`<|turn>system\nS<turn|>\n<|turn>user\nU<turn|>\n<|turn>model\n<|channel>thought\n<channel|>`.
Düzeltmeden sonra duman testi 11 token'da temiz EOS.

> **Dosya-okuma kanıtı:** `--chat-template-file` gerçekten okunuyor — sahte bir işaret şablonuyla
> test edildi (`ISARET_SABLON_OKUNDU` render'da göründü). Bu, "bayrak sessizce yok sayılıyor"
> ihtimalini eledi.

### Neden bu bir *sessiz* tuzak
Hiçbir aşamada "hata" yoktu: server açılıyor, istek 200 dönüyor, JSON geliyor. Sadece **içerik**
bozuktu. Regex tabanlı `rejection_exact` omurgası ve uzunluk/atıf metrikleri bu çıktılar üzerinde
sayı üretir ve tablo dolar. Duman testi olmasa CANON'un tamamı fark edilmeden zehirlenirdi.

---

## 3. ⭐ Çekimserlik talimatı, cevabı kaynakta olan soruda M4'ü kırıyor

Şablon düzeldikten sonra CANON sistem istemiyle model **yanlış çekimser** kaldı. Kademeli izolasyon
(`scripts/diag_abstain.sh`, aynı soru/kaynak, temperature=0, n=1):

| sistem istemi | cevap |
| :--- | :--- |
| A) yok | ✅ "10 yıldır" |
| B) sadece rol | ✅ "10 yıldır" |
| C) rol + "yalnızca kaynağa dayan" | ✅ "on yıldır" |
| **D) + "kaynakta yoksa 'yer almıyor' de"** (CANON istemi) | ❌ **"Verilen kaynakta bu bilgi yer almıyor."** |

Tetikleyen tek bileşen **çekimserlik talimatı**. Bu bir araç hatası değil, ölçülecek davranış —
ve M4'ün (oracle grounding) var olma sebebi. v0→v3 boyunca gözlenen **Grounding-Abstention
paradoksu**nun (girdi #24) base modeldeki karşılığı: çekimserliği talep etmek grounding'i bozuyor.

> ⚠️ n=1 anekdot. Sayı olarak raporlanmaz; B1/B2'de CANON n'iyle ölçülür.

### Açılan protokol borcu: **düşünme modu kararsız**
Gemma 4 bir *düşünen* model; bizim düzeltmemiz düşünce kanalını **boş** ön-dolduruyor = reasoning
KAPALI. ADR-0023 dağıtım konfigürasyonunu tanımlarken bu ekseni hiç ele almadı. Model muhtemelen
akıl yürütme bütçesi olmadığı için talimatı yüzeysel eşleştiriyor. Bu eksen e2e sayılarını doğrudan
etkiler ve **rakip adaleti** için de kritik (Flash/Sonnet/5-mini'nin reasoning'i açık mı kapalı mı?).
→ B1'den ÖNCE karara bağlanmalı; ADR gerekiyor.

---

## 4. Ölçüm: 12B @128K + KV q8_0 gerçek VRAM — **projeksiyonun ÜSTÜNDE**

| kaynak | değer |
| :--- | :--- |
| `kv_cache_compare.py` projeksiyonu (ağırlık + KV) | 6.97 GB |
| ölçüm (server süreci payı, `-c 131072 -fa --cache-type-k/-v q8_0`) | **7.86 – 8.52 GiB** |

⚠️ **Bu ölçüm kirli** — E4B dönüşümü aynı anda koşuyordu, taban okuması 1268 ve 3695 MiB arasında
oynadı. Temiz ölçüm B4'te tekrarlanacak. Yine de yön kesin: **gerçek > projeksiyon**, fark
compute buffer + CUDA bağlam ek yükünden (projeksiyon yalnız ağırlık + KV sayıyordu).

**Tez açısından:** ADR-0021'in kısmi düzeltmesini (masaüstü VRAM yükü → E4B kolu) *güçlendiriyor*.
Ek ampirik destek: boştaki masaüstü bile karttan **1.2 GB** yiyor (`--list-devices`: 12226 toplam /
11026 boş). 8 GB'lık bir kartta 12B için pratikte yer yok.

**Üretilen artefakt:** `g4-12b-q4_0-pure.gguf` = **6.26 GiB** (2026-07-23 referansıyla birebir).
Hız: ~22-48 tok/s (tek istek, kısa üretim, dönüşümle yarışırken — gösterge amaçlı).

---

## Dersler

1. **Yeni bir generation taşıyıcısı = yeni bir sessiz-bozulma yüzeyi.** Taşıyıcı değiştiğinde
   200-OK yeterli değil; *içeriğin* biçimi elle doğrulanmalı. Duman testi opsiyonel değil.
2. **Şablonu modelin kendi dosyasından almak yetmez** — motorun (minja) onu nasıl değerlendirdiği
   ayrı bir değişken. Render'ı gözle görmek (`/apply-template`) tek güvenilir yol.
3. **Bir bayrağın etkisiz kalması ile yok sayılması farklı şeyler** — sahte-işaret testiyle ayırt et.
4. Ölçüm ile projeksiyon ayrıldığında **projeksiyonun neyi saymadığını** ara (burada: compute
   buffer + bağlam ek yükü), sayıyı "yaklaşık tutuyor" diye geçme.

## Üretilen/değişen dosyalar

- `configs/gemma4_nothink.jinja` — yamalı şablon (düzeltmenin kendisi)
- `scripts/setup_llamacpp.sh` — linker bayrakları (kalıcı düzeltme)
- `scripts/smoke_llamacpp.sh` — A4 duman testi + VRAM delta ölçümü
- `scripts/diag_chat_template.sh` · `diag_template_fix.sh` · `diag_template_load.sh` ·
  `diag_raw_completion.sh` · `diag_abstain.sh` — tanı zinciri (yeniden koşturulabilir)
