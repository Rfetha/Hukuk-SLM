# `/goal` promptu — `HP` → Hat A → Hat B planı için

**Kullanım:** aşağıdaki bloğu olduğu gibi `/goal` komutuna yapıştır.
⚠️ `/goal` **4000 karakter** sınırı koyuyor; bu metin **3.936 karakter** (2026-09-07). Ayrıntı planın kendisinde:
[`2026-09-07-hp-hat-a-hat-b.md`](2026-09-07-hp-hat-a-hat-b.md) (17 görev, 89 kutucuk).

---

```
/goal Planı uygula: docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md
⭐ ÖNCE OKU: planın "Global kısıtlar" + "AÇIK KARARLAR" bölümü. 17 görev, 89 kutucuk.

🔒 SIRALAMA KİLİTLİ (insan kararı): HP → Hat A (PARALEL, $0) → Faz 3 → v0.2 → Hat B → v1.0
 FAZ 1 · HP hakem paneli (G1-4, 18 kutucuk, ~$3-5) — ÖNCE
 ⛔ G8 (indeks dağıtımı) BEKLETİLİYOR: kapsam CB_KARAR+KKY ile 8,4× büyüyecek
    (340.303 madde, indeks ~697 MB — ölçüldü) ⇒ önce mevzuat spec'inin planı,
    v0.2 GENİŞLETİLMİŞ korpusla. ⚠️ G8b (mülga) ve G8/1b (KUNYE kilidi) BEKLEMEZ.
 🆕 G8b YÜRÜRLÜK: mülga madde vatandaşa GİTMEZ + korpusa tarih damgası
     ölçüldü: mulga bayrağı VAR (2.547 madde) ama retriever KULLANMIYOR ⇒ 800 getirilen
     kaynağın 2'si mülga. Korpusta TARİH ALANI YOK. Bu eksik özellik değil, YANLIŞ CEVAP.
     ⛔ v2'ye kalan: canlı bedesten API (B6, TR IP şart) · 892→tam kapsam · tazelik boru hattı
 FAZ 2 · Hat A paketleme (G5-12, 43 kutucuk, $0, GPU yok) — HP'ye PARALEL koşabilir
 FAZ 3 · Belge katmanı (G13, 7 kutucuk, $0) → v0.2 YAYIN
 FAZ 4 · Hat B model (G14-16, 14 kutucuk, ~$7-15) → v1.0 kapısı · ⛔ HP bitmeden BAŞLAMAZ

NEREDE KALDIK: Faz 0 KAPANDI 48/48. v1.0 kapısının ÜÇ maddesi de sayıyla geçti:
kütle 0,8011 ↔ eşik 0,7225 (+5,86 p) · isabetsizlik 8/80 · M5 −6,82 p (çıpa BASE).
recall@10 0,9500 · aşırı-red 4/80 · uydurulmuş madde 0/114 — SIFIR eğitimle, aletin
BEŞ kusuru bulunarak. ADR 0063-0073 · #62 · S1·S2·S11·S13·S14·S15 kapandı.
⚠️ kapı DEV'de geçti; donmuş TEST kabul koşusu KOŞMADI ⇒ v1.0 VERİLMEDİ (ADR-0064/65).

⚡ HER GPU KOŞUSUNDAN ÖNCE: künyede `güç : ŞARJDA` DOĞRULA. Pilde GPU 180 MHz'e
kısılıyor → 80 kalem 4,8 saat ↔ şarjda ~25 dk.

🚨 BÜTÇE — ÖLÇÜLDÜ: OpenRouter $6,60 (credits 20 − usage 13,397) · Modal $29,19.
Plan ~$10-20 ⇒ HP + kapı koşusuna YETMEYEBİLİR. Duraklarda bakiyeyi YENİDEN ÖLÇ.

✅ AÇIK KARARLAR GRİLLENDİ 2026-09-07 — bloke görev 4 → 0. Üçü OLGUYLA kapandı:
 S18 ölçülen istem kanon, train_sft.py'deki ÖLÜ KOD silinir · τ_g çift-system DEĞİL
     (Qwen şablonu iki system'e TemplateError = yapısal imkânsızlık)     → G5
 S16 TEK anthropic/claude-*-sonnet* öznesi (~$0,35), GPT usulen dışarıda → G4
 S10 geçici ibare, cli.py'de TEK sabit, tui.py IMPORT eder            → G10·G12
 S8 (a) HF dataset ama G8 bekliyor · S7 yalnız merge GGUF, adaptör YOK
 S5 Wilson RAPORLANIR kapı DEĞİŞMEZ · S12 ertelendi · S9·S17 plan dışı

KRİTİK TUZAKLAR (planda tam yazılı, hepsi ölçüldü):
· HP: üretim YENİDEN KOŞULMAZ — aynı 80 cevap, farklı hakem (ADR-0017)
· AİLE DIŞLAMASI: üçlü κ YALNIZ bizim kolumuzda kurulur; Gemini öznesi Google hakemle
  notlanamaz (ADR-0032). Eksiklik değil kuralın sonucu — açıkça raporla.
· G5: istem taşındıktan sonra çıktı 10/10 BİREBİR aynı olmalı — değilse DUR
· G7: sınıflandırıcı `kaynaklar`ı DA görmeli. "…bulunmamaktadır" İKİ iş görür:
  "kaynakta yok" (çekinme) ↔ "kanunda hüküm yok" (CEVAP) — ayrım 6/6 y.pozitif üretti.
· G9: retriever boş dönerse model ÇAĞRILMAZ — üründe M5 koşulu oluşmamalı
· G16: donmuş TEST tek kez açılır; ADR-0069 raporlaması ZORUNLU (ham kütle manşet,
  tavan kullanımı yanında, rakip kıyası o orandan KURULMAZ)
· G5 Adım 6'nın ön koşulu Faz 0 planı T5 Adım 2 (sys.path deseni)

KURALLAR: TDD — önce failing test, koş, gör, sonra asgari kod · sorunu açık bırakma,
tuzağı plana yaz · uzun koşu setsid nohup, |tail yok · her adımda plan-göreli STATUS
(hangi faz, kaç kutucuk, ne harcandı) · sayı hatırlanmaz KAYNAKLANIR, çelişki iki yerde
damgalanır · gözle okuma bir KAPIDIR (Faz 0'da sayısal kapı beş kusuru geçirdi) ·
kutucuk yalnız verify: çıktısı ALINDIKTAN sonra · yapısal ↔ davranışsal değişiklik AYRI
commit · ADR-0059 REZERVE, sıradaki 0074 · belge/commit dili TÜRKÇE, kod İngilizce ·
⛔ docs/record/** ve docs/adr/** TARİHSEL KAYIT — kırık link onarımında bile dokunulmaz.

⛔ DUR ve SOR: yeni rejim kararı · tek adımda >$1 harcama · donmuş TEST'in açılması ·
bir AÇIK KARAR damgasını kendi başına kapatmak · bir kapıdan kalan koşuyu puanlamak.
```

---

## Bu goal neyi kasten dışarıda bırakıyor

| iş | nerede | neden burada değil |
| :--- | :--- | :--- |
| **T5** `scripts/` alt-klasör düzeni | Faz 0 planı **Görev 9** (8 adım) | Ayrı plan; ama **G5 Adım 6'nın ön koşulu** |
| **T1** `models/` ~20 GB temizliği | Faz 0 planı §⏭️ | Ön koşulu **AÇIK KARAR S7** |
| **Hat C** metodoloji paper'ı | spec §7 | `v1.0` sonrası |
| **S9** `v2` barındırma · **S17** kuantizasyon eğrisi | `open_questions.md` | Bu planın dışında |
| `exact_reject`'in kör mod dalı | plan §⏭️ | Sıradaki turda, **koşudan ÖNCE** düzeltilir |
| `recall_taban.json` | plan §⏭️ | Faz 0'ın tek *"kaynaklanmadı"* ihlali; $0, ~15 dk |
