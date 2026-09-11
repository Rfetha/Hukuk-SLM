# ADR-0082 — `app` kutusu da `--host 0.0.0.0` kullanır: ikinci sapma, **icra sırasında doğdu**

**Tarih:** 2026-09-11
**Statü:** yürürlükte
**Karar:** insan (2026-09-11) — sapma **onaylandı**
**Bağlı:** [ADR-0078](0078-konteyner-dagitimi-rejim-kilidi.md) (konteyner dağıtımı; **madde 2**
tek izinli sapmayı tanımlar — bu ADR onu **genişletir**, değiştirmez) ·
[ADR-0057](0057-harness-rekabet-kapisi-esit-sinav.md) (eşit sınav) ·
[ADR-0065](0065-bolunmus-surumleme.md) (bölünmüş sürümleme)
**Kaynak:** `compose.yaml` (`app` servisi) · `hakhukuk/api.py` (`HOST` sabiti ve şerhi) ·
ana planın [Görev 20](../superpowers/plans/2026-09-07-hp-hat-a-hat-b.md) Adım 1-5 kapanışı

## Bağlam — kilitli karar kümesinin **dışında** doğan bir sapma

ADR-0078 beş kararı kilitledi ve bunlardan **madde 2** yalnız `llama` kutusu için bir sapma
tanımlıyordu: üretimde `--host 127.0.0.1`'dir, konteynerde `--host 0.0.0.0` olur, çünkü
konteyner içinde `127.0.0.1` **komşu kutudan erişilemez**.

Görev 20'nin icrasında **aynı sorunun ikinci hâli** ortaya çıktı ve kilitli beş kararda
karşılığı yoktu. `hakhukuk/api.py` şunu der:

```python
HOST = "127.0.0.1"   # S9 açılmadı; buranın değişmesi ürünün vaadini değiştirir
```

Bu arayüze bağlanan bir süreç, konteyner içinde **host'tan erişilemez**: `ports` yönlendirmesi
konteynerin `eth0`'ına proxy'ler, **loopback'ine değil**. Dolayısıyla `app` kutusu
`hakhukuk-api` giriş noktasını çağırırsa servis ayağa kalkar ama **hiç kimse ulaşamaz** —
ve bu, hata vermeden başarısız olan bir yapılandırmadır.

## Karar

`app` kutusu `hakhukuk-api` yerine `uvicorn hakhukuk.api:uygulama --host 0.0.0.0 --port 8000`
çağırır. Gerekçe **ADR-0078 madde 2 ile birebir aynı sınıftandır** ve aynı iki koruma
yürürlüktedir:

1. **`api.py` DEĞİŞTİRİLMEDİ.** Ürün kodunun `127.0.0.1` diyen vaadi ve yanındaki şerh
   **yerinde durur**. Sapma yalnız *paketleme* katmanındadır.
2. **Erişim yüzeyi daralmadığı gibi GENİŞLEMEZ** de: `ports: "127.0.0.1:8000:8000"` yayını
   host'un loopback'ine kısıtlar. Konteyner **yerel ve tek kullanıcı** kalır.

⇒ **`S9` yine AÇILMADI.** Barındırma, mahremiyet vaadi ve TR IP kısıtı soruları `v2`'de
açık durur.

## Elenen seçenek

| seçenek | niçin elendi |
| :--- | :--- |
| **`api.py`'ye bir ortam değişkeni eklemek** (`HAKHUKUK_HOST`) | Ürün kodunu **yalnız paketleme kolaylığı için** değiştirirdi. Üstelik `HOST` sabitinin yanındaki *"buranın değişmesi ürünün vaadini değiştirir"* şerhini **tam da şerhin uyardığı biçimde** aşındırırdı: bugün konteyner için eklenen bir değişken, yarın barındırma için kullanılır ve `S9` **kimse karar vermeden** açılmış olur. |

## Niçin kendi ADR'si var

Bu madde **icra sırasında doğdu**, tasarım turunda değil. Kilitli bir karar kümesinin dışında
kalan bir sapmayı **sessizce uygulamak, kilidin kendisini anlamsız kılar** — kilit ancak
kapsamadığı şeyi görünür kıldığı sürece kilittir.

ADR-0078'in metni **değiştirilmedi**: o gün beş karar kilitlenmişti ve kayıt öyle durur.
Altıncı karar buradadır ve 0078'e **tek satırlık bir işaretçi** düşülmüştür — çelişki
**iki yerde** damgalanır, biri diğerinin üstüne yazılmaz.

## Ne KURULMAZ

- Bu ADR **`api.py`'nin davranışını değiştirmez** ve `HOST` sabitini **tartışmaya açmaz**.
- Bu ADR *"konteyner ağa açılabilir"* **demez**. `ports` yayını `127.0.0.1`'dedir ve bunu
  değiştirmek **ayrı bir karardır** (`S9`).
- Bu ADR, sapmanın **ölçülmüş** bir gerekçesi olduğunu iddia etmez: gerekçe ölçüm değil,
  konteyner ağının **tanımı**dır. ADR-0078 madde 1'in bayrakları ise ölçülmüştür ve onlara
  **dokunulmamıştır**.

## Bedel

Konteyner yolunda çalışan süreç, üretimde çalışandan **bir bayrak** farklıdır ve bu fark
`compose.yaml`'da **yorumla** yazılıdır. Uçtan uca doğrulama (`docker compose up`) **henüz
koşmadı** — Görev 20 Adım 6 insandan `HF_TOKEN` ve indeks kaynağı bekliyor. Bu ADR o
doğrulamanın **yerine geçmez**.
