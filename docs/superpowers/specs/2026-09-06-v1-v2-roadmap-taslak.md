# HakHukuk — v1 / v2 Yol Haritası (TASLAK)

- **Tarih:** 2026-09-06 · **Durum:** taslak, insan onayı bekliyor
- **Üreten:** repo geneli tarama (CLAUDE.md · ROADMAP · MODEL_CARD · kollar.md · VISION ·
  research_log #39-#59 · 34 ADR · sprint3-part1 borç kuyruğu · açık plan · open_questions ·
  tuzaklar · BEDESTEN_API · VERI_PLANI · FINE_TUNING · `scripts/` · `outputs/eval/`)
- **Çerçeve:** tez değil **ürün**. v1 = çalışan model release'i · v2 = aynı modelin API'si.
  arxiv yan ürün.

> 🚨 **ŞERH — bu belge [#60](../../record/research_log/2026-09-06-hasat-kabul-olcutu-coktu.md)'tan
> ÖNCE yazıldı.** #60, B10 hasadının kabul ölçütünün çöktüğünü ölçtü (`exact_reject` doğru
> cevapları çekinme sayıyor; ön-kayıtlı D1 kapısı aslında düşüyor). Aşağıdaki **Faz 1** bu
> yüzden olduğu gibi koşulamaz: 1.1 ödendi (`99 passed, 1 xfailed`), 1.2 koşuldu ve
> **ölçütü çürüttü**, 1.3-1.8 **bloke**. Faz 1'e yeni bir sıfırıncı adım girer:
> *kabul ölçütünü onar ya da hasadı önsözlü koş* (§7.2'ye **S13** olarak eklendi).
> Belgenin geri kalanı — özellikle Faz 0, Faz 2-4, borç envanteri ve §7 — etkilenmiyor.

> **Bu belgede uydurulmuş sayı yok.** Her sayının yanında üretildiği dosya var. Kaynağı
> bulunamayan her nicelik **ÖLÇÜLMEMİŞ** damgalı.
> **Eşik önerileri taslağın önerisidir** — ADR-0050 gereği eşiği **insan** koyar ve koşudan
> **önce** ön-kayıtlar.

---

## 1. NEREDEYİZ — ölçülmüş ve kaynaklı

### 1.1 Artefakt
`HakHukuk-4B-v0.1` = `tgta_v1` = `tg_v1` + `ta_v1`, **ham TIES** (norm dengeleme KAPALI,
ADR-0052) · trim_k 0,2 · λ 1,0 · 224/224 tensör. Base `Qwen/Qwen3.5-4B`, commit `851bf6e8`.
Taşıyıcı `models/gguf/tgta_v1-q4_k_m.gguf`, **2,59 GiB**.
Kayıt `docs/record/kollar.md` · künye `outputs/eval/cp3d-merge/KUNYE_tgta_v1.json`.
‖τ_g‖ **10,4589** · ‖τ_a‖ **1,1806** (oran 8,87×).

### 1.2 Ürünün resmî sayısı — harness AÇIK, ana protokol (ADR-0058)
Rejim: `k=10` · indeks `mevzuat_bge_m3_s2` · yeterlilik önsözü AÇIK · thinking on 1024+512 ·
seed 3407 · klip 900 · hakem `gpt-4o-mini` (OpenRouter, `OpenAI` pinli) · DEV n=80.

| eksen | değer | kaynak |
| :--- | ---: | :--- |
| `recall@10` | **0,8750** (70/80) | `outputs/eval/olcum-bi/harness_tablo.json` |
| coverage | **0,7625** | aynı |
| A1 (cevaplanan-only) | **0,8229** | aynı + `rescore_answered` çapraz doğrulaması |
| A1 · altın getirilen | **0,8705** | aynı |
| **sadık-cevap KÜTLESİ** | **%62,8** | aynı |
| uydurulmuş madde no | **0/83** | aynı |
| katı kapı reddi | 3/80 | aynı |
| **B10 — altın bağlamdayken çekinme** | **14/80** | aynı |
| **B1 — gerçek ama soruya uymayan madde** | **5/80** | #56 §5 (D1) |

Önsözsüz ablasyon (`outputs/eval/s2-harness-k10-etiketli/`): kütle **%61,3** · A1 0,8042 ·
A1-altın 0,8616 · B10 **16/80** · B1 7/80 · uydurulmuş 0/118.

### 1.3 Tavan — harness KAPALI (rakip DEĞİL)
`outputs/eval/cp3-supurme-ham/*_tg_ta_ham_th_*`: kütle **%71,6** · A1 **0,9087** ·
coverage 0,7875 · aşırı-red **0,212 (17/80)** · M2 **0,833ᴷ⁴ (55/66)** · M2b **0,766ᴷ³** ·
714 tok/cevap. ⚠️ KAPALI'da altın madde bağlama **kurgu gereği** konur — **tavan**, kıyas değil.

10,2 puanlık KAPALI↔AÇIK açığı ayrıştırıldı (⚠️ **önsözsüz** çıpayla; ADR-0058 sonrası açık
**8,8 puan** ve **yeniden ayrıştırılmadı**): ≈5,1 p erişim ıskası + ≈4,5 p dikkat dağılması.
Çekinme iki tarafta aynı (0,771 ↔ 0,787) → **aşırı-red harness'ın suçu değil, modelin özelliği**.

### 1.4 🚨 Rakip — ürün rejiminde İLK KEZ ölçüldü (2026-08-06) ve hedef bayatladı
Kaynak `outputs/eval/g2-fl-harness/OZET.md` (eşit sınav kanıtı: üç öznede `recall@10` birebir 0,875).

| eksen | **BİZ** | 3.1 FL | **3.5 FL** |
| :--- | ---: | ---: | ---: |
| M1 kütle (AÇIK) | %62,8 | %61,7 | **%69,5** |
| A1 · cevaplanan | **0,8229** | 0,7054 | 0,7940 |
| A1 · altın getirilen | **0,8705** | 0,7835 | 0,8607 |
| aşırı-red (↓ iyi) | %23,75 | **%12,5** | **%12,5** |
| altın bağlamda ama sustu | 14/80 | 8/80 | **6/80** |
| M2b Rej* (önsözlü, k=4) | 0,809 | 0,809 | **0,926** |
| $/cevap (girdi+çıktı) | **$0** (yerel) | $0,002074 | $0,002175 |

**Okuma:** *sadakatte birinciyiz, çekinmede rakibin iki katı gerideyiz.* ROADMAP'in
*"önce 3.1 FL'ı geç"* hedefi **geçildi (+1,0 p, dar)** ama **3.5 FL bizi 6,7 puan geçiyor** →
hedef cümlesi bayat (borç **YB5**).
⛔ *"Aşırı-red kapansa %72,0'a çıkardık"* cümlesi **TAVAN/VARSAYIMSAL** damgalı; rakip kıyası
ondan kurulmaz.

### 1.5 🚨 ARA KAPI 2026-08-06'da DÜŞTÜ — CP4-CP5 yetkisi YOK
Ön-kayıtlı olan **formüldü**, sayı değil:
```
eşik  = 0,90 × base M2b 0,961 = 0,8649
merge = 0,766   →  🔴 9,9 puan altında.  Eski 0,887 eşiğine karşı da DÜŞTÜ.
paydalar EŞİT (77 ↔ 77) → kıyas geçerli
```
`outputs/eval/cp2-r-kor-payda/ara_kapi_esikleri_2026-08-06.json` · #58. ⛔ ADR-0050 gereği
**alet** düzeltildi, eşiğe dokunulmadı. **CP4-CP5 harcamasını yetkilendiren kapı buydu; yetki yok.**
⚠️ ADR-0052'nin hükmü (*ham TIES ≫ norm-dengeli*) **etkilenmedi**: sıçrama +0,26 değişmedi.

### 1.6 Donanım — MODEL_CARD *"hesap, ölçüm değil"* diyor ama ÖLÇÜM VAR
`outputs/eval/_artefakt/vram_stack.json` (`measure_vram_stack.py`, Q4_K_M, KV q8_0, **base GGUF**):

| ctx | sunucu VRAM | tepe |
| ---: | ---: | ---: |
| 4.096 | **3,09 GiB** | 4.530 MiB |
| 32.768 | 3,70 GiB | 5.146 MiB |
| 131.072 | 5,76 GiB | 7.259 MiB |

⚠️ Ölçüm `q35-4b-q4_k_m.gguf` üzerinde; `tgta_v1` aynı boyut sınıfında ama **kendisi ölçülmedi** —
≤8 GB yumuşak kapısının **ucuza kapanabilecek** borcu ($0, ~15 dk).

### 1.7 Neyin ölçülmediği
- ⛔ **Frozen TEST (`data/eval/canon/`, 40+35) hiç görülmedi.** Merge yapılandırması **DEV'de**
  3 varyant arasından seçildi.
- ⛔ **Hakem paneli kurulmadı** — tüm A1/Rej sayıları **tek aile** (`gpt-4o-mini`), κ yok.
- ⛔ **`k=10`'un çekinme ekseni TANIMSIZ** — kör payda hakemi k=10'da kaynakların %57'sini
  görüyor (`SOURCE_CLIP=3500`), k=4'te %100'ünü (KARAR-4, ADR-0057). Bedel ≈$0,30, ödenmedi.
- ⛔ **M3 paydası hâlâ modele bağımlı** — cp09'da `54 · 56 · 39`, oysa ADR-0048 m.2 gereği 80/80.
- ⛔ **A1 sütunu yığın-eşleşmesiz** (base/FL openai-doğrudan + ADR-0041 öncesi istem);
  ayrıştırma **kalıcı olarak imkânsız** (OpenAI kredisi yok).
- ⛔ **DEV n=80 için güç analizi yok.** Elde yalnız hakem gürültü tabanı (**0,3 A1 puanı**);
  ikili oran eksenlerinin kuantumları 1,52 / 1,30 / 1,25 puan.
- ⛔ **Canlı mevzuat ürün yolunda kullanılmıyor** — sözleşme 4/4 GEÇERLİ, güncellik iddiası
  **kanıtlanmamış** (B6).
- ⛔ **Servis katmanı kodu YOK** — `grep fastapi|uvicorn|flask|gradio` → **0 sonuç**.
- ⛔ **`τ_a` v2 turu YARIDA** — **22/71 kutucuk**, 41 commit.

### 1.8 Belgede bulunan tutarsızlıklar (ucuz)

| # | ne | kanıt |
| :-- | :--- | :--- |
| D-a | **`README.md`/`README.tr.md` hâlâ ADR-0058 ÖNCESİ çıpaları taşıyor** (%61,3 · 16/80 · 7/80 · 0/118). `grep '62.8' README*` → **0 sonuç**. Dışa dönük ilk belge resmî sayıyı söylemiyor | `README.md:60-77` |
| D-b | **MODEL_CARD "calculated, not measured"** — oysa `vram_stack.json` var | §1.6 |
| D-c | **Hiçbir script `KUNYE.json` yazmıyor** — elle yazılmış; `s2-harness-k10-etiketli/`'de künye **hiç yok** (tuzak 6.12) | plan §KÜNYE |
| D-d | **`SUFFICIENCY_PREAMBLE` tek yerde:** `scripts/gen_eval_grounded.py`. Dağıtım artefaktı **yok** → modeli indiren **ablasyon** sayısını (%61,3) alır | plan §YENİ BORÇ |
| D-e | **ADR-0059 rezerve ama YAZILMADI** — altı yer atıf yapıyor | `docs/adr/` |
| D-f | **`data/eval/canon/` git'te ve repo PUBLIC** — "donmuş"luk gizlilikle değil **usulle** korunuyor | `git ls-files data/eval` |

---

## 2. AÇIK BORÇ ENVANTERİ

**Ürün borçları (sprint3-part1 kuyruğu)**

| # | borç | ölçülen büyüklük | nerede | engelliyor | iş |
| :-- | :--- | :--- | :--- | :-- | :--- |
| **B10** ⭐ | **Aşırı-red** — altın bağlamdayken çekinme | **14/80** (ablasyon 16/80) · `k`'dan bağımsız (14→15→16) · KAPALI 17/80 · **rakip 8 ve 6** | sprint3-part1 · ROADMAP 2.1c | **v1** | eğitim turu ~$1,6 GPU + $0,2 hakem; tur **açık, yarıda**, ⚠️ #60 ile **bloke** |
| **B1** | Gerçek ama soruya uymayan madde | **5/80** (ablasyon 7/80) | sprint3-part1 · ADR-0055 | v1 (şerh) | eksen belirlendi, kod açılmadı |
| **B4** | `τ_a` merge'de seyreliyor (0,987 → 0,766, −22,1 p) | ‖τ_a‖=1,18 · 70 adım @1e-5 | sprint3-part1 | v1 (dolaylı) | **B10 turunda YASAK** (spec §10) — ayrı tur |
| **B6** | **Canlı bedesten katmanı yok** | sözleşme 4/4 GEÇERLİ, ürün kullanmıyor | BEDESTEN_API | **v2** | ürün işi; TR IP şart |
| **B8** | Katı kapı tek karakterlik yazım hatasına takılıyor | 1/80 · eğri ölçüldü, tolerans **BENİMSENMEDİ** | sprint3-part1 · #56 | v1 (düşük) | ~$0, karar insanın |
| **B9** | Tablo/cetvel parçaları madde diye indeksli (~7.966 satır) | modele **0/800** blok ulaşıyor | sprint3-part1 | v2 | indeksi değiştirir → yeniden indeksleme turuyla paketlenir |
| ~~B2·B3·B5·B7~~ | kapandı | — | — | — | — |

**Ölçüm/metodoloji borçları**

| # | borç | durum | engelliyor | bedel |
| :-- | :--- | :--- | :-- | ---: |
| **YB2** | M2b artık **eğitim** borcu (`h2b@k=4` 0,735 < 0,766) | açık | v1 | B10 turuna gömülü |
| **YB3** | `k`'nın çekinme bedeli **TANIMSIZ** (`SOURCE_CLIP=3500`) | açık, fiyatlı | v1 raporu | **≈$0,30** |
| **YB4** | Üç-aileli hakem paneli + aile dışlaması | açık | v1 şerhi | ÖLÇÜLMEMİŞ |
| **YB5** | ROADMAP hedef cümlesi bayat (3.5 FL 6,7 p önde) | açık | v1 anlatısı | $0 |
| **YB6** | **Dağıtım istemi artefaktı yok** (D-d) | açık | **v1 — sert engel** | ~1 oturum |
| **YB7** 🆕 | **Hasat kabul ölçütü bozuk** — `exact_reject` önsözsüz rejimde doğru cevapları red sayıyor | [#60](../../record/research_log/2026-09-06-hasat-kabul-olcutu-coktu.md) | **Faz 1 — sert engel** | ~1 oturum + yeniden pilot |
| OQ-1 | M3 paydası tanım gereği 80/80 olmalı | açık | v1 raporu | **$0** |
| OQ-2 | İkili oran çözünürlük sınırı yazılmadı → M2'de −0,015 **tek kalem** | insan kararı | v1 iddiaları | $0 |
| OQ-3 | Önsözün **atıf yoğunluğu bedeli**: iddia 268→206 (−%23), atıf 118→83 (−%30) | ölçüm var, yorum yok | v1 | insan kararı |
| OQ-4 | `cp2c_kabul.sh` hakem yığını varsayılanı `openai` | açık | v2 hijyeni | $0 |
| OQ-5 | `harness_tablo.py:137` `id` ↔ indeks karışıklığı — `--resume`'da **sessizce yanlış coverage** | gizil | v2 | önce düşen test |
| OQ-6 | Açılış-yeterlilik kuralının maruziyeti **~8 kat asimetrik** (39/80 ↔ 5/80) | kayda geçti | rakip kıyası | $0 |
| **ARA KAPI** 🚨 | **DÜŞTÜ** — 0,766 < 0,8649 | yürürlükte | **CP4-CP5 yetkisi YOK** | — |
| D-a…D-f | belge tutarsızlıkları (§1.8) | yeni | v1 | $0 · ~1 oturum |

---

## 3. v1 RELEASE — *"pratik olarak çalışan model"* nedir

### 3.1 Tanım (öneri, gerekçeli)

> **v1 = bir kullanıcının kendi makinesine indirip, mevzuat metnini KENDİ yapıştırmadan Türkçe
> bir hukuk sorusu sorup ya kaynaklı bir cevap ya da gerekçeli bir red alabildiği ve yayımlanan
> sayıyı kendi makinesinde yeniden üretebildiği sürüm.**

**Model-only v1 neden reddediliyor — ölçülmüş gerekçe:**
1. Resmî sayı (%62,8) **retriever + yeterlilik önsözü** rejiminde üretiliyor (ADR-0058). Bugün
   modeli indiren ikisine de sahip değil → **ablasyon sayısını** alır (%61,3, D-d).
   *Yayımlanan sayıyı kimsenin üretemediği bir release, repo'nun kendi disiplininin ihlalidir.*
2. `MODEL_CARD`/`README` bunu zaten itiraf ediyor: *"The retrieval layer exists and is measured,
   but it is not packaged into the serving path."* — release notu değil, **borç beyanı**.
3. Retriever GPU'ya girmiyor (CPU, 759 ms/sorgu, indeks 80 MB) → paketlemenin donanım maliyeti **yok**.

⚠️ v1 **web arayüzü veya API değildir** (o v2). Taşıyıcısı tek komutluk CLI:
`hakhukuk sor "..."` → retriever + önsöz + llama.cpp + atıf doğrulayıcı.

### 3.2 Asgari kabul ölçütleri

**A. Model kalitesi** — ana protokolde (AÇIK · k=10 · S2 · önsözlü), DEV:
```
A1  GERİLEME YOK:   kütle ≥ %62,8 · A1(cevaplanan) ≥ 0,8229
                    M2b Rej*(önsözlü h2b@k=4) ≥ 0,809 · M2(payda 66) ≥ 0,833
                    KAPALI kütle ≥ %71,6
A2  B10 DÜŞTÜ:      aşırı-red (AÇIK) ≤ 11/80     ← turun KENDİ ön-kayıtlı tahmini 8-11/80
A3  KÜTLE İLERLEDİ: kütle ≥ %65,0                ← A2'nin mekanik sonucu (3 kalem ≈ +3,75 coverage p)
A4  GEÇERLİLİK:     kesik ≤ %5 · ALTIN_SIZAN = 0 · künye tam
```
**Neden daha yükseği değil:** 3.5 FL'ı geçmek v1 ölçütü **yapılmıyor** — açık **6,7 puan** ve
kapanacağının tek dayanağı **TAVAN/VARSAYIMSAL** damgalı karşıolgu. Sürüm kapısını damgalı bir
tavana bağlamak, repo'nun altı kez düzelttiği hatanın aynısı olur.
A2'nin ≤11 olması keyfi değil: spec sayı görülmeden **8-11/80** yazdı; üst uç kapı, alt uç bonus.
M2 ekseni "gerileme yok"tan fazlasını iddia etmiyor (kuantum 1,52 p; Gemini açıklığı **tek kalem**).
A1 ekseni kapı değil şerh: coverage-eşleşmiş alt kümede (n=40) base **0,9525** ↔ biz **0,9563** ↔
FL 0,9813, 33/40 berabere — **ham A1 az cevaplamayı ödüllendiriyor**.

**B. Sürüm kabul koşusu — frozen TEST, bir kez**
```
B1  data/eval/canon/ (40+35) BİR KEZ; kabul ölçütü koşudan ÖNCE ön-kayıtlı
B2  🚨 v2.0'ın YENİ donmuş seti B1'DEN ÖNCE üretilir (~$1 + yarım gün)
B3  ⚠️ İNSAN KARARI: canon zaten PUBLIC. HF'ye yüklenirse gelecek base'lerde kontaminasyon riski
```

**C. Dağıtım ve çalışabilirlik**
```
C1  GGUF Q4_K_M (2,59 GiB) + bf16 merged + LoRA adaptörleri HF'de
    ⚠️ kollar.md'nin "adaptörler yedeklenmiyor — bilinçli" kararını DEĞİŞTİRİR → ADR
C2  Ölçülmüş donanım satırı: measure_vram_stack.py tgta_v1'de koşulur (D-b, $0)
C3  Dağıtım istemi artefaktı (YB6): tek kaynak, hem eval hem servis okur
C4  hakhukuk sor "<soru>": retriever(S2, k=10) + önsöz + llama-server + atıf doğrulayıcı
C5  İndeks dağıtımı (80 MB): HF dataset mi, kurulumda üretim mi → İNSAN KARARI
C6  Çevrimdışı kurulum belgelenir (mahremiyet vaadiyle tutarlılık)
```

**D. Yeniden üretilebilirlik**
```
D1  KUNYE.json'u SCRIPT yazar (D-c) — elle yazılan künye künye değildir
D2  "hangi komut hangi sayıyı üretir" tablosu — MODEL_CARD'ın her hücresi için
D3  requirements.lock.txt + llama.cpp commit'i pinlenir
```

**E. Belgeler ve lisans**
```
E1  README + README.tr → ADR-0058 çıpaları (D-a)
E2  MODEL_CARD Limitations'a EKLENECEK (hiçbiri "future work" diye yumuşatılmaz):
      · ARA KAPI DÜŞTÜ (0,766 < 0,8649); merge yapılandırması tabanlara karşı sınanmadı
      · 3.5 FL kütlede 6,7 p önde; aşırı-red bizde rakibin ~2 katı
      · tek hakem ailesi, κ yok, insan-κ DESCOPED
      · tek boyut / tek base → dışsal geçerlilik açığı KAPANMIYOR
      · ADR-0018'in eğri şartı karşılanmadı (tek nokta)
      · önsözün atıf yoğunluğu bedeli (OQ-3)
E3  LICENSE/NOTICE temiz: Apache-2.0, base Apache-2.0, veri Mevzuat + iki Apache-2.0 HF seti,
    ticari kaynak SIFIR — bu kalemde iş YOK (doğrulandı)
E4  "Avukat değildir" uyarısı model kartında + CLI'ın HER çıktısında (dipnotta değil)
```

**F. ÇIKMAMASI gerekenler**
```
F1 ⛔ Frozen TEST'in cevapları/analizi     F2 ⛔ .env, API anahtarları, Modal token'ı
F3 ⛔ Parite iddiası ("Gemini'yi geçtik" tek başına hiçbir eksende)
F4 ⛔ Harness KAPALI sayıların rakip sütunuyla yan yana konması (TAVAN, ADR-0057)
F5 ⛔ %62,8'in "harness'sız da alınabilir" ima edilmesi
F6 ⛔ Emekli birimdeki sayılar damgasız (0,877 / 0,840 / 0,893 ~20 belgede)
```

---

## 4. v2 RELEASE — API katmanı

### 4.1 Servis mimarisi — üç seçenek

| eksen | **(a) llama.cpp server + FastAPI** | **(b) vLLM (bf16/AWQ) + FastAPI** | **(c) Hosted (Modal/Runpod)** |
| :--- | :--- | :--- | :--- |
| artefakt | **ölçülen artefaktın ta kendisi** (Q4_K_M GGUF) | ⚠️ **BAŞKA artefakt** — kuantizasyon davranışı değiştirir | seçime bağlı |
| ölçüm sürekliliği | ✅ tüm çıpalar bu yığında | 🔴 **bütün çıpalar yeniden türetilir** | yığına bağlı |
| donanım | 3,09 GiB @ ctx 4096 (**ölçüldü**) | ~9-10 GiB (bf16, ölçülmedi) | kiralık |
| eşzamanlılık | zayıf; `-np N` KV'yi böler ⚠️ **çıpalar tek slotta ölçüldü** | güçlü (continuous batching) | otomatik |
| maliyet | **$0 marjinal** | $0 marjinal, büyük donanım | **~$100-300/ay süregelen** |
| mahremiyet | ✅ tam yerel — **iki yapısal üstünlükten biri** | ✅ yerel | 🔴 vaadi zayıflatır |
| kurulum | orta (`setup_llamacpp.sh` var) | zor (CUDA/vLLM sürüm cehennemi) | ✅ kolay |

**Öneri: (a) birincil · (c) yalnız hız-sınırlı vitrin · (b) reddedilmez, ertelenir.**
Gerekçe ölçülmüş: **KARAR-6 bu soruyu zaten sordu ve Modal/vLLM'i reddetti** — *"farklı çıkarım
yığınıyla toplarsak başka bir modelin davranışını ölçmüş oluruz; kuantizasyon davranışı değiştirir,
sessiz sapma."* Aynı argüman servis için geçerli: **ölçtüğümüz modeli servis etmezsek, yayımladığımız
sayı servisin sayısı değildir.** (b) bir gün gerekirse **kendi kapısı** olur: aynı DEV koşusu iki
yığında koşulur, fark **ölçülür**.
⚠️ **`-np` borcu v2'ye devrediyor** — tüm çıpalar tek slotta üretildi.
🆕 Ve bu artık teorik değil: [#60](../../record/research_log/2026-09-06-hasat-kabul-olcutu-coktu.md)
pilotunda `-np 1` ↔ `-np 8` kabul kümeleri **Jaccard 0,5278**, kesişimin 19'unda yalnız **3'ü**
birebir aynı metin (⚠️ bozuk ölçütle toplandı, hüküm kurulmadı — ölçüt onarılınca yeniden koşulmalı).

### 4.2 RAG/harness serviste nerede durur
```
istemci → FastAPI ─┬─ retriever (CPU: BM25 + bge-m3, RRF, S2 indeks 80 MB, 759 ms)
                   ├─ yeterlilik önsözü (TEK KAYNAK — YB6 artefaktı)
                   ├─ llama-server (GPU: 3,09 GiB @ ctx 4096)  ← tek GPU sakini
                   ├─ atıf doğrulayıcı (deterministik, hakemsiz, MULGA dâhil)
                   └─ red kapısı (ADR-0038 katı)
```
**Bağlayıcı:** *harness GPU'ya girmez* (CLAUDE.md) — sığar/sığmaz farkını yaratan tek şey bu.
⚠️ **Atıf doğrulayıcı sunumda ürünün ASIL farkıdır**, skor özelliği değil: uydurulmuş madde no
**0/83**, yani yakalayacağı sınıf zaten boş. Değeri **denetlenebilirlik**te: maddeler ✅ işaretli
ve `mevzuat.gov.tr`'ye tıklanabilir; **MULGA** hükmü mülga maddeyi reddeder (DEV'de 0 kez tetiklendi —
bir **ürün-güvenliği** özelliği).

### 4.3 Canlı mevzuat (B6)
- Sözleşme çalışıyor (4/4 GEÇERLİ), **TR IP şart** (gov firewall yurtdışı/VPN'i bloke ediyor) —
  ⚠️ **bulut barındırmayı da kısıtlar**: TR-dışı VPS bedesten'e erişemeyebilir.
- **Sıra bağlayıcı:** *mevzuat değişti → İNDEKSİ tazele, modeli DEĞİL.*
- v2'nin işi: bedesten → korpus farkı → S2 alanlarıyla yeniden indeksleme →
  **`recall@10` yeniden ölçülür** (indeks değişince `k` kıyası geçersizleşir; B9 ile aynı tur).

### 4.4 Vatandaş dili — istem katmanı (ADR-0010 tuzağı)
- ⚠️ **Sade dille EĞİTMEK denendi ve doğruluğu düşürdü** (ADR-0010, yürürlükte). Sadeleştirme
  **sunum katmanıdır**.
- İki kip: `uzman` (varsayılan, ölçülen çıktı) ↔ `vatandaş` (aynı cevap + sadeleştirme istemi).
  **Ölçüm daima `uzman` kipinde.**
- 🚨 **Yeterlilik önsözünün yan etkisi ürün kararı doğuruyor:** cevap *"Verilen kaynaklar bu soruyu
  cevaplamaktadır…"* diye başlıyor — ölçüm için değerli, vatandaş için gürültü. Öneri: **üretimde
  tut, sunumda rozete çevir** (✅/⛔ yeterlilik rozeti). Karara bağlanmadı.
- **Türkçe muhakeme** (iz 8/8 İngilizce) bir **ürün** açığı — **önce istem katmanında bedavaya dene**.

### 4.5 Operasyonel

| eksen | öneri | gerekçe/ölçüm |
| :--- | :--- | :--- |
| rate limit | kullanıcı başına eşzamanlı **1 üretim** | tek GPU slotu; `-np` rejimi çıpadan kaydırır |
| önbellek | **retriever** ve **atıf doğrulama** önbelleklenir; **model çıktısı önbelleklenmez** | doğrulayıcı deterministik; model çıktısı sunucu rejimine duyarlı |
| ⛔ istem önbelleği | **AÇILMAZ** | ölçüldü: `extract` 828 tok < 1024 eşiği; kazanç ~%11 ≈ $0,03. Asıl sebep maliyet değil: **hakem istemi bu repo'daki HER sayının tanımı** (ADR-0041 base A1'ini 2,77 p oynattı) |
| maliyet | yerel çıkarım **$0**; dış maliyet yalnız hakem (koşu başı ≈$0,04) | `llm_client.PRICE` |
| gözlemlenebilirlik | her cevaba **koşu künyesi**: model sürümü · indeks sürümü · k · önsöz · getirilen madde id'leri | *"bu sayı neyin sayısı"* kuralının ürün karşılığı |
| sağlamlık | 🐞 **sessiz-ölüm** serviste de var: HTTP 200 + `finish_reason='error'` + boş içerik → geri-çekilmeli retry + **boş cevap = hata** | Görev 2'de iki koşu 22. ve 32. kalemde öldü |

### 4.6 Hukuki sorumluluk katmanı
```
1. Her cevabın YANINDA (dipnotta değil): "Bu hukuki tavsiye değildir."
2. Her madde atfı mevzuat.gov.tr'ye tıklanabilir → doğrulama kullanıcıya devredilir
3. MULGA/yürürlük rozeti: mülga maddeye dayanan cevap ÜRETİLMEZ
4. Bilgi kesim tarihi + indeks tarihi HER cevapta görünür
5. Red GÖRÜNÜR ve gerekçeli — "kaynaklar yetmiyor" başarısızlık değil, ürünün VAADİ
6. Kişisel veri: sorular yerelde kalır; log varsayılan KAPALI
7. ⚠️ İNSAN/HUKUKÇU KARARI: Avukatlık Kanunu sınırı — repo'da hiç değerlendirilmemiş
```

---

## 5. SIRALI YOL HARİTASI

**[K]** kritik yol · **[P]** paralel · süreler **oturum** cinsinden.

### FAZ 0 — Ucuz düzeltmeler (Faz 1'i BEKLETMEZ)

| # | iş | neden | verify | bedel |
| :-- | :--- | :--- | :--- | ---: |
| 0.1 **[P]** | README + README.tr çıpalarını ADR-0058'e taşı | D-a: dışa dönük belge %61,3 diyor | `grep -c '62,8\|62.8' README*` > 0; 61,3 yalnız *ablasyon* damgasıyla | $0 · ½ |
| 0.2 **[P]** | `measure_vram_stack.py`'yi `tgta_v1`'de koş | D-b | `vram_stack.json`'da `tgta_v1` satırı | $0 · ¼ |
| 0.3 **[P]** | M3 paydasını 80/80 yap, yayılımı damgala | OQ-1: kayıtta üç yanlış sayı | üç kolda payda 80; eski değerler damgalı | **$0** · ½ |
| 0.4 **[P]** | `kunye_yaz` bir **script** olur | D-c (tuzak 6.12) | yeni koşuda `KUNYE.json` otomatik | $0 · ½ |
| 0.5 **[P]** | ADR-0059 yazılır | D-e: altı yer atıf yapıyor | `docs/adr/0059-*.md` var | $0 · ½ |
| 0.6 | `SOURCE_CLIP` borcunu öde | YB3: `k=10` çekinme ekseni TANIMSIZ | payda hakemin **gördüğü** bağlamla eşleşiyor | **≈$0,30** ⚠️ tüm tarihsel `verdict`leri kıyaslanamaz kılar → insan onayı |

### FAZ 1 — B10 turunu bitir **[K]**
Plan: `docs/superpowers/plans/2026-08-06-asiri-red-tau-a-v2.md` — **22/71 kutucuk**.

| # | iş | verify | bedel | durum |
| :-- | :--- | :--- | ---: | :--- |
| 1.0 🆕 **[K]** | 🚨 **Kabul ölçütünü onar** (#60 / YB7) — `exact_reject` önsözsüz dalı düzeltilir **ya da** hasat önsözlü koşar → **S13** | gözle okunan 10 kabulün **10'u** gerçek çekinme | $0 · 1 oturum | 🔴 **AÇIK** |
| 1.1 | `pytest tests/ -q` yeşil | **99 passed, 1 xfailed** | $0 | ✅ **ödendi 2026-09-06** |
| 1.2 | Pilot iki kez (KARAR-6) | np1 26/0,1733/2.174,9 s ↔ np8 29/0,1933/845,4 s · **2,57×** · Jaccard 0,5278 · birebir 3/19 | $0 · ~50 dk | ⚠️ **koşuldu, ölçütü ÇÜRÜTTÜ** — onarım sonrası yeniden |
| 1.3 | Görev 4 üretim hasadı | tekil, şema doğrulanmış havuz; süzgeç 13.350→12.914 ✅ | ~$1,5 (Modal L4, ~2 sa @ np8) | ⏸ **bloke (1.0)** |
| 1.4 | Görev 5-6: ORPO paketleme + `τ_a` v2 eğitimi | `‖τ_a v2‖` = 1,18 ±%25 | **~$1,60 GPU** | ⏸ |
| 1.5 | 🛑 **Görev 7 KOL KAPISI** | `aşırı-red < 0,425 ∧ M2b ≥ 0,95 ∧ A1 ≥ 0,88` — **BAŞARISIZ → tur DURUR** | ~$0,10 | ⏸ |
| 1.6 | Görev 8 merge (`tgta_v2`) — ham TIES **verili değil**, DEV'de süpürülür | 224/224 · GGUF 2,59 GiB bandında | $0 | ⏸ |
| 1.7 | 🛑 **Görev 9 ÜRÜN KAPISI** | `kütle > %62,8 ∧ B10 < 14/80 ∧ M2b ≥ 0,809` | ~$0,14 | ⏸ |
| 1.8 | Görev 10 kayıt (**BAŞARISIZ dâhil**) | ADR + kayıt + `kollar.md` | $0 | ⏸ |

**Tur toplamı ~$2,0-2,5.** Bakiye $10,26.
⚠️ **Ön-kayıtlı tahminler:** B10 → **8-11/80** · kütle(AÇIK) → **%64-66** · kütle(KAPALI) → **%75-79** ·
Δ(önsöz) → +0,0…+0,7 p. Tutmazsa **öyle** kaydedilir.

### FAZ 2 — v1 hazırlığı

| # | iş | neden | verify | bedel |
| :-- | :--- | :--- | :--- | ---: |
| 2.1 **[K]** | 🚨 **v2.0'ın YENİ donmuş setini ÜRET** | sonra üretilirse yetişmez | 40+35, CANON protokolü, künyeli, görülmemiş | ~$1 · ½ gün |
| 2.2 **[K]** | YB6 — dağıtım istemi artefaktı | D-d | eval ve servis **aynı** dosyadan okuyor | $0 · 1 |
| 2.3 **[K]** | `hakhukuk sor` CLI | v1 tanımı §3.1 | **temiz konteynerde**, yalnız belgeyle çalışıyor | $0 · 2-3 |
| 2.4 **[P]** | B8 kararı (tolerans) | risk tarafında **0 gözlem** | karar yazılı (katı kalırsa da) | $0 |
| 2.5 **[P]** | Türkçe muhakeme — **önce istem katmanı** | ürün açığı (8/8 İngilizce) | 20 çıktı gözle; A1 gerilemiyor | ~$0,04 |
| 2.6 **[P]** | OQ-2 çözünürlük sınırı | M2'de −0,015 tek kalem | kural yazılı | $0 |
| 2.7 **[P]** | OQ-3 önsözün atıf bedeli — ürün yorumu | denetlenebilirlik vaadi | kural yazılı | $0 |
| 2.8 | Repro tablosu (D2) + pinler | v1 §D | her hücre için tek satır komut | $0 · 1 |

### FAZ 3 — v1 RELEASE **[K]**

| # | iş | verify | bedel |
| :-- | :--- | :--- | ---: |
| 3.1 | 🛑 **Sürüm kabul koşusu — frozen TEST, BİR KEZ** | ölçüt **koşudan önce** ön-kayıtlı; kesik ≤%5; künye tam | ~$0,10 |
| 3.2 | MODEL_CARD + README + Limitations (§3.2/E2) | ARA KAPI · 3.5 FL · tek hakem ailesi · tek boyut yazılı | $0 |
| 3.3 | HF yayını: GGUF + bf16 + **adaptörler** + veri + eval seti | indirilip çalışıyor; ⚠️ adaptör yayını **ADR** ister | $0 |
| 3.4 | `v1.0` etiketi | §3.2 A/B/C/D/E'nin **hepsi** ✅ | $0 |

⛔ **A1-A4 karşılanmazsa `v0.2` çıkar, `v1.0` çıkmaz.**

### FAZ 4 — v2 (API) **[K]**

| # | iş | verify | bedel |
| :-- | :--- | :--- | ---: |
| 4.1 | FastAPI: `/ask` · `/sources` · `/health` · künye alanı | temiz konteynerde yalnız belgeyle kurulum | $0 · 3-4 |
| 4.2 | Sunum: atıf paneli (tıklanabilir), **görünür red**, yeterlilik rozeti, vatandaş kipi | yasal uyarı arayüzde, dipnotta değil | $0 · 2-3 |
| 4.3 | Docker Compose + SQLite + çevrimdışı kurulum | tek `up`; Windows GPU geçirme belgeli | $0 · 2 |
| 4.4 **[P]** | **B6 — canlı bedesten** | sözleşme yeniden sınanır (⚠️ TR IP) | $0 |
| 4.5 **[P]** | **B9 + yeniden indeksleme** (4.4 ile aynı tur) | `recall@10` yeniden ölçülür | ~$0,04 |
| 4.6 | Ölçüm rejimi ↔ servis rejimi eşitliği | servis `-np`/ctx ayarında DEV koşusu tekrarlanır, sapma **ölçülür** | ~$0,04 |

**Kritik yol:** `1.0 → Faz 1 → 2.2 → 2.3 → 3.1 → 3.4 → 4.1 → 4.2/4.3`
**Paralel:** Faz 0'ın tamamı · 2.1 · 2.4-2.7 · 4.4/4.5
**v1 sonrası eğitim sırası:** B1 → B4 → A1 açığı → 8B/12B port.
⚠️ **önce 4B'yi tavana yaklaştır — reçete yukarı taşınır, ölçümler aşağı taşınmaz.**

---

## 6. arxiv — yan ürün

**Bugün savunulabilir iddialar:**
1. ✅ *"İki çatışan beceri ayrı kollarda eğitilip TIES ile birleşince ikisi de kısmen korunuyor."*
   `τ_g` tek başına M2b **0,506** · `τ_a` tek başına M1 kütle **%41,2** · merge **%71,6 / 0,766** —
   grounding **tam** korunmuş, çöküşün **%57'si** onarılmış.
2. ✅ *"Ön-kayıtlı bir tasarım kararı ölçümle tersine çevrildi."* ADR-0036 → ADR-0052.
3. ✅ *"Deterministik atıf doğrulama fabrikasyonu değil transkripsiyonu yakalar."* 0/83 ve 0/118 —
   kurulduğu sınıf **boş**; asıl hata *başka bir gerçek maddeden* cevaplama (5/80).
4. ✅ *"Aşırı-red baskın kayıp kanalıdır ve erişimle kapanmaz."* 14/80, `k`'dan bağımsız.
5. ✅ **Ölçüm metodolojisi bulguları** — muhtemelen en özgün kısım: cevaba bağlı payda ·
   hakem yığını kayması (base A1 0,9864 → 0,9587, asimetrik) · yeniden-koşum gürültü tabanı 0,3 p ·
   ikili oran kuantumu · eşit sınav kapısı (ADR-0057).
   🆕 **#60 bu listeye altıncıyı ekliyor:** *bir çekinme dedektörünün istem rejimine bağımlı olması
   ve bunun ancak gözle okumayla yakalanması.*

**"Şu üçünü ölçersen paper çıkar" — ÖNCELİK DEĞİL:**

| # | eksik ölçüm | ne kazandırır | bedel |
| :-- | :--- | :--- | ---: |
| **P1** | **CP4 + CP5 tabanları** | *"merge, ardışık/karışık SFT'den daha iyi korur"* — iddianın çekirdeği. ⚠️ **ARA KAPI düştüğü için yetkisi YOK.** ⚠️ Ön-kayıt CP4'e *"karışık SFT"* diyor ama `τ_a` **ORPO** ile eğitildi | ~$19,1 |
| **P2** | **Üç-aileli hakem paneli + κ** (YB4) | her yargı-eksenli sayı bugün **tek aile** damgalı | ÖLÇÜLMEMİŞ |
| **P3** | **Frozen TEST + güç analizi** | DEV n=80'in gözlenen farkları ayırt edip etmediği bilinmiyor | ~$1 |

⚠️ Ürün için üçü de gerekli değil; P2/P3 model kartında **Limitations satırı** olarak yazılmalı.

---

## 7. RİSKLER ve İNSANA SORULACAKLAR

### 7.1 Riskler

| # | risk | kanıt | azaltma |
| :-- | :--- | :--- | :--- |
| R1 | **Rakip koşan hedef** — 3.1 → 3.5 FL 16 günde kütlede **+7,8 p** ve kazanç **daha az düşünerek** geldi (770 → 445 tok) | `g2-fl-harness/OZET.md` | Rakip **ölçüt**, hedef değil; yapısal üstünlükler (güncellik · mahremiyet · $0) zamanla **büyüyor** |
| R2 | **B10 turu kol kapısında düşebilir** | ön-kayıtlı kapı | v1 `tgta_v1` ile çıkar, B10 **bilinen sınır** olarak yazılır; A2/A3 karşılanmazsa `v0.2` |
| R3 | **ARA KAPI düştü** → merge'in tabanlara üstünlüğü **kanıtsız** | #58 | `v1.0` adı savunulabilir mi? **S1** |
| R4 | **Frozen TEST public** | `git ls-files data/eval` | Yeni set üret (2.1) + kontaminasyon prosedürü |
| R5 | **Adaptörler tek kopya, yedeksiz** (12B hattında adaptörler kalıcı kaybedildi) | kollar.md | HF yayını **ilk gerçek yedek** → ADR |
| R6 | **`SOURCE_CLIP` ödenmeden `k` hükümleri TANIMSIZ** | KARAR-4 | ≈$0,30 ⚠️ tarihsel `verdict`leri kıyaslanamaz kılar |
| R7 | **TR IP kısıtı bulut barındırmayı engelleyebilir** | BEDESTEN_API | v2'de **ölç**, varsayma |
| R8 | **Aralıklı ritim** — hafıza yalnız repo'da | CLAUDE.md | Faz 0.1-0.5 **önce**: bugünkü repo dışa **yanlış sayı** yayımlıyor |
| R9 | **Servis rejimi ↔ ölçüm rejimi sapması** (`-np`, ctx, kuantizasyon) — hata vermez, sayı tutmaz | kusur 13 · KARAR-6 · 🆕 **#60: Jaccard 0,5278** | 4.6 zorunlu |
| R10 🆕 | **Ölçüt kırılganlığı** — `exact_reject` istem rejimine bağımlı çıktı; aynı sınıf başka aletlerde de olabilir | #60 | Her yeni tüketicide **gözle okuma adımı zorunlu** (ADR-0051 iki kez kendini ödedi) |

### 7.2 Karara bağlanacaklar

| # | soru | seçenekler |
| :-- | :--- | :--- |
| **S1** | **ARA KAPI düşmüşken `v1.0` adı verilebilir mi?** | (a) v1.0 = *ürün* olgunluğu, ARA KAPI *iddia* kapısıydı → yeni ölçütle aç · (b) CP4-CP5 koşulana dek `v0.x` (⚠️ ~$19, yetkisi yok) · (c) sürümü ikiye ayır |
| **S2** | **v1 harness'lı mı çıkar?** | (a) **evet, CLI ile** (öneri) · (b) model-only → ama yayımlanan sayı yeniden üretilemez |
| **S3** | **B10 hedefi?** | (a) ≤11/80 (öneri) · (b) ≤8/80 (3.1 FL ile eşitlen) · (c) yalnız "gerileme yok" |
| **S4** | **`SOURCE_CLIP` ödensin mi?** (≈$0,30) | (a) öde → `k` tanımlı, ⚠️ tarihsel `verdict` kıyaslanamaz · (b) ödeme → TANIMSIZ damgayla taşı |
| **S5** | **İkili oran çözünürlük sınırı** | (a) k-kalem · (b) ölçülmüş taban · (c) Wilson ($0) |
| **S6** | **Önsözün atıf bedeli kabul mü?** | atıf −%30, atıfsız cevap 8→13 ↔ kütle +1,4 p, A1 +1,9 p |
| **S7** | **Adaptörler HF'ye yüklensin mi?** | kollar.md kararını değiştirir → ADR |
| **S8** | **İndeks nasıl dağıtılır?** | (a) HF dataset (80 MB) · (b) kurulumda üret (10 dk) |
| **S9** | **v2 barındırma** | (a) yalnız self-host · (b) + vitrin (~$100-300/ay) · (c) hosted-first (⚠️ mahremiyet) |
| **S10** | **Avukatlık Kanunu / sorumluluk** | hukukçu görüşü gerekir |
| **S11** | **arxiv** | (a) hayır · (b) yalnız P2/P3 (**metodoloji paper'ı — en güçlü hikâye**) · (c) tam iddia katmanı |
| **S12** | **KARAR-6 (paralel slot)** | sayılar geldi (Jaccard 0,5278 · birebir 3/19) ⚠️ **bozuk ölçütle** → onarım sonrası yeniden koş, **hükmü insan kurar** |
| **S13** 🆕 | **Hasat kabul ölçütü nasıl onarılır?** (#60) | (a) `exact_reject`'in önsözsüz dalı düzeltilir — ⚠️ **çıpaları da etkileyebilir**, ADR gerekir · (b) hasat **önsözlü** koşar — alet değişmez ama hasat `τ_a` v1'in rejiminden uzaklaşır · (c) ikisi de + çıpaların 80 kalemi gözle okunur |

---

### Son not — bu roadmap'in kendi zayıflığı

Faz 1'in getirisi **koşulmamış bir turun** ön-kayıtlı tahminlerine dayanıyor. Repo'nun sicili:
ön-kayıtlı tahminler **üç kez tuttu, üç kez tutmadı** (S1'in %65'i %59,5 · S2'nin %59,5±1'i %61,3 ·
D1 öncesi *"istem katmanı eğitilmiş refleksi değiştirmez"* çürütüldü). §3.2'nin A2/A3 eşikleri
**kapıdır, plan değildir**: karşılanmazsa v1 `tgta_v1` ile ve **B10 açık borç olarak** çıkar — bu da
meşru bir v1'dir, çünkü ürünün vaadi *"en iyi model"* değil,
***"ne bildiğini ve ne bilmediğini söyleyen model"***.

🆕 Ve #60 bu zayıflığı bir kez daha gösterdi: Faz 1'in ilk ölçülen adımı, planın kendi
ön-kayıtlı kapısının **yanlış sebeple geçtiğini** ortaya çıkardı.
