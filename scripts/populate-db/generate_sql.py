# -*- coding: utf-8 -*-
"""
Génération SQL pour TYPEU, QUALIFICATIONS et USINES
"""

import random
from generators import gen_qualifs, gen_usines, gen_typeu

random.seed(31)

def main():
    output_file = "insert_qualifications_usines.sql"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- TYPEU, QUALIFICATIONS et USINES\n\n")
        typeu = gen_typeu()
        for (nom,) in typeu:
            f.write(f"INSERT INTO TYPEU(NOMTU) VALUES ('{nom}');\n")
        f.write("\n")
        qualifs = gen_qualifs()
        for (nom, taux, completee) in qualifs:
            nom_escaped = nom.replace("'", "''")
            completee_val = "NULL" if completee is None else str(completee)
            f.write(f"INSERT INTO QUALIFICATIONS(NOMQ, TAUXMINQ, CODEQ_EST_COMPLETEE) ")
            f.write(f"VALUES ('{nom_escaped}', {taux}, {completee_val});\n")
        f.write("\n")
        usines = gen_usines()
        for (nom, rue, cp, ville, tel) in usines:
            nom_escaped = nom.replace("'", "''")
            rue_escaped = rue.replace("'", "''")
            ville_escaped = ville.replace("'", "''")
            f.write(f"INSERT INTO USINES(NOMU, RUEU, CPOSTALU, VILLEU, TELU) ")
            f.write(f"VALUES ('{nom_escaped}', '{rue_escaped}', '{cp}', '{ville_escaped}', '{tel}');\n")
        f.write("\n")
        f.write("COMMIT;\n")

    print(f"Fichier généré : {output_file}")

if __name__ == "__main__":
    main()
