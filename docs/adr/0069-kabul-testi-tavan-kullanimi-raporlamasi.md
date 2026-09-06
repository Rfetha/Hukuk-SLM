# ADR-0069 — Kabul testi raporlaması: ham kütle + tavan kullanımı

**Tarih:** 2026-09-06 · **Statü:** ✅ yürürlükte · **Karar:** insan
**Kapattığı açık soru:** **S15** · **Ön-kayıt:** kabul testi **henüz koşmadı**

## Bağlam

`v1` kabul testi donmuş TEST'te (`data/eval/canon/`) koşacak, ama bütün geliştirme ölçümleri
DEV'de yapıldı. 2026-09-06'da ölçüldü ki iki setin **erişim tavanı farklı**:

| | `recall@10` | ⇒ kütle tavanı |
| :--- | ---: | ---: |
| DEV (80) | 0,9500 | **%95** |
| TEST core_hard (40) | 0,7500 | **%75** |

Kütle `= coverage × A1` ve altın madde bağlama girmediyse doğru cevap üretilemez ⇒ **kütle,
`recall@10`'u aşamaz.** Fark setin daha zor sorular içermesinden değil **bileşimden** geliyor:
ayrım kanuna göre katmanlı ama **madde uzunluğuna göre katmanlanmamış**; en zor uzunluk
diliminde (Q4, `recall@10` 0,6667) DEV'in payı %12, TEST'in **%50**. **Bileşim farkın %81'ini
açıklıyor** ([ANALIZ](../../outputs/eval/f01c-dev-test-farki/ANALIZ.md)).

**Risk:** DEV'de %73,0 yayımlanır, kabul testinde ~%58 çıkarsa, model hiç kötüleşmemiş olduğu
hâlde tablo **gerileme** gibi okunur.

## Karar

**1. Ham kütle MANŞET ve BAĞLAYICI sayıdır.** Kabul testi sonucu ham raporlanır.

**2. Yanına tek bir tanısal oran eklenir:**

```
tavan kullanımı  =  kütle ÷ recall@10
```

*"Altın madde bağlama girdiğinde model onu ne kadar iyi kullanıyor."* Her seti **kendi
tavanına** böldüğü için **setten bağımsızdır** ve DEV ↔ TEST arasında kıyaslanabilir.
Bugünkü DEV değeri: `0,730 ÷ 0,9375 = 0,779`.

**3. Ön-kayıtlı korumalar — oranın kötü sonucu süslemesini engellemek için:**
- ⛔ Tavan kullanımı **KAPI DEĞİLDİR.** `v1.0` kapısının üç maddesi (ADR-0064) ham kütle,
  isabetsizlik ve M5 üzerinden kurulur; bu oran hiçbirinin yerine geçmez.
- ⛔ **Rakip kıyas cümlesi bu orandan KURULMAZ.** Rakip kıyası DEV'de, eşit sınavda yapılır
  (ADR-0057) ve orada üç özne de aynı `recall`'u görür — tavan farkı zaten yoktur.
- ✅ Her iki setin `recall@10`'u sayının **yanında zorunlu** olarak yazılır; tavan görünmeden
  oran yayımlanmaz.
- ✅ DEV sayısı ile TEST sayısı **aynı metrik değildir** ve yan yana konurken tavan farkı
  damgalanır.

## Reddedilenler

- **(b) yalnız ham + şerh** — REDDEDİLDİ: şerh, farkın **ne kadarının** bileşim olduğunu
  okuyucuya vermiyor; *"%73 duyurduk, %58 çıktı"* okumasını engellemiyor.
- **(c) ayrımı yeniden katmanla** — REDDEDİLDİ: **donmuş TEST'i açar**, usulü kırar.
- **Tam "standardize kütle" raporlamak** — REDDEDİLDİ: zorluk düzeltmesi kötü sonucu süslemenin
  kapısıdır. Tavan kullanımı bundan dar: tek bir bölme, gizli ağırlıklandırma yok.

## Neden ŞİMDİ karar verildi

Kabul testi **henüz koşmadı**. ADR-0050 raporlama biçiminin koşudan **önce** ön-kayıtlanmasını
istiyor: sayı görüldükten sonra *"zorluk düzeltilirse şu kadar"* demek, kuralın engellemek için
var olduğu şeydir.

## Açık kalan, bu ADR'nin KAPATMADIĞI

- 🆕 **Uzun madde chunk'lama borcu** — Q4'te `recall@10 = 0,6667`. B9'dan **ayrı**: orada bozuk
  chunk var, burada **doğru ama çok uzun** chunk. chunk = tam madde (ADR-0054/K2) kararının
  ilk ölçülen bedeli.
- ⚠️ **Ayrımın katmanlanmamış olması** — düzeltmek donmuş TEST'i açmak demek; bugün yapılmıyor.
