# Les étapes, journée par journée

![Schéma de la gouvernance](docs/gouvernance.png)

Chaque journée suit le même plan : le guide à suivre d'abord, les étapes, les pièges à éviter, le résultat à obtenir avant de passer à la suite.

---

## Jour 1 — Inventorier, charger et cataloguer

**Dossiers de travail** : `docs/`, `snowflake/gouvernance/`, `ingestion/`
**Guide à suivre d'abord** : [Authentification et gouvernance des données](https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/15-gouvernance.md), section 5.3 (tags et classification)

### Étapes

1. **Lire `CONTRAT_GOUVERNANCE.md` en entier**, puis ouvrir les deux fichiers CSV.
2. **Faire l'inventaire des données personnelles**, à partir du modèle `docs/INVENTAIRE_MODELE.md` : pour chaque colonne des deux fichiers, dit-elle quelque chose d'une personne ? Permet-elle de l'identifier seule, ou seulement combinée à d'autres ?
3. **Décider si le fichier RH a sa place dans votre dépôt Git public**, et agir en conséquence.
4. **Charger les deux fichiers dans RAW**, en adaptant votre script du brief précédent : format de fichier CSV, stage, `PUT`, `COPY INTO`, colonnes techniques.
5. **Exécuter les fichiers SQL fournis** dans Snowsight, dans le bon ordre, et vérifier les volumes de `README_GOUVERNANCE.md`.
6. **Créer le schéma `GOUVERNANCE`, le rôle `GOUVERNANCE` et les trois tags** par un script versionné et rejouable.
7. **Exécuter le modèle `modele_catalogue_dim_zone.sql`**, puis écrire sur ce modèle la fiche de `DIM_DRIVER`, `MART_DRIVER_MONTHLY`, `FCT_TRIPS`, `RAW.DRIVERS` et `RAW.DRIVER_SHIFTS`.
8. **Créer la vue `GOUVERNANCE.V_CATALOGUE`** : une ligne par colonne, avec sa table, sa description, son type et ses tags.
9. **Ouvrir l'onglet Lineage de `MART_DRIVER_MONTHLY`** dans Snowsight et faire une capture.

### Coup de pouce

Les descriptions sont dans `INFORMATION_SCHEMA.COLUMNS` (colonne `comment`). Les tags d'une table et de ses colonnes s'obtiennent avec la fonction `TAG_REFERENCES_ALL_COLUMNS`, utilisée à la fin du modèle.

### Pièges à éviter

- Poser un tag sur une table qui ne vous appartient pas demande un privilège : relisez dans le guide qui peut créer un tag et qui peut le poser.
- `DIM_ZONE` est recréée à chaque exécution du pipeline mensuel : ses descriptions et ses tags disparaissent avec elle. Un catalogue saisi à la main dans l'interface ne survit pas ; un catalogue écrit dans des fichiers SQL rejouables, si.
- Une description qui répète le nom de la colonne (« email : l'email ») ne documente rien.
- L'onglet Lineage peut mettre plusieurs minutes à refléter une table qui vient d'être alimentée.

### Pour vous guider

Le numéro de licence TLC est public à New York. Est-ce pour autant une donnée que tout le monde doit voir dans votre entrepôt ?

### Résultat à obtenir

400 chauffeurs et 25 951 services dans RAW. `SELECT COUNT(*) FROM NYC_TAXI.GOUVERNANCE.V_CATALOGUE WHERE description IS NULL` renvoie 0.

---

## Jour 2 — Protéger : qui voit quoi

**Dossiers de travail** : `snowflake/gouvernance/`, `airflow/include/sql/rh/`, `docs/`
**Guide à suivre d'abord** : le même guide, sections 5.1 (masquage) et 5.2 (accès par ligne), puis l'atelier de la section 11 sur son exemple (`SALES_DB`)

### Étapes

1. **Faire l'atelier du guide** (étapes 1 à 4) sur son exemple.
2. **Créer les quatre rôles métier** et leur donner le droit de lire `MARTS`. Donnez-vous ces rôles pour pouvoir les tester avec `USE ROLE`.
3. **Écrire le cahier de tests avant les politiques**, à partir de `docs/MATRICE_TESTS_MODELE.md` : pour chaque rôle, ce qu'il doit voir, en nombre de lignes et en valeurs.
4. **Décider, colonne par colonne**, entre masquer et supprimer : l'analyste a-t-elle besoin d'une colonne e-mail, même masquée ?
5. **Écrire les politiques de masquage** et les attacher. Une politique par colonne fonctionne ; une politique attachée à un tag protège d'un coup toutes les colonnes qui le portent.
6. **Remplir `GOUVERNANCE.ACCES_DEPOT`**, écrire la politique d'accès par ligne et l'ajouter aux deux tables de `MARTS`.
7. **Dérouler le cahier de tests** avec chaque rôle, y compris `ACCOUNTADMIN` et `GOUVERNANCE`.
8. **Relancer les fichiers SQL fournis avec le rôle des outils** et vérifier que les tables sont toujours justes.

### Pièges à éviter

- Une politique de masquage renvoie le type qu'elle reçoit : une date masquée reste une date.
- Le rôle des outils remplit `DIM_DRIVER` à partir de ce qu'il voit. S'il voit des valeurs masquées, il écrit des valeurs masquées dans la table, définitivement.
- Une colonne calculée à partir d'une donnée personnelle est une donnée personnelle : regardez `driver_name` dans `MART_DRIVER_MONTHLY`.
- Tester avec `ACCOUNTADMIN` et conclure que « ça ne marche pas » : le résultat dépend de ce qu'écrit la politique, pas de la puissance du rôle.
- Une politique attachée ne se supprime pas : il faut d'abord la détacher.

### Pour vous guider

Si demain un dépôt ouvre à Staten Island, que faut-il modifier : la politique, ou une ligne dans une table ?

### Résultat à obtenir

Le cahier de tests est entièrement vert. Chaque responsable de dépôt ne voit que ses chauffeurs, l'analyste ne peut nommer personne, le service paie voit tout.

---

## Jour 3 — Conserver, contrôler, auditer, présenter

**Dossiers de travail** : `airflow/dags/`, `airflow/include/sql/rh/`, `docs/`, `README.md`
**Guides à suivre d'abord** : [Stockage et protection des données](https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/13-stockage-protection.md), sections 4 et 5 (Time Travel, Fail-safe) ; guide de gouvernance, section 6 (audit)

### Étapes

1. **Écrire la purge** (règle R1) et prévoir avant de l'exécuter combien de chauffeurs elle supprime.
2. **Prouver qu'une ligne supprimée est encore lisible** par Time Travel, puis appliquer la règle R2.
3. **Appliquer la règle R3** au stage.
4. **Écrire les règles de qualité** du contrat sur le modèle fourni : la règle fournie et au moins quatre autres.
5. **Écrire le DAG `gouvernance_rh`** : purge, vues, tables, fiches de catalogue, règles de qualité enregistrées dans `QUALITE_RESULTATS`. Un dépassement bloquant arrête le DAG.
6. **Vérifier après une exécution** que les politiques, les tags et les descriptions sont toujours en place.
7. **Auditer** : retrouver dans `SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY` qui a lu `DIM_DRIVER` depuis hier, et avec quel rôle.
8. **Remplir la fiche de registre** (`docs/REGISTRE_MODELE.md`), terminer le README, présenter.

### Pièges à éviter

- `ACCESS_HISTORY` a jusqu'à 3 heures de retard : vos lectures de ce matin n'y sont pas encore. Celles d'hier y sont.
- Une purge exécutée par un rôle qui ne voit pas toutes les lignes ne supprime que celles qu'il voit.
- Après la fin de Time Travel, Snowflake garde encore les données 7 jours en Fail-safe : vous ne pouvez ni les lire ni raccourcir ce délai sur une table permanente. Dites-le dans votre registre.
- Un DAG quotidien n'a pas besoin de rejouer le passé : pas de reprise d'historique ici.

### Pour vous guider

Le mois prochain, le service RH vous envoie un nouveau fichier complet, avec tous les chauffeurs depuis 2005. Que devient votre purge ?

### Bonus

- **Bonus 1** : lancer la classification automatique de Snowflake (`SYSTEM$CLASSIFY`) sur `RAW.DRIVERS` et comparer ses propositions à votre inventaire du jour 1.
- **Bonus 2** : remplacer la purge du DAG par une tâche planifiée Snowflake (`CREATE TASK`) et comparer les deux solutions.
- **Bonus 3** : interdire à l'analyste de lire les lignes une à une en n'autorisant que les agrégats (politique d'agrégation).

### Résultat à obtenir

Une exécution réussie du DAG, des lignes dans `QUALITE_RESULTATS`, une requête d'audit qui nomme les rôles ayant lu les données, et une démonstration de 15 minutes.
