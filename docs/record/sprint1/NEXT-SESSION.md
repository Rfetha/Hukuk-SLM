# NEXT SESSION — Sprint 2 başladı (2026-07-29)

> **Bu belge ne:** oturumlar arası devir notu.
> ⚠️ Önceki içerik (Sprint 1 kapanış notu) **değiştirildi** — Sprint 2 planlandı ve yazıldı.

---

## Durum

| | durum |
| :--- | :--- |
| Sprint 1 (CP0-CP7) | ✅ **KAPANDI** — [`sprint1.md`](../../../sprint1.md) arşiv |
| Sprint 2 | 🟢 **PLANLANDI** — ⭐ yürütme belgesi [`sprint2.md`](../../../sprint2.md), **hiçbir CP koşulmadı** |

## Sıradaki iş — `sprint2.md` **CP0**

**Düşünce modu ölçümü.** Sprint 2'nin 1. günü, ~$0.15, ikisi de yerel:

| | ne | çıktısı |
| :-- | :--- | :--- |
| **CP0-a** | base, DEV, `--thinking on`, **4096 token** + kesik sayacı | 🟢🟡🔴 → RS-FT kararı ([ADR-0040](../../adr/0040-dusunce-modu-olculecek-on-kayitli-kural.md)) |
| **CP0-b** | `τ_g`, `--thinking on`, ~20 çıktı **gözle** | reçete fazla sert miydi → `τ_g` v2 hipotezi |

🚨 **Geçerlilik ön şartı:** kesik-cevap > %5 ise **koşu geçersiz** — sonuç okunmaz, bütçe artırılır.
*(ADR-0030 ölçtü: 1024 token'da `</think>` kapanmıyor, `content` boş dönüyor, HTTP 200.)*

**Neden ilk sırada:** sonucu RS-FT kararını, `τ_a`'nın referans noktasını ve olası bir `τ_g` v2'yi
belirliyor. Sonra koşulursa arkasındaki her şey yanlış varsayımla koşulmuş olur.

## Bu oturumda verilen kararlar (grill, 2026-07-29)

| ADR | karar |
| :--- | :--- |
| [0039](../../adr/0039-kapi-6-parametrik-sizinti.md) | Kapı 5'in **(d) maddesi ayrıldı → Kapı 6**. Çıpa **base** (rakip değil): M5 coverage ≤ %37.5 · ezber kütlesi ≤ %10.7. `τ_g` bugün **kalıyor** ve öyle raporlanıyor |
| [0040](../../adr/0040-dusunce-modu-olculecek-on-kayitli-kural.md) | Düşünce modu **ölçülecek**, ön-kayıtlı 🟢🟡🔴 kuralı. RS-FT'nin tetikleyicisi. Kalıcı kural: kol yeniden eğitilirse **düşünme korunur** |
| [0041](../../adr/0041-raft-meta-iddia-hakem-kurali.md) | §13.8 **A** ile kapandı — hakem istemine muafiyet satırı, **TÜM kollara aynı anda**, ham sayılar da yayımlanır |
| [0042](../../adr/0042-rejected-havuzu-tek-kaynak-ve-on-policy-kontrol.md) | `rejected` **tek havuz ham base'den** + **FT-6 on-policy kontrol koşusu** (~$0.65) |
| — | Tabanlar **ARA KAPI'dan sonra**: `τ_a` M2 Rej ≥ 0.75 geçmezse rakiplere ~$12 harcanmaz |

## Bütçe

Modal cap **$42.50** · harcanan ~**$5.8** · Sprint 2 tahmini ~**$13.2** · kalan ~**$23.5**.
⚠️ CP0-a **YEŞİL** çıkarsa bütçe ve takvim yeniden hesaplanır (~3-4 hafta uzama).

## Ortam notu

`.wslconfig`'e `memory=24GB` eklendi mi kontrol et — merge tepe RSS **9.86 GB** yapmıştı, Sprint 3'ün
k-yollu TIES'i daha fazlasını isteyecek. `free -g` ile doğrula.
