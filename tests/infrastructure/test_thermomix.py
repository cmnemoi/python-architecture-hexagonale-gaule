import time

import pytest

from pythonoramix.infrastructure.thermomix import ContenuDuBol, TempératureNonAtteinteException, Thermomix


# @spec cuiseur.thermomix::chauffe-progressivement
def test_lancer_la_chauffe_rend_la_main_avant_d_atteindre_la_température() -> None:
    thermomix = Thermomix()

    thermomix.lancer_la_chauffe(90)

    assert thermomix.lire_la_température() < 90


# @spec cuiseur.thermomix::chauffe-progressivement
def test_la_chauffe_atteint_90_degrés_en_2_secondes_7_sans_les_dépasser() -> None:
    thermomix = Thermomix()
    début = time.monotonic()

    thermomix.lancer_la_chauffe(90)
    _attendre_la_température(thermomix, 90)

    assert time.monotonic() - début >= 2.7
    time.sleep(0.4)
    assert thermomix.lire_la_température() == 90


# @spec cuiseur.thermomix::refuse-cuisson-hors-temperature
def test_cuire_pendant_la_chauffe_lève_l_erreur_du_thermomix() -> None:
    thermomix = Thermomix()
    thermomix.lancer_la_chauffe(90)

    with pytest.raises(TempératureNonAtteinteException):
        thermomix.cuire("fraise bouillie", 12)


def test_vider_le_bol_sort_la_cuisson_puis_ne_rend_plus_rien() -> None:
    thermomix = Thermomix(durée_d_un_palier_en_secondes=0.001)
    thermomix.lancer_la_chauffe(90)
    _attendre_la_température(thermomix, 90)
    thermomix.cuire("fraise bouillie", 12)

    assert thermomix.vider_le_bol() == ContenuDuBol(nom="fraise bouillie", quantité=12)
    assert thermomix.vider_le_bol() is None


def _attendre_la_température(thermomix: Thermomix, degrés: int) -> None:
    while thermomix.lire_la_température() != degrés:
        time.sleep(0.01)
