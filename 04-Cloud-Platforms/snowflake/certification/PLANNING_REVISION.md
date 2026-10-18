# Planning de révision et d'entraînement — SnowPro Core (COF-C03)

[← Plan de formation en 8 jours](PLAN.md) | [← Sommaire du cours](../README.md)

Ce planning s'adresse à un apprenant qui a suivi le cours et prépare l'examen seul. Il tient en **3 semaines**, à raison de **5 séances d'environ 1 h 30** par semaine, puis l'examen.

Chaque séance suit le même déroulé :

1. **Regarder** la vidéo indiquée (30 à 45 minutes), en prenant des notes.
2. **Relire** le chapitre du cours et sa section « À retenir pour la certification » (20 minutes).
3. **S'entraîner** : refaire l'atelier du chapitre sur son compte d'essai, ou le quiz, sans regarder le corrigé (30 minutes).
4. **Noter** dans un carnet les questions ratées et la règle qui manquait : c'est ce carnet qu'on relit la veille de l'examen.

## À savoir sur les vidéos

- Elles sont en anglais, sauf mention contraire. Sur YouTube : Paramètres → Sous-titres → Traduire automatiquement → Français.
- Leur existence a été vérifiée le 4 octobre 2026. Leur contenu n'a pas été visionné en entier : en cas de désaccord entre une vidéo et la documentation officielle, c'est la documentation qui fait foi.
- Plusieurs vidéos sont longues : le planning indique quelle partie regarder. Avancez en vitesse 1,25 si vous êtes à l'aise.

## Les deux vidéos fil rouge

| Vidéo | Durée | Usage |
|---|---|---|
| [Full Course for Snowflake SnowPro Core (COF-C03), Data-2-Dollars](https://www.youtube.com/watch?v=EpnptFl6Z4s) | environ 7 h | le cours vidéo complet, à suivre par chapitre tout au long des trois semaines |
| [Playlist « Tutorial for SnowPro Core COF-C03 : From Beginner to Certified », Data-2-Dollars](https://www.youtube.com/playlist?list=PLoBPFxYnzgeqRAplDY6HaNlO6l6FMv9e1) | par épisodes | le même contenu découpé par sujet, plus pratique pour revoir un point précis |

## Semaine 1 — Architecture et stockage (domaine 1, 31 % de l'examen)

| Séance | Sujet | Vidéo | À relire | Entraînement |
|---|---|---|---|---|
| 1 | L'examen et la plateforme | [SnowPro Core COF-C03 Exam Explained, CertQueen Guides](https://www.youtube.com/watch?v=1q4pmT8xomM) ; [Introduction to Snowflake, NIC IT Academy](https://www.youtube.com/watch?v=H40Y6nDoD8g) | [12. Architecture](../12-architecture.md) | lire le [plan en 8 jours](PLAN.md) et fixer sa date d'examen |
| 2 | Trois couches, warehouses, éditions | [Your Complete Snowflake Guide, DataMuscle](https://www.youtube.com/watch?v=cqdqkvLQnUk) : partie architecture et warehouses | [12. Architecture](../12-architecture.md) | [quiz 12](quiz-12-architecture.md) |
| 3 | Micro-partitions et clustering | [Micro-partitions & Data Clustering Explained Simply, Praveen Reddy Learnings](https://www.youtube.com/watch?v=eEe5Y_E4S1E) | [13. Stockage et protection](../13-stockage-protection.md) | atelier du chapitre 13 |
| 4 | Time Travel, Fail-safe, clonage | [Crash Course, Part 26 : Time Travel, Cloning, Replication & Encryption, Ganapathy Tech Tips](https://www.youtube.com/watch?v=O8FnTIkj95k) ; [A Quick Look At Zero Copy Cloning, Snowflake Developers](https://www.youtube.com/watch?v=uGCpwoQOQzQ) | [13. Stockage et protection](../13-stockage-protection.md) | [quiz 13](quiz-13-stockage-protection.md) |
| 5 | Fonctions d'IA, Snowpark, Streamlit | cours fil rouge : chapitre sur les fonctions d'IA et les applications | [14. IA et applications](../14-ia-applications.md) | [quiz 14](quiz-14-ia-applications.md) |

## Semaine 2 — Gouvernance et chargement (domaines 2 et 3, 38 % de l'examen)

| Séance | Sujet | Vidéo | À relire | Entraînement |
|---|---|---|---|---|
| 6 | Rôles, privilèges, propriété | [Roles in Snowflake](https://www.youtube.com/watch?v=-1aHd1WYus4) | [10. Sécurité](../10-securite.md) | exercice d'application du chapitre 10 |
| 7 | Authentification, politiques, masquage | cours fil rouge : chapitre sur la sécurité et la gouvernance | [15. Gouvernance](../15-gouvernance.md) | [quiz 15](quiz-15-gouvernance.md) |
| 8 | Coûts et suivi | [Your Complete Snowflake Guide, DataMuscle](https://www.youtube.com/watch?v=cqdqkvLQnUk) : partie coûts et mise à l'échelle | [09. Monitoring](../09-monitoring.md) | créer un resource monitor sur son compte d'essai |
| 9 | Stages et COPY INTO | [Snowflake Stages : Data Loading and Unloading, SleekData](https://www.youtube.com/watch?v=reWO0qqnpN0) ; [Data Loading : Using COPY Command & Stages, KnowHow Academy](https://www.youtube.com/watch?v=ZKiA6P_jU8k) | [11. Chargement](../11-chargement-stage-copy.md) | exercice d'application du chapitre 11 |
| 10 | Snowpipe, export, connecteurs | [Connect to S3 Storage (Copy Into / Snowpipe), Daniel Wilczak](https://www.youtube.com/watch?v=K9i_PWE_HHw) ; [Real-Time Ingestion And Transformation With Snowflake, Snowflake Developers](https://www.youtube.com/watch?v=GT3XkZtDrm8) | [16. Snowpipe, export, connectivité](../16-snowpipe-export-connectivite.md) | [quiz 16](quiz-16-snowpipe-export-connectivite.md) |

## Semaine 3 — Performance, transformation, collaboration, examens blancs (domaines 4 et 5, 31 % de l'examen)

| Séance | Sujet | Vidéo | À relire | Entraînement |
|---|---|---|---|---|
| 11 | Caches, mise à l'échelle, profil de requête | [Your Complete Snowflake Guide, DataMuscle](https://www.youtube.com/watch?v=cqdqkvLQnUk) : partie caches ; [Micro-Partitioning & Clustering Explained, Cloudlearningyard](https://www.youtube.com/watch?v=arqBva_2eRI) | [17. Performance](../17-performance.md) | [quiz 17](quiz-17-performance.md) |
| 12 | Données semi-structurées | [FLATTEN & LATERAL FLATTEN in Snowflake, Time Variant](https://www.youtube.com/watch?v=RGaSUBhkWKw) | [18. Transformation](../18-transformation.md) | atelier du chapitre 18 |
| 13 | Streams, tasks, tables dynamiques | [Snowflake Stream & Task Hands On, Data Engineering Simplified](https://www.youtube.com/watch?v=me4chjq0JCQ) ; [Dynamic Tables and Snowpipe Streaming, Mastering Snowflake](https://www.youtube.com/watch?v=o8YXmsy8Rss) | [18. Transformation](../18-transformation.md) | [quiz 18](quiz-18-transformation.md) |
| 14 | Partage de données, réplication | [Snowflake Data Sharing, Data Engineering Simplified](https://www.youtube.com/watch?v=2d6d-zZMXtA) | [19. Collaboration](../19-collaboration.md) | [quiz 19](quiz-19-collaboration.md) |
| 15 | Examen blanc en conditions réelles | aucune : 115 minutes sans documentation | [fiche de révision](FICHE_REVISION.md), après l'examen blanc | [examen blanc 1](examen-blanc-1.md), puis dépouillement par domaine |

## Les derniers jours

| Moment | Quoi faire |
|---|---|
| Après l'examen blanc | calculer son score par domaine avec le tableau de dépouillement ; revoir le chapitre du domaine le plus faible |
| Deux jours avant | s'entraîner sur des questions commentées : [COF-C03 Practice Test, Part 1, BuzzByte](https://www.youtube.com/watch?v=Gp_nX73suhk) et [Practice Questions with Explanations, Cert QuestionsBank](https://www.youtube.com/watch?v=l44WpBx5v50). Ces vidéos viennent de chaînes tierces : vérifier dans la documentation toute réponse qui surprend |
| La veille | relire la [fiche de révision](FICHE_REVISION.md) et son carnet d'erreurs ; ne rien apprendre de nouveau |
| Le jour même | 115 minutes pour 100 questions, soit un peu plus d'une minute par question : répondre d'abord aux questions sûres, marquer les autres et y revenir |

## Score visé avant de s'inscrire

L'examen se réussit à 750 sur 1000. Avant de payer l'inscription, visez **au moins 80 bonnes réponses sur 100** à l'examen blanc, et aucun domaine sous les deux tiers de bonnes réponses.

## En français

- [Stocker et visualiser des données dans Snowflake, Mind7 Consulting](https://www.youtube.com/watch?v=9vZr6NcSVls) : une présentation en français, utile en première semaine.
- Le cours de ce dépôt, ses quiz et son examen blanc sont en français, comme l'examen si vous choisissez cette langue à l'inscription.

## Si vous avez moins de temps

En deux semaines : fusionner les séances 1 et 2, 6 et 7, 9 et 10, 12 et 13. Ne jamais supprimer la séance 15 : l'examen blanc est l'entraînement le plus utile.
