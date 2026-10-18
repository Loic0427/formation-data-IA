"""Brief PY1 — SQUELETTE À COMPLÉTER : analyse de l'export de Valenciennes.

Renomme ce fichier en analyse_valenciennes.py, puis remplace chaque `...` en
suivant le commentaire. L'exemple analyse_magasin_exemple.py fait la même chose
pour Tourcoing : regarde-le autant que tu veux, mais écris tes lignes toi-même.

Lancer :  python analyse_valenciennes.py
"""

import csv
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

# --- Paramètres (déjà remplis) -------------------------------------------------
FICHIER = Path(__file__).parent / "ventes_valenciennes.csv"
VILLE = "Valenciennes"
SEPARATEUR = ","


# --- 1. Lecture (le cadre est fourni : complète les règles) ----------------------
def lire_ventes(chemin, separateur=","):
    """Renvoie (liste de ventes, nombre de lignes écartées)."""
    ventes = []
    ecartees = 0
    with open(chemin, encoding="utf-8", newline="") as fichier:          # fourni
        for ligne in csv.DictReader(fichier, delimiter=separateur):      # fourni : un dict par ligne
            try:
                vente = {
                    "date": ...,          # datetime.strptime(ligne["date"], "%Y-%m-%d").date()
                    "categorie": ...,     # ligne["categorie"] sans espaces autour (strip)
                    "produit": ...,       # idem pour le produit
                    "quantite": ...,      # entier
                    "montant": ...,       # flottant
                }
            except (KeyError, ValueError):
                ecartees += 1
                continue
            if ...:                       # quantité OU montant pas strictement positif
                ecartees += 1
                continue
            ventes.append(vente)
    return ventes, ecartees


# --- 2. Indicateurs : une fonction = un indicateur ---------------------------------
def chiffre_affaires(ventes):
    """Somme des montants."""
    ...                                   # sum(...) sur les montants


def ca_par_categorie(ventes):
    """Dict {catégorie: CA}, du plus gros au plus petit."""
    totaux = defaultdict(float)
    ...                                   # boucle : ajoute le montant à totaux[catégorie]
    return ...                            # dict trié par valeur décroissante (sorted + key + reverse)


def top_produits(ventes, n=5):
    """Liste des n (produit, quantité) les plus vendus."""
    compteur = Counter()
    ...                                   # boucle : ajoute la quantité à compteur[produit]
    return ...                            # compteur.most_common(n)


def statistiques_montant(ventes):
    """Dict moyenne / mediane / ecart_type / minimum / maximum du montant."""
    montants = ...                        # liste des montants
    return {
        "moyenne": ...,                   # statistics.mean
        "mediane": ...,                   # statistics.median
        "ecart_type": ...,                # statistics.stdev
        "minimum": ...,                   # min(montants)
        "maximum": ...,                   # max(montants)
    }


def ca_par_mois(ventes):
    """Dict {'AAAA-MM': CA} dans l'ordre des mois."""
    totaux = defaultdict(float)
    ...                                   # clé = v["date"].strftime("%Y-%m")
    return ...                            # dict trié par clé


# --- 3. Les deux indicateurs en plus (même modèle que ceux du dessus) -------------
def ca_moyen_par_jour(ventes):
    """CA total divisé par le nombre de jours DISTINCTS ayant au moins une vente."""
    jours = ...                           # un set des dates : {v["date"] for v in ventes}
    return ...                            # chiffre_affaires(ventes) / len(jours)


def quantite_par_categorie(ventes):
    """Dict {catégorie: quantité vendue}, trié décroissant (même modèle que ca_par_categorie)."""
    ...                                   # defaultdict(int), même boucle avec v["quantite"], même tri


# --- 4. Rapport -------------------------------------------------------------------
def afficher_rapport(ville, ventes, ecartees):
    ca = chiffre_affaires(ventes)
    stats = statistiques_montant(ventes)
    mois = ca_par_mois(ventes)
    meilleur_mois = ...                   # la clé de `mois` dont la valeur est la plus grande : max(mois, key=mois.get)

    print(f"=== Rapport {ville} ===")
    print(f"Lignes conformes : {len(ventes)} | écartées : {ecartees}")
    print(f"Chiffre d'affaires : {ca:,.2f} €".replace(",", " "))
    print(f"CA moyen par jour de vente : {...:,.2f} €".replace(",", " "))     # ton indicateur 1
    print()
    print("CA par catégorie :")
    for categorie, total in ca_par_categorie(ventes).items():
        print(f"  {categorie:<16} {total:>12,.2f} €  ({total / ca:.1%})".replace(",", " "))
    print()
    print("Quantité vendue par catégorie :")
    ...                                   # même boucle que ci-dessus avec quantite_par_categorie   (indicateur 2)
    print()
    print("Top 5 produits (quantité vendue) :")
    for rang, (produit, quantite) in enumerate(top_produits(ventes), start=1):
        print(f"  {rang}. {produit:<22} {quantite:>5}")
    print()
    print("Montant d'une vente :")
    ...                                   # une ligne par clé de stats : f"  {nom:<10} {valeur:>10.2f} €"
    print()
    print(f"Meilleur mois : {meilleur_mois} ({mois[meilleur_mois]:,.2f} €)".replace(",", " "))


# --- 5. Point de lancement (fourni) ----------------------------------------------
def main():
    ventes, ecartees = lire_ventes(FICHIER, SEPARATEUR)
    afficher_rapport(VILLE, ventes, ecartees)


if __name__ == "__main__":
    main()
