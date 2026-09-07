# ADR-0074 — Hakem paneli kuruldu (iki aile), bağlayıcı hüküm kuralı

**Tarih:** 2026-09-07
**Durum:** Kabul edildi
**Bağlam:** plan `docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md` Faz 1 (Görev 1-3)

> ⛔ **BU KURAL KAPI KOŞUSUNDAN *ÖNCE* YAZILDI** (2026-09-07). ADR-0050 gereği raporlama
> biçimi koşudan önce ön-kayıtlanır; sayı görüldükten sonra *"şu hakeme göre…"* demek
> kuralın engellediği şeydir. Görev 16'nın kabul koşusu bu kurala tabidir.

## Sorun

Bugüne kadar yayımlanan **her** sayı `openai/gpt-4o-mini`'nin **tek başına** hükmüydü.
κ hesaplanmamış, öz-tercih ölçülmemişti — ADR-0064 bunu *"Ne KURULMAZ"* madde 2 olarak
borç yazmıştı.

## Ölçülen (2026-09-07)

İkinci hakem ailesi (`anthropic/claude-sonnet-5`) **aynı 80 cevabı** yeniden puanladı.
Üretim yeniden koşulmadı — yalnız hakem değişkeni oynadı (ADR-0017).

| eksen | ölçü | değer | eşik (aracın kendi eşiği) |
| :--- | :--- | ---: | :--- |
| `faithfulness` | Pearson r | 0,705 | — |
| `cit_precision` | Pearson r | 0,487 | — |
| `tam_sadık` | Cohen's κ | **0,534** | κ ≥ 0,6 makul ⇒ **ZAYIF** |
| `atıf_temiz` | Cohen's κ | **0,409** | **ZAYIF** |

Kayma **tek yönlü**: Anthropic 24/80 kalemde daha düşük, 8/80'de daha yüksek not verdi.
A1 farkı **11,33 puan** = yeniden-koşum gürültü tabanının (0,3 puan) **38 katı**.

Manşet üzerindeki etkisi:

| | `gpt-4o-mini` | `claude-sonnet-5` |
| :--- | ---: | ---: |
| kütle | **0,8011** | **0,6940** |

Ayrıntı: [`outputs/eval/hp-hakem-paneli/KAPPA.md`](../../outputs/eval/hp-hakem-paneli/KAPPA.md)

## Karar

**(a) Bağlayıcı hakem = `openai/gpt-4o-mini`.**
Gerekçe tercih değil, **eşit sınavdır** (ADR-0057): kapının **iki tarafı da** — bizim kol ve
çıpa rakip `3.5 Flash` — yalnız bu hakemle ölçüldü. Anthropic hakem yalnız **bizim** kolumuzu
puanladı; rakip kolu puanlanmadan `0,6940` sayısı **eşiti olmayan bir sınavın sonucudur** ve
`v1.0` kapısına **sokulamaz**. Bir sayıyı başka hakemin eşiğiyle kıyaslamak, kapıyı sahte
biçimde devirir ya da sahte biçimde geçirir — yön fark etmez, ikisi de aynı kusurdur.

**(b) κ eşiğin altında çıktı — ne olur.**
κ (0,534 · 0,409) *"makul"* eşiği 0,6'nın altında. Bu, yayımlanan sayıyı **geçersiz kılmaz**
ama **kırılgan** yapar. Sonuç: manşet sayının yanında bundan böyle şu şerh **zorunludur**:

> *"Bu sayı tek hakem ailesinin (`gpt-4o-mini`) hükmüdür. İkinci bir aile
> (`claude-sonnet-5`) aynı 80 cevabı puanladığında kütle %80,1 → %69,4 düşmüştür
> (κ = 0,534, eşiğin altında). İki tarafı aynı hakemle ölçen bir kıyas kurulmadığı için
> bu düşüş kapı hükmüne girmez, ama sayının hakem seçimine duyarlı olduğu ölçülmüştür."*

**(c) Hükmün hangi kısmı kaç aileye dayanıyor.**
- **Hiçbiri üç aileye dayanmıyor.** Panel **iki ailelidir**; ADR-0032'nin üç aile kuralından
  **sapılmıştır** ve bu yayında eksiklik olarak yazılır.
- Sapmanın sebebi ölçüldü: OpenRouter bakiyesi **$3,45**, rakip kolunu ikinci hakemle
  puanlamanın tahmini gerçek faturası **$2,81** (bakiyenin %81'i) ve donmuş TEST kabul
  koşusunun puanlaması da aynı bakiyeden ödenecekti. **İnsan kararı 2026-09-07: harcanmadı;
  proje önceliği çalışan uçtan uca ürün, hakem panelinin tamamlanması değil.**
- **Öz-tercih ÖLÇÜLMEDİ** ⇒ *"hakem kendi ailesini kayırmıyor"* cümlesi **kurulmaz**.
  Google özne ↔ Google hakem hücresi aile dışlaması (ADR-0032) gereği zaten **yasaktır**;
  o hücre hiçbir bütçeyle ölçülemez.

## Sonuçlar

- `v1.0` kapısı (Görev 16) **`gpt-4o-mini` ile** koşulur; başka hakem hükmü kapıya girmez.
- `KAPPA.md`'deki `0,6940` **açık borç** olarak durur, **yayımlanmaz** — eşiti olmayan sınav.
- Borcun kapanma koşulu tektir: `3.5 Flash` kolunun **aynı ikinci hakemle** puanlanması.
- ADR-0072'nin GPT öznesi bu turda **eklenmedi** (hakemi değiştirir + dört sayıyı yeniden
  koşmayı gerektirir); ADR-0072 açık kalır.

## Reddedilenler

| seçenek | neden reddedildi |
| :--- | :--- |
| Anthropic hükmünü bağlayıcı yapmak | Eşit sınav yok — rakip kolu o hakemle puanlanmadı |
| Panel ortalamasını bağlayıcı yapmak | Aynı sorun + iki hakemin ortalaması aykırıyı gizler |
| Üçüncü aileyi (Google) eklemek | ~$0,72-2,46; kapı hükmünü **çözmez** (eşit sınav sorunu aynı kalır) |
| `0,6940`'ı yayımlamak | ADR-0057 ihlali — hakemi eşleşmemiş kıyas |
