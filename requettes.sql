-- # Requêtes SQL
-- #
-- #
-- # Lister le nom des gammes de produits n’ayant pas fait l’objet de vente dans des Brico-Express :
-- #

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



-- -- # Pour chaque supermarché, donner son nom, son adresse complète et éventuellement le nombre de salariés qu’elle emploie chaque mois :

-- Supermarché avec employés historisées
SELECT pv.NomPV, pv.RuePV, pv.CPostalPV, pv.VillePV,
       tpv.Année, tpv.Mois,
       COUNT(DISTINCT tpv.CodeE) AS NbSalaries
FROM POINTS_DE_VENTE pv, TRAVAILLER_PT_VENTE tpv
WHERE lower(pv.TypePV) = 'supermarche'
  AND tpv.CodePV = pv.CodePV
GROUP BY pv.NomPV, pv.RuePV, pv.CPostalPV, pv.VillePV, tpv.Année, tpv.Mois

UNION ALL

-- Si jamais y a des supermarchés sans aucun employé
SELECT pv.NomPV, pv.RuePV, pv.CPostalPV, pv.VillePV,
       NULL AS Année, NULL AS Mois, 0 AS NbSalaries
FROM POINTS_DE_VENTE pv
WHERE lower(pv.TypePV) = 'supermarche'
  AND NOT EXISTS (SELECT 1 FROM TRAVAILLER_PT_VENTE t WHERE t.CodePV = pv.CodePV)
ORDER BY NomPV, Année, Mois;






-- # Donner le nom et l’adresse des usines qui autorisent des qualifications qui ne sont possédées par les employés travaillant dans cette usine :

SELECT DISTINCT u.NomU, u.RueU, u.CPostalU, u.VilleU
FROM USINES u
WHERE EXISTS (
  SELECT *
  FROM DEPARTEMENTS d, AUTORISER a
  WHERE d.CodeU = u.CodeU
    AND a.CodeD = d.CodeD
    AND NOT EXISTS (
      SELECT *
      FROM TRAVAILLER_USINE tu, POSSEDER ps
      WHERE tu.CodeD = d.CodeD
        AND ps.CodeE = tu.CodeE
        AND ps.CodeQ = a.CodeQ
    )
);




-- # Donner le nom et le type du points de vente ayant le chiffre d’affaires le plus élevé pour le mois en cours

SELECT pv.NomPV, pv.TypePV,
       SUM(v.Qte_Vendue * f.PrixUnitP) AS ChiffreAffaires
FROM POINTS_DE_VENTE pv, VENDRE v, FACTURER f
WHERE v.CodePV = pv.CodePV
  AND f.CodeP  = v.CodeP
  AND f.Année  = v.Année
  AND f.Mois   = v.Mois
  AND v.Année  = EXTRACT(YEAR FROM CURRENT_DATE)
  AND v.Mois   = EXTRACT(MONTH FROM CURRENT_DATE)
GROUP BY pv.NomPV, pv.TypePV
ORDER BY ChiffreAffaires DESC
FETCH FIRST 1 ROW ONLY;












-- # Donner le nom et le prix unitaire des produits vendus dans le département de la Haute Garonne et mais pas fabriqués dans ce même département (classement par ordre décroissant des prix unitaires)

SELECT DISTINCT p.NomP, fct.PrixUnitP
FROM PRODUITS p, VENDRE v, POINTS_DE_VENTE pv, FACTURER fct
WHERE v.CodeP   = p.CodeP
  AND pv.CodePV = v.CodePV
  AND fct.CodeP = p.CodeP
  AND fct.Année = v.Année
  AND fct.Mois  = v.Mois
  AND pv.CPostalPV LIKE '31%'
  AND NOT EXISTS (
    SELECT *
    FROM "Fabriquer / Assembler 1" fa, USINES u
    WHERE fa.CodeP = p.CodeP
      AND u.CodeU  = fa.CodeU
      AND u.CPostalU LIKE '31%'
  )
ORDER BY fct.PrixUnitP DESC;


-- # Pour les deux dernières années, donner les salaires mensuels des employés (classement par année, nom et prénom des employés)

SELECT p1.Année, e.NomE, e.PrenomE,
       (p1.FixeMensuelE * p1.IndiceSalE) AS SalaireMensuel
FROM PAYER1 p1, EMPLOYES e
WHERE e.CodeE = p1.CodeE
  AND p1.Année >= EXTRACT(YEAR FROM CURRENT_DATE) - 1
ORDER BY p1.Année, e.NomE, e.PrenomE;


-- # Donner le nom de l’usine, son type, sa ville ainsi que le nom d’un département homonyme d’un autre département


SELECT DISTINCT u.NomU, tu.NomTU, u.VilleU, d1.NomD
FROM USINES u, AVOIR_TYPE atp, TYPEU tu, DEPARTEMENTS d1, DEPARTEMENTS d2
WHERE atp.CodeU = u.CodeU
  AND tu.CodeTU = atp.CodeTU
  AND d1.CodeU  = u.CodeU
  AND d2.NomD   = d1.NomD
  AND d2.CodeD <> d1.CodeD
  AND d2.CodeU <> d1.CodeU;
-- #
-- # Penser à mettre les données permettant de vérifier ça dans la base de donées
-- # Donner le nom et le type du point de vente ayant vendu cette année tous les produits de la gamme Cuisine

SELECT pv.NomPV, pv.TypePV
FROM POINTS_DE_VENTE pv
WHERE NOT EXISTS (
  SELECT *
  FROM PRODUITS p, GAMME g
  WHERE g.CodeG = p.CodeG
    AND UPPER(g.NomG) = 'CUISINE'
    AND NOT EXISTS (
      SELECT *
      FROM VENDRE v
      WHERE v.CodePV = pv.CodePV
        AND v.CodeP  = p.CodeP
        AND v.Année  = EXTRACT(YEAR FROM CURRENT_DATE)
    )
);


-- # Donner le nom et le prénom des employés qui, la même année, sont directeur d’un département d’usine et responsable de la gamme de produits fabriqués dans l’usine associé à ce département

SELECT DISTINCT e.NomE, e.PrenomE
FROM EMPLOYES e, DIRIGER d, DEPARTEMENTS dep
WHERE d.CodeE = e.CodeE
  AND dep.CodeD = d.CodeD
  AND EXISTS (
    SELECT 1
    FROM RESPONSABLE r, "Fabriquer / Assembler 1" fa, PRODUITS p
    WHERE r.CodeE = e.CodeE
      AND p.CodeP = fa.CodeP
      AND fa.CodeU = dep.CodeU
      AND p.CodeG  = r.CodeG
      AND EXTRACT(YEAR FROM d.DateDebutDir) = r.Année
      AND EXTRACT(YEAR FROM fa.DateFab)     = r.Année
  );


-- # Donner le nom et l’adresse de l’usine ayant fabriqué le plus de produits non encore vendu cette année

SELECT u.NomU, u.RueU, u.CPostalU, u.VilleU
FROM USINES u
ORDER BY (
  SELECT COALESCE(SUM(
    GREATEST(
      (
        (SELECT COALESCE(SUM(fa.Qte_Fab),0)
         FROM "Fabriquer / Assembler 1" fa
         WHERE fa.CodeU = u.CodeU
           AND fa.CodeP = pf.CodeP
           AND EXTRACT(YEAR FROM fa.DateFab) = EXTRACT(YEAR FROM CURRENT_DATE)
        )
        -
        (SELECT COALESCE(SUM(v.Qte_Vendue),0)
         FROM VENDRE v
         WHERE v.CodeP = pf.CodeP
           AND v.Année = EXTRACT(YEAR FROM CURRENT_DATE)
        )
      ), 0)
  ), 0)
  FROM (
    SELECT DISTINCT fa2.CodeP
    FROM "Fabriquer / Assembler 1" fa2
    WHERE fa2.CodeU = u.CodeU
      AND EXTRACT(YEAR FROM fa2.DateFab) = EXTRACT(YEAR FROM CURRENT_DATE)
  ) pf
) DESC
FETCH FIRST 1 ROW ONLY;

