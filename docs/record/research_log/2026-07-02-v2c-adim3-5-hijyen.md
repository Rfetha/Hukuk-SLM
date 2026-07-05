## v2c icra — ADIM 3-5: C2 (position-bias) + B1 (GOLD-scrub) + B2/B3 (hijyen) (2026-07-02)
Otorite: [`v2c/roadmap.md`](../v2c/roadmap.md) §5 madde 3-5. Hepsi GPU'suz kod/veri incelemesi — ADIM 2 GPU batch'i (C3+C4+C1-base/v1) arka planda koşarken paralel yapıldı. `v2c` branch'inde.

**ADIM 3 — C2 position-bias shuffle (G2 de test eder): sıfır-kod, ZATEN VAR.**
- `raft_pack.pack_context` satır 125 `rng.shuffle(chunks)` → gold, distractor'lar arasında randomize. rng per-örnek deterministik (`gen_eval_grounded` satır 210 `Random(seed+i)`) → tekrar-üretilebilir ama pozisyon sabit değil.
- **Ampirik teyit (v2b M1 detail, n=40):** gold `[KAYNAK n]` pozisyon dağılımı `{1:9, 2:9, 3:9, 4:9, 5:4}` (40/40 eşleşti) → 5 slota düzgün yayılmış, **pozisyon-bias YOK**. Bu, G2 off-by-one'ın "gold hep aynı slotta → etiket ezberi" maskesini de dışlar. **Kod değişikliği gerekmedi.**

**ADIM 4 — B1 GOLD-scrub (G3): TAMAMLANDI.**
- **(a) Teacher-prompt yasağı:** `gen_v2b_answers.py` `TEACHER_SYSTEM`'e "cevap metninde 'GOLD' kelimesini ASLA kullanma (hiçbir çekimle); 'ilgili kaynak/madde' veya '[KAYNAK N]' de" kuralı eklendi. ⛓️ ADIM 6b gen_answers'tan önce şart — yeni üretim temiz doğsun.
- **(b) Mevcut answers.jsonl scrub:** `data/processed/sft_v2b/answers.jsonl` — sızıntı **1157/19305 = %5.99** (v2b_sonuclar %5.7 tahminini doğruladı). Baskın kalıp: "GOLD metnidir" (603), "GOLD madde metnidir" (94), "GOLD maddesidir" (28), "GOLD kaynağıdır" (27). Sıralı (en-özgül-önce) regex + fallback token → **1157→0**, cümleler korundu ("…içeren GOLD metnidir" → "…içeren ilgili kaynak metnidir"). Yedek: `answers.jsonl.pre_scrub.bak`.

**ADIM 5 — B2 replay teyit + B3 core_hard: B2 DOĞRULANDI (dokunulmadı) · B3 BELGELENDİ (kaldırma ertelendi).**
- **B2:** `data/processed/replay_tr.jsonl` (n=600) = `AlicanKiraz0/Turkish-SFT-Dataset-v1.0` (MIT, license-clean), EDA-süzülü **genel/hukuk-DIŞI** TR instruction (yalnız 2/600 hukuk-terimli). Amaç = genel-yetenek koruması (anti-forgetting). Danışmanın "temiz Yargıtay" önerisi hukuk pattern'i pekiştirir = replay'in AMACINA aykırı → **mevcut replay uygun, DOKUNULMADI** (Claude-filtre "uygunsa dokunma").
- **B3:** core_hard kötü-eşleşme kesin vaka = **#28 & #29** (ikisi de "KAT MÜLKİYETİ KANUNU Madde 4"e bağlı, ama gold Md4 = "Ortak yerler" tanımı; sorular uyumsuzluk-yaptırımı/pay-iptali hakkında = ilgisiz). ⚠️ core_hard ŞİMDİ düzenlenirse koşan C3 batch + v2b sonuçları elmayla-elma olmaktan çıkar → **kaldırma n=120 final-kapı regen'ine ertelendi** (tüm modeller temiz sette birlikte koşulacak).

---

