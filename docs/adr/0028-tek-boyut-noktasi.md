# ADR-0028 — Tek boyut noktası: tez tek base üzerinde tamamlanır

**Statü:** Yürürlükte · **Tarih:** 2026-07-24
**Otorite belge:** `TASARIM.md` §8
**İlgili:** ADR-0027 (**iki boyut noktası kısmı süperseded**) · ADR-0018 (eğri şartı — **karşılanmıyor, kabul edildi**) · ADR-0017 (dış geçerlilik sınırı — **teyit ve genişletildi**) · ADR-0026 (base bir parametre)

---

## Bağlam

ADR-0027 **iki boyut noktası** kararlaştırmıştı: birincil ~4B (tam ızgara) + aynı ailenin bir üst
boyutu (yalnız kazanan konfigürasyon). Gerekçe ADR-0018'in *"erişilebilirlik tek nokta değil eğri
olarak raporlanır"* şartıydı — ve eğri için en az iki nokta gerekiyor.

Kullanıcı kararı (2026-07-24): **tez tek base üzerinde tamamlanır.** İkinci boyut, makale bittikten
sonra, **aynı reçeteyle ayrı bir geçiş** olarak yapılır — tezin içinde değil.

---

## Karar

### 1. Tek boyut noktası

Tüm deney ızgarası **tek base** üzerinde koşar: 3 kol + 2 taban + 7 hücreli kafes + harness +
dış parite matrisi. Çalışma varsayımı ~4B sınıfı instruct model (ADR-0026'nın doğrulama kapısına
bağlı, ADR-0027 §8).

**FT bütçesi 10 → 6** (Kapı 0 `τ_register`'ı düşürürse **5**). Sprint sayısı **6 → 5.**

### 2. İkinci boyut = **koşullu opsiyon**, planlanmış adım değil

Tez tek base'de bitirilir. Daha büyük bir modelin ince-ayarı **ancak dışsal bir tetikle** gündeme
gelir — takvimde yeri yoktur, kimse onu beklemez:

| tetik | ne değişir |
| :--- | :--- |
| **Ürüne dönüşürse** | dağıtım kalitesi tezin değil ürünün gereği olur; daha büyük model ticari gerekçeyle koşulur |
| **Destek/kaynak gelirse** | compute kısıtı gevşer, ölçek sorusu maliyetsiz sorulabilir hâle gelir |
| **Makale büyürse** | boyut ekseni hakem talebi ya da dergi kapsamı nedeniyle gerekli olursa |

Hiçbiri gerçekleşmezse **tez eksik kalmaz** — Y1 (parite) ve Y2 (iş bölümü) tek noktada tam ölçülür.

Reçetenin taşınabilir olması zaten tasarımın bir özelliği: base bir parametre (ADR-0026), hiçbir
script'te gömülü default yok, doğrulama kapısı (ADR-0027 §8) her base için aynı. Yani opsiyon
açık tutuluyor ama **hiçbir maliyeti şimdi ödenmiyor.**

### 3. Bunun bedeli — açıkça kabul edilir

**(a) Dış geçerlilik açığı kapanmıyor.** *"Bulgular bu base'e mi özgü?"* sorusu cevapsız kalır.
Bu, 12B hattının kalıcı sınırıydı ve yeni hatta **aynen miras kalıyor.** ADR-0017 bunu zaten
"kapatılmayan sınır" olarak yazmıştı; ADR-0028 o sınırı **boyut eksenine de** genişletir.

**(b) Kapasite sorusu ölçülemez.** *"Çatışan beceriler kapasite arttıkça birbirini daha az mı
yiyor?"* — merge iddiasının en ilginç ikinci sorusu. Tek noktada sorulamaz. Merge bulgusu
(hangi yöne çıkarsa çıksın) **tek boyuta ait bir bulgu** olarak raporlanır.

**(c) ADR-0018'in "eğri" şartı karşılanmıyor.** Erişilebilirlik tek noktada raporlanır. ADR-0018'in
soft-gate çerçevesi (≤8 GB tercih bandı, aşan yapılandırmalar kayıpla raporlanır) **ilke olarak
ayakta** — ama ölçülmüş bir eğri olmadan, tek bir işaretli noktadır.

**Üçü de limitations bölümüne yazılır.** Gizlenmez, "gelecek çalışma" diye geçiştirilmez.

---

## Değerlendirilen alternatifler

| elenen | neden |
| :--- | :--- |
| **İki boyut noktası (ADR-0027'nin kararı)** | 4 ek FT + bir sprint. Tez zaten tek noktada tam: parite iddiası da iş bölümü ayrıştırması da tek boyutta ölçülebiliyor. İkinci nokta *eğriyi* verir, *iddiayı* değil. |
| **Dört donanım tier'ı** (referans belgenin önerisi) | Zaten ADR-0027'de elenmişti; 4× maliyet, çekirdek çalışmayı aç bırakır. |
| **İkinci noktayı küçültmek** (ör. yalnız 1 kol tekrarlamak) | Tek kol ne eğri verir ne replikasyon; iki dünyanın da kötüsü. |
| **İkinci noktayı tez içinde tutup harness'ı çıkarmak** | Harness parite iddiasının yarısı (ADR-0019); boyut eğrisi değil. Yanlış takas. |

---

## Sonuçlar

- **ADR-0027'nin "iki boyut noktası" maddesi süperseded** — ADR-0027 **yeniden yazılmaz**, o günkü
  gerekçe (eğri şartı + confound kontrolü için aynı-aile kuralı) kayıtta kalır ve ikinci geçiş
  yapılacağı gün **doğrudan uygulanabilir reçetedir.**
- **Aynı-aile kuralı geçerliliğini korur** — ikinci geçiş yapıldığında aile *ve* boyut birlikte
  değişirse fark hiçbirine atfedilemez (ADR-0017 çok-base kolunu bu yüzden elemişti). Karar
  ertelendi, kural değil.
- **Kapı 4 (karşıtlık noktası) kaldırıldı.** Geriye dört kapı kalır: Kapı 0 (register) ·
  Kapı 1 (rakip boşluğu) · Kapı 2 (iş bölümü) · Kapı 3 (hibrit kol).
- **Sprint 6 dağıldı:** içindeki iki iş — *eval ≠ dağıtım hizalaması* ve *gerçek donanımda VRAM
  ölçümü* — zaten ikinci boyut noktasına bağlı değildi, birincil modelin kendisi hakkındaydı.
  Sprint 5'e taşındı.
- **Merge'in bedavalığı değişmedi** — 7 hücrenin tamamı hâlâ 6 (ya da 5) koşudan türüyor.
