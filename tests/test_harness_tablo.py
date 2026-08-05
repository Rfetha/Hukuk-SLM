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
