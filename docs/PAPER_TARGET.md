# PAPER TARGET — Akademik Hedef Tasarımı

> **⚠️ KISMEN SÜPERSED — TEZ YENİDEN ÇERÇEVELENDİ (2026-07-17).** Bu belge **içeri-dönük** çerçeveyi
> (sistem paper'ı; ana iddia = "doğru VE anlaşılır tek model"; benchmark = yan iş) yansıtır. Yeni tez
> çerçevesi **dışarı-dönük**: *dar bir domainde (TR hukuku) SLM+harness, kapalı ticari modellerin
> dağıtım sınıfına **maliyet-normalize paritede** ne kadar yaklaşır — ve bunun ne kadarı FT, ne kadarı
> harness?* Ana iddia artık **maliyet-normalize parite** (eşdeğerlik/TOST), benchmark = **birincil katkı
> değil, ölçüm altyapısı.** Otorite belge: **`docs/superpowers/specs/2026-07-17-tez-cercevesi-design.md`**
> + **ADR-0017…0020.** Bu doküman **iz olarak** korunur (v0/v1/K3 kanıtı + eval protokolü hâlâ geçerli);
> "ana iddia" / "rakip tablosu" / "benchmark headline değil" ifadeleri yeni spec ışığında okunur.
> **Süregelen geçerli kısımlar:** §3 adil-kıyas (eşit dağıtım ayak izi), §5 eval protokolü (canon), §6 eldeki kanıt, §8 venue.
>
> **Amaç (orijinal):** Bu doküman, projenin akademik yayın hedefini tek yerde sabitler. Bundan
> sonraki eval/veri/sistem kararları **bu hedefe hizmet edecek** şekilde alınır
> (baseline'lar, insan-κ, sabit seed, ablasyon baştan tutulur → sonunda "veri
> toplama" değil "yazma" işi kalır).
>
> **Durum:** taslak v0 (2026-06-08). Açık kararlar sonda işaretli. İlgili:
> `[[eval-accuracy-gate]]`, `docs/_archive/FAZ1_PLAN.md` (arşiv), `docs/VISION.md`.

---

## 0. ODAK: bu bir SİSTEM paper'ı (benchmark yan iş)

Asıl katkı = **uçtan uca, tüketici donanımında çalışan, doğru + anlaşılır Türkçe
vatandaş hukuk asistanı SİSTEMİ.** Boru hattı:

```
Gemma-4-12B (encoder-free, unified)
   → law-domain SLM (QLoRA SFT — hukuki doğruluk/groundedness, sade DEĞİL)
      → RAG (TurboQuant'lı KV-cache + quantize vektör store)
         → Agentic katman (çok-adımlı: getir→hesapla→taslak→doğrula)
            → APP katmanı: prompt config → profesyonel (tam) / vatandaş (sadeleştir)
               → deploy: Q4_0 GGUF ~6.5GB / 8GB tüketici GPU
```

Benchmark (§ eski K1) **headline değil** — sistemi ölçmek için *gerekli ama yan*
bir araç. İyi çıkarsa ayrı (LREC) yayınlanabilir; çıkmazsa sistemin değerlendirme
bölümü olarak kalır. **Tek güçlü hikâye = sistem.**

## 1. Tek cümle tez (the claim)

> **Tüketici donanımında (8GB GPU) çalışan, hukuki olarak DOĞRU ve gerçek mevzuata
> DAYALI bir Türkçe hukuk asistanı; encoder-free bir SLM'i hukuki doğruluk/groundedness
> için fine-tune edip, TurboQuant'lı verimli RAG ile gerçek kanuna zeminleyip, agentic
> bir akışla uçtan uca bir sisteme dönüştürerek inşa edilebilir — ve aynı doğru model,
> APP katmanında prompt ile hem profesyonele (tam derinlik) hem vatandaşa (sadeleştirilmiş)
> hizmet eder.**

⚠️ **Kritik tasarım kararı (2026-06-08):** erişilebilirlik (sade dil) modele GÖMÜLMEZ —
**inference/app katmanında** çözülür. Gerekçe (v0 kanıtı): plainness'i ağırlığa fine-tune
etmek doğruluğu düşürüyor (K3). Bunun yerine *doğru+grounded* tek model + prompt-zamanı
sadeleştirme → tek modelden iki kitle.

Savunulabilir iddia = **sistem + groundedness/verimlilik**, "modelimiz onlarınkinden
büyük/iyi" DEĞİL. Kaynak yarışında (newmindai 112B token) kaybederiz; **groundedness +
tüketici donanımı kısıtında + tek-model-iki-kitle mimarisinde** kazanırız.

---

## 2. Hedef katkılar (öncelik sırasıyla)

> ℹ️ **Numaralama notu (eklendi 2026-07-01):** buradaki **K1/K2/K3 = paper KATKI (contribution)** etiketleridir (K1=sistem, K2=verimlilik, K3=ampirik bulgu). `docs/record/research_log/README.md`'deki **K1/K3 = paper BÖLÜM/deney-tipi** etiketleridir (K1=ablasyon tablosu, K3=ayrışma/negatif bulgular). İki şema FARKLI eksenler — karıştırma. research_log'un "K3=negatif bulgu"su bu belgenin "K3=ampirik bulgu" katkısını **besler** (aynı v0/v1 kanıtı).

**(K1 — ANA) Uçtan uca erişilebilir hukuk asistanı sistemi.**
encoder-free SLM → **uzman-register + grounding/abstention SFT** (⚠️ 2026-06-13/ADR-0010: "vatandaş-dilli SFT" değil — sade dil app-layer prompt) → TurboQuant'lı RAG → agentic akış, **tüketici
donanımında**. Doğruluğu RAG'le (gerçek madde) yüksek tut, **davranışı (grounding/abstention/format) SFT'le ver** (anlaşılırlık = app-layer),
çok-adımlı işi agent'la bağla (getir→hesapla→taslak→atıf doğrula). **Ablasyonla
kanıtla:** base → +SFT → +RAG → +agent → +atıf-doğrulama; her katmanın doğruluk/
anlaşılırlık/verimlilik katkısı ayrı.

**(K2 — DESTEK) Verimlilik: TurboQuant'lı RAG + Q4 deploy, 8GB GPU'da.**
TurboQuant (arXiv:2504.19874) KV-cache (uzun mevzuat context, ~256K) + quantize vektör
store. "Eşit/küçük dağıtım ayak izinde bu kaliteyi veriyoruz" — paper'ın *erişilebilirlik*
ekseni. `knowledge/summary_turboquant.md`.

**(K3 — DESTEK) Ampirik bulgu: SFT bilgi/plainness gömmek doğruluğu bozar + abstention'ı çökertir + mevcut metrik körlüğü → mimari sonuç.**
> ⚠️ **GÜNCELLENDİ (2026-06-13, research_log + ADR-0011):** K3'ün **ana** bulgusu artık **v1 SFT abstention çöküşü** (TRAP rejection 0.741→0.000; literatürde birebir = **Cor-RAIT UNDER-refusal**, yayınlı FT-harm'ın TERS yönü → özgün K3 bulgusu). v0 plainness bulgusu K3'ün *ikincil alt-bileşeni*.
Eldeki kanıt (bu projede ölçüldü, §6):
- **⭐ SFT abstention'ı yok ediyor** (v1: TRAP Rej* 0.741→0.000, tuzakların %100'ünde uydurdu; param_leak=1.000) → temiz grounded SFT bile kalibrasyonu siliyor → *abstention'ı KORU (replay + düşük-rank + CRaFT), bilgiyi RAG'e bırak* (mimari katkı, ADR-0012).
- **Plainness ağırlığa gömülünce doğruluk düşüyor** (v0: legal_acc 0.362→0.124) → *sade dili fine-tune etme, app-layer'da prompt ile yap* (ADR-0010).
- Mevcut hukuk reward modeli (Muhakim) **kısa-sade'ye kör + derinlik-yanlı** (`corr(sadelik, legal_acc)=−0.15`; grounded doğru cevaplara ≈0 verdi, elle doğrulandı) → erişilebilirliği yargılayamıyor.
- İki hakem doğrulukta **zayıf korele** (`+0.34` pooled, `−0.08` base) → tek metriğe güvenilemez; ana metrik **groundedness** olmalı.

**(YAN İŞ) Çift-eksenli değerlendirme aracı.**
Sistemi ölçmek için Muhakim (doğruluk kapısı) + anlaşılırlık metriği + göz testi +
hukukçu κ. Güçlü çıkarsa ayrı benchmark paper'ı (LREC); değilse sistemin eval bölümü.
**Headline değil.**

---

## 3. Adil kıyas çerçevesi (red gerekçesini baştan kes)

"12B > 4B, tabii ki" itirazını nötrle:
- **Dağıtım ayak izini eşitle.** Deploy hedefi = Q4_0 GGUF **~6.5GB / 8GB tüketici GPU**.
  Çerçeve: *"eşit dağıtım bütçesinde erişilebilir-hukuk SLM'i şunları geçiyor."*
- Compute/parametre bütçesini **raporla** (gizleme); "system vs system" çerçevesi
  "model vs model"den daha savunulabilir.
- Aynı sorular, aynı hakemler, aynı seed — herkes için tek protokol.

---

## 4. Rakipler / baseline tablosu (paper Tablo 1)

| Sistem | Tür | Boyut | Neden tabloda |
|---|---|---|---|
| **Bizim (Gemma-4-12B QLoRA + RAG + agent)** | decoder+sistem | 12B→Q4 ~6.5GB | ana katkı |
| `newmindai/Mecellem-Qwen3-4B-TR` | decoder | 4B | **en yakın decoder rakip** ⚠️ continual-pretrain (instruction-tuned DEĞİL) → "foundation karşılaştırması" diye çerçevele |
| `newmindai/Mecellem-Qwen3-1.7B-TR` | decoder | 1.7B | küçük-uç (aynı caveat) |
| `newmindai/Llama-3.1-8B-Instruct-*` (domain) | instruct decoder | 8B | instruction-tuned legal rakip (adil QA kıyası) |
| `newmindai/Llama-3.3-70b-Instruct` | instruct decoder | 70B | büyük TR-legal tavanı |
| HukukBERT | encoder | ? | ilgili görevde (atıf/segmentasyon) ref |
| GPT-4o / 4o-mini | kapalı | — | genel tavan |
| Ham Gemma-4-12B (fine-tune'suz) | decoder | 12B | bizim katkımızın izolasyonu |

> İlk somut adım: Mecellem decoder'ını **bizim skorkartımızdan** geçirip baseline'a koy.
> Muhakim'i hakem yapmak akıllıca — **onların kendi metriğiyle** kazanırsan itiraz edemezler
> (ama yanına anlaşılırlık metriği şart; Muhakim tek başına onların lehine yanlı).

---

## 5. Değerlendirme protokolü

> ⚠️ **SÜPERSED (2026-06-13, ADR-0011/0013) → güncel canon eval:** ana eval setleri artık
> **`data/eval/core_hard.jsonl` + `data/eval/trap.jsonl`** (CORE-HARD + TRAP), metrik sistemi
> **4-eksen CANON** (A1 groundedness / A2 correctness / A3 abstention / A4 format + A-register),
> mod-stratifiye (5 mod: M1 distractor / M2 TRAP / M3 E-set / M4 oracle / M5 KÖR), birincil araç
> **`scripts/bench_scorecard.py`** (`build_scorecard.py` DEĞİL). Aşağıdaki n=30 `eval_sample_v1`
> + serbest 1-10 protokolü v1-era'dır, iz olarak korunuyor.

- **~~Sabit test seti:~~ (v1-era)** vatandaş soruları (şu an `data/eval/eval_sample_v1.jsonl`, n=30 →
  paper için **n≥150-200**'e büyüt, niş-dengeli: kira/iş/icra/aile/tüketici/ceza). → **Güncel:** CORE-HARD + TRAP (pilot n=40/35, paper n=100/75).
- **ANA metrik = Groundedness (`scripts/groundedness.py`, KURULDU):** akademik format —
  **FactScore** (Min+2022) iki-aşamalı claim-level faithfulness (cevabı atomik iddialara böl →
  her iddiayı kaynak maddeye karşı SUPPORTED/CONTRADICTED/NOT_IN_SOURCE) + **ALCE** (Gao+2023)
  gold-bağlı atıf precision/recall + **wrong_ref_rate** (yanlış maddeye yönlendirme). Sayısal,
  tekrar-üretilebilir (`--runs N`), stil-bağımsız. Ölçüm: grounded veri faithfulness 0.97.
- **İkincil + ayrışma bayrağı:** ~~`scripts/build_scorecard.py`~~ → **güncel: `scripts/bench_scorecard.py`** (canon; ANA=groundedness, İKİNCİL=Muhakim,
  Sadelik=app sinyali). Ayrışma Grounded↔Muhakim → "Grounded↑ Muhakim↓" = Muhakim'in
  kısa-sade-doğruya körlüğü (**K3 kanıtı otomatik üretiliyor**).
- **Güvenilirlik katmanı (insan-κ DESCOPE, 2026-06-08):** fiziksel insan iş gücü kapasitesi yok →
  avukat-κ (≥2 avukat) bu kişisel/pre-akademik çalışma için ŞART DEĞİL, açıkça gelecek iş. Yerine
  SIFIR-EMEK vekil: **hakem-uyumu (inter-judge agreement: gpt-4o-mini ↔ gpt-4o, aynı şema)** +
  `--runs N` kararlılık + **opsiyonel yazar-örneklem** (~30 örnek maddeye-karşı). Hakem üreticiden
  FARKLI/güçlü (gpt-4o) olmalı — self-preference'ı kes. κ olmadan faithfulness **göreli** (sıralama)
  okunur, mutlak değil. Meşru: iddia = kaynağa-sadakat + rakip-göreli üstünlük, mutlak hukuki
  geçerlilik değil → avukat gerekmez. Paper'da bu sınır açıkça yazılır.
- **Tekrar-üretilebilirlik:** sabit seed (3407), loglu run (W&B), `requirements.lock.txt`,
  veri+model versiyonlama. CLAUDE.md zaten taahhüt etti.
- **Ablasyonlar:** (base) → (+SFT **uzman-register/grounding/abstention/format** — ⚠️ "sade" değil, ADR-0010) → (+RAG) → (+agent) → (+atıf doğrulama). Her
  katmanın doğruluk/anlaşılırlık/verimlilik katkısı ayrı ayrı.

---

## 6. Eldeki kanıt (şimdiden toplandı)

- base vs v0 skorkart: `outputs/PHASE1_REPORT.md`.
- Hakem-hakem ayrışması + 11 işaretli soru (insan denetimi için hazır).
- v0 echo/dejenerasyon bulgusu (kısa-veri artefaktı) — "fine-tune yan etkileri" bölümüne malzeme.
- → K2'nin (gerilim bulgusu) çekirdeği **zaten var**; sadece n büyüt + hakem-uyumu ekle (insan-κ descope).

---

## 7. Roadmap eşlemesi (ne zaman ne birikir)

| Faz | Paper'a katkısı |
|---|---|
| **Faz 1** (model) | K2 çekirdeği (gerilim bulgusu) + benchmark v1 + baseline tablosu |
| **Faz 2** (RAG/Graph) | K3'ün "doğruluğu RAG'le kurtar" yarısı + atıf doğrulama |
| **Faz 3** (agentic) | K3'ün agentic akışı + son ablasyonlar → **yazım** |

Paper, mevcut 5-fazın **doğal çıktısı** — şimdi yazılmaz, şimdi **ölçüm disiplini kurulur.**

---

## 8. Venue

- **NLLP** (EMNLP Natural Legal Language Processing workshop) — niş+sistem için ideal.
- **LREC** — benchmark (K1) tek başına buraya.
- Türkçe NLP venue (yedek/ek).

---

## 9. AÇIK KARARLAR (netleştirilecek)

- [x] **Başlık/scope: SYSTEM paper** (2026-06-08 kararı). Çekirdek = boru hattı
      (encoder-free SLM → TurboQuant RAG → agent, tüketici donanımı). Benchmark = yan iş.
- [ ] **TurboQuant kapsamı:** sadece KV-cache mi, yoksa vektör store quantization da mı
      ("turbovector")? Faz 2'de netleşir. `knowledge/summary_turboquant.md`.
- [ ] **Rakip kesinleştir:** Mecellem decoder HF'de public mi? Hangi checkpoint? (kontrol edilecek)
- [x] **Groundedness metriği operasyonelleştirildi (2026-06-08):** FactScore claim-level
      faithfulness + ALCE atıf P/R + wrong_ref_rate → `scripts/groundedness.py`. Paper-grade hakem =
      `--judge-model gpt-4o` (self-preference'ı keser).
- [x] **İnsan-κ DESCOPE (2026-06-08):** avukat-κ ŞART DEĞİL (insan iş gücü yok) → yerine hakem-uyumu
      (gpt-4o-mini ↔ gpt-4o) + opsiyonel yazar-örneklem; sayılar göreli. `[[eval-accuracy-gate]]`.
- [ ] **Anlaşılırlık metriği:** zeminlenmiş okunabilirlik nasıl ölçülür? (kelime/cümle uzunluğu +
      jargon-sözlük oranı + LLM-judge) — app/vatandaş-modu eval'i (Faz 3).
- [ ] **Test seti büyüklüğü + niş dağılımı** (n≥150-200, niş-dengeli).
- [ ] **Tek/çift-blind, hakem maliyeti** (vatandaş verisi PII maskeleme zaten kural).

---

## 10. Tek paragraf özet (abstract tohumu)

> Türkçe hukukta SLM'ler ya hukuki doğruluğa (encoder/retrieval) ya da genel akıcılığa
> odaklanıyor; vatandaşın *anlayacağı* doğru cevap ölçülmüyor. Biz (i) çift-eksenli,
> hukukçu-doğrulamalı bir Türkçe vatandaş hukuk QA benchmark'ı, (ii) sadeleştirmenin
> doğruluğu düşürdüğü ve mevcut hukuk reward modellerinin erişilebilirliğe kör olduğu
> ampirik bulgusunu, ve (iii) gerilimi çözen grounded-RAG + agentic bir sistemi sunuyoruz.
> Eşit dağıtım bütçesinde (8GB tüketici GPU) sistemimiz, güçlü Türkçe hukuk baseline'larını
> (Mecellem decoder, ham Gemma-4-12B, GPT-4o) hem doğruluk hem anlaşılırlıkta geçiyor.
