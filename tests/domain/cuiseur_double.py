from pythonoramix.domain.druide.cuiseur import CuiseurNonPréchaufféException
from pythonoramix.domain.recette import INGRÉDIENT_VIDE, Ingrédient, Température


class CuiseurDouble:
    """Atteint la température à la deuxième vérification, pour garder le refus de cuire sans attente réelle."""

    def __init__(self) -> None:
        self.températures_demandées: list[Température] = []
        self.ingrédient_en_cuisson = INGRÉDIENT_VIDE
        self._température_actuelle = Température(degré=0)
        self._température_souhaitée = Température(degré=0)

    def préchauffer(self, température: Température) -> None:
        self.températures_demandées.append(température)
        self._température_souhaitée = température

    def vérifier_température(self) -> Température:
        température_vérifiée = self._température_actuelle
        self._température_actuelle = self._température_souhaitée
        return température_vérifiée

    def cuire(self, ingrédient_à_cuire: Ingrédient, nom_ingrédient_obtenu: str) -> None:
        if self._température_actuelle != self._température_souhaitée:
            raise CuiseurNonPréchaufféException()
        self.ingrédient_en_cuisson = Ingrédient(nom=nom_ingrédient_obtenu, quantité=ingrédient_à_cuire.quantité)

    def prélever(self) -> Ingrédient:
        ingrédient_prélevé = self.ingrédient_en_cuisson
        self.ingrédient_en_cuisson = INGRÉDIENT_VIDE
        return ingrédient_prélevé
