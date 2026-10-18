# 18. Requêtes et transformation : semi-structuré, fonctions, streams, tasks, tables dynamiques

[← Retour au sommaire](README.md) | [← Précédent](17-performance.md) | [Suivant →](19-collaboration.md)

## Vue d'ensemble

Une fois les données chargées, le travail du Data Engineer consiste à les transformer : extraire les champs d'un document JSON, dédoublonner, agréger, puis tenir ces résultats à jour quand de nouvelles données arrivent. Ce chapitre présente les outils que Snowflake fournit pour cela, sans outil extérieur :

- lire et aplatir des données **semi-structurées** (JSON, Parquet) avec le type `VARIANT` ;
- connaître l'essentiel sur les données **non structurées** (fichiers) et les tables de répertoire ;
- utiliser les **fonctions** qui reviennent partout : fenêtrage, `QUALIFY`, estimation ;
- écrire une **fonction** ou une **procédure stockée**, et savoir ce qui les distingue ;
- automatiser : **streams** (savoir ce qui a changé), **tasks** (planifier), **tables dynamiques** (déclarer le résultat voulu) ;
- comprendre les **transactions**.

Ce chapitre couvre la seconde moitié du domaine 4 de l'examen SnowPro Core COF-C03 (« Performance, requêtes et transformation », 21 %). La performance est au [chapitre 17](17-performance.md).

Exemple suivi : `SALES_DB`, `SALES_WH`, rôle `SALES_ENGINEER`, et la table `SALES_DB.RAW_DATA.ORDERS_RAW` chargée au [chapitre 11](11-chargement-stage-copy.md). Tout ce chapitre fonctionne en édition Standard.

Droits nécessaires, à donner une fois :

```sql
USE ROLE ACCOUNTADMIN;      -- ou SYSADMIN s'il est propriétaire des schémas, sauf pour les deux dernières lignes
GRANT CREATE STREAM, CREATE TASK, CREATE DYNAMIC TABLE, CREATE FUNCTION, CREATE PROCEDURE
  ON SCHEMA SALES_DB.RAW_DATA TO ROLE SALES_ENGINEER;
GRANT CREATE STREAM, CREATE TASK, CREATE DYNAMIC TABLE, CREATE FUNCTION, CREATE PROCEDURE
  ON SCHEMA SALES_DB.ANALYTICS TO ROLE SALES_ENGINEER;
GRANT EXECUTE TASK ON ACCOUNT TO ROLE SALES_ENGINEER;             -- faire tourner des tasks
GRANT EXECUTE MANAGED TASK ON ACCOUNT TO ROLE SALES_ENGINEER;     -- tasks serverless
```

---

## 1. Trois familles de données

| Famille | Définition | Exemples | Dans Snowflake |
|---|---|---|---|
| Structurées | colonnes et types fixés à l'avance | CSV, tables | colonnes typées (`NUMBER`, `VARCHAR`, `DATE`...) |
| Semi-structurées | la structure est décrite dans la donnée elle-même et peut varier d'une ligne à l'autre | JSON, Avro, ORC, Parquet, XML | types `VARIANT`, `OBJECT`, `ARRAY` |
| Non structurées | pas de modèle de données exploitable en colonnes | PDF, images, sons, vidéos | fichiers sur un stage, tables de répertoire, URL de fichier |

---

## 2. Données semi-structurées

### 2.1 Les trois types

Analogie : une colonne `VARIANT` est une boîte dans laquelle on peut ranger n'importe quoi, un nombre, un texte, une liste, un document entier, et dont on peut lire le contenu sans la déballer dans des colonnes.

| Type | Contient | Équivalent JSON | Exemple |
|---|---|---|---|
| `VARIANT` | une valeur de n'importe quel type, y compris un objet ou un tableau | n'importe quelle valeur | `{"device": "desktop", "tags": ["a", "b"]}` |
| `OBJECT` | des paires clé-valeur ; la clé est un texte, la valeur un `VARIANT` | objet `{ }` | `{"ip": "192.168.1.100"}` |
| `ARRAY` | une liste ordonnée de `VARIANT`, numérotée à partir de 0 | tableau `[ ]` | `["a", "b", "c"]` |

Une valeur `VARIANT` a une taille maximale. La documentation actuelle indique 128 Mo de données non compressées ; la limite était de 16 Mo auparavant, et ce chiffre figure encore dans beaucoup de supports de révision.

### 2.2 Créer et remplir une colonne VARIANT

`PARSE_JSON` transforme un texte en `VARIANT`. Le fichier `Data/saas/usage_events.csv` contient une colonne `properties` qui est du JSON écrit dans un CSV : c'est un cas très courant.

```sql
USE ROLE SALES_ENGINEER;
USE WAREHOUSE SALES_WH;
USE SCHEMA SALES_DB.RAW_DATA;

CREATE OR REPLACE TABLE USAGE_EVENTS (
  event_id    VARCHAR,
  event_type  VARCHAR,
  event_ts    TIMESTAMP_NTZ,
  properties  VARIANT
);

-- PARSE_JSON ne s'utilise pas dans une clause VALUES : on passe par INSERT ... SELECT
INSERT INTO USAGE_EVENTS
SELECT 'EVT-001', 'login',     '2024-02-13 14:22:00', PARSE_JSON('{"ip": "192.168.1.100", "device": "desktop"}')
UNION ALL
SELECT 'EVT-002', 'page_view', '2024-02-13 14:23:00', PARSE_JSON('{"page": "dashboard", "duration": 45}');
```

`TRY_PARSE_JSON` fait la même chose mais renvoie `NULL` au lieu d'une erreur quand le texte n'est pas du JSON valide : utile sur des données brutes.

### 2.3 Lire : la notation d'accès

```sql
SELECT
  properties:device              AS device_brut,     -- "desktop"  (VARIANT, avec guillemets)
  properties:device::VARCHAR     AS device,          -- desktop    (texte)
  properties:duration::NUMBER    AS duree,           -- 45
  properties['page']::VARCHAR    AS page,            -- notation entre crochets, équivalente
  properties:absent              AS champ_absent     -- NULL : une clé absente ne provoque pas d'erreur
FROM USAGE_EVENTS;
```

| Notation | Usage |
|---|---|
| `colonne:cle` | premier niveau : deux-points après le nom de la colonne |
| `colonne:cle.sous_cle` | niveaux suivants : point |
| `colonne['cle']['sous_cle']` | crochets, à tous les niveaux ; obligatoire si la clé contient un espace ou un caractère spécial |
| `colonne:liste[0]` | élément d'un tableau, numéroté à partir de 0 |
| `expression::TYPE` | conversion de type (*cast*) |

Trois règles :

- le nom de la colonne est insensible à la casse, mais **les clés JSON sont sensibles à la casse** : `properties:Device` renvoie `NULL` si la clé s'appelle `device` ;
- sans conversion, le résultat est un `VARIANT` : un texte s'affiche entre guillemets, et les comparaisons ou jointures peuvent surprendre. On convertit toujours avec `::` ;
- un `null` JSON n'est pas un `NULL` SQL. `properties:champ IS NULL` est faux pour `{"champ": null}` ; la fonction `IS_NULL_VALUE` détecte ce cas, et la conversion `::VARCHAR` le ramène à un `NULL` SQL.

### 2.4 Aplatir : FLATTEN et LATERAL

Un document contient souvent une liste : les lignes d'une commande, les étiquettes d'un produit. `FLATTEN` est une fonction de table qui produit **une ligne par élément** de la liste. `LATERAL` permet à cette fonction de lire une colonne de la table placée avant elle dans le `FROM`.

```sql
CREATE OR REPLACE TABLE ORDERS_JSON (doc VARIANT);

INSERT INTO ORDERS_JSON
SELECT PARSE_JSON('{
  "order_id": 1001,
  "customer": {"id": 1, "country": "USA"},
  "items": [ {"product_id": 1, "qty": 1, "price": 999.99},
             {"product_id": 7, "qty": 2, "price": 49.50} ]
}');

SELECT
  doc:order_id::NUMBER            AS order_id,
  doc:customer.country::VARCHAR   AS country,
  i.index                         AS position,
  i.value:product_id::NUMBER      AS product_id,
  i.value:qty::NUMBER             AS qty,
  i.value:price::FLOAT            AS price
FROM ORDERS_JSON,
     LATERAL FLATTEN(INPUT => doc:items) i;
```

Résultat attendu : deux lignes pour la commande 1001, une par article.

```
ORDER_ID | COUNTRY | POSITION | PRODUCT_ID | QTY | PRICE
1001     | USA     | 0        | 1          | 1   | 999.99
1001     | USA     | 1        | 7          | 2   | 49.5
```

Colonnes renvoyées par `FLATTEN` :

| Colonne | Contenu |
|---|---|
| `SEQ` | numéro de la ligne d'entrée |
| `KEY` | la clé, si l'on aplatit un objet |
| `PATH` | le chemin de l'élément dans le document |
| `INDEX` | la position, si l'on aplatit un tableau |
| `VALUE` | l'élément lui-même (c'est la colonne qu'on utilise le plus) |
| `THIS` | l'élément en cours d'aplatissement |

Options : `PATH` (aplatir un sous-élément), `OUTER => TRUE` (garder la ligne d'entrée même si la liste est vide ou absente, comme une jointure externe), `RECURSIVE => TRUE` (descendre dans tous les niveaux), `MODE` (`OBJECT`, `ARRAY` ou `BOTH`).

### 2.5 Construire du semi-structuré

```sql
SELECT OBJECT_CONSTRUCT('order_id', order_id, 'country', ship_country) AS doc   -- un objet par ligne
FROM ORDERS_RAW LIMIT 3;

SELECT customer_id, ARRAY_AGG(order_id) AS commandes                           -- une liste par client
FROM ORDERS_RAW GROUP BY customer_id;
```

Autres fonctions utiles : `TYPEOF` (type réel d'une valeur `VARIANT`), `ARRAY_SIZE`, `ARRAY_CONTAINS`, `OBJECT_KEYS`, `GET` et `GET_PATH` (accès par fonction), `TO_JSON` (retour au texte).

### 2.6 Charger des fichiers JSON et Parquet

Deux façons de charger, avec les objets du chapitre 11 (format de fichier, stage, `COPY INTO`) :

```sql
-- 1. Tout le document dans une colonne VARIANT (schéma à la lecture)
CREATE OR REPLACE FILE FORMAT JSON_FF TYPE = JSON STRIP_OUTER_ARRAY = TRUE;
CREATE OR REPLACE TABLE EVENTS_JSON_RAW (doc VARIANT);
COPY INTO EVENTS_JSON_RAW FROM @VENTES_STAGE FILES = ('events.json')
  FILE_FORMAT = (FORMAT_NAME = JSON_FF);

-- 2. Colonnes typées dès le chargement, par une requête sur le fichier
COPY INTO USAGE_EVENTS (event_id, event_type, properties)
FROM (SELECT $1:event_id::VARCHAR, $1:event_type::VARCHAR, $1:properties FROM @VENTES_STAGE/events.json)
FILE_FORMAT = (FORMAT_NAME = JSON_FF);
```

- `STRIP_OUTER_ARRAY = TRUE` : si le fichier est un grand tableau `[ {...}, {...} ]`, chaque élément devient une ligne. Sans cette option, tout le fichier est une seule valeur, qui peut dépasser la taille maximale.
- `$1` désigne le document lu dans le fichier ; pour JSON comme pour Parquet, un fichier se lit comme une seule colonne `$1`.
- Parquet contient les noms et les types de ses colonnes : `MATCH_BY_COLUMN_NAME` (chapitre 11) le charge directement en colonnes, et la fonction `INFER_SCHEMA` lit la structure du fichier pour créer la table (`CREATE TABLE ... USING TEMPLATE`).

### 2.7 Performance du semi-structuré

À l'intérieur d'une colonne `VARIANT`, Snowflake range quand il le peut les champs les plus fréquents en colonnes cachées, ce qui permet de ne lire que les champs demandés. Cette extraction n'a pas lieu pour un champ qui contient des `null` JSON ou dont le type varie d'une ligne à l'autre. Les dates et horodatages placés dans un `VARIANT` sont stockés comme du texte. Pratique courante : garder le document brut en `VARIANT` dans la couche brute, puis extraire en colonnes typées les champs sur lesquels on filtre ou on joint.

---

## 3. Données non structurées et tables de répertoire, en bref

Les fichiers (PDF, images...) restent sur un stage, interne ou externe. Snowflake fournit de quoi les lister, y donner accès et les traiter.

Une **table de répertoire** (*directory table*) est un catalogue des fichiers d'un stage. Ce n'est pas un objet séparé : elle est attachée au stage et s'active avec une option.

```sql
CREATE STAGE IF NOT EXISTS DOCS_STAGE
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

ALTER STAGE DOCS_STAGE REFRESH;                    -- met le catalogue à jour après un dépôt de fichiers
SELECT relative_path, size, last_modified, file_url FROM DIRECTORY(@DOCS_STAGE);
```

On peut poser un stream sur une table de répertoire pour détecter l'arrivée de nouveaux fichiers. Trois types d'URL donnent accès à un fichier :

| URL | Fonction | Caractéristique |
|---|---|---|
| URL à portée limitée (*scoped URL*) | `BUILD_SCOPED_FILE_URL` | temporaire, réservée à l'utilisateur qui l'a générée ; sert à donner accès à un fichier sans donner de droit sur le stage |
| URL de fichier (*file URL*) | `BUILD_STAGE_FILE_URL` | permanente ; demande un rôle qui a les droits sur le stage |
| URL pré-signée (*pre-signed URL*) | `GET_PRESIGNED_URL` | utilisable sans s'authentifier auprès de Snowflake, jusqu'à une date d'expiration choisie |

Le traitement du contenu des fichiers se fait avec des fonctions Python, Java ou Scala et Snowpark (chapitre 14).

---

## 4. Fonctions utiles

### 4.1 Agrégats et fenêtrage

Un agrégat (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `LISTAGG`, `ARRAY_AGG`...) réduit plusieurs lignes en une. Une **fonction de fenêtrage** calcule sur un groupe de lignes sans les réduire : chaque ligne garde sa place et reçoit un résultat.

```sql
SELECT
  order_id, customer_id, order_date, total_amount,
  ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date)  AS rang_commande,
  SUM(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date
                          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumul_client,
  LAG(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date)     AS montant_precedent
FROM ORDERS_RAW;
```

| Élément | Rôle |
|---|---|
| `PARTITION BY` | découpe les lignes en groupes (ici un groupe par client) |
| `ORDER BY` (dans `OVER`) | ordonne les lignes à l'intérieur du groupe |
| `ROWS BETWEEN ...` | le cadre : quelles lignes du groupe entrent dans le calcul |

| Fonction | Résultat sur des ex æquo (100, 100, 90) |
|---|---|
| `ROW_NUMBER()` | 1, 2, 3 : numéros tous différents |
| `RANK()` | 1, 1, 3 : même rang, puis un saut |
| `DENSE_RANK()` | 1, 1, 2 : même rang, sans saut |
| `LAG` / `LEAD` | valeur de la ligne précédente / suivante |

### 4.2 QUALIFY

`QUALIFY` filtre sur le résultat d'une fonction de fenêtrage, comme `HAVING` filtre sur un agrégat. Sans lui, il faut une sous-requête. Cas le plus courant : dédoublonner en gardant la ligne la plus récente.

```sql
-- La dernière commande de chaque client
SELECT *
FROM ORDERS_RAW
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) = 1;
```

Ordre d'évaluation d'une requête : `FROM` → `WHERE` → `GROUP BY` → `HAVING` → fonctions de fenêtrage → `QUALIFY` → `DISTINCT` → `ORDER BY` → `LIMIT`. C'est pourquoi une fonction de fenêtrage ne peut pas figurer dans `WHERE`.

### 4.3 Fonctions d'estimation

Sur de très grands volumes, un compte exact de valeurs distinctes demande beaucoup de mémoire. Les fonctions d'estimation donnent un résultat approché, beaucoup plus vite.

| Besoin | Fonction exacte | Fonction d'estimation | Algorithme |
|---|---|---|---|
| nombre de valeurs distinctes | `COUNT(DISTINCT col)` | `APPROX_COUNT_DISTINCT(col)` (synonyme `HLL`) | HyperLogLog |
| percentile, médiane | `PERCENTILE_CONT`, `MEDIAN` | `APPROX_PERCENTILE(col, 0.5)` | t-Digest |
| valeurs les plus fréquentes | `GROUP BY` + `ORDER BY COUNT(*)` | `APPROX_TOP_K(col, 10)` | Space-Saving |
| similarité de deux ensembles | intersection / union | `MINHASH` + `APPROXIMATE_SIMILARITY` | MinHash |

```sql
SELECT COUNT(DISTINCT o_custkey), APPROX_COUNT_DISTINCT(o_custkey)
FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF10.ORDERS;      -- deux valeurs proches, la seconde calculée plus vite
```

L'erreur moyenne de `APPROX_COUNT_DISTINCT` est de l'ordre de 1,6 %.

---

## 5. Fonctions définies par l'utilisateur et procédures stockées

### 5.1 Fonction définie par l'utilisateur (UDF)

Une UDF est un calcul réutilisable qu'on appelle **dans une requête**, comme une fonction native.

```sql
CREATE OR REPLACE FUNCTION SALES_DB.ANALYTICS.MONTANT_TTC(ht FLOAT, taux FLOAT)
RETURNS FLOAT
AS
$$
  ht * (1 + taux)
$$;

SELECT order_id, SALES_DB.ANALYTICS.MONTANT_TTC(total_amount, 0.20) AS ttc FROM ORDERS_RAW;
```

| Variante | Renvoie | Appel |
|---|---|---|
| UDF scalaire | une valeur par ligne d'entrée | `SELECT f(col)` |
| UDTF (fonction de table) | plusieurs lignes et colonnes | `FROM TABLE(f(...))` |
| UDAF (fonction d'agrégat) | une valeur pour un groupe de lignes | comme `SUM` |
| Fonction externe | le résultat d'un service appelé hors de Snowflake | `SELECT f(col)` |

Langages : SQL, JavaScript, Python, Java, Scala. Une UDF `SECURE` cache sa définition aux rôles qui ne la possèdent pas.

### 5.2 Procédure stockée

Une procédure stockée enchaîne des instructions avec de la logique (variables, conditions, boucles) et peut **modifier la base**. On l'appelle seule, avec `CALL`.

```sql
CREATE OR REPLACE PROCEDURE SALES_DB.ANALYTICS.PURGER_COMMANDES(avant DATE)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS OWNER
AS
$$
BEGIN
  DELETE FROM SALES_DB.RAW_DATA.ORDERS_RAW WHERE order_date < :avant;
  RETURN 'Lignes supprimées : ' || SQLROWCOUNT;
END;
$$;

CALL SALES_DB.ANALYTICS.PURGER_COMMANDES('2020-01-01');
```

Langages : Snowflake Scripting (SQL procédural, ci-dessus), JavaScript, Python, Java, Scala.

| `EXECUTE AS` | La procédure s'exécute avec les droits | Usage |
|---|---|---|
| `OWNER` (défaut) | du rôle propriétaire de la procédure | déléguer une action précise à un rôle qui n'a pas les droits sur les tables |
| `CALLER` | du rôle qui appelle, avec le contexte de sa session | outil générique qui agit sur les objets de l'appelant |

### 5.3 Fonction ou procédure

| | Fonction (UDF) | Procédure stockée |
|---|---|---|
| But | calculer et renvoyer une valeur | exécuter des actions |
| Appel | dans une expression : `SELECT f(x)` | instruction autonome : `CALL p(x)` |
| Valeur de retour | obligatoire | facultative |
| DDL et DML (`CREATE`, `INSERT`, `DELETE`...) | non | oui |
| Plusieurs appels dans une même instruction | oui | non : une seule procédure par `CALL` |
| Droits d'exécution | sans objet | propriétaire (défaut) ou appelant |
| Langages | SQL, JavaScript, Python, Java, Scala | Snowflake Scripting, JavaScript, Python, Java, Scala |

### 5.4 Snowpark

Snowpark permet d'écrire ces transformations, fonctions et procédures en Python, Java ou Scala avec une API de DataFrame, le calcul restant exécuté dans Snowflake. Il est présenté au [chapitre 14, section 4](14-ia-applications.md).

---

## 6. Streams : savoir ce qui a changé

### 6.1 Principe

Analogie : un marque-page dans le journal des modifications d'une table. Un **stream** ne contient aucune donnée : il mémorise une position, le **décalage** (*offset*), et montre les modifications survenues depuis cette position. C'est la capture des changements (*change data capture*).

```
ORDERS_RAW :   v1 ──── v2 ──── v3 ──── v4 (version actuelle)
                       ▲
                       décalage du stream
SELECT * FROM le stream  →  les changements entre v2 et v4
```

```sql
CREATE OR REPLACE STREAM ORDERS_STREAM ON TABLE ORDERS_RAW;

INSERT INTO ORDERS_RAW (order_id, customer_id, order_date, order_status, total_amount)
  VALUES (9001, 1, '2024-06-01', 'PENDING', 120.00);
UPDATE ORDERS_RAW SET order_status = 'DELIVERED' WHERE order_id = 1001;

SELECT order_id, order_status, METADATA$ACTION, METADATA$ISUPDATE FROM ORDERS_STREAM;
```

Résultat attendu :

```
ORDER_ID | ORDER_STATUS | METADATA$ACTION | METADATA$ISUPDATE
9001     | PENDING      | INSERT          | FALSE
1001     | DELIVERED    | INSERT          | TRUE      ← nouvelle version de la ligne
1001     | SHIPPED      | DELETE          | TRUE      ← ancienne version de la ligne
```

### 6.2 Colonnes de métadonnées

| Colonne | Contenu |
|---|---|
| `METADATA$ACTION` | `INSERT` ou `DELETE` |
| `METADATA$ISUPDATE` | `TRUE` si la ligne fait partie d'une mise à jour : un `UPDATE` apparaît comme une paire `DELETE` + `INSERT` |
| `METADATA$ROW_ID` | identifiant unique et stable de la ligne |

Un stream standard montre le **bilan net** des changements : une ligne insérée puis supprimée entre deux lectures n'apparaît pas.

### 6.3 Types de streams

| Type | Capture | Sur |
|---|---|---|
| Standard (défaut) | insertions, mises à jour, suppressions | tables, vues, tables de répertoire, tables dynamiques |
| Append-only (`APPEND_ONLY = TRUE`) | insertions seulement ; plus léger | tables, vues, tables dynamiques |
| Insert-only (`INSERT_ONLY = TRUE`) | insertions seulement | tables externes (et tables Iceberg gérées par un catalogue externe) |

### 6.4 Le décalage avance quand on consomme

- Un `SELECT` sur le stream ne fait **pas** avancer le décalage : on peut le lire autant de fois qu'on veut.
- Le décalage avance quand le stream est utilisé dans une instruction **DML** validée (`INSERT INTO ... SELECT ... FROM stream`, `MERGE`, `CREATE TABLE AS SELECT`). Le stream paraît alors vide jusqu'au prochain changement.
- Dans une transaction, toutes les instructions voient le même contenu du stream, et le décalage n'avance qu'au `COMMIT`.
- Un stream ne sert qu'un consommateur : pour deux traitements indépendants, on crée deux streams sur la même table (un stream ne coûte presque rien en stockage).

```sql
INSERT INTO SALES_DB.ANALYTICS.ORDERS_CHANGES
SELECT order_id, order_status, total_amount, METADATA$ACTION, CURRENT_TIMESTAMP()
FROM ORDERS_STREAM;                            -- consomme le stream (table ORDERS_CHANGES : voir l'atelier, étape 4)

SELECT SYSTEM$STREAM_HAS_DATA('ORDERS_STREAM');   -- FALSE juste après
```

### 6.5 Péremption

Un stream s'appuie sur l'historique de la table (Time Travel, chapitre 13). S'il n'est pas consommé assez longtemps, son décalage sort de la période de rétention : le stream est **périmé** (*stale*), illisible, et il faut le recréer. Pour limiter ce risque, quand la rétention de la table est inférieure à 14 jours, Snowflake la prolonge temporairement pour le stream, jusqu'à 14 jours par défaut (paramètre `MAX_DATA_EXTENSION_TIME_IN_DAYS`). `SHOW STREAMS` affiche les colonnes `stale` et `stale_after`. Remède : consommer le stream régulièrement.

La clause `CHANGES` d'un `SELECT` lit les changements d'une table entre deux instants sans créer de stream et sans décalage.

---

## 7. Tasks : planifier

### 7.1 Principe

Une **task** exécute une instruction SQL, un appel de procédure ou un bloc Snowflake Scripting, selon une planification ou à la suite d'une autre task.

```sql
CREATE OR REPLACE TASK SALES_DB.RAW_DATA.TRAITER_COMMANDES
  WAREHOUSE = SALES_WH
  SCHEDULE = '5 MINUTES'
  WHEN SYSTEM$STREAM_HAS_DATA('SALES_DB.RAW_DATA.ORDERS_STREAM')
AS
  INSERT INTO SALES_DB.ANALYTICS.ORDERS_CHANGES
  SELECT order_id, order_status, total_amount, METADATA$ACTION, CURRENT_TIMESTAMP()
  FROM SALES_DB.RAW_DATA.ORDERS_STREAM;

ALTER TASK SALES_DB.RAW_DATA.TRAITER_COMMANDES RESUME;    -- une task est créée suspendue
EXECUTE TASK SALES_DB.RAW_DATA.TRAITER_COMMANDES;         -- lancement manuel immédiat
ALTER TASK SALES_DB.RAW_DATA.TRAITER_COMMANDES SUSPEND;
```

| Élément | Rôle |
|---|---|
| `SCHEDULE = '5 MINUTES'` | intervalle fixe |
| `SCHEDULE = 'USING CRON 0 6 * * MON-FRI Europe/Paris'` | expression cron avec fuseau horaire : du lundi au vendredi à 6 heures |
| `WHEN SYSTEM$STREAM_HAS_DATA(...)` | condition : si elle est fausse, l'exécution est sautée et aucun warehouse ne démarre |
| sans `SCHEDULE`, avec `WHEN SYSTEM$STREAM_HAS_DATA(...)` | task déclenchée : elle s'exécute quand le stream reçoit des données |
| `ALTER TASK ... RESUME` | indispensable : une task créée est toujours suspendue |

Une task planifiée n'a qu'une exécution à la fois : si une exécution dure plus longtemps que l'intervalle, la suivante est sautée.

### 7.2 Serverless ou warehouse

| | Task avec warehouse | Task serverless |
|---|---|---|
| Déclaration | `WAREHOUSE = SALES_WH` | pas de paramètre `WAREHOUSE` ; taille de départ facultative avec `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE` |
| Calcul | votre warehouse, à sa taille | ressources gérées par Snowflake, ajustées d'après les exécutions précédentes |
| Facturation | crédits du warehouse (minimum 60 secondes à chaque reprise) | à l'usage réel |
| Privilège | `EXECUTE TASK` sur le compte, `USAGE` sur le warehouse | `EXECUTE TASK` et `EXECUTE MANAGED TASK` sur le compte |
| À préférer pour | traitements longs ou nombreux qui remplissent un warehouse | traitements courts, fréquents, ou peu prévisibles |

### 7.3 Graphes de tasks

Un **graphe de tasks** (*task graph*, ou DAG) enchaîne plusieurs tasks : une **task racine** porte la planification, les **tasks enfants** s'exécutent après leurs parents.

```
T_RACINE (SCHEDULE)
   ├──> T_NETTOYER ──┐
   └──> T_ENRICHIR ──┴──> T_AGREGER        puis T_FINALE (FINALIZE) dans tous les cas
```

```sql
CREATE OR REPLACE TASK T_AGREGER
  WAREHOUSE = SALES_WH
  AFTER T_NETTOYER, T_ENRICHIR         -- pas de SCHEDULE sur une task enfant
AS CALL SALES_DB.ANALYTICS.CALCULER_AGREGATS();

SELECT SYSTEM$TASK_DEPENDENTS_ENABLE('SALES_DB.RAW_DATA.T_RACINE');   -- reprend la racine et toutes ses enfants
```

- Seule la racine a un `SCHEDULE` ; les enfants ont `AFTER`.
- Une task finale (`FINALIZE = T_RACINE`) s'exécute à la fin du graphe, qu'il ait réussi ou échoué : utile pour notifier ou nettoyer.
- Limites : 1 000 tasks par graphe, 100 parents et 100 enfants par task.
- Pour modifier une task du graphe, on suspend d'abord la racine.
- Suivi : fonction de table `INFORMATION_SCHEMA.TASK_HISTORY()`, vue `ACCOUNT_USAGE.TASK_HISTORY`, et la page des tasks dans Snowsight.

---

## 8. Tables dynamiques : déclarer le résultat

### 8.1 Principe

Avec un stream et une task, on écrit **comment** tenir une table à jour. Avec une **table dynamique**, on écrit seulement **quel résultat** on veut, sous forme de requête, et le retard qu'on accepte. Snowflake s'occupe du rafraîchissement, de l'ordre entre tables dépendantes et, quand la requête le permet, du traitement des seules lignes modifiées.

```sql
CREATE OR REPLACE DYNAMIC TABLE SALES_DB.ANALYTICS.CA_PAR_PAYS
  TARGET_LAG = '10 minutes'
  WAREHOUSE = SALES_WH
AS
SELECT ship_country, COUNT(*) AS nb_commandes, SUM(total_amount) AS chiffre_affaires
FROM SALES_DB.RAW_DATA.ORDERS_RAW
GROUP BY ship_country;

ALTER DYNAMIC TABLE SALES_DB.ANALYTICS.CA_PAR_PAYS REFRESH;    -- rafraîchissement immédiat
ALTER DYNAMIC TABLE SALES_DB.ANALYTICS.CA_PAR_PAYS SUSPEND;    -- arrête les rafraîchissements
```

| Paramètre | Rôle |
|---|---|
| `TARGET_LAG = '10 minutes'` | retard cible : les données ne doivent pas avoir plus de 10 minutes de retard sur les tables sources. Minimum : 1 minute |
| `TARGET_LAG = DOWNSTREAM` | la table ne se rafraîchit que lorsque les tables dynamiques qui la lisent en ont besoin |
| `WAREHOUSE` | obligatoire : c'est lui qui exécute les rafraîchissements |
| `REFRESH_MODE` | `AUTO` (défaut : Snowflake choisit), `INCREMENTAL` (seulement les changements), `FULL` (tout recalculer) |

Le retard cible est un objectif, pas une garantie : si le rafraîchissement dure plus longtemps, le retard réel le dépasse. Une table dynamique ne reçoit pas d'`INSERT`, `UPDATE` ou `DELETE` : son contenu vient uniquement de sa requête.

### 8.2 Comparaison

| | Stream + task | Table dynamique | Vue matérialisée |
|---|---|---|---|
| Approche | procédurale : on écrit les étapes | déclarative : on écrit le résultat | déclarative |
| Requête | libre : `MERGE`, procédures, appels externes | un `SELECT`, jointures et agrégats compris | un `SELECT` sur une seule table, sans jointure |
| Fraîcheur | selon la planification de la task | retard cible, 1 minute au minimum | toujours à jour |
| Planification | à écrire (`SCHEDULE`, graphe) | automatique, dépendances comprises | automatique |
| Calcul | warehouse ou serverless | warehouse désigné | serverless |
| Réécriture automatique des requêtes par l'optimiseur | non | non | oui |
| Édition | Standard | Standard | Enterprise |
| À choisir pour | logique complexe, ordonnancement strict, appels de procédures | chaînes de transformation en SQL (brut, nettoyé, agrégé) | accélérer un agrégat sur une table |

---

## 9. Transactions

Une transaction regroupe plusieurs instructions qui réussissent ou échouent ensemble.

```sql
BEGIN;
  UPDATE ORDERS_RAW SET order_status = 'CANCELLED' WHERE order_id = 9001;
  INSERT INTO SALES_DB.ANALYTICS.ORDERS_CHANGES
    SELECT 9001, 'CANCELLED', 120.00, 'MANUEL', CURRENT_TIMESTAMP();
COMMIT;        -- ou ROLLBACK pour tout annuler
```

| Règle | Détail |
|---|---|
| `AUTOCOMMIT` | activé par défaut : hors transaction explicite, chaque instruction est validée seule |
| Niveau d'isolation | `READ COMMITTED`, le seul proposé pour les tables standard : une instruction ne voit que les données validées avant son début |
| DDL | un `CREATE`, `ALTER` ou `DROP` valide la transaction en cours, puis s'exécute dans sa propre transaction : on ne peut pas l'annuler par `ROLLBACK` |
| Verrous | `UPDATE`, `DELETE` et `MERGE` verrouillent la table contre les autres modifications de ce type ; `INSERT` et `COPY` écrivent de nouvelles micro-partitions et peuvent en général s'exécuter en parallèle |
| Attente d'un verrou | paramètre `LOCK_TIMEOUT`, 43 200 secondes (12 heures) par défaut |
| Transaction abandonnée | annulée automatiquement après 4 heures d'inactivité, ou 5 minutes si elle bloque d'autres transactions |
| Procédures | une transaction ne peut pas commencer dans une procédure et finir en dehors, ni l'inverse |
| Outils | `SHOW TRANSACTIONS`, `SHOW LOCKS`, `SYSTEM$ABORT_TRANSACTION(<id>)` |

Lien avec les streams : un stream lu dans une transaction n'avance qu'au `COMMIT`. En cas de `ROLLBACK`, les changements restent à consommer : rien n'est perdu.

---

## 10. Pièges fréquents

1. **Oublier la conversion `::`** : `properties:device` renvoie `"desktop"` avec ses guillemets, et une comparaison avec une colonne texte peut échouer.
2. **Se tromper de casse sur une clé JSON** : `doc:Order_ID` renvoie `NULL` sans erreur si la clé est `order_id`.
3. **`PARSE_JSON` dans `VALUES`** : erreur. Utiliser `INSERT ... SELECT PARSE_JSON(...)`.
4. **Charger un fichier JSON en tableau sans `STRIP_OUTER_ARRAY`** : une seule ligne énorme, ou un dépassement de la taille maximale.
5. **`FLATTEN` sans `OUTER => TRUE`** : les lignes dont la liste est vide disparaissent du résultat.
6. **Fonction de fenêtrage dans `WHERE`** : interdit. C'est le rôle de `QUALIFY`.
7. **Croire qu'un `SELECT` vide un stream** : seul un DML validé fait avancer le décalage.
8. **Deux traitements sur le même stream** : le premier qui consomme prive l'autre des changements. Un stream par consommateur.
9. **Créer une task et attendre** : elle est suspendue. Il faut `ALTER TASK ... RESUME`, et dans un graphe, reprendre aussi les enfants.
10. **Mettre un `SCHEDULE` sur une task enfant** : seule la racine en porte un.
11. **Laisser tourner une task toutes les minutes sur un warehouse** : chaque reprise est facturée 60 secondes au minimum. Ajouter une condition `WHEN`, ou passer en serverless.
12. **Mettre un DDL au milieu d'une transaction** : il valide tout ce qui précède.
13. **Vouloir un `INSERT` dans une table dynamique**, ou une jointure dans une vue matérialisée.

---

## 11. À retenir pour la certification

- Types semi-structurés : `VARIANT` (toute valeur), `OBJECT` (clés-valeurs), `ARRAY` (liste, à partir de 0). Formats : JSON, Avro, ORC, Parquet, XML.
- Accès : `col:cle.sous_cle`, `col['cle']`, `col:liste[0]`, conversion `::TYPE`. Les clés sont sensibles à la casse.
- `FLATTEN` est une fonction de table ; colonnes `SEQ`, `KEY`, `PATH`, `INDEX`, `VALUE`, `THIS` ; options `OUTER`, `RECURSIVE`, `PATH`, `MODE`. Elle s'emploie avec `LATERAL`.
- `PARSE_JSON` : texte vers `VARIANT`. `STRIP_OUTER_ARRAY` : un tableau JSON devient plusieurs lignes.
- Table de répertoire : catalogue des fichiers d'un stage, activé par `DIRECTORY = (ENABLE = TRUE)`, lu par `DIRECTORY(@stage)`. Trois URL : à portée limitée, de fichier, pré-signée.
- `QUALIFY` filtre le résultat d'une fonction de fenêtrage. `APPROX_COUNT_DISTINCT` utilise HyperLogLog.
- UDF : appelée dans une requête, renvoie toujours une valeur, pas de DDL ni de DML ; langages SQL, JavaScript, Python, Java, Scala. Procédure : `CALL`, peut faire du DDL et du DML, droits du propriétaire par défaut ; Snowflake Scripting, JavaScript, Python, Java, Scala.
- Stream : ne stocke pas de données, seulement un décalage ; colonnes `METADATA$ACTION`, `METADATA$ISUPDATE`, `METADATA$ROW_ID` ; un `UPDATE` = `DELETE` + `INSERT` avec `METADATA$ISUPDATE = TRUE` ; types standard, append-only, insert-only (tables externes) ; avance sur un DML validé, pas sur un `SELECT` ; devient périmé si non consommé pendant la période de rétention (prolongée jusqu'à 14 jours par défaut).
- Task : créée suspendue ; `SCHEDULE` en intervalle ou `USING CRON` ; `WHEN SYSTEM$STREAM_HAS_DATA` ; serverless si `WAREHOUSE` est omis ; privilège `EXECUTE TASK` ; graphe : une racine planifiée, enfants avec `AFTER`, 1 000 tasks au maximum, task finale avec `FINALIZE`.
- Table dynamique : `TARGET_LAG` (1 minute au minimum, ou `DOWNSTREAM`) et `WAREHOUSE` ; accepte les jointures, contrairement à la vue matérialisée ; déclarative, contrairement à stream + task.
- Transactions : `READ COMMITTED` ; `AUTOCOMMIT` activé par défaut ; un DDL valide la transaction en cours.

---

## 12. Atelier pratique (30 à 45 minutes)

Objectif : partir d'un fichier contenant du JSON, l'aplatir, puis automatiser une transformation de trois façons. Tout l'atelier fonctionne sur un compte d'essai en édition Standard ; aucune étape ne demande l'édition Enterprise (la vue matérialisée citée en question de réflexion, elle, la demande).

Prérequis : les droits du début de chapitre, et la table `ORDERS_RAW` du chapitre 11.

### Étape 1 : JSON dans un CSV (10 minutes)

1. Charger `Data/saas/usage_events.csv` dans une table `SALES_DB.RAW_DATA.USAGE_EVENTS_RAW` avec la méthode du chapitre 11 (ou l'assistant de chargement du chapitre 7), la colonne `properties` étant déclarée en `VARCHAR`.
2. Créer une table typée :

```sql
CREATE OR REPLACE TABLE SALES_DB.RAW_DATA.USAGE_EVENTS AS
SELECT event_id, user_id, event_type, event_timestamp::TIMESTAMP_NTZ AS event_ts,
       TRY_PARSE_JSON(properties) AS properties
FROM SALES_DB.RAW_DATA.USAGE_EVENTS_RAW;
```

3. Compter les lignes dont `properties` est `NULL` : y a-t-il du JSON invalide dans le fichier ?
4. Lister toutes les clés présentes dans `properties` et leur fréquence :

```sql
SELECT f.key, TYPEOF(f.value) AS type_valeur, COUNT(*) AS nb
FROM SALES_DB.RAW_DATA.USAGE_EVENTS, LATERAL FLATTEN(INPUT => properties) f
GROUP BY 1, 2 ORDER BY nb DESC;
```

5. Écrire la requête qui donne, par `device`, le nombre d'événements `login`. Refaire le test avec `properties:Device` : que se passe-t-il ?

### Étape 2 : aplatir une liste (5 minutes)

1. Créer la table `ORDERS_JSON` de la section 2.4 et y ajouter une deuxième commande dont la liste `items` est vide (`"items": []`).
2. Exécuter la requête `LATERAL FLATTEN` : combien de lignes ? Ajouter `OUTER => TRUE` et comparer.
3. Calculer le montant de chaque commande (`SUM(qty * price)`).

### Étape 3 : fenêtrage et QUALIFY (5 minutes)

1. Sur `ORDERS_RAW`, numéroter les commandes de chaque client par date.
2. Avec `QUALIFY`, ne garder que la commande la plus chère de chaque client.
3. Sur `SNOWFLAKE_SAMPLE_DATA.TPCH_SF10.ORDERS`, comparer la durée et le résultat de `COUNT(DISTINCT o_custkey)` et de `APPROX_COUNT_DISTINCT(o_custkey)` (désactiver d'abord le cache de résultats : `ALTER SESSION SET USE_CACHED_RESULT = FALSE;`).

### Étape 4 : stream et task (10 minutes)

```sql
CREATE OR REPLACE TABLE SALES_DB.ANALYTICS.ORDERS_CHANGES (
  order_id NUMBER, order_status VARCHAR, total_amount FLOAT, action VARCHAR, traite_le TIMESTAMP_LTZ);
```

1. Créer le stream `ORDERS_STREAM` (section 6.1), puis exécuter l'`INSERT` et l'`UPDATE` de la démonstration.
2. Lire le stream deux fois de suite : le contenu change-t-il ? Combien de lignes pour l'`UPDATE` ?
3. Créer la task `TRAITER_COMMANDES` (section 7.1), ne pas la reprendre, et la lancer une fois avec `EXECUTE TASK`.
4. Vérifier : `ORDERS_CHANGES` est remplie, `SYSTEM$STREAM_HAS_DATA` renvoie `FALSE`, et l'exécution apparaît dans l'historique :

```sql
SELECT name, state, scheduled_time, error_message
FROM TABLE(SALES_DB.INFORMATION_SCHEMA.TASK_HISTORY(TASK_NAME => 'TRAITER_COMMANDES'))
ORDER BY scheduled_time DESC LIMIT 5;
```

5. Exécuter `SHOW STREAMS;` et relever les colonnes `stale` et `stale_after`.

### Étape 5 : table dynamique (5 minutes)

1. Créer la table dynamique `CA_PAR_PAYS` (section 8.1) avec un retard cible d'une minute.
2. Insérer une commande dans `ORDERS_RAW` pour un nouveau pays, attendre un peu plus d'une minute et relire la table dynamique.
3. Essayer `INSERT INTO SALES_DB.ANALYTICS.CA_PAR_PAYS VALUES ('FR', 1, 10);` et lire le message d'erreur.
4. Exécuter `SHOW DYNAMIC TABLES;` et relever les colonnes `target_lag` et `refresh_mode`.

### Nettoyage (important : une task ou une table dynamique active consomme des crédits)

```sql
ALTER TASK IF EXISTS SALES_DB.RAW_DATA.TRAITER_COMMANDES SUSPEND;
DROP TASK IF EXISTS SALES_DB.RAW_DATA.TRAITER_COMMANDES;
DROP DYNAMIC TABLE IF EXISTS SALES_DB.ANALYTICS.CA_PAR_PAYS;
DROP STREAM IF EXISTS SALES_DB.RAW_DATA.ORDERS_STREAM;
DROP TABLE IF EXISTS SALES_DB.ANALYTICS.ORDERS_CHANGES;
DROP TABLE IF EXISTS SALES_DB.RAW_DATA.ORDERS_JSON;
DELETE FROM SALES_DB.RAW_DATA.ORDERS_RAW WHERE order_id >= 9000;
UPDATE SALES_DB.RAW_DATA.ORDERS_RAW SET order_status = 'SHIPPED' WHERE order_id = 1001;   -- valeur d'origine
ALTER SESSION UNSET USE_CACHED_RESULT;
```

### Questions de réflexion

1. À l'étape 4, pourquoi le stream est-il vide après l'exécution de la task, alors qu'il ne l'était pas après vos deux `SELECT` ?
2. Vous avez deux traitements qui doivent chacun recevoir tous les changements de `ORDERS_RAW`. Que créez-vous ?
3. La même agrégation `CA_PAR_PAYS` pourrait être une vue matérialisée (édition Enterprise). Qu'y gagnerait-on, et qu'est-ce qui deviendrait impossible si l'on voulait y joindre la table des clients ?
4. Une task planifiée toutes les minutes sur un warehouse XS ne trouve des données que deux fois par jour. Que coûte-t-elle avec et sans la condition `WHEN SYSTEM$STREAM_HAS_DATA` ? Quelle autre forme de task conviendrait ?
5. Pourquoi garder le document JSON brut en `VARIANT` dans `RAW_DATA` plutôt que de n'en charger que quelques champs ?

## Points de vérification
- [ ] Je sais lire un champ JSON, le convertir, et expliquer pourquoi une clé mal écrite renvoie `NULL`
- [ ] J'ai aplati une liste avec `LATERAL FLATTEN` et vu l'effet de `OUTER => TRUE`
- [ ] J'ai dédoublonné avec `QUALIFY`
- [ ] Je sais dire quand écrire une fonction et quand écrire une procédure
- [ ] J'ai vu un `UPDATE` apparaître comme deux lignes dans un stream, et le stream se vider après un DML
- [ ] J'ai lancé une task et retrouvé son exécution dans `TASK_HISTORY`
- [ ] J'ai créé une table dynamique et constaté son rafraîchissement
- [ ] Task, table dynamique et stream de l'atelier sont supprimés

## Documentation officielle
- [Certifications Snowflake : guide de l'examen SnowPro Core](https://learn.snowflake.com/en/certifications/)
- [Interroger des données semi-structurées](https://docs.snowflake.com/en/user-guide/querying-semistructured)
- [Considérations sur les données semi-structurées](https://docs.snowflake.com/en/user-guide/semistructured-considerations)
- [FLATTEN](https://docs.snowflake.com/en/sql-reference/functions/flatten)
- [Données non structurées](https://docs.snowflake.com/en/user-guide/unstructured-intro)
- [Tables de répertoire](https://docs.snowflake.com/en/user-guide/data-load-dirtables)
- [QUALIFY](https://docs.snowflake.com/en/sql-reference/constructs/qualify)
- [Estimation du nombre de valeurs distinctes](https://docs.snowflake.com/en/user-guide/querying-approximate-cardinality)
- [Fonctions définies par l'utilisateur](https://docs.snowflake.com/en/developer-guide/udf/udf-overview)
- [Procédures stockées](https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-overview)
- [Choisir entre procédure stockée et fonction](https://docs.snowflake.com/en/developer-guide/stored-procedures-vs-udfs)
- [Introduction aux streams](https://docs.snowflake.com/en/user-guide/streams-intro)
- [Introduction aux tasks](https://docs.snowflake.com/en/user-guide/tasks-intro)
- [Tables dynamiques](https://docs.snowflake.com/en/user-guide/dynamic-tables-about)
- [Tables dynamiques, streams et tasks, vues matérialisées : comparaison](https://docs.snowflake.com/en/user-guide/dynamic-tables-comparison)
- [Transactions](https://docs.snowflake.com/en/sql-reference/transactions)

---

[← Retour au sommaire](README.md) | [← Précédent](17-performance.md) | [Suivant →](19-collaboration.md)
