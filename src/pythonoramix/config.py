from fastapi import FastAPI

from pythonoramix.adapters.druide.garde_manger_adapter import GardeMangerAdapter
from pythonoramix.adapters.druide.thermomix_adapter import ThermomixAdapter
from pythonoramix.apix.potion_magique import créer_routeur_potion_magique
from pythonoramix.domain.druide.pythonoramix import Pythonoramix
from pythonoramix.domain.recette import RECETTE_DE_LA_POTION_MAGIQUE, Ingrédient
from pythonoramix.infrastructure.garde_manger import GardeManger
from pythonoramix.infrastructure.thermomix import Thermomix

POISSONS_FRAIS = Ingrédient(nom="poisson frais arrivant de Lutèce par char à bœufs", quantité=100)


# @spec api::une-seule-potion-par-demarrage
def créer_garde_manger() -> GardeManger:
    return GardeManger([POISSONS_FRAIS, *RECETTE_DE_LA_POTION_MAGIQUE.ingrédients])


def créer_application(garde_manger: GardeManger, thermomix: Thermomix) -> FastAPI:
    druide = Pythonoramix(GardeMangerAdapter(garde_manger), ThermomixAdapter(thermomix))
    application = FastAPI(title="Pythonoramix")
    application.include_router(créer_routeur_potion_magique(druide))
    return application
