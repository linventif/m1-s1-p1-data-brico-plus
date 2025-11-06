
-- ============================================================
-- CAS 1: Employé avec un nombre de ventes de 0 alors qu'il a bien travaillé dans un point de vente
-- ============================================================

DECLARE
  v_codee NUMBER;
  v_coded NUMBER;
  v_codepv NUMBER;
  v_codep NUMBER;
BEGIN
  -- Création de l'employé sans vente
  INSERT INTO EMPLOYES (NomE, PrenomE, TelPersE, TelProE, RuePersE, RueProE, CPostalPersE, CPostalProE, VillePersE, VilleProE)
  VALUES ('Patrick', 'NOSALE', '0600000001', '0500000001', '10 Rue du Doyen Gabriel Marty', '10 Rue du Doyen Gabriel Marty', '31000', '31000', 'Toulouse', 'Toulouse')
  RETURNING CODEE INTO v_codee;

  -- Récupération d'un département existant
  SELECT MIN(CODED) INTO v_coded FROM DEPARTEMENTS WHERE ROWNUM = 1;

  -- Récupération d'un point de vente existant
  SELECT MIN(CODEPV) INTO v_codepv FROM POINTS_DE_VENTE WHERE ROWNUM = 1;

  -- Récupération d'un produit existant
  SELECT MIN(CODEP) INTO v_codep FROM PRODUITS WHERE ROWNUM = 1;

  -- Salaire moyen pour 0 vente
  INSERT INTO PAYER1 (CodeE, Annee, FixeMensuelE, IndiceSalE)
  VALUES (v_codee, 2025, 1900, 1.5);

  -- Heures effectuées en usine (Novembre)
  INSERT INTO TRAVAILLER_USINE (CodeD, CodeE, Mois, Annee, NbHeures_U)
  VALUES (v_coded, v_codee, 11, 2025, 10);

  -- Heures en point de vente (Novembre)
  INSERT INTO TRAVAILLER_PT_VENTE (CodeE, CodePV, Mois, Annee, NbHeures_PV)
  VALUES (v_codee, v_codepv, 11, 2025, 150);

  -- Ventes de 0 en Point de vente (Novembre) - ERREUR
  INSERT INTO VENDRE (CodeE, CodePV, CodeP, Mois, Annee, Qte_Vendue)
  VALUES (v_codee, v_codepv, v_codep, 11, 2025, 0);

  -- Heures effectuées en usine (Octobre)
  INSERT INTO TRAVAILLER_USINE (CodeD, CodeE, Mois, Annee, NbHeures_U)
  VALUES (v_coded, v_codee, 10, 2025, 0);

  -- Heures en point de vente (Octobre)
  INSERT INTO TRAVAILLER_PT_VENTE (CodeE, CodePV, Mois, Annee, NbHeures_PV)
  VALUES (v_codee, v_codepv, 10, 2025, 160);

  -- Ventes de 0 en Point de vente (Octobre) - ERREUR
  INSERT INTO VENDRE (CodeE, CodePV, CodeP, Mois, Annee, Qte_Vendue)
  VALUES (v_codee, v_codepv, v_codep, 10, 2025, 0);

  COMMIT;

  DBMS_OUTPUT.PUT_LINE('✓ CAS 1 créé - Employé NOSALE (ID: ' || v_codee || ') avec 0 ventes');
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    DBMS_OUTPUT.PUT_LINE('✗ ERREUR CAS 1: ' || SQLERRM);
END;
/

-- requette de test
SELECT * FROM VENDRE WHERE CodeE = (SELECT CodeE FROM EMPLOYES WHERE NomE = 'NOSALE');

-- Employé avec aucune heure travaillé et un salaire mensuel fixe

-- Employé sans heure
INSERT INTO EMPLOYES (CodeE, NomE, PrenomE, TelPersE, TelProE, RuePersE, RueProE, CPostalPersE, CPostalProE, VillePersE, VilleProE)
VALUES (12002, 'Robert', 'NOJOB', '0600000002', '0500000002', '2 Rue du Doyen Gabriel Marty', '2 Rue du Doyen Gabriel Marty', '31000', '31000', 'Toulouse', 'Toulouse');

-- Salaire élevé pour l’année
INSERT INTO PAYER1 (CodeE, Annee, FixeMensuelE, IndiceSalE)
VALUES (12002, 2025, 6000, 1.8);

-- Heures effectuées en usine (Novembre)
INSERT INTO TRAVAILLER_USINE (CodeD, CodeE, Mois, Annee, NbHeures_U)
VALUES (2, 12002, 11, 2025, 0);

-- Éventuellement des heures en point de vente (Novembre)
INSERT INTO TRAVAILLER_PT_VENTE (CodeE, CodePV, Mois, Annee, NbHeures_PV)
VALUES (12002, 2, 11, 2025, 0);


-- Heures effectuées en usine (Octobre)
INSERT INTO TRAVAILLER_USINE (CodeD, CodeE, Mois, Annee, NbHeures_U)
VALUES (2, 12002, 10, 2025, 0);

-- Éventuellement des heures en point de vente (Octobre)
INSERT INTO TRAVAILLER_PT_VENTE (CodeE, CodePV, Mois, Annee, NbHeures_PV)
VALUES (12002, 2, 10, 2025, 0);

-- Heures effectuées en usine (Septembre)
INSERT INTO TRAVAILLER_USINE (CodeD, CodeE, Mois, Annee, NbHeures_U)
VALUES (2, 12002, 9, 2025, 0);

-- Éventuellement des heures en point de vente (Septembre)
INSERT INTO TRAVAILLER_PT_VENTE (CodeE, CodePV, Mois, Annee, NbHeures_PV)
VALUES (12002, 2, 9, 2025, 0);


-- Employé qui a travailler uniquement en usine et perçoit les 3 parties du salaire

-- Employé en usine
INSERT INTO EMPLOYES (CodeE, NomE, PrenomE, TelPersE, TelProE, RuePersE, RueProE, CPostalPersE, CPostalProE, VillePersE, VilleProE)
VALUES (12003, 'Victor', 'FACT', '0600000003', '0500000003', '20 Rue du Doyen Gabriel Marty', '20 Rue du Doyen Gabriel Marty', '31000', '31000', 'Toulouse', 'Toulouse');

-- Salaire élevé pour l’année
INSERT INTO PAYER1 (CodeE, Annee, FixeMensuelE, IndiceSalE)
VALUES (12003, 2025, 10000, 2.5);

-- Heures effectuées en usine (Mai)
INSERT INTO TRAVAILLER_USINE (CodeD, CodeE, Mois, Annee, NbHeures_U)
VALUES (2, 12003, 5, 2025, 150);

-- Éventuellement des heures en point de vente (Mai)
INSERT INTO TRAVAILLER_PT_VENTE (CodeE, CodePV, Mois, Annee, NbHeures_PV)
VALUES (12003, 2, 5, 2025, 0);

-- Ventes effectuées en Point de vente (pas sûr)
INSERT INTO VENDRE (CodeE, CodePV, CodeP, Mois, Annee, Qte_Vendue)
VALUES (12003, 1, 20, 2, 2025, 100);


-- Heures effectuées en usine (Avril)
INSERT INTO TRAVAILLER_USINE (CodeD, CodeE, Mois, Annee, NbHeures_U)
VALUES (2, 12003, 4, 2025, 150);

-- Éventuellement des heures en point de vente (Avril)
INSERT INTO TRAVAILLER_PT_VENTE (CodeE, CodePV, Mois, Annee, NbHeures_PV)
VALUES (12003, 2, 4, 2025, 0);

-- Ventes effectuées en Point de vente (pas sûr)
INSERT INTO VENDRE (CodeE, CodePV, CodeP, Mois, Annee, Qte_Vendue)
VALUES (12003, 1, 20, 4, 2025, 100);

-- Heures effectuées en usine (Mars)
INSERT INTO TRAVAILLER_USINE (CodeD, CodeE, Mois, Annee, NbHeures_U)
VALUES (2, 12003, 3, 2025, 148);

-- Éventuellement des heures en point de vente (Mars)
INSERT INTO TRAVAILLER_PT_VENTE (CodeE, CodePV, Mois, Annee, NbHeures_PV)
VALUES (12003, 2, 3, 2025, 0);

-- Ventes effectuées en Point de vente (pas sûr)
INSERT INTO VENDRE (CodeE, CodePV, CodeP, Mois, Annee, Qte_Vendue)
VALUES (12003, 1, 20, 3, 2025, 100);
