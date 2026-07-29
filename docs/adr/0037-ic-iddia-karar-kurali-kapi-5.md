# ADR-0037 — İç iddianın karar kuralı: **Kapı 5**, veriye bakılmadan yazıldı

**Statü:** Yürürlükte — ⚠️ **madde (d) 2026-07-29'da kaldırıldı, bkz. [ADR-0039](0039-kapi-6-parametrik-sizinti.md)**
· **Tarih:** 2026-07-28
**Otorite belge:** `TASARIM.md` §7 (kapılar) · §4.4 (karşılaştırma tabanları) · §3.2 (DEV/TEST)
**İlgili:** ADR-0036 (norm-dengeli ayar — kural **o ayarda** uygulanır) ·
`open_questions` **#9 → ✅ KAPANDI** · #8 (tekiller referans noktası) · #12
**Ön-kayıt notu:** Bu kural **hiçbir merge sonucu görülmeden** yazıldı. CP5 (`τ_grounding`)
o sırada henüz eval aşamasındaydı; hiçbir kafes hücresi üretilmemişti.

---

## Bağlam

`TASARIM.md` §7 dört kapı tanımlıyordu (0 register · 1 rakip boşluğu · 2 iş bölümü ·
3 hibrit kol) — ama **iç iddianın kendisi için kapı yoktu.** *"Merge tabanlardan iyi"* cümlesinin
sayısal karşılığı hiçbir yerde yazılı değildi.

Bu boşluk tehlikeli: `λ` · density · drop-rate DEV'de **taranacak**, ve tarama sonuçlarına
baktıktan sonra kural yazmak sonucu rasyonalize etmektir. §7'nin kendi cümlesi:
*"eşikler sonradan yazılırsa çıkan sonuç rasyonalize edilir."*

Zorluk, iddianın **tek metrik değil çatışma** olması: `τg+τa` hem grounding'i (M1/M4) hem
abstention'ı (M2/M2b) **aynı anda** korumalı. Tek skora indirgemek çatışmayı gizler; iki metriği
ayrı raporlamak *"kazandı mı"* sorusunu cevapsız bırakır.

## Karar — Kapı 5

**Ayar: norm-dengeli** (ADR-0036'nın ana sonucu). Ham TIES ablasyonunda aynı kural ayrıca
raporlanır ama iddia norm-dengeli üzerinden kurulur.

```
KAPI 5 — τg+τa şunların HEPSİNİ sağlamalı:

  (a) M1/M4   ≥  0.90 × (τg tek)          ← grounding korundu
  (b) M2/M2b  ≥  0.90 × (τa tek)          ← abstention korundu
  (c) BİLEŞİK = min(grounding, abstention)
      ve bu bileşikte Taban A ve Taban B'nin İKİSİ de geçilmeli
  (d) M5 (anti-hedef) base'in ÜSTÜNE ÇIKMAMALI     ← ❌ KALDIRILDI 2026-07-29
```

> ### ⚠️ Madde (d) 2026-07-29'da bu kapıdan ÇIKARILDI — [ADR-0039](0039-kapi-6-parametrik-sizinti.md)
>
> **Sebep:** CP6 (#41) `τ_g`'nin M5 ezber kütlesini %10.7 → %14.6 çıkardığını ölçtü. (d) sert veto
> olduğu için `τ_g` içeren **her** hücre — yani ölçmek üzere kurulmuş `τg+τa` dahil — (a)(b)(c)'yi
> geçse bile kalıyordu. **Kapı, ölçmek için kurulduğu şeyi ölçemeden kapanıyordu.**
>
> **Ne oldu:** (d) *silinmedi*, **kendi kapısına** taşındı — **Kapı 6**, aynı katılıkta
> (çıpa yine **base**, rakip değil) ve iki metrik üzerinden (coverage · ezber kütlesi), artı zorunlu
> delta yayını. Kapı 5 saf iç iddia olarak üç maddeye indi.
>
> **Ön-kayıt şerhi:** değişiklik tekil M5 sayıları görülmüşken, **hiçbir merge hücresi
> üretilmemişken** yapıldı. Ayrıntı ve elenen alternatifler ADR-0039'da.

**Referans noktaları tekil hücrelerdir** (`τg tek`, `τa tek`) — #8 gereği çiftle **aynı hattan**
geçmiş hâlleri. Farklı hattan geçmiş bir tekile oranlamak, orana budamanın hasarını da katardı.

### Seçim prosedürü — çoklu karşılaştırma

- DEV'de **tek bir kural** sabitlendi: *"bileşik ölçütü (`min`) maksimize eden konfigürasyon
  seçilir"*. **O tek konfigürasyon** TEST'e gider.
- Taranan **tüm** konfigürasyonların DEV skorları eklerde yayımlanır — saklanmaz.
- ⚠️ **Aynı seçim prosedürü tabanlara da uygulanır.** Taban A/B için de DEV'de en iyi checkpoint
  seçilir. Yoksa biz taranmış, onlar taranmamış olur — kıyas haksız hâle gelir ve iddia değersizleşir.

## Değerlendirilen alternatifler

| eleme | gerekçe |
| :--- | :--- |
| **Bileşik = aritmetik ortalama** `(g+h)/2` | ❌ **Takasa izin verir:** grounding'i şişirip abstention'ı feda etmek "kazanç" görünür. İddia tam olarak bunun olmadığını söylüyor; ölçüt onu ödüllendiremez |
| **Bileşik = harmonik ortalama** | Dengesizliği cezalandırır ama yine takas yapılabilir; `min` kadar keskin değil |
| **Asimetrik eşik** (ör. grounding %95, abstention %85) | Bir beceriyi kayırmak, *"çatışan becerileri **eşit** koruyor mu"* iddiasını bozar. **X = Y = %90** simetrik tutuldu |
| **Eşik yazmayıp "iyileşme var mı" demek** | Kapı değil temenni; §7'nin varlık sebebine aykırı |
| **Taranan en iyi `λ`'yı doğrudan raporlamak** | Çoklu karşılaştırma → optimistik sayı. Tek seçilmiş nokta + tüm tarama eklerde |
| **Tabanları taramadan koşmak** | Bizim taranmış, onların taranmamış olması = haksız kıyas; `D > A` tipi değersiz iddia |

## Sonuç — kabul edilen sınır

⚠️ **Güç analizi YOK.** Eşikler yazıldı ama *"DEV havuzunun `n`'i bu farkı ayırt etmeye
yetiyor mu"* sorusu **cevaplanmadı** — `TASARIM.md` §13'ün 3. sorusu açık kalıyor. Yani Kapı 5
bir **karar kuralıdır**, istatistiksel bir testin yerini tutmaz. Limitations'a bu hâliyle yazılır.

**%90 eşiği bir yargıdır, türetilmiş bir sayı değil.** Gerekçesi: %10 kayıp, bir becerinin
"korunduğunu" söylemenin makul üst sınırı; bu hattaki çöküşler (`#07` 0.741→0.000,
`#32` 0.96→0.53) bu bandın çok ötesinde. Yani eşik, ayırt etmesi gereken şeyi rahatça ayırt ediyor.
