# Partie 2 — Les mesures de dispersion : étendue, variance, écart-type, quartiles

> **Question de la partie.** Deux séries peuvent avoir la même moyenne et ne pas se ressembler du
> tout. Comment mesurer si les valeurs sont **serrées** autour du centre ou **éparpillées** ?

## 1. Pourquoi la position ne suffit pas

Ventes journalières de deux magasins sur cinq jours, en milliers d'euros :

```
Magasin A :   48   50   52   49   51        moyenne = 250 ÷ 5 = 50
Magasin B :   10   90   20   80   50        moyenne = 250 ÷ 5 = 50
```

Même moyenne, même médiane (50). Pourtant A est **régulier** et B part **dans tous les sens**. Pour
un gestionnaire, la différence est capitale : A se planifie (stock, personnel), B non.

La **dispersion** mesure cet éparpillement. Un résumé honnête d'une série donne toujours **une mesure
de position et une mesure de dispersion**.

---

## 2. L'étendue

### Définition

**L'étendue** est la différence entre la plus grande et la plus petite valeur.

$$\text{étendue} = x_{\max} - x_{\min}$$

- Magasin A : 52 − 48 = **4 k€**
- Magasin B : 90 − 10 = **80 k€**

### Limite

L'étendue ne regarde que **deux** valeurs. Une seule valeur extrême la fait exploser, et elle ne dit
rien de ce qui se passe entre les deux bornes. Sur les 613 commandes du module tableur, l'étendue
est de 379 034,80 € à cause d'une seule commande : elle situe les bornes, elle ne décrit pas la série.

---

## 3. Les écarts à la moyenne, la variance et l'écart-type

### L'idée

Pour mesurer l'éparpillement, l'idée naturelle est de regarder **de combien chaque valeur s'éloigne
de la moyenne** : l'**écart** xᵢ − x̄.

Magasin A (moyenne 50) : écarts −2, 0, +2, −1, +1. Magasin B : −40, +40, −30, +30, 0.

Premier réflexe : faire la moyenne des écarts. Impossible : on a vu en partie 1 que **la somme des
écarts à la moyenne est toujours nulle**. Les écarts négatifs annulent les positifs. Pour A comme
pour B, on trouverait 0.

Il faut effacer le signe. Deux façons : prendre la valeur absolue, ou **mettre au carré**. La
statistique a retenu le carré, pour ses propriétés mathématiques : c'est la variance.

### Définition de la variance

**La variance** est la moyenne des carrés des écarts à la moyenne.

$$V = \frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^2$$

### Définition de l'écart-type

**L'écart-type** est la racine carrée de la variance. Il se note σ (sigma) ou s.

$$\sigma = \sqrt{V} = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^2}$$

Pourquoi la racine ? La variance est en **unités au carré** (des euros au carré, des km² au carré),
ce qui ne se lit pas. La racine carrée ramène dans l'unité de départ. **L'écart-type s'exprime dans
la même unité que les données**, et c'est lui qu'on interprète.

**Ce qu'il représente** : la distance **typique** entre une valeur et la moyenne. « En général, les
valeurs sont à environ σ de la moyenne. »

### Calcul à la main, pas à pas

Série de 8 valeurs : `2, 4, 4, 4, 5, 5, 7, 9`. Moyenne : 40 ÷ 8 = **5**.

| Valeur xᵢ | Écart xᵢ − x̄ | Écart au carré (xᵢ − x̄)² |
|---|---|---|
| 2 | −3 | 9 |
| 4 | −1 | 1 |
| 4 | −1 | 1 |
| 4 | −1 | 1 |
| 5 | 0 | 0 |
| 5 | 0 | 0 |
| 7 | +2 | 4 |
| 9 | +4 | 16 |
| **Somme** | **0** | **32** |

1. Les écarts se compensent (somme 0) : c'est attendu.
2. Somme des carrés : 32.
3. Variance : 32 ÷ 8 = **4**.
4. Écart-type : √4 = **2**.

Lecture : les valeurs sont typiquement à **2** de la moyenne 5.

Même méthode pour les magasins :

- A : carrés 4, 0, 4, 1, 1 → somme 10 → V = 10 ÷ 5 = 2 → σ = √2 ≈ **1,41 k€**
- B : carrés 1 600, 1 600, 900, 900, 0 → somme 5 000 → V = 1 000 → σ = √1 000 ≈ **31,6 k€**

B est vingt-deux fois plus dispersé que A. Le chiffre confirme ce que l'œil voyait.

### Population ou échantillon : n ou n − 1

Il existe **deux** écarts-types, et les outils ne calculent pas le même par défaut.

| Cas | Diviseur | Nom | Sheets / Excel | pandas |
|---|---|---|---|---|
| On décrit **toutes** les données qu'on a (une population) | n | écart-type de population, σ | `STDEVP` (ECARTYPEP) | `ddof=0` |
| Les données sont un **échantillon** d'un ensemble plus grand qu'on veut estimer | n − 1 | écart-type d'échantillon, s | `STDEV` (ECARTYPE) | `ddof=1`, par défaut |

Sur les 8 valeurs : σ = √(32 ÷ 8) = 2 ; s = √(32 ÷ 7) = √4,571 = **2,14**. Le diviseur n − 1
corrige le fait qu'un échantillon sous-estime un peu la dispersion de la population. Avec des
centaines de lignes, les deux valeurs sont presque identiques. Ce qui compte : **savoir lequel tu as
calculé, et le dire**.

### Propriétés

| Propriété | Énoncé |
|---|---|
| Signe | la variance et l'écart-type sont toujours **≥ 0** ; ils valent 0 si toutes les valeurs sont égales |
| Décalage | ajouter une constante à toutes les valeurs **ne change pas** l'écart-type (les écarts restent les mêmes) |
| Échelle | multiplier toutes les valeurs par k multiplie l'écart-type par k (et la variance par k²) |
| Sensibilité | comme la moyenne, l'écart-type est **très sensible aux valeurs extrêmes**, encore plus qu'elle à cause du carré |

Sur les 613 commandes : moyenne 1 679,77 €, écart-type 15 504,58 €, soit neuf fois la moyenne. Sans
la commande à 379 050 €, l'écart-type tombe à 2 707,51 € (−83 %). Une seule ligne sur 613.

### Lire un écart-type : le coefficient de variation

Un écart-type de 1,41 k€ est-il grand ? Cela dépend de la moyenne : 1,41 sur une moyenne de 50, c'est
peu ; sur une moyenne de 2, c'est énorme. Pour comparer des séries d'échelles différentes, on
rapporte l'écart-type à la moyenne :

$$CV = \frac{\sigma}{\bar{x}}$$

- Magasin A : 1,41 ÷ 50 = 0,028, soit **2,8 %** : très régulier.
- Magasin B : 31,6 ÷ 50 = 0,63, soit **63 %** : très irrégulier.
- Commandes : 15 505 ÷ 1 680 ≈ 9,2, soit **920 %** : la moyenne ne résume rien.

Repère courant : en dessous de 15 %, la série est homogène et la moyenne la résume bien ; au-dessus
de 30 %, la moyenne est à prendre avec des pincettes ; au-delà de 100 %, elle ne veut plus rien dire.

---

## 4. Les quartiles, déciles et centiles

L'écart-type partage le défaut de la moyenne : les valeurs extrêmes le déforment. Il existe une
famille de mesures de dispersion **robustes**, construites comme la médiane, sur les rangs.

### Définition

On range la série par ordre croissant. **Les quartiles** sont les trois valeurs qui la coupent en
**quatre parts de même effectif** :

```
[ 25 % des valeurs ]  Q1  [ 25 % ]  Q2 = médiane  [ 25 % ]  Q3  [ 25 % des valeurs ]
```

- **Q1**, premier quartile : un quart des valeurs lui sont inférieures ou égales.
- **Q2** : la médiane.
- **Q3**, troisième quartile : trois quarts des valeurs lui sont inférieures ou égales.

Même principe pour les **déciles** (dix parts : D1, D2, … D9) et les **centiles** ou percentiles
(cent parts : P1 … P99). « Le 9ᵉ décile des salaires » est le salaire au-dessus duquel se trouvent
les 10 % les mieux payés.

### Méthode à la main

Pour une série rangée de n valeurs :

- Q1 est la valeur de rang **n ÷ 4, arrondi à l'entier supérieur** ;
- Q3 est la valeur de rang **3n ÷ 4, arrondi à l'entier supérieur**.

Neuf paniers rangés :

```
10   15  [20]  30  [40]  55  [70]  90   120
          Q1        Q2        Q3
```

- n = 9 ; 9 ÷ 4 = 2,25 → rang 3 → **Q1 = 20 €**
- médiane : rang 5 → **Q2 = 40 €**
- 3 × 9 ÷ 4 = 6,75 → rang 7 → **Q3 = 70 €**

**La phrase à savoir dire** : « la moitié des paniers est comprise entre 20 et 70 € ». C'est la
moitié **du milieu**, entre Q1 et Q3.

### L'écart interquartile

$$IQR = Q_3 - Q_1$$

Ici 70 − 20 = **50 €**. C'est la largeur de la moitié centrale. Comme la médiane, il est **robuste** :
remplacer 120 par 12 000 ne le change pas. C'est la mesure de dispersion à donner quand on a donné
la médiane.

> ⚠️ **Les conventions.** Il existe plusieurs façons de calculer un quartile quand n n'est pas un
> multiple de 4. La méthode ci-dessus (rang arrondi vers le haut) est celle du lycée. Google Sheets
> et Excel (`QUARTILE`) **interpolent** entre deux valeurs : sur les 9 paniers ils donnent aussi 20
> et 70, mais sur d'autres séries ils peuvent différer d'une valeur ou d'une fraction. Sur des
> centaines de lignes, l'écart est négligeable. Ce n'est pas une erreur : c'est une convention, à
> nommer si quelqu'un compare vos chiffres.

---

## 5. Repérer les valeurs atypiques : la règle de 1,5 × IQR

Une **valeur atypique** (ou aberrante, *outlier*) est une valeur très éloignée du reste de la série.
Il faut une règle pour la désigner, sinon « très éloignée » reste une opinion. La plus utilisée
s'appuie sur les quartiles :

$$\text{borne basse} = Q_1 - 1{,}5 \times IQR \qquad \text{borne haute} = Q_3 + 1{,}5 \times IQR$$

Toute valeur en dehors de ces bornes est déclarée atypique.

### Exemple

Durées de visite d'un site, en minutes, rangées : `2, 3, 4, 5, 6, 7, 8, 9, 30`.

- n = 9 → Q1 rang 3 = **4** ; médiane rang 5 = **6** ; Q3 rang 7 = **8**.
- IQR = 8 − 4 = **4**.
- Bornes : 4 − 1,5 × 4 = **−2** ; 8 + 1,5 × 4 = **14**.
- **30 est atypique** (au-dessus de 14). Aucune valeur en dessous de −2 : normal, une durée est positive.

### Que faire d'une valeur atypique ?

**Atypique ne veut pas dire fausse.** La commande de 379 050 € était une vraie commande. La règle
désigne, elle ne juge pas. Trois cas :

| Cas | Exemple | Décision |
|---|---|---|
| **Erreur** de saisie ou de mesure | un prix au litre à 18,50 € au lieu de 1,85 € ; un âge de 250 ans | corriger si on connaît la bonne valeur, sinon écarter **en le disant** |
| **Vraie valeur rare** | la commande de flotte ; la Métropole de Lille dans une liste d'intercommunalités | garder, et donner des mesures robustes (médiane, IQR) ; ou analyser à part |
| **Autre population** mélangée | des ventes B2B au milieu des ventes B2C | séparer les deux séries |

Règle absolue : **jamais de suppression silencieuse**. Toute valeur écartée est listée, avec la
raison, et les chiffres sont donnés avec et sans.

---

## 6. La boîte à moustaches

La **boîte à moustaches** (*boxplot*) dessine en un seul schéma **cinq nombres** : minimum, Q1,
médiane, Q3, maximum, plus les valeurs atypiques.

### Construction à la main

Sur les durées de visite `2, 3, 4, 5, 6, 7, 8, 9, 30` :

1. Trace un axe gradué (ici de 0 à 32).
2. Dessine la **boîte** de Q1 à Q3 : de 4 à 8. Elle contient la moitié centrale des valeurs.
3. Trace un **trait** dans la boîte à la médiane : 6.
4. Calcule les bornes (−2 et 14). La **moustache** basse va de la boîte jusqu'à la plus petite valeur
   **à l'intérieur** des bornes : 2. La moustache haute jusqu'à la plus grande valeur à l'intérieur
   des bornes : 9.
5. Chaque valeur au-delà des bornes est un **point isolé** : 30.

```
        ┌───────┐
   ├────┤   │   ├──┤                              •
   2    4   6   8  9                             30
        Q1  Q2  Q3
   0    5    10   15   20   25   30   minutes
```

### Lecture

| Ce qu'on regarde | Ce qu'on en déduit |
|---|---|
| **Position de la boîte** | où se trouve la moitié centrale |
| **Largeur de la boîte** (IQR) | la dispersion de la moitié centrale |
| **Position du trait** dans la boîte | trait au milieu : symétrique ; trait collé à gauche : étalée à droite |
| **Longueur des moustaches** | l'étendue des valeurs « normales » |
| **Points isolés** | les valeurs atypiques, à examiner une par une |

Deux boîtes côte à côte (une par magasin, par département, par intercommunalité) se comparent d'un
coup d'œil : c'est l'usage principal du graphique.

![Boîte à moustaches des 613 montants de commande : minimum 15 €, Q1 50 €, médiane 177 €, Q3 1 790 €, seuil haut 4 400 €, puis 14 valeurs atypiques dont la commande de 379 050 € ; médiane collée à gauche, distribution étalée à droite](../../../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/images/boite-a-moustaches-anatomie.svg)

*Sur les 613 commandes : Q1 = 50,15 €, Q3 = 1 790 €, IQR = 1 739,85 €, borne haute = 1 790 + 1,5 ×
1 739,85 ≈ 4 400 €. Quatorze commandes la dépassent. La médiane (177 €) est collée à gauche de la
boîte : distribution étalée à droite.*

> Google Sheets ne dessine pas de boîte à moustaches. Excel le fait (*Insertion › Graphique
> statistique › Zone et valeur*), Python aussi. Dans Sheets, on donne les cinq nombres dans un tableau.

---

## 7. Sur des données réelles

Taux de pauvreté 2023 des **92 intercommunalités** des Hauts-de-France (fichier
`insee_revenus_population_hdf-v.xlsx` du module tableur), en % :

| Mesure | Valeur |
|---|---|
| Minimum | 7,0 |
| Q1 | 12,0 |
| Médiane | 14,5 |
| Q3 | 20,15 |
| Maximum | 33,5 (CA Creil Sud Oise) |
| Moyenne | 16,1 |
| Écart-type (population, ÷ n) | 5,6 |
| Écart interquartile | 8,15 |

Lecture :

- « La moitié des intercommunalités ont entre 12 et 20 % de pauvres. »
- Médiane 14,5 < moyenne 16,1 : étalée à droite, quelques territoires très pauvres tirent la moyenne.
- De Q1 à la médiane : 2,5 points. De la médiane à Q3 : 5,65 points. Les territoires peu pauvres
  sont serrés, les territoires pauvres sont étalés.
- Bornes : 12 − 1,5 × 8,15 = −0,2 ; 20,15 + 1,5 × 8,15 = 32,4. **Une seule valeur atypique** :
  Creil Sud Oise, 33,5 %. Ce n'est pas une erreur : c'est le territoire le plus pauvre de la région.
  On le garde, on le nomme.

---

## 8. Dans le tableur

| Mesure | Google Sheets (Excel FR) | Remarque |
|---|---|---|
| Minimum, maximum | `MIN(plage)`, `MAX(plage)` | étendue : `MAX(plage)-MIN(plage)` |
| Variance de population (÷ n) | `VARP(plage)` (VAR.P) | |
| Variance d'échantillon (÷ n − 1) | `VAR(plage)` (VAR.S) | |
| Écart-type de population | `STDEVP(plage)` (ECARTYPE.PEARSON) | |
| Écart-type d'échantillon | `STDEV(plage)` (ECARTYPE.STANDARD) | **celui par défaut dans la plupart des outils** |
| Quartiles | `QUARTILE(plage; 1)`, `QUARTILE(plage; 3)` | convention par interpolation |
| Centiles | `PERCENTILE(plage; 0,9)` (CENTILE) | le 9ᵉ décile |
| n-ième plus grande valeur | `LARGE(plage; n)` (GRANDE.VALEUR) | pour voir les extrêmes sans trier |
| Coefficient de variation | `STDEVP(plage)/AVERAGE(plage)` | à formater en % |

À faire : saisis `2, 4, 4, 4, 5, 5, 7, 9`, vérifie `STDEVP` = 2 et `STDEV` = 2,14. Saisis les 9
durées de visite, vérifie Q1 = 4, Q3 = 8.

---

## Exercices

### Exercice 1 — Variance et écart-type à la main

Ventes journalières d'une boutique sur 5 jours, en k€ : `12, 15, 14, 13, 16`.
Calcule la moyenne, la variance (÷ n), l'écart-type et le coefficient de variation. Conclus.

<details>
<summary>Corrigé</summary>

- Moyenne = 70 ÷ 5 = **14 k€**.
- Écarts : −2, +1, 0, −1, +2 (somme 0). Carrés : 4, 1, 0, 1, 4 → somme **10**.
- Variance = 10 ÷ 5 = **2**. Écart-type = √2 ≈ **1,41 k€**.
- CV = 1,41 ÷ 14 ≈ **10 %** : boutique très régulière, la moyenne la résume bien.

</details>

### Exercice 2 — Même moyenne, dispersions différentes

Deux vendeurs, ventes par jour sur 5 jours (nombre de vélos) :

```
Camille :  20   22   18   21   19
Dimitri :   5   35   20   30   10
```

1. Vérifie qu'ils ont la même moyenne.
2. Calcule l'écart-type de chacun (÷ n) et le coefficient de variation.
3. Le responsable veut confier le magasin un samedi de forte affluence à celui qui « fait le plus de
   ventes ». Que lui réponds-tu ?

<details>
<summary>Corrigé</summary>

1. Camille : 100 ÷ 5 = 20. Dimitri : 100 ÷ 5 = 20. Même moyenne.
2. Camille : écarts 0, +2, −2, +1, −1 → carrés 0, 4, 4, 1, 1 → somme 10 → V = 2 → σ ≈ **1,41** →
   CV ≈ **7 %**.
   Dimitri : écarts −15, +15, 0, +10, −10 → carrés 225, 225, 0, 100, 100 → somme 650 → V = 130 →
   σ ≈ **11,4** → CV ≈ **57 %**.
3. Ils font le même nombre de ventes en moyenne : le critère ne départage pas. Camille est
   prévisible (entre 18 et 22), Dimitri fait des journées à 35 et des journées à 5. Pour un samedi
   crucial, la question est : veut-on la sécurité (Camille) ou le pari (Dimitri) ? La statistique
   pose le choix, elle ne le fait pas.

</details>

### Exercice 3 — Quartiles, IQR et valeur atypique

Douze commandes rangées par montant, en € : `5, 7, 8, 8, 9, 10, 12, 13, 15, 18, 22, 40`.

1. Calcule Q1, la médiane, Q3 et l'IQR avec la méthode du cours.
2. Applique la règle 1,5 × IQR. Y a-t-il une valeur atypique ?
3. Google Sheets donne Q3 = 15,75. Pourquoi ?

<details>
<summary>Corrigé</summary>

1. n = 12. Q1 : 12 ÷ 4 = 3 → rang 3 → **8**. Médiane : rangs 6 et 7 → (10 + 12) ÷ 2 = **11**.
   Q3 : 36 ÷ 4 = 9 → rang 9 → **15**. IQR = 15 − 8 = **7**.
2. Bornes : 8 − 10,5 = −2,5 ; 15 + 10,5 = 25,5. **40 est atypique.**
3. Sheets interpole : il place Q3 à la position 1 + (12 − 1) × 0,75 = 9,25, soit un quart du chemin
   entre la 9ᵉ valeur (15) et la 10ᵉ (18) : 15 + 0,25 × 3 = 15,75. Autre convention, même
   conclusion : 40 reste atypique (borne haute 15,75 + 1,5 × 7,75 = 27,4).

</details>

### Exercice 4 — Lire cinq nombres

Délais de traitement de réclamations, en jours : minimum 3, Q1 9, médiane 12, Q3 20, maximum 60.

1. Entre quelles valeurs se trouve la moitié centrale des réclamations ?
2. La distribution est-elle symétrique ?
3. Le délai de 60 jours est-il atypique au sens de la règle ?
4. Jusqu'où va la moustache haute ?

<details>
<summary>Corrigé</summary>

1. Entre **9 et 20 jours** (Q1 à Q3). IQR = 11.
2. Non : de Q1 à la médiane, 3 jours ; de la médiane à Q3, 8 jours ; et le maximum est très loin.
   **Étalée à droite** : la plupart des réclamations sont traitées vite, quelques-unes traînent.
3. Borne haute = 20 + 1,5 × 11 = **36,5**. Oui, 60 est atypique.
4. Jusqu'à la plus grande valeur **inférieure ou égale à 36,5**. On ne peut pas la connaître avec
   les cinq nombres seuls ; ce n'est pas 36,5, et ce n'est pas 60.

</details>

### Exercice 5 — Propriétés de l'écart-type

Les prix d'un rayon ont un écart-type de 4 €.

1. Tous les prix augmentent de 5 €. Nouvel écart-type ?
2. Tous les prix augmentent de 10 %. Nouvel écart-type ? Nouvelle variance, sachant qu'elle valait 16 ?

<details>
<summary>Corrigé</summary>

1. **4 €** : un décalage ne change pas les écarts entre valeurs.
2. Écart-type × 1,10 = **4,40 €**. Variance × 1,10² = 16 × 1,21 = **19,36**.

</details>

### Exercice 6 — n ou n − 1

Sur la série `2, 4, 4, 4, 5, 5, 7, 9`, un collègue trouve un écart-type de 2,14 et toi 2. Qui a
raison ? Dans quel cas utiliser l'un ou l'autre ?

<details>
<summary>Corrigé</summary>

Les deux. 2 est l'écart-type de **population** (÷ 8), 2,14 celui d'**échantillon** (÷ 7). Si les
8 valeurs sont tout ce qu'on décrit, on prend 2. Si elles sont un échantillon d'un ensemble plus
grand qu'on cherche à estimer, on prend 2,14. Dans un rapport, on écrit lequel on a utilisé. Le
collègue a probablement tapé `STDEV`, qui divise par n − 1.

</details>

### Exercice 7 — Sur les données réelles

Reprends les cinq nombres du taux de pauvreté des 92 intercommunalités (section 7).

1. Écris la phrase « la moitié des intercommunalités… ».
2. Quel pourcentage des intercommunalités ont un taux inférieur à 20,15 % ?
3. Un élu dit : « Creil Sud Oise est une anomalie, il faut l'enlever du calcul. » Que réponds-tu ?

<details>
<summary>Corrigé</summary>

1. « La moitié des intercommunalités ont un taux de pauvreté compris entre 12 et 20,15 %. »
2. **75 %** : 20,15 est le troisième quartile.
3. Atypique au sens de la règle, oui (au-dessus de 32,4). Anomalie, non : c'est un vrai territoire,
   avec de vrais habitants, et le plus pauvre de la région. On le garde. Si l'élu veut une moyenne
   « sans Creil », on la donne **à côté** de la moyenne complète, en le disant. Et on rappelle que
   la médiane (14,5) ne bouge pas, avec ou sans lui.

</details>

---

⬅️ [1 — Position](01-position.md) · ➡️ [3 — Les pièges de la moyenne](03-pieges-de-la-moyenne.md)
