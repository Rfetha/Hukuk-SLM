# ADR-0040 — Düşünce modu **ölçülecek**: ön-kayıtlı karar kuralı · RS-FT'nin tetikleyicisi

**Statü:** Yürürlükte · **Tarih:** 2026-07-29
**Otorite belge:** `TASARIM.md` §8 · §10.2 · `sprint2.md` CP0
**İlgili:** **ADR-0030 madde 2 (düşünce modu KAPALI)** — bu ADR onu *sorguya açar*, geri almaz ·
**ADR-0035 (`τ_reasoning`/RS-FT kapsam dışı)** — YEŞİL sonuçta yeniden açılır ·
ADR-0028 (tek boyut noktası) · ADR-0017 (maliyet-normalize parite)
**Kanıt:** `research_log` [#39](../record/research_log/2026-07-24-cp0-base-dogrulama-kapisi.md)
(düşünce modu ölçümü, 4 koşullu düzenek) · [#41](../record/research_log/2026-07-29-cp6-tau-grounding-olcumu.md)
**Açık soru:** ADR-0030'un *"ayrı bir eksen olarak ölçmek meşru ama Sprint 1'in işi değil; açık
bırakıldı"* satırı — **bu ADR ile kapatılıyor.**

---

## Bağlam

Base **düşünen bir modeldir** (`Qwen/Qwen3.5-4B`), ve biz onu ADR-0030 madde 2 gereği
`--thinking off` koşuyoruz. Gerekçe ölçülmüştü ve sağlamdı:

1. **Eğitim-eval hizalaması** — SFT verimizde (`raft/`, `orpo_abstain/`, `grounded_qa/`) akıl
   yürütme izi **yok**; Qwen'in şablonu izsiz cevabı `<think>\n\n</think>` diye render ediyor.
   Yani veri modele düşünce-**kapalı** biçimi öğretiyor. Açık koşmak, eğitilmediği biçimde ölçmek
   olurdu (`900-char` eval-mirror kuralıyla aynı mantık).
2. **Sessiz çöp koşusu riski** — varsayılan modda model 1024 token bütçesinde `</think>`'i
   kapatmıyor, `content` **boş** dönüyor (HTTP 200, geçerli JSON, sıfır hata).
3. **Maliyet** — düşünce token'ı ödenen token'dır; `$`/sorgu metriğine doğrudan yazılır.

**Ama ADR-0030 kendi Limitations'ına şunu yazdı:** *"base'in **tam kapasitesini ölçmediğimiz**
anlamına gelir ve dürüstçe yazılır."* Bu satır bugün hâlâ **ölçülmemiş bir itiraf** olarak duruyor.

**Ve konu tekrar açıldı** (kullanıcı, 2026-07-29): *"thinking-off eğitmek hata değil mi?"*
Sezgi meşru — düşünen bir base seçip düşünmeyi kapatmak, seçilenin bir kısmını kullanmamaktır.

## Karar

### 1. Düşünce modu **ölçülür**, tartışılmaz — Sprint 2'nin 1. günü

İki koşu, `sprint2.md` CP0:

| | ölçüm | bedel |
| :-- | :--- | ---: |
| **a** | **base**, DEV havuzu, 6-mod CANON, `--thinking on` | GPU $0 (yerel) · hakem ~$0.15 |
| **b** | **`τ_g`**, `--thinking on`, ~20 çıktı **gözle** incelenir | $0 |

**Geçerlilik ön şartı (a):** `max_new_tokens 4096` **ve** kesik-cevap sayacı. Cevapların
**%5'inden fazlası** `</think>`'i kapatamadan kesilirse **koşu geçersizdir** — sonuç okunmaz,
bütçe artırılıp tekrarlanır. *(ADR-0030 ölçtü: 1024 yetmiyordu.)* Boş `content` zaten
`gen_eval_grounded.py` içinde erken patlıyor.

### 2. Ön-kayıtlı karar kuralı — **sonuç görülmeden yazıldı**

Referans, `base --thinking off` (DEV, #39/#41):
tuzak reddi **M2 Rej = 0.6330** · M1 sadık-cevap kütlesi **%42.6** · M5 ezber kütlesi **%10.7** ·
cevap başına **249 token**.

```
YEŞİL  →  M2 Rej ≥ 0.78            (+15 puan)
          VEYA M1 kütle ≥ %57.6    (+15 puan)
          VE   M5 ezber kütlesi ≤ %10.7   (Kapı 6 muhafızı, base'i geçmesin)

SARI   →  kazanç var, eşiğin altında — ya da M5 muhafızı ihlal

KIRMIZI→  her iki eksende de kazanç ≤ +5 puan
```

| sonuç | eylem |
| :--- | :--- |
| 🟢 **YEŞİL** | **RS-FT Sprint 2 kapsamına alınır.** ADR-0030 madde 2 geri alınır, **ADR-0035 yeniden açılır.** Sprint 1'in üç öznesi (base · Gemini · `τ_g`) thinking-açık protokolde **yeniden koşulur** (~$0.5) — yoksa Kapı 5'in referans noktaları farklı protokolden gelir. Takvim ~3-4 hafta uzar |
| 🟡 **SARI** | **Plan değişmez, eksen eklenir.** Thinking *rapor edilen bir eksen* olur (kapanış ölçümleri iki modda verilir); eğitim thinking-off kalır. RS-FT, Kapı 6 merdiveninin 4. basamağında bekler |
| 🔴 **KIRMIZI** | **ADR-0030 madde 2 kanıtla teyit edilir.** Limitations'taki *"tam kapasiteyi ölçmedik"* itirafı, *"ölçtük — bu protokolde fark yaratmıyor"* **bulgusuna** döner. RS-FT future-work'e sabitlenir |

**Eşiklerin gerekçesi.** +15 puan, *"hiç eğitilmeden, sadece düşünerek, bir kolun işinin kayda
değer bir kısmını yapmak"* eşiğidir: M2'de bu 0.633 → 0.78 demek (rakip Gemini 0.842); M1 kütlede
%42.6 → %57.6, yani `τ_g`'nin ulaştığı %72'nin yarı yolu. Türetilmiş sayılar değil, **yargı** —
ADR-0037'nin %90'ı gibi; ayırt etmesi gereken şeyi (haftalarca sürecek bir yola girmeye değer mi)
rahatça ayırt ediyor.

**Token maliyeti kapı DEĞİL, rapor edilir.** Kararı değil *dağıtımı* etkiler; ama doğrudan
maliyet-normalize parite matematiğine girer (249 → 2000 token = aynı donanımda sorgu başına ~8×
süre). ADR-0017'nin muhasebesine yazılır.

### 3. Ölçüm b bir **kapı değil, hasar sensörü** — eylemi (a)'ya bağlı

`τ_g` thinking-açıkken düzgün akıl yürütmüyorsa, bu yalnız *"düşünme öldü"* demek değil:
**reçetenin fazla sert olduğunun belirtisidir** (1.083 adım · lr 1e-4 · `all-linear` · r=16).
Ve o hipotez, CP6'nın **sahipsiz negatifini** — cevap doğruluğu %2.7 → %17.4 — de açıklayabilir.
Hiçbir kolun görevi o negatifi düzeltmek değil.

```
ÖLÇÜM b:
  BOZULMAMIŞ → reçete yumuşak; τ_g olduğu gibi devam.
               Düşünme kararı tamamen ölçüm a'ya kalır.

  BOZULMUŞ   → "eğitim fazla sertti" hipotezi güçlenir; sahipsiz doğruluk
               sorununun da açıklaması olabilir.
               → τ_g v2 (yumuşak reçete + replay karışımı) MASAYA GELİR
               → ama koşulmadan ÖNCE ölçüm a'nın sonucu beklenir:
                 a YEŞİL ise τ_g zaten RS-FT kapsamında yeniden doğar,
                 ayrı bir v2 israf olur.
```

`build_replay_tr.py` bu iş için repo'da hazır.

### 4. Kalıcı kural — `τ_g` her yeniden eğitildiğinde düşünme korunur

> **Bundan sonra `τ_g` (ya da herhangi bir kol) yeniden eğitilirse, düşünme yeteneğini koruyacak
> biçimde eğitilir** — replay karışımı ya da izli veri ile.

**Gerekçe:** yeteneği bugün kullanmıyor olmamız, yarın kapıyı kapatmamızı gerektirmez; ve kapıyı
açık tutmanın maliyeti **eğitim anında ≈ sıfır**, sonradan **yüksek** (yeni veri + hasar onarımı).

## Değerlendirilen alternatifler

| eleme | gerekçe |
| :--- | :--- |
| **Ölçmeden doğrudan thinking-on'a geçmek** | Eğitim verisinde iz yok → thinking-on eğitmek modele *"düşün diyorum ama işte boş düşünce örneği"* göstermektir: kapatmaktan **daha kötü**, çünkü yeteneği aktif bastırır. Ayrıca Sprint 1'in tüm sayıları geçersizleşir. Bu hatta iki kez makul hikâye ölçülünce çürüdü (`#40` `fla`, `#38` şablon) |
| **Ölçmeden thinking-off'ta kalmak** | Limitations'taki itiraf ölçülmemiş kalır; ve `τ_a`'nın referans noktası yanlış okunabilir — base düşünerek tuzak reddini zaten yükseltiyorsa `τ_a`'ya haksız kredi verilir |
| **`τ_reasoning`'i üçüncü kol yapmak** | ADR-0035 hâlâ geçerli: reasoning ↔ abstention çatışması **ölçülmedi**. Kafes 3→7, yeni kapılar, haftalar. YEŞİL çıkarsa yeniden değerlendirilir; şimdi değil |
| **Ölçüm b'yi bağımsız kapı yapmak** | Ölçüm a KIRMIZI çıkarsa — düşünme bu protokolde işe yaramıyorsa — kullanılmayacak bir yeteneğin ölümü için ~$5.5 ve günler harcanır |

## Sonuç — kabul edilen bedel ve şerhler

- ⚠️ **YEŞİL sadece iyi haber değil.** Base *hiç eğitilmeden* `τ_a`'nın işinin çoğunu yapıyorsa,
  *"ince-ayar ne kadar katkı veriyor"* sorusunun cevabı küçülür ve dış iddiada **üçüncü bir
  açıklama** belirir: kazanç ince-ayardan mı, harness'tan mı, **yoksa modelin zaten sahip olduğu
  düşünme yeteneğinden mi?** Bu, Kapı 2'nin (`D` vs `E`) sorduğu sorunun kardeşidir. Çıkarsa
  **negatif/daraltıcı bulgu olarak yazılır**, saklanmaz — ve makalenin çerçevesi değişir.
- Bu ADR **ADR-0030 madde 2'yi geri almaz**; onu ölçülebilir bir kurala bağlar. Geri alma yalnız
  YEŞİL sonucunda, bu ADR'nin kendi kuralıyla olur.
- `runs=1`, güven aralığı yok — Kapı 5/6 ile aynı sınır.
