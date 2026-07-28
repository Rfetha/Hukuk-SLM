# Açık sorular — canlı sicil

> **Bu belge ne:** kararlaşmamış ama **kararlaşması gereken** sorular, her biri gerekçesi ve
> seçenekleriyle. Konuşa konuşa netleşecekler; netleşen soru buradan **silinmez**, cevabı ve ADR
> numarası yazılıp `✅ KAPANDI` işaretlenir — hangi soruyu ne zaman neye göre cevapladığımız
> makale malzemesi.
>
> **Otorite:** [`TASARIM.md`](../TASARIM.md) · **numaralandırma** onun §13'ünden devam eder
> (1-7 orada, 8'den itibarısı burada). §13 donmuş kayıt, **canlı liste burası.**
>
> **Kural:** bir soru veriye bakılarak cevaplanacaksa, **cevap kuralı veriden ÖNCE** yazılır.
> Sonra yazılan kural rasyonalizasyondur (pre-registration mantığı, `TASARIM.md` §7).

---

## 8. Tekil kafes hücreleri de TIES hattından geçecek mi? 🔴

**Soru.** Kafesin tekil hücreleri (`τg tek`, `τa tek`) nasıl üretilecek — **düz adaptör**
(`λ=1`, budama yok) mı, yoksa çoklu hücrelerle **aynı merge hattından** geçmiş mi?

**Neden önemli.** Tek vektörde TIES'ın ② işaret-seçimi ve ③ ayrık-ortalama adımları anlamsız
(seçilecek çatışma yok); geriye yalnız ① budama + `λ` ölçeği kalıyor. Yani iki seçenek **farklı
sayı üretir.** Ve tekiller kafeste bir süs değil, **atıf aracı**: `τg+τa` düşük çıkarsa sebebin
"merge çatışması" mı yoksa "kol zaten öğrenememiş" mi olduğunu ancak tekile bakarak ayırıyoruz
(`TASARIM.md` §4.3). Tekil farklı bir hattan geçerse aradaki fark **üçüncü bir şeyi** de içerir:
budamanın kendi hasarını.

| seçenek | sonuç |
| :--- | :--- |
| **A — aynı hat** (tekil de budanır + `λ` uygulanır) | Fark yalnız *çatışmadan* gelir; atıf temiz. Ama "kolun tek başına ne öğrendiği" budanmış hâliyle ölçülür |
| **B — düz adaptör** (`λ=1`, budamasız) | Kolun ham yeteneği görünür. Ama `τg` → `τg+τa` düşüşü *çatışma + budama* karışımı olur, ayrıştırılamaz |
| **C — ikisi de** (ekstra hücre) | Budamanın hasarını **ayrı ölçer**; maliyeti yalnız eval (merge bedava) |

**İlk eğilim:** A — atfedilebilirlik en pahalı şeyimiz. C teknik olarak en bilgilendirici ve
maliyeti düşük; ciddiye alınmalı.
**Ne zaman:** Sprint 3'ten önce. **Bağlı:** `TASARIM.md` §4.3.

---

## 9. "Merge tabanlardan iyi" ne demek — sayıyla? 🔴

**Soru.** İç iddianın karar kuralı ne? Hangi metrikte, ne kadar fark, hangi yönde?

**Neden önemli.** DEV'de `λ` · density · drop-rate taradıktan **sonra** kural yazmak,
sonucu rasyonalize etmektir. Proje pre-registration'ı zaten uyguluyor (`TASARIM.md` §7:
*"eşikler sonradan yazılırsa çıkan sonuç rasyonalize edilir"*) — ama **iç iddianın kendisi için
kural yazılmamış.** Kapı 0-3 var, "merge kazandı mı" kapısı yok.

Zorluk şu: iddia **tek metrik değil, çatışma**. `τg+τa`, grounding'i (M1/M4) *ve* abstention'ı
(M2/M2b) **aynı anda** korumalı. Tek bir skora indirgemek çatışmayı gizler; iki metriği ayrı
raporlamak da "kazandı mı" sorusunu cevapsız bırakır.

**Taslak öneri** (rakam yok, şekil var):

```
τg+τa  ŞUNLARIN HEPSİNİ sağlamalı:
  (a) M1/M4 ≥ X% · (τg tek)'in değeri        ← grounding korundu
  (b) M2/M2b ≥ Y% · (τa tek)'in değeri       ← abstention korundu
  (c) bileşik ölçütte Taban A ve Taban B'nin İKİSİNİ de geçmeli
  (d) M5 (anti-hedef) base'in üstüne çıkmamalı
```

**Cevaplanmamışlar:** X ve Y kaç · "bileşik ölçüt" nasıl tanımlanır (min? harmonik ortalama?) ·
DEV'deki `n` bu farkı görmeye yetiyor mu (§13 soru 3 ile bağlı — güç analizi yok) ·
tarama sonrası **hangi hücre** raporlanır (en iyi λ mi, önceden sabitlenmiş λ mi — çoklu
karşılaştırma sorunu).

**Ne zaman:** Sprint 3 taramasından **önce**, veriye bakmadan. **Bağlı:** `TASARIM.md` §4.4, §7.

---

## 10. Merge kütüphanesi — hazır mı, kendi mi? 🟡

**Soru.** `mergekit` mi, ~200 satırlık kendi streaming merge'imiz mi?

| seçenek | artı | eksi |
| :--- | :--- | :--- |
| **`mergekit`** | `ties` · `dare_ties` · `task_arithmetic` hazır ve test edilmiş · out-of-core/lazy yükleme var · tarama YAML ile ucuz | yeni bağımsızlık zinciri (pinlenebilir ama pinli `requirements.lock.txt`'e dokunur) · içeride ne olduğu bizim değil |
| **kendi** | `TASARIM.md` §4.2 zaten tarif ediyor (host RAM, tensör tensör, bf16 ΔW, kuantizasyon en son) · tam kontrol · makalede birebir yazılabilir | TIES'ı yanlış uygulamak **sessiz** bir hata sınıfı — işaret-seçimini yanlış yazarsan sayı çıkar ama yanlış çıkar |

**Not.** Hangisi seçilirse seçilsin, **doğrulama testi şart**: bilinen küçük bir örnekte
TIES'ın üç adımı elle hesaplanıp kodun çıktısıyla karşılaştırılmalı. Bu hattın sessiz-bozulma
sicili (`#38` şablon tuzağı, `#40` `fla-core`) bunu tavsiye değil zorunluluk yapıyor.

**Ne zaman:** Sprint 3 uygulamasından önce. **Bağlı:** `TASARIM.md` §4.2.

---

## 11. `τ_reasoning` / RS-FT tez kapsamına giriyor mu? 🔴

**Soru.** `docs/ft-is-akisi.mmd`'de taslak olarak duran **rejection-sampling FT** kolu — üçüncü
task-vector olarak tez kapsamına girecek mi?

**Neden önemli — bu sorunun bedeli en büyük:**

- **Kapsam:** kol 2 → 3, kafes 3 → 7 hücre, eğitim koşusu 5'ten yukarı, araya **FAZ 0 kapıları**
  giriyor (M6 seti üretimi + deterministik zincir-verifier + `pass@16` tanısı + **Kapı R**).
- **Bir ADR'yi geri alıyor:** RS-FT düşünce izi üretmeyi gerektiriyor, ama **ADR-0030 madde 2**
  düşünce modunu KAPALI kilitledi — gerekçe kolaylık değildi: varsayılan modda model `</think>`'i
  kapatmıyor, `content` **boş** dönüyor (HTTP 200, sıfır hata), ve SFT verisi akıl yürütme izi
  taşımıyor (eğitim-eval hizalaması). Geri alınacaksa **ADR-0035** gerekir ve o iki sorunun
  ikisine de cevap vermelidir.
- **Kapı R zaten yazılmış:** `pass@16 = 0` çıkarsa yol **kapanıyor** — RS-FT'nin süzeceği doğru iz
  yok demektir. Yani bu soru kısmen ölçümle cevaplanacak, ama **ölçümü yapmaya değer mi** kararı
  bizde.

**Ne zaman:** Sprint 2 planlanmadan önce — Sprint 2'nin kapsamını doğrudan belirliyor.
**Bağlı:** `docs/ft-is-akisi.mmd`, `docs/model-soyagaci.mmd` (🟡 işaretli), ADR-0030 madde 2.

---

## 12. Kol vektörlerinin ÖLÇEĞİ nasıl eşitlenecek? (ΔW norm asimetrisi) 🔴

**Soru.** `τ_grounding` **17.323** satırda, `τ_abstention` **1.741** çiftte eğitiliyor — 10× fark.
`τ_g`'nin deltası büyük olasılıkla belirgin şekilde **daha büyük normlu** çıkacak. Merge'de bu
farkı düzeltecek miyiz, nasıl?

**Neden kritik — TIES'ın üç adımına ne yaptığı:**

| adım | norma duyarlı mı |
| :--- | :--- |
| ① budama (her vektörde kendi içinde top-k%) | ✅ duyarsız |
| ② işaret seçimi `γ = sgn(Σ τ̂)` | ❌ **kütle ağırlıklı → büyük normlu kol kazanır** |
| ③ ayrık ortalama (ham değerler toplanır) | ❌ **büyük normlu kol baskın** |

Hiçbir şey yapmazsak merge **otomatik olarak grounding lehine kayar** ve `τ_abstention` sistematik
olarak eziliyor görünür — ama sebep *çatışma* değil, *ölçek.* Bu doğrudan iç iddiayı vurur: jüri
haklı olarak *"abstention merge'de kayboldu mu, yoksa vektörünüz mü küçüktü?"* diye sorar.

| seçenek | not |
| :--- | :--- |
| **A — kol başına ağırlık `w_t`** (`mergekit`'in `weight` parametresi) | DEV'de taranabilir; ama `w_t` de bir serbestlik derecesi, #9'un karar kuralına dahil edilmeli |
| **B — norm normalizasyonu** `τ_t / ‖τ_t‖` | mekanik, tarama gerektirmez; kolun *büyüklük* bilgisini atar (bilgi mi, gürültü mü — bilinmiyor) |
| **C — hiçbiri, ham TIES** | savunulabilir tek koşul: asimetrinin ölçülüp **raporlandığı** durum |

⚠️ **Ön adım, ucuz ve şart:** her kolun `‖τ‖` değeri eğitim biter bitmez **ölçülüp kaydedilecek.**
Fark küçükse bu sorunun tamamı düşer; büyükse hangi seçenek olursa olsun rapora girer.

**Ne zaman:** Sprint 3 öncesi. **Bağlı:** #8, #9, `TASARIM.md` §4.2.

---

## 13. Kollar arası eğitim rejiminde ne eşleşmek ZORUNDA, ne serbest? 🔴

**Soru.** İki kol bugün farklı ayarlarda koşuyor. Hangileri task-vector geçerliliği için
**eşleşmek zorunda**, hangileri yöntemin doğası gereği **serbest**?

| | `τ_grounding` (SFT) | `τ_abstention` (ORPO) | değerlendirme |
| :--- | ---: | ---: | :--- |
| precision | **bf16 taban** (ADR-0031) | ~~QLoRA NF4 sabit~~ → ✅ `--bf16-base` | 🔴 **ZORUNLU eşleşme** — farklı `θ_base` = task-vector tanımı bozulur · *düzeltildi* |
| `lora_dropout` | 0.05 (ADR-0033 `0`'ı reddetti) | ~~0.0 sabit~~ → ✅ `--lora-dropout` 0.05 | 🔴 **ZORUNLU** — atfedilebilirlik · *düzeltildi* |
| `target_modules` | varsayılanda `in_proj_*` **YOK** (elle veriliyor) | varsayılanda `in_proj_*` **YOK** | 🔴 **ZORUNLU** — ama sorun **paylaşılan**, ORPO'ya özgü değil; bkz. Kod borçları |
| `lora_r` / `alpha` | 16 / 32 | 16 / 32 | ✅ eşleşiyor |
| seed | 3407 | 3407 | ✅ eşleşiyor |
| lr | 1e-4 | 1e-5 | 🟡 **serbest?** — ORPO'nun kendi rejimi |
| etkin batch | 16 | 64 | 🟡 **serbest?** — reçete: OR-sinyali ≥64 ister |
| `max_seq_len` | 2048 | 1536 / prompt 1152 | 🟡 karar verilmedi |

İlk ikisi düzeltildi (aşağıda), üçüncüsü açık. Son üçü **gerçek soru**: lr/batch farkı meşru mu,
yoksa "iki kol farklı yörüngeden geldi" diye limitations'a mı yazılmalı?

⚠️ **Ayrıca ölçülmemiş bir varsayım:** ORPO bu hatta **hiç ham base'den koşmadı** — 12B'de
continuation'dı (`--adapter`, v2b üstüne). Teorik olarak doğru (ORPO'nun kaybı `L_SFT` terimi
içerir, referans model istemez — DPO'dan farkı bu) ve veri **%20 grounding replay** taşıyor,
ama bu hatta **ölçülmedi.** `τa` tekil hücresi tam olarak bunu ölçecek.

**Ne zaman:** Sprint 2 başlamadan. **Bağlı:** ADR-0031, ADR-0033, `TASARIM.md` §4.1.

---

## Kod borçları

### ✅ KAPANDI (2026-07-28) — `train_orpo.py` rejim sapması

`scripts/train_orpo.py` 12B dönemi ayarlarında kalmıştı ve `train_sft.py`'den **sessizce**
ayrışıyordu — hata vermez, sayı üretir, sayı kıyaslanamaz olurdu:

| ne | eskiden | şimdi |
| :--- | :--- | :--- |
| precision | `load_in_4bit=True` **sabit kodlu** (QLoRA NF4) | `--bf16-base` bayrağı, ADR-0031 birincil yolu |
| `lora_dropout` | `0.0` **sabit kodlu** | `--lora-dropout`, varsayılan **0.05** (ADR-0033) |

Bayraklar `modal_train.py`'ın `train_orpo` + `spawn_orpo` yollarından da geçiriliyor
(`bf16_base` · `lora_dropout` · `target_modules`), yoksa Modal'dan kullanılamazlardı.

### 🔴 AÇIK — `--target-modules` varsayılanı İKİ script'te de eksik

Düzeltme sırasında çıktı: **`train_sft.py` ve `train_orpo.py` aynı varsayılanı taşıyor** —
`q/k/v/o + gate/up/down`, yani **`in_proj_qkv/z/a/b` YOK.** Bu ORPO'ya özgü bir sapma değil,
**paylaşılan bir mayın**: Qwen3.5'te 24 linear-attention katmanı LoRA'sız kalır, hata vermeden.

Bugün tek koruma, listeyi **her çağrıda elle vermek** (CP5 komutu öyle yapıyor,
`NEXT-SESSION.md` §3 "asla düşürme" diye uyarıyor). Bu koruma değil, disiplin.

**Seçenekler:** (a) varsayılanı sil, `--target-modules` **zorunlu** yap → tanımsız base erken
patlar, ADR-0026'nın ruhu · (b) base'e göre liste tut → ADR-0026'ya aykırı (script base bilmemeli) ·
(c) olduğu gibi bırak + uyarı bas.
**Eğilim: (a).** ⚠️ `train_sft.py`'ye dokunmak CP5 koşarken **yapılmadı** — koşu bitince.

### ⚠️ Kalıcı uyarı — `--adapter` yolu

`train_orpo`'nun **`--adapter` (continuation) yolu Sprint 2'de KULLANILMAZ**; `--fresh-adapter`
zorunlu. `--adapter tg` yazmak ardışık SFT üretir, yani **Taban B**'yi kol diye kaydeder.
Kod bunu engellemiyor, sadece uyarı basıyor. `spawn_orpo` docstring'ine yazıldı.

**Bağlı:** #13.

---

## Başka yerde duran açık kalemler — burada tekrarlanmaz

| ne | nerede |
| :--- | :--- |
| 7 tasarım sorusu (embedder · red eşiği · DEV n · zamansal eksen · hakem 3. aile · içtihat grafı · yinelemeli merge) | [`TASARIM.md`](../TASARIM.md) §13 |
| `τ_abstention` Sprint 1'e çekilsin mi | [`sprint1.md`](../sprint1.md) §Sprint 1 dışında kalanlar |
| Sağlayıcı pinlemesi · rakip üretim maliyeti · CP2 M2 regex uyuşmazlığı | [`docs/record/sprint1/NEXT-SESSION.md`](record/sprint1/NEXT-SESSION.md) §8 |
| `causal-conv1d` + H100 hız kaldıraçları | [ADR-0033](adr/0033-egitim-hizi-fla-core-checkpointing-batch.md) |
| Devir paketinin yedeksiz tek nüsha olması | [ADR-0034](adr/0034-emekli-hat-artefaktlarinin-repodan-cikarilmasi.md) |
