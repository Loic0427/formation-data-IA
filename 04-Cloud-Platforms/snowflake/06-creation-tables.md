# 6. Création des tables

[← Retour au sommaire](README.md) | [← Précédent](05-creation-database-schema.md) | [Suivant →](07-import-donnees.md)

## Vue d'ensemble

Une table décrit la structure des données : le nom des colonnes, leur type et les règles qu'elles doivent respecter. Bien choisir les types évite les erreurs de chargement et les calculs faux.

Ce chapitre crée les quatre tables de l'exemple suivi (`CUSTOMERS`, `PRODUCTS`, `ORDERS`, `ORDER_ITEMS`) dans `SALES_DB.RAW_DATA`. Il contient surtout un point que beaucoup de personnes venant d'une autre base de données ignorent, et qui tombe régulièrement à l'examen : **sur une table standard, Snowflake n'applique pas les contraintes de clé primaire, d'unicité et de clé étrangère**. Elles sont enregistrées, mais rien n'empêche d'insérer un doublon ou une commande sans client.

```
CUSTOMERS (1) ──────< (n) ORDERS
                            │ (1)
                            ∨ (n)
PRODUCTS (1) ──────< (n) ORDER_ITEMS
```

---

## 1. Les types de données utiles

| Famille | Type | À savoir |
|---|---|---|
| Nombres | `NUMBER(p,s)` | `p` chiffres au total, dont `s` après la virgule. `NUMBER` seul vaut `NUMBER(38,0)` : aucune décimale |
| Nombres | `INTEGER`, `INT` | synonymes de `NUMBER(38,0)` |
| Nombres | `FLOAT` | nombre à virgule flottante, valeur approchée |
| Texte | `VARCHAR(n)` | `n` est une longueur maximale. Sans `n`, la longueur maximale par défaut est de 16 777 216 caractères. Déclarer une longueur plus courte ne change ni le stockage ni la performance |
| Texte | `STRING`, `TEXT` | synonymes de `VARCHAR` |
| Dates | `DATE`, `TIME` | date seule, heure seule |
| Dates | `TIMESTAMP_NTZ`, `TIMESTAMP_LTZ`, `TIMESTAMP_TZ` | date et heure : sans fuseau, dans le fuseau de la session, avec fuseau enregistré. `TIMESTAMP` désigne par défaut `TIMESTAMP_NTZ` |
| Logique | `BOOLEAN` | `TRUE`, `FALSE` ou `NULL` |
| Semi-structuré | `VARIANT`, `OBJECT`, `ARRAY` | JSON et formats voisins ([chapitre 18](18-transformation.md)) |

---

## 2. Les contraintes : ce que Snowflake applique vraiment

| Contrainte | Table standard | Table hybride |
|---|---|---|
| `NOT NULL` | appliquée | appliquée |
| `PRIMARY KEY` | **non appliquée** | obligatoire et appliquée |
| `UNIQUE` | **non appliquée** | appliquée |
| `FOREIGN KEY` | **non appliquée** | appliquée |

Sur une table standard, `NOT NULL` est la seule de ces quatre contraintes que Snowflake vérifie. Les trois autres sont **informatives** : elles documentent le modèle et sont lues par les outils de modélisation et de BI, mais Snowflake ne refuse aucune ligne à cause d'elles. Les tables hybrides, conçues pour les traitements transactionnels, sont le seul type de table où elles sont appliquées.

Conséquence pratique : dans un entrepôt Snowflake, l'unicité et l'intégrité référentielle se **contrôlent par des requêtes** après chaque chargement ([chapitre 7](07-import-donnees.md), section 5), ou par des tests dans un outil comme dbt.

La documentation actuelle mentionne aussi les contraintes `CHECK`, appliquées sur les tables standard. C'est un ajout récent : vérifiez sa disponibilité sur votre compte avant de vous en servir.

---

## 3. Créer les tables en SQL

Les tables se créent dans un fichier SQL d'un workspace ([chapitre 2](02-connexion.md)). C'est la méthode à privilégier : le script se relit, se versionne et se rejoue.

```sql
USE ROLE SYSADMIN;
USE WAREHOUSE SALES_WH;
USE SCHEMA SALES_DB.RAW_DATA;

CREATE TABLE IF NOT EXISTS CUSTOMERS (
    CUSTOMER_ID     NUMBER(10,0)  NOT NULL,
    FIRST_NAME      VARCHAR(50)   NOT NULL,
    LAST_NAME       VARCHAR(50)   NOT NULL,
    EMAIL           VARCHAR(100),
    PHONE           VARCHAR(20),
    ADDRESS         VARCHAR(200),
    CITY            VARCHAR(50),
    POSTAL_CODE     VARCHAR(10),
    COUNTRY         VARCHAR(50)   DEFAULT 'France',
    CONSTRAINT PK_CUSTOMERS PRIMARY KEY (CUSTOMER_ID),       -- informative
    CONSTRAINT UQ_CUSTOMERS_EMAIL UNIQUE (EMAIL)             -- informative
);

CREATE TABLE IF NOT EXISTS PRODUCTS (
    PRODUCT_ID      NUMBER(10,0)  NOT NULL,
    PRODUCT_NAME    VARCHAR(100)  NOT NULL,
    CATEGORY        VARCHAR(50),
    BRAND           VARCHAR(50),
    UNIT_PRICE      NUMBER(10,2)  NOT NULL,
    DESCRIPTION     VARCHAR(500),
    CONSTRAINT PK_PRODUCTS PRIMARY KEY (PRODUCT_ID)          -- informative
);

CREATE TABLE IF NOT EXISTS ORDERS (
    ORDER_ID            NUMBER(10,0)  NOT NULL,
    CUSTOMER_ID         NUMBER(10,0)  NOT NULL,
    ORDER_DATE          DATE          NOT NULL,
    ORDER_STATUS        VARCHAR(20)   DEFAULT 'PENDING',
    TOTAL_AMOUNT        NUMBER(12,2),
    SHIPPING_ADDRESS    VARCHAR(200),
    CONSTRAINT PK_ORDERS PRIMARY KEY (ORDER_ID),             -- informative
    CONSTRAINT FK_ORDERS_CUSTOMER                            -- informative
        FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMERS (CUSTOMER_ID)
);

CREATE TABLE IF NOT EXISTS ORDER_ITEMS (
    ORDER_ITEM_ID   NUMBER(10,0)  NOT NULL,
    ORDER_ID        NUMBER(10,0)  NOT NULL,
    PRODUCT_ID      NUMBER(10,0)  NOT NULL,
    QUANTITY        NUMBER(8,0)   NOT NULL,
    UNIT_PRICE      NUMBER(10,2)  NOT NULL,
    CONSTRAINT PK_ORDER_ITEMS PRIMARY KEY (ORDER_ITEM_ID),   -- informative
    CONSTRAINT FK_ORDER_ITEMS_ORDER                          -- informative
        FOREIGN KEY (ORDER_ID) REFERENCES ORDERS (ORDER_ID),
    CONSTRAINT FK_ORDER_ITEMS_PRODUCT                        -- informative
        FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCTS (PRODUCT_ID)
);
```

Points à remarquer :

- Une clé étrangère référence une table qui doit déjà exister : l'ordre de création est `CUSTOMERS`, `PRODUCTS`, `ORDERS`, `ORDER_ITEMS`.
- `DEFAULT` donne la valeur utilisée quand une instruction `INSERT` ne cite pas la colonne.
- Le montant d'une ligne de commande (`QUANTITY * UNIT_PRICE`) n'est pas stocké : on le calcule dans la requête qui en a besoin.
- Les tables sont créées par `SYSADMIN`, qui en devient propriétaire.

Vérifier :

```sql
SHOW TABLES IN SCHEMA SALES_DB.RAW_DATA;
DESC TABLE ORDERS;                                -- colonnes, types, NOT NULL, valeurs par défaut
SHOW PRIMARY KEYS IN SCHEMA SALES_DB.RAW_DATA;    -- les contraintes déclarées
SHOW IMPORTED KEYS IN TABLE ORDERS;               -- les clés étrangères de la table
```

### Et dans l'interface ?

Dans **Catalog** » **Explorer**, ouvrez `SALES_DB` puis `RAW_DATA`. Le bouton **Create** de la page du schéma propose les objets que l'on peut y créer : table, vue, stage, format de fichier, séquence, table dynamique, stream, tâche, pipe, fonction, procédure. Pour une table, l'interface propose notamment de la créer à partir d'un fichier ([chapitre 7](07-import-donnees.md)). Quel que soit le chemin suivi, c'est une instruction `CREATE TABLE` qui est exécutée : autant l'écrire soi-même.

---

## 4. Le constater par soi-même

Rien ne vaut un essai. Les instructions suivantes montrent ce qui est refusé et ce qui ne l'est pas.

```sql
-- 1. Deux clients avec la même clé primaire et le même e-mail : accepté
INSERT INTO CUSTOMERS (CUSTOMER_ID, FIRST_NAME, LAST_NAME, EMAIL)
VALUES (999, 'Test', 'Un',   'test@exemple.fr'),
       (999, 'Test', 'Deux', 'test@exemple.fr');

SELECT CUSTOMER_ID, COUNT(*) FROM CUSTOMERS GROUP BY CUSTOMER_ID HAVING COUNT(*) > 1;

-- 2. Une commande pour un client qui n'existe pas : acceptée
INSERT INTO ORDERS (ORDER_ID, CUSTOMER_ID, ORDER_DATE)
VALUES (9999, 123456, CURRENT_DATE());

-- 3. Une valeur NULL dans une colonne NOT NULL : refusée
INSERT INTO CUSTOMERS (CUSTOMER_ID, FIRST_NAME, LAST_NAME)
VALUES (998, NULL, 'Trois');
-- NULL result in a non-nullable column

-- Remettre les tables à vide avant le chapitre suivant
TRUNCATE TABLE ORDERS;
TRUNCATE TABLE CUSTOMERS;
```

La valeur par défaut a bien été appliquée : avant le `TRUNCATE`, la commande 9999 portait le statut `PENDING` et les clients le pays `France`.

---

## 5. Les types de tables

Les tables créées ci-dessus sont des tables **permanentes**, le type par défaut. Snowflake en propose d'autres, qui diffèrent par leur durée de vie et leur protection :

| Type | Création | Particularité |
|---|---|---|
| Permanente | `CREATE TABLE` | Time Travel et Fail-safe |
| Transitoire | `CREATE TRANSIENT TABLE` | pas de Fail-safe, Time Travel de 0 ou 1 jour |
| Temporaire | `CREATE TEMPORARY TABLE` | disparaît à la fin de la session |

Le [chapitre 13](13-stockage-protection.md) les compare en détail, avec les tables externes, dynamiques, hybrides et Iceberg.

---

## À retenir pour la certification

- Sur une table standard, `PRIMARY KEY`, `UNIQUE` et `FOREIGN KEY` sont acceptées mais **non appliquées** ; `NOT NULL` est appliquée.
- Les tables hybrides appliquent les contraintes de clé primaire (obligatoire), d'unicité et de clé étrangère.
- `NUMBER` sans précision vaut `NUMBER(38,0)` ; `INTEGER` en est un synonyme.
- `VARCHAR` sans longueur accepte jusqu'à 16 777 216 caractères ; déclarer une longueur plus courte n'apporte aucun gain de stockage ni de performance. `STRING` et `TEXT` sont des synonymes de `VARCHAR`.
- `TIMESTAMP` est par défaut un alias de `TIMESTAMP_NTZ` (paramètre `TIMESTAMP_TYPE_MAPPING`).
- Trois types de tables de base : permanente (par défaut), transitoire, temporaire.

## ✅ Points de vérification
- [ ] Les quatre tables existent dans `SALES_DB.RAW_DATA` et appartiennent à `SYSADMIN`
- [ ] Contraintes déclarées visibles avec `SHOW PRIMARY KEYS` et `SHOW IMPORTED KEYS`
- [ ] Doublon de clé primaire accepté, valeur `NULL` en colonne `NOT NULL` refusée : essai fait
- [ ] Tables vidées après l'essai

## Documentation officielle
- [Contraintes : vue d'ensemble](https://docs.snowflake.com/en/sql-reference/constraints-overview)
- [CREATE TABLE](https://docs.snowflake.com/en/sql-reference/sql/create-table)
- [Types de données](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)
- [Types de données texte](https://docs.snowflake.com/en/sql-reference/data-types-text)

---

[← Retour au sommaire](README.md) | [← Précédent](05-creation-database-schema.md) | [Suivant →](07-import-donnees.md)
