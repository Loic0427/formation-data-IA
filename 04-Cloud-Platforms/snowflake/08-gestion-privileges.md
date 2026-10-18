# 8. Gestion des privilèges

[← Retour au sommaire](README.md) | [← Précédent](07-import-donnees.md) | [Suivant →](09-monitoring.md)

## Vue d'ensemble

Le rôle `SALES_ANALYST` créé au [chapitre 3](03-creation-role.md) ne peut encore rien faire. Un **privilège** est le droit de faire une action sur un objet (`SELECT` sur une table, `USAGE` sur un warehouse) ; il se donne à un rôle avec `GRANT` et se retire avec `REVOKE`.

Les objets étant emboîtés, il faut un droit à chaque étage. Pour lire une table, un rôle a besoin de **quatre** privilèges : `USAGE` sur un warehouse, `USAGE` sur la base, `USAGE` sur le schéma, `SELECT` sur la table. S'il en manque un seul, Snowflake répond que l'objet n'existe pas ou n'est pas autorisé.

Ce chapitre donne ces quatre droits à `SALES_ANALYST`, donne le rôle à votre utilisateur, puis vérifie le résultat en prenant le rôle.

---

## 1. Donner les privilèges dans Snowsight

Prenez le rôle `SYSADMIN`, propriétaire du warehouse, de la base et des tables : le propriétaire d'un objet peut donner des droits dessus.

### Étape 1 : le warehouse

1. Dans le menu, sélectionnez **Compute** » **Warehouses**, puis ouvrez `SALES_WH`.
2. Dans la section **Privileges**, sélectionnez **+ Privilege**.
3. Choisissez le rôle `SALES_ANALYST` et le privilège `USAGE`, puis validez.

### Étape 2 : la base, le schéma et les tables

1. Dans le menu, sélectionnez **Catalog** » **Explorer** et ouvrez `SALES_DB`.
2. Dans la section **Privileges** de la page, sélectionnez **+ Privilege**, puis le rôle `SALES_ANALYST` et le privilège `USAGE`.
3. Ouvrez le schéma `RAW_DATA` et faites de même : `USAGE` pour `SALES_ANALYST`.
4. Ouvrez chacune des quatre tables (`CUSTOMERS`, `PRODUCTS`, `ORDERS`, `ORDER_ITEMS`) et donnez le privilège `SELECT` à `SALES_ANALYST`.

### Étape 3 : donner le rôle à un utilisateur

1. Dans le menu, sélectionnez **Governance & security** » **Users & roles**, onglet **Roles**.
2. Passez en vue **Table** et ouvrez le rôle `SALES_ANALYST`.
3. Dans la section qui liste les utilisateurs ayant reçu le rôle, sélectionnez **Grant to User** et choisissez votre utilisateur.

L'interface demande un geste par objet : quatre tables, quatre fois la même manipulation. C'est la raison pour laquelle les droits se gèrent en pratique par script SQL.

---

## 2. SQL équivalent

```sql
USE ROLE SYSADMIN;

-- Calcul
GRANT USAGE ON WAREHOUSE SALES_WH TO ROLE SALES_ANALYST;

-- Chaîne d'accès : base, puis schéma
GRANT USAGE ON DATABASE SALES_DB TO ROLE SALES_ANALYST;
GRANT USAGE ON SCHEMA SALES_DB.RAW_DATA TO ROLE SALES_ANALYST;

-- Lecture des tables qui existent aujourd'hui
GRANT SELECT ON ALL TABLES IN SCHEMA SALES_DB.RAW_DATA TO ROLE SALES_ANALYST;

-- Donner le rôle à un utilisateur (remplacer par votre nom d'utilisateur)
USE ROLE SECURITYADMIN;
GRANT ROLE SALES_ANALYST TO USER <votre_utilisateur>;
```

`ON ALL TABLES` remplace les quatre `GRANT SELECT ON TABLE ...` : il s'applique à toutes les tables présentes dans le schéma au moment où il est exécuté.

---

## 3. Vérifier en prenant le rôle

La seule preuve est d'essayer, y compris ce qui doit être refusé.

```sql
USE ROLE SALES_ANALYST;
USE WAREHOUSE SALES_WH;

SELECT COUNT(*) FROM SALES_DB.RAW_DATA.CUSTOMERS;                  -- doit réussir
DELETE FROM SALES_DB.RAW_DATA.CUSTOMERS WHERE CUSTOMER_ID = 1;     -- doit échouer : pas de DELETE
CREATE TABLE SALES_DB.RAW_DATA.TEST (id INT);                      -- doit échouer : pas de CREATE TABLE
```

Pour lire ce qui a été donné :

```sql
SHOW GRANTS TO ROLE SALES_ANALYST;                      -- les privilèges du rôle
SHOW GRANTS OF ROLE SALES_ANALYST;                      -- à qui le rôle est donné
SHOW GRANTS TO USER <votre_utilisateur>;                -- les rôles de l'utilisateur
SHOW GRANTS ON TABLE SALES_DB.RAW_DATA.CUSTOMERS;       -- qui a quel droit sur la table
```

---

## 4. Les privilèges par type d'objet

| Objet | Privilèges courants |
|---|---|
| Warehouse | `USAGE`, `OPERATE`, `MODIFY`, `MONITOR` |
| Base | `USAGE`, `CREATE SCHEMA`, `MONITOR`, `MODIFY` |
| Schéma | `USAGE`, `CREATE TABLE`, `CREATE VIEW`, `CREATE STAGE`, `MODIFY` |
| Table | `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`, `REFERENCES` |
| Vue | `SELECT`, `REFERENCES` |
| Tous | `OWNERSHIP` : détenu par un seul rôle, celui qui a créé l'objet |

Exemple de répartition entre trois rôles d'un même domaine :

| Action | SALES_ANALYST | SALES_DEVELOPER | SALES_ADMIN |
|---|---|---|---|
| Lire les données | oui | oui | oui |
| Modifier les données | non | oui | oui |
| Créer des tables | non | oui | oui |
| Gérer les droits du domaine | non | non | oui |

## 5. Hiérarchie des rôles

```
ACCOUNTADMIN
    ├── SECURITYADMIN
    │       └── USERADMIN
    └── SYSADMIN
            └── SALES_ADMIN (custom)
                    ├── SALES_DEVELOPER (custom)
                    └── SALES_ANALYST (custom)
```

Un rôle hérite des privilèges des rôles qui lui sont donnés : ici, `SALES_ADMIN` peut tout ce que peuvent `SALES_DEVELOPER` et `SALES_ANALYST`, et `SYSADMIN` peut tout ce que peut `SALES_ADMIN`.

Le modèle complet (propriété des objets, rôles système, droits futurs, utilisateurs de service, diagnostic des erreurs) est détaillé en SQL au [chapitre 10](10-securite.md).

---

## 6. Les droits futurs

`ON ALL TABLES` ne couvre que les tables existantes. Pour que le rôle lise aussi les tables créées plus tard, on ajoute un droit futur :

```sql
USE ROLE SECURITYADMIN;

GRANT SELECT ON FUTURE TABLES IN SCHEMA SALES_DB.RAW_DATA TO ROLE SALES_ANALYST;

SHOW FUTURE GRANTS IN SCHEMA SALES_DB.RAW_DATA;
```

Donner un droit futur sur un schéma demande d'être propriétaire du schéma ou de posséder le privilège global `MANAGE GRANTS`, que détient `SECURITYADMIN`.

---

## 7. Créer un utilisateur

1. Dans le menu, sélectionnez **Governance & security** » **Users & roles**, puis **+ User**.
2. Renseignez **User Name**, éventuellement **Email**, puis **Password** et **Confirm Password**.
3. Laissez cochée la case **Force user to change password on first time login**.
4. Dans **Advanced User Options**, précisez le rôle et le warehouse par défaut.
5. Sélectionnez **Create User**.

Le rôle par défaut choisi dans le formulaire n'est pas donné à l'utilisateur : il faut le lui donner ensuite, sinon sa connexion échoue.

```sql
USE ROLE USERADMIN;

CREATE USER IF NOT EXISTS ALICE
    PASSWORD = '<mot de passe provisoire>'
    MUST_CHANGE_PASSWORD = TRUE
    DEFAULT_ROLE = SALES_ANALYST
    DEFAULT_WAREHOUSE = SALES_WH
    COMMENT = 'Analyste des ventes';

GRANT ROLE SALES_ANALYST TO USER ALICE;
```

---

## 8. Aller plus loin : droits sur les lignes et les colonnes

Les privilèges s'arrêtent à la table : un rôle lit toute la table ou rien. Deux mécanismes, disponibles à partir de l'édition Enterprise, affinent l'accès :

| Mécanisme | Effet |
|---|---|
| Politique d'accès aux lignes (row access policy) | un rôle ne voit que certaines lignes d'une table |
| Politique de masquage (masking policy) | une colonne sensible est masquée pour certains rôles |

Ils sont traités au [chapitre 15](15-gouvernance.md).

---

## 9. Bonnes pratiques

### ✅ À faire
1. Donner les privilèges aux rôles, et les rôles aux utilisateurs.
2. Ne donner que les droits nécessaires (principe du moindre privilège).
3. Écrire les `GRANT` dans un script versionné plutôt que de cliquer.
4. Tester chaque rôle, y compris ce qui doit être refusé.
5. Revoir régulièrement les droits et retirer ceux qui ne servent plus.

### ❌ À éviter
1. Travailler au quotidien avec `ACCOUNTADMIN`.
2. Donner des privilèges au rôle `PUBLIC`.
3. Partager un compte utilisateur entre plusieurs personnes.
4. Donner `ALL PRIVILEGES` par facilité.

---

## 10. Avant de passer au chapitre 10

Le [chapitre 10](10-securite.md) réorganise les droits : `SALES_ANALYST` n'y lit plus que le schéma `ANALYTICS`, et l'un de ses tests vérifie que la lecture de `RAW_DATA` lui est refusée. Retirez donc les droits donnés ici sur `RAW_DATA` avant de le commencer :

```sql
USE ROLE SECURITYADMIN;

REVOKE SELECT ON ALL TABLES IN SCHEMA SALES_DB.RAW_DATA FROM ROLE SALES_ANALYST;
REVOKE SELECT ON FUTURE TABLES IN SCHEMA SALES_DB.RAW_DATA FROM ROLE SALES_ANALYST;
REVOKE USAGE ON SCHEMA SALES_DB.RAW_DATA FROM ROLE SALES_ANALYST;
```

---

## À retenir pour la certification

- Lire une table demande `USAGE` sur un warehouse, `USAGE` sur la base, `USAGE` sur le schéma et `SELECT` sur la table.
- Les privilèges se donnent à des rôles ; les rôles se donnent à des utilisateurs ou à d'autres rôles, qui en héritent.
- `OWNERSHIP` est détenu par un seul rôle ; par défaut, celui qui a créé l'objet.
- `GRANT ... ON ALL TABLES` couvre les tables existantes ; `GRANT ... ON FUTURE TABLES` couvre celles qui seront créées.
- `MANAGE GRANTS` (détenu par `SECURITYADMIN`) permet de donner ou retirer n'importe quel privilège du compte.
- `DEFAULT_ROLE` ne donne pas le rôle : il faut aussi un `GRANT ROLE ... TO USER`.

## ✅ Points de vérification
- [ ] `USAGE` donné sur le warehouse, la base et le schéma
- [ ] `SELECT` donné sur les quatre tables
- [ ] Rôle donné à votre utilisateur
- [ ] Lecture réussie et écriture refusée avec le rôle `SALES_ANALYST`
- [ ] Droits sur `RAW_DATA` retirés avant le chapitre 10

## Documentation officielle
- [Configurer le contrôle d'accès](https://docs.snowflake.com/en/user-guide/security-access-control-configure)
- [Liste des privilèges par objet](https://docs.snowflake.com/en/user-guide/security-access-control-privileges)
- [Gestion des utilisateurs](https://docs.snowflake.com/en/user-guide/admin-user-management)
- [GRANT privilèges](https://docs.snowflake.com/en/sql-reference/sql/grant-privilege)

---

[← Retour au sommaire](README.md) | [← Précédent](07-import-donnees.md) | [Suivant →](09-monitoring.md)
