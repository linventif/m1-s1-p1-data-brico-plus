# -*- coding: utf-8 -*-
"""
Fonctions utilitaires pour la génération de données
"""

import random
import string
import os
import csv

def getRandomPhone():
    return random.choice(["01", "02", "03", "04", "05", "09"]) + "".join(random.choices(string.digits, k=8))

def getRandomStreet():
    path = "./data/adresses/adresses-france-extract.csv"
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found. Please execute get-and-extract.sh before trying to generate data.")

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = []
        for r in reader:
            if not r:
                continue
            # expect lines like: numero,nom_voie,code_postal,nom_commune
            if len(r) < 4:
                continue
            # skip possible header
            if any(h.lower() in r[i].lower() for i, h in enumerate(["numero", "nom_voie", "code_postal", "nom_commune"]) if i < len(r)):
                continue
            rows.append(r)

    if not rows:
        raise ValueError(f"No valid address lines found in {path}. Please execute get-and-extract.sh before trying to generate data.")

    numero, nom_voie, code_postal, nom_commune = [c.strip() for c in random.choice(rows)]

    # merge numero with nom_voie when numero is present
    if numero and numero not in ("", "-", "0"):
        street_full = f"{numero} {nom_voie}"
    else:
        street_full = nom_voie

    return {
        "street": street_full,
        "number": numero,
        "street_name": nom_voie,
        "postal_code": code_postal,
        "city": nom_commune,
    }


def getRandomStreetNearby(base_street_info):
    """
    Return a random street whose postal code shares the same first 3 digits
    as the provided base_street_info (or postal code string).
    """
    if not base_street_info:
        raise ValueError("base_street_info is required")

    # allow passing either the dict returned by getRandomStreet or a postal code string
    if isinstance(base_street_info, str):
        base_postal = base_street_info
    else:
        base_postal = base_street_info.get("postal_code") if isinstance(base_street_info, dict) else None

    if not base_postal:
        raise ValueError("base_street_info must contain a 'postal_code' or be a postal code string")

    # normalize to digits and take first 3
    base_digits = "".join(ch for ch in base_postal if ch.isdigit())
    if len(base_digits) < 3:
        raise ValueError(f"postal code '{base_postal}' is too short to extract 3 digits")
    dep_prefix = base_digits[:3]

    path = "./data/adresses/adresses-france-extract.csv"
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found. Please execute get-and-extract.sh before trying to generate data.")

    matches = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for r in reader:
            if not r or len(r) < 4:
                continue
            # skip possible header
            if any(h.lower() in r[i].lower() for i, h in enumerate(["numero", "nom_voie", "code_postal", "nom_commune"]) if i < len(r)):
                continue

            numero, nom_voie, code_postal, nom_commune = [c.strip() for c in r[:4]]
            code_digits = "".join(ch for ch in code_postal if ch.isdigit())
            if code_digits.startswith(dep_prefix):
                matches.append((numero, nom_voie, code_postal, nom_commune))

    if not matches:
        raise ValueError(f"No address lines found with postal code starting with '{dep_prefix}' in {path}")

    numero, nom_voie, code_postal, nom_commune = random.choice(matches)
    if numero and numero not in ("", "-", "0"):
        street_full = f"{numero} {nom_voie}"
    else:
        street_full = nom_voie

    return {
        "street": street_full,
        "number": numero,
        "street_name": nom_voie,
        "postal_code": code_postal,
        "city": nom_commune,
    }

def getRandomFullName():
    pathPatronymes = "./data/patronymes/patronymes-extract.csv"
    pathPrenoms = "./data/patronymes/prenom-extract.csv"
    if not os.path.exists(pathPatronymes) or not os.path.exists(pathPrenoms):
        raise FileNotFoundError("Patronymes or prénoms data files not found. Please execute get-and-extract.sh before trying to generate data.")
    patronymes = []
    with open(pathPatronymes, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                continue  # skip header
            if row and row[0].strip():
                patronymes.append(row[0].strip())
    prenoms = []
    with open(pathPrenoms, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                continue  # skip header
            if row and row[0].strip():
                prenoms.append(row[0].strip())
    if not patronymes or not prenoms:
        raise ValueError("No patronymes or prénoms found in data files. Please execute get-and-extract.sh before trying to generate data.")
    first_name = random.choice(prenoms)
    last_name = random.choice(patronymes)
    return {
        "first_name": first_name,
        "last_name": last_name,
        "full_name": f"{first_name} {last_name}"
    }

print(getRandomFullName())