from typing import Protocol

from pythonoramix.domain.recette import Plat, Recette


class Druide(Protocol):
    def préparer(self, recette_à_préparer: Recette) -> Plat: ...
