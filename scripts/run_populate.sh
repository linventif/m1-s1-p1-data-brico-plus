#!/usr/bin/env bash
set -Eeuo pipefail

# Usage: ./run_populate.sh [fichier_env]
# Ex:    ./run_populate.sh .env.moonoy

ENV_FILE="${1:-.env}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${HERE}/.venv"
PY="${VENV_DIR}/bin/python"
PIP="${VENV_DIR}/bin/pip"
APP="${HERE}/populate-db.py"

if [[ ! -f "$APP" ]]; then
  echo "❌ Introuvable: ${APP}"
  echo "Place ce script dans le même dossier que populate-db.py"
  exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "❌ Fichier .env manquant: ${ENV_FILE}"
  echo "Crée un .env (voir modèles plus bas) puis relance."
  exit 1
fi

echo "🔧 Chargement des variables depuis ${ENV_FILE}"
set -o allexport
# shellcheck disable=SC1090
source "${ENV_FILE}"
set +o allexport

if [[ ! -d "$VENV_DIR" ]]; then
  echo "🐍 Création du venv dans ${VENV_DIR}"
  python3 -m venv "${VENV_DIR}"
fi

echo "📦 Mise à jour des dépendances"
"${PIP}" install --upgrade pip >/dev/null
"${PIP}" install --quiet oracledb

echo "▶️ Lancement du peuplement vers ${ORACLE_USER}@${ORACLE_HOST}:${ORACLE_PORT}/${ORACLE_SERVICE}"
"${PY}" "${APP}"

echo "✅ Terminé."
