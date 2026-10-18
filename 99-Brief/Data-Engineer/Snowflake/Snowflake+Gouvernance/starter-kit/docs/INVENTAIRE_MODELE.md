# Inventaire des données personnelles — <nom du fichier ou de la table>

Un inventaire par source. Copier ce fichier, le renommer (`inventaire_drivers.md`, `inventaire_driver_shifts.md`) et le compléter avant tout chargement.

Une donnée personnelle est une information qui se rapporte à une personne identifiée ou identifiable. Trois cas à distinguer :

- **identifiant direct** : la colonne suffit à désigner la personne (un nom, un e-mail) ;
- **identifiant indirect** : la colonne ne suffit pas seule, mais permet d'identifier quelqu'un une fois combinée à d'autres (une date de naissance et un dépôt) ;
- **pas une donnée personnelle** : la colonne ne dit rien d'une personne.

## Colonnes

| Colonne | Exemple de valeur | Donnée personnelle ? (direct, indirect, non) | Valeur du tag `DONNEE_PERSONNELLE` | Qui en a besoin, et pour quoi faire |
|---|---|---|---|---|
| | | | | |

## Où cette donnée est-elle copiée ?

Pour chaque colonne personnelle : la liste des tables et des vues de l'entrepôt où elle se retrouve, y compris sous une autre forme (colonne renommée, colonne calculée). À compléter au fil des trois jours.

| Colonne d'origine | Table ou vue | Colonne | Sous quelle forme |
|---|---|---|---|
| | | | |

## Ce qui a surpris

Deux ou trois lignes : une colonne plus sensible que prévu, une colonne dont personne n'a besoin, une donnée qui n'aurait pas dû être dans le fichier.
