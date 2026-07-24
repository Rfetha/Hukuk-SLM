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
| — | — | *(ilk girdi bekleniyor)* | — |

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
