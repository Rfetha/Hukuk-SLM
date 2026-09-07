# ADR-0072 — `v1.0` rakip havuzu genişler · **ön koşulu hakem panelidir**

**Tarih:** 2026-09-07 · **Statü:** ✅ yürürlükte · **Karar:** insan
**Bağlı:** [ADR-0064](0064-v1-kapisi-uc-maddeli-on-kayit.md) (kapı) ·
[ADR-0032](0032-hakem-paneli-uc-aile-ve-aile-dislama.md) (3 aile + **aile dışlaması**) ·
[ADR-0057](0057-harness-rekabet-kapisi-esit-sinav.md) (eşit sınav) ·
[ADR-0050](0050-verim-kapisi-tahmin-edici-duzeltmesi.md) (eşik koşudan önce konur)

## Bağlam

`v1.0` kapısının çıpası **`google/gemini-3.5-flash`** (ADR-0064). Bugün ölçülen dört özne de
**tek sağlayıcıdan**: `3.1 FL` · `3.5 FL` · `3.5 Flash` + biz. İnsan kararı: *"`v1.0` release
olacaksa **diğer sağlayıcıların** 3.5-Flash seviyesindeki modelleriyle de karşılaştırılsın."*

Gerekçe doğru ve ürün-yönlü: *"Gemini'yi geçtik"* cümlesi **bir sağlayıcının** o günkü hattına
dair bir cümledir; vatandaş için anlamlı olan *"bu sınıftaki modellerin arasında neredeyiz"*dir.

## Karar

**1. Havuz genişler.** `v1.0` yayınında Gemini hattının yanında **en az bir başka sağlayıcının**
aynı sınıftaki modeli aynı eşit sınavda (ADR-0057) raporlanır.

**2. ⛔ Kapı eşiği OYNAMAZ.** ADR-0064 madde (1)'in çıpası **`3.5 Flash` olarak kalır** ve
δ = 2,0 puan sabittir. Yeni özneler **raporlanır**, eşiği **kurmaz**. Gerekçe ADR-0050: eşik
koşudan önce konur; sayı görüldükten sonra *"aslında şu rakibe göre..."* demek, kuralın
engellemek için var olduğu harekettir. Yeni bir özne bizi geçerse bu **negatif bulgu olarak**
yazılır, kapı yeniden tanımlanmaz.

**3. 🚨 AİLE DIŞLAMASI ENGELİ — havuzun şekli buradan çıkıyor.** Hakem bugün
`openai/gpt-4o-mini`. ADR-0032: **hiçbir özne kendi ailesinin hakemiyle notlanmaz.**

| aday özne | aile | bugünkü hakemle | bedeli |
| :--- | :--- | :--- | :--- |
| Claude Sonnet sınıfı | Anthropic | ✅ sorunsuz | yalnız yeni öznenin koşusu |
| GPT sınıfı (`gpt-*-mini` vb.) | **OpenAI** | ❌ **çakışır** | hakem **değişir** ⇒ bugünkü **dört sayı da** yeniden koşulur |
| Gemini hattı | Google | ✅ (mevcut) | — |

**⇒ Bir GPT öznesi eklemek, ölçümün tamamını yeniden fiyatlandırır.** Tek bir öznenin bedeli
değil, **panelin** bedelidir.

**4. Sıralama kilitlenir: T1 (hakem paneli) → sonra havuz genişlemesi.**
Bugünkü **her** sayı tek ailenin (`gpt-4o-mini`) hükmü; **κ yok**, öz-tercih ölçülmedi
(ADR-0064 §*"Ne KURULMAZ"* madde 2 bunu zaten borç olarak yazıyor). Panel kurulmadan havuzu
genişletmek, **aynı şüpheli hakemle daha çok sayı üretmek** olur — ve GPT öznesini zaten
imkânsız kılar. `scripts/judge_agreement.py` **hazır**, κ hesabı için yeni araç gerekmiyor.

## Reddedilenler

- **Havuzu şimdi genişlet, paneli sonra kur** — REDDEDİLDİ: GPT sınıfı bugünkü hakemle
  ölçülemez, yani genişleme **zaten yarım** kalır; ve panel sonradan kurulunca üretilen
  sayıların hepsi **yeniden koşulur**. Sıra tersine çevrilince aynı para iki kez ödenir.
- **Hakemi şimdi `gpt-4o-mini`'den başka bir aileye çevir** — REDDEDİLDİ: tek aileyi başka
  tek aileyle değiştirmek κ'yı **üretmez**; yalnız hangi ailenin öznesinin dışlandığını
  değiştirir. Sorun hakem **seçimi** değil, panelin **yokluğu**.
- **Havuzu Gemini ile sınırlı bırak** — REDDEDİLDİ: insan kararı açık ve gerekçesi ürün-yönlü.

## Açık kalan

- 🆕 **Hangi sağlayıcı(lar), kaç özne** — T1'in çıktısıyla birlikte kararlaştırılır; bedel
  öznebaşı ~$0,35 (F0.4'te ölçüldü: üç rakip çıpası **$1,35**).
- ⚠️ **Model sürümleri kayar.** *"3.5-Flash seviyesi"* bir **sınıf** tanımıdır, sağlayıcılar
  arasında birebir eşleşmez; her öznenin tam model kimliği künyeye yazılır ve *"eşdeğer sınıf"*
  iddiası **açıkça bir yargı** olarak damgalanır, ölçüm olarak değil.
