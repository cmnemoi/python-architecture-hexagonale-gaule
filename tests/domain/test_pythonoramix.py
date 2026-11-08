from pythonoramix.domain.druide.pythonoramix import Pythonoramix
from pythonoramix.domain.recette import Plat
from pythonoramix.infrastructure.garde_manger import GardeManger
from tests.domain.recettes import RECETTE_DES_FRAIFLES, fraises, trèfles


# @spec druide.preparation::sert-le-resultat-de-la-derniere-etape
def test_préparer_des_fraifles_sert_le_résultat_et_vide_le_stock() -> None:
    stock = GardeManger([fraises(12), trèfles(8)])
    druide = Pythonoramix(stock)

    plat = druide.préparer(RECETTE_DES_FRAIFLES)

    assert plat == Plat(nom="fraifle", quantité=20)
    assert stock.contenu == []
