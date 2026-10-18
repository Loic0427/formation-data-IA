# Examen blanc n° 1 — SnowPro Core (COF-C03)

## Consignes

Cet examen blanc reproduit le format de l'examen SnowPro Core : 100 questions, 115 minutes, cinq domaines pondérés. Ce format (nombre de questions, durée, score d'admission de 750 sur 1000, pondérations) est celui de la [page officielle de l'examen en français](https://learn.snowflake.com/en/certifications/snowpro-core-fra-c03/), relevé le 4 octobre 2026.

Conditions de passage :

- Durée : 115 minutes, en une seule fois, chronomètre lancé. Cela représente un peu plus d'une minute par question.
- Sans documentation, sans cours, sans compte Snowflake ouvert.
- Notez vos réponses à part (feuille ou fichier), sous la forme « numéro : lettres ». N'écrivez rien dans ce document.
- Les questions sans mention particulière n'ont qu'une seule bonne réponse. Les questions à choix multiples indiquent « (2 réponses attendues) » ou « (3 réponses attendues) ».
- Ne consultez la grille et le corrigé qu'une fois les 115 minutes écoulées.

## Barème simplifié

- Un point par question entièrement juste. Une question à choix multiples n'est juste que si toutes les lettres attendues sont cochées, et aucune autre.
- Aucun point négatif : répondez à toutes les questions.
- Objectif : au moins 75 bonnes réponses sur 100. L'examen réel utilise un score pondéré sur 1000 avec un seuil à 750 ; le barème « 75 sur 100 » en est une approximation prudente.

## Exploiter le résultat

1. Corrigez avec la grille de réponses, puis reportez vos erreurs dans le tableau de dépouillement (fin du document) pour obtenir un score par domaine.
2. Un domaine en dessous de 70 % de réussite doit être retravaillé : le tableau indique les chapitres du cours correspondants.
3. Lisez le corrigé détaillé de chaque question ratée, mais aussi de chaque question réussie par hasard : notez-les pendant l'épreuve avec un point d'interrogation.
4. Attendez au moins trois jours avant de repasser cet examen, afin de mesurer une compréhension et non un souvenir des réponses.

---

## Questions

### Question 1

Dans l'architecture de Snowflake, quelle couche prend en charge l'authentification, la gestion des métadonnées et l'optimisation des requêtes ?

- A. La couche de stockage (database storage)
- B. La couche de calcul (virtual warehouses)
- C. La couche des services cloud (cloud services)
- D. La couche de réplication

### Question 2

Quel préfixe permet de référencer le stage interne associé automatiquement à une table nommée `ventes` ?

- A. `@~ventes`
- B. `@%ventes`
- C. `@ventes`
- D. `$ventes`

### Question 3

Quel rôle système est dédié uniquement à la gestion des utilisateurs et des rôles, et reçoit directement (sans héritage) les privilèges `CREATE USER` et `CREATE ROLE` ?

- A. SYSADMIN
- B. SECURITYADMIN
- C. PUBLIC
- D. USERADMIN

### Question 4

Un analyste exécute une requête à 9 h. À 11 h, il relance exactement la même requête ; les tables interrogées n'ont pas changé. Le résultat s'affiche presque instantanément, alors que le warehouse est suspendu et ne redémarre pas. Quel mécanisme explique ce comportement ?

- A. Le cache de résultats (result cache), géré par la couche des services cloud
- B. Le cache local du warehouse, conservé pendant la suspension
- C. Une vue matérialisée créée automatiquement par Snowflake
- D. Le service d'optimisation de recherche (search optimization service)

### Question 5

Un warehouse standard de taille Medium, composé d'un seul cluster, fonctionne sans interruption pendant 30 minutes. Combien de crédits consomme-t-il ?

- A. 1 crédit
- B. 2 crédits
- C. 4 crédits
- D. 8 crédits

### Question 6

Quelles affirmations décrivent correctement le partage sécurisé de données (Secure Data Sharing) ? (2 réponses attendues)

- A. Aucune donnée n'est copiée ni transférée vers le compte du consommateur.
- B. Le consommateur paie le stockage des données qui lui sont partagées.
- C. Le consommateur paie le calcul utilisé par ses propres requêtes sur les données partagées.
- D. Le consommateur peut modifier les tables partagées si le fournisseur lui accorde le privilège UPDATE.
- E. Les données sont exportées chaque nuit vers un stage du consommateur.

### Question 7

Quelles affirmations sont exactes à propos des tables temporaires (temporary tables) ? (2 réponses attendues)

- A. Elles sont visibles par toutes les sessions du même utilisateur.
- B. Elles n'existent que pendant la session qui les a créées.
- C. Elles bénéficient de sept jours de Fail-safe.
- D. Elles n'ont pas de période de Fail-safe.
- E. Elles ne génèrent aucun coût de stockage.

### Question 8

Chaque lundi matin, deux cents utilisateurs lancent en même temps des requêtes simples sur le même warehouse de taille Medium. Les requêtes passent beaucoup de temps en file d'attente, mais s'exécutent vite une fois démarrées. Quelle est la solution la plus adaptée ?

- A. Passer le warehouse de la taille Medium à la taille X-Large.
- B. Activer le service d'optimisation de recherche sur les tables interrogées.
- C. Définir une clustering key sur les tables interrogées.
- D. Configurer le warehouse en multi-cluster et augmenter son nombre maximal de clusters.

### Question 9

L'utilisatrice LEA, dont le rôle primaire actif est `DATA_ENG`, crée une table. Qui est propriétaire de cette table ?

- A. L'utilisatrice LEA
- B. Le rôle ACCOUNTADMIN
- C. Le rôle `DATA_ENG`
- D. Le rôle SYSADMIN

### Question 10

Quelle est la valeur par défaut de l'option `ON_ERROR` pour un chargement en masse avec la commande `COPY INTO <table>` ?

- A. `ABORT_STATEMENT`
- B. `CONTINUE`
- C. `SKIP_FILE`
- D. `RETURN_ERRORS`

### Question 11

Quelles affirmations sont exactes à propos du Fail-safe ? (2 réponses attendues)

- A. Sa durée est de sept jours et n'est pas configurable.
- B. Sa durée se règle entre 0 et 90 jours avec le paramètre `DATA_RETENTION_TIME_IN_DAYS`.
- C. L'utilisateur récupère lui-même les données avec la commande `UNDROP`.
- D. Seul le support de Snowflake peut récupérer les données pendant cette période.
- E. Il s'applique aux tables transient comme aux tables permanentes.

### Question 12

La table `commandes` contient une colonne `src` de type VARIANT. Que renvoie la requête suivante ?

```sql
SELECT src:client.ville::STRING FROM commandes;
```

- A. Le contenu complet de la colonne `src`, converti en chaîne de caractères
- B. La valeur de la clé `ville` située dans l'objet `client` de la colonne `src`, convertie en chaîne de caractères
- C. La colonne `ville` de la table `client` du schéma `src`
- D. Une erreur, car l'opérateur `::` n'est pas autorisé sur une colonne VARIANT

### Question 13

Comment décrit-on l'architecture de Snowflake ?

- A. Une architecture shared-nothing pure, où chaque nœud possède son propre stockage
- B. Une architecture shared-disk pure, où un seul cluster de calcul accède au stockage
- C. Une architecture client-serveur classique installée chez le client
- D. Une architecture hybride : un stockage central partagé (shared-disk) et des clusters de calcul indépendants à traitement massivement parallèle (shared-nothing)

### Question 14

Quelles affirmations sont exactes à propos des resource monitors ? (2 réponses attendues)

- A. Ils permettent de plafonner la consommation des fonctionnalités serverless comme Snowpipe.
- B. Par défaut, seul le rôle ACCOUNTADMIN peut en créer.
- C. Ils permettent de plafonner le volume de stockage d'une base de données.
- D. Un même warehouse peut être rattaché à plusieurs resource monitors.
- E. Ils surveillent la consommation de crédits des warehouses.

### Question 15

Une ingénieure veut envoyer un fichier CSV présent sur son poste de travail vers un stage interne nommé, depuis un client en ligne de commande. Quelle commande doit-elle utiliser ?

- A. `COPY INTO`
- B. `GET`
- C. `PUT`
- D. `INSERT`

### Question 16

Dans un compte en édition Enterprise, quelle est la durée maximale de rétention du Time Travel pour une table permanente ?

- A. 1 jour
- B. 7 jours
- C. 30 jours
- D. 90 jours

### Question 17

Un développeur crée une task planifiée toutes les dix minutes avec `CREATE TASK`. Une heure plus tard, elle ne s'est jamais exécutée. Quelle est la cause la plus probable ?

- A. Une task ne peut pas être planifiée à moins d'une heure d'intervalle.
- B. Une task est créée à l'état suspendu ; il faut l'activer avec `ALTER TASK ... RESUME`.
- C. Une task ne s'exécute que si un stream lui est associé.
- D. Une task exige un warehouse de taille Large au minimum.

### Question 18

Quelles affirmations sont exactes à propos des comptes lecteurs (reader accounts) ? (2 réponses attendues)

- A. Les crédits consommés par le compte lecteur sont facturés au consommateur.
- B. Ils nécessitent l'édition Business Critical chez le consommateur.
- C. Ils sont créés et gérés par le fournisseur des données.
- D. Les crédits consommés par le compte lecteur sont facturés au fournisseur.
- E. Un compte lecteur peut consommer les données de n'importe quel fournisseur.

### Question 19

Une équipe clone une table de 2 To avec `CREATE TABLE ... CLONE`. Quel est l'effet sur le stockage facturé au moment de la création du clone ?

- A. Aucun stockage supplémentaire : le clone référence les micro-partitions existantes, et seules les modifications ultérieures consomment du stockage.
- B. 2 To supplémentaires, car les données sont copiées physiquement.
- C. 1 To supplémentaire, car le clone est compressé deux fois plus.
- D. 2 To supplémentaires pendant sept jours, puis plus rien.

### Question 20

Quel rôle système détient par défaut le privilège global `MANAGE GRANTS`, qui permet d'accorder ou de révoquer n'importe quel privilège ?

- A. USERADMIN
- B. SYSADMIN
- C. SECURITYADMIN
- D. PUBLIC

### Question 21

Un warehouse est configuré avec une suspension automatique après 60 secondes d'inactivité. Les utilisateurs constatent que la première requête après chaque reprise est plus lente que les suivantes, alors que les données n'ont pas changé. Quelle est l'explication ?

- A. Le cache de résultats est vidé à chaque suspension du warehouse.
- B. Le cache des métadonnées est reconstruit à chaque reprise du warehouse.
- C. Le Time Travel est recalculé à chaque reprise du warehouse.
- D. Le cache local du warehouse est perdu à la suspension ; les données doivent être relues depuis le stockage distant.

### Question 22

Quelle est l'édition minimale de Snowflake requise pour utiliser les warehouses multi-cluster ?

- A. Standard
- B. Enterprise
- C. Business Critical
- D. Virtual Private Snowflake

### Question 23

Par quels moyens Snowpipe peut-il être informé de l'arrivée de nouveaux fichiers à charger ? (2 réponses attendues)

- A. Des notifications d'événements émises par le stockage cloud (auto-ingest)
- B. Une planification CRON définie dans l'objet pipe
- C. Un appel à l'API REST de Snowpipe par une application cliente
- D. Un stream créé sur le stage
- E. La reprise du warehouse associé au pipe

### Question 24

Lequel de ces objets est créé au niveau du compte, et non à l'intérieur d'un schéma ?

- A. Un file format
- B. Un stage nommé
- C. Un pipe
- D. Un warehouse

### Question 25

Sans dupliquer la table ni créer de vue, une équipe veut que la colonne `email` apparaisse en clair pour le rôle `RH` et masquée pour tous les autres rôles. Quelle fonctionnalité répond à ce besoin ?

- A. Une masking policy appliquée à la colonne
- B. Une row access policy appliquée à la table
- C. Une network policy appliquée au compte
- D. Un resource monitor appliqué au warehouse

### Question 26

La colonne VARIANT `v` contient, pour chaque commande, un tableau JSON `articles`. Quelle construction produit une ligne par article ?

- A. `SELECT PARSE_JSON(v:articles) FROM commandes;`
- B. `SELECT ARRAY_SIZE(v:articles) FROM commandes;`
- C. `SELECT f.value FROM commandes, LATERAL FLATTEN(input => v:articles) f;`
- D. `SELECT OBJECT_CONSTRUCT(v:articles) FROM commandes;`

### Question 27

Un warehouse est démarré, exécute une requête de 20 secondes, puis est suspendu aussitôt. Quelle durée est facturée ?

- A. 20 secondes
- B. 60 secondes
- C. Une heure entière
- D. Rien, car la durée est inférieure à une minute

### Question 28

Lundi, une commande `COPY INTO ventes FROM @stage_ventes` charge dix fichiers. Mardi, la même commande est relancée alors que les dix fichiers sont toujours dans le stage, inchangés, et qu'aucune option particulière n'est précisée. Que se passe-t-il ?

- A. Les dix fichiers sont chargés une seconde fois, ce qui duplique les lignes.
- B. La commande échoue avec une erreur de doublon.
- C. Les dix fichiers sont supprimés du stage.
- D. Aucun fichier n'est rechargé, car les métadonnées de chargement de la table indiquent qu'ils ont déjà été chargés.

### Question 29

Un consommateur a créé une base de données à partir d'un share. Il souhaite corriger certaines valeurs dans une table partagée. Que doit-il faire ?

- A. Exécuter un `UPDATE` directement sur la table partagée.
- B. Copier les données dans une table de son propre compte, par exemple avec `CREATE TABLE ... AS SELECT`, puis modifier cette copie.
- C. Cloner la table partagée, puis modifier le clone.
- D. Demander au fournisseur le privilège OWNERSHIP sur la table partagée.

### Question 30

Quelles affirmations sont exactes à propos des vues sécurisées (secure views) ? (2 réponses attendues)

- A. Elles stockent physiquement le résultat de leur requête.
- B. Leur définition n'est pas visible par les rôles qui n'en sont pas propriétaires.
- C. Elles sont toujours plus rapides que les vues standard.
- D. Elles exigent l'édition Business Critical.
- E. Certaines optimisations de requête sont désactivées, ce qui peut les rendre plus lentes qu'une vue standard.

### Question 31

Quelles affirmations sont exactes lorsque l'on compare le schéma ACCOUNT_USAGE de la base SNOWFLAKE et l'INFORMATION_SCHEMA d'une base de données ? (2 réponses attendues)

- A. Les vues de l'INFORMATION_SCHEMA ont une latence de 45 minutes à 3 heures.
- B. Les vues d'ACCOUNT_USAGE n'ont aucune latence.
- C. Les vues d'ACCOUNT_USAGE incluent les objets supprimés.
- D. Les vues d'historique d'ACCOUNT_USAGE conservent les données pendant 365 jours.
- E. Les fonctions d'historique de l'INFORMATION_SCHEMA conservent les données pendant deux ans.

### Question 32

Dans le profil d'une requête lente comportant de grosses jointures et agrégations, on lit une valeur élevée pour « Bytes spilled to remote storage ». La requête ne peut pas être simplifiée. Quelle action est la plus adaptée ?

- A. Utiliser un warehouse de taille supérieure, qui dispose de plus de mémoire.
- B. Ajouter des clusters au warehouse multi-cluster.
- C. Réduire le délai de suspension automatique du warehouse.
- D. Désactiver le cache de résultats.

### Question 33

Dans un compte en édition Standard, quelle est la durée maximale de rétention du Time Travel pour une table permanente ?

- A. 1 jour
- B. 7 jours
- C. 14 jours
- D. 90 jours

### Question 34

Quels formats de fichier sont pris en charge pour le déchargement de données avec `COPY INTO <location>` ? (3 réponses attendues)

- A. CSV (fichiers délimités)
- B. AVRO
- C. JSON
- D. ORC
- E. PARQUET

### Question 35

Un stream standard est créé sur une table. Une ligne de cette table est ensuite modifiée par un `UPDATE`. Comment cette modification apparaît-elle dans le stream ?

- A. Une seule ligne avec `METADATA$ACTION = 'UPDATE'`
- B. Une seule ligne avec `METADATA$ACTION = 'INSERT'` et `METADATA$ISUPDATE = FALSE`
- C. Aucune ligne : un stream standard ne suit que les insertions
- D. Deux lignes, l'une avec `METADATA$ACTION = 'DELETE'`, l'autre avec `METADATA$ACTION = 'INSERT'`, toutes deux avec `METADATA$ISUPDATE = TRUE`

### Question 36

La table `clients` a été supprimée par erreur, puis une nouvelle table vide portant le même nom a été créée. La période de Time Travel n'est pas écoulée. Comment restaurer la table d'origine ?

- A. Exécuter `UNDROP TABLE clients` : la nouvelle table est remplacée automatiquement.
- B. C'est impossible : la création d'une table du même nom efface l'historique.
- C. Renommer la nouvelle table, puis exécuter `UNDROP TABLE clients`.
- D. Contacter le support de Snowflake pour une restauration par le Fail-safe.

### Question 37

Quelles affirmations sont exactes à propos des network policies ? (2 réponses attendues)

- A. Plusieurs network policies peuvent être actives simultanément au niveau du compte.
- B. Si une adresse IP figure à la fois dans la liste autorisée et dans la liste bloquée, elle est bloquée.
- C. Seul le rôle ORGADMIN peut créer une network policy.
- D. Une seule network policy peut être associée au compte à un instant donné.
- E. Elles ne s'appliquent qu'aux connexions passant par Snowsight.

### Question 38

Quelle affirmation décrit correctement une table externe (external table) ?

- A. Ses données sont stockées dans Snowflake et bénéficient du Fail-safe.
- B. Elle accepte les commandes `INSERT`, `UPDATE` et `DELETE` comme une table standard.
- C. Elle est en lecture seule et référence des fichiers situés dans un stage externe.
- D. Elle n'existe que pendant la session qui l'a créée.

### Question 39

Que fait la commande suivante ?

```sql
COPY INTO ventes FROM @stage_ventes VALIDATION_MODE = RETURN_ERRORS;
```

- A. Elle charge les lignes valides et renvoie la liste des lignes rejetées.
- B. Elle charge toutes les lignes, puis annule le chargement si une erreur est détectée.
- C. Elle supprime du stage les fichiers contenant des erreurs.
- D. Elle valide les fichiers et renvoie les erreurs rencontrées, sans charger aucune donnée.

### Question 40

Parmi les conditions suivantes, lesquelles sont nécessaires pour qu'une requête réutilise le cache de résultats ? (2 réponses attendues)

- A. La requête doit s'exécuter sur le même warehouse que la requête initiale.
- B. Le texte de la requête doit être strictement identique à celui de la requête initiale.
- C. La requête doit être lancée par le même utilisateur que la requête initiale.
- D. Le warehouse doit être de taille Medium ou supérieure.
- E. Les données des tables interrogées ne doivent pas avoir changé depuis la requête initiale.

### Question 41

Une entreprise recherche des jeux de données météorologiques et démographiques publiés par des fournisseurs tiers, utilisables directement dans son compte sans mettre en place de pipeline. Vers quoi doit-elle se tourner ?

- A. Les vues ACCOUNT_USAGE de la base SNOWFLAKE
- B. Un stage externe public
- C. Snowflake Marketplace
- D. Un compte lecteur (reader account) qu'elle crée elle-même

### Question 42

Quelles affirmations sont exactes à propos des micro-partitions ? (2 réponses attendues)

- A. Elles doivent être définies manuellement avec une clause `PARTITION BY` à la création de la table.
- B. Chacune contient entre 50 et 500 Mo de données non compressées.
- C. Elles sont modifiées sur place lors d'un `UPDATE`.
- D. Les données y sont organisées en colonnes, et Snowflake conserve des métadonnées sur les valeurs de chaque colonne (plages de valeurs notamment).
- E. Elles ont une taille fixe de 16 Mo compressés.

### Question 43

Un script d'ingestion tourne chaque nuit sans intervention humaine. L'équipe sécurité refuse l'usage d'un mot de passe. Quelle méthode d'authentification est la plus adaptée ?

- A. L'authentification multifacteur avec validation sur téléphone
- B. L'authentification par paire de clés (key-pair authentication)
- C. L'authentification unique (SSO) par navigateur
- D. Un mot de passe partagé entre les membres de l'équipe

### Question 44

Une table de plusieurs milliards de lignes est interrogée par des requêtes très sélectives du type `WHERE id_transaction = '...'`, sur une colonne à très forte cardinalité qui ne correspond pas à l'ordre de chargement des données. Chaque requête ne renvoie que quelques lignes. Quelle fonctionnalité est conçue pour ce cas ?

- A. Un warehouse multi-cluster
- B. Le cache de résultats
- C. Le service d'optimisation de recherche (search optimization service)
- D. Une vue sécurisée

### Question 45

Une table de préparation est rechargée intégralement chaque nuit depuis les fichiers sources. Elle doit rester accessible plusieurs jours à toutes les sessions, mais l'équipe veut réduire au minimum les coûts de stockage liés à la protection des données. Quel type de table choisir ?

- A. Une table permanente
- B. Une table temporaire
- C. Une table transient
- D. Une table externe

### Question 46

Par défaut, `COPY INTO <location>` répartit les données déchargées en plusieurs fichiers. Quelle option permet d'obtenir un seul fichier ?

- A. `SINGLE = TRUE`
- B. `PURGE = TRUE`
- C. `FORCE = TRUE`
- D. `OVERWRITE = TRUE`

### Question 47

Quelle description correspond à Snowpark ?

- A. Un outil graphique de création de tableaux de bord intégré à Snowsight
- B. Un moteur Spark hébergé que le client doit dimensionner lui-même
- C. Un service de chargement continu de fichiers
- D. Un ensemble de bibliothèques (Python, Java, Scala) offrant une API DataFrame dont les traitements sont exécutés dans Snowflake

### Question 48

Une table `ventes` contient les données de toutes les régions. Chaque responsable régional ne doit voir que les lignes de sa région lorsqu'il interroge la table, sans que l'on crée une vue par région. Quelle fonctionnalité utiliser ?

- A. Une row access policy
- B. Une masking policy
- C. Un tag
- D. Une network policy

### Question 49

Une task doit s'exécuter toutes les cinq minutes, mais seulement si le stream `s_commandes` contient de nouvelles données. Quelle clause compléter dans la définition de la task ?

```sql
CREATE TASK t_commandes
  WAREHOUSE = wh_etl
  SCHEDULE = '5 MINUTE'
  ______
AS
  INSERT INTO commandes_hist SELECT * FROM s_commandes;
```

- A. `AFTER s_commandes`
- B. `IF EXISTS (SELECT 1 FROM s_commandes)`
- C. `WHEN SYSTEM$STREAM_HAS_DATA('s_commandes')`
- D. `TARGET_LAG = '5 minutes'`

### Question 50

Dans un compte Enterprise, une table permanente dont la rétention Time Travel est d'un jour a été supprimée il y a trois jours. Aucun clone ni sauvegarde n'existe. Comment tenter de récupérer les données ?

- A. Exécuter `UNDROP TABLE`.
- B. Contacter le support de Snowflake : les données sont dans la période de Fail-safe.
- C. Interroger la table avec la clause `AT (OFFSET => ...)`.
- D. Augmenter `DATA_RETENTION_TIME_IN_DAYS` à 90, puis exécuter `UNDROP TABLE`.

### Question 51

Un pipe Snowpipe est créé sans préciser l'option `ON_ERROR`. Un fichier contenant des lignes invalides arrive dans le stage. Quel est le comportement par défaut ?

- A. Le chargement s'arrête et le pipe est suspendu (`ABORT_STATEMENT`).
- B. Les lignes valides sont chargées et les lignes invalides ignorées (`CONTINUE`).
- C. Le fichier est supprimé du stage.
- D. Le fichier en erreur est ignoré (`SKIP_FILE`).

### Question 52

Une entreprise veut pouvoir basculer son activité sur un compte Snowflake situé dans une autre région en cas de panne régionale (failover et failback). Quelle est l'édition minimale requise ?

- A. Standard
- B. Enterprise
- C. Business Critical
- D. Aucune édition ne le permet ; il faut passer par un déchargement et un rechargement.

### Question 53

Comment la consommation de la couche des services cloud est-elle facturée ?

- A. Elle n'est facturée que pour la part qui dépasse 10 % de la consommation quotidienne de crédits des warehouses.
- B. Elle est toujours facturée intégralement, en plus des warehouses.
- C. Elle n'est jamais facturée.
- D. Elle est facturée au volume de données stockées, en téraoctets par mois.

### Question 54

Un rôle dispose déjà du privilège USAGE sur un warehouse. Quels privilèges faut-il lui accorder, au minimum, pour qu'il puisse exécuter `SELECT * FROM ventes_db.public.commandes` ? (3 réponses attendues)

- A. USAGE sur la base de données `ventes_db`
- B. OWNERSHIP sur la table `commandes`
- C. USAGE sur le schéma `public`
- D. SELECT sur la table `commandes`
- E. MONITOR sur la base de données `ventes_db`

### Question 55

Une table de plusieurs téraoctets est presque toujours filtrée sur la colonne `date_evenement`. Dans le profil d'une requête portant sur une seule journée, on lit « Partitions scanned : 48 210 » et « Partitions total : 48 300 ». Quelle action est la plus adaptée ?

- A. Ajouter des clusters au warehouse.
- B. Définir une clustering key sur `date_evenement`.
- C. Allonger la durée de rétention du Time Travel.
- D. Transformer la table en table transient.

### Question 56

Que fait la commande suivante ?

```sql
CREATE TABLE commandes_restore CLONE commandes AT (OFFSET => -3600);
```

- A. Elle crée un clone de `commandes` qui sera supprimé automatiquement au bout d'une heure.
- B. Elle crée un clone de `commandes` limité aux 3 600 premières lignes.
- C. Elle réplique `commandes` vers un autre compte avec une heure de décalage.
- D. Elle crée un clone de `commandes` dans l'état où la table se trouvait une heure plus tôt.

### Question 57

Quelles affirmations sont exactes à propos de la commande `PUT` ? (2 réponses attendues)

- A. Par défaut, elle compresse en gzip les fichiers qui ne sont pas déjà compressés.
- B. Elle permet d'envoyer des fichiers locaux directement vers un stage externe Amazon S3.
- C. Elle charge les données directement dans la table cible.
- D. Les fichiers envoyés sont chiffrés automatiquement.
- E. Elle supprime le fichier local une fois le transfert terminé.

### Question 58

Un administrateur vient d'exécuter une requête il y a cinq minutes. Il ne la retrouve pas dans la vue `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY`. Quelle est l'explication ?

- A. La vue ne contient que les requêtes en échec.
- B. La vue ne contient que les requêtes du rôle ACCOUNTADMIN.
- C. Les vues d'ACCOUNT_USAGE ont une latence ; pour `QUERY_HISTORY`, elle peut atteindre 45 minutes.
- D. La requête a été servie par le cache de résultats et n'est donc jamais enregistrée.

### Question 59

Une équipe veut résumer et traduire des commentaires clients directement dans une requête SQL, à l'aide d'un grand modèle de langage, sans déployer d'infrastructure. Quelle offre de Snowflake correspond à ce besoin ?

- A. Les fonctions d'IA de Snowflake Cortex (Cortex AI Functions)
- B. Le service d'optimisation de recherche
- C. Snowpipe Streaming
- D. Les vues matérialisées

### Question 60

Quelles affirmations sont exactes à propos des vues matérialisées ? (2 réponses attendues)

- A. Elles doivent être rafraîchies manuellement par une task planifiée.
- B. Elles sont disponibles dès l'édition Standard.
- C. Leur requête de définition ne peut porter que sur une seule table (pas de jointure).
- D. Leurs résultats peuvent être périmés lorsqu'on les interroge juste après une modification de la table de base.
- E. Leur maintenance est assurée automatiquement par un service d'arrière-plan, qui consomme des crédits.

### Question 61

Un fournisseur dont le compte est hébergé sur AWS en Europe veut partager des données avec un consommateur dont le compte est hébergé sur Azure aux États-Unis. Quelle affirmation est exacte ?

- A. Un share direct fonctionne tel quel entre toutes les régions et tous les clouds, sans réplication ni configuration supplémentaire.
- B. C'est impossible tant que le consommateur n'a pas migré son compte vers le cloud et la région du fournisseur.
- C. Le fournisseur doit cloner sa base de données dans la région du consommateur, puis ajouter le clone au share.
- D. Un share direct est limité à une même région : les données doivent d'abord être répliquées vers la région du consommateur.

### Question 62

Un warehouse passe de la taille Small à la taille Large pendant que des requêtes sont en cours d'exécution. Quel est l'effet du redimensionnement ?

- A. Les requêtes en cours sont annulées, puis relancées sur la nouvelle taille.
- B. Les requêtes en cours se terminent avec les ressources d'origine ; les requêtes en file d'attente et les nouvelles requêtes utilisent les ressources supplémentaires.
- C. Les requêtes en cours bénéficient immédiatement des ressources supplémentaires.
- D. Le redimensionnement est refusé tant que le warehouse n'est pas suspendu.

### Question 63

Quelle option de `COPY INTO <table>` supprime automatiquement du stage les fichiers chargés avec succès ?

- A. `PURGE = TRUE`
- B. `FORCE = TRUE`
- C. `OVERWRITE = TRUE`
- D. `TRUNCATECOLUMNS = TRUE`

### Question 64

Une équipe crée des rôles personnalisés qui seront propriétaires de bases de données et de tables. Selon les bonnes pratiques, à quel rôle système faut-il rattacher (accorder) ces rôles personnalisés, afin que les administrateurs système puissent gérer tous les objets du compte ?

- A. ACCOUNTADMIN
- B. SYSADMIN
- C. USERADMIN
- D. PUBLIC

### Question 65

Un warehouse multi-cluster en mode auto-scale utilise la politique de mise à l'échelle Economy. Dans quelle condition Snowflake démarre-t-il un cluster supplémentaire ?

- A. Dès qu'une requête est placée en file d'attente
- B. À heure fixe, selon un calendrier défini par l'administrateur
- C. Seulement si le système estime que la charge suffira à occuper ce cluster pendant au moins six minutes
- D. Jamais : la politique Economy désactive l'ajout de clusters

### Question 66

Une table standard est créée ainsi :

```sql
CREATE TABLE clients (
  id INT PRIMARY KEY,
  nom STRING NOT NULL
);
```

On exécute ensuite deux fois `INSERT INTO clients VALUES (1, 'Dupont');`. Que se passe-t-il ?

- A. Les deux insertions réussissent : sur une table standard, la contrainte PRIMARY KEY n'est pas appliquée ; seule NOT NULL l'est.
- B. La seconde insertion échoue pour violation de clé primaire.
- C. La seconde insertion remplace la première ligne.
- D. La création de la table échoue, car les clés primaires ne sont pas acceptées par Snowflake.

### Question 67

Quelles affirmations sont exactes à propos du stockage des données d'une table standard dans Snowflake ? (2 réponses attendues)

- A. Les données sont réorganisées dans un format en colonnes, compressé et optimisé par Snowflake.
- B. Le client peut lire directement les fichiers de données dans le stockage cloud sous-jacent.
- C. Le stockage est facturé en fonction de la taille du warehouse utilisé pour le chargement.
- D. Les données sont chiffrées au repos par défaut, quelle que soit l'édition.
- E. Le client doit créer et maintenir des index pour accélérer les requêtes.

### Question 68

Un fichier JSON a la forme `[ {...}, {...}, {...} ]` : un seul tableau englobant tous les enregistrements. Quelle option du file format permet de charger chaque enregistrement dans une ligne distincte ?

- A. `SKIP_HEADER = 1`
- B. `FIELD_OPTIONALLY_ENCLOSED_BY = '"'`
- C. `STRIP_OUTER_ARRAY = TRUE`
- D. `PURGE = TRUE`

### Question 69

Un resource monitor doit suspendre un warehouse lorsque son quota est atteint, tout en laissant se terminer les requêtes déjà en cours d'exécution. Quelle action configurer ?

- A. NOTIFY
- B. SUSPEND
- C. SUSPEND_IMMEDIATE
- D. ABORT_STATEMENT

### Question 70

Un développeur exécute plusieurs fois `SELECT * FROM s_commandes` sur un stream, sans autre opération. Il obtient à chaque fois les mêmes lignes. Pourquoi ?

- A. Le stream est périmé (stale).
- B. Un stream ne se vide qu'au bout de 24 heures.
- C. Il faut exécuter `ALTER STREAM ... REFRESH` pour avancer la position du stream.
- D. Une simple interrogation n'avance pas la position (offset) du stream ; il faut consommer le stream dans une instruction DML.

### Question 71

Un fournisseur a ajouté le compte d'un consommateur à son share `partage_ventes`. Quelle commande le consommateur doit-il exécuter pour pouvoir interroger les données ?

- A. `CREATE DATABASE ventes_partagees FROM SHARE fournisseur.partage_ventes;`
- B. `CREATE TABLE ventes_partagees CLONE fournisseur.partage_ventes;`
- C. `COPY INTO ventes_partagees FROM SHARE fournisseur.partage_ventes;`
- D. `CREATE SHARE ventes_partagees FROM fournisseur.partage_ventes;`

### Question 72

Une entreprise exige que les connexions à Snowflake passent par une connectivité privée (AWS PrivateLink, Azure Private Link ou Google Cloud Private Service Connect) plutôt que par l'internet public. Quelle est l'édition minimale requise ?

- A. Standard
- B. Enterprise
- C. Business Critical
- D. Cette option n'existe dans aucune édition.

### Question 73

Une équipe de gouvernance veut que toute colonne portant le tag `pii = 'email'` soit masquée automatiquement, y compris les colonnes qui recevront ce tag à l'avenir, sans attacher une politique colonne par colonne. Quelle approche utiliser ?

- A. Créer une row access policy sur chaque table concernée.
- B. Créer une vue sécurisée par table concernée.
- C. Créer une network policy associée au tag.
- D. Associer une masking policy au tag (tag-based masking).

### Question 74

Quelles affirmations sont exactes lorsque l'on compare les fonctions définies par l'utilisateur (UDF) et les procédures stockées ? (2 réponses attendues)

- A. Une procédure stockée s'exécute avec la commande `CALL`.
- B. Une UDF renvoie une valeur et peut être utilisée comme expression dans une instruction `SELECT`.
- C. Une UDF est le moyen recommandé pour exécuter des instructions DDL telles que `CREATE TABLE`.
- D. Une procédure stockée doit obligatoirement renvoyer une table.
- E. Les procédures stockées ne peuvent être écrites qu'en JavaScript.

### Question 75

Un administrateur veut créer un stage externe sur un bucket Amazon S3 sans inscrire de clés d'accès dans la définition du stage. Quel objet doit-il utiliser ?

- A. Un file format
- B. Une storage integration
- C. Une network policy
- D. Un resource monitor

### Question 76

Quelle affirmation est exacte à propos d'une vue standard (non matérialisée) ?

- A. Elle stocke le résultat de sa requête et le met à jour toutes les heures.
- B. Elle exige l'édition Enterprise.
- C. Elle ne stocke aucune donnée : sa requête de définition est exécutée chaque fois que la vue est interrogée.
- D. Elle dispose de sa propre période de Fail-safe, distincte de celle des tables sous-jacentes.

### Question 77

Une équipe data veut développer en Python une application web interactive (filtres, graphiques) hébergée et exécutée dans Snowflake, sans gérer de serveur. Quelle fonctionnalité utiliser ?

- A. Snowpipe
- B. Streamlit in Snowflake
- C. SnowSQL
- D. Une table dynamique

### Question 78

Un administrateur veut permettre au rôle `ANALYSTE_COUTS` d'interroger les vues du schéma ACCOUNT_USAGE. Quelle commande convient ?

- A. `GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE ANALYSTE_COUTS;`
- B. `GRANT OWNERSHIP ON DATABASE SNOWFLAKE TO ROLE ANALYSTE_COUTS;`
- C. `GRANT SELECT ON ALL TABLES IN ACCOUNT TO ROLE ANALYSTE_COUTS;`
- D. `GRANT ROLE ORGADMIN TO ROLE ANALYSTE_COUTS;`

### Question 79

Une équipe veut déclarer un pipeline de transformation sous la forme d'une simple requête `SELECT`, et laisser Snowflake maintenir le résultat à jour avec un retard maximal de dix minutes par rapport aux tables sources, sans écrire ni streams ni tasks. Quel objet créer ?

- A. Une vue sécurisée
- B. Une table externe avec `AUTO_REFRESH = TRUE`
- C. Une table temporaire
- D. Une table dynamique (dynamic table) avec `TARGET_LAG = '10 minutes'`

### Question 80

Pendant combien de temps Snowpipe conserve-t-il l'historique de chargement des fichiers dans les métadonnées du pipe ?

- A. 7 jours
- B. 14 jours
- C. 64 jours
- D. 365 jours

### Question 81

Une base de données est répliquée vers un compte secondaire. Quelle affirmation décrit la base secondaire tant qu'elle n'a pas été promue ?

- A. Elle est accessible en lecture et en écriture, et les modifications sont fusionnées avec la base primaire.
- B. Elle est inaccessible tant que la base primaire fonctionne.
- C. Elle est en lecture seule.
- D. Elle est supprimée automatiquement après sept jours sans bascule.

### Question 82

Une équipe veut exécuter dans Snowflake un modèle de machine learning empaqueté dans une image de conteneur, avec accès à des GPU. Quelle fonctionnalité correspond à ce besoin ?

- A. Snowpark Container Services
- B. Les tasks serverless
- C. Le service d'accélération des requêtes (query acceleration service)
- D. Les tables hybrides

### Question 83

Une entreprise utilise un fournisseur d'identité (Okta ou Microsoft Entra ID) et veut que les utilisateurs et les groupes y soient créés, modifiés et désactivés automatiquement dans Snowflake. Quel mécanisme utiliser ?

- A. L'authentification par paire de clés
- B. Une network policy
- C. L'authentification multifacteur
- D. SCIM

### Question 84

Dans quels cas la définition d'une clustering key est-elle pertinente ? (2 réponses attendues)

- A. La table ne contient que quelques mégaoctets de données.
- B. La table contient plusieurs téraoctets de données.
- C. La plupart des requêtes filtrent ou joignent sur les colonnes envisagées pour la clé.
- D. La table est modifiée en permanence par des DML et n'est presque jamais interrogée.
- E. La table est une table temporaire utilisée pour une seule requête.

### Question 85

Des fichiers Parquet contiennent les mêmes colonnes que la table cible, mais dans un ordre différent. Quelle option de `COPY INTO <table>` permet de charger chaque colonne du fichier dans la colonne de la table qui porte le même nom ?

- A. `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE`
- B. `FORCE = TRUE`
- C. `ON_ERROR = CONTINUE`
- D. `VALIDATION_MODE = RETURN_ERRORS`

### Question 86

Quelles affirmations caractérisent Snowflake en tant que service entièrement géré ? (2 réponses attendues)

- A. Snowflake peut être installé sur les serveurs du client, dans son propre centre de données.
- B. Le client doit créer et entretenir des index pour obtenir de bonnes performances.
- C. Le client n'a aucun matériel ni logiciel à installer, configurer ou administrer.
- D. Le client doit obligatoirement fournir un réseau privé virtuel dédié pour héberger les warehouses.
- E. La maintenance et les mises à jour de la plateforme sont assurées par Snowflake.

### Question 87

Quelle affirmation décrit correctement la durée de conservation d'un résultat dans le cache de résultats ?

- A. 1 heure, non renouvelable
- B. 24 heures, non renouvelables
- C. 24 heures, période réinitialisée à chaque réutilisation du résultat, dans la limite de 31 jours après la première exécution
- D. 7 jours, période réinitialisée à chaque réutilisation, sans limite

### Question 88

Dans un schéma créé avec l'option `WITH MANAGED ACCESS`, qui peut accorder des privilèges sur les objets du schéma ?

- A. Le propriétaire du schéma, ou un rôle disposant du privilège `MANAGE GRANTS`
- B. Le propriétaire de chaque objet, comme dans un schéma standard
- C. Uniquement le rôle ORGADMIN
- D. N'importe quel rôle disposant du privilège USAGE sur le schéma

### Question 89

Quelle description correspond à une table Apache Iceberg dans Snowflake ?

- A. Une table transactionnelle à faible latence dont les clés primaires sont appliquées
- B. Une table dont les données sont effacées à la fin de la session
- C. Une table dont le contenu est maintenu automatiquement à partir d'une requête
- D. Une table au format de table ouvert, lisible par d'autres moteurs, dont les fichiers résident le plus souvent dans le stockage cloud du client

### Question 90

Quelle commande télécharge des fichiers d'un stage interne vers un répertoire du poste local ?

- A. `PUT`
- B. `COPY INTO <location>`
- C. `GET`
- D. `LIST`

### Question 91

Une équipe a besoin d'une copie de sa base de production dans un compte Snowflake situé dans une autre région, synchronisée régulièrement. Quelle fonctionnalité utiliser ?

- A. Le clonage zéro-copie (`CREATE DATABASE ... CLONE`)
- B. La réplication de base de données
- C. Le Time Travel
- D. Le Fail-safe

### Question 92

Comment configure-t-on un warehouse multi-cluster en mode Maximized ?

- A. En choisissant la politique de mise à l'échelle Economy
- B. En fixant le nombre minimal de clusters à 1 et le nombre maximal à 10
- C. En désactivant la suspension automatique
- D. En donnant la même valeur, supérieure à 1, au nombre minimal et au nombre maximal de clusters

### Question 93

Quelles affirmations décrivent correctement les modèles de contrôle d'accès de Snowflake ? (2 réponses attendues)

- A. Contrôle d'accès discrétionnaire (DAC) : chaque objet a un propriétaire, qui peut accorder l'accès à cet objet.
- B. Contrôle d'accès discrétionnaire (DAC) : l'accès est décidé par le niveau de sensibilité attribué à chaque utilisateur.
- C. Contrôle d'accès basé sur les rôles (RBAC) : un utilisateur ne peut se voir accorder qu'un seul rôle.
- D. Contrôle d'accès basé sur les rôles (RBAC) : les privilèges sont accordés à des rôles, et les rôles sont accordés aux utilisateurs.
- E. Par défaut, l'accès à un objet est autorisé tant qu'il n'a pas été révoqué.

### Question 94

Un `DELETE` exécuté par erreur a vidé une partie de la table `factures`. On connaît l'identifiant de cette requête. Quelle requête permet de lire la table telle qu'elle était juste avant le `DELETE` ?

- A. `SELECT * FROM factures BEFORE (STATEMENT => '<query_id>');`
- B. `SELECT * FROM factures AT (STATEMENT => '<query_id>');`
- C. `SELECT * FROM TABLE(RESULT_SCAN('<query_id>'));`
- D. `UNDROP TABLE factures;`

### Question 95

Une entreprise veut alimenter des tables Snowflake à partir de topics Apache Kafka, sans développer son propre consommateur. Quel composant fourni par Snowflake utiliser ?

- A. Le pilote ODBC
- B. Le Snowflake Connector for Kafka
- C. SnowSQL
- D. Une table externe

### Question 96

Une network policy est active au niveau du compte. Une autre network policy, différente, est associée à l'utilisateur `SVC_ETL`. Laquelle s'applique aux connexions de `SVC_ETL` ?

- A. Celle du compte, qui prime toujours
- B. Les deux à la fois : la connexion doit satisfaire les deux politiques
- C. Celle de l'utilisateur, qui prime sur celle du compte
- D. Aucune : le conflit désactive les deux politiques

### Question 97

Sur une table standard, on veut un stream qui ne capture que les insertions, sans enregistrer les mises à jour ni les suppressions. Quelle commande convient ?

- A. `CREATE STREAM s ON TABLE t INSERT_ONLY = TRUE;`
- B. `CREATE STREAM s ON TABLE t APPEND_ONLY = TRUE;`
- C. `CREATE STREAM s ON TABLE t SHOW_INITIAL_ROWS = TRUE;`
- D. `CREATE STREAM s ON TABLE t;`

### Question 98

Pour optimiser un chargement en masse avec `COPY INTO`, quelle taille de fichiers de données Snowflake recommande-t-il ?

- A. Moins de 1 Mo compressé, pour multiplier les fichiers
- B. Environ 16 Mo non compressés
- C. Un fichier unique, le plus volumineux possible
- D. Environ 100 à 250 Mo compressés

### Question 99

Un auditeur demande quels utilisateurs ont lu la colonne `iban` de la table `clients` au cours du dernier mois. Quelle vue d'ACCOUNT_USAGE apporte cette information ?

- A. `ACCESS_HISTORY`
- B. `LOGIN_HISTORY`
- C. `WAREHOUSE_METERING_HISTORY`
- D. `TABLE_STORAGE_METRICS`

### Question 100

Quelle est la différence entre un replication group et un failover group ?

- A. Un replication group réplique entre régions, un failover group uniquement au sein d'une même région.
- B. Les deux répliquent un ensemble d'objets vers un compte cible, mais seul le failover group permet de promouvoir les objets secondaires en objets primaires, accessibles en écriture.
- C. Un replication group ne peut contenir que des warehouses, un failover group que des bases de données.
- D. Un failover group est une copie par clonage zéro-copie, un replication group une copie physique.

---

## Grille de réponses

| N° | Réponse | N° | Réponse | N° | Réponse | N° | Réponse | N° | Réponse |
|---|---|---|---|---|---|---|---|---|---|
| 1 | C | 21 | D | 41 | C | 61 | D | 81 | C |
| 2 | B | 22 | B | 42 | B, D | 62 | B | 82 | A |
| 3 | D | 23 | A, C | 43 | B | 63 | A | 83 | D |
| 4 | A | 24 | D | 44 | C | 64 | B | 84 | B, C |
| 5 | B | 25 | A | 45 | C | 65 | C | 85 | A |
| 6 | A, C | 26 | C | 46 | A | 66 | A | 86 | C, E |
| 7 | B, D | 27 | B | 47 | D | 67 | A, D | 87 | C |
| 8 | D | 28 | D | 48 | A | 68 | C | 88 | A |
| 9 | C | 29 | B | 49 | C | 69 | B | 89 | D |
| 10 | A | 30 | B, E | 50 | B | 70 | D | 90 | C |
| 11 | A, D | 31 | C, D | 51 | D | 71 | A | 91 | B |
| 12 | B | 32 | A | 52 | C | 72 | C | 92 | D |
| 13 | D | 33 | A | 53 | A | 73 | D | 93 | A, D |
| 14 | B, E | 34 | A, C, E | 54 | A, C, D | 74 | A, B | 94 | A |
| 15 | C | 35 | D | 55 | B | 75 | B | 95 | B |
| 16 | D | 36 | C | 56 | D | 76 | C | 96 | C |
| 17 | B | 37 | B, D | 57 | A, D | 77 | B | 97 | B |
| 18 | C, D | 38 | C | 58 | C | 78 | A | 98 | D |
| 19 | A | 39 | D | 59 | A | 79 | D | 99 | A |
| 20 | C | 40 | B, E | 60 | C, E | 80 | B | 100 | B |

---

## Corrigé détaillé

Les domaines sont numérotés ainsi : 1 = Fonctionnalités et architecture de la plateforme ; 2 = Gestion du compte et gouvernance des données ; 3 = Chargement, déchargement et connectivité ; 4 = Performance, requêtes et transformation ; 5 = Collaboration autour des données.

**Question 1 — Réponse C — Domaine 1.** La couche des services cloud coordonne l'ensemble : authentification, contrôle d'accès, métadonnées, analyse et optimisation des requêtes. La couche de calcul (B) exécute les requêtes mais ne les optimise pas et ne gère pas les métadonnées.

**Question 2 — Réponse B — Domaine 3.** Le stage de table se note `@%nom_de_table`. Le préfixe `@~` (A) désigne le stage de l'utilisateur, et `@nom` (C) un stage nommé, qui est un objet créé explicitement.

**Question 3 — Réponse D — Domaine 2.** USERADMIN est dédié à la gestion des utilisateurs et des rôles : les privilèges CREATE USER et CREATE ROLE lui sont accordés directement. SECURITYADMIN (B) peut aussi créer des utilisateurs, mais seulement parce qu'il hérite de USERADMIN ; son rôle propre est la gestion globale des privilèges (`MANAGE GRANTS`).

**Question 4 — Réponse A — Domaine 4.** Le cache de résultats est conservé par la couche des services cloud : une requête identique sur des données inchangées est servie sans warehouse. Le cache local du warehouse (B) est au contraire perdu lors de la suspension et ne pourrait de toute façon pas servir sans warehouse actif.

**Question 5 — Réponse B — Domaine 1.** Un warehouse Medium consomme 4 crédits par heure (X-Small 1, Small 2, Medium 4, Large 8), soit 2 crédits pour 30 minutes. La réponse C confond la consommation horaire et la consommation réelle, facturée à la seconde.

**Question 6 — Réponses A et C — Domaine 5.** Le partage repose sur les métadonnées de la couche de services : rien n'est copié, et le consommateur ne paie que le calcul de ses requêtes. Le stockage (B) reste à la charge du fournisseur, et les objets partagés sont en lecture seule (D).

**Question 7 — Réponses B et D — Domaine 1.** Une table temporaire disparaît à la fin de la session et n'a pas de Fail-safe. Elle n'est visible que dans la session qui l'a créée (A), et ses données sont facturées en stockage tant qu'elle existe (E).

**Question 8 — Réponse D — Domaine 4.** Des requêtes rapides mais en file d'attente signalent un problème de concurrence, que l'on traite en ajoutant des clusters (mise à l'échelle horizontale). Agrandir le warehouse (A) accélère les requêtes lourdes, mais ce n'est pas le remède prévu pour une file d'attente due au nombre de requêtes simultanées.

**Question 9 — Réponse C — Domaine 2.** La propriété d'un objet revient au rôle primaire actif au moment de la création, jamais à l'utilisateur. Penser que l'utilisatrice est propriétaire (A) est la confusion classique entre rôle et utilisateur.

**Question 10 — Réponse A — Domaine 3.** En chargement en masse, `ON_ERROR` vaut `ABORT_STATEMENT` par défaut : la première erreur interrompt le chargement. `SKIP_FILE` (C) est la valeur par défaut de Snowpipe, pas de `COPY INTO` exécuté manuellement.

**Question 11 — Réponses A et D — Domaine 1.** Le Fail-safe dure sept jours, n'est pas configurable et n'est accessible que par le support de Snowflake. `UNDROP` et le paramètre de rétention (B, C) relèvent du Time Travel, et les tables transient n'ont pas de Fail-safe (E).

**Question 12 — Réponse B — Domaine 4.** La notation `colonne:cle.sous_cle` parcourt une valeur semi-structurée et `::STRING` convertit le résultat. La réponse C interprète à tort la notation comme un chemin base, schéma, table.

**Question 13 — Réponse D — Domaine 1.** Snowflake combine un stockage central accessible à tous les clusters (shared-disk) et des clusters de calcul indépendants à traitement massivement parallèle (shared-nothing). La réponse A oublie que le stockage est centralisé et séparé du calcul.

**Question 14 — Réponses B et E — Domaine 2.** Les resource monitors sont créés par ACCOUNTADMIN et suivent les crédits des warehouses. Ils ne couvrent pas les fonctionnalités serverless (A), et un warehouse ne peut être rattaché qu'à un seul monitor (D).

**Question 15 — Réponse C — Domaine 3.** `PUT` envoie un fichier local vers un stage interne. `COPY INTO` (A) charge dans une table des fichiers déjà présents dans un stage ; il ne lit pas le poste local.

**Question 16 — Réponse D — Domaine 1.** À partir de l'édition Enterprise, la rétention d'une table permanente se règle de 0 à 90 jours. La valeur d'un jour (A) est la valeur par défaut, et le maximum de l'édition Standard.

**Question 17 — Réponse B — Domaine 4.** Toute task est créée suspendue et doit être activée avec `ALTER TASK ... RESUME`. Un stream (C) n'est pas obligatoire : il sert seulement à conditionner l'exécution.

**Question 18 — Réponses C et D — Domaine 5.** Le compte lecteur est créé, géré et payé par le fournisseur, pour un consommateur qui n'a pas de compte Snowflake. Il ne peut consommer que les données du fournisseur qui l'a créé (E).

**Question 19 — Réponse A — Domaine 1.** Le clonage zéro-copie ne duplique que des métadonnées ; le stockage n'augmente que lorsque le clone ou la source sont modifiés. La réponse B décrit une copie physique de type `CREATE TABLE ... AS SELECT`.

**Question 20 — Réponse C — Domaine 2.** SECURITYADMIN détient `MANAGE GRANTS` et gère les privilèges à l'échelle du compte. USERADMIN (A) crée utilisateurs et rôles, mais ne possède pas ce privilège global.

**Question 21 — Réponse D — Domaine 4.** Le cache local du warehouse (données lues sur disque local) est vidé à la suspension, d'où une première requête plus lente. Le cache de résultats (A) ne dépend pas du warehouse et survit à sa suspension.

**Question 22 — Réponse B — Domaine 1.** Les warehouses multi-cluster sont disponibles à partir de l'édition Enterprise. Business Critical (C) les inclut aussi, mais ce n'est pas l'édition minimale.

**Question 23 — Réponses A et C — Domaine 3.** Snowpipe est déclenché soit par les notifications d'événements du stockage cloud, soit par un appel à son API REST. Un pipe n'a pas de planification (B) : c'est le propre des tasks.

**Question 24 — Réponse D — Domaine 1.** Le warehouse est un objet de niveau compte, comme les utilisateurs et les rôles. Stages, file formats et pipes (A, B, C) sont des objets de schéma.

**Question 25 — Réponse A — Domaine 2.** Une masking policy masque dynamiquement la valeur d'une colonne selon le rôle, au moment de la requête. Une row access policy (B) filtre des lignes entières et ne masque pas une colonne.

**Question 26 — Réponse C — Domaine 4.** `LATERAL FLATTEN` éclate un tableau en autant de lignes qu'il contient d'éléments, accessibles par la colonne `value`. `PARSE_JSON` (A) convertit une chaîne en VARIANT sans produire de lignes supplémentaires.

**Question 27 — Réponse B — Domaine 1.** La facturation se fait à la seconde, avec un minimum de 60 secondes à chaque démarrage du warehouse. La réponse A oublie ce minimum : 20 secondes d'activité sont facturées comme 60.

**Question 28 — Réponse D — Domaine 3.** Les métadonnées de chargement de la table, conservées 64 jours, empêchent de recharger un fichier déjà chargé et inchangé. Pour forcer le rechargement (et obtenir le comportement de la réponse A), il faudrait ajouter `FORCE = TRUE`.

**Question 29 — Réponse B — Domaine 5.** Les objets d'une base créée à partir d'un share sont en lecture seule : il faut copier les données dans une table locale pour les modifier. Le clonage d'objets partagés (C) n'est pas possible.

**Question 30 — Réponses B et E — Domaine 1.** Une vue sécurisée cache sa définition aux rôles non propriétaires et renonce à certaines optimisations qui pourraient exposer des données, au prix des performances. Elle ne stocke rien (A) : c'est la vue matérialisée qui stocke un résultat.

**Question 31 — Réponses C et D — Domaine 2.** ACCOUNT_USAGE inclut les objets supprimés et conserve un an d'historique, avec une latence de 45 minutes à 3 heures. L'INFORMATION_SCHEMA n'a pas de latence (A) mais son historique est limité, de 7 jours à 6 mois selon les fonctions.

**Question 32 — Réponse A — Domaine 4.** Le débordement sur le stockage distant signifie que la mémoire puis le disque local du warehouse sont insuffisants : un warehouse plus grand apporte ces ressources. Ajouter des clusters (B) augmente la capacité en concurrence, pas la mémoire disponible pour une requête donnée.

**Question 33 — Réponse A — Domaine 1.** En édition Standard, la rétention vaut 0 ou 1 jour. Les 90 jours (D) nécessitent l'édition Enterprise ou supérieure.

**Question 34 — Réponses A, C et E — Domaine 3.** Le déchargement prend en charge les fichiers délimités (CSV), JSON et Parquet. AVRO et ORC (B, D) sont acceptés au chargement, mais pas au déchargement.

**Question 35 — Réponse D — Domaine 4.** Dans un stream standard, une mise à jour est représentée par une paire DELETE et INSERT, marquée `METADATA$ISUPDATE = TRUE`. La valeur 'UPDATE' (A) n'existe pas pour `METADATA$ACTION`, qui ne prend que les valeurs INSERT et DELETE.

**Question 36 — Réponse C — Domaine 1.** `UNDROP` échoue si un objet du même nom existe déjà : il faut d'abord renommer la nouvelle table. Le Fail-safe (D) n'intervient qu'après la fin de la période de Time Travel.

**Question 37 — Réponses B et D — Domaine 2.** La liste bloquée l'emporte sur la liste autorisée, et une seule politique peut être associée au compte à la fois. La création revient à SECURITYADMIN, à un rôle supérieur ou à un rôle disposant de CREATE NETWORK POLICY, et non à ORGADMIN (C).

**Question 38 — Réponse C — Domaine 1.** Une table externe expose en lecture seule des fichiers restés dans un stockage cloud externe. Ses données ne sont pas stockées dans Snowflake (A) et ne bénéficient donc ni du Time Travel ni du Fail-safe.

**Question 39 — Réponse D — Domaine 3.** `VALIDATION_MODE` valide les fichiers sans rien charger ; `RETURN_ERRORS` renvoie les erreurs de tous les fichiers. Le comportement de la réponse A (charger les lignes valides) correspond à `ON_ERROR = CONTINUE`.

**Question 40 — Réponses B et E — Domaine 4.** Le résultat est réutilisé si le texte de la requête est identique et si les données sous-jacentes n'ont pas changé (entre autres conditions). Ni le warehouse (A) ni l'utilisateur (C) n'entrent en jeu : un autre utilisateur dont le rôle possède les privilèges requis peut profiter du résultat.

**Question 41 — Réponse C — Domaine 5.** Snowflake Marketplace permet de découvrir et d'obtenir des jeux de données de fournisseurs tiers, accessibles sans pipeline. Un compte lecteur (D) est créé par un fournisseur pour un consommateur sans compte Snowflake ; il ne sert pas à trouver des données.

**Question 42 — Réponses B et D — Domaine 1.** Les micro-partitions contiennent 50 à 500 Mo de données non compressées, stockées en colonnes, avec des métadonnées qui permettent l'élagage (pruning). Elles sont créées automatiquement (A) et sont immuables : un `UPDATE` écrit de nouvelles micro-partitions (C).

**Question 43 — Réponse B — Domaine 2.** L'authentification par paire de clés est la méthode adaptée aux comptes de service et aux traitements automatisés. Le SSO par navigateur et la validation sur téléphone (A, C) exigent une action humaine.

**Question 44 — Réponse C — Domaine 4.** Le service d'optimisation de recherche accélère les recherches ponctuelles très sélectives (égalité, IN) sur de grandes tables. Un warehouse multi-cluster (A) traite la concurrence, pas le temps d'exécution d'une recherche isolée.

**Question 45 — Réponse C — Domaine 1.** Une table transient persiste entre les sessions mais n'a pas de Fail-safe et au plus un jour de Time Travel, ce qui réduit le stockage de protection. Une table temporaire (B) disparaîtrait à la fin de la session et ne serait pas visible des autres sessions.

**Question 46 — Réponse A — Domaine 3.** `SINGLE = TRUE` force la production d'un fichier unique ; par défaut, `SINGLE` vaut `FALSE`. `OVERWRITE` (D) remplace des fichiers de même nom mais ne change pas leur nombre.

**Question 47 — Réponse D — Domaine 1.** Snowpark fournit une API DataFrame en Python, Java et Scala, dont les opérations sont exécutées par le moteur de Snowflake. Ce n'est pas un cluster Spark à administrer (B) : aucun moteur externe n'est nécessaire.

**Question 48 — Réponse A — Domaine 2.** Une row access policy détermine quelles lignes sont visibles selon le contexte de la requête, par exemple le rôle. Une masking policy (B) agit sur la valeur d'une colonne, pas sur la visibilité des lignes.

**Question 49 — Réponse C — Domaine 4.** La clause `WHEN SYSTEM$STREAM_HAS_DATA('...')` évite d'exécuter la task lorsque le stream est vide. `AFTER` (A) sert à désigner une task parente dans un graphe de tasks, pas un stream.

**Question 50 — Réponse B — Domaine 1.** Après un jour de Time Travel, les données entrent pour sept jours dans le Fail-safe, où seul le support de Snowflake peut tenter une récupération. `UNDROP` (A, D) ne fonctionne que pendant la période de Time Travel, et augmenter la rétention après coup n'y change rien.

**Question 51 — Réponse D — Domaine 3.** Pour Snowpipe, `ON_ERROR` vaut `SKIP_FILE` par défaut : le fichier en erreur est ignoré et les autres sont chargés. `ABORT_STATEMENT` (A) est la valeur par défaut du chargement en masse, pas de Snowpipe.

**Question 52 — Réponse C — Domaine 5.** La bascule (failover et failback) entre comptes exige l'édition Business Critical ou supérieure. La réplication de bases de données et de shares est disponible dans toutes les éditions, ce qui rend la réponse A tentante, mais répliquer n'est pas basculer.

**Question 53 — Réponse A — Domaine 1.** Les services cloud ne sont facturés que pour la part dépassant 10 % de la consommation quotidienne des warehouses. Ils ne sont donc ni toujours facturés (B) ni toujours gratuits (C).

**Question 54 — Réponses A, C et D — Domaine 2.** Pour lire une table, il faut USAGE sur la base, USAGE sur le schéma et SELECT sur la table. OWNERSHIP (B) donnerait tous les droits sur la table, mais ce n'est pas le minimum requis.

**Question 55 — Réponse B — Domaine 4.** Presque toutes les micro-partitions sont lues malgré un filtre sélectif : l'élagage est inefficace, et une clustering key sur la colonne filtrée regroupe les données pour le rétablir. Ajouter des clusters (A) n'a aucun effet sur le nombre de micro-partitions à lire.

**Question 56 — Réponse D — Domaine 1.** Combiné au Time Travel, le clonage crée une copie de la table dans un état passé ; `OFFSET => -3600` désigne l'instant situé 3 600 secondes avant maintenant. Il ne s'agit pas de réplication (C) : un clone reste dans le même compte.

**Question 57 — Réponses A et D — Domaine 3.** `PUT` compresse par défaut en gzip (`AUTO_COMPRESS = TRUE`) et chiffre les fichiers envoyés vers le stage interne. Il ne fonctionne pas vers un stage externe (B) : on y dépose les fichiers avec les outils du fournisseur cloud.

**Question 58 — Réponse C — Domaine 2.** Les vues d'ACCOUNT_USAGE sont alimentées avec retard, jusqu'à 45 minutes pour `QUERY_HISTORY`. Pour une requête récente, on utilise la fonction `QUERY_HISTORY` de l'INFORMATION_SCHEMA ou l'historique de Snowsight ; une requête servie par le cache (D) est bien enregistrée.

**Question 59 — Réponse A — Domaine 1.** Les fonctions d'IA de Cortex donnent accès à des modèles de langage depuis SQL (résumé, traduction, analyse de sentiment, complétion). Snowpipe Streaming (C) est un service d'ingestion, sans rapport avec l'IA.

**Question 60 — Réponses C et E — Domaine 4.** Une vue matérialisée ne porte que sur une seule table et est tenue à jour automatiquement par un service d'arrière-plan facturé. Ses résultats sont toujours à jour (D) : si la maintenance est en retard, Snowflake complète avec la table de base.

**Question 61 — Réponse D — Domaine 5.** Un share direct ne fonctionne qu'entre comptes de la même région ; pour une autre région ou un autre cloud, les données doivent y être répliquées (listing avec auto-fulfillment, ou réplication vers un compte du fournisseur dans la région cible). Le clonage (C) ne sort pas du compte d'origine.

**Question 62 — Réponse B — Domaine 1.** Le redimensionnement ne touche pas les requêtes en cours ; les ressources ajoutées servent aux requêtes en attente et aux suivantes. La réponse C est le piège : une requête déjà lancée ne s'accélère pas.

**Question 63 — Réponse A — Domaine 3.** `PURGE = TRUE` supprime du stage les fichiers chargés avec succès ; par défaut, `PURGE` vaut `FALSE`. `FORCE = TRUE` (B) recharge tous les fichiers, y compris ceux déjà chargés.

**Question 64 — Réponse B — Domaine 2.** Snowflake recommande de rattacher les rôles personnalisés à SYSADMIN, pour que ce rôle hérite de leurs privilèges et puisse gérer tous les objets. USERADMIN (C) sert à créer les rôles, mais n'a pas vocation à hériter des privilèges sur les objets de données.

**Question 65 — Réponse C — Domaine 4.** La politique Economy privilégie l'économie de crédits : un cluster n'est ajouté que si la charge estimée l'occupera au moins six minutes. Le démarrage dès la mise en file d'attente (A) décrit la politique Standard.

**Question 66 — Réponse A — Domaine 1.** Sur une table standard, PRIMARY KEY, UNIQUE et FOREIGN KEY sont déclaratives et non appliquées ; seule NOT NULL est appliquée. Ces contraintes ne sont réellement appliquées que sur les tables hybrides, ce qui rend la réponse B fausse ici.

**Question 67 — Réponses A et D — Domaine 1.** Snowflake réorganise les données en colonnes compressées et les chiffre au repos dans toutes les éditions. Les fichiers ne sont pas accessibles directement (B) : on n'atteint les données que par des requêtes SQL.

**Question 68 — Réponse C — Domaine 3.** `STRIP_OUTER_ARRAY = TRUE` retire les crochets extérieurs afin que chaque élément du tableau devienne une ligne. `SKIP_HEADER` (A) est une option des fichiers CSV.

**Question 69 — Réponse B — Domaine 2.** L'action SUSPEND attend la fin des requêtes en cours avant de suspendre le warehouse. SUSPEND_IMMEDIATE (C) annule les requêtes en cours d'exécution.

**Question 70 — Réponse D — Domaine 4.** La position d'un stream n'avance que lorsque son contenu est consommé par une instruction DML dans une transaction validée. Un `SELECT` seul ne consomme rien ; la commande de la réponse C n'existe pas.

**Question 71 — Réponse A — Domaine 5.** Le consommateur crée une base de données à partir du share avec `CREATE DATABASE ... FROM SHARE`. Aucune copie ni clonage (B, C) n'a lieu : la base créée pointe vers les objets du fournisseur.

**Question 72 — Réponse C — Domaine 1.** La connectivité privée au service Snowflake est une fonctionnalité de l'édition Business Critical. L'édition Enterprise (B) apporte notamment le Time Travel étendu et les warehouses multi-cluster, mais pas la connectivité privée.

**Question 73 — Réponse D — Domaine 2.** Avec le masquage basé sur les tags, la masking policy est associée au tag et protège toute colonne qui le porte. Une row access policy (A) filtre des lignes et ne masque pas de colonnes.

**Question 74 — Réponses A et B — Domaine 4.** Une procédure s'appelle avec `CALL` et sert à exécuter des opérations ; une UDF calcule une valeur utilisable dans une requête. Les procédures peuvent être écrites dans plusieurs langages, dont SQL (Snowflake Scripting), JavaScript et Python (E).

**Question 75 — Réponse B — Domaine 3.** Une storage integration délègue l'authentification à une identité gérée par le fournisseur cloud, sans clés dans la définition du stage. Un file format (A) ne décrit que la structure des fichiers.

**Question 76 — Réponse C — Domaine 1.** Une vue standard n'est qu'une requête nommée, exécutée à chaque interrogation. La réponse A décrit approximativement une vue matérialisée, qui stocke un résultat (et le maintient en continu, non toutes les heures).

**Question 77 — Réponse B — Domaine 1.** Streamlit in Snowflake permet de créer en Python des applications interactives hébergées dans Snowflake. SnowSQL (C) est un client en ligne de commande, pas un outil de création d'applications.

**Question 78 — Réponse A — Domaine 2.** La base SNOWFLAKE est une base partagée par Snowflake : on y donne accès avec `GRANT IMPORTED PRIVILEGES`. On ne peut pas en transférer la propriété (B).

**Question 79 — Réponse D — Domaine 4.** Une table dynamique matérialise le résultat d'une requête et le rafraîchit automatiquement pour respecter le `TARGET_LAG` demandé. Une vue sécurisée (A) est recalculée à chaque interrogation et ne matérialise rien.

**Question 80 — Réponse B — Domaine 3.** Snowpipe conserve l'historique de chargement 14 jours, dans les métadonnées du pipe. Les 64 jours (C) concernent le chargement en masse, dont l'historique est stocké dans les métadonnées de la table.

**Question 81 — Réponse C — Domaine 5.** Une base secondaire est en lecture seule ; elle ne devient accessible en écriture qu'après sa promotion en base primaire. Il n'existe pas de fusion bidirectionnelle des modifications (A).

**Question 82 — Réponse A — Domaine 1.** Snowpark Container Services exécute des images de conteneurs dans Snowflake, y compris sur des pools de calcul dotés de GPU. Les tasks serverless (B) exécutent du SQL ou des procédures planifiés, pas des conteneurs.

**Question 83 — Réponse D — Domaine 2.** SCIM automatise le provisionnement des utilisateurs et des groupes depuis le fournisseur d'identité. L'authentification multifacteur et la paire de clés (A, C) traitent de l'authentification, pas du cycle de vie des comptes.

**Question 84 — Réponses B et C — Domaine 4.** Une clustering key se justifie sur de très grandes tables dont les requêtes filtrent ou joignent sur les colonnes de la clé. Sur une table très souvent modifiée et peu lue (D), le coût du reclustering dépasse le bénéfice.

**Question 85 — Réponse A — Domaine 3.** `MATCH_BY_COLUMN_NAME` associe les colonnes du fichier à celles de la table par leur nom, avec ou sans respect de la casse. `FORCE` (B) ne concerne que le rechargement de fichiers déjà chargés.

**Question 86 — Réponses C et E — Domaine 1.** Snowflake est un service entièrement géré : rien à installer, et la maintenance comme les mises à jour sont prises en charge par Snowflake. Il s'exécute uniquement sur l'infrastructure de fournisseurs cloud publics, et non dans le centre de données du client (A).

**Question 87 — Réponse C — Domaine 4.** Un résultat est conservé 24 heures ; chaque réutilisation relance cette période, dans la limite de 31 jours après la première exécution. La réponse B oublie cette prolongation.

**Question 88 — Réponse A — Domaine 2.** Dans un schéma à accès géré, les décisions d'octroi sont centralisées : seul le propriétaire du schéma ou un rôle doté de `MANAGE GRANTS` peut accorder des privilèges. Les propriétaires d'objets (B) perdent cette faculté, contrairement au schéma standard.

**Question 89 — Réponse D — Domaine 1.** Une table Iceberg utilise le format ouvert Apache Iceberg ; ses fichiers sont le plus souvent dans un stockage cloud du client, désigné par un external volume (la documentation décrit aussi un stockage géré par Snowflake). La réponse A décrit une table hybride, et la réponse C une table dynamique.

**Question 90 — Réponse C — Domaine 3.** `GET` télécharge des fichiers d'un stage interne vers le poste local. `COPY INTO <location>` (B) décharge une table vers un stage, sans rien écrire sur le poste local.

**Question 91 — Réponse B — Domaine 5.** La réplication copie une base vers un autre compte, y compris dans une autre région ou un autre cloud, et la resynchronise. Le clonage (A) est instantané mais reste à l'intérieur du même compte.

**Question 92 — Réponse D — Domaine 4.** En mode Maximized, les nombres minimal et maximal de clusters sont identiques et supérieurs à 1 : tous les clusters démarrent avec le warehouse. Des valeurs différentes (B) correspondent au mode auto-scale.

**Question 93 — Réponses A et D — Domaine 2.** Snowflake combine le contrôle discrétionnaire (le propriétaire d'un objet en accorde l'accès) et le contrôle basé sur les rôles (privilèges accordés aux rôles, rôles accordés aux utilisateurs). L'accès est refusé par défaut tant qu'il n'a pas été accordé (E).

**Question 94 — Réponse A — Domaine 1.** `BEFORE (STATEMENT => ...)` renvoie l'état de la table juste avant l'instruction désignée. `AT (STATEMENT => ...)` (B) inclut les changements effectués par cette instruction, donc l'état après le `DELETE`.

**Question 95 — Réponse B — Domaine 3.** Le Snowflake Connector for Kafka lit les topics et charge les messages dans des tables Snowflake. Le pilote ODBC (A) permet à une application d'exécuter du SQL, mais ne consomme pas de topics.

**Question 96 — Réponse C — Domaine 2.** La politique la plus spécifique l'emporte : celle de l'utilisateur prime sur celle du compte. Les deux politiques ne se cumulent pas (B).

**Question 97 — Réponse B — Domaine 4.** Sur une table standard, un stream limité aux insertions se crée avec `APPEND_ONLY = TRUE`. `INSERT_ONLY` (A) est réservé aux tables externes et aux tables Iceberg gérées en externe.

**Question 98 — Réponse D — Domaine 3.** Snowflake recommande des fichiers d'environ 100 à 250 Mo compressés, pour paralléliser le chargement sans surcoût par fichier. Un fichier unique très volumineux (C) empêche la parallélisation.

**Question 99 — Réponse A — Domaine 2.** `ACCESS_HISTORY` (édition Enterprise ou supérieure) indique quels objets et quelles colonnes ont été lus par chaque requête et chaque utilisateur. `LOGIN_HISTORY` (B) ne recense que les connexions.

**Question 100 — Réponse B — Domaine 5.** Un failover group est un replication group doté en plus de la capacité de bascule : ses objets secondaires peuvent être promus en primaires, accessibles en écriture. Les deux types de groupes fonctionnent entre régions et entre clouds (A).

---

## Tableau de dépouillement

Entourez les numéros des questions réussies, comptez-les par domaine, puis calculez le pourcentage. Un domaine sous 70 % est à revoir en priorité.

| Domaine | Questions | Total | Votre score | Chapitres à revoir |
|---|---|---|---|---|
| 1. Fonctionnalités et architecture de la plateforme | 1, 5, 7, 11, 13, 16, 19, 22, 24, 27, 30, 33, 36, 38, 42, 45, 47, 50, 53, 56, 59, 62, 66, 67, 72, 76, 77, 82, 86, 89, 94 | 31 | ... / 31 | `12-architecture.md`, `13-stockage-protection.md`, `14-ia-applications.md` |
| 2. Gestion du compte et gouvernance des données | 3, 9, 14, 20, 25, 31, 37, 43, 48, 54, 58, 64, 69, 73, 78, 83, 88, 93, 96, 99 | 20 | ... / 20 | `10-securite.md`, `15-gouvernance.md`, `09-monitoring.md` |
| 3. Chargement, déchargement et connectivité | 2, 10, 15, 23, 28, 34, 39, 46, 51, 57, 63, 68, 75, 80, 85, 90, 95, 98 | 18 | ... / 18 | `11-chargement-stage-copy.md`, `16-snowpipe-export-connectivite.md` |
| 4. Performance, requêtes et transformation | 4, 8, 12, 17, 21, 26, 32, 35, 40, 44, 49, 55, 60, 65, 70, 74, 79, 84, 87, 92, 97 | 21 | ... / 21 | `17-performance.md`, `18-transformation.md` |
| 5. Collaboration autour des données | 6, 18, 29, 41, 52, 61, 71, 81, 91, 100 | 10 | ... / 10 | `19-collaboration.md` |
| **Total** | | **100** | **... / 100** | Objectif : 75 au minimum |

Repères de lecture du score global :

- 85 et plus : niveau confortable ; consolidez seulement les domaines les plus faibles.
- De 75 à 84 : niveau suffisant mais fragile ; reprenez le corrigé des questions ratées et le chapitre du domaine le plus faible.
- De 60 à 74 : révisez les deux domaines les plus faibles en entier avant de repasser un examen blanc.
- Moins de 60 : reprenez le cours chapitre par chapitre, en commençant par le domaine 1, qui pèse le plus lourd.


