# Tez Çerçevesi — Maliyet-Normalize Parite (TASARIM)

> ### ⚠️ KISMEN SÜPERSED (2026-07-24, ADR-0027) — otorite artık [`TASARIM.md`](../../../../TASARIM.md)
>
> Bu belgenin **çekirdeği yürürlükte**: parite çerçevesi (§0-§1), katmanlı kapsam (§2), deney
> hücreleri A/B/C/D/E (§4.3), adalet kuralı (§5.2), hakem tasarımı (§6), maliyet muhasebesi (§7),
> sürüm kayması (§9), terminoloji (§13). Bunlar `TASARIM.md`'ye taşındı ve orada yaşıyor.
>
> **Güncellenen üç yer** — bu belge **yeniden yazılmaz**, çelişki burada işaretlenir:
> | § | eski | yeni (ADR-0027) |
> | :--- | :--- | :--- |
> | §3.1 | Base **Gemma 4 12B SABİT** | ADR-0026 ile base bir **parametre**; çalışma varsayımı ~4B, doğrulama kapısına bağlı |
> | §5.3 | LLM-indeksli GraphRAG **"KESİN DIŞARIDA"** | **Kapılı Katman-1 kolu** — iki itiraz (air-gapped, non-determinizm) yeniden incelenip düştü; ayakta kalan itiraz halüsinatif kenar |
> | §12 s.1 | *"eval için dondurulmuş, doğrulayıcı için canlı"* | **İkisi de dondurulmuş** — aksi hâlde mülga olmuş maddeye atıf haksız reddedilir |
>
> Ayrıca §8'in adım sırası ve v4 kapıları **12B hattına** aitti; yeni hattın kapıları
> `TASARIM.md` §7'de (Kapı 0-4).

> **Durum:** Kısmen süperseded (→ ADR-0027) · çekirdek çerçeve yürürlükte
> **Tarih:** 2026-07-17 · **Revizyon: 2026-07-23** (ADR-0021/0022/0023) · **2026-07-24** (ADR-0027)
> **Kapsam:** Projenin Master tezi çıktısına göre yeniden çerçevelenmesi
> **Sonraki adım:** `VISION.md` + `PAPER_TARGET.md` + `TEKNIK_PLAN.md` + `CLAUDE.md` revizyonu bu spec'ten türetilir
>
> ### 2026-07-23 revizyon özeti (bu spec'te ne değişti)
> | § | Değişiklik | Otorite |
> | :--- | :--- | :--- |
> | §3.1 | Base teyidi **ölçümle** güçlendi (8 GB'da 176K vs 91K bağlam tavanı); "18× KV" iddiam çürütüldü (gerçek 2.5–3.7×) | ADR-0021 |
> | §3.3 | ⚠️ "Darboğaz KV-cache" tezi **yanlış çıktı** (KV = ağırlığın %18'i); TurboQuant = bağlam tavanı kaldıracı | ADR-0021/0023 |
> | §5 | Harness 3 → **4 bileşen** (yapısal graf eklendi); harness **GPU'ya girmez** | ADR-0022/0023 |
> | §5.3 | ⚠️ "Graph-RAG tez dışı" **daraltıldı**: (a) yapısal içeride, (b) çok-ajanlı dışarıda | ADR-0022 |
> | §7.4 | VRAM ölçümü kısmen kapandı (`kv_cache_compare.py`) | ADR-0023 |
> | §11 | 2 yeni risk: **eval ≠ dağıtım**, VRAM tahminleri ölçülmedi | ADR-0023 |
> | §12 | Yeni açık soru: **zamansal eksen** (mülga/değişik) CANON'a girsin mi | ADR-0022 |

---

## 0. Özet

Proje bugüne kadar **içeri dönük** bir soruyu cevaplıyordu: *"Bizim ince-ayarımız kendi base'imizi geçiyor mu?"*
Tez, soruyu **dışarı dönük** hale getiriyor:

> **Dar ve yüksek-riskli bir domainde (Türk hukuku), tüketici donanımında sıfır marjinal maliyetle
> çalışan bir SLM+harness sistemi, kapalı ticari modellerin dağıtım sınıfına maliyet-normalize
> paritede ne kadar yaklaşır — ve bu yaklaşmanın ne kadarını ince-ayar, ne kadarını harness sağlar?**

Mevcut v0→v3 serisi bu tezin **proof-of-concept**'i olarak konumlanır; çöpe gitmez, tezin
ince-ayar (FT) kolunu oluşturur.

**Ana iddia (tek cümle):** *Bu maliyetle, buraya kadar çıkıyoruz.*

---

## 1. Ne değişti

| | Eski çerçeve | Yeni çerçeve |
| :--- | :--- | :--- |
| Soru | FT base'i geçiyor mu? | Sistem, kapalı rakiplerin dağıtım sınıfına maliyet-normalize paritede mi? |
| Birincil katkı | 6-mod CANON benchmark | **Parite + iş bölümü**; benchmark = altyapı (bkz. §1.1) |
| Kıyas | base, v2b, v2c, v3, Mecellem | + Gemini 3 Flash, Claude Sonnet, GPT-5-mini (+ tavan referansı) |
| Ölçülen eksen | kalite (6-mod) | kalite **× maliyet** (iki boyutlu Pareto) |
| Faz sırası | Faz 1 bitmeden Faz 2 yok | Tez Faz 1 + Faz 2'nin gerekli dilimini kapsar (bkz. §10) |
| Erişilebilirlik | ~8 GB sert kısıt | **Parametrik**: "tüketici donanımı, tek GPU" — 8 GB en agresif nokta |

### 1.1 Benchmark neden birincil katkı olmaktan çıkıp altyapı oluyor

Parite iddiası bir **eşdeğerlik** iddiasıdır (D ≈ B), fark iddiası değil. Eşdeğerlik testi (TOST)
fark testinden daha çok örnek ister. Mevcut n (core_hard 40, trap 35, E-set 40) bunu taşımaz —
repo bunu zaten biliyor: `scripts/bench_scorecard.py:25` *"n=40/35 PİLOT → underpowered … paper-cetveli n=100/75"*.

Sonuç: **benchmark'ı büyütmek tezin opsiyonu değil, parite iddiasının ön koşulu.** Benchmark
katkısı böylece bedava gelir — ama iddianın kendisi değil, taşıyıcısı olur.

---

## 2. Katmanlı kapsam

> **Kural (pazarlıksız):** Her katman tek başına savunulabilir bir tez.
> Üst katmanlar **bölüm ekler**, alt katmanı **kurtarmaz**.
> Bütçe ve takvim hiçbir noktada HPC tahsisine bağlı olmaz.

### Katman 0 — HPC'siz çekirdek (~birkaç yüz $; tek başına tam bir tez)

0. Benchmark'ı n=100/75'e büyüt (bir defalık; §1.1) + sağlayıcı soyutlaması + regex kalibrasyonu
1. **Rakip baseline** (harness'sız) + **maliyet enstrümantasyonu** — *aynı* koşuda
2. **Harness** (retriever + atıf doğrulayıcı + red kapısı) — 1 ile paralel
3. **Parite matrisi** — A/B/C/D **+ E** + eşdeğerlik (TOST, hesap)
4. **v4** — *sadece kapılar izin verirse* (§8)

**Çıktı:** tek base üzerinde tam maliyet-normalize parite çalışması.

### Katman 1 — Bütçe genişlerse (HPC yok)

- Eşdeğerlik testi için yeterli güç (TOST)
- Harness varyant ablasyonu (retriever'sız / doğrulayıcısız / kapısız → hangi parça ne taşıyor)
- **Gürültülü-retrieval eval modu** → RAFT'ın gerçek değeri burada görünür (§3.2)

### Katman 2 — MN5 tahsisi gelirse (bonus bölümler)

- **Büyük-n benchmark:** benchmark katkısını yayımlanabilir ölçeğe taşı
- **Model-boyut eğrisi:** aile içi (E4B / 12B / 26B) → maliyet-kalite eğrisinin ölçülmüş hali

**Katman 2'nin hiçbir maddesi Katman 0'daki bir eksiği kapatmaz.** MN5 reddedilirse tez aynen
savunulur, "gelecek çalışma" bölümü uzar.

### Non-goal'lar (HPC gelse bile yapılmayacaklar)

| Yapılmayacak | Neden |
| :--- | :--- |
| **CPT (continued pre-training)** | HPC gelince yapılacak en cazip şey — ve kapsamı patlatacak şey. Tez FT + harness üzerine; CPT ayrı bir tez. **Tahsis gelse bile hayır.** |
| **Çok-base replikasyon** (Qwen vb.) | 2026-07-17'de kapsam dışı bırakıldı. Sonucu: dış geçerlilik **kalıcı sınır** (§11). |
| **Graph-RAG** | §5.3 |

**İlke:** Tez HPC'siz tamamlanabilir olmalı. HPC bir yükselteç; ona göre plan yapılmaz.

---

## 3. Base model kararı

### 3.1 Karar: **Gemma 4 12B birincil kalır** *(teyit: 2026-07-17 · **ölçümle yeniden teyit: 2026-07-23, ADR-0021**)*

> ⚠️ **2026-07-23 güncellemesi.** Karar sunk-cost sıfırlanarak yeniden açıldı ve **değişmedi** —
> ama gerekçeler ölçüldü, biri de düzeltildi. Sayı kaynağı: `scripts/kv_cache_compare.py`.
>
> **Eklenen (en güçlü ikinci kalem): 8 GB'da bağlam tavanı.** Aynı kartta kullanıcının
> yapıştırabileceği en uzun metin **176.128 tok (Gemma) vs 90.982 tok (Qwen3.5 9B)** — ~1.9×,
> kabaca 110 bin vs 57 bin kelime. Bandı biz değil kullanıcı seçer → kuyruğa tasarlanır.
> Asimetri: Gemma'da hata bedeli ~1 GB boşuna ağırlık; Qwen'de 128K'da 9.22 GB → ürün çalışmıyor.
>
> **Düzeltilen:** aşağıdaki §3.3'ün "darboğaz KV-cache" tezi bu base için **yanlış** (128K'da
> KV = ağırlığın %18'i). Ayrıca ilk sözlü "18× KV avantajı" iddiası **çürütüldü** — o Qwen**3**'ün
> hibrit-öncesi mimarisiydi; Qwen3.5 24/32 katmanı Gated DeltaNet'e çevirmiş, gerçek fark **2.5–3.7×**.
>
> **Qwen'in dürüstçe kabul edilen üstünlükleri:** saf Apache-2.0 (bizde Apache-2.0 **+ Prohibited
> Use Policy**) ve <64K bağlamda daha hafif oluş. İkisi de kararı çevirmedi.

`google/gemma-4-12B-it-qat-q4_0-unquantized` (Apache-2.0). Gerekçeler:

1. **QAT, maliyet iddiasının dayanağı.** Tezin tamamı şu zincire yaslanıyor:
   *12B eğit → Q4_0 → ~6.5 GB → tüketici GPU → maliyet ~0.* O zincirin en kırılgan halkası
   quantization kaybı. Gemma, Q4_0 için **quantization-aware-trained** resmî checkpoint sunuyor →
   halka garanti altında. QAT'siz bir base (ör. Qwen3.5-9B) Q4_0'a kendi elimizle indirilir,
   bilinmeyen kalite kaybı **doğrudan tezin kalite ekseninden** düşer. Ucuz uçta iyi olduğumuzu
   iddia ederken, ucuz uçta kalite kaybettiren bir base seçmek iddianın altını oyar.
2. **E-vs-D ablasyonu FT hattını gerektiriyor** (v2b RAFT → v3 ORPO → v4) — o hat Gemma'da.
3. **Sunk cost:** 5 eğitim koşusu + ~35 judge hücresi Gemma'ya çapalı (`docs/record/SCORECARD.md:10`
   ortak protokol). v4 = "v2b-continuation ORPO" olarak kilitli (`docs/record/v4/recipe.md:41`).
4. Türkçe'de Gemma ailesi küçük Qwen'lerden daha istikrarlı raporlanıyor.

### 3.2 RAFT'ın (v2b) yeni tezdeki yeri — değeri **artıyor**

RAFT'ın öğrettiği tek beceri: *distractor'lar arasından doğruya sadık kal.* Bugüne kadar
**oracle-context** altında ölçüldü — o rejimde gereksiz görünüyor (base M4 = 0.978, kanılacak
bir şey yok). Gerçek retriever devreye girince rejim değişir: **top-k getirme = k-1 distractor.**
Yani RAFT'ın eğittiği beceri, Faz 2'nin tam olarak ihtiyaç duyduğu beceri.

Kanıt çizgisi: M1 (distractor-altında sadakat) 0.662 (base) → 0.737 (v2b) → 0.881 (v3).

**Ölçülebilir hipotez (Katman 1):** *RAFT'ın katkısı oracle-context'te küçük, gürültülü retrieval
altında büyük.* Bu, `E ≈ D` tehdidine karşı en güçlü savunma. Çıkmazsa paper-değerinde negatif bulgu.

### 3.3 VRAM darboğazı: base değil, KV-cache — ⚠️ **DÜZELTİLDİ (2026-07-23)**

> **Bu bölümün tezi bu base için yanlış çıktı.** 128K bağlamda KV = **1.16 GB**, Q4_0 ağırlık
> ≈ **6.5 GB** → KV, ağırlığın yalnız **%18'i**. Darboğaz **ağırlık**. Sebep mimari: 48 katmanın
> 40'ı `sliding_attention` (win=1024, bağlamla büyümüyor), büyüyen 8 `full_attention` katmanı
> 1 KV head × 512 dim, ve `attention_k_eq_v=True` cache'i bir daha yarıya indiriyor.
>
> **TurboQuant'ın rolü değişti:** bellek-darboğazı çözücü değil, **bağlam tavanı kaldıracı**
> (8 GB'da bf16 → 64.755 tok; q8_0 → 149.990; q4_0 → 320.461; ~3 bit → 434.108). Ayrıca
> **llama.cpp'de yok** → bugünkü kaldıraç `--cache-type-k/-v q8_0`; TurboQuant sonraya (ADR-0023).
> "Base değiştirmenin verdiğinden fazlasını bedavaya verir" argümanı da gereksizleşti: base kıyası
> KV üzerinden değil, **8 GB'da bağlam tavanı** üzerinden kazanıldı (§3.1).

Düşük-spec derdinin doğru kolu base değiştirmek değil. Asıl darboğaz uzun RAG bağlamının
KV-cache'i, ve kayıtlı çözümü var: `knowledge/summary_turboquant.md` — KV-cache'i 2.5–3.5 bit'e
sıkıştırır, **eğitim gerektirmez**, online çalışır, Llama-3.1-8B'de 4.5× sıkıştırmada
full-precision performansı korur, **ağırlığa dokunmaz.**

Boyut sorusu bir karar değil **ölçüm**: aile içi eğri (E4B / 12B / 26B) — aile, tokenizer,
QAT hattı, eğitim kodu sabit kalır. E4B zaten kayıtlı ama hiç koşulmamış aday
(`docs/VISION.md:35`, `docs/FINE_TUNING.md:221`).

### 3.4 8 GB: sert kısıt değil, **soft gate**

`CLAUDE.md`'nin "~8 GB VRAM" ifadesi bugün sert kısıt gibi okunuyor. Doğrusu: **≤8 GB tercihimiz,
soft gate.** Aşmak yasaklı değil — ama bedeli var ve o bedel **ölçülür**, gizlenmez.

- **Varsayılan hedef:** ≤8 GB, tek GPU, tüketici donanımı. Bir yapılandırma bunu tutuyorsa
  "tercih bölgesinde" sayılır.
- **Aşan yapılandırmalar da raporlanır** (12/16/24 GB), ama erişilebilirlik ekseninde kayıpla.
  Tek nokta yerine **maliyet-performans eğrisi** sunulur; 8 GB o eğri üzerinde **işaretli bir
  tercih bandı**, eğrinin sonu değil.
- Boyut/bellek sorusu bir karar değil **ölçüm** (§3.3).

---

## 4. Deney matrisi

### 4.1 Anlatı: Biz vs Rakipler

| | Modeller | Özellik |
| :--- | :--- | :--- |
| **Biz** | Gemma 4 12B → v2b → v3 → v4 (× harness) | yerel · açık · sorgu başına ~$0 · veri dışarı çıkmıyor |
| **Rakipler** | Gemini 3 Flash · Claude Sonnet · GPT-5-mini | kapalı · API · sorgu başına ücretli · veri dışarı çıkıyor |

Rakipler modern frontier'ın **dağıtım sınıfı** — ölçekte gerçekten koşulan modeller (kimse her
sorguya Opus ödemiyor). Hem gerçekçi hem bizim köşemize en yakın.

**Terminoloji kuralı:** paper'da bunlara "frontier" **denmez**, **maliyet bandı** denir.
Böylece "hangisi frontier" tartışması hiç açılmaz.

### 4.2 Yardımcı roller

| Rol | Modeller | Neden |
| :--- | :--- | :--- |
| **Tavan referansı** | Gemini 3.5 Pro, Claude Opus | Rakip değil, grafikte **tek referans çizgisi**. Maliyeti ~$3. Kapattığı delik: *"neden en güçlüsüyle kıyaslamadınız?"* — ölçülmezse savunmada açık kalır. Parite iddia **edilmez**. |
| **İlgili çalışma** | Mecellem (`newmindai/Mecellem-Qwen3-4B-TR`) | *"Ucuz uç kendiliğinden iyi değil"*in kanıtı: register 0.20, M4 0.783, M5 0.350. **Yeni koşu yok, tek kuruş harcanmaz.** ADR-0016'nın cite-only konumu geçerli. |

**Mecellem'i "geçtim" iddiası kurulmaz.** CPT foundation base o, asistan değil — kategori farkı.
İnce-ayarlı asistanın foundation base'i register'da geçmesi beklenen şeydir; iddia olarak korkuluk dövmek olur.

**Rakip seti = kapalı ticari lablar.** Açık modeller özne değil (Gemma base + Mecellem zaten
"açık modeli yerelde koşsak yetmez mi" sorusunu cevaplıyor). "Ucuz alternatif" boşluğunu GPT-5-mini dolduruyor.

### 4.3 Hücreler

Her özne × {harness yok, harness var} × 6-mod CANON:

| | harness yok | harness var |
| :--- | :---: | :---: |
| **Rakipler** | A | **B** |
| **Bizim FT** | C | **D** |
| **Gemma base** | (mevcut) | **E** ← *tezin ana ablasyonu* |

- **İddia `D > A` ise değersizdir** — harness'ı sadece kendimize verip rakibi çıplak koşmak.
- **İddia `D ≈ B` ise tez vardır** — asıl rakip **rakip + aynı harness**.
- **`E` hücresi kaderi belirler:** `E ≈ D` → ince-ayar dekorasyon; `D > E` → iş bölümü doğrulandı.

---

## 5. Harness mimarisi

> ⚠️ **GÜNCELLENDİ (2026-07-23, ADR-0022):** bileşen sayısı 3 → **4**. Yapısal/deterministik graf
> eklendi; §5.3'ün eski "graph-RAG tez dışı" ifadesi daraltıldı (aşağı bkz.).
> ⚠️ **VRAM kısıtı (ADR-0023):** harness **GPU'ya girmez** — embedder CPU'da, graf + vektör indeksi
> CPU RAM/disk'te. 8 GB'da embedder'ı GPU'ya koymak yığını açtırmıyor; bu bir tasarım kısıtı.

Dört bağımsız bileşen; her biri ayrı test edilebilir, ayrı ablasyon edilebilir.

| # | Bileşen | Arayüz | Not |
| :--- | :--- | :--- | :--- |
| 1 | **Retriever** | `soru → top-k madde` | Hibrit (BM25 + TR embedding). `raft_pack.py`'nin bugün *simüle* ettiği şeyin gerçeği. Kayıtlı borç: `raft_pack.py:13` *"Gerçek RAG retriever kurulunca (Adım 0) dağılımı onunla kalibre et."* **CPU'da koşar** (ADR-0023). |
| 1b | **Yapısal graf** *(YENİ, ADR-0022)* | `madde → {hiyerarşi, atıf-komşuları, sürüm-zinciri}` | Deterministik: kanun→madde→fıkra hiyerarşisi + atıf ağı + **mülga/değişik zamansal zincirleri**. Getirmede 1-2 hop genişletme. LLM yok → marjinal ~0 maliyet. Ön-çalışma: SAT-Graph RAG (Work/Expression), Citation Grounding. |
| 2 | **Atıf doğrulayıcı** | `cevap → her atıf için {VAR, YOK, METİN_UYUŞMUYOR}` | Kanun+madde atıflarını çıkar, **Bedesten API**'ye karşı doğrula. Kontrat: `docs/BEDESTEN_API.md`, probe: `scripts/bedesten_probe.py`. **Zamansal boyut adayı:** *"atıf yapılan tarihte yürürlükte miydi?"* (Citation Grounding'in 3. ekseni — bizde henüz yok). |
| 3 | **Red kapısı** | `doğrulama düşerse → cevabı redde çevir` | Modelin sahip olmadığı abstention'ı harness'ın **satın aldığı** yer. |

### 5.1 Kritik özellik: 1b, 2 ve 3 **deterministik**

LLM çağırmıyorlar. Sonuçları:

- **Bedava** — çıkarım maliyeti yok, $/sorgu iddiasını bozmuyor
- **Tekrarlanabilir** — hakem varyansı yok
- **Kapalı API'nin satın alamayacağı şey** — halüsine atıfı *olasılıkla değil kesinlikle* yakalar
- Hukukta doğrudan mahremiyet+maliyet argümanını besler

### 5.2 Adalet kuralı (pazarlıksız)

**Harness tüm öznelere birebir aynı uygulanır.** Aynı retriever, aynı doğrulayıcı, aynı kapı,
aynı eşikler. Harness'ı sadece kendi modelimize verirsek tez ölür.

### 5.3 Kapsam sınırı — **REVİZE (2026-07-23, ADR-0022)**

> ⚠️ Eski ifade: *"Graph-RAG tez dışı (future work). Parite iddiasına sıfır katkı yapıyor…"*
> Bu **fazla genişti** — "graph-RAG" adı altında iki farklı iş var ve ayrılmaları gerekiyordu.

- ✅ **(a) Yapısal / deterministik graf → TEZE DAHİL** (§5 tablo, bileşen 1b). Korpusun kendi
  yapısından çıkar (hiyerarşi + atıf ağı + zamansal zincirler), indekslemede **LLM yok**,
  marjinal maliyet ~0, determinizmi (§5.1) korur. Zaten bileşen 2'nin (atıf doğrulayıcı) ihtiyaç
  duyduğu yapı — onu getirmede de kullanmak.
- ❌ **(b) Çok-ajanlı / LLM-indeksli GraphRAG → KESİN DIŞARIDA.** Sorgu başına ~3× çıkarım →
  **doğrudan maliyet-normalize parite metriğinden düşer**; üstelik adalet kuralı (§5.2) gereği
  rakiplere de aynı harness verileceği için maliyet iki taraflı katlanır. Referans: LegalGraphRAG
  (%6.3–19.1 kazanç raporluyor, **maliyet/gecikme yükünü hiç raporlamıyor**).
- ❌ **OCR / belge ingestion → harness dışı.** Faz 3 app katmanı; harness metin *alır*. Ölçüme
  sokulursa groundedness skorları OCR gürültüsüyle karışır (ayrıştırılamaz).
- ❌ **Faz 3** (agents, app, serving) — kapsam dışı (değişmedi).

Eski "Katkı 3" (vanilla-vs-graph-RAG karşılaştırması) tez sonrasına atılır; ama **(a) sayesinde
ucuz bir ablasyon açılıyor:** *yapı-farkındalıklı getirme işe yarıyor mu?* (vektör vs vektör+graf).

---

## 6. Hakem tasarımı — self-preference savunması

**Eldeki altyapı (sıfırdan değil, genişletme):** `scripts/judge_agreement.py` cross-judge κ
(Cohen kappa + Pearson) ve yazar spot-check'i zaten yapıyor. `score_abstention.py:40-51`'de
hakemsiz `rejection_exact` var. 59 summary birikmiş. Aşağıdaki dört katman bu altyapının
**üstüne** kurulur; mevcut hiçbir şey çöpe gitmez.

**Problem:** OpenAI ailesi hem hakem (gpt-4o-mini) hem özne (GPT-5-mini). Üç büyük aileyi özne
yaparsan tarafsız hakem ailesi kalmaz. `bench_scorecard.py:24` bunu zaten not etmiş:
*"cross-judge CROSS-FAMILY olmalı (Claude/Gemini) — gpt-4o aynı-aile, self-preference'ı gidermez (Wataoka)."*

**Dört katmanlı savunma:**

1. **Omurgayı hakemsiz kur.** `rejection_exact` (regex, `score_abstention.py:40-51`, zaten var)
   + atıf doğrulama (deterministik). Tezin iddia yüzeyinin çoğu — abstention ve atıf —
   **hiç hakem görmez.** En güçlü savunma.
2. **Hakem paneli.** Sadece yargı gerektiren eksenlerde (M1/M4 groundedness): üç aileden üç hakem,
   uyum raporlanır (`judge_agreement.py` var). Hakem ailesi değişince sonuç değişmiyorsa → sağlam.
3. **Aile-dışlama.** F ailesinden bir özneyi F ailesinin hakemi puanlamaz. 3 hakem × 3 aile ile
   her özne 2 tarafsız hakem alır.
4. **Self-preference'ı ölç.** Aynı özneyi kendi ailesinin hakemi ile diğerlerinin puanladığı farkı
   raporla. Sınır değil, **küçük bir bulgu** — Wataoka notunu ölçülmüş hale getirir.

### 6.1 Zorunlu ön-adım: regex kalibrasyonu

`rejection_exact`'in regex'i Türkçe red kalıplarına göre yazılmış, muhtemelen **Gemma çıktılarına
bakılarak** (`düzenlemiyor`, `yer almıyor`, `kapsamıyor`, `bilgi yok`, `mevcut değil`,
`bir avukata danış`). GPT'nin *"cevap veremem"* / *"yanıtlayamam"* kalıbı **listede yok**.

Kalibre edilmemiş regex rakiplerin reddini eksik sayar → skorlarını düşürür → **bizim lehimize kayar.**
Hakemin bulmayı en sevdiği hata türü: ölçüm aracının kendi modeline göre kalibre edilmiş olması.

**Kural:** Adım 0'ın ön-adımı olarak her rakip ailesinin çıktısında regex recall'ı ölçülür,
kalıplar model-agnostik hale getirilir, ~30 çıktı elle spot-check edilir (projenin standart protokolü).
**Bu yapılmadan hiçbir sayı raporlanmaz.**

---

## 7. Maliyet muhasebesi

### 7.1 İki maliyet karıştırılmaz

| | Ne | MN5 etkisi |
| :--- | :--- | :--- |
| **Araştırma maliyeti** | Eğitim koşuları, deney matrisi — bilimi *yapmanın* maliyeti | ~0'a iner |
| **Dağıtım maliyeti** | Sorgu başına çıkarım — sistemi *çalıştırmanın* maliyeti | **Hiç değişmez** |

**Tezin iddiası ikincisi hakkındadır.** MN5 alınsa da alınmasa da dağıtım maliyeti aynı — model
yine tüketici GPU'sunda, yine elektrik parasına çalışır.

### 7.2 HPC sübvansiyonu iddiadan **izole edilir** (pazarlıksız)

MN5 tahsisi alınırsa, başabaş hesabında eğitim maliyetini **$0 yazma cazibesi** doğar. Bu savunulamaz:
çalışmayı tekrarlayacak bir hukuk bürosu MN5 tahsisi almıyor, A100 saatini piyasa fiyatından kiralıyor.
Sübvanse maliyet raporlanırsa **başabaş sayısı kimsenin kullanamayacağı bir kurgu** olur —
ve tekrarlanabilirlik bu projenin ana varlığı.

**Kural:** compute **GPU-saat** olarak raporlanır, **piyasa fiyatından** fiyatlandırılır.
MN5, maliyet iddiasını ne güçlendirir ne zayıflatır.

### 7.3 Ana metrik: başabaş noktası

Maliyet tek sayı değil **eğri** olarak kurulur:

- **Bizim:** `$/sorgu = eğitim_maliyeti / N + ~0` (N büyüdükçe düşen eğri)
- **Rakip:** sabit `$/sorgu`, sonsuza kadar düz çizgi

İki eğri kesişir → **başabaş sorgu sayısı N\***:

> *"~N\* sorgudan sonra bizim sistem <rakip>'ten ucuz — ve kalite kıyaslanabilir."*

Jürinin aklında kalacak türden somut bir sayı; "sıfır maliyet" gibi tartışmaya açık bir ifadeden
çok daha savunulabilir. Bir hukuk bürosu senaryosuyla somutlaştırılır (günde X sorgu → Y ayda başabaş).

### 7.4 Ölçülecekler *(2026-07-23: VRAM kısmen kapandı)*

`$/sorgu`, latency, throughput, VRAM, GPU-saat. Mevcut tek maliyet ölçümü `judge_cost_usd` —
yani *not verme* maliyeti, *servis* maliyeti değil (`eval.py:210`, `groundedness.py:273`,
`score_correctness.py:181`, `score_abstention.py:126`).

**Durum güncellemesi:**
- ✅ **VRAM / bellek modeli** → `scripts/kv_cache_compare.py` (ağırlık + KV + runtime, retriever
  yerleşimine göre; sığdırma merdiveni + bağlam tavanı). ADR-0023 hedef config: **6.97 GB sabit,
  ~250K bağlam.** ⚠️ İçindeki CUDA-bağlamı ve compute-buffer kalemleri hâlâ **tahmin** — gerçek
  RTX 5070 + gerçek GGUF ölçümü açık borç.
- ❌ `$/sorgu`, latency, throughput, GPU-saat → hâlâ yok.

### 7.5 Pareto sunumu

```
kalite ↑
       │   Biz ●                        ○ tavan referansı (Opus / 3.5 Pro)
       │   (hedef köşe)          ● Sonnet  ● Gemini 3 Flash
       │              ● GPT-5-mini
       │  ● Mecellem
       │   (domine edilmiş)
       └────────────────────────────────────→ maliyet (log $/sorgu)
```

Katmanlar doğrudan x eksenidir — her katman bir maliyet bandı, grafik doğal kümelere ayrılır.
Bu, danışmanın **çok-kriterli karar verme** uzmanlığına birebir konuşur (Pareto-dominans analizi).

---

## 8. Sıra ve kapılar

> **Kapı eşikleri veriyi görmeden, ŞİMDİ yazılır.** Sonradan yazılırsa çıkan sonuç rasyonalize edilir.
> Proje pre-registration'ı zaten biliyor (V2_PLAN öyleydi) ve "para-kapısı" kültürü var (ADR-0015).

### 8.1 Sıra

**n baştan büyük kurulur.** Benchmark'ı n=100/75'e büyütmek (§1.1) Adım 0'ın *ön-adımı* — bir
defalık, sadece yeni soru üretimi. Böylece her ölçüm (rakip baseline, parite matrisi, v4) zaten
büyük-n koşulur; küçük-n koşup sonra tekrarlamak (= iki kez ödemek) yok. **n bir "adım 5" değil,
protokol parametresi.**

**TOST bir eğitim değil.** Eşdeğerlik testi, veri toplandıktan sonra yapılan **bedava hesaptır**
(analiz, API çağrısı yok). Ayrı bütçe kalemi değil.

| # | Adım | Maliyet | GPU |
| :--- | :--- | :--- | :--- |
| **0a** | Benchmark'ı n=100/75'e büyüt (bir defalık soru üretimi) | ~$5 | Hayır |
| **0b** | Sağlayıcı soyutlaması (OpenRouter) + **regex kalibrasyonu** | $0 | Hayır |
| **0c** | **Rakip baseline** (harness'sız) + **maliyet enstrümantasyonu** *aynı koşuda* | inf. + hakem | Hayır |
| **1** | **Harness inşası** (retriever + doğrulayıcı + kapı) — 0 ile paralel | $0 | Hayır |
| **2** | **Parite matrisi** — tüm özneler × {harness var/yok} → A/B/C/D/E + **TOST** (hesap) | inf. + hakem | Yerel |
| **3** | **v4** — *sadece Kapı 1 ∧ Kapı 2 izin verirse* | $15-40 | Modal |
| **K2** | Katman 2 (büyük-n zaten var → aile içi boyut eğrisi) — *tahsis gelirse* | HPC | MN5 |

**Maliyet iki kalem** (eski ~$30/~$100 tek-sayıları yanıltıcıydı):
- **Hakem:** gpt-4o-mini çok ucuz (~$0.15/1M in). Asıl hakem gideri **cross-family** (Claude/Gemini
  hakem, §6). Tüm matris için kaba tavan: onlarca dolar mertebesi, yüzlerce değil.
- **Rakip inference:** OpenRouter üzerinden (Gemini 3 Flash / Sonnet / GPT-5-mini + tavan referansı).
  n=115 × ~7 özne × {harness yok/var} × 9 kulvar → dağıtım-sınıfı modeller ucuz; tavan referansı
  (Opus/3.5 Pro) pahalı ama **tek referans çizgisi** olduğu için az çağrı.
- **Bizim inference:** yerel RTX 5070, $0.

> **Not:** rakip modelleri koşma (baseline inference) işi zaten **OpenRouter'a** yaptırılıyor —
> tek anahtar, `base_url` değişikliği, mevcut `OpenAI()` client'ı API-uyumlu. Ayrı entegrasyon yok.

### 8.2 KAPI 1 — rakip baseline sonrası

**Ölçülen:** **en iyi rakibin** M2'si (near-miss red) + ood dilimi.
*Neden en iyi rakip (ortalama değil):* soru "boşluk var mı" — herhangi bir rakip çözüyorsa problem
çözülebilirdir ve bizim "boşluk" hikâyemiz zayıflar. En iddialı (kendimize karşı en sert) istatistik bu.
**Referans:** base Gemma M2 = 0.704 · v3 = 0.593 · base ood = 0.889 · v3 ood = 0.483

| Sonuç | Karar |
| :--- | :--- |
| **maks(rakip M2) ≥ 0.90** | Rakipler bu işi çözmüş. "Abstention'da yetişiyoruz" hikâyesi ölür → tez **maliyet + mahremiyet** eksenine yaslanır; v4 opsiyonel. |
| **maks(rakip M2) ≤ 0.80** | Boşluk gerçek → v4 gerekçeli, tez güçlü. |
| **0.80 – 0.90** | Gri bölge → ood dilimiyle karar. |

### 8.3 KAPI 2 — harness ablasyonu sonrası

**Karşılaştırılan:** **D** (v3+harness) vs **E** (base+harness).

| Sonuç | Karar |
| :--- | :--- |
| **D ≈ E** | İnce-ayar harness'ın üstüne bir şey eklemiyor. **Kötü haber değil, bulgu:** *"bu domainde scaffolding ince-ayarı ikame ediyor"* — yayımlanabilir, dürüstçe raporlanır. |
| **D > E** | İş bölümü doğrulandı; tezin omurgası ayakta. |

### 8.4 KAPI 3 — v4 git/gitme

v4 **sadece** Kapı 1 = "boşluk gerçek" **∧** Kapı 2 = "FT değer katıyor" ise koşar.
Aksi halde koşulmaz — o durumda tez zaten Adım 3 sonunda tam (parite + iş bölümü ölçülmüş),
harcanacak ek para yok.

**Kazanç:** v4 artık iki ölçümle korunuyor. Bugün koşulursa hedefinin gerçek olup olmadığı
bilinmeden $15-40 harcanır. Kapılardan sonra ya gerekçeli koşulur ya hiç koşulmaz.
(v4'ün *reçetesi* birden çok tur içerebilir — gold-absent sweep 0.3/0.4/0.5, `recipe.md:20`;
"tak diye tek koşu" değil. Kapı, o çok-turlu reçeteyi başlatıp başlatmamaya karar verir.)

**Not:** v4 tasarımı KİLİTLİ (`docs/record/v4/recipe.md:1`), reçete değişmiyor — sadece
**sırası** ve **koşulup koşulmayacağı** değişiyor.

### 8.5 HPC başvurusu

Katman 2 **çekirdek (Adım 0-3) bittikten sonra** ve tahsis gelirse. Başvuru **çekirdek sonuçları
elde varken** yapılır — çok daha güçlü: *"işte pilot bulgularımız, ölçeklemek için şu kadar H100-saat."*

Gerekçe formülasyonu: **"eşdeğerlik iddiası için istatistiksel güç gerekiyor"** (düzgün),
"para biriktirmek için lazım" (zayıf) değil.

Kanal: **TÜBİTAK ULAKBİM ulusal erişim çağrısı** (MareNostrum 5 pilot access) — Türk araştırmacılar
EuroHPC JU genel çağrılarına girmek zorunda değil.
⚠️ MN5 **ACC partition'ı (H100) yoğun talep nedeniyle Development Access'e kapalı** — GPU tarafı
en çekişmeli kısım. Çağrı koşulları dönemsel değişir, başvuru öncesi ULAKBİM sayfasından teyit edilir.

---

## 9. Sürüm kayması

Rakipler hareketli hedef; tezin rampası ≥2 yıl. **Zorunluluk (ilk günden):**

**Tarihli snapshot'lara pinle** — `gpt-4o-2024-11-20` gibi, jenerik `gpt-4o` değil.
Ölçüm tarihi her summary'ye yazılır. Bu yapılmazsa hiçbir sayı tekrarlanabilir olmaz.

**Yeniden ölçüm turu takvime bağlanmıyor** (karar: 2026-07-17). Teslime ≥2 yıl var; şimdiden tarih
koymak anlamsız. Pinleme + tarih kaydı yapıldığı sürece, yeniden ölçüm zamanı gelince ucuz bir
tekrar koşusudur (~$30). Karar o zaman verilir.

---

## 10. Mevcut dokümanlarla çelişkiler (onay sonrası düzeltilecek)

`CLAUDE.md`'nin sert kuralı: *"Bir karar eski bir dokümanla çelişiyorsa, sessizce üzerine yazmak
yerine çelişkiyi her iki yerde işaretle."* Tespit edilenler:

| # | Doküman | Çelişki | Aksiyon |
| :--- | :--- | :--- | :--- |
| 1 | `CLAUDE.md` (Faz sırası) | *"Faz 1 bitmeden Faz 2'ye (RAG/Graph) atlama"* — yeni tez tam bunu yapıyor; harness olmadan parite iddiası kurulamaz | Kural tez lehine esnetilir: **tez Faz 1 + Faz 2'nin retriever/doğrulayıcı dilimini kapsar; graph-RAG hariç** |
| 2 | `CLAUDE.md` (~8 GB) | Sert kısıt gibi yazılmış | **Parametrik** hale getirilir (§3.4) |
| 3 | `docs/VISION.md` | Birincil katkı = benchmark | Birincil katkı = **parite + iş bölümü**; benchmark = altyapı (§1.1) |
| 4 | `docs/TEKNIK_PLAN.md:192` | ADR-0003'ün gerekçe listesinde **olmayan** "multimodal (gelecek fazlar)" maddesini gerekçeye eklemiş — **gerekçe kayması** | ADR-0003'e hizalanır + her iki yere çelişki notu |
| 5 | `docs/VISION.md:35` | Aynı kayma (multimodal'ı seçim gerekçesine yaklaştırıyor) | Aynı |
| 6 | OCR/multimodal iddiaları (`CLAUDE.md:48`, `VISION.md:80-89`, `TEKNIK_PLAN.md:135`, `ADR-0003:23-24`, sunum) | Hepsi kanıtsız *"model kartı teyitli"* formülüne dayalı; repoda **tek bir görselli inference testi yok**; `VERI_PLANI.md:89` zaten OCR için harici DotsOCR diyor | Faz 3 opsiyonu olarak işaretlenir, **karar gerekçesi değil**. Doğrulanmış veri: Gemma 4 12B Unified gerçekten encoder-free, OCR/ses native (model kartı); **ama** OmniDocBench 1.5 = 0.164 (26B A4B 0.149, 31B 0.131 — 12B ailenin en zayıfı). Ayrıca OCRTurk (arXiv:2602.03693): Türkçe'de dedicated OCR motorları (PaddleOCR NED 0.08) genel VLM'leri yeniyor; `ğ→˘g`, `ş→¸s`, `İ→Ì` kırılmaları hukuk metninde RAG eşleşmesini bozar → **Faz 3'te native OCR yerine ayrık OCR preprocessor doğru mimari.** |
| 7 | Sunum (`docs/sunum/`) | Gemma'nın "native multimodal"ını Faz 3 vaadi olarak sunuyor | #6 ile hizalanır |

**Yeni ADR'ler (onay sonrası):**
- Tez çerçevesi = maliyet-normalize parite (bu spec'in özeti)
- Base model sabit tutuluyor: gerekçe + dış geçerlilik limitasyonu + Katman 2 replikasyon kolu
- Faz sırası istisnası: harness dilimi teze dahil, graph-RAG hariç
- Rakip seti + tavan referansı + Nemotron'un kapsam dışı bırakılması

---

## 11. Riskler ve sınırlar

| Risk | Etki | Azaltma |
| :--- | :--- | :--- |
| **`E ≈ D`** — FT harness'ın üstüne bir şey eklemiyor | Tezin FT kolu değersizleşir | Kapı 2'de açıkça karşılanır; çıkarsa **negatif bulgu olarak yayımlanır**. §3.2'deki gürültülü-retrieval hipotezi ana savunma. |
| **Rakipler abstention'da ~1.0** | "Yetişiyoruz" hikâyesi ölür | Kapı 1; tez maliyet+mahremiyet eksenine yaslanır (iddia hâlâ ayakta) |
| **Regex kalibrasyonsuz** | Rakip skorları bizim lehimize kayar → tez çöker | §6.1 zorunlu ön-adım; hiçbir sayı öncesinde raporlanmaz |
| **n yetersiz** | Eşdeğerlik iddiası kurulamaz | n=100/75 baştan (Adım 0); Katman 2 ile daha da büyütülür |
| **Sürüm kayması** | Sayılar eskir | §9 tarihli snapshot pin |
| **HPC alınamaz** | — | **Tasarım gereği etkisiz** (§2 kuralı) |
| **Oracle-context gerçek RAG değil** | Mevcut M1/M4 iyimser tavan | Harness ile gerçek retriever gelince kapanır — zaten sunumda işaretli sınır |
| **Hakem = LLM** | İnsan-κ descoped | §6 dört katmanlı savunma + hakemsiz omurga |
| **Mecellem kıyası birebir değil** | Farklı çıkarım protokolü | İlgili çalışmaya indirildi, cite-only (ADR-0016) |
| **Kapsam şişmesi** | Üç ayrı tez (abstention + graph-RAG + parite) | **(b) çok-ajanlı GraphRAG kesin dışarıda** (§5.3, ADR-0022); (a) yapısal graf dahil ama deterministik + ~0 marjinal maliyet → kapsamı şişirmiyor; katmanlar (§2) |
| **Eval ≠ dağıtım** *(yeni, 2026-07-23)* | CANON bf16/NF4'te koşuyor, dağıtım artefaktı Q4_0+KV q8_0 (ADR-0023) → "dağıtım sınıfında parite" iddiasında delik | En az bir kez aynı CANON'da hizalama koşusu (Q4_0+q8_0 vs bf16); zaten KV-bit × kalite eğrisinin ilk noktası |
| **VRAM tahminleri ölçülmedi** *(yeni)* | Sığdırma merdiveninin sabit kalemleri (CUDA ctx 0.40 GB, compute buffer 0.45/0.30 GB) tahmin; 0.3 GB sapma bağlamı yarıya indirir | Gerçek RTX 5070 + gerçek GGUF ile ölçüm (açık borç); hiçbir sayı öncesinde iddia edilmez |
| **Dış geçerlilik** — bulgular Gemma'ya özgü mü? | Genellenebilirlik kanıtlanmıyor | **Kapatılmayan sınır** (§3.3 kararı: çok-base kolu kapsam dışı). Dürüst limitations maddesi + gelecek çalışma. |

---

## 12. Açık sorular

1. **Retriever korpusu:** canlı Bedesten API mi, dondurulmuş snapshot mı? *Tekrarlanabilirlik dondurulmuş
   snapshot ister; güncellik canlı API ister.* Muhtemel cevap: **eval için dondurulmuş** (tekrarlanabilirlik),
   **doğrulayıcı için canlı** (Faz 2 vaadi). Kararlaştırılmalı. ⚠️ Bedesten **Türk IP** gerektiriyor.
   *(2026-07-23 notu: yapısal graf (ADR-0022) da aynı snapshot'tan türetilir — graf ve retriever
   korpusu ayrışamaz, tek karar.)*
1b. **Zamansal eksen (YENİ, 2026-07-23):** Citation Grounding'in 3. bileşeni — *"atıf yapılan tarihte
   yürürlükte miydi?"* — bizde **hiç yok** (ne CANON'da ne v4 reçetesinde). TR mevzuatında
   `mülga`/`değişik` zincirleri var, Bedesten veriyi sunuyor, yapısal graf zaten taşıyacak.
   **Soru:** CANON'a yeni bir red kulvarı olarak eklensin mi, yoksa yalnız doğrulayıcı boyutu mu
   kalsın? Rakiplerin beceremediği eksen → tez değeri yüksek, ama eval matrisini büyütür.
2. **TR embedding modeli:** hangisi? Lisansı? EDA-verify kuralı burada da geçerli.
3. **Red kapısı eşiği:** tüm atıflar doğrulanmalı mı, çoğunluk mu yeterli? Ablasyon konusu olabilir.
4. **Hakem paneli üçüncü ailesi:** GPT + Gemini + Claude özneyse, hakem panelinde hangi 3 aile?
   Aile-dışlama ile birlikte çözülmeli.
5. **n hedefi:** eşdeğerlik için gerçek güç analizi yapılmalı — n=100/75 (repo hedefi) **fark** testi
   için; **eşdeğerlik** için yeterli mi?

---

## 13. Terminoloji

- **Parite:** eşdeğerlik (D ≈ B), üstünlük değil
- **Maliyet bandı:** "frontier" yerine kullanılır (§4.1)
- **Harness:** retriever + atıf doğrulayıcı + red kapısı (graph yok)
- **Katman 0/1/2:** kapsam katmanları (§2), Faz 1-5 ile karıştırılmaz
- **Kapı:** önceden yazılmış eşikli karar noktası (§8)
- **A/B/C/D/E:** deney hücreleri (§4.3)
