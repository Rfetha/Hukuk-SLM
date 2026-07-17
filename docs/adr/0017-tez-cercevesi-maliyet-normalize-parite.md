# ADR-0017 — Tez çerçevesi: maliyet-normalize parite + base model sabitleme

**Statü:** Yürürlükte · **Tarih:** 2026-07-17
**Otorite belge:** `docs/superpowers/specs/2026-07-17-tez-cercevesi-design.md`
**İlgili:** ADR-0003 (base), ADR-0016 (dış-benchmark/rakip), ADR-0018 (8GB soft-gate), ADR-0019 (faz-sırası istisnası), ADR-0020 (rakip seti) · spec §0-4

## Bağlam
Proje Master tezi çıktısı olarak yeniden çerçevelendi. Eski soru **içeri dönüktü** ("FT base'i geçiyor mu?" — base/v2b/v3/Mecellem tek eksende, kalite). Yeni hedef: tezin frontier-sınıf modellere karşı **dışarı dönük** bir iddia taşıması. TÜBİTAK ULAKBİM → MareNostrum5 HPC başvurusu gündemde; compute kısıtı gevşeyebilir.

## Karar
1. **Ana iddia = maliyet-normalize parite.** *Dar bir domainde (TR hukuku) SLM+harness, kapalı ticari modellerin dağıtım sınıfına maliyet-normalize paritede ne kadar yaklaşır — ve bunun ne kadarını FT, ne kadarını harness sağlar?* Ölçüm iki boyutlu: **kalite × maliyet** (Pareto). Cümle: *"bu maliyetle, buraya kadar çıkıyoruz."*
2. **v0→v3 = proof-of-concept / FT kolu.** Çöpe gitmiyor; tezin ince-ayar kolunu oluşturuyor.
3. **Base model = Gemma 4 12B, SABİT (QAT).** `gemma-4-12B-it-qat-q4_0-unquantized`. Qwen3.5-9B'ye geçme **VE** Qwen'i ikinci kol olarak koşma — **ikisi de reddedildi.** Asıl gerekçe: **QAT→Q4_0 zinciri maliyet iddiasının dayanağı** (12B eğit → Q4_0 → ~6.5GB → tüketici GPU → ~0 marjinal maliyet; en kırılgan halka quantization kaybı, Gemma onu resmî QAT ile garantiliyor). QAT'siz base (Qwen) Q4_0'a kendi elimizle indirilir → bilinmeyen kalite kaybı doğrudan tezin kalite ekseninden düşer.
4. **Benchmark = birincil katkı DEĞİL, altyapı.** Parite bir *eşdeğerlik* iddiasıdır (D≈B), fark iddiası değil; TOST fark testinden çok örnek ister. n=100/75 baştan kurulur. 6-mod CANON bu iddianın ölçüm zemini.

## Elenen seçenekler
- **Qwen3.5-9B'ye geçiş** → confounded (hem aile hem boyut değişir) + 5 koşu + ~35 judge hücresi + QAT garantisi kaybı; kazanç ~1.5GB. Değmez. Düşük-spec derdi base değil KV-cache → TurboQuant.
- **Çok-base kolu (Qwen replikasyon)** → kapsam dışı; sonuç: dış geçerlilik **kapatılmayan sınır** (dürüst limitations).
- **CPT** → non-goal (HPC gelse bile); ayrı tez.

## Sonuç
- Dış geçerlilik ("bulgular Gemma'ya özgü mü?") tezde **açık limitations maddesi** + future-work.
- ADR-0016'yı **süpersed etmez, genişletir:** ADR-0016 "frontier kıyası kendi canon setinde" demişti (yardımcı ölçüm); ADR-0017 onu **ana iddiaya** yükseltiyor.
- HPC = yükselteç, bağımlılık değil (ADR-0019/spec §2). Sübvansiyon maliyet iddiasından izole (GPU-saat piyasa fiyatı).
