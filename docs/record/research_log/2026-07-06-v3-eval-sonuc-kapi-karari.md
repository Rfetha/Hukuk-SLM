# 2026-07-06 · v3 ADIM 9 SONUÇ — tam judge skorkartı + kapı kararı (KISMİ) + M2b regresyon teşhisi

> **Bağlam:** v3 = v2b-adaptöründen DEVAM eden ORPO turu (near-miss abstention'ı düzeltmek için).
> ADIM 8 eğitim bitti (entry #30), ADIM 9 lokal generation + gpt-4o-mini judge tamamlandı.
> Bu entry = **v3'ün tam judge skorkartı + Q1 kapı kararı + sürpriz M2b regresyonunun kök teşhisi.**
> Kanıt: `outputs/eval/{gnd,abst,corr,reg}_bench_*_v3*_summary.json` (+ per-item `abst_bench_m2b_v3.jsonl`).
> Protokol: canon (cevaplanan-only A1, eval-mirror 900-char, n=40/35, seed 3407, hakem gpt-4o-mini). Judge maliyet ~$0.08.

## Tam skorkart (gerçek judge, v3-final = 2 epoch)

| Eksen | base | v2b | v2c ❌ | **v3** | Kapı | Sonuç |
|---|---|---|---|---|---|---|
| **M1 grounding faithfulness A1** (distractor'lı) | 0.662 | 0.737 | 0.681 | **0.881** | regresyon yok | ✅ ARTTI (v2b+base'i geçti) |
| **M4 oracle grounding** | 0.978 | 0.968 | 0.974 | **1.000** | tavan koru | ✅ tavan |
| **M2 yanlış-kaynak red** (birincil hedef) | 0.704 | 0.346 | 0.407 | **0.593** | ≥0.704 (base) | ❌ base-altı (v2c'yi +0.19 geçti) |
| **M2b RAG-multi miss red** | 1.0 | 0.96 | 0.973 | **0.529** | tavan koru | ❌ **REGRESYON** |
| **M3 boş-bağlam red** | 1.0 | 1.0 | 1.0 | **1.000** | tavan koru | ✅ tavan |
| **M5 kör/parametrik** (düşük=iyi, anti-hedef) | 0.225 | 0.175 | 0.125 | **0.075** | base-altı | ✅ RAG'e-dayanma kanıtı |
| **Register uzman_frac** | 1.0 | 1.0 | 1.0 | **0.975** | koru | ✅ korundu |

**1-epoch (ck28) vs 2-epoch (final):** M2 0.519→**0.593** (2. epoch işe yaradı), M1 0.899→0.881 (marjinal↓), register 1.0→0.975. **Final tercih edildi** (M2 kazanımı > marjinal M1/register kaybı).

## Genelleme dilimleri (held-out; gerçek judge)

| Dilim | ne test eder | base | v2b | **v3** |
|---|---|---|---|---|
| **xkanun** (çapraz-kanun, yapısal tuzak) | kolay-red | 0.968 | 0.387 | **0.656** |
| **ood** (held-out novel soru) | en zor | 0.889 | 0.115 | **0.483** |

Örüntü 3 dilimde tutarlı: **v3 >> batık-SFT (v2b) her yerde · v3 < base her yerde · OOD en kırılgan (0.483).**
v3 yapısal tuzağı (xkanun 0.66) iyi genelliyor ama novel-OOD'de zayıf = **ilke değil kalıp** → v4 #2b sinyali sağlam.

## Proxy → judge farkı (metodolojik ders)

Generation sonrası bedava red-proxy (keyword dedektörü) ile ön-skorkart çıkarılmıştı; judge sonrası fark:

| Dilim | ham proxy | kalibre ~judge | **gerçek judge** |
|---|---|---|---|
| m2_v3 | 0.429 | ~0.55 | **0.593** |
| m2_v3ck28 | 0.400 | 0.52 | **0.519** (kalibre 🎯) |
| xkanun_v3 | 0.657 | 0.79 | **0.656** (judge≈HAM) |
| ood_v3 | 0.286 | 0.39 | **0.483** (judge>>kalibre) |
| ood_base | 0.686 | 0.82 | **0.889** |

**Neden judge ≥ proxy (neredeyse her yerde):** (1) **semantik red** — proxy sadece keyword görür, "bu madde X'i düzenler, sorunuz Y hakkında" gibi keyword'süz reddi kaçırır → judge yukarı; (2) **invalid-trap paydası** — proxy ham N=35'e böler, judge `red/geçerli_tuzak`'a böler (m2_v3'te 27 valid), payda küçülünce oran yükselir; (3) **kalibrasyon transfer etmedi** — lineer fit kanon M2 dilimlerinde kuruldu, yapısal xkanun/ood'a taşınmadı (xkanun'da şişirdi, ood'da az söyledi). **Ders: ham proxy güvenilir TABAN; kalibre sabiti slice-family'ye özel, taşınmaz.**

## 🔬 M2b REGRESYON — kök teşhis (sürpriz negatif, paper-değerli)

**Bulgu:** M2b'de v3, 34 geçerli tuzağın **16'sında FABRICATE** etti (v2b ~0.96 → v3 0.529). Fabrikasyon örüntüsü **birebir aynı:**
> *"İlgili kaynak, KAYNAK 3'tür çünkü bu kaynak ... ile ilgili düzenlemeleri içermektedir. Diğer kaynaklar ... doğrudan ilgili olmadığı için elenmiştir."*

Judge gerekçesi her vakada: *"kaynak metin doğrudan bilgi sunmuyor, model yanıltıcı atıf yapıyor."*

**Mekanizma:** ORPO'nun muhakemeli-red şablonu (chosen) modele **"kaynakları değerlendir → en ilgilisini SEÇ"** adımını öğretti. M2'de (tek yanlış kaynak) bu doğru davranış — o tek kaynağı eler/reddeder. Ama **M2b'de (birden çok makul distractor, doğrusu YOK)** aynı "seç" refleksi ateşleniyor: model "hiçbiri değil → reddet" yerine **en yakın distractor'ı seçip bağ uyduruyor.**

**Yani v3 "yanlış-KONU kaynağını reddet"i öğrendi ama "cevap bu kaynakların HİÇBİRİNDE yok"u kısmen unuttu.** İki farklı abstention becerisi; ORPO verisi yalnız birincisini (tek-kaynak near-miss) içeriyordu → ikincisi (multi-distractor-no-gold) eğitilmedi, hatta "zorla-seçim" bias'ıyla bozuldu.

**K3 ailesine ek:** düz SFT abstention'ı topyekûn bozar (K3, entry #24); **ORPO tek-aile near-miss ile eğitilince o aileyi düzeltir ama komşu abstention-ailesinde (multi-miss) "forced source-selection" bias'ı indükler.** Fix = negatif-aile çeşitliliği (v4 #2b).

## Kapı kararı (Q1) — KISMİ / KOŞULLU (detay ADR-0015)

- ✅ **M1 regresyon yok** (0.737→0.881, base'i de geçti) · ✅ **M4/M3/register tavan** · ✅ **M5 base-altı.**
- ❌ **M2 = 0.593 < base 0.704** — birincil hedefte base geçilmedi (ama K3 büyük ölçüde onarıldı: 0.35→0.59).
- ❌ **M2b regresyon** (0.96→0.53, forced-source-selection bias).

**Verdict:** v3 teslim-adayı DEĞİL (strict kapı düştü) AMA v2c'den kategorik farklı — **K3'ü kıran + grounding'i yükselten ilk tur.** Fix-yönü artık AÇIK değil, **NET**: v4 = ORPO rejected setine **multi-distractor-no-gold (#2b)** + OOD hard-negatifleri ekle; M2'yi de base-üstüne itmek için near-miss yoğunluğu.

## Öğrenilen dersler
- **ORPO grounding'i bozmaz, yükseltir** (M1 0.74→0.88): SFT-terimi (chosen grounding örnekleri) + preference birlikte "forget" yapmadı — nll 7.65→2.96 (entry #30) davranışsal olarak da doğrulandı.
- **Abstention tek beceri değil, aile:** tek-kaynak-near-miss ≠ multi-distractor-no-gold ≠ boş-bağlam. Bir aileyi eğitmek diğerini garanti etmez, hatta bozabilir. **Eval'in mod-ayrışması (M2/M2b/M3) tam bu yüzden vazgeçilmez.**
- **M2=1.0 hâlâ yanlış yıldız** (entry #31 B4): v3 M2 0.593 + M4 1.0 + register 0.975 = base'in yapamadığı bileşik; hedef mutlak M2 değil, grounding-korumalı red.

## Paper eşleme
- **K3 (negatif bulgu) genişletme:** M2b forced-source-selection = "preference-opt tek-aile negatifle eğitilince komşu-aile abstention'ı boza­bilir" — K1 ablasyon + K3'e yeni alt-bulgu.
- **Tablo (turlar):** base/v2b/v2c/v3 7-eksen + genelleme (xkanun/ood).
- **Metodoloji notu:** free-proxy→judge kalibrasyon transfer sınırı (ham proxy taban, kalibre slice-özel).
- İlgili: entry #24 (K3), #30 (eğitim), #31 (konumlama), ADR-0014 (v2c/P1-ORPO seçilmişti), ADR-0015 (bu tur).
