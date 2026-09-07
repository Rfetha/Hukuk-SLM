# Yarın devam notu — Faz 0 kapanışı + sıradaki plan

**Yazıldı:** 2026-09-07 · **Durum:** Faz 0 **39/40**, 42 commit, ağaç temiz, süreç yok

## AŞAMA 1 — Faz 0'ı 40/40'a tamamla

**Plan:** `docs/superpowers/plans/2026-09-06-faz0-olcum-zinciri.md`
**Kalan tek ölçüm:** M5 → ADR-0064 madde (3) → kapanış.

⚡ **ÖNCE ŞARJ.** Künyede `güç : ŞARJDA` yazdığını doğrula. Pilde GPU **P5 · 180 MHz**'e
kısılıyor (8,4 t/s) → 80 kalem **4,8 saat**; şarjda **~57 dk**. Sayı değişmez, süre değişir.

### Nerede kaldık
| eksen | değer |
| :--- | ---: |
| kütle | **%80,1** |
| `recall@10` | 0,9500 |
| aşırı-red | 4/80 |
| isabetsizlik | 8/80 |
| uydurulmuş madde | 0/114 |

Hepsi **sıfır eğitim koşusuyla** — aletin dört kusuru bulunarak (soru seti · füzyon ·
DEV↔TEST bileşimi · rakiple eşit olmayan üretim bütçesi).
`v1.0` kapısı **madde (1) GEÇTİ**: GÖZ-katı okumasında **+5,86 p**.
ADR **0063-0070** · research_log **#62** · S1·S2·S11·S14·S15 kapandı.

### Adımlar
1. `outputs/eval/f07-m5-anti-hedef/DURUM.md`'deki komutu koş (`setsid nohup`, ayrık)
2. Geçerlilik kapısı (kesik ≤%5) → M5'i puanla. **`scripts/cp0_thinking_score.sh` arayüzünü
   koşmadan ÖNCE oku** (plandaki komut yanlış bayrak taşıyor olabilir — bu tur üç kez oldu)
3. **ADR-0064 madde (3)**'ü sayıyla kapat: M5 bugünkü değerin **üstüne çıkmamalı**
   (anti-hedef, ADR-0039/0040). Yükselmişse kazancın bir kısmı **ezberden** gelmiştir ve
   bu açıkça yazılır.
4. Plan **40/40** · künye · commit · **Faz 0 kapanış özeti**

### Kapanış özetine girecek iki insan kararı (2026-09-07 — ADR yaz, sıradaki **0071**)

**A) `v1.0` release artefaktı:** adaptörler merge edilmiş **TEK bir GGUF**; dosya adı
**model + boyut + sürüm + KUANTİZASYON** taşır → `HakHukuk-4B-v1.0-Q4_K_M.gguf`.
İç ad `tgta_v1-q4_k_m.gguf` izlenebilirlik için **korunur**; dışa dönük ad ayrı
(`kollar.md`'nin *"iki ad ayrı iş görür"* kuralı zaten bunu söylüyor).

**B) `v1.0` rakip havuzu genişler:** yalnız Gemini değil, **diğer sağlayıcıların
3.5-Flash seviyesindeki** modelleri de.
⚠️ **AİLE DIŞLAMASI ENGELİ (ADR-0032):** hakem `openai/gpt-4o-mini`. Bir **GPT öznesi**
eklemek hakemi değiştirmeyi **ve bugünkü dört sayıyı yeniden koşmayı** gerektirir.
**Claude Sonnet sorunsuz** (Anthropic özne ↔ OpenAI hakem). ⇒ **T1 önce gelir.**

## AŞAMA 2 — sıradaki planı YAZ (koşma)

`superpowers:writing-plans` ile. Spec hazır:
`docs/superpowers/specs/2026-09-06-yeni-belge-katmani-design.md`

🔒 **SIRALAMA KİLİTLİ (insan kararı 2026-09-07): T1 → Hat A (paralel, $0) → Hat B**

### T1 · Hakem paneli (~$3-5) — ÖNCE
Bugünkü **her** sayı tek ailenin (`gpt-4o-mini`) hükmü; **κ yok**, self-preference
ölçülmedi. Panel kurulmadan yeni rakip eklemek, aynı şüpheli hakemle daha çok sayı
üretmek olur. 3 aile + aile dışlaması + κ (`scripts/judge_agreement.py` **var**).
⇒ **B kararının (GPT öznesi) ön koşulu da budur.**

### Hat A · Paketleme ($0, GPU yok, T1'e paralel) → `v0.2`
| # | iş |
| :-- | :--- |
| A1 | **İstem artefaktı** — YB6, **sert engel**: istem yalnız `gen_eval_grounded.py` içinde |
| A2 | **CLI servis katmanı** — `answer(soru) → {cevap, atıflar, kaynaklar}` |
| A3 | İndeks dağıtımı (80 MB) — **AÇIK KARAR S8** |
| A4 | Yeniden üretim yolu — tek komut |
| A5 | MODEL_CARD/README **tam yazım** (bugün yalnız "eski birim" bandı çakıldı) |
| A6 | Sorumluluk ibaresi — **AÇIK KARAR S10** |
| A7 | Basit **TUI** (`textual` adayı) |
| A8 | **`suskunluk_terazisi`'ni ürün yüzeyine taşı** — dürüst suskunluk · çekinceli cevap rozeti · uydurulmuş atıfın kullanıcıya gitmeden yakalanması |

### Hat B · Model (~$7-15, Modal) → `v1.0`
`B1` isabetsizlik 8/80, reddetme-örneklemesi (ADR-0066) ~$5 ·
`B4` `τ_a` genliği (0,987→0,766 seyrelme) ~$1,3 · `YB2` M2b · kapı koşusu ~$1

**Plan formatı:** her adım `ne · neden (hangi ölçülmüş boşluk) · verify: · bedel · bağımlılık`.
Kritik yol işaretli. **AÇIK KARAR** damgaları: S5 · S7 · S8 · S9 · S10 · S12.
⛔ **Planı YAZ, UYGULAMA.** Yazınca DUR ve insan onayı iste.

## Kilitli kararlar (yeniden sorulmaz)
1. `v1.0` kapısının **bağlayıcı okuması = GÖZ-katı**; ALET/GÖZ-orta yan sütun
2. Kapı madde (2) çıpası **8/80** (v2 birimi, gözle sayılmış) — kural *"gerileme yok"*
3. Kapı madde (3) — **M5 yükselmez**
4. Sıralama **T1 → Hat A ∥ → Hat B**
5. Bütçe: ~~OpenRouter **~$8,88**~~ 🚨 **ÖLÇÜLDÜ 2026-09-07: $6,60** (`total_credits` 20 −
   `total_usage` 13,397; $2,28'i bu plan dışından) · Modal **$29,19** · bugün harcanan **$1,38**

## Çalışma kuralları
- Yolda çıkan sorunu **açık bırakma**, çözerek git; her tuzağı plana yaz
- Uzun koşuları **`setsid nohup … &`** ile ayrık başlat; çıktıyı `| tail`'a **sokma**
- Her adımda **plan-göreli STATUS**: hangi görev, kaç kutucuk, ne harcandı
- **Sayı hatırlanmaz, kaynaklanır.** Çelişki **iki yerde** işaretlenir
- **Gözle okuma bir kapıdır** — sayısal kapı bu tur dört kusuru birden geçirdi
- Kutucuk **yalnız `verify:` çıktısı GERÇEKTEN alındıktan sonra** işaretlenir
- **ADR-0059 REZERVE.** Sıradaki ADR **0071**
- ⛔ **DUR ve sor:** yeni rejim kararı · **>$1 harcama** · donmuş TEST'in açılması ·
  Aşama 2'nin planını **uygulamaya** geçmek
