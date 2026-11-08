from pythonoramix.domain.recette import Action, Ingrédient, Recette, Température, Étape


def recette_des_fraifles() -> Recette:
    return Recette(
        nom="Recette des fraifles",
        ingrédients=(trèfles(8), fraises(12)),
        préchauffage=None,
        déroulé=(_mélanger_les_trèfles_et_les_fraises(),),
    )


def recette_des_fraifles_au_gui() -> Recette:
    return _recette_de_fraifles_au_gui(
        nom="Recette des fraifles au gui",
        fraifles_demandées=20,
        gui_demandé=1,
    )


def recette_des_fraifles_au_gui_pas_assez_de_fraifles() -> Recette:
    return _recette_de_fraifles_au_gui(
        nom="Recette approximative des fraifles au gui",
        fraifles_demandées=21,
        gui_demandé=1,
    )


def recette_des_fraifles_au_gui_pas_assez_de_gui() -> Recette:
    return _recette_de_fraifles_au_gui(
        nom="Recette gourmande des fraifles au gui",
        fraifles_demandées=20,
        gui_demandé=2,
    )


def recette_des_fraifles_au_gui_et_lait_doré() -> Recette:
    return Recette(
        nom="Recette des fraifles au gui et lait doré",
        ingrédients=(trèfles(8), fraises(12), gui(1), lait_de_sanglier(4), curcuma(10)),
        préchauffage=None,
        déroulé=(
            *recette_des_fraifles_au_gui().déroulé,
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


def recette_des_fraises_bouillies() -> Recette:
    return Recette(
        nom="Recette des fraises bouillies",
        ingrédients=(fraises(12),),
        préchauffage=Température(degré=90),
        déroulé=(
            Étape(
                nom="Faire bouillir les fraises",
                base=fraises(12),
                avec=None,
                action=Action.BOUILLIR,
                nom_ingrédient_obtenu="fraise bouillie",
            ),
        ),
    )


def recette_des_fraifles_bouillies() -> Recette:
    return Recette(
        nom="Recette des fraifles bouillies",
        ingrédients=(trèfles(8), fraises(12)),
        préchauffage=Température(degré=90),
        déroulé=(
            _mélanger_les_trèfles_et_les_fraises(),
            Étape(
                nom="Faire bouillir les fraifles",
                base=fraifles(20),
                avec=None,
                action=Action.BOUILLIR,
                nom_ingrédient_obtenu="fraifle bouillie",
            ),
        ),
    )


def recette_sans_étape() -> Recette:
    return Recette(nom="Recette sans étape", ingrédients=(), préchauffage=None, déroulé=())


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


def _recette_de_fraifles_au_gui(nom: str, fraifles_demandées: int, gui_demandé: int) -> Recette:
    return Recette(
        nom=nom,
        ingrédients=(trèfles(8), fraises(12), gui(1)),
        préchauffage=None,
        déroulé=(
            _mélanger_les_trèfles_et_les_fraises(),
            Étape(
                nom="Mélanger les fraifles et le gui",
                base=fraifles(fraifles_demandées),
                avec=gui(gui_demandé),
                action=Action.MÉLANGER,
                nom_ingrédient_obtenu="fraifle au gui",
            ),
        ),
    )


def _mélanger_les_trèfles_et_les_fraises() -> Étape:
    return Étape(
        nom="Mélanger les trèfles et les fraises",
        base=trèfles(8),
        avec=fraises(12),
        action=Action.MÉLANGER,
        nom_ingrédient_obtenu="fraifle",
    )
