# Pythonoramix

[![Continuous Integration](https://github.com/cmnemoi/python-architecture-hexagonale-gaule/actions/workflows/continuous_integration.yaml/badge.svg)](https://github.com/cmnemoi/python-architecture-hexagonale-gaule/actions/workflows/continuous_integration.yaml)
[![codecov](https://codecov.io/gh/cmnemoi/python-architecture-hexagonale-gaule/graph/badge.svg)](https://codecov.io/gh/cmnemoi/python-architecture-hexagonale-gaule)

Version Python et FastAPI du kata d'architecture hexagonale au pays des irréductibles développeurs.

Le kata reprend [Javanoramix](https://github.com/ambreperson/java-architecture-hexagonale-gaule) et [Dotnetoramix](https://github.com/swcraftLille/ArchihexaEnGaule).

## Structure

```text
src/pythonoramix/
├── domain/           Le cœur métier et ses ports, sans dépendance externe
├── apix/             L'API REST, qui appelle le port Druide
├── infrastructure/   Le garde-manger et le Thermomix en mémoire, qui implémentent les ports
├── config.py         L'assemblage de l'application
└── main.py           Le point d'entrée
```

## Lancer l'application

Le projet utilise [mise](https://mise.jdx.dev) pour installer ses outils et lancer ses tâches.

```bash
mise trust
mise install
mise run start
```

Dans un autre terminal :

```bash
mise run potion
```

La première requête sert la potion magique après 2,7 s de préchauffage. La requête suivante répond 409, car le garde-manger contient de quoi préparer une seule potion.

## Le kata

Le village veut savoir quand un plat est prêt, sans surveiller le druide. Ajoute cette notification sans lier le druide à la personne qui annonce la nouvelle.

## Licence

Ce projet est distribué sous la [licence Apache 2.0](LICENSE).

Il porte en Python [Javanoramix](https://github.com/ambreperson/java-architecture-hexagonale-gaule), distribué sous licence Apache 2.0. Il reprend aussi des éléments de [Dotnetoramix](https://github.com/swcraftLille/ArchihexaEnGaule), Copyright (c) 2026 Software Craft Lille, distribué sous licence MIT.
