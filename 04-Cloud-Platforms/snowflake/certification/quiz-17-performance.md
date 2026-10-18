# Quiz 17 — Performance et optimisation

[← Chapitre 17](../17-performance.md) | [← Sommaire du cours](../README.md)

20 questions au format de l'examen SnowPro Core (COF-C03), domaine 4. Une seule bonne réponse, sauf mention « 2 réponses attendues ». Comptez 25 minutes, sans le cours. Le corrigé est à la fin.

---

### Question 1
Combien de temps le résultat d'une requête est-il conservé dans le cache de résultats s'il n'est jamais réutilisé ?

- A. 1 heure
- B. 24 heures
- C. 7 jours
- D. 31 jours

### Question 2
Le lundi matin, 200 analystes lancent en même temps des requêtes simples sur un warehouse de taille Medium. Le profil montre que chaque requête s'exécute vite, mais passe un long moment en file d'attente. Le compte est en édition Enterprise. Quelle est la réponse la plus adaptée ?

- A. Passer le warehouse en taille X-Large
- B. Définir une clé de clustering sur les tables interrogées
- C. Configurer le warehouse en multi-cluster avec mise à l'échelle automatique
- D. Désactiver le cache de résultats

### Question 3
Le profil d'une requête affiche une valeur élevée pour « Bytes spilled to remote storage ». Quelles sont les deux actions pertinentes ? (2 réponses attendues)

- A. Utiliser un warehouse de taille supérieure
- B. Augmenter le nombre maximal de clusters du warehouse
- C. Réduire le volume traité : filtrer plus tôt, sélectionner moins de colonnes
- D. Augmenter la durée de rétention Time Travel de la table
- E. Passer la politique de mise à l'échelle à `ECONOMY`

### Question 4
Quelle requête peut être servie par le cache de métadonnées, sans warehouse en marche ?

- A. `SELECT COUNT(*) FROM ORDERS;`
- B. `SELECT COUNT(DISTINCT customer_id) FROM ORDERS WHERE total_amount > 100;`
- C. `SELECT * FROM ORDERS LIMIT 10;`
- D. `SELECT AVG(total_amount) FROM ORDERS GROUP BY ship_country;`

### Question 5
Que devient le cache du warehouse (données sur disque local) lorsque le warehouse est suspendu ?

- A. Il est conservé 24 heures
- B. Il est transféré dans la couche des services cloud
- C. Il est conservé tant que les tables ne changent pas
- D. Il est perdu

### Question 6
Quelle édition minimale de Snowflake est nécessaire pour créer une vue matérialisée ?

- A. Standard
- B. Business Critical
- C. Enterprise
- D. Virtual Private Snowflake

### Question 7
Quelles sont les deux affirmations exactes à propos des vues matérialisées ? (2 réponses attendues)

- A. Elles peuvent contenir une jointure entre deux tables
- B. Elles n'interrogent qu'une seule table
- C. Elles doivent être rafraîchies manuellement par une task
- D. Elles renvoient toujours des données à jour
- E. Elles peuvent contenir des fonctions de fenêtrage

### Question 8
Dans le profil d'une requête, un nœud de jointure reçoit 10 000 et 5 000 lignes en entrée et en produit 48 millions en sortie. Quel est le diagnostic le plus probable ?

- A. Élagage inefficace
- B. Jointure explosive due à une condition de jointure absente ou non unique
- C. Débordement sur le disque distant
- D. Cache du warehouse froid

### Question 9
Un warehouse multi-cluster utilise la politique de mise à l'échelle `ECONOMY`. Quand Snowflake démarre-t-il un cluster supplémentaire ?

- A. Dès qu'une requête est mise en file d'attente
- B. À heure fixe, selon un calendrier défini par l'administrateur
- C. Quand le cache de résultats est plein
- D. Quand il estime que la charge suffit à occuper ce cluster pendant au moins 6 minutes

### Question 10
Une table de 5 To contient l'historique des ventes. La plupart des requêtes filtrent sur une plage de dates et le profil montre que presque toutes les micro-partitions sont lues. La table est peu modifiée. Quelle optimisation est la plus adaptée ?

- A. Définir une clé de clustering sur la date de vente
- B. Activer le multi-cluster sur le warehouse
- C. Augmenter `AUTO_SUSPEND`
- D. Créer un index sur la colonne de date

### Question 11
Une table de plusieurs milliards de lignes est interrogée pour retrouver un client à partir de son adresse électronique (`WHERE email = '...'`). La table est déjà clusterisée par date. Quel service est conçu pour ce type de recherche ponctuelle ?

- A. Query Acceleration Service
- B. Une vue matérialisée avec jointure
- C. Le service d'optimisation de la recherche
- D. Le cache de métadonnées

### Question 12
On passe un warehouse de la taille Small à la taille Large pendant qu'une requête longue s'exécute. Que se passe-t-il pour cette requête ?

- A. Elle est annulée puis relancée sur la nouvelle taille
- B. Elle se termine sur les ressources d'origine ; seules les requêtes en attente et les nouvelles profitent de la nouvelle taille
- C. Elle bascule immédiatement sur les nouvelles ressources
- D. Elle est mise en pause jusqu'à la fin du changement de taille

### Question 13
Quelles sont les deux conditions nécessaires pour qu'une requête réutilise le cache de résultats ? (2 réponses attendues)

- A. Le warehouse qui a exécuté la première requête doit être en marche
- B. Le texte de la requête doit être identique à celui de la requête précédente
- C. La requête doit être lancée par le même utilisateur
- D. Les données des tables interrogées ne doivent pas avoir changé
- E. La table doit avoir une clé de clustering

### Question 14
À propos de la profondeur de clustering (*clustering depth*) d'une table qui contient des données, quelle affirmation est exacte ?

- A. Plus elle est élevée, mieux la table est rangée
- B. Elle n'existe que pour les tables qui ont une clé de clustering
- C. Elle correspond au nombre de colonnes de la clé
- D. Plus elle est faible, mieux la table est rangée

### Question 15
Une clé de clustering doit porter sur trois colonnes. Dans quel ordre la documentation recommande-t-elle de les déclarer ?

- A. De la cardinalité la plus faible à la plus forte
- B. De la cardinalité la plus forte à la plus faible
- C. Par ordre alphabétique
- D. L'ordre n'a aucune importance

### Question 16
Comment le reclustering automatique d'une table (Automatic Clustering) est-il exécuté et facturé ?

- A. Par le warehouse de l'utilisateur qui a défini la clé
- B. Gratuitement, par la couche des services cloud
- C. Par des ressources serverless gérées par Snowflake, facturées séparément des warehouses
- D. Par le warehouse par défaut du rôle `ACCOUNTADMIN`

### Question 17
Sur un warehouse de taille Medium, la plupart des requêtes sont courtes, mais quelques requêtes hors norme lisent des volumes énormes avec des filtres très sélectifs. Quelle fonction permet d'accélérer ces quelques requêtes sans agrandir le warehouse pour toutes les autres ?

- A. La politique de mise à l'échelle `ECONOMY`
- B. Query Acceleration Service
- C. Le cache de métadonnées
- D. `USE_CACHED_RESULT = FALSE`

### Question 18
Quel est le délai maximal d'apparition d'une requête dans la vue `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY`, et sur quelle durée cette vue conserve-t-elle l'historique ?

- A. Aucun délai ; 7 jours
- B. Jusqu'à 3 heures ; 90 jours
- C. Aucun délai ; 14 jours
- D. Jusqu'à 45 minutes ; 365 jours

### Question 19
La fonction `WAREHOUSE_LOAD_HISTORY` montre une valeur de `AVG_QUEUED_LOAD` régulièrement supérieure à 0 aux heures de bureau. Qu'est-ce que cela indique ?

- A. Des requêtes attendent parce que le warehouse est saturé
- B. Des requêtes sont bloquées par un verrou de transaction
- C. Le warehouse met trop de temps à démarrer
- D. Le cache du warehouse est trop petit

### Question 20
Une table `ORDERS` est bien rangée par `order_date`. Laquelle de ces requêtes risque le plus d'empêcher l'élagage des micro-partitions ?

- A. `WHERE order_date = '2024-03-15'`
- B. `WHERE order_date BETWEEN '2024-03-01' AND '2024-03-31'`
- C. `WHERE TO_CHAR(order_date, 'YYYY-MM') = '2024-03'`
- D. `WHERE order_date >= '2024-03-01'`

---

## Corrigé

| Question | Réponse | Explication | Section du chapitre 17 |
|---|---|---|---|
| 1 | B | Le résultat est conservé 24 heures ; chaque réutilisation relance ce délai, dans la limite de 31 jours. | 3.1 |
| 2 | C | La file d'attente due au nombre d'utilisateurs se traite en multipliant les clusters, pas en agrandissant le warehouse. | 2.2 |
| 3 | A, C | Le débordement vient d'un manque de mémoire : on réduit le volume traité ou on prend un warehouse plus grand ; des clusters supplémentaires n'aident pas une requête isolée. | 4.3 |
| 4 | A | Le nombre de lignes d'une table fait partie des métadonnées tenues par les services cloud ; les autres requêtes doivent lire les données. | 3.2 |
| 5 | D | Le cache du warehouse est porté par ses disques locaux : il disparaît à la suspension. | 3.3 |
| 6 | C | Les vues matérialisées demandent l'édition Enterprise ou supérieure. | 6.2 |
| 7 | B, D | Une vue matérialisée n'interroge qu'une table, sans jointure ni fenêtrage ; sa maintenance est automatique et les données lues sont toujours à jour. | 6.2 |
| 8 | B | Un nœud de jointure qui produit beaucoup plus de lignes qu'il n'en reçoit signale une jointure explosive. | 4.3 |
| 9 | D | `ECONOMY` ne démarre un cluster que si la charge estimée l'occupe au moins 6 minutes ; démarrer dès qu'une requête attend est le comportement de `STANDARD`. | 2.3 |
| 10 | A | Très grande table, filtres par plage sur la même colonne, peu de modifications : c'est le cas d'usage de la clé de clustering ; Snowflake n'a pas d'index sur les tables standard. | 5.3 |
| 11 | C | Le service d'optimisation de la recherche accélère les recherches ponctuelles par égalité sur de très grandes tables. | 6.1 |
| 12 | B | Le changement de taille n'affecte pas les requêtes en cours d'exécution. | 2.2 |
| 13 | B, D | Texte identique et données inchangées ; le cache de résultats ne demande ni warehouse ni même utilisateur, seulement les privilèges nécessaires. | 3.1 |
| 14 | D | La profondeur mesure le chevauchement des micro-partitions : plus elle est faible, meilleur est le rangement ; elle se mesure sur n'importe quelles colonnes. | 5.2 |
| 15 | A | La documentation recommande d'ordonner les colonnes de la cardinalité la plus faible à la plus forte. | 5.3 |
| 16 | C | Automatic Clustering utilise des ressources serverless de Snowflake, sans warehouse de l'utilisateur. | 5.5 |
| 17 | B | Query Acceleration Service confie une partie du travail des requêtes hors norme à des ressources de renfort, facturées à l'usage. | 6.3 |
| 18 | D | La vue `ACCOUNT_USAGE.QUERY_HISTORY` a jusqu'à 45 minutes de délai et conserve 365 jours. | 8.1 |
| 19 | A | `AVG_QUEUED_LOAD` compte les requêtes en attente pour cause de saturation ; le verrou correspond à `AVG_BLOCKED`, le démarrage à `AVG_QUEUED_PROVISIONING`. | 8.2 |
| 20 | C | Une fonction appliquée à la colonne filtrée peut empêcher la comparaison avec les minimum et maximum des micro-partitions. | 5.1 et 7 |

Répartition des bonnes réponses : A 5, B 6, C 6, D 6 (les questions à deux réponses comptent pour deux lettres).

**Lecture du score** : 16 ou plus, le chapitre est acquis ; de 12 à 15, relire les sections des questions ratées ; moins de 12, reprendre le chapitre et refaire l'atelier.
