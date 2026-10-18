"""Analyse d'un export de ventes d'un magasin NordRetail.

EXEMPLE À IMITER (magasin de Tourcoing). Lancer depuis ce dossier :

    python analyse_magasin_exemple.py

Le script lit le CSV, écarte les lignes non conformes, puis affiche un rapport :
chiffre d'affaires, répartition par catégorie, produits les plus vendus,
statistiques du montant d'une vente et mois le plus fort.
"""

import csv
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

# --- Paramètres : ce qui change d'un magasin à l'autre -----------------------
FICHIER = Path(__file__).parent / "ventes_tourcoing.csv"
VILLE = "Tourcoing"
SEPARATEUR = ","


# --- Lecture et règles de conformité -----------------------------------------
def lire_ventes(chemin, separateur=","):
    """Lit le CSV et renvoie (liste de ventes typées, nombre de lignes écartées).

    Une ligne est écartée si une valeur est absente ou mal formée (date, nombre),
    ou si la quantité ou le montant n'est pas strictement positif.
    """
    ventes = []
    ecartees = 0
    with open(chemin, encoding="utf-8", newline="") as fichier:
        for ligne in csv.DictReader(fichier, delimiter=separateur):
            try:
                vente = {
                    "date": datetime.strptime(ligne["date"], "%Y-%m-%d").date(),
                    "categorie": ligne["categorie"].strip(),
                    "produit": ligne["produit"].strip(),
                    "quantite": int(ligne["quantite"]),
                    "montant": float(ligne["montant"]),
                }
            except (KeyError, ValueError):      # colonne absente ou valeur mal formée
                ecartees += 1
                continue
            if vente["quantite"] <= 0 or vente["montant"] <= 0:
                ecartees += 1
                continue
            ventes.append(vente)
    return ventes, ecartees


# --- Indicateurs : une fonction = un indicateur --------------------------------
def chiffre_affaires(ventes):
    """Somme des montants."""
    return sum(v["montant"] for v in ventes)


def ca_par_categorie(ventes):
    """Dict {catégorie: CA}, trié du plus gros au plus petit CA."""
    totaux = defaultdict(float)
    for v in ventes:
        totaux[v["categorie"]] += v["montant"]
    return dict(sorted(totaux.items(), key=lambda item: item[1], reverse=True))


def top_produits(ventes, n=5):
    """Les n produits les plus vendus en quantité : liste de (produit, quantité)."""
    compteur = Counter()
    for v in ventes:
        compteur[v["produit"]] += v["quantite"]
    return compteur.most_common(n)


def statistiques_montant(ventes):
    """Position et dispersion du montant d'une vente."""
    montants = [v["montant"] for v in ventes]
    return {
        "moyenne": statistics.mean(montants),
        "mediane": statistics.median(montants),
        "ecart_type": statistics.stdev(montants),
        "minimum": min(montants),
        "maximum": max(montants),
    }


def ca_par_mois(ventes):
    """Dict {'AAAA-MM': CA} dans l'ordre chronologique."""
    totaux = defaultdict(float)
    for v in ventes:
        cle = v["date"].strftime("%Y-%m")
        totaux[cle] += v["montant"]
    return dict(sorted(totaux.items()))


# --- Rapport --------------------------------------------------------------------
def afficher_rapport(ville, ventes, ecartees):
    ca = chiffre_affaires(ventes)
    stats = statistiques_montant(ventes)
    mois = ca_par_mois(ventes)
    meilleur_mois = max(mois, key=mois.get)

    print(f"=== Rapport {ville} ===")
    print(f"Lignes conformes : {len(ventes):,} | écartées : {ecartees}".replace(",", " "))
    print(f"Période : du {min(v['date'] for v in ventes):%d/%m/%Y} au {max(v['date'] for v in ventes):%d/%m/%Y}")
    print(f"Chiffre d'affaires : {ca:,.2f} €".replace(",", " "))
    print()
    print("CA par catégorie :")
    for categorie, total in ca_par_categorie(ventes).items():
        print(f"  {categorie:<16} {total:>12,.2f} €  ({total / ca:.1%})".replace(",", " "))
    print()
    print("Top 5 produits (quantité vendue) :")
    for rang, (produit, quantite) in enumerate(top_produits(ventes), start=1):
        print(f"  {rang}. {produit:<22} {quantite:>5}")
    print()
    print("Montant d'une vente :")
    for nom, valeur in stats.items():
        print(f"  {nom:<10} {valeur:>10.2f} €")
    print()
    print(f"Meilleur mois : {meilleur_mois} ({mois[meilleur_mois]:,.2f} €)".replace(",", " "))


def main():
    ventes, ecartees = lire_ventes(FICHIER, SEPARATEUR)
    afficher_rapport(VILLE, ventes, ecartees)


if __name__ == "__main__":      # point de lancement : exécuté seulement avec `python fichier.py`
    main()
