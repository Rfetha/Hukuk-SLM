# ADR-0026 — Base bir **parametre**; hat emekliliği yürürlükte; `data/` yeniden yapılandırıldı

**Statü:** Yürürlükte · **Tarih:** 2026-07-24
**İlgili:** ADR-0024 (hat emekliliği — **koşulu farklı yoldan gerçekleşti**) · ADR-0021 (base teyidi
— **süperseded**) · ADR-0017 (base SABİT — **süperseded**) · ADR-0023 (dağıtım config) · ADR-0025 (eval yolu)

## Bağlam

ADR-0017 base'i (Gemma 4 12B) **sabit** ilan etmiş, ADR-0021 bunu ölçülmüş gerekçeyle teyit
etmişti. ADR-0024 ise emekliliği **koşullu** bırakmıştı: yürürlük "task #22 (E4B vs 12B CANON
ölçümü)" kapısına bağlıydı.

Kullanıcı kararı (2026-07-24): **hiçbir modele bağlanma, sıfırdan başla.** Yeni base henüz seçilmedi.
Yani ADR-0024'ün koşulu, öngörülen yoldan (*ölçüm E4B'yi seçerse*) değil, **başka bir yoldan**
gerçekleşti: base artık 12B değil, *belirsiz*. Sonuç aynı — 12B'ye çapalı artefaktlar taşınmaz.

## Karar

### 1. Base bir **parametre**, gömülü karar değil

Hiçbir script'te base default'u YOK. Tanımsızsa **erken hata** verilir — gerekçe: yanlış modele
sessizce düşmek saatlerce süren bir koşuyu fark edilmeden çöpe çevirir.

Parametreleştirilen noktalar (tarama: 33 nokta / 14 dosya):
`train_sft.py` · `train_orpo.py` · `gen_v3_rejected.py` · `gen_eval_grounded.py` ·
`setup_llamacpp.sh` · `smoke_llamacpp.sh` · `diag_abstain.sh` · `build_replay_tr.py` · `modal_train.py`

**Koşulsuz olan üç şey koşullu hale getirildi** — hepsi base'e bağlıydı, sabit kodlanmıştı:
- `llama-quantize --pure` → `PURE` env. Gerekçesi *"QAT Q4_0 için kalibre"* (ADR-0023); QAT
  **olmayan** base'de yanlış tercih.
- `extra_special_tokens` LİSTE→DICT tokenizer yaması → `FIX_TOKENIZER` env. Gemma 4'e özgüydü.
- GPU seçimi (`A100`, gerekçe "12B QLoRA tatlı nokta") → `HUKUK_GPU` env.

### 2. Sessiz-bozulma kapısı: turn işaretleri assert edilir

`train_sft.py`'deki `GEMMA_USER_PART`/`GEMMA_ASSISTANT_PART` sabitleri (`<|turn>user\n` /
`<|turn>model\n`) repodaki **en tehlikeli bağımlılıktı**: yanlış base'de `train_on_responses_only`
hiçbir şeyi maskelemez, loss tüm diziden akar, **eğitim sessizce bozulur — hata vermez.**

Artık zorunlu argüman (`--user-part` / `--assistant-part`) **ve render'a karşı assert ediliyor**:
işaret render edilmiş şablonda yoksa eğitim başlamadan durur. Yeni base'de ilk kırılacak yer burasıydı.

Bu, 2026-07-24'teki minja şablon tuzağının genelleştirilmiş dersidir (`research_log` #38):
**her yeni base için şablon render'ı gözle doğrulanmalı.** Kontrol listesi: `configs/README.md`.

### 3. ADR-0024 yürürlükte — `old-version-gemma4-12b/`

Bölme çizgisi ADR-0024'ün tanımladığı gibi: *base'e bağlı mı, değil mi.*

| → arşive (taşındı, **silinmedi**) | → yerinde kaldı |
| :--- | :--- |
| `outputs/v0…v3` LoRA (1.8 GB) · `outputs/eval/` (161 dosya) | **`data/`** — en pahalı varlık |
| `models/gguf/` (21 GB) · `configs/gemma4_nothink.jinja` | `scripts/` — harness (sıfırdan yazılmaz) |
| `record/SCORECARD.md` + tur belgeleri (v2b/v2c/v3/v4) | **`docs/record/research_log/`** — kronoloji kesintisiz |
| `docs/_archive/` · 12 ölü script + `_legacy/` | `docs/adr/` · `knowledge/` |
| kirli `sft_v0` + reddedilen `sft_v2c` verisi | |

⚠️ **ADR-0024'ten sapma:** ADR-0024 `docs/record/{v2b,v2c,v3,v4}` + `SCORECARD.md`'yi arşive
gönderiyordu ve bu uygulandı — ancak `research_log/` ve `adr/` **pazarlıksız yerinde kaldı**
(ADR-0024'ün iki pazarlıksız kuralından biri). Taşımanın kırdığı 22 belge bağlantısı arşiv
yoluna güncellendi; repo genelinde 104 bağlantı doğrulandı, 0 kırık.

### 4. `data/` yönteme göre yeniden yapılandırıldı

Tur numarası (`sft_v2b`) yerine **yöntem adı** — yeni hat "hangi tur" bilmez, "hangi yöntem" bilir:

```
corpus/                      40.496 madde (yer-gerçeği)
eval/canon/                  core_hard(40) + trap(35)   🔒 dondurulmuş
eval/genelleme/              trap_xkanun · trap_ood · ood_qa
train/{grounded_qa, raft, orpo_abstain} + replay_tr.jsonl
_ham_ve_ara/                 ara + SUPERSEDED_ eval setleri
```

`.gitignore` istisnaları yeni yollara taşındı — **eval setleri ve korpus git-takipli kalır**
(dondurulmuş setin sessizce değişmemesi araştırma repro'sunun şartı). Büyük eğitim setleri git dışı.

## Sonuçlar

- **ADR-0017 ve ADR-0021 süperseded:** "base SABİT (Gemma 4 12B)" iddiası artık geçerli değil.
  İki ADR de **silinmez/yeniden yazılmaz** — o günkü gerekçe (QAT, 8 GB'da bağlam tavanı 176K vs
  91K, ölçülmüş KV analizi) yeni base seçiminde **kriter listesi** olarak hâlâ değerlidir.
- **ADR-0023 kısmen süperseded:** `--pure` + KV q8_0 kararı *QAT-Q4_0 base'ler için* doğru kalır,
  evrensel değil. Artık config'ten gelir.
- **CANON metodolojisi (ADR-0011) değişmez** — modlar, setler, n, seed, hakem aynı. Yeni base'in
  sayıları eski tabloyla **aynı tabloya karıştırılmaz** (protokol satırı ayrı; ADR-0025).
- **Açık borç:** yeni base seçilince tek bir `configs/base/<isim>.yaml` toplayıcısı kurulabilir —
  bugün parametreler script argümanı/env olarak dağınık ama **hiçbiri gömülü değil**, asıl risk kapandı.
- **Devir paketi:** repo dışında `~/code/hukuk-devir/` (veri + harness + kayıt + git bundle +
  damıtılmış `DEVIR.md` / `RECETELER_12B.md`) — repo silinse bile birikim ayakta.
