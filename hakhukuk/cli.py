"""`hakhukuk "soru"` — `servis.answer()` üstünde ince kabuk. Kendi mantığı yoktur.

Çıktı dört şeyi ayrı ayrı gösterir ve hiçbirini gizlemez:
durum rozeti · cevap · atıflar (doğrulanmamışlar ⚠️ ile) · kaynaklar · sorumluluk ibaresi.
"""
import argparse
import json
import pathlib
import sys

from hakhukuk.tipler import Cevap, Durum

# ⚠️ GEÇİCİ METİN — açık karar S10. Nihai hukuki ibare hukukçu görüşüne bağlı; geldiğinde
# BURADAN, tek yerden güncellenir. `tui.py` bu sabiti IMPORT eder, kopyalamaz: S18'in dersi
# aynı metnin iki yerde sessizce ayrışmasıydı.
SORUMLULUK_IBARESI = (
    "⚖️  Bu yanıt hukuki tavsiye değil, bilgilendirme amaçlıdır. Bağlayıcı bir karar "
    "vermeden önce güncel mevzuatı doğrulayın ve bir avukata danışın."
)

# ⚠️ Görev 21 Adım 7: sayılar KUNYE.json'dan OKUNUR, koda gömülmez — künye değişince
# bu satır da (yeniden okunarak) değişmeli, elle güncellenmemeli.
_KUNYE_YOLU = pathlib.Path(__file__).resolve().parent.parent / "data/corpus/KUNYE.json"


def kapsam_satiri() -> str:
    """Statik kapsam satırı — SINIFLANDIRICI YOK (karar 3, brief Adım 7).

    Bir soru sınıflandırıcısı yanılır ve yanıldığında vatandaşa "bu konu kapsam
    dışı" diyerek cevabı olan soruyu öldürür. Ucuz ve dürüst alternatif: kapsamı
    HER ZAMAN, aynı statik satırla göstermek. Künye dosyası bulunamazsa uygulamanın
    AÇILMAMASI kabul edilebilir bir karar DEĞİL (brief); bu yüzden sayısız ama
    dürüst bir satırla devam edilir, patlanmaz.

    ⚠️ Burası `tui.py`'de DEĞİL `cli.py`'de duruyor (`SORUMLULUK_IBARESI` emsali): metnin
    ikinci bir kopyası çıkarsa iki yüzey sessizce ayrışır (S18) ve `cli`/`api` bu satırı
    almak için `textual` bağımlılığını içeri çekmek zorunda kalırdı.
    """
    try:
        kunye = json.loads(_KUNYE_YOLU.read_text(encoding="utf-8"))
        n_kanun, n_madde = kunye["n_kanun"], kunye["n_madde"]
        n_madde_bicimli = f"{n_madde:,}".replace(",", ".")
        return (
            f"Kapsam: yürürlükteki {n_kanun} kanun, {n_madde_bicimli} madde "
            f"({kunye.get('anlik_goruntu_tarihi', '?')} itibarıyla). "
            "Yönetmelik · tüzük · KHK · tebliğ YOK."
        )
    except (OSError, KeyError, json.JSONDecodeError):
        return ("Kapsam: yürürlükteki kanunlar (künye okunamadı — sayı belirsiz). "
                "Yönetmelik · tüzük · KHK · tebliğ YOK.")


ROZET = {
    Durum.CEVAP: "✅ CEVAP — dayanağı getirilen kaynaklarda",
    Durum.CEKINCELI: "⚠️ ÇEKİNCELİ — kısmen dayanaklı; atıfları kendiniz doğrulayın",
    Durum.SUSKUNLUK: "🤐 SUSKUNLUK — kaynaklarda karşılık bulunamadı",
    Durum.KESIK: "✂️ KESİK — üretim bütçesi bitti, cevap YARIM",
    # ⛔ KESİK'ten AYRI (ADR-0076): orada cümle yarım, burada cümle tam ama DAYANAĞI eksik.
    Durum.ARAMA_TUKENDI: "🔍 ARAMA TÜKENDİ — arama sınırına dayanıldı, dayanak EKSİK olabilir",
}


def iskele_isaretlerini_sil(metin: str) -> str:
    """`##begin_quote##`/`##end_quote##` iskelesini SUNUM katmanında temizler.

    ⛔ Yalnız sunum katmanında: `Cevap.metin` modelin ham çıktısıdır, `score_register.py:41`
    aynı işareti register göstergesi olarak SAYIYOR — ham alanı değiştirmek ölçümü bozar.
    `tui.py` bu fonksiyonu IMPORT eder, KOPYALAMAZ (S18'in dersi).
    """
    return metin.replace("##begin_quote##", "").replace("##end_quote##", "")


def bicimle(cevap: Cevap) -> str:
    """Cevabı insan okur biçime çevir. Yan etkisi yok — test edilebilsin diye ayrı."""
    parcalar = [ROZET[cevap.durum], "", iskele_isaretlerini_sil(cevap.metin.strip()), ""]
    if cevap.atiflar:
        parcalar.append("Atıflar:")
        for a in cevap.atiflar:
            isaret = "  ✓" if a.dogrulandi else "  ⚠️ DOĞRULANAMADI —"
            parcalar.append(f"{isaret} {a.kanun_no}/{a.madde_no}".rstrip())
        parcalar.append("")
    if cevap.kaynaklar:
        parcalar.append("Kaynaklar:")
        parcalar += [f"  [{k.sira}] {k.kanun_adi} {k.madde_no}" for k in cevap.kaynaklar]
        parcalar.append("")
    parcalar.append(SORUMLULUK_IBARESI)
    return "\n".join(parcalar)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="hakhukuk", description="Türk hukuku asistanı")
    p.add_argument("soru", nargs="?", help="sorulacak soru")
    p.add_argument("-k", type=int, default=None, help="getirilecek kaynak sayısı")
    p.add_argument("--kuru-calisma", action="store_true",
                   help="model ve indeks olmadan çıktı biçimini göster (duman testi)")
    p.add_argument("--durumlari-listele", action="store_true",
                   help="dört durumu ve ne anlama geldiklerini yaz")
    a = p.parse_args(argv)

    if a.durumlari_listele:
        for d in Durum:
            print(f"{d.name:<10} {ROZET[d]}")
        return 0

    if not a.soru:
        p.error("soru gerekli (ya da --durumlari-listele)")

    if a.kuru_calisma:
        # Sunucu ve indeks GEREKMEZ: çıktı biçimi ve ibare, ağır bağımlılık olmadan sınanır.
        ornek = Cevap(metin=f"(kuru çalışma) soru alındı: {a.soru}",
                      durum=Durum.SUSKUNLUK, atiflar=(), kaynaklar=())
        print(bicimle(ornek))
        return 0

    from hakhukuk import servis  # noqa: PLC0415 — retriever ~2 GB, gecikmeli yüklenir
    cevap = servis.answer(a.soru, **({"k": a.k} if a.k else {}))
    print(bicimle(cevap))
    return 0


if __name__ == "__main__":
    sys.exit(main())
