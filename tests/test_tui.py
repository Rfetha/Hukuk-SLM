"""TUI'nin İNCE KABUK olduğunu sınayan kapı (plan Görev 12)."""
import inspect

from hakhukuk import tui


def test_tui_kendi_mantigi_yok_yalnizca_answer_cagirir():
    """TUI ince kabuktur. Sınıflandırma/atıf mantığı BURAYA sızarsa iki yerde bakım olur."""
    kaynak = inspect.getsource(tui)
    for yasak in ("REJECT_RE", "re.compile", "siniflandir(", "_getir(", "_uret("):
        assert yasak not in kaynak, f"TUI'ye mantık sızmış: {yasak}"
    assert "answer(" in kaynak


def test_sorumluluk_ibaresi_TEK_kaynaktan_geliyor():
    """S18'in dersi: aynı metin iki yerde durursa sessizce ayrışır."""
    from hakhukuk.cli import SORUMLULUK_IBARESI
    assert tui.SORUMLULUK_IBARESI is SORUMLULUK_IBARESI
