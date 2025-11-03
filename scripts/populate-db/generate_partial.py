# -*- coding: utf-8 -*-
"""
Génération partielle : uniquement QUALIFICATIONS et USINES
"""

import random
from database import get_connection, clear_all_data
from generators import gen_qualifs, gen_usines, gen_typeu
from config import USER, HOST, PORT, SERVICE

random.seed(31)

def main():
    print(f"Connecting to {USER}@{HOST}:{PORT}/{SERVICE} ...")
    with get_connection() as con:
        cur = con.cursor()

        # Pas de nettoyage, juste insertion
        print("📊 Génération des données...\n")

        # Insertion TYPEU (requis pour USINES via AVOIR_TYPE)
        print("📊 Insertion des TYPEU...")
        typeu = gen_typeu()
        try:
            cur.executemany("INSERT INTO TYPEU(NOMTU) VALUES (:1)", typeu)
            print(f"   ✓ {len(typeu)} types d'usine insérés")
        except Exception as e:
            print(f"   ⚠️  Erreur: {e}")

        # Insertion QUALIFICATIONS
        print("📊 Insertion des QUALIFICATIONS...")
        qualifs = gen_qualifs()
        try:
            cur.executemany("""INSERT INTO QUALIFICATIONS
                               (NOMQ,TAUXMINQ,CODEQ_EST_COMPLETEE)
                               VALUES (:1,:2,:3)""", qualifs)
            cur.execute("SELECT COUNT(*) FROM QUALIFICATIONS")
            count = cur.fetchone()[0]
            print(f"   ✓ {count} qualifications insérées")
        except Exception as e:
            print(f"   ⚠️  Erreur: {e}")

        # Insertion USINES
        print("🏭 Insertion des USINES...")
        usines = gen_usines()
        try:
            cur.executemany("""INSERT INTO USINES(NOMU,RUEU,CPOSTALU,VILLEU,TELU)
                               VALUES (:1,:2,:3,:4,:5)""", usines)
            cur.execute("SELECT COUNT(*) FROM USINES")
            count = cur.fetchone()[0]
            print(f"   ✓ {count} usines insérées")
        except Exception as e:
            print(f"   ⚠️  Erreur: {e}")

        con.commit()
        print("\n✅ Génération partielle terminée.")
        print(f"   → QUALIFICATIONS : {len(qualifs)} entrées")
        print(f"   → USINES : {len(usines)} entrées")

if __name__ == "__main__":
    main()
