# -*- coding: utf-8 -*-
"""
Gestion de la base de données et des insertions
"""
# note: si pas d'heure de travail pas de bonnus
# note: la ville pro employé doit être proche de la ville pro usine
import oracledb
from config import HOST, PORT, SERVICE, USER, PASS

def clear_all_data(cursor):
    """Vide toutes les tables dans l'ordre correct (dépendances)"""
    tables_to_clear = [
        "TRAVAILLER_PT_VENTE", "TRAVAILLER_USINE", "PAYER1", "VENDRE",
        "FACTURER", "PAYER2", "RESPONSABLE", "FABRIQUER_ASSEMBLER1",
        "AUTORISER", "DIRIGER", "AVOIR_TYPE", "ASSEMBLER", "POSSEDER",
        "PRODUITS", "POINTS_DE_VENTE", "DEPARTEMENTS", "QUALIFICATIONS",
        "EMPLOYES", "USINES", "CALENDRIER4", "CALENDRIER3", "CALENDRIER2",
        "CALENDRIER1", "GAMME", "TYPEU"
    ]

    print("🧹 Nettoyage des données existantes...")
    for table in tables_to_clear:
        try:
            cursor.execute(f"DELETE FROM {table}")
            print(f"   ✓ {table} vidée")
        except Exception as e:
            print(f"   ⚠️  Erreur lors du nettoyage de {table}: {e}")
    print("🧹 Nettoyage terminé.\n")

def get_connection():
    """Crée et retourne une connexion Oracle"""
    dsn = oracledb.makedsn(HOST, PORT, service_name=SERVICE)
    return oracledb.connect(user=USER, password=PASS, dsn=dsn)
