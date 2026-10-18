# Formation Apache Airflow 3

Deux façons de parcourir ce module, écrites toutes les deux pour **Airflow 3.3** :

- **Le cours par chapitres** (parties 01 à 06) : la référence, à lire dans l'ordre ou à consulter au besoin.
- **La semaine atelier « NYC Taxi dans Snowflake »** : cinq jours guidés, un pipeline complet construit de bout en bout, qui prépare le brief [NYC-Taxi-Orchestration, variante A](../../99-Brief/Data-Engineer/NYC-Taxi-Orchestration/VARIANTE_A_SNOWFLAKE_DBT_AIRFLOW.md).

## Objectifs pédagogiques

À l'issue de ce module, vous serez capable de :

- Comprendre l'architecture et les concepts fondamentaux d'Apache Airflow
- Créer et orchestrer des pipelines de données (DAGs) complexes
- Utiliser les opérateurs courants (Python, SQL, HTTP, fichiers)
- Maîtriser les mécanismes avancés : XCom, Variables, Connexions, branchement conditionnel, assets
- Écrire des DAGs dynamiques, idempotents et testables
- Charger des données dans un entrepôt (Snowflake) sans doublon et rattraper l'historique
- Déployer Airflow en production avec Docker ou Kubernetes

## Prérequis

- Python 3.10+ (fonctions, décorateurs, modules)
- Notions de base en SQL
- Docker et Docker Compose installés
- Connaissances basiques en ligne de commande Linux/macOS

---

## Parcours 1 : le cours par chapitres (~14 h)

```
Airflow/
├── 01-Fondamentaux/
│   ├── 01-introduction.md             ← Architecture, concepts clés, cas d'usage
│   ├── 02-installation.md             ← Docker Compose, configuration, exécuteurs
│   └── 03-premier-dag.md              ← Premiers pas avec les DAGs
├── 02-Operateurs/
│   ├── 01-operateurs-python.md        ← PythonOperator, TaskFlow API
│   ├── 02-operateurs-sql.md           ← SQLExecuteQueryOperator, PostgresHook
│   ├── 03-operateurs-fichiers.md      ← FileSensor, S3Operator
│   └── 04-operateurs-http.md          ← HttpOperator, HttpSensor
├── 03-Concepts-Avances/
│   ├── 01-xcom.md                     ← Passage de données entre tâches
│   ├── 02-variables-connections.md    ← Variables et connexions Airflow
│   ├── 03-branching.md                ← Workflows conditionnels
│   └── 04-dynamic-dags.md             ← DAGs et tâches dynamiques
├── 04-Bonnes-Pratiques/
│   ├── 01-idempotence.md              ← Idempotence, catchup, re-exécution
│   └── 02-tests-dags.md               ← Tests unitaires et validation
├── 05-Deploiement/
│   └── 01-production.md               ← Kubernetes, CI/CD, supervision
├── 06-Airflow3-Astro/
│   └── 01-airflow3-astro-snowflake.md ← Astro CLI, Snowflake, dbt (Cosmos), notifications
└── exercices/
    ├── exercice-01-pipeline-etl.md    ← Pipeline ETL complet
    └── exercice-02-pipeline-ml.md     ← Pipeline ML avec MLflow
```

| Module | Durée |
|---|---|
| Fondamentaux | 3h |
| Opérateurs | 2h30 |
| Concepts avancés | 3h |
| Bonnes pratiques | 1h30 |
| Déploiement | 1h30 |
| Exercices pratiques | 3h |
| **Total** | **~14h** |

---

## Parcours 2 : la semaine atelier « NYC Taxi dans Snowflake » (5 jours, 35 h)

> **Une semaine, un pipeline.** Chaque mois, la commission des taxis de New York (TLC) publie les
> courses du mois écoulé, avec un à trois mois de retard, à une date que personne ne connaît à
> l'avance. Vous construisez le pipeline qui attend ce fichier, le charge dans Snowflake sans
> jamais créer de doublon, rattrape l'historique, calcule des indicateurs et vous prévient quand
> quelque chose casse.

| | |
|---|---|
| **Entrepôt** | Snowflake, compte d'essai gratuit (30 jours) |
| **Données** | [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page), taxis jaunes, Parquet mensuel, ~3,5 millions de courses par mois |
| **Stack** | Docker Compose, image officielle `apache/airflow:3.3.2` |

### Pourquoi un orchestrateur ?

Un script lancé par `cron` chaque nuit fonctionne jusqu'au jour où il échoue. Ce jour-là, personne ne le sait (pas d'interface, pas d'alerte, pas d'historique), on ne sait plus quoi relancer (quels mois sont chargés ?), et les étapes suivantes tournent quand même sur des données incomplètes. Airflow **montre** chaque exécution, **rejoue** précisément ce qui manque et **enchaîne** les étapes selon leurs dépendances.

### La semaine

| Jour | Cours | Ce que vous construisez |
|---|---|---|
| **Lundi** | [01 — Architecture et premier DAG](01-lundi-architecture-premier-dag.md) | la stack Docker, ses cinq services, votre premier DAG |
| **Mardi** | [02 — Le temps : planification et ingestion](02-mardi-planification-ingestion.md) | un DAG mensuel qui télécharge le bon mois, rejouable, rattrapable |
| **Mercredi** | [03 — Snowflake : connexion, chargement, parallélisme](03-mercredi-snowflake-connexions-parallelisme.md) | le chargement idempotent dans Snowflake, le rattrapage en parallèle |
| **Jeudi** | [04 — Capteurs différés, assets et branchement](04-jeudi-capteurs-assets-branchement.md) | un pipeline qui attend la donnée au lieu de l'horloge |
| **Vendredi** | [05 — Fiabilité, tests et mini-brief](05-vendredi-fiabilite-tests.md) | rappels d'échec, tests automatisés, puis un mini-brief en autonomie |

À garder ouverts toute la semaine : le [mémo des commandes](memo-commandes.md), la fiche [dépannage](depannage.md) (« mon DAG n'apparaît pas », « ma tâche ne démarre pas ») et les [vidéos récentes sur Airflow 3 et Snowflake](videos.md).

### L'atelier

Tout le code de la semaine vit dans [`atelier/`](atelier/) :

```
atelier/
├── docker-compose.yaml     la stack (dérivée du fichier officiel, commentée service par service)
├── Dockerfile              l'image Airflow étendue
├── .env.example            à copier en .env
├── dags/                   vos DAG (un DAG d'exemple fourni : bonjour_airflow.py)
├── exercices/              le point de départ de chaque journée (mardi à vendredi)
├── plugins/tlc/            code partagé : capteur différé fourni, le reste à écrire
├── tests/                  vos tests de DAG
├── snowflake/              scripts d'installation et de destruction côté Snowflake
├── secrets/                votre clé privée Snowflake (jamais commitée)
└── data/                   fichiers téléchargés (jamais commités)
```

### Compétences travaillées

| Compétence | Où |
|---|---|
| Automatiser l'extraction de données depuis une source externe | lundi, mardi |
| Intégrer des données dans un entrepôt de données (Snowflake) | mercredi |
| Orchestrer un pipeline : dépendances, planification, reprise | toute la semaine |
| Sécuriser les accès (secrets hors du code, moindre privilège) | mercredi |
| Surveiller et fiabiliser un pipeline (alertes, tests) | vendredi |

---

## Versions utilisées

Tout le module est écrit pour Airflow 3.3. Les chapitres signalent au fil de l'eau ce qui a changé depuis Airflow 2.

| Outil | Version |
|---|---|
| Apache Airflow | 3.3.x (dernière version stable : 3.3.2) |
| Python | 3.12 |
| PostgreSQL | 16 |
| Docker | 27+ |
| Docker Compose | 2.14+ |

### Airflow 2 → Airflow 3 : ce qui vous piégera dans les tutoriels en ligne

| Airflow 2 | Airflow 3 |
|---|---|
| `airflow webserver` | `airflow api-server` (l'interface et l'API REST v2) |
| le scheduler lit les fichiers de DAG | un service séparé, le **dag-processor**, les lit |
| `from airflow.decorators import dag, task` | `from airflow.sdk import dag, task` |
| `Dataset` | `Asset` |
| `schedule="@monthly"` crée un intervalle de données | `schedule="@monthly"` **ne crée plus d'intervalle** : utiliser `CronDataIntervalTimetable` si besoin (mardi) |
| un déclenchement manuel a une date logique | un déclenchement manuel n'a **pas** de date logique |
| les tâches peuvent lire la base de métadonnées | interdit : elles passent par l'API d'exécution |
| `from airflow.models import DagBag` | `from airflow.dag_processing.dagbag import DagBag` |

---

## Ressources complémentaires

- [Documentation officielle Airflow 3](https://airflow.apache.org/docs/apache-airflow/stable/)
- [Notes de migration vers Airflow 3](https://airflow.apache.org/docs/apache-airflow/stable/installation/upgrading_to_airflow3.html)
- [Provider Snowflake](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/)
- [Snowflake, `COPY INTO`](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table)
- [Astronomer Registry (providers)](https://registry.astronomer.io/)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
