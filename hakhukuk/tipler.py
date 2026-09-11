"""Ürün yüzeyinin veri tipleri. Donmuş — cevap üretildikten sonra değiştirilemez.

⚠️ Neden `Durum` bir enum, `bool` değil (ölçüldü 2026-09-06/07): çekinme dedektörü ÜÇ kez
yanıldı çünkü dünya ikili değil. `suskunluk_terazisi` üç hâl buldu (cevap · çekinceli cevap ·
suskunluk); Faz 0 dördüncüyü ölçtü (kesik). Vatandaş için en tehlikelisi ORTADAKİdir:
"doğrudan madde yok, bununla birlikte…" — cevap gibi görünür, değildir.
"""
import re
from dataclasses import dataclass
from enum import Enum

_MADDE_SAYISI_DESENI = re.compile(r"\d+")
_HARF_OBEGI_DESENI = re.compile(r"[^\W\d_]+")


def _madde_sayisi_cikar(madde_no: str) -> int | None:
    """`madde_no`'nun karşılaştırılabilir tam sayı hâli — HAM alanı DEĞİŞTİRMEZ.

    Korpus tutarsız: "MADDE 349" ↔ "Madde 6" ↔ "330" aynı maddeyi üç yazımla taşır; üçü de
    aynı sayıya iner. Alt-madde harfi ("31/a" → 31) bu alanda ATILIR çünkü `madde_sayisi`
    kıyas/sıralama için bir SAYIdır, adres kimliği değil — adres kimliği ham `madde_no`'da
    zaten duruyor.

    ⛔ ÖNEKLİ biçimler ("Geçici Madde 1", "Ek Madde 1", "Mükerrer Madde 1") düz sayıya
    İNDİRGENMEZ, `None` döner. Gerekçe ölçülmüştür (`scripts/erisim_korpus/madde_anahtar.py`):
    *"`Geçici Madde 1` ile `Madde 1` aynı sayılırsa recall@k şişer ve hiçbir yerde hata
    çıkmaz"* — 40.496 madde 27.706 anahtara düşüyor. Bunlar FARKLI maddelerdir; bir `int`
    ikisini de taşıyamaz, dolayısıyla burada üretilecek her değer sessiz bir yalan olurdu.
    Önekli maddeyi kıyaslaması gereken kod `madde_anahtari()` kullanır (`terazi.py`,
    `araclar.py` zaten öyle yapıyor); bu alan o işin YERİNE geçmez.
    Ayrıştırılamayan girdi (rakam yoksa) da `None` — sessiz bir tahmin üretilmez.
    """
    eslesme = _MADDE_SAYISI_DESENI.search(madde_no)
    if eslesme is None:
        return None
    onek = madde_no[:eslesme.start()]
    if any(k.casefold() != "madde" for k in _HARF_OBEGI_DESENI.findall(onek)):
        return None
    return int(eslesme.group())


class Durum(Enum):
    """Bir cevabın vatandaşa ne söylediği. Kapalı küme."""

    CEVAP = "cevap"            # dayanağı var, atıflı
    CEKINCELI = "cekinceli"    # kısmen dayanaklı — rozetle gösterilir
    SUSKUNLUK = "suskunluk"    # dürüst "bilmiyorum"
    KESIK = "kesik"            # üretim bütçesi bitti — YARIM cevap, gizlenmez
    ARAMA_TUKENDI = "arama_tukendi"   # araç döngüsü SINIRA dayandı — dayanak eksik OLABİLİR

    # ⛔ ARAMA_TUKENDI, KESIK ile BİRLEŞTİRİLMEZ (ADR-0076). İkisi vatandaşa FARKLI şey söyler:
    #   KESIK          = "cümle yarım kaldı"        → metne güvenme
    #   ARAMA_TUKENDI  = "cümle tam, dayanağı eksik" → metne güven, DAYANAĞINA güvenme
    # Tek hâle indirmek, sınırın GÖRÜNÜR olması şartını (ADR-0076) sessizce kaldırırdı.


class Yururluk(Enum):
    """Getirilen maddelerin yürürlük süzgeci.

    ⛔ Public API'de bool bayrak yok (CLAUDE.md §4): `getir(..., mulga_dahil=True)`
    çağrı yerinde okunmaz olurdu. Varsayılan YALNIZ_YURURLUKTE — çünkü mülga bir maddeyi
    vatandaşa göstermek eksik özellik değil, YANLIŞ CEVAPtır.
    """

    YALNIZ_YURURLUKTE = "yalniz_yururlukte"   # varsayılan
    MULGA_DAHIL = "mulga_dahil"               # soru tam da mülga maddeyle ilgiliyse


@dataclass(frozen=True)
class Kaynak:
    """Retriever'ın getirdiği tek madde."""

    kanun_adi: str
    kanun_no: str
    madde_no: str
    metin: str
    sira: int

    @property
    def kimlik(self) -> str:
        """`kanun_no/madde_no` — korpustaki anahtar (bkz. tuzak 7.6: %22,7 yineleniyor)."""
        return f"{self.kanun_no}/{self.madde_no}"

    @property
    def madde_sayisi(self) -> int | None:
        """Türetilmiş kıyas alanı — bkz. `_madde_sayisi_cikar`. `madde_no` HAM kalır."""
        return _madde_sayisi_cikar(self.madde_no)


@dataclass(frozen=True)
class Atif:
    """Modelin cevapta andığı madde. `dogrulandi` deterministik olarak doldurulur."""

    kanun_no: str
    madde_no: str
    dogrulandi: bool = False

    @property
    def madde_sayisi(self) -> int | None:
        """Türetilmiş kıyas alanı — bkz. `_madde_sayisi_cikar`. `madde_no` HAM kalır."""
        return _madde_sayisi_cikar(self.madde_no)


@dataclass(frozen=True)
class Cevap:
    metin: str
    durum: Durum
    atiflar: tuple[Atif, ...]
    kaynaklar: tuple[Kaynak, ...]
