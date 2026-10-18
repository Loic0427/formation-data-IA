# 14. Fonctions d'IA et applications : Cortex, Snowflake ML, Snowpark, notebooks, Streamlit et applications natives

[← Retour au sommaire](README.md) | [← Précédent](13-stockage-protection.md) | [Suivant →](15-gouvernance.md)

## Vue d'ensemble

Snowflake n'est plus seulement un entrepôt où l'on exécute du SQL. La plateforme permet aussi d'appeler des modèles de langage depuis une requête, d'écrire des traitements en Python, de développer dans des notebooks et de publier de petites applications, le tout **sans sortir les données du compte**.

L'examen SnowPro Core COF-C03 a ajouté ces sujets au domaine 1, sous l'intitulé « fonctionnalités d'IA, de ML et de développement d'applications » : Snowflake Notebooks, Streamlit in Snowflake, Snowpark, Snowflake Cortex (fonctions SQL d'IA, Cortex Search, Cortex Analyst) et Snowflake ML. Le niveau attendu est de **reconnaître et situer** : pour chaque brique, savoir ce qu'elle fait, quand l'utiliser et ce qu'elle n'est pas. On ne vous demandera pas d'écrire une application.

C'est utile dans le métier : un Data Engineer est de plus en plus souvent celui qui prépare les données pour ces usages, qui choisit la brique adaptée à une demande (« on veut classer les avis clients », « on veut un écran pour le service commercial ») et qui en surveille le coût.

Exemple suivi : les avis clients du fichier `Data/ecommerce/reviews.csv`, chargés dans `SALES_DB.RAW_DATA.REVIEWS_RAW`, avec le rôle `SALES_ENGINEER` et le warehouse `SALES_WH`.

---

## 1. La carte d'ensemble

### 1.1 Une image pour s'y retrouver

Reprenons la bibliothèque du chapitre 12. Jusqu'ici, on y consultait des livres. Désormais, on y trouve aussi :
- un **assistant** à qui l'on demande de résumer, traduire ou classer des textes (Cortex) ;
- un **atelier** où l'on fabrique ses propres outils dans le langage de son choix (Snowpark, Snowflake ML) ;
- un **cahier de brouillon** partagé pour explorer et documenter (notebooks) ;
- un **guichet** où l'on présente les résultats au public (Streamlit) ;
- une **boutique** où l'on distribue ses créations à d'autres bibliothèques (applications natives).

Le principe commun : le code vient aux données, et non l'inverse. Les droits (RBAC) et la gouvernance du compte s'appliquent partout.

### 1.2 Qui fait quoi

| Brique | Ce que c'est | Pour qui | Mot-clé pour l'examen |
|---|---|---|---|
| **Cortex — fonctions SQL d'IA** | des fonctions SQL qui appellent un modèle de langage hébergé par Snowflake | toute personne qui écrit du SQL | texte, image, document traités dans un `SELECT` |
| **Cortex Search** | un service de recherche dans des textes, par sens et par mots-clés | développeurs d'assistants et de moteurs de recherche | recherche hybride, RAG |
| **Cortex Analyst** | un service qui transforme une question en français ou en anglais en requête SQL | utilisateurs métier, par l'intermédiaire d'une application | données structurées, modèle sémantique |
| **Snowflake ML** | un ensemble d'outils pour entraîner, enregistrer et déployer ses propres modèles | data scientists | registre de modèles, magasin de caractéristiques |
| **Snowpark** | des bibliothèques pour écrire des traitements en Python, Java ou Scala exécutés dans Snowflake | data engineers, data scientists | DataFrame, exécution dans le warehouse |
| **Snowflake Notebooks** | des carnets à cellules SQL, Python et Markdown dans Snowsight | exploration, prototypage | cellules, développement interactif |
| **Streamlit in Snowflake** | des applications web écrites en Python, hébergées dans Snowflake | restitution vers des utilisateurs internes | application de données sans infrastructure |
| **Applications natives** | des applications empaquetées qu'un fournisseur distribue à d'autres comptes | éditeurs, partenaires | *Native App Framework*, Marketplace |

---

## 2. Snowflake Cortex : l'IA par le SQL

### 2.1 Les fonctions SQL d'IA

Une fonction SQL d'IA s'appelle comme n'importe quelle fonction : on lui passe une colonne, elle renvoie un résultat pour chaque ligne. Le modèle de langage est hébergé et géré par Snowflake : il n'y a ni modèle à installer, ni clé d'API d'un service extérieur.

| Fonction | Ce qu'elle fait | Exemple d'usage |
|---|---|---|
| `AI_COMPLETE` | génère un texte à partir d'une consigne, avec le modèle de langage choisi | rédiger une réponse à un avis client |
| `AI_CLASSIFY` | range un texte ou une image dans des catégories que vous fournissez | classer des avis : livraison, qualité, prix |
| `AI_FILTER` | répond vrai ou faux à une question posée sur un texte ou une image | garder les avis qui mentionnent un défaut |
| `AI_SENTIMENT` | évalue le sentiment d'un texte | repérer les avis négatifs |
| `AI_SUMMARIZE` | résume un texte ou un document | condenser un long compte rendu |
| `AI_TRANSLATE` | traduit un texte d'une langue à une autre | traduire des avis en français |
| `AI_EXTRACT` | extrait des informations d'un texte ou d'un fichier | lire le montant et la date d'une facture |
| `AI_PARSE_DOCUMENT` | extrait le texte d'un document (reconnaissance de caractères), avec ou sans sa mise en page | rendre un PDF interrogeable |
| `AI_TRANSCRIBE` | transcrit un fichier audio ou vidéo déposé sur un stage | transcrire des appels |
| `AI_REDACT` | masque les données personnelles d'un texte | anonymiser avant analyse |
| `AI_EMBED` | transforme un texte ou une image en vecteur numérique (*embedding*) | préparer une recherche par similarité |
| `AI_SIMILARITY` | mesure la proximité de sens entre deux entrées | rapprocher des doublons |
| `AI_AGG` | applique une consigne à **l'ensemble des lignes** d'une colonne de texte | « quels sont les trois reproches les plus fréquents ? » |
| `AI_SUMMARIZE_AGG` | résume l'ensemble des lignes d'une colonne de texte | synthèse de tous les avis d'un produit |

Fonctions d'appoint : `AI_COUNT_TOKENS` (compter les jetons d'un texte pour estimer un coût), `PROMPT` (construire une consigne avec des variables), `TO_FILE` (désigner un fichier d'un stage).

Ces fonctions ont succédé à une première série rangée dans le schéma `SNOWFLAKE.CORTEX` (`COMPLETE`, `SUMMARIZE`, `TRANSLATE`, `SENTIMENT`, `EXTRACT_ANSWER`...), que vous croiserez encore dans des supports et des questions d'entraînement : le rôle de chaque fonction se devine à son nom.

### 2.2 Démonstration sur les avis clients

```sql
USE ROLE SALES_ENGINEER;
USE WAREHOUSE SALES_WH;
USE SCHEMA SALES_DB.RAW_DATA;

-- Un sentiment et une traduction par avis
SELECT review_id,
       rating,
       review_text,
       AI_SENTIMENT(review_text)              AS sentiment,       -- objet décrivant le sentiment
       AI_TRANSLATE(review_text, 'en', 'fr')  AS avis_en_francais -- langue source, langue cible
FROM REVIEWS_RAW
LIMIT 5;

-- Classer chaque avis dans une catégorie que l'on définit soi-même
SELECT review_id,
       review_text,
       AI_CLASSIFY(review_text, ['qualité du produit', 'batterie', 'confort', 'prix']) AS categorie
FROM REVIEWS_RAW
LIMIT 5;

-- Ne garder que les avis qui expriment une réserve
SELECT review_id, review_text
FROM REVIEWS_RAW
WHERE AI_FILTER(PROMPT('Cet avis contient-il une critique ? {0}', review_text));

-- Une seule réponse pour toute la table
SELECT AI_AGG(review_text, 'Cite en français les deux reproches les plus fréquents.') AS synthese
FROM REVIEWS_RAW;

-- Consigne libre, avec le modèle de son choix
SELECT review_id,
       AI_COMPLETE('<modèle>', 'Rédige en français une réponse courtoise à cet avis client : ' || review_text) AS reponse
FROM REVIEWS_RAW
WHERE rating <= 3
LIMIT 3;
```

`<modèle>` est à remplacer par le nom d'un modèle disponible dans la région du compte : la liste figure dans la documentation et évolue souvent. Plusieurs fonctions renvoient un objet (type `OBJECT`) plutôt qu'un texte simple : on en lit les champs avec la notation `:`.

Gardez toujours un `LIMIT` pendant les essais : chaque ligne traitée est facturée.

### 2.3 Droits, coût et confidentialité

| Sujet | Règle |
|---|---|
| Droits | le rôle doit avoir le privilège de compte `USE AI FUNCTIONS` et un rôle de base de données tel que `SNOWFLAKE.CORTEX_USER`. Par défaut, les deux sont accordés au rôle `PUBLIC`, donc à tous les utilisateurs ; un administrateur peut les retirer à `PUBLIC` pour restreindre l'accès |
| Coût | à l'usage, en crédits, selon le nombre de **jetons** (*tokens*, des fragments de mots) traités, et selon la fonction et le modèle. C'est une ligne de calcul distincte de celle du warehouse |
| Warehouse | la requête passe par un warehouse, mais le modèle ne tourne pas dessus : un grand warehouse n'accélère pas l'appel et coûte plus cher |
| Disponibilité | elle dépend de la région ; l'inférence entre régions peut être activée par un administrateur pour accéder à des modèles absents de la région du compte |
| Confidentialité | les données restent dans le périmètre de gouvernance de Snowflake |
| Nature du résultat | la réponse d'un modèle de langage est probabiliste : elle peut varier d'un appel à l'autre et peut être fausse. On la contrôle sur un échantillon |

```sql
-- Donner l'accès aux fonctions d'IA à un rôle (si l'administrateur l'a retiré du rôle PUBLIC)
USE ROLE ACCOUNTADMIN;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE SALES_ENGINEER;
```

Les fonctions SQL d'IA sont conçues pour le traitement **par lots** (beaucoup de lignes, débit élevé), pas pour une réponse immédiate dans une application interactive, pour laquelle Snowflake renvoie vers son API REST.

### 2.4 Cortex Search : retrouver les bons passages

**Cortex Search** est un service de recherche géré, sur des données textuelles. Il combine la recherche par mots-clés et la recherche par le sens (recherche vectorielle) : on parle de recherche **hybride**. On le crée en SQL ; Snowflake calcule les vecteurs, construit l'index et le rafraîchit quand les données changent.

```sql
CREATE OR REPLACE CORTEX SEARCH SERVICE SALES_DB.ANALYTICS.REVIEWS_SEARCH
  ON review_text                       -- colonne dans laquelle on cherche
  ATTRIBUTES product_id                -- colonnes utilisables comme filtres
  WAREHOUSE = SALES_WH                 -- warehouse des rafraîchissements
  TARGET_LAG = '1 hour'                -- fraîcheur cible de l'index
  AS (SELECT review_id, product_id, review_text FROM SALES_DB.RAW_DATA.REVIEWS_RAW);
```

Deux usages principaux :
- le **RAG** (*retrieval-augmented generation*, génération augmentée par la recherche) : avant de faire répondre un modèle de langage, on va chercher les passages pertinents dans ses propres documents et on les lui fournit, pour qu'il réponde à partir de faits et non de mémoire ;
- la **recherche d'entreprise** : une barre de recherche dans une application.

Ce que ce n'est pas : Cortex Search ne rédige pas de réponse, il renvoie des passages. Il ne faut pas le confondre avec le service d'optimisation de la recherche (*search optimization service*), qui accélère des requêtes SQL très sélectives sur des tables.

### 2.5 Cortex Analyst : poser une question aux données structurées

**Cortex Analyst** est un service géré qui transforme une question en langage courant (« quel a été le chiffre d'affaires par pays le mois dernier ? ») en requête SQL, sur des **données structurées** (des tables).

Pour répondre juste, il s'appuie sur un **modèle sémantique** (une vue sémantique, ou un fichier YAML dans l'ancienne forme) qui décrit les tables, leurs liens et le vocabulaire métier : ce que veut dire « chiffre d'affaires », quelle colonne est une date. On y accède par une **API REST**, depuis une application (Streamlit, par exemple). Les droits du rôle de l'utilisateur continuent de s'appliquer, et la facturation se fait au message traité, en plus du warehouse qui exécute le SQL produit.

| | Cortex Search | Cortex Analyst |
|---|---|---|
| Données | textes, documents (non structuré) | tables (structuré) |
| Renvoie | les passages les plus pertinents | une requête SQL et son résultat |
| S'appuie sur | un index hybride tenu à jour | un modèle sémantique |
| Question type | « que disent nos contrats sur les pénalités de retard ? » | « combien de commandes en mars, par région ? » |

À connaître de nom : les **Cortex Agents** combinent ces deux services pour répondre à des questions qui demandent à la fois des chiffres et des documents.

---

## 3. Snowflake ML : ses propres modèles

**Snowflake ML** regroupe les outils pour mener un projet d'apprentissage automatique de bout en bout sur des données gouvernées, sans les exporter. La différence avec Cortex : Cortex fournit des modèles **prêts à l'emploi** ; Snowflake ML sert à **entraîner et exploiter les vôtres**.

| Composant | Rôle |
|---|---|
| Registre de modèles (*Model Registry*) | enregistrer, versionner et déployer des modèles, quelle que soit leur origine. Un modèle enregistré est un objet de schéma |
| Magasin de caractéristiques (*Feature Store*) | définir, stocker et retrouver les variables d'entrée des modèles, tenues à jour automatiquement |
| Environnement d'exécution en conteneurs (*Container Runtime*) | environnement préparé pour l'entraînement, avec processeurs graphiques si besoin |
| Tâches ML (*ML Jobs*) | automatiser l'exécution des chaînes d'entraînement |
| Observabilité et traçabilité | surveiller la dérive d'un modèle en production ; retracer le chemin des données jusqu'au modèle |

La bibliothèque Python associée est `snowflake-ml-python`.

---

## 4. Snowpark : du code Python, Java ou Scala exécuté dans Snowflake

### 4.1 Le principe

**Snowpark** est un ensemble de bibliothèques qui permet d'interroger et de transformer les données de Snowflake en **Python, Java ou Scala**, avec des **DataFrames**, à la manière de pandas ou de Spark.

Le point essentiel : le code que vous écrivez **ne traite pas les données sur votre poste**. Snowpark le traduit en SQL, et ce SQL s'exécute dans un warehouse de Snowflake. Il n'y a pas de cluster Spark à gérer et les données ne sortent pas du compte.

```
votre code Python (DataFrame)
      │  traduit en SQL
      ▼
warehouse Snowflake (exécution)  →  seul le résultat demandé revient
```

### 4.2 Démonstration

```python
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import avg, col, count

session = get_active_session()          # dans un notebook ou une application Streamlit de Snowflake

avis = session.table("SALES_DB.RAW_DATA.REVIEWS_RAW")      # aucune donnée lue à ce stade

notes = (
    avis.filter(col("VERIFIED_PURCHASE") == 1)             # toujours rien d'exécuté
        .group_by("PRODUCT_ID")
        .agg(avg("RATING").alias("NOTE_MOYENNE"), count("REVIEW_ID").alias("NB_AVIS"))
)

notes.show()                            # l'action déclenche l'exécution dans le warehouse
notes.write.save_as_table("SALES_DB.ANALYTICS.PRODUCT_RATINGS", mode="overwrite")
```

L'évaluation est **paresseuse** (*lazy*) : `filter`, `group_by` et `agg` ne font que décrire le calcul. Rien ne s'exécute tant qu'une action (`show`, `collect`, `to_pandas`, écriture dans une table) n'est pas demandée.

### 4.3 Fonctions et procédures

Snowpark sert aussi à créer deux objets de schéma, que l'on peut également écrire directement en SQL :

| | Fonction définie par l'utilisateur (UDF) | Procédure stockée |
|---|---|---|
| Renvoie | toujours une valeur (ou une table, pour une UDTF) | éventuellement une valeur |
| S'appelle | dans une requête : `SELECT ma_fonction(colonne)` | avec `CALL ma_procedure()` |
| Sert à | un calcul appliqué à chaque ligne | enchaîner des opérations : créer des tables, charger, administrer |
| Langages | SQL, Python, Java, JavaScript, Scala | SQL (Snowflake Scripting), Python, Java, JavaScript, Scala |

```sql
-- UDF en SQL : montant toutes taxes comprises
CREATE OR REPLACE FUNCTION SALES_DB.ANALYTICS.MONTANT_TTC(montant FLOAT)
  RETURNS FLOAT
  AS $$ montant * 1.2 $$;

SELECT order_id, total_amount, SALES_DB.ANALYTICS.MONTANT_TTC(total_amount) AS ttc
FROM SALES_DB.RAW_DATA.ORDERS_RAW LIMIT 5;
```

Pour les traitements Snowpark gourmands en mémoire (entraînement de modèles), on utilise un warehouse optimisé pour Snowpark (chapitre 12, section 5.6). À connaître de nom : **Snowpark Container Services** exécute des conteneurs dans Snowflake, sur des groupes de machines appelés *compute pools*, pour ce qui ne tient pas dans un warehouse.

---

## 5. Snowflake Notebooks

Un **notebook** est un carnet de travail, dans Snowsight, composé de cellules de trois sortes : **SQL**, **Python** et **Markdown** (texte). Le résultat d'une cellule SQL se réutilise dans une cellule Python, et inversement.

| Sujet | À retenir |
|---|---|
| Usages | exploration de données, prototypage de transformations, science des données, documentation d'une analyse |
| Calcul | sur un warehouse (environnement « warehouse »), ou sur un *compute pool* (environnement « conteneur », avec processeurs graphiques et installation libre de paquets) |
| Outils intégrés | Snowpark et Streamlit sont disponibles dans les cellules Python ; bibliothèques de graphiques courantes |
| Collaboration | droits gérés par rôles ; intégration avec Git ; exécution planifiable |
| Évolution | Snowflake fait migrer les notebooks vers une nouvelle génération, intégrée aux espaces de travail (*Workspaces*) de Snowsight et compatible avec Jupyter ; le principe des cellules reste le même |

Ce que ce n'est pas : un notebook est un outil de développement interactif, pas un ordonnanceur de production ni une application pour utilisateurs finaux.

---

## 6. Streamlit in Snowflake

**Streamlit** est une bibliothèque Python libre qui transforme un script en application web (filtres, graphiques, tableaux) sans écrire de HTML ni de JavaScript. **Streamlit in Snowflake** héberge ces applications dans le compte : Snowflake gère le calcul et le stockage de l'application.

```python
import streamlit as st
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.title("Avis clients")
note_min = st.slider("Note minimale", 1, 5, 3)                       # un curseur à l'écran

avis = session.table("SALES_DB.RAW_DATA.REVIEWS_RAW").filter(f"RATING >= {note_min}")
st.metric("Nombre d'avis", avis.count())
st.dataframe(avis.select("PRODUCT_ID", "RATING", "REVIEW_TEXT").to_pandas())
```

| Sujet | À retenir |
|---|---|
| Nature | l'application est un objet de schéma (`STREAMLIT`), créé depuis Snowsight, en SQL ou avec Snowflake CLI |
| Accès | par les rôles : on partage l'application avec un rôle, pas avec une adresse publique |
| Calcul | un warehouse (ou un environnement en conteneur) tourne tant que l'application est utilisée : elle consomme des crédits |
| Données | elles ne quittent pas Snowflake |
| Usages | petit outil interne, tableau de bord sur mesure, interface de saisie, démonstrateur d'IA |

Ce que ce n'est pas : ce n'est pas un outil de BI généraliste comme Power BI ou Tableau, ni un site web ouvert au public.

---

## 7. Les applications natives

Le **Native App Framework** permet à un **fournisseur** d'empaqueter des données et de la logique dans une application, et de la distribuer à des **consommateurs**, qui l'installent dans leur propre compte.

```
FOURNISSEUR                                  CONSOMMATEUR
paquet d'application                         application installée
(application package)        annonce         dans son compte
├── fichier manifeste     ──(listing)──►     ├── s'exécute chez lui
├── script d'installation   Marketplace      ├── sur ses données
└── code, données, Streamlit  ou privée      └── le code du fournisseur reste protégé
```

| Notion | Définition |
|---|---|
| Paquet d'application (*application package*) | le conteneur, côté fournisseur : données, logique, métadonnées |
| Fichier manifeste (*manifest*) | décrit la configuration et les propriétés de l'application |
| Script d'installation (*setup script*) | instructions SQL exécutées à l'installation et à chaque mise à jour |
| Annonce (*listing*) | le moyen de distribution : publique sur la Snowflake Marketplace, ou privée vers des comptes choisis |
| Application | l'objet créé dans le compte du consommateur à l'installation |
| Versions et correctifs | le fournisseur publie des mises à jour que les consommateurs reçoivent |

Une application native peut contenir une interface Streamlit, des procédures stockées, des fonctions, et des conteneurs.

Ne pas confondre avec le partage de données : un partage (*share*) donne un accès en lecture à des objets ; une application native livre en plus du code qui s'exécute dans le compte du consommateur.

---

## 8. Quelle brique pour quel besoin

| Besoin exprimé | Brique |
|---|---|
| « Classer, résumer ou traduire des milliers de textes stockés dans une table » | fonctions SQL d'IA de Cortex |
| « Extraire le contenu de factures PDF déposées sur un stage » | `AI_PARSE_DOCUMENT`, `AI_EXTRACT` |
| « Un assistant qui répond à partir de notre documentation interne » | Cortex Search (pour le RAG) et `AI_COMPLETE` |
| « Les commerciaux veulent interroger les ventes en langage courant » | Cortex Analyst, avec un modèle sémantique |
| « Entraîner notre propre modèle de prévision et le suivre en production » | Snowflake ML |
| « Écrire une transformation complexe en Python sans sortir les données » | Snowpark |
| « Appliquer un calcul maison à chaque ligne d'une requête » | UDF |
| « Enchaîner plusieurs opérations d'administration ou de chargement » | procédure stockée |
| « Explorer un jeu de données en mêlant SQL, Python et commentaires » | Snowflake Notebooks |
| « Un écran simple pour que l'équipe consulte et filtre des résultats » | Streamlit in Snowflake |
| « Vendre notre outil d'analyse à d'autres clients de Snowflake » | application native, publiée sur la Marketplace |

---

## 9. Pièges fréquents

| Confusion | La réalité |
|---|---|
| « Cortex envoie mes données à un service extérieur » | les modèles sont hébergés par Snowflake et les données restent dans son périmètre de gouvernance |
| « Un warehouse plus grand accélère les fonctions d'IA » | le modèle ne tourne pas sur le warehouse ; le coût principal est celui des jetons traités |
| « Cortex Search répond aux questions sur les chiffres de vente » | Search cherche dans des textes ; les questions sur des tables relèvent de Cortex Analyst |
| « Cortex Analyst fonctionne sans préparation » | il lui faut un modèle sémantique qui décrit les tables et le vocabulaire métier |
| « Cortex Search et l'optimisation de la recherche, c'est pareil » | le premier est une recherche par le sens dans des textes ; le second accélère des requêtes SQL sélectives |
| « Snowpark, c'est Spark » | l'interface y ressemble, mais l'exécution se fait dans les warehouses de Snowflake, sans cluster Spark |
| « Snowpark rapatrie les données sur mon poste » | le code est traduit en SQL exécuté côté Snowflake ; seul le résultat demandé revient |
| « Chaque ligne Snowpark s'exécute immédiatement » | l'évaluation est paresseuse : rien ne part avant une action |
| « Une UDF et une procédure stockée sont interchangeables » | l'UDF renvoie une valeur et s'appelle dans un `SELECT` ; la procédure s'appelle avec `CALL` |
| « Cortex et Snowflake ML, c'est la même chose » | Cortex : modèles prêts à l'emploi ; Snowflake ML : entraîner et gérer ses propres modèles |
| « Une application Streamlit dans Snowflake est publique » | elle est réservée aux rôles auxquels on l'a ouverte |
| « Une application native s'exécute chez le fournisseur » | elle s'installe et s'exécute dans le compte du consommateur |
| « Le résultat d'une fonction d'IA est exact et reproductible » | il est probabiliste : on le vérifie |

---

## 10. À retenir pour la certification

- Programme COF-C03, domaine 1 : Snowflake Notebooks, Streamlit in Snowflake, Snowpark, Snowflake Cortex (fonctions SQL d'IA, Cortex Search, Cortex Analyst), Snowflake ML.
- Fonctions SQL d'IA : appelées dans une requête, modèles hébergés par Snowflake, facturation selon les jetons traités.
- Associer chaque fonction à son rôle : `AI_COMPLETE` (générer), `AI_CLASSIFY` (catégoriser), `AI_FILTER` (vrai ou faux), `AI_SENTIMENT`, `AI_SUMMARIZE`, `AI_TRANSLATE`, `AI_EXTRACT`, `AI_PARSE_DOCUMENT` (texte d'un document), `AI_EMBED` (vecteur), `AI_AGG` et `AI_SUMMARIZE_AGG` (sur plusieurs lignes).
- Accès : rôle de base de données `SNOWFLAKE.CORTEX_USER` et privilège `USE AI FUNCTIONS`.
- Cortex Search : recherche hybride (vecteurs et mots-clés) sur du texte ; usages : RAG et recherche d'entreprise ; index rafraîchi automatiquement.
- Cortex Analyst : question en langage courant → SQL, sur données structurées ; modèle sémantique ; API REST.
- Snowflake ML : registre de modèles, magasin de caractéristiques, entraînement ; pour ses propres modèles.
- Snowpark : Python, Java, Scala ; DataFrames ; évaluation paresseuse ; exécution dans Snowflake.
- UDF : renvoie une valeur, s'appelle dans une requête. Procédure stockée : `CALL`.
- Warehouse optimisé pour Snowpark : pour les traitements qui demandent beaucoup de mémoire.
- Notebooks : cellules SQL, Python, Markdown, dans Snowsight.
- Streamlit in Snowflake : application Python hébergée dans le compte, objet de schéma, accès par rôles.
- Applications natives : fournisseur, consommateur, paquet d'application, fichier manifeste, script d'installation ; distribution par annonce, sur la Marketplace ou en privé ; exécution dans le compte du consommateur.

---

## 11. Atelier pratique : des avis clients à une petite application (45 minutes)

Objectif : utiliser quatre briques sur le même jeu de données et savoir dire ce que chacune a apporté. Jeu de données : `Data/ecommerce/reviews.csv` (colonnes `review_id`, `product_id`, `customer_id`, `rating`, `review_text`, `review_date`, `helpful_count`, `verified_purchase`).

Avant de commencer : la disponibilité des fonctions d'IA dépend de la région et du type de compte. Si l'étape 2 renvoie une erreur de fonction inconnue ou de région non prise en charge, notez le message, lisez la page de disponibilité régionale de la documentation et passez aux étapes 3 et 4, qui n'en dépendent pas.

### Étape 1 — Préparer (10 minutes)

Chargez `Data/ecommerce/reviews.csv` dans `SALES_DB.RAW_DATA.REVIEWS_RAW` avec le rôle `SALES_ENGINEER` (chapitre 7 ou chapitre 11). Puis donnez au rôle le droit de créer un notebook et une application Streamlit :

```sql
USE ROLE SYSADMIN;        -- ou le rôle propriétaire du schéma
GRANT CREATE NOTEBOOK, CREATE STREAMLIT ON SCHEMA SALES_DB.ANALYTICS TO ROLE SALES_ENGINEER;

USE ROLE SALES_ENGINEER;
USE WAREHOUSE SALES_WH;
SELECT COUNT(*), MIN(rating), MAX(rating) FROM SALES_DB.RAW_DATA.REVIEWS_RAW;
```

### Étape 2 — Fonctions SQL d'IA (15 minutes)

1. Exécutez la première requête de la section 2.2 (sentiment et traduction) sur 5 lignes.
2. Comparez le sentiment renvoyé à la colonne `rating` : sont-ils cohérents ?
3. Classez tous les avis avec `AI_CLASSIFY` dans trois catégories de votre choix, et enregistrez le résultat :

```sql
CREATE OR REPLACE TABLE SALES_DB.ANALYTICS.REVIEWS_CLASSIFIED AS
SELECT review_id, product_id, rating, review_text,
       AI_CLASSIFY(review_text, ['<catégorie 1>', '<catégorie 2>', '<catégorie 3>']) AS classement
FROM SALES_DB.RAW_DATA.REVIEWS_RAW;

SELECT * FROM SALES_DB.ANALYTICS.REVIEWS_CLASSIFIED LIMIT 10;
```

4. Relancez la même classification sur 5 lignes : obtenez-vous exactement le même résultat ?

### Étape 3 — Snowpark dans un notebook (10 minutes)

Dans Snowsight, créez un notebook dans `SALES_DB.ANALYTICS` avec le warehouse `SALES_WH`. Ajoutez une cellule Markdown qui décrit l'objectif, une cellule SQL qui compte les avis par note, et une cellule Python avec le code de la section 4.2. Ajoutez une ligne `print(notes.queries)` avant `notes.show()` : que contient-elle ?

### Étape 4 — Une application Streamlit (10 minutes)

Dans Snowsight, créez une application Streamlit dans `SALES_DB.ANALYTICS` avec le warehouse `SALES_WH`, collez le code de la section 6 et exécutez-la. Ajoutez un graphique du nombre d'avis par note :

```python
par_note = session.table("SALES_DB.RAW_DATA.REVIEWS_RAW").group_by("RATING").count().sort("RATING").to_pandas()
st.bar_chart(par_note, x="RATING", y="COUNT")
```

Nettoyage : supprimez l'application, le notebook et la table `REVIEWS_CLASSIFIED`, et vérifiez que `SALES_WH` est suspendu.

### Questions de réflexion

1. À l'étape 2, qu'est-ce qui a été facturé en plus du warehouse ? Que deviendrait ce coût sur dix millions d'avis ?
2. À l'étape 3, où le calcul des notes moyennes a-t-il réellement été exécuté ? Qu'est-ce qui le prouve ?
3. Le service client veut retrouver « les avis qui parlent d'un problème de charge », sans connaître les mots exacts employés. Quelle brique ?
4. La direction veut demander « quelle est la note moyenne par catégorie de produit ce trimestre ? » sans écrire de SQL. Quelle brique, et que faut-il préparer avant ?
5. Un partenaire veut utiliser votre outil de classement d'avis sur ses propres données, dans son propre compte. Quelle brique, et par quel canal la distribuer ?

## ✅ Points de vérification
- [ ] Je sais dire en une phrase ce que fait chacune des huit briques de la section 1.2
- [ ] Je sais associer une fonction SQL d'IA à son usage
- [ ] Je distingue Cortex Search (textes) et Cortex Analyst (tables)
- [ ] Je distingue Cortex (modèles prêts à l'emploi) et Snowflake ML (ses propres modèles)
- [ ] Je sais expliquer où s'exécute un code Snowpark et ce qu'est l'évaluation paresseuse
- [ ] Je distingue une UDF et une procédure stockée
- [ ] J'ai créé un notebook et une application Streamlit dans mon compte
- [ ] Je sais décrire le parcours d'une application native, du fournisseur au consommateur

## Documentation officielle
- [Fonctions SQL d'IA de Cortex](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql)
- [Cortex Search](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview)
- [Cortex Analyst](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst)
- [Snowflake ML](https://docs.snowflake.com/en/developer-guide/snowflake-ml/overview)
- [Snowpark](https://docs.snowflake.com/en/developer-guide/snowpark/index)
- [Fonctions définies par l'utilisateur](https://docs.snowflake.com/en/developer-guide/udf/udf-overview)
- [Snowflake Notebooks](https://docs.snowflake.com/en/user-guide/ui-snowsight/notebooks)
- [Streamlit in Snowflake](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)
- [Native App Framework](https://docs.snowflake.com/en/developer-guide/native-apps/native-apps-about)
- [Warehouses optimisés pour Snowpark](https://docs.snowflake.com/en/user-guide/warehouses-snowpark-optimized)

---

[← Retour au sommaire](README.md) | [← Précédent](13-stockage-protection.md) | [Suivant →](15-gouvernance.md)
