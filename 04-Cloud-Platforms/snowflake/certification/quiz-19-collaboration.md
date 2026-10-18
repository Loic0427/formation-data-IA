# Quiz 19. Collaboration autour des données

[← Chapitre 19](../19-collaboration.md) | [Plan de préparation](PLAN.md) | [Fiche de révision](FICHE_REVISION.md)

Domaine 5 de l'examen SnowPro Core (COF-C03), « Data Collaboration », 10 % des questions.

Consignes : 20 questions, 25 minutes, sans documentation. Chaque question précise le nombre de réponses attendues ; une question à plusieurs réponses n'est juste que si toutes les bonnes réponses sont cochées, et elles seules. Le corrigé est à la fin du fichier. Objectif : 15 bonnes réponses sur 20.

---

## Questions

**Question 1.** Un fournisseur partage une table de 500 Go avec un compte consommateur par un partage direct. Qui paie le stockage de ces données ? (1 réponse)

- A. Le consommateur, pour la totalité
- B. Le fournisseur et le consommateur, pour moitié chacun
- C. Le fournisseur uniquement
- D. Personne : les données partagées ne sont pas facturées

**Question 2.** Quelles affirmations décrivent correctement le partage sécurisé de données (Secure Data Sharing) ? (2 réponses)

- A. Les données sont copiées dans le compte du consommateur à chaque rafraîchissement
- B. Le consommateur lit les données du fournisseur sans qu'aucune copie soit créée
- C. Le consommateur peut modifier les lignes des tables partagées
- D. Le consommateur paie le calcul utilisé pour interroger les données partagées
- E. Le partage exige que le consommateur utilise le même warehouse que le fournisseur

**Question 3.** Quel objet Snowflake contient les privilèges donnés sur les objets partagés et la liste des comptes autorisés ? (1 réponse)

- A. `SHARE`
- B. `STAGE`
- C. `REPLICATION GROUP`
- D. `MANAGED ACCOUNT`

**Question 4.** Un partenaire n'est pas client de Snowflake. Le fournisseur veut tout de même lui donner accès à des données partagées. Que doit-il créer ? (1 réponse)

- A. Un groupe de bascule
- B. Un clone de la base dans un schéma dédié
- C. Un utilisateur de type `SERVICE` dans son propre compte
- D. Un compte lecteur (reader account)

**Question 5.** Qui paie les crédits consommés par les warehouses d'un compte lecteur ? (1 réponse)

- A. Le partenaire qui utilise le compte lecteur
- B. Le fournisseur qui a créé le compte lecteur
- C. Snowflake, tant que le compte reste sous un seuil gratuit
- D. Personne : un compte lecteur n'a pas de warehouse

**Question 6.** Quelle commande crée un compte lecteur ? (1 réponse)

- A. `CREATE ACCOUNT ... EDITION = READER`
- B. `CREATE USER ... TYPE = READER`
- C. `CREATE MANAGED ACCOUNT ... TYPE = READER`
- D. `CREATE SHARE ... WITH READER`

**Question 7.** Dans le compte consommateur, quel privilège donne-t-on à un rôle pour qu'il puisse interroger une base créée à partir d'un partage ? (1 réponse)

- A. `SELECT ON ALL TABLES IN DATABASE`
- B. `OWNERSHIP ON DATABASE`
- C. `IMPORT SHARE ON DATABASE`
- D. `IMPORTED PRIVILEGES ON DATABASE`

**Question 8.** Un consommateur a créé la base `PARTNER_SALES` à partir d'un partage. Quelles actions lui sont impossibles sur cette base ? (3 réponses)

- A. Cloner une table de la base
- B. Joindre une table de la base avec une de ses propres tables
- C. Utiliser Time Travel sur une table de la base
- D. Insérer des lignes dans une table de la base
- E. Interroger une vue de la base avec son propre warehouse

**Question 9.** Pourquoi partage-t-on une vue sécurisée plutôt qu'une vue ordinaire ? (2 réponses)

- A. Parce qu'une vue sécurisée s'exécute plus vite
- B. Parce que sa définition est cachée aux utilisateurs qui n'ont pas le rôle propriétaire
- C. Parce qu'elle stocke son résultat, ce qui évite de recalculer
- D. Parce que certaines optimisations pouvant révéler des données filtrées sont désactivées
- E. Parce qu'elle est la seule à accepter une clause `WHERE`

**Question 10.** Un fournisseur veut qu'une même vue sécurisée montre à chaque compte consommateur uniquement ses propres lignes. Quelle fonction de contexte utilise-t-il dans la vue, avec une table de correspondance ? (1 réponse)

- A. `CURRENT_ACCOUNT()`
- B. `CURRENT_USER()`
- C. `CURRENT_ROLE()`
- D. `CURRENT_WAREHOUSE()`

**Question 11.** Un fournisseur ajoute une nouvelle table dans un schéma dont plusieurs tables sont déjà partagées. Que se passe-t-il pour les consommateurs ? (1 réponse)

- A. La table est visible immédiatement, sans autre action
- B. La table est visible après le prochain rafraîchissement du partage
- C. La table n'est visible qu'après un `GRANT SELECT ... TO SHARE` sur cette table
- D. La table n'est visible qu'après la recréation de la base chez chaque consommateur

**Question 12.** Un fournisseur dont le compte est en Europe sur AWS doit servir un consommateur dont le compte est aux États-Unis sur Azure. Quelles solutions conviennent ? (2 réponses)

- A. Un partage direct, en ajoutant le compte distant avec `ALTER SHARE ... ADD ACCOUNTS`
- B. Une annonce (listing) avec Cross-Cloud Auto-Fulfillment
- C. Un clone de la base créé directement dans le compte distant
- D. La réplication de la base vers un compte du fournisseur situé dans la région du consommateur, puis un partage direct depuis ce compte
- E. Un compte lecteur créé dans la région du consommateur

**Question 13.** Qu'est-ce qu'une annonce (listing) ? (1 réponse)

- A. Une copie d'une base tenue à jour dans une autre région
- B. Un partage ou une application accompagné de métadonnées, proposé à des comptes désignés ou publié sur le Marketplace
- C. Un rapport d'audit des accès aux données partagées
- D. La liste des fichiers présents sur un stage

**Question 14.** Un groupe industriel veut un espace privé où ses filiales et quelques fournisseurs invités publient et consomment des jeux de données, sans que rien n'apparaisse publiquement. Quelle fonctionnalité répond à ce besoin par définition ? (1 réponse)

- A. Un compte lecteur
- B. Snowflake Marketplace
- C. Un groupe de réplication
- D. Un Data Exchange

**Question 15.** Deux entreprises veulent mesurer le recouvrement de leurs fichiers clients sans qu'aucune ne voie les lignes de l'autre. Quelle solution est conçue pour ce cas ? (1 réponse)

- A. Une salle blanche (data clean room)
- B. Un partage direct de chaque table client
- C. Un clone croisé des deux bases
- D. Un groupe de bascule commun

**Question 16.** Quelles affirmations sur les éditions sont exactes ? (2 réponses)

- A. La réplication d'une base de données est disponible dans toutes les éditions
- B. La réplication d'une base de données exige l'édition Business Critical
- C. La bascule (failover) exige l'édition Business Critical ou supérieure
- D. La bascule est disponible dès l'édition Standard
- E. Le partage sécurisé de données exige l'édition Enterprise

**Question 17.** Quelle est la différence entre un groupe de réplication et un groupe de bascule ? (1 réponse)

- A. Le groupe de réplication ne peut contenir qu'une seule base
- B. Le groupe de bascule fonctionne uniquement dans la même région
- C. Le groupe de bascule peut être promu en primaire, ce qui rend ses objets modifiables dans le compte cible
- D. Le groupe de réplication donne un accès en écriture dans le compte cible

**Question 18.** La région du compte de production est indisponible. Dans quel compte, et avec quelle commande, fait-on du compte de secours le nouveau primaire ? (1 réponse)

- A. Dans le compte source : `ALTER FAILOVER GROUP ... REFRESH`
- B. Dans le compte cible : `ALTER FAILOVER GROUP ... PRIMARY`
- C. Dans le compte source : `ALTER FAILOVER GROUP ... PRIMARY`
- D. Dans le compte cible : `CREATE DATABASE ... FROM SHARE`

**Question 19.** À quoi sert Client Redirect ? (1 réponse)

- A. À répliquer les utilisateurs et les rôles vers le compte de secours
- B. À chiffrer les connexions entre deux comptes
- C. À rafraîchir automatiquement une base secondaire
- D. À fournir une adresse de connexion stable, redirigée vers le compte de secours lors d'une bascule

**Question 20.** Un compte fournisseur en édition Business Critical tente d'ajouter à un partage un compte consommateur en édition Standard. Que se passe-t-il ? (1 réponse)

- A. L'ajout réussit toujours : l'édition du consommateur n'a aucune importance
- B. L'ajout est impossible dans tous les cas
- C. L'ajout est bloqué par défaut ; il devient possible avec le privilège `OVERRIDE SHARE RESTRICTIONS` et `SHARE_RESTRICTIONS = FALSE`
- D. L'ajout réussit, mais le consommateur doit payer le stockage

---

## Corrigé

| Question | Réponse | Question | Réponse |
|---|---|---|---|
| 1 | C | 11 | C |
| 2 | B, D | 12 | B, D |
| 3 | A | 13 | B |
| 4 | D | 14 | D |
| 5 | B | 15 | A |
| 6 | C | 16 | A, C |
| 7 | D | 17 | C |
| 8 | A, C, D | 18 | B |
| 9 | B, D | 19 | D |
| 10 | A | 20 | C |

**1. C.** Les données partagées n'occupent aucun stockage dans le compte du consommateur : le stockage reste à la charge du fournisseur.

**2. B, D.** Le partage donne un accès en lecture seule aux données du fournisseur, sans copie ; le consommateur paie le warehouse qu'il utilise pour les interroger.

**3. A.** Le `SHARE` est l'objet nommé qui regroupe les privilèges sur les objets partagés et les comptes destinataires.

**4. D.** Le compte lecteur permet de partager avec un tiers qui n'a pas de compte Snowflake ; il est créé et géré par le fournisseur.

**5. B.** Le compte lecteur appartient au fournisseur : tous les crédits consommés par ses warehouses sont facturés au compte fournisseur.

**6. C.** Un compte lecteur est un compte géré, créé par `CREATE MANAGED ACCOUNT ... TYPE = READER`.

**7. D.** Sur une base importée, on ne donne pas les privilèges objet par objet : le seul privilège disponible est `IMPORTED PRIVILEGES`.

**8. A, C, D.** Une base importée est en lecture seule, sans clonage et sans Time Travel ; la lire et la joindre à ses propres tables reste possible.

**9. B, D.** Une vue sécurisée cache sa définition et désactive les optimisations qui pourraient exposer des données ; elle peut en contrepartie être plus lente.

**10. A.** Les utilisateurs et les rôles appartiennent au consommateur et sont inconnus du fournisseur : le filtrage se fait sur le compte, avec `CURRENT_ACCOUNT()`.

**11. C.** Un objet n'entre dans un partage que par un `GRANT ... TO SHARE` explicite ; une fois le droit donné, il est visible immédiatement, sans rafraîchissement.

**12. B, D.** Le partage direct est limité à la même région ; il faut soit une annonce avec auto-fulfillment, soit une réplication suivie d'un partage local. Un compte lecteur est créé dans la région du fournisseur.

**13. B.** Une annonce est une forme enrichie de partage : un partage ou une application native, plus un titre, une description et des exemples, pour des comptes désignés ou pour le Marketplace.

**14. D.** Le Data Exchange est une place de marché privée, réservée à un groupe de membres invités et administrée par le compte qui l'héberge.

**15. A.** La salle blanche permet une analyse conjointe dont seuls des résultats contrôlés sortent, sans exposer les données sous-jacentes de chaque partie.

**16. A, C.** La réplication des bases et des partages existe dans toutes les éditions ; la bascule, comme la réplication des autres objets du compte, demande Business Critical.

**17. C.** Les deux répliquent un ensemble d'objets en lecture seule ; seul le groupe de bascule peut être promu, ce qui ouvre l'écriture dans le compte cible.

**18. B.** La promotion s'exécute dans le compte cible, qui prend le relais : `ALTER FAILOVER GROUP ... PRIMARY`.

**19. D.** Client Redirect ne réplique aucune donnée : il fournit une URL de connexion stable que l'on fait pointer vers le compte devenu primaire.

**20. C.** Snowflake empêche par défaut le partage d'un compte Business Critical vers un compte d'édition inférieure ; un rôle ayant `OVERRIDE SHARE RESTRICTIONS` peut lever la restriction avec `SHARE_RESTRICTIONS = FALSE`.

---

[← Chapitre 19](../19-collaboration.md) | [Plan de préparation](PLAN.md) | [Fiche de révision](FICHE_REVISION.md)
