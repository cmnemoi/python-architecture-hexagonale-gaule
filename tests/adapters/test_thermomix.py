import time

import pytest

from pythonoramix.adapters.druide import thermomix as thermomix_adapté
from pythonoramix.domain.druide.cuiseur import CuiseurNonPréchaufféException
from pythonoramix.domain.recette import INGRÉDIENT_VIDE, Ingrédient, Température
from pythonoramix.infrastructure.thermomix import Thermomix


# @spec adaptateurs::traduisent-le-thermomix
def test_préchauffer_puis_vérifier_parle_en_températures() -> None:
    cuiseur = thermomix_adapté.Thermomix(Thermomix(durée_d_un_palier_en_secondes=0.001))

    cuiseur.préchauffer(_90_DEGRÉS)
    _attendre_la_température(cuiseur)

    assert cuiseur.vérifier_température() == _90_DEGRÉS


# @spec cuiseur.thermomix::refuse-cuisson-hors-temperature
def test_cuire_pendant_le_préchauffage_lève_l_erreur_du_domaine() -> None:
    cuiseur = thermomix_adapté.Thermomix(Thermomix())
    cuiseur.préchauffer(_90_DEGRÉS)

    with pytest.raises(CuiseurNonPréchaufféException):
        cuiseur.cuire(_FRAISES, "fraise bouillie")


# @spec adaptateurs::traduisent-le-thermomix
def test_prélever_après_cuisson_rend_le_résultat_puis_l_ingrédient_vide() -> None:
    cuiseur = thermomix_adapté.Thermomix(Thermomix(durée_d_un_palier_en_secondes=0.001))
    cuiseur.préchauffer(_90_DEGRÉS)
    _attendre_la_température(cuiseur)
    cuiseur.cuire(_FRAISES, "fraise bouillie")

    assert cuiseur.prélever() == Ingrédient(nom="fraise bouillie", quantité=12)
    assert cuiseur.prélever() == INGRÉDIENT_VIDE


def _attendre_la_température(cuiseur: thermomix_adapté.Thermomix) -> None:
    while cuiseur.vérifier_température() != _90_DEGRÉS:
        time.sleep(0.01)


_90_DEGRÉS = Température(degré=90)
_FRAISES = Ingrédient(nom="fraise", quantité=12)
