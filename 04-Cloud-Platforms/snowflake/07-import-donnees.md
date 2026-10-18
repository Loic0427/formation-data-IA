# 7. Import de données CSV

[← Retour au sommaire](README.md) | [← Précédent](06-creation-tables.md) | [Suivant →](08-gestion-privileges.md)

## Vue d'ensemble

Une table vide ne sert à rien : il faut y charger des fichiers. Snowsight propose un assistant qui charge un fichier de votre poste dans une table en quelques clics. C'est la façon la plus rapide de faire un premier chargement ou un essai.

Derrière l'assistant, Snowflake fait toujours la même chose : le fichier est déposé dans une zone de stockage appelée **stage**, puis la commande `COPY INTO` le lit selon un **format de fichier** et l'écrit dans la table. L'assistant convient à des chargements ponctuels ; un chargement régulier s'écrit en SQL, ce que fait le [chapitre 11](11-chargement-stage-copy.md).

---

## 1. Préparer les fichiers

Créez ces quatre fichiers sur votre poste, encodés en UTF-8. Leurs colonnes correspondent aux tables du [chapitre 6](06-creation-tables.md).

**customers.csv**
```csv
CUSTOMER_ID,FIRST_NAME,LAST_NAME,EMAIL,PHONE,ADDRESS,CITY,POSTAL_CODE,COUNTRY
1,Jean,Dupont,jean.dupont@email.com,0123456789,123 Rue de la Paix,Paris,75001,France
2,Marie,Martin,marie.martin@email.com,0987654321,456 Avenue des Champs,Lyon,69001,France
3,Pierre,Durand,pierre.durand@email.com,0147258369,789 Boulevard Voltaire,Marseille,13001,France
4,Sophie,Moreau,sophie.moreau@email.com,0156789012,321 Place République,Toulouse,31000,France
5,Thomas,Rousseau,thomas.rousseau@email.com,0167890123,654 Rue Commerce,Nice,06000,France
```

**products.csv**
```csv
PRODUCT_ID,PRODUCT_NAME,CATEGORY,BRAND,UNIT_PRICE,DESCRIPTION
101,Ordinateur Portable HP,Informatique,HP,899.99,Ordinateur portable 15 pouces avec SSD 512GB
102,Souris sans fil Logitech,Accessoires,Logitech,29.99,Souris optique sans fil ergonomique
103,Clavier mécanique Corsair,Accessoires,Corsair,129.99,Clavier mécanique gaming RGB
104,Écran Dell 27 pouces,Informatique,Dell,459.99,Moniteur IPS 4K avec HDR
105,Casque Sony WH-1000XM4,Audio,Sony,299.99,Casque bluetooth réduction de bruit
```

**orders.csv**
```csv
ORDER_ID,CUSTOMER_ID,ORDER_DATE,ORDER_STATUS,TOTAL_AMOUNT,SHIPPING_ADDRESS
1001,1,2024-01-15,Delivered,899.99,123 Rue de la Paix Paris
1002,2,2024-01-16,Delivered,189.97,456 Avenue des Champs Lyon
1003,3,2024-01-18,Shipped,589.98,789 Boulevard Voltaire Marseille
1004,4,2024-01-20,Processing,459.99,321 Place République Toulouse
1005,5,2024-01-22,Pending,329.98,654 Rue Commerce Nice
```

**order_items.csv**
```csv
ORDER_ITEM_ID,ORDER_ID,PRODUCT_ID,QUANTITY,UNIT_PRICE
1,1001,101,1,899.99
2,1002,102,2,29.99
3,1002,103,1,129.99
4,1003,104,1,459.99
5,1003,103,1,129.99
6,1004,104,1,459.99
7,1005,102,1,29.99
8,1005,105,1,299.99
```

Le dossier `Data/` du cours contient des jeux de données plus riches (`ecommerce`, `finance`, `saas`, `airbnb`). Leurs colonnes diffèrent de celles de nos quatre tables : ils sont utilisés à partir du chapitre 11.

---

## 2. Charger un fichier avec l'assistant de Snowsight

Prenez le rôle `SYSADMIN` (propriétaire des tables) et le warehouse `SALES_WH` : un chargement a besoin d'un warehouse en marche.

1. Dans le menu, sélectionnez **Ingestion** » **Add Data**, puis **Load data into a Table**. Autre chemin : dans **Catalog**, ouvrez la table `SALES_DB.RAW_DATA.CUSTOMERS` et sélectionnez **Load Data**.
2. Déposez `customers.csv` dans la fenêtre, ou parcourez votre disque pour le sélectionner.
3. Choisissez la base `SALES_DB`, le schéma `RAW_DATA` et la table existante `CUSTOMERS`.
4. Dans l'écran de réglage du format, vérifiez :
   - le type de fichier : CSV, délimité par des virgules ;
   - l'en-tête : la première ligne contient les noms de colonnes ;
   - l'aperçu : chaque colonne du fichier est associée à la bonne colonne de la table ;
   - le comportement en cas d'erreur (question « What should happen if an error occurs during loading ») : laissez l'arrêt du chargement.
5. Lancez le chargement, puis ouvrez la table pour voir les lignes.

Répétez pour les trois autres fichiers, dans cet ordre : `products.csv`, `orders.csv`, `order_items.csv`.

| Limite de l'assistant | Valeur |
|---|---|
| Taille d'un fichier | 250 Mo au maximum |
| Nombre de fichiers par chargement | 250 au maximum |
| Formats acceptés | CSV, TSV, JSON, Avro, ORC, Parquet, XML |
| Privilèges nécessaires | `USAGE` sur la base et le schéma, `INSERT` sur la table |

Par défaut, l'assistant **ajoute** les lignes à la table (mode Append). Si vous chargez deux fois le même fichier par erreur, contrôlez le nombre de lignes (section 5) ; en cas de doublons, videz la table avec `TRUNCATE TABLE` et rechargez.

---

## 3. Ce que fait l'assistant : stage, format de fichier, COPY INTO

```
fichier sur votre poste
      │  dépôt du fichier
      ▼
   stage                (zone de dépôt des fichiers)
      │  COPY INTO      (lecture selon un format de fichier)
      ▼
   table
```

| Notion | Rôle |
|---|---|
| Stage interne | zone de stockage gérée par Snowflake, où l'on dépose les fichiers |
| Stage externe | pointeur vers un stockage cloud que vous gérez : Amazon S3, Azure Blob Storage, Google Cloud Storage |
| Format de fichier | description de la structure des fichiers : type, séparateur, en-tête, valeurs à lire comme `NULL` |
| `COPY INTO <table>` | commande qui charge les fichiers d'un stage dans une table |

Le chargement équivalent en SQL ressemble à ceci (le [chapitre 11](11-chargement-stage-copy.md) le construit pas à pas, avec le dépôt du fichier par `PUT`) :

```sql
COPY INTO SALES_DB.RAW_DATA.CUSTOMERS
  FROM @MON_STAGE
  FILES = ('customers.csv')
  FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '"')
  ON_ERROR = ABORT_STATEMENT;
```

---

## 4. Deux familles d'options à ne pas confondre

### Les options du format de fichier : comment lire le fichier

Elles décrivent le fichier et se placent dans `FILE_FORMAT = (...)` ou dans un objet `FILE FORMAT`.

| Option (CSV) | Rôle |
|---|---|
| `FIELD_DELIMITER` | caractère qui sépare les colonnes (virgule par défaut) |
| `SKIP_HEADER` | nombre de lignes d'en-tête à ignorer au début du fichier |
| `FIELD_OPTIONALLY_ENCLOSED_BY` | caractère qui peut entourer une valeur, par exemple `"` |
| `TRIM_SPACE` | supprime les espaces autour des valeurs |
| `NULL_IF` | liste des chaînes à lire comme `NULL`, par exemple `('', 'N/A')` |

### Les options de copie : comment se comporte le chargement

Elles appartiennent à la commande `COPY INTO`. La principale est `ON_ERROR` :

| Valeur de `ON_ERROR` | Comportement |
|---|---|
| `ABORT_STATEMENT` | à la première erreur, le chargement s'arrête et rien n'est chargé. Valeur par défaut de `COPY INTO` |
| `CONTINUE` | les lignes en erreur sont ignorées, les autres sont chargées |
| `SKIP_FILE` | un fichier qui contient une erreur est ignoré en entier. Valeur par défaut de Snowpipe |
| `SKIP_FILE_<n>` ou `'SKIP_FILE_<n>%'` | le fichier est ignoré à partir de `n` erreurs, ou de `n` % de lignes en erreur |

Autres options de copie utiles : `VALIDATION_MODE` (contrôler les fichiers sans rien charger) et `PURGE = TRUE` (supprimer du stage les fichiers chargés avec succès).

`COPY INTO` peut aussi transformer les données pendant le chargement, mais cela se fait avec une requête `SELECT` sur le stage (réordonner des colonnes, en écarter, convertir un type), et non avec les options ci-dessus.

---

## 5. Contrôler les données chargées

### Nombre de lignes

```sql
USE SCHEMA SALES_DB.RAW_DATA;

SELECT 'CUSTOMERS' AS table_name, COUNT(*) AS row_count FROM CUSTOMERS
UNION ALL SELECT 'PRODUCTS',    COUNT(*) FROM PRODUCTS
UNION ALL SELECT 'ORDERS',      COUNT(*) FROM ORDERS
UNION ALL SELECT 'ORDER_ITEMS', COUNT(*) FROM ORDER_ITEMS;
```

Résultat attendu : 5, 5, 5 et 8 lignes.

### Unicité et intégrité référentielle

Snowflake n'applique ni les clés primaires ni les clés étrangères sur les tables standard ([chapitre 6](06-creation-tables.md)) : c'est à vous de vérifier, après chaque chargement, que les données respectent le modèle. Chacune de ces requêtes doit renvoyer zéro ligne.

```sql
-- Doublons sur la clé primaire
SELECT CUSTOMER_ID, COUNT(*) AS nb
FROM CUSTOMERS
GROUP BY CUSTOMER_ID
HAVING COUNT(*) > 1;

-- Commandes dont le client n'existe pas
SELECT o.ORDER_ID, o.CUSTOMER_ID
FROM ORDERS o
LEFT JOIN CUSTOMERS c ON c.CUSTOMER_ID = o.CUSTOMER_ID
WHERE c.CUSTOMER_ID IS NULL;

-- Lignes de commande dont la commande ou le produit n'existe pas
SELECT oi.ORDER_ITEM_ID
FROM ORDER_ITEMS oi
LEFT JOIN ORDERS o   ON o.ORDER_ID = oi.ORDER_ID
LEFT JOIN PRODUCTS p ON p.PRODUCT_ID = oi.PRODUCT_ID
WHERE o.ORDER_ID IS NULL OR p.PRODUCT_ID IS NULL;
```

### Cohérence des montants

```sql
-- Le total d'une commande doit être la somme de ses lignes
SELECT o.ORDER_ID, o.TOTAL_AMOUNT, SUM(oi.QUANTITY * oi.UNIT_PRICE) AS total_calcule
FROM ORDERS o
JOIN ORDER_ITEMS oi ON oi.ORDER_ID = o.ORDER_ID
GROUP BY o.ORDER_ID, o.TOTAL_AMOUNT
HAVING o.TOTAL_AMOUNT <> SUM(oi.QUANTITY * oi.UNIT_PRICE);
```

---

## 6. Diagnostiquer

| Symptôme | Cause probable | Correction |
|---|---|---|
| Nombre de colonnes du fichier différent de celui de la table | mauvais séparateur, ou valeur contenant une virgule sans guillemets | vérifier le séparateur ; entourer les valeurs de guillemets et régler `FIELD_OPTIONALLY_ENCLOSED_BY` |
| Valeur numérique ou date non reconnue | la ligne d'en-tête est lue comme une donnée, ou le format de date diffère | ignorer l'en-tête ; écrire les dates au format `AAAA-MM-JJ` |
| Caractères accentués illisibles | fichier qui n'est pas en UTF-8 | réenregistrer le fichier en UTF-8 |
| Lignes en double | fichier chargé deux fois en mode Append | `TRUNCATE TABLE` puis recharger |
| Fichier refusé par l'assistant | fichier de plus de 250 Mo | passer par un stage et `COPY INTO` (chapitre 11) |

---

## À retenir pour la certification

- Un chargement en masse passe par un stage (interne ou externe) et par la commande `COPY INTO <table>`, qui utilise un warehouse.
- Formats de fichier acceptés au chargement : CSV, JSON, Avro, ORC, Parquet, XML.
- `ON_ERROR` vaut par défaut `ABORT_STATEMENT` pour `COPY INTO` et `SKIP_FILE` pour Snowpipe. Les autres valeurs sont `CONTINUE`, `SKIP_FILE_<n>` et `'SKIP_FILE_<n>%'`.
- `SKIP_HEADER`, `FIELD_DELIMITER`, `TRIM_SPACE`, `NULL_IF` et `FIELD_OPTIONALLY_ENCLOSED_BY` sont des options de format de fichier, pas des options de copie.
- `VALIDATION_MODE` contrôle les fichiers sans les charger ; `PURGE = TRUE` supprime du stage les fichiers chargés.
- L'assistant de Snowsight accepte des fichiers de 250 Mo au maximum.

## ✅ Points de vérification
- [ ] Quatre fichiers CSV créés en UTF-8
- [ ] Données chargées dans les quatre tables : 5, 5, 5 et 8 lignes
- [ ] Aucun doublon de clé primaire
- [ ] Aucune commande sans client, aucune ligne de commande orpheline

## Documentation officielle
- [Charger des données avec Snowsight](https://docs.snowflake.com/en/user-guide/data-load-web-ui)
- [COPY INTO table](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table)
- [CREATE FILE FORMAT](https://docs.snowflake.com/en/sql-reference/sql/create-file-format)

---

[← Retour au sommaire](README.md) | [← Précédent](06-creation-tables.md) | [Suivant →](08-gestion-privileges.md)
