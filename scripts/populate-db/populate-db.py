# -*- coding: utf-8 -*-
"""
Peuplement réaliste de la BD Brico Plus.
Point d'entrée principal.
"""

import random
from database import delete_table_data, get_connection, clear_all_data
from generators import *
from relations_generators import *
from utils import genCalendrier
from config import USER, HOST, PORT, SERVICE

random.seed(31)

def main():
    print("\n" + "="*60)
    print("   🔧 BRICO PLUS DATABASE POPULATION")
    print("="*60)

    with get_connection() as con:
        cur = con.cursor()

        print("\n🗑️  Clearing all existing data...")
        clear_all_data(cur)
        print("  ✓ Database cleared")

        print("\n📅 Generating calendars...")
        cal_yyyy_mm_dd = genCalendrier()
        cal_yyyy_mm_dd = [(d,) for d in cal_yyyy_mm_dd]
        cal_yyyy = genCalendrier(format="%Y")
        cal_yyyy = list(set([(d.year,) for d in cal_yyyy]))
        cal_split = genCalendrier(split=True)
        print("  ✓ Calendars generated")

        # '''

        print("\n🏷️  Generating factory types...")
        typeu = gen_typeu()
        cur.executemany("INSERT INTO TYPEU(NOMTU) VALUES (:1)", typeu)
        cur.execute("SELECT CODETU, NOMTU FROM TYPEU ORDER BY CODETU")
        typeu_with_ids = cur.fetchall()
        print(f"  ✓ Completed: {len(typeu)} factory types")

        print("\n📦 Generating product ranges...")
        gammes = gen_gammes()
        cur.executemany("INSERT INTO GAMME(CODEG, NOMG) VALUES (:1,:2)", gammes)
        print(f"  ✓ Completed: {len(gammes)} product ranges")

        print("\n📅 Inserting calendar data...")
        cur.executemany("INSERT INTO CALENDRIER1(DATEFAB) VALUES (:1)", cal_yyyy_mm_dd)
        cur.executemany("INSERT INTO CALENDRIER2(DATEDEBUTDIR) VALUES (:1)", cal_yyyy_mm_dd)
        cur.executemany("INSERT INTO CALENDRIER3(MOIS, ANNEE) VALUES (:1,:2)", cal_split)
        cur.executemany("INSERT INTO CALENDRIER4(ANNEE) VALUES (:1)", cal_yyyy)
        print(f"  ✓ Completed: {len(cal_yyyy_mm_dd)} dates, {len(cal_yyyy)} years")

        # Generate factories first
        usines = gen_usines()
        cur.executemany("""INSERT INTO USINES(NOMU,RUEU,CPOSTALU,VILLEU,TELU)
                           VALUES (:1,:2,:3,:4,:5)""", usines)
        cur.execute("SELECT CODEU, NOMU FROM USINES ORDER BY CODEU")
        usines_with_ids = cur.fetchall()
        cur.execute("SELECT CODEU, NOMU, RUEU, CPOSTALU, VILLEU FROM USINES ORDER BY CODEU")
        usines_full_data = cur.fetchall()

        # Generate points of sale with address info BEFORE factory types
        pvs, pv_info = gen_points_vente()
        cur.executemany("""INSERT INTO POINTS_DE_VENTE
                           (NOMPV,RUEPV,CPOSTALPV,VILLEPV,TELPV,TYPEPV)
                           VALUES (:1,:2,:3,:4,:5,:6)""", pvs)
        cur.execute("SELECT CODEPV FROM POINTS_DE_VENTE ORDER BY CODEPV")
        pvs_ids = [row[0] for row in cur.fetchall()]

        # Generate factory types with addresses and get factory info (classification and size)
        print("\n🏭 Classifying factories...")
        avoir_type, factory_info = gen_avoir_type_with_ids(usines_with_ids, typeu_with_ids, usines_full_data)
        cur.executemany("INSERT INTO AVOIR_TYPE(CODEU,CODETU) VALUES (:1,:2)", avoir_type)

        # Print factory classification summary
        print("\n" + "┌" + "─"*58 + "┐")
        print("│  📊 Factory Classification Summary" + " "*23 + "│")
        print("├" + "─"*58 + "┤")
        for u_id, info in sorted(factory_info.items()):
            usine_nom = next((nom for uid, nom in usines_with_ids if uid == u_id), f"Usine {u_id}")[:30]
            print(f"│  {usine_nom:<30} │")
            print(f"│    Classification: {info['classification']:<26} │")
            print(f"│    Size: {info['taille']:<39} employees │")
            print(f"│    Types: {', '.join(info['types'])[:36]:<36} │")
            print("├" + "─"*58 + "┤")
        print("└" + "─"*58 + "┘")

        # Generate employees based on factory sizes and PV types
        employes, employee_workplace = gen_employes_by_factory_size(factory_info, pv_info)
        cur.executemany("""INSERT INTO EMPLOYES
                           (NOME,PRENOME,RUEPERSE,CPOSTALPERSE,VILLEPERSE,
                            RUEPROE,CPOSTALPROE,VILLEPROE,TELPERSE,TELPROE)
                           VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)""", employes)
        cur.execute("SELECT CODEE FROM EMPLOYES ORDER BY CODEE")
        employes_ids = [row[0] for row in cur.fetchall()]

        print("\n🎓 Generating qualifications...")
        qualifs = gen_qualifs()
        # Insert with CODEQ_EST_COMPLETEE as None
        qualifs_insert = [(diplome[:50], taux, None) for diplome, taux, base_diplome in qualifs]
        cur.executemany("""INSERT INTO QUALIFICATIONS
                           (NOMQ,TAUXMINQ,CODEQ_EST_COMPLETEE)
                           VALUES (:1,:2,:3)""", qualifs_insert)
        cur.execute("SELECT CODEQ, NOMQ FROM QUALIFICATIONS ORDER BY CODEQ")
        qualifs_rows = cur.fetchall()
        # Build a mapping from NOMQ to CODEQ
        nomq_to_codeq = {row[1]: row[0] for row in qualifs_rows}
        # Now update CODEQ_EST_COMPLETEE for each qualification
        qualifs_to_update = []
        for i, q in enumerate(qualifs):
            diplome, taux, base_diplome = q
            codeq = nomq_to_codeq[diplome[:50]]
            base_codeq = nomq_to_codeq.get(base_diplome[:50], codeq)
            if base_codeq != codeq:
                qualifs_to_update.append((base_codeq, codeq))
        if qualifs_to_update:
            cur.executemany("UPDATE QUALIFICATIONS SET CODEQ_EST_COMPLETEE = :1 WHERE CODEQ = :2", qualifs_to_update)
        print(f"  ✓ Completed: {len(qualifs)} qualifications")

        qualifs_ids = [row[0] for row in qualifs_rows]

        print("\n👤 Assigning qualifications to employees...")
        posseder = gen_posseder_with_ids(employes_ids, qualifs_ids)
        cur.executemany("INSERT INTO POSSEDER(CODEE,CODEQ) VALUES (:1,:2)", posseder)
        print(f"  ✓ Completed: {len(posseder)} employee-qualification assignments")

        print("\n🏢 Generating departments...")
        departements = gen_departements_with_ids(usines_with_ids)
        cur.executemany("""INSERT INTO DEPARTEMENTS(NOMD,CODEU) VALUES (:1,:2)""", departements)
        cur.execute("SELECT CODED, NOMD, CODEU FROM DEPARTEMENTS ORDER BY CODED")
        departements_rows = cur.fetchall()
        print(f"  ✓ Completed: {len(departements)} departments")

        produits = gen_produits()
        cur.executemany("""INSERT INTO PRODUITS(NOMP,MARQUEP,CODEG) VALUES (:1,:2,:3)""", produits)
        cur.execute("SELECT CODEP, NOMP, MARQUEP, CODEG FROM PRODUITS ORDER BY CODEP")
        produits_rows = cur.fetchall()

        print("\n👨‍💼 Assigning product range managers...")
        responsable = gen_responsable_with_ids(employes_ids, gammes, cal_yyyy)
        cur.executemany("""INSERT INTO RESPONSABLE(CODEE,CODEG,ANNEE)
                           VALUES (:1,:2,:3)""", responsable)
        print(f"  ✓ Completed: {len(responsable)} manager assignments")

        print("\n🎯 Assigning department directors...")
        departements_ids = [row[0] for row in departements_rows]
        diriger = gen_diriger_with_ids(employes_ids, departements_ids, cal_yyyy_mm_dd)
        cur.executemany("""INSERT INTO DIRIGER(CODEE,CODED,DATEDEBUTDIR)
                           VALUES (:1,:2,:3)""", diriger)
        print(f"  ✓ Completed: {len(diriger)} director assignments")

        print("\n💰 Generating employee salaries...")
        payer1 = gen_payer1_with_ids(employes_ids, cal_yyyy)
        cur.executemany("""INSERT INTO PAYER1(CODEE,ANNEE,FIXEMENSUELE,INDICESALE)
                           VALUES (:1,:2,:3,:4)""", payer1)
        print(f"  ✓ Completed: {len(payer1)} salary records")

        print("\n✅ Generating department-qualification authorizations...")
        autoriser = gen_autoriser_with_ids(qualifs_rows, departements_rows)
        cur.executemany("INSERT INTO AUTORISER(CODEQ,CODED) VALUES (:1,:2)", autoriser)
        print(f"  ✓ Completed: {len(autoriser)} authorization rules")

        print("\n🔧 Generating product assembly relationships...")
        assembler = gen_assembler_with_ids(produits_rows)
        cur.executemany("""INSERT INTO ASSEMBLER(CODEP_EST_COMPOSE,CODEP_COMPOSE,QTE_ASSEMBL)
                           VALUES (:1,:2,:3)""", assembler)
        print(f"  ✓ Completed: {len(assembler)} assembly relationships")
        # '''

        # fabriquer = gen_fabriquer_with_ids(usines_with_ids, produits_ids, typeu_with_ids, cal1_dates)
        # cur.executemany("""INSERT INTO FABRIQUER_ASSEMBLER1(CODEU,CODEP,DATEFAB,QTE_FAB)
        #                    VALUES (:1,:2,:3,:4)""", fabriquer)

        # payer2 = gen_payer2(gammes)
        # cur.executemany("""INSERT INTO PAYER2(CODEG,ANNEE,INDICERETROCESSIONG)
        #                    VALUES (:1,:2,:3)""", payer2)

        # facturer = gen_facturer_with_ids(produits_ids, cal3)
        # cur.executemany("""INSERT INTO FACTURER(CODEP,MOIS,ANNEE,PRIXUNITP)
        #                    VALUES (:1,:2,:3,:4)""", facturer)

        # vendre = gen_vendre_with_ids(employes_ids, pvs_ids, produits_ids, cal3)
        # cur.executemany("""INSERT INTO VENDRE(CODEE,CODEPV,CODEP,MOIS,ANNEE,QTE_VENDUE)
        #                    VALUES (:1,:2,:3,:4,:5,:6)""", vendre)

        # trav_u = gen_travailler_usine_with_ids(employes_ids, departements_ids, cal3)
        # cur.executemany("""INSERT INTO TRAVAILLER_USINE(CODEE,CODED,MOIS,ANNEE,NBHEURES_U)
        #                    VALUES (:1,:2,:3,:4,:5)""", trav_u)

        # trav_pv = gen_travailler_pv_with_ids(employes_ids, pvs_ids, cal3)
        # cur.executemany("""INSERT INTO TRAVAILLER_PT_VENTE(CODEE,CODEPV,MOIS,ANNEE,NBHEURES_PV)
        #                    VALUES (:1,:2,:3,:4,:5)""", trav_pv)

        print("\n💾 Committing all changes to database...")
        con.commit()
        print("  ✓ All data committed successfully")

        print("\n" + "="*60)
        print("   ✨ DATABASE POPULATION COMPLETED SUCCESSFULLY ✨")
        print("="*60 + "\n")

if __name__ == "__main__":
    main()
