from pythonoramix.domain.druide.stock import Stock
from pythonoramix.domain.recette import Ingrédient
from pythonoramix.infrastructure import garde_manger as infrastructure


# @spec adaptateurs::traduisent-le-garde-manger
class GardeManger(Stock):
    def __init__(self, garde_manger: infrastructure.GardeManger) -> None:
        self._garde_manger = garde_manger

    def vérifier_disponibilité(self, ingrédient_recherché: Ingrédient) -> bool:
        return self._garde_manger.peut_fournir(ingrédient_recherché.nom, ingrédient_recherché.quantité)

    def stocker_ingrédient(self, ingrédient: Ingrédient) -> None:
        self._garde_manger.ranger(ingrédient.nom, ingrédient.quantité)

    # @spec druide.preparation::conserve-le-surplus
    def récupérer_ingrédient(self, ingrédient_recherché: Ingrédient) -> Ingrédient | None:
        try:
            self._garde_manger.retirer(ingrédient_recherché.nom, ingrédient_recherché.quantité)
        except infrastructure.QuantitéInsuffisanteException:
            return None
        return ingrédient_recherché
