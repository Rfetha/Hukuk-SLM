---
license: apache-2.0
language:
  - tr
base_model: Qwen/Qwen3.5-4B
pipeline_tag: text-generation
library_name: llama.cpp
tags:
  - legal
  - turkish
  - rag
  - gguf
  - task-arithmetic
---

# HakHukuk-4B v0.3 (Q4_K_M)

Türkçe mevzuat için, tüketici sınıfı bir dizüstü GPU'sunda çalışan 4B parametreli bir hukuk
asistanı. İki LoRA kolu ham temel modelden bağımsız eğitilmiş, görev vektörü olarak ham TIES
ile birleştirilmiş ve Q4_K_M'e kuantize edilmiştir.

Bu kart, ölçülen değerleri ve ölçülmeyen sınırları birlikte bildirmek üzere yazılmıştır.
Aşağıdaki üç bölüm, modeli indirmeden önce okunması gereken kısıtları içerir.

## 1. Model tek başına bildirilen başarımı üretemez

Bildirilen %80,1'lik sadık cevap kütlesi, erişim katmanı etkin (harness açık) koşulda
ölçülmüştür: model cevaplamadan önce bir retriever ilgili mevzuat maddelerini bulup bağlama
yerleştirmektedir.

| Bileşen | Durum |
| :--- | :--- |
| Ağırlıklar (bu depo) | Yayımlandı |
| Kod (retriever, servis, sınıflandırma) | [github.com/Rfetha/Hukuk-SLM](https://github.com/Rfetha/Hukuk-SLM) |
| Arama indeksi (`bge-m3`, 40.496 madde, ~80 MB) | Yayımlanmadı |

Modelin tek başına indirilmesi, ölçümün yapıldığı rejimi vermez. Kaynaksız koşulda modelin
yüksek güvenle yanlış hukuki içerik ürettiği ölçülmüştür. İndeksin dağıtımı açık bir iştir;
korpusun kapsamı yaklaşık 8,4 kat genişleyeceğinden bugünkü indeksin paketlenmesi kısa
ömürlü olacaktır.

## 2. Bilinen kusur: soruların yaklaşık %5'inde cevap boş dönmektedir

80 soruluk geliştirme kümesinde, ürün yolunda (`hakhukuk/servis.py`) 2026-09-09 tarihinde
ölçülmüştür:

| | Ürün yolu | Ölçüm hattı (bildirilen %80,1 bu hattan) |
| :--- | ---: | ---: |
| Kesik veya boş cevap | 7/80 (%8,75) | 4/80 (%5,0) |
| Tamamen boş metin | 4/80 (%5,0) | 0 |

Nedeni ölçülmüştür: düşünce modu etkinken model bazı örneklerde `</think>` etiketini
kapatmamakta, üretim bütçesinin tamamını düşünce kanalında harcamakta ve HTTP 200 ile boş
içerik döndürmektedir. Bu bir sonlanmama sorunudur, bütçe yetersizliği değildir. Ölçüm hattı
iki geçişli zorunlu kapatma uygulayarak bunu engellemektedir; ürün yolunda bu koruma yoktur.

Boş cevap gizlenmemektedir: durum `KESIK` olarak damgalanır ve arayüzde "cevap yarım"
uyarısı gösterilir. Bununla birlikte kullanıcı açısından sonuç boş bir ekrandır. Bu kusur
açık borç olarak kaydedilmiştir; düzeltilmesi ürün davranışını değiştireceğinden yeniden
ölçüm yapılmadan uygulanmayacaktır.

## 3. Hukuki tavsiye değildir

HakHukuk, hukuk metnini anlaşılır kılmak amacıyla geliştirilmiş bir araştırma artefaktıdır.
Avukat değildir ve çıktısı hukuki tavsiye niteliği taşımaz. Ürettiği her madde numarası,
[mevzuat.gov.tr](https://www.mevzuat.gov.tr) üzerinden doğrulanması gereken bir iddia olarak
değerlendirilmelidir. Mevzuat değişir, ağırlıklar değişmez; güncellik erişim katmanının
sorumluluğundadır.

## 4. Ölçüm sonuçları

Geliştirme kümesi (n=80, erişim katmanı etkin, k=10, önsözsüz istem, hakem `gpt-4o-mini`):

| Ölçüt | Değer |
| :--- | ---: |
| Sadık cevap kütlesi | 0,8011 |
| `recall@10` (kütlenin üst sınırı) | 0,9500 |
| Uydurulmuş madde numarası | 0/114 |
| Aşırı çekinme (gözle sayım) | 4/80 |
| İsabetsiz atıf (gözle sayım) | 8/80 |

Donmuş test kümesi (n=40, tek kez açıldı, 2026-09-09):

| Ölçüt | TEST | DEV |
| :--- | ---: | ---: |
| Ham kütle | 0,5804 | 0,8011 |
| `recall@10` (üst sınır) | 0,7500 | 0,9500 |
| Üst sınır kullanımı | 0,7739 | 0,8433 |
| Uydurulmuş madde numarası | 0/52 | 0/114 |

İki değer aynı ölçüt değildir; kümelerin erişim üst sınırları farklıdır. Düşüşün %76'sı küme
bileşiminden kaynaklanmakta, %24'ü kaynaklanmamaktadır. Model, görülmemiş veride üst sınırını
da daha düşük oranda kullanmaktadır.

## 5. Sürüm neden v1.0 değil

Sürüm kapısının üç maddesi geliştirme kümesinde geçilmiş ve kabul testi koşulmuştur. v1.0 adı
yine de verilmemiştir: bildirilen her değer tek bir hakem ailesinin (`gpt-4o-mini`) hükmüdür
ve iki hakem ailesi arasında ölçülen uyum κ = 0,534 olup aracın 0,6 eşiğinin altındadır.
Sürümü sınırlayan etken modelin başarımı değil, ölçüm aygıtının güvenilirliğidir.

## 6. Karşılaştırma — skor kartı

Karşılaştırma tek bir ölçüt üzerinden yapılmamıştır. Beş özne aynı sınava girmiştir: v2 soru
seti (n=80, geliştirme kümesi), önsözsüz istem, erişim katmanı etkin (k=10), üretim bütçesi
1536 belirteç, seed 3407, hakem `gpt-4o-mini`. Sınavın eşit olduğu varsayılmamış, ölçülmüştür
(bölüm 6.2).

| Eksen | **HakHukuk-4B** | `gemini-3.1-flash-lite` | `gemini-3.5-flash-lite` | `gemini-3.5-flash` | `claude-sonnet-5` | `Qwen3.5-4B` (temel) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Sadık cevap kütlesi ↑ ᵃ | 0,8011 | 0,7058 | 0,7622 | 0,7425 | **0,8348** | ölçülemedi ᵇ |
| Cevaplama oranı (`coverage`) | **0,9375** | 0,8750 | 0,8750 | 0,8375 | 0,9000 | ölçülemedi ᵇ |
| `A1`, cevaplanan ↑ | 0,8545 | 0,7710 | 0,8199 | 0,8269 | **0,8790** | ölçülemedi ᵇ |
| `A1`, altın getirilen ↑ | 0,8902 | 0,7900 | 0,8449 | 0,8523 | **0,9031** | ölçülemedi ᵇ |
| `recall@10` (erişim) | 0,9500 | 0,9500 | 0,9500 | 0,9500 | 0,9500 | ölçülemedi ᵇ |
| Aşırı çekinme ↓ ᶜ | **4/80** | 7/80 | 9/80 | 7/80 | **4/80** | ölçülemedi ᵇ |
| İsabetsiz atıf ↓ ᵈ | 8/80 | 8/80 | **7/80** | 8/80 | ölçülmedi ᵈ | ölçülemedi ᵇ |
| **Uydurulmuş madde numarası** ↓ | **0/114** | 1/152 | 4/130 | 4/133 | 2/163 | ölçülemedi ᵇ |
| Ezber kütlesi (M5) ↓ ᵉ | **0,3899** | 0,6710 | 0,7013 | 0,8241 | ölçülmedi ᵉ | 0,4697 |
| Cevap başına maliyet ↓ | **$0** | $0,001895 | $0,001152 | $0,009914 | $0,014915 | **$0** |
| Ortalama belirteç / cevap | 782,5 | 861,5 | **171,1** | 699,4 | 706,6 | ölçülemedi ᵇ |

Sonnet-5 kütle, `A1` ve atıf kalitesi eksenlerinde öndedir. HakHukuk cevaplama oranında ve
uydurulmuş madde numarasında öndedir; aşırı çekinmede iki model eşittir. Fark, kaynak verilen
bir sınavda ölçülmüştür; kaynaksız bir karşılaştırma değildir.

### 6.1 Kütlenin üç okuması

Ana tabloda bağlayıcı olan (GÖZ-katı) okuma yer almaktadır. Üçü birlikte:

| Kol | ALET (ham) | GÖZ-orta (yanlış pozitif düzeltilmiş) | GÖZ-katı (bağlayıcı) |
| :--- | ---: | ---: | ---: |
| HakHukuk-4B | 0,8011 | 0,8011 | 0,8011 |
| `gemini-3.1-flash-lite` | 0,6746 | 0,7058 | 0,7058 |
| `gemini-3.5-flash-lite` | 0,7174 | 0,7403 | 0,7622 |
| `gemini-3.5-flash` | 0,6925 | 0,7050 | 0,7425 |
| `claude-sonnet-5` | 0,7911 | 0,8223 | **0,8348** |

Bağlayıcı okuma olarak en muhafazakâr olan seçilmiştir; bu okumada rakiplerin çekinceli
cevapları da cevap sayılır, dolayısıyla onların kütlesi en yüksek, HakHukuk'un farkı en dar
çıkar. HakHukuk üç okumada da aynıdır: kendi kolunda yanlış pozitif ve çekinceli cevap yoktur
(80 kalem gözle okunmuş, araç ile göz arasındaki fark sıfır bulunmuştur).

Aletin ham okuması HakHukuk'u Sonnet-5'in önünde göstermektedir (0,8011'e karşı 0,7911). Bu
okuma kullanılmamıştır: çekinme dedektörü Sonnet-5 kolunda sekiz çekinmenin üçünü yanlış
saymaktadır (tam ve atıflı üç doğru cevap), HakHukuk kolunda ise yanlış pozitif yoktur.
Düzeltme uygulandığında sıralama değişmektedir.

### 6.2 Sınavın eşit olduğunun kanıtı

| Eksen | HakHukuk | Gemini kolları | Sonnet-5 |
| :--- | ---: | ---: | ---: |
| `recall@1 / @3 / @5 / @10` | 0,5250 / 0,7625 / 0,8250 / 0,9500 | aynı | 0,5250 / 0,7625 / 0,8250 / 0,9500 |
| Kesik cevap | 4/80 | 4/80 | 4/80 |
| Girdi belirteci (toplam) | 193.042 | 193.042 | ölçülmedi |
| İstem | önsözsüz | aynı | aynı |
| Üretim bütçesi | 1536 | 1536 | 1536 |

### 6.3 Dipnotlar

- **ᵃ** Rakip sütunlarında bağlayıcı GÖZ-katı okuması yazılıdır (bölüm 6.1).
- **ᵇ** Temel model ölçülmedi değil, **ölçülemedi**: sınava sokulmuş ve geçerlilik kapısından
  kalmıştır (kesik cevap 16/80 = %20, eşik %5), dolayısıyla hakem çağrılmamıştır. Nedeni
  ölçülmüştür: temel model uzun, kaynak alıntılayan cevaplar üretmekte ve 1536 belirtece
  sığmamaktadır. Aynı model kör modda yalnızca 2/80 kesik vermektedir; şişiren etken
  kaynakların kendisidir.
- **ᶜ** Tanım tüm öznelerde aynıdır: altın madde bağlama girmiş, model yine de çekinmiştir.
  Değerler gözle düzeltilmiştir; ham araç sayıları HakHukuk için 5/80, Sonnet-5 için 7/80,
  Gemini kolları için 8-11/80'dir.
- **ᵈ** İsabetsiz atıf, dört öznede 80/80 kalemin gözle taranmasıyla sayılmıştır. Sonnet-5
  kolunda bu tarama yapılmamıştır ve tahmin yazılmamıştır. Hakem tabanlı vekil ölçüt olan
  `wrong_ref_rate_micro` şu değerleri vermektedir: HakHukuk 0,0769, Sonnet-5 0,0083. Bu eksen
  HakHukuk'un açık borcudur.
- **ᵉ** Ezber kütlesi, kaynak verilmeden ölçülen anti-hedeftir; düşük olması istenir. Sonnet-5
  bu modda koşulmamıştır.

Bu değerlerin hiçbiri standart bir ölçüt kümesinden gelmemektedir. Tümü, Türkçe ve güncel
Türkiye Cumhuriyeti mevzuatı üzerine kurulmuş kendi CANON kümemizden üretilmiştir. MMLU,
LegalBench ve BigLaw-Bench gibi dış ölçütler koşulmamıştır; bu bir eksiklik değil kayıtlı bir
karardır (söz konusu kümeler İngilizce ve ABD common-law temellidir).

## 7. Yöntem

İki LoRA kolu ham temel modelden bağımsız eğitilmiştir; görev vektörü tanımı
(`τ = θ_ft − θ_base`) bunu zorunlu kılar. Birleştirme, eşzamanlı k-yollu ham TIES ile tam
ağırlık uzayında yapılmış, kuantizasyon en sona bırakılmıştır. Norm dengeleme ana sonuç değil
ablasyondur; ölçüm, önceki kararın çıkarımını tersine çevirmiştir.

## 8. Dosya

| | |
| :--- | :--- |
| Dosya | `HakHukuk-4B-v0.3-Q4_K_M.gguf` |
| `sha256` | `755e15e92e9f7021934f2d5eada6c1f02fcc92be23f0536b0c2a0a9586e7bffc` |
| Boyut | 2.783.446.720 bayt (2,592 GiB) |
| İç ad (izlenebilirlik) | `tgta_v1-q4_k_m.gguf` |

## 9. Sınırlar

- Kapsam yalnızca yürürlükteki Türkiye Cumhuriyeti kanunlarıdır (892 kanun, 40.496 madde).
  Yönetmelik, tüzük, KHK ve tebliğ kapsam dışıdır.
- Tek boyut noktası (~4B) ölçülmüştür; bulguların bu temel modele özgü olup olmadığı sorusu
  açıktır.
- Yanlış kaynağa atıf oranı 0,0769'dur (Sonnet-5: 0,0083). Model madde numarası
  uydurmamakta, ancak mevcut ve yanlış maddeye atıf yapabilmektedir. Açık borç.
- Bildirilen her değer tek hakem ailesinin hükmüdür; κ eşiğin altındadır.

Örnek soru-cevap çıktıları için bu depodaki `ORNEK_CEVAPLAR.md` dosyasına bakınız. Tam
araştırma kaydı, reddedilen alternatifler ve her değerin kaynağı
[github.com/Rfetha/Hukuk-SLM](https://github.com/Rfetha/Hukuk-SLM) deposundadır.
