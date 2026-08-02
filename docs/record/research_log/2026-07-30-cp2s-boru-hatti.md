# #47 — CP2-s: boru hattı smoke'u, **yazılmamış bir kodu** buldu · TIES'te işaret hatası · iki yeni tuzak

**Tarih:** 2026-07-30 · **Checkpoint:** `sprint2.md` CP2-s · **Modal GPU:** ~$0,20 · **Hakem:** $0
**Karar belgesi:** [ADR-0049](../../adr/0049-sprint2-kalan-kararlarin-kilitlenmesi.md) m.4
**Çıktı:** `outputs/eval/cp2-s-boru-hatti-smoke/` (+ `KUNYE.json`)
**Yazılan betik:** ⭐ `scripts/merge_ties.py` · **düzeltilen:** `scripts/train_orpo.py` (veri kapısı)

> ### 🚨 Bu turun hiçbir sayısı performans çıpası DEĞİLDİR
> ADR-0049 m.4 smoke'u kasten *mekanik* tanımladı: ölçtüğü şey **"çalışıyor mu"**, *"iyi mi"*
> değil. Okunabilir bir performans sayısı üretmemesi **tasarım gereğidir** — eşikler yeniden
> türetilmişken böyle bir sayı çıpalama riski taşır.

---

## Sorulan soru

`τ_a` eğitilip `τ_g` ile birleştirilip servis edilebiliyor mu? Zincir dört halkalı ve Sprint 3'ün
**8 kafes hücresi** ile ARA KAPI'nın 2. gözlemi bu zincirin üstünde duruyor.

## ⭐ Asıl bulgu: ikinci halka **hiç yoktu**

`merge_lora.py` **tek** adaptörü base'e katıyor. **Norm-dengeli k-yollu TIES yazılmamıştı.**
Yani Sprint 3'ün kafesi ve ARA KAPI'nın merge onarım kontrolü, var olmayan bir koda dayanıyordu —
ve bu, `τ_a` eğitilip ~$4 harcandıktan sonra fark edilecekti.

`scripts/merge_ties.py` yazıldı. ADR-0027/0036'nın gerektirdikleri:

- **eşzamanlı k-yollu** (iteratif değil): kırp → işaret seç → ayrık ortalama, **hepsi k vektörün
  tamamı üzerinde bir kerede**
- ΔW **bf16**'da materyalize, **tam ağırlık uzayında** birleştirme
- **ana RAM'de, tensör tensör akıtmalı** — asla GPU'da
- her `τ` **birim Frobenius normuna** indirilir, sonuç normların **ortalamasıyla** geri ölçeklenir
- `--no-norm-balance` ham TIES ablasyonunu koşar
- `‖τ‖_F` **koşulsuz** ölçülür, modül kırılımıyla künyeye yazılır
- iki **sessiz-bozulma kapısı**: kolların LoRA hedefleri ayrışırsa DUR · eksik uygulama varsa DUR

## Operatörün doğrulanması — biri **başarısız çıktı**

Gerçek koşudan önce, $0'a, sentetik tensörlerde (seed 3407):

| # | özellik | sonuç |
| :-- | :--- | :--- |
| 1 | `TIES(τ,τ)` ≈ kırpılmış τ | ✅ sıfırdışı **0,199** (beklenen 0,20) · max sapma 3,08e-02 = bf16 yuvarlaması |
| 2 | `TIES(τ,−τ)` = 0 | ❌ → ✅ **hata bulundu ve düzeltildi** |
| 3 | norm-dengeleme küçük kolu kurtarıyor | ✅ **0,656 → 0,734** |
| 4 | eşzamanlı ≠ iteratif | ✅ max fark **2,9766** |

### 2. testin anatomisi — gerçek bir tasarım hatası

İşaret toplamı **tam sıfır** olduğunda keyfi olarak `sign=+1` atıyordum. Sonuç: tam çakışan
kollarda (`τ` ve `−τ`) birbirini götürmesi gereken parametrelerde **sıfır yerine `|τ|`** —
yani **sistematik pozitif sapma**. Ölçülen: `|ortalama| = 1,023`.

**Düzeltme:** seçilmiş işaret yoksa güncelleme de yok (`merged = 0`). Sonrası tam sıfır.

Gerçek delta'larda tam eşitlik pratikte olmaz — ama **keyfi bir kırılımın sapması ölçülemez,
sıfırın sapması ölçülebilir.** Bu yüzden düzeltildi, "nadir" diye bırakılmadı.

### 3. test, ADR-0036'yı teoriden çıkarıp koda soktu

Norm-dengeleme küçük kolun işaretini izleme oranını **0,656 → 0,734**'e çıkarıyor. ADR-0036'nın
*"kütle-ağırlıklı sign election küçük-normlu kolu siler"* gerekçesi artık ölçülmüş.

## Zincirin diğer üç halkası

| halka | sonuç |
| :--- | :--- |
| **1. `τ_a` eğitimi** | ✅ Modal A100-40GB, 50 adım, `--fresh-adapter`. Eğitilebilir parametre **29.908.992 / 4.569.174.528 = %0,65** → 11 hedef modül (`in_proj_*` dahil) uygulandı |
| **3. GGUF** | ✅ f16 8,07 GiB → **Q4_K_M 2,59 GiB**, quantize 63 s. `PURE=0` (Qwen3.5-4B QAT değil). `merge_ties.py`'nin kopyaladığı config/tokenizer/chat_template dönüştürücüye yetiyor |
| **4. servis** | ✅ `llama-server` açıldı, **3/3 istek dolu cevap** döndürdü |

## Ölçülen norm değerleri + bir çapraz doğrulama

```
‖τ_tg‖_F = 10.472179     ← kayıtlı artefakt tau_norm_tg.json: 10.458926
                            %0,13 fark = bf16'da ΔW materyalize etmemden
                            → norm ölçümü BAĞIMSIZ olarak doğrulandı
```

Merge istatistikleri: `trim_k=0,20` · `geri_ölçek=5,526` · çatışan parametre **%0,16** ·
sıfır kalan **%67,3** (2 kol × %20 kırpma için beklenen).

> ### ⚠️ Bir tahmin, CP3'te ölçülecek
> Çatışma oranı **%0,16** düşük çıktı çünkü sentetik kol `τ_g`'nin ölçeklenmiş kopyası — yüksek
> korelasyon. **Gerçek `τ_g` ↔ `τ_a` çatışma oranı çok daha yüksek olmalı ve ADR-0036'nın asıl
> merak ettiği sayı O.**
>
> Norm asimetrisi de: sentetikte **18×**, ama gerçekte `adım × lr` kabası
> (`τ_g` 1083×1e-4 = 0,108 ↔ `τ_a` 73×1e-5 = 0,00073) **~148×** gösteriyor — sentetiğin 8 katı.
> Doğruysa norm-dengeleme sanılandan **çok daha ağır iş** yapıyor.

## İki yeni yürütme tuzağı — ikisi de "hata vermeden yanlış/hiç sonuç"

### `modal run` → `--detach` düşürüldü, iş **hiç koşmadı**

Terminal *"✓ App completed"* yazdı. Log ise yalnızca *"Stopping app — local entrypoint
completed"* içeriyordu: **hiçbir iş başlamamıştı, hata da yoktu.**

Sebep: `modal run` **efemer** bir app yaratır; yerel giriş noktası dönünce app kapanır ve
`spawn()` ile kuyruğa atılan iş **onunla birlikte ölür**. Ders **A4.1** zaten *"`spawn()` +
`--detach`"* diyordu — bayrak düşürülmüştü.

### `train_orpo.py`'de veri kapısı **yoktu**, `train_sft.py`'de vardı

`--data` bir **dizin** bekliyor (`train.jsonl` + `validation.jsonl`). Dosya yolu verilince
`load_dataset` `<dosya>/train.jsonl` arıyor ve patlıyor — ama bu, model **A100'e yüklendikten
sonra** oluyor. `train_sft.py` aynı denetimi **model yüklemeden önce** yapıyordu (satır 144-151);
`train_orpo.py` yapmıyordu. Boşa giden GPU dakikası ≈ $0,10.

Kapı `train_orpo.py`'ye eklendi. **CP3 aynı yolu kullanacak** — orada 20 dakikalık bir yükleme
boşa gitmeyecek.

## 🔴 Yan bulgu: eğitim hızı kayıtlının **10 katı yavaş** — CP3 bütçesi değişti

> ### ⚠️ DÜZELTME (2026-08-02, [#48](2026-08-02-cp2c-modal-koprusu.md))
> Aşağıdaki *"kayıtlı 7 s/it **yanlıştı**"* ifadesi **iki farklı rejimi** kıyaslıyor. Yanlış olan
> kayıt değil, kıyas:
> **6,8-7,0 s/it = SFT, efektif batch 16** (`τ_g`'nin gerçek 1.083 adımlık koşusu —
> `raft_scrubbed/train.jsonl` **17.323 satır ÷ 16 = 1.083 adım**, doğrulandı) ·
> **~70 s/it = ORPO, efektif batch 64** (bu smoke).
> **Sonuç: CP4/CP5'in SFT tahminleri (~$5,7 / ~$6,5) AYAKTA**; yalnız **ORPO** kalemleri ~**4×**
> pahalılaştı. Bu bölümün CP3 (ORPO) sayıları geçerli kalıyor.

Smoke'un progress bar'ı **60-81 s/it** gösterdi (medyan ~**70 s/it**). Kayıtlı değer CP5'ten
**6,8-7,0 s/it**'ti. 10× fark.

| | kayıtlı varsayım | **ölçülen** |
| :--- | --: | --: |
| s/it (etkin batch 64) | 7 | **~70** |
| CP3 = ~73 adım | ~9 dk | **~85 dk** |
| CP3 Modal maliyeti | ~$0,85 | **~$3,2** |

Ve smoke'un kendisi $0,20 değil, tamamlansa **~$2,4** olacaktı. **6/50 adımda durduruldu**
(~$0,35): mekanik soru zaten cevaplanmıştı — model yüklendi, LoRA doğru uygulandı (29.908.992 =
%0,65), veri okundu, ORPO kaybı hesaplandı (`loss 2.606`, `nll_loss 2.443`), optimizer adım attı,
ara commit çalıştı. 50. adıma gitmek **hiçbir mekanik bilgi eklemiyordu.**

⚠️ Kalan doğrulanmamış tek halka: **adaptörün volume'a yazılması** (`save_steps=100` olduğu için
50 adımdan önce kaydetmiyordu). Risk düşük — aynı kayıt yolu `train_sft.py`'de defalarca koştu
(`tg_v1` onunla üretildi) ve CP3 gerçek veriyle zaten o yolu kullanacak.

### Bunun bütçeye etkisi

Modal'da kalan **$7,27** (bkz. tuzak 6.3). Yeni tahminlerle:

| iş | eski tahmin | **yeni** |
| :--- | --: | --: |
| CP2-s *(fiili, durduruldu)* | 0,20 | **−0,35** |
| CP2-c hasat (Modal) | 3,00 | 3,00 |
| CP3 `τ_a` | 0,85 | **3,20** |
| **toplam** | 4,05 | **6,55** → $7,27'ye sığıyor ama **payı $0,7'ye** düşürüyor |

Bu pay, ilk 10 dakika kapısının tetiklenmesi hâlinde yeniden koşmaya yetmez. Sonuç: **CP2-c'nin
Modal'da koşması artık savunulabilir değil** ve ADR-0047'nin kendi geri-dönüş şıkkı devreye giriyor
(*"yerel `-np 8` … Modal koşusu tıkanırsa geri dönülecek seçenek olarak duruyor"*). Modal bütçesi
tıkanmadı ama **payı kalmadı** — aynı sonuç.

## 🔴 Yerel hasat ölçüldü ve **ELENDİ** — ADR-0047'nin geri-dönüş şıkkı kapandı

Modal payı kalmadığı için ADR-0047'nin *"yerel `-np 8` … Modal tıkanırsa geri dönülecek seçenek"*
şıkkı denendi. `cp2_harvest.py` eş zamanlı üretime alındı (`--concurrency`, `ThreadPoolExecutor`,
yazım kilidi) ve `llama-server` **8 slotla** (`-np 8 -c 16384`) açılıp ölçüldü:

| | s/üretim | kazanç |
| :--- | --: | --: |
| seri (tek slot) | 11,12 | — |
| **`-np 8`** | **8,23** | **1,35×** |

Beklenen 4-6×'ti. **Kazanç yok denecek kadar az.**

### Sebep ölçüldü: **zorunlu kapatma 9/9**

Her "üretim" aslında **iki istek**: (1) 1024 düşünce token'ı yakılır, `</think>` kapanmaz;
(2) iz + kapatma isteği yapıştırılıp `/completions` ile devam edilir — bu ikinci çağrı **3.933
karakterlik izi baştan prefill eder**. Prefill compute-bound ve slotlar arası iyi ölçeklenmiyor.

Bu düzeltilebilir bir kusur **değil**: base'in `</think>`'i kendi kapatmaması #42'de ölçülmüş bir
özellik, zorunlu kapatma da ADR-0043'ün **rejim değişmezi**. Ortalama 1.144 completion token
(+ ~1.000 prefill) → üretim başına ~2.150 token, toplam verim **~260 token/s**.

### Yerel süre tablosu (ölçülen 8,23 s/üretim · verim %10)

| hedef negatif | süre |
| --: | --: |
| **750** *(ADR-0047)* | **17,1 sa** |
| 500 | 11,4 sa |
| 350 | 8,0 sa |
| 200 | 4,6 sa |

**Karar (2026-07-30):** yerel hasat **elendi**. 750 negatif için 17 saat, iki geceye bölünse bile
(hasat `load_done` ile devam ettirilebilir) makul değil. Hasat, Modal bütçesi **1 Ağustos'ta**
yenilendiğinde **Modal'da** koşacak — yani **ADR-0047 m.2 doğrulandı**, geri-dönüş şıkkı ölçümle
kapandı.

**Modal tahmini** (ölçülen yerel verimden türetildi, ⚠️ ölçüm değil): A100 bant genişliği 4-6× +
prefill compute avantajı → ~10× → **0,7-1,4 üretim/s** → 7.500 üretim **1,5-3 saat**, ~**$3-6**.
ADR-0047'nin **ilk 10 dakika verim kapısı** tam bu tahmini denetler.

## Ders

**Bir smoke'un işi çalışan şeyi doğrulamak değil, olmayan şeyi bulmaktır.** Bu tur dört halkanın
üçünü doğruladı ve **birinin hiç var olmadığını** ortaya çıkardı — üstelik o halka, Sprint 3'ün
tamamının ve bir ön-kayıtlı kapının dayanağıydı. Maliyeti **$0,20 ve 25 dakika**; `τ_a` eğitilip
CP2-c'nin ~$3'ü harcandıktan sonra bulunsaydı bedeli çok daha yüksek olacaktı.

İkinci ders: **operatörün matematiksel özellikleri sınanabilir ve sınanmalı.** `TIES(τ,−τ)=0`
gibi bir özellik, gerçek ağırlıklarda asla fark edilmeyecek bir işaret hatasını üç satırda
yakaladı — çünkü gerçek ağırlıklarda çıktı *makul görünür.*

## Paper eşlemesi

- **Methodology / merge:** eşzamanlı k-yollu TIES'in implementasyonu + norm-dengeleme; operatör
  özellik testleriyle doğrulandı (özellikle sign-election tie-break kararı).
- **Limitations:** norm-dengeleme kapsamı **global** (`τ/‖τ‖`), modül-başına alternatifi
  değerlendirilmedi — kolların modül dağılımı çok farklıysa sonucu değiştirebilir.
- **Negatif bulgu / süreç:** ön-kayıtlı bir kapının (ADR-0045 m.2) dayandığı kod, kapı yazıldıktan
  **beş gün sonra** hâlâ mevcut değildi. Kapı tasarımı ile uygulama arasındaki bu boşluk mekanik
  bir smoke olmadan görünmüyordu.

## Yeni yürütme tuzakları

- **6.1 — `modal run` efemer app + `spawn()` = iş hiç koşmaz.** `--detach` zorunlu. Belirti:
  *"App completed"* ama logta yalnızca *"Stopping app"*. Kontrol: `modal volume ls <out>` ile
  çıktının gerçekten yazıldığını doğrula; "spawned" mesajı iş koştuğunu KANITLAMAZ.
- **6.2 — Veri kapısı model yüklemeden ÖNCE olmalı.** Aksi hâlde yol/format hatası GPU parasını
  yaktıktan sonra çıkar. `train_sft.py` doğru, `train_orpo.py` düzeltildi. Kural: her eğitim
  betiği girdi dosyalarını `os.path.isfile` ile **model yüklemeden önce** doğrular.
