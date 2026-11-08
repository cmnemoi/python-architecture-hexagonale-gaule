from pythonoramix.domain.druide.cuiseur import AppareilDeCuisson
from pythonoramix.domain.recette import Ingrédient, Température
from pythonoramix.infrastructure import thermomix as infrastructure


class Thermomix(AppareilDeCuisson):
    def __init__(self, thermomix: infrastructure.Thermomix) -> None:
        self._thermomix = thermomix

    def préchauffer(self, température: Température) -> None:
        self._thermomix.préchauffer(température)

    def vérifier_température(self) -> Température:
        return self._thermomix.vérifier_température()

    def cuire(self, ingrédient_à_cuire: Ingrédient, nom_ingrédient_obtenu: str) -> None:
        self._thermomix.cuire(ingrédient_à_cuire, nom_ingrédient_obtenu)

    def prélever(self) -> Ingrédient:
        return self._thermomix.prélever()
