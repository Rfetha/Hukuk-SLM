# #60 — B10 hasadının kabul ölçütü çöktü: `exact_reject` doğru cevapları çekinme sayıyor

- **Tarih:** 2026-09-06
- **Tur:** Görev 3 pilotu (B10 aşırı-red turu) — [plan](../../superpowers/plans/2026-08-06-asiri-red-tau-a-v2.md)
- **Bedel:** GPU **Modal L4, ~50 dk** · hakem **$0** · **çıktı kullanılamaz**
- **Hüküm:** 🛑 **Görev 4 başlatılmadı.** Kabul ölçütü onarılmadan hasat yapılamaz.
- **Kaynak dosyalar:** `data/_ham_ve_ara/b10-pilot/` (`b10_np1.jsonl` 26 · `b10_np8.jsonl` 29 ·
  künyeler · `b10_np_karsilastirma.json` · `GOZLE_OKUMA_10.txt`) · Modal `hukuk-data:/b10-pilot`

## Ne ölçüldü

Pilot iki kolda koştu (`--limit 150`, seed 3407, Q4_K_M GGUF + llama.cpp, KV q8_0, `-fa on`,
`--no-context-shift`, L4):

```
np1   denenen 150 · kabul 26 · kabul_orani 0,1733 · s_uretim 13,735 s · 2.174,9 s
np8   denenen 150 · kabul 29 · kabul_orani 0,1933 · s_uretim  ~5,1  s ·   845,4 s   (2,57×)
```

Plan Adım 3.8 **10 kabul kalemini gözle okumayı** emrediyor (ADR-0051 dersi: şablon çıktısı
okunmadan kabul edilmez). Okundu — ve kapıyı düşürdü.

### ⭐ Bulgu: kabul edilen kalemlerin çoğunluğu çekinme DEĞİL

| | sayı |
| :--- | ---: |
| `rejected` alanı aslında **tam, atıflı CEVAP** | **6 / 10** |
| gerçek çekinme | 4 / 10 |

Örnek (`raft11188`, altın `2004/Madde 225`) — "çekinme" diye toplanan metin:

> 3) Sonuç olarak, itiraz süresi **yedi gündür** (İCRA VE İFLAS KANUNU, Madde 225).

Aynısı `raft12319` (TMK 228) · `raft1328` (CMK 200) · `raft3230` (İİK 54) · `raft5789` (TBK 606) ·
`raft10304` (TMK 468). Gerçek çekinmeler: `raft8972` · `raft3488` · `raft382` · `raft12744`.

## Kök neden — kesin, tekrarlanabilir

`b10_hasat.py` hasadı **yeterlilik önsözü OLMADAN** koşuyor
(`b10_np1_KUNYE.json`: `"sufficiency_preamble": false`). O rejimde cevapta açılış yeterlilik
hükmü oluşmuyor — **26/26 kalemde `_acilis_yeterlilik_hukmu` → `None`**.

`exact_reject` (`scripts/score_abstention.py:208`) o dalda **cevabın TAMAMINI** `REJECT_RE` ile
tarıyor. Havuzun (`data/train/raft_scrubbed/`) cevap şablonu ise şu:

```
1) [gerekçe] … diğer kaynaklar … İÇERMEMEKTEDİR   ← REJECT_RE BURADA tetikleniyor
2) ##begin_quote## … ##end_quote##
3) Sonuç olarak, <CEVAP> (KANUN, Madde N).        ← gerçek hüküm BURADA
```

Yani tetikleyen ibare cevabın hükmü değil, **elenen kaynakların gerekçesi**. Doğrulandı:
üç kalemde de eşleşen ibare `'içermemektedir'`, `_son_esasli_ibare` çıktısında ise red işareti
**yok**.

⚠️ `exact_reject`'in doğru okuyan yolu (`_son_esasli_ibare`, #57/Ö2 ile eklendi) **yalnız açılış
hükmü `True` iken** çalışıyor. Önsözsüz rejimde o yola hiç girilmiyor.

### Sonucu: ön-kayıtlı D1 kapısı aslında DÜŞÜYOR

```
raporlanan kabul_orani   0,1733  (26/150)          → kapı geçmiş GÖRÜNÜYORDU
gözle okumaya göre       ~0,07   (kabullerin ~%40'ı gerçek)  → eşik 0,10'un ALTINDA
```

Görev 4 koşulsaydı ~250 kalemin çoğunluğu **doğru atıflı cevap** olarak `rejected` etiketiyle
ORPO'ya girecek, `τ_a` v2'ye *"doğru cevap verme"* öğretilecekti — **turun hedefinin tam tersi.**
Kapıyı tutan tek şey planın gözle-okuma adımı oldu.

## ⚠️ Çıpalara bulaşma: KANITLANMADI, kapanmadı da

Programatik bir sonda (*"`exact_reject` True ama `_son_esasli_ibare`'de red yok"*) resmî çıpada
(`outputs/eval/olcum-bi/h1_tgta_v1_bi_k10_detail.jsonl`, n=80, `exact_reject`=19)
**10 kalemi** işaretledi. Üçü gözle okundu:

| id | sonda | gözle okuma |
| :--- | :--- | :--- |
| 7 | yanlış pozitif | ❌ **GERÇEK çekinme** — sonda yanıldı |
| 19 | yanlış pozitif | ✅ **gerçek yanlış pozitif** (tam atıflı cevap veriyor) |
| 20 | yanlış pozitif | ❌ **GERÇEK çekinme** — sonda yanıldı |

🚨 **Sonda her iki yönde de hatalı** — hasat kolunda gerçek bir çekinmeyi (`raft3488`) yanlış
pozitif saydı. Bu yüzden *"çıpanın 19 redinin 10'u yanlış"* **kurulmadı ve kurulmamalıdır.**

Kesin olan iki şey:
1. Çıpada **en az bir doğrulanmış yanlış pozitif** var (`id=19`).
2. Önsözlü resmî koşuda bile açılış hükmü çoğunlukla oluşmuyor: **75 `None` · 5 `True`** — yani
   cevapların **%94'ü** aynı hatalı dala düşüyor.

**Çıpa bulaşmasının büyüklüğü ÖLÇÜLMEMİŞ.** Kapatması 80 kalemin gözle okunmasını gerektirir.
B10'un turdaki sayıları (**16 → 14**, [#56](2026-08-05-olcum-bosluklari.md)) bu ölçüm yapılana
dek **şüpheli** sayılmalıdır.

## KARAR-6 kıyası — toplandı, ama BOZUK ölçütle

```
kesişim 19 · yalnız np1 7 · yalnız np8 10 · Jaccard 0,5278
cevap metni birebir aynı 3 · kesişimde metin farklı 16
```

⛔ Hüküm **kurulmadı** (KARAR-6 insan kararı) — ve kurulamaz da: bu kümeler bozuk ölçütle
seçildi. Ölçüt onarılınca kıyas **yeniden koşulmalıdır.**

## Yine de ödenen: taşıyıcı doğrulandı

- Sızıntı süzgeci konteynerde yerelle **birebir**: `13.350 → 12.914` (atılan **436**, %3,3)
- GPU'ya yüklendiği ölçüldü: **65,8 tok/s** üretim · 2.542 tok/s prompt (CPU olsa ~5 tok/s)
- `gguf_sha256 755e15e92e9f7021…` · kart `NVIDIA L4, 23034 MiB`
- Modal hasat yolu (`harvest_b10`) çalışır durumda ve ADR-0047 m.2 taşıyıcısına uyuyor.

🐞 Yol boyunca iki alet kusuru bulundu ve düzeltildi:
1. `os.chdir("/root")` (sızıntı süzgecinin göreli `DEV_YOLLARI`'sı için gerekli) `llama-server`'ın
   `libllama-server-impl.so`'yu bulmasını engelliyordu → kod **127**. Sunucu artık ikilinin
   dizininde + açık `LD_LIBRARY_PATH` ile koşuyor.
2. `--version` probu da aynı sebeple künyeye sürüm yerine **linker hatası** yazıyordu.

🐞 Üçüncü, düzeltilmemiş: `b10_hasat.py:223` ilerleme satırını yalnız **reddedilen** kalemlerde
ve `n%25==0` iken basıyor → `denenen=100` gibi kilometre taşları kabul edilen bir kaleme denk
gelirse hiç görünmüyor. İlerleme ölçer olarak güvenilmez.

## Ders

⚠️ **Bu, #57'nin dersinin tekrarı:** *"alet düzeltmesi aletin kendisinde yapılır."* `_son_esasli_ibare`
yolu #57'de tam da bu sınıf hata için eklendi, ama **yalnız bir dala** bağlandı; önsözsüz rejim
kapsam dışında kaldı ve üç hafta sonra yeni bir tüketicide (hasat) geri geldi.

⚠️ **Ve ADR-0051'in dersi ikinci kez kendini ödedi:** kabul ölçütü sayısal olarak sağlıklı
görünüyordu (0,1733 > 0,10), yalnız **gözle okuma** çürüttü.

## Açık kalemler

1. `exact_reject` önsözsüz rejimde onarılacak mı, yoksa hasat **önsözlü** mü koşacak? İkisi farklı:
   ikincisi hasadı ADR-0058 ana protokolüne yaklaştırır ama `τ_a` v1'in hasat rejiminden uzaklaştırır.
2. Çıpaların 80 kalemi gözle okunacak mı? Okunmazsa B10 sayıları şüpheli kalır.
3. Alet değişecekse ADR gerekir (sıradaki **0061**; ⚠️ **0059 REZERVE**).
