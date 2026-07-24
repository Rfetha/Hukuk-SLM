#!/usr/bin/env python3
"""Base seçim kriteri + dağıtım bütçesi — cihazda uzun-RAG inference.

NE ÜRETİR (ADR-0021 / ADR-0023 / research_log 2026-07-23'ün sayı kaynağı):
  1. Mimari kıyas          — Gemma 4 12B (sliding+full) vs Qwen3.5 9B (hibrit DeltaNet)
  2. KV-cache tablosu      — bağlam × model
  3. Tavan bağlam          — verili VRAM'de en uzun metin
  4. Tam harness bütçesi   — Q4_0 ağırlık + KV + runtime, retriever yerleşimine göre
  5. Sığdırma merdiveni    — "tam yığın ≤8 GB'a nasıl sığar" (ADR-0023 hedef config)
  6. KV-bit tavanı         — llama.cpp --cache-type-k/v seçeneklerine göre bağlam

KAYNAK (CLAUDE.md: "Numbers are sourced, not remembered"):
  • Gemma 4 12B  → YEREL config.json (indirilmiş ağırlıklar, HF cache)
  • Qwen3        → YEREL Mecellem-Qwen3-4B-TR config.json (hibrit-öncesi referans)
  • Qwen3.5 9B   → huggingface.co/Qwen/Qwen3.5-9B/raw/main/config.json (çekildi 2026-07-23,
                   aşağıda sabit; yerelde indirilmiş değil)
  • N_PARAM      → gemma safetensors başlığından sayıldı (11.959.730.224)

⚠️ TAHMİN olan satırlar (ölçüm borcu, task #3): CUDA bağlamı 0.40 GB, compute buffer
   0.45/0.30 GB, Qwen Q4_0 ağırlığı 5.2 GB. Gerçek RTX 5070 + gerçek GGUF ile ölçülmeli.

Kullanım: python scripts/kv_cache_compare.py
"""
import glob
import json

BF16 = 2  # byte / eleman


def load(pattern):
    path = glob.glob(pattern)[0]
    cfg = json.load(open(path))
    return cfg.get("text_config", cfg), path


def gemma4_kv(t, n_ctx):
    """Gemma 4: karışık sliding/full katman. Sliding katmanlar pencereyle sınırlı."""
    types = t["layer_types"]
    n_slide = types.count("sliding_attention")
    n_full = types.count("full_attention")
    win = t["sliding_window"]
    # attention_k_eq_v: K ve V aynı tensör → cache yarıya iner
    kv_mult = 1 if t.get("attention_k_eq_v") else 2

    slide_tok = min(n_ctx, win)
    slide = n_slide * slide_tok * t["num_key_value_heads"] * t["head_dim"] * kv_mult * BF16
    full = n_full * n_ctx * t["num_global_key_value_heads"] * t["global_head_dim"] * kv_mult * BF16
    return slide + full


def dense_kv(t, n_ctx):
    """Klasik full-attention GQA (Qwen3 vb.): her katman tüm diziyi cache'ler."""
    head_dim = t.get("head_dim") or t["hidden_size"] // t["num_attention_heads"]
    return t["num_hidden_layers"] * n_ctx * t["num_key_value_heads"] * head_dim * 2 * BF16


def hybrid_kv(t, n_ctx):
    """Qwen3.5: linear_attention (Gated DeltaNet, sabit durum) + full_attention (büyüyen KV)."""
    types = t["layer_types"]
    n_full = types.count("full_attention")
    n_lin = types.count("linear_attention")
    grow = n_full * n_ctx * t["num_key_value_heads"] * t["head_dim"] * 2 * BF16
    # DeltaNet özyineli durumu: value_head × key_dim × value_dim (bağlamdan bağımsız, ~yaklaşık)
    state = n_lin * t["linear_num_value_heads"] * t["linear_key_head_dim"] * t["linear_value_head_dim"] * BF16
    return grow + state


# Qwen3.5-9B — huggingface.co/Qwen/Qwen3.5-9B/raw/main/config.json (çekildi 2026-07-23)
QWEN35_9B = {
    "layer_types": ["linear_attention"] * 3 + ["full_attention"] * 1,
    "num_key_value_heads": 4,
    "head_dim": 256,
    "linear_num_value_heads": 32,
    "linear_key_head_dim": 128,
    "linear_value_head_dim": 128,
}
QWEN35_9B["layer_types"] *= 8  # 8 × (3 linear + 1 full) = 32 katman


HUB = "/home/ersoy/.cache/huggingface/hub"
g, gp = load(f"{HUB}/models--google--gemma-4-12B-it-qat-q4_0-unquantized/snapshots/*/config.json")
q, qp = load(f"{HUB}/models--newmindai--Mecellem-Qwen3-4B-TR/snapshots/*/config.json")

print("KAYNAK config.json (yerel, indirilmiş ağırlıklardan):")
print(f"  Gemma 4 12B : {gp}")
print(f"  Qwen3       : {qp}")
print()
print("MİMARİ")
types = g["layer_types"]
print(f"  Gemma 4 12B : {g['num_hidden_layers']} katman = "
      f"{types.count('sliding_attention')} sliding(win={g['sliding_window']}) + "
      f"{types.count('full_attention')} full")
print(f"                sliding KV: {g['num_key_value_heads']} head × {g['head_dim']} dim")
print(f"                full    KV: {g['num_global_key_value_heads']} head × {g['global_head_dim']} dim")
print(f"                attention_k_eq_v = {g.get('attention_k_eq_v')} "
      f"(True → K=V paylaşımlı, cache yarıya iner)")
print(f"  Qwen3       : {q['num_hidden_layers']} katman = {q['num_hidden_layers']} full (sliding YOK)")
print(f"                KV: {q['num_key_value_heads']} head × {q.get('head_dim')} dim")
print()
qt = QWEN35_9B
print(f"  Qwen3.5 9B  : {len(qt['layer_types'])} katman = "
      f"{qt['layer_types'].count('linear_attention')} linear(DeltaNet, sabit durum) + "
      f"{qt['layer_types'].count('full_attention')} full")
print(f"                full KV: {qt['num_key_value_heads']} head × {qt['head_dim']} dim")
print()

print("SADECE KV-CACHE")
print(f"{'bağlam':>10} | {'Gemma4 12B':>12} | {'Qwen3.5 9B':>12} | {'Qwen3 9B*':>12} | {'G avantajı':>10}")
print("-" * 70)
for n in (16384, 32768, 65536, 131072, 262144):
    gv, hv, dv = gemma4_kv(g, n), hybrid_kv(qt, n), dense_kv(q, n) * 9 / 4
    print(f"{n:>10,} | {gv / 2**30:>9.2f} GB | {hv / 2**30:>9.2f} GB | "
          f"{dv / 2**30:>9.2f} GB | {hv / gv:>9.1f}×")
print("* Qwen3 (eski, hibritsiz) 9B'ye ölçeklenmiş — mimari sıçramanın büyüklüğünü göstermek için.")
print()

# Toplam ayak izi: Q4_0 ağırlık + KV. 8 GB soft-gate'e göre asıl karar bu.
W_G, W_Q = 6.5, 5.2  # GB, Q4_0
print("TOPLAM VRAM (Q4_0 ağırlık + KV) — 8 GB soft-gate'e göre")
print(f"{'bağlam':>10} | {'Gemma4 12B':>12} | {'Qwen3.5 9B':>12} | {'kazanan':>10}")
print("-" * 54)
for n in (16384, 32768, 65536, 131072, 262144):
    gt_ = W_G + gemma4_kv(g, n) / 2**30
    qt_ = W_Q + hybrid_kv(qt, n) / 2**30
    win = "Gemma" if gt_ < qt_ else "Qwen"
    flag = lambda v: f"{v:>9.2f} GB" + ("!" if v > 8 else " ")
    print(f"{n:>10,} | {flag(gt_)} | {flag(qt_)} | {win:>10}")
print(f"(ağırlık varsayımı: Gemma {W_G} GB, Qwen {W_Q} GB · ! = 8 GB aşıldı)")
print()

# Asıl ürün sorusu: verili bir VRAM bütçesinde kullanıcı EN FAZLA kaç token yapıştırabilir?
# (ADR-0018 soft-gate: tek nokta değil, maliyet-performans eğrisi)
def max_ctx(fn, cfg, weights_gb, budget_gb):
    lo, hi = 0, 4_000_000
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if weights_gb + fn(cfg, mid) / 2**30 <= budget_gb:
            lo = mid
        else:
            hi = mid - 1
    return lo


print("TAVAN BAĞLAM — verili VRAM'de kullanıcının yapıştırabileceği en uzun metin")
print(f"{'VRAM':>8} | {'Gemma4 12B':>14} | {'Qwen3.5 9B':>14} | {'Gemma başı çekme':>17}")
print("-" * 64)
for budget in (8, 12, 16, 24):
    mg = max_ctx(gemma4_kv, g, W_G, budget)
    mq = max_ctx(hybrid_kv, qt, W_Q, budget)
    ratio = f"{mg / mq:.1f}×" if mq else "—"
    print(f"{budget:>5} GB | {mg:>11,} tok | {mq:>11,} tok | {ratio:>17}")
print("(~1.6 token/kelime TR · 8 GB = tercih bandı, üstü kayıpla raporlanır)")
print()

# ---------------------------------------------------------------------------
# TAM HARNESS VRAM BÜTÇESİ — "model + retriever + KV" tek kartta sığıyor mu?
# Not: vektör indeksi ve (varsa) graph store CPU RAM/disk'te; VRAM'i ilgilendirmez.
# ---------------------------------------------------------------------------
N_PARAM = 11_959_730_224  # safetensors başlığından sayıldı
Q4_0_BPW = 4.5            # llama.cpp Q4_0: 32 ağırlık/blok + fp16 ölçek = 4.5 bit/ağırlık

w_q40 = N_PARAM * Q4_0_BPW / 8 / 2**30
# token_embd (262144×3840, tie edilmiş) llama.cpp'de sık sık Q6_K tutulur → fark:
embd_extra = 262144 * 3840 * (6.5 - 4.5) / 8 / 2**30

FIXED = [
    ("Gemma 4 12B ağırlık (Q4_0)", w_q40),
    ("  + token_embd Q6_K farkı (llama.cpp varsayılanı)", embd_extra),
    ("CUDA bağlamı + runtime", 0.40),
    ("llama.cpp compute buffer (12B, uzun bağlam)", 0.45),
]

print("TAM HARNESS VRAM BÜTÇESİ (tek kart)")
for name, gb in FIXED:
    print(f"  {name:<52} {gb:>6.2f} GB")
fixed_total = sum(gb for _, gb in FIXED)
print(f"  {'SABİT TOPLAM':<52} {fixed_total:>6.2f} GB")
print()

EMBEDDERS = [
    ("retriever CPU'da (embedder GPU'ya girmiyor)", 0.00),
    ("bge-m3 sınıfı embedder, GPU fp16 (~568M)", 1.06),
    ("bge-m3 sınıfı embedder, GPU int8", 0.53),
]
print(f"{'retriever yerleşimi':<44} | {'8 GB':>10} | {'12 GB':>10} | {'16 GB':>10}")
print("-" * 82)
for name, emb in EMBEDDERS:
    row = f"{name:<44} |"
    for budget in (8, 12, 16):
        free = budget - fixed_total - emb
        if free <= 0:
            row += f" {'SIĞMIYOR':>10} |"
        else:
            # sliding sabiti düşülür, kalanı büyüyen full katmanlara
            toks = max_ctx(gemma4_kv, g, fixed_total + emb, budget)
            row += f" {toks:>7,} tok |"
    print(row)
print()
print("Vektör indeksi + graph store: CPU RAM/disk — VRAM bütçesine girmez.")
print()

# 8 GB'da daha fazla bağlam gerekirse doğru kaldıraç: KV quantization (CPU offload DEĞİL).
# llama.cpp bugün --cache-type-k/v ile sunuyor; TurboQuant araştırma ucu (2.5-3.5 bit).
print("8 GB'DA BAĞLAM TAVANI — KV bit genişliğine göre (retriever CPU'da)")
print(f"{'KV precision':<34} | {'bit/eleman':>10} | {'tavan bağlam':>14}")
print("-" * 66)
base_bf16 = None
for label, bits in [("bf16 (varsayılan)", 16), ("q8_0 (llama.cpp, hazır)", 8),
                    ("q4_0 (llama.cpp, hazır)", 4), ("TurboQuant ~3 bit (araştırma)", 3)]:
    BF16 = bits / 8  # modül düzeyi rebind — fonksiyonlar çağrı anında okur
    toks = max_ctx(gemma4_kv, g, fixed_total, 8)
    if base_bf16 is None:
        base_bf16 = toks
    print(f"{label:<34} | {bits:>10} | {toks:>10,} tok  ({toks / base_bf16:.1f}×)")
BF16 = 2  # geri al

# ---------------------------------------------------------------------------
# SIĞDIRMA MERDİVENİ — "tam yığın ≤8 GB'a nasıl sığar?"
# Yığın: Gemma4 12B Q4_0 + KV + harness(retriever + yapısal graf, ADR-0022 (a))
# ---------------------------------------------------------------------------
W_Q4_PURE = N_PARAM * Q4_0_BPW / 8 / 2**30          # saf Q4_0 (QAT'in kalibre ettiği hedef)
W_Q6_EMBD = W_Q4_PURE + embd_extra                  # llama.cpp varsayılanı token_embd'i yükseltir
CUDA_CTX = 0.40
CBUF_STD, CBUF_FA = 0.45, 0.30                      # flash-attention compute buffer'ı küçültür

LADDER = [
    ("0. naif: Q6_K embd · bf16 KV · embedder GPU'da", W_Q6_EMBD + CUDA_CTX + CBUF_STD + 1.06, 16),
    ("1. retriever+graf CPU'ya (harness = 0 VRAM)", W_Q6_EMBD + CUDA_CTX + CBUF_STD, 16),
    ("2. + saf Q4_0 (token_embd dahil, QAT-sadık)", W_Q4_PURE + CUDA_CTX + CBUF_STD, 16),
    ("3. + flash-attention (-fa)", W_Q4_PURE + CUDA_CTX + CBUF_FA, 16),
    ("4. + KV q8_0 (--cache-type-k/v q8_0)", W_Q4_PURE + CUDA_CTX + CBUF_FA, 8),
    ("5. + KV q4_0 (agresif)", W_Q4_PURE + CUDA_CTX + CBUF_FA, 4),
]

print("SIĞDIRMA MERDİVENİ — 8 GB'da tam yığın")
print(f"{'konfigürasyon':<48} | {'sabit':>7} | {'boş':>6} | {'bağlam':>12}")
print("-" * 82)
for label, fixed, kvbits in LADDER:
    BF16 = kvbits / 8
    free = 8 - fixed
    toks = max_ctx(gemma4_kv, g, fixed, 8) if free > 0 else 0
    ctx = f"{toks:,} tok" if toks else "SIĞMIYOR"
    print(f"{label:<48} | {fixed:>4.2f} GB | {free:>3.2f} GB | {ctx:>12}")
BF16 = 2
print()
print("Harness (retriever + yapısal graf) = 0 VRAM: embedder CPU'da, graf+indeks CPU RAM/disk.")

gd = (gemma4_kv(g, 131072) - gemma4_kv(g, 131071)) / 1024
hd = (hybrid_kv(qt, 131072) - hybrid_kv(qt, 131071)) / 1024
qd = (dense_kv(q, 131072) - dense_kv(q, 131071)) / 1024 * 9 / 4
print("Token başına büyüme:")
print(f"  Gemma 4 12B : {gd:6.1f} KB/token")
print(f"  Qwen3.5 9B  : {hd:6.1f} KB/token")
print(f"  Qwen3 9B*   : {qd:6.1f} KB/token (hibrit öncesi)")
