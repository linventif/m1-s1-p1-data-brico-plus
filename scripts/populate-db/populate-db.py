# -*- coding: utf-8 -*-
"""
Peuplement réaliste de la BD Brico Plus.
Point d'entrée principal.
"""

import random
from database import get_connection, clear_all_data
from generators import *
from relations_generators import *
from utils import generate_calendars
from config import USER, HOST, PORT, SERVICE

random.seed(31)

def main():
    cal1_dates, cal2_dates, cal3, cal4 = generate_calendars()
    cal1 = [(d,) for d in cal1_dates]
    cal2 = [(d,) for d in cal2_dates]
    cal3_rows = [(m, y) for (m, y) in cal3]
    cal4_rows = [(y,) for y in cal4]

    with get_connection() as con:
        cur = con.cursor()

        clear_all_data(cur)

        typeu = gen_typeu()
        cur.executemany("INSERT INTO TYPEU(NOMTU) VALUES (:1)", typeu)
        cur.execute("SELECT CODETU, NOMTU FROM TYPEU ORDER BY CODETU")
        typeu_with_ids = cur.fetchall()

        gammes = gen_gammes()
        cur.executemany("INSERT INTO GAMME(CODEG, NOMG) VALUES (:1,:2)", gammes)

        cur.executemany("INSERT INTO CALENDRIER1(DATEFAB) VALUES (:1)", cal1)
        cur.executemany("INSERT INTO CALENDRIER2(DATEDEBUTDIR) VALUES (:1)", cal2)
        cur.executemany("INSERT INTO CALENDRIER3(MOIS, ANNEE) VALUES (:1,:2)", cal3_rows)
        cur.executemany("INSERT INTO CALENDRIER4(ANNEE) VALUES (:1)", cal4_rows)

        usines = gen_usines()
        cur.executemany("""INSERT INTO USINES(NOMU,RUEU,CPOSTALU,VILLEU,TELU)
                           VALUES (:1,:2,:3,:4,:5)""", usines)
        cur.execute("SELECT CODEU, NOMU FROM USINES ORDER BY CODEU")
        usines_with_ids = cur.fetchall()

        employes = gen_employes()
        cur.executemany("""INSERT INTO EMPLOYES
                           (NOME,PRENOME,RUEPERSE,CPOSTALPERSE,VILLEPERSE,
                            RUEPROE,CPOSTALPROE,VILLEPROE,TELPERSE,TELPROE)
                           VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)""", employes)
        cur.execute("SELECT CODEE FROM EMPLOYES ORDER BY CODEE")
        employes_ids = [row[0] for row in cur.fetchall()]

        qualifs = gen_qualifs()
        cur.executemany("""INSERT INTO QUALIFICATIONS
                           (NOMQ,TAUXMINQ,CODEQ_EST_COMPLETEE)
                           VALUES (:1,:2,:3)""", qualifs)
        cur.execute("SELECT CODEQ FROM QUALIFICATIONS ORDER BY CODEQ")
        qualifs_ids = [row[0] for row in cur.fetchall()]

        departements = gen_departements_with_ids(usines_with_ids)
        cur.executemany("""INSERT INTO DEPARTEMENTS(NOMD,CODEU) VALUES (:1,:2)""", departements)
        cur.execute("SELECT CODED FROM DEPARTEMENTS ORDER BY CODED")
        departements_ids = [row[0] for row in cur.fetchall()]

        pvs = gen_points_vente()
        cur.executemany("""INSERT INTO POINTS_DE_VENTE
                           (NOMPV,RUEPV,CPOSTALPV,VILLEPV,TELPV,TYPEPV)
                           VALUES (:1,:2,:3,:4,:5,:6)""", pvs)
        cur.execute("SELECT CODEPV FROM POINTS_DE_VENTE ORDER BY CODEPV")
        pvs_ids = [row[0] for row in cur.fetchall()]

        produits = gen_produits()
        cur.executemany("""INSERT INTO PRODUITS(NOMP,MARQUEP,CODEG) VALUES (:1,:2,:3)""", produits)
        cur.execute("SELECT CODEP FROM PRODUITS ORDER BY CODEP")
        produits_ids = [row[0] for row in cur.fetchall()]

        posseder = gen_posseder_with_ids(employes_ids, qualifs_ids)
        cur.executemany("INSERT INTO POSSEDER(CODEE,CODEQ) VALUES (:1,:2)", posseder)

        assembler = gen_assembler_with_ids(produits_ids)
        cur.executemany("""INSERT INTO ASSEMBLER(CODEP_EST_COMPOSE,CODEP_COMPOSE,QTE_ASSEMBL)
                           VALUES (:1,:2,:3)""", assembler)

        avoir_type = gen_avoir_type_with_ids(usines_with_ids, typeu_with_ids)
        cur.executemany("INSERT INTO AVOIR_TYPE(CODEU,CODETU) VALUES (:1,:2)", avoir_type)

        diriger = gen_diriger_with_ids(employes_ids, departements_ids, cal2_dates)
        cur.executemany("""INSERT INTO DIRIGER(CODEE,CODED,DATEDEBUTDIR)
                           VALUES (:1,:2,:3)""", diriger)

        autoriser = gen_autoriser_with_ids(qualifs_ids, departements_ids)
        cur.executemany("INSERT INTO AUTORISER(CODEQ,CODED) VALUES (:1,:2)", autoriser)

        fabriquer = gen_fabriquer_with_ids(usines_with_ids, produits_ids, typeu_with_ids, cal1_dates)
        cur.executemany("""INSERT INTO FABRIQUER_ASSEMBLER1(CODEU,CODEP,DATEFAB,QTE_FAB)
                           VALUES (:1,:2,:3,:4)""", fabriquer)

        responsable = gen_responsable_with_ids(employes_ids, gammes, cal4)
        cur.executemany("""INSERT INTO RESPONSABLE(CODEE,CODEG,ANNEE)
                           VALUES (:1,:2,:3)""", responsable)

        payer2 = gen_payer2(gammes)
        cur.executemany("""INSERT INTO PAYER2(CODEG,ANNEE,INDICERETROCESSIONG)
                           VALUES (:1,:2,:3)""", payer2)

        facturer = gen_facturer_with_ids(produits_ids, cal3)
        cur.executemany("""INSERT INTO FACTURER(CODEP,MOIS,ANNEE,PRIXUNITP)
                           VALUES (:1,:2,:3,:4)""", facturer)

        vendre = gen_vendre_with_ids(employes_ids, pvs_ids, produits_ids, cal3)
        cur.executemany("""INSERT INTO VENDRE(CODEE,CODEPV,CODEP,MOIS,ANNEE,QTE_VENDUE)
                           VALUES (:1,:2,:3,:4,:5,:6)""", vendre)

        payer1 = gen_payer1_with_ids(employes_ids, cal4)
        cur.executemany("""INSERT INTO PAYER1(CODEE,ANNEE,FIXEMENSUELE,INDICESALE)
                           VALUES (:1,:2,:3,:4)""", payer1)

        trav_u = gen_travailler_usine_with_ids(employes_ids, departements_ids, cal3)
        cur.executemany("""INSERT INTO TRAVAILLER_USINE(CODEE,CODED,MOIS,ANNEE,NBHEURES_U)
                           VALUES (:1,:2,:3,:4,:5)""", trav_u)

        trav_pv = gen_travailler_pv_with_ids(employes_ids, pvs_ids, cal3)
        cur.executemany("""INSERT INTO TRAVAILLER_PT_VENTE(CODEE,CODEPV,MOIS,ANNEE,NBHEURES_PV)
                           VALUES (:1,:2,:3,:4,:5)""", trav_pv)

        con.commit()

if __name__ == "__main__":
    main()
