"""Ürün tiplerinin kapı testleri (plan Görev 6)."""
import pytest

from hakhukuk.tipler import Atif, Cevap, Durum, Kaynak


def test_durum_dort_hali_var():
    assert {d.name for d in Durum} == {"CEVAP", "CEKINCELI", "SUSKUNLUK", "KESIK"}


def test_cevap_donmus_ve_degistirilemez():
    c = Cevap(metin="x", durum=Durum.CEVAP, atiflar=(), kaynaklar=())
    with pytest.raises(Exception):
        c.metin = "y"


def test_kaynak_kimligi_kanun_madde_ciftidir():
    k = Kaynak(kanun_adi="İŞ KANUNU", kanun_no="4857", madde_no="Madde 31",
               metin="…", sira=1)
    assert k.kimlik == "4857/Madde 31"


def test_atif_dogrulanmamis_olarak_baslar():
    a = Atif(kanun_no="4857", madde_no="Madde 31")
    assert a.dogrulandi is False
