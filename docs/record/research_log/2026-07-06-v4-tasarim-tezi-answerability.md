# 2026-07-06 · v4 tasarım tezi — "tek answerability-dedektörü" + her-kulvar-#1 teorik mümkün

> **Bağlam:** v3 kapandı (KISMİ, ADR-0015). "SCORECARD'a bakıp her kulvarda #1 olmak için ne artmalı /
> bu teorik mümkün mü?" tartışmasının kavramsal ürünü. Bu entry = v4 reçetesinin üstüne kurulacağı **tez**
> (paper Discussion malzemesi). Deney değil, çerçeve. v4 detayı → [[../v4/README]] (yapılacak).

## Tez — 9 kulvar = 1 zor beceri + 1 kolay dik beceri

CANON'daki 9 ölçüm ayrı hedefler DEĞİL; büyük çoğunluğu **tek bir latent beceriye** iner:

- **Grup 1 (cevap VAR → kullan):** M4 (temiz gold), M1 (distractor arası gold).
- **Grup 2 (cevap YOK → reddet):** M2 (yanlış kaynak), M2b (çok distractor gold-yok), M3 (boş), xkanun/ood (görülmemiş yanlış).
- Grup 1 + Grup 2 = **aynı becerinin iki yüzü:** *"verilen bağlam bu soruyu cevaplıyor mu?"* = **answerability discrimination** (cevaplanabilirlik ayrımı).
- **Ortogonal:** Register (uzman dili, ayrı beceri, ~1.0 çözülü) · M5 (parametrik ezber, düşük=iyi) = **üçüncü beceri değil, iyi ayrımın gölgesi** (bağlama güvenen model ezbere yaslanmaz → M5 doğal düşer).

**Çıkarım:** Tek becerinin *iç takası olmaz.* Mükemmel ayrım → var-durumunda cevaplar (M1/M4=1.0) VE yok-durumunda reddeder (M2/M2b/M3=1.0), **aynı anda.** "Doğruyu kullan" ile "yanlışı reddet" ancak *ayrım zayıfsa* çekişir.

## Sonuç: "grounding-abstention frontier" bir doğa kanunu DEĞİL
Gördüğümüz takas eğrisi = **mevcut dedektörün kusurunun artefaktı.** Ayrımı iyileştirmek frontier'ı dışarı iter:
M2'yi M1'e takas etmezsin, **ikisini de daha iyi ayrımla satın alırsın.** → her kulvarda (berabere-)#1 **teorik mümkün.**

## Base ve Mecellem neden yapamıyor (aynı çerçeve)
İkisi de ayrım-uzayının bir **köşesini** seçmiş, dedektörü kurmamış:
- **base** = "her şeyi reddet" köşesi → abstention yüksek, grounding çökük (M1 0.662).
- **Mecellem** = "hep ezberden cevapla" köşesi → M5 yüksek (0.35), gerisi düşük (M4 0.78, register 0.2).
- **Biz** = merkezdeki gerçek dedektör → köşeleri domine eden tek çözüm. v3 = ilk somut adım (M1 0.881: ayrım kurulmaya başladı).

## KABUL EDİLEN TASARIM AKSİYOMLARI (v4 kilit — kullanıcı onayı 2026-07-06)
1. **Mutlak mükemmellik hedef DEĞİL.** En zor kulvarlarda (M2b) **~0.90 yeterli** kabul edildi. 1.0 = over-refuse patolojisi + invalid-trap ölçüm-tavanı yüzünden hem gereksiz hem ulaşılmaz.
2. **Anlamlı hedef = "berabere-tavan VEYA lider."** Geçilemeyen kulvarda **eş olmak yeterli** (net kabul). Yani grounding dörtlüsü + register'da lider/tavan; abstention'da base-üstü VEYA en kötü base-eş. Bunu başaran = hem grounding hem abstention köşesini birden tutan **tek model.**
3. **Optimizasyon-tuzağı gerçek → net odak veri-ölçeği.** Over-refuse köşesi bir *yerel optimum*; sınırlı veriyle (v3 train=1741) gradient oraya kayar. Gerçek dedektör **daha çok + daha çeşitli** kontrast ister. **v4'ün 1 numaralı kaldıracı: veriyi ölçekle + tüm present/absent ailelerini kapsa.** (Algoritma değil, veri-kompozisyon.)

## v4 için ne değişiyor (reçete yönü)
Çerçeve reçeteyi yeniden tanımlıyor: **"8 takası dengele" DEĞİL, "tek answerability-dedektörünü keskinleştir."**
Her eğitim çifti **present/absent sınırını** netleştirmeli:
- Aynı formatta (çok-kaynak RAFT) hem gold-VAR→cevapla hem gold-YOK→reddet çifti → körlemesine değil, *yokluğu tespit* öğrenir (M2b fix).
- Negatif-aile çeşitliliği + veri ölçeği (1741→~6-8K) → yerel optimumdan çıkış, aile-ötesi genelleme (ood/xkanun fix).
- Temiz etiket (τ) → sınır gürültüsüz.

## Paper eşleme
- **Discussion / ana tez:** "hukuki RAG-asistanında grounding ve abstention ayrı hedefler değil, tek answerability-discrimination becerisinin izdüşümleri; gözlenen frontier kusur-artefaktı." (K3'ü pozitif teze çevirir.)
- **Frontier figürü:** base (refuse-köşe) vs Mecellem (answer-köşe) vs bizim turlar (merkeze yürüyüş: v2c→v2b→v3→v4).
- İlgili: entry #24 (K3 negatif), #31 (konumlama), #32 (v3 sonuç + M2b teşhis), ADR-0015.
