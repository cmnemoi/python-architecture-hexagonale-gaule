from pythonoramix.domain.recette import Action, Ingrédient, Recette, Étape


def trèfles(quantité: int) -> Ingrédient:
    return Ingrédient(nom="trèfle à 4 feuilles", quantité=quantité)


def fraises(quantité: int) -> Ingrédient:
    return Ingrédient(nom="fraise", quantité=quantité)


def fraifles(quantité: int) -> Ingrédient:
    return Ingrédient(nom="fraifle", quantité=quantité)


def gui(quantité: int) -> Ingrédient:
    return Ingrédient(nom="feuille de gui coupée à la serpe d'or", quantité=quantité)


def lait_de_sanglier(quantité: int) -> Ingrédient:
    return Ingrédient(nom="once de lait de sanglier", quantité=quantité)


def curcuma(quantité: int) -> Ingrédient:
    return Ingrédient(nom="pincée de curcuma", quantité=quantité)


def lait_doré(quantité: int) -> Ingrédient:
    return Ingrédient(nom="lait doré", quantité=quantité)


def fraifles_au_gui(quantité: int) -> Ingrédient:
    return Ingrédient(nom="fraifle au gui", quantité=quantité)


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


def _recette_de_fraifles_au_gui(nom: str, fraifles_demandées: int, gui_demandé: int) -> Recette:
    return Recette(
        nom=nom,
        ingrédients=(trèfles(8), fraises(12), gui(1)),
        préchauffage=None,
        déroulé=(
            _MÉLANGER_LES_TRÈFLES_ET_LES_FRAISES,
            Étape(
                nom="Mélanger les fraifles et le gui",
                base=fraifles(fraifles_demandées),
                avec=gui(gui_demandé),
                action=Action.MÉLANGER,
                nom_ingrédient_obtenu="fraifle au gui",
            ),
        ),
    )


RECETTE_DES_FRAIFLES_AU_GUI = _recette_de_fraifles_au_gui(
    nom="Recette des fraifles au gui",
    fraifles_demandées=20,
    gui_demandé=1,
)

RECETTE_DES_FRAIFLES_AU_GUI_PAS_ASSEZ_DE_FRAIFLES = _recette_de_fraifles_au_gui(
    nom="Recette approximative des fraifles au gui",
    fraifles_demandées=21,
    gui_demandé=1,
)

RECETTE_DES_FRAIFLES_AU_GUI_PAS_ASSEZ_DE_GUI = _recette_de_fraifles_au_gui(
    nom="Recette gourmande des fraifles au gui",
    fraifles_demandées=20,
    gui_demandé=2,
)

RECETTE_DES_FRAIFLES_AU_GUI_ET_LAIT_DORÉ = Recette(
    nom="Recette des fraifles au gui et lait doré",
    ingrédients=(trèfles(8), fraises(12), gui(1), lait_de_sanglier(4), curcuma(10)),
    préchauffage=None,
    déroulé=(
        *RECETTE_DES_FRAIFLES_AU_GUI.déroulé,
        Étape(
            nom="Préparer le lait doré",
            base=lait_de_sanglier(4),
            avec=curcuma(10),
            action=Action.MÉLANGER,
            nom_ingrédient_obtenu="lait doré",
        ),
        Étape(
            nom="Mélanger les fraifles et le lait doré",
            base=fraifles_au_gui(21),
            avec=lait_doré(14),
            action=Action.MÉLANGER,
            nom_ingrédient_obtenu="fraifle au gui et lait doré",
        ),
    ),
)

RECETTE_SANS_ÉTAPE = Recette(nom="Recette sans étape", ingrédients=(), préchauffage=None, déroulé=())
