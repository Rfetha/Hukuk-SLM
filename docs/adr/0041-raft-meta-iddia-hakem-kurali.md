# ADR-0041 — RAFT meta-iddiaları hakemde iddia sayılmaz · geriye dönük ve **tüm kollara** uygulanır

**Statü:** Yürürlükte · **Tarih:** 2026-07-29
**Otorite belge:** `TASARIM.md` §3.4 (hakem savunması) · §7 (ön-kayıt)
**İlgili:** ADR-0013 (RAFT biçimi · eval-mirror 900-char) · ADR-0011 (6-mod CANON) ·
ADR-0032 (üç aileli panel, aile dışlama) · **ADR-0037/0039 (Kapı 5/6 — taraflılık burada oluşuyordu)**
**Kanıt:** `research_log` [#41](../record/research_log/2026-07-29-cp6-tau-grounding-olcumu.md)
**Açık soru:** [`docs/open_questions.md`](../open_questions.md) **§13.8 → ✅ KAPANDI (seçenek A)**

---

## Bağlam — ölçülen taraflılık

RAFT şablonunun kanonik cevabı üç adımlıdır (`data/train/raft_scrubbed/`, n=17.323; cevapların
**%76'sı** `1)` numaralı çıkarım adımıyla başlıyor — ADR-0035'in biçim sayımı):

```
1) İlgili kaynak KAYNAK 4'tür, çünkü diğerleri başka konuları ele almaktadır.   ← ÇIKARIM
2) ##begin_quote## "…" ##end_quote##                                            ← ALINTI
3) Sonuç olarak, … (TÜRK MEDENİ KANUNU, Madde 271).                             ← SONUÇ + ATIF
```

**1. adım kaynağın *içinden* değil, kaynak *hakkında* bir cümledir.** Groundedness hakemi onu bir
iddia gibi ayrıştırıp `NOT_IN_SOURCE` diyor — ve **teknik olarak haklı**: o bilgi kaynak metninde
gerçekten yok.

**Ölçülen etki (CP6, M1, cevaplanan iddialar):**

| | base | **`τ_g`** |
| :--- | ---: | ---: |
| toplam iddia | 147 | 242 |
| `NOT_IN_SOURCE` | 3 | **31** — bunun **18'i (%58) meta-iddia** |
| hatalı iddia oranı | %2.7 | **%17.4** |
| meta-iddialar düşülürse | %2.7 | **%9.9** |

**Neden karar gerektiriyor:** model bu cümleyi yazmak **zorunda** — eğitim verisinin biçimi bu.
Kafesin **8 eval koşusunun** hepsi bu hakemden geçecek → **`τ_g` içeren her hücre sistematik ceza
alır, `τ_a` tekili almaz.** ADR-0037'nin Kapı 5'i `min`(grounding, abstention) üzerinden çalıştığı
için **iç iddianın kıyası doğrudan taraflanır.**

## Karar — seçenek A

**Groundedness hakem istemine bir kural satırı eklenir:** *kaynak seçimi/eleme hakkındaki
meta-cümleler (ör. "ilgili kaynak KAYNAK 3'tür çünkü diğerleri farklı konuları ele alıyor")
**iddia olarak ayrıştırılmaz ve puanlanmaz.*** Kaynağın içeriği hakkındaki her cümle normal
şekilde puanlanmaya devam eder.

### Uygulama kuralları — üçü de zorunlu

1. **TÜM kollara aynı anda.** `base` · `Gemini 3.1 FL` · `τ_g` · gelecek her kafes hücresi ve
   taban. **Tek kola uygulamak sayıyı doğrudan bizim lehimize kaydırır** ve bu, kuralın kendisinden
   daha büyük bir taraflılık üretir.
2. **Eski skorlar silinmez, kontrol olarak saklanır.** İstem değişikliği başka eksenleri
   (`cit_precision`, iddia sayısı) kaydırıyor mu — ölçülür ve `research_log`'a yazılır. Yığın
   pinlemesi ADR-0029/0032 uyarınca aynı kalır; değişen tek şey istem metnidir.
3. **Meta-iddia düzeltmesi bir *ölçüm* düzeltmesidir, *sonuç* düzeltmesi değil.** Düzeltilmiş
   sayıların yanında **ham** sayılar da yayımlanır. `τ_g`'nin kalan açığı (%9.9 vs base %2.7,
   `CONTRADICTED` 1 → 11) artefakt **değildir** ve maskelenmez.

**Bedel:** ~$0.12 (base + Gemini + `τ_g` yeniden hakem, `gpt-4o-mini`).
**Ne zaman:** `sprint2.md` CP1 — `τ_a` eğitilmeden ve yeni sayı üretilmeden önce.

## Değerlendirilen alternatifler

| eleme | gerekçe |
| :--- | :--- |
| **B — eval-mirror'da cevabın 1. adımını ayıklamak** | Ayıklama regex'i biçim varyasyonunda **sessizce** kırılır. Bu hattın imza hata sınıfı tam olarak bu (`yurutme-tuzaklari.md`: *"hata vermeden yanlış sonuç üreten"*). Ayrıca modelin ürettiği metni ölçüm öncesi kesmek, ölçülen nesneyi değiştirir |
| **C — dokunmamak, artefaktı Limitations'a yazmak** | $0, ama **kafes taraflı ölçülür**: `τ_g` içeren her hücre sistematik ceza alır, `τ_a` tekili almaz → Kapı 5'in kıyası bozulur. İç iddia zarar görür |
| **D — RAFT şablonundan 1. adımı çıkarıp `τ_g`'yi yeniden eğitmek** | Artefaktı kaynağında yok ederdi ve ürün çıktısını da temizlerdi (o cümleyi ne avukat ne vatandaş istiyor). **Ama 1. adım RAFT CoT'unun parçası** — grounding kazancının (coverage %43.8 → %85) ne kadarı ondan geliyor **ölçülmedi**. ~$5.5 + bir gün, ve bütçedeki tek yeniden-eğitim payı. Kanıtsız bir risk için harcanmaz. *(Not: `τ_g` başka bir sebeple yeniden eğitilirse — ADR-0040 madde 3 — bu değişiklik o koşuda yeniden değerlendirilir)* |

## Sonuç — kabul edilen sınır

- Kural, groundedness hakemine **davranışsal bir muafiyet** tanıyor. Muafiyetin sınırı dar tutuldu:
  yalnız *kaynak seçimi/eleme* hakkındaki cümleler. Kaynağın **içeriği** hakkındaki her iddia
  puanlanır. Sınırın doğru çizilip çizilmediği, yeniden hakem koşusunda **elle ~20 örnek
  spot-check** ile doğrulanır.
- ⚠️ Bu kural yalnız **groundedness** hakemini etkiler. Abstention regex'i, atıf doğrulayıcı ve
  register hakemi **değişmez**.
- Düzeltmeden sonra bile `τ_g`'nin hatalı-iddia oranı base'in **3.7 katı** kalıyor. Bu sahipsiz
  negatif ADR-0040 madde 3'te (`τ_g` v2 hipotezi) ve Sprint 4'te (harness iddia doğrulayıcı)
  ele alınır.
