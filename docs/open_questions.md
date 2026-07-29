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

### §13.1 — TR embedding modeli hangisi olacak? ⏸️ *ölçüm bekliyor*

Lisansı temiz, Türkçe hukuk metninde iyi çalışan bir gömü modeli lazım. **EDA-doğrulama kuralı
burada da geçerli** — model denenmeden seçilemez. **Ne zaman:** Sprint 4.

**Birinci aday: `BAAI/bge-m3`** *(kullanıcı işaret etti, 2026-07-28)*
Kaynak: [`muhamparlak/turkish-law-bge-m3-embeddings`](https://huggingface.co/datasets/muhamparlak/turkish-law-bge-m3-embeddings)
— ⚠️ bu bir **veri seti**, model değil: Türkçe hukuk metinlerinin `bge-m3` ile önceden hesaplanmış
gömüleri.

| künye (sayfadan) | değer |
| :--- | :--- |
| model | `BAAI/bge-m3`, çok dilli · **1024-dim** |
| satır | **1.824.298** — 1.82M **içtihat** parçası + 4.69k **mevzuat** maddesi |
| kaynak | Yargıtay + Danıştay · Anayasa, TMK, TCK ve diğer temel kanunlar |
| chunk | içtihat **3000 char**, mevzuat chunk'sız |
| lisans | **CC-BY-4.0** (atıf şartlı, temiz) |

**⚠️ Üç uyarı, hiçbiri doğrulanmadı:**
1. **Chunk uyumsuzluğu.** Hazır gömüler **3000 char**'da parçalanmış; bizim protokol **900 char
   eval-mirror** (ADR-0011 değişmezi). Gömüler **olduğu gibi kullanılamaz** — model alınıp korpus
   kendi clip'imizle yeniden gömülmeli. Değeri "hazır index" değil, **"model adayı"**.
2. **Boyut bütçeyi değiştirir.** Önceki tahmin e5-base sınıfıydı (278M, 768-dim); `bge-m3` ~568M
   ve 1024-dim → embedder RAM ~1.1 GB değil **~2.3 GB** (fp32), index 88 MB değil ~**236 MB**.
   ≤8 GB tablosunun **CPU tarafı** yeniden kurulmalı (VRAM etkilenmez — embedder CPU'da).
3. **EDA şart.** `newmindai/EuroHPC-Legal` de kâğıt üstünde kusursuzdu.

---

### §13.3 — DEV havuzunun `n`'i yeterli mi? ⏸️ *ölçüm bekliyor*

**Güç analizi yapılmadı.** ADR-0037'nin Kapı 5 eşikleri (%90, `min` bileşik) yazıldı ama
*"DEV'in `n`'i bu farkı ayırt etmeye yetiyor mu"* sorusu cevapsız. Kapı 5 bir **karar kuralıdır,
istatistiksel testin yerini tutmaz** — ADR-0037 bunu limitations'a yazıyor.

⚠️ Analiz için **varyans tahmini** gerekiyor; o da CP6'nın ilk gerçek ölçümünden gelecek.
**Ne zaman:** CP6 sonrası, Sprint 3 öncesi.

---

### §13.5 — Hakem panelinin üçüncü ailesi hangisi? 🔴

ADR-0032 paneli **OpenAI · Anthropic · Google** olarak belirledi ve aile-dışlama haritasını çizdi.
Kalan iş: **sürüm pinleme + harcama planı**. **Ne zaman:** Sprint 3.

---

### §13.6 — İçtihat yapısal grafa girsin mi? 🔴

Eğitim kolu olarak **değil**, yapısal graf düğümü olarak — içtihat→madde atıfı deterministik.
`TASARIM.md` §10.2 zaten *"grafa girmeye aday"* diyor.

**Ön koşullar:** TR IP + hacim/lisans/PII doğrulaması + EDA.
**Not:** §13.1'deki `bge-m3` veri seti **1.82M içtihat gömüsü** taşıyor — Bedesten'den ham çekip
kendimiz gömmeye göre kısayol olabilir, ama aynı üç uyarı geçerli.
**Ne zaman:** Sprint 4.

---

### §13.8 — RAFT meta-iddiaları groundedness hakeminde nasıl ele alınacak? 🔴 ⏰ **`τ_a`'DAN ÖNCE**

**Ölçülen sorun (#41, CP6).** RAFT şablonunun 1. adımı — *"İlgili kaynak KAYNAK 3'tür çünkü diğer
kaynaklar farklı konuları ele almaktadır"* — kaynak **hakkında** bir cümle, kaynaktan değil. Hakem
haklı olarak `NOT_IN_SOURCE` diyor. M1'de `τ_g`'nin 31 `NOT_IN_SOURCE` iddiasının **18'i (%58)**
bu şekilde; hatalı-iddia oranı **%17.4 → %9.9**'a iniyor bunlar düşülünce.

**Neden karar gerektiriyor:** model bu cümleyi yazmak **zorunda** (eğitim verisinin %77'si bu biçim,
ADR-0013). Kafesin **8 eval koşusunun** hepsi bu hakemden geçecek → **`τ_g` içeren her hücre
sistematik ceza alır, `τ_a` tekili almaz.** ADR-0037'nin Kapı 5 kuralı `min`(grounding, abstention)
üzerinden çalıştığı için **iç iddianın kıyası doğrudan taraflanır.**

**Seçenekler:**

| # | ne | bedel | risk |
| :-- | :--- | :--- | :--- |
| A | Hakem istemine *"kaynak seçimi hakkındaki meta-cümleleri iddia sayma"* satırı | ~$0.12 (base+gem+tg yeniden hakem) | istem değişikliği başka etkiler doğurabilir |
| B | Eval-mirror'da cevabın 1. adımını hakeme göndermeden ayıkla | kod + yeniden hakem | ayıklama regex'i biçim varyasyonunda kırılır |
| C | Dokunma, artefaktı Limitations'a yaz | $0 | **kafes taraflı ölçülür** — iç iddia zarar görür |

**Pre-registration kuralı (TASARIM §7):** karar **veriye bakılarak** verilecekse cevap kuralı önce
yazılır. Hangi seçenek seçilirse seçilsin **base + Gemini dahil TÜM kollara aynı anda** uygulanır;
tek kola uygulamak sayıyı bizim lehimize kaydırır.

**Ne zaman:** Sprint 2 başlamadan — `τ_abstention` eğitilmeden önce.

---

## 🟡 PLANLANMIŞ İŞ — karar değil, yapılacak

### `causal-conv1d` hız kaldıracı — Sprint 2 öncesi ÖLÇÜLECEK

CP5'te ölçüldü: **6.8-7.0 s/it · 2.619 token/s · MFU ≈ %15.** Sebep büyük ölçüde
`causal-conv1d`'nin kurulu olmaması — GatedDeltaNet katmanları PyTorch referans yoluna düşüyor
(*"The fast path is not available"*) ve Qwen3.5-4B'nin **32 katmanının 24'ü** linear-attention.
Fallback **matematiksel olarak aynı**: çıktı geçerli, yalnız yavaş.

**Yapılacak:** Sprint 2'nin 4 koşusundan **önce** image'a eklenip **bir smoke ile s/it ölçülecek.**
2× çıkarsa ~5 saat + ~$12 tasarruf. ⚠️ **Kazanç ölçülmeden yazılmayacak** (`fla-core` dersi, `#40`)
· `requirements.lock.txt` **korunacak**.
Gerekçe ve erteleme kararı: [ADR-0033](adr/0033-egitim-hizi-fla-core-checkpointing-batch.md).

### Korpus temizliği — Sprint 4 ön koşulu

Ölçüm ve gerekçe artık [`TASARIM.md` §5.3](../TASARIM.md)'te. Özet: **1.901 saf kabuk (%4.7)** +
3.101 tadil-kanunu maddesi. **Eğitim ve eval temiz** (sızıntı ölçüldü: %0.06 / sıfır) →
**yeniden eğitim gerektirmez**; risk yalnız retriever indeksinde.

### Merge doğrulama birim testi — Sprint 3 öncesi

ADR-0036'daki 5 parametreli örnek birim testine çevrilecek (ham TIES → p1 = 0.80 · norm-dengeli →
p1 = 0.739, p3 = 0.547). **Zorunlu şart**, `TASARIM.md` §4.2'de kayıtlı.

---

## ✅ KAPANIŞ DİZİNİ — hangi karar nereye gitti

> Kararların kendisi burada **tekrarlanmaz**; kalıcı yerlerinde durur.

| soru | karar | kalıcı yer |
| :--- | :--- | :--- |
| **#8** tekil hücreler | aynı hat + `τg` düz kontrol → **4 hücre** | [ADR-0036](adr/0036-tau-norm-asimetrisi-ve-norm-dengeli-merge.md) Ek · `TASARIM.md` §4.3 |
| **#9** iç iddianın karar kuralı | **Kapı 5** — `min` bileşik, simetrik %90, iki tabanı da geç | [ADR-0037](adr/0037-ic-iddia-karar-kurali-kapi-5.md) · `TASARIM.md` §7 |
| **#10** merge kütüphanesi | **kendi kodumuz** + zorunlu birim testi + `mergekit` çapraz kontrol 🔄 | `TASARIM.md` §4.2 |
| **#11** `τ_reasoning` / RS-FT | **kapsam dışı** — biçim zaten `τ_g`'de (%76), zincirleme harness'ın işi | [ADR-0035](adr/0035-tau-reasoning-rs-ft-kapsam-disi.md) · `TASARIM.md` §2 (satır 13), §10.2 |
| **#12** ΔW norm asimetrisi | **norm-dengeli ana**, ham TIES ablasyon · `‖τ‖` koşulsuz ölçülür | [ADR-0036](adr/0036-tau-norm-asimetrisi-ve-norm-dengeli-merge.md) · `TASARIM.md` §4.2 |
| **#13** rejim eşleşmesi | precision/dropout/modül/uzunluk **eşleşti** · lr/batch **serbest** + tetik · ORPO **epochs 3** | `TASARIM.md` **§4.1.1** |
| **§13.2** red kapısı eşiği | **katı** — tek doğrulanamayan atıf tüm cevabı reddettirir | [ADR-0038](adr/0038-red-kapisi-esigi-kati.md) |
| **§13.4** zamansal eksen | **kapsam dışı** — sebep tercih değil, korpusta metadata yok | `TASARIM.md` §10.2 · ön koşul §5.3 |
| **§13.7** yinelemeli merge | **konusuz kaldı** — `k=2`'de ayrım tanımsız | `TASARIM.md` §4.2 |
| kod borcu — ORPO rejim sapması | `--bf16-base` + `--lora-dropout` eklendi | `scripts/train_orpo.py` · `modal_train.py` · `TASARIM.md` §4.1.1 |
| kod borcu — `--target-modules` | **zorunlu**, varsayılan silindi (bedel ölçüldü: `‖τ‖`'nin %26.8'i) | her iki eğitim script'i · `TASARIM.md` §4.1.1 |
| gözlem — sıfır marjinal maliyet | ek çıkarım bizde ucuz/rakipte pahalı · `N*` etkilenmiyor | `TASARIM.md` §6.4 |

---

## Başka yerde duran açık kalemler — burada tekrarlanmaz

| ne | nerede |
| :--- | :--- |
| `τ_abstention` Sprint 1'e çekilsin mi | [`sprint1.md`](../sprint1.md) §Sprint 1 dışında kalanlar |
| Sağlayıcı pinlemesi · rakip üretim maliyeti · CP2 M2 regex uyuşmazlığı | [`docs/record/sprint1/NEXT-SESSION.md`](record/sprint1/NEXT-SESSION.md) |
| H100 hız kaldıracı | [ADR-0033](adr/0033-egitim-hizi-fla-core-checkpointing-batch.md) |
| Devir paketinin yedeksiz tek nüsha olması | [ADR-0034](adr/0034-emekli-hat-artefaktlarinin-repodan-cikarilmasi.md) |
| Doğrulayıcı kalibrasyonu (yanlış-negatif → coverage kaybı) | [ADR-0038](adr/0038-red-kapisi-esigi-kati.md) |
