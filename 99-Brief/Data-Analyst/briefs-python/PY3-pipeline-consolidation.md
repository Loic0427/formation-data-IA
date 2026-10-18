# Brief PY3 — Consolider les ventes de Valenciennes et Roubaix en un seul fichier

## Informations

| Critère | Valeur |
|---------|--------|
| **Quand** | Après les briefs [PY1](PY1-syntaxe-analyse-magasin.md) et [PY2](PY2-poo-suivi-objectifs.md), dernier jour avant pandas |
| **Durée** | Une journée (7 h) |
| **Niveau** | 1 — **imiter** : un pipeline exemple complet, un squelette à remplir et un script de contrôle sont fournis |
| **Modalité** | Individuel |
| **Outils** | Python 3.10+ sans rien installer, Mermaid, Git/GitHub |
| **Kit** | [`kit-PY3/`](kit-PY3/) : `consolidation_exemple.py` (l'exemple, Tourcoing + Lille), `diagramme_consolidation.md`, `consolidation_squelette.py` (ton squelette), `controle.py` (vérifie ton résultat), les quatre exports `ventes_*.csv` et la référence `ventes_consolidees.csv` |

## Ta mission en une phrase

Le responsable BI a écrit un programme qui rassemble les ventes de **Tourcoing et Lille** dans un seul fichier propre. Tu écris le même pour **Valenciennes et Roubaix**, tu vérifies avec le script de contrôle que ton fichier est exact, et tu publies.

## Ce que tu rends

Un dépôt GitHub public qui contient :

- `consolidation.py` : ton programme, qui tourne avec `python consolidation.py` ;
- `controle.py` : le script fourni, sans modification ;
- `ventes_valenciennes.csv`, `ventes_roubaix.csv`, `ventes_consolidees.csv` : les données ;
- `ventes_consolidees_valenciennes_roubaix.csv` : le fichier que ton programme produit ;
- `RAPPORT.md` : la sortie du programme, la sortie du contrôle, ton diagramme Mermaid, la liste de tes règles de nettoyage ;
- `README.md` : titre, ce que fait le programme, les deux commandes dans l'ordre, ton nom.

Le fichier exemple ne doit **pas** être dans ton dépôt.

## Le contexte

Avant de brancher un outil de BI, NordRetail a besoin d'un seul fichier de ventes pour tous les magasins. Problème : chaque magasin exporte à sa façon. Le fichier de **Roubaix** appelle ses colonnes `qte` et `CA` au lieu de `quantite` et `montant`. C'est la seule différence avec l'exemple, et le lecteur de l'exemple sait déjà renommer des colonnes grâce à son paramètre `renommage`. Le fichier `ventes_consolidees.csv` est la **référence** : ton résultat doit lui être identique pour tes deux villes.

## Les étapes

### Étape 1 — Installe-toi (30 min)

1. Copie `kit-PY3`, renomme-le `consolidation-ventes`, crée le dépôt GitHub public.
2. Lance `python consolidation_exemple.py`. Un fichier `ventes_consolidees_exemple.csv` apparaît ; supprime-le ensuite.
3. Ouvre `ventes_valenciennes.csv` et `ventes_roubaix.csv` dans un éditeur et regarde la première ligne de chacun.

**C'est bon quand** : tu as vu que Roubaix écrit `date,categorie,produit,qte,CA` et Valenciennes `date,categorie,produit,quantite,montant`.

### Étape 2 — Lis l'exemple avec le diagramme (45 min)

Lis `consolidation_exemple.py` une classe à la fois, avec `diagramme_consolidation.md` à côté. Le programme a six pièces :

- `LigneInvalide` : une ligne refusée, avec sa raison ;
- `Vente` : une ligne propre et typée ;
- `LecteurCsv` : lit un fichier, connaît son séparateur et ses renommages ;
- `Nettoyeur` : transforme chaque ligne en `Vente` ou la refuse, et compte les refus ;
- `Indicateur` et ses variantes : calculent les chiffres du rapport ;
- `EcrivainCsv` et `Pipeline` : écrivent le fichier et enchaînent le tout.

**C'est bon quand** : tu peux dire quelle classe tu modifierais pour ajouter une nouvelle règle de nettoyage (réponse : `Nettoyeur.normaliser`).

### Étape 3 — Remplis le lecteur et le nettoyeur (1 h 30)

Renomme `consolidation_squelette.py` en `consolidation.py`. Dans le squelette, `LigneInvalide`, `Vente`, `EcrivainCsv` et la méthode `presenter` sont déjà écrits : ne les touche pas. Remplis dans l'ordre :

1. `LecteurCsv.lignes` : le renommage des clés et l'ajout de la ville.
2. `Nettoyeur.normaliser` : les quatre conversions, puis les trois règles, dont la nouvelle : **produit vide → refusé avec la raison « produit manquant »**.
3. `Nettoyeur.nettoyer`.

Teste dans un terminal Python :

```python
from consolidation import *
lecteur = LecteurCsv("ventes_roubaix.csv", "Roubaix", renommage={"qte": "quantite", "CA": "montant"})
next(lecteur.lignes())        # doit afficher un dict avec les clés quantite, montant et ville
n = Nettoyeur()
len(list(n.nettoyer(lecteur.lignes())))   # doit afficher 1914
n.rejets                                  # doit afficher Counter() (aucun rejet)
```

Essaie ensuite **sans** le renommage : tu obtiens 0 vente et `n.rejets` montre `colonne manquante 'quantite'`. C'est exactement l'erreur que le renommage corrige.

**C'est bon quand** : les deux tests ci-dessus donnent 1914 ventes pour Roubaix et 1183 pour Valenciennes.

### Étape 4 — Remplis les indicateurs et le pipeline (1 h 30)

1. `CaParVille`, `PanierMoyen`, `TopProduits` : la méthode `calculer` de chacun, comme dans l'exemple.
2. `CaParMois` : le nouvel indicateur, construit comme `CaParVille` avec le mois `AAAA-MM` comme clé.
3. `Pipeline.executer` et `Pipeline.rapport`.
4. Dans `main()`, le `renommage` de Roubaix.

**C'est bon quand** : `python consolidation.py` affiche `Consolidation : 3097 ventes, 0 lignes écartées` et le rapport, et le fichier `ventes_consolidees_valenciennes_roubaix.csv` est créé.

### Étape 5 — Contrôle (30 min)

Lance `python controle.py`. Il compare ton fichier à la référence pour tes deux villes : nombre de lignes et CA au centime.

**C'est bon quand** : la dernière ligne est `CONTRÔLE RÉUSSI`. Valeurs attendues : Roubaix 1 914 lignes et 2 327 084.09 € ; Valenciennes 1 183 lignes et 1 471 140.54 €. Si le contrôle échoue, regarde d'abord le renommage, puis la règle `montant <= 0`, puis l'arrondi à deux décimales.

### Étape 6 — Rapport et dépôt (1 h 15)

Écris `RAPPORT.md` avec quatre parties :

1. **Sortie du programme** : la sortie de `python consolidation.py`, dans un bloc de code.
2. **Contrôle** : la sortie de `python controle.py`.
3. **Diagramme** : copie `diagramme_consolidation.md`, ajoute ta classe `CaParMois` sous `Indicateur`. Vérifie le rendu sur [mermaid.live](https://mermaid.live).
4. **Règles de nettoyage** : une ligne par règle (il y en a cinq : valeur mal formée, quantité non positive, montant non positif, produit manquant, ville mise en casse propre) avec, pour chacune, la raison en une phrase.

Puis `README.md` (titre, une phrase, `python consolidation.py` puis `python controle.py`, ton nom), commit, push.

### Étape 7 — Restitution (30 min, en groupe)

Chacun montre son contrôle réussi et dit en une phrase ce qui lui a pris le plus de temps.

### Si tu as fini en avance

- Consolide les **quatre** magasins et adapte `VILLES` dans `controle.py` pour vérifier.
- Lance ton pipeline sur `../data/ventes_sales.csv` (fichier volontairement sale) et lis les compteurs de rejets.

## Évaluation

- **Revue du dépôt (70 %)** : le formateur lance `consolidation.py` puis `controle.py`, puis lit tes classes à côté de l'exemple et ton rapport.
- **Restitution (30 %)** : ta minute de l'étape 7 et une question du formateur sur une règle de nettoyage ou une flèche du diagramme.

Si le lecteur et le nettoyeur sont justes et testés mais que le pipeline n'est pas fini, tu peux valider partiellement. Si le contrôle échoue, le critère d'exactitude n'est pas validé.

## Compétences visées (référentiel Data Analyst Simplon, niveau 1)

**C8 — Développer des règles de nettoyage de données**
- Les deux fichiers sont lus par la même classe `LecteurCsv`, avec le renommage pour Roubaix et la ville ajoutée.
- Les lignes sont converties et les cinq règles appliquées ; le rapport compte les refus par raison.
- `RAPPORT.md` liste les règles avec leur raison ; le README donne les deux commandes dans l'ordre.
- Le code est sur un dépôt GitHub public.

**C13 — Réaliser une analyse statistique**
- CA par ville, moyenne, médiane, écart-type, top 5 produits et CA par mois sont affichés et justes.
- `controle.py` affiche `CONTRÔLE RÉUSSI` : le fichier produit est identique à la référence.

**C2 — Concevoir un produit data**
- Le diagramme Mermaid du rapport montre toutes les classes, `CaParMois` comprise, avec les bonnes flèches.
- Les six colonnes du fichier produit correspondent à la classe `Vente` et aux règles décrites dans le rapport.

## Ressources

- Cours : [01-Syntaxe](../../../01-Fondamentaux/Python/01-Syntaxe/) et [02-POO](../../../01-Fondamentaux/Python/02-POO/), surtout [05-heritage-polymorphisme-composition](../../../01-Fondamentaux/Python/02-POO/05-heritage-polymorphisme-composition.ipynb) et [07-methodes-speciales-exceptions](../../../01-Fondamentaux/Python/02-POO/07-methodes-speciales-exceptions.ipynb).
- [Cheatsheet POO](../../../01-Fondamentaux/Python/02-POO/CHEATSHEET-poo.ipynb) · [mermaid.live](https://mermaid.live)
- La suite : [Brief S06 — EDA des ventes avec pandas](../briefs-hebdo/semaine-06-eda-ventes-nordretail.md), qui repart de ce fichier consolidé.
