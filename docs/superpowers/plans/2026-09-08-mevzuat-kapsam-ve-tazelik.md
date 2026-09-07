# Mevzuat kapsamı ve tazelik — uygulama planı

> **Ajan işçiler için:** ZORUNLU ALT BECERİ — bu planı görev görev uygulamak için
> `superpowers:subagent-driven-development` (önerilen) ya da `superpowers:executing-plans`
> kullan. Adımlar `- [ ]` kutucuklu.

**Hedef:** Korpusu 40.496 maddeden ~340.303'e **kat kat, her katı bir kapıdan geçirerek**
büyütmek; ve korpusu *tarihi belli, tazelenebilir, geri alınabilir bir anlık görüntüye*
çevirmek — ürün ağa dokunmadan çalışmaya devam ederken.

**Mimari:** Üç sorumluluk, üç zaman ölçeği (spec §3). ① `hakhukuk/mevzuat/` altındaki dört
dar birim canlı bedesten API'sinden **fark tarar** ve anlık görüntüyü **hepsi-ya-da-hiçbiri**
yazar; ② indeksleme yalnız değişen maddeleri yeniden gömer; ③ erişim kullanıcının makinesinde
**ağa dokunmaz**. Kapsam genişlemesi ayrı bir eksendir ve **ön-kayıtlı bir `recall@10` kapısıyla**
kat kat girer.

**Teknoloji:** Python 3.11 · `urllib` (stdlib, `bedesten_probe.py` deseni) · `numpy` fp32 ·
`rank_bm25` · `sentence-transformers` (`BAAI/bge-m3`) · `pytest`.

**Kaynak spec:** [`specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md`](../specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md)
(insan onaylı) · **iş sırasındaki yeri:** [`README.md`](../README.md) — ana plandan **sonra**.

---

## Global kısıtlar

Her görevin gereksinimleri bunları **örtük olarak içerir**. Değerler spec'ten ve
`CLAUDE.md`'den **birebir** kopyalandı.

| kısıt | değer | kaynak |
| :--- | :--- | :--- |
| Gömme dtype | **`fp32` KALIR** — `fp16` ölçüldü ve reddedildi (44,4× yavaş, 10/80 sorguda ilk-10 değişiyor) | spec §7b |
| Vektör veritabanı | **YOK** — kaba kuvvet bu ölçekte ayakta (~0,8 sn/sorgu) | spec §7b |
| RRF | `RRF_K = 10` (ADR-0068) — ölçüm ile ürün **aynı** yolu kullanır | `retriever.py`:43 |
| Seed | **3407** | ADR-0043 |
| Chunk | **tam madde** (ADR-0054/K2) — indeks kırpılmaz | `retriever.py`:18 |
| TR IP | **şart**, ⛔ **cihaz içi fallback YOK** — `TrIpGerekli` atılır, yutulmaz | spec §4 |
| Yazma | ⛔ **hepsi ya da hiçbiri** — kısmi tazeleme diske yazılmaz | spec §4 |
| Bool bayrak | ⛔ public API'de yok — `Tazelik` enum | `CLAUDE.md` §4 |
| Kapsam kapısı | `recall@10 ≥ 0,9500` → kat girer; altında ⛔ **girmez** | spec §5, ön-kayıtlı |
| Veri lisansı | yalnız açık kaynak (bedesten/Mevzuat.gov.tr). ⛔ Lexpera · Kazancı **asla** | `CLAUDE.md` |
| Dil | belge ve commit **Türkçe**, kod tanımlayıcıları **İngilizce** | `CLAUDE.md` |
| Dokunulmaz | ⛔ `docs/record/**` · `docs/adr/**` — tarihsel kayıt | `CLAUDE.md` |
| ADR numarası | sıradaki **0074**; ⛔ **0059 REZERVE** | `CLAUDE.md` |

### ⛔ DUR ve SOR — bu planda tetiklenecek yerler

- **Görev 7'nin gömme koşusu tek adımda >$1'dır** (Modal GPU ~1,5 sa). Koşmadan **sor**.
- Bir kat kapıdan **kalarsa** eşiği değil aleti düzelt (ADR-0050); kat girmez, **insana sor**.
- `kayitTarihi` testi (Görev 5 Adım 5) **çıkmazsa tasarım değişir** — o da insan kararıdır.

---

## Dosya yapısı

| dosya | tek sorumluluğu |
| :--- | :--- |
| `hakhukuk/mevzuat/__init__.py` | `tazele()` · `Tazelik` · `Rapor` — paketin **tek** dış yüzü |
| `hakhukuk/mevzuat/kaynak.py` | **bedesten sözleşmesi**. Sayfalama (max 20), `{"data":…}` sarmalaması, TR IP tespiti, geri çekilmeli retry **burada gizli** |
| `hakhukuk/mevzuat/tipler.py` | `Kayit` · `Fark` · `Kunye` · `Rapor` · `Tazelik` · `TrIpGerekli` — donmuş veri tipleri |
| `hakhukuk/mevzuat/tazelik.py` | **fark taraması** — yerel künye ↔ uzak `kayitTarihi`. ⛔ **ağa kendisi dokunmaz** |
| `hakhukuk/mevzuat/anlik.py` | **anlık görüntü** — sürümleme · künye · `sha256` · atomik yazma · geri alma |
| `hakhukuk/mevzuat/indeksle.py` | **artımlı gömme** — yalnız değişen `madde_id`'ler; indeks künyesini korpus künyesine bağlar |
| `scripts/erisim_korpus/kapsam_kapisi.py` | kapsam kapısının **aleti**: ürün retriever'ıyla `recall@10`, hakem yok, $0 |
| `scripts/erisim_korpus/korpus_kimlik.py` | korpusa `mevzuat_id` + `madde_id` geri doldurur (Görev 3) |

**Neden `hakhukuk/mevzuat/` ayrı bir alt paket** *(POSD silme testi)*: silinirse bedesten'in
tuhaflıkları — `pageSize` max 20, `guncellemeTarihi` boş, TR IP şartı, base64+HTML gövde —
**dört çağırana birden** yayılır. `hakhukuk/tipler.py` (ana planın Görev 6'sı) **ürün yüzeyinin**
tipleridir ve bu alt paketin tipleriyle **karışmaz**: biri vatandaşa dönen cevabı, diğeri
korpusun kendisini tarif eder.

---

## 🚨 Bu planın devraldığı iki ölçülmüş sürpriz

Bunlar spec yazıldıktan **sonra** ölçüldü ve spec'e damgalandı (§7b). Plan bunların üstüne kuruluyor.

**1 · Baskın sorgu maliyeti BM25, yoğun kol değil.** Spec'in *"340k'da ~51 ms"* sayısı yalnız
`q @ gomme.T`'yi sayıyordu. Ölçüldü:

| kol | 40.496 | 340.303 |
| :--- | ---: | ---: |
| **BM25** | **87,7 ms** | **713,8 ms** ← %89 |
| yoğun | 5,3 ms | 34,9 ms |
| RRF + argsort | 8,6 ms | 54,0 ms |
| **toplam** | ~102 ms | **~803 ms** |

Karar değişmiyor (0,8 sn hâlâ fark edilmez), **gerekçe** değişiyor — ve optimizasyon yönü
tersine döndü. RAM de öyle: BM25 ~741 MB + yoğun 1.394 MB ⇒ **~2,1 GB**.

**2 · Korpusta kararlı madde kimliği YOK.** `(kanun_no, madde_no)` **3.699** yerde çakışıyor;
metni de katınca hâlâ **538**. Bugünkü kimlik **satır sırasıdır**. Artımlı gömme bu zeminde
**yanlış satırı tazeler ve hata vermez** ⇒ Görev 3 kimliği **artımlıdan önce** kuruyor.

---

## Görev sırası ve bağımlılık

```
G1 kapsam kapısı aleti + ÇIPA   ← her şeyden ÖNCE: kapının çıpası yoksa kapı yoktur (tuzak 2.17)
 ├── G2 kaynak.py (bedesten)                    ─┐
 ├── G3 korpus kimliği (mevzuat_id · madde_id)   │  G4 ile paralel koşabilir
 └── G4 tipler + tazelik.py (saf, ağsız)        ─┘
        └── G5 anlik.py (atomik anlık görüntü + kayitTarihi sinyal testi)
              └── G6 indeksle.py (artımlı) + ÖLÇEK KAPISI
                    └── G7 kat kat kapsam girişi  ⚠️ >$1, DUR ve SOR
                          └── G8 tazele() ana arayüz + CLI
                                └── G9 ADR + kayıt + kapanış
```

---

### Görev 1: Kapsam kapısının aleti — ve ÇIPASI

**Dosyalar:**
- Create: `scripts/erisim_korpus/kapsam_kapisi.py`
- Create: `tests/test_kapsam_kapisi.py`
- Create: `outputs/eval/f12-kapsam-kapisi/CIPA_kat0.json`

**Arayüzler:**
- Tüketir: `retriever.Retriever` (`yukle` · `getir`) · `madde_anahtar.madde_anahtari`
- Üretir: `recall_olc(retriever, sorular, k=10) -> dict` — Görev 7 her katta bunu çağırır

**🚨 Neden bu görev BİRİNCİ:** Faz 0'ın en pahalı dersi **tuzak 2.17** idi — *"ön-kayıtlı bir
kapı maddesi, çıpası olmadan yazılmıştı"*. Spec'in kapısı `recall@10 ≥ 0,9500` diyor; bu sayı
**bugünkü indeksten, ürün retriever'ıyla yeniden üretilebilmeli**, yoksa Görev 7'nin ölçtüğü
şeyin ne olduğu bilinmiyor.

⛔ **`recall_olc.py` bu iş için KULLANILAMAZ.** O betiğin kendi `rrf_birlestir`'i var ve
varsayılanı `rrf_k=60`; ürün `retriever.py` ise `RRF_K=10` kullanıyor (ADR-0068). Aynı isimli
iki farklı ölçüm birimi — Faz 0'da tam bu sınıftan beş kusur çıktı.

- [ ] **Adım 1: Failing test yaz**

```python
# tests/test_kapsam_kapisi.py
"""Kapsam kapısının aleti — ürün retriever'ıyla recall@k.

⚠️ Sahte retriever kullanılır: gerçek bge-m3 CPU'da 80 sorgu için dakikalar sürer ve
testin ölçtüğü şey RECALL ARİTMETİĞİdir, gömme kalitesi değil.
"""
import pytest

from kapsam_kapisi import recall_olc


class SahteRetriever:
    """`getir(soru, k)` çağrısını önceden yazılmış listelerle karşılar."""

    def __init__(self, cevaplar):
        self._cevaplar = cevaplar

    def getir(self, soru, k=10):
        return self._cevaplar[soru][:k]


def _kayit(kanun_no, madde_no):
    return {"kanun_no": kanun_no, "madde_no": madde_no,
            "kanun_adi": "TEST KANUNU", "text": "…"}


def test_altin_ilk_sirada_recall_1_de_sayilir():
    r = SahteRetriever({"s1": [_kayit("4857", "Madde 31"), _kayit("4857", "Madde 32")]})
    sonuc = recall_olc(r, [{"soru": "s1", "kanun_no": "4857", "madde_no": "Madde 31"}], k=10)
    assert sonuc["recall@1"] == 1.0
    assert sonuc["recall@10"] == 1.0
    assert sonuc["altin_siralari"] == [0]


def test_altin_hic_getirilmezse_sira_None_ve_recall_sifir():
    r = SahteRetriever({"s1": [_kayit("6098", "Madde 1")]})
    sonuc = recall_olc(r, [{"soru": "s1", "kanun_no": "4857", "madde_no": "Madde 31"}], k=10)
    assert sonuc["altin_siralari"] == [None]
    assert sonuc["recall@10"] == 0.0


def test_gecici_madde_normal_maddeden_AYRI_sayilir():
    """⚠️ Sessiz şişme kaynağı: 'Geçici Madde 1' ile 'Madde 1' aynı sayılırsa recall
    şişer ve hiçbir yerde hata çıkmaz (madde_anahtar.py'nin kendi uyarısı)."""
    r = SahteRetriever({"s1": [_kayit("4857", "Madde 1")]})
    sonuc = recall_olc(r, [{"soru": "s1", "kanun_no": "4857", "madde_no": "Geçici Madde 1"}], k=10)
    assert sonuc["altin_siralari"] == [None], "geçici madde normal maddeyle eşleşti — recall şişer"


def test_k_getirilenden_buyukse_patlamaz():
    r = SahteRetriever({"s1": [_kayit("4857", "Madde 31")]})
    sonuc = recall_olc(r, [{"soru": "s1", "kanun_no": "4857", "madde_no": "Madde 31"}], k=10)
    assert sonuc["n"] == 1


def test_recall_orani_paydayi_TUM_sorulardan_alir():
    """Cevaplanamayan soru paydadan DÜŞMEZ — recall bir kapsama ölçüsüdür."""
    r = SahteRetriever({"s1": [_kayit("4857", "Madde 31")], "s2": [_kayit("9999", "Madde 1")]})
    sorular = [{"soru": "s1", "kanun_no": "4857", "madde_no": "Madde 31"},
               {"soru": "s2", "kanun_no": "4857", "madde_no": "Madde 31"}]
    assert recall_olc(r, sorular, k=10)["recall@10"] == 0.5
```

- [ ] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör**

Run: `python -m pytest tests/test_kapsam_kapisi.py -v`
Beklenen: `FAIL` — `ModuleNotFoundError: No module named 'kapsam_kapisi'`

- [ ] **Adım 3: Asgari uygulama**

```python
#!/usr/bin/env python3
"""Kapsam kapısı — ürün retriever'ıyla recall@k. Hakem YOK, model YOK, $0.

⛔ `recall_olc.py` bu işi YAPAMAZ: onun kendi `rrf_birlestir`'i var ve varsayılanı
`rrf_k=60`. Ürün `retriever.py` `RRF_K=10` kullanıyor (ADR-0068). Aynı isimli iki
farklı ölçüm birimi — kapı, ÜRÜNÜN gördüğü sırayı ölçmeli.

⚠️ Bu betiğin tek işi ARİTMETİK. Gömme, füzyon, sıralama hep `Retriever`'ın içinde.

Kullanım:
  python scripts/erisim_korpus/kapsam_kapisi.py \
      --indeks data/index/mevzuat_bge_m3_s2 \
      --sorular data/eval/dev/core_hard.jsonl \
      --out outputs/eval/f12-kapsam-kapisi/CIPA_kat0.json
"""
import argparse
import json
import os
import sys

# ── scripts/ yol köprüsü (T5, 2026-09-07) ────────────────────────────────────
# Kardeş modüller alt klasörlere bölündükten SONRA da bulunsun diye scripts/ kökü, tüm
# alt klasörleri ve repo kökü sys.path'e girer. Uzantısız `import X` bu köprü olmadan
# taşımada SESSİZCE kırılır: ImportError çalışma zamanında, bazen GPU koşusunun ortasında.
# ⚠️ 26 dosyada BİREBİR aynı; değiştirirsen hepsinde değiştir (grep: "yol köprüsü").
import os, sys
_K = os.path.dirname(os.path.abspath(__file__))
_K = _K if os.path.basename(_K) == "scripts" else os.path.dirname(_K)
sys.path[:0] = [_K, *(os.path.join(_K, _d) for _d in sorted(os.listdir(_K))
                      if os.path.isdir(os.path.join(_K, _d)) and _d[0] not in "_."),
                os.path.dirname(_K)]
# ─────────────────────────────────────────────────────────────────────────────
from madde_anahtar import madde_anahtari  # noqa: E402

ESIK = 0.9500   # ⛔ ÖN-KAYITLI (spec §5). Sonucu gördükten sonra DEĞİŞTİRİLEMEZ (ADR-0050).
KLER = (1, 5, 10)


def recall_olc(retriever, sorular: list[dict], k: int = 10) -> dict:
    """Her soru için altın maddenin ilk-k içindeki sırası; None = getirilmedi."""
    siralar = []
    for s in sorular:
        altin = madde_anahtari(s["kanun_no"], s["madde_no"])
        getirilen = retriever.getir(s["soru"], k)
        siralar.append(next(
            (i for i, p in enumerate(getirilen)
             if madde_anahtari(p["kanun_no"], p["madde_no"]) == altin), None))
    n = len(sorular)
    sonuc = {"n": n, "k": k, "altin_siralari": siralar}
    for j in KLER:
        if j <= k:
            sonuc[f"recall@{j}"] = sum(1 for x in siralar if x is not None and x < j) / n
    return sonuc


def sorulari_yukle(yol: str) -> list[dict]:
    """DEV kalemini `{soru, kanun_no, madde_no}` üçlüsüne indirger."""
    cikti = []
    with open(yol, encoding="utf-8") as f:
        for satir in f:
            if not satir.strip():
                continue
            r = json.loads(satir)
            soru = next(m["content"] for m in r["messages"] if m["role"] == "user")
            cikti.append({"soru": soru, "kanun_no": r["kanun_no"], "madde_no": r["madde_no"]})
    return cikti


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--indeks", required=True)
    p.add_argument("--sorular", default="data/eval/dev/core_hard.jsonl")
    p.add_argument("--out", required=True)
    p.add_argument("-k", type=int, default=10)
    p.add_argument("--etiket", default="", help="hangi kat — künyeye yazılır")
    a = p.parse_args()

    from retriever import Retriever
    r = Retriever.yukle(a.indeks)
    sorular = sorulari_yukle(a.sorular)
    sonuc = recall_olc(r, sorular, a.k)
    sonuc["indeks"] = a.indeks
    sonuc["indeks_kunye"] = r._kunye
    sonuc["sorular"] = a.sorular
    sonuc["etiket"] = a.etiket
    sonuc["esik"] = ESIK
    sonuc["gecti"] = sonuc[f"recall@{a.k}"] >= ESIK

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(sonuc, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    for j in KLER:
        if f"recall@{j}" in sonuc:
            print(f"  recall@{j:<3} {sonuc[f'recall@{j}']:.4f}")
    damga = "✅ GEÇTİ" if sonuc["gecti"] else "⛔ KALDI"
    print(f"[kapsam] {damga} — recall@{a.k} {sonuc[f'recall@{a.k}']:.4f} ↔ eşik {ESIK:.4f}")
    return 0 if sonuc["gecti"] else 2


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Adım 4: Testleri koş, GEÇTİĞİNİ gör**

Run: `python -m pytest tests/test_kapsam_kapisi.py -v`
Beklenen: `5 passed`

- [ ] **Adım 5: 🚨 ÇIPAYI KOŞ — bugünkü indeks 0,9500 üretiyor mu**

```bash
source ~/code/global_venv/bin/activate
python scripts/erisim_korpus/kapsam_kapisi.py \
    --indeks data/index/mevzuat_bge_m3_s2 \
    --sorular data/eval/dev/core_hard.jsonl \
    --etiket "kat0 — bugünkü korpus, 40.496 madde" \
    --out outputs/eval/f12-kapsam-kapisi/CIPA_kat0.json
```

Beklenen: `recall@10 0.9500` (76/80) · `EXIT=0`

⛔ **0,9500 çıkmazsa DUR ve Görev 7'ye GEÇME.** İki ihtimal var ve ayırt edilmeli:
(a) alet ürünün gördüğünden başka bir şey ölçüyor — **aleti düzelt**;
(b) yayımlanmış 0,9500 bu yoldan üretilmemiş — **o zaman kapının çıpası yok demektir ve
bu, tuzak 2.17'nin aynısıdır**. İkisi de insana sorulur; eşik **oynatılmaz**.

- [ ] **Adım 6: Çıpayı `outputs/` içine damgala ve commit et**

```bash
git add scripts/erisim_korpus/kapsam_kapisi.py tests/test_kapsam_kapisi.py \
        outputs/eval/f12-kapsam-kapisi/CIPA_kat0.json
git commit -m "Kapsam kapısının aleti + çıpası: bugünkü indeks recall@10 0,9500

Kapı eşiği spec'te ön-kayıtlı ama ÇIPASI yoktu — tuzak 2.17'nin tam sınıfı.
Alet ürünün retriever'ını (RRF_K=10, ADR-0068) kullanıyor; recall_olc.py
KULLANILMADI çünkü onun kendi füzyonu rrf_k=60 varsayıyor.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DgANwHgkTBaaNYpWvczNB5"
```

---

### Görev 2: `kaynak.py` — bedesten sözleşmesi tek yerde

**Dosyalar:**
- Create: `hakhukuk/__init__.py` · `hakhukuk/mevzuat/__init__.py` · `hakhukuk/mevzuat/tipler.py` · `hakhukuk/mevzuat/kaynak.py`
- Create: `tests/test_mevzuat_kaynak.py`

**Arayüzler:**
- Tüketir: yok (stdlib `urllib`)
- Üretir:
  - `Kayit(mevzuat_id: str, tur: str, ad: str, kayit_tarihi: str)` — donmuş
  - `TrIpGerekli(Exception)` · `BedestenHatasi(Exception)`
  - `Kaynak.listele(tur: str) -> list[Kayit]`
  - `Kaynak.maddeler(mevzuat_id: str) -> list[dict]` — `{madde_id, madde_no, baslik}`
  - `Kaynak.madde_metni(madde_id: str) -> str`
  - Görev 4 (`tazelik`) ve Görev 7 (kat girişi) bunları çağırır

**Neden `requests` değil `urllib`:** `bedesten_probe.py` sözleşmeyi stdlib ile **4/4 doğruladı**;
yeni bağımlılık gerekçe ister (`CLAUDE.md` §2) ve burada gerekçe yok.

- [ ] **Adım 1: Failing test yaz**

```python
# tests/test_mevzuat_kaynak.py
"""bedesten sözleşmesi — AĞA DOKUNMADAN sınanır.

⚠️ Ağa dokunan test TR IP olmayan makinede kırmızı yanar ve CI'yı yalan söyler.
Gerçek API'ye karşı doğrulama ayrı bir betiktir (bedesten_probe.py).
"""
import base64
import json

import pytest

from hakhukuk.mevzuat.kaynak import Kaynak
from hakhukuk.mevzuat.tipler import BedestenHatasi, Kayit, TrIpGerekli


def _sarmala(ic):
    return {"data": ic, "metadata": {"FMTY": "SUCCESS"}}


def _sayfa(adet, baslangic=0):
    return _sarmala({"total": 25, "mevzuatList": [
        {"mevzuatId": f"id{baslangic + i}", "mevzuatAdi": f"KANUN {baslangic + i}",
         "mevzuatTur": "KANUN", "kayitTarihi": "2026-05-22T10:00:00"}
        for i in range(adet)]})


def test_sayfalama_20_lik_sinirla_hepsini_toplar():
    """⚠️ pageSize max 20 — 50 ve 100 BOŞ döner (ölçüldü). 25 kayıt = 2 istek."""
    cagrilar = []

    def sahte_post(yol, ic, paging=False):
        cagrilar.append(ic)
        return _sayfa(20, 0) if ic["pageNumber"] == 1 else _sayfa(5, 20)

    k = Kaynak(post=sahte_post)
    kayitlar = k.listele("KANUN")
    assert len(kayitlar) == 25
    assert all(c["pageSize"] == 20 for c in cagrilar), "pageSize 20'yi aşmamalı"
    assert [c["pageNumber"] for c in cagrilar] == [1, 2]


def test_kayit_donmus_ve_kayit_tarihi_tasiniyor():
    k = Kaynak(post=lambda *a, **kw: _sayfa(1))
    kayit = k.listele("KANUN")[0]
    assert isinstance(kayit, Kayit)
    assert kayit.kayit_tarihi == "2026-05-22T10:00:00"
    with pytest.raises(Exception):
        kayit.ad = "başka"


def test_TR_IP_YOKSA_TrIpGerekli_ATILIR_fallback_YOK():
    """⛔ Sert kural (spec §4): sessiz düşürme bu repoda hata sınıfının kendisidir."""
    import urllib.error

    def sahte_post(*a, **kw):
        raise urllib.error.HTTPError("u", 403, "Forbidden", {}, None)

    with pytest.raises(TrIpGerekli):
        Kaynak(post=sahte_post).listele("KANUN")


def test_gecici_ag_hatasi_geri_cekilmeli_RETRY_edilir():
    denemeler = []

    def sahte_post(*a, **kw):
        denemeler.append(1)
        if len(denemeler) < 3:
            raise TimeoutError("geçici")
        return _sayfa(1)

    k = Kaynak(post=sahte_post, bekle=lambda s: None)
    assert len(k.listele("KANUN")) == 1
    assert len(denemeler) == 3


def test_retry_tukenince_YUTULMAZ_BedestenHatasi_atilir():
    def sahte_post(*a, **kw):
        raise TimeoutError("hep düşük")

    with pytest.raises(BedestenHatasi):
        Kaynak(post=sahte_post, bekle=lambda s: None).listele("KANUN")


def test_madde_metni_base64_html_cozulur_ve_etiketler_temizlenir():
    ham = "<p>Madde 31 &ndash; İşçi&nbsp;askere gider.</p><br/>İkinci satır."
    govde = _sarmala({"mimeType": "text/html",
                      "content": base64.b64encode(ham.encode()).decode()})
    metin = Kaynak(post=lambda *a, **kw: govde).madde_metni("m1")
    assert "<p>" not in metin
    assert "Madde 31" in metin
    assert "İkinci satır." in metin


def test_madde_agaci_ic_ice_children_duzlestirilir():
    """⚠️ maddeler ağacın YAPRAKLARINDA değil, herhangi bir düzeyinde olabilir."""
    agac = _sarmala({"children": [
        {"maddeNo": None, "title": "BİRİNCİ KISIM", "children": [
            {"maddeId": "m1", "maddeNo": "Madde 1", "title": "Amaç", "children": []},
            {"maddeId": "m2", "maddeNo": "Madde 2", "title": "Kapsam", "children": []}]},
        {"maddeId": "m3", "maddeNo": "Madde 3", "title": "Tanımlar", "children": []}]})
    maddeler = Kaynak(post=lambda *a, **kw: agac).maddeler("mv1")
    assert [m["madde_id"] for m in maddeler] == ["m1", "m2", "m3"]
    assert all(m["madde_no"] for m in maddeler), "maddeNo=None olan düğüm madde DEĞİL"
```

- [ ] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör**

Run: `python -m pytest tests/test_mevzuat_kaynak.py -v`
Beklenen: `FAIL` — `ModuleNotFoundError: No module named 'hakhukuk'`

- [ ] **Adım 3: Tipleri yaz**

```python
# hakhukuk/mevzuat/tipler.py
"""Mevzuat katmanının veri tipleri ve hataları. Hepsi DONMUŞ.

⚠️ `hakhukuk/tipler.py` ile karıştırma: o, vatandaşa dönen CEVABI tarif eder
(`Durum` · `Cevap` · `Atif`); bu, KORPUSUN KENDİSİNİ tarif eder.
"""
from dataclasses import dataclass, field
from enum import Enum


class Tazelik(Enum):
    """⛔ Bool bayrak yok (CLAUDE.md §4): "sor" hâli bir bool ile ifade edilemez."""

    SOR = "sor"
    OTOMATIK = "otomatik"
    KAPALI = "kapali"


class Durum(Enum):
    GUNCEL = "guncel"
    TAZELENDI = "tazelendi"
    IP_YOK = "ip_yok"
    HATA = "hata"


class TrIpGerekli(Exception):
    """bedesten TR dışından erişimi engelledi. ⛔ YUTULMAZ — fallback yoktur."""


class BedestenHatasi(Exception):
    """Geri çekilmeli retry tükendi. Kalıcı altyapı hatası."""


@dataclass(frozen=True)
class Kayit:
    """Uzaktaki bir mevzuat belgesinin künyesi. `kayit_tarihi` fark taramasının sinyali."""

    mevzuat_id: str
    tur: str
    ad: str
    kayit_tarihi: str


@dataclass(frozen=True)
class Fark:
    """İki künye arasındaki fark. Boş olması "değişiklik yok" demektir."""

    yeni: tuple[Kayit, ...] = ()
    degisen: tuple[Kayit, ...] = ()
    kaybolan: tuple[str, ...] = ()

    def bos_mu(self) -> bool:
        return not (self.yeni or self.degisen or self.kaybolan)

    def toplam(self) -> int:
        return len(self.yeni) + len(self.degisen) + len(self.kaybolan)


@dataclass(frozen=True)
class Rapor:
    """`tazele()`'nin dönüşü. ⚠️ `korpus_tarihi` HER hâlde doludur — kullanıcı asla
    tarihsiz kalmaz (spec §2)."""

    durum: Durum
    korpus_tarihi: str
    fark: Fark = field(default_factory=Fark)
    mesaj: str = ""
```

- [ ] **Adım 4: `kaynak.py`'yi yaz**

```python
# hakhukuk/mevzuat/kaynak.py
"""bedesten.adalet.gov.tr/mevzuat sözleşmesi — TEK yerde.

Silme testi (POSD): bu modül silinirse bedesten'in tuhaflıkları DÖRT çağırana birden
yayılır — `pageSize` max 20 · `{"data": …, "applicationName": …}` sarmalaması ·
base64+HTML gövde · TR IP şartı · `guncellemeTarihi`'nin boş olması.

⚠️ Ölçüldü 2026-09-07: `guncellemeTarihi` alanı VAR ama 60/60 örnekte None. Bu modül
onu OKUMAZ; değişim sinyali `kayitTarihi`dir (100/100 dolu). Şemada alan görüp dolu
varsaymak bu reponun avladığı hata sınıfıdır.

Sözleşme: docs/BEDESTEN_API.md · prob: scripts/erisim_korpus/bedesten_probe.py
"""
from __future__ import annotations

import base64
import html as _html
import json
import re
import time
import urllib.error
import urllib.request

from .tipler import BedestenHatasi, Kayit, TrIpGerekli

BASE = "https://bedesten.adalet.gov.tr/mevzuat"
SAYFA = 20   # ⚠️ ölçüldü: 50 ve 100 BOŞ döner. Büyütmek sessizce sıfır kayıt getirir.
DENEME = 3
HEADERS = {
    "Content-Type": "application/json",
    "Origin": "https://mevzuat.adalet.gov.tr",
    "Referer": "https://mevzuat.adalet.gov.tr/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120 Safari/537.36",
    "Accept": "application/json",
}
_ETIKET = re.compile(r"<[^>]+>")
_BR = re.compile(r"<br\s*/?>", re.I)


def _post(yol: str, ic: dict, paging: bool = False) -> dict:
    govde = {"data": ic, "applicationName": "UyapMevzuat"}
    if paging:
        govde["paging"] = True
    istek = urllib.request.Request(
        BASE + yol, data=json.dumps(govde).encode("utf-8"), headers=HEADERS, method="POST")
    with urllib.request.urlopen(istek, timeout=30) as r:
        return json.load(r)


def _temizle(ham: str) -> str:
    return "\n".join(
        s.strip() for s in _html.unescape(_ETIKET.sub("", _BR.sub("\n", ham))).split("\n")
        if s.strip())


class Kaynak:
    """bedesten istemcisi. `post`/`bekle` testler için enjekte edilir."""

    def __init__(self, post=_post, bekle=time.sleep):
        self._post = post
        self._bekle = bekle

    def _cagir(self, yol: str, ic: dict, paging: bool = False) -> dict:
        """Geri çekilmeli retry. ⛔ 403 retry EDİLMEZ — TR IP kalıcı bir durumdur."""
        son = None
        for deneme in range(DENEME):
            try:
                return self._post(yol, ic, paging)
            except urllib.error.HTTPError as e:
                if e.code in (403, 451):
                    raise TrIpGerekli(
                        "bedesten TR dışı IP'yi engelledi (HTTP "
                        f"{e.code}) — tazeleme yapılamaz, fallback YOK") from e
                son = e
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                son = e
            if deneme < DENEME - 1:
                self._bekle(2 ** deneme)
        raise BedestenHatasi(f"{DENEME} denemede ulaşılamadı: {yol} — {son!r}")

    def listele(self, tur: str) -> list[Kayit]:
        """Bir türün TÜM belgelerini sayfalayarak topla."""
        cikti, sayfa = [], 1
        while True:
            govde = self._cagir("/searchDocuments", {
                "pageSize": SAYFA, "pageNumber": sayfa,
                "sortFields": ["RESMI_GAZETE_TARIHI"], "sortDirection": "desc",
                "mevzuatTurList": [tur],
            }, paging=True)
            liste = ((govde.get("data") or {}).get("mevzuatList")) or []
            cikti.extend(Kayit(mevzuat_id=d["mevzuatId"], tur=d.get("mevzuatTur") or tur,
                               ad=d.get("mevzuatAdi") or "",
                               kayit_tarihi=d.get("kayitTarihi") or "")
                         for d in liste)
            if len(liste) < SAYFA:
                return cikti
            sayfa += 1

    def maddeler(self, mevzuat_id: str) -> list[dict]:
        """Madde ağacını düzleştir. ⚠️ `maddeNo is None` olan düğüm BÖLÜM başlığıdır."""
        govde = self._cagir("/mevzuatMaddeTree", {"mevzuatId": mevzuat_id})
        cikti = []

        def in_(dugumler):
            for d in dugumler:
                if d.get("maddeNo") is not None:
                    cikti.append({"madde_id": d.get("maddeId"),
                                  "madde_no": d.get("maddeNo"),
                                  "baslik": d.get("title") or ""})
                in_(d.get("children") or [])

        in_(((govde.get("data") or {}).get("children")) or [])
        return cikti

    def madde_metni(self, madde_id: str) -> str:
        """Bir maddenin düz metni. Gövde base64; HTML ise etiketler temizlenir."""
        govde = self._cagir("/getDocumentContent",
                            {"documentType": "MADDE", "id": madde_id})
        veri = govde.get("data") or {}
        ham = base64.b64decode(veri.get("content", "")).decode("utf-8", "replace")
        return _temizle(ham) if "html" in (veri.get("mimeType") or "") else ham
```

`hakhukuk/__init__.py` ve `hakhukuk/mevzuat/__init__.py` bu adımda **boş** yaratılır;
`tazele()` Görev 8'de eklenecek.

- [ ] **Adım 5: Testleri koş, GEÇTİĞİNİ gör**

Run: `python -m pytest tests/test_mevzuat_kaynak.py -v`
Beklenen: `7 passed`

- [ ] **Adım 6: Tüm süiti koş — regresyon yok**

Run: `python -m pytest -q`
Beklenen: önceki taban + yeni testler, **0 failed**

- [ ] **Adım 7: Commit**

```bash
git add hakhukuk/ tests/test_mevzuat_kaynak.py
git commit -m "hakhukuk.mevzuat.kaynak: bedesten sözleşmesi tek modülde

pageSize 20 sınırı, {data:…} sarmalaması, base64+HTML gövde, madde ağacının
düzleştirilmesi ve TR IP tespiti burada gizli. 403/451 retry EDİLMEZ — TR IP
kalıcı bir durum; TrIpGerekli atılır ve yutulmaz (spec §4 sert kural).

guncellemeTarihi OKUNMUYOR: alan var ama 60/60 örnekte None (ölçüldü).

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DgANwHgkTBaaNYpWvczNB5"
```

---

### Görev 3: Korpusa KARARLI KİMLİK — artımlı gömmenin ön koşulu

**Dosyalar:**
- Create: `scripts/erisim_korpus/korpus_kimlik.py`
- Create: `tests/test_korpus_kimlik.py`
- Modify: `data/corpus/mevzuat_maddeler.jsonl` *(yalnız ALAN eklenir — metin değişmez)*
- Modify: `data/index/mevzuat_bge_m3_s2/KUNYE.json` *(korpus imzası yenilenir)*

**Arayüzler:**
- Tüketir: `hakhukuk.mevzuat.kaynak.Kaynak` (Görev 2) · `madde_anahtar.madde_anahtari`
- Üretir: korpus satırlarında `mevzuat_id: str | None` · `madde_id: str | None`
  — Görev 6 (artımlı gömme) ve Görev 7 (kat girişi) bunlara dayanır

**🚨 Sorun — ölçüldü, tahmin değil:**

| aday anahtar | benzersiz | çakışan |
| :--- | ---: | ---: |
| `(kanun_no, madde_no)` | 32.281 | 🚨 **3.699** |
| `(kanun_no, madde_no, text)` | 39.379 | 🚨 **538** |

Bugün kimlik **satır sırasıdır**: `gomme.npy`'nin *i*. satırı korpusun *i*. satırıdır, başka
hiçbir bağ yok. Artımlı güncelleme bu zeminde **yanlış satırı tazeler ve hata vermez.**

**Tasarım — üç kural, üçü de sessiz bozulmayı engellemek için:**

1. **Metin DEĞİŞMEZ.** Yalnız iki alan eklenir. Gömme `kanun_adi + madde_no + text`'ten
   üretiliyor ⇒ bu alanlar gömmeye girmez ⇒ `gomme.npy` **geçerli kalır** ve yeniden
   gömme gerekmez. Bu bir test ile çivilenir.
2. **Satır sırası DEĞİŞMEZ.** İndeks satır sırasına bağlı; sıra bozulursa 40.496 gömme
   sessizce yanlış maddeye bakar.
3. **Belirsiz eşleşme `None` bırakılır ve SAYILIR.** 3.699 çakışan anahtarda hangi bedesten
   maddesinin hangi satır olduğu bilinemez ⇒ uydurmak yerine **boş bırakılır**; o satırlar
   artımlı tazelemeye **girmez**, tam yeniden gömmeyle tazelenir. Sayı künyeye yazılır.

- [ ] **Adım 1: Failing test yaz**

```python
# tests/test_korpus_kimlik.py
"""Korpusa kimlik geri doldurma — metin ve satır sırası KORUNARAK.

⚠️ Bu dosyadaki her test bir SESSİZ bozulmayı hedefliyor. Kimlik yanlış eşlenirse
artımlı tazeleme yanlış maddeyi günceller ve hiçbir yerde hata çıkmaz.
"""
import json

import pytest

from korpus_kimlik import gomulen_metin_ozeti, kimlik_doldur


def _satir(kanun_no, madde_no, text="metin"):
    return {"kanun_no": kanun_no, "kanun_adi": "TEST KANUNU",
            "madde_no": madde_no, "text": text, "mulga": False}


def test_tek_esleme_kimlik_yazilir():
    korpus = [_satir("4857", "Madde 31")]
    uzak = {"4857": [{"madde_id": "m-31", "madde_no": "Madde 31"}]}
    yeni, rapor = kimlik_doldur(korpus, uzak, {"4857": "mv-4857"})
    assert yeni[0]["madde_id"] == "m-31"
    assert yeni[0]["mevzuat_id"] == "mv-4857"
    assert rapor["eslesen"] == 1


def test_CAKISAN_anahtar_None_birakilir_ve_SAYILIR():
    """⛔ 3.699 gerçek çakışma var. Uydurmak, yanlış satırı tazelemektir."""
    korpus = [_satir("7452", "MADDE 1", "birinci"), _satir("7452", "MADDE 1", "ikinci")]
    uzak = {"7452": [{"madde_id": "m-a", "madde_no": "MADDE 1"}]}
    yeni, rapor = kimlik_doldur(korpus, uzak, {"7452": "mv-7452"})
    assert [s["madde_id"] for s in yeni] == [None, None]
    assert rapor["belirsiz"] == 2


def test_uzakta_olmayan_madde_None_kalir_patlamaz():
    korpus = [_satir("1475", "Madde 14")]
    yeni, rapor = kimlik_doldur(korpus, {}, {})
    assert yeni[0]["madde_id"] is None
    assert rapor["eslesmeyen"] == 1


def test_SATIR_SIRASI_korunur():
    """⛔ İndeks satır sırasına bağlı — sıra bozulursa 40.496 gömme yanlış maddeye bakar."""
    korpus = [_satir("1", "Madde 1"), _satir("2", "Madde 2"), _satir("3", "Madde 3")]
    yeni, _ = kimlik_doldur(korpus, {}, {})
    assert [s["kanun_no"] for s in yeni] == ["1", "2", "3"]
    assert len(yeni) == len(korpus)


def test_GOMULEN_METIN_degismez():
    """⭐ Kritik: gömme `kanun_adi + madde_no + text`'ten üretildi. Bu üçü aynı kalırsa
    gomme.npy geçerli kalır ve 340k'lık yeniden gömme GEREKMEZ."""
    korpus = [_satir("4857", "Madde 31", "İşçi askere gider.")]
    once = gomulen_metin_ozeti(korpus)
    yeni, _ = kimlik_doldur(korpus, {"4857": [{"madde_id": "m-31", "madde_no": "Madde 31"}]},
                            {"4857": "mv-4857"})
    assert gomulen_metin_ozeti(yeni) == once


def test_gecici_madde_normal_maddeye_ESLESMEZ():
    korpus = [_satir("4857", "Geçici Madde 1")]
    uzak = {"4857": [{"madde_id": "m-1", "madde_no": "Madde 1"}]}
    yeni, rapor = kimlik_doldur(korpus, uzak, {"4857": "mv-4857"})
    assert yeni[0]["madde_id"] is None
    assert rapor["eslesmeyen"] == 1
```

- [ ] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör**

Run: `python -m pytest tests/test_korpus_kimlik.py -v`
Beklenen: `FAIL` — `ModuleNotFoundError: No module named 'korpus_kimlik'`

- [ ] **Adım 3: Asgari uygulama**

```python
#!/usr/bin/env python3
"""Korpusa bedesten kimliğini (mevzuat_id · madde_id) geri doldurur.

🚨 Neden gerekli — ölçüldü 2026-09-07: korpusta KARARLI KİMLİK YOK.
   (kanun_no, madde_no)        → 3.699 çakışma
   (kanun_no, madde_no, text)  → 538 çakışma
Bugünkü kimlik SATIR SIRASIdır. Artımlı gömme bu zeminde yanlış satırı tazeler
ve hata vermez — tam olarak bu reponun avladığı sınıf.

⛔ ÜÇ DEĞİŞMEZ:
  1. `kanun_adi`, `madde_no`, `text` DOKUNULMAZ  → gomme.npy geçerli kalır
  2. satır sırası DOKUNULMAZ                     → indeks satır sırasına bağlı
  3. belirsiz eşleşme None bırakılır ve SAYILIR  → uydurmak sessiz bozulmadır

Yazma atomik: geçici dosya → doğrulama → os.replace. Doğrulama düşerse korpus DEĞİŞMEZ.

Kullanım:
  python scripts/erisim_korpus/korpus_kimlik.py --korpus data/corpus/mevzuat_maddeler.jsonl
  python scripts/erisim_korpus/korpus_kimlik.py --korpus ... --kuru   # yazmaz, rapor verir
"""
import argparse
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict

# ── scripts/ yol köprüsü (T5, 2026-09-07) ────────────────────────────────────
# Kardeş modüller alt klasörlere bölündükten SONRA da bulunsun diye scripts/ kökü, tüm
# alt klasörleri ve repo kökü sys.path'e girer. Uzantısız `import X` bu köprü olmadan
# taşımada SESSİZCE kırılır: ImportError çalışma zamanında, bazen GPU koşusunun ortasında.
# ⚠️ 26 dosyada BİREBİR aynı; değiştirirsen hepsinde değiştir (grep: "yol köprüsü").
import os, sys
_K = os.path.dirname(os.path.abspath(__file__))
_K = _K if os.path.basename(_K) == "scripts" else os.path.dirname(_K)
sys.path[:0] = [_K, *(os.path.join(_K, _d) for _d in sorted(os.listdir(_K))
                      if os.path.isdir(os.path.join(_K, _d)) and _d[0] not in "_."),
                os.path.dirname(_K)]
# ─────────────────────────────────────────────────────────────────────────────
from madde_anahtar import madde_anahtari  # noqa: E402


def gomulen_metin_ozeti(kayitlar: list[dict]) -> str:
    """`retriever._gomulecek_metin` ile BİREBİR aynı üçlünün sha256'sı.

    Why: gömme bu üçlüden üretildi. Özet değişmediyse gomme.npy geçerlidir ve
    340k'lık yeniden gömme gerekmez — bu, saatlerce GPU demektir.
    """
    h = hashlib.sha256()
    for r in kayitlar:
        h.update(f"{r['kanun_adi']} {r['madde_no']} {r['text']}".encode("utf-8"))
        h.update(b"\x00")
    return h.hexdigest()


def kimlik_doldur(korpus: list[dict], uzak_maddeler: dict[str, list[dict]],
                  mevzuat_idler: dict[str, str]) -> tuple[list[dict], dict]:
    """Korpus satırlarına `mevzuat_id` + `madde_id` ekle. Sıra ve metin korunur.

    `uzak_maddeler`: kanun_no → bedesten madde listesi (`madde_id`, `madde_no`)
    `mevzuat_idler`: kanun_no → bedesten `mevzuatId`
    """
    yerel_sayim = Counter(madde_anahtari(r["kanun_no"], r["madde_no"]) for r in korpus)

    uzak_idx: dict[tuple, list[str]] = defaultdict(list)
    for kanun_no, maddeler in uzak_maddeler.items():
        for m in maddeler:
            uzak_idx[madde_anahtari(kanun_no, m["madde_no"])].append(m["madde_id"])

    rapor = Counter()
    cikti = []
    for r in korpus:
        anahtar = madde_anahtari(r["kanun_no"], r["madde_no"])
        adaylar = uzak_idx.get(anahtar, [])
        # ⛔ Belirsizlik İKİ yönlü: yerelde ya da uzakta birden fazlaysa eşleme yapılmaz.
        if yerel_sayim[anahtar] > 1 or len(adaylar) > 1:
            madde_id = None
            rapor["belirsiz"] += 1
        elif len(adaylar) == 1:
            madde_id = adaylar[0]
            rapor["eslesen"] += 1
        else:
            madde_id = None
            rapor["eslesmeyen"] += 1
        cikti.append({**r, "mevzuat_id": mevzuat_idler.get(r["kanun_no"]),
                      "madde_id": madde_id})
    return cikti, dict(rapor)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--korpus", default="data/corpus/mevzuat_maddeler.jsonl")
    p.add_argument("--kuru", action="store_true", help="yazmaz, yalnız rapor")
    a = p.parse_args()

    from hakhukuk.mevzuat.kaynak import Kaynak

    korpus = [json.loads(s) for s in open(a.korpus, encoding="utf-8") if s.strip()]
    once = gomulen_metin_ozeti(korpus)

    kaynak = Kaynak()
    uzak_maddeler, mevzuat_idler = {}, {}
    kanunlar = {r["kanun_no"] for r in korpus}
    # Why tek tek arama: `listele("KANUN")` mevzuatId veriyor ama bizim korpusun anahtarı
    # `kanun_no` ve bedesten o eşlemeyi liste sonucunda vermiyor. `mevzuatNo` ile arama
    # destekleniyor (bedesten_probe.py:46) ⇒ 892 istek + 892 madde ağacı ≈ 1.784 çağrı,
    # tek seferlik. ⚠️ Uzun sürer; `setsid nohup` ile koş.
    for kanun_no in sorted(kanunlar):
        govde = kaynak._cagir("/searchDocuments", {
            "pageSize": 20, "pageNumber": 1, "mevzuatNo": str(kanun_no),
            "mevzuatTurList": ["KANUN"],
            "sortFields": ["RESMI_GAZETE_TARIHI"], "sortDirection": "desc"}, paging=True)
        liste = ((govde.get("data") or {}).get("mevzuatList")) or []
        if len(liste) != 1:
            continue          # 0 → bulunamadı · >1 → belirsiz; ikisi de None bırakılır
        mevzuat_idler[kanun_no] = liste[0]["mevzuatId"]
        uzak_maddeler[kanun_no] = kaynak.maddeler(liste[0]["mevzuatId"])

    yeni, rapor = kimlik_doldur(korpus, uzak_maddeler, mevzuat_idler)

    sonra = gomulen_metin_ozeti(yeni)
    if sonra != once:
        raise SystemExit(f"🚫 GÖMÜLEN METİN DEĞİŞTİ ({once[:12]} → {sonra[:12]}) — "
                         "indeks geçersizleşirdi, YAZILMADI")
    if len(yeni) != len(korpus):
        raise SystemExit(f"🚫 satır sayısı değişti {len(korpus)} → {len(yeni)} — YAZILMADI")

    print(f"[kimlik] eşleşen {rapor.get('eslesen', 0):,} · "
          f"belirsiz {rapor.get('belirsiz', 0):,} · "
          f"eşleşmeyen {rapor.get('eslesmeyen', 0):,} / {len(korpus):,}")
    if a.kuru:
        print("[kimlik] --kuru: yazılmadı")
        return 0

    gecici = a.korpus + ".tmp"
    with open(gecici, "w", encoding="utf-8") as f:
        for r in yeni:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(gecici, a.korpus)
    print(f"[kimlik] yazıldı → {a.korpus}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Adım 4: Testleri koş, GEÇTİĞİNİ gör**

Run: `python -m pytest tests/test_korpus_kimlik.py -v`
Beklenen: `6 passed`

- [ ] **Adım 5: ⚠️ TR IP ile KURU koş — hiçbir şey yazmadan sayıyı gör**

```bash
source ~/code/global_venv/bin/activate
python scripts/erisim_korpus/korpus_kimlik.py --kuru
```

Beklenen biçim: `[kimlik] eşleşen N · belirsiz M · eşleşmeyen P / 40.496`

⚠️ **`belirsiz` sayısı ~3.699 civarında beklenir** (ölçülen çakışma). Çok daha büyük çıkarsa
`madde_no` biçimleri uzakta farklıdır — **normalleştirmeyi düzelt, sayıyı kabul etme**.
⛔ TR IP yoksa `TrIpGerekli` alırsın; bu **beklenen** davranıştır, bu adım o zaman **bekler**.

- [ ] **Adım 6: Gerçek koş + indeks künyesini yenile**

```bash
python scripts/erisim_korpus/korpus_kimlik.py
# Korpus baytı değişti ⇒ retriever bayat indeks diye REDDEDER (bu doğru davranış).
# İmza yenilenir; gömme YENİDEN KURULMAZ çünkü gömülen metin özeti aynı kaldı.
python - <<'PY'
import json, os
y = "data/index/mevzuat_bge_m3_s2/KUNYE.json"
k = json.load(open(y, encoding="utf-8"))
st = os.stat(k["korpus"]["yol"])
k["korpus"].update(bayt=st.st_size, mtime=int(st.st_mtime))
k["korpus"]["kimlik_notu"] = (
    "2026-09-08: korpusa mevzuat_id + madde_id eklendi (korpus_kimlik.py). "
    "GÖMÜLEN METİN (kanun_adi + madde_no + text) DEĞİŞMEDİ — sha256 ile doğrulandı, "
    "betik değişseydi yazmayı reddederdi. gomme.npy YENİDEN KURULMADI, gerekmiyordu.")
json.dump(k, open(y, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("künye yenilendi")
PY
```

- [ ] **Adım 7: 🚨 ÇIPAYI YENİDEN KOŞ — recall DEĞİŞMEMELİ**

```bash
python scripts/erisim_korpus/kapsam_kapisi.py \
    --indeks data/index/mevzuat_bge_m3_s2 \
    --etiket "kat0 — kimlik eklendikten SONRA" \
    --out outputs/eval/f12-kapsam-kapisi/CIPA_kat0_kimlikli.json
```

Beklenen: **`recall@10 0.9500` — Adım 5'teki çıpayla BİREBİR aynı.**
⛔ Farklıysa metin ya da sıra değişmiştir; `git checkout` ile korpusu geri al ve **DUR**.

- [ ] **Adım 8: Commit**

```bash
git add scripts/erisim_korpus/korpus_kimlik.py tests/test_korpus_kimlik.py \
        data/corpus/mevzuat_maddeler.jsonl data/index/mevzuat_bge_m3_s2/KUNYE.json \
        outputs/eval/f12-kapsam-kapisi/CIPA_kat0_kimlikli.json
git commit -m "Korpusa kararlı kimlik: mevzuat_id + madde_id

Artımlı gömmenin ön koşulu. Ölçüldü: (kanun_no, madde_no) 3.699 yerde çakışıyor,
metinle birlikte bile 538. Bugünkü kimlik SATIR SIRASI ⇒ artımlı tazeleme yanlış
satırı günceller ve HATA VERMEZ.

Belirsiz eşleşme None bırakıldı ve sayıldı — uydurmak sessiz bozulmadır.
Gömülen metin (kanun_adi + madde_no + text) sha256 ile çivilendi: DEĞİŞMEDİ
⇒ gomme.npy geçerli, yeniden gömme yok. recall@10 0,9500 aynen doğrulandı.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DgANwHgkTBaaNYpWvczNB5"
```

---

### Görev 4: `tazelik.py` — fark taraması, ağa DOKUNMADAN

**Dosyalar:**
- Create: `hakhukuk/mevzuat/tazelik.py`
- Create: `tests/test_mevzuat_tazelik.py`

**Arayüzler:**
- Tüketir: `tipler.Kayit` · `tipler.Fark` (Görev 2)
- Üretir: `fark_bul(yerel: dict[str, str], uzak: list[Kayit]) -> Fark`
  — Görev 5 (`anlik`) ve Görev 8 (`tazele`) bunu çağırır

**Neden saf fonksiyon:** Fark taraması bu tasarımın **tek karar verici** parçası; ağ ondan
ayrılınca üç senaryonun da (yeni · değişen · kaybolan) testi **milisaniyeler** sürer ve
TR IP olmayan makinede de koşar.

`yerel`: korpus künyesindeki `mevzuat_id → kayit_tarihi` eşlemesi.

- [ ] **Adım 1: Failing test yaz**

```python
# tests/test_mevzuat_tazelik.py
"""Fark taraması — saf, ağsız.

⚠️ `kayitTarihi`'nin bir DEĞİŞİM sinyali olduğu henüz KANITLANMADI (spec §8).
Bu dosya sinyalin ARİTMETİĞİNİ sınar; sinyalin kendisi Görev 5 Adım 5'te ölçülür.
"""
from hakhukuk.mevzuat.tazelik import fark_bul
from hakhukuk.mevzuat.tipler import Kayit


def _k(mid, tarih="2026-05-22T10:00:00"):
    return Kayit(mevzuat_id=mid, tur="KANUN", ad=f"KANUN {mid}", kayit_tarihi=tarih)


def test_degisiklik_yoksa_fark_BOSTUR():
    yerel = {"a": "2026-05-22T10:00:00"}
    fark = fark_bul(yerel, [_k("a")])
    assert fark.bos_mu()
    assert fark.toplam() == 0


def test_uzakta_olup_yerelde_olmayan_YENIDIR():
    fark = fark_bul({}, [_k("a")])
    assert [x.mevzuat_id for x in fark.yeni] == ["a"]
    assert fark.degisen == () and fark.kaybolan == ()


def test_kayit_tarihi_farkliysa_DEGISENDIR():
    fark = fark_bul({"a": "2026-05-22T10:00:00"}, [_k("a", "2026-09-03T08:00:00")])
    assert [x.mevzuat_id for x in fark.degisen] == ["a"]
    assert fark.yeni == ()


def test_yerelde_olup_uzakta_olmayan_KAYBOLANDIR():
    """⚠️ Kaybolan SİLİNMEZ — yalnız raporlanır. Bir belgenin aramadan düşmesi
    yürürlükten kalkması demek DEĞİLDİR; API tarafı bir değişiklik de olabilir."""
    fark = fark_bul({"a": "2026-05-22T10:00:00"}, [])
    assert fark.kaybolan == ("a",)


def test_uc_senaryo_ayni_anda_ayrisir():
    yerel = {"a": "t1", "b": "t1", "c": "t1"}
    uzak = [_k("a", "t1"), _k("b", "t2"), _k("d", "t1")]
    fark = fark_bul(yerel, uzak)
    assert [x.mevzuat_id for x in fark.yeni] == ["d"]
    assert [x.mevzuat_id for x in fark.degisen] == ["b"]
    assert fark.kaybolan == ("c",)
    assert fark.toplam() == 3


def test_uzak_kayit_tarihi_BOSSA_degisen_SAYILMAZ():
    """⛔ Boş `kayitTarihi` "değişti" demek değildir — her taramada tüm korpusu
    yeniden indirmeye yol açar. Sinyal yoksa DOKUNULMAZ."""
    fark = fark_bul({"a": "2026-05-22T10:00:00"}, [_k("a", "")])
    assert fark.bos_mu()


def test_fark_SIRALI_ve_yeniden_uretilebilir():
    """Aynı girdi aynı çıktıyı vermeli — rapor metni ve testler buna dayanıyor."""
    yerel = {"b": "t1", "a": "t1"}
    uzak = [_k("z"), _k("y")]
    assert [x.mevzuat_id for x in fark_bul(yerel, uzak).yeni] == ["y", "z"]
    assert fark_bul(yerel, []).kaybolan == ("a", "b")
```

- [ ] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör**

Run: `python -m pytest tests/test_mevzuat_tazelik.py -v`
Beklenen: `FAIL` — `ImportError: cannot import name 'fark_bul'`

- [ ] **Adım 3: Asgari uygulama**

```python
# hakhukuk/mevzuat/tazelik.py
"""Fark taraması — yerel künye ↔ uzak `kayitTarihi`.

⛔ Bu modül AĞA DOKUNMAZ. Ağ `kaynak.py`'de, karar burada; ayrılık üç senaryonun da
milisaniyelerde ve TR IP olmadan sınanabilmesi için.

⚠️ `kayitTarihi`'nin gerçekten bir DEĞİŞİM sinyali olduğu KANITLANMADI (spec §8):
100/100 dolu ve benzersiz, ama kümeleniyor — toplu yeniden alım da olabilir.
Görev 5 Adım 5 bunu ölçüyor; çıkmazsa TASARIM DEĞİŞİR (içerik sha256'sına geçilir).
"""
from .tipler import Fark, Kayit


def fark_bul(yerel: dict[str, str], uzak: list[Kayit]) -> Fark:
    """`yerel`: mevzuat_id → kayit_tarihi. Çıktı sıralı ve yeniden üretilebilir."""
    uzak_idx = {k.mevzuat_id: k for k in uzak}

    yeni = [k for mid, k in uzak_idx.items() if mid not in yerel]
    # ⛔ Boş kayit_tarihi "değişti" DEĞİLDİR: sinyal yoksa dokunulmaz, yoksa her
    # tarama tüm korpusu yeniden indirir.
    degisen = [k for mid, k in uzak_idx.items()
               if mid in yerel and k.kayit_tarihi and k.kayit_tarihi != yerel[mid]]
    kaybolan = sorted(mid for mid in yerel if mid not in uzak_idx)

    anahtar = lambda k: k.mevzuat_id   # noqa: E731
    return Fark(yeni=tuple(sorted(yeni, key=anahtar)),
                degisen=tuple(sorted(degisen, key=anahtar)),
                kaybolan=tuple(kaybolan))
```

- [ ] **Adım 4: Testleri koş, GEÇTİĞİNİ gör**

Run: `python -m pytest tests/test_mevzuat_tazelik.py -v`
Beklenen: `7 passed`

- [ ] **Adım 5: Commit**

```bash
git add hakhukuk/mevzuat/tazelik.py tests/test_mevzuat_tazelik.py
git commit -m "hakhukuk.mevzuat.tazelik: fark taraması, saf ve ağsız

Üç senaryo (yeni · değişen · kaybolan) ağa dokunmadan sınanıyor. Boş kayitTarihi
'değişti' saymıyor — sinyal yoksa dokunulmaz, yoksa her tarama tüm korpusu
yeniden indirirdi. Kaybolan SİLİNMİYOR, yalnız raporlanıyor.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DgANwHgkTBaaNYpWvczNB5"
```

---

### Görev 5: `anlik.py` — anlık görüntü, atomik yazma, geri alma

**Dosyalar:**
- Create: `hakhukuk/mevzuat/anlik.py`
- Create: `tests/test_mevzuat_anlik.py`
- Create: `outputs/eval/f13-tazelik/KAYITTARIHI_SINYAL.json`

**Arayüzler:**
- Tüketir: `tipler.Kunye` · `tazelik.fark_bul` (Görev 4) · `kaynak.Kaynak` (Görev 2)
- Üretir:
  - `Anlik.yukle(korpus_yolu) -> Anlik` · `Anlik.kunye -> dict` · `Anlik.tarih -> str`
  - `Anlik.yaz(kayitlar, kunye)` — **atomik**
  - Görev 6 (`indeksle`) ve Görev 8 (`tazele`) bunları çağırır

**⛔ Sert kural (spec §4):** *"14 belgeden 9'u inip ağ koparsa korpus **bayt-bayt eski
hâlinde** kalır."* Aksi hâlde künyedeki tarih ile içerik ayrışır — ve o ayrışma **hata
vermez**, yalnız sessizce yanlış olur.

- [ ] **Adım 1: Failing test yaz**

```python
# tests/test_mevzuat_anlik.py
"""Anlık görüntü — atomik yazma, künye, geri alma.

⛔ En kritik test `test_yazma_ortasinda_hata_KORPUSU_DEGISTIRMEZ`. Kısmi yazma
künye tarihi ile içeriği ayrıştırır ve o ayrışma HATA VERMEZ.
"""
import hashlib
import json

import pytest

from hakhukuk.mevzuat.anlik import Anlik


def _kayitlar(n=3):
    return [{"kanun_no": str(i), "kanun_adi": f"K{i}", "madde_no": "Madde 1",
             "text": f"metin {i}", "mulga": False,
             "mevzuat_id": f"mv{i}", "madde_id": f"m{i}"} for i in range(n)]


def _kunye(tarih="2026-09-08T12:00:00"):
    return {"tarih": tarih, "kaynak": "bedesten", "turler": ["KANUN"],
            "belge_tarihleri": {"mv0": "t1", "mv1": "t1", "mv2": "t1"}}


def test_yazilan_okunur_ve_kunye_tarihi_gorunur(tmp_path):
    yol = tmp_path / "korpus.jsonl"
    Anlik.yaz(str(yol), _kayitlar(), _kunye())
    a = Anlik.yukle(str(yol))
    assert a.tarih == "2026-09-08T12:00:00"
    assert len(a.kayitlar) == 3


def test_kunye_AYRI_dosyada_korpusun_yanında(tmp_path):
    """Künye korpusun içine gömülemez: satır tabanlı okuma onu bir madde sanar."""
    yol = tmp_path / "korpus.jsonl"
    Anlik.yaz(str(yol), _kayitlar(), _kunye())
    assert (tmp_path / "korpus.KUNYE.json").exists()
    ilk = json.loads(yol.read_text(encoding="utf-8").splitlines()[0])
    assert "kanun_no" in ilk, "künye korpus satırlarına sızmış"


def test_sha256_kunyeye_yazilir_ve_dogrulanir(tmp_path):
    yol = tmp_path / "korpus.jsonl"
    Anlik.yaz(str(yol), _kayitlar(), _kunye())
    k = json.loads((tmp_path / "korpus.KUNYE.json").read_text(encoding="utf-8"))
    beklenen = hashlib.sha256(yol.read_bytes()).hexdigest()
    assert k["sha256"] == beklenen


def test_bozulmus_korpus_yuklemede_ERKEN_patlar(tmp_path):
    yol = tmp_path / "korpus.jsonl"
    Anlik.yaz(str(yol), _kayitlar(), _kunye())
    yol.write_text(yol.read_text(encoding="utf-8") + '{"kanun_no":"x"}\n', encoding="utf-8")
    with pytest.raises(SystemExit, match="sha256"):
        Anlik.yukle(str(yol))


def test_yazma_ortasinda_hata_KORPUSU_DEGISTIRMEZ(tmp_path, monkeypatch):
    """⛔ Hepsi ya da hiçbiri. Ağ 9/14'te koparsa korpus bayt-bayt eski kalmalı."""
    yol = tmp_path / "korpus.jsonl"
    Anlik.yaz(str(yol), _kayitlar(), _kunye("ESKI"))
    once_korpus = yol.read_bytes()
    once_kunye = (tmp_path / "korpus.KUNYE.json").read_bytes()

    import hakhukuk.mevzuat.anlik as m
    monkeypatch.setattr(m.os, "replace",
                        lambda *a: (_ for _ in ()).throw(OSError("disk doldu")))
    with pytest.raises(OSError):
        Anlik.yaz(str(yol), _kayitlar(5), _kunye("YENI"))

    assert yol.read_bytes() == once_korpus, "korpus kısmen yazılmış"
    assert (tmp_path / "korpus.KUNYE.json").read_bytes() == once_kunye
    assert not list(tmp_path.glob("*.tmp")), "geçici dosya temizlenmemiş"


def test_geri_al_bir_onceki_surume_doner(tmp_path):
    yol = tmp_path / "korpus.jsonl"
    Anlik.yaz(str(yol), _kayitlar(3), _kunye("SURUM1"))
    Anlik.yaz(str(yol), _kayitlar(5), _kunye("SURUM2"))
    assert Anlik.yukle(str(yol)).tarih == "SURUM2"
    Anlik.geri_al(str(yol))
    a = Anlik.yukle(str(yol))
    assert a.tarih == "SURUM1"
    assert len(a.kayitlar) == 3


def test_geri_alinacak_surum_yoksa_ACIK_hata(tmp_path):
    yol = tmp_path / "korpus.jsonl"
    Anlik.yaz(str(yol), _kayitlar(), _kunye())
    with pytest.raises(SystemExit, match="önceki sürüm"):
        Anlik.geri_al(str(yol))


def test_belge_tarihleri_fark_bulun_girdisi_olarak_cikar(tmp_path):
    """`Anlik.belge_tarihleri()` doğrudan `fark_bul(yerel=…)`'e verilir."""
    yol = tmp_path / "korpus.jsonl"
    Anlik.yaz(str(yol), _kayitlar(), _kunye())
    assert Anlik.yukle(str(yol)).belge_tarihleri() == {"mv0": "t1", "mv1": "t1", "mv2": "t1"}
```

- [ ] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör**

Run: `python -m pytest tests/test_mevzuat_anlik.py -v`
Beklenen: `FAIL` — `ModuleNotFoundError: No module named 'hakhukuk.mevzuat.anlik'`

- [ ] **Adım 3: Asgari uygulama**

```python
# hakhukuk/mevzuat/anlik.py
"""Korpusun sürümlenmiş anlık görüntüsü — künye · sha256 · atomik yazma · geri alma.

⛔ HEPSİ YA DA HİÇBİRİ. 14 belgeden 9'u inip ağ koparsa korpus BAYT-BAYT eski hâlinde
kalır. Aksi hâlde künyedeki tarih ile içerik ayrışır ve o ayrışma HATA VERMEZ —
yalnız sessizce yanlış olur (spec §4).

Diskteki üçlü:
    korpus.jsonl            madde satırları
    korpus.KUNYE.json       tarih · türler · sha256 · belge_tarihleri
    korpus.jsonl.onceki     tek adımlık geri alma
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil


def _kunye_yolu(korpus_yolu: str) -> str:
    kok, _ = os.path.splitext(korpus_yolu)
    return kok + ".KUNYE.json"


def _sha256(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for parca in iter(lambda: f.read(1 << 20), b""):
            h.update(parca)
    return h.hexdigest()


class Anlik:
    """Bir korpus anlık görüntüsü. `yukle` sha256'yı DOĞRULAR — bayat/bozuk korpus
    sessizce kullanılmaz."""

    def __init__(self, kayitlar: list[dict], kunye: dict, yol: str):
        self.kayitlar = kayitlar
        self.kunye = kunye
        self.yol = yol

    @property
    def tarih(self) -> str:
        """⚠️ HER hâlde doludur — kullanıcı asla tarihsiz kalmaz (spec §2)."""
        return self.kunye["tarih"]

    def belge_tarihleri(self) -> dict[str, str]:
        """`fark_bul(yerel=…)`'in beklediği eşleme."""
        return dict(self.kunye.get("belge_tarihleri") or {})

    @staticmethod
    def yukle(korpus_yolu: str) -> "Anlik":
        ky = _kunye_yolu(korpus_yolu)
        if not os.path.exists(ky):
            raise SystemExit(f"🚫 künye yok: {ky} — korpusun tarihi bilinmiyor")
        kunye = json.load(open(ky, encoding="utf-8"))
        simdi = _sha256(korpus_yolu)
        if kunye.get("sha256") and simdi != kunye["sha256"]:
            raise SystemExit(
                f"🚫 korpus sha256 tutmuyor ({kunye['sha256'][:12]} → {simdi[:12]}) — "
                "içerik künyeden bağımsız değişmiş; geri al ya da yeniden tazele")
        kayitlar = [json.loads(s) for s in open(korpus_yolu, encoding="utf-8") if s.strip()]
        return Anlik(kayitlar, kunye, korpus_yolu)

    @staticmethod
    def yaz(korpus_yolu: str, kayitlar: list[dict], kunye: dict) -> None:
        """Atomik yazma. Herhangi bir adım düşerse disk DEĞİŞMEZ.

        Sıra önemli: önce geçiciye yaz → sha hesapla → eskiyi yedekle →
        os.replace (atomik) → künyeyi yaz. Son adım düşerse geri sarılır.
        """
        gecici = korpus_yolu + ".tmp"
        gecici_kunye = _kunye_yolu(korpus_yolu) + ".tmp"
        onceki = korpus_yolu + ".onceki"
        onceki_kunye = _kunye_yolu(korpus_yolu) + ".onceki"
        try:
            with open(gecici, "w", encoding="utf-8") as f:
                for r in kayitlar:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
            tam_kunye = {**kunye, "sha256": _sha256(gecici), "n": len(kayitlar)}
            with open(gecici_kunye, "w", encoding="utf-8") as f:
                json.dump(tam_kunye, f, ensure_ascii=False, indent=2)

            if os.path.exists(korpus_yolu):
                shutil.copy2(korpus_yolu, onceki)
                if os.path.exists(_kunye_yolu(korpus_yolu)):
                    shutil.copy2(_kunye_yolu(korpus_yolu), onceki_kunye)

            os.replace(gecici, korpus_yolu)
            os.replace(gecici_kunye, _kunye_yolu(korpus_yolu))
        finally:
            # Why finally: hata hangi adımda olursa olsun geçici dosya kalmamalı —
            # kalırsa bir sonraki koşu onu yarım bir "yeni sürüm" sanabilir.
            for y in (gecici, gecici_kunye):
                if os.path.exists(y):
                    os.remove(y)

    @staticmethod
    def geri_al(korpus_yolu: str) -> None:
        """Tek adımlık geri alma. İki sürüm saklanmaz — YAGNI."""
        onceki = korpus_yolu + ".onceki"
        if not os.path.exists(onceki):
            raise SystemExit(f"🚫 geri alınacak önceki sürüm yok: {onceki}")
        os.replace(onceki, korpus_yolu)
        ok = _kunye_yolu(korpus_yolu) + ".onceki"
        if os.path.exists(ok):
            os.replace(ok, _kunye_yolu(korpus_yolu))
```

- [ ] **Adım 4: Testleri koş, GEÇTİĞİNİ gör**

Run: `python -m pytest tests/test_mevzuat_anlik.py -v`
Beklenen: `8 passed`

- [ ] **Adım 5: 🚨 `kayitTarihi` GERÇEKTEN bir değişim sinyali mi — ÖLÇ**

Bu, spec'in **yıldızlı** testi (§6) ve **açık kalanı** (§8). Bugün kanıtlanmadı.

```bash
source ~/code/global_venv/bin/activate
python - <<'PY'
"""kayitTarihi bir DEĞİŞİM sinyali mi, yoksa TOPLU YENİDEN ALIM sinyali mi?

Yöntem: kayitTarihi'ne göre en yeni 30 KANUN'u al. Her biri için madde metinlerini
indir ve korpustaki metinle karşılaştır. kayitTarihi bir değişim sinyaliyse bu
belgelerin metinlerinde korpusa göre FARK olmalı.

⛔ Bu ölçüm bir ŞEY KANITLAMAZ tek başına — korpusun kendi tarihi bilinmiyor.
Ölçtüğü şey: "yeni kayitTarihi'li belgeler bizden farklı mı?" Hayırsa sinyal
gürültülüdür ve tasarım değişir (içerik sha256'sına geçilir).
"""
import json, collections
from hakhukuk.mevzuat.kaynak import Kaynak

korpus = collections.defaultdict(dict)
for s in open("data/corpus/mevzuat_maddeler.jsonl", encoding="utf-8"):
    r = json.loads(s)
    korpus[str(r["kanun_no"])][str(r["madde_no"]).strip()] = r["text"]

k = Kaynak()
kayitlar = sorted(k.listele("KANUN"), key=lambda x: x.kayit_tarihi, reverse=True)[:30]
ayni = farkli = yok = 0
for kayit in kayitlar:
    for m in k.maddeler(kayit.mevzuat_id):
        bizde = korpus.get(kayit.ad, {}).get(str(m["madde_no"]).strip())
        if bizde is None:
            yok += 1
            continue
        farkli += (k.madde_metni(m["madde_id"]).strip() != bizde.strip())
        ayni += (k.madde_metni(m["madde_id"]).strip() == bizde.strip())

sonuc = {"belge": len(kayitlar), "metni_ayni": ayni, "metni_farkli": farkli,
         "korpusta_yok": yok,
         "yorum": "farkli >> ayni ise kayitTarihi degisim sinyali; ayni >> farkli ise GURULTULU"}
import os; os.makedirs("outputs/eval/f13-tazelik", exist_ok=True)
json.dump(sonuc, open("outputs/eval/f13-tazelik/KAYITTARIHI_SINYAL.json", "w"),
          ensure_ascii=False, indent=2)
print(sonuc)
PY
```

⛔ **`metni_ayni` baskın çıkarsa DUR ve insana sor.** Sinyal gürültülü demektir; spec §8
bunun sonucunu yazmış: *"o zaman içerik sha256 karşılaştırması gerekir, yani her belgeyi
indirmek"* — bu **tasarım değişikliğidir**, tek başına yapılmaz.

- [ ] **Adım 6: Ölçümü künyeye ve plana damgala, commit et**

```bash
git add hakhukuk/mevzuat/anlik.py tests/test_mevzuat_anlik.py \
        outputs/eval/f13-tazelik/KAYITTARIHI_SINYAL.json
git commit -m "hakhukuk.mevzuat.anlik: atomik anlık görüntü + kayitTarihi sinyal ölçümü

Hepsi-ya-da-hiçbiri yazma testle yasaklandı: os.replace düşürülünce korpus
bayt-bayt eski kalıyor ve geçici dosya kalmıyor. sha256 künyede ve yüklemede
DOĞRULANIYOR — bayat korpus sessizce kullanılamaz.

kayitTarihi'nin değişim sinyali olduğu spec'te KANITLANMAMIŞTI; ölçüldü.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DgANwHgkTBaaNYpWvczNB5"
```

---

### Görev 6: `indeksle.py` — artımlı gömme + ÖLÇEK KAPISI

**Dosyalar:**
- Create: `hakhukuk/mevzuat/indeksle.py`
- Create: `tests/test_mevzuat_indeksle.py`
- Create: `outputs/eval/f14-olcek/OLCEK_KAPISI.json`

**Arayüzler:**
- Tüketir: `anlik.Anlik` (Görev 5) · `retriever.Retriever` · `numpy`
- Üretir: `artimli_gom(eski_kayitlar, eski_gomme, yeni_kayitlar, gomucu) -> np.ndarray`
  — Görev 7 her katta bunu çağırır

**Neden artımlı:** Tam gömme **GPU'da ~1,5 saat, CPU'da ~23 saat** (spec §7b). Haftalık
tazelemede 14 belge değiştiyse 340.303 maddeyi yeniden gömmek **saçmadır**.

**⛔ Ön koşul:** Görev 3. Kararlı `madde_id` olmadan artımlı gömme **yanlış satırı tazeler
ve hata vermez.** `madde_id is None` olan satırlar artımlıya **girmez** — yeniden gömülür.

- [ ] **Adım 1: Failing test yaz**

```python
# tests/test_mevzuat_indeksle.py
"""Artımlı gömme — yalnız değişen maddeler yeniden gömülür.

⚠️ Her test bir SESSİZ bozulmayı hedefliyor: yanlış satırın tazelenmesi, satır
sırasının kayması, kimliksiz satırın yanlışlıkla yeniden kullanılması.
"""
import numpy as np
import pytest

from hakhukuk.mevzuat.indeksle import artimli_gom


def _k(madde_id, text, kanun_no="4857"):
    return {"kanun_no": kanun_no, "kanun_adi": "İŞ KANUNU", "madde_no": "Madde 1",
            "text": text, "mulga": False, "mevzuat_id": "mv1", "madde_id": madde_id}


def _gomucu(cagrilar):
    """Metnin uzunluğunu 4 boyuta yayan sahte gömücü — deterministik ve okunur."""
    def kodla(metinler):
        cagrilar.extend(metinler)
        return np.array([[float(len(m)), 1.0, 0.0, 0.0] for m in metinler], dtype=np.float32)
    return kodla


def test_hicbir_sey_degismediyse_GOMUCU_CAGRILMAZ():
    eski = [_k("m1", "a"), _k("m2", "b")]
    eski_g = np.array([[1., 1., 0., 0.], [1., 1., 0., 0.]], dtype=np.float32)
    cagrilar = []
    yeni_g = artimli_gom(eski, eski_g, eski, _gomucu(cagrilar))
    assert cagrilar == [], "değişmeyen madde yeniden gömüldü"
    assert np.array_equal(yeni_g, eski_g)


def test_yalnizca_METNI_DEGISEN_madde_yeniden_gomulur():
    eski = [_k("m1", "a"), _k("m2", "b")]
    eski_g = np.array([[1., 1., 0., 0.], [1., 1., 0., 0.]], dtype=np.float32)
    yeni = [_k("m1", "a"), _k("m2", "bbbb")]
    cagrilar = []
    yeni_g = artimli_gom(eski, eski_g, yeni, _gomucu(cagrilar))
    assert len(cagrilar) == 1 and "bbbb" in cagrilar[0]
    assert np.array_equal(yeni_g[0], eski_g[0]), "değişmeyen satırın gömmesi bozuldu"
    assert yeni_g[1][0] != eski_g[1][0]


def test_YENI_madde_eklenince_satir_SIRASI_yeni_korpusu_izler():
    """⛔ gomme.npy'nin i. satırı korpusun i. satırıdır — sıra kayarsa hepsi kayar."""
    eski = [_k("m1", "a")]
    eski_g = np.array([[1., 1., 0., 0.]], dtype=np.float32)
    yeni = [_k("m0", "zz"), _k("m1", "a")]
    yeni_g = artimli_gom(eski, eski_g, yeni, _gomucu([]))
    assert yeni_g.shape[0] == 2
    assert np.array_equal(yeni_g[1], eski_g[0]), "m1'in gömmesi yeni sırasına taşınmadı"


def test_SILINEN_madde_gommeden_de_duser():
    eski = [_k("m1", "a"), _k("m2", "b")]
    eski_g = np.array([[1., 1., 0., 0.], [2., 1., 0., 0.]], dtype=np.float32)
    yeni_g = artimli_gom(eski, eski_g, [_k("m2", "b")], _gomucu([]))
    assert yeni_g.shape[0] == 1
    assert np.array_equal(yeni_g[0], eski_g[1])


def test_KIMLIKSIZ_satir_ASLA_yeniden_kullanilmaz():
    """⛔ madde_id=None olan 3.699+ satır var. Kimliksiz satırı eşleştirmek,
    yanlış maddenin gömmesini kullanmaktır — ve hata vermez."""
    eski = [_k(None, "a")]
    eski_g = np.array([[9., 9., 9., 9.]], dtype=np.float32)
    cagrilar = []
    yeni_g = artimli_gom(eski, eski_g, [_k(None, "a")], _gomucu(cagrilar))
    assert len(cagrilar) == 1, "kimliksiz satır yeniden kullanıldı"
    assert not np.array_equal(yeni_g[0], eski_g[0])


def test_gomme_dtype_fp32_KALIR():
    """⛔ fp16 ölçüldü ve REDDEDİLDİ: 44,4× yavaş ve 10/80 sorguda ilk-10 değişiyor."""
    yeni_g = artimli_gom([], np.zeros((0, 4), np.float32), [_k("m1", "a")], _gomucu([]))
    assert yeni_g.dtype == np.float32


def test_bos_eski_indeks_hepsini_gomer():
    cagrilar = []
    yeni_g = artimli_gom([], np.zeros((0, 4), np.float32),
                         [_k("m1", "a"), _k("m2", "b")], _gomucu(cagrilar))
    assert len(cagrilar) == 2 and yeni_g.shape == (2, 4)
```

- [ ] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör**

Run: `python -m pytest tests/test_mevzuat_indeksle.py -v`
Beklenen: `FAIL` — `ModuleNotFoundError: No module named 'hakhukuk.mevzuat.indeksle'`

- [ ] **Adım 3: Asgari uygulama**

```python
# hakhukuk/mevzuat/indeksle.py
"""Artımlı gömme — yalnız değişen maddeler yeniden gömülür.

Neden: tam gömme GPU'da ~1,5 saat, CPU'da ~23 saat (spec §7b). Haftalık tazelemede
14 belge değiştiyse 340.303 maddeyi yeniden gömmek saçmadır.

⛔ ÖN KOŞUL: kararlı `madde_id` (korpus_kimlik.py). Kimlik yoksa artımlı gömme YANLIŞ
SATIRI tazeler ve HATA VERMEZ. `madde_id is None` olan satır artımlıya GİRMEZ.

⛔ dtype `fp32` KALIR — fp16 ölçüldü ve reddedildi (44,4× yavaş, 10/80 sorguda ilk-10
değişiyor). Bu bir takas değil, ölçüm birimini değiştiren müdahale (spec §7b).
"""
from __future__ import annotations

import numpy as np


def _gomulecek_metin(r: dict) -> str:
    """⚠️ `retriever._gomulecek_metin` ile BİREBİR aynı olmalı. Ayrışırsa artımlı
    gömme ile tam gömme farklı vektörler üretir ve fark hiçbir yerde görünmez."""
    return f"{r['kanun_adi']} {r['madde_no']} {r['text']}"


def artimli_gom(eski_kayitlar: list[dict], eski_gomme: np.ndarray,
                yeni_kayitlar: list[dict], gomucu) -> np.ndarray:
    """Yeni korpusun gömme matrisi. Değişmeyen maddelerin satırları KOPYALANIR.

    Eşleşme anahtarı `(madde_id, gömülen metin)` — ikisi birden. Yalnız `madde_id`
    yetmez: metin değiştiyse gömme de değişmeli.
    """
    eski_idx = {}
    for i, r in enumerate(eski_kayitlar):
        mid = r.get("madde_id")
        if mid is None:
            continue          # ⛔ kimliksiz satır ASLA yeniden kullanılmaz
        eski_idx[(mid, _gomulecek_metin(r))] = i

    boyut = eski_gomme.shape[1] if eski_gomme.size else None
    yeniden = [i for i, r in enumerate(yeni_kayitlar)
               if r.get("madde_id") is None
               or (r["madde_id"], _gomulecek_metin(r)) not in eski_idx]

    taze = gomucu([_gomulecek_metin(yeni_kayitlar[i]) for i in yeniden]) if yeniden else None
    if taze is not None:
        taze = np.asarray(taze, dtype=np.float32)
        boyut = taze.shape[1]
    if boyut is None:
        raise ValueError("boyut belirlenemedi: eski indeks boş ve gömülecek madde yok")

    cikti = np.empty((len(yeni_kayitlar), boyut), dtype=np.float32)
    taze_sira = {i: j for j, i in enumerate(yeniden)}
    for i, r in enumerate(yeni_kayitlar):
        if i in taze_sira:
            cikti[i] = taze[taze_sira[i]]
        else:
            cikti[i] = eski_gomme[eski_idx[(r["madde_id"], _gomulecek_metin(r))]]
    return cikti
```

- [ ] **Adım 4: Testleri koş, GEÇTİĞİNİ gör**

Run: `python -m pytest tests/test_mevzuat_indeksle.py -v`
Beklenen: `7 passed`

- [ ] **Adım 5: 🚨 ÖLÇEK KAPISI — 340k'da erişim hâlâ kullanılabilir mi**

Spec'in *"~51 ms"*'i **yalnız yoğun kolu** sayıyordu; ölçülen toplam **~803 ms** ve baskın
yük **BM25**'te. Kat kat büyürken bu **ön-kayıtlı** bir kapıya bağlanır:

```
sorgu (gömücü hariç)   ≤ 2.000 ms   → kat GİRER
yükleme (BM25 kurulumu) ≤   90  sn  → kat GİRER
RAM (yoğun + BM25)      ≤ 4.000 MB  → kat GİRER
```

⛔ **Eşikler koşudan ÖNCE yazıldı** (ADR-0050). Gerekçe: 340k tahmini sırasıyla
~803 ms · ~37 sn · ~2,1 GB; eşikler bunun **~2,5×**'i — büyümenin tahminden sapmasına pay,
ama *"vektör db gerekmiyor"* iddiasını hâlâ savunabilecek bir tavan.

```bash
source ~/code/global_venv/bin/activate
python - <<'PY'
"""Ölçek kapısı: mevcut korpus çoğaltılarak 340k'da erişim maliyeti ölçülür.

⚠️ SENTETİK: sorgu vektörleri rastgele, metinler korpusun kendisinin tekrarı.
Ölçtüğü şey ARİTMETİK MALİYET, erişim KALİTESİ değil. Kalite kapısı ayrı
(recall@10, kapsam_kapisi.py).
"""
import json, time, gc, os, numpy as np, sys
sys.path.insert(0, "scripts/erisim_korpus")
from retriever import rrf_birlestir
from rank_bm25 import BM25Okapi
import tracemalloc

K = [json.loads(s) for s in open("data/corpus/mevzuat_maddeler.jsonl", encoding="utf-8") if s.strip()]
tok = [f"{r['kanun_adi']} {r['madde_no']} {r['text']}".lower().split() for r in K]
kat = 340303 // len(K) + 1
buyuk = (tok * kat)[:340303]
rng = np.random.default_rng(3407)

gc.collect(); tracemalloc.start()
t = time.perf_counter(); bm = BM25Okapi(buyuk); yukleme = time.perf_counter() - t
bm_ram, _ = tracemalloc.get_traced_memory(); tracemalloc.stop()

G = rng.standard_normal((len(buyuk), 1024), dtype=np.float32); G /= np.linalg.norm(G, axis=1, keepdims=True)
q = rng.standard_normal(1024).astype(np.float32); q /= np.linalg.norm(q)
sorgu = "işe iade davası ne zaman açılır".split()

def bir():
    return np.argsort(rrf_birlestir([bm.get_scores(sorgu), q @ G.T]))[::-1][:10]

bir()
t = time.perf_counter()
for _ in range(5): bir()
sorgu_ms = (time.perf_counter() - t) / 5 * 1000

sonuc = {"n": len(buyuk), "sorgu_ms": round(sorgu_ms, 1),
         "yukleme_sn": round(yukleme, 1),
         "ram_mb": round((bm_ram + G.nbytes) / 1e6, 1),
         "esikler": {"sorgu_ms": 2000, "yukleme_sn": 90, "ram_mb": 4000},
         "not": "SENTETIK — sorgu vektorleri rastgele, metinler korpus tekrari. "
                "Olculen sey ARITMETIK MALIYET, erisim KALITESI degil."}
sonuc["gecti"] = (sorgu_ms <= 2000 and yukleme <= 90 and sonuc["ram_mb"] <= 4000)
os.makedirs("outputs/eval/f14-olcek", exist_ok=True)
json.dump(sonuc, open("outputs/eval/f14-olcek/OLCEK_KAPISI.json", "w"), ensure_ascii=False, indent=2)
print(json.dumps(sonuc, ensure_ascii=False, indent=2))
PY
```

⛔ **Kapı kalırsa Görev 7'ye GEÇME.** Sonuç bir **tasarım kararını** yeniden açar: BM25'i
kalıcılaştırmak · `mmap_mode="r"` · boyut indirgeme (spec §7b'nin *"açık borç"*u, hiçbiri
ölçülmedi). Bunlar bu planın dışında ⇒ **insana sor**.

- [ ] **Adım 6: Commit**

```bash
git add hakhukuk/mevzuat/indeksle.py tests/test_mevzuat_indeksle.py \
        outputs/eval/f14-olcek/OLCEK_KAPISI.json
git commit -m "hakhukuk.mevzuat.indeksle: artımlı gömme + ölçek kapısı

Eşleşme anahtarı (madde_id, gömülen metin) — ikisi birden. Kimliksiz satır ASLA
yeniden kullanılmıyor (testle çivilendi): 3.699+ belirsiz satır var ve birini
yeniden kullanmak yanlış maddenin vektörünü kullanmaktır.

Ölçek kapısı ÖN-KAYITLI: sorgu ≤2000 ms · yükleme ≤90 sn · RAM ≤4000 MB.
Gerekçe 340k tahmininin ~2,5×'i. Spec'in '~51 ms'i yalnız yoğun kolu sayıyordu.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DgANwHgkTBaaNYpWvczNB5"
```

---

### Görev 7: Kapsam KAT KAT girer — her kat bir kapıdan ⚠️ **>$1, DUR ve SOR**

**Dosyalar:**
- Create: `scripts/erisim_korpus/kat_ekle.py`
- Create: `tests/test_kat_ekle.py`
- Create: `outputs/eval/f12-kapsam-kapisi/kat{1..5}.json`
- Modify: `data/corpus/mevzuat_maddeler.jsonl` · `data/index/mevzuat_bge_m3_s2/`

**Arayüzler:**
- Tüketir: `kaynak.Kaynak` · `anlik.Anlik` · `indeksle.artimli_gom` · `kapsam_kapisi.recall_olc`
- Üretir: kat başına bir korpus sürümü + bir kapı raporu

**⛔ DUR VE SOR — bu görev tek adımda >$1 harcar.** Kat 4-5 (`CB_KARAR` + `KKY`,
**202.660 madde**) gömmesi Modal GPU'da ~1,5 saattir. Koşmadan **insana sor**.

**Katlar (spec §5, insan kararıyla 5'e çıktı):**

| kat | tür | belge | ≈ madde |
| :--- | :--- | ---: | ---: |
| 1 | `KHK` + `CB_KARARNAME` | 119 | ~33.000 |
| 2 | `TUZUK` | 110 | ~4.000 |
| 3 | `YONETMELIK` | 172 | ~8.000 |
| 4 | `CB_KARAR` | 4.361 | ~76.317 |
| 5 | `KKY` | 4.043 | ~126.343 |

```
recall@10 ≥ 0,9500  →  kat GİRER          ⛔ eşik ön-kayıtlı, ADR-0050
recall@10 <  0,9500  →  kat GİRMEZ, geri alınır, sebebi bulunana kadar
```

**🚨 Kapının sınırı — baştan yazılıyor (spec §5):** Kapı yalnız ***"eskiyi bozmadı"*** der;
***"yeniyi buluyor"* DEMEZ.** 80 sorunun **hepsi kanun düzeyinde**; yönetmelik düzeyinde
cevaplanan sorumuz **yok**. Kat 3 geçse bile *"yönetmelik eklemek işe yaradı"* **kurulamaz.**

- [ ] **Adım 1: Failing test yaz**

```python
# tests/test_kat_ekle.py
"""Kat ekleme — birleştirme mantığı, ağa dokunmadan.

⚠️ Testin ölçtüğü şey BİRLEŞTİRMEdir: mükerrer eklenmemesi, sıranın korunması,
kapı kalınca geri alınması.
"""
import pytest

from kat_ekle import kati_birlestir


def _m(mid, kanun_no, text="t"):
    return {"kanun_no": kanun_no, "kanun_adi": f"K{kanun_no}", "madde_no": "Madde 1",
            "text": text, "mulga": False, "mevzuat_id": f"mv{kanun_no}", "madde_id": mid}


def test_yeni_kat_MEVCUDUN_SONUNA_eklenir():
    """⛔ Mevcut satırlar yerinde kalmalı — artımlı gömme onların vektörünü kopyalıyor."""
    mevcut = [_m("a", "1"), _m("b", "2")]
    yeni = kati_birlestir(mevcut, [_m("c", "3")])
    assert [r["madde_id"] for r in yeni] == ["a", "b", "c"]


def test_ayni_madde_id_MUKERRER_eklenmez():
    mevcut = [_m("a", "1")]
    yeni = kati_birlestir(mevcut, [_m("a", "1"), _m("b", "2")])
    assert [r["madde_id"] for r in yeni] == ["a", "b"]


def test_kimliksiz_yeni_madde_REDDEDILIR():
    """⛔ Yeni gelen her maddenin bedesten kimliği olmalı — kimliksiz satır
    artımlı tazelemeye giremez ve sessizce her turda yeniden gömülür."""
    with pytest.raises(ValueError, match="madde_id"):
        kati_birlestir([_m("a", "1")], [_m(None, "2")])


def test_bos_kat_hicbir_sey_degistirmez():
    mevcut = [_m("a", "1")]
    assert kati_birlestir(mevcut, []) == mevcut
```

- [ ] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör**

Run: `python -m pytest tests/test_kat_ekle.py -v`
Beklenen: `FAIL` — `ModuleNotFoundError: No module named 'kat_ekle'`

- [ ] **Adım 3: Asgari uygulama**

```python
#!/usr/bin/env python3
"""Kapsamı KAT KAT büyütür; her kat ön-kayıtlı kapıdan geçer.

⛔ Eşik: recall@10 ≥ 0,9500. Koşudan ÖNCE yazıldı (spec §5, ADR-0050).
⛔ Kapı yalnız "eskiyi bozmadı" der; "yeniyi buluyor" DEMEZ — 80 sorunun hepsi
   kanun düzeyinde, yönetmelik düzeyinde cevaplanan sorumuz YOK.
⚠️ Tek seferde tüm türleri eklemek REDDEDİLDİ: düşerse hangi katın düşürdüğü
   bilinmez (T5'in dersi — grup grup taşındığı için kırılma hemen görüldü).

Kullanım:
  python scripts/erisim_korpus/kat_ekle.py --kat 1 --turler KHK CB_KARARNAME \
      --korpus data/corpus/mevzuat_maddeler.jsonl --indeks data/index/mevzuat_bge_m3_s2
"""
import argparse
import json
import os
import sys

import numpy as np

# ── scripts/ yol köprüsü (T5, 2026-09-07) ────────────────────────────────────
# Kardeş modüller alt klasörlere bölündükten SONRA da bulunsun diye scripts/ kökü, tüm
# alt klasörleri ve repo kökü sys.path'e girer. Uzantısız `import X` bu köprü olmadan
# taşımada SESSİZCE kırılır: ImportError çalışma zamanında, bazen GPU koşusunun ortasında.
# ⚠️ 26 dosyada BİREBİR aynı; değiştirirsen hepsinde değiştir (grep: "yol köprüsü").
import os, sys
_K = os.path.dirname(os.path.abspath(__file__))
_K = _K if os.path.basename(_K) == "scripts" else os.path.dirname(_K)
sys.path[:0] = [_K, *(os.path.join(_K, _d) for _d in sorted(os.listdir(_K))
                      if os.path.isdir(os.path.join(_K, _d)) and _d[0] not in "_."),
                os.path.dirname(_K)]
# ─────────────────────────────────────────────────────────────────────────────
from kapsam_kapisi import ESIK, recall_olc, sorulari_yukle  # noqa: E402


def kati_birlestir(mevcut: list[dict], yeni: list[dict]) -> list[dict]:
    """Yeni katı mevcudun SONUNA ekle. Mevcut satırlar yerinde kalır."""
    for r in yeni:
        if not r.get("madde_id"):
            raise ValueError(f"yeni madde kimliksiz (madde_id): {r.get('kanun_adi')} "
                             f"{r.get('madde_no')} — kimliksiz satır artımlıya giremez")
    var = {r.get("madde_id") for r in mevcut if r.get("madde_id")}
    return mevcut + [r for r in yeni if r["madde_id"] not in var]


def turu_indir(kaynak, tur: str) -> list[dict]:
    """Bir türün tüm belgelerinin tüm maddelerini korpus satırına çevir."""
    cikti = []
    for kayit in kaynak.listele(tur):
        for m in kaynak.maddeler(kayit.mevzuat_id):
            if not m.get("madde_id"):
                continue
            cikti.append({
                "kanun_no": kayit.mevzuat_id, "kanun_adi": kayit.ad,
                "madde_no": m["madde_no"], "text": kaynak.madde_metni(m["madde_id"]),
                "mulga": False, "mevzuat_id": kayit.mevzuat_id, "madde_id": m["madde_id"],
                "tur": tur, "kayit_tarihi": kayit.kayit_tarihi})
    return cikti


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--kat", type=int, required=True)
    p.add_argument("--turler", nargs="+", required=True)
    p.add_argument("--korpus", default="data/corpus/mevzuat_maddeler.jsonl")
    p.add_argument("--indeks", default="data/index/mevzuat_bge_m3_s2")
    p.add_argument("--sorular", default="data/eval/dev/core_hard.jsonl")
    p.add_argument("--cihaz", default="cpu", choices=["cpu", "cuda"])
    a = p.parse_args()

    from hakhukuk.mevzuat.anlik import Anlik
    from hakhukuk.mevzuat.indeksle import artimli_gom
    from hakhukuk.mevzuat.kaynak import Kaynak
    from retriever import Retriever, bge_gomucu

    anlik = Anlik.yukle(a.korpus)
    kaynak = Kaynak()

    yeni_satirlar, belge_tarihleri = [], dict(anlik.belge_tarihleri())
    for tur in a.turler:
        satirlar = turu_indir(kaynak, tur)
        print(f"[kat{a.kat}] {tur}: {len(satirlar):,} madde", flush=True)
        yeni_satirlar.extend(satirlar)
        for r in satirlar:
            belge_tarihleri[r["mevzuat_id"]] = r.get("kayit_tarihi", "")

    birlesik = kati_birlestir(anlik.kayitlar, yeni_satirlar)
    print(f"[kat{a.kat}] korpus {len(anlik.kayitlar):,} → {len(birlesik):,}", flush=True)

    eski_gomme = np.load(os.path.join(a.indeks, "gomme.npy")).astype(np.float32)
    gomme = artimli_gom(anlik.kayitlar, eski_gomme, birlesik,
                        bge_gomucu(a.cihaz, "BAAI/bge-m3"))

    Anlik.yaz(a.korpus, birlesik,
              {**anlik.kunye, "tarih": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
               "turler": sorted(set(anlik.kunye.get("turler", [])) | set(a.turler)),
               "belge_tarihleri": belge_tarihleri, "kat": a.kat})
    np.save(os.path.join(a.indeks, "gomme.npy"), gomme.astype(np.float16))

    kunye_yolu = os.path.join(a.indeks, "KUNYE.json")
    kunye = json.load(open(kunye_yolu, encoding="utf-8"))
    st = os.stat(a.korpus)
    kunye["korpus"].update(bayt=st.st_size, mtime=int(st.st_mtime))
    kunye["n"] = len(birlesik)
    json.dump(kunye, open(kunye_yolu, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    sonuc = recall_olc(Retriever.yukle(a.indeks), sorulari_yukle(a.sorular), 10)
    sonuc.update(kat=a.kat, turler=a.turler, n_madde=len(birlesik), esik=ESIK,
                 gecti=sonuc["recall@10"] >= ESIK,
                 sinir="Kapi yalnız 'eskiyi bozmadi' der; 'yeniyi buluyor' DEMEZ — "
                       "80 sorunun hepsi kanun duzeyinde (spec §5)")
    out = f"outputs/eval/f12-kapsam-kapisi/kat{a.kat}.json"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(sonuc, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    if sonuc["gecti"]:
        print(f"[kat{a.kat}] ✅ GEÇTİ — recall@10 {sonuc['recall@10']:.4f} ≥ {ESIK}")
        return 0
    print(f"[kat{a.kat}] ⛔ KALDI — recall@10 {sonuc['recall@10']:.4f} < {ESIK}\n"
          f"   korpus GERİ ALINIYOR; indeksi yeniden kurmak GEREKİR:\n"
          f"   python scripts/erisim_korpus/retriever.py kur --korpus {a.korpus} "
          f"--indeks {a.indeks} --cihaz cuda")
    Anlik.geri_al(a.korpus)
    return 2


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Adım 4: Testleri koş, GEÇTİĞİNİ gör**

Run: `python -m pytest tests/test_kat_ekle.py -v`
Beklenen: `4 passed`

- [ ] **Adım 5: ⚠️ İNSANA SOR — kat 4-5 bütçesi**

Kat 1-3 (~45.000 madde) yerel GPU'da makul. **Kat 4-5 202.660 madde** ⇒ Modal GPU ~1,5 sa,
**>$1**. Sormadan koşma. Sorulacak somut şey: *"kat 4-5 şimdi mi, yoksa kat 1-3 kapıdan
geçtikten sonra ayrı bir oturumda mı?"*

- [ ] **Adım 6: Kat 1 — `KHK` + `CB_KARARNAME`**

```bash
source ~/code/global_venv/bin/activate
setsid nohup python scripts/erisim_korpus/kat_ekle.py --kat 1 \
    --turler KHK CB_KARARNAME --cihaz cuda \
    > outputs/eval/f12-kapsam-kapisi/kat1.log 2>&1 &
```

⚡ **GPU koşusundan ÖNCE künyede `güç : ŞARJDA` DOĞRULA** — pilde GPU 180 MHz'e kısılıyor.
Beklenen: `[kat1] ✅ GEÇTİ — recall@10 0.9xxx ≥ 0.95` · `EXIT=0`

- [ ] **Adım 7: Kat 2 — `TUZUK`** *(kat 1 geçmeden başlama)*

```bash
setsid nohup python scripts/erisim_korpus/kat_ekle.py --kat 2 --turler TUZUK --cihaz cuda \
    > outputs/eval/f12-kapsam-kapisi/kat2.log 2>&1 &
```

- [ ] **Adım 8: Kat 3 — `YONETMELIK`** *(kat 2 geçmeden başlama)*

```bash
setsid nohup python scripts/erisim_korpus/kat_ekle.py --kat 3 --turler YONETMELIK --cihaz cuda \
    > outputs/eval/f12-kapsam-kapisi/kat3.log 2>&1 &
```

- [ ] **Adım 9: Kat 4-5 — `CB_KARAR` · `KKY`** *(Adım 5'in izni ALINDIKTAN sonra)*

```bash
setsid nohup python scripts/erisim_korpus/kat_ekle.py --kat 4 --turler CB_KARAR --cihaz cuda \
    > outputs/eval/f12-kapsam-kapisi/kat4.log 2>&1 &
# kat 4 geçtikten SONRA:
setsid nohup python scripts/erisim_korpus/kat_ekle.py --kat 5 --turler KKY --cihaz cuda \
    > outputs/eval/f12-kapsam-kapisi/kat5.log 2>&1 &
```

- [ ] **Adım 10: Ölçek kapısını GERÇEK korpusta yeniden koş**

Görev 6 Adım 5 **sentetikti**. Kat 5 bittikten sonra gerçek korpusla tekrarlanır ve
`outputs/eval/f14-olcek/OLCEK_KAPISI_gercek.json`'a yazılır. Sentetik tahminden sapma
**raporlanır** — sapmanın kendisi bir bulgudur.

- [ ] **Adım 11: Commit** *(her kat AYRI commit — düşerse hangisi belli olsun)*

```bash
git add data/corpus/mevzuat_maddeler.jsonl data/corpus/mevzuat_maddeler.KUNYE.json \
        data/index/mevzuat_bge_m3_s2/ outputs/eval/f12-kapsam-kapisi/ \
        scripts/erisim_korpus/kat_ekle.py tests/test_kat_ekle.py
git commit -m "Kapsam kat N: <TÜRLER> girdi — recall@10 0,9xxx ≥ 0,9500

Korpus N → M madde. Kapı ön-kayıtlıydı, eşik oynatılmadı.
⚠️ Kapı yalnız 'eskiyi bozmadı' diyor; 'yeniyi buluyor' DEMİYOR — 80 sorunun
hepsi kanun düzeyinde, bu türde cevaplanan sorumuz yok (spec §5).

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DgANwHgkTBaaNYpWvczNB5"
```

⛔ **Bir kat kalırsa:** betik korpusu **geri alır** ama indeks kat'ın gömmesini taşır ⇒
`retriever.py kur` ile **yeniden kur**, sonra `kapsam_kapisi.py` ile çıpanın geri geldiğini
doğrula. Sonra **insana sor** — eşik oynatılmaz.

---

### Görev 8: `tazele()` — ana arayüz, `Tazelik` enum, CLI

**Dosyalar:**
- Modify: `hakhukuk/mevzuat/__init__.py` *(boştu — `tazele` · `Tazelik` · `Rapor` dışa açılır)*
- Create: `hakhukuk/mevzuat/_tazele.py`
- Create: `tests/test_mevzuat_tazele.py`
- Modify: `scripts/erisim_korpus/kat_ekle.py` — yok; CLI `python -m hakhukuk.mevzuat`

**Arayüzler:**
- Tüketir: `kaynak.Kaynak` · `tazelik.fark_bul` · `anlik.Anlik` · `indeksle.artimli_gom`
- Üretir: `tazele(mod: Tazelik = Tazelik.SOR, ...) -> Rapor` — ürünün (v2, CLI/TUI) çağıracağı **tek** giriş

```
tazele(mod: Tazelik = Tazelik.SOR) -> Rapor
```

`Tazelik`: **`SOR`** (varsayılan — *"14 belge değişmiş, güncelleyeyim mi"*) · `OTOMATIK` · `KAPALI`.
⛔ **Bool bayrak yok** (`CLAUDE.md` §4): *"sor"* hâli bir `bool` ile ifade edilemez.

**İki sert kural, ikisi de testle çivilenir:**
1. ⛔ TR IP yoksa **fallback YOK** — `Rapor.durum = IP_YOK`, korpus tarihi yine gösterilir.
2. ⛔ Kısmi tazeleme **diske yazılmaz** — hepsi ya da hiçbiri.

- [ ] **Adım 1: Failing test yaz**

```python
# tests/test_mevzuat_tazele.py
"""`tazele()` — ana arayüz. Ağa dokunmadan, sahte kaynakla.

⛔ Bu dosyanın iki testi SERT KURAL sınıyor: IP_YOK'ta fallback olmaması ve
kısmi indirmede diske yazılmaması.
"""
import json

import pytest

from hakhukuk.mevzuat import Rapor, Tazelik, tazele
from hakhukuk.mevzuat.anlik import Anlik
from hakhukuk.mevzuat.tipler import Durum, Kayit, TrIpGerekli


class SahteKaynak:
    def __init__(self, kayitlar=(), maddeler=None, metin_hatasi_at=None):
        self._kayitlar = list(kayitlar)
        self._maddeler = maddeler or {}
        self._hata = metin_hatasi_at
        self.indirilen = []

    def listele(self, tur):
        return [k for k in self._kayitlar if k.tur == tur]

    def maddeler(self, mevzuat_id):
        return self._maddeler.get(mevzuat_id, [])

    def madde_metni(self, madde_id):
        if self._hata and madde_id == self._hata:
            raise TimeoutError("ağ koptu")
        self.indirilen.append(madde_id)
        return f"metin-{madde_id}"


def _kur(tmp_path, tarih="2026-09-01T00:00:00"):
    yol = tmp_path / "korpus.jsonl"
    Anlik.yaz(str(yol), [{"kanun_no": "4857", "kanun_adi": "İŞ KANUNU",
                          "madde_no": "Madde 1", "text": "eski", "mulga": False,
                          "mevzuat_id": "mv1", "madde_id": "m1"}],
              {"tarih": tarih, "turler": ["KANUN"], "belge_tarihleri": {"mv1": "t1"}})
    return str(yol)


def test_degisiklik_yoksa_GUNCEL_doner_ve_disk_DEGISMEZ(tmp_path):
    yol = _kur(tmp_path)
    once = open(yol, "rb").read()
    r = tazele(Tazelik.OTOMATIK, korpus_yolu=yol,
               kaynak=SahteKaynak([Kayit("mv1", "KANUN", "İŞ KANUNU", "t1")]))
    assert r.durum is Durum.GUNCEL
    assert r.fark.bos_mu()
    assert open(yol, "rb").read() == once


def test_TR_IP_YOKSA_IP_YOK_doner_ve_TARIH_YINE_GORUNUR(tmp_path):
    """⛔ Sert kural: fallback yok, ama kullanıcı ASLA tarihsiz kalmaz (spec §2)."""
    class IpsizKaynak:
        def listele(self, tur):
            raise TrIpGerekli("403")

    r = tazele(Tazelik.OTOMATIK, korpus_yolu=_kur(tmp_path), kaynak=IpsizKaynak())
    assert r.durum is Durum.IP_YOK
    assert r.korpus_tarihi == "2026-09-01T00:00:00"
    assert "tazeleme yapılamadı" in r.mesaj.lower()


def test_KAPALI_modda_AGA_HIC_DOKUNULMAZ(tmp_path):
    class PatlayanKaynak:
        def listele(self, tur):
            raise AssertionError("KAPALI modda ağa dokunuldu")

    r = tazele(Tazelik.KAPALI, korpus_yolu=_kur(tmp_path), kaynak=PatlayanKaynak())
    assert r.durum is Durum.GUNCEL


def test_SOR_modda_ONAY_VERILMEZSE_disk_DEGISMEZ(tmp_path):
    yol = _kur(tmp_path)
    once = open(yol, "rb").read()
    kaynak = SahteKaynak([Kayit("mv1", "KANUN", "İŞ KANUNU", "t2")],
                         {"mv1": [{"madde_id": "m1", "madde_no": "Madde 1"}]})
    r = tazele(Tazelik.SOR, korpus_yolu=yol, kaynak=kaynak, onayla=lambda fark: False)
    assert r.durum is Durum.GUNCEL
    assert open(yol, "rb").read() == once
    assert kaynak.indirilen == [], "onay yokken metin indirildi"


def test_SOR_modda_ONAY_VERILINCE_yazilir(tmp_path):
    yol = _kur(tmp_path)
    kaynak = SahteKaynak([Kayit("mv1", "KANUN", "İŞ KANUNU", "t2")],
                         {"mv1": [{"madde_id": "m1", "madde_no": "Madde 1"}]})
    r = tazele(Tazelik.SOR, korpus_yolu=yol, kaynak=kaynak, onayla=lambda fark: True)
    assert r.durum is Durum.TAZELENDI
    assert Anlik.yukle(yol).kayitlar[0]["text"] == "metin-m1"


def test_ORTADA_AG_KOPARSA_KORPUS_BAYT_BAYT_ESKI_KALIR(tmp_path):
    """⛔ En kritik test: 14 belgeden 9'u inip ağ koparsa hiçbir şey yazılmaz."""
    yol = _kur(tmp_path)
    once = open(yol, "rb").read()
    kaynak = SahteKaynak(
        [Kayit("mv1", "KANUN", "İŞ KANUNU", "t2")],
        {"mv1": [{"madde_id": "m1", "madde_no": "Madde 1"},
                 {"madde_id": "m2", "madde_no": "Madde 2"}]},
        metin_hatasi_at="m2")
    r = tazele(Tazelik.OTOMATIK, korpus_yolu=yol, kaynak=kaynak)
    assert r.durum is Durum.HATA
    assert open(yol, "rb").read() == once, "kısmi tazeleme diske yazıldı"


def test_rapor_korpus_tarihi_HER_HALDE_dolu(tmp_path):
    """Sistemin tamamında kullanıcı asla tarihsiz kalmaz (spec §2)."""
    for mod in (Tazelik.KAPALI, Tazelik.OTOMATIK):
        r = tazele(mod, korpus_yolu=_kur(tmp_path), kaynak=SahteKaynak())
        assert isinstance(r, Rapor) and r.korpus_tarihi
```

- [ ] **Adım 2: Testi koş, BAŞARISIZ olduğunu gör**

Run: `python -m pytest tests/test_mevzuat_tazele.py -v`
Beklenen: `FAIL` — `ImportError: cannot import name 'tazele'`

- [ ] **Adım 3: `_tazele.py`'yi yaz**

```python
# hakhukuk/mevzuat/_tazele.py
"""`tazele()` — mevzuat katmanının tek giriş noktası.

İKİ SERT KURAL (spec §4), ikisi de testle çivili:
  ⛔ TR IP yoksa fallback YOK — Rapor.durum = IP_YOK, korpus tarihi YİNE gösterilir
  ⛔ Kısmi tazeleme diske YAZILMAZ — hepsi ya da hiçbiri

⭐ Mahremiyet: tazelik çağrısı SORUYU TAŞIMAZ. `searchDocuments` yalnız "şu türde hangi
belgeler var, kayitTarihi ne" diye sorar. Sızan tek şey "bu IP korpusunu tazeliyor".
"""
from __future__ import annotations

import datetime

from .anlik import Anlik
from .tazelik import fark_bul
from .tipler import BedestenHatasi, Durum, Fark, Rapor, Tazelik, TrIpGerekli

KORPUS = "data/corpus/mevzuat_maddeler.jsonl"


def _varsayilan_onay(fark: Fark) -> bool:
    cevap = input(f"{fark.toplam()} belge değişmiş "
                  f"(yeni {len(fark.yeni)} · değişen {len(fark.degisen)} · "
                  f"kaybolan {len(fark.kaybolan)}). Güncelleyeyim mi? [e/H] ")
    return cevap.strip().lower() in ("e", "evet", "y", "yes")


def tazele(mod: Tazelik = Tazelik.SOR, *, korpus_yolu: str = KORPUS,
           kaynak=None, onayla=_varsayilan_onay) -> Rapor:
    """Korpusu canlı bedesten'e karşı tazele.

    `mod`: SOR (varsayılan, kullanıcıya sorar) · OTOMATIK · KAPALI.
    ⛔ Bool bayrak yok: "sor" hâli bir bool ile ifade edilemez (CLAUDE.md §4).
    """
    anlik = Anlik.yukle(korpus_yolu)

    if mod is Tazelik.KAPALI:
        return Rapor(durum=Durum.GUNCEL, korpus_tarihi=anlik.tarih,
                     mesaj="tazeleme kapalı")

    if kaynak is None:
        from .kaynak import Kaynak
        kaynak = Kaynak()

    turler = anlik.kunye.get("turler") or ["KANUN"]
    try:
        uzak = [k for tur in turler for k in kaynak.listele(tur)]
    except TrIpGerekli as e:
        # ⛔ YUTULMAZ ama ÜRÜNÜ DÜŞÜRMEZ: kullanıcı korpusuyla çalışmaya devam eder
        # ve TARİHİNİ GÖRÜR. Sessiz düşürme olmayan şey, tarihin gizlenmesidir.
        return Rapor(durum=Durum.IP_YOK, korpus_tarihi=anlik.tarih,
                     mesaj=f"tazeleme yapılamadı (TR IP gerekiyor); "
                           f"korpusun tarihi {anlik.tarih} — {e}")
    except BedestenHatasi as e:
        return Rapor(durum=Durum.HATA, korpus_tarihi=anlik.tarih,
                     mesaj=f"bedesten'e ulaşılamadı; korpusun tarihi {anlik.tarih} — {e}")

    fark = fark_bul(anlik.belge_tarihleri(), uzak)
    if fark.bos_mu():
        return Rapor(durum=Durum.GUNCEL, korpus_tarihi=anlik.tarih, fark=fark,
                     mesaj="korpus güncel")

    if mod is Tazelik.SOR and not onayla(fark):
        return Rapor(durum=Durum.GUNCEL, korpus_tarihi=anlik.tarih, fark=fark,
                     mesaj="kullanıcı güncellemeyi reddetti")

    # ── İNDİRME ── ⛔ hepsi bellekte biriktirilir; TEK BİR hata varsa disk el değmez
    guncel = {k.mevzuat_id: k for k in [*fark.yeni, *fark.degisen]}
    try:
        taze_satirlar = []
        for mid, kayit in guncel.items():
            for m in kaynak.maddeler(mid):
                if not m.get("madde_id"):
                    continue
                taze_satirlar.append({
                    "kanun_no": mid, "kanun_adi": kayit.ad, "madde_no": m["madde_no"],
                    "text": kaynak.madde_metni(m["madde_id"]), "mulga": False,
                    "mevzuat_id": mid, "madde_id": m["madde_id"],
                    "tur": kayit.tur, "kayit_tarihi": kayit.kayit_tarihi})
    except Exception as e:
        return Rapor(durum=Durum.HATA, korpus_tarihi=anlik.tarih, fark=fark,
                     mesaj=f"indirme yarıda kaldı, korpus DEĞİŞMEDİ "
                           f"(tarihi {anlik.tarih}) — {e!r}")

    taze_idler = {r["madde_id"] for r in taze_satirlar}
    degisen_belgeler = set(guncel)
    korunan = [r for r in anlik.kayitlar
               if r.get("madde_id") not in taze_idler
               and r.get("mevzuat_id") not in degisen_belgeler]

    tarihler = dict(anlik.belge_tarihleri())
    tarihler.update({k.mevzuat_id: k.kayit_tarihi for k in guncel.values()})
    yeni_tarih = datetime.datetime.now().isoformat(timespec="seconds")
    Anlik.yaz(korpus_yolu, korunan + taze_satirlar,
              {**anlik.kunye, "tarih": yeni_tarih, "belge_tarihleri": tarihler})

    return Rapor(durum=Durum.TAZELENDI, korpus_tarihi=yeni_tarih, fark=fark,
                 mesaj=f"{fark.toplam()} belge tazelendi; "
                       f"⚠️ indeks BAYAT — `python -m hakhukuk.mevzuat indeksle` gerekiyor")
```

- [ ] **Adım 4: `__init__.py`'yi yaz — paketin tek dış yüzü**

```python
# hakhukuk/mevzuat/__init__.py
"""Mevzuat katmanı — korpusun kapsamı ve tazeliği.

Tasarım: docs/superpowers/specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md

Dışa açılan YALNIZ şunlar. `kaynak` · `tazelik` · `anlik` · `indeksle` iç modüldür;
doğrudan çağırmak bedesten'in tuhaflıklarını çağırana sızdırır.
"""
from ._tazele import tazele
from .tipler import Durum, Fark, Kayit, Rapor, Tazelik, TrIpGerekli

__all__ = ["tazele", "Tazelik", "Rapor", "Durum", "Fark", "Kayit", "TrIpGerekli"]
```

- [ ] **Adım 5: Testleri koş, GEÇTİĞİNİ gör**

Run: `python -m pytest tests/test_mevzuat_tazele.py -v`
Beklenen: `7 passed`

- [ ] **Adım 6: Tüm süiti koş — regresyon yok**

Run: `python -m pytest -q`
Beklenen: **0 failed**

- [ ] **Adım 7: Commit**

```bash
git add hakhukuk/mevzuat/_tazele.py hakhukuk/mevzuat/__init__.py tests/test_mevzuat_tazele.py
git commit -m "hakhukuk.mevzuat.tazele(): ana arayüz, Tazelik enum, iki sert kural

SOR varsayılan; bool bayrak yok çünkü 'sor' hâli bir bool ile ifade edilemez.
IP_YOK'ta fallback YOK ama kullanıcı tarihini GÖRÜYOR — sessiz düşürme olan şey
tarihi gizlemek olurdu. Kısmi indirme testle yasaklandı: 2 maddeden 2.'si
düşünce korpus bayt-bayt eski kalıyor.

Tazeleme çağrısı SORUYU TAŞIMAZ — sızan tek şey 'bu IP korpusunu tazeliyor'.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DgANwHgkTBaaNYpWvczNB5"
```

---

### Görev 9: Kayıt — ADR · research_log · spec ve plan kapanışı

**Dosyalar:**
- Create: `docs/adr/0074-mevzuat-anlik-goruntu-ve-kapsam-kapisi.md`
- Modify: `docs/record/research_log/README.md` *(yeni satır — **var olan satırlar dokunulmaz**)*
- Create: `docs/record/research_log/2026-09-08-kapsam-genislemesi.md`
- Modify: bu plan *(✅ kapanış bloğu)* · `docs/superpowers/README.md` · `CLAUDE.md`

⛔ **`docs/record/**` ve `docs/adr/**` tarihsel kayıttır** — buraya **EKLEME** yapılır,
var olan satır **düzenlenmez**.

- [ ] **Adım 1: ADR-0074'ü yaz**

⚠️ Sıradaki numara **0074**; **0059 REZERVE** (τ_a v2 veri-simetrisi ADR'si, Görev 10'da yazılacak).

İçermesi gerekenler — her biri bu planda **ölçüldü**:
- **Karar:** korpus sürümlenmiş bir anlık görüntüdür; canlılık ürünün dışındadır
- **Elenen:** her soruda canlı API (TR IP herkese bulaşır · API düşerse ürün düşer ·
  **kullanıcının sorusu sızar** · ölçüm yeniden üretilemez olur) · melez atıf doğrulaması
  (`terazi.py`'nin determinizmini bozar)
- **Ölçülen ve tasarımı değiştiren üç şey:**
  (1) *"51 ms"* yalnız yoğun koldu; gerçek ~803 ms, baskın yük **BM25**
  (2) korpusta **kararlı kimlik yoktu** (3.699 çakışma) — artımlı gömmenin ön koşulu
  (3) `fp16` reddedildi: 44,4× yavaş **ve** 10/80 sorguda ilk-10 değişiyor
- **Kapı:** `recall@10 ≥ 0,9500`, koşudan önce yazıldı; **sınırı da yazıldı** — *"eskiyi
  bozmadı"* der, *"yeniyi buluyor"* **demez**
- **Kabul edilen maliyet:** kullanıcı canlı hukukla değil, *tarihi belli* bir korpusla
  çalışır. Bu bilerek **tekrarlanabilirlik lehine** yapılmış bir takastır.

- [ ] **Adım 2: research_log girdisi (#64) + README satırı**

`docs/record/research_log/2026-09-08-kapsam-genislemesi.md` — kat kat kapı sonuçları,
`kayitTarihi` sinyal ölçümü, ölçek kapısının sentetik ↔ gerçek sapması.
README'ye **tek satır** eklenir; var olan satırlara dokunulmaz.

- [ ] **Adım 3: Spec'in açık kalanlarını GÜNCELLE**

`specs/2026-09-07-mevzuat-kapsam-ve-tazelik-design.md` §8'deki altı 🔓 maddesinin her biri
için: **kapandı** (sayıyla) ya da **açık kaldı** (neden). Özellikle:
- `kayitTarihi` sinyal mi → Görev 5 Adım 5 ölçtü
- Yönetmelik düzeyinde eval sorusu yok → **hâlâ açık**, ADR-0067 usulü ayrı tur
- RAM kaldıraçları (`mmap` · boyut indirgeme) → **hâlâ ölçülmedi**

- [ ] **Adım 4: `README.md` ve `CLAUDE.md` işaretçilerini güncelle**

- `README.md`: *"Bir bakışta"* kutusu — bu plan ✅, **Görev 8 (indeks dağıtımı) AÇILDI**
- `CLAUDE.md`: korpus/indeks satırı (*"892 kanun · 40.496 madde"* → yeni sayı) ·
  *"brute force 8,2 ms, indeks 83 MB"* → **yeni ölçüm** · ADR sayacı **0075**

- [ ] **Adım 5: Bu planın ✅ kapanış bloğunu yaz**

Faz 0 planının biçimi: kaç kutucuk · ne harcandı · **hangi iddia çürütüldü** · ne açık kaldı.

- [ ] **Adım 6: Son commit**

```bash
git add docs/
git commit -m "Mevzuat kapsam + tazelik planı KAPANDI — ADR-0074 · research_log #64

Korpus N → M madde, K kat kapıdan geçti. Üç ölçüm tasarımı değiştirdi:
BM25'in baskın maliyeti · korpusta kararlı kimliğin olmaması · fp16'nın reddi.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DgANwHgkTBaaNYpWvczNB5"
```

---

## Bu planın kasten DIŞARIDA bıraktıkları

| iş | nerede | neden burada değil |
| :--- | :--- | :--- |
| **Görev 8b** mülga süzgeci | ana plan `2026-09-07-hp-hat-a-hat-b.md` | Doğruluk meselesi, **beklemiyor** — korpus büyümesinden bağımsız |
| **Görev 8** indeks dağıtımı (S8) | ana plan | Bu plan bitince **açılır**: 79 MB → ~697 MB, *"kurulumda üret"* seçeneği öldü |
| Yönetmelik düzeyinde **yeni eval sorusu** | — | Ayrı tur + **insan onayı** (ADR-0067 usulü); donmuş TEST'i de ilgilendirir |
| RAM kaldıraçları: `mmap` · boyut indirgeme · ayrı indeks profilleri | spec §7b *"açık borç"* | **Hiçbiri ölçülmedi**; ölçek kapısı geçerse gerekmiyor |
| `TEBLIG` türü | spec §8 | Sayısı **ölçülemedi** — sorgu hata verdi |
| Tazeleme **sıklığı** (haftalık mı, aylık mı) | spec §8 | Bugün veri yok; `kayitTarihi` dağılımı yeniden alım hızını gösteriyor olabilir |

---

## Öz-denetim

**1 · Spec kapsaması** — §1 ölçülmüş durum → G1 çıpası · §2 üç karar → G7 (K1·K3) · G8 (K2) ·
§3 mimari → G2·G4·G5·G6 · §4 dört birim + iki sert kural → G2·G4·G5·G6·G8 · §5 kapsam kapısı
→ G1·G7 · §6 test felsefesi → her görevin testleri; `kayitTarihi` yıldızlı testi **G5 Adım 5** ·
§7 reddedilenler → ADR-0074 (G9) · §7b ölçek → **G6 Adım 5 ölçek kapısı** · §8 açık kalanlar →
G9 Adım 3.
**Spec'te olup planda karşılığı olmayan:** yok. **Planda olup spec'te olmayan:** Görev 3
(korpus kimliği) ve Görev 6 Adım 5 (ölçek kapısı) — ikisi de plan yazılırken **ölçülerek**
bulundu ve spec'e §7b'de damgalandı.

**2 · Yer tutucu taraması** — yapıldı. Kod adımlarının hepsi tam gövde taşıyor. Tek
"doldurulacak" nokta Görev 9'un ADR ve kayıt metinleridir; onlar **sonuç sayılarını** bekliyor
ve içermesi gereken maddeler **tek tek listelendi**. Görev 7'nin commit mesajlarında `N`/`M`/
`0,9xxx` yer tutucudur — **ölçülen sayı yazılır**, uydurulmaz.

**3 · Tip tutarlılığı** — `Kayit(mevzuat_id, tur, ad, kayit_tarihi)` G2'de tanımlandı, G4·G7·G8'de
aynı alanlarla kullanıldı · `Fark(yeni, degisen, kaybolan)` G2 → G4 → G8 · `Anlik.yaz(yol,
kayitlar, kunye)` G5 → G7·G8 · `artimli_gom(eski_kayitlar, eski_gomme, yeni_kayitlar, gomucu)`
G6 → G7 · `recall_olc(retriever, sorular, k)` G1 → G7 · `_gomulecek_metin` **iki yerde** var
(`retriever.py` ve `indeksle.py`) ve ayrışırlarsa artımlı ile tam gömme farklı vektör üretir —
`indeksle.py`'nin docstring'i bunu uyarıyor, ve G3'ün `gomulen_metin_ozeti` testi aynı üçlüyü
çiviliyor.
