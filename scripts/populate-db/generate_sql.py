# -*- coding: utf-8 -*-
"""
Génération des instructions SQL INSERT pour QUALIFICATIONS et USINES
"""

import random
from generators import gen_qualifs, gen_usines, gen_typeu

random.seed(31)

def main():
    print("📊 Génération des instructions SQL...\n")
    
    output_file = "insert_qualifications_usines.sql"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("-- Instructions SQL pour peupler QUALIFICATIONS et USINES\n")
        f.write("-- Généré automatiquement\n\n")
        
        # TYPEU
        f.write("-- ============================================\n")
        f.write("-- TYPEU\n")
        f.write("-- ============================================\n\n")
        typeu = gen_typeu()
        for (nom,) in typeu:
            f.write(f"INSERT INTO TYPEU(NOMTU) VALUES ('{nom}');\n")
        f.write(f"\n-- {len(typeu)} types d'usine\n\n")
        
        # QUALIFICATIONS
        f.write("-- ============================================\n")
        f.write("-- QUALIFICATIONS\n")
        f.write("-- ============================================\n\n")
        qualifs = gen_qualifs()
        for (nom, taux, completee) in qualifs:
            # Échapper les apostrophes dans les noms
            nom_escaped = nom.replace("'", "''")
            completee_val = "NULL" if completee is None else str(completee)
            f.write(f"INSERT INTO QUALIFICATIONS(NOMQ, TAUXMINQ, CODEQ_EST_COMPLETEE) ")
            f.write(f"VALUES ('{nom_escaped}', {taux}, {completee_val});\n")
        f.write(f"\n-- {len(qualifs)} qualifications\n\n")
        
        # USINES
        f.write("-- ============================================\n")
        f.write("-- USINES\n")
        f.write("-- ============================================\n\n")
        usines = gen_usines()
        for (nom, rue, cp, ville, tel) in usines:
            # Échapper les apostrophes
            nom_escaped = nom.replace("'", "''")
            rue_escaped = rue.replace("'", "''")
            ville_escaped = ville.replace("'", "''")
            f.write(f"INSERT INTO USINES(NOMU, RUEU, CPOSTALU, VILLEU, TELU) ")
            f.write(f"VALUES ('{nom_escaped}', '{rue_escaped}', '{cp}', '{ville_escaped}', '{tel}');\n")
        f.write(f"\n-- {len(usines)} usines\n\n")
        
        # Commit
        f.write("COMMIT;\n")
    
    print(f"✅ Fichier généré : {output_file}")
    print(f"   → TYPEU : {len(typeu)} entrées")
    print(f"   → QUALIFICATIONS : {len(qualifs)} entrées")
    print(f"   → USINES : {len(usines)} entrées")
    print(f"\nVous pouvez maintenant exécuter ce fichier SQL dans votre base de données.")

if __name__ == "__main__":
    main()
