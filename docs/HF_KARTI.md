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

# HakHukuk-4B — `v0.3` (Q4_K_M)

> **Bu dosya, Hugging Face model reposunun `README.md`'si olarak yüklenecek metindir.**
> Repodaki kaynağı burasıdır; HF'e kopyalanır, orada ayrıca düzenlenmez (S18'in dersi:
> aynı metin iki yerde durursa sessizce ayrışır).

## 🚨 ÖNCE BUNU OKUYUN — model TEK BAŞINA yayımlanan sayıyı ÜRETEMEZ

Bu modelin ölçülen **%80,1**'lik sadık-cevap kütlesi, **harness AÇIK** koşulunda üretildi:
soruyu cevaplamadan önce bir **retriever** ilgili mevzuat maddelerini bulup modele veriyor.

| gerekli parça | durumu |
| :--- | :--- |
| ağırlıklar (bu repo) | ✅ burada |
| kod (retriever + servis + terazi) | ✅ [github.com/Rfetha/Hukuk-SLM](https://github.com/Rfetha/Hukuk-SLM) |
| **arama indeksi** (`bge-m3`, 40.496 madde, ~80 MB) | ⛔ **HENÜZ YAYIMLANMADI** |

⇒ Modeli tek başına indirirseniz **çıplak** çalışır ve bu, ölçülen rejim **değildir**.
Kaynaksız koşulda modelin kendinden emin ve **yanlış** hukuk ürettiği ölçüldü.
İndeks dağıtımı açık bir iştir (repoda `Görev 8`): korpus yakında **8,4×** büyüyecek ve
bugünkü indeksi paketlemek birkaç hafta sonra atılacak bir iş olurdu.

## ⚠️ BU HUKUKİ TAVSİYE DEĞİLDİR

HakHukuk, hukuk metnini **anlaşılır kılmak** için yapılmış bir araştırma artefaktıdır.
Avukat değildir. Ürettiği her madde numarasını [mevzuat.gov.tr](https://www.mevzuat.gov.tr)
üzerinden **doğrulanması gereken bir iddia** olarak görün.
**Mevzuat değişir, ağırlıklar değişmez** — güncellik kütüphanenin işidir, modelin değil.

## Sayılar — hepsi kaynaklı

**DEV** (n=80, harness açık, k=10, önsözsüz, hakem `gpt-4o-mini`):

| | değer |
| :--- | ---: |
| sadık-cevap kütlesi | **0,8011** |
| `recall@10` *(kütlenin tavanı)* | 0,9500 |
| **uydurulmuş madde numarası** | **0/114** |
| aşırı-red *(gözle)* | 4/80 |
| isabetsizlik *(gözle)* | 8/80 |

**Donmuş TEST** (n=40, **tek kez** açıldı, 2026-09-09):

| | TEST | DEV |
| :--- | ---: | ---: |
| ham kütle | **0,5804** | 0,8011 |
| `recall@10` = tavan | 0,7500 | 0,9500 |
| tavan kullanımı | 0,7739 | 0,8433 |
| uydurulmuş madde | **0/52** | 0/114 |

⚠️ İki sayı **aynı metrik değildir** — setlerin erişim tavanı farklı. Düşüşün **%76'sı**
setin bileşiminden geliyor, **%24'ü gelmiyor**.

## Neden `v1.0` değil

Kapının üç maddesi DEV'de geçildi ve kabul testi koştu. `v1.0` yine de **verilmedi**:
yayımlanan her sayı hâlâ **tek hakem ailesinin** hükmü (`gpt-4o-mini`), ve iki aile arasında
ölçülen uyum **κ = 0,534** — aracın 0,6 eşiğinin **altında**.
⇒ **`v1.0`'ı bloke eden model değil, ölçüm aygıtıdır.**

## Rakip kıyası — kaynak verildiğinde, eşit sınavda

Aynı sorular, aynı 10 kaynak, aynı bütçe (n=80, gözle düzeltilmiş en muhafazakâr okuma):

| | kütle |
| :--- | ---: |
| Gemini 3.1 Flash-Lite | 0,7058 |
| Gemini 3.5 Flash | 0,7425 |
| Gemini 3.5 Flash-Lite | 0,7622 |
| **HakHukuk-4B (2,59 GiB, yerel)** | **0,8011** |
| Claude Sonnet-5 | **0,8348** |

⛔ Bu bir *"frontier'a karşı çıplak model"* kıyası **değildir** — hepsine kaynak verildi.
Sonnet-5 **önde**; tek önde olduğumuz eksen uydurulmuş madde numarası (**0** ↔ 2).

## Yöntem

İki LoRA kolu **ham base'den bağımsız** eğitildi (`τ = θ_ft − θ_base` bunu şart koşar) ve
**görev vektörü** olarak **ham TIES** ile birleştirildi; sonra Q4_K_M'e kuantize edildi.
Norm dengeleme **ablasyondur**, ana sonuç değil — ölçüm ADR-0036'nın çıkarımını **tersine
çevirdi**.

## Dosya

| | |
| :--- | :--- |
| dosya | `HakHukuk-4B-v0.3-Q4_K_M.gguf` |
| `sha256` | `755e15e92e9f7021934f2d5eada6c1f02fcc92be23f0536b0c2a0a9586e7bffc` |
| boyut | 2.783.446.720 bayt (2,592 GiB) |
| iç ad *(izlenebilirlik)* | `tgta_v1-q4_k_m.gguf` |

## Sınırlar

- Kapsam **yalnız yürürlükteki TC kanunları** (892 kanun · 40.496 madde); yönetmelik, tüzük,
  KHK, tebliğ **yok**.
- Tek boyut noktası (~4B) ⇒ *"bulgular bu base'e mi özgü"* sorusu **açık kalıyor**.
- `wrong_ref_rate` **0,0769** ↔ Sonnet-5 **0,0083**: madde **uydurmuyoruz** ama var olan
  **yanlış** maddeye atıf yapıyoruz. Açık borç.
- Her sayı tek hakem ailesinin hükmü; κ eşiğin altında.

Tam kayıt, reddedilen alternatifler ve her sayının kaynağı:
[github.com/Rfetha/Hukuk-SLM](https://github.com/Rfetha/Hukuk-SLM) —
`MODEL_CARD.md` · `docs/adr/` · `docs/record/research_log/`.
