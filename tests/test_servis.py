"""Servis katmanının kapı testleri (plan Görev 9). Sunucu ve indeks GEREKMEZ."""
from hakhukuk import servis
from hakhukuk.tipler import Durum, Kaynak

IS_K_31 = Kaynak(kanun_adi="İŞ KANUNU", kanun_no="4857", madde_no="Madde 31",
                 metin="Muvazzaf askerlik ödevi dışında …", sira=1)


def test_answer_kaynaklari_ve_atiflari_dondurur(monkeypatch):
    monkeypatch.setattr(servis, "_getir", lambda soru, k: (IS_K_31,))
    monkeypatch.setattr(servis, "_uret",
                        lambda mesajlar: ("İş Kanunu Madde 31 uyarınca askıya alınır.", "stop"))
    c = servis.answer("Askerlik nedeniyle iş sözleşmesi ne olur?")
    assert c.durum is Durum.CEVAP
    assert c.kaynaklar == (IS_K_31,)
    assert any(a.dogrulandi for a in c.atiflar)


def test_answer_bos_getirmede_susar(monkeypatch):
    """Retriever boş dönerse model konuşturulmaz — üründe M5 koşulu OLUŞMAMALI."""
    monkeypatch.setattr(servis, "_getir", lambda soru, k: ())
    patladi = []
    monkeypatch.setattr(servis, "_uret",
                        lambda mesajlar: patladi.append(1) or ("olmamalı", "stop"))
    c = servis.answer("İlgisiz soru")
    assert c.durum is Durum.SUSKUNLUK
    assert c.kaynaklar == ()
    assert not patladi, "🚨 kaynaksız soruda model ÇAĞRILDI — üründe M5 koşulu oluştu"


def test_answer_kesigi_gizlemez(monkeypatch):
    monkeypatch.setattr(servis, "_getir", lambda soru, k: (IS_K_31,))
    monkeypatch.setattr(servis, "_uret", lambda mesajlar: ("Yarım cüm", "length"))
    assert servis.answer("x").durum is Durum.KESIK
