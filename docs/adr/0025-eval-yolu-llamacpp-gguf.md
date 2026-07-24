# ADR-0025 — Eval yolu: Unsloth NF4 → **llama.cpp + Q4_0 GGUF (OpenAI-uyumlu HTTP)**

**Statü:** Yürürlükte · **Tarih:** 2026-07-24
**İlgili:** ADR-0011 (CANON metodoloji) · ADR-0023 (dağıtım config) · ADR-0021/0024 (E4B kolu) · spec §5.2 (adalet kuralı), §6.1
**Etkiler:** `scripts/gen_eval_grounded.py` · `scripts/eval.py` · SCORECARD protokol satırı

## Bağlam

`#22` (E4B vs 12B kapı ölçümü) mevcut eval hattında **koşturulamadı.** Deneme sırası ve sonuçlar:

| yol | 12B | E4B |
| :--- | :--- | :--- |
| **Unsloth 4-bit** (mevcut protokol) | ✅ çalışıyor | ❌ `unsloth_zoo` `gemma4`'ü tanımıyor (`No config file found`) + `libnvJitLink.so.13` eksik + flash-attn bozuk |
| **transformers + bitsandbytes NF4** | — | ❌ ağırlık dönüşüm hatası (`_finalize_model_loading` → CONVERSION; muhtemelen PLE/altup tensörleri) |
| transformers bf16 (quant yok) | — | ⚠️ yükleniyor ama **14.81 GiB** → 12 GB karta sığmıyor, taşmadan 0.9 tok/s |
| **llama.cpp + Q4_0 GGUF** | ✅ **üretildi (6.26 GiB)** | ✅ dönüşüyor |

Yani E4B'yi 4-bit koşturabilen **tek çalışan yol llama.cpp.** Karar stratejik tercihten önce
**pratik zorunluluk**; ama stratejik olarak da doğru çıktı.

## Karar

**Eval generation yolu = `llama-server` (llama.cpp, CUDA) + saf Q4_0 GGUF, OpenAI-uyumlu HTTP.**

Kullanıcı gerekçesi (2026-07-24): *"llama.cpp varsa evalde tek tek model load/unload'lara gerek
kalmayacak."* Doğru — server bir kez yüklenir, tüm modlar HTTP isteğiyle koşar.

### Neden bu, sadece "çalışan yol" olmaktan fazlası

1. **Adalet kuralı artık yapısal garanti.** Spec §5.2 harness'ın tüm öznelere birebir aynı
   uygulanmasını şart koşuyordu — bu bugüne kadar *disiplinle* sağlanacaktı. Artık tek kod yolu:

   ```python
   bizim = OpenAI(base_url="http://localhost:8080/v1", api_key="none")
   rakip = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=...)
   ```

   Aynı istemci, aynı parametreler, aynı harness. Spec zaten rakipler için OpenRouter'ı
   `OpenAI()` uyumlu diye seçmişti; `llama-server` de öyle → **iki taraf tek yoldan akıyor.**

2. **`eval ≠ dağıtım` deliği kapanıyor.** CANON bugüne kadar bf16/NF4 üzerinde koştu, dağıtım
   artefaktı ise Q4_0. "Dağıtım sınıfında parite" iddiası için bu bir açıktı (ADR-0023 Sonuç,
   SCORECARD uyarısı). Artık **ölçtüğümüz = dağıttığımız.**

3. **Üç task ucuzluyor:** VRAM ölçümü (server sürecini ölç), KV-bit × kalite eğrisi
   (`--cache-type-k/-v` bayrağı), eval-dağıtım hizalaması (kendiliğinden).

4. **Kırılganlık azalıyor.** Bugün üç ayrı Unsloth sorunu görüldü. Unsloth bir *eğitim*
   optimizasyon kütüphanesi; çıkarımda ona ihtiyaç yok. **Eğitimde kalır, eval'den çıkar.**

## Bedeli (dürüstçe)

- **Protokol değişimi → 12B base yeniden ölçülmeli.** SCORECARD'ın 35 hücresi Unsloth NF4 ile
  ölçüldü; yükleyici değişince E4B–12B kıyası confound olurdu. *(Not: bu bedel `transformers+bnb`
  seçeneğinde de aynıydı — quantization NF4→Q4_0 değişimi kaçınılmazdı.)*
- **Her model için GGUF gerekiyor.** 12B ✅, E4B 🔄. LoRA adaptörleri merge+convert ister —
  ama base E4B'ye geçerse o adaptörler zaten emekli (ADR-0024).
- **`gen_eval_grounded.py`'nin model yükleme + generate kısmı HTTP'ye çevrilecek.** Skorlama
  script'leri (`score_*.py`, `groundedness.py`) etkilenmiyor — onlar `*_detail.jsonl` okuyor.
- **Eski sayılarla kıyas:** arşive giden 12B/Unsloth hücreleri **tarihsel** kalır; yeni tablo
  Q4_0 tabanlı. İki tablo karıştırılmaz (SCORECARD'da protokol satırı ayrılır).

## Kurulum kararı: **kalıcı**, scratchpad'de değil

2026-07-24'te oturum scratchpad'i temizlendi ve ~22 GiB build + GGUF kayboldu (ölçüm *sonuçları*
git'te olduğu için bilgi kaybı olmadı, sadece yeniden üretim maliyeti). Bu yüzden:

- llama.cpp → `~/code/llama.cpp` · izole venv → `~/code/llamacpp_venv` (global_venv'e dokunulmaz)
- GGUF çıktıları → `models/gguf/` (repo içi, gitignored)
- Kurulum tek komut: `bash scripts/setup_llamacpp.sh [12b|e4b|all]` — idempotent, var olanı atlar

CUDA notu: pip'te CUDA 13 için nvcc yok (yalnız 0.0.1 stub); **cu12 12.9.86** kullanılıyor —
sm_120 (Blackwell) desteği 12.8+ ile geldi, sürücü 13.0 geriye uyumlu.

## Sonuç

- CANON metodolojisi (ADR-0011) **değişmiyor** — modlar, setler, n, seed, hakem aynı. Değişen
  yalnız *generation taşıyıcısı*.
- SCORECARD protokol satırı güncellenecek: `Unsloth 4-bit NF4` → `llama.cpp Q4_0 (--pure) + KV q8_0`.
- Hakem tarafı (gpt-4o-mini) ve `rejection_exact` hakemsiz omurgası aynı kalır.
- ⚠️ **Regex kalibrasyonu (spec §6.1) hâlâ zorunlu ön-adım** — yeni taşıyıcı bunu değiştirmiyor.
