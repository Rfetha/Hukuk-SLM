## v2c icra — ADIM 6a+6b: Tier A yeni-kod + v2c eğitim verisi İNŞA EDİLDİ (2026-07-02)
Otorite: [`v2c/roadmap.md`](../v2c/roadmap.md) §5 madde 6a-6b · §7 AÇ-KOŞ-2/3. `v2c` branch. **Modal eğitimi (6c) = para-kapısı → kullanıcı onayı bekleniyor.**

**Yeni-kod (4 parça, hepsi çalışır+test-edildi):**
- `build_sft_v2b.py pack`: 2 yeni slice üretici — `counterfactual` (A2) + `abstain_trap` (A1). Dönüşüm kararı **AYRI `crng`** ile (ana P-roll/distractor rng akışı BOZULMAZ) → dönüşmeyen grounded/abstain satırlar v2b ile **byte-identik** → reuse geçerli + §1 regresyon güvenli. `--cf-frac/--trap-frac/--trap-k/--out-dir` args.
- `_gate`: counterfactual için referans = `cf_gold_text` (gerçek gold'a bakarsa haksız reddeder); abstain_trap = abstain gibi (ABSTAIN_RE).
- `gen_v2b_answers.py`: `ABSTAIN_TRAP_TEMPLATES` (5 varyant, hepsi ABSTAIN_RE-uyumlu) + `build_cf_answer` (cf_quote alıntıla+atıf) + worker dispatch + **`--reuse-answers`** (grounded'ı v2b'den al).

**Ampirik bulgu — Türk hukuk metni sayıları KELİME yazar (K3 malzemesi):** digit-regex CF olgusu grounded'ın sadece **%0.3'ünü** (49/15447) tuttu; kelime-sayı ("otuz gün", "yüzde yirmi") desteği eklenince tespit **%17.6'ya** çıktı. cf-frac=0.25'te CF=716 (cf_miss=3195). CF, hedeflenen ~1.5K'nın altında (olgu-kıtlığı) ama trap (birincil kaldıraç) hedefi tam tutturuyor → CF ikincil, grounded-seyreltmeyi (§1 risk) minimalde tutmak için bilinçli düşük.

**Kompozisyon (`data/processed/sft_v2c/packed.jsonl`, seed 3407, P=0.8, cf-frac 0.25, trap-frac 0.40):**
`{grounded 14742 (76%), counterfactual 716 (3.7%), abstain 2339 (12%), abstain_trap 1508 (7.8%)}` — abstain+trap=**19.9%** (§7 ~%20 ✓), trap/abstain=**39/61** (§7 40/60 ✓).

**gen_answers — API çağrısı=0:** 14742 grounded'ın HEPSİ v2b scrub'lı answers'tan (reuse-map=15458) alındı → **maliyet ~$0, grounding dağılımı birebir korundu.** cf/trap/abstain şablon.

**assemble (gate+replay+split) → `data/processed/sft_v2c/{train,validation,test}.jsonl`:**
- kept 18701 / red 604 (601 quote + 3 atıf). **Red'lerin TAMAMI grounded**, CF'te 0 red (716/716 gate geçti), trap'te 0 red. Red'ler **pre-existing v2b-mirası** (v2b 635 red; v2c daha AZ çünkü bazı red-grounded CF'e dönüştü). GOLD-scrub hiçbir quote'u bozmadı (quote-içinde-GOLD = 0).
- train=17353 (grounded 12720 · trap 1369 · abstain 2092 · cf 650 · replay 522) · val=963 · test=963.
- Örnek-teyit: CF cevabı counterfactual değeri kaynaktan alıntılıyor (ezber değil); trap cevabı yanlış kaynağı (KMK Md43) adıyla reddediyor. İkisi de hedefe uygun.

**Kalan:** 6c Modal `--detach` eğitim (config=v2b: lr=1e-4, r=16/α=32) → **PARA-KAPISI, onay bekleniyor.** Sonra 6d 6-mod eval (§6 üstünlük + §1 regresyon).

---

