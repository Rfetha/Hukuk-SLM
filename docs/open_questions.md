# Açık sorular — canlı sicil

> **Bu belge ne:** kararlaşmamış ama **kararlaşması gereken** sorular.
> **Kural:** bir soru kapandığında kararı **kalıcı yerine** (ADR ya da `TASARIM.md`'nin ilgili
> bölümü) işlenir ve **buradan çıkarılır.** Bu belge birikmez; nereye gittiği aşağıdaki
> kapanış dizininde durur.
>
> **Otorite:** [`TASARIM.md`](../TASARIM.md) · numaralandırma onun §13'ünden devam eder.
>
> **Pre-registration kuralı:** bir soru veriye bakılarak cevaplanacaksa, **cevap kuralı veriden
> ÖNCE** yazılır (`TASARIM.md` §7).

---

## 🔴 AÇIK

### §13.3 — DEV havuzunun `n`'i yeterli mi? ⏸️ *ölçüm bekliyor*

**Güç analizi yapılmadı.** ADR-0037'nin Kapı 5 eşikleri (%90, `min` bileşik) yazıldı ama
*"DEV'in `n`'i bu farkı ayırt etmeye yetiyor mu"* sorusu cevapsız. Kapı 5 bir **karar kuralıdır,
istatistiksel testin yerini tutmaz** — ADR-0037 bunu limitations'a yazıyor.

⚠️ Analiz için **varyans tahmini** gerekiyor; o da CP6'nın ilk gerçek ölçümünden gelecek.
**Ne zaman:** ⏰ **geçti** — Sprint 3 Part 1 bu soru cevaplanmadan koşuldu. Güç analizi hâlâ yok; elde yalnız hakem gürültü tabanı var (aşağı bak).

⭐ **2026-08-05 — varyansın bir bileşeni artık ÖLÇÜLDÜ ve bu soruyu daraltıyor.**
Aynı üretimin (80/80 cevap, 80/80 bağlam **bit-birebir**) iki kez puanlanması
**A1'de ~0,3 puan**, kütlede ~0,2 puan fark verdi ([#55](record/research_log/2026-08-05-s2-yururluk-alani.md) §9).
Yani `n=80`'de gözlenen farkın **hakemden gelen tabanı** biliniyor; bilinmeyen kısım
**örneklem** varyansı. Bundan sonra bu repoda **0,3 A1 puanının altındaki hiçbir fark
yorumlanmaz** — soru kapanmadı ama artık bir **tabanı** var.

---

### §13.5 — Hakem panelinin üçüncü ailesi hangisi? 🔴

ADR-0032 paneli **OpenAI · Anthropic · Google** olarak belirledi ve aile-dışlama haritasını çizdi.
Kalan iş: **sürüm pinleme + harcama planı**. **Ne zaman:** ⏰ **geçti** — Sprint 3 Part 1 tek hakemle (`gpt-4o-mini`) koşuldu, panel kurulmadı. ⚠️ Bu, o turun bütün yargı-eksenli sayılarına (A1, Rej) **tek aile** damgası vurur; κ raporlanamadı.

---

### §13.6 — İçtihat yapısal grafa girsin mi? 🔴

Eğitim kolu olarak **değil**, yapısal graf düğümü olarak — içtihat→madde atıfı deterministik.
`TASARIM.md` §10.2 zaten *"grafa girmeye aday"* diyor.

**Ön koşullar:** TR IP + hacim/lisans/PII doğrulaması + EDA.
**Not:** `muhamparlak/turkish-law-bge-m3-embeddings` (CC-BY-4.0) **1.82M içtihat gömüsü**
taşıyor — Bedesten'den ham çekip kendimiz gömmeye göre kısayol olabilir. ⚠️ Ama **chunk
uyumsuzluğu** hâlâ geçerli: hazır gömüler 3000 karakterde parçalanmış, bizim protokol 900
(ADR-0011 değişmezi) → değeri *"hazır indeks"* değil, **veri kaynağı**.
**Ne zaman:** erişim/doğruluk işleri bittikten sonra — graf'ın ölçülmüş gerekçesi ve sınırları [`ROADMAP.md` §5.2](../ROADMAP.md)'de.

---

### §13.9 — `τ_g` reçetesi fazla sert miydi? 🔽 **YARISI CEVAPLANDI** — **CP0-b**

> ⭐ **Düşünme hipotezi ÇÜRÜDÜ (2026-07-29, [#42](record/research_log/2026-07-29-cp0-dusunce-modu-sonlanmama.md)).**
> `τ_g` `--thinking on`'da **kendi başına sonlanıyor** (35/36, medyan **452 token**) — üstelik
> **çıplak base sonlanamıyor**. Yani ince-ayar muhakemeyi öldürmedi, **stabilize etti**.
> Reçetenin sertliği bu eksende **kanıtlanmadı**.
>
> 🔴 **Açık kalan yarı:** cevap doğruluğu %2,7 → %17,4 (**sahipsiz negatif**). Ortak sebep
> varsayımı düştüğüne göre bu artık **kendi başına** bir soru — ve bugün numaralı borcu var:
> aşırı-red **B10** ([`sprint3-part1.md`](_arsiv/sprint3-part1.md)). ⚠️ İkisi **birleştirilmedi**:
> aynı kökten geldikleri **makul ama ölçülmemiş**.

CP6 iki hasar bıraktı ve **ikisi de aynı sebepten olabilir**: cevap doğruluğu %2.7 → %17.4
(**sahipsiz negatif** — hiçbir kolun görevi değil) ve *(varsayım)* düşünme yeteneğinin bastırılması.
Ortak şüpheli **reçete**: 1.083 adım · lr 1e-4 · `all-linear` · r=16.

**Ölçüm:** `τ_g` `--thinking on` koşulur, ~20 çıktı gözle incelenir (`sprint2.md` CP0-b, $0).
**Karar kuralı:** bozulmuşsa `τ_g` v2 (yumuşak reçete + `build_replay_tr.py` replay karışımı)
masaya gelir — **ama CP0-a'nın sonucu beklenir**: a YEŞİL ise `τ_g` zaten RS-FT kapsamında
yeniden doğar, ayrı v2 israf olur. Gerekçe: [ADR-0040](adr/0040-dusunce-modu-olculecek-on-kayitli-kural.md) m.3.

---

## 🟡 PLANLANMIŞ İŞ — karar değil, yapılacak

### ~~`causal-conv1d` hız kaldıracı~~ ✅ **KAPANDI 2026-07-30 — kapı KALDI, eklenmedi**

CP0.5 koşuldu (`research_log` [#44](record/research_log/2026-07-30-cp05-cp1-cp2-zemin.md)).
Kaynak okumasıyla teşhis: çekirdekler **bağımsız** ikame ediliyor, pahalı özyineli çekirdek
`fla`'dan geliyor ve **kurulu** (kimlik kontrolü `True`); `causal-conv1d` yokluğunda fallback'e
düşen tek şey depthwise conv. *"Fast path is not available"* uyarısı yalnız bir `warning_once`.

Kazancın **tavanı** ölçüldü (hızlı yol dalına bedeli sıfır saplama): **1.254×** @ batch 2 × 2048,
dört şekilde kararlı (1.196–1.254×). Katman-seviyesi tavan model-seviyesinin **üst sınırı**
olduğu için ölçüm bağlayıcı. **Kapı ≥2.0× → KALDI.** `requirements.lock.txt` korundu,
CP3-CP5 mevcut hızla koşacak. MFU ≈ %15 **framework tavanı** olarak Limitations'a girer.

### ✅ CP2 hasadının kabul ölçütü — **KARARA BAĞLANDI** *(2026-07-30 · ADR-0046)*

CP2 pilotu (`research_log` [#44](record/research_log/2026-07-30-cp05-cp1-cp2-zemin.md)):
ADR-0042'nin ön-kayıtlı kabul ölçütü **regex** (`exact_reject` red saymıyor), ama `τ_a`'nın
raporlanacağı ve ARA KAPI'nın okuyacağı sayı **LLM hakemi**. Ölçüldü (n=120, M2-tipi):

```
regex ölçütü        : 36/120 kabul  (%30)
bunlardan geçersiz tuzak : 15  (%42 — kaynak soruyu gerçekten cevaplıyor)
geçerli tuzakta ABSTAIN  : 15/21  (0.714)  ← havuza YANLIŞ tarafla giriyor
gerçek fabrikasyon       :  6/21  (0.286)  → gerçek verim %5.0
```

Düzeltilmiş verimle hedef **ulaşılamaz**: `1.495 ÷ 0.05 = 29.900 üretim > havuzdaki 19.284 kalem`
(ve ≈92 saat yerel GPU). Üretim hasadı **bilerek başlatılmadı.**

**Kaçışın anatomisi ölçüldü:** 15 kaçağın **10'u morfolojik** (`belirtilmemekle`, `içermediği`,
`tanımlamamaktadır` — Türkçe eklemeli, `REJECT_RE` yüzey biçimlerini tek tek sayıyor),
**5'i leksik işaretsiz** (model kaynağı doğru aktarıp soruyu cevaplamıyor; hiçbir desen yakalayamaz).
→ *"Regex'i genişletelim"* üçte ikisini kurtarır, kalan üçte biri havuza yine yanlış tarafla girer.

> ## ✅ KARARA BAĞLANDI — [ADR-0046](adr/0046-cp2-kabul-olcutu-hakem-ve-havuz-on-elemesi.md) (2026-07-30)
> **1 EVET · 2 EVET · 4 kalem 2'ye devredildi · 3 AÇIK (ölçümden sonra).** Uygulama **başlamadı**;
> sıradaki iş ADR-0046 m.3'ün **uyum kapısı** (`cp2_prefilter.py --against`, ~$0,004).
> Aşağıdaki dört kalem karar öncesinin kaydıdır ve **audit için duruyor.**

**Karara bağlanacak kalemler:**
1. ✅ **EVET** — kabul ölçütü **LLM hakemine** çevrildi (raporlanan metrikle aynı olur; regex ucuz
   ön-filtre kalır; ~$0,4). Anatomisi gereği tek yapısal çözüm.
2. ❌ **Çevrimdışı örtüşme filtresi ELENDİ (ölçüldü):** `ov_gold` eşiği geçersiz oranını
   %42 → %30 indirirken geçerli tuzakların **%24'ünü** kurban ediyor; verime net etkisi
   %5.0 → ~%6.0. `judge_flag` bilgisiz. **Yerine:** geçerlilik `(soru, tuzak madde)`'den
   hakeme sorulabilir — üretimden **önce**, ölçülen birim maliyetle ≈ **$0.94 / 8.000 kalem**,
   verim %5 → **%8.6**. ✅ **EVET — koşulacak** (ADR-0046 m.2), ama önce m.3'ün uyum kapısı.
3. ✅ **KARARA BAĞLANDI — [ADR-0047](adr/0047-cp2-hedef-750-modal-hasat.md): hedef 750 · hasat
   Modal `-np 32` · `τ_a` rejimi ~73 adım / 5 epoch (~$3, ~1,4 sa).** Belirleyici kısıt geçerli
   tuzak sayısı değil **duvar saati** çıktı: yerel hasat tek slotla koşuyordu. ❌ Sentetik
   `rejected` reddedildi (üçüncü bir modelin hataları → Kapı 5 çürür). ⚠️ Koşullu geri alma:
   ön-eleme ≥ ~8.700 geçerli tuzak bırakmazsa hedef otomatik iner.
   *Aşağıdaki tablo kararın dayanağıdır ve audit için duruyor.* Süreler tek ölçülen sabitten
   (**11,12 s/üretim, tek akış**) türer; değişen yalnız verimdir:

   | hedef | filtresiz **%5,0 ölçülen** (3,71 dk/neg) | hakemli ön-elemeli %8,6 *tahmin* (2,16 dk/neg) |
   | --: | --: | --: |
   | 1.495 | **92 sa** | 54 sa |
   | 750 | 46 sa | 27 sa |
   | 500 | 31 sa | 18 sa |
   | 400 | 25 sa | 14 sa |

   ⚠️ Bu tablonun önceki sürümü (77/26/21 sa) **elenmiş** çevrimdışı filtrenin verimiyle
   (%6,0 → 3,09 dk/neg) hesaplanmıştı; premis düşünce tablo da düştü. m2b tipi biraz daha yavaş
   (11,69 s/üretim) ve verimi **ölçülmedi** — karışım oranı süreyi yukarı çeker.

   **Ve tablonun tamamı TEK AKIŞ sayısıdır.** `llama-server` `-np` bayrağı olmadan tek slotla
   koşuyordu; 11,12 s bir **gecikme** sayısı, verim sayısı değil. Modal `-np 32` ile 750 hedef
   ≈ **1,4 sa** (ADR-0047). Yerel `-np 8` ölçülmedi — Modal tıkanırsa geri dönülecek seçenek.
4. ✅ **Kalem 2'ye devredildi** — `abstain_trap_v3` dilimi %42 geçersiz taşıyor, ama `chosen`
   denetimi **ayrı bir iş değil**: ön-eleme dilimin tamamını etiketliyor, geçersiz tuzağın
   **çifti düşüyor**. `chosen` metni zaten diskte (`orpo_chosen.jsonl`) → yeniden üretim yok,
   havuz **baştan kurulmaz, süzülür** (tek-havuz kuralı korunur).

Yeni tuzaklar kayda geçti: `yurutme-tuzaklari.md` **4.7** (kabul ölçütü ≠ raporlanan metrik) ·
**4.8** (tuzak havuzunun kendisi geçersiz).

### Korpus temizliği — ⭐ **kısmen KAPANDI 2026-08-05 (S2), gerisi borç B9**

Ölçüm ve gerekçe artık [`TASARIM.md` §5.3](../TASARIM.md)'te. Özet: **1.901 saf kabuk (%4.7)** +
3.101 tadil-kanunu maddesi. **Eğitim ve eval temiz** (sızıntı ölçüldü: %0.06 / sıfır) →
**yeniden eğitim gerektirmez**; risk yalnız retriever indeksinde.

✅ **Yapıldı** ([#55](record/research_log/2026-08-05-s2-yururluk-alani.md)): `mulga` + ilga alanı
**2.547 satır**, alt-madde kimliği **485 satır**, doğrulayıcıya `MULGA` hükmü → **B7 kapandı**.

⭐ **Ve kapsam kararı bir menüden değil ÖLÇÜMDEN çıktı.** Sorulacak doğru soru *"korpus ne kadar
bozuk"* değil **"modelin GÖRDÜĞÜ bağlamda çöp var mı"** idi. `context_shown` ayrıştırılınca:
tablo/cetvel parçaları (**~7.966 satır**) modele **0/800 blok** ulaşıyor — parçalar `", Ek"`
kadar kısa, ne BM25 ne vektör üste çıkarıyor. **Elenmedi, ertelendi (borç B9):** elemek
*ölçülemez bir kazanç için ölçülmüş bir sayıyı harcamak* olurdu (indeks değişir → `recall@k`
kayar → `k` kıyası geçersizleşir).

⚠️ **Yinelenme ≠ kirlenme.** Aynı korpus için *"anahtar yinelenmesi %29,4"* ve *"bağlam
kirlenmesi %1,8"* **ikisi de doğru** — farklı nesneleri ölçüyorlar. Retriever yinelenen
anahtarın **doğru** satırını getiriyordu.

### ~~Modül-başına normalleştirme~~ — ✅ **KAPANDI 2026-08-04, REDDEDİLDİ**

[ADR-0053](adr/0053-modul-basina-norm-kapsami-reddedildi.md) · [research_log #50](record/research_log/2026-08-04-modul-basina-norm.md)

Ölçüldü, iki kere düştü:

1. **Gerekçesi çürüdü.** *"Çatışma rastgele dağılmıyor"* doğru ama **kapsam sorunu
   kanıtlamıyor** — kolların modül profilleri neredeyse **orantılı** (τ_g/τ_a oranı 11
   yüzeyin hepsinde 7,18-10,08), dolayısıyla global norm payları **zaten eşitliyor**
   (τ̂_a/τ̂_g = 0,88-1,24). Ayırt eden sütun **oran**dı ve o ölçülmemişti.
2. **Ölçüm de geçmedi.** Kapsam değişikliği no-op değil (ağırlık uzayında yön farkı
   **%27,2**, genlik aynı) ama kabul ölçütü düştü: cevaplanan **45/80** → kütle
   ≤ **%56,2** < gereken %71,6. Hakem maliyeti **$0** (bileşik ölçütte önce regexle
   ölçülen kütle ayağı koşuldu).

⚠️ **Yerine geçen açık soru:** `τ_a`'nın merge'de seyrelmesi (M2b 0,987 → 0,877) **hâlâ
açık**. Bu tur onu norm *kapsamının* çözmediğini gösterdi; aşırı-reddi yaratan **yön değil
genlik**. Kalan adaylar: `--trim-k` · λ · farklı operatör · ve en olası doğru yer —
**`τ_a`'nın eğitim genliği** (82 adım @1e-5 çok kısa, ‖τ_a‖ = 1,18 bu yüzden küçük).
Yani çözüm bir **merge** parametresi değil, muhtemelen bir **eğitim** parametresi.

### Merge doğrulama birim testi — Sprint 3 öncesi

ADR-0036'daki 5 parametreli örnek birim testine çevrilecek (ham TIES → p1 = 0.80 · norm-dengeli →
p1 = 0.739, p3 = 0.547). **Zorunlu şart**, `TASARIM.md` §4.2'de kayıtlı.

⚠️ **Test hâlâ gerekli, rolleri değişti** ([ADR-0052](adr/0052-merge-norm-dengeleme-hukmu-tersine.md)):
artık **ham TIES ana yol**, norm-dengeli ablasyon. Test ikisini de doğrulamalı — hangisinin
"ana" olduğu testin kapsamını değiştirmiyor, yalnız hangi sayının manşete gireceğini.

---

## ✅ KAPANIŞ DİZİNİ — hangi karar nereye gitti

> Kararların kendisi burada **tekrarlanmaz**; kalıcı yerlerinde durur.

| soru | karar | kalıcı yer |
| :--- | :--- | :--- |
| **§13.10** RS-FT / düşünce modu | 🟡 **SARI — CP0-a koşuldu, RS-FT kapsama GİRMEDİ.** Ön-kayıtlı kural aynen uygulandı: M2 eşiği filtresiz de geçiliyor (0,786 ≥ 0,78) ama muhafız düştü → ADR-0035 **açılmadı**, ADR-0030 m.2 **geri alınmadı**. ⚠️ Ön okuma *"yanlış gerekçeyle doğru çıktı"* — 🟡 tahmin edilmişti ama **M2 bacağının** düşeceği beklenmiyordu; bu da kayda geçti. ⭐ Yan bulgu, kalıcı rejim değişikliği doğurdu: base `--thinking on`'da **hiç sonlanmıyor** → **bütçeli zorla kapatma** (1024+512) artık seed ve clip ile aynı statüde bir **değişmez** | [ADR-0040](adr/0040-dusunce-modu-olculecek-on-kayitli-kural.md) · [ADR-0043](adr/0043-dusunce-modu-acik-butceli-kapatma.md) · [#42](record/research_log/2026-07-29-cp0-dusunce-modu-sonlanmama.md) · [#43](record/research_log/2026-07-29-cp09-butceli-dusunce-cipalari.md) |
| **§13.1** TR gömme modeli | ✅ **ÖLÇÜMLE SEÇİLDİ 2026-08-04** — `BAAI/bge-m3` **+ BM25**, RRF hibriti. Tek başına hiçbiri değil: `recall@10` BM25 **0,625** · e5-base **0,700** · bge-m3 **0,800** · **hibrit 0,875**. ⚠️ Hazır gömü seti **kullanılmadı** (chunk uyumsuzluğu); model alınıp korpus kendi 900-karakter protokolümüzle gömüldü | [ADR-0054](adr/0054-harness-tasarim-kararlari-k2-k5.md) K1 · [#49](record/research_log/2026-08-04-s3a-on-prob.md) · `scripts/retriever.py` |
| **#8** tekil hücreler | aynı hat + `τg` düz kontrol → **4 hücre** | [ADR-0036](adr/0036-tau-norm-asimetrisi-ve-norm-dengeli-merge.md) Ek · `TASARIM.md` §4.3 |
| **#9** iç iddianın karar kuralı | **Kapı 5** — `min` bileşik, simetrik %90, iki tabanı da geç | [ADR-0037](adr/0037-ic-iddia-karar-kurali-kapi-5.md) · `TASARIM.md` §7 |
| **#10** merge kütüphanesi | **kendi kodumuz** + zorunlu birim testi + `mergekit` çapraz kontrol 🔄 | `TASARIM.md` §4.2 |
| **#11** `τ_reasoning` / RS-FT | **kapsam dışı** — biçim zaten `τ_g`'de (%76), zincirleme harness'ın işi. ⚠️ **§13.10 ile şartlı yeniden açıldı** (CP0-a YEŞİL çıkarsa) | [ADR-0035](adr/0035-tau-reasoning-rs-ft-kapsam-disi.md) · [ADR-0040](adr/0040-dusunce-modu-olculecek-on-kayitli-kural.md) · `TASARIM.md` §2 (satır 13), §10.2 |
| **#12** ΔW norm asimetrisi | ⚠️ **HÜKÜM TERSİNE (2026-08-03)** — **ham TIES ana**, norm-dengeli ablasyon. Asimetri **ölçüldü** (8,87×: ‖τ_g‖ 10,47 ↔ ‖τ_a‖ 1,18) ve `‖τ‖` koşulsuz ölçülmeye devam eder; çürütülen şey *"dengelenmezse küçük kol silinir"* çıkarımı — ham TIES'te `τ_a` silinmedi (M2b 0,607→0,877), tersine dengeleme `τ_g`'yi ezdi (grounding 71,4%→53,4%) | [**ADR-0052**](adr/0052-merge-norm-dengeleme-hukmu-tersine.md) ADR-0036'yı tadil eder · [#48 §24](record/research_log/2026-08-02-cp2c-modal-koprusu.md) |
| **#13** rejim eşleşmesi | precision/dropout/modül/uzunluk **eşleşti** · lr/batch **serbest** + tetik · ORPO **epochs 3** | `TASARIM.md` **§4.1.1** |
| **§13.2** red kapısı eşiği | **katı** — tek doğrulanamayan atıf tüm cevabı reddettirir | [ADR-0038](adr/0038-red-kapisi-esigi-kati.md) |
| **§13.4** zamansal eksen | **kapsam dışı** — sebep tercih değil, korpusta metadata yok | `TASARIM.md` §10.2 · ön koşul §5.3 |
| **§13.7** yinelemeli merge | **konusuz kaldı** — `k=2`'de ayrım tanımsız | `TASARIM.md` §4.2 |
| **§13.8** RAFT meta-iddiaları | **A** — hakem istemine muafiyet satırı, **TÜM kollara aynı anda**, ham sayılar da yayımlanır | [ADR-0041](adr/0041-raft-meta-iddia-hakem-kurali.md) · `sprint2.md` CP1 |
| — M5 anti-hedefi Kapı 5'i kilitliyor | **(d) ayrıldı → Kapı 6**; çıpa **base** (rakip değil), coverage + ezber kütlesi, orijinal (d)'ye karşı da rapor | [ADR-0039](adr/0039-kapi-6-parametrik-sizinti.md) · `TASARIM.md` §7 |
| — `rejected` havuzu hangi modelden | **tek havuz ham base'den** (veri sabit) + **FT-6 on-policy kontrol koşusu** (~$0.65) | [ADR-0042](adr/0042-rejected-havuzu-tek-kaynak-ve-on-policy-kontrol.md) · `sprint2.md` CP2/CP5 |
| — rakip yöntemler Sprint 2'de mi | **önce `τ_a`, ARA KAPI'da dur, sonra tabanlar** — `τ_a` tutmazsa ~$12 harcanmaz | `sprint2.md` CP3 |
| kod borcu — ORPO rejim sapması | `--bf16-base` + `--lora-dropout` eklendi | `scripts/train_orpo.py` · `modal_train.py` · `TASARIM.md` §4.1.1 |
| kod borcu — `--target-modules` | **zorunlu**, varsayılan silindi (bedel ölçüldü: `‖τ‖`'nin %26.8'i) | her iki eğitim script'i · `TASARIM.md` §4.1.1 |
| gözlem — sıfır marjinal maliyet | ek çıkarım bizde ucuz/rakipte pahalı · `N*` etkilenmiyor | `TASARIM.md` §6.4 |

---

## Başka yerde duran açık kalemler — burada tekrarlanmaz

| ne | nerede |
| :--- | :--- |
| ~~`τ_abstention` Sprint 1'e çekilsin mi~~ | ✅ **konusuz** — Sprint 1 kapandı (2026-07-29), `τ_a` Sprint 2'ye kaldı |
| Sağlayıcı pinlemesi · rakip üretim maliyeti (Sprint 5 ön koşulu) | [`sprint1-sonuc-tablosu.md`](record/sprint1/sprint1-sonuc-tablosu.md) §Geçerlilik şerhleri |
| Rakip aileleri için red-regex kalibrasyonu | [`yurutme-tuzaklari.md`](record/yurutme-tuzaklari.md) §2.2 |
| CP2 tablosundaki 4 sayı uyuşmazlığı (işaretlendi, düzeltilmedi) | [`sprint1.md`](_arsiv/sprint1.md) CP2 · [#41 §6](record/research_log/2026-07-29-cp6-tau-grounding-olcumu.md) |
| H100 hız kaldıracı | [ADR-0033](adr/0033-egitim-hizi-fla-core-checkpointing-batch.md) |
| Devir paketinin yedeksiz tek nüsha olması | [ADR-0034](adr/0034-emekli-hat-artefaktlarinin-repodan-cikarilmasi.md) |
| Doğrulayıcı kalibrasyonu (yanlış-negatif → coverage kaybı) | [ADR-0038](adr/0038-red-kapisi-esigi-kati.md) |
