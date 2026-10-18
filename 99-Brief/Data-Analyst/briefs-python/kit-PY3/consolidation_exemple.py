"""Consolidation de plusieurs exports magasin NordRetail en un seul fichier propre.

EXEMPLE À IMITER (Tourcoing + Lille). Lancer depuis ce dossier :

    python consolidation_exemple.py

Les exports n'ont pas tous le même format : séparateur différent, colonnes parfois
renommées. Le pipeline lit chaque fichier avec son propre lecteur, normalise les
lignes en objets Vente, écarte les lignes non conformes en comptant pourquoi,
écrit un CSV consolidé et affiche un rapport d'indicateurs.

Structure (voir diagramme_consolidation.md) :
- LigneInvalide (Exception)          : une ligne refusée, avec sa raison
- Vente (dataclass frozen)            : une ligne propre et typée
- LecteurCsv                          : lit UN fichier, sait son séparateur et ses renommages
- Nettoyeur                           : applique les règles de conformité, compte les rejets
- Indicateur (ABC) et ses variantes   : CaParVille, PanierMoyen, TopProduits
- EcrivainCsv                         : écrit le fichier consolidé
- Pipeline                            : compose tout ça et orchestre
"""

import csv
import statistics
from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict, fields
from datetime import date, datetime
from pathlib import Path

DOSSIER = Path(__file__).parent
COLONNES = ["date", "ville", "categorie", "produit", "quantite", "montant"]


# --- Exception et enregistrement --------------------------------------------------
class LigneInvalide(Exception):
    def __init__(self, raison, ligne):
        super().__init__(f"{raison} : {ligne}")
        self.raison = raison
        self.ligne = ligne


@dataclass(frozen=True)
class Vente:
    date: date
    ville: str
    categorie: str
    produit: str
    quantite: int
    montant: float


# --- Lecture : un lecteur par fichier --------------------------------------------
class LecteurCsv:
    """Lit un export et renvoie des dicts aux noms de colonnes standard.

    `renommage` traduit les en-têtes du fichier vers les noms standard,
    par exemple {"qte": "quantite", "CA": "montant"}. None si rien à renommer.
    """

    def __init__(self, chemin, ville, separateur=",", renommage=None):
        self.chemin = Path(chemin)
        self.ville = ville
        self.separateur = separateur
        self.renommage = renommage or {}

    def lignes(self):
        with open(self.chemin, encoding="utf-8", newline="") as fichier:
            for brute in csv.DictReader(fichier, delimiter=self.separateur):
                ligne = {self.renommage.get(cle, cle): valeur for cle, valeur in brute.items()}
                ligne["ville"] = self.ville                 # la ville n'est pas dans le fichier
                yield ligne

    def __repr__(self):
        return f"LecteurCsv({self.chemin.name!r}, {self.ville!r}, sep={self.separateur!r})"


# --- Nettoyage : règles de conformité -------------------------------------------
class Nettoyeur:
    """Transforme un dict brut en Vente, ou lève LigneInvalide. Compte les rejets par raison."""

    def __init__(self):
        self.rejets = Counter()

    def normaliser(self, ligne):
        try:
            jour = datetime.strptime(ligne["date"].strip(), "%Y-%m-%d").date()
            quantite = int(ligne["quantite"])
            montant = float(str(ligne["montant"]).replace(",", "."))   # tolère la virgule décimale
        except KeyError as e:
            raise LigneInvalide(f"colonne manquante {e}", ligne) from None
        except ValueError:
            raise LigneInvalide("valeur mal formée", ligne) from None
        if quantite <= 0:
            raise LigneInvalide("quantité non positive", ligne)
        if montant <= 0:
            raise LigneInvalide("montant non positif", ligne)
        return Vente(
            date=jour,
            ville=ligne["ville"].strip().title(),
            categorie=ligne["categorie"].strip(),
            produit=ligne["produit"].strip(),
            quantite=quantite,
            montant=round(montant, 2),
        )

    def nettoyer(self, lignes):
        """Génère les Vente valides ; mémorise les rejets."""
        for ligne in lignes:
            try:
                yield self.normaliser(ligne)
            except LigneInvalide as erreur:
                self.rejets[erreur.raison] += 1


# --- Indicateurs -------------------------------------------------------------------
class Indicateur(ABC):
    titre = "indicateur"

    @abstractmethod
    def calculer(self, ventes):
        """Renvoie un dict {libellé: valeur}."""

    def presenter(self, ventes):
        lignes = [f"{self.titre} :"]
        for libelle, valeur in self.calculer(ventes).items():
            texte = f"{valeur:,.2f} €" if isinstance(valeur, float) else str(valeur)
            lignes.append(f"  {libelle:<22} {texte:>16}".replace(",", " "))
        return "\n".join(lignes)


class CaParVille(Indicateur):
    titre = "Chiffre d'affaires par ville"

    def calculer(self, ventes):
        totaux = defaultdict(float)
        for v in ventes:
            totaux[v.ville] += v.montant
        return dict(sorted(totaux.items(), key=lambda item: item[1], reverse=True))


class PanierMoyen(Indicateur):
    titre = "Montant d'une vente"

    def calculer(self, ventes):
        montants = [v.montant for v in ventes]
        return {"moyenne": statistics.mean(montants), "médiane": statistics.median(montants),
                "écart-type": statistics.stdev(montants)}


class TopProduits(Indicateur):
    titre = "Top 5 produits (quantité)"

    def __init__(self, n=5):
        self.n = n

    def calculer(self, ventes):
        compteur = Counter()
        for v in ventes:
            compteur[v.produit] += v.quantite
        return dict(compteur.most_common(self.n))


# --- Écriture ------------------------------------------------------------------------
class EcrivainCsv:
    def __init__(self, chemin):
        self.chemin = Path(chemin)

    def ecrire(self, ventes):
        with open(self.chemin, "w", encoding="utf-8", newline="") as fichier:
            writer = csv.DictWriter(fichier, fieldnames=[f.name for f in fields(Vente)])
            writer.writeheader()
            for v in ventes:
                writer.writerow(asdict(v))
        return len(ventes)


# --- Orchestration -------------------------------------------------------------------
class Pipeline:
    def __init__(self, lecteurs, nettoyeur, ecrivain, indicateurs):
        self.lecteurs = list(lecteurs)
        self.nettoyeur = nettoyeur
        self.ecrivain = ecrivain
        self.indicateurs = list(indicateurs)
        self.ventes = []

    def executer(self):
        for lecteur in self.lecteurs:
            avant = len(self.ventes)
            self.ventes.extend(self.nettoyeur.nettoyer(lecteur.lignes()))
            print(f"{lecteur!r} -> {len(self.ventes) - avant} ventes")
        self.ventes.sort(key=lambda v: (v.date, v.ville))
        ecrites = self.ecrivain.ecrire(self.ventes)
        return ecrites

    def rapport(self):
        blocs = [f"=== Consolidation : {len(self.ventes)} ventes, "
                 f"{sum(self.nettoyeur.rejets.values())} lignes écartées ==="]
        if self.nettoyeur.rejets:
            blocs.append("Rejets : " + ", ".join(f"{r} ({n})" for r, n in self.nettoyeur.rejets.items()))
        for indicateur in self.indicateurs:
            blocs.append(indicateur.presenter(self.ventes))
        return "\n\n".join(blocs)


def main():
    pipeline = Pipeline(
        lecteurs=[
            LecteurCsv(DOSSIER / "ventes_tourcoing.csv", "Tourcoing"),
            LecteurCsv(DOSSIER / "ventes_lille.csv", "Lille", separateur=";"),
        ],
        nettoyeur=Nettoyeur(),
        ecrivain=EcrivainCsv(DOSSIER / "ventes_consolidees_exemple.csv"),
        indicateurs=[CaParVille(), PanierMoyen(), TopProduits(5)],
    )
    pipeline.executer()
    print()
    print(pipeline.rapport())


if __name__ == "__main__":
    main()
