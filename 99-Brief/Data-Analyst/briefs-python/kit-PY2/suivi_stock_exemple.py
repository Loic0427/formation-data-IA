"""Suivi de stock d'un entrepôt NordRetail.

EXEMPLE À IMITER : un petit module orienté objet, à reproduire sur un autre sujet
(le suivi des objectifs de chiffre d'affaires). Lancer depuis ce dossier :

    python suivi_stock_exemple.py

Structure (voir diagramme_stock.md) :
- une exception métier          StockInsuffisant
- un enregistrement immuable    Mouvement (dataclass)
- une entité encapsulée         Produit (stock protégé, méthodes qui valident)
- un contrat + ses variantes    Indicateur (ABC) -> StockTotal, ValeurStock, NbRuptures
- un agrégat par composition    Entrepot (contient des Produit, délègue, produit le rapport)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date


# --- 1. Exception métier ---------------------------------------------------------
class StockInsuffisant(Exception):
    """Levée quand on veut sortir plus d'unités qu'il n'y en a en stock."""

    def __init__(self, produit, manque):
        super().__init__(f"{produit} : il manque {manque} unité(s)")
        self.produit = produit
        self.manque = manque


# --- 2. Enregistrement immuable --------------------------------------------------
@dataclass(frozen=True)
class Mouvement:
    """Une entrée (quantite > 0) ou une sortie (quantite < 0) de stock."""

    jour: date
    produit: str
    quantite: int


# --- 3. Entité encapsulée --------------------------------------------------------
class Produit:
    """Un produit référencé, avec un stock qui ne peut jamais devenir négatif."""

    def __init__(self, nom, prix_unitaire, stock_initial=0):
        if prix_unitaire <= 0:
            raise ValueError(f"prix invalide pour {nom} : {prix_unitaire}")
        if stock_initial < 0:
            raise ValueError(f"stock initial négatif pour {nom}")
        self.nom = nom
        self.prix_unitaire = prix_unitaire
        self._stock = stock_initial              # interne : on passe par entrer / sortir

    @property
    def stock(self):                              # lecture seule
        return self._stock

    @property
    def valeur(self):                             # calculée, jamais stockée
        return self._stock * self.prix_unitaire

    def entrer(self, quantite):
        if quantite <= 0:
            raise ValueError("une entrée doit être strictement positive")
        self._stock += quantite

    def sortir(self, quantite):
        if quantite <= 0:
            raise ValueError("une sortie doit être strictement positive")
        if quantite > self._stock:
            raise StockInsuffisant(self.nom, quantite - self._stock)
        self._stock -= quantite

    def __repr__(self):
        return f"Produit({self.nom!r}, stock={self._stock})"

    def __lt__(self, autre):                      # permet sorted(produits)
        return self.valeur < autre.valeur


# --- 4. Contrat d'indicateur et ses variantes --------------------------------------
class Indicateur(ABC):
    """Tout indicateur sait se calculer sur une liste de produits et se présenter."""

    nom = "indicateur"
    unite = ""

    @abstractmethod
    def calculer(self, produits):
        ...

    def presenter(self, produits):                # concrète : partagée par toutes les filles
        valeur = self.calculer(produits)
        texte = f"{valeur:,.2f}" if isinstance(valeur, float) else f"{valeur:,}"
        return f"{self.nom:<28} {texte:>12} {self.unite}".replace(",", " ")


class StockTotal(Indicateur):
    nom = "Unités en stock"
    unite = "u"

    def calculer(self, produits):
        return sum(p.stock for p in produits)


class ValeurStock(Indicateur):
    nom = "Valeur du stock"
    unite = "€"

    def calculer(self, produits):
        return sum(p.valeur for p in produits)


class NbRuptures(Indicateur):
    nom = "Produits en rupture"
    unite = ""

    def calculer(self, produits):
        return sum(1 for p in produits if p.stock == 0)


# --- 5. Agrégat par composition --------------------------------------------------
class Entrepot:
    """Contient des produits ; applique les mouvements ; produit le rapport."""

    def __init__(self, nom):
        self.nom = nom
        self._produits = {}                       # nom -> Produit
        self.rejets = []                          # mouvements refusés, pour le rapport

    def ajouter(self, produit):
        self._produits[produit.nom] = produit

    @property
    def produits(self):
        return tuple(self._produits.values())     # copie immuable : pas de fuite

    def appliquer(self, mouvement):
        produit = self._produits[mouvement.produit]
        try:
            if mouvement.quantite > 0:
                produit.entrer(mouvement.quantite)
            else:
                produit.sortir(-mouvement.quantite)
        except (StockInsuffisant, ValueError) as erreur:
            self.rejets.append((mouvement, str(erreur)))

    def rapport(self, indicateurs):
        lignes = [f"=== Entrepôt {self.nom} ==="]
        for indicateur in indicateurs:            # polymorphisme : même appel, calcul différent
            lignes.append(indicateur.presenter(self.produits))
        lignes.append("")
        lignes.append("Produits par valeur de stock décroissante :")
        for produit in sorted(self.produits, reverse=True):
            lignes.append(f"  {produit.nom:<22} {produit.stock:>5} u  {produit.valeur:>10,.2f} €".replace(",", " "))
        if self.rejets:
            lignes.append("")
            lignes.append(f"Mouvements refusés : {len(self.rejets)}")
            for mouvement, raison in self.rejets:
                lignes.append(f"  {mouvement.jour} {mouvement.produit:<18} {mouvement.quantite:>5} -> {raison}")
        return "\n".join(lignes)


# --- 6. Point de lancement ---------------------------------------------------------
def main():
    entrepot = Entrepot("Lille-Nord")
    for nom, prix, stock in [("Perceuse", 105.66, 12), ("Vélo VTT", 545.21, 3),
                             ("Lampe LED", 134.22, 0), ("T-shirt coton", 24.90, 150)]:
        entrepot.ajouter(Produit(nom, prix, stock))

    mouvements = [
        Mouvement(date(2024, 3, 1), "Perceuse", -4),
        Mouvement(date(2024, 3, 2), "Vélo VTT", -5),        # refusé : il n'y en a que 3
        Mouvement(date(2024, 3, 3), "Lampe LED", 20),
        Mouvement(date(2024, 3, 4), "T-shirt coton", 0),    # refusé : quantité nulle
        Mouvement(date(2024, 3, 5), "Vélo VTT", -3),        # accepté : passe à 0
    ]
    for mouvement in mouvements:
        entrepot.appliquer(mouvement)

    print(entrepot.rapport([StockTotal(), ValeurStock(), NbRuptures()]))


if __name__ == "__main__":
    main()
