### 2026-06-14 — v2 plan oturumu: SaulLM okuması + SFT hedef + veri pipeline + eval matrisi (ADR-0013)
Strateji oturumu, `docs/V2_PLAN.md`'yi execute-edilebilir hale getirdi. Kararlar/çıktılar:
- **SaulLM okundu** (`knowledge/summary_saullm.md`): bilgiyi **CPT** gömdü (SFT değil) → "SFT bilgi gömmüyor" bulgumuzu doğruladı; SaulLM peer-açık-modelleri yendi, **frontier'ı değil**; replay %2 + DPO-fayda-yok bizim bulgularla uyumlu. → ağırlık-temelli bilgi = CPT yolu (bizde v2c EntiGraph).
- **Kullanıcı kararı: PLAN A** = SFT (davranış) + RAG (bilgi, sonra), CPT'siz; yön = **direkt v2b** (v2a baseline'a indi). `V2_PLAN` banner + §4.
- **SFT hedef tanımı** (`V2_PLAN §3.1/§3.2`): 4 davranış (grounding/abstention/format/correctness-koru) ↔ 4 canon ekseni; bilgi-ezber ve register-loss bilinçli DIŞARIDA. base-vs-SFT örnek senaryolar = gold-cevap şablonu.
- **HEDGE MEKANİZMASI DÜZELTİLDİ** (`V2_PLAN §5.2`): RAG-grounded model için abstention = **context-yeterliliği** (Sufficient-Context 2411.06037), **parametrik base-prob DEĞİL** (R-Tuning closed-book için). Deterministik → "hedge oranı" = **(1-P)**; base-prob İPTAL; tek knob P (~%80, ablate). *(Önceki base-prob önerisi düzeltildi.)*
- **Veri durumu:** hammadde HAZIR (40.496 madde + 19.305 soru↔gold tohumu); **v2b eğitim çiftleri ÜRETİLMEDİ** (v1 cevapları kaynaksız/vatandaş-register/CoT-quote yok → kullanılamaz). Pipeline §5.2, script `build_sft_v2b.py` (Adım1/3/4/5 deterministik) + teacher-LLM (Adım2).
- **ADR-0013 yazıldı:** canon eval v2 = **5 mod matrisi** (M1 gold+distractor [YENİ, v2b manşeti] · M2 TRAP · M3 E-set [YENİ] · M4 temiz-Oracle [referans] · M5 KÖR) + A-register ekseni. Mevcut Oracle distractor içermiyor → deployment'tan kolay; düzeltilecek. İki bilinmeyen: distractor-dağılımı (retriever'a bağlı) + register-rubriği (Muhakim çapası).
- **Execution sırası** `V2_PLAN §9` (A eval-altyapı ∥ B veri → C eğit → D ölç → E sonrası). İlk iş: A1 (✅ ADR-0013) + B1 (build script).
- **Yol haritası ufku (OPSİYON, karar değil):** SFT → RAG → (gerekirse) **RLHF/GRPO**; reward = canon-skorlayıcılar (RLVR) + Muhakim, ayrı RM gerekmez; RAG'dan sonra (deployment dağılımı). on-policy PPO forgetting-direnci = teorik artı.
**Paper-eşleme:** methodology (eval-dist=deploy-dist ilkesi, mod matrisi) + K3 (SaulLM CPT-vs-SFT ayrımı bizim bulguyu evrenselleştirir).

