import time

import pytest

from pythonoramix.domain.druide.cuiseur import CuiseurNonPréchaufféException
from pythonoramix.domain.recette import INGRÉDIENT_VIDE, Ingrédient, Température
from pythonoramix.infrastructure.thermomix import Thermomix


# @spec cuiseur.thermomix::chauffe-progressivement
def test_préchauffer_rend_la_main_avant_d_atteindre_la_température() -> None:
    thermomix = Thermomix()

    thermomix.préchauffer(_90_DEGRÉS)

    assert thermomix.vérifier_température().degré < _90_DEGRÉS.degré


# @spec cuiseur.thermomix::chauffe-progressivement
def test_préchauffer_atteint_90_degrés_en_2_secondes_7_sans_les_dépasser() -> None:
    thermomix = Thermomix()
    début = time.monotonic()

    thermomix.préchauffer(_90_DEGRÉS)
    _attendre_les_90_degrés(thermomix)

    assert 2.7 <= time.monotonic() - début < _LIMITE_HAUTE_DE_CHAUFFE_EN_SECONDES
    time.sleep(0.4)
    assert thermomix.vérifier_température() == _90_DEGRÉS


# @spec cuiseur.thermomix::chauffe-progressivement
def test_deux_préchauffages_ne_dépassent_pas_la_température_demandée() -> None:
    thermomix = Thermomix(durée_d_un_palier_en_secondes=0.01)

    thermomix.préchauffer(_90_DEGRÉS)
    thermomix.préchauffer(_90_DEGRÉS)
    while thermomix.vérifier_température().degré < _90_DEGRÉS.degré:
        time.sleep(0.01)
    time.sleep(0.05)

    assert thermomix.vérifier_température() == _90_DEGRÉS


# @spec cuiseur.thermomix::refuse-cuisson-hors-temperature
def test_cuire_pendant_le_préchauffage_échoue() -> None:
    thermomix = Thermomix()
    thermomix.préchauffer(_90_DEGRÉS)

    with pytest.raises(CuiseurNonPréchaufféException):
        thermomix.cuire(_FRAISES, "fraise bouillie")


# @spec cuiseur.thermomix::refuse-cuisson-hors-temperature
def test_prélever_après_cuisson_sort_le_résultat_puis_laisse_le_cuiseur_vide() -> None:
    thermomix = Thermomix(durée_d_un_palier_en_secondes=0.001)
    thermomix.préchauffer(_90_DEGRÉS)
    _attendre_les_90_degrés(thermomix)
    thermomix.cuire(_FRAISES, "fraise bouillie")

    assert thermomix.prélever() == Ingrédient(nom="fraise bouillie", quantité=12)
    assert thermomix.prélever() == INGRÉDIENT_VIDE


# @spec cuiseur.thermomix::refuse-cuisson-hors-temperature
def test_un_thermomix_neuf_sans_préchauffage_accepte_de_cuire() -> None:
    thermomix = Thermomix()

    thermomix.cuire(_FRAISES, "fraise bouillie")

    assert thermomix.prélever() == Ingrédient(nom="fraise bouillie", quantité=12)


def test_un_thermomix_neuf_rend_l_ingrédient_vide() -> None:
    assert Thermomix().prélever() == INGRÉDIENT_VIDE


def _attendre_les_90_degrés(thermomix: Thermomix) -> None:
    while thermomix.vérifier_température() != _90_DEGRÉS:
        time.sleep(0.01)


_90_DEGRÉS = Température(degré=90)
_FRAISES = Ingrédient(nom="fraise", quantité=12)
_LIMITE_HAUTE_DE_CHAUFFE_EN_SECONDES = 5
