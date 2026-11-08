import pytest

from pythonoramix.domain.druide.pythonoramix import Pythonoramix
from pythonoramix.domain.druide.stock import IngrédientManquantException
from pythonoramix.domain.recette import INGRÉDIENT_VIDE, RECETTE_DE_LA_POTION_MAGIQUE, Plat, Température
from pythonoramix.infrastructure.garde_manger import GardeManger
from tests.domain.cuiseur_double import CuiseurDouble
from tests.domain.recettes import (
    RECETTE_DES_FRAIFLES,
    RECETTE_DES_FRAIFLES_AU_GUI,
    RECETTE_DES_FRAIFLES_AU_GUI_ET_LAIT_DORÉ,
    RECETTE_DES_FRAIFLES_AU_GUI_PAS_ASSEZ_DE_FRAIFLES,
    RECETTE_DES_FRAIFLES_AU_GUI_PAS_ASSEZ_DE_GUI,
    RECETTE_DES_FRAIFLES_BOUILLIES,
    RECETTE_DES_FRAISES_BOUILLIES,
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
    druide = Pythonoramix(stock, CuiseurDouble())

    plat = druide.préparer(RECETTE_DES_FRAIFLES)

    assert plat == Plat(nom="fraifle", quantité=20)
    assert stock.contenu == []


# @spec druide.preparation::refuse-ingredient-manquant-au-depart
def test_préparer_sans_trèfle_échoue_et_laisse_le_stock_intact() -> None:
    stock = GardeManger([fraises(12)])
    druide = Pythonoramix(stock, CuiseurDouble())

    with pytest.raises(IngrédientManquantException):
        druide.préparer(RECETTE_DES_FRAIFLES)

    assert stock.contenu == [fraises(12)]


# @spec druide.preparation::refuse-ingredient-manquant-au-depart
def test_préparer_avec_une_fraise_de_moins_échoue_et_laisse_le_stock_intact() -> None:
    stock = GardeManger([fraises(11), trèfles(8)])
    druide = Pythonoramix(stock, CuiseurDouble())

    with pytest.raises(IngrédientManquantException):
        druide.préparer(RECETTE_DES_FRAIFLES)

    assert stock.contenu == [fraises(11), trèfles(8)]


# @spec druide.preparation::sert-le-resultat-de-la-derniere-etape
def test_préparer_des_fraifles_au_gui_enchaîne_les_étapes() -> None:
    stock = GardeManger([fraises(12), trèfles(8), gui(1)])
    druide = Pythonoramix(stock, CuiseurDouble())

    plat = druide.préparer(RECETTE_DES_FRAIFLES_AU_GUI)

    assert plat == Plat(nom="fraifle au gui", quantité=21)
    assert stock.contenu == []


# @spec druide.preparation::melange-additionne-les-quantites
def test_préparer_des_fraifles_au_gui_et_lait_doré_additionne_toutes_les_quantités() -> None:
    stock = GardeManger([fraises(12), trèfles(8), gui(1), lait_de_sanglier(4), curcuma(10)])
    druide = Pythonoramix(stock, CuiseurDouble())

    plat = druide.préparer(RECETTE_DES_FRAIFLES_AU_GUI_ET_LAIT_DORÉ)

    assert plat == Plat(nom="fraifle au gui et lait doré", quantité=35)


# @spec druide.preparation::conserve-le-surplus
def test_préparer_avec_une_fraise_de_plus_garde_le_surplus_hors_du_plat() -> None:
    stock = GardeManger([fraises(13), trèfles(8)])
    druide = Pythonoramix(stock, CuiseurDouble())

    plat = druide.préparer(RECETTE_DES_FRAIFLES)

    assert plat == Plat(nom="fraifle", quantité=20)
    assert stock.contenu == [fraises(1)]


# @spec druide.preparation::echoue-sans-restitution-en-cours-de-recette
def test_manquer_de_fraifles_à_la_deuxième_étape_ne_rend_pas_les_ingrédients_consommés() -> None:
    stock = GardeManger([fraises(12), trèfles(8), gui(1)])
    druide = Pythonoramix(stock, CuiseurDouble())

    with pytest.raises(IngrédientManquantException):
        druide.préparer(RECETTE_DES_FRAIFLES_AU_GUI_PAS_ASSEZ_DE_FRAIFLES)

    assert set(stock.contenu) == {fraifles(20), gui(1)}


# @spec druide.preparation::echoue-sans-restitution-en-cours-de-recette
def test_manquer_de_gui_à_la_deuxième_étape_ne_consomme_pas_les_fraifles_de_cette_étape() -> None:
    stock = GardeManger([fraises(12), trèfles(8), gui(1)])
    druide = Pythonoramix(stock, CuiseurDouble())

    with pytest.raises(IngrédientManquantException):
        druide.préparer(RECETTE_DES_FRAIFLES_AU_GUI_PAS_ASSEZ_DE_GUI)

    assert set(stock.contenu) == {fraifles(20), gui(1)}


# @spec druide.preparation::recette-sans-etape-echoue
def test_préparer_une_recette_sans_étape_échoue() -> None:
    druide = Pythonoramix(GardeManger([]), CuiseurDouble())

    with pytest.raises(IngrédientManquantException):
        druide.préparer(RECETTE_SANS_ÉTAPE)


# @spec druide.preparation::ebullition-conserve-la-quantite
def test_préparer_des_fraises_bouillies_conserve_la_quantité_et_vide_le_cuiseur() -> None:
    stock = GardeManger([fraises(12)])
    cuiseur = CuiseurDouble()
    druide = Pythonoramix(stock, cuiseur)

    plat = druide.préparer(RECETTE_DES_FRAISES_BOUILLIES)

    assert plat == Plat(nom="fraise bouillie", quantité=12)
    assert stock.contenu == []
    assert cuiseur.ingrédient_en_cuisson == INGRÉDIENT_VIDE


# @spec druide.preparation::ebullition-conserve-la-quantite
def test_préparer_des_fraifles_bouillies_enchaîne_mélange_et_ébullition() -> None:
    stock = GardeManger([fraises(12), trèfles(8)])
    cuiseur = CuiseurDouble()
    druide = Pythonoramix(stock, cuiseur)

    plat = druide.préparer(RECETTE_DES_FRAIFLES_BOUILLIES)

    assert plat == Plat(nom="fraifle bouillie", quantité=20)
    assert stock.contenu == []
    assert cuiseur.ingrédient_en_cuisson == INGRÉDIENT_VIDE


# @spec druide.preparation::prechauffe-avant-les-etapes
def test_préparer_des_fraises_bouillies_préchauffe_le_cuiseur_à_la_température_demandée() -> None:
    cuiseur = CuiseurDouble()
    druide = Pythonoramix(GardeManger([fraises(12)]), cuiseur)

    druide.préparer(RECETTE_DES_FRAISES_BOUILLIES)

    assert cuiseur.températures_demandées == [Température(degré=90)]


# @spec druide.preparation::prechauffe-avant-les-etapes
def test_préparer_des_fraifles_sans_préchauffage_ne_sollicite_pas_le_cuiseur() -> None:
    cuiseur = CuiseurDouble()
    druide = Pythonoramix(GardeManger([fraises(12), trèfles(8)]), cuiseur)

    druide.préparer(RECETTE_DES_FRAIFLES)

    assert cuiseur.températures_demandées == []


# @spec druide.preparation::refuse-ingredient-manquant-au-depart
def test_un_ingrédient_manquant_empêche_le_préchauffage() -> None:
    cuiseur = CuiseurDouble()
    druide = Pythonoramix(GardeManger([fraises(12)]), cuiseur)

    with pytest.raises(IngrédientManquantException):
        druide.préparer(RECETTE_DES_FRAIFLES_BOUILLIES)

    assert cuiseur.températures_demandées == []


def _stock_de_potion_magique() -> GardeManger:
    return GardeManger([trèfles(8), fraises(12), lait_de_sanglier(4), curcuma(10), gui(1)])


# @spec recette::potion-magique
def test_préparer_la_potion_magique_sert_35_potions_et_vide_le_stock_et_le_cuiseur() -> None:
    stock = _stock_de_potion_magique()
    cuiseur = CuiseurDouble()
    druide = Pythonoramix(stock, cuiseur)

    plat = druide.préparer(RECETTE_DE_LA_POTION_MAGIQUE)

    assert plat == Plat(nom="potion magique", quantité=35)
    assert stock.contenu == []
    assert cuiseur.ingrédient_en_cuisson == INGRÉDIENT_VIDE


# @spec druide.preparation::reste-silencieuse
def test_préparer_la_potion_magique_n_écrit_rien_sur_la_sortie_standard(capsys: pytest.CaptureFixture[str]) -> None:
    druide = Pythonoramix(_stock_de_potion_magique(), CuiseurDouble())

    druide.préparer(RECETTE_DE_LA_POTION_MAGIQUE)

    assert capsys.readouterr().out == ""
