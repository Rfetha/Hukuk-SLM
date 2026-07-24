# v3 — CANON Eval Sonuçları (6-mod + register + genelleme) — ⚠️ KISMİ (teslim değil)

> **Karar:** v3 **KISMİ / teslim değil** (2026-07-06, ADR-0015). K3'ü büyük ölçüde onardı (M2 0.35→0.59, M1 0.74→**0.88**)
> ama base-M2'yi (0.704) geçmedi **+** M2b'de regresyon açtı (0.96→0.53). Bu doküman = ölçülen tam skorkart + kapı
> gerekçesi + **M2b forced-source-selection teşhisi** + proxy→judge dersi.
> Otorite: [[../../adr/0015-v3-orpo-kapi-karari-kismi-v4-yonu-net]] · kronoloji [[../research_log/2026-07-06-v3-eval-sonuc-kapi-karari]] (#32) · birleşik tablo [[../SCORECARD]].

## Kurulum (tüm modlar ortak)
- **Model:** Gemma 4 12B + QLoRA adapter `outputs/v3/` (**v2b-adaptöründen DEVAM eden ORPO**; `train_orpo.py:132` PeftModel is_trainable, lr düşük, 2 epoch / 56 step). Eğitim = Modal A100 (ADIM 8, entry #30).
- **Eval:** lokal RTX 5070, deterministik seed 3407, eval-mirror (900-char chunk clip), hakem gpt-4o-mini. Judge 14 koşu, 0 hata, ~$0.08.
- **n:** core_hard n=40 (M1/M4/M5/M2b), trap n=35 (M2 + genelleme), E-set n=40 (M3).
- **A1 kuralı (ADR-0011):** cevaplanan-only macro faithfulness; "A1 @ coverage%". Tüm modellere aynı.
- **Kaynak:** `outputs/eval/{gnd,abst,corr,reg}_bench_*_v3*_summary.json` + per-item `abst_bench_m2b_v3.jsonl` (M2b teşhis) + genelleme `abst_bench_{xkanun,ood}_{base,v2b,v3}`. ⚠️ `outputs/eval/` gitignored → script'ten üretilir; sayılar burada + #32 + SCORECARD'da "sourced".

---

## Matris — durum panosu (6/6 mod + genelleme kapandı)

| Mod | Ne ölçer | v3 manşet | vs base | vs v2b |
|---|---|---|---|---|
| **M1** gold+distractor | grounding-under-noise | A1=**0.881** ✅ | +0.219 | +0.144 |
| **M4** oracle gold-only | iyimser tavan | A1=**1.000** ✅ | +0.022 | +0.032 |
| **M2** TRAP yanlış-kaynak | abstention (hedef) | Rej=**0.593** ⚠️ | −0.111 | +0.247 |
| **M2b** distractor-only | abstention (RAG-ıska) | Rej=**0.529** ❌ | −0.471 | −0.440 |
| **M3** boş/kaynaksız | abstention (kaynak-eksik) | Rej=**1.000** ✅ | 0 | 0 |
| **M5** KÖR/kaynaksız | parametrik ezber (anti) | A2=**0.075** ✅ | −0.150 | −0.100 |
| register | uzman dili | expert-frac=**0.975** ✅ | −0.025 | −0.025 |

**Genelleme (M2-modu, held-out):** xkanun (çapraz-kanun) base .968 / v2b .387 / **v3 .656** · ood (novel) base .889 / v2b .115 / **v3 .483**.
**1ep (ck28) vs 2ep (final):** M2 0.519→**0.593** · M1 0.899→0.881 · register 1.0→0.975 → **final tercih**.

---

## KAPI SONUCU — ⚠️ KISMİ (v2c gibi topyekûn RED değil)

| Eksen | v3 | Eşik | Sonuç |
|---|---|---|---|
| **M2 yanlış-kaynak abstention (birincil hedef)** | 0.593 | ≥0.704 (base) | ❌ **base-altı** (ama v2c 0.407'yi +0.19 geçti; K3 kırıldı) |
| **M1 grounding A1 (regresyon kapısı)** | 0.881 | v2b 0.737 koru | ✅ **ARTTI** (base'i de geçti) |
| **M2b RAG-multi miss (tavan kapısı)** | 0.529 | v2b 0.96 koru | ❌ **REGRESYON** (yeni açık) |
| M4 oracle grounding tavan | 1.000 | ≥0.975 | ✅ GEÇTİ |
| M3 boş-bağlam abstention | 1.000 | 1.0 | ✅ GEÇTİ |
| register (uzman dili) | 0.975 | v2b koru | ✅ GEÇTİ |
| Anti-hedef (parametrik ezber M5) | 0.075 | base 0.225 geçme | ✅ TUTTU (RAG'e dayanma) |

**Net:** teslim-adayı değil (2 gerçek borç: M2 base-altı + M2b regresyon) AMA v2c'den kategorik farklı — K3'ü kıran + grounding'i yükselten ilk tur. `outputs/v3/` = en-iyi-tur referansı + v4 başlangıç adaptörü.

---

## 🔬 M2b REGRESYON — kök teşhis (sürpriz negatif, paper-değerli)

34 geçerli tuzağın **16'sı FABRICATE** (v2b 0.96 → v3 0.529). Örüntü birebir aynı:
> *"İlgili kaynak, KAYNAK 3'tür çünkü ... Diğer kaynaklar ... elenmiştir."*

Judge gerekçesi her vakada: *"kaynak metin doğrudan bilgi sunmuyor, model yanıltıcı atıf yapıyor."*

**Mekanizma:** ORPO muhakemeli-red şablonu "kaynakları değerlendir → en ilgilisini **SEÇ**" adımını öğretti. M2'de (tek yanlış kaynak) doğru — o kaynağı eler. M2b'de (çok makul distractor, doğrusu YOK) aynı refleks "hiçbiri değil → reddet" yerine en yakın distractor'ı seçip uyduruyor. **v3 "yanlış-KONU kaynağını reddet"i öğrendi, "cevap bunların HİÇBİRİNDE yok"u kısmen unuttu.** → abstention tek beceri değil **AİLE**; tek-aile ORPO komşu-aileyi bozdu (K3'e alt-bulgu).

**v4 fix (NET):** ORPO rejected setine multi-distractor-no-gold (#2b) + OOD hard-negatifleri ekle. Detay [[receteler]] §v4.

---

## Metodoloji dersi — proxy → judge

Generation sonrası bedava red-proxy (keyword) ön-skorkart çıkardık; judge sonrası:

| Dilim | ham proxy | kalibre ~judge | gerçek judge |
|---|---|---|---|
| m2_v3 | 0.429 | ~0.55 | **0.593** |
| xkanun_v3 | 0.657 | 0.79 | **0.656** (judge≈HAM) |
| ood_v3 | 0.286 | 0.39 | **0.483** (judge>>kalibre) |

**Ders:** judge ≥ ham-proxy her yerde — (1) semantik red (keyword'süz) proxy'de görünmez, judge sayar; (2) invalid-trap paydası (judge `red/geçerli`, proxy ham N); (3) lineer kalibrasyon slice-family'ye özel, taşınmaz. **Ham proxy güvenilir taban; kalibre sabiti değil.**

---

## 📂 Ham çıktı dosyaları — v3'ün gerçek cevapları (`outputs/eval/`)

Skorların **kaynağı**: her mod için v3'ün ürettiği ham cevaplar. Dosya şeması (`_detail.jsonl`):
`id · soru · referans · context_shown · mode · cevap · kanun_adi · madde_no · kanun_no`.
Skor özetleri ayrıca `*_summary.json`, judge-etiketli per-item ise `abst_bench_*_v3*.jsonl` / `gnd_bench_*_v3*.jsonl`'de.

| Dosya | n | Mod / ne gösterir | v3 skoru |
|---|---|---|---|
| `bench_m1_v3_detail.jsonl` | 40 | **M1 grounding** — distractor'lı, doğru cevap kaynakta; sadık aktarım + atıf | 0.881 ✅ |
| `bench_m2_v3_detail.jsonl` | 35 | **M2 yanlış-kaynak red** (birincil hedef) — near-miss kaynağı reddetmeli | 0.593 ❌ base-altı |
| `bench_m2b_v3_detail.jsonl` | 40 | **M2b multi-distractor, doğrusu YOK** — reddetmeli; **16/34 FABRICATE** (kök teşhis burada) | 0.529 ❌ regresyon |
| `bench_m3_v3_detail.jsonl` | 40 | **M3 boş-bağlam red** — hiç kaynak yoksa temiz red | 1.000 ✅ |
| `bench_m4_v3_detail.jsonl` | 40 | **M4 oracle** — tek doğru kaynak verili; kusursuz aktarım | 1.000 ✅ |
| `bench_m5_v3_detail.jsonl` | 40 | **M5 kör/parametrik** (anti-hedef, düşük=iyi) — kaynaksız ezberden cevaplamamalı | 0.075 ✅ |
| `bench_xkanun_v3_detail.jsonl` | 35 | **Genelleme: çapraz-kanun** yapısal tuzak (held-out kolay-red) | 0.656 |
| `bench_ood_v3_detail.jsonl` | 35 | **Genelleme: OOD** novel soru (held-out, en zor/kırılgan) | 0.483 |
| `bench_m1_v3ck28_detail.jsonl` | 40 | M1, **1-epoch checkpoint (ck28)** — final-vs-1epoch kıyası (M1 0.899) | (ck28) |
| `bench_m2_v3ck28_detail.jsonl` | 35 | M2, **1-epoch checkpoint (ck28)** — final-vs-1epoch kıyası (M2 0.519) | (ck28) |

> `ck28` = checkpoint-28 (1 epoch); etiketsiz = final (2 epoch, checkpoint-56). Final tercih edildi (M2 0.519→0.593). Somut örnek cevaplar için dosyaları `cevap` alanından oku; M2b'deki *"İlgili kaynak KAYNAK 3'tür… elenmiştir"* örüntüsü fabrikasyon bulgusunun kanıtıdır.

## İlgili
- [[../../adr/0015-v3-orpo-kapi-karari-kismi-v4-yonu-net]] · [[../research_log/2026-07-06-v3-eval-sonuc-kapi-karari]] (#32) · [[../research_log/2026-07-05-v3-adim7-8-orpo-egitim-bitti]] (#30, eğitim) · [[../SCORECARD]] (birleşik) · [[receteler]] (v4) · önceki: [[../v2c/sonuclar]] (RED).
