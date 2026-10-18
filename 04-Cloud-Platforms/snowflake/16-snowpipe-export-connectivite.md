# 16. Aller plus loin sur le chargement : stages, Snowpipe, déchargement et connectivité

[← Retour au sommaire](README.md) | [← Précédent](15-gouvernance.md) | [Suivant →](17-performance.md)

## Vue d'ensemble

Le [chapitre 11](11-chargement-stage-copy.md) charge un fichier avec un format de fichier, un stage interne, `PUT` et `COPY INTO`. Ce chapitre élargit le sujet dans quatre directions :

- **Où poser les fichiers** : les quatre types de stages, et l'intégration de stockage qui relie Snowflake à un espace de stockage cloud.
- **Comment charger** : les options de `COPY INTO` qui tombent à l'examen, la taille des fichiers, puis le chargement continu avec Snowpipe.
- **Comment faire sortir les données** : le déchargement (`COPY INTO` vers un stage, puis `GET`), les tables externes et les tables Iceberg.
- **Comment se connecter** : outils en ligne de commande, pilotes, connecteurs, API, outils partenaires.

Dans le métier, le Data Engineer choisit entre un chargement par lots lancé par un orchestrateur et un chargement continu, livre des exports à d'autres équipes, et branche des outils sur Snowflake. À l'examen SnowPro Core, ces sujets forment le domaine 3 « Chargement, déchargement et connectivité » (18 % des questions).

Exemple suivi : `SALES_DB.RAW_DATA`, le warehouse `SALES_WH`, le rôle `SALES_ENGINEER`, le stage `VENTES_STAGE` et le format `CSV_FF` créés au chapitre 11.

```
fichiers ──PUT──> stage interne ──COPY INTO table──> table ──COPY INTO @stage──> stage ──GET──> fichiers
                  stage externe ──Snowpipe──────────> table
```

---

## 1. Les types de stages

Un stage est l'endroit où se trouvent les fichiers à charger ou les fichiers exportés. Il en existe quatre types. Les trois premiers sont **internes** : les fichiers sont stockés par Snowflake. Le quatrième est **externe** : les fichiers restent dans le stockage cloud de l'entreprise.

| Type | Référence | Création | Qui y accède | Limites |
|---|---|---|---|---|
| Stage utilisateur | `@~` | automatique, un par utilisateur | cet utilisateur seulement | ne peut être ni modifié ni supprimé ; pas d'options de format ; inadapté au partage de fichiers |
| Stage de table | `@%NOM_TABLE` | automatique, un par table | le propriétaire de la table | ne charge que dans sa table ; pas de transformation au chargement ; ce n'est pas un objet à part, on ne peut pas donner de droits dessus |
| Stage interne nommé | `@NOM_STAGE` | `CREATE STAGE` | les rôles qui ont reçu `READ` ou `WRITE` | aucun de ces défauts : c'est le choix recommandé pour un travail d'équipe |
| Stage externe | `@NOM_STAGE` | `CREATE STAGE ... URL = ...` | les rôles qui ont reçu `USAGE` | les fichiers vivent dans Amazon S3, Google Cloud Storage ou Microsoft Azure ; `PUT` et `GET` ne s'y appliquent pas |

```sql
USE ROLE SALES_ENGINEER;
USE SCHEMA SALES_DB.RAW_DATA;

LIST @~;                   -- mon stage utilisateur
LIST @%ORDERS_RAW;         -- le stage de la table ORDERS_RAW
LIST @VENTES_STAGE;        -- le stage interne nommé du chapitre 11

REMOVE @~/essais/;         -- supprimer des fichiers d'un stage
```

Un stage nommé peut porter un format de fichier par défaut : `CREATE STAGE ... FILE_FORMAT = (FORMAT_NAME = CSV_FF)`. Le `COPY INTO` n'a alors plus besoin de le préciser.

### 1.1 Stage externe et intégration de stockage

Pour lire un espace de stockage cloud, Snowflake a besoin d'une autorisation. On pourrait écrire des clés d'accès dans la définition du stage, mais elles se retrouveraient dans des scripts. La méthode recommandée est l'**intégration de stockage** (*storage integration*) : un objet de compte qui porte une identité créée par Snowflake, à laquelle l'administrateur cloud donne accès au stockage. Aucun secret ne circule.

```sql
-- 1. L'intégration : objet de compte, créé par ACCOUNTADMIN (ou un rôle qui a CREATE INTEGRATION)
USE ROLE ACCOUNTADMIN;
CREATE STORAGE INTEGRATION S3_VENTES_INT
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::001234567890:role/snowflake-ventes'
  ENABLED = TRUE
  STORAGE_ALLOWED_LOCATIONS = ('s3://ventes-entreprise/depot/');

DESC INTEGRATION S3_VENTES_INT;     -- valeurs à reporter côté cloud pour autoriser Snowflake
GRANT USAGE ON INTEGRATION S3_VENTES_INT TO ROLE SALES_ENGINEER;

-- 2. Le stage externe : objet de schéma, créé par le rôle outil
USE ROLE SALES_ENGINEER;
CREATE STAGE SALES_DB.RAW_DATA.VENTES_S3_STAGE
  URL = 's3://ventes-entreprise/depot/'
  STORAGE_INTEGRATION = S3_VENTES_INT
  FILE_FORMAT = (FORMAT_NAME = CSV_FF);
```

Une même intégration sert à plusieurs stages, dans la limite des emplacements listés par `STORAGE_ALLOWED_LOCATIONS`. Cet exemple demande un compte cloud : il n'est pas faisable sur un compte d'essai seul.

---

## 2. Les options de COPY INTO à connaître

### 2.1 Choisir les fichiers

| Option | Rôle |
|---|---|
| chemin dans le `FROM` | `FROM @VENTES_STAGE/2025/01/` : les fichiers sous ce chemin ; le plus efficace |
| `FILES = ('a.csv', 'b.csv')` | une liste de noms ; 1 000 fichiers au maximum |
| `PATTERN = '.*orders.*[.]csv'` | une expression régulière sur le chemin ; pratique mais plus lent sur un stage très rempli |

### 2.2 Vérifier avant de charger : VALIDATION_MODE

`VALIDATION_MODE` lit les fichiers et signale les erreurs **sans rien charger**.

```sql
COPY INTO ORDERS_RAW
  FROM @VENTES_STAGE
  FILES = ('orders.csv')
  FILE_FORMAT = (FORMAT_NAME = CSV_FF)
  VALIDATION_MODE = RETURN_ERRORS;
```

| Valeur | Résultat |
|---|---|
| `RETURN_n_ROWS` (par exemple `RETURN_10_ROWS`) | affiche les n premières lignes si elles sont valides ; s'arrête à la première erreur |
| `RETURN_ERRORS` | toutes les erreurs de tous les fichiers |
| `RETURN_ALL_ERRORS` | toutes les erreurs, y compris celles des fichiers chargés partiellement lors d'un chargement précédent |

`VALIDATION_MODE` n'est pas accepté quand le `COPY` transforme les données (section 2.5). Pour examiner les erreurs d'un chargement déjà exécuté, on utilise la fonction `VALIDATE` :

```sql
SELECT * FROM TABLE(VALIDATE(ORDERS_RAW, JOB_ID => '_last'));    -- erreurs du dernier COPY de la session
```

### 2.3 Que faire en cas d'erreur : ON_ERROR

| Valeur | Comportement |
|---|---|
| `ABORT_STATEMENT` | à la première erreur, rien n'est chargé. **Valeur par défaut de `COPY INTO`** |
| `CONTINUE` | charge les lignes valides, ignore les lignes en erreur |
| `SKIP_FILE` | ignore en entier tout fichier qui contient une erreur. **Valeur par défaut de Snowpipe** |
| `SKIP_FILE_10` | ignore le fichier s'il contient au moins 10 erreurs |
| `'SKIP_FILE_5%'` | ignore le fichier si plus de 5 % de ses lignes sont en erreur |

### 2.4 Après le chargement : PURGE, FORCE et les autres

| Option | Défaut | Effet |
|---|---|---|
| `PURGE = TRUE` | `FALSE` | supprime du stage les fichiers chargés avec succès |
| `FORCE = TRUE` | `FALSE` | recharge tous les fichiers, même déjà chargés : risque de doublons |
| `LOAD_UNCERTAIN_FILES = TRUE` | `FALSE` | tente de charger les fichiers dont l'historique de chargement a expiré, en évitant les doublons quand l'historique existe encore |
| `SIZE_LIMIT = n` | aucun | arrête de prendre de nouveaux fichiers une fois n octets chargés |
| `TRUNCATECOLUMNS = TRUE` | `FALSE` | coupe les textes trop longs au lieu d'échouer (`ENFORCE_LENGTH = FALSE` est l'écriture inverse) |
| `RETURN_FAILED_ONLY = TRUE` | `FALSE` | le résultat ne liste que les fichiers en échec |

Rappel du chapitre 11 : Snowflake garde pendant **64 jours** la liste des fichiers déjà chargés dans chaque table, ce qui évite les doublons. Au-delà, si un fichier ancien doit être chargé, `COPY` l'ignore par défaut : c'est le cas d'usage de `LOAD_UNCERTAIN_FILES`.

### 2.5 Transformer pendant le chargement

`COPY INTO` accepte une requête à la place du stage. Les colonnes du fichier se nomment `$1`, `$2`, etc.

```sql
COPY INTO SALES_DB.RAW_DATA.ORDERS_LIGHT (order_id, customer_id, order_day, total_ttc, source_file)
FROM (
  SELECT $1,                         -- 1re colonne du fichier
         $2,
         $3::DATE,                   -- conversion de type
         $14::NUMBER(12,2),          -- 14e colonne : on saute celles dont on n'a pas besoin
         METADATA$FILENAME           -- colonne de métadonnées
  FROM @VENTES_STAGE/orders.csv
)
FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '"');
```

| Permis | Non permis |
|---|---|
| choisir, réordonner, omettre des colonnes | filtrer avec `WHERE` |
| convertir un type (`::DATE`), tronquer un texte | joindre (`JOIN`), agréger (`GROUP BY`) |
| appliquer des fonctions simples, ajouter les colonnes `METADATA$...` | `DISTINCT`, `ORDER BY`, `LIMIT` |

Pour tout le reste, on charge d'abord les données brutes, puis on transforme en SQL dans Snowflake (démarche ELT).

On peut aussi interroger un fichier du stage sans le charger, ce qui sert à l'inspecter :

```sql
SELECT $1, $2, $3, METADATA$FILENAME, METADATA$FILE_ROW_NUMBER
FROM @VENTES_STAGE/orders.csv (FILE_FORMAT => 'CSV_FF')
LIMIT 5;
```

---

## 3. Bonnes pratiques de taille de fichiers

Un warehouse charge plusieurs fichiers en parallèle, mais ne découpe pas efficacement un seul fichier géant. À l'inverse, des milliers de fichiers minuscules coûtent cher en gestion.

- Viser des fichiers de **100 à 250 Mo compressés** (ou un peu plus).
- Éviter les fichiers très volumineux (100 Go ou plus) : les découper avant l'envoi.
- Regrouper les très petits fichiers avant de les déposer.
- Pour Snowpipe, déposer un fichier **environ une fois par minute** est un bon compromis entre coût et fraîcheur.
- Organiser les fichiers par chemin (`/2025/01/15/`) : un `COPY` qui cible un chemin lit moins de fichiers qu'un `PATTERN` sur tout le stage.

Les fichiers compressés sont reconnus automatiquement (gzip par exemple). `PUT` compresse en gzip par défaut (chapitre 11, option `AUTO_COMPRESS`).

---

## 4. Snowpipe : le chargement continu

### 4.1 L'idée

Avec `COPY INTO`, quelqu'un (ou un orchestrateur) décide du moment du chargement. Avec Snowpipe, **le fichier est chargé peu après son arrivée sur le stage**, sans planification et sans warehouse à démarrer. On parle de chargement continu, ou de micro-lots.

Un **pipe** est un objet de schéma qui contient une instruction `COPY INTO`. Snowpipe l'exécute pour chaque nouveau fichier.

```sql
CREATE PIPE SALES_DB.RAW_DATA.ORDERS_PIPE
  AUTO_INGEST = TRUE
AS
  COPY INTO SALES_DB.RAW_DATA.ORDERS_RAW
  FROM @SALES_DB.RAW_DATA.VENTES_S3_STAGE
  FILE_FORMAT = (FORMAT_NAME = CSV_FF)
  MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
```

### 4.2 Comment Snowpipe apprend qu'un fichier est arrivé

| Mécanisme | Fonctionnement | Quand l'utiliser |
|---|---|---|
| Auto-ingest (`AUTO_INGEST = TRUE`) | le stockage cloud envoie une notification d'événement à chaque nouveau fichier ; Snowpipe la reçoit et charge le fichier | stage externe, flux régulier de fichiers ; le plus courant |
| API REST (`AUTO_INGEST = FALSE`) | votre application appelle un point d'accès REST (`insertFiles`) avec le nom du pipe et la liste des fichiers | stage interne, ou quand l'application sait exactement quand un fichier est prêt |

L'appel à l'API REST de Snowpipe s'authentifie par paire de clés (jeton JWT).

### 4.3 Surveiller un pipe

```sql
SHOW PIPES IN SCHEMA SALES_DB.RAW_DATA;
SELECT SYSTEM$PIPE_STATUS('SALES_DB.RAW_DATA.ORDERS_PIPE');         -- executionState : RUNNING ou PAUSED

ALTER PIPE SALES_DB.RAW_DATA.ORDERS_PIPE SET PIPE_EXECUTION_PAUSED = TRUE;   -- mettre en pause
ALTER PIPE SALES_DB.RAW_DATA.ORDERS_PIPE REFRESH;                   -- rattrapage, voir ci-dessous

SELECT file_name, status, row_count, pipe_name, last_load_time
FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
  TABLE_NAME => 'ORDERS_RAW', START_TIME => DATEADD(HOUR, -1, CURRENT_TIMESTAMP())));
```

`ALTER PIPE ... REFRESH` met dans la file du pipe les fichiers déjà présents sur le stage, à condition qu'ils y aient été déposés depuis moins de **7 jours**. C'est un outil de dépannage, pas un mode de fonctionnement normal.

### 4.4 COPY INTO contre Snowpipe

| | `COPY INTO` (chargement par lots) | Snowpipe (chargement continu) |
|---|---|---|
| Déclenchement | une commande lancée à la main ou par un orchestrateur | automatique : notification du stockage cloud ou appel REST |
| Calcul | un warehouse choisi par l'utilisateur | des ressources fournies par Snowflake (serverless), aucun warehouse |
| Facturation | temps d'activité du warehouse | consommation serverless du pipe, sans warehouse |
| Historique des fichiers chargés | 64 jours, dans les métadonnées de la table | 14 jours, dans les métadonnées du pipe |
| Transactions | une transaction par commande `COPY` | chargements regroupés ou découpés par Snowpipe selon le volume |
| `ON_ERROR` par défaut | `ABORT_STATEMENT` | `SKIP_FILE` |
| Options refusées | aucune | `FILES`, `PURGE`, `FORCE`, `SIZE_LIMIT`, `VALIDATION_MODE`, `ON_ERROR = ABORT_STATEMENT` |
| Usage type | chargement quotidien d'un gros volume | fichiers qui arrivent au fil de l'eau |

Sur la facturation : Snowpipe est facturé comme un service serverless. La documentation actuelle décrit un nombre fixe de crédits **par gigaoctet chargé**. L'ancien modèle, encore présent dans des supports de révision, comptait le calcul consommé à la seconde plus un supplément par millier de fichiers. Dans les deux cas, l'idée à retenir est la même : pas de warehouse, et un coût visible dans `PIPE_USAGE_HISTORY`. Un resource monitor ne surveille pas Snowpipe (chapitre 15, section 7).

### 4.5 Snowpipe Streaming en bref

Snowpipe charge des **fichiers**. Snowpipe Streaming charge des **lignes**, envoyées directement par une application grâce à un kit de développement (Java, Python...) ou à une API REST : pas de fichier, pas de stage, et une donnée interrogeable en quelques secondes.

| | Snowpipe | Snowpipe Streaming |
|---|---|---|
| Unité chargée | fichier déposé sur un stage | ligne envoyée par une application |
| Délai typique | de l'ordre de la minute | de l'ordre de quelques secondes |
| Usage type | exports de fichiers réguliers | événements, capteurs, flux Kafka |

Le connecteur Kafka de Snowflake (section 7) peut s'appuyer sur Snowpipe Streaming.

---

## 5. Décharger des données

Décharger (*unload*), c'est exporter le contenu d'une table ou le résultat d'une requête vers des fichiers. Le chemin est l'inverse du chargement, en deux étapes.

### 5.1 COPY INTO vers un stage

```sql
COPY INTO @VENTES_STAGE/export/orders_
FROM (
  SELECT order_id, customer_id, order_date, ship_country, total_amount
  FROM SALES_DB.RAW_DATA.ORDERS_RAW
  WHERE order_status = 'SHIPPED'              -- ici, une vraie requête : WHERE, JOIN... sont permis
)
FILE_FORMAT = (TYPE = CSV COMPRESSION = GZIP FIELD_OPTIONALLY_ENCLOSED_BY = '"')
HEADER = TRUE
OVERWRITE = TRUE;

LIST @VENTES_STAGE/export/;
```

| Option | Défaut | Rôle |
|---|---|---|
| `FILE_FORMAT` | CSV compressé en gzip | formats de sortie possibles : **CSV, JSON, Parquet** |
| `HEADER` | `FALSE` | écrit les noms de colonnes en première ligne (et les conserve en Parquet) |
| `SINGLE` | `FALSE` | `FALSE` : plusieurs fichiers produits en parallèle ; `TRUE` : un seul fichier |
| `MAX_FILE_SIZE` | 16 Mo | taille maximale de chaque fichier ; jusqu'à 5 Go |
| `OVERWRITE` | `FALSE` | remplace les fichiers du même nom |
| `PARTITION BY` | aucun | répartit les lignes dans des sous-dossiers selon une expression |
| `INCLUDE_QUERY_ID` | `FALSE` | ajoute un identifiant unique au nom des fichiers, pour éviter les écrasements |
| `DETAILED_OUTPUT` | `FALSE` | renvoie une ligne par fichier produit au lieu d'un résumé |

Par défaut, les fichiers s'appellent `data_0_0_0.csv.gz`, `data_0_1_0.csv.gz`, etc. : le préfixe est `data_` si l'on n'en précise pas d'autre.

Pour exporter en JSON, la requête doit renvoyer une seule colonne de type `VARIANT`, construite par exemple avec `OBJECT_CONSTRUCT(*)`.

### 5.2 Partitionner l'export

```sql
COPY INTO @VENTES_STAGE/export_par_pays/
FROM (SELECT order_id, customer_id, order_date, ship_country, total_amount FROM ORDERS_RAW)
PARTITION BY ('pays=' || ship_country)
FILE_FORMAT = (TYPE = PARQUET)
HEADER = TRUE
MAX_FILE_SIZE = 32000000;
```

Le stage contient alors `export_par_pays/pays=USA/data_...parquet`, `export_par_pays/pays=France/...`. Cette organisation est celle qu'attendent les moteurs qui lisent un lac de données. `PARTITION BY` ne se combine ni avec `SINGLE = TRUE` ni avec `OVERWRITE = TRUE`.

### 5.3 GET : rapatrier les fichiers

```sql
GET @VENTES_STAGE/export/ file:///tmp/export/ PATTERN = '.*orders_.*';
```

`GET` est le symétrique de `PUT` : il télécharge des fichiers d'un **stage interne** vers le poste, et les déchiffre au passage. Comme `PUT`, il s'exécute depuis un client installé sur le poste (Snowflake CLI, SnowSQL, connecteur Python, pilotes) et **pas depuis une feuille SQL de Snowsight**. Il ne fonctionne pas sur un stage externe : là, les fichiers sont déjà dans le stockage cloud de l'entreprise, et on les récupère avec les outils du fournisseur.

On peut d'ailleurs décharger directement vers un emplacement cloud : `COPY INTO 's3://...' ... STORAGE_INTEGRATION = ...`, ou vers un stage externe.

---

## 6. Lire sans charger : tables externes et tables Iceberg

Parfois, les données doivent rester dans le stockage cloud de l'entreprise, parce que d'autres outils les lisent aussi.

| | Table standard | Table externe | Table Iceberg |
|---|---|---|---|
| Où sont les données | dans Snowflake | dans un stage externe | dans le stockage cloud de l'entreprise (volume externe), au format ouvert Apache Iceberg (fichiers Parquet) |
| Écriture depuis Snowflake | oui | non : lecture seule | oui si Snowflake gère le catalogue ; lecture seule avec un catalogue externe |
| Performance | la meilleure | plus lente : chaque requête lit des fichiers distants | proche d'une table standard |
| Usage type | l'entrepôt | interroger un lac de données sans le copier | partager les mêmes données avec d'autres moteurs (Spark, etc.) |

Une **table externe** expose chaque ligne de fichier dans une colonne `VALUE` de type `VARIANT`, accompagnée de `METADATA$FILENAME` et `METADATA$FILE_ROW_NUMBER` ; on définit par-dessus des colonnes calculées et des partitions. Snowflake tient à jour la liste des fichiers, automatiquement par notifications du stockage cloud ou manuellement avec `ALTER EXTERNAL TABLE ... REFRESH`. Une vue matérialisée sur une table externe accélère les lectures (édition Enterprise).

Une **table Iceberg** combine le stockage externe et les fonctions d'une table Snowflake. Avec un volume externe, le stockage est facturé par le fournisseur cloud de l'entreprise, pas par Snowflake (la documentation décrit aussi une variante où Snowflake stocke et facture les fichiers).

---

## 7. Connectivité : se brancher sur Snowflake

### 7.1 Panorama

| Outil | Nature | Sert à |
|---|---|---|
| Snowsight | interface web | travailler à la main : feuilles SQL, notebooks, tableaux de bord |
| Snowflake CLI (`snow`) | client en ligne de commande | exécuter du SQL, gérer les stages, déployer des applications ; client recommandé aujourd'hui |
| SnowSQL (`snowsql`) | ancien client en ligne de commande | exécuter du SQL, `PUT` et `GET` ; toujours présent à l'examen, remplacé par Snowflake CLI pour les nouveaux projets |
| Pilotes JDBC et ODBC | bibliothèques standard | brancher une application Java (JDBC) ou un outil de BI et de bureautique (ODBC) |
| Autres pilotes | Go, .NET, Node.js, PHP | brancher une application écrite dans ces langages |
| Connecteur Python | bibliothèque `snowflake-connector-python` | scripts, orchestrateurs, dbt (chapitres 10 et 11) |
| Connecteur Spark | bibliothèque pour Apache Spark | lire et écrire des tables Snowflake depuis Spark, dans les deux sens |
| Connecteur Kafka | composant Kafka Connect | verser des sujets (*topics*) Kafka dans des tables Snowflake |
| API SQL | API REST | envoyer une instruction SQL par requête HTTP, sans installer de pilote |
| Snowpark | bibliothèques Python, Java, Scala | écrire des traitements exécutés dans Snowflake ([chapitre 14](14-ia-applications.md)) |

### 7.2 Snowflake CLI

```bash
snow connection add          # enregistrer une connexion (compte, utilisateur, clé privée)
snow connection test
snow sql -q "SELECT CURRENT_USER(), CURRENT_ROLE()"
snow sql -q "PUT file://Data/saas/usage_events.csv @SALES_DB.RAW_DATA.VENTES_STAGE AUTO_COMPRESS=FALSE"
snow stage list-files @SALES_DB.RAW_DATA.VENTES_STAGE
```

SnowSQL fait les mêmes opérations SQL avec la commande `snowsql -a <compte> -u <utilisateur>`.

### 7.3 Connecteurs Kafka et Spark

- **Kafka** : le connecteur lit les messages des sujets et les écrit dans des tables. Par défaut, chaque message arrive dans deux colonnes `VARIANT`, `RECORD_CONTENT` (le message) et `RECORD_METADATA` (sujet, partition, position). Il s'appuie sur Snowpipe ou sur Snowpipe Streaming.
- **Spark** : le connecteur échange des données dans les deux sens et peut déléguer une partie des calculs à Snowflake (*query pushdown*).

### 7.4 API SQL

L'API SQL est une API REST : on envoie une instruction SQL par une requête HTTP sur le point d'accès `/api/v2/statements`, on suit son état, on récupère le résultat en JSON. Elle s'authentifie par OAuth, par paire de clés (jeton JWT) ou par jeton d'accès programmatique. Elle convient aux applications qui ne peuvent pas embarquer de pilote. Elle ne permet pas `PUT` ni `GET`.

### 7.5 Outils partenaires

Snowflake classe ses partenaires technologiques par catégorie : intégration de données (Fivetran, Matillion, Informatica, dbt), informatique décisionnelle (Tableau, Power BI, Looker), apprentissage automatique, sécurité et gouvernance. **Partner Connect**, dans Snowsight, ouvre en quelques clics un compte d'essai chez certains partenaires et crée automatiquement dans Snowflake les objets nécessaires à la connexion (base, warehouse, utilisateur et rôle dédiés). Il se lance avec le rôle `ACCOUNTADMIN`.

---

## 8. Pièges fréquents

| Piège | Ce qu'il faut savoir |
|---|---|
| Lancer `PUT` ou `GET` dans une feuille SQL de Snowsight | ces commandes demandent un client sur le poste |
| Utiliser `GET` ou `PUT` sur un stage externe | impossible : passer par les outils du fournisseur cloud |
| Croire que `VALIDATION_MODE` charge les lignes valides | il ne charge rien ; c'est `ON_ERROR = CONTINUE` qui charge les lignes valides |
| Supposer le même `ON_ERROR` par défaut partout | `ABORT_STATEMENT` pour `COPY`, `SKIP_FILE` pour Snowpipe |
| Mettre `PURGE = TRUE` dans un pipe | option refusée par Snowpipe : supprimer les fichiers par un autre moyen |
| Filtrer avec `WHERE` dans un `COPY INTO` de chargement | non permis au chargement ; permis au déchargement |
| Confondre les durées d'historique | 64 jours pour `COPY` (table), 14 jours pour Snowpipe (pipe) |
| Utiliser `FORCE = TRUE` pour « réparer » un chargement | recharge tout et crée des doublons |
| Attendre un seul fichier d'un déchargement | `SINGLE = FALSE` par défaut : plusieurs fichiers de 16 Mo au plus |
| Charger depuis un stage de table vers une autre table | un stage de table ne sert qu'à sa table |
| Compter sur `ALTER PIPE REFRESH` au quotidien | outil de rattrapage, limité aux fichiers de moins de 7 jours |
| Déposer des milliers de fichiers de quelques kilooctets | viser 100 à 250 Mo compressés |

---

## 9. À retenir pour la certification

- Quatre stages : utilisateur `@~`, table `@%table`, interne nommé `@stage`, externe `@stage` avec `URL`. Les stages utilisateur et de table sont créés automatiquement et ne peuvent être ni modifiés ni supprimés.
- Intégration de stockage : objet de **compte**, créé par `ACCOUNTADMIN` (privilège `CREATE INTEGRATION`), qui évite d'écrire des clés d'accès dans le stage.
- Formats au chargement : CSV, JSON, Avro, ORC, Parquet, XML. Formats au déchargement : **CSV, JSON, Parquet**.
- `VALIDATION_MODE` : `RETURN_n_ROWS`, `RETURN_ERRORS`, `RETURN_ALL_ERRORS` ; ne charge rien ; incompatible avec une transformation.
- `ON_ERROR` : `ABORT_STATEMENT` par défaut pour `COPY`, `SKIP_FILE` par défaut pour Snowpipe.
- `PURGE = TRUE` supprime les fichiers chargés ; `FORCE = TRUE` recharge tout.
- Historique de chargement : **64 jours** (`COPY`), **14 jours** (Snowpipe).
- `FILES` : 1 000 fichiers au maximum par commande.
- Taille de fichier recommandée : **100 à 250 Mo compressés**.
- Snowpipe : serverless, sans warehouse ; déclenché par notification cloud (auto-ingest) ou par API REST ; un pipe contient un `COPY INTO`.
- Snowpipe Streaming : des lignes et non des fichiers, sans stage, latence de quelques secondes.
- Déchargement : `COPY INTO @stage FROM (requête)` ; `SINGLE = FALSE` et `MAX_FILE_SIZE` de 16 Mo par défaut, 5 Go au maximum ; `PARTITION BY` pour organiser en dossiers.
- `PUT` et `GET` : stages internes seulement, client sur le poste seulement.
- Table externe : lecture seule, colonne `VALUE` en `VARIANT`.
- Le connecteur Kafka écrit `RECORD_CONTENT` et `RECORD_METADATA`. L'API SQL est une API REST.

---

## 10. Atelier pratique (45 minutes)

Objectif : charger un fichier d'événements avec contrôle préalable et transformation, simuler un chargement continu avec un pipe, puis exporter un résultat partitionné.

Données : `Data/saas/usage_events.csv` (29 événements ; la colonne `properties` contient du JSON) et la table `ORDERS_RAW` du chapitre 11.

Prérequis : un client capable d'exécuter `PUT` et `GET` (Snowflake CLI, ou le connecteur Python du chapitre 11). Aucune étape ne demande d'édition particulière. Le stage externe, l'intégration de stockage et l'auto-ingest de Snowpipe demandent un compte cloud (AWS, Azure ou Google Cloud) : l'atelier les remplace par un stage interne et un déclenchement manuel du pipe.

### Étape 1 : trois stages (8 minutes)

```sql
USE ROLE SALES_ENGINEER;
USE WAREHOUSE SALES_WH;
USE SCHEMA SALES_DB.RAW_DATA;

CREATE TABLE IF NOT EXISTS USAGE_EVENTS_RAW (
  event_id VARCHAR, user_id NUMBER, event_type VARCHAR, event_timestamp TIMESTAMP_NTZ,
  properties VARIANT, session_id VARCHAR, page_url VARCHAR, user_agent VARCHAR,
  _source_file VARCHAR
);
```

Depuis votre client, déposez le fichier sur votre stage utilisateur, sur le stage de la table et sur `VENTES_STAGE` (`PUT file://.../usage_events.csv @~/atelier/ AUTO_COMPRESS=FALSE`, puis `@%USAGE_EVENTS_RAW`, puis `@VENTES_STAGE/events/`). Vérifiez avec trois `LIST`.

### Étape 2 : inspecter et valider sans charger (8 minutes)

```sql
CREATE OR REPLACE FILE FORMAT CSV_SKIP_FF
  TYPE = CSV SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '"';

SELECT $1, $3, $5 FROM @VENTES_STAGE/events/ (FILE_FORMAT => 'CSV_SKIP_FF') LIMIT 5;

COPY INTO USAGE_EVENTS_RAW FROM @VENTES_STAGE/events/
  FILE_FORMAT = (FORMAT_NAME = CSV_SKIP_FF)
  VALIDATION_MODE = RETURN_ERRORS;
```

Le fichier a 8 colonnes et la table 9 : que signale la validation ? Relancez avec `RETURN_5_ROWS` après avoir ajouté `ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE` au format.

### Étape 3 : charger en transformant (8 minutes)

```sql
COPY INTO USAGE_EVENTS_RAW
FROM (
  SELECT $1, $2, $3, $4, PARSE_JSON($5), $6, $7, $8, METADATA$FILENAME
  FROM @VENTES_STAGE/events/
)
FILE_FORMAT = (FORMAT_NAME = CSV_SKIP_FF)
ON_ERROR = CONTINUE;

SELECT event_type, properties:device::STRING AS appareil, COUNT(*) FROM USAGE_EVENTS_RAW GROUP BY 1, 2;
```

Relancez le même `COPY` : combien de fichiers traités ? Relancez-le avec `FORCE = TRUE`, comptez les lignes, puis videz la table avec `TRUNCATE TABLE` et rechargez une seule fois.

### Étape 4 : un pipe sans compte cloud (10 minutes)

```sql
TRUNCATE TABLE USAGE_EVENTS_RAW;

CREATE OR REPLACE PIPE EVENTS_PIPE AS
  COPY INTO USAGE_EVENTS_RAW
  FROM (SELECT $1, $2, $3, $4, PARSE_JSON($5), $6, $7, $8, METADATA$FILENAME FROM @VENTES_STAGE/events/)
  FILE_FORMAT = (FORMAT_NAME = CSV_SKIP_FF);

SELECT SYSTEM$PIPE_STATUS('EVENTS_PIPE');
ALTER PIPE EVENTS_PIPE REFRESH;            -- tient lieu de notification : met les fichiers du stage dans la file
```

Attendez une minute, puis comptez les lignes et consultez `COPY_HISTORY` (section 4.3) : la colonne `pipe_name` est-elle remplie ? Avez-vous eu besoin que `SALES_WH` soit démarré pour ce chargement ? Si le pipe refuse de se créer, vérifiez que `SALES_ENGINEER` a le privilège `CREATE PIPE` sur le schéma (à donner avec `SYSADMIN`).

### Étape 5 : décharger et rapatrier (10 minutes)

1. Exportez `ORDERS_RAW` en Parquet, partitionné par `ship_country`, avec le `COPY INTO` de la section 5.2. Listez le stage.
2. Exportez les événements en un seul fichier CSV avec en-tête (`SINGLE = TRUE`, `HEADER = TRUE`) sous `@VENTES_STAGE/export/events.csv.gz`.
3. Depuis votre client, rapatriez ce fichier avec `GET` et ouvrez-le.

Variante si vous disposez d'un compte cloud : créez l'intégration de stockage et le stage externe de la section 1.1, puis le pipe de la section 4.1 avec `AUTO_INGEST = TRUE`, et déposez un fichier dans le stockage.

### Nettoyage

```sql
DROP PIPE IF EXISTS EVENTS_PIPE;
REMOVE @VENTES_STAGE/events/;  REMOVE @VENTES_STAGE/export/;  REMOVE @VENTES_STAGE/export_par_pays/;
REMOVE @~/atelier/;
DROP TABLE IF EXISTS USAGE_EVENTS_RAW;     -- supprime aussi le stage de la table
DROP FILE FORMAT IF EXISTS CSV_SKIP_FF;
```

### Questions de réflexion

1. Pourquoi le chargement de l'étape 3 ne pouvait-il pas être précédé d'un `VALIDATION_MODE` sur la même instruction ?
2. Des fichiers de 2 Ko arrivent toutes les dix secondes, ou un fichier de 30 Go arrive chaque nuit : que proposez-vous dans chaque cas ?
3. Un fichier chargé par un pipe il y a 20 jours est déposé de nouveau sous le même nom. Sera-t-il rechargé ? Et avec un `COPY INTO` manuel ?
4. Une équipe partenaire lit vos exports avec Spark. Quel format et quelle organisation de fichiers lui livrez-vous ?
5. Votre entreprise veut que les données restent dans son propre stockage cloud, lisibles par d'autres moteurs, tout en les modifiant depuis Snowflake. Table externe ou table Iceberg ?

---

## ✅ Points de vérification
- [ ] Je sais référencer les quatre types de stages et citer une limite de chacun
- [ ] Je sais pourquoi on utilise une intégration de stockage et qui la crée
- [ ] J'ai utilisé `VALIDATION_MODE` et je sais qu'il ne charge rien
- [ ] Je connais les valeurs de `ON_ERROR` et leurs valeurs par défaut (`COPY` et Snowpipe)
- [ ] J'ai chargé un fichier en transformant ses colonnes dans le `COPY INTO`
- [ ] Je connais la taille de fichier recommandée
- [ ] Je sais expliquer cinq différences entre `COPY INTO` et Snowpipe
- [ ] J'ai déchargé une table vers un stage, avec partitionnement, puis rapatrié un fichier avec `GET`
- [ ] Je sais distinguer table externe et table Iceberg
- [ ] Je sais quel outil de connexion choisir pour un script, un outil de BI, Spark, Kafka ou un appel HTTP

## Documentation officielle
- [Choisir un stage interne](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage)
- [CREATE STORAGE INTEGRATION](https://docs.snowflake.com/en/sql-reference/sql/create-storage-integration)
- [COPY INTO table](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table)
- [Transformer les données pendant un chargement](https://docs.snowflake.com/en/user-guide/data-load-transform)
- [Préparer les fichiers de données (tailles recommandées)](https://docs.snowflake.com/en/user-guide/data-load-considerations-prepare)
- [Considérations sur le chargement (historique de 64 jours)](https://docs.snowflake.com/en/user-guide/data-load-considerations-load)
- [Introduction à Snowpipe](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro)
- [CREATE PIPE](https://docs.snowflake.com/en/sql-reference/sql/create-pipe)
- [Coûts de Snowpipe](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-billing)
- [Snowpipe Streaming](https://docs.snowflake.com/en/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview)
- [COPY INTO location (déchargement)](https://docs.snowflake.com/en/sql-reference/sql/copy-into-location)
- [GET](https://docs.snowflake.com/en/sql-reference/sql/get)
- [Tables externes](https://docs.snowflake.com/en/user-guide/tables-external-intro)
- [Tables Apache Iceberg](https://docs.snowflake.com/en/user-guide/tables-iceberg)
- [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index)
- [SnowSQL](https://docs.snowflake.com/en/user-guide/snowsql)
- [Pilotes et connecteurs](https://docs.snowflake.com/en/developer-guide/drivers)
- [Connecteur Kafka](https://docs.snowflake.com/en/user-guide/kafka-connector)
- [API SQL](https://docs.snowflake.com/en/developer-guide/sql-api/index)
- [Partner Connect](https://docs.snowflake.com/en/user-guide/ecosystem-partner-connect)

---

[← Retour au sommaire](README.md) | [← Précédent](15-gouvernance.md) | [Suivant →](17-performance.md)
