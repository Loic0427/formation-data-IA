"""Brief PY3 — CONTRÔLE (fourni, à ne pas modifier).

Compare ton fichier consolidé à la référence ventes_consolidees.csv, filtrée sur
tes deux villes : même nombre de lignes et même CA par ville, au centime.

Lancer :  python controle.py
"""

import csv
from collections import defaultdict
from pathlib import Path

DOSSIER = Path(__file__).parent
MON_FICHIER = DOSSIER / "ventes_consolidees_valenciennes_roubaix.csv"
REFERENCE = DOSSIER / "ventes_consolidees.csv"
VILLES = {"Valenciennes", "Roubaix"}


def resume(chemin, villes=None):
    """Renvoie {ville: (nombre de lignes, CA arrondi au centime)}."""
    lignes = defaultdict(int)
    ca = defaultdict(float)
    with open(chemin, encoding="utf-8", newline="") as fichier:
        for ligne in csv.DictReader(fichier):
            if villes and ligne["ville"] not in villes:
                continue
            lignes[ligne["ville"]] += 1
            ca[ligne["ville"]] += float(ligne["montant"])
    return {ville: (lignes[ville], round(ca[ville], 2)) for ville in lignes}


def main():
    if not MON_FICHIER.exists():
        print(f"Fichier introuvable : {MON_FICHIER.name}. Lance d'abord consolidation.py.")
        return
    if not REFERENCE.exists():
        print(f"Référence introuvable : copie {REFERENCE.name} depuis 99-Brief/Data-Analyst/data/.")
        return

    mien = resume(MON_FICHIER)
    attendu = resume(REFERENCE, VILLES)
    tout_bon = True
    print(f"{'ville':<14} {'lignes':>8} {'attendu':>8}   {'CA':>14} {'attendu':>14}")
    for ville in sorted(VILLES):
        n, total = mien.get(ville, (0, 0.0))
        n_ref, total_ref = attendu.get(ville, (0, 0.0))
        ok = (n == n_ref) and (total == total_ref)
        tout_bon = tout_bon and ok
        print(f"{ville:<14} {n:>8} {n_ref:>8}   {total:>14,.2f} {total_ref:>14,.2f}   {'OK' if ok else 'ÉCART'}".replace(",", " "))
    villes_en_trop = set(mien) - VILLES
    if villes_en_trop:
        tout_bon = False
        print(f"Villes inattendues dans ton fichier : {sorted(villes_en_trop)}")
    print()
    print("CONTRÔLE RÉUSSI : ton fichier est identique à la référence." if tout_bon
          else "CONTRÔLE ÉCHOUÉ : regarde d'abord le renommage de Roubaix, puis les règles du nettoyeur.")


if __name__ == "__main__":
    main()
