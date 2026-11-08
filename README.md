# Pythonoramix

Version Python et FastAPI du kata d'architecture hexagonale au pays des irréductibles développeurs.

Le kata reprend [Javanoramix](https://github.com/ambreperson/java-architecture-hexagonale-gaule) et [Dotnetoramix](https://github.com/swcraftLille/ArchihexaEnGaule).

## Structure

```text
src/pythonoramix/
├── domain/           Le cœur métier et ses ports, sans dépendance externe
├── apix/             L'API REST, qui appelle le port Druide
├── adapters/         Les adaptateurs, qui relient les ports à l'infrastructure
├── infrastructure/   Le garde-manger et le Thermomix
├── config.py         L'assemblage de l'application
└── main.py           Le point d'entrée
```

## Lancer l'application

```bash
uv run uvicorn pythonoramix.main:application
```

Dans un autre terminal :

```bash
curl -X POST http://localhost:8000/potion-magique
```

La première requête sert la potion magique après 2,7 s de préchauffage. La requête suivante répond 409, car le garde-manger contient de quoi préparer une seule potion.

## Lancer les vérifications

```bash
uv run pytest
uv run ruff check .
uv run mypy
```

## Le kata

Le village veut savoir quand un plat est prêt, sans surveiller le druide. Ajoute cette notification sans lier le druide à la personne qui annonce la nouvelle.
