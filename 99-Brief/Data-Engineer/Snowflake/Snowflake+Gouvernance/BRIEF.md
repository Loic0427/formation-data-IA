# Brief projet Data Engineer

## 🏷️ Titre

Gouverner l'entrepôt NYC Taxi : catalogue, accès et conservation dans Snowflake

## 📝 Description rapide

L'entrepôt de Hudson Cab Partners fonctionne, et la direction veut y ajouter le fichier RH des chauffeurs : noms, téléphones, numéros de licence. Avant de l'ouvrir aux responsables de dépôt, au service paie et à l'analyste, il faut savoir ce qu'il contient, qui a le droit de voir quoi, combien de temps on le garde et si l'on peut s'y fier. Vous chargez ce fichier, vous cataloguez les données, vous posez les politiques de masquage et d'accès par ligne, vous automatisez la purge et les règles de qualité avec Airflow, puis vous prouvez par l'historique des accès que les règles tiennent. Brief guidé en binôme sur 3 jours, à la suite du brief « Pipeline médaillon NYC Yellow Taxi ».

## 🎯 Compétences et niveaux

| Compétence | Niveau |
|---|---|
| C19. Intégrer les composants d'infrastructure | 2 (adapter) |
| C20. Gérer le catalogue des données | 1 (imiter) |
| C21. Implémenter les règles de gouvernance des données | 2 (adapter) |

## 📖 Contexte

### La situation

Votre pipeline tourne : chaque mois, les trajets de la TLC arrivent dans l'entrepôt et Priya, l'analyste, y trouve ses tables. La direction de Hudson Cab Partners veut maintenant répondre à une autre question : quels dépôts et quels chauffeurs font tourner la flotte ? Le service RH vous a donc transmis son fichier du personnel et le relevé des services de janvier à mars 2025.

Priya a aussitôt écrit le SQL qui construit une dimension chauffeur et une table d'activité mensuelle. Elle l'a fait comme pour les trajets, sans se demander ce que contenait le fichier. Or il contient des noms, des adresses e-mail, des téléphones, des dates de naissance et des numéros de licence. Trois services réclament déjà un accès : la paie, les responsables de dépôt, et Priya elle-même.

Personne ne sait dire aujourd'hui quelles colonnes de l'entrepôt décrivent une personne, qui les lit, ni ce que deviennent les données d'un chauffeur parti depuis dix ans. La direction a fixé les règles avec son conseil juridique. Elle vous demande de les mettre en œuvre avant d'ouvrir le moindre accès.

### La question à laquelle répondre

> Qui peut voir quelle donnée, pendant combien de temps, et peut-on s'y fier ?

Chaque choix des trois jours doit pouvoir se justifier par cette question.

### Ce que vous allez construire

![Schéma de la gouvernance](starter-kit/docs/gouvernance.png)

- **L'intégration du fichier RH** : stage, tables RAW, chargement rejouable, puis les transformations fournies.
- **Le catalogue** : une description pour chaque table et chaque colonne, trois tags, une vue qui rassemble le tout.
- **Les accès** : quatre rôles métier, des politiques de masquage, une politique d'accès par ligne pilotée par une table de correspondance.
- **La conservation et la qualité** : un DAG Airflow quotidien qui purge, reconstruit, recatalogue et contrôle.
- **La preuve** : un cahier de tests des accès et une requête d'audit.

### Les sources de données

| Source | Format | Volume | Où |
|---|---|---|---|
| Chauffeurs | 1 fichier CSV | 400 lignes, 10 colonnes | `data/drivers.csv` du kit |
| Services | 1 fichier CSV | 25 951 lignes, 8 colonnes | `data/driver_shifts.csv` du kit |
| Entrepôt existant | tables Snowflake | 10,4 millions de trajets | votre base `NYC_TAXI` |

Le fichier RH est fictif : on ne s'exerce pas à la gouvernance sur de vraies personnes. Aucun chauffeur n'existe et les adresses e-mail ne mènent nulle part. Il se traite pourtant comme un vrai fichier du personnel, et comme tout fichier venu d'un autre service, il contient des erreurs.

### Ce qui vous est fourni

Le kit de démarrage (commandes pour le récupérer dans les ressources) s'ajoute à votre projet du brief précédent :

- les deux fichiers CSV ;
- les fichiers SQL de Priya pour le domaine RH, que vous avez le droit de modifier ;
- `CONTRAT_GOUVERNANCE.md` : les noms imposés, la matrice des accès, les durées de conservation, les règles de qualité ;
- `ETAPES_GOUVERNANCE.md` : le détail de chaque journée ;
- un modèle complet de fiche de catalogue pour une table, une règle de qualité modèle ;
- trois modèles de documents : inventaire des données personnelles, cahier de tests, fiche de registre.

### Contraintes techniques

- Snowflake en édition Enterprise : le masquage, l'accès par ligne et l'historique des accès n'existent pas en édition Standard.
- Les règles sont portées par des rôles, jamais par des utilisateurs nommés.
- Le rôle qui écrit les règles ne lit pas les données ; ACCOUNTADMIN non plus.
- Tout est écrit dans des fichiers SQL versionnés et rejouables : rien n'est saisi à la main dans l'interface.
- Les règles survivent à une exécution du pipeline.
- Aucun secret et aucune donnée personnelle dans le dépôt GitHub public.

### Vocabulaire

| Terme | Sens |
|---|---|
| Donnée personnelle | information qui se rapporte à une personne identifiée ou identifiable |
| Catalogue | l'inventaire documenté des données : ce que contient chaque table, d'où elle vient, qui en répond |
| Tag | étiquette posée sur une table ou une colonne ; elle décrit, et peut déclencher une règle |
| Politique de masquage | règle qui transforme la valeur d'une colonne selon le rôle qui la lit |
| Politique d'accès par ligne | règle qui cache certaines lignes selon le rôle qui lit |
| Minimisation | ne conserver et ne montrer que les données nécessaires à un usage |
| Durée de conservation | délai au bout duquel une donnée doit être supprimée |
| Time Travel, Fail-safe | les deux délais pendant lesquels Snowflake garde une donnée supprimée |
| Lignage | le chemin d'une donnée, de sa source aux tables qui en dépendent |
| Registre des traitements | document qui décrit ce qu'une organisation fait des données personnelles |

## 🧭 Modalités pédagogiques

### Organisation

- **Durée et format** : 3 jours, en binôme (le même qu'au brief précédent), en autonomie accompagnée.
- **Méthode** : chaque journée commence par un guide pas à pas sur un exemple voisin (des clients). Reproduisez-le, puis transposez-le à nos données.
- **Document de référence** : `CONTRAT_GOUVERNANCE.md`. Il dit ce qui est exigé, pas comment le faire.
- **Répartition** : pendant qu'un membre écrit une politique, l'autre écrit le test qui la vérifie, puis vous échangez.
- **Règle d'or** : un test s'écrit avant la politique qu'il vérifie.

Le détail de chaque étape, avec les pièges à éviter, est dans `ETAPES_GOUVERNANCE.md` à la racine du kit.

### Jour 1 — Inventorier, charger et cataloguer

**Guide du jour** : [Authentification et gouvernance des données](https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/15-gouvernance.md), section 5.3

Aucune politique ce jour-là : on ne protège pas ce que l'on n'a pas inventorié.

1. Lire le contrat, ouvrir les fichiers, remplir l'inventaire des données personnelles. Quelles colonnes identifient quelqu'un à elles seules ? Lesquelles seulement une fois combinées ?
2. Décider si le fichier RH a sa place dans votre dépôt public.
3. Charger les deux fichiers dans RAW en adaptant votre script, puis exécuter le SQL fourni.
4. Créer le schéma et le rôle de gouvernance, les trois tags.
5. Écrire les fiches de catalogue sur le modèle fourni, puis la vue du catalogue.

**Résultat à obtenir** : 400 chauffeurs et 25 951 services dans RAW ; aucune colonne sans description dans la vue du catalogue.

### Jour 2 — Protéger : qui voit quoi

**Guide du jour** : le même guide, sections 5.1 et 5.2, puis son atelier

1. Créer les rôles métier et écrire le cahier de tests avant toute politique : que doit voir chaque rôle, en nombre de lignes et en valeurs ?
2. Décider, colonne par colonne, entre masquer et supprimer. L'analyste a-t-elle besoin d'une colonne e-mail, même masquée ?
3. Écrire et attacher les politiques de masquage, puis la politique d'accès par ligne.
4. Dérouler le cahier de tests avec chaque rôle, puis relancer le SQL fourni avec le rôle des outils : les tables sont-elles toujours justes ?

**Résultat à obtenir** : un cahier de tests entièrement vert.

### Jour 3 — Conserver, contrôler, auditer, présenter

**Guides du jour** : [Stockage et protection des données](https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/13-stockage-protection.md), sections 4 et 5 ; guide de gouvernance, section 6

1. Écrire la purge et prévoir combien de chauffeurs elle supprime. Une ligne supprimée a-t-elle vraiment disparu ?
2. Appliquer les règles de conservation à Time Travel et au stage.
3. Écrire les règles de qualité, puis le DAG qui purge, reconstruit, recatalogue et contrôle chaque jour.
4. Retrouver dans l'historique des accès qui a lu les données la veille.
5. Remplir la fiche de registre, terminer le README, présenter.

**Résultat à obtenir** : une exécution réussie du DAG, des résultats de qualité enregistrés, une requête d'audit qui nomme les rôles ayant lu les données.

**Bonus** : classification automatique de Snowflake comparée à votre inventaire ; purge par une tâche planifiée Snowflake ; politique d'agrégation pour l'analyste.

## 📊 Modalités d'évaluation

L'évaluation se fait par binôme, en deux volets. Chaque membre doit pouvoir expliquer l'ensemble.

### Démonstration technique (70 %)

15 minutes de démonstration en direct, puis 10 minutes de questions. Déroulé attendu :

1. Chercher une colonne dans la vue du catalogue et lire sa fiche : description, tags, table d'origine.
2. Exécuter la même requête sur la dimension chauffeur avec quatre rôles, dont ACCOUNTADMIN, et commenter les quatre résultats.
3. Ajouter un dépôt à un responsable en modifiant une ligne de la table de correspondance, sans toucher à la politique.
4. Montrer une exécution du DAG, puis prouver que politiques, tags et descriptions sont toujours en place.
5. Montrer le nombre de chauffeurs avant et après la purge, et ce qu'il reste dans Time Travel.
6. Exécuter la requête d'audit : qui a lu la dimension chauffeur, avec quel rôle.

### Revue de dépôt et de conception (30 %)

Lecture du dépôt GitHub : scripts rejouables, absence de secret et de donnée personnelle, cahier de tests, inventaire, fiche de registre, README. Les questions portent sur les choix : pourquoi masquer cette colonne plutôt que la supprimer, pourquoi une table de correspondance, que voit le rôle des outils et pourquoi, que se passe-t-il si le service RH renvoie un fichier complet le mois prochain, dans combien de jours une donnée purgée a-t-elle réellement disparu.

### Validation partielle

Chaque compétence est validée séparément. Un binôme dont le DAG ne tourne pas, mais dont les politiques sont justes et prouvées par le cahier de tests, peut valider C21 ; C19 ne serait pas validée. À l'inverse, des politiques qui disparaissent à la première exécution du pipeline, ou un fichier RH présent dans le dépôt public, ne valident pas C21, même si la démonstration réussit.

## 📦 Livrables attendus

**1. Le dépôt GitHub public** du brief précédent, complété :

| Dossier ou fichier | Contenu |
|---|---|
| `README.md` | section « Gouvernance » : ce qui est protégé et comment, ordre d'exécution des scripts, choix techniques, limites connues |
| `snowflake/gouvernance/` | scripts SQL rejouables : schéma, rôles et droits, tags, fiches de catalogue, vue du catalogue, politiques, table de correspondance, conservation, requête d'audit |
| `ingestion/` | script de chargement du fichier RH |
| `airflow/dags/` | le DAG `gouvernance_rh` |
| `airflow/include/sql/rh/` | les fichiers SQL du domaine RH, modifiés si besoin, et vos règles de qualité |
| `docs/` | inventaires, cahier de tests rempli, fiche de registre, captures |
| `.gitignore` | exclut le fichier RH |

**2. Les captures d'écran**, dans `docs/` : l'onglet Lineage de `MART_DRIVER_MONTHLY`, les tags d'une table dans Snowsight, la même requête lue par deux rôles, une exécution réussie du DAG, le contenu de `QUALITE_RESULTATS`, le résultat de la requête d'audit.

**3. Trois documents**, dans `docs/` : l'inventaire des données personnelles des deux fichiers, le cahier de tests des accès (attendu et obtenu), la fiche de registre du traitement.

## ✅ Critères de performance

### C19 — Intégrer les composants d'infrastructure

- Les deux fichiers RH sont chargés par un script rejouable (stage, COPY INTO, colonnes techniques) ; le stage est vide après le chargement.
- Le DAG `gouvernance_rh` enchaîne purge, vues, tables, catalogue et règles de qualité, et s'exécute avec succès avec le rôle des outils.
- Politiques, tags et descriptions sont toujours en place après une exécution du DAG.
- Le README permet de rejouer toute l'installation dans l'ordre ; aucun secret ni donnée personnelle dans le dépôt.

### C20 — Gérer le catalogue des données

- Chaque table du périmètre et chacune de ses colonnes a une description qui dit sa signification, sa source et son rythme de mise à jour.
- Toutes les colonnes personnelles de l'inventaire portent le tag `DONNEE_PERSONNELLE`, y compris les colonnes calculées ; chaque table porte sa sensibilité et sa durée de conservation.
- La vue `V_CATALOGUE` rassemble descriptions et tags, et un rôle métier peut l'interroger.
- Les règles de qualité sont documentées (énoncé, seuil, gravité) et le lignage d'une table est présenté.

### C21 — Implémenter les règles de gouvernance

- Chaque rôle voit exactement les lignes et les valeurs de la matrice, ACCOUNTADMIN et le rôle de gouvernance compris : le cahier de tests le prouve.
- L'accès par dépôt repose sur la table de correspondance : ajouter un dépôt ne demande aucune modification de politique.
- La purge supprime les chauffeurs partis depuis plus de 5 ans dans toutes les tables ; Time Travel est limité à 1 jour sur les tables concernées.
- Au moins cinq règles de qualité s'exécutent et s'enregistrent ; la règle bloquante arrête le DAG en cas de dépassement.
- Une requête sur l'historique des accès établit qui a lu les données personnelles, et la fiche de registre est renseignée avec ses preuves.

## 🔗 Ressources

Voir `RESSOURCES.md` : guides, documentation et vidéos, jour par jour.
