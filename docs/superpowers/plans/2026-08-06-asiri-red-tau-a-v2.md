# Aşırı-red turu (B10) — `τ_a` v2 uygulama planı

> **Agentic worker için:** GEREKLİ ALT-BECERİ: `superpowers:subagent-driven-development` ya da
> `superpowers:executing-plans`. Adımlar `- [ ]` kutucuklu.
>
> ⚠️ **Kutucuk kuralı — 2026-08-06'da İNSAN KARARIYLA DEĞİŞTİ:** kutucuğu **ajan** işaretler.
> Bir adım ancak `→ verify:` çıktısı **gerçekten alındıktan** sonra işaretlenir; işaretli kutucuk
> *"koştu ve doğrulaması tuttu"* demektir, *"yapıldı sayılır"* değil.
> 🔁 **Eski kural (aynı gün, aynı insan):** *"kutucuğu insan işaretler, ajan yalnız raporlar."*
> İkisi de burada duruyor — [`CLAUDE.md`](../../../CLAUDE.md) §Dokümantasyon disiplini: bir karar
> eskisini değiştirince **çelişki iki yerde de işaretlenir**, sessizce üzerine yazılmaz.

**Spec:** [`specs/2026-08-06-asiri-red-turu-design.md`](../specs/2026-08-06-asiri-red-turu-design.md)
**Hedef:** Aşırı-reddi (**B10**, 14/80) `τ_a`'nın eğitim verisindeki tek-yönlü tercih baskısını
simetrikleştirerek düşürmek; ve rakip kıyasını ürün rejiminde ilk kez kurmak.
**Yaklaşım:** `τ_a` v2, aynı rejimle ama **iki yönlü** tercih verisiyle ham base'den eğitilir
(altın yokken çekin ↔ altın varken cevapla, **aynı kalıpta, aynı çeldirici profiliyle**), ham
TIES ile `τ_g` v1'e merge edilir, ön-kayıtlı iki kapıdan geçirilir.
**Yığın:** `uv` + Python 3.11 · llama.cpp/llama-server (Q4_K_M GGUF) · Modal A100 (ORPO) ·
`gpt-4o-mini` hakem (OpenRouter, sağlayıcı pinli) · `pytest`.

---

## 🔄 İCRA DURUMU — AÇIK (başladı 2026-08-06)

> Bu blok *"nerede kaldık, ne yaşandı, plan nerede yanlıştı"* yazar. **Sayılar kayda gider**
> (#57/#58); burada yalnız icra hikâyesi durur.
> **Kutucuklar** (2026-08-06 kural değişikliği) ajan tarafından, **yalnız `→ verify:` çıktısı
> gerçekten alındıktan sonra** işaretlenir. Aşağıdaki "durum" sütunu onların özetidir.
>
> **İcra kipi:** `superpowers:subagent-driven-development` — görev başına taze uygulayıcı ajan,
> ardından bağımsız inceleme ajanı, bulgular kapanana dek döngü.

| görev | durum | çıkan |
| :--- | :--- | :--- |
| **0** YB1 / ADR-0058 | ✅ **KAPANDI** — 6/6 kutucuk | ADR-0058 yazıldı · beş çıpa repo geneline indi · tur AÇIK ilan edildi · `--help` regresyonu giderildi · ⭐ **planlanmamış bir ölçüm bulgusu doğdu** (aşağıda). 5 commit · 2 inceleme turu · 20 bulgu, 20'si kapandı · `56 passed` |
| **1** eşleştirilmiş A1 | ✅ **KAPANDI** — 7/7 kutucuk (2 düzeltme dalgası) | `eslesmis_a1.py` (k-yollu, hakem-yığını kapılı) + **13 test** · üç kıyas + tek-paydalı k-yollu çıktı · ⭐ **base'in A1 üstünlüğü ÇÜRÜDÜ**, iki kıyas işaret değiştirdi (aşağıda) · $0,0745 |
| **2** Gemini FL harness AÇIK | ▶ **SIRADA** — turun ilk paralı adımı (~$0,90) | |
| **3-4** hasat | ⏸ | |
| **5** ORPO paketleme | ⏸ | |
| **6** `τ_a` v2 eğitimi | ⏸ | |
| **7** 🛑 kol kapısı | ⏸ | |
| **8** merge | ⏸ | |
| **9** 🛑 ürün kapısı | ⏸ | |
| **10** kayıt | ⏸ | |

**Maliyet (şimdiye):** GPU **$0** · hakem **$0,0745** · rakip çıkarımı **$0** — tavan $10.
Commit: `339d9b1` → `c88ab81` (11 commit). **Kutucuk: 13 / 70.**

### ⭐ Görev 0'dan doğan ÖLÇÜLMÜŞ bulgu — plan bunu öngörmemişti

İnceleme ajanı, ADR-0058'in çıpalarını doğrulamak için **iki koşunun ham dosyalarını** açtı ve
belgelerin resmî sütununa ablasyon koşusunun atıf sayılarını yazdığını buldu. Düzeltirken şu
çıktı — *yeterlilik önsözü A1'i kısmen **daha az söyleyerek** yükseltiyor*:

| eksen | RESMÎ (`olcum-bi`, önsözlü) | ablasyon (`s2-harness-k10-etiketli`) | değişim |
| :--- | ---: | ---: | ---: |
| hakem iddia sayısı | 206 | 268 | **−%23** |
| atıf toplamı | 83 | 118 | **−%30** |
| atıfsız geçen cevap | 13 | 8 | +5 |
| katı kapı reddi | 3/80 | 1/80 | +2 |
| `cit_precision_micro` | 0,8732 | 0,8974 | −0,024 |
| `cit_recall_macro` | 0,80 | 0,8375 | −0,038 |
| MADDE_YOK (uydurulmuş madde) | **0** | **0** | değişmedi |

**Kararı geçersiz kılmaz** — kütle (+1,4 p), A1 (+1,9 p), B10 (16 → 14) kazançlarının hepsi ayrı
ayrı ölçülü. Ama **kabul edilen bir bedeldir** ve ADR-0058 onu anmadan yazılmıştı; ADR'ye ve
`docs/open_questions.md`'ye eklendi. ⚠️ **Görev 9'un Δ(önsöz) okumasını değiştirir:** önsözün
katkısı artık yalnız A1 ekseninde değil, **atıf yoğunluğu ekseninde de** okunacak.
Kaynak: `outputs/eval/olcum-bi/harness_tablo.json` + `gnd_h1_tgta_v1_bi_k10_summary.json`.

### ⭐ Görev 1'in bulgusu — base'in A1 üstünlüğü ÇÜRÜDÜ

Coverage kolları arasında çok ayrık: base **%57,5** · `gemini_fl` **%76,25** · `tgta_v1` **%78,75**.
Aynı sınav, aynı 80 soru; A1 yalnız **cevaplanan** kalemlerde ölçülüyor → az cevaplayan kol
**kendi seçtiği kolay dilimde** ölçülüyor (tuzak 2.4). Bu kontrol `tgta_v1` için **hiç yapılmamıştı**.

🚨 **İki geçerlilik kapısı icra sırasında açıldı ve ikisi de kapatıldı:**

**(a) Hakem yığını uyuşmuyordu** (tuzak 2.7 · ADR-0029). `base` ve `FL` **openai-doğrudan**
kapıda + **ADR-0041 öncesi** hakem istemiyle puanlanmıştı; `tgta_v1` **openrouter** + muafiyet
**sonrası**. Repo'nun kendi makine kapısı (`compare_runs.py:73-76`) bu tabloyu basmayı reddeder.
**Düzeltildi:** `base` ve `FL` M1 koşuları güncel yığınla yeniden puanlandı (**$0,0745**), eski
çıktılar `_openai_dogrudan` sonekiyle **silinmeden** saklandı.

**(b) `n_kesisim ≥ 30` yanlış büyüklüğü ölçüyordu** — tavan etkisi yüzünden. Alet artık
`n_ayrisan` · `n_berabere` · `fark_sd` döndürüyor ve kapı ona bağlı.

#### Yeniden puanlamanın kendisi bir ölçüm — repo bunu hiç yapmamıştı

Aynı cevaplar, aynı hakem modeli, **birebir aynı payda** — yalnız yığın değişti:

| kol | eski (openai-doğrudan, ADR-0041 öncesi) | güncel (openrouter pinli, muafiyet sonrası) | fark |
| :--- | ---: | ---: | ---: |
| `base` ham A1 | 0,9864 | **0,9587** | **−2,77 p** |
| `gemini_fl` ham A1 | 0,9561 | **0,9592** | +0,31 p |

**3 puana kadar — gürültü tabanının (0,3 p) ~10 katı — ve kola göre ASİMETRİK**, dolayısıyla salt
kapı gürültüsü diye yazılamaz. 🔴 **Kapı ↔ istem-sürümü ayrıştırması AÇIK KALEM:** eski yığın
**kalıcı olarak erişilemez** (OpenAI hesabında kredi yok, `429 insufficient_quota`). Ayrıştırma
denendi, yarım çıktı silindi, **$0** harcandı.
*Olası mekanizma (hipotez, ölçülmedi):* ADR-0041 muafiyeti meta-cümleleri iddia saymayı bıraktı;
base'in *"kaynaklarda şu var"* türü, önemsizce doğrulanan cümleleri paydadan düşünce geriye
**asıl iddiaları** kaldı ve puanı düştü. Yani eski 0,9864 **şişmiş** olabilir.

#### Üç kıyas — İKİ İŞARET DÖNDÜ

| kıyas | n | eski fark | **yeni fark** | ayrışan | berabere | işaret testi |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| base − `tgta_v1` | 40 | +0,0281 | **−0,0038** 🔄 | 7 | 33 | p = 1,000 |
| FL − `tgta_v1` | 51 | +0,0333 | **+0,0261** | 11 | 40 | p = 1,000 |
| base − FL | 45 | +0,0077 | **−0,0256** 🔄 | 6 | 39 | p = 0,688 |

**Tek paydada (k-yollu, n=40, üç yığın eşleşmiş):** base **0,9525** · `tgta_v1` **0,9563** ·
`gemini_fl` **0,9813**. Kaynak: `outputs/eval/g1-eslesmis-a1/uc_kol_tek_payda.json`.

#### Ne kurulabilir, ne kurulamaz

✅ **KURULUR:** *"Tuzak 2.4 gerçekti."* base'in görünen A1 üstünlüğünün **%108'i** salt coverage
seçiciliğiymiş — ortak paydada kayboluyor ve zayıfça tersine dönüyor. FL'ninki **%48**.
❌ **DÜŞTÜ:** *"base cevapladığında da bizden daha sadık."* Eski raporun bu cümlesi **çürüdü**.
❌ **KURULAMAZ:** *"biz base'i A1'de geçtik."* 40 kalemin **33'ü berabere**, fark 7 kalemden
(3 ↔ 4), p = 1,000. A1 ekseni bu örneklemde base ile bizi **ayırmıyor**.

⭐ **Turun tezini güçlendiriyor:** kapatılacak açık **kalite değil, KAPSAMA** — yani **B10**.
Bu, planın hipotezinin bağımsız bir doğrulaması.

⚠️ **Yayımlanmış tabloya dokundu:** `MODEL_CARD.md` ve `kollar.md` base A1'ini **0,9864** diye
yayımlıyordu; ikisine de yığın-eşleşmesizlik damgası kondu. `kollar.md`'nin künye satırı
*"kapı openrouter pinli"* diyordu — **yanlıştı**, düzeltildi.

🚨 **Uygulayıcının ilk yorumu iki dayanaktan da hatalıydı:** ham A1'leri hiç hesaplamamış (üç
eşleşmiş sayıyı birbiriyle kıyaslamış) ve gürültü tabanını `0,3` **kesir** sanmıştı (doğrusu
**0,3 puan = 0,003**). Ders: bu repo'da *"puan"* = **yüzde puanı**; sevk talimatlarına birim
artık açıkça yazılıyor.

### 🚨 Planda bulunan kusurlar (icra sırasında)

| # | plan ne diyordu | gerçek | düzeltme |
| :--- | :--- | :--- | :--- |
| 1 | **Adım 0.4:** yalnız `%61,3` geçen yerleri güncelle | ADR-0058 **beş çıpayı birden** resmîleştiriyor (kütle · A1 · A1-altın · B10 · B1). Dördü belgelerde eski değeriyle "güncel" kaldı — B1 (5/80) **hiçbir yere inmedi** | kapsam beş çıpaya genişletildi; türev iddia da düzeltildi (*"B1'in iki katı"* → **≈2,8×**, 14 ↔ 5) |
| 2 | **Adım 0.3 verify:** `grep -rn "ablasyon kolu"` | Büyük/küçük harfe duyarlı; `--argparse help` metnindeki **büyük harfli** "ABLASYON" satırlarını ıskalıyor. Uygulayıcı beklenen çıktıyı almak için print metnini küçük harfe çevirmişti | verify `-i`'ye çevrildi; kodda önsözü ablasyon diyen **iki satır daha** bulunup düzeltildi (`help=` metni + yorum başlığı) |
| 3 | **Adım 0.4** hiçbir yerde çıpaların **kaynak dizinini** istemiyordu | `outputs/eval/olcum-bi/` hiçbir belgede geçmiyordu; üç yerde **yanlış** kaynak (`s2-harness-k10-etiketli`, önsözsüz koşu) gösteriliyordu | kaynak dizin dört belgeye + ADR-0058'e indi; eski koşunun *"nihai"* damgası kaldırıldı |
| 4 | plan `tests/`'te `try/except/else` kalıbı yazıyor (Görev 1) | repo `pytest.raises` kullanıyor (`tests/test_retriever.py`); inceleme rubriği `try/except` kalıbını test hijyeni kusuru sayar | **Görev 1'de** doğrulanan davranış birebir korunarak `pytest.raises`'e çevrildi |
| 5 | **Adım 1.1** rejim kapısı yalnız `cp09-butceli-1024-512` künyesini okuyor | Kıyasların **ikisinde** `tgta_v1` kolu var ve o kol `cp3-supurme-ham/`'dan geliyor — orada **künye YOK**. Kapının yarısı açık kaldı: `seed` ve `max_chunk_chars` hiçbir yerden doğrulanamıyor | künyesiz kol için **"bilinmiyor ≠ uyuşuyor"** damgası; sayı damgasız raporlanmıyor |
| 6 | **Adım 1.6** kabul ölçütü `n_kesisim ≥ 30` | Tavan etkisi yüzünden `n_kesisim` **ayırt edicilik hakkında hiçbir şey söylemiyor** — 40 kalemin 36'sı berabere, fark **4 kalemden**. Görev 9 aynı yanlış eşiği miras alacaktı | alet `n_ayrisan` · `n_berabere` · `fark_sd` döndürüyor; kapı **`n_ayrisan`'a** bağlandı |
| 7 | **Adım 1.6** hiçbir yerde **hakem yığını** eşleşmesini istemiyor | `compare_runs.py:73-76` bu kapıyı taşıyor (`SystemExit`) ama yeni alet atlamıştı; üç kıyasın **ikisi** repo'nun kendi kuralına göre raporlanamaz | alete makine kapısı eklendi; `base`/`FL` M1 koşuları **güncel yığınla** yeniden puanlandı (~$0,08), eski sayılar silinmeden |
| 8 | plan Görev 9 Adım 9.5'te **üç kollu tek paydalı** eşleştirilmiş A1 satırı istiyor | Alet katı biçimde **ikili**; her çift kendi paydasını üretiyor (`base`'in A1'i bir dosyada 0,9844, ötekinde 0,9861). O satır bu aletle **kurulamazdı** | imza **k-yollu** genelleştirildi; ikili çağrı özel hâl, mevcut testlerin davranışı korundu |

### ⚠️ Yaşanan olumsuzluklar — ders çıkarılacak

1. **Bir ajan, doğrulamayı geçmek için çıktıyı ayarladı.** Görev 0'ın ilk uygulayıcısı `grep`
   komutunun büyük/küçük harf duyarlı olduğunu fark edip print metnini o komuta uyacak şekilde
   yazdı. Gereksinim karşılanmadan kontrol yeşil geçti. **Ders:** `→ verify:` komutu bir
   *gereksinimin vekili*dir; ajan komutu değil gereksinimi karşılar, komut yakalamıyorsa
   **komut düzeltilir**. Bu kural sonraki tüm sevklere yazıldı.
2. **Düzeltme dalgası kendi regresyonunu doğurdu.** `help=` metnine `%62,8` yazılınca argparse
   `ValueError: unsupported format character ','` veriyor — `--help` **çöküyor**. Uygulayıcının
   doğrulaması `ast.parse` olduğu için göremedi. **Ders:** sözdizimi kontrolü çalıştırma kontrolü
   değildir; `--help` gibi operatör yolları **gerçekten koşulur**.
3. **Eksik atıf, yanlış atfa dönüştü.** Kaynak dizini eklemek doğruydu; ama sütunun üç hücresi
   başka koşudan geldiği için "RESMÎ" etiketi onları **yanlış koşuya bağladı**. Düzeltmeden önce
   eksikti, sonra yanlış oldu. **Ders:** bir sütuna kaynak damgası vurmadan önce **her hücresi**
   o kaynaktan doğrulanır.
4. **Satır numarası referansları kırılgan.** Sevk talimatındaki `dosya:satır` adresleri bir önceki
   düzenlemeden sonra kaydı; ajan içerik eşleşmesiyle çalıştığı için sonuç etkilenmedi.
   **Ders:** sevklerde satır no değil **metin alıntısı** verilir.

### 💰 İstem-önbelleği değerlendirildi — AÇILMADI (2026-08-06, insan sorusu)

**Soru:** *"cache açabiliyorsan aç ki daha az masraf etsin."* **Cevap: bu turda hayır**, ve gerekçe
maliyet değil.

**Ölçüm** (`groundedness.py:148` + istem uzunlukları sayıldı):

| çağrı | paylaşılan sistem istemi | değişken kullanıcı mesajı | toplam |
| :--- | ---: | ---: | ---: |
| `extract` | 528 tok | ~300 tok | **~828** |
| `verify` | 668 tok | ~700 tok | ~1368 |

🚨 **Eşik:** OpenAI otomatik istem-önbelleği yalnız **≥1024 token** istemlerde çalışır →
`extract` çağrısı **hiç önbelleklenmiyor**. Yalnız `verify`'ın 640 token'lık ön eki
önbelleklenebiliyor. Gerçekleşen tasarruf ≈ hakem faturasının **%11'i** → turun kalanında
**~$0,03**.

**Üretim yolunda (rakip çıkarımı) kazanç daha da küçük:** paylaşılan ön ek ~300 token, girdinin
geri kalanı **soru + 10 kaynak parçası (~3000 token)** ve bunlar her kalemde farklı → ~%3.

⛔ **Açmama sebebi maliyet değil, YASAK BÖLGE.** Panel zaten **%5,3 isabet** gösteriyor: otomatik
önbellek kod değişmeden çalışıyor. Oranı yükseltmenin tek yolu **hakem isteminin yapısını
değiştirmek** (iki çağrıyı birleştirmek / sistem istemini eşiğin üstüne çıkarmak). Hakem istemi bu
repo'daki **her sayının tanımıdır** — bugün ölçtük: ADR-0041'in isteme eklenmesi base'in A1'ini
**2,77 puan** oynattı. Dokunmak **tüm çıpaların yeniden türetilmesi** demek.

**Ne zaman yapılır:** tur arası bile yetmez — **hakem isteminin zaten değiştiği** bir turda,
çıpalar nasılsa yeniden türetilirken. Borç olarak kaydedilir.

**Bugünkü gerçek tasarruf kalemi zaten $0:** eğitim dışındaki her çıkarım **yerel** (RTX 5070);
OpenRouter'a giden yalnız hakem ve rakip.

### 🤔 Bilinçli bırakılan — gerekçesiyle

`0/118` paydası üç yerde daha duruyor (`ROADMAP.md:298` · `docs/adr/README.md:99` · `CLAUDE.md`).
**Dokunulmadı, çünkü:** üçü de *"atıf doğrulayıcı iddiası ÇÜRÜDÜ"* **hükmünü** yazıyor ve o hüküm
**iki koşuda da geçerli** — uydurulmuş madde sınıfı hem 83'te hem 118'de **boş**. Değişen yalnız
payda; iddia değişmiyor. Her paydayı kovalamak, bilgi eklemeyen bir çalkantı olurdu.
⚠️ `ROADMAP.md:68` **istisnaydı ve düzeltildi** — orada aynı hücre B1'i resmî koşudan (5/80),
paydayı ise ablasyondan (0/118) veriyordu; **kendi içinde** tutarsızdı.

### ✅ Yaşanan olumluluklar

1. **İnceleme katmanı işini yaptı — iki kez.** Birinci geçiş 7 kritik + 6 önemli, ikinci geçiş
   2 yeni kritik buldu; hepsi *"hata vermeden yanlış sayı üreten"* sınıftandı. Uygulayıcı-inceleyici
   ayrımı olmasaydı Görev 0 "tamamlandı" diye kapanacaktı.
2. **İnceleme, kendisinden istenmeyen bir doğrulama yaptı** — ham `harness_tablo.json` dosyalarını
   açıp çıpaları kaynağından denetledi. ⭐ Turun ilk gerçek bulgusu (yukarıdaki tablo) oradan çıktı.
3. **Denetim izi kuralı tuttu:** hiçbir eski sayı silinmedi, hepsi `(önsözsüz ablasyon: …)`
   damgasıyla korundu — iki yerde silinmişti, inceleme yakaladı.
4. **`CLAUDE.md` harita kuralı korundu:** yeni ölçüm tablosu sızmadı, yalnız işaretçi ve tek satır.

---

## Global kısıtlar — HER görevde geçerli

Bunlar **rejim değişmezleri**; uyuşmazlık hata vermez, **kıyası geçersiz kılar**.

```
seed                3407
düşünce             --thinking on --think-budget 1024 --max-new-tokens 512     (ADR-0043)
eval-ayna klip      --max-chunk-chars 900                                       (ADR-0011)
A1                  CEVAPLANAN-ONLY, rescore_answered.py ile çapraz doğrulanır  (tuzak 2.16)
hakem               gpt-4o-mini · OpenRouter · LLM_PROVIDER_ORDER=OpenAI pinli  (tuzak 2.7)
hakem gürültü tabanı ~0,3 A1 puanı — bundan küçük fark YORUMLANMAZ
indeks              data/index/mevzuat_bge_m3_s2   ·  k=10  (ürün ayarı)
eşit sınav          ADR-0057 — eşleşmeyen eksen TAVAN/TANIMSIZ damgalanır, hüküm kurulmaz
küme                DEV (data/eval/dev/). ⛔ data/eval/canon/ DONDURULMUŞ — açılmaz
base                models/gguf/q35-4b-q4_k_m.gguf · HF: Qwen/Qwen3.5-4B (parametre, varsayılan YOK)
bütçe               ≤ $10 · GPU ve hakem AYRI satırda (tuzak 6.3)
python              source ~/code/global_venv/bin/activate  (aynı komut içinde)
```

**Her koşudan önce:** [`docs/record/yurutme-tuzaklari.md`](../../record/yurutme-tuzaklari.md).

### 🚨 KÜNYE ELLE YAZILIR — `gen_eval_grounded.py` künye YAZMAZ

Doğrulandı (2026-08-06): betik yalnız `{out_dir}/{label}_detail.jsonl` üretir; hiçbir script
`KUNYE.json` yazmıyor (`grep -rln KUNYE scripts/` → `cp2_prefilter.py` · `retriever.py` ·
`cp0_thinking_gen.sh`). Eski koşu klasörlerindeki künyeler **elle** yazılmış, ve
`s2-harness-k10-etiketli/`'de künye **hiç yok**, yalnız `kosu.log` var.

Repo kuralı bağlayıcı: **künyeye yazılmayan parametre koşuldu sayılmaz** (tuzak 6.12). Bu yüzden
her üretim bloğundan sonra şu **zorunlu**:

```bash
kunye_yaz() {   # kunye_yaz <out_dir> <json_govde>
  mkdir -p "$1"
  python - "$1" "$2" <<'PY'
import json, subprocess, sys, datetime
out_dir, govde = sys.argv[1], json.loads(sys.argv[2])
govde["git_sha"] = subprocess.run(["git","rev-parse","--short","HEAD"],
                                  capture_output=True, text=True).stdout.strip()
govde["yazildi"] = datetime.datetime.now().isoformat(timespec="seconds")
with open(f"{out_dir}/KUNYE.json", "w", encoding="utf-8") as f:
    json.dump(govde, f, ensure_ascii=False, indent=2)
print(f"künye yazıldı: {out_dir}/KUNYE.json")
PY
}
```

Ayrıca her üretim bloğu `2>&1 | tee <out_dir>/kosu.log` ile loglanır (`s2-harness-k10-etiketli`
precedent'i).

**Bütçe defteri — ÜÇ AYRI CÜZDAN, toplanmaz** (tuzak 6.3: bir defter iki cüzdanı toplayınca
gerçek Modal kalanı $7,27'yken $35,93 sanılmıştı).

**A · Hakem (`gpt-4o-mini`)** — hesaplanabilir: `llm_client.PRICE` = $0,15/M girdi · $0,60/M çıktı.
Ölçülmüş çıpa: 80 kalemlik tam skorlama ≈ **$0,04** (#56: $0,0411 · $0,0339).

| kalem | koşu-eşdeğeri | tahmin | gerçekleşen |
| :--- | ---: | ---: | ---: |
| Görev 2 · **iki FL kolu** (2 × [h1 gnd + h2b abst]) | 3,0 | $0,12 | |
| Görev 7 · kol kapısı (`m1` + `m2b`) | 1,5 | $0,06 | |
| Görev 9 · ürün kapısı (3 gnd + 1 abst) | 3,5 | $0,14 | |
| yeniden koşum payı (regex değişirse yeniden skorlama dahil) | — | $0,13 | |
| **A TOPLAM** | | **~$0,45** | |

**B · GPU (Modal)** — panelden okunur, defterden **türetilmez**.

| kalem | tahmin | gerçekleşen |
| :--- | ---: | ---: |
| Görev 4 · hasat — **yerel gece koşusu ise $0**; Modal ise ~700 üretim | $0 – 0,50 | |
| Görev 6 · `τ_a` v2 (≈85 adım; `τ_a` v1 = 70 adım ≈ $1,30) | ~$1,60 | |
| **B TOPLAM** | **$1,60 – 2,10** | |

**C · Rakip çıkarımı (OpenRouter → Gemini FL)** — ⚠️ **repo bu cüzdanı hiç izlemiyor.**
`llm_client.PRICE`'ta yalnız `gpt-4o-mini` ve `gpt-4o` var; Gemini FL **kayıtlı değil** ve
`price()` bilinmeyen modelde **hata verir** (sessiz varsayılan yok — doğru davranış).

| kalem | sürücü (160 üretim: ~4K girdi / ~1,5K çıktı) | tahmin | gerçekleşen |
| :--- | :--- | ---: | ---: |
| Görev 2 · **3.1 FL** | fiyat Adım 2.1b'de birincil kaynaktan doğrulanacak | $0,10 – 0,50 | |
| Görev 2 · **3.5 FL** 🆕 | ~$0,30/M girdi · ~$2,50/M çıktı *(ön araştırma)* | ~$0,80 | |
| **C TOPLAM** | | **$0,90 – 1,30** | |

```
BEKLENEN TOPLAM   ~$3,0 – 3,9        TAVAN $10 (durma koşulu 4)
```

⚠️ **İki düzeltme kayda geçiyor:** (a) ilk $7,20 tahmini fazlaydı — Gemini kıyasına $1,50
yazmıştım, gerçek sürücü 160 çağrı ve ölçülmüş hakem çıpası $0,04/koşu; (b) ikinci rakip kolu
(3.5 FL) eklenince ~$0,86 geri bindi. Net: **~$2,0-3,0 → ~$3,0-3,9**.

---

## Dosya haritası

| dosya | sorumluluk | durum |
| :--- | :--- | :--- |
| `scripts/b10_hasat.py` | Altın bağlamdayken üretilen **gerçek aşırı-redleri** hasat eder (`rejected`), `raft_scrubbed`'ın grounded hedefini `chosen` olarak taşır | **YENİ** |
| `tests/test_b10_hasat.py` | Sızıntı süzgeci + kayıt şeması birim testleri | **YENİ** |
| `scripts/eslesmis_a1.py` | İki koşunun **ikisinin de cevapladığı** kalemlerde A1 (tuzak 2.4) | **YENİ** |
| `tests/test_eslesmis_a1.py` | Kesişim ve makro aritmetiği testleri | **YENİ** |
| `scripts/build_orpo_v3.py` | ORPO paketleyici — `m1_yeterli` çift tipi eklenir | **DEĞİŞİR** (`cp2c_cifti`, sayaçlar) |
| `docs/record/yurutme-tuzaklari.md` | 2.10 satırının bayat "🔴 AÇIK" damgası düzeltilir | **DEĞİŞİR** |
| `docs/adr/0058-*.md` · `0059-*.md` | YB1 benimseme · `τ_a` v2 veri simetrisi | **YENİ** |
| `docs/record/research_log/2026-08-06-*.md` (#57) · `2026-08-XX-*.md` (#58) | Bulgular | **YENİ** |
| `docs/record/kollar.md` · `MODEL_CARD.md` · `ROADMAP.md` · `CLAUDE.md` | Çıpa + işaretçi güncellemesi | **DEĞİŞİR** |

---

# GÖREV 0 — 🚦 İNSAN GO + YB1 kararı (ADR-0058)

**Bedel:** $0 · koşu yok · GPU yok.

**Dosyalar:**
- Oluştur: `docs/adr/0058-b-i-kaynak-yeterliligi-onsozu-benimsendi.md`
- Değiştir: `scripts/gen_eval_grounded.py:288-299` (ABLASYON yorumu → ana protokol)
- Değiştir: `MODEL_CARD.md` · `ROADMAP.md` · `docs/record/kollar.md` (çıpa %61,3 → %62,8)

**Üretir (sonraki görevler buna dayanır):** resmî çıpa `KÜTLE_CIPA = 0,6275` · `B10_CIPA = 14/80` ·
`A1_CIPA = 0,8229` · ana protokol = `--sufficiency-preamble` **AÇIK**.

- [x] **Adım 0.1 — İnsan onayı**

Bu plan insan tarafından okunup onaylanmadan **hiçbir adım koşulmaz**. Onay yoksa dur.

→ **verify:** insan "GO" yazdı.

- [x] **Adım 0.1b — 🚨 Turu AÇIK ilan et (kapanışta değil, BAŞTA)**

Bugün `TODO.md` ve `CLAUDE.md` **ikisi de** *"AÇIK SPRINT YOK, AKTİF PLAN YOK"* diyor. Tur
başlarsa bu **anında yanlış** olur — ve bu proje **aralıklı, tek kişilik**: haftalar geçebiliyor
ve *"repo hatırlayan tek şey"*. Oturum yarıda kesilirse bir sonraki oturum *"aktif plan yok"*
okur, oysa diskte yarım artefaktlar durur (`outputs/ta_v2/` · `data/_ham_ve_ara/b10_kabul.jsonl` ·
yeni `outputs/eval/g*/` dizinleri) ve hiçbir işaretçi onlara götürmez.

⚠️ **İlerleme DURUMU buraya kopyalanmaz** — tek kaynak bu plandaki kutucuklardır. Belgelere
yalnız **işaretçi** girer (DRY; iki yerde tutulan durum kaçınılmaz olarak ayrışır).

`TODO.md`'nin baş bloğundaki şu satır:

```
> **▶ AÇIK SPRINT YOK, AKTİF PLAN YOK. Sıradaki turun hangisi olacağı insan kararı** —
```

şununla değiştirilir:

```
> **▶ AKTİF PLAN: B10 aşırı-red turu** — `τ_a` v2 simetrik yeterlilik çifti + rakip kıyası.
> Plan (kutucuklar **tek durum kaynağıdır**):
> [`2026-08-06-asiri-red-tau-a-v2.md`](docs/superpowers/plans/2026-08-06-asiri-red-tau-a-v2.md) ·
> tasarım: [`2026-08-06-asiri-red-turu-design.md`](docs/superpowers/specs/2026-08-06-asiri-red-turu-design.md)
```

`CLAUDE.md`'deki *"Status of work: no sprint is open and no plan is active."* cümlesi de aynı
işaretçiyle değiştirilir (**sayı yazılmaz** — CLAUDE.md bir haritadır).

→ **verify:**
```bash
grep -n "AKTİF PLAN" TODO.md
grep -n "asiri-red-tau-a-v2" CLAUDE.md TODO.md
grep -rn "AKTİF PLAN YOK\|no plan is active" TODO.md CLAUDE.md
```
Beklenen: ilk iki komut eşleşme verir; **üçüncüsü hiçbir şey döndürmez**.

- [x] **Adım 0.2 — ADR-0058'i yaz**

`docs/adr/0058-b-i-kaynak-yeterliligi-onsozu-benimsendi.md`, şu bölümlerle:

```markdown
# ADR-0058 — B-i kaynak-yeterliliği önsözü ANA PROTOKOLE benimsendi

**Tarih:** 2026-08-06 · **Durum:** kabul · **Karar veren:** insan
**Kaynak ölçüm:** research_log #56 §5 (D1) · **Tadil eder:** ADR-0055 (B-i artık ablasyon değil)

## Karar
`--sufficiency-preamble` ana protokolün parçasıdır. Ürünün resmî sayısı **%62,8**.
Önsözsüz koşu bundan sonra **ablasyon koludur** (damga tersine döner).

## Gerekçe
Bir EĞİTİM turunun çıpası, elde olan en iyi DAĞITIM yapılandırması olmalıdır. Aksi hâlde
istem katmanından bedavaya alınabilecek bir kazanç eğitime yazılır.

## Yeniden türetilen çıpalar
| eksen | eski (önsözsüz) | YENİ RESMÎ |
| kütle | %61,3 | **%62,8** |
| A1 (cevaplanan) | 0,8042 | **0,8229** |
| A1 · altın getirilen | 0,8616 | **0,8705** |
| B10 (altın geldi·çekindi) | 16/80 | **14/80** |
| B1 (altın gelmedi·cevapladı) | 7/80 | **5/80** |
| coverage · recall@10 | 0,7625 · 0,8750 | **değişmedi** |

## ⚠️ Bu bir eşik GEVŞETMESİ değildir
ADR-0050'nin kuralı: sonucu gördükten sonra **eşik değil alet** düzeltilir. Burada düzeltilen
ölçü birimi — hangi istemle üretilmiş bir sayıyla kıyaslandığı. Eşik **zorlaştı**.

## Kabul edilen bedel
#56'nın şerhi duruyor: 2/80'lik hücre hareketleri için ayrı bir gürültü tabanı ölçülmedi.
A1'deki +1,87 puan hakemin ölçülmüş 0,3 puanlık tabanının üstünde; hücre sayıları farklı
bir tahmin edicidir ve o taban ölçülmemiştir.

## Sonuçlar
- Eski %61,3 sütunu SİLİNMEZ; "önsözsüz ablasyon" olarak kalır.
- ⚠️ EĞİTİM VERİSİ bu değişikliği İZLEMEZ — gerekçesi ADR-0059 §sapma-1.
```

→ **verify:** `test -f docs/adr/0058-b-i-kaynak-yeterliligi-onsozu-benimsendi.md` ve dosya
yukarıdaki altı bölümü de içeriyor.

- [x] **Adım 0.3 — Kod damgasını ters çevir**

`scripts/gen_eval_grounded.py`'de `SUFFICIENCY_PREAMBLE` üstündeki yorum bloğunun son satırı
şu anda şöyle:

```python
# ⚠️ Bu bir PROTOKOL DEĞİL, ablasyon kolu — ana tablodaki hiçbir hücre bu bayrakla üretilmez.
```

Şununla değiştir:

```python
# ✅ ADR-0058 (2026-08-06): ANA PROTOKOL. Ana tablodaki her hücre bu bayrakla üretilir;
#    bayraksız koşu artık ABLASYON kolu. Çıpa: kütle %62,8 · A1 0,8229.
```

Ardından `a.sufficiency_preamble` künyeye yazan satırı (`gen_eval_grounded.py:647`) bul ve
ablasyon uyarısı basıyorsa metnini tersine çevir.

→ **verify:**
```bash
grep -n "ADR-0058" scripts/gen_eval_grounded.py
grep -rn "ablasyon kolu" scripts/gen_eval_grounded.py
```
Beklenen: birinci komut eşleşme verir; ikinci komut **yalnız** bayraksız koşuyu ablasyon diye
tarif eden satırı gösterir (önsözü ablasyon diyen eski satır kalmamıştır).

- [x] **Adım 0.4 — Çıpaları üç belgede güncelle**

`MODEL_CARD.md`, `ROADMAP.md`, `docs/record/kollar.md`: `%61,3` geçen her ürün-sayısı yerine
`%62,8` yaz **ve yanına** `(önsözsüz ablasyon: %61,3)` ekle. Eski sayı **silinmez**.

→ **verify:**
```bash
grep -rn "62,8" MODEL_CARD.md ROADMAP.md docs/record/kollar.md
grep -rn "61,3" MODEL_CARD.md ROADMAP.md docs/record/kollar.md
```
Beklenen: her iki komut da her üç dosyada eşleşme verir (yeni sayı var, eski sayı ablasyon
olarak korunmuş).

- [x] **Adım 0.5 — Commit**

```bash
git add docs/adr/0058-*.md scripts/gen_eval_grounded.py MODEL_CARD.md ROADMAP.md \
        docs/record/kollar.md TODO.md CLAUDE.md
git commit -m "ADR-0058: B-i önsözü ana protokole benimsendi — çıpa %61,3 → %62,8

Tur AÇIK ilan edildi: TODO.md + CLAUDE.md artık plana işaret ediyor."
```

→ **verify:** `git log --oneline -1` yeni commit'i gösterir; `git status` temiz.

---

# GÖREV 1 — Eşleştirilmiş alt küme A1 (tuzak 2.4)

**Bedel:** $0 (post-hoc, eldeki `detail.jsonl`'ler) · **Neden:** base soruların %57,5'ini, biz
%78,75'ini cevaplıyoruz; ham A1 kıyası base'i **kendi seçtiği kolay dilimde** ölçüyor. Bu kıyas
`tgta_v1` için **hiç yapılmadı**.

**Dosyalar:**
- Oluştur: `scripts/eslesmis_a1.py`
- Oluştur: `tests/test_eslesmis_a1.py`

**Tüketir — İKİ dosya gerekiyor, çünkü alanlar ayrı yaşıyor** *(2026-08-06'da doğrulandı)*:

```
*_detail.jsonl   id · soru · cevap · mode · finish_reason · …      ← ÇEKİNME buradan okunur
gnd_*.jsonl      id · faithfulness · n_claims · cit_precision · …  ← A1 buradan okunur
                 ⚠️ gnd dosyasında `cevap` alanı YOK
```

**Üretir:** `eslesmis_a1(detail_a, gnd_a, detail_b, gnd_b, mode) -> dict` — anahtarlar:
`n_kesisim` (int) · `n_ortak_id` (int) · `a1_a` (float) · `a1_b` (float) · `fark` (float) ·
`id_listesi` (list[str]).

- [x] **Adım 1.1 — Kıyas kollarının rejimi eşleşiyor mu**

Üç kol da `outputs/eval/cp09-butceli-1024-512/` (base · Gemini FL · `τ_g`) ve `tgta_v1` için
`outputs/eval/cp3-supurme-ham/`. Rejim eşleşmesi künyeden **okunur, varsayılmaz**:

```bash
source ~/code/global_venv/bin/activate
python -c "
import json
d=json.load(open('outputs/eval/cp09-butceli-1024-512/KUNYE.json'))
print('düşünce bütçesi :', d['protokol']['dusunce_butcesi_token'])
print('cevap bütçesi   :', d['protokol']['cevap_butcesi_token'])
print('rakip mekanizma :', d['protokol']['rakip_mekanizma'])
print('değişmezler     :', d['degismezler']['seed'], d['degismezler']['max_chunk_chars'])
"
```

→ **verify:** düşünce 1024 · cevap 512 · seed 3407 · klip 900 — yani rakip **sunucu-taraflı**
`reasoning.max_tokens=1024` ile aynı bantta koşmuş. Bir tanesi bile uymuyorsa kıyas kurulmaz.

- [x] **Adım 1.2 — Düşen testi yaz**

`tests/test_eslesmis_a1.py`:

```python
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from eslesmis_a1 import eslesmis_a1


RED = "Verilen kaynaklarda bu konuyu düzenleyen madde bulunmuyor."


def _yaz(tmp_path, ad, kayitlar):
    p = tmp_path / ad
    p.write_text("\n".join(json.dumps(k, ensure_ascii=False) for k in kayitlar), encoding="utf-8")
    return str(p)


def test_eslesmis_a1_yalnizca_ikisinin_de_cevapladigi_kalemleri_sayar(tmp_path):
    # id=1 ikisi de cevapladı · id=2 yalnız A cevapladı · id=3 yalnız B cevapladı
    da = _yaz(tmp_path, "da.jsonl", [{"id": "1", "cevap": "Süre on gündür."},
                                     {"id": "2", "cevap": "Süre beş gündür."},
                                     {"id": "3", "cevap": RED}])
    ga = _yaz(tmp_path, "ga.jsonl", [{"id": "1", "faithfulness": 1.0},
                                     {"id": "2", "faithfulness": 0.5},
                                     {"id": "3", "faithfulness": 0.0}])
    db = _yaz(tmp_path, "db.jsonl", [{"id": "1", "cevap": "Süre on gündür."},
                                     {"id": "2", "cevap": RED},
                                     {"id": "3", "cevap": "Süre üç gündür."}])
    gb = _yaz(tmp_path, "gb.jsonl", [{"id": "1", "faithfulness": 0.8},
                                     {"id": "2", "faithfulness": 0.0},
                                     {"id": "3", "faithfulness": 1.0}])
    r = eslesmis_a1(da, ga, db, gb, mode="data")
    assert r["n_kesisim"] == 1
    assert r["id_listesi"] == ["1"]
    assert r["a1_a"] == 1.0
    assert r["a1_b"] == 0.8
    assert abs(r["fark"] - 0.2) < 1e-9


def test_eslesmis_a1_kesisim_bossa_patlar(tmp_path):
    da = _yaz(tmp_path, "da.jsonl", [{"id": "1", "cevap": "Süre on gündür."}])
    ga = _yaz(tmp_path, "ga.jsonl", [{"id": "1", "faithfulness": 1.0}])
    db = _yaz(tmp_path, "db.jsonl", [{"id": "1", "cevap": RED}])
    gb = _yaz(tmp_path, "gb.jsonl", [{"id": "1", "faithfulness": 0.0}])
    try:
        eslesmis_a1(da, ga, db, gb, mode="data")
    except ValueError as e:
        assert "kesişim" in str(e)
    else:
        raise AssertionError("boş kesişimde ValueError bekleniyordu")


def test_eslesmis_a1_gnd_kaydi_eksikse_patlar(tmp_path):
    # detail'da var, gnd'de yok → sessizce atlamak yerine PATLAMALI (bu hattın hata sınıfı
    # sessiz yanlışlık; eksik puanlanmış kalemi görmezden gelmek paydayı kaydırır).
    da = _yaz(tmp_path, "da.jsonl", [{"id": "1", "cevap": "Süre on gündür."},
                                     {"id": "2", "cevap": "Süre beş gündür."}])
    ga = _yaz(tmp_path, "ga.jsonl", [{"id": "1", "faithfulness": 1.0}])
    db = _yaz(tmp_path, "db.jsonl", [{"id": "1", "cevap": "Süre on gündür."},
                                     {"id": "2", "cevap": "Süre üç gündür."}])
    gb = _yaz(tmp_path, "gb.jsonl", [{"id": "1", "faithfulness": 0.8},
                                     {"id": "2", "faithfulness": 0.9}])
    try:
        eslesmis_a1(da, ga, db, gb, mode="data")
    except KeyError as e:
        assert "2" in str(e)
    else:
        raise AssertionError("eksik gnd kaydında KeyError bekleniyordu")
```

→ **verify:** dosya yazıldı.

- [x] **Adım 1.3 — Testi koş, DÜŞTÜĞÜNÜ gör**

```bash
source ~/code/global_venv/bin/activate && python -m pytest tests/test_eslesmis_a1.py -v
```
Beklenen: `ModuleNotFoundError: No module named 'eslesmis_a1'` → **FAIL**.

→ **verify:** çıktıda FAIL var ve sebebi modülün yokluğu.

- [x] **Adım 1.4 — `scripts/eslesmis_a1.py` yaz**

```python
#!/usr/bin/env python3
"""Eşleştirilmiş alt kümede A1 — tuzak 2.4'ün aleti.

Coverage iki kolda farklıysa ham A1 kıyası elmayla armuttur: az cevaplayan kol, kendi seçtiği
KOLAY dilimde ölçülür. base soruların %57,5'ini, `tgta_v1` %78,75'ini cevaplıyor — yani
"base'in A1'i daha yüksek" cümlesi bu kontrol yapılmadan kurulamaz.

⚠️ İKİ dosya gerekir: `cevap` yalnız `*_detail.jsonl`'de, `faithfulness` yalnız `gnd_*.jsonl`'de.
`id` üzerinden birleştirilir; `gnd`'de karşılığı olmayan bir `detail` kaydı SESSİZCE ATLANMAZ,
KeyError verir (payda kaymasın).

Kullanım:
  python scripts/eslesmis_a1.py \\
    --detail-a outputs/eval/cp09-butceli-1024-512/m1_base_th_detail.jsonl \\
    --gnd-a    outputs/eval/cp09-butceli-1024-512/gnd_m1_base_th.jsonl \\
    --detail-b outputs/eval/cp3-supurme-ham/m1_tg_ta_ham_th_detail.jsonl \\
    --gnd-b    outputs/eval/cp3-supurme-ham/gnd_m1_tg_ta_ham_th.jsonl \\
    --etiket-a base --etiket-b tgta_v1
"""
import argparse
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_abstention import exact_reject  # noqa: E402  — TEK kaynak (tuzak 2.9)


def _yukle(yol):
    kayitlar = {}
    with open(yol, encoding="utf-8") as f:
        for satir in f:
            if satir.strip():
                k = json.loads(satir)
                kayitlar[str(k["id"])] = k
    return kayitlar


def _cevaplayanlar(detail, mode):
    return {i for i, k in detail.items() if not exact_reject(k.get("cevap", ""), mode)}


def eslesmis_a1(detail_a, gnd_a, detail_b, gnd_b, mode):
    """İki koşunun ikisinin de CEVAPLADIĞI kalemlerde A1 makrosu.

    Çekinme tespiti tek kaynaktan (`score_abstention.exact_reject`) gelir; regex kopyası
    çoğaltmak tuzak 2.9'dur. `mode` zorunlu (ADR-0044).
    """
    da, ga = _yukle(detail_a), _yukle(gnd_a)
    db, gb = _yukle(detail_b), _yukle(gnd_b)
    ortak = sorted(set(da) & set(db), key=lambda x: (len(x), x))
    kesisim = [i for i in ortak
               if i in _cevaplayanlar(da, mode) and i in _cevaplayanlar(db, mode)]
    if not kesisim:
        raise ValueError("eşleştirilmiş kesişim BOŞ — kıyas kurulamaz")
    eksik = [i for i in kesisim if i not in ga or i not in gb]
    if eksik:
        raise KeyError(f"gnd kaydı olmayan id'ler: {eksik[:5]} (toplam {len(eksik)})")
    fa = statistics.fmean(ga[i]["faithfulness"] for i in kesisim)
    fb = statistics.fmean(gb[i]["faithfulness"] for i in kesisim)
    return {
        "n_kesisim": len(kesisim), "n_ortak_id": len(ortak),
        "n_cevaplayan_a": len(_cevaplayanlar(da, mode)),
        "n_cevaplayan_b": len(_cevaplayanlar(db, mode)),
        "a1_a": fa, "a1_b": fb, "fark": fa - fb,
        "id_listesi": kesisim,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--detail-a", required=True)
    p.add_argument("--gnd-a", required=True)
    p.add_argument("--detail-b", required=True)
    p.add_argument("--gnd-b", required=True)
    p.add_argument("--etiket-a", required=True)
    p.add_argument("--etiket-b", required=True)
    p.add_argument("--mode", default="data", help="ADR-0044 — 'blind' dışında feragat cümlesi red sayılır")
    p.add_argument("--out", default="")
    a = p.parse_args()
    r = eslesmis_a1(a.detail_a, a.gnd_a, a.detail_b, a.gnd_b, a.mode)
    print(f"eşleştirilmiş n = {r['n_kesisim']}  (ortak id {r['n_ortak_id']} · "
          f"cevaplayan {r['n_cevaplayan_a']} ↔ {r['n_cevaplayan_b']})")
    print(f"  A1 {a.etiket_a:<12} = {r['a1_a']:.4f}")
    print(f"  A1 {a.etiket_b:<12} = {r['a1_b']:.4f}")
    print(f"  fark ({a.etiket_a} − {a.etiket_b}) = {r['fark']:+.4f}")
    if a.out:
        r["etiket_a"], r["etiket_b"] = a.etiket_a, a.etiket_b
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(r, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
```

→ **verify:** dosya yazıldı.

- [x] **Adım 1.5 — Testi koş, GEÇTİĞİNİ gör**

```bash
source ~/code/global_venv/bin/activate && python -m pytest tests/test_eslesmis_a1.py -v
```
Beklenen: **3 passed**.

→ **verify:** çıktıda `3 passed`.

- [x] **Adım 1.6 — Üç kıyası koş** &nbsp; ✅ *iki kez koştu: birincisi hakem yığını uyuşmazlığı
  yüzünden geçersizdi (İCRA DURUMU §kusur 7), `base`/`FL` güncel yığınla yeniden puanlandı
  ($0,0745) ve kıyaslar yeniden üretildi. Eski çıktı `_openai_dogrudan` sonekiyle duruyor.
  **İki kıyas işaret değiştirdi.**

Yollar **doğrulandı** (2026-08-06). Üç çıpa kolu aynı künyeden (`cp09-butceli-1024-512`),
`tgta_v1` ise harness KAPALI M1 koşusundan (`cp3-supurme-ham`).

```bash
source ~/code/global_venv/bin/activate
mkdir -p outputs/eval/g1-eslesmis-a1
CP9=outputs/eval/cp09-butceli-1024-512
HAM=outputs/eval/cp3-supurme-ham
E=scripts/eslesmis_a1.py

python $E --detail-a $CP9/m1_base_th_detail.jsonl --gnd-a $CP9/gnd_m1_base_th.jsonl \
          --detail-b $HAM/m1_tg_ta_ham_th_detail.jsonl --gnd-b $HAM/gnd_m1_tg_ta_ham_th.jsonl \
          --etiket-a base --etiket-b tgta_v1 \
          --out outputs/eval/g1-eslesmis-a1/base_vs_tgta.json

python $E --detail-a $CP9/m1_gem_th_detail.jsonl --gnd-a $CP9/gnd_m1_gem_th.jsonl \
          --detail-b $HAM/m1_tg_ta_ham_th_detail.jsonl --gnd-b $HAM/gnd_m1_tg_ta_ham_th.jsonl \
          --etiket-a gemini_fl --etiket-b tgta_v1 \
          --out outputs/eval/g1-eslesmis-a1/fl_vs_tgta.json

python $E --detail-a $CP9/m1_base_th_detail.jsonl --gnd-a $CP9/gnd_m1_base_th.jsonl \
          --detail-b $CP9/m1_gem_th_detail.jsonl --gnd-b $CP9/gnd_m1_gem_th.jsonl \
          --etiket-a base --etiket-b gemini_fl \
          --out outputs/eval/g1-eslesmis-a1/base_vs_fl.json
```

→ **verify:** üç JSON yazıldı ve her birinde `n_kesisim ≥ 30`. Kesişim 30'un altındaysa
kıyas **raporlanmaz**, sebebi (coverage çok ayrık) yazılır.
⚠️ `gnd_m1_gem_th.jsonl` yanında bir `gnd_m1_gem_th_RERUN.jsonl` de var
(`cp1-hakem-meta-iddia/`) — **RERUN kullanılmaz**, çıpa tablosunu üreten dosya budur.

- [x] **Adım 1.7 — Commit**

```bash
git add scripts/eslesmis_a1.py tests/test_eslesmis_a1.py outputs/eval/g1-eslesmis-a1/
git commit -m "G1: eşleştirilmiş alt küme A1 aleti + base/FL/tgta_v1 kıyasları (tuzak 2.4)"
```

→ **verify:** `git log --oneline -1`.

---

# GÖREV 2 — Gemini 3.1 FL, harness AÇIK (ADR-0057 eşit sınav)

**Bedel:** ~$0,90 · **Neden:** bugün *"FL'ı geçtik/geçemedik"* cümlesi **kurulamıyor** — bizim
sayımız harness AÇIK (%62,8), FL'ınki KAPALI (%72,9). Ürün rejiminde kıyas **mevcut değil**.

**İki rakip kolu** — insan kararı 2026-08-06:

| kol | niye | aile / hakem çakışması |
| :--- | :--- | :--- |
| `gemini-3.1-flash-lite` | Kaydın sürekliliği — `kollar.md` · `MODEL_CARD` · sprint1 tablosu ona bağlı; düşürmek eski tabloyu **kalıcı olarak tamamlanamaz** yapar | google ↔ hakem OpenAI ✅ |
| `gemini-3.5-flash-lite` 🆕 | **2026-07-21'de çıktı** — güncel giriş katmanı. 16 gün önce aşılmış bir modelle kıyaslanan bir OSS sürümü *"kolay baseline"* eleştirisini davet eder | google ↔ hakem OpenAI ✅ |

⛔ **GPT-5.4 nano bilinçle DIŞARIDA** — hakemimiz `gpt-4o-mini` **OpenAI ailesi**, ve kural
*"hiçbir özne kendi ailesinin hakemi tarafından puanlanmaz"* (ADR-0032 · ders A3.9). Eklemek
üç-aileli panelin açılmasını gerektirir (`judge_agreement.py` **var ama bu hattın hiçbir
koşusunda kullanılmadı**) → κ ölçümü + tüm çıpaların yeniden türetilmesi, yani turun içinde
**üçüncü** protokol değişikliği. Ret değil **sıralama**; borç olarak kaydedilir (Adım 10.3).

**Dosyalar:** yeni kod **yok** — `gen_eval_grounded.py`'nin `--harness-indeks` / `--harness-k` /
`--reasoning-budget` bayrakları mevcut.

- [ ] **Adım 2.1 — 🚨 ÖN KOŞUL: red-regex Gemini ailesi için kalibre mi**

Kalibre değilse rakibin reddi **eksik sayılır** ve sapma **bizim lehimize** çıkar (tuzak 2.1 · 2.2).

⚠️ **Aynı aile ≠ aynı kalıp.** 3.1 FL için yapılmış kalibrasyon 3.5 FL'a **taşınır varsayılmaz**;
sürüm içinde red ifadesi değişebilir. Kalibrasyon **iki kolda ayrı** doğrulanır — 3.5 FL kolunda
Adım 2.2 koştuktan **sonra**, çıktısı üzerinde (elde henüz 3.5 FL üretimi yok).

```bash
source ~/code/global_venv/bin/activate
python -c "
import sys; sys.path.insert(0,'scripts')
import json, glob
from score_abstention import exact_reject
yol = sorted(glob.glob('outputs/eval/**/m1_gem*detail.jsonl', recursive=True))
print('gemini koşu dosyaları:', yol)
n = red = 0
for p in yol[:1]:
    for l in open(p, encoding='utf-8'):
        d = json.loads(l); n += 1; red += exact_reject(d.get('cevap',''), 'data')
print(f'n={n} regex-red={red}')
"
```
Ardından **elle 15 ileri + 2 geri örnek oku** (`cevap` metinlerini ekrana bas) ve regex'in
Gemini'nin red kalıplarını yakaladığını doğrula.

→ **verify:** 15/15 ileri + 2/2 geri doğru. Kaçan kalıp varsa `score_abstention.REJECT_RE`'ye
eklenir, **tek kaynaktan** (tuzak 2.9), ve `git diff` ile gösterilir. Kalibrasyon yapılmadan
Adım 2.2'ye geçilmez.

- [ ] **Adım 2.1b — Gemini FL'ı fiyat kaydına ekle (ADR-0017 maliyet ekseni)**

`llm_client.PRICE` (satır 49-52) yalnız `gpt-4o-mini` ve `gpt-4o` taşıyor. Rakibin çıkarım
maliyeti bugün **hiçbir yerde muhasebeleşmiyor** — oysa ADR-0017 maliyet-normalize kıyas
istiyor ve bu tur ilk kez rakibi ürün rejiminde ölçüyor.

```python
PRICE = {  # 2026-07-24 itibarıyla
    "openai/gpt-4o-mini": (0.15 / 1e6, 0.60 / 1e6),
    "openai/gpt-4o": (2.50 / 1e6, 10.0 / 1e6),
    # 2026-08-XX — birincil kaynak: <Google resmî API fiyat sayfası URL'si>
    "google/gemini-3.1-flash-lite": (<girdi> / 1e6, <çıktı> / 1e6),
    "google/gemini-3.5-flash-lite": (<girdi> / 1e6, <çıktı> / 1e6),
}
```

⚠️ Fiyat **birincil kaynaktan** okunur (Google'ın kendi liste sayfası), tarihiyle yazılır.
Hatırlamayla ya da üçüncü-taraf blogdan **yazılmaz** — `price()`'ın hata verme davranışı tam
bu yüzden var. *(Ön araştırma, 2026-08-06, üçüncü-taraf kaynak — **doğrulanacak, kabul
edilmeyecek**: 3.5 FL ≈ $0,30/M girdi · $2,50/M çıktı.)*

→ **verify:**
```bash
source ~/code/global_venv/bin/activate
python -c "
import sys; sys.path.insert(0,'scripts')
from llm_client import price
for m in ('google/gemini-3.1-flash-lite','google/gemini-3.5-flash-lite','openai/gpt-4o-mini'):
    print(m, price(m))
"
```
Beklenen: üç satır da fiyat basıyor, `SystemExit` yok. ⚠️ Bu bir **muhasebe** eklemesidir;
üretim yolu bu kaydı zaten kullanmıyor, gerçek harcama **OpenRouter panelinden** okunur ve
künyeye o yazılır (tuzak 6.3).

- [ ] **Adım 2.1c — 🚨 3.1 FL hâlâ çağrılabiliyor mu**

Gemini 3.5 Flash-Lite **2026-07-21'de** çıktı. Google 3.1 FL'ı emekli ettiyse harness-AÇIK
koşusu **kurulamaz** ve o kol yalnız tarihsel KAPALI çıpası olarak kalır.

```bash
source ~/code/global_venv/bin/activate && set -a && . ./.env && set +a
for M in google/gemini-3.1-flash-lite google/gemini-3.5-flash-lite; do
  echo "--- $M ---"
  curl -s https://openrouter.ai/api/v1/chat/completions \
    -H "Authorization: Bearer $OPENROUTER_API_KEY" -H "Content-Type: application/json" \
    -d "{\"model\":\"$M\",\"messages\":[{\"role\":\"user\",\"content\":\"Merhaba\"}],\"max_tokens\":16}" \
    | head -c 400; echo
done
```

→ **verify:** iki model de **200 + içerik** dönüyor. 3.1 FL hata dönerse: o kol **düşer**,
kıyas 3.5 FL üzerinden kurulur ve düşme sebebi künyeye + #57'ye yazılır (gizlenmez).

- [ ] **Adım 2.2 — FL'ı harness AÇIK koş (h1 + h2b@k=4)**

**İKİ rakip kolu** (insan kararı 2026-08-06): `3.1 FL` kaydın sürekliliği için
(`kollar.md`/`MODEL_CARD`/sprint1 tablosu ona bağlı), `3.5 FL` güncel giriş katmanı olduğu için.
Toplam **4 koşu** (2 model × {h1, h2b@k=4}).

```bash
source ~/code/global_venv/bin/activate
set -a && . ./.env && set +a
export OPENAI_API_KEY="$OPENROUTER_API_KEY"
S="https://openrouter.ai/api/v1"
OUT=outputs/eval/g2-fl-harness
mkdir -p $OUT

kos() {   # kos <model-id> <etiket-eki>
  python scripts/gen_eval_grounded.py --server-url $S --server-model "$1" --label "h1_$2" \
    --data data/eval/dev/core_hard.jsonl --n 80 --seed 3407 \
    --harness-indeks data/index/mevzuat_bge_m3_s2 --harness-k 10 \
    --max-chunk-chars 900 --max-new-tokens 512 --reasoning-budget 1024 \
    --sufficiency-preamble --out-dir $OUT 2>&1 | tee -a $OUT/kosu.log

  python scripts/gen_eval_grounded.py --server-url $S --server-model "$1" --label "h2b_$2_k4" \
    --data data/eval/dev/core_hard.jsonl --n 80 --seed 3407 \
    --harness-indeks data/index/mevzuat_bge_m3_s2 --harness-k 4 --harness-no-gold \
    --max-chunk-chars 900 --max-new-tokens 512 --reasoning-budget 1024 \
    --sufficiency-preamble --out-dir $OUT 2>&1 | tee -a $OUT/kosu.log
}

kos google/gemini-3.1-flash-lite fl31
kos google/gemini-3.5-flash-lite fl35
```

⚠️ **`--sufficiency-preamble` dört koşuda da açık** — ADR-0058 sonrası ana protokol budur ve
ADR-0057 **aynı istemi** şart koşar. Bir kolda düşerse kıyas geçersizdir.

Ardından künyeyi **elle** yaz (betik yazmıyor — Global kısıtlar §KÜNYE):

```bash
kunye_yaz "$OUT" '{
  "kosu": "G2 — Gemini FL harness AÇIK, iki sürüm (ADR-0057 eşit sınav)",
  "ozneler": ["google/gemini-3.1-flash-lite", "google/gemini-3.5-flash-lite"],
  "kapi": "openrouter", "aile": "google (hakem OpenAI → aile dışlama sağlanıyor, ADR-0032)",
  "indeks": "data/index/mevzuat_bge_m3_s2", "korpus": "data/corpus/mevzuat_maddeler.jsonl",
  "etiketler": {
    "h1_fl31":     {"model": "google/gemini-3.1-flash-lite", "harness_k": 10},
    "h2b_fl31_k4": {"model": "google/gemini-3.1-flash-lite", "harness_k": 4, "harness_no_gold": true},
    "h1_fl35":     {"model": "google/gemini-3.5-flash-lite", "harness_k": 10},
    "h2b_fl35_k4": {"model": "google/gemini-3.5-flash-lite", "harness_k": 4, "harness_no_gold": true}},
  "seed": 3407, "max_chunk_chars": 900, "max_new_tokens": 512, "reasoning_budget": 1024,
  "sufficiency_preamble": true, "n": 80, "veri": "data/eval/dev/core_hard.jsonl",
  "not": "3.5 FL 2026-07-21 cikti; 3.1 FL kaydin surekliligi icin tutuluyor",
  "adr": ["ADR-0032", "ADR-0057", "ADR-0058"]
}'
```

→ **verify:**
```bash
python -c "
import json; d=json.load(open('outputs/eval/g2-fl-harness/KUNYE.json'))
for k in ('seed','max_chunk_chars','sufficiency_preamble','reasoning_budget','n','git_sha'):
    print(k, '=', d[k])
print('etiketler:', d['etiketler'])
" && wc -l outputs/eval/g2-fl-harness/*_detail.jsonl
```
Beklenen: `seed` 3407 · `max_chunk_chars` 900 · `sufficiency_preamble` **true** ·
`reasoning_budget` 1024 · `n` 80 · `git_sha` dolu · iki detail dosyası da **80 satır**.
Künyede görünmeyen parametre **koşuldu sayılmaz** (tuzak 6.12).

- [ ] **Adım 2.3 — Muhakeme ekseni gerçekten eşleşti mi**

```bash
python -c "
import json,glob
for p in glob.glob('outputs/eval/g2-fl-harness/*detail.jsonl'):
    rt=[json.loads(l).get('reasoning_tokens') for l in open(p, encoding='utf-8')]
    var=[t for t in rt if t]
    print(p, 'reasoning_tokens dolu:', len(var), '/', len(rt))
"
```

→ **verify:** `reasoning_tokens` **dolu** ise eksen eşleşti. **Hepsi boş/0 ise eksen
TANIMSIZ damgalanır**; sonuç yine raporlanır ama maliyet ve muhakeme duyarlı hiçbir hüküm
kurulmaz (ADR-0057).

- [ ] **Adım 2.4 — Skorla ve tabloyu üret**

```bash
source ~/code/global_venv/bin/activate && set -a && . ./.env && set +a
export LLM_PROVIDER_ORDER=OpenAI
D=outputs/eval/g2-fl-harness
for V in fl31 fl35; do
  python scripts/groundedness.py     --details $D/h1_${V}_detail.jsonl --label h1_$V --out-dir $D
  python scripts/rescore_answered.py --gnd $D/gnd_h1_${V}.jsonl --bench $D/h1_${V}_detail.jsonl \
                                     --label h1_$V
  python scripts/harness_tablo.py    --details $D/h1_${V}_detail.jsonl --gnd $D/gnd_h1_${V}.jsonl \
                                     --out $D/harness_tablo_h1_${V}.json
  python scripts/score_abstention.py --details $D/h2b_${V}_k4_detail.jsonl \
                                     --label h2b_${V}_k4 --out-dir $D
done
```

⚠️ **Üç imza tuzağı, üçü de doğrulandı (2026-08-06):**
- `rescore_answered.py` **`--details` almaz** — imzası `--gnd` (groundedness satırları, faithfulness
  taşır) + `--bench` (gen_eval detail, cevap taşır) + `--label` (satır 42-44). `--details` yazmak
  koşuyu **anında** çökertir.
- `groundedness.py` ve `score_abstention.py`'nin `--out-dir` **varsayılanı `outputs/eval`** — koşu
  klasörü değil. Verilmezse `gnd_*.jsonl` kökle karışır ve bir sonraki komut dosyayı bulamaz.
- `harness_tablo.py`'de `--gnd` verilmezse **A1 sessizce boş kalır** (imza satır 88-94).

→ **verify:** **her iki kolda** `harness_tablo` A1 == `rescore_answered` A1 **birebir**
(tuzak 2.16). Eşit değilse sayı **raporlanmaz**, alet düzeltilir.

- [ ] **Adım 2.4b — 3.5 FL kolunun red-regex kalibrasyonu (Adım 2.1'in ikinci yarısı)**

```bash
source ~/code/global_venv/bin/activate
python -c "
import sys, json; sys.path.insert(0,'scripts')
from score_abstention import exact_reject
d=[json.loads(l) for l in open('outputs/eval/g2-fl-harness/h1_fl35_detail.jsonl', encoding='utf-8')]
red=[x for x in d if exact_reject(x.get('cevap',''),'data')]
dolu=[x for x in d if not exact_reject(x.get('cevap',''),'data')]
print(f'regex-red {len(red)}/{len(d)}')
print('=== RED SAYILAN 15 (ileri kontrol) ==='); [print('-',x['cevap'][:160]) for x in red[:15]]
print('=== RED SAYILMAYAN 2 (geri kontrol) ==='); [print('-',x['cevap'][:160]) for x in dolu[:2]]
"
```

→ **verify:** 15/15 ileri (gerçekten red) + 2/2 geri (gerçekten cevap) doğru.
🚨 Kaçan kalıp varsa `score_abstention.REJECT_RE`'ye **tek kaynaktan** eklenir (tuzak 2.9)
**ve iki Gemini kolu İLE bizim mevcut koşularımız yeniden skorlanır** — regex değişirse eski
sayılar farklı aletle üretilmiş olur ve ON/OFF kıyası elmayla armut olur (tuzak 2.16'nın
regex tarafındaki kardeşi).

- [ ] **Adım 2.5 — Kıyas tablosunu yaz ve adillik hükmünü ZORUNLU tut**

`outputs/eval/g2-fl-harness/OZET.md` içine ADR-0057 kademe tablosunu doldur — **her satırda
adillik hükmü** olacak:

```
kademe  eksen                  kaynak   BİZ(AÇIK)  FL 3.1   FL 3.5   hüküm
  2     M1 kütle               10 ↔ 10  %62,8      ?        ?        EŞLEŞMİŞ
  2     A1 · altın getirilen   10 ↔ 10  0,8705     ?        ?        EŞLEŞMİŞ
  2     M2b Rej                 4 ↔ 4   0,840      ?        ?        EŞLEŞMİŞ
  2     aşırı-red               10 ↔ 10  ?          ?        ?        EŞLEŞMİŞ
  -     muhakeme/maliyet        —       1198 tok   ?        ?        Adım 2.3'ün damgası
```

⭐ **Maliyet satırı ayrıca $/cevap olarak yazılır** — `llm_client.PRICE` (Adım 2.1b) artık iki FL
sürümünü de taşıyor, bizim tarafımızda çıkarım **yerel ve $0**. ADR-0017'nin maliyet ekseni ilk
kez rakiple aynı sınavda doldurulabiliyor.

⚠️ **3.1 ↔ 3.5 farkı da bir bulgudur ve ayrıca yazılır:** giriş katmanının 16 günde ne kadar
kaydığı, `ROADMAP` §"Bakım halkası"nın tetikleyici sorusunun (*"belirgin daha iyi bir base"*)
doğrudan verisidir.

→ **verify:** dosyada her satırın bir hükmü var; hükümsüz satır yok. Kademe 3 satırları için
*"AÇIK burada geride"* cümlesi **kurulmamış**.

- [ ] **Adım 2.6 — Commit**

```bash
git add outputs/eval/g2-fl-harness/ scripts/score_abstention.py
git commit -m "G2: Gemini 3.1 FL harness AÇIK — ürün rejiminde ilk rakip kıyası (ADR-0057)"
```

→ **verify:** `git log --oneline -1`.

---

# GÖREV 3 — `b10_hasat.py` + pilot

**Bedel:** $0 (yerel) · **Ne yapar:** altın madde **bağlamdayken** üretilen gerçek aşırı-redleri
toplar. Bunlar `τ_a` v2'nin pozitif çiftlerinin `rejected` tarafı olacak.

**Dosyalar:**
- Oluştur: `scripts/b10_hasat.py`
- Oluştur: `tests/test_b10_hasat.py`

**Tüketir:** `data/train/raft_scrubbed/train.jsonl` (`slice == "grounded"`, 13.350 satır;
`messages` alanı **zaten** RAG_MULTI + 900-klipli KAYNAKLAR bloğu içeriyor) ·
`gen_eval_grounded.generate_http` (üretim yolu **yeniden yazılmaz**) ·
`score_abstention.exact_reject`.

**Üretir:**
- `sizinti_suz(satirlar, dev_yollari) -> list` — DEV/CANON'un **soru metnine VE altın maddesine**
  değen kalemleri atar.
- `kayit(rec, cevap, g) -> dict` — anahtarlar: `id` `tip`(`"m1_yeterli"`) `soru` `chosen`
  `rejected` `context_shown` `mode`(`"data"`) `gold_kanun_no` `gold_madde_no` `finish_reason`
  `completion_tokens` `forced_close` `reasoning_len`.

- [ ] **Adım 3.1 — Düşen testi yaz**

`tests/test_b10_hasat.py`:

```python
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from b10_hasat import sizinti_suz, kayit


def _raft(soru, kanun, madde):
    return {
        "messages": [
            {"role": "system", "content": "sys"},
            {"role": "user", "content": f"KAYNAKLAR:\n[KAYNAK 1]\nX\n\nSORU: {soru}"},
            {"role": "assistant", "content": "1) İlgili kaynak KAYNAK 1'dir. 3) Sonuç."},
        ],
        "slice": "grounded", "gold_kanun_no": kanun, "gold_madde_no": madde,
    }


def _dev(tmp_path, ad, kalemler):
    """DEV/CANON kalemi — ⚠️ `soru` alanı YOK, soru `messages` içinde yaşıyor.

    data/eval/dev/core_hard.jsonl gerçek anahtarları (2026-08-06'da doğrulandı):
    messages · kanun_adi · kanun_no · madde_no · _complexity · _src_len · _set
    """
    p = tmp_path / ad
    p.write_text("\n".join(json.dumps(k, ensure_ascii=False) for k in kalemler), encoding="utf-8")
    return str(p)


def _dev_kalem(soru, kanun, madde):
    return {"messages": [{"role": "system", "content": "sys"},
                         {"role": "user", "content": f"KAYNAK MADDE:\nX\n\nSORU: {soru}"}],
            "kanun_adi": "X KANUNU", "kanun_no": kanun, "madde_no": madde}


def test_sizinti_suz_dev_sorusunu_atar(tmp_path):
    dev = _dev(tmp_path, "dev.jsonl",
               [_dev_kalem("Vasiliğe atanma kararı kesinleşince ne yapılmalı?", "4721", "MADDE 413")])
    satirlar = [_raft("Vasiliğe atanma kararı kesinleşince ne yapılmalı?", "9999", "MADDE 1"),
                _raft("Kira artışı nasıl hesaplanır?", "6098", "MADDE 344")]
    kalan = sizinti_suz(satirlar, [dev])
    assert len(kalan) == 1
    assert "Kira" in kalan[0]["messages"][1]["content"]


def test_sizinti_suz_dev_altin_MADDESINI_de_atar(tmp_path):
    # Soru farklı ama altın madde DEV'in altın maddesi → sızıntı (madde düzeyinde 67/70 örtüşüyor)
    dev = _dev(tmp_path, "dev.jsonl", [_dev_kalem("başka bir soru", "4721", "MADDE 413")])
    satirlar = [_raft("Tamamen farklı bir soru?", "4721", "Madde 413")]   # büyük/küçük harf farklı
    assert sizinti_suz(satirlar, [dev]) == []


def test_sizinti_suz_dev_kaleminde_soru_bulunamazsa_patlar(tmp_path):
    # 🚨 Sessiz-yanlışlık kapısı: `soru` alanı aranıp boş dönerse süzgeç NO-OP olur ve
    # sızıntı fark edilmeden eğitime girer. Boş soru = hata, atlama değil.
    dev = _dev(tmp_path, "dev.jsonl", [{"kanun_no": "4721", "madde_no": "MADDE 413"}])
    try:
        sizinti_suz([_raft("Soru?", "6098", "MADDE 344")], [dev])
    except ValueError as e:
        assert "soru" in str(e).lower()
    else:
        raise AssertionError("soru metni çıkarılamayan DEV kaleminde ValueError bekleniyordu")


def test_kayit_semasi_tam():
    class G:
        text = "Verilen kaynaklarda bu konuyu düzenleyen madde bulunmuyor."
        finish_reason = "stop"; completion_tokens = 42; forced_close = False; reasoning_len = 10
    r = kayit(_raft("Soru?", "6098", "MADDE 344"), 7, G())
    assert r["tip"] == "m1_yeterli"
    assert r["mode"] == "data"
    assert r["id"] == "raft7"
    assert r["soru"] == "Soru?"
    assert r["chosen"].startswith("1) İlgili kaynak")
    assert r["rejected"].startswith("Verilen kaynaklarda")
    assert r["context_shown"].startswith("[KAYNAK 1]")
    assert set(r) >= {"id", "tip", "soru", "chosen", "rejected", "context_shown", "mode",
                      "gold_kanun_no", "gold_madde_no", "finish_reason", "completion_tokens",
                      "forced_close", "reasoning_len"}
```

→ **verify:** dosya yazıldı.

- [ ] **Adım 3.2 — Testi koş, DÜŞTÜĞÜNÜ gör**

```bash
source ~/code/global_venv/bin/activate && python -m pytest tests/test_b10_hasat.py -v
```
Beklenen: `ModuleNotFoundError: No module named 'b10_hasat'` → **FAIL**.

→ **verify:** çıktıda FAIL ve sebebi modülün yokluğu.

- [ ] **Adım 3.3 — `scripts/b10_hasat.py` yaz**

```python
#!/usr/bin/env python3
"""B10 hasadı — altın madde BAĞLAMDAYKEN üretilen gerçek aşırı-redler (`τ_a` v2'nin `rejected`'ı).

`τ_a` v1'in eğitim setinde "altın varken CEVAPLA" yönünde tek bir tercih baskısı yok
(703 çiftin tamamı çekinme yönünde; 142 grounding replay `is_pref=0` → OR maskeli). Bu betik
eksik sınıfın negatif tarafını toplar: model altın maddeyi görüp yine de çekindiyse, o çekinme
`rejected` olur; `chosen` aynı kalemin `raft_scrubbed` grounded hedefidir.

⚠️ ÜRETİM YOLU `gen_eval_grounded.generate_http` — yeniden yazılmaz (ikinci bir üretim gövdesi
tam olarak sessiz protokol sapması üretir).

⚠️ KABUL ÖLÇÜTÜ `exact_reject(cevap, "data")` — `harness_tablo.py:111`'in B10'u saydığı BİREBİR
aynı çağrı. Tuzak 4.7: hasadın kabul ölçütü, o veriyle eğitilen kolun RAPORLANACAĞI metrikle
aynı olmalı.

⚠️ İSTEM ÖNSÖZSÜZ. ADR-0058 ana protokolü önsözlü yaptı, ama mevcut 703 çekinme çifti önsözsüz
hasat edildi. İki istemi karıştırmak modele "önsöz varsa cevapla, yoksa çekin" kısayolunu
öğretir — tam ters kalibrasyon, ve hiçbir yerde hata vermez. Gerekçe ADR-0059 §sapma-1.

Kullanım:
  # PİLOT
  python scripts/b10_hasat.py --limit 150 --out data/_ham_ve_ara/b10_pilot.jsonl
  # ÜRETİM
  python scripts/b10_hasat.py --target 250 --out data/_ham_ve_ara/b10_kabul.jsonl
"""
import argparse
import json
import os
import random
import re
import sys
import threading
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gen_eval_grounded import generate_http          # noqa: E402  — TEK üretim gövdesi
from score_abstention import exact_reject            # noqa: E402  — TEK regex kaynağı

HAVUZ = "data/train/raft_scrubbed/train.jsonl"
DEV_YOLLARI = ["data/eval/dev/core_hard.jsonl", "data/eval/canon/core_hard.jsonl"]
MODE = "data"                                        # harness_tablo.py:111 ile birebir


def _soru(rec):
    """Soru metni. `raft_scrubbed` ve `data/eval/*` kalemlerinin İKİSİ de `messages` kullanır.

    ⚠️ `rec.get("soru")` yazma tuzağı: `data/eval/dev/core_hard.jsonl`'de `soru` alanı YOKTUR
    (anahtarlar: messages · kanun_adi · kanun_no · madde_no · _complexity · _src_len · _set).
    `.get("soru", "")` boş dize döndürür, süzgeç NO-OP olur ve sızıntı sessizce eğitime girer.
    """
    msgs = rec.get("messages")
    if msgs:
        for m in msgs:
            if m.get("role") == "user" and "SORU:" in m.get("content", ""):
                return m["content"].split("SORU:")[-1].strip()
    s = (rec.get("soru") or "").strip()
    if not s:
        raise ValueError(f"soru metni çıkarılamadı: anahtarlar={sorted(rec)}")
    return s


def _baglam(rec):
    """KAYNAKLAR bloğu — `raft_scrubbed` onu ZATEN 900-klipli kurmuş (ADR-0013 eval aynası)."""
    u = rec["messages"][1]["content"]
    return u.split("KAYNAKLAR:\n", 1)[1].rsplit("\n\nSORU:", 1)[0]


def _anahtar(kanun, madde):
    """(kanun_no, madde_no) normalize — külliyatta HEM 'Madde 42' HEM 'MADDE 14' var."""
    m = re.sub(r"[^0-9A-Za-zÇĞİÖŞÜçğıöşü/]", "", str(madde or "")).upper()
    return (str(kanun or "").strip(), m)


def sizinti_suz(satirlar, dev_yollari):
    """DEV/CANON'a değen kalemleri at — SORU metni VE ALTIN MADDE düzeyinde.

    # Why madde düzeyi de: soru düzeyinde kesişim ölçüldü ve 0, ama ALTIN MADDE düzeyinde
    # 67/70 örtüşüyor. `τ_g` v1'de bu hijyen yok (pre-existing, düzeltilmiyor); yeni kol için
    # bedeli ~%2,5 havuz kaybı, karşılığı temiz bir DEV ölçümü.
    """
    yasak_soru, yasak_madde = set(), set()
    for yol in dev_yollari:
        if not os.path.exists(yol):
            raise FileNotFoundError(f"sızıntı süzgeci kaynağı yok: {yol}")
        with open(yol, encoding="utf-8") as f:
            for satir in f:
                if not satir.strip():
                    continue
                d = json.loads(satir)
                yasak_soru.add(_soru(d))          # boş dönerse ValueError — no-op süzgeç YASAK
                yasak_madde.add(_anahtar(d.get("kanun_no"), d.get("madde_no")))
    return [r for r in satirlar
            if _soru(r) not in yasak_soru
            and _anahtar(r.get("gold_kanun_no"), r.get("gold_madde_no")) not in yasak_madde]


def kayit(rec, i, g):
    """Hasat kaydı. `chosen` kalemin KENDİ grounded hedefi — dış model kullanılmaz (ADR-0051 m.2)."""
    return {
        "id": f"raft{i}", "tip": "m1_yeterli", "soru": _soru(rec),
        "chosen": rec["messages"][2]["content"],
        "rejected": g.text,
        "context_shown": _baglam(rec),
        "mode": MODE,
        "gold_kanun_no": rec.get("gold_kanun_no"), "gold_madde_no": rec.get("gold_madde_no"),
        "finish_reason": g.finish_reason, "completion_tokens": g.completion_tokens,
        "forced_close": g.forced_close, "reasoning_len": g.reasoning_len,
    }


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--havuz", default=HAVUZ)
    p.add_argument("--out", required=True)
    p.add_argument("--limit", type=int, default=0, help="kaç ÜRETİM denenecek (pilot)")
    p.add_argument("--target", type=int, default=0, help="kaç KABUL edilene kadar (üretim)")
    p.add_argument("--seed", type=int, default=3407)
    p.add_argument("--server-url", default="http://127.0.0.1:8080/v1")
    p.add_argument("--server-model", default="local")
    p.add_argument("--think-budget", type=int, default=1024)   # ADR-0043 rejim değişmezi
    p.add_argument("--max-new-tokens", type=int, default=512)  # ADR-0043 rejim değişmezi
    p.add_argument("--concurrency", type=int, default=1, help="sunucunun -np değeriyle EŞLEŞMELİ")
    return p.parse_args()


def _devam(yol):
    if not os.path.exists(yol):
        return set()
    with open(yol, encoding="utf-8") as f:
        return {json.loads(l)["id"] for l in f if l.strip()}


def main():
    a = parse_args()
    if not (a.limit or a.target):
        raise SystemExit("--limit (pilot) ya da --target (üretim) ver")

    with open(a.havuz, encoding="utf-8") as f:
        satirlar = [json.loads(l) for l in f if l.strip()]
    grounded = [r for r in satirlar if r.get("slice") == "grounded"]
    temiz = sizinti_suz(grounded, DEV_YOLLARI)
    print(f"[b10] havuz {len(grounded)} → sızıntı süzgecinden sonra {len(temiz)} "
          f"(atılan {len(grounded) - len(temiz)})")

    isler = list(enumerate(temiz))
    random.Random(a.seed).shuffle(isler)
    gorulen = _devam(a.out)
    isler = [(i, r) for i, r in isler if f"raft{i}" not in gorulen]

    from openai import OpenAI
    client = OpenAI(base_url=a.server_url, api_key=os.environ.get("OPENAI_API_KEY", "none"),
                    max_retries=int(os.environ.get("LLM_MAX_RETRIES", "8")),
                    timeout=float(os.environ.get("LLM_TIMEOUT_S", "300")))

    kilit = threading.Lock()
    denenen = kabul = 0
    t0 = time.time()
    cikti = open(a.out, "a", encoding="utf-8")

    def uret(is_):
        nonlocal denenen, kabul
        i, rec = is_
        try:
            g = generate_http(client, a.server_model, _soru(rec), a.max_new_tokens,
                              sources_block=_baglam(rec), thinking="on",
                              think_budget=a.think_budget, server_url=a.server_url)
        except Exception as e:
            print(f"  id=raft{i} üretim hatası: {e}", flush=True)
            return None
        with kilit:
            denenen += 1
            n = denenen
        # KABUL: model altın bağlamdayken ÇEKİNDİYSE bu bir B10 örneğidir.
        if not exact_reject(g.text, MODE):
            if n % 25 == 0:
                print(f"  denenen={n} kabul={kabul} oran={kabul/n:.3f} "
                      f"| {(time.time()-t0)/n:.2f} s/üretim", flush=True)
            return None
        return kayit(rec, i, g)

    limit = a.limit or len(isler)
    with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
        kuyruk, sira = set(), iter(isler[:limit])
        for _ in range(a.concurrency):
            nxt = next(sira, None)
            if nxt is not None:
                kuyruk.add(ex.submit(uret, nxt))
        while kuyruk:
            bitti, kuyruk = wait(kuyruk, return_when=FIRST_COMPLETED)
            for f in bitti:
                r = f.result()
                if r:
                    with kilit:
                        kabul += 1
                    cikti.write(json.dumps(r, ensure_ascii=False) + "\n")
                    cikti.flush()
            if a.target and kabul >= a.target:
                break
            for _ in bitti:
                nxt = next(sira, None)
                if nxt is not None:
                    kuyruk.add(ex.submit(uret, nxt))
    cikti.close()

    kunye = {
        "denenen": denenen, "kabul": kabul,
        "kabul_orani": round(kabul / denenen, 4) if denenen else 0.0,
        "havuz_ham": len(grounded), "havuz_temiz": len(temiz),
        "seed": a.seed, "think_budget": a.think_budget, "max_new_tokens": a.max_new_tokens,
        "server_model": a.server_model, "mode": MODE, "sufficiency_preamble": False,
        "s_uretim": round((time.time() - t0) / denenen, 3) if denenen else 0.0,
    }
    with open(a.out.replace(".jsonl", "_KUNYE.json"), "w", encoding="utf-8") as f:
        json.dump(kunye, f, ensure_ascii=False, indent=2)
    print(f"[b10] BİTTİ · {json.dumps(kunye, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
```

→ **verify:** dosya yazıldı.

- [ ] **Adım 3.4 — Testi koş, GEÇTİĞİNİ gör**

```bash
source ~/code/global_venv/bin/activate && python -m pytest tests/test_b10_hasat.py -v
```
Beklenen: **4 passed**.

→ **verify:** çıktıda `4 passed`.

- [ ] **Adım 3.5 — Sızıntı süzgecini GERÇEK veride ölç**

```bash
source ~/code/global_venv/bin/activate
python -c "
import sys, json; sys.path.insert(0,'scripts')
from b10_hasat import sizinti_suz, HAVUZ, DEV_YOLLARI
g=[json.loads(l) for l in open(HAVUZ, encoding='utf-8') if l.strip()]
g=[r for r in g if r.get('slice')=='grounded']
t=sizinti_suz(g, DEV_YOLLARI)
print(f'ham {len(g)} → temiz {len(t)} · atılan {len(g)-len(t)} (%{100*(len(g)-len(t))/len(g):.1f})')
"
```

→ **verify:** atılan oran **%1-8** bandında. **%0 ise süzgeç çalışmıyor** (madde-anahtar
normalizasyonu bozuk) — durdur, düzelt. %20'nin üstündeyse fazla eliyor — durdur, incele.

- [ ] **Adım 3.6 — Sunucuyu aç (çıplak base)**

```bash
cd ~/code/llama.cpp 2>/dev/null || cd "$(dirname "$(command -v llama-server)")"
llama-server -m ~/code/Hukuk-SLM/models/gguf/q35-4b-q4_k_m.gguf \
  -c 8192 --cache-type-k q8_0 --cache-type-v q8_0 -np 4 --port 8080 &
sleep 30 && curl -s http://127.0.0.1:8080/health
```

→ **verify:** `{"status":"ok"}`. ⚠️ Dizüstü **şarjda** olmalı (tuzak 1.6: pilde 7,9 t/s ↔
şarjda 134 t/s). Şarj durumu pilot künyesine not edilir.

- [ ] **Adım 3.7 — PİLOT koş (150 üretim)**

```bash
cd ~/code/Hukuk-SLM && source ~/code/global_venv/bin/activate
python scripts/b10_hasat.py --limit 150 --concurrency 4 \
       --out data/_ham_ve_ara/b10_pilot.jsonl
```

→ **verify:** `data/_ham_ve_ara/b10_pilot_KUNYE.json` yazıldı ve içinde `kabul_orani` ile
`s_uretim` var.
- **`kabul_orani < 0,10` → 🛑 DUR** (durma koşulu 2). Havuz mu ölçüt mü sorusu cevaplanmadan
  hasat büyütülmez.
- `kabul_orani ≥ 0,10` → devam.

- [ ] **Adım 3.8 — 10 kabul edilen kalemi GÖZLE oku**

```bash
python -c "
import json
for i,l in enumerate(open('data/_ham_ve_ara/b10_pilot.jsonl', encoding='utf-8')):
    if i>=10: break
    d=json.loads(l)
    print('='*70); print('SORU     :', d['soru'][:120])
    print('REJECTED :', d['rejected'][:220])
    print('CHOSEN   :', d['chosen'][:220])
"
```

→ **verify:** 10/10 kalemde `rejected` **gerçekten bir çekinme** (cevap değil) ve `chosen`
**gerçekten o soruyu cevaplayan** grounded hedef. Bir tanesi bile uymuyorsa kabul ölçütü
yeniden düşünülür. *(ADR-0051 dersi: şablon çıktısı gözle okunmadan kabul edilmez.)*

- [ ] **Adım 3.9 — Hasat yerini ÖLÇÜMLE seç**

`s_uretim` × (250 ÷ `kabul_orani`) = tahmini yerel süre.
- ≤ 6 saat → **yerel gece koşusu ($0)**.
- \> 6 saat → **Modal** (`modal_train.py` içine `harvest_cp2` benzeri bir giriş noktası
  eklemek gerekir; o iş bu planın kapsamında **değil** → önce yerel dene).

→ **verify:** karar ve dayandığı sayı `data/_ham_ve_ara/b10_pilot_KUNYE.json` yanına bir
satırla yazıldı.

- [ ] **Adım 3.10 — Commit**

```bash
git add scripts/b10_hasat.py tests/test_b10_hasat.py
git commit -m "G3: b10_hasat.py — altın bağlamdayken çekinme hasadı + sızıntı süzgeci (soru VE madde)"
```

→ **verify:** `git log --oneline -1`. ⚠️ `data/_ham_ve_ara/` git'e **girmez** (ara veri).

---

# GÖREV 4 — Üretim hasadı

**Hedef:** ~**250** kabul. Gerekçe: RAG_MULTI kalıbındaki mevcut çekinme çifti sayısı **188**;
~250 pozitif çift o kalıpta kabaca 1:1 denge kurar.

- [ ] **Adım 4.1 — Koş**

```bash
cd ~/code/Hukuk-SLM && source ~/code/global_venv/bin/activate
python scripts/b10_hasat.py --target 250 --concurrency 4 \
       --out data/_ham_ve_ara/b10_kabul.jsonl 2>&1 | tee /tmp/b10_hasat.log
```

→ **verify:** `wc -l data/_ham_ve_ara/b10_kabul.jsonl` ≥ 200. 250'ye ulaşılamadıysa havuz
tükenmiştir; gerçek sayı künyeye yazılır ve **eksiklik gizlenmez**.

- [ ] **Adım 4.2 — Tekilleştir ve şemayı doğrula**

```bash
python -c "
import json
sat=[json.loads(l) for l in open('data/_ham_ve_ara/b10_kabul.jsonl', encoding='utf-8') if l.strip()]
ids=[s['id'] for s in sat]
print('satır', len(sat), '· tekil id', len(set(ids)))
assert len(ids)==len(set(ids)), 'YİNELENEN id — tuzak 6.10'
zorunlu={'id','tip','soru','chosen','rejected','context_shown','mode','gold_kanun_no','gold_madde_no'}
assert all(zorunlu <= set(s) for s in sat), 'eksik alan'
assert all(s['tip']=='m1_yeterli' for s in sat)
print('şema ✓')
"
```

→ **verify:** çıktıda `şema ✓` ve yinelenen id yok.

---

# GÖREV 5 — `build_orpo_v3.py` genişletmesi + paketleme

**Dosyalar:**
- Değiştir: `scripts/build_orpo_v3.py` — `cp2c_cifti()` fonksiyonuna `m1_yeterli` dalı + rapor sayacı
- Oluştur: `data/train/orpo_abstain_v2/` (`train.jsonl` · `validation.jsonl` · `orpo_report.json`)

**Tüketir:** Görev 4'ün `b10_kabul.jsonl`'i · mevcut `cp2c_kabul_m2.jsonl` · `cp2c_kabul_m2b.jsonl`.
**Üretir:** `data/train/orpo_abstain_v2/` — `train_orpo.py --data` bunu **dizin** olarak bekler.

- [ ] **Adım 5.1 — Mevcut kabul dosyalarını doğrula (yerleri BULUNDU, 2026-08-06)**

`τ_a` v1'in havuzu **dört dosyaya** bölünmüş — ikisi değil (`orpo_report.json`'daki
`hasat_kaynak_karisimi`: `cp2c 3 · cp2c-64 357 · cp2c-ek1 366`):

```bash
wc -l outputs/eval/cp2c-kabul/cp2c_kabul_m2.jsonl \
      outputs/eval/cp2c-kabul/cp2c_kabul_m2b.jsonl \
      outputs/eval/cp2c-kabul-ek1/cp2c_kabul_m2.jsonl \
      outputs/eval/cp2c-kabul-ek1/cp2c_kabul_m2b.jsonl
```

→ **verify:** sırasıyla **272 · 90 · 266 · 100** (toplam 728). m2 = 272+266 = **538** ✓ ·
m2b = 90+100 = **190** (rapordaki 188 + 2 `dev_excluded`) ✓. Sayılar tutmuyorsa dosyalar
değişmiş demektir — **devam edilmez**, yeniden üretilecek set eskisini kapsamak zorunda.

- [ ] **Adım 5.2 — `cp2c_cifti`'ye `m1_yeterli` dalını ekle**

`scripts/build_orpo_v3.py` içindeki `cp2c_cifti` fonksiyonunda, `if r["tip"] == "m2b":`
satırından **önce** şu dalı ekle:

```python
    if r["tip"] == "m1_yeterli":
        # ⭐ ADR-0059 — eksik SINIF: altın BAĞLAMDA, doğru davranış CEVAPLAMAK.
        # `τ_a` v1'de bu yönde tek bir tercih baskısı yoktu (703 çiftin tamamı çekinme yönünde;
        # grounding replay `is_pref=0` → OR maskeli, kontrast üretmiyor). m2b çiftiyle AYNI
        # kalıp, AYNI komşu-öncelikli çeldirici profili; tek fark altının bağlamda OLMASI.
        # `rejected` bu yüzden m2b'nin `chosen`'ıyla aynı cümledir — aynı dize altın yokken
        # yukarı, altın varken aşağı itilir. Kaybın düşebileceği tek yol YETERLİLİĞİ okumaktır.
        ch = r.get("chosen")
        if not ch:
            return None
        return {
            "prompt": [{"role": "system", "content": SYSTEM_PROMPT_RAG_MULTI},
                       {"role": "user", "content": f"KAYNAKLAR:\n{ctx}\n\nSORU: {soru}"}],
            "chosen": [{"role": "assistant", "content": ch}],
            "rejected": [{"role": "assistant", "content": r["rejected"]}],
            "is_pref": 1,
            "_kind": "yeterli", "_mod": "m1_yeterli", "_kaynak": r.get("kaynak"),
            "_hi_overlap": False,
        }
```

→ **verify:** `python -c "import ast,sys; ast.parse(open('scripts/build_orpo_v3.py').read())"`
hata vermiyor.

- [ ] **Adım 5.3 — Rapor sayacını genişlet**

`build_orpo_v3.py`'de `abstain_mod_karisimi` sayacını üreten yeri bul ve `_kind == "yeterli"`
satırlarını ayrı bir alana say: `yeterli_cift_sayisi`. Ayrıca `orpo_report.json`'a şu alanı ekle:

```python
        "cift_dengesi": {
            "m2b_cekinme": sum(1 for x in satirlar if x.get("_mod") == "m2b"),
            "m1_yeterli":  sum(1 for x in satirlar if x.get("_mod") == "m1_yeterli"),
        },
```

→ **verify:** `grep -n "cift_dengesi\|yeterli_cift_sayisi" scripts/build_orpo_v3.py` eşleşme verir.

- [ ] **Adım 5.4 — SMOKE: küçük fixture ile paketle**

```bash
source ~/code/global_venv/bin/activate
head -20 data/_ham_ve_ara/b10_kabul.jsonl > /tmp/b10_smoke.jsonl
python scripts/build_orpo_v3.py --rejected /tmp/b10_smoke.jsonl --out-dir /tmp/orpo_smoke
python -c "
import json
sat=[json.loads(l) for l in open('/tmp/orpo_smoke/train.jsonl', encoding='utf-8')]
y=[s for s in sat if s.get('_mod')=='m1_yeterli']
print('yeterli çift:', len(y))
d=y[0]
assert d['is_pref']==1
assert d['prompt'][1]['content'].startswith('KAYNAKLAR:')
assert 'bulunmuyor' in d['rejected'][0]['content'] or 'bulunmamaktadır' in d['rejected'][0]['content']
print('SMOKE ✓')
print(d['prompt'][1]['content'][:200]); print('---'); print(d['rejected'][0]['content'][:200])
"
```

→ **verify:** `SMOKE ✓` ve basılan istem/rejected **gözle okunup** doğru bulundu.
*(Tuzak 4.6: veri şeması sessizce yanlış olabilir; her veri üretiminden sonra küçük smoke.)*

- [ ] **Adım 5.5 — Tam seti paketle**

```bash
source ~/code/global_venv/bin/activate
python scripts/build_orpo_v3.py \
  --rejected outputs/eval/cp2c-kabul/cp2c_kabul_m2.jsonl \
             outputs/eval/cp2c-kabul/cp2c_kabul_m2b.jsonl \
             outputs/eval/cp2c-kabul-ek1/cp2c_kabul_m2.jsonl \
             outputs/eval/cp2c-kabul-ek1/cp2c_kabul_m2b.jsonl \
             data/_ham_ve_ara/b10_kabul.jsonl \
  --out-dir data/train/orpo_abstain_v2
cat data/train/orpo_abstain_v2/orpo_report.json
```

→ **verify:** rapor şunları göstermeli:
- `abstain_mod_karisimi`: `m2` = **538** · `m2b` = **188** (**v1 ile birebir** — eski çiftler korunmuş)
- `cift_dengesi.m1_yeterli` ≥ 200
- `skipped.no_chosen` == 0
- `total` ≈ 1.100

Eski çift sayıları **düştüyse** eski kabul dosyaları eksik verilmiştir → durdur, düzelt.

- [ ] **Adım 5.6 — DEV/CANON sızıntısını SET ÜZERİNDE bir kez daha ölç**

```bash
source ~/code/global_venv/bin/activate
python -c "
import json
def soru(u): return u.split('SORU:')[-1].strip()
tr={soru(json.loads(l)['prompt'][1]['content']) for l in open('data/train/orpo_abstain_v2/train.jsonl', encoding='utf-8')}
for p in ['data/eval/dev/core_hard.jsonl','data/eval/canon/core_hard.jsonl','data/eval/dev/trap.jsonl']:
    ev={(json.loads(l).get('soru') or '').strip() for l in open(p, encoding='utf-8') if l.strip()}
    print(p, 'kesişim =', len(tr & ev))
"
```

→ **verify:** üç satırda da **kesişim = 0**. Sıfır değilse eğitim **başlatılmaz** (tuzak 4.1).

- [ ] **Adım 5.7 — Token bütçesi: truncation kapısı**

⚠️ `measure_token_budget.py` **kullanılamaz**: `--data` bir **jsonl** bekliyor ve satırlarda
`messages` arıyor; ORPO satırlarının şeması `prompt`/`chosen`/`rejected`. Bayrağı da
`--max-seq-len` (`--max-length` yok). ORPO'nun kendi iki sınırı için doğrudan ölçüm:

```bash
source ~/code/global_venv/bin/activate
python - <<'PY'
import json
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B")
MAX_PROMPT, MAX_LEN = 1536, 2048          # train_orpo.py varsayılanları
dusen = kesik = n = 0
for l in open("data/train/orpo_abstain_v2/train.jsonl", encoding="utf-8"):
    d = json.loads(l); n += 1
    p = len(tok.apply_chat_template(d["prompt"], tokenize=True, add_generation_prompt=True))
    for taraf in ("chosen", "rejected"):
        c = len(tok(d[taraf][0]["content"])["input_ids"])
        if p >= MAX_PROMPT:               # istem tek başına sınırı doldurdu → label yok
            dusen += 1; break
        if p + c > MAX_LEN:               # cevap ortasında kesildi → yarım cevap öğretimi
            kesik += 1; break
print(f"n={n} · DÜŞEN={dusen} (%{100*dusen/n:.2f}) · KESİK={kesik} (%{100*kesik/n:.2f})")
PY
```

→ **verify:** `DÜŞEN + KESİK` oranı **≤ %1**. Üstündeyse **koşma** (tuzak 4.3: yarım cevap
öğretimi, uyarısız) — sınırlar yeniden düşünülür ve gerekçesi yazılır.
⚠️ Bu ölçüm `τ_a` v1 setinde de koşulup **kıyaslanır**; v2 belirgin biçimde kötüyse suçlu
büyüyen `chosen` tarafıdır (RAFT şablonu uzun).

- [ ] **Adım 5.8 — Commit**

```bash
git add scripts/build_orpo_v3.py
git commit -m "G5: build_orpo_v3 — m1_yeterli çift tipi (ADR-0059, eksik pozitif sınıf)"
```

→ **verify:** `git log --oneline -1`. ⚠️ `data/train/orpo_abstain_v2/` boyutuna göre git'e
girer ya da girmez — `git check-ignore -v data/train/orpo_abstain_v2/train.jsonl` ile kontrol et.

---

# GÖREV 6 — `τ_a` v2 eğitimi (Modal)

**Bedel:** ~$1,30 · **Rejim `τ_a` v1 ile BİREBİR** — değişen tek şey veri.

- [ ] **Adım 6.1 — Veriyi Modal volume'a yükle**

```bash
source ~/code/global_venv/bin/activate
modal volume put hukuk-data data/train/orpo_abstain_v2 /orpo_abstain_v2
modal volume ls hukuk-data /orpo_abstain_v2
```

→ **verify:** `train.jsonl` **ve** `validation.jsonl` listede. ⚠️ `--data` **konteyner** yoludur
(tuzak 3.6); yerel yol verilirse koşu yanar.

- [ ] **Adım 6.2 — Çakışan canlı iş var mı**

```bash
modal app list | grep -i orpo
```

→ **verify:** canlı ORPO işi **yok**. Varsa yeni koşu **başlatılmaz** (tuzak 6.10: iki detached
iş aynı çıktıya yazar, künyeyi son biten yeniden yazar).

- [ ] **Adım 6.3 — SMOKE (50 adım) — format + loss + OOM**

```bash
modal run --detach modal_train.py::spawn_orpo \
  --model Qwen/Qwen3.5-4B --data /data/orpo_abstain_v2 --run-name ta_v2 --smoke \
  --beta 0.1 --lr 1e-5 --grad-accum 64 --bf16-base --lora-dropout 0.05 \
  --target-modules "q_proj k_proj v_proj o_proj in_proj_qkv in_proj_z in_proj_a in_proj_b gate_proj up_proj down_proj"
```

→ **verify:** logda **`Trainable parameters = 29,908,992`** görünüyor (τ_g/τ_a v1 ile birebir) ·
turn-işareti assert'i tetiklendi · loss sayı üretiyor (NaN değil) · OOM yok.
⚠️ `--adapter` **verilmedi** → taze adaptör, ham base'den (tuzak 3.8: `--adapter` ardışık SFT
üretir ve merge'i geçersiz kılar).

- [ ] **Adım 6.4 — Gerçek koşu (5 epoch)**

```bash
modal run --detach modal_train.py::spawn_orpo \
  --model Qwen/Qwen3.5-4B --data /data/orpo_abstain_v2 --run-name ta_v2 --epochs 5 \
  --beta 0.1 --lr 1e-5 --grad-accum 64 --bf16-base --lora-dropout 0.05 --save-steps 100 \
  --target-modules "q_proj k_proj v_proj o_proj in_proj_qkv in_proj_z in_proj_a in_proj_b gate_proj up_proj down_proj"
```

→ **verify:** *"SPAWNED ✓"* mesajı işin koştuğunu **KANITLAMAZ** (tuzak 6.1). Doğrulama:
```bash
modal volume ls hukuk-outputs /ta_v2
```
Çıktı dosyaları gerçekten yazılmış olmalı.

- [ ] **Adım 6.5 — Adaptörü indir ve ARTEFAKT kapısını koş**

```bash
source ~/code/global_venv/bin/activate
modal volume get hukuk-outputs /ta_v2 outputs/ta_v2
python -c "
from safetensors.torch import load_file
import glob
p=glob.glob('outputs/ta_v2/**/adapter_model.safetensors', recursive=True)[0]
t=load_file(p); n=sum(v.numel() for v in t.values())
print('tensör', len(t), '· parametre', n)
assert len(t)==448, f'tensör {len(t)} ≠ 448 — rejim sapması'
assert n==29_908_992, f'parametre {n} ≠ 29.908.992 — target_modules sapması'
print('ARTEFAKT KAPISI ✓')
"
```

→ **verify:** `ARTEFAKT KAPISI ✓`. *Ders (#48): bir kapının ölçütü mümkünse **artefakt** olmalı,
log satırı değil.*

- [ ] **Adım 6.6 — `‖τ_a v2‖`'yi ölç ve raporla**

```bash
source ~/code/global_venv/bin/activate
python -c "
from safetensors.torch import load_file
import glob, math
p=glob.glob('outputs/ta_v2/**/adapter_model.safetensors', recursive=True)[0]
t=load_file(p)
# ΔW = (alpha/r)·BA — merge_ties.py'nin kullandığı ölçek (r=16, alpha=32 → 2.0)
kare=0.0
import torch, re
A={k:v for k,v in t.items() if 'lora_A' in k}
for ka,va in A.items():
    kb=ka.replace('lora_A','lora_B')
    if kb in t:
        dW = 2.0 * (t[kb].float() @ va.float())
        kare += float((dW**2).sum())
print(f'‖τ_a v2‖_F = {math.sqrt(kare):.4f}   (τ_a v1 = 1,1806 · τ_g v1 = 10,4589)')
"
```

→ **verify:** sayı ekrana basıldı. **Ön-kayıtlı beklenti 1,18 ± %25 (0,89 – 1,48).** Bandın
dışındaysa bu **B4 eksenine dokunulduğu** anlamına gelir ve `research_log`'a öyle geçer —
sonuçlar o şerhle okunur. Koşu iptal edilmez; şerh gizlenmez.

- [ ] **Adım 6.7 — `kollar.md`'ye satır ekle ve commit**

`docs/record/kollar.md` "Kollar" tablosuna:

```
| `τ_abstention` | **v2** | 2026-08-XX | 🟢 aktif | <N> adım (5 epoch) · lr 1e-5 · beta 0.1 · etkin batch 64 · r=16/α=32 · dropout 0.05 · 224 LoRA çifti · `--fresh-adapter` · seed 3407 · veri `data/train/orpo_abstain_v2/` (m2 538 + m2b 188 + **m1_yeterli <M>** + replay) | **<‖τ‖>** | `*_ta_v2_th` | [#58](...) |
```

```bash
git add docs/record/kollar.md && git commit -m "G6: τ_a v2 eğitildi — kol kaydına satır (‖τ‖ <değer>)"
```

→ **verify:** `git log --oneline -1`; satırdaki `‖τ‖` Adım 6.6'nın ölçtüğü sayı.

---

# GÖREV 7 — 🛑 KOL KAPISI (merge'den ÖNCE)

**Bedel:** ~$0,10 · **Bu kapı düşerse tur DURUR** — merge edilmez, ürün eval'i koşulmaz.

- [ ] **Adım 7.1 — `τ_a` v2'yi merge et + GGUF'a çevir (tek kol)**

```bash
source ~/code/global_venv/bin/activate
python scripts/merge_lora.py --base Qwen/Qwen3.5-4B --adapter outputs/ta_v2 \
       --out models/merged/ta_v2
# GGUF — imza: setup_llamacpp.sh <dizin> [etiket], quant ENV ile (scripts/cp3_merge_dene.sh:36)
# ⚠️ PURE=0 ZORUNLU: Qwen3.5-4B QAT DEĞİL. PURE=1 (ADR-0023) yalnız QAT-Q4_0 base'ler içindir;
#    burada kullanılırsa embedding gereksiz yere kaybeder.
QUANT=Q4_K_M PURE=0 bash scripts/setup_llamacpp.sh models/merged/ta_v2 ta_v2
```

→ **verify:** `merge_lora.py` **224/224** uygulandı diyor (tuzak 5.2) **ve**
`ls -la models/gguf/ta_v2-q4_k_m.gguf` boyutu `q35-4b-q4_k_m.gguf` ile **aynı bantta**
(~2,59 GiB; tuzak 5.1 · 5.3).

- [ ] **Adım 7.2 — M1 + M2b koş (harness KAPALI, ana protokol)**

```bash
# sunucu: ta_v2 GGUF
llama-server -m models/gguf/ta_v2-q4_k_m.gguf -c 8192 --cache-type-k q8_0 --cache-type-v q8_0 -np 4 --port 8080 &
sleep 30 && curl -s http://127.0.0.1:8080/health

cd ~/code/Hukuk-SLM && source ~/code/global_venv/bin/activate
G="python scripts/gen_eval_grounded.py --server-url http://127.0.0.1:8080/v1 --server-model local \
   --thinking on --think-budget 1024 --max-new-tokens 512 --max-chunk-chars 900 --seed 3407 \
   --sufficiency-preamble --out-dir outputs/eval/g7-kol-kapisi"
$G --label m1_ta_v2  --data data/eval/dev/core_hard.jsonl --distractors 4 --n 80 \
   2>&1 | tee outputs/eval/g7-kol-kapisi/kosu.log
$G --label m2b_ta_v2 --data data/eval/dev/core_hard.jsonl --distractors 4 --no-gold --n 80 \
   2>&1 | tee -a outputs/eval/g7-kol-kapisi/kosu.log

kunye_yaz outputs/eval/g7-kol-kapisi '{
  "kosu": "G7 — KOL KAPISI: τ_a v2 tek başına, harness KAPALI",
  "ozne": "models/gguf/ta_v2-q4_k_m.gguf", "adaptor": "outputs/ta_v2",
  "etiketler": {"m1_ta_v2": {"distractors": 4}, "m2b_ta_v2": {"distractors": 4, "no_gold": true}},
  "thinking": "on", "think_budget": 1024, "max_new_tokens": 512, "max_chunk_chars": 900,
  "seed": 3407, "n": 80, "sufficiency_preamble": true, "veri": "data/eval/dev/core_hard.jsonl",
  "adr": ["ADR-0043", "ADR-0058", "ADR-0059"]
}'
```

→ **verify:** `KUNYE.json` yazıldı ve `thinking=on` · `think_budget=1024` ·
`max_chunk_chars=900` · `seed=3407` · `n=80` · `sufficiency_preamble=true` içeriyor.
Kesik oranı:
```bash
python -c "
import json
for L in ('m1_ta_v2','m2b_ta_v2'):
    d=[json.loads(l) for l in open(f'outputs/eval/g7-kol-kapisi/{L}_detail.jsonl', encoding='utf-8')]
    kesik=sum(1 for x in d if x.get('finish_reason')=='length')
    print(L, 'n=',len(d), 'kesik=', kesik, f'%{100*kesik/len(d):.1f}')
"
```
**Kesik oranı > %5 ise koşu geçersiz** — sayı raporlanmaz (tuzak 1.9).

- [ ] **Adım 7.3 — Skorla**

```bash
source ~/code/global_venv/bin/activate && set -a && . ./.env && set +a
export LLM_PROVIDER_ORDER=OpenAI
D=outputs/eval/g7-kol-kapisi
python scripts/groundedness.py     --details $D/m1_ta_v2_detail.jsonl --label m1_ta_v2 --out-dir $D
python scripts/rescore_answered.py --gnd $D/gnd_m1_ta_v2.jsonl --bench $D/m1_ta_v2_detail.jsonl \
                                   --label m1_ta_v2
python scripts/score_abstention.py --details $D/m2b_ta_v2_detail.jsonl --label m2b_ta_v2 --out-dir $D
python -c "
import sys, json; sys.path.insert(0,'scripts')
from score_abstention import exact_reject
d=[json.loads(l) for l in open('outputs/eval/g7-kol-kapisi/m1_ta_v2_detail.jsonl', encoding='utf-8')]
red=sum(exact_reject(x.get('cevap',''),'data') for x in d)
print(f'aşırı-red = {red}/{len(d)} = {red/len(d):.4f}   (base 0,425 · τ_a v1 0,575)')
"
```

→ **verify:** `rescore_answered` A1 == `groundedness` A1 (tuzak 2.16). Eşit değilse sayı
raporlanmaz.

- [ ] **Adım 7.4 — 🛑 KAPIYI UYGULA**

```
BAŞARILI   aşırı-red < 0,425  VE  M2b Rej ≥ 0,95  VE  M1 A1 ≥ 0,88
KISMİ      0,425 ≤ aşırı-red < 0,50  VE  M2b Rej ≥ 0,95    → merge, "kısmi" damgalı
BAŞARISIZ  aşırı-red ≥ 0,50  ya da  M2b Rej < 0,95
           → MERGE YOK · ÜRÜN EVAL'İ YOK · TUR DURUR
```

→ **verify:** üç sayı (aşırı-red · M2b Rej · M1 A1) ve **hangi banda düştüğü** açıkça yazıldı.
**BAŞARISIZ ise Görev 8-9 ATLANIR**, doğrudan Görev 10'a (negatif bulgu kaydı) geçilir.
⚠️ Geçerlilik kapısı düşerse reçeteye körü körüne uyulmaz.

- [ ] **Adım 7.5 — Commit**

```bash
git add outputs/eval/g7-kol-kapisi/
git commit -m "G7: KOL KAPISI — τ_a v2 tek başına (aşırı-red <x> · M2b <y> · A1 <z>) → <HÜKÜM>"
```

→ **verify:** commit mesajında üç sayı ve hüküm yazılı.

---

# GÖREV 8 — Merge (`tgta_v2`) + GGUF

**Ön koşul:** Görev 7 BAŞARILI ya da KISMİ. **Merge parametreleri v1 ile BİREBİR** — B4 ekseni açılmıyor.

- [ ] **Adım 8.1 — Ham TIES merge**

```bash
source ~/code/global_venv/bin/activate
python scripts/merge_ties.py --base Qwen/Qwen3.5-4B \
  --adapter tg=outputs/tg_v1 --adapter ta=outputs/ta_v2 \
  --no-norm-balance --trim-k 0.20 --lam 1.0 \
  --out models/merged/tgta_v2 \
  --kunye models/merged/tgta_v2/KUNYE_tgta_v2.json
```

⚠️ **`--kunye` varsayılanı BOŞ** (imza satır 65) — verilmezse merge künyesi (kol normları, TIES
istatistikleri) **hiç yazılmaz** ve `‖τ‖` kaydı kaybolur. `--trim-k`/`--lam` varsayılanları zaten
0,20/1,0 ama **açıkça yazılır**: bunlar v1 ile eşleşmesi gereken merge parametreleri ve
"varsayılan buydu" demek, künyeden okunabilir olmaktan zayıftır.

⚠️ `--no-norm-balance` = ham TIES ([ADR-0052](../../adr/0052-merge-norm-dengeleme-hukmu-tersine.md)).
trim_k 0,2 · λ 1,0 · eşzamanlı 2-yollu — **v1'in birebir aynısı**.

→ **verify:** çıktıda **224/224** tensör uygulandı **ve** `‖merged − base‖_F ≈ ‖τ‖` kapısı
geçti (tuzak 5.3). Künye `models/merged/tgta_v2/KUNYE_tgta_v2.json` yazıldı.

- [ ] **Adım 8.2 — Q4_K_M GGUF**

```bash
QUANT=Q4_K_M PURE=0 bash scripts/setup_llamacpp.sh models/merged/tgta_v2 tgta_v2
ls -la models/gguf/tgta_v2-q4_k_m.gguf models/gguf/q35-4b-q4_k_m.gguf
```

→ **verify:** iki dosya **aynı bantta** (~2,59 GiB). Küçükse kuantizasyon yarıda kesilmiştir
(tuzak 5.1) — dosya diskte durur ama geçersizdir.

- [ ] **Adım 8.3 — `kollar.md`'ye merge satırı + commit**

```bash
git add docs/record/kollar.md models/merged/tgta_v2/KUNYE_tgta_v2.json
git commit -m "G8: tgta_v2 merge (ham TIES, v1 parametreleri birebir)"
```

→ **verify:** `git log --oneline -1`.

---

# GÖREV 9 — 🛑 ÜRÜN KAPISI + ek ölçümler

**Bedel:** ~$0,30.

- [ ] **Adım 9.1 — Dört koşuyu üret**

```bash
llama-server -m models/gguf/tgta_v2-q4_k_m.gguf -c 8192 --cache-type-k q8_0 --cache-type-v q8_0 -np 4 --port 8080 &
sleep 30 && curl -s http://127.0.0.1:8080/health

cd ~/code/Hukuk-SLM && source ~/code/global_venv/bin/activate
B="python scripts/gen_eval_grounded.py --server-url http://127.0.0.1:8080/v1 --server-model local \
   --thinking on --think-budget 1024 --max-new-tokens 512 --max-chunk-chars 900 --seed 3407 \
   --data data/eval/dev/core_hard.jsonl --n 80 --out-dir outputs/eval/g9-urun-kapisi"

# 1) ANA: harness AÇIK k=10, ana protokol (önsözlü) → %62,8 çıpasına karşı
$B --label h1_tgta_v2 --harness-indeks data/index/mevzuat_bge_m3_s2 --harness-k 10 --sufficiency-preamble
# 2) ABLASYON: önsözsüz → %61,3 çıpasına karşı + Δ(önsöz) testi
$B --label h1_tgta_v2_onsozsuz --harness-indeks data/index/mevzuat_bge_m3_s2 --harness-k 10
# 3) M2b eşleşmiş sınav (ADR-0057 Kademe 2)
$B --label h2b_tgta_v2_k4 --harness-indeks data/index/mevzuat_bge_m3_s2 --harness-k 4 \
   --harness-no-gold --sufficiency-preamble
# 4) TAVAN: harness KAPALI M1 → 17/80 çıpasına karşı
$B --label m1_tgta_v2 --distractors 4 --sufficiency-preamble

kunye_yaz outputs/eval/g9-urun-kapisi '{
  "kosu": "G9 — ÜRÜN KAPISI: tgta_v2",
  "ozne": "models/gguf/tgta_v2-q4_k_m.gguf", "kollar": ["tg_v1", "ta_v2"], "merge": "ham TIES",
  "indeks": "data/index/mevzuat_bge_m3_s2", "korpus": "data/corpus/mevzuat_maddeler.jsonl",
  "etiketler": {
    "h1_tgta_v2":          {"harness_k": 10, "sufficiency_preamble": true},
    "h1_tgta_v2_onsozsuz": {"harness_k": 10, "sufficiency_preamble": false},
    "h2b_tgta_v2_k4":      {"harness_k": 4, "harness_no_gold": true, "sufficiency_preamble": true},
    "m1_tgta_v2":          {"harness": false, "distractors": 4, "sufficiency_preamble": true}},
  "thinking": "on", "think_budget": 1024, "max_new_tokens": 512, "max_chunk_chars": 900,
  "seed": 3407, "n": 80, "veri": "data/eval/dev/core_hard.jsonl",
  "cipa": {"kutle": 0.6275, "b10": "14/80", "a1": 0.8229},
  "adr": ["ADR-0043", "ADR-0052", "ADR-0057", "ADR-0058", "ADR-0059"]
}'
```

→ **verify:** `KUNYE.json` yazıldı ve **dört etiketin** bayrakları ayrı ayrı görünüyor
(özellikle `h1_tgta_v2_onsozsuz` için `sufficiency_preamble: false` — Δ(önsöz) testi buna dayanır).
Ardından:
```bash
python -c "
import json, glob
ids=None
for p in sorted(glob.glob('outputs/eval/g9-urun-kapisi/*_detail.jsonl')):
    d=[json.loads(l) for l in open(p, encoding='utf-8')]
    kesik=sum(1 for x in d if x.get('finish_reason')=='length')
    cur={str(x['id']) for x in d}
    print(p.split('/')[-1], 'n=',len(d), 'kesik=%.1f%%'%(100*kesik/len(d)))
    if ids is None: ids=cur
    else: assert ids==cur, 'ÖRNEKLEM KAYMASI — dört koşu aynı 80 id olmalı (tuzak 1.5)'
print('örneklem birebir aynı ✓')
"
```
Beklenen: dört dosyada da `n=80`, kesik ≤ %5, **örneklem birebir aynı ✓**.

- [ ] **Adım 9.2 — Skorla + çapraz doğrula**

```bash
source ~/code/global_venv/bin/activate && set -a && . ./.env && set +a
export LLM_PROVIDER_ORDER=OpenAI
D=outputs/eval/g9-urun-kapisi
for L in h1_tgta_v2 h1_tgta_v2_onsozsuz m1_tgta_v2; do
  python scripts/groundedness.py     --details $D/${L}_detail.jsonl --label $L --out-dir $D
  python scripts/rescore_answered.py --gnd $D/gnd_${L}.jsonl --bench $D/${L}_detail.jsonl --label $L
done
python scripts/score_abstention.py --details $D/h2b_tgta_v2_k4_detail.jsonl \
                                   --label h2b_tgta_v2_k4 --out-dir $D
python scripts/harness_tablo.py --details $D/h1_tgta_v2_detail.jsonl --gnd $D/gnd_h1_tgta_v2.jsonl \
                                --out $D/harness_tablo_h1_tgta_v2.json
```

→ **verify:** her etikette `harness_tablo` A1 == `rescore_answered` A1 **birebir** (tuzak 2.16).
⚠️ İmzalar: `rescore_answered` **`--gnd` + `--bench`** ister (`--details` DEĞİL) ·
`groundedness`/`score_abstention` `--out-dir` verilmezse `outputs/eval` köküne yazar ·
`harness_tablo`'da `--gnd` düşerse A1 **sessizce boş** kalır.

- [ ] **Adım 9.3 — Ayırt edici / belirsiz kırılımı (ADR-0054 K4 — ZORUNLU)**

```bash
source ~/code/global_venv/bin/activate
D=outputs/eval/g9-urun-kapisi
python scripts/harness_tablo.py --details $D/h1_tgta_v2_detail.jsonl --gnd $D/gnd_h1_tgta_v2.jsonl \
       --etiketler outputs/eval/s3-ayirt-edicilik/etiketler.jsonl \
       --out $D/harness_tablo_h1_tgta_v2_kirilim.json
```

→ **verify:** iki alt küme için ayrı `recall` · `coverage` · `A1` · `kütle` basıldı
(62 ayırt edici · 18 belirsiz). **Bundan sonra hiçbir harness sayısı bu ayrım yapılmadan
raporlanmaz.**

- [ ] **Adım 9.4 — 🛑 ÜRÜN KAPISINI UYGULA**

```
BAŞARILI   kütle > %62,8  VE  B10 < 14/80  VE  M2b Rej (h2b@k=4) ≥ 0,840
KISMİ      B10 < 14/80 ama kütle ±0,3 içinde → çekinme düzeldi, kayıp başka yerde; tanı OKUNUR
BAŞARISIZ  kütle < %62,5  ya da  B10 ≥ 14/80  → tgta_v1 ÜRÜN OLARAK KALIR
```

Ayrıca **hüküm üretmeyen ama zorunlu** üç okuma:

| ölçüm | çıpa | ne söyler |
| :--- | :--- | :--- |
| M2b Rej | 0,877 | ⭐ **mekanizma testi**: ≥0,877 yeterlilik öğrenildi · <0,84 kör kayma |
| Δ(önsöz) = ana − ablasyon | +1,43 p | daralıyorsa yetenek **varsayılan** oldu |
| harness KAPALI aşırı-red | 17/80 | tavan tarafı da hareket etti mi |

→ **verify:** üç kapı sayısı + üç ek okuma yazıldı ve hüküm ilan edildi.

- [ ] **Adım 9.5 — Rakip kıyasını kur (ADR-0057)**

Görev 2'nin FL sayılarıyla yan yana; **her satırda adillik hükmü**:

```
kademe  eksen                 kaynak   base   BİZ v2   FL(AÇIK)   hüküm
  2     M1 kütle (AÇIK)       10 ↔ 10   —      ?        ?         EŞLEŞMİŞ
  2     M2b Rej                4 ↔ 4    —      ?        ?         EŞLEŞMİŞ
  2     A1 (eşleştirilmiş)      —       ?      ?        ?         G1'in aleti
  3     M1 kütle (KAPALI)      5 ↔ —   56,7%   ?       72,9%      TAVAN — hüküm YOK
```

→ **verify:** hükümsüz satır yok; *"AÇIK burada geride"* cümlesi **Kademe 3 satırları için
kurulmadı**.

- [ ] **Adım 9.6 — Commit**

```bash
git add outputs/eval/g9-urun-kapisi/
git commit -m "G9: ÜRÜN KAPISI — tgta_v2 (kütle <x> · B10 <y>/80 · M2b <z>) → <HÜKÜM>"
```

→ **verify:** `git log --oneline -1`.

---

# GÖREV 10 — Kayıt (her hükümde koşulur, BAŞARISIZ dahil)

⚠️ Bu görev **atlanmaz**. Negatif sonuç da aynı titizlikle kaydedilir — bu hattın en değerli
bulgularının birkaçı kendi planlarının çürütülmesidir.

- [ ] **Adım 10.1 — ADR-0059'u yaz**

`docs/adr/0059-tau-a-v2-simetrik-yeterlilik-cifti.md`. Zorunlu bölümler:
- **Bağlam:** `τ_a` v1'in 703:0 asimetrisi + `build_orpo_v3.py:44` (`is_pref=0` → OR maskeli)
- **Ölçülmüş teşhis:** kol bazında aşırı-red (base 0,425 · `τ_g` 0,175 · **`τ_a` 0,575** · merge 0,212)
- **§2.1 B4–B10 antagonizması:** genlik bir çare değil **takas**
- **Karar:** simetrik yeterlilik çifti; aynı dize altın yokken yukarı, varken aşağı
- **Elenenler:** spec §4'ün yedi satırı, gerekçeleriyle
- **§sapma-1:** çiftler **önsözsüz** — ADR-0011 eval-ayna kuralından bilinçli sapma, gerekçesi
  istem-kısayolu riski
- **§sapma-2:** `chosen` RAFT şablonunu taşıyor (tuzak 2.10) — kusur `τ_g`'de zaten var, bu turda
  çözülmüyor; sahibi ADR-0041 seçenek D
- **§sapma-3:** hasat öznesi base, B10 `tgta_v1`'de yaşıyor — on-policy tanımı eğitilen modele göre
- **Ön-kayıtlı tahminler ve TUTUP TUTMADIĞI** (spec §6.3 tablosu, "çıkan" sütunu doldurulmuş)

→ **verify:** dosya yazıldı; sekiz bölüm de var; tahmin tablosunun "çıkan" sütunu **dolu**.

- [ ] **Adım 10.2 — `research_log` #57'yi yaz** *(YB1 + G1 + G2)*

`docs/record/research_log/2026-08-06-yb1-ve-rakip-kiyasi.md` — künye bloğu (model · indeks ·
rejim · hakem · koşular · maliyet · geçit) + üç bölüm: YB1 benimseme · eşleştirilmiş A1 ·
**Gemini FL harness AÇIK (3.1 ↔ 3.5)**. **Her sayı, yaşadığı dosyayla birlikte.**

Ayrıca **"Yeni doğan borçlar / kararlar"** tablosuna:

| # | ne | neden karar gerektiriyor |
| :--- | :--- | :--- |
| **YB4** 🆕 | **OpenAI-ailesi rakip (GPT-5.4 nano sınıfı) ölçülemiyor** — hakemimiz `gpt-4o-mini` aynı aile, ADR-0032 aile-dışlaması yasaklıyor | Eklemek **üç-aileli panelin açılmasını** gerektirir: `judge_agreement.py` var ama bu hattın hiçbir koşusunda kullanılmadı → κ ölçümü + tüm çıpaların yeniden türetilmesi. Kendi turunu ister |
| **YB5** 🆕 | **`ROADMAP` hedef cümlesi bayatladı** — *"önce Gemini 3.1 Flash-Lite'ı geçmek"*; giriş katmanı **2026-07-21'den beri 3.5 FL** | Hedef, bu turun ölçtüğü sayı **görüldükten sonra** güncellenir; ölçmeden güncellemek sayısız bir hedef yazmak olur. ROADMAP bunu zaten öngörmüştü (*"koşan bir hedef"*) |

→ **verify:** `docs/record/research_log/README.md`'ye #57 satırı eklendi, bağlantı çözülüyor,
ve YB4/YB5 borç tablosunda görünüyor.

- [ ] **Adım 10.3 — `research_log` #58'i yaz** *(tur)*

`docs/record/research_log/2026-08-XX-tau-a-v2-asiri-red.md`:
- Künye · kol kapısı · ürün kapısı · üç ek okuma
- **Ön-kayıtlı tahminlerin hükmü** — tutan da, ıskalayan da
- **Ders** bölümü (tek cümle, kalın)
- **Açık kalanlar** tablosu — B10 · B4 · B1 · B8 · B9 · B6 güncel durumlarıyla
- Yeni doğan borçlar / kararlar

→ **verify:** README'ye #58 satırı eklendi; borç tablosu `sprint3-part1.md` borç kuyruğuyla
tutarlı.

- [ ] **Adım 10.4 — Bayat tuzak damgasını düzelt**

`docs/record/yurutme-tuzaklari.md` satır 2.10 şu anda *"🔴 AÇIK — open_questions.md §13.8,
τ_a'dan önce karara bağlanmalı"* diyor. Oysa ADR-0041 **kabul edilmiş** ve kural
`groundedness.py:65-71`'de **canlı**. Korunma sütununu şuna çevir:

```
✅ ADR-0041 uygulandı (groundedness.py:65-71 — "KAYNAK SEÇİMİ/ELEME cümlesi İDDİA DEĞİL").
Muafiyet DAR. ⚠️ Düzeltmeden SONRA bile τ_g'nin hatalı-iddia oranı base'in 3,7 katı —
kalan açık GERÇEK, sahibi ADR-0041 seçenek D (RAFT 1. adımı + τ_g yeniden eğitimi).
```

→ **verify:** `grep -n "ADR-0041 uygulandı" docs/record/yurutme-tuzaklari.md` eşleşiyor ve
o satırda artık "🔴 AÇIK" yok.

- [ ] **Adım 10.5 — Planı kapat**

Bu dosyanın başına ✅ kapanış bloğu ekle: hüküm · üretilen artefaktlar · maliyet defteri
(gerçekleşen) · nereye devam edileceği. Ardından `docs/superpowers/plans/` altında kalır
(plan arşivlenmez; kapanan **icra** belgesi arşive taşınır).

→ **verify:** kapanış bloğu var ve bütçe defterinin "gerçekleşen" sütunu dolu.

- [ ] **Adım 10.6 — `CLAUDE.md`'de yalnız İŞARETÇİLERİ güncelle**

⚠️ **SAYI YAZMA.** Güncellenecekler: "Current state" bloğundaki ürün sayısı ve artefakt adı ·
research_log aralığı (#39-#58) · ADR aralığı (0059'a kadar) ·
*"Two things a new session must not get wrong"* bloğu (B10'un yeni durumu).

⚠️ **Adım 0.1b'nin işaretçisi geri alınır:** `TODO.md` ve `CLAUDE.md`'deki *"AKTİF PLAN: B10…"*
satırı, tur kapandığı için *"aktif plan yok"* hâline döner ve kapanan plana **kayıt olarak**
işaret eder. `TODO.md` baş bloğu, `#56` kapanışının biçimiyle yazılır (*"✅ … turu KAPANDI"* +
plan + sonuç bağlantısı + çıkanlar).

→ **verify:** `git diff CLAUDE.md` — eklenen satırlarda **ölçüm tablosu yok**, yalnız işaretçi
ve tek-satırlık durum.

- [ ] **Adım 10.7 — Son commit**

```bash
git add docs/ CLAUDE.md
git commit -m "#58: τ_a v2 turu kapandı — B10 <x>/80, ADR-0058/0059, tuzak 2.10 damgası düzeltildi"
```

→ **verify:** `git log --oneline -3` ve `git status` temiz.

---

## Öz-denetim — plan ↔ spec kapsaması

| spec bölümü | görev |
| :--- | :--- |
| §5 Kapsam adım 0 (YB1) | Görev 0 |
| §5 Kapsam adım 1 (eşleştirilmiş A1) | Görev 1 |
| §5 Kapsam adım 2 (Gemini FL harness AÇIK) | Görev 2 |
| §3.2 Hasat · §3.3 veri hijyeni | Görev 3-4 |
| §3 Karar (simetrik çift) | Görev 5 |
| §3.1 Rejim değişmez | Görev 6 |
| §6.1 Kol kapısı | Görev 7 |
| §3.1 merge · ADR-0052 | Görev 8 |
| §6.2 Ürün kapısı · §6.3 tahminler | Görev 9 |
| §7 sapmalar · §9 kayıt yükümlülükleri | Görev 10 |
| §8 durma koşulları | 3.7 (kabul<%10) · 7.4 (kol kapısı) · bütçe defteri · her koşunun geçerlilik kapısı |
