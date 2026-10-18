# Ressources — parcours d'apprentissage par jour

Méthode : pour chaque jour, 1) suivre le guide pas à pas indiqué en premier, sur son exemple, dans votre compte Snowflake, 2) transposer aux données de Hudson Cab Partners, 3) aller chercher le détail dans la documentation officielle, 4) regarder une vidéo si un geste reste flou. Les vidéos en anglais ont des sous-titres automatiques français sur YouTube (Paramètres → Sous-titres → Traduire automatiquement).

## Kit de démarrage

- Fichiers RH, fichiers SQL fournis, contrat de gouvernance, détail des étapes, modèles de documents : à parcourir sur https://github.com/gsoulat/formation-data-IA/tree/main/99-Brief/Data-Engineer/Snowflake/Snowflake+Gouvernance/starter-kit
- Pour l'ajouter à votre projet du brief précédent, sans télécharger tout le dépôt de cours (à lancer depuis le dossier parent de `nyc-taxi-pipeline`) :
  ```bash
  git clone --depth 1 --filter=blob:none --sparse https://github.com/gsoulat/formation-data-IA.git
  cd formation-data-IA
  git sparse-checkout set "99-Brief/Data-Engineer/Snowflake/Snowflake+Gouvernance/starter-kit"
  cd ..
  cp -R "formation-data-IA/99-Brief/Data-Engineer/Snowflake/Snowflake+Gouvernance/starter-kit/." nyc-taxi-pipeline/
  rm -rf formation-data-IA
  cd nyc-taxi-pipeline
  ```
  Aucun fichier de votre projet n'est écrasé : les fichiers du kit portent des noms qui lui sont propres.

## Avant le premier jour

Vérifier :
- Votre compte Snowflake du brief précédent est toujours actif (un compte d'essai dure 30 jours) et en édition Enterprise. Sinon, en recréer un : https://www.snowflake.com/en/snowflake-trial/
- Votre pipeline du brief précédent tourne : la base `NYC_TAXI` et la table `MARTS.FCT_TRIPS` existent.

Regarder :
- Vidéo (FR) — RGPD : Qu'est-ce qu'une donnée personnelle ?, Leto : https://www.youtube.com/watch?v=muSdwpDrYEY
- Vidéo (EN) — Snowflake Horizon Demo For Data Engineers, Snowflake Inc. : https://www.youtube.com/watch?v=MdZ1PaJWH2w

Lire :
- CNIL, définition d'une donnée personnelle : https://www.cnil.fr/fr/definition/donnee-personnelle

## Jour 1 — Inventorier, charger et cataloguer

Guide à suivre en premier (FR) :
- Authentification et gouvernance des données, section 5.3 (tags, héritage, classification) : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/15-gouvernance.md
- Pour le chargement, le guide du brief précédent reste la référence : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/11-chargement-stage-copy.md

Documentation officielle Snowflake :
- Tags d'objets (création, valeurs autorisées, héritage, privilèges) : https://docs.snowflake.com/en/user-guide/object-tagging/introduction
- COMMENT (décrire une table ou une colonne) : https://docs.snowflake.com/en/sql-reference/sql/comment
- Fonction TAG_REFERENCES_ALL_COLUMNS (lister les tags d'une table et de ses colonnes) : https://docs.snowflake.com/en/sql-reference/functions/tag_references_all_columns
- INFORMATION_SCHEMA (vues `TABLES` et `COLUMNS`, colonne `comment`) : https://docs.snowflake.com/en/sql-reference/info-schema
- Lignage des données dans Snowsight : https://docs.snowflake.com/en/user-guide/ui-snowsight-lineage
- Privilèges du contrôle d'accès (qui peut créer un tag, qui peut le poser) : https://docs.snowflake.com/en/user-guide/security-access-control-privileges

Vidéos :
- Vidéo (EN) — Creating a Data Classification Process Using Tags in Snowflake, ness-intricity101 : https://www.youtube.com/watch?v=uTQ_3BA3qbc

## Jour 2 — Protéger : qui voit quoi

Guide à suivre en premier (FR) :
- Le même guide, sections 5.1 (masquage dynamique) et 5.2 (politiques d'accès par ligne), puis l'atelier de la section 11, étapes 1 à 4 : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/15-gouvernance.md
- Rappel sur les rôles et les droits : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/10-securite.md

Documentation officielle Snowflake :
- Sécurité au niveau des colonnes (masquage, comportement avec CREATE TABLE AS SELECT et les vues) : https://docs.snowflake.com/en/user-guide/security-column-intro
- Masquage attaché à un tag : https://docs.snowflake.com/en/user-guide/tag-based-masking-policies
- Politiques d'accès par ligne (dont l'exemple avec une table de correspondance) : https://docs.snowflake.com/en/user-guide/security-row-intro
- Fonction POLICY_REFERENCES (où une politique est-elle attachée ?) : https://docs.snowflake.com/en/sql-reference/functions/policy_references
- INSERT, option OVERWRITE : https://docs.snowflake.com/en/sql-reference/sql/insert

Vidéos :
- Vidéo (EN) — Snowflake Data Governance Features - 1 - Data Masking & Row Access, Anupam Kushwah : https://www.youtube.com/watch?v=FTLrAGpXgsQ
- Vidéo (EN) — Protect Sensitive Data in Snowflake with Dynamic Masking, Mastering Snowflake : https://www.youtube.com/watch?v=u4fHBJUMulg
- Vidéo (EN) — Tag Based Dynamic Data Masking In Snowflake, Data Engineering Simplified : https://www.youtube.com/watch?v=80l8943gGk0
- Vidéo (EN) — Snowflake Row-level Security In-depth explanation, Knowledge Amplifier : https://www.youtube.com/watch?v=hUNWmJG0OkY

## Jour 3 — Conserver, contrôler, auditer, présenter

Guides à suivre en premier (FR) :
- Stockage et protection des données, sections 4 (Time Travel) et 5 (Fail-safe) : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/13-stockage-protection.md
- Gouvernance, section 6 (auditer : `ACCOUNT_USAGE`, `ACCESS_HISTORY`, latences) : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/15-gouvernance.md
- Airflow 3 avec Astro CLI, section 6 (fichiers SQL et contrôles) : https://github.com/gsoulat/formation-data-IA/blob/main/06-Data-Engineering/Airflow/06-Airflow3-Astro/01-airflow3-astro-snowflake.md

Documentation officielle :
- Time Travel (durée de rétention, clause AT) : https://docs.snowflake.com/en/user-guide/data-time-travel
- Fail-safe : https://docs.snowflake.com/en/user-guide/data-failsafe
- REMOVE (retirer un fichier d'un stage) : https://docs.snowflake.com/en/sql-reference/sql/remove
- Vue ACCESS_HISTORY : https://docs.snowflake.com/en/sql-reference/account-usage/access_history
- Opérateurs SQL d'Airflow (lien non vérifié) : https://airflow.apache.org/docs/apache-airflow-providers-common-sql/stable/operators.html

Réglementation :
- CNIL, les durées de conservation des données : https://www.cnil.fr/fr/les-durees-de-conservation-des-donnees
- CNIL, le registre des activités de traitement (trame complète) : https://www.cnil.fr/fr/RGPD-le-registre-des-activites-de-traitement
- Vidéo (FR) — Comment déterminer la durée de conservation d'une donnée personnelle ?, Leto : https://www.youtube.com/watch?v=idQwBOcYcbI

## Bonus

- Bonus 1, classification automatique : https://docs.snowflake.com/en/user-guide/classify-intro et la procédure `SYSTEM$CLASSIFY` https://docs.snowflake.com/en/sql-reference/stored-procedures/system_classify (elle consomme des crédits)
- Bonus 2, tâches planifiées : section 7 du guide https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/18-transformation.md et https://docs.snowflake.com/en/sql-reference/sql/create-task
- Bonus 3, politiques d'agrégation : https://docs.snowflake.com/en/user-guide/aggregation-policies

## À savoir

- Les fonctions de mesure de la qualité intégrées à Snowflake (*data metric functions*) ne sont pas disponibles sur un compte d'essai : les règles de qualité de ce brief s'écrivent en SQL et s'exécutent avec Airflow.
- La propagation automatique des tags existe (https://docs.snowflake.com/en/user-guide/object-tagging/propagation) mais n'est pas demandée : comprenez d'abord ce qui se passe sans elle.
