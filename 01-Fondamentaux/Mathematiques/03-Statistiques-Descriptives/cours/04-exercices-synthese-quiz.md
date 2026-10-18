# Partie 4 — Exercices de synthèse et quiz

Deux exercices longs qui mobilisent les trois parties, sur des **données réelles**, puis un quiz de
15 questions. Papier d'abord ; le tableur ensuite, pour vérifier.

---

## Exercice A — Quatre intercommunalités à la main

Quatre intercommunalités des Hauts-de-France, population 2023 arrondie et taux de pauvreté 2023
(source INSEE, comparateur de territoires) :

| Intercommunalité | Population | Taux de pauvreté |
|---|---|---|
| Métropole Européenne de Lille | 1 195 000 | 21,4 % |
| CC du Sud Avesnois | 24 000 | 29,7 % |
| CC Senlis Sud Oise | 25 000 | 8,8 % |
| CC de l'Aire Cantilienne | 45 000 | 7,1 % |

1. Type de chaque colonne.
2. Moyenne simple des quatre taux. Médiane.
3. Nombre de personnes pauvres dans chaque intercommunalité, puis dans l'ensemble.
4. Taux de pauvreté de l'ensemble des quatre (moyenne pondérée par la population).
5. Pourquoi la moyenne simple et la pondérée diffèrent-elles autant ? Laquelle répond à « quelle
   part des habitants de ces quatre territoires est pauvre ? », laquelle à « quel est le taux d'une
   intercommunalité typique parmi ces quatre ? »
6. Une agence doit aider **un** de ces territoires. Le Sud Avesnois a le taux le plus fort, la
   Métropole le plus grand nombre de pauvres. Rédige deux phrases, une pour chaque choix, chacune
   avec son indicateur, sa valeur et son effectif.

<details>
<summary>Corrigé</summary>

1. Nom : qualitative nominale. Population : quantitative discrète. Taux : quantitative continue.
2. Simple : (21,4 + 29,7 + 8,8 + 7,1) ÷ 4 = 67 ÷ 4 = **16,75 %**. Rangés : 7,1 · 8,8 · 21,4 · 29,7 ;
   n pair → médiane = (8,8 + 21,4) ÷ 2 = **15,1 %**.
3. Lille : 1 195 000 × 0,214 = **255 730**. Sud Avesnois : 24 000 × 0,297 = **7 128**. Senlis :
   25 000 × 0,088 = **2 200**. Aire Cantilienne : 45 000 × 0,071 = **3 195**. Total **268 253**
   personnes pauvres.
4. Population totale : 1 289 000. Taux = 268 253 ÷ 1 289 000 = **20,8 %**. C'est la moyenne
   pondérée : (1 195 000 × 21,4 + 24 000 × 29,7 + 25 000 × 8,8 + 45 000 × 7,1) ÷ 1 289 000.
5. La Métropole contient 93 % des habitants des quatre : le taux de l'ensemble est presque le sien.
   La moyenne simple laisse trois petites intercommunalités peser autant qu'elle. **Pondérée** →
   part des habitants ; **simple** → intercommunalité typique (et sur quatre unités, la médiane
   15,1 % est plus honnête encore).
6. « Sur les quatre territoires, le Sud Avesnois a le taux de pauvreté le plus élevé : 29,7 %, soit
   7 100 personnes sur 24 000. » / « La Métropole de Lille concentre 255 700 personnes pauvres, soit
   95 % des personnes pauvres des quatre territoires, avec un taux de 21,4 %. » Les deux phrases sont
   vraies ; le choix entre intensité et volume n'est pas statistique, il est politique. Le
   statisticien fournit les deux.

</details>

---

## Exercice B — Le portrait des 92 intercommunalités

Voici les résumés calculés sur les 92 intercommunalités des Hauts-de-France (INSEE, 2023).

| Mesure | Taux de pauvreté (%) | Niveau de vie médian (€ par an) |
|---|---|---|
| Minimum | 7,0 | 19 250 (CA Creil Sud Oise) |
| Q1 | 12,0 | 23 148 |
| Médiane | 14,5 | 24 350 |
| Q3 | 20,15 | 25 688 |
| Maximum | 33,5 (CA Creil Sud Oise) | 34 810 (CC de l'Aire Cantilienne) |
| Moyenne simple | 16,1 | 24 483 |
| Moyenne pondérée par la population | 19,1 | 23 979 |
| Écart-type (÷ n) | 5,6 | 2 321 |

1. Pour chaque variable : étendue, écart interquartile, coefficient de variation.
2. Pour chaque variable, moyenne simple contre médiane : quelle forme de distribution ?
3. Pour chaque variable, bornes de la règle 1,5 × IQR. Les valeurs extrêmes données sont-elles
   atypiques ? *(Pour le niveau de vie, trois autres intercommunalités valent 29 620, 31 670 et
   20 100 €.)*
4. Le taux publié par l'INSEE pour la région est 19 %. Quelle moyenne le retrouve, et pourquoi
   l'autre est-elle plus basse ?
5. Pour le niveau de vie, la moyenne pondérée (23 979 €) est **inférieure** à la simple (24 483 €).
   Que dit ce signe sur les grandes agglomérations, comparées aux petites intercommunalités ?
6. Écris trois phrases de restitution pour une directrice d'agence : une sur le taux typique, une
   sur la dispersion, une sur le territoire le plus en difficulté.

<details>
<summary>Corrigé</summary>

1. Taux : étendue 33,5 − 7,0 = **26,5 points** ; IQR = 20,15 − 12,0 = **8,15** ; CV = 5,6 ÷ 16,1 =
   **35 %**. Niveau de vie : étendue 34 810 − 19 250 = **15 560 €** ; IQR = 25 688 − 23 148 =
   **2 540 €** ; CV = 2 321 ÷ 24 483 = **9,5 %**.
   Le taux de pauvreté est une variable très dispersée entre territoires (CV 35 %), le niveau de vie
   médian beaucoup moins (9,5 %).
2. Taux : moyenne 16,1 > médiane 14,5 → **étalée à droite** : quelques territoires très pauvres.
   Niveau de vie : moyenne 24 483 > médiane 24 350, écart faible (0,5 %) → **à peu près
   symétrique**, avec une légère traîne vers les hauts niveaux de vie.
3. Taux : bornes 12 − 12,2 = −0,2 et 20,15 + 12,2 = **32,4**. Creil Sud Oise (33,5) est atypique,
   seul. Niveau de vie : bornes 23 148 − 3 810 = **19 338** et 25 688 + 3 810 = **29 498**. Creil
   (19 250) est atypique **par le bas** ; 29 620, 31 670 et 34 810 sont atypiques par le haut (les
   intercommunalités aisées du sud de l'Oise, près de Paris) ; 20 100 ne l'est pas.
   Creil Sud Oise est atypique sur les deux variables, dans le sens attendu : le territoire le plus
   pauvre a le niveau de vie le plus bas. Ce n'est pas une erreur de données.
4. La **pondérée** (19,1 %) retrouve le chiffre régional : le taux régional est une part des
   habitants, pas une part des intercommunalités. La simple (16,1 %) est plus basse parce que les
   intercommunalités rurales, nombreuses et peu peuplées, ont des taux plus faibles que les grandes
   agglomérations où vivent la plupart des habitants.
5. Pondérer par la population fait **baisser** le niveau de vie : les territoires peuplés ont un
   niveau de vie plus bas que la moyenne des territoires. Même message qu'au point 4, vu par l'autre
   bout : les grandes agglomérations des Hauts-de-France sont, en moyenne, plus pauvres que leurs
   campagnes.
6. Par exemple : « Sur les 92 intercommunalités, le taux de pauvreté médian est de 14,5 % ; la
   moitié des territoires se situent entre 12 et 20 %. » / « Les écarts sont grands : de 7 % à
   33,5 %, et l'écart-type (5,6 points) vaut plus du tiers de la moyenne. » / « La CA Creil Sud
   Oise est hors norme : 33,5 % de pauvres, soit 30 200 personnes sur 90 200, et le niveau de vie le
   plus bas de la région (19 250 €). »

</details>

---

## Quiz — 15 questions

Une seule bonne réponse par question. Le corrigé est en bas.

**1.** La somme des écarts à la moyenne d'une série vaut :
a) toujours 0 · b) toujours n · c) la variance · d) cela dépend de la série

**2.** Sur la série `3, 5, 5, 6, 8, 9, 20`, la médiane est :
a) 5 · b) 6 · c) 8 · d) 8,29

**3.** Une distribution où la moyenne est nettement supérieure à la médiane est :
a) symétrique · b) étalée à gauche · c) étalée à droite · d) bimodale

**4.** Un code postal est une variable :
a) quantitative discrète · b) quantitative continue · c) qualitative nominale · d) ordinale

**5.** L'écart-type s'exprime :
a) sans unité · b) dans l'unité des données · c) dans l'unité des données au carré · d) en %

**6.** Si on ajoute 10 à toutes les valeurs d'une série, l'écart-type :
a) augmente de 10 · b) est multiplié par 10 · c) ne change pas · d) devient nul

**7.** Le coefficient de variation vaut :
a) σ ÷ x̄ · b) x̄ ÷ σ · c) Q3 − Q1 · d) σ²

**8.** « La moitié des valeurs sont comprises entre 50 et 1 790 € » : 50 et 1 790 sont :
a) le minimum et le maximum · b) Q1 et Q3 · c) la médiane et la moyenne · d) D1 et D9

**9.** Q1 = 4, Q3 = 8. Selon la règle de 1,5 × IQR, une valeur de 15 est :
a) normale · b) atypique · c) impossible à dire · d) la médiane

**10.** La mesure de position robuste aux valeurs extrêmes est :
a) la moyenne · b) la médiane · c) l'écart-type · d) l'étendue

**11.** Trois magasins ont des paniers moyens de 40, 60 et 100 € pour 200, 50 et 10 clients. Le
panier moyen de l'ensemble des clients est :
a) 66,67 € · b) 46,15 € · c) 60 € · d) 200 €

**12.** Un taux passe de 16 % à 19 %. Il a augmenté de :
a) 3 % · b) 3 points · c) 19 % · d) 16 points

**13.** `STDEV` dans Google Sheets divise par :
a) n · b) n − 1 · c) n + 1 · d) 2

**14.** Un prix monte de 50 % puis baisse de 50 %. Au total il a :
a) retrouvé son niveau · b) baissé de 25 % · c) monté de 25 % · d) baissé de 50 %

**15.** Dans une boîte à moustaches, la boîte représente :
a) toutes les valeurs · b) la moitié centrale des valeurs · c) la moyenne ± écart-type · d) les
valeurs atypiques

<details>
<summary>Corrigé du quiz</summary>

| Q | Réponse | Rappel |
|---|---|---|
| 1 | **a** | propriété de la moyenne (partie 1) |
| 2 | **b** | n = 7, rang 4 → 6 |
| 3 | **c** | quelques grandes valeurs tirent la moyenne vers le haut |
| 4 | **c** | un faux nombre : étiquette sans ordre |
| 5 | **b** | c'est la variance qui est au carré |
| 6 | **c** | les écarts entre valeurs ne bougent pas |
| 7 | **a** | dispersion rapportée à la moyenne |
| 8 | **b** | l'intervalle interquartile contient la moitié centrale |
| 9 | **b** | IQR = 4, borne haute = 8 + 6 = 14 |
| 10 | **b** | elle ne regarde que les rangs |
| 11 | **b** | 12 000 € ÷ 260 clients |
| 12 | **b** | en pourcentage, ce serait + 19 % |
| 13 | **b** | écart-type d'échantillon ; `STDEVP` divise par n |
| 14 | **b** | 1,5 × 0,5 = 0,75 |
| 15 | **b** | de Q1 à Q3 |

12 bonnes réponses ou plus : le socle est acquis. En dessous de 9 : refaire les exercices de la
partie concernée avant de passer à l'outil.

</details>

---

⬅️ [3 — Les pièges de la moyenne](03-pieges-de-la-moyenne.md) · ➡️ [5 — Mémo des formules](05-memo-formules.md)
