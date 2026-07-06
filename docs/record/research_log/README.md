# Araştırma Kaydı — kronolojik index

> **Bu klasör ne:** Projenin **deney günlüğü** (makale-sigortası). Her anlamlı deney/bulgu/karar = ayrı
> dated dosya (ADR paterni). İçerik BİREBİR — özet değil. ADR'ler *kararı* tutar; buradaki entry'ler
> *anlatıyı + sayıları + öğrenilen dersi* tutar. Yeni entry → bu klasöre yeni `YYYY-MM-DD-slug.md` +
> aşağıdaki tabloya satır.
>
> **Çerçeve + künye (model/metrik/eval-modları):** [`00-kunye-ve-cerceve.md`](00-kunye-ve-cerceve.md).
> **Paper eşlemesi (K1/K3 haritası):** [`99-paper-esleme.md`](99-paper-esleme.md).
> **Paper haritası:** K1=ablasyon, K3=ayrışma/negatif bulgular. Detay: `docs/PAPER_TARGET.md` · Kararlar: `docs/adr/`.

## Kronoloji (eski→yeni; sıra korunur)

| # | Tarih | Başlık | Kanca |
|---|---|---|---|
| 01 | ~2026-05/06 | [Çerçeve + planlama](2026-05-cerceve-planlama.md) | private repo + Gemma 4 12B + Modal; veri kuralı; niş+sistem paper |
| 02 | 2026-06-07/08 | [v0 (forum verisi) → BAŞARISIZ](2026-06-07-v0-forum-basarisiz.md) | forum QA modeli batırdı; "7 Kasım 1982" 154× ezber (K3) |
| 03 | 2026-06-08 | [Grounded pivot → v1 verisi + kalite kapısı](2026-06-08-grounded-pivot-v1-veri.md) | 21.458 grounded Q&A, faithfulness 0.984 kapısı |
| 04 | 2026-06-09 | [v1 SFT eğitimi (Modal A100)](2026-06-09-v1-sft-egitimi.md) | 1 epoch; spawn() fire-and-forget dersi (ADR-0008) |
| 05 | 2026-06-12 | [Dış v2-analiz raporu → ADR-0009](2026-06-12-dis-v2-analiz-adr0009.md) | "filtre gevşek" iddiası import-doğrulamayla FABRİKASYON çıktı |
| 06 | 2026-06-13 | [base vs v1: KÖR vs MADDE-VERİLİ ⭐](2026-06-13-base-vs-v1-kor-madde-verili.md) | KÖR test artefaktı; madde verilince faith 0.52→0.97; SFT base'i geçmedi |
| 07 | 2026-06-13 (akşam) | [BENCHMARK RUN ⭐⭐](2026-06-13-aksam-benchmark-run.md) | SFT abstention'ı YOK ETTİ (0.786→0.000); v1 tek kazanım = atıf formatı |
| 08 | 2026-06-13 (gece) | [CANON eval metodolojisi → ADR-0011 ⭐](2026-06-13-gece-canon-metodoloji-adr0011.md) | 4 eksen A1/A2/A3/A4 mod-stratifiye; /deep-research 22 kaynak |
| 09 | 2026-06-13 (gece) | [CANON PİLOT → Product A ⭐⭐⭐](2026-06-13-gece-canon-pilot-product-a.md) | scope=Product A (ADR-0012); v1 net-negatif; SFT üslup öğretir bilgi değil |
| 10 | 2026-06-14 | [2 /deep-research → V2_PLAN](2026-06-14-iki-deep-research-v2plan.md) | Suff-Context selective-gen + RAFT + EntiGraph-CPT; 3-adım karar ağacı |
| 11 | 2026-06-14 | [3. /deep-research (FT-reçete) → v2b kartı](2026-06-14-uc-deep-research-ft-recete.md) | RAFT/hedge-oranı/Cor-RAIT/replay; keyfi %15/%25 çürüdü |
| 12 | 2026-06-14 | [v2 plan oturumu → ADR-0013](2026-06-14-v2-plan-oturumu-adr0013.md) | PLAN A (SFT+RAG, CPT'siz); SFT hedef tanımı; 5-mod eval matrisi |
| 13 | 2026-06-14 | [v2b execution: blocker'lar temizlendi](2026-06-14-v2b-execution-blocker.md) | raft_pack + build_sft_v2b + eval mod'ları (compute'suz kod) |
| 14 | 2026-06-14 | [A+B paralel + B1 veri-bozukluğu bug'ı](2026-06-14-ab-paralel-b1-veri-bozuklugu.md) | gold_text=provenance-tag sessiz bozukluk; smoke yakaladı |
| 15 | 2026-06-24 | [v2b veri tamamlandı + replay + truncation fix](2026-06-24-v2b-veri-tamamlandi-replay.md) | 19.305 cevap; replay 600; uzun-madde clip 900-char (%11.6→%0.03) |
| 16 | 2026-07-02 | [v2b tam eğitim BİTTİ + 🔴 GOLD-sızıntı](2026-07-02-v2b-egitim-bitti-gold-sizinti.md) | 6-mod D1: v2b tüm kapıları geçti; GOLD jargonu %5.7 sızmış |
| 17 | 2026-07-02 | [v2c ADIM 1: register ölçümü](2026-07-02-v2c-adim1-register-olcumu.md) | v2b register-proxy = 1.000 (tam uzman); regresyon alt-sınırı |
| 18 | 2026-07-02 | [v2c ADIM 3-5: position-bias + GOLD-scrub + hijyen](2026-07-02-v2c-adim3-5-hijyen.md) | pozisyon-bias yok; GOLD-scrub 1157→0; core_hard #28/#29 belge |
| 19 | 2026-07-02 | [v2c ADIM 6a+6b: Tier A kod + eğitim verisi](2026-07-02-v2c-adim6ab-egitim-verisi.md) | counterfactual+abstain_trap slice; sft_v2c train 17353 (API=$0) |
| 20 | 2026-07-02 | [🔴 CANLI DURUM SNAPSHOT](2026-07-02-canli-durum-snapshot.md) | compact-sigortası: v2c eğitim + C3 baseline eşzamanlı koşuyordu |
| 21 | 2026-07-02 | [v2c ADIM 6c: Modal eğitim BAŞLADI](2026-07-02-v2c-adim6c-modal-egitim-basladi.md) | smoke GREEN; --detach ŞART; erken elmayla-elma v2b>base coverage |
| 22 | 2026-07-02 | [v2c ADIM 2: base vs v2b tam tablo](2026-07-02-v2c-adim2-base-vs-v2b-tablo.md) | base her yerde over-refuse; v2b tek açık M2=0.346 |
| 23 | 2026-07-02 | [v2c ADIM 2 · C4 Mecellem → TABLO 1](2026-07-02-v2c-adim2-c4-mecellem-tablo1.md) | rakip lm_head=0 fix; coverage'da v2b 2×; Mecellem eval'i sadece perplexity |
| 24 | 2026-07-03 | [v2c TAM SKORKART + ❌ RED + K3](2026-07-03-v2c-tam-skorkart-red-karari.md) | M2 0.407«0.90 + M1 regresyon → RED; Grounding-Abstention paradoksu |
| 25 | 2026-07-03 | [v3 ADIM 1: near-miss trap + EVAL-AYNASI](2026-07-03-v3-adim1-near-miss-trap.md) | hard-negative dağılımını eval ile eşle (kapsama %6.6→%66.3) |
| 26 | 2026-07-04 | [v3 ADIM 2-6: rejected harvest + FRAMING](2026-07-04-v3-adim2-6-rejected-harvest.md) | eval M2=ORACLE keşfi (Bulgu-3); offline ORPO pipeline; mojibake fix |
| 27 | 2026-07-05 | [v3 ADIM 2 KOŞTU + 6a paketlendi](2026-07-05-v3-adim2-kostu-orpo-hazir.md) | harvest fab=0.870 (K3 funnel); ORPO train 1741/val 53 hazır |
| 28 | 2026-07-05 | [v3 genelleme eval-dilimleri + 🔴 OOD-bloklu](2026-07-05-v3-genelleme-eval-dilimleri.md) | çapraz-kanun DRAFT; eval kanun-kapsamı = train kanun-kapsamı sınırı |
| 29 | 2026-07-05 | [v3 OOD BLOĞU AÇILDI](2026-07-05-v3-ood-blogu-acildi.md) | held-out 7-kanun grounded-sentetik OOD (35); temporal/çok-hop defer |
| 30 | 2026-07-05 | [v3 ADIM 7 smoke + ADIM 8 ORPO eğitim BİTTİ ⭐](2026-07-05-v3-adim7-8-orpo-egitim-bitti.md) | 56/56 step 2ep; nll 7.65→2.96 (forget YOK) + margin -0.31→~0 (M2 öğrenildi); ckpt-28+final volume'de; ADIM 9'a hazır |
| 31 | 2026-07-06 | [Mecellem konumlama + strateji (benchmark beklerken)](2026-07-06-mecellem-konumlama-strateji.md) | rakip = CPT foundation base (M4 0.78/reg 0.2/M5 0.35); biz grounding+register makinesi; M2=1.0 patoloji, hedef 0.8-0.9 korunmuş-grounding; CPT'yi geçme→RAG ile alakasızlaştır (paper Tablo 1 + Tartışma) |
| 32 | 2026-07-06 | [v3 ADIM 9 SONUÇ — tam judge + kapı kararı (KISMİ) + M2b teşhis ⭐](2026-07-06-v3-eval-sonuc-kapi-karari.md) | v3 K3'ü onardı (M2 0.35→0.59, M1 0.74→**0.88**) ama base-M2'yi geçmedi (0.593<0.704) + **M2b regresyon 0.96→0.53** (forced-source-selection bias); teslim değil, v4 yönü NET = #2b multi-distractor-no-gold hard-neg (ADR-0015) |

> **Not (2026-07-05 restructure):** eski tek-dosya `research_log.md` bu klasöre bölündü (içerik birebir).
> Dosya-dibindeki "Açık kararlar / sıradaki" TODO bölümü tarihsel kayıttan çıkarıldı → canlı maddeler
> `TODO.md`'ye taşındı, tamamlanan/superseded olanlar kapatıldı. Turların özet + karar belgeleri:
> [`../v2b/`](../v2b/) · [`../v2c/`](../v2c/) · [`../v3/`](../v3/) · ana harita [`../README.md`](../README.md).
