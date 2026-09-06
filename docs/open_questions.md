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

## 🆕 v1/v2 SÜRÜM KARARLARI — **S1…S14** *(eklendi 2026-09-06)*

> **Nereden geliyor:** [`docs/superpowers/specs/2026-09-06-v1-v2-roadmap-taslak.md`](superpowers/specs/2026-09-06-v1-v2-roadmap-taslak.md) §7.2.
> Çerçeve: tez değil **ürün** — **v1 = çalışan model release'i · v2 = API · arxiv yan ürün**.
> **Hepsi insan kararıdır.** Eşik/ölçüt koymak ADR-0050 gereği insanın işidir ve koşudan
> **önce** ön-kayıtlanır.
>
> ⚠️ **Bu tablo aşağıdaki OQ girdilerini YİNELEMEZ.** Zaten burada duran sorular karar
> numarasıyla **damgalandı**: **S4** = `SOURCE_CLIP` (YB3) · **S5** = OQ-2 ikili oran
> çözünürlüğü · **S6** = OQ-3 önsözün atıf bedeli. OQ-1 (M3 paydası) · OQ-4 · OQ-5 · OQ-6
> ilgili başlıklarında duruyor ve karar sorusu değil, **iş kalemi**dir.

| # | soru | seçenekler | bağlı olduğu |
| :-- | :--- | :--- | :--- |
| **S1** | **ARA KAPI düşmüşken `v1.0` adı verilebilir mi?** | (a) `v1.0` = *ürün* olgunluğu, ARA KAPI bir *iddia* kapısıydı → yeni ölçütle açılır · (b) CP4-CP5 koşulana dek `v0.x` ⚠️ ~$19 ve **yetkisi yok** · (c) sürümü ikiye ayır (ürün sürümü ↔ iddia sürümü) | [ADR-0045](adr/0045-ara-kapi-merge-onarim-kontrolu.md) · [#58](record/research_log/2026-08-06-payda-tekillesmesi.md) |
| **S2** | **v1 harness'lı mı çıkar?** | (a) **evet, CLI ile** *(taslağın önerisi)* · (b) model-only → ⚠️ o zaman **yayımlanan sayı (%62,8) yeniden üretilemez**, ablasyon (%61,3) alınır | ADR-0058 · borç **D-d/YB6** |
| **S3** | **B10 hedefi ne olsun?** | (a) ≤11/80 *(taslağın önerisi; turun kendi ön-kayıtlı tahmini 8-11/80)* · (b) ≤8/80 (3.1 FL ile eşitlen) · (c) yalnız *"gerileme yok"* | plan ön-kayıtları · `g2-fl-harness/OZET.md` |
| **S4** | **`SOURCE_CLIP` ödensin mi?** (≈$0,30) | (a) öde → `k`'nın çekinme ekseni **tanımlı** olur, ⚠️ tarihsel `verdict`ler kıyaslanamaz hâle gelir · (b) ödeme → **TANIMSIZ** damgasıyla taşı | ⬇️ aynı adlı OQ · KARAR-4 · ADR-0057 |
| **S5** | **İkili oran çözünürlük sınırı** | (a) `k` kalem kuralı · (b) ölçülmüş taban (hakem maliyeti var) · (c) Wilson aralığı ($0, kapı kuralını değiştirir) | ⬇️ **OQ-2** |
| **S6** | **Önsözün atıf bedeli kabul mü?** | takas ölçüldü: atıf **−%30**, atıfsız cevap 8 → 13 ↔ kütle **+1,4 p**, A1 **+1,9 p** | ⬇️ **OQ-3** |
| **S7** | **LoRA adaptörleri HF'ye yüklensin mi?** | `kollar.md`'nin *"adaptörler yedeklenmiyor — bilinçli"* kararını **değiştirir** → **ADR gerekir**. ⚠️ 12B hattında adaptörler **kalıcı kaybedildi**; HF yayını ilk gerçek yedek olur | [`record/kollar.md`](record/kollar.md) · [ADR-0034](adr/0034-emekli-hat-artefaktlarinin-repodan-cikarilmasi.md) |
| **S8** | **İndeks nasıl dağıtılır?** (80 MB) | (a) HF dataset · (b) kurulumda üret (~10 dk) | v1 §C5 |
| **S9** | **v2 nasıl barındırılır?** | (a) yalnız self-host · (b) + hız-sınırlı vitrin (~$100-300/ay) · (c) hosted-first ⚠️ **mahremiyet vaadini zayıflatır** ⚠️ **TR IP** kısıtı bulut barındırmayı da kısıtlayabilir | taslak §4.1 · [`BEDESTEN_API.md`](BEDESTEN_API.md) |
| **S10** | **Avukatlık Kanunu / hukuki sorumluluk sınırı** | **hukukçu görüşü gerekir** — repo'da hiç değerlendirilmemiş | taslak §4.6 |
| **S11** | **arxiv yazılsın mı?** | (a) hayır · (b) yalnız **P2/P3** → *metodoloji paper'ı* (taslağın okumasıyla **en güçlü hikâye**) · (c) tam iddia katmanı (P1, ⚠️ ARA KAPI düştüğü için **yetkisiz**) | [`PAPER_TARGET.md`](PAPER_TARGET.md) · taslak §6 |
| **S12** | **KARAR-6 — paralel slot (`-np`)** | sayılar geldi (Jaccard **0,5278** · birebir **3/19**) ⚠️ **bozuk ölçütle toplandı** → ölçüt onarılınca **yeniden koşulur**, hükmü **insan** kurar | [#60](record/research_log/2026-09-06-hasat-kabul-olcutu-coktu.md) |
| **S13** 🆕 | **Hasat kabul ölçütü nasıl onarılır?** ⬇️ ayrıntı aşağıda | ✅ **KAPANDI 2026-09-06 → (c) uygulandı.** Alet TDD ile onarıldı (`112 passed, 2 xfailed`) · **82** dosya $0'a yeniden puanlandı · çıpanın **80 kalemi gözle okundu** · pilot **yeniden koşulmadı, gerek kalmadı** (yeni kabul kümesi eskisinin **alt kümesi** olduğu için kaydedilmiş kabuller yeniden süzüldü, ~$0,81 tasarruf) | [#60](record/research_log/2026-09-06-hasat-kabul-olcutu-coktu.md) · [#61](record/research_log/2026-09-06-dedektor-onarimi-b10-yeniden.md) · [ADR-0061](adr/0061-cekinme-dedektoru-istem-rejimi-bagimliligi.md) |
| **S14** 🆕🚨 | **ADR-0058'in gerekçesi TERSİNE DÖNDÜ — ana protokol önsözlü kalsın mı?** Önsöz *kütleyi yükselttiği için* benimsenmişti; onarılmış aletle **düşürüyor**: önsözlü **%68,4** ↔ önsözsüz **%73,0** (**−4,6 p**). Kıyas eşleşmiş ve **doğrudan ham dosyalardan** doğrulandı: aynı 80 id · **80/80 birebir aynı `context_shown`** · aynı `recall@10` → değişen **yalnız istem**. ⚠️ Ama önsözün diğer ayakları **ayakta**: A1 **0,8288 ↔ 0,8110** (+1,8 p) · A1·altın **0,8729 ↔ 0,8593** (+1,4 p) · isabetsizlik **5/80 ↔ 7/80**. Takas iki yönlü: önsöz modeli **daha seçici ama daha suskun** yapıyor (coverage 0,8250 ↔ 0,9000 · B10 9/80 ↔ 5/80). ⚠️ −4,6 p'yi koruyan **çözünürlük sınırı YOK** (0,3 tabanı A1 makrosu içindir; kütle = cov × A1 ve coverage'ın varyansı o tabanda yok) | 🔴 **AÇIK — insan kararı.** Protokol **değiştirilmedi**, resmî sayı hâlâ **önsözlü %68,4**. Değiştirmek **yeni bir ADR** ister. Seçenekler: (a) önsözü koru — A1/B1 lehine, kütleyi feda et · (b) önsözü kaldır — kütle lehine, A1/B1'i feda et · (c) çözünürlük sınırı önce kararlaştırılsın (**S5** ile birlikte), sonra bakılsın | [#61](record/research_log/2026-09-06-dedektor-onarimi-b10-yeniden.md) §ADR-0058 · [ADR-0058](adr/0058-b-i-kaynak-yeterliligi-onsozu-benimsendi.md) |
| **S15** 🆕 | **DEV ↔ TEST erişim farkı standardize edilerek mi raporlansın?** Ölçüldü 2026-09-06: `recall@10` DEV **0,8875** ↔ TEST **0,7500** (temiz kıyas v1/k=60: 0,8750 ↔ 0,7250, p=0,0415, Wilson aralıkları örtüşüyor). Fark setin zorluğundan değil **bileşimden**: ayrım kanuna göre katmanlı ama **madde uzunluğuna göre değil** — en zor uzunluk diliminde (Q4, `recall@10` 0,6667) DEV'in payı %12, TEST'in **%50**. Bileşim farkın **%81'ini** açıklıyor. ⇒ **v1 kabul testinin kütle tavanı ≈%75, DEV'in %95'i değil.** | (a) kabul testi sonucu **ham + uzunluk-standardize** iki sütun raporlansın · (b) yalnız ham, tavan farkı şerhle damgalansın · (c) ayrım yeniden katmanlansın ⚠️ **donmuş TEST açılır** | [ANALIZ](../outputs/eval/f01c-dev-test-farki/ANALIZ.md) · [ADR-0068](adr/0068-rrf-k-60-to-10.md) |

### **[S13]** 🚨 Hasat kabul ölçütü çöktü — onarılacak mı, hasat rejimi mi değişecek? 🔴 *ölçüldü 2026-09-06, karar yok*

`b10_hasat.py` hasadı **yeterlilik önsözü OLMADAN** koşuyor (`sufficiency_preamble: false`).
O rejimde açılış yeterlilik hükmü oluşmuyor (**26/26 kalemde `None`**), ve
`exact_reject` (`scripts/score_abstention.py:208`) o dalda **cevabın TAMAMINI** `REJECT_RE` ile
tarıyor. Havuzun cevap şablonunda tetikleyen ibare cevabın hükmü değil, **elenen kaynakların
gerekçesi** (*"…İÇERMEMEKTEDİR"*); gerçek hüküm 3. maddede duruyor.

```
gözle okunan 10 kabul  →  6'sı tam, atıflı CEVAP · 4'ü gerçek çekinme
raporlanan kabul_orani    0,1733 (26/150)   → kapı geçmiş GÖRÜNÜYORDU
gözle okumaya göre        ~0,07             → eşik 0,10'un ALTINDA
```

⚠️ Doğru okuyan yol (`_son_esasli_ibare`, [#57](record/research_log/2026-08-06-cekinme-aleti-onarimi.md)/Ö2
ile eklendi) **yalnız açılış hükmü `True` iken** çalışıyor — önsözsüz rejim kapsam dışı kaldı.
Bu, #57'nin dersinin tekrarı: *alet düzeltmesi aletin **kendisinde** yapılır, bir dalında değil.*

**Seçenekler ve takasları:**
- **(a) `exact_reject`'in önsözsüz dalı düzeltilir** — ⚠️ aynı fonksiyon **çıpaları da** okuyor,
  dolayısıyla **yayımlanmış sayıları etkileyebilir** → **ADR gerekir** (sıradaki **0061**;
  ⚠️ **0059 REZERVE**).
- **(b) Hasat önsözlü koşar** — alet değişmez, ADR-0058 ana protokolüne yaklaşır; ama hasat
  `τ_a` v1'in eğitildiği rejimden **uzaklaşır**.
- **(c) İkisi de + çıpaların 80 kalemi gözle okunur** — en pahalısı, tek kesin olanı.

> ## ✅ KARARA BAĞLANDI — **(c)**, insan kararı, 2026-09-06
>
> 1. **`exact_reject` onarılır** — TDD ile (önce düşen test), aletin **kendisinde**, bir dalında
>    değil (#57'nin dersi). Alet değiştiği için **ADR gerekir**: sıradaki **0061**
>    (⚠️ **0059 REZERVE**).
> 2. **73 detay dosyası yeniden puanlanır** — hakem çağrısı yok, maliyet **$0**.
> 3. **Çıpanın 80 kalemi gözle okunur** — bulaşmanın büyüklüğünü *ölçen* tek yol; sonda her iki
>    yönde de hatalı olduğu için programatik kestirme **kabul edilmiyor**.
> 4. **Pilot yeniden koşulur** — bugünkü kabul kümeleri bozuk ölçütle seçildi; KARAR-6 kıyası
>    (**S12**) da bu koşudan yeniden gelir.
>
> 🔒 **Eşik kuralı — karar YENİ SAYILAR GÖRÜLMEDEN verildi (seçim yanlılığı yok).** Onarım
> çıpaları oynatırsa, turun **Görev 7 (kol kapısı)** ve **Görev 9 (ürün kapısı)** eşikleri
> **AYNI FORMÜLLE yeniden çıpalanır** — eşiğin *sayısı* yeni çıpadan türer, *kuralı* değişmez.
> Bu, ADR-0050'nin hükmünün aynısıdır: **alet düzeltilir, eşik insan tarafından ve önceden
> konur**; sonucu gördükten sonra eşik oynatılmaz.

🔴 **Ayrı ve kapanmamış:** çıpa bulaşmasının **büyüklüğü ÖLÇÜLMEDİ.** Kesin olan iki şey:
(1) resmî çıpada **en az bir doğrulanmış yanlış pozitif** var (`id=19`); (2) önsözlü resmî
koşuda bile açılış hükmü çoğunlukla oluşmuyor (**75 `None` · 5 `True`** — cevapların %94'ü aynı
dala düşüyor). Programatik sonda **her iki yönde de** hatalı çıktığı için
*"çıpanın 19 reddinin 10'u yanlış"* cümlesi **kurulmadı ve kurulmamalıdır.**
Kapanana dek **B10'un 16 → 14 sayıları şüpheli** sayılır.

---

## 🔴 AÇIK

### **[YB3 · karar S4]** `SOURCE_CLIP = 3500` hakemi k=10'da bağlamın yarısına kör bırakıyor 🔴 *ölçüldü, kapatılmadı*

`score_abstention.judge_gecerlilik()` (payda) **ve** `judge()` (pay) hakeme kaynak metnini
`[:3500]` kırparak veriyor. Ölçüldü 2026-08-06 (`[KAYNAK` sayımı):

| sınav | tam kaynak | klip 3500 ile görülen | oran |
| :--- | ---: | ---: | ---: |
| cp09 `m2b` (k=4 kurgusu, n=80) | 320 | 320 | **%100** ✅ |
| `h2b_tgta_v1_h2b_k10` (n=80) | 800 | 454 | **%57** 🔴 |

`h2b@k=10`'un bağlamı 3.203-10.281 karakter (medyan **7.174**), yani hakem *"kaynak soruyu
cevaplıyor mu"* sorusuna **eksik görüntüden** cevap veriyor. Somut vaka: `id=12`'de 10.281
karakterin 3.500'ü (4/10 kaynak) görülüyor; 7. kaynak soruyu cevaplıyorsa tuzak GEÇERSİZ
olmalıydı, geçerli sayılıyor ve modelin o kaynaktan verdiği doğru cevap `FABRICATE` yazılıyor.

**Neden bu dalgada büyütülmedi:** aynı sabit **pay hakemini** de besliyor; büyütmek tüm
tarihsel `verdict` sayılarını kıyaslanamaz kılar (tuzak 2.16'nın kardeşi). Ayrıca `k=10`
paydası ayrı bir kusurla (K-1, anahtar paylaşımı) karışmıştı; o dalga anahtarı tam metne
taşıdı ve ölçtü ki **anahtar onarımı sayıyı kıpırdatmıyor** (15 kalem yeniden ödendi, 15/15
aynı hüküm) — yani `Rej* = 0,723`'te bir yanlılık varsa kaynağı **klip**tir.

> ### 🚨 KARAR-4 (insan kararı, 2026-08-06) — klibi büyütmek **BİLİNÇLE REDDEDİLDİ**
> Bu turun **üçüncü** alet değişikliği olurdu ve pay hakemi aynı klibi kullandığı için
> **tüm çekinme sayıları yeniden oynardı**. Aynı kararla K-1'in tam-metin anahtarı da
> **geri alındı** (anahtar hakem istemine eşitlendi, `hakem_kaynagi()`), çünkü hakemin
> ayırt edemediği bir farka göre bölünen anahtar *aynı istem → aynı cevap* değişmezini
> kırıyordu (65 istem >1 anahtara · 83 gereksiz çağrı · `Rej*`'de ~1,5 p sahte oynama).
>
> **Bedeli açıkça ödendi:** `k=4` bağlamı `k=10`'unkinin öneki olduğu için ikisi tek payda
> kaydına düşer → **`k=10`'un paydası TANIMSIZ damgalıdır** (ADR-0057) ve *"`k` büyütmenin
> çekinme bedeli"* bir hüküm olmaktan çıkıp **borca** dönmüştür. Bu borcu kapatan tek şey
> aşağıdaki reçetedir.

**Kapatmak için gereken:** (a) payda klipi ile pay klipini **ayrı sabitlere** böl — payda
klipi büyütülebilir, pay klipi tarihsel süreklilik için sabit kalır; (b) k=10 paydasını yeni
klip ile yeniden öde (~80 kalem × `gpt-4o`, ölçülmüş birim maliyet **$0,0037/kalem** →
**≈$0,30**); (c) eski/yeni paydayı yan yana raporla; (d) kapandığında `k=10`'un **TANIMSIZ**
damgası kalkar ve `k`'nın çekinme bedeli ilk kez hüküm kurabilir. **Karar insana ait.**

### **[OQ-4]** `cp2c_kabul.sh` hangi hakem yığınıyla koşmalı? 🟡 *rejim kararı, kod hazır*

`cp2c_kabul.sh:39` → `LLM_GATEWAY="${LLM_GATEWAY:-openai}"`, oysa ölçüm koşuları
`openrouter` + sağlayıcı pini kullanıyor (global kısıt). Zincir 4. adımda **ortak**
içerik-adresli önbelleğe **yazıyor**; kusur K1'e kadar bu, openai damgalarının sonraki
openrouter ölçümlerine **sessizce** sızması demekti. Sızıntı **kapatıldı**
(`onbellek_isabeti()` uyuşmazlıkta durur, iki yönde de), ama varsayılan **değiştirilmedi**:
kabul ölçütünü hangi yığının ürettiği bir rejim kararıdır, sessiz bir düzeltme değil.
**Seçenekler:** (a) varsayılanı `openrouter` yap — kabul havuzu ölçüm yığınıyla eşitlenir,
ama geçmiş kabul koşularıyla kıyaslanamaz; (b) zincire ayrı `--gecerlilik-onbellek` ver —
yalıtılır, paylaşımın kazandırdığı devralma kaybolur. **Karar insana ait.**

⚠️ **Düzeltme 2026-08-06 (kusur k5) — sızıntı *"kirletemez"* değil, *"SESSİZCE kirletemez"*.**
Ayrım önemli: betik `LLM_GATEWAY=openai` ile koşulursa (bugünkü varsayılan) ve anahtar boşsa,
ortak önbelleğe **openai damgalı kayıt YAZILIR**. Yakalayan şey sonraki `openrouter` ölçümünün
`SystemExit`'idir — davranış **doğru** (fail-loud, K1), ama bedeli **sonraki koşuya** ödetiliyor
ve o koşunun sahibi elinde **kirlenmiş bir önbellekle** kalıyor.
🔴 **Kapanmayan:** kirlenen kaydı **düşürme yolu belgesiz**. `--gecerlilik-onbellek` ile
yalıtmak yalnız *bundan sonrasını* korur, **hâlihazırda yazılmış** openai damgalı kalemleri
temizlemez. Gereken: (i) hata mesajının temizleme yolunu **söylemesi** (hangi dosya, hangi
alan, kaç kalem), (ii) damgaya göre seçici düşürme reçetesi. ⛔ Bu dalgada kod değişmedi
(inceleme kod kalitesini onayladı) — **borç olarak açık**.

### **[OQ-2 · karar S5]** İkili oran eksenlerinin (M2 / M2b / M3 `Rej`) çözünürlük sınırı yazılmadı 🔴 *insan kararı*

Global kısıttaki **`0,3 A1 puanı = 0,003 kesir`** gürültü tabanı **yalnız A1 makrosu** içindir
(cevaplanan-only, hakemin yeniden-koşum gürültüsünden türetildi). Çekinme oranları **ikili
sayımlardır** ve kendi kuantumları var:

```
M2   payda 66  →  kuantum 1/66 = 1,52 puan
M2b  payda 77  →  kuantum 1/77 = 1,30 puan
M3   payda 80  →  kuantum 1/80 = 1,25 puan
```

⭐ **Isırdığı yer ölçüldü:** payda eşitlendikten sonra M2'de `tgta_v1` **55/66** ↔ Gemini
**56/66** — yayımlanan `−0,015` farkı **tam olarak bir kalem**, yani aletin ifade edebileceği en
küçük sıfırdan farklı değer. Bir hakem yargısı dönerse *"Gemini ile M2'de eşitlendik"* yazılır;
hareket eden şey ölçüm değil, tek bir yargıdır ([`MODEL_CARD.md`](../MODEL_CARD.md) ·
[`ROADMAP.md`](../ROADMAP.md)'de kuantum şerhi olarak damgalandı).

⛔ **Bu turda yeni bir taban UYDURULMADI.** Eşik/taban koymak **insan kararıdır** (ADR-0050'nin
ruhu: alet düzeltilir, eşik insan tarafından konur). Karar verilene kadar kural: *bu eksenlerde
`≤ 1 kalem`lik farktan hüküm kurulmaz, kuantum cümlede yazılır.*
**Seçenekler:** (a) `k` kalem kuralı — sabit bir kalem sayısı altındaki fark yorumlanmaz;
(b) ölçülmüş taban — aynı kolun yeniden-skorlamasıyla `Rej` oynamasını ölç (hakem maliyeti var);
(c) güven aralığı — Wilson aralığı, ek maliyet $0 ama kapı kuralını değiştirir.

### **[OQ-1 — kalan ayak: M3 paydası]** ~~M2'nin paydası hâlâ modele bağımlı — fiyatı ölçüldü~~ ✅ **KAPANDI 2026-08-06 (KARAR-3)**

> ✅ **Ödendi:** on koşunun `m2` paydası **$0,1054** ile eşitlendi (55-63 → **66/70**, 10/10 kol).
> Kayıt: [#59](record/research_log/2026-08-06-m2-paydasi-ve-karar-4.md) ·
> `outputs/eval/karar3-m2-payda/m2_payda_2026-08-06.json`.
> **ARA KAPI 1. gözlemi askıdan indi: `τ_a` M2 0,955 ≥ 0,923 ✅ GEÇTİ.**
> ⚠️ Düzeltmenin yönü **bizim lehimize** ve öyle raporlanıyor (en çok kayan özne **rakip**).
> Aşağıdaki metin, karar anındaki bilgi durumu olarak **silinmeden** duruyor.
> 🔴 **Kalan:** `m3`'ün paydası ADR-0048 m.2 gereği tanım gereği 80/80 olmalıyken cp09'da
> `54 · 56 · 39` — o ayak **hâlâ açık** ve hakemsiz/ücretsiz kapanır.

K3/KARAR-2 `m2b`, `h2b` ve `m3`'ü kapattı. **`m2` kapanmadı:** cp09'da üç kol **59 · 57 · 55**
payda gösteriyor (aynı sınav), yani `m2` oranları hâlâ kirli hakemden geliyor. Etkilenen
**10 koşu** — cp09 ×3 · cp09-ab-ayrımı · cp3-supurme ×2 · cp3c · sprint1 ×3.

⭐ **Tek ödemeyle onarılıyor:** on koşunun m2 sınavı **birebir aynı** (70 ayrık `(soru, referans)`
anahtarı, kesişim 70/70 — ölçüldü). Önbellek içerik-adresli olduğu için **70 hakem çağrısı**
hepsini kapatır: `referans` medyanı 586 karakter → **≈$0,11** (`gpt-4o`).

⛔ **Bu dalgada harcanmadı:** dalga bütçesi ≈$0,05-0,15 idi ve K-1'in yeniden ödemesi $0,056
tüketti; $0,11 daha eklemek tavanı aşardı → durup soruldu. Ayrıca bir kestirme **bilerek
reddedildi**: `cp2-r-kor-payda/valid_trap_cache.json`'daki 66/70 damgası $0'a devralınabilirdi
(52 kalemde metin ≤900 olduğu için hakem istemi bayt-bayt aynı, ispatlanabilir özdeşlik) —
ama o damga **`gateway=openai`** ile üretildi, bugünkü ölçümler **`gateway=openrouter`**;
ADR-0029/tuzak 2.7 hakem yığınının aynı olmasını şart koşuyor. Ucuz ama kirli.

**Bağlı olan:** ARA KAPI'nın **1. gözlemi** (`τ_a` tekil M2 ≥ base + 0,12) bu paydadan türüyor
ve bugün **askıda** — ne doğrulandı ne çürütüldü ([ADR-0045](adr/0045-ara-kapi-merge-onarim-kontrolu.md)).

### **[OQ-6]** Açılış-yeterlilik kuralının maruziyeti kollar arasında ~8 kat asimetrik 🟡 *ölçüldü, kural değişmedi*

ADR-0058'in açılış hükmü kuralı (`score_abstention._acilis_yeterlilik_hukmu`) her kolda aynı
sıklıkta **tetiklenmiyor**, çünkü modeller önsözü farklı sıklıkta uyguluyor. Ölçüldü 2026-08-06:

| kol | kural kapsamındaki cevap | olumlu açılış | olumlu ∧ gövdede red |
| :--- | ---: | ---: | ---: |
| `h2b_fl35_k4` | **39/80** | 19 | **4** |
| `h1_fl35` | **56/80** | 54 | 1 |
| `h2b_fl31_k4` | 8/80 | 4 | 0 |
| `h1_fl31` | 6/80 | 6 | 0 |
| BİZ önsözlü (`h2b`) | **5/80** | 5 | 1 |
| BİZ önsözsüz (`h2b`) | **0/80** | 0 | 0 |

**39 ↔ 5 = ~8 kat.** Kaydın bugünkü savunması *"bizim çıpalarımızda 0 satır değişti"* — bu bir
**gözlenen etki** argümanı, **maruziyet** argümanı değil: kuralın çevirdiği 3 satırın **üçü de**
manşet hükmün kurulduğu kolda (`h2b_fl35_k4`). Kural yanlı olmasa bile, hatası olsaydı **yalnız
o kolda** görünürdü. Kural bu dalgada **değiştirilmedi** (ADR-0050); asimetri kayda geçti.

### **[OQ-5]** 🐞 Gizil kusur — `harness_tablo.py:137` `id` ile liste indeksini karıştırıyor 🟡 *bugün çalışıyor*

`cevaplandi[i]` ifadesinde `i`, `gnd` kaydının **`id`**'si; oysa `cevaplandi` **konum-indeksli**
bir liste. Bugün doğru sonuç veriyor çünkü harness detay dosyalarında id'ler `0..n-1` sırayla
gidiyor (doğrulandı). **Devam ettirilen** (`--resume`) ya da **seyrek id**'li bir koşuda
`coverage` **sessizce yanlış** çıkar — hata vermez. Düzeltmek serbest; düzeltilirse **önce
düşen test** yazılır (seyrek id'li fixture).

### **[OQ-3 · karar S6]** Yeterlilik önsözünün atıf bedeli ürün açısından kabul edilebilir mi? 🔴 *ölçüm var, yorum yok*

`--sufficiency-preamble` (ana protokol, [ADR-0058](adr/0058-b-i-kaynak-yeterliligi-onsozu-benimsendi.md))
kütleyi ve A1'i yükseltiyor, ama bunu kısmen **daha az söyleyerek** yapıyor: hakem iddia sayısı
268 → **206** (−%23), atıf toplamı 118 → **83** (−%30), atıfsız geçen cevap 8 → **13**, katı
kapının reddi 1 → **3**; atıf hassasiyeti 0,8974 → **0,8732**, geri çağırma 0,8375 → **0,80**.
Uydurulmuş madde no sınıfı **iki koşuda da boş** — değişen paydadır, iddia değil.

**Soru:** atıf yoğunluğundaki bu düşüş, mevzuat asistanı için kabul edilebilir bir takas mı?
Kaynak-gösteren cevap sayısı düşerken doğruluk yükselmesi, kullanıcıya *"denetlenebilirlik"*
ekseninde bedel çıkarabilir. **Ölçüm var, yorum yok** — kural yazılmadan kapanmaz.

**Kaynak:** `outputs/eval/olcum-bi/harness_tablo.json` · `gnd_h1_tgta_v1_bi_k10_summary.json`
↔ `outputs/eval/s2-harness-k10-etiketli/` karşılıkları ·
[#56](record/research_log/2026-08-05-olcum-bosluklari.md) §5 (D1)

---

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

⚠️ **Yerine geçen açık soru:** `τ_a`'nın merge'de seyrelmesi (M2b 0,987 → **0,766** ᴷ³ —
yeniden puanlandı 2026-08-06, [#57](record/research_log/2026-08-06-cekinme-aleti-onarimi.md); `τ_a`'nın kendi sayısı **değişmedi**) **hâlâ
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
| **#12** ΔW norm asimetrisi | ⚠️ **HÜKÜM TERSİNE (2026-08-03)** — **ham TIES ana**, norm-dengeli ablasyon. Asimetri **ölçüldü** (8,87×: ‖τ_g‖ 10,47 ↔ ‖τ_a‖ 1,18) ve `‖τ‖` koşulsuz ölçülmeye devam eder; çürütülen şey *"dengelenmezse küçük kol silinir"* çıkarımı — ham TIES'te `τ_a` silinmedi (M2b **0,506→0,766** ᴷ³ ~~0,607→0,877~~; sıçrama +0,26 aynı, **onarım oranı %71→%57**), tersine dengeleme `τ_g`'yi ezdi (grounding 71,4%→53,4%). ⚠️ ᴷ³ damgası 2026-08-06'da eklendi (kusur Ö3): ADR-0052 ve `TASARIM.md`:337 damgalanırken aynı iddiayı taşıyan bu satır atlanmıştı | [**ADR-0052**](adr/0052-merge-norm-dengeleme-hukmu-tersine.md) ADR-0036'yı tadil eder · [#48 §24](record/research_log/2026-08-02-cp2c-modal-koprusu.md) |
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
