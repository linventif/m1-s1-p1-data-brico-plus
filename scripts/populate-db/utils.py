# -*- coding: utf-8 -*-
"""
Fonctions utilitaires pour la génération de données
"""

import random
import string
import datetime as dt
from constants import HG_CITIES, FR_CITIES, YEAR_NOW, N_CAL1

def phone(hg=False):
    """Génère un numéro de téléphone français"""
    if hg:
        pref = "05"
    else:
        pref = random.choice(["01", "02", "03", "04", "05", "09"])
    return pref + "".join(random.choices(string.digits, k=8))

def pick_city(hg_bias=True):
    """Sélectionne une ville (70% HG si hg_bias=True)"""
    if hg_bias and random.random() < 0.7:
        return random.choice(HG_CITIES)
    return random.choice(FR_CITIES)

def street():
    """Génère une adresse de rue factice"""
    types = ["Rue", "Avenue", "Boulevard", "Allée", "Chemin", "Impasse", "Place"]
    noms = ["Victor-Hugo", "de la République", "des Lilas", "du 14-Juillet", "Jean-Jaurès",
            "de la Liberté", "des Acacias", "des Forges", "Pasteur", "des Écoles"]
    return f"{random.randint(1, 220)} {random.choice(types)} {random.choice(noms)}"

def sample_dates(n):
    """Génère n dates aléatoires <= aujourd'hui"""
    base = dt.date(YEAR_NOW-1, 1, 1)
    last = dt.date.today()
    span = (last - base).days
    seen = set()
    out = []
    while len(out) < n:
        d = base + dt.timedelta(days=random.randint(0, max(span, 1)))
        if d <= last and d not in seen:
            seen.add(d)
            out.append(d)
    out.sort()
    return out

def generate_calendars():
    """Génère les 4 calendriers"""
    # CAL1 & CAL2: dates
    cal1_dates = sample_dates(N_CAL1)
    cal2_dates = sample_dates(N_CAL1)
    
    # CAL3: (mois, année)
    cal3 = []
    y, m = YEAR_NOW, dt.date.today().month
    for _ in range(60):
        cal3.append((m, y))
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    cal3 = cal3[:50]
    
    # CAL4: années 1985-2025
    cal4 = list(range(1985, 2026))
    
    return cal1_dates, cal2_dates, cal3, cal4
