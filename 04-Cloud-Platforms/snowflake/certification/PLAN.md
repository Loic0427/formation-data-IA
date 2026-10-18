# Plan de préparation à la certification SnowPro Core (COF-C03) en 8 jours

[← Sommaire du cours](../README.md) | [Fiche de révision](FICHE_REVISION.md) | [Planning de révision en 3 semaines](PLANNING_REVISION.md)

Ce document s'adresse au formateur, qui y trouve le déroulé jour par jour, et à l'apprenant, qui y trouve ce qu'il doit lire, pratiquer et réussir chaque jour. Il couvre les 19 chapitres du cours et les cinq domaines de l'examen.

Pour réviser seul après la formation, voir le [planning de révision en 3 semaines](PLANNING_REVISION.md), qui associe des vidéos à chaque chapitre.

---

## 1. L'examen en bref

Les informations ci-dessous viennent de la page officielle de la certification, consultée le 4 octobre 2026. Elles peuvent changer : vérifiez-les sur la [page officielle SnowPro Core](https://learn.snowflake.com/en/certifications/snowpro-core-c03/) avant de vous inscrire.

| Élément | Valeur |
|---|---|
| Nom et version | SnowPro Core Certification, COF-C03 |
| Nombre de questions | 100 |
| Types de questions | choix unique (multiple choice) et choix multiples (multiple select) |
| Durée | 115 minutes |
| Seuil de réussite | 750, sur une échelle de 0 à 1000 |
| Langues | anglais, japonais, coréen, français, espagnol |
| Prix | 175 dollars américains par tentative |
| Prérequis | aucun ; Snowflake décrit le candidat type comme ayant au moins 6 mois de pratique |
| Passage | en ligne avec surveillance à distance, ou en centre d'examen |

L'examen peut contenir des questions non notées, que rien ne distingue des autres : répondez à toutes avec le même soin. La note est une note mise à l'échelle : 750 ne signifie pas exactement 75 % de bonnes réponses.

### Les cinq domaines et les chapitres qui les couvrent

| Domaine (intitulé officiel) | Poids | Chapitres du cours |
|---|---|---|
| 1. Snowflake AI Data Cloud Features & Architecture : fonctionnalités et architecture | 31 % | [12](../12-architecture.md), [13](../13-stockage-protection.md), [14](../14-ia-applications.md), et 01 à 06 |
| 2. Account Management and Data Governance : gestion du compte et gouvernance | 20 % | [08](../08-gestion-privileges.md), [09](../09-monitoring.md), [10](../10-securite.md), [15](../15-gouvernance.md) |
| 3. Data Loading, Unloading, and Connectivity : chargement, déchargement et connectivité | 18 % | [07](../07-import-donnees.md), [11](../11-chargement-stage-copy.md), [16](../16-snowpipe-export-connectivite.md) |
| 4. Performance Optimization, Querying, and Transformation : performance, requêtes et transformation | 21 % | [17](../17-performance.md), [18](../18-transformation.md) |
| 5. Data Collaboration : collaboration autour des données | 10 % | [19](../19-collaboration.md) |

Sur 100 questions, cela représente environ 31, 20, 18, 21 et 10 questions. Les domaines 1 et 4 pèsent ensemble plus de la moitié de l'examen : c'est là que le temps de révision rapporte le plus.

---

## 2. Vue d'ensemble des 8 jours

| Jour | Thème | Domaine | Chapitres | Quiz |
|---|---|---|---|---|
| 1 | Découvrir la plateforme | 1 | 01 à 06, 12 | [quiz 12](quiz-12-architecture.md) |
| 2 | Architecture en profondeur | 1 | 13, 14 | [quiz 13](quiz-13-stockage-protection.md), [quiz 14](quiz-14-ia-applications.md) |
| 3 | Compte et gouvernance | 2 | 08, 10, 15, 09 | [quiz 15](quiz-15-gouvernance.md) |
| 4 | Charger, décharger, se connecter | 3 | 07, 11, 16 | [quiz 16](quiz-16-snowpipe-export-connectivite.md) |
| 5 | Performance | 4 | 17 | [quiz 17](quiz-17-performance.md) |
| 6 | Requêtes et transformation | 4 | 18 | [quiz 18](quiz-18-transformation.md) |
| 7 | Collaboration, puis révisions | 5, puis tous | 19, fiche de révision | [quiz 19](quiz-19-collaboration.md) |
| 8 | Examen blanc et plan individuel | tous | aucun nouveau | [examen blanc 1](examen-blanc-1.md) |

### La journée type (7 heures)

| Créneau | Durée | Activité |
|---|---|---|
| Matin | 3 h 30 (9 h à 12 h 30, pause comprise) | concepts : lecture guidée des chapitres, démonstrations du formateur, questions |
| Début d'après-midi | 2 h (13 h 30 à 15 h 30) | atelier pratique du chapitre, sur le compte d'essai de chaque apprenant |
| Fin d'après-midi | 1 h 30 (15 h 45 à 17 h 15) | quiz en temps limité, puis correction collective et mise à jour du carnet d'erreurs |

Le carnet d'erreurs est un simple fichier où chaque apprenant note, pour chaque question ratée, la règle qui lui manquait, formulée en une phrase. Il sert de support de révision les jours 7 et 8.

Chaque apprenant a besoin d'un compte d'essai Snowflake ([chapitre 01](../01-creation-compte.md)). L'essai est limité dans le temps et en crédits : créez le compte au plus tôt la veille du jour 1, et suspendez les warehouses en fin de journée.

---

## 3. Le détail jour par jour

### Jour 1. Découvrir la plateforme

**Objectifs.** Créer un compte et s'y connecter ; créer un rôle, un warehouse, une base, un schéma et des tables ; expliquer les trois couches de l'architecture (stockage, calcul, services) et ce que l'on paie pour chacune.

**À lire.** [01](../01-creation-compte.md), [02](../02-connexion.md), [03](../03-creation-role.md), [04](../04-creation-warehouse.md), [05](../05-creation-database-schema.md), [06](../06-creation-tables.md), puis [12](../12-architecture.md).

| Créneau | Contenu |
|---|---|
| Matin (3 h 30) | prise en main guidée, chapitres 01 à 06, chacun réalisé en direct sur son compte : l'apprenant termine la matinée avec `SALES_DB` et `SALES_WH` en place |
| Début d'après-midi (2 h) | chapitre 12 : lecture guidée (1 h), puis atelier du chapitre 12 (1 h) |
| Fin d'après-midi (1 h 30) | [quiz 12](quiz-12-architecture.md), correction, ouverture du carnet d'erreurs |

Les chapitres 01 à 06 sont courts et se font en pratiquant : la matinée est donc un atelier continu, et la partie conceptuelle est déplacée en début d'après-midi.

### Jour 2. Architecture en profondeur

**Objectifs.** Décrire les micro-partitions, les types de tables, Time Travel, Fail-safe et le clonage ; situer les fonctions d'IA et les applications (Cortex, Snowpark, Streamlit, applications natives) dans la plateforme.

**À lire.** [13](../13-stockage-protection.md), [14](../14-ia-applications.md).

| Créneau | Contenu |
|---|---|
| Matin (3 h 30) | chapitre 13 (2 h), chapitre 14 (1 h 30) |
| Début d'après-midi (2 h) | atelier du chapitre 13 (1 h 15), atelier du chapitre 14 (45 min) |
| Fin d'après-midi (1 h 30) | [quiz 13](quiz-13-stockage-protection.md) et [quiz 14](quiz-14-ia-applications.md), correction |

Ce jour clôt le domaine 1, le plus lourd de l'examen (31 %) : ne passez pas au jour 3 sans avoir corrigé toutes les erreurs des quiz 12 à 14.

### Jour 3. Compte et gouvernance

**Objectifs.** Expliquer le modèle de droits (rôles, privilèges, hiérarchie, propriété) ; écrire un script de droits rejouable ; décrire les politiques de masquage et d'accès aux lignes, les étiquettes (tags) et les méthodes d'authentification ; suivre la consommation et poser un moniteur de ressources.

**À lire.** [08](../08-gestion-privileges.md), [10](../10-securite.md), [15](../15-gouvernance.md), [09](../09-monitoring.md), dans cet ordre.

| Créneau | Contenu |
|---|---|
| Matin (3 h 30) | chapitres 08 et 10 (1 h 45), chapitre 15 (1 h 15), chapitre 09 (30 min) |
| Début d'après-midi (2 h) | exercice d'application du chapitre 10 (1 h), atelier du chapitre 15 (1 h) |
| Fin d'après-midi (1 h 30) | [quiz 15](quiz-15-gouvernance.md), correction |

### Jour 4. Charger, décharger, se connecter

**Objectifs.** Distinguer les types de stages et de formats de fichier ; charger avec `PUT` et `COPY INTO` ; expliquer Snowpipe et le chargement en continu ; décharger des données ; citer les connecteurs, pilotes et outils de connexion.

**À lire.** [07](../07-import-donnees.md), [11](../11-chargement-stage-copy.md), [16](../16-snowpipe-export-connectivite.md).

| Créneau | Contenu |
|---|---|
| Matin (3 h 30) | chapitre 07 (30 min), chapitre 11 (1 h 15), chapitre 16 (1 h 45) |
| Début d'après-midi (2 h) | exercice d'application du chapitre 11 (45 min), atelier du chapitre 16 (1 h 15) |
| Fin d'après-midi (1 h 30) | [quiz 16](quiz-16-snowpipe-export-connectivite.md), correction |

### Jour 5. Performance

**Objectifs.** Lire un profil de requête ; expliquer les trois caches ; choisir entre agrandir un warehouse et ajouter des clusters ; savoir quand utiliser une clé de clustering, le service d'optimisation de recherche, l'accélération de requêtes ou une vue matérialisée.

**À lire.** [17](../17-performance.md).

| Créneau | Contenu |
|---|---|
| Matin (3 h 30) | chapitre 17, avec démonstrations sur `SNOWFLAKE_SAMPLE_DATA` |
| Début d'après-midi (2 h) | atelier du chapitre 17 |
| Fin d'après-midi (1 h 30) | [quiz 17](quiz-17-performance.md), correction ; point d'étape : relecture du carnet d'erreurs des jours 1 à 5 |

### Jour 6. Requêtes et transformation

**Objectifs.** Interroger des données semi-structurées (`VARIANT`, `FLATTEN`) ; utiliser les vues, les fonctions et les procédures ; expliquer les flux (streams), les tâches (tasks) et les tables dynamiques.

**À lire.** [18](../18-transformation.md).

| Créneau | Contenu |
|---|---|
| Matin (3 h 30) | chapitre 18 |
| Début d'après-midi (2 h) | atelier du chapitre 18 |
| Fin d'après-midi (1 h 30) | [quiz 18](quiz-18-transformation.md), correction |

### Jour 7. Collaboration, puis révisions

**Objectifs.** Expliquer le partage sécurisé, les comptes lecteurs, les annonces et le Marketplace, la réplication et la bascule ; ne plus confondre partage, réplication et clonage. L'après-midi : consolider les cinq domaines.

**À lire.** [19](../19-collaboration.md) le matin, la [fiche de révision](FICHE_REVISION.md) l'après-midi.

| Créneau | Contenu |
|---|---|
| Matin (3 h 30) | chapitre 19 (1 h 30), atelier du chapitre 19 (45 min), [quiz 19](quiz-19-collaboration.md) et correction (45 min) |
| Début d'après-midi (2 h) | révisions guidées avec la [fiche de révision](FICHE_REVISION.md) : un domaine toutes les 20 à 25 minutes, en interrogation orale croisée par binômes |
| Fin d'après-midi (1 h 30) | chacun refait, sans le corrigé, le quiz où il a obtenu son plus mauvais score ; relecture du carnet d'erreurs |

### Jour 8. Examen blanc et plan de révision individuel

**Objectifs.** Se mesurer dans les conditions de l'examen ; savoir précisément quoi réviser avant le passage réel.

| Créneau | Contenu |
|---|---|
| Matin (3 h 30) | [examen blanc 1](examen-blanc-1.md) en conditions réelles : 100 questions, 115 minutes, sans documentation, sans échange, sans pause ; puis pause, puis autocorrection et calcul du score par domaine (1 h) |
| Début d'après-midi (2 h) | correction collective, centrée sur les questions ratées par plus d'un tiers du groupe |
| Fin d'après-midi (1 h 30) | chaque apprenant rédige son plan de révision individuel, puis le présente au formateur en 5 minutes |

Le plan de révision individuel tient en une page :

| Domaine | Score à l'examen blanc | Chapitres à relire | Ateliers à refaire | Date |
|---|---|---|---|---|
| 1 | ... sur 31 | | | |
| 2 | ... sur 20 | | | |
| 3 | ... sur 18 | | | |
| 4 | ... sur 21 | | | |
| 5 | ... sur 10 | | | |

Repère pour décider de la date d'inscription : un score d'au moins 80 % à l'examen blanc, sans domaine sous 70 %, donne une marge raisonnable. En dessous, suivez le [planning de révision en 3 semaines](PLANNING_REVISION.md) avant de vous inscrire. Ce repère est un conseil de formateur, pas une règle de Snowflake.

---

## 4. Conseils de préparation

### Méthode de révision

1. **Pratiquer avant de mémoriser.** Une règle vue fonctionner (ou échouer) sur son compte d'essai se retient mieux qu'une règle lue. Refaites les ateliers, y compris les essais qui doivent échouer.
2. **Tenir le carnet d'erreurs.** Une question ratée, une phrase : la règle qui manquait. Ne recopiez pas la question.
3. **Réviser par comparaison.** L'examen aime les paires proches : table transitoire ou temporaire, agrandir un warehouse ou ajouter des clusters, Time Travel ou Fail-safe, partage ou réplication, `COPY INTO` ou Snowpipe. Les tableaux de comparaison des chapitres sont faits pour cela.
4. **Apprendre les chiffres par cœur.** Durées de rétention, tailles, limites, éditions requises : ils sont réunis dans la [fiche de révision](FICHE_REVISION.md).
5. **Espacer les révisions.** Revoir un domaine le lendemain, puis trois jours après, puis une semaine après, vaut mieux qu'une longue séance unique.
6. **En cas de doute, la documentation officielle fait foi.** Chaque chapitre se termine par les liens utiles. Snowflake évolue vite : un guide tiers ou une vidéo peut être dépassé.

### Vocabulaire : examen en français ou en anglais ?

L'examen existe en français. Les noms d'objets, de commandes et de fonctions restent en anglais dans toutes les langues (`SHARE`, `COPY INTO`, Time Travel, Fail-safe), et la documentation de référence est en anglais. Si vous choisissez le français, connaissez tout de même les termes anglais : ce cours les donne systématiquement à côté de leur explication.

### Gérer son temps le jour de l'examen

115 minutes pour 100 questions, soit un peu plus d'une minute par question (69 secondes).

| Repère | Où en être |
|---|---|
| 30 minutes | question 30 |
| 60 minutes | question 60 |
| 90 minutes | question 90 |
| 100 minutes | premier passage terminé, 15 minutes pour revenir sur les questions marquées |

- **Premier passage sans s'arrêter.** Si la réponse ne vient pas en une minute, choisissez la plus plausible, marquez la question si l'interface le permet, et avancez.
- **Répondre à tout.** Rien n'indique, dans les informations officielles consultées, qu'une mauvaise réponse retire des points : ne laissez aucune question vide.
- **Questions à choix multiples.** L'énoncé indique le nombre de réponses attendues : cochez exactement ce nombre. Traitez chaque proposition comme un vrai ou faux indépendant.
- **Lire les mots qui changent tout.** « Minimum », « par défaut », « toujours », « uniquement », « n'est pas » : une proposition absolue est souvent fausse, mais pas toujours.
- **Éliminer.** Sur quatre propositions, deux sont en général écartées rapidement ; le choix se joue entre les deux restantes.
- **Ne changer une réponse que pour une raison précise.** Un fait retrouvé, pas une impression.

---

## 5. S'inscrire à l'examen

Les modalités d'inscription relèvent de Snowflake et de son prestataire d'examen ; elles peuvent évoluer. Ce qui suit décrit la démarche générale constatée sur le site officiel le 4 octobre 2026.

1. Consulter la [page officielle de la certification SnowPro Core](https://learn.snowflake.com/en/certifications/snowpro-core-c03/) : format, prix, langues, guide d'étude officiel (téléchargeable après avoir rempli un formulaire).
2. Suivre le bouton d'inscription de cette page, ou la [page d'inscription aux examens SnowPro](https://learn.snowflake.com/en/pages/snowpro-examreg/) : il faut créer un compte candidat sur le portail de certification de Snowflake.
3. Choisir la langue de l'examen et le mode de passage : en ligne avec surveillance à distance, ou en centre d'examen.
4. Payer les frais (175 dollars américains par tentative à la date de consultation) et réserver un créneau.

Avant de réserver, vérifiez sur les pages officielles, et dans la [foire aux questions des certifications](https://learn.snowflake.com/en/faqs/certification-faqs/), les points que ce document ne garantit pas : pièce d'identité exigée, configuration technique pour le passage en ligne, conditions de report et d'annulation, délai entre deux tentatives, durée de validité de la certification et conditions de renouvellement. La liste de toutes les certifications est sur la [page des certifications Snowflake](https://learn.snowflake.com/en/certifications/).

---

## 6. Articulation avec le brief « Pipeline médaillon NYC Yellow Taxi : Snowflake et Airflow »

Le dépôt contient un brief pratique : [Pipeline médaillon NYC Yellow Taxi : Snowflake et Airflow](../../../99-Brief/Data-Engineer/Snowflake/Snowflake+Airflow/BRIEF.md) (dossier `99-Brief/Data-Engineer/Snowflake/Snowflake+Airflow/`).

Il est conseillé de le réaliser **avant** ces 8 jours. Il fait pratiquer, sur un vrai projet, deux domaines de l'examen :

| Domaine de l'examen | Ce que le brief fait pratiquer | Chapitres liés |
|---|---|---|
| 2. Gestion du compte et gouvernance | rôles, droits, droits futurs, utilisateur de service, authentification par paire de clés | [08](../08-gestion-privileges.md), [10](../10-securite.md) |
| 3. Chargement, déchargement et connectivité | formats de fichier, stage, `PUT`, `COPY INTO`, chargement rejouable, connexion depuis Python et Airflow | [07](../07-import-donnees.md), [11](../11-chargement-stage-copy.md), [16](../16-snowpipe-export-connectivite.md) |

Conséquences pour le formateur :

- Avec un groupe qui a fait le brief, les jours 3 et 4 vont plus vite sur les chapitres 08, 10, 07 et 11 : le temps gagné est reporté sur les chapitres 15 et 16, dont le contenu (politiques de masquage, Snowpipe, déchargement, connecteurs) n'est pas pratiqué dans le brief.
- Avec un groupe qui ne l'a pas fait, gardez le déroulé tel quel et proposez le brief après la formation, comme mise en pratique.
- Le brief ne couvre pas les domaines 1, 4 et 5 : ils reposent entièrement sur les chapitres 12 à 14 et 17 à 19.

---

[← Sommaire du cours](../README.md) | [Fiche de révision](FICHE_REVISION.md) | [Planning de révision en 3 semaines](PLANNING_REVISION.md)
