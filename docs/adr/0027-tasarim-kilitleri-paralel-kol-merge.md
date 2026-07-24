# ADR-0027 — Tasarım kilitleri: paralel kol + task-vector merge; iki matris; DEV/TEST ayrımı

**Statü:** Yürürlükte · **Tarih:** 2026-07-24
**Otorite belge:** `TASARIM.md` (repo root)
**Kaynak taslak:** `referans-design-doc.md` (kullanıcı; **değiştirilmez, temiz kalır**)

**İlgili:** ADR-0003 (base — **süperseded**) · ADR-0011 (CANON — **genişletildi**) ·
ADR-0017 (tez çerçevesi — **parite kısmı YÜRÜRLÜKTE, teyit edildi**) · ADR-0018 (eğri — **somutlaştırıldı**) ·
ADR-0022 (graf kapsamı — **revize**) · ADR-0025 (eval yolu — base seçim kriteri oldu) · ADR-0026 (base parametre)

---

## Bağlam

ADR-0026 base'i bir parametreye çevirdi ve 12B hattını emekli etti, ama **yeni hattın ne olacağını
söylemedi.** Kullanıcı bunun üzerine bir sistem tasarım taslağı hazırladı (`referans-design-doc.md`):
Qwen sınıfı ~4B base, kademeli QLoRA + Mergekit, Graph-RAG (LightRAG), OCR/STT servisleri,
Tauri masaüstü app, Docker orkestrasyonu, ve dış benchmark tabanlı bir eval.

Taslak repo kaydına karşı okundu ve **HITL yöntemiyle** — her karar tek tek tartışılıp kilitlenerek —
keskinleştirildi. Tespit edilen sekiz gerilimin tamamı karara bağlandı. Sonuç: `TASARIM.md`.

Bu ADR o oturumun **donmuş kararlarını** ve **eleme gerekçelerini** kaydeder.

---

## Karar

### 1. İki katmanlı iddia

- **Dış (ana tez):** maliyet-normalize parite — **ADR-0017'nin çerçevesi yürürlükte, teyit edildi.**
  Taslağın §2'si "frontier'a ulaşmak" derken §6'sı "amiral gemisiyle değil workhorse sınıfıyla"
  diyordu; belge içi çelişki parite lehine kapatıldı. **Terminoloji kuralı:** paper'da "frontier"
  denmez, **maliyet bandı** denir.
- **İç (metodolojik, YENİ):** *beceri başına bağımsız eğitilmiş LoRA kolları + task-vector merge,
  çatışan becerileri (grounding ↔ abstention) ardışık ve tek-aşamalı SFT'den daha iyi koruyor mu?*

İç iddia repo'nun en pahalı negatif bulgusuna bağlanıyor: düz SFT reddi sıfıra indirdi
(`research_log` #07) · Grounding-Abstention paradoksu (#24, ADR-0014) · v3'te M1 0.881'e çıkarken
M2b 0.96→0.53 çöktü (#32, ADR-0015).

### 2. FT mimarisi: paralel kollar, ardışık değil

Taslak §3 "Merge Stage: TIES/SLERP" diyordu ama §4.1 `merge_and_unload()` matematiğini yazıyordu.
**TIES/DARE/SLERP çoklu task-vector teknikleridir**; ardışık tek-adaptör fuse'ta çözülecek işaret
çatışması yok, seçilecek algoritma yok. O kurguda iç iddia "curriculum ablasyonu"na inerdi.

Karar: üç kol (`τ_grounding` · `τ_abstention` · `τ_register`) **ham base'den bağımsız** eğitilir —
task-vector tanımı (τ = θ_ft − θ_base) ortak base şartı koyar; bir kolu diğerinin üstüne eğitmek
task-vector değil ardışık SFT üretir.

- Birleştirme **eşzamanlı k-yollu** (yinelemeli değil: `TIES(TIES(τg,τa),τr) ≠ TIES(τg,τa,τr)`).
- **7 hücreli kafes**: 3 tekil + 3 ikili + 1 üçlü. Tekiller **zorunlu** — τ_abstention tek başına
  ölçülmeden ikili sonucu atfedilemez ("merge çatışması" mı "kol öğrenememiş" mi ayrılamaz).
- "Kademeli" olan **ölçüm merdiveni**, birleştirme süreci değil.
- **Karşılaştırma tabanları:** tek-aşamalı karışık SFT + ardışık SFT (= taslağın orijinal kurgusu).
- ΔW bf16'da açılır, birleşim **tam ağırlık uzayında**, kuantizasyon en son, **host RAM'de ve
  akış hâlinde** (tam materyalizasyon karşıtlık noktasında host RAM'i zorlar).

### 3. İki ayrı matris — değişken kirliliğine karşı

| matris | koşul | cevapladığı soru |
| :--- | :--- | :--- |
| **İç ablasyon** | harness **KAPALI** | ağırlık uzayında beceri çatışması; merge onu koruyor mu |
| **Dış parite** | × {harness var/yok} | A/B/C/D/E; parite ve iş bölümü |

**Merge kafesi harness kapalı ölçülür.** Red kapısı açıkken abstention'ı harness sağlar ve
model-düzeyi fark maskelenir — modelin bilmediği yerde dış sistem devreye girip zayıflığı örter.

### 4. DEV / TEST ayrımı — CANON'un korunması

Merge bedava olduğu için λ / TIES density / DARE drop-rate taranacak. **Taramayı CANON'a bakarak
yapmak dondurulmuş test setini seçim için harcamaktır**; her sayı optimistik çıkar.

- `eval/canon/` (40 + 35) → **TEST**, nihai raporda **bir kez** görülür.
- Yeni üretilecek CANON-protokollü öğeler → **DEV**, seçim orada.
- `eval/genelleme/` rolü değişmez.

Bu tek iş iki ihtiyacı karşılıyor: seçim seti doğar **ve** eşdeğerlik testinin gerektirdiği n
büyümesi gelir. **ADR-0011 böylece süperseded değil, genişletilmiştir** — modlar, sabitler
(seed 3407, 900-char eval-mirror, A1 cevaplanan-only macro) aynen korunur.

### 5. Hakem: dört katmanlı savunma

Taslak tek hakem (Gemini) öneriyordu ama Gemini aynı zamanda özne. Karar: (1) omurga hakemsiz
(abstention regex + deterministik atıf doğrulama) · (2) panel yalnız M1/M4'te, üç aileden üç hakem,
κ raporlanır · (3) **aile-dışlama** · (4) self-preference'ın kendisi ölçülür.

**Zorunlu ön-adım:** red-tespit regex'i her rakip ailesinde kalibre edilir. Kalibre edilmezse
rakiplerin reddi eksik sayılır → **bizim lehimize kayar.** Bu yapılmadan hiçbir sayı raporlanmaz.

### 6. Harness ve graf — ADR-0022 **revize**

Dört bileşen: hibrit retriever · **yapısal graf (parse ile, LLM yok)** · Bedesten atıf doğrulayıcı ·
red kapısı. Substrat **NetworkX/GraphML** — gömülü, sunucu değil.

> ⚠️ **ADR-0022 revizyonu.** ADR-0022 LLM-indeksli GraphRAG'i *"KESİN DIŞARIDA"* bırakmıştı.
> Bu **kapılı bir Katman-1 koluna yumuşatıldı.** Gerekçe: ADR-0022'nin iki itirazı (air-gapped'i
> deler · non-deterministik) yeniden incelendiğinde **ayakta durmadı** — indekslenen şey kamuya
> açık mevzuat (müvekkil verisi değil) ve indeks bir kez kurulup dondurulunca sorgu anı
> deterministik. Ayakta kalan itiraz: **halüsinatif kenar hukukta mülga hükmü yürürlükteymiş gibi
> ilişkilendirir ve ucuza doğrulanamaz** (doğrulama emeği = deterministik kurma emeği).
>
> Kolun kapısı: yalnız **getirme** ölçümü (recall@k + MRR, kavram kenarı açık/kapalı) — jenerasyon
> yok, hakem yok. Getirmede iyileştirmiyorsa aşağı akışta iyileştiremez → kol kapanır ve
> **"ölçtük, katkı yok"** negatif bulgusu raporlanır. Ortak substrat sayesinde kol ucuz: LLM
> kenarları aynı grafa `provenance` etiketiyle yazılır, ablasyon tek satırlık filtre olur.

### 7. Korpus dondurma — spec §12 **düzeltmesi**

**Eval'de retriever *ve* doğrulayıcı aynı dondurulmuş snapshot'ı kullanır.**

`docs/superpowers/specs/2026-07-17-tez-cercevesi-design.md` §12'nin geçici cevabı *"eval için
dondurulmuş, doğrulayıcı için canlı"* idi. Bu **yanlış**: snapshot'ta var olup ölçüm gününe kadar
mülga olmuş bir maddeye yapılan atıf haksız yere reddedilir, ve hata zamanla büyür. Canlı Bedesten
ürün yolunda kalır.

Snapshot **sha256 ile pinlenir.** Bugünkü zemin: `data/corpus/mevzuat_maddeler.jsonl`,
40.496 madde, `sha256 51e220081801098e813cc68eeccd59ef5352571f6e3d28354e2f04a9610f6f07`.

### 8. Base: ~4B çalışma varsayımı + sert doğrulama kapısı — **ADR-0003 süperseded**

ADR-0003 base'i Gemma 4 12B ilan etmişti; ADR-0026 base'i parametreye çevirmişti. Şimdi **çalışma
varsayımı** taslağın önerdiği ~4B sınıfı instruct model. Karar değil varsayım: altı maddelik kapıdan
geçmeden hiçbir koşu başlamaz — llama.cpp mimari desteği (**ADR-0025 böylece bir base seçim kriteri
hâline geldi**) · şablon render'ının gözle doğrulanması (`research_log` #38) · turn işareti assert'i ·
Unsloth/sm_120 · kuantizasyon (QAT yoksa **Q4_K_M**; ADR-0023'ün saf-Q4_0'ı QAT'e özgüydü) · lisans.

**İki boyut noktası** — birincil ~4B (tam ızgara, çoğu **yerelde $0**) + karşıtlık ~8-9B (yalnız
kazanan konfigürasyon). **ADR-0018 böylece somutlaştı:** "tek nokta değil eğri" şartı iki noktayla
asgari düzeyde karşılanıyor ve 12B hattının kapatamadığı dış-geçerlilik açığına kısmi cevap veriyor.

### 9. Kapsam sınırları

**Ölçülmez (ürün katmanı, inşa edilebilir):** OCR · STT · Tauri app · Docker orkestrasyonu.
İddia model+harness iddiası; ayrıca OCR gürültüsü groundedness skoruna karışır, ayrıştırılamaz.

**Plandan çıkar:** dilekçe eğitim verisi (PII + lisans duvarı) · CoT kolu (veri yok + CANON'da mod
yok + tümüyle hakem-bağımlı olurdu, "hakemsiz omurga" savunmasını zayıflatır) · içtihat **kolu**
(korpus yok; ama içtihat→madde atıfı deterministik olduğu için **yapısal grafa girmeye aday**) ·
32B tier · CPT · Faz 3-5.

---

## Değerlendirilen alternatifler

| elenen | yerine | gerekçe |
| :--- | :--- | :--- |
| Kapalı-kitap sınav doğruluğu ana metrik | CANON 6-mod (dış sınav = ikincil dilim) | Parametrik ezber ölçer → "güncellik modelin beyninde değil kütüphanesinde" ilkesinin zıttı; repo bunu M5 **anti-hedefi** ilan etti |
| Ardışık FT + `merge_and_unload` | Paralel kollar + k-yollu TIES/DARE | Ardışıkta çözülecek çatışma yok; iç iddia curriculum ablasyonuna inerdi |
| Tek güçlü hakem | Dört katmanlı savunma | Hakem ailesi özneyse self-preference savunmasız; tek hakem = uyum ölçülemez |
| LightRAG çekirdek harness | Deterministik yapısal graf (LightRAG kapılı kol) | Mevzuatın yapısı zaten açık → LLM ile tahmin dominated; halüsinatif kenar ucuza doğrulanamaz |
| Neo4j sunucusu | Gömülü NetworkX/GraphML | Ayak izinin ölçüldüğü tezde konteyner saf yük; ~40K düğüm gömülü kütüphane için önemsiz |
| Retriever dondurulmuş + doğrulayıcı canlı | İkisi de dondurulmuş (eval'de) | Mülga olmuş maddeye atıf haksız reddedilir; hata zamanla büyür |
| Dört donanım tier'ı | İki boyut noktası | Eğri için 2 nokta yeter; 4 tier çekirdek çalışmayı aç bırakır |
| Rakipleri çıplak koşmak | Adalet kuralı (harness herkese) | `D > A` iddiası değersizdir |
| λ/density'yi CANON'a bakarak seçmek | DEV/TEST ayrımı | Dondurulmuş test setini seçim için harcamak = optimistik sayı |
| Hiperparametreleri sabitleyip taramamak | DEV'de tarama | "Merge çalışmıyor" ile "bu λ yanlış" ayrılamaz hâle gelirdi |
| Uçtan uca sistem tezi (OCR+STT+app dahil) | Model + harness tezi | Ölçüm yüzeyi ayrıştırılamaz hâle gelir; mühendislik yükü tez-taşımayan yere gider |

---

## Sonuçlar

- **ADR-0003 süperseded** — silinmez; base çalışma varsayımı artık ~4B sınıfı, doğrulama kapısına bağlı.
- **ADR-0011 genişletildi** (süperseded DEĞİL) — modlar ve sabitler aynı, üzerine **DEV/TEST ayrımı** eklendi.
- **ADR-0017 teyit edildi** — parite çerçevesi yürürlükte. (Base-SABİT kısmı zaten ADR-0026 ile düşmüştü.)
- **ADR-0018 somutlaştı** — eğri = iki boyut noktası.
- **ADR-0022 revize** — çok-ajanlı/LLM-indeksli graf "kesin dışarıda" değil, **kapılı Katman-1 kolu**;
  iki eski itiraz düştü, biri (halüsinatif kenar) ayakta.
- **ADR-0025 rol değiştirdi** — eval yolu kararı artık aynı zamanda bir **base seçim kriteri**.
- **spec `2026-07-17-tez-cercevesi-design.md` kısmen süperseded** — parite çerçevesi, katmanlı kapsam,
  maliyet muhasebesi ve hakem tasarımı **yürürlükte**; §12'nin korpus cevabı ve §5.3'ün graf kapsamı
  `TASARIM.md` ile güncellendi. Belge **yeniden yazılmaz**, başına durum bandı eklenir.
- **Yeni iç iddia hattı v0→v3 ile kıyaslanmaz** — o hat ardışıktı ve 12B protokolündeydi.
  Dersler taşınır, sayılar taşınmaz (ADR-0024/0026 çizgisi).
- **Açık borçlar:** DEV havuzu hedef n'i · TR embedding modeli seçimi + EDA · red kapısı eşiği ·
  zamansal eksen CANON'a girsin mi · hakem panelinin üçüncü ailesi · `$/sorgu` + latency + GPU-saat
  enstrümantasyonu (bugün yalnız `judge_cost_usd` var — *not verme* maliyeti, *servis* maliyeti değil).
