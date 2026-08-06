# ADR-0058 — B-i kaynak-yeterliliği önsözü ANA PROTOKOLE benimsendi

**Tarih:** 2026-08-06 · **Durum:** kabul · **Karar veren:** insan
**Kaynak ölçüm:** research_log #56 §5 (D1) · **Tadil eder:** ADR-0055 (B-i artık ablasyon değil)
**Çıktı dizini:** `outputs/eval/olcum-bi/` *(önsözsüz ablasyon koşusu: `outputs/eval/s2-harness-k10-etiketli/`)*

## Karar
`--sufficiency-preamble` ana protokolün parçasıdır. Ürünün resmî sayısı **%62,8**.
Önsözsüz koşu bundan sonra **ablasyon koludur** (damga tersine döner).

## Gerekçe
Bir EĞİTİM turunun çıpası, elde olan en iyi DAĞITIM yapılandırması olmalıdır. Aksi hâlde
istem katmanından bedavaya alınabilecek bir kazanç eğitime yazılır.

## Yeniden türetilen çıpalar
| eksen | eski (önsözsüz) | YENİ RESMÎ |
| :--- | ---: | ---: |
| kütle | %61,3 | **%62,8** |
| A1 (cevaplanan) | 0,8042 | **0,8229** |
| A1 · altın getirilen | 0,8616 | **0,8705** |
| B10 (altın geldi·çekindi) | 16/80 | **14/80** |
| B1 (altın gelmedi·cevapladı) | 7/80 | **5/80** |
| coverage · recall@10 | 0,7625 · 0,8750 | **değişmedi** |

## ⚠️ Bu bir eşik GEVŞETMESİ değildir
ADR-0050'nin kuralı: sonucu gördükten sonra **eşik değil alet** düzeltilir. Burada düzeltilen
ölçü birimi — hangi istemle üretilmiş bir sayıyla kıyaslandığı. Eşik **zorlaştı**.

## Kabul edilen bedel
#56'nın şerhi duruyor: 2/80'lik hücre hareketleri için ayrı bir gürültü tabanı ölçülmedi.
A1'deki +1,87 puan hakemin ölçülmüş 0,3 puanlık tabanının üstünde; hücre sayıları farklı
bir tahmin edicidir ve o taban ölçülmemiştir.

## Sonuçlar
- Eski %61,3 sütunu SİLİNMEZ; "önsözsüz ablasyon" olarak kalır.
- ⚠️ EĞİTİM VERİSİ bu değişikliği İZLEMEZ — gerekçesi ADR-0059 §sapma-1.
