# HakHukuk — Maliyet-Normalize Paritede Erişilebilir Bir Türk Hukuk Asistanı

### Tez İddiası, Değerlendirme Yöntemi ve Kanıtlanmış İlerleme

> **Danışman sunumu · 17 Temmuz 2026**
> Tez ekseni: *Dar bir domainde (Türk hukuku), sıfır-marjinal-maliyetle tüketici donanımında çalışan
> bir SLM+harness sistemi, kapalı ticari modellerin **dağıtım sınıfına** **maliyet-normalize paritede**
> ne kadar yaklaşır — ve bu yaklaşmanın ne kadarını ince-ayar (FT), ne kadarını harness sağlar?*
>
> Bu belge, projenin **ne olduğunu, neden bu yolu seçtiğimizi ve şimdiye kadar ölçülmüş gerçek
> sonuçları** özetler. Amaç bir hayal değil, **koşan ve loglanan bir araştırma programının** durum
> raporudur. Tüm sayılar `outputs/eval/*_summary.json` dosyalarına dayanır ve repodan yeniden
> üretilebilir (sabit seed, loglu koşu, temiz ablasyon).
>
> **Otorite belgeler:** `docs/superpowers/specs/2026-07-17-tez-cercevesi-design.md` + ADR-0017…0020.

---

## 0. Yönetici Özeti

**Problem.** Türkiye'de hukuki bilgiye erişim pahalı ve opak. Frontier LLM'ler (GPT, Gemini, Claude)
güçlü ama **kapalı, pahalı ve ölçekte her sorguya ödenmesi zor**; üstelik hukukta en tehlikeli
oldukları yerde — **var olmayan kanun/madde uydurmakta (hallucination)** — yapısal olarak açıklar.

**Tez iddiası (tek cümle).** *Dar bir domainde (TR hukuku), **~0 marjinal maliyetle** tüketici
donanımında (≤8 GB tercih bandı) çalışan bir SLM + harness sistemi, kapalı ticari modellerin
**dağıtım sınıfına** (Gemini 3 Flash · Claude Sonnet · GPT-5-mini) **maliyet-normalize paritede**
yaklaşabilir — ve bu yaklaşmanın kaynağı ölçülebilir şekilde **FT ile harness arasında ayrıştırılır**.*
Cümlenin çekirdeği: **"bu maliyetle, buraya kadar çıkıyoruz."**

**Yaklaşım.** Sıradan bir GPU'da çalışan küçük bir modeli (**Gemma 4 12B**, QLoRA ile ince-ayar →
QAT/Q4_0 kuantizasyon → ~6.5 GB GGUF) Türk hukuk diline adapte ediyoruz; etrafına deterministik bir
**harness** (retriever + atıf-doğrulayıcı + red-kapısı) kuruyoruz. Model her şeyi "bilmez"; iki
davranışı öğrenir: **grounding** (verilen kaynağa sadakat) ve **abstention** (cevap yoksa uydurmak
yerine reddetmek). Güncel bilgi ağırlıkta değil, kütüphanede (RAG) durur.

**Neden özgün.** İki boşluk var *(kaynak: research_log #35)*: (1) üretken, açık bir **TR-hukuk
grounding/abstention benchmark'ı yok**; (2) **açık-ağırlıklı, kullanıma hazır bir TR-hukuk asistanı
yok**. Ama tezin *ana* iddiası bir benchmark iddiası değil — **bir maliyet-parite iddiası**. Benchmark,
o iddiayı ölçmenin **altyapısı** (6-mod CANON), birincil katkı olarak değil.

**Nerede olduğumuz (dürüstçe).** İddianın **ince-ayar kolu** (FT arm) çalıştı: beş eğitim turu
(v0→v3) = tezin **proof-of-concept**'i. En iyi tur (v3, ORPO) grounding'i taban modelin belirgin
üstüne çıkardı (0.662 → **0.881**), ezberi neredeyse sıfırladı (0.225 → **0.075**) ve paper-değerinde
bir **negatif bulgu** üretti ("abstention tek beceri değil, bir davranış ailesidir"). **Henüz yapılmamış
olan:** rakip kapalı modellerin **kendi terazimizde çıplak ölçümü** (KAPI 1) + harness'ın inşası.
Aktif iş budur.

**Bir cümlede tez katkısı:** *Dar-domain bir SLM+harness sisteminin frontier dağıtım-sınıfına
maliyet-normalize paritesini ölçen bir çerçeve + FT-vs-harness katkı ayrıştırması — pozitif kadar
negatif bulgularıyla, tüketici donanımında.*

---

## 1. Problem ve Misyon

**Misyon:** Adalete erişimi demokratikleştirmek. Vatandaşın yanında duran, hukuk dilini sadeleştiren,
belge üreten ve kişinin kendi dosyasını anlamasına yardım eden bir yapay zeka asistanı.

Üç somut engel ve tezin cevabı:

| Engel | Açıklama | Tez'in cevabı |
| :--- | :--- | :--- |
| **Erişim maliyeti** | Hukuki danışmanlık pahalı; frontier LLM API'leri de öyle (ölçekte her sorgu ücretli). | **SLM + tüketici donanımı → ~0 marjinal maliyet.** Maliyet iddianın **birinci ekseni.** |
| **Halüsinasyon riski** | Genel LLM'ler var olmayan madde/karar uydurur — hukukta felaket. | **Grounding + abstention** eğitimi (model) **+ deterministik atıf-doğrulayıcı** (harness). |
| **Güncellik** | Yasalar değişir, ağırlıklar değişmez. | **Güncellik modelin beyninde değil, kütüphanesinde** (harness/RAG). |

**Tasarım prensipleri:**

- **Erişilebilirlik = maliyet-performans eğrisi** (tek nokta değil). ≤8 GB VRAM = **tercih bandı /
  soft gate**, sert yasak değil; aşan yapılandırmalar (12/16/24 GB) da eksende **kayıpla raporlanır**
  *(ADR-0018)*.
- **Birincil kitle = uzman (hukukçu).** Çıktı hassas ve atıflı. Vatandaş sadeleştirmesi *app-katmanı*
  prompt modu, modelin eğitim hedefi değil *(ADR-0010)*.
- **Lisans-temiz.** Yalnız açık/kamu kaynaklar (Mevzuat.gov.tr, Resmî Gazete, Yargıtay açık portal).
  Ticari kaynak (Lexpera/Kazancı) **kesinlikle yasak** — telif zehiri.
- **Tekrarlanabilirlik baştan.** Sabit seed, loglu koşu, temiz ablasyon — makale kapısı açık.

---

## 2. Tez İddiası — Maliyet-Normalize Parite

### 2.1 İddianın anatomisi

Klasik "12B > 4B, tabii ki" ya da "frontier'ı geçtik" tuzağına düşmüyoruz. İddia **iki eksenli**:

```
        kalite (6-mod CANON)
          ▲
   frontier│      ● Gemini 3.5 Pro / Opus  (TAVAN REFERANSI — rakip değil, tek çizgi)
   dağıtım │   ◐ Flash / Sonnet / 5-mini   (RAKİPLER — parite hedefi)
   sınıfı  │  ★ Bizim (FT + harness)        ← "bu maliyetle buraya çıkıyoruz"
          │ ○ base + harness               (E: harness'ın tek başına katkısı)
          └──────────────────────────────►  maliyet (marjinal, log-ölçek)
             ~0          $$          $$$$
```

- **Rakipler = kapalı ticari, DAĞITIM SINIFI:** Gemini 3 Flash · Claude Sonnet · GPT-5-mini. Modern
  frontier'ın *ölçekte gerçekten koşulan* katmanı (kimse her sorguya en üst-ucu ödemez) + bizim maliyet
  köşemize en yakın olan. **Parite hedefi bunlar.**
- **Tavan referansı (rakip DEĞİL):** Gemini 3.5 Pro · Claude Opus — grafikte tek çizgi. "Neden en
  güçlüsüyle kıyaslamadınız?" açığını kapatır; parite iddia edilmez, sadece tavanı gösterir *(ADR-0020)*.
- **Terminoloji disiplini:** paper'da rakiplere "frontier" **denmez**, **maliyet bandı** denir →
  "hangisi gerçek frontier" tartışması açılmaz.

### 2.2 Bu bir *eşdeğerlik* iddiası — istatistiksel incelik

> Bu, hocanın **istatistik + karar-analizi** uzmanlığına doğrudan konuşan noktadır.

Parite = "bizim sistem ≈ rakip" demektir; yani bir **fark** iddiası değil, bir **eşdeğerlik**
iddiası (D ≈ B). İstatistikte fark testi (t-test) burada **yanlış araçtır** — "fark bulamadık" ≠
"eşdeğer". Doğru araç **TOST (Two One-Sided Tests)**: önceden tanımlı bir eşdeğerlik payı içinde
kalındığını *pozitif olarak* gösterir. TOST fark testinden **daha çok örnek** ister → bu yüzden
n baştan büyük tutulur (**core_hard 100 / trap 75**), sonradan büyütmek zorunda kalmayalım diye.

### 2.3 Deney ızgarası — "ne kadarı FT, ne kadarı harness?" (2×2+E)

Tezin özgün analitik omurgası: parite'yi **kaynağına ayrıştırmak.**

| | **harness YOK** | **harness VAR** |
| :--- | :---: | :---: |
| **Rakipler** (kapalı) | **A** | **B** |
| **Bizim FT** (v4) | **C** | **D** |
| **base** (ham Gemma) | — | **E** ⭐ |

- **Adil kıyas = D vs B** (herkes aynı harness'la). "Modelimiz çıplak frontier'ı geçti" gibi haksız
  bir kıyas kurmuyoruz.
- **E = base + harness** = tezin **ana ablasyonu**: paritenin ne kadarı sadece harness'tan geliyor?
  (FT hiç olmasa ne olurdu?) FT'nin gerçek katma değeri = **D − E**.
- **Adalet kuralı (pazarlıksız):** harness tüm öznelere birebir aynı uygulanır — sadece kendi
  modelimize verirsek tez ölür *(ADR-0019)*.

### 2.4 İki-katmanlı güvenlik (KAPI 2 neden iki-boyutlu)

Halüsinasyonun iki tipi ayrı savunma ister:

- **Atıflı halüsinasyon** ("Madde X der ki…", ama X öyle demez) → **harness'ın atıf-doğrulayıcısı**
  deterministik yakalar.
- **Atıfsız halüsinasyon** (kaynak göstermeden uydurma) → yalnız **modelin kendi abstention'ı** yakalar.

Bu yüzden başarı kapısı iki boyutlu: (a) harness'lı marj (D vs E) **VE** (b) base-only dağıtım
güvenliği (v4-çıplak vs C). Base-only senaryoda (harness'sız, en ucuz dağıtım) modelin *kendi içi*
güvenli olmalı — harness yoksa atıfsız uydurmayı hiçbir şey durdurmaz.

---

## 3. Yöntem Mimarisi

### 3.1 Baz model ve neden SABİT

- **Baz:** **Gemma 4 12B** (`gemma-4-12B-it-qat-q4_0-unquantized`, Apache-2.0). **Kilitli** *(ADR-0017)*.
- **Neden Gemma sabit (Qwen'e geçmedik):** **QAT → Q4_0 zinciri maliyet iddiasının dayanağıdır.**
  Maliyet iddiasının en kırılgan halkası kuantizasyon kaybıdır; Gemma bunu **resmî QAT** ile
  garantiler (12B eğit → Q4_0 → ~6.5 GB → tüketici GPU → ~0 marjinal maliyet). QAT'siz bir base'i
  (Qwen) Q4_0'a kendi elimizle indirmek → *bilinmeyen* kalite kaybı, doğrudan tezin kalite ekseninden
  düşer. Kazanç ~1.5 GB, kayıp = iddianın temeli → değmez.
- **Dış geçerlilik sınırı (dürüstçe):** "bulgular Gemma'ya özgü mü?" sorusu tezde **açık bir
  limitations maddesi** + future-work. Tek-base bir çalışmayız; Qwen replikasyon kolu kapsam dışı.

### 3.2 İnce-ayar (FT kolu)

- **Yöntem:** **QLoRA** (4-bit NF4 + LoRA adaptörü, `r=16`, `α=32`, `all-linear`). 12B'nin tümünü
  değil küçük bir adaptör eğitilir → 12 GB laptop GPU'da bile mümkün.
- **Felsefe — "bilgi değil, dürüstlük":** modelin kafasına güncel kanun basmaya çalışmıyoruz. İki
  davranış: kaynak verilince ona **sadık kal** (grounding), kaynak yok/yanlışsa **uydurma, reddet**
  (abstention). Bu yüzden ana metrik *doğru-cevap-oranı* değil **groundedness**.
- **Dağıtım hattı:** İnce-ayar (NF4) → merge (bf16) → **Q4_0** (llama.cpp) → GGUF ~6.5 GB → 8 GB
  VRAM son-kullanıcı. Erişilebilirlik, 4B'ye *inmekle* değil, 12B'yi *kuantize etmekle* sağlanır.

### 3.3 Harness (Faz-2 dilimi — teze DAHİL)

> **Faz-sırası istisnası** *(ADR-0019)*: parite iddiası harness'sız kurulamaz (adil kıyas = "rakip +
> aynı harness"). Bu yüzden Faz 2'nin şu dilimi teze alındı:

- **Hibrit retriever** (BM25 + TR embedding) — doğru maddeyi getirir.
- **Bedesten API atıf-doğrulayıcı** (deterministik) — modelin verdiği atfı canlı mevzuata karşı
  doğrular; atıflı halüsinasyonu yakalar.
- **Red kapısı** (refusal-gate) — güven eşiği altında cevabı bloke eder.
- ❌ **Graph-RAG = kesin future-work, tezden HARİÇ** (parite iddiasına sıfır katkı, takvimin yarısını
  yer, iki hikâyeyi seyreltir).

### 3.4 Maliyet ekseni ve HPC

- **≤8 GB = soft gate;** erişilebilirlik bir eğri. Bellek darboğazı çoğu zaman ağırlık değil,
  uzun-RAG **KV-cache**'i → **TurboQuant** (arXiv:2504.19874, KV-cache 2.5–3.5 bit, eğitim gerektirmez,
  ağırlığa dokunmaz) *(ADR-0018)*.
- **HPC = yükselteç, bağımlılık DEĞİL.** Tez, HPC'siz (12B QLoRA = tek GPU) tek başına ayakta durur.
  **TÜBİTAK ULAKBİM → MareNostrum5** başvurusu gelirse boyut-eğrisi/replikasyon açılır (bonus).
  **Sübvansiyon maliyet iddiasından izole** — bedava compute'u "0 maliyet" saymayız; GPU-saat piyasa
  fiyatından raporlanır.

---

## 4. Değerlendirme Çerçevesi — Ölçüm Omurgası

> Parite bir *ölçüm* iddiasıdır; bu bölüm o ölçümün nasıl yapıldığıdır. Hocanın **çok-kriterli karar
> verme + örüntü tanıma + istatistik** uzmanlığına doğrudan konuşur.

### 4.1 Neden çok-kriterli

Tek skorla ("doğruluk %X") bir hukuk modelini değerlendirmek yanıltıcıdır: yüksek doğruluk
**aşırı-güvenle uydurmaktan** da gelebilir. Modeli **çok eksenli** ölçüyoruz; eksenler **birbiriyle
çelişebilir** (birini iyileştirmek başkasını bozar — klasik Pareto ödünleşimi).

**CANON değerlendirme seti — 6 mod + 1 register ekseni** *(ADR-0011)*:

| Eksen | Ne ölçer | Yön | Sezgi |
| :--- | :--- | :---: | :--- |
| **M1** grounding faithfulness | Distractor kaynaklar altında sadakat | ↑ | "Yanıltıcı ek metin varken doğruya bağlı kal" |
| **M4** oracle grounding | Temiz/doğru kaynak verilince tavan | ↑ | "Mükemmel getirme" üst-sınırı |
| **M2** yanlış-kaynak reddi | Near-miss (benzer ama yanlış) kaynağı reddet | ↑ | "Yakın ama yanlış → kanma" (**FT kolunun ana hedefi**) |
| **M2b** çok-kaynak ıska reddi | Doğrusu hiçbirinde yokken reddet | ↑ | "Birçok distractor, doğrusu yok → hiçbiri de" |
| **M3** boş-bağlam reddi | Kaynak hiç yokken reddet | ↑ | "Elimde belge yok → cevap veremem" |
| **M5** kör/parametrik doğruluk | Kaynaksız ezberden doğru cevap | ↓ | **Anti-hedef**: düşük = harness'e dayanıyor, ezberlemiyor |
| **register** uzman_frac | Uzman dili (vatandaş jargonu değil) | ↑ | "Hukukçuya hitap eden kayıt" |

Metodolojik incelikler:

- **Mod-stratifikasyon:** Her mod ayrı bir test dağılımı; skorlar modlar arası **ortalanmaz** — çünkü
  M2'yi düzeltmenin M2b'yi bozması *tam da görmek istediğimiz* sinyaldir.
- **Cevaplanan-only makro ortalama:** Grounding yalnız modelin cevaplamayı *seçtiği* örneklerde
  ölçülür → "her şeyi reddederek yüksek sadakat" hilesi engellenir; reddetme ayrı eksende (M2/M2b/M3).
- **Sabit protokol:** Gemma 4 12B + QLoRA · eval-mirror 900-char · **seed 3407** · n: core_hard 40,
  trap 35 (→ paper 100/75).

### 4.2 Hakem tasarımı — self-preference'ı kesmek

Rakipler kapalı ticari modeller olunca **hakem yanlılığı** kritik: OpenAI ailesi hem hakem
(gpt-4o-mini) hem özne (GPT-5-mini) olursa **self-preference** (Wataoka+) skoru bizim aleyhimize/
lehimize kaydırır. Çözüm üç katman:

1. **Cross-family panel** — hakem özneden farklı aileden (Claude/Gemini hakem), κ ile uyum ölçülür
   (`judge_agreement.py`: Cohen κ + Pearson + spot-check).
2. **Aile-dışlama** — bir özneyi kendi ailesinden hakem puanlamaz.
3. **Hakemsiz omurga** — reddetme `rejection_exact` regex'le (LLM-judge'suz) + atıf `Bedesten` API'yle
   deterministik doğrulanır. **⚠️ Ön-adım (zorunlu):** bu regex Gemma çıktısına göre yazıldı; rakip red
   kalıplarını ("cevap veremem" vb.) eksik sayabilir → **ölçümden önce kalibre edilir**, yoksa skor
   sessizce bizim lehimize kayar.

---

## 5. Eldekiler — FT Kolu (Proof-of-Concept)

v0→v3 = tezin **ince-ayar kolu**. Her tur bir öncekinin **ölçülmüş zaafını** hedefledi. Bu, "paritenin
ne kadarı FT?" sorusunun *bizim taraf* kanıtıdır. **(Çöpe gitmiyor — ADR-0017.)**

> **📎 Her turun tam reçetesi (yöntem + hiperparametre + veri kompozisyonu + kanıt dosyası) →
> [Ek C](#ek-c--proof-of-concept-tur-reçeteleri-kanıt-referanslı).** Bu ek, hocaya ve TÜBİTAK
> değerlendiricisine gösterilen **kabiliyet kanıtıdır**: veri mühendisliği → QLoRA-SFT → RAFT →
> tercih optimizasyonu (ORPO) → **özel trainer (MaskedORPOTrainer)** → eval-aynası hard-negative
> mining → literatür-çıpalı v4 tasarımı (DTA/ACL-2025).

### 5.1 Anlatı (ne denedik, ne oldu, ne öğrendik)

| Tur | Yöntem | Sonuç | Öğrenilen ders (kanıt) |
| :--- | :--- | :--- | :--- |
| **v0** | Forum verisiyle SFT | ❌ Battı | Model ezberledi; "7 Kasım 1982" ifadesini **154×** tekrarladı → forum verisi grounding değil, ezber öğretir. |
| **v1** | Grounded SFT | ❌ Net-negatif | Reddetme becerisini **yok etti** (trap-red 0.741 → **0.000**). SFT üslubu öğretir ama **abstention'ı söker.** |
| **v2b** | RAFT-SFT (distractor'a dayanıklı) | ✅ Kabul | Tüm kapıları geçti; grounding'i taban üstüne çıkardı. İlk sağlam temel. |
| **v2c** | Near-miss reddi, **düz SFT** ile | ❌ RED | Düz-SFT ile reddetme öğretmek yine grounding'i bozdu → **Grounding-Abstention paradoksu.** Abstention = *tercih* işi, SFT işi değil *(ADR-0014)*. |
| **v3** | **ORPO** (v2b üstüne tercih-optimizasyonu) | ⚠️ Kısmî | Paradoksu büyük ölçüde onardı: grounding **base'i geçti**, ezber sıfırlandı. Ama M2 base-altı kaldı + **yeni bir M2b regresyonu** *(ADR-0015)*. |
| **v4** | ORPO + **negatif-aile çeşitliliği** | ⚪ Koşullu | v3'ün açığını hedefler; ama artık **Kapı 1∧2'ye bağlı** (aşağıda). |

### 5.2 Skorkart — FT turları × eksenler

*(Protokol: Gemma 4 12B + QLoRA, seed 3407, hakem gpt-4o-mini. ↑ yüksek iyi, ↓ düşük iyi.
Kaynak: `docs/record/SCORECARD.md`.)*

| Eksen | Ne ölçer | base | v2b | v2c ❌ | **v3 ⚠️** | Mecellem¹ |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **M1** grounding faithfulness ↑ | distractor-altında sadakat | 0.662 | 0.737 | 0.681 | **0.881** | 0.713 |
| **M4** oracle grounding ↑ | temiz-kaynak tavanı | 0.978 | 0.968 | 0.974 | **1.000** | 0.783 |
| **M2** yanlış-kaynak red ↑ | near-miss abstention *(hedef)* | 0.704 | 0.346 | 0.407 | **0.593** | 1.000\* |
| **M2b** çok-kaynak ıska red ↑ | RAG-ıska abstention | 1.000 | 0.969 | 0.973 | **0.529** | 0.919 |
| **M3** boş-bağlam red ↑ | kaynak-eksik abstention | 1.000 | 1.000 | 1.000 | **1.000** | 1.000 |
| **M5** kör/parametrik doğ. ↓ | ezber *(anti-hedef)* | 0.225 | 0.175 | 0.125 | **0.075** | 0.350 |
| **register** uzman_frac ↑ | uzman dili | 1.000 | 1.000 | 1.000 | **0.975** | 0.200 |

<sub>¹ Mecellem = NewMind'ın CPT foundation base'i; **cite-only referans** (rakip değil, ADR-0016/0020),
completion-fewshot ile ölçüldü — birebir kıyas değil. \* M2=1.0'ı few-shot red-taklidi + **aşırı-reddetme**
patolojisidir (M4=0.78 ile paket gelir), gerçek yetenek değil.</sub>

**Genelleme (held-out, M2-modu):**

| Dilim | Ne test eder | base | v2b | **v3** |
| :--- | :--- | :---: | :---: | :---: |
| **xkanun** çapraz-kanun | yapısal tuzak (kolay-red) | 0.968 | 0.387 | **0.656** |
| **ood** held-out yeni soru | en zor (ilke vs kalıp) | 0.889 | 0.115 | **0.483** |

Örüntü net: **v3 ≫ batık-SFT (v2b) her yerde**, ama **v3 < base her yerde** → OOD (dağıtım-dışı) en
kırılgan nokta.

### 5.3 En değerli bulgu: "Abstention tek beceri değil, bir aile"

v3'ün ORPO'su "en ilgili kaynağı **SEÇ**" refleksini öğretti. Sonuç:

- **M2'de doğru:** Tek yakın-ama-yanlış kaynak → reddedebiliyor.
- **M2b'de yanlış:** Birçok distractor, doğrusu **hiçbirinde yok** → "hiçbiri değil" diyemiyor, en
  yakınını seçip **uyduruyor.**

Bu, 1.000 → **0.529**'luk M2b regresyonunu açıklar ve tezin merkezî **negatif bulgusudur:** reddetme
tekil bir yetenek değil, **farklı tuzak-tiplerine karşı ayrı ayrı öğretilmesi gereken bir davranış
ailesidir** *(ADR-0015 + research_log #32, #34)*.

---

## 6. Hedef vs Eldeki — Aktif İş ve Kapılar

### 6.1 Izgaranın neresi dolu, neresi boş

| Hücre | Ne | Durum |
| :--- | :--- | :--- |
| **C (kısmen)** | Bizim FT, harness'sız | ⚠️ v0→v3 ölçüldü; ama "oracle-context" gerçek retriever değil, **iyimser tavan** (mock). |
| **E (kısmen)** | base + harness | ⚠️ base çıplak ölçüldü; gerçek harness (retriever+doğrulayıcı+kapı) **henüz inşa edilmedi.** |
| **A / B** | Rakipler (± harness) | 🔴 **BOŞ** — hiç ölçülmedi. **Bu KAPI 1.** |
| **D** | Bizim FT + harness | 🔴 harness + v4 sonrası. |

### 6.2 Aktif iş = KAPI 1

**Rakip baseline'ı (Gemini 3 Flash · Sonnet · GPT-5-mini) kendi 6-mod CANON terazimizde çıplak ölç.**
- Aynı set/mod/n/seed/hakem; rakip inference = **OpenRouter** (tek anahtar, tarihli snapshot pin).
- **Ön-adım:** `rejection_exact` regex kalibrasyonu (§4.2).
- **Kapı çıktısı:** maks(rakip M2) **≥0.90** → parite açığı zaten kapalı olabilir, v4 gereksiz;
  **≤0.80** → açık gerçek, v4 devreye girer.

### 6.3 v4 artık KOŞULLU

Eskiden v4 zorunlu Faz-1-kapanışıydı; **artık Kapı 1∧2'ye bağlı.** Reçete kilitli (ORPO + negatif-aile
çeşitliliği, DTA dört-kadran, gold-absent sweep), ama **koşup koşmayacağımıza Kapı 1 karar verir.**
Bu, "önce ölç, sonra eğit" disiplinidir — kör eğitim değil.

> **Not:** v4 eğitimi, GPT-hakem skorlaması ve OpenRouter rakip-inference = **para-kapıları**;
> onay olmadan koşulmaz.

---

## 7. Beş-Faz Yol Haritası (Vizyon)

Tez = Faz 1 + Faz 2'nin **harness dilimi**. Sonrası ürün vizyonu. **Sıra katıdır** (tek istisna:
harness dilimi teze çekildi, ADR-0019).

```
Faz 1               Faz 2                 Faz 3                 Faz 4            Faz 5
LLM + FT      →     Harness (RAG)    →    Serving + Agentic  →  Niş Uzmanlık →  Vatandaş
SFT/ORPO           retriever+atıf+kapı    API + Workflow        Kira/İş/Tük.    Platformu
(← ŞU AN + Kapı 1)  ↑ dilim teze dahil                                         (Web+e-Devlet)
                    ✗ graph-RAG = future-work
```

- **Faz 2 — harness (teze dahil dilim):** hibrit retriever + Bedesten atıf-doğrulayıcı + red-kapısı.
  Graph-RAG (Neo4j/Memgraph) **tezden hariç, future-work.**
- **Faz 3 — Serving + Agentic + App:** vLLM/GGUF → FastAPI; LangGraph agent; TÜFE/RAG/Bedesten araç
  entegrasyonu; dilekçe şablonları.
  - **⚠️ OCR düzeltmesi (2026-07-17):** Gemma'nın "native multimodal"i base-seçim gerekçesi **değil**
    ve repoda tek bir görselli inference testi bile yok. Üstelik 12B ailenin OmniDocBench skoru
    ailenin en zayıfı (**0.164**) ve TR'de dedicated OCR motorları genel VLM'leri yener (OCRTurk,
    arXiv:2602.03693; `ğ→˘g` gibi kırılmalar hukuk metninde RAG eşleşmesini bozar). → **Doğru mimari:
    native OCR değil, ayrık bir OCR-preprocessor** (Faz 3 opsiyonu).
- **Faz 4 — Niş:** Kira/tahliye, işçi hakları, tüketici, KVKK domain workflow'ları.
- **Faz 5 — Vatandaş platformu:** sade web arayüzü, e-Devlet/UYAP entegrasyonu, gönüllü-avukat HITL
  geri-bildirim döngüsü (DPO).

**Örnek uçtan-uca akış (Faz 3-4 hedefi):**

```
Kullanıcı: "Ev sahibim kirayı %100 artırmak istiyor"
  → [Agent] Sözleşme tarihini sorar
  → [Tool] TÜFE API → güncel oran
  → [RAG] Güncel kira artış kuralı (TBK 344 + varsa geçici madde)
  → [Atıf-doğrulayıcı] Verilen maddeyi canlı mevzuata karşı doğrula
  → [Çıktı] İtiraz dilekçesi taslağı + ödeme/tevdi yöntemi açıklaması
```

---

## 8. Akademik Katkı ve Yayın Ekseni

1. **Ana tez:** Dar-domain SLM+harness sisteminin frontier dağıtım-sınıfına **maliyet-normalize
   paritesi** + **FT-vs-harness katkı ayrıştırması** (2×2+E ızgarası, E = base+harness ablasyonu).
2. **Katkı — ölçüm altyapısı:** Açık TR-hukuk **grounding/abstention benchmark'ı** (6-mod CANON) —
   literatürde yok. *Birincil değil, iddiayı ölçen altyapı.*
3. **Katkı — ampirik bulgu:** Küçük modeli "dürüst" davranmaya eğitmenin ablasyon serisi;
   **negatif bulgular birinci sınıf:** "SFT abstention'ı söker", "grounding-abstention paradoksu",
   "abstention bir davranış ailesidir".
4. **Future-work:** graph-RAG mimari karşılaştırması; çok-base replikasyon (dış geçerlilik).

**Neden negatif bulgular değerli:** Alan "SFT ile her şey düzelir" varsayımıyla dolu. Biz bunun
grounding-abstention ödünleşiminde **neden çöktüğünü** kontrollü ablasyonla gösteriyoruz — çok-kriterli
çerçeve olmadan **görünmez** kalırdı.

**Venue:** NLLP (EMNLP legal NLP workshop) — niş+sistem için ideal · LREC (benchmark tek başına) ·
Türkçe NLP venue (yedek).

---

## 9. Riskler, Sınırlar ve Sonraki Adımlar

**Bilinen sınırlar (dürüstçe):**

- **Dış geçerlilik — tek-base.** Bulgular Gemma 4 12B'ye özgü olabilir; QAT-zinciri gerekçesiyle
  base'i kilitledik → **açık limitations + future-work** (Qwen replikasyon kolu kapsam dışı).
- **"Oracle-context" gerçek RAG değil.** M1/M4, doğru maddenin metni *elle* prompt'a konarak ölçülür
  → gerçek retriever'ın **iyimser tavanı.** Gerçek harness (Faz 2 dilimi) inşa edilince skorlar düşebilir.
- **Rakip hücreleri (A/B) henüz boş.** Parite iddiası şu an *kurulu ama ölçülmemiş* — Kapı 1 bunu doldurur.
- **Hakem = LLM.** İnsan-κ descoped; cross-family + spot-check ile hafifletildi ama sınır olarak duruyor.
- **HPC belirsizliği.** MareNostrum5 gelmezse boyut-eğrisi kolu (Katman 2) kapanır — ama tez Katman 0'da
  ayakta (HPC = yükselteç, bağımlılık değil).

**Sonraki somut adımlar:**

1. **KAPI 1:** regex kalibrasyonu → rakipleri (Flash/Sonnet/5-mini) 6-mod CANON'da çıplak ölç (OpenRouter).
2. Kapı kararı: parite açığı gerçek mi? → v4 go/no-go.
3. **Harness dilimini inşa et** (retriever + Bedesten atıf-doğrulayıcı + red-kapısı) → B/D/E hücrelerini doldur.
4. TOST ile eşdeğerlik testi (n=100/75) → parite iddiasını istatistiksel olarak kur.

---

## Ek A — Künye (protokol referansı)

| Alan | Değer |
| :--- | :--- |
| **Ana iddia** | Maliyet-normalize parite (D≈B eşdeğerlik/TOST) + FT-vs-harness ayrıştırma (E=base+harness) |
| **Baz model** | Gemma 4 12B (`gemma-4-12B-it-qat-q4_0-unquantized`, Apache-2.0) — SABİT, QAT gerekçesi |
| **İnce-ayar** | QLoRA (NF4 4-bit + LoRA `r=16`, `α=32`, `all-linear`, dropout 0.05) |
| **Harness** | hibrit retriever (BM25+TR-embed) + Bedesten atıf-doğrulayıcı + red-kapısı (graph-RAG hariç) |
| **Rakipler** | Gemini 3 Flash · Claude Sonnet · GPT-5-mini (dağıtım sınıfı) · tavan ref: 3.5 Pro / Opus |
| **Ana metrik** | groundedness = FactScore (iddia böl→doğrula) + ALCE (atıf prec/recall, wrong_ref) |
| **Hakem** | cross-family panel + aile-dışlama + hakemsiz omurga (regex + Bedesten) |
| **Seed / protokol** | 3407 · eval-mirror 900-char · cevaplanan-only makro |
| **n** | core_hard 40→**100** · trap 35→**75** · E-set 40 (parite için baştan büyük) |
| **Eğitim / eval** | Modal A100 (eğitim) · yerel RTX 5070 (eval, $0) · rakip = OpenRouter |
| **Dağıtım hedefi** | Q4_0 GGUF ~6.5 GB → 8 GB VRAM son-kullanıcı (soft gate) |
| **Otorite dosyaları** | spec `2026-07-17-tez-cercevesi-design.md` · `docs/adr/` (0017-0020) · `docs/record/research_log/` · `SCORECARD.md` |

## Ek B — Terim Sözlüğü

- **SLM** — Small Language Model; erişilebilir donanımda çalışabilen küçük dil modeli.
- **Maliyet-normalize parite** — kaliteyi *eşit maliyet başına* kıyaslamak; "ucuza aynı işi" iddiası.
- **Dağıtım sınıfı** — frontier'ın ölçekte gerçekten koşulan katmanı (Flash/Sonnet/mini), en üst-uç değil.
- **TOST** — Two One-Sided Tests; **eşdeğerlik** testi (fark testi değil), parite iddiasının doğru aracı.
- **Harness** — modelin etrafındaki deterministik sistem: retriever + atıf-doğrulayıcı + red-kapısı.
- **QLoRA** — 4-bit kuantize modele küçük eğitilebilir adaptör (LoRA) → düşük-bellekte ince-ayar.
- **QAT** — Quantization-Aware Training; modeli kuantizasyona *dayanıklı* eğitmek → Q4_0 kaybını garantiler.
- **SFT / RAFT / ORPO** — örnek-taklidi eğitim / distractor'a-dayanıklı SFT / referanssız tek-aşama tercih optimizasyonu.
- **Grounding / Abstention** — verilen kaynağa sadakat / cevap yoksa uydurmak yerine reddetme.
- **Groundedness / FactScore / ALCE** — sadakati ölçen metrikler (iddiayı parçala→kaynağa doğrula + atıf doğruluğu).
- **Distractor / Near-miss / OOD** — kandırıcı yanlış kaynak / konu-yakın ama hukuken yanlış / dağıtım-dışı yeni soru.
- **Register** — dil kaydı; "uzman (hukukçu) dili" vs "vatandaş sadeleştirmesi".
- **CPT** — Continued Pre-Training; talimat-ayarından önceki ham alan-adaptasyonu (Mecellem böyle).
- **TurboQuant** — KV-cache'i 2.5–3.5 bit'e sıkıştıran, eğitim gerektirmeyen, ağırlığa dokunmayan yöntem.

---

## Ek C — Proof-of-Concept: Tur Reçeteleri (kanıt-referanslı)

> **Amaç:** Bu ek, "ne yaptım / neyi gösterebiliyorum" sorusunun **kanıtlı** cevabıdır. Her tur =
> ayrı bir metodolojik yetenek; her satırın **repo-içi kanıt dosyası** var (uydurma yok). Bu, bir
> tez danışmanına ve TÜBİTAK/HPC başvurusu değerlendiricisine **teknik olgunluk sinyalidir.**

### C.0 Genel FT protokolü (tüm turlarda sabit)

| Alan | Değer |
| :--- | :--- |
| **Base** | Gemma 4 12B (`gemma-4-12B-it-qat-q4_0-unquantized`, Apache-2.0) |
| **Yöntem** | QLoRA — 4-bit NF4 + LoRA (`r=16`, `α=32`, `target=all-linear`, dropout 0.05), gradient_checkpointing |
| **Adaptör boyutu** | ~65.5M eğitilebilir param (12B'nin ~%0.5'i) |
| **Eğitim yeri** | Modal serverless A100 (`--detach` = fire-and-forget, ADR-0008 dersi) |
| **Eval** | yerel RTX 5070 ($0) · seed **3407** · eval-mirror 900-char · hakem gpt-4o-mini · n=40/35 |
| **Değişmez kurallar** | lisans-temiz veri · sabit seed · loglu koşu · Modal para-kapısı · her skorkartta Mecellem sütunu |

### C.1 Tur-tur reçete + gösterilen kabiliyet

| Tur | Yöntem + hiperparametre / veri | Gösterilen kabiliyet | Sonuç (kanıt) | Kanıt dosyası |
| :--- | :--- | :--- | :--- | :--- |
| **v0** | Forum-QA SFT (ham forum verisi) | Baseline SFT pipeline + **başarısızlığı teşhis** | ❌ Battı: "7 Kasım 1982" **154×** tekrar; legal_acc 0.362→**0.124** | research_log #02 · `2026-06-07-v0-forum-basarisiz.md` |
| **v1** | Grounded SFT · **21.458** grounded Q&A (faithfulness kapısı **0.984**) · Modal A100, 1 epoch/1207 step, ~3.5h/~$10 | **Grounded sentetik veri üretimi + kalite kapısı** (gerçek madde→LLM üret→doğrula) | ❌ Net-negatif: abstention **0.786→0.000** (tuzakların %100'ünde uydurdu, param_leak=1.0) → *SFT üslubu öğretir, abstention'ı söker* (K3) | research_log #03/#04/#07 · `outputs/v1/` |
| **v2b** | **RAFT-SFT** (distractor'a dayanıklı) · base'den taze QLoRA · **19.305** cevap + **replay 600** · chunk-clip 900-char · train_loss **0.30**, 4h19m A100 | **RAFT** + replay ile katastrofik-unutma kontrolü + verbatim-quote formatı + uzman-register | ✅ **Tüm kapılar geçti:** M1 **0.904** · M4 0.975 · M2b **0.96** · M3 1.0 · M5 nötr · register 1.0. Tek açık: M2 0.346 | `docs/record/v2b/sonuclar.md` · `outputs/v2b/` |
| **v2c** | Near-miss reddi **düz SFT** ile · counterfactual + abstain_trap slice · sft_v2c train **17.353** (API=$0) | Hipotez testi: "abstention'ı SFT ile öğretebilir miyim?" → **kontrollü çürütme** | ❌ **RED:** M2 0.407 + M1 regresyon → **Grounding-Abstention paradoksu** (abstention = *tercih* işi, SFT işi değil) | research_log #24 · **ADR-0014** |
| **v3** | **ORPO** (v2b-continuation) · **MaskedORPOTrainer** (per-satır `is_pref` OR-maskesi, karışık-hedef: NLL-replay + tercih tek loss'ta, NaN-safe `torch.where`) · **eval-aynası** hard-negative (gold'a MAX Jaccard) · rejected = v2b'nin **gerçek fabrikasyonu** (harvest 1728 → 1504 fab, fab-oranı **0.870**) · chosen = muhakemeli-red · train **1741** (1449 abstain + 292 grounding)/val 53 · `beta=0.1`, `lr=1e-5`, 2 epoch/56 step, nll **7.65→2.96** (forget YOK) | **Tercih optimizasyonu (ORPO) + özel TRL trainer yazımı** (kaynak-okuma ile mixed-objective türetme, NaN/batch-varyans emniyeti) + **hard-negative mining** (eğitim-sertliğini eval'e eşleme) | ⚠️ **KISMİ:** paradoksu onardı (M1 0.662→**0.881**, M5 0.225→**0.075** ezber-sıfır) ama M2 0.593 (base-altı) + **M2b 1.0→0.529 regresyon** ("abstention bir ailedir" negatif bulgusu) | `docs/record/v3/recipe.md` · research_log #30/#32 · **ADR-0015** |
| **v4** 🔒 | **DTA-uyarlı ORPO** (Divide-Then-Align, ACL 2025) · tez-güdümlü **2-kadran** (retrieval-KB ✓→cevapla / ✗→reddet) + **✗✓-aşı dilimi** · ~**8K** çift · gold-absent oranı **SWEEP 0.3/0.4/0.5** (sıfır YASAK) · tek-şablon chosen (grounding-alıntı / abstain-uyuşmazlık) · gold-absent çiftte **doğru-cevap=REJECTED** (şanslı-tahmini cezala) · v2b-continuation · marj = iki-taraflı rejected-filtre | **Literatür-çıpalı tasarım** (DTA + Sufficient-Context + RefusalBench + ERA + CRaFT + RAAT sentezi) + ön-kayıtlı çok-kapılı hedef | 🎯 **Hedef (koşullu):** M2b≥0.90 · M2≥0.704 · xkanun≥0.90 · ood≥0.75 · M4/M1/M3/register≥v3 · M5≤0.10. Maliyet ~$15-40 | `docs/record/v4/recipe.md` · research_log #33/#34 |

### C.2 Reçetelerin anlattığı metodolojik yay (hocaya mesaj)

Bu altı tur rastgele denemeler değil, **teşhis-güdümlü bir dizi** — her tur bir öncekinin *ölçülmüş*
zaafını hedefler ve bir sonraki tekniği *gerektiği kanıtlandığı için* getirir:

1. **v0→v1:** ham veri işe yaramaz → **grounded sentetik veri + kalite kapısı** (veri mühendisliği).
2. **v1→v2b:** düz SFT abstention'ı söküyor → **RAFT + replay** (unutmayı kontrol et).
3. **v2b→v2c:** "SFT ile abstention" hipotezini **kontrollü çürüt** (paradoks kanıtı, negatif bulgu).
4. **v2c→v3:** SFT yetmiyor → **ORPO tercih optimizasyonu + özel trainer** (mixed-objective, kaynak
   kodu okuyarak türetildi; NaN/batch emniyeti mühendisliği).
5. **v3→v4:** "abstention tek beceri değil bir aile" bulgusu → **DTA (ACL 2025) literatür-çıpası** ile
   çok-kadranlı yeniden-kurgu.

**Kanıtlanan yetkinlikler:** QLoRA/PEFT · RAFT · ORPO/DPO ailesi · **TRL kaynak-seviyesi özelleştirme** ·
grounded sentetik veri üretimi + EDA-doğrulama · hard-negative mining · LLM-as-judge + cross-judge κ ·
ön-kayıtlı hipotez testi + **negatif bulgu disiplini** · maliyet-bilinçli bulut eğitim (Modal, para-kapısı).
Hepsi sabit-seed + loglu + repodan yeniden-üretilebilir → **HPC ölçeğine taşınmaya hazır bir pipeline.**

### C.3 HPC başvurusu için ölçek-gerekçesi (TÜBİTAK/MareNostrum5)

Mevcut pipeline **tek-GPU'da** (12B QLoRA) çalışır — bu, HPC'nin **gereksiz** değil, **yükseltici**
olduğunu gösterir (bkz. §3.4). HPC geldiğinde açılan Katman-2 kolları: (a) **base boyut-eğrisi**
(E4B/12B/26B aynı QAT hattında → erişilebilirlik-Pareto'yu doldur); (b) **n=100/75 → daha büyük**
TOST örneklemi; (c) v4 **gold-absent sweep**'i tek turda paralel; (d) çok-base **replikasyon**
(dış-geçerlilik sınırını kapatma kolu). Sübvansiyon **maliyet iddiasından izole** raporlanır.

---

> *Bu belge canlı bir araştırma programının anlık görüntüsüdür. Sayılar repodan yeniden üretilebilir;
> anlatı `research_log/` ve `adr/`'de tam kayıtlıdır. Aktif iş = KAPI 1 (rakip baseline, çıplak ölçüm).*
