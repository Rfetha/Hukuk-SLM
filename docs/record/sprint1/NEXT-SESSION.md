# NEXT SESSION — CP6 ölçümü (2026-07-28 kapanışı)

> **Bu belge ne:** sıradaki oturumun devir notu. **Tek iş kaldı: CP6.**
> **Otorite:** [`TASARIM.md`](../../../TASARIM.md) · **yürütme:** [`sprint1.md`](../../../sprint1.md) CP6
> **Açık sorular:** [`docs/open_questions.md`](../../open_questions.md) — 4 açık, hiçbiri CP6'yı bloke etmiyor
>
> ⚠️ Önceki devir notu (CP5 hazırlığı) **tamamen değiştirildi**; bu belge sıfırdan yazıldı.

---

## 1. Durum

| | durum |
| :--- | :--- |
| Faz A (CP0-CP3) · CP7 · CP4 | ✅ tamam |
| **CP5 — `τ_grounding` tam eğitim** | ✅ **TAMAM** (2026-07-28) |
| **CP6 — ölçüm** | 🔵 **SIRADA — tek kalan iş** |
| Sprint 1 çıkışı | CP6 bitince kapanır |

## 2. CP5 ne üretti

```
1083/1083 adım · ~2sa 05dk · A100-40GB · train loss ~0.38 (adım 50) → sonu #41'e
adaptör: outputs/tg/adapter_model.safetensors (114 MB)  ·  volume: hukuk-outputs:/tg
```

**Ölçülen `‖τ_grounding‖`** (ADR-0036'nın koşulsuz borcu) → `outputs/eval/tau_norm_tg.json`

| | değer |
| :--- | ---: |
| `‖τ_g‖_F` (toplam) | **10.4589** |
| LoRA çifti | **224** |
| `α/r` | 2.0 |

**224 sayısı mimari varsayımı birebir doğruladı:** `8 full-attn×4 + 24 linear-attn×4 + 32×3(MLP) = 224`.
Modül dağılımı: `gate_proj` %34.5 · `up_proj` %23.2 · **`in_proj_qkv` %16.8 · `in_proj_z` %10.0** ·
`down_proj` %6.8 · `q_proj` %5.9 · diğerleri <%2. *(`k_proj`/`v_proj` neredeyse hiç değişmemiş.)*

**Hız — ADR-0033'ün projeksiyonu düzeltildi:** 5.4 s/it **smoke projeksiyonuydu**; gerçek koşuda
**6.8-7.0 s/it · 2.619 token/s · MFU ≈ %15**. Stack için normal (A100'de yayımlanmış Unsloth
rakamının %8 altı). Sebep büyük ölçüde `causal-conv1d` yokluğu — **çıktı geçerli**, fallback
matematiksel olarak aynı.

---

## 3. ⚠️⚠️ CP6'NIN EN BÜYÜK TUZAĞI — önce bunu oku

`gen_eval_grounded.py` **iki yol** destekliyor ve **yanlışını seçmek CP6'yı sessizce geçersiz kılar:**

| yol | nasıl | CP6 için |
| :--- | :--- | :--- |
| **A — GGUF / llama-server** | `--server-url`, adaptör GGUF'a gömülü | ✅ **ZORUNLU** |
| B — transformers + `--adapter` | `--adapter outputs/tg`, 4-bit yükleme | 🚫 **KULLANMA** |

**Neden:** CP2 çıpaları **Q4_K_M GGUF üzerinden llama-server ile** üretildi. B yolu farklı bir
precision/runtime — çıkan sayı CP2 ile **kıyaslanamaz**, ama tablo dolar ve doğru görünür.
CP6'nın tek işi *"elmayla elma"* kıyas (aynı mod/n/seed/hakem **ve aynı runtime**).

> Bu, bu hattın klasik hatası: `#38` şablon tuzağı, `#39` yanlış `--data`, `#40` `fla-core` —
> hepsi **hata vermeden yanlış sayı üretti**.

---

## 4. Eksik halka: adaptör → GGUF zinciri

`scripts/setup_llamacpp.sh` **HF repo alıyor, adaptör almıyor.** Aradaki adım **yok, yazılacak.**

```
outputs/tg (LoRA adaptör)
      +  Qwen/Qwen3.5-4B  (ham base)
              ↓  ❌ BU ADIM YOK — yazılacak
      birleştirilmiş HF dizini (bf16)
              ↓  bash scripts/setup_llamacpp.sh <dizin> tg     (QUANT=Q4_K_M PURE=0)
      models/gguf/tg-q4_k_m.gguf
              ↓  llama-server
      CP6 eval
```

**Merge adımı basit** — tek adaptör, TIES yok: `PeftModel.from_pretrained(...)` +
`merge_and_unload()` + `save_pretrained`. Bellek: bf16 4.57B ≈ 9.1 GB → **host RAM'de** yapılır
(32 GB var), GPU gerekmez.

⚠️ **Kuantizasyon bayrakları:** `QUANT=Q4_K_M` **PURE=0** — `setup_llamacpp.sh`'ın varsayılanı
`Q4_0` + `PURE=1` ve o **QAT base'lere özgü** (ADR-0023). Qwen3.5-4B QAT değil; yanlış bayrakla
embedding gereksiz kayıp verir.

⚠️ **Kuantizasyon yarıda kesilirse dosya "var" görünür** (`sprint1.md` CP0 notu) — bitişi teyit et.

⚠️ **Boyut teyidi:** merge sonrası GGUF **base ile aynı boyutta** çıkmalı (~2.59 GiB). LoRA merge
parametre sayısını değiştirmez. Farklıysa dur — `NEXT-SESSION` §9'un eski açık kalemi buydu.

---

## 5. CP6 — 6 mod, harness KAPALI, DEV havuzu

**Sunucuyu aç:**
```bash
$HOME/code/llama.cpp/build-cuda/bin/llama-server -m models/gguf/tg-q4_k_m.gguf \
  --port 8080 --ctx-size 4096 --cache-type-k q8_0 --cache-type-v q8_0 &
export LLAMA_SERVER_URL=http://127.0.0.1:8080
export DEV=data/eval/dev
```

**Üret** — CP2 ile **birebir aynı** bayraklar, yalnız etiket `_base` → `_tg`:
```bash
python scripts/gen_eval_grounded.py --label m1_tg  --data $DEV/core_hard.jsonl --distractors 4 --max-chunk-chars 900 --n 80
python scripts/gen_eval_grounded.py --label m4_tg  --data $DEV/core_hard.jsonl --with-source --n 80
python scripts/gen_eval_grounded.py --label m2_tg  --data $DEV/trap.jsonl      --with-source --n 70
python scripts/gen_eval_grounded.py --label m2b_tg --data $DEV/core_hard.jsonl --distractors 4 --no-gold --n 80
python scripts/gen_eval_grounded.py --label m3_tg  --data $DEV/core_hard.jsonl --empty-context --n 80
python scripts/gen_eval_grounded.py --label m5_tg  --data $DEV/core_hard.jsonl --n 80        # kör
```

**Skorla:**
```bash
for M in m1 m4 m5; do
  python scripts/groundedness.py --details outputs/eval/${M}_tg_detail.jsonl --label ${M}_tg --mode data
done
for M in m2 m2b m3; do
  python scripts/score_abstention.py --details outputs/eval/${M}_tg_detail.jsonl --label ${M}_tg \
    $( [ $M = m2b ] && echo --source-field context_shown )
done
python scripts/rescore_answered.py --gnd outputs/eval/gnd_m1_tg.jsonl --bench outputs/eval/m1_tg_detail.jsonl --label m1_tg
python scripts/score_register.py --details outputs/eval/m1_tg_detail.jsonl --label m1_tg
```

### 🚫 Bunlar asla düşürülmez

| bayrak | düşerse |
| :--- | :--- |
| `--data $DEV/...` | Varsayılan `data/train/grounded_qa/test.jsonl` — **eğitim setinin komşusu**, CANON değil. Hata vermez, tablo dolar, sayı yanlış sete aittir |
| `--max-chunk-chars 900` | Eval-mirror kırılır — model eğitildiğinden uzun bağlamla ölçülür (ADR-0011 değişmezi) |
| `--n` değerleri (80/80/70/80/80/80) | CP2 ile n eşleşmezse kıyas bozulur |
| seed 3407 | varsayılan, değiştirme |

---

## 6. Ön-kayıtlı beklenti — **M2 DÜŞECEK, panik yok**

| eksen | beklenti | neden |
| :--- | :---: | :--- |
| **M1** distractor sadakati | **↑↑** | kolun çekirdek hedefi (verinin %77'si bu biçim) |
| **M4** oracle | **→** | tavan, ayırmıyor |
| **M2b** çok-kaynak ıska | **↑** | %20 abstain dilimi tam bu şekli öğretiyor |
| **M3** boş bağlam | **→** | zaten tavan |
| **M2** near-miss tek kaynak | **↓↓** | bu şekil veride **hiç yok** |
| **M5** kör | **↓/→** | **anti-hedef** — yükselmemeli |
| register | **→** | loss'ta değil |

> **M2'nin düşmesi Sprint 1'in ölçmek istediği şeydir, önlemek istediği değil.** Grounding kolu
> tek başına abstention'ı korumaz — `τ_abstention` ve merge tam bu yüzden var.
>
> **Ama ayrım yap:** off-distribution artefaktı mı, gerçek kayıp mı? 12B'de M2-oracle 0.346'ydı
> ama training-matched **M2b 0.96**. → **M2 ve M2b birlikte okunur.**
> **M2 = 1.0 iyi haber DEĞİL** — aşırı red, coverage çöküşünün diğer yüzü.

---

## 7. Kayıt — `research_log` **#41**

Aynı gün yazılır, sayılar kaynağıyla (metrik + n + hakem + seed + çıktı dosyası). İçermeli:

- CP6'nın 6 mod tablosu, **CP2 çıpalarıyla yan yana**
- Sprint 1'in üç çıkış sorusu: hat çalışıyor mu · `τ_g` ne satın aldı · yan hasar ne kadar
- **CP5 künyesi:** 1.083 adım · 6.8-7.0 s/it · `‖τ_g‖ = 10.4589` · 224 LoRA çifti
- Hız düzeltmesi (ADR-0033'ün 5.4'ü smoke projeksiyonuydu)

---

## 8. Bütçe

| kalem | durum |
| :--- | :--- |
| Modal cap | **$42.50** |
| CP5 fiili | ~$5.5 *(2sa 05dk A100 — panelden teyit et)* |
| CP6 | **GPU maliyeti yok** (yerel llama.cpp) + hakem ~$0.10-0.30 |
| OpenAI hakem | `.env` `OPENAI_BUDGET_USD=5` |

---

## 9. Bu oturumda kapanan işler (2026-07-28)

**Üç yeni ADR:** [0035](../../adr/0035-tau-reasoning-rs-ft-kapsam-disi.md) `τ_reasoning` kapsam dışı ·
[0036](../../adr/0036-tau-norm-asimetrisi-ve-norm-dengeli-merge.md) norm-dengeli merge ·
[0037](../../adr/0037-ic-iddia-karar-kurali-kapi-5.md) **Kapı 5** iç iddianın karar kuralı ·
[0038](../../adr/0038-red-kapisi-esigi-kati.md) red kapısı katı. *(0034 emekli hat silindi.)*

**Tasarım artık şöyle:** 2 kol (`τg` · `τa`) · kafes **4 hücre × 2 merge ayarı = 8 eval** ·
**5 eğitim koşusu** · ana sonuç **norm-dengeli** merge.

**İki kod borcu kapandı:** `train_orpo.py` rejim sapması (`--bf16-base`, `--lora-dropout`) ·
`--target-modules` artık **zorunlu, varsayılansız** (bedeli ölçüldü: `‖τ‖`'nin %26.8'i).

**Sprint 2 için kilitlendi:** ORPO `epochs = 3` (27 adım → 82) · uzunluk 2048/1536 ·
`--fresh-adapter` zorunlu · `causal-conv1d` **4 koşudan önce ölçülecek**.

---

## 10. Açık kalanlar — CP6'yı bloke ETMİYOR

| ne | nerede |
| :--- | :--- |
| §13.1 embedder (aday `bge-m3`) · §13.3 güç analizi · §13.5 hakem pinleme · §13.6 içtihat | [`docs/open_questions.md`](../../open_questions.md) |
| **Korpus temizliği** — 1.901 saf kabuk (%4.7). ⚠️ Eğitim/eval **temiz**, risk yalnız Sprint 4 retriever'ında | [`TASARIM.md`](../../../TASARIM.md) §5.3 |
| Sağlayıcı pinlemesi rakip tarafında kayda geçmiyor · rakip üretim maliyeti ölçülmedi | Sprint 5 ön koşulu |
| `sprint1.md` CP2 tablosundaki M2 base regex `0.500` ↔ `abst_m2_base_summary.json`'daki **0.567** uyuşmazlığı | işaretlendi, düzeltilmedi |
| Devir paketi (`~/code/hukuk-devir/`) yedeksiz tek nüsha | [ADR-0034](../../adr/0034-emekli-hat-artefaktlarinin-repodan-cikarilmasi.md) |
