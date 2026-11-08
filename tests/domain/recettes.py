from pythonoramix.domain.recette import Action, Ingrédient, Recette, Étape


def trèfles(quantité: int) -> Ingrédient:
    return Ingrédient(nom="trèfle à 4 feuilles", quantité=quantité)


def fraises(quantité: int) -> Ingrédient:
    return Ingrédient(nom="fraise", quantité=quantité)


def fraifles(quantité: int) -> Ingrédient:
    return Ingrédient(nom="fraifle", quantité=quantité)


_MÉLANGER_LES_TRÈFLES_ET_LES_FRAISES = Étape(
    nom="Mélanger les trèfles et les fraises",
    base=trèfles(8),
    avec=fraises(12),
    action=Action.MÉLANGER,
    nom_ingrédient_obtenu="fraifle",
)

RECETTE_DES_FRAIFLES = Recette(
    nom="Recette des fraifles",
    ingrédients=(trèfles(8), fraises(12)),
    préchauffage=None,
    déroulé=(_MÉLANGER_LES_TRÈFLES_ET_LES_FRAISES,),
)
