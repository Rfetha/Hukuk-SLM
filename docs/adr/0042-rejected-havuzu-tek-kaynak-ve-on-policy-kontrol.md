# ADR-0042 — `rejected` havuzu **tek kaynaktan** (ham base) · Taban B için **on-policy kontrol koşusu**

**Statü:** Yürürlükte · **Tarih:** 2026-07-29
**Otorite belge:** `TASARIM.md` §4.1 (kol verisi) · §4.4 (karşılaştırma tabanları)
**İlgili:** **ADR-0037 (Kapı 5 — "iki tabanı da geç" şartı)** · ADR-0027 (görev-vektörü:
her kol ham base'den) · ADR-0034 (12B artefaktları emekli)
**Kanıt:** `research_log` [#41](../record/research_log/2026-07-29-cp6-tau-grounding-olcumu.md)
(çalışan çıkarım hattı CP6'da doğdu — hasadın önkoşulu buydu)

---

## Bağlam

`τ_abstention` bir ORPO koşusudur: her örnekte bir `chosen` (doğru davranış = reddetme) ve bir
`rejected` (istenmeyen davranış = tuzağa düşüp cevaplama) çifti gerekir.

**Mevcut `rejected` havuzu kullanılamaz:** emekli **Gemma 4 12B** hattının fabrikasyonlarından
üretilmişti. Olduğu gibi kullanmak, yeni modele **başka bir modelin hatalarını** öğretmek olur —
ORPO'nun negatif örnekleri, eğitilen modelin gerçekten yapabileceği hatalar olmalıdır.

Yeniden hasat için gereken *"çalışan yerel çıkarım hattı"* CP6'da doğdu (merge → GGUF →
`llama-server`). Hasat **yerel ve $0**.

## Sorun — hangi modelden hasat edileceği üç kola birden dokunuyor

| kol | hangi ağırlıktan eğitiliyor | "on-policy" havuz ne olurdu |
| :--- | :--- | :--- |
| **FT-2** `τ_a` | ham base | **base**'den hasat |
| **FT-4** Taban A (tek-aşamalı karışık SFT) | ham base | **base**'den hasat |
| **FT-6** Taban B aşama 2 (ardışık SFT) | **FT-5'in çıktısı** | ⚠️ **FT-5'in modelinden** hasat |

🚨 **Taraflılık burada:** FT-6'ya base'den hasat edilmiş `rejected` verirsek, o örnekler FT-5'in
modelinin *gerçekten söylediği* şeyler değildir → **off-policy** → taban **zayıf eğitilir.**
ADR-0037'nin Kapı 5'i *"Taban A ve Taban B'nin İKİSİ de geçilmeli"* diyor; yani bu sapma
**doğrudan bizim lehimize** kayar ve *"tabanı zayıf eğittiniz"* itirazı Kapı 5'in tamamını
çürütebilir.

## Karar

### 1. Ana sonuç: **tek havuz, ham base'den hasat** — tüm kollar aynı veriyi görür

`τ_a` · Taban A · Taban B'nin her iki aşaması, **aynı** `rejected` havuzunu kullanır; havuz
**çıplak base**'den (`Qwen/Qwen3.5-4B`, `--thinking off`, aynı üretim ayarları) hasat edilir.

**Gerekçe:** ablasyonun anlamı veriyi sabit tutmaktan gelir. Veri kollar arası değişirse, ölçülen
fark ne yönteme ne veriye atfedilebilir — iç iddia ölçülemez hâle gelir.

### 2. Robustluk kontrolü: **FT-6 ikinci kez**, FT-5'ten hasat edilmiş veriyle

Aynı taban, tek fark `rejected` kaynağı (FT-5'in kendi çıktısı = on-policy).

- **Bedel:** ORPO **82 adım** — ~$0.5 GPU + ~$0.15 hakem ≈ **$0.65**
- **Nerede raporlanır:** **robustluk satırı**, ana tablo değil. Ana sonuç her zaman veri-sabit
  koşudur (madde 1)
- **Ne satın alır:** *"tabanı off-policy veriyle sakatladınız"* itirazı ölçümle kapanır.
  Kapı 5'in en saldırıya açık noktası $0.65'e sigortalanır

**Yorum kuralı (ön-kayıtlı):** on-policy taban, veri-sabit tabandan **anlamlı biçimde iyiyse**
(bileşik ölçütte ≥ +0.05), Kapı 5'in *"iki tabanı da geç"* şartı **on-policy sürüm üzerinden**
okunur — yani daha güçlü tabana karşı kazanmamız gerekir. Kural şimdi yazıldı ki sonuç görülünce
lehimize olan sürüm seçilmesin.

### 3. Hasat künyesi kayıt altına alınır

`research_log`'a: base sha · `--thinking off` · sıcaklık/`top_p` · `max_new_tokens` · seed **3407**
· üretim tarihi · kaç örnekten kaçının `rejected` olarak kabul edildiği (kabul kriteri:
`score_abstention.py` RED **saymıyor**, yani model tuzağa düşmüş). `τ_a`'nın rejimi
`TASARIM.md` §4.1.1 ile eşleşmeli.

## Değerlendirilen alternatifler

| eleme | gerekçe |
| :--- | :--- |
| **Her kol kendi on-policy havuzunu kullansın** | Her kol kendi içinde metodolojik olarak ideal olurdu. **Ama veri kollar arası değişir** → fark ne yönteme ne veriye atfedilebilir; ablasyonun anlamı gider. Tez tam olarak *"yöntem farkı"* iddia ediyor |
| **Mevcut 12B havuzunu kullanmak** | Yeni modele başka bir modelin hatalarını öğretir; ORPO'nun negatifi eğitilen modelin yapabileceği hata olmalı. Ayrıca 12B artefaktları emekli (ADR-0034) |
| **Sentetik/kural tabanlı `rejected`** | Modelin gerçek hata dağılımını temsil etmez; ORPO sinyali zayıflar. Ayrıca "hangi kural" sorusu yeni bir keyfîlik kaynağı |
| **FT-6'yı yalnız on-policy koşmak** (veri-sabiti atlamak) | Ana kıyası bozar (madde 1'in gerekçesi). Kontrol koşusu ana sonucun *yerine* değil, *yanına* konur |

## Sonuç — kabul edilen bedel

- Ana kıyasta Taban B **off-policy** veriyle eğitiliyor; bu sapma **bizim lehimize**dir ve
  Limitations'a **açıkça** yazılır — kontrol koşusuyla birlikte.
- Toplam ek bedel ~**$0.65**, Sprint 2 bütçesi içinde ihmal edilebilir.
- Hasat maliyeti **$0** (yerel çıkarım), ama **süre** gerektirir; `sprint2.md` CP2'de boyutlandırılır.
