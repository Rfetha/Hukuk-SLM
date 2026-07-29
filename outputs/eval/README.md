# `outputs/eval/` — ölçüm çıktıları, **koşu klasörü** düzeninde

> **Kural (2026-07-29):** her ölçüm turu **kendi klasörüne** yazar ve klasörün içinde bir
> **`KUNYE.json`** bulunur. Düz `outputs/eval/` köküne dosya yazılmaz — kök yalnız koşu
> klasörlerini barındırır.
>
> Gerekçe `docs/record/yurutme-tuzaklari.md`'nin tek kuralı: *"bir sayı üretildiğinde 'bu sayı
> neyin sayısı' sorusunun cevabı **künyeden** okunabilmeli. Okunamıyorsa sayı yoktur."* Düz
> dizinde iki protokolün dosyaları yalnız `_th` ekiyle ayrılıyordu; bir ekin düşmesi sessizce
> yanlış protokolün sayısını verirdi.

## Koşular

| klasör | protokol | özneler | n | durum |
| :--- | :--- | :--- | --: | :--- |
| [`sprint1-thinking-off/`](sprint1-thinking-off/KUNYE.json) | `--thinking off` | base · `τ_g` v1 · Gemini 3.1 FL | 470/özne | 🔴 **çıpa değil** (ADR-0043) — kayıt olarak durur |
| [`cp09-butceli-1024-512/`](cp09-butceli-1024-512/KUNYE.json) | thinking **on**, bütçe 1024+512, zorunlu kapatma | aynı üç özne | 470/özne | 🟢 **yürürlükteki çıpa** |
| [`cp09-ab-ayrimi/`](cp09-ab-ayrimi/KUNYE.json) | thinking **off** + kaynak-yeterliliği önsözü | base | 70 + 80 | ⚗️ **ABLASYON** — ana tabloya girmez |
| [`cp1-hakem-meta-iddia/`](cp1-hakem-meta-iddia/KUNYE.json) | **üretim yok** — CP0.9 cevapları, YENİ hakem istemi (ADR-0041) | base · `τ_g` v1 · Gemini 3.1 FL | 80/özne (M1) | 🟢 **yürürlükteki M1 groundedness** — CP0.9'un `gnd_m1_*` dosyaları artık **ham/kontrol** |
| [`cp2-rejected-hasat/`](cp2-rejected-hasat/KUNYE.json) | hasat pilotu, bütçeli düşünce | base (çıplak) | 120 + 120 | 🔴 **PİLOT** — üretim hasadı başlamadı, kabul ölçütü karar bekliyor |
| `_artefakt/` | — | ölçüm dışı artefaktlar | — | `tau_norm_tg` · `vram_stack` · `token_budget` · eski smoke |

## Dosya adı şeması (klasör içinde)

```
{mod}_{özne}_detail.jsonl        üretim: soru · referans · context_shown · cevap · künye alanları
gnd_{mod}_{özne}.jsonl           groundedness hakemi, satır satır
gnd_{mod}_{özne}_summary.json    aynısının özeti
abst_{mod}_{özne}.jsonl          abstention hakemi, satır satır  (JSON dizisi, .jsonl adına rağmen)
abst_{mod}_{özne}_summary.json   Rej(LLM) · Rej(regex) · geçerli tuzak paydası · fabrikasyon
reg_{mod}_{özne}*                register proxy
a1_{mod}_{özne}.txt              A1 = cevaplanan-only + coverage (ADR-0011)
```

`{özne}`: `base` · `tg` / `tg_v1_th` · `gem` — protokol eki (`_th`) **tarihsel**; protokolün
asıl kaynağı artık **klasördür**.

## ⚠️ Sprint 1 klasöründe iki A1 sürümü var

`a1_m5_*.txt` **eski** (mod-bağımsız) red kuralıyla, `a1_m5_*_adr0044.txt` **düzeltilmiş**
(mod-duyarlı) kuralla hesaplandı — bkz. [ADR-0044](../../docs/adr/0044-mod-duyarli-feragat-kurali.md).
**Okunacak olan `_adr0044` sürümüdür**; eskisi audit için duruyor ve sayı olarak kullanılmaz.
M1/M4 dosyalarında iki sürüm birebir aynıdır (kural yalnız kör modu etkiliyor).

## Eski yollar → yeni yollar

Kapalı belgeler (`sprint1.md`, `research_log` #39/#41, ADR-0031, eski planlar) düz yolları
gösteriyor ve **bilerek değiştirilmedi** — audit trail'e dokunulmaz. Eşleme:

| eski | yeni |
| :--- | :--- |
| `outputs/eval/{m,gnd_,abst_,reg_,a1_}*_{base,tg,gem}*` | `outputs/eval/sprint1-thinking-off/…` |
| `outputs/eval/*_{base_th,tg_v1_th,gem_th}*` | `outputs/eval/cp09-butceli-1024-512/…` |
| `outputs/eval/{vram_stack,token_budget_*,tau_norm_*}.json` | `outputs/eval/_artefakt/…` |

## Yeni koşu açarken

1. Klasörü **koşunun kimliğiyle** adlandır (checkpoint + protokolün ayırt edici parametresi):
   `cp3-tau-abstention/`, `cp09-butceli-1024-512/` gibi. Tarih değil — tarih künyede.
2. `OUT_DIR=outputs/eval/<klasör>` ver (18 betik `--out-dir`/`OUT_DIR` alıyor).
3. Koşu biter bitmez **`KUNYE.json`** yaz: protokol · değişmezler (seed · klip · n · bütçe) ·
   özneler ve taşıyıcıları · hakem + gateway · geçerlilik kapısı sonucu · güç durumu · şerhler.
4. `.log` dosyaları klasörde durur ama **git'e girmez** (`*.log` kuralı `!outputs/**`
   negasyonundan sonra geldiği için yok sayılır — sıra önemli, bkz. `.gitignore`).
