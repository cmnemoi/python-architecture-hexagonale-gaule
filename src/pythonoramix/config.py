from fastapi import FastAPI

from pythonoramix.adapters.druide import garde_manger as garde_manger_adapté
from pythonoramix.adapters.druide import thermomix as thermomix_adapté
from pythonoramix.apix.potion_magique import créer_le_routeur_de_la_potion_magique
from pythonoramix.domain.druide.pythonoramix import Pythonoramix
from pythonoramix.domain.recette import RECETTE_DE_LA_POTION_MAGIQUE, Ingrédient
from pythonoramix.infrastructure.garde_manger import GardeManger
from pythonoramix.infrastructure.thermomix import Thermomix


def créer_l_application(garde_manger: GardeManger, thermomix: Thermomix) -> FastAPI:
    druide = Pythonoramix(garde_manger_adapté.GardeManger(garde_manger), thermomix_adapté.Thermomix(thermomix))
    application = FastAPI(title="Pythonoramix")
    application.include_router(créer_le_routeur_de_la_potion_magique(druide))
    return application


# @spec api::une-seule-potion-par-demarrage
def créer_le_garde_manger() -> GardeManger:
    return GardeManger([POISSONS_FRAIS, *RECETTE_DE_LA_POTION_MAGIQUE.ingrédients])


POISSONS_FRAIS = Ingrédient(nom="poisson frais arrivant de Lutèce par char à bœufs", quantité=100)
