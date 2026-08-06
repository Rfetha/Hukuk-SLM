"""`exact_reject` — çekinme dedektörünün kalibrasyon davranışı.

Her test bir ÖLÇÜLMÜŞ yanlış sınıflandırmayı kilitliyor; hiçbiri varsayımsal değil.
Kaynak: G2 Adım 2.1 + 2.4b (2026-08-06), Gemini ailesi kalibrasyonu.
"""
import sys

sys.path.insert(0, "scripts")
from score_abstention import exact_reject  # noqa: E402


# ── ADR-0058 açılış yeterlilik hükmü — kural İKİ KUTUPLU ────────────────────
# Ölçülen sapma iki yönlüydü: h1'de red=kötü (yanlış-pozitif rakibi kötü gösterir),
# h2b'de red=iyi (aynı hata rakibi iyi gösterir). Bu yüzden "muhafazakâr" savunması yok.

def test_exact_reject_olumlu_yeterlilik_acilisi_govdedeki_olumsuzlamaya_kanmaz():
    """h2b_fl35_k4'te 4/80 = 5 puan. Açılış 'kaynaklar cevaplamaktadır' diyorsa,
    gövdedeki olumsuzlamanın öznesi KAYNAK değil HUKUKUN İÇERİĞİdir."""
    cevap = ("Verilen kaynaklar soruyu doğrudan cevaplamaktadır. Verilen kaynaklarda "
             "zorla fuhşa sevketme fiilinin insanlığa karşı bir suç olarak "
             "düzenlendiğine dair bir hüküm yoktur.")
    assert exact_reject(cevap, "data") is False


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
