from pythonoramix.domain.druide.stock import Stock
from pythonoramix.domain.recette import Ingrédient
from pythonoramix.infrastructure import garde_manger as infrastructure


class GardeManger(Stock):
    def __init__(self, garde_manger: infrastructure.GardeManger) -> None:
        self._garde_manger = garde_manger

    def vérifier_disponibilité(self, ingrédient_recherché: Ingrédient) -> bool:
        return self._garde_manger.vérifier_disponibilité(ingrédient_recherché)

    def stocker_ingrédient(self, ingrédient: Ingrédient) -> None:
        self._garde_manger.stocker_ingrédient(ingrédient)

    def récupérer_ingrédient(self, ingrédient_recherché: Ingrédient) -> Ingrédient | None:
        return self._garde_manger.récupérer_ingrédient(ingrédient_recherché)
