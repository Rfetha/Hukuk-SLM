"""Görev 21 — kusur 3·4·5b·8·12a·13 kapı testleri (+ inceleme bulguları B1·B2·B3·B6).

⚠️ Bu dosya KIRMIZI doğdu (Adım 1: üretim kodu henüz değişmemişti) ve artık KAPANIŞ hâlini
anlatır: kusurlar kapatıldı, testler YEŞİL ve bundan sonra REGRESYON KAPISIdır — biri
kapanan bir kusuru geri getirirse burası kırmızıya döner. Kırmızı hâlin kaydı commit
mesajlarındadır (`d75b5c5` ve inceleme düzeltme turu). İki test grubu hiç kırmızı olmadı ve
bilerek öyle: "ölçüm hattı dokunulmazlık kapısı" (henüz kırılmamış bir şeyi ÇİVİLİYOR) ve
"kısa-ama-dolu sorgu reddedilmiyor" (uydurulmuş bir eşik EKLENMEDİĞİNİ garanti eden muhafız).

Hiçbir test retriever/llama-server/korpus yüklemez — monkeypatch ve sahte nesne kullanılır.
"""
import inspect
import json
import pathlib
import re

from hakhukuk import cli, servis, tipler, tui
from hakhukuk.tipler import Cevap, Durum, Kaynak

REPO_KOK = pathlib.Path(__file__).resolve().parent.parent

IS_K_31 = Kaynak(kanun_adi="İŞ KANUNU", kanun_no="4857", madde_no="Madde 31",
                 metin="Muvazzaf askerlik ödevi dışında …", sira=1)


# ── kusur 4 — boş sorgu KAPISI `servis.answer`/`servis.answer_arac`'a konur ──────────

def _patlayan_getir():
    """`_getir` çağrılırsa test'i düşürecek sahte — boş sorgu KAPI'yı geçmemeli."""
    cagrildi = []

    def getir(soru, k):
        cagrildi.append(soru)
        raise AssertionError(f"boş/boşluk sorgu ({soru!r}) _getir'e ULAŞTI")
    return getir, cagrildi


def test_answer_bos_sorgu_getire_ulasmiyor(monkeypatch):
    getir, cagrildi = _patlayan_getir()
    monkeypatch.setattr(servis, "_getir", getir)
    c = servis.answer("")
    assert not cagrildi, "boş sorgu _getir'e ulaştı"
    assert isinstance(c, Cevap) and c.metin.strip(), "boş sorguda okunur bir mesaj yok"


def test_answer_bosluk_sorgu_getire_ulasmiyor(monkeypatch):
    getir, cagrildi = _patlayan_getir()
    monkeypatch.setattr(servis, "_getir", getir)
    c = servis.answer("   ")
    assert not cagrildi, "yalnız boşluktan ibaret sorgu _getir'e ulaştı"
    assert isinstance(c, Cevap) and c.metin.strip(), "boşluk sorgusunda okunur bir mesaj yok"


def test_answer_arac_bos_sorgu_getire_ulasmiyor(monkeypatch):
    """`answer_arac` aynı kapıdan geçmeli — ayrı yol, ayrı savunmasızlık olmasın."""
    getir, cagrildi = _patlayan_getir()
    monkeypatch.setattr(servis, "_getir", getir)
    # araclar= verilmeden çağrılırsa _varsayilan_araclar() ağır korpusu yükler; kapı
    # _getir'den ÖNCE tetiklenmeliyse zaten oraya hiç gerek kalmaz, ama testi ağır
    # bağımlılıktan bağımsız tutmak için sahte bir nesne veriyoruz.
    c = servis.answer_arac("   ", araclar=object())
    assert not cagrildi, "boşluk sorgu answer_arac üzerinden _getir'e ulaştı"
    assert isinstance(c, Cevap) and c.metin.strip(), "answer_arac boşluk sorgusunda okunur mesaj yok"


def test_answer_kisa_dolu_sorgu_reddedilmiyor(monkeypatch):
    """Uydurulmuş uzunluk eşiği YOK: "kira?" gibi kısa ama dolu bir soru _getir'e ulaşmalı.

    Bu, kapı henüz eklenmeden de bugün zaten doğru (muhafız testi) — kapı eklendikten
    sonra da BOZULMAMASI gereken davranış budur.
    """
    cagrildi = []
    monkeypatch.setattr(servis, "_getir", lambda soru, k: cagrildi.append(soru) or ())
    servis.answer("kira?")
    assert cagrildi == ["kira?"], "kısa ama dolu bir soru _getir'e ulaşmadı — uydurulmuş eşik var"


# ── kusur 12a — `bicimle()`'de iskele işareti süzgeci; `Cevap.metin` HAM kalır ───────

def test_bicimle_iskele_isaretlerini_temizler_alinti_metni_kalir():
    ham = "Bu konuda ##begin_quote##ilgili kanun hükmü##end_quote## uygulanır."
    c = Cevap(metin=ham, durum=Durum.CEVAP, atiflar=(), kaynaklar=())
    sunum = cli.bicimle(c)
    assert "##begin_quote##" not in sunum, "sunumda iskele işareti kaldı"
    assert "##end_quote##" not in sunum, "sunumda iskele işareti kaldı"
    assert "ilgili kanun hükmü" in sunum, "işaretlerle birlikte alıntı metni de silindi"


def test_cevap_metin_ham_alan_isaretleri_koruyor():
    """`Cevap.metin` modelin ham çıktısıdır — `bicimle()` onu MUTASYONA UĞRATMAZ."""
    ham = "Bu konuda ##begin_quote##ilgili kanun hükmü##end_quote## uygulanır."
    c = Cevap(metin=ham, durum=Durum.CEVAP, atiflar=(), kaynaklar=())
    cli.bicimle(c)  # yan etkisi olmamalı
    assert c.metin == ham, "Cevap.metin bicimle() çağrısından sonra değişti — ham kayıt bozuldu"


# ── ölçüm hattı DOKUNULMAZLIK KAPISI — kusur 12a'nın çözümü scripts/'e SIZMAMALI ─────

def test_score_register_begin_quote_deseni_yerinde_duruyor():
    """`##begin_quote##` `score_register.py`'de register göstergesi olarak SAYILIYOR
    (CLAUDE.md karar 2). Bu desen silinirse register ölçümü bozulur."""
    dosya = REPO_KOK / "scripts" / "puanlama" / "score_register.py"
    icerik = dosya.read_text(encoding="utf-8")
    assert "##begin_quote##" in icerik, (
        "score_register.py'deki begin_quote deseni kayboldu — register ölçümü bozulur")


def test_scripts_altinda_begin_quote_temizleme_suzgeci_yok():
    """kusur 12a'nın süzgeci YALNIZ `cli.bicimle()`'de olmalı; `scripts/` ölçüm hattına
    hiçbir zaman bir begin_quote/end_quote STRIP işlemi sızmamalı."""
    desen = re.compile(
        r'(replace|sub)\(\s*[rRuU]?["\'][^"\']*(begin_quote|end_quote)[^"\']*["\']\s*,\s*'
        r'[rRuU]?["\']{2}', re.IGNORECASE)
    supheli = []
    for dosya in (REPO_KOK / "scripts").rglob("*.py"):
        icerik = dosya.read_text(encoding="utf-8")
        if desen.search(icerik):
            supheli.append(str(dosya.relative_to(REPO_KOK)))
    assert not supheli, f"scripts/ altında begin_quote SÜZGECİ bulundu: {supheli}"


# ── kusur 13 — `madde_sayisi` türetilmiş alanı; ham `madde_no` KORUNUR ───────────────

def test_madde_sayisi_uc_farkli_yazimi_ayni_degere_indirger():
    atif = tipler.Atif(kanun_no="6098", madde_no="Madde 330")
    k_buyuk = tipler.Kaynak(kanun_adi="x", kanun_no="6098", madde_no="MADDE 330",
                            metin="", sira=1)
    k_ciplak = tipler.Kaynak(kanun_adi="x", kanun_no="6098", madde_no="330",
                             metin="", sira=1)
    assert atif.madde_sayisi == 330
    assert k_buyuk.madde_sayisi == 330
    assert k_ciplak.madde_sayisi == 330


def test_madde_sayisi_turetilirken_ham_madde_no_bozulmuyor():
    atif = tipler.Atif(kanun_no="6098", madde_no="Madde 330")
    k = tipler.Kaynak(kanun_adi="x", kanun_no="6098", madde_no="MADDE 330", metin="", sira=1)
    _ = atif.madde_sayisi, k.madde_sayisi
    assert atif.madde_no == "Madde 330", "ham madde_no normalizasyonla ezildi"
    assert k.madde_no == "MADDE 330", "ham madde_no normalizasyonla ezildi"


# ── kusur 3 — TUI: `answer()` olay döngüsünde DOĞRUDAN çağrılmıyor ───────────────────

def test_tui_answer_dogrudan_olay_dongusunde_cagrilmiyor():
    """`on_input_submitted` senkron olay döngüsü metodudur; içinde `answer(` doğrudan
    çağrılırsa ağ + retriever I/O arayüzü DONDURUR."""
    kaynak = inspect.getsource(tui.HakHukukTUI.on_input_submitted)
    assert "answer(" not in kaynak, (
        "answer() doğrudan on_input_submitted içinde çağrılıyor — arayüz donar")


def test_tui_answer_calisan_ipliginde_calistiriliyor():
    """answer() bir yerde `@work(thread=True)` ya da `run_worker(..., thread=True)` ile
    çalışan iş parçacığına alınmış olmalı."""
    tum_kaynak = inspect.getsource(tui)
    assert "answer(" in tum_kaynak, "answer() TUI'den tamamen kayboldu"
    isaretli = ("@work(thread=True)" in tum_kaynak
               or ("run_worker(" in tum_kaynak and "thread=True" in tum_kaynak))
    assert isaretli, "answer() çalışan iş parçacığına (worker) alınmamış"


# ── kusur 8 + 5b — açılış yönergesi + STATİK kapsam satırı (KUNYE.json'dan okunur) ───

def test_tui_kapsam_satiri_kunyeden_sayilari_okuyor():
    """Sayılar `data/corpus/KUNYE.json`'dan okunmalı, koda gömülmemeli."""
    kunye = json.loads((REPO_KOK / "data/corpus/KUNYE.json").read_text(encoding="utf-8"))
    satir = tui.kapsam_satiri()
    assert isinstance(satir, str) and satir.strip()
    n_kanun, n_madde = kunye["n_kanun"], kunye["n_madde"]
    n_madde_bicimli = f"{n_madde:,}".replace(",", ".")
    assert str(n_kanun) in satir, "kapsam satırında kanun sayısı yok"
    assert str(n_madde) in satir or n_madde_bicimli in satir, "kapsam satırında madde sayısı yok"
    for kapsam_disi in ("yönetmelik", "tüzük", "khk", "tebliğ"):
        assert kapsam_disi in satir.lower(), f"kapsam dışı tür anılmıyor: {kapsam_disi}"


def test_tui_kapsam_satiri_sayilari_koda_gommez():
    """Kod, KUNYE.json'daki güncel sayıları OKUMALI — kendi kopyasını GÖMMEMELİ."""
    kaynak = inspect.getsource(tui)
    kunye = json.loads((REPO_KOK / "data/corpus/KUNYE.json").read_text(encoding="utf-8"))
    n_madde_bicimli = f"{kunye['n_madde']:,}".replace(",", ".")
    assert str(kunye["n_kanun"]) not in kaynak, "kanun sayısı koda gömülmüş"
    assert str(kunye["n_madde"]) not in kaynak and n_madde_bicimli not in kaynak, (
        "madde sayısı koda gömülmüş")


def test_tui_acilis_ekrani_yonerge_ve_kapsam_satirini_gosteriyor():
    """Açılış ekranı BOŞ değil: `compose()` hem yönerge hem statik kapsam satırını
    üretmeli. Sınıflandırıcı YOK — kapsam her zaman aynı statik satırdır (karar 3)."""
    kaynak = inspect.getsource(tui.HakHukukTUI.compose)
    assert "kapsam_satiri(" in kaynak, "açılış ekranı statik kapsam satırını göstermiyor"


# ── kusur: TUI sunumu `c.metin`'i HAM basıyor — iskele işareti vatandaşa gidiyor ─────

def test_tui_suzgeci_cli_ile_AYNI_nesne():
    """`tui.py` süzgeci `cli.py`'den İMPORT etmeli, KOPYALAMAMALI (S18'in dersi:
    `SORUMLULUK_IBARESI` bu deponun yerleşik emsalidir — `is` ile sınanır)."""
    assert tui.alinti_isaretlerini_tirnaga_cevir is cli.alinti_isaretlerini_tirnaga_cevir, (
        "tui'nin süzgeci cli'dekiyle AYNI nesne değil — kopyalanmış olabilir")


def test_tui_sunum_dizesinde_iskele_isareti_yok(monkeypatch):
    """`tui.py` kendi sunum dizesini kuruyor (`bicimle()` çağırmıyor); süzgeci `cli`'den
    IMPORT ettiği için ##begin_quote##/##end_quote## vatandaşa GİTMEZ — bu test o yolu
    kapalı tutar. `servis.answer` sahtelenir; llama-server/indeks GEREKMEZ."""
    import asyncio

    from textual.widgets import Static

    ham = "Bu konuda ##begin_quote##ilgili kanun hükmü##end_quote## uygulanır."
    sahte_cevap = Cevap(metin=ham, durum=Durum.CEVAP, atiflar=(), kaynaklar=())
    monkeypatch.setattr(tui, "answer", lambda soru: sahte_cevap)

    async def _calistir() -> str:
        app = tui.HakHukukTUI()
        async with app.run_test() as pilot:
            await pilot.click("#soru")
            await pilot.press(*"soru", "enter")
            await app.workers.wait_for_complete()
            await pilot.pause()
            return str(app.query_one("#cikti", Static).content)

    cikti = asyncio.run(_calistir())
    assert "##begin_quote##" not in cikti, "TUI sunumunda iskele işareti kaldı"
    assert "##end_quote##" not in cikti, "TUI sunumunda iskele işareti kaldı"
    assert "ilgili kanun hükmü" in cikti, "işaretlerle birlikte alıntı metni de silindi"


# ══ inceleme bulguları (kod incelemesi, 2026-09-11) ══════════════════════════════════

# ── B1 — TUI'de eşzamanlı iki çalışan: "son biten kazanır" ekranda YANLIŞ eşleşme üretir ─

def test_tui_kosu_surerken_ikinci_sorgu_calisan_baslatmiyor(monkeypatch):
    """İki ardışık Enter → İKİ çalışan; yavaş biten 1. soruysa ekranda 2. sorunun altında
    1. sorunun cevabı görünür ve hiçbir hata çıkmaz ("hata vermeden yanlış").

    Kapatma: koşu sürerken girdi DEVRE DIŞI + çalışan `exclusive`.
    """
    import threading

    kapi = threading.Event()
    cagrilar = []

    def yavas_answer(soru):
        cagrilar.append(soru)
        kapi.wait(timeout=5)
        return Cevap(metin=f"cevap:{soru}", durum=Durum.CEVAP, atiflar=(), kaynaklar=())

    import asyncio

    from textual.widgets import Input, Static

    monkeypatch.setattr(tui, "answer", yavas_answer)

    async def _calistir():
        app = tui.HakHukukTUI()
        async with app.run_test() as pilot:
            await pilot.click("#soru")
            await pilot.press(*"bir", "enter")
            await pilot.pause()
            await pilot.press(*"iki", "enter")   # koşu SÜRERKEN — yok sayılmalı
            await pilot.pause()
            kapi.set()
            await app.workers.wait_for_complete()
            await pilot.pause()
            return (str(app.query_one("#cikti", Static).content),
                    app.query_one("#soru", Input).disabled)

    try:
        cikti, girdi_kapali = asyncio.run(_calistir())
    finally:
        kapi.set()

    assert cagrilar == ["bir"], (
        f"koşu sürerken ikinci sorgu da başladı — iki çalışan yarışıyor: {cagrilar}")
    assert "cevap:bir" in cikti, "ekranda koşan sorunun cevabı yok"
    assert not girdi_kapali, "koşu bitti ama girdi kapalı kaldı — arayüz kilitli"


def test_tui_hata_yolunda_girdi_tekrar_aciliyor(monkeypatch):
    """`answer()` patlarsa girdi AÇILMALI — yoksa llama-server kapalıyken arayüz
    tek bir hatadan sonra kalıcı olarak kilitlenir."""
    import asyncio

    from textual.widgets import Input

    def patlayan_answer(soru):
        raise RuntimeError("llama-server kapalı")

    monkeypatch.setattr(tui, "answer", patlayan_answer)

    async def _calistir():
        app = tui.HakHukukTUI()
        async with app.run_test() as pilot:
            await pilot.click("#soru")
            await pilot.press(*"soru", "enter")
            await app.workers.wait_for_complete()
            await pilot.pause()
            return app.query_one("#soru", Input).disabled

    assert not asyncio.run(_calistir()), "hata yolunda girdi kapalı kaldı"


# ── B2 — kapsam satırı MÜLGA maddeleri "yürürlükteki" saymamalı ──────────────────────

def test_kapsam_satiri_mulgayi_duserek_yururlukteki_madde_sayisini_veriyor(monkeypatch, tmp_path):
    """`n_madde` TOPLAMdır; retriever varsayılanı mülgayı eler ⇒ vatandaşa gösterilecek
    sayı `n_madde - n_mulga`. Sayı künyeden TÜRETİLİR, koda gömülmez (sahte künye)."""
    sahte = tmp_path / "KUNYE.json"
    sahte.write_text(json.dumps(
        {"n_kanun": 3, "n_madde": 100, "n_mulga": 40, "anlik_goruntu_tarihi": "2026-01-01"}),
        encoding="utf-8")
    monkeypatch.setattr(cli, "_KUNYE_YOLU", sahte)
    satir = cli.kapsam_satiri()
    assert "yürürlükteki 60 madde" in satir, (
        f"yürürlükteki madde sayısı mülga düşülerek verilmiyor: {satir!r}")


def test_kapsam_satiri_tek_kaynak_tui_cli_ile_AYNI_nesne():
    """B4: metin `cli.py`'de tanımlı, `tui.py` IMPORT eder (SORUMLULUK_IBARESI emsali)."""
    assert tui.kapsam_satiri is cli.kapsam_satiri, (
        "tui'nin kapsam satırı cli'dekiyle AYNI nesne değil — kopyalanmış olabilir")


# ── B3 — `madde_sayisi` ÖNEKLİ biçimleri düz sayıya indirgememeli ────────────────────

def test_madde_sayisi_gecici_maddeyi_duz_maddeye_indirgemiyor():
    """`madde_anahtar.py`'nin önlemek için var olduğu SESSİZ hata: `Geçici Madde 1` ile
    `Madde 1` FARKLI maddelerdir; aynı değere inerlerse eşleşme şişer ve hata çıkmaz."""
    gecici = tipler.Atif(kanun_no="5237", madde_no="Geçici Madde 1")
    duz = tipler.Atif(kanun_no="5237", madde_no="Madde 1")
    assert duz.madde_sayisi == 1
    assert gecici.madde_sayisi != duz.madde_sayisi, (
        "Geçici Madde 1 ile Madde 1 aynı değere indi — yanlış maddeyi doğrular")


def test_madde_sayisi_ek_ve_mukerrer_onekli_biciminde_de_indirgemiyor():
    ek = tipler.Kaynak(kanun_adi="x", kanun_no="4857", madde_no="Ek Madde 1",
                       metin="", sira=1)
    mukerrer = tipler.Kaynak(kanun_adi="x", kanun_no="4857", madde_no="Mükerrer Madde 1",
                             metin="", sira=1)
    duz = tipler.Kaynak(kanun_adi="x", kanun_no="4857", madde_no="Madde 1",
                        metin="", sira=1)
    assert ek.madde_sayisi != duz.madde_sayisi, "Ek Madde 1 düz Madde 1'e indi"
    assert mukerrer.madde_sayisi != duz.madde_sayisi, "Mükerrer Madde 1 düz Madde 1'e indi"


# ── B6 — alıntı iskelesi SİLİNMEZ, tipografik tırnağa ÇEVRİLİR ───────────────────────

def test_alinti_isaretleri_tipografik_tirnaga_ceviriliyor():
    """İşaretin TAŞIDIĞI bilgi "burası kanunun kendi cümlesidir" sınırıdır; silinirse
    birebir kanun metni ile modelin yorumu ayırt edilemez hâle gelir."""
    sunum = cli.alinti_isaretlerini_tirnaga_cevir(
        "Kanun der ki: ##begin_quote##İşçi kıdem tazminatına hak kazanır.##end_quote## Ancak…")
    assert "“İşçi kıdem tazminatına hak kazanır.”" in sunum, f"alıntı sınırı kayboldu: {sunum!r}"
    assert "##" not in sunum, "iskele işareti sunuma sızdı"


def test_eslesmeyen_tek_alinti_isareti_siliniyor():
    """Eşleşmeyen tek işaret (model kapatmayı unutmuş) tırnak AÇMAZ — silinir."""
    sunum = cli.alinti_isaretlerini_tirnaga_cevir("Kanun der ki: ##begin_quote##İşçi …")
    assert "##" not in sunum, "eşleşmeyen iskele işareti sunumda kaldı"
    assert "İşçi" in sunum, "işaretle birlikte metin de silindi"
    assert "“" not in sunum and "”" not in sunum, "eşleşmeyen işaret için tırnak açıldı"


def test_alinti_cevirisi_ham_metni_bozmuyor():
    ham = "Bu konuda ##begin_quote##ilgili kanun hükmü##end_quote## uygulanır."
    c = Cevap(metin=ham, durum=Durum.CEVAP, atiflar=(), kaynaklar=())
    cli.bicimle(c)
    assert c.metin == ham, "Cevap.metin sunum çevirisinden sonra değişti — ham kayıt bozuldu"
