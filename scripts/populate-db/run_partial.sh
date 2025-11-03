#!/usr/bin/env bash
set -Eeuo pipefail

# Script pour générer uniquement QUALIFICATIONS et USINES

ENV_FILE="${1:-.env}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${HERE}/.venv"
PY="${VENV_DIR}/bin/python"
PIP="${VENV_DIR}/bin/pip"
APP="${HERE}/generate_partial.py"

if [[ ! -f "$APP" ]]; then
  echo "❌ Introuvable: ${APP}"
  exit 1
fi

# Cherche le .env à la racine du projet ou dans le dossier courant
if [[ -f "${HERE}/${ENV_FILE}" ]]; then
  ENV_PATH="${HERE}/${ENV_FILE}"
elif [[ -f "${HERE}/../../${ENV_FILE}" ]]; then
  ENV_PATH="${HERE}/../../${ENV_FILE}"
else
  echo "❌ Fichier .env manquant: ${ENV_FILE}"
  echo "Cherché dans ${HERE} et ${HERE}/../.."
  exit 1
fi

echo "🔧 Chargement des variables depuis ${ENV_PATH}"
export ENV_FILE="${ENV_PATH}"

if [[ ! -d "$VENV_DIR" ]]; then
  echo "🐍 Création du venv dans ${VENV_DIR}"
  python3 -m venv "${VENV_DIR}"
  echo "📦 Installation des dépendances"
  "${PIP}" install --upgrade pip >/dev/null
  "${PIP}" install --quiet oracledb python-dotenv
fi

echo "▶️ Génération partielle (QUALIFICATIONS + USINES)..."
"${PY}" "${APP}"

echo "✅ Terminé."
