# DEVİR NOTU — 1 Ağustos'ta buradan devam

**Yazıldı:** 2026-07-30 gece · **Sebep:** Modal fatura dönemi 1 Ağustos'ta yenileniyor, CP2-c o
zamana ertelendi. **Bu dosya geçicidir** — CP2-c koştuktan sonra silinir.

---

## Tek cümlede

Sprint 2'nin **zemin işi bitti**; kalan tek şey **veri üretimi** ve o saf GPU-saati. Üç eşik
türetilip kilitlendi, merge kodu yazılıp doğrulandı, hiçbir ön-kayıtlı sayı açık değil.

## İlk komut

```bash
# 1) Modal bütçesi gerçekten yenilendi mi — PANELDEN doğrula (defterden türetme, tuzak 6.3)
#    https://modal.com → Settings → Usage. Beklenen: ~$42.50 kullanılabilir.

# 2) Hasadı başlat (iki tip, ADR-0045 m.4) — modal_train.py'ye bir hasat giriş noktası gerekiyor:
#    mevcut `harvest_rejected` ESKİ betiği (gen_v3_rejected.py) çağırıyor, CP2 `cp2_harvest.py`
#    kullanıyor. ⚠️ Bu köprü YAZILMADI — ilk iş o.
```

> ### 🔴 1 Ağustos'ta yapılacak İLK teknik iş
> `modal_train.py`'nin `harvest_rejected` fonksiyonu **eski** `scripts/gen_v3_rejected.py`'yi
> çağırıyor. CP2 ise `scripts/cp2_harvest.py` kullanıyor (bütçeli düşünce · iki tip · `--concurrency`).
> **Modal tarafında bu köprü yok.** Yapılacaklar:
> 1. `modal_train.py`'ye `cp2_harvest.py`'yi çağıran bir fonksiyon + `spawn_` giriş noktası
> 2. İçinde `llama-server`'ı `-np 32` ile ayağa kaldırmak gerekiyor (hasat HTTP üzerinden çalışıyor,
>    doğrudan transformers değil) — **taşıyıcı Q4_K_M GGUF + llama.cpp, vLLM YASAK** (ADR-0047 m.2)
> 3. GGUF'u Modal volume'una yükle: `models/gguf/q35-4b-q4_k_m.gguf` (2,59 GiB)
> 4. `--detach` **zorunlu** (tuzak 6.1 — yoksa iş sessizce hiç koşmaz)

## Kilitli sayılar — tartışmaya açılmaz, yalnız uygulanır

```
ARA KAPI eşikleri (CP2-r'de türetildi · ADR-0049 m.1)
  τ_a tekil  M2 Rej ≥ 0.923      (base 0.803 + 0.12)
  muhafız    M1 A1  ≥ 0.880      (base A1 0.9777 × 0.90)
  merge      M2b    ≥ 0.854      (base 0.949 × 0.90)
  → sonuç ESKİ eşiklere (0.934 / 0.888 / 0.887) karşı DA raporlanır

CP2-c hedefi        750 negatif = ~7.500 üretim (ölçülen verim %10)
τ_a rejimi          ~937 çift · 5 epoch · ~73 adım · lr 1e-5 · etkin batch 64 · --fresh-adapter
kabul tasarımı B    regex ön-filtre → mini verdict → gpt-4o verdict TEYİT → gpt-4o KÖR geçerlilik
M2b kurgu tabanı    79/80 ≫ 40/80 → GEÇİLDİ, merge onarımı ARA KAPI'nın 2. gözlemi olarak kalıyor
```

## Bütçe — İKİ CÜZDAN, karıştırma (tuzak 6.3)

| | durum |
| :--- | :--- |
| **Modal GPU** | 2026-07-30'da kalan **$7,27** / $42,50 · **1 Ağustos'ta yenilenmesi bekleniyor** |
| **OpenAI hakem** | ayrı cüzdan · Sprint 2'de $1,00 harcandı |

Modal sayısı **panelden okunur**, defterden türetilmez. ~$28'lik geçmiş harcama **emekli 12B
hattına** aitti ve bu defterde hiç görünmüyordu — CP4-CP5'in sığmadığı böyle fark edilmedi.

**1 Ağustos sonrası plan:** CP2-c ~$3-6 · CP3 ~$3,2 · CP4-CP5 ~$12,2 → toplam ~$21, $42,50'ye sığar.

## Ölçülmüş, tekrar denenmeyecek şeyler

| ne | sonuç |
| :--- | :--- |
| Yerel `-np 8` hasat | ❌ **1,35×** (beklenen 4-6×) → 750 negatif **17,1 saat**. Sebep: zorunlu kapatma 9/9, ikinci istek 3.933 karakterlik izi baştan prefill ediyor. **Düzeltilemez** (ADR-0043 rejim değişmezi) |
| Eğitim hızı | **~70 s/it** (etkin batch 64) — kayıtlı 7 s/it **yanlıştı**. CP3 = ~85 dk / ~$3,2 |
| Havuz ön-elemesi | ❌ **net zararlı** (isabet 0,14) → koşulmuyor (ADR-0048 m.4) |
| Çevrimdışı örtüşme filtresi | ❌ elendi (%42→%30 ama geçerlilerin %24'ü kurban) |
| Sentetik `rejected` (API) | ❌ **YASAK** — üçüncü bir modelin hataları, Kapı 5'i çürütür |
| `causal-conv1d` | ❌ tavan 1,254× < 2,0× kapısı → eklenmedi |

## Doğrulanmış boru hattı (CP2-s)

```
τ_a eğitimi (--fresh-adapter, %0,65 eğitilebilir)  ✅ Modal'da koştu
norm-dengeli k-yollu TIES  (scripts/merge_ties.py) ✅ 224/224 tensör, gerçek ağırlıklarda
  operatör 4 özellikle sınandı; TIES(τ,−τ)=0 testi bir İŞARET HATASI yakaladı ve düzeltildi
GGUF Q4_K_M                                        ✅ 2,59 GiB, PURE=0
llama-server + 3 cevap                             ✅ 3/3 dolu
```

⚠️ Doğrulanmamış tek halka: **adaptörün volume'a yazılması** (smoke 6/50 adımda durduruldu).
Risk düşük — aynı yol `train_sft.py`'de defalarca koştu. CP3 zaten kullanacak.

## Sıra

```
CP2-c  hasat (Modal, ~1,5-3 sa)  → ilk 10 dk VERİM KAPISI: tahminin 2 katını aşarsa DUR
CP3    τ_a (~85 dk) + tekil ölçüm + τ_g+τ_a TIES merge onarım kontrolü
ARA KAPI  ADR-0045'in 2×2 tablosuyla oku → DUR, insana sun
CP4-CP5   ~$12,2 · ARA KAPI sonucu sunulmadan GEÇİLMEZ
```

## CP3'te ölçülecek iki tahmin

1. **Norm asimetrisi.** `adım × lr` kabası `τ_g` 0,108 ↔ `τ_a` 0,00073 → **~148×** olabilir
   (CP2-s'in sentetik kolunda 18×'ti). Doğruysa ADR-0036'nın norm-dengelemesi sanılandan çok daha
   ağır iş yapıyor. `‖τ_a‖_F` koşulsuz raporlanır.
2. **Çatışan parametre oranı.** Sentetikte %0,16 çıktı ama o kol `τ_g`'nin kopyasıydı. Gerçek
   `τ_g` ↔ `τ_a` çatışması ADR-0036'nın asıl merak ettiği sayı.

## Okuma sırası

1. [`docs/record/yurutme-tuzaklari.md`](docs/record/yurutme-tuzaklari.md) — **her koşudan önce**, özellikle yeni **6.1 · 6.2 · 6.3**
2. [`sprint2.md`](sprint2.md) — *"Elde ne var / ne yok"* + *"ADR-0049 ile kilitlenen beş karar"*
3. `research_log` [#45](docs/record/research_log/2026-07-30-cp2a-hakem-capalanmasi.md) · [#46](docs/record/research_log/2026-07-30-cp2r-kor-payda.md) · [#47](docs/record/research_log/2026-07-30-cp2s-boru-hatti.md)
4. [ADR-0048](docs/adr/0048-cevaba-kor-tuzak-gecerliligi.md) · [ADR-0049](docs/adr/0049-sprint2-kalan-kararlarin-kilitlenmesi.md)
