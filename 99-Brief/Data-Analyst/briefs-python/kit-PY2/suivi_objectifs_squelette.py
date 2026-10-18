"""Brief PY2 — SQUELETTE À COMPLÉTER : suivi des objectifs de CA 2024.

Renomme ce fichier en suivi_objectifs.py et remplace chaque `...` en suivant le
commentaire. Chaque classe a son équivalent dans suivi_stock_exemple.py :

    StockInsuffisant -> ObjectifInvalide      Mouvement -> Realisation
    Produit          -> Magasin               Entrepot  -> Reseau
    StockTotal / ValeurStock / NbRuptures -> CaTotal / TauxGlobal / NbMagasinsEnRetard

Lancer :  python suivi_objectifs.py
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from donnees_objectifs import CA_REEL, OBJECTIFS      # listes de (ville, mois, montant)


# --- 1. Exception métier (modèle : StockInsuffisant) -----------------------------
class ObjectifInvalide(Exception):
    """Un objectif impossible : mois hors de 1..12 ou montant non positif."""

    def __init__(self, ville, mois, raison):
        super().__init__(...)             # message : f"{ville}, mois {mois} : {raison}"
        ...                               # garde ville et mois en attributs


# --- 2. Enregistrement immuable (modèle : Mouvement) -------------------------------
@dataclass(frozen=True)
class Realisation:
    """Le CA réellement réalisé par un magasin sur un mois."""

    ville: str
    mois: int
    ca: float


# --- 3. Entité encapsulée (modèle : Produit) ----------------------------------------
class Magasin:
    def __init__(self, ville):
        self.ville = ville
        self._objectifs = {}              # mois -> objectif  (interne : passe par fixer_objectif)
        self._realise = {}                # mois -> CA réel

    def fixer_objectif(self, mois, montant):
        ...                               # si mois pas entre 1 et 12 : raise ObjectifInvalide(self.ville, mois, "mois hors de 1..12")
        ...                               # si montant <= 0 : raise ObjectifInvalide(..., "montant non positif")
        ...                               # sinon range montant dans self._objectifs[mois]

    def enregistrer(self, realisation):
        ...                               # si realisation.ca < 0 : raise ValueError("CA négatif")
        ...                               # sinon self._realise[realisation.mois] = realisation.ca

    @property
    def objectifs(self):
        ...                               # une COPIE de self._objectifs : dict(self._objectifs)

    @property
    def objectif_annuel(self):
        ...                               # somme des objectifs

    @property
    def ca_annuel(self):
        ...                               # somme des CA réels

    @property
    def taux_atteinte(self):
        ...                               # ca_annuel / objectif_annuel  (0.0 s'il n'y a aucun objectif)

    def mois_atteints(self):
        """Liste des mois où le CA réel atteint ou dépasse l'objectif."""
        ...                               # compréhension sur sorted(self._objectifs.items())

    def __repr__(self):
        ...                               # f"Magasin({self.ville!r}, taux={self.taux_atteinte:.1%})"

    def __lt__(self, autre):
        ...                               # compare les taux d'atteinte


# --- 4. Contrat d'indicateur (fourni) et ses trois variantes (à écrire) --------------
class Indicateur(ABC):
    nom = "indicateur"
    unite = ""

    @abstractmethod
    def calculer(self, magasins):
        ...                               # fourni : méthode abstraite, pas de corps

    def presenter(self, magasins):                                   # fourni
        valeur = self.calculer(magasins)
        if self.unite == "%":
            return f"{self.nom:<30} {valeur:>13.1%}"
        texte = f"{valeur:,.2f}" if isinstance(valeur, float) else f"{valeur:,}"
        return f"{self.nom:<30} {texte:>14} {self.unite}".replace(",", " ")


class CaTotal(Indicateur):
    nom = "CA réalisé (réseau)"
    unite = "€"

    def calculer(self, magasins):
        ...                               # somme des ca_annuel


class TauxGlobal(Indicateur):
    nom = "Taux d'atteinte global"
    unite = "%"

    def calculer(self, magasins):
        ...                               # somme des ca_annuel / somme des objectif_annuel


class NbMagasinsEnRetard(Indicateur):
    nom = "Magasins sous l'objectif"
    unite = ""

    def calculer(self, magasins):
        ...                               # nombre de magasins dont taux_atteinte < 1


# --- 5. Agrégat par composition (modèle : Entrepot) ---------------------------------
class Reseau:
    def __init__(self, nom):
        self.nom = nom
        self._magasins = {}               # ville -> Magasin
        self.rejets = []                  # messages des entrées refusées

    def ajouter(self, magasin):
        ...                               # range le magasin dans le dict, clé = sa ville

    @property
    def magasins(self):
        ...                               # tuple(self._magasins.values())

    def charger(self, objectifs, realisations):
        for ville, mois, montant in objectifs:
            magasin = self._magasins.setdefault(ville, Magasin(ville))   # crée le magasin s'il manque
            try:
                ...                       # magasin.fixer_objectif(mois, montant)
            except ObjectifInvalide as erreur:
                ...                       # ajoute str(erreur) à self.rejets
        for ville, mois, ca in realisations:
            ...                           # self._magasins[ville].enregistrer(Realisation(ville, mois, ca))

    def rapport(self, indicateurs):
        lignes = [f"=== Réseau {self.nom} : objectifs 2024 ==="]
        for indicateur in indicateurs:
            ...                           # ajoute indicateur.presenter(self.magasins)
        lignes.append("")
        lignes.append("Magasins par taux d'atteinte décroissant :")
        for magasin in sorted(self.magasins, reverse=True):
            atteints = magasin.mois_atteints()
            lignes.append(f"  {magasin.ville:<13} {magasin.taux_atteinte:>6.1%}  {len(atteints):>2}/12 mois atteints  {atteints}")
        if self.rejets:
            lignes.append("")
            lignes.append(f"Entrées refusées : {len(self.rejets)}")
            ...                           # une ligne "  - message" par rejet
        return "\n".join(lignes)


# --- 6. Point de lancement ------------------------------------------------------------
def main():
    reseau = Reseau("NordRetail")
    objectifs = list(OBJECTIFS) + [...]  # ajoute DEUX objectifs invalides, ex. ("Lille", 13, 100000) et ("Amiens", 6, -5000)
    reseau.charger(objectifs, CA_REEL)
    print(reseau.rapport([CaTotal(), TauxGlobal(), NbMagasinsEnRetard()]))


if __name__ == "__main__":
    main()
