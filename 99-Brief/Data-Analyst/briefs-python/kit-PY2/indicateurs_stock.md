# Dictionnaire des indicateurs — exemple « suivi de stock »

Un indicateur = un intitulé, l'objectif (quelle décision il éclaire), une définition fonctionnelle, une formule, une unité. À reproduire pour vos trois indicateurs d'objectifs dans `indicateurs_objectifs.md`.

## Unités en stock

- **Objectif** : savoir si l'entrepôt est globalement plein ou vide avant une commande fournisseur.
- **Définition** : nombre total d'unités physiquement présentes, tous produits confondus.
- **Formule** : somme des `stock` de chaque produit.
- **Unité** : unités (u).
- **Classe** : `StockTotal`.

## Valeur du stock

- **Objectif** : chiffrer l'argent immobilisé en entrepôt pour le contrôleur de gestion.
- **Définition** : valeur d'achat des unités en stock.
- **Formule** : somme, pour chaque produit, de `stock × prix_unitaire`.
- **Unité** : euros (€).
- **Classe** : `ValeurStock`.

## Produits en rupture

- **Objectif** : déclencher les réassorts prioritaires.
- **Définition** : nombre de produits référencés dont le stock est à zéro.
- **Formule** : nombre de produits tels que `stock == 0`.
- **Unité** : nombre de produits.
- **Classe** : `NbRuptures`.
