from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from pythonoramix.domain.druide.druide import Druide
from pythonoramix.domain.druide.stock import IngrédientManquantException
from pythonoramix.domain.recette import RECETTE_DE_LA_POTION_MAGIQUE, Plat


def créer_le_routeur_de_la_potion_magique(druide: Druide) -> APIRouter:
    routeur = APIRouter()

    # @spec api::prepare-la-potion-magique
    # Fonction synchrone : FastAPI l'exécute dans un thread, donc l'attente du préchauffage ne bloque pas le serveur.
    @routeur.post("/potion-magique")
    def préparer_la_potion_magique() -> Plat:
        try:
            return druide.préparer(RECETTE_DE_LA_POTION_MAGIQUE)
        # @spec api::ingredient-manquant-donne-409
        except IngrédientManquantException as ingrédient_manquant:
            raise HTTPException(HTTPStatus.CONFLICT, detail=str(ingrédient_manquant)) from ingrédient_manquant

    return routeur
