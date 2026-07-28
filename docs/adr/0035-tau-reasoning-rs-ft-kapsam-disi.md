# ADR-0035 — `τ_reasoning` / RS-FT kapsam dışı · ADR-0030 madde 2 yürürlükte kalır

**Statü:** Yürürlükte · **Tarih:** 2026-07-28
**Otorite belge:** `TASARIM.md` §1.2 (iç iddia) · §10.2 (plandan çıkanlar)
**İlgili:** **ADR-0030 madde 2 (düşünce modu KAPALI) — geri ALINMADI, teyit edildi** ·
ADR-0028 (tek boyut noktası — aynı daraltma disiplini) · ADR-0027 (kol tanımı) ·
ADR-0010 (uzman register, hedef kitle avukat)
**Kanıt:** `data/train/raft_scrubbed/train.jsonl` biçim sayımı (n=17.323, 2026-07-28) ·
`data/README.md:91` · `TASARIM.md` §5 (harness 1-2 hop) · §10.2 mevcut "CoT / gerekçe kolu" satırı
**Açık soru:** [`docs/open_questions.md`](../open_questions.md) **#11 → ✅ KAPANDI**

---

## Bağlam

`docs/ft-is-akisi.mmd` (kullanıcı taslağı, 2026-07-28) üçüncü bir kol öneriyordu:
**`τ_reasoning`**, rejection-sampling FT (RS-FT) döngüsüyle üretilecek. Bedeli küçük değildi:
kol 2→3, kafes 3→7 hücre, araya **FAZ 0 kapıları** (M6 seti + deterministik zincir-verifier +
`pass@16` tanısı + Kapı R), ve **ADR-0030 madde 2'nin geri alınması** (düşünce modu KAPALI).

Karar öncesi ürün sorusu soruldu — *"modelin işi kaynağı aktarmak mı, sonuç çıkarmak mı?"*
Kullanıcının cevabı: **hibrit — "kaynak şu şu, benim sonucum bu bu"**, yani kaynakları refere
ederek sonuç çıkarmak.

## Bulgu — istenen davranış ZATEN eğitiliyor

`raft_scrubbed`'ın biçimi sayıldı (n=17.323):

| ölçüt | oran |
| :--- | ---: |
| `user`'da `KAYNAK` bloğu | **%97.0** |
| cevapta `##begin_quote##` birebir alıntı | **%77.1** |
| cevap `1)` numaralı çıkarım adımıyla başlıyor | **%76.0** |

Cevapların kanonik şekli:

```
1) İlgili kaynak KAYNAK 4'tür, çünkü diğerleri … bu nedenle onları eledim.   ← ÇIKARIM
2) ##begin_quote## "Mahkemece evliliğin iptal … sona erer." ##end_quote##     ← ALINTI
3) Sonuç olarak, … (TÜRK MEDENİ KANUNU, Madde 271).                          ← SONUÇ + ATIF
```

Bu, kullanıcının tarif ettiği hibridin **birebir kendisi**. Yani `τ_grounding` (CP5'te koşan iş)
"kaynağı refere ederek sonuç çıkarma"yı zaten öğretiyor; ayrı bir reasoning kolu bu biçim için
gerekli değil.

`τ_grounding`'in öğretmediği tek şey **maddeler arası zincir** (*"m.347 → m.350 istisnası →
senin durumun"*). **Ama o zincir ağırlığın değil, getirmenin işi:** `TASARIM.md` §5 harness'ı
zaten *"hibrit retriever — BM25 + embedding + **1-2 hop**"* ve *"graf parser — hiyerarşi +
**atıf ağı**"* olarak tanımlıyor. Graf iki maddeyi birden önüne koyduğunda, model zaten bildiği
tek-kaynak çıkarımını iki kaynağa uygular. Zinciri ağırlığa gömmek, harness'ın tasarlanmış işini
tekrar etmek olur.

## Karar

**`τ_reasoning` / RS-FT tez kapsamına GİRMEZ.** Kollar **2** (`τ_grounding` · `τ_abstention`),
kafes **3 hücre**, FT bütçesi **5 koşu** — Kapı 0'ın (#39) bıraktığı hâl korunur.

**ADR-0030 madde 2 (düşünce modu KAPALI) yürürlükte kalır.** Geri alma gerekçesi ortadan kalktı:
RS-FT olmayınca düşünce izi üretme ihtiyacı da yok, dolayısıyla ADR-0030'un ölçülmüş iki sorunu
(varsayılan modda `content` **boş** dönüyor · SFT verisi akıl yürütme izi taşımıyor →
eğitim-eval hizalaması) hiç açılmıyor.

**Bu yeni bir karar değil, teyit:** `TASARIM.md` §10.2 zaten *"CoT / gerekçe kolu"*nu plandan
çıkarmıştı (veri yok · CANON'da ölçüm modu yok · tümüyle hakem-bağımlı olurdu → "hakemsiz omurga"
savunmasını zayıflatır). Bu ADR o kararı **yeni kanıtla** genişletir ve RS-FT varyantını da kapsar.

## Değerlendirilen alternatifler

| eleme | gerekçe |
| :--- | :--- |
| **A — "üçüncü ÇATIŞAN beceri"** (reasoning ↔ abstention gerilimi: biri "kaynaktan türet" der, öteki "yazmayanı söyleme") | Teorik olarak sağlam ve iç iddiayı güçlendirirdi. **Ama çatışmanın kendisi ölçülmedi** — elde hikâye var, kanıt yok. Bu hatta mantıklı hikâyelerin ölçülünce çürüdüğü iki vaka var (`#40` `fla` teşhisi, `#38` şablon). Kanıtsız bir çatışma varsayımı üzerine sprint kurulmaz |
| **B — "ürünü iyileştiren ek yetenek"** | İç iddiaya hiçbir şey katmaz; kafesi 7 hücreye çıkarır ama 4 hücre hipotezi test etmez. Ürün iyileştirmesi `TASARIM.md` §10.1'e göre "inşa edilebilir ama ölçülmez" kutusunda |
| **Yalnız `pass@16` tanısını koşmak** (RS-FT yapmadan) | *"Bu base zor hukuk sorularında akıl yürütebiliyor mu"* sorusu başlı başına bir bulgu olurdu. **Ertelendi, reddedilmedi** — tez sonrası, ucuz bir çıkarım koşusu. Şimdi koşmak Sprint 2'yi cevabı kullanılmayacak bir ölçümle geciktirir |

## Sonuç — kabul edilen bedel

**Limitations'a yazılacak:** *"Çok adımlı hukuki akıl yürütme **model düzeyinde eğitilmedi**;
maddeler arası zincirleme harness'a (graf + 1-2 hop getirme) bırakıldı. İkisinin katkısı **ayrı
ayrı ölçülmedi** — yani 'model mi akıl yürüttü, graf mı doğru maddeleri önüne koydu' sorusu
bu çalışmada cevaplanmıyor."*

⚠️ Bu, Kapı 2'nin (`D` vs `E`, iş bölümü) cevaplayacağı sorunun **komşusu ama aynısı değil**:
Kapı 2 harness'ın toplam katkısını ölçer, akıl yürütmenin nereden geldiğini ayrıştırmaz.

**Future work:** RS-FT kolu + `pass@16` tanısı, aynı reçeteyle, tez sonrası — ADR-0028'in ikinci
boyut noktası için söylediğinin aynısı.
