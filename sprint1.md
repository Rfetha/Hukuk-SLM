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
│ CP0 base kapısı    (GPU yok)      │   │ CP4 smoke      (~$0.15)       │
│ CP1 DEV havuzu     (CPU)          │──►│ CP5 tam eğitim (asıl koşu)    │
│ CP2 base baseline  (çıkarım)      │   │ CP6 ölçüm      (hakem)        │
│ CP3 veri hazırlığı (CPU)          │   │                               │
└───────────────────────────────────┘   └───────────────────────────────┘
   6 kapı yeşil · DEV ayrık · Kapı 0      sprint biter: 3 soru cevaplı
```

> **CP1 neden burada?** Kapı 0 bir **seçim** kararı (`τ_register` eğitilsin mi) ve CP2'nin
> sayılarından veriliyor. O sayılar dondurulmuş TEST setinde üretilirse **test üzerinde seçim**
> yapmış oluruz — `TASARIM.md` §3.2 `data/eval/canon/`'u *"nihai raporda bir kez görülür"* diye
> bağlamıştı. DEV havuzu bu yüzden ilk FT'den önce, Faz A'da üretilir.

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

**TODO:** §0 (tamamı) · **GPU:** yok · **Çıkış:** `TASARIM.md` §8'in **6 kapı maddesi** yeşil

> ### ✅ GERÇEKLEŞEN (2026-07-24, #39) — **6/6 kapı yeşil**
>
> **Base seçildi:** `Qwen/Qwen3.5-4B` (sha `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`), **saf Apache-2.0**
> — kararlar **ADR-0030** (base + düşünce modu) · **ADR-0031** (precision) · **ADR-0032** (hakem paneli).
> ⚠️ **İsim düzeltmesi:** HF'de `Qwen/Qwen3.5-4B-Instruct` **yoktur** — instruct varyantının adı düz
> `Qwen/Qwen3.5-4B`. Belgelerde "-Instruct" geçen her yer yanlıştır.
>
> **GGUF üretildi:** `models/gguf/q35-4b-q4_k_m.gguf` (2.59 GiB, Q4_K_M, **PURE=0** — QAT yok).
>
> ⚠️ **Düşünce-modu bulgusu (ADR-0030).** Qwen3.5 **düşünen bir model**: varsayılan modda `</think>`
> kapanmıyor, `content` **BOŞ** dönüyor (HTTP **200**, sıfır hata — regex omurgası bu boş çıktılar
> üzerinde de sayı üretir). Model **yalnız düşünce modu KAPALI iken** düzgün duruyor (`finish_reason=stop`).
> → `gen_eval_grounded.py`'ye **`--thinking off`** + boş cevapta **erken patlama kapısı** eklendi.
>
> **Turn işaretleri:** `--user-part='<|im_start|>user\n'` · `--assistant-part='<|im_start|>assistant\n'`.
>
> **Kuantizasyon merdiveni + VRAM×bağlam matrisi** ölçüldü (`outputs/eval/vram_stack.json`):
> Q4_K_M ctx4096 = **3.09 GiB** · ctx131072 = **5.76 GiB** · f16 **sığmıyor**.
> **Performans:** 134 t/s decode (şarjda) — pilde **7.9** t/s (güç-durumu tuzağı kayda geçti).

Tablo 8 satır ama **kapı 6 madde** — 1 ve 5 destek adımı, kendi başlarına kapı değil.
`🔒` sütunu satırın §8'deki karşılığını verir.

| # | 🔒 §8 | iş | doğrulama |
| :-- | :--: | :--- | :--- |
| 1 | — | Aday base'i indir | destek adımı |
| 2 | **1** | **llama.cpp mimari desteği** | model yükleniyor mu, `--list-devices` |
| 3 | **5** | GGUF üret (kuantizasyon) | `bash scripts/setup_llamacpp.sh <repo> <etiket>` · **`PURE=0`** (QAT yok) |
| 4 | **2** | **Şablon render'ını GÖZLE oku** | `bash scripts/diag_chat_template.sh <gguf>` → `/apply-template` |
| 5 | — | **Model DURUYOR mu** | 4'ün saha teyidi: `bash scripts/smoke_llamacpp.sh <gguf>` → `finish_reason=stop` |
| 6 | **3** | **Turn işaretlerini çıkar** | 4. adımın render'ından `user_part` / `assistant_part` |
| 7 | **4** | Unsloth + sm_120 ortamı | `requirements.lock.txt` yeniden kur |
| 8 | **6** | Lisansı kaydet | attribution + limitations satırı |

> **7. madde CP2'yi bloke ETMİYOR.** Eval yolu llama.cpp/GGUF üzerinden koşuyor (ADR-0025) —
> `transformers`/Unsloth gerektirmez. Yani sm_120 borcu açıkken bile CP1-CP2-CP3 yürüyebilir;
> borç yalnız **Faz B'yi** (eğitim) bekletir. Sprintin en oynak kalemini kritik yoldan çıkarır.

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

> ### ✅ GERÇEKLEŞEN (CP0.7, #39) — çekirdek engel **bir günde** çözüldü
>
> Çekirdek engel bir **LD_LIBRARY_PATH** sorunuydu (`libnvJitLink.so.13`) — `global_venv/bin/activate`'e
> kalıcı bir satır eklendi, **NF4 forward doğrulandı**. Sprint'in en oynak kalemi bir haftayı yemedi.
> **Açık kalanlar Faz B'yi bekletir, Faz A'yı değil:** (a) `causal-conv1d` derlenmiyordu → **CUDA 13.0
> toolkit** kuruldu (`setup_cuda_toolkit.sh` sürüm-parametreli yapıldı), derleme sürüyor; (b) `all-linear`
> **görüntü kulesine** LoRA takıyordu (Qwen3.5 bir **VLM**) → metin-kulesi modül listesi çıkarıldı
> (`q_proj,k_proj,v_proj,o_proj,in_proj_qkv,in_proj_z,in_proj_a,in_proj_b,gate_proj,up_proj,down_proj`),
> **29.9M eğitilebilir param**, görüntü kulesi temiz.

## CP1 — DEV havuzu 🔒

**TODO:** §1 "DEV havuzu üret" · **GPU:** yok

`data/eval/canon/` (40+35) **TEST**'tir: dondurulmuş, nihai raporda **bir kez** görülür
(`TASARIM.md` §3.2). Seçim kararlarının hepsi — Kapı 0, merge süpürmesi, hiperparametre —
**DEV** üzerinde alınır.

```bash
python scripts/build_eval_sets.py --core-n 80 --trap-n 70 --seed 20260724 \
  --out-dir data/eval/dev \
  --exclude data/eval/canon/core_hard.jsonl data/eval/canon/trap.jsonl
```

**Kabul ölçütü: TEST ile kesişim = 0.**

```bash
python - <<'PY'
import json
def qs(p):
    return {next(x['content'] for x in json.loads(l)['messages'] if x['role']=='user')
            for l in open(p, encoding='utf-8') if l.strip()}
dev  = qs('data/eval/dev/core_hard.jsonl')  | qs('data/eval/dev/trap.jsonl')
test = qs('data/eval/canon/core_hard.jsonl') | qs('data/eval/canon/trap.jsonl')
print(f"DEV={len(dev)} TEST={len(test)} KESİŞİM={len(dev & test)}")   # KESİŞİM 0 OLMALI
PY
```

> ### ⚠️ `--exclude` olmadan DEV üretmek İŞE YARAMAZ
>
> CORE-HARD seçimi **karmaşıklığa göre sıralı ve seed'den bağımsız** — farklı `--seed` **aynı**
> maddeleri verir, büyük `--core-n` ise TEST'in **üst kümesini**. Yani `--exclude`'suz "DEV"
> üretmek TEST'i ikinci bir isimle kopyalamaktır ve **hata vermez.** Bayrak bunun için eklendi;
> kesişim denetimi de bu yüzden kabul ölçütü.
>
> **n = 80+70 geçici.** Hedef n güç analizine bağlı (`TODO` §1, açık soru). Üretim deterministik
> ve bedava — sayı netleşince komutu yeniden koş.

## CP2 — Base baseline + Kapı 0

**TODO:** §2 "Kapı 0" · §1 (regex kalibrasyonunun ilk yarısı) · **GPU:** çıkarım (llama.cpp, yerel)

Yeni base'i **çıplak** olarak 6-mod CANON protokolünde, **DEV havuzunda** koş. Üç çıktı:

1. **Çıpalar** — `τ_grounding`'in yeneceği/koruyacağı sayılar (M1 · M3 · M4)
2. **Kapı 0 kararı** — register-proxy → `τ_register` kolu gerekli mi?
3. **Hattın doğrulaması** — eval yolu yeni base'de uçtan uca çalışıyor mu

**Önce sunucuyu aç** (ADR-0025: eval llama.cpp/GGUF üzerinden; `transformers` yolu gerekmez):

```bash
$HOME/code/llama.cpp/build-cuda/bin/llama-server -m <CP0'ın GGUF'u> \
  --port 8080 --ctx-size 4096 --cache-type-k q8_0 --cache-type-v q8_0 &
export LLAMA_SERVER_URL=http://127.0.0.1:8080
export DEV=data/eval/dev
```

**1) Altı modun cevaplarını üret** — `--data` her modda AÇIKÇA verilir:

```bash
python scripts/gen_eval_grounded.py --label m1_base  --data $DEV/core_hard.jsonl --distractors 4 --max-chunk-chars 900 --n 80
python scripts/gen_eval_grounded.py --label m4_base  --data $DEV/core_hard.jsonl --with-source --n 80
python scripts/gen_eval_grounded.py --label m2_base  --data $DEV/trap.jsonl      --with-source --n 70
python scripts/gen_eval_grounded.py --label m2b_base --data $DEV/core_hard.jsonl --distractors 4 --no-gold --n 80
python scripts/gen_eval_grounded.py --label m3_base  --data $DEV/core_hard.jsonl --empty-context --n 80
python scripts/gen_eval_grounded.py --label m5_base  --data $DEV/core_hard.jsonl --n 80        # kör
```

> ⚠️ **`--data`'yı ASLA düşürme.** Script'in default'u `data/train/grounded_qa/test.jsonl`
> (1022 satır) — CANON değil, eğitim setinin komşusu. Hata vermez, tablo dolar, sayı yanlış sete
> aittir. `--n` havuz boyutuyla aynı olduğu için çıktı **doğru görünür.**

**2) Skorla** — M1/M4 groundedness hakemi, M2/M2b/M3 abstention hakemi, M5 anti-hedef:

```bash
for M in m1 m4 m5; do
  python scripts/groundedness.py --details outputs/eval/${M}_base_detail.jsonl --label ${M}_base --mode data
done
for M in m2 m2b m3; do
  python scripts/score_abstention.py --details outputs/eval/${M}_base_detail.jsonl --label ${M}_base \
    $( [ $M = m2b ] && echo --source-field context_shown )     # M2b: gold GÖSTERİLMEDİ
done
```

**3) A1 = cevaplanan-only + register:**

```bash
python scripts/rescore_answered.py --gnd outputs/eval/gnd_m1_base.jsonl \
  --bench outputs/eval/m1_base_detail.jsonl --label m1_base
python scripts/score_register.py --details outputs/eval/m1_base_detail.jsonl --label m1_base
```

**Kapı 0:** register-proxy yüksekse `τ_register` **düşer** → kol 3→2, kafes 7→3 hücre, **FT bütçesi
6'dan 5'e iner** (FT-3 düşer). Düşükse kol gerekçeli olur.

> ### ✅ Kapı 0 KARARI VERİLDİ (#39) — **`τ_register` DÜŞÜYOR**
>
> Register proxy **0.96-0.98** (RAG modlarında) → yüksek, base zaten güçlü. Sonuç: **kol 3→2**,
> **kafes 7→3 hücre** (`τg · τa · τg+τa`), **FT bütçesi 6→5 koşu** (FT-3 / `τ_register` düşer).

### Hakem erişimi — bu sprintte tek aile yeter, kod çok-aileye hazır

CP2'nin çıktısı **iç kıyas**: çıpalar CP6'da `τ_grounding` ile *aynı hakemle* karşılaştırılacak.
Aynı hakem her iki tarafta kullanıldığı sürece **tek aile — bugünkü `OPENAI_API_KEY` — yeterli.**
Üç aileli panel sayıların **rapor edildiği** yerde gerekir → **Sprint 3** (iç iddia kararı) ve
**Sprint 5** (parite). Sprint 1'de çok-aile için para harcanmaz.

> ⚠️ **GERÇEKLEŞEN (#39):** `.env`'e `OPENROUTER_API_KEY` de eklendi (CP7 önizlemesi için, aşağıda) —
> ama **CP2 yine OpenAI-direct'e PİNLENDİ** (`LLM_GATEWAY=openai`, hakem gpt-4o-mini): iç kıyasın iki
> tarafı (base çıpaları ↔ CP6 `τ_grounding`) **tek servis yığınında** tutulsun diye. Anahtar durur,
> gateway CP2 için OpenAI'da sabit.

Kod tarafı şimdiden hazır (ADR-0029): `scripts/llm_client.py` **tek erişim kapısı**, hakem
scriptleri oradan geçiyor. `.env`'e `OPENROUTER_API_KEY` eklendiği an kapı kendiliğinden
OpenRouter'a döner — **script değişikliği yok**, anahtar yokken `OPENAI_API_KEY` yolu aynen çalışır.

**Faz A'da yine de bir karar var:** panelin üç ailesi **base ailesi belli olunca** seçilebilir —
aile-dışlama (bir özneyi kendi ailesinin hakemi notlamaz) doğrudan CP0'ın çıktısına bağlı.
CP0 biter bitmez üç aileyi yaz; harcama Sprint 3'e kalsın.

> ### ⚠️ Anahtar takıldığı gün üç doğrulama — üçü de varsayılamaz
>
> | ne | neden |
> | :--- | :--- |
> | **JSON modu her ailede çalışıyor mu** | hakem scriptleri katı JSON bekliyor; OpenAI dışı ailelerde `response_format` yok sayılabilir. `loads_tolerant` yedeği var ama **çalıştığını gör** |
> | **Sağlayıcı pinlenmiş mi** | özet JSON'daki `judge_providers` **tek eleman** olmalı. Birden fazlaysa aynı model kimliği farklı servis yığınında (farklı kuantizasyon) koşmuş → sayılar kıyaslanamaz, ve **hata vermez** |
> | **Fiyat kaydı var mı** | `llm_client.PRICE`'a **birincil-kaynak liste fiyatı** girilir, kapıya ödenen tutar değil. Ödediğini parite fiyatı sanmak rakibi pahalı gösterir — kalibre edilmemiş red regex'iyle aynı hata sınıfı (ADR-0029) |

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

> ### ✅ GERÇEKLEŞEN — **YENİ BASE ÇIPALARI** (Qwen3.5-4B · DEV · gpt-4o-mini · seed 3407, #39)
>
> 6-mod base çıpaları DEV havuzunda üretildi (**470 cevap**), hakemle skorlandı (`judge_gateway=openai`):
>
> | mod | metrik | değer |
> | :--- | :--- | ---: |
> | **M1** distractor | faithfulness_macro · cit_precision · coverage(cevaplanan) | **0.8385** · 0.9775 · **%56** |
> | **M4** oracle | faithfulness_macro · cit_precision | **0.981** · 1.0 *(tavan)* |
> | **M2** near-miss | regex-Rej · LLM-red | 0.500 · **0.633** |
> | **M2b** çok-kaynak ıska | Rej | **0.938** |
> | **M3** boş bağlam | Rej | **1.000** |
> | **M5** kör *(anti-hedef)* | red | **%62.5** |
> | **register** (deterministik proxy) | RAG modlarında | **0.96-0.98** |
>
> ⚠️ **Regex kalibrasyonu YAPILDI — kendi base'imizde (#39).** Eski regex, base'in **baskın red kalıbı**
> olan `bulunmuyor`u görmüyordu → kalibrasyonsuz **M3 0.000** (gerçek 1.000) ve **M2b 0.662** (gerçek 0.938)
> çıkacaktı. `score_abstention.py` kalibre edildi, **15/15 ileri + 2/2 geri** yön elle doğrulandı. Bu, TASARIM
> §3.4'ün "hiçbir abstention sayısı kalibrasyonsuz raporlanmaz" kuralının **bizim base'imizde** de ısırdığının
> kanıtı (rakip aileleri için kalibrasyon hâlâ açık — CP7'de ilk rakip).

## CP3 — Veri hazırlığı

**TODO:** §2 (`τ_grounding` verisi) · **GPU:** yok

`train/raft/` **hazır** (17.323 / 962 / 962) ve base'den bağımsız. Ölçülmüş bileşimi:

| dilim | satır | pay | şekli |
| :--- | ---: | ---: | :--- |
| grounded | 13.350 | 77,1% | 5 `[KAYNAK]` (1 gold + 4 hard-negative) → gold'a dayan, birebir alıntıla, atıf ver |
| abstain | 3.455 | 19,9% | 4 `[KAYNAK]`, **gold çıkarılmış** → reddet |
| replay | 518 | 3,0% | genel Türkçe, 0 kaynak → unutma sigortası |

İki şey **yeni tokenizer'a göre yeniden doğrulanmalı:**

- [x] **Token bütçesi** ✅ — **GERÇEKLEŞEN (#39): etkilenen %0.06** (eşik %1'in çok altında),
      `max_seq_len=2048` **korundu**. Yeni tokenizer Türkçe'yi farklı verimlilikte kodlar → kırpma oranı değişir:

```bash
python scripts/measure_token_budget.py --data data/train/raft/train.jsonl \
  --model <CP0'ın base'i> --max-seq-len 2048 --out outputs/eval/token_budget_base.json
```

  Script iki sayıyı ayrı verir: **DÜŞEN** (istem sınırı doldurmuş, cevaba yer kalmamış → tüm
  label −100) ve **KESİK** (cevap ortasında kesilmiş → yarım cevap öğretimi). **Etkilenen >%1 ise
  koşma** — `--max-chunk-chars`'ı kıs ya da `max_seq_len`'i büyüt. Dilim kırılımı da basılır,
  yani hasarın grounded'da mı abstain'de mi olduğu görünür.

- [ ] **Chat template render'ı** eğitim tarafında CP0'ınkiyle aynı mı.
- [x] **20 satırlık smoke pack** ✅ **GERÇEKLEŞEN (#39): gözle doğrulandı** — gold context'te, distractor'lar makul.

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
> → Teacher, **öğrencinin gördüğü etiket uzayında** promptlanmalı.
> ⚠️ **DÜZELTME (2026-07-24, #39):** `raft/` scrub'lı **DEĞİLDİ** (yalnız `grounded_qa` scrub'lıydı —
> eski not sadece onun için doğruydu). Yeni base hazırlığında **%7.51 sızıntı** bulundu
> (GOLD/DISTRACTOR, **1301/17323**, öğrenci girdisinde 0) — #16'nın birebir tekrarı.
> `scripts/scrub_teacher_jargon.py` yazıldı → temiz set **`data/train/raft_scrubbed/`** üretildi
> (orijinal ellenmedi, alıntı blokları korundu).
>
> **Topik-skew (#14).** Seed dosyası kanuna göre **sıralı**ydı; yarıda kesilen üretim "rastgele
> örnek" değil **sistematik kapsama deliği** verdi (bir kanun tamamen sıfırdı).

---

### ✅ FAZ A çıkış ölçütü — **TAMAM (2026-07-24, #39)**

- [x] CP0 — §8'in **6 kapı maddesi 6/6 yeşil** · model duruyor (`finish_reason=stop`, `--thinking off`, ADR-0030) · turn işaretleri elde (`<|im_start|>user\n` / `<|im_start|>assistant\n`) · GGUF `q35-4b-q4_k_m.gguf` 2.59 GiB
- [x] CP1 — DEV havuzu (`data/eval/dev/`, 80 core_hard + 70 trap) üretildi, **TEST ile kesişim = 0** doğrulandı
- [x] CP2 — 6-mod base çıpaları **DEV'de** kayıtlı (470 cevap, gpt-4o-mini, seed 3407), **Kapı 0 kararı VERİLDİ: `τ_register` düşüyor** (register 0.96-0.98)
- [x] Hakem panelinin **üç ailesi yazıldı** — **ADR-0032**: OpenAI · Anthropic · Google (Qwen özneden **ayrık**, aile-dışlama) — harcama Sprint 3'te
- [x] CP3 — token bütçesi ölçüldü (**etkilenen %0.06 ≤ %1**), smoke pack gözle doğrulandı, `raft_scrubbed/` üretildi (%7.51 sızıntı temizlendi)
- [x] `research_log/` girdisi **#39** yazıldı (`docs/record/research_log/2026-07-24-cp0-base-dogrulama-kapisi.md` — Faz A bulguları + base çıpaları)

---

# FAZ B — İLK FINE-TUNE (FT-1)

## CP4 — SMOKE (para-kapısı: ~$0.15)

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

> ### ✅ GERÇEKLEŞEN (2026-07-25) — **4/4 ölçüt yeşil · hız 36 → 5.4 s/it (6.4×)**
>
> Karar: **ADR-0033**. Modal A100-40GB, `--bf16-base`, 50/50 adım **6 dk 52 sn**.
>
> | ölçüt | sonuç |
> | :--- | :--- |
> | veri doğru yüklendi | ✅ `Num examples = 17,323` (`/data/raft_scrubbed`) |
> | turn işareti assert'i | ✅ render'da doğrulandı |
> | LoRA param sayısı | ✅ **29.908.992 / 4.57B = %0.65**, görüntü kulesi temiz |
> | loss düşüyor · OOM/NaN yok | ✅ 0.7987 (adım 10) → **0.3537** (adım 50), grad_norm 0.54 |
>
> **Faz B'nin kapısı bir paket bölünmesiydi, sürüm değil.** Devir notunun *"fla torch≥2.11 istiyor,
> ayrı image kur"* teşhisi **çürütüldü**: `flash-linear-attention` 0.5.x'te bölünmüş, çekirdekler
> **`fla-core`**'da; `--no-deps` onu atlayınca `import fla` çalışıyor (→ transformers fast-path'i
> **açık sanıyor**) ama `fla.modules` yok → **model hiç yüklenmiyor.** Eksik `fla-core`, fla'nın
> hiç olmamasından KÖTÜ. Pinli lock korundu, ayrı image kurulmadı.
> ⚠️ `causal-conv1d` yok → *"fast path is not available"* uyarısı **yine basılır**; uyarı ölçüt değil, **s/it** ölçüt.
>
> **Hız kaldıraçları KALİTE-NÖTR olanlarla sınırlandı** (kullanıcı kuralı): checkpointing kapalı +
> `batch 2 × grad_accum 8` (etkin batch **16 sabit**). **`lora_dropout=0` reddedildi** — CP6'nın
> yan-hasar ölçümünde *"kol mu bozdu, dropout mu"* sorusunu cevapsız bırakırdı.
> Kanıt: adım 10 loss **0.7987 ↔ 0.788** (çıpa) · `adapter_config.json`: `lora_dropout=0.05`,
> `use_rslora=False` → `ΔW=(α/r)·BA` tanımı sağlam.
>
> **⚠️ İki yol tuzağı kayda geçti** (ikisi de bir koşu yaktı):
> `--data` **konteyner** yoludur → volume `/data`'ya bağlı, yani `/data/raft_scrubbed`
> (artık model yüklenmeden **saniyede** patlıyor) · `--target-modules` verilmezse `in_proj_*`
> düşer ve **24 linear-attention katmanı LoRA'sız kalır** — hata vermeden.
>
> **Yeni araç:** `modal_diag.py` — `transformers`'ın kök nedeni gizleyen tembel-modül hatasını
> (`Could not import module 'Qwen3_5ForConditionalGeneration'`) en ucuz GPU'da saniyeler içinde açar.
>
> **Tam koşu projeksiyonu:** 1083 adım × 5.4 s ≈ **1.6 saat ≈ $4** (Modal cap $35 → **$42.50**).

> ### ⚠️ 12B'den
> **`--detach` ŞART.** `--detach`siz `spawn` → ephemeral app entrypoint bitince kapanır, spawn'lanan
> job **iptal olur.** İlk smoke tam böyle 0 task koştu.
> **`spawn()` kullan, `remote()` değil** — `remote()` client'a bağlı bekler; WSL/PC kapanınca
> SIGTERM → Modal'a cancel → **job ölür.** Bu ders **4 koşu yakarak** öğrenildi.

## CP5 — FT-1: `τ_grounding` tam eğitim

**TODO:** §2 "τ_grounding eğit" · **GPU:** CP4'ün `s/it` sonucuna göre yerel ya da Modal

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
> **~4B projeksiyonu:** A100'de ~4-5 s/it → ~1,5 saat. Yerel: **ölçülmemiş**, CP4 söyleyecek.

## CP6 — Ölçüm

**TODO:** §3 (kafesin ilk hücresi: `τg` tekili) · **GPU:** çıkarım + hakem

`τ_grounding`'i CP2'nin **aynı** 6 modunda koş — **harness KAPALI**, aynı seed/n/hakem.

| ne | nasıl |
| :--- | :--- |
| 6-mod CANON | CP2'nin komutları + `--adapter outputs/tg` |
| A1 | **cevaplanan-only** + coverage yan yana |
| Kıyas | CP2 çıpaları — **elmayla elma**, aynı harness/mod/n/seed/hakem |
| Kayıt | `research_log/` girdisi **#41**, aynı gün *(#40 CP4'e gitti — 2026-07-25)* |

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

## CP7 — erken rakip önizlemesi (Gemini 3.1 Flash-Lite)

**TODO:** — (Sprint 5'ten öne çekilen bir dilim) · **GPU:** yok (rakip API) · **Kayıt:** `docs/record/sprint1/`

**Amaç:** Sprint 5 dış parite matrisinden **BİR DİLİMİ** öne çekmek — *"nerede duruyoruz"* erken
sinyali. Base çıpaları (CP2) çıktığına göre, tek komutla bir rakibin aynı çıpalarını almak bedava sayılır.

> ### ⚠️ Bu Sprint 5'in parite İDDİASI DEĞİL — bir önizleme
>
> Kazanan konfigürasyon **yok** (hedef model Sprint 3'te doğar), **adalet kuralı** (harness rakibe de
> verilir) burada **UYGULANMAZ** — çünkü **harness zaten KAPALI**: bu bir model-düzeyi kıyas, tam olarak
> CP2/CP6'nın koşulu (aynı harness/mod/n/seed). Parite iddiası harness × {açık/kapalı} matrisiyle Sprint 5'te kurulur.

**Rakip:** `google/gemini-3.1-flash-lite` (OpenRouter, **tarihli snapshot** — TASARIM §3.5 pinleme).

> ⚠️ **NOT:** daha yeni lite'lar var (`google/gemini-3.5-flash-lite`, `google/gemini-3.6-flash`,
> 2026-07-21). Kullanıcı açıkça **3.1-flash-lite** seçti; pin revize edilebilir (benchmark tek komut).

**Kurulum:** rakip aynı 6-mod CANON'u **DEV havuzunda**, aynı **seed/n**, `--thinking off` eşdeğeri
(Gemini için kendi düşünce ayarı — **doğrula**), **OpenRouter** üzerinden koşar. Hakem **gpt-4o-mini
(OpenAI)** → **aile-dışlama SAĞLANIR** (Google özneyi OpenAI hakem notlar, ADR-0032).

> ### ⚠️ ZORUNLU ÖN-ADIM (TASARIM §3.4) — kalibrasyonsuz hiçbir abstention sayısı raporlanmaz
>
> Red-tespit regex'i **Gemini'nin ÇIKTISINDA** kalibre edilMEDEN hiçbir abstention sayısı raporlanmaz.
> Kendi base'imizde `bulunmuyor` tuzağı çıktı (#39) — Gemini'nin **red dağarcığı farklı** olacak.
> **~30 çıktı elle spot-check.**

> ### ⚠️ Sağlayıcı pinleme (ADR-0029)
>
> OpenRouter **aynı model kimliğini farklı upstream'de** koşabilir; `judge_providers` / `gen_providers`
> **tek eleman** olmalı — yoksa sayı tek bir servis yığınına ait değildir.

> ⚠️ **Fiyat:** parite maliyeti **birincil-kaynak LİSTE fiyatıyla** (kapıya ödenen tutarla değil).

**Kayıt:** `docs/record/sprint1/` altında — metrik + n + hakem + **rakip snapshot** + seed + çıktı dosyası.

> ### ✅ GERÇEKLEŞEN (2026-07-24/25) — **kayıt: [`docs/record/sprint1/cp7-gemini-onizleme.md`](docs/record/sprint1/cp7-gemini-onizleme.md)**
>
> 6-mod × 2 özne **DEV** havuzunda koşuldu (470 cevap/özne, seed 3407, hakem `gpt-4o-mini`
> OpenAI-direct, harness KAPALI). **Aile-dışlama sağlandı** (Google özne ↔ OpenAI hakem, ADR-0032).
>
> **Sonuç: en ucuz frontier model çıplak base'i EZMİYOR.** Tavanda (M4 **0.981** vs 0.974) ve
> *cevapladığında* (A1 **0.9730** vs 0.9729) fark **ölçülemiyor**; M3 boş bağlamda ikisi de **1.000**,
> M2b'de ikisi de ~0.97-0.99. Açık **tam iki eksende**: **coverage** (M1 **%43.75** vs **%76.25**) ve
> **near-miss abstention** (M2 Rej regex **0.567** vs **0.807**). İkisi de `τ_grounding` + `τ_abstention`
> + red-kapısı harness'ının **doğrudan hedefi.** M5 anti-hedefte base daha temiz (0.399 vs 0.579).
>
> **§3.4 zorunlu ön-adımı yapıldı:** Gemini'nin red dağarcığı **kalibrasyon gerektirmedi** — bizim
> base'imizin dağarcığının **alt kümesi** (`bulunmuyor`/`bulunmamaktadır` %80). 181 geçerli tuzakta
> **2 ayrışma** (ikisi de regex'in hatası değil), 13 non-reject satırın **tamamı** + 18 reject satırı
> elle okundu. Regex **değiştirilmedi.**
>
> **⚠️ İki bulgu kayda girdi:** (a) **hakem varyansı** — `m4_gem` faith üç okumada 0.987 · 0.9738 ·
> 0.9736 (±0.013 bandı) → "M4/A1'de fark yok" ifadesi *fark ölçülemiyor* demektir; Sprint 3'ün
> üç-aileli paneli tam bu yüzden var. (b) **`rescore_answered.py` kalibre edilmemiş bir regex
> KOPYASI taşıyordu** → tek kaynaktan ithale çevrildi, tüm A1/coverage sayıları yeniden hesaplandı.
>
> **⚠️ Açık kalemler (Sprint 5 ön koşulu):** üretim tarafında **sağlayıcı pinlemesi artefaktlarda
> kayıtlı değil** (ham HTTP yolu `llm_client`'ı atlıyor) · **rakip üretim maliyeti ölçülmedi**
> (`llm_client.PRICE`'ta liste fiyatı yok).

---

## Sprint 1 dışında kalanlar

| iş | nerede | neden burada değil |
| :--- | :--- | :--- |
| `rejected` hasadı + `τ_abstention` | Sprint 2 | çalışan çıkarım hattı ister — Faz A onu kuruyor |
| `τ_register` | Sprint 2 | kararı Kapı 0 veriyor (CP2) |
| Tabanlar (karışık · ardışık SFT) | Sprint 2 | kollar bitmeden kıyas anlamsız |
| Merge + 7 hücreli kafes | Sprint 3 | en az 2 kol gerekiyor |
| Regex kalibrasyonu (rakip aileleri) | Sprint 2-3 | çok-aile erişimi ister (ADR-0029) — *DEV havuzu Faz A'ya alındı, CP1* |
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
