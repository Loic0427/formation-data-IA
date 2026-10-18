# Brief PY1 — Mon premier script d'analyse : les ventes de Valenciennes

## Informations

| Critère | Valeur |
|---------|--------|
| **Quand** | Fin du dossier [01-Syntaxe](../../../01-Fondamentaux/Python/01-Syntaxe/), après les 4 séries d'exercices |
| **Durée** | Une demi-journée (3 h 30) |
| **Niveau** | 1 — **imiter** : un exemple complet et un squelette à remplir sont fournis |
| **Modalité** | Individuel |
| **Outils** | Python 3.10+ sans rien installer, Git/GitHub |
| **Kit** | [`kit-PY1/`](kit-PY1/) : `analyse_magasin_exemple.py` (l'exemple, pour Tourcoing), `analyse_valenciennes_squelette.py` (ton squelette), `ventes_tourcoing.csv`, `ventes_valenciennes.csv` |

## Ta mission en une phrase

Le responsable BI a écrit un script qui analyse les ventes du magasin de **Tourcoing**. Tu écris le même pour **Valenciennes**, en remplissant le squelette fourni, puis tu publies ton travail sur GitHub.

## Ce que tu rends

Un dépôt GitHub public qui contient :

- `analyse_valenciennes.py` : ton script, complet, qui tourne avec `python analyse_valenciennes.py` ;
- `ventes_valenciennes.csv` : les données, à côté du script ;
- `RAPPORT.md` : la sortie de ton script et tes trois phrases de lecture ;
- `README.md` : titre, ce que fait le script, comment le lancer, ton nom.

Le fichier exemple ne doit **pas** être dans ton dépôt.

## Le contexte

NordRetail a six magasins. Chaque magasin envoie un fichier CSV de ses ventes avec cinq colonnes : `date`, `categorie`, `produit`, `quantite`, `montant`. Le responsable BI en a assez de refaire les calculs à la main dans un tableur : il a écrit un script Python pour Tourcoing et te demande le même pour Valenciennes. Il veut y retrouver ses repères : mêmes fonctions, même rapport.

## Les étapes

### Étape 1 — Installe-toi (15 min)

1. Copie le dossier `kit-PY1` sur ta machine et renomme-le `analyse-valenciennes`.
2. Dans un terminal, place-toi dedans et lance `python analyse_magasin_exemple.py`.
3. Crée ton dépôt GitHub public et fais un premier commit.

**C'est bon quand** : le rapport de Tourcoing s'affiche, il se termine par `Meilleur mois : 2023-01 (123 606.33 €)`.

### Étape 2 — Lis l'exemple (30 min)

Ouvre `analyse_magasin_exemple.py` et lis-le du haut vers le bas, une fonction à la fois. Pour chacune, trouve la cellule du cours qui montre la même chose : `Counter`, `defaultdict`, tri avec `key`, f-strings, `strftime`. Trois choses ne sont pas dans ton cours, tu les recopieras telles quelles, elles sont déjà dans le squelette : `csv.DictReader`, le module `statistics`, le bloc `if __name__ == "__main__":`.

**C'est bon quand** : tu peux dire en une phrase ce que renvoie chaque fonction (par exemple « `ca_par_mois` renvoie un dict mois → total »).

### Étape 3 — Remplis le squelette (1 h 30)

Renomme `analyse_valenciennes_squelette.py` en `analyse_valenciennes.py`. Chaque `...` a un commentaire qui dit quoi écrire. Remplis dans cet ordre :

1. `lire_ventes` : les cinq conversions et la règle « quantité ou montant pas strictement positif » ;
2. `chiffre_affaires`, `ca_par_categorie`, `top_produits`, `statistiques_montant`, `ca_par_mois` : une à la fois ;
3. les deux indicateurs en plus, `ca_moyen_par_jour` et `quantite_par_categorie` : ils se construisent comme ceux du dessus ;
4. les `...` de `afficher_rapport`.

Pour tester une fonction sans attendre la fin, ouvre un terminal Python dans le dossier :

```python
from analyse_valenciennes import *
ventes, ecartees = lire_ventes(FICHIER)
len(ventes)                 # doit afficher 1183
chiffre_affaires(ventes)    # doit afficher 1471140.54 (à l'arrondi près)
```

Règle du brief : tu regardes l'exemple autant que tu veux, mais tu **tapes tes lignes toi-même**. Pas de copier-coller d'une fonction entière.

**C'est bon quand** : `python analyse_valenciennes.py` affiche le rapport complet sans erreur.

### Étape 4 — Vérifie tes chiffres (15 min)

Compare avec ces valeurs de contrôle :

- Lignes conformes : **1 183**, écartées : **0**
- Chiffre d'affaires : **1 471 140.54 €**
- CA moyen par jour de vente : **2 571.92 €**
- Première catégorie : **Sport, 410 242.79 € (27,9 %)**
- Montant d'une vente : moyenne **1243.57**, médiane **889.56**
- Meilleur mois : **2024-01 (130 348.57 €)**

Un écart ? Regarde d'abord la règle de conformité (`<=` et non `<`), puis la conversion du montant.

### Étape 5 — Rapport et dépôt (1 h)

1. Lance le script une dernière fois et colle toute la sortie dans `RAPPORT.md`, dans un bloc de code.
2. Sous la sortie, écris trois phrases pour la contrôleuse de gestion, une par question : quelle catégorie pèse le plus dans le CA ? La moyenne d'une vente est bien plus haute que la médiane : qu'est-ce que ça veut dire ? Le meilleur mois est janvier 2024 : à quoi cela correspond-il dans le calendrier d'un magasin ?
3. Écris `README.md` sur ce modèle :

```markdown
# Analyse des ventes de Valenciennes
Script Python qui lit l'export de ventes du magasin et affiche un rapport (CA, catégories, top produits, statistiques, meilleur mois).
## Lancer
python analyse_valenciennes.py
## Auteur
Prénom Nom
```

4. Commit et push. Vérifie sur GitHub que les quatre fichiers sont là.

### Si tu as fini en avance

- Lance ton script sur `ventes_tourcoing.csv` (change les deux constantes) : tu dois retrouver les chiffres de l'exemple.
- Ajoute la part de chaque trimestre dans le CA.

## Évaluation

- **Revue du dépôt (70 %)** : le formateur lance ton script, compare avec les valeurs de contrôle et lit tes fonctions.
- **Démo (30 %)** : 5 minutes en fin de demi-journée. Tu lances le script et tu expliques une fonction que le formateur choisit.

Si ton script n'est pas terminé mais que les fonctions écrites sont justes et testées, tu peux valider partiellement. Un script recopié de l'exemple avec seulement le nom de la ville changé n'est pas validé.

## Compétences visées (référentiel Data Analyst Simplon, niveau 1)

**C8 — Développer des règles de nettoyage de données**
- La lecture convertit chaque colonne (date, entier, flottant) et une ligne mal formée est écartée sans faire planter le script.
- Une ligne dont la quantité ou le montant n'est pas strictement positif est écartée et comptée ; le rapport affiche conformes et écartées.
- Le script est sur un dépôt GitHub public avec un README qui donne la commande de lancement.

**C13 — Réaliser une analyse statistique**
- Moyenne, médiane, écart-type, minimum et maximum du montant sont affichés et justes.
- CA total, CA par catégorie avec pourcentage, top 5 produits et CA par mois sont affichés et justes.
- Les deux indicateurs supplémentaires sont présents et justes.
- `RAPPORT.md` contient la sortie du script et trois phrases de lecture qui répondent aux trois questions.

## Ressources

- Cours : [01-bases](../../../01-Fondamentaux/Python/01-Syntaxe/01-bases.ipynb) (f-strings), [03-structures-donnees](../../../01-Fondamentaux/Python/01-Syntaxe/03-structures-donnees.ipynb) (dict, `Counter`, `defaultdict`, tri), [05-controle-fonctions](../../../01-Fondamentaux/Python/01-Syntaxe/05-controle-fonctions.ipynb) (fonctions), [07-generateurs-modules-dates](../../../01-Fondamentaux/Python/01-Syntaxe/07-generateurs-modules-dates.ipynb) (dates, import).
- Documentation Python : [`statistics`](https://docs.python.org/fr/3/library/statistics.html), [`csv`](https://docs.python.org/fr/3/library/csv.html)
- Brief suivant : [PY2 — Les objectifs 2024 en objets](PY2-poo-suivi-objectifs.md)
