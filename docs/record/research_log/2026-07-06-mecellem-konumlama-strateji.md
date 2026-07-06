# 2026-07-06 · Mecellem rakip-konumlama + stratejik çerçeve (benchmark beklerken)

> **Bağlam:** v3 ADIM 9 generation (yerel GPU) arka planda koşarken, cache'li canon sayıları üzerinden
> Mecellem karşısındaki konumumuzu ve "M2=1.0 / CPT'yi geçme" sorularını netleştiren tartışma.
> Kayıt amacı: paper **Tablo 1 (rakip baseline) + Tartışma (konumlama)** bölümü. Yeni deney YOK — mevcut
> cache'li judge sayılarının stratejik sentezi. v3 hücreleri judge sonrası netleşecek (bkz. entry #30, NEXT_SESSION).

## Rakip spesifiği (Tablo 1 dipnotu — her zaman belirt)
`newmindai/Mecellem-Qwen3-4B-TR` — Qwen3-4B tabanlı, ~270B token **CPT** (continual pre-training),
**instruction-tuned DEĞİL** (foundation base), Apache-2.0. Bizim canon'da **completion-style few-shot**
(`gen_eval_grounded.py --completion-fewshot`, 2-shot: biri atıflı-cevap biri red; chat-template YOK) ile
ölçüldü — çünkü asistan değil. Aynı set/mod/n(40/35)/seed(3407)/hakem(gpt-4o-mini).
⚠️ **Birebir kıyas değil:** bizimkiler Gemma-4-12B QLoRA-SFT asistan; Mecellem prompt'lanmış 4B foundation base.

## Kafa-kafaya tablo (TAM judge — v3 dahil KESİNLEŞTİ 2026-07-06 akşam)
> **GÜNCELLEME:** v3 hücreleri artık proxy değil, gerçek gpt-4o-mini judge (14 koşu, ADIM 9 kapandı).
> Kaynak: [[2026-07-06-v3-eval-sonuc-kapi-karari]] (#32) + [[../SCORECARD]]. Aşağıdaki proxy notu tarihsel (tuttu mu → tuttu).

| Eksen | base | v2b | v2c ❌ | Mecellem¹ | **v3 (judge)** |
|---|---|---|---|---|---|
| **M4 oracle grounding** (sadık kullanım) | 0.978 | 0.968 | 0.974 | **0.783** ↓ | **1.000** 🏆 |
| **Register uzman_frac** | 1.0 | 1.0 | 1.0 | **0.2** ↓↓ | **0.975** |
| M2b RAG-miss reddi | 1.0 | 0.96 | 0.973 | 0.919 | **0.529** ⬇️ regresyon |
| M3 boş-bağlam reddi | 1.0 | 1.0 | 1.0 | 1.0 | **1.000** |
| M1 grounding faithfulness | 0.662 | 0.737 | 0.681 | 0.713 | **0.881** 🏆 |
| **M2 yanlış-kaynak reddi** | 0.704 | 0.346 | 0.407 | **1.0*** | **0.593** (base-altı, v2c'yi +0.19 geçti) |
| **M5 kör/parametrik doğruluk** | 0.225 | 0.175 | 0.125 | **0.35** | **0.075** (en düşük = en az ezber) |

¹ yukarıdaki spesifik. \* Mecellem M2=1.0 few-shot red-taklidi + aşırı-reddetme (aşağı bak).
**Proxy doğrulaması (tarihsel):** v3 M2 proxy ~0.55 demişti → gerçek judge **0.593** (proxy taban tuttu; judge semantik-red + invalid-trap paydası nedeniyle biraz üstte çıktı, beklendiği gibi). M2b'yi proxy öngörmedi (yeni eksen değil ama regresyon judge'da ortaya çıktı — teşhis #32).

**Kesinleşen konumlama:** v3 deploy-anlamlı eksenlerde (M4 1.0, M1 0.881, register 0.975) **hem base'i hem Mecellem'i geçti**; kaybı yalnız red eksenlerinde (M2 base-altı, M2b regresyon). Mecellem'in tek üstünlüğü M5 (0.35 vs 0.075) = parametrik ezber = RAG-varken alakasız (B3/B5).

## Bulgular / çerçeve

**B1 — İki farklı makine.** Biz = **grounding + register makinesi** (M4 0.97, register 1.0); Mecellem =
**parametrik-ezber makinesi** (M5 0.35 en yüksek, ama M4 0.78 + register 0.2 + asistan değil). Güçlü ve
zayıf yanlar simetrik: bizim gücümüz onların açığı, tam tersi de öyle.

**B2 — Tek gerçek açığımız M2 near-miss.** Düz SFT (v2b/v2c) bu ekseni base'in **altına** düşürdü
(0.704→0.35–0.41) = **K3 negatif bulgu** (Grounding-Abstention paradoksu, entry #24). v3 ORPO tam bunu
tamir için var; proxy v2c'yi geçtiğini (0.31→0.43) ama base'i (0.571 proxy / 0.704 judge) geçip geçmediğinin
**belirsiz** olduğunu söylüyor → kapının kendisi.

**B3 — Mecellem'in M5 üstünlüğü aslında borç, varlık değil.** 270B token'a gömülen statik hukuk bilgisi;
mevzuat değişince yanlışa döner. Tezimiz **"güncellik kütüphanede/RAG'da, ağırlıkta değil"** → biz o bilgiyi
**çıkarımda RAG ile kiralıyoruz** (near-sıfır eğitim maliyeti, hep güncel). M5'i kovalamak = bilerek
tasarladığımız kırılganlığı geri inşa etmek.

**B4 — M2=1.0 yanlış yıldız.** M2 (yanlış kaynağı reddet) ve M4 (doğru kaynağı kullan) birbirini çeker.
1.0'ın en kolay yolu **aşırı-reddetme** → M4 çöker. Mecellem'in 1.0'ı tam bu patoloji (M4 0.78 ile paket).
Ayrıca set'te **invalid trap** var (kaynak soruyu cevaplıyor; base'te 27/35 valid) → mükemmel-kalibre model
ham sette 1.0 *almamalı*; 1.0 çoğu zaman "cevaplanabilirleri de reddettim" sinyali. **Hedef 1.0 değil:**
M2 ≥ 0.704 **+ M4/register korunmuş** = Mecellem'in yapamadığı bileşik.

**B5 — CPT ekonomisi asimetrik.** Mecellem ~270B token / GPU-ayları; biz QLoRA-SFT ~milyon-token / A100-saatleri
(~3-4 büyüklük mertebesi ucuz). CPT'yi geçmeye çalışmak "erişilebilir/ucuz" değer önermesini siler.
**Doğru hamle:** onları kendi sahalarında (CPT/M5) geçmeye çalışmak DEĞİL; o sahayı RAG ile alakasızlaştırıp
kendi sahamızda (grounding + register + ucuz ORPO-red) bileşik üstünlüğü büyütmek.

## Kararlar / yön (yeni ADR gerektirmez — mevcut tezin teyidi)
- **Kıyas ölçütü = "RAG-gerçekçi" bileşik** (kaynak-verilince M4 + M2 + register), kör-M5 değil. Paper'da bu
  çerçeveyle sun; Mecellem'in M5 avantajını "deploy-dışı eksen" olarak konumla.
- **M5'i kovalama.** Parametrik taban ancak niş gerekçeyle küçük statute-SFT ile artırılır; aksi = Mecellem'e dönüşmek.
- **M2 hedefi 1.0 değil**, grounding'i koruyan **0.8–0.9** (v3→v4 yolu: ertelenmiş #2b negatif-aile + ADIM 4 τ temiz etiket).

## Paper eşleme
- **Tablo 1 (rakip baseline):** Mecellem spesifiği + protokol-caveat + 7-eksen kafa-kafaya.
- **Tartışma / Konumlama:** B1 (iki makine), B3 (parametrik = borç), B4 (M2=1.0 patoloji + invalid-trap), B5 (CPT asimetri).
- **K3 (negatif bulgu):** B2 — düz SFT abstention'ı bozar; çözüm preference (ORPO).
- Ayrıntı: `99-paper-esleme.md` · rakip kurulum entry #23 (`2026-07-02-v2c-adim2-c4-mecellem-tablo1.md`).
