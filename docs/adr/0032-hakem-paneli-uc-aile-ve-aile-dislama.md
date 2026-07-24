# ADR-0032 — Hakem panelinin üç ailesi + aile-dışlama haritası

**Statü:** Yürürlükte (aile seçimi kesin · **sürüm pinleme ve harcama Sprint 3**) · **Tarih:** 2026-07-24
**Otorite belge:** `TASARIM.md` §3.3 (dört katmanlı savunma) · §3.5 (sürüm kayması) · §6.2 (parite matrisi)
**İlgili:** ADR-0029 (tek model erişim kapısı) · ADR-0030 (base = Qwen3.5-4B) · ADR-0027 (aile-dışlama ilkesi)
**Kapatır:** `TASARIM.md` §13 açık soru **5** — *"üç büyük aile özneyse, panelde hangi üç aile?"*

---

## Bağlam

TASARIM §3.3'ün üçüncü savunma katmanı **aile-dışlama**: *"F ailesinden bir özneyi F ailesinin
hakemi puanlamaz."* Bu kural **base ailesi belli olmadan yazılamazdı** — §13'te açık soru olarak
bekliyordu. ADR-0030 base'i `Qwen/Qwen3.5-4B` olarak kilitledi, yani harita artık çizilebilir.

`sprint1.md` bunu Faz A çıkış ölçütü yapmıştı: *"Hakem panelinin üç ailesi yazıldı (base ailesine
göre aile-dışlama) — **harcama Sprint 3'te**."* Yani bu ADR **seçimi** kilitler, **parayı** değil.

---

## Karar

### 1. Panel = üç aile: **OpenAI · Anthropic · Google**

Gerekçe sırayla:

- **Özne ailesinden ayrık.** Bizim öznemiz Qwen (Alibaba) ailesinden türüyor. Panelin üç ailesinin
  hiçbiri Qwen değil → öznemiz için **üç hakem de tarafsız.**
- **Dış parite matrisinin rakipleri zaten bu üç aileden geliyor** (§6.2, "3 dağıtım-sınıfı rakip").
  Panel ile rakip kümesi aynı aileler olunca dışlama kuralı **her rakip için ısırıyor** — savunmada
  en sık sorulan *"rakibi kendi hakemiyle mi puanladınız"* sorusu yapısal olarak kapanıyor.
- **Erişim tek kapıdan** (ADR-0029, `scripts/llm_client.py`). `OPENROUTER_API_KEY` eklendiği an
  üçü de aynı koddan geçer; script değişikliği yok.

### 2. Aile-dışlama haritası

| özne | ailesi | OpenAI hakem | Anthropic hakem | Google hakem | uygun hakem |
| :--- | :--- | :--: | :--: | :--: | :--: |
| **Bizim merge** (τ birleşimi) | Qwen | ✅ | ✅ | ✅ | **3** |
| **Çıplak base** (Qwen3.5-4B) | Qwen | ✅ | ✅ | ✅ | **3** |
| Rakip-A | OpenAI | ❌ | ✅ | ✅ | 2 |
| Rakip-B | Anthropic | ✅ | ❌ | ✅ | 2 |
| Rakip-C | Google | ✅ | ✅ | ❌ | 2 |
| Tavan referansı | (matriste özne değil, §6.2) | — | — | — | — |

### 3. ⚠️ Asimetri — önceden yazılır, sonradan rasyonalize edilmez

Haritanın doğrudan sonucu: **bizim öznelerimiz 3 hakem alıyor, rakipler 2.** Bu, savunmada
*"kendi modelinizi daha çok hakeme puanlattınız"* diye okunabilir. Ön-kayıtlı ele alış:

1. **Manşet sayı, uygun hakemlerin ortalamasıdır** (bizde 3, rakipte 2).
2. **Ek olarak**, bizim öznelerimiz için **her 2-hakem alt kümesinin** ortalaması da raporlanır
   (3 alt küme). Sonuç bu alt kümelerin hiçbirinde değişmiyorsa asimetri sonucu taşımıyordur;
   değişiyorsa **o da bulgudur** ve öyle yazılır.
3. **Her öznenin hakem-başına ham skoru yayımlanır** (ek/appendix), κ ile birlikte.

### 4. Self-preference ölçümü — panelin sınırı

TASARIM §3.3 katman 4 self-preference'ı *ölçülecek bir bulgu* sayıyor. Panelde Qwen ailesi
**olmadığı için bizim öznemizde self-preference doğrudan ölçülemez** — yalnız üç rakipte ölçülür
(her biri kendi ailesinin hakemiyle de puanlanıp fark raporlanarak). Bu **kabul edilen bir sınırdır**
ve limitations'a yazılır: *"self-preference üç rakip ailede ölçüldü; kendi öznemizde ölçülemedi,
çünkü panelde o aile yok — ve panele koymak dışlama kuralını kendi lehimize gevşetirdi."*

Alternatif (paneli 4 aileye çıkarmak, Qwen dahil) **elendi**: maliyeti %33 artırır, ve Qwen
hakemini kendi öznemize uygulamak tam da dışlama kuralının yasakladığı şey — ölçüm için açıp
skorlama için kapatmak, savunulması güç bir çift standart olur.

### 5. Sürüm pinleme — **Sprint 3'e ertelendi, kuralı şimdi yazılı**

TASARIM §3.5: jenerik model adı kullanılmaz, **tarihli snapshot'a pinlenir**, ölçüm tarihi her
summary'ye yazılır. Bu ADR **aileleri** kilitler; **hangi sürüm** Sprint 3'te seçilir çünkü:

- rakip modeller hareketli hedef — bugün pinlenen sürüm Sprint 5'e kadar eskir;
- `llm_client.py`'ın **sağlayıcı pinleme** kontrolü (ADR-0029) o gün koşulmalı: özet JSON'daki
  `judge_providers` **tek eleman** olmalı, yoksa aynı model kimliği farklı servis yığınında
  (farklı kuantizasyon) koşmuş demektir ve **hata vermez.**

### 6. Sprint 1'de panel KULLANILMAZ

CP2 ↔ CP6 bir **iç kıyas**: base çıpaları ile `τ_grounding` aynı hakemle karşılaştırılıyor.
Aynı hakem iki tarafta olduğu sürece aile sayısı sonucu değiştirmez → **tek aile yeterli**
(bugünkü `OPENAI_API_KEY`, `gpt-4o-mini`). Panel, sayıların **raporlandığı** yerde gerekir:
**Sprint 3** (iç iddia kararı) ve **Sprint 5** (parite). ADR-0029'un maliyet çizelgesiyle hizalı.

---

## Elenen alternatifler

| eleme | neden |
| :--- | :--- |
| **Panele Qwen'i katmak** (4 aile) | Kendi öznemizi kendi ailesinin hakemine puanlatmak = dışlama kuralının ihlali. Self-preference'ı ölçmek için açıp skorlamada kapatmak çift standart |
| **Tek güçlü hakem** | TASARIM §11'de zaten elenmiş: aile self-preference'a savunmasız, uyum (κ) ölçülemez |
| **Rakipleri panelden farklı ailelerden seçmek** | Dışlama kuralı hiç ısırmazdı → katman 3 dekoratif olurdu. Rakip kümesi ile panelin **çakışması** kuralın işlemesinin şartı |
| **İnsan hakem / κ** | **Descoped** (annotator yok) — TASARIM §12'de kayıtlı, değişmedi |
| **Sürümleri bugün pinlemek** | Sprint 5'e kadar eskir; §3.5 gereği pin + ölçüm tarihi **aynı gün** olmalı |

---

## Sonuç

- `TASARIM.md` §13 açık soru **5 kapandı**; §13'e "→ ADR-0032" işareti düşülür.
- Sprint 1'de harcama **yok**; kod tarafı ADR-0029 ile zaten hazır.
- Limitations'a iki satır: **(a)** özne başına hakem sayısı asimetrik (3 vs 2), ele alışı §3'te;
  **(b)** kendi öznemizde self-preference ölçülemiyor.
