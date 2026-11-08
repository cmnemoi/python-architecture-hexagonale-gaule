from pythonoramix.domain.recette import Ingrédient


class GardeManger:
    def __init__(self, contenu: list[Ingrédient]) -> None:
        self.contenu = contenu

    def vérifier_disponibilité(self, ingrédient_recherché: Ingrédient) -> bool:
        return self._trouver_en_quantité_suffisante(ingrédient_recherché) is not None

    def stocker_ingrédient(self, ingrédient: Ingrédient) -> None:
        self.contenu.append(ingrédient)

    # @spec druide.preparation::conserve-le-surplus
    def récupérer_ingrédient(self, ingrédient_recherché: Ingrédient) -> Ingrédient | None:
        ingrédient_en_stock = self._trouver_en_quantité_suffisante(ingrédient_recherché)
        if ingrédient_en_stock is None:
            return None

        self.contenu.remove(ingrédient_en_stock)
        quantité_restante = ingrédient_en_stock.quantité - ingrédient_recherché.quantité
        if quantité_restante > 0:
            self.contenu.append(Ingrédient(nom=ingrédient_en_stock.nom, quantité=quantité_restante))
        return ingrédient_recherché

    def _trouver_en_quantité_suffisante(self, ingrédient_recherché: Ingrédient) -> Ingrédient | None:
        ingrédient_du_même_nom = next(
            (ingrédient for ingrédient in self.contenu if ingrédient.nom == ingrédient_recherché.nom),
            None,
        )
        if ingrédient_du_même_nom is None or ingrédient_du_même_nom.quantité < ingrédient_recherché.quantité:
            return None
        return ingrédient_du_même_nom
