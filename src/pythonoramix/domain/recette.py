from dataclasses import dataclass
from enum import Enum, auto


class Action(Enum):
    MÉLANGER = auto()
    BOUILLIR = auto()


@dataclass(frozen=True)
class Ingrédient:
    nom: str
    quantité: int


INGRÉDIENT_VIDE = Ingrédient(nom="", quantité=0)


@dataclass(frozen=True)
class Plat:
    nom: str
    quantité: int


@dataclass(frozen=True)
class Température:
    degré: int


@dataclass(frozen=True)
class Étape:
    nom: str
    base: Ingrédient
    avec: Ingrédient | None
    action: Action
    nom_ingrédient_obtenu: str


@dataclass(frozen=True)
class Recette:
    nom: str
    ingrédients: tuple[Ingrédient, ...]
    préchauffage: Température | None
    déroulé: tuple[Étape, ...]


_TRÈFLES = Ingrédient(nom="trèfle à 4 feuilles", quantité=8)
_FRAISES = Ingrédient(nom="fraise", quantité=12)
_LAIT_DE_SANGLIER = Ingrédient(nom="once de lait de sanglier", quantité=4)
_CURCUMA = Ingrédient(nom="pincée de curcuma", quantité=10)
_GUI = Ingrédient(nom="feuille de gui coupée à la serpe d'or", quantité=1)

# @spec recette::potion-magique
RECETTE_DE_LA_POTION_MAGIQUE = Recette(
    nom="Recette de la potion magique",
    ingrédients=(_TRÈFLES, _FRAISES, _LAIT_DE_SANGLIER, _CURCUMA, _GUI),
    préchauffage=Température(degré=90),
    déroulé=(
        Étape(
            nom="Mélanger les trèfles et les fraises",
            base=_TRÈFLES,
            avec=_FRAISES,
            action=Action.MÉLANGER,
            nom_ingrédient_obtenu="fraifle",
        ),
        Étape(
            nom="Préparer le lait doré",
            base=_LAIT_DE_SANGLIER,
            avec=_CURCUMA,
            action=Action.MÉLANGER,
            nom_ingrédient_obtenu="lait doré",
        ),
        Étape(
            nom="Faire bouillir les fraifles",
            base=Ingrédient(nom="fraifle", quantité=20),
            avec=None,
            action=Action.BOUILLIR,
            nom_ingrédient_obtenu="fraifle bouillie",
        ),
        Étape(
            nom="Ajouter le gui",
            base=Ingrédient(nom="fraifle bouillie", quantité=20),
            avec=_GUI,
            action=Action.MÉLANGER,
            nom_ingrédient_obtenu="fraifle au gui",
        ),
        Étape(
            nom="Verser le lait doré",
            base=Ingrédient(nom="fraifle au gui", quantité=21),
            avec=Ingrédient(nom="lait doré", quantité=14),
            action=Action.MÉLANGER,
            nom_ingrédient_obtenu="précurseur de potion magique",
        ),
        Étape(
            nom="Faire bouillir le précurseur",
            base=Ingrédient(nom="précurseur de potion magique", quantité=35),
            avec=None,
            action=Action.BOUILLIR,
            nom_ingrédient_obtenu="potion magique",
        ),
    ),
)
