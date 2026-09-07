"""Ürün yüzeyinin veri tipleri. Donmuş — cevap üretildikten sonra değiştirilemez.

⚠️ Neden `Durum` bir enum, `bool` değil (ölçüldü 2026-09-06/07): çekinme dedektörü ÜÇ kez
yanıldı çünkü dünya ikili değil. `suskunluk_terazisi` üç hâl buldu (cevap · çekinceli cevap ·
suskunluk); Faz 0 dördüncüyü ölçtü (kesik). Vatandaş için en tehlikelisi ORTADAKİdir:
"doğrudan madde yok, bununla birlikte…" — cevap gibi görünür, değildir.
"""
from dataclasses import dataclass
from enum import Enum


class Durum(Enum):
    """Bir cevabın vatandaşa ne söylediği. Kapalı küme."""

    CEVAP = "cevap"            # dayanağı var, atıflı
    CEKINCELI = "cekinceli"    # kısmen dayanaklı — rozetle gösterilir
    SUSKUNLUK = "suskunluk"    # dürüst "bilmiyorum"
    KESIK = "kesik"            # üretim bütçesi bitti — YARIM cevap, gizlenmez


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


@dataclass(frozen=True)
class Atif:
    """Modelin cevapta andığı madde. `dogrulandi` deterministik olarak doldurulur."""

    kanun_no: str
    madde_no: str
    dogrulandi: bool = False


@dataclass(frozen=True)
class Cevap:
    metin: str
    durum: Durum
    atiflar: tuple[Atif, ...]
    kaynaklar: tuple[Kaynak, ...]
