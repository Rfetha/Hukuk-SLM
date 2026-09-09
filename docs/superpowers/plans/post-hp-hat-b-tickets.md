# post-hp-hat-b — açık tickets

Bu dosya, `hp-hat-a-hat-b` planının yürütülmesi sırasında (2026-09-09) ortaya çıkan ve o planın
kapsamında **çözülmeyen** kusurları kaydeder. Her ticket, gözlemi, kanıtı, kurulmuş hipotezi ve
yapılması gerekeni ayrı ayrı içerir. Hipotez ile ölçüm birbirine karıştırılmamıştır.

Durum: plan altı sıradan beşini kapattı. Açık olan tek kapı SIRA 2'dir (ticket 9).

---

## 1. Ürün yolunda cevapların yaklaşık yüzde beşi tamamen boş dönüyor

**Gözlem.** 80 soruluk geliştirme kümesinde `hakhukuk.servis.answer()` ile ölçüldü:

| | ürün yolu | ölçüm hattı |
| :--- | ---: | ---: |
| kesik veya boş cevap | 7/80 (%8,75) | 4/80 (%5,0) |
| tamamen boş metin | 4/80 (id 7, 64, 65, 66) | 0 |

**Kanıt.** `outputs/eval/g18-arac-katmani/aracsiz_yol_80.json`. Yedi kesik kalemin yedisi de
ölçüm hattında `finish=stop` ile tamamlanmıştır (485-892 belirteç), yani sorunun kaynağı
soruların zorluğu değildir.

**Neden.** Ölçüm hattı düşünce kanalını iki geçişte **zorla kapatır** (`--think-budget 1024`),
ürün yolu kapatmaz ve düşünce ile cevap tek bütçeyi (1536) paylaşır. Model bazı örneklerde
`</think>` etiketini hiç kapatmaz, bütçeyi düşüncede bitirir ve HTTP 200 ile boş içerik döner.
Bu bir sonlanmama sorunudur; araştırma kaydı #42'de aynı sınıf ölçülmüştür.

**Sonucu.** ADR-0040'ın geçerlilik kapısı yüzde beştir. Ölçüm hattı tam eşikte geçmekte, ürün
yolu yüzde 8,75 ile **geçememektedir**. Yayımlanan 0,8011 ölçüm hattının sayısıdır.

**Yapılacak.** Ürün yoluna iki geçişli zorunlu kapatma eklenecek mi, karar verilmeli. Bu bir
rejim değişikliğidir ve uygulanırsa 80 kalem yeniden ölçülmelidir.

---

## 2. Sunucu yapılandırması cevabı değiştiriyor, etkisi ölçülmedi

**Gözlem.** Aynı soru, aynı kod, seed 3407, sıcaklık 0; değişen tek etken KV önbelleğinin
kuantizasyonu:

| KV önbelleği | durum | `sha256` | uzunluk |
| :--- | :--- | :--- | ---: |
| `q8_0` (bütün ölçümlerin yapıldığı) | SUSKUNLUK | `79b6915a…` | 201 |
| varsayılan (fp16) | ÇEKİNCELİ | `e97a2b85…` | 622 |

**Kanıt.** Kontrollü deney: 8081 numaralı bağlantı noktasında varsayılan KV ile ikinci sunucu
açıldı, 8080 değiştirilmedi. Aynı yapılandırmada iki koşu birebir aynı çıktı verdi, yani bu
belirsizlik değil yapılandırmanın sonucudur.

**Sonucu.** Modeli indiren kişi kendi sunucu bayraklarını seçer. Bağlayıcı yapılandırma HF
kartının üçüncü bölümüne yazıldı, `MODEL_CARD` §7.10'a ve `servis.py` docstring'ine şerh düşüldü.

**Yapılacak.** Varsayılan KV ile 80 kalem yeniden ölçülmeli; bugün 0,8011'in o rejimde
korunacağı **iddia edilmiyor**. Bedeli sıfır dolar, yaklaşık bir saat GPU.

---

## 3. Arayüz soru sorulduğunda donuyor

**Gözlem.** `hakhukuk/tui.py` içinde `on_input_submitted` doğrudan `answer()` çağırıyor ve
Textual'ın olay döngüsünü otuz ile altmış saniye bloke ediyor. "Kaynaklar taranıyor" satırı bile
çizilemiyor, çünkü çizim aynı döngüde sıraya giriyor.

**Sonucu.** Donmuş ekran ile boş ekran kullanıcı açısından ayırt edilemiyor.

**Yapılacak.** `answer()` bir çalışan (worker) iş parçacığına alınmalı ve ilerleme göstergesi
gerçekten çizilmeli.

---

## 4. Boş sorgu reddedilmiyor, sabit bir gürültü kümesi dönüyor

**Gözlem.** Ölçüldü 2026-09-09:

```
_getir("", 10)   → RUMELİ DEMİRYOLLARI Madde 22 · ASAYİŞE MÜESSİR … Madde 1 ·
                    ÖZEL TÜKETİM VERGİSİ Madde 7 · OLAĞANÜSTÜ HAL … MADDE 12 …
_getir(" ", 10)  → aynı küme
```

Boş sorgu ile tek boşluk aynı sonucu veriyor; BM25 sıfır skor üretince sıralama korpus sırasına
düşüyor ve ilk on kayıt sabit bir gürültü olarak dönüyor. Model bu kaynaklarla çağrılıyor.

**Sonucu.** Anlamsız bir girdi, anlamlı görünen bir kaynak listesiyle karşılanıyor.

**Yapılacak.** Boş veya anlamsız kısalıktaki sorgu, retriever'a gitmeden reddedilmeli. Bu, bir
KAPI'dır ve döngü dışında uygulanmalıdır.

---

## 5. Erişim başarısız olduğunda kullanıcıya sinyal verilmiyor

**Gözlem.** Kullanıcı 2026-09-09'da iki soruda birbiriyle tamamen ilgisiz kaynak listeleri gördü
(örnek: Amme Alacaklarının Tahsili 51, Hususi Hastaneler 13, Damga Vergisi 30, Basın Mesleği 3).
Model doğru davranarak sustu, ancak arayüz *"getirilen kaynaklar sorunuzla ilgisiz"* bilgisini
vermiyor; kullanıcı bunu ürün hatası olarak okuyor.

**Ölçülmüş bağlam.** `recall@10` 0,9500'dür, yani her yirmi sorudan birinde doğru madde ilk ona
hiç girmez. Kapsam yalnızca yürürlükteki kanunlardır; yönetmelik, tüzük, KHK ve tebliğ korpusta
yoktur.

**Yapılacak.** İki ayrı iş: (a) getirilen kaynakların skor dağılımına bakıp *"zayıf eşleşme"*
durumunu arayüzde göstermek; (b) kapsam dışı soruları ayırt edip kullanıcıya kapsamı bildirmek.
İkisi de ürün yeteneğidir, ölçülen sayıya eklenmez.

---

## 6. Yanlış kaynağa atıf: frontier karşısında geride

**Gözlem.** `wrong_ref_rate_micro`: HakHukuk 0,0769, Claude Sonnet-5 0,0083. Yaklaşık 9,3 kat
geride.

**Ayrım.** Bu, uydurulmuş madde numarası değildir; o eksende önde olan taraf HakHukuk'tur
(0/114'e karşı 2/163). Model madde uydurmuyor, mevcut ve yanlış maddeye atıf yapıyor.

**Sonucu.** Planın *"B1'de rakiplerden geride değiliz"* hükmü yalnızca Gemini havuzunda
doğruydu. Frontier havuzunda geçmiyor.

**Yapılacak.** B1 borcu `v2` turuna taşındı. Bugün kapatılmıyor (ADR-0075).

---

## 7. Duman koşusundan doğrusal maliyet tahmini kapı kurmuyor

**Gözlem.** Beş kalemlik duman koşusundan çarpım yoluyla 0,82 dolar tahmin edildi; gerçekleşen
1,1932 dolar oldu, yani bir dolarlık kapı yüzde 45 aşıldı.

**Neden.** Cevap uzunluğu soruya göre değişen bir özne için beş kalemlik örneklem temsili
değildir. Gerçekleşen: cevap başına 706,6 belirteç, çıktı fiyatı milyon başına on dolar.

**Yapılacak.** Yeni bir özne eklenirken duman koşusu ya tabakalanmış seçilmeli (kısa, orta, uzun)
ya da kapıya yüzde elli emniyet payı konmalı.

---

## 8. Arayüz açılışında yönlendirme yok

**Gözlem.** Uygulama açıldığında çıktı alanı tamamen boştur; ne yapılacağını söyleyen bir satır
yoktur. Kullanıcı bunu "boş ekran" olarak okumuştur.

**Yapılacak.** Açılışta kısa bir yönerge gösterilmeli.

---

## 9. SIRA 2 kapısı açık

`hp-hat-a-hat-b` planının Görev 12 Adım 6-7 kapısı, insan gözüyle doğrulama gerektirir ve
kapanmamıştır. Üç soruda durum rozeti, atıflar, kaynaklar ve sorumluluk ibaresinin ekranda
görüldüğünün insan tarafından teyidi beklenmektedir.

Not: bu kapı çalışırken bir ürün kusuru yakalandı — `python -m hakhukuk.tui` komutu hiçbir şey
yapmıyordu, çünkü modülde `if __name__ == "__main__":` bloğu yoktu. Onarıldı ve testle çivilendi.
Kapının varlık sebebi tam olarak budur.

---

## 10. Dağıtım kararları

- **Push.** On üç commit `hp-hat-a-hat-b` dalında bekliyor, `origin`'e gönderilmedi. GitHub'daki
  açılış sayfası `master`'ı gösterdiği için biçim temizliği orada henüz görünmüyor.
- **Hugging Face.** Depo 2026-09-09'da insan kararıyla **özele** alındı; açık kusurlar giderilene
  kadar böyle kalacak. Yükleme ve `sha256` doğrulaması tamamlanmıştır, geri alınan yalnız
  görünürlüktür.
- **GitHub Pages.** Repoda Pages sitesi yoktur. Açılış sayfası olarak `README.md` güncellenmiştir;
  ayrı bir Pages sitesi kurulacaksa bu ayrı bir iştir ve planda yoktur.
