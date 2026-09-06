# ADR-0063 — Yeterlilik önsözü KALDIRILDI · ADR-0058'in gerekçesi tersine döndü

**Tarih:** 2026-09-06 · **Statü:** ✅ yürürlükte · **Karar:** insan (açık soru **S14**)
**Değiştirdiği:** [ADR-0058](0058-b-i-kaynak-yeterliligi-onsozu-benimsendi.md) — *iptal değil,
gerekçesi çürüdü*

## Bağlam

ADR-0058 (2026-08-06) kaynak-yeterliliği önsözünü **ana protokol** yapmıştı. Gerekçesi tekti:
**önsöz kütleyi yükseltiyordu.**

2026-09-06'da çekinme dedektörü onarıldı ([ADR-0061](0061-cekinme-dedektoru-istem-rejimi-bagimliligi.md)):
*"açılış hükmü yok"* dalında dedektör cevabın tamamını tarıyordu ve bizim şablonumuzun
**eleme gerekçesi** (*"diğer kaynaklar … içermemektedir"*) red regex'ini tetikliyordu.
Onarılmış aletle aynı ölçüm **tersine döndü**.

## Ölçüm (v1 soru seti birimi, ADR-0067 öncesi)

Kıyas eşleşmiş ve ham dosyalardan doğrulandı: **aynı 80 id · 80/80 birebir aynı
`context_shown` · aynı `recall@10`** → değişen **yalnız istem**.

| eksen | önsözLÜ | önsözSÜZ | fark |
| :--- | ---: | ---: | ---: |
| **kütle** | %68,4 | **%73,0** | **−4,6 p** (önsöz aleyhine) |
| coverage | 0,8250 | 0,9000 | −7,5 p |
| A1 · cevaplanan | 0,8288 | 0,8110 | +1,8 p (önsöz lehine) |
| A1 · altın getirilen | 0,8729 | 0,8593 | +1,4 p (önsöz lehine) |
| isabetsizlik | 5/80 | 7/80 | önsöz lehine |
| aşırı-red | 9/80 | 5/80 | önsöz aleyhine |

⚠️ **−4,6 p'yi koruyan çözünürlük sınırı YOK:** hakem gürültü tabanı (0,3 p) yalnız **A1**
için ölçüldü; kütle = coverage × A1 ve **coverage'ın varyansı o tabanda yok**.

## Karar

**Ürünün varsayılan rejimi ÖNSÖZSÜZ.** Önsözlü koşu **ablasyon** koludur.
`gen_eval_grounded.py`'nin üç yerindeki *"ANA PROTOKOL / ABLASYON"* nitelemesi **takas edildi**;
ADR-0058'in hükmü **silinmedi**, *"yapılmıştı … TERSİNE DÖNDÜ"* diye damgalandı.
Künyedeki `ekstra : <yok>` satırı, önsözün gerçekten kapalı olduğunun **koşu-başına kanıtıdır**.

**Takas açıkça kabul ediliyor:** önsöz modeli *daha seçici ama daha suskun* yapıyor.
A1 ve isabetsizliği bir miktar iyileştiriyor, ama coverage'ı ve kütleyi düşürüyor. Vatandaş
ürünü için bağlayıcı metrik **kütledir**: cevaplanmayan soru vatandaş için değersizdir.
İsabetsizlik istem yamasıyla değil **kendi ekseninde** (B1, ADR-0066) ödenecektir.

## Sonradan gelen doğrulama

ADR-0070 (bütçe eşitlenmesi) bu kararın **yan etkisini** açığa çıkardı: önsöz kalkınca model
`</think>`'i daha sık kendi kapatıyor (zorla kapatma **21/80 → 5/80**), dolayısıyla ayrı 512
cevap payını alan kalem sayısı düştü ve **paylaşımlı bütçenin** bedeli görünür oldu.
⇒ S14 kararı o kusuru **yaratmadı, açığa çıkardı**.

## Reddedilenler
- **Önsözü koru** — A1/isabetsizlik lehine, kütleyi feda et: REDDEDİLDİ (kütle bağlayıcı metrik).
- **İkisini de dağıt, kullanıcı seçsin** — REDDEDİLDİ: vatandaşın veremeyeceği bir kararı
  vatandaşa devretmek olur.
- **Çözünürlük sınırı kararlaşana dek ertele** (S5 ile birlikte) — REDDEDİLDİ: −4,6 p hiçbir
  makul çözünürlük sınırının altında değil.
