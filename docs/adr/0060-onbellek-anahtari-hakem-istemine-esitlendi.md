# ADR-0060 — Kör payda önbelleğinin anahtarı **hakem istemine eşitlendi**; `k=10`'un paydası TANIMSIZ

**Statü:** Yürürlükte · **Tarih:** 2026-08-06 · **Karar:** insan (KARAR-4)
**Otorite belge:** `docs/record/yurutme-tuzaklari.md` 2.17 · `scripts/score_abstention.py`
**İlgili:** [ADR-0048](0048-cevaba-kor-tuzak-gecerliligi.md) (cevaba kör payda) ·
[ADR-0057](0057-harness-rekabet-kapisi-esit-sinav.md) (eşit sınav / TANIMSIZ damgası) ·
[ADR-0029](0029-tek-model-erisim-kapisi.md) (hakem yığını) · ADR-0050 (eşik değil alet)
**Kanıt:** [#58](../record/research_log/2026-08-06-payda-tekillesmesi.md) ·
[#59](../record/research_log/2026-08-06-m2-paydasi-ve-karar-4.md)

## Bağlam

[#58](../record/research_log/2026-08-06-payda-tekillesmesi.md), tuzak **2.17**'yi bulup önbellek
anahtarını `sha256(soru ‖ TAM kaynak)`'a taşımıştı: `h2b k=4` ile `k=10`, 80 kalemin 15'inde
tek payda kaydını paylaşıyordu.

**Ama aynı giriş, onarımın sayısal karşılığının olmadığını da ölçtü:** 15 çakışan çift yeniden
ödendi, **15/15 aynı hüküm**. Sebebi yapısal — klip (`SOURCE_CLIP = 3500`) sabitken çakışan
çiftin hakem istemi **bayt-bayt aynıdır**, dolayısıyla hakem ikisini **ayırt edemez**.

## Karar

### 1. Anahtar hakem istemine geri eşitlenir

```
anahtar = sha256(soru ‖ NUL ‖ kaynak[:SOURCE_CLIP])
```

Klip **tek bir yerde** tanımlıdır (`score_abstention.hakem_kaynagi()`) ve pay hakemi, payda
hakemi ile anahtar **üçü de** oradan beslenir; ayrışmaları yapısal olarak imkânsızdır.

**Gerekçe — değişmez:** *aynı istem → aynı cevap.* Anahtarı istemden **ince** tutmak bu
değişmezi kırar. Ölçülen bedel: **5.363** ayrı hakem isteminin **65'i** birden fazla anahtara
düşüyor · **83 garantili gereksiz çağrı** · ve aynı istem iki kayda dönerse hakem
dönüklüğünde `Rej*` **~1,5 puan** oynar. Bu oynama *"k'nın çekinme bedeli"* diye okunur, oysa
**saf gürültüdür** — yani anahtar ayrımı, kapatmak istediği hata sınıfının **kendisini**
üretiyordu.

### 2. Bedeli KABUL EDİLİR ve **damgayla** taşınır: `k=10`'un paydası TANIMSIZ

`k=4` bağlamı `k=10`'unkinin **öneki** olduğu için ikisi aynı kayda düşer. Asıl kusur anahtar
değil **klip**: kör hakem `k=4`'te kaynakların **%100'ünü** (320/320), `k=10`'da **%57'sini**
(454/800) görüyor. Payda ekseni **eşleşmiyor** → ADR-0057'nin kendi mekanizması işler:

> Eşleşmeyen eksen **TANIMSIZ** damgalanır; o eksende **hüküm kurulmaz.**

**Sonucu:** [#56](../record/research_log/2026-08-05-olcum-bosluklari.md)'nın *"`k` büyütmenin
çekinme bedeli"* bulgusu (`Rej` 0,840 → 0,784) **hüküm olmaktan çıkar, BORCA döner.**
Sadakat eksenindeki bulgu ([#54](../record/research_log/2026-08-05-k-supurmesi-ve-a1-duzeltmesi.md),
A1 0,923 → 0,843) **etkilenmez** — o payda paylaşmıyor.

⛔ **Yumuşatılmaz.** *"Muhtemelen yine de geçerli"* yazılmaz. **Alet kuramadığı hükmü kurmaz.**

### 3. Klibi büyütmek bu turda **reddedilir**, borç olarak kalır

Turun **üçüncü** alet değişikliği olurdu ve pay hakemi (`judge()`) aynı klibi kullandığı için
**tüm tarihsel çekinme sayıları** yeniden oynardı. Reçete + fiyat (**≈$0,30**)
[`open_questions.md`](../open_questions.md)'de açık borç. Bu borç ödendiğinde m.2'nin TANIMSIZ
damgası kalkar ve `k`'nın çekinme bedeli **ilk kez** hüküm kurabilir.

### 4. Önbellek kaydı hakem YIĞINI kimliğini taşır (kusur K1)

Anahtar hakem modelini de kapıyı da taşımaz; okuma yolu bunları **ayrıca** denetler
(`onbellek_isabeti()`) ve uyuşmazlıkta **DURUR**. Damgasız (eski şema) kayıt da uyuşmazlıktır.
Gerekçe: `cp2c_kabul.sh` ortak önbelleğe `LLM_GATEWAY=openai` ile yazıyordu; sessiz devralma
tuzak 2.7 / ADR-0029 ihlalidir ve özet dosyaya `judge_gateway: "openrouter"` yazardı.

## Değerlendirilen alternatifler

| eleme | gerekçe |
| :--- | :--- |
| **Tam-metin anahtarı korumak** (#58'in hâli) | Kapattığı hatanın **sayısal karşılığı yok** (15/15 aynı hüküm), açtığı gürültü yolu **ölçülmüş** (65 istem, 83 çağrı, ~1,5 p). Net zarar |
| **Klibi hemen büyütmek** | Turun üçüncü alet değişikliği; pay hakemi de aynı klibi kullanıyor → **tüm** tarihsel `verdict` sayıları kıyaslanamaz olur. Ayrı tur işi |
| **Payda klipini pay klipinden ayırmak** | Doğru çözüm ve borcun reçetesinin (a) maddesi — ama yine **ölçüm** ister (k=10 paydası yeniden ödenir, ≈$0,30). Bu turun bütçesi ≈$0,11'di |
| **`k=10` satırını silmek** | Kayıt tahrif edilmez. Sayı durur, **damgalı** durur |
| **Anahtara `k` (kaynak sayısı) eklemek** | Anahtarı yine istemden ince yapardı — aynı değişmezi başka biçimde kırar; ayrıca hakemin gördüğü metin `k`'nın fonksiyonu değil, klibin |

## Sonuç — kabul edilen bedeller

- **Sınavı gerçekten paylaşmayan iki kol tek payda kaydına düşebilir.** Bu artık bilinen ve
  damgalı bir durum, sessiz bir kusur değil; ve tek örneği (`h2b k=4` ↔ `k=10`) etiketli.
- **Bir hüküm kaybedildi** (`k`'nın çekinme bedeli). Karşılığında o hükmün **kurulamayacağı**
  kayda geçti — bu hattın hata sınıfı, kurulmaması gereken hükmün sessizce kurulmasıdır.
- **Tuzak 2.17'nin reçetesi değişti, teşhisi durdu.** Çelişki üç yerde birden işaretli
  (kod · tuzak tablosu · #58 satırı).
