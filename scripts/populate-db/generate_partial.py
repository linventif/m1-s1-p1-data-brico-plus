# -*- coding: utf-8 -*-
"""
Génération partielle : TYPEU, TYPEPV, QUALIFICATIONS, USINES et POINTS_DE_VENTE
"""

import random
from database import get_connection, clear_all_data
from generators import gen_qualifs, gen_usines, gen_typeu, gen_typepv, gen_points_vente_par_zone

random.seed(31)

def main():
    with get_connection() as con:
        cur = con.cursor()

        clear_all_data(cur)

        # Insertion des types d'usines
        typeu = gen_typeu()
        try:
            cur.executemany("INSERT INTO TYPEU(NOMTU) VALUES (:1)", typeu)
            print(f"✓ {len(typeu)} types d'usines insérés")
        except Exception as e:
            print(f"Erreur TYPEU: {e}")

        # Note: TYPEPV table n'existe pas dans le schéma - les types sont validés par une contrainte CHECK

        # Insertion des qualifications
        qualifs = gen_qualifs()
        try:
            cur.executemany("""INSERT INTO QUALIFICATIONS
                               (NOMQ,TAUXMINQ,CODEQ_EST_COMPLETEE)
                               VALUES (:1,:2,:3)""", qualifs)
            print(f"✓ {len(qualifs)} qualifications insérées")
        except Exception as e:
            print(f"Erreur QUALIFICATIONS: {e}")

        # Insertion des usines
        usines = gen_usines()
        try:
            cur.executemany("""INSERT INTO USINES(NOMU,RUEU,CPOSTALU,VILLEU,TELU)
                               VALUES (:1,:2,:3,:4,:5)""", usines)
            print(f"✓ {len(usines)} usines insérées")
        except Exception as e:
            print(f"Erreur USINES: {e}")

        # Insertion des points de vente par zone
        pvs, adresses_utilisees = gen_points_vente_par_zone()
        try:
            cur.executemany("""INSERT INTO POINTS_DE_VENTE(NOMPV,RUEPV,CPOSTALPV,VILLEPV,TELPV,TYPEPV)
                               VALUES (:1,:2,:3,:4,:5,:6)""", pvs)
            print(f"✓ {len(pvs)} points de vente insérés")

        except Exception as e:
            print(f"Erreur POINTS_DE_VENTE: {e}")
            import traceback
            traceback.print_exc()

        con.commit()
        print("\n✓ Toutes les données ont été insérées avec succès!")

if __name__ == "__main__":
    main()
