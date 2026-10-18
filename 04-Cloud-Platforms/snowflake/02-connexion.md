# 2. Connexion à Snowflake et découverte de Snowsight

[← Retour au sommaire](README.md) | [← Précédent](01-creation-compte.md) | [Suivant →](03-creation-role.md)

## Vue d'ensemble

Snowsight est l'interface web de Snowflake : on y écrit du SQL, on y explore les objets et on y administre le compte. Ce n'est qu'une des portes d'entrée : les mêmes commandes SQL fonctionnent depuis un outil en ligne de commande, un connecteur Python ou dbt.

Le concept à retenir dans ce chapitre est le **contexte de session** : chaque requête s'exécute avec un rôle (qui a le droit ?), un warehouse (qui calcule ?), une base et un schéma (où chercher les tables ?). La plupart des erreurs des débutants viennent d'un contexte mal réglé.

---

## 1. Se connecter

1. Ouvrez l'adresse de votre compte, notée au [chapitre 1](01-creation-compte.md) : `https://ORGANISATION-COMPTE.snowflakecomputing.com`. Vous pouvez aussi passer par https://app.snowflake.com et saisir votre identifiant de compte.
2. Saisissez le nom d'utilisateur et le mot de passe que vous avez choisis à l'activation du compte.
3. Si l'authentification multifacteur (MFA) n'est pas encore configurée, Snowsight vous propose de l'activer : faites-le. Elle se gère ensuite dans le menu utilisateur, **Settings**, rubrique **Authentication**.

![Page de connexion](images/10-login-page.png)
*Page de connexion de Snowflake*

---

## 2. Se repérer dans le menu de navigation

Le menu de gauche est organisé en trois groupes. Les libellés ci-dessous sont ceux de l'interface en anglais ; ils évoluent régulièrement, c'est pourquoi chaque chapitre donne aussi la commande SQL équivalente, qui ne change pas.

| Groupe | Entrée | Sert à | Chapitre |
|---|---|---|---|
| Work with data | **Projects** | écrire du SQL dans les **Workspaces** | 2 |
| Work with data | **Ingestion** | charger des fichiers (**Add Data**) | 7 |
| Work with data | **Transformation**, **AI & ML** | tables dynamiques, tâches, fonctions d'IA | 14, 18 |
| Work with data | **Monitoring** | historique des requêtes (**Query History**) | 9 |
| Work with data | **Marketplace** | jeux de données et applications partagés | 19 |
| Horizon Catalog | **Catalog** | explorer bases, schémas et tables | 5, 6 |
| Horizon Catalog | **Data sharing** | partages de données | 19 |
| Horizon Catalog | **Governance & security** | utilisateurs et rôles (**Users & roles**), politiques réseau | 3, 8 |
| Manage | **Compute** | warehouses | 4 |
| Manage | **Admin** | coûts (**Cost management**), comptes, facturation | 9 |

En bas à gauche, le **menu utilisateur** (votre nom) permet de changer de rôle (**Switch role**), d'afficher l'identifiant du compte (**View account details**) et d'ouvrir les réglages (**Settings**).

---

## 3. Écrire et exécuter du SQL : les Workspaces

Les fichiers SQL vivent dans des **Workspaces**, qui ont remplacé les anciennes « Worksheets » (encore accessibles, sous le nom de Legacy Worksheets). Un workspace contient des fichiers et des dossiers, comme un éditeur de code. Chaque utilisateur dispose d'un workspace privé, **My Workspace**.

1. Dans le menu, sélectionnez **Projects** » **Workspaces**.
2. Sélectionnez **+ Add new** puis **SQL File**, et nommez le fichier `02_verification.sql`.
3. Dans la barre du fichier, choisissez le contexte : rôle et warehouse (le compte d'essai fournit un warehouse `COMPUTE_WH`).
4. Collez la requête ci-dessous et exécutez-la avec `Cmd + Entrée` (macOS) ou `Ctrl + Entrée` (Windows).

```sql
SELECT
    CURRENT_USER()         AS utilisateur,
    CURRENT_ROLE()         AS role_actif,
    CURRENT_WAREHOUSE()    AS warehouse,
    CURRENT_DATABASE()     AS base,
    CURRENT_SCHEMA()       AS schema_courant,
    CURRENT_ACCOUNT_NAME() AS compte;
```

Le raccourci n'exécute que l'instruction où se trouve le curseur (ou la sélection). Le résultat montre votre contexte : `base` et `schema_courant` sont vides tant que vous n'en avez choisi aucun.

### Régler le contexte en SQL

Le contexte se choisit dans l'interface ou, de façon reproductible, en SQL :

```sql
USE ROLE SYSADMIN;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE SNOWFLAKE_SAMPLE_DATA;   -- base d'exemple fournie avec le compte d'essai
USE SCHEMA TPCH_SF1;

SELECT COUNT(*) FROM CUSTOMER;        -- le nom court suffit : base et schéma sont dans le contexte
```

Sans contexte, on écrit le nom complet de l'objet, sur trois niveaux : `BASE.SCHEMA.TABLE`.

```sql
SELECT COUNT(*) FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER;
```

---

## 4. Régler son profil

Dans le menu utilisateur, **Settings** permet de choisir :

| Réglage | Choix possibles |
|---|---|
| Langue de l'interface | English, Français, Deutsch, 日本語, 한국어, Português |
| Apparence | **Light**, **Dark** ou **System** |
| Rôle et warehouse par défaut dans Snowsight | un rôle et un warehouse auxquels vous avez accès |
| Authentification | ajout d'une méthode MFA |

Ce cours cite les libellés en anglais, qui correspondent à la documentation officielle. Si vous passez l'interface en français, les entrées sont traduites (**Projets**, **Supervision**, **Catalogue**, **Gouvernance et sécurité**, **Calculer**, **Administration**).

---

## 5. Les autres façons de se connecter

| Outil | Usage |
|---|---|
| Snowsight | interface web : exploration, SQL, administration |
| Snowflake CLI (`snow`), SnowSQL | ligne de commande, scripts, envoi de fichiers avec `PUT` |
| Connecteurs et pilotes (Python, JDBC, ODBC, Node.js, Go, .NET) | applications, dbt, Airflow, outils de BI |

Le [chapitre 10](10-securite.md) crée un utilisateur de service pour ces outils et le [chapitre 11](11-chargement-stage-copy.md) utilise le connecteur Python.

---

## 6. Sessions et historique

- Une session Snowsight inactive est fermée au bout de 18 heures par défaut ; pour les autres clients (connecteurs, ligne de commande), le délai par défaut est de 4 heures. Un administrateur peut modifier ces délais avec une politique de session.
- La page **Monitoring** » **Query History** affiche les requêtes des 14 derniers jours. Au-delà, on interroge la vue `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY`, qui conserve 365 jours ([chapitre 9](09-monitoring.md)).

---

## À retenir pour la certification

- Snowsight est l'interface web de Snowflake ; les autres accès sont la ligne de commande (Snowflake CLI, SnowSQL) et les pilotes et connecteurs (Python, JDBC, ODBC...).
- Le contexte d'une session comporte quatre éléments : rôle, warehouse, base de données, schéma. On les fixe avec `USE ROLE`, `USE WAREHOUSE`, `USE DATABASE`, `USE SCHEMA`.
- Les fonctions de contexte `CURRENT_USER()`, `CURRENT_ROLE()`, `CURRENT_WAREHOUSE()`, `CURRENT_DATABASE()`, `CURRENT_SCHEMA()` renvoient le contexte actif.
- Le nom complet d'un objet a trois niveaux : `BASE.SCHEMA.OBJET`.
- La page Query History de Snowsight couvre 14 jours ; la vue `ACCOUNT_USAGE.QUERY_HISTORY` conserve 365 jours.

## ✅ Points de vérification
- [ ] Connexion réussie, MFA activée
- [ ] Fichier SQL créé dans **My Workspace**
- [ ] Requête de contexte exécutée
- [ ] Requête sur `SNOWFLAKE_SAMPLE_DATA` réussie avec le nom complet de la table

## Documentation officielle
- [Démarrer avec Snowsight](https://docs.snowflake.com/en/user-guide/ui-snowsight-gs)
- [Visite rapide de Snowsight](https://docs.snowflake.com/en/user-guide/ui-snowsight-quick-tour)
- [Workspaces](https://docs.snowflake.com/en/user-guide/ui-snowsight/workspaces)
- [Profil et préférences](https://docs.snowflake.com/en/user-guide/ui-snowsight-profile)
- [Politiques de session](https://docs.snowflake.com/en/user-guide/session-policies)

---

[← Retour au sommaire](README.md) | [← Précédent](01-creation-compte.md) | [Suivant →](03-creation-role.md)
