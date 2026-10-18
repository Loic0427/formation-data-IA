# 19. Collaboration autour des données : partage, annonces, réplication

[← Retour au sommaire](README.md) | [← Précédent](18-transformation.md) | [Plan de préparation à la certification →](certification/PLAN.md)

## Vue d'ensemble

Jusqu'ici, toutes les données restaient dans un seul compte Snowflake. Ce chapitre traite de ce qui se passe **entre** comptes : donner un accès en lecture à un partenaire sans lui envoyer de fichier, publier un jeu de données sur une place de marché, recopier une base dans une autre région pour survivre à une panne. C'est le domaine 5 de l'examen SnowPro Core, « Data Collaboration », qui pèse 10 % des questions.

Trois mécanismes reviennent sans cesse, et l'examen vérifie surtout que vous ne les confondez pas :

| Mécanisme | En une phrase | Les données sont-elles copiées ? |
|---|---|---|
| Partage (Secure Data Sharing) | donner un accès en lecture seule à un autre compte | non |
| Réplication | recopier des objets dans un autre compte de la même organisation, et les tenir à jour | oui |
| Clonage | créer, dans le même compte, une copie indépendante qui ne coûte rien au départ | non au départ |

Exemple suivi : la base `SALES_DB` des chapitres précédents, le warehouse `SALES_WH`, les rôles `SALES_ENGINEER` et `SALES_ANALYST`. L'entreprise veut ouvrir ses ventes quotidiennes à un distributeur partenaire.

Trois objets seront créés : la table `ANALYTICS.DAILY_SALES` (ventes par jour et par pays), la vue sécurisée `ANALYTICS.DAILY_SALES_PARTNER_V` (ce que le partenaire voit réellement) et le partage `SALES_SHARE`.

---

## 1. Le partage sécurisé de données (Secure Data Sharing)

### 1.1 L'idée : on partage un accès, pas des données

Dans un système classique, partager des données signifie exporter un fichier, l'envoyer, puis le recharger ailleurs : il existe alors deux copies, qui divergent dès le lendemain.

Dans Snowflake, le stockage est séparé du calcul ([chapitre 12](12-architecture.md)). Un partage se contente donc d'autoriser un autre compte à **lire les mêmes fichiers**, à travers la couche de services et les métadonnées :

```
Compte FOURNISSEUR (provider)                Compte CONSOMMATEUR (consumer)
┌──────────────────────────────┐             ┌──────────────────────────────┐
│ SALES_DB.ANALYTICS           │             │ Base PARTNER_SALES           │
│   DAILY_SALES_PARTNER_V      │◄── SHARE ───│   (créée à partir du partage,│
│ stockage : payé ici          │             │    lecture seule)            │
│                              │             │ warehouse : payé ici         │
└──────────────────────────────┘             └──────────────────────────────┘
```

Conséquences à connaître par cœur :

- **Aucune donnée n'est copiée ni déplacée.** Les données partagées n'occupent aucun stockage dans le compte du consommateur.
- **Le fournisseur paie le stockage ; le consommateur paie le calcul**, c'est-à-dire le warehouse avec lequel il interroge les données.
- **Les données sont à jour en permanence** : le consommateur lit la table du fournisseur, pas un instantané.
- **Tout est en lecture seule** côté consommateur : il ne peut ni modifier ni supprimer les objets partagés.
- **Le fournisseur peut retirer l'accès à tout moment**, avec effet immédiat.

### 1.2 Fournisseur, consommateur, et l'objet SHARE

| Terme | Définition |
|---|---|
| Fournisseur (provider) | le compte qui crée le partage et choisit les objets et les comptes destinataires |
| Consommateur (consumer) | le compte qui crée une base de données à partir du partage et l'interroge |
| `SHARE` | un objet Snowflake nommé qui contient les droits donnés sur les objets partagés et la liste des comptes autorisés |

Un même compte peut être fournisseur et consommateur à la fois. Un fournisseur peut créer autant de partages qu'il le souhaite et ajouter plusieurs comptes à chacun. Côté consommateur, on ne peut créer qu'**une seule base par partage reçu**.

Un partage ne contient pas de données : c'est une enveloppe de droits. On y range des privilèges (`GRANT ... TO SHARE`) comme on en donne à un rôle.

### 1.3 Ce qui peut être partagé

D'après la documentation : bases de données, tables, tables dynamiques, tables externes, tables Apache Iceberg, vues (dont vues sécurisées et vues matérialisées sécurisées), fonctions définies par l'utilisateur (UDF), ainsi que des objets plus récents (services Cortex Search, modèles).

Par défaut, un partage n'accepte que des objets **sécurisés** pour les vues et les fonctions : le paramètre `SECURE_OBJECTS_ONLY` d'un `SHARE` vaut `TRUE`. Il faut le passer explicitement à `FALSE` pour partager une vue ordinaire. Pour l'examen, retenez la règle classique : **on partage des vues sécurisées et des UDF sécurisées**.

### 1.4 Côté fournisseur, en SQL

Créer un partage demande le rôle `ACCOUNTADMIN`, ou un rôle ayant reçu le privilège global `CREATE SHARE`.

```sql
USE ROLE ACCOUNTADMIN;

-- 1. L'enveloppe, vide pour l'instant
CREATE SHARE IF NOT EXISTS SALES_SHARE
  COMMENT = 'Ventes quotidiennes pour le distributeur partenaire';

-- 2. La chaîne d'accès, comme pour un rôle : base, schéma, puis objet
GRANT USAGE  ON DATABASE SALES_DB                             TO SHARE SALES_SHARE;
GRANT USAGE  ON SCHEMA   SALES_DB.ANALYTICS                   TO SHARE SALES_SHARE;
GRANT SELECT ON VIEW     SALES_DB.ANALYTICS.DAILY_SALES_PARTNER_V TO SHARE SALES_SHARE;

-- 3. Les comptes destinataires (identifiant ORGANISATION.COMPTE)
ALTER SHARE SALES_SHARE ADD ACCOUNTS = PARTNERORG.PARTNER_ACCOUNT;

-- Contrôler
SHOW SHARES;                          -- kind = OUTBOUND : partages émis ; INBOUND : partages reçus
SHOW GRANTS TO SHARE SALES_SHARE;     -- ce que contient le partage
SHOW GRANTS OF SHARE SALES_SHARE;     -- les comptes qui y ont accès
```

Deux points souvent demandés :

- Un objet ajouté plus tard dans le schéma n'est **pas** partagé automatiquement : il faut un nouveau `GRANT ... TO SHARE`. Une fois le droit donné, l'objet est visible immédiatement par les consommateurs.
- Retirer l'accès : `REVOKE SELECT ON VIEW ... FROM SHARE SALES_SHARE;` pour un objet, `ALTER SHARE SALES_SHARE REMOVE ACCOUNTS = ...;` pour un compte, `DROP SHARE SALES_SHARE;` pour tout arrêter.

### 1.5 Côté consommateur, en SQL

Créer une base à partir d'un partage demande `ACCOUNTADMIN`, ou un rôle ayant les privilèges globaux `IMPORT SHARE` et `CREATE DATABASE`.

```sql
USE ROLE ACCOUNTADMIN;

SHOW SHARES;                                        -- les partages reçus (kind = INBOUND)
DESC SHARE PROVIDERORG.PROVIDER_ACCOUNT.SALES_SHARE; -- ce qu'il contient

-- Le partage ne devient utilisable qu'une fois transformé en base
CREATE DATABASE PARTNER_SALES FROM SHARE PROVIDERORG.PROVIDER_ACCOUNT.SALES_SHARE;

-- Ouvrir la base aux autres rôles du compte : un seul privilège, IMPORTED PRIVILEGES
GRANT IMPORTED PRIVILEGES ON DATABASE PARTNER_SALES TO ROLE SALES_ANALYST;

SELECT * FROM PARTNER_SALES.ANALYTICS.DAILY_SALES_PARTNER_V LIMIT 10;   -- avec SON warehouse
```

Ce que le consommateur **ne peut pas** faire sur une base importée :

| Action | Possible ? |
|---|---|
| Insérer, modifier, créer un objet dans la base | non (lecture seule) |
| Cloner la base, un schéma ou une table | non |
| Utiliser Time Travel sur les objets partagés | non |
| Répliquer la base importée vers un autre compte | non |
| Créer une deuxième base à partir du même partage | non |
| Repartager à un tiers | non par défaut ; uniquement si le fournisseur a autorisé le repartage |

Pour garder une copie modifiable, le consommateur écrit un `CREATE TABLE ... AS SELECT` dans une de ses propres bases : il paie alors le stockage de cette copie, qui n'est plus tenue à jour.

### 1.6 Comptes lecteurs (reader accounts)

Que faire si le partenaire n'est pas client de Snowflake ? Le fournisseur lui crée un **compte lecteur** : un compte Snowflake géré par le fournisseur, sans contrat ni coût pour le partenaire.

```sql
USE ROLE ACCOUNTADMIN;      -- ou un rôle ayant le privilège global CREATE ACCOUNT

CREATE MANAGED ACCOUNT PARTNER_READER
  ADMIN_NAME = 'partner_admin',
  ADMIN_PASSWORD = '<mot de passe robuste>',
  TYPE = READER;

SHOW MANAGED ACCOUNTS;
ALTER SHARE SALES_SHARE ADD ACCOUNTS = <identifiant du compte lecteur>;
```

| Question | Réponse |
|---|---|
| Qui le crée et le possède ? | le compte fournisseur |
| Qui paie le calcul ? | **le fournisseur** : les crédits des warehouses du compte lecteur lui sont facturés |
| Quelle édition, quelle région ? | celles du compte fournisseur |
| De qui peut-il lire les données ? | uniquement du fournisseur qui l'a créé |
| Que peut-on y faire ? | interroger les données partagées ; pas de `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `COPY INTO <table>`, ni de création de partage, de pipe ou de stage |
| Combien peut-on en créer ? | 75 par défaut ; au-delà, demande au support |

Un compte lecteur est vide à sa création : il faut s'y connecter, créer un warehouse, puis la base à partir du partage. Comme le fournisseur paie, la documentation recommande d'y poser un moniteur de ressources (resource monitor, [chapitre 9](09-monitoring.md)).

---

## 2. Vues sécurisées et fonctions sécurisées

### 2.1 Pourquoi « sécurisées »

Une vue ordinaire a deux faiblesses lorsqu'on la montre à un tiers :

1. Sa définition est lisible (`GET_DDL`, `SHOW VIEWS`) : le tiers apprend le nom des tables et la logique de filtrage.
2. L'optimiseur peut réorganiser la requête de telle sorte qu'une fonction ou un message d'erreur laisse deviner des lignes que le filtre devait cacher.

Une **vue sécurisée** (`SECURE VIEW`) corrige les deux : sa définition n'est visible que des utilisateurs ayant le rôle propriétaire, et certaines optimisations sont désactivées pour qu'aucune donnée filtrée ne fuie. Le prix à payer est la performance : une vue sécurisée peut être plus lente qu'une vue ordinaire. On ne l'utilise donc que lorsque la confidentialité le justifie.

```sql
CREATE OR REPLACE SECURE VIEW SALES_DB.ANALYTICS.DAILY_SALES_FR_V AS
  SELECT sale_date, country, total_amount
  FROM SALES_DB.ANALYTICS.DAILY_SALES
  WHERE country = 'France';

ALTER VIEW SALES_DB.ANALYTICS.DAILY_SALES_FR_V SET SECURE;     -- convertir une vue existante (UNSET SECURE pour l'inverse)
SHOW VIEWS LIKE 'DAILY_SALES%' IN SCHEMA SALES_DB.ANALYTICS;   -- colonne is_secure
```

Le même mot-clé existe pour les vues matérialisées (`CREATE SECURE MATERIALIZED VIEW`) et les fonctions (`CREATE SECURE FUNCTION`). Une UDF sécurisée cache son code, ce qui permet de partager un calcul sans en révéler la formule.

### 2.2 Une seule vue pour plusieurs consommateurs

Le modèle recommandé par la documentation : une table de correspondance dit quel compte a droit à quelles lignes, et la vue sécurisée filtre avec `CURRENT_ACCOUNT()`.

```sql
USE ROLE SALES_ENGINEER;
USE SCHEMA SALES_DB.ANALYTICS;

CREATE TABLE IF NOT EXISTS SHARING_ACCESS (
  country            VARCHAR,
  snowflake_account  VARCHAR      -- le compte consommateur autorisé à voir ce pays
);

INSERT INTO SHARING_ACCESS VALUES
  ('France',  'PARTNER_FR'),
  ('Germany', 'PARTNER_DE');

CREATE OR REPLACE SECURE VIEW DAILY_SALES_PARTNER_V AS
  SELECT s.sale_date, s.country, s.total_amount
  FROM DAILY_SALES s
  JOIN SHARING_ACCESS a
    ON a.country = s.country
   AND a.snowflake_account = CURRENT_ACCOUNT();
```

Dans le compte du fournisseur, cette vue ne renvoie rien : `CURRENT_ACCOUNT()` n'y correspond à aucune ligne de la table de correspondance. Pour la tester sans second compte, on simule le consommateur :

```sql
ALTER SESSION SET SIMULATED_DATA_SHARING_CONSUMER = 'PARTNER_FR';
SELECT country, COUNT(*) FROM DAILY_SALES_PARTNER_V GROUP BY 1;   -- uniquement France
ALTER SESSION UNSET SIMULATED_DATA_SHARING_CONSUMER;
```

Dans une vue partagée, c'est `CURRENT_ACCOUNT()` qu'il faut utiliser : `CURRENT_USER()` et `CURRENT_ROLE()` n'ont pas de sens pour le fournisseur, puisque les utilisateurs et les rôles sont ceux du consommateur. La table de correspondance, elle, n'est jamais ajoutée au partage : seule la vue l'est.

---

## 3. Annonces, Marketplace et échanges de données

### 3.1 Les annonces (listings)

Le partage direct de la section 1 est simple, mais limité : il ne fonctionne que dans la même région, il ne décrit pas les données et il ne permet pas de les vendre. Une **annonce** (listing) est, selon la documentation, une méthode enrichie de partage sécurisé : elle emballe un partage ou une application native (Snowflake Native App) avec des métadonnées (titre, description, exemples de requêtes).

| Qui voit l'annonce ? | Type |
|---|---|
| Des comptes désignés par le fournisseur | annonce privée (private listing) |
| Tous les utilisateurs de Snowflake Marketplace | annonce publique |
| Les comptes de sa propre organisation | annonce interne à l'organisation (organizational listing) |

Une annonce peut être **gratuite** (accès complet et immédiat), en **essai limité** (accès restreint de 1 à 90 jours, puis demande d'accès complet) ou **payante** (facturée au consommateur, dans certaines régions seulement).

Ce qu'une annonce ajoute à un partage direct : le partage entre régions et entre fournisseurs cloud, la publication sur le Marketplace, la facturation, les statistiques d'usage, la description des données.

### 3.2 Snowflake Marketplace

Le Marketplace est le catalogue public des annonces. On y trouve des jeux de données (météo, démographie, données financières) et des applications, proposés par Snowflake et par des fournisseurs tiers. On y accède dans Snowsight, sans quitter son compte.

Côté consommateur, « obtenir » (Get) une annonce gratuite crée une base de données importée dans le compte, exactement comme un `CREATE DATABASE ... FROM SHARE`. Les règles de la section 1.5 s'appliquent : lecture seule, aucun stockage facturé, calcul payé par le consommateur.

### 3.3 Les échanges de données privés (Data Exchange)

Un Data Exchange est un Marketplace privé : un espace où un groupe **fermé** de membres invités (filiales, fournisseurs, partenaires) publie et consomme des annonces. Le compte qui héberge l'échange en est l'administrateur : il invite les membres et décide qui peut publier (fournisseur) et qui peut consommer. La fonctionnalité n'est pas activée par défaut : il faut la demander au support de Snowflake. La documentation oriente désormais vers les annonces privées et les annonces internes à l'organisation pour les mêmes besoins.

### 3.4 Partage direct, annonce ou échange : comparaison

| | Partage direct | Annonce (privée ou Marketplace) | Data Exchange |
|---|---|---|---|
| Destinataires | comptes nommés | comptes nommés, ou tout le Marketplace | membres invités d'un groupe fermé |
| Même région obligatoire | oui | non (auto-fulfillment) | non |
| Description, exemples de requêtes | non | oui | oui |
| Facturation au consommateur | non | possible (annonce payante) | non |
| Statistiques d'usage | limitées | oui | oui |
| Mise en place | trois commandes SQL | Snowsight, Provider Studio | activation par le support |

### 3.5 Les salles blanches (data clean rooms), en bref

Deux entreprises veulent croiser leurs fichiers clients (par exemple mesurer combien de clients elles ont en commun) **sans se montrer leurs lignes**. Une salle blanche est un environnement où chaque partie apporte ses données, et où seules des analyses prédéfinies et des résultats agrégés peuvent sortir. Snowflake Data Clean Rooms s'appuie sur le partage sécurisé et sur les politiques de gouvernance ([chapitre 15](15-gouvernance.md)). À retenir : l'objectif est l'analyse conjointe **sans exposer les données sous-jacentes**. La fonctionnalité n'est pas disponible sur un compte d'essai.

---

## 4. Partager entre régions et entre fournisseurs cloud

Un partage direct ne fonctionne qu'entre comptes de la **même région** du même fournisseur cloud : il n'y a pas de copie, les deux comptes doivent donc lire le même stockage. Pour servir un consommateur situé ailleurs, il faut que les données y soient présentes. Deux solutions :

| Solution | Principe |
|---|---|
| Annonce avec Cross-Cloud Auto-Fulfillment | Snowflake réplique automatiquement le produit de données vers la région du consommateur ; le fournisseur n'administre rien |
| Réplication manuelle puis partage | le fournisseur crée un compte dans la région du consommateur, y réplique la base (section 5), puis crée un partage direct depuis ce compte |

Dans les deux cas, des données sont réellement copiées dans une autre région : le fournisseur paie cette réplication (transfert, calcul, stockage), et doit vérifier qu'aucune règle juridique n'interdit d'héberger ces données dans le pays concerné.

---

## 5. Réplication et bascule

### 5.1 Répliquer : une copie tenue à jour dans un autre compte

La réplication recopie des objets d'un compte **source** vers un ou plusieurs comptes **cibles** de la **même organisation**, dans une autre région ou chez un autre fournisseur cloud. L'objet d'origine est dit primaire ; sa copie, secondaire, est en **lecture seule** et se met à jour par rafraîchissements successifs.

Trois usages : la continuité d'activité, le partage entre régions (section 4), la migration d'un compte vers une autre région.

### 5.2 Groupes de réplication et groupes de bascule

| | Groupe de réplication (`REPLICATION GROUP`) | Groupe de bascule (`FAILOVER GROUP`) |
|---|---|---|
| Rôle | répliquer un ensemble d'objets comme un tout cohérent | idem, et pouvoir **promouvoir** la copie en primaire |
| Copie secondaire | lecture seule | lecture seule, puis lecture et écriture après promotion |
| Édition | toutes pour les bases et les partages | Business Critical ou supérieure |

Les bases et les partages se répliquent dans toutes les éditions. Les autres objets du compte (utilisateurs, rôles, warehouses, moniteurs de ressources, politiques réseau, intégrations) et toute bascule demandent Business Critical.

Avant toute chose, l'administrateur de l'organisation (rôle `ORGADMIN`) active la réplication pour le compte source et le compte cible.

```sql
-- Dans le compte SOURCE
USE ROLE ACCOUNTADMIN;
CREATE FAILOVER GROUP SALES_FG
  OBJECT_TYPES = DATABASES, ROLES, WAREHOUSES
  ALLOWED_DATABASES = SALES_DB
  ALLOWED_ACCOUNTS = MYORG.ACCOUNT_SECOURS
  REPLICATION_SCHEDULE = '10 MINUTE';

-- Dans le compte CIBLE
CREATE FAILOVER GROUP SALES_FG AS REPLICA OF MYORG.ACCOUNT_PROD.SALES_FG;
ALTER FAILOVER GROUP SALES_FG REFRESH;       -- rafraîchissement manuel, en plus du planning

-- Le jour de la panne, toujours dans le compte CIBLE : il devient primaire
ALTER FAILOVER GROUP SALES_FG PRIMARY;
```

La commande de bascule s'exécute **dans le compte cible**, celui qui prend le relais. Entre deux rafraîchissements, les dernières modifications de la source ne sont pas encore sur la cible : la fréquence du planning détermine la quantité de données que l'on accepte de perdre.

Une base importée depuis un partage ne peut pas être répliquée : c'est le fournisseur qui réplique sa base, pas le consommateur.

### 5.3 Rediriger les connexions (Client Redirect)

Basculer les données ne suffit pas : les outils se connectent encore à l'adresse de l'ancien compte. Client Redirect fournit une adresse de connexion stable, de la forme `organisation-nom_de_connexion.snowflakecomputing.com`, portée par un objet `CONNECTION`. Le jour de la bascule, on désigne la connexion du compte de secours comme primaire, et les outils suivent sans changer leur configuration. Client Redirect ne réplique aucune donnée, et demande l'édition Business Critical.

### 5.4 Continuité d'activité : ce que chaque mécanisme protège

| Incident | Mécanisme | Chapitre |
|---|---|---|
| Une table modifiée ou supprimée par erreur | Time Travel (`UNDROP`, `AT`, `BEFORE`) | [13](13-stockage-protection.md) |
| Données perdues après la fin de Time Travel | Fail-safe : 7 jours, récupération par Snowflake uniquement | [13](13-stockage-protection.md) |
| Une région entière indisponible | réplication, groupe de bascule, Client Redirect | ce chapitre |

Time Travel et Fail-safe protègent contre une erreur **dans** le compte ; ils ne servent à rien si la région est en panne. La réplication protège contre la perte d'une région ; elle recopie aussi fidèlement une erreur humaine.

---

## 6. Clonage et partage

Le clonage (`CREATE ... CLONE`, [chapitre 13](13-stockage-protection.md)) crée une copie « sans copie » : le clone pointe sur les mêmes micro-partitions que l'original, et seul ce qui est modifié ensuite occupe du stockage supplémentaire. Le clone reste dans le **même compte**.

Liens avec le partage :

- Un clone est un objet comme un autre dans le compte du fournisseur : il peut être ajouté à un partage. C'est une façon de partager une image figée des données pendant que l'original continue d'évoluer.
- Le consommateur ne peut **pas** cloner une base importée, ni aucun de ses schémas ou tables.
- Cloner une table ne copie pas, en règle générale, les droits donnés sur la table d'origine. Cloner une base ou un schéma conserve les droits des objets qu'ils contiennent, mais pas ceux du conteneur lui-même.

### Partage, réplication, clonage : le tableau à connaître

| | Partage | Réplication | Clonage |
|---|---|---|---|
| But | donner accès à un autre compte | copie de secours ou de proximité | environnement de test, sauvegarde instantanée |
| Destination | autre compte, même région (partage direct) | autre compte de la même organisation, autre région ou autre cloud | même compte |
| Données copiées | non | oui | non au départ |
| Droits sur la copie | lecture seule | lecture seule (jusqu'à une bascule) | lecture et écriture |
| Fraîcheur | temps réel | au dernier rafraîchissement | figée à l'instant du clonage |
| Stockage payé par | le fournisseur | le compte cible, en plus du source | le compte, pour les seules modifications |
| Commande | `CREATE SHARE` | `CREATE REPLICATION GROUP`, `CREATE FAILOVER GROUP` | `CREATE ... CLONE` |

---

## 7. Pièges fréquents

| Affirmation tentante | Réalité |
|---|---|
| « Le consommateur paie le stockage des données partagées. » | Non : aucun stockage chez lui. Il ne paie que son calcul. |
| « Avec un compte lecteur, le partenaire paie ses requêtes. » | Non : c'est le fournisseur qui paie le calcul du compte lecteur. |
| « Le consommateur peut cloner la base reçue pour travailler dessus. » | Non : ni clonage ni Time Travel sur une base importée. |
| « Il suffit de créer la table dans le schéma partagé. » | Non : chaque nouvel objet doit être donné au partage par un `GRANT`. |
| « Un partage direct fonctionne entre AWS et Azure. » | Non : même région seulement. Il faut une annonce avec auto-fulfillment, ou une réplication. |
| « La réplication demande l'édition Business Critical. » | Faux pour les bases et les partages (toutes éditions). Vrai pour la bascule et pour les autres objets du compte. |
| « On donne `SELECT` sur la base importée à un rôle. » | Non : un seul privilège, `IMPORTED PRIVILEGES`. |
| « Un compte Business Critical partage librement avec un compte Standard. » | Non : bloqué par défaut. Il faut le privilège `OVERRIDE SHARE RESTRICTIONS` et `SHARE_RESTRICTIONS = FALSE` à l'ajout du compte. |
| « Une vue sécurisée est plus rapide. » | Non : elle peut être plus lente, des optimisations étant désactivées. |

---

## 8. À retenir pour la certification

1. Le partage sécurisé ne copie rien : il passe par la couche de services et les métadonnées. Stockage payé par le fournisseur, calcul par le consommateur.
2. Un `SHARE` contient des privilèges et une liste de comptes. Création : `ACCOUNTADMIN` ou privilège `CREATE SHARE`. Consommation : `ACCOUNTADMIN` ou privilèges `IMPORT SHARE` et `CREATE DATABASE`.
3. Côté consommateur : une base par partage, en lecture seule, sans clonage, sans Time Travel, sans réplication. Accès donné aux rôles par `GRANT IMPORTED PRIVILEGES`.
4. Compte lecteur : pour un partenaire sans compte Snowflake ; créé, possédé et **payé** par le fournisseur ; `CREATE MANAGED ACCOUNT ... TYPE = READER` ; 75 par défaut ; même édition et même région que le fournisseur.
5. On partage des vues **sécurisées** et des UDF **sécurisées** : définition cachée, pas de fuite par l'optimiseur, au prix de la performance. Filtrage par consommateur avec `CURRENT_ACCOUNT()`.
6. Partage direct : même région. Autre région ou autre cloud : annonce avec Cross-Cloud Auto-Fulfillment, ou réplication puis partage.
7. Annonce (listing) : un partage ou une application, plus des métadonnées. Privée, publique sur le Marketplace, ou interne à l'organisation. Gratuite, en essai limité, ou payante.
8. Data Exchange : place de marché privée pour un groupe fermé de membres invités, administrée par le compte hôte.
9. Salle blanche : analyser des données à plusieurs sans exposer les lignes de chacun.
10. Réplication : entre comptes de la même organisation, copie secondaire en lecture seule. Bases et partages : toutes éditions. Bascule, Client Redirect et autres objets du compte : Business Critical.
11. Groupe de réplication : lecture seule. Groupe de bascule : promouvable avec `ALTER FAILOVER GROUP ... PRIMARY`, exécuté dans le compte cible.
12. Clonage : même compte, sans copie au départ, copie modifiable. À ne confondre ni avec le partage ni avec la réplication.

---

## 9. Atelier pratique (30 à 45 minutes)

L'atelier se fait sur un seul compte d'essai. Les étapes qui exigent un second compte ou une édition supérieure ont une variante.

### Étape 1 : préparer les données (5 minutes)

```sql
USE ROLE SALES_ENGINEER;
USE WAREHOUSE SALES_WH;
USE SCHEMA SALES_DB.ANALYTICS;

CREATE OR REPLACE TABLE DAILY_SALES AS
  SELECT order_date AS sale_date, ship_country AS country, SUM(total_amount) AS total_amount
  FROM SALES_DB.RAW_DATA.ORDERS_RAW          -- table chargée au chapitre 11
  GROUP BY 1, 2;

SELECT country, COUNT(*) FROM DAILY_SALES GROUP BY 1 ORDER BY 2 DESC;
```

### Étape 2 : la vue sécurisée et la simulation d'un consommateur (10 minutes)

1. Créer la table `SHARING_ACCESS` et la vue `DAILY_SALES_PARTNER_V` de la section 2.2, en utilisant deux pays réellement présents dans vos données.
2. Interroger la vue : combien de lignes renvoie-t-elle, et pourquoi ?
3. Simuler `PARTNER_FR`, puis `PARTNER_DE`, avec `SIMULATED_DATA_SHARING_CONSUMER`, et vérifier que chacun ne voit que son pays.
4. Avec le rôle `SALES_ANALYST`, exécuter `SELECT GET_DDL('VIEW', 'SALES_DB.ANALYTICS.DAILY_SALES_PARTNER_V');` : que constatez-vous ? Comparez avec une vue ordinaire.

### Étape 3 : créer le partage (10 minutes)

1. Avec `ACCOUNTADMIN`, créer `SALES_SHARE` et lui donner les trois droits de la section 1.4.
2. Tenter `GRANT SELECT ON TABLE SALES_DB.ANALYTICS.SHARING_ACCESS TO SHARE SALES_SHARE;` puis le retirer : pourquoi cette table ne doit-elle pas être partagée ?
3. Contrôler avec `SHOW GRANTS TO SHARE SALES_SHARE;` et `SHOW SHARES;`.

Ajouter un consommateur :

- **Avec un second compte** dans la même région (celui d'un autre apprenant) : échanger les identifiants de compte, exécuter `ALTER SHARE ... ADD ACCOUNTS`, puis faire jouer à l'autre apprenant la section 1.5. Pensez à ajouter son compte dans `SHARING_ACCESS`.
- **Variante avec un seul compte** : s'arrêter à la simulation de l'étape 2. La création d'un compte lecteur (section 1.6) peut être tentée, mais elle n'est pas garantie sur un compte d'essai ; si elle réussit, supprimez le compte lecteur en fin d'atelier, car son calcul est prélevé sur vos crédits.

### Étape 4 : se mettre à la place du consommateur (10 minutes)

Votre compte d'essai consomme déjà un partage : la base `SNOWFLAKE_SAMPLE_DATA`.

```sql
USE ROLE ACCOUNTADMIN;
SHOW SHARES;                                   -- repérer la ligne kind = INBOUND
SHOW DATABASES LIKE 'SNOWFLAKE_SAMPLE_DATA';   -- colonnes origin et kind

SELECT COUNT(*) FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.NATION;                   -- lecture : réussit
CREATE TABLE SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.TEST (id INT);                    -- doit échouer
CREATE TABLE SALES_DB.ANALYTICS.NATION_CLONE
  CLONE SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.NATION;                                -- doit échouer
CREATE TABLE SALES_DB.ANALYTICS.NATION_COPY AS
  SELECT * FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.NATION;                        -- réussit : vraie copie
```

Si la base n'apparaît pas, ouvrez le Marketplace dans Snowsight, choisissez une annonce gratuite et obtenez-la : une base importée est créée, sur laquelle refaire les mêmes essais. Notez les messages d'erreur obtenus.

### Étape 5 : réplication (lecture, 5 minutes)

La bascule demande Business Critical et deux comptes d'une même organisation : elle ne se pratique pas sur un compte d'essai. Variante : relire le script de la section 5.2 et dire dans quel compte s'exécute chaque commande, et laquelle rend la copie modifiable.

### Étape 6 : nettoyer

```sql
USE ROLE ACCOUNTADMIN;
DROP SHARE IF EXISTS SALES_SHARE;
USE ROLE SALES_ENGINEER;
DROP VIEW  IF EXISTS SALES_DB.ANALYTICS.DAILY_SALES_PARTNER_V;
DROP TABLE IF EXISTS SALES_DB.ANALYTICS.SHARING_ACCESS;
DROP TABLE IF EXISTS SALES_DB.ANALYTICS.NATION_COPY;   -- avec le rôle qui l'a créée
```

Questions : pourquoi l'étape 4 échoue-t-elle au clonage mais réussit-elle au `CREATE TABLE ... AS SELECT` ? Qui paie le stockage de `NATION_COPY` ? Si le distributeur partenaire était hébergé dans une autre région, que faudrait-il changer ?

## Points de vérification

- [ ] La vue sécurisée ne renvoie aucune ligne dans votre compte, et les bonnes lignes pour chaque consommateur simulé
- [ ] La définition de la vue sécurisée est invisible pour un rôle non propriétaire
- [ ] `SHOW GRANTS TO SHARE` liste la base, le schéma et la vue, et pas la table de correspondance
- [ ] Vous savez dire qui paie le stockage et qui paie le calcul dans un partage, puis dans un compte lecteur
- [ ] Les deux erreurs attendues de l'étape 4 ont été obtenues et expliquées
- [ ] Vous savez citer, pour le partage, la réplication et le clonage : la destination, la copie ou non des données, les droits sur la copie

## Documentation officielle

- [Présentation du partage sécurisé de données](https://docs.snowflake.com/en/user-guide/data-sharing-intro)
- [Consommer un partage](https://docs.snowflake.com/en/user-guide/data-share-consumers)
- [Comptes lecteurs](https://docs.snowflake.com/en/user-guide/data-sharing-reader-create)
- [Vues sécurisées](https://docs.snowflake.com/en/user-guide/views-secure)
- [À propos des annonces (listings)](https://docs.snowflake.com/en/collaboration/collaboration-listings-about)
- [Data Exchange](https://docs.snowflake.com/en/user-guide/data-exchange)
- [Partager entre régions et fournisseurs cloud](https://docs.snowflake.com/en/user-guide/secure-data-sharing-across-regions-platforms)
- [Snowflake Data Clean Rooms](https://docs.snowflake.com/en/user-guide/cleanrooms/introduction)
- [Introduction à la réplication et à la bascule](https://docs.snowflake.com/en/user-guide/account-replication-intro)
- [Client Redirect](https://docs.snowflake.com/en/user-guide/client-redirect)

---

[← Retour au sommaire](README.md) | [← Précédent](18-transformation.md) | [Plan de préparation à la certification →](certification/PLAN.md)
