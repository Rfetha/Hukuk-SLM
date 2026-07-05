# v2c ROADMAP — harman (v2b ampirik × dış danışman × Claude değerlendirmesi)

> ❄️ **DONDURULDU (2026-07-05).** v2c iterasyonu kapandı → **REDDEDİLDİ** ([[v2c_sonuclar]], ADR-0014).
> Aktif reçete artık **[[v3_recipe]]** (ORPO). Bu doküman v2c'nin tam planı olarak tarihsel referanstır;
> güncellenmez. Kronoloji otoritesi: [[research_log]].

---
## 🟢 DURUM — taze agent BUNU OKU (güncel tutulur, silinmez)

> **Proje:** HakHukuk / Hukuk-TR — Türkçe hukuk SLM (Gemma 4 12B QLoRA, Faz 1 SFT).
> Eğitim = Modal A100 (`--detach` ŞART), eval = lokal RTX 5070 (`source ~/code/global_venv/bin/activate`).
> Önce oku: `CLAUDE.md` · `docs/record/research_log.md` (kronoloji, OTORİTE) · `docs/record/v2b_sonuclar.md`.
>
> **NEREDEYİZ (2026-07-03):** v2c eğitildi (Modal A100, adapter `outputs/v2c/`, config = v2b) + **6-mod eval TAM KAPANDI**.
> **SONUÇ → v2c REDDEDİLDİ.** Ana hedef **M2 yanlış-kaynak red = 0.407** « §6 hedefi 0.90 (v2b 0.346'dan
> sadece +0.06; base 0.704'ün bile altında). Ayrıca **M1 A1 = 0.832 < §1 kapı 0.904** (regresyon). Tier A SFT
> veri-kolu (counterfactual + abstain_trap) yanlış-kaynak reddini **restore edemedi** →
> **K3 NEGATİF BULGUSU:** §3-E hipotezi ("ucuz SFT counterfactual yeter") ÇÜRÜDÜ.
> Tavan korundu (M4 0.977 · M2b 0.973 · M3 1.000 · register 1.0) + anti-hedef tuttu (M5 0.125 < base 0.225). Detay: §6.
>
> **TAM SKORKART (6/6 + register + M5):** M1 0.832@80% · M4 0.977 · M2 0.407 · M2b 0.973 · M3 1.000 · M5 0.125 · reg 1.0.
> **SIRADAKİ = AÇIK (KARAR YOK):** fix seçenekleri literatür taramasıyla çerçevelendi → `docs/record/v2c_fix_deep_research.md`
> (5 aile: ORPO/DPO · RAFT · R-Tuning · RAAT/CaRT · DTA/RPO). Dış görüş-2 (Gemini) alındı. **Yeni iterasyon adı/kararı
> VERİLMEDİ** (kullanıcı kısıtı) — seçenekler v2c ADR'ında "potansiyel durumlar" olarak listeli. Herhangi bir yeni FT/pipeline
> = Modal para-kapısı + kullanıcı onayı (sormadan başlama).
>
> **DEĞİŞMEZ KURAL:** §1 regresyon kapısı 6 sayı (M1 0.904 · M4 0.975 · M2b 0.96 · M3 1.000 · M5 0.175-nötr · A4 0.925).
> **BİTİRİRKEN:** bulgu → `research_log.md` · karar → v2c ADR · bu roadmap'i güncel tut · Modal $30 kredi (kart ekli).

---

> **Bu doküman ne:** v2c FT turunun KARAR belgesi. Üç girdiyi birleştirir:
> 1. [[v2b_sonuclar]] — ampirik gerçek (v2b tüm kapıları geçti; tek gerçek açık M2=0.346).
> 2. [[v2c_inputs_birlesik]] Bölüm A — harici agent teknik önerileri (v2b'yi görmeden). *(arşiv)*
> 3. [[v2c_inputs_birlesik]] Bölüm B — önerileri v2b açıklarına bağlayan süzme + itirazlar. *(arşiv)*
> **Harman kuralı:** v2c hedefi = (v2b kapı-durumu) ∩ (danışman ∩ Claude süzmesi).
> **Tarih:** 2026-07-02 · Otorite kronoloji: [[research_log]] · Karar: yeni ADR (v2c) yazılacak.

---

## 0. Tek cümle
v2b **tüm kapıları geçti**; v2c bir kurtarma değil **hedefli robustness turu** —
tek gerçek açığı (**yanlış-tek-kaynakta abstention M2=0.346, param_leak %61.5**) ve 3 ikincil
kusuru, geçmiş eksenleri (grounding + deployment-abstention) **bozmadan** TEK FT'de kapatmak.

## 1. Değişmez kısıt: REGRESYON KAPISI (v2c bunları DÜŞÜREMEZ)
| Eksen | v2b değeri | Kaynak |
|---|---|---|
| M1 A1 (cevaplanan grounding) | **0.904** | deployment manşeti |
| M4 A1 (oracle tavan) | 0.975 | |
| M2b abstention (deployment-modu, adil) | **0.96** | asıl A3 manşeti |
| M3 abstention (boş-kaynak) | 1.000 | |
| M5 A2 forgetting (blind) | 0.175 (base-nötr) | replay tuttu |
| A4 cit_precision | 0.925 | |

Her v2c koşusu bu 6 sayıyı yeniden ölçer; **biri anlamlı düşerse v2c reddedilir.**

---

## 2. Hedefler (v2b'nin bıraktığı 4 açık → G1–G4)

> **SONUÇ (2026-07-02):** **G1 ❌ başarısız** (M2 0.407, birincil hedef — Tier E'ye kaldı) ·
> **G3 ✅** (GOLD-scrub %5.99→0) · **G4 ✅** (register ölçüldü, v2b=1.0) · **G2** (off-by-one) v2c'de
> ele alınmadı → Tier D'ye ertelendi. v2c REDDE gidiyor çünkü G1 (birincil) tutmadı + §1 M1 regresyonu.

| # | Açık | v2b sayısı | Hedef | Sınıf |
|---|---|---|---|---|
| **G1** | Yanlış-makul TEK-kaynakta abstention | M2 Rej\* **0.346** · param_leak 0.615 | Rej\* **≥0.90** (base 0.786'yı NET geç, §6) | 🔴 birincil |
| **G2** | Off-by-one yanlış-madde atfı | CMK 109→"110", İş K 55→"56"… | off-by-one vakalar ↓ | 🟡 ikincil |
| **G3** | GOLD-jargon sızıntısı | hedef %5.7 · çıktı ~1/40 | ~%0 | 🟢 kozmetik |
| **G4** | Register/altitude ekseni | script VAR, koşulmadı¹ | önce ÖLÇ (proxy), sonra hedefle | ⚪ açık eksen |

> ¹ **Düzeltme (2026-07-02):** `scripts/score_register.py` MEVCUT (v1-leksik-proxy, hakemsiz, bedava). "Hiç ölçülmedi" = script eksik değil, sadece base/v1/v2b üstünde henüz KOŞULMADI. Kanonik metrik (LLM-judge rubriği) hâlâ TODO (ADR-0013). Aç-koş spec → §7·AÇ-KOŞ-1.
| (yan) | core_hard kötü-eşleşme | ≥3 vaka (KMK Md4 vb.) | benchmark temizliği | 🟡 veri-hijyeni |

---

## 3. İş kalemleri — 3 girdinin nerede birleştiği/ayrıldığı

### 🔴 TIER A — v2c reçetesinin ÇEKİRDEĞİ (hepsi TEK v2c FT'de, ayrı koşu açma)

**A1 · TRAP-tipi abstain dilimi ekle** — *asıl kaldıraç, G1*
- **Üç girdi de birleşiyor:** v2b-notu #1 · danışman §3/§6 · Claude §1.
- Mevcut abstain dilimi = "gold yok, sadece distractor" (RAG-ıska) → M2b 0.96 zaten çözdü.
  EKSİK = "**yanlış-ama-makul TEK/az kaynak var → gerekçeli reddet**". `trap.jsonl` KALIBI gibi
  (aynı kanun, numara-komşusu yanlış madde) ama **kaynağı trap.jsonl DEĞİL** (eval sızıntısı) →
  madde havuzundan üret. Hedef = yanlış kaynağı ADIYLA reddet.
- **Aksiyon:** yeni slice `abstain_trap` — `build_sft_v2b.py pack`'te üret + `gen_v2b_answers.py`'a
  reddetme şablonu ekle; abstain kompozisyonunu RAG-ıska + TRAP-tipi böl. **Oranı koru (~%20),
  TİPİNİ zenginleştir** (Claude §1: sorun oran değil kompozisyon).
- **Aç-koş spec → §7·AÇ-KOŞ-3** (dilim sayısı, komşu-seçimi, şablon, kompozisyon oranları).

**A2 · Anti-parametric-leak counterfactual** — *G1'in ikinci yarısı (param_leak 0.615)*
- **Kaynak:** v2b-notu #2 (ampirik; danışmanda YOK). Claude §1'in "ORPO M2-negatifleri" ile aynı hedef.
- Kaynak ezbere aykırı/eksik olduğunda hedef = kaynağa uy ya da reddet, **ezberden tamamlama**.
- **Aksiyon:** counterfactual örnek imal et (madde metni ↔ ezber çatışır); SFT-içi. ORPO'ya
  gerek YOK bu aşamada — SFT counterfactual dilimi daha ucuz ve ablasyon-temiz (bkz Tier D).
- **Aç-koş spec → §7·AÇ-KOŞ-2** (otomatik olgu-bozma yöntemi, miktar, gate ayarı — teacher YOK).

### 🟢 TIER B — VERİ HİJYENİ (gerçekten bedava, regresyon riski ~0)

**B1 · GOLD scrub** *(G3)* — danışman §5 · Claude §1 · v2b-notu #3, **üçü birleşiyor**.
- (a) `gen_v2b_answers.py` teacher-prompt'unda "GOLD" yasağı + morfoloji kuralı;
  (b) mevcut `answers.jsonl`'da **önce raporla (kaç örnek/kalıp) → cümle bozmadan temizle**.
- Sayıları research_log'a (temizlik öncesi/sonrası). *Not: app-layer post-process de yeter, acil değil.*

**B2 · Replay kaynağı teyidi** — danışman §5 "temiz Yargıtay". Claude §1: **önce DOĞRULA**
mevcut `build_replay_tr.py` (%3) ne içeriyor; uygunsa dokunma.

**B3 · core_hard kötü-eşleşme temizliği** *(yan)* — M1'de yakalanan ≥3 vaka (KMK Md4).
Benchmark hijyeni; eval adaletini artırır.

### 🔵 TIER C — ÖLÇÜM / EVAL ADALETİ — ✅ TÜMÜYLE KAPANDI (2026-07-02, research_log "ADIM 2 · TABLO 1")
> C1 register (base/v2b=1.0) · C2 shuffle-teyit · C3 base rescore · C4 Mecellem Tablo 1 — hepsi bitti. Aşağısı gerekçe/spec arşivi (paper metodu).

**C1 · Register eksenini ÖLÇ** *(G4)* — Claude §1 + v2b-notu #5. **Hedef koymadan önce baseline gerek**
(ADR-0010/0013 açık eksen). base/v1/v2b üçünde uzman-register skorla.
**Script MEVCUT** (`score_register.py`, leksik-proxy) → ŞİMDİ koşulabilir. **Aç-koş spec → §7·AÇ-KOŞ-1.**

**C2 · Position-bias shuffle + gold-pozisyon randomizasyon** — danışman §7 · Claude §1.
`gen_eval_grounded.py`'de gold pozisyonu gerçekten randomize mi TEYİT et; değilse ekle.
**G2'yi (off-by-one) de test eder** — gold hep aynı yerdeyse etiket ezberi maskelenir.

**C3 · base/v1 yeniden skorla** (cevaplanan-only + eval-mirror + M2b no-gold) → elmayla-elma;
M2b'yi n=40'a tamamla. (v2b_sonuclar açık işi.)

**C4 · RAKİP BASELINE skorla → paper Tablo 1** *(PAPER_TARGET §4)* — C3 ile AYNI operasyon
(aynı harness/mod/n/hakem/seed), FT'den bağımsız, C3 ile tek ölçüm-oturumunda batch'le.
- **Modeller:** `newmindai/Mecellem-Qwen3-4B-TR` (en yakın decoder rakip) + (bütçe/zaman kalırsa) `Mecellem-1.7B`, `Llama-3.1-8B-legal`.
- **Yerel koşar** (4B → RTX 5070, Modal gerekmez).
- ✅ **HF TEYİT (2026-07-02):** `Mecellem-Qwen3-4B-TR` (Qwen3-4B) + `Mecellem-Qwen3-1.7B-TR` (Qwen3-1.7B) ikisi de **public/gated değil, Apache-2.0**. İndirilebilir, lisans-temiz.
- ⚠️ **Çerçeve (teyitli):** CPT (~270.8B token), **instruction-tuned DEĞİL** → RAFT/RAG promptunu düzgün takip etmez → paper'da **"foundation karşılaştırması"** diye yaz, "instruct elmayla-elma" DEME.
- ⚠️ **Llama-3.1-8B-legal newmindai altında YOK** → ayrı ara (opsiyonel/ikincil, Tablo 1'i bloklamaz).
- **Bu, base-üstünlük kapısından AYRI eksen:** base-gate = katkı izolasyonu · C4 = rekabetçi konumlama (Tablo 1). Çıktı → `PAPER_TARGET.md §4`.

### 🟡 TIER D — G2 off-by-one *(ikincil, veri+format)*
- Danışman §2 "citation-tuning" · Claude §1 "madde-no sadakati + distractor kurgusu" · v2b-notu #4.
- **Kök neden:** bitişik-madde distractor'ından madde-no sızması. → distractor'ı **uzak-madde**
  seç + citation-tuning'i format değil **madde-no doğruluğuna** odakla (cit_precision zaten 0.925).

### ⚪ TIER E — PAPER ABLASYON KOLLARI *(bütçe kalırsa, HER BİRİ AYRI KOL — drop-in değil)*
Claude §2'nin danışmandan en net ayrıldığı yer: danışman bunları "bedava P0/tek-koşu" saydı; **değiller.**
| Kol | Danışman | Claude verdikti | Neden ayrı kol |
|---|---|---|---|
| **rsLoRA** | "P0 sıfır maliyet" | ⚠️ **ablasyon kolu** | r=16'da α/√r = efektif **4× lr** → tuned lr=1e-4'ü bozar (3e-4 elenmişti). Denenirse lr yeniden ayarla. |
| **ret-token loss ×2** | "P0" | ⚠️ **ablasyon kolu, ≤1.5×** | over-abstention → M1 A1'i düşürme riski; veri-fix (A1) önce. |
| **DoRA** | "P1 dene" | ✅ P1 kol | +%10-15 bellek, önce ~2K OOM testi; kazanç kanıtı yok. |
| **ORPO (M2-negatif)** | "P0" | ✅ ama **SFT counterfactual'dan SONRA** | reference-free doğru; ama A2 counterfactual daha ucuz+temiz. Negatif = v2b M2-fabrikasyonu (M3 DEĞİL — M3 zaten 1.000). |
**Kural:** danışmanın "rsLoRA+ORPO tek-koşu"su iki değişkeni karıştırır → paper için ayrı tut.

---

## 4. Elenen öneriler (danışman ∩ Claude, itiraz yok)
Full-FT, LoRA+, context-distillation, CoVe, SimPO/KTO, tokenizer-genişletme, LoftQ, seq_len>2048 —
hepsi bütçe/bellek/amaç gerekçesiyle **v2c kapsamı dışı** (gerekçeler girdi dokümanlarında).

---

## 5. Sıra (execution) — TEK NUMARALI AKIŞ (aç-koş)

> Bu liste **tam icra sırası** — yukarıdan aşağı, karar kalmadan koşulur. `⛓️` = bağımlılık
> (o adım biri BİTMEDEN başlamaz). Tier etiketleri gruplama; **gerçek sıra bu numaralar.**

1. ✅ **C1-v2b register** (Tier C) — KOŞULDU 2026-07-02. v2b M1: `register_mean=1.0` · `expert_frac=1.0` · `citizen_frac=0.0` (n=40, 40/40 expert_hits≥1 & citizen_hits=0). Uzman-register tam. Kaynak: `outputs/eval/reg_m1_v2b_summary.json`; kayıt: research_log "v2c icra — ADIM 1". base/v1 yarısı → ADIM 2 (⛓️ C3 rescore detail'i).
2. ✅ **C3 + C4 + C1** — TEK ölçüm oturumu **TAMAMLANDI (2026-07-02)** → research_log "ADIM 2 · TABLO 1".
   - ✅ **base 6-mod (C3)** cevaplanan-only+eval-mirror+M2b rescore · ✅ **C1 register base/v2b** = 1.0 · ✅ **C4 Mecellem 6-mod → Tablo 1** (completion-fewshot, lm_head-tie fix). Ana bulgular: base over-refuse (M1 %52), v2b tek açık **M2=0.346**; **Mecellem coverage çöküyor** (M1 %35/M4 %45 — oracle'da bile), M2=1.0'ı kör-red artefaktı; M5 KÖR'de rakip yüksek (0.35, CPT-ezber). **v2b rakibi coverage'da 2× geçiyor**, eşit faithfulness.
   - ❌ **v1 DÜŞÜRÜLDÜ** (kullanıcı kararı): kıyas = base vs v2b vs Mecellem; v1 eski iç-tur, rakip değil.
   - Not: M2b v2b n=30 vs base/mecellem n=40 → v2b M2b n=40 regen ADIM 6d'de (aynı 6-mod eval).
3. ✅ **C2 position-shuffle teyit** — KOŞULDU 2026-07-02. `raft_pack.pack_context:125 rng.shuffle(chunks)` = gold ZATEN randomize. Ampirik: v2b M1 gold-pozisyon `{1:9,2:9,3:9,4:9,5:4}` (bias yok). Sıfır-kod. Kayıt: research_log ADIM 3-5.
4. ✅ **B1 GOLD-scrub** (Tier B) — TAMAMLANDI 2026-07-02. (a) `gen_v2b_answers.py` TEACHER_SYSTEM'e GOLD-yasağı eklendi (⛓️ 6b hazır). (b) answers.jsonl **1157/19305=%5.99 → 0** (cümle korundu, yedek `.pre_scrub.bak`). Kayıt: research_log ADIM 3-5.
5. ✅ **B2 replay teyit + B3 core_hard** — 2026-07-02. B2: replay_tr.jsonl = MIT genel-TR (hukuk-dışı, anti-forgetting amaçlı) → DOKUNULMADI. B3: kötü-eşleşme #28&#29 (KMK Md4) belgelendi, kaldırma n=120 regen'ine ERTELENDİ (elmayla-elma). Kayıt: research_log ADIM 3-5.
6. **Tier A — tek v2c SFT** (sıralı alt-akış):
   - 6a. ✅ **Yeni-kod (4 parça) TAMAM** 2026-07-02: `build_sft_v2b.py` counterfactual+abstain_trap slice (ayrı crng→ana akış bozulmaz) · `_gate` cf-referans · kelime-sayı CF · `gen_v2b_answers.py` ABSTAIN_TRAP_TEMPLATES+build_cf_answer+`--reuse-answers`. py_compile OK, birim-test OK.
   - 6b. ✅ **pack→gen→assemble TAMAM** 2026-07-02 (`data/processed/sft_v2c/`): grounded 14742/cf 716/abstain 2339/trap 1508 (abstain+trap=19.9%✓, trap/abstain=39/61✓); gen **API=0** (grounded v2b-reuse); assemble kept 18701 (CF+trap 0 red), **train 17353/val 963/test 963**. Kayıt: research_log ADIM 6a+6b.
   - 6c. ✅ **Modal `--detach` eğitim TAMAM** (config = v2b: lr=1e-4, r=16/α=32) → adapter `outputs/v2c/` çekildi (251M, r=16/α=32).
   - 6d. ✅ **6-mod eval KOŞTU (2026-07-02)** → **KAPI GEÇİLEMEDİ, v2c REDDE gidiyor.** Sayılar → §6 sonuç tablosu.
     - **M2 = 0.407** « hedef 0.90 (birincil hedef ÇÖKTÜ) · **M1 A1 = 0.832** < §1 kapı 0.904 (regresyon).
     - M4 0.977 · M2b 0.973 · M3 1.000 ✅ (tavan/deployment eksenleri korundu). M5 + register + v2b M2b n=40 regen: eval kuyruğunda.
7. **(kapı GEÇİLEMEDİ →) fix turu = Tier E** (§3-E: ORPO M2-negatif / ret-token loss). Artık opsiyonel değil — K3 bulgusu Tier A'nın yetmediğini kanıtladı. Modal para-kapısı → kullanıcı onayı. Tier D (off-by-one) ikincil, Tier E'den sonra.

## 6. Başarı kapısı (v2c) — ❌ SONUÇ: KAPI GEÇİLEMEDİ, v2c REDDEDİLDİ — ✅ SKORKART KAPANDI (2026-07-03, 6/6 mod)

> **Sonuç (2026-07-03, tam skorkart):** hedef "base'i anlamlı-eksenlerde NET geçmek"ti; v2c **birincil hedefi (M2)
> tutturamadı VE §1 regresyon kapısını (M1) düşürdü.** Aşağıdaki tablolarda **v2c-GERÇEK** sütunu
> ölçülen değerler, Mecellem = rakip baseline (C4, completion-fewshot). Tüm 6 mod + register + M5 kapandı.
> Kaynak: `outputs/eval/*_v2c_*` + research_log "ADIM 2 · TABLO 1" (Mecellem).
> **Kanonik kural:** cevaplanan-only A1 (ADR-0011), eval-mirror 900, n=40/35, hakem gpt-4o-mini, seed 3407.

### 🎯 Tip A — EZİLEBİLİR eksenler (asıl savaş; NET fark ŞART)
| Eksen | base | v2b | Mecellem | **v2c-GERÇEK** | v2c-HEDEF | Sonuç |
|---|---|---|---|---|---|---|
| **M2 yanlış-kaynak abstention** (G1) | 0.704 | 0.346 | 1.0* | **0.407** | ≥0.90 | ❌ **ÇÖKTÜ** (v2b'den +0.06, base'in altında) |
| **M1 grounding A1 @cov** | 0.886 @47.5% | 0.920 @72.5% | 0.918 @35% | **0.832 @80%** | ≥0.94 | ❌ hedefin de §1 kapı 0.904'ün de altında |
| **A4 atıf precision** | ~0.87 | 0.925 | 0.2 (reg) | **M1 0.872 / M4 0.975** | ≥0.95 | 🟡 oracle'da geçer, gürültüde düşük |

> \* Mecellem M2=1.0 **kör-red artefaktı** (coverage %35–45'e çöküyor, oracle'da bile) → gerçek yetenek değil.

### ⚪ Tip B — TAVAN eksenleri (BOZMADAN koru) — ✅ korundu
| Eksen | base | v2b | Mecellem | **v2c-GERÇEK** | Sonuç |
|---|---|---|---|---|---|
| M4 oracle grounding | 0.983 | 0.975 | 0.921 | **0.977** | ✅ §1 kapı 0.975 geçti |
| M3 boş-kaynak abstention | 1.000 | 1.000 | 1.000 | **1.000** | ✅ |
| M2b RAG-ıska abstention | 1.0 | 0.96 | 0.919 | **0.973** | ✅ §1 kapı 0.96 geçti |
| Register (uzman dili) | — | 1.0 | — | **1.0** (expert-frac 1.0) | ✅ v2b'yi korudu (G4 tavan) |

> **v2b M2b @n40 karşılaştırma teyidi:** v2b M2b n40 = **0.969** (n=40, aynı reçete) ≈ v2c 0.973 → M2b ekseni her iki modelde de sağlam; sorun M2b (bariz-off-topic) değil, **yalnız M2 (makul-komşu yanlış-kaynak)**. Ayrım net: kolay-negatif çözülü, zor-negatif çökük.

### 🔻 Tip C — ANTI-HEDEF (base'i geçmek İSTEMEYİZ; düşük = RAG'e dayanma kanıtı)
| Eksen | base | v2b | Mecellem | **v2c-GERÇEK** | Yorum |
|---|---|---|---|---|---|
| M5 KÖR (parametrik ezber) | 0.225 | 0.175 | 0.35 | **0.125** (cov 1.0, cond_acc 0.125) | ✅ base'in ALTINDA — parametrik ezber düşük, RAG'e dayanma kanıtı güçlendi (anti-hedef tuttu) |

> M5 lenient=0.75 / partial=0.625 → model bağlamsız "yaklaşık" konuşuyor ama kesin-doğru madde bilgisi vermiyor (5 CORRECT / 25 PARTIAL / 10 WRONG / 0 ABSTAIN). CORE'da abstain=0 → over-refusal yok; parametrik kesinlik düşük = istediğimiz.

### ❌ KAPI SONUCU — v2c REDDEDİLDİ
- **G1 (birincil):** M2 = **0.407** « 0.90 → **başarısız.** Tier A veri-kolu yanlış-kaynak reddini restore edemedi.
- **§1 regresyon:** M1 A1 = **0.832 < 0.904** → **regresyon kapısı da kırıldı** (coverage↑ %80 ama faithfulness↓).
- **Tavan korundu:** M4 0.977 · M2b 0.973 · M3 1.000 · register 1.0 ✅ — ama tek başına yetmez.
- **Anti-hedef tuttu:** M5 KÖR = **0.125** < base 0.225 → parametrik ezber düşük, model RAG'e dayanıyor (istediğimiz yön).
- **n≥100 güç şartı KOŞULMADI** (n=40/35 kaldı) — moot: v2c n=40'ta bile başarısız, güç artırmak sonucu değiştirmez.
- **K3 negatif bulgusu:** §3-E "ucuz SFT counterfactual yeter" hipotezi ÇÜRÜDÜ → **Tier E (ORPO M2-negatif / ret-token loss) artık zorunlu fix kolu.**
- **Mekanizma:** SFT coverage'ı artırdı (over-refusal↓, iyi) ama **ayrım gücünü kaybetti** — topik-komşu yanlış kaynağa (M2) yapışıp uyduruyor; M2b (bariz-off-topic distractor) ✅ ama M2 (makul-komşu tek-kaynak) ❌.
- Bulgu → research_log · karar → **yeni v2c ADR** (bekliyor, tam skorkart sonrası).

---

## 7. AÇ-KOŞ EKİ — 3 boşluk somutlaştı — ✅ TÜMÜ UYGULANDI (spec arşivi = paper metodu)

> **Durum (2026-07-02):** A1 (abstain_trap) + A2 (counterfactual) + C1 (register) speclerinin
> hepsi **kodlandı ve koştu** (§5 · ADIM 6a/6b · research_log). Aşağısı artık "yapılacak" değil,
> **paper'ın metod bölümü için donmuş spec + gerekçe arşivi.** ⚠️ Ama K3 sonucu: A1+A2 SFT-kolu
> M2'yi 0.346→0.407'ye taşıdı (yetersiz) → yöntem GEÇERLİ ama SFT-tek-başına-yetersiz kanıtlandı;
> fix Tier E'de (ORPO/ret-token). Bu ek, "denedik-neden-yetmedi"nin reçetesi olarak değerli.
>
> **Neden bu ek (orijinal gerekçe):** §3'teki A1/A2/C1 "Aksiyon" satırları niyet düzeyindeydi.
> Kaynak-teyit: `score_register.py` (var), `build_sft_v2b.py` (pack/gate), `gen_v2b_answers.py`
> (şablon), `raft_pack.madde_ord`/`pack_context`, `trap.jsonl` (KALIP referansı, veri kaynağı DEĞİL).

### AÇ-KOŞ-1 · Register ölçümü (C1 / G4)

**Durum:** `scripts/score_register.py` MEVCUT — v1 leksik-proxy (EXPERT_PAT vs CITIZEN_PAT oranı,
`register_score∈[0,1]`, 1=uzman). Hakemsiz, bedava, deterministik. Girdi = `*_detail.jsonl`'ın
`cevap` alanı (mevcut bench detail'lerinde VAR). Yani **şu an aç-koş.**

**Katman-1 (proxy — ŞİMDİ koş, bedava):**
```bash
source ~/code/global_venv/bin/activate
for m in base v1 v2b; do
  python scripts/score_register.py \
    --details outputs/eval/bench_m1_${m}_detail.jsonl --label m1_${m}
done   # (base/v1 için detail eksikse Tier C3 rescore'da üretilecek → aynı oturumda skorla)
```
Manşet: `register_mean` + `expert_frac(>=0.6)` + `citizen_frac(<=0.4)`. base/v1/v2b üçlü tablo → research_log.

**Katman-2 (kanonik — LLM-judge rubriği, ADR-0013 TODO, C1'i kapatır):**
- Hakem = gpt-4o-mini, çapraz = gpt-4o (κ-vekili). `score_correctness.py`'ın judge-call kalıbını
  klonla; SADECE rubriği değiştir.
- 5'li rubrik (1=uzman ↔ 5=vatandaş-basit): (a) madde/kanun atıf dili, (b) resmî bağlaç
  (uyarınca/gereğince/hükmünce), (c) doğrudan-hitap YOKluğu (yapabilirsiniz/siz), (d) sadeleştirme
  kalıbı YOKluğu (yani/kısaca/merak etme), (e) genel ton. Çıktı: `outputs/eval/reg_judge_{label}.jsonl`.
- Proxy ↔ judge uyumunu (κ-vekili) raporla — proxy'yi çapraz-doğrular.

**Hedef (baseline sonrası):** v2c uzman-register **≥ v2b** (`expert_frac` düşmesin, `citizen_frac`
artmasın). Bu bir **regresyon alt-sınırı**, üstünlük değil — uzman-register zaten v2 tasarımı (§6 dışı).

---

### AÇ-KOŞ-2 · A2 anti-parametric-leak counterfactual üretim yöntemi

**Amaç:** "kaynak metni ↔ parametrik ezber çatışınca **kaynağa uy**" öğret (param_leak 0.615 ↓).
**Prensip:** teacher-LLM YOK — otomatik + deterministik + ablasyon-temiz (ORPO'ya gerek yok, §3-E).

**Yeni slice `counterfactual` — `build_sft_v2b.py pack` içine ek üretici:**
1. Grounded tohumun `gold_text`'inde bir **sayısal/somut olgu** yakala (regex):
   süre `\b\d+\s*(gün|ay|yıl|hafta|saat)`, eşik `%\s*\d+` / `\b\d[\d.]*\s*(TL|lira)`,
   yaş `\b(on\s?sekiz|\d+)\s*yaş`. Olgu bulunmayan tohumu ATLA.
2. Olguyu **sistematik boz** (sabit seed'le farklı-ama-akla-yatkın değer: 15 gün→30 gün, %25→%40,
   on sekiz→yirmi bir). Sonuç = `cf_gold_text` (gold'un counterfactual kopyası).
3. `cf_gold_text`'i KAYNAK olarak context'e koy (uzak distractor'larla). Hedef cevap ŞABLON:
   "Verilen kaynağa göre ##begin_quote## [cf_gold'daki DEĞİŞTİRİLMİŞ ifade, verbatim] ##end_quote##
   … (KANUN, Madde X)." → model **gerçek-dünya ezberini değil KAYNAĞI** izler.
4. **Gate ayarı:** `_gate` grounded verbatim⊂gold kontrolü, counterfactual slice'ta **cf_gold_text'e**
   bakmalı (gerçek gold_text'e değil) — yoksa "alıntı gold'da değil" ile reddeder. `row["cf_gold_text"]`
   alanını ekle, `_gate` slice=="counterfactual" ise onu referans al.

**Miktar:** grounded dilimin ~%10'u (~15K grounded → ~1.5K cf). Regex tutmayan tohum düşer, gerçek sayı loglanır.
**Kayıt:** kaç tohumda olgu bulundu / kaç bozuldu / hangi olgu-tipleri → research_log (K3 ampirik malzeme).

---

### AÇ-KOŞ-3 · A1 TRAP-abstain dilim speci

**Amaç:** "yanlış-ama-makul TEK/az kaynak var → **gerekçeli reddet**" (M2 Rej* 0.346 → ≥0.90).
**Kaynak kuralı:** yanlış-komşu maddeler **`trap.jsonl`'DAN ALINMAZ** (eval seti = sızıntı) →
madde havuzundan (`mevzuat_maddeler.jsonl`) üretilir. trap.jsonl sadece **KALIBI** verir
(aynı kanun, numara-komşusu yanlış madde no; ör. TMK gold=Md40 → yanlış=Md409).

**Yeni slice `abstain_trap` — `build_sft_v2b.py pack`'te:**
1. Grounded tohum al (soru + gerçek gold, ör. TMK Md 40).
2. gold'u context'ten ÇIKAR; yerine **aynı kanun_no**'nun konu-komşusu YANLIŞ maddesini koy
   + 2-3 uzak distractor. → context'te "makul ama yanlış" tek-kaynak var.
3. Hedef cevap = **gerekçeli red** ŞABLON (API yok): yanlış kaynağı ADIYLA reddeder
   (RAG-ıska şablonundan FARKLI — bkz `ABSTAIN_TRAP_TEMPLATES` altında).

**Komşu seçimi (deterministik):** aynı `kanun_no` içinde, `raft_pack.madde_ord` ile
`0 < |ord(gold) − ord(cand)| ≤ K` (bitişik DEĞİL ama yakın; K≈20) + soruyla düşük leksik örtüşme.
`pack_context`'in distractor havuzu zaten kanun-içi çeker → aynı mekanizmayı yeniden kullan.

**Kompozisyon (abstain toplam oranı ~%20 KORUNUR, tipi bölünür):**
- ~%60 **RAG-ıska** (gold yok, sadece uzak distractor) — MEVCUT, M2b 0.96'yı korur.
- ~%40 **TRAP-tipi** (yanlış-komşu tek-kaynak) — YENİ, M2'yi hedefler.
- → toplamın ~%12 RAG-ıska + ~%8 TRAP-tipi. (pack'te abstain'e düşen tohumu bu oranla ikiye ayır.)

**Yeni şablon seti — `gen_v2b_answers.py`'a `ABSTAIN_TRAP_TEMPLATES` (4-6 varyant):**
> "Sağlanan {yanlış_kanun}, {yanlış_madde} farklı bir hususu düzenlemektedir; sorulan konu bu
> kaynakta yer almamaktadır. Doğru bir atıf için ilgili hükmün ayrıca temini gerekir."
`worker()`: `slice=="abstain_trap"` → `ABSTAIN_TRAP_TEMPLATES`, `slice=="abstain"` → mevcut
`ABSTAIN_TEMPLATES`. İkisi de `ABSTAIN_RE`'yi geçer (gate uyumlu).

---

### Küçük netleştirmeler (aç-koş için gerekli, non-blocking)

| Konu | Karar |
|---|---|
| **n≥100 (§6 güç şartı)** | core_hard=40, trap=35 → yetersiz. `gen_eval_grounded.py --n 120` (deterministik seed → base ve v-model AYNI sorular). TRAP eval seti: `build_eval_sets.py` trap üreticisini n↑ ile yeniden koş. Hedef: her mod ≥100. |
| **C4 Mecellem prompt formatı** | CPT / instruction-tuned DEĞİL → chat-template DEĞİL; **completion-style few-shot** (2-3 örnekli, RAG bloğu düz-metin). Paper'da "foundation kıyası" diye yaz (§3-C4). |
| **Tier A eğitim config** | v2b ile AYNI (lr=1e-4, r=16/α=32, gradient_checkpointing, batch=1). Yeni slice'lar (counterfactual ~%10 + abstain_trap kompozisyon-içi) veri hacmini ~%5-10 artırır → Modal süresi ~orantılı, $30 kredi içinde. rsLoRA/ret-token-loss DAHİL DEĞİL (Tier E ayrı kol). |

**Aç-koş sonucu:** A1/A2/C1 artık "karar bekleyen" değil "koşulabilir." Kalan tek gerçek yeni-kod:
`build_sft_v2b.py pack`'e 2 slice üretici (`counterfactual`, `abstain_trap`) + `_gate`'e cf-referans +
`gen_v2b_answers.py`'a `ABSTAIN_TRAP_TEMPLATES`. Register Katman-1 sıfır-kod (mevcut script).
