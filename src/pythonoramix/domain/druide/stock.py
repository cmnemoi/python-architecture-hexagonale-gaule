from typing import Protocol

from pythonoramix.domain.recette import Ingrédient


class IngrédientManquantException(Exception):
    def __init__(self) -> None:
        super().__init__("Un ingrédient est manquant pour la recette.")


class Stock(Protocol):
    def vérifier_disponibilité(self, ingrédient_recherché: Ingrédient) -> bool: ...

    def stocker_ingrédient(self, ingrédient: Ingrédient) -> None: ...

    def récupérer_ingrédient(self, ingrédient_recherché: Ingrédient) -> Ingrédient | None: ...
