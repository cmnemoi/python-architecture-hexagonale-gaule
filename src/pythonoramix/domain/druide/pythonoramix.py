import time
from collections.abc import Iterable

from pythonoramix.domain.druide.cuiseur import AppareilDeCuisson
from pythonoramix.domain.druide.druide import Druide
from pythonoramix.domain.druide.stock import IngrédientManquantException, Stock
from pythonoramix.domain.recette import INGRÉDIENT_VIDE, Action, Ingrédient, Plat, Recette, Température, Étape

DÉLAI_ENTRE_DEUX_VÉRIFICATIONS_EN_SECONDES = 0.05


class Pythonoramix(Druide):
    def __init__(self, stock: Stock, cuiseur: AppareilDeCuisson) -> None:
        self._stock = stock
        self._cuiseur = cuiseur

    # @spec druide.preparation::sert-le-resultat-de-la-derniere-etape
    def préparer(self, recette_à_préparer: Recette) -> Plat:
        self._vérifier_disponibilité(recette_à_préparer.ingrédients)
        self._préchauffer(recette_à_préparer.préchauffage)

        dernier_ingrédient_obtenu = INGRÉDIENT_VIDE
        for étape in recette_à_préparer.déroulé:
            dernier_ingrédient_obtenu = (
                self._mélanger(étape) if étape.action is Action.MÉLANGER else self._bouillir(étape)
            )
            self._stock.stocker_ingrédient(dernier_ingrédient_obtenu)
        return self._servir(dernier_ingrédient_obtenu)

    # @spec druide.preparation::refuse-ingredient-manquant-au-depart
    def _vérifier_disponibilité(self, ingrédients: Iterable[Ingrédient]) -> None:
        if not all(self._stock.vérifier_disponibilité(ingrédient) for ingrédient in ingrédients):
            raise IngrédientManquantException()

    # @spec druide.preparation::prechauffe-avant-les-etapes
    def _préchauffer(self, température_souhaitée: Température | None) -> None:
        if température_souhaitée is None:
            return
        self._cuiseur.préchauffer(température_souhaitée)
        while self._cuiseur.vérifier_température().degré < température_souhaitée.degré:
            time.sleep(DÉLAI_ENTRE_DEUX_VÉRIFICATIONS_EN_SECONDES)

    # @spec druide.preparation::melange-additionne-les-quantites
    def _mélanger(self, étape: Étape) -> Ingrédient:
        if étape.avec is None:
            raise ValueError("Une étape de mélange doit avoir un ingrédient associé.")
        self._vérifier_disponibilité((étape.base, étape.avec))
        ingrédient_de_base = self._récupérer(étape.base)
        ingrédient_avec = self._récupérer(étape.avec)
        return Ingrédient(
            nom=étape.nom_ingrédient_obtenu,
            quantité=ingrédient_de_base.quantité + ingrédient_avec.quantité,
        )

    # @spec druide.preparation::ebullition-conserve-la-quantite
    def _bouillir(self, étape: Étape) -> Ingrédient:
        ingrédient_de_base = self._récupérer(étape.base)
        self._cuiseur.cuire(ingrédient_de_base, étape.nom_ingrédient_obtenu)
        return self._cuiseur.prélever()

    def _servir(self, ingrédient: Ingrédient) -> Plat:
        ingrédient_à_servir = self._récupérer(ingrédient)
        return Plat(nom=ingrédient_à_servir.nom, quantité=ingrédient_à_servir.quantité)

    def _récupérer(self, ingrédient: Ingrédient) -> Ingrédient:
        ingrédient_récupéré = self._stock.récupérer_ingrédient(ingrédient)
        if ingrédient_récupéré is None:
            raise IngrédientManquantException()
        return ingrédient_récupéré
