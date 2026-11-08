# Pythonoramix

Version Python et FastAPI du kata d'architecture hexagonale au pays des irréductibles développeurs.

Le kata reprend [Javanoramix](https://github.com/ambreperson/java-architecture-hexagonale-gaule) et [Dotnetoramix](https://github.com/swcraftLille/ArchihexaEnGaule).

## Structure

```text
src/pythonoramix/
├── domain/           Le cœur métier et ses ports, sans dépendance externe
├── apix/             L'API REST, qui appelle le port Druide
├── adapters/         Les adaptateurs, qui traduisent entre les ports et l'infrastructure
├── infrastructure/   Le garde-manger et le Thermomix, qui ignorent le domaine
├── config.py         L'assemblage de l'application
└── main.py           Le point d'entrée
```

## Lancer l'application

Le projet utilise [mise](https://mise.jdx.dev) pour installer ses outils et lancer ses tasks.

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

## Les tasks

| Task | Rôle |
|---|---|
| `mise run install` | Installe les dépendances |
| `mise run start` | Démarre le serveur sur http://localhost:8000 |
| `mise run dev` | Démarre le serveur et le recharge à chaque modification |
| `mise run potion` | Demande une potion magique au serveur déjà démarré |
| `mise run docs` | Ouvre la documentation de l'API du serveur déjà démarré |
| `mise run test` | Lance tous les tests |
| `mise run test:rapide` | Lance les tests sans attente réelle du préchauffage |
| `mise run test:domaine` | Lance les tests du domaine |
| `mise run test:api` | Lance les tests de l'API |
| `mise run test:infrastructure` | Lance les tests de l'infrastructure |
| `mise run test:architecture` | Lance les tests d'architecture |
| `mise run lint` | Vérifie le style du code |
| `mise run format` | Formate le code et corrige ce que ruff sait corriger |
| `mise run format:check` | Vérifie le formatage sans modifier les fichiers |
| `mise run typecheck` | Vérifie les types |
| `mise run check` | Lance toutes les vérifications |

## Le kata

Le village veut savoir quand un plat est prêt, sans surveiller le druide. Ajoute cette notification sans lier le druide à la personne qui annonce la nouvelle.
