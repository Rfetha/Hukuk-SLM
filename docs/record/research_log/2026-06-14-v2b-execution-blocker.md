### 2026-06-14 — v2b execution: compute'suz blocker'lar temizlendi (kod + doğrulama)
§9 execution sırasındaki benim-tarafımdaki tüm işler yazıldı + GERÇEK/sentetik veriyle doğrulandı (GPU yok):
- **`scripts/raft_pack.py`** (YENİ, ortak): RAFT context paketleme — gold + hard-negative distractor (aynı kanun komşu madde). Eval ↔ eğitim AYNI modül + AYNI sistem promptu (`SYSTEM_PROMPT_RAG_MULTI`) → dağılım eşleşir (ADR-0013).
- **A2/A3** `gen_eval_grounded.py`: `--distractors N` (M1, gold+N distractor) + `--empty-context` (M3, E-set boş bağlam). detail'e `context_shown`+`mode` eklendi. *(Tam gen GPU ister; paketleme B1 ile doğrulandı.)*
- **A4** `scripts/score_register.py` (YENİ): uzman-vs-vatandaş leksik proxy. Doğrulama: uzman cevap→1.00 (E7/C0), vatandaş→0.00 (E0/C7). Kanonik=LLM-judge (TODO).
- **B1** `scripts/build_sft_v2b.py` (YENİ): `pack` (Adım1) + `assemble` (Adım3/4/5). **Koştu:** 19.305 tohum → 15.458 grounded / 3.847 abstain (P=0.8 ✓), grounded=gold+4distractor gold-içinde, abstain=gold-çıkarılmış. Kapı testi: 4 sentetik→2 geçti/2 elendi (kötü-quote + uydurma-abstain doğru elendi).
- **B2** `scripts/gen_v2b_answers.py` (YENİ): teacher-LLM (grounded→gpt-4o-mini CoT+verbatim-quote+atıf, abstain→şablon bedava). abstain-yolu + assemble zinciri doğrulandı. **Koşmak=kullanıcı** (OPENAI_API_KEY, ~15K çağrı).
- Artefakt: `data/processed/sft_v2b/packed.jsonl` (19.305, B1 çıktısı). Sentetik test dosyaları temizlendi.
**Kalan (yalnız compute/kullanıcı):** B2 koş (API) → assemble → C1 Modal A100 eğit → D canon ölç. Kod tarafı %100 hazır.

