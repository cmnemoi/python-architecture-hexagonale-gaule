from pythonoramix.domain.druide.cuiseur import AppareilDeCuisson, CuiseurNonPréchaufféException
from pythonoramix.domain.recette import INGRÉDIENT_VIDE, Ingrédient, Température
from pythonoramix.infrastructure import thermomix as infrastructure


# @spec adaptateurs::traduisent-le-thermomix
class Thermomix(AppareilDeCuisson):
    def __init__(self, thermomix: infrastructure.Thermomix) -> None:
        self._thermomix = thermomix

    def préchauffer(self, température: Température) -> None:
        self._thermomix.lancer_la_chauffe(température.degré)

    def vérifier_température(self) -> Température:
        return Température(degré=self._thermomix.lire_la_température())

    def cuire(self, ingrédient_à_cuire: Ingrédient, nom_ingrédient_obtenu: str) -> None:
        try:
            self._thermomix.cuire(nom_ingrédient_obtenu, ingrédient_à_cuire.quantité)
        except infrastructure.TempératureNonAtteinteException as température_non_atteinte:
            raise CuiseurNonPréchaufféException() from température_non_atteinte

    def prélever(self) -> Ingrédient:
        contenu_du_bol = self._thermomix.vider_le_bol()
        if contenu_du_bol is None:
            return INGRÉDIENT_VIDE
        return Ingrédient(nom=contenu_du_bol.nom, quantité=contenu_du_bol.quantité)
