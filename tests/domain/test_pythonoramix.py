import pytest

from pythonoramix.domain.druide.pythonoramix import Pythonoramix
from pythonoramix.domain.druide.stock import IngrédientManquantException
from pythonoramix.domain.recette import Plat
from pythonoramix.infrastructure.garde_manger import GardeManger
from tests.domain.recettes import (
    RECETTE_DES_FRAIFLES,
    RECETTE_DES_FRAIFLES_AU_GUI,
    RECETTE_DES_FRAIFLES_AU_GUI_ET_LAIT_DORÉ,
    RECETTE_DES_FRAIFLES_AU_GUI_PAS_ASSEZ_DE_FRAIFLES,
    RECETTE_DES_FRAIFLES_AU_GUI_PAS_ASSEZ_DE_GUI,
    RECETTE_SANS_ÉTAPE,
    curcuma,
    fraifles,
    fraises,
    gui,
    lait_de_sanglier,
    trèfles,
)


# @spec druide.preparation::sert-le-resultat-de-la-derniere-etape
def test_préparer_des_fraifles_sert_le_résultat_et_vide_le_stock() -> None:
    stock = GardeManger([fraises(12), trèfles(8)])
    druide = Pythonoramix(stock)

    plat = druide.préparer(RECETTE_DES_FRAIFLES)

    assert plat == Plat(nom="fraifle", quantité=20)
    assert stock.contenu == []


# @spec druide.preparation::refuse-ingredient-manquant-au-depart
def test_préparer_sans_trèfle_échoue_et_laisse_le_stock_intact() -> None:
    stock = GardeManger([fraises(12)])
    druide = Pythonoramix(stock)

    with pytest.raises(IngrédientManquantException):
        druide.préparer(RECETTE_DES_FRAIFLES)

    assert stock.contenu == [fraises(12)]


# @spec druide.preparation::refuse-ingredient-manquant-au-depart
def test_préparer_avec_une_fraise_de_moins_échoue_et_laisse_le_stock_intact() -> None:
    stock = GardeManger([fraises(11), trèfles(8)])
    druide = Pythonoramix(stock)

    with pytest.raises(IngrédientManquantException):
        druide.préparer(RECETTE_DES_FRAIFLES)

    assert stock.contenu == [fraises(11), trèfles(8)]


# @spec druide.preparation::sert-le-resultat-de-la-derniere-etape
def test_préparer_des_fraifles_au_gui_enchaîne_les_étapes() -> None:
    stock = GardeManger([fraises(12), trèfles(8), gui(1)])
    druide = Pythonoramix(stock)

    plat = druide.préparer(RECETTE_DES_FRAIFLES_AU_GUI)

    assert plat == Plat(nom="fraifle au gui", quantité=21)
    assert stock.contenu == []


# @spec druide.preparation::melange-additionne-les-quantites
def test_préparer_des_fraifles_au_gui_et_lait_doré_additionne_toutes_les_quantités() -> None:
    stock = GardeManger([fraises(12), trèfles(8), gui(1), lait_de_sanglier(4), curcuma(10)])
    druide = Pythonoramix(stock)

    plat = druide.préparer(RECETTE_DES_FRAIFLES_AU_GUI_ET_LAIT_DORÉ)

    assert plat == Plat(nom="fraifle au gui et lait doré", quantité=35)


# @spec druide.preparation::conserve-le-surplus
def test_préparer_avec_une_fraise_de_plus_garde_le_surplus_hors_du_plat() -> None:
    stock = GardeManger([fraises(13), trèfles(8)])
    druide = Pythonoramix(stock)

    plat = druide.préparer(RECETTE_DES_FRAIFLES)

    assert plat == Plat(nom="fraifle", quantité=20)
    assert stock.contenu == [fraises(1)]


# @spec druide.preparation::echoue-sans-restitution-en-cours-de-recette
def test_manquer_de_fraifles_à_la_deuxième_étape_ne_rend_pas_les_ingrédients_consommés() -> None:
    stock = GardeManger([fraises(12), trèfles(8), gui(1)])
    druide = Pythonoramix(stock)

    with pytest.raises(IngrédientManquantException):
        druide.préparer(RECETTE_DES_FRAIFLES_AU_GUI_PAS_ASSEZ_DE_FRAIFLES)

    assert set(stock.contenu) == {fraifles(20), gui(1)}


# @spec druide.preparation::echoue-sans-restitution-en-cours-de-recette
def test_manquer_de_gui_à_la_deuxième_étape_ne_consomme_pas_les_fraifles_de_cette_étape() -> None:
    stock = GardeManger([fraises(12), trèfles(8), gui(1)])
    druide = Pythonoramix(stock)

    with pytest.raises(IngrédientManquantException):
        druide.préparer(RECETTE_DES_FRAIFLES_AU_GUI_PAS_ASSEZ_DE_GUI)

    assert set(stock.contenu) == {fraifles(20), gui(1)}


# @spec druide.preparation::recette-sans-etape-echoue
def test_préparer_une_recette_sans_étape_échoue() -> None:
    druide = Pythonoramix(GardeManger([]))

    with pytest.raises(IngrédientManquantException):
        druide.préparer(RECETTE_SANS_ÉTAPE)
