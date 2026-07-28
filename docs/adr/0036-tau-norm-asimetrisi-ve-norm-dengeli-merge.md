# ADR-0036 — ΔW norm asimetrisi: ana sonuç **norm-dengeli** merge, ham TIES ablasyon

**Statü:** Yürürlükte · **Tarih:** 2026-07-28
**Otorite belge:** `TASARIM.md` §4.2 (birleştirme) · §4.3 (kafes) · §7 (kapılar — ön-kayıt kuralı)
**İlgili:** ADR-0027 (eşzamanlı k-yollu TIES/DARE) · **open_questions #12 → ✅ KAPANDI** ·
#13 (rejim eşleşmesi — asimetrinin kaynağı orada ölçüldü) · #8 (tekil hücreler)
**Kanıt:** eğitim rejimi karşılaştırması (aşağıdaki tablo) · TIES adım analizi (Yadav+ 2023,
arXiv:2306.01708) · DARE (Yu+ 2023, arXiv:2311.03099)

---

## Bağlam — sorun ölçüm öncesi görülebiliyor

İki kol farklı ölçekte eğitiliyor ve bu **kasıtlı** (her yöntemin kendi reçetesi var, #13):

| | optimizer adımı | lr | veri |
| :--- | ---: | ---: | ---: |
| `τ_grounding` (SFT) | **1.083** | 1e-4 | 17.323 |
| `τ_abstention` (ORPO, 3 epoch) | **82** | 1e-5 | 1.741 çift |

~13× az güncelleme + 10× düşük lr → `‖τ_a‖`'nın `‖τ_g‖`'den **belirgin küçük** çıkması bekleniyor.

**Neden bu bir ölçüm hatasına dönüşür.** TIES'ın üç adımından ikisi **kütle ağırlıklı**:

```
① budama   : τ̂_t = en büyük k% |değer|                    ← norma DUYARSIZ (vektör içi)
② işaret   : γ_p = sgn( Σ_t τ̂_t,p )                        ← KÜTLE oyluyor
③ ortalama : A_p={t: sgn(τ̂_t,p)=γ_p};  (1/|A_p|)Σ_{A_p} τ̂  ← kaybeden HİÇ girmez
```

Küçük normlu vektör, **gerçek çatışmanın olduğu her parametrede** otomatik kaybeder ve
katkısı sıfırlanır. Sonucu *"abstention merge'de eziliyor"* diye okuruz — oysa sebep çatışma
değil **ölçek**. Bu, tezin ölçmek istediği şeyin tam olarak ölçülemez hâle gelmesidir.

**Sayısal gösterim** (5 parametre, p1'de gerçek çatışma):

```
τ_g = [ 0.80, -0.60, 0.10, 0.40, -0.02]   ‖τ_g‖ = 1.082
τ_a = [-0.10,  0.05, 0.09,-0.08,  0.01]   ‖τ_a‖ = 0.165      oran ≈ 6.6×
```

| density %40, p1 | işaret oyu Σ | sonuç | `τ_a` katkısı |
| :--- | ---: | ---: | :--- |
| **ham TIES** | +0.70 (ezici) | 0.80 | **tamamen silindi** |
| **norm-dengeli** | +0.132 (başa baş) | 0.739 | yarışa girdi; p3'te katkı 0.09 → **0.547 (6×)** |

⚠️ **DARE bu sorunu ÇÖZMEZ.** `τ̃ = (m⊙τ)/(1−p)` beklenen değeri korur, dolayısıyla **oranı da
korur** — 6.6× asimetri DARE'den sonra da 6.6×'tır. DARE'in derdi *çok vektör arası girişim*,
ölçek eşitleme değil. İki problem ayrıdır ve karıştırılmamalıdır.

## Karar

**Üç parça, hepsi veriye bakılmadan sabitlendi** (`TASARIM.md` §7 ön-kayıt kuralı):

1. **`‖τ‖` ölçümü KOŞULSUZ.** Her kol eğitilir eğitilmez Frobenius normu (katman bazında +
   toplam) hesaplanıp `outputs/`'a yazılır ve **sayı ne çıkarsa çıksın raporlanır.**
   `‖τ_g‖ / ‖τ_a‖` oranı çalışmanın künye bilgisidir.
2. **Kafes İKİ ayarda koşulur:** **ham TIES** (`w_g = w_a = 1`) ve **norm-dengeli**
   (`τ_t ← τ_t/‖τ_t‖`, sonra TIES, sonra `λ` ile ölçekle). Merge'in eğitim maliyeti sıfır
   olduğu için bedel yalnız eval'de.
3. **Ana sonuç = norm-dengeli. Ham TIES = ablasyon**, yanında raporlanır, gizlenmez.

## Değerlendirilen alternatifler

| eleme | gerekçe |
| :--- | :--- |
| **Yalnız ham TIES** (müdahalesiz) | Daha *gerçekçi* — üründe kimse normu elle eşitlemez. **Ama iç iddiayı ölçemez:** "abstention kayboldu mu, vektörünüz mü küçüktü?" sorusu cevapsız kalır. Ablasyon olarak korunuyor |
| **Yalnız norm-dengeli** | Jüriye tek taraflı görünür; asimetrinin gerçek etkisi gizlenmiş olur |
| **Kol başına ağırlık `w_t`'yi DEV'de taramak** | Ekstra serbestlik derecesi → #9'un karar kuralına dahil edilmesi gerekirdi ve çoklu karşılaştırma sorununu büyütürdü. Norm normalizasyonu **mekanik** ve taramasız |
| **`lr`/batch'i eşitleyip asimetriyi kaynağında yok etmek** | #13'te reddedildi — çalışan ORPO reçetesini kıyas uğruna bozmak kötü takas. Tetiğe bağlandı |
| **DARE ile çözmek** | Matematiksel olarak çözmüyor (yukarıda); yanlış araç |

> **Ek (aynı gün, `open_questions` #8):** tekil hücreler de **aynı hattan** geçer (budama +
> normalizasyon + `λ`) — yoksa tekil↔çift farkı budamanın hasarını da içerir ve atıf bozulur.
> Buna karşılık **bir `τ_g` DÜZ kontrol hücresi** eklendi (`λ=1`, işlemsiz): normalize edilmiş
> bir tekil *"τ_g ne satın aldı"* değil *"τ_g'nin YÖNÜ λ büyüklüğünde ne satın aldı"* sorusunu
> cevaplar; düz kontrol farkı görünür kılar. **Fiilî kafes: 4 hücre × 2 ayar = 8 eval.**

## Sonuç — kabul edilen bedel

- **Eval maliyeti iki katına çıkıyor** (kafes × 2 ayar). Merge bedava olduğu için bu yalnız hakem
  + üretim maliyeti; kabul edilebilir.
- **Norm normalizasyonu bilgi atıyor:** kolun *büyüklüğü* de bir sinyal olabilir ("bu beceri
  daha büyük bir değişiklik gerektiriyordu"). Bunu attığımızı **limitations'ta yazıyoruz**;
  ham TIES ablasyonu tam da bu bilgiyi geri veriyor.
- **Sapma kaydı:** TIES literatürü normalizasyonu standart adım olarak tanımlamaz. Yaptığımız
  şey bir **varyant**, ve paper'da öyle sunulacak — "TIES uyguladık" değil, "TIES'ı norm-dengeli
  ön-adımla uyguladık, ham hâlini de raporladık".
