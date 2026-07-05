## Paper'a ne yarar (eşleme)
- **K1 ablasyon:** base → +SFT → +madde-verili (oracle) tablosu. **Uyarı:** faithfulness'la ölçülürse "+SFT" satırı boş çıkar (tavan); SFT katkısını wrong_ref/hedge/format eksenlerinde göster. (oracle = gerçek RAG'ın iyimser tavanı.)
- **K3 ayrışma/negatif bulgular:** (a) v0 forum verisi çöküşü (154x ezber), (b) **KÖR-vs-madde-verili: parametrik madde-no ezberi imkansız, oracle-tavan SFT'yi faithfulness'ta gereksizleştirir** — güçlü, yayınlanabilir negatif bulgu, (c) etiketsiz-chunk → uydurma atıf.
- **Methodology:** grounded veri imali, kalite kapısı köprüsü, dış-iddia doğrulama disiplini.
