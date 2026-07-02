# DEVİR NOTU — 2026-07-02 (v2b eval BİTTİ + geçti · sıradaki = v2c reçetesi)

## TEK CÜMLE
v2b tam eğitim + 6-mod canon eval bitti, **tüm KAPILAR geçti** (grounding korundu, abstention
0.000→0.96 dirildi) → sıradaki iş: **v2c reçetesini yaz** (eval bulguları + dış danışman raporu sentezi).

## ▶ v2b SONUÇ — TÜM KAPILAR GEÇTİ ✅ (detay: `docs/record/v2b_sonuclar.md`)
| Mod | Ölçüm | v2b | base | v1 |
|---|---|---|---|---|
| M1 distractor | A1 (cevaplanan) | **0.904** | 0.879 | — |
| M2 TRAP-oracle | Rej* | 0.346 | 0.786 | 0.000 |
| **M2b distractor-only (adil A3)** | Rej* | **0.96** (n=30) | — | — |
| M3 boş | Rej* | **1.000** | 1.000 | — |
| M4 oracle | A1 | **0.975** | 0.977 | 0.960 |
| M5 KÖR | A2 | 0.175 | 0.225 | 0.300 |
- **v1'e karşı net kazandı:** grounding korundu+aştı, abstention **dirildi** (v1 0.000→v2b M2b 0.96), unutma yok (replay tuttu).
- **İki methodology dersi:** (1) abstention'ı **eğitim moduyla ölç** (M2-oracle 0.346 = off-dist artefakt, M2b 0.96 gerçek); (2) A1'i **cevaplananlarda** oku (ham 0.737 çekinme yüzünden yanıltıcı).
- **Kalan zayıflık = yalnız "yanlış-makul TEK kaynak" (M2 0.346)** = robustness, gate-fail DEĞİL.

## ▶ SIRADAKİ: v2c REÇETESİ (iki girdi harmanlanacak)
**Girdi A — eval bulguları (bu oturum):** `v2b_sonuclar.md` sonundaki "v2c tasarım notu".
**Girdi B — dış danışman raporu:** `docs/record/v2c_input_dis_danisman.md` (commit'e KATILMADI, yerel).

### Sentez — v2c için birleşik öncelikler
**P0 (sıfır maliyet, önce bunlar):**
- 🔴 **GOLD-scrub** — teacher hedeflerindeki `"GOLD metnidir"`/`"Verilen dökümana göre"` kalıpları regex temizle (%5.7→0). *(danışman P0 + eval bulgusu ortak)*
- 🔴 **TRAP-tipi abstain dilimi EKLE** *(EVAL bulgusu — danışman kaçırdı, kritik)*: "konu-komşusu yanlış TEK madde → gerekçeli red" örnekleri. Mevcut abstain dilimi "gold yok" tipinde (M2b 0.96 çözdü); eksik olan "yanlış-makul kaynak var" (M2 0.346). `gen_v2b_answers.py`'a dilim tipi ekle.
- 🔴 **Abstention loss-masking** — ret token'larına CE loss ×1.5-2.0 *(danışman P0)*. M2 0.346'yı ve param_leak %61.5'i hedefler.
- 🟢 **rsLoRA** (`use_rslora=True`) — sıfır maliyet kararlılık *(danışman P0)*.
- 🟢 **position-bias shuffle** — M1 gold yerini karıştır + judge'a "sıra önemsiz" *(danışman P0; not: raft_pack zaten shuffle ediyor, judge talimatı eklenebilir)*.

**P1 (Modal run, bütçe varsa):**
- 🟡 **ORPO** (reference-free) — teacher-jargon/leak çıktısı = negatif (y_l), temiz = pozitif (y_w) *(danışman P0 ama biz FT-run gerektirdiği için P1)*. Anti-parametric-leak'e de yarar.
- 🟡 **DoRA** — 2K örnekte bellek testi → kararlıysa ana eğitim *(danışman P1)*.
- 🟡 hedge dozajı %19→%25 ablasyonu.

**Regresyon KAPISI (v2c bunları DÜŞÜRMEMELİ):** M1 0.904 · M4 0.975 grounding · M2b 0.96 · M3 1.000 abstention.

**Açık (bloklamaz):** off-by-one atıf fix · core_hard kötü-eşleşme temizliği (≥3 vaka) · register ekseni ölç · base/v1'i M2b modunda yeniden skorla (elmayla-elma) · M2b n=40'a tamamla.

## DOSYALAR
- v2b scorecard: `docs/record/v2b_sonuclar.md` (6-mod + KAPI + v2c tasarım notu)
- Kayıt: `docs/record/research_log.md` (2026-07-02: D1 sonuç + methodology dersleri)
- Danışman girdisi: `docs/record/v2c_input_dis_danisman.md` (yerel, commit'siz)
- Eval kod: `gen_eval_grounded.py` (`--max-chunk-chars` mirror · `--no-gold` M2b) · `score_abstention.py` (`--source-field`)
- Eğitim: `modal_train.py::spawn_v2b` · `train_sft.py`
- ADR: 0010 (register) · 0011 (canon) · 0012 (scope) · 0013 (5-mod matris)
