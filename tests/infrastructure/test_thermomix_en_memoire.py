import time

import pytest

from pythonoramix.domain.druide.cuiseur import CuiseurNonPréchaufféException
from pythonoramix.domain.recette import INGRÉDIENT_VIDE, Ingrédient, Température
from pythonoramix.infrastructure.thermomix_en_memoire import ThermomixEnMémoire


# @spec cuiseur.thermomix::chauffe-progressivement
def test_préchauffer_rend_la_main_avant_d_atteindre_la_température() -> None:
    thermomix = ThermomixEnMémoire()

    thermomix.préchauffer(_90_DEGRÉS)

    assert thermomix.vérifier_température().degré < _90_DEGRÉS.degré


# @spec cuiseur.thermomix::chauffe-progressivement
def test_préchauffer_atteint_90_degrés_en_2_secondes_7_sans_les_dépasser() -> None:
    thermomix = ThermomixEnMémoire()
    début = time.monotonic()

    thermomix.préchauffer(_90_DEGRÉS)
    _attendre_les_90_degrés(thermomix)

    assert time.monotonic() - début >= 2.7
    time.sleep(0.4)
    assert thermomix.vérifier_température() == _90_DEGRÉS


# @spec cuiseur.thermomix::refuse-cuisson-hors-temperature
def test_cuire_pendant_le_préchauffage_échoue() -> None:
    thermomix = ThermomixEnMémoire()
    thermomix.préchauffer(_90_DEGRÉS)

    with pytest.raises(CuiseurNonPréchaufféException):
        thermomix.cuire(_FRAISES, "fraise bouillie")


# @spec cuiseur.thermomix::refuse-cuisson-hors-temperature
def test_prélever_après_cuisson_sort_le_résultat_puis_laisse_le_cuiseur_vide() -> None:
    thermomix = ThermomixEnMémoire(durée_d_un_palier_en_secondes=0.001)
    thermomix.préchauffer(_90_DEGRÉS)
    _attendre_les_90_degrés(thermomix)
    thermomix.cuire(_FRAISES, "fraise bouillie")

    assert thermomix.prélever() == Ingrédient(nom="fraise bouillie", quantité=12)
    assert thermomix.prélever() == INGRÉDIENT_VIDE


def _attendre_les_90_degrés(thermomix: ThermomixEnMémoire) -> None:
    while thermomix.vérifier_température() != _90_DEGRÉS:
        time.sleep(0.01)


_90_DEGRÉS = Température(degré=90)
_FRAISES = Ingrédient(nom="fraise", quantité=12)
