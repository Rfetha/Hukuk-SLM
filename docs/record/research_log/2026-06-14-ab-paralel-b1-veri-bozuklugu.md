### 2026-06-14 — A+B paralel koşu + B1 veri-bozukluğu bug'ı (smoke yakaladı)
Kullanıcı "A+B paralel başlat" dedi. A (GPU eval) lokal RTX 5070 Ti'de (12GB boş), B (API) gpt-4o-mini.
- **A-track:** M1 (gold+4 distractor) + M3 (empty-context) base baseline — `gen_eval_grounded.py`, lokal 4-bit 12B, ardışık (tek GPU).
- **B-track BUG (kritik, smoke yakaladı):** B2 smoke (20 satır) → assemble gate **16/16 grounded RED** ("alıntı gold'da değil"). Kök-neden: **B1 pack yanlış alanı gold_text sanıyordu** — `sft_v1/train.jsonl`'deki `source` alanı madde metni DEĞİL, provenance etiketi (`'grounded_gpt-4o-mini'`). Gerçek madde metni sft_v1'de YOK; `mevzuat_maddeler.jsonl`'den `(kanun_no|madde_no)` ile JOIN edilmeli (gen_eval_grounded zaten öyle yapıyor — eğitim tarafı atlanmış). JOIN kapsamı %100 (19.305/19.305, format uyumlu "MADDE 6").
- **Düzeltme:** `build_sft_v2b.py`'ye `load_madde_index` + `extract_seed(rec, madde_idx)` JOIN eklendi; gate'e tırnak-soyutlama (`strip`) — teacher metni `"..."` sarınca eşleşme kırılıyordu. Pack yeniden koştu → gold_text artık gerçek (TKHK M6 "Vitrinde... satışından kaçınılamaz" ↔ soru eşleşiyor). Smoke tekrar → **gate 19/20 geçti** (1 ret = teacher distractor'dan alıntı yaptı, gate DOĞRU eledi = kapının asıl işi).
- **Ders (paper/methodology):** smoke-test (~16 çağrı, cent'ler) tam B2 (~15K çağrı, ~$9) öncesi veri-bozukluğunu yakaladı → "EDA-verify her dataset" disiplini burada da ödedi. Gold-text-as-provenance-tag = sessiz bozukluk; deterministik gate (verbatim⊂gold) onu görünür yaptı. → tam B2 başlatıldı.

#### A-track BASELINE sonuçları (base, gemma-4-12B, n=40, gpt-4o-mini judge)
v2b SFT'nin **yeneceği/koruyacağı** çıpa sayıları (yeni M1/M3 modları, ADR-0013):
- **M1 (gold+4 distractor, A1 groundedness):** faithfulness_micro=**0.879**, hallucination_micro=0.122, cit_precision_micro=0.905, wrong_ref_rate=0.095, faithfulness_macro=0.742. Dosya `outputs/eval/gnd_bench_m1_base_summary.json`. → Base distractor-gürültüsünde %88 sadık; v2b bunu **koru/artır**.
- **M3 (empty-context, A3 abstention, deterministik):** rejection_rate=**1.000** (40/40), fabrication=0.000. → **Base boş bağlamda kusursuz çekiniyor.** v2b'nin asıl riski bu sayıyı BOZMAK (v1 abstention çöküşü 0.74→0.00 = Cor-RAIT over-refusal'ın TERSİ: SFT burada fabrikasyona kaydı). CRaFT/replay reçetesi tam bunu korumak için.
- **Okuma:** base zaten iyi bir RAG-okuyucu+çekinici. v2b'nin işi yeni yetenek eklemek değil, bu iki davranışı (faithful-when-grounded ∧ abstain-when-empty) SFT sonrası KORUYABİLDİĞİNİ + uzman-register + verbatim-quote format eklemek. Headline ablasyon: base vs v2b, AYNI M1/M3 modunda.

#### C1 EĞİTİM ALTYAPISI hazırlandı (B akarken, kod-only)
v2b Modal eğitim hattı kuruldu — mevcut v1 altyapısı (`train_sft.py` + `modal_train.py`) reçeteye (§5.1) uyarlandı:
- **`train_sft.py`:** (a) `--warmup-ratio` flag (sweep, §5.1-C %3-5); (b) `--allow-high-lr` + **3e-4 GÜVENLİK KİLİDİ** — lr≥3e-4 normalde `SystemExit` (v1 abstention-çöküşü rejimi = continual-pretrain re-warming, 2403.08763/2503.02844; davranışsal SFT'de yasak). Test: 1e-4/2e-4 geçer, 3e-4 blok, `--allow-high-lr` açar.
- **`modal_train.py::spawn_v2b`:** fire-and-forget v2b entrypoint, reçete varsayılanları (lr=1e-4 = LoRA≈10x-full-FT, r=16/α=32, warmup=0.05, 1 epoch, `--no-system`). **Kilit tasarım:** `--no-system` zorunlu çünkü v2b verisi `SYSTEM_PROMPT_RAG_MULTI`'yi `messages[0]`'da TAŞIR (assemble gömüyor) → v1 gibi system eklenirse ÇİFT system olur. Ablasyon (C2) için lr/rank/data parametrik.
- **Çalıştırma sırası (B+assemble bitince):**
  1. `modal volume put hukuk-data data/processed/sft_v2b /sft_v2b`
  2. `modal run modal_train.py::spawn_v2b --smoke` (50 step, ~$0.15, loss düşüyor mu)
  3. `modal run modal_train.py::spawn_v2b --run-name v2b --epochs 1` (tam, fire-and-forget)
  4. `modal volume get hukuk-outputs /v2b ./outputs/v2b` → D1 canon eval (M1/M3 v2b)
- **Henüz YOK:** v2b train.jsonl (B2→assemble üretecek) → smoke ancak ondan sonra. requirements.lock + volume'lar v1'den hazır.

#### B2 paralelizasyon + Tier 1 RPD duvarı + topik-skew dersi
- **Paralelize edildi:** `gen_v2b_answers.py` `--workers` (ThreadPool + yazım-lock + resume korundu). İki bug bulundu+çözüldü: (a) **timeout'suz OpenAI client** paralel koşuda asılı sokette tüm worker'ları kilitliyor → `timeout=30, max_retries=0` (kendi exp-backoff'umuz var); (b) **6 worker Tier 1 TPM 200K tavanına biniyor** → 429 → default 4 worker (~160K TPM güvenli). Ağ-değişimine dayanıklılık kanıtlandı (stale-conn timeout→retry self-heal).
- **🔴 Tier 1 RPD duvarı (10.000 istek/gün):** ~10K çağrıdan sonra `429 ... requests per day (RPD): Limit 10000, Used 10000`. Bugün B2 14.800/19.305'te durdu. Reset ~gece yarısı UTC. (İlk RPD tahminim doğruymuş; v1 muhtemelen <10K veya güne yayılmıştı.)
- **🔴 TOPİK-SKEW dersi (kullanıcı yakaladı):** seed dosyası (`sft_v1/train.jsonl`) **kanuna göre SIRALI** (id boyunca 18 kanun-değişimi = blok blok), shuffle DEĞİL. → ilk 14.800'ü almak rastgele örnek değil: **İCRA VE İFLAS KANUNU (2.727, ~%14) ve KAT MÜLKİYETİ üretilende SIFIR.** Slice oranı (80/20) korunur ama **topik dağılım bozulur.** → "eldekiyle eğit" İPTAL; tam set ZORUNLU. **Ders:** partial-tolerant pipeline için seed'ler pack'te SHUFFLE'lanmalıydı; aksi halde yarıda-kesilme = sistematik kapsama deliği. (Paper-methodology: veri-üretim sırası temsililiği.)
- **Karar:** RPD reset bekle → resume (kalan ~4.505, İİK dahil) → assemble → C1. Devir notu: `NEXT_SESSION.md`.

---

