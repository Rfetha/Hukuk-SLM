# 2026-07-17 — Tez çerçeve değişimi: içeri-dönük → maliyet-normalize parite ⭐⭐⭐

> **Tür:** karar/çerçeve (deney değil). **Otorite belge:** `docs/superpowers/specs/2026-07-17-tez-cercevesi-design.md`.
> **ADR'ler:** 0017 (çekirdek) · 0018 (8GB soft-gate) · 0019 (faz-sırası istisnası) · 0020 (rakip seti).

## Ne değişti (tek cümle)

Proje **içeri-dönük** ("FT base'i geçiyor mu?" — base/v2b/v3/Mecellem tek eksende, kalite) olmaktan
çıkıp **dışarı-dönük** hale getirildi: *dar bir domainde (TR hukuku) SLM+harness, kapalı ticari
modellerin **dağıtım sınıfına** **maliyet-normalize paritede** ne kadar yaklaşır — ve bunun ne
kadarını FT, ne kadarını harness sağlar?* Cümle: **"bu maliyetle, buraya kadar çıkıyoruz."**

## Neden (bağlam)

- Proje **Master tezi** çıktısı olarak konumlandı; danışmana sunulacak. Vizyon esneyebilir.
- **TÜBİTAK ULAKBİM → MareNostrum5** HPC başvurusu gündemde (TR PI uygun); compute kısıtı gevşeyebilir.
- Eski "FT base'i geçiyor mu?" sorusu bir tez için fazla dar + zaten kısmî cevaplandı (v3 KISMİ).
  Dışarı-dönük parite iddiası hem daha iddialı hem literatürde boşluk (üretken TR-hukuk grounding, #35).

## Kararlar (özet — detay ADR'lerde)

1. **Ana iddia = maliyet-normalize parite** (kalite × maliyet Pareto). Bir *eşdeğerlik* iddiası (D≈B),
   fark iddiası değil → **TOST**, daha çok örnek ister → **n=100/75 baştan** (ADR-0017).
2. **v0→v3 = proof-of-concept / FT kolu.** Çöpe gitmiyor; tezin ince-ayar kolunu oluşturuyor.
3. **Base = Gemma 4 12B SABİT (QAT).** Qwen3.5-9B'ye geçiş VE Qwen-ikinci-kol **ikisi de reddedildi**;
   gerekçe = **QAT→Q4_0 zinciri maliyet iddiasının dayanağı** (12B eğit → Q4_0 → ~6.5GB → tüketici GPU
   → ~0 marjinal maliyet). Dış geçerlilik ("Gemma'ya özgü mü?") = açık limitations (ADR-0017).
4. **Rakipler = kapalı ticari dağıtım-sınıfı:** Gemini 3 Flash · Claude Sonnet · GPT-5-mini. Tavan
   referansı (rakip değil): Gemini 3.5 Pro · Claude Opus. **Llama-8B/Nemotron ÇIKTI**, Mecellem cite-only
   (ADR-0020, ADR-0016 revize). Rakip inference = **OpenRouter** (yeni para-kapısı).
5. **8 GB = soft gate**, sert kısıt değil → erişilebilirlik bir **maliyet-performans eğrisi** (ADR-0018).
6. **Faz-sırası istisnası:** Faz 2'nin **retriever + atıf-doğrulayıcı + red-kapısı** dilimi teze DAHİL
   (parite harness'sız kurulamaz); **graph-RAG kesin future-work, HARİÇ** (ADR-0019).

## Deney ızgarası (2×2+E)

Özne {Rakipler / Bizim FT / base} × harness {yok / var} → hücreler A/B/C/D/E. **E = base+harness**
(tezin ana ablasyonu: "ne kadarı harness?"). **Adil kıyas = D (bizim+harness) vs B (rakip+harness).**
Adalet kuralı (pazarlıksız): harness tüm öznelere birebir aynı uygulanır.

## Kapılar (ön-kayıt)

- **KAPI 1 (aktif iş):** rakip baseline'ı 6-mod CANON'da **çıplak** ölç. Ön-adım = `rejection_exact`
  regex kalibrasyonu (Gemma'ya göre yazılı → rakip red kalıplarını eksik sayar). maks(rakip M2) ≥0.90
  → parite açığı kapalı; ≤0.80 → açık gerçek, v4 devreye girer.
- **KAPI 2 (iki-boyutlu, defense-in-depth):** harness'lı marj (D vs E) **AND** base-only marj
  (v4-çıplak vs C). Atıflı halüsinasyon → harness yakalar; atıfsız halüsinasyon → yalnız model-içi
  abstention yakalar → base-only dağıtım güvenliği ayrı ölçülür.
- **KAPI 3:** v4 go/no-go (Kapı 1∧2'ye bağlı). **v4 artık koşullu, zorunlu Faz-1-kapanışı değil.**

## Hakem tasarımı (mevcut altyapı yeter)

Self-preference riski (OpenAI hem hakem gpt-4o-mini hem özne GPT-5-mini) → **cross-family panel +
aile-dışlama + hakemsiz omurga** (`score_abstention.py` `rejection_exact` regex + Bedesten atıf-doğrulama).
`judge_agreement.py` (Cohen κ + Pearson + spot-check) zaten var.

## HPC konumu

**HPC = yükselteç, bağımlılık DEĞİL.** Tez Katman 0'da (12B QLoRA = tek GPU, HPC'siz) tek başına
ayakta. Sübvansiyon **maliyet iddiasından izole** — GPU-saat piyasa fiyatından raporlanır.

## Öğrenilen ders / paper-eşleme

- Dar-domain SLM+harness parite iddiası, "modelimiz daha büyük/iyi" yarışından çıkıp **maliyet köşesinde
  kazanma** çerçevesine geçince savunulabilir olur (kaynak yarışında newmindai 112B token'a kaybederiz).
- FT ile harness'ın katkısını **ayırmak** (E hücresi) tezin özgün analitik omurgası.
- Süregelen doküman hizalaması: CLAUDE.md, VISION.md, TEKNIK_PLAN.md, TODO.md, PAPER_TARGET.md (banner),
  ADR-0003/0006 (notlar), danışman sunumu — hepsi bu entry ile aynı turda güncellendi.
