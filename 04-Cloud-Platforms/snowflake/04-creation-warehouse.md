# 4. Création d'un warehouse

[← Retour au sommaire](README.md) | [← Précédent](03-creation-role.md) | [Suivant →](05-creation-database-schema.md)

## Vue d'ensemble

Dans Snowflake, le stockage et le calcul sont séparés. Les données sont stockées une fois ; la puissance de calcul est fournie par des **warehouses virtuels**, des groupes de serveurs que l'on démarre, arrête et redimensionne à la demande. Attention au vocabulaire : un warehouse Snowflake ne contient aucune donnée, c'est uniquement du calcul.

Un warehouse consomme des **crédits** tant qu'il tourne, qu'il exécute des requêtes ou non. Le régler correctement (petite taille, suspension automatique) est donc le premier geste de maîtrise des coûts. Ce chapitre crée `SALES_WH`, le warehouse de l'exemple suivi.

---

## 1. Créer le warehouse dans Snowsight

Prenez le rôle `SYSADMIN` (menu utilisateur, **Switch role**) : c'est lui qui possède le privilège `CREATE WAREHOUSE`.

1. Dans le menu, sélectionnez **Compute** » **Warehouses**. Le compte d'essai contient déjà `COMPUTE_WH`.
2. Sélectionnez **+ Warehouse**. La fenêtre **New Warehouse** s'ouvre.
3. Renseignez :
   - le nom : `SALES_WH` ;
   - un commentaire : `Calcul pour les données de ventes` ;
   - **Size** : `X-Small`. Vérifiez toujours ce champ : la taille proposée par défaut par le formulaire peut être bien plus grande.
4. Ouvrez **Advanced Options** et réglez la suspension automatique (auto-suspend) sur 1 minute, en laissant la reprise automatique (auto-resume) activée.
5. Sélectionnez **Create Warehouse**.

![Page Warehouses](images/13-warehouses-page.png)
*Page Compute » Warehouses*

![Fenêtre New Warehouse](images/14-warehouse-creation-form.png)
*Fenêtre New Warehouse : nom, taille et options avancées*

![Warehouse créé](images/15-warehouse-created.png)
*Le warehouse apparaît dans la liste avec son état*

---

## 2. SQL équivalent

```sql
USE ROLE SYSADMIN;

CREATE WAREHOUSE IF NOT EXISTS SALES_WH
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60              -- secondes d'inactivité avant suspension
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE     -- ne démarre qu'à la première requête
    COMMENT = 'Calcul pour les données de ventes';

SHOW WAREHOUSES LIKE 'SALES_WH';
```

Valeurs par défaut de `CREATE WAREHOUSE` quand on ne précise rien :

| Paramètre | Valeur par défaut |
|---|---|
| `WAREHOUSE_SIZE` | `XSMALL` |
| `AUTO_SUSPEND` | `600` secondes (10 minutes) |
| `AUTO_RESUME` | `TRUE` |
| `INITIALLY_SUSPENDED` | `FALSE` : le warehouse démarre, donc consomme, dès sa création |
| `MIN_CLUSTER_COUNT` / `MAX_CLUSTER_COUNT` | `1` / `1` (un seul cluster) |

Les commandes utiles ensuite :

```sql
ALTER WAREHOUSE SALES_WH SUSPEND;                          -- arrêter
ALTER WAREHOUSE SALES_WH RESUME;                           -- démarrer
ALTER WAREHOUSE SALES_WH SET WAREHOUSE_SIZE = 'SMALL';     -- redimensionner
ALTER WAREHOUSE SALES_WH SET WAREHOUSE_SIZE = 'XSMALL';
```

---

## 3. Tailles et consommation

Chaque taille double la puissance et la consommation de la précédente (warehouses standard de première génération) :

| Taille | Crédits par heure |
|---|---|
| X-Small | 1 |
| Small | 2 |
| Medium | 4 |
| Large | 8 |
| X-Large | 16 |
| 2X-Large | 32 |
| 3X-Large | 64 |
| 4X-Large | 128 |
| 5X-Large | 256 |
| 6X-Large | 512 |

La facturation se fait **à la seconde, avec un minimum de 60 secondes à chaque démarrage**. Un warehouse X-Small qui tourne 10 minutes consomme 1/6 de crédit ; s'il démarre pour une requête de 5 secondes, il est facturé 60 secondes.

Le prix d'un crédit dépend de l'édition, du fournisseur cloud et de la région.

---

## 4. Les réglages qui comptent

### Suspension et reprise automatiques

- `AUTO_SUSPEND` : après ce délai sans activité, le warehouse s'arrête et ne consomme plus.
- `AUTO_RESUME` : le warehouse redémarre tout seul dès qu'une requête lui est envoyée.

Avec ces deux réglages, il n'y a rien à planifier : le warehouse ne tourne que lorsqu'on s'en sert. Un délai très court a une contrepartie : à chaque suspension, le cache local du warehouse est vidé, et les premières requêtes suivantes sont plus lentes.

### Agrandir ou multiplier

| Besoin | Réponse | Nom |
|---|---|---|
| Des requêtes trop lentes parce que trop lourdes | augmenter la taille du warehouse | scale up |
| Trop de requêtes en même temps, qui font la queue | ajouter des clusters de même taille | scale out (multi-cluster) |

Un warehouse **multi-cluster** (`MAX_CLUSTER_COUNT` supérieur à 1) ajoute et retire des clusters selon la charge. Il demande l'édition Enterprise ou supérieure. Sa politique d'ajustement (`SCALING_POLICY`) vaut `STANDARD` ou `ECONOMY`. Le [chapitre 17](17-performance.md) y revient.

### Conseils

1. Commencer en X-Small et n'augmenter la taille que si une mesure le justifie.
2. Garder la suspension automatique courte sur les warehouses de développement.
3. Séparer les usages : un warehouse pour le chargement, un autre pour l'analyse, afin qu'ils ne se gênent pas et que les coûts soient lisibles.
4. Poser une limite de consommation avec un resource monitor ([chapitre 9](09-monitoring.md)).

---

## À retenir pour la certification

- Un warehouse fournit le calcul ; il ne stocke pas de données. Stockage et calcul sont facturés séparément.
- Facturation à la seconde, avec un minimum de 60 secondes à chaque démarrage.
- La consommation double à chaque taille : X-Small = 1 crédit par heure, Small = 2, Medium = 4, Large = 8, jusqu'à 6X-Large = 512.
- `CREATE WAREHOUSE` sans option crée un warehouse `XSMALL`, avec `AUTO_SUSPEND = 600` secondes et `AUTO_RESUME = TRUE`.
- Scale up (taille) pour des requêtes complexes ; scale out (multi-cluster) pour la concurrence. Le multi-cluster exige l'édition Enterprise.
- Politiques d'ajustement d'un multi-cluster : `STANDARD` (par défaut) et `ECONOMY`.

## ✅ Points de vérification
- [ ] Warehouse `SALES_WH` créé avec le rôle `SYSADMIN`
- [ ] Taille X-Small
- [ ] Suspension automatique à 60 secondes, reprise automatique activée

## Documentation officielle
- [Vue d'ensemble des warehouses](https://docs.snowflake.com/en/user-guide/warehouses-overview)
- [Utiliser les warehouses](https://docs.snowflake.com/en/user-guide/warehouses-tasks)
- [CREATE WAREHOUSE](https://docs.snowflake.com/en/sql-reference/sql/create-warehouse)

---

[← Retour au sommaire](README.md) | [← Précédent](03-creation-role.md) | [Suivant →](05-creation-database-schema.md)
