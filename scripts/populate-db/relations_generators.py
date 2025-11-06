# -*- coding: utf-8 -*-
"""
Générateurs pour les tables de relation (associations)
"""

import random
from constants import *
from config import (
    FACTORY_SPECIALIZED_MIN, FACTORY_SPECIALIZED_MAX,
    FACTORY_SEMI_SPECIALIZED_MIN, FACTORY_SEMI_SPECIALIZED_MAX,
    FACTORY_GENERAL_MIN, FACTORY_GENERAL_MAX
)

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

def gen_assembler_with_ids(produits_rows):
    """
    Generate assembly relationships between products and their components.
    A product that has components in PRODUITS will be assembled from those components.

    Parameters:
    - produits_rows: [(CODEP, NOMP, MARQUEP, CODEG), ...] from database

    Returns: [(CODEP_EST_COMPOSE, CODEP_COMPOSE, QTE_ASSEMBL), ...]
    where CODEP_EST_COMPOSE is the final product and CODEP_COMPOSE is the component
    """
    from constants import PRODUITS

    rows = []

    # Build a mapping from product name to CODEP
    name_to_codep = {}
    for codep, nomp, marquep, codeg in produits_rows:
        # Store by base product name (without model number suffix)
        # Extract base name by removing model numbers like "Model-XX"
        base_name = nomp
        if " Model-" in nomp:
            base_name = nomp.split(" Model-")[0]

        # Map both full name and base name to CODEP
        name_to_codep[nomp] = codep
        if base_name not in name_to_codep:
            name_to_codep[base_name] = codep

    # For each product in PRODUITS that has components
    for prod_name, gamme, type_usine, composants in PRODUITS:
        if not composants:  # Skip products without components
            continue

        # Find the CODEP for this product
        prod_codep = name_to_codep.get(prod_name)
        if not prod_codep:
            # Try to find any product variant that matches (e.g., with Model-XX suffix)
            matching_products = [codep for name, codep in name_to_codep.items()
                                if name.startswith(prod_name) or prod_name in name]
            if matching_products:
                # Create assembly for all variants of this product
                for variant_codep in matching_products:
                    for composant_name, qte in composants:
                        composant_codep = name_to_codep.get(composant_name)
                        if composant_codep and composant_codep != variant_codep:
                            rows.append((variant_codep, composant_codep, qte))
            continue

        # For each component of this product
        for composant_name, qte in composants:
            composant_codep = name_to_codep.get(composant_name)
            if composant_codep and composant_codep != prod_codep:
                # Product is composed of this component with given quantity
                rows.append((prod_codep, composant_codep, qte))

    # Remove duplicates
    rows = list(set(rows))
    return rows

def gen_avoir_type_with_ids(usines_with_ids, typeu_with_ids, usines_full_data):
    """
    Generate factory type assignments with specialization and size classification.
    - Specialized factories: focus on 1 type (configurable employee count)
    - Semi-specialized: 2 types (configurable employee count)
    - General factories: 3-4 types (configurable employee count)

    Parameters:
    - usines_with_ids: [(CODEU, NOMU), ...]
    - typeu_with_ids: [(CODETU, NOMTU), ...]
    - usines_full_data: [(CODEU, NOMU, RUEU, CPOSTALU, VILLEU), ...]

    Returns: (rows, factory_info)
    """
    rows = []
    factory_info = {}  # Store classification and size per factory

    # Build address mapping
    address_map = {}
    for codeu, nomu, rue, cp, ville in usines_full_data:
        address_map[codeu] = {
            'street': rue,
            'postal_code': cp,
            'city': ville
        }

    # Categorize factories
    num_factories = len(usines_with_ids)
    num_specialized = max(1, num_factories // 3)  # ~33% specialized
    num_semi = max(1, num_factories // 3)          # ~33% semi-specialized
    num_general = num_factories - num_specialized - num_semi  # ~33% general

    factory_list = list(usines_with_ids)
    random.shuffle(factory_list)

    idx = 0

    # Specialized factories: 1 type, configurable employee count
    for i in range(num_specialized):
        if idx >= len(factory_list):
            break
        u_id, u_nom = factory_list[idx]
        selected_type = random.choice(typeu_with_ids)
        rows.append((u_id, selected_type[0]))
        taille = random.randint(FACTORY_SPECIALIZED_MIN, FACTORY_SPECIALIZED_MAX)
        factory_info[u_id] = {
            "classification": "specialized",
            "taille": taille,
            "types": [selected_type[1]],
            "address": address_map.get(u_id)
        }
        idx += 1

    # Semi-specialized factories: 2 types, configurable employee count
    for i in range(num_semi):
        if idx >= len(factory_list):
            break
        u_id, u_nom = factory_list[idx]
        selected_types = random.sample(typeu_with_ids, k=2)
        for t_id, t_nom in selected_types:
            rows.append((u_id, t_id))
        taille = random.randint(FACTORY_SEMI_SPECIALIZED_MIN, FACTORY_SEMI_SPECIALIZED_MAX)
        factory_info[u_id] = {
            "classification": "semi-specialized",
            "taille": taille,
            "types": [t[1] for t in selected_types],
            "address": address_map.get(u_id)
        }
        idx += 1

    # General factories: 3-4 types, configurable employee count
    for i in range(num_general):
        if idx >= len(factory_list):
            break
        u_id, u_nom = factory_list[idx]
        num_types = random.randint(3, min(4, len(typeu_with_ids)))
        selected_types = random.sample(typeu_with_ids, k=num_types)
        for t_id, t_nom in selected_types:
            rows.append((u_id, t_id))
        taille = random.randint(FACTORY_GENERAL_MIN, FACTORY_GENERAL_MAX)
        factory_info[u_id] = {
            "classification": "general",
            "taille": taille,
            "types": [t[1] for t in selected_types],
            "address": address_map.get(u_id)
        }
        idx += 1

    return rows, factory_info

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
        # Extract code if g is a tuple (CODEG, NOMG)
        g_code = g[0] if isinstance(g, tuple) else g
        for year in cal4:
            year_val = year[0] if isinstance(year, tuple) else year
            if g == static_gamme:
                # For the static gamme, pick one of the fixed responsibles (randomly per year)
                e = random.choice(fixed_responsibles)
            else:
                # For other gammes, pick a random employee
                e = random.choice(employes_ids)
            rows.append((e, g_code, year_val))
    # Uniqueness is guaranteed by construction (one per gamme/year)
    return rows

def gen_payer2(gammes, cal4):
    """
    Generate commission/retrocession indices for product ranges by year.

    Parameters:
    - gammes: list of (CODEG, NOMG) tuples from GAMME table
    - cal4: list of year tuples from CALENDRIER4

    Returns: [(CODEG, ANNEE, INDICERETROCESSIONG), ...]
    """
    rows = []

    # Extract years from cal4 (unwrap tuples if needed)
    all_years = []
    for y in cal4:
        if isinstance(y, tuple):
            all_years.append(y[0])
        else:
            all_years.append(y)
    all_years = sorted(list(set(all_years)))

    print("\n📊 Generating product range commissions...")

    for year in all_years:
        num_records = random.randint(2, min(10, len(gammes)))
        selected_gammes = random.sample(gammes, k=num_records)
        for g_code, g_name in selected_gammes:
            indice = round(random.uniform(0.01, 0.99), 2)
            rows.append((g_code, year, indice))

    print(f"  ✓ Generated: {len(rows)} commission records")
    return rows

def gen_fabriquer_with_ids(usines_with_ids, produits_rows, factory_info, cal1_dates):
    """
    Generate manufacturing records based on factory specialization and size.
    - Specialized factories produce more of their specific product types
    - Larger factories produce more volume
    - Production is consistent over time with seasonal variations

    Parameters:
    - usines_with_ids: [(CODEU, NOMU), ...]
    - produits_rows: [(CODEP, NOMP, MARQUEP, CODEG), ...]
    - factory_info: dict with factory details (classification, taille, types, address)
    - cal1_dates: list of manufacturing dates

    Returns: [(CODEU, CODEP, DATEFAB, QTE_FAB), ...]
    """
    from constants import PRODUITS, GAMMES

    rows = []

    print("\n🏭 Generating manufacturing records...")

    # Build mapping of product types to factory types
    type_to_gammes = {}
    for prod_name, gamme, type_usine, composants in PRODUITS:
        if type_usine not in type_to_gammes:
            type_to_gammes[type_usine] = set()
        type_to_gammes[type_usine].add(gamme)

    # Build mapping from CODEG to gamme name
    gamme_code_to_name = {f"G{str(i).zfill(2)}": nom for i, nom in enumerate(GAMMES, start=1)}

    # Build products by gamme
    products_by_gamme = {}
    for codep, nomp, marquep, codeg in produits_rows:
        gamme_name = gamme_code_to_name.get(codeg, "")
        if gamme_name not in products_by_gamme:
            products_by_gamme[gamme_name] = []
        products_by_gamme[gamme_name].append((codep, nomp, marquep))

    # Sample dates for manufacturing (not every day)
    sampled_dates = random.sample(cal1_dates, min(len(cal1_dates), 500))

    total_records = 0

    for u_id, info in factory_info.items():
        factory_types = info['types']  # List of factory type names
        factory_size = info['taille']
        classification = info['classification']

        # Determine production capacity based on size
        if factory_size >= 400:
            daily_capacity_range = (100, 500)
            num_products = random.randint(15, 30)
        elif factory_size >= 250:
            daily_capacity_range = (50, 300)
            num_products = random.randint(10, 20)
        else:
            daily_capacity_range = (20, 150)
            num_products = random.randint(5, 15)

        # Find gammes this factory can produce based on its types
        factory_gammes = set()
        for factory_type in factory_types:
            if factory_type in type_to_gammes:
                factory_gammes.update(type_to_gammes[factory_type])

        if not factory_gammes:
            continue

        # Select products this factory will manufacture
        factory_products = []
        for gamme in factory_gammes:
            if gamme in products_by_gamme:
                available_products = products_by_gamme[gamme]
                # Specialized factories focus on fewer products but higher volume
                if classification == "specialized":
                    num_from_gamme = random.randint(3, 8)
                elif classification == "semi-specialized":
                    num_from_gamme = random.randint(5, 12)
                else:  # general
                    num_from_gamme = random.randint(2, 6)

                num_from_gamme = min(num_from_gamme, len(available_products))
                selected = random.sample(available_products, k=num_from_gamme)
                factory_products.extend(selected)

        if not factory_products:
            continue

        # Limit to num_products
        factory_products = random.sample(factory_products, k=min(num_products, len(factory_products)))

        # Generate manufacturing records for this factory
        # Specialized factories produce more consistently
        if classification == "specialized":
            dates_to_use = random.sample(sampled_dates, k=min(len(sampled_dates), 80))
        elif classification == "semi-specialized":
            dates_to_use = random.sample(sampled_dates, k=min(len(sampled_dates), 60))
        else:
            dates_to_use = random.sample(sampled_dates, k=min(len(sampled_dates), 40))

        for date_tuple in dates_to_use:
            date = date_tuple[0] if isinstance(date_tuple, tuple) else date_tuple

            # Each day, produce some of the products
            num_products_today = random.randint(len(factory_products) // 3, len(factory_products))
            products_today = random.sample(factory_products, k=num_products_today)

            for codep, nomp, marquep in products_today:
                quantity = random.randint(daily_capacity_range[0], daily_capacity_range[1])
                rows.append((u_id, codep, date, quantity))
                total_records += 1

                if total_records % 1000 == 0:
                    print(f"  ├─ Progress: {total_records} manufacturing records")

    print(f"  ✓ Completed: {total_records} manufacturing records")
    return rows

def gen_facturer_with_ids(produits_ids, cal3):
    rows = []
    for p_id in produits_ids:
        for (m, y) in random.sample(cal3, k=random.randint(4, 12)):
            pu = round(random.uniform(2.0, 2500.0), 2)
            rows.append((p_id, m, y, pu))
    return rows[:500]

def gen_vendre_with_ids(employes_ids, pvs_ids, produits_rows, pv_info, employee_workplace, cal3, trav_pv):
    """
    Generate sales records based on point of sale size and employee assignments.
    - Larger stores sell more products
    - Employees only sell at their assigned location
    - Sales volume depends on store type (Express vs GSB)
    - CRITICAL: Employees can ONLY sell during months when they have work hours at the PV

    Parameters:
    - employes_ids: list of employee IDs
    - pvs_ids: list of point of sale IDs
    - produits_rows: [(CODEP, NOMP, MARQUEP, CODEG), ...]
    - pv_info: dict with PV details (is_express, postal_code, city)
    - employee_workplace: list of lists containing (workplace_type, workplace_id) tuples
    - cal3: list of (month, year) tuples
    - trav_pv: list of PV work hour records [(CODEE, CODEPV, MOIS, ANNEE, NBHEURES_PV), ...]

    Returns: [(CODEE, CODEPV, CODEP, MOIS, ANNEE, QTE_VENDUE), ...]
    """
    rows = []

    print("\n🛒 Generating sales records...")

    # Build mapping of employees working at PV by month/year
    # Key: (employee_id, pv_id, month, year) -> has work hours
    employee_pv_month_hours = set()
    for codee, codepv, mois, annee, nbheures in trav_pv:
        employee_pv_month_hours.add((codee, codepv, mois, annee))

    print(f"  ├─ Employee-PV-Month combinations with work hours: {len(employee_pv_month_hours)}")

    # Build mapping of employees to their workplaces
    pv_employees = {}  # pv_id -> [employee_ids]
    for idx, workplaces in enumerate(employee_workplace):
        if idx < len(employes_ids):
            # Check if this employee works at any PV
            for workplace_type, workplace_id in workplaces:
                if workplace_type == 'pv':
                    if workplace_id not in pv_employees:
                        pv_employees[workplace_id] = []
                    pv_employees[workplace_id].append(employes_ids[idx])

    # Get all product IDs
    all_products = [codep for codep, nomp, marquep, codeg in produits_rows]

    # Sample calendar dates (not every month for every combination)
    sampled_cal = random.sample(cal3, min(len(cal3), 200))

    total_records = 0
    skipped_no_hours = 0

    for pv_id in pvs_ids:
        # Get PV info
        pv_data = pv_info.get(pv_id, {})
        is_express = pv_data.get('is_express', True)

        # Get employees working at this PV
        pv_employee_list = pv_employees.get(pv_id, [])
        if not pv_employee_list:
            continue

        # Determine sales characteristics based on store type
        if is_express:
            # Brico-Express: smaller store, fewer products, lower volume
            num_products_sold = random.randint(20, 50)
            sales_per_employee_month = random.randint(2, 8)
            quantity_range = (1, 25)
        else:
            # GSB: large store, more products, higher volume
            num_products_sold = random.randint(80, 200)
            sales_per_employee_month = random.randint(5, 15)
            quantity_range = (5, 100)

        # Select products this store sells
        store_products = random.sample(all_products, k=min(num_products_sold, len(all_products)))

        # Sample dates for this store
        store_dates = random.sample(sampled_cal, k=min(len(sampled_cal), 40))

        for month, year in store_dates:
            # Filter employees who have work hours THIS MONTH at THIS PV
            employees_with_hours_this_month = [
                emp_id for emp_id in pv_employee_list
                if (emp_id, pv_id, month, year) in employee_pv_month_hours
            ]

            if not employees_with_hours_this_month:
                skipped_no_hours += 1
                continue

            # Select employees who make sales this month (only from those with hours)
            num_selling_employees = min(len(employees_with_hours_this_month),
                                       max(1, len(employees_with_hours_this_month) // 2))
            selling_employees = random.sample(employees_with_hours_this_month, k=num_selling_employees)

            for emp_id in selling_employees:
                # Number of different products this employee sells this month
                num_products_emp = random.randint(1, sales_per_employee_month)
                emp_products = random.sample(store_products, k=min(num_products_emp, len(store_products)))

                for prod_id in emp_products:
                    quantity = random.randint(quantity_range[0], quantity_range[1])
                    rows.append((emp_id, pv_id, prod_id, month, year, quantity))
                    total_records += 1

                    if total_records % 1000 == 0:
                        print(f"  ├─ Progress: {total_records} sales records")

    print(f"  ├─ Skipped {skipped_no_hours} PV-month combinations (no employees with work hours)")
    print(f"  ✓ Completed: {total_records} sales records")
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

        # Generate salary for EVERY year from start to end (continuous coverage)
        base_salary = round(random.uniform(1200, 5000), 2)

        # Generate continuous salary records for all years in employment
        for year in range(start_year, end_year + 1):
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

def gen_travailler_usine_with_ids(employes_ids, departements_ids, employee_workplace, cal3):
    """
    Generate factory work hours for factory employees (including dual workers).
    Employees work in departments at their assigned factory.

    Parameters:
    - employes_ids: list of employee IDs
    - departements_ids: list of department IDs
    - employee_workplace: list of lists containing (workplace_type, workplace_id) tuples
    - cal3: list of (month, year) tuples

    Returns: [(CODEE, CODED, MOIS, ANNEE, NBHEURES_U), ...]
    """
    rows = []

    print("\n⏰ Generating factory work hours...")

    # Get factory employees (including those who work at both factory and PV)
    factory_employees = []
    for idx, workplaces in enumerate(employee_workplace):
        if idx < len(employes_ids):
            # Check if this employee works at any factory
            for workplace_type, workplace_id in workplaces:
                if workplace_type == 'factory':
                    factory_employees.append((employes_ids[idx], workplace_id))
                    break  # Only add once even if multiple factories

    # Sort calendar chronologically for continuous employment
    sorted_cal = sorted(cal3, key=lambda x: (x[1], x[0]))  # Sort by (year, month)

    total_records = 0

    for emp_id, factory_id in factory_employees:
        # Get departments (we'd need dept->factory mapping, so use all for now)
        factory_depts = departements_ids

        if not factory_depts:
            continue

        # Assign employee to 1-2 stable departments
        num_assigned_depts = random.randint(1, min(2, len(factory_depts)))
        assigned_depts = random.sample(factory_depts, k=num_assigned_depts)

        # Determine employment period (continuous from start to end)
        # Random start index in calendar
        start_idx = random.randint(0, max(0, len(sorted_cal) - 12))

        # 95% work until end of calendar, 5% leave early (after 6-24 months)
        if random.random() < 0.05:
            # Early termination after 6-24 months
            duration = random.randint(6, min(24, len(sorted_cal) - start_idx))
            end_idx = start_idx + duration
        else:
            # Work until present (end of calendar)
            end_idx = len(sorted_cal)

        # Check if this is a dual worker
        emp_idx = employes_ids.index(emp_id)
        is_dual_worker = len(employee_workplace[emp_idx]) > 1

        # Generate work hours for EVERY month from start to end (continuous employment)
        for month_idx in range(start_idx, end_idx):
            month, year = sorted_cal[month_idx]

            # Work in assigned departments
            for dept_id in assigned_depts:
                # Determine if full-time or part-time (80% full-time, 20% part-time)
                if random.random() < 0.8:
                    # Adjust hours if dual worker (split time between workplaces)
                    if is_dual_worker:
                        # Dual workers: 60-80 hours at factory (part-time)
                        hours = round(random.uniform(60, 80), 2)
                    else:
                        # Full-time: 120-160 hours per month
                        hours = round(random.uniform(120, 160), 2)
                else:
                    # Part-time: 35-119 hours per month
                    hours = round(random.uniform(35, 119), 2)

                rows.append((emp_id, dept_id, month, year, hours))
                total_records += 1

                if total_records % 1000 == 0:
                    print(f"  ├─ Progress: {total_records} factory work records")

    avg_records_per_emp = total_records / len(factory_employees) if factory_employees else 0
    print(f"  ✓ Completed: {total_records} factory work hour records (~{avg_records_per_emp:.1f} per employee)")
    return rows

def gen_travailler_pv_with_ids(employes_ids, pvs_ids, employee_workplace, cal3):
    """
    Generate point of sale work hours for PV employees (including dual workers).
    Employees work at their assigned point of sale.

    Parameters:
    - employes_ids: list of employee IDs
    - pvs_ids: list of point of sale IDs
    - employee_workplace: list of lists containing (workplace_type, workplace_id) tuples
    - cal3: list of (month, year) tuples

    Returns: [(CODEE, CODEPV, MOIS, ANNEE, NBHEURES_PV), ...]
    """
    rows = []

    print("\n🏪 Generating point of sale work hours...")

    # Get PV employees (including those who work at both factory and PV)
    pv_employees = []
    for idx, workplaces in enumerate(employee_workplace):
        if idx < len(employes_ids):
            # Check if this employee works at any PV
            for workplace_type, workplace_id in workplaces:
                if workplace_type == 'pv':
                    pv_employees.append((employes_ids[idx], workplace_id))
                    break  # Only add once even if multiple PVs

    # Sort calendar chronologically for continuous employment
    sorted_cal = sorted(cal3, key=lambda x: (x[1], x[0]))  # Sort by (year, month)

    total_records = 0

    for emp_id, pv_id in pv_employees:
        # Determine employment period (continuous from start to end)
        # Random start index in calendar
        start_idx = random.randint(0, max(0, len(sorted_cal) - 12))

        # 95% work until end of calendar, 5% leave early (after 8-30 months)
        if random.random() < 0.05:
            # Early termination after 8-30 months
            duration = random.randint(8, min(30, len(sorted_cal) - start_idx))
            end_idx = start_idx + duration
        else:
            # Work until present (end of calendar)
            end_idx = len(sorted_cal)

        # Check if this is a dual worker
        emp_idx = employes_ids.index(emp_id)
        is_dual_worker = len(employee_workplace[emp_idx]) > 1

        # Generate work hours for EVERY month from start to end (continuous employment)
        for month_idx in range(start_idx, end_idx):
            month, year = sorted_cal[month_idx]

            # Determine if full-time or part-time (75% full-time, 25% part-time)
            if random.random() < 0.75:
                # Adjust hours if dual worker
                if is_dual_worker:
                    # Dual workers: 60-80 hours at PV (part-time)
                    hours = round(random.uniform(60, 80), 2)
                else:
                    # Full-time: 120-169 hours per month
                    hours = round(random.uniform(120, 169), 2)
            else:
                # Part-time: 50-119 hours per month
                hours = round(random.uniform(50, 119), 2)

            rows.append((emp_id, pv_id, month, year, hours))
            total_records += 1

            if total_records % 1000 == 0:
                print(f"  ├─ Progress: {total_records} PV work records")

    avg_records_per_emp = total_records / len(pv_employees) if pv_employees else 0
    print(f"  ✓ Completed: {total_records} PV work hour records (~{avg_records_per_emp:.1f} per employee)")
    return rows
