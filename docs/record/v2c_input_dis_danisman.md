# v2c GİRDİ — Dış Danışman Raporu (harici agent)

> **Statü:** v2c reçetesi için HAM GİRDİ. Bu doküman dışarıdaki bir LLM-agent'a
> [[prompt: bkz. bu oturum]] verilerek alınan cevabın kaydıdır. Tek başına karar
> değildir — [[v2c_input_claude_degerlendirme]] ile HARMANLANARAK v2c reçetesine
> dönüşecek (v2b tam-run bitince).
> **Tarih:** 2026-07-02 · **Kaynak:** harici agent (FT/LLM teknikleri danışmanlığı)
> **Girdi olarak verilen bağlam:** V2_PLAN, FINE_TUNING, research_log, ADR-0010/0011/0013,
> güncel teknik durum (Gemma 4 12B QLoRA r16/α32, RAFT, abstention/grounded eval,
> base baseline faith 0.879 / abstention 1.000, GOLD sızıntısı %5.7, truncation fix).

---

## Yönetici özeti (danışmanın çerçevesi)
Mevcut baseline'ı (Faithfulness 0.879, Abstention 1.000) düşürmeden bilinen açıkları
kapatmak; literatürdeki güncel teknikleri Modal ($30) + Gemma 4 12B QAT kısıtlarına uyarlamak.

## 1. FT yöntem ailesi
| Yöntem | Danışman kararı | Öncelik | Gerekçe |
| --- | --- | --- | --- |
| **DoRA** (weight-decomposed LoRA) | DENE | P1 | Magnitude+direction ayrıştırır, kararlılık artar, full-FT'e yaklaşır. ~%10-15 ekstra bellek, A100-40GB'a sığar. (Liu et al., 2024) |
| **rsLoRA** (rank-stabilized) | KULLAN | P0 | Ölçekleme α/r yerine α/√r; yüksek rank'te çöküşü engeller. "Sıfır maliyet", ablasyon-dostu. (Kalajdzievski, 2023) |
| **LoRA+** | ELE | P2 | A/B için farklı lr; arama uzayını büyütür, bütçe yer. |
| **Full-FT** | ELE | P2 | 12B tek A100-40GB'da OOM; bütçeyi ilk epoch'ta aşar. |

## 2. Grounding / halüsinasyon azaltma
- **Citation-tuning** — KULLAN/P0. Sentetik üretim prompt'unda her iddiayı döküman
  indeksiyle `[idx]` formatında eşleştir; atıf davranışını loss'a dahil et → A4 yükselir.
- **Context-distillation** — ELE/P2. Özetleme madde no / kelime kaybı → hukukta zararlı.
- **CoVe (Chain-of-Verification)** — ELE/P2. Inference'ta çok-aşama; 8GB'da latency kabul edilemez.

## 3. Abstention / kalibrasyon
- **🔴 Abstention-aware loss masking** — KULLAN/P0. abstain ~3.5K örnekte ret token'larına
  cross-entropy loss ağırlığını **1.5x–2.0x** yükselt. Sıfır ekstra GPU. Paper ablasyonu:
  "loss manipülasyonuyla abstention kararlılığının korunması".
- **🟡 ORPO ile negative rejection** — DENE/P1. Boş-bağlamda (M3) yanlış cevap veren eski
  checkpoint çıktıları negatif (y_l) → ORPO'ya besle. (bkz. §4)

## 4. Tercih optimizasyonu
- **ORPO** — KULLAN/P0. DPO reference-model tutar → 12B'de OOM; ORPO reference-free,
  SFT+tercih tek loss. Uygulama: teacher jargon hatası = negatif (y_l), temiz metin =
  pozitif (y_w), tek epoch. Maliyet: SFT ile ~aynı bellek, ~%5 fazla süre. (Hong et al., 2024)
- **SimPO / KTO** — ELE/P2. SimPO TRL'de ORPO kadar kararlı değil; bütçede risk alma.

## 5. Veri kalitesi / teacher-jargon sızıntısı
- **Regex/kural temizlik** — KULLAN/P0. ~17.3K hedef metinde `"GOLD metnidir"`,
  `"Verilen dökümana göre"`, `"Metin incelendiğinde"` kalıplarını temizle / yasal dille
  yeniden başlat (`"X Kanunu uyarınca..."`). Maliyet $0, %5.7 → %0.
- **%3 replay kontrolü** — KULLAN/P0. Replay ham Türkçe wiki değil, temiz dilli Yargıtay
  kararlarından seçilsin; dil yapısı korunur, jargondan uzaklaşmaz.

## 6. Uzun bağlam / chunking
- **2048 seq_len** — KULLAN/P0. 900 char ≈ 200-250 token; 1 gold + 4 distractor ≈ 1250
  token bağlam + 500 soru/cevap ≈ ~1750 < 2048. Yeterli. 4096 → O(N²) bellek, bütçe yer.
- **RAFT distractor oranı** — KULLAN/P0. RAFT (Tian et al., 2024) veri setinin %20-30'unun
  bağlamsız ret örneği olmasını önerir; mevcut ~%20 ret literatürle uyumlu, değiştirme.

## 7. Eval / judge güvenilirliği
- **gpt-4o-mini judge** — KULLAN/P0. Maliyet/performans dengesi. Kronik sorun: **position bias**.
- **Position-bias azaltma** — KULLAN/P0. M1'de gold döküman yerini her örnekte rastgele
  karıştır (shuffle); judge prompt'una "sıra önemsiz" talimatı ekle.

## 8. Quantization-aware FT
- **bf16 merge → llama.cpp Q4_0 GGUF** — KULLAN/P0. Base zaten QAT (q4_0 hedefli) →
  kuantizasyon sonrası kayıp standart modellerden az. Ekstra LoftQ vb. GEREKMEZ (bütçe).

## 9. Türkçe / düşük-kaynak
- **Tokenizer genişletme (vocab expansion)** — ELE/P2. Embedding sıfırdan eğitim ister,
  QLoRA'yı bozar, pre-training bütçesi ister. Kısıt ihlali.
- **Morfolojik sonek koruma** — KULLAN/P0. Sentetik üretimde teacher'a "mevzuat dili
  morfolojisine sadık kal, kök+ek bozma" kuralı dayat.

## Danışmanın önceliklendirilmiş yol haritası
- **Faz 0 (sıfır maliyet):** 1) GOLD scrub · 2) `use_rslora=True` · 3) ret token loss ×2.0
- **Faz 1 (Modal run):** 1) DoRA'yı ~2K örnekte bellek testi → kararlıysa ana eğitim ·
  2) bütçe kalırsa ORPO tek epoch
- **Faz 2 (paper):** ablasyon matrisi → Baseline(No-FT) vs QLoRA+SFT vs rsLoRA+ORPO
  (Faithfulness ve Abstention eksenleri)
