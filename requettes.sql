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
    AND LOWER(pv.TypePV) = 'brico-express'
);

-- Requête de vérification :
-- Afficher pour chaque gamme tous les types de points de vente où ses produits ont été vendus
-- (y compris les gammes jamais vendues dans un Brico-Express)
SELECT DISTINCT
    g.NomG,
    --Permet de remplacer une valeur NULL par une leur par défaut
    NVL(pv.TypePV, 'Aucun point de vente') AS TypePointVente
FROM GAMME g,
     PRODUITS p,
     VENDRE v,
     POINTS_DE_VENTE pv
WHERE p.CodeG(+) = g.CodeG
  AND v.CodeP(+) = p.CodeP
  AND pv.CodePV(+) = v.CodePV
ORDER BY g.NomG, TypePointVente;































--------------------------------------------------------------------------------
-- 2️⃣  Pour chaque supermarché, donner son nom, son adresse complète
--      et éventuellement le nombre de salariés qu’il emploie chaque mois
--------------------------------------------------------------------------------
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



-- Requête de vérification :
-- Afficher, pour chaque point de vente de type "GSB", la liste des employés qui y travaillent avec leur année et mois d’affectation, afin de vérifier la cohérence du nombre de salariés par mois
SELECT DISTINCT
    pv.NomPV,
    pv.RuePV,
    pv.CPostalPV,
    pv.VillePV,
    tpv.Annee,
    tpv.Mois,
    e.NomE,
    e.PrenomE
FROM POINTS_DE_VENTE pv,
     TRAVAILLER_PT_VENTE tpv,
     EMPLOYES e
WHERE LOWER(pv.TypePV) = 'gsb'
  AND pv.CodePV = tpv.CodePV(+)
  AND tpv.CodeE = e.CodeE(+)
ORDER BY pv.NomPV, tpv.Annee, tpv.Mois, e.NomE;
























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

-- Requête de vérification :
-- Voir, pour chaque usine et chacun de ses départements, guelles qualifications sont autorisées et quels employés du département les possèdent (ou pas)
SELECT DISTINCT
    u.NomU,
    d.CodeD,
    d.NomD,
    a.CodeQ AS QualifAutorisee,
    e.CodeE,
    e.NomE,
    e.PrenomE,
    ps.CodeQ AS QualifPossedee
FROM USINES u,
     DEPARTEMENTS d,
     AUTORISER a,
     TRAVAILLER_USINE tu,
     EMPLOYES e,
     POSSEDER ps
WHERE d.CodeU = u.CodeU
  AND a.CodeD = d.CodeD
  -- employés qui travaillent dans le département
  AND tu.CodeD(+) = d.CodeD
  AND e.CodeE(+) = tu.CodeE
  -- qualification réellement possédée par l'employé
  AND ps.CodeE(+) = e.CodeE
  AND ps.CodeQ(+) = a.CodeQ
ORDER BY u.NomU, d.NomD, a.CodeQ, e.NomE;

























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

-- Requête de vérification :
-- Liste le CA du mois en cours pour TOUS les points de vente
SELECT
    pv.CodePV,
    pv.NomPV,
    pv.TypePV,
    SUM(v.Qte_Vendue * f.PrixUnitP) AS CA_Mois_Courant
FROM
    POINTS_DE_VENTE pv,
    VENDRE v,
    FACTURER f
WHERE
    pv.CodePV = v.CodePV
    AND v.CodeP = f.CodeP
    -- même filtre de période que la requête principale
    AND v.Mois  = TO_CHAR(SYSDATE, 'MM')
    AND v.Annee = TO_CHAR(SYSDATE, 'YYYY')
    AND f.Mois  = TO_CHAR(SYSDATE, 'MM')
    AND f.Annee = TO_CHAR(SYSDATE, 'YYYY')
GROUP BY
    pv.CodePV, pv.NomPV, pv.TypePV
ORDER BY
    CA_Mois_Courant DESC, pv.CodePV;

























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
-- Permet de visualiser les codes postaux des points de vente et des usines, pour confirmer que les produits vendus en Haute-Garonne ne sont pas fabriqués dans le même département
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
-- Requête de vérification :
-- Affiche les composantes du salaire par employé / mois / année

SELECT
    e.CodeE,
    e.NomE,
    e.PrenomE,
    m.Annee,
    m.Mois,
    p1.FixeMensuelE,
    p1.IndiceSalE,
    NVL(hu.H_u, 0)   AS Heures_Usine,
    NVL(hpv.H_pv, 0) AS Heures_PV,
    NVL(v.CA_retro, 0) AS CA_Retrocession
FROM EMPLOYES e,
     /* même ensemble (CodeE, Mois, Annee) que dans la requête principale */
     ( SELECT CodeE, Mois, Annee FROM Travailler_Usine
       UNION
       SELECT CodeE, Mois, Annee FROM Travailler_Pt_Vente
       UNION
       SELECT CodeE, Mois, Annee FROM Vendre
     ) m,
     /* paramètres annuels (fixe + indice) */
     Payer1 p1,
     /* heures en usine */
     ( SELECT CodeE, Mois, Annee, SUM(NbHeures_U) AS H_u
       FROM Travailler_Usine
       GROUP BY CodeE, Mois, Annee
     ) hu,
     /* heures en point de vente */
     ( SELECT CodeE, Mois, Annee, SUM(NbHeures_PV) AS H_pv
       FROM Travailler_Pt_Vente
       GROUP BY CodeE, Mois, Annee
     ) hpv,
     /* rétro mensuelle par employé */
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

  -- même filtre que la requête principale : les 2 dernières années
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
SELECT pv.NomPV, pv.TypePV, pv.CODEPV
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


-- Requête de vérification :
-- Voir, pour chaque point de vente et pour chaque produit de la gamme "cuisine", si le produit a été vendu cette année

SELECT
    pv.CodePV,
    pv.NomPV,
    pv.TypePV,
    p.CodeP,
    p.NomP,
    v.Qte_Vendue,
    v.Mois,
    v.Annee
FROM
    POINTS_DE_VENTE pv,
    VENDRE v,
    PRODUITS p,
    GAMME g
WHERE
    -- lier le point de vente à la vente
    pv.CodePV = v.CodePV
    -- lier la vente au produit
    AND v.CodeP = p.CodeP
    -- lier le produit à sa gamme
    AND p.CodeG = g.CodeG
    -- garder uniquement la gamme cuisine
    AND LOWER(g.NomG) = 'cuisine'
    -- garder uniquement l'année courante
    AND v.Annee = EXTRACT(YEAR FROM CURRENT_DATE)
ORDER BY
    pv.NomPV,
    p.CodeP;
--Requête de vérification 2 (vérifier la liste de produits de la gamme cuisine)
SELECT
    p.CodeP,
    p.NomP
FROM
    PRODUITS p,
    GAMME g
WHERE
    p.CodeG = g.CodeG
    AND LOWER(g.NomG) = 'cuisine'
ORDER BY
    p.CodeP;
















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


-- Requête de vérification :
SELECT DISTINCT
    e.NomE,
    e.PrenomE,
    dep.CodeD              AS Dept_Dirige,
    dep.CodeU              AS Usine_Departement,
    TO_CHAR(d.DateDebutDir, 'YYYY') AS Annee_Direction,
    r.Annee                AS Annee_Responsable,
    r.CodeG                AS Gamme_Responsable
FROM
    EMPLOYES e,
    DIRIGER d,
    DEPARTEMENTS dep,
    RESPONSABLE r
WHERE
    -- l'employé dirige un département
    d.CodeE = e.CodeE
    AND dep.CodeD = d.CodeD
    -- le même employé est responsable d'une gamme
    AND r.CodeE = e.CodeE
    -- on ne garde que les cas où l'année de direction = l'année de responsabilité
    AND TO_CHAR(d.DateDebutDir, 'YYYY') = r.Annee
    -- et où l'usine du département fabrique bien un produit de cette gamme cette année-là
    AND EXISTS (
        SELECT *
        FROM FABRIQUER_ASSEMBLER1 fa, PRODUITS p
        WHERE fa.CodeU = dep.CodeU
          AND p.CodeP = fa.CodeP
          AND p.CodeG = r.CodeG
          AND TO_CHAR(fa.DateFab, 'YYYY') = r.Annee
    )
ORDER BY
    e.NomE, e.PrenomE, Annee_Direction, dep.CodeD;



















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

-- Vérification Q10 :
-- quantité fabriquée cette année et non vendue, par usine
SELECT
    u.CodeU,
    u.NomU,
    u.RueU,
    u.CPostalU,
    u.VilleU,
    SUM(f.Qte_Fab) AS NbPdtNonVendus
FROM
    USINES u,
    FABRIQUER_ASSEMBLER1 f
WHERE
    u.CodeU = f.CodeU
    -- fabrication de l'année courante
    AND TO_CHAR(f.DateFab, 'YYYY') = TO_CHAR(SYSDATE, 'YYYY')
    -- seulement les produits non vendus cette année
    AND NOT EXISTS (
        SELECT *
        FROM VENDRE v
        WHERE v.CodeP = f.CodeP
          AND v.Annee = TO_CHAR(SYSDATE, 'YYYY')
    )
GROUP BY
    u.CodeU, u.NomU, u.RueU, u.CPostalU, u.VilleU
ORDER BY
    NbPdtNonVendus DESC;

--------------------------------------------------------------------------------
-- 🆕 Requête en plus // Détection des anomalies sur les prix unitaires des produits (méthode IQR)
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
