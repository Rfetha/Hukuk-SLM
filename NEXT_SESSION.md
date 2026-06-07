# Sonraki Oturum — Başlangıç Promptu

Kopyala-yapıştır:

---

**Proje:** HakHukuk / Hukuk-SLM — Türkçe hukuki SLM (Qwen3.5-4B + QLoRA).  
**Durum:** Planlama ve dokümentasyon tamamlandı. Şimdi WSL2'ye geçip Faz 1 execute başlıyor.

**Önce oku:** `CLAUDE.md`, `docs/TEKNIK_PLAN.md`, `docs/VERI_PLANI.md`

**Yapılacak (Adım 1 — Geliştirme Ortamı):**

WSL2 (Ubuntu 22.04) üzerine Blackwell-uyumlu ML stack kur:

```
uv + Python 3.11
PyTorch (sm_120 / Blackwell uyumlu build)
unsloth (Blackwell-compat)
bitsandbytes 0.43+ (NF4 4-bit)
transformers, trl, peft, datasets, accelerate
flash-attn (sm_120 uyumlu)
wandb (W&B takip)
```

**Kritik uyarı:** RTX 5070 Laptop — Blackwell sm_120, CUDA 13.1. Standart `pip install unsloth` veya `bitsandbytes` ÇALIŞMAZ — Blackwell-uyumlu wheel gerekir. Kurulumda her kütüphane için uyumlu sürümü araştır, smoke test yap (Gemma 3 270M ile).

**Mevcut veri:**
- `data/processed/sft_v0/` — 32.234 temiz chat-template Q&A (train/val/test, hash-split)
- `data/raw/mevzuat_maddeler.jsonl` — 40.853 kanun maddesi (grounding zemini)

**Sonraki adımlar (sırayla):**
1. Ortam kurulumu + smoke test
2. v0 baseline SFT koşusu (32K uzman veri → Muhakim ölç)
3. 32K sadeleştirme (GPT-4o-mini ~$13)
4. Grounded üretim kanıt koşusu (50 örnek)
5. sft_v1 → iteratif SFT

---
