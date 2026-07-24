# ADR-0023 — Dağıtım konfigürasyonu: saf Q4_0 + flash-attention + KV q8_0

**Statü:** Yürürlükte · **Tarih:** 2026-07-23
**İlgili:** ADR-0018 (8GB soft-gate) · ADR-0021 (base teyidi) · ADR-0022 (harness kapsamı)
**Sayı kaynağı:** `scripts/kv_cache_compare.py` (commit `02265bb`)

## Bağlam

Tez "tüketici donanımında, dağıtım sınıfında parite" iddia ediyor ama **dağıtım artefaktı hiç
tanımlanmamıştı** — ne quantization ayarı, ne KV ayarı, ne harness'ın nereye yerleşeceği.
Kullanıcı sorusu netleştirdi: *"benim anlattığım harness stack'i Gemma 4 12B Q4_0 ile ≤8 GB
VRAM'e sığıyor mu, nasıl sığdırırız?"*

Yığın: **model + KV-cache + harness (retriever + yapısal graf, ADR-0022 (a))**.

## Ölçüm: sığdırma merdiveni (8 GB hedef)

| # | konfigürasyon | sabit | bağlam |
| :-- | :--- | ---: | ---: |
| 0 | naif: Q6_K embd · bf16 KV · embedder GPU'da | 8.41 GB | **SIĞMIYOR** |
| 1 | retriever+graf CPU'ya (harness = 0 VRAM) | 7.35 GB | 64.755 tok |
| 2 | + saf Q4_0 (token_embd dahil) | 7.12 GB | 95.475 tok |
| 3 | + flash-attention (`-fa`) | 6.97 GB | 115.136 tok |
| **4** | **+ KV q8_0** ← **HEDEF** | **6.97 GB** | **250.752 tok** |
| 5 | + KV q4_0 (agresif) | 6.97 GB | 521.984 tok |

Sabit bütçe kalemleri (basamak 4): Q4_0 ağırlık 6.27 GB + CUDA bağlamı 0.40 GB +
compute buffer (fa'lı) 0.30 GB.

> ✅ **AĞIRLIK ÖLÇÜLDÜ (2026-07-24) — projeksiyon değil artık.** GGUF hattı koştu
> (llama.cpp `0cea362`, CPU build):
>
> | dosya | **gerçek** | projeksiyon | sapma |
> | :--- | ---: | ---: | ---: |
> | `g4-12b-f16.gguf` | **22.20 GiB** | 22.28 | −0.4% |
> | `g4-12b-q4_0-pure.gguf` | **6.26 GiB** | 6.27 | **−0.2%** |
> | `g4-12b-q4_0-default.gguf` | **6.50 GiB** | 6.50 | **0%** |
>
> → **`--pure` farkı 0.24 GiB, ölçüldü.** Kararın 2. maddesi (token_embd Q6_K'ya yükseltilmez)
> hem sayıyla hem ilkeyle (QAT tam Q4_0 için kalibre) doğrulandı. Merdivendeki 6.27 GB satırı
> **6.26 GB** olarak okunmalı; tablo pratikte değişmiyor.
>
> ⚠️ **Dönüştürme engeli ve çözümü (kayda değer):** `convert_hf_to_gguf.py` Gemma 4'ün
> `tokenizer_config.json`'ındaki `extra_special_tokens` alanı **liste** (`['<|video|>']`) olduğu
> için düşüyor — transformers **dict** bekliyor (`AttributeError: 'list' object has no attribute
> 'keys'`). Çözüm: snapshot'ı symlink'lerle kopyalayıp `tokenizer_config.json`'da alanı dict'e
> çevirmek (`{'video_token': '<|video|>'}`). Aynı sorun E4B'de de çıkabilir.
>
> Kalan borç: CUDA bağlamı 0.40 + compute buffer 0.30 hâlâ **tahmin** (CUDA build + `llama-server`
> gerektirir).

## Karar

**Hedef dağıtım konfigürasyonu = basamak 4:**

```
llama-server -m gemma4-12b-q4_0.gguf -ngl 99 -fa on --no-context-shift \
             --cache-type-k q8_0 --cache-type-v q8_0 -c 131072
```

Dört kaldıraç, en önemlisinden:

1. **Harness GPU'ya girmez** (−1.06 GB) — *sığar/sığmaz farkı.* Embedder CPU'da, graf + vektör
   indeksi CPU RAM/disk'te. Embedder'ı GPU'ya koyarsan 8 GB'da yığın ya hiç açılmıyor (fp16) ya
   bağlam sıfırlanıyor (int8 → 750 token). ADR-0022 (a) bunu bedavaya veriyor: deterministik graf
   gezinmesi GPU istemiyor. **Faz 2 harness tasarımına giren kısıt.**
2. **Saf Q4_0 — `token_embd` Q6_K'ya YÜKSELTİLMEZ** (−0.23 GB). llama.cpp varsayılan olarak
   `token_embd`'i Q6_K'ya çıkarır; bizde bu **yanlış**, çünkü QAT checkpoint'i tam olarak **Q4_0
   için** kalibre edildi. Yükseltmek QAT'in optimize ettiği noktadan sapmak demek → hem 0.23 GB
   kazanç hem ilkesel doğru.
3. **Flash-attention** (−0.15 GB) — compute buffer küçülür. Bedava.
4. **KV q8_0** (2.2× bağlam) — pratikte ihmal edilebilir kalite bedeli.

### KV yolu: llama.cpp quant ile başla, TurboQuant sonra

`--cache-type-k/-v q8_0|q4_0` **bugün llama.cpp'de var**, araştırma gerektirmiyor.
**TurboQuant llama.cpp'de yok** — arXiv'de bir yöntem; dağıtım hattımız llama.cpp/GGUF olduğu
için bugün kurulabilir değil. Kullanıcı kararı: **llama.cpp quant ile başlanır, TurboQuant sonra
zorlanır** (paper-implementation işi, tez gövdesine üçüncü araştırma yüzeyi eklemez).

### Bağlam bütçesi: `-c 131072`, 262144 değil *(2026-07-24 eki)*

llama.cpp KV-cache'i **`-c` değerine göre önden tahsis eder** (konuşma uzadıkça büyütmez).
Çalışırken VRAM:

| bağlam | KV (q8_0) | **toplam VRAM** | 8 GB |
| ---: | ---: | ---: | :--- |
| 32K | 0.20 GB | 7.17 GB | ✅ |
| 128K | 0.58 GB | **7.55 GB** | ✅ |
| 256K | 1.08 GB | 8.05 GB | ❌ kıl payı |

→ **Hedef `-c` = 131072** (0.45 GB pay). 262144 istenirse 8 GB'da **yüklenmez** (CUDA OOM,
ilk saniyede — sürpriz yok). KV quant olmadan (bf16) sınır 64K'ya düşer → `--cache-type` opsiyonel
değil, config'in parçası.

> ⚠️ **DOĞRULUK TEHLİKESİ — sessiz kaynak düşürme.** `-c`'ye sığdırılmış ama bağlam dolmuş bir
> istekte llama.cpp varsayılanı **context shift**: en eski token'ları atıp devam eder. Sohbet botu
> için makul, **bizim için felaket** — RAG'de bağlamın başında **getirilen kanun maddeleri** durur;
> shift onları sessizce atar, model kaynağı görmeden cevap üretir ve **hiçbir hata çıkmaz.**
> Ölçtüğümüz groundedness'ın altı boşalır.
>
> **Kural:** `--no-context-shift` + **harness'ta bağlam bütçesi kontrolü** — sığmayan girdi
> *kesilmez, reddedilir.* Bu, red kapısının (harness bileşen 3) doğal görevi; tasarımda yoktu,
> eklendi. Doğru çözüm bağlamı büyütmek değil, **belgeyi de retriever'dan geçirmek** (chunk'la,
> ilgili kısmı getir) — graf + retriever zaten bunun için var.
>
> Ayrıca **262144 = `max_position_embeddings`**; ötesi RoPE tanımsız (YaRN vb. ölçekleme olmadan
> çıktı bozulur) — VRAM meselesi değil, mimari sınır.

### CPU offload ilkesi

Retriever/embedder ve indeks CPU'ya → **bedava** (sorgu başına bir kez, kısa metin).
Model katmanı veya KV → **yasak sayılmaz ama tezin para birimiyle ödenir:** PCIe + DDR5 üzerinden
üretim hızı düşer → GPU-saat başına daha az cevap → birim maliyet artar → **doğrudan
maliyet-normalize parite metriğinden** düşer. Rakip API'ler bu cezayı ödemiyor. Bütçe zaten
kapandığı için gerek de yok; daha fazla bağlam gerekirse doğru kaldıraç **KV quantization**
(az kalite, ölçülebilir) — offload değil (çok throughput).

## Doğrulanan varsayımlar

- llama.cpp **`LLM_ARCH_GEMMA4`** ve `GEMMA4_ASSISTANT` mimarilerini destekliyor → dağıtım hattı
  gerçek (bugüne kadar hiç doğrulanmamış varsayımdı).
- **`llama_kv_cache_iswa`** sınıfı var → 40 sliding katmanın cache'i gerçekten pencereyle sınırlı
  tutuluyor; ADR-0021'in KV hesabının dayandığı varsayım ayakta.

## Sonuç

- **≤8 GB hedefi tutuyor**, ama naif kurulumla tutmuyor — konfigürasyon **tezin bir parçası**,
  detay değil. ADR-0018'in "8 GB = eğri üzerinde işaretli bant" çerçevesini somutlaştırır.
- **Ölçüm borçları (tezde iddia edilmeden önce kapanmalı):**
  1. CUDA bağlamı 0.40 GB + compute buffer 0.45/0.30 GB **tahmin** → gerçek RTX 5070 + gerçek
     GGUF ile ölçülecek. 0.3 GB şaşarsa basamak 4: 250K → ~180K (yine rahat).
  2. Ağırlık 6.27 GB **projeksiyon** — merge → quantize hattı henüz koşulmadı, Q4_0 GGUF yok.
  3. **KV q8_0/q4_0'ın CANON kalitesine bedeli ölçülmedi.** q8_0 genelde ihmal edilebilir,
     q4_0 değil.
- **Ucuz tez katkısı:** KV-bit × bağlam × VRAM × CANON kalitesi eğrisi — ADR-0018'in istediği
  maliyet-performans eğrisinin ta kendisi, ve Türkçe hukuk için kimsede yok.
- **Yeni delik (işaretlendi):** CANON eval'i bf16/NF4 üzerinde koşuyor, dağıtım artefaktı
  Q4_0+q8_0 → *ölçtüğümüz ≠ dağıttığımız.* "Dağıtım sınıfında parite" iddiası için en az bir kez
  aynı CANON'da hizalanmalı.

## İlgili

`scripts/kv_cache_compare.py` · ADR-0018 · ADR-0021 · ADR-0022 · `knowledge/summary_turboquant.md`
