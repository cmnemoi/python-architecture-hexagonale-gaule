import pytest

from pythonoramix.infrastructure.garde_manger import GardeManger, QuantitéInsuffisanteException


def test_retirer_plus_que_le_contenu_lève_l_erreur_du_garde_manger() -> None:
    garde_manger = GardeManger({"fraise": 11})

    with pytest.raises(QuantitéInsuffisanteException):
        garde_manger.retirer("fraise", 12)

    assert garde_manger.contenu == {"fraise": 11}
