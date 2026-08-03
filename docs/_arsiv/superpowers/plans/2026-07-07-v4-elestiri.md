# v4 Execution Plan — Dış Eleştiri & Revizyon

> Kaynak: `docs/superpowers/plans/2026-07-06-v4-execution.md` + v3 ham çıktılar (`bench_*_v3_detail.jsonl`, `sonuclar.md`).
> Amaç: v4'ü onaylamak/reddetmek değil — **başarısızlık senaryosunu önceden tanımlamak** ve tek yüksek-kaldıraç değişkeni tahminden taramaya çevirmek.
> Kapsam: yöntem doğru, iki boşluk var. Gerisi dokunulmaz.

---

## 1. Genel yargı

**Plan sağlam. Yöntem sıçraması zaten içinde.** v3'ün kök sorunu (forced-source-selection) plan tarafından semptomda değil kaynakta hedefleniyor. Beklentinin üstünde.

| Eksen | Durum |
|---|---|
| Teşhis (answerability = tek beceri, aile değil) | ✅ doğru, Entry 33 reframe korunmuş |
| DTA gold-as-rejected (Task 4) | ✅ zaten var — ayrı yöntem değil, ORPO verisinde 1 satır |
| Forced-source-selection kırma (Task 2 sufficiency-structure) | ✅ kaynakta çözüyor |
| Parametrik-probing atma (2-quadrant) | ✅ doğru sadeleştirme |
| Whack-a-mole guard (kapıda `M1/M4/M3/register ≥v3`) | ✅ over-reject'i yakalar |
| **M2-fail off-ramp** | ❌ tanımsız → Revizyon 1 |
| **ORPO hparam + gold-absent oranı pinlenmemiş** | ❌ tahmin → Revizyon 2 |

---

## 2. DTA yanlış-anlaşılması (netleştirme)

DTA **ORPO'nun yanına eklenen ayrı bir şey değildir.** Ayrı model / ayrı loss / ayrı eğitim yoktur.
Planda Task 4'teki tek satırdır:

```
gold-absent çiftlerde EK rejected = gold_text   # DTA: doğru-cevabı da cezala → şanslı-tahmin kes
```

Öğrettiği: *"bağlam desteklemiyorsa, doğru-görünen kelimeler bile yanlış cevaptır."*
Aynı ORPO loss'unun içinde, sadece veri hazırlığında çalışır. **v4'e yöntem olarak ekleme gerekmiyor.**

> "Ayrı sufficient-context head" fikri **v4 değil, v5 yedeğidir** — sadece v4 kapıyı geçemezse. Aşağıda Revizyon 1'de.

---

## 3. Kapı (plandan, doğrulanmış)

```
M2b ≥0.90 · M2 ≥0.704 · xkanun ≥0.90 · ood ≥0.75 · M4/M1/M3/register ≥v3 · M5 ≤0.10
```

Kapı iyi tasarlanmış: over-reject guard'ı (`M1/M4 ≥v3`) içinde. **Eksik olan kapının kendisi değil, "tutmazsa ne olacağı".**

---

## 4. REVİZYON 1 — M2-fail off-ramp (pre-registered karar)

**Sorun:** `M2 ≥0.704` kapısı var ama tutmazsa ne yapılacağı yazılı değil → başarısızlıkta "biraz daha negatif ekle" refleksi riski.

**Ekle → Task 9:**

```md
### Task 9 — Kapı sonrası karar (önceden yazılı)
- M2 ≥0.704 VE M2b ≥0.90            → v4 teslim-adayı.
- M2b ≥0.90 AMA M2 <0.704           → M2b onarıldı, M2 borcu SÜRÜYOR.
    Kök neden ilanı: "az negatif" DEĞİL "yanlış araç".
    → v5 = answerability'yi ORPO loss'undan AYIR (sufficient-context head).
      Daha fazla ORPO-negatifi DENEME. (tekrar aynı duvar)
- M2 tuttu AMA M1<v3 veya M4<v3      → DTA cezası aşırı bastı (over-reject).
    → beta düşür / gold-as-rejected oranını kıs (Revizyon 2).
```

Kazanç: her başarısızlık türü bir sonraki adımı deterministik tetikler. "Çalışsın" değil, verifiable kapı.

---

## 5. REVİZYON 2 — hparam + gold-absent oranını pinle (+1 sweep)

**Sorun:** Plan `beta / lr / grad_accum` vermiyor, sadece `--epochs`. Ama DTA gold-as-rejected loss manzarasını değiştirdi → `beta` bu tahterevallinin ayar vidası. v3 beta=0.1'i körlemesine taşımak over-penalize riski.

**Ekle → Task 8:**

```md
### Task 8 — ORPO v4 hparam (pinned + 1 ablasyon)
- Sabit: lr=1e-5, grad_accum=64, epochs=2, seed=3407.   # v3 ile aynı
- beta ablasyonu: {0.1, 0.05}
    # DTA eklendiği için beta daha sert ısırıyor.
    # Smoke'ta ikisini koş, M1/M4 gerilemeyeni seç.
- gold-as-rejected oranı: gold-absent çiftlerin %100'üne DEĞİL, önce %50'sine.
    # Neden: %100, gold-PRESENT vakalara "doğru metne güvenme" olarak
    # sızıp M4 oracle'ı düşürebilir. M2b yetmezse %100'e çıkar.
```

---

## 6. Başarıyı yükselten eklemeler (garanti yok — risk azaltır)

> v4'ün kaderi tek sayıya bağlı: **eğitim setinde gold-present : gold-absent oranı.** Bu tahterevallinin ta kendisi.
> Çok no-gold → over-reject (M1/M4↓). Az no-gold → M2b kapanmaz.

**Ekle → yeni Task 8.5:**

```md
### Task 8.5 — Oran sweep + ucuz kanarya
1. gold-absent PAYINI tara (oranın kendisi, gold-as-rejected'dan ayrı):
   {%20, %35, %50}. Smoke, seç: M2b↑ VE M1/M4 korunan.
2. Kanarya (A100 harcamadan): eğitim biter bitmez ~10 örnek
   "gold VAR ama zor" (M4/M1 alt kümesi) koştur.
   Model bunlarda reddediyorsa → over-reject, tam eval'e GİRME, oranı geri çek.
3. Checkpoint: 1-epoch (ck-yarı) + final ikisini de ölç (v3'te ck28 gibi),
   M1/M4 gerilemeyeni seç. Over-reject genelde fazla-eğitimle gelir.
```

**Prerekizit (eğitimden ÖNCE):**

```md
- 108 "kazara-cevaplayan" (accidental-answerers) TEMİZLENMİŞ olmalı.
  Task 3 gray-band judge bunu yapıyor → BİTTİĞİNİ doğrula, bitmeden v4 BAŞLATMA.
  # Kirli pozitif = yanlış "cevapla" sinyali = M2'yi baştan sabote eder.
```

---

## 7. İzleme notu (revizyon değil)

DTA cezası agresif. Doğru-cevap-metnini rejected'a koymak abstention için iyi ama **M4 (oracle) hücresine sızabilir.** Kapıda `M4 ≥v3` zaten var → yakalanır. Sadece M4 düşerse sebebi budur, önden bil, panik yapma; oran/beta ile geri çek.

---

## 8. Tek cümlelik özet

Yöntem tamam, DTA zaten içeride — **v4'e teknik ekleme gerekmiyor.** İki revizyon (off-ramp + hparam/oran pinle) ve iki ucuz güvence (kanarya + prerekizit temizlik) planı "başarısızlıkta ne yapacağını önceden bilen" hale getiriyor. v4'ün başarısız olacağı tek gerçekçi senaryo gold-present:absent oranının yanlış sabitlenmesi — onu taramaya çevir, riskin çoğunu kapattın.
