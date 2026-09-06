# ADR-0058 — B-i kaynak-yeterliliği önsözü ANA PROTOKOLE benimsendi

**Tarih:** 2026-08-06 · **Durum:** kabul · **Karar veren:** insan
**Kaynak ölçüm:** research_log #56 §5 (D1) · **Tadil eder:** ADR-0055 (B-i artık ablasyon değil)
**Çıktı dizini:** `outputs/eval/olcum-bi/` *(önsözsüz ablasyon koşusu: `outputs/eval/s2-harness-k10-etiketli/`)*

> 🚨🚨 **2026-09-06 — BU KARARIN GEREKÇESİ TERSİNE DÖNDÜ. Karar yürürlükte, gerekçesi değil.**
>
> Önsöz **kütleyi yükselttiği için** benimsenmişti. Çekinme dedektörü onarılınca
> ([ADR-0061](0061-cekinme-dedektoru-istem-rejimi-bagimliligi.md) ·
> [#61](../record/research_log/2026-09-06-dedektor-onarimi-b10-yeniden.md)) yön **döndü**:
>
> | | eski (bozuk) alet | **onarılmış alet** |
> | :--- | ---: | ---: |
> | önsözlü (resmî) | %62,8 | **%68,4** |
> | önsözsüz (ablasyon) | %61,3 | **%73,0** |
> | **Δ(önsöz)** | **+1,5 p** ✅ | **−4,6 p** 🔴 |
>
> Kıyas **geçerli ve doğrudan ham dosyalardan doğrulandı** (künye yok — borç D-c):
> aynı 80 id · **80/80 birebir aynı `context_shown`** · aynı `recall@10` → değişen **yalnız istem**.
>
> ⚠️ **Ama karar salt kütleye dayanmıyordu** ve diğer ayakları **hâlâ ayakta**:
> A1 **0,8288 ↔ 0,8110** (önsöz +1,8 p) · A1·altın **0,8729 ↔ 0,8593** (+1,4 p) ·
> B1 isabetsizlik **5/80 ↔ 7/80** (önsöz lehine). Takas iki yönlü: önsöz modeli **daha seçici**
> ama **daha suskun** yapıyor (coverage 0,8250 ↔ 0,9000 · B10 9/80 ↔ 5/80).
>
> ⛔ **Protokol DEĞİŞTİRİLMEDİ** — ana protokol hâlâ önsözlü, resmî sayı **%68,4**.
> Değiştirmek **yeni bir ADR ve insan kararı** ister; açık soru **S14**
> ([`open_questions.md`](../open_questions.md)).

## Karar
`--sufficiency-preamble` ana protokolün parçasıdır. Ürünün resmî sayısı ~~**%62,8**~~ →
**%68,4** *(2026-09-06'da alet onarımıyla yeniden türetildi, ADR-0061)*.
Önsözsüz koşu bundan sonra **ablasyon koludur** (damga tersine döner) — ~~%61,3~~ → **%73,0**.

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

**⚠️ Önsözün atıf davranışına bedeli — ölçüldü, ADR-0058 yazılırken anılmamıştı.**
Önsöz A1'i kısmen **daha az söyleyerek** yükseltiyor: hakem iddia sayısı 268 → **206** (−%23),
atıf toplamı 118 → **83** (−%30), atıfsız geçen cevap 8 → **13**, katı kapının reddi 1 → **3**.
Atıf *hassasiyeti* de düşüyor (0,8974 → **0,8732**), *geri çağırması* da (0,8375 → **0,80**).
Uydurulmuş madde numarası sınıfı **iki koşuda da boş** (0) — değişen paydadır, iddia değil.
Kaynak: `outputs/eval/olcum-bi/harness_tablo.json` · `gnd_h1_tgta_v1_bi_k10_summary.json`
↔ `outputs/eval/s2-harness-k10-etiketli/` karşılıkları.
**Karar bu bedelle birlikte alınmıştır**: kütle (+1,4 p), A1 (+1,9 p) ve B10 (16 → 14) kazançları
ölçülü, bedel ise atıf yoğunluğunda. Bedelin ürün açısından kabul edilebilirliği **açık bir
sorudur** ve [`docs/open_questions.md`](../open_questions.md)'ye borç olarak girer.

## Sonuçlar
- Eski %61,3 sütunu SİLİNMEZ; "önsözsüz ablasyon" olarak kalır.
- ⚠️ EĞİTİM VERİSİ bu değişikliği İZLEMEZ — gerekçesi ADR-0059 §sapma-1.

---

## 🚨 DAMGA 2026-08-06 (kusur Ö-B) — A/B ablasyon koşusunun bir sayısı emekli dedektörden geliyordu

`outputs/eval/cp09-ab-ayrimi/` bu ADR'nin **A/B ayrım** koşusudur — önsözün M2 tarafındaki
etkisi orada ölçüldü. Kaydedilen `rejection_exact = 0,452` **artık var olmayan** bir dedektör
sürümüyle üretilmişti (ADR-0058'in açılış-hükmü kuralı henüz yoktu). Bugünkü aletle yeniden
puanlandı (**hakem çağrısı yok, $0** — `score_abstention --pay-kaynagi onceki --payda-kaynagi onceki`):

```
rejection_exact   0,452  →  0,484     (id 53 ve 55 açılış kuralıyla çekinmeye döndü)
rejection_rate    0,968  →  0,968     değişmedi (LLM hakemi yeniden koşmadı)
valid_traps          62  →     62     payda DEVRALINDI — aşağıdaki şerh
```

**3,2 puan = hakem gürültü tabanının (0,3 p) ~10 katı.** Eski özet
`abst_m2_base_suff_summary.json.ONCEKI-20260806` olarak duruyor.

**ADR-0058'in hükmüne etkisi: YOK.** Bu ADR'nin benimseme gerekçesi *kütle · A1 · B10* üzerine
kuruludur; `rejection_exact` bu ADR'de hiçbir eşiğe girmiyor. Düzeltmenin yönü zaten önsözün
**lehine** (regex artık önsözün emrettiği çekinmeleri sayıyor). Ama sayı kayıtta yanlış duruyordu.

> 🔴 **KAPANMAYAN:** bu koşunun **paydası** (62/70) hâlâ modele bağımlı — `m2` kolu K3/KARAR-2
> kapsamında onarılmadı. Özet dosyası `valid_trap_kaynagi` alanında bunu damgalıyor.
> Onarımın fiyatı ölçüldü: **≈$0,11**, tek ödemeyle 10 m2 koşusunu birden kapatır
> ([`open_questions.md`](../open_questions.md)). **İnsan kararı bekliyor.**
