# TODO — yeni hat

> Kaynak: **[`TASARIM.md`](TASARIM.md)** (otorite) · kararlar: **ADR-0027**
> Sıra kapılara bağlı — bir kapı kararı gelmeden ona bağlı iş başlamaz.
> Tamamlananlar `docs/record/research_log/`'a girdi olarak taşınır, buradan silinir.

> ### 📍 Bu belge **harita**, yürütme planı değil
>
> Buradaki maddeler **ne yapılacağını**, sprint belgesi **hangi sırayla ve neye dikkat ederek**
> yapılacağını söyler. Her koşudan önce ⭐ [`docs/record/yurutme-tuzaklari.md`](docs/record/yurutme-tuzaklari.md)
> — *"hata vermeden yanlış sonuç üreten"* kalıpların tek listesi.
>
> **Aktif yürütme belgesi: ⭐ [`sprint2.md`](sprint2.md)** (yazıldı 2026-07-29).
> Sprint 1 kapandı; [`sprint1.md`](sprint1.md) 🔒 arşiv.
>
> | sprint | kapsam | koşan FT | TODO bölümleri |
> | :--- | :--- | :--- | :--- |
> | **[1](sprint1.md)** ✅ **KAPANDI** | **Faz A** hazırlık (base kapısı · **DEV havuzu** · base baseline + Kapı 0 · veri) → **Faz B** ilk FT · **+ CP7 Gemini 3.1 Flash-Lite erken önizleme** | **FT-1** ✅ | §0 · §1 (kısmi) · §2 (kısmi) · §3 (ilk hücre) |
> | **[2](sprint2.md)** ← *aktif* | ✅ düşünce modu (CP0 → **thinking AÇIK, bütçeli**, ADR-0043) · **çıpaların yeniden koşulması (CP0.9)** · hakem düzeltmesi · `rejected` hasat · `τ_a` + **ARA KAPI** · tabanlar | **FT-2 · FT-4 · FT-5/6** | §1 · §2 |
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
> | ~~**FT-3**~~ | ~~`τ_register` (SFT)~~ | ~~2~~ | ❌ **DÜŞTÜ** — Kapı 0 (#39) izin vermedi (register 0.96-0.98) |
> | **FT-4** | Taban A: tek-aşamalı **karışık** SFT | 2 | — |
> | **FT-5** | Taban B: **ardışık** SFT, aşama 1 | 2 | — |
> | **FT-6** | Taban B: **ardışık** SFT, aşama 2 | 2 | FT-5 |
>
> **Toplam ~~6~~ → 5 koşu** — Kapı 0 (#39) `τ_register`'ı (FT-3) **düşürdü**. Hepsi **tek base'de.**
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

## 0 — Base doğrulama kapısı 🔒 *her şeyin önünde* — ✅ **6/6 GEÇTİ (2026-07-24, #39, ADR-0030)**

Hiçbir eğitim koşusu bu altı madde geçmeden başlamaz (`TASARIM.md` §8).
**Base = `Qwen/Qwen3.5-4B`** (sha `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`), **saf Apache-2.0**.
⚠️ HF'de `-Instruct` varyantı **yok** — instruct'ın adı düz `Qwen/Qwen3.5-4B`.

- [x] Aday base seç → **`Qwen/Qwen3.5-4B`** (~4B sınıfı instruct, ADR-0030)
- [x] **llama.cpp mimari desteği** doğrula — yükleniyor, GGUF `q35-4b-q4_k_m.gguf` (2.59 GiB) üretildi (ADR-0025 artık bir *base seçim kriteri*)
- [x] **Şablon render'ını GÖZLE doğrula** — ⚠️ Qwen3.5 **düşünen model**: varsayılan modda `</think>` kapanmıyor, `content` BOŞ (HTTP 200) → boş-cevap erken patlama kapısı eklendi (ADR-0030, #39). ⚠️ **2026-07-29 güncelleme:** `--thinking off` çözümü **geri alındı** — hat `--thinking on` + **bütçeli zorunlu kapatma** (1024+512) ile koşuyor, çünkü base belirsiz modlarda `</think>`'i **hiç** kapatmıyor ve bütçe artırmak çözmüyor (ADR-0043, #42)
- [x] Turn işaretlerini assert et → `<|im_start|>user\n` / `<|im_start|>assistant\n`; model duruyor (`finish_reason=stop`)
- [x] Unsloth + sm_120 ortamını onar → çekirdek engel **LD_LIBRARY_PATH** (`libnvJitLink.so.13`) idi, `global_venv/bin/activate`'e kalıcı satır eklendi, NF4 forward doğrulandı. *(Açık kalan `causal-conv1d` derlemesi Faz B'yi bekletir, kapıyı değil.)*
- [x] Kuantizasyon yolunu doğrula → **Q4_K_M**, `PURE=0` (QAT yok), VRAM×ctx matrisi `outputs/eval/vram_stack.json`'a ölçüldü
- [x] Lisansı kaydet → **saf Apache-2.0** (ek kullanım politikası yok, Qwen3.5) → attribution + limitations

## 1 — Ölçüm zemini

> ### 🔌 Çok-model erişimi ne zaman gerekli (ADR-0029)
>
> Erişim **tek kapıdan**: `scripts/llm_client.py`. Kod **hazır ve geriye dönük uyumlu** —
> `OPENROUTER_API_KEY` yoksa bugünkü `OPENAI_API_KEY` yolu aynen çalışır, anahtar eklendiği an
> kapı OpenRouter'a döner (script değişikliği yok).
>
> | ne zaman | ne gerekir | neden o zaman |
> | :--- | :--- | :--- |
> | **Sprint 1** | tek aile (mevcut `OPENAI_API_KEY`) | CP1↔CP5 **iç kıyas**; aynı hakem iki tarafta olduğu sürece aile sayısı fark etmez. **Ama panelin üç ailesi burada seçilir** — aile-dışlama base ailesine bağlı, o da CP0'ın çıktısı |
> | **Sprint 2-3** | çok-aile · rakip erişimi | **regex kalibrasyonu** her rakip ailesinde koşar (aşağıdaki madde) + iç iddia kararı üç aileli panelle raporlanır |
> | **Sprint 5** | çok-aile · maliyet muhasebesi | dış parite matrisi; rakipler API'den |
>
> ⚠️ İki muhasebe tuzağı, ikisi de sessiz ve ikisi de **bizim lehimize** kayar:
> **(a) fiyat** — parite matematiği birincil-kaynak liste fiyatıyla yapılır, kapıya ödenen tutarla
> değil; **(b) sağlayıcı yönlendirme** — aynı model kimliği farklı upstream yığında koşabilir,
> `judge_providers` tek eleman değilse sayı tek bir servis yığınına ait değildir.

- [x] **DEV havuzu üret** ✅ (#39) — `data/eval/dev/` (80 core_hard + 70 trap), **TEST ile kesişim = 0** doğrulandı. `eval/canon/` (40+35) **TEST**, dokunulmaz, nihai raporda bir kez görülür.
      ⚠️ `build_eval_sets.py --exclude` **zorunlu**: CORE-HARD seçimi karmaşıklığa göre sıralı ve **seed'den bağımsız** → `--exclude`'suz "DEV" TEST'in kopyası/üst kümesi olur ve hata vermez. Kabul ölçütü: **kesişim = 0**
- [ ] DEV hedef n'ini belirle — eşdeğerlik için güç analizi (açık soru)
- [~] **Regex kalibrasyonu** — ✅ **kendi base'imizde YAPILDI (#39)**: `bulunmuyor` tuzağı yakalandı, `score_abstention.py` kalibre edildi, 15/15 ileri + 2/2 geri elle doğrulandı. **[ ] rakip aileleri için AÇIK** — model-agnostik hale getir, ~30 çıktı elle spot-check (**Gemini önizlemesi CP7'de ilk rakip kalibrasyonu**). ⚠️ **Bu yapılmadan hiçbir sayı raporlanmaz**
- [x] Hakem panelinin üç ailesini seç ✅ **ADR-0032**: OpenAI · Anthropic · Google (Qwen özneden **ayrık**, aile-dışlama sağlandı)
- [ ] Rakip model adlarını **tarihli snapshot'a** pinle
- [ ] `$/sorgu` + latency + throughput + GPU-saat enstrümantasyonu — bugün yalnız `judge_cost_usd` var (*not verme* maliyeti, *servis* maliyeti değil)

## 2 — Kollar

### FT hedefleri — ön-kayıt 🔒

> **Veriyi görmeden yazıldı.** Sonradan yazılırsa çıkan sonuç rasyonalize edilir.
> Sağdaki 12B sayıları **kalibrasyon çıpası**, hedef değil.

**Toplam FT bütçesi: ✅ ~~6~~ → 5 koşu** — Kapı 0 (#39) `τ_register`'ı (FT-3) **düşürdü** →
kalan: 2 kol (`τ_grounding` · `τ_abstention`) + karışık taban + ardışık tabanın 2 aşaması, hepsi
**tek boyut noktasında** (ADR-0028).
**Merge'in eğitim maliyeti sıfır** — 7 hücrenin tamamı bu koşulardan türer.
`rejected` hasadı eğitim değil, tek çıkarım koşusu.

| kol | ne katacak | riski | 12B kanıtı |
| :--- | :--- | :--- | :--- |
| **`τ_grounding`** (RAFT-SFT) | **M1 ↑↑** gürültüde kaynağa sadakat + coverage · **M2b ↑** (%20 abstain dilimi tam bu şekli öğretiyor) · M4/M3 korunur | **M2 ↓↓** — near-miss tek-kaynak şekli veride **hiç yok** | M1 0.879→**0.904** (cov %47,5→**%72,5**) · M2b **0.96** · M2 0.786→**0.346** |
| **`τ_abstention`** (ORPO) | **M2 ↑↑** near-miss ayrımı — tek gerçek hedefi | **M2b ↓↓** *forced-source-selection*: "en ilgilisini SEÇ" refleksi, doğrusu olmayan yerde en yakın distractor'ı seçtiriyor | v3: M2 0.346→**0.593** · M1 0.737→**0.881** · **M2b 0.96→0.529** |
| ~~**`τ_register`** (SFT)~~ ❌ | register ↑ — yalnız base zayıfsa | **abstention ↓↓** — bu setin *cevapları* v1'de reddi **0.000**'a indirmişti | **Kapı 0 (#39) bu kolu DÜŞÜRDÜ** — yeni base register 0.96-0.98 |

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

- [x] **Kapı 0:** ✅ **KARAR VERİLDİ (#39): `τ_register` DÜŞÜYOR** — register-proxy **0.96-0.98** (yüksek, base güçlü) → kol 3→2, kafes 7→3 hücre, **FT bütçesi 6→5** (FT-3 düşer). (12B'de de 1.000'e oturmuştu)
- [ ] `τ_abstention` için `rejected` havuzunu **yeni base ile yeniden hasat et** (`gen_v3_rejected.py` — tek çıkarım koşusu, eğitim değil)
- [ ] `τ_grounding` eğit (RAFT) — ham base'den
- [ ] `τ_abstention` eğit (ORPO) — ham base'den
- [~] ~~`τ_register` eğit~~ — ❌ **DÜŞTÜ**: Kapı 0 (#39) izin vermedi (register 0.96-0.98)
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
~~hakem panelinin üçüncü ailesi~~ **→ ÇÖZÜLDÜ ADR-0032** (OpenAI·Anthropic·Google, Qwen-ayrık) ·
içtihat grafa girsin mi · yinelemeli merge ekstra hücre olsun mu
