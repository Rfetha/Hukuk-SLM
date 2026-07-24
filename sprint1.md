# Sprint 1 — hazırlık ve ilk fine-tune

> **Otorite:** [`TASARIM.md`](TASARIM.md) · **kararlar:** ADR-0027, ADR-0028 · **tam iş listesi:** [`TODO.md`](TODO.md)
> **Bu belge neden var:** `TODO.md` tüm tezin haritası (7 bölüm, 40+ madde). Sprint 1 onun ilk
> dilimini **yürütülebilir** hâle getirir: sıra, kapı, komut, ve *"burada ne patlar."*
>
> **Kaynak:** sıralama ve uyarılar **Gemma 4 12B hattının 5 turundan** çıkarıldı
> ([kronoloji](docs/record/gemma4-12b-kronoloji.md) · [dersler](docs/adr/gemma4-12b-dersler.md)).
> ⚠️ Buradaki 12B sayıları **kalibrasyon çıpası**, hedef değil.

---

## İki faz — A ve B

| | faz | soru | biterken elde ne var |
| :-- | :--- | :--- | :--- |
| **A** | **HAZIRLIK** | *Model fine-tune edilebilir ve düzgün çalışır hâlde mi?* | doğrulanmış base · çalışan eğitim ortamı · çalışan eval hattı · base çıpaları · hazır veri |
| **B** | **İLK FINE-TUNE** | *`τ_grounding` ne satın aldı, neyi bozdu?* | eğitilmiş + ölçülmüş ilk task-vector · kayda geçmiş sonuç |

> **Faz A bitmeden Faz B başlamaz.** Bu bir tercih değil: 12B hattında Faz A'ya ait üç ayrı hata
> (şablon render'ı · turn işaretleri · veri şeması) **eğitim koşusunu sessizce çöpe çevirdi.**
> Hiçbiri hata vermedi — koşu tamamlandı, çıktı üretildi, sayı raporlandı, ve yanlıştı.

```
┌─ FAZ A — HAZIRLIK ────────────────┐   ┌─ FAZ B — İLK FT ──────────────┐
│ CP0 base kapısı    (GPU yok)      │   │ CP3 smoke      (~$0.15)       │
│ CP1 base baseline  (çıkarım)      │──►│ CP4 tam eğitim (asıl koşu)    │
│ CP2 veri hazırlığı (CPU)          │   │ CP5 ölçüm      (hakem)        │
└───────────────────────────────────┘   └───────────────────────────────┘
   6/6 yeşil + Kapı 0 kararı              sprint biter: 3 soru cevaplı
```

---

## Neden ilk FT `τ_grounding`?

Üç kol da **ham base'den bağımsız** eğitiliyor (TASARIM §4.1) → doğruluk açısından sıra serbest.
Yürütme açısından değil:

| kol | veri | bağımlılık | reçete |
| :--- | :--- | :--- | :--- |
| **`τ_grounding`** | ✅ hazır (`train/raft/`, 17.323) | **yok** | 12B'de kanıtlandı (v2b tüm kapıları geçti) |
| `τ_abstention` | ⚠️ `rejected` yeniden hasat gerekiyor | **çalışan çıkarım hattı** ister | ORPO, 12B'de kısmi |
| `τ_register` | ✅ hazır (`train/grounded_qa/`) | **Kapı 0'a bağlı** (gerekmeyebilir) | düz SFT |

`τ_grounding` **bağımsız + verisi hazır + reçetesi kanıtlı** → ilk koşu o. Ayrıca hattın kendisini
uçtan uca doğrular; sonraki iki kol aynı raydan geçer.

> 12B'de sıralama böyle çalıştı: grounding (v2b) **kabul edildi** · abstention'ı düz SFT'yle eklemek
> (v2c) **reddedildi** · tercih-optimizasyonuyla (v3) kısmen onarıldı.
> **Ders: grounding SFT'nin işi, abstention preference'ın işi.**

---

# FAZ A — HAZIRLIK

## CP0 — Base doğrulama kapısı 🔒

**TODO:** §0 (tamamı) · **GPU:** yok · **Çıkış:** 6/6 yeşil

| # | iş | doğrulama |
| :-- | :--- | :--- |
| 1 | Aday base'i indir | — |
| 2 | **llama.cpp mimari desteği** | model yükleniyor mu, `--list-devices` |
| 3 | GGUF üret | `bash scripts/setup_llamacpp.sh <repo> <etiket>` · **`PURE=0`** (QAT yok) |
| 4 | **Şablon render'ını GÖZLE oku** | `bash scripts/diag_chat_template.sh <gguf>` → `/apply-template` |
| 5 | **Model DURUYOR mu** | `bash scripts/smoke_llamacpp.sh <gguf>` → `finish_reason=stop` |
| 6 | **Turn işaretlerini çıkar** | 4. adımın render'ından `user_part` / `assistant_part` |
| 7 | Unsloth + sm_120 ortamı | `requirements.lock.txt` yeniden kur |
| 8 | Lisansı kaydet | attribution + limitations satırı |

> ### ⚠️ 12B'den — **buradaki iki madde bir CANON koşusunu sessizce çöpe çevirir**
>
> **Şablon (#38).** minja motoru şablonun bir dalını yanlış render etti; model **hiç durmadı**,
> girdiyi tekrarladı. Hiçbir aşamada hata yoktu — server açıldı, istek **200** döndü, JSON geldi.
> Sadece **içerik** bozuktu. Regex omurgası o çıktılar üzerinde **sayı üretir ve tablo dolar.**
> → Render'ı **gözle** oku. *"Bayrak çalışıyor mu"* ile *"bayrak yok sayılıyor mu"* farklı şeyler;
> sahte-işaret şablonuyla ayırt et.
>
> **Turn işaretleri.** Yanlış işaretle `train_on_responses_only` **hiçbir şeyi maskelemez**,
> loss tüm diziden akar, **eğitim sessizce bozulur.** `train_sft.py` render'a karşı assert ediyor —
> ama doğru değeri sen vermelisin. Assert'in gerçekten tetiklendiğini smoke'ta gör.
>
> **Kuantizasyon.** Quantize yarıda kesilirse dosya "var" görünür (bir GGUF 666 tensörün 4'ünde
> kesilmişti, 70 MB diskte duruyordu). Script artık <100 MB'da durur.

**⚠️ Bu sprintin en oynak kalemi 7. madde.** Blackwell/sm_120 wheel derdi bir günde de çözülebilir,
bir haftayı da yiyebilir. Takvim belirsizliği buradan geliyor. Modal'a kaçmak borcu **ertelemek**
demek — kapatmak değil.

## CP1 — Base baseline + Kapı 0

**TODO:** §2 "Kapı 0" · §1 (regex kalibrasyonunun ilk yarısı) · **GPU:** çıkarım, yerel

Yeni base'i **çıplak** olarak 6-mod CANON'da koş. Tek koşu, üç çıktı:

1. **Çıpalar** — `τ_grounding`'in yeneceği/koruyacağı sayılar (M1 · M3 · M4)
2. **Kapı 0 kararı** — register-proxy → `τ_register` kolu gerekli mi?
3. **Hattın doğrulaması** — eval yolu yeni base'de uçtan uca çalışıyor mu

```bash
python scripts/gen_eval_grounded.py --label bench_m1_base  --distractors 4 --max-chunk-chars 900 --n 40
python scripts/gen_eval_grounded.py --label bench_m4_base  --with-source --n 40
python scripts/gen_eval_grounded.py --label bench_m2_base  --data data/eval/canon/trap.jsonl --with-source --n 35
python scripts/gen_eval_grounded.py --label bench_m2b_base --distractors 4 --no-gold --n 40
python scripts/gen_eval_grounded.py --label bench_m3_base  --empty-context --n 40
python scripts/gen_eval_grounded.py --label bench_m5_base  --n 40          # kör
python scripts/rescore_answered.py ...                                      # A1 = cevaplanan-only
python scripts/score_register.py --details outputs/eval/bench_m1_base_detail.jsonl
```

**Kapı 0:** register-proxy yüksekse `τ_register` **düşer** → kol 3→2, kafes 7→3 hücre, **FT bütçesi
6'dan 5'e iner** (FT-3 düşer). Düşükse kol gerekçeli olur.

> ### ⚠️ 12B'den
>
> **Base'in over-refuse etmesini bekle — bug değil, ölçülecek davranış.** 12B base'de gold
> prompt'ta **VAR**ken **21/40 = %52,5** *"kaynaklarda bu konuyu düzenleyen madde bulunmuyor"* dedi
> (spot-check teyitli). M1 coverage **%47,5**. Ve base'in yüksek M2/M2b/M3 reddi bu körlüğün
> **yan ürünüydü** — "iyi kalibrasyon" değil "kör red".
> → **A1 mutlaka cevaplanan-only** (`rescore_answered.py`); yoksa çekinme faith=0 alıp ortalamayı
> çeker: 12B'de ham 0.737 vs gerçek **0.904.** Ve **coverage'ı A1'in yanında raporla.**
>
> **Çekimserlik talimatı grounding'i bozabilir (#38).** Kademeli izolasyonda tetikleyen tek bileşen
> sistem istemindeki *"kaynakta yoksa 'yer almıyor' de"* satırıydı; o satırla model, cevabı kaynakta
> **olan** soruda bile çekimser kaldı. n=1 anekdottu → **CANON n'iyle ölçülmeli.**
>
> **12B çıpaları (kalibrasyon, hedef değil):** M1 0.879 · M3 1.000 · M4 0.977-0.983 · M2 0.704 ·
> M5 0.225 · register 1.0

## CP2 — Veri hazırlığı

**TODO:** §2 (`τ_grounding` verisi) · **GPU:** yok

`train/raft/` **hazır** (17.323 / 962 / 962) ve base'den bağımsız. Ölçülmüş bileşimi:

| dilim | satır | pay | şekli |
| :--- | ---: | ---: | :--- |
| grounded | 13.350 | 77,1% | 5 `[KAYNAK]` (1 gold + 4 hard-negative) → gold'a dayan, birebir alıntıla, atıf ver |
| abstain | 3.455 | 19,9% | 4 `[KAYNAK]`, **gold çıkarılmış** → reddet |
| replay | 518 | 3,0% | genel Türkçe, 0 kaynak → unutma sigortası |

İki şey **yeni tokenizer'a göre yeniden doğrulanmalı:**

- [ ] **Token bütçesi** — `max_seq_len` içine kaç örnek sığıyor? Yeni tokenizer Türkçe'yi farklı
      verimlilikte kodlar → kırpma oranı değişir. Ölç, `--max-chunk-chars`'ı gerekirse ayarla.
- [ ] **Chat template render'ı** eğitim tarafında CP0'ınkiyle aynı mı.
- [ ] **20 satırlık smoke pack** → gözle bak: gold gerçekten context'te mi, distractor'lar makul mü.

> ### ⚠️ 12B'den — burada üç ayrı sessiz bozukluk çıktı
>
> **Truncation (#15).** `max_seq_len=2048` ile **1.421/17.323 (%8,2)** örnek "tüm label −100" diye
> düşürüldü; toplam **2.010 (%11,6)** örneğin cevabı kısmen kesikti — *yarım cevap öğretimi*,
> hiçbir uyarı vermeden. Kök neden ölçüldü: suçlu cevap değil (median **196** token), **kaynak
> bloğu** (median 1.030, **max 12.805**). Çözüm **900-char clip** → %11,6 → **%0,03.**
> Ve bu clip bir eval artefaktı değil: gerçek retriever zaten **chunk** döner.
>
> **Sessiz veri bozukluğu (#14).** Pack, `source` alanını gold metni sanıyordu — o alan
> **provenance etiketiydi.** Hata vermedi; smoke'un gate'i **16/16 RED** verince yakalandı.
> → Her veri üretiminden sonra **küçük bir smoke.** ~16 çağrı, ~15K çağrılık koşuyu kurtardı.
>
> **Teacher jargonu sızar (#16).** Eğitim hedeflerinin **%5,99'u (1157/19305)** teacher'ın iç
> etiketini ("GOLD") cevabına taşımıştı — öğrenci o etiketi context'te hiç görmediği hâlde ezberledi.
> → Teacher, **öğrencinin gördüğü etiket uzayında** promptlanmalı. *(Mevcut set scrub'lı.)*
>
> **Topik-skew (#14).** Seed dosyası kanuna göre **sıralı**ydı; yarıda kesilen üretim "rastgele
> örnek" değil **sistematik kapsama deliği** verdi (bir kanun tamamen sıfırdı).

---

### ✅ FAZ A çıkış ölçütü

- [ ] CP0 **6/6 yeşil** — base doğrulandı, model duruyor, turn işaretleri elde
- [ ] CP1 tamamlandı — 6-mod base çıpaları kayıtlı, **Kapı 0 kararı verildi**
- [ ] CP2 tamamlandı — token bütçesi ölçüldü, smoke pack gözle doğrulandı
- [ ] `research_log/` girdisi **#39** yazıldı (Faz A bulguları + base çıpaları)

---

# FAZ B — İLK FINE-TUNE (FT-1)

## CP3 — SMOKE (para-kapısı: ~$0.15)

**TODO:** §2 · **GPU:** Modal ve/veya yerel

```bash
modal run --detach modal_train.py::spawn_sft \
  --model <base> --data data/train/raft \
  --user-part '<CP0'dan>' --assistant-part '<CP0'dan>' \
  --run-name tg-smoke --max-steps 50
```

**Geçme ölçütü (dördü birden):**
- [ ] Veri doğru yüklendi (satır sayısı beklendiği gibi)
- [ ] **Turn işareti assert'i geçti** — yanlışsa burada durur, asıl amacı bu
- [ ] LoRA takıldı, param sayısı makul — **0 ise `--target-modules` tutmuyor**
- [ ] Loss düşüyor · OOM/NaN yok

**💡 Bu smoke'u iki yerde de koş.** 50 step yerelde ~10 dk, Modal'da ~$0.15. Çıkan `s/it` değeri
"yerelde mi Modal'da mı eğitelim" sorusunu **tahminle değil ölçümle** kapatır — ve zaten yapman
gereken işin içinde.

> ### ⚠️ 12B'den
> **`--detach` ŞART.** `--detach`siz `spawn` → ephemeral app entrypoint bitince kapanır, spawn'lanan
> job **iptal olur.** İlk smoke tam böyle 0 task koştu.
> **`spawn()` kullan, `remote()` değil** — `remote()` client'a bağlı bekler; WSL/PC kapanınca
> SIGTERM → Modal'a cancel → **job ölür.** Bu ders **4 koşu yakarak** öğrenildi.

## CP4 — FT-1: `τ_grounding` tam eğitim

**TODO:** §2 "τ_grounding eğit" · **GPU:** CP3'ün `s/it` sonucuna göre yerel ya da Modal

```bash
--lr 1e-4 --rank 16 --alpha 32 --target-modules <all-linear> \
--warmup-ratio 0.05 --epochs 1 --save-steps 200
```

**Kilitler:** `lr ≥ 3e-4` **yasak** (v1'in abstention çöküşü tam o rejimdeydi; `--allow-high-lr`
olmadan `train_sft.py` durur) · replay havuzu karışımda · `save_steps` + oto-resume açık.

> ### ⚠️ 12B'den
> **Ara checkpoint hayat kurtarır.** `save_steps=200` + oto-resume + periyodik volume commit
> sayesinde spawn tutmasa bile koşu kaybolmaz.
> **Replay'i atlama** — LoRA + düşük rank + **replay** üçlüsünün üçüncü ayağı; 12B'de M5'te
> forgetting görülmedi.
>
> **12B referansı:** v2b = 1.083 step · 4 sa 19 dk (12,72 s/it, A100-40GB) · train_loss 0.30 ·
> adapter 65.5M param / 262 MB · 0 örnek düşürüldü.
> **~4B projeksiyonu:** A100'de ~4-5 s/it → ~1,5 saat. Yerel: **ölçülmemiş**, CP3 söyleyecek.

## CP5 — Ölçüm

**TODO:** §3 (kafesin ilk hücresi: `τg` tekili) · **GPU:** çıkarım + hakem

`τ_grounding`'i CP1'in **aynı** 6 modunda koş — **harness KAPALI**, aynı seed/n/hakem.

| ne | nasıl |
| :--- | :--- |
| 6-mod CANON | CP1'in komutları + `--adapter outputs/tg` |
| A1 | **cevaplanan-only** + coverage yan yana |
| Kıyas | CP1 çıpaları — **elmayla elma**, aynı harness/mod/n/seed/hakem |
| Kayıt | `research_log/` girdisi **#40**, aynı gün |

### Ön-kayıtlı beklenti

| eksen | beklenti | neden | 12B'de |
| :--- | :---: | :--- | :--- |
| **M1** distractor sadakati | **↑↑** | kolun çekirdek hedefi (%77 dilim) | 0.879 → **0.904**, cov %47,5 → **%72,5** |
| **M4** oracle | **→** | tavan, ayırmıyor | 0.977 → 0.975 |
| **M2b** çok-kaynak ıska | **↑** | %20 abstain dilimi **tam bu şekli** öğretiyor | **0.96** |
| **M3** boş bağlam | **→** | zaten tavan | 1.000 → 1.000 |
| **M2** near-miss tek kaynak | **↓↓** | bu şekil veride **hiç yok** | 0.786 → **0.346** |
| **M5** kör | **↓/→** | anti-hedef | 0.225 → 0.175 |
| **register** | **→** | loss'ta değil | 1.0 |

> ### ⚠️ **M2 düşecek — bu beklenen, panik sebebi değil**
>
> Grounding kolu tek başına abstention'ı korumaz; zaten o yüzden ayrı bir `τ_abstention` kolu ve
> merge var. **Sprint 1'in işi bu düşüşü ölçmek, önlemek değil.**
>
> **Ama bir ayrım yap: off-distribution artefaktı mı, gerçek kayıp mı?** 12B'de M2-oracle 0.346'ydı
> ama **training-matched M2b 0.96** — model *eğitilmediği prompt biçiminde* ölçülmüştü.
> → M2 ve M2b'yi **birlikte** oku; ikisi farklı şey söylüyorsa framing uyumsuzluğunu ara.
>
> **M2 = 1.0 iyi haber değil.** Aşırı red, coverage çöküşünün diğer yüzü. Hedef: grounding korunmuş
> hâlde ~0.8-0.9 bandı.

---

### ✅ FAZ B = SPRINT 1 çıkış ölçütü — üç soru cevaplanmış olur

1. **Hat çalışıyor mu?** veri → eğitim → GGUF → eval, yeni base'de uçtan uca.
2. **`τ_grounding` ne satın aldı?** M1 ve coverage'da base'e göre delta.
3. **Yan hasar ne kadar?** M2/M2b/M3 düştü mü — grounding kolu tek başına abstention'ı bozuyor mu.

---

## Sprint 1 dışında kalanlar

| iş | nerede | neden burada değil |
| :--- | :--- | :--- |
| `rejected` hasadı + `τ_abstention` | Sprint 2 | çalışan çıkarım hattı ister — Faz A onu kuruyor |
| `τ_register` | Sprint 2 | kararı Kapı 0 veriyor (CP1) |
| Tabanlar (karışık · ardışık SFT) | Sprint 2 | kollar bitmeden kıyas anlamsız |
| Merge + 7 hücreli kafes | Sprint 3 | en az 2 kol gerekiyor |
| DEV havuzu + regex kalibrasyonu | Sprint 2-3 | rakip ölçümünden önce |
| Harness | Sprint 4 | iç ablasyondan bağımsız, **paralel yürüyebilir** |
| Dış parite matrisi | Sprint 5 | kazanan konfigürasyon belli olduktan sonra |

> **📌 Açık genişletme seçeneği.** Faz B'ye **FT-2** (`τ_abstention`) de eklenirse ilk **çatışma sinyali** bir
> sprint erken görülür (`τg + τa` hücresi, merge bedava → yalnız eval maliyeti). Tek engel:
> `rejected` hasadı bir çıkarım koşusu ve Faz A'nın bitmesini bekliyor. **Karar verilmedi.**

---

## Kayıt hijyeni (sprint boyunca)

- Her fazın sonunda → `research_log/` girdisi, **aynı gün**, sayılar kaynağıyla
  (metrik + n + hakem + seed + çıktı dosyası).
- Sürpriz/negatif sonuç → **aynı rigorla** kaydedilir; 12B'nin en değerli bulguları negatiflerdi.
- Yeni karar çıkarsa → ADR-0028+ (eskiyi silme, süperseded işaretle).
