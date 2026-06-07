# HakHukuk — Fine-Tuning Teknik Araştırması

> **Amaç:** Faz 1'de Türk hukuk diline adapte edilmiş bir SLM üretmek için fine-tuning stratejisini, donanım kısıtlarını ve teknik kararları belgelemek.
>
> **Kısıt:** Yerel donanım — ASUS ROG Strix G16 G614FR (RTX 5070 Laptop, **12 GB VRAM**, Blackwell sm_120, CUDA 13.1; AMD Ryzen 9 9955HX 16-core, 32 GB DDR5).
>
> ⚠️ **Düzeltme (2026-05-29):** Bu dokümanın eski sürümleri "RTX 4070 / 8 GB / 13th gen Intel" diyordu — **yanlış**. Gerçek rig yukarıdaki. **8 GB rakamı bizim eğitim rig'imiz değil, son-kullanıcı erişilebilirlik hedefi** (ürün ~8 GB tüketici GPU'da koşmalı). 12 GB bize 4B model için rahat yerel QLoRA alanı verir. Blackwell sm_120 + CUDA 13.1 bleeding-edge → PyTorch/bitsandbytes/flash-attn/Unsloth için Blackwell-uyumlu wheel şart (eski "CUDA 12.1" geçersiz).

---

## 1. Donanım Gerçekliği

### Yerel makine (G614FR)

| Bileşen | Değer | FT açısından anlamı |
| :--- | :--- | :--- |
| GPU | RTX 5070 Laptop, **12 GB VRAM** | 7B+ tam FT yine yok; ama 4B QLoRA için rahat alan — yerelde gerçek SFT, sadece smoke test değil. |
| CUDA | **Blackwell (sm_120), CUDA 13.1** | ⚠️ Bleeding-edge. Blackwell-uyumlu wheel şart (bitsandbytes/flash-attn/Unsloth). Eski "sm_89 / CUDA 12.1" geçersiz. |
| CPU | AMD Ryzen 9 9955HX (16-core) | Veri ön işleme/temizleme bol bol yeter. |
| RAM | 32 GB DDR5 (5600 MT/s) | Veri ön işleme + dataset yükleme için rahat. |
| Depolama | NVMe SSD (954 GB) | Checkpoint I/O sorun değil. |

### 12 GB VRAM'de gerçekçi ne sığar (QLoRA 4-bit)

| Model | Yaklaşık VRAM | Yorum |
| :--- | :--- | :--- |
| Gemma 3 270M | ~1.5 GB | Pipeline doğrulama / smoke test. |
| 2–3B (Phi-3.5-mini vb.) | ~5–6 GB | Rahat, hızlı iterasyon. |
| Qwen3.5-4B (eski plan) | ~8–10 GB | Referans; artık seçilen model değil. |
| **Gemma 4 12B QAT-unquantized (seçilen baz)** | ~11–12 GB | batch=1 + gradient_checkpointing zorunlu. **Sıkışık ama mümkün.** |
| 7B (Mistral, Llama-3-8B vb.) | ~14–18 GB | **Sığmaz.** Colab/Kaggle/RunPod'a kaçar. |

> **ℹ️ 8 GB nereden geliyor?** 8 GB rakamı **ürün erişilebilirlik hedefi** (model son-kullanıcının ~8 GB tüketici GPU'sunda koşmalı) — bizim eğitim rig'imiz değil. Eğitimi 12 GB'de yapıp 4-bit'i 8 GB'a sığacak şekilde ölçeriz.

**Sonuç:** 12 GB yerel makine **4B QLoRA SFT'yi gerçekten koşturur** (prototip + tek-konfig eğitim). Ablation sweep / büyük koşu yine bulutta (Colab Pro A100 40GB veya RunPod).

### Bulut seçenekleri (asıl koşu için)

| Sağlayıcı | GPU | Saat ücreti (yaklaşık 2026) | Kullanım |
| :--- | :--- | :--- | :--- |
| Google Colab Pro+ | A100 40GB / L4 22GB | $50/ay quota | Birincil tercih (Unsloth + ücretsiz tier başlangıç) |
| Kaggle | 2× T4 16GB / P100 | Ücretsiz, 30h/hafta | Yedek + benchmark koşusu |
| RunPod | A100 80GB / H100 | $1.5–3/saat | Final eğitim koşusu |
| Lambda Labs | A100 / H100 | $1.3+/saat | Alternatif |

---

## 2. Fine-Tuning Yöntem Karşılaştırması

| Yöntem | VRAM | Kalite | Hız | Bizim için |
| :--- | :--- | :--- | :--- | :--- |
| **Full FT** | Çok yüksek (40GB+) | En iyi | Yavaş | ❌ Donanım yetmez. |
| **LoRA** (16-bit base) | Orta-yüksek | Çok iyi | Orta | ⚠️ 4B 16-bit base 12 GB'a zor sığar; QLoRA daha güvenli. |
| **QLoRA** (4-bit base + LoRA) | Düşük | İyi (full FT'e ~%99 yakın) | Orta | ✅ **Birincil seçim.** |
| **DoRA** | QLoRA + ~%10 | LoRA'dan iyi | Biraz yavaş | 🔬 Faz 2'de denenebilir. |
| **GaLore** | Düşük-orta | Full FT'e yakın | Yavaş | 🔬 Araştırma kıyası için ilginç. |
| **Prompt/Prefix Tuning** | Çok düşük | Sınırlı | Hızlı | ❌ Domain adaptasyonu için yetersiz. |

**Karar:** **QLoRA** (NF4 quantization + LoRA adapters). Akademik olarak `arXiv:2305.14314` referansı.

### LoRA Hiperparametreleri (başlangıç)

```python
LoraConfig(
    r=16,                    # rank — 8/16/32 ile sweep
    lora_alpha=32,           # genelde 2*r
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],                       # all-linear hedefleme
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
```

---

## 3. Yazılım Yığını

| Katman | Seçim | Gerekçe |
| :--- | :--- | :--- |
| Base framework | **PyTorch 2.4+** | Standart. |
| FT kütüphanesi | **Unsloth** | ~2× hız, %60 daha az VRAM. ⚠️ Blackwell (sm_120) için son-sürüm wheel şart. Akademik makale ile referanslanabilir. |
| Alternatif | TRL + PEFT + transformers | Unsloth desteklemediği bir model için. |
| Quantization | bitsandbytes 0.43+ | NF4, double quantization. |
| Attention | FlashAttention-2 | Blackwell sm_120 için uyumlu wheel gerekir; uzun seq için kritik. |
| Eval | lm-eval-harness + custom Türk hukuk benchmarkı | Standart + bizim katkımız. |
| Deney takibi | Weights & Biases (akademik free tier) | Tez'de grafikler için. |
| Ortam | uv (paket) + Python 3.11 | Hız + reproducibility. |
| Versiyonlama | DVC veya HF Hub (model + dataset) | Reproducibility. |

### Kurulum sırası (Windows + WSL2 önerilir)

```
WSL2 Ubuntu 22.04
└── CUDA (Blackwell-uyumlu; 13.x — kesin sürüm kurulumda doğrulanır)
    └── Python 3.11 (uv)
        └── PyTorch (sm_120 destekli build)
            ├── unsloth
            ├── bitsandbytes
            ├── transformers
            ├── trl
            ├── peft
            ├── datasets
            ├── accelerate
            └── flash-attn
```

> Native Windows'ta da çalışır ama bitsandbytes/flash-attn için WSL2 daha az ağrı verir.

---

## 4. Veri Pipeline'ı

### 4.1 Kaynaklar (Faz 1)

> ⚠️ **Bu tablo ilk taslaktır — güncel/otoriter veri planı `docs/VERI_PLANI.md`.** Orada EDA ile doğrulanmış setler (OrionCAF, Renicames), reddedilenler (EuroHPC), canlı kanun API'si (Bedesten) ve grounded üretim pipeline'ı var. Aşağıdaki tablo tarihsel bağlam.

| Kaynak | Tip | Lisans | Tahmini hacim |
| :--- | :--- | :--- | :--- |
| Kaggle Turkish Law Dataset | Q&A | CC | ~13K çift |
| HF `hukuk_soru_cevap` | Q&A | Açık | ~5–10K çift |
| Mevzuat.gov.tr | Kanun metni | Kamu | Yüzlerce kanun |
| Resmi Gazete | Yeni mevzuat | Kamu | Aylık akış |
| Yargıtay Karar Arama | İçtihat | Kamu (kısıtlı kazıma) | Milyonlarca |
| Dergipark hukuk makaleleri | Doktrin | Yazara göre değişir | Binlerce özet |

> **Lisans uyarısı:** Lexpera/Kazancı gibi ticari kaynaklar **kullanılmaz**. Akademik repo'da telif sorunu yaratır.

### 4.2 Format

Chat template (Gemma 4 uyumlu — EOS token: `<turn|>`):

```json
{
  "messages": [
    {"role": "user", "content": "Ev sahibi haklı sebep göstermeden çıkarabilir mi?"},
    {"role": "assistant", "content": "TBK 350. madde kapsamında ev sahibi ancak ... ..."}
  ]
}
```

Şu varyantları üretin:
- **Q&A** (vatandaş sorusu → sade cevap)
- **Term simplification** (hukuki terim → günlük dil)
- **Madde özetleme** (kanun metni → özet)
- **Senaryo → ilgili madde** (olay anlatımı → atıf)

### 4.3 Temizlik

- Mükerrer kayıt (MinHash + LSH)
- PII / ad-soyad maskeleme
- Token uzunluk filtresi (≤ 4096)
- Dil tespiti (sadece TR)
- Kalite filtresi (uzunluk, format hatası)

---

## 5. Eğitim Koşusu Reçetesi

### 5.1 Yerel deneme (Gemma 4 12B, G614FR / RTX 5070 12 GB)

```python
# Pseudocode
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="google/gemma-4-12B-it-qat-q4_0-unquantized",
    max_seq_length=2048,
    load_in_4bit=True,    # NF4 — 12GB VRAM için zorunlu
    dtype=None,
)

model = FastLanguageModel.get_peft_model(
    model, r=16, lora_alpha=32, lora_dropout=0.05,
    target_modules="all-linear",
    use_gradient_checkpointing="unsloth",
)

# TrainingArguments — 12B için batch=1 zorunlu
per_device_train_batch_size=1
gradient_accumulation_steps=16      # effective batch = 16
learning_rate=2e-4
num_train_epochs=2
warmup_ratio=0.03
lr_scheduler_type="cosine"
optim="adamw_8bit"
bf16=True
```

Beklenen (12B QLoRA, seq 2048, batch 1): ~11–12 GB VRAM (sıkışık, gradient_checkpointing zorunlu), 32K örnek için ~10–16 saat yerelde.

### 5.4 Deploy Pipeline (QAT → GGUF)

```bash
# Fine-tune + merge sonrası:
model.save_pretrained_merged("gemma4-hakhukuk-merged", tokenizer)  # bf16

# llama.cpp ile Q4_0 quantize:
./quantize gemma4-hakhukuk-merged/model.gguf output.Q4_0.gguf Q4_0

# Sonuç: ~6.5GB GGUF → 8GB VRAM end-user hedef ✓
```

### 5.2 Bulut koşusu (A100 40GB)

- `per_device_train_batch_size=8`
- `gradient_accumulation_steps=4`
- `max_seq_length=4096`
- ~1 saat / epoch (13K örnek)

### 5.3 Ablation matrisi (tez için)

| Eksen | Değerler |
| :--- | :--- |
| Base model | **Gemma 4 12B** (asıl); kıyas için Qwen3.5-4B, Gemma 4 E4B opsiyonel |
| LoRA rank | 8, 16, 32 |
| Veri karması | %100 Q&A vs %70 Q&A + %30 mevzuat |
| Epoch | 1, 2, 3 |

= 3 × 3 × 2 × 3 = 54 koşu (sweep). Mantıklı subset: 8–12 koşu.

---

## 6. Değerlendirme

> Detayları için ileride `BENCHMARK.md`. Burada sadece teknik bağlantı.

- **Otomatik:** Perplexity, BLEU/ROUGE (özet için), exact match (sınav soruları).
- **LLM-as-judge:** GPT-4o ile karşılaştırmalı (rubric: doğruluk, sade dil, atıf doğruluğu).
- **İnsan değerlendirmesi:** En az 2 hukukçu, ≥ 100 örnek, inter-annotator agreement (Cohen's κ).
- **Baselines:** Base Gemma 4 12B (FT öncesi), Qwen3.5-4B (kıyas), GPT-4o, Gemini 2.5, Trendyol-LLM, Llama-3-8B-instruct.

---

## 7. Riskler ve Açık Sorular

| Risk | Mitigasyon |
| :--- | :--- |
| Telif sorunu (içtihat metinleri) | Sadece kamu kaynakları + Yargıtay açık portal. |
| Halüsinasyon (uydurma kanun maddesi) | Faz 2 RAG + atıf doğrulama; FT'te "bilmiyorum" örnekleri eklenir. |
| Türkçe tokenizer verimsizliği | Qwen3.5 BPE tokenizer'ı TR için makul (çok dilli); EDA'da TR token/karakter oranı ölçülecek. |
| Yerelde (12 GB) çoklu-konfig ablation sweep pahalı | Tek konfig yerelde doğrulanır, sweep buluta. |
| Reproducibility | Seed sabitleme, requirements lock, HF Hub'a checkpoint push. |

---

## 8. Sonraki Adımlar

1. WSL2 + Blackwell-uyumlu CUDA + uv + PyTorch (sm_120) kurulumu.
2. Unsloth ile küçük model üzerinde 100 örnekle pipeline doğrulama (smoke test).
3. `data/processed/sft_v0/` (32K, hazır) ile format/yükleme kontrolü.
4. Yerel **Qwen3.5-4B** QLoRA ile v0 baseline koşu.
5. Sonuçları W&B'ye logla, Muhakim ile ilk eval raporu.
6. Açığa göre üretim (sadeleştirme/grounded) → sft_v1 → gerekirse buluta ablation.
