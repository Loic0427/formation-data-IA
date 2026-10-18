"""Génère deux quiz Kahoot (format d'import officiel) pour le parcours Data Analyst :
- Kahoot_DataAnalyst_Maths_25Questions.xlsx : moyenne, médiane, quartiles, écart-type, % (cours 00 à 02)
- Kahoot_DataAnalyst_Git_Bash_25Questions.xlsx : commandes de base (semaine 1), niveau facile
- Kahoot_DataAnalyst_Stats_Metier_30Questions.xlsx : stats descriptives + métier de data analyst (distracteurs humoristiques)
- Kahoot_DataAnalyst_Stats_Metier_30Questions_v2.xlsx : même thème, 30 autres questions

Usage : uv run --with openpyxl python build_kahoot_da.py
Chaque question est écrite avec la BONNE réponse en premier ; le script mélange l'ordre (graine fixe)
et contrôle les limites Kahoot : question ≤ 120 caractères, réponse ≤ 75, durée autorisée.
"""
from pathlib import Path
import random
import shutil

import openpyxl

HERE = Path(__file__).parent
TEMPLATE = HERE / "KahootQuizTemplate.xlsx"
DUREES = {5, 10, 20, 30, 60, 90, 120, 240}

MATHS = [
    ("Quelle est la moyenne de 2, 4 et 6 ?", ["4", "3", "6", "12"], 20),
    ("Quelle est la médiane de 1, 3, 7, 8, 20 ?", ["7", "3", "8", "7,8"], 20),
    ("Quelle est la médiane de 2, 4, 6, 8 ?", ["5", "4", "6", "20"], 30),
    ("Quel est le mode de 3, 5, 5, 7, 9 ?", ["5", "3", "7", "9"], 20),
    ("Quel indicateur ne bouge presque pas si on ajoute une valeur énorme ?", ["La médiane", "La moyenne", "L'étendue", "L'écart-type"], 20),
    ("La moyenne est bien plus grande que la médiane. La distribution est…", ["Étalée à droite", "Symétrique", "Étalée à gauche", "Impossible à dire"], 30),
    ("Quelle est l'étendue de 4, 9, 15, 30 ?", ["26", "30", "15", "34"], 20),
    ("Le 1er quartile (Q1) laisse en dessous de lui…", ["25 % des valeurs", "10 % des valeurs", "50 % des valeurs", "75 % des valeurs"], 20),
    ("La médiane est aussi appelée…", ["Le 2e quartile", "Le 1er quartile", "Le 3e quartile", "Le mode"], 20),
    ("Entre Q1 et Q3, on trouve…", ["La moitié des valeurs", "Toutes les valeurs", "Un quart des valeurs", "Les valeurs extrêmes"], 20),
    ("Que mesure l'écart-type ?", ["La dispersion autour de la moyenne", "Le centre des données", "La valeur la plus fréquente", "Le nombre de valeurs"], 20),
    ("Pour la variance, pourquoi met-on les écarts au carré ?", ["Pour que les + et les − ne s'annulent pas", "Pour aller plus vite", "Pour arrondir", "Pour trier les valeurs"], 30),
    ("L'écart-type est la racine carrée de…", ["La variance", "La moyenne", "La médiane", "L'étendue"], 20),
    ("Série 2, 4, 4, 4, 5, 5, 7, 9 (moyenne 5). Écart-type (divisé par n) ?", ["2", "1", "4", "5"], 60),
    ("Quelle fonction Google Sheets calcule la médiane ?", ["MEDIAN", "AVERAGE", "MODE", "COUNT"], 20),
    ("Que fait la fonction COUNTBLANK (NB.VIDE) ?", ["Elle compte les cellules vides", "Elle compte les nombres", "Elle additionne", "Elle compte les textes"], 20),
    ("La fonction AVERAGE (MOYENNE) ignore les cellules vides.", ["Vrai", "Faux"], 10),
    ("Un prix passe de 50 € à 60 €. Quelle est l'évolution ?", ["+20 %", "+10 %", "+16,7 %", "+60 %"], 30),
    ("Un taux passe de 16 % à 19 %. Il augmente de…", ["3 points", "3 %", "19 %", "16 points"], 30),
    ("30 commandes livrées sur 120. Quelle part est livrée ?", ["25 %", "30 %", "40 %", "12 %"], 20),
    ("Moyenne pondérée de 10 (coefficient 1) et 16 (coefficient 2) ?", ["14", "13", "12", "16"], 60),
    ("Pour comparer des territoires, on pondère souvent par…", ["La population", "La superficie", "L'ordre alphabétique", "Le code postal"], 20),
    ("Quel graphique montre la forme d'une distribution ?", ["L'histogramme", "Le camembert", "La courbe", "La carte"], 20),
    ("Moyenne 1 680 €, médiane 177 €. Pour décrire une commande type, on donne…", ["La médiane", "La moyenne", "Le maximum", "La somme"], 20),
    ("« Note moyenne de nos 613 commandes : 4,1 » alors que 560 sont notées. Le souci ?", ["Le périmètre est faux", "Le calcul est faux", "4,1 est trop haut", "Aucun"], 30),
]

GIT_BASH = [
    ("Quelle commande affiche le dossier dans lequel tu te trouves ?", ["pwd", "ls", "cd", "mkdir"], 20),
    ("Quelle commande liste les fichiers d'un dossier ?", ["ls", "cd", "rm", "cat"], 20),
    ("Que fait la commande « cd .. » ?", ["Elle remonte d'un dossier", "Elle supprime un dossier", "Elle crée un dossier", "Elle liste les fichiers"], 20),
    ("Comment créer un dossier nommé data ?", ["mkdir data", "touch data", "cd data", "rm data"], 20),
    ("Comment créer un fichier vide notes.txt ?", ["touch notes.txt", "mkdir notes.txt", "ls notes.txt", "pwd notes.txt"], 20),
    ("Quelle commande affiche le contenu d'un fichier texte ?", ["cat", "cd", "mkdir", "pwd"], 20),
    ("Que fait « rm fichier.txt » ?", ["Il supprime le fichier", "Il renomme le fichier", "Il copie le fichier", "Il ouvre le fichier"], 20),
    ("Comment copier a.txt vers b.txt ?", ["cp a.txt b.txt", "mv a.txt b.txt", "rm a.txt b.txt", "cat a.txt b.txt"], 20),
    ("Quelle commande renomme ou déplace un fichier ?", ["mv", "cp", "ls", "rm"], 20),
    ("Dans le terminal, que désigne le symbole ~ ?", ["Ton dossier personnel", "La racine du disque", "Le dossier parent", "Un fichier caché"], 20),
    ("Quelle touche complète automatiquement un nom de fichier ?", ["Tab", "Entrée", "Échap", "Espace"], 10),
    ("Git, c'est…", ["Un logiciel de gestion de versions", "Un langage de programmation", "Un réseau social", "Un tableur"], 20),
    ("GitHub, c'est…", ["Un site qui héberge des dépôts Git", "Le même logiciel que Git", "Un éditeur de texte", "Un navigateur web"], 20),
    ("Quelle commande crée un dépôt Git dans le dossier courant ?", ["git init", "git start", "git new", "git create"], 20),
    ("Quelle commande montre les fichiers modifiés ?", ["git status", "git log", "git push", "git clone"], 20),
    ("Quelle commande prépare un fichier pour le prochain commit ?", ["git add", "git commit", "git push", "git pull"], 20),
    ("Comment enregistrer une version avec un message ?", ['git commit -m "message"', 'git save "message"', 'git add -m "message"', 'git push "message"'], 30),
    ("Quelle commande envoie tes commits sur GitHub ?", ["git push", "git pull", "git init", "git status"], 20),
    ("Quelle commande récupère les nouveautés depuis GitHub ?", ["git pull", "git push", "git add", "git commit"], 20),
    ("Comment copier un dépôt GitHub sur ton ordinateur ?", ["git clone", "git copy", "git download", "git init"], 20),
    ("Quelle commande affiche l'historique des commits ?", ["git log", "git status", "git history", "git show-all"], 20),
    ("Un bon message de commit…", ["Dit ce que fait le commit", "Tient en un mot : « modifs »", "Est vide", "Contient seulement la date"], 20),
    ("À quoi sert le fichier .gitignore ?", ["Lister les fichiers à ne pas versionner", "Cacher le dépôt", "Supprimer des fichiers", "Écrire la documentation"], 30),
    ("Que présente le fichier README.md d'un dépôt ?", ["Le projet et comment l'utiliser", "Les mots de passe", "L'historique des commits", "La liste des branches"], 20),
    ("À quoi sert une branche Git ?", ["Travailler sur une version parallèle", "Supprimer le dépôt", "Envoyer un e-mail", "Trier les fichiers"], 20),
]


STATS_METIER = [
    # --- Le métier de data analyst (17) ---
    ("Quel logiciel un data analyst utilise-t-il pour créer des tableaux de bord ?", ["Power BI", "Morpion", "Paint", "Minecraft"], 20),
    ("Quel langage sert à interroger une base de données ?", ["SQL", "Le morse", "Le latin", "HTML"], 20),
    ("Quel langage de programmation est le plus utilisé par les data analysts ?", ["Python", "Le klingon", "Scratch", "Fortran 77"], 20),
    ("Quel outil Google permet de faire des tableaux de bord gratuitement ?", ["Looker Studio", "Google Maps", "Gmail", "YouTube"], 20),
    ("Quel format de fichier texte stocke des données séparées par des virgules ?", ["CSV", "MP3", "JPEG", "GIF"], 20),
    ("Quelle bibliothèque Python sert à manipuler des tableaux de données ?", ["pandas", "pingouins", "Tetris", "Wordle"], 20),
    ("Que signifie KPI ?", ["Key Performance Indicator", "Kebab Pizza Intégral", "Keep Playing Immediately", "Kilo Par Instant"], 30),
    ("Que fait un data analyst en premier quand il reçoit une demande ?", ["Il clarifie le besoin métier", "Il fait un camembert 3D", "Il envoie un mail à tout le monde", "Il achète un nouvel écran"], 30),
    ("Que veut dire « nettoyer les données » ?", ["Corriger doublons, vides et erreurs", "Passer l'éponge sur l'écran", "Supprimer toutes les lignes", "Mettre les chiffres en gras"], 30),
    ("Un dashboard, c'est…", ["Un tableau de bord d'indicateurs", "Un tableau de bord de voiture", "Une planche de skate", "Un jeu de société"], 20),
    ("Que signifie BI ?", ["Business Intelligence", "Bureau Indépendant", "Big Internet", "Bière Intégrale"], 20),
    ("À qui un data analyst présente-t-il ses résultats ?", ["Aux décideurs métier", "À son chat", "À personne, c'est secret", "Au robot aspirateur"], 20),
    ("Quel outil versionne le code et les scripts d'un analyste ?", ["Git", "Une clé USB", "Un post-it", "Une photocopieuse"], 20),
    ("Quel graphique évite-t-on pour comparer 12 catégories ?", ["Le camembert", "Le diagramme en barres", "Le tableau", "Le nuage de points"], 30),
    ("Les étapes d'une analyse : collecter, puis…", ["Nettoyer, analyser, restituer", "Restituer, analyser, nettoyer", "Dormir, analyser, restituer", "Analyser, collecter, nettoyer"], 30),
    ("Le RGPD protège…", ["Les données personnelles", "Les recettes de cuisine", "Les fichiers Excel", "Les mots de passe Wi-Fi"], 20),
    ("Tableau, Power BI et Looker Studio sont des outils de…", ["Data visualisation", "Montage vidéo", "Jeux vidéo", "Retouche photo"], 20),
    # --- Statistiques descriptives (13) ---
    ("Laquelle est une variable qualitative ?", ["La couleur des yeux", "La taille en cm", "Le salaire", "L'âge"], 20),
    ("Quelle est la moyenne de 10, 20, 30, 40 ?", ["25", "30", "20", "100"], 20),
    ("Médiane de 5, 1, 9, 3, 7 (attention, la série n'est pas triée) ?", ["5", "9", "1", "3"], 30),
    ("Mode de « bleu, vert, bleu, rouge, bleu » ?", ["Bleu", "Vert", "Rouge", "Il n'y en a pas"], 20),
    ("Un « outlier » (valeur aberrante), c'est…", ["Une valeur très éloignée des autres", "Une valeur en anglais", "Une valeur vide", "La valeur du milieu"], 20),
    ("Q1 = 50 et Q3 = 80. L'écart interquartile vaut…", ["30", "130", "65", "80"], 30),
    ("Un écart-type de 0 signifie…", ["Toutes les valeurs sont identiques", "Il y a une erreur", "La moyenne vaut 0", "Il n'y a aucune valeur"], 30),
    ("Même moyenne 12, écarts-types 1 et 5. Quelle classe est la plus homogène ?", ["Celle avec l'écart-type 1", "Celle avec l'écart-type 5", "Les deux", "Impossible à dire"], 30),
    ("3 ventes sur 4 sont livrées. En pourcentage ?", ["75 %", "34 %", "43 %", "25 %"], 20),
    ("Un salaire passe de 2 000 € à 2 100 €. Évolution ?", ["+5 %", "+10 %", "+100 %", "+1 %"], 30),
    ("Le minimum est 10, le maximum est 50. L'étendue vaut…", ["40", "60", "30", "50"], 20),
    ("Quel graphique montre la médiane, Q1, Q3 et les extrêmes ?", ["La boîte à moustaches", "Le camembert", "La courbe", "Le nuage de points"], 20),
    ("« 4,5 enfants par foyer en moyenne » signifie…", ["Une valeur calculée, pas un vrai foyer", "Qu'un foyer a 4,5 enfants", "Une erreur de calcul", "Que la médiane est 4,5"], 30),
]


STATS_METIER_2 = [
    # --- Le métier de data analyst (15) ---
    ("Quel outil de Power BI sert à nettoyer et transformer les données ?", ["Power Query", "Power Point", "Power Rangers", "Power Nap"], 20),
    ("Quel langage de formules utilise Power BI ?", ["DAX", "DOX", "LOL", "ABBA"], 20),
    ("Dans Excel, quel outil résume un grand tableau en quelques clics ?", ["Le tableau croisé dynamique", "Le tableau périodique", "La chaise croisée", "Le tableau de Picasso"], 20),
    ("Quel outil open source crée des tableaux de bord sur une base SQL ?", ["Metabase", "Metaverse", "Métro", "Météo France"], 20),
    ("Quel outil permet d'écrire du code Python et du texte dans le même document ?", ["Jupyter", "Saturne", "Bloc-notes", "Word"], 20),
    ("Que signifie ETL ?", ["Extract, Transform, Load", "Écrire Toujours Lentement", "Excel Tableau Looker", "Envoyer Tout Lundi"], 30),
    ("Un graphique montre une chute de 40 % des ventes. Le data analyst…", ["Vérifie la donnée avant d'alerter", "Publie sur LinkedIn", "Supprime la ligne", "Ferme l'ordinateur"], 30),
    ("Un « doublon », c'est…", ["Une ligne présente deux fois", "Un double café", "Une colonne vide", "Un graphique en deux couleurs"], 20),
    ("Que signifie NULL dans une base de données ?", ["Une valeur absente", "Zéro", "Une insulte", "Le texte « null »"], 20),
    ("Un bon titre de graphique…", ["Dit le message clé", "Dit « Graphique 1 »", "Est en Comic Sans", "Est absent"], 20),
    ("Le data analyst documente son travail pour…", ["Que d'autres le comprennent et le refassent", "Faire joli", "Gagner du temps de pause", "Personne"], 20),
    ("Quel format échange des données entre applications web ?", ["JSON", "JASON", "JPEG", "JOJO"], 20),
    ("Lequel n'est PAS un métier de la data ?", ["Data Sommelier", "Data Analyst", "Data Engineer", "Data Scientist"], 20),
    ("Que fait le data engineer pour le data analyst ?", ["Il construit les pipelines de données", "Il conduit les trains", "Il répare les écrans", "Il fait les cafés"], 20),
    ("Pour montrer une évolution dans le temps, on utilise…", ["Une courbe", "Un camembert", "Un tableau", "Une carte"], 20),
    # --- Statistiques descriptives (15) ---
    ("Moyenne de 3, 3, 3, 3 ?", ["3", "12", "9", "0"], 10),
    ("Moyenne de 0, 0, 0, 100 ?", ["25", "100", "0", "50"], 20),
    ("Sur 0, 0, 0, 100, la médiane vaut…", ["0", "25", "50", "100"], 20),
    ("Une série peut avoir plusieurs modes.", ["Vrai", "Faux"], 10),
    ("Le mode s'applique aussi aux variables qualitatives (ex. : couleur).", ["Vrai", "Faux"], 10),
    ("Un salaire au 9e décile (D9) est…", ["Plus haut que 90 % des salaires", "Plus bas que 90 % des salaires", "Égal à la moyenne", "Égal à la médiane"], 30),
    ("Le coefficient de variation, c'est…", ["Écart-type ÷ moyenne", "Moyenne ÷ écart-type", "Max − min", "Q3 − Q1"], 30),
    ("Q1 = 10, Q3 = 30. Une valeur de 70 est…", ["Probablement aberrante (> Q3 + 1,5 × IQR)", "Normale", "La médiane", "Le mode"], 60),
    ("Variance de 2, 4, 6 (moyenne 4, divisé par n) ?", ["8/3 ≈ 2,67", "4", "2", "0"], 60),
    ("Dans une distribution symétrique…", ["Moyenne ≈ médiane", "Moyenne >> médiane", "Moyenne << médiane", "Il n'y a pas de médiane"], 20),
    ("40 « oui » sur 200 réponses. Fréquence relative ?", ["20 %", "40 %", "5 %", "0,4 %"], 20),
    ("Un histogramme représente…", ["Une variable quantitative continue", "Une liste de noms", "Des couleurs", "Un tableau croisé"], 20),
    ("« L'entreprise a doublé ses ventes. » En pourcentage ?", ["+100 %", "+200 %", "+50 %", "+2 %"], 30),
    ("Note moyenne de 4/5 avec seulement 2 avis. C'est…", ["Peu fiable, trop peu d'avis", "Très fiable", "Une note parfaite", "Impossible"], 20),
    ("Quelle fonction Google Sheets calcule l'écart-type ?", ["STDEV", "ECART", "SIGMA", "AVERAGE"], 20),
]


def construire(questions, nom, graine, nb=25):
    assert len(questions) == nb, (nom, len(questions))
    rnd = random.Random(graine)
    dest = HERE / nom
    shutil.copy(TEMPLATE, dest)
    wb = openpyxl.load_workbook(dest)
    ws = wb.active
    positions = []
    for i, (q, reps, duree) in enumerate(questions):
        assert len(q) <= 120, (q, len(q))
        assert all(len(r) <= 75 for r in reps), reps
        assert duree in DUREES
        bonne = reps[0]
        ordre = reps[:]
        if len(ordre) == 4:
            rnd.shuffle(ordre)
        r = 9 + i
        ws.cell(r, 1, i + 1)
        ws.cell(r, 2, q)
        for j in range(4):
            ws.cell(r, 3 + j, ordre[j] if j < len(ordre) else None)
        ws.cell(r, 7, duree)
        ws.cell(r, 8, str(ordre.index(bonne) + 1))
        positions.append(ordre.index(bonne) + 1)
    wb.save(dest)
    print(f"{nom} : {nb} questions · bonnes réponses en position 1/2/3/4 : "
          f"{[positions.count(k) for k in (1, 2, 3, 4)]}")


construire(MATHS, "Kahoot_DataAnalyst_Maths_25Questions.xlsx", 11)
construire(GIT_BASH, "Kahoot_DataAnalyst_Git_Bash_25Questions.xlsx", 22)
construire(STATS_METIER, "Kahoot_DataAnalyst_Stats_Metier_30Questions.xlsx", 33, nb=30)
construire(STATS_METIER_2, "Kahoot_DataAnalyst_Stats_Metier_30Questions_v2.xlsx", 44, nb=30)
