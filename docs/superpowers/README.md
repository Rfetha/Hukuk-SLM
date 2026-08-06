# `docs/superpowers/` — planlar ve spec'ler

`superpowers` skill'lerinin ürettiği belgeler burada durur. **Kayıt değildirler** —
*ne yapılacağını* söylerler, *ne olduğunu* değil.

| klasör | ne | yaşam döngüsü |
| :--- | :--- | :--- |
| [`specs/`](specs/) | tasarım/kapsam belgesi — `brainstorming`, `grill-with-docs` çıktısı | onaylanır, uygulanınca kaynak olarak kalır |
| [`plans/`](plans/) | uygulama planı — `writing-plans` çıktısı, `- [ ]` kutucuklu | koşarken kutucuklar **işaretlenir** + bir **İCRA DURUMU** bloğu tutulur |

🔁 **KURAL DEĞİŞTİ — 2026-08-05 (insan kararı).** Önceki kural *"kutucuklar işaretlenmez,
plan tarihî bir belgedir"* idi. Gerekçesi hâlâ geçerli ama **yetersiz çıktı**: bu, aralıklı
çalışan tek kişilik bir projedir ve *"planın neresindeyiz"* sorusunun **plana bakarak**
cevaplanabilmesi gerekiyor. Sohbet kaybolur, plan kalır.

**Yeni kural — üç parça, üçü de ayrı iş:**

| ne | nereye | biçim |
| :--- | :--- | :--- |
| **niyet** | planın gövdesi | `- [ ]` adımlar — yazıldığı gibi kalır, **geçmişe dönük düzeltilmez** |
| **ilerleme** | planın `İCRA DURUMU` bloğu | `[x]` bitti · `[~]` koşuyor · `[ ]` sırada + sapmalar + bulunan kusurlar |
| **sonuç** | `docs/record/research_log/` | sayılar, mekanizma, ders |

⚠️ **Değişmeyen kısım:** plan **sonuç belgesi değildir**. Sayılar `research_log`'a, kararlar
`docs/adr/`'ye gider; plan yalnız o ikisine **işaret eder**. İCRA DURUMU bloğu *"ne oldu"*
değil *"nerede kaldık ve plan nerede yanlıştı"* yazar.

⭐ **Neden "plan nerede yanlıştı" da yazılıyor:** ilk koşuda bu planda **beş** sessiz-yanlışlık
kusuru bulundu (yanlış payda, düşmüş rejim bayrağı, imkânsız bir okuma cümlesi, yanlış kıyas
uzayı, iki ayrı yeri karıştıran bir talimat). Hiçbiri hata vermezdi. Bunları plana **geri
yazmazsan** bir sonraki plan aynı kusurla doğar.

## Şu an

| belge | durum |
| :--- | :--- |
| [`plans/2026-08-03-s3a-on-prob.md`](plans/2026-08-03-s3a-on-prob.md) | ✅ uygulandı 2026-08-04 → [#49](../record/research_log/2026-08-04-s3a-on-prob.md) · [ADR-0054](../adr/0054-harness-tasarim-kararlari-k2-k5.md) |
| [`plans/2026-08-05-olcum-bosluklari.md`](plans/2026-08-05-olcum-bosluklari.md) | ✅ **uygulandı 2026-08-05** → [#56](../record/research_log/2026-08-05-olcum-bosluklari.md) · [ADR-0056](../adr/0056-m2b-harness-acik-protokolu-ve-0055-cipasi.md) · [ADR-0057](../adr/0057-harness-rekabet-kapisi-esit-sinav.md). 6/6 görev, GPU $0 + hakem $0,075. Planın **5 sessiz-yanlışlık kusuru** İCRA DURUMU bloğunda |
| [`specs/2026-08-03-yol-haritasi-design.md`](specs/2026-08-03-yol-haritasi-design.md) | onaylandı — yürürlükteki özet [`ROADMAP.md`](../../ROADMAP.md) |

Arşive alınmış eskiler: [`../_arsiv/superpowers/`](../_arsiv/superpowers/)
