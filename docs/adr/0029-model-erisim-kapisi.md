# ADR-0029 — Tek model erişim kapısı + maliyet muhasebesi kuralı

**Statü:** Yürürlükte · **Tarih:** 2026-07-24
**Otorite belge:** `TASARIM.md` §5.2 (adalet kuralı) · §14 (terminoloji)
**İlgili:** ADR-0017 (maliyet-normalize parite) · ADR-0027 (dört katmanlı hakem savunması, aile-dışlama) · ADR-0020 (rakip seti) · ADR-0011 (CANON)

---

## Bağlam

Tasarım üç yerde **birden fazla model ailesine** erişim istiyor:

1. **Hakem paneli** — üç aile, aile-dışlamayla (ADR-0027). Bugünkü kod tek aileye çakılıydı
   (`from openai import OpenAI`, `OPENAI_API_KEY`); `bench_scorecard.py` bunun self-preference'ı
   gidermediğini zaten not etmişti ama karşılığı yazılmamıştı.
2. **Red regex kalibrasyonu** — her rakip ailesinde ölçülmeden hiçbir sayı raporlanmıyor (`TODO` §1).
3. **Dış parite matrisi** — rakipler API'den (Sprint 5).

Ayrıca fiyat tablosu **iki script'te ayrı ayrı** kopyalanmıştı ve bilinmeyen model sessizce
`gpt-4o-mini` fiyatına düşüyordu. Tez iddiasının yarısı maliyet-normalize parite olduğu için
(ADR-0017) yanlış fiyat, yanlış sonuç demek.

---

## Karar

### 1. Tek kapı: `scripts/llm_client.py`

Tüm model erişimi buradan geçer — hakem, rakip, üretici. Kapı **OpenAI-uyumlu**: `OPENROUTER_API_KEY`
varsa OpenRouter, yoksa doğrudan OpenAI. **Geriye dönük uyumlu** — anahtar eklenene kadar bugünkü
`OPENAI_API_KEY` yolu değişmeden çalışır, eklendiğinde script değişikliği gerekmez.

Kapı ayrıca şunları tek yerde tutar: fiyat tablosu · aile kimliği (aile-dışlama bunun üzerinden
işler) · ailelere göre JSON-modu · sağlayıcı pinleme · toleranslı JSON ayrıştırma.

### 2. Ne zaman gerekli — **Sprint 1'de değil**

| sprint | erişim | neden |
| :--- | :--- | :--- |
| **1** | tek aile (mevcut) | CP1↔CP5 **iç kıyas**; aynı hakem iki tarafta olduğu sürece aile sayısı sonucu değiştirmez. **Panelin üç ailesi burada seçilir** (aile-dışlama base ailesine bağlı = CP0 çıktısı), harcama yapılmaz |
| **2-3** | çok-aile | regex kalibrasyonu + iç iddia kararının üç aileli panelle raporlanması |
| **5** | çok-aile + maliyet | dış parite matrisi |

### 3. Maliyet muhasebesi kuralı 🔒

**Parite matematiği birincil-kaynak liste fiyatıyla yapılır — kapıya ödenen tutarla değil.**
Kapının kendi marjı var; ödenen tutarı rakibin fiyatı sanmak rakibi pahalı gösterir ve sayıyı
**bizim lehimize** kaydırır. Bu, kalibre edilmemiş red regex'iyle **aynı hata sınıfı**.
Ödenen tutar ayrı, operasyonel bir kalem olarak kaydedilir.

Bilinmeyen model için fiyat **sessizce varsayılmaz** — `price()` hata verir.

### 4. Sağlayıcı yönlendirme kaydı 🔒

Kapı aynı model kimliğini farklı upstream sağlayıcıya yollayabilir (farklı kuantizasyon/örnekleme).
**Hata vermez, sayı değişir** — 12B hattının imza arıza biçimi. Karşılık: `LLM_PROVIDER_ORDER` ile
pinle (`allow_fallbacks=false`) ve her koşuda gerçekten hizmet vereni özet JSON'a yaz
(`judge_providers`). **Tek elemandan fazlaysa sayı tek bir servis yığınına ait değildir.**

---

## Değerlendirilen alternatifler

| elenen | neden |
| :--- | :--- |
| **Aile başına birinci-taraf SDK** | 3-4 SDK + 3-4 anahtar + aile başına ayrı fiyat/JSON davranışı. Fiyat kaydı yine dağılırdı. Kapı marjı yok — tek gerçek avantajı bu, ve §3 kuralı zaten o sorunu çözüyor |
| **Kapıyı Sprint 5'te kurmak** | CP1 çıpaları farklı hakem yapılandırmasıyla üretilmiş olurdu; CP5 *"aynı seed/n/hakem"* diyor — hakem kıyasın değişmezi, hat ortasında değiştirilemez |
| **Kapıyı şimdi kurup çok-aileyi de şimdi koşmak** | Sprint 1 iç kıyas; harcamanın karşılığı yok. Karar (üç aile) alınır, harcama Sprint 3'e bırakılır |
| **Fiyatı kapıdan canlı çekmek** | Skorlama anında ağ bağımlılığı + raporlanan sayı koşudan koşuya sessizce değişir. Tablo tarihiyle sabitlenir (*sayılar kaynaklı* kuralı) |

---

## Sonuçlar

- `scripts/llm_client.py` eklendi; `groundedness.py` ve `score_abstention.py` oradan geçiyor,
  kopya fiyat tabloları kaldırıldı.
- Özet JSON'lara `judge_gateway` + `judge_providers` eklendi — yönlendirme kaydı artık koşunun
  kendi çıktısında.
- **Açık uç:** panelin üç ailesi seçilmedi (base ailesi belli olunca, CP0 sonrası). JSON modunun
  OpenAI dışı ailelerde davranışı **doğrulanmadı** — `loads_tolerant` yedeği var ama anahtar
  takıldığı gün gerçek çağrıyla görülecek (`sprint1.md` CP1).
- **Kapsam dışı:** eğitim/çıkarım yolu değişmedi. Kapı yalnız API-tarafı erişimi kapsar;
  yerel GGUF/llama.cpp yolu ayrıdır.
