# Partie 3 — Les pièges de la moyenne

> **Question de la partie.** La moyenne est le chiffre le plus calculé et le plus mal utilisé de
> l'analyse de données. Dans quelles situations trompe-t-elle, et que faire à la place ?

Six pièges, un exemple chacun, un remède chacun. À la fin, une liste de contrôle à passer avant de
publier n'importe quelle moyenne.

---

## Piège 1 — Les valeurs extrêmes

**Le mécanisme.** Une valeur très grande (ou très petite) pèse dans la somme autant que des dizaines
de valeurs ordinaires. La moyenne est déplacée vers elle.

**L'exemple.** Six salaires nets mensuels : `1 800, 1 900, 2 000, 2 100, 2 200, 9 500` (le dernier
est le gérant). Moyenne = 19 500 ÷ 6 = **3 250 €**. Aucun des six ne gagne « à peu près » 3 250 € :
cinq gagnent moins, un gagne trois fois plus. Médiane = (2 000 + 2 100) ÷ 2 = **2 050 €**.

**Le remède.**
- Donner la **médiane** pour décrire l'individu typique.
- Signaler la valeur extrême et son effet : « moyenne 3 250 €, dont 9 500 € pour le gérant ; sans
  lui, 2 000 € ».
- Ne **jamais** la supprimer sans le dire (partie 2, section 5).
- Éventuellement une **moyenne tronquée** : on retire les 5 % de valeurs les plus hautes et les 5 %
  les plus basses avant de moyenner. À nommer comme telle.

---

## Piège 2 — Les distributions asymétriques

**Le mécanisme.** Ce n'est pas toujours une valeur isolée : parfois c'est **la forme** de la série
qui est déséquilibrée. Beaucoup de petites valeurs, une longue traîne de grandes. Montants, prix,
salaires, patrimoines, durées, tailles de communes : il y a un plancher (zéro) et pas de plafond.
La moyenne se retrouve dans la traîne, loin de la masse.

**L'exemple.** Sur les 613 commandes du module tableur, 259 font moins de 100 €, la moitié moins de
177 €, et la moyenne est à 1 680 €. Sur les 92 intercommunalités des Hauts-de-France, la médiane du
taux de pauvreté est 14,5 % et la moyenne 16,1 %.

**Le remède.**
- Regarder l'**histogramme** avant de choisir la mesure. Bosse à gauche et traîne à droite : la
  moyenne sera au-dessus de la médiane.
- Donner **médiane et quartiles** (« la moitié entre 50 et 1 790 € ») : trois nombres décrivent
  mieux une distribution asymétrique qu'un seul.
- Garder la moyenne pour ce à quoi elle sert : les **totaux** (moyenne × n = chiffre d'affaires) et
  les prévisions de volume.

---

## Piège 3 — Les effectifs déséquilibrés : la moyenne pondérée

**Le mécanisme.** Quand on fait la moyenne de valeurs qui **ne représentent pas le même nombre
d'individus**, une moyenne simple donne le même poids à un groupe de 10 et à un groupe de 10 000.

**L'exemple.** Trois magasins et leur panier moyen :

| Magasin | Panier moyen | Clients |
|---|---|---|
| Lille | 40 € | 200 |
| Lens | 60 € | 50 |
| Arras | 100 € | 10 |

Moyenne simple des trois paniers : (40 + 60 + 100) ÷ 3 = **66,67 €**. Mais 260 clients ont dépensé
en tout 200 × 40 + 50 × 60 + 10 × 100 = 8 000 + 3 000 + 1 000 = 12 000 €, soit **46,15 €** par
client. Le « panier moyen du réseau » est 46 €, pas 67 €. La moyenne simple laisse les 10 clients
d'Arras peser autant que les 200 de Lille.

**La définition.** La **moyenne pondérée** donne à chaque valeur xᵢ un **poids** wᵢ :

$$\bar{x}_w = \frac{\sum w_i x_i}{\sum w_i} = \frac{w_1 x_1 + w_2 x_2 + \dots + w_k x_k}{w_1 + w_2 + \dots + w_k}$$

C'est la formule de la moyenne à partir d'un tableau d'effectifs (partie 1), avec des poids
quelconques : effectifs, populations, coefficients, montants.

**Sur des données réelles.** Taux de pauvreté des 92 intercommunalités des Hauts-de-France :
moyenne simple **16,1 %**, moyenne pondérée par la population **19,1 %**. L'INSEE publie 19 % pour la
région : c'est la pondérée qui est juste. La simple donne à une communauté de communes de 5 500
habitants le même poids qu'à la Métropole de Lille (1,2 million). Comme les territoires ruraux,
nombreux et peu peuplés, sont moins pauvres que les grandes agglomérations, la moyenne simple
sous-estime la pauvreté de 3 points.

**Le remède.** Se demander **sur quoi porte la question**. Si elle porte sur les **personnes** (les
habitants, les clients), on pondère par les personnes. Si elle porte sur les **unités** (« combien
d'intercommunalités dépassent 20 % ? »), la moyenne simple des unités a un sens. Et on donne les deux
quand l'écart est grand : c'est une information en soi.

---

## Piège 4 — La moyenne de moyennes et le paradoxe de Simpson

**Le mécanisme.** Le piège 3 sous une forme plus vicieuse : on compare deux groupes sur leurs
moyennes (ou leurs taux) globales, alors que les groupes n'ont pas la **même composition**. Le
classement peut s'**inverser** entre le détail et le global. C'est le **paradoxe de Simpson**.

**L'exemple.** Deux vendeurs, taux de conversion (ventes ÷ visites) selon le moment de la journée :

| | Matin | Après-midi | **Total** |
|---|---|---|---|
| **Alix** | 5 ventes / 10 visites = **50 %** | 80 / 100 = **80 %** | 85 / 110 = **77,3 %** |
| **Bilal** | 60 / 100 = **60 %** | 9 / 10 = **90 %** | 69 / 110 = **62,7 %** |

Bilal est meilleur le matin (60 contre 50) **et** l'après-midi (90 contre 80). Pourtant, au total,
Alix est devant (77 contre 63). Explication : l'après-midi est plus facile (les clients viennent pour
acheter), et Alix y fait presque toutes ses visites. Le total mélange deux choses : la performance et
la **répartition** des visites.

**Le remède.**
- Toujours vérifier la **composition** des groupes avant de comparer des moyennes globales.
- Comparer **segment par segment**, ou à composition égale.
- Pour un taux régional, un taux d'entreprise, un panier « du réseau » : additionner les
  **numérateurs** et les **dénominateurs**, jamais moyenner des taux. 85 ÷ 110, pas (50 + 80) ÷ 2.

---

## Piège 5 — Les pourcentages

Trois pièges dans un.

**Points et pourcentage.** Un taux qui passe de 16 % à 19 % augmente de **3 points**, pas de 3 %. En
pourcentage, la hausse est de (19 − 16) ÷ 16 = **+19 %**. Dès qu'on compare deux pourcentages, on
parle en points.

**La base d'une évolution.** Un prix qui monte de 50 % puis baisse de 50 % ne revient pas à son point
de départ : 100 → 150 → 75, soit **−25 %**. Les pourcentages successifs se **multiplient** (1,5 ×
0,5 = 0,75), ils ne s'additionnent pas. De même, la moyenne de taux d'évolution mensuels n'est pas
le taux d'évolution de l'année.

**Le taux sur une petite base.** « 50 % des clients de l'après-midi ont acheté » impressionne moins
quand on sait qu'il y avait 2 clients. Un taux se donne **avec son dénominateur** : 1 sur 2, 85 sur
110.

**Le remède.** Écrire l'unité (points ou %), écrire la base (de quoi à quoi), écrire le
dénominateur.

---

## Piège 6 — Les valeurs manquantes, les zéros et les petits effectifs

**Les valeurs manquantes.** Un tableur **ignore les cellules vides** dans une moyenne, mais **compte
les zéros**. Un zéro qui veut dire « inconnu » ou « non renseigné » est un poison.

Sept notes clients `4, 5, 3, 5, 4, 4, 5`, et trois clients qui n'ont pas répondu. Moyenne sur les
répondants : 30 ÷ 7 = **4,29**. Si les trois non-réponses ont été saisies comme 0 : 30 ÷ 10 =
**3,0**. Même fichier, une note qui passe de « très bien » à « moyen ».

Remède : distinguer **vide** (inconnu) et **0** (mesuré nul) ; annoncer l'effectif réel (« 4,29 sur
7 répondants sur 10 »).

**Les petits effectifs.** Sur un petit groupe, un taux ou une moyenne saute d'une valeur à l'autre au
moindre individu. Une commune de 200 habitants avec 30 % de pauvres, c'est 60 personnes ; une famille
qui déménage change le taux d'un point. C'est pourquoi l'INSEE **ne publie pas** le taux de pauvreté
des petites communes (secret statistique) et pourquoi on n'a pas le droit de **classer** des unités
minuscules sur un taux.

Remède : donner l'effectif à côté du taux ; regrouper les petites unités (passer de la commune à
l'intercommunalité) ; ne pas classer sur des effectifs inférieurs à quelques dizaines.

**Le périmètre.** Enfin, la moyenne de **quoi** ? Sur les 613 commandes, le montant commandé est de
1 029 700 € et le montant livré de 343 877 € : les deux sont justes, ils ne répondent pas à la même
question. Un chiffre sans son périmètre est un chiffre faux.

---

## La liste de contrôle avant de publier une moyenne

| # | Question | Si la réponse est mauvaise |
|---|---|---|
| 1 | Sur **combien** de valeurs est-elle calculée, et lesquelles (périmètre) ? | l'écrire dans la phrase |
| 2 | Y a-t-il des **valeurs manquantes** ? Des zéros qui n'en sont pas ? | compter, corriger, annoncer l'effectif réel |
| 3 | Moyenne et **médiane** sont-elles proches ? | sinon, la distribution est asymétrique : donner la médiane et les quartiles |
| 4 | Y a-t-il des **valeurs atypiques** (règle 1,5 × IQR) ? | les nommer, donner les chiffres avec et sans |
| 5 | Les valeurs représentent-elles des groupes de **tailles différentes** ? | pondérer, ou additionner numérateurs et dénominateurs |
| 6 | Si je compare deux groupes, ont-ils la **même composition** ? | comparer segment par segment |
| 7 | Les **pourcentages** ont-ils leur unité, leur base et leur dénominateur ? | les écrire |
| 8 | La phrase donne-t-elle **l'indicateur, la valeur, le périmètre et l'effectif** ? | la réécrire |

---

## Dans le tableur

| Besoin | Google Sheets (Excel FR) |
|---|---|
| Moyenne pondérée | `SUMPRODUCT(valeurs; poids) / SUM(poids)` (SOMMEPROD) |
| Taux global à partir de comptes | `SUM(numerateurs) / SUM(denominateurs)`, jamais `AVERAGE(taux)` |
| Moyenne tronquée | `TRIMMEAN(plage; 0,1)` (MOYENNE.REDUITE) retire 5 % de chaque côté |
| Compter les vides | `COUNTBLANK(plage)` (NB.VIDE) ; les « non publié » en texte : `COUNTIF(plage; "non publié")` |
| Évolution | `=(nouveau - ancien) / ancien`, formaté en % |

---

## Exercices

### Exercice 1 — Moyenne de moyennes

Trois agences et leur délai moyen de traitement d'un dossier : 3 jours (agence A, 400 dossiers),
8 jours (agence B, 80 dossiers), 15 jours (agence C, 20 dossiers). Quel est le délai moyen d'un
dossier dans le réseau ? Que vaut la moyenne simple des trois délais, et que représente-t-elle ?

<details>
<summary>Corrigé</summary>

Pondérée : (400 × 3 + 80 × 8 + 20 × 15) ÷ 500 = (1 200 + 640 + 300) ÷ 500 = 2 140 ÷ 500 =
**4,28 jours** par dossier. Moyenne simple : (3 + 8 + 15) ÷ 3 = **8,67 jours** : c'est le délai
moyen « d'une agence », où la petite agence C pèse autant que la grosse A. Pour un client, c'est
4,28 qui compte ; pour comparer les agences entre elles, 8,67 n'a aucun intérêt, on regarde les trois
délais séparément.

</details>

### Exercice 2 — Taux régional

Trois intercommunalités : taux de pauvreté 10 % (500 000 habitants), 25 % (100 000), 30 % (20 000).
Calcule la moyenne simple des taux et le taux de pauvreté de l'ensemble. Explique l'écart.

<details>
<summary>Corrigé</summary>

Simple : (10 + 25 + 30) ÷ 3 = **21,7 %**. Pondérée : personnes pauvres = 50 000 + 25 000 + 6 000 =
81 000 sur 620 000 habitants = **13,1 %**. La grande intercommunalité, peu pauvre, contient 80 % des
habitants : le taux de l'ensemble est proche du sien. La moyenne simple décrit « l'intercommunalité
moyenne », pas « l'habitant moyen ».

</details>

### Exercice 3 — Paradoxe de Simpson

Deux ateliers de réparation, taux de réparations réussies selon la difficulté :

| | Simples | Complexes |
|---|---|---|
| **Atelier Nord** | 95 / 100 | 10 / 20 |
| **Atelier Sud** | 20 / 20 | 60 / 100 |

1. Calcule les quatre taux, puis le taux global de chaque atelier.
2. Quel atelier est le meilleur ? Comment le présenter honnêtement ?

<details>
<summary>Corrigé</summary>

1. Nord : simples **95 %**, complexes **50 %**, global 105 ÷ 120 = **87,5 %**.
   Sud : simples **100 %**, complexes **60 %**, global 80 ÷ 120 = **66,7 %**.
2. Sud est meilleur sur **chaque** type de réparation, Nord est meilleur au global, parce que Nord
   traite surtout des réparations simples et Sud surtout des complexes. Présenter les taux **par
   type** ; si on ne donne qu'un chiffre, ce sera faux dans un sens ou dans l'autre. La bonne
   phrase : « Sud réussit mieux à difficulté égale ; Nord a un meilleur taux global parce que sa
   charge est plus facile. »

</details>

### Exercice 4 — Évolutions successives

Le chiffre d'affaires d'un magasin augmente de 20 % en 2024, puis baisse de 20 % en 2025.

1. Est-il revenu à son niveau de 2023 ?
2. Quelle est l'évolution sur les deux ans ?
3. Un collègue dit « en moyenne, 0 % par an ». Qu'en penses-tu ?

<details>
<summary>Corrigé</summary>

1. Non : 100 → 120 → 96.
2. 1,20 × 0,80 = 0,96, soit **−4 %**.
3. Faux : les évolutions se multiplient, elles ne se moyennent pas. La moyenne des deux taux (0 %)
   ne décrit pas ce qui s'est passé (−4 %).

</details>

### Exercice 5 — Points et pourcentage

Le taux de commandes livrées passe de 58 % à 64 %. Écris la variation de deux façons correctes et
une façon fausse.

<details>
<summary>Corrigé</summary>

Correct : « + 6 **points** » ; « + 10,3 % » ((64 − 58) ÷ 58 = 0,103). Faux : « + 6 % ». Pour un
lecteur pressé, la première formulation est la plus claire.

</details>

### Exercice 6 — Zéros et valeurs manquantes

Un fichier de 12 livraisons contient les délais suivants, en jours : `2, 3, 0, 2, 4, 0, 3, 2, 0, 5,
2, 3`. Le responsable dit que les 0 sont des livraisons « dont on n'a pas la date ».

1. Quel délai moyen le tableur affiche-t-il ?
2. Quel est le vrai délai moyen ?
3. Que faut-il corriger dans le fichier ?

<details>
<summary>Corrigé</summary>

1. 26 ÷ 12 = **2,17 jours**.
2. Sur les 9 livraisons datées : 26 ÷ 9 = **2,89 jours**.
3. Remplacer les 0 par des cellules **vides** (ou une mention « inconnu » dans une colonne à part),
   et écrire « 2,89 jours sur 9 livraisons datées sur 12 ».

</details>

### Exercice 7 — Petits effectifs

Un tableau classe les 3 782 communes des Hauts-de-France par taux de pauvreté. En tête : une commune
de 45 habitants à 40 %. Un journal titre « la commune la plus pauvre de la région ».

1. Combien de personnes pauvres cela représente-t-il ?
2. Pourquoi ce classement est-il fragile ?
3. Que proposes-tu à la place ?

<details>
<summary>Corrigé</summary>

1. 40 % de 45 = **18 personnes**.
2. Une seule famille qui arrive ou qui part change le taux de plusieurs points. Sur 45 habitants, le
   taux n'est pas une mesure stable ; l'INSEE ne le publie d'ailleurs pas pour une commune de cette
   taille (secret statistique).
3. Classer à une échelle où les effectifs sont suffisants (les intercommunalités), ou ne classer que
   les communes au-dessus d'un seuil d'habitants, et toujours afficher l'effectif à côté du taux.

</details>

### Exercice 8 — Le périmètre

Sur les 613 commandes, un stagiaire écrit « chiffre d'affaires 2025 : 1 029 700 € ». Le comptable
dit 343 877 €. Qui a raison ?

<details>
<summary>Corrigé</summary>

Les deux chiffres sont justes et répondent à deux questions : montant **commandé** (toutes les
commandes, y compris annulées et en cours) et montant **livré** (les 360 commandes livrées). Le
chiffre d'affaires, au sens comptable, est le second. La phrase du stagiaire est fausse par omission
du périmètre.

</details>

---

⬅️ [2 — Dispersion](02-dispersion.md) · ➡️ [4 — Exercices de synthèse et quiz](04-exercices-synthese-quiz.md)
