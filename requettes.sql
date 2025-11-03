--------------------------------------------------------------------------------
-- 1️⃣  Lister le nom des gammes de produits n’ayant pas fait l’objet de vente
--     dans des Brico-Express
--------------------------------------------------------------------------------
SELECT DISTINCT g.NomG
FROM GAMME g
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

-- Supermarchés avec employés historisés
SELECT pv.NomPV,
       pv.RuePV,
       pv.CPostalPV,
       pv.VillePV,
       tpv.Annee,
       tpv.Mois,
       COUNT(DISTINCT tpv.CodeE) AS NbSalaries
FROM POINTS_DE_VENTE pv, TRAVAILLER_PT_VENTE tpv
WHERE pv.CodePV = tpv.CodePV
  AND LOWER(pv.TypePV) = 'gsb'
GROUP BY pv.NomPV, pv.RuePV, pv.CPostalPV, pv.VillePV, tpv.Annee, tpv.Mois

UNION ALL

-- Supermarchés sans employés
SELECT pv.NomPV,
       pv.RuePV,
       pv.CPostalPV,
       pv.VillePV,
       NULL AS Annee,
       NULL AS Mois,
       0 AS NbSalaries
FROM POINTS_DE_VENTE pv
WHERE LOWER(pv.TypePV) = 'gsb'
  AND NOT EXISTS (
    SELECT *
    FROM TRAVAILLER_PT_VENTE t
    WHERE t.CodePV = pv.CodePV
  )
ORDER BY NomPV, Annee, Mois;


--------------------------------------------------------------------------------
-- 3️⃣  Donner le nom et l’adresse des usines qui autorisent des qualifications
--      non possédées par les employés travaillant dans cette usine
--------------------------------------------------------------------------------
SELECT DISTINCT u.NomU, u.RueU, u.CPostalU, u.VilleU
FROM USINES u
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
SELECT
    pv.NomPV,
    pv.TypePV,
    SUM(v.Qte_Vendue * f.PrixUnitP) AS ChiffreAffaires
FROM
    POINTS_DE_VENTE pv,
    VENDRE v,
    FACTURER f
WHERE
    v.CodePV = pv.CodePV
    AND f.CodeP = v.CodeP
    AND f.Annee = v.Annee
    AND f.Mois  = v.Mois
    AND v.Annee = EXTRACT(YEAR FROM CURRENT_DATE)
    AND v.Mois  = EXTRACT(MONTH FROM CURRENT_DATE)
GROUP BY
    pv.NomPV, pv.TypePV
HAVING
    SUM(v.Qte_Vendue * f.PrixUnitP) = (
        SELECT MAX(SUM(v2.Qte_Vendue * f2.PrixUnitP))
        FROM POINTS_DE_VENTE pv2, VENDRE v2, FACTURER f2
        WHERE v2.CodePV = pv2.CodePV
          AND f2.CodeP = v2.CodeP
          AND f2.Annee = v2.Annee
          AND f2.Mois  = v2.Mois
          AND v2.Annee = EXTRACT(YEAR FROM CURRENT_DATE)
          AND v2.Mois  = EXTRACT(MONTH FROM CURRENT_DATE)
        GROUP BY pv2.CodePV
    );


--------------------------------------------------------------------------------
-- 5️⃣  Produits vendus en Haute-Garonne mais non fabriqués dans ce département
--------------------------------------------------------------------------------

SELECT DISTINCT p.NomP, fct.PrixUnitP
FROM PRODUITS p, VENDRE v, POINTS_DE_VENTE pv, FACTURER fct
WHERE p.CodeP = v.CodeP
  AND pv.CodePV = v.CodePV
  AND fct.CodeP = p.CodeP
  AND fct.Annee = v.Annee
  AND fct.Mois  = v.Mois
  AND pv.CPostalPV LIKE '31%'
  AND NOT EXISTS (
    SELECT *
    FROM FABRIQUER_ASSEMBLER1 fa, USINES u
    WHERE fa.CodeU = u.CodeU
      AND fa.CodeP = p.CodeP
      AND u.CPostalU LIKE '31%'
  )
ORDER BY fct.PrixUnitP DESC;

--------------------------------------------------------------------------------
-- 6️⃣  Pour les deux dernières années, salaires mensuels des employés
--------------------------------------------------------------------------------
/* Salaires mensuels (année courante et N-1) – jointures implicites */
WITH
months AS (
  SELECT c.mois, c.annee
  FROM CALENDRIER3 c
  WHERE c.annee IN (EXTRACT(YEAR FROM SYSDATE), EXTRACT(YEAR FROM SYSDATE) - 1)
),
emp_year AS (
  SELECT e.codee, e.nome, e.prenome, p1.annee, p1.fixemensuele, p1.indicesale
  FROM EMPLOYES e, PAYER1 p1
  WHERE p1.codee = e.codee
    AND p1.annee IN (EXTRACT(YEAR FROM SYSDATE), EXTRACT(YEAR FROM SYSDATE) - 1)
),
emp_month AS (
  SELECT ey.codee, ey.nome, ey.prenome, m.mois, m.annee,
         ey.fixemensuele, ey.indicesale
  FROM emp_year ey, months m
  WHERE m.annee = ey.annee
),
heures_tot AS (
  /* PV + Usine, agrégé par (employé, mois, année) */
  SELECT x.codee, x.mois, x.annee, SUM(x.heures) AS heures_total
  FROM (
    SELECT tpv.codee, tpv.mois, tpv.annee, tpv.nbheures_pv AS heures
    FROM TRAVAILLER_PT_VENTE tpv
    WHERE tpv.annee IN (EXTRACT(YEAR FROM SYSDATE), EXTRACT(YEAR FROM SYSDATE) - 1)
    UNION ALL
    SELECT tu.codee, tu.mois, tu.annee, tu.nbheures_u AS heures
    FROM TRAVAILLER_USINE tu
    WHERE tu.annee IN (EXTRACT(YEAR FROM SYSDATE), EXTRACT(YEAR FROM SYSDATE) - 1)
  ) x
  GROUP BY x.codee, x.mois, x.annee
),
commissions AS (
  /* Σ (QTE_VENDUE * PRIXUNITP * INDICERETROCESSIONG) par (employé, mois, année) */
  SELECT v.codee, v.mois, v.annee,
         SUM(v.qte_vendue * f.prixunitp * p2.indiceretrocessiong) AS commission
  FROM VENDRE v, FACTURER f, PRODUITS pr, PAYER2 p2
  WHERE f.codep = v.codep
    AND f.mois  = v.mois
    AND f.annee = v.annee
    AND pr.codep = v.codep
    AND p2.codeg = pr.codeg
    AND p2.annee = v.annee
    AND v.annee IN (EXTRACT(YEAR FROM SYSDATE), EXTRACT(YEAR FROM SYSDATE) - 1)
  GROUP BY v.codee, v.mois, v.annee
)
SELECT
  em.codee,
  em.nome,
  em.prenome,
  em.annee,
  em.mois,
  em.fixemensuele                                   AS partie_fixe,
  (em.indicesale * NVL(ht.heures_total, 0))         AS partie_travail,
  NVL(cms.commission, 0)                            AS partie_objectif,
  em.fixemensuele
  + (em.indicesale * NVL(ht.heures_total, 0))
  + NVL(cms.commission, 0)                          AS salaire_mensuel
FROM emp_month em, heures_tot ht, commissions cms
WHERE ht.codee(+) = em.codee
  AND ht.mois(+)  = em.mois
  AND ht.annee(+) = em.annee
  AND cms.codee(+) = em.codee
  AND cms.mois(+)  = em.mois
  AND cms.annee(+) = em.annee
ORDER BY em.annee, em.nome, em.prenome, em.mois;



--------------------------------------------------------------------------------
-- 7️⃣  Usine, type, ville et département homonyme d’un autre département
--------------------------------------------------------------------------------
SELECT DISTINCT u.NomU, tu.NomTU, u.VilleU, d1.NomD
FROM USINES u, AVOIR_TYPE atp, TYPEU tu, DEPARTEMENTS d1, DEPARTEMENTS d2
WHERE atp.CodeU = u.CodeU
  AND tu.CodeTU = atp.CodeTU
  AND d1.CodeU = u.CodeU
  AND d2.NomD = d1.NomD
  AND d2.CodeD <> d1.CodeD
  AND d2.CodeU <> d1.CodeU;


--------------------------------------------------------------------------------
-- 8️⃣  Point de vente ayant vendu cette année tous les produits de la gamme Cuisine
--------------------------------------------------------------------------------
SELECT pv.NomPV, pv.TypePV
FROM POINTS_DE_VENTE pv
WHERE NOT EXISTS (
  SELECT *
  FROM PRODUITS p, GAMME g
  WHERE g.CodeG = p.CodeG
    AND lower(g.NomG) = 'cuisine'
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
SELECT DISTINCT e.NomE, e.PrenomE
FROM EMPLOYES e, DIRIGER d, DEPARTEMENTS dep
WHERE d.CodeE = e.CodeE
  AND dep.CodeD = d.CodeD
  AND EXISTS (
    SELECT *
    FROM RESPONSABLE r, FABRIQUER_ASSEMBLER1 fa, PRODUITS p
    WHERE fa.CodeU = dep.CodeU
      AND p.CodeP = fa.CodeP
      AND r.CodeE = e.CodeE
      AND p.CodeG = r.CodeG
      AND EXTRACT(YEAR FROM d.DateDebutDir) = r.Annee
      AND EXTRACT(YEAR FROM fa.DateFab) = r.Annee
  );


--------------------------------------------------------------------------------
-- 🔟  Usine ayant fabriqué le plus de produits non encore vendus cette année
--------------------------------------------------------------------------------
SELECT u.NomU, u.RueU, u.CPostalU, u.VilleU
FROM USINES u
ORDER BY (
  SELECT COALESCE(SUM(GREATEST(
    (SELECT COALESCE(SUM(fa.Qte_Fab), 0)
     FROM FABRIQUER_ASSEMBLER1 fa
     WHERE fa.CodeU = u.CodeU
       AND fa.CodeP = pf.CodeP
       AND EXTRACT(YEAR FROM fa.DateFab) = EXTRACT(YEAR FROM CURRENT_DATE))
    -
    (SELECT COALESCE(SUM(v.Qte_Vendue), 0)
     FROM VENDRE v
     WHERE v.CodeP = pf.CodeP
       AND v.Annee = EXTRACT(YEAR FROM CURRENT_DATE))
  ,0)),0)
  FROM (
    SELECT DISTINCT fa2.CodeP
    FROM FABRIQUER_ASSEMBLER1 fa2
    WHERE fa2.CodeU = u.CodeU
      AND EXTRACT(YEAR FROM fa2.DateFab) = EXTRACT(YEAR FROM CURRENT_DATE)
  ) pf
) DESC
FETCH FIRST 1 ROW ONLY;
