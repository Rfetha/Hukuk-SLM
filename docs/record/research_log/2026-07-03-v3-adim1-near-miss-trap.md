## 2026-07-03 · v3 ADIM 1 — zor near-miss trap havuzu (`build_sft_v3.py`) + EVAL-AYNASI kararı

**Ne yapıldı:** v3 ORPO pipeline ADIM 1 (v3_recipe §5.1). Yeni `scripts/build_sft_v3.py pack` → 19284 zor near-miss trap adayı (`data/processed/sft_v3/packed_v3.jsonl`). v2b/v2c dokunulmadı; raft_pack + build_sft_v2b yardımcıları import ile reuse.

**🔴 KARAR — recipe Q3 override (veri-doğrulamalı, kullanıcı onaylı):** recipe Q3 sertliği **SORU-örtüşme MAX**'a çıpalıyordu. İlk kod bunu uyguladı; ölçtüm → eval M2 ile örtüşmüyor:
- Bizim `ov_gold` = kardeş↔gold-kaynak Jaccard = eval M2 `_overlap` ile **AYNI metrik** (build_eval_sets.py:138).
- Soru-çıpası pool: `ov_gold` med=0.047, eval-med(0.123) üstü kapsama **%6.6** → eğitim-negatifi eval'den KOLAY = **v2c Bulgu-2 hatasının başka eksende tekrarı.**
- **Düzeltme:** `pick_hard_neighbor` → EVAL-AYNASI: aynı kanunun tüm kardeşleri içinden gold-kaynağa MAX Jaccard (eval:138 ile birebir). Pencere yok.

**Sonuç (eval-aynası, n=19284):**
| Dağılım | med | p90 | eval-med üstü kapsama |
|---|---|---|---|
| Eval M2 `_overlap` (n=35) | 0.123 | 0.253 | — |
| v3 `ov_gold` (n=19284) | **0.141** | **0.277** | **%66.3** (önce %6.6) |

Dağılımlar artık özdeş (v3 hafif daha zor). **Bulgu-2 hatası ölçülebilir eksende kapandı.**

**Geçerlilik ekseni yeniden konumlandı:** ov_gold artık SERTLİK ekseni (yüksek=zor=istenen). "Yanlış madde soruyu gerçekten cevaplıyor mu?" (geçerlilik) lexical ile ölçülemez → **semantik judge**'a taşındı (ADIM 4). `judge_flag='hi_overlap'` (ov_gold>0.35, 1192 aday) = judge-önceliği (kazara-cevaplama şüphesi en yüksek). Gözle doğrulama: hi_overlap örnekleri (CMK 140 teknik-izleme vs CMK 135 iletişim-tespiti; TCK 197 sahte-para vs TCK 199 kıymetli-damga) yüksek-örtüşmeli ama farklı hüküm → çekimser hâlâ doğru → **yüksek lexical örtüşme ≠ gerçekten cevaplıyor**, judge'a taşıma kararı doğrulandı.

**Kaynak:** `scripts/build_sft_v3.py` · `data/processed/sft_v3/packed_v3.jsonl` (seed 3407) · kıyas eval `data/eval/trap.jsonl`.
**Paper eşleme:** Bulgu-2 (eğitim-eval sertlik uyumsuzluğu) = K3'ün iki-sebepli rafinasyonu; eval-aynası düzeltmesi = "hard-negative dağılımını eval ile eşle" metodoloji katkısı. Recipe Q3 çelişkisi v3/recipe.md'de bayraklandı → ADR-0015'te formalize edilecek.

---

