"""suskunluk_terazisi — ürün yüzeyi.

⚠️ NEDEN VAR (üç kez ölçüldü, üçünde de alet FAZLA RED saydı):
   2026-09-06  bizim şablon, önsözsüz    alet 14 → göz  8   (ADR-0061)
   2026-09-06  Gemini şablonu, F0.4      alet 11 → göz  7
   2026-09-07  kör mod, iki kol          alet  6 → göz  0   (6/6 yanlış pozitif)

Kök sebep: "…bulunmamaktadır" ailesi hukuk metninde İKİ iş görür —
  (a) "kaynakta yok, cevaplayamam"  = çekinme
  (b) "kanunda böyle bir hüküm yok" = ESASA İLİŞKİN CEVAP
Metne tek başına bakan bir sınıflandırıcı bunları ayıramaz. Bu modül `kaynaklar`ı da
görür: kaynak YOKSA (a) mümkündür, kaynak VARSA (b) çok daha olasıdır.
"""
import os
import re
import sys

from hakhukuk.tipler import Atif, Durum, Kaynak

# ⚠️ `score_abstention` scripts/puanlama/ ALT KLASÖRÜNDE (T5 bölünmesi, 2026-09-07);
# yalnız `scripts` eklemek yetmez — planın yazdığı yol eksikti.
_KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_KOK, "scripts", "puanlama"))
from score_abstention import REJECT_RE  # noqa: E402  — TEK KAYNAK, kopyalanmaz

# "Kanunda hüküm yok" kalıbı: olumsuzlama + hemen ardından bir madde/kanun atfı.
# Bu birleşim bir CEVAPTIR; tek başına olumsuzlama değildir.
_ESASA_ILISKIN = re.compile(
    r"(bulunmamakta|belirtilmemiş|yer almaz|düzenlenmemiş)", re.IGNORECASE)
# İki yazım da tutulmalı — ikisi de gerçek cevaplarda ölçüldü:
#   "Madde 31" / "md. 31"   → anahtar ÖNCE
#   "503. madde" / "33. maddesi" → sayı ÖNCE  (planın regex'i bunu KAÇIRIYORDU)
_ATIF = re.compile(
    r"(?:(\d{3,5})\s*[Ss]ayılı[^.]{0,60}?)?"
    r"(?:(?:madde|md\.?)\s*[:\s]*([0-9]+(?:/[a-zA-Z])?)"
    r"|([0-9]+(?:/[a-zA-Z])?)\s*\.?\s*madde)", re.IGNORECASE)


def _atiflari_cikar(metin: str, kaynaklar: tuple[Kaynak, ...]) -> tuple[Atif, ...]:
    """Metindeki madde atıflarını çıkar ve GETİRİLEN kaynaklara karşı doğrula.

    Doğrulama deterministik: atıf, getirilen kaynakların kimlik kümesinde varsa doğrudur.
    Yoksa `dogrulandi=False` — bu, kullanıcıya UYARIYLA gösterilir, sessizce geçilmez.
    """
    kimlikler = {k.kimlik for k in kaynaklar}
    kanunlar = {k.kanun_no for k in kaynaklar}
    out: list[Atif] = []
    for kanun_no, madde_sonra, madde_once in _ATIF.findall(metin):
        madde = madde_sonra or madde_once
        # Kanun numarası anılmadıysa ancak TEK kaynak varsa ona atfedilir; birden çok
        # kaynakta hangisine ait olduğu belirsizdir ve TAHMİN EDİLMEZ (boş kalır ⇒
        # doğrulanmamış sayılır, kullanıcıya uyarıyla gider).
        kn = kanun_no or (next(iter(kanunlar)) if len(kanunlar) == 1 else "")
        mn = f"Madde {madde}"
        out.append(Atif(kanun_no=kn, madde_no=mn, dogrulandi=f"{kn}/{mn}" in kimlikler))
    return tuple(out)


def siniflandir(
    metin: str, kaynaklar: tuple[Kaynak, ...], finish_reason: str
) -> tuple[Durum, tuple[Atif, ...]]:
    """Cevabı dört durumdan birine ayır ve atıflarını doğrula.

    Yan etkisi yok, idempotent. `finish_reason` üretimden GELDİĞİ GİBİ verilir —
    "length" sessizce yutulmaz (Faz 0: yarım cümle teslim edilmişti).
    """
    atiflar = _atiflari_cikar(metin, kaynaklar)

    if finish_reason == "length":
        return Durum.KESIK, atiflar

    red = bool(REJECT_RE.search(metin))
    esasa = bool(_ESASA_ILISKIN.search(metin))

    if red and not kaynaklar:
        # Kaynak yok ⇒ "kaynakta yok, cevaplayamam" okuması MÜMKÜN.
        return Durum.SUSKUNLUK, atiflar
    if red and kaynaklar and not atiflar:
        # Kaynak var ama model hiçbirine dayanmadı ⇒ gerçek çekinme.
        return Durum.SUSKUNLUK, atiflar
    if esasa or any(not a.dogrulandi for a in atiflar):
        # Olumsuz hüküm ya da doğrulanamayan atıf ⇒ çekinceli: cevap gibi görünür, tam değildir.
        return Durum.CEKINCELI, atiflar
    return Durum.CEVAP, atiflar
