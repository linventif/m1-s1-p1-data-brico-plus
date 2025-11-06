#!/bin/bash
# -----------------------------------------------------------------------------
# Script : create_oracle_groups.sh
# Description : Create Oracle users (GROUPE_1..13, LA_PLUS_BELLE_TUILE, DATA_LINK_SOLUTION)
#               only if they don't already exist in FREEPDB1
# -----------------------------------------------------------------------------
# Usage : ./create_oracle_groups.sh
# -----------------------------------------------------------------------------

CONTAINER_NAME="oracle-brico-plus"
LOGFILE="oracle_user_creation.log"

echo "===== $(date) : Starting Oracle user creation =====" | tee -a "$LOGFILE"

# Function to run SQL inside the container
run_sql() {
  local sql="$1"
  docker exec -i "$CONTAINER_NAME" sqlplus -s / as sysdba <<SQL
SET PAGESIZE 0 FEEDBACK OFF VERIFY OFF HEADING OFF ECHO OFF
ALTER SESSION SET CONTAINER = FREEPDB1;
${sql}
EXIT;
SQL
}

# Function to create one user safely
create_user_if_missing() {
  local USERNAME="$1"
  local PASSWORD="$2"

  echo "→ Checking user ${USERNAME}..." | tee -a "$LOGFILE"
  EXISTS=$(run_sql "SELECT COUNT(*) FROM dba_users WHERE username='${USERNAME}';")

  if [[ "$EXISTS" -eq 0 ]]; then
    echo "⚙️  Creating user ${USERNAME}..." | tee -a "$LOGFILE"
    run_sql "
      CREATE USER ${USERNAME} IDENTIFIED BY \"${PASSWORD}\"
        DEFAULT TABLESPACE USERS
        TEMPORARY TABLESPACE TEMP
        QUOTA UNLIMITED ON USERS;

      GRANT CONNECT, RESOURCE TO ${USERNAME};
      GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE,
            CREATE TRIGGER, CREATE PROCEDURE TO ${USERNAME};
    "
    echo "✅ User ${USERNAME} created successfully." | tee -a "$LOGFILE"
  else
    echo "ℹ️  User ${USERNAME} already exists, skipping." | tee -a "$LOGFILE"
  fi
}

# Custom users
create_user_if_missing "LA_PLUS_BELLE_TUILE" "Tuile123"
create_user_if_missing "DATA_LINK_SOLUTION" "DataLink"

# Group users GROUPE_1 → GROUPE_13
for i in $(seq 1 13); do
  USER="GROUPE_${i}"
  PASS="Groupe${i}"
  create_user_if_missing "$USER" "$PASS"
done

echo "===== $(date) : All user checks complete =====" | tee -a "$LOGFILE"
