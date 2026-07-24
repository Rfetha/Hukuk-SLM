# ADR-0021 — Base teyidi: Gemma 4 12B, **ölçülmüş** gerekçeyle

**Statü:** Yürürlükte · **Tarih:** 2026-07-23
**İlgili:** ADR-0003 (base seçimi) · ADR-0017 (base sabitleme) · ADR-0018 (8GB soft-gate) · ADR-0023 (dağıtım config)
**Sayı kaynağı:** `scripts/kv_cache_compare.py` (commit `02265bb`) · `docs/record/research_log/2026-07-23-base-dogrulama-kv-cache.md`

> **Bu ADR kararı değiştirmiyor — gerekçeyi değiştiriyor.** ADR-0003 ve ADR-0017'nin sonucu
> (base = Gemma 4 12B) ayakta; ama ikisinin de dayandığı bazı gerekçeler **yanlış çıktı.**

## Bağlam

Kullanıcı base kararını yeniden açtı: *"gemma4 12b'yi multimodal encoder-free diye seçtik ama bu
yeterli bir sebep mi — Qwen3.5 9B daha mı iyi olur?"* Ek olarak yeni bir kriter geldi: proje
**tamamen open-weight** hedefliyor ve asıl kullanım **cihazda KV-cache + RAG + inference.**

Karar, **sunk cost sıfırlanarak** yeniden verildi: 5 eğitim koşusu, ~35 judge hücresi ve
confounding maliyeti yok sayıldı; "bugün sıfırdan seçiyor olsaydık" sorusu soruldu.

## Düzeltilen yanlış gerekçeler

1. **"Multimodal / encoder-free" — seçim nedeni değil, olamaz da.**
   ADR-0003 bunu zaten gerekçeden çıkarmıştı (gerekçe-kayması notu). Şimdi **ağırlıklardan da
   doğrulandı:** safetensors başlığında vision = 10 tensör / 49.9M param, audio = **1 tensör /
   2.46M param**, text/decoder = 666 tensör / 11.91B. Google'ın kendi ifadesiyle örtüşüyor
   ("lightweight embedding module: a single matrix multiplication, positional embedding and
   normalizations" · "We removed the audio encoder entirely and projected the raw audio signal
   into the same dimensional space as text tokens").
   → **Ortada encoder yok; algılamanın tamamı decoder'da.** Bu, `target_modules="all-linear"`
   LoRA'nın tam da algılamayı taşıyan katmanlara dokunduğu anlamına gelir. Yani
   *"text-only SFT multimodal yeteneği bozmaz"* iddiası encoder-free mimaride **daha az**
   güvenli, daha çok değil. Ayrıca Google ne multimodal benchmark ne de fine-tuning etkisi
   açıklıyor. → Ölçülene kadar vaat edilmez (probe = TODO, bkz. Sonuç).

2. **"VRAM darboğazı ağırlık değil KV-cache" (ADR-0018:12) — bu base için YANLIŞ.**
   128K bağlamda KV = 1.16 GB, ağırlık = ~6.5 GB → **KV, ağırlığın %18'i.** Darboğaz ağırlık.
   TurboQuant'ın gerçek rolü bellek-darboğazı çözücü değil, **bağlam tavanı kaldıracı**
   (bkz. ADR-0018 düzeltmesi + ADR-0023).

## Karar

**Base = Gemma 4 12B** (`google/gemma-4-12B-it-qat-q4_0-unquantized`) — **teyit.**
Yeni, ölçülmüş gerekçe:

1. **Resmî QAT Q4_0 checkpoint** (ADR-0017'nin gerekçesi — ayakta, en güçlü kalem).
   Tez zinciri: *12B eğit → Q4_0 → ~6.5 GB → tüketici GPU → ~0 marjinal maliyet.* En kırılgan
   halka quantization kaybı; Gemma onu resmî QAT ile garantiliyor. Qwen'de QAT checkpoint **yok**
   (411 topluluk quantizasyonu var, QAT değil) → kayıp doğrudan tezin kalite ekseninden düşer.

> ⚠️ **KISMİ DÜZELTME (2026-07-24): "8 GB'a sığıyor" iddiası masaüstü yükünü saymıyordu.**
> Kullanıcı itirazı: *"128K 7.55 GB istiyorsa o PC'de illaki başka VRAM yiyen app olacak, imkânsız."*
> **Haklı.** 8 GB kartın 8 GB'ı kullanıcıya ait değil — Windows masaüstü compositor + tarayıcı
> tipik 0.5–1.5 GB yer:
>
> | gerçek durum | uygun VRAM | 12B @128K (7.55 GB) | E4B @128K (5.82 GB) |
> | :--- | ---: | :---: | :---: |
> | sadece masaüstü | 7.5 GB | ❌ | ✅ |
> | masaüstü + tarayıcı | 7.0 GB | ❌ | ✅ |
> | çok sekme | 6.5 GB | ❌ | ✅ |
>
> 12B'nin sabiti 6.97 GB → tipik masaüstünde KV'ye **0.03 GB** kalır (~4K bağlam, kullanılamaz).
>
> **Ayakta kalan:** *göreli* iddia — aynı bütçede 12B, Qwen3.5 9B'den fazla bağlam verir (her ikisi
> de aynı masaüstü yükünü çeker). Aile değiştirme reddi geçerli.
> **Düşen:** *mutlak* iddia — "12B gerçek bir 8 GB tüketici PC'sinde uzun bağlamla çalışır."
>
> → **Aile içi küçültme kolu açıldı: Gemma 4 E4B** (`google/gemma-4-E4B-it-qat-q4_0-unquantized`
> — QAT'li, aynı aile/tokenizer/hat → confound yok). Q4_0 ≈ 4.16 GB, @128K toplam **5.82 GB**;
> `num_kv_shared_layers=18` (42 katmanın 18'i KV paylaşıyor) KV dezavantajını (`attention_k_eq_v:
> false`) fazlasıyla kapatıyor. Native bağlam 131K (12B'de 262K). "E4B" = *effective* 4B —
> gerçek ağırlık 14.79 GiB bf16 (~7.4B param, Gemma-3n tarzı per-layer embedding).
>
> **Kullanıcı kararı (2026-07-24): E4B'ye geçilecek — ama ÖNCE ÖLÇÜLECEK.** Kalite hiç ölçülmedi;
> ADR-0021 ölçümle kuruldu, ölçümsüz değiştirilmez. Kapı = task #22 (E4B base, CANON, ~$0.10).
> ⚠️ **Maliyet dürüstçe:** geçiş FT kolunu sıfırlar — LoRA adaptörleri modele özgü, `v2b/v3`
> 12B adaptörleri E4B'de çalışmaz, v4 "v2b-continuation" olarak kilitli. ~5 koşu + ~35 judge
> hücresi yeniden. Tezi geçersiz kılmaz (spec zaten "v0→v3 = proof-of-concept" diyor) ama
> ucuz değil.

2. **8 GB'da 1.9× bağlam tavanı — asıl ürün kriteri.**
   Aynı 8 GB kartta kullanıcının yapıştırabileceği en uzun metin: **Gemma 176.128 tok vs
   Qwen3.5 9B 90.982 tok** (~1.6 tok/kelime TR → ~110 bin vs ~57 bin kelime). Avukat tam dava
   dosyası yapıştırdığında Gemma yutuyor, Qwen 8 GB'ı kırıyor. Bu *nice-to-have* değil **çökme
   sınırı** — ve bandı biz değil kullanıcı seçiyor (medyana değil kuyruğa tasarlanır).

3. **Mimari: token başına 8 KB vs 32 KB.**
   48 katmanın 40'ı `sliding_attention` (win=1024) → bağlamla büyümüyor. Büyüyen 8 `full_attention`
   katmanı **1 KV head × 512 dim**. `attention_k_eq_v: True` → K=V paylaşımlı, cache yarıya iniyor.
   (llama.cpp bunu `llama_kv_cache_iswa` ile gerçekten uyguluyor — doğrulandı.)

4. **Asimetrik risk.** Gemma seçip 16K'da kalmanın bedeli ~1.06 GB boşuna taşınan ağırlık
   (can sıkıcı). Qwen seçip kullanıcının 128K atmasının bedeli 9.22 GB → **ürün çalışmıyor**
   (geri dönüşsüz).

## Değerlendirilen alternatif: Qwen3.5 9B

**Gerçek config'iyle ölçüldü** (`huggingface.co/Qwen/Qwen3.5-9B`, çekildi 2026-07-23) —
ve bu ölçüm **önceki sözlü iddiamı çürüttü.**

| Kriter | Gemma 4 12B | Qwen3.5 9B |
| :--- | :--- | :--- |
| Resmî QAT Q4_0 | ✅ var | ❌ yok |
| Lisans | Apache-2.0 **+ Prohibited Use Policy** | ✅ saf Apache-2.0 |
| KV @32K / @128K | **0.41 / 1.16 GB** | 1.02 / 4.02 GB |
| Toplam @32K / @128K | 6.91 / **7.66 GB** | **6.22** / 9.22 GB |
| Tavan bağlam @8GB | **176.128 tok** | 90.982 tok |
| Ölçülmüş TR hukuk | base M4 0.978 · M2 0.704 | ❓ hiç ölçülmedi |

⚠️ **Kayda geçen düzeltme:** İlk sözlü iddiam *"Gemma 18× KV avantajlı"* idi — **yanlıştı.**
O rakam Qwen**3**'ün hibrit-öncesi mimarisinden geliyordu (324 KB/token). Qwen3.5, 32 katmanın
24'ünü **Gated DeltaNet**'e (lineer attention, sabit durum) çevirmiş; gerçek fark **2.5–3.7×**.
Karar bu düzeltmeden sonra da değişmedi — ama gerekçe artık doğru büyüklükte.

**Kesişim ~64K:** altında Qwen daha hafif, üstünde Gemma kazanıyor ve Qwen 8 GB'ı kırıyor.
Yani mekanizma şu: 12B'nin fazla ağırlığı **tek seferlik sabit maliyet**, KV avantajı ise
**token başına yinelenen kazanç**.

**Qwen'in dürüstçe kabul edilen üstünlükleri:** saf Apache-2.0 (bkz. Sonuç/lisans) ve <64K'da
daha hafif oluş. İkisi de kararı çevirmeye yetmedi.

## Sonuç

- **Repo'nun temel sezgisi tersine döndü:** dokümanlar boyunca "küçük model = erişilebilir"
  varsayılmıştı. Ölçüm diyor ki **8 GB kapısında 12B, 9B'den daha erişilebilir** — çünkü
  erişilebilirlik ağırlık değil, *gerçek kullanım bağlamında ağırlık + KV*. ADR-0018'in
  soft-gate/eğri çerçevesini güçlendirir, gerekçesini düzeltir.
- **Lisans dipnotu (yeni):** repo ~10 yerde Gemma 4'ü "Apache-2.0" diye anıyor — **doğru**
  (model kartı frontmatter `license: apache-2.0`; Gemma 1/2/3'ten farklı olarak Gemma 4
  Apache-2.0'a geçmiş). **Ama eksik:** Google üstüne **Prohibited Use Policy + Intended Use
  Statement** katmanlıyor. "Tamamen open-weight" iddiası kurulacaksa limitations'ta bir cümle
  gerekir. Hukuk asistanı hiçbir yasak kullanımı ihlal etmiyor → pratikte engel yok.
- **Dış geçerlilik** hâlâ kapatılmayan sınır (ADR-0017): bulgular Gemma'ya özgü olabilir.
- **Açık ölçüm borcu:** multimodal probe (repoda tek bir görselli inference testi yok);
  multimodalite kullanılmayacaksa doküman vaatlerini kaldırmak daha ucuz (bkz. ADR-0023 ve
  doküman revizyonu).

## İlgili

`scripts/kv_cache_compare.py` · ADR-0003 · ADR-0017 · ADR-0018 · ADR-0023 ·
`docs/superpowers/specs/2026-07-17-tez-cercevesi-design.md` §3
