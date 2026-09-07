"""Belge katmanının kapı testleri (plan Görev 13).

⚠️ Neden test: doküman katmanı 2026-09-06'da silindi ve geriye ONLARCA kırık işaretçi kaldı
(`ROADMAP.md` 10 yerde, `TODO.md` 4 yerde…). Gözle taramak bunu kaçırır; döngü kaçırmaz.
⛔ `docs/record/**` ve `docs/adr/**` KAPSAM DIŞI — onlar tarihsel kayıttır, "o gün şu belge
şunu diyordu" bilgisini taşırlar ve kırık link onarımında bile DEĞİŞTİRİLMEZ.
"""
import pathlib
import re

KOK = pathlib.Path(__file__).resolve().parent.parent
# Canlı belgeler — tarihsel kayıt (docs/record, docs/adr) ve planlar hariç.
CANLI = ["CLAUDE.md", "README.md", "README.tr.md", "MODEL_CARD.md",
         "PRODUCT.md", "ROADMAP.md", "TODO.md", "docs/MIMARI.md",
         "docs/YENIDEN_URETIM.md"]
# Markdown bağlantısı; http(s), mailto ve saf çapa (#…) atlanır.
_LINK = re.compile(r"\[[^\]]*\]\((?!https?://|mailto:|#)([^)\s]+)\)")


def _kirik_baglantilar(belge: pathlib.Path) -> list[str]:
    kirik = []
    for hedef in _LINK.findall(belge.read_text(encoding="utf-8")):
        yol = (belge.parent / hedef.split("#", 1)[0]).resolve()
        if not yol.exists():
            kirik.append(hedef)
    return kirik


def test_canli_belgelerde_kirik_baglanti_yok():
    rapor = {}
    for ad in CANLI:
        p = KOK / ad
        if not p.exists():
            rapor[ad] = ["BELGENİN KENDİSİ YOK"]
            continue
        if kirik := _kirik_baglantilar(p):
            rapor[ad] = kirik
    assert not rapor, "kırık bağlantılar:\n" + "\n".join(
        f"  {a}: {', '.join(k)}" for a, k in rapor.items())


def test_dort_belge_de_var():
    """Faz 3'ün varlık sebebi: bu dördü 2026-09-06'da silinmişti ve yerine hiçbir şey yoktu."""
    for ad in ("PRODUCT.md", "ROADMAP.md", "TODO.md", "docs/MIMARI.md"):
        assert (KOK / ad).exists(), f"{ad} yok"


def test_mimari_her_urun_modulunu_var_olan_dosyaya_baglıyor():
    """MIMARI.md'nin ürün tablosu gerçek dosyaları göstermeli — kutu ≠ niyet."""
    metin = (KOK / "docs" / "MIMARI.md").read_text(encoding="utf-8")
    for modul in ("istem.py", "tipler.py", "terazi.py", "servis.py", "cli.py", "tui.py"):
        assert modul in metin, f"MIMARI.md {modul}'yi anmıyor"
        assert (KOK / "hakhukuk" / modul).exists(), f"hakhukuk/{modul} yok"
