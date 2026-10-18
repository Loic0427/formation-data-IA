# Cours Snowflake : de la prise en main à la certification SnowPro Core

Ce cours s'adresse à des apprenants Data Engineer qui découvrent Snowflake. Il part de la création d'un compte d'essai et va jusqu'à la préparation de la certification SnowPro Core. Aucune connaissance préalable de Snowflake n'est nécessaire ; des bases de SQL suffisent.

Chaque chapitre explique d'abord pourquoi on fait un geste et le concept qu'il y a derrière, puis comment le faire, dans l'interface Snowsight et en SQL. Il se termine par une section « À retenir pour la certification ».

## Sommaire

### Partie 1 : prise en main

1. [Création d'un compte Snowflake](01-creation-compte.md)
2. [Connexion à Snowflake et découverte de Snowsight](02-connexion.md)
3. [Création d'un rôle personnalisé](03-creation-role.md)
4. [Création d'un warehouse](04-creation-warehouse.md)
5. [Création d'une base de données et d'un schéma](05-creation-database-schema.md)
6. [Création des tables](06-creation-tables.md)
7. [Import de données CSV](07-import-donnees.md)
8. [Gestion des privilèges](08-gestion-privileges.md)
9. [Suivi de l'activité et des coûts](09-monitoring.md)

### Partie 2 : pratiquer en SQL

10. [Sécurité : rôles, droits et utilisateurs de service en SQL](10-securite.md)
11. [Charger des fichiers en SQL : format de fichier, stage, PUT et COPY INTO](11-chargement-stage-copy.md)

### Partie 3 : concepts pour la certification

12. [Architecture de Snowflake](12-architecture.md)
13. [Stockage, types de tables, Time Travel, Fail-safe, clonage](13-stockage-protection.md)
14. [Fonctions d'IA, Snowpark, Streamlit et outils](14-ia-applications.md)
15. [Authentification, politiques réseau, masquage, gouvernance](15-gouvernance.md)
16. [Snowpipe, export, connecteurs](16-snowpipe-export-connectivite.md)
17. [Performance et optimisation](17-performance.md)
18. [Données semi-structurées, streams, tasks, tables dynamiques, fonctions](18-transformation.md)
19. [Partage de données, Marketplace, réplication](19-collaboration.md)

### Préparer l'examen

- [Plan de révision en 8 jours](certification/PLAN.md)
- Un quiz par chapitre, dans le dossier [`certification/`](certification/)
- [Examen blanc n° 1](certification/examen-blanc-1.md)

## L'examen SnowPro Core (COF-C03)

| | |
|---|---|
| Nombre de questions | 100 |
| Durée | 115 minutes |
| Seuil de réussite | 750 sur 1000 |
| Langue | disponible en français |

| Domaine (intitulé officiel) | Pondération |
|---|---|
| 1.0 Caractéristiques et architecture de l'AI Data Cloud de Snowflake | 31 % |
| 2.0 Gestion des comptes et gouvernance des données | 20 % |
| 3.0 Chargement/Déchargement des données et connectivité | 18 % |
| 4.0 Optimisation des performances, requêtes et transformation | 21 % |
| 5.0 Collaboration sur les données | 10 % |

Ces chiffres sont ceux de la [page officielle de l'examen en français](https://learn.snowflake.com/en/certifications/snowpro-core-fra-c03/), relevés le 4 octobre 2026 : frais d'inscription de 175 USD, aucun prérequis, passage en ligne surveillé ou en centre d'examen, langues anglais, japonais, coréen, français et espagnol. Le programme étant révisé régulièrement, vérifiez-les avant de vous inscrire. Le guide d'étude détaillé, qui liste les objectifs de chaque domaine, se télécharge depuis cette page.

## Prérequis

- Un navigateur récent (Chrome, Firefox, Edge ou Safari).
- Une adresse e-mail pour créer un compte d'essai : 30 jours, avec un solde d'usage gratuit, sans carte bancaire. Choisissez l'édition **Enterprise** ([chapitre 1](01-creation-compte.md)).
- À partir du chapitre 10 : un terminal et Python 3.

## L'exemple suivi

Tous les chapitres travaillent sur le même exemple de ventes en ligne :

| Objet | Nom |
|---|---|
| Warehouse | `SALES_WH` |
| Base de données | `SALES_DB` |
| Schémas | `RAW_DATA` (données brutes), `ANALYTICS` (tables d'analyse) |
| Tables de la partie 1 | `CUSTOMERS`, `PRODUCTS`, `ORDERS`, `ORDER_ITEMS` |
| Rôles | `SALES_ANALYST` (lecture), `SALES_ENGINEER` (chargement et transformation) |

## Les jeux de données

Le dossier `Data/` contient quatre jeux de données au format CSV, pour s'exercer :

| Dossier | Contenu |
|---|---|
| `Data/ecommerce/` | clients, produits, catégories, fournisseurs, commandes, lignes de commande, paiements, avis |
| `Data/finance/` | clients, comptes, transactions |
| `Data/saas/` | offres, utilisateurs, abonnements, événements d'usage |
| `Data/airbnb/` | hôtes, annonces, avis (plus de 400 000 lignes), fréquentation touristique par année |

La partie 1 utilise de petits fichiers à créer soi-même ([chapitre 7](07-import-donnees.md)) ; le dossier `Data/` sert à partir du chapitre 11.

## Comment suivre le cours

- Suivez la partie 1 dans l'ordre : chaque chapitre utilise les objets créés au précédent.
- L'interface Snowsight évolue souvent et ses libellés peuvent différer de ceux du cours. En cas d'écart, fiez-vous à la commande SQL donnée dans chaque chapitre : elle ne dépend pas de l'interface.
- Surveillez votre solde d'essai et suspendez les warehouses que vous n'utilisez pas ([chapitre 9](09-monitoring.md)).

## Ressources

- [Documentation officielle de Snowflake](https://docs.snowflake.com/)
- [Page de statut](https://status.snowflake.com/)
- Le dossier [`Cours/`](Cours/menu.md) : rappels sur l'entrepôt de données et la modélisation
