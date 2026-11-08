from typing import Protocol

from pythonoramix.domain.recette import Ingrédient, Température


class CuiseurNonPréchaufféException(Exception):
    pass


class AppareilDeCuisson(Protocol):
    def préchauffer(self, température: Température) -> None: ...

    def vérifier_température(self) -> Température: ...

    def cuire(self, ingrédient_à_cuire: Ingrédient, nom_ingrédient_obtenu: str) -> None: ...

    def prélever(self) -> Ingrédient: ...
