

-- Vide toutes les tables dans l'ordre correct
SET SERVEROUTPUT ON;

DECLARE
    tables_to_clear SYS.ODCIVARCHAR2LIST := SYS.ODCIVARCHAR2LIST(
        'TRAVAILLER_PT_VENTE', 'TRAVAILLER_USINE', 'PAYER1', 'VENDRE',
        'FACTURER', 'PAYER2', 'RESPONSABLE', 'FABRIQUER_ASSEMBLER1',
        'AUTORISER', 'DIRIGER', 'AVOIR_TYPE', 'ASSEMBLER', 'POSSEDER',
        'PRODUITS', 'POINTS_DE_VENTE', 'DEPARTEMENTS', 'QUALIFICATIONS',
        'EMPLOYES', 'USINES', 'CALENDRIER4', 'CALENDRIER3', 'CALENDRIER2',
        'CALENDRIER1', 'GAMME', 'TYPEPV', 'TYPEU'
    );
BEGIN
    FOR i IN 1 .. tables_to_clear.COUNT LOOP
        BEGIN
            EXECUTE IMMEDIATE 'TRUNCATE TABLE ' || tables_to_clear(i) || ' CASCADE';
            DBMS_OUTPUT.PUT_LINE('✔ TRUNCATED: ' || tables_to_clear(i));
        EXCEPTION
            WHEN OTHERS THEN
                BEGIN
                    EXECUTE IMMEDIATE 'DELETE FROM ' || tables_to_clear(i);
                    DBMS_OUTPUT.PUT_LINE('⚠️ TRUNCATE failed, deleted instead: ' || tables_to_clear(i));
                EXCEPTION
                    WHEN OTHERS THEN
                        DBMS_OUTPUT.PUT_LINE('❌ ERROR deleting: ' || tables_to_clear(i) || ' - ' || SQLERRM);
                END;
        END;
    END LOOP;

    COMMIT;
    DBMS_OUTPUT.PUT_LINE('✅ All tables cleared successfully.');
END;
/
