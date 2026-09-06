# ADR-0062 — B10 aşırı-red turu KAPATILDI: hedef eğitimsiz karşılandı, sıradaki eksen B1

- **Tarih:** 2026-09-06
- **Durum:** kabul edildi
- **Karar veren:** insan
- **Kaynak ölçüm:** [#60](../record/research_log/2026-09-06-hasat-kabul-olcutu-coktu.md) ·
  [#61](../record/research_log/2026-09-06-dedektor-onarimi-b10-yeniden.md)
- **Kapatır:** [`superpowers/plans/2026-08-06-asiri-red-tau-a-v2.md`](../superpowers/plans/2026-08-06-asiri-red-tau-a-v2.md)
  (Görev 4-10 **koşulmadı**)
- **İzler:** [ADR-0061](0061-cekinme-dedektoru-istem-rejimi-bagimliligi.md)

## Bağlam

Turun amacı: aşırı-redi (altın madde bağlamdayken çekinme) **14/80 → 8-11/80** bandına indirmek
için `τ_a` v2'yi ORPO ile yeniden eğitmek. Ön-kayıtlı hedef bandı spec'te, sayı görülmeden yazıldı.

Görev 3'ün pilotu, planın **gözle okuma** adımında (Adım 3.8) hasadın kabul ölçütünü çürüttü.
ADR-0061 uyarınca `exact_reject` onarıldı ve etkilenen 82 çıktı **$0'a** yeniden puanlandı.
Ortaya çıkan tablo turun **öncülünü** değiştirdi:

| eksen | tur başlarken | **onarımdan sonra** |
| :--- | ---: | ---: |
| aşırı-red (B10) | 14/80 | **8/80** (gözle okuma) · 9/80 (alet) |
| kütle (ürün sayısı) | %62,8 | **%68,4** |
| coverage | 0,7625 | 0,8250 |
| hasat verimi (`kabul_orani`) | 0,1733 | **0,0667** |

## Karar

**Tur KAPATILDI. `τ_a` v2 eğitilmedi.** Gerekçe üç ölçülmüş sayıya dayanıyor:

1. **Ön-kayıtlı hedef zaten karşılandı.** Band **8-11/80** idi; ölçüm **8/80** veriyor — bandın
   alt ucundayız ve **hiç eğitim yapılmadı**. Aşırı-red gerçekti, ama büyüklüğünün **%43'ü
   aletin kendisiydi**.
2. **Hasadın bedeli getirisini aştı.** Gerçek verimle `250 ÷ 0,0667 = 3.750 üretim × 5,1 s =
   **5,3 saat ≈ $5,2**` — planın **D10** (3 saat) sınırını aşıyor, **D9** ($5) sınırını zorluyor.
   Üstüne eğitim ~$2. Toplam ~$7, hedefi **zaten tutturmuş** bir eksende.
3. **Kalan pay dar ve rakip yakın.** 8/80 ↔ 3.5 FL'ın 6/80'i. İki kalemlik bir fark için
   yedi dolar ve beş saat harcamanın gerekçesi kurulamadı.

**Sıradaki birinci eksen: B1 (isabet denetimi)** — *gerçek ama soruya uymayan madde*, ölçülen
**5/80** (önsözsüz ablasyon 7/80). ROADMAP §2 sırası buna göre güncellendi.

## Neyi kapatmıyor

- ⛔ **Aşırı-red SIFIRLANMADI, küçüldü.** 8/80 hâlâ 3.5 FL'ın **6/80**'inin üstünde. B10
  *"kapandı"* değil **"küçüldü, ölçüldü, birinci sıradan indi"** diye kapanır ve MODEL_CARD'ın
  Limitations bölümünde **açık sınır** olarak durur.
- ⛔ **KARAR-6'nın hükmü hâlâ insanındır** ve artık ölçülmüş sayılara dayanıyor: onarılmış
  ölçütle `Jaccard 0,90` · ayrışma **tek kalem** · ama kesişimin **7/9**'unda cevap metni farklı.
  ⭐ *Paralel slot metni değiştiriyor, çekinme kararını değiştirmiyor.* Bu, gelecekte servis
  rejimi (`-np`) kararında kullanılacak **ölçülmüş** bir girdidir.
- ⛔ **B4** (`τ_a`'nın merge'de seyrelmesi) ve **YB2** (M2b eğitim borcu) **açık kalır** —
  bu tur onları kapatacaktı, kapatmadı.
- ⛔ **ARA KAPI hâlâ düşük** ([#58](../record/research_log/2026-08-06-payda-tekillesmesi.md)):
  CP4-CP5 yetkisi yok. Bu tur onu değiştirmedi.

## Kabul edilen bedel

- **`τ_a` v2 diye bir kol yok.** *"Aşırı-red eğitimle ne kadar iner"* sorusu **ölçülmedi** ve
  ölçülmemiş olarak kalır. MODEL_CARD'ın Limitations'ına yazılır.
- Turun 41+ commit'lik hazırlığı (hasat aleti, Modal taşıyıcısı, ORPO paketleme reçetesi)
  **kullanılmadı** — ama **silinmez**: `b10_hasat.py`, `harvest_b10`, sızıntı süzgeci ve
  ADR-0047 m.2 taşıyıcısı çalışır durumda duruyor ve B1 turunda yeniden kullanılabilir.
- Ön-kayıtlı tahminlerin geri kalanı (kütle %64-66, KAPALI %75-79, Δ(önsöz)) **sınanmadı**.

## Sonuçlar

- Planın `İCRA DURUMU` bloğuna ✅ kapanış yazıldı; Görev 4-10 **koşulmadı** damgasıyla kapandı.
- **Ürünün resmî sayısı güncellendi:** kütle **%68,4** · B10 **9/80** (alet) · coverage **0,8250**.
  README ×2 ve MODEL_CARD taşındı; eski değerler damgalanarak duruyor.
- ADR-0061 Karar 2'nin yeniden türettiği eşikler (`aşırı-red < 0,4125` vb.) **kayıtta kalır** —
  bu tur kullanmadı, **bir sonraki eğitim turu kullanacak**.
- ⭐ **Turun asıl getirisi bir model değil, bir ölçüm:** *"bu repodaki en büyük tek kaybın
  %43'ü aletin kendisiydi"* — ve bunu yakalayan şey sayısal kapı değil, **planın gözle okuma
  adımıydı** (ADR-0051, ikinci kez kendini ödedi).
