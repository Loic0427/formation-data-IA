# 13. Stockage et protection des données : micro-partitions, tables, vues, Time Travel, Fail-safe et clonage

[← Retour au sommaire](README.md) | [← Précédent](12-architecture.md) | [Suivant →](14-ia-applications.md)

## Vue d'ensemble

Le chapitre 12 a présenté la couche de stockage comme « la réserve ». Ce chapitre ouvre la porte de la réserve : comment les données y sont rangées, quels types de tables et de vues existent, et comment Snowflake permet de revenir en arrière après une erreur.

C'est utile dans le métier pour trois raisons :
- **réparer une erreur** : un `DELETE` sans `WHERE` ou un `DROP TABLE` malheureux se rattrape en une commande, à condition de savoir laquelle et dans quel délai ;
- **choisir le bon type de table** : une table de travail n'a pas besoin de la même protection qu'une table de référence, et la différence se voit sur la facture ;
- **comprendre la vitesse des requêtes** : une requête est rapide quand Snowflake peut éviter de lire la plus grande partie de la table.

Programme de l'examen : micro-partitions, clustering, types de tables et types de vues relèvent du domaine 1 ; Time Travel, Fail-safe et clonage sont rattachés au domaine 5 (collaboration et protection des données). Ils sont traités ensemble ici parce qu'ils reposent tous sur le même mécanisme.

Exemple suivi : la table `SALES_DB.RAW_DATA.ORDERS_RAW` chargée au chapitre 11, avec le rôle `SALES_ENGINEER` et le warehouse `SALES_WH`.

---

## 1. Les micro-partitions

### 1.1 L'idée en une image

Imaginez des archives rangées dans des cartons. Sur chaque carton, une étiquette indique ce qu'il contient : « commandes du 3 au 9 janvier, montants de 12 à 950 euros ». Pour trouver les commandes du 5 janvier, on lit les étiquettes et on n'ouvre que les cartons concernés.

Dans Snowflake, les cartons sont les **micro-partitions** et les étiquettes sont les **métadonnées**.

```
Table ORDERS_RAW
┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐
│ micro-partition 1  │ │ micro-partition 2  │ │ micro-partition 3  │
│ order_date :       │ │ order_date :       │ │ order_date :       │
│  01/01 → 31/01     │ │  01/02 → 29/02     │ │  01/03 → 31/03     │
└────────────────────┘ └────────────────────┘ └────────────────────┘

SELECT ... WHERE order_date = '2024-02-14'
→ seule la micro-partition 2 est lue : c'est l'élagage (pruning)
```

### 1.2 Les caractéristiques à connaître

| Caractéristique | Détail |
|---|---|
| Création | automatique, pour toutes les tables, dans l'ordre d'arrivée des données ; il n'y a rien à déclarer |
| Taille | entre 50 et 500 Mo de données **avant compression** par micro-partition |
| Organisation | en colonnes : chaque colonne est stockée et compressée séparément ; une requête ne lit que les colonnes qu'elle cite |
| Immuabilité | une micro-partition n'est jamais modifiée : un `UPDATE` ou un `DELETE` en écrit de nouvelles et retire les anciennes de la version courante de la table |
| Métadonnées | pour chaque micro-partition : plage de valeurs (minimum et maximum) de chaque colonne, nombre de valeurs distinctes, et d'autres propriétés utiles à l'optimisation |

L'immuabilité est la clé de tout le chapitre : puisque les anciennes micro-partitions ne sont pas modifiées mais seulement mises de côté, Snowflake peut les conserver un certain temps (Time Travel, Fail-safe) ou les partager entre deux tables (clonage).

### 1.3 L'élagage

L'**élagage** (*pruning*) consiste à écarter, grâce aux métadonnées, les micro-partitions qui ne peuvent pas contenir les lignes demandées, avant même de les lire. On le vérifie dans le profil de la requête (*Query Profile*), qui affiche les micro-partitions lues sur le total (*Partitions scanned* / *Partitions total*).

L'élagage fonctionne bien quand le filtre porte sur une colonne dont les valeurs sont regroupées dans peu de micro-partitions. C'est naturellement le cas des dates dans une table chargée jour après jour. Il fonctionne mal si le filtre applique une fonction à la colonne ou si les valeurs sont éparpillées dans toutes les micro-partitions.

### 1.4 Le clustering

Le **clustering** désigne la façon dont les valeurs d'une colonne sont regroupées dans les micro-partitions. Deux indicateurs le mesurent : le recouvrement (*overlap*, combien de micro-partitions partagent les mêmes plages de valeurs) et la profondeur (*clustering depth*, de 1 à plus ; plus elle est faible, meilleur est le regroupement).

Sur une très grande table dont les requêtes filtrent toujours sur les mêmes colonnes, on peut déclarer une **clé de clustering** : Snowflake réorganise alors la table en arrière-plan pour maintenir le regroupement. Ce service, le clustering automatique, est *serverless* : il consomme des crédits sans passer par vos warehouses.

```sql
USE ROLE SALES_ENGINEER;
USE WAREHOUSE SALES_WH;
USE SCHEMA SALES_DB.RAW_DATA;

SELECT SYSTEM$CLUSTERING_INFORMATION('ORDERS_RAW', '(order_date)');   -- état du regroupement sur order_date

ALTER TABLE ORDERS_RAW CLUSTER BY (order_date);     -- déclare une clé de clustering
ALTER TABLE ORDERS_RAW DROP CLUSTERING KEY;         -- la retire
```

Une clé de clustering n'a d'intérêt que sur de très gros volumes (la documentation parle de tables de plusieurs téraoctets). Sur les petites tables de ce cours, elle coûterait sans rien apporter : ne la laissez pas en place.

---

## 2. Les types de tables

### 2.1 Les trois types de base : permanente, transitoire, temporaire

```sql
CREATE TABLE ORDERS_REF (order_id NUMBER, total_amount FLOAT);                 -- permanente (défaut)
CREATE TRANSIENT TABLE ORDERS_STAGING (order_id NUMBER, total_amount FLOAT);   -- transitoire
CREATE TEMPORARY TABLE ORDERS_TMP (order_id NUMBER, total_amount FLOAT);       -- temporaire
```

| Type | Durée de vie | Visible par | Time Travel | Fail-safe | Usage |
|---|---|---|---|---|---|
| Permanente (édition Standard) | jusqu'au `DROP` | tous les rôles autorisés | 0 ou 1 jour (défaut : 1) | 7 jours | données à protéger |
| Permanente (Enterprise et plus) | jusqu'au `DROP` | tous les rôles autorisés | 0 à 90 jours (défaut : 1) | 7 jours | données à protéger |
| Transitoire (`TRANSIENT`) | jusqu'au `DROP` | tous les rôles autorisés | 0 ou 1 jour (défaut : 1) | aucun | données intermédiaires que l'on sait reconstruire |
| Temporaire (`TEMPORARY`) | la session | la session qui l'a créée | 0 ou 1 jour (défaut : 1) | aucun | calculs de travail d'une session |

Points à retenir :
- le type se choisit à la création et **ne se change pas** ensuite : pour transformer une table transitoire en table permanente, il faut en créer une nouvelle et y copier les données ;
- une table temporaire peut porter le même nom qu'une table permanente du même schéma : dans la session, c'est la temporaire qui est utilisée, et elle masque l'autre ;
- une table temporaire occupe du stockage facturé tant qu'elle existe : supprimez-la quand vous n'en avez plus besoin, surtout dans une session longue ;
- il existe aussi des **bases** et des **schémas** transitoires : toutes les tables qu'on y crée sont transitoires.

Les outils de transformation comme dbt créent souvent leurs tables en transitoire : elles se reconstruisent à chaque exécution, les protéger sept jours de plus ne sert à rien.

### 2.2 Les autres types au programme

| Type | Ce que c'est | Où sont les données | Écriture | À retenir |
|---|---|---|---|---|
| Externe (`EXTERNAL TABLE`) | une table qui lit des fichiers restés dans un stage externe | dans votre stockage cloud | lecture seule | Snowflake ne garde que des métadonnées sur les fichiers ; chaque ligne est exposée dans une colonne `VALUE` de type `VARIANT` ; les métadonnées se rafraîchissent automatiquement (notifications du fournisseur cloud) ou manuellement |
| Apache Iceberg (`ICEBERG TABLE`) | une table au format ouvert Iceberg (fichiers Parquet), lisible par d'autres moteurs | le plus souvent dans votre stockage cloud, déclaré par un volume externe (*external volume*) | lecture et écriture | le catalogue est tenu par Snowflake (prise en charge complète) ou par un catalogue externe (prise en charge plus limitée) ; quand les fichiers sont chez vous, le stockage est facturé par votre fournisseur cloud et sans Fail-safe |
| Dynamique (`DYNAMIC TABLE`) | une table définie par une requête, que Snowflake tient à jour tout seul | dans Snowflake | pas d'écriture directe | on fixe une fraîcheur cible avec `TARGET_LAG` et un warehouse pour les rafraîchissements ; remplace bien des montages de streams et de tâches |

```sql
-- Table dynamique : ventes par jour, jamais en retard de plus d'une heure sur ORDERS_RAW
CREATE OR REPLACE DYNAMIC TABLE SALES_DB.ANALYTICS.DAILY_SALES_DT
  TARGET_LAG = '1 hour'
  WAREHOUSE = SALES_WH
  AS
  SELECT order_date, COUNT(*) AS nb_commandes, SUM(total_amount) AS chiffre_affaires
  FROM SALES_DB.RAW_DATA.ORDERS_RAW
  GROUP BY order_date;
```

`TARGET_LAG` peut aussi valoir `DOWNSTREAM` : la table ne se rafraîchit alors que lorsque les tables dynamiques qui dépendent d'elle en ont besoin. Le rôle doit avoir le privilège `CREATE DYNAMIC TABLE` sur le schéma. Une table dynamique coûte du calcul (le warehouse des rafraîchissements) et du stockage.

Hors programme, à connaître de nom : la **table hybride** (*hybrid table*) est stockée en lignes, avec clé primaire obligatoire et contraintes réellement appliquées, pour des applications transactionnelles à faible latence. Dans les tables ordinaires, les contraintes de clé primaire, d'unicité et de clé étrangère sont déclaratives et ne sont pas vérifiées ; seul `NOT NULL` l'est.

### 2.3 Comment choisir

```
Les données sont-elles dans Snowflake ?
├── non, elles restent dans mon stockage cloud
│     ├── format Iceberg, partagé avec d'autres moteurs  → table Iceberg
│     └── fichiers à interroger sans les charger         → table externe
└── oui
      ├── résultat d'une requête à tenir à jour          → table dynamique
      ├── besoin limité à ma session                     → table temporaire
      ├── données que je sais reconstruire               → table transitoire
      └── données à protéger                             → table permanente
```

---

## 3. Les types de vues

Une vue est une requête enregistrée sous un nom, que l'on interroge comme une table. Elle est en lecture seule.

```sql
USE SCHEMA SALES_DB.ANALYTICS;

-- Vue standard : la requête est rejouée à chaque appel
CREATE OR REPLACE VIEW V_ORDERS_FR AS
  SELECT order_id, order_date, total_amount
  FROM SALES_DB.RAW_DATA.ORDERS_RAW
  WHERE ship_country = 'France';

-- Vue sécurisée : la définition est cachée aux rôles qui ne possèdent pas la vue
CREATE OR REPLACE SECURE VIEW V_ORDERS_FR_SECURE AS
  SELECT order_id, order_date, total_amount
  FROM SALES_DB.RAW_DATA.ORDERS_RAW
  WHERE ship_country = 'France';

-- Vue matérialisée : le résultat est stocké et tenu à jour par Snowflake (édition Enterprise)
CREATE OR REPLACE MATERIALIZED VIEW MV_SALES_BY_COUNTRY AS
  SELECT ship_country, COUNT(*) AS nb_commandes, SUM(total_amount) AS chiffre_affaires
  FROM SALES_DB.RAW_DATA.ORDERS_RAW
  GROUP BY ship_country;
```

| | Vue standard | Vue sécurisée | Vue matérialisée |
|---|---|---|---|
| Résultat stocké | non | non | oui |
| Coût de stockage | aucun | aucun | oui |
| Coût de calcul | à chaque requête | à chaque requête | maintenance en arrière-plan (*serverless*), puis lecture rapide |
| Requête autorisée | toute requête | toute requête | **une seule table**, pas de jointure, pas de fonction de fenêtrage, pas de `HAVING`, `ORDER BY` ni `LIMIT`, pas d'UDF |
| Définition visible | par les rôles qui ont accès à la vue | par les rôles autorisés seulement (propriétaire) | selon qu'elle est sécurisée ou non |
| Performance | celle de la requête | parfois plus lente : certaines optimisations sont désactivées pour ne rien laisser deviner des données cachées | rapide |
| Édition minimale | Standard | Standard | Enterprise |
| Usage | simplifier, réutiliser, restreindre des colonnes | exposer des données à d'autres sans révéler la logique ni les lignes filtrées ; partage de données | accélérer une agrégation coûteuse et souvent demandée sur une table qui change peu |

Compléments :
- « sécurisée » et « matérialisée » se combinent : `CREATE SECURE MATERIALIZED VIEW` existe ;
- une vue matérialisée renvoie toujours un résultat à jour : si la maintenance est en retard, Snowflake complète avec la table de base ;
- le privilège `CREATE MATERIALIZED VIEW` est distinct de `CREATE VIEW` ;
- ne rendez pas toutes les vues sécurisées par principe : la sécurité se paie en performance.

Vue matérialisée ou table dynamique ? La vue matérialisée porte sur une seule table et reste toujours exacte ; la table dynamique accepte les jointures et les enchaînements, avec un retard maîtrisé par `TARGET_LAG`.

---

## 4. Time Travel : revenir en arrière

### 4.1 Le principe

Quand une ligne est modifiée ou supprimée, les anciennes micro-partitions ne sont pas effacées tout de suite : elles sont conservées pendant la **durée de rétention**. Tant qu'elles existent, on peut :
- **interroger** une table telle qu'elle était à un instant passé ;
- **restaurer** une table, un schéma ou une base supprimés ;
- **cloner** un objet tel qu'il était à un instant passé.

### 4.2 La durée de rétention

| Objet | Standard | Enterprise et plus |
|---|---|---|
| Table permanente | 0 ou 1 jour | 0 à 90 jours |
| Table transitoire ou temporaire | 0 ou 1 jour | 0 ou 1 jour |

La valeur par défaut est de **1 jour** pour tous les comptes. Elle se règle avec le paramètre `DATA_RETENTION_TIME_IN_DAYS`, sur le compte, une base, un schéma ou une table (le réglage le plus précis l'emporte, chapitre 12, section 4.3).

```sql
ALTER TABLE ORDERS_RAW SET DATA_RETENTION_TIME_IN_DAYS = 30;     -- édition Enterprise
SHOW TABLES LIKE 'ORDERS_RAW';                                    -- colonne retention_time
```

- Une rétention de **0** désactive le Time Travel pour l'objet.
- Un administrateur peut imposer un plancher au niveau du compte avec `MIN_DATA_RETENTION_TIME_IN_DAYS` : la rétention effective est alors la plus grande des deux valeurs.
- Allonger la rétention augmente le stockage facturé (section 7).

### 4.3 Interroger le passé : AT et BEFORE

```sql
-- État de la table il y a 10 minutes (décalage en secondes, négatif)
SELECT COUNT(*) FROM ORDERS_RAW AT(OFFSET => -60*10);

-- État de la table à une date et une heure précises
SELECT COUNT(*) FROM ORDERS_RAW AT(TIMESTAMP => '2026-10-04 09:00:00'::TIMESTAMP_LTZ);

-- État de la table juste avant une instruction donnée (identifiant de requête)
SELECT COUNT(*) FROM ORDERS_RAW BEFORE(STATEMENT => '01b2c3d4-0000-1234-0000-000000000000');
```

| Mot-clé | Sens |
|---|---|
| `AT` | l'état à l'instant indiqué, modifications de cet instant comprises |
| `BEFORE` | l'état juste avant l'instant ou l'instruction indiqués |

| Repère | Valeur attendue |
|---|---|
| `TIMESTAMP` | une date et une heure |
| `OFFSET` | un nombre de secondes par rapport à maintenant (négatif) |
| `STATEMENT` | l'identifiant d'une requête (onglet historique des requêtes, ou `LAST_QUERY_ID()`) |

### 4.4 Réparer une erreur de modification

```sql
DELETE FROM ORDERS_RAW;                       -- l'erreur : pas de WHERE
SET requete_fautive = LAST_QUERY_ID();        -- on retient l'identifiant du DELETE

-- Réparation : remettre les lignes telles qu'elles étaient juste avant
INSERT INTO ORDERS_RAW
  SELECT * FROM ORDERS_RAW BEFORE(STATEMENT => $requete_fautive);
```

Autre méthode : créer une copie de la table à l'instant voulu avec un clone (section 6), la vérifier, puis l'échanger avec la table abîmée.

### 4.5 Restaurer un objet supprimé : UNDROP

```sql
DROP TABLE ORDERS_RAW;
SHOW TABLES HISTORY LIKE 'ORDERS_RAW';        -- la colonne dropped_on est remplie
UNDROP TABLE ORDERS_RAW;                      -- la table revient, avec ses données et ses droits
```

`UNDROP` existe notamment pour les tables, les schémas et les bases (`UNDROP SCHEMA`, `UNDROP DATABASE`). Deux règles :
- il ne fonctionne que pendant la durée de rétention de l'objet ;
- il **échoue si un objet du même nom existe déjà** : il faut d'abord renommer l'objet présent. Après un `CREATE OR REPLACE TABLE`, l'ancienne version se récupère donc en renommant la nouvelle puis en lançant `UNDROP`.

---

## 5. Fail-safe : le dernier recours

Quand la durée de rétention du Time Travel est écoulée, les données d'une table permanente entrent en **Fail-safe** pour **7 jours**.

```
modification ou suppression
        │
        ▼
┌───────────────────────────┐   ┌──────────────────┐
│ Time Travel               │   │ Fail-safe        │
│ 0 à 90 jours selon        │ → │ 7 jours          │ → suppression définitive
│ l'édition et le réglage   │   │ non réglable     │
│ vous agissez vous-même    │   │ Snowflake seul   │
└───────────────────────────┘   └──────────────────┘
```

| | Time Travel | Fail-safe |
|---|---|---|
| Durée | 0 à 90 jours, réglable | 7 jours, **non réglable** |
| Qui récupère les données | vous, en SQL (`AT`, `BEFORE`, `UNDROP`, clone) | **Snowflake uniquement**, sur demande au support |
| Tables concernées | permanentes, transitoires, temporaires | **permanentes seulement** |
| Usage | opérations courantes | dernier recours après un incident grave ; la récupération peut prendre de plusieurs heures à plusieurs jours |

Le Fail-safe n'est pas une sauvegarde à la demande : on ne peut ni l'interroger ni le désactiver sur une table permanente. Pour ne pas le payer, on utilise une table transitoire. Sur une table permanente en édition Enterprise, la protection continue maximale est donc de 90 + 7 = 97 jours.

---

## 6. Le clonage sans copie

### 6.1 Le principe

Un **clone** est une copie instantanée d'une table, d'un schéma ou d'une base. Rien n'est recopié : le clone pointe vers les mêmes micro-partitions que l'original (*zero-copy cloning*). Les deux objets vivent ensuite leur vie séparément.

```
Juste après le clonage            Après un UPDATE sur le clone
ORDERS_RAW    ORDERS_DEV          ORDERS_RAW    ORDERS_DEV
   │  │  │      │  │  │              │  │  │      │  │  │
   ▼  ▼  ▼      ▼  ▼  ▼              ▼  ▼  ▼      ▼  ▼  ▼
  [P1][P2][P3] (partagées)          [P1][P2][P3] [P1][P2][P4]
  stockage en plus : aucun          stockage en plus : P4 seulement
```

### 6.2 Les commandes

```sql
-- Copie de travail pour tester une transformation sans risque
CREATE TABLE ORDERS_DEV CLONE ORDERS_RAW;

-- Clone de la table telle qu'elle était il y a une heure (clone + Time Travel)
CREATE TABLE ORDERS_AVANT CLONE ORDERS_RAW AT(OFFSET => -3600);

-- Environnement de développement complet (rôle disposant du droit de créer une base)
USE ROLE SYSADMIN;
CREATE DATABASE SALES_DB_DEV CLONE SALES_DB;
```

### 6.3 Les règles

| Sujet | Règle |
|---|---|
| Objets clonables | surtout bases, schémas et tables ; aussi d'autres objets de schéma : tables dynamiques, stages externes, formats de fichier, séquences, streams, tâches, entre autres (voir la documentation de `CREATE ... CLONE`) |
| Coût à la création | aucun stockage supplémentaire ; seules les micro-partitions créées ensuite par des modifications, d'un côté ou de l'autre, sont facturées |
| Indépendance | modifier ou supprimer le clone ne touche pas l'original, et inversement |
| Droits | le clone d'une table ne reprend pas les droits de la table source, sauf avec `COPY GRANTS` ; le clone d'une base ou d'un schéma ne reprend pas les droits donnés sur le conteneur, mais les objets qu'il contient gardent les leurs |
| Historique de chargement | le clone d'une table ne reprend pas l'historique des fichiers chargés par `COPY INTO` : un même fichier peut donc y être rechargé |
| Stages internes | un stage interne nommé n'est pas cloné avec le schéma ou la base, sauf demande explicite (`INCLUDE INTERNAL STAGES`) |
| Tâches | les tâches clonées sont créées suspendues |
| Types | une table permanente peut être clonée en table transitoire ou temporaire ; une table transitoire ou temporaire ne peut pas être clonée en table permanente |
| Tables externes | elles ne sont pas clonées |

---

## 7. Les coûts de stockage associés

Le stockage facturé d'une table comprend ses données courantes, son historique de Time Travel et son Fail-safe. L'historique ne contient que les micro-partitions **modifiées ou supprimées**, pas une copie complète de la table par jour.

| Type de table | Jours d'historique facturables au maximum après une modification |
|---|---|
| Permanente, rétention de 1 jour | 1 (Time Travel) + 7 (Fail-safe) = 8 |
| Permanente, rétention de 90 jours | 90 + 7 = 97 |
| Transitoire ou temporaire | 1 au maximum, aucun Fail-safe |

Cas à surveiller : une table permanente **entièrement réécrite chaque jour**. Chaque réécriture envoie toutes les anciennes micro-partitions en Time Travel puis en Fail-safe, et l'historique peut peser plusieurs fois la table. C'est le cas typique où une table transitoire s'impose.

```sql
-- Répartition du stockage d'une table, en octets
SELECT table_name, active_bytes, time_travel_bytes, failsafe_bytes, retained_for_clone_bytes
FROM SALES_DB.INFORMATION_SCHEMA.TABLE_STORAGE_METRICS
WHERE table_schema = 'RAW_DATA';
```

| Colonne | Sens |
|---|---|
| `active_bytes` | données courantes de la table |
| `time_travel_bytes` | historique conservé pour le Time Travel |
| `failsafe_bytes` | données en Fail-safe |
| `retained_for_clone_bytes` | micro-partitions que la table n'utilise plus mais qu'un clone utilise encore |

---

## 8. Pièges fréquents

| Confusion | La réalité |
|---|---|
| « Le Fail-safe se règle comme le Time Travel » | il dure 7 jours, sans réglage possible, et seul le support de Snowflake peut y récupérer des données |
| « Une table transitoire n'a pas de Time Travel » | elle a 0 ou 1 jour de Time Travel ; ce qu'elle n'a pas, c'est le Fail-safe |
| « Une table temporaire est gratuite » | elle occupe du stockage facturé tant que la session dure |
| « 90 jours de Time Travel sur tous les comptes » | 1 jour au maximum en édition Standard ; 90 jours à partir d'Enterprise, et seulement pour les objets permanents |
| « On peut passer une table de transitoire à permanente avec `ALTER TABLE` » | le type ne se change pas : il faut recréer la table |
| « Un clone double le stockage » | il ne coûte rien à la création ; seules les modifications ultérieures sont stockées en plus |
| « Supprimer la table d'origine casse le clone » | le clone est indépendant |
| « `UNDROP` écrase la table qui porte le même nom » | il échoue : il faut renommer la table existante d'abord |
| « Il faut définir les partitions d'une table » | les micro-partitions sont automatiques ; on ne règle que, parfois, une clé de clustering |
| « Une vue matérialisée accepte les jointures » | une seule table ; pour des jointures tenues à jour, table dynamique |
| « Une vue sécurisée est plus rapide » | elle peut être plus lente : c'est le prix de la confidentialité |
| « Une table externe se met à jour avec `INSERT` » | elle est en lecture seule ; les données se modifient dans le stockage cloud |
| « `AT` et `BEFORE` sont équivalents » | `AT` inclut les changements de l'instant indiqué, `BEFORE` s'arrête juste avant |

---

## 9. À retenir pour la certification

- Micro-partitions : automatiques, de 50 à 500 Mo avant compression, en colonnes, **immuables**.
- Métadonnées par micro-partition : plage de valeurs de chaque colonne, nombre de valeurs distinctes. Elles permettent l'élagage (*pruning*).
- Clé de clustering : pour les très grandes tables ; le clustering automatique est un service *serverless* facturé en crédits.
- Table permanente : Time Travel de 0 à 1 jour (Standard) ou de 0 à 90 jours (Enterprise), Fail-safe de 7 jours.
- Tables transitoires et temporaires : Time Travel de 0 ou 1 jour, **pas de Fail-safe**.
- Table temporaire : liée à la session, invisible des autres sessions, prioritaire sur une table du même nom.
- Table externe : lecture seule, données hors de Snowflake. Table Iceberg : format ouvert, volume externe. Table dynamique : requête + `TARGET_LAG`, pas d'écriture directe.
- Vue matérialisée : édition Enterprise, une seule table, résultat stocké, maintenance automatique facturée.
- Vue sécurisée : définition cachée, optimisations limitées, adaptée au partage.
- Time Travel par défaut : 1 jour. Paramètre : `DATA_RETENTION_TIME_IN_DAYS`. Rétention de 0 = Time Travel désactivé.
- Trois repères : `TIMESTAMP`, `OFFSET` (secondes), `STATEMENT` (identifiant de requête), avec `AT` ou `BEFORE`.
- `UNDROP TABLE`, `UNDROP SCHEMA`, `UNDROP DATABASE` ; échec si le nom est déjà pris.
- Fail-safe : 7 jours, non réglable, tables permanentes, récupération par Snowflake uniquement, commence à la fin du Time Travel.
- Clonage : sans copie, instantané, indépendant, combinable avec le Time Travel ; le stockage n'augmente qu'avec les modifications.
- Le clone d'une table ne reprend ni les droits (sauf `COPY GRANTS`) ni l'historique de chargement.

---

## 10. Atelier pratique : casser et réparer (45 minutes)

Objectif : provoquer trois accidents et les réparer, puis lire ce que cela coûte en stockage. Jeu de données : `Data/finance/transactions.csv` (colonnes `transaction_id`, `account_id`, `transaction_date`, `amount`, `currency`, `transaction_type`, `category`, `merchant`, `location`, `is_fraudulent`, `risk_score`).

### Étape 1 — Préparer (10 minutes)

Chargez `Data/finance/transactions.csv` dans une table permanente `SALES_DB.RAW_DATA.TRANSACTIONS_RAW` avec le rôle `SALES_ENGINEER` (assistant de chargement du chapitre 7, ou `PUT` et `COPY INTO` du chapitre 11).

```sql
USE ROLE SALES_ENGINEER;
USE WAREHOUSE SALES_WH;
USE SCHEMA SALES_DB.RAW_DATA;

SELECT COUNT(*) FROM TRANSACTIONS_RAW;            -- notez ce nombre : c'est la référence
SHOW TABLES LIKE 'TRANSACTIONS_RAW';              -- colonnes kind et retention_time
```

### Étape 2 — Accident 1 : une mise à jour sans filtre (10 minutes)

```sql
UPDATE TRANSACTIONS_RAW SET amount = 0;           -- l'erreur
SET requete_fautive = LAST_QUERY_ID();

SELECT SUM(amount) FROM TRANSACTIONS_RAW;                                      -- 0
SELECT SUM(amount) FROM TRANSACTIONS_RAW BEFORE(STATEMENT => $requete_fautive); -- la vraie somme
```

Réparez sans supprimer la table : créez `TRANSACTIONS_OK` par clonage à l'instant précédant l'erreur, vérifiez-la, puis échangez les deux tables.

```sql
CREATE TABLE TRANSACTIONS_OK CLONE TRANSACTIONS_RAW BEFORE(STATEMENT => $requete_fautive);
ALTER TABLE TRANSACTIONS_OK SWAP WITH TRANSACTIONS_RAW;     -- échange les deux noms
DROP TABLE TRANSACTIONS_OK;                                 -- c'est maintenant la version abîmée
```

### Étape 3 — Accident 2 : une table supprimée, puis recréée (10 minutes)

```sql
DROP TABLE TRANSACTIONS_RAW;
CREATE TABLE TRANSACTIONS_RAW (transaction_id VARCHAR);     -- quelqu'un recrée une table vide du même nom
UNDROP TABLE TRANSACTIONS_RAW;                              -- que se passe-t-il ?
```

Trouvez la suite de commandes qui ramène la vraie table. Aide : `SHOW TABLES HISTORY LIKE 'TRANSACTIONS%';` et `ALTER TABLE ... RENAME TO ...`.

### Étape 4 — Comparer les types de tables (10 minutes)

```sql
CREATE TRANSIENT TABLE TRANSACTIONS_TR AS SELECT * FROM TRANSACTIONS_RAW;
CREATE TEMPORARY TABLE TRANSACTIONS_TMP AS SELECT * FROM TRANSACTIONS_RAW;
SHOW TABLES LIKE 'TRANSACTIONS%';                 -- comparez kind et retention_time

ALTER TABLE TRANSACTIONS_TR SET DATA_RETENTION_TIME_IN_DAYS = 30;   -- que répond Snowflake ?
```

Ouvrez une seconde feuille SQL (donc une autre session) et interrogez `TRANSACTIONS_TMP` : que constatez-vous ?

### Étape 5 — Lire le stockage et nettoyer (5 minutes)

```sql
SELECT table_name, is_transient, active_bytes, time_travel_bytes, failsafe_bytes, retained_for_clone_bytes
FROM SALES_DB.INFORMATION_SCHEMA.TABLE_STORAGE_METRICS
WHERE table_name LIKE 'TRANSACTIONS%';
-- les valeurs peuvent mettre un moment à refléter vos dernières opérations

DROP TABLE IF EXISTS TRANSACTIONS_TR;
DROP TABLE IF EXISTS TRANSACTIONS_TMP;
DROP TABLE IF EXISTS TRANSACTIONS_RAW;
```

### Questions de réflexion

1. À l'étape 2, pourquoi le clone n'a-t-il presque rien coûté en stockage ?
2. Si l'erreur de l'étape 2 avait été découverte au bout de trois jours sur un compte en édition Standard, que serait-il resté comme recours ?
3. Une table de 500 Go est entièrement réécrite chaque nuit par un outil de transformation. Quel type de table proposez-vous, et que perd-on en échange ?
4. Votre équipe veut un environnement de test identique à la production chaque lundi. Quelle commande, et que faut-il prévoir pour les droits ?
5. Un tableau de bord affiche un total par pays calculé sur une seule grande table qui change peu ; un autre croise trois tables et tolère dix minutes de retard. Quel objet pour chacun ?

## ✅ Points de vérification
- [ ] Je sais expliquer ce qu'est une micro-partition et pourquoi son immuabilité rend possibles le Time Travel et le clonage
- [ ] Je sais lire l'élagage dans le profil d'une requête
- [ ] Je connais le Time Travel et le Fail-safe de chaque type de table, par édition
- [ ] Je sais choisir entre vue standard, vue sécurisée, vue matérialisée et table dynamique
- [ ] J'ai réparé une modification erronée avec `BEFORE(STATEMENT => ...)`
- [ ] J'ai restauré une table avec `UNDROP`, y compris quand le nom était déjà repris
- [ ] J'ai créé un clone et je sais ce qu'il reprend et ne reprend pas de l'original
- [ ] Je sais lire `TABLE_STORAGE_METRICS`

## Documentation officielle
- [Micro-partitions et clustering des données](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions)
- [Clés de clustering et tables clusterisées](https://docs.snowflake.com/en/user-guide/tables-clustering-keys)
- [Tables temporaires et transitoires](https://docs.snowflake.com/en/user-guide/tables-temp-transient)
- [Tables externes](https://docs.snowflake.com/en/user-guide/tables-external-intro)
- [Tables Apache Iceberg](https://docs.snowflake.com/en/user-guide/tables-iceberg)
- [Tables dynamiques](https://docs.snowflake.com/en/user-guide/dynamic-tables-about)
- [Tables hybrides](https://docs.snowflake.com/en/user-guide/tables-hybrid)
- [Vue d'ensemble des vues](https://docs.snowflake.com/en/user-guide/views-introduction)
- [Vues matérialisées](https://docs.snowflake.com/en/user-guide/views-materialized)
- [Vues sécurisées](https://docs.snowflake.com/en/user-guide/views-secure)
- [Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel)
- [Fail-safe](https://docs.snowflake.com/en/user-guide/data-failsafe)
- [Clonage d'objets](https://docs.snowflake.com/en/user-guide/object-clone)
- [Coût du stockage](https://docs.snowflake.com/en/user-guide/cost-understanding-data-storage)

---

[← Retour au sommaire](README.md) | [← Précédent](12-architecture.md) | [Suivant →](14-ia-applications.md)
