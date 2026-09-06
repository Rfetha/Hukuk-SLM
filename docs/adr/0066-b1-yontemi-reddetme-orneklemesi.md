# ADR-0066 — B1 (isabetsizlik) yöntemi: **reddetme-örneklemesi**; GRPO/RLVR bütçe kapısıyla ertelendi

**Tarih:** 2026-09-06 · **Statü:** ✅ yürürlükte · **Karar:** insan
**Eksen:** [ADR-0055](0055-isabet-denetimi-ekseni.md) — *"eksen belirlendi, kod hiç açılmadı"*

## Borç

**İsabetsizlik:** model **gerçek ama soruya uymayan** bir maddeden cevaplıyor. Vatandaş ürünü
için en tehlikeli kusur sınıfı: cevap iyi biçimli, atıf **doğrulanıyor**, ama yanlış hükmü
gösteriyor — uydurulmuş atıftan (bizde **0/114**) daha sinsi, çünkü deterministik atıf
doğrulaması onu **yakalayamaz**.

**Ölçülen büyüklük (2026-09-06, v2 birimi, gözle tam tarama): 8/80.**

## ⭐ Neden otomatik vekil metrik YOK — ölçüldü

75 cevaplanan kalemin tamamı gözle tarandı ve iki otomatik süzgeç karşılaştırıldı:

| süzgeç | bulduğu | **kaçırdığı** |
| :--- | ---: | :--- |
| `faithfulness < 0,6` | 4 | 27 · 36 · 41 — faith **1,00 · 1,00 · 0,67** |
| altın madde atıflarda yok | 3 | 29 · 30 · 42 · 61 — cevap altını **başka yerde anıyor** |
| **gözle tam tarama** | **8** | — |

⇒ Yüksek `faithfulness` isabetsizliği **elemez** (hakem, modelin dayandığı yanlış maddeye göre
tutarlı bulabilir) ve atıf listesi de elemez (cevap birden çok madde anabilir).
**ADR-0055'in ekseninde kodun açılmamış olmasının mekanik açıklaması budur.**
⛔ B1 turunun kabul ölçütü **gözle okumaya** dayanmak zorundadır; sayısal vekil yeterli değildir.

## Karar: ÖNCE reddetme-örneklemesi

```
n cevap üret  →  yalnız ATIFI ALTINA DOĞRULANANLARI tut  →  TRL SFTTrainer ile eğit
```

**Gerekçe — alet zaten var ve doğrulanmış:** `scripts/b10_hasat.py` · Modal `harvest_b10`
(ADR-0047 m.2 taşıyıcısı: Q4_K_M GGUF + llama.cpp, KV q8_0, `-fa on`, **vLLM/bf16 YASAK**),
L4'te doğrulandı; sızıntı süzgeci havuzu 13.350 → **12.914**'e indiriyor ve konteynerde yerelle
birebir. Devir notu açıkça *"B1 için yeniden kurma"* diyor.
**Tahmini bedel ~$5.**

## ⛔ GRPO / RLVR ertelendi — gerekçeli

Verifier'larımız **deterministik ve programatik** (`atif_dogrula.py` · `groundedness.py` ·
`score_abstention.py`), yani B1 **doğrulanabilir ödül** problemine birebir uyuyor: SFT bunu
ancak taklit ederken RLVR *"doğru maddeyi göster"*i doğrudan ödüllendirir. **Yöntem olarak
daha doğru eşleşme budur.**

**Ama:** 8-16 rollout/istem × (1024+512) bütçe → **$10-30 tahmin**, Modal'da **$29,19** var
ve **tahmin ölçülmedi**. Tek tur bütçenin çoğunu yiyebilir.

**Açılma koşulu (ön-kayıtlı):** reddetme-örneklemesi turu kapandıktan sonra isabetsizlik
**8/80'in altına inmediyse** GRPO kendi ADR'si ve kendi bütçe kapısıyla açılır. Açılmadan önce
**küçük bir pilotla birim maliyet ölçülür** — tahminle bütçe harcanmaz.

## Reddedilenler
- **Doğrudan GRPO** — REDDEDİLDİ: ölçülmemiş bir tahminle bütçenin çoğunu riske atar.
- **İkisini de koş, karşılaştır** — REDDEDİLDİ: metodoloji paper'ı için değerli olurdu ama
  B4/YB2'ye bütçe kalmaz.
- **İstem katmanında çöz** (yeterlilik önsözü gibi) — REDDEDİLDİ ve **ölçüldü**: önsöz
  isabetsizliği 7/80 → 5/80 yapıyordu ama kütleyi **4,6 puan** düşürüyordu (ADR-0063).
  Yama, eksenin kendisini ödemez.
