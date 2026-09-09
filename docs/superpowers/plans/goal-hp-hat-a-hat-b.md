/goal Planı BİTİR: docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md
ÖNCE OKU: planın İCRA DURUMU + İŞ SIRASI blokları (82/90) · plans/post-hp-hat-b-tickets.md.
DURUM 2026-09-09: yedi sıradan beşi kapandı. Sürüm v0.3; v1.0 VERİLMEDİ (ADR-0077) — engel model
değil ÖLÇÜM AYGITI (tek hakem ailesi, κ 0,534 < 0,6). 164 test yeşil. Dal: MASTER, origin ile
eşit, ağaç temiz, v0.3 etiketi push edildi. Ağırlıklar HF'te ama ÖZEL. Bakiye $2,20.
ATLANDI, açma: G2 · G14 · G15 · G8.

━━ SIRA 2 · G12/6-7 — TUI gözle doğrula · $0 · GPU · İNSAN GÖZÜ KAPISI
llama-server aç (bayraklar aşağıda), `python -m hakhukuk.tui`, ÜÇ soru sor.
verify: üçünde de rozet+atıf+kaynak+ibare EKRANDA GÖRÜLDÜ, İNSAN TEYİT ETTİ. Kendi başına
işaretlenmez. Bu kapı 2026-09-09'da bir kusur yakaladı: komut hiç açılmıyordu (__main__ yoktu)
ve 163 test görmemişti — kaynak denetimi programın çalıştığına bakmaz.

━━ SIRA 7 · G19 — HTTP API (FastAPI) · $0 · KAPSAM İNSAN KARARIYLA GENİŞLETİLDİ
API v2'ydi, v1'e alındı; çelişki 00-IS-SIRASI'da damgalandı. S9 AÇILMADI: yerel, tek kullanıcı.
answer() üstünde İNCE KABUK — kendi mantığı YOK, SORUMLULUK_IBARESI cli.py'den IMPORT edilir.
Altı karar KİLİTLİ: (1) 127.0.0.1, kimlik yok · (2) yapısal alanlar + hazır `sunum` dizesi
(tembel tüketici tek alanı bassa bile rozet+atıf+kaynak+ibare gider) · (3) YALNIZ answer();
answer_arac taşıyıcıda araç ayrıştırmıyor, açılırsa tüketici araç kullanıldığını SANIR ·
(4) boş metin → 503, dolu KESİK → 200 ("HTTP 200 ile boş içerik" #42'nin kusurudur, sınırı
geçmesin) · (5) boş sorgu → 422, UYDURULMUŞ UZUNLUK EŞİĞİ YOK · (6) serileştirilmiş tek istek
(tekilin evre güvenliği ÖLÇÜLMEDİ) + opsiyonel ekstra hakhukuk[api], giriş noktası hakhukuk-api.
TDD: failing test (TestClient, sunucu/model YOK, servis.answer monkeypatch) → koş → gör → kod.
Adım 6 de bir GÖZ KAPISI. Ticket 1 ve 3'ü ÇÖZMEZ; boş cevap 503 olarak GÖRÜNÜR, giderilmez.

━━ SIRA 8 · tickets — plans/post-hp-hat-b-tickets.md, on ticket, hiçbiri planda değil
En ağır üçü: (1) ürün yolunda cevapların ~%5'i TAMAMEN BOŞ (4/80, sonlanmama) ve ADR-0040'ın
%5 kapısını GEÇMEZ — düzeltmesi REJİM DEĞİŞİKLİĞİ ⇒ onay + 80 kalem yeniden ölçüm ·
(2) sunucu KV ayarı cevabı DEĞİŞTİRİYOR (ölçüldü), 80 kalemdeki etkisi ÖLÇÜLMEDİ, $0 ~1 sa ·
(4) boş sorgu reddedilmiyor, sabit gürültü dönüyor.

━━ İNSAN KARARI BEKLEYENLER: SIRA 2 onayı · ticket 1/3 düzeltilsin mi · ticket 2 ölçülsün mü ·
HF ne zaman herkese açılsın · ta_v1+tg_v1 adaptörleri (2x114 MB) silinsin mi (T1).

━━ BAĞLAYICI SUNUCU YAPILANDIRMASI (değiştirmek CEVABI değiştirir, ölçüldü)
llama-server -m models/gguf/tgta_v1-q4_k_m.gguf -ngl 99 -fa on --no-context-shift
  --cache-type-k q8_0 --cache-type-v q8_0 -c 8192 --host 127.0.0.1 --port 8080

━━ SAYILAR (hepsi kaynaklı) — DEV kütle 0,8011 · tavan 0,9500 · uydurma madde 0/114 ·
aşırı-red 4/80. Donmuş TEST (tek kez açıldı): kütle 0,5804 · tavan 0,7500 · tavan kullanımı
0,7739 ↔ DEV 0,8433; düşüşün %76'sı bileşimden, %24'ü DEĞİL; uydurma madde 0/52 KORUNDU.
Sonnet-5 ÖNDE: 0,8348 ↔ 0,8011. B1 hükmümüz ÇÜRÜDÜ: wrong_ref 0,0769 ↔ 0,0083.

KURALLAR: TDD (failing test → koş → gör → kod) · uzun koşu setsid nohup, |tail YOK · GPU işini
subagent'a ver · sayı KAYNAKLANIR · çelişki İKİ YERDE damgalanır · gözle okuma bir KAPIDIR ·
kutucuk yalnız verify ALINDIKTAN sonra · yapısal ↔ davranışsal AYRI commit · ADR 0078, log #66 ·
TÜRKÇE belge, İngilizce kod · YAYIMLANAN BELGEDE EMOJİ YOK, akademik register ·
docs/record/** ve docs/adr/** yeniden yazılmaz, yalnız yeni dosya eklenir.
DUR ve SOR: donmuş TEST · yeni rejim · AÇIK KARAR damgası · >$1 · push · HF görünürlüğü.
