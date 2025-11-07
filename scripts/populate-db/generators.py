# -*- coding: utf-8 -*-
"""
Générateurs de données pour toutes les tables
"""

import random
from config import (
    NOMBRE_USINES, NOMBRE_POINTS_VENTE,
    FACTORY_SPECIALIZED_MIN, FACTORY_SPECIALIZED_MAX,
    FACTORY_SEMI_SPECIALIZED_MIN, FACTORY_SEMI_SPECIALIZED_MAX,
    FACTORY_GENERAL_MIN, FACTORY_GENERAL_MAX,
    PV_EXPRESS_MIN, PV_EXPRESS_MAX,
    PV_GSB_MIN, PV_GSB_MAX,
    PV_EXPRESS_PROBABILITY,
    PRODUITS_VARIANTS_MIN, PRODUITS_VARIANTS_MAX,
    DUAL_WORKPLACE_PERCENTAGE
)
from constants import *
from utils import getRandomFullName, getRandomPhone, getRandomStreet, getRandomStreetNearby
from string_utils import truncate_to_bytes

def gen_employes(n=None):
    """Legacy function - use gen_employes_by_factory_size instead"""
    if n is None:
        n = 1000  # Default fallback
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

def gen_employes_by_factory_size(factory_info, pv_info):
    """
    Generate employees based on factory size classification and point of sale types.
    - Factory employees: based on factory_info taille
    - PV employees: 8-15 for Brico-Express, 75-150 for GSB
    - Configurable % of employees work at both a factory AND a point of sale (DUAL_WORKPLACE_PERCENTAGE)
    - Professional address is near their workplace

    Parameters:
    - factory_info: dict with factory_id -> {classification, taille, types, address}
    - pv_info: list of tuples (codepv, type_pv, address_info)

    Returns: (list of employee tuples, list of workplace assignments)
    """
    rows = []
    employee_workplace = []  # Track where each employee works (can be list of workplaces)

    print("\n" + "=" * 60)
    print("=== GENERATING EMPLOYEES ===")
    print("=" * 60)

    # Generate factory employees
    total_factory = sum(info['taille'] for info in factory_info.values())
    print(f"\n📍 Generating {total_factory} factory employees...")

    factory_count = 0
    for factory_id, info in factory_info.items():
        factory_address = info.get('address')
        num_employees = info['taille']

        for i in range(num_employees):
            fullname = getRandomFullName()
            streetPerso = getRandomStreet()
            # Professional address near factory
            if factory_address:
                streetPro = getRandomStreetNearby(factory_address)
            else:
                streetPro = getRandomStreetNearby(streetPerso)

            # Limit all strings to match database constraints (byte-aware for UTF-8)
            rows.append((
                truncate_to_bytes(fullname["last_name"], 50),
                truncate_to_bytes(fullname["first_name"], 50),
                truncate_to_bytes(streetPerso["street"], 50),
                truncate_to_bytes(streetPerso["postal_code"], 5),
                truncate_to_bytes(streetPerso["city"], 50),
                truncate_to_bytes(streetPro["street"], 50),
                truncate_to_bytes(streetPro["postal_code"], 5),
                truncate_to_bytes(streetPro["city"], 50),
                truncate_to_bytes(getRandomPhone("perso"), 10),
                truncate_to_bytes(getRandomPhone("pro"), 10)
            ))
            employee_workplace.append([('factory', factory_id)])

            factory_count += 1
            if factory_count % 500 == 0:
                print(f"  ├─ Progress: {factory_count}/{total_factory} factory employees")

    print(f"  ✓ Completed: {factory_count} factory employees")

    # Generate point of sale employees
    print(f"\n🏪 Generating point of sale employees...")
    pv_count = 0

    for codepv, pv_data in pv_info.items():
        # Determine number of employees based on type
        is_express = pv_data['is_express']
        if is_express:
            num_employees = random.randint(PV_EXPRESS_MIN, PV_EXPRESS_MAX)
        else:  # GSB
            num_employees = random.randint(PV_GSB_MIN, PV_GSB_MAX)

        # Get address info for nearby professional address
        pv_address = {
            'postal_code': pv_data['postal_code'],
            'city': pv_data['city']
        }

        for _ in range(num_employees):
            fullname = getRandomFullName()
            streetPerso = getRandomStreet()
            # Professional address near point of sale
            streetPro = getRandomStreetNearby(pv_address)

            # Limit all strings to match database constraints (byte-aware for UTF-8)
            rows.append((
                truncate_to_bytes(fullname["last_name"], 50),
                truncate_to_bytes(fullname["first_name"], 50),
                truncate_to_bytes(streetPerso["street"], 50),
                truncate_to_bytes(streetPerso["postal_code"], 5),
                truncate_to_bytes(streetPerso["city"], 50),
                truncate_to_bytes(streetPro["street"], 50),
                truncate_to_bytes(streetPro["postal_code"], 5),
                truncate_to_bytes(streetPro["city"], 50),
                truncate_to_bytes(getRandomPhone("perso"), 10),
                truncate_to_bytes(getRandomPhone("pro"), 10)
            ))
            employee_workplace.append([('pv', codepv)])

            pv_count += 1
            if pv_count % 500 == 0:
                print(f"  ├─ Progress: {pv_count} PV employees")

    print(f"  ✓ Completed: {pv_count} PV employees")

    # Assign dual workplace employees based on configuration
    total_employees = len(rows)
    num_dual_workers = max(0, int(total_employees * DUAL_WORKPLACE_PERCENTAGE))

    if num_dual_workers > 0:
        print(f"\n👥 Assigning {num_dual_workers} employees ({DUAL_WORKPLACE_PERCENTAGE*100:.1f}%) to dual workplaces (factory + PV)...")

        # Get available factories and PVs
        available_factories = list(factory_info.keys())
        available_pvs = list(pv_info.keys())

        # Randomly select employees to have dual assignments
        dual_worker_indices = random.sample(range(total_employees), num_dual_workers)

        for idx in dual_worker_indices:
            current_workplace = employee_workplace[idx]

            # If currently only factory, add a random PV
            if current_workplace[0][0] == 'factory':
                random_pv = random.choice(available_pvs)
                current_workplace.append(('pv', random_pv))
            # If currently only PV, add a random factory
            elif current_workplace[0][0] == 'pv':
                random_factory = random.choice(available_factories)
                current_workplace.append(('factory', random_factory))

        print(f"  ✓ Completed: {num_dual_workers} dual workplace assignments")
    else:
        print(f"\n👥 Dual workplace feature disabled (DUAL_WORKPLACE_PERCENTAGE=0)")

    print("\n" + "=" * 60)
    print(f"✅ Total employees generated: {len(rows)}")
    print(f"   ├─ Factory employees: {factory_count}")
    print(f"   ├─ PV employees: {pv_count}")
    print(f"   └─ Dual workplace employees: {num_dual_workers}")
    print("=" * 60 + "\n")

    return rows, employee_workplace

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
    print(f"\n🏭 Generating {n} factories...")
    for code in range(1, n+1):
        street_info = getRandomStreet()
        nom_usine = f"Usine {street_info['city']}"
        rows.append((
            truncate_to_bytes(nom_usine, 50),
            truncate_to_bytes(street_info['street'], 50),
            truncate_to_bytes(street_info['postal_code'], 5),
            truncate_to_bytes(street_info['city'], 50),
            truncate_to_bytes(getRandomPhone("pro"), 10)
        ))
    print(f"  ✓ Completed: {n} factories")
    return rows

def gen_typeu():
    return [(nom,) for nom in TYPEU]

def gen_typepv():
    """Génère les types de points de vente"""
    return [(nom,) for nom in PV_TYPES]

def gen_gammes():
    return [(f"G{str(i).zfill(2)}", nom) for i, nom in enumerate(GAMMES, start=1)]

def gen_points_vente(n=NOMBRE_POINTS_VENTE):
    rows = []
    pv_info = {}
    print(f"\n🏪 Generating {n} points of sale...")
    for code in range(1, n+1):
        is_express = random.random() < PV_EXPRESS_PROBABILITY
        street_info = getRandomStreet()
        if is_express:
            nom_pv = f"Brico-Express {street_info['city']}"
            type_pv = "Brico-Express"
        else:
            nom_pv = f"GSB {street_info['city']}"
            type_pv = "GSB"

        row = (
            truncate_to_bytes(nom_pv, 50),
            truncate_to_bytes(street_info['street'], 50),
            truncate_to_bytes(street_info['postal_code'], 5),
            truncate_to_bytes(street_info['city'], 50),
            truncate_to_bytes(getRandomPhone("pro"), 10),
            type_pv
        )
        rows.append(row)
        pv_info[code] = {
            'is_express': is_express,
            'postal_code': truncate_to_bytes(street_info['postal_code'], 5),
            'city': street_info['city']
        }

    print(f"  ✓ Completed: {n} points of sale")
    return rows, pv_info

def gen_produits():
    """
    Génère des produits à partir de la constante PRODUITS et MARQUES.
    Retourne une liste de tuples (nom_produit, marque, code_gamme) pour l'insertion SQL.
    Si la probabilité PRODUITS_CHANCE_DOUBLE_MARQUE est atteinte, un produit peut avoir
    2 ou 3 marques (min 1, max 3). Les marques multiples sont concaténées par une virgule.
    Format: [(NOMP, MARQUEP, CODEG), ...]
    """
    rows = []
    print(f"\n📦 Generating products...")

    # Créer un mapping des noms de gamme vers leur code (G01, G02, etc.)
    gamme_to_code = {g: f"G{str(i).zfill(2)}" for i, g in enumerate(GAMMES, start=1)}

    # Nombre de variantes par produit (from config)
    NB_VARIANTS_MIN = PRODUITS_VARIANTS_MIN
    NB_VARIANTS_MAX = PRODUITS_VARIANTS_MAX

    total_processed = 0
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
            nom_final = f"{nom_produit}"[:50]
            rows.append((nom_final, marque[:50], codeg))

        total_processed += 1
        if total_processed % 50 == 0:
            print(f"  Progress: {total_processed}/{len(PRODUITS)} product types processed...")

    print(f"  ✓ Completed: {len(rows)} product variants generated from {len(PRODUITS)} product types")
    return rows
