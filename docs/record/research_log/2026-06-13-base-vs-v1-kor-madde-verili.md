### 2026-06-13 — ⭐ base vs v1 eval: KÖR vs MADDE-VERİLİ (asıl bulgu)
**Kurulum:** `gen_eval_grounded.py` — model soruyu cevaplar, gerçek madde **referans** (yer-gerçeği) olarak skorlanır. İki mod: KÖR (madde prompt'ta yok, parametrik) / MADDE-VERİLİ (oracle-context, `--with-source`, etiketli madde ELLE prompt'a konur — gerçek RAG/retriever DEĞİL). n=20, gpt-4o-mini hakem.
> ⚠️ **Kaynak dosyaları silindi (2026-06-13 akşam):** bu n=20 keşif koşusunun detay/skor dosyaları (`eval_*`, `rag_*`, `ragL_*`) eval/ temizliğinde KESİN SİLİNDİ. Sayılar yalnız bu tabloda kayıtlı. Yerine **akşam n=40 KÖR + oracle benchmark** geçer (daha temiz, dosyaları duruyor).

| metrik | KÖR base | KÖR v1 | madde-verili base | madde-verili v1 |
|---|---|---|---|---|
| faithfulness | 0.571 | 0.520 | **0.980** | **0.971** |
| hallucination | 0.429 | 0.480 | 0.020 | 0.029 |
| cit_precision | 0.833 | 0.200 | 0.950 | 0.850 |
| wrong_ref | 0.125 | 0.800 | 0.050 | 0.150 |
| cit_recall | 0.900 | 0.450 | 1.000 | 0.900 |

**Bulgular:**
1. **KÖR test yanıltıcıydı.** Madde verilince faithfulness 0.52→0.97, halüsinasyon 0.48→0.03. v1'in "felaketi" (KÖR wrong_ref 0.80) **test artefaktı** — model ezberden madde no uyduruyordu.
2. **Etiket hatası:** madde-verili modda madde *metni* verilip *etiketi* (Kanun+no) verilmeyince model numarayı yine uydurdu. Etiket eklenince (`ragL`) atıflar düzeldi. → **Faz 2 RAG dersi (gerçek retriever): getirilen chunk atıf metadatasını taşımalı.**
3. **Madde-verili modda v1 ≈ base** (faith 0.971 vs 0.980; v1 cit_precision 0.85 < base 0.95). **SFT ana metrikte base'i GEÇMEDİ, atıfta hafif geriletti.**

**Reframe (bugün netleşti):** birincil kitle = uzman; doğruluk RAG'dan; sadelik app-layer. → "v1 kısa/sade" satış noktası değil.

**Strateji kararı (subagent analizi):** v1'i **eğitim hedefi olarak reddet**, grounding altyapısını koru → **dar v2** kur:
- **Madde-verili modda** eğit (deploy'da retriever maddeyi getirecek; KÖR eğitim wrong_ref 0.80'in sebebi).
- **Uzman-register** (v1 vatandaş-register'ı yanlış kitle).
- **%15-25 hedge/red** örneği (v1'de %1.1 → SFT'nin tek base+prompt'la zor taklit edilen meşru rolü: kaynak-yokken uydurma yerine "maddede yok/danış").
- **Başarı kapısı:** faithfulness DEĞİL (tavan) → **wrong_ref ≤0.05 + hedge-isabeti + atıf-format tutarlılığı.**
- **Versiyonlama:** v2 = **base'den taze QLoRA** (v1 üstüne DEĞİL). v0/v1/v2 = deney nesli, ağırlık atası değil. v1 arşivlenir (ablasyon referansı).

**Açık doc çelişkisi:** VISION.md §1 "default output = vatandaş dili / terim→sade çeviri" reframe ile çelişiyor → ADR-0010 + VISION düzeltmesi bekliyor.

