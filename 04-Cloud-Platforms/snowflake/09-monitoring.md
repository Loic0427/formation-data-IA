# 9. Suivi de l'activité et des coûts

[← Retour au sommaire](README.md) | [← Précédent](08-gestion-privileges.md) | [Suivant →](10-securite.md)

## Vue d'ensemble

Snowflake se paie à l'usage : chaque seconde de warehouse et chaque gigaoctet stocké sont facturés. Suivre l'activité sert donc à deux choses : comprendre pourquoi une requête est lente, et éviter une facture inattendue.

Le coût total a trois composantes : le **calcul** (warehouses, fonctions serverless, services cloud), le **stockage** et le **transfert de données**. Ce chapitre montre où lire ces informations dans Snowsight, comment les interroger en SQL dans la base `SNOWFLAKE`, et comment poser des garde-fous avec les resource monitors et les budgets.

Les requêtes de ce chapitre lisent les vues `SNOWFLAKE.ACCOUNT_USAGE` : elles se lancent avec le rôle `ACCOUNTADMIN`, et leurs chiffres ont un retard qui va de 45 minutes à 3 heures selon la vue.

---

## 1. L'historique des requêtes

1. Dans le menu, sélectionnez **Monitoring** » **Query History**.
2. Filtrez par utilisateur, warehouse, statut, durée ou texte SQL.

La page couvre les 14 derniers jours et affiche, pour chaque requête, le texte SQL, l'identifiant (Query ID), le statut, l'utilisateur, le warehouse, la durée et l'heure de début.

| Qui voit quoi | |
|---|---|
| Tout utilisateur | ses propres requêtes |
| Rôle avec `MONITOR` ou `OPERATE` sur un warehouse | les requêtes exécutées sur ce warehouse |
| `ACCOUNTADMIN` | toutes les requêtes du compte |

### Le profil d'une requête

En ouvrant une requête, l'onglet **Query Profile** affiche son plan d'exécution : les opérations effectuées, leur enchaînement et la part du temps passée dans chacune. Le volet **Most Expensive Nodes** désigne les opérations les plus coûteuses : c'est le point de départ de toute optimisation ([chapitre 17](17-performance.md)).

---

## 2. Le suivi des coûts dans Snowsight

1. Prenez le rôle `ACCOUNTADMIN`.
2. Dans le menu, sélectionnez **Admin** » **Cost management**.

| Page | Contenu |
|---|---|
| **Account Overview** | vue d'ensemble des dépenses du compte |
| **Consumption** | consommation par jour, semaine ou mois, pour le calcul, le stockage et le transfert de données |
| **Budgets** | limites de dépense mensuelles et alertes (section 5) |
| **Resource Monitors** | quotas de crédits sur les warehouses (section 4) |

Ces pages peuvent afficher les données avec un retard allant jusqu'à 72 heures. L'activité d'un warehouse précis se consulte dans **Compute** » **Warehouses**, en ouvrant le warehouse.

---

## 3. Interroger ACCOUNT_USAGE en SQL

La base partagée `SNOWFLAKE` contient le schéma `ACCOUNT_USAGE`, dont les vues conservent un an d'historique, y compris pour les objets supprimés.

| | `SNOWFLAKE.ACCOUNT_USAGE` | `INFORMATION_SCHEMA` de chaque base |
|---|---|---|
| Retard des données | 45 minutes à 3 heures | aucun |
| Historique conservé | 1 an | 7 jours à 6 mois selon la vue ou la fonction |
| Objets supprimés | inclus | non inclus |

Par défaut, seul `ACCOUNTADMIN` lit la base `SNOWFLAKE`. On ouvre l'accès à un autre rôle avec `GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE ...`, ou avec les rôles de base de données `USAGE_VIEWER`, `GOVERNANCE_VIEWER`, `OBJECT_VIEWER` et `SECURITY_VIEWER`.

```sql
USE ROLE ACCOUNTADMIN;
USE WAREHOUSE SALES_WH;
```

### Les dix requêtes les plus longues de la semaine

```sql
SELECT
    QUERY_ID,
    USER_NAME,
    WAREHOUSE_NAME,
    TOTAL_ELAPSED_TIME / 1000           AS duree_s,
    BYTES_SCANNED / POWER(1024, 3)      AS go_lus,
    LEFT(QUERY_TEXT, 100)               AS debut_requete
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME > DATEADD('day', -7, CURRENT_TIMESTAMP())
ORDER BY TOTAL_ELAPSED_TIME DESC
LIMIT 10;
```

### Activité par utilisateur

```sql
SELECT
    USER_NAME,
    COUNT(*)                                        AS nb_requetes,
    SUM(TOTAL_ELAPSED_TIME) / 1000                  AS duree_totale_s,
    AVG(TOTAL_ELAPSED_TIME) / 1000                  AS duree_moyenne_s,
    COUNT_IF(UPPER(EXECUTION_STATUS) <> 'SUCCESS')        AS nb_echecs
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME > DATEADD('day', -7, CURRENT_TIMESTAMP())
GROUP BY USER_NAME
ORDER BY duree_totale_s DESC;
```

### Requêtes qui ont attendu un warehouse saturé

```sql
SELECT
    WAREHOUSE_NAME,
    COUNT(*)                              AS nb_requetes_en_attente,
    AVG(QUEUED_OVERLOAD_TIME) / 1000      AS attente_moyenne_s
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME > DATEADD('day', -7, CURRENT_TIMESTAMP())
  AND QUEUED_OVERLOAD_TIME > 0
GROUP BY WAREHOUSE_NAME;
```

### Crédits consommés par jour et par warehouse

```sql
SELECT
    DATE_TRUNC('day', START_TIME)   AS jour,
    WAREHOUSE_NAME,
    SUM(CREDITS_USED)               AS credits
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE START_TIME > DATEADD('day', -30, CURRENT_TIMESTAMP())
GROUP BY jour, WAREHOUSE_NAME
ORDER BY jour, WAREHOUSE_NAME;
```

`CREDITS_USED` additionne `CREDITS_USED_COMPUTE` (le warehouse) et `CREDITS_USED_CLOUD_SERVICES` (les services cloud). Ce total peut dépasser les crédits réellement facturés : les services cloud ne sont facturés que pour la part qui dépasse 10 % de la consommation quotidienne des warehouses. La vue `METERING_DAILY_HISTORY` donne les crédits facturés.

### Estimation du coût du mois

```sql
WITH prix AS (
    SELECT 3.00 AS prix_du_credit      -- à remplacer par le prix de votre contrat
)
SELECT
    SUM(CREDITS_USED)                    AS credits_du_mois,
    SUM(CREDITS_USED) * prix_du_credit   AS cout_estime
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
CROSS JOIN prix
WHERE START_TIME >= DATE_TRUNC('month', CURRENT_DATE())
GROUP BY prix_du_credit;
```

Le prix du crédit et celui du stockage dépendent de l'édition, du fournisseur cloud, de la région et du contrat : ils figurent dans la grille tarifaire de Snowflake.

### Stockage par base

```sql
SELECT
    DATABASE_NAME,
    AVG(AVERAGE_DATABASE_BYTES) / POWER(1024, 3)    AS go_donnees,
    AVG(AVERAGE_FAILSAFE_BYTES) / POWER(1024, 3)    AS go_failsafe
FROM SNOWFLAKE.ACCOUNT_USAGE.DATABASE_STORAGE_USAGE_HISTORY
WHERE USAGE_DATE > DATEADD('day', -30, CURRENT_DATE())
GROUP BY DATABASE_NAME
ORDER BY go_donnees DESC;
```

Le stockage facturé comprend les données actives, les versions conservées pour le Time Travel et le Fail-safe ([chapitre 13](13-stockage-protection.md)).

### Connexions

```sql
SELECT EVENT_TIMESTAMP, USER_NAME, CLIENT_IP, IS_SUCCESS, ERROR_MESSAGE
FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
WHERE EVENT_TIMESTAMP > DATEADD('day', -7, CURRENT_TIMESTAMP())
ORDER BY EVENT_TIMESTAMP DESC;
```

---

## 4. Limiter la consommation : les resource monitors

Un **resource monitor** fixe un quota de crédits sur une période et déclenche des actions quand des seuils sont atteints. Il ne surveille que les **warehouses** : il ne couvre ni les fonctions serverless ni les services d'IA. Seul `ACCOUNTADMIN` peut en créer.

| Action | Effet |
|---|---|
| Notify (`NOTIFY`) | envoie une notification, sans rien arrêter |
| Notify & Suspend (`SUSPEND`) | notifie et suspend les warehouses une fois les requêtes en cours terminées |
| Notify & Suspend Immediately (`SUSPEND_IMMEDIATE`) | notifie et suspend immédiatement, en annulant les requêtes en cours |

Un moniteur accepte une action de suspension, une action de suspension immédiate et jusqu'à cinq actions de notification. Il s'applique soit au compte entier (un seul moniteur de compte), soit à un ou plusieurs warehouses ; un warehouse ne peut être rattaché qu'à un seul moniteur. Le quota est remis à zéro au début de chaque mois par défaut.

### Dans Snowsight

1. Dans le menu, sélectionnez **Admin** » **Cost management**, puis **Resource Monitors**.
2. Créez un moniteur `SALES_WH_MONITOR` avec un quota de 20 crédits par mois, rattaché au warehouse `SALES_WH`.
3. Ajoutez les seuils : notification à 75 %, suspension à 90 %, suspension immédiate à 100 %.

### SQL équivalent

```sql
USE ROLE ACCOUNTADMIN;

CREATE OR REPLACE RESOURCE MONITOR SALES_WH_MONITOR
  WITH CREDIT_QUOTA = 20
       FREQUENCY = MONTHLY
       START_TIMESTAMP = IMMEDIATELY
  TRIGGERS ON 75 PERCENT DO NOTIFY
           ON 90 PERCENT DO SUSPEND
           ON 100 PERCENT DO SUSPEND_IMMEDIATE;

ALTER WAREHOUSE SALES_WH SET RESOURCE_MONITOR = SALES_WH_MONITOR;

SHOW RESOURCE MONITORS;
```

Les notifications sont désactivées par défaut : chaque administrateur les active dans son profil (**Settings**), après avoir vérifié son adresse e-mail.

---

## 5. Surveiller les dépenses : les budgets

Un **budget** définit une limite de dépense mensuelle, exprimée en crédits, pour le compte entier (budget de compte) ou pour un groupe d'objets (budget personnalisé). Il suit tout le calcul, y compris les fonctions serverless et les services d'IA que les resource monitors ne voient pas.

Un budget **alerte mais ne suspend rien** : il envoie une notification (e-mail, file de messages du fournisseur cloud ou webhook) lorsque la dépense prévue dépasse la limite. Il se configure dans **Admin** » **Cost management** » **Budgets**.

| | Resource monitor | Budget |
|---|---|---|
| Ce qui est suivi | les warehouses uniquement | tout le calcul, serverless et IA compris |
| Peut suspendre un warehouse | oui | non |
| Unité | crédits, sur une période au choix | crédits par mois calendaire |
| Portée | compte ou warehouses | compte ou groupe d'objets |

---

## 6. Les alertes

Snowflake ne fournit pas de liste d'alertes prêtes à cocher. Une **alerte** est un objet de schéma que l'on crée soi-même avec `CREATE ALERT`, à partir de trois éléments : une condition (une requête SQL), une action (par exemple l'envoi d'un e-mail) et une fréquence d'évaluation. Une alerte est créée suspendue : elle ne démarre qu'après `ALTER ALERT ... RESUME`. Créer une alerte demande le privilège global `EXECUTE ALERT`.

Pour le suivi des coûts, les notifications des resource monitors et des budgets suffisent dans la plupart des cas.

---

## 7. Agir à partir des mesures

| Constat | Cause probable | Action |
|---|---|---|
| Des requêtes attendent (`QUEUED_OVERLOAD_TIME` élevé) | trop de requêtes simultanées pour le warehouse | multi-cluster, ou warehouse séparé par usage |
| Des requêtes isolées sont lentes | requête lourde ou mal écrite | lire le Query Profile ; augmenter la taille si la requête est saine |
| Beaucoup de crédits pour peu de requêtes | warehouse trop grand, ou qui reste allumé | réduire la taille ; raccourcir `AUTO_SUSPEND` |
| Stockage qui grossit | rétention Time Travel longue, tables oubliées | revoir `DATA_RETENTION_TIME_IN_DAYS` ; supprimer les tables inutiles |

Habitudes à prendre : regarder la consommation chaque semaine, poser un resource monitor sur chaque warehouse, et un budget sur le compte.

---

## À retenir pour la certification

- Le coût de Snowflake a trois composantes : calcul, stockage, transfert de données. L'entrée de données est gratuite ; la sortie vers une autre région ou un autre cloud est facturée.
- Les services cloud ne sont facturés que pour la part qui dépasse 10 % de la consommation quotidienne des warehouses.
- `ACCOUNT_USAGE` : retard de 45 minutes à 3 heures, historique d'un an, objets supprimés inclus. `INFORMATION_SCHEMA` : pas de retard, historique de 7 jours à 6 mois.
- Un resource monitor ne suit que les warehouses, n'est créé que par `ACCOUNTADMIN`, et propose trois actions : Notify, Notify & Suspend, Notify & Suspend Immediately.
- Un budget suit aussi les fonctions serverless, mais il notifie sans rien suspendre.
- La page Query History de Snowsight couvre 14 jours ; le Query Profile montre le plan d'exécution et les opérations les plus coûteuses.

## ✅ Points de vérification
- [ ] Historique des requêtes consulté, Query Profile d'une requête ouvert
- [ ] Page **Cost management** consultée avec `ACCOUNTADMIN`
- [ ] Requêtes sur `ACCOUNT_USAGE` exécutées
- [ ] Resource monitor `SALES_WH_MONITOR` créé et rattaché à `SALES_WH`

## Documentation officielle
- [Historique des requêtes et Query Profile](https://docs.snowflake.com/en/user-guide/ui-snowsight-activity)
- [Explorer les coûts](https://docs.snowflake.com/en/user-guide/cost-exploring-overall)
- [Comprendre les coûts](https://docs.snowflake.com/en/user-guide/cost-understanding-overall)
- [Schéma ACCOUNT_USAGE](https://docs.snowflake.com/en/sql-reference/account-usage)
- [Resource monitors](https://docs.snowflake.com/en/user-guide/resource-monitors)
- [Budgets](https://docs.snowflake.com/en/user-guide/budgets)
- [Alertes](https://docs.snowflake.com/en/user-guide/alerts)

---

[← Retour au sommaire](README.md) | [← Précédent](08-gestion-privileges.md) | [Suivant →](10-securite.md)
