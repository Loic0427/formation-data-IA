# 3. Création d'un rôle personnalisé

[← Retour au sommaire](README.md) | [← Précédent](02-connexion.md) | [Suivant →](04-creation-warehouse.md)

## Vue d'ensemble

Dans Snowflake, un droit ne se donne jamais directement à une personne : il se donne à un **rôle**, et le rôle se donne ensuite aux utilisateurs. C'est le contrôle d'accès par rôles (RBAC). Créer un rôle par usage permet de donner à chacun le strict nécessaire et de retirer un accès en une seule commande.

Ce chapitre présente les rôles fournis par Snowflake, puis crée le rôle `SALES_ANALYST`, qui servira à lire les données de ventes. Ses droits lui seront donnés au [chapitre 8](08-gestion-privileges.md), une fois les objets créés.

---

## 1. Les rôles système

Tout compte possède des rôles prédéfinis, organisés en hiérarchie : un rôle hérite de tous les droits des rôles placés sous lui.

```
ACCOUNTADMIN
├── SECURITYADMIN
│   └── USERADMIN
└── SYSADMIN
    └── rôles personnalisés (SALES_ANALYST...)

PUBLIC : donné automatiquement à tous les utilisateurs et à tous les rôles
```

| Rôle système | Sert à |
|---|---|
| `ACCOUNTADMIN` | tout administrer, y compris la facturation ; à utiliser le moins possible |
| `SECURITYADMIN` | gérer tous les droits du compte (privilège `MANAGE GRANTS`) |
| `USERADMIN` | créer des utilisateurs et des rôles |
| `SYSADMIN` | créer des warehouses, des bases et leurs objets |
| `PUBLIC` | droits communs à tous : ne rien y mettre de sensible |

`ORGADMIN`, visible dans la liste des rôles, sert à gérer l'organisation (l'ensemble des comptes) et non le contenu d'un compte. Pour les organisations à plusieurs comptes, la documentation annonce son abandon progressif au profit du rôle `GLOBALORGADMIN`, utilisé dans le compte d'organisation.

Sur votre compte d'essai, votre utilisateur possède `ACCOUNTADMIN` et peut donc prendre n'importe lequel de ces rôles. Dans ce cours, on prend l'habitude d'utiliser le rôle prévu pour chaque geste : `USERADMIN` pour créer un rôle, `SYSADMIN` pour créer des objets.

---

## 2. Créer le rôle dans Snowsight

1. Dans le menu, sélectionnez **Governance & security** » **Users & roles**, puis l'onglet **Roles**.
2. Sélectionnez **+ Role**. La fenêtre **New Role** s'ouvre.
3. **Name** : `SALES_ANALYST`. Ajoutez un commentaire : `Lecture des données de ventes`.
4. Validez la création.

![Navigation vers Users & roles](images/11-roles-navigation.png)
*Menu Governance & security, entrée Users & roles (interface en français sur la capture)*

![Page Users & roles, onglet Roles](images/12-role-creation-form.png)
*Onglet Roles : la vue graphique montre la hiérarchie, le bouton + Role crée un rôle*

Le rôle créé appartient au rôle actif au moment de la création. Vérifiez donc le rôle affiché dans le menu utilisateur avant de cliquer (**Switch role** pour en changer).

---

## 3. SQL équivalent

```sql
USE ROLE USERADMIN;

CREATE ROLE IF NOT EXISTS SALES_ANALYST
    COMMENT = 'Lecture des données de ventes';

-- Rattacher le rôle à la hiérarchie : SYSADMIN hérite de SALES_ANALYST
GRANT ROLE SALES_ANALYST TO ROLE SYSADMIN;

-- Vérifier
SHOW ROLES LIKE 'SALES%';
```

Le rattachement à `SYSADMIN` est une bonne pratique recommandée par Snowflake : sans lui, les objets que ce rôle créerait un jour échapperaient aux administrateurs.

À ce stade, le rôle existe mais ne peut rien faire : il n'a aucun privilège et n'est donné à aucun utilisateur.

---

## 4. Bonnes pratiques

1. Ne pas utiliser `ACCOUNTADMIN` pour le travail quotidien, et ne pas en faire le rôle par défaut d'un utilisateur.
2. Créer un rôle par usage (lecture, chargement, administration d'un domaine), pas un rôle par personne.
3. Donner à chaque rôle le minimum de droits nécessaires (principe du moindre privilège).
4. Rattacher chaque rôle personnalisé à `SYSADMIN`.
5. Renseigner le commentaire de chaque rôle.

---

## À retenir pour la certification

- Le contrôle d'accès de Snowflake combine le RBAC (les privilèges sont donnés à des rôles) et le DAC (chaque objet a un rôle propriétaire qui décide des accès).
- Hiérarchie des rôles système : `ACCOUNTADMIN` hérite de `SECURITYADMIN` et de `SYSADMIN` ; `SECURITYADMIN` hérite de `USERADMIN`.
- `USERADMIN` crée les utilisateurs et les rôles ; `SECURITYADMIN` possède `MANAGE GRANTS` ; `SYSADMIN` crée les warehouses et les bases.
- `PUBLIC` est donné automatiquement à tous les utilisateurs et à tous les rôles.
- Snowflake recommande de rattacher les rôles personnalisés à `SYSADMIN` et de ne pas utiliser `ACCOUNTADMIN` pour créer des objets.

## ✅ Points de vérification
- [ ] Rôle `SALES_ANALYST` créé avec un commentaire
- [ ] Rôle rattaché à `SYSADMIN`
- [ ] Rôle visible avec `SHOW ROLES LIKE 'SALES%'`

## Documentation officielle
- [Vue d'ensemble du contrôle d'accès](https://docs.snowflake.com/en/user-guide/security-access-control-overview)
- [Configurer le contrôle d'accès](https://docs.snowflake.com/en/user-guide/security-access-control-configure)
- [CREATE ROLE](https://docs.snowflake.com/en/sql-reference/sql/create-role)

---

[← Retour au sommaire](README.md) | [← Précédent](02-connexion.md) | [Suivant →](04-creation-warehouse.md)
