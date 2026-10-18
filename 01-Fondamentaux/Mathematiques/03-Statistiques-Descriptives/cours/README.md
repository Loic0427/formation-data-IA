# Statistiques descriptives — le cours

> Un cours de statistiques, pas un cours d'outil. Chaque notion est **définie**, **écrite en
> formule**, **calculée à la main** sur un petit exemple, puis **discutée** : à quoi elle sert, quand
> elle trompe, laquelle choisir. Les exercices sont corrigés. L'outil (Google Sheets, Excel, plus tard
> Python) n'arrive qu'en fin de partie, dans un encadré : il ne fait que refaire ce que tu sais déjà
> faire sur papier.

| | |
|---|---|
| **Public** | Data Analyst en formation, aucun prérequis au-delà des quatre opérations, du carré et de la racine carrée |
| **Durée** | 3 demi-journées de cours (une par partie) + exercices · environ 12 h |
| **Compétence** | C13 — Réaliser une analyse statistique (mesures de position et de dispersion, distributions, valeurs atypiques) |
| **Version Python** | le même chapitre avec `pandas` et `numpy` : [01-statistiques-descriptives.md](../01-statistiques-descriptives.md), à reprendre quand Python sera en place |

## Plan

| Partie | Contenu | Durée |
|---|---|---|
| [1 · Position](01-position.md) | Vocabulaire (population, individu, variable, effectif, fréquence) · types de variables · **moyenne** (formule, propriétés, à partir d'un tableau d'effectifs) · **médiane** (n pair ou impair, effectifs cumulés) · **mode** · choisir la bonne mesure selon la distribution | 3 h + exercices |
| [2 · Dispersion](02-dispersion.md) | Pourquoi la position ne suffit pas · **étendue** · écarts à la moyenne · **variance** · **écart-type** (population et échantillon) · coefficient de variation · **quartiles**, déciles, centiles · **écart interquartile** · règle des valeurs atypiques (1,5 × IQR) · **boîte à moustaches** construite à la main | 3 h + exercices |
| [3 · Pièges de la moyenne](03-pieges-de-la-moyenne.md) | Valeurs extrêmes · distributions asymétriques (moyenne, médiane et forme) · effectifs déséquilibrés et **moyenne pondérée** · **moyenne de moyennes** et paradoxe de Simpson · pourcentages (points, base, évolutions) · valeurs manquantes et zéros · petits effectifs · liste de contrôle avant de publier un chiffre | 3 h + exercices |
| [4 · Exercices de synthèse et quiz](04-exercices-synthese-quiz.md) | Un portrait complet sur les 92 intercommunalités des Hauts-de-France (données réelles) · 15 questions à choix multiple corrigées | 2 h |
| [5 · Mémo](05-memo-formules.md) | Toutes les formules sur une page, avec la fonction Sheets / Excel en face | — |

## Comment travailler

1. **Lis la définition, puis refais le calcul à la main** avant de lire la suite. Les exemples sont
   petits (5 à 12 nombres) pour que ce soit possible.
2. **Fais les exercices de la partie avant d'ouvrir le corrigé.** Un exercice raté puis compris vaut
   plus qu'un exercice lu.
3. **L'encadré « dans le tableur » vient en dernier.** Refais chaque exemple dans une feuille et
   vérifie que tu retrouves le résultat calculé à la main. Si ce n'est pas le cas, l'une des deux
   conventions expliquées dans le cours (diviseur n ou n − 1, méthode des quartiles) est en cause.

## Ce que tu sauras faire à la fin

- Dire de quel type est une variable et quels calculs elle autorise.
- Calculer et **interpréter** moyenne, médiane, mode, étendue, variance, écart-type, quartiles,
  écart interquartile.
- Choisir la mesure qui résume honnêtement une série, et justifier ce choix.
- Repérer une valeur atypique par une règle, et décider quoi en faire.
- Construire et lire une boîte à moustaches.
- Reconnaître les six pièges classiques de la moyenne, et les éviter.
- Écrire une phrase de restitution qui donne l'indicateur, le périmètre et l'effectif.
