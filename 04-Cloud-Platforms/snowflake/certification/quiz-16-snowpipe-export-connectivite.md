# Quiz 16 — Stages, Snowpipe, déchargement et connectivité

[← Chapitre 16](../16-snowpipe-export-connectivite.md) | [← Chapitre 11](../11-chargement-stage-copy.md) | [← Sommaire du cours](../README.md)

20 questions au format de l'examen SnowPro Core (COF-C03), domaine 3. Une seule bonne réponse, sauf mention « 2 réponses attendues ». Comptez 25 minutes, sans le cours. Le corrigé est à la fin. Les questions portent sur le chapitre 16 et, pour quelques-unes, sur le chapitre 11.

---

### Question 1
Quelle notation désigne le stage de la table `ORDERS_RAW` ?

- A. `@~ORDERS_RAW`
- B. `@ORDERS_RAW`
- C. `@%ORDERS_RAW`
- D. `@$ORDERS_RAW`

### Question 2
Quelles affirmations sont vraies pour un stage utilisateur ? (2 réponses attendues)

- A. Il est créé automatiquement pour chaque utilisateur
- B. Il peut être partagé avec un rôle par un `GRANT`
- C. Il se supprime avec `DROP STAGE`
- D. Il se référence par `@~`
- E. Il stocke ses fichiers dans le stockage cloud de l'entreprise

### Question 3
Pourquoi utilise-t-on une intégration de stockage pour créer un stage externe ?

- A. Pour accélérer la lecture des fichiers
- B. Pour éviter d'écrire des clés d'accès cloud dans la définition du stage
- C. Pour compresser automatiquement les fichiers
- D. Pour autoriser `PUT` sur un stage externe

### Question 4
Quel est le comportement par défaut de `COPY INTO <table>` lorsqu'une ligne d'un fichier est en erreur ?

- A. `ABORT_STATEMENT` : l'instruction s'arrête et rien n'est chargé
- B. `CONTINUE` : les lignes valides sont chargées
- C. `SKIP_FILE` : le fichier en erreur est ignoré
- D. `SKIP_FILE_10` : le fichier est ignoré à partir de dix erreurs

### Question 5
Quelle est la valeur par défaut de `ON_ERROR` pour un chargement par Snowpipe ?

- A. `ABORT_STATEMENT`
- B. `CONTINUE`
- C. `RETURN_ERRORS`
- D. `SKIP_FILE`

### Question 6
Un ingénieur veut connaître toutes les erreurs que contiendraient les fichiers d'un stage, sans charger aucune ligne. Que doit-il ajouter à son `COPY INTO` ?

- A. `ON_ERROR = CONTINUE`
- B. `FORCE = TRUE`
- C. `VALIDATION_MODE = RETURN_ERRORS`
- D. `PURGE = TRUE`

### Question 7
Quel est l'effet de l'option `PURGE = TRUE` dans un `COPY INTO <table>` ?

- A. Elle vide la table avant le chargement
- B. Elle supprime du stage les fichiers chargés avec succès
- C. Elle efface l'historique de chargement de la table
- D. Elle supprime les lignes en double après le chargement

### Question 8
Pendant combien de temps Snowflake conserve-t-il, dans les métadonnées d'une table, la liste des fichiers chargés par `COPY INTO` ?

- A. 7 jours
- B. 14 jours
- C. 90 jours
- D. 64 jours

### Question 9
Quelle taille de fichier la documentation recommande-t-elle pour un chargement efficace ?

- A. 100 à 250 Mo compressés
- B. 1 à 10 Mo compressés
- C. 1 à 5 Go non compressés
- D. La plus grande possible, pour limiter le nombre de fichiers

### Question 10
Quelles opérations sont permises dans la requête de transformation d'un `COPY INTO <table>` ? (2 réponses attendues)

- A. Filtrer les lignes avec `WHERE`
- B. Réordonner ou omettre des colonnes
- C. Joindre le fichier à une autre table
- D. Agréger avec `GROUP BY`
- E. Convertir le type d'une colonne

### Question 11
Qu'est-ce qui fournit la puissance de calcul d'un chargement par Snowpipe ?

- A. Le warehouse par défaut de l'utilisateur propriétaire du pipe
- B. Un warehouse indiqué dans la définition du pipe
- C. Des ressources serverless fournies et gérées par Snowflake
- D. La couche des services cloud, sans facturation

### Question 12
Des fichiers arrivent en continu dans un espace de stockage cloud et doivent être chargés quelques minutes après leur arrivée, sans orchestrateur. Quelle solution convient ?

- A. Un `COPY INTO` avec `FORCE = TRUE` lancé toutes les heures
- B. Une table externe avec `PURGE = TRUE`
- C. Un `PUT` suivi d'un `GET`
- D. Un pipe avec `AUTO_INGEST = TRUE` sur un stage externe, déclenché par les notifications du stockage

### Question 13
Pendant combien de temps l'historique des fichiers chargés est-il conservé dans les métadonnées d'un pipe ?

- A. 14 jours
- B. 64 jours
- C. 1 jour
- D. 365 jours

### Question 14
En quoi Snowpipe Streaming diffère-t-il de Snowpipe ?

- A. Il utilise un warehouse à la place du calcul serverless
- B. Il charge des lignes envoyées par une application, sans fichier ni stage
- C. Il ne fonctionne qu'avec des fichiers Parquet
- D. Il exige un stage de table

### Question 15
Dans quels formats de fichier peut-on décharger des données avec `COPY INTO <emplacement>` ?

- A. CSV uniquement
- B. CSV, JSON, Avro, ORC, Parquet, XML
- C. CSV, JSON, Parquet
- D. Parquet et ORC

### Question 16
Un `COPY INTO @stage` exporte une grande table sans option particulière. Quel résultat obtient-on ?

- A. Un seul fichier, quelle que soit sa taille
- B. Un fichier par micro-partition de la table
- C. Une erreur : l'option `SINGLE` est obligatoire
- D. Plusieurs fichiers, d'au plus 16 Mo chacun par défaut

### Question 17
Quelle affirmation est vraie pour la commande `GET` ?

- A. Elle télécharge des fichiers d'un stage interne vers le poste, depuis un client comme Snowflake CLI ou SnowSQL
- B. Elle s'exécute dans une feuille SQL de Snowsight
- C. Elle télécharge les fichiers d'un stage externe
- D. Elle charge les fichiers d'un stage dans une table

### Question 18
Quelle affirmation décrit une table externe ?

- A. Ses données sont copiées dans Snowflake à la création
- B. Elle accepte `INSERT` et `UPDATE`
- C. Elle est en lecture seule et ses données restent dans un stage externe
- D. Elle ne peut pas être jointe à une table standard

### Question 19
Une application web doit exécuter des instructions SQL sur Snowflake par des requêtes HTTP, sans installer de pilote. Quel outil utiliser ?

- A. Le pilote ODBC
- B. L'API SQL
- C. SnowSQL
- D. Le connecteur Spark

### Question 20
Après un `DELETE FROM ORDERS_RAW`, un ingénieur relance le `COPY INTO` du même fichier et obtient « 0 files processed ». Que doit-il faire pour recharger proprement, sans option risquée ?

- A. Ajouter `VALIDATION_MODE = RETURN_ERRORS`
- B. Ajouter `PURGE = TRUE`
- C. Recréer le format de fichier
- D. Vider la table avec `TRUNCATE TABLE`, qui efface aussi l'historique de chargement, puis relancer le `COPY INTO`

---

## Corrigé

| Question | Réponse | Explication | Section du chapitre |
|---|---|---|---|
| 1 | C | Un stage de table se note `@%` suivi du nom de la table ; `@~` est le stage utilisateur. | 16, section 1 |
| 2 | A, D | Le stage utilisateur est créé automatiquement et se note `@~` ; il ne se partage pas, ne se supprime pas et reste un stage interne. | 16, section 1 |
| 3 | B | L'intégration de stockage porte une identité autorisée côté cloud : aucune clé d'accès n'est écrite dans le stage. | 16, section 1.1 |
| 4 | A | `ABORT_STATEMENT` est la valeur par défaut d'un chargement par `COPY INTO`. | 16, section 2.3 ; 11, section 6 |
| 5 | D | Snowpipe utilise `SKIP_FILE` par défaut : le fichier en erreur est ignoré en entier. | 16, sections 2.3 et 4.4 |
| 6 | C | `VALIDATION_MODE` lit les fichiers et renvoie les erreurs sans charger ; `ON_ERROR = CONTINUE` chargerait les lignes valides. | 16, section 2.2 |
| 7 | B | `PURGE = TRUE` supprime du stage les fichiers chargés avec succès ; elle ne touche ni la table ni l'historique. | 16, section 2.4 |
| 8 | D | L'historique de chargement d'une table est conservé 64 jours. | 16, section 2.4 ; 11, section 6 |
| 9 | A | La documentation recommande des fichiers d'environ 100 à 250 Mo compressés. | 16, section 3 |
| 10 | B, E | Le chargement permet de choisir, réordonner, omettre et convertir des colonnes ; ni `WHERE`, ni jointure, ni agrégation. | 16, section 2.5 |
| 11 | C | Snowpipe utilise des ressources fournies par Snowflake (serverless), facturées à part, sans warehouse. | 16, section 4.4 |
| 12 | D | L'auto-ingest déclenche le chargement à la notification d'arrivée du fichier ; `FORCE = TRUE` créerait des doublons. | 16, section 4.2 |
| 13 | A | L'historique de chargement d'un pipe est conservé 14 jours, contre 64 jours pour `COPY INTO`. | 16, section 4.4 |
| 14 | B | Snowpipe Streaming reçoit des lignes par un kit de développement ou une API, sans fichier ni stage, avec une latence de quelques secondes. | 16, section 4.5 |
| 15 | C | Le déchargement produit du CSV, du JSON ou du Parquet ; la liste de six formats vaut pour le chargement. | 16, section 5.1 |
| 16 | D | Par défaut `SINGLE = FALSE` et `MAX_FILE_SIZE` vaut 16 Mo : l'export produit plusieurs fichiers. | 16, section 5.1 |
| 17 | A | `GET` rapatrie des fichiers d'un stage interne depuis un client installé ; ni Snowsight ni les stages externes ne le permettent. | 16, section 5.3 |
| 18 | C | Une table externe lit des fichiers restés dans un stage externe ; elle est en lecture seule mais peut être interrogée et jointe. | 16, section 6 |
| 19 | B | L'API SQL est une API REST qui exécute des instructions SQL par requêtes HTTP, sans pilote. | 16, section 7.4 |
| 20 | D | `DELETE` ne remet pas à zéro l'historique de chargement ; `TRUNCATE TABLE` l'efface, ce qui évite de recourir à `FORCE = TRUE`. | 11, section 9 |
