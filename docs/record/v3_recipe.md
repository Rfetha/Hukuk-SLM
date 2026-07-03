# v3 RECIPE — near-miss abstention fix (ORPO, grilling ürünü)

> **Ne:** v2c RED'inden sonra, near-miss (topik-komşu yanlış-kaynak) abstention'ı düzeltmek için v3 reçetesi.
> **Nasıl doğdu:** [[v2c_sonuclar]] + [[v2c_fix_deep_research]] (5 aile + Gemini) → **grilling oturumu** (2026-07-03, 8 düğüm).
> **Otorite:** bu doküman v3'ün KARAR belgesi. Kronoloji [[research_log]] · red kararı ADR-0014 · sonuç → ADR-0015 (yazılacak).
> **Durum:** tasarım KİLİTLİ (8 düğüm) · hiperparametre + kod bekliyor · eğitim = Modal para-kapısı + kullanıcı onayı.

---

## 🔑 v3'ü doğuran iki bulgu

**Bulgu-1 (K3, v2c'den):** near-miss abstention **düz SFT ile öğrenilemiyor.** SFT coverage kazandırır (over-refusal↓) ama ayrım gücünü bozar ("Grounding-Abstention paradoksu"). → teslim SFT değil, **preference (ORPO)** olmalı.

**Bulgu-2 (YENİ, grilling'de kod okumasından — K3'ü RAFİNE eder):** v2c'nin near-miss eğitim verisi **eval'den TERS sertlikte** kurulmuş:
- Eğitim `pick_wrong_neighbor` (build_sft_v2b.py:245) = soruyla **EN DÜŞÜK** leksik örtüşen yanlış madde → **kolay-reddedilir**.
- Eval M2 `build_eval_sets.py:124` = "**en yüksek** kelime-örtüşmeli kardeş (topic-near)" → **zor-reddedilir**.
- Sonuç: model "kelimeler tutmuyorsa reddet" sığ sezgisi öğrendi → M2b (bariz-off-topic) ✅ geçti ama M2 (yüksek-örtüşme) ❌ çöktü. **Mükemmel ORPO bile kolay-negatifle eğitilirse zor-eval'de çöker.**
- → v3 iki cephede düzeltir: **teslim (SFT→ORPO)** VE **veri-sertliği (kolay→spektrum, yüksek-örtüşme ağırlıklı)**.

> Paper notu: bu, K3'ün tek-sebepli anlatısını **iki-sebepli**ye çevirir (teslim + veri-sertliği). Temiz ablasyon ikisini ayırırdı ama v3 pragmatik olarak ikisini birden düzeltir; ayrıştırma opsiyonel ablasyon kolu.

---

## Kilitli kararlar (grilling, 8 düğüm)

| # | Düğüm | Karar |
|---|---|---|
| **Q1** | Yöntem + kapı | **ORPO** (Modal A100). Kapı: **M2 ≥0.704** (base'i NET geç) **+ M1 A1 ≥0.904** (regresyon yok) + tavan koru (M4/M2b/M3/register) + M5 base-altı. Üstünlük (M2 0.90) = ara-hedef/bonus, RED değil. **DTA = opsiyonel 2. aşama.** |
| **Q2** | Checkpoint | **base = v2b adapter** (M1 kapısı zaten geçili). v2c'nin **verisi** ORPO-chosen'a taşınır, **ağırlığı** atılır (M1-regresyonunu sırtlamamak için). |
| **Q3** | Near-miss sertlik | **Spektrum** (tüm örtüşme bandı, **eval M2-tipi yüksek-örtüşme AĞIRLIKLI**) + **geçerlilik kapısı.** "Kaynak yasal cevaplamıyorsa reddet" genel ilkesi, leksik sezgi değil. |
| **Q4** | ORPO çifti | **rejected = v2b'nin gerçek fabrikasyonu** (zor-bağlamda örnekle; çekimser kaldığını atla → zor-negatif küratörü, ~$0). **chosen = muhakemeli-red şablonu** (yanlış-madde konusunu adlandırır, teacher'sız $0, kıyaslanabilir uzunluk → format/uzunluk-bias↓). |
| **Q5** | Geçerlilik kapısı | **Çift-eksen deterministik:** sertlik = overlap(yanlış, **SORU**)↑ · geçerlilik = overlap(yanlış, **GOLD-CEVAP**) < τ (kazara-cevaplayanı ele, $0). + **judge-audit** → τ kalibre. ⚠️ **Geri bildirim-3 (overlap gürültülü):** τ = tek sayı DEĞİL → **gri-bant** [τ_lo, τ_hi]; bant-altı=otomatik geçer, bant-üstü=otomatik eler, **yalnız bant-içi judge'a** gider (funnel sağlığı + gürültü-emniyeti). |
| **Q6** | Kompozisyon | **Pref-ağırlıklı:** abstain-çifti (ORPO) = MAX üretilebilir. Grounding = **hafif SFT-replay** (rejected'sız NLL, unutmama-boyutu). base=v2b zaten ground'ladığı için sinyali M2 açığına yoğunlaştır. |
| **Q7** | Doğrulama | **Held-out zor-near-miss dev-set** (~80, eğitim+eval'den ayrık) → ORPO tuning. **İki-kademe eval:** karar kanon n=40/35 (skorkart-uyumlu); umutluysa teyit n≥100 + base/v2b re-eval. |
| **Q8** | Bağlam yapısı | **Tek yanlış-kaynak AĞIRLIKLI** (eval M2 oracle yapısına eş) + az çok-kaynak (yanlış+uzak-distractor, deploy'a genelleme). |

---

## ÇÖZÜLDÜ — mixed-objective mimarisi (TRL 0.24.0 kaynak-doğrulamalı, 2026-07-03)

> Kaynak: `trl/trainer/orpo_trainer.py` okundu. `loss = policy_nll_loss − beta·losses.mean()` (satır 830); NLL **yalnız chosen** (satır 781, `all_logits[:len_chosen]`); OR-terimi `losses` **per-örnek** (satır 675); `concatenated_forward` chosen+rejected'ı birleştirir → rejected **şekil için zorunlu** ama **NLL'e girmez.**

- **İki açık kutu (mixed-objective + ORPO-continuation) tek kararla kapandı: HİBRİT.**
  - **Grounding-replay satırı = placeholder rejected + maskeli OR.** Grounding satırına atıl bir rejected string konur (concat şekli sağlam kalsın, standart TRL collator bozulmaz). `ORPOTrainer` subclass'ı per-satır `is_pref` maskesi taşır; grounding satırında OR-terimi sıfırlanır. Sonuç: grounding satırı **yalnız NLL(chosen)** katkısı verir = tam olarak istenen SFT-replay. Placeholder içeriği loss'a **dokunmaz** (NLL'e girmez + OR maskeli) → sahte kontrast öğretmez. ~15 satır subclass, sıfırdan loss YOK.
    - ⚠️ **NaN-güvenliği (kritik, geri bildirim-4):** OR-loss `log1p(-exp(rejected_logps))` içerir (satır 672); placeholder tek yüksek-olasılıklı token olursa `exp→1 → log(0)=-inf → NaN`, ve bu maskeden ÖNCE hesaplanır. `nan*0=nan` (IEEE) → `losses*mask` tüm batch'i zehirler. **Doğru maske: `losses = torch.where(is_pref, losses, torch.zeros_like(losses))`** (seçilmeyen daldan NaN taşımaz), sonra `losses.sum()/is_pref.sum().clamp(min=1)`.
    - **Placeholder seçimi:** kısa sabit metin (~10-20 sıradan token). Kısa = compute israfı yok (içerik atıl); tek-token DEĞİL = avg-logprob 0'dan uzak, ikincil sayısal hijyen. Asıl güvence yine `torch.where`.
    - **Batch-varyansı (geri bildirim-4):** maskeli-mean micro-batch'te normalize eder → rastgele shuffle bazı batch'leri %90 grounding yapıp OR-sinyalini zayıflatabilir. Çözüm: `is_pref` **deterministik interleave** (Q6 oranında sabit örüntü, random-shuffle değil → fixed-seed reproducibility'ye uyumlu) + `per_device × grad_accum ≥ 64` çift emniyet.
  - **Continuation cevabı:** ORPO NLL-terimi zaten chosen üzerinde SFT-loss'u içeriyor; v2b adapter'dan devam TRL'de sorunsuz (base-şart değil). DPO-continuation'a gerek yok.
  - **"λ" = `ORPOConfig.beta`** (ayrı param değil). Reçetedeki λ=0.1 → `beta=0.1`.

## Açık kalan (hiperparametre — dev-set'te ayarlanır, öneri-varsayılan)

- **ORPO beta** (=eski "λ", OR ceza ağırlığı): öneri **0.1** (ORPO paper varsayılanı) → dev'de {0.05, 0.1, 0.25} tara. ⚠️ M1 çökerse (catastrophic-forget, geri bildirim-2) 0.1→**0.05** düşür VEYA grounding-replay oranını artır.
- **lr:** v2b'den devam (zaten SFT'li) → düşük, öneri **5e-6–1e-5** (tam SFT lr=1e-4'ten düşük; over-write etmesin).
- **epoch:** öneri 1 (v2b gibi); dev-loss'a göre 2.
- **grounding-replay oranı:** funnel çıktısına göre (Q6) → abstain-çifti hacmi ölçülünce sabitlenir. **M1-koruma kaldıracı:** forget riskinde ilk artırılacak knob.

---

## §5 — TEK NUMARALI AKIŞ (aç-koş) — v3 execution

> Kural: her adım biter → research_log + bu dosya güncel. Modal eğitim = para-kapısı + kullanıcı onayı (sormadan başlama). Eval = lokal RTX 5070.

1. **Veri-üretim kodu (yeni).** `build_sft_v3.py` (veya build_sft_v2b'ye v3-mod):
   1a. `pick_hard_neighbor()` — YENİ: overlap(yanlış, SORU) MAKSİMİZE (mevcut min'in TERSİ) + sertlik-spektrum örnekleme (yüksek ağırlıklı).
   1b. Geçerlilik kapısı — overlap(yanlış, GOLD-CEVAP) < τ deterministik filtre.
   1c. Bağlam yapısı — tek-kaynak ağırlıklı, az çok-kaynak (Q8).
2. **Rejected üretimi (v2b örnekleme).** v2b'yi zor near-miss bağlamlarda çalıştır → fabrikate edenleri tut (rejected), çekimser kalanı ele. Lokal, ~$0.
3. **Chosen üretimi (muhakemeli-red şablon).** Yanlış-madde konusunu çıkar → şablon doldur. Grounding chosen = v2b'nin mevcut grounded cevapları (reuse, $0).
4. **Geçerlilik kalibrasyonu.** ~30 negatifi judge'a ver → τ eşiğini ayarla → funnel'ı raporla (kaç geçerli zor-çift üretildi).
5. **Dev-set kur.** ~80 zor-near-miss, eğitim seed'lerinden VE eval trap.jsonl'dan ayrık. Sızıntı-kontrol.
6. **ORPO paketleme.** abstain-çifti (chosen/rejected) + grounding-replay (NLL) → v3 train.jsonl. Kompozisyon Q6.
7. **Smoke (Modal, --detach, ~50 step, ~$0.15).** Veri yükleniyor mu, loss düşüyor mu, OOM yok mu. ⚠️ **Geri bildirim-7 (kritik erken-yakalama):** ek olarak **format/tokenizer denetimi** — birkaç paketlenmiş örneği **decode et**, chat-template doğru mu, chosen/rejected label-maskeleri (prompt maskeli mi, `label_pad_token_id`) kaymış mı, `is_pref` maskesi doğru satıra mı düşüyor? Bunlar tam eğitim bitince fark edilirse pahalıya patlar.
8. **v3 tam eğitim (Modal A100, --detach, onay-sonrası).** base=v2b adapter, ORPO (`beta`), hiperparam Q-açık. ⚠️ **Geri bildirim-2 (forget-izleme):** dev-loss'a güvenme → **grounding `nll_loss` trendini** (TRL zaten logluyor) forget-vekili say; tırmanıyorsa M1 risk. Ara-checkpoint → lokal M1 spot-eval. Çökerse: `beta`↓ (0.1→0.05) veya replay↑.
9. **Kanon eval (lokal, n=40/35).** 6-mod + register + M5 → skorkart. Kapı Q1.
10. **Karar.** Kapı geçti → (opsiyonel) n≥100 teyit + base/v2b re-eval → **ADR-0015** (v3 kabul/red). Geçmedi → funnel/sertlik/λ hata-analizi; gerekirse DTA (2. aşama) veya base-joint-ORPO (Q2-alternatif).
11. **Belgele.** research_log v3 girişi (sayılar kaynaklı) + v3_sonuclar.md + skorkart Mecellem sütunuyla.

---

## Bağlam / kaynak
- Red kararı + fix-havuzu: **ADR-0014** (P1–P6). v3 = P1(ORPO) birincil + P6(veri-kompozisyon) kaldıraç; P2(DTA) opsiyonel 2. aşama.
- Fix literatürü: [[v2c_fix_deep_research]] (ORPO 2403.07691 · DTA 2505.20871 · RAFT-uyarı · format-bias 2409.11704).
- Kod dokunulacak: `scripts/build_sft_v2b.py` (pick_wrong_neighbor→hard, çift-eksen geçerlilik kapısı+gri-bant), `gen_v2b_answers.py` (muhakemeli-red şablon), `modal_train.py` (ORPO entrypoint + **`MaskedORPOTrainer` subclass** — per-satır `is_pref` OR-maskesi, ~15 satır), `scripts/build_eval_sets.py` (dev-set üretici). ORPO veri şeması: her satır `{prompt, chosen, rejected, is_pref}`; grounding satırı `is_pref=False` + placeholder rejected.
- Değişmez: lisans-temiz veri · Modal --detach · para-kapısı · Mecellem sütunu her skorkartta.
