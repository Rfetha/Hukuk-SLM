# DEVİR NOTU — 2026-07-17 · TEZ YENİDEN ÇERÇEVELENDİ → spec yazıldı, doküman hizalaması GO bekliyor

> **Bu dosya = sabit eksen / canlı devir notu.** Yalnız GÜNCEL durum + sıradaki somut adım.
> Geçmiş anlatı → `docs/record/research_log/README.md` · Kararlar → `docs/adr/` · Görevler → `TODO.md`.

## 🎯 TEK CÜMLE
Proje **içeri dönük** ("FT base'i geçiyor mu?") olmaktan çıkıp **dışarı dönük** hale getirildi:
*dar bir domainde (TR hukuku) SLM+harness, kapalı ticari modellerin dağıtım sınıfına
**maliyet-normalize paritede** ne kadar yaklaşır — ve bunun ne kadarını FT, ne kadarını harness sağlar?*
v0→v3 = bu tezin **proof-of-concept**'i (çöpe gitmiyor, FT kolu oluyor).

## 📌 OTORİTE BELGE
**`docs/superpowers/specs/2026-07-17-tez-cercevesi-design.md`** (13 bölüm). Bu devir notu onun özeti.
Commit'ler: `14d22e3` (spec) + `863070e` (revizyon). **Durum: kullanıcı ONAY AŞAMASINDA — GO öncesi soruları var.**

## 🧭 KİLİTLİ KARARLAR (spec'ten)
- **Ana iddia:** maliyet-normalize parite (kalite × maliyet Pareto). Cümle: *"bu maliyetle, buraya kadar."*
- **Rakipler = kapalı ticari, dağıtım sınıfı:** Gemini 3 Flash · Claude Sonnet · GPT-5-mini.
  **Tavan referansı** (rakip DEĞİL, grafikte tek çizgi): Opus / Gemini 3.5 Pro. Nemotron kapsam dışı.
- **Base = Gemma 4 12B QAT — KESİN.** Qwen geçişi + çok-base kolu İKİSİ DE düştü. Düşük-spec derdi
  base değil KV-cache → TurboQuant kolu. Dış geçerlilik = **kapatılmayan sınır** (dürüst limitations).
- **Harness = retriever + Bedesten atıf-doğrulayıcı + red kapısı.** Graph-RAG KESİN dışarıda (future work).
- **8GB = soft gate** (≤8GB tercih, aşan config'ler kayıpla raporlanır), sert kısıt değil.
- **Rakip inference = OpenRouter** (tek anahtar, `base_url`, mevcut `OpenAI()` uyumlu). Key kullanıcıda VAR.
- **Katmanlı kapsam:** her katman tek başına savunulabilir tez. HPC (TÜBİTAK ULAKBİM → MareNostrum5)
  YÜKSELTEÇ, bağımlılık değil. HPC sübvansiyonu maliyet iddiasından İZOLE (GPU-saat piyasa fiyatı). CPT = non-goal.

## 🔬 DENEY IZGARASI (2 boyut: özne × harness)
|  | harness yok | harness var |
|---|---|---|
| **Rakipler** | A | **B** |
| **Bizim FT** (v3/v4) | C | **D** |
| **base** | (mevcut) | **E** ← tezin ana ablasyonu |

- Adil kıyas = **D vs B** (rakip + AYNI harness). "D>A" değersiz (harness'ı sadece kendine verme).
- **Mecellem** = ızgara dışı "açık referans" (yeni koşu YOK). **Tavan** = grafik referans çizgisi.
- Adalet kuralı: harness tüm öznelere BİREBİR aynı uygulanır.

## 🚦 KAPILAR (ön-kayıtlı, eşikler veriden ÖNCE yazıldı)
- **KAPI 1** (rakip baseline sonrası): maks(rakip M2) ≥0.90 → boşluk yok, v4 gereksiz · ≤0.80 → boşluk gerçek, v4 haklı · gri → ood'a bak. *(Referans: base M2=0.704, v3=0.593.)*
- **KAPI 2** (harness ablasyonu, İKİ BOYUTLU — bkz. NOT): harness'lı marj (D vs E) **VE** base-only marj (v4-çıplak vs C). İkisinden biri anlamlıysa FT haklı.
- **KAPI 3** (v4 git/gitme): Kapı1="gerçek" ∧ Kapı2="değer katıyor" → v4 koşar; yoksa koşulmaz (tez zaten tam).

## ⚙️ v4 RECIPE — DEĞİŞMİYOR, rolü değişiyor
- Recipe `docs/record/v4/recipe.md` **KİLİTLİ kalır** (DTA 2-kadran, gold-absent sweep 0.3/0.4/0.5, v2b-continuation). Teknik gövde yeni hedefle çelişmiyor.
- **Yeni rol:** v4 = harness'ın deterministik olarak çözemediği **semantik answerability** katmanı
  (atıfsız halüsinasyon + base-only dağıtım güvenliği). "M2b'yi düzelt" → "harness'a ortogonal 2. savunma katmanı."
- Eskiden zorunlu Faz-1-kapanışı; şimdi **koşullu** (Kapı 1∧2). Kapı-sonrası recipe hedef tablosuna
  "rakip-lider" + "harness-sonrası" sütunları eklenecek (ŞİMDİ değil, ölçüm gelince).

## ➡️ SIRADAKİ İŞ (GO bekliyor)
**1. Doküman hizalaması** (kullanıcı "tüm docları işle" dedi — GO öncesi sorularını bekliyoruz). Spec §10'daki 7 çelişki + 4 yeni ADR:
   - `CLAUDE.md`: faz-sırası istisnası (harness dilimi teze dahil, graph hariç) · 8GB soft-gate · OCR gerekçe-kayması düzelt
   - `VISION.md`: birincil katkı = parite+iş bölümü (benchmark=altyapı) · multimodal gerekçe-kayması (satır 35)
   - `TEKNIK_PLAN.md:192`: ADR-0003'e hizala (multimodal gerekçe değil)
   - Yeni ADR'ler: tez-çerçevesi · base-sabit+limitations · faz-sırası-istisnası · rakip-seti
   - Sunum (`docs/sunum/`): Faz 3 OCR vaatlerini gerçekle hizala (OmniDocBench 0.164, OCRTurk)
**2. Kapı 1 koşumu** (doküman sonrası): OpenRouter kur → rakipleri mevcut CANON'da çıplak ölç → M2/ood. ~$5. **⚠️ REGEX KALİBRASYONU ZORUNLU ÖN-ADIM** (spec §6.1: `rejection_exact` Gemma'ya göre yazılı, rakip reddini eksik sayar → bizim lehimize kayar → hiçbir sayı öncesinde raporlanmaz).
   - **Hangi sayı nereye (netleştirme — 2026-07-18):** KAPI 1 = YALNIZ rakipleri ölç (Gemini 3 Flash · Claude Sonnet · GPT-5-mini). Bizim taraf ZATEN ölçülü (`SCORECARD.md` = base·v2b·v2c·v3) — yeniden koşulmaz. **v1/v0 aday DEĞİL** (eski protokol / çökmüş = negatif bulgu). **v4 kapıdan SONRA** gelir (KAPI 3), aynı batch'te değil. **gpt-4o-mini = HAKEM** (yarışmacı değil, her turda kalır).
   - **Sunum kartını doldur (`docs/sunum/` sf14 "Tam Karşılaştırma"):** rakip sütunları (Gemini/Sonnet/GPT-5-mini) hazır & boş ("KAPI 1 — ölçülecek"). Sayı gelince → `scratchpad/gen_deck.js` sf14 bloğu: `COLS[]` rakip girdilerine `vi` ver + `rows[].[3]`'e rakip skorlarını ekle → `node gen_deck.js` → LibreOffice ile PDF. Kart zaten `heat()` ile otomatik renklendirir.

## 🚦 STANDING KURALLAR (değişmedi)
- **Para-kapıları (onaysız KOŞMA):** Modal eğitim · GPT-judge scoring · **YENİ: OpenRouter rakip inference.**
- **OPENAI_API_KEY / OPENROUTER_API_KEY** `.env`'de — **asla echo etme.** venv: `source ~/code/global_venv/bin/activate`.
- **v2b/v2c/v3 ağırlıklarına dokunma.** `data/` + `outputs/eval` gitignored → script'ten üret.
- Eğitim = Modal A100 · eval generation = lokal RTX 5070.

## 📁 ELDE VAR (çöpe gitmeyen altyapı)
- **Hakem:** `judge_agreement.py` (cross-judge κ Cohen + Pearson + spot-check) · `rejection_exact` hakemsiz (score_abstention.py:40-51) · **59 summary** birikmiş.
- **Eval:** 6-mod CANON (`build_eval_sets.py`, `bench_scorecard.py`, 5× `score_*.py`) · SCORECARD.md birleşik tablo.
- **Harness tohumu:** Bedesten kontrat (`docs/BEDESTEN_API.md`) + probe (`bedesten_probe.py`) · `raft_pack.py` (retriever'ı simüle ediyor, gerçeği kurulacak).
- **FT hattı:** v2b→v3 adaptörleri (`outputs/`) + train/gen script'leri · v4 execution planı (`docs/superpowers/plans/2026-07-06-v4-execution.md`).

## v3 turu (önceki durum, referans)
Otorite: ADR-0015 + research_log #32 · SCORECARD.md. v3 KISMİ: M1↑0.881, M5↓0.075 (iyi) ama M2=0.593 base-altı + M2b=0.529 regresyon. Kök: "en ilgili kaynağı SEÇ" refleksi → abstention tek beceri değil AİLE.
