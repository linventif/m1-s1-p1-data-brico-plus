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
SELECT
    emp.CodeE,
    emp.NomE,
    emp.PrenomE,
    per.Annee,
    per.Mois,
    pay.FixeMensuelE
      + pay.IndiceSalE * NVL(heu_usine.Heures_Usine, 0)
      + pay.IndiceSalE * NVL(heu_pv.Heures_PV, 0)
      + NVL(retro.CA_Retro, 0) AS SalaireMensuelEmploye
FROM EMPLOYES emp,
     -- ensemble des (employé, mois, année) où il a travaillé ou vendu
     ( SELECT CodeE, Mois, Annee FROM TRAVAILLER_USINE
       UNION
       SELECT CodeE, Mois, Annee FROM TRAVAILLER_PT_VENTE
       UNION
       SELECT CodeE, Mois, Annee FROM VENDRE
     ) per,
     -- paramètres de paie annuels (fixe + indice)
     PAYER1 pay,
     -- heures travaillées en usine dans le mois
     ( SELECT CodeE, Mois, Annee, SUM(NbHeures_U) AS Heures_Usine
       FROM TRAVAILLER_USINE
       GROUP BY CodeE, Mois, Annee
     ) heu_usine,
     -- heures travaillées en point de vente dans le mois
     ( SELECT CodeE, Mois, Annee, SUM(NbHeures_PV) AS Heures_PV
       FROM TRAVAILLER_PT_VENTE
       GROUP BY CodeE, Mois, Annee
     ) heu_pv,
     -- partie objectifs / rétrocession sur les ventes du mois
     ( SELECT v.CodeE,
              v.Mois,
              v.Annee,
              SUM(p2.IndiceRetrocessionG * v.Qte_Vendue * f.PrixUnitP) AS CA_Retro
       FROM VENDRE v, FACTURER f, PRODUITS p, PAYER2 p2
       WHERE f.CodeP = v.CodeP
         AND f.Mois  = v.Mois
         AND f.Annee = v.Annee
         AND p.CodeP = v.CodeP
         AND p2.CodeG = p.CodeG
         AND p2.Annee = v.Annee
       GROUP BY v.CodeE, v.Mois, v.Annee
     ) retro
WHERE per.CodeE = emp.CodeE
  AND pay.CodeE = emp.CodeE
  AND pay.Annee = per.Annee

  AND heu_usine.CodeE(+) = per.CodeE
  AND heu_usine.Mois(+)  = per.Mois
  AND heu_usine.Annee(+) = per.Annee

  AND heu_pv.CodeE(+) = per.CodeE
  AND heu_pv.Mois(+)  = per.Mois
  AND heu_pv.Annee(+) = per.Annee

  AND retro.CodeE(+) = per.CodeE
  AND retro.Mois(+)  = per.Mois
  AND retro.Annee(+) = per.Annee

  AND per.Annee IN (EXTRACT(YEAR FROM SYSDATE), EXTRACT(YEAR FROM SYSDATE)-1)
ORDER BY per.Annee, emp.NomE, emp.PrenomE, per.Mois;
-- Requête de vérification :
-- Affiche les composantes du salaire par employé / mois / année

SELECT
    e.CodeE,
    e.NomE,
    e.PrenomE,
    m.Annee,
    m.Mois,

    /* 1. partie fixe */
    p1.FixeMensuelE                                 AS Partie_Fixe,

    /* 2. partie travail (usine + point de vente) */
    (p1.IndiceSalE * NVL(hu.H_u, 0))                AS Partie_Travail_Usine,
    (p1.IndiceSalE * NVL(hpv.H_pv, 0))              AS Partie_Travail_PV,

    /* 3. partie objectifs / rétrocession */
    NVL(v.CA_retro, 0)                              AS Partie_Objectifs,

    /* salaire total = somme des 3 blocs */
    p1.FixeMensuelE
      + (p1.IndiceSalE * NVL(hu.H_u, 0))
      + (p1.IndiceSalE * NVL(hpv.H_pv, 0))
      + NVL(v.CA_retro, 0)                          AS Salaire_Mensuel_Employe

FROM EMPLOYES e,
     /* même ensemble (CodeE, Mois, Annee) que dans la requête principale */
     ( SELECT CodeE, Mois, Annee FROM Travailler_Usine
       UNION
       SELECT CodeE, Mois, Annee FROM Travailler_Pt_Vente
       UNION
       SELECT CodeE, Mois, Annee FROM Vendre
     ) m,
     /* paramètres annuels (fixe + indice) */
     PAYER1 p1,
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

  -- même filtre que ta requête principale
  AND m.Annee IN (EXTRACT(YEAR FROM SYSDATE), EXTRACT(YEAR FROM SYSDATE)-1)

ORDER BY
    m.Annee,
    e.NomE,
    e.PrenomE,
    m.Mois;


















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
SELECT pv.NomPV, pv.TypePV, pv.CODEPV
--Liste des points de ventes, pour lesquelles il n'existe pas de produits qui n'ont pas été vendus de la gamme cuisine
FROM POINTS_DE_VENTE pv
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
-- Requête en plus 1 // Détection des anomalies sur les salaires (méthode IQR)
--------------------------------------------------------------------------------
WITH salaires AS (
    SELECT t.CODEE, t.ANNEE, t.MOIS,
        (p1.FIXEMENSUELE * p1.INDICESALE) AS salaire_mensuel
    FROM
        PAYER1 p1, TRAVAILLER_USINE t
    WHERE
        p1.CODEE = t.CODEE
        AND p1.ANNEE = t.ANNEE
),
stats AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY salaire_mensuel) AS q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY salaire_mensuel) AS q3,
        ( PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY salaire_mensuel)
        - PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY salaire_mensuel) ) AS iqr
    FROM salaires
)
SELECT
    sals.CODEE,
    sals.ANNEE,
    sals.MOIS,
    sals.salaire_mensuel
FROM
    salaires sals,
    stats st
WHERE
    sals.salaire_mensuel < (st.q1 - 1.5 * st.iqr)
    OR sals.salaire_mensuel > (st.q3 + 1.5 * st.iqr)
ORDER BY
    sals.salaire_mensuel DESC;


--------------------------------------------------------------------------------
-- Requête en plus 2 // Statistiques descriptives sur les salaires et fenêtrage par employé (Agrégation avancée)
--------------------------------------------------------------------------------
WITH m AS (
    /* tous les (employé, mois, année) où il s'est passé quelque chose */
    SELECT CODEE, MOIS, ANNEE FROM TRAVAILLER_USINE
    UNION
    SELECT CODEE, MOIS, ANNEE FROM TRAVAILLER_PT_VENTE
    UNION
    SELECT CODEE, MOIS, ANNEE FROM VENDRE
),
/* heures totales en usine par employé / mois / année */
hu AS (
    SELECT CODEE, MOIS, ANNEE, SUM(NBHEURES_U) AS Heures_Usine
    FROM TRAVAILLER_USINE
    GROUP BY CODEE, MOIS, ANNEE
),
/* heures totales en point de vente par employé / mois / année */
hpv AS (
    SELECT CODEE, MOIS, ANNEE, SUM(NBHEURES_PV) AS Heure_PointVente
    FROM TRAVAILLER_PT_VENTE
    GROUP BY CODEE, MOIS, ANNEE
),
/* partie objectif (rétro) par employé / mois / année */
v AS (
    SELECT
        ve.CODEE,
        ve.MOIS,
        ve.ANNEE,
        SUM(p2.INDICERETROCESSIONG * ve.QTE_VENDUE * f.PRIXUNITP) AS CA_RETRO
    FROM VENDRE ve, FACTURER f, PRODUITS p, PAYER2 p2
    WHERE f.CODEP = ve.CODEP
      AND f.MOIS  = ve.MOIS
      AND f.ANNEE = ve.ANNEE
      AND p.CODEP = ve.CODEP
      AND p2.CODEG = p.CODEG
      AND p2.ANNEE = ve.ANNEE
    GROUP BY ve.CODEE, ve.MOIS, ve.ANNEE
),
/* salaire unique par employé / mois / année */
salaires AS (
    SELECT
        m.ANNEE,
        m.MOIS,
        m.CODEE,
        -- décomposition
        p1.FIXEMENSUELE                                      AS PARTIE_FIXE,
        (p1.INDICESALE * NVL(hu.Heures_Usine, 0))                     AS PARTIE_TRAVAIL_USINE,
        (p1.INDICESALE * NVL(hpv.Heure_PointVente, 0))                   AS PARTIE_TRAVAIL_PV,
        NVL(v.CA_RETRO, 0)                                   AS PARTIE_OBJECTIFS,
        -- salaire total du mois
        p1.FIXEMENSUELE
          + (p1.INDICESALE * NVL(hu.Heures_Usine, 0))
          + (p1.INDICESALE * NVL(hpv.Heure_PointVente, 0))
          + NVL(v.CA_RETRO, 0)                               AS SALAIRE_MENSUEL
    FROM
        m,
        PAYER1 p1,
        hu,
        hpv,
        v
    WHERE
        p1.CODEE = m.CODEE
        AND p1.ANNEE = m.ANNEE
        AND hu.CODEE(+) = m.CODEE
        AND hu.MOIS(+)  = m.MOIS
        AND hu.ANNEE(+) = m.ANNEE
        AND hpv.CODEE(+) = m.CODEE
        AND hpv.MOIS(+)  = m.MOIS
        AND hpv.ANNEE(+) = m.ANNEE
        AND v.CODEE(+) = m.CODEE
        AND v.MOIS(+)  = m.MOIS
        AND v.ANNEE(+) = m.ANNEE
)
SELECT
    s.ANNEE,
    s.MOIS,
    s.CODEE,
    s.SALAIRE_MENSUEL,

    -- statistiques du mois, cette fois sur le salaire unique
    MIN(s.SALAIRE_MENSUEL)
        OVER (PARTITION BY s.ANNEE, s.MOIS) AS MIN_SALAIRE_MOIS,

    MAX(s.SALAIRE_MENSUEL)
        OVER (PARTITION BY s.ANNEE, s.MOIS) AS MAX_SALAIRE_MOIS,

    ROUND(
        AVG(s.SALAIRE_MENSUEL)
        OVER (PARTITION BY s.ANNEE, s.MOIS),
        2
    ) AS MOYENNE_SALAIRE_MOIS,

    ROUND(
        STDDEV(s.SALAIRE_MENSUEL)
        OVER (PARTITION BY s.ANNEE, s.MOIS),
        2
    ) AS ECART_TYPE_SALAIRE_MOIS,

    ROUND(
        VARIANCE(s.SALAIRE_MENSUEL)
        OVER (PARTITION BY s.ANNEE, s.MOIS),
        2
    ) AS VARIANCE_SALAIRE_MOIS
FROM salaires s
ORDER BY s.ANNEE, s.MOIS, s.CODEE;


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


------------------------------------------------------
--Requête d'extraction de données pour analyse salaire
------------------------------------------------------

WITH m AS (
    /* tous les (employé, mois, année) où il s'est passé quelque chose */
    SELECT CODEE, MOIS, ANNEE FROM TRAVAILLER_USINE
    UNION
    SELECT CODEE, MOIS, ANNEE FROM TRAVAILLER_PT_VENTE
    UNION
    SELECT CODEE, MOIS, ANNEE FROM VENDRE
),
/* heures totales en usine */
hu AS (
    SELECT CODEE, MOIS, ANNEE, SUM(NBHEURES_U) AS H_U
    FROM TRAVAILLER_USINE
    GROUP BY CODEE, MOIS, ANNEE
),
/* heures totales en point de vente */
hpv AS (
    SELECT CODEE, MOIS, ANNEE, SUM(NBHEURES_PV) AS H_PV
    FROM TRAVAILLER_PT_VENTE
    GROUP BY CODEE, MOIS, ANNEE
),
/* partie objectifs = rétro sur les ventes du mois */
v AS (
    SELECT
        ve.CODEE,
        ve.MOIS,
        ve.ANNEE,
        SUM(p2.INDICERETROCESSIONG * ve.QTE_VENDUE * f.PRIXUNITP) AS CA_retro
    FROM VENDRE ve, FACTURER f, PRODUITS p, PAYER2 p2
    WHERE f.CODEP = ve.CODEP
      AND f.MOIS  = ve.MOIS
      AND f.ANNEE = ve.ANNEE
      AND p.CODEP = ve.CODEP
      AND p2.CODEG = p.CODEG
      AND p2.ANNEE = ve.ANNEE
    GROUP BY ve.CODEE, ve.MOIS, ve.ANNEE
),
/* quantité vendue dans le mois par employé */
ventes_mois AS (
    SELECT
        v.CODEE,
        v.MOIS,
        v.ANNEE,
        SUM(v.QTE_VENDUE) AS QTE_VENDUE_MOIS
    FROM VENDRE v
    GROUP BY v.CODEE, v.MOIS, v.ANNEE
),
/* quantité fabriquée dans le mois, rattachée à l'employé via l'usine où il a travaillé */
fab_mois AS (
    SELECT
        tu.CODEE,
        EXTRACT(MONTH FROM fa.DATEFAB) AS MOIS,
        EXTRACT(YEAR  FROM fa.DATEFAB) AS ANNEE,
        SUM(fa.QTE_FAB) AS QTE_FAB_MOIS
    FROM TRAVAILLER_USINE tu,
         DEPARTEMENTS d,
         FABRIQUER_ASSEMBLER1 fa
    WHERE d.CODED = tu.CODED
      AND fa.CODEU = d.CODEU
      -- même mois / même année que le travail de l'employé
      AND EXTRACT(MONTH FROM fa.DATEFAB) = tu.MOIS
      AND EXTRACT(YEAR  FROM fa.DATEFAB) = tu.ANNEE
    GROUP BY
        tu.CODEE,
        EXTRACT(MONTH FROM fa.DATEFAB),
        EXTRACT(YEAR  FROM fa.DATEFAB)
)
SELECT
    /* temps + employé */
    m.ANNEE,
    m.MOIS,
    e.CODEE,
    e.NOME,
    e.PRENOME,
<<<<<<< HEAD
    /* adresses utiles pour analyse (perso / pro) */
=======

    /* adresses perso */
>>>>>>> a5e2ecb (Requêtes SQL)
    e.CPOSTALPERSE,
    e.VILLEPERSE,

    /* adresses pro complètes */
    e.RUEPROE,
    e.CPOSTALPROE,
    e.VILLEPROE,
    /* qualifications (via POSSEDER) */
    q.CODEQ,
    q.NOMQ,
    q.TAUXMINQ,
    /* direction de département (facultatif) */
    dpt.CODED       AS CODE_DEPT_DIRIGE,
    dpt.NOMD        AS NOM_DEPT_DIRIGE,
    dir.DATEDEBUTDIR,

    /* responsabilité de gamme (facultatif) */
    r.CODEG         AS CODE_GAMME_RESP,
    g.NOMG          AS NOM_GAMME_RESP,

    /* quantités du mois */
    NVL(ventes_mois.QTE_VENDUE_MOIS, 0) AS QTE_VENDUE_MOIS,
    NVL(fab_mois.QTE_FAB_MOIS, 0)       AS QTE_FABRIQUEE_MOIS,

    /* heures du mois (ce que tu voulais rajouter) */
    NVL(hu.H_U, 0)  AS HEURES_USINE_MOIS,
    NVL(hpv.H_PV, 0) AS HEURES_PV_MOIS,

    /* --- décomposition du salaire (à la fin) --- */
    p1.FIXEMENSUELE                                      AS PARTIE_FIXE,
    (p1.INDICESALE * NVL(hu.H_U, 0))                     AS PARTIE_TRAVAIL_USINE,
    (p1.INDICESALE * NVL(hpv.H_PV, 0))                   AS PARTIE_TRAVAIL_PV,
    NVL(v.CA_retro, 0)                                   AS PARTIE_OBJECTIFS,
    p1.FIXEMENSUELE
      + (p1.INDICESALE * NVL(hu.H_U, 0))
      + (p1.INDICESALE * NVL(hpv.H_PV, 0))
      + NVL(v.CA_retro, 0)                               AS SALAIRE_MENSUEL_EMPLOYE

FROM
    m,
    EMPLOYES e,
    PAYER1 p1,
    POSSEDER pos,
    QUALIFICATIONS q,
    hu,
    hpv,
    v,
    ventes_mois,
    fab_mois,
    DIRIGER dir,
    DEPARTEMENTS dpt,
    RESPONSABLE r,
    GAMME g
WHERE
    /* base */
    m.CODEE = e.CODEE
    AND p1.CODEE = e.CODEE
    AND p1.ANNEE = m.ANNEE
    /* qualification (peut y en avoir plusieurs) */
    AND pos.CODEE(+) = e.CODEE
    AND q.CODEQ(+)   = pos.CODEQ
    /* heures */
    AND hu.CODEE(+) = m.CODEE
    AND hu.MOIS(+)  = m.MOIS
    AND hu.ANNEE(+) = m.ANNEE
    AND hpv.CODEE(+) = m.CODEE
    AND hpv.MOIS(+)  = m.MOIS
    AND hpv.ANNEE(+) = m.ANNEE
    /* ventes / rétro (partie objectifs) */
    AND v.CODEE(+) = m.CODEE
    AND v.MOIS(+)  = m.MOIS
    AND v.ANNEE(+) = m.ANNEE
<<<<<<< HEAD
=======

    /* quantités vendues */
    AND ventes_mois.CODEE(+) = m.CODEE
    AND ventes_mois.MOIS(+)  = m.MOIS
    AND ventes_mois.ANNEE(+) = m.ANNEE

    /* quantités fabriquées */
    AND fab_mois.CODEE(+) = m.CODEE
    AND fab_mois.MOIS(+)  = m.MOIS
    AND fab_mois.ANNEE(+) = m.ANNEE

>>>>>>> a5e2ecb (Requêtes SQL)
    /* direction d'un département sur l'année du mois */
    AND dir.CODEE(+) = e.CODEE
    AND dpt.CODED(+) = dir.CODED
    AND (dir.DATEDEBUTDIR IS NULL
         OR EXTRACT(YEAR FROM dir.DATEDEBUTDIR) <= m.ANNEE)
    /* responsable de gamme sur l'année */
    AND r.CODEE(+) = e.CODEE
    AND r.ANNEE(+) = m.ANNEE
    AND g.CODEG(+) = r.CODEG
ORDER BY
    m.ANNEE,
    m.MOIS,
    e.NOME,
    e.PRENOME;