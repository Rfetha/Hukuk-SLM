# ADR-0043 — Düşünce modu **AÇIK**, bütçeli zorunlu kapatma ile · ADR-0030 madde 2 düşer

**Statü:** Yürürlükte · **Tarih:** 2026-07-29
**Otorite belge:** `TASARIM.md` §4.1.1 (rejim) · §8 (base kapısı) · `sprint2.md` CP0
**Süperseder:** **ADR-0030 madde 2** (*"düşünce modu KAPALI koşulur"*) — geri alındı
**İlgili:** ADR-0040 (ön-kayıtlı 🟢🟡🔴 kuralı — *iptal değil, bütçeli kipte yeniden koşulacak*) ·
ADR-0035 (`τ_reasoning`/RS-FT kapsam dışı — **kapı aralandı**, henüz açılmadı) ·
ADR-0017 (maliyet-normalize parite) · ADR-0036 (rejim eşleşmesi = merge geçerliliği)
**Kanıt:** `research_log` [#42](../record/research_log/2026-07-29-cp0-dusunce-modu-sonlanmama.md) ·
[#43](../record/research_log/2026-07-29-cp09-butceli-dusunce-cipalari.md) (CP0.9 ölçümü + ablasyon)

> ## ✅ 2026-07-29 gecesi — karar ÖLÇÜMLE de teyit edildi, m.4 daraltıldı
> **m.1 güçlendi.** Karar ürün gereksinimiyle alınmıştı; CP0.9 ölçümü artık **ölçümle de**
> destekliyor: bütçeli düşünce thinking-off'u **M5 hariç her eksende domine ediyor**
> (M1 kütle 42.6→56.7 · M2 Rej 0.633→0.814 · fabrikasyon 0.367→0.186 · M4 93.1→95.9 ·
> M2b 0.973→0.986 · M3 eşit). Ve ablasyon (#43 Bulgu 5-b) kazancın **biçimden gelmediğini**
> kanıtladı: kaynak-yeterliliği önsözü M2'yi 0.968'e çıkarıyor ama M1'i 28.2'ye düşürüyor —
> tek eksende kaydırma. Düşünce iki ekseni birden taşıyor; **prompt-mühendisliği alternatifi
> elendi.**
>
> **m.4 DARALTILDI (kullanıcı kararı):** thinking-off artık **canlı rejim değil** — çıpa değil,
> kapı referansı değil, kıyas tabanı değil. **Bundan sonra her şey thinking-on koşar.**
> Gerekçe: dağıtılan kip ile ölçülen kip aynı olmak zorunda (ADR-0036'nın rejim-eşleşmesi
> kuralının eval'deki karşılığı); off ölçmek dağıtılmayacak bir modelin sayılarını üretmektir.
>
> **Ne SİLİNMİYOR:** `outputs/eval/sprint1-thinking-off/` ve iki-kip kıyası **kayıt olarak
> durur** — o kıyasın kendisi ölçülmüş bir bulgudur (#43 Bulgu 5/5-b) ve makalede Results'a
> girer. Değişen şey, off'un bir **alternatif rejim** olarak raporlanmayı bırakması.
>
> **Kabul edilen bedeller aynen duruyor:** M5 ezber kütlesi 36.9→42.5 (ADR-0040'ı 🟡 yapan
> muhafız ihlali) · base tarafında 4.5× token (`τ_g` 772, kendi istem ailesinde **476** —
> orada Gemini'nin 543'ünün altında) · iz hâlâ İngilizce, ürünün *"okunabilir muhakeme"*
> vaadi bugün karşılanmıyor (m.6 açık kalemi).

---

## Bağlam

ADR-0040 düşünce modunu **ölçmeye** karar vermişti ve ön-kayıtlı bir eşik yazmıştı. Ölçüm koşuldu
ve **kural öngörmediği bir dala çarptı**: base, `--thinking on` altında karar eksenlerinin
bulunduğu üç modda (M1 · M2 · M5) `</think>`'i **hiç kapatmıyor**, `content` boş dönüyor, yani
puanlanacak cevap **üretilemiyor.** Bu bir kesilme değil **sonlanmama**; bütçeyi 4096 → 32768
(8×) çıkarmak, örneklemeyi Qwen'in önerdiği `temp 0.6 / top_p 0.95` yapmak (yarısını kurtardı) ve
kuantizasyonu Q8_0'a yükseltmek **çözmedi**. Mekanizma ölçüldü: model *"kaynaktan cevapla"* ile
*"kaynakta yoksa 'bulunmuyor' de"* arasında salınıp aynı muhakeme satırını **219 kez** tekrarlıyor.

Aynı ölçümde ikinci bir şey görüldü: **`τ_g` v1 aynı istemlerde düşünüyor ve duruyor** —
35/36 örnekte kendi kapatıyor, medyan 452 token, düşünce izinde tekrar yok, iz yapılı.

**Ve konuyu kapatan şey ölçüm değil, ürün kararı oldu** (kullanıcı, 2026-07-29):

> *"--thinking off istemiyorum, bu model kökünde think ediyor, neden sakat bırakıyoruz. Final
> hand-crafted modelim think edebiliyor ve onun token'ları da okunabiliyor olmak ZORUNDA."*

## Karar

### 1. Hat **thinking-on** koşar — ADR-0030 madde 2 düşer

Eğitim, eval ve dağıtım `--thinking on` ile gider. **Bu karar ürün gereksinimiyle alındı,
ölçümle değil** — ve öyle yazılır. ADR-0040'ın eşiği *"düşünce sayıları yükseltiyor mu"* sorusuna
bakıyordu; buradaki gerekçe farklı: **düşünen bir base seçip düşünmeyi kapatmak, seçilenin bir
kısmını kullanmamaktır**, ve ürünün vaadi denetlenebilir bir muhakeme izidir.

ADR-0030'un üç gerekçesinin bugünkü durumu:

| ADR-0030'un gerekçesi | bugün |
| :--- | :--- |
| **Eğitim-eval hizalaması** (SFT verisinde iz yok) | 🟡 Kısmen geçersiz: `τ_g` izsiz veriyle eğitildiği hâlde düşünüyor **ve** düşünmesi base'den **daha kararlı** (#42 §5). Yine de tam hizalama izli veri gerektirir → §4 |
| **Sessiz çöp koşusu riski** | ✅ Ortadan kalktı: bütçeli kapatma + boş cevapta erken patlama |
| **Maliyet** | 🔴 **Gerçek ve ödeniyor:** 249 → ~1.198 token (**~4.8×**). Kapı değil, ADR-0017 muhasebesine yazılan bir kalem |

### 2. Protokol: **bütçeli düşünce** — düşünce 1024 + cevap 512, ön-kayıtlı

```
1) Düşünceye 1024 token izin ver           (enable_thinking=true)
2) content boşsa → ham istem + üretilen iz + "</think>\n\n"
3) /completions ile devam → cevap 512 token bütçesinde yazılır
```

**Bütçe ön-kayıtlıdır ve sonuca göre değiştirilmez.** Gerekçe: base'in doğal olarak sonlanabildiği
en ucuz mod (M3) ortalama **1.126** token harcıyor, `τ_g` medyanı **452** — 1024 keyfi bir sayı
değil, *"yeterince düşünmüş"* sayılabilecek ölçülmüş bir bant. Cevap bütçesi **512**, Sprint 1 ile
birebir aynı.

Uygulama: `gen_eval_grounded.py --think-budget N` (`render_prompt()` + `GenOut.forced_close`).
Zorunlu kapatma oranı ve `completion_tokens` her koşuda künyeye yazılır.

### 3. Düşünce bütçesi bir **rejim değişmezidir**

`seed 3407` ve `--max-chunk-chars 900` ile **aynı statüde**: bütün özneler, bütün kollar, bütün
kafes hücreleri ve bütün rakipler **aynı bütçeyle** koşar. Sapma hata vermez, sadece kıyası
geçersiz kılar (`TASARIM.md` §4.1.1, ADR-0036'nın rejim eşleşmesi kuralı).

### 4. Sprint 1'in üç çıpası **yeniden koşulur**

base · Gemini 3.1 Flash-Lite · `τ_g` v1 — üçü de `--thinking off` ile ölçüldü. Yeni protokolde
`τ_a`'nın referans noktası **0.6330 değildir**. Yeniden koşu: 3 özne × 6 mod = **1.410 cevap**,
GPU $0 (yerel/Modal), Gemini + hakem ≈ **$0.5-0.6**. Sprint 1 sayıları **silinmez** — thinking-off
protokolünün kaydı olarak durur ve iki kip yan yana raporlanır.

### 5. ADR-0040'ın ön-kayıtlı kuralı **iptal değil, ertelendi**

🟢🟡🔴 eşiği bütçeli kipte yeniden koşulur ve raporlanır. Artık *"thinking açılsın mı"* sorusunu
değil — o karar verildi — **RS-FT'nin gerekliliğini** belirler: base bütçeli düşünceyle `τ_a`'nın
işinin çoğunu yapıyorsa, iç iddiada üçüncü açıklama (kazanç modelin kendi düşünme yeteneğinden)
belirir ve **daraltıcı bulgu olarak yazılır** (ADR-0040'ın kendi şerhi).

### 6. Türkçe iz — **açık iş kalemi**, bugün hattı durdurmaz

Ölçüldü: iz **8/8 İngilizce**, cevap **8/8 Türkçe**. Ürün gereksinimi *"token'lar okunabilir"* ise
bu bir **eğitim hedefi** hâline gelir ve izli/Türkçe veri gerektirir → `τ_g` v2. Karar, v2'nin
diğer üç gerekçesiyle **birlikte** verilir ([`docs/record/kollar.md`](../record/kollar.md)); ayrı
ayrı eğitim iki kat para ve iki kat kafes ölçümü demektir.

## Değerlendirilen alternatifler

| eleme | gerekçe |
| :--- | :--- |
| **Thinking-off'ta kalmak** (ADR-0040'ın 🔴 dalı) | Ürün gereksinimiyle çelişiyor. Ayrıca *"tam kapasiteyi ölçmedik"* itirafı, *"ölçemedik çünkü model durmuyor"* hâline gelirdi — daha kötü bir Limitations satırı |
| **Bütçeyi büyütüp beklemek** | Ölçüldü: 8× artış 0/2'yi değiştirmedi. Tam koşu ≈ 20+ saat GPU, sonunda yine "geçersiz koşu"; üstelik 32k token/cevap ADR-0017 muhasebesini tek başına yıkar |
| **Örneklemeyi değiştirmek** (`temp 0.6`) | Yarısını kurtardı, çözmedi (%50 başarısızlık, 6.918 tok). Ve Sprint 1 çıpaları `temp 0` — düşünce kazancı örnekleme değişikliğiyle **karışırdı** |
| **Sistem istemindeki çekimserlik talimatını yumuşatmak** | Döngüyü kırardı ama **ölçülen görevi değiştirirdi**: o talimat karar eksenlerinden birinin (abstention) ta kendisi |
| **Daha büyük/başka base** | ADR-0028'in tek-boyut kuralına aykırı |
| **`--reasoning-budget` benzeri sunucu bayrağına güvenmek** | llama.cpp'de düşünceyi **kapatan** bir anahtar var, **N token'da kesip kapatan** yok. İstemci tarafında iki geçiş tek taşınabilir yol — ve rakiplerle aynı kod yolundan geçer (adalet kuralı) |

## Sonuç — kabul edilen bedeller

- **Maliyet ~4.8×** (249 → ~1.198 token/cevap). Parite iddiasının maliyet ekseninde **doğrudan
  görünür**; gizlenmez, ADR-0017 muhasebesine yazılır. *(Not: `τ_g` base'in bütçesinin yarısından
  azını harcıyor — düşünce maliyeti de kolla düşüyor.)*
- **Zorunlu kapatma düşünceyi ortadan keser.** n=2 doğrulamasında cevaplar tutarlı ve atıflı çıktı,
  ama bu bir **protokol müdahalesidir** ve Methodology'de öyle anlatılır. Kesilme oranı her koşuda
  raporlanır.
- **Sprint 1'in sayıları protokol değiştirdiği için çıpa olmaktan çıktı** — silinmiyor, iki kip
  yan yana veriliyor; ama takvim ve ~$0.6 maliyet bu ADR'nin faturasıdır.
- **İz dili İngilizce** — ürün vaadi *"okunabilir muhakeme"* ise bugün **tam karşılanmıyor**;
  Limitations'a yazılır ve v2'nin gerekçelerine eklenir.
- `runs=1`, güven aralığı yok — Kapı 5/6 ile aynı sınır.
