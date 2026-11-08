from fastapi import FastAPI

from pythonoramix.apix.potion_magique import créer_le_routeur_de_la_potion_magique
from pythonoramix.domain.druide.cuiseur import AppareilDeCuisson
from pythonoramix.domain.druide.pythonoramix import Pythonoramix
from pythonoramix.domain.druide.stock import Stock
from pythonoramix.domain.recette import RECETTE_DE_LA_POTION_MAGIQUE, Ingrédient
from pythonoramix.infrastructure.garde_manger_en_memoire import GardeMangerEnMémoire


def créer_l_application(stock: Stock, cuiseur: AppareilDeCuisson) -> FastAPI:
    application = FastAPI(title="Pythonoramix")
    application.include_router(créer_le_routeur_de_la_potion_magique(Pythonoramix(stock, cuiseur)))
    return application


# @spec api::une-seule-potion-par-demarrage
def créer_le_garde_manger() -> GardeMangerEnMémoire:
    return GardeMangerEnMémoire([POISSONS_FRAIS, *RECETTE_DE_LA_POTION_MAGIQUE.ingrédients])


POISSONS_FRAIS = Ingrédient(nom="poisson frais arrivant de Lutèce par char à bœufs", quantité=100)
