--------------------------------------------------------------------------------
-- 1️⃣  Lister le nom des gammes de produits n’ayant pas fait l’objet de vente
--     dans des Brico-Express
--------------------------------------------------------------------------------
-- Sélectionner le nom des gammes de produits
SELECT DISTINCT g.NomG
FROM GAMME g
-- Pour lesquelles il n’existe aucune vente effectuée dans un point de vente de type "Brico-Express"
WHERE NOT EXISTS (
  SELECT *
  FROM PRODUITS p, VENDRE v, POINTS_DE_VENTE pv
  WHERE p.CodeG = g.CodeG
    AND v.CodeP = p.CodeP
    AND pv.CodePV = v.CodePV
    AND pv.TypePV = 'Brico-Express'
);

--------------------------------------------------------------------------------
-- 2️⃣  Pour chaque supermarché, donner son nom, son adresse complète
--      et éventuellement le nombre de salariés qu’il emploie chaque mois
--------------------------------------------------------------------------------

-- Sélectionner le nom, l’adresse et les informations temporelles des points de vente
SELECT
    pv.NomPV,
    pv.RuePV,
    pv.CPostalPV,
    pv.VillePV,
    tpv.Annee,
    tpv.Mois,
    COUNT(DISTINCT tpv.CodeE) AS NbSalaries
FROM
    POINTS_DE_VENTE pv,
    TRAVAILLER_PT_VENTE tpv
-- Lister uniquement les points de vente de type "GSB"
-- et inclure ceux qui n’ont pas d’employés grâce à la jointure externe (+)
WHERE
    LOWER(pv.TypePV) = 'gsb'
    AND pv.CodePV = tpv.CodePV(+)
-- Regrouper par point de vente et par période (année, mois)
GROUP BY
    pv.NomPV, pv.RuePV, pv.CPostalPV, pv.VillePV, tpv.Annee, tpv.Mois
-- Trier les résultats par nom de point de vente, puis par année et mois
ORDER BY
    pv.NomPV, tpv.Annee, tpv.Mois;
--------------------------------------------------------------------------------
-- 3️⃣  Donner le nom et l’adresse des usines qui autorisent des qualifications
--      non possédées par les employés travaillant dans cette usine
--------------------------------------------------------------------------------
-- Sélectionner le nom et l’adresse des usines
SELECT DISTINCT u.NomU, u.RueU, u.CPostalU, u.VilleU
FROM USINES u
-- Garder uniquement les usines pour lesquelles il existe au moins un département
-- autorisant une qualification non possédée par les employés y travaillant
WHERE EXISTS (
  SELECT *
  FROM DEPARTEMENTS d, AUTORISER a
  WHERE a.CodeD = d.CodeD
    AND d.CodeU = u.CodeU
    AND NOT EXISTS (
      SELECT *
      FROM TRAVAILLER_USINE tu, POSSEDER ps
      WHERE ps.CodeE = tu.CodeE
        AND tu.CodeD = d.CodeD
        AND ps.CodeQ = a.CodeQ
    )
);

--------------------------------------------------------------------------------
-- 4️⃣  Donner le nom et le type du point de vente ayant le chiffre d’affaires
--      le plus élevé pour le mois en cours
--------------------------------------------------------------------------------
-- Sélectionner le code, le nom et le type des points de vente
-- ainsi que leur chiffre d'affaires (CA) pour le mois et l’année en cours
SELECT PV.CodePV, PV.NomPV, PV.TypePV, SUM(V.Qte_Vendue * F.PrixUnitP) as CA
FROM POINTS_DE_VENTE PV, VENDRE V, FACTURER F
-- Relier les points de vente aux ventes et aux factures correspondantes
WHERE PV.CodePV = V.CodePV
AND V.CodeP = F.CodeP
-- Filtrer uniquement les ventes et factures du mois et de l’année actuels
AND V.Mois = TO_CHAR(sysdate, 'MM')
AND V.Annee = TO_CHAR(sysdate, 'YYYY')
AND F.Mois = TO_CHAR(sysdate, 'MM')
AND F.Annee = TO_CHAR(sysdate, 'YYYY')
-- Regrouper les données par point de vente
GROUP BY PV.CodePV, PV.NomPV, PV.TypePV
-- Garder uniquement le ou les points de vente ayant le chiffre d'affaires maximal
HAVING SUM(V.Qte_Vendue * F.PrixUnitP) = (
    SELECT MAX(tab.CA) as CAMax
    FROM (
        -- Sous-requête : calcul du chiffre d’affaires de chaque point de vente
        SELECT SUM(V2.Qte_Vendue * F2.PrixUnitP) as CA
        FROM POINTS_DE_VENTE PV2, VENDRE V2, FACTURER F2
        WHERE PV2.CodePV = V2.CodePV
        AND V2.CodeP = F2.CodeP
        AND V2.Mois =  TO_CHAR(sysdate, 'MM')
        AND V2.Annee = TO_CHAR(sysdate, 'YYYY')
        AND F2.Mois =  TO_CHAR(sysdate, 'MM')
        AND F2.Annee = TO_CHAR(sysdate, 'YYYY')
        GROUP BY PV2.CodePV, PV2.NomPV, PV2.TypePV
    ) tab
);



--------------------------------------------------------------------------------
-- 5️⃣  Produits vendus en Haute-Garonne mais non fabriqués dans ce département
--------------------------------------------------------------------------------
-- Sélectionner le code et le nom des produits
SELECT DISTINCT
    p.CodeP,
    p.NomP
FROM PRODUITS p, GAMME g, VENDRE v, POINTS_DE_VENTE pv
-- Relier chaque produit à sa gamme, sa vente et son point de vente
WHERE p.CodeG = g.CodeG
  AND v.CodeP = p.CodeP
  AND pv.CodePV = v.CodePV
-- Ne garder que les ventes effectuées dans le département de la Haute-Garonne (31)
  AND pv.CPostalPV LIKE '31%'
-- Exclure les produits fabriqués ou assemblés dans une usine située en Haute-Garonne
  AND NOT EXISTS (
        SELECT *
        FROM FABRIQUER_ASSEMBLER1 fa, USINES u
        WHERE fa.CodeP = p.CodeP
          AND fa.CodeU = u.CodeU
          AND u.CPostalU LIKE '31%'
  )
-- Trier les résultats par code produit
ORDER BY p.CodeP;



-- Requête de vérification :
-- Permet de visualiser les codes postaux des points de vente et des usines
-- pour confirmer que les produits vendus en Haute-Garonne ne sont pas fabriqués dans le même département
SELECT DISTINCT
    p.CodeP,
    p.NomP,
    pv.CPostalPV AS CP_Vente,
    u.CPostalU   AS CP_Usine
FROM PRODUITS p, GAMME g, VENDRE v, POINTS_DE_VENTE pv, FABRIQUER_ASSEMBLER1 fa, USINES u
-- Liaisons entre produits, gammes, ventes, usines et fabrications
WHERE p.CodeG = g.CodeG
  AND v.CodeP = p.CodeP
  AND pv.CodePV = v.CodePV
  AND fa.CodeP = p.CodeP
  AND u.CodeU = fa.CodeU
-- Filtrer les ventes dans le département 31
  AND pv.CPostalPV LIKE '31%'
-- Exclure les produits fabriqués dans une usine du même département
  AND NOT EXISTS (
        SELECT *
        FROM FABRIQUER_ASSEMBLER1 fa2, USINES u2
        WHERE fa2.CodeP = p.CodeP
          AND fa2.CodeU = u2.CodeU
          AND u2.CPostalU LIKE '31%'
  )
-- Trier par code produit et codes postaux pour faciliter la vérification
ORDER BY p.CodeP, pv.CPostalPV, u.CPostalU;



--------------------------------------------------------------------------------
-- 6️⃣  Pour les deux dernières années, salaires mensuels des employés
--------------------------------------------------------------------------------
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







--------------------------------------------------------------------------------
-- 7️⃣  Usine, type, ville et département homonyme d’un autre département
--------------------------------------------------------------------------------
-- Sélectionner le nom, le type, la ville et le département des usines
SELECT DISTINCT
    u.NomU,
    tu.NomTU,
    u.VilleU,
    d1.NomD
FROM
    USINES u, AVOIR_TYPE atp, TYPEU tu, DEPARTEMENTS d1, DEPARTEMENTS d2
-- Relier chaque usine à son type et à ses départements
WHERE
    atp.CodeU = u.CodeU
    AND tu.CodeTU = atp.CodeTU
    AND d1.CodeU = u.CodeU
-- Rechercher des départements (d1, d2) ayant le même nom mais appartenant à des usines différentes
    AND d2.NomD = d1.NomD
    AND d2.CodeD <> d1.CodeD
    AND d2.CodeU <> d1.CodeU;



--------------------------------------------------------------------------------
-- 8️⃣  Point de vente ayant vendu cette année tous les produits de la gamme Cuisine
--------------------------------------------------------------------------------
-- Sélectionner le nom et le type des points de vente
SELECT pv.NomPV, pv.TypePV
FROM POINTS_DE_VENTE pv
-- Garder uniquement les points de vente
-- pour lesquels il n’existe aucun produit de la gamme "cuisine"
-- non vendu durant l’année en cours
WHERE NOT EXISTS (
  SELECT *
  FROM PRODUITS p, GAMME g
  WHERE g.CodeG = p.CodeG
    AND LOWER(g.NomG) = 'cuisine'
    AND NOT EXISTS (
      SELECT *
      FROM VENDRE v
      WHERE v.CodePV = pv.CodePV
        AND v.CodeP  = p.CodeP
        AND v.Annee  = EXTRACT(YEAR FROM CURRENT_DATE)
    )
);



--------------------------------------------------------------------------------
-- 9️⃣  Employés à la fois directeurs d’un département et responsables de gamme
--      la même année (usine associée au département)
--------------------------------------------------------------------------------
-- Sélectionner le nom et le prénom des employés
SELECT DISTINCT
    e.NomE,
    e.PrenomE
FROM
    EMPLOYES e, DIRIGER d, DEPARTEMENTS dep
-- Relier chaque employé au département qu’il dirige
WHERE
    d.CodeE = e.CodeE
    AND dep.CodeD = d.CodeD
-- Garder uniquement les employés qui, la même année,
-- dirigent un département dont l’usine fabrique un produit
-- appartenant à une gamme dont ils sont responsables
    AND EXISTS (
        SELECT *
        FROM RESPONSABLE r, FABRIQUER_ASSEMBLER1 fa, PRODUITS p
        WHERE
            fa.CodeU = dep.CodeU
            AND p.CodeP = fa.CodeP
            AND r.CodeE = e.CodeE
            AND p.CodeG = r.CodeG
            AND TO_CHAR(d.DateDebutDir, 'YYYY') = r.Annee
            AND TO_CHAR(fa.DateFab, 'YYYY') = r.Annee
    );








--------------------------------------------------------------------------------
-- 🔟  Usine ayant fabriqué le plus de produits non encore vendus cette année
--------------------------------------------------------------------------------

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








--------------------------------------------------------------------------------
-- Requête en plus // Détection des anomalies sur les prix unitaires des produits (méthode IQR)
--------------------------------------------------------------------------------

WITH stats AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY PrixUnitP) AS q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY PrixUnitP) AS q3,
        (PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY PrixUnitP)
        - PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY PrixUnitP)) AS iqr
    FROM FACTURER
)
SELECT
    f.CodeP,
    f.Mois,
    f.Annee,
    f.PrixUnitP
FROM FACTURER f, stats s
WHERE f.PrixUnitP < (s.q1 - 1.5 * s.iqr)
   OR f.PrixUnitP > (s.q3 + 1.5 * s.iqr)
ORDER BY f.PrixUnitP DESC;


--------------------------------------------------------------------------------
-- Requête en plus de véfification : Nombre de tables, nombre de colonnes et nombre de lignes par table
--------------------------------------------------------------------------------
SELECT
    t.table_name         AS NomTable,
    (SELECT COUNT(*)
       FROM user_tab_columns c
      WHERE c.table_name = t.table_name)        AS NbColonnes,
    NVL(t.num_rows, 0)   AS NbLignes
FROM user_tables t
ORDER BY t.table_name;

--------------------------------------------------------------------------------
-- Moyenne mensuelle des salaires par année
--------------------------------------------------------------------------------
SELECT
    t.ANNEE,
    t.MOIS,
    ROUND(AVG(p1.FIXEMENSUELE * p1.INDICESALE), 2) AS Moyenne_Salaire_Mensuel
FROM
    PAYER1 p1,
    TRAVAILLER_USINE t
WHERE
    p1.CODEE = t.CODEE
GROUP BY
    t.ANNEE, t.MOIS
ORDER BY
    t.ANNEE, t.MOIS;


