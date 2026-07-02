# v2c GİRDİ — Claude Değerlendirmesi (danışman raporu × v2b ampirik sonuç)

> **Statü:** v2c reçetesi için HAM GİRDİ. Bu doküman [[v2c_input_dis_danisman]]'ın
> önerilerini [[v2b_sonuclar]]'ın GERÇEK ölçümlerine bağlar. Danışman v2b sonuçlarını
> GÖRMEDEN genel öneri verdi; buradaki işim önerileri v2b'nin açık kalan gerçek
> yerlerine oturtmak + nerede ayrıldığımı gerekçelemek.
> **Tarih:** 2026-07-02 · **Yazar:** Claude (bu oturum)
> **Harmanlama kuralı:** v2c hedefi = (v2b_sonuclar kapı-durumu) ∩ (bu iki girdi dokümanı).

---

## 0. Çıkış noktası: v2b GERÇEKTE ne bıraktı? (v2b_sonuclar'dan)
v2b **tüm kapıları geçti** — yani v2c bir "kurtarma" değil, **hedefli robustness turu**.
Geriye kalan 4 açık (danışman bunları bilmiyordu, hedefimiz bunlar):

| # | Açık | v2b sayısı | Sınıf |
|---|---|---|---|
| **G1** | Yanlış-ama-makul kaynakta abstention | M2 Rej\* **0.346** (base 0.786) | 🔴 birincil — tek gerçek gerileme |
| **G2** | Off-by-one yanlış-madde atfı | CMK 109→"110", İş K 55→"56"… (M1 6 vaka) | 🟡 ikincil |
| **G3** | GOLD-jargon sızıntısı | hedeflerin %5.7'si, çıktıda ~1/40 | 🟢 kozmetik |
| **G4** | Register ölçülmedi | — | ⚪ açık eksen (önce ÖLÇ) |

**KORUNACAK taban çizgileri (v2c bunları DÜŞÜRMEMELİ):** M1 A1=0.904 · M4 A1=0.975 ·
M2b abstention 0.96 · M3 1.000 · M5 forgetting 0.175 (base-nötr) · A4 cit_prec 0.925.

---

## 1. Danışman önerileri × v2b gerçeği — madde madde verdikt

### 🔴 En kritik: G1 (M2 abstention 0.346) — danışmanın bakmadığı gerçek hedef
v2b_sonuclar teşhisi net: M2'deki 0.346 kısmen **off-distribution artefakt** (v2b çok-kaynak
RAG_MULTI ile eğitildi, M2 tek-kaynak `--with-source` promptunda ölçüldü) — ama M2b=0.96
adil sayıyı verse de, **"yanlış-ama-makul TEK kaynak var" senaryosunu v2b öğrenmedi**
(research_log: "hiç kaynak yok"ta çekindi, "yanlış-makul kaynak var"da çekinemedi).
→ **v2c'nin 1 numaralı işi:** abstain dilimini **TRAP-tipine** göre yeniden kur
(gold'un yerine tek, makul-ama-yanlış madde koy → doğru cevap = çekinme). Bu bir **VERİ
kompozisyonu** düzeltmesi; danışmanın §3/§6'sı bunu kısmen yakalıyor ama loss/ratio'ya
yıkıyor — asıl kaldıraç veri.

### FT yöntemleri (§1)
| Öneri | Danışman | Benim verdiktim | Gerekçe (v2b-özgü) |
|---|---|---|---|
| **rsLoRA** | KULLAN/P0 "sıfır maliyet" | ⚠️ **AYRILIYORUM — P0 değil, ayrı ablasyon kolu** | r=16'da α/r=2.0 → α/√r=8.0 = **4× daha büyük efektif güncelleme**. Bu "bedava stabilizasyon" DEĞİL; özenle ayarlanmış lr=1e-4'ü efektif 4× artırır (3e-4 zaten elenmişti!). rsLoRA yüksek rank (r≥64) için tasarlandı; r=16'da kazanç marjinal, regresyon riski gerçek. → **DoRA/rank ablasyonuyla birlikte kontrollü kol**, drop-in değil. |
| **DoRA** | DENE/P1 | ✅ **Katılıyorum, P1 ablasyon kolu** | Makul; ama +%10-15 bellek 12B/40GB'da sıkışık — danışmanın dediği gibi önce ~2K örnekte OOM testi. Kazanç kanıtı bizde YOK → sadece ablasyon değeri için. |
| LoRA+ / Full-FT | ELE | ✅ Katılıyorum | Bütçe+bellek; itiraz yok. |

### Abstention / kalibrasyon (§3)
- **Loss masking ×2 (ret token)** — danışman KULLAN/P0. ⚠️ **AYRILIYORUM.** v2b abstention'ı
  eğitildiği yerde ZATEN güçlü (M2b 0.96, M3 1.000). Boşluk G1 = **off-dist/veri** sorunu,
  loss-ağırlık sorunu değil. Ret token'larını 2× yukarı çekmek **over-abstention** → M1 A1
  (0.904) ve cond_acc'i düşürme riski taşır; v2b'de zaten %5 over-refusal var. → **Önce veri
  fix (TRAP-tipi abstain), loss-masking'i denersek ≤1.5× + kendi ablasyon kolu + A1'i izle.**
- **ORPO ile negative rejection** — danışman DENE/P1. ✅ **Katılıyorum ama KAYNAĞI YÖNLENDİRİYORUM:**
  danışman negatifleri M3'ten almayı ima ediyor — ama v2b M3'te zaten 1.000 (orada hata yok).
  Faydalı negatifler **M2 hataları**: v2b'nin yanlış-kaynakta uydurduğu cevaplar (fabrication
  0.654, parametric_leak 0.615). ORPO çifti: **negatif = v2b'nin M2-fabrikasyonu, pozitif =
  çekinme**. Bu doğrudan G1'i hedefler.

### Grounding / atıf (§2) → G2 (off-by-one)
- **Citation-tuning** — danışman KULLAN/P0. ✅ **Katılıyorum ama DARALTIYORUM:** v2b'nin
  cit_precision'ı zaten yüksek (0.925/0.975); sorun **format değil**, komşu-madde
  distractor'ından **madde-numarası sızması** (off-by-one). → citation-tuning'i "madde no
  sadakati"ne odakla + **distractor kurgusunu düzelt** (bitişik-madde distractor'ları etiket
  karışması yapıyor → uzak-madde distractor'ı seç). Bu G2'nin kök nedeni.
- Context-distillation / CoVe — ELE. ✅ Katılıyorum (hukukta kelime/madde kaybı; latency).

### Veri kalitesi (§5) → G3 (GOLD sızıntısı)
- **Regex/kural scrub + teacher-prompt GOLD yasağı** — KULLAN/P0. ✅ **Tam katılıyorum.**
  Zaten bizim 🔴 açığımız. Öneri: kör silme değil, **önce raporla (kaç örnek/kalıp) → cümleyi
  bozmadan temizle** → sayıları research_log'a düş (ablasyon: temizlik öncesi/sonrası).
- **Replay kaynağı = temiz Yargıtay** — KULLAN/P0. 🟡 **Kısmen — DOĞRULA:** bizde replay
  `build_replay_tr.py` (AlicanKiraz0 MIT, %3). Danışman "ham wiki değil Yargıtay" diyor;
  önce mevcut replay'in NE olduğunu teyit et, sonra karar ver (belki zaten uygun).

### Uzun bağlam (§6)
- **2048 seq_len yeterli** — ✅ Katılıyorum, truncation fix + eval-mirror ile doğrulandı.
- **RAFT %20-30 ret oranı** — danışman "oranı değiştirme". 🟡 **Oran doğru, KOMPOZİSYON eksik:**
  mevcut ~%20 ret "gold'suz distractor paketi" tipinde → M3'ü çözdü, M2'yi çözemedi. Sorun
  oran değil, **ret diliminin TİPİ** (G1). Oranı koru, TRAP-tipi örnek EKLE.

### Eval / judge (§7) → G4 + adillik
- **Position-bias shuffle (M1'de gold yerini randomize)** — KULLAN/P0. ✅ **Katılıyorum, ucuz.**
  Aksiyon: `gen_eval_grounded.py`'de gold pozisyonu gerçekten randomize mi TEYİT et. Ayrıca
  bu G2'yi (off-by-one) de test eder — gold hep aynı yerdeyse etiket ezberi maskelenir.
- **Base'i "cevaplanan-only" yeniden skorla** (v2b_sonuclar'ın kendi uyarısı) — elmayla-elma
  A1 için; danışman bunu bilmiyordu ama v2c kapısı için şart.

### Quantization (§8) & Türkçe (§9)
- bf16 merge → Q4_0 GGUF, LoftQ gereksiz — ✅ Katılıyorum.
- Tokenizer genişletme ELE — ✅. Morfolojik sonek koruma (teacher kuralı) — ✅ ucuz, ekle.

---

## 2. Danışman "Faz 0 sıfır maliyet"ini yeniden sınıflandırma
Danışman 3 şeyi bedava-P0 saydı; bence sadece 2'si gerçekten güvenli-bedava:

| Danışman P0 | Benim sınıfım | Neden |
|---|---|---|
| GOLD scrub | ✅ **Gerçekten bedava-P0** | Veri temizliği, regresyon riski ~0 |
| position-shuffle + replay-teyit | ✅ **Gerçekten bedava-P0** | Eval/veri, güvenli |
| `use_rslora=True` | ❌ **Reçete değişikliği, ablasyon kolu** | efektif 4× lr, tuned setup'ı bozar |
| ret token loss ×2 | ❌ **Reçete değişikliği, ablasyon kolu** | over-abstention → A1 riski |

---

## 3. Bu iki girdiden çıkan ÖNERİLEN v2c hedef taslağı (harmanlamaya açık)
> v2b_sonuclar'ın kapı-durumu + bu değerlendirme birleşince v2c'nin işi:

**Birincil hedef (G1):** M2 (yanlış-makul tek-kaynak) abstention **0.346 → ≥0.786 (base)**,
M1/M4 grounding ve M3/M2b abstention'ı DÜŞÜRMEDEN. Kaldıraç: **veri kompozisyonu (TRAP-tipi
abstain dilimi)** birincil, ORPO (M2-negatifli) ikincil, loss-masking en son.

**İkincil (G2):** off-by-one atfı azalt — distractor kurgusu (uzak-madde) + citation-tuning
(madde-no sadakati) + eval position-shuffle ile ölç.

**Kozmetik (G3):** GOLD scrub (kaynak+veri).

**Ölç-önce (G4):** register eksenini ÖLÇ (şu an boş) — v2c hedefi koymadan önce baseline gerek.

**Ablasyon kolları (paper, isteğe bağlı bütçe):** rsLoRA · DoRA · ORPO — her biri KENDİ kolu,
drop-in değil. Danışmanın "rsLoRA+ORPO" tek-koşusu bizde iki değişkeni karıştırır → ayrı tut.

**KAPI (değişmez, ADR-0011):** A3 ≥ 0.786 · A1∧A2 ≥ 0.875 · A4 ≥ 0.9 · M5 gerilemesin · +register.
