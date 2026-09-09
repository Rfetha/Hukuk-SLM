/goal Planı BİTİR: docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md
ÖNCE OKU: planın "İCRA DURUMU" bloğu (79/89) + plans/post-hp-hat-b-tickets.md (10 ticket).
DURUM 2026-09-09: altı sıradan BEŞİ kapandı. Sürüm v0.3 etiketli; v1.0 VERİLMEDİ (ADR-0077) —
engel model değil ÖLÇÜM AYGITI: tek hakem ailesi, κ 0,534 < 0,6. 164 test yeşil. 16 commit
YEREL, push EDİLMEDİ. Ağırlıklar HF'te (Rfetha/HakHukuk-4B-v0.3-Q4_K_M) ama ÖZEL.
Bakiye OpenRouter $2,20. ATLANDI, açma: G14 · G15 · G2 · G8 (Adım 1b hariç, o bitti).

━━ AÇIK TEK KAPI · SIRA 2 · G12/6-7 — TUI gözle doğrula · $0 · GPU
INSAN GÖZÜ KAPISI, kendi başına işaretlenmez. llama-server aç (bayraklar aşağıda),
`python -m hakhukuk.tui`, ÜÇ soru sor.
verify: üçünde de rozet + atıf + kaynak + sorumluluk ibaresi EKRANDA GÖRÜLDÜ, insan teyit etti.
NOT: 2026-09-09'da bu kapı bir ürün kusuru yakaladı — komut hiç açılmıyordu (`__main__` bloğu
yoktu). Onarıldı, testle çivilendi. Kapının varlık sebebi budur.

━━ SONRA: plans/post-hp-hat-b-tickets.md — ON TICKET, hiçbiri planın kapsamında değil
En ağır üçü:
 (1) Ürün yolunda cevapların ~%5'i TAMAMEN BOŞ (4/80, sonlanmama). ADR-0040'ın %5 geçerlilik
     kapısını ürün yolu GEÇEMEZ. Düzeltme = iki geçişli zorunlu kapatma = REJİM DEĞİŞİKLİĞİ
     ⇒ insan onayı + 80 kalem yeniden ölçüm.
 (2) Sunucu KV ayarı cevabı DEĞİŞTİRİYOR (q8_0 ↔ fp16: SUSKUNLUK ↔ ÇEKİNCELİ, ölçüldü).
     80 kalemdeki etkisi ÖLÇÜLMEDİ; 0,8011'in varsayılan KV'de korunacağı İDDİA EDİLMİYOR. $0, ~1 sa.
 (4) Boş sorgu REDDEDİLMİYOR — sabit gürültü kümesi dönüyor ve model onunla çağrılıyor.

━━ İNSAN KARARI BEKLEYENLER
 · SIRA 2 onayı · push + master merge · ticket 1 ve 3 düzeltilsin mi · ticket 2 ölçülsün mü
 · HF deposu ne zaman herkese açılacak

━━ BAĞLAYICI SUNUCU YAPILANDIRMASI (ölçümlerin yapıldığı, değiştirmek sonucu değiştirir)
llama-server -m models/gguf/tgta_v1-q4_k_m.gguf -ngl 99 -fa on --no-context-shift
  --cache-type-k q8_0 --cache-type-v q8_0 -c 8192 --host 127.0.0.1 --port 8080

━━ BUGÜNKÜ SAYILAR (hepsi kaynaklı)
DEV kütle 0,8011 · tavan recall@10 0,9500 · uydurma madde 0/114 · aşırı-red 4/80
Donmuş TEST (tek kez açıldı): kütle 0,5804 · tavan 0,7500 · tavan kullanımı 0,7739 ↔ DEV 0,8433
  düşüşün %76'sı bileşimden, %24'ü DEĞİL. Uydurma madde 0/52 KORUNDU.
Sonnet-5 ÖNDE: kütle 0,8348 ↔ 0,8011 (GÖZ-katı). Önde olduğumuz tek eksen uydurma madde (0 ↔ 2).
B1 hükmümüz ÇÜRÜDÜ: wrong_ref 0,0769 ↔ 0,0083 = 9,3× geride (yalnız Gemini havuzunda öndeydik).

KURALLAR: TDD (failing test → koş → gör → kod) · uzun koşu setsid nohup, |tail YOK · GPU işini
subagent'a ver · plan-göreli STATUS · sayı KAYNAKLANIR · çelişki İKİ YERDE damgalanır · gözle
okuma bir KAPIDIR · kutucuk yalnız verify ALINDIKTAN sonra · yapısal ↔ davranışsal AYRI commit ·
ADR 0078, log #66 · TÜRKÇE belge, İngilizce kod · YAYIMLANAN BELGEDE EMOJİ YOK, akademik register
· docs/record/** ve docs/adr/** yeniden yazılmaz, yalnız yeni dosya eklenir.
DUR ve SOR: donmuş TEST · yeni rejim · AÇIK KARAR damgası · >$1 · push · HF görünürlüğü.
