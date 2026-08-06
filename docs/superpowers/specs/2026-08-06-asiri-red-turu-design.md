# Tasarım — Aşırı-red turu (B10) · `τ_a` v2 + rakip kıyasının kurulması

**Tarih:** 2026-08-06 · **Tür:** spec (*ne inşa edilecek*) · **Durum:** insan onayı bekliyor
**Girdi:** [#53](../../record/research_log/2026-08-05-ayirt-edicilik-etiketi.md) ·
[#54](../../record/research_log/2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md) ·
[#56](../../record/research_log/2026-08-05-olcum-bosluklari.md) ·
[ADR-0055](../../adr/0055-isabet-denetimi-ekseni.md) · [ADR-0056](../../adr/0056-m2b-harness-acik-protokolu-ve-0055-cipasi.md) ·
[ADR-0057](../../adr/0057-harness-rekabet-kapisi-esit-sinav.md) · [`sprint3-part1`](../../_arsiv/sprint3-part1.md) borç kuyruğu
**Çıktı:** ADR-0058 · ADR-0059 · `research_log` #57 · #58 · uygulama planı
`plans/2026-08-06-asiri-red-tau-a-v2.md`

---

## 1. Problem — ölçülmüş

Ürünün dürüst sayısı **%61,3** (harness AÇIK, k=10, S2). Tavan **%71,6**. Aradaki 10,2 puanın
kabaca yarısı erişimin, yarısı modelin. Ama **asıl kayıp o tabloda yok:** tavanın kendisinde,
80 sorunun **17'sinde** altın madde bağlamda olmasına rağmen model çekiniyor (harness AÇIK'ta
16, B-i önsözüyle 14). Borç **B10**.

Kütle aritmetiği bunu tam olarak görünür kılıyor — üç kol da özdeşliği sağlıyor:

```
kütle = (1 − aşırı-red) × A1
```

| eksen | çıplak base | `tgta_v1` (BİZ) | Gemini 3.1 FL |
| :--- | ---: | ---: | ---: |
| M1 kütle | 56,7% | **71,6%** | 72,9% |
| aşırı-red | 0,425 | **0,212** | 0,237 |
| A1 | **0,9864** | 0,9087 | 0,9561 |
| M2 Rej | 0,814 | **0,893** | 0,930 |
| M2b Rej | 0,986 | 0,877 | **1,000** |
| tok/cevap | 1192 | **714** | — |

*(harness KAPALI · DEV · aynı protokol · [`kollar.md`](../../record/kollar.md) — parite iddiası DEĞİL)*

**Base'in altında olduğumuz iki eksen: A1 (−7,8 p) ve M2b (−10,9 p).** FL karşısında beş
eksenin dördünde geride, yalnız aşırı-red ve maliyette öndeyiz.

---

## 2. Teşhis — aşırı-red `τ_a`'nın **öğretildiği** şey

Yukarıdaki tablo, kimse o gözle okumadığı için sessiz duruyordu: **aşırı-red kaynağı `τ_a`.**
Tek başına 0,575 — çıplak base'i (0,425) bile kötüleştiriyor. `τ_g` 0,175. Merge'in 0,212'si
zaten seyrelmenin eseri.

Sebep kodda doğrulandı, varsayım değil:

```
data/train/orpo_abstain_cp2c/train.jsonl            845 satır
  is_pref = 1   703 çift   → HEPSİ "çekinmeyi tercih et"      (m2 538 · m2b 188)
  is_pref = 0   142 satır  → grounding replay
                             build_orpo_v3.py:44 — "is_pref=0 → OR maskeli,
                             içeriği loss'a girmez, yalnız concat şeklini sağlar"
```

⇒ **`τ_a` v1'in eğitiminde "altın bağlamdayken CEVAPLA" yönünde tek bir tercih baskısı yok.**
Grounding replay yalnız NLL terimi taşıyor; kontrast yok.

Üstelik m2b çiftlerinin çeldiricileri komşu-öncelikli, yani altınla **aynı kanundan**
(`raft_pack.py:75-91`; #56'da ölçülen zorluk **1,0000**). Modelin gördüğü tek örüntü:

> *RAG_MULTI kalıbı + aynı kanundan 4-5 madde → "Verilen kaynaklarda bu konuyu düzenleyen
> madde bulunmuyor" de.*

[#53](../../record/research_log/2026-08-05-ayirt-edicilik-etiketi.md)'ün ölçtüğü patoloji —
*çekinme sinyali bağlamın **konusal uyumundan** geliyor, **yeterliliğinden** değil; model
erişimin en çok battığı belirsiz sorularda **en az** çekiniyor (%5,6 ↔ %30,6)* — bunun
**birebir beklenen sonucu**.

### 2.1 Bu, B4 yasağını yeni bir gerekçeyle güçlendiriyor

`τ_a` genliği tek bir kaldıraç ve **B4 ile B10 onun iki ucunda**:

```
genlik ↑ :  M2b Rej 0,877 → 0,987  ✅ (B4'ün istediği)
            aşırı-red 0,212 → 0,575 ❌ (B10'u yıkar)
```

Genlik bir çare değil, bir **takas**. İkisini birden hareket ettirebilecek tek şey `τ_a`'nın
**ne öğrendiği**. Bu, `sprint3-part1`'in *"birleştirmek ölçülmemiş varsayımı gerçeğe çevirir"*
gerekçesini iptal etmiyor — ona ikinci bir gerekçe ekliyor.

---

## 3. Karar — `τ_a` v2: **simetrik yeterlilik çifti**

Eksik sınıf eklenir. Aynı kalıp, aynı komşu-öncelikli çeldiriciler, **altın madde BAĞLAMDA**:

| | m2b çifti (mevcut, 188) | **m1_yeterli çifti (YENİ, hedef ~250)** |
| :--- | :--- | :--- |
| istem | RAG_MULTI + 4 çeldirici, altın **YOK** | RAG_MULTI + altın **VAR** + komşu çeldiriciler |
| `chosen` | *"Verilen kaynaklarda bu konuyu düzenleyen madde bulunmuyor…"* | gerekçeli, atıflı cevap (`raft_scrubbed` grounded hedefi) |
| `rejected` | çeldiriciden uydurulmuş cevap (on-policy hasat) | ⭐ **aynı çekinme cümlesi** (on-policy hasat) |

**Tasarımın tek iddiası budur:** aynı dize, altın yokken **yukarı**, altın varken **aşağı**
itiliyor. İki çift arasındaki tek fark **cevaplayan maddenin bağlamda olup olmaması** — ORPO'nun
kaybı ancak *yeterliliği* okuyarak düşebilir, *konusal uyumu* okuyarak düşemez.

Müdahale, #53'ün ölçtüğü mekanizmayla birebir hizalı. Yeni bir yetenek öğretmiyor;
[#56](../../record/research_log/2026-08-05-olcum-bosluklari.md)'nın dersini uyguluyor:
**var olan yeteneği varsayılan hâline getiriyor.**

### 3.1 Rejim — değişmez

`τ_a` v1 ile birebir: lr 1e-5 · beta 0.1 · etkin batch 64 · 5 epoch · r=16/α=32 · dropout 0.05 ·
224 LoRA çifti · `--fresh-adapter` · **ham base'den** · seed 3407. **Değişen tek şey veri.**
`‖τ_a v2‖` koşulsuz raporlanır → B4 eksenine dokunulmadığı **ölçülebilir** kalır.

Merge de v1 parametreleriyle: ham TIES, `--no-norm-balance`, trim_k 0,2, λ 1,0, eşzamanlı 2-yollu.

### 3.2 Hasat

- **Havuz:** `data/train/raft_scrubbed/train.jsonl`, `slice="grounded"` (13.350), shuffle seed 3407.
- **Özne:** çıplak base (ADR-0042 on-policy; `cp2_harvest.py`'nin precedent'i). Base'in aşırı-reddi
  0,425 → beklenen kabul oranı ~%40.
- **Kabul ölçütü:** `exact_reject(cevap, "data")` **RED sayıyor** → gerçek aşırı-red örneği.
  Bu, `harness_tablo.py:111`'in B10'u saydığı **birebir aynı çağrı** → tuzak **4.7** tanım gereği sağlanır.
- **Taşıyıcı:** base Q4_K_M GGUF + llama-server, rejim değişmezleri (thinking on · 1024+512 · 900 klip).

### 3.3 Veri hijyeni — `τ_g` v1'de olmayan bir sıkılaştırma

Hasat havuzundan DEV **ve** CANON'un altın maddeleri dışlanır. Soru düzeyinde kesişim zaten
**0** (ölçüldü), ama **madde düzeyinde 67/70 örtüşüyor**. `τ_g` v1'de bu hijyen yok — pre-existing,
kayda geçer, bu turda **düzeltilmez** (cerrahi kural).

---

## 4. Elenen alternatifler

| seçenek | niçin elendi |
| :--- | :--- |
| **merge genliğini oynat** (λ · trim_k · norm) | B4'ün ekseni — yasak. **Ve** §2.1'e göre çare değil takas |
| **B-ii çapraz-kodlayıcı** | ADR-0055'in sırası bağlayıcı: B-i **düşmedi**, geçilmez. Ayrıca harness işi — harness KAPALI'daki 17/80'e dokunamaz |
| **`τ_g` v2** | aşırı-red kaynağı değil (0,175). `kollar.md` kuralı v2'de bütün açık kalemlerin **aynı anda** kapanmasını şart koşuyor → ~$4,4 + kafes yeniden ölçümü. Cerrahi değil |
| **merge edilmiş modele ORPO** | ardışık SFT olur, `τ = θ_ft − θ_base` bozulur (tuzak **3.8**) |
| **142 replay satırını `is_pref=1` yapmak** ($0) | `rejected` tarafı uydurma bir tereddüt cümlesi (*"…ek bilgi ve dikkatli bir inceleme gerekmektedir"*), modelin gerçek aşırı-reddi değil → ADR-0042 ihlali, **ve** öğretilen kontrast yanlış dize olur |
| **sade/kısa dille eğitmek** | denendi, doğruluğu düşürdü ([ADR-0010](../../adr/gemma4-12b-dersler.md#adr-0010)) |
| **A1'i bu turda hedeflemek** | A1 açığı **gerçek** (ADR-0041 muafiyeti zaten uygulanmış, eşleştirilmiş alt kümede de hayatta kalıyor — #41 §4.2). Sahibi ADR-0041 **seçenek D**: RAFT şablonunun 1. adımını çıkarıp `τ_g`'yi yeniden eğitmek, ~$5,5 — kayda geçmiş ve bilinçle park edilmiş. Ayrı tur |

---

## 5. Kapsam — üç iş, sıra bağlayıcı

| # | iş | bedel | neden bu sırada |
| :-: | :--- | :--- | :--- |
| **0** | **YB1 — B-i önsözünü ana protokole benimse** (ADR-0058) | $0 | Bir **eğitim** turunun çıpası, elde olan en iyi **dağıtım** yapılandırması olmalı; yoksa istem katmanından bedavaya alınabilecek bir kazancı eğitime yazarız. Çıpa **%62,8** |
| **1** | **Eşleştirilmiş alt küme A1** — `tgta_v1` ↔ base ↔ FL | $0 post-hoc | Tuzak **2.4**: base soruların %57,5'ini, biz %78,75'ini cevaplıyoruz → ham A1 kıyası elmayla armut. Bu kıyas `tgta_v1` için **hiç yapılmadı** |
| **2** | **Gemini FL harness AÇIK — İKİ SÜRÜM (3.1 + 3.5)** — ADR-0057 eşit sınav | ~$0,9 | 🚨 Bugün *"FL'ı geçtik/geçemedik"* cümlesi **kurulamıyor**: bizim sayımız AÇIK (%62,8), FL'ınki KAPALI (%72,9). Ürün rejiminde kıyas **mevcut değil** |
| **3** | **`τ_a` v2 turu** | ~$2 | Asıl iş. 0-2 bittikten sonra çıpa **donar** ve tur ona karşı ölçülür |

**Bütçe tavanı: $10** (beklenen ~$3,0-3,9). Defter **üç cüzdana** ayrılır — hakem · GPU · rakip
çıkarımı — ve toplanmaz (tuzak 6.3).

### 5.1 Adım 2'nin protokolü

**İki rakip kolu** (insan kararı, 2026-08-06):

| kol | niye | hakem çakışması |
| :--- | :--- | :--- |
| `gemini-3.1-flash-lite` | Kaydın sürekliliği — `kollar.md`/`MODEL_CARD`/sprint1 ona bağlı; düşürmek eski tabloyu **kalıcı olarak tamamlanamaz** yapar | google ↔ OpenAI hakem ✅ |
| `gemini-3.5-flash-lite` 🆕 | **2026-07-21'de çıktı**, güncel giriş katmanı. 16 gün önce aşılmış bir modelle kıyaslanan OSS sürümü *"kolay baseline"* eleştirisini davet eder | google ↔ OpenAI hakem ✅ |

⛔ **GPT-5.4 nano sınıfı DIŞARIDA — para değil, kendi kuralımız engelliyor.** Hakem `gpt-4o-mini`
**OpenAI ailesi**; ADR-0032 *"hiçbir özne kendi ailesinin hakemi tarafından puanlanmaz"* diyor
(ders A3.9). Eklemek üç-aileli panelin açılmasını gerektirir — `judge_agreement.py` **var ama bu
hattın hiçbir koşusunda kullanılmadı** → κ ölçümü + tüm çıpaların yeniden türetilmesi, yani turun
içinde **üçüncü** protokol değişikliği. **Ret değil sıralama** → borç **YB4**.

- Aynı 80 DEV sorusu · aynı indeks (`mevzuat_bge_m3_s2`) · aynı `k`=10 · aynı 900 klip · seed 3407.
  Bağlam **bizim** retriever'ımızla kurulur ve her iki FL'a öyle verilir → ADR-0057'nin *"aynı
  kaynak sayısı, aynı altın koşulu"* şartı sağlanır.
- ⚠️ **Aynı aile ≠ aynı kalıp:** 3.1 için yapılan red-regex kalibrasyonu 3.5'e **taşınır
  varsayılmaz**; iki kolda ayrı doğrulanır. Regex değişirse **bizim koşularımız da** yeniden
  skorlanır — yoksa sayılar farklı aletle üretilmiş olur.
- ⚠️ **Ön koşul:** 3.1 FL'ın OpenRouter'da hâlâ çağrılabildiği doğrulanır. Emekli edildiyse o kol
  düşer, kıyas 3.5 üzerinden kurulur, düşme sebebi **yazılır**.
- **Muhakeme ekseni eşitlenir:** FL `--reasoning-budget 1024` ile koşulur (bizim 1024 düşünce
  bütçemize karşılık). Sağlayıcı bunu onurlandırmıyorsa eksen **TANIMSIZ** damgalanır ve maliyet
  duyarlı hiçbir hüküm kurulmaz.
- **Ön koşul (zorunlu):** red-regex'in Gemini ailesi × mod kalibrasyonu (tuzak **2.1** · **2.2** ·
  ADR-0044). Kalibre değilse rakibin reddi eksik sayılır ve sapma **bizim lehimize** çıkar.
- `h2b@k=4` de koşulur (M2b'nin eşleşmiş ekseni, ADR-0057 Kademe 2).

---

## 6. Ön-kayıtlı kapılar

### 6.1 🛑 KOL KAPISI — merge'den **ÖNCE**

`τ_a` v2 tek başına · harness KAPALI · DEV · n=80 · ana protokol:

```
BAŞARILI   aşırı-red < 0,425 (base çıpası)  VE  M2b Rej ≥ 0,95  VE  M1 A1 ≥ 0,88
KISMİ      0,425 ≤ aşırı-red < 0,50         VE  M2b Rej ≥ 0,95   → merge edilir, "kısmi" damgalı
BAŞARISIZ  aşırı-red ≥ 0,50   ya da   M2b Rej < 0,95
           → MERGE YOK · ÜRÜN EVAL'İ YOK · TUR DURUR
```

Eşik neden **base** (0,425), `τ_a` v1 (0,575) değil: v1'i geçmek ucuz bir eşik. Base'in altına
inmek, kolun artık aşırı-red **üretmediğini** söyler. `M2b ≥ 0,95` takas korumasıdır — patoloji
yer değiştirirse (A3.6 · tuzak **2.13**) kapı düşer.

### 6.2 🛑 ÜRÜN KAPISI

harness AÇIK · k=10 · S2 · ana protokol (önsözlü) · n=80 · seed 3407:

> ⚠️ **BİRİM DÜZELTMESİ 2026-08-06 (kusur Ö-A).** Aşağıdaki eşikler **emekli birimde** yazılmıştı: paydaları modelin cevabına bakan hakemden geliyordu (K3). Eski değerler **silinmedi**, `~~üstü çizili~~` duruyor. Ölçülmüş çeviriler ([#57](../../record/research_log/2026-08-06-cekinme-aleti-onarimi.md)): `tgta_v1` KAPALI m2b **0,877 → 0,766** · AÇIK `h2b@k=4` önsözsüz **0,840 → 0,735** · AÇIK `h2b@k=4` **önsözlü** (ana protokol, ürün kapısının çıpası) **0,809**.

```
BAŞARILI   kütle > %62,8  VE  B10 < 14/80  VE  M2b Rej (önsözlü h2b@k=4) ≥ 0,809   ~~0,840~~
KISMİ      B10 < 14/80 ama kütle ±0,3 içinde → çekinme düzeldi, kayıp başka yerde; tanı OKUNUR
BAŞARISIZ  kütle < %62,5  ya da  B10 ≥ 14/80  → `tgta_v1` ÜRÜN OLARAK KALIR
```
🚨 **0,809 insan kararının mekanik sonucudur** (plan §KARAR-1, 2026-08-06): kural
*"eşik Ö5'in önsözlü çıpasından türetilir"* idi, çıpa 0,809 ölçüldü. ADR-0050 gereği
sonuç görüldükten sonra eşik değil **alet** düzeltildi.

Hüküm üretmeyen, ama zorunlu ek ölçümler: önsözsüz koşu (%61,3 ile kıyas) · ayırt edici/belirsiz
alt küme kırılımı (ADR-0054 K4) · harness KAPALI M1 (17/80 çıpası).

### 6.3 ⛔ Ön-kayıtlı tahminler — *sayı görülmeden yazıldı*

| eksen | çıpa | tahmin | gerekçe |
| :--- | ---: | ---: | :--- |
| B10 (AÇIK) | 14/80 | **8-11/80** | 703:0 asimetri ~4:1'e iniyor; tek bir istem satırı (D1) 2 kalem aldıysa tercih baskısı daha güçlü kaldıraç |
| kütle (AÇIK) | %62,8 | **%64-66** | kurtarılan her kalem ≈ %1,25 kütle, A1 sabit varsayımıyla |
| kütle (KAPALI) | %71,6 | **%75-79** | `(1 − aşırı-red) × A1`; B10 17→10 ise coverage 0,875 |
| **M2b Rej** (önsözlü AÇIK) | **0,809** ~~0,877~~ | ⭐ **mekanizmanın ayırt edici ölçümü** — aşağı bak | |
| Δ(önsöz) | +1,43 p | **+0,0 … +0,7 p** | ⭐ yetenek varsayılan olduysa önsözün marjinal katkısı **daralır** |
| ‖τ_a v2‖ | 1,1806 | **1,18 ± %25** | rejim aynı, veri ~%30 büyüdü → B4'e dokunulmadığının kanıtı |

**M2b bir yan etki değil, turun mekanizma testi:**

```
M2b ≥ 0,766 ~~0,877~~     → model YETERLİLİĞİ öğrendi (altın yokken tanıyor)  ✅ tuttu
0,735 – 0,766 ~~0,84–0,877~~ → kısmi                                          🟡
M2b < 0,735 ~~0,84~~      → model yalnız "daha çok cevapla" öğrendi           ❌ kör kayma
```

🚨 **Bu bandın İKİ UCU İKİ AYRI SINAVDAN geliyor** — üst uç `tgta_v1`'in **KAPALI** m2b'si
(distractor kurgusu), alt uç **AÇIK** `h2b@k=4`. ADR-0057 gereği eşleşmeyen eksenler tek
banda konamaz; band bu hâliyle **birim düzeltmesinden önce de** kusurluydu, çeviri onu
görünür kıldı. **Görev 9 ölçümü ÖNSÖZLÜ `h2b@k=4`'tür** ve tek geçerli çıpası **0,809**;
mekanizma okuması o çıpaya göre yapılır, bu band yalnız **tarihsel süreklilik** için durur.

Simetrik çiftin tek iddiası, modelin altın-var/altın-yok ayrımını okumasıdır. Okuyorsa M2b
düşmez. Düşüyorsa müdahale patolojiyi **taşımıştır**, çözmemiştir — ve kapı orada durur.

---

## 7. Kabul edilen bedeller ve kural sapmaları — üçü de kayda giriyor

1. **⚠️ Çiftler ÖNSÖZSÜZ kurulur — eval-ayna kuralından (ADR-0011) sapma.**
   YB1'den sonra ana protokol önsözlüdür, kural eğitim isteminin de önsözlü olmasını söyler.
   Uyulmuyor: mevcut 703 çekinme çifti 2026-08-02'de **önsözsüz** hasat edildi ve `rejected`
   tarafları o isteme karşı üretildi. Pozitif çiftler önsözlü kurulursa eğitim setinde iki
   sistem istemi olur ve modelin öğrenebileceği en ucuz kısayol **"önsöz varsa cevapla, yoksa
   çekin"** — tam ters kalibrasyon, ve hiçbir yerde hata vermez. Mevcut çiftleri önsözlü hâle
   getirmek `rejected`'ı on-policy olmaktan çıkarır (ADR-0042).
   ⇒ Eğitim seti **iç tutarlı** tutulur; ölçüm ana protokolde yapılır.
   **Yan getiri:** önsözsüz eğitilen bir kol önsözlü eval'de kazandırıyorsa, kazanç önsöze
   bağımlı değildir — Δ(önsöz) testi güçlenir.

2. **⚠️ `chosen` RAFT şablonunu taşıyor** — `1) … 2) ##begin_quote## … 3) Sonuç`. Bu şablon
   tuzak **2.10**'un konusu. ADR-0041'in hakem muafiyeti bunun **ölçüm** tarafını kapatmış
   durumda (zaten uygulanmış), ama **ürün** tarafı açık: o cümleyi ne avukat ne vatandaş istiyor.
   Alternatifi (şablonu sıyırmak) elendi — `chosen` eval aynası olmaktan çıkar ve `τ_g` ile
   çelişen bir üslup öğretir. Kusur `τ_g`'de zaten var; bu turda **çözülmüyor**.

3. **⚠️ Hasat öznesi base, B10 ise `tgta_v1`'de yaşıyor.** ADR-0042'nin on-policy tanımı
   *eğitilen modele* göredir ve `τ_a` ham base'den eğitiliyor; `cp2_harvest.py`'nin precedent'i
   de budur. Base'in aşırı-reddi (0,425) merge'inkinin (0,212) bir **üst kümesi** — ayrım
   gizlenmiyor.

**Ayrıca kaydedilen bir belge tutarsızlığı:** `yurutme-tuzaklari.md` 2.10 ADR-0041'i *"🔴 AÇIK"*
gösteriyor; `open_questions` §13.8 **kapalı** diyor ve kural `groundedness.py:65-71`'de **canlı**.
Tuzak satırı düzeltilir.

---

## 8. Durma koşulları

1. **Kol kapısı BAŞARISIZ** → merge yok, ürün eval'i yok. Negatif bulgu #58'e yazılır, tur durur.
2. **Pilotta kabul oranı < %10** → hasat körü körüne büyütülmez; *havuz mu, ölçüt mü* sorusu
   önce cevaplanır.
3. **Geçerlilik kapısı düşerse** (kesik > %5 · `ALTIN_SIZAN` > 0 · künye eksik) → koşu geçersiz,
   sayı **raporlanmaz**, reçeteye körü körüne uyulmaz.
4. **Bütçe $10** → durur.

---

## 9. Kayıt yükümlülükleri

| belge | ne girer |
| :--- | :--- |
| **ADR-0058** | YB1 — B-i önsözünün benimsenmesi; hangi çıpaların yeniden türetildiği; *"eşik gevşetmesi değil, ölçü birimi düzeltmesi"* ayrımı |
| **ADR-0059** | `τ_a` v2 veri simetrisi kararı; elenen alternatifler; §7'deki **üç kural sapması**; ön-kayıtlı tahminler |
| **`research_log` #57** | YB1 + eşleştirilmiş A1 + Gemini FL harness-AÇIK sonuçları |
| **`research_log` #58** | `τ_a` v2 turu — kol kapısı, ürün kapısı, tahminlerin tutup tutmadığı |
| **`kollar.md`** | `τ_abstention` **v2** satırı (`‖τ‖` dahil) + `tgta_v2` merge satırı |
| **`MODEL_CARD` · `ROADMAP`** | çıpa **%62,8**; FL kıyası artık ürün rejiminde |
| **`CLAUDE.md`** | yalnız **İŞARETÇİLER** — sayı değil |

---

## 10. Bu turun kapsamadığı — açıkça

- **A1 açığı** (base'e −7,8 · FL'a −4,7). Gerçek, ölçülmüş, sahibi ADR-0041 seçenek D. Ayrı tur.
- **B4** — `τ_a` genliği. Yasak, ve §2.1'e göre zaten bir takas.
- **B8 · B9 · B6** — dokunulmuyor.
- **OpenAI-ailesi rakip** (GPT-5.4 nano sınıfı) — aile-dışlaması engelliyor, üç-aileli panel
  turuna kalıyor (**YB4**).
- **`ROADMAP` hedef cümlesinin güncellenmesi** — *"önce 3.1 FL'ı geçmek"* bayatladı, ama yeni
  hedef **ölçüm görüldükten sonra** yazılır (**YB5**).
- ⚠️ **"Her eksende net farkla ezmek" tek turda ulaşılabilir bir hedef değil.** Bu tur
  **kütle** ve **aşırı-red** eksenlerini net farka taşıyabilir; **A1** ve **M2b** eksenlerinin
  sahipleri ayrı ve adları yukarıda yazılı.
