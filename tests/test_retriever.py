import json
import sys

import numpy as np
import pytest

sys.path.insert(0, "scripts")
from retriever import Retriever, rrf_birlestir  # noqa: E402


KORPUS = [
    {"kanun_no": "5271", "kanun_adi": "CEZA MUHAKEMESİ KANUNU", "madde_no": "Madde 161",
     "text": "Cumhuriyet savcısı soruşturmayı bizzat yapar."},
    {"kanun_no": "4857", "kanun_adi": "İŞ KANUNU", "madde_no": "Madde 21",
     "text": "İşe iade davası açan işçi işverene başvurur."},
    {"kanun_no": "634", "kanun_adi": "KAT MÜLKİYETİ KANUNU", "madde_no": "Geçici Madde 1",
     "text": "Ortak giderlere katılmayan kat maliki gecikme tazminatı öder."},
]


def _korpus_yaz(tmp_path):
    yol = tmp_path / "korpus.jsonl"
    yol.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in KORPUS) + "\n",
                   encoding="utf-8")
    return str(yol)


def _sahte_gomucu(metinler):
    """Deterministik sahte gömme: karakter histogramı. Gerçek model indirmez."""
    M = np.zeros((len(metinler), 32), dtype=np.float32)
    for i, m in enumerate(metinler):
        for ch in m.lower():
            M[i, ord(ch) % 32] += 1.0
    M /= np.linalg.norm(M, axis=1, keepdims=True) + 1e-9
    return M


def test_kur_yukle_getir_tur_donusu(tmp_path):
    korpus = _korpus_yaz(tmp_path)
    idx = str(tmp_path / "indeks")
    Retriever.kur(korpus, idx, gomucu=_sahte_gomucu)
    r = Retriever.yukle(idx, gomucu=_sahte_gomucu)
    sonuc = r.getir("Cumhuriyet savcısı soruşturmayı bizzat yapar", k=2)
    assert len(sonuc) == 2
    assert sonuc[0]["madde_no"] == "Madde 161"
    assert sonuc[0]["sira"] == 0 and sonuc[1]["sira"] == 1
    assert sonuc[0]["skor"] >= sonuc[1]["skor"]


def test_getir_k_korpustan_buyukse_korpusla_sinirli(tmp_path):
    korpus = _korpus_yaz(tmp_path)
    idx = str(tmp_path / "indeks")
    Retriever.kur(korpus, idx, gomucu=_sahte_gomucu)
    assert len(Retriever.yukle(idx, gomucu=_sahte_gomucu).getir("işçi", k=99)) == len(KORPUS)


def test_getir_tam_madde_metnini_dondurur_kirpmaz(tmp_path):
    # ⚠️ ADR-0054/K2: 900 karakter kırpması retriever'da DEĞİL, bağlam modele
    # verilirken uygulanır. Retriever kırparsa kural sessizce ihlal edilir.
    uzun = dict(KORPUS[0], text="A" * 3000)
    yol = tmp_path / "uzun.jsonl"
    yol.write_text(json.dumps(uzun, ensure_ascii=False) + "\n", encoding="utf-8")
    idx = str(tmp_path / "indeks")
    Retriever.kur(str(yol), idx, gomucu=_sahte_gomucu)
    assert len(Retriever.yukle(idx, gomucu=_sahte_gomucu).getir("A", k=1)[0]["text"]) == 3000


def test_yukle_korpus_degistiyse_erken_patlar(tmp_path):
    # ⚠️ Bayat indeks SESSİZ yanlışlıktır: sorgular eski korpusa göre cevaplanır,
    # hiçbir yerde hata çıkmaz.
    korpus = _korpus_yaz(tmp_path)
    idx = str(tmp_path / "indeks")
    Retriever.kur(korpus, idx, gomucu=_sahte_gomucu)
    with open(korpus, "a", encoding="utf-8") as f:
        f.write(json.dumps(KORPUS[0], ensure_ascii=False) + "\n")
    with pytest.raises(SystemExit, match="korpus"):
        Retriever.yukle(idx)


def test_kunye_olcum_degismezlerini_yazar(tmp_path):
    korpus = _korpus_yaz(tmp_path)
    idx = str(tmp_path / "indeks")
    Retriever.kur(korpus, idx, gomucu=_sahte_gomucu, model_adi="sahte/model")
    k = json.load(open(f"{idx}/KUNYE.json", encoding="utf-8"))
    assert k["model"] == "sahte/model"
    assert k["n"] == len(KORPUS)
    assert k["yontem"] == "hibrit_bm25+yogun_rrf"
    assert k["chunk"] == "tam madde (ADR-0054/K2)"


def test_rrf_iki_kaynakta_da_ustte_olan_kazanir():
    a = np.array([9.0, 8.0, 1.0])
    b = np.array([1.0, 9.0, 8.0])
    assert int(np.argmax(rrf_birlestir([a, b], rrf_k=60))) == 1
