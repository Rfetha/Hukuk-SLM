# Yeni belge katmanı — tasarım (spec)

**Tarih:** 2026-09-06 · **branch:** `yeni-yeni` · **kaynak:** [`DEVIR-PROMPT.md`](../../../DEVIR-PROMPT.md) §10
**Statü:** insan onaylı (bu oturumda soru-cevapla kilitlendi) · **sonraki adım:** plan (`- [ ]` kutucuklu)

> **Bu belge ne:** silinen ileriye dönük belge katmanının yerine ne yazılacağının tasarımı **ve**
> bu oturumda verilen insan kararlarının kaydı. Sayılar hatırlanarak değil **kaynaklanarak** yazıldı;
> her nicelik yanında yaşadığı dosya var.

---

## 1. Bu oturumda KİLİTLENEN insan kararları

| # | soru | **KARAR** | sonucu |
| :-- | :--- | :--- | :--- |
| **S1** | ARA KAPI düşmüşken sürüm adı | **Sürüm ikiye ayrılır**: *ürün sürümü* (`v0.2` → `v1.0`) ↔ *iddia sürümü* ARA KAPI'ya bağlı kalır | ADR-0065 |
| **S2** | v1 harness'lı mı | **Evet** — ağırlık + retriever + indeks + **dağıtılan istem** + CLI | YB6 ve servis katmanı kritik yola girer |
| **S14/S6** | yeterlilik önsözü | **KALDIRILDI** — ürünün varsayılanı **önsözsüz** | manşet **%68,4 → %73,0**; ADR-0058 tersine → ADR-0063 |
| **S11** | arxiv | **Metodoloji paper'ı** (yan ürün) | Hat C |
| — | sıralama | **İki hat paralel**: paketleme ∥ model | Hat A ∥ Hat B |
| — | ölçüm harcaması | **Dördü de ödenecek** (rakip önsözsüz · 3.5 Flash · `SOURCE_CLIP` · `tgta_v1` VRAM) | Faz 0, ~$1,65 |
| — | `v1.0` çubuğu | **Üç maddeli kapı** · çıpa **Gemini 3.5 Flash (tam)** · **δ = 2 p** | ADR-0064, ön-kayıt |
| — | Faz 0 sırası | **Erişim onarımı rakip ölçümünden ÖNCE** | ~$1,35 tasarruf, aşağıda gerekçe |
| **B1** | isabetsizlik yöntemi | **Önce reddetme-örneklemesi** (mevcut alet), GRPO **ertelendi** | ADR-0066 |
| — | `referans-design-doc.md` | **SİLİNİR**, yerine **`docs/MIMARI.md`** yazılır | bu oturumun kapsamı 3 → 4 belge |

**AÇIK bırakılanlar** — belgelerde `AÇIK KARAR` damgalı duracak, sessizce kapatılmayacak:
**S5** (ikili oran çözünürlük sınırı) · **S7** (LoRA adaptörleri HF'ye) · **S8** (indeks dağıtımı) ·
**S9** (v2 barındırma) · **S10** (Avukatlık Kanunu / sorumluluk — hukukçu görüşü gerekir) ·
**S12** (KARAR-6 paralel slot, bozuk ölçütle toplandı).

---

## 2. Manşet sayı DEĞİŞTİ — ve bunun iki bedeli var

**Yeni varsayılan rejim: harness AÇIK · k=10 · S2 indeks · ÖNSÖZSÜZ**
*(`outputs/eval/s2-harness-k10-etiketli/` · DEV n=80 · hakem `gpt-4o-mini` · seed 3407)*

| eksen | önsözsüz **(yeni varsayılan)** | önsözlü *(eski manşet)* |
| :--- | ---: | ---: |
| sadık-cevap **kütlesi** | **%73,0** | %68,4 |
| coverage | 0,9000 | 0,8250 |
| A1 · cevaplanan | 0,8110 | 0,8288 |
| A1 · altın getirilen | 0,8593 | 0,8729 |
| aşırı-red | 5/80 | 9/80 *(gözle 8/80)* |
| **isabetsizlik** | **7/80** | 5/80 |
| `recall@10` | 0,875 | 0,875 |

**Bedel 1 — rakip kıyası GEÇERSİZ kaldı.** `g2-fl-harness/OZET.md`'nin eşit sınav kanıt tablosu
*"yeterlilik önsözü (h1): BİZ AÇIK · 3.1 FL aynı · 3.5 FL aynı ✅"* diyor. Yani rakipler
**önsözlü** ölçüldü. `%73,0 ↔ %69,5` kıyası ADR-0057 anlamında **eksen uyuşmazlığıdır** ve
*"3.5 FL'ı geçtik"* cümlesi o sütundan **KURULMAZ**. Eşleşmiş tek sayı hâlâ `%68,4 ↔ %69,5`
(**−1,1 p, geride**). ⇒ Faz 0'da rakipler önsözsüz rejimde yeniden ölçülür.
⚠️ Önsözü kaldırmak **onların** sayısını da yükseltebilir — ölçülmedi, varsayılmıyor.

**Bedel 2 — yeni manşetin gözle okuması YOK.** *"Gözle okuma bir kapıdır"* kuralı bu hatta
2026-09-06'da kendini kanıtladı: sayısal kapı (`0,1733 > 0,10`) bozuk ölçümü **geçirdi**, yakalayan
şey gözle okumaydı ve **önsözlü** çıpanın 14 aşırı-red kaleminin **6'sı yanlış pozitif** çıktı
(`outputs/eval/olcum-bi/B10_GOZLE_OKUMA_80.md`). O okuma **yalnız önsözlü rejimde** yapıldı.
⇒ Önsözsüz rejimin 80 kalemi de gözle okunmadan `%73,0` **yayımlanamaz.** Bedel **$0**, kapı.

---

## 3. `v1.0` kapısı — ön-kayıt (ADR-0064)

Formül **şimdi** yazılır, sayı ölçümden sonra **mekanik** türer. ARA KAPI'nın kalıbı budur:
ön-kayıtlanan şey formüldü, sayı değil ([ADR-0045](../../adr/0045-ara-kapi-merge-onarim-kontrolu.md)).

```
(1) kütle ≥ (3.5 Flash'ın kütlesi) − 2,0 p     ← ASIL KAPI · eşleşmiş rejim, aynı 80 soru
(2) isabetsizlik ≤ 7/80                         ← GERİLEMEZ · önsözsüz rejimin bugünkü değeri
(3) M5 (kör/parametrik) ≤ bugünkü               ← ANTİ-HEDEF · ezber kazancı kapıdan geçmez
(*) her sayım adımında GÖZLE OKUMA zorunlu      ← §2 Bedel 2
```

**δ = 2 p neden:** hakem gürültü tabanı (0,3 p) **yalnız A1 için** ölçüldü; kütle = coverage × A1
ve coverage'ın varyansı o tabanda **yok** — dolayısıyla gürültüye dayalı bir δ **kurulamaz**.
2 p, "yetişti" demeyi hak edecek kadar dar, tabanın altına düşmeyecek kadar geniş: insan kararı.

**Kapının bilinen sert sınırı:** `recall@10 = 0,875` → 10/80 soruda altın madde bağlama hiç
girmiyor → kütle tavanı **%87,5**. Aynı harness'ı kullandığı için 3.5 Flash da aynı tavana tabi
(sınav eşit kalır), ama bizim kazanma payımız da o tavanla sınırlı.

---

## 4. Faz 0 — ölçüm ön-koşulu (~$1,65 · zincir, sırası bağlayıcı)

**Neden erişim önce:** eşit sınavın kanıtı *"`recall@10` üç öznede de birebir 0,875"* — rakipler
**bizim indeksimizi** görüyor. İndeksi/erişimi sonradan değiştirmek o kanıtı bozar ve üç kolun
**yeniden ölçülmesini** gerektirir (~$1,35). Erişim onarımı GPU'suz ve **$0**, tavanı yükselten tek
kalem. Kapı formülü §3'te kilitli olduğu için sayıyı önce görmek eşiği oynatamaz.

| # | adım | bedel | `verify:` |
| :-- | :--- | :--- | :--- |
| **F0.1** | **Erişim onarımı** — `recall@10` 0,875 üstüne çıkarma denemesi (hibrit ağırlık, RRF, chunk sınırı; korpus 40.496 madde, indeks 80 MB, 759 ms/sorgu CPU). ⚠️ Süpürme **yalnız DEV'de** — donmuş TEST'e dokunulmaz | **$0** | `recall_olc.py` yeni `recall@10` basar; **yükselmezse indeks olduğu gibi kalır** ve F0.2 atlanır |
| **F0.2** | Erişim değiştiyse **bizim kolun yeniden üretimi + puanlanması** (önsözsüz, h1@k=10) | ~$0,15 | yeni `harness_tablo.json` + KUNYE |
| **F0.3** | ⭐ **Önsözsüz rejimin 80 kalemi GÖZLE OKUNUR** | **$0** | `GOZLE_OKUMA_80.md` + alet ↔ göz deltası raporlanır (önsözlü çıpada delta 9 ↔ 8'di) |
| **F0.4** | **Rakip çıpaları, önsözsüz, TEK KEZ**: 3.1 FL · 3.5 FL · **3.5 Flash (tam, ilk kez)** | ~$1,35 | eşit sınav kanıt tablosu: `recall@10` dört öznede **birebir aynı**; kesiklik (`finish_reason=length`) damgalanır — ⚠️ tuzak K2: muhakeme bütçesi rakipte uygulanmıyor |
| **F0.5** | **`SOURCE_CLIP` ödenir** (YB3) — `k`'nın çekinme ekseni TANIMSIZ'dan çıkar | ~$0,30 | ⚠️ tarihsel `verdict`'ler kıyaslanamaz hâle gelir → eski değerler **damgalanarak durur**, silinmez |
| **F0.6** | **`tgta_v1` VRAM ölçümü** (bugünkü 3,09 GiB **base GGUF** üzerinde ölçüldü) | $0 · ~15 dk | `vram_stack_tgta_v1.json` |
| **F0.7** | **Eşik ön-kaydı** — §3 formülünden sayı türetilir | $0 | ADR-0064 sayıyla kapanır, **eğitimden ÖNCE** |

Kayıt: `research_log` **#62** (sıradaki) · ADR'ler **0063 · 0064 · 0065 · 0066** *(⚠️ 0059 REZERVE, atlanır)*.

---

## 5. Hat A — paketleme (~$0) → `v0.2`

Ürünün altı asıl açığından ikisi burada: servis katmanı **kod olarak yok**
(`grep -rl "fastapi|uvicorn|flask|gradio" scripts/` → 0 sonuç) ve modeli indiren kişi yayımlanan
sayıyı **üretemiyor** (YB6: istem yalnız `gen_eval_grounded.py` içinde).

| # | adım | `verify:` |
| :-- | :--- | :--- |
| **A1** | **YB6** — istem artefaktı: varsayılan (önsözsüz) istem versiyonlu bir dosyaya çıkar, `gen_eval_grounded.py` **onu okur** (tek kaynak, kopya yok) | eval koşusu istemi dosyadan okuyarak **birebir aynı** kütleyi üretir |
| **A2** | **Servis katmanı — CLI.** Tek derin arayüz: `answer(soru) → {cevap, atıflar, kaynaklar}`. İçinde retriever + llama.cpp + istem gizli; harness **GPU'ya girmez** (embedder CPU, indeks CPU RAM/disk) | temiz makinede kurulum → 3 soru → atıflı cevap; `atif_dogrula.py` atıfları doğrular |
| **A3** | **İndeks dağıtımı** — `AÇIK KARAR S8`: HF dataset (80 MB) ↔ kurulumda üret (~10 dk) | karar verilince tek komutla indeks hazır |
| **A4** | **Yeniden üretim yolu** — yayımlanan sayıyı kullanıcının makinesinde üreten tek komut | ölçülen kütle = yayımlanan kütle |
| **A5** | `MODEL_CARD.md` + `README*.md`: yeni manşet, iki sürüm şeması, kırık linkler | `grep` ile silinen dosya adına link kalmadığı gösterilir |
| **A6** | **Sorumluluk ibaresi** — *"hukuki tavsiye değil"* ürün yüzeyine. `AÇIK KARAR S10` (hukukçu görüşü) ibarenin girmesini **engellemez** | CLI çıktısı ve README ibareyi taşır |

## 6. Hat B — model (kütle) → `v1.0`

| # | adım | bedel | `verify:` |
| :-- | :--- | :--- | :--- |
| **B-1** | Faz 0 (§4) | ~$1,65 | eşik ön-kayıtlı |
| **B-2** | **B1 · isabetsizlik** (7/80 önsözsüz) — **reddetme-örneklemesi**: n cevap üret → **yalnız atıfı altına doğrulananları** tut → elimizdeki TRL `SFTTrainer` ile eğit. Alet **hazır ve L4'te doğrulanmış** (`harvest_b10`, ADR-0047 m.2 taşıyıcısı; sızıntı süzgeci 13.350 → 12.914) — **yeniden kurulmayacak** | ~$5 | isabetsizlik ↓ **ve** kütle ↑, gözle okumayla; kapı maddesi (2) gerilemedi |
| **B-3** | **B4 · `τ_a` genliği** — merge'de 0,987 → 0,766 (−22,1 p) seyreliyor; teşhis **genlik** (70 adım @1e-5 → ‖τ_a‖ 1,1806 ↔ ‖τ_g‖ 10,4722, oran 8,87×). Kaldıraç: **aynı ORPO ile daha çok adım / daha yüksek lr**. ⛔ Yöntemi de değiştirmek iki değişkeni birlikte oynatır (ADR-0017) | ~$1,3 | ‖τ_a‖ ölçülür; merge sonrası M2b yükselir |
| **B-4** | **YB2 · M2b eğitim borcu** — kapı yolu ölçülerek öldü (`h2b@k=4` 0,735 < 0,766) | tur içinde | M2b ≥ yeni çıpa |
| **B-5** | **Kapı koşusu** (§3, üç madde + gözle okuma) | ~$1 | geçerse **`v1.0`**; geçmezse sayı **damgalanarak** yayımlanır ve `v0.x` devam |

**⛔ GRPO / RLVR ertelendi (ADR-0066).** Verifier'lar zaten deterministik ve programatik
(`atif_dogrula.py` · `groundedness.py` · `score_abstention.py`) — yani B1 **doğrulanabilir ödül**
problemine birebir uyuyor ve SFT bunu ancak taklit ederken RLVR doğrudan cezalandırır. **Ama**
8-16 rollout/istem × (1024+512) bütçe → **$10-30 tahmin** (Modal'da **$29,19**), ve tahmin
**ölçülmedi**. Karar: **önce ucuz olan**; reddetme-örneklemesi kapı maddesini geçirmezse GRPO
kendi ADR'si ve kendi bütçe kapısıyla açılır.

## 7. Hat C — metodoloji paper'ı (yan ürün)

Savunulacak iddia **ölçüm kaydında zaten duruyor**, yeni koşu gerektirmiyor: cevaba bağlı payda
(K3: payda modele bağımlıydı, üç kol 45/56/50 → **68**) · hakem yığını kayması · yeniden-koşum
gürültü tabanı (0,3 p, **yalnız A1 için**) · eşit sınav kapısı (ADR-0057) · **ve bir çekinme
dedektörünün istem rejimine bağımlı çıkması** — *"en büyük kusur"* sandığımızın **%43'ü ölçüm
aletiydi** (14/80 → 8/80). `v1.0` sonrası.

---

## 8. Yazılacak belgeler ve kabul ölçütleri

| belge | taşıdığı | `verify:` |
| :--- | :--- | :--- |
| **`PRODUCT.md`** | vatandaş kim · hangi soruyu soruyor · cevap neye benziyor · **vaat ETMEDİĞİ** (hukuki tavsiye değil · güncellik indeksin işi · %100 doğruluk değil) · v1↔v2 sınırı · üç maddeli kapı · iki sürüm şeması | her nicelik yanında **kaynak dosya adı** taşır; "vaat etmiyor" bölümü var |
| **`ROADMAP.md`** | Faz 0 → Hat A ∥ Hat B → kapı → `v1.0` → v2. Her adım: *ne · neden (hangi ölçülmüş boşluk) · `verify:` · bedel · bağımlılık* | kritik yol işaretli; **AÇIK KARAR** damgaları S5·S7·S8·S9·S10·S12 |
| **`TODO.md`** | yalnız **bugün koşulabilir** kalemler (F0.1-F0.3, A1) | her satır bir ROADMAP adımına bağlı |
| **`docs/MIMARI.md`** | v1 zinciri: base → kollar → merge → GGUF → retriever → istem → CLI · v2 app katmanı sınırı · `referans-design-doc.md`'nin işlevini devralır | her kutu bir **var olan** dosyaya ya da bir ROADMAP adımına işaret eder |

**Son adım (belgeler var olduktan SONRA):** `CLAUDE.md` · `MODEL_CARD.md` · `README.md` ·
`README.tr.md` + kalan dört belgenin kırık linkleri onarılır.
`verify:` → `grep -rE '(ROADMAP|TODO|TASARIM|VISION|PAPER_TARGET)\.md|_arsiv/'` yalnız **yeni**
dosyalara işaret eden isabetler döner.

## 9. Kaderi belirsiz belgeler — tek tek karar

| belge | **KARAR** | gerekçe |
| :--- | :--- | :--- |
| `docs/FINE_TUNING.md` | **KALSIN**, işaretçi onarılsın | yerel donanım + Unsloth/bitsandbytes yığınının tek düzyazı kaynağı; bayat damgası üstünde |
| `docs/VERI_PLANI.md` | **KALSIN**, işaretçi onarılsın | EDA sert kuralının ve lisans temizliğinin **gerekçesi** yalnız burada |
| `docs/YARGI_KAYNAKLARI.md` | **KALSIN**, işaretçi onarılsın | sökülmüş API sözleşmeleri; v2 içtihat katmanı buradan başlar |
| `docs/open_questions.md` | **KALSIN + kendi kuralı uygulansın** | otoritesi `PRODUCT.md`'ye taşınır; kapanan **S1/S2/S11/S14** ADR'lere işlenip **kapanış dizinine** geçer (iz kalır, gövdeden çıkar); S5-S13 canlı kalır |
| `docs/model-soyagaci.mmd` | **KALSIN**, işaretçi onarılsın | kolların bağımsızlığını ve merge'in zincir **olmadığını** tek bakışta anlatıyor |
| `referans-design-doc.md` | 🗑️ **SİLİNİR** → yerine `docs/MIMARI.md` | insan kararı: *"güncel hedefe göre yenisi yazılsın"* |

## 10. Yan bulgular — bu oturumda ölçüldü, düzeltilmedi

- **TRL zaten kullanılıyor.** `scripts/train_sft.py:28` → `from trl import SFTTrainer, SFTConfig`
  (`τ_g`) · `scripts/train_orpo.py:27` → `from trl import ORPOTrainer, ORPOConfig` + `MaskedORPOTrainer`
  (`τ_a`) · `trl==0.24.0` pinli. Unsloth TRL'nin **alternatifi değil, altındaki yama katmanı**:
  `PatchDPOTrainer()` TRL trainer'larını Unsloth çekirdeklerine uyarlıyor.
  **REJECTED — `Axolotl`/`LLaMA-Factory`:** TRL+PEFT üstüne YAML sarmalayıcı; yeni yetenek sıfır,
  bedeli doğrulanmış hattın (Modal taşıyıcıları, seed'ler, `--fresh-adapter` semantiği) yeniden
  doğrulanması. **REJECTED — `verl`/`OpenRLHF`:** tek L4 + 4B için fazla büyük.
  **REJECTED — `mergekit`:** `merge_ties.py` doğrulanmış (224/224 tensör, host-RAM akışı) ve
  semantiği ADR-0052'yle çivili; ölçülmüş bir soruyu yeniden açar.
- **`train_orpo.py` docstring'i BAYAT** — *"base = v2b ADAPTER'dan DEVAM"* diyor, bu bugünkü
  ham-base kuralına aykırı bir kalıp. Kural **ihlal edilmedi**: `kollar.md`:64 `τ_a v1`'in
  **`--fresh-adapter`** ile koştuğunu gösteriyor. Yalnız docstring yanıltıcı → TODO.
