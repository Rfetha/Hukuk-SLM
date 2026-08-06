"""`exact_reject` — çekinme dedektörünün kalibrasyon davranışı.

Her test bir ÖLÇÜLMÜŞ yanlış sınıflandırmayı kilitliyor; hiçbiri varsayımsal değil.
Kaynak: G2 Adım 2.1 + 2.4b + 2.6 (2026-08-06), Gemini ailesi kalibrasyonu.
"""
import sys

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


def test_gecerlilik_anahtari_kaynak_klipinin_otesini_ayirt_etmez():
    """Anahtar hakeme GİDEN metnin üzerinde: klip sonrası aynı olan iki kaynak aynı
    kalemdir. Aksi hâlde önbellek, hakemin görmediği bir farka göre bölünürdü."""
    from score_abstention import gecerlilik_anahtari, SOURCE_CLIP
    uzun = "A" * SOURCE_CLIP
    assert gecerlilik_anahtari("S", uzun) == gecerlilik_anahtari("S", uzun + "kuyruk")


def test_onbellek_yazimi_diskteki_kalemleri_silmez(tmp_path):
    """İki skorlama aynı önbelleğe yazıyor; ikincisi birincinin kalemini silmemeli."""
    from score_abstention import onbellek_yaz, onbellek_oku
    yol = str(tmp_path / "onbellek.json")
    onbellek_yaz(yol, {"a": {"gecerli": True}})
    onbellek_yaz(yol, {"b": {"gecerli": False}})
    okunan = onbellek_oku(yol)
    assert set(okunan) == {"a", "b"}
