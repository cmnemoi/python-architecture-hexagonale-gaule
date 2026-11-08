class GardeManger:
    def __init__(self, contenu: dict[str, int]) -> None:
        self.contenu = contenu

    def peut_fournir(self, nom: str, quantité: int) -> bool:
        return nom in self.contenu and self.contenu[nom] >= quantité

    def ranger(self, nom: str, quantité: int) -> None:
        self.contenu[nom] = self.contenu.get(nom, 0) + quantité

    def retirer(self, nom: str, quantité: int) -> None:
        if not self.peut_fournir(nom, quantité):
            raise QuantitéInsuffisanteException(nom)

        quantité_restante = self.contenu.pop(nom) - quantité
        if quantité_restante > 0:
            self.contenu[nom] = quantité_restante


class QuantitéInsuffisanteException(Exception):
    pass
