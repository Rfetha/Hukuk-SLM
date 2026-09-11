# ADR-0080 — Ürün yoluna **iki geçişli zorunlu düşünce kapatması** eklendi: ürün yolu ile ölçüm hattı aynı rejime geldi

**Tarih:** 2026-09-11
**Statü:** yürürlükte
**Karar:** **insan** (2026-09-11) — bu bir **REJİM DEĞİŞİKLİĞİDİR** ve bu yüzden model tarafından
uygulanmadan önce **DUR-ve-SOR kapısından** geçirilmiştir. Kapının metni (plan Görev 22 Adım 3):
*"Ürün yolu, ölçüm hattının iki geçişli zorunlu düşünce kapatmasına gelir. Yayımlanan 0,8011
ölçüm hattının sayısıdır ve DEĞİŞMEZ — değişen ürün yoludur."* Karar verilmeden **kod yazılmadı**.
**Bağlı:** [ADR-0040](0040-dusunce-modu-olculecek-on-kayitli-kural.md) (kesiklik **%5** geçerlilik
ön şartı) · [ADR-0043](0043-dusunce-modu-acik-butceli-kapatma.md) (düşünce modu açık, **bütçeli
zorunlu kapatma**) · [ADR-0070](0070-uretim-butcesi-esitlendi.md) (üretim bütçesi tek formül,
**1024 + 512 = 1536**) · [ADR-0065](0065-bolunmus-surumleme.md) (bölünmüş sürümleme: ürün sürümü
ile iddia sürümü ayrıdır) · [ADR-0077](0077-v1-0-verilmedi-v0-3.md) (`v0.3`; ürün yolunun boş
cevap kusuru `MODEL_CARD` §7.9'da kayıtlıydı) · [ADR-0078](0078-konteyner-dagitimi-rejim-kilidi.md)
(rejimi **zorlayan** artefakt fikri)
**Kaynak ölçüm:** `outputs/eval/g22-rejim/` — [`KARSILASTIRMA.md`](../../outputs/eval/g22-rejim/KARSILASTIRMA.md) ·
`aracsiz_yol_80_zorunlu_kapatma.json` (ham) · `KUNYE.json` (rejim + çıpa).
Çıpa: `outputs/eval/g18-arac-katmani/aracsiz_yol_80.json`.
**Kayıt:** [#66](../record/research_log/2026-09-11-urun-yuzeyi-ve-aygit-kusurlari.md) §9

---

## Bağlam — ürün yolu, ADR-0040'ın kendi geçerlilik kapısını GEÇEMİYORDU

80 DEV kaleminde (`data/eval/dev/core_hard.jsonl`) `hakhukuk.servis.answer()` ile ölçüldü
(kaynak: `outputs/eval/g18-arac-katmani/aracsiz_yol_80.json`, 2026-09-09):

| | ürün yolu | ölçüm hattı |
| :--- | ---: | ---: |
| kesik veya boş cevap | **7/80 (%8,75)** | 4/80 (%5,0) |
| **tamamen boş metin** | **4/80** (id 7 · 64 · 65 · 66) | 0/80 |

ADR-0040'ın geçerlilik ön şartı *"cevapların **%5'inden fazlası** `</think>`'i kapatamadan
kesilirse koşu geçersizdir"* der. Ölçüm hattı tam eşikte geçiyor, **ürün yolu geçemiyordu**.

**Sınıf: sonlanmama, kesilme DEĞİL.** Yedi kesik kalemin yedisi de ölçüm hattında `finish=stop`
ile tamamlanmıştır (485-892 belirteç) ⇒ sebep soruların zorluğu değildir. Aynı sınıf araştırma
kaydı [#42](../record/research_log/2026-07-29-cp0-dusunce-modu-sonlanmama.md)'de ölçülmüştür:
bütçeyi **8× artırmak hiçbir şeyi değiştirmemiştir**. Bütçe eklemek bu kusuru kapatmaz.

## Elenen seçenekler — ikisi de insana sunuldu

**(1) *"Şimdi karar verme."*** Reddedildi: kusurun **çıpası elde** (`aracsiz_yol_80.json`),
mekanizma ölçüm hattında **zaten yazılı**, beklemenin karşılığı yok.

**(2) *"Ekleme — ürün yolu kesikliği gizlemiyor."*** Bu, `servis.py` docstring'inde **yazılı
duran** gerekçeydi ve ölçümle **yetersiz** çıktı: kesikliği görünür kılıyordu, ama
**sonlanmamayı karşılamıyordu**. Vatandaşa `Durum.KESIK` damgalı **boş bir metin** teslim
etmek, kusuru damgalamaktır — gidermek değil. ⇒ Gerekçe silinmedi; **neyin değiştiği** ve
insan kararının tarihi docstring'e yazıldı (bu hattın kuralı: çelişki damgalanır, sessizce
üzerine yazılmaz).

## Karar

**Ürün yolu (`hakhukuk.servis`) ölçüm hattının iki geçişli zorunlu düşünce kapatmasına gelir.**
`answer()` ve `answer_arac()` tek bir `_uret()` dikişinden geçtiği için ayrı bir kod yolu
**eklenmedi**.

### Mekanizma — koddan OKUNDU, hatırlanmadı

Kaynak: `scripts/olcum_uretim/gen_eval_grounded.py` → `generate_http()` · `render_prompt()`.

1. **1. geçiş:** `/v1/chat/completions`, `max_tokens = DUSUNCE_BUTCESI + CEVAP_BUTCESI`
   = **1024 + 512 = 1536** (ADR-0043 · ADR-0070), `temperature = 0,0`, `seed = 3407`.
2. **Ayrım noktası:** içerik (`content`) **BOŞ** ve `reasoning_content` **DOLU** ise — ve
   yalnız o zaman — 2. geçiş yapılır. Normal kalemde **fazladan istek yoktur**.
3. **2. geçiş — zorunlu kapatma:** sohbet API'si mesaj ortasından devam ettiremediği için ham
   istem sunucunun **kök** `/apply-template` ucundan alınır (`/v1` son eki **atılır**), istem
   `ham_şablon + düşünce_izi + "\n</think>\n\n"` olarak kurulur ve `/v1/completions`'a
   `max_tokens = 512`, `stop = ["<|im_end|>"]` ile gider. Model `</think>`'in **ötesinde**
   başlatıldığı için cevabı yazmak zorunda kalır.
4. **Künye:** dönen `finish_reason` **2. geçişinkidir** ⇒ 2. geçiş de bütçeye dayanırsa kalem
   yine `Durum.KESIK` damgalanır; kesiklik **gizlenmez**.

## Ölçülen sonuç (80 DEV kalemi, q8_0 KV, seed 3407, $0, 1.061 s)

Kaynak: `outputs/eval/g22-rejim/KARSILASTIRMA.md`. Üç `verify:` şartı bağımsız olarak
**yeniden hesaplanarak** doğrulandı.

| eksen | öncesi (çıpa) | sonrası | hüküm |
| :--- | ---: | ---: | :--- |
| **tamamen boş metin** | 4/80 (id 7·64·65·66) | **0/80** | **GEÇTİ** |
| kesik (`Durum.KESIK`) | 7/80 (**%8,75**) | **3/80 (%3,75)** | **ADR-0040 kapısı GEÇTİ** (≤4/80) |
| `sha256` olarak değişen cevap | — | **4/80** — tam da bozuk olan dördü; **76 kalem birebir aynı** | değişiklik **CERRAHİ** |
| getirilen kaynak kümesi değişen kalem | — | **0/80** (retriever'a dokunulmadı) | muhafız tuttu |
| doğrulanamayan atıf | 10 | 10 | kıpırdamadı |

**Suskunluk kümesi — fark GİZLENMEDİ.** `[10, 34, 63]` → `[7, 10, 34, 63, 64]`:
**giren 2** (id **7** · **64** — ikisi de eskiden **tamamen boş** dönen kalemlerdi, artık açıkça
*"verilen kaynaklarda bu konuyu düzenleyen madde bulunmuyor"* diyorlar), **çıkan 0**.
Diğer iki bozuk kalem (id **65** · **66**) tam **CEVAP**'a döndü. ⇒ Dört kusurlu kalemin
**ikisi cevaba, ikisi açık çekinmeye** gitti.

## Ne KURULMAZ

- **Bu karar yayımlanan `0,8011`'i DEĞİŞTİRMEZ.** O sayı **ölçüm hattının** sayısıdır
  (`outputs/eval/f02-biz-onsozsuz/`); değişen **ürün yoludur**. Bölünmüş sürümleme
  (ADR-0065) tam olarak bu ayrım içindir.
- Bu karar *"model iyileşti"* **demez**. Ağırlıklara dokunulmadı. Dediği şey dardır:
  **ürün yolu artık boş cevap teslim etmiyor.**
- **Kütle bu koşuda ÖLÇÜLMEDİ** — hakem ister, bu işin bütçesi $0'dı. Kütlenin ne kadar
  oynayacağına dair bir cümle kurulmuyor.

## Kabul edilen bedeller — ikisi de *"gelecek işi"* diye geçiştirilmez

**(a) B10'a +2 kalemlik yük.** Kesik sayacı 7 → 3'e düşerken **aşırı-red** ekseni iki kalem
ağırlaştı (id 7 · 64 artık suskun). Bu tur bunu **ölçmedi**, yalnız kaydetti; B10 eşiği ayrı
bir turun işidir. Kesikliği kütleden düşürmenin karşılığı, çekinme eksenine yazılan borçtur.

**(b) Açık kusur 20 — 2. geçiş `reasoning_content` alanına BAĞIMLIDIR.** `llama-server`'ın
`--reasoning-format` varsayılanı değişir ve düşünce izi ayrı alanda dönmezse, ayrım noktasındaki
*"içerik boş **ve** iz dolu"* koşulu hiç tutmaz: mekanizma **sessizce tek geçişe düşer** ve boş
cevap kusuru **geri gelir**. Koşuda doğrulandı, ama **testle çivilenemiyor** — bağımlılık
sunucunun davranışındadır, kodun değil. Bu, bu hattın en pahalı sınıfından (*"hata vermeden
yanlış"*) bir bağımlılıktır ve kusur olarak **açık kalır**.
