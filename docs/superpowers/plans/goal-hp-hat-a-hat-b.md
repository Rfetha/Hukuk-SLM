/goal İCRA — planın kalanını YÜRÜT. Tasarım bitti (insan onayı 2026-09-10).
Plan: docs/superpowers/plans/2026-09-07-hp-hat-a-hat-b.md — İCRA DURUMU + İŞ SIRASI + sondaki
AÇIK KUSURLAR bloklarını ÖNCE oku. Payda 115, 88 bitti (dosyadaki 40 kutucuğu SAYMA, blok söyler).
BECERİ: superpowers:subagent-driven-development. Her adımı alt-ajana ver, sonucu DOĞRULA, sonra
işaretle. OTONOM AK — kapı yoksa sorma, izin isteme, rapor için durma. Yalnız DUR listesinde dur.

━━ SIRA 10 · G21 ürün yüzeyi kusur temizliği · 0/11 · $0 · EN OTONOM İŞ, BURADAN BAŞLA
kusur 3·4·5·7·8·12a·13. TDD: failing test → koş → KIRMIZI GÖR → kod. Adım 1-10 otonom akar.
Dört karar KİLİTLİ: (1) boş sorgu KAPISI servis.answer()'a, üç yüzeyi birden korur, UYDURULMUŞ
UZUNLUK EŞİĞİ YOK · (2) ##begin_quote## süzgeci YALNIZ bicimle()'de, Cevap.metin HAM kalır,
⛔ ölçüm hattına DOKUNMA (score_register.py:41 o işareti register göstergesi SAYIYOR) ·
(3) kapsam satırı STATİK, sınıflandırıcı YOK (yanılırsa cevabı olan soruyu öldürür) ·
(4) zayıf-eşleşme rozeti ÖLÇÜME BAĞLI. Adım 8 bir ÖLÇÜMDÜR: recall'ın kaçırdığı 4/80 ile
tutturduğu 76'nın skor dağılımı AYRIŞMIYORSA rozet EKLENMEZ, kusur 5a açık kalır — bu bir
BULGUDUR, başarısızlık değil. Eşik uydurma. Adım 11 İNSAN GÖZÜ KAPISI.

━━ SIRA 9 · G20 konteyner · 1/9 · $0 · ADR-0078 · Adım 1-6 otonom
Ad0 GPU kapısı GEÇTİ (konteyner RTX 5070 Ti'yi host ile BİREBİR görüyor). 3 kutu / 2 daemon /
2 imaj: indir (TEK SEFERLİK; HF pinli revizyon 902ace67259b3fac18c56907070485f5cace272b →
sha256 KAPISI → volume; tutmazsa iki servis de HİÇ başlamaz) · llama (GPU) · app (CPU).
Beş karar KİLİTLİ (tam metin Görev 20): bayraklar compose'a BİREBİR · tek sapma --host 0.0.0.0
(sebebi yazılı, üretimi etkilemez) · revizyon PİNLİ latest YOK · indeks iki yollu (volume
öncelikli, HF yedek) ⇒ G8 bozulmaz · imaj repo AĞACINI kopyalar, kusur 11 onarılmaz.
Testi Docker OLMADAN koşulur (compose yaml'ı AYRIŞTIR, metin arama YAPMA). Adım 7 GÖZ KAPISI.
NOT: HF deposu ÖZEL, tokensız 401 — Adım 6 HF_TOKEN ister.

━━ SIRA 11 · G22 rejim + KV · 0/5 · GPU · İKİ DUR-ve-SOR VAR
Adım 1 otonom ($0): fp16 KV ile 80 kalem üret, q8_0 koşusuyla HAKEMSİZ karşılaştır — kaç cevap
sha256 olarak değişti, çekinme, uydurma madde, kesik. KÜTLE HESAPLAMA (hakem = para). Adım 2 DUR-ve-SOR: kütle ölçülsün mü, bedel $1 kapısına vurulur. Adım 3 DUR-ve-SOR:
ürün yoluna iki geçişli zorunlu düşünce kapatma REJİM DEĞİŞİKLİĞİDİR. Adım 4 çıpası elde:
outputs/eval/g18-arac-katmani/aracsiz_yol_80.json (kesik 7/80, tamamen boş 4/80).

━━ SIRA 2 · G12/6-7 ve SIRA 7 · G19/6 — İKİSİ DE İNSAN GÖZÜ KAPISI
Kod bitti. Sunucuyu aç, ekranı hazırla, İNSANA SOR. Kendi başına İŞARETLEME.

━━ DURUM · v0.3; v1.0 VERİLMEDİ (ADR-0077) — engel model değil ÖLÇÜM AYGITI (κ 0,534 < 0,6).
178 test yeşil. MASTER, 9 commit yerelde (push EDİLMEDİ). Ağırlıklar HF'te ÖZEL. Bakiye $2,20.
AÇMA: G2 · G8 (Adım 1b hariç) · G14 · G15. DEVREDİLDİ: kusur 6+12b → v2 (B1·B11) · kusur 11.

━━ BAĞLAYICI SUNUCU (değiştirmek CEVABI değiştirir, ölçüldü)
llama.cpp/build-cuda/bin/llama-server (PATH'te DEĞİL) -m models/gguf/tgta_v1-q4_k_m.gguf
  -ngl 99 -fa on --no-context-shift --cache-type-k q8_0 --cache-type-v q8_0 -c 8192
  --host 127.0.0.1 --port 8080

━━ SAYILAR (kaynaklı) — DEV kütle 0,8011 · tavan 0,9500 · uydurma madde 0/114 · aşırı-red 4/80.
Donmuş TEST (tek kez açıldı): 0,5804 · tavan 0,7500. Sonnet-5 ÖNDE 0,8348; wrong_ref 0,0769 ↔
0,0083. Artefakt sha256 755e15e9…

━━ KURALLAR: TDD (failing test → koş → GÖR → kod) · uzun koşu setsid nohup, |tail YOK · GPU işini
alt-ajana ver · sayı KAYNAKLANIR · çelişki İKİ YERDE damgalanır · gözle okuma bir KAPIDIR ·
kutucuk YALNIZ verify ALINDIKTAN sonra · yapısal ↔ davranışsal AYRI commit · ADR 0079, log #66 ·
TÜRKÇE belge, İngilizce kod · EMOJİ YOK · docs/record/** ve docs/adr/** yeniden YAZILMAZ.
━━ DUR ve SOR (yalnız bunlar): insan gözü kapısı · donmuş TEST · REJİM değişikliği · >$1 ·
push · HF görünürlüğü · AÇIK KARAR damgası · plan dışına çıkan iş. Başka hiçbir şey için durma.
