## 2026-07-04 · v3 ADIM 2-6 — rejected harvest tasarımı + FRAMING keşfi + offline pipeline

**🔴 Bulgu-3 (FRAMING, kritik — eval M2 = ORACLE):** rejected üretimi için v2b'yi zor trap'lerde koşturdum. İlk kurulum RAG_MULTI çok-kaynak framing → v2b **%85 çekindi** (fab 0.15). Eval M2 detayı (`outputs/eval/bench_m2_v2b_detail.jsonl` `mode="oracle"`) okununca sebep çıktı: **eval M2 = ORACLE tek-kaynak framing** (SYSTEM_PROMPT_RAG "çekimser kal" DEMEZ + "KAYNAK MADDE:" tek yanlış madde), RAG_MULTI ("ilgili yoksa reddet" der) DEĞİL. Oracle framing'e geçince v2b **fab=0.79-0.875** (eval M2 0.654 ile aynı yön). **Recipe Q8 zaten "eval M2 oracle yapısına eş" diyordu** — ADIM 1 implementasyonum yanlışlıkla RAG_MULTI kurmuştu.
- **Sonuç:** v3 abstain-çiftleri (chosen+rejected+prompt) ORACLE framing kullanır (eval M2 hedefi). grounding-replay RAG_MULTI kalır (M1 sınavı RAG_MULTI). Karışık framing bilinçli — her çift kendi sınav-moduna eşlenir.
- **Paper notu:** train/eval FRAMING uyumsuzluğu = v2b'nin zayıf M2'sinin (0.346) muhtemel ek sebebi (RAG_MULTI eğitildi, oracle test edildi). Bulgu-3, K3'ün üçüncü boyutu.

**Bulgu-4 (v2b fab oranı ölçüldü, K3 funnel):** eval-aynası ORACLE zor-trap'te v2b fabrikasyon oranı ≈ **0.79** (n=24 batch smoke) / **0.875** (n=8 tekil). Yani v2b "makul-komşu yanlış madde + oracle framing"de çoğunlukla uyduruyor → ORPO rejected havuzu bol. Kaynak: `scripts/gen_v3_rejected.py`.

**Hız duvarı + mojibake bug'ı (mühendislik):** lokal RTX 5070'te 12B-4bit greedy ~**30s/örnek**, **batching KIRMADI** (decode bandwidth-bound; FA2 bozuk→Xformers). 1500 fab lokal ≈ 10+ saat → **Modal A100'e taşındı** (kullanıcı onaylı, inference ~$2-4). Ek bug: **batched left-pad `pad_token=eos` baş-token mojibake** ("Eğer"→"트에ğer", batch=8'de %26). Fix: `pad_token_id=<pad>(0)` (Gemma pad≠eos). Kaynak/fix: `gen_v3_rejected.py::generate_batch`.

**Modal erişim engeli (durum):** 2026-07-03/04 gecesi Modal HEM lokal Bash HEM kullanıcı `!` shell'inden erişilemedi ("Could not connect to the Modal server"; genel internet de HTTP 000). Harvest başlatılamadı → ağ geri gelince tekrar denenecek (handoff'ta komutlar). Kod hazır.

**Offline pipeline kuruldu (ADIM 3/5/6, $0, lokal):**
- **ADIM 3** `gen_v3_chosen.py` → `chosen.jsonl` (19284 muhakemeli-red, oracle-uyumlu, yanlış-madde konusunu adlandırır, gate_fail=0, med 31 kelime ≈ fabrikasyon uzunluğu).
- **ADIM 5** `build_v3_devset.py` → `dev.jsonl` (80 held-out, ov_gold band [0.12,0.35]=eval M2 dağılımı, 239 eval-trap sızıntısı elendi, 9 kanun). dev id'leri eğitimden çıkarılır.
- **ADIM 6a** `build_orpo_v3.py` → `train/validation.jsonl` (TRL conversational-preference {prompt,chosen,rejected,is_pref}; abstain-çifti is_pref=1 ORACLE + grounding-replay is_pref=0 RAG_MULTI placeholder-rejected; deterministik interleave). Smoke fixture ile uçtan uca test edildi.
- **ADIM 6b** `train_orpo.py` `MaskedORPOTrainer(ORPOTrainer)` — TRL 0.24 kaynak-doğrulamalı: `get_batch_loss_metrics` override, OR-agregasyonu `torch.where(is_pref, losses, 0)` NaN-safe maskeli (`loss=policy_nll_loss−or_masked_mean`). base=v2b PeftModel is_trainable (continuation). Unsloth `PatchDPOTrainer()`.
- **ADIM 6f** `modal_train.py::{harvest_rejected/spawn_harvest, train_orpo/spawn_v3}` entrypoint'leri.
- **ADIM 6E format-denetimi (geri bildirim-7, offline GEÇTİ):** cache'li Gemma tokenizer ile paketlenmiş örnek decode → chat-template doğru, abstain=oracle (`KAYNAK MADDE:`), grounding=RAG_MULTI (`KAYNAKLAR:`), is_pref satırda korunuyor (1/0). ✅

**Açık doğrulama (ADIM 7 Modal smoke YAPACAK):** (a) v2b-continuation (PeftModel is_trainable) Unsloth+ORPO'da çalışıyor mu; (b) is_pref collator else-dalından list olarak geliyor mu; (c) OOM/loss/NaN. Offline sadece syntax+tasarım doğru.

**Kaynak:** `scripts/{gen_v3_rejected,gen_v3_chosen,build_v3_devset,build_orpo_v3,train_orpo}.py` · `modal_train.py` · `data/processed/sft_v3/{chosen,dev}.jsonl` · smoke fixture `rejected_{batchtest,oracle_smoke}.jsonl`. Detaylı resume planı: v3/recipe.md §HANDOFF.

---

