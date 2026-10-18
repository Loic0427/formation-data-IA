# Partie 1 — Les mesures de position : moyenne, médiane, mode

> **Question de la partie.** On a une colonne de nombres. Si on doit la résumer par **un seul
> chiffre**, lequel choisir, et que veut dire ce chiffre ?

## 1. Le vocabulaire

La statistique descriptive décrit un **ensemble d'observations**. Les mots ci-dessous reviennent
dans toutes les définitions qui suivent : il faut les avoir en tête.

| Mot | Définition | Exemple : un fichier de commandes |
|---|---|---|
| **Population** | l'ensemble de tout ce qu'on observe | les 613 commandes de l'année |
| **Individu** (ou unité statistique) | un élément de la population, **une ligne** du tableau | une commande |
| **Effectif total**, noté **n** | le nombre d'individus | n = 613 |
| **Variable** (ou caractère) | une information relevée sur chaque individu, **une colonne** | le montant, le magasin, la note |
| **Valeur** (ou modalité) | ce que prend la variable pour un individu, **une case** | 40 €, « Lille », 4 |
| **Série statistique** | la liste des valeurs d'une variable pour tous les individus | tous les montants |
| **Effectif d'une valeur**, noté **nᵢ** | le nombre d'individus qui ont cette valeur | 28 commandes à 19 € |
| **Fréquence** d'une valeur, notée **fᵢ** | la part de l'effectif total : fᵢ = nᵢ ÷ n | 28 ÷ 613 = 0,046, soit 4,6 % |
| **Échantillon** | une partie de la population, quand on ne peut pas tout observer | 50 commandes tirées au hasard |

> **Propriété.** La somme des effectifs vaut n, la somme des fréquences vaut 1 (ou 100 %).

### Les types de variables

Le type d'une variable décide de ce qu'on a **le droit** de calculer. C'est la première chose à
établir devant un fichier.

| Type | Définition | Exemples | Calculs autorisés |
|---|---|---|---|
| **Quantitative discrète** | un nombre qui **se compte**, à valeurs isolées | nombre d'articles, nombre d'enfants, nombre de communes | tout : moyenne, médiane, mode, dispersion |
| **Quantitative continue** | un nombre qui **se mesure**, peut prendre n'importe quelle valeur dans un intervalle | montant, superficie, taux de pauvreté, durée | tout |
| **Qualitative nominale** | une étiquette **sans ordre** | magasin, département, mode de paiement | effectifs, fréquences, mode |
| **Qualitative ordinale** | une étiquette **avec un ordre**, mais sans écart mesurable entre deux niveaux | note de satisfaction (1 à 5), taille (S, M, L), tranche de population | effectifs, fréquences, mode, médiane ; moyenne **avec prudence** |
| **Identifiant** | un code qui désigne l'individu | numéro de commande, code INSEE | compter, et rien d'autre |

**Le test qui tranche** : « la somme de cette colonne a-t-elle un sens ? » La somme des montants est
un chiffre d'affaires. La somme des codes postaux ne veut rien dire, même si ce sont des nombres.
Pas de somme, pas de moyenne.

> ⚠️ **Les faux nombres.** Un code postal, un code INSEE, un numéro de téléphone sont écrits avec
> des chiffres mais sont des étiquettes. Un tableur les prend pour des nombres et acceptera d'en faire
> la moyenne : c'est à toi de refuser.

### Le tableau d'effectifs

Quand une variable prend peu de valeurs différentes, on la résume par un **tableau d'effectifs** :
chaque valeur, combien de fois elle apparaît, quelle part ça représente.

Nombre d'articles par commande, sur 30 commandes :

| Valeur xᵢ | Effectif nᵢ | Fréquence fᵢ | Effectif cumulé | Fréquence cumulée |
|---|---|---|---|---|
| 1 | 12 | 0,40 | 12 | 0,40 |
| 2 | 8 | 0,27 | 20 | 0,67 |
| 3 | 5 | 0,17 | 25 | 0,83 |
| 5 | 3 | 0,10 | 28 | 0,93 |
| 10 | 2 | 0,07 | 30 | 1,00 |
| **Total** | **30** | **1,00** | | |

L'**effectif cumulé** additionne les effectifs depuis le début : « 20 commandes ont 2 articles ou
moins ». On s'en servira pour la médiane.

Pour une variable continue (des montants), on regroupe d'abord les valeurs en **classes** (0 à 50 €,
50 à 100 €…) et on compte par classe. C'est ce que dessine un histogramme.

---

## 2. La moyenne

### Définition

**La moyenne arithmétique** d'une série est la somme de toutes les valeurs divisée par leur nombre.

$$\bar{x} = \frac{x_1 + x_2 + \dots + x_n}{n} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

- x̄ se lit « x barre » et désigne la moyenne ;
- Σ (sigma) veut dire « additionne tous les termes » ;
- xᵢ est la i-ème valeur de la série.

**Ce qu'elle représente** : le partage à parts égales. Si les 7 clients du tableau ci-dessous mettaient
leurs dépenses en commun et se les répartissaient également, chacun aurait dépensé la moyenne.

### Calcul à la main

Paniers de 7 clients un mardi matin, en euros :

```
32   41   38   45   29   50   47
```

1. Somme : 32 + 41 + 38 + 45 + 29 + 50 + 47 = **282**
2. Effectif : n = **7**
3. Moyenne : 282 ÷ 7 = **40,29 €**

### À partir d'un tableau d'effectifs

Quand les valeurs sont regroupées, chaque valeur compte **autant de fois que son effectif** :

$$\bar{x} = \frac{n_1 x_1 + n_2 x_2 + \dots + n_k x_k}{n} = \frac{\sum n_i x_i}{n}$$

Avec le tableau des articles par commande :

```
(12 × 1) + (8 × 2) + (5 × 3) + (3 × 5) + (2 × 10) = 12 + 16 + 15 + 15 + 20 = 78
78 ÷ 30 = 2,6 articles par commande
```

C'est déjà une **moyenne pondérée** : chaque valeur est pondérée par son effectif. On y reviendra
dans la partie 3, où les poids seront des populations.

### Propriétés

| Propriété | Énoncé | Exemple |
|---|---|---|
| **Total** | moyenne × n = somme des valeurs | 40,29 × 7 = 282 € de chiffre d'affaires ce matin-là |
| **Décalage** | si on ajoute une constante c à toutes les valeurs, la moyenne augmente de c | tous les prix + 5 € → moyenne 45,29 € |
| **Échelle** | si on multiplie toutes les valeurs par k, la moyenne est multipliée par k | tous les prix × 1,10 → moyenne 44,32 € |
| **Écarts** | la somme des écarts à la moyenne est toujours nulle : Σ(xᵢ − x̄) = 0 | (32 − 40,29) + (41 − 40,29) + … = 0 |
| **Sensibilité** | **une seule valeur très grande ou très petite peut la déplacer beaucoup** | voir ci-dessous |

La propriété des écarts est celle qui fait de la moyenne le « point d'équilibre » de la série : ce
qui est en dessous compense exactement ce qui est au-dessus. C'est aussi pour cela qu'on ne pourra
pas mesurer la dispersion en additionnant simplement les écarts (partie 2).

### Le défaut majeur : la sensibilité aux valeurs extrêmes

Un huitième client passe et achète un vélo électrique à **2 400 €**.

```
32   41   38   45   29   50   47   2 400
Somme = 282 + 2 400 = 2 682        Moyenne = 2 682 ÷ 8 = 335,25 €
```

La moyenne passe de 40 € à 335 € à cause d'**un seul** client. Aucun des huit n'a dépensé 335 €.
Le chiffre reste juste (c'est bien le partage à parts égales), mais il ne décrit plus un client
« typique ». Il faut une autre mesure.

---

## 3. La médiane

### Définition

**La médiane** est la valeur qui partage la série **rangée par ordre croissant** en deux moitiés de
même effectif : la moitié des valeurs lui est inférieure ou égale, l'autre moitié supérieure ou égale.

Image : les clients alignés du plus petit panier au plus gros. La médiane est le panier de la personne
**au milieu de la file**. Peu importe ce que dépense le dernier de la file, le milieu ne bouge pas.

### Méthode

1. **Ranger** les valeurs par ordre croissant. *(Étape obligatoire : une médiane sur une série non
   triée est fausse.)*
2. Si n est **impair**, la médiane est la valeur de rang (n + 1) ÷ 2.
3. Si n est **pair**, il y a deux valeurs centrales, de rangs n ÷ 2 et n ÷ 2 + 1 : la médiane est
   leur moyenne.

### Calcul à la main

Les 7 paniers, rangés :

```
29   32   38  [41]  45   47   50
n = 7, impair : rang (7 + 1) ÷ 2 = 4  →  médiane = 41 €
```

Avec le client à 2 400 € (n = 8, pair) :

```
29   32   38  [41   45]  47   50   2 400
rangs 4 et 5  →  médiane = (41 + 45) ÷ 2 = 43 €
```

La médiane passe de 41 à 43 €, quand la moyenne passait de 40 à 335 €. **La médiane est robuste** :
elle résiste aux valeurs extrêmes, parce qu'elle ne regarde que le rang des valeurs, pas leur
grandeur.

### À partir d'un tableau d'effectifs

On utilise les **effectifs cumulés** : la médiane est la première valeur dont l'effectif cumulé
atteint la moitié de n.

Articles par commande, n = 30, moitié = 15. Les effectifs cumulés sont 12, 20, 25, 28, 30. Le
premier à atteindre 15 est **20**, sur la ligne « 2 articles ». Les 15ᵉ et 16ᵉ commandes ont toutes
deux 2 articles : **médiane = 2**.

Une commande « typique » a 2 articles, alors que la moyenne dit 2,6. Les deux commandes à 10 articles
tirent la moyenne.

### Propriétés

- Décalage et échelle : comme la moyenne, si on ajoute c ou multiplie par k toutes les valeurs, la
  médiane suit.
- **Robustesse** : remplacer la plus grande valeur par une valeur encore plus grande ne change rien.
- La médiane n'a **pas** la propriété du total : médiane × n ne redonne pas la somme.
- Elle se définit aussi pour une variable **ordinale** (la note médiane est 4), pas pour une
  variable nominale.

---

## 4. Le mode

### Définition

**Le mode** est la valeur (ou la modalité) **la plus fréquente** : celle qui a le plus grand effectif.

- Articles par commande : le mode est **1** (12 commandes sur 30).
- Magasin des commandes : le mode est le magasin qui revient le plus souvent.
- Tailles vendues `M, L, M, S, M, L, XL, M` : le mode est **M**.

C'est la **seule** mesure de position qui existe pour une variable qualitative nominale.

### Ce qu'il faut savoir

- Une série peut n'avoir **aucun mode** (toutes les valeurs différentes : les 7 paniers) ou
  **plusieurs** (série bimodale : deux pics, par exemple des petits paniers de dépannage et des gros
  paniers de courses hebdomadaires). Deux modes, c'est souvent **deux populations mélangées** : une
  information précieuse.
- Sur une variable continue (des montants avec des centimes), le mode brut n'a guère de sens : on
  parle alors de **classe modale**, la tranche la plus fournie de l'histogramme.
- Un mode qui gagne d'une seule voix (225 notes à 5 contre 224 à 4) ne mérite pas d'être présenté
  comme « la note des clients ».

---

## 5. Choisir la bonne mesure

### Ce que chacune raconte

| Mesure | Répond à | Sensible aux valeurs extrêmes | Variables possibles |
|---|---|---|---|
| **Moyenne** | « si on partageait à parts égales » ; sert aux totaux et aux prévisions de volume | **oui, fortement** | quantitatives |
| **Médiane** | « la valeur du milieu », l'individu typique | **non** | quantitatives, ordinales |
| **Mode** | « le cas le plus fréquent » | non | toutes, la seule pour le nominal |

### Lire la forme de la distribution

Comparer moyenne et médiane renseigne sur la **forme** de la série, avant même de dessiner un
histogramme :

| Constat | Forme de la distribution | Ce qui se passe | Mesure à donner |
|---|---|---|---|
| moyenne ≈ médiane | **symétrique** | autant de petites que de grandes valeurs, pas d'extrême | la moyenne convient (donner les deux ne coûte rien) |
| moyenne **>** médiane | **étalée à droite** (asymétrie positive) | quelques valeurs très grandes tirent la moyenne vers le haut | **la médiane** |
| moyenne **<** médiane | **étalée à gauche** (asymétrie négative) | quelques valeurs très petites tirent la moyenne vers le bas | **la médiane** |

![Trois formes de distribution : symétrique (moyenne ≈ médiane), étalée vers la droite (moyenne > médiane : salaires, prix, montants de commande), étalée vers la gauche (moyenne < médiane)](../../../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/images/formes-de-distribution.svg)

Les montants d'argent (salaires, prix, paniers, patrimoines), les durées (délais, temps d'attente) et
les tailles de villes sont presque toujours **étalés à droite** : il y a un plancher (zéro) mais pas
de plafond. C'est pourquoi l'INSEE publie un **salaire médian** et un **niveau de vie médian**, jamais
moyens, quand il s'agit de décrire « le Français typique ».

### Sur des données réelles

Les 613 commandes d'un réseau de magasins de vélos (fichier `Ventes_2025` du module tableur) :

| Mesure | Valeur | Lecture |
|---|---|---|
| Mode | 19,00 € | la commande la plus fréquente : une réparation de chambre à air |
| Médiane | 177,00 € | la commande du milieu : un accessoire |
| Moyenne | 1 679,77 € | un montant que peu de commandes atteignent |

Moyenne 9,5 fois plus grande que la médiane : distribution très étalée à droite, à cause de quelques
vélos électriques et d'une commande de flotte à 379 050 €. Pour dire « une commande typique », on
donne la médiane. Pour calculer le chiffre d'affaires, on utilise la moyenne × n, ou directement la
somme.

### La phrase de restitution

Un chiffre ne se donne jamais seul. La phrase complète contient **l'indicateur, sa valeur, le
périmètre et l'effectif** :

- ❌ « La commande moyenne est de 1 680 €. »
- ✅ « Sur les 613 commandes de 2025, la commande médiane est de 177 €. La moyenne (1 680 €) est
  tirée vers le haut par quelques grosses commandes de vélos électriques. »

---

## 6. Dans le tableur

Google Sheets et Excel calculent ces mesures avec les fonctions suivantes (nom anglais de Sheets,
nom français d'Excel entre parenthèses). `plage` désigne les cellules de la série.

| Mesure | Fonction | Remarque |
|---|---|---|
| Effectif | `COUNT(plage)` (NB) | ne compte que les cellules contenant un **nombre** ; `COUNTA` (NBVAL) compte toutes les cellules non vides |
| Moyenne | `AVERAGE(plage)` (MOYENNE) | **ignore les cellules vides**, mais compte les zéros |
| Médiane | `MEDIAN(plage)` (MEDIANE) | trie pour toi |
| Mode | `MODE(plage)` (MODE) | renvoie une erreur s'il n'y a pas de mode |
| Moyenne à partir d'effectifs | `SUMPRODUCT(valeurs; effectifs) / SUM(effectifs)` (SOMMEPROD) | c'est la formule Σ nᵢxᵢ ÷ n |

À faire : saisis les 7 paniers dans une colonne, vérifie 40,29 et 41. Ajoute 2 400, vérifie 335,25
et 43.

---

## Exercices

> Papier et calculatrice. Le corrigé est sous chaque énoncé, à n'ouvrir qu'après avoir répondu.

### Exercice 1 — Types de variables

Voici les colonnes d'un fichier de communes. Donne le type de chacune et dis si une moyenne a un sens.

`Code_INSEE` · `Commune` · `Departement` · `Population` · `Superficie_km2` · `Taille_commune`
(cinq tranches, de « moins de 200 habitants » à « plus de 20 000 ») · `Taux_pauvrete`

<details>
<summary>Corrigé</summary>

| Colonne | Type | Moyenne ? |
|---|---|---|
| `Code_INSEE` | identifiant (faux nombre) | non |
| `Commune` | qualitative nominale | non |
| `Departement` | qualitative nominale | non ; on peut compter les communes par département |
| `Population` | quantitative discrète | oui, mais la médiane sera plus parlante (distribution étalée à droite) |
| `Superficie_km2` | quantitative continue | oui |
| `Taille_commune` | qualitative **ordinale** | non ; mode et médiane possibles |
| `Taux_pauvrete` | quantitative continue | oui, à condition de pondérer par la population si on veut un taux régional (partie 3) |

</details>

### Exercice 2 — Moyenne, médiane, mode

Notes de satisfaction (de 1 à 5) laissées par 8 clients : `5, 4, 5, 3, 5, 4, 2, 5`.

1. Calcule la moyenne, la médiane et le mode.
2. Quelle mesure donnerais-tu au directeur, et pourquoi ?

<details>
<summary>Corrigé</summary>

1. Somme = 33, n = 8 → moyenne = 33 ÷ 8 = **4,125**.
   Série rangée : `2, 3, 4, 4, 5, 5, 5, 5` ; n pair, rangs 4 et 5 → médiane = (4 + 5) ÷ 2 = **4,5**.
   Mode = **5** (4 fois sur 8).
2. La note est une variable ordinale : la moyenne 4,125 se calcule mais l'écart entre 2 et 3 n'est
   pas garanti égal à l'écart entre 4 et 5. On donne plutôt : « la moitié des clients mettent 5, la
   note médiane est 4,5 ; un client sur 8 met 2 ». Le mode (5) et la médiane suffisent, la moyenne
   peut accompagner.

</details>

### Exercice 3 — À partir d'un tableau d'effectifs

Nombre de vélos vendus par jour dans un magasin, sur 20 jours :

| Vélos vendus | 0 | 1 | 2 | 3 | 6 |
|---|---|---|---|---|---|
| Nombre de jours | 4 | 7 | 5 | 3 | 1 |

Calcule la moyenne, la médiane et le mode. Combien de vélos le magasin a-t-il vendus sur les 20 jours ?

<details>
<summary>Corrigé</summary>

- Effectif total : 4 + 7 + 5 + 3 + 1 = **20 jours**.
- Total vendu : (4 × 0) + (7 × 1) + (5 × 2) + (3 × 3) + (1 × 6) = 0 + 7 + 10 + 9 + 6 = **32 vélos**.
- Moyenne : 32 ÷ 20 = **1,6 vélo par jour**.
- Effectifs cumulés : 4, 11, 16, 19, 20. La moitié de 20 est 10 : la 10ᵉ et la 11ᵉ valeurs sont
  dans la ligne « 1 » (rangs 5 à 11). Médiane = **1**.
- Mode = **1** (7 jours).

Un jour typique, le magasin vend 1 vélo ; en moyenne 1,6, parce qu'un jour à 6 vélos et trois jours à
3 tirent la moyenne. Pour prévoir le stock du mois, on utilise la moyenne (1,6 × 20 = 32).

</details>

### Exercice 4 — Propriétés de la moyenne

Le prix moyen des 40 références d'un rayon est de 40 €.

1. Le magasin augmente tous les prix de 5 €. Nouveau prix moyen ?
2. Il applique plutôt une hausse de 10 % sur tous les prix. Nouveau prix moyen ?
3. Quel est le total des 40 prix, avant hausse ?

<details>
<summary>Corrigé</summary>

1. Décalage : 40 + 5 = **45 €**.
2. Échelle : 40 × 1,10 = **44 €**.
3. Total = moyenne × n = 40 × 40 = **1 600 €**.

</details>

### Exercice 5 — Retrouver une valeur manquante

Cinq magasins ont un chiffre d'affaires moyen de 20 k€. Quatre d'entre eux ont fait 12, 18, 25 et
30 k€. Combien a fait le cinquième ?

<details>
<summary>Corrigé</summary>

Total = 20 × 5 = 100 k€. Les quatre connus font 12 + 18 + 25 + 30 = 85 k€. Le cinquième a fait
100 − 85 = **15 k€**.

</details>

### Exercice 6 — Choisir la mesure

Délais de livraison, en jours, de 9 commandes : `1, 1, 2, 2, 2, 3, 3, 4, 21`.

1. Moyenne, médiane, mode.
2. Le service client veut annoncer « un délai habituel » sur le site. Lequel ? Et que fait-on du 21 ?

<details>
<summary>Corrigé</summary>

1. Somme = 39 → moyenne = 39 ÷ 9 = **4,33 jours**. Série déjà rangée, n = 9, rang 5 → médiane =
   **2 jours**. Mode = **2** (3 fois).
2. Moyenne > médiane : une valeur extrême (21) tire la moyenne. Annoncer 4 jours ferait croire que
   les livraisons sont deux fois plus lentes qu'elles ne le sont pour la plupart des clients. On
   annonce **« 2 jours habituellement »** (médiane, ou mode). Le 21 n'est pas supprimé : on cherche
   pourquoi (commande spéciale ? incident ?) et on le signale à part, par exemple « 1 commande sur 9
   a mis plus d'une semaine ».

</details>

---

➡️ Partie suivante : [2 — La dispersion](02-dispersion.md)
