# Fiche de révision SnowPro Core (COF-C03)

[← Plan de préparation](PLAN.md) | [Planning de révision en 3 semaines](PLANNING_REVISION.md) | [← Sommaire du cours](../README.md)

Pour chaque domaine, les faits à connaître par cœur : chiffres, limites, « qui peut faire quoi », éditions requises. Les chiffres ont été vérifiés dans la documentation officielle le 4 octobre 2026. Snowflake fait évoluer ses limites : quand une valeur a changé récemment, l'ancienne est signalée, car elle circule encore dans les questions d'entraînement.

**L'examen** : 100 questions, 115 minutes, seuil 750 sur 1000, choix unique et choix multiples, 175 dollars, disponible en français.

---

## Les éditions : le tableau à savoir réciter

| Fonctionnalité | Édition minimale |
|---|---|
| Time Travel jusqu'à 1 jour, Fail-safe, partage sécurisé, étiquettes (tags), politiques réseau, MFA, SSO | Standard |
| Réplication des bases et des partages | Standard |
| Time Travel jusqu'à 90 jours | Enterprise |
| Warehouses multi-clusters | Enterprise |
| Vues matérialisées, optimisation de recherche, accélération de requêtes | Enterprise |
| Masquage de colonnes, politiques d'accès aux lignes, politiques d'agrégation et de projection | Enterprise |
| Classification des données sensibles, vue `ACCESS_HISTORY`, fonctions de qualité des données | Enterprise |
| Renouvellement périodique du chiffrement (periodic rekeying) | Enterprise |
| Clés gérées par le client (Tri-Secret Secure) | Business Critical |
| Connectivité privée (AWS PrivateLink, Azure Private Link, Google Cloud Private Service Connect) | Business Critical |
| Bascule (failover et failback), Client Redirect, réplication des autres objets du compte | Business Critical |
| Données de santé (HIPAA, HITRUST) et de paiement (PCI DSS) | Business Critical |
| Environnement entièrement isolé des autres comptes | Virtual Private Snowflake (VPS) |

---

## Domaine 1. Fonctionnalités et architecture (31 %)

Chapitres [12](../12-architecture.md), [13](../13-stockage-protection.md), [14](../14-ia-applications.md).

1. **Trois couches indépendantes** : stockage, calcul (warehouses virtuels), services cloud. L'architecture est un hybride de disque partagé (un stockage central) et de « rien de partagé » (des grappes de calcul indépendantes).
2. **Snowflake ne s'installe pas** : service entièrement géré, hébergé sur AWS, Azure ou Google Cloud ; ni installation locale ni cloud privé.
3. **Micro-partitions** : de 50 à 500 Mo de données non compressées chacune, stockage en colonnes, compression automatique, immuables. Créées automatiquement, sans action de l'utilisateur.
4. **Métadonnées par micro-partition** : plage de valeurs de chaque colonne, nombre de valeurs distinctes. Elles permettent l'élagage (pruning) : ne lire que les micro-partitions utiles.
5. **Tailles de warehouse** : X-Small 1 crédit par heure, puis doublement à chaque taille (Small 2, Medium 4, Large 8, X-Large 16, 2X-Large 32, 3X-Large 64, 4X-Large 128, 5X-Large 256, 6X-Large 512).
6. **Facturation du calcul** : à la seconde, avec un minimum de 60 secondes à chaque démarrage du warehouse.
7. **Taille par défaut** : X-Small avec `CREATE WAREHOUSE` en SQL.
8. **Services cloud** : facturés seulement pour la part qui dépasse 10 % de la consommation quotidienne des warehouses.
9. **Types de tables** :

| Type | Durée de vie | Time Travel | Fail-safe |
|---|---|---|---|
| Permanente | jusqu'à suppression | 0 à 1 jour (Standard), 0 à 90 jours (Enterprise) | 7 jours |
| Transitoire (transient) | jusqu'à suppression | 0 ou 1 jour | aucun |
| Temporaire (temporary) | la session | 0 ou 1 jour | aucun |

10. **Time Travel** : 1 jour par défaut ; paramètre `DATA_RETENTION_TIME_IN_DAYS` ; clauses `AT` et `BEFORE` avec `TIMESTAMP`, `OFFSET` ou `STATEMENT` ; `UNDROP` pour une table, un schéma, une base.
11. **Fail-safe** : 7 jours, non configurable, après la fin de Time Travel ; récupération par Snowflake uniquement, jamais par l'utilisateur.
12. **Clonage sans copie** (zero-copy cloning) : le clone partage les micro-partitions de l'original ; seul ce qui change ensuite est stocké. Cloner une table ne copie pas ses droits, en règle générale.
13. **Chiffrement** : toutes les données sont chiffrées par défaut (AES) ; les clés sont renouvelées automatiquement lorsqu'elles ont plus de 30 jours ; le rechiffrement annuel (periodic rekeying) demande Enterprise.
14. **Taille maximale d'une valeur `VARIANT`** : 128 Mo non compressés (les anciens supports indiquent 16 Mo).
15. **Hiérarchie des objets** : organisation, compte, base, schéma, objets (tables, vues, stages, formats de fichier, pipes, flux, tâches, fonctions).

---

## Domaine 2. Gestion du compte et gouvernance (20 %)

Chapitres [08](../08-gestion-privileges.md), [09](../09-monitoring.md), [10](../10-securite.md), [15](../15-gouvernance.md).

1. **Un privilège se donne à un rôle**, le rôle à un utilisateur ou à un autre rôle (contrôle d'accès par rôles), et chaque objet a un rôle propriétaire (contrôle d'accès discrétionnaire).
2. **Rôles système** : `ACCOUNTADMIN` (tout, dont la facturation), `SECURITYADMIN` (`MANAGE GRANTS`), `USERADMIN` (créer utilisateurs et rôles), `SYSADMIN` (créer warehouses et bases), `PUBLIC` (donné à tous). `ORGADMIN` agit au niveau de l'organisation ; la documentation annonce son remplacement progressif par `GLOBALORGADMIN`.
3. **Hiérarchie** : `ACCOUNTADMIN` hérite de `SECURITYADMIN` et de `SYSADMIN` ; `SECURITYADMIN` hérite de `USERADMIN`. Rattacher les rôles personnalisés à `SYSADMIN`.
4. **Lire une table demande quatre droits** : `USAGE` sur le warehouse, sur la base, sur le schéma, et `SELECT` sur la table.
5. **Droits futurs** : `GRANT ... ON FUTURE TABLES IN SCHEMA` couvre les objets créés après ; `ON ALL TABLES` ne couvre que l'existant.
6. **Moniteur de ressources** (resource monitor) : créé uniquement par `ACCOUNTADMIN` ; actions `NOTIFY`, `SUSPEND` (laisse finir les requêtes en cours), `SUSPEND_IMMEDIATE` (les interrompt). Il surveille les warehouses, pas le calcul sans serveur.
7. **Politique réseau** : liste d'adresses autorisées et bloquées, applicable au compte, à une intégration de sécurité ou à un utilisateur ; la plus spécifique l'emporte.
8. **Authentification** : mot de passe avec MFA, SSO fédéré, OAuth, paire de clés, jeton d'accès programmatique. Un utilisateur de type `SERVICE` n'a jamais de mot de passe.
9. **Masquage dynamique** (Enterprise) : une politique de masquage s'applique à une colonne et décide, à l'exécution, de la valeur montrée selon le rôle.
10. **Politique d'accès aux lignes** (Enterprise) : décide quelles lignes un rôle voit.
11. **Étiquettes** (tags) : toutes éditions ; une politique de masquage peut être attachée à une étiquette.
12. **`ACCOUNT_USAGE`** (base partagée `SNOWFLAKE`) : historique sur 1 an, latence de 45 minutes à 3 heures selon la vue, objets supprimés inclus.
13. **`INFORMATION_SCHEMA`** (dans chaque base) : aucune latence, historique de 7 jours à 6 mois selon la vue, objets supprimés exclus.
14. **Vue sécurisée** : définition visible du seul rôle propriétaire ; optimisations désactivées, donc potentiellement plus lente.
15. **Éditions à retenir ici** : Tri-Secret Secure et connectivité privée, Business Critical ; masquage, accès aux lignes, classification, `ACCESS_HISTORY`, Enterprise.

---

## Domaine 3. Chargement, déchargement et connectivité (18 %)

Chapitres [07](../07-import-donnees.md), [11](../11-chargement-stage-copy.md), [16](../16-snowpipe-export-connectivite.md).

1. **Stages internes** : stage utilisateur (un par utilisateur, noté `@~`), stage de table (un par table, noté `@%table`), stage nommé (`@nom`). Les stages utilisateur et de table ne peuvent être ni modifiés ni supprimés.
2. **Stage externe** : pointe vers Amazon S3, Azure ou Google Cloud Storage ; l'accès se configure de préférence par une intégration de stockage.
3. **`PUT`** envoie un fichier local vers un stage interne, **`GET`** le récupère ; ni l'un ni l'autre ne s'exécute dans une feuille SQL de Snowsight. `PUT` compresse en gzip par défaut.
4. **`COPY INTO <table>`** : exige un warehouse de l'utilisateur ; charge depuis un stage.
5. **Mémoire des fichiers chargés** : 64 jours pour `COPY INTO` (métadonnées de la table), 14 jours pour Snowpipe (métadonnées du pipe). Un fichier déjà chargé n'est pas rechargé, sauf `FORCE = TRUE`.
6. **`ON_ERROR`** : `ABORT_STATEMENT` par défaut pour `COPY INTO` ; `SKIP_FILE` par défaut pour Snowpipe ; `CONTINUE` ignore les lignes en erreur.
7. **`VALIDATION_MODE`** (`RETURN_n_ROWS`, `RETURN_ERRORS`, `RETURN_ALL_ERRORS`) : teste les fichiers sans rien charger.
8. **Taille de fichier recommandée** : 100 à 250 Mo compressés. Les très gros fichiers (100 Go ou plus) sont déconseillés.
9. **Snowpipe** : chargement continu, calcul sans serveur fourni par Snowflake, déclenché par une notification du stockage cloud (auto-ingest) ou par un appel à l'API REST. Avec lui, ne pas déposer de fichiers plus d'une fois par minute.
10. **Formats de fichier acceptés au chargement** : CSV, JSON, Avro, ORC, Parquet, XML.
11. **Déchargement** : `COPY INTO <emplacement>` ; plusieurs fichiers par défaut (`SINGLE = FALSE`) ; `MAX_FILE_SIZE` vaut 16 Mo par défaut et 5 Go au maximum.
12. **Transformation au chargement** : `COPY INTO` accepte un `SELECT` sur le stage (réordonner, convertir, omettre des colonnes), mais ni jointure ni agrégation.
13. **Colonnes de métadonnées** : `METADATA$FILENAME`, `METADATA$FILE_ROW_NUMBER`.
14. **Connectivité** : Snowsight, SnowSQL et Snowflake CLI, pilotes JDBC et ODBC, connecteurs Python, Spark et Kafka, API SQL REST.
15. **Identifiant de compte** : format `organisation-compte`.

---

## Domaine 4. Performance, requêtes et transformation (21 %)

Chapitres [17](../17-performance.md), [18](../18-transformation.md).

1. **Cache de résultats** : 24 heures, prolongé à chaque réutilisation, jusqu'à 31 jours au maximum ; aucun warehouse nécessaire ; requête identique au caractère près, données inchangées, pas de fonction non déterministe. Paramètre `USE_CACHED_RESULT`.
2. **Trois caches** : résultats (couche de services), métadonnées (couche de services : `COUNT(*)`, `MIN`, `MAX` sans warehouse), données locales du warehouse (perdues à la suspension).
3. **Agrandir (scale up)** : une taille supérieure accélère une requête lourde. **Ajouter des clusters (scale out)** : absorbe davantage d'utilisateurs simultanés, sans accélérer une requête isolée.
4. **Warehouse multi-clusters** (Enterprise) : mode maximisé (minimum égal au maximum) ou mode auto-scale (minimum différent du maximum). Le nombre maximal de clusters dépend de la taille du warehouse (la valeur historique, encore fréquente dans les questions, est 10).
5. **Politiques de mise à l'échelle** : `STANDARD` (par défaut) démarre un cluster dès qu'une requête attend ; `ECONOMY` ne le démarre que s'il y a de quoi l'occuper au moins 6 minutes.
6. **Clé de clustering** : utile pour les très grandes tables souvent filtrées sur les mêmes colonnes et peu modifiées ; le reclustering automatique est un service sans serveur, facturé.
7. **Profondeur de clustering** : `SYSTEM$CLUSTERING_DEPTH`, `SYSTEM$CLUSTERING_INFORMATION` ; plus la profondeur est faible, mieux la table est ordonnée.
8. **Optimisation de recherche** (Enterprise) : recherches ponctuelles très sélectives. **Accélération de requêtes** (Enterprise) : délègue une partie d'une requête lourde à du calcul sans serveur.
9. **Vue matérialisée** (Enterprise) : résultat stocké et maintenu automatiquement ; une seule table, aucune jointure.
10. **Profil de requête** : repérer l'élagage insuffisant (partitions lues proches du total), le débordement sur disque (spilling : mémoire insuffisante, warehouse trop petit), les jointures explosives.
11. **Semi-structuré** : type `VARIANT` ; accès `colonne:cle.sous_cle::type` ; `FLATTEN` avec `LATERAL` pour déplier un tableau ; `PARSE_JSON`.
12. **Flux (stream)** : enregistre les changements d'une table. Type standard (insertions, modifications, suppressions), append-only (insertions seulement), insert-only (tables externes). Consommé par une instruction DML dans une transaction.
13. **Tâche (task)** : exécute du SQL selon un planning ou après une autre tâche ; un graphe compte au plus 1000 tâches, une tâche au plus 100 parents et 100 enfants ; une tâche est créée suspendue.
14. **Table dynamique** : définie par une requête et un retard cible (`TARGET_LAG`) ; Snowflake la rafraîchit seul.
15. **Fonctions et procédures** : une UDF renvoie une valeur et s'utilise dans une requête ; une procédure stockée s'appelle avec `CALL` et peut exécuter des instructions. `QUERY_HISTORY` (fonction de table d'`INFORMATION_SCHEMA`) couvre les 7 derniers jours.

---

## Domaine 5. Collaboration autour des données (10 %)

Chapitre [19](../19-collaboration.md).

1. **Le partage ne copie rien** : stockage payé par le fournisseur, calcul payé par le consommateur.
2. **Créer un partage** : `ACCOUNTADMIN` ou privilège `CREATE SHARE`. **Le consommer** : `ACCOUNTADMIN` ou privilèges `IMPORT SHARE` et `CREATE DATABASE`.
3. **Trois commandes du fournisseur** : `CREATE SHARE`, `GRANT ... TO SHARE`, `ALTER SHARE ... ADD ACCOUNTS`.
4. **Côté consommateur** : `CREATE DATABASE ... FROM SHARE`, une seule base par partage, puis `GRANT IMPORTED PRIVILEGES ON DATABASE`.
5. **Base importée** : lecture seule ; ni clonage, ni Time Travel, ni réplication.
6. **Un nouvel objet n'est partagé qu'après un `GRANT ... TO SHARE`.**
7. **Compte lecteur** : pour un tiers sans compte Snowflake ; `CREATE MANAGED ACCOUNT ... TYPE = READER` ; calcul payé par le fournisseur ; 75 comptes par défaut ; même édition et même région que le fournisseur ; aucune écriture de données.
8. **Vues et UDF sécurisées** pour le partage ; filtrage par consommateur avec `CURRENT_ACCOUNT()`.
9. **Partage direct : même région.** Autre région ou autre cloud : annonce avec Cross-Cloud Auto-Fulfillment, ou réplication puis partage.
10. **Business Critical vers une édition inférieure** : bloqué par défaut ; privilège `OVERRIDE SHARE RESTRICTIONS` et `SHARE_RESTRICTIONS = FALSE`.
11. **Annonce (listing)** : privée, publique (Marketplace) ou interne à l'organisation ; gratuite, essai limité (1 à 90 jours) ou payante.
12. **Data Exchange** : place de marché privée, membres invités, activation par le support.
13. **Réplication** : entre comptes d'une même organisation ; copie secondaire en lecture seule ; activée par l'administrateur de l'organisation.
14. **Groupe de réplication** : lecture seule. **Groupe de bascule** : promouvable avec `ALTER FAILOVER GROUP ... PRIMARY`, exécuté dans le compte cible (Business Critical).
15. **Partage, réplication, clonage** : accès sans copie vers un autre compte ; copie tenue à jour dans un autre compte ; copie modifiable dans le même compte.

---

## Les confusions classiques

| On confond | La différence en une ligne |
|---|---|
| Time Travel et Fail-safe | l'utilisateur restaure lui-même ; seul Snowflake récupère, pendant 7 jours |
| Transitoire et temporaire | l'une dure jusqu'à suppression, l'autre jusqu'à la fin de la session ; aucune n'a de Fail-safe |
| Agrandir et ajouter des clusters | requête plus rapide ; plus d'utilisateurs en même temps |
| `COPY INTO` et Snowpipe | warehouse de l'utilisateur, 64 jours ; calcul sans serveur, 14 jours |
| `ACCOUNT_USAGE` et `INFORMATION_SCHEMA` | 1 an avec latence ; immédiat avec historique court |
| Vue matérialisée et vue sécurisée | performance ; confidentialité |
| Masquage et accès aux lignes | cache des valeurs de colonne ; cache des lignes |
| Compte lecteur et compte consommateur | calcul payé par le fournisseur ; calcul payé par le consommateur |
| Groupe de réplication et groupe de bascule | lecture seule ; promouvable en primaire |

---

[← Plan de préparation](PLAN.md) | [Planning de révision en 3 semaines](PLANNING_REVISION.md) | [← Sommaire du cours](../README.md)
