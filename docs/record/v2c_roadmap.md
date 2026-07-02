# v2c ROADMAP — harman (v2b ampirik × dış danışman × Claude değerlendirmesi)

---
## 🟢 HANDOFF PROMPT — dönünce/taze agent BUNU OKU (sonra sil değil, güncelle)

> **Proje:** HakHukuk / Hukuk-TR — Türkçe hukuk SLM (Gemma 4 12B QLoRA, Faz 1 SFT).
> Eğitim = Modal A100 (`--detach` ŞART), eval = lokal RTX 5070 (`source ~/code/global_venv/bin/activate`).
> Önce oku: `CLAUDE.md` · `docs/record/research_log.md` (kronoloji) · `docs/record/v2b_sonuclar.md` (v2b sonucu).
>
> **NEREDEYİZ:** v2b bitti, **6-mod canon eval'de TÜM KAPILAR geçti** (grounding 0.904/0.975 · abstention
> M2b 0.96 / M3 1.000 · forgetting nötr). v1'e karşı net kazandı. **Bu doküman (v2c_roadmap.md) = v2c'nin
> TEK OTORİTESİ** — tüm karar/gerekçe burada; başka yerde v2c detayı tekrarlama.
>
> **YAPILACAK — §5 tek numaralı akış OTORİTE (aşağısı özet):**
> 1. **C1-v2b register** (sıfır-kod, hemen). 2. **C3+C4+C1-base/v1** tek ölçüm oturumu (rescore + Mecellem Tablo 1 + M2b n=40).
> 3. **C2** shuffle teyit. 4. **B1 GOLD-scrub** (`⛓️ A gen_answers'tan önce`). 5. **B2+B3** hijyen.
> 6. **Tier A tek v2c SFT:** 4-parça yeni-kod → pack → gen_answers → assemble → Modal `--detach` → adapter → **6-mod eval (§6+§1 kapı)**.
> 7. Kapı geçerse **Tier D** (off-by-one) · **Tier E** (paper ablasyon) bütçe kalırsa. **Ayrıntı/bağımlılık: §5.**
>
> **DEĞİŞMEZ KURAL:** §1 regresyon kapısındaki 6 sayı (M1 0.904 · M4 0.975 · M2b 0.96 · M3 1.000 · M5 0.175-nötr · A4 0.925) **DÜŞEMEZ** — biri anlamlı düşerse v2c reddedilir.
> **⚠️ rsLoRA + ret-token loss-masking P0-BEDAVA DEĞİL** → Tier E ablasyon kolu (gerekçe §3-E). Önce VERİ kaldıracı (Tier A).
> **BİTİRİRKEN:** bulgu → `research_log.md` · karar → yeni **v2c ADR** · bu roadmap'i ilerledikçe güncelle · Modal $30 kredi (kart ekli).

---

> **Bu doküman ne:** v2c FT turunun KARAR belgesi. Üç girdiyi birleştirir:
> 1. [[v2b_sonuclar]] — ampirik gerçek (v2b tüm kapıları geçti; tek gerçek açık M2=0.346).
> 2. [[v2c_input_dis_danisman]] — harici agent teknik önerileri (v2b'yi görmeden).
> 3. [[v2c_input_claude_degerlendirme]] — önerileri v2b açıklarına bağlayan süzme + itirazlar.
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

### 🔵 TIER C — ÖLÇÜM / EVAL ADALETİ (FT'den bağımsız, önce yap)

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
   - 6c. ⏸️ **Modal `--detach` eğitim** (config = v2b: lr=1e-4, r=16/α=32) → adapter çek. **🔴 PARA-KAPISI: kullanıcı onayı bekleniyor.**
   - 6d. **6-mod eval** → §6 üstünlük + §1 regresyon kapısı. **Kapı geçmezse v2c reddedilir.** (base/v1 apples-to-apples baseline = ADIM 2 C3, arka planda koşuyor.)
7. **(kapı geçerse)** Tier D off-by-one mini-tur → Tier E paper ablasyon kolları (bütçe kalırsa).

## 6. Başarı kapısı (v2c) — 🎯 REGRESYON DEĞİL, ÜSTÜNLÜK

> **Hedef yükseltildi (2026-07-02, kullanıcı direktifi):** v2c'nin işi "base'in altına
> düşmemek" DEĞİL, **base'i anlamlı-eksenlerde NET geçmek.** "Küçük fark yeterli değil"
> — hem effect size büyüyecek hem n≥100 + rescore + κ ile gürültü olmadığı kanıtlanacak.
> Aşağıdaki tablo base vs v2b vs **v2c-HEDEF**; v2c koşusu bitince son sütun gerçek sayıyla dolar.

### 🎯 Tip A — EZİLEBİLİR eksenler (asıl savaş; NET fark ŞART)
| Eksen | base | v2b | **v2c-HEDEF** | Not |
|---|---|---|---|---|
| **M2 yanlış-kaynak abstention** (G1) | 0.786 | 0.346 ❌ | **≥0.90** | şu an KAYBEDİYORUZ → net kazanca çevir (dramatik hikâye) |
| **M1 grounding (gürültüde)** | 0.879 | 0.904 🟡 | **≥0.94** | +0.06 gerçek fark → n=100'de gürültü değil |
| **A4 atıf formatı** | ~yok | 0.925 | **≥0.95** + base'in yapamadığını nicele | base yapısal yapamıyor → zaten ezici, ölç-göster |

### ⚪ Tip B — TAVAN eksenleri (ezmek matematiksel imkânsız → BOZMADAN koru)
| Eksen | base | v2b | v2c-HEDEF |
|---|---|---|---|
| M4 oracle grounding | 0.977 | 0.975 | ≥0.975 (base ceiling'i koru, "ezdik" DEME) |
| M3 boş-kaynak abstention | 1.000 | 1.000 | 1.000 |
| M2b RAG-ıska abstention | — | 0.96 | ≥0.96 |

### 🔻 Tip C — ANTI-HEDEF (base'i geçmek İSTEMEYİZ)
| Eksen | base | v2b | v2c-HEDEF |
|---|---|---|---|
| M5 KÖR (parametrik ezber) | 0.225 | 0.175 | ≤base (düşük İYİ = RAG'e dayanma kanıtı; "tasarım" diye çerçevele) |

### İstatistik-gücü şartı (NET fark = iki şart, ikisi de zorunlu)
1. **Effect size:** yukarıdaki Tip-A hedefleri (M2 ≥0.90, M1 ≥0.94).
2. **Güç:** **n≥100** + **base'i aynı modda (cevaplanan-only + eval-mirror + M2b) RESCORE** + **cross-judge κ-vekili (gpt-4o-mini↔gpt-4o)**. Bunlar olmadan "ezdik" denemez — mevcut 0.879 vs 0.904 elmayla-elma bile değil.

### Kapı özeti
- **G1:** M2 Rej\* **≥0.90** (base 0.786'yı da net geç) · param_leak belirgin ↓.
- **M1:** ≥0.94 (base'i +0.06 geç). **A4:** ≥0.95.
- **Tavan eksenleri (M3/M4/M2b) BOZULMADI** (§1 regresyon kapısı hâlâ alt-sınır).
- **G3:** GOLD ~%0. **G4:** register ölçüldü.
- **Güç:** n≥100 + base-rescore + κ tamamlandı.
- Bulgu → research_log · karar → v2c ADR.

---

## 7. AÇ-KOŞ EKİ — 3 boşluk somutlaştı (spec → çalıştırılabilir)

> **Neden bu ek:** §3'teki A1/A2/C1 "Aksiyon" satırları niyet düzeyindeydi ("dilim ekle",
> "counterfactual imal et", "register ölç"). Burada her biri **karar kalmadan koşulabilir**
> seviyeye çekilir: hangi script, hangi fonksiyon, kaç örnek, hangi şablon, hangi gate.
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
