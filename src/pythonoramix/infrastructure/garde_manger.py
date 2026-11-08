from pythonoramix.domain.druide.stock import Stock
from pythonoramix.domain.recette import Ingrédient


# @spec infrastructure::garde-manger-respecte-le-stock
class GardeManger(Stock):
    def __init__(self, ingrédients: list[Ingrédient]) -> None:
        self._quantités = {ingrédient.nom: ingrédient.quantité for ingrédient in ingrédients}

    @property
    def contenu(self) -> list[Ingrédient]:
        return [Ingrédient(nom=nom, quantité=quantité) for nom, quantité in self._quantités.items()]

    def vérifier_disponibilité(self, ingrédient_recherché: Ingrédient) -> bool:
        return (
            ingrédient_recherché.nom in self._quantités
            and self._quantités[ingrédient_recherché.nom] >= ingrédient_recherché.quantité
        )

    def stocker_ingrédient(self, ingrédient: Ingrédient) -> None:
        self._quantités[ingrédient.nom] = self._quantités.get(ingrédient.nom, 0) + ingrédient.quantité

    # @spec druide.preparation::conserve-le-surplus
    def récupérer_ingrédient(self, ingrédient_recherché: Ingrédient) -> Ingrédient | None:
        if not self.vérifier_disponibilité(ingrédient_recherché):
            return None

        quantité_restante = self._quantités.pop(ingrédient_recherché.nom) - ingrédient_recherché.quantité
        if quantité_restante > 0:
            self._quantités[ingrédient_recherché.nom] = quantité_restante
        return ingrédient_recherché
