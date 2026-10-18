# Quiz 13 — Stockage et protection des données

[← Chapitre 13](../13-stockage-protection.md) | [← Sommaire du cours](../README.md)

20 questions au format de l'examen SnowPro Core (COF-C03). Une seule bonne réponse, sauf mention « 2 réponses attendues ». Comptez 25 minutes, sans le cours. Le corrigé est à la fin.

---

### Question 1
Quelle quantité de données une micro-partition contient-elle ?

- A. Exactement 16 Mo après compression
- B. Entre 1 et 5 Go avant compression
- C. Entre 50 et 500 Mo avant compression
- D. Une taille fixée par l'utilisateur à la création de la table

### Question 2
Que se passe-t-il dans le stockage lorsqu'un `UPDATE` modifie des lignes d'une table ?

- A. De nouvelles micro-partitions sont écrites ; les anciennes ne sont pas modifiées
- B. Les micro-partitions concernées sont modifiées sur place
- C. La table entière est toujours réécrite
- D. Les lignes modifiées sont placées dans un journal séparé jusqu'à la suspension du warehouse

### Question 3
Quelles informations Snowflake conserve-t-il sur chaque micro-partition et utilise-t-il pour l'élagage (*pruning*) ?

- A. La liste des utilisateurs qui ont lu la micro-partition
- B. Un index de type B-tree par colonne
- C. Le texte des requêtes qui l'ont créée
- D. La plage de valeurs de chaque colonne et le nombre de valeurs distinctes

### Question 4
Sur un compte en édition Enterprise, quelle est la durée maximale de Time Travel d'une table transitoire ?

- A. 0 jour : les tables transitoires n'ont pas de Time Travel
- B. 1 jour
- C. 7 jours
- D. 90 jours

### Question 5
Quelles affirmations sur le Fail-safe sont exactes ? (2 réponses attendues)

- A. Il dure 7 jours et cette durée n'est pas réglable
- B. Il s'applique aux tables transitoires et temporaires
- C. Seul Snowflake peut y récupérer des données, sur demande au support
- D. Il s'interroge avec la clause `AT(OFFSET => ...)`
- E. Il commence dès la création de la table, en parallèle du Time Travel

### Question 6
Un outil de transformation reconstruit entièrement, chaque nuit, des tables intermédiaires de plusieurs centaines de gigaoctets. Les autres équipes doivent pouvoir les lire le lendemain. Quel type de table limite le coût de stockage ?

- A. Table permanente avec une rétention de 90 jours
- B. Table temporaire
- C. Table externe
- D. Table transitoire

### Question 7
Une table temporaire `ORDERS` est créée dans un schéma qui contient déjà une table permanente `ORDERS`. Que se passe-t-il dans cette session ?

- A. La création échoue : le nom est déjà pris
- B. Les requêtes sur `ORDERS` utilisent la table temporaire, qui masque la permanente
- C. La table permanente est supprimée
- D. Les deux tables sont fusionnées jusqu'à la fin de la session

### Question 8
Quelle édition minimale permet de créer une vue matérialisée ?

- A. Standard
- B. Business Critical
- C. Enterprise
- D. Virtual Private Snowflake

### Question 9
Une équipe veut accélérer un tableau de bord qui joint trois tables, en acceptant jusqu'à dix minutes de retard sur les données. Quel objet convient ?

- A. Une table dynamique avec `TARGET_LAG = '10 minutes'`
- B. Une vue matérialisée
- C. Une vue sécurisée
- D. Une table externe

### Question 10
Quelle requête renvoie l'état de la table `ORDERS_RAW` tel qu'il était une heure plus tôt ?

- A. `SELECT * FROM ORDERS_RAW UNDROP(3600);`
- B. `SELECT * FROM ORDERS_RAW FAILSAFE(HOURS => 1);`
- C. `SELECT * FROM ORDERS_RAW AT(OFFSET => 3600);`
- D. `SELECT * FROM ORDERS_RAW AT(OFFSET => -3600);`

### Question 11
Une table a été supprimée, puis une nouvelle table du même nom a été créée. Que se passe-t-il si l'on exécute `UNDROP TABLE` sur ce nom ?

- A. La nouvelle table est remplacée par l'ancienne
- B. La commande échoue ; il faut d'abord renommer la table existante
- C. Les deux tables sont fusionnées
- D. L'ancienne table est restaurée sous un nom suffixé automatiquement

### Question 12
Sur un compte en édition Enterprise, une table permanente a une rétention réglée au maximum. Pendant combien de jours, au total, des données supprimées restent-elles récupérables par l'utilisateur ou par Snowflake ?

- A. 7
- B. 8
- C. 90
- D. 91
- E. 97

### Question 13
Juste après `CREATE TABLE ORDERS_DEV CLONE ORDERS_RAW;`, quel est le coût de stockage supplémentaire ?

- A. Le double du stockage de la table source
- B. La moitié du stockage de la table source
- C. Aucun : le clone référence les micro-partitions existantes
- D. Le stockage de la table source, facturé au tarif des tables transitoires

### Question 14
Quelle affirmation sur une vue sécurisée (*secure view*) est exacte ?

- A. Sa définition n'est visible que par les rôles autorisés, et certaines optimisations de requête sont désactivées
- B. Elle stocke son résultat pour accélérer les lectures
- C. Elle exige l'édition Business Critical
- D. Elle est toujours plus rapide qu'une vue standard

### Question 15
Quelles affirmations sur le clone d'une table sont exactes ? (2 réponses attendues)

- A. Il reprend automatiquement tous les droits donnés sur la table source
- B. Il ne reprend pas l'historique de chargement de la table source
- C. Supprimer la table source le rend inutilisable
- D. Il peut être créé à un instant passé avec `AT` ou `BEFORE`
- E. Il est en lecture seule

### Question 16
Une entreprise veut interroger en SQL des fichiers Parquet qui doivent rester dans son propre stockage cloud, sans les charger dans Snowflake et sans avoir besoin de les modifier. Quel objet convient ?

- A. Une table temporaire
- B. Une vue matérialisée sur un stage interne
- C. Une table transitoire
- D. Une table externe

### Question 17
Que signifie une valeur de 0 pour `DATA_RETENTION_TIME_IN_DAYS` sur une table ?

- A. Le Time Travel est désactivé pour cette table
- B. La rétention est illimitée
- C. La table hérite de la valeur du compte
- D. Le Fail-safe est porté à 90 jours

### Question 18
Quelle restriction s'applique à la requête d'une vue matérialisée ?

- A. Elle ne peut pas contenir de fonction d'agrégation
- B. Elle ne peut pas contenir de clause `WHERE`
- C. Elle ne peut interroger qu'une seule table, sans jointure
- D. Elle ne peut pas porter sur une table de plus d'un téraoctet

### Question 19
Quelle différence y a-t-il entre `AT` et `BEFORE` dans une requête de Time Travel ?

- A. `AT` s'emploie pour les tables, `BEFORE` pour les schémas
- B. `AT` inclut les changements de l'instant ou de l'instruction indiqués ; `BEFORE` s'arrête juste avant
- C. `AT` accepte un horodatage, `BEFORE` uniquement un décalage en secondes
- D. Aucune : ce sont deux synonymes

### Question 20
Une table de plusieurs téraoctets est presque toujours filtrée sur la colonne `event_date`, mais ses requêtes lisent la quasi-totalité des micro-partitions. Quelle action est la plus adaptée ?

- A. Convertir la table en table temporaire
- B. Porter la rétention Time Travel à 90 jours
- C. Créer une vue sécurisée sur la table
- D. Suspendre le warehouse entre deux requêtes
- E. Définir une clé de clustering sur `event_date`

---

## Corrigé

| Question | Réponse | Explication | Section du chapitre |
|---|---|---|---|
| 1 | C | Une micro-partition contient de 50 à 500 Mo de données avant compression. | 1.2 |
| 2 | A | Les micro-partitions sont immuables : une modification en écrit de nouvelles et met les anciennes de côté. | 1.2 |
| 3 | D | Les plages de valeurs et le nombre de valeurs distinctes par colonne permettent d'écarter des micro-partitions sans les lire. | 1.2, 1.3 |
| 4 | B | Les tables transitoires et temporaires ont 0 ou 1 jour de Time Travel, quelle que soit l'édition. | 2.1, 4.2 |
| 5 | A, C | Le Fail-safe dure 7 jours sans réglage possible et seul Snowflake y accède ; il ne concerne que les tables permanentes et commence à la fin du Time Travel. | 5 |
| 6 | D | Une table transitoire persiste et reste visible de tous, sans Fail-safe : au plus un jour d'historique facturé ; une table temporaire disparaîtrait avec la session. | 2.1, 7 |
| 7 | B | Dans la session, la table temporaire a priorité sur toute table du même nom et la masque. | 2.1 |
| 8 | C | Les vues matérialisées sont une fonctionnalité de l'édition Enterprise. | 3 |
| 9 | A | Une vue matérialisée n'accepte pas les jointures ; la table dynamique tient à jour le résultat d'une requête quelconque selon la fraîcheur cible. | 2.2, 3 |
| 10 | D | `OFFSET` est un décalage en secondes par rapport à maintenant, négatif pour remonter dans le passé. | 4.3 |
| 11 | B | `UNDROP` échoue si un objet du même nom existe ; on renomme l'objet présent puis on restaure. | 4.5 |
| 12 | E | 90 jours de Time Travel (par l'utilisateur) puis 7 jours de Fail-safe (par Snowflake) : 97 jours. | 5 |
| 13 | C | Le clonage ne copie rien : le stockage n'augmente qu'avec les modifications ultérieures. | 6.1 |
| 14 | A | Une vue sécurisée cache sa définition et renonce à certaines optimisations, ce qui peut la ralentir ; elle existe dès l'édition Standard et ne stocke rien. | 3 |
| 15 | B, D | Le clone d'une table ne reprend ni l'historique de chargement ni, sans `COPY GRANTS`, les droits ; il se combine avec le Time Travel et reste indépendant et modifiable. | 6.2, 6.3 |
| 16 | D | Une table externe lit en lecture seule des fichiers restés dans un stage externe. | 2.2 |
| 17 | A | Une rétention de 0 désactive le Time Travel pour l'objet. | 4.2 |
| 18 | C | Une vue matérialisée ne porte que sur une seule table ; les agrégations simples et les filtres sont autorisés. | 3 |
| 19 | B | `AT` inclut l'instant indiqué, `BEFORE` renvoie l'état immédiatement antérieur. | 4.3 |
| 20 | E | Une clé de clustering regroupe les valeurs de la colonne filtrée et rend l'élagage efficace sur une très grande table. | 1.4 |

Répartition des bonnes réponses : A 5, B 5, C 5, D 5, E 2 (les questions à deux réponses comptent pour deux lettres).

**Lecture du score** : 16 ou plus, le chapitre est acquis ; de 12 à 15, relire les sections des questions ratées ; moins de 12, reprendre le chapitre et refaire l'atelier.
