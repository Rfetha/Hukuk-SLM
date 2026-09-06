# ADR-0061 — Çekinme dedektörü istem rejimine bağımlıydı: alet onarılacak, eşikler yeniden çıpalanacak

- **Tarih:** 2026-09-06
- **Durum:** kabul edildi — **uygulama başlamadı**
- **Karar veren:** insan
- **Kaynak ölçüm:** [#60](../record/research_log/2026-09-06-hasat-kabul-olcutu-coktu.md)
- **Bağlar:** [`superpowers/plans/2026-08-06-asiri-red-tau-a-v2.md`](../superpowers/plans/2026-08-06-asiri-red-tau-a-v2.md) Görev 3 · 7 · 9 ·
  [taslak yol haritası](../superpowers/specs/2026-09-06-v1-v2-roadmap-taslak.md) §7.2 **S13**
- **İlgili:** [ADR-0050](0050-esik-degil-alet-duzeltilir.md) (eşik değil alet düzeltilir) ·
  [ADR-0051](0051-m2b-cift-kalibi-ve-chosen-uretimi.md) (şablon çıktısı gözle okunmadan kabul edilmez) ·
  [ADR-0058](0058-b-i-kaynak-yeterliligi-onsozu-benimsendi.md) (yeterlilik önsözü)

## Bağlam

B10 turunun Görev 3 pilotu koşuldu ve planın gözle-okuma adımı (Adım 3.8) kabul ölçütünü çürüttü:
**10 kabul kaleminin 6'sında** `rejected` alanı bir çekinme değil, **tam ve doğru atıflı cevaptı**
(`raft11188`: *"Sonuç olarak, itiraz süresi yedi gündür (İCRA VE İFLAS KANUNU, Madde 225)."*).

Kök neden ölçüldü ve tekrarlanabilir. `b10_hasat.py` hasadı **yeterlilik önsözü olmadan** koşuyor
(`sufficiency_preamble: false`); o rejimde cevapta açılış yeterlilik hükmü oluşmuyor —
**26/26 kalemde `_acilis_yeterlilik_hukmu` → `None`**. `exact_reject`
(`scripts/score_abstention.py:208`) o dalda **cevabın TAMAMINI** `REJECT_RE` ile tarıyor. Havuzun
cevap şablonu ise şu:

```
1) [gerekçe] … diğer kaynaklar … İÇERMEMEKTEDİR   ← REJECT_RE BURADA tetikleniyor
2) ##begin_quote## … ##end_quote##
3) Sonuç olarak, <CEVAP> (KANUN, Madde N).        ← gerçek hüküm BURADA
```

Yani tetikleyen ibare cevabın hükmü değil, **elenen kaynakların gerekçesi**. `exact_reject`'in
doğru okuyan yolu (`_son_esasli_ibare`) **yalnız açılış hükmü `True` iken** çalışıyor.

Sonucu: raporlanan `kabul_orani 0,1733` sahte; gerçek **~0,07** → **ön-kayıtlı D1 kapısı
(≥ 0,10) aslında düşüyordu.**

⚠️ Ve sorun hasada özgü değil: resmî **önsözlü** çıpada da açılış hükmü **75 `None` / 5 `True`**,
yani cevapların **%94'ü** aynı dala düşüyor.
⚠️ Çıpa bulaşmasının büyüklüğü **ÖLÇÜLMEMİŞ** — programatik sonda resmî çıpada 10/19 kalem
işaretledi ama gözle okunan 3'ten **2'si gerçek çekinme** çıktı; **sonda her iki yönde de
hatalı**, dolayısıyla *"çıpanın redlerinin yarısı sahte"* hükmü **kurulmadı**. Kesin olan yalnız
**bir** doğrulanmış yanlış pozitif (`id=19`).

## Değerlendirilen seçenekler

| # | seçenek | neden seçilmedi / seçildi |
| :-- | :--- | :--- |
| (a) | Yalnız `exact_reject`'in önsözsüz dalını onar | Hasadı kurtarır ama çıpanın gerçek B10 sayısı **ölçülmemiş** kalır — ve sondanın güvenilmez olduğu zaten ölçüldü |
| (b) | Alete dokunma, hasadı **önsözlü** koş | En hızlı ve çıpaları oynatmaz, **ama aleti bozuk bırakır**. Alet ürünün ölçüm yolunda da kullanılıyor (%94 aynı dal). Ayrıca hasat `τ_a` v1'in rejiminden uzaklaşır → v1↔v2 kol kıyası zayıflar |
| **(c)** | **Alet onarılır + çıpalar gözle okunur** | ✅ **SEÇİLDİ** |

## Karar 1 — alet onarılır, gözle okuma ölçüt olur

`exact_reject`'in önsözsüz dalı onarılır. Onarım **TDD ile** yapılır: #60'ta gözle okunan
kalemler (10 hasat + 3 çıpa) **test korpusudur**, "düzelttim" iddiası onlarla kanıtlanır.

→ **verify:** gözle okunan 10 hasat kaleminin **10'u** doğru sınıflanır (6 cevap · 4 çekinme) **ve**
çıpadan okunan 3 kalem doğru sınıflanır (`id=7` çekinme · `id=19` cevap · `id=20` çekinme).

Onarımdan sonra etkilenen koşular **yeniden puanlanır**. Bu **$0**'dır: `exact_reject`
deterministik regex, hakemsiz; elde **73 detail dosyası** var, yeniden üretim gerekmiyor.
Eski değerler ADR-0050 usulüyle **damgalanarak durur, silinmez**.

Çıpanın **80 kalemi gözle okunur** — B10'un gerçek sayısı ancak böyle belirlenir. Programatik
sonda bu iş için **yeterli değildir** (ölçüldü).

## Karar 2 — eşikler AYNI FORMÜLLE yeniden çıpalanır

Onarım çıpaları oynatırsa, Görev 7 ve Görev 9'un eşikleri **yeni aletin biriminde yeniden
türetilir** — eşiğin *değeri* değil, *formülü* korunur.

```
Görev 7 (kol kapısı):   aşırı-red < 0,425  ·  M2b Rej ≥ 0,95  ·  M1 A1 ≥ 0,88
Görev 9 (ürün kapısı):  kütle > %62,8  ·  B10 < 14/80  ·  M2b(önsözlü h2b@k=4) ≥ 0,809
                        ↑ bu sayıların hepsi BUGÜN ESKİ ALETİN BİRİMİNDE
```

🚨 **Bu karar, yeni sayılar GÖRÜLMEDEN verildi (2026-09-06).** Kayda geçmesinin sebebi budur:
sonradan verilse, eşiği ölçüme göre seçmek olurdu.

**ADR-0050 ile ilişkisi — genişletme, ihlal değil.** ADR-0050 *"eşik değil alet düzeltilir"* der ve
bu ADR aleti düzeltiyor. Ama #57'de görülen sorun şuydu: alet değişince eşik **eski birimde** kalıyor
ve hükmü yorumlanamaz oluyor (*"Görev 9'un `M2b ≥ 0,840` eşiği ESKİ ALETİN BİRİMİNDE"* diye kayda
geçmişti). Burada seçilen yol, eşiğe keyfî dokunmak değil, **aynı formülü yeni birimde yeniden
hesaplamaktır** — ARA KAPI'nın #58'de yeniden türetilmesiyle aynı işlem
([ADR-0045](0045-ara-kapi-merge-onarim-kontrolu.md): ön-kayıtlı olan **formüldü**, sayı değil).

## Kabul edilen bedel

1. **B10'un turdaki sayıları (16 → 14) yeniden puanlanana dek ŞÜPHELİ.** ROADMAP, MODEL_CARD ve
   README'deki B10 satırları bu onarımdan etkilenebilir.
2. **KARAR-6 kıyası yeniden koşulmalı.** Pilotun `np1 ↔ np8` sayıları (Jaccard **0,5278** ·
   kesişimde birebir aynı metin **3/19** · 2,57× hızlanma) **bozuk ölçütle** seçilmiş kümeler
   üzerinde toplandı; ölçüt onarılınca hükmü kurulamaz, yeniden ölçülür. ⛔ Hüküm **insanındır**.
3. **Pilot yeniden koşulur** (~50 dk Modal L4, ~$1). Bir kez ödenmiş GPU bedeli ikinci kez ödenir.
4. **Turun takvimi kayar.** Görev 4-10 bu onarım bitene dek **bloke**.

## Sonuçlar

- Yeni borç **YB7** ([taslak yol haritası](../superpowers/specs/2026-09-06-v1-v2-roadmap-taslak.md) §2)
  ve yeni risk **R10** (*ölçüt kırılganlığı*) kayda geçti.
- **Ders — #57'nin dersinin tekrarı:** `_son_esasli_ibare` #57/Ö2'de **tam bu hata sınıfı için**
  eklenmişti, ama **yalnız bir dala** bağlandı; üç hafta sonra yeni bir tüketicide (hasat) geri
  geldi. *Alet düzeltmesi aletin kendisinde ve **her dalında** yapılır.*
- **Ders — ADR-0051 ikinci kez kendini ödedi:** kabul ölçütü sayısal olarak sağlıklı görünüyordu
  (0,1733 > 0,10); yalnız **gözle okuma** çürüttü. Yeni bir tüketici bir dedektörü ilk kez
  kullanıyorsa, gözle okuma adımı **zorunludur**.
