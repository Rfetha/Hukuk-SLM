# Yol haritası — ölçülmüş açıklardan işlere

> **Hedef:** daha iyi model. Önce Gemini 3.1 Flash-Lite'ı geçmek, sonra Flash ve
> Pro'ya yetişmek. Bu belge o hedefi **ölçülmüş açıklara** bağlar — his değil, sayı.
>
> Yöntem disiplini (sabit seed, kayıtlı koşu, ön-kayıtlı kapı) **korunuyor**, ama
> gerekçesi değişti: artık bir hakemi ikna etmek için değil, **kendimizi
> kandırmamak** için.

## Şu anki açık

DEV, **harness kapalı**, hakem `gpt-4o-mini` (protokol: [MODEL_CARD](MODEL_CARD.md))

```
                  BİZ 4B   Gemini FL    açık
M1 sadık-cevap    71,6%     72,9%     ~kapandı  ✅
M2 Rej            0,893     0,930      −0,037
A1                0,909     0,956      −0,047
M2b Rej           0,877     1,000      −0,123   ← EN BÜYÜK
```

⚠️ **Bu sayılar bir elimiz bağlıyken alındı.** Harness (erişim + atıf doğrulama +
red kapısı) hiç açılmadı — tez döneminde iç ablasyonun gereğiydi, artık değil.
**Gerçek ürün sayımızı henüz hiç görmedik.**

---

## 1. Harness — en büyük kazanç burada

| bileşen | hangi açığı kapatır | nasıl |
| :--- | :--- | :--- |
| **atıf doğrulayıcı** | A1 0,909 → ~1,0 | uydurulmuş madde numarası **deterministik** yakalanır; hakem gerekmez |
| **red kapısı** | **M2b 0,877 → ~1,0** | doğrulanamayan atıf varsa cevap reddedilir — **kod, model değil** |
| **retriever** | M1 · M4 | gerçek kullanımda maddeyi kimse vermiyor; şu an eval veriyor |

⭐ **Ve kategorik bir üstünlük:** canlı mevzuat API'si (`bedesten.adalet.gov.tr`,
çalışıyor, [`docs/BEDESTEN_API.md`](docs/BEDESTEN_API.md)). Harness'lı bir model
**bugünün mevzuatını** cevaplar. Kapalı ağırlıklı rakipler cevaplayamaz — bu bir
eksende ilerleme değil, farklı bir kategori.

Ayrıntılı faz tarifi: [`docs/VISION.md`](docs/VISION.md) Faz 2.

## 2. Model — ölçülmüş, ucuz düzeltmeler

| # | açık | kanıt | bedel |
| :-: | :--- | :--- | :--- |
| 2.1 | **merge `τ_a`'yı seyreltiyor** | M2b 0,987 (tekil) → 0,877 (merge) | modül-başına norm · **$0** · ~1 saat |
| 2.2 | **`τ_a` şablon ezberledi** | M1 medyan cevabı **58 karakter** = şablonun kendisi; model cümleyi çekimliyor | [ADR-0051](docs/adr/0051-m2b-cift-kalibi-ve-chosen-uretimi.md) B planı · ~$2 |
| 2.3 | **muhakeme izi İngilizce** | 8/8 ölçüldü ([`kollar.md`](docs/record/kollar.md) #4) | veri turu |
| 2.4 | veri inceliği | 728 temiz negatif | hasat hattı kurulu, ucuz |

**2.1 her hâlükârda yapılmalı** — bedava ve merge'in bilinen kusurunu kapatıyor.
**2.3 vatandaş kararıyla öne çıktı:** Türkçe düşünmeyen bir model, vatandaşa
"okunabilir muhakeme" veremez.

## 3. Boyut — kısıt kalktı

Tez tek boyut noktasına kilitliyordu ([ADR-0028](docs/adr/gemma4-12b-dersler.md)).
**O kısıt yok.** 8B/12B çıkabilir, birden çok boyut yayımlanabilir.

Ama önce 4B'yi tavana yaklaştırmak daha verimli: reçete büyük modele taşınır,
tersi taşınmaz.

## 4. Ürün katmanı

- **Vatandaş kipi** — sadeleştirme **istem katmanında**, eğitim hedefi değil.
  ⚠️ Sade dille *eğitmek* denendi ve **doğruluğu düşürdü** ([ADR-0010](docs/adr/gemma4-12b-dersler.md#adr-0010)).
  Ders: *sadelik, doğru cevabın sunum katmanıdır.*
- Model kartı ve sürüm akışı (`v0.1` → `v1.0`, kabul testiyle)

---

## Opsiyonel: iddia katmanı (arxiv)

*"Merge, karışık ve ardışık SFT'den daha iyi korur"* iddiasını kanıtlayan
karşılaştırma — [`sprint2b.md`](sprint2b.md)'de tarifi hazır, **ertelendi**.

Artefaktlar (`τ_g`, `τ_a`, veri, protokol) bozulmuyor; arxiv'e karar verilirse
istenen zaman koşulur (~$19,64).

⚠️ **Ürün için gerekli değil.** *"Daha iyi mi"* sorusunu ölçüm zaten cevaplıyor;
o karşılaştırma *"neden daha iyi"* sorusunu cevaplıyor.

---

## Sırayı belirleyen argüman

Gerçek retriever ~5 gürültülü parça verecek — yani **M2b'ye benzeyen** koşullar.
**En zayıf olduğumuz eksen, üretimde en çok kullanılacak eksen.**

Bu iki yöne birden çekiyor ve karar buna bakarak verilir:
*"M2b'yi modelde düzelt"* ↔ *"M2b'yi red kapısı zaten kodla kapatıyor"*.
