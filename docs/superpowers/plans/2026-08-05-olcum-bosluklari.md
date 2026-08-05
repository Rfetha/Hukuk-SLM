# Ölçüm Boşlukları Turu — Uygulama Planı

> **Ajan işçiler için:** ZORUNLU ALT-SKILL: `superpowers:subagent-driven-development` (önerilen)
> ya da `superpowers:executing-plans` ile görev görev uygula. Adımlar `- [ ]` kutucuklu.

**Hedef:** Sprint 3 Part 1'in ölçmeden bıraktığı üç boşluğu kapatmak — `m2b` harness AÇIK
(kendi gerekçemizin sınanmamış yarısı), K2'nin bedeli (**B5**), yazım-hatası toleransı
(**B8**) — ve ADR-0055'in **B-i** deneyini koşmak.

**Mimari:** Dört işin **ikisi hiç üretim istemiyor** (eldeki `detail.jsonl` dosyaları üzerinde
post-hoc), ikisi birer üretim koşusu. Yeni model yok, yeni eğitim yok, **GPU $0**. Sıra
bağlayıcı değil çünkü ADR-0056 Karar 4 doğrulayıcıyı **donduruyor** — post-hoc işler aleti
değiştirmiyor, yalnız *"değişseydi ne olurdu"*yu sayıyor.

**Yığın:** Python 3.11 · `llama-server` + Q4_K_M GGUF · hakem `openai/gpt-4o-mini`
OpenRouter üzerinden · `pytest`

## Global Kısıtlar

**Bunlar her görevin örtük şartıdır. İhlal, koşuyu geçersiz kılar — hata vermez.**

```
rejim      thinking on · --think-budget 1024 · --max-new-tokens 512 · seed 3407
           --max-chunk-chars 900 · CTX 8192 · temperature 0
model      models/gguf/tgta_v1-q4_k_m.gguf  (tgta_v1 = HakHukuk-4B-v0.1)
indeks     data/index/mevzuat_bge_m3_s2/    ← S2 korpusu. ESKİ indeks KULLANILMAZ.
korpus     data/corpus/mevzuat_maddeler.jsonl
k          10
hakem      GND_JUDGE=openai/gpt-4o-mini · LLM_GATEWAY=openrouter
           LLM_PROVIDER_ORDER=OpenAI  (pin — tuzak 2.7)
bütçe      hakem toplam ≤ $2 · GPU $0
```

🔒 **`scripts/atif_dogrula.py` bu turda DEĞİŞTİRİLMEZ** (ADR-0056 Karar 4). Doğrulayıcı
değişirse kapı kararları değişir, ve hem Ö1 hem D1 farklı aletlerle üretilmiş olur — üstelik
%61,3 çıpası da eski aletle üretildi. B8 toleransının **benimsenmesi** ayrı bir karardır.

⚠️ **A1 her yerde cevaplanan-only** ve `rescore_answered.py` ile **çapraz doğrulanır**
(tuzak **2.16** — bu hattın bir kapı hükmü zaten bir kez metrik hatasıyla tersine döndü).

🛑 **DURMA:** geçerlilik kapısı düşerse (kesik cevap > %5) → koşu **geçersiz**, sonuç
okunmaz, hakem parası harcanmaz.

**Kaynak kararlar:** [ADR-0056](../../adr/0056-m2b-harness-acik-protokolu-ve-0055-cipasi.md) ·
[ADR-0055](../../adr/0055-isabet-denetimi-ekseni.md) ·
borç bağlamları [`sprint3-part1.md`](../../../sprint3-part1.md#post-sprint-3-sırası)

**Çıpalar (hepsi `outputs/eval/s2-harness-k10-etiketli/`):**

```
kütle %61,3 · A1 0,8042 · A1·altın getirilen 0,8616 · coverage 0,7625
recall@10 0,8750 · uydurulmuş madde no 0/118 · katı kapı 1/80 reddetti
m2b harness KAPALI Rej = 0,877          ← Ö1'in çıpası
hakem gürültü tabanı ~0,3 A1 puanı      ← bundan küçük fark YORUMLANMAZ
```

## Dosya Yapısı

| dosya | sorumluluk | görev |
| :--- | :--- | :--- |
| `scripts/harness_tablo.py` | **değişir** — docstring'in 5. maddesi (K2'nin bedeli) yazılı ama **uygulanmamış**; `kapi_katkisi` da yok | 1, 3 |
| `scripts/b8_tolerans_supurme.py` | **yeni** — tolerans eğrisi, post-hoc, doğrulayıcıya dokunmaz | 2 |
| `scripts/gen_eval_grounded.py` | **değişir** — `--harness-no-gold` bayrağı | 3 |
| `scripts/cp0_thinking_gen.sh` | **değişir** — `h2b` modu | 3 |
| `scripts/cp0_thinking_score.sh` | **değişir** — `h2b` puanlama dalı | 3 |
| `tests/test_harness_tablo.py` | **yeni** | 1, 3 |
| `tests/test_b8_tolerans.py` | **yeni** | 2 |
| `docs/record/research_log/2026-08-05-olcum-bosluklari.md` | **yeni** — bu turun kaydı | 6 |

---

### Görev 1: B5 — K2'nin bedeli sayılır *(post-hoc · $0 · üretim yok)*

**Neden:** ADR-0054 K2, *"altın getirildi ama cevap 900 karakter kırpmasının ötesindeydi"*
vakasını **ayrı sınıf olarak saymayı şart koşmuştu**. `harness_tablo.py`'nin docstring'i onu
5. madde diye sayıyor, **kodu yok**, çıktı JSON'unda anahtarı yok. B1'in **7/80**'i bu
sayılmadan temiz değil: içinde *"erişim başardı, kırpma öldürdü"* vakaları olabilir ve o
bambaşka bir çare ister (kırpmayı gevşetmek ↔ modeli eğitmek).

**Dosyalar:**
- Değiştir: `scripts/harness_tablo.py` (`eksenler()` fonksiyonuna yeni eksen)
- Test: `tests/test_harness_tablo.py` *(yeni)*

**Arayüzler:**
- Kullanır: `madde_anahtar.madde_anahtari(kanun_no, madde_no) -> tuple[str,str,str]` ·
  `madde_anahtar.korpus_indeksi(yol) -> dict[tuple, list[dict]]`
- Üretir: `harness_tablo.k2_bedeli(kayit, korpus_idx) -> str` — dört değerden biri döner:
  `"ALTIN_GELMEDI"` · `"TAM"` · `"KIRPILDI"` · `"KIRPILDI_CEVAP_DISI"`.
  Görev 3 bu adı ve dönüş değerlerini aynen kullanır.

- [ ] **Adım 1: Başarısız testi yaz**

`tests/test_harness_tablo.py` dosyasını oluştur:

```python
import sys

import pytest

sys.path.insert(0, "scripts")
from harness_tablo import k2_bedeli  # noqa: E402


KORPUS_IDX = {
    ("4857", "NORMAL", "21"): [{
        "kanun_no": "4857", "kanun_adi": "İŞ KANUNU", "madde_no": "Madde 21",
        # 1. karakterden 40. karaktere kadar giriş, cevap 950. karakterde
        "text": "Giris cumlesi. " + ("dolgu " * 160) + "Isci bir ay icinde basvurur.",
    }],
}


REFERANS = "Isci bir ay icinde isverene basvurur."


def _kayit(context_shown, altin_sirasi=0):
    return {
        "kanun_no": "4857", "madde_no": "Madde 21",
        "context_shown": context_shown,
        "referans": REFERANS,          # ← dayanak kelimeleri buradan çıkar
        "harness": {"k": 10, "altin_sirasi": altin_sirasi, "getirilen": []},
    }


def test_k2_bedeli_altin_gelmediyse_ayri_sinif():
    kayit = _kayit("[KAYNAK 1]\nBASKA KANUN Madde 5\nalakasiz", altin_sirasi=None)
    assert k2_bedeli(kayit, KORPUS_IDX) == "ALTIN_GELMEDI"


def test_k2_bedeli_altin_tam_gosterildiyse_tam():
    tam = KORPUS_IDX[("4857", "NORMAL", "21")][0]["text"]
    kayit = _kayit(f"[KAYNAK 1]\nİŞ KANUNU Madde 21\n{tam}")
    assert k2_bedeli(kayit, KORPUS_IDX) == "TAM"


def test_k2_bedeli_kirpildi_ve_cevap_disarida_kaldi():
    """B5'in ÇEKİRDEK VAKASI: erişim başardı, kırpma cevabı kesti."""
    tam = KORPUS_IDX[("4857", "NORMAL", "21")][0]["text"]
    kayit = _kayit(f"[KAYNAK 1]\nİŞ KANUNU Madde 21\n{tam[:900]}")
    assert k2_bedeli(kayit, KORPUS_IDX) == "KIRPILDI_CEVAP_DISI"


def test_k2_bedeli_kirpildi_ama_cevap_iceride():
    """Kırpıldı ama zararsız — ayrı sayılmalı, yoksa B5 sistematik ŞİŞER."""
    kisa = "Giris cumlesi. Isci bir ay icinde basvurur."
    kayit = _kayit(f"[KAYNAK 1]\nİŞ KANUNU Madde 21\n{kisa}")
    assert k2_bedeli(kayit, KORPUS_IDX) == "KIRPILDI"


def test_k2_bedeli_dayanak_cikarilamazsa_suclamaz():
    """Referans cevapla altın metin hiç örtüşmüyorsa B5 sayılmaz — ölçemediğimiz
    şeyi borç diye yazmak, borcu uydurmaktır."""
    tam = KORPUS_IDX[("4857", "NORMAL", "21")][0]["text"]
    kayit = _kayit(f"[KAYNAK 1]\nİŞ KANUNU Madde 21\n{tam[:900]}")
    kayit["referans"] = "Tamamen alakasiz bambaska sozcukler burada."
    assert k2_bedeli(kayit, KORPUS_IDX) == "KIRPILDI"
```

- [ ] **Adım 2: Testi koş, başarısız olduğunu doğrula**

Çalıştır:
```bash
source ~/code/global_venv/bin/activate && python -m pytest tests/test_harness_tablo.py -v
```
Beklenen: `ImportError: cannot import name 'k2_bedeli' from 'harness_tablo'` — 5 test de hata.

- [ ] **Adım 3: `k2_bedeli` fonksiyonunu yaz**

`scripts/harness_tablo.py`'de `_oran` fonksiyonundan **hemen sonra** ekle:

```python
def _icerik_kelimeleri(metin: str) -> set:
    """≥5 harfli kelimeler — kaba ama deterministik bir içerik-kelime filtresi.
    Türkçe durak kelimelerinin çoğu bu eşiğin altında kalır ve liste bakımı gerekmez."""
    return {w for w in re.findall(r"\w+", (metin or "").lower()) if len(w) >= 5}


def k2_bedeli(kayit, korpus_idx):
    """ADR-0054/K2'nin kabul edilen bedelini SINIFLANDIR (borç B5).

    Dört hâl var ve karıştırılmaları B1'i yanlış okutur:
      ALTIN_GELMEDI        erişim ıskaladı — kırpmanın suçu değil
      TAM                  altın maddenin tamamı bağlamda
      KIRPILDI             kırpıldı ama referans cevabın dayandığı cümle İÇERİDE
      KIRPILDI_CEVAP_DISI  🚨 B5'in çekirdeği: erişim başardı, kırpma cevabı KESTİ

    ⚠️ Why 4 sınıf: "kırpıldı" tek başına bir şey söylemez — 40.496 maddenin çoğu
    900 karakteri aşıyor. Anlamlı olan, kırpmanın CEVABI dışarıda bırakıp
    bırakmadığı. Tek sınıfa indirmek B5'i sistematik olarak şişirir.
    """
    izi = kayit.get("harness") or {}
    if izi.get("altin_sirasi") is None:
        return "ALTIN_GELMEDI"

    anahtar = madde_anahtari(kayit.get("kanun_no"), kayit.get("madde_no"))
    kayitlar = korpus_idx.get(anahtar) or []
    if not kayitlar:
        return "ALTIN_GELMEDI"
    tam_metin = max((r.get("text") or "" for r in kayitlar), key=len)

    gosterilen = kayit.get("context_shown") or ""
    if tam_metin and tam_metin in gosterilen:
        return "TAM"

    # Kırpıldı. Zararlı mı? Ölçüt: referans cevabın DAYANDIĞI kelimeler hâlâ
    # gösteriliyor mu. ⚠️ Why kuyruk eşleştirmesi DEĞİL: "son 60 karakter duruyor mu"
    # maddenin nerede bittiğini ölçer, cevabın nereye dayandığını değil — cevap
    # maddenin ortasındaki bir fıkraya dayanıyorsa o ölçü yanlış suçlama üretir.
    dayanak = _icerik_kelimeleri(kayit.get("referans") or "") & _icerik_kelimeleri(tam_metin)
    if not dayanak:
        return "KIRPILDI"          # dayanak çıkarılamadı → suçlanmaz (borç uydurulmaz)
    kalan = {w for w in dayanak if w in gosterilen.lower()}
    return "KIRPILDI" if len(kalan) / len(dayanak) >= 0.5 else "KIRPILDI_CEVAP_DISI"
```

Aynı dosyanın importlarını kontrol et; eksikse `red_kapisi` importunun **altına** ekle:

```python
import re
from madde_anahtar import madde_anahtari, korpus_indeksi  # noqa: E402
```

- [ ] **Adım 4: Testi koş, geçtiğini doğrula**

Çalıştır:
```bash
source ~/code/global_venv/bin/activate && python -m pytest tests/test_harness_tablo.py -v
```
Beklenen: `5 passed`

- [ ] **Adım 5: Tabloya ekseni bağla**

`scripts/harness_tablo.py` içinde `eksenler(idler)` fonksiyonunun döndürdüğü sözlüğe ekle
(diğer eksenlerin yanına, `erisim_davranis_caprazi`'nın **hemen ardına**):

```python
        "k2_bedeli": {
            sinif: sum(1 for i in s if k2_bedeli(kayitlar[i], _korpus_idx) == sinif)
            for sinif in ("ALTIN_GELMEDI", "TAM", "KIRPILDI", "KIRPILDI_CEVAP_DISI")
        },
```

⚠️ `eksenler()` **indisle** çalışıyor (`s` = indis kümesi, `kayitlar[i]`), kayıt kimliğiyle
değil — bu yüzden `kayitlar[i]` yazılıyor.

`main()` içinde, `Dogrulayici(a.korpus)` satırının **yanına** indeksi bir kez kur:

```python
    _korpus_idx = korpus_indeksi(a.korpus)
```

- [ ] **Adım 6: Gerçek koşuda çalıştır ve sayıyı OKU**

Çalıştır:
```bash
source ~/code/global_venv/bin/activate && python scripts/harness_tablo.py \
  --details outputs/eval/s2-harness-k10-etiketli/h1_tgta_v1_h1_k10_et_detail.jsonl \
  --gnd     outputs/eval/s2-harness-k10-etiketli/gnd_h1_tgta_v1_h1_k10_et.jsonl \
  --korpus  data/corpus/mevzuat_maddeler.jsonl \
  --out     outputs/eval/s2-harness-k10-etiketli/harness_tablo.json
```

Beklenen: JSON'da `k2_bedeli` bloğu belirir ve **dört sınıfın toplamı 80 eder**.
🚨 Toplamıyorsa betik yanlıştır, bulgu değil (**tuzak 7.5**'in genel kuralı).

**Okuma:** `KIRPILDI_CEVAP_DISI` sayısı, B1'in **7/80**'inden düşülmesi gereken paydır.
0 çıkarsa B5 kapanır ve B1 temizdir; >0 çıkarsa B1 **abartılmış** demektir.

- [ ] **Adım 7: Commit**

```bash
git add scripts/harness_tablo.py tests/test_harness_tablo.py \
        outputs/eval/s2-harness-k10-etiketli/harness_tablo.json
git commit -m "B5: K2'nin bedeli sayılıyor — docstring'in 5. maddesi nihayet kodda"
```

---

### Görev 2: B8 — yazım-hatası tolerans eğrisi *(post-hoc · $0 · alet DEĞİŞMEZ)*

**Neden:** Katı kapı, `FİKİR VE SANAT ESERLERİ KANUNU`'nu `…ESELERİ…` diye kopyalayan bir
cevabı **tümüyle** reddetti — madde numaraları doğru, kanun bağlamda var, tek harf düşmüş.
Doğrulayıcının **ilk gerçek yakalayışı** ve o bir fabrikasyon değil **transkripsiyon** hatası.
Tolerans kapıyı **gevşetir**, dolayısıyla ölçülmeden seçilemez: kaç doğru atıf kurtulur ↔
kaç yanlış içeri girer.

🔒 **`atif_dogrula.py` DEĞİŞTİRİLMEZ.** Bu görev *"tolerans şu olsaydı ne olurdu"*yu sayar.

**Dosyalar:**
- Oluştur: `scripts/b8_tolerans_supurme.py`
- Test: `tests/test_b8_tolerans.py` *(yeni)*

**Arayüzler:**
- Kullanır: `atif_dogrula.atiflari_ayikla(cevap) -> list[Atif]` · `atif_dogrula._ad_normal(ad) -> str`
- Üretir: `b8_tolerans_supurme.mesafe(a: str, b: str) -> int` (Levenshtein) ·
  `b8_tolerans_supurme.supur(detay_yolu, korpus_yolu, esikler) -> dict`

- [ ] **Adım 1: Başarısız testi yaz**

`tests/test_b8_tolerans.py` dosyasını oluştur:

```python
import sys

sys.path.insert(0, "scripts")
from b8_tolerans_supurme import mesafe  # noqa: E402


def test_mesafe_ayni_metin_sifir():
    assert mesafe("İŞ KANUNU", "İŞ KANUNU") == 0


def test_mesafe_tek_harf_dusmesi_bir():
    """B8'in gerçek vakası: ESERLERİ → ESELERİ (bir 'R' düşmüş)."""
    assert mesafe("FİKİR VE SANAT ESERLERİ KANUNU",
                  "FİKİR VE SANAT ESELERİ KANUNU") == 1


def test_mesafe_farkli_kanunlar_buyuk():
    """Tolerans BUNLARI birbirine karıştırmamalı — kapının gevşeme riski burada."""
    assert mesafe("TÜRK CEZA KANUNU", "TÜRK MEDENİ KANUNU") > 3


def test_mesafe_simetrik():
    assert mesafe("abc", "abd") == mesafe("abd", "abc")
```

- [ ] **Adım 2: Testi koş, başarısız olduğunu doğrula**

Çalıştır:
```bash
source ~/code/global_venv/bin/activate && python -m pytest tests/test_b8_tolerans.py -v
```
Beklenen: `ModuleNotFoundError: No module named 'b8_tolerans_supurme'`

- [ ] **Adım 3: Betiği yaz**

`scripts/b8_tolerans_supurme.py` dosyasını oluştur:

```python
#!/usr/bin/env python3
"""B8 — katı kapının yazım-hatası toleransı için EĞRİ ÖLÇÜMÜ (borç B8).

🔒 **Bu betik `atif_dogrula.py`'yi DEĞİŞTİRMEZ** (ADR-0056 Karar 4). Yalnız
*"tolerans şu olsaydı ne olurdu"*yu eldeki koşu çıktısı üzerinde sayar.

Neden ölçülmeden karar verilmez: tolerans kapıyı **gevşetir**. `ESERLERİ→ESELERİ`
(mesafe 1) kurtarılmalı, ama `TÜRK CEZA→TÜRK MEDENİ` asla. Aradaki eşik ampiriktir.

Kullanım:
  python scripts/b8_tolerans_supurme.py \\
      --details outputs/eval/s2-harness-k10-etiketli/h1_..._detail.jsonl \\
      --korpus  data/corpus/mevzuat_maddeler.jsonl
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from atif_dogrula import Dogrulayici, DOGRULANDI, KANUN_YOK, _ad_normal  # noqa: E402


def mesafe(a: str, b: str) -> int:
    """Levenshtein. Kütüphane yok — 40 satırlık bir bağımlılık eklemeye değmez."""
    a, b = _ad_normal(a), _ad_normal(b)
    if a == b:
        return 0
    onceki = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        simdi = [i]
        for j, cb in enumerate(b, 1):
            simdi.append(min(onceki[j] + 1, simdi[j - 1] + 1,
                             onceki[j - 1] + (ca != cb)))
        onceki = simdi
    return onceki[-1]


def supur(detay_yolu: str, korpus_yolu: str, esikler=(0, 1, 2, 3)) -> dict:
    """Her eşik için: kaç KANUN_YOK kurtulur, kaç YANLIŞ kanuna eşleşir."""
    dog = Dogrulayici(korpus_yolu)
    adlar = sorted({r["kanun_adi"] for r in dog._kayitlar if r.get("kanun_adi")})

    sonuc = {str(e): {"kurtarilan": 0, "yanlis_esleme": 0, "belirsiz": 0} for e in esikler}
    with open(detay_yolu, encoding="utf-8") as f:
        for satir in f:
            if not satir.strip():
                continue
            kayit = json.loads(satir)
            for h in dog.cevabi_dogrula(kayit.get("cevap") or ""):
                if h.hukum != KANUN_YOK:
                    continue
                yazilan = h.atif.kanun
                for e in esikler:
                    if e == 0:
                        continue
                    adaylar = [ad for ad in adlar if mesafe(yazilan, ad) <= e]
                    kova = sonuc[str(e)]
                    if len(adaylar) == 1:
                        # Bağlamda gösterilen kanunlardan biri mi? Değilse yanlış eşleme.
                        if adaylar[0] in (kayit.get("context_shown") or ""):
                            kova["kurtarilan"] += 1
                        else:
                            kova["yanlis_esleme"] += 1
                    elif len(adaylar) > 1:
                        kova["belirsiz"] += 1
    return sonuc


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--details", required=True)
    p.add_argument("--korpus", default="data/corpus/mevzuat_maddeler.jsonl")
    p.add_argument("--out", default="")
    a = p.parse_args()

    sonuc = supur(a.details, a.korpus)
    cikti = {"kaynak": a.details, "esik_egrisi": sonuc}
    print(json.dumps(cikti, ensure_ascii=False, indent=2))
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(cikti, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
```

- [ ] **Adım 4: Testi koş, geçtiğini doğrula**

Çalıştır:
```bash
source ~/code/global_venv/bin/activate && python -m pytest tests/test_b8_tolerans.py -v
```
Beklenen: `4 passed`

- [ ] **Adım 5: Gerçek koşuda süpür**

Çalıştır:
```bash
source ~/code/global_venv/bin/activate && python scripts/b8_tolerans_supurme.py \
  --details outputs/eval/s2-harness-k10-etiketli/h1_tgta_v1_h1_k10_et_detail.jsonl \
  --korpus  data/corpus/mevzuat_maddeler.jsonl \
  --out     outputs/eval/s2-harness-k10-etiketli/b8_tolerans_egrisi.json
```

Beklenen: `esik_egrisi` bloğu, eşik 1/2/3 için üç sayı.
**Okuma:** `yanlis_esleme > 0` olan **ilk** eşik, toleransın **üst sınırıdır**.

⚠️ **Bu adım tolerans BENİMSEMEZ.** Eğri elde olduktan sonra karar ayrı bir ADR'dir
(ADR-0056 Karar 4). Kapı bu turda **katı** kalır.

- [ ] **Adım 6: Commit**

```bash
git add scripts/b8_tolerans_supurme.py tests/test_b8_tolerans.py \
        outputs/eval/s2-harness-k10-etiketli/b8_tolerans_egrisi.json
git commit -m "B8: tolerans eğrisi ölçüldü — doğrulayıcıya DOKUNULMADI (ADR-0056 m.4)"
```

---

### Görev 3: `--harness-no-gold` — `m2b`'nin harness-AÇIK karşılığı *(kod · üretim YOK)*

**Neden:** ADR-0056 Karar 1. `m2b` harness KAPALI'da bir kurgudur (altın zorla çıkarılır,
4 elle-paketlenmiş çeldirici). Harness AÇIK karşılığı **altın ablasyonudur**: retriever
`k+1` getirir, altın sonuçtaysa **düşürülür**, ilk `k` kalır. Böylece tek değişken
*"çeldiricileri kim seçti"* olur ve bağlam uzunluğu `k=10` ile **aynı** kalır.

**Dosyalar:**
- Değiştir: `scripts/gen_eval_grounded.py:140` civarı *(bayrak)* · `:492-518` *(harness bloğu)*
- Değiştir: `scripts/cp0_thinking_gen.sh` *(`h2b` modu)*
- Değiştir: `scripts/cp0_thinking_score.sh` *(`h2b` puanlama dalı)*
- Test: `tests/test_harness_tablo.py` *(genişletilir)*

**Arayüzler:**
- Kullanır: `retriever.Retriever.getir(soru, k) -> list[dict]` — her parçada `sira` alanı var ·
  `madde_anahtar.madde_anahtari`
- Üretir: `harness_izi["altin_dusuruldu"] -> bool` *(künye izi)* ve
  `harness_izi["altin_sirasi"] -> int | None`. Görev 4'ün geçerlilik kapısı **`altin_sirasi`**
  okur ve ablasyon koşusunda **her kayıtta `None`** olmasını şart koşar.

- [ ] **Adım 1: Başarısız testi yaz**

`tests/test_harness_tablo.py` dosyasının **sonuna** ekle:

```python
from gen_eval_grounded import altin_ablasyonu  # noqa: E402


def test_altin_ablasyonu_altini_dusurur_ve_k_korur():
    parcalar = [
        {"kanun_no": "9999", "madde_no": "Madde 1", "sira": 0},
        {"kanun_no": "4857", "madde_no": "Madde 21", "sira": 1},   # ← altın
        {"kanun_no": "8888", "madde_no": "Madde 3", "sira": 2},
    ]
    kalan = altin_ablasyonu(parcalar, ("4857", "NORMAL", "21"), k=2)
    assert len(kalan) == 2
    assert all(p["kanun_no"] != "4857" for p in kalan)


def test_altin_ablasyonu_altin_yoksa_ilk_k_doner():
    parcalar = [{"kanun_no": str(i), "madde_no": "Madde 1", "sira": i} for i in range(3)]
    kalan = altin_ablasyonu(parcalar, ("4857", "NORMAL", "21"), k=2)
    assert len(kalan) == 2
    assert [p["sira"] for p in kalan] == [0, 1]


def test_altin_ablasyonu_sirayi_yeniden_numaralar():
    """`sira` alanı 0'dan başlamalı — yoksa recall hesabı kayar (tuzak 7.5 ikizi)."""
    parcalar = [
        {"kanun_no": "4857", "madde_no": "Madde 21", "sira": 0},   # ← altın, ilk sırada
        {"kanun_no": "9999", "madde_no": "Madde 1", "sira": 1},
        {"kanun_no": "8888", "madde_no": "Madde 3", "sira": 2},
    ]
    kalan = altin_ablasyonu(parcalar, ("4857", "NORMAL", "21"), k=2)
    assert [p["sira"] for p in kalan] == [0, 1]
```

- [ ] **Adım 2: Testi koş, başarısız olduğunu doğrula**

Çalıştır:
```bash
source ~/code/global_venv/bin/activate && python -m pytest tests/test_harness_tablo.py -v -k ablasyon
```
Beklenen: `ImportError: cannot import name 'altin_ablasyonu'`

- [ ] **Adım 3: Fonksiyonu ve bayrağı yaz**

`scripts/gen_eval_grounded.py`'de, `clip_sources_block` importundan sonraki modül düzeyine ekle:

```python
def altin_ablasyonu(parcalar, altin_anahtar, k):
    """Altın maddeyi getirilen parçalardan DÜŞÜR, ilk k'yı döndür (ADR-0056 Karar 1).

    `m2b`'nin harness-AÇIK karşılığı budur: aynı 80 soru, aynı retriever, ama altın
    madde bağlamda YOK. Tek değişken "çeldiricileri kim seçti" olsun diye k+1 getirilip
    biri düşürülür — bağlam uzunluğu normal k=10 koşusuyla AYNI kalır.

    ⚠️ Why yeniden numaralama: `sira` 0-indeksli ve aşağı akıştaki recall hesabı onu
    okuyor. Düşürme sonrası boşluk bırakmak sessiz kayma üretir (tuzak 7.5'in ikizi).
    """
    kalan = [p for p in parcalar
             if madde_anahtari(p.get("kanun_no"), p.get("madde_no")) != altin_anahtar]
    return [dict(p, sira=yer) for yer, p in enumerate(kalan[:k])]
```

Bayrağı `--sufficiency-preamble`'ın **hemen ardına** ekle:

```python
    p.add_argument("--harness-no-gold", action="store_true",
                   help="ADR-0056 Karar 1 — `m2b`'nin harness-AÇIK karşılığı: retriever "
                        "k+1 getirir, ALTIN madde düşürülür, ilk k kalır. Bağlam uzunluğu "
                        "normal koşuyla AYNI. Yalnız --harness-indeks ile anlamlı.")
```

- [ ] **Adım 4: Harness bloğunu bağla**

`scripts/gen_eval_grounded.py:492-496` arasını değiştir. **Eski:**

```python
            if a.harness_indeks:                        # HARNESS AÇIK: bağlamı retriever seçer
                parcalar = _retriever.getir(soru, a.harness_k)
```

**Yeni:**

```python
            if a.harness_indeks:                        # HARNESS AÇIK: bağlamı retriever seçer
                altin = madde_anahtari(rec.get("kanun_no"), rec.get("madde_no"))
                if a.harness_no_gold:                   # ADR-0056: m2b'nin AÇIK karşılığı
                    parcalar = altin_ablasyonu(
                        _retriever.getir(soru, a.harness_k + 1), altin, a.harness_k)
                else:
                    parcalar = _retriever.getir(soru, a.harness_k)
```

`:510` satırındaki `altin = madde_anahtari(...)` **artık yukarıda** tanımlı — o satırı **sil**
(mükerrer olur). İzi genişlet, `:511-518` bloğunu şununla değiştir:

```python
                harness_izi = {
                    "k": a.harness_k,
                    "altin_dusuruldu": bool(a.harness_no_gold),
                    "altin_sirasi": next(
                        (p["sira"] for p in parcalar
                         if madde_anahtari(p.get("kanun_no"), p.get("madde_no")) == altin), None),
                    "getirilen": [f"{p.get('kanun_adi','')}|{p.get('madde_no','')}"
                                  for p in parcalar],
                }
```

- [ ] **Adım 5: Testi koş, geçtiğini doğrula**

Çalıştır:
```bash
source ~/code/global_venv/bin/activate && python -m pytest tests/ -v -k "ablasyon or k2_bedeli"
```
Beklenen: `8 passed`

- [ ] **Adım 6: `h2b` modunu koşu betiklerine ekle**

`scripts/cp0_thinking_gen.sh` içinde `h1)` satırının **hemen ardına**:

```bash
    # HARNESS AÇIK + ALTIN ABLASYONU (ADR-0056 Karar 1) = m2b'nin harness-AÇIK karşılığı.
    # h1 ile tek farkı budur; k, kırpma, istem ve rejim AYNI kalır.
    h2b) echo "--data $DEV/core_hard.jsonl --harness-indeks $HARNESS_INDEKS --harness-k ${HARNESS_K:-10} --harness-no-gold --n ${N_OVERRIDE:-80}" ;;
```

Veri kapısını da genişlet — `*" h1 "*)` satırını şununla değiştir:

```bash
  *" h1 "*|*" h2b "*) [ -n "${HARNESS_INDEKS:-}" ] || die "h1/h2b modu HARNESS_INDEKS ister (ör. data/index/mevzuat_bge_m3_s2)";;
```

`scripts/cp0_thinking_score.sh` içinde `m2b)` dalını genişlet:

```bash
    m2b|h2b)    # gold GÖSTERİLMEDİ → payda `context_shown` üzerinden
      python scripts/score_abstention.py --details "$D" --label "$L" --out-dir "$OUT_DIR" \
        --source-field context_shown || die "$L abstention başarısız"
      ;;
```

- [ ] **Adım 7: Betikleri sözdizimi kontrolünden geçir**

Çalıştır:
```bash
cd /home/ersoy/code/Hukuk-SLM && bash -n scripts/cp0_thinking_gen.sh scripts/cp0_thinking_score.sh \
  && source ~/code/global_venv/bin/activate && python -m py_compile scripts/gen_eval_grounded.py \
  && python -m pytest tests/ -q
```
Beklenen: sözdizimi hatası yok, `53 passed`

- [ ] **Adım 8: Commit**

```bash
git add scripts/gen_eval_grounded.py scripts/cp0_thinking_gen.sh \
        scripts/cp0_thinking_score.sh tests/test_harness_tablo.py
git commit -m "h2b modu: m2b'nin harness-AÇIK karşılığı — altın ablasyonu (ADR-0056 m.1)"
```

---

### Görev 4: Ö1 — `m2b` harness AÇIK koşulur *(üretim + hakem ~$0,04)*

**Neden:** Sprint 3 Part 1'in iki gerekçesinden biri *"red kapısı M2b'yi kapatır"* idi ve
**hiç sınanmadı**. Bu görev onu sınar.

⚠️ **Ön-kayıtlı tahmin ADR-0056 Karar 2'de yazılı ve bu görev koşulmadan ÖNCE okunmalıdır.**
Sayı görüldükten sonra tahmine bakmak, tahmini yok saymakla aynıdır.

**Dosyalar:**
- Oluştur: `outputs/eval/olcum-h2b/` *(koşu çıktısı)*
- Değiştir: yok *(Görev 3 kodu hazırladı)*

**Arayüzler:**
- Kullanır: Görev 3'ün `h2b` modu · `harness_izi["altin_dusuruldu"]`
- Üretir: `outputs/eval/olcum-h2b/h2b_<etiket>_detail.jsonl` — Görev 6 bunu kayda geçirir.

- [ ] **Adım 1: Üretimi koş**

Çalıştır:
```bash
cd /home/ersoy/code/Hukuk-SLM && cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
mkdir -p outputs/eval/olcum-h2b && \
MODES="h2b" OUT_DIR="outputs/eval/olcum-h2b" \
HARNESS_INDEKS="data/index/mevzuat_bge_m3_s2" HARNESS_K=10 \
bash scripts/cp0_thinking_gen.sh models/gguf/tgta_v1-q4_k_m.gguf tgta_v1_h2b_k10 \
  2>&1 | tee outputs/eval/olcum-h2b/kosu.log
```
Beklenen: `80/80` üretim, `outputs/eval/olcum-h2b/h2b_tgta_v1_h2b_k10_detail.jsonl` oluşur.

- [ ] **Adım 2: 🛑 GEÇERLİLİK KAPISI — hakem parası harcanmadan ÖNCE**

Çalıştır:
```bash
source ~/code/global_venv/bin/activate && python - <<'PY'
import json
yol = "outputs/eval/olcum-h2b/h2b_tgta_v1_h2b_k10_detail.jsonl"
k = [json.loads(s) for s in open(yol, encoding="utf-8") if s.strip()]
kesik = sum(1 for r in k if r.get("finish_reason") == "length")
altin_sizdi = sum(1 for r in k if (r.get("harness") or {}).get("altin_sirasi") is not None)
print(f"n={len(k)}  kesik={kesik} (%{100*kesik/len(k):.1f})  ALTIN SIZAN={altin_sizdi}")
assert len(k) == 80,        "🚫 n 80 değil — küme değişmez ihlali (ADR-0054 K4)"
assert kesik / len(k) <= .05, "🚫 kesik > %5 → KOŞU GEÇERSİZ, hakem çağrılmaz"
assert altin_sizdi == 0,     "🚫 ablasyon SIZDIRIYOR — altın hâlâ bağlamda, koşu anlamsız"
print("✅ geçerlilik kapısı GEÇTİ — hakem çağrılabilir")
PY
```
Beklenen: `✅ geçerlilik kapısı GEÇTİ`.
🚨 `ALTIN SIZAN > 0` çıkarsa **dur** — ablasyon çalışmıyor, Görev 3 Adım 4'e dön.

- [ ] **Adım 3: Hakemi koş**

Çalıştır:
```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
set -a && source .env && set +a && \
MODES="h2b" OUT_DIR="outputs/eval/olcum-h2b" \
bash scripts/cp0_thinking_score.sh tgta_v1_h2b_k10 \
  2>&1 | tee outputs/eval/olcum-h2b/hakem.log
```
Beklenen: `score_abstention.py` koşar, `outputs/eval/olcum-h2b/abstain_h2b_*.json` oluşur.

- [ ] **Adım 4: İki sayıyı AYRI çıkar**

Çalıştır:
```bash
source ~/code/global_venv/bin/activate && python scripts/harness_tablo.py \
  --details outputs/eval/olcum-h2b/h2b_tgta_v1_h2b_k10_detail.jsonl \
  --korpus  data/corpus/mevzuat_maddeler.jsonl \
  --out     outputs/eval/olcum-h2b/harness_tablo.json
```

Sonra iki sayıyı oku:
```bash
source ~/code/global_venv/bin/activate && python - <<'PY'
import json
t = json.load(open("outputs/eval/olcum-h2b/harness_tablo.json", encoding="utf-8"))
cov = t["kutle_ekseni"]["coverage"]
kapi = t["kapi"]["kati"]
rej_model = round(1 - cov, 4)
katki = round((kapi["kapi_sonrasi_coverage"] and cov - kapi["kapi_sonrasi_coverage"]) or 0, 4)
print(f"Rej_model        = {rej_model}    (çıpa: m2b KAPALI 0,877)")
print(f"kapının KATKISI  = {katki}    ({kapi['reddedilen']}/80 reddedildi)")
PY
```

- [ ] **Adım 5: 🚨 ÖN-KAYITLI TAHMİNE KARŞI HÜKMÜ YAZ**

ADR-0056 Karar 2'nin tahmini:

| | tahmin | tutarsa | tutmazsa |
| :--- | :--- | :--- | :--- |
| **A** kapının katkısı | **≈0** (0-2/80) | Part 1'in M2b iddiası **yapısal olarak çürük** → M2b eğitim tarafına geçer | kapı hakkını veriyor, yürürlükte kalır |
| **B** `Rej_model` | **0,30-0,60** | — | — |
| | `< 0,877` | 🚨 harness M2b eksenini **kötüleştiriyor** — manşet bulgu | |

⚠️ Sayıyı **olduğu gibi** yaz. Tahmin tutmazsa *"tahmin kötüydü"* değil, **"payda yanlıydı"**
diye oku — ADR-0056 B tahmininin yanlı bir alt kümeden türetildiğini **kendi içinde** yazıyor.

- [ ] **Adım 6: Commit**

```bash
git add outputs/eval/olcum-h2b/
git commit -m "Ö1: m2b harness AÇIK ilk kez ölçüldü — Part 1'in sınanmamış yarısı"
```

---

### Görev 5: D1 — B-i deneyi *(kaynak-yeterliliği önsözü · üretim + hakem ~$0,04)*

**Neden:** ADR-0055. Aşırı-red (**16/80**) ve isabetsizlik (**7/80**) açıklarına **tek deneyle**
dokunan en ucuz müdahale. Bayrak `--sufficiency-preamble` **zaten var**.

**Dosyalar:**
- Oluştur: `outputs/eval/olcum-bi/` *(koşu çıktısı)*
- Değiştir: yok

**Arayüzler:**
- Kullanır: `gen_eval_grounded.py --sufficiency-preamble` *(mevcut)* · `h1` modu
- Üretir: `outputs/eval/olcum-bi/h1_<etiket>_detail.jsonl`

- [ ] **Adım 1: Yön çıpasını post-hoc hesapla — koşudan ÖNCE**

ADR-0056 Karar 3: kabul ölçütünün ikinci ayağı *"belirsiz alt kümede çekinme ≥ ayırt edici
alt kümede"*. Bu oranın **S2 korpusundaki** güncel değeri bilinmiyor (#53 S2-öncesinde ölçtü).

Çalıştır:
```bash
source ~/code/global_venv/bin/activate && python - <<'PY'
import json
t = json.load(open("outputs/eval/s2-harness-k10-etiketli/harness_tablo.json", encoding="utf-8"))
alt = t["ayirt_edicilik_alt_kumeleri"]
for ad in ("belirsiz", "ayirt_edici"):
    print(f"{ad:12s} n={alt[ad]['n']:3d}  çekinme={round(1-alt[ad]['coverage'],4)}")
print("→ ÇIPA: yön DOĞRU ise belirsiz ≥ ayırt edici")
PY
```
Bu iki sayıyı **not al** — D1'in kabul ölçütü bunlara karşı okunacak.

- [ ] **Adım 2: `EXTRA_ARGS` desteğini ekle** *(betikte YOK — doğrulandı)*

`scripts/cp0_thinking_gen.sh:113` civarındaki python çağrısında `$ARGS`'ın **ardına** ekle:

```bash
    --label "${M}_${TAG}" --out-dir "$OUT_DIR" $ARGS ${EXTRA_ARGS:-} \
```

Ve künye bloğuna (`echo "  gguf      : $GGUF"` satırının yanına) ekle:

```bash
echo "  ekstra    : ${EXTRA_ARGS:-<yok>}"
```

⚠️ **Why künyeye yazılıyor:** bayrağı elle koşuya gömmek bu hattın en pahalı tuzak sınıfıdır
(*dropped flag*, `yurutme-tuzaklari.md`) — künyede görünmeyen bayrak sessizce düşer ve koşu
geçerli görünür.

Doğrula ve commit et:
```bash
cd /home/ersoy/code/Hukuk-SLM && bash -n scripts/cp0_thinking_gen.sh && \
git add scripts/cp0_thinking_gen.sh && \
git commit -m "cp0_thinking_gen: EXTRA_ARGS + künyeye yazılması (dropped-flag sigortası)"
```

- [ ] **Adım 3: Üretimi koş**

Çalıştır:
```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
mkdir -p outputs/eval/olcum-bi && \
MODES="h1" OUT_DIR="outputs/eval/olcum-bi" \
HARNESS_INDEKS="data/index/mevzuat_bge_m3_s2" HARNESS_K=10 \
EXTRA_ARGS="--sufficiency-preamble" \
bash scripts/cp0_thinking_gen.sh models/gguf/tgta_v1-q4_k_m.gguf tgta_v1_bi_k10 \
  2>&1 | tee outputs/eval/olcum-bi/kosu.log
```

Beklenen: `80/80` üretim, künyede `ekstra : --sufficiency-preamble` görünür.

- [ ] **Adım 4: 🛑 GEÇERLİLİK KAPISI + bayrağın gerçekten uygulandığının kanıtı**

Çalıştır:
```bash
source ~/code/global_venv/bin/activate && python - <<'PY'
import json
yol = "outputs/eval/olcum-bi/h1_tgta_v1_bi_k10_detail.jsonl"
k = [json.loads(s) for s in open(yol, encoding="utf-8") if s.strip()]
kesik = sum(1 for r in k if r.get("finish_reason") == "length")
print(f"n={len(k)}  kesik={kesik} (%{100*kesik/len(k):.1f})")
assert len(k) == 80, "🚫 n 80 değil"
assert kesik / len(k) <= .05, "🚫 kesik > %5 → KOŞU GEÇERSİZ"
print("✅ geçerlilik kapısı GEÇTİ")
PY
grep -c "sufficiency" outputs/eval/olcum-bi/kosu.log
```
🚨 Logda `sufficiency` **görünmüyorsa bayrak düşmüştür** — koşu geçersiz, tekrarla.
Bu, bu hattın en pahalı tuzak sınıfıdır (*dropped flag*, `yurutme-tuzaklari.md`).

- [ ] **Adım 5: Hakemi koş**

Çalıştır:
```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && \
set -a && source .env && set +a && \
MODES="h1" OUT_DIR="outputs/eval/olcum-bi" \
bash scripts/cp0_thinking_score.sh tgta_v1_bi_k10 \
  2>&1 | tee outputs/eval/olcum-bi/hakem.log
```
Beklenen: `groundedness.py` **ve** `rescore_answered.py` koşar (A1 cevaplanan-only, tuzak 2.16).

- [ ] **Adım 6: Tabloyu çıkar ve hükmü ver**

Çalıştır:
```bash
source ~/code/global_venv/bin/activate && python scripts/harness_tablo.py \
  --details   outputs/eval/olcum-bi/h1_tgta_v1_bi_k10_detail.jsonl \
  --gnd       outputs/eval/olcum-bi/gnd_h1_tgta_v1_bi_k10.jsonl \
  --etiketler outputs/eval/s3-ayirt-edicilik/etiketler.jsonl \
  --korpus    data/corpus/mevzuat_maddeler.jsonl \
  --out       outputs/eval/olcum-bi/harness_tablo.json
```

**Ön-kayıtlı kabul (ADR-0055 + ADR-0056 Karar 3):**

```
BAŞARILI  : kütle > %61,3   VE   yön doğru (belirsiz çekinme ≥ ayırt edici çekinme)
KISMİ     : kütle %61,3 ± 1 puan, ama yön düzeliyor  → sinyal doğru, eşik yanlış
BAŞARISIZ : kütle DÜŞER ya da yön bozulur            → B-i düşer, B-ii'ye geçilir
```

⚠️ **Hakem gürültü tabanı ~0,3 A1 puanı.** Kütledeki 0,3 puandan küçük fark
**yorumlanmaz** — o taban aynı girdide ölçüldü (#55 §9).

⚠️ **A1'i `rescore_answered` ile çapraz doğrula:** `harness_tablo.json`'daki
`kutle_ekseni.A1_cevaplanan` ile `a1_*.txt` içindeki `A1_faithfulness_macro_answered`
**eşleşmeli**. Eşleşmiyorsa tuzak 2.16 tekrarlıyor — dur.

- [ ] **Adım 7: Commit**

```bash
git add outputs/eval/olcum-bi/
git commit -m "D1: B-i deneyi koşuldu — kaynak-yeterliliği önsözü (ADR-0055)"
```

---

### Görev 6: Kayıt — research_log + belge güncellemeleri

**Neden:** Repo kuralı: *"her bulgu AYNI GÜN `research_log`"*. Sohbette kalan bulgu kayıp
bulgudur. Ve **negatif/şaşırtıcı sonuç birinci sınıftır** — bu tur onlardan üretmeye
elverişli (tahminlerin ikisi de tutmayabilir).

**Dosyalar:**
- Oluştur: `docs/record/research_log/2026-08-05-olcum-bosluklari.md`
- Değiştir: `docs/record/research_log/README.md` *(satır ekle, numara #56'dan devam)*
- Değiştir: `sprint3-part1.md` *(borç tablosu: B5 · B8 · B1 · B10 durumları)*
- Değiştir: `ROADMAP.md` · `MODEL_CARD.md` *(yalnız sayı değiştiyse)*

- [ ] **Adım 1: research_log girdisini yaz**

`docs/record/research_log/2026-08-05-olcum-bosluklari.md` oluştur. **Zorunlu bölümler:**

```markdown
# #56 — Ölçüm boşlukları: m2b harness AÇIK · B5 · B8 · B-i

**Tarih:** 2026-08-05 · **Plan:** [`docs/superpowers/plans/2026-08-05-olcum-bosluklari.md`](...)
**Kararlar:** [ADR-0056](...) · [ADR-0055](...)

## Künye
model · indeks · k · seed · think-budget · hakem · geçit · koşu dizinleri · maliyet

## 1. Ö1 — m2b harness AÇIK
ön-kayıtlı tahmin ↔ ÇIKAN SAYI, yan yana. Tahmin tutmadıysa NEDEN.

## 2. B5 — K2'nin bedeli
dört sınıfın sayıları · B1'in 7/80'inden düşülen pay

## 3. B8 — tolerans eğrisi
eşik ↔ kurtarılan ↔ yanlış eşleme · ⚠️ tolerans BENİMSENMEDİ

## 4. D1 — B-i deneyi
kütle · yön · ön-kayıtlı kabule karşı hüküm

## Ders
Sayı değil MEKANİZMA. Bu turun bir cümlelik dersi ne?

## Açık kalanlar
hangi borç kapandı, hangisi açık kaldı, yeni borç doğdu mu
```

- [ ] **Adım 2: Dizine satır ekle**

`docs/record/research_log/README.md` tablosuna `#56` satırını ekle — **sayılarla**,
önceki satırların yoğunluğunda.

- [ ] **Adım 3: Borç tablosunu güncelle**

`sprint3-part1.md`'de: **B5** kapandıysa ✅ KAPANDI tablosuna taşı · **B8** eğrisi ölçüldü
diye işaretle *(tolerans benimsenmediği için AÇIK kalır)* · **B1**'i B5'in düştüğü payla
düzelt · **B10**'u D1'in sonucuyla güncelle.

⚠️ Bir borç kapanırken **açık ↔ kapalı tablolarının ikisi de** düzenlenir; yalnız birini
düzenlemek sayıyı tutarsız bırakır (bu hata Part 1'de bir kez oldu: B8 satırı tablonun
**dışında** kalmıştı).

- [ ] **Adım 4: Manşet sayı değiştiyse üç belgeye birden işle**

Kütle değiştiyse `ROADMAP.md` · `MODEL_CARD.md` · `CLAUDE.md` **aynı commit'te** güncellenir.
Biri atlanırsa repo kendi içinde çelişir — ve bu, `research_log/README.md`'de bir kez
gerçekten oldu.

- [ ] **Adım 5: Testleri son kez koş**

Çalıştır:
```bash
cd /home/ersoy/code/Hukuk-SLM && source ~/code/global_venv/bin/activate && python -m pytest tests/ -q
```
Beklenen: tüm testler geçer.

- [ ] **Adım 6: Commit**

```bash
git add docs/ sprint3-part1.md ROADMAP.md MODEL_CARD.md CLAUDE.md
git commit -m "#56: ölçüm boşlukları kapandı — m2b AÇIK, B5, B8 eğrisi, B-i"
```

---

## Bu plan NE YAPMIYOR — ve neden

| yapılmıyor | neden |
| :--- | :--- |
| **Eğitim turu (B10 · B4)** | En büyük açık (**16/80**) burada ama **GPU parası ister** ve hedefi bu turun sonucuna bağlı: Ö1 kapının m2b'yi kapatmadığını gösterirse eğitimin hedef listesi **değişir**. Bugün eğitim atmak, henüz sayılmamış bir açığa para harcamak olurdu. |
| **Korpus-dışı soru kümesi** | ADR-0056 Karar 1: **çıpası yok**, iddia denetimi yapamaz. Kapsam dışı değil, **sonraki**. |
| **B8 toleransını benimsemek** | ADR-0056 Karar 4: alet tur boyunca **donuk**. Eğri elde olunca karar kendi ADR'sini alır. |
| **Yeniden-sıralama (ADR-0055 C)** | ADR-0055: B ile aynı turda koşulursa **ikisi de yorumlanamaz**. Ayrı tur. |
| **B9 indeks hijyeni** | İndeksi değiştirir → `recall@k` kayar → bu turun tüm kıyasları geçersizleşir. İndeksin zaten değişeceği bir turla paketlenir. |
| **B6 canlı bedesten** | Ürün işi; doğruluk işleri bitince. |
| **Rakip harness AÇIK** | Gerçek bir boşluk ama **ayrı bütçe ve ayrı protokol** ister (maliyet normalizasyonu, ADR-0017). Bu tur kendi modelimizi ölçüyor. |
