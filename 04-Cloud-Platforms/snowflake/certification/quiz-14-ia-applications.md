# Quiz 14 — Fonctions d'IA et applications

[← Chapitre 14](../14-ia-applications.md) | [← Sommaire du cours](../README.md)

20 questions au format de l'examen SnowPro Core (COF-C03), domaine 1. Une seule bonne réponse, sauf mention « 2 réponses attendues ». Comptez 25 minutes, sans le cours. Le corrigé est à la fin.

---

### Question 1
Qu'est-ce qu'une fonction SQL d'IA de Snowflake Cortex ?

- A. Une fonction qui envoie les données à un service d'IA extérieur choisi par l'utilisateur
- B. Une fonction appelée dans une requête SQL, qui utilise un modèle de langage hébergé par Snowflake
- C. Une procédure stockée qu'il faut écrire en Python avant de l'utiliser
- D. Un type de warehouse réservé à l'intelligence artificielle

### Question 2
Une équipe veut ranger 50 000 avis clients dans trois catégories qu'elle a définies (« livraison », « qualité », « prix »), directement en SQL. Quelle fonction convient ?

- A. `AI_TRANSLATE`
- B. `AI_EMBED`
- C. `AI_CLASSIFY`
- D. `AI_PARSE_DOCUMENT`

### Question 3
Quelle fonction extrait le texte de documents PDF déposés sur un stage, avec ou sans leur mise en page ?

- A. `AI_PARSE_DOCUMENT`
- B. `AI_SENTIMENT`
- C. `AI_FILTER`
- D. `AI_AGG`

### Question 4
Sur quelle base l'utilisation des fonctions SQL d'IA est-elle principalement facturée ?

- A. Le nombre de micro-partitions lues
- B. Un abonnement mensuel fixe par utilisateur
- C. La taille du warehouse multipliée par le nombre de lignes
- D. Le nombre de jetons (*tokens*) traités, selon la fonction et le modèle

### Question 5
Quelles affirmations décrivent correctement Cortex Search ? (2 réponses attendues)

- A. Il combine recherche vectorielle et recherche par mots-clés
- B. Il transforme une question en requête SQL sur des tables
- C. Il exige que l'utilisateur calcule et stocke lui-même les vecteurs
- D. Il sert notamment à la génération augmentée par la recherche (RAG)
- E. Il accélère les requêtes SQL très sélectives sur de grandes tables

### Question 6
Des responsables commerciaux veulent poser des questions en langage courant sur les tables de ventes et obtenir des résultats chiffrés, sans écrire de SQL. Quelle brique est conçue pour cela ?

- A. Cortex Search
- B. Snowpark
- C. Cortex Analyst
- D. `AI_TRANSLATE`

### Question 7
De quoi Cortex Analyst a-t-il besoin pour produire des requêtes SQL justes ?

- A. D'un index vectoriel construit sur les tables
- B. D'un modèle sémantique qui décrit les tables, leurs liens et le vocabulaire métier
- C. D'un warehouse optimisé pour Snowpark
- D. D'une application native installée depuis la Marketplace

### Question 8
Quels langages l'interface DataFrame de Snowpark prend-elle en charge ?

- A. Python uniquement
- B. SQL et JavaScript
- C. Python, R et Julia
- D. Python, Java et Scala

### Question 9
Où s'exécutent les transformations écrites avec un DataFrame Snowpark ?

- A. Dans Snowflake : les opérations sont traduites en SQL et exécutées par un warehouse
- B. Sur le poste du développeur, après téléchargement des données
- C. Sur un cluster Spark que le client doit administrer
- D. Dans le navigateur, par Snowsight

### Question 10
Un développeur écrit `df = session.table("ORDERS_RAW").filter(col("TOTAL_AMOUNT") > 100)`. Que se passe-t-il à cet instant ?

- A. La table entière est copiée en mémoire sur son poste
- B. Une table temporaire filtrée est créée dans le schéma courant
- C. Rien n'est exécuté : le calcul ne partira qu'à la première action, par exemple `show()` ou `collect()`
- D. La requête s'exécute et son résultat est placé dans le cache de résultats

### Question 11
Quelle affirmation distingue correctement une UDF d'une procédure stockée ?

- A. Une UDF ne peut être écrite qu'en SQL ; une procédure, qu'en Python
- B. Une UDF s'appelle avec `CALL` ; une procédure s'utilise dans un `SELECT`
- C. Une UDF est un objet de compte ; une procédure est un objet de schéma
- D. Une UDF ne peut pas recevoir de paramètres
- E. Une UDF renvoie toujours une valeur et s'utilise dans une requête ; une procédure s'appelle avec `CALL`

### Question 12
Quels types de cellules un notebook Snowflake propose-t-il ?

- A. SQL uniquement
- B. SQL, Python et Markdown
- C. Python et R
- D. SQL, Scala et HTML

### Question 13
Une équipe veut mettre à disposition de collègues un petit écran interactif (filtres, graphiques) écrit en Python, sans gérer de serveur et sans sortir les données du compte. Que choisir ?

- A. Une vue matérialisée
- B. Cortex Search
- C. Un pilote ODBC
- D. Streamlit in Snowflake

### Question 14
Comment contrôle-t-on l'accès à une application Streamlit in Snowflake ?

- A. Par les rôles de Snowflake : l'application est un objet de schéma auquel on donne accès
- B. Par une adresse publique protégée par un mot de passe partagé
- C. Par une liste d'adresses IP saisie dans le code Python
- D. On ne le contrôle pas : toute personne ayant l'adresse peut l'ouvrir

### Question 15
Quels éléments font partie du Native App Framework ? (2 réponses attendues)

- A. Le moniteur de ressources
- B. Le volume externe
- C. Le paquet d'application (*application package*)
- D. La clé de clustering
- E. Le script d'installation (*setup script*)

### Question 16
Où s'exécute une application native une fois installée ?

- A. Dans le compte du fournisseur, qui reçoit les données du consommateur
- B. Dans le compte du consommateur
- C. Sur l'infrastructure de la Marketplace, hors de tout compte
- D. Sur le poste de travail de l'utilisateur

### Question 17
Une équipe de science des données veut enregistrer, versionner et déployer les modèles qu'elle a entraînés elle-même. Quel composant est prévu pour cela ?

- A. Cortex Analyst
- B. Le cache de résultats
- C. `AI_COMPLETE`
- D. Le registre de modèles (*Model Registry*) de Snowflake ML

### Question 18
Quelle fonction applique une consigne à l'ensemble des lignes d'une colonne de texte et renvoie une seule réponse de synthèse ?

- A. `AI_AGG`
- B. `AI_CLASSIFY`
- C. `AI_EMBED`
- D. `AI_TRANSLATE`

### Question 19
Quel rôle de base de données donne accès aux fonctions de Cortex ?

- A. `SNOWFLAKE.OBJECT_VIEWER`
- B. `SYSADMIN`
- C. `SNOWFLAKE.CORTEX_USER`
- D. `ORGADMIN`

### Question 20
Une entreprise veut construire un assistant qui répond aux questions des salariés à partir de milliers de documents internes (procédures, contrats). Quelle combinaison est la plus adaptée ?

- A. Cortex Analyst et une vue matérialisée
- B. Cortex Search pour retrouver les passages pertinents, puis `AI_COMPLETE` pour rédiger la réponse
- C. Un warehouse multi-cluster et le cache de résultats
- D. `AI_SENTIMENT` et une table dynamique

---

## Corrigé

| Question | Réponse | Explication | Section du chapitre |
|---|---|---|---|
| 1 | B | Les fonctions SQL d'IA s'appellent dans une requête et s'appuient sur des modèles hébergés par Snowflake. | 2.1 |
| 2 | C | `AI_CLASSIFY` range un texte dans des catégories fournies par l'utilisateur. | 2.1 |
| 3 | A | `AI_PARSE_DOCUMENT` extrait le texte d'un document, avec ou sans sa mise en page. | 2.1 |
| 4 | D | Le coût dépend du nombre de jetons traités, de la fonction et du modèle ; le warehouse n'héberge pas le modèle. | 2.3 |
| 5 | A, D | Cortex Search est une recherche hybride gérée, utilisée pour le RAG ; il calcule lui-même les vecteurs ; la question → SQL relève de Cortex Analyst, et l'accélération de requêtes sélectives du service d'optimisation de la recherche. | 2.4 |
| 6 | C | Cortex Analyst traduit une question en langage courant en SQL sur des données structurées. | 2.5 |
| 7 | B | Le modèle sémantique fournit à Cortex Analyst la description des tables et le vocabulaire métier. | 2.5 |
| 8 | D | Snowpark propose ses bibliothèques en Python, Java et Scala. | 4.1 |
| 9 | A | Snowpark traduit les opérations en SQL, exécuté par un warehouse de Snowflake, sans cluster extérieur. | 4.1 |
| 10 | C | L'évaluation est paresseuse : les transformations ne s'exécutent qu'à la première action. | 4.2 |
| 11 | E | Une UDF renvoie une valeur et s'utilise dans une requête ; une procédure stockée s'appelle avec `CALL`. | 4.3 |
| 12 | B | Un notebook Snowflake mêle des cellules SQL, Python et Markdown. | 5 |
| 13 | D | Streamlit in Snowflake héberge une application Python interactive dans le compte, sans serveur à gérer. | 6 |
| 14 | A | L'application est un objet de schéma `STREAMLIT`, ouvert à des rôles. | 6 |
| 15 | C, E | Le paquet d'application contient notamment le fichier manifeste et le script d'installation. | 7 |
| 16 | B | L'application native est installée et s'exécute dans le compte du consommateur. | 7 |
| 17 | D | Le registre de modèles de Snowflake ML enregistre, versionne et déploie les modèles de l'équipe. | 3 |
| 18 | A | `AI_AGG` agrège une colonne de texte et renvoie une réponse pour l'ensemble des lignes. | 2.1 |
| 19 | C | Le rôle de base de données `SNOWFLAKE.CORTEX_USER` ouvre l'accès aux fonctions de Cortex. | 2.3 |
| 20 | B | C'est le schéma du RAG : Cortex Search retrouve les passages, un modèle de langage rédige la réponse à partir d'eux. | 2.4, 8 |

Répartition des bonnes réponses : A 5, B 5, C 5, D 5, E 2 (les questions à deux réponses comptent pour deux lettres).

**Lecture du score** : 16 ou plus, le chapitre est acquis ; de 12 à 15, relire les sections des questions ratées ; moins de 12, reprendre le chapitre et refaire l'atelier.
