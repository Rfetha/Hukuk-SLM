# Yeni belge katmanı — tasarım (spec)

**Tarih:** 2026-09-06 · **branch:** `yeni-yeni` · **kaynak:** `DEVIR-PROMPT.md` *(silindi)* ⚰️ *(silindi 2026-09-07 — işi bitti; borç kuyruğu §5 [güncel plana](../plans/2026-09-07-hp-hat-a-hat-b.md) taşındı)* §10
**Statü:** insan onaylı (bu oturumda soru-cevapla kilitlendi) · **sonraki adım:** plan (`- [ ]` kutucuklu)

> **Bu belge ne:** silinen ileriye dönük belge katmanının yerine ne yazılacağının tasarımı **ve**
> bu oturumda verilen insan kararlarının kaydı. Sayılar hatırlanarak değil **kaynaklanarak** yazıldı;
> her nicelik yanında yaşadığı dosya var.

---

## 1. Bu oturumda KİLİTLENEN insan kararları

| # | soru | **KARAR** | sonucu |
| :-- | :--- | :--- | :--- |
| **S1** | ARA KAPI düşmüşken sürüm adı | **Sürüm ikiye ayrılır**: *ürün sürümü* (`v0.2` → `v1.0`) ↔ *iddia sürümü* ARA KAPI'ya bağlı kalır | ADR-0065 |
| **S2** | v1 harness'lı mı | **Evet** — ağırlık + retriever + indeks + **dağıtılan istem** + CLI | YB6 ve servis katmanı kritik yola girer |
| **S14/S6** | yeterlilik önsözü | **KALDIRILDI** — ürünün varsayılanı **önsözsüz** | manşet **%68,4 → %73,0**; ADR-0058 tersine → ADR-0063 |
| **S11** | arxiv | **Metodoloji paper'ı** (yan ürün) | Hat C |
| — | sıralama | **İki hat paralel**: paketleme ∥ model | Hat A ∥ Hat B |
| — | ölçüm harcaması | **Dördü de ödenecek** (rakip önsözsüz · 3.5 Flash · `SOURCE_CLIP` · `tgta_v1` VRAM) | Faz 0, ~$1,65 |
| — | `v1.0` çubuğu | **Üç maddeli kapı** · çıpa **Gemini 3.5 Flash (tam)** · **δ = 2 p** | ADR-0064, ön-kayıt |
| — | Faz 0 sırası | **Erişim onarımı rakip ölçümünden ÖNCE** | ~$1,35 tasarruf, aşağıda gerekçe |
| **B1** | isabetsizlik yöntemi | **Önce reddetme-örneklemesi** (mevcut alet), GRPO **ertelendi** | ADR-0066 |
| — | `referans-design-doc.md` | **SİLİNİR**, yerine **`docs/MIMARI.md`** yazılır | bu oturumun kapsamı 3 → 4 belge |

**AÇIK bırakılanlar** — belgelerde `AÇIK KARAR` damgalı duracak, sessizce kapatılmayacak:
**S5** (ikili oran çözünürlük sınırı) · **S7** (LoRA adaptörleri HF'ye) · **S8** (indeks dağıtımı) ·
**S9** (v2 barındırma) · **S10** (Avukatlık Kanunu / sorumluluk — hukukçu görüşü gerekir) ·
**S12** (KARAR-6 paralel slot, bozuk ölçütle toplandı).

---

## 2. Manşet sayı DEĞİŞTİ — ve bunun iki bedeli var

**Yeni varsayılan rejim: harness AÇIK · k=10 · S2 indeks · ÖNSÖZSÜZ**
*(`outputs/eval/s2-harness-k10-etiketli/` · DEV n=80 · hakem `gpt-4o-mini` · seed 3407)*

| eksen | önsözsüz **(yeni varsayılan)** | önsözlü *(eski manşet)* |
| :--- | ---: | ---: |
| sadık-cevap **kütlesi** | **%73,0** | %68,4 |
| coverage | 0,9000 | 0,8250 |
| A1 · cevaplanan | 0,8110 | 0,8288 |
| A1 · altın getirilen | 0,8593 | 0,8729 |
| aşırı-red | 5/80 | 9/80 *(gözle 8/80)* |
| **isabetsizlik** | **7/80** | 5/80 |
| `recall@10` | 0,875 | 0,875 |

**Bedel 1 — rakip kıyası GEÇERSİZ kaldı.** `g2-fl-harness/OZET.md`'nin eşit sınav kanıt tablosu
*"yeterlilik önsözü (h1): BİZ AÇIK · 3.1 FL aynı · 3.5 FL aynı ✅"* diyor. Yani rakipler
**önsözlü** ölçüldü. `%73,0 ↔ %69,5` kıyası ADR-0057 anlamında **eksen uyuşmazlığıdır** ve
*"3.5 FL'ı geçtik"* cümlesi o sütundan **KURULMAZ**. Eşleşmiş tek sayı hâlâ `%68,4 ↔ %69,5`
(**−1,1 p, geride**). ⇒ Faz 0'da rakipler önsözsüz rejimde yeniden ölçülür.
⚠️ Önsözü kaldırmak **onların** sayısını da yükseltebilir — ölçülmedi, varsayılmıyor.

**Bedel 2 — yeni manşetin gözle okuması YOK.** *"Gözle okuma bir kapıdır"* kuralı bu hatta
2026-09-06'da kendini kanıtladı: sayısal kapı (`0,1733 > 0,10`) bozuk ölçümü **geçirdi**, yakalayan
şey gözle okumaydı ve **önsözlü** çıpanın 14 aşırı-red kaleminin **6'sı yanlış pozitif** çıktı
(`outputs/eval/olcum-bi/B10_GOZLE_OKUMA_80.md`). O okuma **yalnız önsözlü rejimde** yapıldı.
⇒ Önsözsüz rejimin 80 kalemi de gözle okunmadan `%73,0` **yayımlanamaz.** Bedel **$0**, kapı.

---

## 3. `v1.0` kapısı — ön-kayıt (ADR-0064)

Formül **şimdi** yazılır, sayı ölçümden sonra **mekanik** türer. ARA KAPI'nın kalıbı budur:
ön-kayıtlanan şey formüldü, sayı değil ([ADR-0045](../../adr/0045-ara-kapi-merge-onarim-kontrolu.md)).

```
(1) kütle ≥ (3.5 Flash'ın kütlesi) − 2,0 p     ← ASIL KAPI · eşleşmiş rejim, aynı 80 soru
(2) isabetsizlik ≤ 7/80                         ← GERİLEMEZ · önsözsüz rejimin bugünkü değeri
(3) M5 (kör/parametrik) ≤ bugünkü               ← ANTİ-HEDEF · ezber kazancı kapıdan geçmez
(*) her sayım adımında GÖZLE OKUMA zorunlu      ← §2 Bedel 2
```

**δ = 2 p neden:** hakem gürültü tabanı (0,3 p) **yalnız A1 için** ölçüldü; kütle = coverage × A1
ve coverage'ın varyansı o tabanda **yok** — dolayısıyla gürültüye dayalı bir δ **kurulamaz**.
2 p, "yetişti" demeyi hak edecek kadar dar, tabanın altına düşmeyecek kadar geniş: insan kararı.

**Kapının bilinen sert sınırı:** `recall@10 = 0,875` → 10/80 soruda altın madde bağlama hiç
girmiyor → kütle tavanı **%87,5**. Aynı harness'ı kullandığı için 3.5 Flash da aynı tavana tabi
(sınav eşit kalır), ama bizim kazanma payımız da o tavanla sınırlı.

---

## 4. Faz 0 — ölçüm ön-koşulu (~$1,65 · zincir, sırası bağlayıcı)

**Neden erişim önce:** eşit sınavın kanıtı *"`recall@10` üç öznede de birebir 0,875"* — rakipler
**bizim indeksimizi** görüyor. İndeksi/erişimi sonradan değiştirmek o kanıtı bozar ve üç kolun
**yeniden ölçülmesini** gerektirir (~$1,35). Erişim onarımı GPU'suz ve **$0**, tavanı yükselten tek
kalem. Kapı formülü §3'te kilitli olduğu için sayıyı önce görmek eşiği oynatamaz.

| # | adım | bedel | `verify:` |
| :-- | :--- | :--- | :--- |
| **F0.1** | **Erişim onarımı** — `recall@10` 0,875 üstüne çıkarma denemesi (hibrit ağırlık, RRF, chunk sınırı; korpus 40.496 madde, indeks 80 MB, 759 ms/sorgu CPU). ⚠️ Süpürme **yalnız DEV'de** — donmuş TEST'e dokunulmaz | **$0** | `recall_olc.py` yeni `recall@10` basar; **yükselmezse indeks olduğu gibi kalır** ve F0.2 atlanır |
| **F0.2** | Erişim değiştiyse **bizim kolun yeniden üretimi + puanlanması** (önsözsüz, h1@k=10) | ~$0,15 | yeni `harness_tablo.json` + KUNYE |
| **F0.3** | ⭐ **Önsözsüz rejimin 80 kalemi GÖZLE OKUNUR** | **$0** | `GOZLE_OKUMA_80.md` + alet ↔ göz deltası raporlanır (önsözlü çıpada delta 9 ↔ 8'di) |
| **F0.4** | **Rakip çıpaları, önsözsüz, TEK KEZ**: 3.1 FL · 3.5 FL · **3.5 Flash (tam, ilk kez)** | ~$1,35 | eşit sınav kanıt tablosu: `recall@10` dört öznede **birebir aynı**; kesiklik (`finish_reason=length`) damgalanır — ⚠️ tuzak K2: muhakeme bütçesi rakipte uygulanmıyor |
| **F0.5** | **`SOURCE_CLIP` ödenir** (YB3) — `k`'nın çekinme ekseni TANIMSIZ'dan çıkar | ~$0,30 | ⚠️ tarihsel `verdict`'ler kıyaslanamaz hâle gelir → eski değerler **damgalanarak durur**, silinmez |
| **F0.6** | **`tgta_v1` VRAM ölçümü** (bugünkü 3,09 GiB **base GGUF** üzerinde ölçüldü) | $0 · ~15 dk | `vram_stack_tgta_v1.json` |
| **F0.7** | **Eşik ön-kaydı** — §3 formülünden sayı türetilir | $0 | ADR-0064 sayıyla kapanır, **eğitimden ÖNCE** |

Kayıt: `research_log` **#62** (sıradaki) · ADR'ler **0063 · 0064 · 0065 · 0066** *(⚠️ 0059 REZERVE, atlanır)*.

---

## 5. Hat A — paketleme (~$0) → `v0.2`

> 🚨 **A1 ÖLÇÜLDÜ 2026-09-07 — durum spec'in dediğinden KÖTÜ.** Bu bölüm *"istem yalnız
> `gen_eval_grounded.py` içinde"* diyor (YB6). Sayıldı: `"Sen HakHukuk'sun"` literali
> **5 dosyada** (`gen_eval_grounded.py` · `train_sft.py` · `raft_pack.py` · `build_orpo_v3.py` ·
> `gen_v3_rejected.py`). Kopyaların içerikleri karşılaştırıldı:
> - `SYSTEM_PROMPT_RAG` — **3 tanım, üçü de bayt-bayt aynı** (`bbfdd6613f`) ✅
> - `SYSTEM_PROMPT_RAG_MULTI` — tek tanım, `gen_eval_grounded` onu **import ediyor** ✅
> - 🚨 `SYSTEM_PROMPT` — **2 tanım, SÜRÜKLENMİŞ.** Son satırları farklı:
>   ölçüm `…ilgili kanun ve madde numarasını belirt.` ↔ eğitim
>   `Bu yanıt hukuki tavsiye değil, bilgilendirme amaçlıdır.`
>   Bu, **M5'in (kör mod) istemidir** — yani bugün koşulan anti-hedef ölçümünün istemi.
>
> ⇒ **A1'in kapsamı büyüyor:** iş *"istemi dosyaya çıkar"* değil, *"beş kopyayı tek kaynağa
> indir **ve sürüklenmiş olanın hangisinin doğru olduğuna karar ver**"*. İkincisi bir insan
> kararıdır, mekanik bir refactor değil. Bağlı açık soru: **S18**.

Ürünün altı asıl açığından ikisi burada: servis katmanı **kod olarak yok**
(`grep -rl "fastapi|uvicorn|flask|gradio" scripts/` → 0 sonuç) ve modeli indiren kişi yayımlanan
sayıyı **üretemiyor** (YB6: istem yalnız `gen_eval_grounded.py` içinde).

| # | adım | `verify:` |
| :-- | :--- | :--- |
| **A1** | **YB6** — istem artefaktı: varsayılan (önsözsüz) istem versiyonlu bir dosyaya çıkar, `gen_eval_grounded.py` **onu okur** (tek kaynak, kopya yok) | eval koşusu istemi dosyadan okuyarak **birebir aynı** kütleyi üretir |
| **A2** | **Servis katmanı — CLI.** Tek derin arayüz: `answer(soru) → {cevap, atıflar, kaynaklar}`. İçinde retriever + llama.cpp + istem gizli; harness **GPU'ya girmez** (embedder CPU, indeks CPU RAM/disk) | temiz makinede kurulum → 3 soru → atıflı cevap; `atif_dogrula.py` atıfları doğrular |
| **A3** | **İndeks dağıtımı** — `AÇIK KARAR S8`: HF dataset (80 MB) ↔ kurulumda üret (~10 dk) | karar verilince tek komutla indeks hazır |
| **A4** | **Yeniden üretim yolu** — yayımlanan sayıyı kullanıcının makinesinde üreten tek komut | ölçülen kütle = yayımlanan kütle |
| **A5** | `MODEL_CARD.md` + `README*.md`: yeni manşet, iki sürüm şeması, kırık linkler | `grep` ile silinen dosya adına link kalmadığı gösterilir |
| **A6** | **Sorumluluk ibaresi** — *"hukuki tavsiye değil"* ürün yüzeyine. `AÇIK KARAR S10` (hukukçu görüşü) ibarenin girmesini **engellemez** | CLI çıktısı ve README ibareyi taşır |
| **A7** 🆕 | **Basit TUI** — hazır bir kütüphaneyle (aday: `textual`; `prompt_toolkit` alternatif) tek ekranlı arayüz: soru kutusu · cevap · atıflar · kaynak listesi. ⛔ Web arayüzü, API sunucusu, hesap/oturum **DEĞİL** — onlar v2. Kullanıcı kararı 2026-09-06: *"v1'de belki hazır bir TUI kütüphanesi ile basit bir arayüz olsun"* | terminalde çalışır; `answer()` derin arayüzünün üstüne oturur, kendi mantığı yoktur |
| **A8** 🆕 | **Ölçüm aletlerini ürün yüzeyine taşı — `suskunluk_terazisi`.** Bugün ölçüm aleti olan üç şey üründe **güven mekanizması** olur: (1) **dürüst suskunluk** — model çekindiğinde vatandaşa açıkça söylenir (`exact_reject` zaten var) · (2) **çekinceli cevap rozeti** — 2026-09-06'da keşfedilen üçüncü sınıf (*"doğrudan madde yok, bununla birlikte…"*) vatandaş için en tehlikelisi: cevap gibi görünüyor ama tam değil · (3) **atıf doğrulama** (`atif_dogrula.py`) — uydurulmuş madde numarası kullanıcıya **gitmeden** yakalanır (bizde 0/114 ↔ rakiplerde 1·4·4). Kullanıcı kararı 2026-09-06. ⛔ Sıfır yeni araştırma, mevcut kodun yeniden kullanımı | CLI/TUI çıktısında üç durum ayırt edilebiliyor: **cevap · çekinceli cevap · suskunluk**; uydurulmuş atıf kullanıcıya ulaşmıyor |

### A2'nin üretim ayarları — 2026-09-07'de ölçümden doğdu (insan sorusu)

Ölçüm rejiminin üç sayısı **ürüne taşınmaz**; üçü de rakip eşitlemesi ya da tanı içindir:

| ayar | ölçümde | **üründe** | gerekçe (ölçülmüş) |
| :--- | :--- | :--- | :--- |
| toplam bütçe | **1536** (ADR-0070) | cömert; tavan = **bağlam penceresi** | 1536 rakiple eşitlemek içindi; üründe rakip yok. VRAM: ctx 32.768 yalnız **3,70 GiB** (4.096'da 3,09) ⇒ ~12 GB kartta rahat |
| düşünce ↔ cevap | **paylaşımlı tek havuz** | 🆕 **AYRI bütçeler** | ölçüldü (id 27, M5): düşünce 1536'nın tamamını yaktı, cevaba **3 karakter** kaldı (`"Kat"`). Paylaşım ADR-0070'in *eşitleme* aracıydı; üründe düşüncenin cevabı **aç bırakması** için hiçbir sebep yok. Bedeli **$0** |
| tekrar cezası | **yok** (temiz çıpa) | 🆕 **DRY açık** | kör modda yozlaşmış döngü ölçüldü (3/80). ⛔ `repeat_penalty` **değil**: hukuk metninde madde numarası ve terim **meşru olarak** tekrarlar; DRY tekrarlayan **dizileri** cezalandırır. ⭐ İkisi de `temperature=0`'da çalışır ⇒ **determinizm korunur** |
| kesilme | sayılır, kapı olur | 🆕 kullanıcıya **söylenir** | yarım cümleyi sessizce teslim etmek `suskunluk_terazisi`'nin (A8) ruhuna aykırı: üç durum **cevap · çekinceli cevap · suskunluk** idi; **kesik cevap** dördüncüsü ve ayırt edilmeli |

⚠️ Bunlar **ürün** kararlarıdır ve **ölçüm rejimini değiştirmez**; ölçüm rejimini değiştirmek
bugüne kadarki bütün sayıları yeniden koşturur (ADR-0057 eşit sınav).

## 6. Hat B — model (kütle) → `v1.0`

> 🚨 **BAYAT SAYI — B-2'deki *"7/80"* geçersiz (damgalandı 2026-09-07).** O sayı **v1 soru
> setinden** geliyordu ve **hiç gözle sayılmamıştı**. v2 biriminde ilk kez tam gözle sayıldı:
> **8/80** (75 cevaplanan kalemin tamamı tarandı; iki otomatik süzgeç de tek başına yetmiyor).
> İnsan kararı: çıpa **8/80**'e yeniden çivilendi, kural *"gerileme yok"*
> ([ADR-0064](../../adr/0064-v1-kapisi-uc-maddeli-on-kayit.md) madde 2 ·
> [ADR-0066](../../adr/0066-b1-yontemi-reddetme-orneklemesi.md)).
> ⛔ Eşik **gevşetilmedi**, birimi düzeltildi — `7/80` ile `8/80` **aynı birimde değildir**.

| # | adım | bedel | `verify:` |
| :-- | :--- | :--- | :--- |
| **B-1** | Faz 0 (§4) | ~$1,65 | eşik ön-kayıtlı |
| **B-2** | **B1 · isabetsizlik** (7/80 önsözsüz) — **reddetme-örneklemesi**: n cevap üret → **yalnız atıfı altına doğrulananları** tut → elimizdeki TRL `SFTTrainer` ile eğit. Alet **hazır ve L4'te doğrulanmış** (`harvest_b10`, ADR-0047 m.2 taşıyıcısı; sızıntı süzgeci 13.350 → 12.914) — **yeniden kurulmayacak** | ~$5 | isabetsizlik ↓ **ve** kütle ↑, gözle okumayla; kapı maddesi (2) gerilemedi |
| **B-3** | **B4 · `τ_a` genliği** — merge'de 0,987 → 0,766 (−22,1 p) seyreliyor; teşhis **genlik** (70 adım @1e-5 → ‖τ_a‖ 1,1806 ↔ ‖τ_g‖ 10,4722, oran 8,87×). Kaldıraç: **aynı ORPO ile daha çok adım / daha yüksek lr**. ⛔ Yöntemi de değiştirmek iki değişkeni birlikte oynatır (ADR-0017) | ~$1,3 | ‖τ_a‖ ölçülür; merge sonrası M2b yükselir |
| **B-4** | **YB2 · M2b eğitim borcu** — kapı yolu ölçülerek öldü (`h2b@k=4` 0,735 < 0,766) | tur içinde | M2b ≥ yeni çıpa |
| **B-5** | **Kapı koşusu** (§3, üç madde + gözle okuma) | ~$1 | geçerse **`v1.0`**; geçmezse sayı **damgalanarak** yayımlanır ve `v0.x` devam |

**⛔ GRPO / RLVR ertelendi (ADR-0066).** Verifier'lar zaten deterministik ve programatik
(`atif_dogrula.py` · `groundedness.py` · `score_abstention.py`) — yani B1 **doğrulanabilir ödül**
problemine birebir uyuyor ve SFT bunu ancak taklit ederken RLVR doğrudan cezalandırır. **Ama**
8-16 rollout/istem × (1024+512) bütçe → **$10-30 tahmin** (Modal'da **$29,19**), ve tahmin
**ölçülmedi**. Karar: **önce ucuz olan**; reddetme-örneklemesi kapı maddesini geçirmezse GRPO
kendi ADR'si ve kendi bütçe kapısıyla açılır.

## 7. Hat C — metodoloji paper'ı (yan ürün)

Savunulacak iddia **ölçüm kaydında zaten duruyor**, yeni koşu gerektirmiyor: cevaba bağlı payda
(K3: payda modele bağımlıydı, üç kol 45/56/50 → **68**) · hakem yığını kayması · yeniden-koşum
gürültü tabanı (0,3 p, **yalnız A1 için**) · eşit sınav kapısı (ADR-0057) · **ve bir çekinme
dedektörünün istem rejimine bağımlı çıkması** — *"en büyük kusur"* sandığımızın **%43'ü ölçüm
aletiydi** (14/80 → 8/80). `v1.0` sonrası.

---

## 8. Yazılacak belgeler ve kabul ölçütleri

| belge | taşıdığı | `verify:` |
| :--- | :--- | :--- |
| **`PRODUCT.md`** | vatandaş kim · hangi soruyu soruyor · cevap neye benziyor · **vaat ETMEDİĞİ** (hukuki tavsiye değil · güncellik indeksin işi · %100 doğruluk değil) · v1↔v2 sınırı · üç maddeli kapı · iki sürüm şeması | her nicelik yanında **kaynak dosya adı** taşır; "vaat etmiyor" bölümü var |
| **`ROADMAP.md`** | Faz 0 → Hat A ∥ Hat B → kapı → `v1.0` → v2. Her adım: *ne · neden (hangi ölçülmüş boşluk) · `verify:` · bedel · bağımlılık* | kritik yol işaretli; **AÇIK KARAR** damgaları S5·S7·S8·S9·S10·S12 |
| **`TODO.md`** | yalnız **bugün koşulabilir** kalemler (F0.1-F0.3, A1) | her satır bir ROADMAP adımına bağlı |
| **`docs/MIMARI.md`** | v1 zinciri: base → kollar → merge → GGUF → retriever → istem → CLI · v2 app katmanı sınırı · `referans-design-doc.md`'nin işlevini devralır | her kutu bir **var olan** dosyaya ya da bir ROADMAP adımına işaret eder |

**Son adım (belgeler var olduktan SONRA):** `CLAUDE.md` · `MODEL_CARD.md` · `README.md` ·
`README.tr.md` + kalan dört belgenin kırık linkleri onarılır.
`verify:` → `grep -rE '(ROADMAP|TODO|TASARIM|VISION|PAPER_TARGET)\.md|_arsiv/'` yalnız **yeni**
dosyalara işaret eden isabetler döner.

## 9. Kaderi belirsiz belgeler — tek tek karar

| belge | **KARAR** | gerekçe |
| :--- | :--- | :--- |
| `docs/FINE_TUNING.md` | **KALSIN**, işaretçi onarılsın | yerel donanım + Unsloth/bitsandbytes yığınının tek düzyazı kaynağı; bayat damgası üstünde |
| `docs/VERI_PLANI.md` | **KALSIN**, işaretçi onarılsın | EDA sert kuralının ve lisans temizliğinin **gerekçesi** yalnız burada |
| `docs/YARGI_KAYNAKLARI.md` | **KALSIN**, işaretçi onarılsın | sökülmüş API sözleşmeleri; v2 içtihat katmanı buradan başlar |
| `docs/open_questions.md` ⚰️ | **KALSIN + kendi kuralı uygulansın** | otoritesi `PRODUCT.md`'ye taşınır; kapanan **S1/S2/S11/S14** ADR'lere işlenip **kapanış dizinine** geçer (iz kalır, gövdeden çıkar); S5-S13 canlı kalır |
| `docs/model-soyagaci.mmd` | **KALSIN**, işaretçi onarılsın | kolların bağımsızlığını ve merge'in zincir **olmadığını** tek bakışta anlatıyor |
| `referans-design-doc.md` | 🗑️ **SİLİNİR** → yerine `docs/MIMARI.md` | insan kararı: *"güncel hedefe göre yenisi yazılsın"* |

## 9b. Aletin adı — `suskunluk_terazisi` (kullanıcı kararı 2026-09-06)

Red dedektörü **tek başına alet değildir**; iki parçadır ve ikincisi olmadan birincisi yanıltır:
1. **`exact_reject`** — deterministik, rejim-duyarlı red tespiti (ADR-0061)
2. **Kalibrasyon protokolü** — her özne ailesinde işaretlenen kalemlerin **gözle okunması**, sonra
   **ALET / GÖZ-orta / GÖZ-katı** üçlü raporlama

**Ad: `suskunluk_terazisi`.** Gerekçe: 2026-09-06'nın asıl bulgusu *"alet tek başına hüküm vermez,
iki kefe gerekir"* oldu — dedektör önce **bizim** şablonumuzda 14'ü 8 gösterdi (ADR-0061), sonra
**Gemini** şablonunda 11'i 7 gösterdi (F0.4 kalibrasyonu). İki kez, iki farklı yönde.

## 10. Yan bulgular — bu oturumda ölçüldü, düzeltilmedi

- **TRL zaten kullanılıyor.** `scripts/egitim/train_sft.py:28` → `from trl import SFTTrainer, SFTConfig`
  (`τ_g`) · `scripts/egitim/train_orpo.py:27` → `from trl import ORPOTrainer, ORPOConfig` + `MaskedORPOTrainer`
  (`τ_a`) · `trl==0.24.0` pinli. Unsloth TRL'nin **alternatifi değil, altındaki yama katmanı**:
  `PatchDPOTrainer()` TRL trainer'larını Unsloth çekirdeklerine uyarlıyor.
  **REJECTED — `Axolotl`/`LLaMA-Factory`:** TRL+PEFT üstüne YAML sarmalayıcı; yeni yetenek sıfır,
  bedeli doğrulanmış hattın (Modal taşıyıcıları, seed'ler, `--fresh-adapter` semantiği) yeniden
  doğrulanması. **REJECTED — `verl`/`OpenRLHF`:** tek L4 + 4B için fazla büyük.
  **REJECTED — `mergekit`:** `merge_ties.py` doğrulanmış (224/224 tensör, host-RAM akışı) ve
  semantiği ADR-0052'yle çivili; ölçülmüş bir soruyu yeniden açar.
- **`train_orpo.py` docstring'i BAYAT** — *"base = v2b ADAPTER'dan DEVAM"* diyor, bu bugünkü
  ham-base kuralına aykırı bir kalıp. Kural **ihlal edilmedi**: `kollar.md`:64 `τ_a v1`'in
  **`--fresh-adapter`** ile koştuğunu gösteriyor. Yalnız docstring yanıltıcı → TODO.

---

## 11. Temizlik turu — bayat/çöp envanteri (insan kararlı, 2026-09-06)

> ⛔ **İLK KURAL: KAYIT TEMİZLENMEZ.** `docs/record/**` · `docs/adr/**` ·
> `outputs/eval/**` sayıları ve `KUNYE.json`'ları · `.ONCEKI-*` / `.YARIM-*` izleri
> **dokunulmaz.** Bunlar yayımlanmış her sayının kaynağıdır ve *"çelişki iki yerde
> işaretlenir, sessizce üzerine yazılmaz"* kuralının fiziksel hâlidir.

**Ölçülen envanter** (2026-09-06, `du`/`git check-ignore`/`find` ile):

| sınıf | ölçüm | **KARAR** |
| :--- | ---: | :--- |
| `models/merged/` 4 × 8,8 GB | 35 GB | **T1** — yalnız `tg_ta_modulmin` + `tg_ta_globalmin` silinir |
| `models/gguf/` 12 dosya | 40 GB | **T1** — yalnız `cp2s-ties-smoke-q4_k_m.gguf` silinir |
| `.ONCEKI-*` / `.YARIM-*` | 173 dosya · 2,8 MB | 🔒 **KALIR** — denetim izi, insan kararı |
| emekli tur script'i | 16 dosya | **T2** — `scripts/_arsiv/`e **taşınır** (silinmez) |
| `.pytest_cache` | 40 KB | **T3** — ne ignore ne tracked → `.gitignore` |
| bayat içerik | — | **T4** — damgalanır (silinmez) |

### T1 · `models/` — ~20 GB (git'te değil, yeniden üretilebilir)

> 🚨 **AD ÇAKIŞMASI — 2026-09-07'de yakalandı, okumadan önce bunu oku.** Bu belgedeki **T1**
> `models/` temizliğidir. 2026-09-07'nin devir notu ve `/goal` metni ise *"T1"* diyerek
> **hakem panelini** kastediyordu (3 aile + aile dışlaması + κ). *"Sıralama: T1 → Hat A →
> Hat B"* cümlesi bu belgeye bakılarak okunursa, hakem paneli kurulacağı yerde **20 GB model
> silinir** — üstelik adaptörler **yedeksizken** (aşağıdaki ⚠️).
> ⇒ **Hakem panelinin etiketi `HP` oldu.** Bu belgedeki `T1`-`T4` temizlik serisidir ve
> anlamı **değişmedi**. Kilitli sıralamanın doğru okunuşu: **`HP` → Hat A (paralel) → Hat B**.
> ⚠️ Ayrıca: **hakem paneli bu spec'te HİÇ geçmiyor** — ADR-0064'ün *"Ne KURULMAZ"* madde 2
> borcundan (tek aile, κ yok, öz-tercih ölçülmedi) doğdu ve sıradaki planın işidir.

Silinecek: `models/merged/tg_ta_modulmin/` · `models/merged/tg_ta_globalmin/`
(**ADR-0053: modül başına norm kapsamı REDDEDİLDİ** — reddedilmiş varyantlar) ·
`models/gguf/cp2s-ties-smoke-q4_k_m.gguf` (smoke testi artefaktı).

**Neden güvenli — bugün doğrulandı:** asıl artefakt **adaptördür** ve ikisi de yerinde:
`outputs/tg_v1` (115 MB) · `outputs/ta_v1` (326 MB). Yeniden üretim komutu
`kollar.md`:24-26'da yazılı (`merge_lora.py` / `merge_ties.py` + llama.cpp Q4_K_M).

⚠️ **Ama adaptörler YEDEKSİZ** (`kollar.md`: *"yedeklenmiyor — bilinçli"*; 12B hattında
adaptörler **kalıcı kaybedildi**). Türevleri silmek tek disk arızasının yıkım yarıçapını
büyütür. ⇒ **`AÇIK KARAR S7` (adaptörler HF'ye yüklensin mi) bu temizliğin gerçek ön
koşuludur** ve ROADMAP'te T1'in **önüne** yazılır. Kalan `tgta_v1` (yayımlanacak taşıyıcı) ·
`tg_v1` (aktif kol) · base `q4_k_m` (kıyas çıpası) **korunur**.

`verify:` `du -sh models/` öncesi **75 GB** → sonrası **≈55 GB**; `kollar.md`'nin
"diskte tutulan" satırı gerçeği yansıtır hâle gelir.

### T2 · Emekli tur script'leri → `scripts/_arsiv/`

`cp05_conv1d_ceiling.py` · `cp09_gemini_gen.sh` · `cp09_tablo.py` · `cp0_thinking_gen.sh` ·
`cp0_thinking_score.sh` · `cp1_delta.py` · `cp1_rescore_meta.sh` · `cp1_spotcheck.py` ·
`cp2_audit.py` · `cp2_harvest.py` · `cp2_pilot.sh` · `cp2_prefilter.py` · `cp2c_birlestir.py` ·
`cp2c_kabul.sh` · `cp2r_esikler.py` · `watch_cp09.sh` (16 dosya).

⚠️ **Silinmiyor, taşınıyor** — `cp2_prefilter.py` / `cp2_harvest.py` B1 turunun
reddetme-örneklemesinde işe yarayabilir; görünmez kılmak istemiyoruz.

🚨 **DÜZELTME 2026-09-06 — toplu taşıma YAPILAMAZ, ölçüldü.** 16'nın **7'si canlı kodla bağlı**
ve `cp0_` öneki emekliliği değil *checkpoint-0 dönemi adlandırmasını* gösteriyor:

```
cp0_thinking_gen.sh    ← modal_train.py · cp3_merge_dene.sh · cp0_thinking_score.sh   🔴 CANLI KOŞUCU
cp0_thinking_score.sh  ← cp0_thinking_gen.sh · cp09_gemini_gen.sh · watch_cp09.sh     🔴 CANLI PUANLAYICI
cp2_harvest.py         ← modal_train.py · cp2c_kabul.sh · cp2_pilot.sh                🔴
cp2c_kabul.sh          ← score_abstention.py · valid_trap_cache.py · cp2c_birlestir.py 🔴
cp09_tablo.py ← cp1_delta.py   ·   cp1_delta.py ← cp1_rescore_meta.sh   ·   cp2_audit.py ← cp2c_kabul.sh
```

`cp0_thinking_gen.sh` **harness koşularının canlı koşucusudur** — llama-server'ı açar, künyeyi
basar, kesiklik kapısını uygular; `outputs/eval/*/kosu.log`'un künye başlığını o yazıyor.
⇒ **T2 iki kez daraltıldı:** liste **izole 9 dosyaya** indi *ve* **Faz 0'dan sonraya** alındı.
Gerekçe: ölçümün aletini ölçümden hemen önce oynatmak `yurutme-tuzaklari.md`'nin ana sınıfıdır
(*"sessiz yanlışlık, çökme değil"*).

`verify:` taşımadan önce `grep -rnE "cp0[59]?_|cp1_|cp2[cr]?_|watch_cp09"` ile çağıran/import
eden aranır (bulunursa yol güncellenir) · taşımadan sonra `pytest` **112 passed, 2 xfailed**.

### T3 · `.gitignore` · `.pytest_cache/` eklenir. `verify:` `git check-ignore -q .pytest_cache`

### T4 · Bayat içerik — damgalanır, silinmez

| yer | bayat olan | eylem |
| :--- | :--- | :--- |
| `scripts/egitim/train_orpo.py` docstring | *"base = v2b ADAPTER'dan DEVAM"* — bugünkü **ham-base** kuralına aykırı kalıp | docstring gerçeğe çekilir: `τ_a v1` **`--fresh-adapter`** ile koştu (`kollar.md`:64), kural ihlal edilmedi |
| `docs/FINE_TUNING.md` · `VERI_PLANI.md` · `YARGI_KAYNAKLARI.md` · `model-soyagaci.mmd` | silinen dosyalara **kırık işaretçiler** (toplam 9) | yeni belgelere bağlanır (§8 son adım) |
| `docs/open_questions.md` ⚰️ | otoritesi silinen `TASARIM.md` (20 atıf) · kapanan **S1/S2/S11/S14** gövdede duruyor | otorite `PRODUCT.md`'ye çekilir; kapanan dördü ADR-0063/0064/0065'e işlenip **kapanış dizinine** taşınır |
| `CLAUDE.md` · `MODEL_CARD.md` · `README*.md` | manşet `%68,4` + kırık işaretçiler | Faz 0 sayısı geldikten sonra güncellenir |

**Temizliğin bütün turu için `verify:`**
`grep -rE '(ROADMAP|TODO|TASARIM|VISION|PAPER_TARGET)\.md|docs/_arsiv/|docs/superpowers/specs/2026-09-06-v1-v2'`
→ yalnız **var olan** dosyalara işaret eden isabetler döner.
