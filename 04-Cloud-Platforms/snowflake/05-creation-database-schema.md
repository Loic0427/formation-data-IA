# 5. Création d'une base de données et d'un schéma

[← Retour au sommaire](README.md) | [← Précédent](04-creation-warehouse.md) | [Suivant →](06-creation-tables.md)

## Vue d'ensemble

Les objets de Snowflake sont emboîtés : un compte contient des **bases de données**, une base contient des **schémas**, un schéma contient les tables, les vues, les stages et les autres objets. Cette organisation sert à deux choses : ranger les données par domaine et par étape de traitement, et donner les droits à chaque étage ([chapitre 8](08-gestion-privileges.md)).

Ce chapitre crée la base `SALES_DB` et le schéma `RAW_DATA`, qui recevra les données brutes. Il introduit aussi la durée de rétention, qui règle le Time Travel.

```
Compte
└── SALES_DB                  (base de données)
    ├── INFORMATION_SCHEMA    (créé automatiquement : vues de métadonnées)
    ├── PUBLIC                (créé automatiquement : schéma par défaut)
    └── RAW_DATA              (notre schéma)
        └── tables, vues, stages...
```

---

## 1. Créer la base et le schéma dans Snowsight

Prenez le rôle `SYSADMIN`, qui possède le privilège `CREATE DATABASE`.

1. Dans le menu, sélectionnez **Catalog**, puis l'explorateur de bases (**Explorer**, affiché sous le titre **Database Explorer**).
2. Utilisez le bouton de création de base de données de cette page et nommez la base `SALES_DB`, avec le commentaire `Données de ventes`.
3. Ouvrez `SALES_DB`, puis sélectionnez **+ Schema**. La fenêtre **New Schema** s'ouvre.
4. **Name** : `RAW_DATA`. Commentaire : `Données brutes importées`. Laissez la case **Managed access** décochée.
5. Sélectionnez **Create**.

![Création du schéma](images/16-databases-navigation.png)
*Database Explorer : fenêtre New Schema ouverte depuis le bouton + Schema d'une base*

---

## 2. SQL équivalent

```sql
USE ROLE SYSADMIN;

CREATE DATABASE IF NOT EXISTS SALES_DB
    COMMENT = 'Données de ventes';

CREATE SCHEMA IF NOT EXISTS SALES_DB.RAW_DATA
    COMMENT = 'Données brutes importées';

SHOW SCHEMAS IN DATABASE SALES_DB;
```

`SHOW SCHEMAS` renvoie trois schémas : `RAW_DATA`, plus `PUBLIC` et `INFORMATION_SCHEMA`, créés automatiquement avec toute base.

Créer une base en fait la base courante de la session. Pour travailler ensuite sans répéter les noms complets :

```sql
USE SCHEMA SALES_DB.RAW_DATA;
```

---

## 3. Organiser les données par couches

Une base se découpe en schémas qui suivent le trajet des données :

| Schéma | Contenu | Créé au |
|---|---|---|
| `RAW_DATA` | données brutes, telles qu'elles arrivent des fichiers sources | chapitre 5 |
| `ANALYTICS` | tables nettoyées et agrégées, prêtes pour l'analyse | [chapitre 10](10-securite.md) |

Les données brutes ne sont jamais modifiées à la main : on les recharge, puis on reconstruit les tables d'analyse à partir d'elles.

Convention de nommage : noms en majuscules, mots séparés par un tiret bas. Snowflake met en majuscules tout nom écrit sans guillemets ; un nom écrit entre guillemets doubles (`"Sales_db"`) garde sa casse et devra toujours être écrit ainsi, ce qui est une source d'erreurs à éviter.

---

## 4. Durée de rétention et Time Travel

Le **Time Travel** permet de relire une table telle qu'elle était dans le passé et de restaurer un objet supprimé (`UNDROP`). La durée pendant laquelle c'est possible est le paramètre `DATA_RETENTION_TIME_IN_DAYS`.

| Édition | Tables permanentes | Tables transitoires et temporaires |
|---|---|---|
| Standard | 0 ou 1 jour | 0 ou 1 jour |
| Enterprise et supérieures | 0 à 90 jours | 0 ou 1 jour |

La valeur par défaut est de 1 jour. Le paramètre se règle au niveau du compte, de la base, du schéma ou de la table ; un objet hérite de la valeur du niveau supérieur s'il n'a pas la sienne.

```sql
-- Édition Enterprise : 7 jours de Time Travel sur toute la base
ALTER DATABASE SALES_DB SET DATA_RETENTION_TIME_IN_DAYS = 7;

SHOW DATABASES LIKE 'SALES_DB';      -- colonne retention_time
```

Une rétention plus longue augmente le stockage facturé, puisque Snowflake conserve les anciennes versions des données. Après la période de Time Travel, les tables permanentes passent en **Fail-safe** pendant 7 jours : seul le support de Snowflake peut alors récupérer les données. Le [chapitre 13](13-stockage-protection.md) détaille ces mécanismes.

---

## À retenir pour la certification

- Hiérarchie des objets : organisation, compte, base de données, schéma, objets de schéma (tables, vues, stages, formats de fichier...).
- Toute nouvelle base contient deux schémas créés automatiquement : `PUBLIC` et `INFORMATION_SCHEMA`.
- `DATA_RETENTION_TIME_IN_DAYS` vaut 1 par défaut ; maximum 1 jour en Standard, 90 jours en Enterprise pour les objets permanents, 1 jour pour les tables transitoires et temporaires.
- Le paramètre se définit au niveau du compte, de la base, du schéma ou de la table.
- Le Fail-safe dure 7 jours, ne concerne que les tables permanentes, et n'est accessible que par le support de Snowflake.
- Un nom sans guillemets est stocké en majuscules ; un nom entre guillemets doubles est sensible à la casse.

## ✅ Points de vérification
- [ ] Base `SALES_DB` créée avec le rôle `SYSADMIN`
- [ ] Schéma `RAW_DATA` créé
- [ ] `SHOW SCHEMAS IN DATABASE SALES_DB` renvoie trois schémas
- [ ] Rétention de la base réglée à 7 jours (édition Enterprise)

## Documentation officielle
- [Explorer les objets dans Snowsight](https://docs.snowflake.com/en/user-guide/ui-snowsight-data-databases)
- [CREATE DATABASE](https://docs.snowflake.com/en/sql-reference/sql/create-database)
- [CREATE SCHEMA](https://docs.snowflake.com/en/sql-reference/sql/create-schema)
- [Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel)

---

[← Retour au sommaire](README.md) | [← Précédent](04-creation-warehouse.md) | [Suivant →](06-creation-tables.md)
