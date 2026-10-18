# Cours Python : de 0 a Expert

## Presentation

Ce cours couvre Python de maniere generaliste, du niveau debutant au niveau expert. Il est structure en **6 sections thematiques**, accompagnees d'**exercices** et de **briefs** (projets de validation).

> **Note :** Le SQL est traite dans d'autres modules de la formation (voir `05-Databases/`). Ce cours se concentre exclusivement sur Python.

## Prerequis

- Un ordinateur avec Python 3.10+ installe
- Un editeur de code (VS Code recommande) ou JupyterLab
- Aucune connaissance prealable en programmation requise

## Legende des badges

| Badge | Signification |
|-------|--------------|
| `Debutant` | Aucun prerequis, accessible a tous |
| `Intermediaire` | Necessite les bases Python (sections 01-02) |
| `Avance` | Necessite une bonne maitrise (sections 01-04) |
| `Expert` | Necessite toutes les sections precedentes |

## Sommaire

### 01 - Syntaxe (~10h30)

Les fondamentaux du langage en 4 notebooks de demonstration (cours dense, une cellule par point, code a executer en direct). Chaque cours est suivi de son notebook d'exercices de niveau **imiter** : un exercice par geste vu en cours, avec une cellule de verification automatique (`assert`) apres chacun. Les corriges ne sont pas dans ce depot.

| # | Notebook | Duree | Niveau |
|---|----------|-------|--------|
| 01 | [Les bases : installation, conventions, types, print, input](01-Syntaxe/01-bases.ipynb) | 90 min | Debutant |
| 02 | [Exercices - Les bases](01-Syntaxe/02-exercices-bases.ipynb) | 60 min | Debutant |
| 03 | [Structures de donnees : str, list, tuple, dict, set](01-Syntaxe/03-structures-donnees.ipynb) | 2 h | Debutant |
| 04 | [Exercices - Structures de donnees](01-Syntaxe/04-exercices-structures-donnees.ipynb) | 60 min | Debutant |
| 05 | [Controle de flux et fonctions : if, match, boucles, def, lambda, comprehensions](01-Syntaxe/05-controle-fonctions.ipynb) | 2 h | Debutant |
| 06 | [Exercices - Controle de flux et fonctions](01-Syntaxe/06-exercices-controle-fonctions.ipynb) | 60 min | Debutant |
| 07 | [Generateurs, modules et dates](01-Syntaxe/07-generateurs-modules-dates.ipynb) | 90 min | Intermediaire |
| 08 | [Exercices - Generateurs, modules et dates](01-Syntaxe/08-exercices-generateurs-modules-dates.ipynb) | 60 min | Intermediaire |

### 02 - POO (~11h30)

Programmation orientee objet en Python, de la premiere classe aux patrons de conception, en 5 notebooks de demonstration (meme format que 01-Syntaxe : une cellule de code par point, section « Pieges » en fin de cours). Chaque cours est suivi de son notebook d'exercices de niveau **imiter**, un exercice par geste vu en cours, avec une cellule de verification automatique (`assert`) apres chacun. Les corriges ne sont pas dans ce depot.

> Les anciens dossiers `02-POO-Concepts` et `03-POO-Python` ont ete fusionnes ici. Le numero 03 n'est plus utilise.

| # | Notebook | Duree | Niveau |
|---|----------|-------|--------|
| 01 | [Classes et objets : class, __init__, self, attributs, methodes, __repr__](02-POO/01-classes-objets.ipynb) | 90 min | Intermediaire |
| 02 | [Exercices - Classes et objets](02-POO/02-exercices-classes-objets.ipynb) | 60 min | Intermediaire |
| 03 | [Encapsulation : visibilite, @property, invariants](02-POO/03-encapsulation.ipynb) | 60 min | Intermediaire |
| 04 | [Exercices - Encapsulation](02-POO/04-exercices-encapsulation.ipynb) | 45 min | Intermediaire |
| 05 | [Heritage, polymorphisme et composition : super(), ABC, duck typing](02-POO/05-heritage-polymorphisme-composition.ipynb) | 2 h | Intermediaire |
| 06 | [Exercices - Heritage, polymorphisme et composition](02-POO/06-exercices-heritage-polymorphisme-composition.ipynb) | 60 min | Intermediaire |
| 07 | [Methodes speciales et exceptions : __eq__, __lt__, __add__, __len__, try/raise](02-POO/07-methodes-speciales-exceptions.ipynb) | 90 min | Intermediaire |
| 08 | [Exercices - Methodes speciales et exceptions](02-POO/08-exercices-methodes-speciales-exceptions.ipynb) | 60 min | Intermediaire |
| 09 | [UML et conception : diagramme de classes, Mermaid, SRP, dataclass, Strategy, Factory](02-POO/09-uml-conception.ipynb) | 60 min | Intermediaire |
| 10 | [Exercices - UML et conception](02-POO/10-exercices-uml-conception.ipynb) | 45 min | Intermediaire |
| -- | [CHEATSHEET POO](02-POO/CHEATSHEET-poo.ipynb) | ref. | -- |

### 04 - Bibliotheque Standard (~8h)

Modules essentiels de la bibliotheque standard et outils modernes.

| # | Notebook | Duree | Niveau |
|---|----------|-------|--------|
| 01 | [Arguments CLI](04-Bibliotheque-Standard/01-arguments-cli.ipynb) | 45 min | Intermediaire |
| 02 | [Expressions regulieres](04-Bibliotheque-Standard/02-expressions-regulieres.ipynb) | 60 min | Intermediaire |
| 03 | [Systeme de fichiers](04-Bibliotheque-Standard/03-systeme-fichiers.ipynb) | 45 min | Intermediaire |
| 04 | [Fichiers I/O](04-Bibliotheque-Standard/04-fichiers-io.ipynb) | 45 min | Intermediaire |
| 05 | [Context managers](04-Bibliotheque-Standard/05-context-managers.ipynb) | 45 min | Avance |
| 06 | [Type hints](04-Bibliotheque-Standard/06-type-hints.ipynb) | 45 min | Intermediaire |
| 07 | [Dataclasses et Enums](04-Bibliotheque-Standard/07-dataclasses-enums.ipynb) | 45 min | Intermediaire |
| 08 | [Collections et itertools](04-Bibliotheque-Standard/08-collections-itertools.ipynb) | 60 min | Avance |
| 09 | [Secrets et environnement](04-Bibliotheque-Standard/09-secrets-environnement.ipynb) | 45 min | Intermediaire |
| 10 | [Packaging et installation](04-Bibliotheque-Standard/10-packaging-installation.ipynb) | 45 min | Intermediaire |
| -- | [CHEATSHEET Stdlib](04-Bibliotheque-Standard/CHEATSHEET-stdlib.ipynb) | ref. | -- |

### 05 - Qualite et Tests (~6h)

Outils et pratiques pour produire du code fiable et maintenable.

| # | Notebook | Duree | Niveau |
|---|----------|-------|--------|
| 01 | [Analyse statique](05-Qualite-Tests/01-analyse-statique.ipynb) | 45 min | Intermediaire |
| 02 | [Debugging](05-Qualite-Tests/02-debugging.ipynb) | 45 min | Intermediaire |
| 03 | [Tests unitaires avec pytest](05-Qualite-Tests/03-tests-unitaires-pytest.ipynb) | 60 min | Intermediaire |
| 04 | [Couverture et automatisation](05-Qualite-Tests/04-couverture-automatisation.ipynb) | 45 min | Avance |
| 05 | [Pre-commit hooks](05-Qualite-Tests/05-pre-commit-hooks.ipynb) | 45 min | Avance |
| 06 | [Logging structure](05-Qualite-Tests/06-logging-structure.ipynb) | 45 min | Avance |
| 07 | [Profiling et performance](05-Qualite-Tests/07-profiling-performance.ipynb) | 45 min | Avance |
| -- | [CHEATSHEET Qualite](05-Qualite-Tests/CHEATSHEET-qualite.ipynb) | ref. | -- |

### 06 - Data Engineering (~10h)

Python pour le traitement de donnees : NumPy, Pandas, Pydantic, DuckDB, ETL.

> **Fil rouge :** Un meme dataset (donnees de ventes e-commerce) est utilise tout au long de cette section pour assurer la continuite pedagogique.

| # | Notebook | Duree | Niveau |
|---|----------|-------|--------|
| 01 | [NumPy](06-Data-Engineering/01-numpy.ipynb) | 60 min | Intermediaire |
| 02 | [Pandas bases](06-Data-Engineering/02-pandas-bases.ipynb) | 60 min | Intermediaire |
| 03 | [Pandas avance](06-Data-Engineering/03-pandas-avance.ipynb) | 60 min | Avance |
| 04 | [Pydantic et validation](06-Data-Engineering/04-pydantic-validation.ipynb) | 60 min | Avance |
| 05 | [API REST et requests](06-Data-Engineering/05-api-rest-requests.ipynb) | 60 min | Intermediaire |
| 06 | [Connexion bases de donnees](06-Data-Engineering/06-connexion-bases-donnees.ipynb) | 60 min | Avance |
| 07 | [Concurrence et asyncio](06-Data-Engineering/07-concurrence-asyncio.ipynb) | 60 min | Expert |
| 08 | [Formats de donnees](06-Data-Engineering/08-formats-donnees.ipynb) | 45 min | Intermediaire |
| 09 | [DuckDB](06-Data-Engineering/09-duckdb.ipynb) | 60 min | Avance |
| 10 | [ETL en Python](06-Data-Engineering/10-etl-python.ipynb) | 60 min | Expert |
| -- | [CHEATSHEET Data Engineering](06-Data-Engineering/CHEATSHEET-data-engineering.ipynb) | ref. | -- |

### 07 - Pygame (~6h)

Developpement de jeux 2D avec Pygame.

| # | Notebook | Duree | Niveau |
|---|----------|-------|--------|
| 01 | [Introduction et installation](07-Pygame/01-introduction-installation.ipynb) | 30 min | Intermediaire |
| 02 | [Game loop et surfaces](07-Pygame/02-game-loop-surfaces.ipynb) | 45 min | Intermediaire |
| 03 | [Evenements clavier et souris](07-Pygame/03-evenements-clavier-souris.ipynb) | 45 min | Intermediaire |
| 04 | [Formes, images et texte](07-Pygame/04-formes-images-texte.ipynb) | 45 min | Intermediaire |
| 05 | [Sprites et groupes](07-Pygame/05-sprites-groupes.ipynb) | 60 min | Avance |
| 06 | [Sons et musique](07-Pygame/06-sons-musique.ipynb) | 45 min | Intermediaire |
| 07 | [Animations et physique](07-Pygame/07-animations-physique.ipynb) | 60 min | Avance |
| 08 | [Projet jeu complet](07-Pygame/08-projet-jeu-complet.ipynb) | 60 min | Avance |
| -- | [CHEATSHEET Pygame](07-Pygame/CHEATSHEET-pygame.ipynb) | ref. | -- |

### Exercices (~10h)

| # | Notebook | Sections validees | Duree |
|---|----------|-------------------|-------|
| 01 | [Syntaxe et bases](exercices/exercice-01-syntaxe-bases.ipynb) | 01-Syntaxe | 2h |
| 02 | [Structures de donnees](exercices/exercice-02-structures-donnees.ipynb) | 01-Syntaxe | 2h |
| 03 | [Projet POO](exercices/exercice-03-poo-projet.ipynb) | 02-POO | 2h |
| 04 | [Stdlib et fichiers](exercices/exercice-04-stdlib-fichiers.ipynb) | 04-Stdlib | 2h |
| 05 | [Data Engineering](exercices/exercice-05-data-engineering.ipynb) | 06-Data | 2h |

### Briefs - Projets de validation (~15h)

| # | Brief | Sections validees | Duree |
|---|-------|-------------------|-------|
| 01 | [Automatisation de scripts](briefs/brief-01-automatisation-scripts.ipynb) | 01 + 04 | 3h |
| 02 | [Gestionnaire de bibliotheque](briefs/brief-02-gestionnaire-bibliotheque.ipynb) | 02-POO | 3h |
| 03 | [Qualite de code](briefs/brief-03-qualite-code.ipynb) | 05 | 3h |
| 04 | [Jeu Pygame](briefs/brief-04-jeu-pygame.ipynb) | 07 + 02 | 3h |
| 05 | [Pipeline ETL](briefs/brief-05-pipeline-etl.ipynb) | 06 + 04 + 05 | 3h |

## Planning suggere

| Semaine | Contenu | Duree |
|---------|---------|-------|
| 1 | 01-Syntaxe (cours et exercices 01 a 06) | ~8h |
| 2 | 01-Syntaxe (cours et exercices 07-08) + exercices 01-02 | ~6h |
| 3 | 02-POO (cours et exercices 01 a 06) | ~7h |
| 4 | 02-POO (cours et exercices 07 a 10) + exercice 03 + brief 02 | ~9h |
| 5 | 04-Bibliotheque-Standard + exercice 04 | ~10h |
| 6 | 05-Qualite-Tests + brief 01 + brief 03 | ~9h |
| 7 | 06-Data-Engineering (01-05) | ~5h |
| 8 | 06-Data-Engineering (06-10) + exercice 05 | ~7h |
| 9 | 07-Pygame + brief 04 | ~9h |
| 10 | Brief 05 (Pipeline ETL) + revision | ~6h |

**Duree totale estimee : ~78h**

## Outils recommandes

| Outil | Usage |
|-------|-------|
| **Python 3.10+** | Langage (match-case, \|= dict merge) |
| **uv** | Gestionnaire de packages moderne |
| **ruff** | Linter + formatter (remplace flake8, black, isort) |
| **pytest** | Framework de tests |
| **mypy** | Verification de types statique |
| **pre-commit** | Hooks de pre-commit automatises |
| **JupyterLab** | Environnement notebooks |
| **VS Code** | Editeur de code recommande |
