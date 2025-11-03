# -*- coding: utf-8 -*-
"""
Génération partielle : TYPEU, QUALIFICATIONS et USINES
"""

import random
from database import get_connection
from generators import gen_qualifs, gen_usines, gen_typeu

random.seed(31)

def main():
    with get_connection() as con:
        cur = con.cursor()

        typeu = gen_typeu()
        try:
            cur.executemany("INSERT INTO TYPEU(NOMTU) VALUES (:1)", typeu)
        except Exception as e:
            print(f"Erreur TYPEU: {e}")

        qualifs = gen_qualifs()
        try:
            cur.executemany("""INSERT INTO QUALIFICATIONS
                               (NOMQ,TAUXMINQ,CODEQ_EST_COMPLETEE)
                               VALUES (:1,:2,:3)""", qualifs)
        except Exception as e:
            print(f"Erreur QUALIFICATIONS: {e}")

        usines = gen_usines()
        try:
            cur.executemany("""INSERT INTO USINES(NOMU,RUEU,CPOSTALU,VILLEU,TELU)
                               VALUES (:1,:2,:3,:4,:5)""", usines)
        except Exception as e:
            print(f"Erreur USINES: {e}")

        con.commit()

if __name__ == "__main__":
    main()
