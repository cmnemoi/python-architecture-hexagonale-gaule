from collections.abc import Callable

import pytest

from pythonoramix.adapters.druide import garde_manger as garde_manger_adapté
from pythonoramix.domain.druide.stock import Stock
from pythonoramix.domain.recette import INGRÉDIENT_VIDE, Ingrédient
from pythonoramix.infrastructure.garde_manger import GardeManger
from tests.domain.stock_double import StockDouble

type CréateurDeStock = Callable[[list[Ingrédient]], Stock]


# @spec adaptateurs::traduisent-le-garde-manger
def test_vérifier_disponibilité_accepte_la_quantité_exacte_et_refuse_une_de_plus(
    créer_le_stock: CréateurDeStock,
) -> None:
    stock = créer_le_stock([_fraises(12)])

    assert stock.vérifier_disponibilité(_fraises(12))
    assert not stock.vérifier_disponibilité(_fraises(13))


# @spec adaptateurs::traduisent-le-garde-manger
def test_un_ingrédient_absent_n_est_ni_disponible_ni_récupérable(créer_le_stock: CréateurDeStock) -> None:
    stock = créer_le_stock([])

    assert not stock.vérifier_disponibilité(_fraises(1))
    assert stock.récupérer_ingrédient(_fraises(1)) is None


# @spec adaptateurs::traduisent-le-garde-manger
# @spec druide.preparation::recette-sans-etape-echoue
def test_l_ingrédient_vide_n_est_jamais_disponible(créer_le_stock: CréateurDeStock) -> None:
    stock = créer_le_stock([])

    assert not stock.vérifier_disponibilité(INGRÉDIENT_VIDE)
    assert stock.récupérer_ingrédient(INGRÉDIENT_VIDE) is None


# @spec druide.preparation::conserve-le-surplus
def test_récupérer_rend_la_quantité_demandée_et_laisse_le_surplus(créer_le_stock: CréateurDeStock) -> None:
    stock = créer_le_stock([_fraises(13)])

    assert stock.récupérer_ingrédient(_fraises(12)) == _fraises(12)
    assert stock.vérifier_disponibilité(_fraises(1))
    assert not stock.vérifier_disponibilité(_fraises(2))


# @spec adaptateurs::traduisent-le-garde-manger
def test_récupérer_toute_la_quantité_retire_le_nom_du_stock(créer_le_stock: CréateurDeStock) -> None:
    stock = créer_le_stock([_fraises(12)])

    stock.récupérer_ingrédient(_fraises(12))

    assert not stock.vérifier_disponibilité(_fraises(0))


# @spec adaptateurs::traduisent-le-garde-manger
def test_récupérer_trop_ne_rend_rien_et_laisse_le_stock_intact(créer_le_stock: CréateurDeStock) -> None:
    stock = créer_le_stock([_fraises(11)])

    assert stock.récupérer_ingrédient(_fraises(12)) is None
    assert stock.vérifier_disponibilité(_fraises(11))


# @spec adaptateurs::traduisent-le-garde-manger
def test_stocker_un_nom_déjà_présent_additionne_les_quantités(créer_le_stock: CréateurDeStock) -> None:
    stock = créer_le_stock([_fraises(2)])

    stock.stocker_ingrédient(_fraises(3))

    assert stock.vérifier_disponibilité(_fraises(5))
    assert not stock.vérifier_disponibilité(_fraises(6))


@pytest.fixture(params=["garde-manger réel", "double de test"])
def créer_le_stock(request: pytest.FixtureRequest) -> CréateurDeStock:
    return _garde_manger_adapté if request.param == "garde-manger réel" else StockDouble


def _garde_manger_adapté(ingrédients: list[Ingrédient]) -> Stock:
    quantités = {ingrédient.nom: ingrédient.quantité for ingrédient in ingrédients}
    return garde_manger_adapté.GardeManger(GardeManger(quantités))


def _fraises(quantité: int) -> Ingrédient:
    return Ingrédient(nom="fraise", quantité=quantité)
