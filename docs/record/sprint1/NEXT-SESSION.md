# NEXT SESSION — kaldığımız yer (2026-07-25 kapanış)

> **Bu belge ne:** oturum kapanırken elde kalan işlerin devir notu.
> **Otorite:** [`TASARIM.md`](../../../TASARIM.md) · **yürütme:** [`sprint1.md`](../../../sprint1.md)
> **Bu oturumun bulguları:** [`research_log #40`](../research_log/2026-07-25-cp4-fla-core-ve-hiz-kaldiraclari.md) ·
> **kararı:** [ADR-0033](../../adr/0033-egitim-hizi-fla-core-checkpointing-batch.md) ·
> **CP7 kaydı:** [`cp7-gemini-onizleme.md`](cp7-gemini-onizleme.md)

---

## 1. Durum özeti

| | durum |
| :--- | :--- |
| **Sprint 1 / Faz A** | ✅ **TAMAMLANDI** (2026-07-24, #39) — 6/6 çıkış ölçütü |
| **CP7 — Gemini önizlemesi** | ✅ **TAMAMLANDI** — kayıt belgesi yazıldı, tüm A1/coverage yeniden hesaplandı |
| **CP4 — smoke + hız** | ✅ **TAMAMLANDI** — 4/4 ölçüt yeşil, **36 → 5.4 s/it (6.4×)**, ADR-0033 |
| **CP5 — `τ_grounding` tam eğitim** | 🔵 **HAZIR, BİLEREK BAŞLATILMADI** (kullanıcı kuralı, 2026-07-25) |
| **CP6 — ölçüm + `research_log #41`** | 🔴 CP5'e bağlı |

> ⚠️ **Önceki devir notunun §2'si (Faz B'yi bloke eden "kritik engel") ARTIK GEÇERSİZ.**
> Teşhisi (*"`fla` torch ≥2.11 istiyor → yerelden bağımsız Modal image kur"*) **ölçülerek
> çürütüldü.** O planı uygulama — gereksiz iş ve pinli lock'tan sapma riski. Doğrusu §2'de.

---

## 2. Faz B'nin kapısı nasıl açıldı (özet — ayrıntı #40'ta)

**Engel sürüm değil, bir paket bölünmesiydi.** `flash-linear-attention` 0.5.x'te ikiye ayrılmış;
çekirdekler (`fla.ops.gated_delta_rule`, `fla.modules`) **`fla-core`** paketinde ve image
`--no-deps` kullandığı için o hiç kurulmuyordu. Sonuç, sessiz-bozulmanın "kötüden de kötü" bir
biçimi: `import fla` çalıştığı için `transformers`'ın kapısı **True** dönüyor ama alt-modül yok →
**model hiç yüklenmiyor.** Hata mesajı da kök nedeni gizliyordu.

**Düzeltme:** image'a `fla-core` eklendi (`modal_train.py`). Pinli `requirements.lock.txt`
**korundu** — `fla-core` yalnız `torch≥2.7` + `triton≥3.3` istiyor, bizde 2.10 + 3.6 var.

**Hız kaldıraçları — yalnız kalite-nötr olanlar alındı** (kullanıcı kuralı: *"kaliteden
kaybetmeden"*): `gradient_checkpointing` kapalı + `batch 2 × grad_accum 8` (etkin batch **16
sabit**). **`lora_dropout=0` reddedildi** — CP6'nın yan-hasar ölçümünde atfedilebilirliği bozardı.

| konfigürasyon | s/it | tam koşu |
| :--- | ---: | ---: |
| fla YOK (eski) | ~36 | ~11 sa · ~$25 |
| `fla-core` + eski ayarlar | 10.5 | ~3.2 sa · ~$7.6 |
| **seçilen** | **5.4** | **~1.9 sa · ~$4.5** *(1.6 sa eğitim + eval/checkpoint payı)* |

⚠️ **`causal-conv1d` bilerek yok** → *"The fast path is not available"* uyarısı **yine basılır.**
Uyarıyı başarısızlık sanma; ölçüt **s/it**.

---

## 3. Sıradaki iş — CP5 (komut hazır, kopyala-koş)

**Ön koşul yok.** Smoke bu komutun `--smoke` hâliyle geçti; tek fark `--smoke` yerine `--epochs 1`.

```bash
source ~/code/global_venv/bin/activate
modal run --detach modal_train.py::spawn_sft \
  --model 'Qwen/Qwen3.5-4B' --data /data/raft_scrubbed --run-name tg --epochs 1 \
  --user-part '<|im_start|>user\n' --assistant-part '<|im_start|>assistant\n' \
  --bf16-base --no-system --no-grad-checkpoint --batch 2 --grad-accum 8 \
  --lr 1e-4 --lora-r 16 --lora-alpha 32 --warmup-ratio 0.05 \
  --target-modules 'q_proj k_proj v_proj o_proj in_proj_qkv in_proj_z in_proj_a in_proj_b gate_proj up_proj down_proj'
```

**İzleme:** `modal app list` → app-id al → `modal app logs <app-id>`.
Filtrelerken `grep -vF "Loading weights"` ekle, yoksa ağırlık çubuğu logu boğuyor.

**Bitince:** `modal volume get hukuk-outputs /tg ./outputs/tg`

### ⚠️ Bu komuttaki üç şey ASLA düşürülmez

| bayrak | düşerse ne olur |
| :--- | :--- |
| `--data /data/raft_scrubbed` | `/raft_scrubbed` **yanlıştır** — volume konteynerde `/data`'ya bağlı. (Artık saniyede patlar, ama yine de doğrusunu yaz.) |
| `--target-modules …` | Varsayılan liste `in_proj_*` içermez → **24 linear-attention katmanı LoRA'sız kalır, hata vermeden.** |
| `--no-system` | Veri kendi system prompt'unu taşıyor → çift system olur. |

🚫 **`--no-grad-checkpoint` YEREL kartta kullanılmaz** (12 GB → OOM). Yalnız A100/H100.

---

## 4. CP6 — ölçüm (CP5 bitince)

`τ_grounding`'i CP2'nin **aynı** 6 modunda, **harness KAPALI**, aynı seed/n/hakem ile koş
(`sprint1.md` CP6). Kıyas **DEV havuzundaki base çıpalarına** karşı — elmayla elma.
Kayıt: `research_log` **#41** (⚠️ #40 bu oturumda CP4'e gitti).

**Ön-kayıtlı beklenti** `sprint1.md` CP6'da yazılı — özellikle **M2'nin düşmesi beklenen bir
sonuçtur**, panik sebebi değil; M2 ve M2b **birlikte** okunur.

---

## 5. Bütçe

| kalem | durum |
| :--- | :--- |
| Modal cap | **$42.50** (kullanıcı kararı 2026-07-25, $35'ten yükseltildi — ADR-0033) |
| Bu oturumda Modal harcaması | smoke denemeleri + teşhis koşuları (biri ~25 dk boşa giden ilk deneme) — **gerçek rakam Modal panelinden teyit edilmeli** |
| CP5 projeksiyonu | ~$4.5 |
| OpenAI hakem | `.env` `OPENAI_BUDGET_USD=5`; bu oturumda ~$0.08 (m4_gem + m5_gem yeniden skorlama) |

---

## 6. Bu oturumda değişen dosyalar (commit EDİLMEDİ)

**Yeni:** `docs/adr/0033-egitim-hizi-fla-core-checkpointing-batch.md` ·
`docs/record/research_log/2026-07-25-cp4-fla-core-ve-hiz-kaldiraclari.md` ·
`docs/record/sprint1/cp7-gemini-onizleme.md` · `modal_diag.py` · `scripts/runlock.py` ·
`outputs/eval/a1_{m1,m4,m5}_base.txt` · `outputs/eval/a1_m5_gem.txt` ·
`outputs/eval/gnd_m{4,5}_gem_summary.run*-BOZUK-DETAY.json` *(eski okumaların yedeği — hakem varyansı kanıtı)*

**Değişen:** `modal_train.py` · `scripts/train_sft.py` · `scripts/{groundedness,score_abstention,score_register,rescore_answered,gen_eval_grounded}.py` ·
`sprint1.md` · `docs/adr/README.md` · `docs/record/research_log/README.md` · `.gitignore`

---

## 7. Bu oturumda kapanan üç kod borcu

1. **Yarış koruması** (`scripts/runlock.py`) — aynı label'a paralel yazan ikinci süreç artık
   **para harcamadan erken patlıyor.** Dört skorlama/üretim scripti kilit alıyor. Test edildi.
2. **`rescore_answered.py` kalibrasyonu ithal ediyor** — kendi kopya red-regex'i #39'un
   kalibrasyonunu almamıştı; üç yanlış-pozitif ölçüldü, hepsi **coverage'ı düşük gösteriyordu**.
   Artık `from score_abstention import REJECT_RE`.
3. **Veri kapısı model yüklemesinin önüne alındı** — yanlış `--data` artık saniyede patlıyor
   (~10 dk A100 yemek yerine).

---

## 8. Açık kalemler (CP7 belgesinden taşınan)

- **Sağlayıcı pinlemesi rakip tarafında kayda geçmiyor:** `gen_eval_grounded.py` OpenRouter'a ham
  HTTP ile gidiyor, `llm_client`'ın `note_provider()` yolunu atlıyor. **Sprint 5 ön koşulu.**
- **Rakip üretim maliyeti ölçülmedi** — `llm_client.PRICE`'ta `gemini-3.1-flash-lite` yok.
- **`sprint1.md` CP2 tablosundaki M2 base regex `0.500`**, `abst_m2_base_summary.json`'daki
  **0.567** ile uyuşmuyor. Değiştirilmedi, işaretlendi.
- **`causal-conv1d`** ve **H100** hız kaldıraçları elenmedi, sırada bekliyor (ADR-0033).

---

## 9. ≤8 GB bütçesi — ölçülen + Graph RAG için ilk TAHMİN

**Ölçülen** (`outputs/eval/vram_stack.json`, Q4_K_M, KV `q8_0`, `-ngl 99 -fa on`, **tek akış**).
⚠️ `server_gib` sunucunun payı; kartın toplamı için **masaüstü/compositor 1.33 GiB** eklenir —
ADR-0031'in Q8_0'ı elerken kullandığı ayrım budur, burada da geçerli.

| bağlam | ağırlık | KV + compute | sunucu payı | + masaüstü = **kart toplamı** |
| ---: | ---: | ---: | ---: | ---: |
| 4.096 | 2.59 | **0.50** | 3.09 | **4.53 GiB** |
| 32.768 | 2.59 | **1.11** | 3.70 | **5.15 GiB** |
| 131.072 | 2.59 | **3.17** | 5.76 | **7.26 GiB** |

Bağlamı **32× büyütmek KV'ye yalnız +2.67 GiB** ekliyor — 32 katmanın 24'ü linear-attention,
KV sadece 8 full-attention katmanında büyüyor (ADR-0031 yan bulgusu).

### Graph RAG — **CPU'da. VRAM katkısı SIFIR.** ⚠️ Aşağıdakiler TAHMİN (harness Sprint 4)

**Yukarıdaki tablo full-stack'tir** — RAG eklenince değişmez, çünkü harness GPU'ya hiç girmiyor
(CLAUDE.md kararı: embedder CPU'da, graf + index CPU RAM/diskte). RAG **sistem RAM'inde** yaşar:

Korpus **ölçüldü**: `data/corpus/mevzuat_maddeler.jsonl` = **40.496 madde**,
900-char clip ile **≈60.300 chunk** (ort. 735 char, medyan 314).

| bileşen | **CPU RAM** (plan) | *(GPU'ya konsaydı)* |
| :--- | ---: | ---: |
| vektör index — 60.3k × 768-dim fp16 | 88 MB *(1024-dim fp32'de 236 MB)* | *~0.09 GiB* |
| embedder — e5-base sınıfı 278M | ~1.1 GB fp32 *(int8 ~0.3 GB)* | *~0.56 GiB* |
| graf — 40k düğüm + atıf kenarları | on-MB'lar | *~0* |
| reranker (opsiyonel, 278M) | ~1.1 GB | *~0.56 GiB* |
| **toplam (reranker'sız)** | **~1.3-1.5 GB RAM** | *~0.65 GiB VRAM* |

**Bedeli tek yerde:** sorgu embedding'i CPU'da → **~10-50 ms** ek gecikme. Model zaten 122.9 t/s
decode ediyor (300 token ≈ **2.4 sn**), yani embedding toplam gecikmenin **~%1'i** — tek
kullanıcıda hissedilmez. Karşılığında **tüm bağlam başlığı** satın alınıyor.

### Embedder GPU'da olmalı mı? — görev döngüsü (duty cycle) argümanı

Embedder **kesikli**, sürekli değil: indeksleme (60.3k forward pass) **bir kez, çevrimdışı**;
runtime'da **kullanıcı turu başına TEK kısa forward pass**. Model cevabı üretirken boşta.
→ %99 boşta duran bir bileşen için kıt 8 GB'tan **0.56 GiB kalıcı** ayırmak, sorgu başına ~30 ms
kazandırır. "İhtiyaç anında GPU'ya yükle" seçeneği elenir (her sorguda ~0.5-1 sn yükleme →
CPU'da koşmaktan kötü).

| senaryo | ctx 4.096 | ctx 32.768 | ctx 131.072 |
| :--- | ---: | ---: | ---: |
| embedder **CPU'da** (plan) | 4.53 ✅ | 5.15 ✅ | 7.26 ✅ *(0.74 başlık)* |
| embedder **GPU'da** (+0.56) | 5.09 ✅ | 5.71 ✅ | **7.82 ❌** *(0.18 başlık)* |

**Yani <8 GB runtime'da her iki durumda da tutuyor — tek istisna embedder-GPU + 131.072.**
Çalışma bandında (4.096-32.768) embedder'ı GPU'ya almak **serbest**, bütçeyi bozmuyor;
sadece 128k bağlamla birlikte olmuyor, ikisinden biri seçilir.

⚠️ **Asıl GPU tartışması reranker üzerinden yapılmalı, embedder üzerinden değil:** reranker
sorgu başına top-k (~20) belgeyi *uzun metinlerle* skorlar → 20 uzun forward pass. Runtime'ın
ağır RAG bileşeni odur. Reranker kullanılacaksa bu tablo yeniden kurulur.

### 131.072 bağlam ne kadar uzun — ve neden ona hiç yaklaşmıyoruz (ÖLÇÜLDÜ)

**Proje sabiti:** Türkçe hukuk metninde **1 token ≈ 3.12 karakter** (gerçek Qwen3.5 tokenizer'ı,
`mevzuat_maddeler.jsonl`'den n=500 rastgele örneklem, seed 3407: 352.483 char / 112.964 token).
Madde başına ortalama **226 token**.

| bağlam | karakter | ~A4 sayfa | ~madde |
| ---: | ---: | ---: | ---: |
| 2.048 | 6.400 | 3 | 9 |
| **4.096** | 12.800 | 6 | 18 |
| 32.768 | 102.200 | 51 | 145 |
| 131.072 | 409.000 | **204** | 580 |

**Fiili runtime bağlamımız ~2.000 token** = 131.072'nin **%1.5'i**: 5 `[KAYNAK]` × 900-char clip
(4.500 char ≈ 1.440 token) + system + soru. `max_seq_len=2048` bu yüzden seçildi (#39: etkilenen %0.06).

**Ve "uzun bağlam" stratejisi bu domende zaten çalışmıyor** — korpustan ölçüldü:

| kanun | madde | ~token |
| :--- | ---: | ---: |
| TÜRK TİCARET KANUNU | 1570 | **~300.700** |
| SOSYAL SİGORTALAR VE GSS | 473 | ~220.700 |
| DEVLET MEMURLARI KANUNU | 848 | ~156.700 |
| İCRA VE İFLAS KANUNU | 520 | ~132.800 |

**En büyük dört kanunun hiçbiri 131k'ya sığmıyor.** Yani bağlamı büyütmek "kanunu modele okut"
çözümünü açmıyor; **RAG tam olarak bu yüzden var.**

→ **Çalışma noktası ctx 4096** (çok turlu sohbet için 8192-32768 rahat tavan).
**131.072 satırı fiilen akademik** — ne VRAM bütçesinde ne ürün tasarımında bağlayıcı.

### KV baştan tahsis ediliyor — "dolu bağlam" ek maliyet getirmiyor

`measure_vram_stack.py` sunucuyu `-c <ctx>` ile açıp yalnız **8 token** üretiyor, yani context
fiilen doldurulmadı. Buna rağmen sayılar geçerli: **llama.cpp KV cache'i `-c`'ye göre BAŞTAN
tahsis ediyor**, dolarken büyütmüyor. Kanıt verinin kendisinde — üç ölçümde de prompt 8 token'dı
ama KV+compute payı 0.50 → 1.11 → **3.17 GiB** diye büyüdü; tembel tahsis olsaydı üçü de aynı
çıkardı. → Tablodaki rakamlar **dolu-KV rakamlarıdır**; 32.768'i tepesine kadar doldurmak
KV tarafına tek byte eklemez.

⚠️ **Ölçülmemiş tek pay:** gerçek bir 32k *prefill*'in compute buffer'ı, 8 token'lık üretimdekinden
bir miktar büyük olabilir. llama.cpp'de bu buffer `-b/--batch-size` (varsayılan 2048) ile
boyutlanır — **context uzunluğuyla değil** — yani sınırlı ve büyük kısmı yükleme anında zaten
tahsisli. 2.3-2.9 GiB başlığı yiyebilmesi gerçekçi değil, ama *"olmalı"* diyoruz, ölçmedik.
**Kapatması ucuz:** yerel kartta `-c 32768` + ~30k token'lık gerçek prompt + `nvidia-smi` tepe
okuması. GPU maliyeti yok. ADR-0031'in VRAM tablosuna *"dolu-KV teyidi"* satırı olarak eklenecek.

### 🟢 SONUÇ — embedder GPU'da olabilir, 131.072 hariç

| senaryo | ctx 4.096 | ctx 32.768 | ctx 131.072 |
| :--- | ---: | ---: | ---: |
| embedder **CPU'da** (plan) | 4.53 ✅ | 5.15 ✅ | 7.26 ✅ *(0.74 başlık)* |
| embedder **GPU'da** (+0.56) | 5.09 ✅ | 5.71 ✅ | **7.82 ❌** |

**Embedder'ı GPU'ya almak ≤8 GB bütçesi açısından YEŞİL** — çalışma bandında (4.096-32.768)
2.3-2.9 GiB başlık kalıyor, dolu KV dahil. **Tek kırıldığı yer 131.072+**, ki oraya zaten
yaklaşmıyoruz (fiili bağlam ~2.000 token) ve en büyük kanunlarımız oraya sığmadığı için uzun-bağlam
stratejisi bu domende çalışmıyor. Yani **hız için embedder GPU'da tutulabilir; 128k ile birlikte
olmaz, ikisinden biri seçilir.**
⚠️ Embedder boyutu **tahmin** (e5-base sınıfı, 278M fp16); model seçilmedi, hiçbir RAG sayısı
ölçülmedi — Sprint 4.

**İki yan bulgu:**
- **Index önemsiz.** 60k chunk'lık korpusta vektör index'i çeyrek GB'ı geçmiyor — "RAG VRAM/RAM
  yer" korkusu bizim ölçeğimizde yersiz. Yer kaplayan tek şey embedder/reranker **ağırlıkları**.
- **Çalışma bandı ctx 4096-32768** (kart toplamı 4.53-5.15 GiB, 2.9-3.5 GiB başlık).
  **131.072 "gösterilebilir tavan", çalışma noktası değil:** 7.26/8 GiB, tek akış, ve son
  kullanıcının masaüstü bizim ölçtüğümüz 1.33 GiB'den ağırsa taşar.

**Açık kalemler:** embedder seçimi yapılmadı (Türkçe kalitesi ayrı karar) · hiçbir RAG sayısı
ölçülmedi · merge sonrası GGUF'un aynı boyutta çıktığı CP6'da teyit edilecek ·
`≤8 GB full-stack` iddiası şu an **tasarım taahhüdü**, ölçüm değil.
