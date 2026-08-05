# `docs/superpowers/` — planlar ve spec'ler

`superpowers` skill'lerinin ürettiği belgeler burada durur. **Kayıt değildirler** —
*ne yapılacağını* söylerler, *ne olduğunu* değil.

| klasör | ne | yaşam döngüsü |
| :--- | :--- | :--- |
| [`specs/`](specs/) | tasarım/kapsam belgesi — `brainstorming`, `grill-with-docs` çıktısı | onaylanır, uygulanınca kaynak olarak kalır |
| [`plans/`](plans/) | uygulama planı — `writing-plans` çıktısı, `- [ ]` kutucuklu | uygulanınca **üstüne ✅ kapanış kutusu** konur, kutucuklar **işaretlenmez** |

⚠️ **Kutucuklar neden işaretlenmiyor:** plan, yazıldığı andaki hâliyle **tarihî bir
belgedir** — *"o gün ne yapmayı planlamıştık"* sorusunun cevabı. İlerleme takibi onun
işi değil. *Ne olduğu* `docs/record/research_log/`'ta durur.

**Kural:** bir plan koştuktan sonra sonuçları **buraya yazılmaz**. Sonuç `research_log`'a,
karar `docs/adr/`'ye gider. Plan yalnız o ikisine **işaret eder**.

## Şu an

| belge | durum |
| :--- | :--- |
| [`plans/2026-08-03-s3a-on-prob.md`](plans/2026-08-03-s3a-on-prob.md) | ✅ uygulandı 2026-08-04 → [#49](../record/research_log/2026-08-04-s3a-on-prob.md) · [ADR-0054](../adr/0054-harness-tasarim-kararlari-k2-k5.md) |
| [`plans/2026-08-05-olcum-bosluklari.md`](plans/2026-08-05-olcum-bosluklari.md) | ▶ **koşulmayı bekliyor** — kararları [ADR-0056](../adr/0056-m2b-harness-acik-protokolu-ve-0055-cipasi.md)'da |
| [`specs/2026-08-03-yol-haritasi-design.md`](specs/2026-08-03-yol-haritasi-design.md) | onaylandı — yürürlükteki özet [`ROADMAP.md`](../../ROADMAP.md) |

Arşive alınmış eskiler: [`../_arsiv/superpowers/`](../_arsiv/superpowers/)
