"""`exact_reject` — çekinme dedektörünün kalibrasyon davranışı.

Her test bir ÖLÇÜLMÜŞ yanlış sınıflandırmayı kilitliyor; hiçbiri varsayımsal değil.
Kaynak: G2 Adım 2.1 + 2.4b + 2.6 (2026-08-06), Gemini ailesi kalibrasyonu.
"""
import sys

import pytest

sys.path.insert(0, "scripts")
from score_abstention import exact_reject  # noqa: E402


# ── ADR-0058 açılış yeterlilik hükmü — kural İKİ KUTUPLU ────────────────────
# Ölçülen sapma iki yönlüydü: h1'de red=kötü (yanlış-pozitif rakibi kötü gösterir),
# h2b'de red=iyi (aynı hata rakibi iyi gösterir). Bu yüzden "muhafazakâr" savunması yok.

def test_exact_reject_olumlu_acilis_karsitlikla_cozulen_olumsuzlamaya_kanmaz():
    """YANLIŞ-POZİTİF kutbu — `h2b_fl35_k4` id=18'in GERÇEK metni.

    Olumsuzlama "ancak ... m.80 kapsamında yer almaktadır" ile ÇÖZÜLÜYOR: bu dolu bir
    cevap. Son esaslı ibare olumsuzlama değil, çözüm cümlesidir."""
    cevap = ("Verilen kaynaklar soruyu doğrudan cevaplamaktadır.  Verilen kaynaklarda zorla "
             "fuhşa sevketme fiilinin insanlığa karşı bir suç olarak düzenlendiğine dair bir "
             "ifade bulunmamaktadır; ancak bu fiil insan ticareti suçunu düzenleyen Türk Ceza "
             "Kanunu Madde 80 kapsamında yer almaktadır. (TÜRK CEZA KANUNU, Madde 80)")
    assert exact_reject(cevap, "data") is False


def test_exact_reject_olumlu_acilis_govdedeki_kaynak_yoklugu_beyanina_yenilir():
    """YANLIŞ-NEGATİF kutbu — `h2b_fl35_k4` id=5'in GERÇEK metni.

    Kural 334880d'de olumlu açılışı BAĞLAYICI saymıştı; bu, modelin kendi (yanlış) beyanını
    gerçek davranışının önüne koyuyordu. Cevap kendi açılışını cümle sonunda yalanlıyor."""
    cevap = ("Verilen kaynaklar soruyu cevaplamaktadır.   Verilen kaynaklarda bir çocuğu fuhşa "
             "teşvik eden kişiye verilecek cezayı doğrudan düzenleyen özel bir madde "
             "bulunmamaktadır. Bu nedenle verilen kaynaklarda bu konuyu düzenleyen yeterli "
             "madde bulunmuyor.")
    assert exact_reject(cevap, "data") is True


def test_exact_reject_son_esasli_ibare_salt_atif_parantezini_atlar():
    """`h2b_fl35_k4` id=76: cevap bir atıf paranteziyle bitiyor. Atıf hüküm taşımaz;
    son ibare sayılırsa gerçek sonuç (kaynak-yokluğu beyanı) görünmez olur."""
    cevap = ("Verilen kaynaklar soruyu cevaplamaktadır.  Verilen kaynaklarda borçlunun beyan "
             "yükümlülüğü düzenlenmiştir; ancak kaynaklarda borçlu ile başka birinin malı "
             "birlikte elinde bulundurması durumunda kimin mal sahibi sayılacağına dair bir "
             "düzenleme bulunmamaktadır.   (İCRA VE İFLAS KANUNU, Madde 85)")
    assert exact_reject(cevap, "data") is True


def test_exact_reject_olumsuz_yeterlilik_acilisi_red_sayilir():
    """Simetrinin öbür yarısı: bu kalıp REJECT_RE'nin HİÇBİR desenine uymuyordu,
    3 kalem sessizce 'cevapladı' sayılıyordu (h2b_fl35_k4'te 1)."""
    assert exact_reject("Verilen kaynaklar soruyu cevaplamamaktadır.", "data") is True
    assert exact_reject("Verilen kaynak metni soruyu cevaplamaz.", "data") is True


def test_exact_reject_acilis_hukmu_yoksa_govde_taranir():
    assert exact_reject("Verilen kaynaklarda bu konuyu düzenleyen madde bulunmuyor.",
                        "data") is True
    assert exact_reject("Mahkeme lehine karar verirse icra emri tebliğ edilir "
                        "(İİK m.32).", "data") is False


@pytest.mark.xfail(strict=True, reason=(
    "🔴 AÇIK BORÇ (kusur Ö-E, 2026-08-06). `_son_esasli_ibare` yalnız SON esaslı ibareye "
    "bakıyor; çekinme beyanı sonuç konumunda olup ARKASINDAN sonuç-dışı bir tavsiye cümlesi "
    "gelirse kural onu göremez. ÖLÇÜLDÜ ve kapatılmadı: tüm `outputs/eval`'da olumlu açılışlı "
    "96 cevabın **0'ı** bu şekle uyuyor (gövdede red + son ibarede red yok = 3 vaka, üçü de "
    "GERÇEKTEN dolu cevap; son ibaresi tavsiye/başvuru kalıbıyla biten 4 vaka, dördü de "
    "gerçekten dolu). Yani kuralı bugün onarmanın ölçülmüş bir dayanağı YOK ve körlemesine "
    "genişletmek yeni yanlış-pozitif üretir (ADR-0050 ruhu). Bu test kusuru KİLİTLEMEZ, "
    "SINIRI çizer: kural düzelirse strict=True ile PATLAR ve damga kaldırılmak zorunda kalır."))
def test_exact_reject_cekinme_sonrasi_tavsiye_kuyrugu_kacar():
    """Sınır vakası — kural bugün bunu 'cevapladı' sayıyor, oysa çekinmedir."""
    cevap = ("Verilen kaynaklar soruyu cevaplamaktadır. Kaynaklarda bu konu düzenlenmiyor. "
             "Bu konuda güncel mevzuata başvurmanız gerekir.")
    assert exact_reject(cevap, "data") is True


# ── Kanunun kendi KOŞUL kipi red değildir (#39'un `(?!sa)` ilkesi) ──────────

def test_exact_reject_kosul_kipi_red_sayilmaz():
    """Gemini bu iki kalıbı DOLU cevabın ortasında kullanıyordu; 998 ve 1904
    karakterlik tam cevaplar çekinme sayılıyordu."""
    assert exact_reject("ilamda belirtilen süre içinde (süre belirtilmemişse işin "
                        "mahiyetine göre belirlenen sürede) işin yapılması emredilir.",
                        "data") is False
    assert exact_reject("Yapı bölümleri mevcut değilse, hava hakkı kendiliğinden kat "
                        "irtifakına çevrilir (Kat Mülkiyeti Kanunu, Madde 52).",
                        "data") is False
    # #39'un asıl vakası korunuyor
    assert exact_reject("kanunda hüküm bulunmazsa hâkim karar verir.", "data") is False


def test_exact_reject_koşul_kipi_olmayan_olumsuzlama_red_kalir():
    """Daraltma fazla geniş olmasın: koşul eki YOKSA red tespiti sürmeli."""
    assert exact_reject("Bu konu kaynakta belirtilmemiştir.", "data") is True
    assert exact_reject("Bu bilgi mevcut değildir.", "data") is True
    assert exact_reject("Bu husus söz konusu değildir.", "data") is True


# ── Mod duyarlılığı (ADR-0044) korunuyor ───────────────────────────────────

def test_exact_reject_kor_modda_feragat_cumlesi_red_sayilmaz():
    cevap = ("Türk Ceza Kanunu'na göre ceza verilir. Güncel mevzuat için "
             "bir avukata danışmanızı öneririm.")
    assert exact_reject(cevap, "blind") is False
    assert exact_reject(cevap, "data") is True


# ── K3: payda (valid_trap) CEVAPTAN BAĞIMSIZ olmalı ─────────────────────────
# Ölçülen kusur: `judge()` soruyu, kaynağı ve CEVABI tek çağrıda veriyordu; aynı sınavda
# 80 kalemin 19'unda üç kol farklı `source_answers` alıyor, `valid_traps` 45/56/50 oluyordu.

def test_gecerlilik_anahtari_cevaptan_bagimsiz():
    """Anahtar yalnız (soru, kaynak) üzerinden — cevap girmiyor, giremez."""
    from score_abstention import gecerlilik_anahtari
    assert (gecerlilik_anahtari("Soru?", "KAYNAK metni")
            == gecerlilik_anahtari("Soru?", "KAYNAK metni"))
    assert (gecerlilik_anahtari("Soru?", "KAYNAK metni")
            != gecerlilik_anahtari("Soru?", "BAŞKA kaynak"))


def test_gecerlilik_anahtari_HAKEM_ISTEMINE_ESIT():
    """⭐ KARAR-4 m.1 (2026-08-06) — anahtar, hakemin GERÇEKTEN gördüğü metnin fonksiyonu.

    K-1 anahtarı TAM metne taşımıştı; ölçüm o onarımın **sayısal** karşılığı olmadığını
    gösterdi (15/15 aynı hüküm) ve bir gürültü yolu açtı: hakemin AYIRT EDEMEDİĞİ bir
    farka göre bölünen anahtar, *aynı istem → aynı cevap* değişmezini kırar. Ölçüldü:
    5.363 ayrı istemin **65'i** birden fazla anahtara düşüyor, **83** çağrı garanti
    gereksiz, ve aynı istem iki kayda dönerse `Rej*` ~1,5 p oynar (saf gürültü).

    Sınanan şey vekil DEĞİL: hakeme giden metin `hakem_kaynagi()`'ndan çıkıyor ve anahtar
    da aynı fonksiyondan besleniyor — ikisi ayrışırsa bu test düşer.
    """
    from score_abstention import gecerlilik_anahtari, hakem_kaynagi, SOURCE_CLIP
    onek = "A" * SOURCE_CLIP
    # Hakem ikisini AYIRT EDEMEZ (istem bayt-bayt aynı) → anahtar da ayırmamalı.
    assert hakem_kaynagi(onek + "kuyruk-A") == hakem_kaynagi(onek + "kuyruk-B")
    assert gecerlilik_anahtari("S", onek + "kuyruk-A") == gecerlilik_anahtari("S", onek + "kuyruk-B")
    # Klip İÇİNDE ayrışan metinler farklı istem → farklı anahtar (kural tek yöne bozulmasın).
    assert gecerlilik_anahtari("S", "KAYNAK bir") != gecerlilik_anahtari("S", "KAYNAK iki")
    assert gecerlilik_anahtari("S", "KAYNAK bir") != gecerlilik_anahtari("T", "KAYNAK bir")


def test_hakem_isteminden_TASAN_METIN_ANAHTARA_GIRMEZ():
    """Aynı değişmezin uçtan uca hâli: `judge_gecerlilik`'in kurduğu istem AYNI iken
    anahtar da AYNI olmalı. İstem metni ile anahtar arasına klip farkı giremez.

    ⚠️ Bedeli KABUL EDİLDİ ve tek yerde tutuluyor (KARAR-4 m.2): `k=4` bağlamı `k=10`
    bağlamının ÖNEKİ olduğu için ikisi TEK kayda düşer — `k=10`'un paydası bu yüzden
    **TANIMSIZ** damgalıdır ve ondan hüküm kurulmaz. Aleti değil damgayı taşıyoruz.
    """
    from score_abstention import gecerlilik_anahtari, gecerlilik_istemi
    soru = "Kat maliki ortak gideri ödemezse ne olur?"
    k4 = "".join(f"[KAYNAK {i}]\n{'m' * 900}\n" for i in range(1, 5))
    k10 = k4 + "".join(f"[KAYNAK {i}]\n{'m' * 900}\n" for i in range(5, 11))
    assert k10.startswith(k4) and len(k4) > 3500          # gerçek şekil korunuyor
    assert gecerlilik_istemi(soru, k4) == gecerlilik_istemi(soru, k10)
    assert gecerlilik_anahtari(soru, k4) == gecerlilik_anahtari(soru, k10)


# ── KARAR-2: BOŞ BAĞLAMDA PAYDA TANIM GEREĞİ 80/80 (ADR-0048 m.2) ──────────
# Ölçülen kusur: cp09'un AYNI M3 sınavında üç kol 54 · 56 · 39 payda gösterdi. Kural
# aletin dışında (`valid_trap_cache.py`) durduğu için skorlama varsayılan
# `--source-field referans` ile ALTIN maddeyi hakeme gösteriyor, hakem "kaynak
# cevaplıyor" deyip tuzağı geçersiz sayıyordu. Üç sayı da yanlıştı.

def test_payda_tanimdan_gecerli_yalniz_bos_baglam_modunda():
    from score_abstention import payda_tanimdan_gecerli
    assert payda_tanimdan_gecerli("empty") is True
    assert payda_tanimdan_gecerli("oracle") is False
    assert payda_tanimdan_gecerli("distractor_nogold") is False
    assert payda_tanimdan_gecerli("harness") is False
    assert payda_tanimdan_gecerli(None) is False


def test_bos_baglam_kosusu_paydayi_HAKEMSIZ_ve_TAM_verir(tmp_path, monkeypatch):
    """Uçtan uca: `mode=empty` + `--pay-kaynagi onceki` → SIFIR ağ çağrısı, payda n/n.

    Bu test hem KARAR-2'yi (payda 80/80) hem `--pay-kaynagi onceki` sözleşmesini
    kilitler. Ağ çağrısı olursa `make_client` kimlik ister ve test çöker — yani
    "hakeme gitmedi" iddiası gerçekten sınanıyor, varsayılmıyor.
    """
    import json
    import subprocess

    d = tmp_path / "kosu"
    d.mkdir()
    # `referans` DOLU: eski kusurun tam koşulu — hakem görseydi "cevaplıyor" derdi.
    detay = [{"id": i, "soru": f"Soru {i}?", "cevap": "Verilen kaynaklarda bu konu yok.",
              "mode": "empty", "context_shown": "",
              "referans": "Madde 1 — Bu madde soruyu tam olarak cevaplar."} for i in range(4)]
    with open(d / "m3_test_detail.jsonl", "w", encoding="utf-8") as f:
        for r in detay:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    json.dump([{"id": i, "verdict": "ABSTAIN", "used_parametric": False, "reason": "x"}
               for i in range(4)],
              open(d / "abst_m3_test.jsonl", "w", encoding="utf-8"))

    ortam = {k: v for k, v in __import__("os").environ.items()
             if k not in ("OPENAI_API_KEY", "OPENROUTER_API_KEY")}
    ortam["OPENAI_BUDGET_USD"] = "0.01"
    p = subprocess.run(
        [sys.executable, "scripts/score_abstention.py",
         "--details", str(d / "m3_test_detail.jsonl"), "--label", "m3_test",
         "--out-dir", str(d), "--pay-kaynagi", "onceki",
         "--gecerlilik-onbellek", str(tmp_path / "onbellek.json")],
        capture_output=True, text=True, env=ortam)
    assert p.returncode == 0, p.stdout + p.stderr
    ozet = json.load(open(d / "abst_m3_test_summary.json", encoding="utf-8"))
    assert ozet["valid_traps"] == 4, "boş bağlamda payda TANIM gereği n/n olmalı"
    assert ozet["invalid_traps"] == 0
    assert ozet["gecerlilik_tanimdan"] == 4
    assert ozet["judge_cost_usd"] == 0.0, "hiçbir hakem çağrılmamalıydı"
    assert not (tmp_path / "onbellek.json").exists() or \
        json.load(open(tmp_path / "onbellek.json", encoding="utf-8"))["cache"] == {}, \
        "TANIM kararı içerik-adresli önbelleğe SIZMAMALI"


def test_pay_kaynagi_onceki_verdict_dosyasi_yoksa_ERKEN_PATLAR(tmp_path):
    """Sessizce boş verdict'le devam etmek yerine dur (ADR-0026 ruhu)."""
    import json
    import subprocess
    d = tmp_path / "kosu"
    d.mkdir()
    with open(d / "x_detail.jsonl", "w", encoding="utf-8") as f:
        f.write(json.dumps({"id": 0, "soru": "S?", "cevap": "C", "mode": "empty"}) + "\n")
    p = subprocess.run(
        [sys.executable, "scripts/score_abstention.py", "--details", str(d / "x_detail.jsonl"),
         "--label", "x", "--out-dir", str(d), "--pay-kaynagi", "onceki"],
        capture_output=True, text=True)
    assert p.returncode != 0
    assert "abst_x.jsonl" in (p.stdout + p.stderr)


def test_onbellek_yazimi_diskteki_kalemleri_silmez(tmp_path):
    """İki skorlama aynı önbelleğe yazıyor; ikincisi birincinin kalemini silmemeli."""
    from score_abstention import onbellek_yaz, onbellek_oku
    yol = str(tmp_path / "onbellek.json")
    onbellek_yaz(yol, {"a": {"gecerli": True}})
    onbellek_yaz(yol, {"b": {"gecerli": False}})
    okunan = onbellek_oku(yol)
    assert set(okunan) == {"a", "b"}


def test_onbellek_es_zamanli_yazimda_kalem_KAYBETMEZ(tmp_path):
    """🚨 KAYIP GÜNCELLEME kapısı — kilitsiz oku-birleştir-yaz'da bu test DÜŞER.

    Sekiz süreç aynı önbelleğe farklı anahtar yazıyor; hepsi diskteki hâli kilitten ÖNCE
    okumuş olsa bile hiçbiri diğerinin kalemini silmemeli. Ödenmiş hakem kaleminin sessizce
    yok olması bu hattın en pahalı hata sınıfı."""
    import json
    import multiprocessing as mp
    from score_abstention import onbellek_oku

    yol = str(tmp_path / "onbellek.json")
    json.dump({"n": 0, "cache": {}}, open(yol, "w", encoding="utf-8"))

    def yaz(anahtar):
        import sys
        sys.path.insert(0, "scripts")
        import time
        from score_abstention import onbellek_yaz, onbellek_oku
        onbellek_oku(yol)            # bayat kopya: herkes önce okusun
        time.sleep(0.05)             # ...sonra hep birlikte yazsın
        onbellek_yaz(yol, {anahtar: {"gecerli": True}})

    ctx = mp.get_context("fork")
    isciler = [ctx.Process(target=yaz, args=(f"k{i}",)) for i in range(8)]
    for p in isciler:
        p.start()
    for p in isciler:
        p.join(timeout=30)
    assert all(p.exitcode == 0 for p in isciler)
    assert set(onbellek_oku(yol)) == {f"k{i}" for i in range(8)}
    assert not list(tmp_path.glob("*.tmp*")), "atomik replace sonrası geçici dosya kalmamalı"
