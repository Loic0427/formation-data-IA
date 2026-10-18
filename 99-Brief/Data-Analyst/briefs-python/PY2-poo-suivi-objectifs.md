# Brief PY2 — Les objectifs 2024 des magasins, en objets

## Informations

| Critère | Valeur |
|---------|--------|
| **Quand** | Fin du dossier [02-POO](../../../01-Fondamentaux/Python/02-POO/), après les 5 séries d'exercices |
| **Durée** | Une demi-journée (3 h 30) |
| **Niveau** | 1 — **imiter** : un module exemple complet et un squelette à remplir sont fournis |
| **Modalité** | Individuel |
| **Outils** | Python 3.10+ sans rien installer, Mermaid (dans un fichier Markdown), Git/GitHub |
| **Kit** | [`kit-PY2/`](kit-PY2/) : `suivi_stock_exemple.py` (l'exemple), `diagramme_stock.md`, `indicateurs_stock.md`, `suivi_objectifs_squelette.py` (ton squelette), `donnees_objectifs.py` (tes données) |

## Ta mission en une phrase

Le responsable BI a écrit un petit programme orienté objet qui suit le **stock d'un entrepôt**. Tu écris le même programme, classe pour classe, pour suivre les **objectifs de chiffre d'affaires 2024** des sept points de vente, puis tu publies ton travail.

## Ce que tu rends

Un dépôt GitHub public qui contient :

- `suivi_objectifs.py` : ton module, complet, qui tourne avec `python suivi_objectifs.py` ;
- `donnees_objectifs.py` : les données, copiées du kit ;
- `diagramme_objectifs.md` : le diagramme de tes classes, en Mermaid ;
- `indicateurs_objectifs.md` : la fiche de tes trois indicateurs ;
- `README.md` : titre, ce que fait le programme, comment le lancer, la sortie collée, ton nom.

Le fichier exemple ne doit **pas** être dans ton dépôt.

## Le contexte

La direction de NordRetail a fixé à chaque magasin un objectif de chiffre d'affaires pour chaque mois de 2024. Fin d'année, la contrôleuse de gestion veut savoir : qui a atteint ses objectifs, à quel pourcentage, et quels mois ? Le responsable BI veut un programme construit **exactement comme son programme de stock**, parce qu'il en connaît chaque pièce.

## La correspondance entre l'exemple et ton programme

Chaque classe de l'exemple a son équivalent. Tu n'as rien à inventer : tu adaptes.

- `StockInsuffisant` (une exception avec des informations dedans) → `ObjectifInvalide` : un objectif refusé, avec la ville et le mois.
- `Mouvement` (un enregistrement daté, impossible à modifier) → `Realisation` : le CA réel d'une ville pour un mois.
- `Produit` (une entité dont le stock est protégé et modifié uniquement par des méthodes qui vérifient) → `Magasin` : ses objectifs sont protégés, `fixer_objectif` vérifie le mois et le montant, et son taux d'atteinte est calculé, jamais stocké.
- `StockTotal`, `ValeurStock`, `NbRuptures` (trois indicateurs qui respectent le même contrat `Indicateur`) → `CaTotal`, `TauxGlobal`, `NbMagasinsEnRetard`.
- `Entrepot` (contient les produits, applique les mouvements, écrit le rapport) → `Reseau` : contient les magasins, charge les données, écrit le rapport.

## Les étapes

### Étape 1 — Installe-toi (15 min)

1. Copie `kit-PY2` sur ta machine, renomme-le `suivi-objectifs`, crée le dépôt GitHub public.
2. Lance `python suivi_stock_exemple.py` et lis le rapport.

**C'est bon quand** : tu vois « Mouvements refusés : 2 » en bas du rapport de l'exemple.

### Étape 2 — Lis l'exemple avec la correspondance sous les yeux (30 min)

Lis `suivi_stock_exemple.py` une classe à la fois, avec `diagramme_stock.md` à côté. Pour chaque classe, relis la ligne de correspondance ci-dessus et repère : où est la validation ? où est la propriété calculée ? où l'exception est-elle capturée sans arrêter le programme ?

**C'est bon quand** : tu sais dire pourquoi `valeur` est une `@property` et pas un attribut dans `Produit`.

### Étape 3 — Remplis le squelette, classe par classe (1 h 45)

Renomme `suivi_objectifs_squelette.py` en `suivi_objectifs.py`. Les classes, les méthodes et leurs noms sont déjà là ; chaque `...` a un commentaire qui dit quoi écrire. Remplis dans cet ordre, et teste à chaque étape dans un terminal Python :

1. `ObjectifInvalide`. Test : `raise ObjectifInvalide("Lille", 13, "test")` doit afficher `Lille, mois 13 : test`.
2. `Magasin` : `fixer_objectif`, `enregistrer`, les quatre propriétés, `mois_atteints`, `__repr__`, `__lt__`. Test : `m = Magasin("Test"); m.fixer_objectif(1, 100); m.enregistrer(Realisation("Test", 1, 120)); m.taux_atteinte` doit afficher `1.2`, et `m.fixer_objectif(13, 100)` doit lever `ObjectifInvalide`.
3. Les trois indicateurs : `calculer` seulement, `presenter` est déjà écrite.
4. `Reseau` : `ajouter`, `magasins`, `charger`, `rapport`.
5. `main()` : ajoute deux objectifs invalides à la liste, comme indiqué.

Pour tester dans un terminal Python : `from suivi_objectifs import *`.

Règle du brief : tu regardes l'exemple autant que tu veux, mais tu tapes tes lignes toi-même.

**C'est bon quand** : `python suivi_objectifs.py` affiche le rapport, avec les deux entrées refusées en bas.

### Étape 4 — Vérifie tes chiffres (15 min)

- CA réalisé (réseau) : **7 195 913.43 €**
- Taux d'atteinte global : **96,0 %**
- Magasins sous l'objectif : **7** (oui, aucun n'atteint 100 % sur l'année)
- Premier du classement : **Amiens, 99,9 %, 4 mois atteints [1, 7, 10, 12]** ; dernier : **Lille, 91,2 %**
- Entrées refusées : **2**, tes deux objectifs invalides

Un écart sur le taux ? Vérifie que tu divises la somme des CA par la somme des objectifs, pas la moyenne des taux mensuels.

### Étape 5 — Diagramme, fiche des indicateurs, dépôt (45 min)

1. `diagramme_objectifs.md` : copie `diagramme_stock.md`, puis remplace chaque boîte par ta classe, ses attributs et ses méthodes. Les flèches restent les mêmes : héritage pour les indicateurs et l'exception, agrégation entre `Reseau` et `Magasin`. Vérifie le rendu sur [mermaid.live](https://mermaid.live).
2. `indicateurs_objectifs.md` : copie `indicateurs_stock.md` et remplis les mêmes rubriques pour tes trois indicateurs. Les définitions à respecter : CA réalisé = somme des CA annuels des magasins ; taux global = CA réalisé divisé par la somme des objectifs ; magasins sous l'objectif = nombre de magasins dont le taux est inférieur à 100 %.
3. `README.md` : titre, une phrase, la commande, la sortie du programme dans un bloc de code, ton nom.
4. Commit, push, vérifie sur GitHub.

### Si tu as fini en avance

- Un quatrième indicateur : le mois où le plus de magasins ont atteint leur objectif.
- Rendre `Reseau` parcourable avec `for magasin in reseau` (`__iter__`).

## Évaluation

- **Revue du dépôt (70 %)** : le formateur lance ton module, compare aux valeurs de contrôle et lit tes classes à côté de l'exemple.
- **Démo (30 %)** : 5 minutes. Tu montres le rapport, tu expliques pourquoi `taux_atteinte` est une propriété, et tu ajoutes en direct un objectif invalide pour montrer qu'il est refusé.

Si l'exception, `Realisation` et `Magasin` sont justes mais que les indicateurs ou le réseau manquent, tu peux valider partiellement. Si les objectifs peuvent être modifiés sans passer par `fixer_objectif`, ou si le taux est stocké dans un attribut mis à jour à la main, le critère d'encapsulation n'est pas validé.

## Compétences visées (référentiel Data Analyst Simplon, niveau 1)

**C2 — Concevoir un produit data**
- `indicateurs_objectifs.md` décrit les trois indicateurs avec objectif, définition, formule, unité et classe, et le code applique bien ces formules.
- `diagramme_objectifs.md` montre toutes les classes avec les bonnes flèches : héritage pour les indicateurs et l'exception, agrégation pour le réseau.

**C8 — Développer des règles de nettoyage de données**
- Un objectif dont le mois est hors de 1 à 12 ou dont le montant n'est pas positif est refusé par `ObjectifInvalide`, qui porte la ville et le mois.
- `charger` capture l'exception, continue, et le rapport liste les entrées refusées, dont les deux ajoutées dans `main()`.
- Les objectifs ne sont modifiables que par `fixer_objectif` ; la propriété `objectifs` renvoie une copie.
- Le module est sur un dépôt GitHub public avec un README qui donne la commande et la sortie.

## Ressources

- Cours : [01-classes-objets](../../../01-Fondamentaux/Python/02-POO/01-classes-objets.ipynb), [03-encapsulation](../../../01-Fondamentaux/Python/02-POO/03-encapsulation.ipynb), [05-heritage-polymorphisme-composition](../../../01-Fondamentaux/Python/02-POO/05-heritage-polymorphisme-composition.ipynb), [07-methodes-speciales-exceptions](../../../01-Fondamentaux/Python/02-POO/07-methodes-speciales-exceptions.ipynb), [09-uml-conception](../../../01-Fondamentaux/Python/02-POO/09-uml-conception.ipynb).
- [Cheatsheet POO](../../../01-Fondamentaux/Python/02-POO/CHEATSHEET-poo.ipynb) · [mermaid.live](https://mermaid.live)
- Brief suivant : [PY3 — Consolider deux magasins](PY3-pipeline-consolidation.md)
