# 12. Architecture de Snowflake : couches, éditions, objets, warehouses et facturation

[← Retour au sommaire](README.md) | [← Précédent](11-chargement-stage-copy.md) | [Suivant →](13-stockage-protection.md)

## Vue d'ensemble

Les chapitres précédents ont créé un warehouse, une base, des rôles et chargé des fichiers. Ce chapitre prend du recul : il explique comment Snowflake est construit, et pourquoi cette construction détermine presque tout le reste (ce qui coûte, ce qui est rapide, ce qui est possible selon l'édition).

C'est utile dans le métier pour trois raisons :
- **maîtriser la facture** : savoir ce qui consomme des crédits et ce qui n'en consomme pas ;
- **dimensionner le calcul** : choisir la taille et le nombre de warehouses selon l'usage ;
- **parler le même langage** que les administrateurs : organisation, compte, édition, région.

Ce chapitre et les deux suivants couvrent le domaine 1 de l'examen SnowPro Core COF-C03, « Fonctionnalités et architecture de la plateforme », qui pèse 31 % de la note.

Exemple suivi : `SALES_DB`, `SALES_WH` et le rôle `SALES_ENGINEER` des chapitres 10 et 11.

---

## 1. Les trois couches

### 1.1 L'idée en une image

Imaginez une grande bibliothèque :
- la **réserve** contient tous les livres, rangés une seule fois ;
- les **salles de lecture** sont des pièces qu'on ouvre quand des lecteurs arrivent et qu'on ferme quand ils partent ; on peut en ouvrir plusieurs en même temps, toutes puisent dans la même réserve ;
- l'**accueil** vérifie les cartes, tient le catalogue et indique dans quel rayon chercher.

Snowflake est organisé de la même façon, en trois couches indépendantes :

```
┌──────────────────────────────────────────────────────────────┐
│  SERVICES CLOUD (l'accueil)                                  │
│  authentification, contrôle d'accès, métadonnées,            │
│  analyse et optimisation des requêtes, gestion de l'infra    │
├──────────────────────────────────────────────────────────────┤
│  CALCUL (les salles de lecture)                              │
│  warehouses virtuels : SALES_WH, BI_WH, LOAD_WH...           │
│  indépendants les uns des autres                             │
├──────────────────────────────────────────────────────────────┤
│  STOCKAGE (la réserve)                                       │
│  une seule copie des données, compressée, en colonnes,       │
│  découpée en micro-partitions                                │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 Ce que fait chaque couche

| Couche | Rôle | Ce qu'il faut retenir |
|---|---|---|
| Stockage (*Database Storage*) | conserve les données dans le stockage objet du fournisseur cloud, dans un format interne compressé et en colonnes, découpé en micro-partitions (chapitre 13) | les fichiers ne sont pas accessibles directement : on n'y accède que par des requêtes |
| Calcul (*Compute*) | exécute les requêtes dans des warehouses virtuels, qui sont des grappes de machines | chaque warehouse est indépendant : il ne partage ni processeur ni mémoire avec les autres |
| Services cloud (*Cloud Services*) | coordonne tout : authentification, contrôle d'accès, gestion des métadonnées, analyse et optimisation des requêtes, gestion de l'infrastructure | fonctionne en permanence, sur des machines gérées par Snowflake, sans warehouse de votre part |

### 1.3 Pourquoi cette séparation compte

La documentation décrit cette architecture comme un **hybride** de deux modèles classiques :
- *shared-disk* (disque partagé) : un seul dépôt de données, accessible par tous les nœuds de calcul ;
- *shared-nothing* (rien de partagé) : des grappes de calcul massivement parallèles (MPP), où chaque nœud traite une portion des données.

On parle aussi d'architecture **multi-cluster à données partagées**. Les conséquences pratiques :

1. **Stockage et calcul évoluent séparément.** On peut stocker beaucoup et calculer peu, ou l'inverse. Suspendre un warehouse ne supprime aucune donnée.
2. **Les équipes ne se gênent pas.** Le chargement nocturne sur un warehouse ne ralentit pas les tableaux de bord qui tournent sur un autre, alors que les deux lisent les mêmes tables.
3. **Chaque couche se facture à part** (section 6).

Snowflake est un service entièrement géré (SaaS) : il n'y a ni machine à installer, ni mise à jour à planifier, ni index à reconstruire.

---

## 2. Fournisseurs cloud, régions et organisation

### 2.1 Où tourne un compte

Un compte Snowflake est hébergé chez **un** fournisseur cloud, dans **une** région, choisis à la création du compte :

| Fournisseur | Exemples de régions |
|---|---|
| Amazon Web Services (AWS) | Paris, Francfort, Irlande, Virginie |
| Microsoft Azure | Europe de l'Ouest, France Centre |
| Google Cloud | Belgique, Francfort |

Le choix a trois effets : le prix du crédit et du stockage (ils varient selon la région), la localisation des données (conformité, RGPD) et la disponibilité de certaines fonctionnalités récentes. L'interface et le SQL sont les mêmes partout. Un compte hébergé sur un cloud peut charger des fichiers stockés chez un autre fournisseur, mais le transfert peut alors être facturé (section 6.4).

### 2.2 Organisation et comptes

```
Organisation (ex. : MONENTREPRISE)
├── Compte DEV    (AWS, Paris)
├── Compte PROD   (AWS, Paris)
└── Compte US     (Azure, Virginie)
```

Une **organisation** regroupe les comptes d'une même entreprise. Chaque compte a sa propre édition, sa région, ses utilisateurs et ses bases : rien n'est partagé par défaut entre deux comptes. L'identifiant de compte s'écrit `ORGANISATION-COMPTE` (chapitre 10, section 5.5).

```sql
SELECT CURRENT_ORGANIZATION_NAME(), CURRENT_ACCOUNT_NAME(), CURRENT_REGION();
```

`CURRENT_REGION()` renvoie par exemple `AWS_EU_WEST_3` : le fournisseur, puis la région.

---

## 3. Les éditions

L'édition est un niveau de service choisi pour chaque compte. Chaque édition contient tout ce que propose la précédente, et le prix du crédit augmente avec l'édition.

| Édition | Ce qu'elle ajoute | Pour qui |
|---|---|---|
| **Standard** | toutes les fonctions de base : SQL complet, partage de données, Time Travel de 1 jour maximum, chiffrement automatique, tables dynamiques, étiquettes d'objets | petites équipes, découverte |
| **Enterprise** | Time Travel jusqu'à 90 jours, warehouses multi-cluster, vues matérialisées, service d'optimisation de la recherche (*search optimization*), accélération des requêtes (*query acceleration*), masquage de colonnes, politiques d'accès aux lignes, renouvellement périodique des clés de chiffrement | la plupart des entreprises |
| **Business Critical** | clés gérées par le client (*Tri-Secret Secure*), connectivité privée (AWS PrivateLink, Azure Private Link, Google Private Service Connect), prise en charge des données de santé (PHI) et de paiement (PCI DSS), bascule et retour entre comptes (*failover / failback*) | données réglementées, continuité d'activité |
| **Virtual Private Snowflake (VPS)** | environnement isolé des autres clients : magasin de métadonnées et ressources de calcul dédiés | exigences d'isolation maximale (banques, secteur public) |

Méthode pour répondre à une question d'examen sur les éditions :
- performance ou gouvernance avancée (multi-cluster, vue matérialisée, masquage, 90 jours) → **Enterprise** ;
- sécurité renforcée, réglementation, bascule entre régions → **Business Critical** ;
- isolation physique complète → **VPS**.

Un compte d'essai permet de choisir son édition à l'inscription : choisissez Enterprise pour pouvoir tester les fonctions de ce cours.

---

## 4. La hiérarchie des objets

### 4.1 L'emboîtement

```
Organisation
└── Compte
    ├── Utilisateurs, rôles
    ├── Warehouses
    ├── Moniteurs de ressources, politiques réseau, intégrations, partages (shares)
    └── Bases de données
        └── Schémas
            ├── Tables, vues
            ├── Stages, formats de fichier, pipes
            ├── Séquences
            ├── Fonctions (UDF), procédures stockées
            ├── Streams, tâches
            └── Modèles ML, applications Streamlit, notebooks
```

| Niveau | Objets | À retenir |
|---|---|---|
| Compte | utilisateurs, rôles, warehouses, bases, moniteurs de ressources, politiques réseau, intégrations, partages | un warehouse n'appartient à aucune base : il peut interroger toutes les bases du compte |
| Base | schémas | toute base contient d'office les schémas `PUBLIC` et `INFORMATION_SCHEMA` |
| Schéma | tables, vues, stages, formats de fichier, pipes, séquences, fonctions, procédures, streams, tâches, modèles | un objet de schéma a un nom complet en trois parties |

Le nom complet d'un objet de schéma est `BASE.SCHEMA.OBJET`, par exemple `SALES_DB.RAW_DATA.ORDERS_RAW`. La paire base + schéma s'appelle l'**espace de noms** (*namespace*).

Quelques objets cités par le programme de l'examen :

| Objet | En une phrase | Chapitre |
|---|---|---|
| Stage | zone de dépôt de fichiers, interne ou externe | 11 |
| Format de fichier | description de la structure des fichiers à lire | 11 |
| Pipe | objet qui contient un `COPY INTO` exécuté en continu par Snowpipe | chargement |
| Séquence | générateur de nombres uniques ; l'unicité est garantie, pas l'absence de trous | 6 |
| UDF (*user-defined function*) | fonction écrite par l'utilisateur, qui renvoie une valeur et s'appelle dans un `SELECT` | 14 |
| Procédure stockée | programme appelé avec `CALL`, qui peut exécuter plusieurs instructions | 14 |
| Share (partage) | objet de compte qui donne à un autre compte un accès en lecture à des objets, sans copier les données | partage |
| Modèle ML | modèle d'apprentissage enregistré dans un schéma | 14 |
| Application | application native installée dans le compte | 14 |

### 4.2 Le contexte d'une session

Une session a un contexte : rôle, warehouse, base et schéma courants. Il évite d'écrire le nom complet à chaque requête.

```sql
USE ROLE SALES_ENGINEER;
USE WAREHOUSE SALES_WH;
USE SCHEMA SALES_DB.RAW_DATA;

SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA();
```

Une session peut aussi porter des **variables de session**, qui disparaissent à la fin de la session :

```sql
SET pays = 'France';                                    -- crée la variable
SELECT COUNT(*) FROM ORDERS_RAW WHERE ship_country = $pays;   -- $ pour la lire
SHOW VARIABLES;
UNSET pays;
```

### 4.3 Les paramètres et leur ordre de priorité

Un **paramètre** règle un comportement : durée de conservation des données, délai maximal d'une requête, fuseau horaire. Il existe trois familles :

| Famille | Se règle sur | Exemple |
|---|---|---|
| Paramètre de compte | le compte uniquement | paramètres de sécurité du compte |
| Paramètre de session | compte → utilisateur → session | `TIMEZONE`, `USE_CACHED_RESULT` |
| Paramètre d'objet | compte → objet (warehouse, ou base → schéma → table) | `DATA_RETENTION_TIME_IN_DAYS` |

Règle de priorité : **le réglage le plus précis l'emporte**. Une valeur posée sur la session remplace celle de l'utilisateur, qui remplace celle du compte. Une valeur posée sur une table remplace celle du schéma, puis de la base, puis du compte.

```sql
SHOW PARAMETERS LIKE 'TIMEZONE' IN SESSION;      -- colonne level : d'où vient la valeur
ALTER SESSION SET TIMEZONE = 'Europe/Paris';     -- valable pour cette session seulement
ALTER SESSION UNSET TIMEZONE;                    -- retour à la valeur héritée

SHOW PARAMETERS LIKE 'DATA_RETENTION_TIME_IN_DAYS' IN TABLE SALES_DB.RAW_DATA.ORDERS_RAW;
```

La colonne `level` du résultat indique à quel étage la valeur a été fixée ; si elle est vide, c'est la valeur par défaut.

---

## 5. Les warehouses virtuels

### 5.1 Ce qu'est un warehouse

Un warehouse virtuel est une grappe de machines louée à la seconde pour exécuter des requêtes. Il ne contient aucune donnée. Il est nécessaire pour les `SELECT` sur les tables, les chargements (`COPY INTO`) et les modifications (`INSERT`, `UPDATE`, `DELETE`, `MERGE`).

### 5.2 Tailles et crédits

Chaque taille double la puissance et le coût de la précédente.

| Taille | Crédits par heure | Taille | Crédits par heure |
|---|---|---|---|
| X-Small (`XSMALL`) | 1 | 2X-Large | 32 |
| Small | 2 | 3X-Large | 64 |
| Medium | 4 | 4X-Large | 128 |
| Large | 8 | 5X-Large | 256 |
| X-Large | 16 | 6X-Large | 512 |

Ces valeurs sont celles des warehouses standard de première génération ; les autres types ont leur propre barème (section 5.6).

Règles de facturation :
- la facturation se fait **à la seconde**, avec un **minimum de 60 secondes** à chaque démarrage ;
- un warehouse suspendu ne consomme aucun crédit ;
- un warehouse démarré consomme, qu'il exécute des requêtes ou non.

Exemple : `SALES_WH` en X-Small tourne 15 minutes puis est suspendu. Coût : 1 crédit × 15/60 = 0,25 crédit. S'il démarre pour une requête de 5 secondes puis s'arrête, 60 secondes sont facturées.

Taille par défaut : X-Small avec `CREATE WAREHOUSE` en SQL. Le formulaire de l'interface propose une taille plus grande : vérifiez toujours ce champ.

### 5.3 Suspension et reprise automatiques

```sql
USE ROLE SYSADMIN;

CREATE WAREHOUSE IF NOT EXISTS SALES_WH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60            -- suspension après 60 secondes sans requête
  AUTO_RESUME = TRUE           -- redémarrage automatique à la prochaine requête
  INITIALLY_SUSPENDED = TRUE;  -- ne démarre pas (et ne facture pas) à la création

ALTER WAREHOUSE SALES_WH SUSPEND;      -- arrêt manuel
ALTER WAREHOUSE SALES_WH RESUME;       -- démarrage manuel
SHOW WAREHOUSES LIKE 'SALES_WH';       -- colonnes state, size, auto_suspend
```

| Usage | Réglage de `AUTO_SUSPEND` conseillé | Pourquoi |
|---|---|---|
| Chargements et tâches planifiées | court (60 secondes) | le warehouse ne sert qu'entre deux lots |
| Requêtes ponctuelles, développement | quelques minutes | éviter les arrêts et redémarrages incessants |
| Tableaux de bord | plus long (une dizaine de minutes) | conserver le cache du warehouse (section 7) |

### 5.4 Agrandir ou multiplier : deux réponses à deux problèmes

| Problème | Réponse | Nom | Commande |
|---|---|---|---|
| Une requête est lente parce qu'elle est lourde (gros volumes, jointures complexes) | augmenter la **taille** | *scale up* (redimensionner) | `ALTER WAREHOUSE ... SET WAREHOUSE_SIZE = 'LARGE'` |
| Les requêtes font la queue parce qu'il y a beaucoup d'utilisateurs en même temps | augmenter le **nombre de clusters** | *scale out* (multi-cluster) | `MAX_CLUSTER_COUNT = 3` |

```sql
ALTER WAREHOUSE SALES_WH SET WAREHOUSE_SIZE = 'MEDIUM';
```

Le changement de taille ne touche pas les requêtes en cours : elles se terminent sur l'ancienne taille, et seules les nouvelles requêtes profitent de la nouvelle. Une taille plus grande n'accélère pas forcément une petite requête simple.

### 5.5 Le multi-cluster en bref

Un warehouse **multi-cluster** (édition Enterprise ou supérieure) contient plusieurs clusters de la même taille. Il améliore la **concurrence**, pas la vitesse d'une requête isolée.

```sql
CREATE WAREHOUSE IF NOT EXISTS BI_WH
  WAREHOUSE_SIZE = 'SMALL'
  MIN_CLUSTER_COUNT = 1
  MAX_CLUSTER_COUNT = 3
  SCALING_POLICY = 'STANDARD'
  AUTO_SUSPEND = 600
  AUTO_RESUME = TRUE;
```

| Mode | Réglage | Comportement |
|---|---|---|
| Maximisé (*maximized*) | minimum = maximum (supérieur à 1) | tous les clusters démarrent ensemble : capacité constante |
| Mise à l'échelle automatique (*auto-scale*) | minimum < maximum | Snowflake ajoute et retire des clusters selon la charge |

| Politique de mise à l'échelle | Priorité | Démarre un cluster quand |
|---|---|---|
| `STANDARD` (défaut) | éviter les files d'attente | une requête est mise en attente, ou Snowflake estime que les clusters en service sont saturés |
| `ECONOMY` | économiser les crédits | la charge suffit à occuper le nouveau cluster pendant au moins 6 minutes |

Coût : crédits de la taille × nombre de clusters en service. Un warehouse Medium (4 crédits par heure) avec 3 clusters actifs consomme 12 crédits par heure.

### 5.6 Les types de warehouses

| Type | Pour quoi | Création |
|---|---|---|
| Standard, 1re génération (Gen1) | usage général | `WAREHOUSE_TYPE = 'STANDARD'` (type par défaut) avec `GENERATION = '1'` |
| Standard, 2e génération (Gen2) | même usage, matériel plus rapide et optimisations pour `DELETE`, `UPDATE`, `MERGE` et les lectures de tables | `GENERATION = '2'` (ou `RESOURCE_CONSTRAINT = STANDARD_GEN_2`) ; selon la documentation actuelle, c'est la génération par défaut là où Gen2 est disponible |
| Optimisé pour Snowpark (*Snowpark-optimized*) | traitements gourmands en mémoire : entraînement de modèles dans des procédures stockées ou des UDF | `WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED'` |

Les warehouses optimisés pour Snowpark offrent par défaut 16 fois plus de mémoire par nœud qu'un warehouse standard ; ils coûtent plus cher et démarrent plus lentement. Les warehouses Gen2 n'existent pas dans toutes les régions ni dans les tailles 5X-Large et 6X-Large. Selon la région, un warehouse standard créé sans précision peut être de génération 1 ou 2 : `SHOW WAREHOUSES` l'indique.

### 5.7 Quel warehouse pour quel usage

| Usage | Conseil |
|---|---|
| Chargement de fichiers | une petite taille suffit le plus souvent : le débit dépend surtout du nombre et de la taille des fichiers ; warehouse dédié |
| Requêtes ponctuelles d'exploration | taille petite à moyenne, suspension rapide |
| Tableaux de bord, nombreux utilisateurs | multi-cluster en mise à l'échelle automatique, suspension plus longue pour garder le cache |
| Requêtes complexes sur gros volumes | taille plus grande |
| Équipes différentes | un warehouse par équipe ou par usage : pas de gêne mutuelle, coûts attribuables |

Bonne pratique de la documentation : regrouper sur un même warehouse des requêtes de nature comparable, ce qui rend le dimensionnement et l'analyse plus simples.

---

## 6. Le modèle de facturation

La facture a quatre lignes. Le **crédit** est l'unité de consommation du calcul ; son prix en euros dépend de l'édition, de la région et du contrat.

### 6.1 Le calcul : trois sources de crédits

| Source | Ce qui consomme | Facturation |
|---|---|---|
| Warehouses virtuels | requêtes, chargements, modifications de données | à la seconde, minimum 60 secondes, selon la taille |
| Fonctions sans serveur (*serverless*) | calcul géré par Snowflake, sans warehouse à vous : Snowpipe, maintenance des vues matérialisées, clustering automatique, optimisation de la recherche, réplication | selon le temps de calcul réellement utilisé |
| Services cloud | authentification, métadonnées, optimisation des requêtes | voir la règle des 10 % ci-dessous |

### 6.2 La règle des 10 % des services cloud

Les services cloud ne sont facturés que si leur consommation **quotidienne** dépasse **10 % de la consommation quotidienne des warehouses**. Seul le dépassement est facturé.

| Jour | Crédits warehouses | Crédits services cloud | Seuil (10 %) | Facturé pour les services cloud |
|---|---|---|---|---|
| Lundi | 100 | 8 | 10 | 0 |
| Mardi | 100 | 14 | 10 | 4 |

Le calcul est fait chaque jour, en heure UTC. Dans la plupart des comptes, cette ligne vaut zéro.

### 6.3 Le stockage

Le stockage est facturé à un **tarif fixe par téraoctet et par mois**, calculé sur la **moyenne quotidienne** du volume, **après compression**. Ce volume comprend :
- les données des tables ;
- les fichiers déposés dans les stages internes ;
- l'historique conservé pour le Time Travel et le Fail-safe (chapitre 13) ;
- les données propres aux clones, c'est-à-dire ce qui a changé depuis le clonage.

Le tarif dépend de la région et du mode d'achat : à la demande (*On Demand*, sans engagement, plus cher) ou par capacité (*Capacity*, crédits achetés d'avance).

### 6.4 Le transfert de données

| Mouvement | Facturé ? |
|---|---|
| Entrée de données dans Snowflake (*ingress*) | non |
| Sortie vers la même région du même fournisseur | non |
| Sortie vers une autre région ou un autre fournisseur (*egress*) : export avec `COPY INTO <emplacement>`, réplication, fonctions externes | oui, au volume |

### 6.5 Voir sa consommation

```sql
USE ROLE ACCOUNTADMIN;

-- Crédits par warehouse sur 7 jours (vue mise à jour avec quelques heures de retard)
SELECT warehouse_name,
       SUM(credits_used_compute)        AS credits_calcul,
       SUM(credits_used_cloud_services) AS credits_services_cloud
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE start_time >= DATEADD(DAY, -7, CURRENT_TIMESTAMP())
GROUP BY warehouse_name
ORDER BY credits_calcul DESC;
```

Le chapitre 9 détaille le suivi des coûts et les moniteurs de ressources.

---

## 7. Vue d'ensemble des caches

Snowflake évite de refaire un travail déjà fait grâce à trois caches, un par couche.

| Cache | Couche | Contenu | Durée de vie | Warehouse nécessaire ? |
|---|---|---|---|---|
| Cache de métadonnées | services cloud | nombre de lignes, minimum, maximum et nombre de valeurs distinctes par colonne et par micro-partition | permanent, tenu à jour | non |
| Cache de résultats | services cloud | le résultat complet de chaque requête exécutée | 24 heures, prolongées à chaque réutilisation, 31 jours au maximum | non |
| Cache du warehouse (disque local) | calcul | les données de tables lues récemment par ce warehouse | tant que le warehouse est démarré ; **perdu à la suspension** | oui |

Conditions pour que le cache de résultats serve : la requête est **identique au caractère près** (une différence de majuscules ou d'alias suffit à l'empêcher), les données n'ont pas changé, la requête ne contient pas de fonction dont le résultat varie à chaque appel (`RANDOM`, `UUID_STRING`...), et le rôle a les droits nécessaires. Le résultat peut être réutilisé par un autre utilisateur qui remplit ces conditions.

```sql
SELECT COUNT(*) FROM SALES_DB.RAW_DATA.ORDERS_RAW;        -- répondu par les métadonnées

SELECT ship_country, SUM(total_amount) FROM SALES_DB.RAW_DATA.ORDERS_RAW GROUP BY 1;
SELECT ship_country, SUM(total_amount) FROM SALES_DB.RAW_DATA.ORDERS_RAW GROUP BY 1;
-- la seconde exécution est quasi instantanée : cache de résultats

ALTER SESSION SET USE_CACHED_RESULT = FALSE;              -- le désactiver pour mesurer une vraie durée
```

Le compromis de la suspension automatique vient du troisième cache : suspendre vite économise des crédits, mais vide le cache du warehouse, et les premières requêtes après la reprise sont plus lentes.

---

## 8. Interfaces et outils

| Outil | Ce que c'est | Usage |
|---|---|---|
| **Snowsight** | l'interface web : feuilles SQL, notebooks, tableaux de bord, chargement de fichiers, suivi des requêtes et des coûts, administration | travail interactif |
| **Snowflake CLI** (commande `snow`) | client en ligne de commande, libre (*open source*), conçu pour les développeurs : exécuter du SQL, déployer des applications Streamlit, des applications natives, du code Snowpark, gérer des stages | scripts, intégration continue |
| **SnowSQL** | ancien client en ligne de commande, limité au SQL ; Snowflake n'y ajoute plus de nouveautés | à connaître de nom |
| **Extension Visual Studio Code** | écrire et exécuter du SQL depuis l'éditeur, parcourir les objets, déposer des fichiers sur un stage, déboguer du code Snowpark Python | développement sur le poste |
| **Pilotes** (*drivers*) | JDBC, ODBC, Python, Node.js, Go, .NET, PHP | connecter un programme ou un outil de BI |
| **Connecteurs** | Kafka, Spark | échanger des données avec ces systèmes |
| **API SQL REST** | exécuter des requêtes par appels HTTP | intégration sans pilote |

```bash
# Snowflake CLI : exécuter une requête depuis le terminal
snow sql -q "SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE();" --connection sales
```

`--connection sales` désigne une connexion enregistrée dans le fichier de configuration de l'outil (compte, utilisateur, clé privée du chapitre 10).

---

## 9. Pièges fréquents

| Confusion | La réalité |
|---|---|
| « Un warehouse stocke des données » | il ne fait que calculer ; les données sont dans la couche de stockage |
| « Suspendre le warehouse rend les tables inaccessibles » | les tables restent là ; avec `AUTO_RESUME`, la requête suivante redémarre le warehouse |
| « Une taille plus grande règle les files d'attente » | les files d'attente dues au nombre d'utilisateurs se règlent par le multi-cluster ; la taille règle les requêtes lourdes |
| « Le multi-cluster accélère ma requête » | il augmente le nombre de requêtes servies en même temps, pas la vitesse d'une requête |
| « Les services cloud sont gratuits » | ils sont facturés au-delà de 10 % de la consommation quotidienne des warehouses |
| « Le cache de résultats dépend du warehouse » | il est dans la couche des services cloud et survit à la suspension ; c'est le cache du warehouse qui est perdu |
| « Une requête de 5 secondes coûte 5 secondes » | 60 secondes au minimum si elle a provoqué le démarrage du warehouse |
| « Le stockage est facturé sur la taille des fichiers chargés » | il est facturé sur le volume compressé, en moyenne quotidienne |
| « Les données de deux comptes de la même organisation sont communes » | chaque compte est isolé ; il faut un partage ou une réplication |
| « Le paramètre du compte s'applique toujours » | le réglage le plus précis l'emporte (session, table) |

---

## 10. À retenir pour la certification

- Trois couches : **stockage**, **calcul**, **services cloud**. Architecture hybride *shared-disk* / *shared-nothing*, dite multi-cluster à données partagées.
- Les services cloud assurent l'authentification, le contrôle d'accès, les métadonnées, l'analyse et l'optimisation des requêtes, la gestion de l'infrastructure.
- Trois fournisseurs : AWS, Azure, Google Cloud. Un compte = un fournisseur + une région.
- Quatre éditions : Standard, Enterprise, Business Critical, Virtual Private Snowflake.
- Enterprise : Time Travel jusqu'à 90 jours, multi-cluster, vues matérialisées, optimisation de la recherche, accélération des requêtes, masquage de colonnes, politiques d'accès aux lignes.
- Business Critical : Tri-Secret Secure, connectivité privée, données PHI et PCI DSS, bascule entre comptes.
- Tailles de X-Small (1 crédit par heure) à 6X-Large (512), en doublant à chaque taille.
- Facturation à la seconde, minimum 60 secondes à chaque démarrage.
- *Scale up* = taille = requêtes complexes. *Scale out* = clusters = concurrence.
- Multi-cluster : édition Enterprise ; modes maximisé et automatique ; politiques `STANDARD` (défaut) et `ECONOMY`.
- Types de warehouses : standard (Gen1, Gen2) et optimisé pour Snowpark (mémoire).
- Services cloud facturés seulement au-delà de 10 % des crédits quotidiens des warehouses.
- Stockage : tarif par téraoctet et par mois, moyenne quotidienne, données compressées, Time Travel et Fail-safe compris.
- Transfert : l'entrée est gratuite ; la sortie vers une autre région ou un autre cloud est payante.
- Cache de résultats : 24 heures, 31 jours au maximum, sans warehouse. Cache du warehouse : perdu à la suspension. Cache de métadonnées : répond à `COUNT(*)`, `MIN`, `MAX` sans warehouse.
- Paramètres : compte, session, objet ; le niveau le plus précis l'emporte.
- Nom complet d'un objet : `BASE.SCHEMA.OBJET`. Les warehouses, utilisateurs, rôles et bases sont des objets de compte.
- Snowflake CLI (`snow`) est le client en ligne de commande à privilégier ; SnowSQL est l'ancien.

---

## 11. Atelier pratique : observer l'architecture (40 minutes)

Objectif : voir de ses yeux la séparation entre calcul et stockage, les trois caches et le coût d'un warehouse. Jeu de données : `Data/airbnb/reviews.csv` (environ 8 Mo, deux colonnes `listing_id` et `date`).

### Étape 1 — Charger le fichier (10 minutes)

Dans Snowsight, avec le rôle `SALES_ENGINEER`, chargez `Data/airbnb/reviews.csv` dans une nouvelle table `SALES_DB.RAW_DATA.AIRBNB_REVIEWS` par l'assistant de chargement (méthode du chapitre 7) ou par `PUT` et `COPY INTO` (chapitre 11). Nommez la seconde colonne `review_date`.

### Étape 2 — Le cache de métadonnées (5 minutes)

```sql
USE ROLE SALES_ENGINEER;
USE SCHEMA SALES_DB.RAW_DATA;
ALTER WAREHOUSE SALES_WH SUSPEND;          -- une erreur ici signifie qu'il était déjà suspendu

SELECT COUNT(*), MIN(review_date), MAX(review_date) FROM AIRBNB_REVIEWS;
SHOW WAREHOUSES LIKE 'SALES_WH';           -- colonne state
```

Le warehouse a-t-il redémarré ? Ouvrez le profil de la requête (*Query Profile*) : quel opérateur apparaît ?

### Étape 3 — Le cache de résultats (10 minutes)

```sql
SELECT YEAR(review_date) AS annee, COUNT(*) AS nb_avis
FROM AIRBNB_REVIEWS GROUP BY 1 ORDER BY 1;
```

1. Exécutez la requête deux fois de suite et comparez les durées. Dans le profil de la seconde, repérez la mention de réutilisation du résultat.
2. Suspendez le warehouse, puis relancez la requête : redémarre-t-il ?
3. Remplacez `annee` par `ANNEE_AVIS` et relancez : le cache sert-il encore ?
4. Désactivez le cache (`ALTER SESSION SET USE_CACHED_RESULT = FALSE;`) et relancez.

### Étape 4 — La taille du warehouse (10 minutes)

```sql
USE ROLE SYSADMIN;                         -- ou le rôle propriétaire de SALES_WH
ALTER WAREHOUSE SALES_WH SET WAREHOUSE_SIZE = 'SMALL';

USE ROLE SALES_ENGINEER;
SELECT listing_id, COUNT(*) AS nb, MIN(review_date), MAX(review_date)
FROM AIRBNB_REVIEWS GROUP BY 1 ORDER BY nb DESC LIMIT 20;

USE ROLE SYSADMIN;
ALTER WAREHOUSE SALES_WH SET WAREHOUSE_SIZE = 'XSMALL';   -- revenir à la taille initiale
```

Comparez les durées en X-Small et en Small, cache de résultats désactivé.

### Étape 5 — Lire l'historique et nettoyer (5 minutes)

```sql
USE ROLE SALES_ENGINEER;
SELECT query_text, warehouse_size, total_elapsed_time, bytes_scanned
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY_BY_SESSION())
ORDER BY start_time DESC LIMIT 15;

ALTER SESSION UNSET USE_CACHED_RESULT;
DROP TABLE AIRBNB_REVIEWS;                 -- sauf si vous la gardez pour le chapitre 13
```

### Questions de réflexion

1. Pourquoi le `COUNT(*)` de l'étape 2 n'a-t-il pas eu besoin du warehouse ?
2. À l'étape 4, le passage en Small a-t-il divisé la durée par deux ? Qu'en concluez-vous pour une petite table ?
3. Votre équipe lance 40 tableaux de bord chaque matin à 9 h et les requêtes font la queue. Que proposez-vous, et quelle édition faut-il ?
4. Un warehouse Large tourne 8 heures par jour ouvré sans suspension, pour 30 minutes d'usage réel. Combien de crédits par jour ? Combien avec une suspension après 60 secondes ?
5. Dans quel cas raccourcir `AUTO_SUSPEND` peut-il dégrader les temps de réponse ?

## ✅ Points de vérification
- [ ] Je sais citer les trois couches et ce que fait chacune
- [ ] Je sais associer une fonctionnalité à l'édition minimale qui la propose
- [ ] Je sais calculer le coût en crédits d'un warehouse selon sa taille, sa durée et son nombre de clusters
- [ ] Je distingue *scale up* et *scale out* et je sais lequel choisir
- [ ] Je sais expliquer la règle des 10 % des services cloud
- [ ] J'ai observé le cache de métadonnées et le cache de résultats sur mon compte
- [ ] Je sais dire quel cache est perdu à la suspension du warehouse
- [ ] Je sais lire d'où vient la valeur d'un paramètre avec `SHOW PARAMETERS`

## Documentation officielle
- [Concepts clés et architecture](https://docs.snowflake.com/en/user-guide/intro-key-concepts)
- [Fournisseurs cloud pris en charge](https://docs.snowflake.com/en/user-guide/intro-cloud-platforms)
- [Éditions de Snowflake](https://docs.snowflake.com/en/user-guide/intro-editions)
- [Vue d'ensemble des warehouses](https://docs.snowflake.com/en/user-guide/warehouses-overview)
- [Warehouses multi-cluster](https://docs.snowflake.com/en/user-guide/warehouses-multicluster)
- [Considérations sur les warehouses](https://docs.snowflake.com/en/user-guide/warehouses-considerations)
- [Warehouses standard de 2e génération](https://docs.snowflake.com/en/user-guide/warehouses-gen2)
- [Warehouses optimisés pour Snowpark](https://docs.snowflake.com/en/user-guide/warehouses-snowpark-optimized)
- [Comprendre le coût du calcul](https://docs.snowflake.com/en/user-guide/cost-understanding-compute)
- [Comprendre le coût du stockage](https://docs.snowflake.com/en/user-guide/cost-understanding-data-storage)
- [Comprendre le coût du transfert](https://docs.snowflake.com/en/user-guide/cost-understanding-data-transfer)
- [Résultats de requêtes conservés](https://docs.snowflake.com/en/user-guide/querying-persisted-results)
- [Paramètres](https://docs.snowflake.com/en/sql-reference/parameters)
- [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index)
- [Extension Visual Studio Code](https://docs.snowflake.com/en/user-guide/vscode-ext)

---

[← Retour au sommaire](README.md) | [← Précédent](11-chargement-stage-copy.md) | [Suivant →](13-stockage-protection.md)
