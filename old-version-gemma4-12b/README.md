# old-version-gemma4-12b — emekli hat

**Emekli edildi:** 2026-07-24 · **Base:** `google/gemma-4-12B-it-qat-q4_0-unquantized`
**Neden:** Base model değiştiriliyor; hat sıfırdan yeni bir modelle kurulacak. Buradaki
artefaktlar **12B'ye çapalı ve taşınamaz** — LoRA adaptörleri modele özgüdür, ölçüm sayıları
12B protokolüyle alınmıştır.

> **Kural: taşındı, silinmedi.** ADR-0024'ün tanımladığı bölme çizgisi uygulandı:
> *base'e bağlı olan buraya, base'den bağımsız olan ana ağaçta.*

## İçindekiler

| ne | boyut | not |
| :--- | ---: | :--- |
| `outputs/v0…v3/` | 1.8 GB | LoRA adaptörleri — Modal A100 parasıyla üretildi, **yeni base'de yüklenmez** |
| `outputs/eval/` | 8.3 MB | 161 dosya — SCORECARD'ın kaynak sayıları (bf16/NF4 protokolü) |
| `outputs/{PHASE1,BENCHMARK}_REPORT.md` | — | tur raporları |
| `models/gguf/` | 21 GB | `g4-12b-q4_0-pure.gguf` (6.26 GiB, doğrulanmış) · `g4-e4b-f16.gguf` · `g4-e4b-q4_0-pure.gguf` ⚠️ **bozuk** (70 MB, quantize 4/666. tensörde kesilmiş) |
| `configs/gemma4_nothink.jinja` | 17 KB | Gemma 4 şablonunun minja-uyumlu yaması (`enable_thinking` tuzağı) |
| `record/SCORECARD.md` | — | **tüm turların kanonik sonuç tablosu** — hücreler 12B-çapalı |
| `record/{v2b,v2c,v3,v4}/` | — | tur sonuç belgeleri + reçeteler + kilitli v4 recipe |
| `record/law-slm-v3-jsonls/` | 1.1 MB | v3 CANON eval detay jsonl'leri (8 mod) + LaTeX sunumu |
| `NEXT_SESSION.md` | 13 KB | eski hattın devir notu |

⚠️ `docs/sunum/HakHukuk_Danisman_Sunumu.*` ana ağaçta bırakıldı (proje düzeyi sunum, tur
artefaktı değil) — ama **içindeki sayılar 12B'ye ait**, yeni base ile güncellenmeli.

## Ana ağaçta KALANLAR (base'den bağımsız — yeni hat bunları kullanır)

`data/` (778 MB, en pahalı varlık) · `scripts/` (5 turda doğrulanmış harness) ·
`docs/adr/` (26 karar) · `docs/record/research_log/` (42 girdi, **kronoloji kesintisiz akar**) ·
`docs/*.md` plan belgeleri · `knowledge/` · `requirements.lock.txt` · `modal_train.py`

## Nereden okunur

- **Ne denendi, ne çıktı:** `record/SCORECARD.md` → tek tabloda 5 tur × 7 eksen
- **Damıtılmış devir:** `~/code/hukuk-devir/RECETELER_12B.md` (config + veri + sonuç + karar)
  ve `~/code/hukuk-devir/DEVIR.md` (dersler + tuzaklar + scripts'in base-bağımlılık haritası)
- **Kararlar:** `docs/adr/` (ana ağaçta) — özellikle ADR-0011 (CANON), 0014 (v2c red),
  0015 (v3 kısmi), 0023 (dağıtım config), 0024 (bu emeklilik), 0025 (llama.cpp eval yolu)

## ⚠️ Kayıp kaydı

`outputs/_archive/` (691 MB) oturum başındaki taramada vardı, taşıma sırasında diskte
bulunamadı. Git'te takipli değildi (`outputs/` gitignored), hiçbir belgede referansı yok,
diskte başka kopyası yok. İçeriği bilinmiyor — büyük olasılıkla eski adaptör kopyaları.
Devir paketine de girmedi.
