# Diagramme de classes — exemple « consolidation Tourcoing + Lille »

Structure du module `consolidation_exemple.py`. À reproduire, avec vos propres classes, dans votre `RAPPORT.md`.

```mermaid
classDiagram
    class LigneInvalide {
        +str raison
        +dict ligne
    }
    Exception <|-- LigneInvalide

    class Vente {
        <<dataclass frozen>>
        +date date
        +str ville
        +str categorie
        +str produit
        +int quantite
        +float montant
    }

    class LecteurCsv {
        +Path chemin
        +str ville
        +str separateur
        +dict renommage
        +lignes() dict
    }

    class Nettoyeur {
        +Counter rejets
        +normaliser(ligne) Vente
        +nettoyer(lignes) Vente
    }

    class Indicateur {
        <<abstract>>
        +str titre
        +calculer(ventes)* dict
        +presenter(ventes) str
    }
    Indicateur <|-- CaParVille
    Indicateur <|-- PanierMoyen
    Indicateur <|-- TopProduits

    class EcrivainCsv {
        +Path chemin
        +ecrire(ventes) int
    }

    class Pipeline {
        +list ventes
        +executer() int
        +rapport() str
    }
    Pipeline *-- "1..*" LecteurCsv
    Pipeline *-- "1" Nettoyeur
    Pipeline *-- "1" EcrivainCsv
    Pipeline o-- "1..*" Indicateur
    Nettoyeur ..> Vente : produit
    Nettoyeur ..> LigneInvalide : lève
    EcrivainCsv ..> Vente : écrit
```

Lecture :

- `Pipeline` **compose** (`*--`) ses lecteurs, son nettoyeur et son écrivain : ils sont construits pour lui et n'ont pas de sens sans lui.
- Les indicateurs sont **agrégés** (`o--`) : on peut en passer une liste différente à chaque exécution.
- `LecteurCsv` ne connaît que **son** fichier : séparateur et renommage sont des paramètres, pas du code dupliqué.
- Toute la logique de conformité est dans `Nettoyeur` ; une ligne refusée est une **exception** `LigneInvalide` porteuse de sa raison, comptée dans `rejets`.
