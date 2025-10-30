#!/usr/bin/env bash
set -euo pipefail

# Config - update if needed
CONTAINER_NAME="oracle-brico-plus"   # docker container name
HOST="localhost"                     # host reachable from inside container (or external IP)
PORT="15210"                         # listener port (as you provided earlier)
SERVICE="FREEPDB1"                   # service name / PDB

LOGFILE="fetch_db_users.log"
: > "$LOGFILE"

# === User:password list (declare or modify as needed) ===
declare -A ORACLE_USERS=(
  [LA_PLUS_BELLE_TUILE]="Tuile123"
  [DATA_LINK_SOLUTION]="DataLink"
  [GROUPE_1]="Groupe1"
  [GROUPE_2]="Groupe2"
  [GROUPE_3]="Groupe3"
  [GROUPE_4]="Groupe4"
  [GROUPE_5]="Groupe5"
  [GROUPE_6]="Groupe6"
  [GROUPE_7]="Groupe7"
  [GROUPE_8]="Groupe8"
  [GROUPE_9]="Groupe9"
  [GROUPE_10]="Groupe10"
  [GROUPE_11]="Groupe11"
  [GROUPE_12]="Groupe12"
  [GROUPE_13]="Groupe13"
)

echo "=== $(date) : Starting user existence & connectivity checks ===" | tee -a "$LOGFILE"

# Helper: run SQL in container (as SYSDBA) to check user existence in FREEPDB1
user_exists_in_pdb() {
  local username="$1"
  docker exec -i "$CONTAINER_NAME" sqlplus -s / as sysdba <<SQL
SET PAGESIZE 0 FEEDBACK OFF VERIFY OFF HEADING OFF ECHO OFF
ALTER SESSION SET CONTAINER = $SERVICE;
SELECT COUNT(*) FROM dba_users WHERE username = UPPER('${username}');
EXIT;
SQL
}

# Helper: try to connect as a user (returns 0 on success, non-zero on failure)
try_connect_user() {
  local username="$1"
  local password="$2"
  # We'll attempt a silent sqlplus connection to the PDB using the thin connect string.
  # WARNING: this will expose username/password in the commandline inside the container while running.
  docker exec -i "$CONTAINER_NAME" bash -c "echo exit | sqlplus -s ${username}/${password}@//${HOST}:${PORT}/${SERVICE}" >/dev/null 2>&1
}

# Iterate users
for user in "${!ORACLE_USERS[@]}"; do
  pass="${ORACLE_USERS[$user]}"
#  echo "Checking user: $user" | tee -a "$LOGFILE"

  # 1) Does the user exist in the PDB?
  exists=$(user_exists_in_pdb "$user" | tr -d '[:space:]')
  if [[ -z "$exists" ]]; then
#    echo "  ❌ Could not query dba_users for $user (unexpected result)." | tee -a "$LOGFILE"
    continue
  fi

  if [[ "$exists" -eq 0 ]]; then
#    echo "  - User $user does NOT exist in PDB $SERVICE." | tee -a "$LOGFILE"
    continue
  fi

#  echo "  - User $user exists in PDB $SERVICE." | tee -a "$LOGFILE"

  # 2) Try to connect using provided password
  if try_connect_user "$user" "$pass"; then
    # connection successful
   echo "${user}:${pass}" | tee -a "$LOGFILE"
#  else
 #   echo "  ⚠️  CONNECT FAIL -> ${user} (password may be wrong or CREATE SESSION missing)" | tee -a "$LOGFILE"
  fi
done

echo "=== $(date) : Done. See $LOGFILE for details ===" | tee -a "$LOGFILE"
