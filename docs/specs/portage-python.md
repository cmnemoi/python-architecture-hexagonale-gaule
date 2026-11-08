# Pythonoramix : portage Python du kata

## Why

Le kata existe en Java (Javanoramix) et en .NET (Dotnetoramix).
Des développeurs Python doivent pouvoir le pratiquer dans leur langage.
Ce portage est le point de départ du kata : il ne contient aucune notification.

## Scope

- Préparer une recette avec le druide.
- Exposer la préparation de la potion magique par une API FastAPI.
- Vérifier les règles de l'architecture hexagonale par des tests.

## Required constraints

- Le dépôt Java, branche `main`, est la référence, sauf décision écrite dans cette spec. Le dépôt .NET sert uniquement de complément.
- La branche `main` reste le point de départ. Les participants ajoutent le barde en direct pendant le kata.
- Le vocabulaire reste celui du kata, en français et avec les accents (`préparer`, `Étape`).
- Le code a deux zones, comme la version .NET : le domaine et l'infrastructure. L'infrastructure implémente directement les ports du domaine.
- Les tests du domaine n'attendent pas le préchauffage réel. Leur cuiseur garde toutefois le refus de cuire hors température.

## Example mapping

Chaque règle porte ses exemples, et la colonne `ZOMBIES` donne le risque couvert par chaque exemple.
La colonne `Origine` donne la source de chaque exemple :

- **Test Java** : test de `JavanoramixTest` ou de `ArchitectureHexagonaleTest`.
- **Test .NET** : test de `DotnetoramixTest`.
- **Code Java** ou **Code .NET** : le comportement vient du code, car aucun test ne le couvre.
- **Décision** : le comportement s'écarte volontairement de la référence.

Quand un test d'origine vérifie moins que l'exemple, la colonne indique le code qui fonde le reste.

Recettes des exemples, reprises des constantes de `JavanoramixTest` :

| Recette | Déroulé |
|---|---|
| Fraifles | 8 trèfles + 12 fraises → 20 fraifles |
| Fraifles au gui | Fraifles, puis 20 fraifles + 1 gui → 21 fraifles au gui |
| Fraifles au gui approximatives | Fraifles, puis 21 fraifles + 1 gui → 22 fraifles au gui |
| Fraifles au gui et lait doré | Fraifles au gui, 4 onces de lait + 10 pincées de curcuma → 14 laits dorés, puis 21 + 14 → 35 unités |
| Fraises bouillies | 90 °C, puis 12 fraises → 12 fraises bouillies |
| Fraifles bouillies | 90 °C, Fraifles, puis 20 fraifles → 20 fraifles bouillies |

### Règle 1 : le plat vient de la dernière étape

`{#druide.preparation::sert-le-resultat-de-la-derniere-etape}`

Le druide exécute les étapes dans l'ordre.
Chaque résultat retourne dans le stock et peut servir à l'étape suivante.
Le plat porte le nom et la quantité du résultat de la dernière étape.
Le druide retire ce résultat du stock quand il sert le plat.

| ZOMBIES | Étant donné | Quand | Alors | Origine |
|---|---|---|---|---|
| Simple, One | 12 fraises et 8 trèfles | le druide prépare des fraifles | il sert 20 fraifles et le stock est vide | Test Java `préparerDesFraifles`, test .NET `PreparerDesFraifles` |
| Many | 12 fraises, 8 trèfles et 1 gui | le druide prépare des fraifles au gui | il sert 21 fraifles au gui et le stock est vide | Test Java `préparerDesFraiflesAuGui` |
| Many | les ingrédients de la potion | le druide prépare la potion magique | il sert 35 potions magiques, le stock et le cuiseur sont vides | Test Java `préparerDeLaPotionMagique` |

### Règle 2 : un mélange additionne les quantités

`{#druide.preparation::melange-additionne-les-quantites}`

Le mélange consomme les deux ingrédients de l'étape.
Le résultat porte le nom prévu par l'étape et la somme des quantités consommées.

| ZOMBIES | Étant donné | Quand | Alors | Origine |
|---|---|---|---|---|
| Many | les ingrédients des fraifles au gui et du lait doré | le druide prépare cette recette | il sert 35 unités de `fraifle au gui et lait doré` | Test Java `préparerDesFraiflesAuGuiAvecDuLaitDoré` |

### Règle 3 : une ébullition conserve la quantité

`{#druide.preparation::ebullition-conserve-la-quantite}`

L'ébullition consomme l'ingrédient de base et donne le résultat prévu, en même quantité.
Après le prélèvement, le cuiseur est vide.

| ZOMBIES | Étant donné | Quand | Alors | Origine |
|---|---|---|---|---|
| One | 12 fraises | le druide prépare des fraises bouillies | il sert 12 fraises bouillies, le stock et le cuiseur sont vides | Test Java `préparerDesFraisesBouillies` |
| Many | 12 fraises et 8 trèfles | le druide prépare des fraifles bouillies | il sert 20 fraifles bouillies, le stock et le cuiseur sont vides | Test Java `préparerDesFraiflesBouillies` |

### Règle 4 : un ingrédient manquant bloque la recette dès le départ

`{#druide.preparation::refuse-ingredient-manquant-au-depart}`

Un ingrédient de la recette est manquant s'il est absent ou si sa quantité est insuffisante.
La préparation échoue alors avec `IngrédientManquantException`.
Le stock ne change pas et le cuiseur ne préchauffe pas.

| ZOMBIES | Étant donné | Quand | Alors | Origine |
|---|---|---|---|---|
| Zero | 12 fraises, sans trèfle | le druide prépare des fraifles | `IngrédientManquantException` et le stock reste intact | Test Java `préparerDesFraiflesIngrédientAbsent`, test .NET `PreparerDesFraiflesIngredientAbsent`. Stock intact : code Java `vérifierDisponibilitéIngrédients` |
| Boundary | 11 fraises et 8 trèfles | le druide prépare des fraifles | `IngrédientManquantException` et le stock reste intact | Test Java `préparerDesFraiflesIngrédientManquant`. Stock intact : code Java `vérifierDisponibilitéIngrédients` |
| Exceptional | 12 fraises sans trèfle, recette à 90 °C | le druide prépare des fraifles bouillies | `IngrédientManquantException` et le cuiseur ne reçoit aucune demande de préchauffage | Code Java `préparer` : la vérification précède le préchauffage |

### Règle 5 : un manque en cours de recette ne rend pas le stock

`{#druide.preparation::echoue-sans-restitution-en-cours-de-recette}`

Si une étape demande plus que le stock ne contient, la préparation échoue avec `IngrédientManquantException`.
Les ingrédients des étapes précédentes restent consommés.

| ZOMBIES | Étant donné | Quand | Alors | Origine |
|---|---|---|---|---|
| Exceptional, Boundary | 12 fraises, 8 trèfles et 1 gui | le druide prépare les fraifles au gui approximatives | `IngrédientManquantException`, et le stock contient 20 fraifles et 1 gui | Test Java `préparerDesFraiflesAuGuiPasAssezDeFraifles`. État du stock : code Java `mélanger` |
| Boundary | 12 fraises, 8 trèfles et 1 gui | le druide prépare une recette qui demande 2 gui à l'étape 2 | `IngrédientManquantException`, et le stock contient 20 fraifles et 1 gui | Code Java `mélanger` : la vérification des deux ingrédients précède leur retrait |

### Règle 6 : le surplus reste dans le stock

`{#druide.preparation::conserve-le-surplus}`

Une étape consomme uniquement la quantité prévue par la recette.
Le surplus reste dans le stock et ne compte pas dans le plat.

| ZOMBIES | Étant donné | Quand | Alors | Origine |
|---|---|---|---|---|
| Boundary | 13 fraises et 8 trèfles | le druide prépare des fraifles | il sert 20 fraifles et il reste 1 fraise | Test Java `préparerDesFraiflesSurplusIngrédients`. La version .NET sert la quantité complète et ne fait pas référence |

### Règle 7 : le préchauffage précède les étapes

`{#druide.preparation::prechauffe-avant-les-etapes}`

Si la recette demande un préchauffage, le druide attend la température avant la première étape.
Si la recette ne demande pas de préchauffage, le druide ne préchauffe pas le cuiseur.

| ZOMBIES | Étant donné | Quand | Alors | Origine |
|---|---|---|---|---|
| Simple | 12 fraises et un cuiseur qui refuse de cuire hors température | le druide prépare des fraises bouillies | il sert le plat, sans erreur du cuiseur | Test Java `préparerDesFraisesBouillies`, avec `CuiseurDouble` hérité de `Thermomix` |
| Zero | 12 fraises et 8 trèfles | le druide prépare des fraifles, sans préchauffage | le cuiseur ne reçoit aucune demande de préchauffage | Code Java `Javanoramix.préchauffer` |

### Règle 8 : une recette sans étape ne donne aucun plat

`{#druide.preparation::recette-sans-etape-echoue}`

La préparation échoue avec `IngrédientManquantException`.

| ZOMBIES | Étant donné | Quand | Alors | Origine |
|---|---|---|---|---|
| Zero | une recette sans étape | le druide la prépare | `IngrédientManquantException` | Code Java `servir`, qui échoue déjà. Décision : le type d'erreur remplace `NoSuchElementException` |

### Règle 9 : la préparation reste silencieuse

`{#druide.preparation::reste-silencieuse}`

Le domaine n'écrit rien sur la sortie standard, contrairement à la version Java.

| ZOMBIES | Étant donné | Quand | Alors | Origine |
|---|---|---|---|---|
| Interface | les ingrédients de la potion | le druide prépare la potion magique | la sortie standard reste vide | Décision : le retrait des traces de `Javanoramix` |

### Règle 10 : le Thermomix chauffe progressivement

`{#cuiseur.thermomix::chauffe-progressivement}`

Le Thermomix gagne 10 °C toutes les 300 ms, sans bloquer l'appelant.
Il atteint 90 °C en 2,7 s.

| ZOMBIES | Étant donné | Quand | Alors | Origine |
|---|---|---|---|---|
| Simple | un Thermomix à 0 °C | la chauffe à 90 °C vient de démarrer | la température reste sous 90 °C | Code Java `Thermomix.préchauffer` |
| Boundary | un Thermomix en préchauffage vers 90 °C | 2,7 s sont passées | la température est 90 °C et ne dépasse pas cette valeur | Code Java `Thermomix.préchauffer` |

### Règle 11 : le Thermomix refuse de cuire hors température

`{#cuiseur.thermomix::refuse-cuisson-hors-temperature}`

Si la température actuelle diffère de la température demandée, la cuisson échoue avec `CuiseurNonPréchaufféException`.

| ZOMBIES | Étant donné | Quand | Alors | Origine |
|---|---|---|---|---|
| Exceptional | un Thermomix en préchauffage | le druide cuit | `CuiseurNonPréchaufféException` | Code Java `Thermomix.cuire`. |
| Simple | un Thermomix à la température demandée | le druide cuit puis prélève | le résultat sort avec son nouveau nom et la même quantité | Code Java `Thermomix.cuire` et `Thermomix.prélever` |
| Zero | un Thermomix déjà prélevé | le druide prélève encore | il reçoit l'ingrédient vide | Code Java `Thermomix.prélever`. |

### Règle 12 : la recette de la potion magique reste celle du kata

`{#recette::potion-magique}`

La recette demande 90 °C et ces ingrédients :
8 trèfles à 4 feuilles, 12 fraises, 4 onces de lait de sanglier, 10 pincées de curcuma, 1 feuille de gui.

| Étape | Action | Base | Avec | Résultat |
|---|---|---|---|---|
| Mélanger les trèfles et les fraises | mélanger | trèfle à 4 feuilles (8) | fraise (12) | fraifle |
| Préparer le lait doré | mélanger | once de lait de sanglier (4) | pincée de curcuma (10) | lait doré |
| Faire bouillir les fraifles | bouillir | fraifle (20) | | fraifle bouillie |
| Ajouter le gui | mélanger | fraifle bouillie (20) | feuille de gui coupée à la serpe d'or (1) | fraifle au gui |
| Verser le lait doré | mélanger | fraifle au gui (21) | lait doré (14) | précurseur de potion magique |
| Faire bouillir le précurseur | bouillir | précurseur de potion magique (35) | | potion magique |

Origine : code Java `Recette.RECETTE_DE_LA_POTION_MAGIQUE` et code .NET `Recette.PotionMagique`. Le test de la règle 1 couvre cette recette.

### Règle 13 : la requête prépare la potion magique

`{#api::prepare-la-potion-magique}`

`POST /potion-magique` prépare la potion magique.
Si la préparation réussit, la réponse a le statut 200 et le corps JSON `{"nom": "potion magique", "quantité": 35}`.

| ZOMBIES | Étant donné | Quand | Alors | Origine |
|---|---|---|---|---|
| Interface | un serveur qui vient de démarrer | un client envoie `POST /potion-magique` | la réponse a le statut 200 et décrit 35 potions magiques | Code .NET `Program.cs`, qui renvoie le plat. Décision : la clé `quantité` garde son accent |

### Règle 14 : un ingrédient manquant est une erreur prévisible

`{#api::ingredient-manquant-donne-409}`

Un ingrédient manquant est une règle métier, pas une panne.
La réponse a donc le statut 409 et le corps JSON `{"detail": "Un ingrédient est manquant pour la recette."}`.

| ZOMBIES | Étant donné | Quand | Alors | Origine |
|---|---|---|---|---|
| Exceptional | un garde-manger sans les ingrédients de la potion | un client envoie `POST /potion-magique` | la réponse a le statut 409 et donne le motif | Décision : Java répond 500. Motif : code .NET `IngredientManquantException` |

### Règle 15 : le garde-manger permet une seule potion

`{#api::une-seule-potion-par-demarrage}`

Le garde-manger démarre avec les quantités exactes d'une potion et 100 poissons frais de Lutèce.
Une seconde requête échoue donc avec le statut 409.
Le stock ne change pas pendant cet échec.

| ZOMBIES | Étant donné | Quand | Alors | Origine |
|---|---|---|---|---|
| Many | un serveur qui a déjà préparé une potion | un client renvoie `POST /potion-magique` | la réponse a le statut 409 et il reste 100 poissons dans le garde-manger | Code Java `JavanoramixConfiguration`. Statut : décision de la règle 14 |

### Règle 16 : l'architecture protège le domaine

`{#architecture::domaine-isole}`

Le domaine importe uniquement le domaine et la bibliothèque standard.

`{#architecture::api-depend-du-domaine}`

L'API importe uniquement le domaine, FastAPI et la bibliothèque standard.

`{#architecture::infrastructure-implemente-les-ports}`

L'infrastructure importe uniquement le domaine et la bibliothèque standard.

| ZOMBIES | Étant donné | Quand | Alors | Origine |
|---|---|---|---|---|
| Interface | un module du domaine qui importe l'infrastructure | les tests d'architecture tournent | ils échouent | Test Java `domainNeDoitDépendreQueDuDomain` |
| Interface | un module du domaine qui importe FastAPI | les tests d'architecture tournent | ils échouent | Test Java `domainNeDoitPasUtiliserSpring`, transposé à FastAPI |
| Interface | un module de l'API qui importe l'infrastructure | les tests d'architecture tournent | ils échouent | Test Java `apixNeDoitUtiliserQueDomainOuSpring`, transposé à FastAPI |
| Interface | un module de l'infrastructure qui importe l'API | les tests d'architecture tournent | ils échouent | Test Java `adaptersDoitDependreDeDomainInfrastructureEtSpring`, transposé à l'infrastructure |

Chaque règle d'architecture doit devenir rouge une fois sur un import interdit ajouté à la main.

### Règle 17 : le garde-manger en mémoire respecte le port du stock

`{#infrastructure::garde-manger-respecte-le-stock}`

Le garde-manger en mémoire implémente directement le port `Stock`.

| ZOMBIES | Étant donné | Quand | Alors | Origine |
|---|---|---|---|---|
| Boundary | 12 fraises | le druide vérifie 12 fraises, puis 13 fraises | la première vérification réussit et la seconde échoue | Code Java `GardeManger.vérifierDisponibilité` |
| Zero | un stock sans fraise | le druide vérifie puis récupère des fraises | il n'en trouve pas et ne reçoit rien | Code Java `GardeManger.récupérerIngrédient` |
| Zero | un stock vide | le druide récupère l'ingrédient vide | il ne reçoit rien | Code Java `GardeManger.vérifierDisponibilité` : un nom absent n'est jamais disponible, même en quantité 0 |
| Simple | 13 fraises | le druide récupère 12 fraises | il reçoit 12 fraises et il en reste 1 | Code Java `GardeManger.récupérerIngrédient` |
| Boundary | 12 fraises | le druide récupère 12 fraises | le nom `fraise` n'est plus dans le stock | Code Java `GardeManger.récupérerIngrédient` |
| Exceptional | 11 fraises | le druide récupère 12 fraises | il ne reçoit rien et les 11 fraises restent | Code Java `GardeManger.récupérerIngrédient` |
| Many | 2 fraises en stock | le druide stocke 3 fraises | le stock contient 5 fraises | Décision : le garde-manger fusionne les quantités |

## Out of scope

- Toute notification : les participants l'ajoutent en direct pendant le kata.
- La persistance : le garde-manger reste en mémoire et se remplit à chaque démarrage.
- Les requêtes simultanées : aucune protection du stock partagé. Le résultat de deux préparations simultanées reste indéfini.
- Les températures qui ne sont pas des multiples de 10 °C : le Thermomix dépasse la cible, puis refuse de cuire, comme en Java.
- La validation des recettes, par exemple un mélange sans second ingrédient : les recettes sont écrites dans le code.
- Le garde-manger vide à chaque requête de la version .NET : le garde-manger reste unique, comme en Java.
