# Sprint 3 **PART 1** — HARNESS: modeli ürüne çevirmek

> 📁 **Bu belge KAPANDI ve KAYITTIR.** Buradaki hiçbir satır artık koşulmaz; sayılar ve
> gerekçeler **kaynak** olarak durur.
>
> **Devamı (Part 2)** Part 1'in *ölçerek açtığı* borçları kapatır. Kararları verildi ve
> [ADR-0056](docs/adr/0056-m2b-harness-acik-protokolu-ve-0055-cipasi.md)'da; **uygulama
> planı** `docs/plans/` altına yazılır.
>
> # ✅ SPRINT 3 PART 1 KAPANDI — 2026-08-05
>
> **Adım 0 🔴 · Adım 1-4 ✅ · S3a ✅ · S1 ✅ · S3 ✅ · S2 ✅ · S4 ✅** — dört işin dördü bitti.
>
> ## Ürünün resmî sayısı
>
> | eksen | KAPALI (m1) | AÇIK k=5 | AÇIK k=10 | **AÇIK k=10 + S2** ⭐ |
> | :--- | ---: | ---: | ---: | ---: |
> | `recall@10` | — | — | 0,8750 | **0,8750** |
> | coverage | 0,7875 | 0,7500 | 0,7750 | **0,7625** |
> | **A1** (cevaplanan-only) | 0,9087 | 0,7591 | 0,7681 | **0,8042** |
> | A1 · altın getirilen | 0,9087 | 0,9230 | 0,8426 | **0,8616** |
> | **KÜTLE** | **%71,6** | %56,9 | %59,5 | **%61,3** |
> | uydurulmuş madde no | 0 | 0/89 | 0/120 | **0/118** |
>
> `outputs/eval/s2-harness-k10-etiketli/` · hakem `openai/gpt-4o-mini` @ openrouter (pin `OpenAI`)
>
> ## ⭐ *"Harness açılınca kütle neden düştü — suç modelde mi harness'ta mı?"*
>
> **Yanlış okuma:** *%71,6 → %61,3 bir gerilemedir.* Değil — **iki ölçüm aynı şeyi ölçmüyor.**
> KAPALI'da altın madde bağlama **kurgu gereği garanti** konuyor; AÇIK'ta **bulunması gerekiyor.**
> KAPALI bir rakip değil, **tavan**. Açık ayrıştırılabilir ve ayrıştırıldı:
>
> ```
> KAPALI 57,25/80 = %71,6      AÇIK 49,06/80 = %61,3      açık = 10,2 puan
>
> ① ERİŞİM ISKASI   altın 10/80 soruda HİÇ gelmiyor          ≈ 5,1 puan  ← HARNESS'IN
> ② ALTIN BAĞLAMDA  getirilen 70 soruda KAPALI'dan sapma     ≈ 4,5 puan  ← MODELİN
>                     ├ çekinme  0,771 ↔ 0,787  → neredeyse AYNI
>                     └ sadakat  0,862 ↔ 0,909  → DİKKAT DAĞILMASI
> ```
>
> **Cevap: yarı yarıya.** Yarısı harness'ın (erişim ıskası — yeniden sıralamayla kapanır,
> post-sprint sıra 4), yarısı modelin (dikkat dağılması — bağlam yönetimi / eğitim).
>
> 🚨 **Ve bir çerçeve düzeltmesi:** aşırı-red **harness'ın suçu değil**. Harness KAPALI'da
> model, altın madde **garanti** bağlamdayken **17/80 (%21,2)** çekiniyor; AÇIK'ta altın
> getirilen alt kümede **16/70 (%22,9)**. **İki oran neredeyse aynı** → B10 bir **model
> özelliği**, bir harness gerilemesi değil. Bu, *"eğitimle kapanır"* hükmünü kanıtlıyor.
>
> ## Sprintin kazandırdığı — sayı değil, **dört mekanizma**
>
> 1. **`k` büyütmenin bedeli var.** Altın madde bağlamdayken bile yanına madde konunca A1
>    düşüyor (0,9230 → 0,8426). Dikkat dağılması **ölçüldü**, spekülasyon değil. → `k=20` zayıf.
> 2. **Çekinme yanlış sinyale kalibre.** Model **konusal uyuma** bakıyor, **yeterliliğe** değil
>    → erişimin en çok battığı yerde en az çekiniyor. ADR-0055'in ekseni bu bulgudan çıktı.
> 3. **Doğrulayıcı fabrikasyonu değil transkripsiyonu yakalıyor.** Uydurma madde no **0/118**;
>    ilk gerçek yakalayış bir **harf düşmesi** (borç B8).
> 4. **Hakem gürültüsünün tabanı var:** aynı girdide **A1'de ~0,3 puan** (#55 §9). Bunun
>    altındaki hiçbir fark yorumlanmaz.
>
> ## Sprintin bedeli
>
> **GPU $0** (harness CPU'da, üretim yerelde) · **hakem $0,127** *(bütçe ≤ $2)* ·
> **7 research_log** ([#49](docs/record/research_log/2026-08-04-s3a-on-prob.md) ·
> [#50](docs/record/research_log/2026-08-04-modul-basina-norm.md) ·
> [#51](docs/record/research_log/2026-08-04-harness-acik-ilk-olcum.md) ·
> [#52](docs/record/research_log/2026-08-05-korpus-butunlugu.md) ·
> [#53](docs/record/research_log/2026-08-05-ayirt-edicilik-etiketi.md) ·
> [#54](docs/record/research_log/2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md) ·
> [#55](docs/record/research_log/2026-08-05-s2-yururluk-alani.md)) ·
> **3 ADR** ([0053](docs/adr/0053-modul-basina-norm-kapsami-reddedildi.md) ·
> [0054](docs/adr/0054-harness-tasarim-kararlari-k2-k5.md) ·
> [0055](docs/adr/0055-isabet-denetimi-ekseni.md)) · **3 yeni tuzak** (2.16 · 7.5 · 7.6) ·
> **3 yeni betik** (`retriever.py` · `atif_dogrula.py` · `red_kapisi.py`) + `korpus_yururluk.py`
>
> ## 🚨 Sprint 4'ün gerekçesi — bugün ölçüldü
>
> **Coverage kaybının BÜYÜK yarısı aşırı-red: altın madde bağlamdayken 16/80 çekiniyor**,
> ve bu sayı **`k`'dan bağımsız** (14 → 15 → 16). Retriever ne kadar iyileşirse iyileşsin
> kapanmıyor — **harness'la değil eğitimle** kapanır. B1 (7/80) bunun yarısı kadar.
>
---

# ▶ SIRADAKİ — ⛔ **BU BELGEDE KOŞACAK İŞ KALMADI**

> **Part 1'in dört işi de kapandı.** Bu belge artık **kayıt**; canlı iş yok.
> Part 2'nin kararları: **[ADR-0056](docs/adr/0056-m2b-harness-acik-protokolu-ve-0055-cipasi.md)** ·
> uygulama planı `docs/plans/` altına yazılacak.
>
> Part 1'in ölçerek bıraktığı borçlar ve sıraları aşağıdaki
> [post-sprint 3 sırasında](#post-sprint-3-sırası) duruyor — **ölçüm bağlamlarıyla birlikte**,
> çünkü bir borcun büyüklüğü onu üreten koşudan koparılınca yorumlanamaz hâle gelir.
> Part 2 o sıradan hangisini aldığını ve **neden** aldığını kendi belgesinde yazar.

<details><summary>Sprint boyunca geçerli olan koşu kısıtları (kayıt)</summary>

```
🛑 DURMA : geçerlilik kapısı düşerse · kütle DÜŞERSE (ön-kayıtlı eşikler)
           · korpusa yazmadan önce (S2) yedek yoksa · bütçe: hakem toplam ≤ $2
kapsam   : S1-S4.  Graph-RAG, ajanlar, vatandaş kipi DIŞINDA
           graf gerekçesi ve ön-kayıtlı tahmini: ROADMAP.md §5.2 — ayrı yetenek,
           ayrı soru kümesiyle ölçülür; bu kümede ölçmek haksız yere başarısız gösterir
```

**⚠️ SIRA BAĞLAYICIYDI — S1 mutlaka S2'den ÖNCE (uygulandı).** S2 korpusu değiştiriyor;
k=5 **eski**, k=10 **yeni** korpusta ölçülseydi `k` farkıyla **korpus** farkı karışırdı ve
hiçbir yerde hata çıkmazdı. Bu, tam olarak bu hattın hata sınıfı.

</details>
---

## Durum tablosu — **8 ✅ · 1 🔴 · 0 açık**

| adım | durum | çıktı |
| :--- | :--- | :--- |
| **K1** gömme modeli | ✅ **çözüldü** | `bge-m3` + BM25 hibriti (RRF) — research_log #49 |
| **K2-K5** tasarım kararları | ✅ **KİLİTLENDİ** 2026-08-04 | [ADR-0054](docs/adr/0054-harness-tasarim-kararlari-k2-k5.md) — ⛔ kilidi açıldı, Adım 1-4 kodlanabilir |
| **S3a** ön-prob (recall@k + bedesten) | ✅ **KAPANDI** 2026-08-04 | hibrit `recall@10` **0,875** · bedesten ✅ GEÇERLİ · `outputs/eval/s3a-on-prob/` · research_log #49 |
| **0** modül-başına norm | 🔴 **REDDEDİLDİ** 2026-08-04 | kütle ≤ %56,2 < %71,6 · hakem **$0** · [ADR-0053](docs/adr/0053-modul-basina-norm-kapsami-reddedildi.md) · research_log #50 |
| **1** retriever | ✅ **BİTTİ** 2026-08-04 | `scripts/retriever.py` + `data/index/mevzuat_bge_m3/` (40.496 madde, 83 MB) · bileşen S3a sayısını birebir üretti: **recall@10 0,8750 · @20 0,9250** · 759 ms/sorgu (CPU) |
| **2** atıf doğrulayıcı | ✅ **BİTTİ** 2026-08-04 | `scripts/atif_dogrula.py` — hakemsiz. Gerçek çıktıda 56 atıf · 53 doğrulandı · **0 yanlış alarm** · pozitif kontrol geçti. Gözle denetim **dört** yanlış-alarm hatası buldu (ad çakışması · başlık biçimi · Türkçe `upper()` · ada kaçan sözcük) |
| **3** red kapısı | ✅ **BİTTİ** 2026-08-04 | `scripts/red_kapisi.py` — ADR-0038 katı + `cogunluk`/`cerrahi` ablasyonları, üçü post-hoc aynı kümede |
| **4** harness AÇIK ölçüm | ✅ **ÖLÇÜLDÜ 2026-08-04** ⚠️ sayıları 08-05'te düzeltildi | kütle **%71,6 → ~~%58,7~~ %56,9** · ⭐ altın getirilince A1 **~~0,9344~~ 0,9230 > 0,9087** · uydurulmuş atıf **0/89** · `outputs/eval/s3-harness-acik/` · research_log **#51** + düzeltme **#54** |
| **S1** `k` süpürmesi (B3) | ✅ **KAPANDI 2026-08-05 — `k=10` KABUL** | kütle **%56,9 → %59,5** (+2,6) · `recall@10` **0,875** (70/80) · ⚠️ bedeli ölçüldü: altın getirilende A1 **0,9230 → 0,8426** (dikkat dağılması) · B1 sınıfı **14 → 7**, aşırı-red **14 → 15** (değişmedi) · 🚨 **tuzak 2.16** bulundu ve 8 belge düzeltildi · hakem **$0,0403** · `outputs/eval/s3-harness-k10/` · research_log **#54** |
| **S3** ayırt-edicilik etiketi (B2) | ✅ **KAPANDI 2026-08-05** | kör hakem, istem ön-kayıtlı · **62 ayırt edici / 18 belirsiz (%22,5)** · `recall@5` **0,8226 ↔ 0,5000** (tuzak 7.4 doğrulandı) · ⭐⭐ **ters çekinme kalibrasyonu** bulundu (belirsizde %5,6, ayırt edicide %30,6 çekinme) · hakem **$0,0069** · `outputs/eval/s3-ayirt-edicilik/` · research_log **#53** |
| **S2** yürürlük alanı (B7) | ✅ **KAPANDI 2026-08-05 — B7 KAPANDI** | ⭐ **NİHAİ SAYI:** kütle **%59,5 → %61,3** · A1 **0,7681 → 0,8042** (+3,6 p) · `recall@10` **0,8750** · bozuk blok **14/800 → 0/800** · `outputs/eval/s2-harness-k10-etiketli/` · hakem **$0,0398** · `mulga`+ilga alanı **2.547 satır** (%99,6 kaynaklı) · alt-madde kimliği **485 satır** · **`MULGA`** hükmü (`red_kapisi` değişmedi) · kabul 3/3 ✅ · ⭐ **kapsam ölçümden seçildi:** sınıf A modele **0/800** ulaşıyor → elenmedi (**B9**) · 🐞 iki kural verify hedefine çarpıp düzeldi (sonek **%80 eksikti**: 98 → **485**; ilga kaynağı **tarihi kanun sanıyordu**) · ⚠️ **dürüst negatif (atıf kanalı):** `MULGA` **0**, hükmü değişen cevap **0/80** · ⚠️ **ön-kayıtlı kütle tahmini TUTMADI** (%59,5±1 dendi, %61,3 çıktı — kazanç erişim kanalından geldi) · 🚨 eval altın etiketi **3 kalemde** kör hakemle düzeltildi (insan onaylı; manşeti **yükseltmedi**) · 🎁 hakem yeniden-koşum gürültüsü ilk kez ölçüldü: **A1'de ~0,3 puan** · research_log **#52 + #55** |
| **S4** isabet denetimi tasarımı (B1) | ✅ **KAPANDI 2026-08-05 — kod açılmadı** | [ADR-0055](docs/adr/0055-isabet-denetimi-ekseni.md): denetim **kaynak-yeterliliği** ekseninde kurulur · ❌ cevap↔kaynak örtüşme **reddedildi** (B1'in çekirdek vakasında kör; sınıfı zaten boş — uydurma no **0/118**) · 🔁 yeniden-sıralama **ayrı tur** (dikkat dağılmasının çaresi, ama karıştırılırsa ikisi de yorumlanamaz) · ilk deney **$0** (`--sufficiency-preamble` bayrağı zaten var) · ön-kayıtlı kabul yazıldı |
| **araç onarımı** *(sprint sonu)* | ✅ **2026-08-05** | `cp0_thinking_score.sh`'ta **`h1` dalı yoktu** — harness modunda hakemi hiç çağırmadan `0` ile çıkıyordu; dal eklendi + tanınmayan mod artık **ölüyor** · geçit varsayılanı **OpenRouter**'a alındı (tek yol, insan kararı) · `harness_tablo.py` atıf sayacına **`MULGA`** anahtarı (yoksa `KeyError`) |

## 📌 Sprint 3'ün borçları — **6 açık · 3 kapandı**

Hiçbiri Sprint 3'ü durdurmadı; hepsi **ölçülerek** ortaya çıktı ve S4'ün şeklini belirledi.

<a id="post-sprint-3-sırası"></a>

> ### 📋 POST-SPRINT 3 SIRASI ⬅️ **BU BÖLÜM CANLI** *(belgenin geri kalanı KAYIT)*
>
> Sıra **ölçülmüş büyüklük ÷ bedel** ile kuruldu. 1-4 harness tarafı ve **hepsi ucuz**;
> üçü bir **ölçüm boşluğu** kapatıyor. 5 eğitim tarafı ve pahalı — ama ancak 1-4 bitince
> *"geriye ne kaldı"* net olur. **Bugün B1'e eğitim atmak, henüz sayılmamış bir açığa para
> harcamak olurdu.**
>
> | sıra | iş | bedel | neden burada |
> | :--- | :--- | :--- | :--- |
> | **1** | **B-i deneyi** ([ADR-0055](docs/adr/0055-isabet-denetimi-ekseni.md)) — `--sufficiency-preamble` | **$0** | Bayrak **zaten var**. Tek deney **B1 ve B10'a birden** dokunuyor (yetersizde cevaplama ↔ yeterlide çekinme). Red şıkkı ön-kayıtlı. |
> | **2** | **B5** — K2'nin bedeli | ~$0 | B1'in **7/80**'i sayılmadan **temiz değil**: içinde *"getirildi ama 900-karakter kırpmasının ötesindeydi"* vakası olabilir. |
> | **3** | **B8** — yazım hatası toleransı | ~$0 | Tolerans **ölçülmeden seçilmez**: kaç doğru atıf kurtulur ↔ kaç yanlış içeri girer. |
> | **4** | **C** ([ADR-0055](docs/adr/0055-isabet-denetimi-ekseni.md)) — ikinci geçiş yeniden-sıralama | CPU | Dikkat dağılmasının (**0,9230 → 0,8426**) ölçülmüş çaresi. ⚠️ **B-i ile aynı turda değil.** |
> | **5** | **B10 + B4** — aşırı-red (**16/80**) / `τ_a` seyreltme | **GPU, eğitim** | Coverage kaybının **büyük yarısı**. Harness'la kapanmıyor. Kendi sprint'i. |
> | **6** | **B9** — indeks hijyeni | ~10 dk + koşu | Ucuz ama **indeksi değiştirir** → indeksin zaten değişeceği bir turla **paketlenir**. |
> | **7** | **B6** — canlı `bedesten` | ürün işi | Güncellik iddiası ayakta ama kanıtlanmamış. Doğruluk işleri bitince. |
>
> ⚠️ **Belge seçimi bilinçli sapmadır:** repo kuralı *"kapanan belge kayıttır, canlı tutulmaz"*
> der; borç sırası yine de burada tutuluyor (insan kararı, 2026-08-05) — çünkü borçların
> **ölçüm bağlamı** bu belgede ve ayrı bir belgeye taşımak gerekçeyi bağlamından koparıyordu.
> Sapma gizlenmiyor.

### 🔴 AÇIK — 6 borç

| # | borç | ölçülen büyüklük | neden önemli |
| :--- | :--- | :--- | :--- |
| **B10** 🆕 ⭐ | **AŞIRI-RED — altın madde BAĞLAMDAYKEN çekinme.** | **16/80** · k=5'te 14, k=10'da 15, +S2'de 16 → **`k`'dan bağımsız** | 🚨 **Coverage kaybının BÜYÜK yarısı burada, B1'in (7/80) iki katı** — ama bugüne kadar **numarası yoktu**, yalnız B1'in notunda geçiyordu; numarasız borç hiçbir listede görünmez. Retriever ne kadar iyileşirse iyileşsin kapanmıyor. Mekanizması [#53](docs/record/research_log/2026-08-05-ayirt-edicilik-etiketi.md)'te ölçüldü: çekinme sinyali **konusal uyuma** bakıyor, **yeterliliğe** değil. ⚠️ B4 ile **birleştirilmedi**: *"aşırı-red `τ_a` seyrelmesinden geliyor"* makul ama **ölçülmemiş bir varsayım**; birleştirmek varsayımı kayıtta gerçeğe çevirirdi. |
| **B1** ⭐ | **"Gerçek ama soruya uymayan madde"** — doğrulayıcı bunu yakalayamıyor. | ~~14/80~~ → **7/80** (k=10 ile yarıya indi) | Ürün vaadi *"denetlenebilir"*. Bugün **fabrikasyona karşı** denetlenebilir, **isabetsizliğe karşı değil**. [ADR-0055](docs/adr/0055-isabet-denetimi-ekseni.md) ekseni belirledi, kod açılmadı. |
| **B4** | **`τ_a` merge'de seyreliyor** (0,987 → 0,877). Adım 0 bunun norm *kapsamı* olmadığını gösterdi. | ‖τ_a‖ = **1,18** (82 adım @1e-5) | Çözüm merge parametresinde değil, muhtemelen `τ_a`'nın **eğitim genliğinde**. Eğitim işi. |
| **B5** | **K2'nin bedeli ölçülmedi**: *"getirildi ama cevap 900 karakter kırpmasının ötesindeydi"* vakası. | **sayılmadı** (iz var) | ADR-0054 bunu ayrı vaka sınıfı olarak saymayı **şart koşmuştu**. B1'in 7/80'i bu sayılmadan temiz değil. |
| **B8** | **Katı kapı tek karakterlik yazım hatasına takılıyor.** Model `FİKİR VE SANAT ESERLERİ KANUNU`'nu `…ESELERİ…` diye kopyaladı; madde no'ları **doğru**, kanun bağlamda **var** → `KANUN_YOK` → cevabın tamamı reddedildi. | **1/80** | Doğrulayıcının **ilk gerçek yakalayışı** ve o bir fabrikasyon değil **transkripsiyon hatası**. ADR-0038 resmî adın *kısa hâlini* çözmüştü, **yazım hatasını** çözmüyor. ⚠️ Tolerans kapıyı **gevşetir** — ölçülmeden karar verilmez. |
| **B9** 🆕 | **Tablo/cetvel parçaları madde diye indeksli** (~7.966 satır, `3520`'de yoğun; `", Ek"` gibi 4 karakterlik hücreler). S2'de **kasten elenmedi**. | modele **0/800** blok ulaşıyor | Elemek *ölçülemez bir kazanç için ölçülmüş bir sayıyı harcamak* olurdu (indeks değişir → `recall@k` kayar → k kıyası geçersizleşir). ⚠️ *"Anahtar yinelenmesi %29,4"* ile *"bağlam kirlenmesi %1,8"* **ikisi de doğru** — farklı nesneler. |
| **B6** | **Canlı `bedesten` katmanı** eklenmedi (K3: bilinçli erteleme). | — | Güncellik iddiası ayakta ama **kanıtlanmış değil** — S3a sözleşmenin çalıştığını doğruladı, ürün onu henüz kullanmıyor. |

### ✅ KAPANDI — 3 borç

| # | kapanış | sonuç |
| :--- | :--- | :--- |
| ~~**B2**~~ | **2026-08-05 (S3)** — ayırt-edicilik etiketi, kör hakem + ön-kayıtlı istem. **62/18**. | Tuzak 7.4 **sayıyla** doğrulandı: `recall@5` **0,8226 ↔ 0,5000** (32,3 puan). Bundan sonra hiçbir harness sayısı bu ayrım yapılmadan raporlanmaz. **#53** |
| ~~**B3**~~ | **2026-08-05 (S1)** — `k=10` süpürüldü ve **kabul edildi** (kütle %56,9 → **%59,5**). | Kazanç tahminin (~%65) **altında**; bedeli ölçüldü: dikkat dağılması A1'i **8 puan** düşürüyor. `k=20` gerekçesi **zayıf**. **#54** |
| ~~**B7**~~ | **2026-08-05 (S2)** — korpusa `mulga` + ilga alanı (**2.547 satır**), alt-madde kimliği (**485 satır**), **`MULGA`** hükmü. `"İş Kanunu Madde 15"` artık üç red politikasında da **REDDEDİLİYOR**. | ⚠️ **Dürüst negatif:** `MULGA` **0**, hükmü değişen cevap **0/80** — mekanik kapandı, bu DEV kümesinde **tetiklenmedi** (`core_hard` yürürlükteki maddelerden üretildi). **B7 bir ürün-güvenliği özelliği, skor özelliği değil.** Erişim kanalından ayrıca **+3,6 puan A1**. **#55** · özgün kayıt aşağıda. |

<details><summary>B7'nin özgün kaydı — açığın ilk görüldüğü hâl (2026-08-04)</summary>

**MÜLGA maddeye yapılan atıf doğrulamayı ve katı kapıyı GEÇİYOR.** `"İŞ KANUNU Madde 15"` →
`DOGRULANDI` (kanun_no **1475**) → kapı ✅. Oysa korpustaki metni:
*"110- (Mülga: 22/5/2003/4857/120 md.)"*.

**Ürün-güvenliği açığı, akademik değil.** Vaadimiz *"denetlenebilir"*; burada sistem
**yürürlükten kalkmış** bir hükme yapılan atıfı **doğrulanmış** damgalıyor. Korpusta yürürlük
alanı **yok** — 4 alan var (`kanun_adi · kanun_no · madde_no · text`) ve ilga bilgisi yalnız
**serbest metnin içinde**. Aynı ad iki kanuna ait olabildiği için (`İŞ KANUNU` = 4857
yürürlükte **ve** 1475 mülga) doğrulayıcı ayırt edemiyor.

</details>

### 🚨 B7 hakkında — bu, graph-RAG'in ölçülmüş gerekçesi

Bugüne kadar graph-RAG *"hukuk ilişkiseldir"* diye **varsayımla** savunuluyordu
([`VISION.md`](docs/VISION.md) Faz 2). Bugün ilk kez **ölçülmüş** bir gerekçe çıktı ve
beklenen yerde değil:

- ❌ **Erişim kalitesi için değil.** Recall eğrisi `@5` 0,750 → `@10` 0,875 → `@20` 0,925
  diyor; kalan açığın çoğu **k'yı büyütmekle** kapanıyor (borç B3, bedeli ~0). Ayrıca
  soruların ~%25'i konusunu hiç belirtmiyor — graf, belirsiz sorguyu düzeltemez.
- ❌ **Cevap kalitesi için de değil.** Altın getirildiğinde A1 zaten **0,934**; model
  ilişki çıkarımına ihtiyaç duymuyor.
- ✅ **Yürürlük ve atıf zincirleri için.** İlga/tadil ilişkisi, aynı adı taşıyan mülga
  kanunlar, *"yerine işlenmiştir"* kabuk maddeleri — **bunların hiçbiri düz vektör
  benzerliğinden okunamaz.** B7 tam bu sınıf.

⚠️ **Ama acil çözüm graf değil.** B7'nin ucuz çaresi korpusa **yürürlük alanı** eklemek
(`mulga: true/false` + ilga eden kanun/madde) — bu bir **veri** işi, graf değil. Graf, o
alan varken **atıf zincirleri** ve **çapraz referans** için hak eder. Sıralama:
**B7 (veri) → B3 (k) → B1 (isabet) → graf**.

📌 **Graf'ın mimari farkı, ön-kayıtlı tahmini ve gerçekten kazanacağı üç yer
[`ROADMAP.md` §5.2](ROADMAP.md)'de.** Özeti: bugünkü kümede graf **ölçülemez** bir
iyileşme üretirdi (sorular tek-madde, çok-hop yok, n=80'de ±2 soru gürültü) — bu yüzden
bugün koşulmadı; kurulursa **kendi soru kümesiyle** ölçülür.
---

## Dört işin özeti

> Tam kayıt `research_log`'da; burada **ne yapıldı, ne çıktı, ne öğrenildi** var.

### ✅ S1 — `k` süpürmesi *(borç B3)* · **KAPANDI 2026-08-05 · `k=10` KABUL** · [#54](docs/record/research_log/2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md)

> GPU **$0** · hakem **$0,0403** · geçerlilik kapısı ✅ (kesik %2,5) · örneklem birebir aynı 80 ✅

**Sonuç:** kütle **%56,9 → %59,5** (+2,6 p) — kabul karşılandı, ama ön-kayıtlı tahminin
(~%65) **altında**, ve sebebi ölçüldü.

⭐ **Bulgu — `k` büyütmenin ölçülmüş bedeli:** altın madde bağlamdayken bile, yanına madde
konunca A1 **8 puan** düşüyor (`0,9230 → 0,8426`). Net kazanç, erişimin kazandırdığı **+10
sorunun** bu bedeli aşmasından geliyor. → **`k=20` gerekçesi zayıf** (`recall@20` +5 puan,
bağlam iki kat, bedel ölçülmüş biçimde büyür).

**İki kazanç daha:** B1 sınıfı **14 → 7** · ters çekinme kalibrasyonu **yönü düzeliyor**
(belirsizde coverage 0,944 → 0,722, ayırt edicide 0,694 → 0,790).
**Yeni borç B8:** doğrulayıcının ilk gerçek yakalayışı bir **harf düşmesi** (`…ESELERİ…`).

🚨 **Bu sprintin yayınlanmış kütle sayısı yanlış metrikle üretilmişti** (tuzak **2.16**):
`harness_tablo.py` `A1` diye **cevaplanan-only** değil **ham makro** yazıyordu; sapmanın
**yönü sabit değil** (k=5'te yukarı, k=10'da aşağı) ve KAPALI çıpa doğru metrikteydi →
ON/OFF kıyası **elmayla armuttu**. [ADR-0050](docs/adr/0050-verim-kapisi-tahmin-edici-duzeltmesi.md)
uygulandı: **eşik değil ALET** düzeltildi, iki kola simetrik, eşik yeniden türetildi
(%58,7 → %56,9). 8 belge düzeltildi.

<details><summary>S1'in ön-kayıtlı planı (kayıt, üzerine yazılmadı)</summary>

```
1. k ∈ {5, 10} için harness AÇIK koş (k=5 zaten var, yalnız k=10 koşulacak)
   → verify: geçerlilik kapısı geçiyor (kesik ≤ %5) ve bağlam CTX 8192'ye sığıyor
2. harness_tablo.py ile iki k'yı yan yana koy
   → verify: erişim/davranış çapraz tablosu k=10'da altın-getirildi sayısını yükseltiyor
3. kütleyi karşılaştır
```

**⛔ ÖN-KAYITLI TAHMİN (2026-08-04, sayı görülmeden):** bugünkü çapraz tablodan türetildi —
altın getirildiğinde cevaplama oranı 46/60 = **0,767**, altın getirilenlerde A1 **0,934**,
getirilmeyenlerde A1 **0,284** *(0,7823×60 − 0,934×46)/14 ile türetildi)*.

| k | beklenen altın getirilen | beklenen coverage | beklenen A1 | **beklenen kütle** |
| ---: | ---: | ---: | ---: | ---: |
| 5 *(ölçüldü)* | 60/80 | 0,750 | 0,782 | **%58,7** |
| **10** | ~70/80 | ~0,76 | ~0,86 | **~%65** |
| 20 | ~74/80 | ~0,76 | ~0,89 | ~%68 · ⚠️ 20×900 kar ≈ 6K token, düşünce bütçesiyle CTX'e sığmaz |

**Kabul:** k=10 kütlesi **> %58,7**. **Ret:** kütle düşerse → k=5 kalır, sebebi
(bağlam uzunluğu mu, dikkat dağılması mı) **gözle okunur**, uydurulmaz.

</details>

### ✅ S3 — Ayırt-edicilik etiketi *(borç B2)* · **KAPANDI 2026-08-05** · [#53](docs/record/research_log/2026-08-05-ayirt-edicilik-etiketi.md)

> S1 koşarken paralel koşuldu (hakem API'si; GPU'ya ve korpusa dokunmuyor) · hakem **$0,0069**
> · istem koşudan **önce** kayda geçti · körlük çağrı imzasının kısıtı (`_istem(soru)`).

**Etiket: 62 ayırt edici · 18 belirsiz (%22,5).**

| eksen (k=5) | ayırt edici (n=62) | belirsiz (n=18) |
| :--- | ---: | ---: |
| `recall@5` | **0,8226** | **0,5000** |
| coverage | 0,6935 | 0,9444 |
| kütle | %60,0 | %46,4 |

**Tuzak 7.4 sayıyla doğrulandı:** `recall@5` iki alt küme arasında **32,3 puan** ayrışıyor →
*"recall@5 = 0,750"* retriever'ın değil **kümenin kompozisyonunun** sayısı. Bundan sonra
hiçbir harness sayısı bu ayrım yapılmadan raporlanmaz.

⭐⭐ **Sprintin en değerli bulgusu:** model, erişimin **en çok battığı** yerde **en az**
çekiniyor (belirsizde %5,6, ayırt edicide %30,6). Mekanizma: çekinme sinyali bağlamın
**konusal uyumundan** geliyor, **yeterliliğinden** değil → doğrudan
[ADR-0055](docs/adr/0055-isabet-denetimi-ekseni.md)'in ekseni oldu. *(k=10 tersliğin yönünü
düzeltiyor ama kapatmıyor.)*

### ✅ S2 — Yürürlük alanı *(borç B7)* · **KAPANDI 2026-08-05** 🚨 ürün-güvenliği · [#52](docs/record/research_log/2026-08-05-korpus-butunlugu.md) + [#55](docs/record/research_log/2026-08-05-s2-yururluk-alani.md)

> hakem **$0,0407** (yeniden koşu + etiket denetimi) · korpus yedeklendi · indeks **yeni
> dizine** kuruldu (`mevzuat_bge_m3_s2`), eskisi duruyor ki S2 öncesi sayılar üretilebilsin.

⭐ **Kapsam menüden değil ÖLÇÜMDEN seçildi.** Soru *"korpus ne kadar bozuk"* değil,
**"modelin GÖRDÜĞÜ bağlamda çöp var mı"** diye soruldu (`context_shown` ayrıştırıldı):

| bozulma sınıfı | korpusta | **modele ulaşan blok** | karar |
| :--- | ---: | :--- | :--- |
| **A — tablo/cetvel parçası** | ~7.966 satır | **0 / 800** ❌ | **ertelendi → borç B9** |
| **B — alt-madde soneki** | 485 satır | **14 / 800 · 12 soru** ✅ | ✅ yapıldı |

Sınıf A'yı elemek *ölçülemez bir kazanç için ölçülmüş bir sayıyı harcamak* olurdu.
⚠️ *"Anahtar yinelenmesi"* (%29,4) ile *"bağlam kirlenmesi"* (%1,8) **aynı şey değil** —
retriever yinelenen anahtarın **doğru** satırını getiriyordu.

**Yapılan** ([`korpus_yururluk.py`](scripts/korpus_yururluk.py), atomik yazma): `mulga` +
ilga eden kanun/madde/tarih **2.547 satır** (%99,6 kaynaklı) · alt-madde kimliği **485
satır** · `atif_dogrula.py`'ye **`MULGA`** hükmü (`red_kapisi` değişmedi).
**Kabul 3/3 ✅:** `1475/15` MULGA · `1475/14` yürürlükte · *"İş Kanunu Madde 15"* katı kapıda
**REDDEDİLDİ** · yanlış-pozitif 0.

**Sonuç:** A1 **0,7681 → 0,8042** · kütle **%59,5 → %61,3** · bozuk blok **14/800 → 0/800**.

⚠️ **İki dürüst kayıt:**
1. **Atıf kanalında etki SIFIR** — `MULGA` **0**, hükmü değişen cevap **0/80**. B7 bir
   **ürün-güvenliği** özelliği, bir skor özelliği değil.
2. **Erişim kanalında etki sıfır DEĞİL** — +3,6 puan A1. Ön-kayıtlı tahminim (*"kütle
   %59,5 ± 1"*) **tutmadı** ve gerekçesi de yanlıştı: gömülen metin değişince **getirilen
   bağlam da** değişti, A1 bağlam üzerinden ölçülüyor.

🐞 **İki kural verify hedefine çarpıp düzeldi** (ikisi de sessizce yanlış veri üretecekti):
sonek kuralı **%80 eksikti** (en sık sonek büyük `/A`; 98 sanılan sınıf gerçekte **485**) ·
ilga kaynağı **tarihi kanun sanıyordu** (`"22/5/2003/4857/120 md."` → `2003/4857`).

🚨 **Sonradan düzeltilen kendi hatam:** *"eval etiketleri düzeltilmedi, gerek kalmadı"*
**yanlıştı**. Anahtar yaşıyor ama **iki satırdan yanlış olanı** gösteriyordu. Kural-tabanlı
tarama **5** şüpheli buldu; kör hakem + konum-yanlılığı kontrolü **3'ünü düzeltti**
(id 0/74/76). İnsan onayıyla uygulandı. ⚠️ Düzeltme **manşeti yükseltmedi** (altın etiket
A1'e girmiyor); yalnız `recall@10` 0,8625 → **0,8750** ve B1 sınıfı 8 → **7**.

### ✅ S4 — İsabet denetimi tasarımı *(borç B1)* · **KAPANDI 2026-08-05 — kod açılmadı** · [ADR-0055](docs/adr/0055-isabet-denetimi-ekseni.md)

**Karar: isabet denetimi cevap-SONRASI örtüşme ekseninde değil, cevap-ÖNCESİ
KAYNAK-YETERLİLİĞİ ekseninde kurulur.**

Gerekçe S1+S3'ün birlikte ölçtüğünden çıktı: **B1 ile aşırı-red aynı madalyonun iki yüzü** —
biri yetersiz kaynakta cevaplıyor (**7/80**), diğeri yeterli kaynakta çekiniyor (**16/80**).
Tek bir eksik sinyal iki hatayı birden üretiyor.

❌ **Reddedilen (A) — cevap↔kaynak örtüşme denetimi:** B1'in **çekirdek vakasında kör**
(model *başka bir gerçek maddeden* cevaplıyor, örtüşme yüksek çıkar). Üstelik uydurma madde
no **0/118 ölçüldü** → denetimin sınıfı zaten **boş**. *Ölçülmüş boş bir sınıfa deterministik
denetim yazmak, S2'de sınıf A'yı elemekle aynı hata olurdu.*

🔁 **Ayrı tutulan (C) — ikinci geçiş yeniden-sıralama:** isabet denetimi değil **erişim
iyileştirmesi**; dikkat dağılmasının olası çaresi, ama aynı turda ölçülürse hangisinin
kazandırdığı ayrılamaz → **kendi turu, kendi ön-kayıtlı tahmini**.

**İlk deney bedeli sıfır:** `--sufficiency-preamble` bayrağı **zaten var**. Ön-kayıtlı kabul:
*kütle artar **ve** çekinme sıralaması belirsiz alt kümede ayırt ediciyi geçer*; düşerse B-i
elenir, çapraz-kodlayıcıya geçilir.

---

> **Bu belge icra dokümanıydı; sprint kapandığı için artık KAYIT.** Aşağısı üretildiği
> hâliyle duruyor — kararların gerekçesi ve *o gün ne bilindiği* audit izidir.
>
> ### ⭐ HER KOŞUDAN ÖNCE OKU
> [`docs/record/yurutme-tuzaklari.md`](docs/record/yurutme-tuzaklari.md) — bu hattın hata sınıfı
> **çökme değil, sessiz yanlışlık**. Sprint 2 buraya **6.10 · 6.11 · 6.12**'yi,
> **Sprint 3** ise **2.16 · 7.5 · 7.6**'yı ekledi.

---

## 📌 BU BELGE ARTIK KAYIT

⚠️ **2026-08-05'te sprint kapandı; canlı iş kalmadı.** Belgenin tek canlı bölümü
[POST-SPRINT 3 SIRASI](#-post-sprint-3-sırası) — yeni turun hangisi olacağı **insan kararı**
ve **yeni bir `/goal` ister**. Diğer her şey kayıt: üzerine yazılmaz, çelişki çıkarsa
**her iki yerde de işaretlenir**.

Sprint boyunca uygulanan kural (sonraki sprintler de aynısını uygular):
**adım başlarken** 🟡 KOŞUYOR + ne koşuyor · **adım biterken** ✅/🔴 + **fiili sayılar** +
çıktı nerede + hangi kayıt · **karar insana gittiğinde** aynı gün ADR + `research_log`.

*Sohbette kalan bulgu, kaybolmuş bulgudur.*

<details>
<summary><h2>📚 ARŞİV — sprintin tasarım kararları, adımları ve ön-kayıtları (aç/kapa)</h2></summary>

> Buradaki her şey **kayıt**: hedefin kendisi, harness kararının gerekçesi, K1-K5 tasarım
> kararları, adım adım icra, S3a ön-probu, reddedilen Adım 0 ve rejim değişmezleri.
> Üzerine yazılmaz. Sadeleştirme 2026-08-05'te yalnız **görünürlüğü** değiştirdi, içeriği değil.

## 🎯 HEDEF — ✅ **SAĞLANDI 2026-08-04** *(kayıt)*

```
koşul     : harness kuruldu (retriever + atıf doğrulayıcı + red kapısı) ve
            HARNESS AÇIK ölçüm yapıldı, harness kapalıyla yan yana raporlandı
🛑 DURMA  : kırmızı kapı · geçerlilik kapısı düşerse · bütçe aşımı
            · ⛔ tasarım kararları çözülmeden kod yazılmaz (aşağıda)
kapsam    : adım 0-4.  Graph-RAG, ajanlar, vatandaş kipi bu hedefin DIŞINDA
bedel     : GPU $0 (harness CPU'da) · hakem ~$1 · gömme modeli indirme
```

## Neden harness — karar gerekçesi (insan, 2026-08-03)

> ### ⚠️ 2026-08-04 — bu dört gerekçe ÖLÇÜLDÜ, ikisi ayakta değil
>
> Metin **olduğu gibi bırakıldı** (karar o gün bu gerekçelerle verildi, kayıt bu).
> Ölçümün hükmü:
>
> | # | gerekçe | hüküm |
> | :-- | :--- | :--- |
> | 1 | ortada ürün yok | ✅ **doğruydu** — retriever kuruldu, kullanıcı artık madde yapıştırmıyor |
> | 2 | iki açığı **kod** kapatır | ❌ **A1 ayağı ÇÜRÜDÜ** · ⏸ **M2b ayağı sınanmadı** |
> | 3 | şimdi eğitmek yanlış dağılıma eğitmek olur | ❌ **ZAYIFLADI** — retriever bağlamı daha *az* tuzaklı çıktı |
> | 4 | canlı mevzuat = kategori farkı | ⏸ **SINANMADI** — canlı katman kurulmadı (borç B6) |
>
> **2 neden çürüdü:** *"A1 0,909 → atıf doğrulayıcı uydurulan madde numarası yakalar"*
> diyordu. Ölçüldü: **uydurulmuş madde numarası SIFIR** (harness açık 89/89 doğrulandı,
> kapalı 87/89 — kalan 2'si "ayrıştırılamadı", uydurma değil). Doğrulayıcının yakalayacağı
> bir şey yoktu; model numara uydurmuyor, bağlamdaki etiketi kopyalıyor. A1'in açığı
> fabrikasyondan **gelmiyormuş** — **14/80** soruda altın gelmeden *başka bir gerçek*
> maddeden cevaplanmasından geliyor. O atıf doğrulanır, kapıdan geçer, soruya uymaz
> → **borç B1**. `M2b` ayağı ise çürümedi, **harness açık m2b hiç koşulmadı**.
>
> **3 neden zayıfladı:** *"gerçek retriever ~5 gürültülü parça verecek"* deniyordu.
> Ölçüldü: retriever bağlamında A1 **0,9344**, elle kurulmuş çeldiricili m1 bağlamında
> **0,9087**. m1'in 4 hard-negative çeldiricisi retriever'ın 5 konusal maddesinden
> **daha** tuzaklıymış. *"Önce harness, sonra eğitim"* sıralamasının bu dayanağı düştü.
>
> > 🚨 **2026-08-05 — bu paragrafın sayısı iki kez düzeltildi.** (a) 0,9344 yanlış metrikle
> > üretilmişti, doğrusu **0,9230** (tuzak 2.16). (b) Daha önemlisi: bulgu **k'ya bağlıymış**.
> > `k=10`'da aynı sayı **0,8426 < 0,9087** — yani retriever bağlamı m1'in çeldiricili
> > bağlamından **daha az tuzaklı değil**, yalnız **k=5'te** öyleydi. *"3 neden zayıfladı"*
> > hükmü bu yüzden **geri alınıyor**: bağlam uzadıkça tuzaklılık artıyor ve bu ölçüldü
> > ([#54](docs/record/research_log/2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md)).
>
> Kaynak: [research_log #51](docs/record/research_log/2026-08-04-harness-acik-ilk-olcum.md)
> · düzeltme [#54](docs/record/research_log/2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md)

**1. Şu an ortada ürün yok.** Model çalışsın diye kullanıcının **mevzuat metnini
kendisi yapıştırması** gerekiyor. Vatandaş bunu yapamaz — hangi maddeyi arayacağını
bilse zaten asistana ihtiyacı olmazdı.

**2. Üç açığımızdan ikisini kod kapatıyor, eğitim değil.**

```
M2b 0,877 → red kapısı        doğrulanamayan atıf = cevap reddedilir   deterministik
A1  0,909 → atıf doğrulayıcı  uydurulan madde numarası yakalanır       deterministik
```

**3. Şimdi eğitmek yanlış dağılıma eğitmek olur.** Eval şu an modele temiz bir madde
veriyor; gerçek retriever ~5 gürültülü parça verecek. Modeli bugünkü girdiye göre
optimize edip yarın girdiyi değiştirmek işi iki kez yapmaktır.

**4. Kategori farkı.** Canlı mevzuat API'si çalışıyor. Harness'lı model **bugünün
mevzuatını** cevaplar; kapalı ağırlıklı rakipler cevaplayamaz. Model reçetesiyle
elde edilemeyecek üstünlük.

---

## ⛔ TASARIM KARARLARI — kod yazılmadan çözülür

### K1. Gömme modeli (embedder) — ✅ **ÇÖZÜLDÜ 2026-08-04** (S3a ön-probu)

**Karar: `BAAI/bge-m3`, BM25 ile RRF hibriti içinde.** Ölçümle seçildi, etiketle değil.

| yöntem | recall@10 | recall@20 | kaçan (80'de) |
| :--- | ---: | ---: | ---: |
| BM25 | 0,625 | 0,750 | 20 |
| `intfloat/multilingual-e5-base` | 0,700 | 0,750 | 20 |
| `BAAI/bge-m3` | 0,800 | 0,863 | 11 |
| ⭐ **hibrit** (BM25 + bge-m3, RRF) | **0,875** | **0,925** | **6** |

BM25 tek başına en zayıf ama hibritte bge-m3'e **+0,075** ekliyor — iki yöntem farklı
soruları kaçırıyor. Maliyet: bge-m3 CPU'da indeksleme ~2-3 sa (bir kerelik), sorgu anında
kaba kuvvet arama **8,2 ms** / indeks **83 MB** fp16 → **vektör veritabanı gerekmiyor**
(bu ölçekte ANN bile gereksiz; gerekçe research_log #49 §7).

⚠️ **Sayılar bu soru kümesinin tavanı, retriever'ın değil** — aşağıya bak (S3a sonucu).

### K2. Chunk birimi — ✅ **ÇÖZÜLDÜ** ([ADR-0054](docs/adr/0054-harness-tasarim-kararlari-k2-k5.md))

**Tam madde indekslenir; 900 karakter kırpması yalnız bağlam modele verilirken uygulanır**
— yani bugünkü eval'de uygulandığı noktada. Eval-ayna kuralının öznesi **modelin girdisi**,
indeks değil; indeksi de kırpmak uzun maddelerin sonundaki hükümleri **aranamaz** yapardı.

**Bedel (kabul edildi, ölçülecek):** retriever'ın eşleştiği metin ≠ modelin gördüğü metin.
*"Getirildi ama cevap kırpılan kısımdaydı"* vakası harness-AÇIK tablosunda **ayrı sayılır**.
**Yan sonuç:** S3a sayıları tam madde üzerinde ölçüldü → aynen geçerli.

### K3. Statik korpus mu, canlı API mi — ✅ **ÇÖZÜLDÜ** (statikle başla)

Harness `data/corpus/mevzuat_maddeler.jsonl` üzerine kurulur; canlı `bedesten` katmanı
S3'ten **sonra**. Gerekçe ölçüm tekrarlanabilirliği — canlı içerik koşular arasında
değişirse harness-AÇIK sayıları kıyaslanamaz. S3a sözleşmenin geçerli olduğunu doğruladı,
yani bu bir **risk** değil **sıralama** kararı.

### K4. ⭐ HARNESS AÇIK ölçüm protokolü — ✅ **ÇÖZÜLDÜ** ([ADR-0054](docs/adr/0054-harness-tasarim-kararlari-k2-k5.md))

**`core_hard.jsonl` DEĞİŞTİRİLMEZ.** Her soruya *"kendi başına ayırt edici mi"* etiketi
eklenir, harness sayıları **iki alt kümede ayrı** raporlanır. Etiket **erişim sonucundan
kör** bir hakemle atanır (hakem soruyu görür, altın maddeyi ve retriever'ın onu bulup
bulmadığını görmez); istem etiketleme koşulmadan önce yazılır.

Neden küme değiştirilmiyor: sayı görüldükten sonra küme değiştirmek *"cilaladılar"* diye
okunur — tuzak 6.9'un veri tarafındaki karşılığı: **sonucu gördükten sonra ölçüt değil
alet düzeltilir.** Etiket kümeyi değiştirmeden aleti keskinleştiriyor.

⚠️ **Kaydedilen çekince:** bu ekseni ölçme fikri sonuçtan doğdu (kaçan sorular görülerek).
Ayrım korunuyor: ölçülen büyüklük ön-kayıtlı değil, ama **alet sonuca göre ayarlanmadı**.

Aşağıdaki ölçüm tasarımı yürürlükte:

Mevcut modlar modele bağlamı **doğrudan** veriyor: m1 altın madde · m2 yanlış madde ·
m2b çeldiriciler. Harness açıkken bağlamı **retriever** belirler. Bu **yeni bir
ölçüm** ve tasarlanması gerekir:

```
soru → retrieve(k) → model cevaplar → atıf doğrula → kapı → cevap / red
```

Ölçülecekler:
- **recall@k** — retriever altın maddeyi buluyor mu (modelden bağımsız)
- **uçtan uca** — DEV sorularında, oracle bağlam yerine getirilen bağlamla
- **kapı isabeti** — korpusta cevabı olmayan sorularda kapı reddediyor mu

⚠️ Harness açık/kapalı sayılar **yan yana** raporlanır; harness kapalı olan
tarihî çıpalarla (base · Gemini · `τ_g` · `τ_a`) kıyaslanabilirliği korur.

### K5. Red kapısı eşiği

[ADR-0038](docs/adr/0038-red-kapisi-esigi-kati.md): **katı** — tek doğrulanamayan
atıf tüm cevabı reddettirir. Karar duruyor; harness açıkken **aşırı-red** yaratıp
yaratmadığı ölçülecek (kütle ekseni).

---

## ▶ ADIMLAR

```
S3a) ÖN-PROB                ✅ KAPANDI  hibrit recall@10 0,875 · bedesten GEÇERLİ
0) MODÜL-BAŞINA NORM        🔴 REDDEDİLDİ  kütle ≤ %56,2 < %71,6 · hakem $0
1) RETRIEVER                ✅ BİTTİ    bileşen + indeks, recall@10 0,8750 birebir
2) ATIF DOĞRULAYICI         ✅ BİTTİ    deterministik, hakemsiz · 4+1 sessiz hata düzeltildi
3) RED KAPISI               ✅ BİTTİ    ADR-0038 katı + 2 ablasyon
4) HARNESS AÇIK ÖLÇÜM       🛑 ÖLÇÜLDÜ  ürün sayısı ilk kez görüldü → İNSANA SUNULDU
```

### 🛑 Adım 4 sonucu — harness AÇIK ↔ KAPALI, aynı model (`tgta_v1`)

> 🚨 **2026-08-05 düzeltmesi:** aşağıdaki A1/kütle sayıları **yanlış metrikle** üretilmişti
> (tuzak **2.16** — `A1` diye ham makro). Tablo **kayıt olarak duruyor**, doğruları üstü
> çizili yanına yazıldı. Ürünün güncel ayarı **k=10** — güncel tablo [S1'de](#s1--k-süpürmesi-borç-b3--kapandı-2026-08-05--k10-kabul--research_log-54).

| eksen | harness **KAPALI** (m1) | harness **AÇIK** (h1, k=5) |
| :--- | ---: | ---: |
| altın madde bağlamda | **garanti** (kurgu) | **60/80** — `recall@5` 0,750 |
| coverage | 0,7875 | **0,7500** |
| A1 (cevaplanan-only) | 0,9087 | ~~0,7823~~ → **0,7591** |
| **kütle = coverage × A1** | **%71,6** | ~~%58,7~~ → **%56,9** |
| ⭐ A1 · **altın getirilen** alt küme | 0,9087 | ~~0,9344~~ → **0,9230** |
| doğrulanan atıf | 87/89 | **89/89** |
| **uydurulmuş madde numarası** | 0 | **0** |
| katı kapı reddi | 2/80 | **1/80** |

**Üç okuma** (tamamı [research_log #51](docs/record/research_log/2026-08-04-harness-acik-ilk-olcum.md)):

1. **Ürün sayısı oracle sayısından düşük — ve olması gereken bu.** Düşüşün tamamı erişimden:
   soruların %25'inde altın madde ilk 5'e girmiyor. Ölçüm dürüstleşti.
2. ⭐ **Retriever doğru maddeyi bulduğunda model DAHA sadık** (A1 0,9344 > 0,9087). Yani
   *"gerçek retriever daha gürültülü bağlam verir"* varsayımı — S3'e girerken yazdığımız
   gerekçelerden biri — **bu ölçümde doğrulanmadı**. Darboğaz model değil **erişim**.
3. ⚠️ **Kapının sınırı.** Model madde numarası **uydurmuyor** (0/89), bağlamdaki etiketi
   kopyalıyor; bu yüzden katı kapı yalnız 1 cevap reddetti. Asıl hata şurada: **14/80**
   soruda altın gelmeden cevaplandı — atıf **gerçek**, doğrulanır, kapıdan geçer, ama
   soruya uymuyor. Atıf doğrulayıcısı *"uydurulmuş atıf"*ı çözüyor, *"gerçek ama soruya
   uymayan madde"*yi çözmüyor. **S3'ün asıl açığı bu.**

```
altın geldi   → cevapladı   46
altın geldi   → çekindi     14
altın GELMEDİ → cevapladı   14   ← A1'i düşüren sınıf
altın GELMEDİ → çekindi      6
```

### S3a — ÖN-PROB · $0 · ~1 gün · ⭐ ÖNCE BU

1-2 aylık bir sprinte girmeden **planın iki temel varsayımını** sınar. İkisi de model çağrısı,
hakem ve GPU **gerektirmez**.

#### Prob 1 — `recall@k`: retriever altın maddeyi buluyor mu

DEV soruları maddelerden üretildi; her sorunun altın `kanun_adi + madde_no`'su **biliniyor**.
Saf bilgi-erişim ölçümü.

**Sırayla, ucuzdan pahalıya:**

```
1. BM25             gömme YOK · indeks dakikalar · TAMAMEN BEDAVA
2. multilingual-e5  CPU · model indirme
3. bge-m3           CPU · uzun bağlam
4. hibrit           BM25 + yoğun — ilk üçü yetmezse
```

> **BM25 neden ilk:** hukuk metni ayırt edici terimlerle dolu (kanun adları, madde numaraları).
> Sözlüksel arama burada beklenenden güçlü olabilir ve **taban çizgisi** kurar. Yoğun gömme
> BM25'i geçemiyorsa gömme modeli seçmenin anlamı yok. *(Bu aynı zamanda K1'i çözer.)*
>
> ⚠️ **2026-08-04 — öngörü tersine çıktı.** BM25 *"beklenenden güçlü"* değil, **en zayıf**
> yöntem oldu: `recall@10` **0,625** — ön-kayıtlı **"<%70 → DUR"** bölgesinde. Yoğun gömme
> onu her k'da geçti (bge-m3 0,800). **Ama merdivenin mantığı yine de işe yaradı:** BM25 tek
> başına zayıfken hibritte bge-m3'e **+0,075** ekledi (0,800 → **0,875**) — iki yöntem
> **farklı** soruları kaçırıyor. Yani *"taban çizgisi kur"* gerekçesi tuttu, *"tek başına
> yetebilir"* öngörüsü tutmadı.

**⛔ ÖN-KAYITLI KARAR EŞİKLERİ — sayı görülmeden yazıldı:**

| `recall@10` | S3 ne olur |
| :--- | :--- |
| **≥ %90** | plan tarif edildiği gibi koşar |
| **%70-90** | **hibrit** eklenir, S3 büyür |
| **< %70** | 🛑 **DUR, insana sor** — sorun korpus yapısında, S3'e girilmez |

`recall@1/5/10/20` eğrisi de çıkarılır → modele kaç parça verileceğini o belirler.

#### Prob 2 — bedesten sözleşmesi hâlâ geçerli mi

```
scripts/bedesten_probe.py  →  arama · tam metin · madde ağacı
⚠️ Türk IP gerekiyor (gov firewall)
```

Güncellik iddiamızın **tek dayanağı** bu ve sözleşme 2026-06-07'den beri doğrulanmadı.
Değişmişse: retriever statik korpusla sürer ama **güncellik iddiası DÜŞER** →
[`ROADMAP.md`](ROADMAP.md) + [`MODEL_CARD.md`](MODEL_CARD.md) düzeltilir.

#### 📋 Uygulama planı hazır

[`docs/plans/2026-08-03-s3a-on-prob.md`](docs/plans/2026-08-03-s3a-on-prob.md) — 5 görev,
TDD adımlarıyla, gerçek kodla. İlk görev **madde anahtarı normalleştirme**: altın etiketi
korpusa bağlayan çekirdek, kendi testleriyle. *(Plan yazılırken burada bir hata bulundu:
`Geçici Madde 1` ile `Madde 1` aynı sayılınca 40.496 madde 27.706 anahtara düşüyor ve
recall sessizce şişiyor — test olarak çivilendi.)*

⚠️ **S3'ün planı YAZILMADI, bilinçli.** S3a'nın sonucu S3'ün şeklini belirliyor; probu
koşmadan S3 planı yazmak, probun engellemek için var olduğu şeyi yapmak olur.

#### S3a çıkış ölçütü — ✅ **KAPANDI 2026-08-04**

```
✅ recall@1/5/10/20 eğrisi ölçüldü, en iyi yöntem seçildi (K1 çözüldü)
✅ eşik kararı verildi ve S3'ün boyutu buna göre kesinleşti
✅ bedesten sözleşmesi sınandı, sonucu kayda geçti
→ research_log #49 · çıktılar outputs/eval/s3a-on-prob/
```

**Eşik kararı: `recall@10` = 0,875 → %70-90 bandı → 🟡 HİBRİT, S3 büyür.**
Merdivenin 4. basamağı S3a içinde koşulduğu için "S3 büyür" = **retriever hibrit olur**,
ayrı bir keşif turu değil.

**Bedesten: ✅ GEÇERLİ** (4/4 çağrı `SUCCESS`, İş Kanunu M1 `guncellemeTarihi` 2026-05-07)
→ güncellik iddiası ayakta, `ROADMAP.md`/`MODEL_CARD.md` düzeltmesi **gerekmiyor**.
⚠️ Prob betiğinin kendisi bozuktu (`documentId` arıyordu, alan `mevzuatId`) ve API
çalışırken *"sözleşme bozuk"* raporluyordu — düzeltildi, **tuzak 7.1**.

#### ⭐ S3a'nın planlanmamış bulgusu — insana

**DEV soru kümesi erişim ölçümü için yetersiz belirlenmiş.** Kaçırılan soruların hemen
tamamı hangi kanuna ait olduğunu söylemiyor (*"Başvurum kabul edilirse ne olur?"*,
*"El konulan gönderilerim ne olacak?"*). Ölçüldü: aynı BM25, aday havuzu altının **kendi
kanunuyla** sınırlanınca `recall@10` **0,625 → 0,875**.

`core_hard.jsonl` altın madde elde tutularak üretildi — **grounded QA kümesi, retrieval
kümesi değil.** Sonuç: `recall@k` sayılarımız retriever kabiliyetinin değil **bu kümenin**
tavanı. → **tuzak 7.4**, ve **K4'ü (harness-AÇIK protokolü) doğrudan etkiliyor**:
protokol bu kümeyle mi kurulacak, yoksa ayırt edici sorulardan oluşan bir alt küme mi
gerekiyor? ⚠️ Sayı görüldükten sonra küme değiştirmek dışarıdan *"cilaladılar"* diye
okunur — **karar insanın, ADR'ye yazılır.** Öneri: küme **değiştirilmez**, yanına
"kendi başına ayırt edici mi" etiketi eklenir, sayılar iki alt kümede **ayrı** raporlanır.

---

### Adım 0 — modül-başına normalleştirme *(harness'tan bağımsız, önce yapılır)*

Merge'in **bilinen** kusuru: `τ_a` seyreliyor (tekil 0,987 → merge 0,877).
Normalleştirme şu an **global** (tek `‖τ‖_F`). Ölçüldü: iki kolun da en büyük normu
**aynı MLP yüzeyinde** — `gate_proj` (τ_g 6,150 ↔ τ_a 0,621) · `up_proj`
(5,047 ↔ 0,628). Global norm bunu göremiyor.

```
python scripts/merge_ties.py --base Qwen/Qwen3.5-4B \
  --adapter tg=outputs/tg_v1 --adapter ta=outputs/ta_v1 \
  --norm-kapsam modul ...                       ← ~20 satır, henüz YOK
bash scripts/cp3_merge_dene.sh models/merged/<yeni> modul
```

**Kabul:** M2b > 0,877 **ve** M1 kütlesi ≥ %71,6 (ikisi birden — tek eksen yeter değil).
Tutmazsa `v0.1` yerinde kalır, kayıp 1 saat. `open_questions.md`'de açık soru olarak
duruyor.

#### 🔴 KAPANDI (2026-08-04) — reddedildi · [ADR-0053](docs/adr/0053-modul-basina-norm-kapsami-reddedildi.md) · research_log #50

`--norm-kapsam {global,modul}` **yazıldı** (`scripts/merge_ties.py`), merge koştu (224/224).

**① Adım 0'ın gerekçesi ölçümde durmuyor.** *"İki kolun da en büyük normu aynı MLP
yüzeyinde, global norm bunu göremiyor"* — ölçüldü: kolların modül profilleri neredeyse
**orantılı**, τ_g/τ_a oranı 11 yüzeyin hepsinde **7,2–10,1**. Global normalleştirmeden
sonra payları zaten eşitleniyor (τ̂_a/τ̂_g = **0,88–1,24**). Yani `τ_a` bir **kapsam
artefaktı** yüzünden silinmiyor.

**② Ama modül-başına kapsam yine de no-op değil** — ölçüldü, ağırlık uzayında:
`‖W_modül − W_global‖ / ‖W_global − base‖` = **0,272**. Yön %27 değişiyor, **genlik
değişmiyor** (‖Δ‖ 1,3835 ↔ 1,3865). Farkın kaynağı TIES'in doğrusal-olmayan işaret
seçimi. Bu yüzden eval **koşuluyor** — akıl yürütmeyle değil ölçümle kapanacak.

**Bütçe sırası:** kabul bir **VE** koşulu ve genlik `min`'le aynı olduğu için düşmesi
beklenen eksen **kütle**. Bu yüzden önce **yalnız m1** koşuluyor; kütle düşerse m2b/m2
üretimi ve hakem parası harcanmıyor.

**③ SONUÇ 🔴 — kabul ölçütü düştü, hakem hiç çağrılmadı.** Geçerlilik kapısı geçildi
(kesik %1,2). Cevaplanan **45/80** → coverage **%56,2**. Kütle = coverage × A1 olduğundan,
**A1 = 1,000 olsa bile** kütle ≤ %56,2 < gereken **%71,6**. A1'i ölçmek sonucu
değiştiremezdi → m2b/m2 koşulmadı, **hakem maliyeti $0**.

| varyant | cevaplanan | A1 | **kütle** | M2b red |
| :--- | ---: | ---: | ---: | ---: |
| `ham` = yayınlanan `tgta_v1` | 63/80 | 0,909 | **%71,6** | 0,877 |
| `min` (global norm-dengeli) | 43/80 | 0,994 | **%53,4** | 0,987 |
| **`modulmin`** (bu adım) | **45/80** | ölçülmedi | **≤ %56,2** | ölçülmedi |

Modül-başına kapsam global `min`'i **tekrarladı**. %27'lik yön farkı aşırı-reddi
kurtarmadı — çünkü aşırı-reddi yaratan **yön değil genlik**: her iki kapsamda da `τ_g`
kendi eğitim genliğinin ~1/9'una iniyor ve zeminleme zayıflıyor.

**`v0.1` yerinde kalıyor.** `--norm-kapsam` bayrağı kodda kaldı (varsayılan `global`).
⚠️ `τ_a`'nın merge'de seyrelmesi **hâlâ açık** — çözüm merge parametresinde değil,
muhtemelen `τ_a`'nın **eğitim genliğinde** (82 adım @1e-5 çok kısaydı).

---

## Değişmezler

```
ölçüm     thinking on · 1024+512 · seed 3407 · chunk 900 · Q4_K_M + llama-server
havuz     data/eval/dev/ — DEV. frozen TEST (data/eval/canon/) sürüm kabul testi,
          yayın öncesi BİR KEZ
hakem     gpt-4o-mini · kapı openrouter · LLM_PROVIDER_ORDER=OpenAI PİNLİ
harness   CPU'da — gömme, indeks, doğrulayıcı GPU'ya GİRMEZ (sığar/sığmaz farkı)
🛑 geçerlilik kapısı: kesik > %5 → koşu geçersiz, puanlamaya para harcanmaz
```

> ### 🚨 TEK EKSENLE OKUMA — Sprint 2'nin en pahalı dersi
> A1 **cevaplanan-only**; çekinerek kazanmayı ödüllendirir. Ölçüldü: `τ_a` A1
> **0,9697** (en yüksek) ama kütle %41,2 · dejenere merge A1 **1,0000** (tavan) ama
> 80 sorudan **2'sini** cevaplıyordu.
>
> **Her tabloda kütle = coverage × A1.** Red kapısı **tanımı gereği** aşırı-red
> üretebilir — bu eksen olmadan kapı "başarılı" görünür.

> ### 🚨 Geçerlilik kapısı düşerse reçeteye körü körüne uyma
> Kapı *"`MAXTOK` büyüt"* der. Sprint 2'de kesiklerin tamamı **tekrarlama
> döngüsüydü** — bütçe darlığı değil model hasarı. Ayrıca `MAXTOK` bir **rejim
> değişmezi** (ADR-0043). **Önce kesikleri gözle oku.**

---

## Koşu öncesi kısa liste

- [ ] Modal panelden bakiye (defterden türetme — 6.3) · **kalan ~$22,31**
- [ ] Eklenen her bayrak **çağrı zinciri uçtan uca** izlendi mi: betik →
      orkestratör → komut → **künye** (6.12: Sprint 2'de **dört kez** ısırdı)
- [ ] Eval sonrası: kesik oranı %5 altında mı · **kütle** A1'in yanında mı
- [ ] Her bulgu **aynı gün** `research_log` + gerekirse ADR (numaralandırma
      **0053**'ten, `research_log` **#49**'dan devam)

</details>

## Bağlantılar

| ne | nerede |
| :--- | :--- |
| Ürün yol haritası | [`ROADMAP.md`](ROADMAP.md) · [`docs/VISION.md`](docs/VISION.md) Faz 2 |
| Model kartı ve sınırlar | [`MODEL_CARD.md`](MODEL_CARD.md) |
| Artefakt kimlikleri | ⭐ [`docs/record/kollar.md`](docs/record/kollar.md) |
| Mevzuat API sözleşmesi | [`docs/BEDESTEN_API.md`](docs/BEDESTEN_API.md) |
| Sprint 2 kapanışı | [`sprint2.md`](docs/_arsiv/sprint2.md) · [`defter.md`](docs/record/sprint2/defter.md) |
| Ertelenen iddia katmanı | [`sprint2b.md`](docs/_arsiv/sprint2b.md) — arxiv'e karar verilirse |
| **Koşu öncesi tuzaklar** | ⭐ [`yurutme-tuzaklari.md`](docs/record/yurutme-tuzaklari.md) |
