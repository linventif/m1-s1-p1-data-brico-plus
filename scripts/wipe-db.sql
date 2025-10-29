SET SERVEROUTPUT ON
BEGIN
  FOR t IN (SELECT table_name FROM user_tables) LOOP
    BEGIN
      EXECUTE IMMEDIATE 'DROP TABLE "' || t.table_name || '" CASCADE CONSTRAINTS';
      DBMS_OUTPUT.PUT_LINE('Dropped table: ' || t.table_name);
    EXCEPTION
      WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Skipped table: ' || t.table_name || ' (' || SQLERRM || ')');
    END;
  END LOOP;
END;
/