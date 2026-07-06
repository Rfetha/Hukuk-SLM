# v4 DEEP-RESEARCH BRIEF — kopyala/tetikle hazır

> **Ne:** v4 tasarım taslağını ([[recipe]]) revize etmek için `/deep-research`'e verilecek **kendi-kendine yeten** brief.
> **Nasıl kullan:** Aşağıdaki "PROMPT" bloğunu olduğu gibi `/deep-research`'e ver. Dönüş → grilling → recipe kilit.
> **Durum:** hazır (2026-07-06). Tetikleme kullanıcıda.

---

## PROMPT (bunu /deep-research'e ver)

**Rol:** Retrieval-augmented fine-tuning + preference-optimizasyon (DPO/ORPO/KTO) + LLM abstention/grounding literatüründe uzman araştırmacı. Kanıt-temelli, kaynak-künyeli (arXiv/ACL/vb.), tarih + bulgu + bizim kısıta uygunluk ile yanıtla. Pazarlama/blog değil, hakemli/preprint kaynak.

**Bağlam (proje):**
- Türkçe hukuk asistanı SLM. Base = **Gemma 4 12B**, **QLoRA** (r=16, α=32, all-linear), 4-bit NF4. Eğitim = tek A100 (Modal); yerel dev = 12GB. **Ref-model-free preference şart** (12GB'da 12B + ref-model sığmaz) → ORPO tercih ediliyor.
- Deploy hedefi = **RAG** (retriever bağlamı verir). Tez: "güncellik ağırlıkta değil, kütüphanede." → **parametrik bilgi (kör-QA doğruluğu) HEDEF DEĞİL**; hatta düşük olması istenir. Değer = *verilen kaynağı sadık kullan + yanlış/eksik kaynağı reddet.*
- Veri **lisans-temiz** olmalı (kamu mevzuat metni + sentetik üretim). Ticari korpus yok.

**Bulunduğumuz nokta (ampirik):**
6-mod CANON eval (LLM-judge gpt-4o-mini, n=35-40, seed sabit). Turlar:
- **v2b** (RAFT-SFT): grounding iyi (M1 0.737, M4 0.968), ama yanlış-kaynak reddi zayıf (M2 0.346).
- **v2c** (near-miss abstention'ı DÜZ SFT ile): M2 düzelmedi (0.407) + grounding regresyonu → RED. **Negatif bulgu (K3): düz SFT abstention'ı bozar.**
- **v3** (ORPO, v2b-adaptöründen DEVAM): M1 grounding **0.881'e ÇIKTI** (base 0.662, v2b 0.737'yi geçti), M4 1.0. Yanlış-kaynak reddi M2 0.35→**0.593** (iyileşti ama base 0.704'ün altında). **İki sorun:** (a) M2b "çok-distractor-doğru-kaynak-yok" reddi **0.96→0.529 GERİLEDİ** — model reddetmek yerine en yakın distractor'ı seçip uyduruyor ("forced source-selection" bias; near-miss red şablonunun 'en ilgili kaynağı seç' adımından); (b) held-out OOD (görülmemiş kanun/soru) reddi zayıf (0.483 vs aynı-dağılım 0.656). v3 train = yalnız **1741 preference çifti** (küçük).

**Tasarım tezimiz (revize etmeni istediğimiz):**
CANON'un grounding kulvarları (cevap-VAR → kullan) ile abstention kulvarları (cevap-YOK → reddet) **tek bir "answerability discrimination" becerisinin iki yüzü**; mantıksal takas yok, gözlenen frontier = zayıf-dedektör artefaktı. → v4 = "8 metriği dengele" değil, **tek dedektörü keskinleştir**; en büyük kaldıraç **preference-veri ölçeği + present/absent aile çeşitliliği** (algoritma değil, veri-kompozisyon).

**Kabuller (bunları veri temelinde DOĞRULA/ÇÜRÜT):**
1. En zor kulvarda ~0.90 abstention yeterli (mutlak 1.0 = over-refusal patolojisi).
2. Başarı = "lider veya berabere-tavan."
3. 1 numaralı kaldıraç veri-ölçeği/çeşitliliği.

### Cevaplanacak 6 SORU (her birine kanıt + bizim-kısıta-öneri)

1. **Preference-veri ölçek-getiri eğrisi (RAG-refusal/grounding'de).** Kaç preference çifti anlamlı? 1.7K→~6-8K'ya çıkmanın beklenen getirisi ne? "Az-ama-zor" vs "çok-ama-çeşitli" — hangisi abstention-discrimination'da baskın? Ölçek-doygunluk noktası bulgusu var mı?

2. **RAFT/çok-kaynak eğitiminde abstain (gold-yok) örnek oranı.** Gold-absent (cevap bağlamda YOK → reddet) çiftlerinin ideal payı ne? Fazlası over-refusal'a (grounding çöküşü) iter mi? "Presence/absence" dengesini kuran oran üzerine kanıt (RAFT, Cor-RAIT, Sufficient-Context, RAAT vb.).

3. **OOD/held-out hard-negative mining — sızıntısız yöntem.** Görülmemiş kanun/konu dağılımından novel-soru near-miss tuzağı üretmenin sağlam yolu? Eval-sızıntısını (train/test kanun-örtüşmesi) önleyen protokoller? Sentetik hard-negative üretiminde kalite-kapısı (grounded-verification) örnekleri.

4. **Zemin: continuation-preference vs joint (base'den) preference.** Grounding'i önce SFT'le öğrenmiş adaptör ÜSTÜNE ORPO (bizim v3) vs base'den grounding+abstention'ı BİRLİKTE ORPO — tavan/forgetting/veri-ihtiyacı farkı üzerine kanıt? "Continuation prior'ı abstention'ı sınırlar mı" sorusuna literatür ne diyor?

5. **Abstain "chosen" muhakeme yapısı.** "Kaynak yeterli mi?" ayrımını en iyi öğreten hedef-cevap formatı: uzun CoT-red mi, kısa gerekçeli-red mi, "yeterlilik-etiketi + red" mi? Reasoning-trace'in abstention-genellemesine etkisi (kanıt).

6. **DPO/ORPO RAG-refusal ~%87 platosunu aşmak.** Tek-tur preference'ın abstention platosunu kıran teknikler — iteratif hard-negative (online/self-play), DTA (Divide-Then-Align), Cor-RAIT, knowledge-boundary kalibrasyonu — **12GB/ref-free/QLoRA kısıtına uyanları** önceliklendir. Her biri: kanıtlı kazanç + bizim kuruluma uyarlanabilirlik.

### İSTENEN ÇIKTI FORMATI
- Her soru için: **(i)** 2-4 künyeli bulgu (kaynak + tarih + sayısal sonuç), **(ii)** bizim-kısıta net öneri (uygula/uygulama + parametre aralığı), **(iii)** risk/uyarı.
- Kapanış: **tasarım-taslağımıza (5 kaldıraç + zemin-A-önerisi + veri-ölçeği-1-numara) somut REVİZYON listesi** — neyi değiştir, neyi doğrula, neyi ekle/çıkar.
- Çelişen kanıtı gizleme; "keyfi oran/ölçek" iddialarını (ör. sabit %X) veri yoksa işaretle.

---

## Dönüş sonrası
Bulgular → grilling (zemin A/B kilit + kaldıraç parametreleri) → [[recipe]] güncelle + KİLİTLE → ADIM-plan → para-kapısı onayı → koş. Bulguları research_log'a yeni entry olarak da işle (v2/v3'te olduğu gibi).
