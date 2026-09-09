"""`hakhukuk "soru"` — `servis.answer()` üstünde ince kabuk. Kendi mantığı yoktur.

Çıktı dört şeyi ayrı ayrı gösterir ve hiçbirini gizlemez:
durum rozeti · cevap · atıflar (doğrulanmamışlar ⚠️ ile) · kaynaklar · sorumluluk ibaresi.
"""
import argparse
import sys

from hakhukuk.tipler import Cevap, Durum

# ⚠️ GEÇİCİ METİN — açık karar S10. Nihai hukuki ibare hukukçu görüşüne bağlı; geldiğinde
# BURADAN, tek yerden güncellenir. `tui.py` bu sabiti IMPORT eder, kopyalamaz: S18'in dersi
# aynı metnin iki yerde sessizce ayrışmasıydı.
SORUMLULUK_IBARESI = (
    "⚖️  Bu yanıt hukuki tavsiye değil, bilgilendirme amaçlıdır. Bağlayıcı bir karar "
    "vermeden önce güncel mevzuatı doğrulayın ve bir avukata danışın."
)

ROZET = {
    Durum.CEVAP: "✅ CEVAP — dayanağı getirilen kaynaklarda",
    Durum.CEKINCELI: "⚠️ ÇEKİNCELİ — kısmen dayanaklı; atıfları kendiniz doğrulayın",
    Durum.SUSKUNLUK: "🤐 SUSKUNLUK — kaynaklarda karşılık bulunamadı",
    Durum.KESIK: "✂️ KESİK — üretim bütçesi bitti, cevap YARIM",
    # ⛔ KESİK'ten AYRI (ADR-0076): orada cümle yarım, burada cümle tam ama DAYANAĞI eksik.
    Durum.ARAMA_TUKENDI: "🔍 ARAMA TÜKENDİ — arama sınırına dayanıldı, dayanak EKSİK olabilir",
}


def bicimle(cevap: Cevap) -> str:
    """Cevabı insan okur biçime çevir. Yan etkisi yok — test edilebilsin diye ayrı."""
    parcalar = [ROZET[cevap.durum], "", cevap.metin.strip(), ""]
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
