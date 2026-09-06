# ADR-0067 — DEV/TEST `core_hard` soru onarımı (v1 → v2)

**Tarih:** 2026-09-06 · **Statü:** ✅ yürürlükte · **Karar:** insan (15 önerinin tamamı onaylandı)

## Bağlam

F0.1 erişim teşhisinde `recall@10`'un kaçırdığı 10 kalem gözle okundu. Kaybın **yarısı erişim
hatası değildi**: 5 kalemde soru, altın maddeyi **belirlemiyordu**. Ölçüt: *soru tek başına
okunduğunda (i) hangi kanun ailesine ait olduğu (ii) o kanun içinde hangi hükmü sorduğu ayırt
edilebiliyor mu?*

Tarama 155 sorunun tamamına uygulandı (DEV 80 + TEST core_hard 40 + TEST trap 35). Üç kusur
sınıfı çıktı ve üçü de soruların **altın maddenin içinden üretildiğini** gösteriyor:
**A** askıda gönderim (öncülsüz "bu") · **B** kanun ailesi belirsiz · **C** kurum belirsiz.

En ağır örnek: İİK 31/a **gemi sicili** hakkındadır; sorusu *"Mahkeme benim lehime bir karar
verirse ne olur?"* idi — belirsiz değil, neredeyse **ilgisiz**.

⭐ **Eşleşmeler tam metinle denetlendi ve DOĞRU çıktı.** KMK 21 gerçekten *"kendi bağımsız
bölümünü ayrıca sigorta ettirme"*yi, KMK 33 gerçekten *"hâkim hangi kurallara göre karar verir"*i,
CMK 142/9 gerçekten avukatlık ücretini düzenliyor. ⇒ Kusur **yer-gerçeğinde değil**, sorunun
bağlamının sökülmüş olmasında.

## Karar

DEV `core_hard` **13 soru**, TEST `core_hard` **2 soru** yeniden yazıldı → **v2**.
Eski dosyalar `.v1-2026-09-06` olarak saklandı (sha256 künyede). Altın alanlar (`kanun_adi`,
`kanun_no`, `madde_no`) ve `n` **birebir korundu** — kod tarafından doğrulandı.

**Dokunulmayanlar, gerekçeli:**
- ⛔ **`canon/trap.jsonl` (35 kalem)** — oradaki tuhaf sorular kusur değil, reddetme davranışını
  ölçen **kasıtlı tuzak**. Aynı ölçütle "düzeltmek" testin kendisini yok ederdi.
- ⛔ **TEST id 31 (KMK 44)** — soru maddenin *"kapanan eski kütük sayfasiyle … bağlantı
  sağlanması"* ifadesini **birebir kopyalıyor**, yani erişimi **yapay kolaylaştırıyor**.
  Düzeltmek kendi sayımızı **yükseltirdi** → dokunulmadı, damgalandı.
- TEST id 34 (TMK 727) — soru maddeyle uyumlu, kusur yok.

## Yanlılık korumaları

1. Her soru **yalnız altın maddenin metnine** bakılarak yazıldı; retriever çıktısına, model
   cevabına, hangi kalemin kaçırıldığına **bakılmadı**.
2. ⛔ Maddenin **ayırt edici ifadeleri kopyalanmadı** — kopyalamak `recall`'u yapay şişirir.
3. 15 önerinin tamamı **insana liste hâlinde** sunuldu; onaysız hiçbiri sete girmedi.
   Künye: *soru yazarı = model · denetçi = insan*.

## Ölçülen sonuç

`recall@10` (aynı indeks, `RRF_K=60` sabit): **0,8750 → 0,9375** · kaçan **10 → 5**.
Kontrol grubu (v1 sorular) çıpayı **birebir** yeniden üretti → ölçüm yolu doğrulandı.
Kütle tavanı **%87,5 → %93,75**.

🚨 **Bir kayıp kayda geçti ve GERİ ALINMADI: id 79.** Eski soru öncülsüz "bu" yüzünden
belirlenemezdi ama içindeki **"eğitim"** sözcüğü maddeyle birebir eşleşiyordu; yeni soru o
sözcüksel çıpayı kaybetti ve kalem **bulunuyorken kaçtı**. Geri almak, eval sorusunu ölçülen
sistemin lehine ayarlamak olurdu — 2. korumanın doğrudan ihlali.

## Bedeli — açıkça

⚠️ `#39-#61` arasındaki **her DEV sayısı v1 birimindedir** ve damgalanmalıdır: kütle
(%68,4 · %73,0 · %62,8) · aşırı-red (9/80 · 8/80) · isabetsizlik (5/80 · 7/80) ·
**ARA KAPI eşiği 0,8649 ve merge M2b 0,766** · ADR-0052'nin 0,506→0,766 sıçraması ·
B10'un 80 kalemlik gözle okuması. Parasal ek yük ≈ $0,15; harcanan şey **kaydın
karşılaştırılabilirliği**.

## Reddedilen alternatifler

- **Değiştirme, yalnız etiketle** ($0, kayıt kırılmaz) — REDDEDİLDİ: sorular bozuk kalır ve model
  onlardan *"bilemedi"* notu almayı sürdürür.
- **Yalnız 7 kesin kalemi düzelt** — REDDEDİLDİ: aynı kusur sınıfı iki kez açılırsa kayıt iki kez kırılır.
- **Sorular insan tarafından yazılsın** — insan bunu değil, *"yaz + onaya sun"*u seçti.

## Kaynaklar
`data/eval/KUNYE_soru_onarimi_2026-09-06.json` · `outputs/eval/f01-erisim/KACIRILAN_10.md` ·
`outputs/eval/f01b-soru-onarimi/ONERI.md` · `outputs/eval/f01b-soru-onarimi/SONUC_recall_v1_v2.md`
