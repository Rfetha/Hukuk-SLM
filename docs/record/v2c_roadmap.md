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
> **YAPILACAK (bu dosyanın §5 sırası):**
> 1. **Tier C** (FT'siz, önce — eval'i adil yapar): C1 register ekseni ÖLÇ (base/v1/v2b) · C2 gold-pozisyon shuffle teyit · C3 base/v1'i M2b (`--no-gold`) + cevaplanan-only modda yeniden skorla + M2b'yi n=40'a tamamla · **C4 rakip baseline (Mecellem-4B) skorla → paper Tablo 1** (C3 ile aynı oturum).
> 2. **Tier B** (veri hijyeni): B1 GOLD-scrub · B2 replay teyit · B3 core_hard kötü-eşleşme temizliği.
> 3. **Tier A** (çekirdek, TEK v2c SFT): A1 TRAP-tipi abstain dilimi + A2 anti-leak counterfactual → Modal `--detach` eğitim → adapter çek → **6-mod regresyon eval**.
> 4. Kapı geçerse Tier D (off-by-one) · Tier E (paper ablasyon kolları) bütçe kalırsa.
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
| **G4** | Register/altitude ekseni | hiç ölçülmedi | önce ÖLÇ, sonra hedefle | ⚪ açık eksen |
| (yan) | core_hard kötü-eşleşme | ≥3 vaka (KMK Md4 vb.) | benchmark temizliği | 🟡 veri-hijyeni |

---

## 3. İş kalemleri — 3 girdinin nerede birleştiği/ayrıldığı

### 🔴 TIER A — v2c reçetesinin ÇEKİRDEĞİ (hepsi TEK v2c FT'de, ayrı koşu açma)

**A1 · TRAP-tipi abstain dilimi ekle** — *asıl kaldıraç, G1*
- **Üç girdi de birleşiyor:** v2b-notu #1 · danışman §3/§6 · Claude §1.
- Mevcut abstain dilimi = "gold yok, sadece distractor" (RAG-ıska) → M2b 0.96 zaten çözdü.
  EKSİK = "**yanlış-ama-makul TEK/az kaynak var → gerekçeli reddet**". `trap.jsonl` kurgusu gibi:
  konu-komşusu yanlış madde koy, hedef = kaynağa dayalı red.
- **Aksiyon:** `gen_v2b_answers.py`'a bu dilim tipini ekle; abstain kompozisyonunu
  RAG-ıska + TRAP-tipi olarak ikiye böl. **Oranı koru (~%20), TİPİNİ zenginleştir**
  (Claude §1: sorun oran değil kompozisyon; danışmanın "%20-30 doğru" tespiti doğru ama eksik).

**A2 · Anti-parametric-leak counterfactual** — *G1'in ikinci yarısı (param_leak 0.615)*
- **Kaynak:** v2b-notu #2 (ampirik; danışmanda YOK). Claude §1'in "ORPO M2-negatifleri" ile aynı hedef.
- Kaynak ezbere aykırı/eksik olduğunda hedef = kaynağa uy ya da reddet, **ezberden tamamlama**.
- **Aksiyon:** counterfactual örnek imal et (madde metni ↔ ezber çatışır); SFT-içi. ORPO'ya
  gerek YOK bu aşamada — SFT counterfactual dilimi daha ucuz ve ablasyon-temiz (bkz Tier D).

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

**C2 · Position-bias shuffle + gold-pozisyon randomizasyon** — danışman §7 · Claude §1.
`gen_eval_grounded.py`'de gold pozisyonu gerçekten randomize mi TEYİT et; değilse ekle.
**G2'yi (off-by-one) de test eder** — gold hep aynı yerdeyse etiket ezberi maskelenir.

**C3 · base/v1 yeniden skorla** (cevaplanan-only + eval-mirror + M2b no-gold) → elmayla-elma;
M2b'yi n=40'a tamamla. (v2b_sonuclar açık işi.)

**C4 · RAKİP BASELINE skorla → paper Tablo 1** *(PAPER_TARGET §4)* — C3 ile AYNI operasyon
(aynı harness/mod/n/hakem/seed), FT'den bağımsız, C3 ile tek ölçüm-oturumunda batch'le.
- **Modeller:** `newmindai/Mecellem-Qwen3-4B-TR` (en yakın decoder rakip) + (bütçe/zaman kalırsa) `Mecellem-1.7B`, `Llama-3.1-8B-legal`.
- **Yerel koşar** (4B → RTX 5070, Modal gerekmez).
- ⚠️ **Çerçeve:** Mecellem = continual-pretrain, **instruct DEĞİL** → RAFT/RAG promptunu düzgün takip etmez → paper'da **"foundation karşılaştırması"** diye yaz, "instruct elmayla-elma" DEME.
- ⚠️ **Önce teyit:** HF public mi + hangi checkpoint (PAPER_TARGET §9 açık kararı).
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

## 5. Sıra (execution)
1. **Tier C önce** (C1 register ölç, C2 shuffle teyit, C3 base yeniden-skor, **C4 rakip baseline→Tablo 1**) — FT'siz, eval'i adil yapar; C3+C4 tek ölçüm-oturumu.
2. **Tier B** (B1 GOLD scrub, B2 replay teyit, B3 core_hard temizlik) — veri hazırlanırken.
3. **Tier A** (A1 TRAP-abstain + A2 counterfactual) → **tek v2c SFT koşusu** → 6-mod regresyon eval.
4. Kapı geçerse Tier D (off-by-one) sonraki mini-tur; Tier E paper bütçesi kalırsa.

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
