"""suskunluk_terazisi ürün yüzeyinin kapı testleri (plan Görev 7).

Vakalar UYDURULMADI — hepsi Faz 0'da gözle okunmuş gerçek kalemler.
"""
from hakhukuk.terazi import siniflandir
from hakhukuk.tipler import Durum, Kaynak

IS_K_31 = Kaynak(kanun_adi="İŞ KANUNU", kanun_no="4857", madde_no="Madde 31",
                 metin="Muvazzaf askerlik ödevi dışında manevra veya herhangi bir "
                       "sebeple silâh altına alınan …", sira=1)


def test_olumsuz_hukum_kaynak_VARKEN_cevaptir_cekinme_degildir():
    """2026-09-07 · GERÇEK vaka (BİZ id=37): alet bunu çekinme saydı, göz CEVAP dedi.

    "…zorunlu bir şart bulunmamaktadır" bir HUKUKİ HÜKÜMDÜR, red değil.
    """
    metin = ("Vesayet altındaki bir kişi için aile meclisinin kurulmasının zorunlu bir "
             "şartı bulunmamaktadır. Vesayet, mahkeme kararıyla atanır. "
             "**İlgili Kanun:** Türk Medeni Kanunu, 503. madde.")
    durum, atiflar = siniflandir(metin, kaynaklar=(IS_K_31,), finish_reason="stop")
    assert durum is not Durum.SUSKUNLUK


def test_kaynak_YOKKEN_ayni_metin_suskunluk_sayilabilir():
    """Aynı metin, kaynak yokken: "kaynakta yok" okuması artık MÜMKÜN."""
    metin = "Bu konuda elimdeki kaynaklarda bir hüküm bulunmamaktadır."
    durum, _ = siniflandir(metin, kaynaklar=(), finish_reason="stop")
    assert durum is Durum.SUSKUNLUK


def test_kesik_cevap_gizlenmez():
    """Faz 0 · id 43: yarım cümle sessizce teslim edilmez."""
    durum, _ = siniflandir("İddianame, Cumhuriyet Başsavcılığı tarafından mahkemeye "
                           "sunulur ve mahkeme tarafından kabul edilirse",
                           kaynaklar=(IS_K_31,), finish_reason="length")
    assert durum is Durum.KESIK


def test_uydurulmus_atif_dogrulanmadi_isaretlenir():
    """Faz 0 · base id=16: "4711 Sayılı Türk Hakemlik Kanunu" — var olmayan kanun."""
    metin = "Karşı oy yer almaz. 4711 Sayılı Türk Hakemlik Kanunu'nun 33. maddesi."
    _, atiflar = siniflandir(metin, kaynaklar=(IS_K_31,), finish_reason="stop")
    assert atiflar, "atıf çıkarılamadı"
    assert all(not a.dogrulandi for a in atiflar), "getirilen kaynakta olmayan atıf doğrulanmış"


def test_kaynaktaki_atif_dogrulanir():
    metin = "İş Kanunu Madde 31 uyarınca sözleşme askıya alınır."
    _, atiflar = siniflandir(metin, kaynaklar=(IS_K_31,), finish_reason="stop")
    assert any(a.dogrulandi for a in atiflar)
