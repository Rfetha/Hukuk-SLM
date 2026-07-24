# TODO — yeni hat

> Kaynak: **[`TASARIM.md`](TASARIM.md)** (otorite) · kararlar: **ADR-0027**
> Sıra kapılara bağlı — bir kapı kararı gelmeden ona bağlı iş başlamaz.
> Tamamlananlar `docs/record/research_log/`'a girdi olarak taşınır, buradan silinir.

> ### 📍 Bu belge **harita**, yürütme planı değil
>
> Aktif iş → **[`sprint1.md`](sprint1.md)**: ilk FT koşusunun (`τ_grounding`) checkpoint zinciri,
> komutlarıyla ve her adımda 12B hattından gelen *"burada şu patlar"* uyarılarıyla.
> Buradaki maddeler **ne yapılacağını**, sprint belgesi **hangi sırayla ve neye dikkat ederek**
> yapılacağını söyler.
>
> | sprint | kapsam | koşan FT | TODO bölümleri |
> | :--- | :--- | :--- | :--- |
> | **[1](sprint1.md)** ← *aktif* | **Faz A** hazırlık (base kapısı · base baseline + Kapı 0 · veri) → **Faz B** ilk FT | **FT-1** | §0 · §1 (kısmi) · §2 (kısmi) · §3 (ilk hücre) |
> | 2 | `rejected` hasat · kalan kollar · tabanlar · DEV havuzu · regex kalibrasyonu | **FT-2 … FT-6** | §1 · §2 |
> | 3 | merge + 7 hücreli kafes → **🎯 hedef model doğuyor** + iç iddia kararı | — *(merge bedava)* | §3 |
> | 4 | harness (retriever · graf · doğrulayıcı · kapı) + Kapı 3 — **2-3 ile paralel yürüyebilir** | — *(eğitim yok)* | §4 · §6 |
> | 5 | dış parite matrisi + Kapı 1/2 + eşdeğerlik + başabaş N\* + kapanış ölçümleri (eval≠dağıtım · gerçek VRAM) — **tez burada biter** | — *(rakipler API)* | §5 · §6 |
>
> ### FT sıralaması — hangi koşu nerede
>
> **TEK boyut noktası (ADR-0028).** Tüm ızgara tek base üzerinde koşar. Daha büyük bir modelin
> ince-ayarı **koşullu bir opsiyon**, planlanmış adım değil — ancak proje **ürüne dönüşürse**,
> **destek/kaynak gelirse** ya da **makale büyürse** gündeme gelir. Takvimde yeri yok.
>
> | # | ne | sprint | önkoşulu |
> | :--- | :--- | :---: | :--- |
> | **FT-1** | `τ_grounding` (RAFT-SFT) | **1** | Faz A'nın tamamı |
> | **FT-2** | `τ_abstention` (ORPO) | 2 | `rejected` yeniden hasat *(çıkarım koşusu, FT değil)* |
> | **FT-3** | `τ_register` (SFT) | 2 | ⚠️ **koşullu** — Kapı 0 izin verirse |
> | **FT-4** | Taban A: tek-aşamalı **karışık** SFT | 2 | — |
> | **FT-5** | Taban B: **ardışık** SFT, aşama 1 | 2 | — |
> | **FT-6** | Taban B: **ardışık** SFT, aşama 2 | 2 | FT-5 |
>
> **Toplam 6 koşu** — Kapı 0 `τ_register`'ı düşürürse **5** (FT-3 düşer). Hepsi **tek base'de.**
> Sprint 3-4-5'te **hiç eğitim yok**: merge bir ağırlık işlemi (bedel yalnız eval'de), harness
> deterministik, rakipler API. **Bütün eğitim yükü Sprint 1-2'de.**
>
> ⚠️ **Tek noktanın bedeli — üçü de limitations'a yazılır (ADR-0028):**
> (a) **dış geçerlilik açığı kapanmıyor** — *"bulgular bu base'e mi özgü?"* cevapsız kalır;
> (b) **kapasite sorusu ölçülemez** — *"çatışan beceriler kapasiteyle azalıyor mu?"*;
> (c) **ADR-0018'in eğri şartı karşılanmıyor** — tek işaretli nokta var, ölçülmüş eğri yok.
> *Aynı-aile kuralı iptal değil ertelendi:* opsiyon kullanılacağı gün aile ve boyut birlikte
> değişmemeli, yoksa fark hiçbirine atfedilemez (ADR-0027'de hazır reçete olarak duruyor).
>
> **Hedef model Sprint 3'ün sonunda doğar** (kazanan merge konfigürasyonu). Sprint 4-5 o modeli
> inşa etmez, **hakkındaki iddiayı kanıtlar.** Kaba takvim: seri ~9-13 hafta, Sprint 4 paralelken
> **~7-10 hafta** — en oynak kalem Sprint 1'deki Unsloth/sm_120 ortam borcu.

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

### FT hedefleri — ön-kayıt 🔒

> **Veriyi görmeden yazıldı.** Sonradan yazılırsa çıkan sonuç rasyonalize edilir.
> Sağdaki 12B sayıları **kalibrasyon çıpası**, hedef değil.

**Toplam FT bütçesi: 6 koşu** — 3 kol + karışık taban + ardışık tabanın 2 aşaması, hepsi
**tek boyut noktasında** (ADR-0028). Kapı 0 `τ_register`'ı düşürürse **5**.
**Merge'in eğitim maliyeti sıfır** — 7 hücrenin tamamı bu koşulardan türer.
`rejected` hasadı eğitim değil, tek çıkarım koşusu.

| kol | ne katacak | riski | 12B kanıtı |
| :--- | :--- | :--- | :--- |
| **`τ_grounding`** (RAFT-SFT) | **M1 ↑↑** gürültüde kaynağa sadakat + coverage · **M2b ↑** (%20 abstain dilimi tam bu şekli öğretiyor) · M4/M3 korunur | **M2 ↓↓** — near-miss tek-kaynak şekli veride **hiç yok** | M1 0.879→**0.904** (cov %47,5→**%72,5**) · M2b **0.96** · M2 0.786→**0.346** |
| **`τ_abstention`** (ORPO) | **M2 ↑↑** near-miss ayrımı — tek gerçek hedefi | **M2b ↓↓** *forced-source-selection*: "en ilgilisini SEÇ" refleksi, doğrusu olmayan yerde en yakın distractor'ı seçtiriyor | v3: M2 0.346→**0.593** · M1 0.737→**0.881** · **M2b 0.96→0.529** |
| **`τ_register`** (SFT) | register ↑ — yalnız base zayıfsa | **abstention ↓↓** — bu setin *cevapları* v1'de reddi **0.000**'a indirmişti | Kapı 0 bu kolu tamamen düşürebilir |

⚠️ **`τ_abstention` için dürüst belirsizlik:** 12B'deki v3 **ham base'den değil, v2b'nin üstünden**
devam etti; M1'i yükseltmesi orada v2b'nin grounding'inin taşınmasından geliyordu. **Bağımsız bir
task-vector olarak o etki olmayabilir.** Ölçülecek.

**Merge beklentisi (asıl iddia):** `τg + τa` hücresi paranın olduğu yer. Merge çatışmayı çözerse
M1 **yüksek** ∧ M2 **yüksek** ∧ M2b **korunmuş** — 12B'de **hiçbir tur** bu üçünü aynı anda
tutturamadı. Çözemezse biri diğerini bastırır ve ardışık SFT'den farkı çıkmaz.
`+ τr` ağırlıkla register getirir, abstention'ı aşağı çekme riski taşır.

**Ne öğretmiyorlar (üçü de):** hukuk **bilgisi** — SFT bilgi gömmez. 12B kanıtı: M4 oracle 0.975 vs
M5 kör 0.175 = **%80 uçurum.** Güncellik kütüphanede, ağırlıkta değil.

---

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
