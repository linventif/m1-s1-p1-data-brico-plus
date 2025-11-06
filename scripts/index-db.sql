DECLARE
  v_count NUMBER;

  -- petite procédure pour créer un index seulement s'il n'existe pas,
  -- et ignorer si la table est verrouillée
  PROCEDURE create_index_if_needed(
    p_index_name  IN VARCHAR2,
    p_sql         IN VARCHAR2
  ) IS
  BEGIN
    -- l'index existe déjà ?
    SELECT COUNT(*) INTO v_count
    FROM USER_INDEXES
    WHERE INDEX_NAME = UPPER(p_index_name);

    IF v_count = 0 THEN
      BEGIN
        EXECUTE IMMEDIATE p_sql;
      EXCEPTION
        WHEN OTHERS THEN
          -- si c'est un lock (ORA-00054), on ignore et on continue
          IF SQLCODE = -54 THEN
            DBMS_OUTPUT.PUT_LINE('Index ' || p_index_name || ' ignoré : table verrouillée.');
          ELSE
            RAISE; -- autre erreur → on laisse remonter
          END IF;
      END;
    ELSE
      DBMS_OUTPUT.PUT_LINE('Index ' || p_index_name || ' déjà présent, ignoré.');
    END IF;
  END;
BEGIN
  --------------------------------------------------
  -- QUALIFICATIONS
  --------------------------------------------------
  create_index_if_needed(
    'IDX_QUALIFICATIONS_CODEQ_EST_COMPLETEE',
    'CREATE INDEX IDX_QUALIFICATIONS_CODEQ_EST_COMPLETEE ON QUALIFICATIONS (CODEQ_EST_COMPLETEE)'
  );

  --------------------------------------------------
  -- DEPARTEMENTS
  --------------------------------------------------
  create_index_if_needed(
    'IDX_DEPARTEMENTS_CODEU',
    'CREATE INDEX IDX_DEPARTEMENTS_CODEU ON DEPARTEMENTS (CODEU)'
  );

<<<<<<< HEAD
CREATE INDEX IDX_PV_NOM_TYPE ON POINTS_DE_VENTE (NOMPV, TYPEPV);
=======
  --------------------------------------------------
  -- PRODUITS
  --------------------------------------------------
  create_index_if_needed(
    'IDX_PRODUITS_CODEG',
    'CREATE INDEX IDX_PRODUITS_CODEG ON PRODUITS (CODEG)'
  );

  --------------------------------------------------
  -- POSSEDER
  --------------------------------------------------
  create_index_if_needed(
    'IDX_POSSEDER_CODEE',
    'CREATE INDEX IDX_POSSEDER_CODEE ON POSSEDER (CODEE)'
  );
  create_index_if_needed(
    'IDX_POSSEDER_CODEQ',
    'CREATE INDEX IDX_POSSEDER_CODEQ ON POSSEDER (CODEQ)'
  );

  --------------------------------------------------
  -- ASSEMBLER
  --------------------------------------------------
  create_index_if_needed(
    'IDX_ASSEMBLER_CODEP_EST_COMPOSE',
    'CREATE INDEX IDX_ASSEMBLER_CODEP_EST_COMPOSE ON ASSEMBLER (CODEP_EST_COMPOSE)'
  );
  create_index_if_needed(
    'IDX_ASSEMBLER_CODEP_COMPOSE',
    'CREATE INDEX IDX_ASSEMBLER_CODEP_COMPOSE ON ASSEMBLER (CODEP_COMPOSE)'
  );

  --------------------------------------------------
  -- TRAVAILLER_USINE
  --------------------------------------------------
  create_index_if_needed(
    'IDX_TRAVAILLER_USINE_CODEE',
    'CREATE INDEX IDX_TRAVAILLER_USINE_CODEE ON TRAVAILLER_USINE (CODEE)'
  );
  create_index_if_needed(
    'IDX_TRAVAILLER_USINE_CODED',
    'CREATE INDEX IDX_TRAVAILLER_USINE_CODED ON TRAVAILLER_USINE (CODED)'
  );
  create_index_if_needed(
    'IDX_TRAVAILLER_USINE_MOIS_ANNEE',
    'CREATE INDEX IDX_TRAVAILLER_USINE_MOIS_ANNEE ON TRAVAILLER_USINE (MOIS, ANNEE)'
  );

  --------------------------------------------------
  -- AVOIR_TYPE
  --------------------------------------------------
  create_index_if_needed(
    'IDX_AVOIR_TYPE_CODEU',
    'CREATE INDEX IDX_AVOIR_TYPE_CODEU ON AVOIR_TYPE (CODEU)'
  );

  --------------------------------------------------
  -- DIRIGER
  --------------------------------------------------
  create_index_if_needed(
    'IDX_DIRIGER_CODEE',
    'CREATE INDEX IDX_DIRIGER_CODEE ON DIRIGER (CODEE)'
  );
  create_index_if_needed(
    'IDX_DIRIGER_CODED',
    'CREATE INDEX IDX_DIRIGER_CODED ON DIRIGER (CODED)'
  );
  create_index_if_needed(
    'IDX_DIRIGER_DATEDEBUTDIR',
    'CREATE INDEX IDX_DIRIGER_DATEDEBUTDIR ON DIRIGER (DATEDEBUTDIR)'
  );

  --------------------------------------------------
  -- AUTORISER
  --------------------------------------------------
  create_index_if_needed(
    'IDX_AUTORISER_CODEQ',
    'CREATE INDEX IDX_AUTORISER_CODEQ ON AUTORISER (CODEQ)'
  );
  create_index_if_needed(
    'IDX_AUTORISER_CODED',
    'CREATE INDEX IDX_AUTORISER_CODED ON AUTORISER (CODED)'
  );

  --------------------------------------------------
  -- FABRIQUER_ASSEMBLER1
  --------------------------------------------------
  create_index_if_needed(
    'IDX_FABASS1_CODEU',
    'CREATE INDEX IDX_FABASS1_CODEU ON FABRIQUER_ASSEMBLER1 (CODEU)'
  );
  create_index_if_needed(
    'IDX_FABASS1_CODEP',
    'CREATE INDEX IDX_FABASS1_CODEP ON FABRIQUER_ASSEMBLER1 (CODEP)'
  );
  create_index_if_needed(
    'IDX_FABASS1_DATEFAB',
    'CREATE INDEX IDX_FABASS1_DATEFAB ON FABRIQUER_ASSEMBLER1 (DATEFAB)'
  );

  --------------------------------------------------
  -- RESPONSABLE
  --------------------------------------------------
  create_index_if_needed(
    'IDX_RESPONSABLE_CODEE',
    'CREATE INDEX IDX_RESPONSABLE_CODEE ON RESPONSABLE (CODEE)'
  );
  create_index_if_needed(
    'IDX_RESPONSABLE_CODEG_ANNEE',
    'CREATE INDEX IDX_RESPONSABLE_CODEG_ANNEE ON RESPONSABLE (CODEG, ANNEE)'
  );

  --------------------------------------------------
  -- VENDRE
  --------------------------------------------------
  create_index_if_needed(
    'IDX_VENDRE_CODEPV',
    'CREATE INDEX IDX_VENDRE_CODEPV ON VENDRE (CODEPV)'
  );
  create_index_if_needed(
    'IDX_VENDRE_CODEP',
    'CREATE INDEX IDX_VENDRE_CODEP ON VENDRE (CODEP)'
  );
  create_index_if_needed(
    'IDX_VENDRE_MOIS_ANNEE',
    'CREATE INDEX IDX_VENDRE_MOIS_ANNEE ON VENDRE (MOIS, ANNEE)'
  );

  --------------------------------------------------
  -- FACTURER
  --------------------------------------------------
  create_index_if_needed(
    'IDX_FACTURER_MOIS_ANNEE',
    'CREATE INDEX IDX_FACTURER_MOIS_ANNEE ON FACTURER (MOIS, ANNEE)'
  );

  --------------------------------------------------
  -- TRAVAILLER_PT_VENTE
  --------------------------------------------------
  create_index_if_needed(
    'IDX_TRAV_PV_CODEPV',
    'CREATE INDEX IDX_TRAV_PV_CODEPV ON TRAVAILLER_PT_VENTE (CODEPV)'
  );
  create_index_if_needed(
    'IDX_TRAV_PV_MOIS_ANNEE',
    'CREATE INDEX IDX_TRAV_PV_MOIS_ANNEE ON TRAVAILLER_PT_VENTE (MOIS, ANNEE)'
  );

END;
/
>>>>>>> a5e2ecb (Requêtes SQL)
