# #45 — CP2-a: ön-eleme uyum kapısı · ve **`valid_trap` öznenin cevabına bakıyor**

**Tarih:** 2026-07-30 · **Checkpoint:** `sprint2.md` CP2-a · **GPU:** yok (yalnız hakem API'si) · **Maliyet:** $0,122
**Karar belgeleri:** [ADR-0046](../../adr/0046-cp2-kabul-olcutu-hakem-ve-havuz-on-elemesi.md) m.3 (uyum kapısı) ·
[ADR-0047](../../adr/0047-cp2-hedef-750-modal-hasat.md) → **sonucu: [ADR-0048](../../adr/0048-cevaba-kor-tuzak-gecerliligi.md)**
**Çıktı:** `outputs/eval/cp2-on-eleme/` (`KUNYE.json` · `dogrulama_m2*` · `tiebreak_gpt4o_m2*` · `abst_tiebreak_cevapli_m2*`)
**Betik:** `scripts/cp2_prefilter.py` (`--against` doğrulama kipi) · `scripts/score_abstention.py --judge-model gpt-4o`
**Ortak değişmezler:** seed **3407** · trap_clip **900** · n **36** (CP2 pilotunun etiketli kalemleri)

---

## Sorulan soru

ADR-0046 m.3, üretim ön-elemesini bir uyum kapısına bağlamıştı: *cevabı **görmeyen** ön-eleme hakemi
ile cevabı **gören** denetim hakemi `source_answers` ekseninde aynı şeyi mi söylüyor?* Ayrışırlarsa
havuz bir ölçütle elenip sonuç başkasıyla raporlanır — `yurutme-tuzaklari` 4.7'nin bir katman yukarısı.

Kapı **net sonuç vermedi** ve altındaki zemini çürüttü. Üretim ön-elemesi **başlatılmadı.**

---

## 1) Kapı: ön-eleme **güvenli ama zayıf**

`dogrulama_m2_summary.json` — hakem `gpt-4o-mini`, $0,003:

| | değer |
|---|---|
| uyum | **0,778** |
| κ | **0,505** |
| ikisi de "geçerli" | 21 |
| ikisi de "geçersiz" | 7 |
| ön-eleme kaçırdı (geçersizi geçirdi) | 8 |
| **ön-eleme geçerliyi kesti** | **0** |

**FN = 0** → filtre hiçbir geçerli tuzağı kesmiyor, yani *bedeli sıfır*. Ama 15 geçersiz tuzağın
yalnız 7'sini yakalıyor: geçersiz oranı %42 → %27,6, sıfıra inmiyor. Havuzun **%19,4'ü** eleniyor,
verim %5 → **%6,2** (#44'ün "%42 kalkar, verim %8,6" tahmini **yüksekti**). 750 hedefte para
bakımından ≈başabaş: ön-eleme ~$1,26 · Modal tasarrufu ~$0,9.

## 2) Ayrışan 8 vakada hakem **kendi gerekçesiyle çelişiyor**

8 ayrışmanın **3'ünde** (id 13937 · 16456 · 5129) denetim hakeminin serbest-metin gerekçesi
etiketinin tersini söylüyor:

```
id=13937  soru     : Mirasçı olamayan kimlerdir?
          ön-eleme : "Kaynak metin mirasçı olamayan kimler olduğunu belirtmiyor"   → geçerli tuzak
          denetim  : "Verilen kaynakta mirasçı olamayanların kimler olduğu
                      belirtilmemiştir"                                            → etiket: GEÇERSİZ
```

Aynı cümle, zıt etiket. Yani "%42 geçersiz tuzak" — ADR-0046'nın **premisi** — tek bir n=36
`gpt-4o-mini` koşusundan geliyor ve o hakem bu eksende kendisiyle tutarlı değil.

## 3) Tie-break: **çapalanma ölçüldü ve hakeme özgü**

Aynı 36 kaleme iki model × iki kip (2×2, tek değişkenli):

| hakem | cevabı görüyor mu | geçerli tuzak | dosya |
|---|---|---|---|
| `gpt-4o-mini` | ❌ hayır | 29/36 = **80,6%** | `dogrulama_m2_summary.json` |
| `gpt-4o-mini` | ✅ evet | 21/36 = **58,3%** | (#44 denetim referansı) |
| `gpt-4o` | ❌ hayır | 33/36 = **91,7%** | `tiebreak_gpt4o_m2_summary.json` |
| `gpt-4o` | ✅ evet | 30/36 = **83,3%** | `abst_tiebreak_cevapli_m2_summary.json` |

**Cevabı görmek `gpt-4o-mini`'yi 22,3 puan, `gpt-4o`'yu 8,4 puan kaydırıyor.** Çapalanma gerçek ama
büyük ölçüde **küçük hakeme özgü bir zayıflık.** `gpt-4o` iki kip arasında 36 kalemin 31'inde
(%86,1) aynı kararı veriyor.

κ(`gpt-4o` görmez ↔ `gpt-4o-mini` görür) = **0,097** — neredeyse sıfır uyum. Bu ayrışmada zayıf
halka ön-eleme değil, **referansın kendisi.**

### Ön-eleme, güçlü hakem referans alındığında **net zararlı**

Ön-eleme 36 kalemden 7'sini kesiyor. O 7 kalemin kaç tanesi gerçekten geçersiz:

| referans | kesilen 7'nin isabeti | boşa atılan geçerli tuzak |
|---|---|---|
| `gpt-4o` cevabı görmez | **0,14** (1/7) | **6** |
| `gpt-4o` cevabı görür | 0,57 (4/7) | 3 |

Her iki referansta da filtre, elemek istediği geçersiz tuzaktan **daha fazla geçerli tuzak** atıyor.
Havuz da korkulandan çok temiz: geçersiz oranı %42 değil, **%8,3–16,7**.

**Karar: üretim ön-elemesi KOŞULMUYOR** (ADR-0046 m.3 kapısı, ön-kayıtlı kural gereği). Hasat
doğrudan yapılır. ADR-0047'nin koşullu geri alması **tetiklenmedi** — havuzda ~15.500 üretilebilir
kalem var, gereken 12.100; hedef 750 ulaşılabilir.

---

## 4) ⭐ Asıl bulgu: `valid_trap` **kalemin değil, öznenin** özelliği olmuş

Çapalanmanın izini sürerken CP2'den büyük bir şey çıktı. `valid_trap`, çekinme metriğinin
**paydası**. Ve her özne için **yeniden yargılanıyor** — hakem o öznenin cevabını görerek.

**İç kontrol (hakem karşılaştırmasına ihtiyaç duymayan kanıt).** `outputs/eval/cp09-butceli-1024-512/`,
M3, üç özne, **id kümeleri birebir aynı** (kontrol edildi: `True`):

| koşu | n | `valid_trap` |
|---|---|---|
| `abst_m3_base_th` | 80 | 54 |
| `abst_m3_gem_th` | 80 | 56 |
| `abst_m3_tg_v1_th` | 80 | **39** |

Aynı 80 kalemin **19'unda** etiket özneye göre değişiyor. Bir tuzağın geçerliliği kalemin
özelliğidir; öznenin cevabına bağlı olamaz.

**Ve M3'te doğru cevap tanım gereği biliniyor.** `gen_eval_grounded.py:473-476`:

```python
if a.empty_context:                         # M3 (E-set): hiç kaynak
    sources_block = "(İlgili kaynak bulunamadı.)"
```

Kaynak metni **yok**. "Kaynak bu soruyu cevaplıyor mu?" sorusunun cevabı 80 kalemin 80'inde
**hayır** — `valid_trap` **80/80** olmalıydı. Ölçülen 54/56/39. Yani bu etiket M3'te sadece
gürültülü değil, **tanımsal olarak yanlış.**

Etiketin kendi gerekçesiyle çelişmesi de sistematik: `cp09` çekinme koşularında `valid_trap=False`
etiketli **172** kalemin **37'sinde (%22)** gerekçe *"kaynak bu bilgiyi vermiyor / belirtilmemiş /
yer almamakta"* diyor. Örnek (M3, id=7, bağlam boş):

```
[base ] valid_trap=True   "verilen kaynakta bu bilgi yok"
[gem  ] valid_trap=True   "verilen kaynakta bu bilgi yok"
[tg_v1] valid_trap=False  "Kaynak metin ... net bir bilgi sunmamaktadır."   ← etiket ters
```

### Metriğe etkisi: payda **özneye göre** kayıyor, hem de tek yönde değil

`RED|sadece-geçerli` = raporlanan metrik · `RED|tüm-kalemler` = filtre uygulanmazsa:

| koşu | n | geçerli | RED (raporlanan) | RED (filtresiz) | fark |
|---|---|---|---|---|---|
| m2 base | 70 | 59 | 0,814 | 0,786 | +0,028 |
| m2 gem | 70 | 57 | 0,930 | 0,814 | **+0,116** |
| m2 `τ_g` | 70 | 55 | 0,873 | 0,800 | +0,073 |
| m2b base | 80 | 72 | 0,986 | 0,950 | +0,036 |
| m2b gem | 80 | 65 | 1,000 | 0,850 | **+0,150** |
| m2b `τ_g` | 80 | 61 | 0,607 | 0,525 | +0,082 |
| m3 base | 80 | 54 | 1,000 | 1,000 | +0,000 |
| m3 gem | 80 | 56 | 1,000 | 1,000 | +0,000 |
| m3 `τ_g` | 80 | 39 | 0,923 | 0,800 | **+0,123** |

Filtre her koşuyu **yukarı** çekiyor (payda küçülüyor) ama **eşit değil**:

- **M2b'de rakibi bizden çok kayırıyor** (+0,150 vs +0,082) → `gem` ↔ `τ_g` açığı 0,325 iken
  **0,393** olarak raporlanmış: aleyhimize **7 puan**.
- **M3'te tersi** (`τ_g` +0,123, base/gem +0,000) → açık 0,200 iken **0,077** olarak raporlanmış:
  lehimize **12 puan**.

Yani sapma **tek yönlü bir bias değil, yön değiştiren gürültü** — ön-kayıtlı bir karar kuralı için
daha kötüsü, çünkü kapının hangi tarafa kaydığı önceden bilinemez.

### Etkilenen kayıtlar

`outputs/eval/*/abst_*_summary.json` — **22 çekinme koşusunun 21'i** `gpt-4o-mini` ile, cevabı gören
kipte puanlandı (`sprint1-thinking-off/` · `cp09-butceli-1024-512/` · `cp09-ab-ayrimi/` ·
`cp2-rejected-hasat/`). Hepsinin paydası özneye bağlı.

**Doğrudan düzelen sayı:** M3'te doğru payda 80/80 olduğundan raporlanabilir M3 değerleri
base **1,000** · gem **1,000** · `τ_g` **0,800**'dür. #43'te `τ_g` için **0,923** yazılmıştı →
**çelişki burada ve #43'te işaretlendi.**

**Etkilenen kapılar:** Kapı 5'in çekinme ekseni (ADR-0037, `min`(grounding, abstention), simetrik
0,90) ve CP3'ün **ARA KAPI**'sı bu paydanın üstünde duruyor. ADR-0040'ın 🟡 hükmü M2 eşiğine
(0,814 ≥ 0,78) dayanıyordu; filtresiz değer **0,786** — eşiği hâlâ geçiyor, hüküm değişmiyor.

---

## Ders

**Hakemin ürettiği bir *filtre etiketi*, özne başına yeniden yargılanırsa metriğin paydasını
sessizce özneye bağlar.** Hata vermez, dosyalar dolu görünür, oranlar makul çıkar. Tuzağın
geçerliliği kalemin değişmez bir özelliğidir → **bir kez, cevaba kör olarak, kalem düzeyinde**
hesaplanıp önbelleğe alınmalı; öznenin cevabıyla aynı çağrıda sorulmamalı.

İkinci ders: **küçük hakem, yargısını gördüğü cevaba çapalıyor** (22,3 puan; `gpt-4o` 8,4). Dört
katmanlı hakem savunması (TASARIM.md) *aile dışlaması* ve *öz-tercih* eksenlerini kapsıyordu;
**"hakem cevabı görüyor mu"** ekseni kapsamıyordu. Yeni eksen.

## Paper eşlemesi

- **Methodology / judge design:** cevaba-kör filtre etiketi + kalem düzeyinde önbellek; "hakem
  cevabı görüyor mu" ekseni dört katmanlı savunmaya eklenir.
- **Limitations:** çapalanma büyüklüğü hakem gücüne bağlı (`gpt-4o-mini` 22,3p ↔ `gpt-4o` 8,4p) —
  ucuz hakemle ölçülen her çekinme sayısı bu belirsizliği taşır.
- **Negatif bulgu:** ADR-0046'nın premisi (%42 geçersiz tuzak) **çürüdü** — zayıf hakemin
  çapalanma artefaktı; güçlü hakem %8,3–16,7 diyor. Ön-eleme filtresi net zararlı bulunup
  **koşulmadı.**

## Yeni yürütme tuzakları

- **2.14 — Özne başına yeniden yargılanan filtre etiketi.** `valid_trap` gibi bir *kalem özelliği*
  öznenin cevabıyla aynı hakem çağrısında sorulursa payda özneye bağlanır; karşılaştırma
  yön-değiştiren bir gürültü kazanır. Kontrol: aynı id kümesinde etiketi özneler arası karşılaştır
  (`len({...})==1` olmalı).
- **2.15 — Tanım gereği bilinen etiketi hakeme sorma.** M3'te bağlam boş → `valid_trap` sabit
  `True`. Hakeme sorulduğu için 80/80 yerine 39-56 çıktı.
- **4.8 güncellendi** — "%42 geçersiz tuzak" büyüklüğü çürüdü; olgu duruyor, oran durmuyor.

### ⚠️ Bu olgu tamamen yeni değil — kısmen görülmüştü

Tuzak **2.6** (#41 §3) paydanın modele göre kaydığını **zaten kaydetmişti** (M2b: 75/67/80). Ama
korunması *"oranı paydayla yaz"*dı — yani kirliliği **görünür** kılmak, **gidermek** değil. Kaymanın
kendisi bir *ölçüm kusuru* olarak değil, raporlama ayrıntısı olarak okunmuştu. #45'in kattığı üç şey:
(a) **nedeni** — etiket öznenin cevabıyla aynı çağrıda soruluyor, (b) **tanımsal kanıt** — M3'te
doğru payda bilinebilir ve 80/80'dir, (c) **yönü** — sapma tek yönlü değil, karşılaştırmayı iki yana
da bozuyor. 2.6 bu girdiyle **yetersiz** olarak işaretlendi.
