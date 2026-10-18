# Mémo — Statistiques descriptives sur une page

Notations : n = effectif · xᵢ = i-ème valeur · x̄ = moyenne · Σ = « additionne tout ».

## Position

| Mesure | Formule ou méthode | Ce qu'elle dit | Sensible aux extrêmes | Sheets (Excel FR) |
|---|---|---|---|---|
| **Moyenne** | x̄ = Σxᵢ ÷ n | partage à parts égales ; × n redonne le total | **oui** | `AVERAGE` (MOYENNE) |
| **Moyenne à partir d'effectifs** | Σnᵢxᵢ ÷ n | idem, valeurs regroupées | oui | `SUMPRODUCT(x; n)/SUM(n)` |
| **Moyenne pondérée** | Σwᵢxᵢ ÷ Σwᵢ | chaque valeur compte selon son poids | oui | `SUMPRODUCT(x; w)/SUM(w)` (SOMMEPROD) |
| **Médiane** | trier ; rang (n+1)/2 si n impair, moyenne des rangs n/2 et n/2+1 si pair | la valeur du milieu, l'individu typique | **non** | `MEDIAN` (MEDIANE) |
| **Mode** | valeur la plus fréquente | le cas le plus courant ; seule mesure pour le nominal | non | `MODE` |

**Lire la forme** : moyenne ≈ médiane → symétrique · moyenne > médiane → étalée à droite (donner la
médiane) · moyenne < médiane → étalée à gauche.

## Dispersion

| Mesure | Formule ou méthode | Ce qu'elle dit | Robuste | Sheets (Excel FR) |
|---|---|---|---|---|
| **Étendue** | max − min | l'écart entre les deux extrêmes | non | `MAX(…)-MIN(…)` |
| **Variance** (population) | V = Σ(xᵢ − x̄)² ÷ n | moyenne des carrés des écarts ; unité au carré | non | `VARP` (VAR.P) |
| **Écart-type** (population) | σ = √V | distance typique à la moyenne ; même unité que les données | non | `STDEVP` (ECARTYPE.PEARSON) |
| **Écart-type** (échantillon) | s = √(Σ(xᵢ − x̄)² ÷ (n − 1)) | idem, corrigé pour un échantillon ; **le défaut des outils** | non | `STDEV` (ECARTYPE.STANDARD) |
| **Coefficient de variation** | CV = σ ÷ x̄ | dispersion relative ; < 15 % homogène, > 30 % moyenne peu fiable | non | `STDEVP(…)/AVERAGE(…)` |
| **Quartiles** | trier ; Q1 au rang ⌈n/4⌉, Q3 au rang ⌈3n/4⌉ (les outils interpolent) | coupent la série en quatre parts égales | **oui** | `QUARTILE(…; 1)`, `QUARTILE(…; 3)` |
| **Écart interquartile** | IQR = Q3 − Q1 | largeur de la moitié centrale | **oui** | `QUARTILE(…;3)-QUARTILE(…;1)` |
| **Déciles, centiles** | même principe en 10 ou 100 parts | « le 9ᵉ décile » : seuil des 10 % les plus hauts | oui | `PERCENTILE(…; 0,9)` (CENTILE) |

## Valeurs atypiques et boîte à moustaches

- **Règle de 1,5 × IQR** : atypique si x < Q1 − 1,5 × IQR ou x > Q3 + 1,5 × IQR.
- Atypique ≠ faux. Trois cas : erreur (corriger ou écarter en le disant), vraie valeur rare (garder,
  mesures robustes), autre population (séparer). **Jamais de suppression silencieuse.**
- **Boîte à moustaches** : boîte de Q1 à Q3, trait à la médiane, moustaches jusqu'aux dernières
  valeurs à l'intérieur des bornes, points isolés au-delà.

## Pourcentages

| Besoin | Formule |
|---|---|
| Part | partie ÷ total |
| Évolution | (nouveau − ancien) ÷ ancien |
| Évolutions successives | on **multiplie** les coefficients : +50 % puis −50 % → 1,5 × 0,5 = 0,75 (−25 %) |
| Écart entre deux taux | en **points** (16 % → 19 % : + 3 points, soit + 19 %) |
| Taux global de plusieurs groupes | Σ numérateurs ÷ Σ dénominateurs, jamais la moyenne des taux |

## Les six pièges de la moyenne

1. **Valeurs extrêmes** → médiane, signaler.
2. **Distribution asymétrique** → histogramme, médiane et quartiles.
3. **Effectifs déséquilibrés** → moyenne pondérée.
4. **Moyenne de moyennes**, paradoxe de Simpson → comparer à composition égale, additionner les comptes.
5. **Pourcentages** → points, base, dénominateur.
6. **Manquants, zéros, petits effectifs, périmètre** → compter, annoncer l'effectif, regrouper.

## La phrase de restitution

**Indicateur + valeur + périmètre + effectif.**
« Sur les 613 commandes de 2025, la commande médiane est de 177 € ; la moyenne (1 680 €) est tirée
vers le haut par quelques grosses commandes. »

## Notation mathématique, pour lire les livres

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i \qquad
\sigma^2 = \frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^2 \qquad
\sigma = \sqrt{\sigma^2} \qquad
\bar{x}_w = \frac{\sum_i w_i x_i}{\sum_i w_i}$$

⬅️ [Sommaire du cours](README.md)
