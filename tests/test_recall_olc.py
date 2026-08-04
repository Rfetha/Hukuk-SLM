import sys; sys.path.insert(0, "scripts")
from recall_olc import recall_at_k


def test_recall_at_k_bulunanlari_sayar():
    # sıra = altının kaçıncı sırada geldiği (0-tabanlı), None = hiç gelmedi
    assert recall_at_k([0, 1, 2, None], k=3) == 0.75


def test_recall_at_k_k_disindakini_saymaz():
    assert recall_at_k([0, 5], k=3) == 0.5


def test_recall_at_k_bos_liste_sifir():
    assert recall_at_k([], k=10) == 0.0
