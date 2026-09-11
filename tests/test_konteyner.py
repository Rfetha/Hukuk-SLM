"""Görev 20 — konteyner dağıtımının kapı testleri ([ADR-0078](../docs/adr/0078-konteyner-dagitimi-rejim-kilidi.md)).

⛔ **Docker GEREKMEZ ve ÇAĞRILMAZ.** `compose.yaml` bir metin dosyası olarak değil, YAML
olarak **ayrıştırılır**; `indir.py` kapısı ağa çıkmadan, indirme monkeypatch'lenerek sınanır.

⚠️ Niçin metin araması YASAK: `grep "cache-type-k" compose.yaml` bayrağın **doğru servise**,
**doğru değerle** geçtiğini kanıtlamaz — bir yorum satırında, yanlış kutuda ya da değeri
düşmüş hâlde de eşleşir. Bu hattın hata sınıfı tam olarak budur: bayrak sessizce düşer, koşu
hata vermeden yanlış sayı üretir (`docs/record/yurutme-tuzaklari.md` birinci madde).

⚠️ `yaml` bir KAPI şartıdır, `importorskip` ile atlanmaz: atlanan test kapı değildir.
`PyYAML==6.0.3` `requirements.lock.txt`'te pinli ve kurulu ortamdan okundu (2026-09-11).
"""
import hashlib
import pathlib
import re

import pytest
import yaml

KOK = pathlib.Path(__file__).resolve().parent.parent

# ── Ölçüm rejiminin BAĞLAYICI bayrakları (ADR-0078 madde 1 · MODEL_CARD §7.10).
# Ticket 2 ölçtü: yalnız KV önbelleğinin kuantizasyonu değişince (q8_0 ↔ fp16) aynı soruda
# cevap DEĞİŞTİ. Bunlar tercih değil, cevabı belirleyen ayarlardır.
# ⚠️ `--host` bilerek burada DEĞİL: tek izinli sapma aşağıda ayrıca sınanır.
KANONIK_DEGERLI = {
    "-ngl": "99",
    "-fa": "on",
    "--cache-type-k": "q8_0",
    "--cache-type-v": "q8_0",
    "-c": "8192",
    "--port": "8080",
    # ⚠️ Üretimin bağlayıcı komutunda YOKTU; 2026-09-11'de insan kararıyla AÇIKÇA pinlendi
    # (açık kusur 20). Ürün yolunun iki geçişli zorunlu kapatması (ADR-0080)
    # `message.reasoning_content` alanına bağımlı; varsayılan `auto` başka bir biçime
    # çözülürse mekanizma SESSİZCE tek geçişe düşer ve boş cevap kusuru geri gelir.
    # Rejim DEĞİŞMEDİ: `auto` ≡ `deepseek` olduğu koşan sunucuya doğrudan istekle ÖLÇÜLDÜ.
    "--reasoning-format": "deepseek",
}
KANONIK_DEGERSIZ = ("--no-context-shift",)


@pytest.fixture(scope="module")
def compose() -> dict:
    return yaml.safe_load((KOK / "compose.yaml").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def indir():
    """Gecikmeli içe alma: modül yoksa test ADIYLA kırmızı düşsün, toplama çökmesin."""
    from hakhukuk import indir as modul
    return modul


def _bayraklar(komut: list[str]) -> dict[str, str | None]:
    """`["-ngl", "99", "--no-context-shift"]` → `{"-ngl": "99", "--no-context-shift": None}`.

    ⚠️ Değersiz bayrak `None` ile durur: *"bayrak var"* ile *"bayrağın değeri şu"* ayrı
    şeylerdir ve ikisi ayrı ayrı çivilenir.
    """
    esleme: dict[str, str | None] = {}
    for i, jeton in enumerate(komut):
        if not jeton.startswith("-"):
            continue
        sonraki = komut[i + 1] if i + 1 < len(komut) else None
        esleme[jeton] = None if sonraki is None or sonraki.startswith("-") else sonraki
    return esleme


# ── (a) kanonik bayrak kümesi BİREBİR ────────────────────────────────────────────────────

def test_llama_komutu_kanonik_bayraklari_birebir_tasiyor(compose):
    bayrak = _bayraklar(compose["services"]["llama"]["command"])
    for ad, deger in KANONIK_DEGERLI.items():
        assert bayrak.get(ad) == deger, f"{ad} bayrağı {bayrak.get(ad)!r}, beklenen {deger!r}"
    for ad in KANONIK_DEGERSIZ:
        assert ad in bayrak, f"{ad} bayrağı DÜŞMÜŞ"
        assert bayrak[ad] is None, f"{ad} değersiz bayraktır, {bayrak[ad]!r} almış"


def test_llama_model_yolu_volumedeki_gguf_dosyasini_gosteriyor(compose, indir):
    """Model yolu imajın içini değil, `indir` kutusunun yazdığı volume'ü göstermeli."""
    llama = compose["services"]["llama"]
    yol = _bayraklar(llama["command"])["-m"]
    bagli = [b.split(":")[1] for b in llama["volumes"]]
    assert any(yol.startswith(hedef.rstrip("/") + "/") for hedef in bagli), \
        f"-m {yol} bağlı volume'lerin ({bagli}) hiçbirinin altında değil"
    assert yol.endswith(indir.GGUF_DOSYA)


# ── (b) tek izinli sapma + erişim yüzeyi — İKİSİ BİRLİKTE ────────────────────────────────

def test_llama_host_sapmasi_var_ve_yayin_yalniz_yerele(compose):
    """⚠️ Bu iki hüküm AYRILMAZ: biri olmadan diğeri tehlikelidir.

    `--host 0.0.0.0` konteyner içinde zorunludur (`127.0.0.1` komşu kutudan erişilemez),
    ama erişim yüzeyi `ports` ile host'un `127.0.0.1`'ine kısıtlı KALMALIDIR — aksi hâlde
    sunucu ağa açılır ve S9 (barındırma/mahremiyet) sessizce açılmış olur.
    """
    llama = compose["services"]["llama"]
    assert _bayraklar(llama["command"])["--host"] == "0.0.0.0"
    assert llama["ports"] == ["127.0.0.1:8080:8080"]


# ── (c) indirme bir KAPIdır: tutmazsa erken çıkar, hedefe HİÇBİR ŞEY bırakmaz ────────────

@pytest.fixture
def sahte_inis(monkeypatch, indir):
    """`_hf_indir`'i ağsız bir sahteyle değiştirir; inen baytları çağıran seçer."""
    def kur(icerik: bytes):
        def sahte(depo, dosya, revizyon, dizin):
            yol = pathlib.Path(dizin) / dosya
            yol.write_bytes(icerik)
            return yol
        monkeypatch.setattr(indir, "_hf_indir", sahte)
    return kur


def test_indir_yanlis_sha256_karsisinda_erken_cikiyor(tmp_path, monkeypatch, indir, sahte_inis):
    """Bayt sayısı tutan ama içeriği BAŞKA olan dosya — kapı yalnız boyuta bakamaz."""
    icerik = b"bu dogru artefakt DEGIL"
    sahte_inis(icerik)
    monkeypatch.setattr(indir, "GGUF_BAYT", len(icerik))       # bayt kapısı GEÇSİN
    with pytest.raises(indir.KimlikHatasi):
        indir.indir_model(tmp_path)
    assert list(tmp_path.iterdir()) == [], "kapı tutmadı ama hedefte artık var"


def test_indir_yanlis_bayt_sayisi_karsisinda_erken_cikiyor(tmp_path, monkeypatch, indir,
                                                           sahte_inis):
    """Bayt kapısı `sha256`'dan BAĞIMSIZ tutmalı: özet doğru olsa bile boyut yanlışsa durur."""
    icerik = b"kisa"
    sahte_inis(icerik)
    monkeypatch.setattr(indir, "GGUF_SHA256", hashlib.sha256(icerik).hexdigest())
    with pytest.raises(indir.KimlikHatasi):
        indir.indir_model(tmp_path)
    assert list(tmp_path.iterdir()) == []


def test_indir_kapi_tutmazsa_cikis_kodu_sifirdan_farkli(tmp_path, indir, sahte_inis, capsys):
    """Compose bağı çıkış koduna bakar: `indir` patlarsa iki daemon da HİÇ başlamaz."""
    sahte_inis(b"yanlis artefakt")
    assert indir.main([str(tmp_path)]) != 0
    assert list(tmp_path.iterdir()) == []


def test_indir_kapi_tutunca_artefakti_hedefe_tasiyor(tmp_path, monkeypatch, indir, sahte_inis):
    """Mutlu yol: dosya hedefe taşınır ve geçici hiçbir kalıntı kalmaz."""
    icerik = b"dogru artefakt oldugunu varsaydigimiz baytlar"
    sahte_inis(icerik)
    monkeypatch.setattr(indir, "GGUF_BAYT", len(icerik))
    monkeypatch.setattr(indir, "GGUF_SHA256", hashlib.sha256(icerik).hexdigest())
    yol = indir.indir_model(tmp_path)
    assert yol.read_bytes() == icerik
    assert [y.name for y in tmp_path.iterdir()] == [indir.GGUF_DOSYA]


# ── (d) revizyon PİNLİ — `latest` yasak ──────────────────────────────────────────────────

def test_pinlenmis_revizyon_latest_degil_ve_tam_commit_sha(indir):
    """*"En güncel modeli çek"* bu hattın hata sınıfıdır: yayımlanan sayı BELİRLİ bir
    dosyanındır (`kollar.md` 2026-09-09). Dal adı da yetmez — dal ilerler."""
    assert indir.GGUF_REVIZYON != "latest"
    assert re.fullmatch(r"[0-9a-f]{40}", indir.GGUF_REVIZYON), \
        f"revizyon 40 karakterlik commit sha'sı değil: {indir.GGUF_REVIZYON!r}"


def test_compose_imajlari_pinli(compose):
    """Aynı kuralın imaj tarafı: etiketsiz ya da `latest` imaj sessizce başka bir ikili çeker."""
    for ad, servis in compose["services"].items():
        if "image" not in servis:
            continue
        etiket = servis["image"].rsplit(":", 1)
        assert len(etiket) == 2 and etiket[1] != "latest", \
            f"{ad} servisinin imajı pinli değil: {servis['image']}"


# ── (e) app kutusu: llama'ya yönelir, yalnız yerele yayımlar ─────────────────────────────

def test_app_llama_kutusuna_yoneliyor_ve_yalniz_yerele_yayimliyor(compose):
    app = compose["services"]["app"]
    assert app["environment"]["HAKHUKUK_SUNUCU"] == "http://llama:8080/v1"
    assert app["ports"] == ["127.0.0.1:8000:8000"]


# ── (f) indirme başarısızsa İKİ daemon da hiç başlamaz ───────────────────────────────────

@pytest.mark.parametrize("daemon", ["llama", "app"])
def test_daemonlar_indir_kapisina_bagli(compose, daemon):
    bag = compose["services"][daemon]["depends_on"]["indir"]
    assert bag["condition"] == "service_completed_successfully"
