"""Brief PY3 — SQUELETTE À COMPLÉTER : consolidation Valenciennes + Roubaix.

Renomme ce fichier en consolidation.py et remplace chaque `...` en suivant le
commentaire. consolidation_exemple.py fait la même chose pour Tourcoing + Lille.
Les parties marquées « fourni » sont déjà écrites : ne les modifie pas.

Lancer :  python consolidation.py      puis      python controle.py
"""

import csv
import statistics
from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, fields
from datetime import date, datetime
from pathlib import Path

DOSSIER = Path(__file__).parent


# --- 1. Exception et enregistrement (fournis) ---------------------------------------
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


# --- 2. Lecture : un lecteur par fichier -----------------------------------------------
class LecteurCsv:
    """Lit UN export. `renommage` = {"nom dans le fichier": "nom standard"}."""

    def __init__(self, chemin, ville, separateur=",", renommage=None):
        self.chemin = Path(chemin)
        self.ville = ville
        self.separateur = separateur
        self.renommage = renommage or {}

    def lignes(self):
        with open(self.chemin, encoding="utf-8", newline="") as fichier:                 # fourni
            for brute in csv.DictReader(fichier, delimiter=self.separateur):             # fourni
                ligne = ...               # nouveau dict : chaque clé passée par self.renommage.get(cle, cle)
                ...                       # ajoute la ville : ligne["ville"] = self.ville
                yield ligne

    def __repr__(self):
        return f"LecteurCsv({self.chemin.name!r}, {self.ville!r}, sep={self.separateur!r})"


# --- 3. Nettoyage : règles de conformité -------------------------------------------------
class Nettoyeur:
    def __init__(self):
        self.rejets = Counter()           # raison -> nombre de lignes écartées

    def normaliser(self, ligne):
        """Transforme un dict brut en Vente, ou lève LigneInvalide."""
        try:
            jour = ...                    # datetime.strptime(ligne["date"].strip(), "%Y-%m-%d").date()
            quantite = ...                # int(...)
            montant = ...                 # float(...) en remplaçant une éventuelle virgule par un point
            produit = ...                 # ligne["produit"].strip()
        except KeyError as e:
            raise LigneInvalide(f"colonne manquante {e}", ligne) from None
        except ValueError:
            raise LigneInvalide("valeur mal formée", ligne) from None
        ...                               # quantite <= 0  -> raise LigneInvalide("quantité non positive", ligne)
        ...                               # montant <= 0   -> raise LigneInvalide("montant non positif", ligne)
        ...                               # produit vide   -> raise LigneInvalide("produit manquant", ligne)   (règle ajoutée)
        return Vente(
            date=jour,
            ville=...,                    # ligne["ville"] nettoyé : strip() puis title()
            categorie=...,                # strip()
            produit=produit,
            quantite=quantite,
            montant=round(montant, 2),
        )

    def nettoyer(self, lignes):
        """Génère les Vente valides et compte les rejets par raison."""
        for ligne in lignes:
            try:
                yield ...                 # self.normaliser(ligne)
            except LigneInvalide as erreur:
                ...                       # self.rejets[erreur.raison] += 1


# --- 4. Indicateurs : le contrat est fourni, écris les quatre variantes -------------------
class Indicateur(ABC):
    titre = "indicateur"

    @abstractmethod
    def calculer(self, ventes):
        """Renvoie un dict {libellé: valeur}."""

    def presenter(self, ventes):                                                          # fourni
        lignes = [f"{self.titre} :"]
        for libelle, valeur in self.calculer(ventes).items():
            texte = f"{valeur:,.2f} €" if isinstance(valeur, float) else str(valeur)
            lignes.append(f"  {libelle:<22} {texte:>16}".replace(",", " "))
        return "\n".join(lignes)


class CaParVille(Indicateur):
    titre = "Chiffre d'affaires par ville"

    def calculer(self, ventes):
        ...                               # defaultdict(float) : totaux[v.ville] += v.montant, puis dict trié décroissant


class PanierMoyen(Indicateur):
    titre = "Montant d'une vente"

    def calculer(self, ventes):
        ...                               # {"moyenne": ..., "médiane": ..., "écart-type": ...} avec statistics


class TopProduits(Indicateur):
    titre = "Top 5 produits (quantité)"

    def __init__(self, n=5):
        self.n = n

    def calculer(self, ventes):
        ...                               # Counter des quantités par produit, dict(compteur.most_common(self.n))


class CaParMois(Indicateur):              # indicateur ajouté : même modèle que CaParVille
    titre = "Chiffre d'affaires par mois"

    def calculer(self, ventes):
        ...                               # clé = v.date.strftime("%Y-%m"), dict trié par clé


# --- 5. Écriture (fournie) ----------------------------------------------------------------
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


# --- 6. Orchestration ------------------------------------------------------------------------
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
            ...                           # self.ventes.extend(self.nettoyeur.nettoyer(lecteur.lignes()))
            print(f"{lecteur!r} -> {len(self.ventes) - avant} ventes")
        ...                               # trie self.ventes par (date, ville)
        return ...                        # self.ecrivain.ecrire(self.ventes)

    def rapport(self):
        blocs = [f"=== Consolidation : {len(self.ventes)} ventes, "
                 f"{sum(self.nettoyeur.rejets.values())} lignes écartées ==="]
        if self.nettoyeur.rejets:
            blocs.append("Rejets : " + ", ".join(f"{r} ({n})" for r, n in self.nettoyeur.rejets.items()))
        ...                               # pour chaque indicateur : ajoute indicateur.presenter(self.ventes)
        return "\n\n".join(blocs)


def main():
    pipeline = Pipeline(
        lecteurs=[
            LecteurCsv(DOSSIER / "ventes_valenciennes.csv", "Valenciennes"),
            LecteurCsv(DOSSIER / "ventes_roubaix.csv", "Roubaix", renommage=...),   # {"qte": "quantite", "CA": "montant"}
        ],
        nettoyeur=Nettoyeur(),
        ecrivain=EcrivainCsv(DOSSIER / "ventes_consolidees_valenciennes_roubaix.csv"),
        indicateurs=[CaParVille(), PanierMoyen(), TopProduits(5), CaParMois()],
    )
    pipeline.executer()
    print()
    print(pipeline.rapport())


if __name__ == "__main__":
    main()
