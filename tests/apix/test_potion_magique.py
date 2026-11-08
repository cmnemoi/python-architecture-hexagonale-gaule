from http import HTTPStatus

from fastapi.testclient import TestClient

from pythonoramix.config import POISSONS_FRAIS, créer_l_application, créer_le_garde_manger
from pythonoramix.infrastructure.garde_manger_en_memoire import GardeMangerEnMémoire
from pythonoramix.infrastructure.thermomix_en_memoire import ThermomixEnMémoire
from pythonoramix.main import application


# @spec api::prepare-la-potion-magique
def test_un_serveur_qui_démarre_sert_la_potion_magique_en_json() -> None:
    client = _créer_le_client(créer_le_garde_manger())

    réponse = client.post("/potion-magique")

    assert réponse.status_code == HTTPStatus.OK
    assert réponse.json() == {"nom": "potion magique", "quantité": 35}


# @spec api::ingredient-manquant-donne-409
def test_un_garde_manger_vide_donne_une_erreur_409_avec_le_motif() -> None:
    client = _créer_le_client(GardeMangerEnMémoire([]))

    réponse = client.post("/potion-magique")

    assert réponse.status_code == HTTPStatus.CONFLICT
    assert réponse.json() == {"detail": "Un ingrédient est manquant pour la recette."}


# @spec api::une-seule-potion-par-demarrage
def test_une_seconde_potion_donne_une_erreur_409_et_laisse_les_poissons() -> None:
    garde_manger = créer_le_garde_manger()
    client = _créer_le_client(garde_manger)
    client.post("/potion-magique")

    réponse = client.post("/potion-magique")

    assert réponse.status_code == HTTPStatus.CONFLICT
    assert garde_manger.contenu == [POISSONS_FRAIS]


# @spec api::prepare-la-potion-magique
def test_l_application_de_production_est_câblée_avec_le_vrai_thermomix() -> None:
    réponse = TestClient(application).post("/potion-magique")

    assert réponse.status_code == HTTPStatus.OK


def _créer_le_client(garde_manger: GardeMangerEnMémoire) -> TestClient:
    return TestClient(créer_l_application(garde_manger, ThermomixEnMémoire(durée_d_un_palier_en_secondes=0.001)))
