# ADR 0006 — Akademik hedef: sistem paper'ı (benchmark yan iş)

- **Durum:** Yürürlükte (2026-06-08)
- **Geriye dönük kayıt.** Otoriter doküman: `docs/PAPER_TARGET.md`.

## Bağlam
Proje uzun vadede akademik yayın hedefliyor. Soru: yayın bir **benchmark paper'ı** mı yoksa
uçtan-uca **sistem paper'ı** mı olmalı? Bu seçim her eval/veri/sistem kararını yönlendiriyor
(ölçüm disiplini, baseline, seed, rakip seçimi baştan kurulmalı).

## Karar
**Ana = SİSTEM paper'ı** (kullanıcı: "asıl mevzu benchmark değil, sistem"). Tez: Türkçe vatandaş-dilli
hukuk asistanında "doğru VE anlaşılır" tek fine-tune ile çelişkili → **grounded-RAG + agentic sistem**
+ çift-eksenli benchmark ile çözülür. Boru hattı: Gemma-4-12B → law-domain SLM (QLoRA SFT, doğruluk/
groundedness — sade DEĞİL) → TurboQuant'lı RAG → Agent → APP katmanı (vatandaş sadeleştirme runtime).
Katkılar: **K1** uçtan-uca sistem (ablasyon base→+SFT→+RAG→+agent), **K2** verimlilik/TurboQuant,
**K3** erişilebilirlik↔doğruluk gerilimi bulgusu. **Benchmark = yan iş** (güçlüyse ayrı LREC).

## Değerlendirilen alternatifler
- **Benchmark-headline paper** → İKİNCİL. Tek başına headline değil; ama sistem paper'ı içinde
  çift-eksen hukukçu-doğrulamalı benchmark katkı olarak durur.
- **"Rakibin benchmark'ında geçmek"** → ANLAMSIZ kabul edildi. Mecellem'in metrikleri (encoder
  cloze, retrieval, perplexity, 112B token) farklı görev/kaynak. Kazanılacak yer = onların
  **ölçmediği** eksen: erişilebilir+doğru vatandaş QA.

## Sonuç
- Rakip seti: `newmindai/Mecellem` (Qwen3-4B-legal) + GPT-4o + ham Gemma. Adil kıyas = eşit dağıtım
  ayak izi (Q4_0 ~6.5GB/8GB GPU); rakipler **bizim terazimizde** ölçülür, paperlarından sayı alınmaz.
- K3 için erken kanıt elde: v0 legal_acc 0.362→0.124, sadelik 6.47→7.30, Muhakim körlüğü −0.15.
- Ölçüm disiplini şimdi kuruluyor (ADR 0001): baseline + sabit seed + hakem-uyumu.

## İlgili
`docs/PAPER_TARGET.md`, `[[paper-target]]`, ADR 0001, `knowledge/summary_turboquant.md`
