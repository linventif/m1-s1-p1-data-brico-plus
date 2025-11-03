# -*- coding: utf-8 -*-
"""
Générateurs de données pour toutes les tables
"""

import random
from constants import *
from utils import phone, pick_city, street

def gen_employes(n=N_EMP):
    rows = []
    for code in range(1, n+1):
        nom = random.choice([
            "Martin", "Bernard", "Thomas", "Petit", "Robert", "Richard", "Durand", "Dubois",
            "Moreau", "Laurent", "Simon", "Michel", "Lefebvre", "Leroy", "Roux", "David", "Foxy"
        ])
        prenom = random.choice([
            "Lucas", "Louis", "Hugo", "Arthur", "Jules", "Adam", "Léo", "Noah",
            "Emma", "Louise", "Chloé", "Lina", "Mia", "Anna", "Zoé", "Léa"
        ])
        vpers, cppers = pick_city(True)
        vpro, cppro = pick_city(True)
        rows.append((
            nom, prenom,
            street(), cppers, vpers,
            street(), cppro, vpro,
            phone(hg=True), phone(hg=True)
        ))
    return rows

def gen_qualifs(n=N_QUALIF):
    """Génère des qualifications avec des diplômes français (1 par titre)"""
    rows = []
    for niveau in QUALIFICATIONS.keys():
        for diplome, taux_min, taux_max in QUALIFICATIONS[niveau]:
            taux = round(random.uniform(taux_min, taux_max), 2)
            rows.append((diplome, taux, None))
    return rows

def gen_usines(n=N_USINES):
    rows = []
    for code in range(1, n+1):
        city, cp = pick_city(True)
        nom_usine = f"Usine {city} {code}"
        rows.append((nom_usine, street(), cp, city, phone(hg=cp.startswith("31"))))
    return rows

def gen_typeu():
    return [(nom,) for nom in TYPEU]

def gen_typepv():
    """Génère les types de points de vente"""
    return [(nom,) for nom in PV_TYPES]

def gen_gammes():
    return [(f"G{str(i).zfill(2)}", nom) for i, nom in enumerate(GAMMES, start=1)]

def gen_points_vente_par_zone():
    """
    Génère des points de vente basés sur les zones avec leurs adresses réelles
    - 1 PV si zone a exactement <= 5 adresses
    - 2 PV si zone a entre 6 et 9 adresses
    - 3 PV si zone a 10 adresses ou plus
    Retourne (rows, adresses_utilisees)
    """
    rows = []
    adresses_utilisees = []
    pv_counter = 1

    for zone in ZONES:
        adresses = ADRESSES_PAR_ZONE[zone]
        nb_adresses = len(adresses)

        # Déterminer le nombre de PV selon le nombre d'adresses
        if nb_adresses <= 5:
            nb_pv = 1
        elif 5 < nb_adresses < 10:
            nb_pv = 2
        else:  # >= 10
            nb_pv = 3

        # Sélectionner des adresses aléatoires pour cette zone
        adresses_selectionnees = random.sample(adresses, min(nb_pv, nb_adresses))

        for adresse_complete in adresses_selectionnees:
            # Parser l'adresse: "12 Rue des Tanneurs, 67000 Strasbourg"
            parts = adresse_complete.split(", ")
            if len(parts) == 2:
                rue = parts[0]
                # Tronquer la rue pour garantir max 50 caractères (limite DB)
                rue = rue[:49]  # Utiliser 49 pour être sûr
                cp_ville = parts[1].split(" ", 1)
                if len(cp_ville) == 2:
                    cp = cp_ville[0]
                    ville = cp_ville[1]
                else:
                    cp = cp_ville[0]
                    ville = "Ville"
            else:
                rue = adresse_complete[:49]  # Tronquer aussi ici à 49
                cp = "00000"
                ville = "Ville"

            # Choisir un type de PV (GSB plus probable)
            type_pv = random.choices(PV_TYPES, weights=[0.6, 0.4])[0]
            # Choisir un nom réaliste selon le type
            nom_pv = random.choice(PV_NAMES[type_pv])
            tel = phone(hg=False)

            rows.append((nom_pv, rue, cp, ville, tel, type_pv))
            adresses_utilisees.append({
                'zone': zone,
                'adresse': adresse_complete,
                'type_pv': type_pv,
                'nom_pv': nom_pv,
                'ville': ville
            })
            pv_counter += 1

    return rows, adresses_utilisees

def gen_points_vente(n=N_PV):
    rows = []
    for code in range(1, n+1):
        city, cp = pick_city(True)
        nompv = random.choices(PV_TYPES, weights=[0.6, 0.4])[0]
        rows.append((
            nompv,
            street(), cp, city, phone(hg=cp.startswith("31")),
            f"Type {nompv}"))
    return rows

def gen_produits(n=N_PRODUITS):
    """Génère des produits réalistes à partir des recettes"""
    rows = []
    code = 1

    marques = ["ProLine", "MaisonPro", "BuildX", "Crafto", "Lumina", "AquaFix",
              "TechMax", "HomeStyle", "PowerTool", "QualityPlus"]

    # Pour chaque recette, générer plusieurs variantes avec des modèles différents
    for nom_produit, gamme_nom, type_usine in RECETTES_PRODUITS:
        if code > n:
            break

        # Trouver le code de la gamme
        codeg = None
        for i, g_nom in enumerate(GAMMES, start=1):
            if g_nom == gamme_nom:
                codeg = f"G{str(i).zfill(2)}"
                break

        if not codeg:
            continue

        # Générer 2-3 variantes du produit avec différentes marques et modèles
        nb_variantes = random.randint(2, 3)
        for i in range(min(nb_variantes, (n - code + 1))):
            if code > n:
                break
            marque = random.choice(marques)
            modele = random.randint(100, 999)
            nom_final = f"{nom_produit} {modele}"
            rows.append((nom_final, marque, codeg))
            code += 1

    # Si on n'a pas assez de produits, générer des produits génériques
    while len(rows) < n:
        nom = f"Produit générique {random.randint(1000, 9999)}"
        marque = random.choice(["Generic", "Standard", "Basic"])
        codeg = f"G{random.randint(1, len(GAMMES)):02d}"
        rows.append((nom, marque, codeg))

    return rows[:n]
