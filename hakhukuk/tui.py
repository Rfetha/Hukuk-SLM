"""Tek ekranlı terminal arayüzü. answer() üstünde İNCE KABUK — kendi mantığı YOKTUR.

⚠️ Sınıflandırma/atıf mantığı buraya sızarsa iki yerde bakım olur ve ikisi sessizce
ayrışır (bkz. istem sürüklenmesi, S18: aynı metin beş dosyada, ikisi farklıydı).
tests/test_tui.py bunu bir KAPI olarak sınar.
"""
from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header, Input, Static

from hakhukuk.cli import SORUMLULUK_IBARESI, iskele_isaretlerini_sil, kapsam_satiri
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
        yield Static(
            "Hukuki sorunuzu yazıp Enter'a basın.\n" + kapsam_satiri(), id="yonerge")
        yield Input(placeholder="Hukuki sorunuzu yazın…", id="soru")
        yield VerticalScroll(Static("", id="cikti"))
        yield Footer()

    def on_input_submitted(self, olay: Input.Submitted) -> None:
        self.query_one("#cikti", Static).update("⏳ kaynaklar taranıyor…")
        self._soruyu_yanitla(olay.value)

    # ⚠️ kusur 3: `answer()` ağ + retriever I/O yapar, olay döngüsünde çağrılırsa
    # arayüz 30-60 sn DONAR. `@work(thread=True)` çalışan iş parçacığına alır;
    # widget güncellemesi `call_from_thread` ile ana döngüye postalanır (evre-güvenliği).
    @work(thread=True)
    def _soruyu_yanitla(self, soru: str) -> None:
        cikti = self.query_one("#cikti", Static)
        try:
            c = answer(soru)
        except Exception as hata:
            # ⚠️ Savunmacı fazlalık DEĞİL: sunucunun kapalı olması (llama-server elle
            # açılıyor) ya da indeksin yüklenememesi bu üründe OLASI bir senaryodur —
            # ekran sessizce donuk kalırsa boş ekrandan ayırt edilemez.
            self.call_from_thread(cikti.update, f"⛔ Hata: {hata}")
            return
        atif = "\n".join(
            f"  {'✅' if a.dogrulandi else '⚠️ DOĞRULANAMADI'} {a.kanun_no} {a.madde_no}"
            for a in c.atiflar) or "  (atıf yok)"
        kaynak = "\n".join(f"  {k.sira}. {k.kanun_adi} {k.madde_no}" for k in c.kaynaklar)
        self.call_from_thread(
            cikti.update,
            f"{ROZET[c.durum]}\n\n{iskele_isaretlerini_sil(c.metin)}\n\nATIFLAR:\n{atif}\n\n"
            f"KAYNAKLAR:\n{kaynak}\n\n{SORUMLULUK_IBARESI}")


def main() -> None:
    HakHukukTUI().run()


# ⚠️ Bu blok olmadan `python -m hakhukuk.tui` modülü içe aktarıp SESSİZCE çıkıyordu:
# `main()` tanımlıydı ama çağrılmıyordu. `cli.py`'de vardı, burada yoktu ve hiçbir test
# yakalamadı — kaynak denetimi mantığın sızmadığına bakar, programın çalıştığına değil.
# Gözle doğrulama kapısında yakalandı (2026-09-09); `tests/test_tui.py` artık çiviliyor.
if __name__ == "__main__":
    main()
