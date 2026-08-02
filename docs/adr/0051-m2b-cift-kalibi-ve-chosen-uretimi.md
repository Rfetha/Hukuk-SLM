# ADR-0051 — `τ_a`'nın M2b çiftleri: kalıp **eval aynası**, `chosen` **şablon** (dış model kullanılmaz)

**Statü:** Yürürlükte · **Tarih:** 2026-08-02
**Otorite belge:** `sprint2.md` CP3 · **TAMAMLAR:** [ADR-0045](0045-ara-kapi-merge-onarim-kontrolu.md) **m.4**
(iki tipin birden hasat edilmesine karar vermişti; *çifte nasıl dönüşeceğini* söylememişti)
**İlgili:** [ADR-0042](0042-rejected-havuzu-tek-kaynak-ve-on-policy-kontrol.md) (on-policy `rejected`) ·
[ADR-0043](0043-dusunce-modu-acik-butceli-kapatma.md) (rejim değişmezleri) ·
[ADR-0011](gemma4-12b-dersler.md#adr-0011) (eval aynası) · ADR-0031 (modül listesi)
**Kanıt:** `research_log` [#48 §7](../record/research_log/2026-08-02-cp2c-modal-koprusu.md) ·
**değişen kod:** `scripts/build_orpo_v3.py` (`m2b_chosen`, `cp2c_cifti`)
**Karar sahibi:** insan (2026-08-02, hasat sürerken; seçenekler ve bedelleriyle sunuldu)

---

## Bağlam — hasadın yarısı çifte dönüşemiyordu

CP2-c iki tip negatif topluyor: **m2** (tuzak madde verilmiş, ORACLE kalıbı) ve **m2b** (doğru
kaynak hiç yok, 4 çeldirici, RAG_MULTI kalıbı). m2b'nin toplanma gerekçesi ADR-0045 m.4'te
kayıtlı ve güçlü: `τ_g`'nin **gerçek açığı** orada (M2b Rej **0.986 → 0.607**), ve **ARA KAPI'nın
ikinci gözlemi** (merge M2b ≥ 0.854) o eksende okunuyor.

Hasat koşarken çift kurucu önden denetlendi (tuzak 6.2 ilkesi) ve üç uyumsuzluk çıktı:

| # | ne | sınıf |
| :-- | :--- | :--- |
| 1 | Alan adları: CP2-c `rejected`/`context_shown` yazıyor, betik `model_answer`/`trap_text` okuyor | mekanik, çöker |
| 2 | Betik sistem istemini ve `KAYNAK MADDE:` kalıbını **sabit** kuruyor; m2b'nin kalıbı RAG_MULTI + `KAYNAKLAR:` | 🔇 **sessiz** |
| 3 | m2b için `chosen` metni **hiç yok** | 🔴 tasarımsal |

(3)'ün kanıtı — `τ_a`'nın mevcut eğitim seti sayıldı: **1.449 çekinme çiftinin tamamı M2 kalıbı**.
RAG_MULTI kalıbı yalnız `is_pref=0` grounding-replay'de var, yani çekinmeyi hiç öğretmiyor.
**`τ_a` bugüne dek kendi asıl hedefi olan kalıpta tek bir çekinme çifti görmemiş.** Eldeki
`chosen` metinleri de oracle biçimli (*"Sağlanan {tuzak madde} … bu maddede yer almamaktadır"*) —
m2b'de "sağlanan madde" diye tek bir şey olmadığı için **takılamaz**.

## Karar

### m.1 — m2b çiftinin kalıbı **eval aynasıdır**, seçim değil

m2b çifti `SYSTEM_PROMPT_RAG_MULTI` + `KAYNAKLAR:\n{context_shown}\n\nSORU: …` ile kurulur;
`context_shown` hasadın **sakladığı** bloktur, yeniden üretilmez. Gerekçe ADR-0011'in eval-ayna
değişmezi: eğitim istemi ilgili modun eval istemiyle **birebir** olmalı. Hasat bu bloğu tam bu
sebeple saklıyor (`cp2_harvest.py` satır 195-197). Bu bir tercih değil, mevcut kuralın
uygulanmasıdır — (1) ve (2) birlikte düzeltildi.

### m.2 — m2b `chosen`'ı **şablonla** üretilir, dış modelle DEĞİL

Şablon, yuvalarını kalemin **kendi** kaynak başlıklarından doldurur:

```
Verilen kaynaklarda bu konuyu düzenleyen madde bulunmuyor. Sağlanan kaynaklar
({KANUN} Madde {n1}, {n2}, …) başka hususları düzenlemektedir; doğru bir atıf
yapabilmek için ilgili hükmün ayrıca temini gerekir.
```

**Gerekçe — hedef davranış istemde zaten yazılı.** `SYSTEM_PROMPT_RAG_MULTI` şunu söylüyor:
*"İlgili kaynak YOKSA cevap uydurma; 'Verilen kaynaklarda bu konuyu düzenleyen madde bulunmuyor'
de."* `chosen`'ın işi bu talimatı **örneklemek**. Bir dış modele yazdırmak yeni bilgi üretmez,
sadece o modelin üslubunu çifte sokar — üstelik `rejected` tarafı **kendi hasadımız** (ADR-0042,
on-policy) olduğu için çift **iki farklı modelin karışımı** hâline gelir. Bedeli (~$0,4) küçük,
ama karşılığı yok ve kirlilik gerçek.

**Ölçülen:** 45 gerçek m2b kaleminde **45/45 tekil** `chosen` metni — tek bir sabit dize oluşmuyor.

### m.3 — Kalıp öğrenme riski **kabul edilir ve zaten ölçülüyor**

Karşı-argüman: kol muhakeme yerine **üslup** öğrenebilir ve M2b metriği üslupla şişebilir.
Bu risk kabul edilmiştir çünkü ARA KAPI'nın **M1 A1 ≥ 0.880 muhafızı** tam bunu ölçer — kol
ayrım gözetmeden çekinmeye başlarsa muhafız düşer. Ayrıca geçerlilik, cevabı **görmeyen** kör
`valid_trap` damgasına bağlıdır (ADR-0048), yani `chosen`'ın üslubu paydayı kaydıramaz.

**Geri dönüş koşulu — ön-kayıtlı:** `τ_a` M2b'de yükselirken **M1 A1 muhafızı düşerse**, teşhis
"kalıp öğrenildi" olur; o durumda `chosen` dış hakemle üretilip (~$0,4) kol yeniden eğitilir
(~$3,2) ve **her iki sonuç da raporlanır**.

## Elenen seçenekler

| | seçenek | niçin elendi |
| :-: | :--- | :--- |
| **B** | `chosen`'ı gpt-4o-mini'ye yazdır (~$0,4) | Yeni bilgi üretmiyor — hedef cümle istemde zaten yazılı. `rejected` on-policy iken `chosen`'ı dış modele yazdırmak çifti iki modelin karışımı yapar. m.3'ün geri dönüş yolu olarak **saklandı** |
| **C** | m2b'yi çiftlerin dışında bırak, `τ_a` yalnız M2'de eğitilsin | Hasadın yarısı çöpe gider **ve** ARA KAPI, `τ_a`'nın hiç hazırlanmadığı bir ekseni ölçer — ADR-0045 m.4'ün gerekçesini iptal eder |

## Sonuçları

- `τ_a` ilk kez kendi asıl hedefi olan kalıpta eğitilir; ARA KAPI'nın ikinci gözlemi **anlamlı** hâle gelir.
- `build_orpo_v3.py` iki şemayı da okur; emekli `gen_v3` yolu **birebir korundu** (regresyon
  doğrulandı: 1495/299/1794, kayıtlı `orpo_report.json` ile özdeş).
- Karışım künyeye yazılır (`abstain_mod_karisimi`, `hasat_kaynak_karisimi`) — ADR-0045 m.4'ün şartı.
- **Limitations'a girer:** m2b'nin `chosen` tarafı insan yazımı bir şablondur, model üretimi değil;
  bu, M2b sonucunun bir bölümünün **biçim öğrenmesi** olabileceği ihtimalini açık bırakır.
  Muhafız metriği ve kör payda bu ihtimali sınırlar ama **sıfırlamaz**.

## 🐞 Uygulamada yakalanan sessiz kusur (aynı gün)

Şablonun kaynak başlığı ayrıştırıcısı büyük/küçük harfe duyarlıydı; külliyatta **hem** `Madde 75`
**hem** `MADDE 64` yazımı var. 45 kalemin **15'i** sessizce kısa yedek metne düşüyordu — hata yok,
yalnız zayıflamış hedef. `re.IGNORECASE` ile düzeltildi → **0/45**. Ders: şablon çıktısı
**gözle okunmadan** kabul edilmez.
