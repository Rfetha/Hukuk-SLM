/goal PLANLAMA MODU — planı TASARLA ve GÜNCELLE. İCRA için insan ONAYI ŞART.
Plan: docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md (88/99) — İCRA DURUMU + İŞ SIRASI +
sondaki AÇIK KUSURLAR bloklarını ÖNCE oku. Harita: docs/superpowers/00-IS-SIRASI.md.

━━ BU MODDA NE YAPILIR
Tasarım ve belge: plana görev/adım eklemek · kilitli karar tablosu yazmak · ADR açmak · goal'ü
yenilemek · grill (bir kararı ölçüyle sınamak, ELENEN seçenekleri yazmak) · kodu OKUYUP bulgu
çıkarmak · bayat işaretçi ve çelişki damgalamak.
━━ BU MODDA NE YAPILMAZ — ÖNCE SOR, ONAY AL
Kod/dosya yazmak · test koşturmak dışında koşu başlatmak · kutucuk işaretlemek · bağımlılık
kurmak · commit · push. Bir görev "hazır" göründüğünde DUR ve "başlayayım mı" diye SOR.

━━ AÇIK SIRA: 2 · 7 · 9 (8 = açık kusurlar, kutucuksuz, paydaya girmez)
SIRA 2 · G12/6-7 TUI — İNSAN GÖZÜ KAPISI, benim işaretleyemeyeceğim tek sınıf. llama-server
(bayraklar aşağıda) + `python -m hakhukuk.tui`, üç soru; rozet+atıf+kaynak+ibare EKRANDA.
SIRA 7 · G19 HTTP API — KOD BİTTİ 2026-09-10, 178 test yeşil. Açık tek kutucuk Adım 6, o da
göz kapısı. Canlı koşuldu: HTTP 200, 42,5 sn, dört parça sunum alanında, boş sorgu 422.
SIRA 9 · G20 KONTEYNER — ADR-0078, 5 karar kilitli, 1/9 (Adım 0 GPU kapısı GEÇTİ: konteyner
RTX 5070 Ti'yi host ile BİREBİR görüyor). Adım 1-8 KODLANMADI, insan onayı bekliyor.
3 kutu / 2 daemon / 2 imaj: indir (TEK SEFERLİK, HF pinli revizyon 902ace67 → sha256 KAPISI →
volume) · llama (GPU) · app (CPU). Gerekçe kolaylık DEĞİL: kusur 2 ölçtü, sunucu bayrağı
CEVABI DEĞİŞTİRİYOR ve bunu bugün hiçbir şey zorlamıyor; compose zorlayan ilk artefakt.

━━ DURUM 2026-09-10 · sürüm v0.3; v1.0 VERİLMEDİ (ADR-0077) — engel model değil ÖLÇÜM AYGITI
(tek hakem ailesi, κ 0,534 < 0,6). 178 test yeşil. MASTER, 6 commit yerelde (push EDİLMEDİ).
Ağırlıklar HF'te ÖZEL (tokensız 401, ölçüldü). Bakiye $2,20. ATLANDI, açma: G2·G14·G15·G8.

━━ AÇIK KUSURLAR — planın sonunda, on üç, KUTUCUK TAŞIMAZ. En ağır dördü:
(1) ürün yolunda cevapların ~%5'i TAMAMEN BOŞ (4/80), ADR-0040'ın %5 kapısını GEÇMEZ;
düzeltmesi REJİM DEĞİŞİKLİĞİ ⇒ onay + 80 kalem yeniden ölçüm · (2) KV ayarının 80 kalemdeki
etkisi ÖLÇÜLMEDİ · (12) eğitim verisinin ##begin_quote## işaretleri VATANDAŞA GİDİYOR; kaynağı
istem DEĞİL, gen_v2b_answers.py:36-37 — model öğrenmiş. Süzme YALNIZ sunum katmanında olmalı,
score_register.py:41 aynı işareti register göstergesi olarak SAYIYOR · (6) yanlış maddeye atıf:
canlı örnek 2026-09-10, model TBK 330'u (TAŞINIR kirası) seçti, doğru cevap aynı listedeki 347.
Uydurma değil UYGULANABİLİRLİK hatası; atıf doğrulayıcısı bu sınıfı yakalayamaz ve GEÇTİ.

━━ İNSAN KARARI BEKLER: SIRA 2 onayı · G19 Adım 6 onayı · G20 kodlansın mı · kusur 12 sunum
katmanında süzülsün mü · kusur 1/3 · kusur 2 ölçülsün mü · HF görünürlüğü · push · T1.

━━ BAĞLAYICI SUNUCU YAPILANDIRMASI (değiştirmek CEVABI değiştirir, ölçüldü)
llama.cpp/build-cuda/bin/llama-server (PATH'te DEĞİL) -m models/gguf/tgta_v1-q4_k_m.gguf
  -ngl 99 -fa on --no-context-shift --cache-type-k q8_0 --cache-type-v q8_0 -c 8192
  --host 127.0.0.1 --port 8080

━━ SAYILAR (kaynaklı) — DEV kütle 0,8011 · tavan 0,9500 · uydurma madde 0/114 · aşırı-red 4/80.
Donmuş TEST (tek kez açıldı): kütle 0,5804 · tavan 0,7500. Sonnet-5 ÖNDE 0,8348; wrong_ref
0,0769 ↔ 0,0083. Artefakt sha256 755e15e9… · 2.783.446.720 bayt · HF revizyon 902ace67…

━━ KURALLAR: sayı KAYNAKLANIR, hatırlanmaz · çelişki İKİ YERDE damgalanır · gözle okuma bir
KAPIDIR ve kendi başına işaretlenmez · elenen seçenek gerekçesiyle YAZILIR · ADR 0079, log #66 ·
TÜRKÇE belge, İngilizce kod · EMOJİ YOK, akademik register · docs/record/** ve docs/adr/**
yeniden YAZILMAZ, yalnız yeni dosya eklenir.
DUR ve SOR: KOD · donmuş TEST · yeni rejim · AÇIK KARAR damgası · >$1 · commit · push · HF.
