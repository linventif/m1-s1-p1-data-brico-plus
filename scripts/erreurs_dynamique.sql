-- ============================================================
-- 🚨 SCRIPT DE TEST D'ERREURS - Cas d'anomalies métier
-- ============================================================
-- Ce script insère des données qui respectent les contraintes techniques
-- mais violent les règles métier (anomalies logiques à détecter)
-- Toutes les valeurs sont récupérées dynamiquement depuis la base
-- ============================================================

SET SERVEROUTPUT ON

-- ============================================================
-- CAS 1: Employé avec très peu de ventes malgré beaucoup d'heures en point de vente
-- ============================================================

DECLARE
  v_codee NUMBER;
  v_coded NUMBER;
  v_codepv NUMBER;
  v_codep NUMBER;
BEGIN
  DBMS_OUTPUT.PUT_LINE('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  DBMS_OUTPUT.PUT_LINE('🚨 CAS 1: Employé avec très peu de ventes malgré 160h en PV');
  DBMS_OUTPUT.PUT_LINE('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  -- Création de l'employé
  INSERT INTO EMPLOYES (NomE, PrenomE, TelPersE, TelProE, RuePersE, RueProE, CPostalPersE, CPostalProE, VillePersE, VilleProE)
  VALUES ('Patrick', 'LOWSALES', '0600000001', '0500000001', '10 Rue du Doyen Gabriel Marty', '10 Rue du Doyen Gabriel Marty', '31000', '31000', 'Toulouse', 'Toulouse')
  RETURNING CODEE INTO v_codee;
  DBMS_OUTPUT.PUT_LINE('  → Employé créé: LOWSALES Patrick (ID: ' || v_codee || ')');

  -- Récupération dynamique des IDs
  SELECT MIN(CODED) INTO v_coded FROM DEPARTEMENTS;
  SELECT MIN(CODEPV) INTO v_codepv FROM POINTS_DE_VENTE;
  SELECT MIN(CODEP) INTO v_codep FROM PRODUITS;

  DBMS_OUTPUT.PUT_LINE('  → Département: ' || v_coded || ' | PV: ' || v_codepv || ' | Produit: ' || v_codep);

  -- Salaire fixe
  INSERT INTO PAYER1 (CodeE, Annee, FixeMensuelE, IndiceSalE)
  VALUES (v_codee, 2025, 1900, 1.5);

  -- Novembre: beaucoup d'heures en PV mais très peu de ventes
  INSERT INTO TRAVAILLER_USINE (CodeD, CodeE, Mois, Annee, NbHeures_U)
  VALUES (v_coded, v_codee, 11, 2025, 5);

  INSERT INTO TRAVAILLER_PT_VENTE (CodeE, CodePV, Mois, Annee, NbHeures_PV)
  VALUES (v_codee, v_codepv, 11, 2025, 160);

  -- ⚠️ ANOMALIE: Seulement 1 vente pour 160h de travail!
  INSERT INTO VENDRE (CodeE, CodePV, CodeP, Mois, Annee, Qte_Vendue)
  VALUES (v_codee, v_codepv, v_codep, 11, 2025, 1);
  DBMS_OUTPUT.PUT_LINE('  ⚠️  Novembre: 160h PV mais seulement 1 vente (ANOMALIE!)');

  -- Octobre: même problème
  INSERT INTO TRAVAILLER_USINE (CodeD, CodeE, Mois, Annee, NbHeures_U)
  VALUES (v_coded, v_codee, 10, 2025, 3);

  INSERT INTO TRAVAILLER_PT_VENTE (CodeE, CodePV, Mois, Annee, NbHeures_PV)
  VALUES (v_codee, v_codepv, 10, 2025, 165);

  INSERT INTO VENDRE (CodeE, CodePV, CodeP, Mois, Annee, Qte_Vendue)
  VALUES (v_codee, v_codepv, v_codep, 10, 2025, 2);
  DBMS_OUTPUT.PUT_LINE('  ⚠️  Octobre: 165h PV mais seulement 2 ventes (ANOMALIE!)');

  COMMIT;
  DBMS_OUTPUT.PUT_LINE('✓ CAS 1 terminé - Performance anormalement basse');
  DBMS_OUTPUT.PUT_LINE('');
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    DBMS_OUTPUT.PUT_LINE('✗ ERREUR CAS 1: ' || SQLERRM);
    DBMS_OUTPUT.PUT_LINE('');
END;
/

-- ============================================================
-- CAS 2: Employé avec très peu d'heures mais salaire très élevé
-- ============================================================

DECLARE
  v_codee NUMBER;
  v_coded NUMBER;
  v_codepv NUMBER;
BEGIN
  DBMS_OUTPUT.PUT_LINE('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  DBMS_OUTPUT.PUT_LINE('🚨 CAS 2: Salaire élevé avec très peu d''heures travaillées');
  DBMS_OUTPUT.PUT_LINE('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  -- Création de l'employé
  INSERT INTO EMPLOYES (NomE, PrenomE, TelPersE, TelProE, RuePersE, RueProE, CPostalPersE, CPostalProE, VillePersE, VilleProE)
  VALUES ('Robert', 'MINIJOB', '0600000002', '0500000002', '2 Rue du Doyen Gabriel Marty', '2 Rue du Doyen Gabriel Marty', '31000', '31000', 'Toulouse', 'Toulouse')
  RETURNING CODEE INTO v_codee;
  DBMS_OUTPUT.PUT_LINE('  → Employé créé: MINIJOB Robert (ID: ' || v_codee || ')');

  -- Récupération dynamique (départements et PV différents si possible)
  SELECT MAX(CODED) INTO v_coded FROM (
    SELECT CODED FROM DEPARTEMENTS ORDER BY CODED FETCH FIRST 2 ROWS ONLY
  );
  IF v_coded IS NULL THEN
    SELECT MIN(CODED) INTO v_coded FROM DEPARTEMENTS;
  END IF;

  SELECT MAX(CODEPV) INTO v_codepv FROM (
    SELECT CODEPV FROM POINTS_DE_VENTE ORDER BY CODEPV FETCH FIRST 2 ROWS ONLY
  );
  IF v_codepv IS NULL THEN
    SELECT MIN(CODEPV) INTO v_codepv FROM POINTS_DE_VENTE;
  END IF;

  DBMS_OUTPUT.PUT_LINE('  → Département: ' || v_coded || ' | PV: ' || v_codepv);

  -- ⚠️ ANOMALIE: Salaire très élevé pour quelqu'un qui travaille peu
  INSERT INTO PAYER1 (CodeE, Annee, FixeMensuelE, IndiceSalE)
  VALUES (v_codee, 2025, 8500, 2.2);
  DBMS_OUTPUT.PUT_LINE('  ⚠️  Salaire: 8500€/mois avec indice 2.2 (ÉLEVÉ!)');

  -- Novembre: Très peu d'heures
  INSERT INTO TRAVAILLER_USINE (CodeD, CodeE, Mois, Annee, NbHeures_U)
  VALUES (v_coded, v_codee, 11, 2025, 2);

  INSERT INTO TRAVAILLER_PT_VENTE (CodeE, CodePV, Mois, Annee, NbHeures_PV)
  VALUES (v_codee, v_codepv, 11, 2025, 1);
  DBMS_OUTPUT.PUT_LINE('  → Novembre: seulement 3h totales');

  -- Octobre: Très peu d'heures
  INSERT INTO TRAVAILLER_USINE (CodeD, CodeE, Mois, Annee, NbHeures_U)
  VALUES (v_coded, v_codee, 10, 2025, 1);

  INSERT INTO TRAVAILLER_PT_VENTE (CodeE, CodePV, Mois, Annee, NbHeures_PV)
  VALUES (v_codee, v_codepv, 10, 2025, 2);
  DBMS_OUTPUT.PUT_LINE('  → Octobre: seulement 3h totales');

  -- Septembre: Très peu d'heures
  INSERT INTO TRAVAILLER_USINE (CodeD, CodeE, Mois, Annee, NbHeures_U)
  VALUES (v_coded, v_codee, 9, 2025, 1);

  INSERT INTO TRAVAILLER_PT_VENTE (CodeE, CodePV, Mois, Annee, NbHeures_PV)
  VALUES (v_codee, v_codepv, 9, 2025, 1);
  DBMS_OUTPUT.PUT_LINE('  → Septembre: seulement 2h totales');
  DBMS_OUTPUT.PUT_LINE('  ⚠️  ANOMALIE: ~8h/mois pour 8500€ de fixe!');

  COMMIT;
  DBMS_OUTPUT.PUT_LINE('✓ CAS 2 terminé - Ratio salaire/heures anormal');
  DBMS_OUTPUT.PUT_LINE('');
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    DBMS_OUTPUT.PUT_LINE('✗ ERREUR CAS 2: ' || SQLERRM);
    DBMS_OUTPUT.PUT_LINE('');
END;
/

-- ============================================================
-- CAS 3: Employé travaillant uniquement en usine avec de nombreuses ventes
-- ============================================================

DECLARE
  v_codee NUMBER;
  v_coded NUMBER;
  v_codepv NUMBER;
  v_codep NUMBER;
BEGIN
  DBMS_OUTPUT.PUT_LINE('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  DBMS_OUTPUT.PUT_LINE('🚨 CAS 3: Employé usine uniquement avec ventes comptabilisées');
  DBMS_OUTPUT.PUT_LINE('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  -- Création de l'employé
  INSERT INTO EMPLOYES (NomE, PrenomE, TelPersE, TelProE, RuePersE, RueProE, CPostalPersE, CPostalProE, VillePersE, VilleProE)
  VALUES ('Victor', 'FACTORYONLY', '0600000003', '0500000003', '20 Rue du Doyen Gabriel Marty', '20 Rue du Doyen Gabriel Marty', '31000', '31000', 'Toulouse', 'Toulouse')
  RETURNING CODEE INTO v_codee;
  DBMS_OUTPUT.PUT_LINE('  → Employé créé: FACTORYONLY Victor (ID: ' || v_codee || ')');

  -- Récupération dynamique (3ème département si possible)
  BEGIN
    SELECT CODED INTO v_coded FROM (
      SELECT CODED FROM DEPARTEMENTS ORDER BY CODED
    ) WHERE ROWNUM = 1 OFFSET 2 ROWS;
  EXCEPTION
    WHEN NO_DATA_FOUND THEN
      SELECT MIN(CODED) INTO v_coded FROM DEPARTEMENTS;
  END;

  SELECT MIN(CODEPV) INTO v_codepv FROM POINTS_DE_VENTE;

  BEGIN
    SELECT CODEP INTO v_codep FROM (
      SELECT CODEP FROM PRODUITS ORDER BY CODEP
    ) WHERE ROWNUM = 1 OFFSET 1 ROWS;
  EXCEPTION
    WHEN NO_DATA_FOUND THEN
      SELECT MIN(CODEP) INTO v_codep FROM PRODUITS;
  END;

  DBMS_OUTPUT.PUT_LINE('  → Département: ' || v_coded || ' | PV: ' || v_codepv || ' | Produit: ' || v_codep);

  -- Salaire très élevé
  INSERT INTO PAYER1 (CodeE, Annee, FixeMensuelE, IndiceSalE)
  VALUES (v_codee, 2025, 10000, 2.5);
  DBMS_OUTPUT.PUT_LINE('  → Salaire: 10000€/mois avec indice 2.5');

  -- Mai: Travail en usine uniquement
  INSERT INTO TRAVAILLER_USINE (CodeD, CodeE, Mois, Annee, NbHeures_U)
  VALUES (v_coded, v_codee, 5, 2025, 150);

  INSERT INTO TRAVAILLER_PT_VENTE (CodeE, CodePV, Mois, Annee, NbHeures_PV)
  VALUES (v_codee, v_codepv, 5, 2025, 1);
  DBMS_OUTPUT.PUT_LINE('  → Mai: 150h usine + 1h PV');

  -- ⚠️ ANOMALIE: Beaucoup de ventes alors qu'il ne travaille presque pas en PV
  INSERT INTO VENDRE (CodeE, CodePV, CodeP, Mois, Annee, Qte_Vendue)
  VALUES (v_codee, v_codepv, v_codep, 5, 2025, 150);
  DBMS_OUTPUT.PUT_LINE('  ⚠️  Mai: 150 ventes pour 1h en PV (ANOMALIE!)');

  -- Avril: Travail en usine uniquement
  INSERT INTO TRAVAILLER_USINE (CodeD, CodeE, Mois, Annee, NbHeures_U)
  VALUES (v_coded, v_codee, 4, 2025, 155);

  INSERT INTO TRAVAILLER_PT_VENTE (CodeE, CodePV, Mois, Annee, NbHeures_PV)
  VALUES (v_codee, v_codepv, 4, 2025, 2);
  DBMS_OUTPUT.PUT_LINE('  → Avril: 155h usine + 2h PV');

  INSERT INTO VENDRE (CodeE, CodePV, CodeP, Mois, Annee, Qte_Vendue)
  VALUES (v_codee, v_codepv, v_codep, 4, 2025, 120);
  DBMS_OUTPUT.PUT_LINE('  ⚠️  Avril: 120 ventes pour 2h en PV (ANOMALIE!)');

  -- Mars: Travail en usine uniquement
  INSERT INTO TRAVAILLER_USINE (CodeD, CodeE, Mois, Annee, NbHeures_U)
  VALUES (v_coded, v_codee, 3, 2025, 148);

  INSERT INTO TRAVAILLER_PT_VENTE (CodeE, CodePV, Mois, Annee, NbHeures_PV)
  VALUES (v_codee, v_codepv, 3, 2025, 1);
  DBMS_OUTPUT.PUT_LINE('  → Mars: 148h usine + 1h PV');

  INSERT INTO VENDRE (CodeE, CodePV, CodeP, Mois, Annee, Qte_Vendue)
  VALUES (v_codee, v_codepv, v_codep, 3, 2025, 100);
  DBMS_OUTPUT.PUT_LINE('  ⚠️  Mars: 100 ventes pour 1h en PV (ANOMALIE!)');

  COMMIT;
  DBMS_OUTPUT.PUT_LINE('✓ CAS 3 terminé - Ventes incohérentes avec heures PV');
  DBMS_OUTPUT.PUT_LINE('');
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    DBMS_OUTPUT.PUT_LINE('✗ ERREUR CAS 3: ' || SQLERRM);
    DBMS_OUTPUT.PUT_LINE('');
END;
/

-- ============================================================
-- 📊 RÉSUMÉ DES ERREURS INSÉRÉES
-- ============================================================

DECLARE
  v_count_cas1 NUMBER;
  v_count_cas2 NUMBER;
  v_count_cas3 NUMBER;
  v_total_ventes_cas1 NUMBER;
  v_total_heures_cas2 NUMBER;
  v_total_ventes_cas3 NUMBER;
BEGIN
  DBMS_OUTPUT.PUT_LINE('');
  DBMS_OUTPUT.PUT_LINE('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  DBMS_OUTPUT.PUT_LINE('📊 RÉSUMÉ DES ANOMALIES INSÉRÉES');
  DBMS_OUTPUT.PUT_LINE('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  -- CAS 1: Peu de ventes malgré beaucoup d'heures
  SELECT COUNT(DISTINCT E.CODEE), COALESCE(SUM(V.QTE_VENDUE), 0)
  INTO v_count_cas1, v_total_ventes_cas1
  FROM EMPLOYES E
  LEFT JOIN VENDRE V ON E.CODEE = V.CODEE
  WHERE E.PRENOME = 'LOWSALES';

  IF v_count_cas1 > 0 THEN
    DBMS_OUTPUT.PUT_LINE('✓ CAS 1 (LOWSALES): ' || v_count_cas1 || ' employé(s)');
    DBMS_OUTPUT.PUT_LINE('  → Total ventes: ' || v_total_ventes_cas1 || ' pour ~325h en PV');
  END IF;

  -- CAS 2: Salaire élevé avec peu d'heures
  SELECT COUNT(DISTINCT E.CODEE),
         COALESCE(SUM(TU.NBHEURES_U), 0) + COALESCE(SUM(TPV.NBHEURES_PV), 0)
  INTO v_count_cas2, v_total_heures_cas2
  FROM EMPLOYES E
  LEFT JOIN TRAVAILLER_USINE TU ON E.CODEE = TU.CODEE
  LEFT JOIN TRAVAILLER_PT_VENTE TPV ON E.CODEE = TPV.CODEE
  WHERE E.PRENOME = 'MINIJOB';

  IF v_count_cas2 > 0 THEN
    DBMS_OUTPUT.PUT_LINE('✓ CAS 2 (MINIJOB): ' || v_count_cas2 || ' employé(s)');
    DBMS_OUTPUT.PUT_LINE('  → Total heures: ' || v_total_heures_cas2 || 'h pour 8500€/mois');
  END IF;

  -- CAS 3: Employé usine avec ventes
  SELECT COUNT(DISTINCT E.CODEE), COALESCE(SUM(V.QTE_VENDUE), 0)
  INTO v_count_cas3, v_total_ventes_cas3
  FROM EMPLOYES E
  LEFT JOIN VENDRE V ON E.CODEE = V.CODEE
  WHERE E.PRENOME = 'FACTORYONLY';

  IF v_count_cas3 > 0 THEN
    DBMS_OUTPUT.PUT_LINE('✓ CAS 3 (FACTORYONLY): ' || v_count_cas3 || ' employé(s)');
    DBMS_OUTPUT.PUT_LINE('  → Total ventes: ' || v_total_ventes_cas3 || ' pour ~4h en PV');
  END IF;

  DBMS_OUTPUT.PUT_LINE('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  DBMS_OUTPUT.PUT_LINE('🎯 Insertion des anomalies terminée');
  DBMS_OUTPUT.PUT_LINE('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  DBMS_OUTPUT.PUT_LINE('');
END;
/

-- ============================================================
-- 🔍 REQUÊTES DE VÉRIFICATION DES ANOMALIES
-- ============================================================

SELECT
    E.CODEE,
    E.NOME || ' ' || E.PRENOME AS "Nom Complet",
    P.FIXEMENSUELE AS "Salaire Fixe",
    P.INDICESALE AS "Indice Salaire"
FROM EMPLOYES E
JOIN PAYER1 P ON E.CODEE = P.CODEE
WHERE E.PRENOME IN ('LOWSALES', 'MINIJOB', 'FACTORYONLY')
ORDER BY E.CODEE;

SELECT
    E.CODEE,
    E.PRENOME,
    TPV.MOIS,
    TPV.ANNEE,
    TPV.NBHEURES_PV AS "Heures PV",
    TU.NBHEURES_U AS "Heures Usine",
    COALESCE(V.QTE_VENDUE, 0) AS "Qté Vendue",
    ROUND(TPV.NBHEURES_PV / NULLIF(V.QTE_VENDUE, 0), 2) AS "Heures/Vente"
FROM EMPLOYES E
JOIN TRAVAILLER_PT_VENTE TPV ON E.CODEE = TPV.CODEE
LEFT JOIN TRAVAILLER_USINE TU ON E.CODEE = TU.CODEE
    AND TPV.MOIS = TU.MOIS
    AND TPV.ANNEE = TU.ANNEE
LEFT JOIN VENDRE V ON E.CODEE = V.CODEE
    AND TPV.MOIS = V.MOIS
    AND TPV.ANNEE = V.ANNEE
WHERE E.PRENOME = 'LOWSALES'
ORDER BY TPV.ANNEE DESC, TPV.MOIS DESC;

SELECT
    E.CODEE,
    E.PRENOME,
    TPV.MOIS,
    TPV.ANNEE,
    TU.NBHEURES_U AS "Heures Usine",
    TPV.NBHEURES_PV AS "Heures PV",
    (TU.NBHEURES_U + TPV.NBHEURES_PV) AS "Total Heures",
    P.FIXEMENSUELE AS "Salaire",
    ROUND(P.FIXEMENSUELE / (TU.NBHEURES_U + TPV.NBHEURES_PV), 2) AS "€/Heure"
FROM EMPLOYES E
JOIN TRAVAILLER_PT_VENTE TPV ON E.CODEE = TPV.CODEE
JOIN TRAVAILLER_USINE TU ON E.CODEE = TU.CODEE
    AND TPV.MOIS = TU.MOIS
    AND TPV.ANNEE = TU.ANNEE
JOIN PAYER1 P ON E.CODEE = P.CODEE AND TPV.ANNEE = P.ANNEE
WHERE E.PRENOME = 'MINIJOB'
ORDER BY TPV.ANNEE DESC, TPV.MOIS DESC;

SELECT
    E.CODEE,
    E.PRENOME,
    V.MOIS,
    V.ANNEE,
    TU.NBHEURES_U AS "Heures Usine",
    TPV.NBHEURES_PV AS "Heures PV",
    V.QTE_VENDUE AS "Qté Vendue",
    ROUND(V.QTE_VENDUE / NULLIF(TPV.NBHEURES_PV, 0), 2) AS "Ventes/Heure PV"
FROM EMPLOYES E
JOIN VENDRE V ON E.CODEE = V.CODEE
LEFT JOIN TRAVAILLER_USINE TU ON E.CODEE = TU.CODEE
    AND V.MOIS = TU.MOIS
    AND V.ANNEE = TU.ANNEE
LEFT JOIN TRAVAILLER_PT_VENTE TPV ON E.CODEE = TPV.CODEE
    AND V.MOIS = TPV.MOIS
    AND V.ANNEE = TPV.ANNEE
WHERE E.PRENOME = 'FACTORYONLY'
ORDER BY V.ANNEE DESC, V.MOIS DESC;

SELECT
    E.PRENOME AS "Type Anomalie",
    COUNT(DISTINCT E.CODEE) AS "Nb Employés",
    ROUND(AVG(P.FIXEMENSUELE), 2) AS "Salaire Moyen",
    SUM(COALESCE(TU.NBHEURES_U, 0) + COALESCE(TPV.NBHEURES_PV, 0)) AS "Total Heures",
    SUM(COALESCE(V.QTE_VENDUE, 0)) AS "Total Ventes"
FROM EMPLOYES E
LEFT JOIN PAYER1 P ON E.CODEE = P.CODEE
LEFT JOIN TRAVAILLER_USINE TU ON E.CODEE = TU.CODEE
LEFT JOIN TRAVAILLER_PT_VENTE TPV ON E.CODEE = TPV.CODEE
LEFT JOIN VENDRE V ON E.CODEE = V.CODEE
WHERE E.PRENOME IN ('LOWSALES', 'MINIJOB', 'FACTORYONLY')
GROUP BY E.PRENOME
ORDER BY E.PRENOME;

