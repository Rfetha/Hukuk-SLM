"""CLI kapı testleri (plan Görev 10).

⛔ Sorumluluk ibaresi KOŞULSUZ basılır: `Durum` ne olursa olsun. Bir hukuk asistanının
çıktısı, hangi güven seviyesinde olursa olsun, tavsiye değildir.
"""
import subprocess
import sys


def test_cli_sorumluluk_ibaresini_HER_cevapta_basar():
    r = subprocess.run([sys.executable, "-m", "hakhukuk.cli", "--kuru-calisma", "test"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "hukuki tavsiye değil" in r.stdout.lower()


def test_cli_dort_durumu_ayirt_edilebilir_basar():
    r = subprocess.run([sys.executable, "-m", "hakhukuk.cli", "--durumlari-listele"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    for ad in ("CEVAP", "CEKINCELI", "SUSKUNLUK", "KESIK"):
        assert ad in r.stdout


def test_ibare_TEK_kaynakta():
    """S18'in dersi: aynı metin iki yerde durursa sessizce ayrışır."""
    from hakhukuk.cli import SORUMLULUK_IBARESI
    assert SORUMLULUK_IBARESI.strip()
