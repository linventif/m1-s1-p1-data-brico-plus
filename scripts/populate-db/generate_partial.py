# -*- coding: utf-8 -*-
"""
Génération partielle : TYPEU, TYPEPV, QUALIFICATIONS, USINES et POINTS_DE_VENTE
"""

import random
from database import get_connection, clear_all_data
from generators import gen_qualifs, gen_typeu
from constants import ZONES, ADRESSES_PAR_ZONE, PV_TYPES, PV_NAMES
from utils import phone

random.seed(31)

def gen_usines_par_zone():
    """
    Génère 1 usine par zone en utilisant une adresse unique.
    Retourne (usines_rows, adresses_utilisees)
    """
    rows = []
    adresses_utilisees = []
    
    for zone in ZONES:
        adresses_disponibles = ADRESSES_PAR_ZONE[zone].copy()
        
        if not adresses_disponibles:
            continue
            
        # Sélectionner une adresse aléatoire
        adresse_complete = random.choice(adresses_disponibles)
        adresses_disponibles.remove(adresse_complete)
        
        # Parser l'adresse: "12 Rue des Tanneurs, 67000 Strasbourg"
        parts = adresse_complete.split(", ")
        if len(parts) == 2:
            rue = parts[0][:49]  # Limiter à 49 caractères
            cp_ville = parts[1].split(" ", 1)
            if len(cp_ville) == 2:
                cp = cp_ville[0]
                ville = cp_ville[1]
            else:
                cp = cp_ville[0]
                ville = "Ville"
        else:
            rue = adresse_complete[:49]
            cp = "00000"
            ville = "Ville"
        
        nom_usine = f"Usine {ville}"
        tel = phone(hg=False)
        
        rows.append((nom_usine, rue, cp, ville, tel))
        adresses_utilisees.append({
            'zone': zone,
            'adresse': adresse_complete,
            'nom_usine': nom_usine,
            'ville': ville
        })
        
        # Mettre à jour la liste globale des adresses disponibles
        ADRESSES_PAR_ZONE[zone] = adresses_disponibles
    
    return rows, adresses_utilisees

def gen_points_vente_par_zone():
    """
    Génère des points de vente basés sur les zones avec leurs adresses réelles.
    Utilise les adresses restantes après la génération des usines.
    - 1 PV si zone a <= 5 adresses disponibles
    - 2 PV si zone a entre 6 et 9 adresses disponibles
    - 3 PV si zone a >= 10 adresses disponibles
    Retourne (rows, adresses_utilisees)
    """
    rows = []
    adresses_utilisees = []

    for zone in ZONES:
        adresses_disponibles = ADRESSES_PAR_ZONE[zone].copy()
        nb_adresses = len(adresses_disponibles)

        # Déterminer le nombre de PV selon le nombre d'adresses disponibles
        if nb_adresses <= 5:
            nb_pv = min(1, nb_adresses)
        elif 5 < nb_adresses < 10:
            nb_pv = min(2, nb_adresses)
        else:  # >= 10
            nb_pv = min(3, nb_adresses)

        # Sélectionner des adresses aléatoires pour cette zone
        adresses_selectionnees = random.sample(adresses_disponibles, nb_pv) if nb_pv > 0 else []

        for adresse_complete in adresses_selectionnees:
            # Parser l'adresse
            parts = adresse_complete.split(", ")
            if len(parts) == 2:
                rue = parts[0][:49]
                cp_ville = parts[1].split(" ", 1)
                if len(cp_ville) == 2:
                    cp = cp_ville[0]
                    ville = cp_ville[1]
                else:
                    cp = cp_ville[0]
                    ville = "Ville"
            else:
                rue = adresse_complete[:49]
                cp = "00000"
                ville = "Ville"

            # Choisir un type de PV (GSB plus probable)
            type_pv = random.choices(PV_TYPES, weights=[0.6, 0.4])[0]
            nom_pv = random.choice(PV_NAMES[type_pv])
            tel = phone(hg=False)

            rows.append((nom_pv, rue, cp, ville, tel, type_pv))
            adresses_utilisees.append({
                'zone': zone,
                'adresse': adresse_complete,
                'type_pv': type_pv,
                'nom_pv': nom_pv,
                'ville': ville
            })
            
            # Retirer l'adresse de la liste disponible
            adresses_disponibles.remove(adresse_complete)
        
        # Mettre à jour la liste globale
        ADRESSES_PAR_ZONE[zone] = adresses_disponibles

    return rows, adresses_utilisees


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

        # Insertion des usines (1 par zone)
        usines, adresses_usines = gen_usines_par_zone()
        try:
            cur.executemany("""INSERT INTO USINES(NOMU,RUEU,CPOSTALU,VILLEU,TELU)
                               VALUES (:1,:2,:3,:4,:5)""", usines)
            print(f"✓ {len(usines)} usines insérées (1 par zone)")
        except Exception as e:
            print(f"Erreur USINES: {e}")

        # Insertion des points de vente par zone (avec adresses restantes)
        pvs, adresses_pvs = gen_points_vente_par_zone()
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
