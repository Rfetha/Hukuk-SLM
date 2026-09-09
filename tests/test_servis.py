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


# ── Araç katmanı — çok adımlı mod (Görev 18 · ADR-0076) ──────────────────────
# ⛔ Bu testlerin hiçbiri sunucu, indeks ya da ağ istemez.

class _SahteAraclar:
    """`ara` çağrıldığını kaydeder; başka araç kullanılmaz."""

    def __init__(self, sonuc=(IS_K_31,)):
        self.cagrildi = []
        self._sonuc = sonuc

    def ara(self, sorgu, k=10):
        self.cagrildi.append((sorgu, k))
        return self._sonuc


def _uret_dizisi(*adimlar):
    """Her çağrıda sıradaki `(metin, finish, arac_cagrilari)` üçlüsünü döndürür."""
    kalan = list(adimlar)

    def uret(mesajlar, semalar=None):
        return kalan.pop(0) if kalan else ("", "stop", ())
    return uret


def test_arac_dongusu_SINIRA_dayaninca_ARAMA_TUKENDI(monkeypatch):
    """⛔ Sınır GÖRÜNÜR olmalı (ADR-0076). Model sonsuza kadar arayamaz ve sınıra
    dayandığında vatandaşa sessizce yarım dayanaklı bir cevap teslim EDİLMEZ."""
    monkeypatch.setattr(servis, "_getir", lambda soru, k: (IS_K_31,))
    a = _SahteAraclar()
    hep_arar = lambda mesajlar, semalar=None: ("", "stop", ({"ad": "ara", "arg": {"sorgu": "x"}},))
    c = servis.answer_arac("x", araclar=a, uret=hep_arar, azami_adim=3)
    assert c.durum is Durum.ARAMA_TUKENDI
    assert len(a.cagrildi) == 3, "döngü sınırı uygulanmadı"


def test_ARAMA_TUKENDI_KESIK_DEGILDIR(monkeypatch):
    """İkisi vatandaşa farklı şey söyler; birleştirilmeleri sınırı görünmez kılardı."""
    monkeypatch.setattr(servis, "_getir", lambda soru, k: (IS_K_31,))
    hep_arar = lambda mesajlar, semalar=None: ("", "stop", ({"ad": "ara", "arg": {"sorgu": "x"}},))
    c = servis.answer_arac("x", araclar=_SahteAraclar(), uret=hep_arar, azami_adim=1)
    assert c.durum is Durum.ARAMA_TUKENDI and c.durum is not Durum.KESIK


def test_KAPILAR_arac_hic_cagrilmasa_da_calisir(monkeypatch):
    """🔒 KAPI ↔ KALDIRAÇ (ADR-0076): atıf doğrulama ve durum sınıflandırma döngünün
    DIŞINDA, koşulsuz çalışır. Uydurma madde 0/114 garantisi buradan geliyor."""
    monkeypatch.setattr(servis, "_getir", lambda soru, k: (IS_K_31,))
    a = _SahteAraclar()
    uret = _uret_dizisi(("İş Kanunu Madde 31 uyarınca askıya alınır.", "stop", ()))
    c = servis.answer_arac("x", araclar=a, uret=uret)
    assert a.cagrildi == [], "araç çağrılmadı, doğru"
    assert c.durum is Durum.CEVAP
    assert any(x.dogrulandi for x in c.atiflar), "🚨 KAPI atlandı — atıf doğrulanmadı"


def test_arac_sonuclari_KAYNAKLARA_eklenir(monkeypatch):
    """Vatandaş, cevabın hangi maddelere dayandığını görmeli — araçla gelen de dahil."""
    ek = Kaynak(kanun_adi="İŞ KANUNU", kanun_no="4857", madde_no="Madde 21",
                metin="İşe iade.", sira=1)
    monkeypatch.setattr(servis, "_getir", lambda soru, k: (IS_K_31,))
    uret = _uret_dizisi(
        ("", "stop", ({"ad": "ara", "arg": {"sorgu": "işe iade"}},)),
        ("İş Kanunu Madde 21 uyarınca başvurulur.", "stop", ()))
    c = servis.answer_arac("x", araclar=_SahteAraclar((ek,)), uret=uret)
    assert c.durum is Durum.CEVAP
    kimlikler = {s.kimlik for s in c.kaynaklar}
    assert IS_K_31.kimlik in kimlikler and ek.kimlik in kimlikler


def test_araclı_yol_KESIGI_de_gizlemez(monkeypatch):
    monkeypatch.setattr(servis, "_getir", lambda soru, k: (IS_K_31,))
    uret = _uret_dizisi(("Yarım cüm", "length", ()))
    assert servis.answer_arac("x", araclar=_SahteAraclar(), uret=uret).durum is Durum.KESIK
