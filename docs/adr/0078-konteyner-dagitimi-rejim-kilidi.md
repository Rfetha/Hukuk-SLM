# ADR-0078 — Konteyner dağıtımı: paketleme bir **REJİM KİLİDİDİR**, kolaylık değil

**Tarih:** 2026-09-10
**Statü:** yürürlükte
**Karar:** insan (2026-09-10, grill oturumu)
**Bağlı:** [ADR-0071](0071-v1-release-artefakti-tek-gguf.md) (tek GGUF, ad kuralı) ·
[ADR-0026](gemma4-12b-dersler.md#adr-0026) (base bir parametredir; tanımsızsa **ERKEN** patlar) ·
[ADR-0057](0057-harness-rekabet-kapisi-esit-sinav.md) (eşit sınav) ·
[ADR-0065](0065-bolunmus-surumleme.md) (bölünmüş sürümleme) ·
[ADR-0077](0077-v1-0-verilmedi-v0-3.md) (`v0.3`)
**Kaynak:** [`post-hp-hat-b-tickets.md`](../superpowers/plans/post-hp-hat-b-tickets.md) ticket 2 ·
[`kollar.md`](../record/kollar.md) 2026-09-09 bloğu (`sha256`, bayt sayısı)

## Bağlam — konteynerin gerekçesi ölçülmüş bir kusurdur

Bu hattın en pahalı hata sınıfı *"hata vermeden yanlış"*tır. Konteyner tartışması, o sınıftan
**ölçülmüş** bir kusurla açıldı:

| KV önbelleği | durum | `sha256` | uzunluk |
| :--- | :--- | :--- | ---: |
| `q8_0` — bütün ölçümlerin yapıldığı | SUSKUNLUK | `79b6915a…` | 201 |
| varsayılan (fp16) | ÇEKİNCELİ | `e97a2b85…` | 622 |

Aynı soru, aynı kod, `--seed 3407`, sıcaklık 0. Değişen tek etken sunucu bayrağıdır ve **cevap
değişmiştir** (ticket 2). Bugün modeli indiren kişi kendi bayraklarını seçer; bağlayıcı
yapılandırma yalnızca **düz metin olarak** üç belgede yazılıdır ve hiçbir şey onu zorlamaz.

İkinci ölçülmüş boşluk, artefakt kimliğidir. Yayımlanan `0,8011` **belirli bir dosyanın**
sayısıdır: `sha256 755e15e92e9f7021934f2d5eada6c1f02fcc92be23f0536b0c2a0a9586e7bffc`,
**2.783.446.720 bayt**. *"En güncel modeli çek"* diyen bir kurulum yolu, sürüm ilerlediğinde
imajı sessizce başka bir artefakta bağlar.

Üçüncüsü koddadır ve iddia değil okumadır: `hakhukuk/servis.py` çalışma anında `sys.path`'e
`scripts/` ve `scripts/erisim_korpus/` ekleyip `retriever.py`'yi oradan alır, indeks yolunu da
repo köküne göreli çözer. Oysa `pyproject.toml` `packages = ["hakhukuk"]` der ve ilk satırında
*"`scripts/` bilerek DIŞARIDA"* yazar. ⇒ Paket **tek başına kurulduğunda retriever'ı bulamaz**.

## Karar

**Ürün, üç kutulu bir `compose` dosyasıyla dağıtılır. İki daemon, iki imaj.**

```
hakhukuk-indir   TEK SEFERLİK   app imajının aynısı, farklı komut
                 HF'ten pinlenmiş revizyonu çeker → sha256 KAPISI → paylaşılan volume
                 tutmazsa çıkış kodu ≠ 0 ⇒ iki servis de HİÇ başlamaz

llama            daemon · GPU   llama.cpp sunucu imajı, volume'den GGUF okur
                 bağlayıcı bayraklar compose dosyasında YAZILI

app              daemon · CPU   hakhukuk + bge-m3 gömücü, volume'den indeks okur
                 HAKHUKUK_SUNUCU=http://llama:8080/v1 · yalnız 127.0.0.1'e yayımlanır
```

### Madde 1 — bağlayıcı bayraklar `compose` dosyasına birebir yazılır

Ölçüm rejiminin bayrakları — `-ngl 99` · `-fa on` · `--no-context-shift` ·
`--cache-type-k q8_0` · `--cache-type-v q8_0` · `-c 8192` — **değişmez** kopyalanır. Bunlar
tercih değil, ticket 2'nin ölçtüğü üzere **cevabı belirleyen** ayarlardır.

**Tek sapma vardır ve sebebi burada yazılıdır:** `--host 127.0.0.1` yerine `--host 0.0.0.0`.
Konteyner içinde `127.0.0.1` komşu servisten erişilemez. Erişim yüzeyi **daralmaz da
genişlemez**: yayın host tarafında `ports: "127.0.0.1:8080:8080"` ile aynı arayüze
kısıtlanır. Bu bayrak üretimi etkilemez; diğer altısı eder.

### Madde 2 — bayrak kümesinin bir TESTİ olur

`tests/test_konteyner.py` `compose` dosyasını ayrıştırır ve `llama` servisinin komutunu kanonik
kümeyle karşılaştırır. **Docker kurulu olmadan koşar.** Gerekçe `yurutme-tuzaklari.md`'nin
birinci maddesidir: bu hatta bayraklar sessizce düşer ve koşu hata vermeden yanlış sayı üretir.
Bağlayıcı yapılandırma düz metin olarak üç belgede duruyordu; hiçbiri kapı değildi.

### Madde 3 — indirme bir KAPIDIR, ADR-0026'nın kuralıyla aynı sınıftan

HF revizyonu **pinlenir**, `latest` kullanılmaz. İndirme sonrası `sha256` ve bayt sayısı
`kollar.md`'nin değerleriyle karşılaştırılır. Tutmazsa **erken çıkılır**; sessiz devam yoktur.
ADR-0026 tanımsız base için aynı hükmü kurmuştu: yanlış artefaktla saatlerce koşmak, hata
vermeden görünmez çöp üretir.

### Madde 4 — indeks iki yollu; G8'in bekleme gerekçesi bozulmaz

Volume'de indeks varsa kullanılır; yoksa HF dataset'ten çekilir. İkinci yol Görev 8'in **kod
gövdesidir**, ama *"83 MB mı 697 MB mı"* sorusu HF deposunda yaşar ve **imaj değişmez**.
Korpus 8,4× büyüdüğünde (40.496 → ~340.303 madde) yeniden verilecek karar dağıtım kararıdır,
paketleme kararı değil.

### Madde 5 — imaj repo ağacını kopyalar; borç YAZILIR, gizlenmez

`hakhukuk` paketi bugün tek başına kurulamaz (yukarıda, kod okumasıyla). Konteyner bunu
**onarmaz**: imaj ağacı kopyalar ve köprü bugünkü gibi çalışır. Bedeli açıkça yazılır —
`pyproject.toml`'un *"`scripts/` DIŞARIDA"* cümlesi çalışma anında geçersizdir ve bu, ticket
11 olarak açık kalır. Retriever'ı pakete taşımak yapısal bir değişikliktir; 26 dosyanın yol
köprüsü ve tüm ölçüm hattı aynı dosyayı kullanır, dolayısıyla kendi turunu ve kendi regresyon
koşusunu hak eder.

## Elenen seçenekler

| seçenek | niçin elendi |
| :--- | :--- |
| **Tek imaj, iki süreç** (supervisor ile `llama-server` + app) | GPU'suz makinede imajın yarısı ölü; CUDA katmanı boşuna taşınır; süreç yönetimi konteyner sınırını bulanıklaştırır. Tek `docker run` kolaylığı, iki farklı kaynak profilini (GPU ↔ CPU) tek kutuya sıkıştırmanın bedelini karşılamıyor. |
| **Ağırlığı bir registry imajına gömmek** | Yayımlanan artefaktın **ikinci bir kopyasını** yaratır. O gün *"gerçek artefakt hangisi"* sorusu doğar ve iki kopya ayrışabilir. HF zaten dağıtım kanalıdır, `sha256` orada yazılıdır, görünürlük kararı orada verilir. Yeni bir doğruluk yüzeyi açmanın karşılığı yok. |
| **Yalnız app konteyneri** (`llama-server` host'ta kalır) | En küçük imaj, ama bu ADR'nin **varlık sebebini** sağlamaz: rejim kilidi kurulmaz, kullanıcı yine kendi bayraklarını seçer. Kolaylık için paketlemek, ölçülmüş kusuru paketlememektir. |
| **İndirmeyi iki servise dağıtmak** (llama kendi GGUF'unu, app kendi indeksini çeker) | `sha256` kapısı iki yerde durur. Aynı mantığın iki yerde durup sessizce ayrışması bu repoda daha önce ölçüldü (istem metni, `AÇIK KARAR S18`). Kapı tek yerde durur. |

## Ne KURULMAZ

1. **Konteyner yayımlanan `0,8011`'i ÜRETMEZ.** O sayı ölçüm hattının (harness AÇIK, iki
   geçişli zorunlu düşünce kapatma) sayısıdır; konteyner **ürün yolunu** paketler. İkisi aynı
   şey değildir ve ticket 1 bu farkı sayıyla kaydeder (ürün yolu 7/80 kesik, 4/80 tamamen boş).
2. **Ticket 1, 3, 4 ve 6 çözülmez.** Boş cevap konteynerde de boş döner — Görev 19 sayesinde
   **503 olarak görünür**, giderilmez.
3. **`v1.0` iddiası doğmaz.** Sürüm hükmü ADR-0077'de duruyor ve engel ölçüm aygıtıdır
   (tek hakem ailesi, κ 0,534); paketleme o engele dokunmaz.
4. **`S9` açılmaz.** API ve konteyner **yerel ve tek kullanıcıdır**. Barındırma, kimlik, hız
   sınırı ve mahremiyet vaadi soruları `v2`'de açık durur.

## Bedel

Doğrudan para bedeli **$0**; GPU yereldir. İmaj boyutu **ölçülecektir, tahmin yazılmamıştır**.
Ölçülmemiş tek teknik ön koşul, WSL2 + Docker Desktop altında konteynerin GPU'yu görüp
görmediğidir (`nvidia-ctk` WSL yolunda bulunamadı, 2026-09-10). Bu, Görev 20'nin **sıfırıncı
adımı** ve ilk kapısıdır: tutmazsa topoloji yeniden kararlaştırılır.
