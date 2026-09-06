# HakHukuk — yeni yön: vatandaşın hukuk danışmanı (açık kaynak ÜRÜN)

Repo: `/home/ersoy/code/Hukuk-SLM` · branch **`yeni-yeni`** · çalışma dili **Türkçe**
(kod tanımlayıcıları İngilizce). Python: `source ~/code/global_venv/bin/activate`
**aynı komut içinde**.

> **Bu belge bir devir notudur.** İleriye dönük belge katmanı **silindi** (yedek: ayrı backup
> branch). Elimizde artefakt, alet ve **ölçüm kaydı** var; **yön belgesi yok.** Onu bu oturumda
> sıfırdan yazacağız. Bu dosya, yön belgesi yazılırken kaybolmaması gereken her şeyi taşıyor.

---

## 1. AMAÇ — çerçeve değişti

```
ESKİ   yüksek lisans tezi → bir iddiayı kanıtla → kapılar/ablasyonlar iddiaya hizmet eder
ARA    açık kaynak model  → "en iyi modeli yap", disiplin kendini kandırmama aleti
YENİ   AÇIK KAYNAK ÜRÜN   → Türk hukukunda VATANDAŞIN tavsiye alabileceği bir danışman
```

- **v1 = MODEL KATMANI.** Çalışan, indirilebilir ve **yayımlanan sayıyı kullanıcının kendi
  makinesinde yeniden üretebildiği** bir fine-tuned model release'i.
- **v2 = APP KATMANI.** Aynı modelin üstünde vatandaşın kullandığı uygulama / API.
- **arxiv paper'ı YAZILACAK** — tez değil, ürünün yanında çıkan bir **metodoloji/sistem**
  paper'ı. Hedef ürün, paper yan ürün. *(Bu yüzden ölçüm kaydı korundu — paper'ın verisi o.)*

## 2. NE SİLİNDİ, NE KALDI

**Silindi** (insan kararı, backup branch'te duruyor):
`ROADMAP.md` · `TODO.md` · `TASARIM.md` · `docs/VISION.md` · `docs/PAPER_TARGET.md` ·
`docs/superpowers/**` (tüm spec + plan) · `docs/_arsiv/**` (kapanmış sprint'ler + devir notları).

**Korundu — çünkü kaynak, iddia değil:**
`docs/record/research_log/` (**#39-#61**, tarihli ölçüm kaydı) · `docs/adr/` (**0062**'ye kadar
karar defteri) · `docs/record/kollar.md` (artefakt sicili) ·
`docs/record/yurutme-tuzaklari.md` (*"hata vermeden yanlış sayı üretir"* kalıpları) ·
`outputs/eval/**` (ham ölçümler + künyeler) · `docs/BEDESTEN_API.md` (canlı mevzuat sözleşmesi) ·
`MODEL_CARD.md` · `README.md` / `README.tr.md` · `CLAUDE.md`.

**Kaderi belirsiz — yeni belge katmanını yazarken karar ver, bana sor:**
`docs/FINE_TUNING.md` (Faz 1 playbook) · `docs/VERI_PLANI.md` (veri planı) ·
`docs/YARGI_KAYNAKLARI.md` · `docs/open_questions.md` (S1-S14 + OQ kaydı) ·
`docs/model-soyagaci.mmd` · `referans-design-doc.md` *(kullanıcının özgün taslağı —
**asla düzenlenmez**, silinip silinmeyeceği kullanıcının kararı)*.

⚠️ **`CLAUDE.md` · `MODEL_CARD.md` · `README*.md` artık silinmiş dosyalara link veriyor.**
Bu linkler **kırık**. Yeni belge katmanı yazılırken bunlar da güncellenecek — ama önce
yeni belgeler var olmalı ki işaretçiler bir yere gitsin.

---

## 3. ELDEKİ GERÇEK — ölçülmüş ve kaynaklı

⚠️ **Bu sayılar yeni belgelerin çıpasıdır.** Hiçbirini hatırlayarak yazma; her biri aşağıdaki
dosyadan okunur. Kaynağı olmayan nicelik **ÖLÇÜLMEMİŞ** damgası alır.

### 3.1 Artefakt
`HakHukuk-4B-v0.1` (iç kimlik `tgta_v1`) = `tg_v1` (grounding) + `ta_v1` (abstention).
İki LoRA kolu **ham base'den bağımsız** eğitilip **ham TIES** ile task-vector olarak birleşti
(trim_k 0,2 · λ 1,0 · 224/224 tensör). Base `Qwen/Qwen3.5-4B` (commit `851bf6e8`).
Taşıyıcı `models/gguf/tgta_v1-q4_k_m.gguf` **2,59 GiB**.
`‖τ_g‖` **10,4722** · `‖τ_a‖` **1,1806** (oran 8,87×) → `docs/record/kollar.md`.

### 3.2 Ürünün resmî sayısı — harness AÇIK · k=10 · S2 indeks · yeterlilik önsözlü
*(`outputs/eval/olcum-bi/harness_tablo.json` · DEV n=80 · hakem `gpt-4o-mini` · seed 3407)*

| eksen | değer |
| :--- | ---: |
| `recall@10` | **0,875** (70/80) |
| coverage | **0,8250** |
| A1 (cevaplanan-only) | **0,8288** |
| A1 · altın getirilen | **0,8729** |
| **sadık-cevap KÜTLESİ** | **%68,4** |
| uydurulmuş madde no | **0/83** |
| aşırı-red (altın bağlamda sustu) | **9/80** — *80 kalem gözle okundu: **8/80*** |
| isabetsizlik (başka gerçek maddeden cevapladı) | **5/80** |

**Önsözsüz ablasyon** (`outputs/eval/s2-harness-k10-etiketli/`): kütle **%73,0** · coverage 0,9000 ·
A1 0,8110 · aşırı-red **5/80** · isabetsizlik 7/80.
**Tavan** — harness KAPALI, altın kurgu gereği verilir (`outputs/eval/cp3-supurme-ham/`):
kütle **%71,6** · A1 **0,9087** · aşırı-red 17/80. ⚠️ **Tavan bir rakip değil.**

### 3.3 Rakip — ürün rejiminde ölçüldü, eşit sınav kanıtlı
*(`outputs/eval/g2-fl-harness/OZET.md` — `recall@10` üç öznede de birebir **0,875**)*

| | **BİZ** | Gemini 3.1 FL | Gemini 3.5 FL |
| :--- | ---: | ---: | ---: |
| M1 kütle | **%68,4** | %61,7 | **%69,5** |
| A1 · cevaplanan | **0,8288** | 0,7054 | 0,7940 |
| A1 · altın getirilen | **0,8729** | 0,7835 | 0,8607 |
| altın bağlamda sustu ↓ | 9/80 *(gözle 8/80)* | 8/80 | **6/80** |
| $/cevap (girdi+çıktı) | **$0** (yerel) | $0,002074 | $0,002175 |

⛔ ***"3.5 FL ile eşitlendik"* cümlesi KURULMUYOR.** Kalan 1,1 puanı koruyan çözünürlük sınırı
**yok**: hakem gürültü tabanı **0,3 A1 puanı** yalnız A1 makrosu içindir, kütle = coverage × A1
ve coverage'ın varyansı o tabanda yok. Ayrıca son kazanç **modelden değil aletten** geldi (§3.5).

### 3.4 Donanım — ölçüldü
`outputs/eval/_artefakt/vram_stack.json` (Q4_K_M · KV q8_0): ctx **4.096 → sunucu 3,09 GiB**,
tepe 4.530 MiB · ctx 32K → 3,70 GiB · ctx 128K → 5,76 GiB.
⚠️ Ölçüm **base GGUF** üzerinde; `tgta_v1`'in kendisi **ölçülmedi** (~15 dk, **$0** borç).
Dev makine: **RTX 5070 Laptop ~12 GB, Blackwell sm_120, CUDA 13.x**. Son kullanıcı hedefi
**≤8 GB yumuşak kapı** (üstü de raporlanır, erişilebilirlik ekseninde bedelle).

### 3.5 🚨 En yeni bulgu — ürünün sayısı neden değişti (2026-09-06)
Çekinme dedektörü (`exact_reject`) *"açılış hükmü yok"* dalında **cevabın tamamını** tarıyordu;
bizim cevap şablonumuzun **eleme gerekçesi** (*"diğer kaynaklar … içermemektedir"*) red regex'ini
tetikliyordu. Hata **bizim kendi eğitim şablonumuza özgüydü** — Gemini'nin cevaplarında o kalıp
80'de yalnız 3'te var ve onarım **onların sayılarını hiç oynatmadı** (varsayılmadı, ölçüldü).
Onarım + **80 kalemin gözle okunması**: aşırı-red **14/80 → 8/80**, kütle **%62,8 → %68,4**,
`recall@10` **değişmedi**. Eski 14'ün **6'sı yanlış pozitifti**, **yanlış negatif yoktu**.
⇒ *"En büyük kusur"* sandığımız şeyin **%43'ü ölçüm aletinin kendisiymiş.**
Kayıt: `#60` · `#61` · `ADR-0061` · `ADR-0062` · `outputs/eval/olcum-bi/B10_GOZLE_OKUMA_80.md`.

⚠️ **Ve aynı onarım `ADR-0058`'in gerekçesini tersine çevirdi:** yeterlilik önsözü *kütleyi
yükselttiği için* benimsenmişti; artık **düşürüyor** (önsözlü %68,4 ↔ önsözsüz %73,0, **−4,6 p**)
ama A1'i (**0,8288 ↔ 0,8110**) ve isabetsizliği (**5/80 ↔ 7/80**) **yükseltiyor**. Kıyas eşleşmiş:
aynı 80 soru, **80/80 birebir aynı bağlam**, değişen yalnız istem. **Protokol değiştirilmedi.**

### 3.6 Erişim katmanı
Hibrit **BM25 + `bge-m3`**, RRF ile birleşik · indeks `data/index/mevzuat_bge_m3_s2/` (**80 MB**,
S2 = yürürlük alanı + alt-madde kimliği) · **759 ms/sorgu, CPU'da — GPU'ya girmiyor** (sığar/
sığmaz farkını yaratan tek şey bu) · korpus `data/corpus/mevzuat_maddeler.jsonl` (**40.496**
madde chunk'ı). Vektör DB **ölçüldü ve reddedildi** (brute force 8,2 ms/sorgu, indeks 83 MB).

### 3.7 Eval protokolü — rejim değişmezleri (uyuşmazlık hata vermez, kıyası GEÇERSİZ kılar)
6 kipli CANON: **M1** çeldirici-sadakat · **M4** oracle tavan · **M2** yakın-ıska red ·
**M2b** çok-kaynak-ıska red · **M3** boş-bağlam red · **M5** kör/parametrik = **ANTİ-HEDEF**
(yükselmemeli). Harness'lı karşılıkları `h1`, `h2b`.
Değişmezler: **seed 3407** · eval-aynası **900 karakter** chunk klip · A1 = **cevaplanan-only**
makro · **düşünce AÇIK, bütçeli zorla kapatma: 1024 düşünce + 512 cevap** (ADR-0043).
**TEST = `data/eval/canon/` (40 + 35 = 75), DONMUŞ ve HİÇ GÖRÜLMEDİ.** Tüm merge/hiperparametre
seçimi **DEV**'de yapıldı. ⚠️ Set **git'te ve repo public** — "donmuş"luğu gizlilikle değil
**usulle** korunuyor.
Hakem: dört katmanlı savunma (hakemsiz omurga = regex red + deterministik atıf doğrulama ·
yargı eksenlerinde 3 aileli panel · **aile dışlaması** · self-preference ölçülür).
⚠️ **Panel kurulmadı** — bugün her yargı-eksenli sayı **tek aile** (`gpt-4o-mini`), κ yok.
⚠️ **Rakip aileleri için red regex'i her seferinde kalibre edilir** — kalibre edilmezse onların
redlerini eksik sayar ve puanı **bizim lehimize** kaydırır.

## 4. NE VAR — yeniden kurma

`scripts/`: `gen_eval_grounded.py` (**tek üretim gövdesi**) · `harness_tablo.py` ·
`groundedness.py` · `rescore_answered.py` · `score_abstention.py` (**2026-09-06'da onarıldı**) ·
`atif_dogrula.py` (**MULGA** hükmü dâhil) · `merge_ties.py` (eşzamanlı k-yollu) · `merge_lora.py` ·
`setup_llamacpp.sh` · `b10_hasat.py` · `eslesmis_a1.py` · `measure_vram_stack.py` ·
`bedesten_probe.py` · `madde_anahtar.py` · `llm_client.py` (tek model erişim kapısı).
`modal_train.py`: `spawn_sft` · `spawn_orpo` · `harvest_cp2` · **`harvest_b10`** (L4'te doğrulandı,
ADR-0047 m.2 taşıyıcısı: Q4_K_M GGUF + llama.cpp, KV q8_0, `-fa on`, **vLLM/bf16 YASAK**).
`pytest` → **112 passed, 2 xfailed**.
Sızıntı süzgeci: havuz 13.350 → **12.914** (konteynerde yerelle birebir).

## 5. AÇIK BORÇLAR — silinen arşivden kurtarıldı, yeni roadmap bunları taşımalı

| # | borç | ölçülen büyüklük | engelliyor |
| :-- | :--- | :--- | :--- |
| **B1** ⭐ | **İsabetsizlik** — gerçek ama soruya uymayan maddeden cevaplama. Eksen `ADR-0055`'te belirlendi, **kod hiç açılmadı** | **5/80** (ablasyon 7/80) | **v1** — *yeni birinci sıra* |
| **B10** | **Aşırı-red** — altın bağlamdayken çekinme | **9/80** (gözle **8/80**) · rakip 8 ve 6 | v1 (açık sınır) — *tur kapandı, `ADR-0062`* |
| **B4** | `τ_a` merge'de seyreliyor (0,987 → 0,766, **−22,1 p**). Çare merge parametresinde değil, muhtemelen **eğitim genliğinde** | `‖τ_a‖` 1,18 · 70 adım @1e-5 | v1 (dolaylı) |
| **B6** | **Canlı `bedesten` katmanı yok** — sözleşme **4/4 geçerli**, ürün çağırmıyor | ⚠️ **TR IP şart** (gov firewall yurtdışı/VPN'i bloke ediyor) | **v2** |
| **B8** | Katı kapı **tek karakterlik yazım hatasına** takılıyor (`…ESELERİ…`) | 1/80 · eğri ölçüldü, tolerans **BENİMSENMEDİ** (risk tarafında **0 gözlem**) | v1 (düşük) |
| **B9** | Tablo/cetvel parçaları madde diye indeksli (~7.966 satır) | modele **0/800** blok ulaşıyor | v2 — *indeksi değiştirir, yeniden indeksleme turuyla paketlenir* |
| **YB2** | M2b artık bir **eğitim** borcu — kapı yolu ölçülerek öldü | `h2b@k=4` **0,735 < 0,766** | v1 |
| **YB3** | `k`'nın **çekinme** ekseni **TANIMSIZ** — kör payda hakemi `k=10`'da kaynakların %57'sini görüyor (`SOURCE_CLIP=3500`), `k=4`'te %100'ünü | ≈**$0,30** ödenmedi | v1 raporu |
| **YB6** | 🔴 **Dağıtım istemi artefaktı YOK** | önsöz yalnız `gen_eval_grounded.py` içinde | **v1 — SERT ENGEL** |
| **ARA KAPI** | 🚨 **DÜŞTÜ** (2026-08-06): merge M2b **0,766** ↔ eşik **0,8649** → 9,9 p altında | paydalar eşit (77↔77) | **CP4-CP5 yetkisi YOK** · `v1.0` adı buna bağlı |
| ~~B2·B3·B5·B7~~ | kapandı | — | — |

## 6. NE YOK — ürünün asıl açıkları

1. 🔴 **Servis katmanı KOD OLARAK YOK** — `grep -rl "fastapi|uvicorn|flask|gradio" scripts/` → **0 sonuç.**
2. 🔴 **Modeli indiren kişi %68,4'ü üretemiyor** — önsöz dağıtılmıyor, retriever servis yoluna
   bağlı değil ⇒ ablasyon sütununu (%73,0) alıyor. **v1'in en sert engeli** (YB6).
3. 🔴 **Donmuş TEST hiç görülmedi** ve merge yapılandırması **DEV'de** seçildi.
4. 🔴 **Hakem paneli kurulmadı** — tek aile, κ yok, insan-κ DESCOPED.
5. 🔴 **Türkçe muhakeme yok** — düşünce izi **8/8 İngilizce**. Vatandaş ürünü için gerçek açık.
   ⚠️ Önce **istem katmanında bedavaya** denenmeli (ADR-0010 tuzağı: sade dille *eğitmek*
   denendi ve **doğruluğu düşürdü**).
6. 🔴 **Avukatlık Kanunu / hukuki sorumluluk sınırı** repo'da **hiç değerlendirilmemiş** —
   vatandaşa danışmanlık veren bir ürün için bu bir **ön koşul**, sonradan eklenecek bir madde değil.

## 7. KORUNAN ÇALIŞMA KURALLARI — çerçeve değişti, bunlar değişmedi

- **Sayı hatırlanmaz, kaynaklanır:** metrik · n · hakem · seed · sonucun yaşadığı dosya.
- **Her ölçüm aynı gün kayda geçer** (`docs/record/research_log/`, sıradaki **#62**);
  her büyük karar bir **ADR** (sıradaki **0063**; ⚠️ **0059 REZERVE**, altı yer atıf yapıyor).
- **Negatif/şaşırtıcı sonuç birinci sınıf** — kazançla aynı titizlikle yazılır. Bu hattın en
  değerli bulgularının birkaçı kendi planlarının çürütülmesidir.
- **Çelişki iki yerde işaretlenir**, sessizce üzerine yazılmaz. Eski değer **damgalanarak durur.**
- **Eşiği insan koyar ve koşudan ÖNCE ön-kayıtlar** (ADR-0050). Alet düzeltilir, **eşik oynatılmaz** —
  ama alet değişirse eşik **aynı formülle yeni birimde yeniden türetilir**.
- ⭐ **GÖZLE OKUMA BİR KAPIDIR.** 2026-09-06'da sayısal kapı (`0,1733 > 0,10`) bozuk ölçümü
  **geçirdi**; yakalayan şey *"10 kalemi gözünle oku"* adımıydı. **Yeni planlarda bu adım zorunlu.**
- `docs/record/yurutme-tuzaklari.md` — **her koşudan önce.** Hata sınıfı **çökme değil, sessiz
  yanlışlık**: düşmüş `--data`, kalibre edilmemiş red regex'i, eksik `--target-modules`,
  `set -e`'nin hatayı yutması, yarım kalan quantization'ın yine de dosya bırakması.
- **Base bir PARAMETREDİR, karar değil** (ADR-0026): hiçbir script varsayılan taşımaz, tanımsız
  base **erken patlar**. Sessizce yanlış modele düşmek saatlerce koşuyu görünmez çöpe çevirir.
- **Her kol HAM BASE'den bağımsız eğitilir** — `τ = θ_ft − θ_base` tanımı bunu şart koşar.
  Bir kolun üstüne eğitmek ardışık SFT üretir, task-vector değil. Merge **eşzamanlı k-yollu**.
- **Lisans temizliği:** yalnız açık kaynaklar (Mevzuat.gov.tr · Resmî Gazete · Yargıtay açık
  portal · Apache-2.0 HF setleri). **Lexpera / Kazancı ASLA** — telif zehri. PII maskelenir.
  Repo **Apache-2.0 ve public**.
- **Veri sert kuralı:** her veri setini **kullanmadan önce EDA ile doğrula.**
  `newmindai/EuroHPC-Legal` harika görünüyordu (43K, Apache-2.0), örnekleme çöp çıkardı
  (eşleşmeyen S-C, uydurma kanunlar, Osmanlıca) ve **reddedildi**. Kapsam: **yalnız yürürlükteki
  T.C. mevzuatı.** Yer gerçeği **Mevzuat.gov.tr**.
- **Yerel makine prototip, gerçek eğitim Modal'da.** Bulut kotası harcamadan önce hattı yerelde
  küçük modelle doğrula.
- **Güncellik kütüphanenin işi, modelin beyninin değil** — mevzuat değişince **indeks tazelenir,
  model DEĞİL.**

## 8. BÜTÇE — ölçülmüş

**Modal $29,19** kalan ($30 kredi, $0,81 harcandı) · **OpenRouter $10,26** kalan.
⭐ Ölçülmüş birim maliyet: **L4 ≈ $0,97/saat** (300 üretim / ~50 dk).
Reçetenin tamamı yeni bir base için ~**$7 / ~1 gün** (τ_g ~$4,4 + τ_a ~$1,3 + merge $0 + eval ~$1).
**Disiplinin asıl getirisi bu:** bir model değil bir **reçete** ürettik.

## 9. AÇIK İNSAN KARARLARI — yeni belgelerde taşınacak, sessizce kapatılmayacak

1. **ARA KAPI düşmüşken `v1.0` adı verilebilir mi?** (alternatif: `v0.2`)
2. **v1 harness'lı mı çıkar?** Çıkmazsa **yayımlanan sayı yeniden üretilemez.**
3. **Yeterlilik önsözü kalsın mı?** (§3.5 — kütleyi düşürüyor, A1/isabetsizliği yükseltiyor)
4. **LoRA adaptörleri HF'ye yüklensin mi?** Bugünkü karar *"yedeklenmiyor, bilinçli"* —
   ⚠️ 12B hattında adaptörler **kalıcı kaybedildi**, HF yayını ilk gerçek yedek olur.
5. **İndeks nasıl dağıtılır?** 80 MB HF dataset ↔ kurulumda üret (~10 dk)
6. **v2 barındırma:** yalnız self-host ↔ + hız-sınırlı vitrin ↔ hosted-first
   (⚠️ mahremiyet vaadini zayıflatır **ve** TR IP kısıtı bulutu kısıtlar)
7. **Avukatlık Kanunu / sorumluluk** — hukukçu görüşü gerekir (§6.6)
8. **arxiv:** hangi iddia savunulabilir? Bugün en güçlü hikâye **metodoloji**: cevaba bağlı payda ·
   hakem yığını kayması · yeniden-koşum gürültü tabanı · eşit sınav kapısı ·
   **ve bir çekinme dedektörünün istem rejimine bağımlı çıkması** (§3.5).
9. **Kaderi belirsiz belgeler** (§2) silinsin mi, yeniden yazılsın mı?

---

## 10. BU OTURUMDA ÜRETİLECEK

⚠️ **Önce `superpowers:brainstorming` kullan.** Tek başına tasarlama — bana soru sor.
Belirsizlik varsa **yorumları sun, sessizce birini seçme.** Varsayım yapıyorsan **söyle**.

Sıfırdan yazılacaklar:

1. **`PRODUCT.md`** — vatandaş kim · hangi soruyu soruyor · cevap neye benziyor · ürün neyi
   **vaat etmiyor** (hukuki tavsiye değil) · v1 ↔ v2 sınırı · **kabul ölçütleri**
2. **`ROADMAP.md`** — ölçülmüş açıklardan v1'e, v1'den v2'ye. Her adım: *ne · neden (hangi
   ölçülmüş boşluk) · `verify:` · bedel ($ ve süre) · bağımlılık*. Kritik yol işaretli.
3. **`docs/VISION.md`** — ürün vizyonu, tez dili tamamen çıkmış hâlde
4. **`docs/superpowers/specs/`** + **`plans/`** — v1 için spec ve `- [ ]` kutucuklu plan
   *(kutucuk yalnız `→ verify:` çıktısı **gerçekten alındıktan** sonra işaretlenir)*
5. **`TODO.md`** — aktif iş listesi
6. **arxiv çerçevesi** — yeni bir belge olarak (eski `PAPER_TARGET.md` silindi)
7. Son adım: **`CLAUDE.md` · `MODEL_CARD.md` · `README*.md`'nin kırık linklerini** yeni
   belgelere bağla.

**Bağlam için oku (salt okuma, yazmaya başlamadan):** `CLAUDE.md` ·
`docs/record/research_log/README.md` (özellikle **#56 · #60 · #61**) ·
`docs/adr/README.md` (özellikle **0058 · 0061 · 0062**) · `MODEL_CARD.md` ·
`docs/record/kollar.md` · `docs/record/yurutme-tuzaklari.md`.

**Bitince `DEVIR-PROMPT.md` silinebilir** — içeriği yeni belgelere dağılmış olacak.
