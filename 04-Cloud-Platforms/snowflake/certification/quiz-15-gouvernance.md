# Quiz 15 — Authentification et gouvernance des données

[← Chapitre 15](../15-gouvernance.md) | [← Chapitre 10](../10-securite.md) | [← Sommaire du cours](../README.md)

20 questions au format de l'examen SnowPro Core (COF-C03), domaine 2. Une seule bonne réponse, sauf mention « 2 réponses attendues ». Comptez 25 minutes, sans le cours. Le corrigé est à la fin. Les questions portent sur le chapitre 15 et, pour quelques-unes, sur le chapitre 10.

---

### Question 1
Quelle est la latence maximale annoncée pour la vue `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY` ?

- A. Aucune, la vue est en temps réel
- B. 45 minutes
- C. 2 heures
- D. 24 heures

### Question 2
Pendant combien de temps les vues d'historique du schéma `ACCOUNT_USAGE` conservent-elles les données ?

- A. 7 jours
- B. 14 jours
- C. 90 jours
- D. 1 an

### Question 3
Un analyste doit retrouver une requête qu'il a lancée il y a dix minutes. Quelle source lui donne le résultat sans attendre ?

- A. La fonction de table `INFORMATION_SCHEMA.QUERY_HISTORY`
- B. La vue `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY`
- C. La vue `SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY`
- D. La vue `SNOWFLAKE.ORGANIZATION_USAGE.QUERY_HISTORY`

### Question 4
Quelles affirmations distinguent `ACCOUNT_USAGE` d'`INFORMATION_SCHEMA` ? (2 réponses attendues)

- A. `ACCOUNT_USAGE` n'a aucune latence
- B. `ACCOUNT_USAGE` inclut les objets supprimés
- C. `INFORMATION_SCHEMA` conserve l'historique pendant un an
- D. `INFORMATION_SCHEMA` existe dans chaque base de données
- E. `ACCOUNT_USAGE` n'est lisible que par le rôle `SYSADMIN`

### Question 5
À quel moment une politique de masquage dynamique s'applique-t-elle ?

- A. Au chargement des données, par `COPY INTO`
- B. Une fois par jour, par une tâche de maintenance
- C. Au moment de l'exécution de la requête, sans modifier la donnée stockée
- D. À la création de la table, de façon définitive

### Question 6
Une équipe veut qu'un rôle ne voie que les lignes de sa région dans une table de ventes. Quel objet répond au besoin ?

- A. Une politique de masquage
- B. Une politique réseau
- C. Un tag
- D. Une politique d'accès par ligne

### Question 7
Une table porte une politique d'accès par ligne et une politique de masquage sur une colonne. Dans quel ordre Snowflake les évalue-t-il ?

- A. La politique d'accès par ligne d'abord, puis la politique de masquage
- B. La politique de masquage d'abord, puis la politique d'accès par ligne
- C. Dans l'ordre de création des politiques
- D. Les deux ne peuvent pas coexister sur une même table

### Question 8
Quelle édition minimale de Snowflake permet d'utiliser Tri-Secret Secure ?

- A. Standard
- B. Enterprise
- C. Business Critical
- D. Toutes les éditions, sur demande au support

### Question 9
Que se passe-t-il quand une clé de chiffrement de Snowflake a plus de 30 jours ?

- A. Les données sont rechiffrées avec une nouvelle clé, dans toutes les éditions
- B. La clé est retirée et remplacée automatiquement ; elle ne sert plus qu'à déchiffrer
- C. Rien, sauf si `ACCOUNTADMIN` lance une rotation manuelle
- D. Les données deviennent illisibles jusqu'au renouvellement de la clé

### Question 10
Une politique réseau est active sur le compte et une autre sur l'utilisateur `ALICE`. Laquelle s'applique aux connexions d'`ALICE` ?

- A. Celle du compte, toujours prioritaire
- B. Les deux, cumulées
- C. La plus récente
- D. Celle de l'utilisateur

### Question 11
Une même adresse IP figure dans la liste autorisée et dans la liste bloquée d'une politique réseau. Quel est le résultat ?

- A. La création de la politique échoue
- B. L'adresse est bloquée
- C. L'adresse est autorisée
- D. Le comportement dépend de l'ordre d'écriture des listes

### Question 12
Quel est le délai d'inactivité par défaut au bout duquel une session de programme (pilote, connecteur) expire ?

- A. 4 heures
- B. 30 minutes
- C. 1 heure
- D. 24 heures

### Question 13
Dans une authentification fédérée (SSO), quels sont les rôles respectifs de Snowflake et de l'annuaire de l'entreprise ?

- A. Snowflake est le fournisseur d'identité, l'annuaire est le fournisseur de service
- B. Les deux sont fournisseurs d'identité
- C. Snowflake est le fournisseur de service, l'annuaire est le fournisseur d'identité
- D. L'annuaire gère aussi les privilèges sur les tables

### Question 14
Un orchestrateur doit se connecter à Snowflake sans intervention humaine. Quelles méthodes conviennent à un utilisateur de type `SERVICE` ? (2 réponses attendues)

- A. Mot de passe avec authentification multifacteur par Duo
- B. Paire de clés
- C. Passkey
- D. Jeton d'accès programmatique
- E. Connexion par l'interface Snowsight

### Question 15
Quel rôle peut créer un resource monitor ?

- A. `SYSADMIN`
- B. `SECURITYADMIN`
- C. `USERADMIN`
- D. `ACCOUNTADMIN`

### Question 16
Un resource monitor atteint un seuil associé à l'action `SUSPEND`. Que se passe-t-il ?

- A. Les requêtes en cours sont annulées immédiatement
- B. Seule une notification est envoyée
- C. Le warehouse est suspendu une fois les requêtes en cours terminées
- D. Le warehouse est supprimé

### Question 17
Une entreprise veut être alertée quand la dépense mensuelle totale, Snowpipe et tâches serverless comprises, risque de dépasser une limite. Quel outil choisir ?

- A. Un budget
- B. Un resource monitor au niveau du compte
- C. Une politique de session
- D. Le paramètre `STATEMENT_TIMEOUT_IN_SECONDS`

### Question 18
Le paramètre `TIMEZONE` vaut `Europe/Paris` au niveau du compte, `UTC` au niveau de l'utilisateur, et la session exécute `ALTER SESSION SET TIMEZONE = 'America/New_York'`. Quelle valeur s'applique dans cette session ?

- A. `Europe/Paris`
- B. `America/New_York`
- C. `UTC`
- D. Une erreur : un paramètre ne peut être fixé qu'à un seul niveau

### Question 19
Un auditeur demande la liste des tables de base réellement lues par les requêtes d'un utilisateur, y compris à travers des vues. Quelle vue interroger ?

- A. `LOGIN_HISTORY`
- B. `QUERY_HISTORY`
- C. `TAG_REFERENCES`
- D. `ACCESS_HISTORY`
- E. `WAREHOUSE_METERING_HISTORY`

### Question 20
Le rôle `SALES_ANALYST` a le privilège `SELECT` sur la table `SALES_DB.ANALYTICS.DAILY_SALES` et `USAGE` sur `SALES_WH`, mais sa requête renvoie « Object does not exist or not authorized ». Quelle est la cause la plus probable ?

- A. Le rôle n'a pas `OWNERSHIP` sur la table
- B. Il manque `USAGE` sur la base ou sur le schéma
- C. La table est protégée par une politique de masquage
- D. Le rôle n'a pas `OPERATE` sur le warehouse

---

## Corrigé

| Question | Réponse | Explication | Section du chapitre |
|---|---|---|---|
| 1 | B | `QUERY_HISTORY` dans `ACCOUNT_USAGE` a jusqu'à 45 minutes de latence ; d'autres vues vont jusqu'à 3 heures. | 15, section 6.1 |
| 2 | D | Les vues d'historique d'`ACCOUNT_USAGE` conservent un an (365 jours) de données. | 15, section 6.1 |
| 3 | A | `INFORMATION_SCHEMA` n'a pas de latence ; `ACCOUNT_USAGE` aurait jusqu'à 45 minutes de retard. | 15, sections 6.1 et 6.3 |
| 4 | B, D | `ACCOUNT_USAGE` inclut les objets supprimés ; chaque base a son propre `INFORMATION_SCHEMA`, sans latence mais avec un historique court. | 15, section 6.1 |
| 5 | C | Le masquage dynamique s'applique à la requête ; la donnée stockée n'est pas modifiée. | 15, section 5.1 |
| 6 | D | Une politique d'accès par ligne renvoie vrai ou faux pour chaque ligne selon le contexte ; le masquage agit sur une colonne. | 15, section 5.2 |
| 7 | A | Snowflake évalue la politique d'accès par ligne en premier, puis les politiques de masquage. | 15, section 5.2 |
| 8 | C | Tri-Secret Secure demande l'édition Business Critical ou supérieure. | 15, section 4 |
| 9 | B | La rotation retire la clé de plus de 30 jours et en crée une nouvelle ; le rechiffrement des données est une autre fonction (Enterprise, après un an). | 15, section 4 |
| 10 | D | Le niveau le plus précis l'emporte : la politique de l'utilisateur remplace celle du compte pour cet utilisateur. | 15, section 2 |
| 11 | B | La liste bloquée est appliquée en premier : l'adresse est bloquée. | 15, section 2 |
| 12 | A | Le délai par défaut est de 240 minutes, soit 4 heures ; une politique de session le modifie. | 15, section 3.1 |
| 13 | C | Snowflake est le fournisseur de service ; l'annuaire (fournisseur d'identité) authentifie, mais les droits restent gérés par les rôles Snowflake. | 15, section 1.3 |
| 14 | B, D | Un utilisateur de service n'a ni mot de passe ni MFA ni accès à l'interface : il utilise une paire de clés, OAuth ou un jeton programmatique. | 15, section 1.1 ; 10, section 3.5 |
| 15 | D | Seul `ACCOUNTADMIN` peut créer un resource monitor ; il peut ensuite donner `MONITOR` ou `MODIFY` à d'autres rôles. | 15, section 7 |
| 16 | C | `SUSPEND` attend la fin des requêtes en cours ; `SUSPEND_IMMEDIATE` les annule. | 15, section 7 |
| 17 | A | Un budget couvre les warehouses et le serverless ; un resource monitor ne surveille que les warehouses. | 15, section 7 |
| 18 | B | Pour un paramètre de session, la session l'emporte sur l'utilisateur, qui l'emporte sur le compte. | 15, section 8 |
| 19 | D | `ACCESS_HISTORY` (colonne `BASE_OBJECTS_ACCESSED`) donne les objets réellement lus ; `QUERY_HISTORY` ne donne que le texte de la requête. | 15, section 6.4 |
| 20 | B | Lire une table demande `USAGE` sur le warehouse, la base et le schéma, plus `SELECT` sur la table ; un maillon manquant donne ce message. | 10, section 1.2 |
