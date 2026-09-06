# ADR-0065 — Bölünmüş sürümleme: ürün sürümü ↔ iddia sürümü

**Tarih:** 2026-09-06 · **Statü:** ✅ yürürlükte · **Karar:** insan (açık soru **S1**)

## Bağlam

**ARA KAPI düştü** (2026-08-06): merge M2b **0,766** ↔ eşik **0,8649** → **9,9 puan altında**
([ADR-0045](0045-ara-kapi-merge-onarim-kontrolu.md) · [#58](../record/research_log/2026-08-06-payda-tekillesmesi.md)).
Bu kapı CP4-CP5 harcamasını yetkilendiren kapıydı; **o yetki yok**. Soru şuydu: kapı düşmüşken
ürüne `v1.0` adı verilebilir mi?

## Karar: sürüm İKİYE ayrılır

```
ÜRÜN sürümü    v0.2 → v1.0    "çalışıyor, indirilebilir, yayımlanan sayı yeniden üretilebilir"
İDDİA sürümü   ARA KAPI'ya bağlı kalır — CP4-CP5 yetkisi geri gelmeden ilerlemez
```

**Gerekçe:** ARA KAPI bir **iddia** kapısıydı — merge'ün `τ_a`'yı ne kadar taşıdığını ölçüyordu.
Ürün olgunluğunu ölçmüyordu ve ölçmek için tasarlanmamıştı. İkisini tek sayıya bağlamak, ürünü
yayımlamayı ölçmediği bir kapıya rehin verir. Ayırmak ise **her iki tarafı da dürüst tutar**:
ürün kendi kapısından (ADR-0064) geçer, iddia kendi kapısından.

**Ne değişmiyor:** ARA KAPI'nın düştüğü **her iki belgede de damgalı durur**. Gevşetilmiyor,
yeniden tanımlanmıyor, "yeni ölçütle açıldı" denmiyor. Düşmüş kapı düşmüş kalır.

## Sonuçları
- `v0.2` = Hat A biter bitmez yayımlanabilir (paketleme, $0): ağırlık + retriever + indeks +
  dağıtılan istem + CLI + basit TUI.
- `v1.0` = ADR-0064'ün üç maddeli kapısı geçilince verilir.
- CP4-CP5 ve Kapı 5 / parite matrisi **iddia sürümünde** kalır; arxiv metodoloji paper'ı
  (S11 kararı) bu iddiaya **dayanmaz**, dolayısıyla ondan bağımsız ilerler.

## Reddedilenler
- **`v1.0` ver, ARA KAPI'yı yeni ölçütle yeniden tanımla** — REDDEDİLDİ: eşiği geçemeyince
  eşiği değiştirmek ADR-0050'nin yasakladığı hareketin ta kendisidir.
- **CP4-CP5 koşulana dek `v0.x`'te kal** — REDDEDİLDİ: ~$19 ve **yetkisi yok**; ürünü
  süresiz olarak ölçmediği bir kapıya rehin verir.
