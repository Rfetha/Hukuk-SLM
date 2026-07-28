# ADR-0038 — Red kapısı eşiği: **katı** (tek doğrulanamayan atıf → cevap reddedilir)

**Statü:** Yürürlükte · **Tarih:** 2026-07-28
**Otorite belge:** `TASARIM.md` §5 (harness) · §13 soru **2 → ✅ KAPANDI**
**İlgili:** ADR-0011 (CANON — A1 cevaplanan-only + coverage yan yana) · ADR-0019 (harness dilimi
teze dahil) · ADR-0037 (Kapı 5 — serbestlik derecesi disiplini)
**Uygulama:** Sprint 4 (harness). Karar **veriden önce** yazıldı.

---

## Bağlam

Harness'ın atıf doğrulayıcısı cevaptaki her atıfı dondurulmuş korpusa karşı kontrol ediyor.
Cevapta birden fazla atıf olabilir ve bir kısmı doğrulanamayabilir:

```
"... (TBK m.350) ... ayrıca (TBK m.353) ... ve (TMK m.1024)"
      ✓                    ✓                   ✗ korpusta yok
```

`TASARIM.md` §13 bunu açık soru olarak bırakmıştı: *"tüm atıflar doğrulanmalı mı, çoğunluk yeter mi?"*

## Karar

**Katı politika: doğrulanamayan TEK bir atıf, cevabın tamamını reddettirir.** Red kapısı ikili
çalışır — geçti / reddedildi. Ara durum yok.

## Değerlendirilen alternatifler

| eleme | gerekçe |
| :--- | :--- |
| **B — çoğunluk** (atıfların >%50'si doğrulanıyorsa geç) | ❌ **Ürün vaadini deler.** *"Uydurma atıf yapamaz çünkü atıf kodla doğrulanıyor"* cümlesi B'de yalan olur; cevapta uydurma atıf kalabilir |
| **C — cerrahi** (doğrulanamayan atıfı cümlesiyle sil, kalanı sun) | Cevabın anlamını bozabilir — silinen cümle sonucu taşıyorsa geriye yanıltıcı bir metin kalır. Ayrıca "hangi cümle silinecek" ayrı bir sezgisel katman getirir |
| **Eşikli varyantlar** (%70, %80 …) | Eşik **taranabilir bir serbestlik derecesi** olur ve ADR-0037'nin çoklu karşılaştırma sorununu büyütür. Katı politika parametresizdir |

**Üç katmanlı gerekçe:**

1. **Ürün vaadi bu.** Sistemin değer önerisi "daha akıllı" değil **"denetlenebilir"**. Tek uydurma
   atıfın geçtiği bir sistem denetlenebilir değildir.
2. **Hukukta kısmi doğruluk işe yaramaz.** Avukat 3 atıftan 2'si doğru bir metne güvenemez —
   hangisinin yanlış olduğunu bilmediği için **hepsini** kontrol etmek zorunda kalır ve sistem
   hiç zaman kazandırmamış olur. Kısmi güven, sıfır güvenle aynı iş yükünü üretir.
3. **Ölçüm temizliği.** Katı politika parametresiz ve ikili; B/C eşik getirir.

## Sonuç — kabul edilen bedel ve nasıl görünür kılınıyor

⚠️ **Coverage düşer.** Tek bir yazım/biçim hatası doğru bir cevabı çöpe atabilir.

Bu bedel **gizlenmiyor, zaten ölçülen bir eksen**: ADR-0011 gereği **A1 = cevaplanan-only**
ve **coverage yan yana** raporlanıyor. Katı kapının maliyeti tabloda doğrudan görünür.

**B ve C elenmedi, ablasyona alındı.** Üç politika **aynı cevap kümesi üzerinde post-hoc**
uygulanabilir — yeniden üretim gerekmez, maliyet ~0. Sprint 4'te coverage/precision eğrisi
üç nokta olarak çizilir ve raporlanır. §13'ün *"ablasyon adayı"* notu böylece karşılanmış olur.

⚠️ **Sınır:** doğrulayıcının kendi hata oranı (yanlış-negatif: doğru atıfı korpusta bulamama)
bu politikada **doğrudan coverage kaybına** dönüşür. Doğrulayıcının kalibrasyonu Sprint 4'ün
ayrı bir borcudur; katı politika onu affetmez.
