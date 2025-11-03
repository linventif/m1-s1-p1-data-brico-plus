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
    """Génère des qualifications avec des diplômes français réalistes"""
    # Postes avec niveau de qualification requis et fourchettes salariales (€/h)
    qualifications = [
        # Niveau 3 (CAP, BEP) - 11€ à 15€/h
        ("CAP Vendeur", 3, (11.0, 15.0)),
        ("CAP Magasinier", 3, (11.5, 14.5)),
        ("CAP Électricien", 3, (12.0, 16.0)),
        ("CAP Plombier", 3, (12.0, 16.0)),
        ("CAP Carreleur", 3, (12.0, 16.0)),
        ("CAP Peintre", 3, (11.5, 15.5)),
        ("BEP Logistique", 3, (11.5, 14.5)),
        ("CAP Menuisier", 3, (12.0, 15.5)),

        # Niveau 4 (Bac, BP) - 13€ à 18€/h
        ("Bac Pro Commerce", 4, (13.0, 17.0)),
        ("Bac Pro Logistique", 4, (13.5, 17.5)),
        ("BP Électricien", 4, (14.0, 18.0)),
        ("BP Plombier", 4, (14.0, 18.0)),
        ("Bac Pro Maintenance", 4, (13.5, 17.5)),
        ("Bac Gestion Administration", 4, (13.0, 16.5)),

        # Niveau 5 (BTS, DUT) - 15€ à 22€/h
        ("BTS Management", 5, (15.0, 20.0)),
        ("BTS Comptabilité", 5, (15.5, 21.0)),
        ("DUT Logistique", 5, (16.0, 21.0)),
        ("BTS Technico-commercial", 5, (15.5, 20.5)),
        ("BTS Maintenance industrielle", 5, (16.0, 22.0)),
        ("DUT Qualité", 5, (15.5, 21.0)),
        ("BTS Assistant de gestion", 5, (15.0, 19.5)),

        # Niveau 6 (Licence, BUT) - 18€ à 26€/h
        ("Licence Pro Commerce", 6, (18.0, 24.0)),
        ("BUT Gestion logistique", 6, (18.5, 25.0)),
        ("Licence Pro RH", 6, (18.0, 24.0)),
        ("BUT Qualité logistique", 6, (18.5, 24.5)),
        ("Licence Gestion", 6, (18.0, 23.5)),

        # Niveau 7 (Master, Ingénieur) - 22€ à 35€/h
        ("Master Management", 7, (22.0, 30.0)),
        ("Master RH", 7, (22.0, 30.0)),
        ("Master Finance", 7, (23.0, 32.0)),
        ("Diplôme Ingénieur", 7, (24.0, 35.0)),
        ("Master Logistique", 7, (22.0, 29.0)),
        ("Master Qualité", 7, (22.0, 30.0)),
    ]

    rows = []
    for i in range(n):
        # Choisit une qualification aléatoire
        nom_base, niveau, (taux_min, taux_max) = random.choice(qualifications)

        # Ajoute une variation au nom pour plus de diversité
        variation = random.randint(1, 3)
        nom = f"{nom_base} N{niveau}" if variation == 1 else nom_base

        # Génère un taux horaire dans la fourchette appropriée
        taux = round(random.uniform(taux_min, taux_max), 2)

        rows.append((nom, taux, None))

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
