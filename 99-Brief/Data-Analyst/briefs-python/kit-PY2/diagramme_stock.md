# Diagramme de classes — exemple « suivi de stock »

Structure du module `suivi_stock_exemple.py`. À reproduire, avec vos propres classes, dans `diagramme_objectifs.md`.

```mermaid
classDiagram
    class StockInsuffisant {
        +str produit
        +int manque
    }
    Exception <|-- StockInsuffisant

    class Mouvement {
        <<dataclass frozen>>
        +date jour
        +str produit
        +int quantite
    }

    class Produit {
        +str nom
        +float prix_unitaire
        -int stock
        +stock() int
        +valeur() float
        +entrer(quantite)
        +sortir(quantite)
    }

    class Indicateur {
        <<abstract>>
        +str nom
        +str unite
        +calculer(produits)*
        +presenter(produits) str
    }
    Indicateur <|-- StockTotal
    Indicateur <|-- ValeurStock
    Indicateur <|-- NbRuptures

    class Entrepot {
        +str nom
        -dict produits
        +list rejets
        +ajouter(produit)
        +appliquer(mouvement)
        +rapport(indicateurs) str
    }
    Entrepot o-- "0..*" Produit : contient
    Entrepot ..> Mouvement : applique
    Entrepot ..> Indicateur : utilise
    Produit ..> StockInsuffisant : lève
```

Lecture :

- **Héritage** (`<|--`) : les trois indicateurs concrets **sont des** `Indicateur` ; `StockInsuffisant` **est une** `Exception`.
- **Agrégation** (`o--`) : l'entrepôt **contient** des produits créés à l'extérieur et ajoutés un par un.
- **Dépendance** (`..>`) : l'entrepôt **utilise** des mouvements et des indicateurs sans les posséder.
- `-int stock` est **privé** : on le lit par la propriété `stock()` et on le modifie seulement par `entrer` / `sortir`, qui valident.
- `calculer(produits)*` : l'astérisque marque la méthode **abstraite**, que chaque fille doit implémenter.
