# -*- coding: utf-8 -*-
"""
Générateurs de données pour toutes les tables
"""

import random
from config import NOMBRE_EMPLOYES_PAR_POINT_VENTE, NOMBRE_EMPLOYES_PAR_USINE, NOMBRE_POINTS_VENTE, NOMBRE_USINES, PRODUITS_CHANCE_DOUBLE_MARQUE
from constants import *
from utils import getRandomFullName, getRandomPhone, getRandomStreet, getRandomStreetNearby

def gen_employes(n=NOMBRE_EMPLOYES_PAR_USINE * NOMBRE_USINES + NOMBRE_POINTS_VENTE * NOMBRE_EMPLOYES_PAR_POINT_VENTE):
    rows = []
    for code in range(1, n+1):
        fullname = getRandomFullName()
        streetPerso = getRandomStreet()
        streetPro = getRandomStreetNearby(streetPerso)
        rows.append((
            fullname["last_name"], fullname["first_name"], streetPerso["street"], streetPerso["postal_code"], streetPerso["city"],
            streetPro["street"], streetPro["postal_code"], streetPro["city"],
            getRandomPhone("perso"), getRandomPhone("perso")
        ))
    return rows

def gen_qualifs():
    """Génère des qualifications avec des diplômes français (1 par titre)"""
    rows = []
    for niveau in QUALIFICATIONS.keys():
        for q in QUALIFICATIONS[niveau]:
            if len(q) == 4:
                diplome, taux_min, taux_max, base_diplome = q
            else:
                diplome, taux_min, taux_max = q
                base_diplome = diplome
            taux = round(random.uniform(taux_min, taux_max), 2)
            rows.append((diplome, taux, base_diplome))
    return rows

def gen_usines(n=NOMBRE_USINES):
    rows = []
    for code in range(1, n+1):
        street_info = getRandomStreet()
        nom_usine = f"Usine {street_info['city']}"
        rows.append((nom_usine, street_info['street'], street_info['postal_code'], street_info['city'], getRandomPhone("pro")))
    return rows

def gen_typeu():
    return [(nom,) for nom in TYPEU]

def gen_typepv():
    """Génère les types de points de vente"""
    return [(nom,) for nom in PV_TYPES]

def gen_gammes():
    return [(f"G{str(i).zfill(2)}", nom) for i, nom in enumerate(GAMMES, start=1)]

# def gen_points_vente_par_zone():
#     """
#     Génère des points de vente basés sur les zones avec leurs adresses réelles
#     - 1 PV si zone a exactement <= 5 adresses
#     - 2 PV si zone a entre 6 et 9 adresses
#     - 3 PV si zone a 10 adresses ou plus
#     Retourne (rows, adresses_utilisees)
#     """
#     rows = []
#     adresses_utilisees = []
#     pv_counter = 1

#     for zone in ZONES:
#         adresses = ADRESSES_PAR_ZONE[zone]
#         nb_adresses = len(adresses)

#         # Déterminer le nombre de PV selon le nombre d'adresses
#         if nb_adresses <= 5:
#             nb_pv = 1
#         elif 5 < nb_adresses < 10:
#             nb_pv = 2
#         else:  # >= 10
#             nb_pv = 3

#         # Sélectionner des adresses aléatoires pour cette zone
#         adresses_selectionnees = random.sample(adresses, min(nb_pv, nb_adresses))

#         for adresse_complete in adresses_selectionnees:
#             # Parser l'adresse: "12 Rue des Tanneurs, 67000 Strasbourg"
#             parts = adresse_complete.split(", ")
#             if len(parts) == 2:
#                 rue = parts[0]
#                 # Tronquer la rue pour garantir max 50 caractères (limite DB)
#                 rue = rue[:49]  # Utiliser 49 pour être sûr
#                 cp_ville = parts[1].split(" ", 1)
#                 if len(cp_ville) == 2:
#                     cp = cp_ville[0]
#                     ville = cp_ville[1]
#                 else:
#                     cp = cp_ville[0]
#                     ville = "Ville"
#             else:
#                 rue = adresse_complete[:49]  # Tronquer aussi ici à 49
#                 cp = "00000"
#                 ville = "Ville"

#             # Choisir un type de PV (GSB plus probable)
#             type_pv = random.choices(PV_TYPES, weights=[0.6, 0.4])[0]
#             # Choisir un nom réaliste selon le type
#             nom_pv = random.choice(PV_NAMES[type_pv])
#             tel = phone(hg=False)

#             rows.append((nom_pv, rue, cp, ville, tel, type_pv))
#             adresses_utilisees.append({
#                 'zone': zone,
#                 'adresse': adresse_complete,
#                 'type_pv': type_pv,
#                 'nom_pv': nom_pv,
#                 'ville': ville
#             })
#             pv_counter += 1

#     return rows, adresses_utilisees

def gen_points_vente(n=NOMBRE_POINTS_VENTE):
    rows = []
    for code in range(1, n+1):
        street_info = getRandomStreet()
        type_pv = random.choices(PV_TYPES, weights=[0.6, 0.4])[0]
        nom_pv = random.choice(PV_NAMES[type_pv])
        rows.append((
            nom_pv, street_info['street'], street_info['postal_code'], street_info['city'],
            getRandomPhone("pro"),
            type_pv
        ))
    return rows

def gen_produits():
    """
    Génère des produits à partir de la constante PRODUITS et MARQUES.
    Retourne une liste de tuples (nom_produit, marque, code_gamme) pour l'insertion SQL.
    Si la probabilité PRODUITS_CHANCE_DOUBLE_MARQUE est atteinte, un produit peut avoir
    2 ou 3 marques (min 1, max 3). Les marques multiples sont concaténées par une virgule.
    Format: [(NOMP, MARQUEP, CODEG), ...]
    """
    rows = []

    # Créer un mapping des noms de gamme vers leur code (G01, G02, etc.)
    gamme_to_code = {g: f"G{str(i).zfill(2)}" for i, g in enumerate(GAMMES, start=1)}

    # Nombre de variantes par produit (modifiable)
    NB_VARIANTS_MIN = 2
    NB_VARIANTS_MAX = 4

    for nom_produit, gamme_nom, type_usine, composants in PRODUITS:
        codeg = gamme_to_code.get(gamme_nom)
        if not codeg:
            print(f"Attention: Gamme '{gamme_nom}' non trouvée pour le produit '{nom_produit}'")
            continue

        marques_disponibles = MARQUES.get(gamme_nom, ["Generic"])
        nb_variants = random.randint(NB_VARIANTS_MIN, NB_VARIANTS_MAX)

        used_marques = set()
        tries = 0
        max_tries = nb_variants * 4  # avoid infinite loop if not enough unique combinations
        while len(used_marques) < nb_variants and tries < max_tries:
            tries += 1
            # Always select only one brand
            marque = random.choice(marques_disponibles)
            if marque in used_marques:
                continue
            used_marques.add(marque)
            modele = random.randint(100, 999)
            nom_final = f"{nom_produit}"
            rows.append((nom_final, marque, codeg))

    return rows
