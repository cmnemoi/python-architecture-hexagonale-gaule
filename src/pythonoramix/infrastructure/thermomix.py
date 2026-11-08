import time
from concurrent.futures import ThreadPoolExecutor

from pythonoramix.domain.druide.cuiseur import CuiseurNonPréchaufféException
from pythonoramix.domain.recette import INGRÉDIENT_VIDE, Ingrédient, Température


class Thermomix:
    def __init__(self, durée_d_un_palier_en_secondes: float = 0.3) -> None:
        self._durée_d_un_palier_en_secondes = durée_d_un_palier_en_secondes
        self._ingrédient_en_cuisson = INGRÉDIENT_VIDE
        self._température_actuelle = Température(degré=0)
        self._température_souhaitée = Température(degré=0)
        self._exécuteur = ThreadPoolExecutor(max_workers=1)

    # @spec cuiseur.thermomix::chauffe-progressivement
    def préchauffer(self, température: Température) -> None:
        self._température_souhaitée = température
        self._exécuteur.submit(self._chauffer_jusqu_à, température)

    def vérifier_température(self) -> Température:
        return self._température_actuelle

    # @spec cuiseur.thermomix::refuse-cuisson-hors-temperature
    def cuire(self, ingrédient_à_cuire: Ingrédient, nom_ingrédient_obtenu: str) -> None:
        if self._température_actuelle != self._température_souhaitée:
            raise CuiseurNonPréchaufféException()
        self._ingrédient_en_cuisson = Ingrédient(nom=nom_ingrédient_obtenu, quantité=ingrédient_à_cuire.quantité)

    def prélever(self) -> Ingrédient:
        ingrédient_prélevé = self._ingrédient_en_cuisson
        self._ingrédient_en_cuisson = INGRÉDIENT_VIDE
        return ingrédient_prélevé

    def _chauffer_jusqu_à(self, température: Température) -> None:
        while self._température_actuelle.degré < température.degré:
            time.sleep(self._durée_d_un_palier_en_secondes)
            self._température_actuelle = Température(degré=self._température_actuelle.degré + DEGRÉS_PAR_PALIER)


DEGRÉS_PAR_PALIER = 10
