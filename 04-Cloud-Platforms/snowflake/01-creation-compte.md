# 1. Création d'un compte Snowflake

[← Retour au sommaire](README.md) | [Suivant →](02-connexion.md)

## Vue d'ensemble

Snowflake est un service entièrement géré (SaaS) : il n'y a ni serveur à installer ni logiciel à mettre à jour. Tout commence donc par un **compte**, qui est l'unité de base de Snowflake : un compte vit chez un seul fournisseur cloud, dans une seule région, avec une seule édition. Ces trois choix se font à l'inscription et déterminent les fonctions disponibles et le prix du crédit.

Ce chapitre crée un compte d'essai gratuit, explique les trois choix, et note l'identifiant de compte dont tous les outils auront besoin par la suite.

---

## 1. Les trois choix de l'inscription

### 1.1 L'édition

L'édition fixe le niveau de fonctionnalités. Chaque édition contient toutes les fonctions de la précédente.

| Édition | Ce qu'elle ajoute | Fonctions vues dans ce cours |
|---|---|---|
| **Standard** | toutes les fonctions de base | Time Travel limité à 1 jour |
| **Enterprise** | fonctions pour les grandes organisations | Time Travel jusqu'à 90 jours, warehouses multi-cluster, vues matérialisées, optimisation de recherche, masquage de colonnes, politiques d'accès aux lignes |
| **Business Critical** | protection renforcée des données sensibles | Tri-Secret Secure, connectivité privée (PrivateLink), bascule entre comptes (failover/failback) |
| **Virtual Private Snowflake (VPS)** | environnement Snowflake complètement isolé des autres comptes | niveau de sécurité le plus élevé |

**Pour ce cours, choisissez Enterprise.** Plusieurs fonctions étudiées plus loin (Time Travel au-delà d'un jour, multi-cluster, masquage) n'existent pas en édition Standard. Le crédit coûte plus cher en Enterprise, donc le solde d'essai baisse un peu plus vite, mais il reste largement suffisant avec un warehouse de taille X-Small.

### 1.2 Le fournisseur cloud

Snowflake s'exécute sur Amazon Web Services (AWS), Microsoft Azure ou Google Cloud Platform (GCP). L'interface et le SQL sont les mêmes partout. Pour ce cours, les trois conviennent ; AWS est le choix le plus courant dans les tutoriels.

### 1.3 La région

La région est l'endroit où les données sont stockées et où les calculs sont exécutés. Choisissez une région européenne proche de vous (par exemple Paris, Francfort ou l'Irlande selon le fournisseur). Toutes les fonctions ne sont pas disponibles dans toutes les régions : en cas de doute, la documentation de chaque fonction précise les régions prises en charge.

---

## 2. Créer le compte d'essai

### Étape 1 : ouvrir le formulaire

Rendez-vous sur https://signup.snowflake.com. L'essai dure 30 jours et comprend un solde d'usage gratuit (400 $ au moment de la rédaction). Aucune carte bancaire n'est demandée.

![Page d'inscription Snowflake](images/01-signup-homepage.png)
*Page d'inscription à l'essai gratuit*

### Étape 2 : renseigner vos informations

Le formulaire demande votre prénom, votre nom, votre adresse e-mail, votre pays et la raison de l'inscription. Utilisez une adresse que vous consultez : le lien d'activation y sera envoyé.

### Étape 3 : configurer le compte

Le second écran demande le nom de votre entreprise ou école, puis les trois choix de la section 1 :

1. **Édition** : `Enterprise`.
2. **Fournisseur cloud** : AWS, Azure ou GCP.
3. **Région** : une région européenne.

Acceptez les conditions puis validez.

![Choix de l'édition, du cloud et de la région](images/03-edition-selection.png)
*Second écran du formulaire. La capture montre l'édition Standard : sélectionnez Enterprise dans la liste.*

### Étape 4 : activer le compte

1. Ouvrez l'e-mail envoyé par Snowflake (vérifiez le dossier des indésirables) et cliquez sur le bouton d'activation. Le lien expire au bout de 72 heures.
2. Choisissez un nom d'utilisateur et un mot de passe. Par défaut, Snowflake exige au moins 14 caractères, dont une majuscule, une minuscule et un chiffre.

![E-mail d'activation](images/05-activation-email.png)
*E-mail d'activation reçu de Snowflake*

L'e-mail contient aussi l'adresse de votre compte : conservez-le.

![Adresse du compte dans l'e-mail](images/07-first-login.png)
*L'adresse du compte, à conserver : la partie encadrée est l'identifiant du compte*

Le premier utilisateur d'un compte d'essai reçoit le rôle `ACCOUNTADMIN`, le plus puissant du compte. Les rôles sont expliqués au [chapitre 3](03-creation-role.md).

---

## 3. L'identifiant de compte

Tous les outils qui se connectent à Snowflake (dbt, Airflow, connecteur Python, Snowflake CLI) demandent l'**identifiant de compte**. Il existe deux formats :

| Format | Exemple | Statut |
|---|---|---|
| `ORGANISATION-COMPTE` (nom de l'organisation, tiret, nom du compte) | `MYORG-MYACCOUNT` | format recommandé |
| Account locator (code attribué par Snowflake, parfois suivi de la région et du cloud) | `xy12345.eu-west-1` | ancien format, toujours accepté mais déconseillé |

L'adresse web du compte se construit à partir du premier format :

```
https://ORGANISATION-COMPTE.snowflakecomputing.com
```

Pour retrouver l'identifiant une fois connecté :

- Dans l'interface : menu utilisateur (votre nom, en bas à gauche), puis **View account details**. La fenêtre affiche l'identifiant et l'adresse du compte.
- En SQL :

```sql
SELECT CURRENT_ORGANIZATION_NAME() || '-' || CURRENT_ACCOUNT_NAME() AS account_identifier;
```

Dans une instruction SQL (partage de données, réplication), le séparateur est un point : `ORGANISATION.COMPTE`.

---

## 4. Ce qu'il faut savoir sur le compte d'essai

- L'essai se termine au bout de 30 jours **ou** dès que le solde gratuit est épuisé, selon ce qui arrive en premier.
- À la fin de l'essai, le compte est suspendu : on peut encore s'y connecter, mais plus rien ne fonctionne tant qu'un moyen de paiement n'est pas ajouté.
- Les fonctions d'IA sont désactivées par défaut sur un compte d'essai tant qu'aucune carte bancaire n'est enregistrée.
- Le solde restant est affiché en bas du menu de navigation. Le [chapitre 9](09-monitoring.md) montre comment suivre et limiter la consommation.

### Informations à conserver

| Information | Exemple |
|---|---|
| Identifiant de compte | `ORGANISATION-COMPTE` |
| Adresse du compte | `https://ORGANISATION-COMPTE.snowflakecomputing.com` |
| Nom d'utilisateur | celui choisi à l'activation |
| Édition, cloud, région | Enterprise, AWS, Europe (Paris) |

Le mot de passe se range dans un gestionnaire de mots de passe, pas dans un fichier de notes.

---

## À retenir pour la certification

- Snowflake est un service SaaS disponible sur trois clouds : AWS, Azure et GCP. Un compte est créé dans **une** région d'**un** fournisseur, avec **une** édition.
- Quatre éditions : Standard, Enterprise, Business Critical, Virtual Private Snowflake. Chacune inclut les fonctions de la précédente.
- Enterprise est l'édition minimale pour : Time Travel jusqu'à 90 jours, warehouses multi-cluster, vues matérialisées, optimisation de recherche, masquage de colonnes et politiques d'accès aux lignes.
- Business Critical est l'édition minimale pour : Tri-Secret Secure, la connectivité privée (PrivateLink) et le failover/failback.
- Le format d'identifiant de compte recommandé est `ORGANISATION-COMPTE` ; l'account locator est l'ancien format.

## ✅ Points de vérification
- [ ] Compte créé en édition Enterprise, dans une région européenne
- [ ] Compte activé, nom d'utilisateur et mot de passe choisis
- [ ] Identifiant `ORGANISATION-COMPTE` et adresse du compte notés

## Documentation officielle
- [Comptes d'essai](https://docs.snowflake.com/en/user-guide/admin-trial-account)
- [Éditions de Snowflake](https://docs.snowflake.com/en/user-guide/intro-editions)
- [Identifiants de compte](https://docs.snowflake.com/en/user-guide/admin-account-identifier)

---

[← Retour au sommaire](README.md) | [Suivant →](02-connexion.md)
