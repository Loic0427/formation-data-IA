# 15. Authentification et gouvernance des données

[← Retour au sommaire](README.md) | [← Précédent](14-ia-applications.md) | [Suivant →](16-snowpipe-export-connectivite.md)

## Vue d'ensemble

Le [chapitre 10](10-securite.md) répond à la question « que peut faire un rôle ? ». Ce chapitre répond aux questions qui l'entourent :

- **Qui se connecte, et comment le prouve-t-il ?** Méthodes d'authentification, politiques réseau, de session et de mot de passe.
- **Comment les données sont-elles protégées ?** Chiffrement, masquage des colonnes, filtrage des lignes, étiquettes (tags) et classification.
- **Qui a fait quoi ?** Audit avec `ACCOUNT_USAGE` et `INFORMATION_SCHEMA`.
- **Combien cela coûte-t-il, et comment le limiter ?** Resource monitors et budgets.
- **Où se règle un comportement ?** Paramètres de compte, d'utilisateur, de session et d'objet.

Dans le métier, un Data Engineer ne décide pas seul de la politique de sécurité, mais c'est lui qui l'applique : il crée l'utilisateur de service d'un outil, masque une colonne d'e-mails avant d'ouvrir une table aux analystes, retrouve dans l'historique qui a lu une table sensible. À l'examen SnowPro Core, ces sujets forment le domaine 2 « Gestion du compte et gouvernance des données » (20 % des questions), avec le contrôle d'accès du chapitre 10.

Exemple suivi : `SALES_DB`, `SALES_WH`, les rôles `SALES_ENGINEER` et `SALES_ANALYST`, l'utilisateur de service `SALES_ETL_SVC`.

Trois mots reviennent dans tout le chapitre :

| Mot | Sens |
|---|---|
| Authentification | prouver son identité (qui êtes-vous ?) |
| Autorisation | vérifier les droits du rôle actif (qu'avez-vous le droit de faire ?) : chapitre 10 |
| Politique (*policy*) | un objet Snowflake qui contient une règle, et que l'on attache ensuite à un compte, un utilisateur, une table ou une colonne |

---

## 1. S'authentifier : prouver son identité

### 1.1 Les méthodes disponibles

Un humain et un programme ne se connectent pas de la même façon. Un humain peut saisir un code sur son téléphone ; un script qui tourne la nuit ne le peut pas.

| Méthode | Principe | Pour qui | À retenir |
|---|---|---|---|
| Mot de passe + authentification multifacteur (MFA) | un mot de passe, puis une seconde preuve (application, passkey, Duo) | humains | le mot de passe seul n'est plus considéré comme suffisant |
| SSO fédéré | la connexion est déléguée à l'annuaire de l'entreprise (fournisseur d'identité) | humains | protocole SAML 2.0 ; Snowflake est le fournisseur de service |
| Paire de clés | l'outil signe un jeton avec sa clé privée ; Snowflake vérifie avec la clé publique | outils, scripts | détaillée au [chapitre 10, section 5](10-securite.md) ; deux clés possibles pour la rotation |
| OAuth | une application obtient un jeton d'accès au nom de l'utilisateur, sans connaître son mot de passe | applications, outils BI | Snowflake OAuth ou External OAuth, configurés par une intégration de sécurité |
| Jeton d'accès programmatique (PAT) | un jeton à durée limitée, généré dans Snowflake, utilisé à la place d'un mot de passe | scripts, appels d'API REST | expire (15 jours par défaut, 365 au maximum) ; affiché une seule fois |

### 1.2 Mot de passe et authentification multifacteur

L'authentification multifacteur (MFA, *multi-factor authentication*) demande deux preuves : quelque chose que l'on sait (le mot de passe) et quelque chose que l'on possède (un téléphone, une clé de sécurité).

- Trois secondes preuves sont acceptées : une **passkey**, une **application d'authentification** qui génère un code temporaire (TOTP), ou **Duo**.
- La MFA concerne les **utilisateurs humains qui se connectent par mot de passe**. Sur les comptes récents, l'inscription à la MFA est exigée par défaut pour ces utilisateurs.
- Un utilisateur de type `SERVICE` n'a ni mot de passe ni MFA : il utilise une paire de clés, OAuth ou un jeton programmatique.
- L'obligation se règle avec une **politique d'authentification** (*authentication policy*), qui précise les méthodes autorisées et l'exigence de MFA.

```sql
-- Dépannage : un utilisateur a perdu son téléphone, on suspend la MFA pendant 30 minutes
ALTER USER ALICE SET MINS_TO_BYPASS_MFA = 30;
```

Le paramètre de compte `ALLOW_CLIENT_MFA_CACHING` permet aux pilotes de garder le jeton MFA en cache (jusqu'à quatre heures) pour ne pas redemander le code à chaque connexion.

### 1.3 SSO fédéré

Avec l'authentification fédérée, l'utilisateur clique sur « Se connecter avec l'entreprise » : il est envoyé vers l'annuaire de son entreprise (Okta, Microsoft Entra ID...), s'y authentifie, puis revient dans Snowflake déjà connecté.

| Rôle | Qui | Fait quoi |
|---|---|---|
| Fournisseur d'identité (IdP) | l'annuaire de l'entreprise | détient les identifiants et authentifie l'utilisateur |
| Fournisseur de service (SP) | Snowflake | fait confiance à la réponse de l'IdP et ouvre la session |

La configuration se fait par une **intégration de sécurité** de type SAML2. Les droits restent gérés dans Snowflake par les rôles : le SSO dit qui vous êtes, pas ce que vous pouvez faire. Le provisionnement automatique des utilisateurs et des rôles depuis l'annuaire s'appelle SCIM.

### 1.4 OAuth

OAuth sert quand une application (un outil de tableaux de bord par exemple) doit agir au nom d'un utilisateur. L'application ne voit jamais le mot de passe : elle reçoit un **jeton d'accès** de courte durée.

- **Snowflake OAuth** : Snowflake délivre lui-même les jetons.
- **External OAuth** : un serveur d'autorisation externe (Okta, Microsoft Entra ID...) délivre les jetons.

Dans les deux cas, on crée une intégration de sécurité (`CREATE SECURITY INTEGRATION`).

### 1.5 Jetons d'accès programmatiques

Un jeton d'accès programmatique (PAT, *programmatic access token*) remplace un mot de passe dans un pilote, un outil en ligne de commande ou un appel d'API REST.

```sql
ALTER USER SALES_ETL_SVC ADD PROGRAMMATIC ACCESS TOKEN JETON_API
  ROLE_RESTRICTION = 'SALES_ENGINEER'    -- le jeton ne peut utiliser que ce rôle
  DAYS_TO_EXPIRY = 30;
```

- Le secret du jeton n'est affiché **qu'une seule fois**, à la création.
- Pour un utilisateur de service, `ROLE_RESTRICTION` est obligatoire, et par défaut l'utilisateur doit être couvert par une politique réseau (section 2).
- Un utilisateur peut avoir au plus 15 jetons actifs.

---

## 2. Politiques réseau : d'où a-t-on le droit de se connecter

Une politique réseau (*network policy*) limite les adresses depuis lesquelles on peut joindre Snowflake. Sans politique, le compte est joignable depuis tout Internet (l'authentification reste nécessaire).

On décrit d'abord les adresses dans une **règle réseau** (*network rule*), puis on range les règles dans une politique en liste autorisée ou en liste bloquée.

```sql
USE ROLE SECURITYADMIN;

-- La règle : les adresses du bureau (objet de schéma)
CREATE NETWORK RULE SALES_DB.ANALYTICS.BUREAU_RULE
  TYPE = IPV4
  MODE = INGRESS                          -- trafic entrant vers Snowflake
  VALUE_LIST = ('203.0.113.0/24');

-- La politique : n'autoriser que cette règle (objet de compte)
CREATE NETWORK POLICY SALES_BUREAU_POLICY
  ALLOWED_NETWORK_RULE_LIST = ('SALES_DB.ANALYTICS.BUREAU_RULE');

-- L'activer pour un seul utilisateur
ALTER USER SALES_ETL_SVC SET NETWORK_POLICY = SALES_BUREAU_POLICY;

-- Ou pour tout le compte (à ne pas faire sans réfléchir)
-- ALTER ACCOUNT SET NETWORK_POLICY = SALES_BUREAU_POLICY;
```

Règles à connaître :

- Une politique s'active à trois niveaux : **compte**, **utilisateur**, **intégration de sécurité**. Le niveau le plus précis l'emporte : la politique d'un utilisateur remplace celle du compte pour cet utilisateur.
- Une seule politique est active par niveau à un instant donné.
- Si une adresse figure à la fois dans la liste autorisée et dans la liste bloquée, **la liste bloquée l'emporte**.
- Snowflake refuse d'activer une politique qui exclurait votre adresse actuelle : on ne peut pas s'enfermer dehors par erreur.
- Il faut le rôle `SECURITYADMIN` (ou supérieur), ou un rôle qui a le privilège `CREATE NETWORK POLICY`.
- L'ancienne syntaxe, avec `ALLOWED_IP_LIST` et `BLOCKED_IP_LIST` directement dans la politique, existe toujours et apparaît encore dans des questions d'examen.

---

## 3. Politiques de session et de mot de passe

### 3.1 Politique de session

Une session inactive finit par expirer : il faut se reconnecter. Par défaut, le délai d'inactivité est de **240 minutes (4 heures)** pour les sessions des programmes, et de 1 080 minutes (18 heures) pour Snowsight. Une politique de session (*session policy*) change ces délais.

```sql
CREATE SESSION POLICY SALES_DB.ANALYTICS.SESSION_COURTE
  SESSION_IDLE_TIMEOUT_MINS = 30          -- pilotes, connecteurs, CLI
  SESSION_UI_IDLE_TIMEOUT_MINS = 30;      -- interface Snowsight

ALTER ACCOUNT SET SESSION POLICY SALES_DB.ANALYTICS.SESSION_COURTE;
```

Le délai se règle entre 5 minutes et 24 heures. Si une politique est posée sur le compte et une autre sur un utilisateur, celle de l'utilisateur l'emporte.

### 3.2 Politique de mot de passe

Une politique de mot de passe (*password policy*) fixe les exigences : longueur, types de caractères, durée de vie, nombre d'essais.

```sql
CREATE PASSWORD POLICY SALES_DB.ANALYTICS.MDP_STRICT
  PASSWORD_MIN_LENGTH = 16
  PASSWORD_MIN_SPECIAL_CHARS = 1
  PASSWORD_MAX_AGE_DAYS = 90              -- changement obligatoire tous les 90 jours
  PASSWORD_MAX_RETRIES = 5                -- 5 essais ratés...
  PASSWORD_LOCKOUT_TIME_MINS = 15         -- ...bloquent l'utilisateur 15 minutes
  PASSWORD_HISTORY = 5;                   -- interdit de reprendre les 5 derniers mots de passe

ALTER ACCOUNT SET PASSWORD POLICY SALES_DB.ANALYTICS.MDP_STRICT;
```

Les valeurs 90 jours, 5 essais, 15 minutes et 5 mots de passe mémorisés sont aussi les valeurs par défaut d'une politique créée sans option.

### 3.3 Résumé des politiques de connexion

| Politique | Règle | S'attache à |
|---|---|---|
| Authentification | méthodes autorisées, exigence de MFA | compte, utilisateur |
| Réseau | adresses d'origine autorisées ou bloquées | compte, utilisateur, intégration de sécurité |
| Session | délai d'inactivité | compte, utilisateur |
| Mot de passe | complexité, durée de vie, blocage | compte, utilisateur |

Dans tous les cas, la politique posée sur l'utilisateur l'emporte sur celle du compte.

---

## 4. Chiffrement

Chiffrer une donnée, c'est la rendre illisible sans la clé. Dans Snowflake, le chiffrement est **toujours actif, dans toutes les éditions, sans rien configurer**.

| Moment | Protection |
|---|---|
| En transit (entre votre poste et Snowflake) | connexion chiffrée par TLS |
| Au repos (fichiers stockés par Snowflake) | chiffrement AES 256 bits |
| Fichiers envoyés sur un stage interne | chiffrés par le client avant l'envoi, puis au repos : chiffrement de bout en bout |

Les clés sont organisées en **hiérarchie à quatre niveaux** : clé racine, clés maîtres de compte, clés maîtres de table, clés de fichier. Chaque clé chiffre les clés du niveau inférieur ; la clé racine est gardée dans un module matériel de sécurité (HSM).

| Mécanisme | Ce qu'il fait | Édition |
|---|---|---|
| Rotation des clés | une clé de plus de 30 jours est retirée et remplacée automatiquement ; elle ne sert plus qu'à déchiffrer | toutes |
| Rechiffrement périodique (*periodic rekeying*) | les données protégées par une clé retirée depuis plus d'un an sont rechiffrées avec une nouvelle clé (`PERIODIC_DATA_REKEYING = TRUE`) | Enterprise |
| Tri-Secret Secure | une clé gérée par le client, dans son propre service de clés cloud, se combine à la clé de Snowflake pour former une clé maîtresse composite | Business Critical |

Avec Tri-Secret Secure, si le client révoque sa clé, Snowflake ne peut plus déchiffrer les données. Le nom vient des trois protections réunies : la clé de Snowflake, la clé du client et l'authentification des utilisateurs.

---

## 5. Gouverner les données

La gouvernance répond à : quelles données sont sensibles, qui peut les voir, et sous quelle forme ? Quatre outils se complètent.

| Outil | Agit sur | Effet | Édition |
|---|---|---|---|
| Masquage dynamique | une colonne | la valeur est cachée ou transformée selon le rôle | Enterprise |
| Politique d'accès par ligne | les lignes d'une table ou d'une vue | certaines lignes sont invisibles selon le rôle | Enterprise |
| Tag | tout objet ou colonne | étiquette descriptive (clé et valeur) pour repérer et suivre | propagation et masquage par tag : Enterprise |
| Classification | les colonnes d'une table | détection automatique des données sensibles, qui pose des tags système | Enterprise |

Les vues sécurisées (*secure views*), qui cachent la définition d'une vue et servent aussi à limiter l'accès aux données, sont traitées au [chapitre 13](13-stockage-protection.md). Elles fonctionnent dans toutes les éditions.

### 5.1 Masquage dynamique des données

Une politique de masquage (*masking policy*) est une petite fonction : elle reçoit la valeur de la colonne et renvoie soit la valeur, soit une version masquée. Elle s'exécute **au moment de la requête**. La donnée stockée n'est jamais modifiée : deux rôles qui lancent la même requête voient deux résultats différents.

```sql
-- La politique : un objet de schéma
CREATE MASKING POLICY SALES_DB.ANALYTICS.MASK_EMAIL AS (val STRING) RETURNS STRING ->
  CASE
    WHEN CURRENT_ROLE() IN ('SALES_ENGINEER') THEN val            -- valeur réelle
    ELSE REGEXP_REPLACE(val, '.+@', '*****@')                      -- *****@email.com
  END;

-- L'attacher à une colonne
ALTER TABLE SALES_DB.ANALYTICS.FIN_CUSTOMERS
  MODIFY COLUMN email SET MASKING POLICY SALES_DB.ANALYTICS.MASK_EMAIL;

-- La retirer
ALTER TABLE SALES_DB.ANALYTICS.FIN_CUSTOMERS MODIFY COLUMN email UNSET MASKING POLICY;
```

Règles à connaître :

- Le type en entrée et le type en sortie doivent être **identiques** (une colonne `STRING` renvoie un `STRING`).
- Une colonne porte **une seule** politique de masquage ; une même politique peut protéger des milliers de colonnes.
- Privilèges : `CREATE MASKING POLICY` sur le schéma pour la créer, `APPLY MASKING POLICY` (sur le compte) pour l'attacher. On peut ainsi séparer celui qui écrit les règles de celui qui possède les tables.
- Le propriétaire de la table est soumis à la politique comme les autres : être propriétaire ne suffit pas pour voir la valeur réelle.
- Le masquage par tag (*tag-based masking*) attache la politique à un tag : toute colonne qui porte ce tag est masquée automatiquement.

### 5.2 Politiques d'accès par ligne

Une politique d'accès par ligne (*row access policy*) est une fonction qui renvoie vrai ou faux pour chaque ligne : si c'est faux, la ligne n'apparaît pas. Elle s'applique aux `SELECT`, mais aussi aux lignes touchées par `UPDATE`, `DELETE` et `MERGE`.

```sql
CREATE ROW ACCESS POLICY SALES_DB.ANALYTICS.RAP_RISQUE AS (risk VARCHAR) RETURNS BOOLEAN ->
  CURRENT_ROLE() = 'SALES_ENGINEER'       -- le rôle outil voit tout
  OR risk = 'LOW';                        -- les autres ne voient que les clients à risque faible

ALTER TABLE SALES_DB.ANALYTICS.FIN_CUSTOMERS
  ADD ROW ACCESS POLICY SALES_DB.ANALYTICS.RAP_RISQUE ON (risk_category);
```

- Une politique d'accès par ligne renvoie toujours un `BOOLEAN`.
- En pratique, la règle s'appuie souvent sur une **table de correspondance** (quel rôle voit quelle région) plutôt que sur des valeurs écrites en dur.
- Quand une table a une politique d'accès par ligne et des politiques de masquage, **la politique d'accès par ligne est évaluée en premier**.
- Une même colonne ne peut pas servir à la fois dans la signature d'une politique d'accès par ligne et dans celle d'une politique de masquage.

### 5.3 Tags et classification

Un tag est une étiquette : un objet de schéma, que l'on attache à un autre objet avec une valeur (texte). Il ne protège rien par lui-même ; il sert à repérer les données sensibles, à suivre les coûts par équipe, ou à déclencher un masquage.

```sql
CREATE TAG SALES_DB.ANALYTICS.SENSIBILITE
  ALLOWED_VALUES 'public', 'interne', 'confidentiel';

ALTER TABLE SALES_DB.ANALYTICS.FIN_CUSTOMERS
  MODIFY COLUMN email SET TAG SALES_DB.ANALYTICS.SENSIBILITE = 'confidentiel';

ALTER WAREHOUSE SALES_WH SET TAG SALES_DB.ANALYTICS.SENSIBILITE = 'interne';

-- Lire le tag d'une colonne
SELECT SYSTEM$GET_TAG('SALES_DB.ANALYTICS.SENSIBILITE',
                      'SALES_DB.ANALYTICS.FIN_CUSTOMERS.EMAIL', 'COLUMN');
```

- Un tag posé sur un objet est **hérité** par les objets qu'il contient : un tag posé sur une table vaut pour ses colonnes, un tag posé sur un schéma vaut pour ses tables.
- Un objet peut porter au plus 50 tags.
- Pour retrouver où un tag est posé : la vue `SNOWFLAKE.ACCOUNT_USAGE.TAG_REFERENCES` ou la fonction `INFORMATION_SCHEMA.TAG_REFERENCES`.

La **classification** des données sensibles analyse le contenu des colonnes et reconnaît les noms, e-mails, numéros de téléphone, etc. Elle pose deux tags système :

| Tag système | Indique | Exemples de valeurs |
|---|---|---|
| `SNOWFLAKE.CORE.SEMANTIC_CATEGORY` | la nature de la donnée | `EMAIL`, `NAME`, `PHONE_NUMBER` |
| `SNOWFLAKE.CORE.PRIVACY_CATEGORY` | son niveau de sensibilité | `IDENTIFIER`, `QUASI_IDENTIFIER`, `SENSITIVE` |

La classification demande l'édition Enterprise et consomme des crédits (calcul serverless).

---

## 6. Auditer : qui a fait quoi

Snowflake enregistre les connexions, les requêtes et les accès aux données. On les lit à deux endroits, qui n'ont pas les mêmes qualités.

### 6.1 ACCOUNT_USAGE contre INFORMATION_SCHEMA

| | `SNOWFLAKE.ACCOUNT_USAGE` | `INFORMATION_SCHEMA` |
|---|---|---|
| Où | un schéma de la base partagée `SNOWFLAKE`, unique pour le compte | un schéma en lecture seule présent dans **chaque** base |
| Périmètre | tout le compte | la base où il se trouve (et les fonctions d'historique) |
| Latence | de 45 minutes à 3 heures selon la vue | aucune : temps réel |
| Historique conservé | 1 an (365 jours) | de 7 jours à 6 mois selon la vue ou la fonction |
| Objets supprimés | inclus (colonne `DELETED`) | absents |
| Accès | `ACCOUNTADMIN` par défaut, puis délégation | selon les droits du rôle actif sur les objets |
| Usage type | audit, coûts, analyse sur plusieurs mois | vérifier tout de suite ce qui vient de se passer |

Latences et durées à connaître :

| Donnée | `ACCOUNT_USAGE` : latence | `ACCOUNT_USAGE` : historique | `INFORMATION_SCHEMA` : historique |
|---|---|---|---|
| `QUERY_HISTORY` | 45 minutes | 1 an | 7 jours |
| `LOGIN_HISTORY` | 2 heures | 1 an | 7 jours |
| `COPY_HISTORY` | 2 heures | 1 an | 14 jours |
| `ACCESS_HISTORY` | 3 heures | 1 an | n'existe pas |

Donner l'accès à `ACCOUNT_USAGE` à un autre rôle qu'`ACCOUNTADMIN` :

```sql
USE ROLE ACCOUNTADMIN;

-- Tout le contenu de la base SNOWFLAKE
GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE SALES_ENGINEER;

-- Ou, plus fin, un rôle de base de données prédéfini
GRANT DATABASE ROLE SNOWFLAKE.GOVERNANCE_VIEWER TO ROLE SALES_ENGINEER;
```

Les rôles de base de données prédéfinis sont `OBJECT_VIEWER`, `USAGE_VIEWER`, `GOVERNANCE_VIEWER` et `SECURITY_VIEWER` : chacun ouvre une partie des vues.

### 6.2 LOGIN_HISTORY : les connexions

```sql
-- Échecs de connexion des 7 derniers jours (jusqu'à 2 heures de retard)
SELECT event_timestamp, user_name, client_ip, reported_client_type,
       first_authentication_factor, second_authentication_factor, error_message
FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
WHERE is_success = 'NO'
  AND event_timestamp > DATEADD(DAY, -7, CURRENT_TIMESTAMP())
ORDER BY event_timestamp DESC;

-- La même information en temps réel, pour un utilisateur
SELECT *
FROM TABLE(INFORMATION_SCHEMA.LOGIN_HISTORY_BY_USER(USER_NAME => 'SALES_ETL_SVC', RESULT_LIMIT => 20));
```

La colonne `second_authentication_factor` montre si la MFA a été utilisée.

### 6.3 QUERY_HISTORY : les requêtes

```sql
-- Les requêtes du rôle analyste sur un mois
SELECT start_time, user_name, role_name, warehouse_name, query_text, total_elapsed_time / 1000 AS secondes
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE role_name = 'SALES_ANALYST'
  AND start_time > DATEADD(DAY, -30, CURRENT_TIMESTAMP())
ORDER BY start_time DESC;

-- Les requêtes de la dernière heure, sans attendre
SELECT query_id, query_text, execution_status
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(
  END_TIME_RANGE_START => DATEADD(HOUR, -1, CURRENT_TIMESTAMP())));
```

Le [chapitre 9](09-monitoring.md) utilise cette vue pour suivre les coûts ; ici, elle sert à l'audit.

### 6.4 ACCESS_HISTORY : les accès aux données

`QUERY_HISTORY` donne le texte de la requête. `ACCESS_HISTORY` donne les **objets et colonnes réellement lus ou modifiés**, même à travers une vue. C'est la vue de l'audit de conformité : « qui a lu la colonne e-mail ce mois-ci ? ». Elle demande l'édition Enterprise.

| Colonne | Contenu |
|---|---|
| `DIRECT_OBJECTS_ACCESSED` | les objets nommés dans la requête (la vue interrogée) |
| `BASE_OBJECTS_ACCESSED` | les objets de base réellement lus (les tables derrière la vue) |
| `OBJECTS_MODIFIED` | les objets écrits, avec la provenance des colonnes (lignage) |
| `POLICIES_REFERENCED` | les politiques de masquage et d'accès par ligne appliquées |

```sql
SELECT ah.query_start_time, ah.user_name, obj.value:objectName::STRING AS objet_lu
FROM SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY ah,
     LATERAL FLATTEN(input => ah.base_objects_accessed) obj
WHERE obj.value:objectName::STRING = 'SALES_DB.ANALYTICS.FIN_CUSTOMERS'
  AND ah.query_start_time > DATEADD(DAY, -7, CURRENT_TIMESTAMP());
```

---

## 7. Maîtriser les coûts : resource monitors et budgets

Le [chapitre 9](09-monitoring.md) crée un resource monitor dans l'interface. Voici la version SQL et les règles précises.

Un **resource monitor** surveille les crédits consommés par des warehouses sur une période et déclenche des actions à des seuils exprimés en pourcentage du quota.

```sql
USE ROLE ACCOUNTADMIN;                    -- seul ACCOUNTADMIN peut créer un resource monitor

CREATE RESOURCE MONITOR SALES_WH_MONITOR WITH
  CREDIT_QUOTA = 20                       -- 20 crédits par période
  FREQUENCY = MONTHLY                     -- remise à zéro chaque mois
  START_TIMESTAMP = IMMEDIATELY
  TRIGGERS
    ON 75  PERCENT DO NOTIFY              -- prévenir
    ON 100 PERCENT DO SUSPEND             -- suspendre après la fin des requêtes en cours
    ON 110 PERCENT DO SUSPEND_IMMEDIATE;  -- suspendre en annulant les requêtes en cours

ALTER WAREHOUSE SALES_WH SET RESOURCE_MONITOR = SALES_WH_MONITOR;
```

| Action | Effet sur les warehouses |
|---|---|
| `NOTIFY` | aucun : une notification est envoyée |
| `SUSPEND` | suspension une fois les requêtes en cours terminées |
| `SUSPEND_IMMEDIATE` | suspension immédiate, les requêtes en cours sont annulées |

- Un monitor se pose au niveau du **compte** (un seul, pour tous les warehouses) ou sur un ou plusieurs **warehouses**. Un warehouse n'a qu'un seul monitor.
- Il ne surveille que les warehouses (et les services cloud dont ils ont besoin). Il **ne contrôle pas les fonctions serverless** (Snowpipe, tâches serverless...) ni les services d'IA.
- Un seuil peut dépasser 100 %, et un warehouse peut consommer un peu plus que le quota avant d'être effectivement suspendu.

Un **budget** fixe une limite de dépense mensuelle pour le compte entier ou pour un groupe d'objets (budget personnalisé), et couvre aussi les fonctions serverless.

| | Resource monitor | Budget |
|---|---|---|
| Surveille | warehouses uniquement | warehouses et fonctions serverless |
| Unité | quota de crédits | limite de dépense mensuelle (mois calendaire) |
| Action | notifier, suspendre | notifier quand la dépense prévue dépassera la limite (e-mail, file cloud, webhook) |
| Peut arrêter un warehouse | oui | pas directement : il faut y associer une procédure stockée |
| Réactivité | suivi des crédits des warehouses | données rafraîchies avec plusieurs heures de délai par défaut |

---

## 8. Paramètres : où se règle un comportement

Un paramètre est un réglage nommé (fuseau horaire, durée maximale d'une requête...). Il existe trois familles.

| Famille | Se règle au niveau | Exemples |
|---|---|---|
| Paramètres de compte | compte uniquement | `PERIODIC_DATA_REKEYING`, `ALLOW_CLIENT_MFA_CACHING`, `MIN_DATA_RETENTION_TIME_IN_DAYS` |
| Paramètres de session | compte → utilisateur → session | `TIMEZONE`, `QUERY_TAG`, `STATEMENT_TIMEOUT_IN_SECONDS` |
| Paramètres d'objet | compte → objet (warehouse, base, schéma, table) | `DATA_RETENTION_TIME_IN_DAYS`, `STATEMENT_TIMEOUT_IN_SECONDS` sur un warehouse |

Le principe est toujours le même : **le niveau le plus précis l'emporte**. Une valeur fixée sur la session remplace celle de l'utilisateur, qui remplace celle du compte.

```sql
ALTER ACCOUNT SET TIMEZONE = 'Europe/Paris';                        -- valeur par défaut pour tous
ALTER USER SALES_ETL_SVC SET TIMEZONE = 'UTC';                      -- pour cet utilisateur
ALTER SESSION SET TIMEZONE = 'America/New_York';                    -- pour la session en cours seulement
ALTER SESSION SET QUERY_TAG = 'chargement_quotidien';               -- étiquette visible dans QUERY_HISTORY

ALTER WAREHOUSE SALES_WH SET STATEMENT_TIMEOUT_IN_SECONDS = 3600;   -- paramètre d'objet
ALTER TABLE SALES_DB.ANALYTICS.FIN_CUSTOMERS SET DATA_RETENTION_TIME_IN_DAYS = 1;

SHOW PARAMETERS LIKE 'TIMEZONE' IN SESSION;                         -- colonne level : d'où vient la valeur
SHOW PARAMETERS IN ACCOUNT;
SHOW PARAMETERS IN WAREHOUSE SALES_WH;
ALTER SESSION UNSET TIMEZONE;                                       -- revenir à la valeur héritée
```

Dans le résultat de `SHOW PARAMETERS`, la colonne `level` indique à quel niveau la valeur a été fixée ; vide, c'est la valeur par défaut de Snowflake.

---

## 9. Pièges fréquents

| Piège | Ce qu'il faut savoir |
|---|---|
| Chercher dans `ACCOUNT_USAGE` une requête lancée il y a cinq minutes | la vue a jusqu'à 45 minutes de retard (3 heures pour d'autres) : utiliser `INFORMATION_SCHEMA` |
| Chercher dans `INFORMATION_SCHEMA` une connexion d'il y a un mois | l'historique n'y dépasse pas 7 jours pour les connexions et les requêtes |
| Croire que le masquage modifie la table | il agit à la lecture ; la donnée stockée est intacte |
| Masquer une colonne `NUMBER` en renvoyant du texte | le type de sortie doit être celui de l'entrée |
| Tester un masquage avec `ACCOUNTADMIN` et conclure qu'il ne marche pas | le résultat dépend de la règle écrite dans la politique, pas de la puissance du rôle : tester avec `USE ROLE` |
| Confondre authentification et autorisation | le SSO et la MFA disent qui vous êtes ; les rôles disent ce que vous pouvez faire |
| Compter sur un resource monitor pour limiter Snowpipe | il ne couvre pas le serverless : utiliser un budget |
| Activer une politique réseau sur tout le compte pour essayer | l'essayer d'abord sur un utilisateur de test |
| Croire que Tri-Secret Secure ou le rechiffrement sont nécessaires pour chiffrer | le chiffrement est actif partout par défaut ; ce sont des options supplémentaires |
| Créer un utilisateur de service avec un mot de passe | type `SERVICE` : paire de clés, OAuth ou jeton programmatique |

---

## 10. À retenir pour la certification

- Le chiffrement est automatique dans toutes les éditions : AES 256 bits au repos, TLS en transit.
- Hiérarchie de clés à quatre niveaux : racine, compte, table, fichier. Rotation automatique des clés de plus de **30 jours**. Rechiffrement périodique après **un an** : édition **Enterprise**.
- **Tri-Secret Secure** : clé gérée par le client combinée à celle de Snowflake ; édition **Business Critical**.
- Masquage dynamique, politiques d'accès par ligne, classification, `ACCESS_HISTORY` : édition **Enterprise**.
- Masquage : appliqué à la requête, types d'entrée et de sortie identiques, une politique par colonne.
- Politique d'accès par ligne : renvoie un `BOOLEAN`, évaluée **avant** les politiques de masquage.
- Politique réseau : niveaux compte, utilisateur, intégration de sécurité ; le plus précis l'emporte ; la liste bloquée l'emporte sur la liste autorisée ; rôle `SECURITYADMIN` ou privilège `CREATE NETWORK POLICY`.
- Délai d'inactivité d'une session par défaut : **4 heures** ; réglable de 5 minutes à 24 heures par une politique de session.
- SSO fédéré : SAML 2.0 ; Snowflake est le fournisseur de service, l'annuaire est le fournisseur d'identité.
- MFA : pour les humains qui utilisent un mot de passe ; passkey, application TOTP ou Duo.
- `ACCOUNT_USAGE` : latence de 45 minutes à 3 heures, historique d'**un an**, objets supprimés inclus. `INFORMATION_SCHEMA` : temps réel, historique de 7 jours à 6 mois, pas d'objets supprimés.
- `QUERY_HISTORY` 45 minutes, `LOGIN_HISTORY` 2 heures, `ACCESS_HISTORY` 3 heures de latence.
- Resource monitor : créé par `ACCOUNTADMIN` seulement ; actions `NOTIFY`, `SUSPEND`, `SUSPEND_IMMEDIATE` ; warehouses uniquement.
- Budget : limite mensuelle, inclut le serverless, notifie.
- Paramètres : compte → utilisateur → session pour les paramètres de session ; compte → objet pour les paramètres d'objet ; le plus précis l'emporte.

---

## 11. Atelier pratique (40 minutes)

Objectif : ouvrir une table de clients aux analystes sans leur montrer les e-mails ni les clients à risque, puis retrouver les traces de l'activité.

Données : `Data/finance/customers.csv` (19 clients, avec les colonnes `email`, `ssn_hash`, `credit_score`, `risk_category`).

Édition : les étapes 2 à 4 demandent l'édition **Enterprise**. Un compte d'essai permet de la choisir à la création. Sur un compte en édition Standard, faites la variante de l'étape 5. Aucune étape ne demande de compte cloud externe. Sur un compte d'essai, les politiques se créent avec `ACCOUNTADMIN` ; en entreprise, on utiliserait un rôle de gouvernance dédié.

### Étape 1 : charger la table (10 minutes)

Avec le rôle `SALES_ENGINEER`, chargez `Data/finance/customers.csv` dans `SALES_DB.ANALYTICS.FIN_CUSTOMERS` : par l'interface (chapitre 7) ou en SQL (chapitre 11). Vérifiez que `SALES_ANALYST` lit la table grâce aux droits futurs du chapitre 10 :

```sql
USE ROLE SALES_ANALYST;
USE WAREHOUSE SALES_WH;
SELECT first_name, email, risk_category FROM SALES_DB.ANALYTICS.FIN_CUSTOMERS LIMIT 5;
```

### Étape 2 : masquer les e-mails (8 minutes)

Avec `ACCOUNTADMIN`, créez la politique `MASK_EMAIL` de la section 5.1 et attachez-la à la colonne `email`. Relancez la requête de l'étape 1 avec `SALES_ANALYST`, puis avec `SALES_ENGINEER`. Écrivez une seconde politique qui remplace `credit_score` par `NULL` pour tout rôle autre que `SALES_ENGINEER` (attention au type).

### Étape 3 : filtrer les lignes (7 minutes)

Créez la politique `RAP_RISQUE` de la section 5.2 et ajoutez-la à la table. Comparez `SELECT risk_category, COUNT(*) ... GROUP BY 1` avec les deux rôles.

### Étape 4 : étiqueter (5 minutes)

Créez le tag `SENSIBILITE`, posez la valeur `confidentiel` sur les colonnes `email` et `ssn_hash`, puis listez les tags de la table :

```sql
SELECT column_name, tag_name, tag_value
FROM TABLE(SALES_DB.INFORMATION_SCHEMA.TAG_REFERENCES_ALL_COLUMNS(
  'SALES_DB.ANALYTICS.FIN_CUSTOMERS', 'table'));
```

### Étape 5 : variante pour l'édition Standard (à la place des étapes 2 à 4)

Sans politique, on obtient un résultat proche avec une vue sécurisée (chapitre 13) : retirez à `SALES_ANALYST` le droit de lire la table, et donnez-lui une vue.

```sql
CREATE OR REPLACE SECURE VIEW SALES_DB.ANALYTICS.V_FIN_CUSTOMERS AS
SELECT customer_id, first_name, last_name,
       REGEXP_REPLACE(email, '.+@', '*****@') AS email,
       city, state, risk_category
FROM SALES_DB.ANALYTICS.FIN_CUSTOMERS
WHERE risk_category = 'LOW';
```

### Étape 6 : session, coûts et audit (10 minutes)

1. Créez la politique de session `SESSION_COURTE` (section 3.1) et attachez-la à votre utilisateur seulement (`ALTER USER ... SET SESSION POLICY ...`), pas au compte.
2. Créez le resource monitor de la section 7 avec un quota de 5 crédits et attachez-le à `SALES_WH`. Vérifiez avec `SHOW RESOURCE MONITORS;`.
3. Fixez `QUERY_TAG = 'atelier_15'` dans votre session, lancez deux requêtes, puis retrouvez-les avec `INFORMATION_SCHEMA.QUERY_HISTORY` (section 6.3).
4. Lancez la requête `LOGIN_HISTORY` de la section 6.2 sur `ACCOUNT_USAGE`. Votre dernière connexion y figure-t-elle déjà ?
5. Affichez `SHOW PARAMETERS LIKE 'STATEMENT_TIMEOUT_IN_SECONDS' IN WAREHOUSE SALES_WH;`, changez la valeur, et observez la colonne `level`.

N'activez pas de politique réseau sur le compte pendant l'atelier : sur un réseau dont l'adresse change (partage de connexion, Wi-Fi public), vous perdriez l'accès au changement d'adresse suivant.

### Nettoyage

Une politique attachée ne peut pas être supprimée : détachez d'abord (`ALTER TABLE ... MODIFY COLUMN ... UNSET MASKING POLICY`, `ALTER TABLE ... DROP ROW ACCESS POLICY ...`, `ALTER USER ... UNSET SESSION POLICY`), puis supprimez les politiques, le tag, la politique de session et le resource monitor.

### Questions de réflexion

1. Vos requêtes de l'étape 6 n'apparaissent pas tout de suite dans `ACCOUNT_USAGE.QUERY_HISTORY`. Pourquoi, et au bout de combien de temps au plus ?
2. `SALES_ANALYST` lance `SELECT COUNT(*) FROM FIN_CUSTOMERS WHERE email LIKE 'john%'`. La politique de masquage change-t-elle le résultat ? Qu'en concluez-vous sur l'ordre dans lequel le masquage s'applique ?
3. Quelle différence de fond entre la vue sécurisée de l'étape 5 et les politiques des étapes 2 et 3 quand on a cinquante tables à protéger ?
4. Votre pipeline utilise Snowpipe et un warehouse. Quel outil choisir pour être prévenu d'un dépassement sur l'ensemble : resource monitor ou budget ?
5. Un auditeur demande qui a lu la colonne `ssn_hash` il y a huit mois. Quelle vue interroger, et quelle édition faut-il ?

---

## ✅ Points de vérification
- [ ] Je sais citer cinq méthodes d'authentification et dire laquelle convient à un humain ou à un outil
- [ ] Je sais à quels niveaux s'active une politique réseau et laquelle l'emporte
- [ ] Je connais le délai d'inactivité par défaut d'une session et l'objet qui le modifie
- [ ] Je sais ce qui est chiffré par défaut, et ce qu'ajoutent le rechiffrement périodique et Tri-Secret Secure
- [ ] J'ai masqué une colonne et vérifié le résultat avec deux rôles
- [ ] J'ai filtré des lignes avec une politique d'accès par ligne (ou une vue sécurisée)
- [ ] Je sais choisir entre `ACCOUNT_USAGE` et `INFORMATION_SCHEMA` selon la latence et l'historique
- [ ] Je sais ce que contiennent `LOGIN_HISTORY`, `QUERY_HISTORY` et `ACCESS_HISTORY`
- [ ] J'ai créé un resource monitor en SQL et je sais ce qu'il ne surveille pas
- [ ] Je sais lire la colonne `level` de `SHOW PARAMETERS`

## Documentation officielle
- [Authentification multifacteur (MFA)](https://docs.snowflake.com/en/user-guide/security-mfa)
- [Authentification fédérée et SSO](https://docs.snowflake.com/en/user-guide/admin-security-fed-auth-overview)
- [Jetons d'accès programmatiques](https://docs.snowflake.com/en/user-guide/programmatic-access-tokens)
- [Politiques réseau](https://docs.snowflake.com/en/user-guide/network-policies)
- [Politiques de session](https://docs.snowflake.com/en/user-guide/session-policies)
- [CREATE PASSWORD POLICY](https://docs.snowflake.com/en/sql-reference/sql/create-password-policy)
- [Gestion des clés de chiffrement](https://docs.snowflake.com/en/user-guide/security-encryption-manage)
- [Tri-Secret Secure](https://docs.snowflake.com/en/user-guide/security-encryption-tss)
- [Sécurité au niveau des colonnes (masquage)](https://docs.snowflake.com/en/user-guide/security-column-intro)
- [Politiques d'accès par ligne](https://docs.snowflake.com/en/user-guide/security-row-intro)
- [Tags d'objets](https://docs.snowflake.com/en/user-guide/object-tagging/introduction)
- [Classification des données sensibles](https://docs.snowflake.com/en/user-guide/classify-intro)
- [Schéma ACCOUNT_USAGE](https://docs.snowflake.com/en/sql-reference/account-usage)
- [INFORMATION_SCHEMA](https://docs.snowflake.com/en/sql-reference/info-schema)
- [Vue ACCESS_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/access_history)
- [Resource monitors](https://docs.snowflake.com/en/user-guide/resource-monitors)
- [Budgets](https://docs.snowflake.com/en/user-guide/budgets)
- [Paramètres](https://docs.snowflake.com/en/sql-reference/parameters)

---

[← Retour au sommaire](README.md) | [← Précédent](14-ia-applications.md) | [Suivant →](16-snowpipe-export-connectivite.md)
