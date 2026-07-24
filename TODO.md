# TODO — yeni hat

> Kaynak: **[`TASARIM.md`](TASARIM.md)** (otorite) · kararlar: **ADR-0027**
> Sıra kapılara bağlı — bir kapı kararı gelmeden ona bağlı iş başlamaz.
> Tamamlananlar `docs/record/research_log/`'a girdi olarak taşınır, buradan silinir.

---

## 0 — Base doğrulama kapısı 🔒 *her şeyin önünde*

Hiçbir eğitim koşusu bu altı madde geçmeden başlamaz (`TASARIM.md` §8).

- [ ] Aday base seç (çalışma varsayımı: ~4B sınıfı instruct)
- [ ] **llama.cpp mimari desteği** doğrula — hibrit dikkat katmanları varsa destek + KV matematiği farklı (ADR-0025 artık bir *base seçim kriteri*)
- [ ] **Şablon render'ını GÖZLE doğrula** — `research_log` #38: minja bir dalı yanlış render etti, model durmadı, bir CANON koşusu **sessizce** çöpe gitti
- [ ] Turn işaretlerini assert et — `train_sft.py --user-part/--assistant-part` render'a karşı kontrol ediyor; smoke ile teyit
- [ ] Unsloth + sm_120 ortamını onar → `requirements.lock.txt` yeniden kur (açık borç: `libnvJitLink.so.13`)
- [ ] Kuantizasyon yolunu doğrula — QAT checkpoint'i yoksa **Q4_K_M**; `setup_llamacpp.sh` `PURE=0` ile
- [ ] Lisansı kaydet (saf Apache-2.0 mı, ek kullanım politikası var mı) → attribution + limitations

## 1 — Ölçüm zemini

- [ ] **DEV havuzu üret** — CANON protokolünde yeni öğeler. `eval/canon/` (40+35) **TEST**, dokunulmaz, nihai raporda bir kez görülür
- [ ] DEV hedef n'ini belirle — eşdeğerlik için güç analizi (açık soru)
- [ ] **Regex kalibrasyonu** — red-tespit regex'ini her rakip ailesinde ölç, model-agnostik hale getir, ~30 çıktı elle spot-check. ⚠️ **Bu yapılmadan hiçbir sayı raporlanmaz** (kalibre edilmemiş regex skorları bizim lehimize kaydırır)
- [ ] Hakem panelinin üç ailesini seç (aile-dışlama ile birlikte çözülmeli)
- [ ] Rakip model adlarını **tarihli snapshot'a** pinle
- [ ] `$/sorgu` + latency + throughput + GPU-saat enstrümantasyonu — bugün yalnız `judge_cost_usd` var (*not verme* maliyeti, *servis* maliyeti değil)

## 2 — Kollar

- [ ] **Kapı 0:** yeni base'in register-proxy'sini ölç → `τ_register` kolu gerekli mi? (12B'de 1.000'e oturmuştu)
- [ ] `τ_abstention` için `rejected` havuzunu **yeni base ile yeniden hasat et** (`gen_v3_rejected.py` — tek çıkarım koşusu, eğitim değil)
- [ ] `τ_grounding` eğit (RAFT) — ham base'den
- [ ] `τ_abstention` eğit (ORPO) — ham base'den
- [ ] `τ_register` eğit — ham base'den, *Kapı 0 izin verirse*
- [ ] Taban A: tek-aşamalı **karışık** SFT
- [ ] Taban B: **ardışık** SFT (referans belgenin orijinal kurgusu — 2 aşama)

## 3 — Merge + iç ablasyon

- [ ] ΔW materyalizasyonu + **akış hâlinde k-yollu merge** (host RAM, bf16, tensör tensör)
- [ ] Merge hiperparametrelerini **DEV'de** tara (λ · TIES density · DARE drop-rate)
- [ ] **7 hücreli kafesi** CANON'da koş — **harness KAPALI**
- [ ] Tabanlarla kıyas → iç iddia kararı
- [ ] Kazanan konfigürasyonu seç

## 4 — Harness

- [ ] **Korpus snapshot'ını dondur + sha256 pinle** (retriever *ve* doğrulayıcı aynı snapshot)
- [ ] Yapısal graf parser'ı: hiyerarşi + atıf ağı + mülga/değişik zincirleri → **NetworkX/GraphML**
- [ ] TR embedding modeli seç — ⚠️ lisans + **EDA doğrulaması şart**
- [ ] Hibrit retriever (BM25 + embedding + 1-2 hop graf genişletme)
- [ ] Bedesten atıf doğrulayıcı
- [ ] Red kapısı — eşik kararı açık (tüm atıflar mı, çoğunluk mu? ablasyon adayı)
- [ ] Harness'ı **rakiplere de** bağla (adalet kuralı, pazarlıksız)

## 5 — Dış parite matrisi

- [ ] **Kapı 1:** rakip baseline'ı çıplak ölç → en iyi rakibin M2 + ood dilimi → boşluk gerçek mi?
- [ ] A/B/C/D/E hücrelerini koş
- [ ] **Kapı 2:** D vs E → iş bölümü doğrulandı mı, yoksa scaffolding FT'yi mi ikame ediyor?
- [ ] Eşdeğerlik testi (veri toplandıktan sonra, **bedava hesap**)
- [ ] Başabaş noktası N\* + Pareto grafiği
- [ ] Dış geçerlilik dilimi: tanınır TR hukuk sınav seti, kapalı-kitap (**hedef değil**, M5 kategorisi) — lisansı önce doğrula

## 6 — Kapılı kollar

- [ ] **Kapı 3:** hibrit kavram katmanı — yalnız getirme ölçümü (recall@k + MRR, kavram kenarı açık/kapalı). Geçmezse "katkı yok" negatif bulgusu
- [ ] LightRAG/GraphML interop iddiasını **doğrula** (EDA kuralı) — kol açılırsa ilk adım
- [ ] **Kapı 4:** karşıtlık noktası (~8-9B) — yalnız kazanan konfigürasyon
- [ ] Eval ≠ dağıtım hizalaması: en az bir kez aynı CANON'da kuantize vs bf16
- [ ] Gerçek donanımda VRAM/ayak izi ölçümü (bugünkü sabit kalemler **tahmin**)

---

## Kayıt hijyeni (sürekli)

- [ ] Her anlamlı deney/bulgu → `docs/record/research_log/` girdisi, **aynı gün**
- [ ] Her büyük karar → yeni ADR (eskiyi silme, süperseded işaretle)
- [ ] Sayılar kaynaklı: metrik + n + hakem + seed + çıktı dosyası

## Açık sorular (`TASARIM.md` §13)

TR embedding modeli · red kapısı eşiği · DEV hedef n'i · zamansal eksen CANON'a girsin mi ·
hakem panelinin üçüncü ailesi · içtihat grafa girsin mi · yinelemeli merge ekstra hücre olsun mu
