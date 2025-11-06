--Question 1 (Lister le nom des gammes de produits n’ayant pas fait l’objet de vente
-- dans des Brico-Express):

SELECT DISTINCT G.NomG
FROM GAMME G, PRODUITS P
WHERE G.CodeG = P.CodeG
AND P.CodeP NOT IN (SELECT V.CodeP
                    FROM VENDRE V, POINTS_DE_VENTE PV
                    WHERE V.CodePV = PV.CodePV
                    AND PV.TypePV = 'Brico-Express'



                        );

SELECT G.NomG
FROM GAMME G
WHERE NOT EXISTS (
  SELECT *
  FROM PRODUITS P, VENDRE V, POINTS_DE_VENTE PV
  WHERE V.CodeP  = P.CodeP
  AND PV.CodePV = V.CodePV
  AND P.CodeG = G.CodeG
  AND PV.TypePV = 'Brico-Express'
);


--Question 2 (Pour chaque supermarché, donner son nom, son adresse complète
--      et éventuellement le nombre de salariés qu’il emploie chaque mois) :

SELECT PV.NOMPV, PV.RUEPV, PV.CPOSTALPV, PV.VILLEPV, COUNT( DISTINCT TPV.CODEE) as NbEmploye
FROM POINTS_DE_VENTE PV, TRAVAILLER_PT_VENTE TPV
WHERE PV.CodePV = TPV.CodePV (+)
AND LOWER(PV.TYPEPV) = 'gsb'
GROUP BY PV.CodePV, PV.NOMPV, PV.RUEPV, PV.CPOSTALPV, PV.VILLEPV, TPV.Mois, TPV.Annee
ORDER BY PV.NomPV, TPV.Annee, TPV.Mois ;

SELECT
  pv.NomPV,
  pv.RuePV,
  pv.CPostalPV,
  pv.VillePV,
  tpv.Mois,
  tpv.Annee,
  COUNT(DISTINCT tpv.CodeE) AS NbEmploye
FROM Points_De_Vente pv, Travailler_Pt_Vente tpv
WHERE pv.CodePV = tpv.CodePV(+)
  AND pv.TypePV = 'GSB'
GROUP BY
  pv.CodePV, pv.NomPV, pv.RuePV, pv.CPostalPV, pv.VillePV,
  tpv.Mois, tpv.Annee
ORDER BY pv.NomPV, tpv.Annee, tpv.Mois;




--Question 3 (Donner le nom et l’adresse des usines qui autorisent des qualifications
--      non possédées par les employés travaillant dans cette usine) :

SELECT DISTINCT U.NomU, U.RueU, U.CPOSTALU, U.VILLEU
FROM USINES U, DEPARTEMENTS D, AUTORISER A
WHERE U.CodeU = D.CodeU
AND D.CodeD = A.CodeD
AND A.CodeQ NOT IN (
    SELECT P.CodeQ
    FROM POSSEDER P, TRAVAILLER_USINE TU, DEPARTEMENTS D2
    WHERE P.CodeE = TU.CodeE
    AND TU.CodeD = D2.CodeD
    AND D2.CodeU = U.CodeU
    );


--Question 4 (Donner le nom et le type du point de vente ayant le chiffre d’affaires
--      le plus élevé pour le mois en cours)

SELECT PV.CodePV, PV.NomPV, PV.TypePV, SUM(V.Qte_Vendue * F.PrixUnitP) as CA
FROM POINTS_DE_VENTE PV, VENDRE V, FACTURER F
WHERE PV.CodePV = V.CodePV
AND V.CodeP = F.CodeP
AND V.Mois = TO_CHAR(sysdate, 'MM')
AND V.Annee = TO_CHAR(sysdate, 'YYYY')
AND F.Mois = TO_CHAR(sysdate, 'MM')
AND F.Annee = TO_CHAR(sysdate, 'YYYY')
GROUP BY PV.CodePV, PV.NomPV, PV.TypePV
HAVING SUM(V.Qte_Vendue * F.PrixUnitP) = (
    SELECT MAX(tab.CA) as CAMax
    FROM (SELECT SUM(V2.Qte_Vendue * F2.PrixUnitP) as CA
          FROM POINTS_DE_VENTE PV2, VENDRE V2, FACTURER F2
          WHERE PV2.CodePV = V2.CodePV
          AND V2.CodeP = F2.CodeP
          AND V2.Mois =  TO_CHAR(sysdate, 'MM')
          AND V2.Annee = TO_CHAR(sysdate, 'YYYY')
          AND F2.Mois =  TO_CHAR(sysdate, 'MM')
          AND F2.Annee = TO_CHAR(sysdate, 'YYYY')
          GROUP BY PV2.CodePV, PV2.NomPV, PV2.TypePV) tab
    ) ;

--Question 5 () :

SELECT DISTINCT P.CodeP, P.NomP, V.Annee, V.Mois
FROM PRODUITS P, FACTURER F, VENDRE V, POINTS_DE_VENTE PV
WHERE P.CodeP = V.CodeP
AND P.CodeP = F.CodeP
AND PV.CPostalPV  LIKE '31%'
AND P.CodeP NOT IN (
    SELECT FAB.CodeP
    FROM FABRIQUER_ASSEMBLER1 FAB, USINES U
    WHERE FAB.CodeU = U.CodeU
    AND U.CPostalU  LIKE '31%'
    );
SELECT DISTINCT P.CodeP, P.NomP, V.Annee, V.Mois, FAB.CodeU
FROM PRODUITS P, FACTURER F, VENDRE V, POINTS_DE_VENTE PV, FABRIQUER_ASSEMBLER1 FAB, USINES U
WHERE P.CodeP = V.CodeP
AND P.CodeP = F.CodeP
AND FAB.CodeU = U.CodeU
AND PV.CPostalPV  LIKE '31%';




--Question 6 :

SELECT e.NomE, e.PrenomE, m.Annee, m.Mois, p1.FixeMensuelE + p1.IndiceSalE * NVL(hu.H_u, 0) + p1.IndiceSalE * NVL(hpv.H_pv, 0) + NVL(v.CA_retro, 0)  AS SalaireMensuelEmploye
FROM Employes e,
     /* Ensemble des (CodeE, Mois, Annee) à considérer (heures ou ventes) */
     ( SELECT CodeE, Mois, Annee FROM Travailler_Usine
       UNION
       SELECT CodeE, Mois, Annee FROM Travailler_Pt_Vente
       UNION
       SELECT CodeE, Mois, Annee FROM Vendre
     ) m,
     /* Paramètres annuels: fixe + indice salarial */
     Payer1 p1,
     /* Heures mensuelles en usine */
     ( SELECT CodeE, Mois, Annee, SUM(NbHeures_U) AS H_u
       FROM Travailler_Usine
       GROUP BY CodeE, Mois, Annee
     ) hu,
     /* Heures mensuelles en point de vente */
     ( SELECT CodeE, Mois, Annee, SUM(NbHeures_PV) AS H_pv
       FROM Travailler_Pt_Vente
       GROUP BY CodeE, Mois, Annee
     ) hpv,
     /* Rétro mensuelle */
     ( SELECT v.CodeE, v.Mois, v.Annee,
              SUM(p2.IndiceRetrocessionG * v.Qte_Vendue * f.PrixUnitP) AS CA_retro
       FROM Vendre v, Facturer f, Produits p, Payer2 p2
       WHERE f.CodeP = v.CodeP
         AND f.Mois  = v.Mois
         AND f.Annee = v.Annee
         AND p.CodeP = v.CodeP
         AND p2.CodeG = p.CodeG
         AND p2.Annee = v.Annee
       GROUP BY v.CodeE, v.Mois, v.Annee
     ) v
WHERE m.CodeE = e.CodeE
  AND p1.CodeE = e.CodeE
  AND p1.Annee = m.Annee

  AND hu.CodeE(+) = m.CodeE
  AND hu.Mois(+)  = m.Mois
  AND hu.Annee(+) = m.Annee

  AND hpv.CodeE(+) = m.CodeE
  AND hpv.Mois(+)  = m.Mois
  AND hpv.Annee(+) = m.Annee

  AND v.CodeE(+) = m.CodeE
  AND v.Mois(+)  = m.Mois
  AND v.Annee(+) = m.Annee

  AND m.Annee IN (EXTRACT(YEAR FROM SYSDATE), EXTRACT(YEAR FROM SYSDATE)-1)
ORDER BY m.Annee, e.NomE, e.PrenomE, m.Mois;


SELECT E.NomE, E.PrenomE, P1.FixeMensuelE + P1.IndiceSalE * (TravU.NbHeureU + TravPV.NbHeurePV) + IndiceVente.Ind
FROM EMPLOYES E, PAYER1 P1, (
    SELECT TU.NbHeures_U as NbHeureU
    FROM TRAVAILLER_USINE TU
    WHERE E.CodeE = TU.CodeE
) TravU, (
    SELECT TPV.NbHeures_PV as NbHeurePV
    FROM TRAVAILLER_PT_VENTE TPV
    WHERE E.CodeE = TPV.CodeE
) TravPV, (
    SELECT (P2.IndiceRetrocessionG * V.Qte_Vendue * F.PrixUnitP) as Ind
    FROM PAYER2 P2, VENDRE V, FACTURER F
    WHERE P2.Annee = P1.Annee
    AND V.CodeE = E.CodeE
    AND V.CodeP = F.CodeP
    AND V.Mois  = F.Mois
    AND V.Annee = F.Annee
) IndiceVente
WHERE P1.CodeE = E.CodeE ;



--Question 7 :








-- Question 8 :

SELECT PV.NomPV, PV.TypePV
FROM POINTS_DE_VENTE PV
WHERE NOT EXISTS (
    SELECT *
    FROM GAMME G
    WHERE G.NomG = 'Cuisine'
    AND NOT EXISTS (
        SELECT *
        FROM VENDRE V, PRODUITS P
        WHERE P.CodeP = V.CodeP
        AND V.CodePV = PV.CodePV
        AND P.CodeG = G.CodeG
        AND V.Annee = TO_CHAR(sysdate, 'YYYY')
    )
);


--Question 9 :

SELECT DISTINCT E.NomE, E.PrenomE
FROM EMPLOYES E, DIRIGER Di
WHERE E.CodeE = Di.CodeE
AND Di.CodeE IN (
    SELECT R.CodeE
    FROM RESPONSABLE R, PRODUITS P, FABRIQUER_ASSEMBLER1 F, DEPARTEMENTS Dep
    WHERE R.CodeG = P.CodeG
    AND P.CodeP = F.CodeP
    AND F.CodeU = Dep.CodeU
    AND Dep.CodeD = Di.CodeD
    AND R.Annee = TO_CHAR(Di.DateDebutDir, 'YYYY')
);



--Question 10 :

SELECT U.NomU, U.RueU, U.CPostalU, U.VilleU
FROM USINES U, FABRIQUER_ASSEMBLER1 F
WHERE U.CodeU = F.CodeU
  -- fabrication de l'année courante
AND TO_CHAR(F.DateFab, 'YYYY') = TO_CHAR(sysdate, 'YYYY')
  -- seulement les produits non vendus cette année
AND NOT EXISTS (
        SELECT *
        FROM VENDRE V
        WHERE V.CodeP = F.CodeP
          AND V.Annee = TO_CHAR(sysdate, 'YYYY')
      )
GROUP BY U.CodeU, U.NomU, U.RueU, U.CPostalU, U.VilleU
HAVING SUM(F.Qte_Fab) = (
    SELECT MAX(tab.NbPdtV)
    FROM (
        SELECT SUM(F2.Qte_Fab) as NbPdtV
        FROM FABRIQUER_ASSEMBLER1 F2
        WHERE TO_CHAR(F2.DateFab, 'YYYY') = TO_CHAR(sysdate, 'YYYY')
        AND NOT EXISTS (
            SELECT *
            FROM VENDRE V2
            WHERE V2.CodeP = F2.CodeP
            AND V2.Annee = TO_CHAR(sysdate, 'YYYY')

        )
        GROUP BY F2.CodeU
    ) tab
);






