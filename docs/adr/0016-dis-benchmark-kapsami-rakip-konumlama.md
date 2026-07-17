# ADR-0016 — Dış-benchmark kapsamı + rakip konumlama (BigLaw/LegalBench & Muhakim = cite-only)

**Statü:** Yürürlükte · **Tarih:** 2026-07-08
**İlgili:** ADR-0010 (register=uzman), ADR-0011 (eval canon) · research_log #31, #35 · memory [[paper-target]], [[eval-harness-decision]], [[benchmark-positioning]]

## Bağlam
İki tetik: (1) "Modeli **BigLaw-Bench** (harveyai) gibi büyük dış benchmark'a soksak, frontier'a göre konumlansak mı?" + "makale için **büyük tanınmış** benchmark kredibilite verir" endişesi. (2) NewMind AI (`newmindai`) TR-hukuk stack'inin tam anatomisi netleşti (Mursit / Mecellem / Muhakim). Detay tarama: research_log #35 + parking notu.

## Karar
1. **BigLaw-Bench + LegalBench = KOŞULMAZ; yalnız Related Work atfı.** İngilizce + US/UK common-law → dil + yargı-sistemi mismatch. TR medeni-hukuk üretken modelini bu setlerde koşmak **yorumlanamaz** (düşük skor "model kötü" değil "yanlış sınav") + off-thesis. BigLaw ayrıca hakemli değil (vendor benchmark); LegalBench hakemli ama yine İngilizce/US.
2. **Frontier kıyası = KENDİ canon benchmark'ımızda** (GPT-4o/Claude/Gemini blind+RAG), dış İngilizce sette DEĞİL. Zaten planlı: TODO'daki G1 cross-family judge + Llama-3.1-8B baseline + koşulu Mecellem-4B baseline.
3. **Muhakim (newmindai reward model) = cite-only; JUDGE olarak koşulmaz.** Gerekçe: (a) hakem-geçerliliği zaten cross-family judge (gpt-4o-mini + gpt-4o/Claude/Gemini — ADR-0011/TODO) ile karşılanıyor → marjinal değer yok; (b) Muhakim reddettiğimiz `newmindai/EuroHPC-Legal`'e bağlı (kalibrasyon kirliliği riski — VERI_PLANI). `models/Muhakim` (15GB) + `scripts/muhakim_judge.py` hazır → ileride istenirse. NOT: "sadelik ekseni yok" artık kusur değil; register hedefi ADR-0010 ile uzman'a döndüğü için Muhakim'in avukatça-derinlik biası HİZALI.
4. **alibayram/turkish_mmlu (law-MCQ) = eğitim/ana-benchmark parçası DEĞİL.** CC BY-NC 4.0 (ticari yasak) + "telif içeren sorular bulunabilir" beyanı (copyright poison). Gerekirse lisans-temiz kendi law-MCQ setimizi kurarız.
5. **Katkı konumlaması:** üretken TR hukuki cevabın grounding/abstention/citation + register kalitesini ölçen **tanınmış benchmark YOK** (mevcut TR hukuk stack retrieval/embedding'e odaklı) → bu boşluk katkımız. (paper-target ile tutarlı.)

## Elenen seçenekler
- BigLaw/LegalBench koş → off-axis, yorumlanamaz, off-thesis.
- Muhakim'i çapraz-judge yap → gereksiz (cross-family zaten var) + veri-kirliliği.
- alibayram law-MMLU'yu "sanity number" diye kullan → NC + poison; en fazla dahili tek-seferlik.

## Sonuç
Paper'ın "frontier'a göre neredeyiz" + "rakip" ihtiyacı **kendi canon setinde** (frontier + Mecellem-4B + Llama-8B baseline + cross-family judge) karşılanır; dış İngilizce benchmark'lar yalnız literatür atfı. Compute grant yolu (MN5/EuroHPC/TRUBA) ayrı fizibilite (research_log #35), Faz-1 (12B QLoRA = tek GPU) için gereksiz.
