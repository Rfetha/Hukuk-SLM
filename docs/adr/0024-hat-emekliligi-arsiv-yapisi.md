# ADR-0024 — Hat emekliliği: base değişirse `_archive_12b/`, kayıt yerinde kalır

**Statü:** **KOŞULLU** — yürürlüğe girmesi task #22 (E4B vs 12B CANON ölçümü) kapısına bağlı
**Tarih:** 2026-07-24
**İlgili:** ADR-0021 (base teyidi + masaüstü VRAM düzeltmesi) · ADR-0017 (base sabitleme) · ADR-0011 (CANON)

## Bağlam

ADR-0021'in kısmi düzeltmesi (masaüstü VRAM yükü) **E4B kolunu açtı.** Kullanıcı kararı:
*"E4B'ye geçmek istiyorum, ama önce ölç."* Geçiş gerçekleşirse 12B üzerine kurulmuş artefaktlar
taşınmaz — LoRA adaptörleri modele özgüdür.

Kullanıcı ayrıca hattın nasıl devredileceğini belirledi: *"eski hattı emekli edip yeni hat kuracağız,
fakat yeni hat dataları vs. eski hattan alacak."* Yani **lineer devam yok** — yeni hat, eski hattın
birikiminden **okuyarak** kurulur.

> Not: Bu, konuşmanın başındaki `vOLD-archived` fikrinin gerekçelenmiş hâlidir. O zaman
> reddedilmişti (base değişmiyordu → arşivin çözdüğü bir sorun yoktu). Base değişirse gerekçe
> gerçek olur: adaptörler ve judge hücreleri fiilen taşınmaz.

## Karar — bölme çizgisi: **base'e bağlı mı, değil mi**

### → `_archive_12b/` (base'e bağlı, taşınmaz)

| ne | boyut | neden |
| :--- | ---: | :--- |
| `outputs/v0…v3/` | ~2.5 GB | LoRA adaptörleri — modele özgü, E4B'de yüklenmez |
| `outputs/eval/` | 8.3 MB | 12B protokolüyle ölçülmüş 59 summary + 101 jsonl |
| `docs/record/{v2b,v2c,v3,v4}/` | — | tur sonuç belgeleri (12B sayıları) |
| `docs/record/SCORECARD.md` | — | tüm hücreler 12B-çapalı |

Arşiv dizinine bir `README.md` konur: **burada ne var, neden emekli, hangi ADR**.

### → Yerinde kalır (base'den bağımsız; yeni hat bunları kullanır)

| ne | boyut | neden |
| :--- | ---: | :--- |
| **`data/`** | **778 MB** | SFT/ORPO setleri **+ eval setleri** (`core_hard`, `trap`, `trap_ood`, `trap_xkanun`). Tokenizer'dan bile bağımsız — **en büyük varlık.** |
| `scripts/` | 632 KB | eval harness + hakem + builder'lar |
| `knowledge/` | 128 KB | literatür özetleri |
| `docs/adr/` | — | kararlar: süperseded olur, **silinmez/taşınmaz** |
| `docs/record/research_log/` | — | kronolojik kayıt — **ASLA arşive gitmez** |
| `docs/BEDESTEN_API.md` + `bedesten_probe.py` | — | harness tohumu |

## İki pazarlıksız kural

**1. `research_log/` ve `adr/` yerinde kalır.** CLAUDE.md'nin çekirdek garantisi:
*"makaleyi repo'dan haftalar sonra yeniden kurabilmek."* Kronolojik kayıt arşive taşınırsa o
garanti kırılır. Tarih **kesintisiz akar**; yalnız artefaktlar ayrışır. v0→v3 zaten
"proof-of-concept" olarak kayıtlı (ADR-0017) — emeklilik bunu değiştirmez, doğrular.

**2. `scripts/` sıfırdan yazılmaz.** Eval harness'ı 5 turda doğrulandı ve içinde **bulunmuş
hataların düzeltmeleri gömülü**: gold sızıntısı, mojibake fix, `rejection_exact` kalibrasyonu,
A1 cevaplanan-only macro (ADR-0011). Sıfırdan yazmak o hataları yeniden bulmayı gerektirir.
Doğrusu: script'ler **taşınır**, yalnız model yolları güncellenir. Gerçekten yeniden yazılacak
olan `build_sft_v4.py` / ORPO hattı — çünkü "v2b-continuation" zemini kırılıyor.

## Hedef yapı

```
_archive_12b/
  outputs/      ← v0…v3 adaptörleri + eval artefaktları
  record/       ← v2b, v2c, v3, v4 tur belgeleri + SCORECARD
  README.md     ← ne var / neden emekli / hangi ADR

(kök — yeni hat)
  data/                       ← DEĞİŞMEZ, yeni hat buradan okur
  scripts/                    ← taşınır, model yolları güncellenir
  docs/adr/                   ← yerinde, yeni ADR'ler eklenir
  docs/record/research_log/   ← yerinde, kronoloji devam eder
  outputs/                    ← boş başlar, E4B turları buraya
```

## Sonuç

- **Eski hat emekli, kayıt sürekli.**
- Yürürlük **task #22'ye kilitli**: ölçüm "E4B ≈ 12B" derse arşivleme başlar; "E4B belirgin kötü"
  derse 12B kalır ve arşive gerek olmaz.
- Geçiş olursa **sürüm rename kararı (v4→v1, eskiler v0.x) bu emeklilikle birleşir** —
  arşivdeki hat `v0.x`, yeni hat `v1` olur; ad şeması emeklilik sınırıyla doğal olarak örtüşür.
- **Açık borç:** `research_log/` (37 girdi) ve `adr/` (24) şişiyor; okunabilirlik için bir
  özet/indeks katmanı gerekebilir. Silme değil **navigasyon** sorunu — ayrı iş olarak ele alınacak.
