from pythonoramix.domain.recette import INGRÉDIENT_VIDE, Ingrédient
from pythonoramix.infrastructure.garde_manger_en_memoire import GardeManger


# @spec infrastructure::garde-manger-respecte-le-stock
def test_vérifier_disponibilité_accepte_la_quantité_exacte_et_refuse_une_de_plus() -> None:
    stock = GardeManger([_fraises(12)])

    assert stock.vérifier_disponibilité(_fraises(12))
    assert not stock.vérifier_disponibilité(_fraises(13))


# @spec infrastructure::garde-manger-respecte-le-stock
def test_un_ingrédient_absent_n_est_ni_disponible_ni_récupérable() -> None:
    stock = GardeManger([])

    assert not stock.vérifier_disponibilité(_fraises(1))
    assert stock.récupérer_ingrédient(_fraises(1)) is None


# @spec infrastructure::garde-manger-respecte-le-stock
# @spec druide.preparation::recette-sans-etape-echoue
def test_l_ingrédient_vide_n_est_jamais_disponible() -> None:
    stock = GardeManger([])

    assert not stock.vérifier_disponibilité(INGRÉDIENT_VIDE)
    assert stock.récupérer_ingrédient(INGRÉDIENT_VIDE) is None


# @spec druide.preparation::conserve-le-surplus
def test_récupérer_rend_la_quantité_demandée_et_laisse_le_surplus() -> None:
    stock = GardeManger([_fraises(13)])

    assert stock.récupérer_ingrédient(_fraises(12)) == _fraises(12)
    assert stock.vérifier_disponibilité(_fraises(1))
    assert not stock.vérifier_disponibilité(_fraises(2))


# @spec infrastructure::garde-manger-respecte-le-stock
def test_récupérer_toute_la_quantité_retire_le_nom_du_stock() -> None:
    stock = GardeManger([_fraises(12)])

    stock.récupérer_ingrédient(_fraises(12))

    assert not stock.vérifier_disponibilité(_fraises(0))


# @spec infrastructure::garde-manger-respecte-le-stock
def test_récupérer_trop_ne_rend_rien_et_laisse_le_stock_intact() -> None:
    stock = GardeManger([_fraises(11)])

    assert stock.récupérer_ingrédient(_fraises(12)) is None
    assert stock.vérifier_disponibilité(_fraises(11))


# @spec infrastructure::garde-manger-respecte-le-stock
def test_stocker_un_nom_déjà_présent_additionne_les_quantités() -> None:
    stock = GardeManger([_fraises(2)])

    stock.stocker_ingrédient(_fraises(3))

    assert stock.vérifier_disponibilité(_fraises(5))
    assert not stock.vérifier_disponibilité(_fraises(6))


def _fraises(quantité: int) -> Ingrédient:
    return Ingrédient(nom="fraise", quantité=quantité)
