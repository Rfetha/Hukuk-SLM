# ADR-0075 — `v1` **SFT ile kapanır**; `v2` = `tgta_v1` üstüne **sequential RL**

**Tarih:** 2026-09-08
**Statü:** ✅ yürürlükte
**Karar:** insan
**Bağlı:** [ADR-0027](0027-tasarim-kilitleri-paralel-kol-merge.md) (task-vector merge) ·
[ADR-0010](gemma4-12b-dersler.md#adr-0010) (düz SFT çekinmeyi yok etti) ·
[ADR-0065](0065-bolunmus-surumleme.md) (bölünmüş sürümleme) ·
[ADR-0071](0071-v1-release-artefakti-tek-gguf.md) (tek GGUF) ·
[ADR-0062](0062-b10-turu-kapatildi-hedef-egitimsiz-karsilandi.md) (B10: eğitim gerekmedi)

## Bağlam

Planın Faz 4'ü iki eğitim turu öngörüyordu: **G14** (`B1` isabetsizlik, ~$5) ve
**G15** (`B4` — `τ_a` genliği, ~$1,3). İkisi de `v1.0` kapısından **önce** koşacaktı.

Aynı anda üç şey ölçülmüştü:

| olgu | sayı | kaynak |
| :--- | :--- | :--- |
| `B1` isabetsizlik — **rakiplerden geride değiliz** | biz **8/80** ↔ 8 · 7 · 8 | [#63](../record/research_log/2026-09-07-skor-karti-bosluklari.md) |
| `B1` için **otomatik vekil metrik YOK** | süzgeçler 4 ve 3 buluyor, **göz 8** | ADR-0066 |
| `B4` — `τ_a` merge'de seyreliyor | **0,987 → 0,766** (−22,1 p) · `‖τ‖` oranı **8,87×** | [#57](../record/research_log/2026-08-06-cekinme-aleti-onarimi.md) |

Ve bu hattın **iki turu** *"daha fazla eğitim"* varsayımıyla başlayıp eğitimsiz kapanmıştı:
**B10** (hedef eğitimsiz karşılandı — ADR-0062) ve **Faz 0** (kütle %68,4 → **%80,1**,
ağırlıklar **hiç değişmeden**).

## Karar

### 1. `G14` ve `G15` **koşulmaz.** `v1`, bugünkü SFT artefaktıyla kapanır.

`v1` = **ham base + SFT hattı** (`τ_g` SFT · `τ_a` ORPO · ham TIES merge = `tgta_v1`).
Kapı koşusu bu artefaktla koşulur, yayın bu artefaktla yapılır.

**Gerekçe, sırayla:**
- **G14 zayıf bahis:** hedeflenen eksende rakiplerden **geride değiliz** (8/80 ↔ 8·8·7·8) ve
  ilerlemeyi ölçmek her turda **80 kalem gözle okuma** ister — bedeli para değil, **insan
  saati**. B10 turunun dersi doğrudan bu sınıftan.
- **G15'in hedefi `v2`'de KONUSUZ kalıyor:** B4 bir **merge** kaybıdır, eğitim kalitesi
  sorunu değil (`τ_a` tek başına 0,987). Sequential mimaride merge yoktur ⇒ aynı 22,1 puan
  ödenmeden geri gelir. G15'i koşmak, birkaç hafta sonra terk edilecek bir mimariyi onarmak
  olurdu.

### 2. `v2` = `tgta_v1` **yeni başlangıç noktası** + **GRPO / thinking RL**

```
v1   ham base ──► SFT (τ_g) + ORPO (τ_a) ──► ham TIES ──► tgta_v1 ──► YAYIN
v2   tgta_v1 (bf16, models/merged/tgta_v1/, 8,8 GB) ──► GRPO + düşünce ayarı ──► v2.0
```

**Neden RL, neden şimdi mümkün:** bu hatta **doğrulanabilir ödül** hazır —
`hakhukuk/terazi.py` atıf doğrulamasını **deterministik** yapıyor (atıf getirilen kaynakta
var mı: evet/hayır). Reward model eğitmeye gerek yok, LLM-hakem bedeli yok. Uydurulmuş madde
**ölçülebilir bir negatif sinyaldir** ve bugünkü değeri **0/114** ↔ rakipler 1 · 4 · 4.

### 3. 🚨 `ADR-0027`'nin task-vector hattı `v1`'de **DONDURULUR** — sessizce değil, burada

`τ = θ_ft − θ_base` tanımı **tüm kolların aynı `θ_base`'i paylaşmasını** şart koşar.
`tgta_v1`'i yeni başlangıç almak bu tanımı bozar: sonraki tur **task vector değil, sequential
post-training** üretir. ⛔ Bu bir kural ihlali **değil**, bilinçli bir mimari geçiştir —
ama ADR-0027 hâlâ yürürlükteymiş gibi okunamaz.

**Sonuç:** merge iddiası `v1`'de **ölçülmüş hâliyle kapanır** (ham TIES ↔ norm-dengeli
ablasyonu, ADR-0052) ve `v2`'ye **taşınmaz**. `v2`'nin iddiası merge değil, **RL kazancıdır**.

### 4. Ödül fonksiyonu **çekinmeyi korumak zorundadır** — pazarlık konusu değil

ADR-0010 ölçtü: düz SFT abstention'ı **yok etti**. RL'de risk daha keskindir çünkü model
ödülü maksimize etmeyi öğrenir: *"cevap ver"* yönünde ödüllendirilen model **susmayı bırakır**.

⇒ `v2`'nin ödülü **en az dört terim** taşır ve son ikisi düşürülemez:

```
r = doğrulanmış_atıf_oranı  −  uydurulmuş_madde_cezası
  + doğru_susma_ödülü       −  aşırı_red_cezası
```

⛔ **Ön-kayıt şartı:** `v2` turu başlamadan önce ödül fonksiyonu, hedef bant ve **durma
kuralı** bir ADR'ye yazılır (ADR-0050). Bugünkü çıpalar korunacak taban olarak alınır:
uydurulmuş madde **0/114** · aşırı-red **4/80** · kütle **0,8011**.

## Reddedilenler

| seçenek | neden reddedildi |
| :--- | :--- |
| **G14'ü koşmak** | Hedef eksende geride değiliz; otomatik metrik yok ⇒ her tur insan-saati. B10 aynı sınıftan bir turdu ve eğitimsiz kapandı |
| **G15'i koşmak** | Onaracağı şey (`merge` kaybı) `v2`'de **konusuz** kalıyor ⇒ terk edilecek mimariyi onarmak |
| **`v1`'i RL'den sonra yayımlamak** | Çalışan bir ürünü, sonucu belirsiz bir tur için **aylarca** bekletmek olurdu; ADR-0065 tam bunu önlemek için bölünmüş sürümlemeyi kurdu |
| **`v2`'de PPO** | Reward model + kritik ağ; 4B ölçeğinde maliyet/karmaşıklık faydayı aşıyor. Doğrulanabilir ödül varken reward model eğitmek gereksiz |
| **`v2`'de DPO** | Referans model ister (bellek 2×). Mevcut ORPO zaten referanssız çalışıyor; DPO'nun net üstünlüğü ölçülmedi |

## Ne KURULMAZ

- ⛔ *"RL daha iyi sonuç verir"* — **ölçülmedi, bir hipotezdir.** Bu hattın tahmin sicili
  bunu gerektiriyor: *"istem katmanı tavanı düşük"* · *"harness A1'i kapatır"* · *"norm
  dengeleme şart"* · *"B10 eğitim ister"* — **dördü de çürüdü**.
- ⛔ *"G14/G15 değersizdi"* — **koşulmadılar**, dolayısıyla ne verecekleri **bilinmiyor**.
  Karar bir öncelik kararıdır, bir ölçüm sonucu değil. İkisi de borç olarak açık kalır.
