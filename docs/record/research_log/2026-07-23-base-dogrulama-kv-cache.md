# 2026-07-23 — Base kararı sunk-cost sıfırlanarak yeniden açıldı: **ölçüm doğruladı, gerekçe değişti**

> **Girdi #37** · Otorite: **ADR-0021** (base teyidi) · **ADR-0022** (graf kapsamı) · **ADR-0023** (dağıtım config)
> Sayı kaynağı: `scripts/kv_cache_compare.py` (commit `02265bb`) — sayılar yerel `config.json`'lardan
> + safetensors başlığından okunur, elle girilmez.

## Tetikleyici

Kullanıcı projeyi arşivleyip (`vOLD-archived`) sıfırdan başlamayı düşündüğünü söyledi. Sorulan
rahatsızlık sebepleri: **(1) sonuçlar ikna etmiyor, (2) base/mimari şüphesi, (3) tez çerçevesi
değişti kod eski.** *("repo/doküman ağırlaştı" şıkkı SEÇİLMEDİ — yani sorun düzen değil, öz.)*

Somut soru: *"gemma4 12b'yi multimodal encoder-free diye seçtik ama bu yeterli bir sebep mi —
Qwen3.5 9B daha mı iyi olur? Paper amacını netledik: tamamen open-weight; asıl kullanım cihazda
KV-cache + RAG + inference."*

Karar **sunk cost sıfırlanarak** yeniden verildi (5 koşu + ~35 judge hücresi + confounding yok sayıldı).

---

## Bulgu 1 — "multimodal/encoder-free" gerekçesi ağırlıklardan çürütüldü

safetensors başlığı sayıldı:

| modality | tensör | parametre |
| :--- | ---: | ---: |
| text/decoder | 666 | 11.91 B |
| vision | 10 | 49.9 M |
| **audio** | **1** | **2.46 M** |

Ses tarafında tek tensör: `model.embed_audio.embedding_projection.weight`. Google'ın resmî
duyurusu birebir aynı şeyi söylüyor: vision = *"a lightweight embedding module consisting of a
single matrix multiplication, positional embedding and normalizations"*; audio = *"We removed the
audio encoder entirely and projected the raw audio signal into the same dimensional space as text
tokens."*

**Sonuç:** ortada encoder yok — ham patch/ses → doğrusal projeksiyon → decoder. **Algılamanın
tamamı decoder'da.** Bu, `target_modules="all-linear"` LoRA'nın tam da algılamayı taşıyan
katmanlara dokunduğu anlamına gelir → *"text-only SFT multimodal yeteneği bozmaz"* iddiası
encoder-free mimaride **DAHA AZ** güvenli, daha çok değil. Ayrıca Google **sıfır multimodal
benchmark** ve fine-tuning etkisine dair **tek cümle** yayınlamıyor.

→ Multimodal, base gerekçesi olamaz (ADR-0003 zaten çıkarmıştı; şimdi ağırlıkla da sabit).
→ Probe testi açık borç; multimodalite kullanılmayacaksa doküman vaatlerini kaldırmak daha ucuz.

## Bulgu 2 — ⚠️ Kendi iddiamı çürüttüm: "18× KV avantajı" YANLIŞTI

İlk sözlü iddiam Gemma'nın Qwen'e karşı **18×** KV avantajlı olduğuydu. **Yanlış.** O rakam
yereldeki **Qwen3**-4B config'inden geliyordu (324 KB/token, 36 katman full-attention).

Gerçek `Qwen/Qwen3.5-9B/config.json` çekildiğinde: Qwen3.5 **hibrit mimariye geçmiş** —
32 katmanın **24'ü Gated DeltaNet** (lineer attention, sabit durum), 8'i klasik attention
(4 KV head × 256 dim). Yani 324 → **32 KB/token**.

```
    bağlam |   Gemma4 12B |   Qwen3.5 9B |    Qwen3 9B* | G avantajı
    32,768 |      0.41 GB |      1.02 GB |     10.12 GB |       2.5×
   131,072 |      1.16 GB |      4.02 GB |     40.50 GB |       3.5×
   262,144 |      2.16 GB |      8.02 GB |     81.00 GB |       3.7×
* hibrit-öncesi Qwen3, 9B'ye ölçeklenmiş — mimari sıçramanın büyüklüğü için
```

Gerçek fark **2.5–3.7×**. Karar değişmedi ama gerekçe artık doğru büyüklükte.

## Bulgu 3 — Kararı belirleyen şey KV değil, **8 GB'da bağlam tavanı**

Toplam ayak izinde (ağırlık + KV) **~64K'da kesişim** var: altında Qwen hafif, üstünde Gemma
kazanıyor ve Qwen 8 GB'ı kırıyor. Asıl ürün sorusu ise "kullanıcı en fazla ne yapıştırabilir":

```
    VRAM |     Gemma4 12B |     Qwen3.5 9B | Gemma başı çekme
    8 GB |    176,128 tok |     90,982 tok |             1.9×
   12 GB |    700,416 tok |    222,054 tok |             3.2×
```

~1.6 tok/kelime TR → **~110 bin vs ~57 bin kelime.** Avukat tam dava dosyası yapıştırdığında
Gemma yutuyor, Qwen 8 GB'ı kırıyor. **Bandı biz değil kullanıcı seçiyor** → medyana değil kuyruğa
tasarlanır. Asimetri: Gemma'da hata bedeli ~1 GB boşuna ağırlık; Qwen'de ürün çalışmıyor.

**Mekanizma (tezin cümlesi olabilir):** 12B'nin fazla ağırlığı **tek seferlik sabit maliyet**,
KV avantajı **token başına yinelenen kazanç**. Bu, repo'nun temel sezgisini tersine çeviriyor —
"küçük model = erişilebilir" varsayılmıştı; ölçüm **8 GB kapısında 12B'nin 9B'den daha erişilebilir**
olduğunu söylüyor.

## Bulgu 4 — ADR-0018'in "darboğaz KV-cache" gerekçesi bu base için yanlış

128K'da KV = 1.16 GB, ağırlık ~6.5 GB → **KV, ağırlığın %18'i.** Darboğaz ağırlık.
Karar (soft-gate + eğri) ayakta, **TurboQuant'ın rolü değişti**: bellek-darboğazı çözücü değil,
**bağlam tavanı kaldıracı**. Üstelik llama.cpp'de yok → bugünkü kaldıraç `--cache-type-k/-v`.

## Bulgu 5 — Tam yığın 8 GB'a sığıyor, ama naif kurulumla sığmıyor

```
0. naif: Q6_K embd · bf16 KV · embedder GPU'da   | 8.41 GB | SIĞMIYOR
1. retriever+graf CPU'ya (harness = 0 VRAM)      | 7.35 GB |  64,755 tok
2. + saf Q4_0 (token_embd dahil)                 | 7.12 GB |  95,475 tok
3. + flash-attention                             | 6.97 GB | 115,136 tok
4. + KV q8_0                       ← HEDEF       | 6.97 GB | 250,752 tok
```

En büyük kaldıraç **harness'ı GPU'dan çıkarmak** (−1.06 GB) = sığar/sığmaz farkı → *retriever CPU'da
koşmak zorunda*, Faz 2 tasarım kısıtı. İkincisi **saf Q4_0**: llama.cpp `token_embd`'i varsayılan
olarak Q6_K'ya çıkarır, bizde bu **yanlış** — QAT tam olarak Q4_0 için kalibre.

Doğrulandı: llama.cpp'de **`LLM_ARCH_GEMMA4`** var (dağıtım hattı gerçek) ve
**`llama_kv_cache_iswa`** var (sliding katmanların cache'i gerçekten pencereyle sınırlı).

## Bulgu 6 — Lisans: repo haklı, ama eksik

Repo ~10 yerde Gemma 4'ü "Apache-2.0" diyor — **doğru** (model kartı frontmatter; Gemma 1/2/3'ün
"Gemma Terms of Use"undan farklı). **Ama** Google üstüne **Prohibited Use Policy + Intended Use
Statement** katmanlıyor. "Tamamen open-weight" iddiası için limitations'ta bir cümle gerekir.
(Qwen3.5 saf Apache-2.0 — bu eksende Qwen önde.)

## Bulgu 7 — Graf kapsamı: literatür (a) ile (b)'yi net ayırdı

Tarama üç makale: **Citation Grounding** (2606.00898, deterministik atıf grafı + zamansal eksen +
algoritmik negatif üretimi), **SAT-Graph RAG** (FAIA251598, Work/Expression ontolojisi),
**LegalGraphRAG** (2605.28120, 3-ajanlı, %6.3-19.1 kazanç ama **maliyet raporu yok**).

→ **ADR-0022:** (a) yapısal/deterministik graf **teze girer** (marjinal ~0 maliyet, determinizmi
korur, atıf-doğrulayıcı zaten gerektiriyor); (b) çok-ajanlı GraphRAG **hariç** (~3× çıkarım →
maliyet-normalize parite iddiasını kendi metriğinden zayıflatır). ADR-0019'un blanket yasağı daraltıldı.
Detay: `knowledge/summary_citation_grounding.md`.

---

## Kararlar (bu girdiden çıkan)

| Karar | ADR |
| :--- | :--- |
| Base = Gemma 4 12B, **teyit** — yeni gerekçe: QAT + 8GB'da 1.9× bağlam tavanı | **0021** |
| Graf: (a) yapısal içeride, (b) çok-ajanlı dışarıda | **0022** (0019'u revize eder) |
| Dağıtım config: saf Q4_0 + `-fa` + KV q8_0 → 6.97 GB / ~250K | **0023** |
| ADR-0018 karar-3 gerekçesi düzeltildi | 0018 (not) |
| Arşivleme/sıfırdan başlama: **yapılmadı** — base ayağı düştü | — |
| `outputs/` ara checkpoint temizliği: 4.5G → 2.5G | — |

## Açık ölçüm borçları

1. CUDA bağlamı 0.40 GB + compute buffer 0.45/0.30 GB **tahmin** → gerçek RTX 5070 + GGUF ile ölçülecek.
2. Ağırlık 6.27 GB **projeksiyon** — Q4_0 GGUF henüz üretilmedi (llama.cpp `gemma4` desteği doğrulandı,
   dönüştürme `transformers` vocab uyumsuzluğunda takıldı).
3. **KV q8_0/q4_0'ın CANON kalitesine bedeli ölçülmedi.**
4. **Eval-dağıtım deliği:** CANON bf16/NF4'te koşuyor, dağıtım Q4_0+q8_0 → *ölçtüğümüz ≠ dağıttığımız.*
5. Multimodal probe hiç koşulmadı.
6. **Zamansal eksen** (mülga/değişik) CANON'da yok — yeni kulvar adayı.

## Paper eşlemesi

- **§Yöntem/Dağıtım:** sığdırma merdiveni + hedef config = "tüketici donanımı" iddiasının somut zemini.
- **§Sınırlar:** lisans dipnotu (Prohibited Use Policy), dış geçerlilik (tek base), multimodal ölçülmedi.
- **§Tartışma:** "12B, 9B'den daha erişilebilir" — erişilebilirlik = ağırlık değil, *kullanım
  bağlamında ağırlık + KV*. Sabit-maliyet vs yinelenen-kazanç çerçevesi.
- **§İlgili çalışma:** Citation Grounding / SAT-Graph / LegalGraphRAG üçlüsü + (a)-(b) ayrımı.
