# Quiz 18 — Requêtes et transformation

[← Chapitre 18](../18-transformation.md) | [← Sommaire du cours](../README.md)

20 questions au format de l'examen SnowPro Core (COF-C03), domaine 4. Une seule bonne réponse, sauf mention « 2 réponses attendues ». Comptez 25 minutes, sans le cours. Le corrigé est à la fin.

---

### Question 1
Quel type de données Snowflake peut contenir une valeur de n'importe quel type, y compris un objet ou un tableau JSON ?

- A. `VARCHAR`
- B. `OBJECT`
- C. `VARIANT`
- D. `ARRAY`

### Question 2
La colonne `doc` (type `VARIANT`) contient `{"customer": {"country": "USA"}}`. Quelle expression renvoie le texte `USA` sans guillemets ?

- A. `doc:customer.country::VARCHAR`
- B. `doc.customer.country`
- C. `doc:Customer.Country::VARCHAR`
- D. `doc->customer->country`

### Question 3
La colonne `properties` contient `{"device": "desktop"}`. Que renvoie `SELECT properties:Device FROM USAGE_EVENTS;` ?

- A. `"desktop"`
- B. Une erreur de compilation
- C. `desktop`
- D. `NULL`

### Question 4
Quelle fonction transforme un tableau contenu dans une colonne `VARIANT` en plusieurs lignes, une par élément ?

- A. `PARSE_JSON`
- B. `FLATTEN`
- C. `OBJECT_CONSTRUCT`
- D. `ARRAY_AGG`

### Question 5
Une requête utilise `LATERAL FLATTEN(INPUT => doc:items)`. Les commandes dont la liste `items` est vide disparaissent du résultat. Quelle option permet de les conserver ?

- A. `RECURSIVE => TRUE`
- B. `MODE => 'ARRAY'`
- C. `OUTER => TRUE`
- D. `STRIP_OUTER_ARRAY = TRUE`

### Question 6
Un fichier JSON est constitué d'un seul grand tableau `[ {...}, {...}, ... ]`. Quelle option du format de fichier permet de charger chaque élément du tableau dans une ligne distincte ?

- A. `STRIP_NULL_VALUES = TRUE`
- B. `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE`
- C. `PARSE_HEADER = TRUE`
- D. `STRIP_OUTER_ARRAY = TRUE`

### Question 7
À quoi sert la clause `QUALIFY` ?

- A. À filtrer sur le résultat d'une fonction de fenêtrage
- B. À filtrer les lignes avant l'agrégation
- C. À vérifier les privilèges du rôle sur une table
- D. À limiter le nombre de lignes renvoyées

### Question 8
Sur une table de plusieurs milliards de lignes, on veut une estimation rapide du nombre de clients distincts. Quelle fonction utiliser, et sur quel algorithme repose-t-elle ?

- A. `COUNT(DISTINCT ...)`, algorithme t-Digest
- B. `APPROX_COUNT_DISTINCT`, algorithme HyperLogLog
- C. `APPROX_TOP_K`, algorithme MinHash
- D. `APPROX_PERCENTILE`, algorithme HyperLogLog

### Question 9
Quelles sont les deux affirmations exactes sur la différence entre une fonction définie par l'utilisateur (UDF) et une procédure stockée ? (2 réponses attendues)

- A. Une UDF s'appelle avec `CALL`
- B. Une procédure stockée peut exécuter des instructions DDL et DML
- C. Une UDF doit toujours renvoyer une valeur
- D. Une procédure stockée s'utilise dans la liste des colonnes d'un `SELECT`, comme une fonction native
- E. Une procédure stockée ne peut pas être écrite en Python

### Question 10
Une procédure stockée est créée sans clause `EXECUTE AS`. Avec quels droits s'exécute-t-elle ?

- A. Ceux du rôle qui l'appelle
- B. Ceux du rôle `ACCOUNTADMIN`
- C. Ceux du rôle `PUBLIC`
- D. Ceux du rôle propriétaire de la procédure

### Question 11
Que stocke un stream ?

- A. Une copie complète de la table source
- B. Une copie des lignes modifiées depuis sa création
- C. Un décalage (*offset*) : une position dans l'historique des versions de la table
- D. Les fichiers du stage qui ont servi au chargement

### Question 12
Une ligne de la table source est modifiée par un `UPDATE`. Comment cette modification apparaît-elle dans un stream standard ?

- A. Une ligne avec `METADATA$ACTION = 'UPDATE'`
- B. Deux lignes, `DELETE` et `INSERT`, avec `METADATA$ISUPDATE = TRUE`
- C. Une ligne `INSERT` avec `METADATA$ISUPDATE = FALSE`
- D. Elle n'apparaît pas : un stream standard ne capture que les insertions

### Question 13
Quelle opération fait avancer le décalage d'un stream ?

- A. Un `SELECT * FROM le_stream`
- B. Un appel à `SYSTEM$STREAM_HAS_DATA`
- C. Un `SHOW STREAMS`
- D. Une instruction DML validée qui lit le stream, par exemple `INSERT INTO ... SELECT ... FROM le_stream`

### Question 14
Quel type de stream utiliser sur une table externe ?

- A. Insert-only
- B. Standard
- C. Append-only
- D. Aucun : les streams ne sont pas pris en charge sur les tables externes

### Question 15
Un stream créé il y a trois mois sur une table n'a jamais été consommé. Une requête sur ce stream renvoie une erreur indiquant qu'il est périmé (*stale*). Quelle en est la cause, et que faut-il faire ?

- A. Le warehouse était suspendu ; il suffit de le reprendre
- B. Le décalage du stream est sorti de la période de rétention des données de la table ; il faut recréer le stream
- C. Le stream a dépassé sa taille maximale ; il faut le vider avec `TRUNCATE`
- D. Le rôle a perdu le privilège `SELECT` ; il faut le redonner

### Question 16
Un ingénieur crée une task avec `CREATE TASK ... SCHEDULE = '5 MINUTES' ...`. Dix minutes plus tard, elle ne s'est jamais exécutée et aucune erreur n'est signalée. Quelle est la cause la plus probable ?

- A. Une task ne peut pas avoir un intervalle inférieur à une heure
- B. Les tasks demandent l'édition Enterprise
- C. La task est créée suspendue : il faut exécuter `ALTER TASK ... RESUME`
- D. Le warehouse de la task doit être en multi-cluster

### Question 17
Comment crée-t-on une task serverless, dont le calcul est géré par Snowflake ?

- A. En omettant le paramètre `WAREHOUSE` dans `CREATE TASK`
- B. En ajoutant `SERVERLESS = TRUE` dans `CREATE TASK`
- C. En l'attachant à un warehouse de taille X-Small
- D. En la créant avec le rôle `ACCOUNTADMIN`

### Question 18
Quelles sont les deux affirmations exactes à propos d'un graphe de tasks (*task graph*) ? (2 réponses attendues)

- A. Chaque task enfant doit avoir son propre `SCHEDULE`
- B. Seule la task racine porte la planification
- C. Un graphe peut avoir plusieurs tasks racines
- D. Une task enfant est rattachée à ses parents avec le mot-clé `AFTER`
- E. Un graphe est limité à 10 tasks

### Question 19
Une équipe veut une table d'agrégats qui joint les commandes et les clients, tenue à jour automatiquement avec au plus 5 minutes de retard, sans écrire de planification. Quel objet convient le mieux ?

- A. Une vue matérialisée
- B. Une table dynamique avec `TARGET_LAG = '5 minutes'`
- C. Une table temporaire
- D. Un stream de type append-only

### Question 20
Dans une transaction ouverte par `BEGIN`, on exécute un `UPDATE`, puis un `CREATE TABLE`, puis un `ROLLBACK`. Que devient l'`UPDATE` ?

- A. Il est validé : le `CREATE TABLE` a validé implicitement la transaction en cours
- B. Il est annulé par le `ROLLBACK`
- C. Il reste en attente jusqu'au prochain `COMMIT`
- D. Le `CREATE TABLE` échoue, car le DDL est interdit dans une transaction

---

## Corrigé

| Question | Réponse | Explication | Section du chapitre 18 |
|---|---|---|---|
| 1 | C | `VARIANT` accepte toute valeur ; `OBJECT` ne contient que des paires clé-valeur et `ARRAY` qu'une liste. | 2.1 |
| 2 | A | Deux-points au premier niveau, point ensuite, puis conversion `::VARCHAR` pour retirer les guillemets ; les clés sont sensibles à la casse. | 2.3 |
| 3 | D | Les clés JSON sont sensibles à la casse : une clé introuvable renvoie `NULL`, sans erreur. | 2.3 |
| 4 | B | `FLATTEN` est la fonction de table qui produit une ligne par élément ; `PARSE_JSON` convertit un texte en `VARIANT`. | 2.4 |
| 5 | C | `OUTER => TRUE` conserve la ligne d'entrée quand il n'y a rien à aplatir, comme une jointure externe. | 2.4 |
| 6 | D | `STRIP_OUTER_ARRAY` retire le tableau englobant : chaque élément devient une ligne. | 2.6 |
| 7 | A | `QUALIFY` est aux fonctions de fenêtrage ce que `HAVING` est aux agrégats. | 4.2 |
| 8 | B | `APPROX_COUNT_DISTINCT` estime le nombre de valeurs distinctes avec HyperLogLog. | 4.3 |
| 9 | B, C | Une procédure s'appelle avec `CALL` et peut faire du DDL et du DML ; une UDF s'appelle dans une expression et renvoie toujours une valeur. | 5.3 |
| 10 | D | Par défaut, une procédure s'exécute avec les droits de son propriétaire (`EXECUTE AS OWNER`). | 5.2 |
| 11 | C | Un stream ne contient aucune donnée de table : il mémorise seulement un décalage. | 6.1 |
| 12 | B | Un `UPDATE` apparaît comme une paire `DELETE` et `INSERT` dont `METADATA$ISUPDATE` vaut `TRUE`. | 6.2 |
| 13 | D | Seule une instruction DML validée qui lit le stream fait avancer le décalage ; un `SELECT` ne le consomme pas. | 6.4 |
| 14 | A | Les tables externes n'acceptent que les streams insert-only. | 6.3 |
| 15 | B | Un stream non consommé devient périmé quand son décalage sort de la période de rétention ; il faut le recréer et le consommer régulièrement. | 6.5 |
| 16 | C | Une task est toujours créée suspendue. | 7.1 |
| 17 | A | Sans paramètre `WAREHOUSE`, la task est serverless. | 7.2 |
| 18 | B, D | Un graphe a une seule racine, qui porte la planification ; les enfants utilisent `AFTER` ; la limite est de 1 000 tasks. | 7.3 |
| 19 | B | Une table dynamique accepte les jointures et se rafraîchit seule selon le retard cible ; une vue matérialisée n'accepte qu'une table. | 8.2 |
| 20 | A | Une instruction DDL valide la transaction en cours avant de s'exécuter : le `ROLLBACK` n'a plus rien à annuler. | 9 |

Répartition des bonnes réponses : A 5, B 7, C 5, D 5 (les questions à deux réponses comptent pour deux lettres).

**Lecture du score** : 16 ou plus, le chapitre est acquis ; de 12 à 15, relire les sections des questions ratées ; moins de 12, reprendre le chapitre et refaire l'atelier.
