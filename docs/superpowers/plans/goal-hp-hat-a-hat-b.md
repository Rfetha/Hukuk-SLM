/goal Planı BİTİR: docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md
ÖNCE OKU: planın İCRA DURUMU + İŞ SIRASI blokları (82/99) · post-hp-hat-b-tickets.md.
DURUM 2026-09-10: sürüm v0.3; v1.0 VERİLMEDİ (ADR-0077) — engel model değil ÖLÇÜM AYGITI (tek
hakem ailesi, κ 0,534 < 0,6). 164 test yeşil. MASTER temiz, origin ile eşit, v0.3
push edildi. Ağırlıklar HF'te ÖZEL. Bakiye $2,20. ATLANDI, açma: G2·G14·G15·G8.
AÇIK SIRA: 2·7·9 (8 = tickets, plan dışı).

━━ SIRA 2 · G12/6-7 — TUI gözle doğrula · $0 · GPU · İNSAN GÖZÜ KAPISI
llama-server aç (bayraklar aşağıda), `python -m hakhukuk.tui`, ÜÇ soru sor.
verify: üçünde de rozet+atıf+kaynak+ibare EKRANDA GÖRÜLDÜ, İNSAN TEYİT ETTİ. Kendi başına
işaretlenmez. Bu kapı 2026-09-09'da bir ürün kusuru yakaladı: kaynak denetimi programın
çalıştığına bakmaz.

━━ SIRA 7 · G19 — HTTP API (FastAPI) · $0 · 6 kutucuk · answer() üstünde İNCE KABUK
Kendi mantığı YOK; SORUMLULUK_IBARESI cli.py'den IMPORT edilir. S9 AÇILMADI: yerel, tek
kullanıcı. Altı karar KİLİTLİ (tam metin: Görev 19): 127.0.0.1 kimliksiz · yapısal alanlar +
hazır `sunum` dizesi (tek alanı bassa bile rozet+atıf+kaynak+ibare gider) · YALNIZ answer()
(answer_arac ayrıştırılmıyor ⇒ tüketici araç kullanıldığını SANIR) · boş metin 503, dolu KESİK
200 · boş sorgu 422, UYDURULMUŞ EŞİK YOK · serileştirilmiş istek + hakhukuk[api].
TDD: failing test (TestClient, sunucu/model YOK, servis.answer monkeypatch) → koş → gör → kod.
Adım 6 GÖZ KAPISI. Ticket 1/3'ü ÇÖZMEZ; boş cevap 503 GÖRÜNÜR, giderilmez.

━━ SIRA 9 · G20 — KONTEYNER · $0 · 9 kutucuk · ADR-0078 · G19'DAN SONRA
Gerekçe kolaylık DEĞİL: ticket 2 ölçtü — sunucu bayrağı CEVABI DEĞİŞTİRİYOR ve bunu bugün
hiçbir şey zorlamıyor; compose zorlayan ilk artefakt.
3 kutu / 2 daemon / 2 imaj: hakhukuk-indir (TEK SEFERLİK; HF pinli revizyon → sha256 KAPISI
→ volume; tutmazsa iki servis de HİÇ başlamaz) · llama (GPU, bayraklar compose'da) · app (CPU,
hakhukuk-api, ports 127.0.0.1). indir+app AYNI imaj. Beş karar KİLİTLİ (tam metin: Görev 20):
bayraklar birebir · tek sapma --host 0.0.0.0, sebebi yazılı, üretimi etkilemez · revizyon PİNLİ,
latest YOK, sha256+bayt kapısı, tutmazsa ERKEN ÇIKIŞ · indeks iki yollu (volume öncelikli, HF
yedek) ⇒ G8'in bekleme gerekçesi bozulmaz · imaj repo AĞACINI kopyalar, F1 (paket tek başına
kurulamıyor, servis.py:46) onarılmaz ve ticket 11'de durur.
ADIM 0 KAPIDIR: konteyner GPU'yu görüyor mu ÖLÇ (nvidia-ctk YOK). Tutmazsa CPU'ya
düşmek -ngl 99'u düşürür = YENİ REJİM ⇒ DUR ve SOR. Adım 7 İNSAN GÖZÜ KAPISI.
Konteyner 0,8011'i ÜRETMEZ (ölçüm hattının sayısı) ve ticket 1/3/4/6'yı ÇÖZMEZ.

━━ SIRA 8 · tickets — plans/post-hp-hat-b-tickets.md, on bir ticket, planda DEĞİL
En ağırı: ürün yolunda cevapların ~%5'i TAMAMEN BOŞ (4/80) ve ADR-0040'ın %5 kapısını GEÇMEZ;
düzeltmesi REJİM DEĞİŞİKLİĞİ ⇒ onay + 80 kalem yeniden ölçüm. Ayrıca: KV ayarının etkisi
ÖLÇÜLMEDİ · boş sorgu reddedilmiyor.

━━ İNSAN KARARI BEKLER: SIRA 2 onayı · ticket 1/3 düzeltilsin mi · ticket 2 ölçülsün mü ·
HF ne zaman herkese açılsın · ta_v1+tg_v1 adaptörleri silinsin mi (T1).

━━ BAĞLAYICI SUNUCU YAPILANDIRMASI (değiştirmek CEVABI değiştirir)
llama-server -m models/gguf/tgta_v1-q4_k_m.gguf -ngl 99 -fa on --no-context-shift
  --cache-type-k q8_0 --cache-type-v q8_0 -c 8192 --host 127.0.0.1 --port 8080

━━ SAYILAR (kaynaklı) — DEV kütle 0,8011 · tavan 0,9500 · uydurma madde 0/114 · aşırı-red 4/80.
Donmuş TEST (tek kez açıldı): kütle 0,5804 · tavan 0,7500. Sonnet-5 ÖNDE 0,8348; wrong_ref
0,0769 ↔ 0,0083. Artefakt sha256 755e15e9… · 2.783.446.720 bayt.

KURALLAR: TDD (failing test → koş → gör → kod) · uzun koşu setsid nohup, |tail YOK · GPU işini
subagent'a ver · sayı KAYNAKLANIR · çelişki İKİ YERDE damgalanır · gözle okuma KAPI ·
kutucuk yalnız verify ALINDIKTAN sonra · yapısal ↔ davranışsal AYRI commit · ADR 0079, log #66 ·
TÜRKÇE belge, İngilizce kod · EMOJİ YOK · docs/record/** ve docs/adr/** yeniden YAZILMAZ.
DUR ve SOR: donmuş TEST · yeni rejim · AÇIK KARAR damgası · >$1 · push · HF görünürlüğü.
