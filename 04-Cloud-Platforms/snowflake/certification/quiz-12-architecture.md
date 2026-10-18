# Quiz 12 — Architecture de Snowflake

[← Chapitre 12](../12-architecture.md) | [← Sommaire du cours](../README.md)

20 questions au format de l'examen SnowPro Core (COF-C03), domaine 1. Une seule bonne réponse, sauf mention « 2 réponses attendues ». Comptez 25 minutes, sans le cours. Le corrigé est à la fin.

---

### Question 1
Quelles sont les trois couches de l'architecture de Snowflake ?

- A. Ingestion, transformation, restitution
- B. Stockage, calcul, services cloud
- C. Bronze, argent, or
- D. Réseau, calcul, sécurité

### Question 2
Quelle couche se charge d'analyser et d'optimiser une requête avant son exécution ?

- A. La couche de stockage
- B. La couche de calcul
- C. Le stage interne
- D. La couche des services cloud

### Question 3
Comment la documentation qualifie-t-elle l'architecture de Snowflake ?

- A. Un hybride des architectures à disque partagé (*shared-disk*) et sans partage (*shared-nothing*)
- B. Une architecture sans partage (*shared-nothing*) pure
- C. Une architecture à disque partagé (*shared-disk*) pure
- D. Une architecture pair à pair sans service central

### Question 4
Un warehouse de taille Large reste démarré exactement 30 minutes, avec un seul cluster. Combien de crédits consomme-t-il ?

- A. 2
- B. 8
- C. 4
- D. 16

### Question 5
Quelles fonctionnalités exigent au minimum l'édition Enterprise ? (2 réponses attendues)

- A. Le partage de données sécurisé (*Secure Data Sharing*)
- B. Les warehouses multi-cluster
- C. Les clés gérées par le client (*Tri-Secret Secure*)
- D. Le Time Travel jusqu'à 90 jours
- E. Le chiffrement automatique des données

### Question 6
Un warehouse suspendu redémarre pour exécuter une requête de 10 secondes, puis il est suspendu de nouveau. Quelle durée est facturée ?

- A. 60 secondes
- B. 10 secondes
- C. 1 heure
- D. Rien : les 60 premières secondes sont offertes

### Question 7
Chaque lundi matin, 200 utilisateurs ouvrent leurs tableaux de bord en même temps et les requêtes sont mises en file d'attente. Chaque requête, prise seule, est rapide. Que faut-il faire ?

- A. Passer le warehouse de Medium à 2X-Large
- B. Allonger la durée de `AUTO_SUSPEND`
- C. Utiliser un warehouse multi-cluster en mise à l'échelle automatique
- D. Créer un warehouse optimisé pour Snowpark

### Question 8
Une entreprise de santé doit stocker des données médicales protégées (PHI) et se connecter par AWS PrivateLink. Quelle est l'édition minimale ?

- A. Standard
- B. Enterprise
- C. Virtual Private Snowflake
- D. Business Critical

### Question 9
Dans quel cas l'utilisation des services cloud est-elle facturée ?

- A. Toujours, à la seconde, comme un warehouse
- B. Quand leur consommation quotidienne dépasse 10 % de la consommation quotidienne des warehouses
- C. Jamais : les services cloud sont gratuits
- D. Quand leur consommation mensuelle dépasse 10 % de la facture de stockage

### Question 10
Quel cache est perdu lorsque le warehouse est suspendu ?

- A. Le cache du warehouse (disque local)
- B. Le cache de résultats
- C. Le cache de métadonnées
- D. Aucun : les trois caches survivent à la suspension

### Question 11
Combien de temps un résultat de requête est-il conservé dans le cache de résultats s'il n'est jamais réutilisé ?

- A. 1 heure
- B. 31 jours
- C. 24 heures
- D. 7 jours

### Question 12
Un utilisateur exécute `SELECT COUNT(*) FROM ORDERS_RAW;` alors que le warehouse est suspendu et que la requête n'a jamais été exécutée. Que se passe-t-il le plus probablement ?

- A. La requête échoue faute de warehouse démarré
- B. Le warehouse redémarre et lit toutes les micro-partitions
- C. La requête attend qu'un administrateur redémarre le warehouse
- D. Le cache du warehouse fournit la réponse
- E. La réponse vient des métadonnées, sans calcul par le warehouse

### Question 13
Parmi ces objets, lesquels sont des objets de niveau compte, et non de niveau schéma ? (2 réponses attendues)

- A. Une table
- B. Un format de fichier
- C. Un warehouse
- D. Un stage
- E. Un rôle

### Question 14
Le paramètre `DATA_RETENTION_TIME_IN_DAYS` vaut 1 sur le compte, 30 sur la base `SALES_DB` et 7 sur la table `SALES_DB.RAW_DATA.ORDERS_RAW`. Quelle valeur s'applique à cette table ?

- A. 1
- B. 7
- C. 30
- D. 38

### Question 15
Quelle affirmation décrit correctement le redimensionnement d'un warehouse pendant que des requêtes s'exécutent ?

- A. Les requêtes en cours sont annulées puis relancées sur la nouvelle taille
- B. Le redimensionnement est refusé tant qu'une requête est en cours
- C. Les requêtes en cours basculent immédiatement sur la nouvelle taille
- D. Les requêtes en cours se terminent sur l'ancienne taille ; les nouvelles utilisent la nouvelle

### Question 16
Une équipe de science des données entraîne des modèles dans des procédures stockées Python et manque de mémoire. Quel type de warehouse est conçu pour ce cas ?

- A. Un warehouse optimisé pour Snowpark
- B. Un warehouse standard X-Small en multi-cluster
- C. Un warehouse standard avec la politique `ECONOMY`
- D. Aucun : une procédure stockée ne s'exécute pas sur un warehouse

### Question 17
Quel mouvement de données donne lieu à une facturation de transfert ?

- A. Le chargement de fichiers depuis le poste de travail vers un stage interne
- B. Une requête entre deux bases du même compte
- C. L'export de données vers un stockage situé dans une autre région
- D. Le clonage d'une table dans le même compte

### Question 18
Sur quelle base le stockage des tables est-il facturé ?

- A. La taille des fichiers sources avant chargement
- B. La moyenne quotidienne du volume compressé, à un tarif par téraoctet et par mois
- C. Le nombre de lignes stockées
- D. Le nombre de micro-partitions lues par les requêtes

### Question 19
Un warehouse multi-cluster de taille Medium est réglé avec `MIN_CLUSTER_COUNT = 3` et `MAX_CLUSTER_COUNT = 3`. Quelles affirmations sont exactes ? (2 réponses attendues)

- A. Il fonctionne en mode maximisé
- B. Il fonctionne en mise à l'échelle automatique
- C. Il consomme 4 crédits par heure lorsqu'il est démarré
- D. Il consomme 12 crédits par heure lorsqu'il est démarré
- E. Chaque requête s'exécute trois fois plus vite

### Question 20
Quel outil en ligne de commande Snowflake recommande-t-il pour les nouveaux projets, y compris pour déployer des applications Streamlit ou du code Snowpark ?

- A. SnowSQL
- B. Le pilote ODBC
- C. Snowsight
- D. Snowflake CLI (commande `snow`)

---

## Corrigé

| Question | Réponse | Explication | Section du chapitre |
|---|---|---|---|
| 1 | B | Les trois couches sont le stockage, le calcul et les services cloud. | 1.1 |
| 2 | D | L'analyse et l'optimisation des requêtes sont des services de la couche des services cloud. | 1.2 |
| 3 | A | Snowflake combine un dépôt central de données (disque partagé) et des grappes de calcul MPP (sans partage). | 1.3 |
| 4 | C | Large = 8 crédits par heure ; une demi-heure coûte 4 crédits. | 5.2 |
| 5 | B, D | Le multi-cluster et le Time Travel étendu commencent à l'édition Enterprise ; Tri-Secret Secure exige Business Critical ; le partage et le chiffrement existent dès Standard. | 3 |
| 6 | A | La facturation est à la seconde, avec un minimum de 60 secondes à chaque démarrage. | 5.2 |
| 7 | C | Un problème de concurrence se règle en ajoutant des clusters (*scale out*), pas en augmentant la taille. | 5.4, 5.5 |
| 8 | D | La prise en charge des données PHI et la connectivité privée commencent à l'édition Business Critical. | 3 |
| 9 | B | Seule la part quotidienne des services cloud qui dépasse 10 % des crédits des warehouses est facturée. | 6.2 |
| 10 | A | Le cache du warehouse vit sur les disques locaux du warehouse et disparaît à la suspension. | 7 |
| 11 | C | Un résultat est conservé 24 heures ; chaque réutilisation relance ce délai, dans la limite de 31 jours. | 7 |
| 12 | E | Le nombre de lignes fait partie des métadonnées tenues par les services cloud : aucun warehouse n'est nécessaire. | 7 |
| 13 | C, E | Les warehouses et les rôles sont des objets de compte ; tables, stages et formats de fichier appartiennent à un schéma. | 4.1 |
| 14 | B | Pour un paramètre d'objet, le réglage le plus précis (la table) l'emporte sur le schéma, la base et le compte. | 4.3 |
| 15 | D | Le changement de taille ne concerne que les requêtes qui démarrent après lui. | 5.4 |
| 16 | A | Les warehouses optimisés pour Snowpark offrent beaucoup plus de mémoire par nœud, pour l'entraînement de modèles. | 5.6 |
| 17 | C | Seule la sortie de données vers une autre région ou un autre fournisseur est facturée ; l'entrée est gratuite. | 6.4 |
| 18 | B | Le stockage est facturé au téraoctet par mois, sur la moyenne quotidienne du volume après compression. | 6.3 |
| 19 | A, D | Minimum égal au maximum : mode maximisé, les trois clusters démarrent ensemble, soit 3 × 4 = 12 crédits par heure ; le multi-cluster n'accélère pas une requête isolée. | 5.5 |
| 20 | D | Snowflake CLI est le client recommandé pour les nouveaux travaux ; SnowSQL est l'ancien client. | 8 |

Répartition des bonnes réponses : A 5, B 5, C 5, D 6, E 2 (les questions à deux réponses comptent pour deux lettres).

**Lecture du score** : 16 ou plus, le chapitre est acquis ; de 12 à 15, relire les sections des questions ratées ; moins de 12, reprendre le chapitre et refaire l'atelier.
