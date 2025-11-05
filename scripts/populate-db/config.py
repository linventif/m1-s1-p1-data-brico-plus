# -*- coding: utf-8 -*-
"""
Configuration et chargement des variables d'environnement
"""

from pathlib import Path
import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    sys.stderr.write("❌ Erreur : le module python-dotenv est requis. Installe-le avec:\n")
    sys.stderr.write("   pip install python-dotenv\n")
    sys.exit(1)

HERE = Path(__file__).resolve().parent
default_env_path = HERE.parent.parent / ".env"
ENV_PATH = Path(os.getenv("ENV_FILE", str(default_env_path)))

if not ENV_PATH.exists():
    sys.stderr.write(f"❌ Fichier .env introuvable : {ENV_PATH}\n")
    sys.stderr.write("Place un fichier .env à la racine du projet ou définis ENV_FILE=/chemin/.env\n")
    sys.exit(1)

load_dotenv(dotenv_path=str(ENV_PATH), override=False)

# Vérification des variables obligatoires
required_vars = ["ORACLE_HOST", "ORACLE_PORT", "ORACLE_SERVICE", "ORACLE_USER", "ORACLE_PASS"]
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    sys.stderr.write("❌ Variables manquantes dans .env : " + ", ".join(missing) + "\n")
    sys.stderr.write("Exemple minimal :\n"
                     "ORACLE_HOST=xxx.xxx.xxx.xxx\n"
                     "ORACLE_PORT=1521\n"
                     "ORACLE_SERVICE=xxx\n"
                     "ORACLE_USER=xxx\n"
                     "ORACLE_PASS=xxx\n")
    sys.exit(1)

# Configuration Oracle
HOST = os.getenv("ORACLE_HOST")
PORT = int(os.getenv("ORACLE_PORT"))
SERVICE = os.getenv("ORACLE_SERVICE")
USER = os.getenv("ORACLE_USER")
PASS = os.getenv("ORACLE_PASS")

# Configurations de génération de données
NOMBRE_EMPLOYES_PAR_USINE = int(os.getenv("NOMBRE_EMPLOYES_PAR_USINE", "10"))
NOMBRE_EMPLOYES_PAR_POINT_VENTE = int(os.getenv("NOMBRE_EMPLOYES_PAR_POINT_VENTE", "5"))
NOMBRE_USINES = int(os.getenv("NOMBRE_USINES", "15"))
NOMBRE_POINTS_VENTE = int(os.getenv("NOMBRE_POINTS_VENTE", "50"))
NOMBRE_PRODUITS = int(os.getenv("NOMBRE_PRODUITS", "100"))
PRODUITS_CHANCE_DOUBLE_MARQUE = float(os.getenv("PRODUITS_CHANCE_DOUBLE_MARQUE", "0.3"))
CALENDRIER_DATE_DEBUT = os.getenv("CALENDRIER_DATE_DEBUT", "2000-01-01")
CALENDRIER_DATE_FIN = os.getenv("CALENDRIER_DATE_FIN", "2025-10-31")