# G21 — "Zayıf eşleşme" rozeti mümkün mü? (Adım 8)

**Bu bir ÖLÇÜMDÜR, özellik geliştirme değil.** Sonuç "rozet eklenmez" ise bu bir BULGU'dur,
başarısızlık değildir.

## Soru

Ürün yüzeyine "bu soruda eşleşme ZAYIF" rozeti konulabilir mi? Konulabilmesi için,
`recall@10`'un **kaçırdığı** kalemlerin RRF skor dağılımı ile **tutturduğu** kalemlerin
dağılımı **ayrışmalıdır**. Ayrışmıyorsa rozet **eklenmez**.

## Rejim ve çıpa doğrulaması

| alan | değer | kaynak |
| :--- | :--- | :--- |
| indeks | `data/index/mevzuat_bge_m3_s2` | `outputs/eval/g21-zayif-eslesme/KUNYE.json` |
| k | 10 | idem |
| RRF_K | 10 (modül sabiti, ADR-0068) | `scripts/erisim_korpus/retriever.py:44` |
| yürürlük süzgeci | `Yururluk.YALNIZ_YURURLUKTE` (varsayılan) | `scripts/erisim_korpus/retriever.py:220` |
| DEV | `data/eval/dev/core_hard.jsonl`, n=80 | idem |
| retriever dosya commit | `49198adcc914b189e0b07cbf05894858a9c74303` | `outputs/eval/g21-zayif-eslesme/KUNYE.json` |
| **ölçülen recall@10** | **0,9500 (76/80)** | `outputs/eval/g21-zayif-eslesme/KUNYE.json` |
| **çıpa recall@10** | **0,9500** | `outputs/eval/f02-biz-onsozsuz/KUNYE.json` (`recall_at_10`) |
| tutuyor mu | **EVET — BİREBİR** (`cipa_tutuyor_mu: true`) | `outputs/eval/g21-zayif-eslesme/KUNYE.json` |

Çıpa birebir tuttuğu için rejim farkı aranmasına gerek kalmadı; Adım 3'ün "DUR" koşulu
tetiklenmedi.

## Kaçırılan 4 kalem

| index | kanun_no | madde_no | soru |
| :--- | :--- | :--- | :--- |
| 1 | 5237 | Madde 89 | Dikkatsizliğim yüzünden birden fazla kişi yaralanırsa ceza nasıl belirlenir? |
| 7 | 5237 | Madde 103 | Mağdur on iki yaşından küçükse ceza ne olur? |
| 25 | 6284 | MADDE 10 | Tedbir kararının tebliğ edilmemesi bir sorun mu? |
| 68 | 6098 | MADDE 99 | Sözleşmemde bir para birimi belirttiğimde ne olur? |

Kaynak: `outputs/eval/g21-zayif-eslesme/skorlar_80.json` (alan: `isabet_10=false`).

## Ayrışma analizi — 6 aday gösterge

Her aday için: kaçırılan (n=4) ve tutturulan (n=76) grubunun min/medyan/maks'ı, ve
kaçırılan her kalemin tutturulan dağılımı içindeki **yüzdelik konumu** (küçük yüzdelik =
kötü taraf = "gerçekten zayıf"; tam ayrışma için 4'ünün de düşük yüzdelikte olması gerekir).

Kaynak: `outputs/eval/g21-zayif-eslesme/skorlar_80.json`.

### 1. sıra skoru (`top1_skor`)

| grup | min | medyan | maks |
| :--- | ---: | ---: | ---: |
| kaçırılan (4) | 0,13025 | 0,13691 | 0,17424 |
| tutturulan (76) | 0,09100 | 0,16783 | 0,18182 |

Kaçırılanların yüzdelik konumu tutturulan dağılımında: **%69,7 · %13,2 · %17,1 · %15,8**.

### 1.↔2. sıra marjı (`marj_1_2`)

| grup | min | medyan | maks |
| :--- | ---: | ---: | ---: |
| kaçırılan (4) | 0,00231 | 0,02084 | 0,03986 |
| tutturulan (76) | 0,00000 | 0,02051 | 0,08902 |

Yüzdelik konum: **%73,7 · %10,5 · %69,7 · %22,4**.

### İlk 10'un ortalaması (`ortalama_skor`)

| grup | min | medyan | maks |
| :--- | ---: | ---: | ---: |
| kaçırılan (4) | 0,08912 | 0,09276 | 0,09721 |
| tutturulan (76) | 0,07793 | 0,10163 | 0,13167 |

Yüzdelik konum: **%19,7 · %21,1 · %10,5 · %30,3**.

### Skor yayılımı (`yayilim` = maks−min, ilk 10)

| grup | min | medyan | maks |
| :--- | ---: | ---: | ---: |
| kaçırılan (4) | 0,05606 | 0,06546 | 0,10753 |
| tutturulan (76) | 0,02127 | 0,09129 | 0,11861 |

Yüzdelik konum: **%78,9 · %18,4 · %31,6 · %17,1**.

### Skor standart sapması (`std_skor`)

| grup | min | medyan | maks |
| :--- | ---: | ---: | ---: |
| kaçırılan (4) | 0,01901 | 0,01934 | 0,03322 |
| tutturulan (76) | 0,00705 | 0,02861 | 0,04048 |

Yüzdelik konum: **%77,6 · %22,4 · %23,7 · %22,4**.

### Skor entropisi (ilk 10, normalize)

| grup | min | medyan | maks |
| :--- | ---: | ---: | ---: |
| kaçırılan (4) | 2,24559 | 2,28165 | 2,28436 |
| tutturulan (76) | 2,23523 | 2,26997 | 2,30000 |

Yüzdelik konum: **%10,5 · %72,4 · %67,1 · %75,0**.

## Okuma

**Hiçbir aday göstergede tam ayrışma yok.** En iyi aday (`ortalama_skor`, ilk 10 ortalaması)
kaçırılanları en tutarlı biçimde düşük yüzdeliğe (%10,5–%30,3) koyuyor, ama bu bile "kaçırılan
= alt kuyruk" demek değil: tutturulan 76'nın da alt %10-30'unda benzer ortalama skorlu kalemler
var, yani bir eşik konsa aynı miktarda **doğru getirilmiş** kalem de "zayıf" diye damgalanır
(yanlış pozitif rozet).

Daha çarpıcısı: `index 1` (Madde 89) — kaçırılan bir kalem — hem `top1_skor` hem `marj_1_2`
hem `yayilim` hem `std_skor` hem `entropi` göstergelerinde tutturulan dağılımının **üst
%70-79'una** düşüyor. Yani bu kalem, retriever'ın "güvenli" göründüğü (yüksek 1. sıra skoru,
geniş marj) çoğu doğru-getirilmiş sorudan **daha iddialı** bir skorla yanlış maddeyi
getirmiş — retriever kendinden emin ama yanlış. Skor dağılımı bu hatayı işaretlemiyor.

**⚠️ n=4 uyarısı — zorunlu damga.** Dört kalemden türetilecek herhangi bir eşiğin güven
aralığı berbattır: tek bir kalemin (index 1) konumu değişse "ayrışma" görüntüsü tamamen
değişir. Yukarıdaki yüzdelikler bile n=4 üzerinden okunuyor — istatistiksel güç yok, yalnız
örtüşme okunabilir. Görülen örtüşme zaten güçlü (tam ayrışmanın tersi), ama n=4 ile "kesin
ayrışmıyor" demek de aşırı iddialı olur — burada söylenen: **eldeki 4 örnekte ayrışma yok**,
daha büyük bir kaçırılan-kalem havuzu olmadan bu değişmez.

## HÜKÜM

**Rozet EKLENMEZ — ayrışma yok/zayıf (en iyi aday göstergede bile kaçırılanların üçte biri
tutturulanların en iyi yarısıyla örtüşüyor, biri en iyi çeyreğiyle); kusur 5a AÇIK kalır.**
