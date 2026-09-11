# ADR-0079 — Zayıf-eşleşme rozeti **EKLENMEZ**: eşik ölçüme bağlanmıştı, ölçüm reddetti

**Tarih:** 2026-09-11
**Statü:** yürürlükte
**Karar:** model (ön-kayıtlı kural gereği — hüküm insana sorulmadan, **ölçümün kendisi**
tarafından verildi: *"ayrışmıyorsa rozet yoktur"* kararı işten önce yazılmıştı)
**Bağlı:** [ADR-0062](0062-b10-turu-kapatildi-hedef-egitimsiz-karsilandi.md) (emsal: bir turun
**ölçümle** kapanması, hedef eğitimsiz karşılandı) ·
[ADR-0050](0050-verim-kapisi-tahmin-edici-duzeltmesi.md) (alet düzeltilir, **eşik oynatılmaz**) ·
[ADR-0068](0068-rrf-k-60-to-10.md) (`RRF_K = 10`, skorların üretildiği füzyon) ·
[ADR-0069](0069-kabul-testi-tavan-kullanimi-raporlamasi.md) (tavan bir kapı değildir)
**Kaynak ölçüm:** `outputs/eval/g21-zayif-eslesme/` — [`BULGU.md`](../../outputs/eval/g21-zayif-eslesme/BULGU.md) ·
`skorlar_80.json` (ham) · `KUNYE.json` (rejim + çıpa) · betik
`scripts/erisim_korpus/zayif_eslesme_olc.py`
**Kayıt:** [#66](../record/research_log/2026-09-11-urun-yuzeyi-ve-aygit-kusurlari.md) §3

## Bağlam

Açık kusur **5**: kullanıcı 2026-09-09'da iki soruda birbiriyle tamamen ilgisiz kaynak
listeleri gördü (Amme Alacaklarının Tahsili 51 · Hususi Hastaneler 13 · Damga Vergisi 30 ·
Basın Mesleği 3). Model doğru davranarak sustu, ama arayüz *"getirilen kaynaklar sorunuzla
ilgisiz"* bilgisini **vermiyordu**; vatandaş bunu ürün hatası olarak okuyor.

Ölçülmüş bağlam: `recall@10` **0,9500**'dür — her yirmi sorudan birinde doğru madde ilk ona
hiç girmez. Kapsam yalnız yürürlükteki kanunlardır.

İstenen çözüm, getirilen kaynakların RRF skor dağılımına bakıp bir *"zayıf eşleşme"* rozeti
göstermekti. Bu rozetin var olabilmesi bir **ön koşula** bağlandı: `recall@10`'un
**kaçırdığı** kalemlerin skor dağılımı, **tutturduğu** kalemlerinkinden **ayrışmalıdır**.

## Elenen seçenek — eşiği ölçmeden koymak

Reddedilen yol: makul görünen bir skor eşiği seçip (*"top-1 skoru 0,13'ün altındaysa zayıf de"*)
rozeti hemen eklemek. Bu **uydurulmuş eşiktir** ve bu hattın kendi yasakladığı şeydir:

- **tuzak 2.17** — çıpası olmayan kapı maddesi, sayıyı göründükten sonra meşrulaştırır;
- **Görev 19 karar 5** — ürün yüzeyindeki her sayısal eşik ölçüme bağlanır;
- **[ADR-0050](0050-verim-kapisi-tahmin-edici-duzeltmesi.md)** — alet düzeltilir, eşik
  oynatılmaz.

Uydurulmuş bir eşiğin bedeli teorik de değildi: doğru getirilmiş sorularda rozet çıkarsa
vatandaş **doğru cevaba güvenmemeyi** öğrenir; hiç çıkmazsa rozet zaten yoktur. İkisi de
*"hata vermeden yanlış"* sınıfındandır.

## Ölçüm

n=80 DEV (`data/eval/dev/core_hard.jsonl`), indeks `mevzuat_bge_m3_s2`, `k = 10`,
`RRF_K = 10`, yürürlük süzgeci varsayılan (`YALNIZ_YURURLUKTE`), CPU, 65,7 s, **$0**, hakemsiz.

**Rejim çıpası birebir tuttu:** aynı koşuda `recall@10` **0,9500 (76/80)** ölçüldü ve çıpa
(`outputs/eval/f02-biz-onsozsuz/KUNYE.json`, `recall_at_10`) **0,9500** diyor
(`cipa_tutuyor_mu: true`). Yani ayrışmanın yokluğu **rejim farkının değil, verinin**
hükmüdür.

Kaçırılan dört kalem: `5237/Madde 89` · `5237/Madde 103` · `6284/MADDE 10` · `6098/MADDE 99`.

Altı aday gösterge sınandı. *"Yanlış alarm"* sütunu şunu sayar: dört kaçağın **dördünü birden**
yakalayacak biçimde eşiklenirse, aynı eşik kaç **doğru getirilmiş** kalemi de *"zayıf"* diye
damgalar:

| gösterge | kaçırılan (n=4) medyan | tutturulan (n=76) medyan | yanlış alarm |
| :--- | ---: | ---: | ---: |
| **`ortalama_skor`** *(en iyi aday)* | 0,09276 | 0,10163 | **23 / 76** |
| `top1_skor` | 0,13691 | 0,16783 | 53 / 76 |
| `marj_1_2` | 0,02084 | 0,02051 | 56 / 76 |
| `std_skor` | 0,01934 | 0,02861 | 59 / 76 |
| `yayilim` | 0,06546 | 0,09129 | 60 / 76 |
| `entropi` | 2,28165 | 2,26997 | 57 / 76 |

Kaynak: `outputs/eval/g21-zayif-eslesme/BULGU.md`, ham veri `skorlar_80.json`; sayılar bağımsız
bir kod incelemesinde `skorlar_80.json`'dan **yeniden hesaplanarak** doğrulandı.

İki gösterge daha keskin bir şey söylüyor: `marj_1_2` ve `entropi`'de **kaçırılanların medyanı
tutturulanlarınkinden daha iyidir** — retriever yanlış maddeyi getirirken de **kendinden emin**
görünüyor. Skor dağılımı bu hata sınıfını işaretlemiyor.

**n=4 damgası — zorunlu.** Dört kalemden türetilecek her eşiğin güven aralığı berbattır: tek
bir kalemin konumu değişse *"ayrışma"* görüntüsü tamamen değişirdi. Bu yüzden hüküm dar
kurulur ve *"kesin ayrışmıyor"* denmez.

## Karar

**Zayıf-eşleşme rozeti EKLENMEZ.** Ürün kodunda hiçbir sayısal eşik, hiçbir yeni rozet yoktur;
denetim bunu çiviledi (`grep -rn "zayif\|eşik\|threshold" hakhukuk/` → sıfır isabet).

Gerekçe tek cümlede: **eşik ölçüme bağlanmıştı, ölçüm reddetti.** Dört kaçak için yirmi üç
yanlış alarm, vatandaşın doğru cevaba olan güvenini bir hata sınıfını yakalamayan bir işaret
uğruna harcamaktır.

**Bu bir BULGUDUR, başarısızlık değil** — ve emsali [ADR-0062](0062-b10-turu-kapatildi-hedef-egitimsiz-karsilandi.md)'dir:
orada da bir tur, hedefi eğitimsiz karşıladığı **ölçüldüğü** için kapandı.

## Ne KURULMAZ

- Bu ölçüm **"zayıf eşleşme sinyali imkânsız"** demez. Dediği tam olarak şudur:
  *"bu altı gösterge, bu 80 kalemde, n=4 ile ayırmıyor."* Başka bir sinyal (sorgu-kaynak
  çapraz kodlayıcı skoru, cevabın kendi dayanak yoğunluğu, daha büyük bir kaçırılan-kalem
  havuzu) sınanmadı ve bu ADR onların önünü **kapatmaz**.
- *"Retriever iyi çalışıyor"* **denmez**. `recall@10` 0,9500 bir tavandır, kapı değildir
  ([ADR-0069](0069-kabul-testi-tavan-kullanimi-raporlamasi.md)); her yirmi sorudan biri hâlâ
  altın maddeyi hiç görmüyor.
- Yayımlanan hiçbir sayı bu ölçümden **etkilenmez**: ağırlıklar değişmedi, ölçüm hattına
  dokunulmadı, kütle hesaplanmadı.
- Kusur 5'in **(b)** yarısı bu ADR'nin konusu değildir; o ayrıca ve farklı biçimde kapandı
  (statik kapsam satırı, sınıflandırıcı **kurulmadı** — yanılan bir kapsam sınıflandırıcısı
  cevabı olan soruyu öldürür).

## Sonuç

- **Kusur 5a AÇIK KALIR** ve planın `AÇIK KUSURLAR` bölümünde *"ölçüldü, rozet eklenmedi"*
  damgasıyla durur.
- **Devir zorunludur.** Planın [kapanış ve devir kuralı](../superpowers/plans/2026-09-07-hp-hat-a-hat-b.md#kapanış-ve-devir-kuralı-insan-kararı-2026-09-10)
  gereği kapanış anında açık kalan her kusur adıyla bir sonraki plana devredilir; devredilmemiş
  açık kusur varsa **kapanış geçersizdir**. Kusur 5a bu kapsamdadır.
- **Ölçüm aleti duruyor ve yeniden kullanılabilir:** `scripts/erisim_korpus/zayif_eslesme_olc.py`
  çıpayı önce doğruluyor (`cipa_tutuyor_mu`), rejimi ve retriever commit'ini künyeye yazıyor.
  Kaçırılan-kalem havuzu büyürse (donmuş TEST'te `recall@10` **0,7500**) aynı soru **daha güçlü
  n** ile yeniden sorulabilir — ve o zaman hüküm değişebilir.
