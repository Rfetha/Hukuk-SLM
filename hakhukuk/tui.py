"""Tek ekranlı terminal arayüzü. answer() üstünde İNCE KABUK — kendi mantığı YOKTUR.

⚠️ Sınıflandırma/atıf mantığı buraya sızarsa iki yerde bakım olur ve ikisi sessizce
ayrışır (bkz. istem sürüklenmesi, S18: aynı metin beş dosyada, ikisi farklıydı).
tests/test_tui.py bunu bir KAPI olarak sınar.
"""
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header, Input, Static

from hakhukuk.cli import SORUMLULUK_IBARESI
from hakhukuk.servis import answer
from hakhukuk.tipler import Durum

ROZET = {
    Durum.CEVAP: "🟢 CEVAP",
    Durum.CEKINCELI: "🟡 ÇEKİNCELİ CEVAP — doğrudan hüküm bulunamadı",
    Durum.SUSKUNLUK: "⚪ SUSKUNLUK — dayanak bulunamadı",
    Durum.KESIK: "🟠 KESİK — üretim bütçesi bitti, cevap YARIM",
    # ⛔ KESİK'ten AYRI (ADR-0076): cümle tam, DAYANAĞI eksik olabilir.
    Durum.ARAMA_TUKENDI: "🔵 ARAMA TÜKENDİ — arama sınırına dayanıldı, dayanak EKSİK olabilir",
}


class HakHukukTUI(App):
    TITLE = "HakHukuk"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Hukuki sorunuzu yazın…", id="soru")
        yield VerticalScroll(Static("", id="cikti"))
        yield Footer()

    def on_input_submitted(self, olay: Input.Submitted) -> None:
        self.query_one("#cikti", Static).update("⏳ kaynaklar taranıyor…")
        c = answer(olay.value)
        atif = "\n".join(
            f"  {'✅' if a.dogrulandi else '⚠️ DOĞRULANAMADI'} {a.kanun_no} {a.madde_no}"
            for a in c.atiflar) or "  (atıf yok)"
        kaynak = "\n".join(f"  {k.sira}. {k.kanun_adi} {k.madde_no}" for k in c.kaynaklar)
        self.query_one("#cikti", Static).update(
            f"{ROZET[c.durum]}\n\n{c.metin}\n\nATIFLAR:\n{atif}\n\n"
            f"KAYNAKLAR:\n{kaynak}\n\n{SORUMLULUK_IBARESI}")


def main() -> None:
    HakHukukTUI().run()


# ⚠️ Bu blok olmadan `python -m hakhukuk.tui` modülü içe aktarıp SESSİZCE çıkıyordu:
# `main()` tanımlıydı ama çağrılmıyordu. `cli.py`'de vardı, burada yoktu ve hiçbir test
# yakalamadı — kaynak denetimi mantığın sızmadığına bakar, programın çalıştığına değil.
# Gözle doğrulama kapısında yakalandı (2026-09-09); `tests/test_tui.py` artık çiviliyor.
if __name__ == "__main__":
    main()
