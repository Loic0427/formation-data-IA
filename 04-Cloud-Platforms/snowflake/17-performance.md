# 17. Performance et optimisation : warehouses, caches, profil de requête, clustering

[← Retour au sommaire](README.md) | [← Précédent](16-snowpipe-export-connectivite.md) | [Suivant →](18-transformation.md)

## Vue d'ensemble

Dans Snowflake, il n'y a ni index à créer ni serveur à régler. Une requête lente se corrige avec un petit nombre de leviers, toujours les mêmes : la taille et le nombre de clusters du warehouse, les caches, l'organisation des données dans les micro-partitions, trois services d'optimisation payants, et la façon d'écrire la requête. Ce chapitre apprend à choisir le bon levier à partir d'un symptôme, et à savoir ce que chaque levier coûte.

Dans le métier, c'est une compétence quotidienne : un tableau de bord qui met 40 secondes à s'afficher, une facture qui double, des requêtes qui attendent leur tour le lundi matin. La réponse « on agrandit le warehouse » est parfois juste, souvent fausse, et toujours payante.

Ce chapitre couvre la première moitié du domaine 4 de l'examen SnowPro Core COF-C03, « Performance, requêtes et transformation » (21 % de l'examen) : évaluer la performance d'une requête, l'optimiser, utiliser les caches. La seconde moitié (transformation des données) est au [chapitre 18](18-transformation.md).

Exemple suivi : `SALES_DB`, `SALES_WH` et le rôle `SALES_ENGINEER` des chapitres précédents. Les tables du dossier `Data/` sont trop petites pour montrer un effet de performance (quelques dizaines de lignes) : pour les volumes, on utilise la base d'exemple `SNOWFLAKE_SAMPLE_DATA` fournie avec chaque compte.

| Fonction abordée | Édition minimale |
|---|---|
| Changer la taille d'un warehouse, caches, Query Profile, clés de clustering | Standard |
| Warehouse multi-cluster | Enterprise |
| Vues matérialisées | Enterprise |
| Service d'optimisation de la recherche | Enterprise |
| Query Acceleration Service | Enterprise |

---

## 1. Où part le temps d'une requête

```
requête envoyée
   │  1. compilation      (couche des services cloud : analyse, plan, élagage)
   │  2. file d'attente   (le warehouse est occupé, ou en cours de démarrage)
   │  3. exécution        (warehouse : lecture des micro-partitions, jointures, tris)
   ▼
résultat
```

Chaque étape a ses remèdes, et un remède appliqué à la mauvaise étape ne change rien :

| Le temps part dans | Symptôme | Levier |
|---|---|---|
| la file d'attente | beaucoup d'utilisateurs en même temps, requêtes simples mais lentes aux heures de pointe | plus de clusters (section 2), séparer les charges |
| la lecture des données | presque toutes les micro-partitions sont lues pour quelques lignes utiles | élagage : filtre, clé de clustering, optimisation de la recherche (sections 5 et 6) |
| le calcul en mémoire | débordement sur disque, tri ou jointure énorme | warehouse plus grand, requête réécrite (sections 2, 4 et 7) |
| rien du tout | la même requête est relancée à l'identique | cache de résultats (section 3) |

---

## 2. Dimensionner un warehouse

### 2.1 Rappel : taille et crédits

Un warehouse est un groupe de machines de calcul. Chaque taille double la puissance et le prix de la précédente : XS consomme 1 crédit par heure, S 2, M 4, L 8, XL 16, et ainsi de suite. La facturation est à la seconde, avec un minimum de 60 secondes à chaque démarrage.

Conséquence utile : si une requête lourde va deux fois plus vite sur un warehouse deux fois plus grand, elle coûte le même prix. Agrandir n'est rentable que si la requête accélère réellement.

### 2.2 Agrandir ou multiplier

Analogie : un restaurant. Si un plat est très long à préparer, il faut une cuisine plus grande (agrandir). Si les clients font la queue devant la porte alors que chaque plat est rapide, il faut ouvrir d'autres cuisines identiques (multiplier).

| | Agrandir (*scale up*) | Multiplier (*scale out*) |
|---|---|---|
| Geste | changer la taille : `WAREHOUSE_SIZE` | warehouse multi-cluster : `MIN_CLUSTER_COUNT`, `MAX_CLUSTER_COUNT` |
| Résout | une requête lourde et complexe, un débordement sur disque | la concurrence : beaucoup d'utilisateurs, requêtes en file d'attente |
| Ne résout pas | la file d'attente due au nombre d'utilisateurs (ou mal, et cher) | une requête isolée trop lente : elle ne s'exécute que sur un cluster |
| Édition | toutes | Enterprise ou supérieure |
| Automatique | non : c'est une commande manuelle | oui en mode auto-scale : les clusters démarrent et s'arrêtent selon la charge |
| Effet sur les requêtes en cours | aucun : seules les requêtes en attente et les nouvelles profitent de la nouvelle taille | aucun |

```sql
USE ROLE SYSADMIN;      -- modifier un warehouse demande le privilège MODIFY ou d'en être propriétaire

-- Agrandir pour un traitement lourd, puis revenir à la taille d'origine
ALTER WAREHOUSE SALES_WH SET WAREHOUSE_SIZE = 'MEDIUM';
-- ... traitement ...
ALTER WAREHOUSE SALES_WH SET WAREHOUSE_SIZE = 'XSMALL';

-- Multiplier (édition Enterprise) : de 1 à 3 clusters selon la charge
ALTER WAREHOUSE SALES_WH SET
  MIN_CLUSTER_COUNT = 1
  MAX_CLUSTER_COUNT = 3
  SCALING_POLICY = 'STANDARD';
```

Un warehouse multi-cluster a deux modes :

| Mode | Réglage | Comportement |
|---|---|---|
| Maximisé | minimum = maximum (supérieur à 1) | tous les clusters démarrent en même temps que le warehouse |
| Auto-scale | minimum différent du maximum | Snowflake démarre et arrête des clusters selon la charge |

Crédits consommés = crédits par heure de la taille × nombre de clusters en marche × durée.

### 2.3 Les politiques de mise à l'échelle

La politique ne s'applique qu'en mode auto-scale.

| Politique | Démarre un cluster | Arrête un cluster | Privilégie |
|---|---|---|---|
| `STANDARD` (défaut) | dès qu'une requête est mise en file d'attente, ou que Snowflake estime les clusters en marche insuffisants | après une période prolongée de faible charge | la rapidité : éviter la file d'attente |
| `ECONOMY` | seulement si la charge estimée suffit à occuper le nouveau cluster pendant au moins 6 minutes | quand il reste moins de 6 minutes de travail au cluster | l'économie de crédits, au prix de requêtes qui attendent |

### 2.4 Séparer les charges de travail

Bonne pratique citée dans le guide de l'examen : regrouper les charges semblables sur un même warehouse et séparer les charges différentes. Un warehouse pour le chargement, un pour les transformations, un pour les tableaux de bord.

- Les requêtes d'une même charge relisent les mêmes données : elles profitent du cache du warehouse (section 3).
- Chaque warehouse a la taille qui convient à sa charge.
- Un traitement lourd ne ralentit pas les tableaux de bord.
- Le coût se lit par équipe ou par usage.

---

## 3. Les trois caches

Snowflake garde trois choses en mémoire, à trois endroits différents.

```
Services cloud ──  cache de résultats    : le résultat complet d'une requête déjà exécutée
               └─  cache de métadonnées  : nombre de lignes, min et max de chaque colonne par micro-partition
Warehouse      ──  cache du warehouse    : les données de table déjà lues, gardées sur le disque local (SSD)
Stockage       ──  les micro-partitions  : lecture distante, la plus lente
```

| | Cache de résultats | Cache de métadonnées | Cache du warehouse |
|---|---|---|---|
| Autres noms | *query result cache*, résultats persistés | *metadata cache* | *warehouse cache*, cache de données local |
| Où | couche des services cloud | couche des services cloud | disques locaux du warehouse |
| Contenu | le résultat d'une requête | statistiques des tables et des micro-partitions | données de table lues par les requêtes précédentes |
| Warehouse nécessaire | non | non | oui, c'est lui qui le porte |
| Partagé entre utilisateurs | oui, si le rôle a les droits nécessaires | oui | oui, entre les requêtes du même warehouse |
| Durée de vie | 24 heures, prolongées à chaque réutilisation, 31 jours au maximum | tenu à jour en permanence | tant que le warehouse est en marche |
| Perdu quand | les données changent, ou le délai expire | jamais | le warehouse est suspendu ; sa taille est réduite |
| Exemple | relancer le même `SELECT` | `SELECT COUNT(*) FROM t`, `MIN(col)`, `MAX(col)` | deux requêtes différentes sur les mêmes colonnes |

### 3.1 Le cache de résultats

Snowflake conserve le résultat de chaque requête pendant 24 heures. Si la même requête revient et que rien n'a changé, il renvoie ce résultat sans exécuter quoi que ce soit : pas de warehouse, pas de crédit de calcul. Chaque réutilisation relance le délai de 24 heures, dans la limite de 31 jours après la première exécution.

Conditions de réutilisation (toutes nécessaires) :

- le texte de la nouvelle requête est identique à l'ancien : une majuscule ou un alias différent suffit à l'empêcher ;
- les données des tables n'ont pas changé, et leurs micro-partitions non plus (un reclustering les modifie) ;
- la requête ne contient pas de fonction dont le résultat ne peut pas être réutilisé, comme `RANDOM()`, `UUID_STRING()` ou `RANDSTR()`, ni de fonction externe (la documentation ne cite que ces trois fonctions en exemple ; pour les fonctions de date et d'heure comme `CURRENT_TIMESTAMP()`, elle ne se prononce pas : voir la page sur les résultats persistants) ;
- le rôle a les privilèges nécessaires sur toutes les tables de la requête ;
- les réglages qui influencent le résultat n'ont pas changé ;
- le résultat est encore disponible.

Le résultat peut être réutilisé par un autre utilisateur que celui qui a lancé la première requête. Même quand toutes les conditions sont réunies, la documentation ne garantit pas la réutilisation.

```sql
USE ROLE SALES_ENGINEER;
USE WAREHOUSE SALES_WH;

SELECT o_orderpriority, COUNT(*) AS nb, SUM(o_totalprice) AS total
FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF10.ORDERS
GROUP BY o_orderpriority;        -- première exécution : quelques secondes

-- Relancer exactement la même instruction : réponse en quelques millisecondes.
-- Dans le profil de la requête, un seul nœud : QUERY RESULT REUSE.

-- Désactiver le cache de résultats pour la session (utile pour mesurer une requête)
ALTER SESSION SET USE_CACHED_RESULT = FALSE;
```

`USE_CACHED_RESULT` vaut `TRUE` par défaut et se règle au niveau du compte, de l'utilisateur ou de la session.

### 3.2 Le cache de métadonnées

La couche des services cloud connaît en permanence, pour chaque table et chaque micro-partition : le nombre de lignes, la plage de valeurs (minimum et maximum) de chaque colonne, le nombre de valeurs distinctes. Certaines requêtes se contentent de ces statistiques et n'ont pas besoin de warehouse :

```sql
SELECT COUNT(*) FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF10.ORDERS;
SELECT MIN(o_orderdate), MAX(o_orderdate) FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF10.ORDERS;
```

Dans le profil de ces requêtes, on lit un nœud « METADATA-BASED RESULT » à la place d'une lecture de table. Ce sont aussi ces métadonnées qui permettent l'élagage (section 5) et qui répondent aux commandes `SHOW` et `DESCRIBE`.

### 3.3 Le cache du warehouse

Quand un warehouse lit des micro-partitions dans le stockage distant, il en garde une copie sur ses disques locaux. La requête suivante qui a besoin des mêmes données les lit localement, ce qui est beaucoup plus rapide. Contrairement au cache de résultats, la requête n'a pas besoin d'être identique : il suffit qu'elle lise les mêmes données.

Ce cache disparaît quand le warehouse est suspendu. D'où un arbitrage sur `AUTO_SUSPEND` :

| `AUTO_SUSPEND` | Avantage | Inconvénient |
|---|---|---|
| court (60 s) | peu de crédits consommés à vide | le cache est perdu à chaque pause : la première requête après reprise est plus lente |
| long (10 minutes et plus) | le cache reste chaud entre deux requêtes | on paie le temps d'inactivité |

Règle pratique : court pour le chargement et les traitements par lots (ils ne relisent pas les mêmes données), plus long pour les tableaux de bord (requêtes répétées sur les mêmes tables). La statistique « Percentage scanned from cache » du profil de requête mesure l'usage de ce cache.

---

## 4. Lire un profil de requête

### 4.1 Ouvrir le profil

Dans Snowsight : **Monitoring** puis **Query History**, cliquer sur une requête, onglet **Query Profile**. L'historique de l'interface couvre les 14 derniers jours. On y trouve :

- l'**arbre des opérateurs** : chaque boîte est une étape (lecture de table, filtre, jointure, agrégat, tri), avec la part du temps total qu'elle a consommée et le nombre de lignes sur chaque flèche. Il se lit de bas en haut ;
- les **nœuds les plus coûteux** (*Most Expensive Nodes*) : là où regarder en premier ;
- la **vue d'ensemble** : répartition du temps entre traitement (CPU), lecture sur disque local, lecture sur disque distant, réseau, initialisation ;
- les **statistiques** ;
- les **Query insights** : des messages produits automatiquement par Snowflake quand il détecte une condition qui nuit à la performance.

### 4.2 Les statistiques à savoir lire

| Statistique | Sens | Signal d'alerte |
|---|---|---|
| Partitions scanned / Partitions total | micro-partitions lues sur le total de la table | les deux nombres sont proches alors que la requête filtre : élagage inefficace |
| Bytes scanned | volume lu | |
| Percentage scanned from cache | part lue dans le cache du warehouse | 0 % sur une requête répétée : warehouse suspendu entre-temps |
| Bytes spilled to local storage | données écrites sur le disque local du warehouse faute de mémoire | ralentissement |
| Bytes spilled to remote storage | données écrites dans le stockage distant, le disque local étant plein lui aussi | ralentissement très important |

### 4.3 Les quatre problèmes classiques

**Débordement sur disque** (*spilling*). Une jointure, un tri ou un agrégat a besoin de plus de mémoire que le warehouse n'en a. Snowflake écrit alors les données intermédiaires sur le disque local, puis, s'il ne suffit pas, dans le stockage distant. La requête aboutit, mais lentement ; le débordement distant est le plus pénalisant. Remèdes, dans l'ordre : réduire le volume traité (filtrer plus tôt, sélectionner moins de colonnes, améliorer l'élagage), traiter les données en lots plus petits, utiliser un warehouse plus grand (plus de mémoire et de disque local). Multiplier les clusters ne sert à rien : la requête reste sur un seul cluster.

**Élagage inefficace**. La requête filtre, mais lit presque toutes les micro-partitions : les valeurs recherchées sont dispersées dans toute la table, ou le filtre empêche l'élagage (fonction appliquée à la colonne). Remèdes : filtrer sur la colonne brute, clé de clustering, optimisation de la recherche (sections 5 à 7).

**Jointure explosive** (*exploding join*). Un nœud de jointure sort beaucoup plus de lignes qu'il n'en reçoit : la condition de jointure est absente (produit cartésien) ou porte sur une colonne qui n'est pas unique. Remède : corriger la condition, dédoublonner ou agréger avant de joindre.

**`UNION` sans `ALL`**. `UNION` supprime les doublons, ce qui ajoute une étape d'agrégation coûteuse visible dans le profil. Si les doublons sont impossibles ou acceptables, `UNION ALL` l'évite.

### 4.4 La file d'attente

Une requête attend quand le warehouse est saturé (*queued overload*) ou en cours de démarrage (*queued provisioning*). Une attente régulière pour cause de surcharge est le signal d'un besoin de clusters supplémentaires, ou de charges à séparer. Deux paramètres encadrent l'attente et la durée :

| Paramètre | Rôle | Défaut |
|---|---|---|
| `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS` | annule une requête restée trop longtemps en file d'attente | 0 (pas de limite) |
| `STATEMENT_TIMEOUT_IN_SECONDS` | annule une requête qui s'exécute trop longtemps | 172 800 secondes (2 jours) |

---

## 5. Micro-partitions et clés de clustering

### 5.1 Rappel : micro-partitions et élagage

Snowflake découpe automatiquement chaque table en micro-partitions : des fichiers en colonnes, compressés, non modifiables, qui contiennent chacun entre 50 et 500 Mo de données avant compression. Pour chaque micro-partition, il connaît le minimum et le maximum de chaque colonne.

L'**élagage** (*pruning*) consiste à ne pas ouvrir les micro-partitions qui ne peuvent pas contenir les lignes cherchées :

```
Filtre : WHERE order_date = '2024-03-15'

Table bien rangée par date                 Table mal rangée
P1  [01-01 → 01-31]  ignorée               P1  [01-02 → 12-28]  lue
P2  [02-01 → 02-29]  ignorée               P2  [01-01 → 12-30]  lue
P3  [03-01 → 03-31]  LUE                   P3  [01-05 → 12-31]  lue
P4  [04-01 → 04-30]  ignorée               P4  [01-03 → 12-29]  lue
→ 1 partition lue sur 4                    → 4 partitions lues sur 4
```

Les données sont rangées dans l'ordre où elles arrivent. Une table chargée jour après jour est donc naturellement bien rangée par date, sans rien faire. Le rangement se dégrade avec les mises à jour, les suppressions et les chargements dans le désordre.

### 5.2 Mesurer : profondeur de clustering

Deux micro-partitions se **chevauchent** quand leurs plages de valeurs se recoupent pour une colonne. La **profondeur de clustering** (*clustering depth*) est le nombre moyen de micro-partitions qui se chevauchent pour une valeur donnée : plus elle est petite, mieux la table est rangée. Elle vaut au minimum 1 pour une table qui contient des données, et 0 pour une table vide.

```sql
SELECT SYSTEM$CLUSTERING_DEPTH('SALES_DB.ANALYTICS.ORDERS_PERF', '(o_orderdate)');
SELECT SYSTEM$CLUSTERING_INFORMATION('SALES_DB.ANALYTICS.ORDERS_PERF', '(o_orderdate)');
```

La seconde fonction renvoie un document JSON : nombre total de micro-partitions, chevauchement moyen (`average_overlaps`), profondeur moyenne (`average_depth`) et un histogramme des profondeurs. Les deux fonctions acceptent n'importe quelle liste de colonnes, même si la table n'a pas de clé de clustering : on peut donc mesurer avant de décider.

### 5.3 Quand définir une clé de clustering

Une **clé de clustering** est une ou plusieurs colonnes (ou expressions) selon lesquelles on demande à Snowflake de maintenir la table rangée. Ce n'est pas un index. La plupart des tables n'en ont pas besoin. La documentation la réserve aux tables qui réunissent ces conditions :

- la table est très volumineuse : plusieurs téraoctets, donc un très grand nombre de micro-partitions ;
- les requêtes se sont dégradées avec le temps, ou la profondeur de clustering est élevée ;
- les requêtes sont sélectives (elles lisent une petite part des lignes) ou trient sur les mêmes colonnes, et la plupart d'entre elles profiteraient de la même clé ;
- la table est beaucoup lue et peu modifiée.

Choix des colonnes :

- d'abord celles des filtres les plus fréquents (souvent une date), puis celles des jointures ;
- 3 ou 4 colonnes au maximum ;
- éviter une cardinalité très faible (un booléen ne sépare rien) ou très forte (un identifiant unique, un horodatage à la milliseconde) ; pour une colonne trop fine, utiliser une expression, par exemple `TO_DATE(event_ts)` ;
- avec plusieurs colonnes, les ordonner de la cardinalité la plus faible à la plus forte ;
- une colonne `VARIANT` ne peut pas servir directement de clé, mais une expression sur un chemin de cette colonne le peut.

### 5.4 Définir, modifier, supprimer

```sql
-- À la création
CREATE TABLE SALES_DB.ANALYTICS.ORDERS_CLUSTERED (
  order_id NUMBER, order_date DATE, ship_country VARCHAR, total_amount FLOAT
) CLUSTER BY (order_date);

-- Sur une table existante
ALTER TABLE SALES_DB.ANALYTICS.ORDERS_PERF CLUSTER BY (o_orderdate);

-- Mettre en pause ou reprendre le reclustering automatique
ALTER TABLE SALES_DB.ANALYTICS.ORDERS_PERF SUSPEND RECLUSTER;
ALTER TABLE SALES_DB.ANALYTICS.ORDERS_PERF RESUME RECLUSTER;

-- Supprimer la clé
ALTER TABLE SALES_DB.ANALYTICS.ORDERS_PERF DROP CLUSTERING KEY;
```

### 5.5 Ce que coûte le reclustering automatique

Dès qu'une table a une clé, le service **Automatic Clustering** la réorganise en arrière-plan, sans warehouse de l'utilisateur et sans bloquer les écritures. Le coût est double :

- du **calcul serverless**, facturé par Snowflake en dehors de vos warehouses ; il augmente avec la fréquence des modifications de la table ;
- du **stockage** : une micro-partition ne se modifie pas, le reclustering en écrit donc de nouvelles, et les anciennes sont conservées le temps du Time Travel et du Fail-safe.

`SYSTEM$ESTIMATE_AUTOMATIC_CLUSTERING_COSTS` donne une estimation avant de se lancer ; la vue `SNOWFLAKE.ACCOUNT_USAGE.AUTOMATIC_CLUSTERING_HISTORY` donne la consommation réelle. Une table très souvent modifiée avec une clé de clustering peut coûter plus cher en maintenance qu'elle ne fait gagner en lecture.

---

## 6. Trois services d'optimisation (édition Enterprise)

### 6.1 Service d'optimisation de la recherche

Analogie : l'index à la fin d'un livre. Pour retrouver une ligne précise dans une table immense (un client par son adresse électronique, une commande par son numéro), le clustering ne suffit pas : on ne peut ranger une table que selon une clé. Le *search optimization service* construit une structure annexe, le **chemin d'accès de recherche** (*search access path*), qui indique dans quelles micro-partitions chaque valeur peut se trouver.

Il accélère les recherches ponctuelles très sélectives : égalité et `IN`, recherche de sous-chaîne et expressions régulières (`LIKE`, `ILIKE`, `RLIKE`), champs d'une colonne `VARIANT`, fonctions géospatiales.

```sql
-- Sur toute la table, ou seulement sur les colonnes utiles (moins coûteux)
ALTER TABLE SALES_DB.ANALYTICS.ORDERS_PERF ADD SEARCH OPTIMIZATION ON EQUALITY(o_orderkey);

SHOW TABLES LIKE 'ORDERS_PERF' IN SCHEMA SALES_DB.ANALYTICS;   -- colonne search_optimization_progress

ALTER TABLE SALES_DB.ANALYTICS.ORDERS_PERF DROP SEARCH OPTIMIZATION;
```

Les requêtes ne sont accélérées qu'une fois le chemin d'accès entièrement construit. Coût : du stockage pour la structure et du calcul serverless pour la construire puis la tenir à jour. `SYSTEM$ESTIMATE_SEARCH_OPTIMIZATION_COSTS` en donne une estimation.

### 6.2 Vues matérialisées

Une vue ordinaire est une requête enregistrée : elle est recalculée à chaque lecture. Une **vue matérialisée** stocke son résultat, et Snowflake le tient à jour en arrière-plan quand la table de base change.

```sql
CREATE MATERIALIZED VIEW SALES_DB.ANALYTICS.MV_CA_PAR_JOUR AS
SELECT o_orderdate, COUNT(*) AS nb_commandes, SUM(o_totalprice) AS chiffre_affaires
FROM SALES_DB.ANALYTICS.ORDERS_PERF
GROUP BY o_orderdate;
```

Ce qu'il faut savoir :

- les données lues sont **toujours à jour** : si la maintenance n'a pas encore rattrapé une modification, Snowflake complète avec la table de base ;
- l'optimiseur peut **réécrire automatiquement** une requête sur la table de base pour utiliser la vue matérialisée, sans que l'utilisateur la nomme ;
- la maintenance est automatique et facturée en calcul serverless, à quoi s'ajoute le stockage du résultat ;
- une vue matérialisée peut avoir sa propre clé de clustering, différente de celle de la table, et peut être sécurisée (`SECURE`).

Limites, souvent demandées à l'examen :

| Interdit dans une vue matérialisée | |
|---|---|
| plusieurs tables | une seule table ; aucune jointure, pas même une auto-jointure |
| interroger une vue, une autre vue matérialisée | uniquement une table |
| fonctions de fenêtrage, fonctions définies par l'utilisateur | |
| `HAVING`, `ORDER BY`, `LIMIT` | |
| fonctions non déterministes | `CURRENT_TIMESTAMP()`, par exemple |
| certains agrégats | seuls quelques-uns sont admis (`SUM`, `COUNT`, `MIN`, `MAX`, `AVG`, `APPROX_COUNT_DISTINCT`...) ; pas de `COUNT(DISTINCT ...)` |

Bon usage : un agrégat coûteux, lu très souvent, sur une table qui change peu.

### 6.3 Query Acceleration Service

Certaines requêtes lisent un volume énorme pour n'en garder qu'une petite partie. Le *query acceleration service* confie une part de ce travail de lecture et de filtrage à des ressources de calcul partagées, fournies par Snowflake en renfort du warehouse. Il sert surtout aux warehouses dont quelques requêtes sont beaucoup plus lourdes que les autres : on évite d'agrandir le warehouse pour elles seules.

```sql
ALTER WAREHOUSE SALES_WH SET
  ENABLE_QUERY_ACCELERATION = TRUE
  QUERY_ACCELERATION_MAX_SCALE_FACTOR = 8;

-- Une requête passée aurait-elle été accélérée ?
SELECT PARSE_JSON(SYSTEM$ESTIMATE_QUERY_ACCELERATION('<identifiant de requête>'));
```

- Requêtes éligibles : grandes lectures avec filtres sélectifs ou agrégats ; insertions et copies de gros volumes.
- Non éligibles : trop peu de micro-partitions à lire, filtre peu sélectif, certaines requêtes avec `LIMIT`, fonctions non déterministes.
- `QUERY_ACCELERATION_MAX_SCALE_FACTOR` plafonne le renfort à un multiple de la taille du warehouse : 8 par défaut, de 0 à 100, 0 signifiant sans plafond.
- Facturation serverless, à la seconde, seulement quand le service est utilisé.
- La vue `SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE` liste les requêtes et les warehouses qui en profiteraient.

### 6.4 Choisir entre les quatre leviers

| | Clé de clustering | Optimisation de la recherche | Vue matérialisée | Query Acceleration |
|---|---|---|---|---|
| Idée | ranger la table | un index de recherche | un résultat précalculé | du renfort de calcul |
| Requêtes visées | filtres sur une plage (dates), tris | recherche d'une valeur précise, sous-chaîne | même agrégat répété | grandes lectures très filtrées, requêtes hors norme |
| S'applique à | une table | une table, des colonnes | une requête sur une seule table | un warehouse |
| Coût de stockage | oui (anciennes micro-partitions) | oui (chemin d'accès) | oui (résultat) | non |
| Coût de calcul | serverless, à chaque réorganisation | serverless, à chaque modification | serverless, à chaque modification | serverless, à l'usage |
| Édition | Standard | Enterprise | Enterprise | Enterprise |
| Nombre par table | une seule clé | plusieurs colonnes | plusieurs vues | sans objet |

Ces leviers se combinent. Les trois premiers ont un coût de maintenance proportionnel aux modifications de la table : ils conviennent aux tables beaucoup lues et peu modifiées.

---

## 7. Écrire des requêtes efficaces

| Pratique | Pourquoi |
|---|---|
| Nommer les colonnes au lieu de `SELECT *` | le stockage est en colonnes : une colonne non demandée n'est pas lue |
| Filtrer le plus tôt possible, sur la colonne brute | `WHERE order_date >= '2024-01-01'` permet l'élagage ; `WHERE YEAR(order_date) = 2024` peut l'empêcher |
| `UNION ALL` plutôt que `UNION` quand les doublons sont impossibles | évite un dédoublonnage |
| Vérifier l'unicité des clés de jointure | évite la jointure explosive |
| `ORDER BY` seulement au dernier niveau, si nécessaire | le tri d'un grand volume demande beaucoup de mémoire |
| `LIMIT` ou `SAMPLE` pour explorer | inutile de tout lire pour regarder dix lignes |
| `APPROX_COUNT_DISTINCT` quand une estimation suffit | bien moins de mémoire que `COUNT(DISTINCT ...)` (chapitre 18) |
| `QUALIFY` pour filtrer sur une fonction de fenêtrage | évite une sous-requête (chapitre 18) |
| Garder le même texte pour une requête répétée | condition du cache de résultats |
| `EXPLAIN` avant une requête lourde | affiche le plan et les partitions prévues sans exécuter la requête |

---

## 8. Suivre la performance

### 8.1 Historique des requêtes

| Source | Portée | Délai | Historique |
|---|---|---|---|
| Snowsight, **Query History** | interface graphique, accès au profil | immédiat | 14 jours |
| `INFORMATION_SCHEMA.QUERY_HISTORY()` (fonction de table) | requêtes visibles par le rôle | immédiat | 7 jours |
| `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY` (vue) | tout le compte | jusqu'à 45 minutes | 365 jours |

```sql
-- Mes requêtes les plus lentes de la dernière heure (sans délai)
SELECT query_id, LEFT(query_text, 60) AS debut, total_elapsed_time / 1000 AS secondes,
       bytes_scanned, warehouse_size
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(
  END_TIME_RANGE_START => DATEADD(HOUR, -1, CURRENT_TIMESTAMP()), RESULT_LIMIT => 1000))
ORDER BY total_elapsed_time DESC
LIMIT 10;

-- Sur tout le compte : requêtes des 7 derniers jours qui ont débordé sur le stockage distant
SELECT query_id, user_name, warehouse_name, warehouse_size,
       partitions_scanned, partitions_total,
       bytes_spilled_to_local_storage, bytes_spilled_to_remote_storage,
       queued_overload_time, total_elapsed_time
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE start_time >= DATEADD(DAY, -7, CURRENT_TIMESTAMP())
  AND bytes_spilled_to_remote_storage > 0
ORDER BY bytes_spilled_to_remote_storage DESC;
```

La seconde requête demande un rôle qui a accès à la base `SNOWFLAKE` (par défaut `ACCOUNTADMIN`). Les durées sont en millisecondes.

Pour le coût : la vue `ACCOUNT_USAGE.QUERY_ATTRIBUTION_HISTORY` attribue à chaque requête les crédits de calcul qu'elle a consommés (colonne `credits_attributed_compute`), hors temps d'inactivité du warehouse ; les requêtes très courtes (environ 100 ms ou moins) n'y figurent pas, et le délai peut atteindre huit heures. Avec le paramètre de session `QUERY_TAG`, on étiquette les requêtes d'un outil ou d'une équipe pour regrouper ces coûts.

### 8.2 Charge du warehouse

```sql
SELECT start_time, avg_running, avg_queued_load, avg_queued_provisioning, avg_blocked
FROM TABLE(INFORMATION_SCHEMA.WAREHOUSE_LOAD_HISTORY(
  DATE_RANGE_START => DATEADD(HOUR, -8, CURRENT_TIMESTAMP()),
  WAREHOUSE_NAME => 'SALES_WH'));
```

| Colonne | Sens | Lecture |
|---|---|---|
| `AVG_RUNNING` | nombre moyen de requêtes en cours d'exécution | faible en permanence : warehouse trop grand ou peu utilisé |
| `AVG_QUEUED_LOAD` | nombre moyen de requêtes en attente parce que le warehouse est saturé | régulièrement supérieur à 0 : multiplier les clusters ou séparer les charges |
| `AVG_QUEUED_PROVISIONING` | en attente du démarrage du warehouse | reprises fréquentes après suspension |
| `AVG_BLOCKED` | bloquées par un verrou de transaction | transactions concurrentes sur la même table (chapitre 18) |

La fonction couvre les 14 derniers jours et demande le privilège `MONITOR` sur le warehouse. Le même graphique existe dans Snowsight, sur la page du warehouse.

---

## 9. Maîtriser le coût de calcul

| Levier | Geste |
|---|---|
| Ne pas payer à vide | `AUTO_SUSPEND` adapté aux pauses de la charge, `AUTO_RESUME = TRUE` |
| Bonne taille | partir petit (XS), agrandir seulement si la requête accélère en proportion |
| Bon nombre de clusters | minimum à 1 en auto-scale ; politique `ECONOMY` si l'attente est acceptable |
| Profiter des caches | même texte pour les requêtes répétées ; warehouse dédié aux tableaux de bord |
| Limiter les dérapages | `STATEMENT_TIMEOUT_IN_SECONDS` sur le warehouse ; moniteurs de ressources (chapitre 9) |
| Surveiller les services serverless | clustering automatique, optimisation de la recherche, vues matérialisées, accélération : chacun a sa vue d'historique dans `ACCOUNT_USAGE` |
| Attribuer les coûts | un warehouse par usage, `QUERY_TAG`, `QUERY_ATTRIBUTION_HISTORY` |

Rappel du chapitre 12 : les services cloud ne sont facturés que pour la part qui dépasse 10 % de la consommation quotidienne des warehouses. Une requête servie par le cache de résultats ou par les métadonnées n'utilise pas de warehouse.

---

## 10. Pièges fréquents

1. **Agrandir le warehouse pour un problème de concurrence.** La file d'attente due au nombre d'utilisateurs se traite en multipliant les clusters, pas en changeant la taille.
2. **Multiplier les clusters pour une requête lente.** Une requête s'exécute sur un seul cluster : elle ne va pas plus vite.
3. **Croire que le changement de taille accélère la requête en cours.** Il ne profite qu'aux requêtes en attente et aux suivantes.
4. **Confondre cache de résultats et cache du warehouse.** Le premier survit à la suspension du warehouse et n'en a pas besoin ; le second disparaît à la suspension.
5. **Mesurer une optimisation avec le cache de résultats actif.** La seconde exécution est instantanée quelle que soit l'optimisation : désactiver `USE_CACHED_RESULT` le temps de la mesure.
6. **Poser une clé de clustering sur une petite table**, ou sur une table modifiée en permanence : coût de maintenance sans gain.
7. **Choisir un identifiant unique comme clé de clustering.** Cardinalité trop forte : rangement coûteux et peu utile pour les filtres par plage. Pour retrouver une valeur précise, c'est l'optimisation de la recherche qui convient.
8. **Vouloir une jointure dans une vue matérialisée.** Impossible : une seule table. Pour une jointure tenue à jour, voir les tables dynamiques au chapitre 18.
9. **Appliquer une fonction à la colonne filtrée** et s'étonner que toutes les partitions soient lues.
10. **Interroger `ACCOUNT_USAGE` pour une requête lancée il y a deux minutes.** La vue a jusqu'à 45 minutes de retard : utiliser `INFORMATION_SCHEMA` ou Snowsight.

---

## 11. À retenir pour la certification

- Agrandir (*scale up*) : requêtes lourdes, débordement sur disque. Multiplier (*scale out*) : concurrence, file d'attente. Le multi-cluster demande l'édition Enterprise.
- Mode maximisé : minimum = maximum. Mode auto-scale : politiques `STANDARD` (défaut, démarre un cluster dès qu'une requête attend) et `ECONOMY` (démarre un cluster seulement pour au moins 6 minutes de charge).
- Le changement de taille n'affecte pas les requêtes en cours d'exécution.
- Cache de résultats : 24 heures, prolongé à chaque réutilisation, 31 jours au maximum ; sans warehouse ; requête identique, données inchangées, privilèges suffisants ; paramètre `USE_CACHED_RESULT`.
- Cache de métadonnées : `COUNT(*)`, `MIN`, `MAX` sans warehouse. Cache du warehouse : données sur disque local, perdu à la suspension.
- Query Profile : « Bytes spilled to local / remote storage » (mémoire insuffisante, le distant est le pire), « Partitions scanned / total » (élagage), jointure explosive (plus de lignes en sortie qu'en entrée), file d'attente.
- Micro-partitions : 50 à 500 Mo avant compression, en colonnes, non modifiables, créées automatiquement.
- Clé de clustering : tables de plusieurs téraoctets, 3 ou 4 colonnes au maximum, de la cardinalité la plus faible à la plus forte ; profondeur de clustering plus petite = meilleur rangement ; `SYSTEM$CLUSTERING_INFORMATION` et `SYSTEM$CLUSTERING_DEPTH`.
- Automatic Clustering : serverless, ne bloque pas les écritures, se suspend avec `ALTER TABLE ... SUSPEND RECLUSTER`.
- Optimisation de la recherche : recherches ponctuelles (égalité, `IN`, sous-chaîne), chemin d'accès de recherche, stockage plus calcul serverless, Enterprise.
- Vue matérialisée : Enterprise, une seule table, pas de jointure, pas de fenêtrage, pas de fonction définie par l'utilisateur, toujours à jour, maintenance serverless, réécriture automatique par l'optimiseur.
- Query Acceleration Service : Enterprise, s'active sur le warehouse, facteur d'échelle 8 par défaut (0 = sans plafond), `SYSTEM$ESTIMATE_QUERY_ACCELERATION`.
- `ACCOUNT_USAGE.QUERY_HISTORY` : jusqu'à 45 minutes de délai, 365 jours. `INFORMATION_SCHEMA.QUERY_HISTORY()` : sans délai, 7 jours. Snowsight : 14 jours.

---

## 12. Atelier pratique (30 à 45 minutes)

Objectif : observer les trois caches, lire un profil de requête et mesurer l'effet du rangement des données sur l'élagage. Tout l'atelier fonctionne sur un compte d'essai en édition Standard, avec un warehouse XS. Les étapes qui demandent l'édition Enterprise sont regroupées à la fin et signalées.

### Étape 0 : préparation (5 minutes)

```sql
-- Une seule fois, avec ACCOUNTADMIN : accès à la base d'exemple et droits du rôle
USE ROLE ACCOUNTADMIN;
GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE_SAMPLE_DATA TO ROLE SALES_ENGINEER;
GRANT MONITOR ON WAREHOUSE SALES_WH TO ROLE SALES_ENGINEER;

USE ROLE SALES_ENGINEER;
USE WAREHOUSE SALES_WH;
USE SCHEMA SALES_DB.ANALYTICS;
```

Si la base `SNOWFLAKE_SAMPLE_DATA` n'apparaît pas dans votre compte, la documentation « Sample data » (lien en fin de chapitre) indique comment la créer à partir du partage fourni par Snowflake.

### Étape 1 : les trois caches (10 minutes)

1. Exécuter `SELECT COUNT(*) FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF10.ORDERS;` puis ouvrir son profil. Quel nœud apparaît ? Le warehouse a-t-il lu des données ?
2. Exécuter la requête d'agrégat de la section 3.1, noter sa durée, puis la relancer à l'identique. Comparer les durées et les profils.
3. Relancer la même requête en changeant seulement la casse d'un mot-clé (`select` au lieu de `SELECT`). Le cache de résultats est-il utilisé ?
4. Exécuter `ALTER SESSION SET USE_CACHED_RESULT = FALSE;`, puis une requête différente sur les mêmes colonnes (par exemple un `GROUP BY o_orderstatus`). Dans le profil, relever « Percentage scanned from cache ».
5. Suspendre le warehouse (`ALTER WAREHOUSE SALES_WH SUSPEND;`, avec un rôle qui a `OPERATE`), relancer la requête du point 4 et relever de nouveau la statistique.

### Étape 2 : élagage et rangement des données (15 minutes)

```sql
-- Deux copies de la même table (15 millions de lignes) : l'une dans le désordre, l'autre triée par date
CREATE OR REPLACE TABLE ORDERS_PERF AS
SELECT * FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF10.ORDERS ORDER BY RANDOM();

CREATE OR REPLACE TABLE ORDERS_PERF_SORTED AS
SELECT * FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF10.ORDERS ORDER BY o_orderdate;
```

1. Mesurer le rangement des deux tables avec `SYSTEM$CLUSTERING_INFORMATION('<table>', '(o_orderdate)')`. Relever `total_partition_count`, `average_overlaps` et `average_depth`.
2. Exécuter la même requête sur les deux tables et comparer, dans le profil, « Partitions scanned » et « Partitions total » :

```sql
SELECT COUNT(*), SUM(o_totalprice) FROM ORDERS_PERF
WHERE o_orderdate BETWEEN '1995-03-01' AND '1995-03-31';
```

3. Sur `ORDERS_PERF_SORTED`, remplacer le filtre par `WHERE TO_CHAR(o_orderdate, 'YYYY-MM') = '1995-03'`. Combien de partitions sont lues ? Comparer avec le point 2.
4. Dans le profil de la création de `ORDERS_PERF_SORTED`, chercher le nœud de tri et la statistique « Bytes spilled to local storage ». Si elle est présente, quel levier l'aurait évitée ?

### Étape 3 : provoquer et lire une jointure explosive (5 minutes)

```sql
SELECT COUNT(*)
FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS o
JOIN SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER c ON o.o_orderstatus <> c.c_mktsegment
WHERE o.o_orderkey < 2000 AND c.c_custkey < 2000;
```

Ouvrir le profil : comparer le nombre de lignes qui entrent dans le nœud de jointure et le nombre qui en sort. Corriger la condition de jointure (`o.o_custkey = c.c_custkey`) et comparer.

### Étape 4 : suivi (5 minutes)

1. Avec `INFORMATION_SCHEMA.QUERY_HISTORY()`, lister vos cinq requêtes les plus longues de l'atelier.
2. Avec `WAREHOUSE_LOAD_HISTORY`, afficher la charge de `SALES_WH` sur la dernière heure. `AVG_QUEUED_LOAD` est-il différent de 0 ?

### Pour aller plus loin (édition Enterprise uniquement)

- Créer la vue matérialisée de la section 6.2 sur `ORDERS_PERF`, puis exécuter la requête d'agrégat directement sur la table : le profil montre-t-il la vue matérialisée ?
- Ajouter l'optimisation de la recherche sur `o_orderkey` et comparer les partitions lues par `WHERE o_orderkey = 1234567` avant et après la fin de la construction.

### Nettoyage

```sql
DROP TABLE IF EXISTS ORDERS_PERF;
DROP TABLE IF EXISTS ORDERS_PERF_SORTED;
ALTER SESSION UNSET USE_CACHED_RESULT;
```

### Questions de réflexion

1. Pourquoi le `COUNT(*)` de l'étape 1 ne consomme-t-il aucun crédit de warehouse ?
2. À l'étape 2, les deux tables contiennent exactement les mêmes lignes. Pourquoi l'une se lit-elle beaucoup plus vite que l'autre ?
3. La table `ORDERS_PERF_SORTED` est bien rangée sans clé de clustering. Dans quelle situation faudrait-il en définir une, et que coûterait-elle ?
4. Un tableau de bord relance les mêmes vingt requêtes toutes les cinq minutes sur des données chargées une fois par nuit. Quels caches travaillent, et quel réglage d'`AUTO_SUSPEND` proposez-vous ?
5. Le lundi à 9 heures, deux cents utilisateurs ouvrent leurs rapports et les requêtes attendent. Que proposez-vous en édition Standard ? En édition Enterprise ?

## Points de vérification
- [ ] Je sais dire, devant un symptôme, s'il faut agrandir le warehouse ou multiplier les clusters
- [ ] Je sais citer les trois caches, où ils se trouvent et ce qui les invalide
- [ ] J'ai vu un nœud « QUERY RESULT REUSE » et un résultat fondé sur les métadonnées dans un profil
- [ ] Je sais lire « Partitions scanned / total » et les deux statistiques de débordement
- [ ] J'ai mesuré la profondeur de clustering de deux tables avec `SYSTEM$CLUSTERING_INFORMATION`
- [ ] Je sais citer trois limites des vues matérialisées et l'édition qu'elles demandent
- [ ] Je sais quelle source d'historique utiliser selon le délai et la période voulus
- [ ] Les tables de l'atelier sont supprimées

## Documentation officielle
- [Certifications Snowflake : guide de l'examen SnowPro Core](https://learn.snowflake.com/en/certifications/)
- [Considérations sur les warehouses](https://docs.snowflake.com/en/user-guide/warehouses-considerations)
- [Warehouses multi-cluster](https://docs.snowflake.com/en/user-guide/warehouses-multicluster)
- [Réutilisation des résultats de requête](https://docs.snowflake.com/en/user-guide/querying-persisted-results)
- [Historique et profil de requête dans Snowsight](https://docs.snowflake.com/en/user-guide/ui-snowsight-activity)
- [Micro-partitions et clustering des données](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions)
- [Clés de clustering](https://docs.snowflake.com/en/user-guide/tables-clustering-keys)
- [Automatic Clustering](https://docs.snowflake.com/en/user-guide/tables-auto-reclustering)
- [Service d'optimisation de la recherche](https://docs.snowflake.com/en/user-guide/search-optimization-service)
- [Vues matérialisées](https://docs.snowflake.com/en/user-guide/views-materialized)
- [Query Acceleration Service](https://docs.snowflake.com/en/user-guide/query-acceleration-service)
- [Vue QUERY_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/query_history)
- [WAREHOUSE_LOAD_HISTORY](https://docs.snowflake.com/en/sql-reference/functions/warehouse_load_history)
- [Débordement mémoire : requêtes trop grandes pour la mémoire](https://docs.snowflake.com/en/user-guide/performance-query-warehouse-memory)
- [Données d'exemple](https://docs.snowflake.com/en/user-guide/sample-data)

---

[← Retour au sommaire](README.md) | [← Précédent](16-snowpipe-export-connectivite.md) | [Suivant →](18-transformation.md)
