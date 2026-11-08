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
