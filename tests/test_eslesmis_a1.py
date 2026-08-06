import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from eslesmis_a1 import eslesmis_a1


RED = "Verilen kaynaklarda bu konuyu düzenleyen madde bulunmuyor."


def _yaz(tmp_path, ad, kayitlar):
    p = tmp_path / ad
    p.write_text("\n".join(json.dumps(k, ensure_ascii=False) for k in kayitlar), encoding="utf-8")
    return str(p)


def test_eslesmis_a1_yalnizca_ikisinin_de_cevapladigi_kalemleri_sayar(tmp_path):
    # id=1 ikisi de cevapladı · id=2 yalnız A cevapladı · id=3 yalnız B cevapladı
    da = _yaz(tmp_path, "da.jsonl", [{"id": "1", "cevap": "Süre on gündür."},
                                     {"id": "2", "cevap": "Süre beş gündür."},
                                     {"id": "3", "cevap": RED}])
    ga = _yaz(tmp_path, "ga.jsonl", [{"id": "1", "faithfulness": 1.0},
                                     {"id": "2", "faithfulness": 0.5},
                                     {"id": "3", "faithfulness": 0.0}])
    db = _yaz(tmp_path, "db.jsonl", [{"id": "1", "cevap": "Süre on gündür."},
                                     {"id": "2", "cevap": RED},
                                     {"id": "3", "cevap": "Süre üç gündür."}])
    gb = _yaz(tmp_path, "gb.jsonl", [{"id": "1", "faithfulness": 0.8},
                                     {"id": "2", "faithfulness": 0.0},
                                     {"id": "3", "faithfulness": 1.0}])
    r = eslesmis_a1(da, ga, db, gb, mode="data")
    assert r["n_kesisim"] == 1
    assert r["id_listesi"] == ["1"]
    assert r["a1_a"] == 1.0
    assert r["a1_b"] == 0.8
    assert abs(r["fark"] - 0.2) < 1e-9


def test_eslesmis_a1_kesisim_bossa_patlar(tmp_path):
    da = _yaz(tmp_path, "da.jsonl", [{"id": "1", "cevap": "Süre on gündür."}])
    ga = _yaz(tmp_path, "ga.jsonl", [{"id": "1", "faithfulness": 1.0}])
    db = _yaz(tmp_path, "db.jsonl", [{"id": "1", "cevap": RED}])
    gb = _yaz(tmp_path, "gb.jsonl", [{"id": "1", "faithfulness": 0.0}])
    with pytest.raises(ValueError, match="kesişim"):
        eslesmis_a1(da, ga, db, gb, mode="data")


def test_eslesmis_a1_gnd_kaydi_eksikse_patlar(tmp_path):
    # detail'da var, gnd'de yok → sessizce atlamak yerine PATLAMALI (bu hattın hata sınıfı
    # sessiz yanlışlık; eksik puanlanmış kalemi görmezden gelmek paydayı kaydırır).
    da = _yaz(tmp_path, "da.jsonl", [{"id": "1", "cevap": "Süre on gündür."},
                                     {"id": "2", "cevap": "Süre beş gündür."}])
    ga = _yaz(tmp_path, "ga.jsonl", [{"id": "1", "faithfulness": 1.0}])
    db = _yaz(tmp_path, "db.jsonl", [{"id": "1", "cevap": "Süre on gündür."},
                                     {"id": "2", "cevap": "Süre üç gündür."}])
    gb = _yaz(tmp_path, "gb.jsonl", [{"id": "1", "faithfulness": 0.8},
                                     {"id": "2", "faithfulness": 0.9}])
    with pytest.raises(KeyError, match="2"):
        eslesmis_a1(da, ga, db, gb, mode="data")
