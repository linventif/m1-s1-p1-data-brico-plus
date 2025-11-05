# -*- coding: utf-8 -*-
"""
Générateurs pour les tables de relation (associations)
"""

import random
from constants import *

def gen_departements_with_ids(usines_with_ids):
    rows = []
    for u_id, u_nom in usines_with_ids:
        nb = random.randint(3, 6)
        noms = random.sample(DEPTS, k=nb)
        for nom in noms:
            rows.append((nom, u_id))
    return rows

def gen_posseder_with_ids(employes_ids, qualifs_ids):
    from constants import QUALIFICATIONS_PROBABILITIES, QUALIFICATIONS
    rows = []
    # Build a mapping from qualification name to CODEQ
    # qualifs_ids is expected to be a list of CODEQ, and we need the names
    # So require a second argument: qualifs_name_map (dict: name -> CODEQ)
    # If not provided, fallback to old logic
    if isinstance(qualifs_ids, dict):
        name_to_codeq = qualifs_ids
        qualif_names_by_level = {}
        for lvl in sorted(QUALIFICATIONS.keys()):
            qualif_names_by_level[lvl] = [q[0] for q in QUALIFICATIONS[lvl]]
        levels = list(QUALIFICATIONS_PROBABILITIES.keys())
        probabilities = [QUALIFICATIONS_PROBABILITIES[lvl] for lvl in levels]
        for e_id in employes_ids:
            lvl = random.choices(levels, weights=probabilities, k=1)[0]
            main_name = random.choice(qualif_names_by_level[lvl])
            main_codeq = name_to_codeq[main_name]
            rows.append((e_id, main_codeq))
            if lvl >= 6:
                lower_levels = [l for l in levels if l < 6]
                lower_lvl = random.choice(lower_levels)
                lower_name = random.choice(qualif_names_by_level[lower_lvl])
                lower_codeq = name_to_codeq[lower_name]
                rows.append((e_id, lower_codeq))
            # Optionally, add more random qualifications (2-5 total)
            extra_count = random.randint(1, 3)
            all_names = set(name_to_codeq.keys())
            already = {main_name}
            if lvl >= 6:
                already.add(lower_name)
            extra_names = random.sample(list(all_names - already), k=extra_count)
            for ename in extra_names:
                rows.append((e_id, name_to_codeq[ename]))
        return rows[:max(500, len(rows))]
    else:
        # fallback: old logic
        for e_id in employes_ids:
            sample_size = min(len(qualifs_ids), random.randint(2, 5)) if qualifs_ids else 0
            qset = random.sample(qualifs_ids, k=sample_size) if sample_size > 0 else []
            for q_id in qset:
                rows.append((e_id, q_id))
        return rows[:max(500, len(rows))]

def gen_assembler_with_ids(produits_ids):
    rows = []
    used = set()
    for _ in range(500):
        a, b = random.sample(produits_ids, 2)
        if a == b:
            continue
        key = (a, b)
        if key in used:
            continue
        used.add(key)
        rows.append((a, b, random.randint(1, 10)))
    return rows

def gen_avoir_type_with_ids(usines_with_ids, typeu_with_ids):
    rows = []
    for u_id, u_nom in usines_with_ids:
        for t_id, t_nom in random.sample(typeu_with_ids, k=random.randint(1, min(2, len(typeu_with_ids)))):
            rows.append((u_id, t_id))
    return rows

def gen_diriger_with_ids(employes_ids, departements_ids, cal2_dates):
    rows = []
    for _ in range(500):
        e = random.choice(employes_ids)
        d = random.choice(departements_ids)
        date = random.choice(cal2_dates)
        rows.append((e, d, date))
    rows = list({(a, b, c) for (a, b, c) in rows})
    return rows[:500]

def gen_autoriser_with_ids(qualifs_ids, departements_ids):
    rows = []
    for d in random.sample(departements_ids, k=min(500, len(departements_ids))):
        for q in random.sample(qualifs_ids, k=random.randint(3, 8)):
            rows.append((q, d))
    return rows[:500]

def gen_fabriquer_with_ids(usines_with_ids, produits_ids, typeu_with_ids, cal1_dates):
    rows = []
    used = set()
    attempts = 0
    max_attempts = 2000
    target_records = 500

    while len(rows) < target_records and attempts < max_attempts:
        attempts += 1
        u_id = random.choice([u[0] for u in usines_with_ids])
        p_id = random.choice(produits_ids)
        d = random.choice(cal1_dates)
        key = (u_id, p_id, d)
        if key not in used:
            used.add(key)
            q = random.randint(10, 500)
            rows.append((u_id, p_id, d, q))
    return rows

def gen_responsable_with_ids(employes_ids, gammes, cal4):
    rows = []
    mandatory_years = [2024, 2025]
    other_years = random.sample([y for y in cal4 if y not in mandatory_years], k=min(15, len(cal4)-2))
    years = mandatory_years + other_years
    for _ in range(500):
        e = random.choice(employes_ids)
        g = random.choice(gammes)[0]
        y = random.choice(years)
        rows.append((e, g, y))
    rows = list({(a, b, c) for (a, b, c) in rows})
    return rows[:500]

def gen_payer2(gammes):
    rows = []
    all_years = list(range(1985, 2026))
    for year in all_years:
        num_records = random.randint(2, 10)
        selected_gammes = random.sample(gammes, k=min(num_records, len(gammes)))
        for g in selected_gammes:
            indice = round(random.uniform(0.01, 0.99), 2)
            rows.append((g[0], year, indice))
    return rows

def gen_facturer_with_ids(produits_ids, cal3):
    rows = []
    for p_id in produits_ids:
        for (m, y) in random.sample(cal3, k=random.randint(4, 12)):
            pu = round(random.uniform(2.0, 2500.0), 2)
            rows.append((p_id, m, y, pu))
    return rows[:500]

def gen_vendre_with_ids(employes_ids, pvs_ids, produits_ids, cal3):
    rows = []
    used = set()
    attempts = 0
    max_attempts = 5000
    target_records = 500

    while len(rows) < target_records and attempts < max_attempts:
        attempts += 1
        e = random.choice(employes_ids)
        pv = random.choice(pvs_ids)
        p = random.choice(produits_ids)
        (m, y) = random.choice(cal3)
        key = (e, pv, p, m, y)
        if key not in used:
            used.add(key)
            q = random.randint(1, 100)
            rows.append((e, pv, p, m, y, q))
    return rows

def gen_payer1_with_ids(employes_ids, cal4):
    rows = []
    mandatory_years = [2024, 2025]
    other_years = random.sample([y for y in cal4 if y not in mandatory_years], k=min(15, len(cal4)-2))
    years = mandatory_years + other_years
    for e_id in employes_ids:
        for y in years:
            fixe = round(random.uniform(1200, 5000), 2)
            idx = random.randint(1, 15)
            rows.append((e_id, y, fixe, idx))
    return rows[:1000]

def gen_travailler_usine_with_ids(employes_ids, departements_ids, cal3):
    rows = []
    used = set()
    attempts = 0
    max_attempts = 2000
    target_records = 500

    while len(rows) < target_records and attempts < max_attempts:
        attempts += 1
        e = random.choice(employes_ids)
        d = random.choice(departements_ids)
        (m, y) = random.choice(cal3)
        key = (e, d, m, y)
        if key not in used:
            used.add(key)
            hrs = round(random.uniform(5, 200), 2)
            rows.append((e, d, m, y, hrs))
    return rows

def gen_travailler_pv_with_ids(employes_ids, pvs_ids, cal3):
    rows = []
    used = set()
    attempts = 0
    max_attempts = 2000
    target_records = 500

    while len(rows) < target_records and attempts < max_attempts:
        attempts += 1
        e = random.choice(employes_ids)
        pv = random.choice(pvs_ids)
        (m, y) = random.choice(cal3)
        key = (e, pv, m, y)
        if key not in used:
            used.add(key)
            hrs = round(random.uniform(3, 180), 2)
            rows.append((e, pv, m, y, hrs))
    return rows
