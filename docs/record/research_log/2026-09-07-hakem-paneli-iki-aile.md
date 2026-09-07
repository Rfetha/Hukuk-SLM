# #64 — Hakem paneli: ikinci aile eklendi, κ EŞİĞİN ALTINDA çıktı

**Tarih:** 2026-09-07 · **Plan:** `docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md` Faz 1
**Harcanan:** hakem **$1,9774** raporlanan / **$3,155** gerçekte düşen · GPU **$0**
**Karar:** [ADR-0074](../../adr/0074-hakem-paneli-kuruldu-baglayici-hukum.md)
**Çıktılar:** `outputs/eval/hp-hakem-paneli/` — `KAPPA.md` · `gnd_h1_tgta_v1_anthropic.jsonl` ·
`harness_tablo_anthropic.json`

## Ne yapıldı

Bugüne kadarki **her** sayı `openai/gpt-4o-mini`'nin tek başına hükmüydü. İkinci hakem ailesi
(`anthropic/claude-sonnet-5`) **aynı 80 cevabı** yeniden puanladı. ⛔ Üretim yeniden koşulmadı —
tek oynayan değişken hakem (ADR-0017).

## Bulgular

**(1) κ eşiğin ALTINDA — hakemler gerçekten ayrışıyor.**
`tam_sadık` κ = **0,534** · `atıf_temiz` κ = **0,409** (aracın kendi eşiği: ≥0,6 makul).
`faithfulness` Pearson r = 0,705 · `cit_precision` r = 0,487.

**(2) Kayma TEK YÖNLÜ — sistematik katılık, gürültü değil.**
Anthropic **24/80** kalemde daha düşük, **8/80**'de daha yüksek not verdi. A1 farkı
**11,33 puan** = yeniden-koşum gürültü tabanının (0,3 puan) **38 katı** ⇒ *"hakemler ayrışıyor"*
cümlesi kurulabilir.

**(3) Manşet sayı hakem seçimine duyarlı.**
Kütle **0,8011** (`gpt-4o-mini`) ↔ **0,6940** (`sonnet-5`). Coverage değişmedi (0,9375, hakemden
bağımsız); farkın tamamı A1'den (0,8545 → 0,7403).

**(4) 🚨 Ama bu tablodan *"kapı düştü"* SONUCU ÇIKARILAMAZ — ve çıkarmak ADR-0057 ihlali olurdu.**
Kapının eşiği (0,7225) çıpa rakip `3.5 Flash`'ın kütlesinden türetildi ve **o sayı da
`gpt-4o-mini`'nin hükmüdür.** İkinci hakem rakibi de aynı katılıkla notlarsa eşik de düşer.
İki tarafı farklı hakemlerle kıyaslamak kapıyı **sahte biçimde** devirir. ⇒ `0,6940` **açık borç**
olarak kaydedildi, **yayımlanmıyor**.

**(5) İddia düzeyinde κ KURULAMAZ — yapısal.**
İki hakem farklı sayıda iddia çıkardı (**273 ↔ 341**) ve iddialar birebir eşleşmiyor. Kalem
düzeyi tek ortak zemindir; ikili etiketler oradan türetildi.

**(6) 💸 Gerçek fatura, raporlanan bedelin 1,596 katı.**
`judge_cost_usd` toplamı **$1,977**, OpenRouter bakiyesinden düşen **$3,155**. Sebep kapının
kendi marjı — `llm_client.py`'nin docstring'i bunu zaten söylüyordu ama bütçe planı liste
fiyatıyla yapılmıştı. ⇒ Bundan sonra her tahmin **×1,6**.

**(7) 💸 Liste fiyat oranı maliyeti TAHMİN ETMİYOR.**
`sonnet-5` liste fiyatı `gpt-4o-mini`'nin ~14 katı, **gerçek bedeli 45 katı** ($0,0417 → $1,8604)
— hakem çok daha uzun gerekçe üretiyor. Duman koşusu şart; fiyat oranından ölçeklemek yanıltır.

**(8) ⛔ `:batch` varyantı bu yoldan kullanılamaz.**
`anthropic/claude-sonnet-5:batch` liste fiyatının tam yarısı ama senkron çağrıya **404** veriyor
(*"only available through the Batch API, use /api/beta/batches"*). `llm_client` senkron ⇒ ayrı
taşıyıcı demek. Bedeli $0 oldu (hiç çağrı geçmedi), olgu koda damgalandı.

## Kapanmayan

- **Panel iki aileli kaldı** — ADR-0032 üç aile diyor. Sebep sayıyla: bakiye **$3,45**, rakip
  kolunu ikinci hakemle puanlamanın tahmini gerçek faturası **$2,81** (bakiyenin %81'i) ve
  donmuş TEST kabul koşusunun puanlaması da aynı bakiyeden ödenecekti. **İnsan kararı: harcanmadı**
  — proje önceliği çalışan uçtan uca ürün.
- **Öz-tercih ölçülmedi.** Google özne ↔ Google hakem hücresi aile dışlaması gereği zaten
  **yasak**; o hücre hiçbir bütçeyle ölçülemez.
- **Borcun kapanma koşulu tek:** `3.5 Flash` kolunun aynı ikinci hakemle puanlanması.

## Ders

⭐ **Tek hakem bir "eksiklik" değil, ÖLÇÜLMÜŞ bir kırılganlıktı.** Panel kurulmadan önce bu bir
usul borcuydu; kurulduktan sonra sayısı var: manşet **11 puan** oynuyor. Ama aynı ölçüm, düzeltmenin
**tek taraflı yapılamayacağını** da gösterdi — hakem değiştirmek yalnız kendi kolunda yapılırsa
elde kalan şey daha doğru bir sayı değil, **eşiti olmayan bir sınavdır**.
