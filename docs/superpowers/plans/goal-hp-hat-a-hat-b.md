# `/goal` promptu — `HP` → Hat A → Hat B planı için

**Kullanım:** aşağıdaki bloğu olduğu gibi `/goal` komutuna yapıştır.
⚠️ `/goal` **4000 karakter** sınırı koyuyor; bu metin **~3,4K**. Ayrıntı planın kendisinde:
[`2026-09-07-hp-hat-a-hat-b.md`](2026-09-07-hp-hat-a-hat-b.md) (1364 satır, 82 kutucuk).

---

```
/goal Planı uygula: docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md
⭐ ÖNCE OKU: planın "Global kısıtlar" + "AÇIK KARARLAR" bölümü. 16 görev, 82 kutucuk.

🔒 SIRALAMA KİLİTLİ (insan kararı): HP → Hat A (PARALEL, $0) → Faz 3 → v0.2 → Hat B → v1.0
 FAZ 1 · HP hakem paneli (G1-4, 18 kutucuk, ~$3-5) — ÖNCE
 FAZ 2 · Hat A paketleme (G5-12, 43 kutucuk, $0, GPU yok) — HP'ye PARALEL koşabilir
 FAZ 3 · Belge katmanı (G13, 7 kutucuk, $0) → v0.2 YAYIN
 FAZ 4 · Hat B model (G14-16, 14 kutucuk, ~$7-15) → v1.0 kapısı · ⛔ HP bitmeden BAŞLAMAZ

NEREDE KALDIK: Faz 0 KAPANDI 40/40 (2026-09-07). v1.0 kapısının ÜÇ maddesi de sayıyla
geçti: (1) kütle 0,8011 ↔ eşik 0,7225 = +5,86 p · (2) isabetsizlik çıpası 8/80 ·
(3) M5 ezber kütlesi −6,82 p (çıpa BASE). Kütle %80,1 · recall@10 0,9500 · aşırı-red
4/80 · uydurulmuş madde 0/114 — SIFIR eğitimle, aletin BEŞ kusuru bulunarak.
ADR 0063-0073 · research_log #62 · S1·S2·S11·S13·S14·S15 kapandı.

⚡ HER GPU KOŞUSUNDAN ÖNCE: künyede `güç : ŞARJDA` DOĞRULA. Pilde GPU 180 MHz'e
kısılıyor → 80 kalem 4,8 saat ↔ şarjda ~25 dk.

🚨 BÜTÇE — ÖLÇÜLDÜ, HATIRLANMADI: OpenRouter $6,60 (total_credits 20 − usage 13,397) ·
Modal $29,19. Bu plan ~$10-20 harcıyor ⇒ HP + kapı koşusuna YETMEYEBİLİR. Fazlar
arası duraklarda bakiyeyi YENİDEN ÖLÇ, hatırlama.

🔓 DÖRT AÇIK KARAR DÖRT GÖREVİ BLOKE EDİYOR — insan cevabı olmadan o görev BAŞLAMAZ:
 S8  indeks nasıl dağıtılır (80 MB, git'te yok)        → G8
 S10 sorumluluk ibaresi (hukukçu görüşü gerekiyor)     → G10
 S16 rakip havuzunda hangi sağlayıcı/kaç özne          → G4
 S18 sürüklenmiş SYSTEM_PROMPT'un hangi hâli kanon     → G5
G8'in adımları BİLEREK BOŞ: iki seçenek farklı kod ister.

KRİTİK TUZAKLAR (planda tam yazılı, hepsi ölçüldü):
· HP: üretim YENİDEN KOŞULMAZ — aynı 80 cevap, farklı hakem (ADR-0017)
· AİLE DIŞLAMASI: üçlü κ YALNIZ bizim kolumuzda kurulabilir; Gemini özneleri Google
  hakemle notlanamaz (ADR-0032). Eksiklik değil, kuralın sonucu — açıkça raporla.
· G5: istem taşındıktan sonra çıktı 10/10 BİREBİR aynı olmalı — değilse DUR
· G7: sınıflandırıcı `kaynaklar`ı DA görmeli. "…bulunmamaktadır" hukuk metninde İKİ iş
  görür: "kaynakta yok" (çekinme) ↔ "kanunda hüküm yok" (CEVAP). Bu ayrımı kaçırmak
  2026-09-07'de 6/6 yanlış pozitif üretti.
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
