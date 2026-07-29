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

### §13.9 — `τ_g` reçetesi fazla sert miydi? ⏸️ *ölçüm bekliyor* — **CP0-b**

CP6 iki hasar bıraktı ve **ikisi de aynı sebepten olabilir**: cevap doğruluğu %2.7 → %17.4
(**sahipsiz negatif** — hiçbir kolun görevi değil) ve *(varsayım)* düşünme yeteneğinin bastırılması.
Ortak şüpheli **reçete**: 1.083 adım · lr 1e-4 · `all-linear` · r=16.

**Ölçüm:** `τ_g` `--thinking on` koşulur, ~20 çıktı gözle incelenir (`sprint2.md` CP0-b, $0).
**Karar kuralı:** bozulmuşsa `τ_g` v2 (yumuşak reçete + `build_replay_tr.py` replay karışımı)
masaya gelir — **ama CP0-a'nın sonucu beklenir**: a YEŞİL ise `τ_g` zaten RS-FT kapsamında
yeniden doğar, ayrı v2 israf olur. Gerekçe: [ADR-0040](adr/0040-dusunce-modu-olculecek-on-kayitli-kural.md) m.3.

---

### §13.10 — RS-FT / düşünce modu tez kapsamına girecek mi? ⏸️ *ölçüm bekliyor* — **CP0-a**

**Karar kuralı ön-kayıtlı ve yazılı** ([ADR-0040](adr/0040-dusunce-modu-olculecek-on-kayitli-kural.md));
açık olan yalnız **sonuç**. 🟢 YEŞİL → RS-FT kapsama girer, ADR-0030 m.2 geri alınır, ADR-0035
yeniden açılır, Sprint 1'in üç öznesi yeniden koşulur (~$0.5), takvim ~3-4 hafta uzar ·
🟡 → thinking rapor edilen eksen olur · 🔴 → ADR-0030 m.2 kanıtla teyit, RS-FT future-work.

⚠️ **YEŞİL sadece iyi haber değil:** base *hiç eğitilmeden* `τ_a`'nın işinin çoğunu yapıyorsa,
dış iddiada üçüncü bir açıklama belirir (*ince-ayar mı, harness mı, **düşünme mi***) ve makalenin
çerçevesi daralır. **Ne zaman:** Sprint 2'nin 1. günü.

---

## 🟡 PLANLANMIŞ İŞ — karar değil, yapılacak

### `causal-conv1d` hız kaldıracı — Sprint 2 öncesi ÖLÇÜLECEK

CP5'te ölçüldü: **6.8-7.0 s/it · 2.619 token/s · MFU ≈ %15.** Sebep büyük ölçüde
`causal-conv1d`'nin kurulu olmaması — GatedDeltaNet katmanları PyTorch referans yoluna düşüyor
(*"The fast path is not available"*) ve Qwen3.5-4B'nin **32 katmanının 24'ü** linear-attention.
Fallback **matematiksel olarak aynı**: çıktı geçerli, yalnız yavaş.

**Yapılacak:** Sprint 2'nin 3 eğitim koşusundan **önce** image'a eklenip **bir smoke ile s/it
ölçülecek** — [`sprint2.md`](../sprint2.md) **CP0.5**. **Kapı: ≥2× yoksa eklenmez**, ölçüm negatif
bulgu olarak yazılır. 2× çıkarsa ~5 saat + ~$12 tasarruf. ⚠️ **Kazanç ölçülmeden yazılmayacak**
(`fla-core` dersi, `#40`) · `requirements.lock.txt` **korunacak**.
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
| **#11** `τ_reasoning` / RS-FT | **kapsam dışı** — biçim zaten `τ_g`'de (%76), zincirleme harness'ın işi. ⚠️ **§13.10 ile şartlı yeniden açıldı** (CP0-a YEŞİL çıkarsa) | [ADR-0035](adr/0035-tau-reasoning-rs-ft-kapsam-disi.md) · [ADR-0040](adr/0040-dusunce-modu-olculecek-on-kayitli-kural.md) · `TASARIM.md` §2 (satır 13), §10.2 |
| **#12** ΔW norm asimetrisi | **norm-dengeli ana**, ham TIES ablasyon · `‖τ‖` koşulsuz ölçülür | [ADR-0036](adr/0036-tau-norm-asimetrisi-ve-norm-dengeli-merge.md) · `TASARIM.md` §4.2 |
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
| CP2 tablosundaki 4 sayı uyuşmazlığı (işaretlendi, düzeltilmedi) | [`sprint1.md`](../sprint1.md) CP2 · [#41 §6](record/research_log/2026-07-29-cp6-tau-grounding-olcumu.md) |
| H100 hız kaldıracı | [ADR-0033](adr/0033-egitim-hizi-fla-core-checkpointing-batch.md) |
| Devir paketinin yedeksiz tek nüsha olması | [ADR-0034](adr/0034-emekli-hat-artefaktlarinin-repodan-cikarilmasi.md) |
| Doğrulayıcı kalibrasyonu (yanlış-negatif → coverage kaybı) | [ADR-0038](adr/0038-red-kapisi-esigi-kati.md) |
