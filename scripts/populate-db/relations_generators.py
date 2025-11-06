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
    """
    Generate director assignments for departments.
    - Each department has a director who changes every 6 months to 4 years
    - One department keeps the same director throughout the entire period
    - Returns: [(CODEE, CODED, DATEDEBUTDIR), ...]
    Only creates entries when a director CHANGES, not for every date.
    """
    rows = []

    # Extract datetime objects if they are wrapped in tuples
    dates = []
    for d in cal2_dates:
        if isinstance(d, tuple):
            dates.append(d[0])
        else:
            dates.append(d)

    # Sort dates to have chronological order
    sorted_dates = sorted(dates)
    start_date = sorted_dates[0]
    end_date = sorted_dates[-1]

    # Pick one department that will have a static director
    static_dept = random.choice(departements_ids)
    static_director = random.choice(employes_ids)

    for dept_id in departements_ids:
        if dept_id == static_dept:
            # Static department: same director from start to end, only one entry
            rows.append((static_director, dept_id, start_date))
        else:
            # Dynamic department: director changes every 6 months to 4 years
            current_date = start_date

            # First director assignment
            director = random.choice(employes_ids)
            rows.append((director, dept_id, current_date))

            # Generate subsequent changes
            from datetime import timedelta
            while current_date < end_date:
                # Determine next change date (6 months to 4 years later)
                months_to_add = random.randint(6, 48)  # 6 months to 4 years
                days_to_add = months_to_add * 30  # approximate
                next_change_date = current_date + timedelta(days=days_to_add)

                # Stop if next change would be after end_date
                if next_change_date > end_date:
                    break

                # Find a date in sorted_dates that is close to next_change_date
                future_dates = [d for d in sorted_dates if d >= next_change_date]
                if not future_dates:
                    break

                # Use the first future date as the change date
                change_date = future_dates[0]

                # Assign a new director (different from previous one)
                new_director = random.choice([e for e in employes_ids if e != director])
                rows.append((new_director, dept_id, change_date))

                # Update for next iteration
                director = new_director
                current_date = change_date

    return rows

def gen_autoriser_with_ids(qualifs_rows, departements_rows):
    """
    Generate authorization rules linking qualifications to departments.
    Each department requires certain minimum qualification levels:
    - Direction, Finance, RH: minimum Licence (level 6+)
    - Fabrication, Assemblage: minimum BTS/DUT (level 5+)
    - Expédition, Logistique: minimum Bac Pro (level 4+)

    Parameters:
    - qualifs_rows: [(CODEQ, NOMQ), ...] from database
    - departements_rows: [(CODED, NOMD, CODEU), ...] from database

    Returns: [(CODEQ, CODED), ...]
    """
    from constants import QUALIFICATIONS

    rows = []

    # Build qualification level mapping
    qualif_name_to_level = {}
    for level, quals in QUALIFICATIONS.items():
        for q in quals:
            diplome = q[0]
            qualif_name_to_level[diplome] = level

    # Department requirements (minimum qualification level)
    dept_requirements = {
        "direction": 6,      # Licence minimum
        "finance": 6,        # Licence minimum
        "RH": 6,            # Licence minimum
        "fabrication": 5,   # BTS/DUT minimum
        "assemblage": 5,    # BTS/DUT minimum
        "expédition": 4,    # Bac Pro minimum
        "logistique": 4,    # Bac Pro minimum
    }

    # Build qualifications by level
    qualifs_by_level = {}
    for codeq, nomq in qualifs_rows:
        level = qualif_name_to_level.get(nomq)
        if level:
            if level not in qualifs_by_level:
                qualifs_by_level[level] = []
            qualifs_by_level[level].append((codeq, nomq))

    # For each department
    for dept_info in departements_rows:
        coded = dept_info[0]
        nomd = dept_info[1]

        # Determine minimum level required
        min_level = dept_requirements.get(nomd, 3)  # Default to CAP/BEP

        # Get eligible qualification levels
        eligible_levels = [lvl for lvl in qualifs_by_level.keys() if lvl >= min_level]

        # Number of qualifications to authorize (more for higher-level departments)
        if min_level >= 6:
            target = random.randint(5, 10)  # Direction/Finance/RH need more qualifications
        elif min_level >= 5:
            target = random.randint(4, 8)   # Fabrication/Assemblage
        else:
            target = random.randint(3, 6)   # Expédition/Logistique

        authorized = []

        # Prioritize higher levels but include some from lower levels too
        for level in sorted(eligible_levels, reverse=True):
            if len(authorized) >= target:
                break

            available = qualifs_by_level.get(level, [])
            if not available:
                continue

            # Take 1-3 qualifications from this level
            num_from_level = random.randint(1, min(3, len(available), target - len(authorized)))
            selected = random.sample(available, k=num_from_level)

            for codeq, nomq in selected:
                authorized.append((codeq, coded))

        rows.extend(authorized)

    # Remove duplicates and return
    rows = list(set(rows))
    return rows

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
    # For every gamme and every year, assign only one responsible employee
    rows = []
    # Choose one gamme for static responsibles
    static_gamme = random.choice(gammes)
    fixed_responsibles = random.sample(employes_ids, k=3)
    for g in gammes:
        for year in cal4:
            year_val = year[0] if isinstance(year, tuple) else year
            if g == static_gamme:
                # For the static gamme, pick one of the fixed responsibles (randomly per year)
                e = random.choice(fixed_responsibles)
            else:
                # For other gammes, pick a random employee
                e = random.choice(employes_ids)
            rows.append((e, g, year_val))
    # Uniqueness is guaranteed by construction (one per gamme/year)
    return rows

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
    """
    Generate salary payment data for employees using SMIC as reference.
    - Each employee gets a random start date from cal4
    - 95% of employees work until now (no end date)
    - 5% have an end date: either ±5 years or ±10 years from start
    - Salary increases year by year following SMIC trends with ±5% variation
    Returns: [(CODEE, ANNEE, FIXEMENSUELE, INDICESALE), ...]
    """
    from constants import SMICS, SMIC_AVG

    rows = []
    current_year = 2025

    # Extract years from cal4 (unwrap tuples if needed)
    years = []
    for y in cal4:
        if isinstance(y, tuple):
            years.append(y[0])
        else:
            years.append(y)
    years = sorted(list(set(years)))

    # Build SMIC lookup by year
    smic_by_year = {}
    for smic in SMICS:
        year = int(smic["date"].split("-")[0])
        if year not in smic_by_year:
            smic_by_year[year] = smic

    for e_id in employes_ids:
        # Random start year
        start_year = random.choice(years)

        # Determine if employee has end date (5% chance)
        has_end_date = random.random() < 0.05
        if has_end_date:
            # Choose range: 5 years (50%) or 10 years (50%)
            if random.random() < 0.5:
                year_range = random.randint(1, 5)
            else:
                year_range = random.randint(1, 10)
            end_year = start_year + year_range
            end_year = min(end_year, current_year)  # Can't be in future
        else:
            end_year = current_year

        # Generate salary for each year from start to end
        base_salary = round(random.uniform(1200, 5000), 2)

        for year in years:
            if year < start_year or year > end_year:
                continue

            # Calculate salary increase based on SMIC trends
            # Apply cumulative increase based on SMIC average with ±5% variation
            increase_factor = 1.0
            for y in range(start_year, year):
                # Get SMIC percentage for this year or use average
                if y in smic_by_year and smic_by_year[y]["pourcentage"] is not None:
                    smic_pct = smic_by_year[y]["pourcentage"]
                else:
                    smic_pct = SMIC_AVG

                # Apply variation ±5%
                variation = random.uniform(-0.05, 0.05)
                yearly_increase = smic_pct * (1 + variation)
                increase_factor *= (1 + yearly_increase)

            # Calculate salary for this year
            salary = round(base_salary * increase_factor, 2)

            # Random index between 1 and 15
            indice = random.randint(1, 15)

            rows.append((e_id, year, salary, indice))

    return rows

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
