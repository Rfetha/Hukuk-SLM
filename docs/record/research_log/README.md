# Araştırma Kaydı — kronolojik index

> **Bu klasör ne:** projenin **deney günlüğü.** Her anlamlı deney/bulgu/karar = ayrı dated dosya.
> İçerik **birebir** — özet değil. ADR'ler *kararı* tutar; buradaki girdiler **anlatıyı + sayıları +
> öğrenilen dersi** tutar. Yeni girdi → bu klasöre `YYYY-MM-DD-slug.md` + aşağıdaki tabloya satır.
>
> **Neden bu kadar önemli:** paper'ın **Results** ve **Discussion** bölümleri buradan yazılır.
> Bir sayı burada yoksa hiçbir yerde yoktur. *Numbers are sourced, not remembered.*

---

## ⚠️ Hat değişimi (2026-07-24)

**Gemma 4 12B hattının 38 girdisi tek dosyada birleştirildi ve tekil dosyalar silindi:**

### 📗 [`../gemma4-12b-kronoloji.md`](../gemma4-12b-kronoloji.md)

Künye (protokol sabitleri) + altı bölüm hâlinde tam kronoloji + paper eşlemesi.
**Sayılar birebir korundu** — damıtma yalnız anlatıda yapıldı. Silinen dosyalar git geçmişinde
duruyor (`4d70a77` ve öncesi).

Damıtılmış **dersler** ayrı belgede: [`../../adr/gemma4-12b-dersler.md`](../../adr/gemma4-12b-dersler.md)
Bölüm A. *(Orada "bundan ne öğrendik", kronolojide "ne oldu ve kaç çıktı" var.)*

> **Sıfırdan gelen için en kritik altı bulgu** — hepsi kronolojide:
> **#02** kaynaksız veri ezberletir (tek cevap 154 soruya yapıştırılmış) ·
> **#07** SFT abstention'ı yok etti (0.786 → 0.000) ·
> **#08** CANON metodolojisi ·
> **#24** Grounding-Abstention paradoksu ·
> **#36** tez çerçeve değişimi ·
> **#38** sessiz şablon tuzağı.

---

## Kronoloji — yeni hat

Numaralandırma **#39'dan devam eder** (kesintisiz akış korunur — 12B hattı #01-#38'di).
Yeni hattın protokolü ve tasarımı: [`TASARIM.md`](../../../TASARIM.md) · kararlar: ADR-0027.

| # | Tarih | Başlık | Kanca |
|---|---|---|---|
| **[39](2026-07-24-cp0-base-dogrulama-kapisi.md)** | 2026-07-24 | **Faz A: base kapısı (Qwen3.5-4B) + CP2 çıpaları** | 6/6 kapı · **dört sessiz-bozulma** (düşünce-modu · güç-durumu · red-regex `bulunmuyor` · teacher-jargon) · Kapı 0: `τ_register` düşer · base kör-red deseni %42.5 coverage |
| **[40](2026-07-25-cp4-fla-core-ve-hiz-kaldiraclari.md)** | 2026-07-25 | **CP4: Faz B'nin kapısı bir paket bölünmesiydi · 36 → 5.4 s/it** | `fla-core` ayrı pakete taşınmış → `import fla` çalışıyor, kapı **True** dönüyor, model **hiç yüklenmiyor** (fla'sızdan kötü) · *"torch≥2.11 gerekiyor"* teşhisi çürütüldü · **6.4× hız, reçete sabit** (kanıt: loss 0.7987↔0.788, `adapter_config.json`) · `dropout=0` **atfedilebilirlik** gerekçesiyle reddedildi · yerel kartın varsayılanları buluta taşınmıştı |
| **[41](2026-07-29-cp6-tau-grounding-olcumu.md)** | 2026-07-29 | **CP6: `τ_grounding` ölçümü — kör red kırıldı, bedeli cevap başına sadakat** | coverage **%43.8 → %85.0**, sadık-cevap kütlesi %42.6 → **%72.0** (Gemini %74.2) · **A1 0.973 → 0.847** ve **eşleştirilmiş 27 soruda da düşük** (0.977→0.878) = seçim değil, gerçek · düşüşün **%58'i biçim artefaktı** (RAFT meta-iddiaları hakeme desteksiz gidiyor → **kafesin 8 koşusunu taraflandırır**) · M2 0.633→0.458 **ön-kayıtlı**, M2b **1.000** · ❌ **anti-hedef ihlali: M5 A1 0.285 → 0.402** (parametrik sızıntı) · adaptör→GGUF zinciri yazıldı (akıtmalı merge, 2 doğrulama kapısı) |

| **[42](2026-07-29-cp0-dusunce-modu-sonlanmama.md)** | 2026-07-29 | **CP0: düşünce modu ölçülemedi — model DURMUYOR; ve bunu kol çözüyor** | `--thinking on`'da base **6 moddan 3'ünde hiç cevap üretmiyor**: kesilme değil **sonlanmama** (aynı muhakeme satırı **219×**; 32k token'da bile `content=''`) · döngü **belirsizlikle** geliyor — M4/M3 sonlanıyor, **M1/M2/M5 (karar eksenlerinin üçü)** sonlanmıyor · üç açıklama **elendi**: bütçe **8×** ❌, `temp 0.6` yarısı 🟡, **Q8_0** ❌ · ⭐ **`τ_g` v1 düşünüyor ve DURUYOR** (35/36, medyan **452 tok**, döngü yok, iz yapılı) → *"reçete fazla sertti"* **desteklenmedi**, ince-ayar akıl yürütmeyi **stabilize etmiş** · çözüm **bütçeli düşünce** (`--think-budget`, zorunlu kapatma) · maliyet **249 → ~1.198 tok (4.8×)** · yeni tuzak: 900-kar klip numaralı listeyi kesince model **sayıyı saymayı sürdürüyor** |

| **[43](2026-07-29-cp09-butceli-dusunce-cipalari.md)** | 2026-07-29 | **CP0.9: üç çıpa bütçeli kipte · anti-hedef ekseni 3.4× yanlış ölçülüyormuş** | ⭐ **ADR-0044**: kör modun sistem istemi feragat cümlesini EMREDİYOR, red-regex onu çekinme sayıyordu → ezber kütlesi base'de %10.7 → **%36.9**, sapma **bizim lehimize**; `τ_g`'nin ihlali aklanmadı **büyüdü** (+3.9→+7.3p) · ⭐ **düşünce = ayırt etme, biçim değil**: önsöz ablasyonu M2'yi 0.968'e çıkarıyor ama M1 kütlesini **28.2**'ye düşürüyor (aşırı-red 0.6875) → prompt alternatifi **elendi**, 4.5× token'ın karşılığı var · ⭐ **sonlanma kararlılığı eğitim istemi ailesine özgü**: `τ_g` RAG_MULTI'de zorunlu kapatma %91.7→**%5.8**, token 1098→**476**; dışında marjinal · **ADR-0040 hükmü 🟡 SARI** (M2 eşiği geçti 0.814≥0.78, M5 muhafızı İHLAL) → RS-FT kapsam dışı · `τ_g`'nin negatiflerinden **ikisi kapandı** (M2 0.873>base, M5 39.2<base), **M2b'de yenisi doğdu** (1.000→**0.607**) · n=3 smoke n=470'i temsil etmiyor |

| **[44](2026-07-30-cp05-cp1-cp2-zemin.md)** | 2026-07-30 | **CP0.5 · CP1 · CP2: Sprint 3'ün zemini — bir kapı kapandı, bir ölçüt çürüdü** | **CP0.5 🔴 kapı KALDI:** `causal-conv1d` kazancının **tavanı 1.254×** (kapı 2.0×), dört şekilde kararlı → **eklenmedi**; teşhis kaynaktan (çekirdekler bağımsız ikame ediliyor, pahalı özyineli çekirdek zaten `fla`'dan geliyor — *"fast path is not available"* uyarısı yalnız `warning_once`) · **CP1 ✅:** RAFT meta-iddia muafiyeti üç özneye birden uygulandı → `τ_g`'nin A1 açığının **%59'u artefaktmış** (0.120 → **0.049**), hatalı iddia oranı %18.1 → **%9.6** (ADR-0041 %9.9 demişti); kapsam ampirik daraltıldı (meta-cümle yalnız M1'de: base 36/80 · `τ_g` 58/80 · Gemini **0/80**); ⚠️ hedef-dışı etki **gürültünün 3 katı** (aynı istemle 2. koşu: −10 iddia gürültü vs −30 istem) · ⭐ **CP2 🔴 PİLOT DURDURDU:** ön-kayıtlı kabul ölçütü **regex**, raporlanan metrik **LLM hakemi** → kabul edilenlerin **%71'i gerçekte ABSTAIN**, **%42'si geçersiz tuzak**; gerçek verim %30 değil **%5**, hedef mevcut havuzdan **ulaşılamaz** (29.900 üretim > 19.284 kalem, ≈92 saat). ORPO'da bu havuz modele **çekinmeyi cezalandırmayı** öğretirdi ve hiçbir yerde hata vermezdi → yeni tuzaklar **4.7 · 4.8** |

| **[45](2026-07-30-cp2a-hakem-capalanmasi.md)** | 2026-07-30 | **CP2-a: ön-eleme kapısı çürüdü · ve `valid_trap` öznenin cevabına bakıyor** | **Ön-eleme KOŞULMADI:** FN=0 (güvenli) ama zayıf; güçlü hakem referansında **net zararlı** — kestiği 7 kalemin 6'sı geçerli tuzak (isabet 0,14) · ⭐ **çapalanma ölçüldü:** cevabı görmek `gpt-4o-mini`'yi **22,3p**, `gpt-4o`'yu 8,4p kaydırıyor → ADR-0046'nın premisi (%42 geçersiz) **artefakt**, gerçek %8,3–16,7 · ⭐⭐ **`valid_trap` özne başına yeniden yargılanıyor:** aynı 80 M3 kaleminde 54/56/**39**, 19 kalemde etiket özneye göre değişiyor; M3 bağlamı **boş** → tanım gereği 80/80 olmalıydı · payda **yön değiştiren** gürültü katıyor (M2b aleyhimize 7p, M3 lehimize 12p) · **22 çekinme koşusunun 21'i** bu paydayla puanlandı; Kapı 5 çekinme ekseni + ARA KAPI üstünde duruyor · `τ_g` M3 **0,923 → 0,800** (#43 ile çelişki işaretlendi) · yeni tuzaklar **4.9 · 4.10** |

| **[46](2026-07-30-cp2r-kor-payda.md)** | 2026-07-30 | **CP2-r: cevaba kör payda · üç eşik türetildi · düzeltme 4/6 karşılaştırmada ALEYHİMİZE** | ADR-0048 uygulandı, **$0,23**: paydalar m2 **66/70** · m2b **79/80** · m3 **80/80** (tanım, hakem yok) — kirli hakem geçerli tuzakları sistematik olarak geçersiz sayıyordu · `verdict` yeniden hesaplanmadı (cevaba bağlılığı meşru, geçersizlerde de kayıtlı 11/11) → yeniden puanlama **saf aritmetik, $0** · ⭐ **eşikler türetildi:** M2 0.934 → **0.923** · A1 0.888 → **0.880** · merge M2b 0.887 → **0.8541**; hareket tahminden (~0.91) **çok küçük: 1,1 puan** · ⭐ **M2b kurgu tabanı 79/80 ≫ 40/80 GEÇİLDİ** → pilotun *"m2b'de 24/25 geçersiz"* bulgusu **kirli hakem artefaktıymış**, merge onarımı ARA KAPI'nın 2. gözlemi olarak kalıyor · ⭐⭐ **düzeltme tek yönlü DEĞİL:** `τ_g`'nin base'e açığı üç modda da **büyüdü** (m2b 0,379 → **0,430** · m3 0,077 → **0,200**) ve en çok kayan özne **RAKİP** (Gemini M2 −0,082 · M2b −0,139 — kirli paydadan en çok o yararlanıyordu) → net etki **aleyhimize**, ön-kayıtlı eşiği yeniden türetmenin dürüstlük kanıtı · `τ_g` M3 **0,923 → 0,800**, M2b **0,607 → 0,519** |

⚠️ **Eski sayılar yeni tabloya karışmaz.** 12B protokolü (bf16/NF4, farklı base) ayrı satırda
raporlanır; **dersler taşınır, rakamlar taşınmaz.**

---

## Girdi yazma kuralları

- **Aynı gün yaz.** Sohbette kalan bulgu, kaybolmuş bulgudur.
- **Sayıyı kaynağıyla yaz:** metrik + n + hakem + seed + çıktı dosyası yolu.
- **Negatif ve şaşırtıcı sonuçlar birinci sınıf** — reddedilen tur da tam rigorla kaydedilir.
- **Paper eşlemesini belirt:** bulgu hangi bölüme yarıyor (ablasyon / negatif bulgu / methodology /
  limitations).
- **Çelişki çıkarsa her iki yerde işaretle**, sessizce üzerine yazma.
