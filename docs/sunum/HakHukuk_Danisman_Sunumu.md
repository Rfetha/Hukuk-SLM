# HakHukuk — Erişilebilir Bir Türk Hukuk Dil Modeli

### Vizyon, Değerlendirme Yöntemi ve Kanıtlanmış İlerleme

> **Danışman sunumu · 14 Temmuz 2026**
> Tez ekseni: *Erişilebilir SLM'ler ile Türk Hukukunda Grounding-Odaklı Yapay Zeka Asistanı*
>
> Bu belge, projenin **ne olduğunu, neden bu yolu seçtiğimizi ve şimdiye kadar ölçülmüş
> gerçek sonuçları** özetler. Amaç bir hayal değil, **koşan ve loglanan bir araştırma
> programının** durum raporudur. Tüm sayılar `outputs/eval/*_summary.json` dosyalarına
> dayanır ve repodan yeniden üretilebilir (sabit seed, loglu koşu, temiz ablasyon).

---

## 0. Yönetici Özeti

**Problem.** Türkiye'de hukuki bilgiye erişim pahalı, dili kapalı ve vatandaş için opak.
Aynı zamanda, üretken dil modelleri hukukta en tehlikeli oldukları yerde — **var olmayan
kanun/madde uydurmakta (hallucination)** — sınırsızdır.

**Yaklaşımımız.** Sıradan bir tüketici GPU'sunda (hatta ~8 GB VRAM) çalışabilen küçük bir
dil modelini (**Gemma 4 12B**, QLoRA ile ince-ayar) Türk hukuk diline adapte ediyoruz.
Tez, modelin "her şeyi bilmesini" değil, **iki davranışı** hedefliyor:

1. **Grounding (dayanaklılık):** Kendisine verilen kaynak metne sadık kalmak.
2. **Abstention (çekimserlik):** Doğru cevap ortada yoksa **uydurmak yerine reddetmek.**

**Neden önemli.** Türk hukuku için **üretken, grounding-odaklı, açık bir değerlendirme
(benchmark) seti bugün mevcut değil.** Bizim çekirdek katkımız, bu boşluğu dolduran
**çok-kriterli, mod-stratifiye bir değerlendirme çerçevesi (6-mod CANON)** ve bu çerçeveyle
disiplinli bir şekilde koşulmuş bir **ablasyon serisidir** (v0 → v1 → v2b → v2c → v3 → v4).

**Nerede olduğumuz.** Beş eğitim turu koştu. En iyi tur (v3, ORPO tercihine dayalı ince-ayar)
grounding'i **taban modelin belirgin üstüne** çıkardı (sadakat 0.662 → **0.881**), ezberi
neredeyse **sıfırladı** (0.225 → **0.075**), ve reddetme becerisinin **tek bir yetenek değil,
bir davranış ailesi** olduğunu ortaya koyan **paper-değerinde negatif bir bulgu** üretti.
Aktif iş bu bulgunun çözümü olan **v4** turudur.

**Bir cümlede tez katkısı:** *Türk hukuku için açık bir grounding/abstention benchmark'ı +
küçük bir modeli erişilebilir donanımda "dürüst" davranmaya eğitmenin ampirik yol haritası —
pozitif kadar negatif bulgularıyla birlikte.*

---

## 1. Problem ve Misyon

**Misyon:** Adalete erişimi demokratikleştirmek. Vatandaşın yanında duran, hukuk dilini
sadeleştiren, belge üreten ve kişinin kendi dosyasını anlamasına yardım eden bir yapay zeka
asistanı.

Ama misyon tek başına yeterli değil; üç somut engel var:

| Engel | Açıklama | Tez'in cevabı |
| :--- | :--- | :--- |
| **Erişim maliyeti** | Hukuki danışmanlık pahalı; frontier LLM API'leri de öyle. | **Küçük model (SLM)** + tüketici donanımı hedefi. |
| **Halüsinasyon riski** | Genel LLM'ler var olmayan madde/karar uydurur — hukukta felaket. | **Grounding + abstention** eğitimi; ana metrik = dayanaklılık. |
| **Güncellik** | Yasalar değişir, model ağırlıkları değişmez. | **Güncellik modelin beyninde değil, kütüphanesinde** (Faz 2 RAG). |

**Tasarım prensipleri (kısaca):**

- **Erişilebilirlik > devasa performans.** Model sıradan bir GPU'da çalışabilmeli → SLM.
- **Birincil kitle = uzman (hukukçu).** Çıktı hassas ve atıflı. Vatandaş sadeleştirmesi
  *app-katmanı* prompt modu, modelin eğitim hedefi değil. *(Karar: ADR-0010, yürürlükte.)*
- **Lisans-temiz.** Yalnız açık/kamu kaynaklar (Mevzuat.gov.tr, Resmî Gazete, Yargıtay açık
  portal). Ticari kaynak (Lexpera/Kazancı) **kesinlikle yasak** — telif zehiri.
- **Tekrarlanabilirlik baştan.** Sabit seed, loglu koşu, temiz ablasyon — makale kapısı açık.

---

## 2. Boşluk ve Konumlandırma — Neden Bu Proje, Neden Şimdi

Piyasa taraması iki net boşluk gösterdi *(kaynak: research_log #35, ADR-0016)*:

1. **Üretken TR-hukuk grounding benchmark'ı YOK.** Mevcut hukuk benchmark'ları ya
   İngilizce/off-axis (LegalBench, BigLaw) ya da **çoktan-seçmeli** (law-MMLU türevleri,
   üstelik bazıları CC BY-NC + veri-zehiri). Bir modelin *serbest metinde* kaynağa sadık
   kalıp kalmadığını, uydurup uydurmadığını, ne zaman reddedeceğini ölçen **açık bir Türkçe
   set yok.** → **Bu bizim birincil katkımız.**

2. **Açık-ağırlıklı, kullanıma hazır TR-hukuk asistanı YOK.** En yakın açık çalışma
   (NewMind'ın Mecellem-4B'si) bir **CPT foundation base** — talimat-ayarlı bir asistan
   değil; register (dil kaydı) skoru 0.20, yani "asistan gibi konuşmuyor". Onu **rakip değil,
   referans nokta** olarak konumlandırıyoruz (yalnız cite-only kıyas, ADR-0016).

**Konum haritası:**

- **Frontier LLM'ler (GPT-4o, Gemini):** güçlü ama pahalı, kapalı, erişilemez ve halüsinasyona
  yapısal olarak açık → erişilebilirlik kısıtımızla çelişir.
- **CPT foundation base (Mecellem):** açık ama ham; asistan davranışı ve grounding disiplini yok.
- **HakHukuk:** ikisinin arasındaki **merkez** — erişilebilir donanımda çalışan, grounding ve
  abstention için özel eğitilmiş, uzman-registerli bir asistan.

---

## 3. Yaklaşım — Yöntem Mimarisi

### 3.1 Baz model ve ince-ayar

- **Baz:** **Gemma 4 12B** (`gemma-4-12B-it-qat-q4_0-unquantized`, Apache-2.0).
- **Yöntem:** **QLoRA** (4-bit NF4 + LoRA adaptörü, `r=16`, `α=32`, `all-linear`).
  Tüm 12B parametreyi eğitmek yerine küçük bir adaptör eğitilir → 12 GB'lık bir laptop GPU'da
  bile mümkün.
- **Dağıtım hattı:** İnce-ayar (NF4) → merge (bf16) → **Q4_0 kuantizasyon** (llama.cpp) →
  GGUF ~6.5 GB → **8 GB VRAM son-kullanıcı** hedefine ulaşılır. Yani erişilebilirlik,
  4B'lik bir modele *inmekle* değil, 12B'yi eğitim sonrası *kuantize etmekle* sağlanır.
- **Eğitim yeri:** Modal (bulut A100). **Değerlendirme:** yerel RTX 5070 ($0, sadece
  OpenAI hakem ücreti).

> **Küçük terim sözlüğü (Ek B'de genişletildi):** *SFT* = denetimli ince-ayar (örnek
> cevapları taklit et). *RAFT* = distractor kaynaklar arasından doğruya sadık kalmayı öğreten
> SFT çeşidi. *ORPO* = referanssız tercih optimizasyonu (iyi cevabı ödüllendir + kötüyü
> cezalandır, tek aşamada). *Grounding* = verilen kaynağa sadakat. *Abstention* = cevap yoksa
> reddetme.

### 3.2 Eğitim felsefesi — "bilgi değil, dürüstlük"

Kritik ve erken öğrenilen bir ders: **modelin kafasına güncel kanun basmaya çalışmıyoruz.**
Yasalar değişir, ağırlıklar değişmez. Onun yerine iki davranış eğitiyoruz:

- **Kaynak verildiğinde ona sadık kal** (grounding) — güncellik Faz 2'de RAG kütüphanesinden gelir.
- **Kaynak yok/yanlış/eksikse uydurma, reddet** (abstention).

Bu, ana metriğimizin neden *doğru-cevap-oranı* değil **groundedness** olduğunu açıklar:
FactScore (iddiayı parçala → her parçayı kaynağa karşı doğrula) + ALCE (atıf precision/recall,
yanlış-atıf oranı) birleşimi.

---

## 4. Değerlendirme Çerçevesi — Projenin Bilimsel Omurgası

> Bu bölüm, hocanın **çok-kriterli karar verme + örüntü tanıma + istatistik** uzmanlığına
> doğrudan konuşan bölümdür ve tezin en özgün katkısıdır.

### 4.1 Değerlendirmeyi çok-kriterli bir problem olarak kurmak

Tek bir skorla ("doğruluk %X") bir hukuk modelini değerlendirmek yanıltıcıdır: yüksek
doğruluk, **aşırı-güvenle uydurmaktan** da gelebilir. Bu yüzden modeli **çok eksenli** ölçüyoruz
ve eksenler **birbiriyle çelişebilir** (bir ekseni iyileştirmek başkasını bozabilir — klasik bir
çok-kriterli ödünleşim / Pareto durumu).

**CANON değerlendirme seti — 6 mod + 1 register ekseni** *(karar: ADR-0011)*:

| Eksen | Ne ölçer | Yön | Sezgi |
| :--- | :--- | :---: | :--- |
| **M1** grounding faithfulness | Distractor kaynaklar altında sadakat | ↑ | "Yanıltıcı ek metin varken doğruya bağlı kal" |
| **M4** oracle grounding | Temiz/doğru kaynak verildiğinde tavan | ↑ | "Mükemmel getirme" senaryosunun üst-sınırı |
| **M2** yanlış-kaynak reddi | Near-miss (benzer ama yanlış) kaynağı reddet | ↑ | "Yakın ama yanlış → kanma" (**tezin ana hedefi**) |
| **M2b** çok-kaynak ıska reddi | Doğrusu hiçbirinde yokken reddet | ↑ | "Birçok distractor, doğrusu yok → hiçbiri de" |
| **M3** boş-bağlam reddi | Kaynak hiç yokken reddet | ↑ | "Elimde belge yok → cevap veremem" |
| **M5** kör/parametrik doğruluk | Kaynaksız ezberden doğru cevap | ↓ | **Anti-hedef**: düşük = RAG'e dayanıyor, ezberlemiyor |
| **register** uzman_frac | Uzman dili (vatandaş jargonu değil) | ↑ | "Hukukçuya hitap eden kayıt" |

Bu tasarımın metodolojik incelikleri (hocaya cazip yönler):

- **Mod-stratifikasyon:** Her mod **ayrı bir test dağılımıdır**; skorlar modlar arası
  ortalanmaz, çünkü M2'yi düzeltmenin M2b'yi bozması *tam da görmek istediğimiz* sinyaldir.
- **Cevaplanan-only makro ortalama (ADR-0011):** Grounding, yalnızca modelin cevap vermeyi
  *seçtiği* örnekler üzerinde ölçülür — böylece "her şeyi reddederek yüksek sadakat" hilesi
  engellenir. Reddetme davranışı ayrı eksende (M2/M2b/M3) ölçülür.
- **LLM-as-judge + çapraz-hakem:** Puanlama gpt-4o-mini ile; makalede güvenilirlik için
  cross-judge gpt-4o (`judge_agreement.py`). İnsan-κ descoped → hakem-uyumu + ~30 yazar
  spot-check'i ile ikame edildi.
- **Sabit protokol:** Gemma 4 12B + QLoRA · eval-mirror 900-char · **seed 3407** · hakem
  gpt-4o-mini · n: core_hard 40, trap 35, E-set 40. Her hücre bir summary dosyasına dayanır.

### 4.2 Neden bu, standart bir doğruluk-benchmark'ından üstün

Bir modeli tek eksende "iyi/kötü" diye etiketlemek yerine, **davranış profilini** çıkarıyoruz.
Bu profil, iki modelin (ör. taban vs ince-ayarlı, ya da bizim vs Mecellem) **hangi eksende
neyi feda ederek kazandığını** görünür kılar — bir çok-kriterli karar analizi gibi. Aşağıdaki
bölüm bunun somut meyvesidir.

---

## 5. Yolculuk ve Bulgular — Ablasyon Serisi

Beş eğitim turu, her biri bir öncekinin **ölçülmüş zaafını** hedefleyerek koştu. Bu, tezin
"K1 = ablasyon" ve "K3 = negatif/ayrışma bulguları" eksenlerini besleyen ana anlatıdır.

### 5.1 Anlatı (ne denedik, ne oldu, ne öğrendik)

| Tur | Yöntem | Sonuç | Öğrenilen ders (kanıt) |
| :--- | :--- | :--- | :--- |
| **v0** | Forum verisiyle SFT | ❌ Battı | Model ezberledi; "7 Kasım 1982" ifadesini **154×** tekrarladı → forum verisi grounding öğretmiyor, ezber yaratıyor. **(K3)** |
| **v1** | Grounded SFT | ❌ Net-negatif | Reddetme becerisini **yok etti** (trap-red 0.741 → **0.000**). SFT, üslubu öğretir ama **abstention'ı söker.** **(K3)** |
| **v2b** | RAFT-SFT (distractor'a dayanıklı) | ✅ Kabul | Tüm kapıları geçti; grounding'i taban üstüne çıkardı. İlk sağlam temel. |
| **v2c** | Near-miss reddi, **düz SFT** ile | ❌ RED | Düz-SFT ile reddetme öğretme çabası yine grounding'i bozdu → **Grounding-Abstention paradoksu.** Abstention = *tercih* işi, SFT işi değil. **(K3, ADR-0014)** |
| **v3** | **ORPO** (v2b üstüne tercih-optimizasyonu) | ⚠️ Kısmî | K3'ü büyük ölçüde onardı: grounding **base'i geçti**, ezber sıfırlandı. Ama M2 base-altı kaldı + **yeni bir M2b regresyonu** çıktı. **(ADR-0015)** |
| **v4** | ORPO + **negatif-aile çeşitliliği** | 🟢 Planlı | v3'ün açığını hedefler: "doğrusu hiçbirinde yok → reddet" becerisini de eğit. |

### 5.2 Skorkart — tüm turlar × tüm eksenler

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

<sub>¹ Mecellem = CPT foundation base; **completion-fewshot** ile ölçüldü (aynı set/seed/hakem
ama birebir kıyas değil). \* Mecellem'in M2=1.0'ı few-shot red-taklidi + **aşırı-reddetme**
patolojisidir (M4=0.78 ile paket gelir) — gerçek bir yetenek değil.</sub>

**Genelleme (held-out, M2-modu):**

| Dilim | Ne test eder | base | v2b | **v3** |
| :--- | :--- | :---: | :---: | :---: |
| **xkanun** çapraz-kanun | yapısal tuzak (kolay-red) | 0.968 | 0.387 | **0.656** |
| **ood** held-out yeni soru | en zor (ilke vs kalıp) | 0.889 | 0.115 | **0.483** |

Örüntü nettir: **v3 ≫ batık-SFT (v2b) her yerde**, ama **v3 < base her yerde** → OOD (dağıtım-dışı)
en kırılgan nokta ve v4'ün ödevi.

### 5.3 En değerli bulgu: "Abstention tek beceri değil, bir aile"

v3'ün ORPO eğitimi, "en ilgili kaynağı **SEÇ**" refleksini öğretti. Sonuç:

- **M2'de doğru davranış:** Tek bir yakın-ama-yanlış kaynak var → onu reddedebiliyor.
- **M2b'de yanlış davranış:** Birçok distractor var, doğrusu **hiçbirinde yok** → "hiçbiri değil,
  reddediyorum" diyemiyor; en yakınını seçip **uyduruyor** (*"İlgili kaynak KAYNAK X'tir çünkü…"*).

Bu, 1.000 → **0.529**'luk M2b regresyonunu açıklar ve tezin merkezî **negatif bulgusudur:**
reddetme (abstention) tekil bir yetenek değil, **birbirinden farklı tuzak-tiplerine karşı ayrı
ayrı öğretilmesi gereken bir davranış ailesidir.** Bu içgörü doğrudan v4 tasarımını yönlendiriyor
*(ADR-0015 + research_log #32, #34)*.

---

## 6. Şu Anki Durum ve v4 Yönü

- **Kapanan:** v3 turu (ADR-0015). Grounding hedefine ulaşıldı, negatif bulgu belgelendi.
- **Aktif:** **v4** — yön NET, reçete + onay aşamasında.
  - **Birincil:** ORPO'nun rejected setine **çok-distractor-ama-doğrusu-yok (M2b-tipi)** +
    **OOD held-out** hard-negatifleri eklemek → "cevap hiçbirinde yok → reddet" becerisini de eğitmek.
    Motor: OOD-odaklı hard-negative mining + literatürden **DTA (Divide-Then-Align, ACL 2025)**
    dört-kadran çerçevesi.
  - **İkincil:** M2'yi taban üstüne itmek için near-miss negatif yoğunluğu/kalitesi (veri-kompozisyon).
  - **Sabit kural:** Reddetme her zaman **tercih (ORPO)** işi — düz-SFT ile "düzeltme" yasak (K3 tuzağı).
- **Tez sigortası:** Her tur, sayıları + kararı + dersiyle `docs/record/research_log/` ve
  `docs/adr/`'de kayıtlı. Makale, repodan haftalar sonra bile yeniden yazılabilir.

---

## 7. Beş-Faz Yol Haritası (Vizyon)

Faz 1 (bu tez) tamamlanmış bir temel; sonrası ürün vizyonunu tanımlar. **Sıra katıdır** —
her faz kendi başına bir çıktıdır.

```
Faz 1               Faz 2                Faz 3                 Faz 4            Faz 5
LLM Temeli    →     Güncel Bilgi    →    Serving + Agentic  →  Niş Uzmanlık →  Vatandaş
SFT+Benchmark      RAG + Graph          API + Workflow        Kira/İş/Tük.    Platformu
(← ŞU AN)                                                                     (Web+e-Devlet)
```

- **Faz 2 — RAG + Knowledge Graph:** "Yeni yasa çıktı, ne yapacağız?" sorusunun mimari cevabı.
  Hukuk ilişkiseldir (Kanun→Madde→Fıkra, atıf, yürürlük) → **Neo4j/Memgraph + vektör hibrit.**
  Akademik katkı: hukuk metinleri için vanilla-RAG vs graph-RAG vs hybrid karşılaştırması.
- **Faz 3 — Serving + Agentic + App:** vLLM/GGUF → FastAPI; LangGraph agent'ı; TÜFE/RAG/Bedesten
  araç entegrasyonu; dilekçe şablonları. Gemma 4'ün **native multimodal**'ı (belge OCR, sesli
  giriş) burada devreye girer.
- **Faz 4 — Niş:** Kira/tahliye, işçi hakları, tüketici, KVKK için domain-specific workflow'lar.
- **Faz 5 — Vatandaş platformu:** sade web arayüzü, e-Devlet/UYAP entegrasyonu, gönüllü-avukat
  HITL geri-bildirim döngüsü (DPO ile sürekli iyileştirme).

**Örnek uçtan-uca akış (Faz 3-4 hedefi):**

```
Kullanıcı [ses]: "Ev sahibim kirayı %100 artırmak istiyor"
  → [Audio] Model sesi anlar (native)
  → [Agent] Sözleşme tarihini sorar
  → [Tool] TÜFE API → güncel oran
  → [RAG/Graph] Güncel kira artış kuralı (TBK 344 + varsa geçici madde)
  → [Agent] Yasal sınırı hesaplar
  → [Çıktı] İtiraz dilekçesi taslağı + ödeme/tevdi yöntemi açıklaması
```

---

## 8. Akademik Katkı ve Yayın Ekseni

Yol haritası birden fazla yayınlanabilir çıktı üretir:

1. **Ana tez:** Erişilebilir SLM ile Türk hukukunda grounding-odaklı asistan.
2. **Katkı 1 (Faz 1):** **Açık Türk-hukuk grounding/abstention benchmark'ı** (6-mod CANON) —
   şu an literatürde yok.
3. **Katkı 2 (yöntem):** Küçük bir modeli erişilebilir donanımda "dürüst" (grounded + abstaining)
   davranmaya eğitmenin ampirik ablasyon serisi — **negatif bulgular birinci sınıf:**
   "SFT abstention'ı söker", "grounding-abstention paradoksu", "abstention bir davranış ailesidir".
4. **Katkı 3 (Faz 2):** Hukuk metinleri için graph-RAG mimari karşılaştırması.

**Neden negatif bulgular değerli:** Alan, "SFT ile her şey düzelir" varsayımıyla dolu. Biz
bunun grounding-abstention ödünleşiminde **neden çökmediğini/çöktüğünü** kontrollü ablasyonla
gösteriyoruz. Bu, çok-kriterli bir değerlendirme çerçevesi olmadan **görünmez** kalırdı — çerçeve
ile katkı arasındaki bağ tam da bu.

---

## 9. Riskler, Sınırlar ve Sonraki Adımlar

**Bilinen sınırlar (dürüstçe):**

- **"Oracle-context" gerçek RAG değil.** M1/M4, doğru maddenin metni *elle* prompt'a konarak
  ölçülür — yani gerçek retriever'ın **iyimser tavanı.** Gerçek RAG (Faz 2) daha düşük skorlar
  getirecektir; bunu açıkça işaretliyoruz.
- **OOD kırılganlığı.** v3 held-out yeni sorularda hâlâ base-altı (0.483) — v4'ün ana hedefi.
- **Hakem = LLM.** İnsan-κ descoped; cross-judge + spot-check ile hafifletildi ama sınır olarak duruyor.
- **Mecellem kıyası birebir değil** (farklı çıkarım protokolü) — cite-only konumlandırıyoruz.

**Sonraki somut adımlar:**

1. v4 reçetesini kilitle → negatif-aile hard-negative seti üret (M2b + OOD).
2. ORPO v4 eğitimi (Modal A100) → 6-mod CANON + genelleme dilimlerinde ölç.
3. Kapı kararı → ADR + skorkart güncelle.
4. Faz 1 kapanışı: benchmark setini paper-hazır paketle.

---

## Ek A — Künye (protokol referansı)

| Alan | Değer |
| :--- | :--- |
| **Baz model** | Gemma 4 12B (`gemma-4-12B-it-qat-q4_0-unquantized`, Apache-2.0) |
| **İnce-ayar** | QLoRA (NF4 4-bit + LoRA `r=16`, `α=32`, `all-linear`, dropout 0.05) |
| **Ana metrik** | groundedness = FactScore (iddia böl→doğrula) + ALCE (atıf prec/recall, wrong_ref) |
| **Hakem** | gpt-4o-mini (makalede cross-judge gpt-4o) |
| **Seed / protokol** | 3407 · eval-mirror 900-char · cevaplanan-only makro |
| **n** | core_hard 40 · trap 35 · E-set 40 |
| **Eğitim / eval** | Modal A100 (eğitim) · yerel RTX 5070 (eval, $0) |
| **Dağıtım hedefi** | Q4_0 GGUF ~6.5 GB → 8 GB VRAM son-kullanıcı |
| **Otorite dosyaları** | `docs/record/research_log/` (kronoloji) · `docs/adr/` (kararlar) · `docs/record/SCORECARD.md` (birleşik tablo) |

## Ek B — Terim Sözlüğü

- **SLM** — Small Language Model; erişilebilir donanımda çalışabilen küçük dil modeli.
- **QLoRA** — 4-bit kuantize edilmiş modele küçük eğitilebilir adaptör (LoRA) ekleyerek
  düşük-bellekte ince-ayar.
- **SFT** — Supervised Fine-Tuning; örnek cevapları taklit ederek eğitim.
- **RAFT** — Retrieval-Augmented Fine-Tuning; distractor kaynaklar arasından doğruya sadık
  kalmayı öğreten SFT çeşidi.
- **ORPO** — Odds-Ratio Preference Optimization; referanssız (tek-aşama) tercih optimizasyonu —
  iyi cevabı ödüllendirir, kötüyü cezalandırır. 12 GB'a uygun.
- **Grounding (dayanaklılık)** — modelin kendisine verilen kaynak metne sadık kalması.
- **Abstention (çekimserlik)** — doğru cevap yoksa/yanlışsa uydurmak yerine reddetme.
- **Groundedness / FactScore / ALCE** — sadakati ölçen metrikler: iddiayı parçalayıp her parçayı
  kaynağa karşı doğrulama + atıf doğruluğu.
- **Register** — dil kaydı; burada "uzman (hukukçu) dili" vs "vatandaş sadeleştirmesi".
- **Distractor** — doğruya benzeyen ama yanlış olan, modeli kandırmak için eklenen kaynak.
- **Near-miss** — konu olarak yakın ama hukuken yanlış kaynak (en zor red senaryosu).
- **OOD (out-of-distribution)** — eğitimde görülmemiş, dağıtım-dışı yeni soru/kanun.
- **CPT** — Continued Pre-Training; talimat-ayarından önceki, ham alan-adaptasyonu.

---

> *Bu belge canlı bir araştırma programının anlık görüntüsüdür. Sayılar repodan yeniden
> üretilebilir; anlatı `research_log/` ve `adr/`'de tam kayıtlıdır. Kod incelemesi bir sonraki
> adımdır.*
