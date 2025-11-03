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

def gen_gammes():
    return [(f"G{str(i).zfill(2)}", nom) for i, nom in enumerate(GAMMES, start=1)]

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
    """Génère des produits réalistes selon les types d'usines"""
    rows = []
    code = 1
    produits_par_type_usine = n // len(TYPEU)

    for type_usine in TYPEU:
        if type_usine not in PRODUITS_PAR_TYPE:
            continue

        for gamme_nom, produits_base in PRODUITS_PAR_TYPE[type_usine].items():
            codeg = None
            for i, g_nom in enumerate(GAMMES, start=1):
                if g_nom == gamme_nom:
                    codeg = f"G{str(i).zfill(2)}"
                    break

            if not codeg:
                continue

            for produit_base in produits_base:
                if code > n:
                    break

                marques = ["ProLine", "MaisonPro", "BuildX", "Crafto", "Lumina", "AquaFix",
                          "TechMax", "HomeStyle", "PowerTool", "QualityPlus"]

                for i in range(min(3, (n - code + 1))):
                    if code > n:
                        break
                    marque = random.choice(marques)
                    modele = random.randint(100, 999)
                    nom_final = f"{produit_base} {modele}"
                    rows.append((nom_final, marque, codeg))
                    code += 1

    while len(rows) < n:
        nom = f"Produit générique {random.randint(1000, 9999)}"
        marque = random.choice(["Generic", "Standard", "Basic"])
        codeg = f"G{random.randint(1, len(GAMMES)):02d}"
        rows.append((nom, marque, codeg))

    return rows[:n]
