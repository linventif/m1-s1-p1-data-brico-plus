--------------------------------------------------------------------------------
-- 1️⃣  Lister le nom des gammes de produits n’ayant pas fait l’objet de vente
--     dans des Brico-Express
--------------------------------------------------------------------------------
SELECT DISTINCT g.NomG
FROM GAMME g
WHERE NOT EXISTS (
  SELECT *
  FROM PRODUITS p
  JOIN VENDRE v ON v.CodeP = p.CodeP
  JOIN POINTS_DE_VENTE pv ON pv.CodePV = v.CodePV
  WHERE p.CodeG = g.CodeG
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
FROM POINTS_DE_VENTE pv
JOIN TRAVAILLER_PT_VENTE tpv ON tpv.CodePV = pv.CodePV
WHERE LOWER(pv.TypePV) = 'gsb'
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
    SELECT * FROM TRAVAILLER_PT_VENTE t WHERE t.CodePV = pv.CodePV
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
  FROM DEPARTEMENTS d
  JOIN AUTORISER a ON a.CodeD = d.CodeD
  WHERE d.CodeU = u.CodeU
    AND NOT EXISTS (
      SELECT *
      FROM TRAVAILLER_USINE tu
      JOIN POSSEDER ps ON ps.CodeE = tu.CodeE
      WHERE tu.CodeD = d.CodeD
        AND ps.CodeQ = a.CodeQ
    )
);


--------------------------------------------------------------------------------
-- 4️⃣  Donner le nom et le type du point de vente ayant le chiffre d’affaires
--      le plus élevé pour le mois en cours
--------------------------------------------------------------------------------
SELECT pv.NomPV,
       pv.TypePV,
       SUM(v.Qte_Vendue * f.PrixUnitP) AS ChiffreAffaires
FROM POINTS_DE_VENTE pv, VENDRE v, FACTURER f
where v.CodePV = pv.CodePV
AND f.CodeP = v.CodeP
AND f.Annee = v.Annee
AND f.Mois  = v.Mois
WHERE v.Annee = EXTRACT(YEAR FROM CURRENT_DATE)
  AND v.Mois  = EXTRACT(MONTH FROM CURRENT_DATE)
GROUP BY pv.NomPV, pv.TypePV
ORDER BY ChiffreAffaires DESC
FETCH FIRST 1 ROW ONLY;


--------------------------------------------------------------------------------
-- 5️⃣  Produits vendus en Haute-Garonne mais non fabriqués dans ce département
--------------------------------------------------------------------------------
SELECT DISTINCT p.NomP, fct.PrixUnitP
FROM PRODUITS p
JOIN VENDRE v ON v.CodeP = p.CodeP
JOIN POINTS_DE_VENTE pv ON pv.CodePV = v.CodePV
JOIN FACTURER fct
  ON fct.CodeP = p.CodeP
 AND fct.Annee = v.Annee
 AND fct.Mois  = v.Mois
WHERE pv.CPostalPV LIKE '31%'
  AND NOT EXISTS (
    SELECT 1
    FROM FABRIQUER_ASSEMBLER1 fa
    JOIN USINES u ON u.CodeU = fa.CodeU
    WHERE fa.CodeP = p.CodeP
      AND u.CPostalU LIKE '31%'
  )
ORDER BY fct.PrixUnitP DESC;


--------------------------------------------------------------------------------
-- 6️⃣  Pour les deux dernières années, salaires mensuels des employés
--------------------------------------------------------------------------------
SELECT p1.Annee,
       e.NomE,
       e.PrenomE,
       (p1.FixeMensuele * p1.Indicesale) AS SalaireMensuel
FROM PAYER1 p1
JOIN EMPLOYES e ON e.CodeE = p1.CodeE
WHERE p1.Annee >= EXTRACT(YEAR FROM CURRENT_DATE) - 1
ORDER BY p1.Annee, e.NomE, e.PrenomE;


--------------------------------------------------------------------------------
-- 7️⃣  Usine, type, ville et département homonyme d’un autre département
--------------------------------------------------------------------------------
SELECT DISTINCT u.NomU, tu.NomTU, u.VilleU, d1.NomD
FROM USINES u
JOIN AVOIR_TYPE atp ON atp.CodeU = u.CodeU
JOIN TYPEU tu ON tu.CodeTU = atp.CodeTU
JOIN DEPARTEMENTS d1 ON d1.CodeU = u.CodeU
JOIN DEPARTEMENTS d2
  ON d2.NomD = d1.NomD
 AND d2.CodeD <> d1.CodeD
 AND d2.CodeU <> d1.CodeU;


--------------------------------------------------------------------------------
-- 8️⃣  Point de vente ayant vendu cette année tous les produits de la gamme Cuisine
--------------------------------------------------------------------------------
SELECT pv.NomPV, pv.TypePV
FROM POINTS_DE_VENTE pv
WHERE NOT EXISTS (
  SELECT 1
  FROM PRODUITS p
  JOIN GAMME g ON g.CodeG = p.CodeG
  WHERE UPPER(g.NomG) = 'CUISINE'
    AND NOT EXISTS (
      SELECT 1
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
FROM EMPLOYES e
JOIN DIRIGER d ON d.CodeE = e.CodeE
JOIN DEPARTEMENTS dep ON dep.CodeD = d.CodeD
WHERE EXISTS (
  SELECT 1
  FROM RESPONSABLE r
  JOIN FABRIQUER_ASSEMBLER1 fa ON fa.CodeU = dep.CodeU
  JOIN PRODUITS p ON p.CodeP = fa.CodeP
  WHERE r.CodeE = e.CodeE
    AND p.CodeG  = r.CodeG
    AND EXTRACT(YEAR FROM d.DateDebutDir) = r.Annee
    AND EXTRACT(YEAR FROM fa.DateFab)     = r.Annee
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
