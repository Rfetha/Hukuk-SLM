/goal Planı BİTİR: docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md
⭐ ÖNCE OKU: planın "İCRA DURUMU" bloğu — sıra + adımlar orada.
✅ BİTTİ: FAZ 1-2-3 → v0.2 · 143 test yeşil · $3,21. 🔒 v1 = ham base + SFT, SFT İLE KAPANIR
(ADR-0075). ⛔ ATLANDI, açma: G14 (B1) · G15 (B4) · G2 (3. hakem) · G8 (indeks). B1: rakiplerden
GERİDE DEĞİLİZ (8/80 ↔ 8·8·7·8); B4: MERGE kaybı, v2'de merge YOK. İkisi BORÇ.

━━ SIRA 1 · G8/1b — KUNYE taşınabilirlik · $0 · bugün ürünü kıran TEK şey
KUNYE.json MUTLAK YOL + mtime damgalıyor (retriever.py:143-152) ⇒ git clone sonrası HER MAKİNEDE
SystemExit. Yol repo-göreli, mtime → içerik hash.
verify: repo BAŞKA DİZİNE kopyalanır, retriever yükler, recall@10 0,9500.

━━ SIRA 2 · G12/6-7 — TUI gözle doğrula · $0 · GPU · ürün yüzü insan gözüyle HİÇ görülmedi
llama-server aç, `python -m hakhukuk.tui`, ÜÇ soru sor (textual 8.2.8 KURULU).
verify: üçünde de rozet+atıf+kaynak+ibare EKRANDA GÖRÜLDÜ.

━━ SIRA 3 · G4 — Sonnet-5 ÖZNE olarak rakip havuzuna · ~$0,82 · havuzda frontier sınıfı YOK
✅ $1 KAPISI AÇIK: $0,82 BAKİYE farkından okundu = ZATEN gerçek fatura ⇒ 1,6× ÇARPMA, sormadan
KOŞ. Kapıyı ETKİLEMEZ (ADR-0072 m.2). Rejim F0.4'ün BİREBİR aynısı: --reasoning-budget 1024
(--think-budget DEĞİL) · k=10 · 900 klip · seed 3407 · önsözsüz · n=80. KAPI: recall@10 = 0,9500,
değilse HÜKÜM KURULMAZ. Red-regex YENİ AİLEDE kalibre; ÜÇ okuma (ALET/GÖZ-orta/GÖZ-katı).

━━ SIRA 4 · G16/2-4 — v1.0 KABUL TESTİ · ~$0,10 · ⛔ ARAÇSIZ (ADR-0076 m.4, eşit sınav)
⛔⛔ DONMUŞ TEST TEK KEZ AÇILIR — açmadan ÖNCE İNSAN ONAYI AL. Adım 1 BİTTİ.
ADR-0069: ham kütle MANŞET · tavan kullanımı + iki setin recall@10'u yanında · ⛔ rakip kıyası o
orandan KURULMAZ. TEST tavanı ≈0,75 ⇒ kütle düşük çıkacak, BAŞARISIZLIK DEĞİL.
Geçerse v1.0, geçmezse damgalanıp yayımlanır (ADR-0065).

━━ SIRA 5 · G18 — ARAÇ KATMANI · $0 · ADR-0076 · davranışı değiştirir ⇒ kapıdan SONRA
🚨 Gerekçesi ÇÜRÜDÜ: isabetsizlik 8/8, aşırı-red 4/4 — altın ZATEN BAĞLAMDAYDI ⇒ sorun SEÇİM. Tek
ölçülmüş hedef recall kaybı 4/80. Yine de konur; gerekçe ÜRÜN YETENEĞİ, ÖLÇÜLMEMİŞ ⇒ kazancı
sayıya EKLENMEZ.
🔒 KAPI ↔ KALDIRAÇ: atıf doğrulama · mülga süzgeci · durum sınıflandırma TOOL DEĞİLDİR, döngü
DIŞINDA koşulsuz çalışır (uydurma 0/114 oradan). 5 KALDIRAÇ: ara · madde_getir · madde_var_mi ·
kanun_bul · yururlukte_mi — LLM ÇAĞIRMAZ.
⛔ Döngü SINIRLI, sınır GÖRÜNÜR: Durum.ARAMA_TUKENDI (KESIK'le BİRLEŞTİRİLMEZ).
🚨 REGRESYON: araçsız yolda 80 kalem BİREBİR aynı (suskunluk [15,37,45,66,79]).

━━ SIRA 6 · G17 — MODELİ YAYINLA · $0 → 🏷️ RELEASE · kapı ADI belirler ⇒ EN SONDA
🚨 Ağırlıklar hiçbir yerde yayında DEĞİL (.gitignore:41, HF linki YOK) ⇒ "açık kaynak" iddiası
YARIM. HF reposu + kart + üç belgede indirme yolu. ⚠️ Kartın İLK EKRANINDA: model TEK BAŞINA
sayıyı ÜRETEMEZ, indeks yok (G8). ⛔ HF_TOKEN .env'de YOK — İNSANDAN İSTE.

━━ ERTELENDİ: G11/2 temiz makine kapısı — G8'e bağlı, bugün TANIM GEREĞİ düşer.
🔮 SONRAKİ TUR (plan DIŞI): v2 = tgta_v1 üstüne GRPO + araç kullanımının EĞİTİMİ.
Taban: uydurma 0/114 · aşırı-red 4/80 · kütle 0,8011.
🚨 BÜTÇE: OpenRouter $3,40 · Modal $29,19; ihtiyaç ~$0,92. 1,6× SADECE judge_cost_usd'ye (liste
fiyatı), BAKİYEYE DEĞİL. ⚡ GPU ÖNCESİ `güç : ŞARJDA`. 🔒 HAKEM = gpt-4o-mini.

KURALLAR: TDD (failing test → koş → gör → kod) · uzun koşu setsid nohup, |tail YOK · GPU işini
subagent'a ver · plan-göreli STATUS · sayı KAYNAKLANIR · çelişki İKİ YERDE damgalanır · gözle
okuma bir KAPIDIR · kutucuk yalnız verify ALINDIKTAN sonra · yapısal ↔ davranışsal AYRI commit ·
ADR 0077, log #65 · TÜRKÇE belge, İngilizce kod · ⛔ docs/record/** ve docs/adr/** dokunulmaz.
⛔ DUR ve SOR: donmuş TEST · yeni rejim · AÇIK KARAR damgası · >$1 (SIRA 3 HARİÇ, ölçüldü).
