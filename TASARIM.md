# Law-FT / HakHukuk — Tasarım Belgesi

> **Statü:** YÜRÜRLÜKTE — bu hattın otorite tasarım belgesi
> **Tarih:** 2026-07-24
> **Kaynak:** `referans-design-doc.md` (kullanıcı taslağı) + repo kaydı (ADR-0001…0026, `docs/record/research_log/` 38 girdi)
> **Yöntem:** HITL hedef keskinleştirme — her karar tek tek tartışılıp kilitlendi.
>
> ⚠️ **`referans-design-doc.md` temiz kalır, değiştirilmez.** O belge taslağın kendisi; bu belge onun
> repo kaydıyla çarpıştırılıp keskinleştirilmiş hâli. Aradaki farklar §2'de kalem kalem yazılı.
>
> ⚠️ **Referans belgedeki sayılar somutlaştırma amaçlıydı** (VRAM bütçeleri, tier tablosu, rakip model
> sürüm adları). Bu belgeye **taşınmadılar.** Buradaki her sayı ya ölçülmüştür ve kaynağı yazılıdır,
> ya da "ölçülecek" olarak işaretlidir. İkisi karıştırılmaz.

---

## 0. Bu belge ne, nasıl okunur

Bu, **ne inşa edeceğimizin ve neyi ölçeceğimizin** belgesidir. Üç şeyi bir arada tutar:

1. **Kararlar** — ne yapılacak (§1, §3-§9)
2. **Elenenler** — ne yapılmayacak ve **neden** (§10, §11). Paper'ın *Methodology* ve *Limitations*
   bölümleri buradan yazılır; bu yüzden eleme gerekçeleri kararların kendisi kadar önemli.
3. **Açık uçlar** — henüz kararlaşmamış, ama işaretli (§13)

**Diğer belgelerle ilişki:** Kronolojik anlatı `docs/record/research_log/README.md`'de, kararların
donmuş gerekçeleri `docs/adr/`'de kalır — **ikisi de bu belge tarafından yeniden yazılmaz.**
Eski hattın (Gemma 4 12B) artefaktları `old-version-gemma4-12b/` altında; taşındı, silinmedi.

---

## 1. İki katmanlı iddia

### 1.1 Dış iddia — ana tez

> Dar ve yüksek-riskli bir domainde (Türk hukuku), tüketici donanımında **sıfır marjinal maliyetle**
> çalışan bir SLM + deterministik harness, kapalı ticari modellerin **dağıtım sınıfına**
> **maliyet-normalize paritede** ne kadar yaklaşır — ve bunun ne kadarını ince-ayar,
> ne kadarını harness sağlar?

Ana iddia tek cümlede: **"Bu maliyetle, buraya kadar çıkıyoruz."**

Bu bir **eşdeğerlik** iddiasıdır (D ≈ B), üstünlük iddiası değil. Eşdeğerlik testi fark testinden
daha çok örnek ister — §3.2'deki havuz büyütmesi bu yüzden opsiyon değil, ön koşul.

### 1.2 İç iddia — metodolojik katkı

> Beceri başına **bağımsız eğitilmiş** LoRA kolları + task-vector merge, **çatışan becerileri**
> (grounding ↔ abstention) ardışık ve tek-aşamalı SFT'den daha iyi koruyor mu?

Bu iddia havadan gelmiyor. Repo'nun beş turluk merkezi bulgusu grounding ile abstention'ın
birbirini yediğidir:

| kanıt | kaynak |
| :--- | :--- |
| Düz grounded SFT red oranını **sıfıra** indirdi | `research_log` #07 |
| v2c: grounding kazanırken M1 geriledi → **"Grounding-Abstention paradoksu"** | #24, ADR-0014 |
| M1 turlar boyunca yükseldi: 0.662 (base) → 0.737 (v2b) → 0.881 (v3) | #32 |
| …ama aynı turda **M2b 0.96 → 0.53 çöktü** ve M2 base'in altında kaldı | #32, ADR-0015 |

Ardışık eğitim bu çatışmayı *zaman içinde* çözmeye çalışır ve **unutmayla** öder. Task-vector merge
*ağırlık uzayında* çözmeye çalışır — TIES'ın işaret-çatışması mekanizması tam bu ortam için tasarlandı.
Yani iç iddia, repo'nun en pahalı negatif bulgusuna doğrudan bağlanan bir hipotez.

### 1.3 Terminoloji kuralı

Rakiplere paper'da **"frontier" denmez**, **"maliyet bandı"** denir. Böylece "hangisi frontier"
tartışması hiç açılmaz. *(Referans belgenin §2'si "frontier'a ulaşmak" derken §6'sı "amiral gemisiyle
değil workhorse sınıfıyla" diyordu — belge içi çelişki; bu kuralla kapatıldı.)*

---

## 2. Referans belgeden ne değişti

CLAUDE.md'nin sert kuralı: *bir karar eski bir belgeyle çelişiyorsa sessizce üzerine yazma, çelişkiyi
her iki yerde işaretle.* Tespit edilenler:

| # | Referans belgede | Bu belgede | Gerekçe |
| :-- | :--- | :--- | :--- |
| 1 | §2 "frontier'a ulaşmak" ↔ §6 "workhorse ile kıyas" | Maliyet-normalize parite; "frontier" terimi yasak | Belge içi çelişki; parite eşdeğerlik iddiasıdır |
| 2 | Abstention ekseni **yok** (yalnız distractor filtering) | Abstention **birinci sınıf** eksen | Repo 5 turda tam bu eksende tıkandı; doc'un ölçtüğü kolay yarı |
| 3 | §3 "Merge = TIES/SLERP" ↔ §4.1 `merge_and_unload()` matematiği | **Paralel kollar + k-yollu TIES/DARE** | TIES/DARE/SLERP çoklu task-vector teknikleri; ardışık tek-adaptör fuse'ta çözülecek çatışma yok |
| 4 | §6 tek hakem (Gemini), rakip de Gemini | **Dört katmanlı savunma** + aile-dışlama | Kendi ailesini puanlayan hakem = savunmada en kolay delinen yer |
| 5 | §6 ÖSYM/TRLawBench doğruluğu **ana** eksen | CANON ana, dış sınav **ikincil dilim** | Kapalı-kitap doğruluk = parametrik ezber = repo'nun M5 **anti-hedefi**; "güncellik kütüphanede" ilkesiyle çelişir |
| 6 | Rakipler **çıplak** koşuluyor | **Adalet kuralı:** harness herkese birebir | `D > A` iddiası değersizdir; asıl rakip *rakip + aynı harness* |
| 7 | §9 LightRAG çekirdek servis | **Deterministik yapısal graf** çekirdek; LightRAG kapılı Katman-1 kolu | Mevzuatın yapısı zaten açık; LLM ile tahmin etmek dominated. Halüsinatif kenar hukukta mülga hükmü yürürlükteymiş gibi ilişkilendirebilir ve ucuza doğrulanamaz. ADR-0022 ile hizalı |
| 8 | §8 dört donanım tier'ı (4B/9B/14B/32B) | **İki boyut noktası** | Her nokta ~5 eğitim koşusu; 4 tier tez bütçesini boyut eğrisine harcar. ADR-0018 "eğri" diyor, eğri için 2 nokta yeter |
| 9 | §3 veri: içtihat + dilekçe taramaları | İkisi de **plandan çıkar** (§10) | İçtihat korpusu yok (Bedesten'de var, TR IP + EDA gerekiyor); dilekçe = PII + lisans duvarı |
| 10 | §1/§10 OCR + STT + Tauri + Docker uçtan uca | **Ürün katmanı, ölçüm dışı** | İddia model+harness iddiası; OCR gürültüsü groundedness skoruna karışır, ayrıştırılamaz |
| 11 | §3 base = Qwen3.5-4B-Instruct | **Çalışma varsayımı**, sert doğrulama kapısına bağlı (§8) | ADR-0026: base bir parametre, gömülü karar değil |
| 12 | §3 Aşama 3 kuantizasyon Q4_K_M | **Q4_K_M doğru** (değişmedi) | ADR-0023'ün saf-Q4_0 kararı QAT'e özgüydü; QAT'siz base'de taşınmaz |

---

## 3. Ölçüm protokolü

### 3.1 CANON 6-mod korunur

| mod | ne ölçer | doğru davranış |
| :--- | :--- | :--- |
| **M1** | distractor altında kaynağa sadakat | gold'a dayan, distractor'a kapılma |
| **M4** | oracle tavan (tek doğru kaynak verili) | doğru cevap |
| **M2** | near-miss yanlış kaynak | **reddet** |
| **M2b** | çok-kaynak, gold yok | **reddet** |
| **M3** | boş bağlam | **reddet** |
| **M5** | kör / parametrik | **ANTİ-HEDEF** — yükselmesi istenmez |

**Değişmeyen sabitler:** seed **3407** · eval-mirror **900-char** chunk kırpma (eğitimde uygulanan
kırpma eval'de birebir uygulanır, yoksa model eğitildiğinden uzun bağlamla ölçülür) ·
**A1 = cevaplanan-only macro.**

⚠️ **Yeni base'in sayıları eski 12B tablosuna karıştırılmaz.** Protokol satırı ayrı tutulur (ADR-0025).

### 3.2 DEV / TEST ayrımı — **yeni**

Merge bedava olduğu için λ, TIES density ve DARE drop-rate taranmak isteniyor. Ama **taramayı CANON'a
bakarak yapmak dondurulmuş test setini seçim için harcamak** demektir; her sayı optimistik çıkar ve
savunmada yakalanır.

| set | rol | durum |
| :--- | :--- | :--- |
| `eval/canon/core_hard.jsonl` (40) + `trap.jsonl` (35) | **TEST** | 🔒 dondurulmuş, **nihai raporda BİR KEZ** görülür |
| **yeni üretilecek CANON-protokollü öğeler** | **DEV** | merge + hiperparametre seçimi burada |
| `eval/genelleme/` (3×35) | genelleme ölçümü | rolü değişmez, seçim için kullanılmaz |

Bu tek iş iki ihtiyacı karşılıyor: seçim seti doğuyor **ve** eşdeğerlik testinin ihtiyaç duyduğu
n büyümesi geliyor (mevcut 40/35 fark testi için bile sınırda).

### 3.3 Hakem — dört katmanlı savunma

1. **Omurga hakemsiz.** Abstention `score_abstention.py`'nin deterministik regex'iyle, atıf doğrulama
   Bedesten'e karşı deterministik olarak ölçülür. **İddia yüzeyinin çoğu hiç hakem görmez** — en güçlü savunma.
2. **Panel yalnız yargı gerektiren eksenlerde** (M1/M4 groundedness): üç aileden üç hakem,
   aralarındaki uyum (Cohen κ + Pearson) raporlanır. Altyapı hazır: `scripts/judge_agreement.py`.
3. **Aile-dışlama.** F ailesinden bir özneyi F ailesinin hakemi puanlamaz. 3 hakem × 3 aile ile her
   özne iki tarafsız hakem alır.
4. **Self-preference ölçülür.** Aynı özneyi kendi ailesinin hakemi ile diğerlerinin puanladığı fark
   raporlanır — sınır değil, **küçük bir bulgu.**

3× panel maliyeti yalnız yargı dilimine uygulanır; omurga hakemsiz olduğu için çarpan matrisin
tamamına yayılmaz.

### 3.4 Zorunlu ön-adım: regex kalibrasyonu

`score_abstention.py`'deki red-tespit regex'i Türkçe kalıplara göre, muhtemelen **tek bir model
ailesinin çıktısına bakılarak** yazılmış. Kalibre edilmezse rakiplerin reddini eksik sayar →
skorlarını düşürür → **bizim lehimize kayar.**

**Kural:** her rakip ailesinin çıktısında regex recall'ı ölçülür, kalıplar model-agnostik hale
getirilir, ~30 çıktı elle spot-check edilir. **Bu yapılmadan hiçbir sayı raporlanmaz.**

### 3.5 Sürüm kayması

Rakip modeller hareketli hedef. **Tarihli snapshot'lara pinlenir** — jenerik model adı kullanılmaz.
Ölçüm tarihi her summary'ye yazılır. Yapılmazsa hiçbir sayı tekrarlanabilir olmaz.

### 3.6 Dış geçerlilik dilimi

Tanınır bir TR hukuk sınav seti kapalı-kitap koşulur ve raporlanır — **ama hedef değildir**,
M5 ile aynı kategoridedir (ezber ölçer). Amacı jürinin *"bu şey gerçekten hukuk biliyor mu"*
sorusuna dışarıdan tanınır bir cevap vermek. Lisans durumu kullanmadan önce doğrulanır.

---

## 4. FT kolu — task-vector kafesi

### 4.1 Kollar

Üç kol, hepsi **ham base'den bağımsız** eğitilir. Bu bir stil tercihi değil geçerlilik şartı:
task-vector tanımı τ = θ_ft − θ_base ortak bir θ_base gerektirir. Bir kolu diğerinin üstüne eğitirsen
elde ettiğin şey task-vector değil ardışık SFT olur — yani ölçmek istediğin şeyin kendisini kaybedersin.

| kol | veri | satır | not |
| :--- | :--- | ---: | :--- |
| `τ_grounding` | `data/train/raft/` | 17.323 | gold + hard-negative distractor |
| `τ_abstention` | `data/train/orpo_abstain/` | 1.741 çift | ⚠️ `rejected` tarafı yeni base ile **yeniden hasat edilir** (`scripts/gen_v3_rejected.py`) |
| `τ_register` | `data/train/grounded_qa/` | 19.305 | **koşullu** — §7 register kapısına bağlı |

> **`rejected` neden yeniden hasat:** mevcut `rejected` satırları 12B'nin *gerçek fabrikasyonları.*
> Olduğu gibi kullanmak yeni modele **başka bir modelin hatalarını** öğretir. `chosen` ve tuzak
> kurgusu yeniden kullanılabilir. Tek çıkarım koşusu, eğitim değil.

### 4.2 Birleştirme

**Eşzamanlı k-yollu**, yinelemeli değil. TIES budama + işaret-seçimi + ayrık-ortalamayı tüm
vektörler üzerinde aynı anda yapar, dolayısıyla `TIES(TIES(τg,τa),τr) ≠ TIES(τg,τa,τr)`.
İkisi de meşru ama farklı şeyler; **eşzamanlı** olan TIES'ın tasarlandığı hâl. Yinelemeli birleşim
ekstra bir hücre olarak durabilir (maliyeti yalnız eval).

**Uygulama:**
- Her kol `ΔW = (α/r)·BA` olarak **bf16'da açılır** — TIES/DARE budama ve işaret-seçimini
  *eleman bazında delta üzerinde* yapar; LoRA'yı A/B matrisleri hâlinde birleştirmek yalnız doğrusal
  kombinasyon için geçerlidir.
- Birleştirme **tam ağırlık uzayında**, kuantizasyon **en son.** (Referans belge §4.2 bunu zaten
  doğru söylüyor: 4-bit tabana doğrudan merge çifte kuantizasyon hatası üretir.)
- **Host RAM'de koşar, GPU VRAM'e girmez.** Ve **akış hâlinde (tensör tensör)** yapılır: base
  tensörü + her kolun karşılık gelen ΔW'si yüklenir, TIES uygulanır, yazılır, bellek boşaltılır.
  Tam materyalizasyon (base + 3 kol aynı anda bf16'da) 4B'de onlarca GB'a çıkar ve karşıtlık
  noktasında host RAM'i de zorlar; akış hâlinde tepe bellek birkaç tensörle sınırlı kalır.

### 4.3 Kafes — 7 hücre

| grup | hücreler | ne söyler |
| :--- | :--- | :--- |
| **tekiller** | τg · τa · τr | her kol **tek başına** ne satın aldı |
| **çiftler** | τg+τa · τg+τr · τa+τr | hangi çift çatışıyor, ne kadar |
| **üçlü** | τg+τa+τr | amiral gemisi |

**Tekiller opsiyonel değil.** τ_abstention'ı tek başına ölçmeden ikili sonucunu atfedemezsin:
abstention düşükse sebep "merge çatışması" mı "kol zaten öğrenememiş" mi — ayırt edilemez.

**Ölçüm merdiveni** (paper anlatısı): τg → τg+τa → τg+τa+τr. Basamak basamak, bir yetenek eklenirken
öncekinin bozulup bozulmadığı gösterilir.

> ⚠️ **Bunlar bir zincir değil, iç içe alt kümeler.** Üçlü, ikilinin *üstüne* inşa edilmiyor;
> üç vektörün taze birleşimi. "Kademeli" olan **ölçüm merdiveni**, birleştirme süreci değil.
> Bu ayrım paper'da net yazılır.

### 4.4 Karşılaştırma tabanları

| taban | ne | koşu |
| :--- | :--- | ---: |
| **A** | tek-aşamalı **karışık** SFT (üç kolun verisi harmanlanmış) | 1 |
| **B** | **ardışık** SFT (referans belgenin orijinal kurgusu: domain → merge → reasoning → merge) | 2 |

İç iddia bu ikisine karşı kurulur. Taban B özellikle önemli: referans belgenin önerdiği kurgunun
kendisi, ve repo'nun unutma problemine çarptığı kurgu.

### 4.5 Kritik ölçüm koşulu

**Merge kafesi harness KAPALI ölçülür.** Red kapısı açıkken abstention'ı harness sağlar ve
model-düzeyi fark maskelenir — modelin bilmediği yerde dış sistem devreye girip zayıflığı örter.
Model yeteneği ile dış sistem desteğini izole etmek metodolojik zorunluluk.

---

## 5. Harness — deterministik dörtlü

| # | bileşen | arayüz | not |
| :-- | :--- | :--- | :--- |
| 1 | **Hibrit retriever** | `soru → top-k madde` | BM25 + TR embedding. `raft_pack.py`'nin bugün *simüle* ettiği şeyin gerçeği |
| 2 | **Yapısal graf** | `madde → {hiyerarşi, atıf-komşuları, sürüm-zinciri}` | **Parse ile, LLM yok.** Getirmede 1-2 hop genişletme |
| 3 | **Atıf doğrulayıcı** | `cevap → her atıf için {VAR, YOK, METİN_UYUŞMUYOR}` | Bedesten'e karşı doğrulama (`docs/BEDESTEN_API.md`, `scripts/bedesten_probe.py`) |
| 4 | **Red kapısı** | `doğrulama düşerse → cevabı redde çevir` | Modelin sahip olmadığı abstention'ı harness'ın **satın aldığı** yer |

**2, 3 ve 4 deterministik.** Sonuçları: marjinal maliyet ~0 (`$/sorgu` iddiasını bozmaz) ·
tekrarlanabilir (hakem varyansı yok) · **kapalı API'nin satın alamayacağı şey** — halüsine atıfı
*olasılıkla değil kesinlikle* yakalar.

**Harness GPU'ya girmez** (ADR-0023): embedder CPU'da, graf + vektör indeksi CPU RAM/disk'te.
8 GB bandında yığının açılma şartı bu.

### 5.1 Substrat

**NetworkX / GraphML** — gömülü, sunucu değil. ~40K düğüm + birkaç yüz bin kenar gömülü kütüphane
için önemsiz; bir Neo4j konteyneri, ayak izinin ölçüldüğü bir tezde saf yük. İhtiyaç **ölçüldüğünde**
sunucuya geçilir.

Ek kazanç: GraphML/NetworkX aynı zamanda LightRAG'in **varsayılan graf deposu.** Yani hibrit kol
açılırsa LLM-çıkarımlı kenarlar **aynı grafa** `provenance` etiketiyle yazılır; ablasyon
"ikinci sistem kur" değil **"kenar kaynağına göre filtrele"** olur — tek satırlık toggle, aynı
retriever, aynı eval. *(Interop iddiası bağlanmadan önce doğrulanır — repo kuralı: EDA-doğrula.)*

### 5.2 Adalet kuralı — pazarlıksız

**Harness tüm öznelere birebir aynı uygulanır.** Aynı retriever, aynı doğrulayıcı, aynı kapı,
aynı eşikler. Harness'ı sadece kendi modelimize verirsek tez ölür.

### 5.3 Korpus dondurma

**Eval'de retriever *ve* doğrulayıcı aynı dondurulmuş snapshot'ı kullanır.**

Retriever dondurulmuş + doğrulayıcı canlı olursa: snapshot'ta var olup ölçüm gününe kadar mülga
olmuş bir maddeye yapılan atıf haksız yere reddedilir → tekrarlanabilirlik kırılır, üstelik hata
zamanla büyür. Canlı Bedesten **ürün yolunda** kalır. *(Bu, `docs/superpowers/specs/2026-07-17-…`
§12'nin geçici cevabını — "eval için dondurulmuş, doğrulayıcı için canlı" — düzeltir.)*

**Snapshot pinleme:** korpus + türetilmiş graf/indeks **sha256 ile pinlenir** ve manifest'e yazılır.
Bugünkü zemin:

```
data/corpus/mevzuat_maddeler.jsonl   40.496 madde · 36 MB
sha256 51e220081801098e813cc68eeccd59ef5352571f6e3d28354e2f04a9610f6f07
```

⚠️ Türetilmiş artefaktlar (graf, vektör indeksi) git'e girerken **dosya başına 100 MB sınırına**
dikkat — GitHub o eşikte push'u reddeder (`data/README.md` git politikası).

### 5.4 Hibrit kavram katmanı — kapılı Katman-1

Deterministik graf **kavram** düğümlerini kapsamaz ("zamanaşımı", "ayıplı mal" gibi kavramların
kanunlar arası bağı). Ama o katmanın değeri büyük ölçüde **embedding ile örtüşür** — dense retriever
zaten o semantiği yakalıyor. Deterministik grafın değeri örtüşmez: *"madde 49'u buldun ama 50 onu
değiştiriyor, 72 zamanaşımını koyuyor"* hiçbir embedding'de yok.

> Deterministik graf = embedding'e **dik** katkı. Kavram grafı = **paralel** katkı. Marjinal değer asimetrik.

Buna rağmen kol plandan silinmiyor, çünkü *"LLM-indeksli graf masrafını hak ediyor mu"* literatürde
açık bir soru — LegalGraphRAG kazanç raporluyor, **maliyet/gecikme yükünü hiç raporlamıyor.**
Bizim maliyet-normalizasyon makinemiz tam da bu soruyu cevaplayacak alet.

**Kapı:** ilk ölçüm uçtan uca değil, **yalnız getirme** — `recall@k` + `MRR`, kavram kenarları
açık/kapalı. Jenerasyon yok, hakem yok. Getirmede iyileştirmiyorsa aşağı akışta iyileştiremez →
kol kapanır ve **"ölçtük, katkı yok"** negatif bulgusu olarak raporlanır.

---

## 6. Deney ızgarası — iki ayrı matris

Değişken kirliliğini önlemek için iç ve dış iddia **ayrı matrislerde** ölçülür.

### 6.1 İç ablasyon — harness KAPALI

**10 özne × 6 mod:** 7 merge hücresi + taban A (karışık SFT) + taban B (ardışık SFT) + çıplak base.

Cevapladığı soru: *ağırlık uzayında beceri çakışması nasıl davranıyor, merge onu koruyor mu?*

### 6.2 Dış parite matrisi

Her özne × {harness yok, harness var} × 6 mod:

| | harness yok | harness var |
| :--- | :---: | :---: |
| **Rakipler** (3 dağıtım-sınıfı) | A | **B** |
| **Bizim kazanan merge** | C | **D** |
| **Çıplak base** | (§6.1'den gelir) | **E** ← *ana ablasyon* |
| **Tavan referansı** | tek çizgi | — |

**Tavan referansı yalnız harness-yok koşulur.** Parite iddiasının öznesi değil, grafikte tek bir
referans çizgisi; iki koşula ihtiyacı yok. Adalet kuralı (§5.2) **parite öznelerini** bağlar —
tavan referansı o kümede değil, bu yüzden kural çiğnenmiş olmuyor. Paper'da bu açıkça yazılır.

- **İddia `D > A` ise değersizdir** — harness'ı sadece kendimize verip rakibi çıplak koşmak.
- **İddia `D ≈ B` ise tez vardır** — asıl rakip *rakip + aynı harness*.
- **`E` hücresi kaderi belirler:** `E ≈ D` → ince-ayar dekorasyon; `D > E` → iş bölümü doğrulandı.

**Tavan referansı** rakip değil, grafikte **tek referans çizgisi.** Parite iddia edilmez;
kapattığı delik: *"neden en güçlüsüyle kıyaslamadınız?"*

**İlgili çalışma:** Mecellem — **cite-only, yeni koşu yok** (ADR-0016). CPT foundation base o,
asistan değil; kategori farkı olduğu için "geçtim" iddiası kurulmaz.

### 6.3 Eğitim koşusu bütçesi

| nokta | koşu | nerede |
| :--- | ---: | :--- |
| **Birincil (~4B)** | 6 — 3 kol + taban A (1) + taban B (2) | çoğu **yerelde, $0** (RTX 5070) |
| **Karşıtlık (~8-9B)** | 4 — 3 kol + taban A; yalnız **kazanan** merge konfigürasyonu | Modal |

Kapı 0 `τ_register`'ı düşürürse sayılar **5 ve 3**'e iner ve kafes 7 hücreden **3**'e (τg · τa · τg+τa)
küçülür — anlatı merdiveni de iki basamağa iner. Bu bir kayıp değil: çatışan çift zaten o ikisi.

**Merge işlemlerinin eğitim maliyeti sıfır** — bedel yalnız eval'de. Bu, merge tekniği taramasını
gerçekçi kılan tek şey.

### 6.4 Maliyet muhasebesi

**İki maliyet karıştırılmaz:** *araştırma maliyeti* (eğitim koşuları, indeks kurma — bilimi yapmanın
maliyeti) ile *dağıtım maliyeti* (sorgu başına çıkarım — sistemi çalıştırmanın maliyeti).
**Tezin iddiası ikincisi hakkındadır.**

Compute **GPU-saat** olarak raporlanır ve **piyasa fiyatından** fiyatlandırılır. Sübvanse edilmiş
bir kaynak (HPC tahsisi vb.) kullanılsa bile $0 yazılmaz — çalışmayı tekrarlayacak bir hukuk bürosu
o tahsisi almıyor, A100 saatini piyasadan kiralıyor.

**Ana metrik: başabaş noktası.** Bizim `$/sorgu = eğitim_maliyeti / N + ~0` (N büyüdükçe düşen eğri);
rakip sabit `$/sorgu` (düz çizgi). Kesişim = **N\***: *"~N\* sorgudan sonra bizim sistem ucuz — ve
kalite kıyaslanabilir."* Jüri için somut; "sıfır maliyet" ifadesinden çok daha savunulabilir.

**Ölçülecekler:** `$/sorgu` · latency · throughput · VRAM · GPU-saat. Bugün mevcut tek maliyet
ölçümü `judge_cost_usd` — yani *not verme* maliyeti, *servis* maliyeti değil. **Açık borç.**

---

## 7. Kapılar — veriyi görmeden, ŞİMDİ yazılır

> Eşikler sonradan yazılırsa çıkan sonuç rasyonalize edilir. Proje pre-registration'ı zaten biliyor.
>
> ⚠️ **İsimlendirme:** kapılar **Kapı 0–4** diye anılır. `K1`/`K3` kısaltmaları repo'da **paper
> katkı haritası** için ayrılmıştır (K1 = ablasyon, K3 = ayrışma/negatif bulgular —
> `research_log/99-paper-esleme.md`); karıştırılmaz.

| kapı | ne zaman | ölçülen | karar |
| :--- | :--- | :--- | :--- |
| **Kapı 0 — register kolu** | eğitim öncesi | yeni base'in register-proxy'si | Yüksekse `τ_register` **düşer** (12B hattında 1.000'e oturmuştu, `research_log` #17); düşükse kol gerekçeli |
| **Kapı 1 — rakip boşluğu** | rakip baseline sonrası | **en iyi** rakibin M2 + ood dilimi | Rakipler çözmüşse "abstention'da yetişiyoruz" hikâyesi ölür → tez **maliyet + mahremiyet** eksenine yaslanır. *Neden en iyi rakip: soru "boşluk var mı"; herhangi biri çözüyorsa problem çözülebilirdir. Kendimize karşı en sert istatistik bu.* |
| **Kapı 2 — iş bölümü** | harness ablasyonu sonrası | **D** vs **E** | `D ≈ E` → *"bu domainde scaffolding ince-ayarı ikame ediyor"* — **kötü haber değil, yayımlanabilir bulgu.** `D > E` → iş bölümü doğrulandı |
| **Kapı 3 — hibrit kol** | getirme ölçümü sonrası | recall@k + MRR (± kavram kenarı) | İyileştirmiyorsa kol kapanır, negatif bulgu raporlanır |
| **Kapı 4 — karşıtlık noktası** | birincil ızgara sonrası | kazanan merge konfigürasyonu | Yalnız kazanan büyük boyutta tekrarlanır |

12B hattının referans değerleri (kıyas için, **12B protokolü, tarihsel**):
base M2 = 0.704 · v3 M2 = 0.593 · base ood = 0.889 · v3 ood = 0.483.

---

## 8. Base ve boyut noktaları

**Base bir parametredir, gömülü karar değil** (ADR-0026). Hiçbir script'te default yok; tanımsızsa
**erken hata** verilir — yanlış modele sessizce düşmek saatlerce süren bir koşuyu fark edilmeden
çöpe çevirir.

**Çalışma varsayımı:** referans belgenin önerdiği ~4B sınıfı instruct model (Qwen3.5-4B-Instruct).
**Hiçbir koşu, şu kapıdan geçmeden başlamaz:**

| # | kontrol | neden |
| :-- | :--- | :--- |
| 1 | **llama.cpp mimari desteği** | ADR-0025 eval yolunu llama.cpp'ye bağladı. Hibrit dikkat (Gated DeltaNet) katmanları varsa destek durumu ve KV matematiği farklıdır |
| 2 | **Şablon render'ı gözle doğrulanır** | `research_log` #38: minja bir şablon dalını yanlış render etti, model durmadı, bir CANON koşusu **sessizce** çöpe gitti |
| 3 | **Turn işaretleri assert edilir** | `train_sft.py` artık `--user-part`/`--assistant-part`'ı render'a karşı assert ediyor; yanlış işaretle `train_on_responses_only` hiçbir şeyi maskelemez, loss tüm diziden akar, **eğitim sessizce bozulur** |
| 4 | **Unsloth + sm_120 uyumu** | Yerel ortam borcu açık (`libnvJitLink.so.13`); `requirements.lock.txt` base seçilince yeniden kurulur |
| 5 | **Kuantizasyon** | QAT checkpoint'i yoksa **Q4_K_M** doğru varsayılan; `--pure` Q4_0 yalnız QAT için kalibreydi (ADR-0023, ADR-0026 ile parametreleştirildi) |
| 6 | **Lisans** | Saf Apache-2.0 mı, üstüne ek kullanım politikası var mı — attribution ve limitations'a yazılır |

**İki boyut noktası:**
- **Birincil ~4B** — tam ızgara (7 merge hücresi + 2 taban), çoğu yerelde $0.
- **Karşıtlık ~8-9B** — yalnız kazanan konfigürasyon. Eğri için ikinci nokta; ADR-0018'in
  "tek nokta değil eğri" şartını asgari düzeyde karşılar ve 12B hattının kapatamadığı
  **dış-geçerlilik açığına** (bulgular tek modele mi özgü?) kısmi cevap verir.

---

## 9. Veri

### 9.1 Elde hazır — base'den bağımsız, taşınabilir

| set | satır | rol |
| :--- | ---: | :--- |
| `corpus/mevzuat_maddeler.jsonl` | 40.496 | yer-gerçeği · graf kaynağı · her grounded üretimin zemini |
| `train/grounded_qa/` | 19.305 / 1.131 / 1.022 | `τ_register` · soru↔madde eşleşmesinin tohumu |
| `train/raft/` | 17.323 / 962 / 962 | `τ_grounding` (gold + hard-negative) |
| `train/orpo_abstain/` | 1.741 / 53 / 80 | `τ_abstention` (⚠️ `rejected` yeniden hasat) |
| `train/replay_tr.jsonl` | — | katastrofik unutmayı bastıran genel TR replay |
| `eval/canon/` | 40 + 35 | 🔒 **TEST** |
| `eval/genelleme/` | 3 × 35 | aile-ötesi genelleme |

### 9.2 Üretilecek

- **DEV havuzu** — CANON protokolünde yeni öğeler (§3.2). Hedef n açık soru (§13).
- **`rejected` yeniden hasat** — yeni base ile, tek çıkarım koşusu.
- **Yapısal graf** — korpustan parse: hiyerarşi · atıf ağı · mülga/değişik zincirleri.

### 9.3 Kalıcı kurallar

- **Kaynaksız QA verisi kullanılmaz.** İlk tur forum verisiyle battı: tek bir cevap 154 farklı soruya
  birebir yapıştırılmıştı (`research_log` #02). O set arşivde **uyarı olarak** duruyor.
- **Her yeni set EDA ile doğrulanır.** `newmindai/EuroHPC-Legal` kâğıt üstünde mükemmeldi
  (43K, Apache-2.0); örnekleme eşleşmeyen Q&A, uydurma kanunlar ve Osmanlı içeriği çıkardı → reddedildi.
- **Lisans-temiz.** Yalnız açık/kamu kaynak. Ticari kaynak (Lexpera, Kazancı) **asla** — telif zehiri.
- **PII maskelenir.**
- **Kapsam:** yalnız yürürlükteki TC mevzuatı.

---

## 10. Kapsam sınırları

### 10.1 İnşa edilebilir ama **ölçülmez** — ürün katmanı

OCR · STT · Tauri masaüstü app · Docker orkestrasyonu · dilekçe şablon sistemi.

İddia bir **model + harness** iddiası, uçtan uca sistem iddiası değil. Ayrıca teknik gerekçe:
OCR gürültüsü groundedness skoruna karışır ve ayrıştırılamaz. Türkçe'de ek bir tuzak: dedicated OCR
motorları genel VLM'leri yeniyor ve `ğ→˘g` / `ş→¸s` / `İ→Ì` kırılmaları hukuk metninde RAG
eşleşmesini bozar → doğru mimari **ayrık OCR preprocessor**, native VLM OCR değil.

### 10.2 Plandan çıkanlar

| çıkan | neden |
| :--- | :--- |
| **Dilekçe eğitim verisi** | Gerçek dilekçe = müvekkil PII + toplu açık yayını olmayan belge. Lisans-temiz + PII kurallarına kapalı. Yolu var (baro/Bakanlık **şablonları** + sentetik üretim) ama o ürün fazı |
| **CoT / gerekçe kolu** | Veri yok · CANON'da ölçüm modu yok · tümüyle hakem-bağımlı olurdu → "hakemsiz omurga" savunmasını zayıflatır |
| **İçtihat kolu** | Korpus yok; Bedesten sunuyor ama TR IP + hacim/lisans/PII doğrulaması + EDA gerekiyor. **Ama içtihat→madde atıfı deterministik olduğu için yapısal grafa girmeye aday** (eğitim kolu olmadan) |
| **Çok-ajanlı / LLM-indeksli GraphRAG (çekirdekte)** | Sorgu başına ek çıkarım → **doğrudan maliyet-normalize parite metriğinden düşer**; adalet kuralı gereği rakiplere de verileceği için maliyet iki taraflı katlanır. Kapılı Katman-1 kolu olarak duruyor (§5.4) |
| **32B tier** | Tek tüketici GPU'da eğitilemez; çekirdek parite çalışması bitmeden bütçeyi boyut eğrisine harcar |
| **CPT (continued pre-training)** | Ayrı bir tez. Kaynak gelse bile hayır — kapsamı patlatacak şey bu |
| **Agents / Faz 3-5** | Kapsam dışı, değişmedi |

---

## 11. Elenen alternatifler — *paper Methodology için*

| eleme | yerine | gerekçe |
| :--- | :--- | :--- |
| Doğruluk-yüzdesi (kapalı-kitap sınav) ana metrik | CANON 6-mod | Parametrik ezber ölçer; "güncellik modelin beyninde değil kütüphanesinde" ilkesinin **zıttı**. Repo bunu M5 anti-hedefi ilan etti |
| Tek güçlü hakem | Dört katmanlı savunma | Hakem ailesi özneyse self-preference savunmasız; tek hakem = tek bakış açısı, uyum ölçülemez |
| Ardışık FT + `merge_and_unload` | Paralel kollar + k-yollu TIES/DARE | Ardışık kurguda TIES/DARE/SLERP'in çözeceği çatışma yok; iç iddia "curriculum ablasyonu"na inerdi |
| LightRAG çekirdek harness | Deterministik yapısal graf | Mevzuatın yapısı zaten açık → LLM ile tahmin dominated. Halüsinatif kenar mülga hükmü yürürlükteymiş gibi ilişkilendirir ve **ucuza doğrulanamaz** (doğrulama = deterministik kurma emeği) |
| Neo4j sunucusu | Gömülü NetworkX/GraphML | Ayak izinin ölçüldüğü tezde konteyner saf yük; ~40K düğüm gömülü kütüphane için önemsiz |
| Retriever dondurulmuş + doğrulayıcı canlı | İkisi de dondurulmuş (eval'de) | Mülga olmuş maddeye atıf haksız reddedilir; hata zamanla büyür |
| Dört donanım tier'ı | İki boyut noktası | Eğri için 2 nokta yeter; 4 tier çekirdek çalışmayı aç bırakır |
| Rakipleri çıplak koşmak | Adalet kuralı | `D > A` iddiası değersiz |
| λ/density'yi CANON'a bakarak seçmek | DEV/TEST ayrımı | Dondurulmuş test setini seçim için harcamak = optimistik sayı |
| Hiperparametreleri sabitleyip taramamak | DEV'de tarama | "Merge çalışmıyor" ile "bu λ yanlış" ayrılamaz hale gelirdi; merge bedava olduğu için en büyük fırsat harcanırdı |

---

## 12. Riskler ve kalıcı sınırlar

| risk | etki | azaltma |
| :--- | :--- | :--- |
| **`E ≈ D`** — FT harness'ın üstüne bir şey eklemiyor | Tezin FT kolu değersizleşir | Kapı 2'de açıkça karşılanır; çıkarsa **negatif bulgu olarak yayımlanır** |
| **Merge kazanmazsa** | İç iddia düşer | Dış iddia ayakta kalır (matrisler ayrı, §6). "Ağırlık uzayı çözümü çatışmayı çözmedi" **yayımlanabilir** — task-arithmetic literatürüne domain-spesifik negatif kanıt |
| **Rakipler abstention'da ~1.0** | "Yetişiyoruz" hikâyesi ölür | Kapı 1; tez maliyet+mahremiyet eksenine yaslanır |
| **Regex kalibrasyonsuz** | Rakip skorları bizim lehimize kayar → tez çöker | §3.4 zorunlu ön-adım |
| **n yetersiz** | Eşdeğerlik iddiası kurulamaz | DEV havuzu büyütmesi (§3.2) |
| **Sürüm kayması** | Sayılar eskir | §3.5 tarihli pin |
| **Şablon/turn işareti tuzağı** | Bir koşu **sessizce** çöpe gider | §8 kapı 2-3; assert artık kodda |
| **Oracle-context gerçek RAG değil** | M1/M4 iyimser tavan | Harness ile gerçek retriever gelince kapanır |
| **Hakem = LLM** | İnsan-κ descoped (annotator yok) | §3.3 dört katman + hakemsiz omurga |
| **Eval ≠ dağıtım** | CANON bf16/NF4'te, dağıtım artefaktı kuantize → "dağıtım sınıfında parite" iddiasında delik | En az bir kez aynı CANON'da hizalama koşusu (kuantize vs bf16) |
| **VRAM tahminleri ölçülmedi** | Sığdırma merdiveninin sabit kalemleri tahmin | Gerçek donanım + gerçek GGUF ile ölçüm — **açık borç** |
| **Dış geçerlilik** | Bulgular tek base'e mi özgü? | Karşıtlık noktası **kısmi** cevap verir; tam replikasyon kapsam dışı → dürüst limitations |

---

## 13. Açık sorular

1. **TR embedding modeli** — hangisi? Lisansı? EDA-doğrulama kuralı burada da geçerli.
2. **Red kapısı eşiği** — tüm atıflar doğrulanmalı mı, çoğunluk yeter mi? Ablasyon adayı.
3. **DEV havuzunun hedef n'i** — eşdeğerlik için gerçek güç analizi yapılmalı; fark testi için
   hedeflenen n, eşdeğerlik için yeterli mi?
4. **Zamansal eksen** — *"atıf yapılan tarihte yürürlükte miydi?"* CANON'a yeni bir red kulvarı
   olarak eklensin mi, yoksa yalnız doğrulayıcı boyutu mu kalsın? Rakiplerin beceremediği eksen →
   tez değeri yüksek, ama eval matrisini büyütür.
5. **Hakem panelinin üçüncü ailesi** — üç büyük aile özneyse, panelde hangi üç aile? Aile-dışlama
   ile birlikte çözülmeli.
6. **İçtihat grafa girsin mi** — eğitim kolu olarak değil ama yapısal graf düğümü olarak
   (içtihat→madde atıfı deterministik). Bedesten + TR IP + EDA gerektirir.
7. **Yinelemeli vs eşzamanlı merge** — eşzamanlı seçildi; yinelemeli ekstra hücre olarak koşulsun mu?

---

## 14. Terminoloji

- **Parite** — eşdeğerlik (D ≈ B), üstünlük değil
- **Maliyet bandı** — "frontier" yerine kullanılır
- **Harness** — retriever + yapısal graf + atıf doğrulayıcı + red kapısı
- **Task-vector (τ)** — `θ_finetuned − θ_base`; ortak base şartı
- **Kafes** — 7 merge alt-kümesi (§4.3); "merdiven" onun içinden geçen anlatı yolu
- **Kapı** — önceden yazılmış eşikli karar noktası (§7)
- **A/B/C/D/E** — dış parite matrisi hücreleri (§6.2)
- **DEV / TEST** — seçim seti / dondurulmuş rapor seti (§3.2)

---

## 15. Bu belgeden türeyecek işler

| iş | dosya |
| :--- | :--- |
| Yeni ADR: tasarım kilitleri + süperseded işaretleri | `docs/adr/0027-…` (son numara 0026) |
| Vizyon revizyonu | `docs/VISION.md` |
| Teknik plan revizyonu | `docs/TEKNIK_PLAN.md` |
| Paper hedefi revizyonu | `docs/PAPER_TARGET.md` |
| FT playbook revizyonu | `docs/FINE_TUNING.md` |
| Proje talimatları revizyonu | `CLAUDE.md` |
| Görev listesi | `TODO.md` |

> **Kural:** çelişen eski kararlar **silinmez** — süperseded işaretlenir ve yeni ADR yazılır
> (ADR-0026'nın ADR-0017/0021 için yaptığı gibi). `docs/record/` ve `docs/adr/` içeriği yeniden
> yazılmaz; kronoloji kesintisiz akar. `data/`, `scripts/`, `knowledge/` ve arşiv dokunulmaz.
